#!/usr/bin/env python3
"""
overnight-curate.py
===================
Orchestrates sequential curation of research pending files into specimen cards
via Claude CLI agents. Reads research/pending/*.json (single-company format),
invokes `claude -p --model opus` to transform each into a full specimen JSON
file, then updates registry, queue, and synthesis queue.

Unlike overnight-research.py (which discovers findings) and
overnight-purpose-claims.py (which scans for leader quotes), this script
performs Phase 2 CURATION — transforming raw research into structured specimens.

Output:
  - specimens/{slug}.json          — created/updated by agents
  - specimens/registry.json        — updated by orchestrator
  - research/queue.json             — entries marked curated
  - curation/synthesis-queue.json   — specimens queued for Phase 3
  - curation/sessions/*.md          — human-readable session log
  - research/curate-retry-queue.json — persistent retry queue

Usage:
    python3 scripts/overnight-curate.py                     # Run all pending
    python3 scripts/overnight-curate.py --dry-run           # Show queue
    python3 scripts/overnight-curate.py --limit 5           # Only curate 5
    python3 scripts/overnight-curate.py --company apple     # Curate one company
    python3 scripts/overnight-curate.py --skip-permissions  # Unattended mode

Run from project root: orgtransformation/
"""

import argparse
import json
import logging
import subprocess
import sys
import time
from collections import Counter
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

PENDING_DIR = PROJECT_ROOT / "research" / "pending"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"
REGISTRY_FILE = SPECIMENS_DIR / "registry.json"
TEMPLATE_FILE = SPECIMENS_DIR / "_template.json"
QUEUE_FILE = PROJECT_ROOT / "research" / "queue.json"
SYNTHESIS_QUEUE_FILE = PROJECT_ROOT / "curation" / "synthesis-queue.json"
CURATE_SESSION_DIR = PROJECT_ROOT / "curation" / "sessions"
RETRY_QUEUE_FILE = PROJECT_ROOT / "research" / "curate-retry-queue.json"

TIMEOUT_SECONDS = 10 * 60   # 10 minutes per agent (no web fetching)
PAUSE_BETWEEN = 5            # seconds between agents
MAX_RETRIES = 1              # retry failed targets once
MAX_RETRY_ATTEMPTS = 3       # across runs, give up after this many total failures

# ─── Logging ─────────────────────────────────────────────────────────────────

log = setup_logging("overnight-curate")

# ─── Taxonomy & Reference Constants ─────────────────────────────────────────

TAXONOMY = """\
Structural Models (classify the organization into ONE primary model):
  M1 Research Lab — Fundamental research, breakthroughs. 3-10 year horizon. Pure exploration.
  M2 Center of Excellence — Governance, standards, enablement. 6-24 month horizon.
  M3 Embedded Teams — Product-specific AI features. Quarterly cadence.
  M4 Hybrid/Hub-and-Spoke — Central standards + distributed execution. Mixed horizons.
  M5 Product/Venture Lab — Commercialize AI into products/ventures. 6-36 months.
     5a Internal Incubator — Products absorbed into parent (Adobe Firefly)
     5b Venture Builder — Creates independent companies (Google X -> Waymo)
     5c Platform-to-Product — Internal capability sold externally (Walmart GoLocal)
  M6 Unnamed/Informal — Quiet transformation without formal AI structure.
     6a Enterprise-Wide Adoption — Mass deployment, 80%+ adoption (BofA)
     6b Centralized-but-Unnamed — Central team without lab branding (P&G)
     6c Grassroots/Bottom-Up — Adoption preceded formal structure
  M7 Tiger Teams — Time-boxed exploration sprints. Weeks to months.
  M8 Skunkworks — Autonomous unit with radical independence. Years.
  M9 AI-Native — Born-AI organization, no legacy to transform.

Ambidexterity Orientation (how they balance exploration vs. execution):
  Structural — Exploration and execution in distinct units
  Contextual — Individuals balance both within their roles
  Temporal — Organization cycles between exploration and execution phases"""

MECHANISMS_REF = """\
Confirmed Mechanisms (link any that apply — use the ID and name):
  1  Protect Off-Strategy Work
  3  Embed Product at Research Frontier
  4  Consumer-Grade UX for Employee Tools
  5  Deploy to Thousands Before You Know What Works
  6  Merge Competing AI Teams Under Single Leader
  7  Put Executives on the Tools
  8  Turn Compliance Into Deployment Advantage
  10 Productize Internal Operational Advantages
  11 Flatten Management Layers to Speed AI Decisions"""

TENSIONS_REF = """\
Tension Axes (score each -1.0 to +1.0 where data supports, null if uncertain):
  structuralVsContextual:  -1 = structural separation   ... +1 = contextual integration
  speedVsDepth:            -1 = deep validation/learning ... +1 = fast wide deployment
  centralVsDistributed:    -1 = central control          ... +1 = distributed autonomy
  namedVsQuiet:            -1 = named lab/branding       ... +1 = quiet transformation
  longVsShortHorizon:      -1 = long time horizons       ... +1 = short accountability"""

CONTINGENCIES_REF = """\
Contingency Variables (assess where data supports):
  regulatoryIntensity:     High | Medium | Low
  timeToObsolescence:      Fast | Medium | Slow
  ceoTenure:               Long | Medium | Short | Founder
  talentMarketPosition:    Talent-rich | Talent-constrained | Non-traditional
  technicalDebt:           High | Medium | Low"""

