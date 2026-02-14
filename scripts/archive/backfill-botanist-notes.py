#!/usr/bin/env python3
"""
backfill-botanist-notes.py
==========================
Generates taxonomyFeedback (botanist's notes) for specimens that are missing them.
Reads each specimen's existing data, sends it to a Claude agent for analysis,
and writes the notes back into the specimen JSON.

Does NOT search the web — purely analytical, based on existing specimen data.

Usage:
    python3 scripts/backfill-botanist-notes.py                 # Run all missing
    python3 scripts/backfill-botanist-notes.py --dry-run       # Show queue only
    python3 scripts/backfill-botanist-notes.py --specimen tesla # One specimen
    python3 scripts/backfill-botanist-notes.py --skip-permissions

Run from project root: orgtransformation/
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path
from textwrap import dedent

# ─── Configuration ───────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
SPECIMENS_DIR = PROJECT_ROOT / "specimens"

TIMEOUT_SECONDS = 5 * 60   # 5 minutes — no web fetching, pure analysis
PAUSE_BETWEEN = 3           # seconds between agents

EXCLUDED_FILES = {"registry.json", "_template.json", "specimen-schema.json", "source-registry.json"}

# ─── Logging ─────────────────────────────────────────────────────────────────

log = logging.getLogger("backfill-notes")
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(handler)

# ─── Taxonomy Context ────────────────────────────────────────────────────────

TAXONOMY = """\
Structural Models (9 models × 3 orientations):
  M1 Research Lab — Fundamental research, breakthroughs. 3-10 year horizon.
  M2 Center of Excellence — Governance, standards, enablement. 6-24 months.
  M3 Embedded Teams — Product-specific AI features. Quarterly cadence.
  M4 Hybrid/Hub-and-Spoke — Central standards + distributed execution.
  M5 Product/Venture Lab — Commercialize AI into products/ventures.
     5a Internal Incubator | 5b Venture Builder | 5c Platform-to-Product
  M6 Unnamed/Informal — Quiet transformation without formal AI structure.
     6a Enterprise-Wide Adoption | 6b Centralized-but-Unnamed | 6c Grassroots
  M7 Tiger Teams — Time-boxed exploration sprints.
  M8 Skunkworks — Autonomous unit with radical independence.
  M9 AI-Native — Born-AI organization, no legacy to transform.

Orientations: Structural | Contextual | Temporal

Mechanisms: 1-Protect Off-Strategy Work, 3-Embed Product at Research Frontier,
  4-Consumer-Grade UX for Employee Tools, 5-Deploy to Thousands Before You Know,
  6-Merge Competing AI Teams, 7-Put Executives on the Tools,
  8-Turn Compliance Into Deployment Advantage, 10-Productize Internal Advantages,
  11-Flatten Management Layers

Tensions (each scored -1 to +1):
  structuralVsContextual, speedVsDepth, centralVsDistributed,
  namedVsQuiet, longVsShortHorizon"""

MODEL_NAMES = {
    1: "Research Lab", 2: "Center of Excellence", 3: "Embedded Teams",
    4: "Hybrid/Hub-and-Spoke", 5: "Product/Venture Lab", 6: "Unnamed/Informal",
    7: "Tiger Teams", 8: "Skunkworks", 9: "AI-Native",
}

# ─── Queue ───────────────────────────────────────────────────────────────────

def find_missing_specimens() -> list[str]:
    """Find specimen IDs that have empty or missing taxonomyFeedback."""
    missing = []
    for f in sorted(SPECIMENS_DIR.iterdir()):
        if f.name in EXCLUDED_FILES or not f.name.endswith(".json"):
            continue
        with open(f) as fh:
            spec = json.load(fh)
        tf = spec.get("taxonomyFeedback", [])
        if not tf or len(tf) == 0:
            missing.append(f.stem)
    return missing


# ─── Prompt ──────────────────────────────────────────────────────────────────

def build_prompt(specimen_id: str, spec: dict) -> str:
    """Build a focused prompt for generating botanist's notes."""
    today = date.today().isoformat()
    spec_json = json.dumps(spec, indent=2)
    specimen_path = str(SPECIMENS_DIR / f"{specimen_id}.json")

    model_num = spec.get("classification", {}).get("structuralModel", "?")
    model_name = MODEL_NAMES.get(model_num, "Unknown") if isinstance(model_num, int) else "?"
    orientation = spec.get("classification", {}).get("orientation", "?")

    prompt = dedent(f"""\
    You are a research botanist for the Ambidexterity Field Guide — a study of how
    organizations structurally enable both AI exploration and operational execution.

    TASK: Read the specimen below and write 2-3 substantive analytical observations
    (botanist's notes) into the `taxonomyFeedback` array. Then write the updated
    specimen JSON back to {specimen_path}.

    ## RULES
    1. Do NOT search the web. Work only from the specimen data below.
    2. Do NOT change any other fields — only add `taxonomyFeedback` entries.
    3. Prefix each note with "[{today[:7]}]" for temporal tracking.
    4. Write the COMPLETE specimen JSON to {specimen_path} (not just the notes).

    ## TAXONOMY CONTEXT
    {TAXONOMY}

    This specimen is classified as: M{model_num} {model_name} | {orientation}

    ## WHAT MAKES A GOOD BOTANIST'S NOTE
    These are NOT summaries. They are analytical observations about:
    - How does this specimen fit or challenge the taxonomy? Edge cases?
    - What is most structurally interesting or surprising?
    - Patterns that connect to other specimens or challenge expectations
    - Why this org's AI structure makes economic/organizational sense (or doesn't)
    - What mechanisms are at work and what's distinctive about how they manifest here

    Bad: "Apple uses a hub-and-spoke model for AI." (this is just description)
    Good: "Apple's functional org structure creates an unusual M4 variant where spokes
    are expertise-based (design, engineering, services) rather than product-based — a
    pattern not seen in other M4 specimens, which typically organize spokes by business
    unit or geography."

    ## SPECIMEN DATA
    {spec_json}

    ## OUTPUT
    Write the complete updated JSON to: {specimen_path}
    The ONLY change should be a populated `taxonomyFeedback` array with 2-3 entries.

    After writing, output this line to stdout:
    BACKFILL_RESULT: {specimen_id} | {{n_notes}} notes
    """)

    return prompt


