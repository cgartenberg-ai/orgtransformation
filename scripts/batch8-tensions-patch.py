#!/usr/bin/env python3
"""Batch 8 patch: update tensions and contingencies for Big Tech specimens."""

import json
import os
from datetime import date

BASE = os.path.join(os.path.dirname(__file__), "..")
SPECIMENS_DIR = os.path.join(BASE, "specimens")
TENSIONS_PATH = os.path.join(BASE, "synthesis", "tensions.json")
CONTINGENCIES_PATH = os.path.join(BASE, "synthesis", "contingencies.json")

today = date.today().isoformat()

# ─── Specimen tension/contingency updates ───

SPECIMEN_UPDATES = {
    "google-deepmind": {
        "tensionPositions": {
            "structuralVsContextual": -0.6,
            "speedVsDepth": 0.1,
            "centralVsDistributed": -0.7,
            "namedVsQuiet": -0.9,
            "longVsShortHorizon": -0.4
        },
        "contingencies": {
            "regulatoryIntensity": "Medium",
            "timeToObsolescence": "Fast",
            "ceoTenure": "Long",
            "talentMarketPosition": "Talent-rich",
            "technicalDebt": "Low"
        }
    },
    "apple": {
        "tensionPositions": {
            # Only updating T4 and T3 per discussion
            "namedVsQuiet": -0.1,
            "centralVsDistributed": 0.4
        }
        # contingencies stay as-is
    },
    "ami-labs": {
        "tensionPositions": {
            "centralVsDistributed": -0.7
        }
        # contingencies stay as-is
    }
}

# ─── Tension evidence entries to add ───

TENSION_EVIDENCE = {
    "structuralVsContextual": [
        {
            "specimenId": "google-deepmind",
            "position": -0.6,
            "evidence": "Named entity with formal leadership under Hassabis, dedicated budget, Brain+DeepMind merger created clear structural boundary. But explicit product pipeline mandate pulls slightly toward integration vs pure research separation."
        },
        {
            "specimenId": "intel",
            "position": -0.7,
            "evidence": "Intel Labs (700+ researchers) structurally separated from product groups. CEO Tan pulled AI strategy directly to himself after CTO departure. Clear structural separation between exploration (Labs) and execution (CCG, DCAI, ASIC)."
        },
        {
            "specimenId": "apple",
            "position": -0.6,
            "evidence": "Hub-and-spoke with deliberately weak hub. VP-level coordinator (Subramanya) under Federighi, not SVP direct-to-CEO. Functional org design distributes AI execution across SVPs. Structural separation exists but is thinner than any other Big Tech M4."
        }
    ],
    "speedVsDepth": [
        {
            "specimenId": "google-deepmind",
            "position": 0.1,
            "evidence": "Nearly balanced. 'Accelerate the pipeline' mandate and 50% AI-generated code signal speed. But world-modeling team (Tim Brooks), $175-185B CapEx for multi-year infrastructure, and Hassabis's Nobel-laureate research depth pull toward depth."
        },
        {
            "specimenId": "intel",
            "position": 0.3,
            "evidence": "Turnaround urgency creates speed pressure. Tan: 'under-promise and over-deliver.' Custom ASIC business growing 50%+. But Intel Labs on multi-year horizons (cognitive AI, quantum) and process node advancement (18A) require depth commitment."
        }
    ],
    "centralVsDistributed": [
        {
            "specimenId": "google-deepmind",
            "position": -0.7,
            "evidence": "Brain+DeepMind merger was explicitly about eliminating distributed coordination friction. Unified leadership under Hassabis. Half of ML compute allocated to Cloud — centrally managed resource."
        },
        {
            "specimenId": "apple",
            "position": 0.4,
            "evidence": "One of the most distributed AI structures in Big Tech. Functional SVPs own execution. Hub is deliberately thin — VP-level coordinator, not an SVP with product authority. Reflects Apple's functional org design philosophy."
        },
        {
            "specimenId": "intel",
            "position": -0.5,
            "evidence": "Turnaround centralization under CEO Tan. AI strategy pulled directly to CEO after CTO departure. Central Engineering Group created. But product groups (CCG, DCAI) retain execution autonomy."
        },
        {
            "specimenId": "ami-labs",
            "position": -0.7,
            "evidence": "Pre-launch startup under single founder's direction. But Executive Chair (not CEO) role suggests LeCun wants research direction authority without operational centralization."
        }
    ],
    "namedVsQuiet": [
        {
            "specimenId": "google-deepmind",
            "position": -0.9,
            "evidence": "Google DeepMind is one of the most visible AI entities globally. Hassabis is a Nobel laureate and public figure. Maximum named visibility."
        },
        {
            "specimenId": "apple",
            "position": -0.1,
            "evidence": "Subramanya is barely visible. VP-level, reports to Federighi, no public profile comparable to Hassabis/Wang/DeSantis. Apple's AI structure is the quietest in Big Tech — no named AI org, no CAIO title. Near the quiet end for a $383B company."
        },
        {
            "specimenId": "intel",
            "position": -0.6,
            "evidence": "Intel Labs is a named entity. Tan is visible as turnaround CEO. But AI-specific branding is weaker than pure AI companies — no 'Intel DeepMind' equivalent."
        }
    ],
    "longVsShortHorizon": [
        {
            "specimenId": "google-deepmind",
            "position": -0.4,
            "evidence": "$175-185B CapEx is multi-year infrastructure investment. World modeling team under Tim Brooks is long-horizon research. Supply-constrained through 2026 means building for 2027+. But 50% AI-generated code and Gemini serving cost reductions are immediate."
        },
        {
            "specimenId": "intel",
            "position": 0.2,
            "evidence": "Turnaround is inherently short-horizon — survival mode demands near-term results. But Intel Labs preserves multi-year research capacity (cognitive AI, quantum). 18A process node is a long-horizon bet paying off."
        }
    ]
}


