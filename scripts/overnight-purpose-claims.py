#!/usr/bin/env python3
"""
overnight-purpose-claims.py
===========================
Orchestrates sequential purpose-claims scans via Claude CLI subprocess.
Reads the scan-tracker for unscanned specimens, builds prompts from specimen
JSON files, invokes `claude -p --model opus` for each, merges results into
registry.json between batches.

Usage:
    python3 scripts/overnight-purpose-claims.py                 # Run all unscanned
    python3 scripts/overnight-purpose-claims.py --dry-run       # Show queue, don't run
    python3 scripts/overnight-purpose-claims.py --limit 5       # Only scan 5 specimens
    python3 scripts/overnight-purpose-claims.py --specimen abb  # Scan one specific specimen
    python3 scripts/overnight-purpose-claims.py --skip-permissions  # Add --dangerously-skip-permissions

Run from project root: orgtransformation/
"""

import argparse
import json
import logging
import os
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
    PROJECT_ROOT, BLOCKED_DOMAINS, CLAIM_TYPES,
)

# ─── Configuration ───────────────────────────────────────────────────────────

REGISTRY_PATH = PROJECT_ROOT / "research" / "purpose-claims" / "registry.json"
SCAN_TRACKER_PATH = PROJECT_ROOT / "research" / "purpose-claims" / "scan-tracker.json"
PENDING_DIR = PROJECT_ROOT / "research" / "purpose-claims" / "pending"
ENRICHMENT_DIR = PROJECT_ROOT / "research" / "purpose-claims" / "enrichment"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"
SESSION_DIR = PROJECT_ROOT / "research" / "purpose-claims" / "sessions"

TIMEOUT_SECONDS = 30 * 60   # 30 minutes per agent
PAUSE_BETWEEN = 10           # seconds between agents
MAX_RETRIES = 1              # retry failed specimens once

# ─── Logging ─────────────────────────────────────────────────────────────────

log = setup_logging("overnight-purpose-claims")

# ─── Specimen Context Extraction ─────────────────────────────────────────────

def load_specimen_context(specimen_id: str) -> dict | None:
    """Load a specimen JSON and extract fields needed for the agent prompt."""
    path = SPECIMENS_DIR / f"{specimen_id}.json"
    if not path.exists():
        log.warning(f"No specimen file: {path}")
        return None

    with open(path) as f:
        spec = json.load(f)

    # Extract CEO/leader from quotes
    leader_name = None
    leader_title = None
    existing_quotes = []

    for q in spec.get("quotes", []):
        if q.get("speaker"):
            # Use the first speaker found as the primary leader
            if leader_name is None:
                leader_name = q["speaker"]
                leader_title = q.get("speakerTitle", "")
            existing_quotes.append({
                "text": q.get("text", "")[:150],
                "speaker": q.get("speaker", ""),
                "source": q.get("source", ""),
            })

    # Extract source URLs
    source_urls = []
    for s in spec.get("sources", []):
        if s.get("url"):
            source_urls.append({
                "name": s.get("name", ""),
                "url": s["url"],
                "type": s.get("type", ""),
            })

    return {
        "id": spec["id"],
        "name": spec["name"],
        "industry": spec.get("habitat", {}).get("industry", "Unknown"),
        "structuralModel": spec.get("classification", {}).get("structuralModel"),
        "structuralModelName": spec.get("classification", {}).get("structuralModelName", ""),
        "leader_name": leader_name,
        "leader_title": leader_title,
        "existing_quotes": existing_quotes[:6],  # cap to keep prompt lean
        "source_urls": source_urls[:5],
    }

# ─── Agent Prompt Builder ────────────────────────────────────────────────────

