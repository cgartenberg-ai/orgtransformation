#!/usr/bin/env python3
"""Batch 3: Patch 6 specimens into tensions.json and contingencies.json.
Uses specimen-level tensionPositions as source of truth."""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Field name to tension ID mapping
TENSION_MAP = {
    "structuralVsContextual": 1,
    "speedVsDepth": 2,
    "centralVsDistributed": 3,
    "namedVsQuiet": 4,
    "longVsShortHorizon": 5,
}

# Evidence strings for each specimen × tension
EVIDENCE = {
    "unitedhealth-group": {
        1: "M4 hub-and-spoke: Responsible AI Board + United AI Studio as central governance hub; distributed execution across UHC/Optum/OptumRx spokes.",
        2: "1,000+ production use cases, 90% claims auto-adjudicated. Speed of broad deployment, not deep R&D bets. But Optum Labs does long-horizon academic research.",
        3: "Central governance (AI Review Board reviews hundreds of use cases monthly). But execution distributed across business units with separate AI leadership roles.",
        4: "Multiple named AI roles (Chief AI Scientist, Chief AI Transformation Officer) but no externally branded AI lab. Avoids AI conference circuit. Quiet external posture despite massive internal deployment.",
        5: "$1B AI cost reduction target for 2026 (short accountability). But Optum Labs UCLA partnership for foundational ML research (long horizon). Mixed.",
    },
    "accenture": {
        1: "No named AI lab visible. Enterprise-wide reskilling-or-exit mandate. Contextual: employees must adapt to AI within existing roles.",
        2: "11,000 role cuts signal speed over depth. Reskill-or-exit implies rapid adoption timeline, not careful piloting.",
        3: "Reskill-or-exit mandate is top-down from CEO. Central direction even if execution is distributed across 733K employees.",
        4: "No named AI lab or CAIO visible. Workforce transformation framed as general restructuring, not branded AI initiative.",
        5: "Short-term restructuring pressure ($865M charge). But consulting model requires continuous capability building for client relevance.",
    },
    "cognizant": {
        1: "Three distinct AI-focused units (market-facing, integrated solutions, centralized platforms). Structural separation of AI from traditional delivery.",
        2: "Vector One augments current delivery (speed). Vectors Two/Three build agentic software (depth). Mixed but tilted toward rapid deployment.",
        3: "Centralized platforms unit + distributed market-facing teams. Balanced hub-and-spoke.",
        4: "Named three-unit reorganization. BASIS framework and 'science of context engineering' are branded. But not a loudly marketed AI lab.",
        5: "Three-vector strategy spans near-term augmentation to medium-term agentic software. Balanced temporal horizon.",
    },
    "genpact": {
        1: "Advanced Technology Solutions as distinct structural unit (24% of revenue). Clear separation from traditional BPO services.",
        2: "400+ GenAI solutions deployed (speed). But building long-term AI Maestro platform and three-pillar agentic model (depth). Tilted toward speed.",
        3: "Central AI Maestro platform with distributed deployment across client engagements. Central product, distributed execution.",
        4: "Named Advanced Technology Solutions unit. AI Maestro platform is branded. But not a research lab — it's a business unit.",
        5: "Quarterly revenue accountability (17% YoY growth target). But building long-term platform play. Slightly short-horizon.",
    },
    # Sanofi — missing T2, T4, T5
    "sanofi": {
        2: "Multi-year drug discovery timelines. CodonBERT and plai platform represent deep capability building, not rapid deployment.",
        4: "AI Research Factory is internally named. CEO Hudson publicly brands Sanofi as 'AI-powered biopharma company.' ROAI framework creates accountability. But no external AI lab brand.",
        5: "Drug discovery inherently long-horizon. But Hudson's ROAI framework and '95% of pilots fail' framing signal push for measurable near-term returns.",
    },
    # Infosys — missing T1, T3, T4, T5
    "infosys": {
        1: "Named CoE with Cursor is a distinct structural unit. AI Engineering Experience Zone is physically separate. Structural separation of AI capability.",
        3: "Central CoE provides standardized tooling to 100K engineers. Centralized capability building, distributed consumption.",
        4: "Named CoE with formal press announcement. CEO involved. AI Engineering Experience Zone for client demos. Named and visible.",
        5: "IT services model demands quarterly delivery. But CoE represents longer-term capability investment. Slightly short-horizon.",
    },
}

# --- TENSIONS ---
tensions_path = os.path.join(BASE, "synthesis", "tensions.json")
with open(tensions_path, "r") as f:
    tensions = json.load(f)

# Read specimen files for positions
specimens_to_patch = ["unitedhealth-group", "accenture", "cognizant", "genpact", "sanofi", "infosys"]
added_count = 0

