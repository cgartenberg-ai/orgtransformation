#!/usr/bin/env python3
"""
Batch 4: Automotive/Industrial specimens — 13 total.
- 9 specimens already have complete specimen-level data (5T, 5C) — sync to central arrays
- 4 specimens need scoring: tesla, hyundai-robotics, bosch-bcai, dow-chemical

Discoveries from this batch:
1. Automotive M4 Convergence: 10 of 13 are M4 hub-and-spoke. Strongest sector-level convergence in collection.
   Exceptions (Tesla M3, ExxonMobil M6b) confirm modularity hypothesis logic.
2. GM CAIO Failure: 8-month CAIO tenure is a natural experiment — tech-style hub fails without domain embedding.
3. Data Foundation First: ExxonMobil + Honeywell both solved data infra before scaling AI — sequencing constraint.
4. Physical AI as Distinct Category: Honeywell, Hyundai, Tesla, Deere all point to hardware-software AI needing
   different structural models than software-only AI.
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
    """Levels are DIRECT keys on contingency object (not nested under 'levels').
    Specimens can be plain strings OR {specimenId, rationale} dicts."""
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

def add_to_contingency(cid, level, sid, rationale):
    """Contingency levels are DIRECT keys on the contingency object."""
    c = find_contingency(cid)
    level_lower = level.lower()
    skip_keys = {'id', 'name', 'whatItDetermines'}

    # Find matching level key (case-insensitive)
    matched_key = None
    for k in c:
        if k in skip_keys:
            continue
        if k.lower() == level_lower:
            matched_key = k
            break

    if not matched_key:
        # Create the level if it doesn't exist
        c[level] = {'label': level, 'favors': [], 'mechanisms': [], 'specimens': []}
        matched_key = level
        print(f"  ! Created new level '{level}' for {cid}")

    if not specimen_in_contingency_level(c, matched_key, sid):
        # Match existing format: plain strings
        c[matched_key]['specimens'].append(sid)
        print(f"  + {cid}/{matched_key} {sid}")
    else:
        print(f"  = {cid}/{matched_key} {sid} already present")

# ─── Evidence strings for specimens that already have numeric positions ───

evidence = {
    'bmw': {
        1: "M4 hub (Project AI) + contextual goal ('nearly every process supported by AI'). +0.6 contextual-leaning despite structural hub.",
        2: "40,000 users on self-service GenAI platform, 450 DevOps teams — breadth-first deployment. +0.3 speed/width.",
        3: "Federated: central platform sets standards, BUs build applications. 'Democratized access' via self-service. Balanced at 0.0.",
        4: "Project AI and BCAI are named entities but no flashy CAIO or branded lab. -0.3 named-leaning.",
        5: "Mixed horizons: production AI (quarterly), Neue Klasse (2025-2027), autonomous campus (1,800 employees, long-term). -0.2 slight long lean."
    },
    'mercedes-benz': {
        1: "Textbook structural: MBRDNA (600+ employees) as dedicated global AI center, Digital Factory for manufacturing AI, separate CDAIO. -0.7 structural.",
        2: "Balanced: MB.OS enables fast iteration but CLA/S-Class launches on multi-year cycles. 0.0 balanced.",
        3: "Central architectural decisions via MB.OS, central CDAIO. Global hubs execute but under central standards. -0.3 central-leaning.",
        4: "Heavily branded: MBRDNA self-designates as 'global AI center,' CDAIO appointed, supervisory board AI expertise added. -0.8 strongly named.",
        5: "Near-term CLA launch (2026-2027), medium-term L4 robotaxi, long-term academic partnerships. 'Double-digit billion euros per year.' -0.2 slight long lean."
    },
    'toyota': {
        1: "Classic structural separation: TRI ($1B research), Enterprise AI (productivity), GAIA (bridge), Woven (startup). -0.7 structural.",
        2: "Deep-first: TRI pursues multi-year research breakthroughs. Enterprise AI pragmatic but measured. -0.3 depth-leaning.",
        3: "Federated: TRI has research autonomy, Enterprise AI has TMNA mandate, GAIA coordinates. Kursar bridges. +0.2 slightly distributed.",
        4: "Multiple named entities: TRI, GAIA, Woven. Public research presence. -0.6 named.",
        5: "Multi-horizon: TRI (3-10 year), Enterprise AI (near-term), manufacturing AI (deployed). Incoming CEO candidly admits trailing Tesla. -0.4 long-leaning."
    },
    'honda': {
        1: "Structural separation across three tiers: HRI (research institutes), American Honda IT (enterprise), Sony Honda Mobility JV (venture). -0.7 structural.",
        2: "Research-first orientation: HRI expanding to Ohio lab, quantum computing research. Enterprise adoption more cautious. -0.3 depth-leaning.",
        3: "Distributed: three separate governance structures (HRI, AHIT, SHM JV). No central CAIO. Regional autonomy pattern. +0.4 distributed.",
        4: "Named research institutes (HRI) and branded JV (AFEELA). -0.5 named.",
        5: "Long horizon: HRI fundamental research (quantum, robotics), AFEELA 2026-2028 production. -0.4 long-leaning."
    },
    'ford': {
        1: "Textbook structural: Latitude AI (550-person subsidiary with own C-suite), Greenfield Labs, FARIC, skunkworks. Ford+ divided into Model e/Blue/Pro. -0.7 structural.",
        2: "Deep pilots before wide deployment: Latitude AI pursuing eyes-off driving on long horizon. BlueCruise expanding incrementally. -0.3 depth-leaning.",
        3: "Highly distributed: multiple autonomous units (Latitude, Greenfield, FARIC, skunkworks) across divisions (Model e, Blue, Pro). +0.5 distributed.",
        4: "Latitude AI is a named, branded subsidiary with its own website, leadership team. -0.6 named.",
        5: "Latitude AI has 5-10 year autonomous driving horizon. Skunkworks for affordable EVs. CEO frames AI around long-term workforce transformation. -0.4 long-leaning."
    },
    'general-motors': {
        1: "M4 with structural elements: Silicon Valley CoE (<20), Autonomous Robotics Center (100+), separate software org under Sterling Anderson. -0.6 structural.",
        2: "Pragmatic speed: deploying AI across manufacturing now, Google Gemini launching 2026, but also deep autonomous work (eyes-off 2028). +0.3 slight speed lean.",
        3: "Shifting distributed: post-CAIO departure, AI being 'strategically integrated directly into business and product organizations.' +0.4 distributed-leaning.",
        4: "GM went from named CAIO role to quiet integration. No branded AI lab. +0.2 quiet-leaning now.",
        5: "Mixed: near-term manufacturing AI + medium-term conversational AI + long-term autonomous. Pragmatic staged approach. 0.0 balanced."
    },
    'deere-and-co': {
        1: "Hub-and-spoke via acquisitions: Blue River ($305M), Bear Flag ($250M) as distinct spokes. CTO Hindman as hub. -0.7 structural.",
        2: "Balanced: See & Spray already at 5M acres (deployed), but autonomous farming targets 2030. 0.0 balanced.",
        3: "CTO sets central standards, acquired units have technical autonomy. University innovation centers add distributed R&D. +0.3 slightly distributed.",
        4: "CTO as hub leader, Blue River and Bear Flag maintain identity. CES keynote presence. -0.3 named-leaning.",
        5: "Mixed: quarterly product improvements alongside 2030 autonomous vision. 'Smart Industrial' strategy 2019-2030. -0.4 long-leaning."
    },
    'honeywell': {
        1: "Hub-and-spoke with ambassador network. Central gen AI program leader + CDTO Jordan. -0.6 structural.",
        2: "Speed/breadth: 24 gen AI initiatives across 95K employees, ambassadors surfacing use cases from field. +0.3 speed-leaning.",
        3: "Top-down: Jordan's team prioritizes after ambassadors surface use cases. Six-chapter framework ensures consistency. -0.4 central.",
        4: "No branded AI lab. Ambassador model is deliberately low-profile. CDTO/CTO split but not flashy. +0.2 quiet-leaning.",
        5: "Mixed: near-term 24 production use cases, medium-term AI-embedded products, long-term 'automated to autonomous' vision. -0.3 slight long lean."
    },
    'exxonmobil': {
        1: "M6b unnamed/informal: 668 data scientists distributed, no CAIO, no branded AI center. AI through GBS and IT. +0.6 contextual-leaning.",
        2: "Deep: data foundation work preceding AI scaling. Seismic interpretation optimization (12-18 month timelines). -0.3 depth-leaning.",
        3: "Historically siloed, now pushing centralization via corporate-wide ERP. Technology consolidated in Houston hub. -0.2 slightly central.",
        4: "Quintessential quiet: no branded AI entity, no CAIO, AI embedded in operational budgets. +0.8 very quiet.",
        5: "CEO frames AI as 'long-term evolution.' $15B savings target by 2027 is near-term but data foundation is long investment. -0.4 long-leaning."
    }
}

# ─── Scores for the 4 problem specimens ───

problem_specimens = {
    'tesla': {
        'tensions': {
            1: (-0.4, "M3 Embedded/Contextual classification but with structural elements (Operation Maestro, distinct Autopilot/Optimus programs). Fleet-as-lab model defies clean separation."),
            2: (0.4, "Deploy-and-iterate: fleet as distributed lab, 1.5PB/week data processing, vision-only approach. Speed orientation with iteration depth."),
            3: (-0.6, "Heavily centralized under Musk. AI team is core central function. No spoke autonomy or federated decision-making."),
            4: (0.5, "No named AI lab or CAIO. AI IS the product — Tesla doesn't brand an 'AI Center,' it brands itself as AI. Quiet by integration."),
            5: (-0.6, "Extreme long-horizon bets: unsupervised FSD deadline, 50K Optimus target, $20B+ CapEx. First-ever revenue decline concurrent with AI pivot.")
        },
        'contingencies': {
            'regulatoryIntensity': ('high', "Automotive safety regulations (NHTSA, EU type approval) plus energy sector regulation."),
            'timeToObsolescence': ('medium', "EVs are augmented by AI but not obsoleted. Robotaxi/Optimus are new markets."),
            'ceoTenure': ('founder', "Musk as founder-CEO is THE singular driver. All AI strategy flows from his directives."),
            'talentMarketPosition': ('talent-rich', "Attracts top AI talent (ex-Google, ex-Meta) despite intense culture. Karpathy, Elluswamy pedigree."),
            'technicalDebt': ('low', "Built from scratch on software-first architecture. No legacy ERP, no supplier-integrated ECU stack.")
        }
    },
    'hyundai-robotics': {
        'tensions': {
            1: (-0.8, "Structural: Named Robotics LAB with dedicated mandate and resources, physically separate from core automotive operations."),
            2: (-0.5, "Deep: Physical AI with custom silicon (edge brain chip) is inherently deep/slow-iteration R&D. Hardware cycles."),
            3: (-0.4, "Central: Dedicated lab within larger conglomerate. Boston Dynamics also centrally managed. Not federated."),
            4: (-0.6, "Named: 'Robotics LAB' is explicitly branded, CES presence, public demonstrations."),
            5: (-0.6, "Long horizon: Physical AI and robotics are long-cycle investments. Edge brain chip just entering mass production.")
        },
        'contingencies': {
            'regulatoryIntensity': ('high', "Automotive safety + robotics safety regulations in multiple jurisdictions."),
            'timeToObsolescence': ('slow', "Physical manufacturing and automotive not easily obsoleted by software AI."),
            'ceoTenure': ('medium', "Chaebol governance structure, not one-person driven."),
            'talentMarketPosition': ('talent-constrained', "Robotics + automotive AI talent scarce. Competing with tech cos for embodied AI expertise."),
            'technicalDebt': ('medium', "Mix of legacy automotive systems and newer robotics/software infrastructure.")
        }
    },
    'bosch-bcai': {
        'tensions': {
            1: (-0.4, "Network model is structural but deliberately not a 'traditional centralized lab.' BCAI connects central research AND business divisions."),
            2: (0.0, "Mixed: CES 2026 demos show breadth (AI cockpits, manufacturing agents, connected appliances) alongside fundamental R&D."),
            3: (0.3, "Distributed-leaning: BCAI explicitly 'not a traditional centralized lab' but a network spanning research and business divisions."),
            4: (-0.5, "Named: BCAI is a branded, visible entity with CES presence and board-level leadership (Dr. Kessler)."),
            5: (-0.3, "Moderate long horizon: 2.5B euro investment by 2027, 10B+ euro software/sensor target by mid-2030s.")
        },
        'contingencies': {
            'regulatoryIntensity': ('high', "Automotive safety + industrial safety across Bosch's diversified portfolio. EU AI Act compliance."),
            'timeToObsolescence': ('slow', "Diversified industrial products (automotive, consumer, energy) not easily obsoleted."),
            'ceoTenure': ('medium', "Board-level AI leadership change (Dr. Kessler joining), but institutional governance."),
            'talentMarketPosition': ('talent-rich', "German engineering talent pipeline, 420K employees, strong R&D culture."),
            'technicalDebt': ('high', "Massive diversified legacy systems across automotive, industrial, consumer, energy divisions.")
        }
    },
    'dow-chemical': {
        'tensions': {
            4: (0.5, "Quiet: No named AI entity, no CAIO. AI framed through workforce restructuring ('reducing complexity, adopting best-available technologies') rather than named initiative.")
        },
        'contingencies': {
            'regulatoryIntensity': ('medium', "Chemical industry environmental and safety regulations, but not as intense as pharma or automotive."),
            'timeToObsolescence': ('slow', "Commodity chemicals not easily obsoleted by AI. Process optimization, not disruption."),
            'ceoTenure': ('medium', "Fitterling CEO since 2018 (~8 years), driving restructuring."),
            'talentMarketPosition': ('talent-constrained', "Chemicals/materials sector competes poorly for AI talent vs tech and pharma."),
            'technicalDebt': ('high', "Legacy industrial infrastructure, process control systems, capital-intensive plants.")
        }
    }
}

# ─── STEP 1: Sync specimens with complete specimen-level data to central arrays ───
print("=" * 60)
print("STEP 1: Sync 9 complete specimens to central arrays")
print("=" * 60)

complete_specimens = ['bmw', 'mercedes-benz', 'toyota', 'honda', 'ford',
                       'general-motors', 'deere-and-co', 'honeywell', 'exxonmobil']

for sid in complete_specimens:
    print(f"\n--- {sid} ---")
    spec = load_json(f'specimens/{sid}.json')
    tp = spec['tensionPositions']
    cont = spec['contingencies']

    tension_map = {
        'structuralVsContextual': 1,
        'speedVsDepth': 2,
        'centralVsDistributed': 3,
        'namedVsQuiet': 4,
        'longVsShortHorizon': 5
    }

    for field, tid in tension_map.items():
        pos = tp.get(field)
        if pos is not None and isinstance(pos, (int, float)):
            ev = evidence.get(sid, {}).get(tid, f"Position {pos} from specimen-level data.")
            add_to_tension(tid, sid, pos, ev)

    # Contingencies — normalize level names to match central array keys
    cont_map = {
        'regulatoryIntensity': cont.get('regulatoryIntensity'),
        'timeToObsolescence': cont.get('timeToObsolescence'),
        'ceoTenure': cont.get('ceoTenure'),
        'talentMarketPosition': cont.get('talentMarketPosition'),
        'technicalDebt': cont.get('technicalDebt')
    }

    for cid, level in cont_map.items():
        if level is not None:
            level_str = str(level).lower()
            # Normalize to match existing keys in contingencies.json
            normalize = {
                'non-traditional': 'non-traditional',
                'nontraditional': 'nonTraditional',
                'talent-rich': 'talent-rich',
                'talent-constrained': 'talent-constrained',
                'long': 'high',
                'short': 'low',
                'founder-era': 'founder',
                'slow': 'low',
                'fast': 'fast',
            }
            level_normalized = normalize.get(level_str, level_str)
            add_to_contingency(cid, level_normalized, sid, f"From specimen-level data: {level}")

# ─── STEP 2: Score and add the 4 problem specimens ───
print("\n" + "=" * 60)
print("STEP 2: Score 4 problem specimens")
print("=" * 60)

for sid, data in problem_specimens.items():
    print(f"\n--- {sid} ---")
    spec = load_json(f'specimens/{sid}.json')

    tension_field_map = {1: 'structuralVsContextual', 2: 'speedVsDepth', 3: 'centralVsDistributed',
                          4: 'namedVsQuiet', 5: 'longVsShortHorizon'}

    for tid, (pos, ev) in data['tensions'].items():
        field = tension_field_map[tid]
        # Update specimen file
        if spec['tensionPositions'].get(field) is None or not isinstance(spec['tensionPositions'].get(field), (int, float)):
            spec['tensionPositions'][field] = pos
            print(f"  specimen.{field} = {pos}")
        # Add to central array
        add_to_tension(tid, sid, pos, ev)

    # Update specimen-level contingencies
    for cid, (level, rationale) in data['contingencies'].items():
        if spec['contingencies'].get(cid) is None:
            # Pretty-print for specimen file
            if cid == 'talentMarketPosition':
                case_map = {'talent-rich': 'Talent-rich', 'talent-constrained': 'Talent-constrained',
                            'nontraditional': 'Non-traditional', 'non-traditional': 'Non-traditional'}
                spec['contingencies'][cid] = case_map.get(level, level.capitalize())
            elif cid == 'ceoTenure':
                case_map = {'founder': 'Founder', 'high': 'Long', 'medium': 'Medium', 'low': 'Short', 'new': 'New'}
                spec['contingencies'][cid] = case_map.get(level, level.capitalize())
            else:
                spec['contingencies'][cid] = level.capitalize()
            print(f"  specimen.{cid} = {spec['contingencies'][cid]}")

        # Add to central array — normalize level for central keys
        normalize = {
            'non-traditional': 'non-traditional',
            'nontraditional': 'nonTraditional',
            'talent-rich': 'talent-rich',
            'talent-constrained': 'talent-constrained',
            'long': 'high',
            'short': 'low',
            'founder-era': 'founder',
            'slow': 'low',
            'fast': 'fast',
        }
        level_normalized = normalize.get(level, level)
        add_to_contingency(cid, level_normalized, sid, rationale)

    # Save specimen
    save_json(f'specimens/{sid}.json', spec)
    print(f"  Saved {sid}.json")

# ─── STEP 3: Update timestamps ───
from datetime import date
today = date.today().isoformat()
tensions_data['lastUpdated'] = today
contingencies_data['lastUpdated'] = today

# ─── Save central files ───
save_json('synthesis/tensions.json', tensions_data)
save_json('synthesis/contingencies.json', contingencies_data)

print("\n" + "=" * 60)
print("DONE. Batch 4 complete.")
print(f"Synced 9 complete specimens + scored 4 problem specimens")
print(f"Total: 13 automotive/industrial specimens placed")
print("=" * 60)
