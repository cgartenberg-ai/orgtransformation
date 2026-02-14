#!/usr/bin/env python3
"""
Batch 9 synthesis patch — Enterprise Software specimens
Adds: 3 new insights, C6 contingency, tension/contingency placements for 6 specimens
"""

import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(path):
    with open(os.path.join(ROOT, path), 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(os.path.join(ROOT, path), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

TODAY = date.today().isoformat()

# ============================================================
# 1. INSIGHTS — Add 3 new insights
# ============================================================

insights = load_json('synthesis/insights.json')

new_insights = [
    {
        "id": "inverse-grove",
        "title": "The Inverse Grove: When Leaders Outrun Their Organizations at Strategic Inflection Points",
        "theme": "mechanism",
        "maturity": "hypothesis",
        "finding": "Grove's original inflection point problem (Only the Paranoid Survive, 1996) described headquarters ignoring bottom-up signals from front-line employees who had already adapted to the new reality. In the AI era, the problem has inverted: CEOs who have internalized Grove and Christensen are pushing AI transformation top-down faster than their organizations, customers, and products can absorb it. The chaos comes from the opposite direction — headquarters manufacturing urgency faster than the market requires. This may be a specifically 2020s phenomenon because Grove's book became a Silicon Valley bible, causing leaders to overcorrect from 'too slow' to 'too fast.'",
        "evidence": [
            {
                "specimenId": "salesforce",
                "note": "Benioff declares 'digital labor revolution,' cuts 4,000 support staff, launches AgentExchange for '$6T digital labor market.' But customers are going through their own uncertain transformations, Agentforce needed deterministic Agent Script recalibration (quality issues), and sales incentives are structured around legacy CRM products. Headquarters is moving faster than front lines and customers."
            },
            {
                "specimenId": "klarna",
                "note": "Friis pushed AI-driven customer service replacement aggressively from the top. Quality degraded. CEO publicly acknowledged the reversal and resumed human hiring. Clearest case of inverse Grove: leadership outran product readiness."
            },
            {
                "specimenId": "meta-ai",
                "note": "Zuckerberg pushed metaverse pivot top-down before technology or market was ready ($70B losses). Then pivoted again to LLMs with 5th restructuring. Serial top-down inflection point management where headquarters repeatedly outpaces organizational readiness."
            },
            {
                "specimenId": "bmw",
                "note": "Zipse pushing Neue Klasse from the top with zero survival rhetoric. Dealers, factory workers, suppliers being pulled along by CEO conviction, not pushing change. Headquarters commitment is absolute; front-line readiness is uncertain."
            }
        ],
        "theoreticalConnection": "Grove (1996): strategic inflection points are recognized bottom-up. The inverse: when leaders internalize Grove's lesson, they act preemptively on inflection points, creating a top-down mandate that outpaces bottom-up readiness. The pathology shifts from 'ignored signals' to 'manufactured urgency.' Connects to March (1991) exploration-exploitation: leaders overweight exploration because they've been taught that exploitation-bias is fatal, but premature exploration commitment is equally dangerous when the technology or market isn't ready. Also connects to Christensen (1997) overcorrection: leaders who fear being disrupted may over-invest in disruption before the sustaining technology has matured.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch9-placement.md",
        "relatedMechanisms": [1, 5],
        "relatedTensions": [2, 5],
        "relatedInsights": ["speed-depth-trap", "product-production-convergence"],
        "watchFor": "Test across the collection: which specimens show headquarters pushing AI faster than front lines want? Which show the original Grove (front lines ahead, headquarters behind)? The distinguishing factor may be environmental AI pull — high pull environments (cybersecurity, defense) produce original Grove problems, low pull environments (retail, media) produce inverse Grove problems."
    },
    {
        "id": "ai-infrastructure-vs-actor-counter-positioning",
        "title": "AI-as-Infrastructure vs. AI-as-Actor: Competitive Counter-Positioning on Organizational Philosophy",
        "theme": "organizational-form",
        "maturity": "emerging",
        "finding": "In every industry undergoing AI transformation, firms counter-position on whether AI should be invisible infrastructure embedded in existing processes (AI-as-infrastructure) or a visible, named actor that replaces or augments human roles (AI-as-actor). This is not random variation but competitive differentiation on organizational philosophy. The two strategies have different failure modes: AI-as-actor risks the inverse Grove (pushing too fast, product not ready); AI-as-infrastructure risks the original Grove (embedding so invisibly that the organization never develops transformation urgency).",
        "evidence": [
            {
                "specimenId": "sap",
                "note": "Klein's 'no apps, no data, no AI' philosophy: AI must be deeply embedded in business processes. Joule is invisible infrastructure woven into S/4HANA, SuccessFactors, Ariba. AI-as-infrastructure strategy. Failure mode: insufficient ambition, original Grove."
            },
            {
                "specimenId": "salesforce",
                "note": "Benioff's 'digital labor revolution': Agentforce is a visible, named agent that replaces human labor. Has a name, a persona, a marketplace (AgentExchange). AI-as-actor strategy. Failure mode: premature commitment, inverse Grove."
            },
            {
                "specimenId": "bmw",
                "note": "'We ARE the Neue Klasse' — AI disappears into the car's identity. Zero separate AI branding. AI-as-infrastructure. Counter-positions against Tesla."
            },
            {
                "specimenId": "tesla",
                "note": "Autonomous driving, Optimus robot, xAI — AI IS the explicitly named product. AI-as-actor. Counter-positions against BMW."
            },
            {
                "specimenId": "roche-genentech",
                "note": "Regev: AI transforms the drug discovery PROCESS ('engineering, not science'). AI changes what scientists do. AI-as-infrastructure applied to R&D."
            },
            {
                "specimenId": "moderna",
                "note": "100% AI adoption, every role augmented. AI transforms the WORKFORCE composition. AI-as-actor — each person's role is visibly changed."
            },
            {
                "specimenId": "jpmorgan",
                "note": "Dimon pulled AI out of technology — 'too important.' AI as strategic asset with named leadership (Heitsenrether + Veloso). AI-as-actor."
            },
            {
                "specimenId": "goldman-sachs",
                "note": "AI Champions from business divisions, multi-vendor, no CAIO. AI embedded as operational tooling without named organizational identity. AI-as-infrastructure."
            }
        ],
        "theoreticalConnection": "Competitive counter-positioning (Hamilton, 2003; Casadesus-Masanell & Zhu, 2013): firms choose strategies that are optimally different from competitors, not optimally effective in isolation. The AI-as-infrastructure vs AI-as-actor axis may reflect a fundamental tradeoff between integration depth (infrastructure) and transformation speed (actor). Connects to our tight-coupling-modularity-constraint: tightly-coupled organizations (Apple, BMW) naturally gravitate toward infrastructure positioning because they can't easily modularize a visible AI actor without disrupting coordination.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch9-placement.md",
        "relatedMechanisms": [1, 5],
        "relatedTensions": [1, 4],
        "relatedInsights": ["inverse-grove", "tight-coupling-modularity-constraint"],
        "watchFor": "Map every industry to its infrastructure/actor positioning. Is one strategy systematically more successful? Does the optimal strategy depend on environmental AI pull (C6)? Industries with high pull (cybersecurity, defense) may need actor positioning; low pull (retail, traditional manufacturing) may benefit from infrastructure positioning."
    },
    {
        "id": "dual-tempo-ai-structures",
        "title": "Dual-Tempo AI Structures: Temporal Ambidexterity Without Structural Separation",
        "theme": "organizational-form",
        "maturity": "emerging",
        "finding": "Some organizations resolve the speed-vs-depth tension by splitting AI mandates at different time horizons within a single organizational unit, rather than creating structurally separate exploration units. Two leaders or teams handle 'today's AI' (operational deployment, tight product feedback loops) and 'tomorrow's AI' (forward-looking innovation, longer horizons) while sharing the same engineering organization. This achieves temporal ambidexterity without the coordination costs of structural separation.",
        "evidence": [
            {
                "specimenId": "crowdstrike",
                "note": "CTO Zaitsev handles operational AI/ML (Charlotte AI, APEX classifier, threat detection) while CTIO Ionescu handles forward-looking technology innovation. Both sit within the engineering org, both report up the same chain, but the mandate split creates temporal separation without organizational separation."
            },
            {
                "specimenId": "uber",
                "note": "Uber AI Labs (Ghahramani, research frontier, long-horizon) operates alongside embedded AI in the marketplace (matching, routing, pricing — immediate operational). Two AI mandates at different time horizons within the same company."
            }
        ],
        "theoreticalConnection": "O'Reilly & Tushman (2004) structural ambidexterity requires organizational separation. This pattern suggests a lighter-weight alternative: mandate separation within shared structure. The mechanism works when tacit information at interfaces is high (CrowdStrike: threat intelligence must flow instantly) — structural separation would break the feedback loop, so temporal separation via mandate-splitting is the feasible alternative. Connects to two-dimensions-of-tacit-information hypothesis.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch9-placement.md",
        "relatedMechanisms": [1, 3],
        "relatedTensions": [1, 2],
        "relatedInsights": ["two-dimensions-of-tacit-information", "tight-coupling-modularity-constraint"],
        "watchFor": "Other M3 specimens with dual-tempo patterns. Does this only work in environments with high interface tacitness (cybersecurity, real-time platforms) or can it work in slower-cycle industries?"
    }
]

# Check for duplicates
existing_ids = {i['id'] for i in insights['insights']}
for ni in new_insights:
    if ni['id'] not in existing_ids:
        insights['insights'].append(ni)
        print(f"  Added insight: {ni['id']}")
    else:
        print(f"  SKIPPED (exists): {ni['id']}")

insights['lastUpdated'] = TODAY
save_json('synthesis/insights.json', insights)
print(f"insights.json updated: {len(insights['insights'])} total insights")

# ============================================================
# 2. CONTINGENCIES — Add C6 (Environmental AI Pull) + place Batch 9 specimens
# ============================================================

contingencies = load_json('synthesis/contingencies.json')

# Check if C6 already exists
existing_c_ids = {c['id'] for c in contingencies['contingencies']}

if 'environmentalAiPull' not in existing_c_ids:
    c6 = {
        "id": "environmentalAiPull",
        "name": "Environmental AI Pull",
        "whatItDetermines": "How strongly the external environment (competitors, adversaries, customers, regulators) demands AI adoption, independent of internal leadership conviction. Predicts whether the primary organizational risk is the original Grove (too slow in high-pull environments) or the inverse Grove (too fast in low-pull environments).",
        "high": {
            "label": "High environmental AI pull (adversaries/competitors actively using AI, customers demanding AI)",
            "favors": [
                "Fast iteration cycles",
                "Embedded AI (M3) for tight feedback loops",
                "Speed over depth in tension resolution",
                "Original Grove risk (org may be too slow)"
            ],
            "mechanisms": [3, 5],
            "specimens": [
                "crowdstrike",
                "anduril",
                "lockheed-martin",
                "goldman-sachs",
                "morgan-stanley",
                "jpmorgan"
            ]
        },
        "medium": {
            "label": "Medium environmental AI pull (industry in transition, mixed customer readiness)",
            "favors": [
                "Hub-and-spoke (M4) with both exploration and execution",
                "Balanced speed-depth tradeoff",
                "Risk of either Grove variant depending on leadership"
            ],
            "specimens": [
                "salesforce",
                "sap",
                "hp-inc",
                "pfizer",
                "roche-genentech",
                "bmw",
                "toyota"
            ]
        },
        "low": {
            "label": "Low environmental AI pull (customers don't demand AI, competitors not yet AI-driven)",
            "favors": [
                "Infrastructure positioning (AI-as-invisible)",
                "Contextual integration over structural separation",
                "Inverse Grove risk (leadership may outrun market)",
                "AI-washing risk (announcements without structural change)"
            ],
            "specimens": [
                "nike",
                "pinterest",
                "workday",
                "kroger",
                "ulta-beauty",
                "ford"
            ]
        }
    }
    contingencies['contingencies'].append(c6)
    print("  Added C6: environmentalAiPull")
else:
    print("  SKIPPED C6 (exists)")

# Place Batch 9 specimens in existing contingencies
batch9_placements = {
    "salesforce": {
        "regulatoryIntensity": "low",
        "timeToObsolescence": "fast",
        "ceoTenure": "founder",
        "talentMarketPosition": "talent-rich"
    },
    "sap": {
        "regulatoryIntensity": "medium",
        "timeToObsolescence": "medium",
        "ceoTenure": "medium",
        "talentMarketPosition": "talent-rich"
    },
    "crowdstrike": {
        "regulatoryIntensity": "medium",
        "timeToObsolescence": "fast",
        "ceoTenure": "founder",
        "talentMarketPosition": "talent-rich"
    },
    "hp-inc": {
        "regulatoryIntensity": "low",
        "timeToObsolescence": "medium",
        "ceoTenure": "short",
        "talentMarketPosition": "talent-constrained"
    },
    "pinterest": {
        "regulatoryIntensity": "low",
        "timeToObsolescence": "fast",
        "ceoTenure": None,  # skip
        "talentMarketPosition": "talent-constrained"
    },
    "workday": {
        "regulatoryIntensity": "low",
        "timeToObsolescence": "fast",
        "ceoTenure": None,  # skip
        "talentMarketPosition": "talent-constrained"
    }
}

for c in contingencies['contingencies']:
    cid = c['id']
    if cid == 'environmentalAiPull':
        continue  # already placed above
    if cid == 'technicalDebt':
        continue  # skip — not placing in central file for this batch
    for specimen_id, placements in batch9_placements.items():
        if cid in ['regulatoryIntensity', 'timeToObsolescence', 'ceoTenure', 'talentMarketPosition']:
            level = placements.get(cid)
            if level is None:
                continue
            # Find the right level bucket
            for level_key in ['high', 'medium', 'low', 'fast', 'slow', 'founder', 'short', 'long',
                              'talent-rich', 'talent-constrained', 'non-traditional', 'nonTraditional']:
                if level_key in c and level_key == level:
                    specimens_list = c[level_key].get('specimens', [])
                    if specimen_id not in specimens_list:
                        specimens_list.append(specimen_id)
                        c[level_key]['specimens'] = specimens_list

contingencies['lastUpdated'] = TODAY
save_json('synthesis/contingencies.json', contingencies)
print(f"contingencies.json updated")

# ============================================================
# 3. TENSIONS — Place Batch 9 specimens
# ============================================================

tensions = load_json('synthesis/tensions.json')

batch9_tensions = {
    "salesforce": {
        "structuralVsContextual": {"position": -0.5, "evidence": "Agentforce as central hub, structurally separated AI budget ($300M), dedicated Chief AI & Transformation Officer. 4,000 support staff redeployed. Strong structural separation between AI-driven operations and legacy functions."},
        "speedVsDepth": {"position": 0.3, "evidence": "Deployed Agentforce on help.salesforce.com before scaling to 9,500 enterprise customers. Speed-first but Agent Script recalibration shows depth corrections needed."},
        "centralVsDistributed": {"position": -0.4, "evidence": "Agentforce platform centrally developed. AgentExchange marketplace centrally managed. Eric Hysen as central transformation officer."},
        "namedVsQuiet": {"position": -0.7, "evidence": "Agentforce has its own brand, logo, marketplace. 'Digital labor revolution' language. CEO publicly claims 4,000 jobs replaced. Most loudly named AI capability in the collection."},
        "longVsShortHorizon": {"position": -0.2, "evidence": "'$6 trillion digital labor market' long-term framing, but quarterly Agentforce ARR metrics and deployment speed suggest near-term execution focus."}
    },
    "sap": {
        "structuralVsContextual": {"position": -0.2, "evidence": "Joule built centrally but embedded invisibly across product lines. 'No apps, no data, no AI' philosophy demands integration. Structural hub with contextual philosophy."},
        "speedVsDepth": {"position": 0.0, "evidence": "Quarterly product releases with AI features, but 2-year vision for no-manual-data-entry. Balanced speed and depth."},
        "centralVsDistributed": {"position": -0.3, "evidence": "Joule developed centrally, distributed across S/4HANA, SuccessFactors, Ariba. Central AI team with distributed embedding."},
        "namedVsQuiet": {"position": -0.3, "evidence": "Joule is named and branded, but Klein's philosophy positions AI as invisible process improvement, not standalone. Named product, quiet philosophy."},
        "longVsShortHorizon": {"position": 0.2, "evidence": "2-year no-manual-entry vision, but RISE deals and quarterly AI adoption metrics drive near-term. Slight short-horizon lean."}
    },
    "crowdstrike": {
        "structuralVsContextual": {"position": 0.2, "evidence": "AI embedded within CTO engineering org (M3), no separate AI unit. But CTO/CTIO split creates some structural differentiation within the embedded model."},
        "speedVsDepth": {"position": -0.3, "evidence": "Charlotte AI multi-agent architecture represents depth investment (12+ specialized agents, Enterprise Graph backbone). But adversarial environment demands real-time speed. Depth-leaning due to architectural sophistication."},
        "centralVsDistributed": {"position": -0.4, "evidence": "CTO Zaitsev centralizes AI/ML, data science, malware research. Not distributed across business units."},
        "namedVsQuiet": {"position": 0.3, "evidence": "Charlotte AI is named and branded, but no CAIO, no separate AI division. CTO carries AI mandate without AI-specific title. Moderately quiet."},
        "longVsShortHorizon": {"position": 0.2, "evidence": "'Security AGI' aspiration is long-horizon, but quarterly product releases and adversarial pressure demand near-term delivery. Slight short-horizon lean."}
    },
    "hp-inc": {
        "structuralVsContextual": {"position": -0.3, "evidence": "Three structurally distinct AI pillars (HP IQ, HP Labs, divisional embedding). HP IQ ring-fenced from divisional cycles. Clear structural separation."},
        "speedVsDepth": {"position": 0.2, "evidence": "AI PC penetration targets (30%→50%) prioritize speed-to-market. HP IQ formed quickly via $116M acqui-hire rather than organic R&D. Speed-leaning."},
        "centralVsDistributed": {"position": -0.1, "evidence": "Company-wide AI program reports to CEO, but three semi-autonomous pillars. Mild central coordination with distributed execution."},
        "namedVsQuiet": {"position": -0.4, "evidence": "HP IQ and HP Labs are named entities. Company-wide AI program. CES and Amplify events showcase AI. Named and visible."},
        "longVsShortHorizon": {"position": 0.1, "evidence": "FY2028 savings target (3-year), but AI PC penetration on 1-year cycle. HP IQ product development on 1-2 year horizon. Balanced with slight short lean."}
    },
    "pinterest": {
        "structuralVsContextual": {"position": 0.5, "evidence": "No dedicated AI lab, CAIO, or CoE. M6a with low confidence. Contextual/undifferentiated."},
        "speedVsDepth": {"position": 0.5, "evidence": "Speed-oriented: 15% layoffs for 'AI pivot' with minimal evidence of depth investment in AI capability building."},
        "centralVsDistributed": {"position": 0.3, "evidence": "No observable central AI function. Enterprise-wide reallocation without central coordination structure."},
        "namedVsQuiet": {"position": 0.6, "evidence": "Pinterest Assistant named product, but no named AI organizational unit. AI-washing question valid."},
        "longVsShortHorizon": {"position": 0.5, "evidence": "Restructuring plan through Sept 2026. Short-horizon cost management framing."}
    },
    "workday": {
        "structuralVsContextual": {"position": 0.5, "evidence": "No dedicated AI lab, CAIO, or CoE. M6a with low confidence. Contextual/undifferentiated."},
        "speedVsDepth": {"position": 0.5, "evidence": "Speed-oriented restructuring framing. No evidence of depth AI capability investment."},
        "centralVsDistributed": {"position": 0.3, "evidence": "No observable central AI function."},
        "namedVsQuiet": {"position": 0.7, "evidence": "CEO cites 'AI demand' in restructuring memo but no named AI organizational unit or leader. Quietest enterprise software specimen."},
        "longVsShortHorizon": {"position": 0.5, "evidence": "Restructuring charges and workforce reduction. Short-horizon financial management."}
    }
}

for t in tensions['tensions']:
    tid = t['id']
    field = t['fieldName']
    specimens_list = t.get('specimens', [])

    for specimen_id, tension_data in batch9_tensions.items():
        if field in tension_data:
            entry = {
                "specimenId": specimen_id,
                "position": tension_data[field]["position"],
                "evidence": tension_data[field]["evidence"]
            }
            # Check if already placed
            existing_ids = [s['specimenId'] for s in specimens_list if isinstance(s, dict)]
            if specimen_id not in existing_ids:
                specimens_list.append(entry)

    t['specimens'] = specimens_list

tensions['lastUpdated'] = TODAY
save_json('synthesis/tensions.json', tensions)
print(f"tensions.json updated")

# ============================================================
# 4. Update Salesforce specimen — fill null contingencies and tensions
# ============================================================

sf = load_json('specimens/salesforce.json')
sf['contingencies'] = {
    "regulatoryIntensity": "Low",
    "timeToObsolescence": "Fast",
    "ceoTenure": "Founder",
    "talentMarketPosition": "Talent-rich",
    "technicalDebt": "Medium"
}
sf['tensionPositions'] = {
    "structuralVsContextual": -0.5,
    "speedVsDepth": 0.3,
    "centralVsDistributed": -0.4,
    "namedVsQuiet": -0.7,
    "longVsShortHorizon": -0.2
}
sf['meta']['lastUpdated'] = TODAY
save_json('specimens/salesforce.json', sf)
print("salesforce.json updated with tensions + contingencies")

print("\n=== Batch 9 synthesis patch complete ===")
