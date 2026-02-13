#!/usr/bin/env python3
"""Batch 2: Patch 8 specimens into tensions.json and contingencies.json."""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- TENSIONS ---
tensions_path = os.path.join(BASE, "synthesis", "tensions.json")
with open(tensions_path, "r") as f:
    tensions = json.load(f)

# Helper: add specimen to tension if not already present
def add_tension(tension_id, specimen_id, position, evidence):
    t = next(t for t in tensions["tensions"] if t["id"] == tension_id)
    existing = {s["specimenId"] for s in t["specimens"]}
    if specimen_id not in existing:
        t["specimens"].append({
            "specimenId": specimen_id,
            "position": position,
            "evidence": evidence
        })
        return True
    return False

# Bank of America — T1-T5
add_tension(1, "bank-of-america", 0.8, "No separate AI unit. 90%+ of 213K employees use AI tools in existing roles. Contextual integration via consumer-grade tools.")
add_tension(2, "bank-of-america", 0.3, "Broad deployment (90%+ adoption, 169M Erica interactions/quarter) over depth. Incremental expansion of proven interfaces.")
add_tension(3, "bank-of-america", -0.3, "Technology leadership drives platform centrally. $4.5B AI budget through existing tech org. But adoption distributed across all roles.")
add_tension(4, "bank-of-america", 0.9, "No named AI lab, no CAIO. AI embedded through consumer-grade tools (Erica). Structural transformation without formal transformation program.")
add_tension(5, "bank-of-america", 0.2, "Quarterly feature additions. 24-month agentic AI efficiency targets. But 15-year sustained investment trajectory.")

# Wells Fargo — T5
add_tension(5, "wells-fargo", 0.2, "30-35% automation target, $612M severance Q4 2025, headcount down 6%. Near-term restructuring pressure, but dual-role appointment signals longer-term investment.")

# UBS — T5
add_tension(5, "ubs", 0.0, "CAIO appointed for long-term AI governance, but Credit Suisse integration forces short-term execution. 300+ use cases suggest breadth over deep R&D bets.")

# Moderna — T1-T5
add_tension(1, "moderna", 0.8, "No separate AI unit. 100% proficiency target across entire organization. AI Academy is educational, not structural.")
add_tension(2, "moderna", 0.6, "100% adoption within 6 months. 750+ GPTs from broad deployment. Deploy-first approach.")
add_tension(3, "moderna", 0.5, "Generative AI Champions are distributed power users, not a central team. Every employee expected to achieve AI proficiency.")
add_tension(4, "moderna", 0.4, "No named AI lab. mChat and AI Academy are tools/programs, not organizational structures.")
add_tension(5, "moderna", 0.3, "6-month proficiency targets. $2B opex reduction pressure. But mRNA R&D inherently long-horizon.")

# Novo Nordisk — T1-T5
add_tension(1, "novo-nordisk", -0.3, "300-person Enterprise AI hub is a distinct structural unit. But mass Copilot deployment (20K) has contextual elements.")
add_tension(2, "novo-nordisk", -0.2, "Mix: deep drug discovery AI + broad Copilot deployment. Neither extreme.")
add_tension(3, "novo-nordisk", -0.4, "Central CAIO with 300-person hub sets standards. BU spokes have some autonomy but hub dominates.")
add_tension(4, "novo-nordisk", -0.3, "CAIO role, named Enterprise AI team. Formally structured internally but not loudly branded externally.")
add_tension(5, "novo-nordisk", -0.4, "Drug discovery inherently long-horizon. DKK 60B manufacturing capex + DKK 30B R&D. New CEO creates some uncertainty.")

# Pfizer — T1, T3, T4, T5
add_tension(1, "pfizer", -0.5, "CAIO-led hub with AI/ML Fab Lab and Incubator as distinct structural units. AI engineers embedded in each R&D function.")
add_tension(3, "pfizer", -0.3, "Central CAIO sets strategy, Fab Lab experiments. But embedding AI engineers in each function distributes capability. Hub-and-spoke balance.")
add_tension(4, "pfizer", -0.5, "Named CAIO, AI/ML Fab Lab, Predictive Analytics Incubator, PACT partnership. Multiple branded structures.")
add_tension(5, "pfizer", -0.3, "Drug discovery = years. But $600M savings in 2025 and $1.5B target by 2027 show quarterly accountability too.")

# Roche-Genentech — T1, T3, T4
add_tension(1, "roche-genentech", -0.6, "gRED Computational Sciences is a distinct research entity. Prescient Design acquisition brought dedicated AI team.")
add_tension(3, "roche-genentech", -0.5, "Computational sciences group centrally coordinated under Aviv Regev. NVIDIA and Recursion partnerships flow through central research leadership.")
add_tension(4, "roche-genentech", -0.4, "Lab in a Loop is a branded concept. Prescient Design is named. But Roche doesn't loudly market an AI Lab externally.")

with open(tensions_path, "w") as f:
    json.dump(tensions, f, indent=2, ensure_ascii=False)
    f.write("\n")

# Verify
print("=== TENSION VERIFICATION ===")
for sid in ["bank-of-america", "wells-fargo", "ubs", "eli-lilly", "moderna", "novo-nordisk", "pfizer", "roche-genentech"]:
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
        print(f"  WARNING: level '{level}' not found in {cont_id}")
        return False
    specimens = c[level].get("specimens", [])
    if specimen_id not in specimens:
        specimens.append(specimen_id)
        c[level]["specimens"] = specimens
        return True
    return False

# Wells Fargo — C2, C3, C4, C5
add_contingency("timeToObsolescence", "medium", "wells-fargo")
add_contingency("ceoTenure", "medium", "wells-fargo")
add_contingency("talentMarketPosition", "low", "wells-fargo")
add_contingency("technicalDebt", "high", "wells-fargo")

# UBS — C2, C3
add_contingency("timeToObsolescence", "medium", "ubs")
add_contingency("ceoTenure", "medium", "ubs")

# Eli Lilly — C4, C5
add_contingency("talentMarketPosition", "high", "eli-lilly")
add_contingency("technicalDebt", "low", "eli-lilly")

# Moderna — C3
add_contingency("ceoTenure", "founder", "moderna")

# Novo Nordisk — C3
add_contingency("ceoTenure", "new", "novo-nordisk")

# Pfizer — C3
add_contingency("ceoTenure", "high", "pfizer")

# Roche-Genentech — C3
add_contingency("ceoTenure", "medium", "roche-genentech")

with open(cont_path, "w") as f:
    json.dump(cont, f, indent=2, ensure_ascii=False)
    f.write("\n")

# Verify contingencies
print("\n=== CONTINGENCY VERIFICATION ===")
for sid in ["bank-of-america", "wells-fargo", "ubs", "eli-lilly", "moderna", "novo-nordisk", "pfizer", "roche-genentech"]:
    present = []
    for c in cont["contingencies"]:
        for level_key in ["high", "medium", "low", "fast", "founder", "new", "critical", "nonTraditional", "non-traditional", "talent-rich", "talent-constrained"]:
            if level_key in c:
                specs = c[level_key].get("specimens", [])
                if sid in specs:
                    present.append(c["id"])
                    break
    missing = [cid for cid in ["regulatoryIntensity", "timeToObsolescence", "ceoTenure", "talentMarketPosition", "technicalDebt"] if cid not in present]
    status = "COMPLETE" if not missing else f"MISSING {missing}"
    print(f"  {sid}: {len(present)}/5 {status}")

print("\nDone.")
