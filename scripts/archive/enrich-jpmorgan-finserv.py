#!/usr/bin/env python3
"""Enrich JPMorgan specimen with financial services natural experiment research findings."""

import json
from pathlib import Path

SPECIMEN_PATH = Path(__file__).parent.parent / "specimens" / "jpmorgan.json"

with open(SPECIMEN_PATH) as f:
    specimen = json.load(f)

# --- Add new sources ---
new_sources = [
    {
        "id": "constellation-dimon-ai-2025",
        "type": "analyst-report",
        "name": "Constellation Research — JPMorgan Chase Dimon on AI, Data, Cybersecurity",
        "url": "https://www.constellationr.com/blog-news/insights/jpmorgan-chases-dimon-ai-data-cybersecurity-and-managing-tech-shifts",
        "timestamp": None,
        "sourceDate": "2025-01-01",
        "collectedDate": "2026-02-10",
        "notes": "Dimon: 'We took AI and data out of technology. It's too important.' Veloso as AI Research head. 600 use cases. $2B AI spend / $18B IT budget."
    },
    {
        "id": "pymnts-heitsenrether-2023",
        "type": "press",
        "name": "PYMNTS — JPMorgan names Heitsenrether as head of new AI unit",
        "url": "https://www.pymnts.com/artificial-intelligence-2/2023/jpmorgan-names-exec-teresa-heitsenrether-as-head-of-new-unit-in-ai-push/",
        "timestamp": None,
        "sourceDate": "2023-06-21",
        "collectedDate": "2026-02-10",
        "notes": "Heitsenrether appointed first CDAO. Background: 8 years heading securities services ($29.7T AUC). Reports to President Daniel Pinto."
    },
    {
        "id": "evident-bank-ai-talent-2025",
        "type": "analyst-report",
        "name": "Evident Insights — Who is poaching whom in AI talent",
        "url": "https://evidentinsights.com/bankingbrief/who-is-poaching-whom-ai/",
        "timestamp": None,
        "sourceDate": "2025-01-01",
        "collectedDate": "2026-02-10",
        "notes": "JPMorgan talent dynamics: lost quantum computing leaders (Pistoia, Lim), AI research director Lecue to Wells Fargo. 70% of new AI hires from academia."
    }
]

existing_source_ids = {s["id"] for s in specimen["sources"]}
for src in new_sources:
    if src["id"] not in existing_source_ids:
        specimen["sources"].append(src)

# --- Add new quotes ---
new_quotes = [
    {
        "text": "We took AI and data out of technology. It's too important.",
        "speaker": "Jamie Dimon",
        "speakerTitle": "CEO, JPMorgan Chase",
        "sourceId": "constellation-dimon-ai-2025",
        "context": "Explaining why JPMorgan structurally separated AI/data from the technology org and elevated it to Operating Committee level"
    },
    {
        "text": "The head of AI is at every single meeting he has with management teams.",
        "speaker": "Jamie Dimon",
        "speakerTitle": "CEO, JPMorgan Chase",
        "sourceId": "constellation-dimon-ai-2025",
        "context": "Describing how AI leadership is embedded in all management conversations despite structural separation — structural separation with contextual integration"
    },
    {
        "text": "There will be no job, no process, no function that won't be affected by AI -- mostly for the positive.",
        "speaker": "Jamie Dimon",
        "speakerTitle": "CEO, JPMorgan Chase",
        "sourceId": "constellation-dimon-ai-2025",
        "context": "Justifying universal AI impact as rationale for organizational elevation to Operating Committee"
    }
]

existing_quote_texts = {q.get("text", "") for q in specimen.get("quotes", [])}
for q in new_quotes:
    if q["text"] not in existing_quote_texts:
        specimen["quotes"].append(q)