CLASSIFICATION_GUARDRAILS = """\
Classification Guardrails — check these before finalizing:
  1. M7 Permanence trap: If the AI team has existed 2+ years, it's NOT M7 Tiger Teams
  2. M1 Prestige bias: Papers alone don't make it M1 if it's really doing product AI
  3. M4 requires BOTH central + distributed: If AI is only central, it's M2 not M4
  4. M6 enterprise-wide (6a): Requires evidence of 80%+ adoption, top-down mandate
  5. Temporal vs one-time: A single pivot is NOT temporal cycling — needs repeated phases
  6. AI-Native (M9): Only for orgs BORN with AI — not orgs that adopted AI early
  7. M5 requires PRODUCT creation: Internal tools/enablement is M2, not M5"""

MODEL_NAMES = {
    1: "Research Lab",
    2: "Center of Excellence",
    3: "Embedded Teams",
    4: "Hybrid/Hub-and-Spoke",
    5: "Product/Venture Lab",
    6: "Unnamed/Informal",
    7: "Tiger Teams",
    8: "Skunkworks",
    9: "AI-Native",
}


# ─── Queue Builder ───────────────────────────────────────────────────────────

def load_retry_queue() -> list[dict]:
    """Load persistent retry queue from prior runs."""
    if not RETRY_QUEUE_FILE.exists():
        return []
    try:
        with open(RETRY_QUEUE_FILE) as f:
            data = json.load(f)
        return [
            entry for entry in data.get("queue", [])
            if entry.get("failCount", 0) < MAX_RETRY_ATTEMPTS
        ]
    except (json.JSONDecodeError, KeyError):
        return []


def is_single_company_file(filepath: Path) -> bool:
    """Check if a pending file is single-company format (from overnight-research.py)."""
    try:
        with open(filepath) as f:
            data = json.load(f)
        return "company" in data
    except (json.JSONDecodeError, KeyError):
        return False


def build_curate_queue(company_filter: str | None = None) -> tuple[list[dict], list[str]]:
    """
    Build the curation queue from pending files + retry queue.

    Returns:
        (queue, skipped) — queue is list of {slug, pendingFile, company, ...},
                           skipped is list of filenames that were multi-company
    """
    queue = []
    skipped = []
    seen_slugs = set()

    # 1. Load retry queue first (priority)
    retries = load_retry_queue()
    for entry in retries:
        slug = entry["slug"]
        pending_path = PENDING_DIR / f"{slug}.json"
        if not pending_path.exists():
            continue
        if not is_single_company_file(pending_path):
            continue

        with open(pending_path) as f:
            data = json.load(f)

        queue.append({
            "slug": slug,
            "pendingFile": str(pending_path),
            "company": data.get("company", slug),
            "sector": data.get("sector", "Unknown"),
            "isRetry": True,
            "failCount": entry.get("failCount", 0),
        })
        seen_slugs.add(slug)

    # 2. Scan pending directory for single-company files
    if not PENDING_DIR.exists():
        return queue, skipped

    for filepath in sorted(PENDING_DIR.glob("*.json")):
        slug = filepath.stem
        if slug in seen_slugs:
            continue

        if not is_single_company_file(filepath):
            skipped.append(filepath.name)
            continue

        # Skip if specimen already exists and was updated today
        specimen_path = SPECIMENS_DIR / f"{slug}.json"
        if specimen_path.exists():
            try:
                with open(specimen_path) as f:
                    specimen = json.load(f)
                last_updated = specimen.get("meta", {}).get("lastUpdated", "")
                if last_updated == date.today().isoformat():
                    log.info(f"  Skip {slug}: specimen already curated today")
                    continue
            except (json.JSONDecodeError, KeyError):
                pass

        with open(filepath) as f:
            data = json.load(f)

        queue.append({
            "slug": slug,
            "pendingFile": str(filepath),
            "company": data.get("company", slug),
            "sector": data.get("sector", "Unknown"),
            "isRetry": False,
            "failCount": 0,
        })
        seen_slugs.add(slug)

    # Apply company filter
    if company_filter:
        queue = [
            q for q in queue
            if company_filter.lower() in q["slug"].lower()
            or company_filter.lower() in q["company"].lower()
        ]

    return queue, skipped


# ─── Prompt Builder ──────────────────────────────────────────────────────────

