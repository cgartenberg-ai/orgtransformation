#!/usr/bin/env python3
"""Add new field signals from podcast/conference sweep (Feb 10, 2026)."""

import json
from pathlib import Path

SIGNALS_PATH = Path(__file__).parent.parent / "research" / "field-signals.json"

with open(SIGNALS_PATH) as f:
    data = json.load(f)

existing_ids = {s["id"] for s in data["signals"]}

new_signals = [
    {
        "id": "ai-agents-as-org-members",
        "signal": "AI agents formally counted as organizational members",
        "description": "McKinsey now counts 25,000 AI agents as part of its 60,000-person 'workforce' — not metaphorically, but literally in their organizational headcount. CEO targets 1:1 human-agent parity by end of 2026. This challenges traditional assumptions about what constitutes an 'organization member' with implications for spans of control, governance, and resource allocation.",
        "theme": "structural-form",
        "firstObserved": "2026-02-07",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": [],
        "dataPoints": [
            "McKinsey: 40K humans + ~25K AI agents = 60K total 'employees' (CES 2026, Sternfels)",
            "Up from 'a few thousand agents' 18 months prior",
            "Target: 1:1 human-agent parity by end of 2026",
            "QuantumBlack (1,700-person AI division) drives 40% of firm revenue",
            "SaaStr: 10 SDRs/AEs replaced by 20 AI agents managed by 1.2 humans (Lemkin)"
        ],
        "counterEvidence": "Definition of 'AI agent' is vague — could be inflated by counting simple automation. No external verification of the 25K number. Merges with existing ai-agent-to-human-ratio signal.",
        "promotedTo": None
    },
    {
        "id": "management-scarcity-inversion",
        "signal": "AI inverts resource scarcity: management skills become the bottleneck",
        "description": "Mollick (Wharton) argues that AI inverts traditional resource scarcity: execution talent becomes abundant and cheap, while judgment/domain knowledge/delegation ability becomes scarce. Senior developers at AI labs report their jobs shifting 'from mostly programming to mostly management of AI agents.' Delegation to AI follows the same frameworks as delegation to humans (military Five Paragraph Order, PRDs, shot lists). If true, organizations built around managing scarce talent need fundamental structural redesign.",
        "theme": "talent",
        "firstObserved": "2026-02-10",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": ["goldman-sachs"],
        "dataPoints": [
            "Mollick: 'Now the talent is abundant and cheap. What is scarce is knowing what to ask for.'",
            "AI lab developers shifting 'from mostly programming to mostly management of AI agents'",
            "Delegation frameworks (Five Paragraph Order, PRDs, shot lists) apply to AI delegation",
            "Goldman Argenti: junior workers as 'player-coaches' managing AI agents (independent convergence)",
            "Implication: organizations with strong delegation cultures may adapt to AI faster"
        ],
        "counterEvidence": "Wharton MBA sample may not generalize. Management skills are hard to define and measure. Many routine management tasks (scheduling, status tracking) ARE automatable.",
        "promotedTo": None
    },
    {
        "id": "cio-ceo-governance-tension",
        "signal": "CIO-CEO tension: competing decision rights over AI adoption pace",
        "description": "NRF 2026 surfaced a specific structural tension: 'CEOs are hungry to implement and drive change — but CIOs are saddled with tempering the speed of implementation and managing expectations.' AI deployment requires multi-year rollouts, not 'flip-the-switch' deployment. This maps the explore-execute tension to specific C-suite roles: CEO as exploration champion vs. CIO as execution guardian.",
        "theme": "governance",
        "firstObserved": "2026-02-10",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": [],
        "dataPoints": [
            "NRF 2026: 'CEOs are hungry to implement — CIOs are saddled with tempering speed'",
            "68% of retailers planning agentic AI deployment in 12-24 months",
            "NRF added dedicated 'AI Stage' for 2026 (structural separation at industry level)",
            "AI deployment entails multi-year rollouts, not 'flip-the-switch' technology"
        ],
        "counterEvidence": "May be sector-specific to retail. In tech firms, CTO/CIO may be the AI champion. Tension may resolve as boards develop AI competence.",
        "promotedTo": None
    },
    {
        "id": "davos-org-design-bottleneck",
        "signal": "Global CEO consensus: organizational design is THE AI bottleneck",
        "description": "Multiple Davos 2026 sessions converged on the view that 'adoption is ultimately where success is measured' and that moving beyond AI pilots requires 'new strategies, capabilities, and organizational designs.' Accenture CEO: 'Human in the lead, not human in the loop.' Technology is no longer the constraint — organization is. Validates our entire research premise.",
        "theme": "convergence",
        "firstObserved": "2026-02-10",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": [],
        "dataPoints": [
            "Davos 2026: 'adoption is ultimately where success is measured'",
            "Accenture CEO (Sweet): 'Human in the lead, not human in the loop'",
            "Amodei (Anthropic): engineers 'use AI to write code, and then edit it themselves'",
            "AI cost management as new governance challenge: usage-based consumption models",
            "Fink (BlackRock): 'Hundreds of billions needed to build this out'"
        ],
        "counterEvidence": "Davos is notoriously susceptible to consensus thinking. CEOs may be post-rationalizing past decisions. The 'organizational design' framing may be vaguer than it sounds.",
        "promotedTo": None
    },
    {
        "id": "ai-governance-maturity-gap",
        "signal": "80% of companies lack mature AI agent governance models",
        "description": "Deloitte 2026 report: only 1 in 5 companies has a mature governance model for autonomous AI agents. Companies report stronger strategic alignment (42% highly prepared) than operational readiness in 'infrastructure, data, risk, and talent.' Education — not role or workflow redesign — remains the #1 talent adjustment strategy, suggesting most orgs are training people for the old structure, not redesigning the structure for AI.",
        "theme": "governance",
        "firstObserved": "2026-02-10",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": [],
        "dataPoints": [
            "Deloitte 2026: only 1 in 5 companies has mature AI agent governance",
            "42% highly prepared on strategic alignment vs. much lower on operational readiness",
            "Education (not workflow/role redesign) is #1 talent adjustment strategy",
            "Gap between strategic intent and operational capability in infrastructure, data, risk, talent"
        ],
        "counterEvidence": "Self-reported survey data. 'Mature governance' may be defined differently across firms. Deloitte has consulting business interest in finding governance gaps.",
        "promotedTo": None
    },
    {
        "id": "professional-services-dual-restructuring",
        "signal": "Professional services firms restructuring both internally and as AI transformation advisors",
        "description": "McKinsey (25K agents, QuantumBlack at 40% revenue), BCG (multi-year embedded AI transformation), PwC, Accenture all restructuring around AI both internally (how they work) and externally (what they sell). Their dual role — restructuring themselves while advising others on restructuring — creates interesting selection effects and potential conflicts of interest. Professional services is a distinct structural pattern we haven't documented.",
        "theme": "structural-form",
        "firstObserved": "2026-02-10",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": ["accenture-openai"],
        "dataPoints": [
            "McKinsey: 25% client-facing growth / 25% back-office cuts",
            "McKinsey: outcome-based partnerships replacing fee-for-service advisory",
            "QuantumBlack: 1,700-person AI division = 40% of McKinsey revenue",
            "Sternfels (CES 2026): 'Transform or die'",
            "BCG: multi-year AI transformation engagements with embedded tools",
            "Accenture: $5.9B GenAI bookings while $865M own restructuring"
        ],
        "counterEvidence": "Conflict of interest: consultants recommending AI restructuring they can sell. McKinsey 25K agent count may be inflated for CES presentation impact.",
        "promotedTo": None
    },
    {
        "id": "saas-to-agent-orchestration-structural-question",
        "signal": "Agent-per-app vs cross-app orchestration as fundamental structural choice",
        "description": "Thompson (Stratechery) argues every SaaS app will have its own agent, but agents will be 'bound by the borders of the application.' The key structural question: who owns the intelligence/orchestration layer? If agents are app-bound, SaaS vendors retain control. If a horizontal orchestrator (Microsoft Work IQ) spans apps, it captures the coordination layer. This is the organizational governance equivalent of 'make vs buy' for AI intelligence.",
        "theme": "structural-form",
        "firstObserved": "2026-02-10",
        "lastUpdated": "2026-02-10",
        "status": "active",
        "sessions": ["podcast-conference-sweep-feb-10.json"],
        "relatedSpecimens": ["microsoft", "salesforce"],
        "dataPoints": [
            "Thompson: 'SaaSmageddon' — AI agents disrupting SaaS business models",
            "Thompson: 'painful corrections to valuation, consolidation, and substantial layoffs' expected",
            "Microsoft Work IQ: using M365 data for 'most valuable stateful agent'",
            "Each SaaS app agent 'definitionally bound by the borders of the application'",
            "Cross-app agent orchestration as the new coordination layer"
        ],
        "counterEvidence": "Thompson argues moats exist and transition will be more graduated than 'SaaS is dead' narrative. Enterprise switching costs remain very high.",
        "promotedTo": None
    }
]

