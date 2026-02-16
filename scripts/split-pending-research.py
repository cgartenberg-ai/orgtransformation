#!/usr/bin/env python3
"""
split-pending-research.py
=========================
Splits multi-company research files into single-company files that the
curation pipeline can consume. Runs between Phase 1 (research) and
Phase 2 (curate) in the overnight pipeline.

Research agents produce several output formats:
  - Earnings: organizations[] array with per-company findings
  - Press-keyword: findings[] array with per-company entries
  - Specimen-targeted: organizations[] array (often single-company)
  - Staleness/podcast/substack: source-level, not company-level

This script normalizes all company-level data into single-company files
with a top-level "company" field that overnight-curate.py expects.

Also harvests newSpecimenCandidates from sweep files.

Usage:
    python3 scripts/split-pending-research.py              # Split all pending
    python3 scripts/split-pending-research.py --dry-run    # Show what would split
"""

import argparse
import json
import logging
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import save_json, load_json, setup_logging, PROJECT_ROOT

# ─── Configuration ───────────────────────────────────────────────────────────

PENDING_DIR = PROJECT_ROOT / "research" / "pending"
PROCESSED_DIR = PENDING_DIR / "processed"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"
TARGET_SPECIMENS = PROJECT_ROOT / "research" / "target-specimens.json"

log = setup_logging("split-pending")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_slug(company: str) -> str:
    """Generate a filesystem-safe slug from company name."""
    slug = company.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
    return "".join(c for c in slug if c.isalnum() or c == "-")


def has_company_field(data: dict) -> bool:
    """Check if file already has a top-level 'company' field (curate-ready)."""
    return "company" in data


def detect_format(data: dict) -> str:
    """Detect the research output format."""
    if has_company_field(data):
        return "single-company"
    if "organizations" in data:
        return "organizations"
    if "findings" in data and isinstance(data["findings"], list):
        # Press-keyword format
        if any(isinstance(f, dict) and "company" in f for f in data["findings"]):
            return "press-keyword"
    if data.get("mode") == "source-staleness-audit":
        return "staleness-audit"
    if data.get("mode") in ("podcast-feed-check", "substacks", "enterprise-reports"):
        return "source-scan"
    return "unknown"


# ─── Splitters ───────────────────────────────────────────────────────────────

def split_organizations(data: dict, source_file: str) -> list[dict]:
    """Split organizations[] array into single-company files."""
    results = []
    for org in data.get("organizations", []):
        name = (org.get("name") or org.get("company") or "").strip()
        if not name:
            continue

        # Strip parenthetical suffixes like "xAI (post-restructuring Feb 2026)"
        clean_name = name.split("(")[0].strip() if "(" in name else name
        slug = get_slug(clean_name)

        # Check for existing specimen to use its ID (field may be named either way)
        # Note: existingSpecimen can be boolean True (just a flag) — only use if string
        existing_id = org.get("existingSpecimenId") or org.get("existingSpecimen")
        if existing_id and isinstance(existing_id, str):
            slug = existing_id

        single = {
            "company": clean_name,
            "sector": org.get("industry", data.get("sourceScanned", {}).get("type", "Unknown")),
            "scannedDate": data.get("scannedDate", date.today().isoformat()),
            "mode": data.get("taskType", data.get("mode", "research")),
            "_splitFrom": source_file,
            "structuralFindings": {},
            "quotes": [],
            "sources": [],
            "botanistNotes": [],
        }

        # Extract findings (field may be "findings" or "observations")
        findings_list = org.get("findings", org.get("observations", []))
        for finding in findings_list:
            cat = finding.get("category", finding.get("type", "general"))
            title = finding.get("title", "")
            detail = finding.get("detail", finding.get("observation", ""))
            single["structuralFindings"][cat] = f"{title}: {detail}" if title else detail

            # Extract sources from finding
            for src in finding.get("sources", []):
                single["sources"].append(src)

        # Extract quotes
        for q in org.get("quotes", org.get("keyQuotes", [])):
            single["quotes"].append(q)

        # Extract botanist notes
        for note in org.get("botanistNotes", []):
            if isinstance(note, str):
                single["botanistNotes"].append(note)
            elif isinstance(note, dict):
                single["botanistNotes"].append(note.get("note", str(note)))

        # Summary
        single["summary"] = org.get("summary", "")

        results.append({"slug": slug, "data": single})

    return results


