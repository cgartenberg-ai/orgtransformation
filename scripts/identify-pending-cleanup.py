#!/usr/bin/env python3
"""
Identify which files in research/pending/ are:
- Group A: Large research agent outputs (keep for reference)
- Group B: Curation artifacts already merged into specimens/ (safe to delete)
"""

import json
from pathlib import Path

PENDING = Path(__file__).parent.parent / "research" / "pending"
SPECIMENS = Path(__file__).parent.parent / "specimens"

# Group A files to KEEP (the 10 large research agent outputs + the finserv experiment)
GROUP_A_KEEP = {
    "goldman-sachs-deep-scan.json",
    "morgan-stanley-deep-scan.json",
    "financial-services-earnings-q4-2025.json",
    "pharma-earnings-q4-2025.json",
    "podcast-deep-scan-feb-2026.json",
    "podcast-substack-feed-check.json",
    "earnings-q4-2025-amazon-google.json",
    "earnings-discovery-q4-2025.json",
    "general-sweep-feb-2026.json",
    "general-sweep-feb-2026-v2.json",
    "finserv-natural-experiment.json",  # from our research agent
}

group_b_delete = []
group_a_keep = []
unknown = []

for f in sorted(PENDING.iterdir()):
    if f.name.startswith('.'):
        continue
    if not f.name.endswith('.json'):
        continue

    if f.name in GROUP_A_KEEP:
        group_a_keep.append(f.name)
        continue

    # Check if this file's name matches a specimen
    specimen_path = SPECIMENS / f.name
    if specimen_path.exists():
        group_b_delete.append(f.name)
    else:
        # Also check without .json extension as specimen ID
        stem = f.stem
        # Look for any specimen with this stem
        matches = list(SPECIMENS.glob(f"{stem}*.json"))
        if matches:
            group_b_delete.append(f.name)
        else:
            unknown.append(f.name)

print("=" * 60)
print(f"GROUP A (KEEP - research outputs): {len(group_a_keep)}")
for f in group_a_keep:
    print(f"  ✓ {f}")

print(f"\nGROUP B (DELETE - already in specimens/): {len(group_b_delete)}")
for f in group_b_delete:
    print(f"  ✗ {f}")

print(f"\nUNKNOWN (investigate): {len(unknown)}")
for f in unknown:
    print(f"  ? {f}")

print(f"\n{'=' * 60}")
print(f"Summary: {len(group_a_keep)} keep, {len(group_b_delete)} delete, {len(unknown)} unknown")

# Check for new specimens in pending that DON'T have matches
# (these might be new specimens we want to create)
if unknown:
    print("\nChecking unknown files for potential new specimens...")
    for f in unknown:
        path = PENDING / f
        try:
            with open(path) as fh:
                data = json.load(fh)
            # Check if it looks like a specimen (has classification)
            if "classification" in data:
                print(f"  {f}: looks like a specimen (has classification)")
            elif "organizations" in data or "structuralFindings" in data:
                print(f"  {f}: looks like research output")
            else:
                keys = list(data.keys())[:5]
                print(f"  {f}: keys = {keys}")
        except:
            print(f"  {f}: could not parse")
