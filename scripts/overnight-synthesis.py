#!/usr/bin/env python3
"""
overnight-synthesis.py
======================
Orchestrates sequential synthesis batches via Claude CLI subprocess.
Each batch reads the current synthesis state + specimen files, writes
analysis to a pending session file + pending updates JSON, then the
orchestrator merges updates into synthesis files before the next batch.

The key constraint: synthesis files are shared mutable state, so batches
run SEQUENTIALLY (not in parallel). Each agent writes to pending/,
and the orchestrator merges between batches.

Usage:
    python3 scripts/overnight-synthesis.py                    # Run all pending batches
    python3 scripts/overnight-synthesis.py --dry-run          # Show batches, don't run
    python3 scripts/overnight-synthesis.py --batch 3          # Run a single batch
    python3 scripts/overnight-synthesis.py --limit 2          # Only run first N batches
    python3 scripts/overnight-synthesis.py --skip-permissions # Add --dangerously-skip-permissions
    python3 scripts/overnight-synthesis.py --batch-size 8     # Specimens per batch (default 8)
    python3 scripts/overnight-synthesis.py --merge-only 3     # Re-merge a batch's pending updates
    python3 scripts/overnight-synthesis.py --promote 3        # Promote discoveries to taxonomy

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
SYNTHESIS_DIR = PROJECT_ROOT / "synthesis"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"
QUEUE_PATH = PROJECT_ROOT / "curation" / "synthesis-queue.json"
MECHANISMS_PATH = SYNTHESIS_DIR / "mechanisms.json"
TENSIONS_PATH = SYNTHESIS_DIR / "tensions.json"
CONTINGENCIES_PATH = SYNTHESIS_DIR / "contingencies.json"
INSIGHTS_PATH = SYNTHESIS_DIR / "insights.json"
SESSIONS_DIR = SYNTHESIS_DIR / "sessions"
PENDING_DIR = SYNTHESIS_DIR / "pending"
DISCOVERIES_DIR = PENDING_DIR / "discoveries"
BACKUPS_DIR = PENDING_DIR / "backups"
REGISTRY_PATH = SPECIMENS_DIR / "registry.json"

TIMEOUT_SECONDS = 45 * 60   # 45 minutes per batch agent
PAUSE_BETWEEN = 15           # seconds between batches

LOG_FILE = PROJECT_ROOT / "overnight-synthesis.log"

# ─── Batch Definitions ──────────────────────────────────────────────────────
# Intentionally mixed industries per batch for cross-cutting analysis.
# These are the PLANNED batches from the HANDOFF; the script filters out
# specimens that are already synthesized.

BATCH_DEFINITIONS = {
    3: {
        "theme": "Pharma + Healthcare + Services",
        "specimens": [
            "sanofi", "rwjbarnabas-health", "unitedhealth-group",
            "accenture", "accenture-openai", "cognizant", "genpact", "infosys",
            "travelers",  # stale from Feb 4 curation
        ],
    },
    4: {
        "theme": "Automotive + Industrials",
        "specimens": [
            "bmw", "ford", "general-motors", "honda", "mercedes-benz",
            "toyota", "deere-and-co", "dow-chemical", "exxonmobil", "honeywell",
        ],
    },
    5: {
        "theme": "Defense/Gov/Aero + Logistics/Airlines",
        "specimens": [
            "anduril", "blue-origin", "lockheed-martin", "nasa",
            "pentagon-cdao", "us-air-force", "us-cyber-command",
            "new-york-state", "delta-air-lines", "fedex",
        ],
    },
    6: {
        "theme": "Media + Retail/Consumer",
        "specimens": [
            "disney", "lionsgate", "netflix", "publicis-groupe",
            "washington-post", "kroger", "lowes", "nike", "pepsico", "ulta-beauty",
        ],
    },
    7: {
        "theme": "IT Services + Telecom + Misc",
        "specimens": [
            "kyndryl", "panasonic", "nokia", "sk-telecom", "t-mobile",
            "uber", "chegg", "thomson-reuters", "recruit-holdings",
            "servicenow",  # re-synthesis with enriched data
        ],
    },
    8: {
        "theme": "Tech core + AI labs",
        "specimens": [
            "amazon-agi", "apple", "google-deepmind", "meta-ai",
            "meta-reality-labs", "microsoft", "anthropic", "ami-labs", "intel",
        ],
    },
    9: {
        "theme": "Tech enterprise + remaining",
        "specimens": [
            "crowdstrike", "hp-inc", "pinterest", "salesforce", "sap",
            "workday",
        ],
    },
}

# ─── Logging ─────────────────────────────────────────────────────────────────

log = logging.getLogger("overnight-synthesis")
if not log.handlers:
    log.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(sh)

# ─── Helpers ─────────────────────────────────────────────────────────────────


def get_pending_specimens() -> set[str]:
    """Get specimen IDs that need synthesis.

    A specimen needs synthesis if ANY of its queue entries has:
    - status == "pending", OR
    - status == "synthesized" but synthesizedIn is null/empty
      (was marked synthesized during curation but never actually processed)
    """
    with open(QUEUE_PATH) as f:
        q = json.load(f)

    needs_synthesis = set()
    for e in q["queue"]:
        sid = e["specimenId"]
        if e["status"] == "pending":
            needs_synthesis.add(sid)
        elif e["status"] == "synthesized" and not e.get("synthesizedIn"):
            # Curated but never actually synthesized — stale entry
            needs_synthesis.add(sid)

    return needs_synthesis


def filter_batch(batch_specimens: list[str], pending: set[str]) -> list[str]:
    """Filter batch to only include specimens that are actually pending."""
    return [s for s in batch_specimens if s in pending]


def load_specimen_summary(specimen_id: str) -> dict | None:
    """Load a specimen file and extract a compact summary for the agent prompt."""
    path = SPECIMENS_DIR / f"{specimen_id}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def read_file_content(path: Path) -> str:
    """Read a file's content as string, or return empty string if missing."""
    if not path.exists():
        return ""
    with open(path) as f:
        return f.read()


# ─── Agent Prompt Builder ────────────────────────────────────────────────────