def split_press_findings(data: dict, source_file: str) -> list[dict]:
    """Split press-keyword findings[] into single-company files."""
    # Group findings by company
    by_company: dict[str, list] = {}
    for finding in data.get("findings", []):
        company = finding.get("company", "").strip()
        if not company:
            continue
        by_company.setdefault(company, []).append(finding)

    results = []
    for company, findings in by_company.items():
        slug = get_slug(company)
        single = {
            "company": company,
            "sector": data.get("keyword", "press"),
            "scannedDate": data.get("scannedDate", date.today().isoformat()),
            "mode": "press-keyword",
            "_splitFrom": source_file,
            "structuralFindings": {},
            "quotes": [],
            "sources": [],
            "botanistNotes": [],
            "summary": "",
        }

        summaries = []
        for f in findings:
            finding_text = f.get("finding", "")
            relevance = f.get("structuralRelevance", "medium")
            summaries.append(finding_text)

            # Key people
            for kp in f.get("keyPeople", []):
                single["botanistNotes"].append(
                    f"Key person: {kp.get('name', '?')} ({kp.get('title', '?')})"
                )

            # Quotes
            for q in f.get("quotes", []):
                single["quotes"].append(q)

            # Source
            if f.get("sourceUrl"):
                single["sources"].append({
                    "url": f["sourceUrl"],
                    "date": f.get("sourceDate", ""),
                    "type": "Press",
                    "name": f"Press: {finding_text[:60]}",
                })

            single["structuralFindings"][relevance] = finding_text

        single["summary"] = "; ".join(summaries)
        results.append({"slug": slug, "data": single})

    return results


def harvest_candidates(data: dict) -> list[str]:
    """Extract newSpecimenCandidates from a research file."""
    candidates = data.get("newSpecimenCandidates", [])
    if isinstance(candidates, list):
        return [c.strip() for c in candidates if isinstance(c, str) and c.strip()]
    return []


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Split multi-company research into single-company files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be split")
    args = parser.parse_args()

    if not PENDING_DIR.exists():
        log.info("No pending directory — nothing to split")
        return

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    all_candidates = []
    split_count = 0
    skipped = 0
    already_single = 0

    for filepath in sorted(PENDING_DIR.glob("*.json")):
        try:
            data = load_json(filepath)
        except Exception as e:
            log.error(f"Cannot parse {filepath.name}: {e}")
            continue

        fmt = detect_format(data)

        if fmt == "single-company":
            already_single += 1
            continue

        if fmt == "organizations":
            splits = split_organizations(data, filepath.name)
        elif fmt == "press-keyword":
            splits = split_press_findings(data, filepath.name)
        elif fmt in ("staleness-audit", "source-scan", "unknown"):
            # These are source-level, not company-level — harvest candidates only
            all_candidates.extend(harvest_candidates(data))
            skipped += 1
            continue
        else:
            skipped += 1
            continue

        # Harvest candidates from this file too
        all_candidates.extend(harvest_candidates(data))

        if not splits:
            log.info(f"  {filepath.name}: {fmt} format but no companies to split")
            skipped += 1
            continue

        if args.dry_run:
            log.info(f"  {filepath.name} ({fmt}) → {len(splits)} companies:")
            for s in splits:
                exists = "UPDATE" if (SPECIMENS_DIR / f"{s['slug']}.json").exists() else "NEW"
                log.info(f"    {s['slug']:40s} [{exists}]")
            split_count += len(splits)
            continue

        # Write split files
        for s in splits:
            out_path = PENDING_DIR / f"{s['slug']}.json"
            if out_path.exists():
                # Merge: append findings to existing single-company file
                try:
                    existing = load_json(out_path)
                    if "company" in existing:
                        # Append new quotes, sources, botanist notes
                        existing.setdefault("quotes", []).extend(s["data"].get("quotes", []))
                        existing.setdefault("sources", []).extend(s["data"].get("sources", []))
                        existing.setdefault("botanistNotes", []).extend(s["data"].get("botanistNotes", []))
                        for k, v in s["data"].get("structuralFindings", {}).items():
                            existing.setdefault("structuralFindings", {})[k] = v
                        save_json(out_path, existing)
                        log.info(f"  Merged into existing: {s['slug']}")
                        split_count += 1
                        continue
                except Exception:
                    pass  # Fall through to overwrite

            save_json(out_path, s["data"])
            log.info(f"  Created: {s['slug']}.json")
            split_count += 1

        # Move original multi-company file to processed/
        dest = PROCESSED_DIR / filepath.name
        shutil.move(str(filepath), str(dest))
        log.info(f"  Moved {filepath.name} → processed/")

    # ─── Report ──────────────────────────────────────────────────────
    log.info(f"\nSplit complete: {split_count} single-company files created, "
             f"{already_single} already single-company, {skipped} skipped (source-level)")

    # ─── Harvest new specimen candidates ─────────────────────────────
    if all_candidates:
        unique = sorted(set(all_candidates))
        log.info(f"\nNew specimen candidates harvested: {len(unique)}")
        for c in unique:
            log.info(f"  - {c}")

        if not args.dry_run and TARGET_SPECIMENS.exists():
            try:
                targets = load_json(TARGET_SPECIMENS)
                existing_names = {t.get("company", "").lower() for t in targets.get("targets", [])}
                new_targets = []
                for c in unique:
                    if c.lower() not in existing_names:
                        new_targets.append({
                            "company": c,
                            "priority": "medium",
                            "source": "auto-harvested",
                            "addedDate": date.today().isoformat(),
                        })
                if new_targets:
                    targets.setdefault("targets", []).extend(new_targets)
                    targets["lastUpdated"] = date.today().isoformat()
                    save_json(TARGET_SPECIMENS, targets)
                    log.info(f"  Added {len(new_targets)} to target-specimens.json")
            except Exception as e:
                log.warning(f"  Could not update target-specimens.json: {e}")


if __name__ == "__main__":
    main()
