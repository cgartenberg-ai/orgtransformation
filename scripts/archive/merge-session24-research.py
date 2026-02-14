#!/usr/bin/env python3
"""
Merge Session 24 research agent outputs into queue.json and source-registry.json.
7 agents completed on 2026-02-12:
  1. podcast-substack-sweep-feb-2026
  2. press-sweep-feb-2026
  3. caio-reorg-discovery-feb-2026
  4. xai-deep-scan-feb-2026
  5. intuit-caio-deep-scan-feb-2026
  6. klarna-ai-backfire-feb-2026
  7. salesforce-evolution-feb-2026
"""

import json
from datetime import datetime

BASE = "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation"

# ── Load current files ──
with open(f"{BASE}/research/queue.json", "r") as f:
    queue = json.load(f)

with open(f"{BASE}/specimens/source-registry.json", "r") as f:
    source_reg = json.load(f)

# ── 1. Add queue entries for all 7 agent outputs ──

new_queue_entries = [
    {
        "sessionFile": "research/pending/podcast-substack-sweep-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "Tier 1 Podcasts + Substacks feed check (No Priors, Acquired, BG2, Latent Space, Stratechery, Mollick, Pragmatic Engineer) — Feb 3-12 window",
        "organizationsFound": [
            "rivian",
            "meta-ai"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "Rivian (new, MEDIUM priority — VP Autonomy, in-house silicon, vertical integration). Meta Compute pivot (HIGH — structural reallocation from Reality Labs to AI infra, update existing specimen). Lila Sciences (LOW, thin). BG2 on hiatus. Acquired no new eps."
    },
    {
        "sessionFile": "research/pending/press-sweep-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "Tier 1 Press keyword sweep (WSJ, FT, Reuters, Bloomberg, CNBC, Fortune) — Feb 1-12, 2026",
        "organizationsFound": [
            "xai",
            "salesforce",
            "amazon-agi",
            "pinterest",
            "workday",
            "dow-chemical",
            "klarna",
            "lionsgate",
            "kyndryl",
            "infosys",
            "asml"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "xAI (new specimen — 4 divisions, SpaceX merger, co-founder exodus). Salesforce (major update — 5 departures, Inzerillo consolidation). Amazon (30K total cuts, management delayering). Pinterest (15% layoffs + internal dissent). Workday (founder return as CEO). Dow 'Transform to Outperform'. ASML (counter-example: restructuring NOT AI-driven). 5 broader trends: AI-washing debate, CAIO institutionalization, sequential layoff waves, Deloitte AI-native framework, management layer elimination. 5 purpose claims."
    },
    {
        "sessionFile": "research/pending/caio-reorg-discovery-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "CAIO Appointments + AI Restructuring Discovery — Feb 1-12, 2026",
        "organizationsFound": [
            "xai",
            "lionsgate",
            "fda-hhs",
            "sk-telecom",
            "columbia-group",
            "anthropic",
            "amazon-agi",
            "dow-chemical",
            "hp",
            "intuit",
            "uk-government",
            "liverpool-city-region",
            "verses-ai"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "Anthropic Labs reshuffle (Krieger→Labs, Vora new product head, Sharma safety departure — HIGH). SK Telecom CIC→CTO promotion (HIGH). Intuit Foresight unit discovery (HIGH — led to deep scan). Lionsgate first entertainment CAIO. FDA/HHS federal CAIO appointments. UK govt + Liverpool regional CAIO. VERSES AI founder-to-operator transition. 7 purpose claims."
    },
    {
        "sessionFile": "research/pending/xai-deep-scan-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "xAI Deep Structural Scan — post-restructuring Feb 2026",
        "organizationsFound": [
            "xai"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "Deep scan: 4 product divisions (Grok, Coding, Imagine, Macrohard), SpaceX acquisition ($1T+$250B), 6/12 co-founders departed, Macrohard 'AI-agent software company' division, 1000+ employees, MACROHARDRR $20B data center, public all-hands video. 8 rich purpose claims including departing co-founders. Musk explicitly frames explore→execute transition."
    },
    {
        "sessionFile": "research/pending/intuit-caio-deep-scan-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "Intuit CAIO Deep Scan — Intuit Foresight, GenOS, three-pillar AI org",
        "organizationsFound": [
            "intuit"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "NEW specimen candidate — richest new discovery. M4 hub-spoke with 'Intuit Foresight' unit (merged AI + Futures teams), GenOS platform (4 components), 3-pillar AI org, dual AI tracks (outward Foresight + inward CoE), three-level goal framework. Key leaders: Srivastava (CAIO), Balazs (CTO), Lazarov (VP Tech), Ho (VP AI), Goodarzi (CEO). Reconstructed org chart, $100M+ OpenAI deal, multi-model strategy. 9 purpose claims from 4 different leaders. Assessment: HIGH — ready for curation."
    },
    {
        "sessionFile": "research/pending/klarna-ai-backfire-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "Klarna AI Backfire Deep Scan — complete reversal timeline 2022-2026",
        "organizationsFound": [
            "klarna"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "Complete reversal timeline: 22% customer satisfaction drop, emergency cross-functional redeployment (engineers to call centers), 'Uber-style' hybrid rehiring model, IPO at $40 → stock below $31, investor class-action lawsuit, EU AI Act regulatory risk. CEO admission: 'cost unfortunately seems to have been a too predominant evaluation factor'. 5 purpose claims showing rhetorical arc from 'AI can do all jobs' to 'we went too far'. Agent notes: 'the single most valuable counter-example in our entire specimen collection.'"
    },
    {
        "sessionFile": "research/pending/salesforce-evolution-feb-2026.json",
        "sessionDate": "2026-02-12",
        "source": "Salesforce Evolution Deep Scan — executive exodus + Agentforce consolidation Feb 2026",
        "organizationsFound": [
            "salesforce"
        ],
        "status": "pending",
        "curatedIn": None,
        "notes": "5 executive departures in 3 months (Dresser→OpenAI, Arkin, Aytay, Evans→startups, Kelman→AMD). 6 replacements. Inzerillo promoted to President Enterprise & AI Technology (consolidating Agentforce + Slack). Slack demoted from CEO-led to EVP/GM-led. 3 AI leaders in <3 years: Shih→Evans→Thattai (narrowing scope each time). Customer Zero model. Feb 2026 layoffs hitting Agentforce team itself. Benioff augmentation→replacement rhetorical arc. 12 rich purpose claims."
    }
]

queue["queue"].extend(new_queue_entries)
queue["lastUpdated"] = "2026-02-12"

# ── 2. Update source-registry.json scan dates ──

source_updates = {
    "no-priors": {
        "scannedThrough": "Through Ep 151 (Feb 12, 2026) — Rivian/Scaringe ep. Roblox/Baszucki (Feb 5) and Deming (Jan 29) also noted.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "acquired": {
        "scannedThrough": "No new full episode since NFL 2026 Update (Jan 26). Super Bowl Innovation Summit Feb 6 — NOT org-structural.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "bg2-pod": {
        "scannedThrough": "No new episodes since Dec 23, 2025 (AI Enterprise — Databricks & Glean). Appears on hiatus.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "latent-space": {
        "scannedThrough": "Through Feb 12, 2026. 'Scientist and Simulator' (Feb 10), AI News, adversarial reasoning essay. Active but technical/research-focused, low org-structural density.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "stratechery": {
        "scannedThrough": "Through Feb 12, 2026. 'AI and the Human Condition' (Feb 11), 'AI Power Now and In 100 Years' (Feb 9), Benedict Evans interview (Feb 5, paywalled), 'Technology Doings' (Meta Compute), 'Chip Fly' (chip shortage).",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "one-useful-thing": {
        "scannedThrough": "No new posts since 'Management as AI superpower' (Jan 27, 2026). No Feb 2026 content found.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "pragmatic-engineer": {
        "scannedThrough": "Through Feb 12, 2026. Kotlin AI podcast (Feb 12), Steve Yegge AI agents (Feb 10), Grady Booch (Feb 4), 10 tech companies dev tools (Feb 3). Pragmatic Summit held Feb 11 — content not yet published.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "earnings-calls": {
        "scannedThrough": "Through Feb 12, 2026. Q4 2025 earnings sweep: Google (Feb 4), Amazon (Feb 5) previously pending — JPM Healthcare Conference scanned. Salesforce Q4 FY2026 upcoming Feb 25.",
        "scannedThroughDate": "2026-02-12",
        "lastScanned": "2026-02-12"
    },
    "jpm-healthcare-conference": {
        "lastScanned": "2026-02-12"
    }
}

# Apply updates
for source in source_reg["sources"]:
    sid = source["id"]
    if sid in source_updates:
        for key, val in source_updates[sid].items():
            source[key] = val
        # Add session file reference if not present
        session_ref = "research/pending/podcast-substack-sweep-feb-2026.json"
        if sid in ["no-priors", "acquired", "bg2-pod", "latent-space", "stratechery", "one-useful-thing", "pragmatic-engineer"]:
            if session_ref not in source.get("sessionFiles", []):
                source.setdefault("sessionFiles", []).append(session_ref)

# Also add press sources session files
press_session_ref = "research/pending/press-sweep-feb-2026.json"
caio_session_ref = "research/pending/caio-reorg-discovery-feb-2026.json"
for source in source_reg["sources"]:
    sid = source["id"]
    if sid in ["wsj", "ft", "reuters-business", "bloomberg-tech", "the-information", "cnbc", "fortune"]:
        source["scannedThroughDate"] = "2026-02-12"
        source["lastScanned"] = "2026-02-12"
        source["scannedThrough"] = f"Keyword sweep through Feb 12, 2026 via press-sweep and CAIO-reorg-discovery agents."
        for ref in [press_session_ref, caio_session_ref]:
            if ref not in source.get("sessionFiles", []):
                source.setdefault("sessionFiles", []).append(ref)

source_reg["lastUpdated"] = "2026-02-12T12:00:00Z"

# ── 3. Write updated files ──

with open(f"{BASE}/research/queue.json", "w") as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
    f.write("\n")

with open(f"{BASE}/specimens/source-registry.json", "w") as f:
    json.dump(source_reg, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("✓ queue.json updated — 7 new entries added")
print("✓ source-registry.json updated — scan dates refreshed")
print(f"  Total queue entries: {len(queue['queue'])}")
print(f"  Total sources tracked: {len(source_reg['sources'])}")