def build_synthesis_prompt(
    batch_num: int,
    theme: str,
    specimen_ids: list[str],
    prev_session_file: str | None,
) -> str:
    """Build the full prompt for a Claude CLI synthesis agent."""

    today = date.today().isoformat()
    session_filename = f"{today}-synthesis-batch{batch_num}.md"
    output_session_path = str(SESSIONS_DIR / session_filename)
    pending_updates_path = str(PENDING_DIR / f"batch{batch_num}-updates.json")
    discoveries_path = str(DISCOVERIES_DIR / f"batch{batch_num}-discoveries.json")

    # Build specimen file list
    specimen_files = "\n".join(
        f'  - specimens/{sid}.json' for sid in specimen_ids
    )

    # Previous session context
    if prev_session_file:
        prev_session_instruction = (
            f"Read the previous batch's session log at `{prev_session_file}` "
            f"and carry forward any emerging sector trends or questions."
        )
    else:
        prev_session_instruction = (
            "Read synthesis/sessions/2026-02-09-synthesis-batch2.md for context "
            "on what was covered in the last completed batch."
        )

    prompt = dedent(f"""\
    You are running synthesis Batch {batch_num} for the Ambidexterity Field Guide.
    Theme: "{theme}"

    ## YOUR TASK

    Analyze {len(specimen_ids)} specimens for cross-cutting patterns about how
    organizations structurally enable both exploration and execution in the AI era.

    You must produce THREE outputs:

    1. A rich session log (markdown) at: {output_session_path}
    2. Structured updates for EXISTING taxonomy (template-based) at: {pending_updates_path}
    3. NEW discoveries (free-form) at: {discoveries_path}

    ## CRITICAL RULES

    1. Read ALL the input files listed below before analyzing anything.
    2. Follow the synthesis protocol EXACTLY — mechanisms, tensions, contingencies, insights, convergent evolution, botanist's field notes, sector trends.
    3. Do NOT modify synthesis/mechanisms.json, tensions.json, contingencies.json, or insights.json directly. Instead, write updates to the two pending JSON files.
    4. DO write the session log directly to synthesis/sessions/.
    5. Always look for CROSS-SECTOR trends — the batches intentionally mix industries.
    6. NEVER delete existing insights. Only add new evidence or new insights.
    7. Check for duplicates before proposing additions — if a specimen is already in a mechanism's evidence array, don't re-add it.
    8. Route output correctly: evidence for EXISTING taxonomy → structured updates file. Anything NEW → discoveries file.

    ## INPUT FILES TO READ (in this order)

    First, read the protocol and domain knowledge:
    1. synthesis/SYNTHESIS-PROTOCOL.md — the step-by-step protocol
    2. skills/ambidexterity-synthesis/SKILL.md — domain knowledge (what to look for)

    Then read current synthesis state:
    3. synthesis/mechanisms.json — current confirmed mechanisms + candidates
    4. synthesis/tensions.json — current tensions with specimen positions
    5. synthesis/contingencies.json — current contingencies
    6. synthesis/insights.json — current insights (NEVER delete these)
    7. specimens/registry.json — master specimen list for cross-referencing
    8. curation/synthesis-queue.json — to verify which specimens are pending

    Then read prior batch context:
    9. {prev_session_instruction}

    Then read each specimen file:
{specimen_files}

    ## SESSION LOG FORMAT

    Write the session log at `{output_session_path}` following the template in
    SYNTHESIS-PROTOCOL.md. Include ALL sections:

    - YAML frontmatter with session metadata
    - Specimens Analyzed table
    - Mechanism Updates (strengthened, candidates identified, candidates promoted)
    - Tensions Identified/Updated
    - Contingencies Identified/Updated
    - Convergent Evolution Observed
    - Insights Updated + New Insights Discovered
    - Botanist's Field Notes (3-6 paragraphs, candid, speculative)
    - Sector Trends (cumulative — reference prior batches)
    - Key Insights for Executives (2-3 bullets)
    - Key Insights for Academics (2-3 bullets)
    - Open Questions

    ## FILE 2: STRUCTURED UPDATES (auto-merged into taxonomy)

    A template has been pre-written at `{pending_updates_path}`.
    Read it first, then OVERWRITE it with your populated data.

    RULES — follow these exactly:
    1. Keep ALL existing top-level keys exactly as-is. Do NOT add, remove, or rename keys.
    2. Append items to existing arrays only.
    3. This file is for EXISTING taxonomy ONLY: existing mechanisms (IDs 1,3,4,5,6,7,8,10,11),
       existing tensions (IDs 1-5), existing contingencies, existing insights.
    4. queueUpdates is pre-filled — leave it as-is unless you skipped a specimen.
    5. Put anything NEW (new candidates, new insights, new tensions) in the discoveries file instead.

    ITEM FORMATS for each array:

    mechanismUpdates.newEvidence — evidence for existing confirmed mechanisms:
      {{"mechanismId": INTEGER, "specimenId": "org-id", "addToSpecimensArray": true,
        "evidence": {{"specimenId": "org-id", "quote": "verbatim or null",
                      "speaker": "name or null", "source": "source name",
                      "notes": "how this demonstrates the mechanism"}}}}

    tensionUpdates — positions on existing tensions:
      {{"tensionId": INTEGER (1-5), "specimenId": "org-id",
        "position": FLOAT (-1.0 to 1.0), "evidence": "Brief explanation"}}

    contingencyUpdates — placements in existing contingencies:
      {{"contingencyField": "regulatoryIntensity|timeToObsolescence|ceoTenure|talentMarketPosition|technicalDebt",
        "level": "high|medium|low|founder|new|inherited|talent-rich|talent-constrained",
        "specimenId": "org-id"}}

    insightUpdates.existingInsightEvidence — evidence for existing insights:
      {{"insightId": "existing-kebab-case-id", "specimenId": "org-id",
        "note": "How this specimen demonstrates the insight"}}

    ## FILE 3: DISCOVERIES (human-reviewed before merging)

    A template has been pre-written at `{discoveries_path}`.
    Read it first, then OVERWRITE it with your findings.

    Put ALL of the following in this file (NOT in the structured updates):
    - New mechanism CANDIDATES (not yet confirmed)
    - New insights discovered in this batch
    - Maturity promotions for existing insights (hypothesis→emerging→confirmed)
    - Proposed new tensions or subdivisions of existing ones
    - Convergent evolution observations
    - Taxonomy proposals (new models, model splits/merges, new contingencies)
    - Sector trends and open questions

    The discoveries file has pre-populated sections. Populate whichever sections apply.
    This file will be reviewed by the research team before anything is promoted.

    IMPORTANT: Both JSON files must be valid JSON. Double-check before writing.
    Include ONLY updates where you found actual evidence — don't force-fit specimens.
    For stubs with insufficient data, still mark them synthesized in the structured
    updates file (they're pre-filled) but note "insufficient data" in specimensSkipped.
    """)

    return prompt


# ─── Template Writers ────────────────────────────────────────────────────────


def write_batch_template(
    batch_num: int, theme: str, specimen_ids: list[str]
) -> Path:
    """Write a pre-filled JSON template for structured updates (auto-merge).

    The agent reads this template, populates the arrays, and overwrites it.
    All keys are canonical — the agent should not add or rename any.
    """
    today = date.today().isoformat()
    session_filename = f"{today}-synthesis-batch{batch_num}.md"

    template = {
        "batchNumber": batch_num,
        "theme": theme,
        "processedDate": today,
        "specimensProcessed": [],
        "specimensSkipped": [],
        "mechanismUpdates": {
            "newEvidence": [],
            "promotions": [],
        },
        "tensionUpdates": [],
        "contingencyUpdates": [],
        "insightUpdates": {
            "existingInsightEvidence": [],
            "maturityPromotions": [],
        },
        "queueUpdates": [
            {
                "specimenId": sid,
                "status": "synthesized",
                "synthesizedIn": session_filename,
            }
            for sid in specimen_ids
        ],
    }

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    path = PENDING_DIR / f"batch{batch_num}-updates.json"
    with open(path, "w") as f:
        json.dump(template, f, indent=2)

    return path


def write_discoveries_template(batch_num: int) -> Path:
    """Write a pre-filled JSON template for discoveries (human review).

    The agent reads this template, populates whichever sections apply,
    and overwrites it. This file is NOT auto-merged — it goes through
    human review and the --promote pipeline.
    """
    today = date.today().isoformat()

    template = {
        "batchNumber": batch_num,
        "processedDate": today,
        "newMechanismCandidates": [],
        "newInsights": [],
        "insightMaturityPromotions": [],
        "newTensionProposals": [],
        "convergentEvolution": [],
        "taxonomyProposals": [],
        "sectorTrends": [],
        "openQuestions": [],
    }

    DISCOVERIES_DIR.mkdir(parents=True, exist_ok=True)
    path = DISCOVERIES_DIR / f"batch{batch_num}-discoveries.json"
    with open(path, "w") as f:
        json.dump(template, f, indent=2)

    return path


# ─── Agent Runner ─────────────────────────────────────────────────────────────


