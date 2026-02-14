#!/usr/bin/env python3
"""Add 3 new field signals from podcast research files (Feb 7, 2026)."""

import json
from pathlib import Path
from datetime import datetime

SIGNALS_PATH = Path(__file__).parent.parent / "research" / "field-signals.json"

with open(SIGNALS_PATH) as f:
    data = json.load(f)

new_signals = [
    {
        "id": "saasmageddon-enterprise-restructuring",
        "signal": "SaaSmageddon: AI agents trigger enterprise software model collapse",
        "description": "On Feb 4, 2026, Nasdaq Cloud Index plummeted $285B as AI agents demonstrated ability to replace SaaS workflows. IDC predicts 70% of software vendors abandon seat-based pricing by 2028. Enterprises shifting from 'managing human workers who use software' to 'managing AI agents that orchestrate workflows.' Forces procurement, IT architecture, and process team restructuring.",
        "theme": "structural-form",
        "firstObserved": "2026-02-07",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-substack-feed-check.json"],
        "relatedSpecimens": ["salesforce", "workday", "sap", "servicenow"],
        "dataPoints": [
            "$285B wiped from Nasdaq Cloud Index on Feb 4, 2026",
            "IDC: 70% of software vendors abandon seat-based pricing by 2028",
            "Triggered by wave of disappointing SaaS earnings + Anthropic automation demos"
        ],
        "counterEvidence": "Some argue this is temporary valuation correction, not structural shift. Enterprise switching costs remain high.",
        "promotedTo": None
    },
    {
        "id": "management-as-ai-superpower",
        "signal": "Management skills (not technical AI) as binding constraint on AI adoption",
        "description": "Mollick's Wharton MBA experiment: students built functional startup prototypes in 4 days using AI tools. Key finding: management training (scoping, delegation, evaluation) predicted success, not AI expertise. Goldman's Argenti independently argues junior workers need 'player-coach' skills (articulating tasks, delegating to agents, supervising results). Both converge: the scarce resource is 'knowing what good looks like,' not technical AI capability.",
        "theme": "talent",
        "firstObserved": "2026-02-07",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-deep-scan-feb-2026.json", "goldman-sachs-deep-scan.json"],
        "relatedSpecimens": ["goldman-sachs"],
        "dataPoints": [
            "Wharton MBA class: functional startup prototypes in 4 days (Mollick: 'order of magnitude further along than full semester before AI')",
            "Goldman Argenti: three competencies for AI era — articulating tasks, delegating to agents, supervising results",
            "Mollick: 'The people who thrive will be the ones who know what good looks like'",
            "Elite AI lab developers shifting from programming to management of AI agents"
        ],
        "counterEvidence": "Selection bias: Wharton MBAs are already high-capability individuals. May not generalize to broader workforce.",
        "promotedTo": None
    },
    {
        "id": "ai-agent-to-human-ratio-as-metric",
        "signal": "AI agent-to-human ratio emerging as trackable organizational metric",
        "description": "McKinsey disclosed 25,000 AI agents alongside 40,000 human employees (0.625:1 ratio), targeting 1:1 by year-end 2026. First major professional services firm to publicly report this metric. Client-facing roles grew ~25%, non-client-facing roles shrank ~25%. Signals organizations moving from 'AI as tool' to 'AI as workforce member' with implications for org charts, resource allocation, and governance.",
        "theme": "structural-form",
        "firstObserved": "2026-02-07",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-substack-feed-check.json"],
        "relatedSpecimens": [],
        "dataPoints": [
            "McKinsey: 25,000 AI agents + 40,000 humans = 0.625:1 ratio",
            "Target: 1:1 human-to-agent ratio by end of 2026",
            "Client-facing roles grew ~25%; non-client-facing roles shrank ~25%",
            "Sternfels: three irreplaceable human capabilities — creativity, judgment, interpersonal acumen",
            "Saved 1.5 million hours in search/synthesis work in 2025"
        ],
        "counterEvidence": "Definition of 'AI agent' is vague — could be inflated by counting simple automation as 'agents.' No external verification of the 25K number.",
        "promotedTo": None
    }
]

existing_ids = {s["id"] for s in data["signals"]}
added = 0
for signal in new_signals:
    if signal["id"] not in existing_ids:
        data["signals"].append(signal)
        added += 1
        print(f"  Added: {signal['id']}")
    else:
        print(f"  Skipped (exists): {signal['id']}")

data["lastUpdated"] = "2026-02-10T10:00:00Z"

with open(SIGNALS_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Added {added} new field signals. Total: {len(data['signals'])}")
