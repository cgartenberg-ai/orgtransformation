#!/usr/bin/env python3
"""
overnight-research.py
=====================
Orchestrates sequential research scans for new specimen targets via Claude CLI.
Reads target-specimens.json, builds prompts for each target, invokes
`claude -p --model opus` to search for structural AI findings, and writes
research output files for subsequent curation.

Unlike overnight-purpose-claims.py (which scans EXISTING specimens for claims),
this script discovers STRUCTURAL FINDINGS for companies that don't yet have
specimen files. Output goes to research/pending/ as research session files
that feed into the /curate workflow.

Usage:
    python3 scripts/overnight-research.py                     # Run all targets
    python3 scripts/overnight-research.py --dry-run           # Show queue
    python3 scripts/overnight-research.py --limit 5           # Only scan 5
    python3 scripts/overnight-research.py --company "Apple"   # Scan one company
    python3 scripts/overnight-research.py --quadrant Q4       # Scan one quadrant
    python3 scripts/overnight-research.py --priority high     # High priority only
    python3 scripts/overnight-research.py --skip-permissions  # Unattended mode

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

TARGET_LIST = PROJECT_ROOT / "research" / "target-specimens.json"
PENDING_DIR = PROJECT_ROOT / "research" / "pending"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"
SESSION_DIR = PROJECT_ROOT / "research" / "sessions"
QUEUE_FILE = PROJECT_ROOT / "research" / "queue.json"

TIMEOUT_SECONDS = 25 * 60   # 25 minutes per agent
PAUSE_BETWEEN = 10           # seconds between agents
MAX_RETRIES = 1              # retry failed targets once

# ─── Logging ─────────────────────────────────────────────────────────────────

log = setup_logging("overnight-research")

# ─── Taxonomy Reference ─────────────────────────────────────────────────────

TAXONOMY = """
Structural Models (classify the organization into ONE primary model):
  M1 Research Lab — Fundamental research, breakthroughs. 3-10 year horizon. Pure exploration.
  M2 Center of Excellence — Governance, standards, enablement. 6-24 month horizon.
  M3 Embedded Teams — Product-specific AI features. Quarterly cadence.
  M4 Hybrid/Hub-and-Spoke — Central standards + distributed execution. Mixed horizons.
  M5 Product/Venture Lab — Commercialize AI into products/ventures. 6-36 months.
     5a Internal Incubator — Products absorbed into parent (Adobe Firefly)
     5b Venture Builder — Creates independent companies (Google X → Waymo)
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
  Temporal — Organization cycles between exploration and execution phases
