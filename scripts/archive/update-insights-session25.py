#!/usr/bin/env python3
"""
Session 25: Add 3 new insights + update inverse-grove with measurement connection.

New insights:
1. measurement-driven-moral-hazard — Holmstrom multi-task applied to AI transitions
2. measurement-inverse-grove-connection — the causal link between measurement failure and inverse-Grove
3. tacit-knowledge-destruction-irreversibility — knowledge loss as irreversible option destruction

Updates:
- inverse-grove: add Klarna full reversal evidence, measurement connection, new related insights
- two-dimensions-of-tacit-information: add Klarna as evidence of within-module tacit knowledge destruction
"""

import json
import sys
from pathlib import Path

INSIGHTS_PATH = Path(__file__).parent.parent / "synthesis" / "insights.json"

def main():
    with open(INSIGHTS_PATH) as f:
        data = json.load(f)

    insights = data["insights"]
    ids = {i["id"] for i in insights}

    # --- NEW INSIGHT 1: measurement-driven-moral-hazard ---
    if "measurement-driven-moral-hazard" not in ids:
        insights.append({
            "id": "measurement-driven-moral-hazard",
            "title": "Measurement-Driven Moral Hazard: AI Transition Metrics Systematically Overstate Success",
            "theme": "mechanism",
            "maturity": "emerging",
            "finding": "When organizations measure AI transition success, the available metrics (cost reduction, volume, speed, resolution rate) systematically overstate effectiveness because they capture the measurable dimensions of output while missing the unmeasurable ones (empathy, trust, complex problem-solving, institutional knowledge). This is Holmstrom (1979) multi-task in organizational form: agents rationally shift effort toward measurable dimensions, and AI amplifies the effect because AI excels precisely at the measurable tasks. The organizational version: executives optimize the metrics they can see, and the dashboard tells them everything is working while quality, trust, and institutional knowledge degrade invisibly. Any organization that announces precise AI performance metrics (resolution rates, cost savings, productivity gains) should be flagged as a measurement-problem candidate — the precision of the metric may be inversely related to its validity as a measure of organizational health.",
            "evidence": [
                {
                    "specimenId": "klarna",
                    "note": "CEO explicitly identified 'cost as predominant evaluation factor' as the root cause of overcorrection. Initial metrics showed AI customer service working (70% resolution, 25-min faster). The 22% satisfaction drop, 900+ BBB complaints, and 102% credit loss increase were lagging indicators of unmeasured quality degradation."
                },
                {
                    "specimenId": "salesforce",
                    "note": "Agentforce reported 84% resolution rate — a measurable metric that authorized headcount cuts. But deterministic Agent Script recalibration was needed for quality issues the resolution rate didn't capture."
                },
                {
                    "specimenId": "intuit",
                    "note": "Three-level goal framework (enterprise→group→team) with precise AI metrics across GenOS platform. Sophisticated governance, but if the metrics are Holmstrom-measurable dimensions, the same bias applies. Candidate for future measurement-problem verification."
                }
            ],
            "theoreticalConnection": "Holmstrom (1979) multi-task principal-agent: when some dimensions of output are measurable and others aren't, rational agents shift effort toward measurable dimensions. Kerr (1975) 'On the folly of rewarding A while hoping for B.' Simon (1947) bounded rationality: decision-makers optimize on available information, and AI transition metrics are bounded in what they can represent. Baker (1992) on incentive contracts and performance measurement distortion.",
            "discoveredIn": "curation/sessions/2026-02-13-batch-curation.md",
            "relatedMechanisms": [5, 11],
            "relatedTensions": [2, 5],
            "relatedInsights": [
                "inverse-grove",
                "measurement-inverse-grove-connection",
                "tacit-knowledge-destruction-irreversibility"
            ],
            "watchFor": "Flag any specimen that announces precise AI performance metrics (resolution rates, cost per interaction, productivity multipliers). The precision of the announced metric may be diagnostic: the more precise and favorable the metric, the higher the risk of unmeasured quality degradation. Scan for lagging indicators: customer satisfaction drops, complaint spikes, employee morale surveys, institutional knowledge loss."
        })
        print("  Added: measurement-driven-moral-hazard")

    # --- NEW INSIGHT 2: measurement-inverse-grove-connection ---
    if "measurement-inverse-grove-connection" not in ids:
        insights.append({
            "id": "measurement-inverse-grove-connection",
            "title": "The Measurement Mechanism Behind Inverse Grove: Why Headquarters Dashboards Lie",
            "theme": "mechanism",
            "maturity": "hypothesis",
            "finding": "The inverse-Grove pattern (headquarters pushing AI faster than organizations can absorb) is not irrational CEO behavior — it is bounded-rational given the available measurement systems. AI transition metrics systematically tell headquarters that everything is working (cost down, volume up, resolution rate high) while front-line quality signals (customer trust erosion, institutional knowledge loss, tacit skill degradation) are invisible to the measurement system. Headquarters pushes harder precisely because their dashboard says it's working. The overcorrection is driven by measurement failure, not managerial hubris. This connects two insights: measurement-driven-moral-hazard provides the MECHANISM; inverse-grove describes the BEHAVIORAL PATTERN. Together they form a testable causal chain: biased metrics → bounded-rational escalation → organizational overcorrection → quality degradation → (optional) forced reversal. Klarna traversed the complete chain. Salesforce is mid-chain. The prediction: any organization reporting strong AI performance metrics while simultaneously cutting headcount is at elevated risk of the full Klarna trajectory.",
            "evidence": [
                {
                    "specimenId": "klarna",
                    "note": "Complete causal chain observed: AI metrics showed 70% resolution → authorized 50% headcount cut → 22% satisfaction drop + 102% credit loss → CEO admission 'cost as predominant evaluation factor' → forced reversal. The measurement system authorized each step of the overcorrection."
                },
                {
                    "specimenId": "salesforce",
                    "note": "Mid-chain: 84% resolution rate metric → 1,000+ Feb 2026 layoffs + 'no more engineers' rhetoric. Deterministic Agent Script recalibration suggests quality issues the metric doesn't capture. Prediction: watch for lagging quality indicators in 2026."
                },
                {
                    "specimenId": "meta-ai",
                    "note": "Partial pattern: $70B metaverse investment driven by Zuckerberg's conviction, not bottom-up metrics. Different mechanism (CEO vision, not metric-driven overcorrection), but same inverse-Grove outcome. Suggests inverse-Grove has multiple causal paths, of which measurement failure is one."
                }
            ],
            "theoreticalConnection": "Combines Holmstrom (1979) multi-task (measurement bias) with Grove (1996) strategic inflection points (organizational inertia) and Simon (1947) bounded rationality (decision-making on available information). The synthesis: Grove identified the information problem (front lines know first); the AI era inverts the information problem (headquarters metrics lie in the other direction). March (1991) provides the exploitation trap mechanism: metrics that show exploitation is working discourage exploration of alternative approaches.",
            "discoveredIn": "curation/sessions/2026-02-13-batch-curation.md",
            "relatedMechanisms": [],
            "relatedTensions": [2, 5],
            "relatedInsights": [
                "inverse-grove",
                "measurement-driven-moral-hazard",
                "tacit-knowledge-destruction-irreversibility"
            ],
            "watchFor": "Test the causal chain: do organizations with stronger AI performance metrics show larger inverse-Grove effects? Do organizations that measure customer satisfaction AND cost (multi-dimensional metrics) avoid the trap? Intuit's three-level goal framework could be a natural experiment — if it measures customer trust alongside cost, it may avoid the Klarna trajectory."
        })
        print("  Added: measurement-inverse-grove-connection")

    # --- NEW INSIGHT 3: tacit-knowledge-destruction-irreversibility ---
    if "tacit-knowledge-destruction-irreversibility" not in ids:
        insights.append({
            "id": "tacit-knowledge-destruction-irreversibility",
            "title": "Irreversible Knowledge Destruction: AI Workforce Transitions Eliminate Tacit Knowledge That Cannot Be Recovered",
            "theme": "mechanism",
            "maturity": "emerging",
            "finding": "AI-driven workforce reductions destroy institutional tacit knowledge that cannot be recovered through rehiring. When organizations reverse AI displacement decisions, they bring in new people without the accumulated tacit knowledge of the departed workforce. This is not just a cost — it is an irreversible option destruction. The tacit knowledge embedded in experienced workers (customer interaction patterns, institutional memory, complaint resolution heuristics, domain-specific judgment) is by definition not capturable in databases or training materials. Organizations that cut first and reverse later end up in a worse position than if they had adopted a hybrid model from the start. The option value of retaining human knowledge is not captured in the cost metrics that drive AI adoption decisions — connecting directly to measurement-driven moral hazard. The measurement system cannot see tacit knowledge because tacit knowledge is by definition unmeasurable. That is WHY the metrics lie.",
            "evidence": [
                {
                    "specimenId": "klarna",
                    "note": "700+ customer service agents accumulated tacit knowledge about interaction patterns, complaint resolution, institutional memory. When agents departed, knowledge was lost. 'Uber-style' rehiring brings new people without this knowledge. 22% satisfaction drop partly attributable to institutional knowledge gap, not just AI capability limits."
                },
                {
                    "specimenId": "amazon-agi",
                    "note": "30K targeted cuts at Manager III/principal levels — these are precisely the layers with the most accumulated organizational tacit knowledge (coordination patterns, institutional relationships, cross-team dependencies). If reversed, the institutional memory is gone."
                },
                {
                    "specimenId": "salesforce",
                    "note": "Feb 2026 layoffs hit Agentforce team itself — the team that built the product being used to justify headcount cuts. Product-specific tacit knowledge (how Agentforce actually works, edge cases, architectural decisions) walks out with the team."
                }
            ],
            "theoreticalConnection": "Polanyi (1966) tacit knowledge: 'we can know more than we can tell.' Nelson & Winter (1982) organizational routines as repositories of tacit organizational knowledge — routines destroyed through layoffs cannot be reconstituted through hiring. Connects to two-dimensions-of-tacit-information hypothesis: within-module tacit knowledge (Dimension 2) is what gets destroyed, and it is precisely the dimension that AI transition metrics cannot measure. Also connects to real options theory: retaining human workers is an option on future organizational capabilities; exercising the option to cut (irreversible) destroys the option to revert.",
            "discoveredIn": "curation/sessions/2026-02-13-batch-curation.md",
            "relatedMechanisms": [11],
            "relatedTensions": [2, 3],
            "relatedInsights": [
                "measurement-driven-moral-hazard",
                "measurement-inverse-grove-connection",
                "inverse-grove",
                "two-dimensions-of-tacit-information",
                "entry-level-talent-hollow"
            ],
            "watchFor": "Track reversal cases: when organizations reverse AI displacement, do they recover to pre-displacement quality levels? If not, the irreversibility thesis is confirmed. Also track hybrid-first organizations — do they outperform cut-first-then-reverse organizations? Klarna vs. a hybrid adopter in the same industry would be the cleanest test."
        })
        print("  Added: tacit-knowledge-destruction-irreversibility")

    # --- UPDATE inverse-grove with Klarna full reversal + measurement connection ---
    for i, insight in enumerate(insights):
        if insight["id"] == "inverse-grove":
            # Update Klarna evidence with full reversal
            for e in insight["evidence"]:
                if e["specimenId"] == "klarna":
                    e["note"] = "Complete inverse-Grove cycle with full reversal. Siemiatkowski pushed AI customer service aggressively from top → metrics showed success → 50% headcount cut → 22% satisfaction drop, 900+ BBB complaints, 102% credit loss → CEO admission 'we went too far, cost as predominant evaluation factor' → emergency redeployment of cross-functional teams → 'Uber-style' hybrid rehiring. Sharpest case because it traverses the COMPLETE arc including forced reversal and CEO acknowledgment of the mechanism (measurement failure)."

            # Add measurement connection to related insights
            related = insight.get("relatedInsights", [])
            for new_id in ["measurement-driven-moral-hazard", "measurement-inverse-grove-connection", "tacit-knowledge-destruction-irreversibility"]:
                if new_id not in related:
                    related.append(new_id)
            insight["relatedInsights"] = related

            # Update finding to reference measurement mechanism
            if "measurement-driven moral hazard" not in insight["finding"]:
                insight["finding"] += "\n\nThe causal mechanism behind inverse-Grove may be measurement-driven moral hazard (see measurement-inverse-grove-connection): AI transition metrics systematically overstate success, causing bounded-rational escalation. The measurement system tells headquarters everything is working while tacit knowledge and quality degrade invisibly. This is not CEO hubris — it is Simon's bounded rationality applied to systematically biased organizational dashboards."

            print("  Updated: inverse-grove (Klarna evidence + measurement connection)")
            break

    # --- UPDATE two-dimensions-of-tacit-information with Klarna evidence ---
    for i, insight in enumerate(insights):
        if insight["id"] == "two-dimensions-of-tacit-information":
            evidence = insight.get("evidence", [])
            # Check if Klarna already exists
            klarna_exists = any(e["specimenId"] == "klarna" for e in evidence)
            if not klarna_exists:
                evidence.append({
                    "specimenId": "klarna",
                    "note": "Customer service has HIGH within-module tacitness (experienced agents accumulate interaction patterns, complaint resolution heuristics, institutional memory that cannot be codified). Klarna treated the work as modular/explicit (AI can do it) and destroyed the within-module tacit knowledge. The 22% satisfaction drop is evidence that within-module tacitness was higher than the organization assumed. Connects irreversibility of knowledge destruction to the two-dimensions framework."
                })
                insight["evidence"] = evidence
                # Add related insights
                related = insight.get("relatedInsights", [])
                if "tacit-knowledge-destruction-irreversibility" not in related:
                    related.append("tacit-knowledge-destruction-irreversibility")
                insight["relatedInsights"] = related
                print("  Updated: two-dimensions-of-tacit-information (Klarna evidence)")
            break

    data["lastUpdated"] = "2026-02-13"
    data["insights"] = insights

    with open(INSIGHTS_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nTotal insights: {len(insights)}")
    print("Done.")

if __name__ == "__main__":
    main()
