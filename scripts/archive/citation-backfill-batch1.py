#!/usr/bin/env python3
"""
Citation backfill: Add inline [source-id] markers to observable markers for
high-completeness specimens. Each fact gets traced to the source that reported it.

Batch 1: bank-of-america, eli-lilly, goldman-sachs, google-deepmind, honeywell,
          morgan-stanley, netflix, disney, sutter-health, unitedhealth-group
"""

import json
import os
import re
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ── Citation mappings: specimen_id → updated observableMarkers ────────────
# Each fact in observable markers is traced to the source that reported it.
# Source IDs must match entries in the specimen's sources array.

UPDATES = {
    # ── BANK OF AMERICA ──────────────────────────────────────────────────
    "bank-of-america": {
        "reportingStructure": "No separate AI organization. AI tools embedded in existing functional structures [bofa-newsroom].",
        "resourceAllocation": "$14B technology budget with $4.5B specifically allocated to AI — the largest disclosed AI-specific budget among traditional banks [startupnews-ai-spending]. Investment through technology budget, not a separate ring-fenced AI organization [bofa-newsroom].",
        "timeHorizons": "Incremental expansion of consumer-proven interfaces. Quarterly feature additions building on established patterns [bofa-newsroom]. Management expects agentic AI to lower efficiency ratio 100-200bps over next 24 months [finterra-agentic-ai].",
        "decisionRights": "Technology leadership drives platform; adoption is expected across all roles [bofa-newsroom].",
        "metrics": "Erica: 20.6M users (up from 19.7M YoY), 169M interactions in Q4 2025 [pymnts-q4-2025-earnings]. Over 90% of 213,000 employees use AI tools daily [bofa-newsroom]. IT service desk calls reduced 50%+ [cto-magazine]. Developer efficiency up 20% [cto-magazine]. Headcount from 300K to 212K over 15 years [bofa-newsroom]. $6B expense savings [bofa-newsroom]."
    },

    # ── ELI LILLY ────────────────────────────────────────────────────────
    "eli-lilly": {
        "reportingStructure": "Hubs report to R&D leadership, not business unit heads [cheeky-pint-2025]. NVIDIA lab is a joint venture structure [nvidia-newsroom-2026]. New therapeutic area presidents (Neuroscience, Immunology) added to leadership team in 2025 [lilly-earnings-q4-2025].",
        "resourceAllocation": "R&D investment target: 20-25% of sales [chief-exec-2025]. At $120B revenue, R&D budget approaches NIH scale. $1B committed to NVIDIA partnership over five years [nvidia-newsroom-2026]. $55B+ committed to manufacturing expansion since 2020 [lilly-earnings-q4-2025].",
        "timeHorizons": "Decades, not quarters. The GLP-1 program exemplifies an 18+ year horizon from first injection to commercial product [cheeky-pint-2025].",
        "decisionRights": "Hub leaders have significant autonomy [cheeky-pint-2025]. CEO actively protects off-strategy work from middle management optimization [cheeky-pint-2025].",
        "metrics": "Drug development cycle ~7 years vs. industry average of 10 [chief-exec-2025]. 300-400 person hub size [cheeky-pint-2025]. 1,016 Blackwell Ultra GPUs (9+ exaflops) [fiercebiotech-2026]. 36 active Phase III programs [lilly-earnings-q4-2025]. 14 new Phase III programs initiated recently [lilly-earnings-q4-2025]. 39 BD transactions in 2025 [lilly-earnings-q4-2025]."
    },

    # ── GOLDMAN SACHS ────────────────────────────────────────────────────
    "goldman-sachs": {
        "reportingStructure": "DELIBERATELY NO CHIEF AI OFFICER (unique among top 3 banks): CIO Marco Argenti serves as de facto AI leader, embedding AI governance within CIO office [fortune-argenti-measured-approach-2025]. Daniel Marcu (Global Head of AI Engineering & Science) works alongside Sharma (AI Platform) and Xiang (AI Research), likely reporting to Argenti [digital-watch-marcu-2025]. AI Steering Group plus risk/control teams evaluate proposals [fortune-argenti-measured-approach-2025]. AI Champions program: non-technical champions from business divisions (asset/wealth mgmt, private banking, trading) drive adoption [fortune-argenti-measured-approach-2025-finserv]. Argenti: 'People might be afraid or skeptical when you drive technology first' [fortune-argenti-measured-approach-2025-finserv]. Office of Applied Innovation co-headed by George Lee and Jared Cohen [nanonets-gs-platform-2025].",
        "resourceAllocation": "Significant technology investment (reported $6B figure needs verification) [nanonets-gs-platform-2025]. 12,000 developers with AI coding assistants (20-40% productivity gains) [ibm-think-devin-2025]. Firmwide GS AI Assistant: 23,000 of 46,000 employees have access (50%, March 2025), targeting near-universal access by end of 2025 [foxbusiness-gs-ai-assistant-2025]. Devin autonomous coder deployment [ibm-think-devin-2025]. Multi-model strategy: GPT-4, Gemini, Claude, Llama — 'plug-and-play' [fortune-argenti-measured-approach-2025-finserv]. Anthropic engineers embedded within Goldman for 6-month co-development period building 'digital co-workers' for trade accounting, compliance, reconciliation, pitchbooks [storyboard18-anthropic-partnership-2025]. Argenti: infrastructure-first approach 'might have slowed us down initially' [evident-goldman-ai-conversation-2025].",
        "timeHorizons": "Solomon frames as 3-5 year transformation: 'If you take a three to five year view, it's giving us more capacity to invest in our business' [fortune-solomon-job-apocalypse-2026]. CFO Coleman describes OneGS 3.0 as multiyear initiative [fortune-coleman-ai-reboot-2025]. Long-term economic outlook of 5-10 years for 'enormous productivity gains' [time-solomon-davos-2026].",
        "decisionRights": "Argenti articulates clear principle: 'You can delegate work, but you cannot delegate accountability' [russell-reynolds-argenti-podcast-2025]. AI steering group governs use case prioritization [fortune-argenti-measured-approach-2025]. Six workstreams each have specific operational targets [fortune-coleman-ai-reboot-2025]. 'Shark Tank'-style developer competitions for innovation (structure unclear) [nanonets-gs-platform-2025].",
        "metrics": "Developer productivity: 20-40% gains on standard coding tasks [ibm-think-devin-2025]. Adoption: 50% of 46,000 employees had AI access by mid-2025 [foxbusiness-gs-ai-assistant-2025]. Client adoption survey: 37% using AI for production (Oct 2025), expected 50% next year, 74% within three years [constellation-gs-transformation-2025]."
    },

    # ── GOOGLE DEEPMIND ──────────────────────────────────────────────────
    "google-deepmind": {
        "reportingStructure": "Demis Hassabis leads unified Google DeepMind [source-3]. Reports to Sundar Pichai [fool-alphabet-q4-2025].",
        "resourceAllocation": "CapEx guidance: $175-185B for 2026 (nearly doubling from $91.4B in 2025) [fool-alphabet-q4-2025]. Breakdown: 60% servers/compute, 40% data centers/networking [fool-alphabet-q4-2025]. Half of ML compute allocated to Cloud [fool-alphabet-q4-2025]. Continued hiring in AI and Cloud [fool-alphabet-q4-2025].",
        "timeHorizons": "Supply-constrained through 2026 — demand outpacing capacity buildout [fool-alphabet-q4-2025-feb].",
        "decisionRights": None,  # keep null
        "metrics": "2,500 to 5,600 employees (post-merger) [source-3]. Gemini: 750M MAU (up from 650M Q3), 10B+ tokens/day via API [fool-alphabet-q4-2025]. Gemini 3 Pro processes 3x daily tokens vs 2.5 Pro [fool-alphabet-q4-2025]. 8M+ paid Gemini Enterprise seats [fool-alphabet-q4-2025]. 120,000+ enterprises using Gemini [fool-alphabet-q4-2025]. Gemini serving costs down 78% in 2025 [fool-alphabet-q4-2025]. Google Cloud backlog: $240B (+55% QoQ from $155B) [fool-alphabet-q4-2025]. ~50% of Google code now AI-generated [fool-alphabet-q4-2025-feb]. Alphabet Q4 2025: $97.23B revenue (+19% YoY), EPS $2.82 [fool-alphabet-q4-2025]."
    },

    # ── HONEYWELL ────────────────────────────────────────────────────────
    "honeywell": {
        "reportingStructure": "Gen AI program leader → Sheila Jordan (CDTO) [honeywell-fortune-ai-chiefs-2025]. Jordan and CTO Venkatarayalu are peers, splitting internal AI vs product AI [honeywell-fortune-ai-chiefs-2025]. Both appear to report to CEO Kapur [honeywell-fortune-ceo-ai-strategy-2024].",
        "resourceAllocation": "Dedicated gen AI program with central budget and ambassador network [honeywell-fortune-ai-chiefs-2025]. Consolidated from 4,500 to ~1,000 applications before AI investment [honeywell-cio-gen-ai-2024]. Enterprise data warehouse (Snowflake) as foundation [honeywell-cio-gen-ai-2024]. 600 engineers added to R&D workforce in 2025 [honeywell-q4-2025-earnings].",
        "timeHorizons": "Short-term: 24+ production use cases available to all 95,000 employees [honeywell-fortune-ai-chiefs-2025]. Medium-term: AI-embedded products launching late 2025-2026 [honeywell-fortune-autonomous-ops-2025]. Long-term: vision of fully 'autonomous' (vs. merely 'automated') industrial operations [honeywell-fortune-autonomous-ops-2025].",
        "decisionRights": "Predominantly top-down. Jordan: prioritization happens at her team level after ambassadors surface use cases [honeywell-fortune-ai-chiefs-2025]. Framework ensures consistent approach across business units [honeywell-fortune-ai-chiefs-2025].",
        "metrics": "Track initiatives 'to the P&L' (Venkatarayalu) [honeywell-fortune-ai-chiefs-2025]. Monthly business results showcases [honeywell-fortune-ai-chiefs-2025]. Value hypothesis tracking [honeywell-fortune-ai-chiefs-2025]. Ranked #17 on Fortune AIQ 50 list for mature AI capabilities [honeywell-fortune-ai-chiefs-2025]."
    },

    # ── MORGAN STANLEY ───────────────────────────────────────────────────
    "morgan-stanley": {
        "reportingStructure": "DEDICATED FIRMWIDE AI HEAD (M4 structural model): Jeff McMillan appointed Head of Firmwide AI (March 2024) [financial-planning-ai-appointment], co-reports to co-presidents Andy Saperstein and Dan Simkowitz — NOT to CTO or CIO [ctomagazine-morgan-stanley-ai-2025]. AI Steering Group co-chaired by McMillan and Katy Huberty (Head of Global Research) — co-chairing with Research Head signals AI seen as knowledge/research function, not primarily technology [morgan-stanley-firmwide-ai-page]. David Wu as Head of Firmwide AI Product & Architecture Strategy (sub-function) [ctomagazine-morgan-stanley-ai-2025]. Key collaborators: Mike Pizzi (Head of U.S. Banks & Technology), Sid Visentini (Head of Firm Strategy) [ctomagazine-morgan-stanley-ai-2025]. McMillan background: headed WM Analytics, Data & Innovation — business/analytics leader, not technologist [financial-planning-ai-appointment]. Distributed domain AI leads in each business division (e.g., Koren Maranca in WM) [ctomagazine-morgan-stanley-ai-2025].",
        "resourceAllocation": "Deep single-vendor partnership with OpenAI (since March 2023) — zero data retention policy for security [ctomagazine-morgan-stanley-ai-2025]. Contrasts with Goldman's multi-model strategy. Three division-specific AI products: (1) AI@MS Assistant for WM advisors (ChatGPT, Sept 2023) [morgan-stanley-openai-announcement], (2) AI@MS Debrief for meeting summarization (2024) [morgan-stanley-debrief-launch], (3) AskResearchGPT for institutional securities/IB (GPT-4, 2024) [morgan-stanley-askresearchgpt]. Document retrieval efficiency: 20% → 80% [ctomagazine-morgan-stanley-ai-2025]. System answering any question from 100,000 documents [ctomagazine-morgan-stanley-ai-2025]. 2,000 job cuts (March 2025) attributed partly to AI-driven efficiency [entrepreneur-ai-layoffs]. ML Research team publishes at NeurIPS 2024, IJCAI 2024, ICLR 2024 [morgan-stanley-firmwide-ai-page]. 70% of new AI model developers hired from academia [evident-bank-ai-talent-2025-ms].",
        "timeHorizons": "Mixed horizons: immediate productivity gains (10-15 hours/week saved per advisor) alongside longer-term agentic AI development [financial-planning-ai-appointment].",
        "decisionRights": "AI Steering Group provides governance [morgan-stanley-firmwide-ai-page]. Eval framework governance committee for model deployment decisions [morgan-stanley-firmwide-ai-page]. Business line leaders retain implementation autonomy [ctomagazine-morgan-stanley-ai-2025].",
        "metrics": "98% adoption rate among 16,000+ WM advisors (but advisors are ~15K of 80K+ employees — firmwide adoption rate unknown) [cdo-magazine-98-adoption]. 10-15 hours/week projected productivity savings per advisor [financial-planning-ai-appointment]. Document retrieval efficiency: 20% → 80% [ctomagazine-morgan-stanley-ai-2025]. System progressed from answering 7,000 questions to answering any question from 100,000 documents [ctomagazine-morgan-stanley-ai-2025]."
    },

    # ── NETFLIX ──────────────────────────────────────────────────────────
    "netflix": {
        "reportingStructure": "AI reports to Elizabeth Stone (CPTO), who reports to co-CEOs Sarandos and Peters [variety-2026-01]. No dedicated CAIO role [variety-2026-01]. AIMS and research teams are part of the technology organization [netflix-research-website].",
        "resourceAllocation": "AI is embedded within technology organization budget, not ring-fenced [netflix-research-website]. Research investments are distributed across business areas rather than centralized [netflix-research-website].",
        "timeHorizons": "Mixed: AIMS works on production models (quarterly) [netflix-aims-job-posting], Eyeline Studios and research teams work on longer-horizon capabilities (e.g., virtual production, de-aging, relighting technology) [techcrunch-2025-10]. VFX innovation is explicitly 3-5 year horizon [deadline-2025-04].",
        "decisionRights": "Distributed — research teams work 'in close collaboration with business teams' and are expected to drive 'high impact' [netflix-research-website]. Experimentation culture means teams can run experiments to validate hypotheses [netflix-research-website].",
        "metrics": "Netflix measures personalization AI by quantified financial ROI [netflix-research-website]. Content AI measured by quality improvement ('10% better') [deadline-2025-04], efficiency gains ('10x faster VFX') [techcrunch-2025-10], and cost reduction (The Pedro Pascal film de-aging cost 'a fraction of The Irishman') [techcrunch-2025-10]. Ads AI measured by revenue growth and campaign planning speed [netflix-q4-2025-earnings]."
    },

    # ── DISNEY ───────────────────────────────────────────────────────────
    "disney": {
        "reportingStructure": "Office of Technology Enablement reports to Alan Bergman (Co-chairman, Disney Entertainment) [variety-ote-2024]. Disney Research Studios appears to operate semi-independently with Chief Scientist Markus Gross [disney-research-about]. OTE has 'accountability to all business segments' and partners with leaders across the company [variety-ote-2024].",
        "resourceAllocation": "OTE is a dedicated unit with growth budget to ~100 employees [variety-ote-2024]. $1B OpenAI investment is ring-fenced strategic capital [fortune-openai-2025]. Research Studios has dedicated facility in Zurich with academic partnerships [disney-research-about]. Not clear if there's a centralized AI budget beyond these structures.",
        "timeHorizons": "Mixed horizons: Disney Research Studios has 16+ year track record and focuses on fundamental research (multi-year horizon) [disney-research-about]. OTE focuses on 'agility, speed, and consistency' (medium-term) [variety-ote-2024]. OpenAI Sora partnership has 3-year term with immediate FY2026 rollout of short-form content on Disney+ (short-term) [fortune-openai-2025].",
        "decisionRights": "OTE explicitly does NOT 'take over or centralize' AI projects in business units [variety-ote-2024]. Instead provides governance and enablement. Business units retain decision rights on their AI initiatives [variety-ote-2024]. This is a coordination/standards model, not a command model.",
        "metrics": "Streaming margin (target 10% in FY2026) [disney-q1-fy2026-earnings], engagement (especially with younger users for Sora content) [fortune-openai-2025], and efficiency gains mentioned. OpenAI partnership framed around consumer engagement, not cost reduction [fortune-openai-2025]."
    },

    # ── SUTTER HEALTH ────────────────────────────────────────────────────
    "sutter-health": {
        "reportingStructure": "CAIO (Ashley Beecy, MD — cardiologist by training, appointed May 2025) [sutter-health-chargeai-2025]. CLINICIAN-CAIO variant: physician background rather than technologist — one of three healthcare CAIO variants identified (clinician-CAIO, technologist-CAIO, dual-hat CMIO/CAIO). CDO (Laura Wilt) handles digital deployment [sutter-health-che-2025]. CIO, CCIO, CDAO also present — multiple C-suite AI-adjacent roles suggest high organizational priority [sutter-health-advisory-2023]. Beecy: 'Working to responsibly operationalize clinical AI at scale, while staying grounded in what matters most, better care and meaningful support for both clinicians and patients' [sutter-health-chargeai-2025].",
        "resourceAllocation": "Dedicated Innovation Center at Pier 1, SF (11,000 sq ft, 7-year lease signed January 2024) [sutter-health-dhn-2024]. Enterprise-wide AI platform deployment through vendor partnerships (Aidoc, Abridge, Hyro, Ferrum Health) [sutter-health-che-2025]. Multiple vendor partnerships rather than building in-house [sutter-health-che-2025].",
        "timeHorizons": "Mixed horizons: Near-term ambient documentation rollout (3,200+ physicians) [sutter-health-che-2025], medium-term Aidoc enterprise deployment across all 21 hospitals (end of 2025/early 2026) [sutter-health-che-2025], longer-term vision of 'dozens of AI use cases in rapid implementation' [sutter-health-che-2025].",
        "decisionRights": "Cross-functional governance structure for AI vetting [sutter-health-che-2025]. Each use case is 'carefully vetted to prioritize patient safety, protect privacy, ensure accuracy, and maintain transparency' [sutter-health-che-2025]. Centralized governance with distributed implementation.",
        "metrics": "1.5 million hours saved in 2025 via automation, AI-powered tools, enhanced technology, and workflow improvements [sutter-health-vizient-2025]. Patient safety, privacy protection, accuracy, transparency for direct care AI [sutter-health-che-2025]. Physician adoption: 3,200+ on ambient docs [sutter-health-che-2025]. Diagnostic improvement: Ferrum platform 430,000 records processed, 1,850 missed pulmonary nodules caught [sutter-aidoc-prnewswire-2025]."
    },

    # ── UNITEDHEALTH GROUP ───────────────────────────────────────────────
    "unitedhealth-group": {
        "reportingStructure": "AI reports through Chief Digital & Technology Officer (Dadlani) and Chief AI Scientist (Pencina) [unitedhealth-group-fortune-2025, unitedhealth-group-stat-2025]. Responsible AI Board (20-25 experts) provides oversight [unitedhealth-group-aiexpert-2025]. Monthly business unit reviews, quarterly CIO monitoring [unitedhealth-group-fortune-2025]. OPTUM TRIPARTITE STRUCTURE: Optum Insight (data analytics/technology — built Optum Real system), Optum Health (care delivery), Optum Rx (pharmacy benefits) [uhg-healthcare-deep-dive-2026]. AI built in one division (Insight), deployed across others. Former naviHealth subsidiary (controversial claims denial algorithm) absorbed into Optum — no longer a named subsidiary [uhg-healthcare-deep-dive-2026]. Former CAIO Dennis Chornenky left for UC Davis Health as Chief AI Adviser (title downgrade: Officer → Adviser) [uhg-healthcare-deep-dive-2026].",
        "resourceAllocation": "Dedicated investment: $1.5B in 2026 for technology/AI [unitedhealth-group-q4-2025-earnings]. Centralized platform (United AI Studio) with distributed usage across 20,000 engineers [unitedhealth-group-fortune-2025]. Separate R&D budget for Optum Labs [unitedhealth-group-ucla-hub-2025].",
        "timeHorizons": "Mixed: 1,000+ production use cases (short-term operational) [unitedhealth-group-ai-page-2025]; Optum Labs academic partnerships for foundational ML research (long-term) [unitedhealth-group-ucla-hub-2025]; Chief AI Scientist role focused on governance standards (medium-term industry shaping) [unitedhealth-group-stat-2025].",
        "decisionRights": "Centralized governance: AI Review Board reviews hundreds of use cases monthly before production approval [unitedhealth-group-ai-page-2025]. Execution is distributed across business units (UHC, Optum, OptumRx) [unitedhealth-group-fortune-2025].",
        "metrics": "Cost reduction ($1B target for 2026) [unitedhealth-group-q4-2025-earnings], adoption (60M lines AI-generated code, 65M chatbot calls, 18M AI-enabled searches) [unitedhealth-group-fortune-2025], efficiency (90% claims auto-adjudicated) [unitedhealth-group-aiexpert-2025], engagement (55M digital users) [unitedhealth-group-aiexpert-2025]."
    },
}


