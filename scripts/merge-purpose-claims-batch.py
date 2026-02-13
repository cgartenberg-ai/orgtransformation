#!/usr/bin/env python3
"""
Merge pending purpose claims files into registry.json and update scan-tracker.json.
Batch: uber (16), nike (12), anduril (12), intel-deep (16) = 56 new claims.

Intel note: Registry already has 18 Intel claims (intel--001 to intel--018).
The intel-deep.json has continuation IDs intel--019 to intel--034. No overlap.
"""

import json
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDING_DIR = os.path.join(BASE, "research", "purpose-claims", "pending")
REGISTRY_PATH = os.path.join(BASE, "research", "purpose-claims", "registry.json")
TRACKER_PATH = os.path.join(BASE, "research", "purpose-claims", "scan-tracker.json")

TODAY = date.today().isoformat()

# Files to merge
MERGE_FILES = [
    {"file": "uber.json", "specimenId": "uber"},
    {"file": "nike.json", "specimenId": "nike"},
    {"file": "anduril.json", "specimenId": "anduril"},
    {"file": "intel-deep.json", "specimenId": "intel"},  # continuation of existing
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
        for spec in tracker["specimens"]:
            if spec["specimenId"] == specimen_id:
                if specimen_id == "intel":
                    # Intel: add deep-scan claims to existing count
                    spec["claimsFound"] = spec.get("claimsFound", 0) + len(new_claims)
                    spec["lastScanned"] = TODAY
                    spec["quality"] = "rich"
                    if "note" not in spec:
                        spec["note"] = f"Deep-scan added {len(new_claims)} Lip-Bu Tan claims (total: {spec['claimsFound']})"
                else:
                    spec["lastScanned"] = TODAY
                    spec["claimsFound"] = len(new_claims)
                    spec["quality"] = pending.get("quality", "rich" if len(new_claims) >= 5 else "adequate" if len(new_claims) >= 2 else "thin")
                break

        tracker["lastUpdated"] = TODAY

        status = f"{specimen_id}: {len(new_claims)} claims added"
        if skipped > 0:
            status += f" ({skipped} duplicates skipped)"
        results.append(status)
        print(f"  ✓ {status}")

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
