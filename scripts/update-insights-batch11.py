#!/usr/bin/env python3
"""
Update synthesis/insights.json with Batch 11 (M4 hub-spoke) findings.

Updates:
1. ceo-silence-spectrum — 4 new data points (Delta CEO monopoly, UHG CEO silence, TR duet, Deere cascade)
2. rhetorical-division-mirrors-structure — TR duet + Deere cascade as new cases
3. sector-rhetorical-signatures — 4 new industry data points
4. purpose-structure-complementarity — broader thesis reinforcement

New insight:
5. commercial-moral-register-convergence — when higher-calling framing aligns with commercial interest
"""

import json
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSIGHTS_PATH = os.path.join(BASE, "synthesis", "insights.json")
TODAY = date.today().isoformat()


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def find_insight(insights, insight_id):
    for i, ins in enumerate(insights):
        if ins["id"] == insight_id:
            return i, ins
    return None, None


def main():
    data = load_json(INSIGHTS_PATH)
    insights = data["insights"]

    # ─── 1. Update ceo-silence-spectrum ───
    idx, ins = find_insight(insights, "ceo-silence-spectrum")
    if ins:
        new_evidence = [
            {
                "specimenId": "delta-air-lines",
                "note": "Batch 11: 14/14 claims from CEO Bastian. Total CEO monopoly — no CDTO (Duggirala), no CTO, no other executive speaks on AI purpose. For a 100K-person org, this is striking. AI narrative is a personal leadership project. Risk: does 'augmented intelligence' philosophy survive Bastian's departure?"
            },
            {
                "specimenId": "unitedhealth-group",
                "note": "Batch 11: 14/16 claims from CDTO Dadlani, only 1 from CEO Hemsley (commercial-success), 1 from CDAO Kurtzweil. CEO silence is strategic risk management — AI is reputationally toxic due to nH Predict algorithm scandal, class-action lawsuits, DOJ scrutiny. The CDTO absorbs rhetorical exposure the CEO cannot."
            },
            {
                "specimenId": "thomson-reuters",
                "note": "Batch 11: Perfect 8/8 split — CEO Hasker (8 claims: market/investor register) and CTO Hron (8 claims: identity/learning register). Most coordinated two-voice strategy in the collection. Acqui-hire CTO brings startup framing; CEO provides institutional framing."
            },
            {
                "specimenId": "deere-and-co",
                "note": "Batch 11: CEO May (6), VP Heraud (3), Product Mgr Moeller (2), CTO Hindman (1), CFO Jepsen (1). ONLY specimen where purpose rhetoric cascades from CEO through middle management with near-verbatim echoes ('do more with less', 'innovate with purpose'). Suggests organizational diffusion rather than concentration."
            }
        ]
        ins["evidence"].extend(new_evidence)
        ins["finding"] = ins["finding"].rstrip() + " Batch 11 M4 specimens reveal three new patterns beyond monopoly/silence/distribution: (1) strategic CEO silence as risk management (UHG — CEO can't afford AI association due to governance scandal), (2) coordinated duet with register specialization (TR — CEO does investor framing, CTO does identity framing, exactly 8 claims each), (3) rhetorical cascade where CEO-level formulations appear nearly verbatim in product manager statements (Deere — 'do more with less' cascades from CEO to PM level)."
        insights[idx] = ins
        print(f"  ✓ Updated ceo-silence-spectrum (+4 evidence)")

    # ─── 2. Update rhetorical-division-mirrors-structure ───
    idx, ins = find_insight(insights, "rhetorical-division-mirrors-structure")
    if ins:
        new_evidence = [
            {
                "specimenId": "thomson-reuters",
                "note": "Batch 11: CEO Hasker occupies market/survival/commercial register (earnings calls, media events). CTO Hron occupies identity/learning register (Fortune profile, SiliconAngle). Exactly 8 claims each. The CEO-CTO structural division perfectly maps to rhetorical specialization — Hasker tells investors 'white space opportunity'; Hron tells the industry 'AI made our roadmap bigger.' Neither crosses into the other's territory."
            },
            {
                "specimenId": "deere-and-co",
                "note": "Batch 11: New pattern — rhetorical CASCADE rather than division. CEO May's formulations ('purpose-driven technology', 'do more with less') appear near-verbatim in product manager Moeller's interviews 2 years later. Acquired-unit VP Heraud (Blue River) retains a more technically utopian register ('superhuman performance') than institutional Deere leaders. The hub-spoke structural boundary maps to rhetorical tone: hub = grounded purpose, acquired spokes = expansive vision."
            }
        ]
        ins["evidence"].extend(new_evidence)
        insights[idx] = ins
        print(f"  ✓ Updated rhetorical-division-mirrors-structure (+2 evidence)")

    # ─── 3. Update sector-rhetorical-signatures ───
    idx, ins = find_insight(insights, "sector-rhetorical-signatures")
    if ins:
        new_evidence = [
            {
                "specimenId": "thomson-reuters",
                "note": "Batch 11 (Legal Tech/Media): commercial-success:8, utopian:4, survival:3, identity:3, higher-calling:1, teleological:0. Heavy commercial clustering because AI IS the product. Most commercially direct rhetoric in collection — no gap between AI strategy and business strategy. Confirms non-tech pattern: utopian claims are present (4) but grounded in professional domain ('biggest disruption in legal history'), not civilizational."
            },
            {
                "specimenId": "deere-and-co",
                "note": "Batch 11 (Agriculture): commercial-success:5, utopian:3, higher-calling:2, identity:2, survival:2, teleological:0. Balanced distribution. 'Feeding the world' is the utopian anchor but remains grounded in agricultural necessity. Higher-calling notable on earnings calls ('driven by a higher purpose that extends beyond merely solving a problem'). Labor shortage is primary legitimation for autonomous AI — structural, not aspirational."
            },
            {
                "specimenId": "unitedhealth-group",
                "note": "Batch 11 (Healthcare/Insurance): identity:6, teleological:5, higher-calling:2, commercial-success:2, survival:1, utopian:0. Zero utopian claims — governance controversy eliminates grandiosity as an option. Defensive identity dominates ('AI is never used to deny a claim'). Note: hold this as provisional — UHG's profile may be crisis-shaped rather than sector-shaped. Need more healthcare payer specimens."
            },
            {
                "specimenId": "delta-air-lines",
                "note": "Batch 11 (Airlines): identity:7, higher-calling:3, utopian:2, commercial-success:2, survival:1, teleological:0. Identity-dominant. 'Augmented intelligence' and 'innovating with heart' are branded philosophies that anchor all claims. Zero teleological — airlines don't lend themselves to specific falsifiable moral outcomes. 'Lift people up' is the higher-calling anchor."
            }
        ]
        ins["evidence"].extend(new_evidence)
        # Update testable implication result
        ins["finding"] = ins["finding"].rstrip() + " Batch 11 adds four non-automotive industries: legal tech (commercial-dominant), agriculture (balanced with higher-calling), healthcare insurance (defensive identity, zero utopian — but possibly crisis-shaped), airlines (identity-dominant, zero teleological). Confirms utopian claims remain rare outside tech; disconfirms prediction that no industrial CEO will use higher-calling on earnings calls (Deere's May uses 'higher purpose' on Q4 2024 call)."
        insights[idx] = ins
        print(f"  ✓ Updated sector-rhetorical-signatures (+4 evidence)")

    # ─── 4. Update purpose-structure-complementarity ───
    idx, ins = find_insight(insights, "purpose-structure-complementarity")
    if ins:
        new_evidence = [
            {
                "specimenId": "thomson-reuters",
                "note": "Batch 11 (high complementarity): M4+M5 structural design with CEO/CTO duet. Hasker speaks to investors/customers in commercial/survival register; Hron speaks to industry/talent in identity/learning register. Purpose-structure complementarity is high — the dual-voice exactly mirrors the dual-function (product + production)."
            },
            {
                "specimenId": "delta-air-lines",
                "note": "Batch 11 (ambiguous complementarity): M4/Contextual structure but total CEO monopoly on rhetoric. The contextual orientation (AI distributed across functions) is NOT matched by distributed rhetoric. Single voice, distributed structure. Does this indicate misalignment, or is CEO-centrism the appropriate complementary form for contextual ambidexterity? Open question."
            },
            {
                "specimenId": "unitedhealth-group",
                "note": "Batch 11 (crisis-induced misalignment): M4/Structural with CEO-silent, CDTO-loud rhetoric. Purpose claims are delegated to tech leader because CEO can't afford AI association. This is NOT organic complementarity but forced by governance crisis — the rhetoric doesn't mirror the structure, it mirrors the crisis."
            }
        ]
        ins["evidence"].extend(new_evidence)
        ins["finding"] = ins["finding"].rstrip() + " Batch 11 reinforces the broader thesis that purpose claims are load-bearing rhetorical infrastructure enabling or constraining structural choices. UHG cannot build ambitious AI partly because it cannot talk about AI ambitiously — defensive rhetoric constrains deployment scope. Delta can deploy slowly because 'augmented intelligence' framing authorizes patience. TR can acquire aggressively because its two-voice strategy makes acquisitions legible as both organizational learning and customer service."
        insights[idx] = ins
        print(f"  ✓ Updated purpose-structure-complementarity (+3 evidence)")

    # ─── 5. New insight: commercial-moral register co-occurrence ───
    new_insight = {
        "id": "commercial-moral-register-convergence",
        "title": "Commercial Interest and Moral Framing Converge in Purpose Claims: Organizations Construct Purpose Where Profit and Principle Align",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "Organizations don't choose between commercial and moral justifications for AI — they construct purpose claims at the intersection where the two converge. Thomson Reuters frames copyright defense as moral obligation to the content ecosystem (higher-calling), but TR's business depends on copyright. Deere frames autonomous farming as 'feeding the world' (teleological/utopian), but Deere sells the equipment that enables it. Delta frames AI as 'lifting people up' (higher-calling), but the 'augmented intelligence' philosophy also protects Delta's service-dependent business model from automation pressure. The rhetorical work is not hiding commercial interest behind moral language — it is finding the moral frame that makes commercial action feel justified to multiple audiences simultaneously (employees, investors, regulators, customers). This is consistent with a relational contract interpretation (Gibbons & Henderson): shared purpose narratives reduce coordination costs by providing a common justification that doesn't require explicit agreement on whether the motivation is moral or commercial. The claim works precisely because it is both at once. The empirical question is whether co-occurrence is different from pure substitution (using moral claims when commercial claims would be politically costly) — this requires comparing within-specimen claim type usage across different audience contexts (earnings calls vs. employee communications vs. public speeches).",
        "evidence": [
            {
                "specimenId": "thomson-reuters",
                "note": "Hasker's copyright defense claim: 'if copyright is fundamentally undermined, then so too are the incentives for people to create content.' Higher-calling framing (duty to content ecosystem) that perfectly serves commercial interest (TR's content moat). The alignment is transparent, not hidden."
            },
            {
                "specimenId": "deere-and-co",
                "note": "May's 'feeding the world' / 'purpose-driven technology' framing elevates tractor sales to civilizational necessity. The labor shortage narrative makes autonomous equipment seem morally necessary (higher-calling) while being commercially beneficial (Deere sells the autonomy). 60% herbicide reduction serves both sustainability (moral) and cost savings (commercial)."
            },
            {
                "specimenId": "delta-air-lines",
                "note": "Bastian's 'augmented intelligence' and 'lift people up' (higher-calling) protect Delta's workforce-intensive business model from the displacement narrative. The moral frame (workers matter) and the commercial logic (Delta needs its people) converge. The $1B profit-sharing commitment is presented as cultural identity, but also as economic policy."
            },
            {
                "specimenId": "unitedhealth-group",
                "note": "Dadlani's 'beautiful experiences in healthcare' (higher-calling) imports consumer-tech aesthetics but also positions UHG's AI products competitively. 'Operate at the top of their license' invokes provider aspiration (moral) while anchoring 'hundreds of billions of dollars' in administrative savings (commercial). Dual-register claims serve both audiences simultaneously."
            }
        ],
        "relatedMechanisms": [],
        "relatedTensions": [4],
        "relatedInsights": ["sector-rhetorical-signatures", "purpose-structure-complementarity"],
        "watchFor": "Cross-context comparison: do the same speakers shift emphasis between moral and commercial registers depending on audience? Earnings calls (investor audience) should lean commercial; employee communications should lean moral; public speeches should blend. If we find pure substitution (moral claims ONLY where commercial claims would be risky), that supports the cynical reading. If we find consistent co-occurrence across contexts, that supports the relational contract interpretation.",
        "testableImplications": [
            "Claims where commercial interest and moral framing converge will be the most durable — they should persist across leadership changes and strategy shifts because they are self-reinforcing",
            "Claims where moral framing contradicts commercial interest ('higher-calling' in the absence of business benefit) will be the most fragile and least common in the collection",
            "Within-specimen, the ratio of commercial-to-moral framing should vary by audience (higher moral ratio in employee-facing contexts, higher commercial ratio in investor-facing contexts) but the SAME underlying claims should appear in both — just with different emphasis",
            "Organizations whose purpose claims show high commercial-moral convergence should show stronger internal alignment (measured by, e.g., employee sentiment or adoption rates) than those with pure commercial OR pure moral framing"
        ],
        "discoveredIn": "synthesis/sessions/2026-02-12-batch11-m4-hub-spoke.md"
    }
    insights.append(new_insight)
    print(f"  ✓ Added new insight: commercial-moral-register-convergence")

    # Save
    data["insights"] = insights
    data["lastUpdated"] = TODAY
    save_json(INSIGHTS_PATH, data)
    print(f"\n  Total insights: {len(insights)}")
    print(f"  Updated: ceo-silence-spectrum, rhetorical-division-mirrors-structure, sector-rhetorical-signatures, purpose-structure-complementarity")
    print(f"  Added: commercial-moral-register-convergence")


if __name__ == "__main__":
    main()