"""

# ─── Prompt Builder ──────────────────────────────────────────────────────────

def build_research_prompt(target: dict) -> str:
    """Build the full prompt for a research agent scanning a new target company."""

    company = target["company"]
    leader = target["leader"]
    leader_title = target["leaderTitle"]
    sector = target["sector"]
    quadrant = target["quadrant"]
    conference = target.get("conference") or "None known"
    rationale = target["rationale"]
    ticker = target.get("ticker") or "PRIVATE"
    today = date.today().isoformat()

    # Generate a slug for the output file
    slug = company.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    output_path = str(PENDING_DIR / f"{slug}.json")

    prompt = dedent(f"""\
    You are a research agent scanning "{company}" for organizational AI structure findings.
    COMPLETE THIS IN UNDER 20 MINUTES.

    TASK: Discover how {company} structures its AI work — team structure, leadership,
    reporting lines, investment levels, strategic framing — and produce a structured
    research output file.

    ## SPEED RULES

    1. **NEVER make parallel WebFetch calls.** Fetch URLs ONE AT A TIME.
    2. **One retry max per URL.** If WebFetch fails, skip and move on.
    3. **Stop fetching after 6 URLs.** Prioritize quality over quantity.
    4. **Skip paywalled domains:** {', '.join(BLOCKED_DOMAINS)}

    ## Target Context

    - Company: {company}
    - Ticker: {ticker}
    - CEO/Leader: {leader} ({leader_title})
    - Sector: {sector}
    - Quadrant: {quadrant}
    - Conference presence: {conference}
    - Why we're scanning: {rationale}

    ## What We're Looking For

    We study how organizations STRUCTURALLY enable both AI exploration and operational
    execution. For each company, we need to understand:

    1. **AI Team Structure**: Is there a dedicated AI team/lab? How is it organized?
       Who leads it? Does it report to the CEO, CTO, a CAIO, or somewhere else?
    2. **Structural Model**: Which of these 9 models best fits? (see taxonomy below)
    3. **Key People**: CEO, CAIO/CDO/Head of AI, key AI leaders and their titles
    4. **Investment Level**: AI headcount, budget, % of R&D, CapEx commitments
    5. **Observable Markers**: Reporting structure, resource allocation, time horizons,
       decision rights, metrics used
    6. **Key Quotes**: Verbatim quotes from leaders about AI strategy, purpose, vision
    7. **Sources**: URLs for everything — earnings calls, press, interviews, conference talks

    {TAXONOMY}

    ## Search Queries — Run ALL 5

    1. "{company}" AI team OR "AI organization" OR "chief AI officer" OR CAIO structure
    2. "{leader}" AI strategy OR vision OR transformation OR investment 2025 2026
    3. "{company}" AI earnings call OR annual report OR shareholder letter 2025 2026
    4. "{company}" AI lab OR research OR "center of excellence" OR hub
    5. "{company}" "{leader}" AI interview OR podcast OR keynote OR conference

    ## WebFetch Instructions

    Fetch URLs ONE AT A TIME. Prioritize:
    1. **Earnings call transcripts** — richest structural data (team sizes, investment, reporting)
    2. **Press profiles / long-form interviews** — how leaders frame AI strategy
    3. **Conference talks** — especially from: {conference}
    4. **Company newsroom / blog posts** — official announcements of AI initiatives

    Prompt WebFetch with: "Extract all information about {company}'s AI strategy,
    team structure, leadership, investment, and organizational approach to AI.
    Include all direct quotes from executives."

    ## Output

    Write a JSON file to: {output_path}

    Use this structure:
    {{
      "company": "{company}",
      "ticker": "{ticker}",
      "leader": "{leader}",
      "leaderTitle": "{leader_title}",
      "sector": "{sector}",
      "quadrant": "{quadrant}",
      "scannedDate": "{today}",
      "searchesCompleted": 5,
      "urlsFetched": N,
      "fetchFailures": [],

      "structuralFindings": {{
        "suggestedModel": N,
        "suggestedModelName": "e.g. Hybrid/Hub-and-Spoke",
        "suggestedOrientation": "Structural|Contextual|Temporal",
        "confidence": "High|Medium|Low",
        "rationale": "Why this classification, based on evidence found",
        "aiTeamStructure": "Description of how AI work is organized",
        "keyPeople": [
          {{"name": "...", "title": "...", "role": "..."}}
        ],
        "investmentSignals": "Budget, headcount, CapEx, % of R&D",
        "observableMarkers": {{
          "reportingStructure": "Who does AI report to?",
          "resourceAllocation": "Dedicated budget? Shared? Ring-fenced?",
          "timeHorizons": "Short-term (quarters) vs. long-term (years)?",
          "decisionRights": "Centralized vs. distributed AI decisions?",
          "metrics": "What does the org measure for AI success?"
        }}
      }},

      "quotes": [
        {{
          "text": "EXACT VERBATIM QUOTE",
          "speaker": "Full Name",
          "speakerTitle": "Title",
          "source": "Source name",
          "sourceUrl": "URL",
          "sourceDate": "YYYY-MM-DD or YYYY-MM",
          "context": "What was the occasion/topic"
        }}
      ],

      "sources": [
        {{
          "name": "Source name",
          "url": "URL",
          "type": "Earnings Call|Press|Interview|Conference|Blog|Report",
          "date": "YYYY-MM-DD or YYYY-MM",
          "notes": "What was useful in this source"
        }}
      ],

      "summary": "2-3 sentence summary of how this organization structures AI work",
      "openQuestions": ["Things we couldn't determine from available sources"],
      "conferenceFindings": "What we found about their conference presentation, if applicable",

      "botanistNotes": [
        "2-4 analytical observations from a research botanist's perspective:",
        "- What is most structurally interesting or surprising about this org?",
        "- Any patterns that connect to or challenge the taxonomy?",
        "- How does this compare to what you'd expect for this industry/size?",
        "- Any provocative quotes that reveal how leaders THINK about AI structure?"
      ],
      "bestQuote": {{
        "text": "The single most revealing/provocative quote found — the one that best captures how this org thinks about AI",
        "speaker": "Full Name",
        "why": "Why this quote is analytically interesting"
      }}
    }}

    IMPORTANT:
    - Only include VERBATIM quotes — never paraphrase
    - Always include source URLs — no URL, no finding
    - If you can't determine the structural model with confidence, say so in rationale
    - It's fine to write a file with limited findings — "we looked and found little" is data
    - If the company is very secretive about AI structure (e.g., Apple), document THAT as a finding
    - The botanistNotes field is CRITICAL — this is where you record your analytical observations
      as a researcher. Don't just describe what you found; note what's interesting, surprising,
      or pattern-breaking about it.
    """)

    return prompt

# ─── Agent Runner ─────────────────────────────────────────────────────────────

def get_slug(company: str) -> str:
    """Generate a filesystem-safe slug from company name."""
    slug = company.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
    return "".join(c for c in slug if c.isalnum() or c == "-")


def run_agent(target: dict, prompt: str, skip_permissions: bool = False) -> bool:
    """Run a single Claude CLI research agent. Returns True if output file created.

    Uses Popen with process groups so timeout kills the entire process tree
    (claude + any child processes), preventing zombie orphans.
    """
    company = target["company"]
    slug = get_slug(company)
    log.info(f"▶ Starting agent: {company} ({slug})")
    start = time.time()

    cmd = ["claude", "-p", prompt, "--model", "opus"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(PROJECT_ROOT),
            start_new_session=True,
        )

        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
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
            log.error(f"✗ {company}: TIMEOUT after {elapsed:.0f}s (process group killed)")
            return False

        elapsed = time.time() - start

        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            try:
                with open(pending_file) as f:
                    data = json.load(f)
                n_quotes = len(data.get("quotes", []))
                n_sources = len(data.get("sources", []))
                model = data.get("structuralFindings", {}).get("suggestedModel", "?")
                log.info(
                    f"✓ {company}: M{model}, {n_quotes} quotes, "
                    f"{n_sources} sources in {elapsed:.0f}s"
                )
                return True
            except json.JSONDecodeError:
                log.error(f"✗ {company}: Output exists but invalid JSON")
                pending_file.unlink()
                return False
        else:
            stdout_preview = stdout[:500] if stdout else "(empty)"
            stderr_preview = stderr[:300] if stderr else "(empty)"
            log.error(
                f"✗ {company}: No output file after {elapsed:.0f}s "
                f"(exit={proc.returncode})\n"
                f"  stdout: {stdout_preview}\n"
                f"  stderr: {stderr_preview}"
            )
            return False

    except Exception as e:
        log.error(f"✗ {company}: Exception: {e}")
        return False

# ─── Curation Queue ──────────────────────────────────────────────────────────

def append_to_curation_queue(target: dict, slug: str):
    """Append a completed research target to research/queue.json for /curate pickup."""
    try:
        with open(QUEUE_FILE) as f:
            queue_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        queue_data = {
            "description": "Curation queue — research sessions awaiting Phase 2 processing.",
            "lastUpdated": date.today().isoformat(),
            "queue": [],
        }

    pending_path = f"research/pending/{slug}.json"
    today_str = date.today().isoformat()

    entry = {
        "sessionFile": pending_path,
        "sessionDate": today_str,
        "source": f"overnight-research.py — {target['company']} ({target['sector']})",
        "organizationsFound": [slug],
        "status": "pending",
        "curatedIn": None,
    }

    queue_data["queue"].append(entry)
    queue_data["lastUpdated"] = today_str

    save_json(QUEUE_FILE, queue_data)

    log.info(f"  → Added {target['company']} to research/queue.json")


# ─── Target Queue ─────────────────────────────────────────────────────────────

def load_targets(
    quadrant: str | None = None,
    priority: str | None = None,
    company: str | None = None,
) -> list[dict]:
    """Load and filter targets from target-specimens.json."""
    with open(TARGET_LIST) as f:
        data = json.load(f)

    targets = data["targets"]

    # Filter out already-scanned (check pending/ and specimens/)
    filtered = []
    for t in targets:
        slug = get_slug(t["company"])
        pending_file = PENDING_DIR / f"{slug}.json"
        specimen_file = SPECIMENS_DIR / f"{slug}.json"

        if pending_file.exists():
            log.info(f"  Skip {t['company']}: already in pending/")
            continue
        if specimen_file.exists():
            log.info(f"  Skip {t['company']}: specimen already exists")
            continue
        filtered.append(t)

    targets = filtered

    # Apply filters
    if company:
        targets = [t for t in targets if company.lower() in t["company"].lower()]
    if quadrant:
        targets = [t for t in targets if t["quadrant"] == quadrant]
    if priority:
        targets = [t for t in targets if t["priority"] == priority]

    # Sort by priority (high > medium > low), then by quadrant
    priority_order = {"high": 0, "medium": 1, "low": 2}
    targets.sort(key=lambda t: (priority_order.get(t["priority"], 9), t["quadrant"], t["company"]))

    return targets

# ─── Session Log ──────────────────────────────────────────────────────────────

def write_session_log(results: list[dict], start_time: datetime):
    """Write a rich markdown session log with per-company insights from pending files."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()
    elapsed = datetime.now() - start_time

    rows = []
    for r in results:
        status = "✓" if r["success"] else "✗"
        model = r.get("model", "?")
        quotes = r.get("quotes", 0)
        rows.append(
            f"| {r['company']:30s} | {r['quadrant']} | {status} | M{model} | "
            f"{quotes} quotes | {r.get('elapsed', 0):.0f}s |"
        )

    succeeded_results = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]

    # ── Extract rich content from pending files ─────────────────────
    specimen_sections = []
    all_open_questions = []
    model_names = {
        1: "Research Lab", 2: "Center of Excellence", 3: "Embedded Teams",
        4: "Hybrid/Hub-and-Spoke", 5: "Product/Venture Lab",
        6: "Unnamed/Informal", 7: "Tiger Teams", 8: "Skunkworks", 9: "AI-Native",
    }

    for r in succeeded_results:
        slug = get_slug(r["company"])
        pending_file = PENDING_DIR / f"{slug}.json"
        if not pending_file.exists():
            continue
        try:
            with open(pending_file) as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            continue

        findings = data.get("structuralFindings", {})
        model_num = findings.get("suggestedModel", "?")
        model_name = model_names.get(model_num, "Unknown") if isinstance(model_num, int) else "?"
        orientation = findings.get("suggestedOrientation", "?")
        confidence = findings.get("confidence", "?")
        summary = data.get("summary", "").strip()
        rationale = findings.get("rationale", "").strip()
        ai_structure = findings.get("aiTeamStructure", "").strip()
        open_qs = data.get("openQuestions", [])
        key_people = findings.get("keyPeople", [])
        n_sources = len(data.get("sources", []))
        n_quotes = len(data.get("quotes", []))

        botanist_notes = data.get("botanistNotes", [])
        best_quote = data.get("bestQuote", {})
        all_quotes = data.get("quotes", [])

        # Build per-company section
        people_str = ", ".join(
            f"{p.get('name', '?')} ({p.get('title', '?')})"
            for p in key_people[:5]
        ) if key_people else "(none identified)"

        section = f"### {r['company']} — M{model_num} {model_name} | {orientation} | {confidence}\n\n"
        if summary:
            section += f"**Summary:** {summary}\n\n"
        if rationale:
            section += f"**Classification rationale:** {rationale}\n\n"
        if ai_structure:
            # Truncate very long descriptions
            if len(ai_structure) > 500:
                ai_structure = ai_structure[:500] + "..."
            section += f"**AI team structure:** {ai_structure}\n\n"
        section += f"**Key people:** {people_str}\n\n"
        section += f"**Data:** {n_quotes} quotes, {n_sources} sources\n\n"

        # Best quote (most revealing)
        if best_quote and best_quote.get("text"):
            quote_text = best_quote["text"][:150]
            if len(best_quote.get("text", "")) > 150:
                quote_text += "..."
            section += f"**Most revealing quote:** \"{quote_text}\"\n"
            section += f"— {best_quote.get('speaker', '?')}\n"
            if best_quote.get("why"):
                section += f"*Why interesting:* {best_quote['why']}\n"
            section += "\n"
        elif all_quotes:
            # Fall back to first quote if no bestQuote field
            q = all_quotes[0]
            quote_text = q.get("text", "")[:150]
            if len(q.get("text", "")) > 150:
                quote_text += "..."
            section += f"**Notable quote:** \"{quote_text}\" — {q.get('speaker', '?')}\n\n"

        # Botanist's notes
        if botanist_notes:
            section += "**Botanist's notes:**\n"
            for note in botanist_notes:
                if isinstance(note, str) and note.strip():
                    section += f"- {note}\n"
            section += "\n"

        if open_qs:
            section += "**Open questions:**\n"
            for q in open_qs[:5]:
                section += f"- {q}\n"
            section += "\n"

        specimen_sections.append(section)

        for q in open_qs:
            all_open_questions.append(f"- **{r['company']}**: {q}")

    # ── Model distribution ──────────────────────────────────────────
    from collections import Counter
    model_counts = Counter(str(r.get("model", "?")) for r in succeeded_results)
    model_rows = []
    for m, c in sorted(model_counts.items()):
        name = model_names.get(int(m), "Unknown") if m.isdigit() else "Unknown"
        model_rows.append(f"| M{m} {name:30s} | {c:5d} |")

    # ── Sector distribution ─────────────────────────────────────────
    sector_counts = Counter(r.get("quadrant", "?") for r in succeeded_results)
    sector_rows = [f"| {q} | {c} |" for q, c in sorted(sector_counts.items())]

    content = dedent(f"""\
    # Overnight Research Run — {today_str}

    **Started:** {start_time.strftime('%Y-%m-%d %H:%M')}
    **Duration:** {elapsed.total_seconds() / 60:.0f} minutes
    **Targets scanned:** {len(results)}
    **Succeeded:** {len(succeeded_results)}
    **Failed:** {len(failed_results)}
    **Method:** `scripts/overnight-research.py` via `claude -p --model opus`

    ## Results

    | Company | Q | Status | Model | Quotes | Time |
    |---------|---|--------|-------|--------|------|
    {chr(10).join(rows)}

    ## Model Distribution

    | Model | Count |
    |-------|-------|
    {chr(10).join(model_rows) if model_rows else "| (none) | |"}

    ## Quadrant Distribution

    | Quadrant | Count |
    |----------|-------|
    {chr(10).join(sector_rows) if sector_rows else "| (none) | |"}

    ## Per-Company Findings

    {chr(10).join(specimen_sections) if specimen_sections else "(no findings to report)"}

    ## Open Questions Across All Specimens

    {chr(10).join(all_open_questions[:50]) if all_open_questions else "- (none)"}

    ## Failed Targets

    {chr(10).join(f"- {r['company']}" for r in failed_results) if failed_results else "- (none)"}

    ## Next Steps

    - Run `overnight-curate.py` to create specimen files from research findings
    - Run `overnight-purpose-claims.py` for newly created specimens
    - Review open questions above for research gaps
    """)

    log_path = SESSION_DIR / f"{today_str}-overnight-research.md"
    counter = 1
    while log_path.exists():
        counter += 1
        log_path = SESSION_DIR / f"{today_str}-overnight-research-{counter}.md"

    with open(log_path, "w") as f:
        f.write(content)
    log.info(f"Session log: {log_path}")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Overnight research scanning for new specimen targets"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show queue and exit")
    parser.add_argument("--limit", type=int, default=0, help="Max targets to scan")
    parser.add_argument("--company", type=str, help="Scan one specific company")
    parser.add_argument("--quadrant", type=str, choices=["Q1", "Q2", "Q3", "Q4"],
                        help="Scan one quadrant only")
    parser.add_argument("--priority", type=str, choices=["high", "medium", "low"],
                        help="Filter by priority level")
    parser.add_argument("--skip-permissions", action="store_true",
                        help="Add --dangerously-skip-permissions")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("OVERNIGHT RESEARCH RUN")
    log.info("=" * 60)

    # ─── Preflight Checks ─────────────────────────────────────────────
    failures = preflight_check(
        required_files=[TARGET_LIST],
        check_claude_cli=not args.dry_run,
        required_dirs=[PENDING_DIR, SESSION_DIR],
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
            lock_path = acquire_lock("overnight-research")
            log.info("Lock acquired")
        except RuntimeError as e:
            log.error(f"LOCK FAIL: {e}")
            sys.exit(1)

    try:  # ← ensures lock is released even on unexpected exceptions

        # Load and filter queue
        queue = load_targets(
            quadrant=args.quadrant,
            priority=args.priority,
            company=args.company,
        )

        log.info(f"Queue: {len(queue)} targets")

        if args.limit > 0:
            queue = queue[:args.limit]
            log.info(f"Limited to {args.limit}")

        # Dry run
        if args.dry_run:
            log.info("\n--- DRY RUN — Target queue ---")
            for i, t in enumerate(queue, 1):
                conf = " ★" if t.get("conference") else ""
                pub = "PUB" if t.get("public", True) else "PVT"
                log.info(
                    f"  {i:2d}. [{t['priority']:6s}] {t['company']:30s} | "
                    f"{t['quadrant']} | {t['sector']:25s} | {t['leader']:25s} | {pub}{conf}"
                )
            log.info(f"\nTotal: {len(queue)} targets")
            log.info("Run without --dry-run to execute.")
            return

        # ─── Run Loop ─────────────────────────────────────────────────────
        start_time = datetime.now()
        results = []
        failed = []

        for i, target in enumerate(queue, 1):
            log.info(f"\n--- [{i}/{len(queue)}] {target['company']} ({target['quadrant']}) ---")

            prompt = build_research_prompt(target)
            agent_start = time.time()
            success = run_agent(target, prompt, args.skip_permissions)
            agent_elapsed = time.time() - agent_start

            if success:
                slug = get_slug(target["company"])
                pending_file = PENDING_DIR / f"{slug}.json"
                try:
                    with open(pending_file) as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    log.error(f"Cannot read pending file {pending_file}: {e}")
                    results.append({
                        "company": target["company"],
                        "quadrant": target["quadrant"],
                        "success": False,
                        "model": "?",
                        "quotes": 0,
                        "elapsed": agent_elapsed,
                    })
                    failed.append(target)
                    continue
                results.append({
                    "company": target["company"],
                    "quadrant": target["quadrant"],
                    "success": True,
                    "model": data.get("structuralFindings", {}).get("suggestedModel", "?"),
                    "quotes": len(data.get("quotes", [])),
                    "elapsed": agent_elapsed,
                })
                append_to_curation_queue(target, slug)
            else:
                results.append({
                    "company": target["company"],
                    "quadrant": target["quadrant"],
                    "success": False,
                    "model": "?",
                    "quotes": 0,
                    "elapsed": agent_elapsed,
                })
                failed.append(target)

            if i < len(queue):
                time.sleep(PAUSE_BETWEEN)

        # ─── Retry Failed ────────────────────────────────────────────────
        if failed and MAX_RETRIES > 0:
            log.info(f"\n--- RETRYING {len(failed)} failed targets ---")
            for target in failed:
                prompt = build_research_prompt(target)
                agent_start = time.time()
                success = run_agent(target, prompt, args.skip_permissions)
                agent_elapsed = time.time() - agent_start

                if success:
                    slug = get_slug(target["company"])
                    pending_file = PENDING_DIR / f"{slug}.json"
                    try:
                        with open(pending_file) as f:
                            data = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        log.error(f"Cannot read pending file on retry {pending_file}: {e}")
                        continue
                    for r in results:
                        if r["company"] == target["company"]:
                            r["success"] = True
                            r["model"] = data.get("structuralFindings", {}).get("suggestedModel", "?")
                            r["quotes"] = len(data.get("quotes", []))
                            r["elapsed"] += agent_elapsed
                            break
                    append_to_curation_queue(target, slug)

                time.sleep(PAUSE_BETWEEN)

        # ─── Summary ──────────────────────────────────────────────────────
        elapsed_total = datetime.now() - start_time
        succeeded = [r for r in results if r["success"]]
        failed_final = [r for r in results if not r["success"]]

        log.info("\n" + "=" * 60)
        log.info("RUN COMPLETE")
        log.info("=" * 60)
        log.info(f"Duration: {elapsed_total.total_seconds() / 60:.0f} minutes")
        log.info(f"Targets scanned: {len(results)}")
        log.info(f"Succeeded: {len(succeeded)}")
        log.info(f"Failed: {len(failed_final)}")

        if succeeded:
            from collections import Counter
            models = Counter(r["model"] for r in succeeded)
            log.info(f"\nModel distribution:")
            for m, c in models.most_common():
                log.info(f"  M{m}: {c}")

        if failed_final:
            log.info(f"\nFailed: {[r['company'] for r in failed_final]}")

        write_session_log(results, start_time)

        # Audit log
        if succeeded:
            write_changelog("overnight-research.py", [
                f"Scanned {len(succeeded)} targets: {', '.join(r['company'] for r in succeeded)}",
                f"Total quotes found: {sum(r.get('quotes', 0) for r in succeeded)}",
            ])

        log.info("\nPending files in research/pending/ — run /curate to create specimens.")

    finally:
        # ─── Release Lock ─────────────────────────────────────────────────
        if lock_path:
            release_lock(lock_path)
            log.info("Lock released")


if __name__ == "__main__":
    main()