def patch_specimens():
    """Update specimen JSON files with corrected tension/contingency values."""
    for spec_id, updates in SPECIMEN_UPDATES.items():
        path = os.path.join(SPECIMENS_DIR, f"{spec_id}.json")
        with open(path, "r") as f:
            spec = json.load(f)

        if "tensionPositions" in updates:
            for k, v in updates["tensionPositions"].items():
                spec["tensionPositions"][k] = v

        if "contingencies" in updates:
            for k, v in updates["contingencies"].items():
                spec["contingencies"][k] = v

        spec["meta"]["lastUpdated"] = today

        with open(path, "w") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

        print(f"  Updated {spec_id}.json")


def patch_tensions():
    """Add new specimen evidence to tensions.json."""
    with open(TENSIONS_PATH, "r") as f:
        data = json.load(f)

    for tension in data["tensions"]:
        field = tension["fieldName"]
        if field in TENSION_EVIDENCE:
            existing_ids = {s["specimenId"] for s in tension.get("specimens", [])}
            added = 0
            for entry in TENSION_EVIDENCE[field]:
                if entry["specimenId"] not in existing_ids:
                    if "specimens" not in tension:
                        tension["specimens"] = []
                    tension["specimens"].append(entry)
                    added += 1
            if added > 0:
                print(f"  {field}: added {added} specimen entries")

    data["lastUpdated"] = today

    with open(TENSIONS_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def patch_contingencies():
    """Add google-deepmind and intel to contingency specimen lists."""
    with open(CONTINGENCIES_PATH, "r") as f:
        data = json.load(f)

    additions = {
        "regulatoryIntensity": {"medium": ["google-deepmind", "intel", "apple"]},
        "timeToObsolescence": {"fast": ["google-deepmind", "intel"]},
        "ceoTenure": {
            "long": ["google-deepmind", "apple"],
            "short": ["intel"],
            "founder": ["ami-labs"]
        },
        "talentMarketPosition": {
            "talent-rich": ["google-deepmind", "apple"],
            "talent-constrained": ["intel"]
        },
        "technicalDebt": {
            "low": ["google-deepmind", "apple", "ami-labs"],
            "high": ["intel"]
        }
    }

    for contingency in data["contingencies"]:
        cid = contingency["id"]
        if cid in additions:
            for level, specs in additions[cid].items():
                # Find the right level key (high, medium, low, or named levels)
                for level_key in ["high", "medium", "low"]:
                    if level_key in contingency and level.lower() == level_key:
                        existing = set(contingency[level_key].get("specimens", []))
                        added = 0
                        for s in specs:
                            if s not in existing:
                                contingency[level_key]["specimens"].append(s)
                                added += 1
                        if added > 0:
                            print(f"  {cid}.{level_key}: added {added} specimens")
                        break
                else:
                    # Check named levels (e.g., "Founder", "Short", "Long")
                    for level_key in contingency:
                        if isinstance(contingency[level_key], dict) and "specimens" in contingency[level_key]:
                            if level_key.lower().startswith(level.lower()):
                                existing = set(contingency[level_key]["specimens"])
                                added = 0
                                for s in specs:
                                    if s not in existing:
                                        contingency[level_key]["specimens"].append(s)
                                        added += 1
                                if added > 0:
                                    print(f"  {cid}.{level_key}: added {added} specimens")
                                break

    data["lastUpdated"] = today

    with open(CONTINGENCIES_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    print("Patching specimen files...")
    patch_specimens()

    print("\nPatching tensions.json...")
    patch_tensions()

    print("\nPatching contingencies.json...")
    patch_contingencies()

    print(f"\nDone. All files updated with date {today}.")


if __name__ == "__main__":
    main()