def build_agent_prompt(specimen_id: str, ctx: dict) -> str:
    """Build the full prompt for a Claude CLI purpose-claims agent."""

    org_name = ctx["name"]
    leader_name = ctx["leader_name"] or f"CEO of {org_name}"
    leader_title = ctx["leader_title"] or "CEO"
    model_num = ctx["structuralModel"] or "?"
    model_name = ctx["structuralModelName"] or "Unknown"

    # Format existing quotes
    if ctx["existing_quotes"]:
        quotes_block = "\n".join(
            f'  - "{q["text"]}" — {q["speaker"]} ({q["source"]})'
            for q in ctx["existing_quotes"]
        )
    else:
        quotes_block = "  (none in specimen file — search broadly)"

    # Format source URLs
    if ctx["source_urls"]:
        sources_block = "\n".join(
            f"  - {s['name']}: {s['url']}"
            for s in ctx["source_urls"]
        )
    else:
        sources_block = "  (no URLs in specimen file)"

    output_path = str(PENDING_DIR / f"{specimen_id}.json")
    today = date.today().isoformat()

    prompt = dedent(f"""\
    You are scanning specimen "{specimen_id}" for purpose claims. COMPLETE THIS IN UNDER 25 MINUTES.

    TASK: Search for verbatim purpose claims by leaders at {org_name}, made in the context of AI adaptation.

    ## SPEED RULES — Read These First

    1. **NEVER make parallel WebFetch calls.** Fetch URLs ONE AT A TIME, sequentially. Parallel fetches cause sibling-error cascades where one 403 kills all concurrent fetches.
    2. **One retry max per URL.** If WebFetch fails, try ONE alternative URL. If that fails too, skip and move on. Do NOT retry the same URL.
    3. **One retry max per search.** If WebSearch fails, retry once. If it fails again, note the failure and move on.
    4. **Stop fetching after 6 URLs.** Even if you found more promising links, 6 fetched pages is enough. Prioritize quality over quantity.
    5. **Skip paywalled/blocked domains.** These always 403: {', '.join(BLOCKED_DOMAINS)}. Don't bother fetching them.

    ## Workflow

    1. Run the 5 search queries below using WebSearch (one at a time)
    2. From ALL search results, pick the 4-6 most promising URLs (articles with direct quotes, transcripts, press releases with CEO statements)
    3. Fetch each URL ONE AT A TIME using WebFetch
    4. Mine fetched content for verbatim quotes that qualify as purpose claims
    5. ALSO mine the existing specimen quotes listed below
    6. Write all qualifying claims to the output file

    ## Specimen Context

    - Organization: {org_name}
    - Industry: {ctx["industry"]}
    - CEO/Leader: {leader_name} ({leader_title})
    - Structural model: M{model_num} ({model_name})
    - Key existing quotes:
    {quotes_block}
    - Key sources:
    {sources_block}

    ## Claim Types (6 types, v2.0 taxonomy — classify by what END the claim invokes)

    - utopian: Civilizational transformation, new era. Epochal scale. "What epoch are we in?"
    - teleological: Specific moral/social outcome. Achievable/falsifiable. "What outcome justifies our existence?"
    - higher-calling: Moral duty supersedes profit. Obligation overrides economics. "What obligation overrides economic logic?"
    - identity: Organizational character, values, culture. "Who are we?" Justification terminates in collective identity.
    - survival: Adapt-or-die. Existential threat. Status quo not viable. "What threat demands action?"
    - commercial-success: Business performance, efficiency, growth, customer experience. "How does this improve outcomes?"

    NOT purpose claims (do NOT collect): managerial directives, adoption metrics, staffing facts, market observations, HR mandates.

    ## Quality Filters (all three required)

    1. Verbatim exact words only — no paraphrasing
    2. Made in context of AI adaptation — not generic mission statements
    3. Traceable source with URL — no URL, no claim

    ## Search Queries — Run ALL 5

    1. "{leader_name}" AI purpose OR mission OR vision OR strategy OR transformation
    2. "{leader_name}" AI "north star" OR "we exist" OR "becoming" OR "unlike" OR "different from"
    3. "{org_name}" AI earnings call OR memo OR letter employees OR shareholders
    4. "{leader_name}" AI workforce OR reskilling OR investment OR CapEx OR "long-term"
    5. "{org_name}" "{leader_name}" AI interview OR podcast OR transcript

    ## WebFetch Instructions

    Fetch URLs ONE AT A TIME. After running all searches, prioritize:
    1. **Podcast/interview transcripts** — Leaders speak freely, richest claims
    2. **Earnings call coverage** — CEO prepared remarks with purpose framing
    3. **Long-form press profiles** — Multiple direct quotes (skip news briefs)
    4. **Internal memos (when published)** — Raw purpose language

    Prompt WebFetch with: "Extract all direct quotes attributed to {leader_name} or other {org_name} executives about AI strategy, transformation, workforce, mission, or long-term vision. Include surrounding context."

    ## Output

    Write a JSON file to: {output_path}

    Use this exact structure:
    {{
      "specimenId": "{specimen_id}",
      "scannedDate": "{today}",
      "claimsFound": N,
      "quality": "rich|adequate|none",
      "searchesCompleted": N,
      "urlsFetched": N,
      "searchFailures": ["queries that failed"],
      "fetchFailures": ["URLs that could not be accessed"],
      "claims": [
        {{
          "id": "{specimen_id}--001",
          "specimenId": "{specimen_id}",
          "claimType": "one of 6 types: utopian|teleological|higher-calling|identity|survival|commercial-success",
          "secondaryType": null,
          "text": "EXACT VERBATIM QUOTE",
          "speaker": "full name",
          "speakerTitle": "title",
          "context": "occasion and AI topic",
          "rhetoricalFunction": "what organizational work this claim does",
          "source": "source name",
          "sourceUrl": "URL",
          "sourceType": "Earnings Call | Podcast | Interview | Internal Memo | Shareholder Letter | Press | Speech | Social Media",
          "sourceDate": "YYYY-MM-DD or YYYY-MM",
          "collectedDate": "{today}",
          "transcriptSource": false,
          "taxonomyFlag": null,
          "notes": ""
        }}
      ]
    }}

    Quality ratings: "rich" = 5+ claims, "adequate" = 2-4 claims, "thin" = 1 claim, "none" = 0 claims.

    If no qualifying claims found, write the file with claims: [] and quality: "none". This is still useful data.
    """)

    return prompt

