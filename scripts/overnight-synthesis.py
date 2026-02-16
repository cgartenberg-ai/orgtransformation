#!/usr/bin/env python3
"""
overnight-synthesis.py
======================
Autonomous synthesis engine for the nightly pipeline.
Reads specimens from the synthesis queue, invokes Claude to score them against
tensions and contingencies, then commits results to synthesis/*.json with
field journal entries as audit trail.

Usage:
    python3 scripts/overnight-synthesis.py                      # Process pending queue
    python3 scripts/overnight-synthesis.py --dry-run             # Show what would be processed
    python3 scripts/overnight-synthesis.py --limit 4             # Process at most 4
    python3 scripts/overnight-synthesis.py --specimen nike       # Process one specimen
    python3 scripts/overnight-synthesis.py --skip-permissions    # Unattended mode

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

# ─── Shared Library ─────────────────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import (
    save_json, load_json, acquire_lock, release_lock,
    preflight_check, setup_logging, write_changelog,
    PROJECT_ROOT, BLOCKED_DOMAINS,
)

# ─── Configuration ───────────────────────────────────────────────────────────

SPECIMENS_DIR = PROJECT_ROOT / "specimens"
SYNTHESIS_DIR = PROJECT_ROOT / "synthesis"
SYNTHESIS_QUEUE = PROJECT_ROOT / "curation" / "synthesis-queue.json"
TENSIONS_PATH = SYNTHESIS_DIR / "tensions.json"
CONTINGENCIES_PATH = SYNTHESIS_DIR / "contingencies.json"
MECHANISMS_PATH = SYNTHESIS_DIR / "mechanisms.json"
INSIGHTS_PATH = SYNTHESIS_DIR / "insights.json"
REPORTS_DIR = PROJECT_ROOT / "pipeline-reports"

TIMEOUT_SECONDS = 15 * 60   # 15 minutes per specimen
PAUSE_BETWEEN = 5
MAX_RETRIES = 1

# ─── Logging ─────────────────────────────────────────────────────────────────

log = setup_logging("overnight-synthesis")

# ─── Tension & Contingency Definitions (for agent prompts) ───────────────────

TENSION_DEFS = """
T1: Structural Separation vs. Contextual Integration (-1.0 to +1.0)
  -1.0 = Full structural separation (dedicated AI units)
  +1.0 = Full contextual integration (everyone does AI)
  fieldName: structuralVsContextual

T2: Speed vs. Depth (-1.0 to +1.0)
  -1.0 = Depth-first (careful, deliberate, research-oriented)
  +1.0 = Speed-first (rapid deployment, move fast)
  fieldName: speedVsDepth

T3: Central vs. Distributed (-1.0 to +1.0)
  -1.0 = Centralized AI governance/capability
  +1.0 = Distributed/federated AI capability
  fieldName: centralVsDistributed

T4: Named vs. Quiet (-1.0 to +1.0)
  -1.0 = Named, branded AI units (visible, marketed)
  +1.0 = Quiet transformation (no formal AI branding)
  fieldName: namedVsQuiet

T5: Long vs. Short Horizon (-1.0 to +1.0)
  -1.0 = Long-horizon focus (multi-year, research)
  +1.0 = Short-horizon focus (quarterly, operational)
  fieldName: longVsShortHorizon
