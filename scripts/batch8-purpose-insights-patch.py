#!/usr/bin/env python3
"""Batch 8 patch: add purpose claims analytical insights from Ford/BMW/Honeywell/Toyota haul."""

import json
import os
from datetime import date

INSIGHTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "synthesis", "insights.json"
)

def main():
    with open(INSIGHTS_PATH, "r") as f:
        data = json.load(f)

    insights = data["insights"]
    today = date.today().isoformat()

    # 1. Survival Rhetoric Inversely Correlated with Structural Exploration Investment
    new_insight_1 = {
        "id": "survival-rhetoric-signals-structural-absence",
        "title": "Survival Rhetoric Signals the Absence of a Structural Solution",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "When CEOs deploy survival-type purpose claims ('adapt or die,' 'no Plan B,' 'half of all white-collar workers'), they may be compensating rhetorically for the absence of a structural solution to the AI challenge. Ford's Farley leads with survival rhetoric (5 of 12 claims) and has the weakest dedicated AI exploration structure among automotive peers — Latitude AI is a subsidiary but Farley's public narrative is almost entirely about workforce displacement, not product AI. Compare BMW: zero survival claims, but BMW has the Neue Klasse platform with 20x computing power and a permanent organizational design commitment ('we will never again separate hardware from software'). BMW's structural solution (identity-anchored, embedded AI) eliminates the need for survival rhetoric. Honeywell's Kapur uses survival rhetoric but directs it outward at customers ('there is no Plan B' for labor shortages), not inward — consistent with Honeywell already having an internal structural solution (AI Ambassador model, six-chapter framework). The hypothesis: survival rhetoric is inversely correlated with structural exploration investment. Leaders who have built dedicated AI exploration structures don't need to invoke existential threat because the structure itself embodies the organizational response. Testable: plot survival-claim frequency against structural exploration investment (M1/M8 presence, R&D allocation) for all specimens with purpose claims data.",
        "evidence": [
            {
                "specimenId": "ford",
                "note": "5 of 12 claims are survival-type. Farley's rhetoric is almost entirely workforce-displacement focused. Latitude AI exists but gets zero purpose rhetoric. Weakest AI exploration narrative among major automakers."
            },
            {
                "specimenId": "bmw",
                "note": "Zero survival claims out of 12. Strongest structural identity-anchoring in automotive sector. Neue Klasse platform + 'never again separate hardware from software' = permanent structural commitment eliminates survival rhetoric need."
            },
            {
                "specimenId": "honeywell",
                "note": "2 survival claims but directed outward at customers, not inward at Honeywell. Internal structural solution (AI Ambassadors, six-chapter framework) already exists. Survival rhetoric sells products, not organizational transformation."
            },
            {
                "specimenId": "toyota",
                "note": "Only 1 survival claim (Kon's competitive-gap admission) despite $1B+ TRI investment. Pratt's dominant narrative is teleological (amplify not replace) — the structural exploration solution (TRI) enables purpose-forward rhetoric."
            }
        ],
        "theoreticalConnection": "Connects to Hirschman (1970) voice vs. exit: survival rhetoric is organizational 'voice' — signaling that something is wrong. Organizations with structural solutions (exit from old model into new structure) don't need to shout. Also relates to March (1991): organizations that have structurally protected exploration don't need to rhetorically justify it. The rhetoric of urgency may be a lagging indicator of structural inadequacy.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch8-placement.md",
        "relatedMechanisms": [1],
        "relatedTensions": [1],
        "relatedInsights": ["expelled-exploration"],
        "testableImplications": [
            "Specimens with dedicated M1/M8 exploration structures will have fewer survival-type purpose claims than specimens without them",
            "As organizations build structural solutions, survival rhetoric should decrease in subsequent earnings calls/speeches",
            "Survival rhetoric directed inward (at employees) signals greater structural inadequacy than survival rhetoric directed outward (at customers/market)",
            "Identity-type claims should be positively correlated with structural exploration investment — identity rhetoric replaces survival rhetoric as the structural solution matures"
        ]
    }

    # 2. Rhetorical Division of Labor Mirrors Structural Division
    new_insight_2 = {
        "id": "rhetorical-division-mirrors-structure",
        "title": "Rhetorical Division of Labor Mirrors the Structural Division of Exploration and Execution",
        "theme": "purpose-claims",
        "maturity": "emerging",
        "finding": "In M4 hub-and-spoke organizations, the division of purpose rhetoric between leaders mirrors the structural division between exploration and execution. Toyota is the sharpest case: Gill Pratt (exploration/TRI) speaks exclusively in teleological and higher-calling terms ('amplify not replace,' 'moral obligation,' 'autonomy of people'), while Brian Kursar (execution/Enterprise AI) speaks exclusively in commercial-success terms ('20% productivity,' 'bridge research and production'). Neither crosses into the other's register. Honeywell shows the same pattern: Kapur (CEO/vision) handles utopian, survival, teleological, and higher-calling claims; Sheila Jordan (CDTO/operations) handles only commercial-success claims ('flywheel,' 'early wins'); Venkatarayalu (CTO/methodology) handles framework claims. Ford: Farley (CEO) owns the public purpose narrative entirely; Doug Field (CTO/Latitude AI) is virtually silent — one press release quote in three years. BMW is the exception that proves the rule: Zipse monopolizes all rhetoric because BMW's functional org design doesn't structurally separate exploration from execution — there is no exploration leader to have a separate rhetorical register. The pattern suggests that purpose claims are not just strategic communication — they are structural artifacts. The organizational boundary between exploration and execution manifests as a rhetorical boundary between purpose types. This has implications for using purpose claims as a diagnostic tool: the distribution of claim types across leaders may reveal structural features that organizational charts don't show.",
        "evidence": [
            {
                "specimenId": "toyota",
                "note": "Sharpest case: Pratt (TRI) = teleological/higher-calling only, Kursar (Enterprise AI) = commercial-success only. Neither crosses into the other's register. The structural M4 hub-spoke boundary is perfectly replicated in rhetorical registers."
            },
            {
                "specimenId": "honeywell",
                "note": "Three-way split: Kapur (CEO) = vision/purpose, Jordan (CDTO) = operational pragmatism, Venkatarayalu (CTO) = methodology. Each leader's claim types match their structural role exactly."
            },
            {
                "specimenId": "ford",
                "note": "Extreme version: Farley monopolizes ALL purpose rhetoric. Field (CTO/Latitude AI) is virtually silent — 1 press release quote in 3 years. The structural separation is reflected in rhetorical absence."
            },
            {
                "specimenId": "bmw",
                "note": "Counter-case: Zipse monopolizes all rhetoric because BMW's functional org doesn't structurally separate exploration from execution. No exploration leader exists to have a separate register."
            },
            {
                "specimenId": "netflix",
                "note": "Prior batch: Sarandos has 13/14 claims, CTO Stone has zero. CEO monopolizes AI rhetoric while CTO is invisible. Similar to Ford pattern."
            },
            {
                "specimenId": "disney",
                "note": "Prior batch: Iger has 14/14 claims. Maximum CEO concentration. 'Absent technical leader' pattern in media/entertainment."
            }
        ],
        "theoreticalConnection": "Connects to Gibbons & Henderson (2012) relational contracts: the rhetorical register a leader adopts is a form of implicit contract with their organizational constituency. Exploration leaders make purpose/meaning claims to their research teams; execution leaders make performance claims to operational teams. Also relates to March (1991): the language of exploration (possibility, purpose, horizon) is structurally different from the language of exploitation (efficiency, metrics, speed). If the rhetorical division reliably maps to structural division, purpose claims become a diagnostic tool for organizational structure — potentially useful for remote organizational assessment without access to org charts.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch8-placement.md",
        "relatedMechanisms": [1, 7],
        "relatedTensions": [1, 4],
        "relatedInsights": ["survival-rhetoric-signals-structural-absence"],
        "watchFor": "Non-automotive/industrial cases. Does the pattern hold in pharma (Bourla vs. Kowalski at Pfizer)? In tech (Pichai vs. Hassabis at Google)? In finance (Dimon vs. Heitsenrether at JPMorgan)? The pharma and financial services specimens should be checked for this pattern."
    }

    # 3. Sector-Level Rhetorical Signatures
    new_insight_3 = {
        "id": "sector-rhetorical-signatures",
        "title": "Industrial Sectors Have Distinctive Rhetorical Signatures That Differ Fundamentally from Technology Sectors",
        "theme": "purpose-claims",
        "maturity": "emerging",
        "finding": "The four industrial/automotive specimens scanned in this batch (Ford, BMW, Honeywell, Toyota) share a striking pattern: zero utopian claims across all 53 claims. Not one industrial CEO invokes civilizational transformation, new eras for humanity, or epochal change. This is a categorical absence, not a distributional shift — industrial CEOs simply do not use the utopian register that dominates tech CEO discourse (Zuckerberg, Altman, Huang). Instead, industrial CEOs cluster around three registers: survival (Ford), identity (BMW), and commercial-success + teleological (Honeywell, Toyota). BMW's profile is the most distinctive: pure identity rhetoric (6/12 claims) with zero survival despite operating in an industry widely described as facing existential disruption. Zipse refuses the adapt-or-die frame entirely, instead asserting 'BMW IS the Neue Klasse' — collapsing product platform and organizational identity into one. This is anti-survival rhetoric: BMW is not threatened, it is choosing. Toyota's profile reveals a different pattern: Pratt's 'amplify not replace' philosophy functions as a pre-existing research identity that was deployed as purpose rhetoric when AI became strategically important. The philosophy predates the AI era — it comes from Toyota's manufacturing heritage (Toyota Production System's respect for human judgment). This suggests that some organizations don't create new purpose narratives for AI; they activate existing identity elements. Cross-sector comparison: tech CEOs use purpose claims to authorize building something new (utopian); industrial CEOs use purpose claims to authorize preserving something existing (identity/survival) or to solve concrete problems (teleological/commercial-success). The rhetorical work is fundamentally different even when the structural models are similar (both sectors converge on M4).",
        "evidence": [
            {
                "specimenId": "ford",
                "note": "0 utopian, 5 survival, 2 higher-calling, 3 teleological, 1 identity, 1 commercial-success. Survival-dominated. Farley uses AI as a backdrop for workforce advocacy, not as a product opportunity."
            },
            {
                "specimenId": "bmw",
                "note": "0 utopian, 0 survival, 6 identity, 2 higher-calling, 2 teleological, 2 commercial-success. Pure identity. Anti-survival framing despite industry disruption narratives. 'BMW path' explicitly rejects external benchmarking."
            },
            {
                "specimenId": "honeywell",
                "note": "1 utopian (only borderline — 'autonomy-based economy' is industrial, not civilizational), 4 identity, 4 commercial-success, 2 survival, 2 teleological, 2 higher-calling. Most balanced distribution. Dual-register rhetoric (epochal for investors, pragmatic for customers)."
            },
            {
                "specimenId": "toyota",
                "note": "1 utopian (marginal — 'software and data are essential to mobility'), 4 teleological, 5 commercial-success, 2 identity, 1 survival, 1 higher-calling. Teleological-dominant. 'Amplify not replace' is a pre-AI identity activated as purpose rhetoric."
            }
        ],
        "theoreticalConnection": "Connects to North (1990) institutional constraints: industrial firms operate under different institutional logics than tech firms — their stakeholders (unions, regulators, physical safety requirements, supply chains) demand different types of authorization for transformation. Also relates to Polanyi (1958) tacit knowledge: industrial organizations' deep tacit knowledge about physical processes may make utopian framing feel false because the leaders understand the limits of AI in physical systems in ways that pure-software CEOs do not. Zipse knows cars are physical; Farley knows factories have limits ('not going to be 80%'). This grounding in physical reality may constrain the available rhetorical registers.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch8-placement.md",
        "relatedMechanisms": [],
        "relatedTensions": [4],
        "relatedInsights": ["survival-rhetoric-signals-structural-absence", "rhetorical-division-mirrors-structure"],
        "testableImplications": [
            "No automotive or heavy-industrial CEO will use pure utopian claims (civilizational transformation language) — test with Mercedes-Benz, Honda, Deere, Siemens specimens",
            "Identity-type claims will be more prevalent in industries with strong pre-existing organizational identity (automotive, luxury goods, pharma) than in industries without (IT services, consulting)",
            "The utopian register is a tech-sector specific phenomenon that will not appear in non-tech specimens (excluding borderline cases like Honeywell's bounded 'autonomy-based economy')",
            "Firms that activate pre-existing identity elements (like Toyota's amplification philosophy) will show stronger internal alignment than firms that construct new AI-specific narratives"
        ]
    }

    # Add all three
    insights.append(new_insight_1)
    insights.append(new_insight_2)
    insights.append(new_insight_3)

    data["lastUpdated"] = today

    with open(INSIGHTS_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Done. Added 3 new purpose claims insights. Total insights: {len(insights)}")
    print(f"  - survival-rhetoric-signals-structural-absence (hypothesis)")
    print(f"  - rhetorical-division-mirrors-structure (emerging)")
    print(f"  - sector-rhetorical-signatures (emerging)")


if __name__ == "__main__":
    main()