for sid in specimens_to_patch:
    spec_path = os.path.join(BASE, "specimens", f"{sid}.json")
    with open(spec_path) as f:
        spec = json.load(f)

    tp = spec.get("tensionPositions", {})

    for field_name, tension_id in TENSION_MAP.items():
        position = tp.get(field_name)
        if position is None:
            continue

        # Check if evidence exists for this specimen × tension
        if sid not in EVIDENCE or tension_id not in EVIDENCE[sid]:
            continue

        t = next(t for t in tensions["tensions"] if t["id"] == tension_id)
        existing = {s["specimenId"] for s in t["specimens"]}
        if sid not in existing:
            t["specimens"].append({
                "specimenId": sid,
                "position": position,
                "evidence": EVIDENCE[sid][tension_id]
            })
            added_count += 1

print(f"Added {added_count} tension placements")

with open(tensions_path, "w") as f:
    json.dump(tensions, f, indent=2, ensure_ascii=False)
    f.write("\n")

# Verify
print("\n=== TENSION VERIFICATION ===")
for sid in specimens_to_patch:
    present = []
    for t in tensions["tensions"]:
        if any(s["specimenId"] == sid for s in t["specimens"]):
            present.append(t["id"])
    missing = [i for i in [1,2,3,4,5] if i not in present]
    status = "COMPLETE" if not missing else f"MISSING T{missing}"
    print(f"  {sid}: {len(present)}/5 {status}")

# --- CONTINGENCIES ---
cont_path = os.path.join(BASE, "synthesis", "contingencies.json")
with open(cont_path, "r") as f:
    cont = json.load(f)

def add_contingency(cont_id, level, specimen_id):
    c = next(c for c in cont["contingencies"] if c["id"] == cont_id)
    if level not in c:
        print(f"  WARNING: level '{level}' not in {cont_id}")
        return False
    specimens = c[level].get("specimens", [])
    if specimen_id not in specimens:
        specimens.append(specimen_id)
        c[level]["specimens"] = specimens
        return True
    return False

# Contingency mappings from specimen files
# UnitedHealth: high reg, slow obsol, long CEO, talent-rich, medium debt
add_contingency("regulatoryIntensity", "high", "unitedhealth-group")
add_contingency("timeToObsolescence", "low", "unitedhealth-group")  # "Slow" maps to low
add_contingency("ceoTenure", "high", "unitedhealth-group")  # "Long" maps to high
add_contingency("talentMarketPosition", "high", "unitedhealth-group")  # "Talent-rich" maps to high
add_contingency("technicalDebt", "medium", "unitedhealth-group")

# Accenture: medium reg, fast obsol, medium CEO, talent-rich, low debt (consulting has low legacy tech)
add_contingency("regulatoryIntensity", "low", "accenture")  # consulting = low reg
add_contingency("timeToObsolescence", "high", "accenture")  # fast = high urgency
add_contingency("ceoTenure", "medium", "accenture")
add_contingency("talentMarketPosition", "high", "accenture")  # talent-rich
add_contingency("technicalDebt", "low", "accenture")  # consulting, low legacy systems

# Cognizant: low reg, fast obsol, medium CEO, talent-rich, low debt
add_contingency("regulatoryIntensity", "low", "cognizant")
add_contingency("timeToObsolescence", "high", "cognizant")  # fast = high urgency (IT services threatened)
add_contingency("ceoTenure", "medium", "cognizant")  # Ravi Kumar CEO since 2023
add_contingency("talentMarketPosition", "high", "cognizant")  # 4000+ AI practitioners
add_contingency("technicalDebt", "low", "cognizant")  # IT services, modern tech

# Genpact: medium reg, medium obsol, medium CEO, talent-rich (7000 AI builders), medium debt
add_contingency("regulatoryIntensity", "medium", "genpact")
add_contingency("timeToObsolescence", "medium", "genpact")
add_contingency("ceoTenure", "medium", "genpact")  # Kalra CEO since 2024
add_contingency("talentMarketPosition", "high", "genpact")  # 7000 AI builders, 20K practitioners
add_contingency("technicalDebt", "medium", "genpact")

# Sanofi — only missing ceoTenure
add_contingency("ceoTenure", "high", "sanofi")  # Paul Hudson CEO since 2019 (~7 years), strong mandate

# Infosys — only missing ceoTenure
add_contingency("ceoTenure", "medium", "infosys")  # Salil Parekh CEO since 2018 (~8 years), medium

with open(cont_path, "w") as f:
    json.dump(cont, f, indent=2, ensure_ascii=False)
    f.write("\n")

# Verify contingencies
print("\n=== CONTINGENCY VERIFICATION ===")
for sid in specimens_to_patch:
    present = []
    for c in cont["contingencies"]:
        for level_key in ["high", "medium", "low", "fast", "founder", "new", "critical",
                          "nonTraditional", "non-traditional", "talent-rich", "talent-constrained"]:
            if level_key in c and isinstance(c[level_key], dict):
                specs = c[level_key].get("specimens", [])
                if sid in specs:
                    present.append(c["id"])
                    break
    missing = [cid for cid in ["regulatoryIntensity", "timeToObsolescence", "ceoTenure",
                                "talentMarketPosition", "technicalDebt"] if cid not in present]
    status = "COMPLETE" if not missing else f"MISSING {missing}"
    print(f"  {sid}: {len(present)}/5 {status}")

print("\nDone.")
