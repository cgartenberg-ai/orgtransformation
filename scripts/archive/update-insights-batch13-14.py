#!/usr/bin/env python3
"""
Update insights.json with Batches 13-14 evidence and 3 new insights.
Keeps additions concise per project directive.
"""

import json
from datetime import date

INSIGHTS_PATH = "../synthesis/insights.json"

with open(INSIGHTS_PATH, "r") as f:
    data = json.load(f)

insights = data["insights"]
insight_map = {i["id"]: i for i in insights}

# ============================================================
# 1. Add evidence to rhetorical-division-mirrors-structure
# ============================================================
rd = insight_map["rhetorical-division-mirrors-structure"]
new_evidence = [
    {
        "specimenId": "visa",
        "note": "Batch 13: McInerney (CEO) = military/defensive ('arms race,' 'epochal'), Taneja (Pres. Technology) = developmental/craft ('toddler,' 'science and art'). New register pair: defensive/developmental."
    },
    {
        "specimenId": "honda",
        "note": "Batch 13: Mibe (CEO) = visionary/identity/survival, Brizendine (VP IT) = commercial-success. 'Augment' bridges both tiers as shared vocabulary in different registers."
    },
    {
        "specimenId": "lowes",
        "note": "Batch 14: First four-way division — Ellison (CEO) = workforce/social, Nair (SVP Data/AI) = technical, Godbole (CIO) = customer experience, McFarland (EVP Stores) = adoption metrics. Maps to operational hierarchy, not hub-spoke."
    },
    {
        "specimenId": "lionsgate",
        "note": "Batch 13: Feltheimer (CEO) = creative-first for talent, Burns (VC) = 'candid channel' revealing commercial logic for investors. Division by audience, not structural role."
    },
    {
        "specimenId": "cvs-health",
        "note": "Batch 14: Mandadi (CXO) carries 9/14 claims while CEO is near-silent. In M6a (no hub), the person who embeds AI across functions IS the purpose narrator."
    }
]
rd["evidence"].extend(new_evidence)

# ============================================================
# 2. Add evidence to ceo-silence-spectrum
# ============================================================
cs = insight_map["ceo-silence-spectrum"]
new_evidence_cs = [
    {
        "specimenId": "hp-inc",
        "note": "Batch 14: NEW category — 'departed narrator.' Lores made 12/14 claims, then left for PayPal. Interim CEO Broussard has 0 claims. Purpose narrative orphaned. First natural experiment in narrator departure."
    },
    {
        "specimenId": "cvs-health",
        "note": "Batch 14: CEO Joyner has 2 tentative claims vs predecessor Lynch's stronger 'panoramic care' vision. Mandadi (CXO, 9/14 claims) fills the CEO purpose-claim vacuum."
    },
    {
        "specimenId": "honda",
        "note": "Batch 13: 12/14 from CEO Mibe — near-monopoly but not total. Brizendine provides operationalizing voice. 'CEO-dominant with translator' pattern."
    }
]
cs["evidence"].extend(new_evidence_cs)

# ============================================================
# 3. Add evidence to sector-rhetorical-signatures
# ============================================================
sr = insight_map["sector-rhetorical-signatures"]
new_evidence_sr = [
    {
        "specimenId": "honda",
        "note": "Batch 13 (Japanese auto): identity:6, survival:3, utopian:2 (bounded by heritage). Heritage-as-authorization via 'Power of Dreams.' Confirms no pure utopian from industrial CEOs — Honda's utopian claims are heritage-mediated."
    },
    {
        "specimenId": "panasonic",
        "note": "Batch 13 (Japanese conglomerate): survival:5, identity:3, commercial:3, utopian:0. Internally-directed survival ('30 years of no growth'). Heritage-continuity via Matsushita. Time horizons 10-20yr. Culturally distinct — no Western parallel."
    },
    {
        "specimenId": "lionsgate",
        "note": "Batch 13 (Entertainment): commercial-success:5, identity:3, utopian:1, survival:1. Confirms 'serve creativity' convergence. Adds audience-dependent ordering: creativity-first for talent, efficiency-first for investors."
    },
    {
        "specimenId": "lowes",
        "note": "Batch 14 (Retail): commercial-success:12, identity:2, survival:1, teleological:1, utopian:0, higher-calling:0. Highest metric density in collection. Confirms retail-practical pattern."
    },
    {
        "specimenId": "cognizant",
        "note": "Batch 14 (IT Services): commercial-success:7, identity:5, utopian:3. Kumar's dual-register ('digital labor' for investors, 'amplifier' for public). Extends services-sector pattern from Accenture/Infosys."
    }
]
sr["evidence"].extend(new_evidence_sr)