# ─── Agent Runner ─────────────────────────────────────────────────────────────

def run_agent(specimen_id: str, prompt: str, skip_permissions: bool = False) -> bool:
    """Run a single Claude CLI agent. Returns True if pending file was created.

    Uses Popen with process groups so timeout kills the entire process tree
    (claude + any child processes), preventing zombie orphans.
    """
    log.info(f"▶ Starting agent: {specimen_id}")
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
            log.error(f"✗ {specimen_id}: TIMEOUT after {elapsed:.0f}s (process group killed)")
            return False

        elapsed = time.time() - start

        # Check if pending file was created
        pending_file = PENDING_DIR / f"{specimen_id}.json"
        if pending_file.exists():
            # Validate it's parseable JSON
            try:
                with open(pending_file) as f:
                    data = json.load(f)
                claims_count = data.get("claimsFound", len(data.get("claims", [])))
                quality = data.get("quality", "unknown")
                log.info(
                    f"✓ {specimen_id}: {claims_count} claims ({quality}) "
                    f"in {elapsed:.0f}s"
                )
                return True
            except json.JSONDecodeError:
                log.error(f"✗ {specimen_id}: Output file exists but invalid JSON")
                pending_file.unlink()
                return False
        else:
            # Log some stdout/stderr for debugging
            stdout_preview = stdout[:500] if stdout else "(empty)"
            stderr_preview = stderr[:500] if stderr else "(empty)"
            log.error(
                f"✗ {specimen_id}: No output file after {elapsed:.0f}s "
                f"(exit={proc.returncode})\n"
                f"  stdout: {stdout_preview}\n"
                f"  stderr: {stderr_preview}"
            )
            return False

    except Exception as e:
        log.error(f"✗ {specimen_id}: Exception: {e}")
        return False

# ─── Enrichment & Scan Narrative Writers ─────────────────────────────────────

