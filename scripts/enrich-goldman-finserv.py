#!/usr/bin/env python3
"""Enrich Goldman Sachs specimen with finserv natural experiment findings."""

import json
from pathlib import Path

SPECIMEN_PATH = Path(__file__).parent.parent / "specimens" / "goldman-sachs.json"

with open(SPECIMEN_PATH) as f:
    specimen = json.load(f)

# --- Add new sources ---
new_sources = [
    {
        "id": "fortune-argenti-measured-approach-2025-finserv",
        "type": "press-interview",
        "name": "Fortune — Goldman Sachs CIO on measured AI approach (finserv comparative)",
        "url": "https://fortune.com/2025/03/19/goldman-sachs-cio-ai/",
        "sourceDate": "2025-03-19",
        "collectedDate": "2026-02-10",
        "notes": "Finserv natural experiment scan: AI Champions program from business divisions, multi-model plug-and-play, three-pillar framework, 23K/46K employee access."
    },
    {
        "id": "storyboard18-anthropic-partnership-2025",
        "type": "press",
        "name": "Storyboard18 — Goldman Sachs Anthropic partnership for digital co-workers",
        "url": "https://www.storyboard18.com/amp/brand-makers/goldman-sachs-teams-up-with-anthropic-to-build-ai-co-workers-aims-to-automate-complex-roles-89131.htm",
        "sourceDate": "2025-01-01",
        "collectedDate": "2026-02-10",
        "notes": "Anthropic engineers embedded within Goldman for 6-month co-development. Trade accounting, client vetting, compliance, reconciliation, pitchbook automation."
    },
    {
        "id": "evident-goldman-ai-conversation-2025",
        "type": "analyst-report",
        "name": "Evident Insights — How Goldman Drives the AI Conversation",
        "url": "https://evidentinsights.com/bankingbrief/how-goldman-drives-ai-conversation/",
        "sourceDate": "2025-01-01",
        "collectedDate": "2026-02-10",
        "notes": "Goldman in 1,200+ AI articles (25x average bank). Ranks 4th Innovation, 8th Talent in bank AI index. External narrative about thought leadership, not internal transformation."
    }
]

existing_source_ids = {s["id"] for s in specimen["sources"]}
for src in new_sources:
    if src["id"] not in existing_source_ids:
        specimen["sources"].append(src)

# --- Add new quotes ---
new_quotes = [
    {
        "text": "People might be afraid or skeptical when you drive technology first.",
        "speaker": "Marco Argenti",
        "speakerTitle": "CIO, Goldman Sachs",
        "sourceId": "fortune-argenti-measured-approach-2025-finserv",
        "context": "Explaining why Goldman uses non-technical AI Champions from business divisions rather than technologist-led adoption — contextual ambidexterity mechanism"
    },
    {
        "text": "We want to continue to plug-and-play with those models.",
        "speaker": "Marco Argenti",
        "speakerTitle": "CIO, Goldman Sachs",
        "sourceId": "fortune-argenti-measured-approach-2025-finserv",
        "context": "Explaining Goldman's multi-model vendor-agnostic AI strategy (Gemini, OpenAI, Llama) — contrasts with Morgan Stanley's deep single-vendor OpenAI partnership"
    },
    {
        "text": "[Infrastructure-first approach] might have slowed us down initially [but we are] picking up speed.",
        "speaker": "Marco Argenti",
        "speakerTitle": "CIO, Goldman Sachs",
        "sourceId": "evident-goldman-ai-conversation-2025",
        "context": "Acknowledging speed-to-deployment tradeoff of prioritizing GenAI infrastructure over quick application deployment"
    }
]

existing_quote_texts = {q.get("text", "") for q in specimen.get("quotes", [])}
for q in new_quotes:
    if q["text"] not in existing_quote_texts:
        specimen["quotes"].append(q)

# --- Update reportingStructure with AI Champions and deliberate no-CAIO ---
specimen["observableMarkers"]["reportingStructure"] = (
    "DELIBERATELY NO CHIEF AI OFFICER (unique among top 3 banks): "
    "CIO Marco Argenti serves as de facto AI leader, embedding AI governance within CIO office. "
    "Daniel Marcu (Global Head of AI Engineering & Science) works alongside Sharma (AI Platform) "
    "and Xiang (AI Research), likely reporting to Argenti. "
    "AI Steering Group plus risk/control teams evaluate proposals. "
    "AI Champions program: non-technical champions from business divisions (asset/wealth mgmt, "
    "private banking, trading) drive adoption. Argenti: 'People might be afraid or skeptical "
    "when you drive technology first.' Office of Applied Innovation co-headed by George Lee and Jared Cohen."
)

# --- Update resourceAllocation with Anthropic partnership ---
specimen["observableMarkers"]["resourceAllocation"] = (
    "Significant technology investment (reported $6B figure needs verification). "
    "12,000 developers with AI coding assistants (20-40% productivity gains). "
    "Firmwide GS AI Assistant: 23,000 of 46,000 employees have access (50%, March 2025), "
    "targeting near-universal access by end of 2025. "
    "Devin autonomous coder deployment. "
    "Multi-model strategy: GPT-4, Gemini, Claude, Llama — 'plug-and-play.' "
    "Anthropic engineers embedded within Goldman for 6-month co-development period "
    "building 'digital co-workers' for trade accounting, compliance, reconciliation, pitchbooks. "
    "Argenti: infrastructure-first approach 'might have slowed us down initially.'"
)

# --- Add new layer ---
new_layer = {
    "date": "2026-02",
    "label": "Finserv Natural Experiment — No-CAIO Contextual Model",
    "summary": (
        "Financial services comparative research (Feb 10, 2026) confirms Goldman's deliberate "
        "structural divergence from JPMorgan and Morgan Stanley: NO Chief AI Officer, AI embedded "
        "in CIO office. Key mechanisms: (1) AI Champions from business divisions, not technologists, "
        "(2) multi-model vendor-agnostic strategy (Gemini, OpenAI, Llama, Anthropic), "
        "(3) Anthropic engineers embedded within Goldman for 6-month co-development. "
        "Argenti acknowledges infrastructure-first 'might have slowed us down initially.' "
        "Goldman appears in 1,200+ AI articles (25x average bank) but reveals little about "
        "internal structure — deliberate opacity. Ranks 4th Innovation, 8th Talent in Evident bank AI index. "
        "Three-pillar framework: data quality + AI technology + organizational change management. "
        "Key contrast: Goldman keeps AI IN the CIO office; JPMorgan took AI OUT of technology; "
        "Morgan Stanley created a new role parallel to technology."
    ),
    "classification": {
        "structuralModel": 6,
        "orientation": "Contextual",
        "confidence": "High",
        "action": "enriched"
    },
    "sourceRefs": ["fortune-argenti-measured-approach-2025-finserv", "storyboard18-anthropic-partnership-2025", "evident-goldman-ai-conversation-2025"]
}

# Insert as most recent layer
specimen["layers"].insert(0, new_layer)

# --- Update meta ---
specimen["meta"]["lastUpdated"] = "2026-02-10"

# --- Write back ---
with open(SPECIMEN_PATH, "w") as f:
    json.dump(specimen, f, indent=2, ensure_ascii=False)

print("✅ Goldman Sachs specimen enriched with finserv natural experiment findings")
print(f"   Sources: {len(specimen['sources'])}")
print(f"   Quotes: {len(specimen['quotes'])}")
print(f"   Layers: {len(specimen['layers'])}")