def run_synthesis_agent(
    batch_num: int, prompt: str, skip_permissions: bool = False
) -> bool:
    """Run a single Claude CLI synthesis agent. Returns True if outputs were created.

    Uses Popen with process groups so timeout kills the entire process tree
    (claude + any child processes), preventing zombie orphans.
    """
    log.info(f"▶ Starting synthesis agent: Batch {batch_num}")
    start = time.time()

    cmd = ["claude", "-p", prompt, "--model", "opus"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        # Use Popen with start_new_session so we can kill the entire process group
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(PROJECT_ROOT),
            start_new_session=True,  # creates new process group
        )

        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            # Kill the entire process group, not just the direct child
            import signal
            try:
                pgid = os.getpgid(proc.pid)
                log.warning(f"  Timeout — killing process group {pgid}")
                os.killpg(pgid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(pgid, signal.SIGKILL)
                    proc.wait(timeout=5)
            except (ProcessLookupError, OSError):
                pass  # process already dead — that's fine
            elapsed = time.time() - start
            log.error(f"✗ Batch {batch_num}: TIMEOUT after {elapsed:.0f}s (process group killed)")
            return False

        elapsed = time.time() - start

        # Check if outputs were created
        today = date.today().isoformat()
        session_file = SESSIONS_DIR / f"{today}-synthesis-batch{batch_num}.md"
        updates_file = PENDING_DIR / f"batch{batch_num}-updates.json"

        session_exists = session_file.exists()
        updates_exists = updates_file.exists()

        if session_exists and updates_exists:
            # Validate updates JSON
            try:
                with open(updates_file) as f:
                    data = json.load(f)
                specimens_done = len(data.get("specimensProcessed", data.get("specimensAnalyzed", [])))
                log.info(
                    f"✓ Batch {batch_num}: {specimens_done} specimens processed "
                    f"in {elapsed:.0f}s"
                )
                # Check for discoveries file (optional — not required for success)
                discoveries_file = DISCOVERIES_DIR / f"batch{batch_num}-discoveries.json"
                if discoveries_file.exists():
                    try:
                        with open(discoveries_file) as f:
                            disco = json.load(f)
                        disco_counts = []
                        for key in ("newMechanismCandidates", "newInsights",
                                    "insightMaturityPromotions", "newTensionProposals",
                                    "convergentEvolution", "taxonomyProposals"):
                            items = disco.get(key, [])
                            if items:
                                disco_counts.append(f"{len(items)} {key}")
                        if disco_counts:
                            log.info(f"  Discoveries: {', '.join(disco_counts)}")
                        else:
                            log.info(f"  Discoveries: none (template unchanged)")
                    except json.JSONDecodeError:
                        log.warning(f"  Discoveries file is invalid JSON")
                else:
                    log.info(f"  Discoveries: file not created (agent may have skipped)")
                return True
            except json.JSONDecodeError:
                log.error(f"✗ Batch {batch_num}: Updates file is invalid JSON")
                return False
        elif session_exists:
            log.warning(
                f"⚠ Batch {batch_num}: Session log written but no updates JSON "
                f"after {elapsed:.0f}s. Session log exists — partial success."
            )
            return False
        else:
            stdout_preview = stdout[:500] if stdout else "(empty)"
            stderr_preview = stderr[:500] if stderr else "(empty)"
            log.error(
                f"✗ Batch {batch_num}: No output files after {elapsed:.0f}s "
                f"(exit={proc.returncode})\n"
                f"  stdout: {stdout_preview}\n"
                f"  stderr: {stderr_preview}"
            )
            return False

    except Exception as e:
        log.error(f"✗ Batch {batch_num}: Exception: {e}")
        return False


# ─── Merge Logic ──────────────────────────────────────────────────────────────


def _map_confidence_to_maturity(confidence: str) -> str:
    """Map agent confidence labels to insight maturity levels."""
    c = confidence.lower().strip()
    if c in ("confirmed", "high"):
        return "confirmed"
    if c in ("emerging", "medium", "medium-high"):
        return "emerging"
    # "hypothesis", "low", "low-medium", or anything else
    return "hypothesis"


def _normalize_agent_output(updates: dict, batch_num: int) -> dict:
    """
    Normalize agent output to the canonical format expected by merge logic.

    Agents produce at least 3 known format variants:
      Variant A (canonical): camelCase keys, flat tensionUpdates list, flat contingencyUpdates list
      Variant B (snake_case): snake_case keys, nested tensions_updates by tension name,
                              nested contingencies_updates by field, queue_updates.mark_synthesized
      Variant C (nested):     camelCase keys but tensionUpdates.specimenPositions with
                              per-specimen positions dict, contingencyUpdates.newPatterns,
                              insightUpdates.extendedInsights

    This function converts all variants to Variant A before merge.
    """
    today = date.today().isoformat()
    session_filename = f"{today}-synthesis-batch{batch_num}.md"

    # Normalization metrics — tracks how much fixing was needed
    metrics = {
        "key_remappings": 0,
        "mechanism_fixes": 0,
        "tension_fixes": 0,
        "contingency_fixes": 0,
        "insight_fixes": 0,
        "queue_fixes": 0,
    }

    # ─── Step 0: snake_case key remapping (Variant B) ────────────────────
    # Map any snake_case top-level keys to camelCase equivalents

    snake_map = {
        "mechanisms_updates": "mechanismUpdates",
        "tensions_updates": "tensionUpdates",
        "contingencies_updates": "contingencyUpdates",
        "insights_updates": "insightUpdates",
        "queue_updates": "queueUpdates",
        "specimenQueueUpdates": "queueUpdates",
        "new_candidates": "newCandidatesTopLevel",
        "new_insights": "newInsightsTopLevel",
    }
    for snake, camel in snake_map.items():
        if snake in updates and camel not in updates:
            updates[camel] = updates.pop(snake)
            log.info(f"  Remapped {snake} → {camel}")
            metrics["key_remappings"] += 1

    # ─── Step 1: mechanismUpdates normalization ──────────────────────────

    mu = updates.get("mechanismUpdates", {})

    if isinstance(mu, list):
        # Variant: list of mechanism items — multiple sub-formats:
        #   A) {id, newEvidence: [{specimenId, ...}], action}  (grouped, newEvidence key)
        #   B) {mechanismId, specimenId, evidence: {...}, action}  (one item per specimen, evidence is dict)
        #   C) {mechanismId, specimenId, evidence: "string", action}  (one item per specimen, evidence is string)
        #   D) {mechanismId, evidence: [{specimenId, note, ...}], action}  (grouped, evidence key as list)
        #   E) {id, evidence: "string", specimens: ["id", ...]}  (flat evidence string, specimen list)
        all_evidence = []
        all_candidates = []
        for item in mu:
            mech_id = item.get("mechanismId", item.get("id"))
            action = item.get("action", "strengthen")
            ev_raw = item.get("evidence", item.get("newEvidence"))

            if isinstance(ev_raw, list):
                # Sub-formats A/D: evidence or newEvidence is a list of dicts
                for ev in ev_raw:
                    if not isinstance(ev, dict):
                        continue
                    sid = ev.get("specimenId", "")
                    all_evidence.append({
                        "mechanismId": mech_id,
                        "specimenId": sid,
                        "addToSpecimensArray": True,
                        "evidence": {
                            "specimenId": sid,
                            "quote": ev.get("quote"),
                            "speaker": ev.get("speaker"),
                            "source": ev.get("source", "synthesis-agent"),
                            "notes": ev.get("evidence", ev.get("notes", ev.get("note", ""))),
                        },
                    })
            elif isinstance(ev_raw, dict) and "specimenId" in item:
                # Sub-format B: single item with evidence as dict
                all_evidence.append({
                    "mechanismId": mech_id,
                    "specimenId": item["specimenId"],
                    "addToSpecimensArray": True,
                    "evidence": {
                        "specimenId": item["specimenId"],
                        "quote": ev_raw.get("quote"),
                        "speaker": ev_raw.get("speaker"),
                        "source": ev_raw.get("source", "synthesis-agent"),
                        "notes": ev_raw.get("notes", ""),
                    },
                })
            elif isinstance(ev_raw, str):
                # Sub-formats C/E: evidence is a string
                # Specimens may be in item["specimenId"] (single) or item["specimens"] (list)
                spec_ids = item.get("specimens", [])
                if isinstance(spec_ids, str):
                    spec_ids = [spec_ids]
                if "specimenId" in item:
                    spec_ids = [item["specimenId"]]
                if not spec_ids:
                    spec_ids = ["unknown"]
                for sid in spec_ids:
                    all_evidence.append({
                        "mechanismId": mech_id,
                        "specimenId": sid,
                        "addToSpecimensArray": True,
                        "evidence": {
                            "specimenId": sid,
                            "quote": None,
                            "speaker": None,
                            "source": "synthesis-agent",
                            "notes": ev_raw,
                        },
                    })
            elif ev_raw is None and "specimenId" in item:
                # No evidence at all, just a specimen reference
                all_evidence.append({
                    "mechanismId": mech_id,
                    "specimenId": item["specimenId"],
                    "addToSpecimensArray": True,
                    "evidence": {
                        "specimenId": item["specimenId"],
                        "quote": None, "speaker": None,
                        "source": "synthesis-agent", "notes": "",
                    },
                })

            if action == "candidate" or item.get("isCandidate"):
                all_candidates.append(item)

        updates["mechanismUpdates"] = {
            "newEvidence": all_evidence,
            "newCandidates": all_candidates,
        }
        log.info(f"  Normalized mechanismUpdates (list): {len(all_evidence)} evidence, {len(all_candidates)} candidates")
        metrics["mechanism_fixes"] += len(all_evidence)

    elif isinstance(mu, dict):
        # Variant B: {evidence_to_add: [...], specimens_to_add: {mechId: [specIds]}}
        if "evidence_to_add" in mu or "specimens_to_add" in mu:
            all_evidence = []
            # Process evidence_to_add: [{mechanismId, specimens: [{specimenId, quote, ...}]}]
            for item in mu.get("evidence_to_add", []):
                mech_id = item.get("mechanismId")
                for spec in item.get("specimens", []):
                    all_evidence.append({
                        "mechanismId": mech_id,
                        "specimenId": spec.get("specimenId", ""),
                        "addToSpecimensArray": True,
                        "evidence": {
                            "specimenId": spec.get("specimenId", ""),
                            "quote": spec.get("quote"),
                            "speaker": spec.get("speaker"),
                            "source": spec.get("source", "synthesis-agent"),
                            "notes": spec.get("notes", ""),
                        },
                    })
            # Also handle specimens_to_add: {mechId: [specIds]} — adds specimens
            # without detailed evidence (just array membership)
            for mech_id_str, spec_ids in mu.get("specimens_to_add", {}).items():
                mech_id = int(mech_id_str)
                for sid in spec_ids:
                    # Only add if not already covered by evidence_to_add
                    already = any(
                        e["mechanismId"] == mech_id and e["specimenId"] == sid
                        for e in all_evidence
                    )
                    if not already:
                        all_evidence.append({
                            "mechanismId": mech_id,
                            "specimenId": sid,
                            "addToSpecimensArray": True,
                            "evidence": {
                                "specimenId": sid,
                                "quote": None,
                                "speaker": None,
                                "source": "synthesis-agent",
                                "notes": "added via specimens_to_add",
                            },
                        })
            updates["mechanismUpdates"] = {
                "newEvidence": all_evidence,
                "newCandidates": [],
            }
            log.info(f"  Normalized mechanismUpdates (snake): {len(all_evidence)} evidence items")
            metrics["mechanism_fixes"] += len(all_evidence)

    # Handle top-level newCandidatesTopLevel (from snake_case new_candidates)
    if "newCandidatesTopLevel" in updates:
        top_cands = updates.pop("newCandidatesTopLevel")
        mu_dict = updates.get("mechanismUpdates", {})
        if isinstance(mu_dict, dict):
            existing = mu_dict.get("newCandidates", [])
            existing.extend(top_cands)
            mu_dict["newCandidates"] = existing
        log.info(f"  Merged {len(top_cands)} top-level newCandidates into mechanismUpdates")

    # ─── Step 2: tensionUpdates normalization ────────────────────────────

    tu = updates.get("tensionUpdates", {})

    # Tension ID mapping for named keys
    TENSION_NAME_MAP = {
        "tension_1_structural_vs_contextual": 1, "structuralVsContextual": 1,
        "tension_2_speed_vs_depth": 2, "speedVsDepth": 2,
        "tension_3_central_vs_distributed": 3, "centralVsDistributed": 3,
        "tension_4_named_vs_quiet": 4, "namedVsQuiet": 4,
        "tension_5_long_vs_short_horizon": 5, "longVsShortHorizon": 5,
    }

    if isinstance(tu, dict):
        flat = []

        if "specimenPositions" in tu:
            # Variant C: {specimenPositions: [{specimenId, positions: {t1: val, ...}, rationale}]}
            for sp in tu["specimenPositions"]:
                sid = sp.get("specimenId", "")
                rationale = sp.get("rationale", "")
                for tkey, pos in sp.get("positions", {}).items():
                    tid = TENSION_NAME_MAP.get(tkey)
                    if tid and pos is not None:
                        flat.append({
                            "tensionId": tid,
                            "specimenId": sid,
                            "position": pos,
                            "evidence": rationale,
                        })
            log.info(f"  Normalized tensionUpdates.specimenPositions: {len(flat)} placements")
            metrics["tension_fixes"] += len(flat)
        else:
            # Variant B: {tension_1_structural_vs_contextual: [{specimenId, position, evidence}]}
            for tkey, placements in tu.items():
                tid = TENSION_NAME_MAP.get(tkey)
                if tid and isinstance(placements, list):
                    for p in placements:
                        flat.append({
                            "tensionId": tid,
                            "specimenId": p.get("specimenId", ""),
                            "position": p.get("position", 0),
                            "evidence": p.get("evidence", ""),
                        })
            if flat:
                log.info(f"  Normalized tensionUpdates (snake dict): {len(flat)} placements")
                metrics["tension_fixes"] += len(flat)

        updates["tensionUpdates"] = flat

    elif isinstance(tu, list) and tu and isinstance(tu[0], dict):
        # List-of-dicts — multiple sub-formats:
        #   D) {tensionId: "name", positions: [{specimenId, position, rationale}]}
        #   E) {tensionId: 1, specimens: [{specimenId, position, evidence}]}
        #   F) {id: "name", specimens: [{specimenId, position}], observation: "..."}
        #   G) canonical: [{tensionId: 1, specimenId: "x", position: 0.5, evidence: "..."}]

        # Detect canonical format: first item has both tensionId and specimenId at top level
        first = tu[0]
        if "specimenId" in first and ("tensionId" in first or "id" in first):
            # Canonical (G) or near-canonical — resolve tension IDs
            flat = []
            for item in tu:
                tid_raw = item.get("tensionId", item.get("id"))
                tid = TENSION_NAME_MAP.get(tid_raw) if isinstance(tid_raw, str) else tid_raw
                if tid is None:
                    log.warning(f"  Unknown tension '{tid_raw}', skipping")
                    continue
                flat.append({
                    "tensionId": tid,
                    "specimenId": item.get("specimenId", ""),
                    "position": item.get("position", 0),
                    "evidence": item.get("evidence", item.get("rationale", "")),
                })
            updates["tensionUpdates"] = flat
        else:
            # Per-tension grouping (D/E/F) — specimens nested under positions or specimens key
            flat = []
            for tension_group in tu:
                tid_raw = tension_group.get("tensionId", tension_group.get("id", ""))
                tid = TENSION_NAME_MAP.get(tid_raw) if isinstance(tid_raw, str) else tid_raw
                if tid is None:
                    log.warning(f"  Unknown tension name '{tid_raw}', skipping")
                    continue
                # Try positions first, then specimens
                placements = tension_group.get("positions", tension_group.get("specimens", []))
                observation = tension_group.get("observation", "")
                for p in placements:
                    if isinstance(p, dict):
                        flat.append({
                            "tensionId": tid,
                            "specimenId": p.get("specimenId", ""),
                            "position": p.get("position", 0),
                            "evidence": p.get("rationale", p.get("evidence", observation)),
                        })
                    elif isinstance(p, str):
                        # Specimen ID as bare string (no position data)
                        flat.append({
                            "tensionId": tid,
                            "specimenId": p,
                            "position": 0,
                            "evidence": observation,
                        })
            log.info(f"  Normalized tensionUpdates (per-tension list): {len(flat)} placements")
            metrics["tension_fixes"] += len(flat)
            updates["tensionUpdates"] = flat

    # ─── Step 3: contingencyUpdates normalization ────────────────────────

    cu = updates.get("contingencyUpdates", {})

    # Variant E/F: list of {contingencyId, specimens: [{specimenId, value, evidence}]}
    if isinstance(cu, list) and cu and isinstance(cu[0], dict) and "contingencyId" in cu[0]:
        LEVEL_MAP = {
            "talent_rich": "talent-rich", "talent-rich": "talent-rich",
            "Talent-rich": "talent-rich", "Talent Rich": "talent-rich",
            "talent_constrained": "talent-constrained", "talent-constrained": "talent-constrained",
            "Talent-constrained": "talent-constrained",
            "high": "high", "High": "high", "medium": "medium", "Medium": "medium",
            "low": "low", "Low": "low",
            "founder": "founder", "Founder": "founder",
            "new": "new", "New": "new", "critical": "critical",
            "nonTraditional": "nonTraditional", "non-traditional": "non-traditional",
        }
        flat = []
        for item in cu:
            field = item.get("contingencyId", "")
            for spec in item.get("specimens", []):
                if not isinstance(spec, dict):
                    continue
                sid = spec.get("specimenId", "")
                raw_level = spec.get("value", spec.get("level", ""))
                mapped = LEVEL_MAP.get(raw_level, raw_level.lower() if raw_level else "")
                if sid and mapped:
                    flat.append({
                        "contingencyField": field,
                        "level": mapped,
                        "specimenId": sid,
                    })
        log.info(f"  Normalized contingencyUpdates (contingencyId list): {len(flat)} placements")
        metrics["contingency_fixes"] += len(flat)
        updates["contingencyUpdates"] = flat

    elif isinstance(cu, dict) and not any(
        isinstance(v, str) for v in cu.values()
    ):
        flat = []

        if "newPatterns" in cu:
            # Variant C: {newPatterns: [{contingencyVariable, evidence: [specIds], ...}]}
            # These are observations, not direct placements — log but skip merge
            # (The session log captures the narrative; structured merge needs level assignments)
            log.info(f"  contingencyUpdates.newPatterns: {len(cu['newPatterns'])} patterns (narrative only, no level assignments to merge)")
        else:
            # Variant B: {technicalDebt: {high: [specIds], ...}, talentMarketPosition: {talent_rich: [...], ...}}
            # Normalize level names to match existing contingency structure
            LEVEL_MAP = {
                "talent_rich": "talent-rich", "talent-rich": "talent-rich",
                "talent_constrained": "talent-constrained", "talent-constrained": "talent-constrained",
                "high": "high", "medium": "medium", "low": "low",
                "founder": "founder", "new": "new", "critical": "critical",
                "nonTraditional": "nonTraditional", "non-traditional": "non-traditional",
            }
            for field, levels in cu.items():
                if not isinstance(levels, dict):
                    continue
                for level_key, level_val in levels.items():
                    if level_key == "notes":
                        continue
                    mapped_level = LEVEL_MAP.get(level_key, level_key)
                    # Handle both direct list and {add: [...]} sub-variants
                    if isinstance(level_val, list):
                        spec_ids = level_val
                    elif isinstance(level_val, dict) and "add" in level_val:
                        spec_ids = level_val["add"]
                    else:
                        continue
                    if not isinstance(spec_ids, list):
                        continue
                    for sid in spec_ids:
                        flat.append({
                            "contingencyField": field,
                            "level": mapped_level,
                            "specimenId": sid,
                        })
            if flat:
                log.info(f"  Normalized contingencyUpdates (snake dict): {len(flat)} placements")
                metrics["contingency_fixes"] += len(flat)

        updates["contingencyUpdates"] = flat

    # ─── Step 4: insightUpdates normalization ────────────────────────────

    iu = updates.get("insightUpdates", {})

    # Handle top-level insightCandidates (Variant from early batches)
    if "insightCandidates" in updates and not iu:
        candidates = updates.pop("insightCandidates", [])
        new_insights = []
        for c in candidates:
            new_insights.append({
                "id": c.get("id", ""),
                "title": c.get("title", ""),
                "theme": c.get("theme", "convergence"),
                "maturity": _map_confidence_to_maturity(c.get("confidence", "hypothesis")),
                "finding": c.get("observation", c.get("finding", "")),
                "evidence": [
                    {"specimenId": sid, "note": c.get("mechanism", "")}
                    for sid in c.get("supportingSpecimens", [])
                ],
                "theoreticalConnection": c.get("mechanism", ""),
                "relatedMechanisms": [],
                "relatedTensions": [],
            })
        iu = {
            "existingInsightEvidence": [],
            "newInsights": new_insights,
            "maturityPromotions": [],
        }
        updates["insightUpdates"] = iu
        log.info(f"  Normalized insightCandidates → insightUpdates: {len(new_insights)} new insights")
        metrics["insight_fixes"] += len(new_insights)

    if isinstance(iu, list):
        # Variant B: insights_updates is a list of {insightId, new_evidence: [...]}
        existing_evidence = []
        for item in iu:
            iid = item.get("insightId", "")
            for ev in item.get("new_evidence", item.get("newEvidence", [])):
                existing_evidence.append({
                    "insightId": iid,
                    "specimenId": ev.get("specimenId", ""),
                    "note": ev.get("note", ""),
                })
        updates["insightUpdates"] = {
            "existingInsightEvidence": existing_evidence,
            "newInsights": [],
            "maturityPromotions": [],
        }
        log.info(f"  Normalized insightUpdates (list): {len(existing_evidence)} evidence items")
        metrics["insight_fixes"] += len(existing_evidence)

    elif isinstance(iu, dict):
        # Normalize extendedInsights → existingInsightEvidence (Variant C)
        if "extendedInsights" in iu and "existingInsightEvidence" not in iu:
            existing_evidence = []
            for item in iu.pop("extendedInsights", []):
                iid = item.get("insightId", "")
                for ev in item.get("newEvidence", []):
                    existing_evidence.append({
                        "insightId": iid,
                        "specimenId": ev.get("specimenId", ""),
                        "note": ev.get("note", ""),
                    })
            iu["existingInsightEvidence"] = existing_evidence
            log.info(f"  Normalized extendedInsights → existingInsightEvidence: {len(existing_evidence)} items")
            metrics["insight_fixes"] += len(existing_evidence)

        # Ensure all required sub-keys exist
        iu.setdefault("existingInsightEvidence", [])
        iu.setdefault("newInsights", [])
        iu.setdefault("maturityPromotions", [])
        updates["insightUpdates"] = iu

    # Handle top-level newInsights (camelCase or snake_case remapped to newInsightsTopLevel)
    for top_key in ("newInsightsTopLevel", "newInsights"):
        if top_key in updates and top_key != "insightUpdates":
            # Don't accidentally grab insightUpdates.newInsights — only top-level
            top_val = updates.get(top_key)
            if isinstance(top_val, list):
                top_insights = updates.pop(top_key)
                iu_dict = updates.setdefault("insightUpdates", {
                    "existingInsightEvidence": [],
                    "newInsights": [],
                    "maturityPromotions": [],
                })
                if isinstance(iu_dict, dict):
                    existing = iu_dict.get("newInsights", [])
                    existing.extend(top_insights)
                    iu_dict["newInsights"] = existing
                log.info(f"  Merged {len(top_insights)} top-level {top_key} into insightUpdates")
                metrics["insight_fixes"] += len(top_insights)
                break  # only handle one

    # ─── Step 4b: normalize individual insight objects ───────────────────
    # Fix proposedId→id, confidence→maturity, auto-generate id from title

    import re

    def _title_to_id(title: str) -> str:
        """Convert a title like 'AI-Washing as Signal' to 'ai-washing-as-signal'."""
        s = title.lower().strip()
        s = re.sub(r'[^a-z0-9\s-]', '', s)
        s = re.sub(r'[\s]+', '-', s)
        return s[:80]  # cap length

    iu_final = updates.get("insightUpdates", {})
    if isinstance(iu_final, dict):
        fixed_count = 0
        for ni in iu_final.get("newInsights", []):
            # proposedId → id (but skip placeholder IDs like "I-14")
            proposed = ni.get("proposedId", "")
            if not ni.get("id") and proposed and not re.match(r'^[A-Z]-\d+$', proposed):
                ni["id"] = ni.pop("proposedId")
                fixed_count += 1
            elif "proposedId" in ni:
                ni.pop("proposedId")  # discard placeholder
            # Auto-generate id from title if still missing
            if not ni.get("id") and ni.get("title"):
                ni["id"] = _title_to_id(ni["title"])
                fixed_count += 1
            # confidence → maturity
            if not ni.get("maturity") and ni.get("confidence"):
                ni["maturity"] = _map_confidence_to_maturity(ni.pop("confidence"))
                fixed_count += 1
            # Ensure maturity exists
            if not ni.get("maturity"):
                ni["maturity"] = "hypothesis"
            # Ensure required fields exist
            ni.setdefault("theme", "convergence")
            ni.setdefault("finding", ni.get("observation", ni.get("description", "")))
            ni.setdefault("evidence", [])
            ni.setdefault("theoreticalConnection", ni.get("implication", ""))
            ni.setdefault("relatedMechanisms", [])
            ni.setdefault("relatedTensions", [])
            # Convert specimens list to evidence if needed
            if not ni["evidence"] and ni.get("specimens"):
                ni["evidence"] = [
                    {"specimenId": sid, "note": ""} if isinstance(sid, str)
                    else sid
                    for sid in ni["specimens"]
                ]
        if fixed_count:
            log.info(f"  Fixed {fixed_count} insight field(s) (proposedId→id, confidence→maturity, etc.)")
            metrics["insight_fixes"] += fixed_count

    # ─── Step 5: queueUpdates normalization ──────────────────────────────

    qu = updates.get("queueUpdates", {})

    if isinstance(qu, list):
        # Could be canonical [{specimenId, status}] or Batch 9 [{id, newStatus}]
        flat = []
        for item in qu:
            if isinstance(item, dict):
                sid = item.get("specimenId", item.get("id", ""))
                status = item.get("status", item.get("newStatus", "synthesized"))
                if sid:
                    flat.append({
                        "specimenId": sid,
                        "status": status,
                        "synthesizedIn": item.get("synthesizedIn", session_filename),
                    })
            elif isinstance(item, str):
                flat.append({
                    "specimenId": item,
                    "status": "synthesized",
                    "synthesizedIn": session_filename,
                })
        updates["queueUpdates"] = flat
        if flat:
            log.info(f"  Normalized queueUpdates (list): {len(flat)} specimens")
            metrics["queue_fixes"] += len(flat)

    elif isinstance(qu, dict):
        # Variant B: {mark_synthesized: [{specimenId, synthesizedIn}]}
        flat = []
        for item in qu.get("mark_synthesized", []):
            flat.append({
                "specimenId": item.get("specimenId", ""),
                "status": "synthesized",
                "synthesizedIn": item.get("synthesizedIn", session_filename),
            })
        updates["queueUpdates"] = flat
        if flat:
            log.info(f"  Normalized queueUpdates.mark_synthesized: {len(flat)} specimens")
            metrics["queue_fixes"] += len(flat)

    # Auto-generate queueUpdates if still missing or empty
    if not updates.get("queueUpdates"):
        specimens = updates.get("specimensAnalyzed",
                       updates.get("specimensProcessed",
                       updates.get("specimens", [])))
        if isinstance(specimens, list) and specimens:
            updates["queueUpdates"] = [
                {"specimenId": sid, "status": "synthesized", "synthesizedIn": session_filename}
                for sid in specimens
                if isinstance(sid, str)
            ]
            log.info(f"  Auto-generated queueUpdates for {len(specimens)} specimens")
            metrics["queue_fixes"] += len(specimens)

    # ─── Metrics summary ─────────────────────────────────────────────────
    total_fixes = sum(metrics.values())
    if total_fixes > 0:
        log.info(f"  Normalizer metrics: {total_fixes} total fixes — {metrics}")
    else:
        log.info("  Normalizer metrics: 0 fixes — output matched template perfectly")

    return updates


def merge_batch_updates(batch_num: int) -> bool:
    """
    Merge a batch's pending updates into synthesis files.
    Returns True if merge succeeded.
    """
    updates_file = PENDING_DIR / f"batch{batch_num}-updates.json"
    if not updates_file.exists():
        log.warning(f"No updates file for batch {batch_num}")
        return False

    try:
        with open(updates_file) as f:
            updates = json.load(f)
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in {updates_file}")
        return False

    today = date.today().isoformat()
    changes = []

    # ─── Backup synthesis files before merge ─────────────────────────────
    import shutil

    synthesis_files = {
        "mechanisms": MECHANISMS_PATH,
        "tensions": TENSIONS_PATH,
        "contingencies": CONTINGENCIES_PATH,
        "insights": INSIGHTS_PATH,
        "queue": QUEUE_PATH,
    }

    backup_dir = BACKUPS_DIR / f"pre-batch{batch_num}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    try:
        for name, path in synthesis_files.items():
            if path.exists():
                shutil.copy2(path, backup_dir / path.name)
        log.info(f"  Backup: {backup_dir}")
    except Exception as e:
        log.error(f"  ✗ Backup failed: {e} — aborting merge")
        return False

    # ─── Normalize agent output ─────────────────────────────────────────
    # Agents sometimes produce slightly different formats than specified.
    # Normalize to the canonical format before processing.

    try:
        updates = _normalize_agent_output(updates, batch_num)
    except Exception as e:
        log.error(f"  ✗ Normalization crashed: {e} — rolling back")
        for name, path in synthesis_files.items():
            backup = backup_dir / path.name
            if backup.exists():
                shutil.copy2(backup, path)
        return False

    # ─── 1. Mechanism updates (wrapped in try-except for rollback) ──────

    try:  # ← entire merge block wrapped for rollback

        with open(MECHANISMS_PATH) as f:
            mechanisms = json.load(f)

        mech_updates = updates.get("mechanismUpdates", {})

        # New evidence for existing mechanisms
        for ev in mech_updates.get("newEvidence", []):
            mech_id = ev.get("mechanismId")
            specimen_id = ev.get("specimenId")
            if mech_id is None or not specimen_id:
                log.warning(f"Mechanism evidence missing mechanismId or specimenId, skipping: {ev}")
                continue

            # Find the mechanism
            target = None
            for m in mechanisms["confirmed"]:
                if m["id"] == mech_id:
                    target = m
                    break

            if target is None:
                log.warning(f"Mechanism #{mech_id} not found, skipping evidence")
                continue

            # Check for duplicate
            if specimen_id in target.get("specimens", []):
                log.info(f"  Mechanism #{mech_id}: {specimen_id} already in specimens array, skipping")
                continue

            # Add to specimens array
            if ev.get("addToSpecimensArray", True):
                target.setdefault("specimens", []).append(specimen_id)

            # Add to evidence array
            evidence_entry = ev.get("evidence", {"specimenId": specimen_id, "notes": "auto-added"})
            target.setdefault("evidence", []).append(evidence_entry)
            changes.append(f"mechanism #{mech_id} +{specimen_id}")

        # New candidates
        for cand in mech_updates.get("newCandidates", []):
            cand_name = cand.get("name", "")
            if not cand_name:
                log.warning(f"Mechanism candidate missing 'name', skipping: {cand}")
                continue
            # Check if candidate already exists by name
            existing_names = {c.get("name", "").lower() for c in mechanisms.get("candidates", [])}
            if cand_name.lower() in existing_names:
                log.info(f"  Candidate '{cand_name}' already exists, skipping")
                continue
            mechanisms.setdefault("candidates", []).append(cand)
            changes.append(f"new candidate: {cand_name}")

        mechanisms["lastUpdated"] = today
        with open(MECHANISMS_PATH, "w") as f:
            json.dump(mechanisms, f, indent=2)

        # ─── 2. Tension updates ──────────────────────────────────────────────

        with open(TENSIONS_PATH) as f:
            tensions = json.load(f)

        for tu in updates.get("tensionUpdates", []):
            tension_id = tu.get("tensionId")
            specimen_id = tu.get("specimenId")
            if not tension_id or not specimen_id:
                log.warning(f"Tension update missing tensionId or specimenId, skipping: {tu}")
                continue

            # Find the tension
            target = None
            for t in tensions["tensions"]:
                if t["id"] == tension_id:
                    target = t
                    break

            if target is None:
                log.warning(f"Tension #{tension_id} not found, skipping")
                continue

            # Check for duplicate
            existing_specimens = {s.get("specimenId") for s in target.get("specimens", [])}
            if specimen_id in existing_specimens:
                log.info(f"  Tension #{tension_id}: {specimen_id} already present, skipping")
                continue

            target.setdefault("specimens", []).append({
                "specimenId": specimen_id,
                "position": tu.get("position", 0),
                "evidence": tu.get("evidence", ""),
            })
            changes.append(f"tension #{tension_id} +{specimen_id}")

        tensions["lastUpdated"] = today
        with open(TENSIONS_PATH, "w") as f:
            json.dump(tensions, f, indent=2)

        # ─── 3. Contingency updates ──────────────────────────────────────────

        with open(CONTINGENCIES_PATH) as f:
            contingencies = json.load(f)

        for cu in updates.get("contingencyUpdates", []):
            field = cu.get("contingencyField")
            level = cu.get("level")
            specimen_id = cu.get("specimenId")
            if not field or not level or not specimen_id:
                log.warning(f"Contingency update missing required fields, skipping: {cu}")
                continue

            # Find the contingency
            target = None
            for c in contingencies["contingencies"]:
                if c.get("fieldName") == field or c.get("id") == field:
                    target = c
                    break

            if target is None:
                log.warning(f"Contingency '{field}' not found, skipping")
                continue

            # Add to the right level
            level_data = target.get(level, {})
            specimens_list = level_data.get("specimens", [])

            if specimen_id in specimens_list:
                log.info(f"  Contingency {field}.{level}: {specimen_id} already present, skipping")
                continue

            specimens_list.append(specimen_id)
            level_data["specimens"] = specimens_list
            target[level] = level_data
            changes.append(f"contingency {field}.{level} +{specimen_id}")

        contingencies["lastUpdated"] = today
        with open(CONTINGENCIES_PATH, "w") as f:
            json.dump(contingencies, f, indent=2)

        # ─── 4. Insight updates ──────────────────────────────────────────────

        with open(INSIGHTS_PATH) as f:
            insights = json.load(f)

        insight_updates = updates.get("insightUpdates", {})

        # New evidence for existing insights
        for ie in insight_updates.get("existingInsightEvidence", []):
            insight_id = ie.get("insightId")
            specimen_id = ie.get("specimenId")
            if not insight_id or not specimen_id:
                log.warning(f"Insight evidence missing insightId or specimenId, skipping: {ie}")
                continue

            # Find the insight
            target = None
            for ins in insights["insights"]:
                if ins["id"] == insight_id:
                    target = ins
                    break

            if target is None:
                log.warning(f"Insight '{insight_id}' not found, skipping")
                continue

            # Check for duplicate
            existing = {e.get("specimenId") for e in target.get("evidence", [])}
            if specimen_id in existing:
                log.info(f"  Insight '{insight_id}': {specimen_id} already present, skipping")
                continue

            target.setdefault("evidence", []).append({
                "specimenId": specimen_id,
                "note": ie.get("note", ""),
            })
            changes.append(f"insight '{insight_id}' +{specimen_id}")

        # New insights
        existing_insight_ids = {ins.get("id") for ins in insights["insights"]}
        for ni in insight_updates.get("newInsights", []):
            ni_id = ni.get("id")
            if not ni_id:
                log.warning(f"New insight missing 'id', skipping: {ni.get('title', '?')}")
                continue
            if ni_id in existing_insight_ids:
                log.info(f"  Insight '{ni_id}' already exists, skipping")
                continue
            insights["insights"].append(ni)
            existing_insight_ids.add(ni_id)
            changes.append(f"new insight: {ni_id}")

        # Maturity promotions
        for mp in insight_updates.get("maturityPromotions", []):
            mp_id = mp.get("insightId")
            mp_maturity = mp.get("newMaturity")
            if not mp_id or not mp_maturity:
                continue
            for ins in insights["insights"]:
                if ins.get("id") == mp_id:
                    old = ins.get("maturity", "unknown")
                    ins["maturity"] = mp_maturity
                    changes.append(f"insight '{mp_id}' {old} → {mp_maturity}")
                    break

        insights["lastUpdated"] = today
        with open(INSIGHTS_PATH, "w") as f:
            json.dump(insights, f, indent=2)

        # ─── 5. Queue updates ────────────────────────────────────────────────

        with open(QUEUE_PATH) as f:
            queue = json.load(f)

        for qu in updates.get("queueUpdates", []):
            sid = qu.get("specimenId")
            if not sid:
                continue
            synth_file = qu.get("synthesizedIn", "")
            # Update ALL entries for this specimen (there may be multiple
            # from successive curation rounds)
            for entry in queue["queue"]:
                if entry["specimenId"] == sid:
                    entry["status"] = qu.get("status", "synthesized")
                    if not entry.get("synthesizedIn"):
                        entry["synthesizedIn"] = synth_file

            queue["lastUpdated"] = today
            queue["lastSynthesisDate"] = today
            with open(QUEUE_PATH, "w") as f:
                json.dump(queue, f, indent=2)

    except Exception as e:
        log.error(f"  ✗ MERGE CRASHED for batch {batch_num}: {e}")
        log.error(f"  Rolling back to pre-merge state...")
        try:
            for name, path in synthesis_files.items():
                backup = backup_dir / path.name
                if backup.exists():
                    shutil.copy2(backup, path)
            log.info(f"  ✓ Rollback complete — synthesis files restored")
        except Exception as rollback_err:
            log.error(f"  ✗ ROLLBACK FAILED: {rollback_err}")
            log.error(f"  CRITICAL: Manual recovery needed from {backup_dir}")
        return False

    # ─── Post-merge validation ───────────────────────────────────────────

    validation_ok = True
    for name, path in synthesis_files.items():
        try:
            with open(path) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            log.error(f"  ✗ POST-MERGE: {path.name} is corrupted: {e}")
            validation_ok = False

    if not validation_ok:
        log.error(f"  Rolling back due to corrupted files...")
        for name, path in synthesis_files.items():
            backup = backup_dir / path.name
            if backup.exists():
                shutil.copy2(backup, path)
        log.info(f"  ✓ Rollback complete")
        return False

    # ─── Summary ─────────────────────────────────────────────────────────

    log.info(f"  Merged batch {batch_num}: {len(changes)} updates")
    for c in changes[:20]:  # cap log output
        log.info(f"    {c}")
    if len(changes) > 20:
        log.info(f"    ... and {len(changes) - 20} more")

    # Move updates file to processed
    processed_dir = PENDING_DIR / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    updates_file.rename(processed_dir / updates_file.name)

    return True


# ─── Discovery Promotion ────────────────────────────────────────────────────


def promote_discoveries(batch_num: int) -> bool:
    """Promote reviewed discoveries from a batch into the formal taxonomy.

    Merges:
      - newMechanismCandidates → mechanisms.json candidates array
      - newInsights → insights.json insights array
      - insightMaturityPromotions → update existing insight maturity levels

    Logs only (requires manual action):
      - newTensionProposals → ACTION REQUIRED in log
      - taxonomyProposals → ACTION REQUIRED in log
    """
    import shutil

    disco_file = DISCOVERIES_DIR / f"batch{batch_num}-discoveries.json"
    if not disco_file.exists():
        log.error(f"No discoveries file for batch {batch_num}: {disco_file}")
        return False

    try:
        with open(disco_file) as f:
            disco = json.load(f)
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in {disco_file}")
        return False

    today = date.today().isoformat()
    changes = []

    # ─── Promote mechanism candidates ────────────────────────────────
    candidates = disco.get("newMechanismCandidates", [])
    if candidates:
        with open(MECHANISMS_PATH) as f:
            mechanisms = json.load(f)

        existing_names = {
            c.get("name", "").lower()
            for c in mechanisms.get("candidates", [])
        }

        for cand in candidates:
            name = cand.get("name", "")
            if not name:
                log.warning(f"  Candidate missing 'name', skipping")
                continue
            if name.lower() in existing_names:
                log.info(f"  Candidate '{name}' already exists, skipping")
                continue
            mechanisms.setdefault("candidates", []).append(cand)
            existing_names.add(name.lower())
            changes.append(f"new candidate: {name}")

        mechanisms["lastUpdated"] = today
        with open(MECHANISMS_PATH, "w") as f:
            json.dump(mechanisms, f, indent=2)

    # ─── Promote new insights ────────────────────────────────────────
    new_insights = disco.get("newInsights", [])
    if new_insights:
        with open(INSIGHTS_PATH) as f:
            insights = json.load(f)

        existing_ids = {i.get("id") for i in insights["insights"]}

        for ni in new_insights:
            ni_id = ni.get("id")
            if not ni_id:
                log.warning(f"  New insight missing 'id', skipping: {ni.get('title', '?')}")
                continue
            if ni_id in existing_ids:
                log.info(f"  Insight '{ni_id}' already exists, skipping")
                continue
            # Ensure required fields
            ni.setdefault("theme", "convergence")
            ni.setdefault("maturity", "hypothesis")
            ni.setdefault("finding", "")
            ni.setdefault("evidence", [])
            ni.setdefault("theoreticalConnection", "")
            ni.setdefault("relatedMechanisms", [])
            ni.setdefault("relatedTensions", [])
            insights["insights"].append(ni)
            existing_ids.add(ni_id)
            changes.append(f"new insight: {ni_id}")

        insights["lastUpdated"] = today
        with open(INSIGHTS_PATH, "w") as f:
            json.dump(insights, f, indent=2)

    # ─── Apply maturity promotions ───────────────────────────────────
    promotions = disco.get("insightMaturityPromotions", [])
    if promotions:
        with open(INSIGHTS_PATH) as f:
            insights = json.load(f)

        for mp in promotions:
            mp_id = mp.get("insightId")
            mp_maturity = mp.get("newMaturity")
            if not mp_id or not mp_maturity:
                continue
            for ins in insights["insights"]:
                if ins.get("id") == mp_id:
                    old = ins.get("maturity", "unknown")
                    ins["maturity"] = mp_maturity
                    changes.append(f"insight '{mp_id}' {old} → {mp_maturity}")
                    break
            else:
                log.warning(f"  Insight '{mp_id}' not found for maturity promotion")

        insights["lastUpdated"] = today
        with open(INSIGHTS_PATH, "w") as f:
            json.dump(insights, f, indent=2)

    # ─── Log-only items (require manual action) ─────────────────────
    tension_proposals = disco.get("newTensionProposals", [])
    if tension_proposals:
        log.info(f"")
        log.info(f"  ⚠ ACTION REQUIRED: {len(tension_proposals)} tension proposal(s)")
        for tp in tension_proposals:
            log.info(f"    • {tp.get('name', '?')}: {tp.get('rationale', '')[:80]}")
            specimens = tp.get("specimens", [])
            if specimens:
                sids = [s.get("specimenId", s) if isinstance(s, dict) else s for s in specimens]
                log.info(f"      Specimens: {', '.join(sids)}")
        log.info(f"    → Manually add to synthesis/tensions.json if warranted")

    taxonomy_proposals = disco.get("taxonomyProposals", [])
    if taxonomy_proposals:
        log.info(f"")
        log.info(f"  ⚠ ACTION REQUIRED: {len(taxonomy_proposals)} taxonomy proposal(s)")
        for tp in taxonomy_proposals:
            log.info(f"    • [{tp.get('type', '?')}] {tp.get('proposal', '')[:80]}")
        log.info(f"    → Review and apply manually if warranted")

    # ─── Summary and move to processed ───────────────────────────────
    log.info(f"")
    log.info(f"  Promoted batch {batch_num}: {len(changes)} changes")
    for c in changes:
        log.info(f"    {c}")

    if not changes and not tension_proposals and not taxonomy_proposals:
        log.info(f"  (no promotable discoveries in batch {batch_num})")

    # Move to processed
    processed_dir = DISCOVERIES_DIR / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    disco_file.rename(processed_dir / disco_file.name)

    return True


# ─── Session Summary ─────────────────────────────────────────────────────────


def write_orchestrator_log(results: list[dict], start_time: datetime):
    """Write a summary log of the full overnight synthesis run."""
    today = date.today().isoformat()
    elapsed = datetime.now() - start_time

    succeeded = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    total_specimens = sum(r.get("specimens_processed", 0) for r in succeeded)

    content = dedent(f"""\
    # Overnight Synthesis Run — {today}

    **Started:** {start_time.strftime('%Y-%m-%d %H:%M')}
    **Duration:** {elapsed.total_seconds() / 60:.0f} minutes
    **Batches attempted:** {len(results)}
    **Succeeded:** {len(succeeded)} | **Failed:** {len(failed)}
    **Total specimens processed:** {total_specimens}

    ## Batch Results

    | Batch | Theme | Specimens | Time | Status |
    |-------|-------|-----------|------|--------|
    """)

    for r in results:
        status = "✓" if r["success"] else "✗ FAILED"
        elapsed_s = r.get("elapsed", 0)
        specimens = r.get("specimens_processed", 0)
        content += (
            f"| {r['batch_num']} | {r['theme'][:40]} | "
            f"{specimens} | {elapsed_s:.0f}s | {status} |\n"
        )

    if failed:
        content += "\n## Failed Batches\n\n"
        for r in failed:
            content += f"- Batch {r['batch_num']} ({r['theme']})\n"

    content += "\n## Next Steps\n\n"
    content += "- Review session logs in synthesis/sessions/\n"
    content += "- Run `node scripts/validate-workflow.js` to check consistency\n"
    content += "- Update HANDOFF.md with results\n"

    log_path = SESSIONS_DIR / f"{today}-overnight-synthesis-run.md"
    counter = 1
    while log_path.exists():
        counter += 1
        log_path = SESSIONS_DIR / f"{today}-overnight-synthesis-run-{counter}.md"

    with open(log_path, "w") as f:
        f.write(content)

    log.info(f"Orchestrator log: {log_path}")


# ─── Main Orchestration ─────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Overnight synthesis batches via Claude CLI"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show batches and exit without running agents",
    )
    parser.add_argument(
        "--batch", type=int, default=0,
        help="Run a single specific batch number (e.g., --batch 3)",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Max batches to run (0 = all remaining)",
    )
    parser.add_argument(
        "--skip-permissions", action="store_true",
        help="Add --dangerously-skip-permissions to claude CLI calls",
    )
    parser.add_argument(
        "--no-merge", action="store_true",
        help="Don't merge results into synthesis files (leave in pending/)",
    )
    parser.add_argument(
        "--batch-size", type=int, default=0,
        help="Override batch size (re-chunk pending specimens, ignoring batch definitions)",
    )
    parser.add_argument(
        "--merge-only", type=int, default=0,
        help="Only merge a specific batch's pending updates (no agent run). E.g., --merge-only 3",
    )
    parser.add_argument(
        "--promote", type=int, default=0,
        help="Promote discoveries from a batch into taxonomy. E.g., --promote 3",
    )
    args = parser.parse_args()

    # ─── Merge-only mode ─────────────────────────────────────────────
    if args.merge_only > 0:
        log.info(f"Merge-only mode: merging batch {args.merge_only} updates")
        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        try:
            ok = merge_batch_updates(args.merge_only)
            if ok:
                log.info(f"✓ Batch {args.merge_only} merged successfully")
            else:
                log.error(f"✗ Batch {args.merge_only} merge returned False")
        except Exception as e:
            log.error(f"✗ Merge crashed: {e}")
            import traceback
            traceback.print_exc()
        return

    # ─── Promote mode ────────────────────────────────────────────────
    if args.promote > 0:
        log.info(f"Promote mode: promoting discoveries from batch {args.promote}")
        DISCOVERIES_DIR.mkdir(parents=True, exist_ok=True)
        try:
            ok = promote_discoveries(args.promote)
            if ok:
                log.info(f"✓ Batch {args.promote} discoveries promoted successfully")
            else:
                log.error(f"✗ Batch {args.promote} promotion returned False")
        except Exception as e:
            log.error(f"✗ Promotion crashed: {e}")
            import traceback
            traceback.print_exc()
        return

    log.info("=" * 60)
    log.info("OVERNIGHT SYNTHESIS RUN")
    log.info("=" * 60)

    # Ensure directories exist
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    # Get current pending specimens
    pending = get_pending_specimens()
    log.info(f"Total pending specimens: {len(pending)}")

    # Build batch plan
    if args.batch_size > 0:
        # Re-chunk: ignore batch definitions, split all pending into equal-sized batches
        pending_list = sorted(pending)
        batches = []
        batch_num = 3  # start numbering from 3 (1-2 already done)
        for i in range(0, len(pending_list), args.batch_size):
            chunk = pending_list[i:i + args.batch_size]
            batches.append({
                "num": batch_num,
                "theme": f"Auto-batch {batch_num} ({len(chunk)} specimens)",
                "specimens": chunk,
            })
            batch_num += 1
    elif args.batch > 0:
        # Single batch mode
        if args.batch not in BATCH_DEFINITIONS:
            log.error(f"Batch {args.batch} not defined. Available: {sorted(BATCH_DEFINITIONS.keys())}")
            return
        defn = BATCH_DEFINITIONS[args.batch]
        actual = filter_batch(defn["specimens"], pending)
        batches = [{"num": args.batch, "theme": defn["theme"], "specimens": actual}]
    else:
        # All remaining batches
        batches = []
        for num in sorted(BATCH_DEFINITIONS.keys()):
            defn = BATCH_DEFINITIONS[num]
            actual = filter_batch(defn["specimens"], pending)
            if actual:
                batches.append({"num": num, "theme": defn["theme"], "specimens": actual})

    if args.limit > 0:
        batches = batches[:args.limit]

    # Filter out empty batches
    batches = [b for b in batches if b["specimens"]]

    if not batches:
        log.info("No pending batches to process!")
        return

    # Show plan
    log.info(f"\n--- BATCH PLAN ({len(batches)} batches) ---")
    total_specimens = 0
    for b in batches:
        log.info(f"  Batch {b['num']}: {b['theme']} — {len(b['specimens'])} specimens")
        for s in b["specimens"]:
            log.info(f"    {s}")
        total_specimens += len(b["specimens"])
    log.info(f"  Total: {total_specimens} specimens across {len(batches)} batches")

    if args.dry_run:
        log.info("\n--- DRY RUN — exiting ---")
        return

    # ─── Run Loop ──────────────────────────────────────────────────────

    start_time = datetime.now()
    results = []
    prev_session_file = None

    for i, batch in enumerate(batches):
        batch_num = batch["num"]
        log.info(f"\n{'='*60}")
        log.info(f"BATCH {batch_num} [{i+1}/{len(batches)}]: {batch['theme']}")
        log.info(f"Specimens: {batch['specimens']}")
        log.info(f"{'='*60}")

        # Write template files for the agent to populate
        template_path = write_batch_template(
            batch_num=batch_num,
            theme=batch["theme"],
            specimen_ids=batch["specimens"],
        )
        discoveries_path = write_discoveries_template(batch_num)
        log.info(f"  Templates: {template_path.name}, {discoveries_path.name}")

        prompt = build_synthesis_prompt(
            batch_num=batch_num,
            theme=batch["theme"],
            specimen_ids=batch["specimens"],
            prev_session_file=prev_session_file,
        )

        agent_start = time.time()
        success = run_synthesis_agent(batch_num, prompt, args.skip_permissions)
        agent_elapsed = time.time() - agent_start

        result = {
            "batch_num": batch_num,
            "theme": batch["theme"],
            "success": success,
            "elapsed": agent_elapsed,
            "specimens_processed": len(batch["specimens"]) if success else 0,
        }

        if success:
            # Merge updates into synthesis files
            if not args.no_merge:
                try:
                    merge_ok = merge_batch_updates(batch_num)
                    if not merge_ok:
                        log.warning(f"  Merge failed for batch {batch_num} — continuing anyway")
                except Exception as e:
                    log.error(f"  Merge CRASHED for batch {batch_num}: {e}")
                    log.error(f"  Updates preserved in synthesis/pending/batch{batch_num}-updates.json")
                    log.error(f"  Fix the merge code and re-run with --merge-only {batch_num}")

            # Track session file for next batch's context
            today = date.today().isoformat()
            prev_session_file = f"synthesis/sessions/{today}-synthesis-batch{batch_num}.md"
        else:
            log.error(f"  Batch {batch_num} failed — skipping merge")

        results.append(result)

        # Pause between batches
        if i < len(batches) - 1:
            log.info(f"  Pausing {PAUSE_BETWEEN}s before next batch...")
            time.sleep(PAUSE_BETWEEN)

    # ─── Summary ───────────────────────────────────────────────────────

    elapsed_total = datetime.now() - start_time
    succeeded = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    log.info("\n" + "=" * 60)
    log.info("RUN COMPLETE")
    log.info("=" * 60)
    log.info(f"Duration: {elapsed_total.total_seconds() / 60:.0f} minutes")
    log.info(f"Batches attempted: {len(results)}")
    log.info(f"Succeeded: {len(succeeded)}")
    log.info(f"Failed: {len(failed)}")
    log.info(
        f"Total specimens: "
        f"{sum(r.get('specimens_processed', 0) for r in succeeded)}"
    )

    if failed:
        log.info(f"Failed batches: {[r['batch_num'] for r in failed]}")

    write_orchestrator_log(results, start_time)


if __name__ == "__main__":
    main()