def build_curate_prompt(slug: str, pending_data: dict, existing_specimen: dict | None) -> str:
    """Build the agent prompt for curating one specimen."""

    company = pending_data.get("company", slug)
    today = date.today().isoformat()
    pending_json = json.dumps(pending_data, indent=2)
    specimen_path = str(SPECIMENS_DIR / f"{slug}.json")

    # Load template
    try:
        with open(TEMPLATE_FILE) as f:
            template_json = f.read()
    except FileNotFoundError:
        template_json = "{}"

    if existing_specimen:
        # ─── Branch 2: ADD LAYER to existing specimen ────────────────
        existing_json = json.dumps(existing_specimen, indent=2)
        prompt = dedent(f"""\
        You are a curation agent for the Ambidexterity Field Guide. COMPLETE THIS IN UNDER 8 MINUTES.

        TASK: UPDATE the existing specimen at {specimen_path} with new research data.
        Do NOT create from scratch. Add new information to the existing specimen.

        ## RULES
        1. Do NOT search the web. All data comes from the research and existing specimen below.
        2. Write ONLY the updated specimen JSON file to {specimen_path}. Nothing else.
        3. Every fact must trace to a source in the research data.
        4. Never paraphrase quotes — copy verbatim from the research data.

        ## UPDATE INSTRUCTIONS
        1. Add a NEW LAYER at the TOP of the layers array (most recent first):
           - date: "{today[:7]}"
           - label: "Overnight research scan"
           - summary: What new information this research adds
           - sourceRefs: IDs of the new sources
        2. APPEND new sources to the sources array (check for duplicates by URL)
        3. APPEND new quotes to the quotes array (check for duplicates by text)
        4. Fill in any null fields with new data where available
        5. Consider whether new data changes the classification — if so, note it
        6. Update meta.lastUpdated to "{today}"
        7. Reassess meta.completeness (High needs 3+ sources with detailed structure)
        8. APPEND new taxonomyFeedback — NEVER delete existing notes. Add new
           observations prefixed with "[{today[:7]}]" so we can see when each was written.
           Example: "[2026-02] New earnings data strengthens M4 classification..."
        9. APPEND new openQuestions — keep existing ones, add new ones, remove any
           that have been answered by the new data

        ## EXISTING SPECIMEN
        {existing_json}

        ## NEW RESEARCH DATA
        {pending_json}

        ## RESEARCH BOTANIST'S NOTES

        The research data above may contain `botanistNotes` (analytical observations from
        the research agent) and a `bestQuote` (the most revealing quote with a `why` field).
        USE these when deciding whether new data changes the classification. If the research
        agent flagged something taxonomically interesting, address it in your update.

        ## OUTPUT
        Write the updated specimen to: {specimen_path}

        After writing, output this summary line to stdout:
        CURATE_RESULT: {slug} | updated | M{{model}} | {{orientation}} | {{confidence}} | {{completeness}} | {{n_quotes}} quotes | {{n_sources}} sources | {{key_change}}
        """)
    else:
        # ─── Branch 1: CREATE new specimen ───────────────────────────
        prompt = dedent(f"""\
        You are a curation agent for the Ambidexterity Field Guide. COMPLETE THIS IN UNDER 8 MINUTES.

        TASK: Transform the research data below into a structured specimen JSON file
        at {specimen_path}.

        ## RULES
        1. Do NOT search the web. All data comes from the research file below.
        2. Write ONLY the specimen JSON file to {specimen_path}. Nothing else.
        3. Every fact must trace to a source in the research data.
        4. Never paraphrase quotes — copy verbatim from the research data.
        5. Be honest about confidence — Low is fine if data is thin.
        6. Use null for fields you can't determine from available data.

        ## CLASSIFICATION DECISION TREE

        {TAXONOMY}

        {CLASSIFICATION_GUARDRAILS}

        ## MECHANISMS — Link Any That Apply

        {MECHANISMS_REF}

        For each mechanism, provide:
        - id: the mechanism number
        - name: the mechanism name
        - evidence: what in this org's data shows this mechanism
        - strength: "Strong" (explicit, multiple sources) | "Moderate" (clear but single source) | "Emerging" (suggestive)

        ## TENSION AXES

        {TENSIONS_REF}

        ## CONTINGENCY VARIABLES

        {CONTINGENCIES_REF}

        ## SPECIMEN TEMPLATE
        {template_json}

        ## RESEARCH DATA
        {pending_json}

        ## RESEARCH BOTANIST'S NOTES

        The research data above may contain `botanistNotes` (analytical observations from
        the research agent) and a `bestQuote` (the most revealing quote with a `why` field
        explaining its significance). USE these as input to your classification:
        - Let the botanist's observations inform your model choice and confidence level
        - If the notes flag a taxonomy edge case, address it in classificationRationale
        - The bestQuote often reveals how leaders *think* about AI structure — use it
        - Build on these observations in your own taxonomyFeedback, don't just repeat them

        ## OUTPUT INSTRUCTIONS

        Write a single JSON file to: {specimen_path}

        Populate these fields:
        - id: "{slug}"
        - name: "{company}"
        - title: Descriptive title about their AI structure (6-10 words)
        - classification:
          - structuralModel: integer 1-9 (walk the decision tree above)
          - structuralModelName: name from taxonomy
          - subType: "5a"/"5b"/"5c"/"6a"/"6b"/"6c" or null
          - orientation: "Structural" | "Contextual" | "Temporal"
          - confidence: "High" | "Medium" | "Low"
          - classificationRationale: Why this model and orientation
          - typeSpecimen: false (unless extraordinary exemplar)
        - habitat: industry, sector, orgSize (Startup/Scaleup/Mid-market/Enterprise), etc.
        - description: 2-3 paragraphs about how they structure AI work
        - observableMarkers: all 5 fields from research data
        - mechanisms: any of the confirmed mechanisms that apply
        - quotes: verbatim from research data, with full attribution
        - layers: one initial layer with date "{today[:7]}", label, summary, sourceRefs
        - sources: all from research data, with IDs like "{slug}-earnings-2025", type, URL, dates
        - contingencies: assess all 5 from available data
        - tensionPositions: score all 5 axes where data supports (-1.0 to +1.0)
        - openQuestions: from research data
        - taxonomyFeedback: IMPORTANT — write 2-3 substantive observations here,
          each prefixed with "[{today[:7]}]" for temporal tracking:
          (a) How does this specimen fit or challenge the taxonomy? Any edge cases?
          (b) What is most structurally interesting about how this org does AI?
          (c) Any patterns you notice compared to the model descriptions above?
          These are "botanist's notes" — analytical observations, not just labels.
          Example: "[2026-02] Apple's functional org structure creates an unusual M4
          variant where spokes are expertise-based rather than product-based."
        - meta: status="Active" (or "Stub" if very thin), created="{today}",
          lastUpdated="{today}", completeness="High"/"Medium"/"Low"

        IMPORTANT:
        - structuralModel is an INTEGER (1-9), not a string
        - For quotes, copy text EXACTLY from the research data
        - For source IDs, use descriptive slugs like "{slug}-q4-2025-earnings"
        - Completeness: High = 3+ sources with detailed structure; Medium = 2+ sources; Low = 1

        After writing the file, output this summary line to stdout:
        CURATE_RESULT: {slug} | new | M{{model}} | {{orientation}} | {{confidence}} | {{completeness}} | {{n_quotes}} quotes | {{n_sources}} sources | {{brief_note}}
        """)

    return prompt