added = 0
for sig in new_signals:
    if sig["id"] not in existing_ids:
        data["signals"].append(sig)
        existing_ids.add(sig["id"])
        added += 1
    else:
        print(f"  ⚠️ Signal '{sig['id']}' already exists — skipping")

# Also update existing signals that the sweep enriched
for sig in data["signals"]:
    if sig["id"] == "management-as-ai-superpower":
        # Enrich with Mollick's full thesis
        if "Mollick: 'Now the talent is abundant and cheap'" not in str(sig["dataPoints"]):
            sig["dataPoints"].extend([
                "Mollick full thesis: delegation to AI follows same frameworks as delegation to humans (Five Paragraph Order, PRDs, shot lists)",
                "Organizations with strong delegation cultures may adapt to AI faster (testable hypothesis)"
            ])
            sig["lastUpdated"] = "2026-02-10"
            sig["sessions"].append("podcast-conference-sweep-feb-10.json")
            print("  📝 Updated management-as-ai-superpower with Mollick thesis detail")

    if sig["id"] == "ai-agent-to-human-ratio-as-metric":
        # Add SaaStr data point
        if "SaaStr" not in str(sig["dataPoints"]):
            sig["dataPoints"].extend([
                "SaaStr/Lemkin: 10 SDRs/AEs → 20 AI agents + 1.2 humans (management ratio ~1:17)",
                "Lemkin predicts 'most SDRs and BDRs will be extinct within a year'"
            ])
            sig["lastUpdated"] = "2026-02-10"
            sig["sessions"].append("podcast-conference-sweep-feb-10.json")
            print("  📝 Updated ai-agent-to-human-ratio with SaaStr data")

    if sig["id"] == "saasmageddon-enterprise-restructuring":
        # Add Thompson detail
        if "agent-per-app vs cross-app" not in str(sig["dataPoints"]):
            sig["dataPoints"].extend([
                "Thompson (Stratechery): moats exist but corrections coming — more graduated than 'SaaS is dead'",
                "Agent-per-app vs cross-app orchestration as key structural question (who owns intelligence layer?)",
                "Microsoft Work IQ: using M365 data to create 'most valuable stateful agent'"
            ])
            sig["lastUpdated"] = "2026-02-10"
            sig["sessions"].append("podcast-conference-sweep-feb-10.json")
            print("  📝 Updated saasmageddon with Thompson detail")

data["lastUpdated"] = "2026-02-10T16:30:00Z"

with open(SIGNALS_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Field signals updated: {added} new signals added. Total: {len(data['signals'])}")
