#!/usr/bin/env python3
"""
Merge pending purpose claims files into registry.json, update scan-tracker.json,
and write enrichment files for Batches 13-14.

Batch 13: visa (14), honda (14), panasonic (10), lionsgate (11) = 49 claims.
Theme: Sector gaps — finserv, automotive, Japanese conglomerate, entertainment.

Batch 14: cognizant (16), hp-inc (14), lowes (16), cvs-health (14) = 60 claims.
Theme: High-value analytical specimens — IT services existential question, CEO departure
mid-transformation, retail AI workforce, anti-CAIO thesis.

Total: 109 claims across 8 specimens.
"""

import json
import os
import shutil
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDING_DIR = os.path.join(BASE, "research", "purpose-claims", "pending")
PROCESSED_DIR = os.path.join(PENDING_DIR, "processed")
REGISTRY_PATH = os.path.join(BASE, "research", "purpose-claims", "registry.json")
TRACKER_PATH = os.path.join(BASE, "research", "purpose-claims", "scan-tracker.json")
ENRICHMENT_DIR = os.path.join(BASE, "research", "purpose-claims", "enrichment")

TODAY = date.today().isoformat()

# Files to merge
MERGE_FILES = [
    # Batch 13
    {"file": "visa.json", "specimenId": "visa"},
    {"file": "honda.json", "specimenId": "honda"},
    {"file": "panasonic.json", "specimenId": "panasonic"},
    {"file": "lionsgate.json", "specimenId": "lionsgate"},
    # Batch 14
    {"file": "cognizant.json", "specimenId": "cognizant"},
    {"file": "hp-inc.json", "specimenId": "hp-inc"},
    {"file": "lowes.json", "specimenId": "lowes"},
    {"file": "cvs-health.json", "specimenId": "cvs-health"},
]


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    # Load registry
    registry = load_json(REGISTRY_PATH)
    tracker = load_json(TRACKER_PATH)

    # Track existing claim IDs to prevent duplicates
    existing_ids = {c["id"] for c in registry["claims"]}

    total_added = 0
    results = []

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(ENRICHMENT_DIR, exist_ok=True)

    for entry in MERGE_FILES:
        filepath = os.path.join(PENDING_DIR, entry["file"])
        specimen_id = entry["specimenId"]

        if not os.path.exists(filepath):
            print(f"  SKIP: {entry['file']} not found")
            results.append(f"{specimen_id}: SKIPPED (file not found)")
            continue

        pending = load_json(filepath)
        claims = pending.get("claims", [])

        # Filter out any duplicates
        new_claims = [c for c in claims if c["id"] not in existing_ids]
        skipped = len(claims) - len(new_claims)

        # Add to registry
        registry["claims"].extend(new_claims)
        for c in new_claims:
            existing_ids.add(c["id"])

        total_added += len(new_claims)

        # Update scan-tracker
        found = False
        for spec in tracker["specimens"]:
            if spec["specimenId"] == specimen_id:
                spec["lastScanned"] = TODAY
                spec["claimsFound"] = len(new_claims)
                spec["quality"] = pending.get("quality", "rich" if len(new_claims) >= 5 else "adequate" if len(new_claims) >= 2 else "thin")
                found = True
                break

        if not found:
            tracker["specimens"].append({
                "specimenId": specimen_id,
                "lastScanned": TODAY,
                "claimsFound": len(new_claims),
                "quality": pending.get("quality", "rich" if len(new_claims) >= 5 else "adequate" if len(new_claims) >= 2 else "thin")
            })

        tracker["lastUpdated"] = TODAY

        # Write enrichment file if specimenEnrichment exists
        enrichment = pending.get("specimenEnrichment")
        if enrichment:
            enrichment_data = {
                "specimenId": specimen_id,
                "scannedDate": pending.get("scannedDate", TODAY),
                "claimCount": len(new_claims),
                "searchesCompleted": pending.get("searchesCompleted", 0),
                "urlsFetched": pending.get("urlsFetched", 0),
                "fetchFailures": len(pending.get("fetchFailures", [])),
                **enrichment
            }
            enrichment_path = os.path.join(ENRICHMENT_DIR, f"{specimen_id}.json")
            save_json(enrichment_path, enrichment_data)
            print(f"  ✓ Enrichment file written: {specimen_id}.json")

        # Move pending file to processed
        processed_path = os.path.join(PROCESSED_DIR, entry["file"])
        shutil.move(filepath, processed_path)

        status = f"{specimen_id}: {len(new_claims)} claims added"
        if skipped > 0:
            status += f" ({skipped} duplicates skipped)"
        results.append(status)
        print(f"  ✓ {status}")

    # Update registry lastUpdated
    registry["lastUpdated"] = TODAY

    # Save
    save_json(REGISTRY_PATH, registry)
    save_json(TRACKER_PATH, tracker)

    print(f"\n  TOTAL: {total_added} claims added to registry")
    print(f"  Registry now has {len(registry['claims'])} claims")

    # Summary
    print("\n  Results:")
    for r in results:
        print(f"    {r}")


if __name__ == "__main__":
    main()