def _write_enrichment_file(specimen_id: str, data: dict, valid_claims: list):
    """Normalize specimenEnrichment and write to enrichment/{specimen-id}.json."""
    ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)
    se = data.get("specimenEnrichment", {})

    # Normalize keyFindings
    key_findings = []
    if isinstance(se.get("keyFindings"), list):
        key_findings = se["keyFindings"]
    elif isinstance(se.get("keyThemes"), list):
        key_findings = se["keyThemes"]
    if isinstance(se.get("rhetoricalProfile"), str):
        key_findings.insert(0, se["rhetoricalProfile"])

    # Normalize rhetoricalPatterns
    rhetorical_patterns = []
    if isinstance(se.get("rhetoricalPatterns"), list):
        rhetorical_patterns = se["rhetoricalPatterns"]
    elif isinstance(se.get("rhetoricalPattern"), str):
        rhetorical_patterns = [se["rhetoricalPattern"]]

    # Compute claimTypeDistribution from valid claims
    dist = {ct: 0 for ct in CLAIM_TYPES}
    for c in valid_claims:
        ct = c.get("claimType", "")
        if ct in dist:
            dist[ct] += 1

    enrichment = {
        "specimenId": specimen_id,
        "scannedDate": data.get("scannedDate", str(date.today())),
        "quality": data.get("quality", "unknown"),
        "claimCount": len(valid_claims),
        "claimTypeDistribution": dist,
        "keyFindings": key_findings,
        "rhetoricalPatterns": rhetorical_patterns,
        "comparativeNotes": se.get("comparativeNotes"),
        "notableAbsences": se.get("notableAbsences") or se.get("notableAbsence"),
        "correctedLeaderInfo": se.get("correctedLeaderInfo"),
        "scanNarrative": data.get("scanNarrative"),
        "searchesCompleted": data.get("searchesCompleted", 0),
        "urlsFetched": data.get("urlsFetched", 0),
        "fetchFailures": data.get("fetchFailures", []),
    }

    out_path = ENRICHMENT_DIR / f"{specimen_id}.json"
    save_json(out_path, enrichment, backup=False)
    log.info(f"  Wrote enrichment: {out_path.name}")