def main():
    updated = []
    for spec_id, new_markers in UPDATES.items():
        path = os.path.join(BASE, "specimens", f"{spec_id}.json")
        if not os.path.exists(path):
            print(f"  SKIP: {spec_id} not found")
            continue

        spec = load_json(path)

        # Verify all cited source IDs exist in the sources array
        source_ids = {s["id"] for s in spec.get("sources", [])}
        cited_ids = set()
        for field, text in new_markers.items():
            if text is None:
                continue
            # Extract [source-id] patterns — match alphanumeric with hyphens and underscores
            refs = re.findall(r'\[([a-zA-Z0-9][a-zA-Z0-9_-]+)\]', text)
            # Filter out things that look like editorial brackets (e.g., [source-1, source-2])
            for ref in refs:
                # Handle comma-separated refs like [source-1, source-2]
                parts = [r.strip() for r in ref.split(",")]
                cited_ids.update(parts)

        missing = cited_ids - source_ids
        if missing:
            print(f"  WARNING {spec_id}: cited sources not in sources array: {missing}")

        # Update observable markers (skip None values to preserve existing)
        for field, text in new_markers.items():
            if text is not None:
                spec["observableMarkers"][field] = text

        # Add citation backfill layer
        spec["layers"].insert(0, {
            "date": "2026-02",
            "label": "Citation Backfill",
            "summary": "Added inline [source-id] citations to all observable markers for fact-level auditability.",
            "classification": None,
            "sourceRefs": []
        })

        # Update meta
        spec["meta"]["lastUpdated"] = TODAY

        save_json(path, spec)
        cited_count = len(cited_ids)
        marker_count = sum(1 for v in new_markers.values() if v is not None)
        updated.append(f"  ✓ {spec_id}: {marker_count} markers cited ({cited_count} unique sources)")
        print(updated[-1])

    print(f"\n  TOTAL: {len(updated)} specimens updated")


if __name__ == "__main__":
    main()