# ============================================================
# 4. Add evidence to survival-rhetoric-signals-structural-absence
# ============================================================
surv = insight_map["survival-rhetoric-signals-structural-absence"]
new_evidence_surv = [
    {
        "specimenId": "panasonic",
        "note": "Batch 13: 5/10 survival — highest proportion in collection. '30 years of no growth' is most candid failure admission. Inward-directed survival (organizational complacency, not competitor threat). New variant."
    },
    {
        "specimenId": "honda",
        "note": "Batch 13: Survival claims concentrated at inauguration (2021), then retired as identity/utopian claims dominate. Clearest evidence for survival rhetoric lifecycle — confirms testable implication that survival decreases as structural solutions build."
    }
]
surv["evidence"].extend(new_evidence_surv)

# ============================================================
# 5. Add CVS to anti-caio-thesis
# ============================================================
ac = insight_map["anti-caio-thesis"]
# CVS is already there from structural synthesis, but add the rhetorical paradox note
for ev in ac["evidence"]:
    if ev["specimenId"] == "cvs-health":
        ev["note"] = "Mandadi explicitly rejects CAIO: 'worst thing companies can do.' $1B savings, 90% ambient AI, 300K employees — all without CAIO. Rhetorical paradox: rejecting concentrated AI leadership concentrates AI rhetoric in one person (9/14 claims are Mandadi's)."
        break