# --- Update reporting structure with dual-track finding ---
specimen["observableMarkers"]["reportingStructure"] = (
    "DUAL-TRACK AI LEADERSHIP (unique among top 3 banks): "
    "(1) Teresa Heitsenrether as Chief Data & Analytics Officer — applied AI/data/analytics, "
    "sits on Operating Committee, reports to President Daniel Pinto. Background: 8 years heading "
    "securities services ($29.7T AUC) — business/ops leader, not technologist. "
    "(2) Dr. Manuela Veloso as Head of AI Research — academic research function, reports "
    "directly to Dimon/president level. SEPARATE reporting line from Heitsenrether. "
    "A.J. Lang named CIO for data/analytics org, matrix-reporting to both Heitsenrether and "
    "firm CIO Lori Beer. David Wu as Head of Firmwide AI Product & Architecture Strategy. "
    "Dimon: 'We took AI and data out of technology. It's too important.' "
    "AI head attends every management meeting."
)

# --- Update resource allocation ---
specimen["observableMarkers"]["resourceAllocation"] = (
    "$2B annual AI investment within $18B total IT budget (11% of IT spend). "
    "600 active AI use cases deployed, expecting to double within a year. "
    "Investments across 100 different companies for testing and learning (venture-style scanning). "
    "2,000 AI/ML specialists across 3 continents. "
    "2026 total expense guidance: $105B with 'meaningful growth' driven by tech/AI spending."
)

# --- Update decision rights ---
specimen["observableMarkers"]["decisionRights"] = (
    "AI head attends every management meeting (Dimon mandate). "
    "Operating Committee membership for CDAO = same organizational authority as business line heads. "
    "Matrix reporting between new AI/data org and existing CIO org (A.J. Lang dual reports). "
    "LLM Suite updated on 8-week cycle with expanding capabilities."
)

# --- Update open questions ---
specimen["openQuestions"] = [
    "How do Heitsenrether (applied CDAO) and Veloso (AI Research) coordinate? Is there a formal mechanism or is it through Dimon's management meetings?",
    "What happened to Derek Waldron (previously CAO)? Did Heitsenrether's appointment supersede or restructure that role?",
    "What is the composition of the 100-company AI investment portfolio? Is this managed through JPMorgan's venture arm or the CDAO org?",
    "How does the branch/call center exclusion from LLM Suite get resolved? Is there a timeline for customer-facing AI deployment?",
    "JPMorgan lost key AI talent (Pistoia, Lim, Lecue) — is the dual-track structure a retention response, or did the losses trigger the restructuring?"
]

# --- Add new layer ---
new_layer = {
    "date": "2026-02",
    "label": "Dual-Track AI Leadership Confirmed",
    "summary": "Financial services comparative research (Feb 10, 2026) reveals JPMorgan has a UNIQUE dual-track AI leadership structure among top 3 US banks: (1) Heitsenrether (CDAO, applied) on Operating Committee reporting to President Pinto, and (2) Veloso (AI Research, academic) reporting directly to Dimon/president level. These are SEPARATE reporting lines — textbook Tushman & O'Reilly ambidextrous design applied to AI. Dimon's rationale: 'We took AI and data out of technology. It's too important.' 600 active use cases, $2B AI spend within $18B IT budget. AI head attends every management meeting. Key contrast: Goldman embeds AI in CIO office, Morgan Stanley created single firmwide AI head — only JPMorgan structurally separates exploration (Veloso) from exploitation (Heitsenrether) at the C-suite level.",
    "classification": {
        "structuralModel": 4,
        "orientation": "Structural",
        "confidence": "High",
        "action": "enriched"
    },
    "sourceRefs": ["constellation-dimon-ai-2025", "pymnts-heitsenrether-2023", "evident-bank-ai-talent-2025"]
}

# Insert as most recent layer
specimen["layers"].insert(0, new_layer)

# --- Update meta ---
specimen["meta"]["lastUpdated"] = "2026-02-10"
specimen["meta"]["completeness"] = "High"

# --- Write back ---
with open(SPECIMEN_PATH, "w") as f:
    json.dump(specimen, f, indent=2, ensure_ascii=False)

print("✅ JPMorgan specimen enriched with finserv natural experiment findings")
print(f"   Sources: {len(specimen['sources'])}")
print(f"   Quotes: {len(specimen['quotes'])}")
print(f"   Layers: {len(specimen['layers'])}")
print(f"   Open questions: {len(specimen['openQuestions'])}")