# ─── Agent Runner ────────────────────────────────────────────────────────────

def run_agent(specimen_id: str, prompt: str, skip_permissions: bool = False) -> bool:
    """Run a Claude agent. Returns True if specimen file was updated."""
    log.info(f"▶ Starting: {specimen_id}")
    start = time.time()

    cmd = ["claude", "-p", prompt, "--model", "sonnet"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=TIMEOUT_SECONDS, cwd=str(PROJECT_ROOT),
        )
        elapsed = time.time() - start

        # Verify the specimen file was updated with taxonomyFeedback
        spec_path = SPECIMENS_DIR / f"{specimen_id}.json"
        try:
            with open(spec_path) as f:
                updated = json.load(f)
            tf = updated.get("taxonomyFeedback", [])
            if tf and len(tf) > 0:
                log.info(f"✓ {specimen_id}: {len(tf)} notes in {elapsed:.0f}s")
                return True
            else:
                log.error(f"✗ {specimen_id}: File written but taxonomyFeedback still empty")
                return False
        except (json.JSONDecodeError, FileNotFoundError):
            log.error(f"✗ {specimen_id}: File not found or invalid after agent run")
            return False

    except subprocess.TimeoutExpired:
        log.error(f"✗ {specimen_id}: TIMEOUT after {TIMEOUT_SECONDS}s")
        return False
    except Exception as e:
        log.error(f"✗ {specimen_id}: Exception: {e}")
        return False


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Backfill botanist's notes for specimens")
    parser.add_argument("--dry-run", action="store_true", help="Show queue only")
    parser.add_argument("--specimen", type=str, help="Backfill one specific specimen")
    parser.add_argument("--skip-permissions", action="store_true")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("BOTANIST NOTES BACKFILL")
    log.info("=" * 60)

    if args.specimen:
        queue = [args.specimen]
    else:
        queue = find_missing_specimens()

    log.info(f"Queue: {len(queue)} specimens missing taxonomyFeedback")

    if args.dry_run:
        for i, sid in enumerate(queue, 1):
            spec_path = SPECIMENS_DIR / f"{sid}.json"
            if spec_path.exists():
                with open(spec_path) as f:
                    spec = json.load(f)
                cls = spec.get("classification", {})
                model = cls.get("structuralModel", "?")
                name = MODEL_NAMES.get(model, "?") if isinstance(model, int) else "?"
                n_quotes = len(spec.get("quotes", []))
                n_sources = len(spec.get("sources", []))
                log.info(f"  {i:2d}. {sid:35s} | M{model} {name:25s} | {n_quotes} quotes | {n_sources} sources")
            else:
                log.info(f"  {i:2d}. {sid:35s} | NO FILE")
        return

    # Run
    start_time = datetime.now()
    results = []

    for i, specimen_id in enumerate(queue, 1):
        log.info(f"\n--- [{i}/{len(queue)}] {specimen_id} ---")

        spec_path = SPECIMENS_DIR / f"{specimen_id}.json"
        if not spec_path.exists():
            log.error(f"Specimen file not found: {spec_path}")
            results.append({"id": specimen_id, "success": False})
            continue

        with open(spec_path) as f:
            spec = json.load(f)

        prompt = build_prompt(specimen_id, spec)
        success = run_agent(specimen_id, prompt, args.skip_permissions)
        results.append({"id": specimen_id, "success": success})

        if i < len(queue):
            time.sleep(PAUSE_BETWEEN)

    # Summary
    elapsed = datetime.now() - start_time
    succeeded = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    log.info("\n" + "=" * 60)
    log.info("BACKFILL COMPLETE")
    log.info("=" * 60)
    log.info(f"Duration: {elapsed.total_seconds() / 60:.1f} minutes")
    log.info(f"Succeeded: {len(succeeded)}/{len(results)}")
    if failed:
        log.info(f"Failed: {[r['id'] for r in failed]}")


if __name__ == "__main__":
    main()
