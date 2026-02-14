#!/usr/bin/env python3
"""
Batch 6: Media/Consumer cluster — 9 specimens.

All 9 specimens have tensions already placed in central arrays (except
lionsgate T2/T5 which are null stubs). Main gap: ALL 9 are missing from
contingency arrays.

Specimens:
- disney (M4/Structural, media/entertainment)
- netflix (M4/Contextual, streaming)
- lionsgate (M2/Structural, film/TV — stub)
- washington-post (M6/Temporal, news — stub)
- kroger (M4/Structural, grocery retail)
- lowes (M4/Structural, home improvement)
- nike (M4/Contextual, apparel)
- pepsico (M4/Contextual, consumer goods)
- ulta-beauty (M4/Contextual, beauty retail)

Key observations:
1. Disney vs Netflix: same industry, different modularity → different orientation
   (Disney integral/Structural, Netflix modular/Contextual)
2. "Data foundation first" extends to retail (PepsiCo SAP, Ulta SOAR, Kroger 84.51°)
3. M4/Contextual concentration: consumer firms expect everyone to use AI (PepsiCo 330K training)
4. Nike CTO elimination: AI becoming infrastructure, not strategy
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


# ═══════════════════════════════════════════════════════════
# STEP 1: Sync contingencies from specimen files to central
# ═══════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 1: Sync contingencies to central arrays")
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
    'medium': 'medium',
    'high': 'high',
    'low': 'low',
    'critical': 'critical',
}

batch6_specimens = [
    'disney', 'netflix', 'lionsgate', 'washington-post',
    'kroger', 'lowes', 'nike', 'pepsico', 'ulta-beauty'
]

# Nike C5 is null in specimen file — score it Medium based on analysis:
# 4 acquisitions (2018-2021), 1,000+ cobots, major restructuring suggest
# integration challenges but not legacy-industrial levels of debt
nike_c5_override = 'Medium'

for sid in batch6_specimens:
    print(f"\n--- {sid} ---")
    spec = load_json(f'specimens/{sid}.json')
    cont = spec.get('contingencies', {})

    for cid in ['regulatoryIntensity', 'timeToObsolescence', 'ceoTenure', 'talentMarketPosition', 'technicalDebt']:
        level = cont.get(cid)

        # Apply Nike C5 override
        if sid == 'nike' and cid == 'technicalDebt' and level is None:
            level = nike_c5_override

        if level is not None:
            level_str = str(level).lower()
            level_normalized = normalize.get(level_str, level_str)
            add_to_contingency(cid, level_normalized, sid)
        else:
            print(f"  ~ {cid} is null for {sid} — skipping (stub policy)")


# ═══════════════════════════════════════════════════════════
# STEP 2: Verify tensions are already in central arrays
# (Audit showed they're all there except lionsgate T2/T5 nulls)
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 2: Verify tensions present (no-op sync)")
print("=" * 60)

tension_map = {
    'structuralVsContextual': 1,
    'speedVsDepth': 2,
    'centralVsDistributed': 3,
    'namedVsQuiet': 4,
    'longVsShortHorizon': 5
}

evidence = {
    'disney': {
        1: "M4/Structural: OTE governs standards, Research Studios separate, BU execution distributed. Three-layer architecture with structural separation.",
        2: "Lean fast with Sora integration for FY2026. But Research Studios has 16-year horizon. Mixed velocity.",
        3: "Distributed: OTE 'does NOT take over or centralize' BU AI. BUs retain decision rights. Hub enables, doesn't command.",
        4: "Named: Disney Research Studios, Office of Technology Enablement, $1B OpenAI partnership. Multiple branded AI initiatives.",
        5: "Mixed: Research Studios multi-year horizon, Sora integration near-term, OTE medium-term governance build-out.",
    },
    'netflix': {
        1: "M4/Contextual: research explicitly NOT centralized. 9 research areas distributed across business. Researchers work 'in close collaboration with business teams.'",
        2: "Lean fast: experimentation culture, rapid deployment. El Eternauta VFX 10x faster. AIMS handles production at 325M member scale.",
        3: "Distributed: research explicitly NOT centralized. Teams distributed across 9 areas. But AIMS and Eyeline are specialized hubs. Lean distributed.",
        4: "Quiet: no CAIO, no branded AI lab. CPTO owns everything. AI capabilities named functionally (AIMS, Eyeline) not branded organizationally.",
        5: "Balanced: AIMS works on production models (quarterly), Eyeline on longer-horizon VFX research. Ads AI is near-term revenue driver.",
    },
    'lionsgate': {
        1: "M2/Structural: first CAIO hire signals centralized governance/enablement. Early-stage structural separation.",
        3: "Centralized: single CAIO for entire studio. Governance/enablement model, not distributed.",
        4: "Named: first CAIO in Hollywood, deliberate C-suite branding. Framing AI as 'serving creative vision.'",
    },
    'washington-post': {
        2: "Lean fast: ~1/3 workforce cut in AI-oriented restructuring. Speed of transformation is extreme. No evidence of deliberate piloting.",
        4: "Quiet: no branded AI lab or CAIO. Restructuring framed as organizational pivot, not AI branding exercise.",
        5: "Short: restructuring driven by immediate existential pressure. Subscription reorientation is near-term survival strategy.",
    },
    'kroger': {
        1: "M4/Structural: 84.51° is legally separate subsidiary (hub), BUs are spokes. AI Factory provides central infrastructure.",
        2: "Lean fast: 84.51° AI Factory scales reusable components. Agent Barney, agentic search deployed. Multiple operational wins already.",
        3: "Balanced: 84.51° hub sets governance, AI Governance Council oversees. BUs develop AI closest to their problems within guardrails.",
        4: "Named: '84.51° AI Factory' is explicitly branded. Named hub with clear identity. But not flashy CEO-driven narrative.",
        5: "Lean short: quarterly operational wins (shrink, pricing) + medium-term connected intelligence vision.",
    },
    'lowes': {
        1: "M4/Structural: Innovation Labs (Kirkland) separate from core. AI Transformation Office governance. Charlotte Tech Hub CoE. Multiple structural layers.",
        2: "Lean fast: OpenAI 100B token milestone, Mylow 1M questions/month, 2x conversion. Deployed at scale. But Innovation Labs is 2-5 year horizon.",
        3: "Central governance: AI Transformation Office vets every use case (4-metric framework). Innovation Labs and Charlotte Hub are centrally managed.",
        4: "Named: Innovation Labs, Mylow, AI Transformation Office. Multiple branded entities. Ellison speaks at conferences about AI.",
        5: "Balanced: Innovation Labs 2-5 year horizon, AI Transformation Office quarterly, store rollouts monthly. Multi-horizon.",
    },
    'nike': {
        1: "M4/Contextual: CDAIO leads central function, but emphasis on 'embedding digital, data and AI across the business.' CTO eliminated, tech under COO.",
        2: "Lean fast: acquisitions deployed, 1,000+ cobots operational. But Gen AI initiative lost leadership. Mixed velocity.",
        3: "Lean distributed: regional leaders elevated to senior leadership team. CDAIO provides central capability but operations drive execution.",
        4: "Quiet: CDAIO exists but no branded AI lab. CTO eliminated. AI framed as operational enabler, not strategic differentiator.",
        5: "Lean short: operational focus (cobots, personalization, supply chain). NSRL is longer-term but not AI-specific.",
    },
    'pepsico': {
        1: "M4/Contextual: central CSTO team (700-1,000) sets standards, but training all 330,000 employees on AI. Contextual orientation with hub structure.",
        2: "Lean fast: record productivity targets for 2026, agentic AI deployment planned, PepGenX experimentation platform. But SAP rollout is multi-year foundation.",
        3: "Balanced: 'four or five big bets' with central governance (AI Council) + mission-based teams with execution autonomy.",
        4: "Named: Digital Hubs (Dallas, Barcelona), CSTO role, AI Council. Named structure but not flashy consumer-facing branding.",
        5: "Lean short: record productivity savings target, but Stanford HAI partnership and digital twins are longer-horizon. Mixed.",
    },
    'ulta-beauty': {
        1: "M4/Contextual: AI Center of Excellence develops capabilities, but AI embedded throughout (supply chain, marketing, associates). CEO: 'way of being.'",
        2: "Lean fast: GlamLab deployed to 46.3M loyalty members, ship-from-store 1,000+ locations, double-digit e-commerce growth. Scaling ahead of full optimization.",
        3: "Lean distributed: CoE develops capabilities, but application distributed to Digital Innovation, Supply Chain, Marketing teams.",
        4: "Named: AI Center of Excellence, GlamLab, Prisma Ventures. Named but not CEO-led AI narrative. CTTO and CDO co-own.",
        5: "Balanced: near-term AI deployment + agentic AI development for 2026. CEO: 'no finish line' in tech investment.",
    },
}

for sid in batch6_specimens:
    print(f"\n--- {sid} ---")
    spec = load_json(f'specimens/{sid}.json')
    tp = spec['tensionPositions']

    for field, tid in tension_map.items():
        pos = tp.get(field)
        if pos is not None and isinstance(pos, (int, float)):
            ev = evidence.get(sid, {}).get(tid, f"Position {pos} from specimen-level data.")
            add_to_tension(tid, sid, pos, ev)
        else:
            print(f"  ~ T{tid} {sid} is null — skipping")


# ─── STEP 3: Update timestamps ───
from datetime import date
today = date.today().isoformat()
tensions_data['lastUpdated'] = today
contingencies_data['lastUpdated'] = today

# ─── Save central files ───
save_json('synthesis/tensions.json', tensions_data)
save_json('synthesis/contingencies.json', contingencies_data)

print("\n" + "=" * 60)
print("DONE. Batch 6 complete.")
print("  Synced 9 media/consumer specimens to contingency arrays")
print("  Verified tensions already present in central arrays")
print("  Filled Nike C5=Medium (was null)")
print("=" * 60)