"""

CONTINGENCY_DEFS = """
C1: regulatoryIntensity — How much regulation affects AI deployment (high/medium/low)
C2: timeToObsolescence — How fast the core business faces disruption (high=fast/medium/low=slow)
C3: ceoTenure — CEO/leader tenure and stability (high=long/medium/low=short)
C4: talentMarketPosition — Access to AI talent (high/medium/low)
C5: technicalDebt — Legacy system burden (high/medium/low)
C6: environmentalAiPull — External pressure to adopt AI (high/medium/low)
"""


# ─── Queue Management ────────────────────────────────────────────────────────

def load_synthesis_queue(specimen_filter: str | None = None) -> list[dict]:
    """Load pending specimens from the synthesis queue."""
    if not SYNTHESIS_QUEUE.exists():
        log.warning("synthesis-queue.json not found")
        return []
    data = load_json(SYNTHESIS_QUEUE)
    queue = data.get("queue", [])
    pending = [q for q in queue if q.get("status") == "pending"]

    if specimen_filter:
        pending = [q for q in pending if q["specimenId"] == specimen_filter]

    return pending


def mark_synthesized(specimen_id: str):
    """Mark a specimen as synthesized in the queue."""
    data = load_json(SYNTHESIS_QUEUE)
    for q in data.get("queue", []):
        if q["specimenId"] == specimen_id and q.get("status") == "pending":
            q["status"] = "synthesized"
            q["synthesizedIn"] = f"overnight-synthesis-{date.today().isoformat()}"
            break
    data["lastUpdated"] = date.today().isoformat()
    save_json(SYNTHESIS_QUEUE, data)


# ─── Agent Prompt Builder ────────────────────────────────────────────────────

def build_synthesis_prompt(specimen_id: str) -> str:
    """Build a prompt for the synthesis agent to score one specimen."""
    spec_file = SPECIMENS_DIR / f"{specimen_id}.json"
    if not spec_file.exists():
        log.error(f"Specimen file not found: {spec_file}")
        return ""

    spec = load_json(spec_file)
    today = date.today().isoformat()

    # Extract key info
    name = spec.get("name", specimen_id)
    cls = spec.get("classification", {})
    model = cls.get("structuralModel", "?")
    model_name = cls.get("structuralModelName", "?")
    orientation = cls.get("orientation", "?")
    confidence = cls.get("confidence", "?")
    desc = spec.get("description", "")[:500]
    industry = spec.get("habitat", {}).get("industry", "?")

    markers = spec.get("observableMarkers", {})
    markers_str = ""
    for key in ("reportingStructure", "resourceAllocation", "timeHorizons",
                "decisionRights", "metrics"):
        val = markers.get(key, "")
        if val:
            markers_str += f"  {key}: {val[:200]}\n"

    # Extract key people from quotes (no top-level keyPeople field in schema)
    speakers = {}
    for q in spec.get("quotes", []):
        name = q.get("speaker")
        if name and name not in speakers:
            speakers[name] = q.get("speakerTitle", "?")
    people_str = ", ".join(f"{n} ({t})" for n, t in list(speakers.items())[:6])

    output_path = str(REPORTS_DIR / f"synth-{specimen_id}.json")

    prompt = dedent(f"""\
    You are a synthesis agent scoring the specimen "{name}" ({specimen_id}) against
    the ambidexterity field guide's tension and contingency frameworks.
    COMPLETE THIS IN UNDER 10 MINUTES.

    ## Specimen Context

    - ID: {specimen_id}
    - Name: {name}
    - Model: M{model} ({model_name})
    - Orientation: {orientation}
    - Confidence: {confidence}
    - Industry: {industry}
    - Key people: {people_str}
    - Description: {desc}

    Observable Markers:
    {markers_str}

    ## Tension Definitions

    {TENSION_DEFS}

    ## Contingency Definitions

    {CONTINGENCY_DEFS}

    ## TASK

    Score this specimen against ALL 5 tensions and ALL 6 contingencies.
    For each, provide:
    1. A numeric score (tensions: -1.0 to +1.0) or bucket (contingencies: high/medium/low)
    2. A one-sentence evidence rationale
    3. Whether you found any cross-cutting patterns with other specimens

    Also check: does this specimen illuminate any new insight about how organizations
    structure AI work? If so, describe the insight with evidence from this specimen
    and any others you can reference.

    ## Output

    Write a JSON file to: {output_path}

    {{
      "specimenId": "{specimen_id}",
      "specimenName": "{name}",
      "synthesizedDate": "{today}",

      "tensions": {{
        "structuralVsContextual": {{
          "position": 0.0,
          "evidence": "One-sentence rationale"
        }},
        "speedVsDepth": {{
          "position": 0.0,
          "evidence": "One-sentence rationale"
        }},
        "centralVsDistributed": {{
          "position": 0.0,
          "evidence": "One-sentence rationale"
        }},
        "namedVsQuiet": {{
          "position": 0.0,
          "evidence": "One-sentence rationale"
        }},
        "longVsShortHorizon": {{
          "position": 0.0,
          "evidence": "One-sentence rationale"
        }}
      }},

      "contingencies": {{
        "regulatoryIntensity": {{ "bucket": "high|medium|low", "rationale": "..." }},
        "timeToObsolescence": {{ "bucket": "high|medium|low", "rationale": "..." }},
        "ceoTenure": {{ "bucket": "high|medium|low", "rationale": "..." }},
        "talentMarketPosition": {{ "bucket": "high|medium|low", "rationale": "..." }},
        "technicalDebt": {{ "bucket": "high|medium|low", "rationale": "..." }},
        "environmentalAiPull": {{ "bucket": "high|medium|low", "rationale": "..." }}
      }},

      "mechanisms": [
        {{
          "mechanismId": 1,
          "strength": "Strong|Moderate|Weak",
          "notes": "How this specimen exemplifies the mechanism"
        }}
      ],

      "newInsight": {{
        "hasInsight": false,
        "title": "Short title if insight found",
        "finding": "Description of the insight",
        "evidence": ["specimen IDs that support this"],
        "confidence": "HIGH|MEDIUM|LOW"
      }},

      "fieldJournal": "3-5 sentence analytical note: what is most structurally interesting about this specimen? What patterns does it confirm or challenge?"
    }}

    IMPORTANT:
    - Use the full -1.0 to +1.0 range for tensions. 0.0 means balanced or insufficient data.
    - Only propose a new insight if confidence >= MEDIUM and backed by >= 2 specimens.
    - The fieldJournal is the most important output — it's the audit trail.
    """)

    return prompt


# ─── Agent Runner ────────────────────────────────────────────────────────────

def run_synthesis_agent(specimen_id: str, prompt: str,
                        skip_permissions: bool = False) -> dict | None:
    """Run a synthesis agent for one specimen. Returns parsed results or None."""
    log.info(f"▶ Synthesizing: {specimen_id}")
    start = time.time()
    output_path = REPORTS_DIR / f"synth-{specimen_id}.json"

    cmd = ["claude", "-p", prompt, "--model", "opus"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, cwd=str(PROJECT_ROOT), start_new_session=True,
        )
        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            import signal
            try:
                pgid = os.getpgid(proc.pid)
                os.killpg(pgid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(pgid, signal.SIGKILL)
                    proc.wait(timeout=5)
            except (ProcessLookupError, OSError):
                pass
            log.error(f"✗ {specimen_id}: TIMEOUT after {time.time()-start:.0f}s")
            return None

        elapsed = time.time() - start
        if output_path.exists():
            try:
                result = load_json(output_path)
                log.info(f"✓ {specimen_id}: synthesized in {elapsed:.0f}s")
                return result
            except Exception:
                log.error(f"✗ {specimen_id}: output exists but invalid JSON")
                output_path.unlink()
                return None
        else:
            log.error(f"✗ {specimen_id}: no output after {elapsed:.0f}s (exit={proc.returncode})")
            return None

    except Exception as e:
        log.error(f"✗ {specimen_id}: Exception: {e}")
        return None


# ─── Apply Results to Synthesis Files ────────────────────────────────────────

def apply_synthesis_result(result: dict, dry_run: bool = False) -> list[str]:
    """Apply one synthesis result to the synthesis JSON files.
    Returns list of change descriptions for the field journal."""
    changes = []
    specimen_id = result["specimenId"]

    # ── Tensions ──────────────────────────────────────────────────────
    tensions_data = load_json(TENSIONS_PATH)
    tension_map = {t["fieldName"]: t for t in tensions_data["tensions"]}

    for field_name, scoring in result.get("tensions", {}).items():
        if field_name not in tension_map:
            continue
        t = tension_map[field_name]
        position = scoring.get("position")
        evidence = scoring.get("evidence", "")
        if position is None:
            continue

        existing_ids = {s["specimenId"] for s in t["specimens"]}
        if specimen_id not in existing_ids:
            t["specimens"].append({
                "specimenId": specimen_id,
                "position": position,
                "evidence": evidence,
            })
            changes.append(f"T{t['id']} {field_name}: placed at {position}")
        else:
            # Update existing position with latest synthesis
            for s in t["specimens"]:
                if s["specimenId"] == specimen_id:
                    old = s.get("position")
                    if old != position or s.get("evidence") != evidence:
                        s["position"] = position
                        s["evidence"] = evidence
                        changes.append(f"T{t['id']} {field_name}: {old} → {position}")
                    break

    if not dry_run and changes:
        tensions_data["lastUpdated"] = date.today().isoformat()
        save_json(TENSIONS_PATH, tensions_data)

    # ── Contingencies ─────────────────────────────────────────────────
    cont_data = load_json(CONTINGENCIES_PATH)
    cont_map = {c["id"]: c for c in cont_data["contingencies"]}
    cont_changes = []

    for cont_id, scoring in result.get("contingencies", {}).items():
        if cont_id not in cont_map:
            continue
        c = cont_map[cont_id]
        bucket = scoring.get("bucket", "").lower()
        if bucket not in ("high", "medium", "low"):
            continue

        # Check if already placed
        all_specimens = set()
        for b in ("high", "medium", "low"):
            if b in c:
                all_specimens.update(c[b].get("specimens", []))

        if specimen_id not in all_specimens:
            c.setdefault(bucket, {}).setdefault("specimens", []).append(specimen_id)
            cont_changes.append(f"C:{cont_id} → {bucket}")

    if not dry_run and cont_changes:
        cont_data["lastUpdated"] = date.today().isoformat()
        save_json(CONTINGENCIES_PATH, cont_data)
    changes.extend(cont_changes)

    # ── Mechanisms ────────────────────────────────────────────────────
    mech_data = load_json(MECHANISMS_PATH)
    mech_map = {m["id"]: m for m in mech_data.get("confirmed", [])}
    mech_changes = []

    for mech_entry in result.get("mechanisms", []):
        mech_id = mech_entry.get("mechanismId")
        if mech_id not in mech_map:
            continue
        m = mech_map[mech_id]
        existing = set(m.get("specimens", []))
        if specimen_id not in existing:
            m["specimens"].append(specimen_id)
            strength = mech_entry.get("strength", "Moderate")
            notes = mech_entry.get("notes", "")
            m.setdefault("evidence", []).append({
                "specimenId": specimen_id,
                "quote": None,
                "speaker": None,
                "source": f"overnight-synthesis {date.today().isoformat()}",
                "notes": f"[{strength}] {notes}",
            })
            mech_changes.append(f"M{mech_id} ← {specimen_id} ({strength})")

    if not dry_run and mech_changes:
        mech_data["lastUpdated"] = date.today().isoformat()
        save_json(MECHANISMS_PATH, mech_data)
    changes.extend(mech_changes)

    # ── Insights ──────────────────────────────────────────────────────
    insight_data = result.get("newInsight", {})
    if insight_data.get("hasInsight") and insight_data.get("confidence", "").upper() in ("HIGH", "MEDIUM"):
        insights_file = load_json(INSIGHTS_PATH)
        existing_ids = {i["id"] for i in insights_file.get("insights", [])}
        title = insight_data.get("title", "")
        insight_id = title.lower().replace(" ", "-").replace("'", "")[:60]
        if insight_id and insight_id not in existing_ids:
            new_insight = {
                "id": insight_id,
                "title": title,
                "theme": "organizational-form",
                "finding": insight_data.get("finding", ""),
                "evidence": [{"specimenId": sid, "note": ""} for sid in insight_data.get("evidence", [])],
                "theoreticalConnection": "",
                "discoveredIn": f"overnight-synthesis/{date.today().isoformat()}",
                "relatedTensions": [],
                "maturity": "hypothesis",
            }
            insights_file["insights"].append(new_insight)
            if not dry_run:
                insights_file["lastUpdated"] = date.today().isoformat()
                save_json(INSIGHTS_PATH, insights_file)
            changes.append(f"New insight: {title}")

    return changes


# ─── Field Journal ───────────────────────────────────────────────────────────

def write_field_journal(entries: list[dict]):
    """Write field journal entries to pipeline-reports/YYYY-MM-DD-field-journal.md."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    journal_path = REPORTS_DIR / f"{date.today().isoformat()}-field-journal.md"

    content = f"## Field Journal — {date.today().isoformat()} (Autonomous Synthesis)\n\n"

    for entry in entries:
        content += f"### Specimen: {entry['specimen_id']} ({entry.get('name', '')})\n"
        content += f"**Model:** M{entry.get('model', '?')} | **Orientation:** {entry.get('orientation', '?')}\n\n"

        if entry.get("changes"):
            content += "**Changes applied:**\n"
            for c in entry["changes"]:
                content += f"- {c}\n"
            content += "\n"

        if entry.get("field_journal_note"):
            content += f"**Analyst note:** {entry['field_journal_note']}\n\n"

        content += "---\n\n"

    # Append if file already exists (multiple runs in one day)
    mode = "a" if journal_path.exists() else "w"
    with open(journal_path, mode) as f:
        f.write(content)

    log.info(f"Field journal: {journal_path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous synthesis engine for the nightly pipeline"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show queue and exit")
    parser.add_argument("--limit", type=int, default=0, help="Max specimens to process")
    parser.add_argument("--specimen", type=str, help="Process one specific specimen")
    parser.add_argument("--skip-permissions", action="store_true",
                        help="Add --dangerously-skip-permissions")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info(f"OVERNIGHT SYNTHESIS — {'DRY RUN' if args.dry_run else 'LIVE'}")
    log.info("=" * 60)

    # ─── Preflight ────────────────────────────────────────────────────
    failures = preflight_check(
        required_files=[SYNTHESIS_QUEUE, TENSIONS_PATH, CONTINGENCIES_PATH,
                        MECHANISMS_PATH, INSIGHTS_PATH],
        check_claude_cli=not args.dry_run,
        required_dirs=[REPORTS_DIR],
    )
    if failures:
        for f in failures:
            log.error(f"PREFLIGHT FAIL: {f}")
        sys.exit(1)

    # ─── Queue ────────────────────────────────────────────────────────
    queue = load_synthesis_queue(args.specimen)
    if args.limit > 0:
        queue = queue[:args.limit]

    if not queue:
        log.info("No pending specimens in synthesis queue")
        return

    log.info(f"Queue: {len(queue)} specimens pending synthesis")

    if args.dry_run:
        for i, q in enumerate(queue, 1):
            log.info(f"  {i:2d}. {q['specimenId']:30s} | {q.get('action', '?')}")
        log.info(f"\nTotal: {len(queue)} specimens")
        return

    # ─── Lock & Execute ───────────────────────────────────────────────
    lock_path = acquire_lock("overnight-synthesis")
    try:
        start_time = datetime.now()
        journal_entries = []
        succeeded = 0
        failed_ids = []

        for i, q_item in enumerate(queue, 1):
            specimen_id = q_item["specimenId"]
            log.info(f"\n--- [{i}/{len(queue)}] {specimen_id} ---")

            # Load specimen metadata for journal
            spec_file = SPECIMENS_DIR / f"{specimen_id}.json"
            spec_meta = {}
            if spec_file.exists():
                try:
                    spec_meta = load_json(spec_file)
                except Exception:
                    pass

            prompt = build_synthesis_prompt(specimen_id)
            if not prompt:
                log.error(f"  Could not build prompt for {specimen_id}")
                failed_ids.append(specimen_id)
                continue

            result = run_synthesis_agent(specimen_id, prompt, args.skip_permissions)
            if not result:
                # Retry once
                log.info(f"  Retrying {specimen_id}...")
                time.sleep(PAUSE_BETWEEN)
                result = run_synthesis_agent(specimen_id, prompt, args.skip_permissions)

            if result:
                changes = apply_synthesis_result(result, dry_run=False)
                mark_synthesized(specimen_id)
                succeeded += 1

                journal_entries.append({
                    "specimen_id": specimen_id,
                    "name": spec_meta.get("name", specimen_id),
                    "model": spec_meta.get("classification", {}).get("structuralModel", "?"),
                    "orientation": spec_meta.get("classification", {}).get("orientation", "?"),
                    "changes": changes,
                    "field_journal_note": result.get("fieldJournal", ""),
                })

                # Clean up temp file
                synth_output = REPORTS_DIR / f"synth-{specimen_id}.json"
                if synth_output.exists():
                    synth_output.unlink()
            else:
                failed_ids.append(specimen_id)

            if i < len(queue):
                time.sleep(PAUSE_BETWEEN)

        # ─── Write Field Journal ──────────────────────────────────────
        if journal_entries:
            write_field_journal(journal_entries)

        # ─── Summary ─────────────────────────────────────────────────
        elapsed = datetime.now() - start_time
        log.info(f"\n{'='*60}")
        log.info("SYNTHESIS COMPLETE")
        log.info(f"{'='*60}")
        log.info(f"Duration: {elapsed.total_seconds() / 60:.0f} minutes")
        log.info(f"Processed: {succeeded}/{len(queue)}")
        if failed_ids:
            log.info(f"Failed: {failed_ids}")

        total_changes = sum(len(e["changes"]) for e in journal_entries)
        if succeeded:
            write_changelog("overnight-synthesis.py", [
                f"Synthesized {succeeded} specimens",
                f"Applied {total_changes} changes to synthesis files",
                f"Failed: {len(failed_ids)}",
            ])

    finally:
        release_lock(lock_path)
        log.info("Lock released")


if __name__ == "__main__":
    main()