# ─── Agent Runner ────────────────────────────────────────────────────────────

def run_agent(slug: str, prompt: str, skip_permissions: bool = False) -> bool:
    """Run a single Claude CLI curation agent. Returns True if specimen file created/updated."""
    log.info(f"▶ Starting agent: {slug}")
    start = time.time()

    cmd = ["claude", "-p", prompt, "--model", "opus"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=str(PROJECT_ROOT),
        )
        elapsed = time.time() - start

        specimen_file = SPECIMENS_DIR / f"{slug}.json"
        if specimen_file.exists():
            try:
                with open(specimen_file) as f:
                    data = json.load(f)

                cls = data.get("classification", {})
                meta = data.get("meta", {})
                model = cls.get("structuralModel", "?")
                orientation = cls.get("orientation", "?")
                confidence = cls.get("confidence", "?")
                completeness = meta.get("completeness", "?")
                n_quotes = len(data.get("quotes", []))
                n_sources = len(data.get("sources", []))

                log.info(
                    f"✓ {slug}: M{model} {orientation} {confidence} "
                    f"{n_quotes}q {n_sources}s in {elapsed:.0f}s"
                )

                # Parse CURATE_RESULT line from stdout for session log
                curate_result = ""
                if result.stdout:
                    for line in result.stdout.splitlines():
                        if line.startswith("CURATE_RESULT:"):
                            curate_result = line
                            break

                return True

            except json.JSONDecodeError:
                log.error(f"✗ {slug}: Specimen file exists but invalid JSON — deleting")
                specimen_file.unlink()
                return False
        else:
            stdout_preview = result.stdout[:500] if result.stdout else "(empty)"
            stderr_preview = result.stderr[:300] if result.stderr else "(empty)"
            log.error(
                f"✗ {slug}: No specimen file after {elapsed:.0f}s "
                f"(exit={result.returncode})\n"
                f"  stdout: {stdout_preview}\n"
                f"  stderr: {stderr_preview}"
            )
            return False

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        log.error(f"✗ {slug}: TIMEOUT after {elapsed:.0f}s")
        # Clean up partially written file
        specimen_file = SPECIMENS_DIR / f"{slug}.json"
        if specimen_file.exists():
            try:
                json.loads(specimen_file.read_text())
            except (json.JSONDecodeError, Exception):
                log.warning(f"  Removing partial file: {specimen_file.name}")
                specimen_file.unlink()
        return False
    except Exception as e:
        log.error(f"✗ {slug}: Exception: {e}")
        return False


# ─── Specimen Validation ─────────────────────────────────────────────────────