# ============================================================
# 6. Three new insights (concise)
# ============================================================
new_insights = [
    {
        "id": "heritage-as-authorization",
        "title": "Heritage-as-Authorization: Japanese Organizations Use Founder Mythology to Make AI Feel Like Continuity",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "Honda invokes Soichiro Honda's 'Power of Dreams'; Panasonic invokes Matsushita's founding vision. Both use founder mythology to convert AI transformation from survival rhetoric ('we must change or die') into identity rhetoric ('we have always been this way'). The mechanism: heritage reduces political cost of authorization by framing discontinuity as continuity. Economically rational — reduces organizational resistance to change. Culturally specific to Japanese corporate culture where founder-reverence runs deep (Matsushita is still 'our Founder' with capital F). No direct Western parallel — closest is Disney/Walt, but Japanese founder mythology operates at a deeper institutional level. Extends sector-rhetorical-signatures: Japanese specimens show dramatically longer time horizons (2035, 10-20yr) than Western counterparts.",
        "evidence": [
            {
                "specimenId": "honda",
                "note": "Mibe repeatedly channels 'Power of Dreams' while adding AI dimensions. 'Second founding' metaphor reframes organizational discontinuity as rebirth. Identity-dominant (6/14). Heritage makes AI feel like natural extension, not foreign addition."
            },
            {
                "specimenId": "panasonic",
                "note": "Kusumi anchors AI transformation in 100-year legacy and Matsushita's 'ideal society with affluence both in matter and mind.' Heritage invocation converts survival urgency ('30 years of no growth') into identity narrative ('grown into' not 'pivoted to')."
            }
        ],
        "theoreticalConnection": "Path-dependent institutional logic (North 1990): Japanese corporate founder mythology is an institutional resource that enables AI transformation at lower political cost. Also connects to Teece's dynamic capabilities: organizational heritage is a capability for managing discontinuity when it can be credibly invoked.",
        "relatedInsights": [
            "sector-rhetorical-signatures",
            "survival-rhetoric-signals-structural-absence"
        ],
        "testableImplications": [
            "Japanese M4 specimens will show more identity-type claims and fewer survival-type claims than Western M4 peers with similar industry constraints",
            "Heritage invocation should correlate with lower internal resistance to AI transformation (measurable via employee sentiment or adoption rates)"
        ]
    },
    {
        "id": "audience-dependent-claim-ordering",
        "title": "Audience-Dependent Claim Ordering: Leaders Systematically Invert Purpose Rhetoric by Stakeholder",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "Lionsgate and Cognizant show systematic inversion of purpose claim priorities by audience. Lionsgate: creativity-first for talent/industry press, efficiency-first for investors (Feltheimer's earnings call ordering is precisely inverted from CAIO announcement ordering). Cognizant: 'amplifier of human potential' for public/employees, 'digital labor' and 'broader pyramid' for investors. This is not hypocrisy but rational communication design — different stakeholders have different loss functions (talent fears displacement, investors fear insufficient returns), and leaders optimize framing to minimize salient risk per audience. This is a new mechanism for rhetorical division — not by structural role (as in Toyota) but by stakeholder audience.",
        "evidence": [
            {
                "specimenId": "lionsgate",
                "note": "Feltheimer earnings call: productivity, cost savings, creative toolkit. CAIO announcement: creative vision, efficiencies, IP protection. Precisely inverted ordering by audience. Burns (VC) serves as 'candid channel' for commercial logic that Feltheimer manages."
            },
            {
                "specimenId": "cognizant",
                "note": "Kumar dual-register: 'digital labor' and 'broader pyramid' (replacement language) on earnings calls, 'amplifier of human potential' in Fortune/press interviews. Audience-segmented rhetoric."
            }
        ],
        "theoreticalConnection": "Information economics (Milgrom & Roberts 1986 on strategic information transmission): leaders with private information about AI's impact choose what to emphasize based on each audience's decision-relevant concerns. Not cheap talk — both framings are accurate descriptions of the same transformation, but optimized for different stakeholder loss functions.",
        "relatedInsights": [
            "rhetorical-division-mirrors-structure",
            "sector-rhetorical-signatures"
        ],
        "testableImplications": [
            "Earnings call claim ordering will systematically differ from press/conference claim ordering for the same leader",
            "Industries with strong labor constituencies (entertainment, services) will show larger audience-dependent framing gaps than industries without (finance, tech)"
        ]
    },
    {
        "id": "ceo-departure-natural-experiment",
        "title": "CEO Departure as Natural Experiment: Can Purpose Claims Survive the Architect's Exit?",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "HP Inc's Lores built the entire AI transformation narrative (12/14 claims), including identity-shedding ('not a PC vendor'), liberation rhetoric ('thinking, creating'), and structural commitments (Humane acquisition, HP IQ, $1B savings). He departed for PayPal in Feb 2026 before execution. Interim CEO Broussard has zero public AI claims. This is a natural experiment: can purpose claims survive the departure of the leader who made them? Complementarity theory predicts: if rhetoric was coherently paired with structural commitments, structural momentum sustains transformation; if rhetoric was substituting for incomplete structure, transformation stalls. HP Inc is the most important longitudinal case for testing whether purpose claims are load-bearing or decorative.",
        "evidence": [
            {
                "specimenId": "hp-inc",
                "note": "Lores: 12/14 claims, then departed. Interim CEO Broussard: 0 claims. CTO Kurtoglu, division presidents: also 0 claims. Entire AI narrative was one-man show. Liberation-vs-elimination tension unresolved (AI enables 'fulfillment' AND eliminates 4-6K jobs)."
            }
        ],
        "theoreticalConnection": "Milgrom & Roberts complementarities: if purpose rhetoric and structure are truly complementary, removing one (rhetoric via CEO departure) should degrade the returns to the other (structural commitments). Also tests Gibbons & Henderson relational contracts: did Lores's rhetoric create implicit contracts with employees/customers that now lack an organizational sponsor?",
        "relatedInsights": [
            "ceo-silence-spectrum",
            "purpose-structure-complementarity",
            "survival-rhetoric-signals-structural-absence"
        ],
        "testableImplications": [
            "If HP Inc's new permanent CEO adopts different rhetorical register, watch whether structural commitments (Humane integration, HP IQ) are maintained or abandoned",
            "Compare HP Inc's transformation trajectory to other 'orphaned narrative' cases (if any emerge) to test whether purpose-claim survival depends on structural lock-in"
        ],
        "watchFor": "Track HP Inc quarterly: does Broussard (or successor) adopt Lores's rhetoric? Abandon it? Substitute different framing? The time-to-rhetorical-replacement is itself a datum about how organizational purpose claims are (or aren't) institutionalized beyond individual leaders."
    }
]

insights.extend(new_insights)

# Update metadata
data["lastUpdated"] = str(date.today())

with open(INSIGHTS_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Count final insights
purpose_claims_insights = [i for i in insights if i.get("theme") == "purpose-claims"]
print(f"Done. Total insights: {len(insights)}. Purpose-claims insights: {len(purpose_claims_insights)}.")
print(f"New evidence added to: rhetorical-division-mirrors-structure (+5), ceo-silence-spectrum (+3), sector-rhetorical-signatures (+5), survival-rhetoric-signals-structural-absence (+2), anti-caio-thesis (1 updated)")
print(f"New insights: heritage-as-authorization, audience-dependent-claim-ordering, ceo-departure-natural-experiment")