def _write_scan_narrative(specimen_id: str, data: dict, narrative: str):
    """Write scanNarrative as a markdown field journal entry."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    today_str = str(date.today())
    quality = data.get("quality", "unknown")
    claim_count = data.get("claimsFound", 0)

    content = dedent(f"""\
    # Purpose Claims Scan: {specimen_id}

    **Date:** {today_str}
    **Specimen:** [{specimen_id}](/specimens/{specimen_id})
    **Claims found:** {claim_count} ({quality})
    **Track:** purpose-claims

    ---

    {narrative}
    """)

    log_path = SESSION_DIR / f"{today_str}-scan-{specimen_id}.md"
    # Avoid overwriting
    counter = 1
    while log_path.exists():
        counter += 1
        log_path = SESSION_DIR / f"{today_str}-scan-{specimen_id}-{counter}.md"

    with open(log_path, "w") as f:
        f.write(content)
    log.info(f"  Wrote scan narrative: {log_path.name}")


# ─── Merge Logic ──────────────────────────────────────────────────────────────

def merge_pending_into_registry() -> tuple[int, list[str]]:
    """
    Merge all pending/*.json files into registry.json and update scan-tracker.
    Returns (claims_added, list_of_merged_specimen_ids).
    """
    pending_files = sorted(PENDING_DIR.glob("*.json"))
    if not pending_files:
        return 0, []

    # Load registry
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    # Load scan-tracker
    with open(SCAN_TRACKER_PATH) as f:
        tracker = json.load(f)

    existing_ids = {c["id"] for c in registry["claims"]}
    valid_types = set(registry["claimTypes"])
    total_added = 0
    merged_specimens = []

    for pf in pending_files:
        try:
            with open(pf) as f:
                data = json.load(f)
        except json.JSONDecodeError:
            log.error(f"Skipping invalid JSON: {pf}")
            continue

        specimen_id = data.get("specimenId", pf.stem)

        # Validate and filter claims
        valid_claims = []
        for claim in data.get("claims", []):
            claim_id = claim.get("id")
            if not claim_id:
                log.warning(f"Claim missing 'id' field in {specimen_id}, skipping")
                continue
            # Check for duplicate IDs
            if claim_id in existing_ids:
                log.warning(f"Duplicate ID {claim_id}, skipping")
                continue
            # Validate claim type
            if claim.get("claimType") not in valid_types:
                log.warning(
                    f"Invalid claimType '{claim.get('claimType')}' in {claim_id}, skipping"
                )
                continue
            # Clear invalid secondary types
            if claim.get("secondaryType") and claim["secondaryType"] not in valid_types:
                claim["secondaryType"] = None
            valid_claims.append(claim)
            existing_ids.add(claim_id)

        registry["claims"].extend(valid_claims)
        total_added += len(valid_claims)

        # Update scan-tracker
        for spec_entry in tracker["specimens"]:
            if spec_entry["specimenId"] == specimen_id:
                spec_entry["lastScanned"] = str(date.today())
                spec_entry["claimsFound"] = len(valid_claims)
                spec_entry["quality"] = data.get("quality", "unknown")
                break

        merged_specimens.append(specimen_id)
        log.info(f"  Merged {specimen_id}: +{len(valid_claims)} claims")

        # ── Write enrichment file ──
        _write_enrichment_file(specimen_id, data, valid_claims)

        # ── Write scan narrative to field journal ──
        scan_narrative = data.get("scanNarrative")
        if scan_narrative:
            _write_scan_narrative(specimen_id, data, scan_narrative)

        # Move pending file to processed/ BEFORE writing registry.
        # This prevents duplicates on crash: if registry write fails,
        # the pending file is already moved so re-run won't re-merge it.
        processed_dir = PENDING_DIR / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        pf.rename(processed_dir / pf.name)

    # Write updated registry (atomic — crash won't corrupt)
    registry["lastUpdated"] = str(date.today())
    save_json(REGISTRY_PATH, registry)

    # Write updated scan-tracker (atomic)
    tracker["lastUpdated"] = str(date.today())
    save_json(SCAN_TRACKER_PATH, tracker)

    # Audit log
    write_changelog("overnight-purpose-claims.py", [
        f"Merged {len(merged_specimens)} specimens into registry: {', '.join(merged_specimens)}",
        f"Registry now has {len(registry['claims'])} total claims (+{total_added})",
    ])

    log.info(
        f"  Registry: {len(registry['claims'])} total claims "
        f"(+{total_added} this merge)"
    )

    return total_added, merged_specimens

# ─── Session Log ──────────────────────────────────────────────────────────────

def write_session_log(
    results: list[dict],
    total_added: int,
    start_time: datetime,
):
    """Write a rich markdown session log with per-specimen claim analysis."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()
    elapsed = datetime.now() - start_time

    succeeded = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]

    # Build results table
    rows = []
    for r in results:
        status = "✓" if r["success"] else "✗"
        claims = r.get("claims", 0)
        quality = r.get("quality", "failed")
        elapsed_s = r.get("elapsed", 0)
        # Show type breakdown inline
        tb = r.get("type_breakdown", {})
        types_str = ", ".join(f"{t}:{c}" for t, c in sorted(tb.items())) if tb else ""
        rows.append(
            f"| {r['specimen_id']:30s} | {status} | {claims:3d} | {quality:7s} "
            f"| {elapsed_s:5.0f}s | {types_str} |"
        )

    # Aggregate type distribution across all new claims
    from collections import Counter
    agg_types = Counter()
    for r in succeeded:
        for t, c in r.get("type_breakdown", {}).items():
            agg_types[t] += c
    type_rows = []
    for t in ["identity", "commercial-success", "utopian", "survival",
              "teleological", "higher-calling"]:
        if agg_types.get(t, 0) > 0:
            type_rows.append(f"| {t:20s} | {agg_types[t]:5d} |")

    # Per-specimen sections with notable claims
    specimen_sections = []
    for r in succeeded:
        notable = r.get("notable_claims", [])
        if not notable:
            continue
        section = f"### {r['specimen_id']} ({r.get('claims', 0)} claims)\n\n"
        for nc in notable:
            quote_preview = nc["text"][:100] + "..." if len(nc["text"]) > 100 else nc["text"]
            section += f"- **[{nc['claimType']}]** \"{quote_preview}\"\n"
            section += f"  — {nc['speaker']}\n"
            if nc.get("rhetoricalFunction"):
                section += f"  *Rhetorical function:* {nc['rhetoricalFunction']}\n"
            if nc.get("notes"):
                section += f"  *Notes:* {nc['notes']}\n"
            section += "\n"
        specimen_sections.append(section)

    # Richest specimens
    richest = sorted(succeeded, key=lambda r: r.get("claims", 0), reverse=True)[:5]
    richest_rows = [
        f"| {r['specimen_id']:30s} | {r.get('claims', 0):3d} |"
        for r in richest
    ]

    content = dedent(f"""\
    # Overnight Purpose Claims Run — {today_str}

    **Started:** {start_time.strftime('%Y-%m-%d %H:%M')}
    **Duration:** {elapsed.total_seconds() / 60:.0f} minutes
    **Specimens scanned:** {len(results)}
    **Succeeded:** {len(succeeded)} | **Failed:** {len(failed_results)}
    **Total claims added:** {total_added}
    **Method:** `scripts/overnight-purpose-claims.py` via `claude -p --model opus`

    ## Results

    | Specimen                       | St | Claims | Quality | Time  | Type Breakdown |
    |--------------------------------|----|--------|---------|-------|----------------|
    {chr(10).join(rows)}

    ## Type Distribution (this batch: {total_added} claims)

    | Claim Type           | Count |
    |----------------------|-------|
    {chr(10).join(type_rows) if type_rows else "| (none) | |"}

    ## Richest Specimens

    | Specimen                       | Claims |
    |--------------------------------|--------|
    {chr(10).join(richest_rows) if richest_rows else "| (none) | |"}

    ## Notable Claims & Rhetorical Analysis

    {chr(10).join(specimen_sections) if specimen_sections else "(no notable claims captured — check registry for full content)"}

    ## Failed Specimens

    {chr(10).join(f"- {r['specimen_id']}" for r in failed_results) if failed_results else "- (none)"}

    ## Next Steps

    - Review notable claims above for analytical patterns
    - Check registry.json for full type distribution
    - Specimens with 0 claims may need manual transcript discovery
    """)

    log_path = SESSION_DIR / f"{today_str}-overnight-run.md"
    # Avoid overwriting — append number if exists
    counter = 1
    while log_path.exists():
        counter += 1
        log_path = SESSION_DIR / f"{today_str}-overnight-run-{counter}.md"

    with open(log_path, "w") as f:
        f.write(content)

    log.info(f"Session log: {log_path}")

# ─── Priority Queue ──────────────────────────────────────────────────────────

def get_priority_queue() -> list[str]:
    """
    Get unscanned specimens ordered by expected richness.
    Priority: High completeness > Medium > Low, then alphabetical.
    """
    with open(SCAN_TRACKER_PATH) as f:
        tracker = json.load(f)

    unscanned = [
        s["specimenId"]
        for s in tracker["specimens"]
        if s["quality"] == "unscanned"
    ]

    # Score by completeness from specimen files
    scored = []
    for sid in unscanned:
        path = SPECIMENS_DIR / f"{sid}.json"
        score = 0
        if path.exists():
            with open(path) as f:
                spec = json.load(f)
            completeness = spec.get("meta", {}).get("completeness", "Low")
            if completeness == "High":
                score = 3
            elif completeness == "Medium":
                score = 2
            else:
                score = 1
            # Bonus for having quotes (more likely to yield claims)
            if spec.get("quotes"):
                score += 1
            # Bonus for having source URLs
            if any(s.get("url") for s in spec.get("sources", [])):
                score += 1
        scored.append((sid, score))

    # Sort by score descending, then alphabetical
    scored.sort(key=lambda x: (-x[1], x[0]))
    return [s[0] for s in scored]

# ─── Main Orchestration ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Overnight purpose-claims scanning via Claude CLI"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show queue and exit without running agents",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max specimens to scan (0 = all)",
    )
    parser.add_argument(
        "--specimen",
        type=str,
        help="Scan a single specific specimen",
    )
    parser.add_argument(
        "--skip-permissions",
        action="store_true",
        help="Add --dangerously-skip-permissions to claude CLI calls",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Don't merge results into registry (leave in pending/)",
    )
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("OVERNIGHT PURPOSE CLAIMS RUN")
    log.info("=" * 60)

    # ─── Preflight Checks ─────────────────────────────────────────────
    failures = preflight_check(
        required_files=[REGISTRY_PATH, SCAN_TRACKER_PATH],
        check_claude_cli=not args.dry_run,
        required_dirs=[PENDING_DIR, ENRICHMENT_DIR, SESSION_DIR],
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
            lock_path = acquire_lock("overnight-purpose-claims")
            log.info("Lock acquired")
        except RuntimeError as e:
            log.error(f"LOCK FAIL: {e}")
            sys.exit(1)

    # Build queue
    if args.specimen:
        queue = [args.specimen]
        log.info(f"Single specimen mode: {args.specimen}")
    else:
        queue = get_priority_queue()
        log.info(f"Queue: {len(queue)} unscanned specimens")

    if args.limit > 0:
        queue = queue[: args.limit]
        log.info(f"Limited to {args.limit} specimens")

    # Dry run — just show the queue
    if args.dry_run:
        log.info("\n--- DRY RUN — Queue order ---")
        for i, sid in enumerate(queue, 1):
            ctx = load_specimen_context(sid)
            if ctx:
                leader = ctx["leader_name"] or "(no leader found)"
                log.info(
                    f"  {i:2d}. {sid:30s} | {ctx['name']:25s} | "
                    f"{ctx['industry']:20s} | M{ctx['structuralModel']} | {leader}"
                )
            else:
                log.info(f"  {i:2d}. {sid:30s} | NO SPECIMEN FILE")
        log.info(f"\nTotal: {len(queue)} specimens")
        log.info("Run without --dry-run to execute.")
        return

    # ─── Run Loop ─────────────────────────────────────────────────────────
    start_time = datetime.now()
    results = []
    failed = []
    cumulative_claims = 0

    for i, specimen_id in enumerate(queue, 1):
        log.info(f"\n--- [{i}/{len(queue)}] {specimen_id} ---")

        ctx = load_specimen_context(specimen_id)
        if not ctx:
            results.append({
                "specimen_id": specimen_id,
                "success": False,
                "claims": 0,
                "quality": "no-file",
                "elapsed": 0,
            })
            failed.append(specimen_id)
            continue

        prompt = build_agent_prompt(specimen_id, ctx)
        agent_start = time.time()
        success = run_agent(specimen_id, prompt, args.skip_permissions)
        agent_elapsed = time.time() - agent_start

        if success:
            # Read the output to get claim count and rich content
            pending_file = PENDING_DIR / f"{specimen_id}.json"
            with open(pending_file) as f:
                data = json.load(f)
            claims_list = data.get("claims", [])
            # Capture rich content before merge deletes the file
            type_breakdown = {}
            notable_claims = []
            for claim in claims_list:
                ct = claim.get("claimType", "unknown")
                type_breakdown[ct] = type_breakdown.get(ct, 0) + 1
                # Capture claims with interesting rhetorical functions
                rf = claim.get("rhetoricalFunction", "")
                if rf and len(rf) > 20:
                    notable_claims.append({
                        "text": claim.get("text", "")[:120],
                        "speaker": claim.get("speaker", ""),
                        "claimType": ct,
                        "rhetoricalFunction": rf,
                        "notes": claim.get("notes", ""),
                    })
            results.append({
                "specimen_id": specimen_id,
                "success": True,
                "claims": data.get("claimsFound", len(claims_list)),
                "quality": data.get("quality", "unknown"),
                "elapsed": agent_elapsed,
                "type_breakdown": type_breakdown,
                "notable_claims": notable_claims[:5],  # top 5 most interesting
            })
        else:
            results.append({
                "specimen_id": specimen_id,
                "success": False,
                "claims": 0,
                "quality": "failed",
                "elapsed": agent_elapsed,
            })
            failed.append(specimen_id)

        # Merge after every 4 specimens (or at the end)
        if not args.no_merge and (i % 4 == 0 or i == len(queue)):
            added, merged = merge_pending_into_registry()
            cumulative_claims += added
            if merged:
                log.info(f"Merged {len(merged)} specimens (+{added} claims)")

        # Pause between agents
        if i < len(queue):
            time.sleep(PAUSE_BETWEEN)

    # ─── Retry Failed ────────────────────────────────────────────────────
    if failed and MAX_RETRIES > 0:
        log.info(f"\n--- RETRYING {len(failed)} failed specimens ---")
        retry_results = []

        for specimen_id in failed:
            ctx = load_specimen_context(specimen_id)
            if not ctx:
                continue

            prompt = build_agent_prompt(specimen_id, ctx)
            agent_start = time.time()
            success = run_agent(specimen_id, prompt, args.skip_permissions)
            agent_elapsed = time.time() - agent_start

            if success:
                pending_file = PENDING_DIR / f"{specimen_id}.json"
                with open(pending_file) as f:
                    data = json.load(f)
                claims_list = data.get("claims", [])
                # Capture rich content before merge deletes the file
                type_breakdown = {}
                notable_claims = []
                for claim in claims_list:
                    ct = claim.get("claimType", "unknown")
                    type_breakdown[ct] = type_breakdown.get(ct, 0) + 1
                    rf = claim.get("rhetoricalFunction", "")
                    if rf and len(rf) > 20:
                        notable_claims.append({
                            "text": claim.get("text", "")[:120],
                            "speaker": claim.get("speaker", ""),
                            "claimType": ct,
                            "rhetoricalFunction": rf,
                            "notes": claim.get("notes", ""),
                        })
                # Update the result
                for r in results:
                    if r["specimen_id"] == specimen_id:
                        r["success"] = True
                        r["claims"] = data.get("claimsFound", len(claims_list))
                        r["quality"] = data.get("quality", "unknown") + " (retry)"
                        r["elapsed"] += agent_elapsed
                        r["type_breakdown"] = type_breakdown
                        r["notable_claims"] = notable_claims[:5]
                        break

            time.sleep(PAUSE_BETWEEN)

        # Final merge
        if not args.no_merge:
            added, merged = merge_pending_into_registry()
            cumulative_claims += added

    # ─── Summary ──────────────────────────────────────────────────────────
    elapsed_total = datetime.now() - start_time
    succeeded = [r for r in results if r["success"]]
    failed_final = [r for r in results if not r["success"]]

    log.info("\n" + "=" * 60)
    log.info("RUN COMPLETE")
    log.info("=" * 60)
    log.info(f"Duration: {elapsed_total.total_seconds() / 60:.0f} minutes")
    log.info(f"Specimens attempted: {len(results)}")
    log.info(f"Succeeded: {len(succeeded)}")
    log.info(f"Failed: {len(failed_final)}")
    log.info(f"Total claims added: {cumulative_claims}")

    if failed_final:
        log.info(f"Failed specimens: {[r['specimen_id'] for r in failed_final]}")

    # Write session log
    write_session_log(results, cumulative_claims, start_time)

    # Print final type distribution
    if not args.no_merge:
        registry = load_json(REGISTRY_PATH)
        type_counts = Counter(c["claimType"] for c in registry["claims"])
        log.info(f"\nRegistry: {len(registry['claims'])} total claims")
        for t in CLAIM_TYPES:
            log.info(f"  {t}: {type_counts.get(t, 0)}")

    # ─── Release Lock ─────────────────────────────────────────────────
    if lock_path:
        release_lock(lock_path)
        log.info("Lock released")


if __name__ == "__main__":
    main()
