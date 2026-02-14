#!/usr/bin/env python3
"""
M4 Taxonomy Audit — Registry + Synthesis Queue Update

Reads all specimen files, rebuilds registry.json entries for reclassified specimens,
and adds reclassified specimens to the synthesis queue.
"""

import json
import os
from datetime import date

TODAY = date.today().isoformat()
SPECIMENS_DIR = "specimens"
REGISTRY_PATH = "specimens/registry.json"
SYNTH_QUEUE_PATH = "curation/synthesis-queue.json"

RECLASSIFIED_IDS = [
    "amazon-agi", "meta-ai", "nvidia", "bosch-bcai", "google-ai-infra",
    "wells-fargo", "pentagon-cdao", "sap", "cvs-health", "kaiser-permanente",
    "apple", "salesforce", "servicenow",
    "mckinsey", "accenture-openai", "netflix", "uber", "nike", "fedex",
]

MODEL_NAMES = {
    1: "Research Lab", 2: "CoE", 3: "Embedded", 4: "Hub-and-Spoke",
    5: "Product/Venture", 6: "Unnamed/Informal", 7: "Tiger Teams",
    8: "Skunkworks", 9: "AI-Native",
}


def update_registry():
    """Update registry.json entries for reclassified specimens."""
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    updated = 0
    for entry in registry["specimens"]:
        if entry["id"] in RECLASSIFIED_IDS:
            # Read the actual specimen file
            fpath = os.path.join(SPECIMENS_DIR, f"{entry['id']}.json")
            with open(fpath, "r") as f:
                spec = json.load(f)

            cls = spec["classification"]
            old_model = entry["structuralModel"]
            new_model = cls["structuralModel"]

            entry["structuralModel"] = cls["structuralModel"]
            entry["subType"] = cls.get("subType")
            entry["secondaryModel"] = cls.get("secondaryModel")
            entry["orientation"] = cls.get("orientation", cls.get("orientationName"))
            entry["confidence"] = cls.get("confidence")
            entry["lastUpdated"] = spec["meta"]["lastUpdated"]
            entry["layerCount"] = len(spec.get("layers", []))

            sec = f"+M{cls['secondaryModel']}" if cls.get('secondaryModel') else ""
            print(f"  ✓ {entry['id']}: M{old_model} → M{new_model}{sec}")
            updated += 1

    # Recalculate aggregates
    from collections import Counter
    model_counts = Counter()
    orient_counts = Counter()
    for s in registry["specimens"]:
        m = s.get("structuralModel")
        if m is not None:
            model_counts[m] += 1
        o = s.get("orientation")
        if o:
            orient_counts[o] += 1

    registry["totalSpecimens"] = len(registry["specimens"])
    registry["byModel"] = {f"M{k}": v for k, v in sorted(model_counts.items())}
    registry["byOrientation"] = dict(sorted(orient_counts.items()))
    registry["lastUpdated"] = TODAY

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nRegistry updated: {updated} entries modified")
    print(f"\nNew distribution:")
    total = registry["totalSpecimens"]
    for m in sorted(model_counts.keys()):
        name = MODEL_NAMES.get(m, f"M{m}")
        cnt = model_counts[m]
        print(f"  M{m} {name:25s} {cnt:3d}  ({100*cnt/total:.0f}%)")


def update_synthesis_queue():
    """Add reclassified specimens to synthesis queue."""
    with open(SYNTH_QUEUE_PATH, "r") as f:
        queue = json.load(f)

    existing_ids = {e["specimenId"] for e in queue.get("specimens", []) if e.get("status") == "pending"}

    added = 0
    for sid in RECLASSIFIED_IDS:
        if sid not in existing_ids:
            queue["specimens"].append({
                "specimenId": sid,
                "addedDate": TODAY,
                "reason": "Reclassified in M4 taxonomy audit",
                "curatedIn": "m4-taxonomy-audit-2026-02-12",
                "status": "pending",
            })
            added += 1

    queue["lastUpdated"] = TODAY

    with open(SYNTH_QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nSynthesis queue: {added} specimens added as pending")


if __name__ == "__main__":
    print("Updating registry.json...")
    update_registry()
    print("\nUpdating synthesis queue...")
    update_synthesis_queue()
