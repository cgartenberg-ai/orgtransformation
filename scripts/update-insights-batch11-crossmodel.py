#!/usr/bin/env python3
"""
Add two cross-model rhetorical pattern insights discovered from batch 11 analysis.

Pattern A: Structural separation licenses non-commercial rhetoric
  - Explore-oriented models (M1+M5) have 14.2% commercial-success vs 28.5% for execute-oriented (M3+M6)
  - A 14.4pp gap suggesting structural separation frees leaders from commercial justification

Pattern B: M9 (AI-First) organizations concentrate teleological claims
  - M9 specimens show 23.1% teleological claims vs 3-10% for other models
  - AI-first orgs need existential purpose narratives because AI IS the organization
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


def main():
    data = load_json(INSIGHTS_PATH)
    insights = data["insights"]

    # ─── Pattern A: Structural separation licenses non-commercial rhetoric ───
    pattern_a = {
        "id": "structural-separation-licenses-non-commercial-rhetoric",
        "title": "Structural Separation Licenses Non-Commercial Rhetoric: Explore-Oriented Models Use Half the Commercial Framing of Execute-Oriented Models",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "Across the full claims registry (1,142 claims, 7 structural models), explore-oriented models (M1 Research Lab + M5 Venture Lab) show 14.2% commercial-success claims, while execute-oriented models (M3 Embedded + M6 Distributed) show 28.5% — a 14.4 percentage point gap. When an organization structurally separates its AI exploration from the core business, leaders can afford to talk about AI in non-commercial terms (identity, utopian, teleological). When AI is embedded in operations, leaders must justify it in the language of business performance. This is consistent with an information-cost interpretation: structurally separated units face lower accountability pressure for near-term commercial returns, which frees rhetorical space for aspirational framing. The mechanism may run in both directions — separation enables non-commercial rhetoric AND non-commercial rhetoric may help attract the talent and risk tolerance that exploration requires. M4 (Hub-and-Spoke) sits in the middle at ~22%, consistent with its hybrid explore/execute design.",
        "evidence": [
            {
                "specimenId": "google-deepmind",
                "note": "M1 Research Lab. Hassabis rhetoric is dominated by utopian and teleological claims ('radical abundance', 'cure all disease'). Very low commercial-success rate despite Google's commercial AI products."
            },
            {
                "specimenId": "anthropic",
                "note": "M5 Venture Lab. Amodei's rhetoric centers on higher-calling and identity ('work on science out of proportion to profitability'). Commercial claims are present but secondary."
            },
            {
                "specimenId": "apple",
                "note": "M3 Embedded. Rhetoric is heavily commercial-success and identity. AI justified through product improvement, not civilizational claims."
            },
            {
                "specimenId": "bank-of-america",
                "note": "M6 Distributed. Rhetoric is overwhelmingly commercial-success. AI justified through operational efficiency and customer experience."
            }
        ],
        "relatedMechanisms": [],
        "relatedTensions": [],
        "relatedInsights": ["sector-rhetorical-signatures", "purpose-structure-complementarity"],
        "watchFor": "Within-firm comparison: organizations that shift from M1/M5 to M3/M6 (or vice versa) — does their rhetorical profile shift accordingly? Also: is the commercial gap driven by leader selection (explore units hire visionaries) or structural affordance (the same leader would talk differently in a different structure)?",
        "testableImplications": [
            "Organizations that structurally separate AI exploration (M1, M5) will show <20% commercial-success claims; organizations that embed AI in operations (M3, M6) will show >25%",
            "M4 Hub-and-Spoke will show intermediate commercial-success rates (~20-25%), reflecting its hybrid structure",
            "Leaders who move between explore and execute roles within the same organization will shift their rhetorical register accordingly"
        ],
        "discoveredIn": "synthesis/sessions/2026-02-12-batch11-m4-hub-spoke.md"
    }
    insights.append(pattern_a)
    print(f"  ✓ Added: structural-separation-licenses-non-commercial-rhetoric")

    # ─── Pattern B: M9 teleological concentration ───
    pattern_b = {
        "id": "ai-first-teleological-concentration",
        "title": "AI-First Organizations Concentrate Teleological Claims: M9 Shows 23% Teleological vs 3-10% for Other Models",
        "theme": "purpose-claims",
        "maturity": "hypothesis",
        "finding": "M9 (AI-First) specimens show 23.1% teleological claims — 2-7x the rate of any other structural model. When AI IS the organization rather than a tool the organization uses, leaders need existential purpose narratives that specify what concrete outcome their AI existence serves. 'We exist to achieve safe superintelligence' (SSI) or 'we exist to ensure AI benefits humanity' (Anthropic-adjacent framing) are not optional rhetorical flourishes — they are the organizational raison d'être. Without a teleological anchor, an AI-first organization has no answer to 'why do you exist?' beyond 'to build AI,' which is tautological. This is analytically distinct from utopian claims (which invoke an epoch) — teleological claims specify a CONCRETE, potentially falsifiable end. M1 (Research Lab) shows a correlated pattern: near-zero higher-calling (1.8%) but moderate teleological. The mechanism is different: M1 labs justify existence through discovery (teleological: 'cure disease') rather than duty (higher-calling: 'we owe the world'). Sample size caveat: only 10 M9 specimens in the collection. Pattern is strong but needs confirmation as the M9 sample grows.",
        "evidence": [
            {
                "specimenId": "ssi",
                "note": "M9 AI-First. Pure teleological framing: 'safe superintelligence' IS the organizational purpose. No commercial-success claims because there is no commercial product yet."
            },
            {
                "specimenId": "anduril",
                "note": "M9 AI-First. Teleological: 'ensure the free world maintains military-technological advantage.' Specific, falsifiable outcome that justifies the organization's existence."
            },
            {
                "specimenId": "sierra-ai",
                "note": "M9 AI-First. Business model (outcome-based pricing) IS a teleological claim: 'we only succeed if the customer succeeds.' Purpose and business logic are structurally fused."
            }
        ],
        "relatedMechanisms": [],
        "relatedTensions": [],
        "relatedInsights": ["structural-separation-licenses-non-commercial-rhetoric", "sector-rhetorical-signatures"],
        "watchFor": "As more M9 specimens are added, does the teleological concentration hold? Also monitor whether M9 organizations that mature and add commercial products shift toward commercial-success claims — this would suggest teleological framing is a startup-phase phenomenon rather than a structural property of AI-first organizations.",
        "testableImplications": [
            "M9 organizations will consistently show >15% teleological claims, regardless of industry",
            "M9 organizations that add commercial products will show increasing commercial-success claims over time, potentially at the expense of teleological claims",
            "New M9 entrants (pre-revenue) will show the highest teleological concentration; post-IPO M9 firms will moderate"
        ],
        "discoveredIn": "synthesis/sessions/2026-02-12-batch11-m4-hub-spoke.md"
    }
    insights.append(pattern_b)
    print(f"  ✓ Added: ai-first-teleological-concentration")

    # Save
    data["insights"] = insights
    data["lastUpdated"] = TODAY
    save_json(INSIGHTS_PATH, data)
    print(f"\n  Total insights: {len(insights)}")
    print(f"  Added: structural-separation-licenses-non-commercial-rhetoric, ai-first-teleological-concentration")


if __name__ == "__main__":
    main()
