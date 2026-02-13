#!/usr/bin/env python3
"""Add xAI and SpaceX-xAI to research queue as pending curation."""

import json
from pathlib import Path

QUEUE_PATH = Path(__file__).parent.parent / "research" / "queue.json"

with open(QUEUE_PATH) as f:
    data = json.load(f)

new_entries = [
    {
        "sessionFile": "research/pending/podcast-deep-scan-feb-2026.json",
        "sessionDate": "2026-02-07",
        "source": "Dwarkesh Podcast — Elon Musk (Feb 5, 2026)",
        "organizationsFound": ["xai", "spacex-xai"],
        "status": "pending",
        "curatedIn": None,
        "notes": "xAI: engineering-not-researcher identity, several hundred employees, Grok as Optimus orchestration layer. SpaceX-xAI: $1.25T merger, personal conglomerate model, infrastructure-sharing rationale. Both thin on internal org structure — may need additional research before curating."
    }
]

# Check for duplicates
existing_sessions = {e["sessionFile"] for e in data["queue"]}
added = 0
for entry in new_entries:
    if entry["sessionFile"] not in existing_sessions:
        data["queue"].append(entry)
        added += 1
        print(f"  Added: {entry['organizationsFound']}")
    else:
        print(f"  Skipped (exists): {entry['sessionFile']}")

data["lastUpdated"] = "2026-02-10"

with open(QUEUE_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Added {added} queue entries. Total: {len(data['queue'])}")
