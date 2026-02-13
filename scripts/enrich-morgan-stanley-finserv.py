#!/usr/bin/env python3
"""Enrich Morgan Stanley specimen with finserv natural experiment findings."""

import json
from pathlib import Path

SPECIMEN_PATH = Path(__file__).parent.parent / "specimens" / "morgan-stanley.json"

with open(SPECIMEN_PATH) as f:
    specimen = json.load(f)

# --- Add new sources ---
new_sources = [
    {
        "id": "morgan-stanley-firmwide-ai-page",
        "type": "corporate-website",
        "name": "Morgan Stanley — Artificial Intelligence Firmwide Team page",
        "url": "https://www.morganstanley.com/about-us/technology/artificial-intelligence-firmwide-team",
        "sourceDate": "2024-01-01",
        "collectedDate": "2026-02-10",
        "notes": "Division-specific AI products: AI@MS Assistant (WM), AI@MS Debrief (meetings), AskResearchGPT (IB). ML Research team publishes at NeurIPS, IJCAI, ICLR."
    },
    {
        "id": "ctomagazine-morgan-stanley-ai-2025",
        "type": "press",
        "name": "CTO Magazine — AI in Morgan Stanley: Shaping the Future of Financial Services",
        "url": "https://ctomagazine.com/ai-in-morgan-stanley-shaping-the-future-of-financial-services/",
        "sourceDate": "2025-01-01",
        "collectedDate": "2026-02-10",
        "notes": "David Wu as Head of Firmwide AI Product & Architecture Strategy. Document retrieval: 20% → 80% efficiency. Deep single-vendor OpenAI partnership with zero data retention policy."
    },
    {
        "id": "evident-bank-ai-talent-2025-ms",
        "type": "analyst-report",
        "name": "Evident Insights — Bank AI talent dynamics (Morgan Stanley)",
        "url": "https://evidentinsights.com/bankingbrief/who-is-poaching-whom-ai/",
        "sourceDate": "2025-01-01",
        "collectedDate": "2026-02-10",
        "notes": "Banks 3x more likely to hire top AI talent from other banks than from tech. 70% of AI model developers from academia."
    }
]

existing_source_ids = {s["id"] for s in specimen["sources"]}
for src in new_sources:
    if src["id"] not in existing_source_ids:
        specimen["sources"].append(src)

# --- Add new quotes ---
new_quotes = [
    {
        "text": "We believe in a very human-centric approach to Generative AI.",
        "speaker": "Morgan Stanley (institutional)",
        "speakerTitle": "Firmwide AI Team",
        "source": "morgan-stanley-firmwide-ai-page",
        "date": "2024-01-01",
        "context": "Core operating philosophy stated on firmwide AI team page"
    }
]

existing_quote_texts = {q.get("text", "") for q in specimen.get("quotes", [])}
for q in new_quotes:
    if q["text"] not in existing_quote_texts:
        specimen["quotes"].append(q)

# --- Update reportingStructure with co-president reporting, steering group detail ---
specimen["observableMarkers"]["reportingStructure"] = (
    "DEDICATED FIRMWIDE AI HEAD (M4 structural model): "
    "Jeff McMillan appointed Head of Firmwide AI (March 2024), co-reports to co-presidents "
    "Andy Saperstein and Dan Simkowitz — NOT to CTO or CIO. "
    "AI Steering Group co-chaired by McMillan and Katy Huberty (Head of Global Research) — "
    "co-chairing with Research Head signals AI seen as knowledge/research function, not primarily technology. "
    "David Wu as Head of Firmwide AI Product & Architecture Strategy (sub-function). "
    "Key collaborators: Mike Pizzi (Head of U.S. Banks & Technology), Sid Visentini (Head of Firm Strategy). "
    "McMillan background: headed WM Analytics, Data & Innovation — business/analytics leader, not technologist. "
    "Distributed domain AI leads in each business division (e.g., Koren Maranca in WM)."
)

# --- Update resourceAllocation with vendor strategy and metrics ---
specimen["observableMarkers"]["resourceAllocation"] = (
    "Deep single-vendor partnership with OpenAI (since March 2023) — zero data retention policy for security. "
    "Contrasts with Goldman's multi-model strategy. "
    "Three division-specific AI products: (1) AI@MS Assistant for WM advisors (ChatGPT, Sept 2023), "
    "(2) AI@MS Debrief for meeting summarization (2024), "
    "(3) AskResearchGPT for institutional securities/IB (GPT-4, 2024). "
    "Document retrieval efficiency: 20% → 80%. System answering any question from 100,000 documents. "
    "2,000 job cuts (March 2025) attributed partly to AI-driven efficiency. "
    "ML Research team publishes at NeurIPS 2024, IJCAI 2024, ICLR 2024. "
    "70% of new AI model developers hired from academia (Evident Insights)."
)

# --- Update metrics ---
specimen["observableMarkers"]["metrics"] = (
    "98% adoption rate among 16,000+ WM advisors (but advisors are ~15K of 80K+ employees — "
    "firmwide adoption rate unknown). "
    "10-15 hours/week projected productivity savings per advisor. "
    "Document retrieval efficiency: 20% → 80%. "
    "System progressed from answering 7,000 questions to answering any question from 100,000 documents."
)

# --- Add new layer ---
new_layer = {
    "date": "2026-02",
    "label": "Finserv Natural Experiment — Single-Vendor Deep Partnership",
    "summary": (
        "Financial services comparative research (Feb 10, 2026) confirms Morgan Stanley's "
        "unique structural position among top 3 banks: dedicated Firmwide AI Head (McMillan) "
        "reporting to co-presidents, NOT to CTO/CIO. Key differentiators: "
        "(1) Deep single-vendor OpenAI partnership vs. Goldman's multi-model and JPMorgan's build-internally, "
        "(2) Division-specific AI products (AI@MS, Debrief, AskResearchGPT) rather than single platform, "
        "(3) McMillan from WM analytics background, not technologist — same pattern as JPMorgan's Heitsenrether. "
        "AI Steering Group co-chaired with Research Head (Huberty), suggesting AI = knowledge function. "
        "ML Research team publishes at top conferences. 98% WM advisor adoption but firmwide rate unknown. "
        "Key contrast: Morgan Stanley was fastest to market (Sept 2023), Goldman prioritized infrastructure, "
        "JPMorgan deployed at scale with $2B investment."
    ),
    "classification": {
        "structuralModel": 4,
        "orientation": "Structural",
        "confidence": "High",
        "action": "enriched"
    },
    "sourceRefs": ["morgan-stanley-firmwide-ai-page", "ctomagazine-morgan-stanley-ai-2025", "evident-bank-ai-talent-2025-ms"]
}

# Insert as most recent layer
specimen["layers"].insert(0, new_layer)

# --- Update meta ---
specimen["meta"]["lastUpdated"] = "2026-02-10"

# --- Write back ---
with open(SPECIMEN_PATH, "w") as f:
    json.dump(specimen, f, indent=2, ensure_ascii=False)

print("✅ Morgan Stanley specimen enriched with finserv natural experiment findings")
print(f"   Sources: {len(specimen['sources'])}")
print(f"   Quotes: {len(specimen['quotes'])}")
print(f"   Layers: {len(specimen['layers'])}")
