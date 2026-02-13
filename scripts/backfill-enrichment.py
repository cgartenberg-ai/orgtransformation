#!/usr/bin/env python3
"""
Backfill enrichment files from processed agent output + registry claims.

Creates research/purpose-claims/enrichment/{specimen-id}.json for every
scanned specimen. Rich enrichment from 3 processed files (apple, goldman-sachs,
general-motors); minimal enrichment (claimTypeDistribution only) for the rest.

Run once: python3 scripts/backfill-enrichment.py
"""
import json
import os
import glob
from pathlib import Path
from collections import Counter
from datetime import date

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "research" / "purpose-claims" / "pending" / "processed"
ENRICHMENT_DIR = PROJECT_ROOT / "research" / "purpose-claims" / "enrichment"
REGISTRY_PATH = PROJECT_ROOT / "research" / "purpose-claims" / "registry.json"
TRACKER_PATH = PROJECT_ROOT / "research" / "purpose-claims" / "scan-tracker.json"

CLAIM_TYPES = ["utopian", "teleological", "higher-calling", "identity", "survival", "commercial-success"]


def empty_distribution():
    return {ct: 0 for ct in CLAIM_TYPES}


def normalize_enrichment(data: dict) -> dict:
    """Normalize agent output into canonical enrichment schema."""
    specimen_id = data.get("specimenId", "unknown")
    se = data.get("specimenEnrichment", {})

    # Normalize keyFindings
    key_findings = []
    if isinstance(se.get("keyFindings"), list):
        key_findings = se["keyFindings"]
    elif isinstance(se.get("keyThemes"), list):
        key_findings = se["keyThemes"]
    # If there's a rhetoricalProfile string, prepend it
    if isinstance(se.get("rhetoricalProfile"), str):
        key_findings.insert(0, se["rhetoricalProfile"])

    # Normalize rhetoricalPatterns
    rhetorical_patterns = []
    if isinstance(se.get("rhetoricalPatterns"), list):
        rhetorical_patterns = se["rhetoricalPatterns"]
    elif isinstance(se.get("rhetoricalPattern"), str):
        rhetorical_patterns = [se["rhetoricalPattern"]]

    # Compute claimTypeDistribution from claims or use provided
    distribution = empty_distribution()
    if se.get("claimTypeDistribution") and isinstance(se["claimTypeDistribution"], dict):
        for ct in CLAIM_TYPES:
            distribution[ct] = se["claimTypeDistribution"].get(ct, 0)
    else:
        for claim in data.get("claims", []):
            ct = claim.get("claimType", "")
            if ct in distribution:
                distribution[ct] += 1

    return {
        "specimenId": specimen_id,
        "scannedDate": data.get("scannedDate", str(date.today())),
        "quality": data.get("quality", "unknown"),
        "claimCount": data.get("claimsFound", len(data.get("claims", []))),
        "claimTypeDistribution": distribution,
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


def main():
    ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)

    # Load registry for computing distributions for specimens without processed files
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    # Load scan-tracker for scanned dates
    with open(TRACKER_PATH) as f:
        tracker = json.load(f)

    tracker_map = {s["specimenId"]: s for s in tracker["specimens"]}

    # Build per-specimen claim distributions from registry
    registry_distributions = {}
    registry_counts = Counter()
    for claim in registry["claims"]:
        sid = claim["specimenId"]
        ct = claim.get("claimType", "")
        if sid not in registry_distributions:
            registry_distributions[sid] = empty_distribution()
        if ct in registry_distributions[sid]:
            registry_distributions[sid][ct] += 1
        registry_counts[sid] += 1

    # Phase 1: Process files in pending/processed/ (may have rich enrichment)
    processed_specimens = set()
    rich_count = 0
    minimal_count = 0

    for pf in sorted(PROCESSED_DIR.glob("*.json")):
        if pf.is_dir():
            continue
        try:
            with open(pf) as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  SKIP {pf.name}: {e}")
            continue

        specimen_id = data.get("specimenId", pf.stem)
        enrichment = normalize_enrichment(data)

        # If no keyFindings from agent, this is minimal
        has_rich = bool(enrichment["keyFindings"])
        if has_rich:
            rich_count += 1
        else:
            minimal_count += 1

        out_path = ENRICHMENT_DIR / f"{specimen_id}.json"
        with open(out_path, "w") as f:
            json.dump(enrichment, f, indent=2, ensure_ascii=False)

        processed_specimens.add(specimen_id)
        print(f"  {'RICH' if has_rich else 'minimal'} {specimen_id}: {enrichment['claimCount']} claims")

    # Phase 2: Create minimal enrichment for all other scanned specimens
    for spec_entry in tracker["specimens"]:
        sid = spec_entry["specimenId"]
        if sid in processed_specimens:
            continue
        if not spec_entry.get("lastScanned"):
            continue  # unscanned, skip

        dist = registry_distributions.get(sid, empty_distribution())
        count = registry_counts.get(sid, 0)

        enrichment = {
            "specimenId": sid,
            "scannedDate": spec_entry.get("lastScanned", str(date.today())),
            "quality": spec_entry.get("quality", "unknown"),
            "claimCount": count,
            "claimTypeDistribution": dist,
            "keyFindings": [],
            "rhetoricalPatterns": [],
            "comparativeNotes": None,
            "notableAbsences": None,
            "correctedLeaderInfo": None,
            "scanNarrative": None,
            "searchesCompleted": 0,
            "urlsFetched": 0,
            "fetchFailures": [],
        }

        out_path = ENRICHMENT_DIR / f"{sid}.json"
        with open(out_path, "w") as f:
            json.dump(enrichment, f, indent=2, ensure_ascii=False)

        minimal_count += 1
        print(f"  minimal {sid}: {count} claims (from registry)")

    total = rich_count + minimal_count
    print(f"\nDone. {total} enrichment files written ({rich_count} rich, {minimal_count} minimal)")
    print(f"Output: {ENRICHMENT_DIR}")


if __name__ == "__main__":
    main()