def validate_specimen(slug: str) -> tuple[bool, list[str]]:
    """Validate a specimen file has required fields and valid values."""
    specimen_path = SPECIMENS_DIR / f"{slug}.json"
    if not specimen_path.exists():
        return False, ["File does not exist"]

    try:
        with open(specimen_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    issues = []

    # Required top-level fields
    for field in ["id", "name", "classification", "description", "sources", "layers", "meta"]:
        if field not in data:
            issues.append(f"Missing required field: {field}")

    # Classification validation
    cls = data.get("classification", {})
    model = cls.get("structuralModel")
    if model is not None and model not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        issues.append(f"Invalid structuralModel: {model}")
    orientation = cls.get("orientation")
    if orientation is not None and orientation not in ["Structural", "Contextual", "Temporal"]:
        issues.append(f"Invalid orientation: {orientation}")
    confidence = cls.get("confidence")
    if confidence not in ["High", "Medium", "Low", None]:
        issues.append(f"Invalid confidence: {confidence}")

    # Meta validation
    meta = data.get("meta", {})
    status = meta.get("status")
    if status not in ["Active", "Stub", "Archived", None]:
        issues.append(f"Invalid status: {status}")

    # Must have at least one layer and source
    if not data.get("layers"):
        issues.append("No layers")
    if not data.get("sources"):
        issues.append("No sources")

    return len(issues) == 0, issues


# ─── Registry & Queue Updaters ───────────────────────────────────────────────

def update_specimen_registry(slug: str, specimen_data: dict):
    """Add or update a specimen entry in specimens/registry.json."""
    try:
        with open(REGISTRY_FILE) as f:
            registry = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        registry = {
            "description": "Specimen Registry",
            "lastUpdated": date.today().isoformat(),
            "totalSpecimens": 0,
            "byModel": {},
            "byOrientation": {},
            "typeSpecimens": [],
            "specimens": [],
        }

    cls = specimen_data.get("classification", {})
    meta = specimen_data.get("meta", {})

    new_entry = {
        "id": slug,
        "name": specimen_data.get("name", ""),
        "structuralModel": cls.get("structuralModel"),
        "subType": cls.get("subType"),
        "secondaryModel": cls.get("secondaryModel"),
        "orientation": cls.get("orientation"),
        "typeSpecimen": cls.get("typeSpecimen", False),
        "status": meta.get("status", "Active"),
        "created": meta.get("created", date.today().isoformat()),
        "lastUpdated": meta.get("lastUpdated", date.today().isoformat()),
        "layerCount": len(specimen_data.get("layers", [])),
        "completeness": meta.get("completeness", "Low"),
        "confidence": cls.get("confidence", "Low"),
    }

    # Find existing entry or append
    existing_idx = None
    for i, entry in enumerate(registry["specimens"]):
        if entry["id"] == slug:
            existing_idx = i
            break

    if existing_idx is not None:
        registry["specimens"][existing_idx] = new_entry
    else:
        registry["specimens"].append(new_entry)
        registry["specimens"].sort(key=lambda x: x["id"])

    # Recalculate aggregates
    registry["totalSpecimens"] = len(registry["specimens"])
    model_counts = Counter(
        str(s["structuralModel"]) for s in registry["specimens"]
        if s.get("structuralModel") is not None
    )
    registry["byModel"] = {k: v for k, v in sorted(model_counts.items())}
    orient_counts = Counter(
        s["orientation"] for s in registry["specimens"]
        if s.get("orientation") is not None
    )
    registry["byOrientation"] = dict(orient_counts)
    registry["lastUpdated"] = date.today().isoformat()

    save_json(REGISTRY_FILE, registry)


def mark_curated_in_queue(slug: str, session_name: str):
    """Mark a research queue entry as curated."""
    try:
        with open(QUEUE_FILE) as f:
            queue_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    for entry in queue_data.get("queue", []):
        if slug in entry.get("organizationsFound", []):
            entry["status"] = "curated"
            entry["curatedIn"] = session_name

    queue_data["lastUpdated"] = date.today().isoformat()

    save_json(QUEUE_FILE, queue_data)


def add_to_synthesis_queue(slug: str, action: str, notes: str):
    """Add a curated specimen to the synthesis queue for Phase 3."""
    try:
        with open(SYNTHESIS_QUEUE_FILE) as f:
            sq = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sq = {
            "description": "Synthesis queue",
            "lastUpdated": date.today().isoformat(),
            "lastSynthesisDate": None,
            "queue": [],
        }

    session_name = f"{date.today().isoformat()}-overnight-curate.md"

    sq["queue"].append({
        "specimenId": slug,
        "action": action,
        "curatedIn": session_name,
        "status": "pending",
        "synthesizedIn": None,
        "notes": notes,
    })
    sq["lastUpdated"] = date.today().isoformat()

    save_json(SYNTHESIS_QUEUE_FILE, sq)


# ─── Retry Queue ─────────────────────────────────────────────────────────────

def update_retry_queue(failed_slugs: list[dict], succeeded_slugs: list[str]):
    """
    Update the persistent retry queue.
    - Add failed slugs (or increment failCount)
    - Remove succeeded slugs
    """
    try:
        with open(RETRY_QUEUE_FILE) as f:
            data = json.load(f)
        existing = {e["slug"]: e for e in data.get("queue", [])}
    except (FileNotFoundError, json.JSONDecodeError):
        existing = {}

    # Remove successes
    for slug in succeeded_slugs:
        existing.pop(slug, None)

    # Add/update failures
    for fail in failed_slugs:
        slug = fail["slug"]
        if slug in existing:
            existing[slug]["failCount"] = existing[slug].get("failCount", 0) + 1
            existing[slug]["lastError"] = fail.get("error", "Unknown")
            existing[slug]["lastFailedDate"] = date.today().isoformat()
        else:
            existing[slug] = {
                "slug": slug,
                "pendingFile": f"research/pending/{slug}.json",
                "failedDate": date.today().isoformat(),
                "lastFailedDate": date.today().isoformat(),
                "failCount": fail.get("priorFailCount", 0) + 1,
                "lastError": fail.get("error", "Unknown"),
                "maxRetries": MAX_RETRY_ATTEMPTS,
            }

    retry_data = {
        "description": "Curation retry queue — specimens that failed overnight curation",
        "lastUpdated": date.today().isoformat(),
        "queue": list(existing.values()),
    }

    save_json(RETRY_QUEUE_FILE, retry_data)

    abandoned = [e for e in existing.values() if e.get("failCount", 0) >= MAX_RETRY_ATTEMPTS]
    if abandoned:
        log.warning(
            f"  {len(abandoned)} specimen(s) abandoned after {MAX_RETRY_ATTEMPTS} attempts: "
            + ", ".join(e["slug"] for e in abandoned)
        )


# ─── Session Log Writer ─────────────────────────────────────────────────────

def write_session_log(
    results: list[dict],
    skipped_files: list[str],
    failed_final: list[dict],
    start_time: datetime,
    existing_registry: dict,
):
    """Write a human-readable session log to curation/sessions/."""
    CURATE_SESSION_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()
    elapsed = datetime.now() - start_time

    succeeded = [r for r in results if r["success"]]
    new_count = len([r for r in succeeded if r["action"] == "new"])
    updated_count = len([r for r in succeeded if r["action"] == "updated"])

    # Results table
    rows = []
    for r in succeeded:
        rows.append(
            f"| {r['slug']:30s} | {r['action']:7s} | M{r.get('model') or '?':<2} "
            f"| {(r.get('orientation') or '?'):11s} | {(r.get('confidence') or '?'):6s} "
            f"| {(r.get('completeness') or '?'):6s} | {r.get('n_quotes', 0) or 0:6d} "
            f"| {r.get('n_sources', 0) or 0:7d} | {r.get('elapsed', 0):5.0f}s |"
        )

    # Model distribution
    model_counts = Counter(str(r.get("model", "?")) for r in succeeded)
    model_rows = []
    for m, c in sorted(model_counts.items()):
        name = MODEL_NAMES.get(int(m), "Unknown") if m.isdigit() else "Unknown"
        existing_count = existing_registry.get("byModel", {}).get(m, 0)
        model_rows.append(f"| M{m} {name:30s} | {c:5d} | {existing_count:8d} | {existing_count + c:9d} |")

    # Orientation distribution
    orient_counts = Counter(r.get("orientation", "?") for r in succeeded)
    orient_rows = []
    for o, c in sorted(orient_counts.items()):
        orient_rows.append(f"| {o:11s} | {c:5d} |")

    # Confidence distribution
    conf_counts = Counter(r.get("confidence", "?") for r in succeeded)
    conf_rows = []
    for c, n in sorted(conf_counts.items()):
        conf_rows.append(f"| {c:6s} | {n:5d} |")

    # Industries covered
    industry_counts = Counter(r.get("sector", "Unknown") for r in succeeded)
    industry_rows = []
    for ind, c in industry_counts.most_common():
        industry_rows.append(f"| {ind:25s} | {c:5d} |")

    # Extract rich content from specimen files (descriptions, rationales, feedback)
    all_feedback = []
    specimen_sections = []
    for r in succeeded:
        specimen_path = SPECIMENS_DIR / f"{r['slug']}.json"
        if not specimen_path.exists():
            continue
        try:
            with open(specimen_path) as f:
                spec = json.load(f)
        except (json.JSONDecodeError, KeyError):
            continue

        cls = spec.get("classification", {})
        description = spec.get("description", "").strip()
        rationale = cls.get("classificationRationale", "").strip()
        feedback = spec.get("taxonomyFeedback", [])
        open_qs = spec.get("openQuestions", [])
        mechanisms = spec.get("mechanisms", [])
        best_quotes = spec.get("quotes", [])[:3]  # top 3 quotes

        model_num = cls.get("structuralModel", "?")
        model_name = MODEL_NAMES.get(model_num, "Unknown") if isinstance(model_num, int) else "?"

        section = f"### {r['slug']} — M{model_num} {model_name} | {r.get('orientation', '?')} | {r.get('confidence', '?')}\n\n"
        if description:
            # Truncate long descriptions
            desc_preview = description[:400] + "..." if len(description) > 400 else description
            section += f"**Description:** {desc_preview}\n\n"
        if rationale:
            section += f"**Classification rationale:** {rationale}\n\n"
        if mechanisms:
            mech_str = ", ".join(f"M{m.get('id', '?')} {m.get('name', '?')}" for m in mechanisms)
            section += f"**Mechanisms linked:** {mech_str}\n\n"
        if best_quotes:
            section += "**Key quotes:**\n"
            for q in best_quotes:
                quote_text = q.get("text", "")[:120]
                if len(q.get("text", "")) > 120:
                    quote_text += "..."
                section += f"- \"{quote_text}\" — {q.get('speaker', '?')}\n"
            section += "\n"
        if feedback:
            section += "**Botanist's notes:**\n"
            for fb in feedback:
                section += f"- {fb}\n"
            section += "\n"
        if open_qs:
            section += "**Open questions:**\n"
            for q in open_qs[:3]:
                section += f"- {q}\n"
            section += "\n"

        specimen_sections.append(section)

        for fb in feedback:
            all_feedback.append(f"- **{r['slug']}**: {fb}")

    # Failed table
    failed_rows = []
    for f_item in failed_final:
        failed_rows.append(f"| {f_item['slug']:30s} | {f_item.get('error', 'Unknown'):50s} |")

    # Skipped files table
    skipped_rows = []
    for sf in skipped_files:
        skipped_rows.append(f"| {sf:50s} | Multi-company session file |")

    content = dedent(f"""\
    # Overnight Curate Run — {today_str}

    **Started:** {start_time.strftime('%Y-%m-%d %H:%M')}
    **Duration:** {elapsed.total_seconds() / 60:.0f} minutes
    **Curated:** {len(succeeded)} | **New:** {new_count} | **Updated:** {updated_count} | **Failed:** {len(failed_final)}
    **Method:** `scripts/overnight-curate.py` via `claude -p --model opus`

    ## Results

    | Specimen                       | Action  | Model | Orientation | Conf.  | Compl. | Quotes | Sources | Time   |
    |--------------------------------|---------|-------|-------------|--------|--------|--------|---------|--------|
    {chr(10).join(rows) if rows else "| (none) | | | | | | | | |"}

    ## Model Distribution (this batch)

    | Model                                | Count | Existing | New Total |
    |--------------------------------------|-------|----------|-----------|
    {chr(10).join(model_rows) if model_rows else "| (none) | | | |"}

    ## Orientation Distribution

    | Orientation | Count |
    |-------------|-------|
    {chr(10).join(orient_rows) if orient_rows else "| (none) | |"}

    ## Confidence Distribution

    | Level  | Count |
    |--------|-------|
    {chr(10).join(conf_rows) if conf_rows else "| (none) | |"}

    ## Industries Covered

    | Industry                  | Count |
    |---------------------------|-------|
    {chr(10).join(industry_rows) if industry_rows else "| (none) | |"}

    ## Per-Specimen Analysis

    {chr(10).join(specimen_sections) if specimen_sections else "(no specimen details to report)"}

    ## Taxonomy Feedback Summary

    {chr(10).join(all_feedback) if all_feedback else "- (none collected)"}

    ## Skipped Files

    | File                                               | Reason                     |
    |----------------------------------------------------|----------------------------|
    {chr(10).join(skipped_rows) if skipped_rows else "| (none) | |"}

    ## Failed Specimens

    | Specimen                       | Error                                              |
    |--------------------------------|----------------------------------------------------|
    {chr(10).join(failed_rows) if failed_rows else "| (none) | |"}

    ## Next Steps

    - Run `/synthesize` to process {len(succeeded)} newly queued specimens
    - Run `overnight-purpose-claims.py` for {new_count} newly created specimens
    - Review failed specimens in `research/curate-retry-queue.json`
    - Process {len(skipped_files)} multi-company session files via interactive `/curate`
    """)

    log_path = CURATE_SESSION_DIR / f"{today_str}-overnight-curate.md"
    counter = 1
    while log_path.exists():
        counter += 1
        log_path = CURATE_SESSION_DIR / f"{today_str}-overnight-curate-{counter}.md"

    with open(log_path, "w") as f:
        f.write(content)
    log.info(f"Session log: {log_path}")
    return log_path


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Overnight curation — transform research pending files into specimen cards"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show queue and exit")
    parser.add_argument("--limit", type=int, default=0, help="Max specimens to curate (0 = all)")
    parser.add_argument("--company", type=str, help="Curate one specific company (by slug)")
    parser.add_argument("--skip-permissions", action="store_true",
                        help="Add --dangerously-skip-permissions to claude CLI calls")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("OVERNIGHT CURATE RUN")
    log.info("=" * 60)

    # ─── Preflight Checks ─────────────────────────────────────────────
    failures = preflight_check(
        required_files=[REGISTRY_FILE],
        check_claude_cli=not args.dry_run,
        required_dirs=[PENDING_DIR, SPECIMENS_DIR, CURATE_SESSION_DIR],
    )
    if failures:
        for f in failures:
            log.error(f"PREFLIGHT FAIL: {f}")
        log.error("Fix the above before running. Aborting.")
        sys.exit(1)

    # ─── Lock ─────────────────────────────────────────────────────────
    lock_path = None
    if not args.dry_run:
        try:
            lock_path = acquire_lock("overnight-curate")
            log.info("Lock acquired")
        except RuntimeError as e:
            log.error(f"LOCK FAIL: {e}")
            sys.exit(1)

    # Snapshot existing registry for session log comparison
    try:
        with open(REGISTRY_FILE) as f:
            existing_registry = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_registry = {"byModel": {}, "byOrientation": {}, "totalSpecimens": 0}

    # Build queue
    queue, skipped_files = build_curate_queue(company_filter=args.company)

    if skipped_files:
        log.info(f"Skipped {len(skipped_files)} multi-company files: {', '.join(skipped_files)}")

    log.info(f"Queue: {len(queue)} specimens to curate")

    if args.limit > 0:
        queue = queue[:args.limit]
        log.info(f"Limited to {args.limit}")

    # Dry run
    if args.dry_run:
        log.info("\n--- DRY RUN — Curation queue ---")
        for i, item in enumerate(queue, 1):
            retry_tag = " [RETRY]" if item["isRetry"] else ""
            log.info(
                f"  {i:2d}. {item['slug']:35s} | {item['company']:30s} "
                f"| {item['sector']:20s}{retry_tag}"
            )
        log.info(f"\nTotal: {len(queue)} to curate")
        if skipped_files:
            log.info(f"Skipped (multi-company): {len(skipped_files)} files")
            for sf in skipped_files:
                log.info(f"  - {sf}")
        log.info("Run without --dry-run to execute.")
        return

    # ─── Run Loop ─────────────────────────────────────────────────────
    start_time = datetime.now()
    results = []
    failed = []
    session_name = f"{date.today().isoformat()}-overnight-curate.md"

    for i, item in enumerate(queue, 1):
        slug = item["slug"]
        retry_tag = " [RETRY]" if item["isRetry"] else ""
        log.info(f"\n--- [{i}/{len(queue)}] {item['company']}{retry_tag} ---")

        # Load research data
        pending_path = Path(item["pendingFile"])
        try:
            with open(pending_path) as f:
                pending_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log.error(f"✗ {slug}: Cannot read pending file: {e}")
            failed.append({"slug": slug, "error": f"Bad pending file: {e}",
                           "priorFailCount": item.get("failCount", 0)})
            results.append({"slug": slug, "company": item["company"],
                            "sector": item["sector"], "success": False, "elapsed": 0})
            continue

        # Check for existing specimen (ADD LAYER vs CREATE)
        specimen_path = SPECIMENS_DIR / f"{slug}.json"
        existing_specimen = None
        action = "new"
        if specimen_path.exists():
            try:
                with open(specimen_path) as f:
                    existing_specimen = json.load(f)
                action = "updated"
            except (json.JSONDecodeError, KeyError):
                existing_specimen = None

        # Build prompt and run agent
        prompt = build_curate_prompt(slug, pending_data, existing_specimen)
        agent_start = time.time()
        success = run_agent(slug, prompt, args.skip_permissions)
        agent_elapsed = time.time() - agent_start

        if success:
            # Validate
            valid, issues = validate_specimen(slug)
            if not valid:
                log.warning(f"  Validation issues for {slug}: {issues}")
                # Still count as success if file exists — issues are warnings

            # Read specimen for result data
            with open(specimen_path) as f:
                spec_data = json.load(f)

            cls = spec_data.get("classification", {})
            meta = spec_data.get("meta", {})

            result = {
                "slug": slug,
                "company": item["company"],
                "sector": item["sector"],
                "success": True,
                "action": action,
                "model": cls.get("structuralModel", "?"),
                "orientation": cls.get("orientation", "?"),
                "confidence": cls.get("confidence", "?"),
                "completeness": meta.get("completeness", "?"),
                "n_quotes": len(spec_data.get("quotes", [])),
                "n_sources": len(spec_data.get("sources", [])),
                "elapsed": agent_elapsed,
            }
            results.append(result)

            # Post-agent updates
            try:
                update_specimen_registry(slug, spec_data)
                log.info(f"  → Registry updated for {slug}")
            except Exception as e:
                log.error(f"  Registry update failed for {slug}: {e}")

            try:
                mark_curated_in_queue(slug, session_name)
            except Exception as e:
                log.error(f"  Queue update failed for {slug}: {e}")

            try:
                model_name = MODEL_NAMES.get(cls.get("structuralModel"), "Unknown")
                notes = f"M{cls.get('structuralModel', '?')} {model_name}, {cls.get('orientation', '?')}"
                add_to_synthesis_queue(slug, action, notes)
                log.info(f"  → Queued for synthesis")
            except Exception as e:
                log.error(f"  Synthesis queue update failed for {slug}: {e}")

        else:
            results.append({
                "slug": slug,
                "company": item["company"],
                "sector": item["sector"],
                "success": False,
                "action": action,
                "elapsed": agent_elapsed,
            })
            failed.append({
                "slug": slug,
                "error": "Agent failed or timed out",
                "priorFailCount": item.get("failCount", 0),
            })

        if i < len(queue):
            time.sleep(PAUSE_BETWEEN)

    # ─── Retry Failed ────────────────────────────────────────────────
    if failed and MAX_RETRIES > 0:
        log.info(f"\n--- RETRYING {len(failed)} failed specimens ---")
        still_failed = []
        for fail_item in failed:
            slug = fail_item["slug"]
            pending_path = PENDING_DIR / f"{slug}.json"
            if not pending_path.exists():
                still_failed.append(fail_item)
                continue

            with open(pending_path) as f:
                pending_data = json.load(f)

            specimen_path = SPECIMENS_DIR / f"{slug}.json"
            existing_specimen = None
            if specimen_path.exists():
                try:
                    with open(specimen_path) as f:
                        existing_specimen = json.load(f)
                except (json.JSONDecodeError, KeyError):
                    pass

            prompt = build_curate_prompt(slug, pending_data, existing_specimen)
            agent_start = time.time()
            success = run_agent(slug, prompt, args.skip_permissions)
            agent_elapsed = time.time() - agent_start

            if success:
                with open(specimen_path) as f:
                    spec_data = json.load(f)
                cls = spec_data.get("classification", {})
                meta = spec_data.get("meta", {})

                # Update the result in place
                for r in results:
                    if r["slug"] == slug:
                        r["success"] = True
                        r["model"] = cls.get("structuralModel", "?")
                        r["orientation"] = cls.get("orientation", "?")
                        r["confidence"] = cls.get("confidence", "?")
                        r["completeness"] = meta.get("completeness", "?")
                        r["n_quotes"] = len(spec_data.get("quotes", []))
                        r["n_sources"] = len(spec_data.get("sources", []))
                        r["elapsed"] += agent_elapsed
                        break

                try:
                    update_specimen_registry(slug, spec_data)
                    action = "updated" if existing_specimen else "new"
                    mark_curated_in_queue(slug, session_name)
                    model_name = MODEL_NAMES.get(cls.get("structuralModel"), "Unknown")
                    notes = f"M{cls.get('structuralModel', '?')} {model_name}"
                    add_to_synthesis_queue(slug, action, notes)
                except Exception as e:
                    log.error(f"  Post-retry update failed for {slug}: {e}")
            else:
                still_failed.append(fail_item)

            time.sleep(PAUSE_BETWEEN)

        failed = still_failed

    # ─── Update Retry Queue ──────────────────────────────────────────
    succeeded_slugs = [r["slug"] for r in results if r["success"]]
    update_retry_queue(failed, succeeded_slugs)

    # ─── Summary ─────────────────────────────────────────────────────
    elapsed_total = datetime.now() - start_time
    succeeded = [r for r in results if r["success"]]
    failed_final = [r for r in results if not r["success"]]

    log.info("\n" + "=" * 60)
    log.info("RUN COMPLETE")
    log.info("=" * 60)
    log.info(f"Duration: {elapsed_total.total_seconds() / 60:.0f} minutes")
    log.info(f"Specimens curated: {len(succeeded)}")
    log.info(f"New: {len([r for r in succeeded if r.get('action') == 'new'])}")
    log.info(f"Updated: {len([r for r in succeeded if r.get('action') == 'updated'])}")
    log.info(f"Failed: {len(failed_final)}")

    if succeeded:
        models = Counter(str(r.get("model", "?")) for r in succeeded)
        log.info("\nModel distribution:")
        for m, c in models.most_common():
            name = MODEL_NAMES.get(int(m), "?") if str(m).isdigit() else "?"
            log.info(f"  M{m} {name}: {c}")

        orientations = Counter(r.get("orientation", "?") for r in succeeded)
        log.info("\nOrientation distribution:")
        for o, c in orientations.most_common():
            log.info(f"  {o}: {c}")

    if failed_final:
        log.info(f"\nFailed: {[r['slug'] for r in failed_final]}")
        log.info(f"Written to: {RETRY_QUEUE_FILE}")

    # New total
    try:
        with open(REGISTRY_FILE) as f:
            final_registry = json.load(f)
        log.info(f"\nRegistry total: {final_registry.get('totalSpecimens', '?')} specimens "
                 f"(was {existing_registry.get('totalSpecimens', '?')})")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Write session log
    write_session_log(
        results=results,
        skipped_files=skipped_files,
        failed_final=[{"slug": r["slug"], "error": "Agent failed"} for r in failed_final],
        start_time=start_time,
        existing_registry=existing_registry,
    )

    # Audit log
    if succeeded:
        write_changelog("overnight-curate.py", [
            f"Curated {len(succeeded)} specimens: {', '.join(r['slug'] for r in succeeded)}",
            f"New: {len([r for r in succeeded if r.get('action') == 'new'])}, "
            f"Updated: {len([r for r in succeeded if r.get('action') == 'updated'])}",
        ])

    # ─── Release Lock ─────────────────────────────────────────────────
    if lock_path:
        release_lock(lock_path)
        log.info("Lock released")

    log.info("\nSpecimens queued for synthesis — run /synthesize next.")


if __name__ == "__main__":
    main()
