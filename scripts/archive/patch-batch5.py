#!/usr/bin/env python3
"""
Batch 5: Defense/Transport specimens — 5 non-government specimens.
Government specimens (nasa, us-cyber-command, new-york-state, us-air-force)
are being removed from synthesis files — political entities with mandate-driven
AI adoption don't belong in an organizational economics analysis.

Specimens placed:
- anduril (M9 AI-Native, defense tech)
- blue-origin (M6a Enterprise-Wide, aerospace)
- lockheed-martin (M4 Hub-and-Spoke, defense — already 5/5 T, 5/5 C)
- delta-air-lines (M4 Hub-and-Spoke, airlines)
- fedex (M4 Hub-and-Spoke, logistics)

Key observations (not new insights — reinforce existing modularity hypothesis):
1. Anduril vs Lockheed validates modularity → structure prediction
   (clean-sheet modular → M9; integral legacy → M4)
2. Delta-FedEx pair: same M4/contextual model, different deployment velocity
   driven by CEO conviction (Bastian skeptic vs Subramaniam pragmatic)
3. Blue Origin M6a in aerospace challenges industry → structure prediction,
   but CEO provenance (Limp from Amazon Alexa) is the explanatory variable
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)

def save_json(path, data):
    with open(os.path.join(BASE, path), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

# ─── Load central files ───
tensions_data = load_json('synthesis/tensions.json')
contingencies_data = load_json('synthesis/contingencies.json')
tensions = tensions_data['tensions']
contingencies = contingencies_data['contingencies']

def find_tension(tid):
    return next(t for t in tensions if t['id'] == tid)

def find_contingency(cid):
    return next(c for c in contingencies if c['id'] == cid)

def specimen_in_tension(t, sid):
    return any(s['specimenId'] == sid for s in t.get('specimens', []))

def specimen_in_contingency_level(c, level_key, sid):
    level_data = c.get(level_key, {})
    if isinstance(level_data, dict):
        for s in level_data.get('specimens', []):
            if isinstance(s, str) and s == sid:
                return True
            elif isinstance(s, dict) and s.get('specimenId') == sid:
                return True
    return False

def add_to_tension(tid, sid, position, evidence):
    t = find_tension(tid)
    if not specimen_in_tension(t, sid):
        t['specimens'].append({
            'specimenId': sid,
            'position': position,
            'evidence': evidence
        })
        print(f"  + T{tid} {sid} @ {position}")
    else:
        print(f"  = T{tid} {sid} already present")

def add_to_contingency(cid, level, sid):
    c = find_contingency(cid)
    level_lower = level.lower()
    skip_keys = {'id', 'name', 'whatItDetermines'}

    matched_key = None
    for k in c:
        if k in skip_keys:
            continue
        if k.lower() == level_lower:
            matched_key = k
            break

    if not matched_key:
        c[level] = {'label': level, 'favors': [], 'mechanisms': [], 'specimens': []}
        matched_key = level
        print(f"  ! Created new level '{level}' for {cid}")

    if not specimen_in_contingency_level(c, matched_key, sid):
        c[matched_key]['specimens'].append(sid)
        print(f"  + {cid}/{matched_key} {sid}")
    else:
        print(f"  = {cid}/{matched_key} {sid} already present")

def remove_from_tension(tid, sid):
    t = find_tension(tid)
    before = len(t.get('specimens', []))
    t['specimens'] = [s for s in t.get('specimens', []) if s.get('specimenId') != sid]
    after = len(t['specimens'])
    if before != after:
        print(f"  - T{tid} removed {sid}")
    return before != after

def remove_from_contingency(cid, sid):
    c = find_contingency(cid)
    skip_keys = {'id', 'name', 'whatItDetermines'}
    removed = False
    for k in list(c.keys()):
        if k in skip_keys:
            continue
        level_data = c.get(k, {})
        if isinstance(level_data, dict) and 'specimens' in level_data:
            before = len(level_data['specimens'])
            level_data['specimens'] = [
                s for s in level_data['specimens']
                if not (isinstance(s, str) and s == sid) and
                   not (isinstance(s, dict) and s.get('specimenId') == sid)
            ]
            if len(level_data['specimens']) != before:
                print(f"  - {cid}/{k} removed {sid}")
                removed = True
    return removed


# ═══════════════════════════════════════════════════════════
# STEP 0: Remove government specimens from synthesis files
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 0: Remove government specimens from synthesis files")
print("=" * 60)

gov_specimens = ['nasa', 'us-cyber-command', 'new-york-state', 'us-air-force', 'pentagon-cdao']

for sid in gov_specimens:
    print(f"\n--- Removing {sid} ---")
    for tid in [1, 2, 3, 4, 5]:
        remove_from_tension(tid, sid)
    for cid in ['regulatoryIntensity', 'timeToObsolescence', 'ceoTenure', 'talentMarketPosition', 'technicalDebt']:
        remove_from_contingency(cid, sid)


# ═══════════════════════════════════════════════════════════
# STEP 1: Sync 5 specimens to central tension arrays
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1: Sync 5 specimens to central tension arrays")
print("=" * 60)

evidence = {
    'anduril': {
        1: "M9 AI-Native with structural orientation. AI is product divisions (Air, Maritime, Space/Intel), each with embedded AI/ML. Lattice is infrastructure, not a separate team.",
        2: "'Months not years' vs defense primes. Ships Ghost/Sentry quickly. But YFQ-44A Fury and Arsenal-1 are multi-year. Fast for defense sector.",
        3: "Centralized around founding team (Luckey, Schimpf, Grimm). Product teams have execution autonomy but strategic decisions are founder-controlled.",
        4: "Maximally named: branded as AI-defense company. Lattice platform, AI Grand Prix competition, 60 Minutes/TED presence. AI IS the brand.",
        5: "Mixed: ships products on contract timelines, but Arsenal-1 and Fury CCA are multi-year. Luckey: 'do things now, tech will catch up.' Lean execution.",
    },
    'blue-origin': {
        1: "M6a contextual: 70% company-wide adoption, 2,700 agents, agent marketplace. 'Everyone builds and collaborates with AI agents.' No separate AI unit.",
        2: "Fast deployment: 2,700 agents, 3.5M monthly interactions, agent marketplace enables rapid proliferation. But T-Rex project is multi-year R&D.",
        3: "Distributed: 'everyone at Blue Origin builds and collaborates with AI agents.' Agent marketplace enables decentralized creation and sharing.",
        4: "Quiet: no CAIO, no AI lab, no branded AI initiative. AI capability delivered through BlueGPT platform managed by Enterprise Technology.",
        5: "Balanced: immediate agent deployment for productivity + 5-10 year vision (space data centers, lunar AI-designed hardware). True dual horizon.",
    },
    'lockheed-martin': {
        1: "M4 hub-and-spoke: LAIC is centralized hub with DGX SuperPOD. 7,000 engineers in spokes access AI Factory. Clear structural separation.",
        2: "Deep/governed: hub provides infrastructure, MLOps, governance. Hundreds of active projects but 6-month update cycles, not weeks. Deliberate pace for classified work.",
        3: "Centralized governance: data council, governance board, data steward network. Standards flow hub→spokes. Ethical AI committee aligned with DoD principles.",
        4: "Named: LAIC, AI Factory, Astris AI subsidiary, CDAIO Mike Baylor, CTO Craig Martell (former DoD CDAO). Heavily branded.",
        5: "Long-leaning: multi-decade '21st Century Security' vision. $5B CapEx/IR&D for 2026. Hub supports near-term integration + long-term research via ATL.",
    },
    'delta-air-lines': {
        1: "M4 with contextual goal: central Enterprise Data & AI sets standards, but 'augmented intelligence' philosophy pushes AI into existing roles. Not separate AI unit.",
        2: "Measured/deep: 1% of pricing AI-driven, multi-year expansion planned. $500M cloud as foundation first. Bastian predicts 'day of reckoning' for rushed AI.",
        3: "Balanced: CDTO centralizes standards, but implementation distributed to TechOps, pricing, crew scheduling, customer experience. Innovation hubs (Hangar, Sustainable Skies Lab).",
        4: "Lean named: CDTO on Leadership Committee, CES keynote. But no branded 'AI Lab' — framed as 'augmented intelligence' philosophy, not org unit.",
        5: "Balanced: near-term operational AI (quarterly) + Delta Concierge (multi-year rollout) + Sustainable Skies Lab (long horizon). Measured across all horizons.",
    },
    'fedex': {
        1: "M4 with contextual training push: Dataworks is central platform hub, but Dec 2025 enterprise-wide AI education trains employees in existing roles.",
        2: "Lean fast: enterprise-wide AI education launched, operational AI deployed broadly (delivery estimation, routing). But humanoid robotics 'not ready for prime time.'",
        3: "Central platform, distributed execution: Dataworks sets standards and builds platform. Business functions apply AI to domain-specific problems. CDIO consolidates all.",
        4: "Lean named: 'FedEx Dataworks' is named but not branded as 'AI Lab.' CDIO title, Fortune AIQ 50 recognition. Named but not flashy.",
        5: "Lean short: operational AI deployed now, education program for near-term capability building. Academic partnerships (IIT) and robotics are longer horizon but secondary.",
    },
}

specimens_to_sync = ['anduril', 'blue-origin', 'lockheed-martin', 'delta-air-lines', 'fedex']
tension_map = {
    'structuralVsContextual': 1,
    'speedVsDepth': 2,
    'centralVsDistributed': 3,
    'namedVsQuiet': 4,
    'longVsShortHorizon': 5
}

for sid in specimens_to_sync:
    print(f"\n--- {sid} ---")
    spec = load_json(f'specimens/{sid}.json')
    tp = spec['tensionPositions']

    for field, tid in tension_map.items():
        pos = tp.get(field)
        if pos is not None and isinstance(pos, (int, float)):
            ev = evidence.get(sid, {}).get(tid, f"Position {pos} from specimen-level data.")
            add_to_tension(tid, sid, pos, ev)


# ═══════════════════════════════════════════════════════════
# STEP 2: Sync missing contingencies to central arrays
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 2: Sync missing contingencies to central arrays")
print("=" * 60)

# Contingency level normalization for central file keys
normalize = {
    'non-traditional': 'non-traditional',
    'nontraditional': 'nonTraditional',
    'talent-rich': 'talent-rich',
    'talent-constrained': 'talent-constrained',
    'long': 'high',
    'short': 'low',
    'new': 'new',
    'founder': 'founder',
    'slow': 'low',
    'fast': 'fast',
}

for sid in specimens_to_sync:
    print(f"\n--- {sid} ---")
    spec = load_json(f'specimens/{sid}.json')
    cont = spec.get('contingencies', {})

    for cid in ['regulatoryIntensity', 'timeToObsolescence', 'ceoTenure', 'talentMarketPosition', 'technicalDebt']:
        level = cont.get(cid)
        if level is not None:
            level_str = str(level).lower()
            level_normalized = normalize.get(level_str, level_str)
            add_to_contingency(cid, level_normalized, sid)


# ─── STEP 3: Update timestamps ───
from datetime import date
today = date.today().isoformat()
tensions_data['lastUpdated'] = today
contingencies_data['lastUpdated'] = today

# ─── Save central files ───
save_json('synthesis/tensions.json', tensions_data)
save_json('synthesis/contingencies.json', contingencies_data)

print("\n" + "=" * 60)
print("DONE. Batch 5 complete.")
print("  Removed 5 government specimens from synthesis files")
print("  Synced 5 defense/transport specimens to central arrays")
print("=" * 60)
