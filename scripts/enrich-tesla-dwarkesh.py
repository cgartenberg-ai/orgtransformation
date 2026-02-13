#!/usr/bin/env python3
"""Enrich Tesla specimen with Dwarkesh-Musk interview findings (Feb 5, 2026)."""

import json
from pathlib import Path

SPECIMEN_PATH = Path(__file__).parent.parent / "specimens" / "tesla.json"

with open(SPECIMEN_PATH) as f:
    specimen = json.load(f)

# --- Add new source ---
new_source = {
    "id": "dwarkesh-musk-feb-2026",
    "type": "Podcast",
    "name": "Dwarkesh Podcast — Elon Musk: 'In 36 months, the cheapest place to put AI will be space'",
    "url": "https://www.dwarkesh.com/p/elon-musk",
    "timestamp": None,
    "sourceDate": "2026-02-05",
    "collectedDate": "2026-02-10",
    "notes": "~2h50m interview. Covers xAI org identity, Tesla AI chip sharing, Optimus Academy, reality generator reuse, Optimus production scaling."
}

# Check if already exists
existing_source_ids = [s["id"] for s in specimen["sources"]]
if new_source["id"] not in existing_source_ids:
    specimen["sources"].append(new_source)

# --- Add new quotes ---
new_quotes = [
    {
        "text": "We'll use the same Tesla AI chips in the robot as in the car. We'll use the same basic principles.",
        "speaker": "Elon Musk",
        "speakerTitle": "CEO, Tesla",
        "sourceId": "dwarkesh-musk-feb-2026",
        "context": "Explaining platform-sharing across FSD and Optimus product lines — one hardware/software architecture serving two product lines"
    },
    {
        "text": "We're going to need to build a lot of robots and put them in kind of an Optimus Academy so they can do self-play in reality.",
        "speaker": "Elon Musk",
        "speakerTitle": "CEO, Tesla",
        "sourceId": "dwarkesh-musk-feb-2026",
        "context": "Describing dedicated physical training facility for 10,000-30,000 Optimus robots in self-play learning"
    },
    {
        "text": "Tesla has quite a good reality generator, a physics-accurate reality generator, that we made for the cars. We'll do the same thing for the robots.",
        "speaker": "Elon Musk",
        "speakerTitle": "CEO, Tesla",
        "sourceId": "dwarkesh-musk-feb-2026",
        "context": "Internal capability transfer — simulation asset built for FSD being repurposed for Optimus training"
    }
]

# Add quotes (Tesla had none)
if not specimen.get("quotes"):
    specimen["quotes"] = []
for q in new_quotes:
    # Dedupe by text
    if not any(existing.get("text") == q["text"] for existing in specimen["quotes"]):
        specimen["quotes"].append(q)

# --- Add new layer ---
new_layer = {
    "date": "2026-02",
    "label": "Platform-Sharing & Optimus Academy",
    "summary": "Dwarkesh interview (Feb 5, 2026) reveals Tesla's platform-sharing structural strategy: same AI chips and architectural principles across car (FSD) and robot (Optimus) platforms. Plans for 'Optimus Academy' — dedicated physical training facility with 10,000-30,000 robots doing self-play, supplemented by millions of simulated robots. Tesla's 'physics-accurate reality generator' built for car simulation will be repurposed for robot training — internal capability transfer reducing development costs. Production roadmap: Gen 3 at ~1M units/year, Gen 4 at ~10M units/year. xAI's Grok positioned as orchestration layer for Optimus robot coordination.",
    "classification": None,
    "sourceRefs": ["dwarkesh-musk-feb-2026"]
}

# Add after most recent layer
specimen["layers"].insert(0, new_layer)

# --- Update observable markers ---
specimen["observableMarkers"]["resourceAllocation"] = (
    "$20B+ CapEx forecast for 2026 AI infrastructure. "
    "Platform-sharing across FSD and Optimus: same AI chips, same reality generator, same architectural principles. "
    "Optimus Academy: dedicated physical training facility for 10,000-30,000 robots in self-play learning. "
    "xAI's Grok as orchestration layer for Optimus coordination (cross-entity dependency)."
)

# --- Update open questions ---
specimen["openQuestions"] = [
    "What does 'Operation Maestro' actually entail structurally?",
    "How is Tesla's AI team (FSD, Optimus, Dojo) organized internally?",
    "What's the reporting line for AI vs. automotive?",
    "How does the xAI-Tesla relationship work structurally? Musk declined to discuss on Dwarkesh citing public company constraints.",
    "What is the division of labor between xAI (Grok) and Tesla AI (FSD/Optimus)? Is Grok the 'brain' and Tesla the 'body'?",
    "Optimus Academy: where will it be built, what's the timeline, how does it interface with factory operations?"
]

# --- Update description to include platform-sharing ---
specimen["description"] = (
    "Tesla operates AI as a deeply integrated product capability rather than a separate organizational "
    "function. The company's 1.5 million-car fleet functions as a distributed data collection "
    "infrastructure, generating 1.5 petabytes per week of training data that feeds the FSD neural "
    "network. This 'fleet as distributed lab' model means customers are co-producers of the AI training "
    "dataset — a radically distributed innovation pipeline.\n\n"
    "A key structural decision is platform-sharing across product lines: Tesla uses the same AI chips "
    "and architectural principles in both cars (FSD) and robots (Optimus). The company's 'physics-accurate "
    "reality generator' built for car simulation is being repurposed for robot training — internal "
    "capability transfer that reduces development costs. Plans for an 'Optimus Academy' envision "
    "10,000-30,000 robots in a dedicated physical training facility for self-play learning, supplemented "
    "by millions of simulated robots. Production ambitions scale to Gen 3 (~1M/year) and Gen 4 (~10M/year).\n\n"
    "The organizational structure faces an unusual tension: massive AI investment ($20B+ CapEx for 2026) "
    "during automotive contraction (first-ever annual revenue decline). 'Operation Maestro' represents "
    "internal reorganization with significant expense impact. Meanwhile, xAI's Grok model is positioned "
    "as an orchestration layer for Optimus robots, creating a cross-entity dependency where xAI provides "
    "the intelligence layer and Tesla provides the physical execution layer. Musk declined to discuss "
    "the xAI-Tesla structural relationship publicly, citing public company constraints."
)

# --- Update meta ---
specimen["meta"]["lastUpdated"] = "2026-02-10"
specimen["meta"]["completeness"] = "Medium"

# --- Write back ---
with open(SPECIMEN_PATH, "w") as f:
    json.dump(specimen, f, indent=2, ensure_ascii=False)

print("✅ Tesla specimen enriched with Dwarkesh-Musk interview data")
print(f"   Sources: {len(specimen['sources'])}")
print(f"   Quotes: {len(specimen['quotes'])}")
print(f"   Layers: {len(specimen['layers'])}")
print(f"   Open questions: {len(specimen['openQuestions'])}")
