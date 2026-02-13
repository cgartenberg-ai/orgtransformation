#!/usr/bin/env python3
"""Merge 53 purpose claims from Ford, BMW, Honeywell, Toyota into registry.json.
Also update scan-tracker.json and create enrichment files."""

import json
import os
import shutil
from datetime import date

BASE = os.path.join(os.path.dirname(__file__), "..")
REGISTRY_PATH = os.path.join(BASE, "research", "purpose-claims", "registry.json")
TRACKER_PATH = os.path.join(BASE, "research", "purpose-claims", "scan-tracker.json")
ENRICHMENT_DIR = os.path.join(BASE, "research", "purpose-claims", "enrichment")
PENDING_DIR = os.path.join(BASE, "research", "purpose-claims", "pending")

today = date.today().isoformat()

SPECIMENS_TO_MERGE = ["ford", "bmw", "honeywell", "toyota"]


def merge_claims():
    """Merge claims from pending files into registry."""
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    existing_ids = {c["id"] for c in registry["claims"]}
    total_added = 0

    for spec_id in SPECIMENS_TO_MERGE:
        pending_path = os.path.join(PENDING_DIR, f"{spec_id}.json")
        if not os.path.exists(pending_path):
            print(f"  WARNING: {spec_id}.json not found in pending/")
            continue

        with open(pending_path, "r") as f:
            pending = json.load(f)

        claims = pending.get("claims", [])
        added = 0
        for claim in claims:
            if claim["id"] not in existing_ids:
                registry["claims"].append(claim)
                existing_ids.add(claim["id"])
                added += 1

        total_added += added
        print(f"  {spec_id}: merged {added} claims (of {len(claims)} in file)")

    registry["lastUpdated"] = today

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"\nTotal claims in registry: {len(registry['claims'])}")
    return total_added


def update_tracker():
    """Update scan-tracker.json for the 4 specimens."""
    with open(TRACKER_PATH, "r") as f:
        tracker = json.load(f)

    claim_counts = {}
    for spec_id in SPECIMENS_TO_MERGE:
        pending_path = os.path.join(PENDING_DIR, f"{spec_id}.json")
        if os.path.exists(pending_path):
            with open(pending_path, "r") as f:
                pending = json.load(f)
            claim_counts[spec_id] = pending.get("claimsFound", len(pending.get("claims", [])))

    for entry in tracker["specimens"]:
        if entry["specimenId"] in SPECIMENS_TO_MERGE:
            count = claim_counts.get(entry["specimenId"], 0)
            entry["lastScanned"] = today
            entry["claimsFound"] = count
            entry["quality"] = "rich" if count >= 5 else ("adequate" if count >= 2 else ("thin" if count >= 1 else "none"))
            print(f"  {entry['specimenId']}: scanned, {count} claims, quality={entry['quality']}")

    tracker["lastUpdated"] = today

    with open(TRACKER_PATH, "w") as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)


def create_enrichment_files():
    """Extract enrichment data from pending files into enrichment directory."""
    os.makedirs(ENRICHMENT_DIR, exist_ok=True)

    for spec_id in SPECIMENS_TO_MERGE:
        pending_path = os.path.join(PENDING_DIR, f"{spec_id}.json")
        if not os.path.exists(pending_path):
            continue

        with open(pending_path, "r") as f:
            pending = json.load(f)

        enrichment = pending.get("specimenEnrichment", {})
        if not enrichment:
            print(f"  {spec_id}: no enrichment data")
            continue

        # Build enrichment file format
        enrichment_data = {
            "specimenId": spec_id,
            "scannedDate": today,
            "claimCount": pending.get("claimsFound", len(pending.get("claims", []))),
            "quality": "rich" if pending.get("claimsFound", 0) >= 5 else "adequate",
            "searchesCompleted": pending.get("searchesCompleted", None),
            "urlsFetched": pending.get("urlsFetched", None),
            "fetchFailures": pending.get("fetchFailures", []),
            "claimTypeDistribution": enrichment.get("claimTypeDistribution", {}),
            "keyFindings": enrichment.get("keyFindings", []),
            "rhetoricalPatterns": enrichment.get("rhetoricalPatterns", []),
            "comparativeNotes": enrichment.get("comparativeNotes", ""),
            "notableAbsences": enrichment.get("notableAbsences", ""),
            "correctedLeaderInfo": enrichment.get("correctedLeaderInfo", None),
            "scanNarrative": pending.get("scanNarrative", "")
        }

        enrichment_path = os.path.join(ENRICHMENT_DIR, f"{spec_id}.json")
        with open(enrichment_path, "w") as f:
            json.dump(enrichment_data, f, indent=2, ensure_ascii=False)

        print(f"  {spec_id}: enrichment file created")


def main():
    print("Merging claims into registry...")
    total = merge_claims()

    print("\nUpdating scan-tracker...")
    update_tracker()

    print("\nCreating enrichment files...")
    create_enrichment_files()

    print(f"\nDone. {total} new claims merged. Scan tracker and enrichment files updated.")


if __name__ == "__main__":
    main()
