#!/usr/bin/env python3
"""Batch 8 insights patch: add 3 new insights, update 1 existing."""

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

    # 1. Update meta-exploration-failure with AMI Labs evidence
    for ins in insights:
        if ins["id"] == "meta-exploration-failure":
            # Add AMI Labs evidence
            existing_ids = {e["specimenId"] for e in ins["evidence"]}
            if "ami-labs" not in existing_ids:
                ins["evidence"].append({
                    "specimenId": "ami-labs",
                    "note": "LeCun's departure from Meta created AMI Labs — the expelled exploration. World models/V-JEPA research direction rejected by Meta's LLM-focused MSL consolidation was externalized into an independent entity. The exploration didn't die; it crossed the organizational boundary. €500M raise at €3-3.5B valuation demonstrates the expelled research has independent viability."
                })
            # Also add meta-reality-labs evidence
            if "meta-reality-labs" not in existing_ids:
                ins["evidence"].append({
                    "specimenId": "meta-reality-labs",
                    "note": "$70B cumulative Reality Labs losses, 1,500 cuts, VR studio closures. Second exploration bet killed under capital allocation pressure. AR/wearables teams selectively protected while metaverse exploration was wound down."
                })
            # Update maturity: now 3 specimens
            ins["maturity"] = "confirmed"
            print(f"Updated meta-exploration-failure: now {len(ins['evidence'])} evidence entries, maturity=confirmed")
            break

    # 2. Add new insight: Expelled Exploration
    new_insight_1 = {
        "id": "expelled-exploration",
        "title": "Expelled Exploration: Failed Internal Protection Creates Independent Organisms",
        "theme": "mechanism",
        "maturity": "hypothesis",
        "finding": "When organizations fail to protect off-strategy exploration (Mechanism #1 failure) and kill internal exploration initiatives, the exploration doesn't necessarily die — it gets externalized. The researchers or teams whose programs are terminated may leave to pursue the rejected research direction independently, creating new organizations that carry the abandoned exploration forward. AMI Labs (LeCun departing Meta after FAIR was subordinated) is the clearest case: Meta rejected world models in favor of LLMs, LeCun left, founded AMI Labs to pursue world models independently at €3-3.5B valuation. The organizational rejection of a research agenda creates a new, independent organism. This is not in March (1991) — he assumed exploration and exploitation were properties of a single organization. What happens when exploration physically leaves? The pattern may extend beyond frontier AI: pharma researchers whose drug programs get killed in portfolio reviews sometimes leave to found biotechs around the abandoned compound. Any organization that kills exploration initiatives should expect the exploration to potentially continue outside its boundaries, now as a competitor or complement rather than an internal capability.",
        "evidence": [
            {
                "specimenId": "ami-labs",
                "note": "LeCun departed Meta after FAIR was subordinated to product-driven MSL under Wang. Founded AMI Labs to pursue world models (V-JEPA) — the research direction Meta rejected in favor of LLMs. €500M raise, €3-3.5B valuation. The expelled exploration has independent market viability."
            },
            {
                "specimenId": "meta-ai",
                "note": "The expelling organization. 5th restructuring consolidated all AI under MSL. FAIR lost autonomy. Wang's product-urgency mandate left no room for LeCun's alternative research agenda. The organizational pressure that expelled the exploration."
            }
        ],
        "theoreticalConnection": "March (1991) models exploration and exploitation as competing for resources within a single organization. This pattern reveals a boundary condition: when exploitation pressure eliminates exploration, the exploration may cross organizational boundaries rather than disappearing. Relates to Klepper's (2007) spinout dynamics — the most capable employees leave when the parent organization's strategy diverges from their expertise. Also connects to Christensen's (1997) disruption theory: incumbent organizations that reject disruptive research directions create the conditions for independent disruptors to form. The expelled exploration may eventually disrupt the parent.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch8-placement.md",
        "relatedMechanisms": [1],
        "relatedTensions": [1],
        "relatedInsights": ["meta-exploration-failure", "ai-native-no-ambidexterity"],
        "watchFor": "Non-tech cases: pharma spinouts from killed drug programs, defense researchers leaving after program cancellations, financial quants leaving after strategy shifts. Any case where an organization kills an exploration initiative and the team reconstitutes independently."
    }

    # 3. Add new insight: Research Output as Production Tool
    new_insight_2 = {
        "id": "research-output-as-production-tool",
        "title": "When Research Output Automates the Production Process, the Explore/Exploit Boundary Dissolves Internally",
        "theme": "organizational-form",
        "maturity": "hypothesis",
        "finding": "When an AI research lab's output is used to automate the organization's own engineering and production processes, the internal boundary between exploration (research) and exploitation (production) dissolves. Google DeepMind's research contributes to AI models that now generate ~50% of Google's code — the research output IS the production tool. Amazon's internal AI agents handle tasks in engineering, product management, and operations. In these cases, the explore/exploit distinction breaks down because exploration directly produces exploitation capacity. March (1991) assumed exploration and exploitation competed for the same scarce resources (attention, budget, talent). But when the exploration function's output makes the exploitation function more productive, exploration generates its own resource justification. This is distinct from product-production-convergence (which operates at the firm boundary — product vs. operations) — this operates at the internal functional boundary between the research function and the engineering/production function.",
        "evidence": [
            {
                "specimenId": "google-deepmind",
                "note": "~50% of Google's code is now AI-generated (Q4 2025). Research lab output (AI models) directly automates the organization's engineering process. The research function's output IS the production tool."
            },
            {
                "specimenId": "amazon-agi",
                "note": "AI agents already handling tasks in engineering, product management, and operations internally. AGI research feeds into tools that automate Amazon's own production processes, not just customer-facing products."
            }
        ],
        "theoreticalConnection": "March (1991) models explore/exploit as competing for scarce organizational attention. This pattern challenges that assumption: when exploration output directly improves exploitation productivity, they become complements rather than substitutes. Relates to Cohen & Levinthal (1990) absorptive capacity — the organization's ability to exploit external knowledge depends on its internal research capacity. Here the mechanism is more direct: internal research capacity directly produces exploitation tools. Distinct from product-production-convergence, which operates at the firm boundary (Coase/Conway). This operates at the internal functional boundary (March/Simon).",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch8-placement.md",
        "relatedMechanisms": [1],
        "relatedTensions": [1, 2],
        "relatedInsights": ["product-production-convergence"],
        "distinctionFromRelated": "product-production-convergence operates at the FIRM BOUNDARY (product vs. operations, Coase/Conway). This insight operates at the INTERNAL FUNCTIONAL BOUNDARY (research vs. engineering, March/Simon). Same structural blurring phenomenon, different organizational layer. Keep separate to preserve analytical precision."
    }

    # 4. Add new insight: Functional Org Coupling as AI Modularity Constraint
    new_insight_3 = {
        "id": "tight-coupling-modularity-constraint",
        "title": "Tightly-Coupled Organizational Designs Face a Structural Disadvantage in AI Exploration Modularity",
        "theme": "organizational-form",
        "maturity": "hypothesis",
        "finding": "Apple's functional organization — single P&L, no divisional structure, tight lateral coupling across functions (Podolny & Hansen, HBR 2020) — appears structurally unable to create the kind of dedicated, independent AI exploration units (M1 research labs, M8 skunkworks) that multi-divisional Big Tech firms have built. Apple has no equivalent of Google DeepMind, Amazon's AGI lab, or Meta's MSL. When Apple restructured AI, the result was a deliberately weak hub (VP-level Subramanya under Federighi, not SVP-level direct-to-CEO) — the thinnest coordination layer in any M4 we've documented. The hypothesis: tightly-coupled organizations (functional structures with single P&L, strong lateral integration) cannot modularize exploration activities into structurally independent units without disrupting the coupling that makes them effective. They default to contextual integration (M5/M6 patterns) or weak-hub M4 variants. Conversely, these same organizations may be faster at embedding AI across existing functions precisely because the resource fluidity and lateral coordination of the functional model facilitates diffusion. Apple's quiet, long-running AI integration ('it's at the root of the Watch' — Cook) is consistent: strong at contextual integration, weak at structural exploration separation. Testable implication: tightly-coupled orgs will be slower to create dedicated AI exploration units than multi-divisional firms, and will show higher contextual AI integration scores on T1.",
        "evidence": [
            {
                "specimenId": "apple",
                "note": "Functional org, single P&L. AI restructured from SVP-level (Giannandrea) to VP-level (Subramanya under Federighi) — AI's organizational prominence DROPPED, opposite of every other Big Tech firm. Weakest hub in any M4. No structurally independent AI research lab comparable to DeepMind/AGI Lab/MSL. But strong contextual AI integration across products for years."
            }
        ],
        "theoreticalConnection": "Podolny & Hansen (2020, HBR) argued Apple's functional structure enables creative integration across product lines by eliminating divisional P&L competition. Henderson & Clark (1990) on architectural innovation: tightly-coupled architectures struggle with modular innovation because changes propagate across the coupled system. Baldwin & Clark (2000) modularity theory: the ability to modularize (create independent exploration units) depends on having decomposable organizational interfaces. Apple's functional coupling resists decomposition. This suggests a boundary condition for the M4 hub-and-spoke model: it requires a minimum level of organizational modularity that tightly-coupled functional designs may not provide.",
        "discoveredIn": "synthesis/sessions/2026-02-12-batch8-placement.md",
        "relatedMechanisms": [1],
        "relatedTensions": [1, 3],
        "relatedInsights": ["modularity-predicts-ai-structure"],
        "testableImplications": [
            "Tightly-coupled (functional) orgs will be slower to create dedicated M1/M8 AI exploration units than multi-divisional firms",
            "Tightly-coupled orgs will show higher contextual AI integration (positive T1 scores) than structurally similar multi-divisional firms",
            "If Apple eventually creates a structurally independent AI lab, it will signal a fundamental shift in Apple's organizational design philosophy",
            "Other functional-org firms (if identifiable in collection) should show similar weak-hub or contextual-integration patterns"
        ]
    }

    # Add all three new insights
    insights.append(new_insight_1)
    insights.append(new_insight_2)
    insights.append(new_insight_3)

    data["lastUpdated"] = today

    with open(INSIGHTS_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Done. Added 3 new insights, updated 1 existing. Total insights: {len(insights)}")
    print(f"  - expelled-exploration (hypothesis)")
    print(f"  - research-output-as-production-tool (hypothesis)")
    print(f"  - tight-coupling-modularity-constraint (hypothesis)")
    print(f"  - meta-exploration-failure updated to confirmed (3 specimens)")

if __name__ == "__main__":
    main()
