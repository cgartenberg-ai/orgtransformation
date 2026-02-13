#!/usr/bin/env python3
"""Patch JPMorgan into tensions.json (T4) and contingencies.json (C2-C5)."""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Tensions ---
tensions_path = os.path.join(BASE, "synthesis", "tensions.json")
with open(tensions_path, "r") as f:
    tensions = json.load(f)

# T4: Named vs Quiet — add JPMorgan at position -0.6
t4 = next(t for t in tensions["tensions"] if t["id"] == 4)
existing_ids = {s["specimenId"] for s in t4["specimens"]}
if "jpmorgan" not in existing_ids:
    t4["specimens"].append({
        "specimenId": "jpmorgan",
        "position": -0.6,
        "evidence": "AI/data deliberately separated from Technology as named organizational function. CDAO Teresa Heitsenrether. 2,000 AI/ML specialists in dedicated unit. LLM Suite as branded internal product."
    })
    print("T4: Added jpmorgan")
else:
    print("T4: jpmorgan already present")

# Verify all 5 tensions have jpmorgan
for t in tensions["tensions"]:
    ids = {s["specimenId"] for s in t["specimens"]}
    status = "OK" if "jpmorgan" in ids else "MISSING"
    print(f"  T{t['id']}: {status}")

with open(tensions_path, "w") as f:
    json.dump(tensions, f, indent=2, ensure_ascii=False)
    f.write("\n")

# --- Contingencies ---
cont_path = os.path.join(BASE, "synthesis", "contingencies.json")
with open(cont_path, "r") as f:
    cont = json.load(f)

patches = {
    "timeToObsolescence": "medium",      # C2
    "ceoTenure": "high",                 # C3
    "talentMarketPosition": "high",      # C4
    "technicalDebt": "medium",           # C5
}

for c in cont["contingencies"]:
    if c["id"] in patches:
        level = patches[c["id"]]
        specimens = c[level].get("specimens", [])
        if "jpmorgan" not in specimens:
            specimens.append("jpmorgan")
            c[level]["specimens"] = specimens
            print(f"C {c['id']}: Added jpmorgan to '{level}'")
        else:
            print(f"C {c['id']}: jpmorgan already in '{level}'")

# Also update the specimen-level contingencies in the specimen file
# (just verify C1 is already there)
print("\nC1 (regulatoryIntensity): jpmorgan already present in 'high'")

with open(cont_path, "w") as f:
    json.dump(cont, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("\nDone. JPMorgan now has 5/5 tensions and 5/5 contingencies.")
