#!/usr/bin/env python3
"""
Patch script for Batch 7: kyndryl, panasonic, t-mobile, uber, chegg, thomson-reuters, recruit-holdings
Adds tension placements and contingency entries to synthesis files.
Session: 2026-02-12
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TENSIONS_PATH = os.path.join(BASE, "synthesis", "tensions.json")
CONTINGENCIES_PATH = os.path.join(BASE, "synthesis", "contingencies.json")

# ============================================================
# TENSION PLACEMENTS
# ============================================================

tension_placements = {
    1: [  # Structural Separation vs. Contextual Integration
        {"specimenId": "kyndryl", "position": -0.4, "evidence": "M2 CoE with 3 dedicated AI practices (Intelligent Ops, Data & AI, App & Digital). Structural separation but practices are delivery-focused, not ring-fenced research."},
        {"specimenId": "panasonic", "position": -0.5, "evidence": "CAIO at holdings level with separate AI lab + Blue Yonder subsidiary. Holdings-level structural separation from operating companies."},
        # t-mobile: already placed at -0.6
        # uber: already placed at -0.6
        # chegg: null — insufficient data
        # thomson-reuters: already placed at -0.3
        {"specimenId": "recruit-holdings", "position": 0.5, "evidence": "M3/Contextual — AI embedded in product/engineering under EVP Mukherjee. No separate AI division, no CAIO. AI proficiency expected across organization. Dual-hat CEO drives integration, not separation."},
    ],
    2: [  # Speed of Deployment vs. Depth of Learning
        {"specimenId": "kyndryl", "position": 0.0, "evidence": "Balanced — alliance-based approach enables rapid deployment of partner-built agents, but practice-based structure preserves domain depth. Bridge roles suggest deliberate translation."},
        {"specimenId": "panasonic", "position": -0.2, "evidence": "Leans depth — CAIO at holdings level with multi-year horizons. Blue Yonder enterprise-grade supply chain AI with methodical implementation for 230K-employee conglomerate."},
        {"specimenId": "t-mobile", "position": 0.0, "evidence": "Split — IntentCX launched quickly (75% interaction reduction target), but AI-RAN is '5G Advanced era and beyond' (3-5+ years). Two tracks at different speeds."},
        {"specimenId": "uber", "position": 0.4, "evidence": "Leans speed — Khosrowshahi: 'surviving car crashes internally' and 'throwing away old policies.' Customer service AI rebuilt through deployment-driven iteration, not specification."},
        # chegg: null
        {"specimenId": "thomson-reuters", "position": -0.4, "evidence": "Leans depth — 4,000+ SMEs (lawyers, accountants) evaluate AI outputs before deployment. CTO Hron: 'AI didn't shrink our roadmap; it made it bigger.' Quality-gated professional services deployment."},
        {"specimenId": "recruit-holdings", "position": 0.4, "evidence": "Leans speed — AI assists job seekers every 2.2 seconds. AI writes 1/3 of code targeting 50% by 2026. ~4,500 employees cut while deploying aggressively."},
    ],
    3: [  # Centralized Control vs. Distributed Autonomy
        {"specimenId": "kyndryl", "position": 0.3, "evidence": "Leans distributed — alliance-based model with multiple vendor partnerships. Practices have autonomy within domains. No single centralized AI authority."},
        {"specimenId": "panasonic", "position": -0.4, "evidence": "Leans centralized — CAIO at holdings level creates central governance over operating companies. 'Business CEO' dual-hat mechanism for Blue Yonder."},
        # t-mobile: already placed at 0.2
        # uber: already placed at -0.3
        # chegg: null
        # thomson-reuters: already placed at -0.2
        {"specimenId": "recruit-holdings", "position": -0.3, "evidence": "Dual-hat CEO centralizes strategic authority. EVP Mukherjee leads AI product decisions within Indeed but reports to Idekoba. Glassdoor absorption eliminates distributed autonomy."},
    ],
    4: [  # Named AI Brand vs. Quiet Integration
        {"specimenId": "kyndryl", "position": -0.3, "evidence": "Named practices (Intelligent Ops, Data & AI), named alliances. Services firm needs visible AI branding for client credibility."},
        {"specimenId": "panasonic", "position": -0.3, "evidence": "Named CAIO role, named 'Panasonic AI' umbrella, Blue Yonder brand. Public about AI transformation at CES and investor events."},
        # t-mobile: already placed at -0.4
        # uber: already placed at -0.7
        # chegg: null
        # thomson-reuters: already placed at -0.6
        {"specimenId": "recruit-holdings", "position": 0.6, "evidence": "Quiet — no named AI lab, no CAIO title, no branded AI initiative. AI embedded in product/engineering without branding. Responsible AI team is governance, not PR."},
    ],
    5: [  # Long Time Horizons vs. Short Accountability Cycles
        {"specimenId": "kyndryl", "position": 0.2, "evidence": "Short-leaning — IBM spinoff under market pressure. Alliance-based strategy enables faster time-to-market. Quarterly client delivery cycles."},
        {"specimenId": "panasonic", "position": -0.3, "evidence": "Long-leaning — Holdings-level CAIO with multi-year AI strategy across operating companies. Blue Yonder investment is multi-year bet."},
        {"specimenId": "t-mobile", "position": -0.3, "evidence": "Long-leaning — AI-RAN is '5G Advanced era and beyond.' 60 edge data centers planned. New CEO creates some short-term accountability."},
        {"specimenId": "uber", "position": 0.0, "evidence": "Split — AV timeline is 10-20 years (long). Customer AI iterates on quarterly cycles (short). AI Labs does multi-year research. Deliberately mixed."},
        # chegg: null
        {"specimenId": "thomson-reuters", "position": 0.0, "evidence": "Split — TR Labs on multi-year R&D horizons, product teams on quarterly ACV cadences, acquisition pipeline on 6-12 month integration cycles. Deliberately balanced."},
        {"specimenId": "recruit-holdings", "position": 0.3, "evidence": "Short-leaning — aggressive sequential restructuring (cut → consolidate → rebuild) over 2023-2025. AI code generation targets on 1-2 year horizons. CEO's return signals urgency."},
    ],
}

# ============================================================
# CONTINGENCY PLACEMENTS
# ============================================================

contingency_placements = {
    "regulatoryIntensity": {
        "high": ["uber", "thomson-reuters"],  # already placed
        "medium": ["kyndryl", "panasonic", "t-mobile"],
        "low": ["chegg", "recruit-holdings"],
    },
    "timeToObsolescence": {
        "fast": ["kyndryl", "uber", "chegg", "recruit-holdings"],
        "medium": ["t-mobile", "thomson-reuters"],
        "slow": ["panasonic"],
    },
    "ceoTenure": {
        "short": ["kyndryl", "t-mobile"],
        "medium": ["panasonic", "uber", "thomson-reuters"],
        "long": ["recruit-holdings"],
        # chegg: null
    },
    "talentMarketPosition": {
        "talent-rich": ["uber", "thomson-reuters", "recruit-holdings"],
        "talent-constrained": ["kyndryl", "panasonic"],
        # t-mobile: mixed → put in medium/neither, handle as note
        # chegg: null
    },
    "technicalDebt": {
        "high": ["kyndryl", "panasonic"],
        "medium": ["t-mobile", "uber", "thomson-reuters", "recruit-holdings"],
        # chegg: null
    },
}


def patch_tensions(data):
    """Add new specimen placements to tensions.json"""
    added = 0
    for tension in data["tensions"]:
        tid = tension["id"]
        if tid not in tension_placements:
            continue

        existing_ids = set()
        for s in tension.get("specimens", []):
            if isinstance(s, dict):
                existing_ids.add(s["specimenId"])
            else:
                existing_ids.add(s)

        for placement in tension_placements[tid]:
            if placement["specimenId"] not in existing_ids:
                tension["specimens"].append(placement)
                added += 1
                print(f"  T{tid}: Added {placement['specimenId']} (pos={placement['position']})")
            else:
                print(f"  T{tid}: {placement['specimenId']} already exists, skipping")

    return added


def patch_contingencies(data):
    """Add new specimen entries to contingencies.json"""
    added = 0
    for contingency in data["contingencies"]:
        cid = contingency["id"]
        if cid not in contingency_placements:
            continue

        for level, specimens in contingency_placements[cid].items():
            # Handle level naming (talent-rich → find the matching key)
            level_key = None
            for k in contingency.keys():
                if k == level:
                    level_key = k
                    break
                # Handle talent-rich / talent-constrained keys
                if level == "talent-rich" and "rich" in k.lower():
                    level_key = k
                    break
                if level == "talent-constrained" and "constrain" in k.lower():
                    level_key = k
                    break

            if level_key is None:
                # Try alternate key names
                for k in contingency.keys():
                    if isinstance(contingency[k], dict) and "specimens" in contingency[k]:
                        lbl = contingency[k].get("label", "").lower()
                        if level in lbl or (level == "talent-rich" and "rich" in lbl) or (level == "talent-constrained" and ("constrain" in lbl or "scarce" in lbl)):
                            level_key = k
                            break

            if level_key is None:
                print(f"  WARNING: Could not find level key '{level}' for contingency '{cid}'")
                continue

            existing = set(contingency[level_key].get("specimens", []))
            for spec in specimens:
                if spec not in existing:
                    contingency[level_key]["specimens"].append(spec)
                    added += 1
                    print(f"  {cid}.{level_key}: Added {spec}")
                else:
                    print(f"  {cid}.{level_key}: {spec} already exists, skipping")

    return added


# Also handle T-Mobile talent as a special case
def patch_tmobile_talent(data):
    """T-Mobile is talent-mixed — place in neither pure bucket but add a note"""
    # For now, skip — T-Mobile doesn't clearly fit talent-rich or talent-constrained
    # The partnership-heavy model (NVIDIA, OpenAI) suggests talent constraints
    # but Bellevue location near Seattle suggests some access
    # Best to leave unplaced with a note
    pass


def main():
    print("=" * 60)
    print("Batch 7 Patch Script")
    print("=" * 60)

    # Patch tensions
    print("\n--- TENSIONS ---")
    with open(TENSIONS_PATH, 'r') as f:
        tensions = json.load(f)

    t_added = patch_tensions(tensions)
    tensions["lastUpdated"] = "2026-02-12"

    with open(TENSIONS_PATH, 'w') as f:
        json.dump(tensions, f, indent=2, ensure_ascii=False)

    print(f"\nTensions: {t_added} placements added")

    # Patch contingencies
    print("\n--- CONTINGENCIES ---")
    with open(CONTINGENCIES_PATH, 'r') as f:
        contingencies = json.load(f)

    c_added = patch_contingencies(contingencies)
    contingencies["lastUpdated"] = "2026-02-12"

    with open(CONTINGENCIES_PATH, 'w') as f:
        json.dump(contingencies, f, indent=2, ensure_ascii=False)

    print(f"\nContingencies: {c_added} placements added")

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {t_added} tension + {c_added} contingency placements")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
