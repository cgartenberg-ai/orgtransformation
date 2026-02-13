#!/usr/bin/env python3
"""
split-multi-company.py
======================
Splits multi-company research files into individual single-company files
in the format expected by overnight-curate.py.

Handles three source formats:
  1. Earnings files: companies[] with {id, ticker, specimenSlug, observations, quotes}
  2. Deep scans:     organizations[] with {id, name, observations, sources, quotes}
  3. General sweeps: organizations[] with {id, name, observations, quotes}

Output format matches overnight-research.py output:
  {company, ticker, sector, scannedDate, structuralFindings, quotes, sources, summary, openQuestions}

Usage:
    python3 scripts/split-multi-company.py                 # Split all multi-company files
    python3 scripts/split-multi-company.py --dry-run       # Show what would be split
    python3 scripts/split-multi-company.py --file X.json   # Split one specific file
    python3 scripts/split-multi-company.py --min-quotes 1  # Only split entries with 1+ quotes

Run from project root: orgtransformation/
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PENDING_DIR = PROJECT_ROOT / "research" / "pending"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"

# Files known to have no per-company structured data
SKIP_FILES = {"podcast-deep-scan-feb-2026.json", "podcast-substack-feed-check.json"}

# Minimum observations to be worth splitting (very thin entries waste curate time)
DEFAULT_MIN_OBS = 2


def get_existing_specimens() -> set[str]:
    """Get set of existing specimen slugs."""
    existing = set()
    excluded = {"registry.json", "_template.json", "specimen-schema.json", "source-registry.json"}
    for f in SPECIMENS_DIR.iterdir():
        if f.name.endswith(".json") and f.name not in excluded:
            existing.add(f.stem)
    return existing


def normalize_quote(q: dict, source_file: str) -> dict:
    """Normalize a quote to the overnight-research format."""
    # Handle "speaker": "Jamie Dimon, CEO" format (earnings)
    speaker = q.get("speaker", "")
    speaker_title = q.get("speakerTitle", "")
    if not speaker_title and ", " in speaker:
        parts = speaker.split(", ", 1)
        speaker = parts[0]
        speaker_title = parts[1]

    return {
        "text": q.get("text", ""),
        "speaker": speaker,
        "speakerTitle": speaker_title or None,
        "source": q.get("source", source_file),
        "sourceUrl": q.get("sourceUrl", ""),
        "sourceDate": q.get("sourceDate", q.get("date", "")),
        "context": q.get("context", ""),
    }


def normalize_source(s: dict) -> dict:
    """Normalize a source to the overnight-research format."""
    # Map deep-scan source types to standard types
    type_map = {
        "press-interview": "Press",
        "press": "Press",
        "earnings-call": "Earnings Call",
        "earnings": "Earnings Call",
        "blog": "Blog",
        "report": "Report",
        "podcast": "Podcast",
        "interview": "Interview",
    }
    raw_type = s.get("type", "Other")
    normalized_type = type_map.get(raw_type.lower(), raw_type)

    return {
        "name": s.get("name", ""),
        "url": s.get("url", ""),
        "type": normalized_type,
        "date": s.get("date", s.get("sourceDate", "")),
        "notes": s.get("notes", s.get("quality", "")),
    }


def build_summary_from_observations(observations: list[dict]) -> str:
    """Build a summary paragraph from observation titles and details."""
    if not observations:
        return ""
    parts = []
    for obs in observations[:4]:  # Top 4 observations
        title = obs.get("title", "")
        detail = obs.get("detail", "")
        if title and detail:
            parts.append(f"{title}: {detail[:200]}")
        elif detail:
            parts.append(detail[:250])
        elif title:
            parts.append(title)
    return " ".join(parts)


def build_structural_findings(observations: list[dict], existing_specimen: dict | None) -> dict:
    """Build structuralFindings from observations, inheriting model from existing specimen if available."""
    model = None
    model_name = None
    orientation = None
    confidence = "Low"

    if existing_specimen:
        cls = existing_specimen.get("classification", {})
        model = cls.get("structuralModel")
        model_name = cls.get("structuralModelName")
        orientation = cls.get("orientation")
        confidence = cls.get("confidence", "Low")

    # Extract key people from observations
    key_people = []
    ai_structure = ""
    for obs in observations:
        detail = obs.get("detail", "")
        # Look for named roles
        if any(term in detail.lower() for term in ["cdo", "caio", "cto", "cio", "chief", "head of ai", "vp of ai"]):
            ai_structure += detail[:200] + " "

    return {
        "suggestedModel": model,
        "suggestedModelName": model_name,
        "suggestedOrientation": orientation,
        "confidence": confidence,
        "rationale": "Based on existing specimen classification. New observations from earnings/research session.",
        "aiTeamStructure": ai_structure.strip() or None,
        "keyPeople": key_people or None,
        "investmentSignals": None,
        "observableMarkers": {},
    }


def extract_sources_from_observations(observations: list[dict]) -> list[dict]:
    """Extract unique sources from observation sourceUrl fields."""
    seen_urls = set()
    sources = []
    for obs in observations:
        url = obs.get("sourceUrl", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            sources.append({
                "name": obs.get("sourceName", obs.get("title", "Research source")),
                "url": url,
                "type": "Earnings Call" if "earnings" in url.lower() else "Press",
                "date": obs.get("sourceDate", ""),
                "notes": obs.get("title", ""),
            })
    return sources


def split_earnings_file(data: dict, source_filename: str) -> list[dict]:
    """Split an earnings file (companies[] format) into single-company files."""
    results = []
    scanned_date = data.get("scannedDate", date.today().isoformat())

    for company in data.get("companies", []):
        slug = company.get("specimenSlug") or company.get("id") or ""
        if not slug:
            continue

        observations = company.get("observations", [])
        quotes = company.get("quotes", [])
        key_findings = company.get("keyFindings", [])

        # Build sources from observation URLs
        sources = extract_sources_from_observations(observations)

        # Build open questions from key findings if present
        open_questions = []
        if isinstance(key_findings, list):
            for kf in key_findings:
                if isinstance(kf, str) and "?" in kf:
                    open_questions.append(kf)

        existing = load_existing_specimen(slug)

        result = {
            "company": existing.get("name", slug.replace("-", " ").title()) if existing else slug.replace("-", " ").title(),
            "ticker": company.get("ticker"),
            "sector": existing.get("habitat", {}).get("industry", "") if existing else "",
            "scannedDate": scanned_date,
            "searchesCompleted": 0,
            "urlsFetched": len(sources),
            "fetchFailures": [],
            "structuralFindings": build_structural_findings(observations, existing),
            "quotes": [normalize_quote(q, source_filename) for q in quotes],
            "sources": sources,
            "summary": build_summary_from_observations(observations),
            "openQuestions": open_questions,
            "splitFrom": source_filename,
        }
        results.append((slug, result))

    return results


def split_deep_scan_file(data: dict, source_filename: str) -> list[dict]:
    """Split a deep scan file (organizations[] format with sources) into single-company files."""
    results = []
    scanned_date = data.get("scannedDate", date.today().isoformat())

    for org in data.get("organizations", []):
        slug = org.get("specimenSlug") or org.get("id") or ""
        if not slug:
            continue

        observations = org.get("observations", [])
        quotes = org.get("quotes", [])
        raw_sources = org.get("sources", [])
        open_questions = org.get("openQuestions", [])

        # Deep scans have proper source objects
        if raw_sources:
            sources = [normalize_source(s) for s in raw_sources]
        else:
            sources = extract_sources_from_observations(observations)

        existing = load_existing_specimen(slug)

        result = {
            "company": org.get("name") or (existing.get("name") if existing else slug.replace("-", " ").title()),
            "ticker": None,
            "sector": existing.get("habitat", {}).get("industry", "") if existing else "",
            "scannedDate": scanned_date,
            "searchesCompleted": data.get("searchesCompleted", 0),
            "urlsFetched": data.get("urlsFetched", len(sources)),
            "fetchFailures": data.get("fetchFailures", []),
            "structuralFindings": build_structural_findings(observations, existing),
            "quotes": [normalize_quote(q, source_filename) for q in quotes],
            "sources": sources,
            "summary": build_summary_from_observations(observations),
            "openQuestions": open_questions if isinstance(open_questions, list) else [],
            "splitFrom": source_filename,
        }
        results.append((slug, result))

    return results


def load_existing_specimen(slug: str) -> dict | None:
    """Load existing specimen for inheriting metadata."""
    path = SPECIMENS_DIR / f"{slug}.json"
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def detect_format(data: dict) -> str:
    """Detect which format a multi-company file uses."""
    if "companies" in data:
        return "earnings"
    if "organizations" in data:
        # Deep scans have sources per org; sweeps don't
        orgs = data["organizations"]
        if orgs and "sources" in orgs[0]:
            return "deep-scan"
        return "sweep"
    return "unknown"


def split_file(filepath: Path, min_obs: int, min_quotes: int) -> list[tuple[str, dict]]:
    """Split a multi-company file into (slug, data) pairs."""
    with open(filepath) as f:
        data = json.load(f)

    # Skip single-company files
    if "company" in data:
        return []

    fmt = detect_format(data)
    source_filename = filepath.name

    if fmt == "earnings":
        results = split_earnings_file(data, source_filename)
    elif fmt in ("deep-scan", "sweep"):
        results = split_deep_scan_file(data, source_filename)
    else:
        return []

    # Filter by minimum content thresholds
    filtered = []
    for slug, result in results:
        n_obs = len(result.get("summary", "").split(": "))  # rough count
        n_quotes = len(result.get("quotes", []))
        # Use observations from original data for threshold check
        if n_quotes >= min_quotes or len(result.get("sources", [])) >= min_obs:
            filtered.append((slug, result))

    return filtered


def main():
    parser = argparse.ArgumentParser(description="Split multi-company research files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be split")
    parser.add_argument("--file", type=str, help="Split one specific file")
    parser.add_argument("--min-quotes", type=int, default=0, help="Min quotes to include (default: 0)")
    parser.add_argument("--min-obs", type=int, default=DEFAULT_MIN_OBS, help=f"Min observations/sources to include (default: {DEFAULT_MIN_OBS})")
    args = parser.parse_args()

    existing_specimens = get_existing_specimens()

    # Build list of files to process
    if args.file:
        files = [PENDING_DIR / args.file]
    else:
        files = sorted(
            f for f in PENDING_DIR.iterdir()
            if f.name.endswith(".json") and f.name not in SKIP_FILES
        )

    total_split = 0
    total_new = 0
    total_update = 0
    total_skipped = 0

    for filepath in files:
        with open(filepath) as f:
            data = json.load(f)

        # Skip single-company files
        if "company" in data:
            continue

        fmt = detect_format(data)
        if fmt == "unknown":
            continue

        results = split_file(filepath, args.min_obs, args.min_quotes)
        if not results:
            continue

        print(f"\n{filepath.name} ({fmt}, {len(results)} entries):")

        for slug, result in results:
            is_new = slug not in existing_specimens
            action = "NEW" if is_new else "ADD LAYER"
            n_quotes = len(result.get("quotes", []))
            n_sources = len(result.get("sources", []))

            output_path = PENDING_DIR / f"{slug}.json"
            exists_already = output_path.exists()

            if exists_already:
                # Don't overwrite existing single-company file
                print(f"  SKIP {slug:30s} | already has pending file")
                total_skipped += 1
                continue

            print(f"  {action:9s} {slug:30s} | {n_quotes:2d} quotes | {n_sources:2d} sources")

            if not args.dry_run:
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2)
                    f.write("\n")

            total_split += 1
            if is_new:
                total_new += 1
            else:
                total_update += 1

    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Summary:")
    print(f"  Split: {total_split} entries ({total_new} new, {total_update} updates)")
    print(f"  Skipped: {total_skipped} (already have pending files)")


if __name__ == "__main__":
    main()
