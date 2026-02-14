#!/usr/bin/env python3
"""
Citation backfill batch 2+3: Add inline [source-id] markers to observable markers
for remaining high-completeness specimens.

19 specimens: amazon-agi, anduril, bloomberg, blue-origin, bmw, cvs-health,
general-motors, intel, kroger, lockheed-martin, lowes, mayo-clinic,
mercedes-benz, meta-ai, mount-sinai-health-system, pepsico, toyota,
ulta-beauty, google-x (if exists)
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

UPDATES = {
    # ── AMAZON AGI ────────────────────────────────────────────────────────
    "amazon-agi": {
        "reportingStructure": "CEO Andy Jassy driving corporate restructuring [cbs-ai-layoffs-2026]. SVP Beth Galetti (People Experience & Technology) leading delayering initiative [hrdigest-amazon-30k-2026].",
        "resourceAllocation": "$200B CapEx planned for 2026 (largest single-year corporate infrastructure commitment) [fool-amazon-q4-2025]. 3.99 GW data center capacity added in 2025 (twice 2022 levels), 1.2 GW in Q4 alone [fool-amazon-q4-2025]. Expects to double capacity again by 2027 [fool-amazon-q4-2025]. $730M severance charge in Q4 2025 [fool-amazon-q4-2025]. ~30,000 corporate layoffs (Oct 2025 - Jan 2026) [crn-layoffs-2026, hrdigest-amazon-30k-2026].",
        "timeHorizons": None,
        "decisionRights": "Jassy explicitly framing AI workforce shift as permanent structural change: 'fewer people doing some jobs, more people doing other types of jobs' [fool-amazon-q4-2025].",
        "metrics": "AWS offers 30+ AI/ML services. AWS $244B backlog (+40% YoY) [fool-amazon-q4-2025]. AWS operating margin: 34.6% (Q3 2025) [ig-amazon-preview-2026]. Custom silicon (Trainium/Graviton): $10B+ ARR, triple-digit growth [fool-amazon-q4-2025]. Bedrock: multibillion-dollar ARR, +60% QoQ [fool-amazon-q4-2025]. AWS: $142B ARR [fool-amazon-q4-2025]. ~350,000 corporate workforce (pre-cuts) [hrdigest-amazon-30k-2026]. ~30K corporate layoffs (~9% of corporate workforce) [crn-layoffs-2026]. 2026 Amazon Nova AI Challenge focuses on 'Trusted Software Agents' [amazon-q4-announcement]."
    },

    # ── ANDURIL ───────────────────────────────────────────────────────────
    "anduril": {
        "reportingStructure": "No separate AI reporting structure — AI capability is embedded in product divisions [anduril-sacra-2026-02]. CEO Brian Schimpf oversees all operations. Luckey serves as primary vision-setter and external spokesperson but is not operational CEO [anduril-60minutes-2025-02].",
        "resourceAllocation": "100% of R&D is AI-related because all products are AI-powered autonomous systems [anduril-sacra-2026-02]. Arsenal-1 ($1B manufacturing facility in Ohio) is being built for AI-enabled manufacturing [anduril-fortune-2026-02]. Lattice is the common AI platform across all products [anduril-60minutes-2025-02].",
        "timeHorizons": "Mixed: Some products ship in months (Ghost drones, Sentry towers), but major programs like YFQ-44A Fury CCA and Arsenal-1 are multi-year [anduril-sacra-2026-02]. Luckey emphasizes 'months not years' compared to traditional defense primes [anduril-fortune-2026-02].",
        "decisionRights": "Highly centralized around founding team. Small founder group (Luckey, Schimpf, Grimm, Stephens, Chen) makes strategic decisions [anduril-wikipedia-2026-02]. Product teams have autonomy in execution.",
        "metrics": "Contracts won, production speed, cost vs. traditional defense primes. Luckey frequently benchmarks against consumer AI (Tesla autopilot, Roomba autonomy) to argue defense systems lag [anduril-60minutes-2025-02]."
    },

    # ── BLOOMBERG ──────────────────────────────────────────────────────────
    "bloomberg": {
        "reportingStructure": "AI Strategy & Research reports to CTO (Shawn Edwards) [bloomberg-ai150-press-2024]. AI Engineering teams distributed across product groups [bloomberg-computing-uk-2025]. Human-in-the-loop approach with domain experts (Bloomberg Intelligence analysts) training and reviewing AI outputs [bloomberg-techmonitor-2024].",
        "resourceAllocation": "Dedicated AI headcount (350+) [bloomberg-computing-uk-2025], dedicated GPU infrastructure, dedicated partnerships (AWS, Tetrate) [bloomberg-techmonitor-2024]. Ring-fenced AI team with cross-functional collaboration model.",
        "timeHorizons": "Mixed. Long-term: 15-year track record of incremental AI building since 2009 [bloomberg-ai150-press-2024]. Medium-term: product releases like earnings call summaries (2024) [bloomberg-earnings-launch-2024], news summaries (2025). Near-term: quarterly product enhancements and new feature launches.",
        "decisionRights": "Centralized strategy (CTO office sets direction) [bloomberg-ai150-press-2024], distributed execution (AI engineers work with domain teams) [bloomberg-computing-uk-2025]. Pragmatic filter: 'figure out what our clients' needs are, and then how we can address those needs, using AI if necessary' [bloomberg-computing-uk-2025].",
        "metrics": "Client needs and value-add are primary metrics. Responsible AI pillars: protection, transparency, reproducibility, robustness [bloomberg-computing-uk-2025]. Accuracy and source traceability (all AI outputs link back to original sources) [bloomberg-techmonitor-2024]. Risk governance: regular security assessments, pen testing, red teaming [bloomberg-computing-uk-2025]."
    },

    # ── BLUE ORIGIN ───────────────────────────────────────────────────────
    "blue-origin": {
        "reportingStructure": "AI reports through Enterprise Technology (VP William Brennan), not a dedicated CAIO or AI lab structure [blue-origin-aws-case-study-2025]. CEO Dave Limp has strong AI background (led Alexa at Amazon) [blue-origin-vanderbilt-2025]. No CAIO or dedicated AI leadership role identified [blue-origin-theorg-2026].",
        "resourceAllocation": "AI embedded in existing functions via BlueGPT platform [blue-origin-aws-case-study-2025]. AWS provides cloud infrastructure [blue-origin-aws-reinvent-2025]. No separate AI budget mentioned — appears integrated into operations.",
        "timeHorizons": "Mixed — short-term agent deployments (manufacturing issue resolution 70% faster) [blue-origin-aws-case-study-2025] plus long-term vision (AI-designed lunar hardware [blue-origin-aws-reinvent-2025], space data centers 'in 5-10 years' [blue-origin-yahoo-finance-2025]).",
        "decisionRights": "Highly distributed — 'everyone at Blue Origin is expected to build and collaborate with AI agents' [blue-origin-aws-reinvent-2025]. Agent marketplace enables discovery and sharing across teams [blue-origin-aws-case-study-2025].",
        "metrics": "70% company-wide adoption rate, 95% of software engineers using AI tools, 70% faster manufacturing issue resolution, 75%+ acceleration in product development cycles (T-Rex project), 3.5M monthly interactions [blue-origin-aws-case-study-2025]."
    },

    # ── BMW ────────────────────────────────────────────────────────────────
    "bmw": {
        "reportingStructure": "No Chief AI Officer. AI leadership reports through enterprise platforms/IT function (Marco Görgmaier) with Project AI excellence cluster (Michael Würtenberger) providing central coordination [bmw-aws-podcast-2024]. Board-level sponsorship from CEO Zipse [bmw-agm-2025].",
        "resourceAllocation": "Centralized platform (Group-wide AI platform, GenAI self-service platform) with distributed execution [bmw-aws-podcast-2024]. Platform provides governance, services, and tools; business units build applications on top [bmw-ai-webpage-2025].",
        "timeHorizons": "Mixed. Production AI applications operate on quarterly/annual cycles [bmw-ai-webpage-2025]. Autonomous driving and Neue Klasse platform investments have 3-5 year horizons [bmw-agm-2025]. AI research (RoboTac Lab) has longer research timelines [bmw-ad-campus-2018].",
        "decisionRights": "Federated model. Central platform sets standards, governance, and regulatory compliance (EU AI Act) [bmw-aws-podcast-2024]. Business units have autonomy to build applications within guardrails. 'Democratized access' via self-service platform [bmw-aws-podcast-2024].",
        "metrics": "Efficiency gains, productivity improvements, ROI on AI investments. Zipse emphasizes being 'faster and more precise' [bmw-agm-2025]. Quality metrics in manufacturing (gap assessment, scratch detection) [bmw-ai-webpage-2025]."
    },

    # ── CVS HEALTH ────────────────────────────────────────────────────────
    "cvs-health": {
        "reportingStructure": "Chief Data Analytics & AI Officer (Keshavarz) and Chief Experience & Technology Officer (Mandadi) both report to CEO [cvs-health-imd-2025]. AI leadership split between data/analytics and technology/platform functions rather than unified under a single AI czar. Mandadi explicitly rejected creating a CAIO role, preferring embedding AI across functions [cvs-health-fortune-2025-07].",
        "resourceAllocation": "$20B tech modernization over 10 years with AI central [cvs-health-larridin-2025]. $1B+ in operational savings reinvested [cvs-health-constellation-2025-12]. AI-native consumer engagement platform connects CVS Pharmacy, CVS Caremark, Aetna, and Oak Street Health into single digital interface [digitalcommerce360-cvs-ai-strategy-2026]. Business-unit-specific AI: Aetna (90 min/day saved per nurse, 30% call center reduction, 4 care management systems → 1), Caremark (300+ claims/sec at peak), Oak Street Health (ambient AI scribe at 90% of facilities) [cvs-health-constellation-2025-12]. 'Engagement as a service' positions AI as horizontal capability across all four businesses [cvs-health-fortune-2025-07].",
        "timeHorizons": "Mixed — 2026 positioned as pivotal year for 'tinkering becomes transformation' [cvs-health-larridin-2025]. Building AI-native consumer platform launched December 2025 [cvs-health-investor-day-2025-12]. $20B is 10-year horizon [cvs-health-larridin-2025]. CEO projects healthcare 'unrecognizable in 5 years' [cvs-health-constellation-2025-12].",
        "decisionRights": "Centralized standards through CDAIO but distributed execution [cvs-health-imd-2025]. 'Qualified humans always make health outcome decisions' — AI decision rights constrained in clinical domains [cvs-health-fortune-2025-07]. AI supports but does not replace human judgment.",
        "metrics": "$1B+ operational cost savings; 90 minutes/day saved per nurse; 30% reduction in Aetna call center volume; 99% first-call resolution at Caremark; 300+ claims/second processing; 1.6% improvement in medication adherence [cvs-health-constellation-2025-12, cvs-health-emerj-2024]."
    },

    # ── GENERAL MOTORS ────────────────────────────────────────────────────
    "general-motors": {
        "reportingStructure": "Post-November 2025: AI team reports to manufacturing engineering organization [cio-dive-caio-departure-2025]. Previously reported to CAIO. Sterling Anderson leads combined vehicle software and product organization [gm-forward-event-2025]. Classic structural separation between AI enablement (manufacturing) and AI product (autonomous/software).",
        "resourceAllocation": "Small elite central team (<20) + large distributed teams (100+ at ARC) [cbt-news-ai-team-2025]. Manufacturing has dedicated AI budget. Software/autonomous has separate substantial investment. Ring-fenced AI Center of Excellence now integrated into manufacturing [cio-dive-caio-departure-2025].",
        "timeHorizons": "Mixed: Near-term manufacturing AI (continuous improvement) [gm-newsroom-ai-manufacturing-2025], medium-term conversational AI (2026 Google Gemini launch) [gm-forward-event-2025], long-term autonomous (eyes-off driving 2028) [gm-forward-event-2025]. Pragmatic, staged approach.",
        "decisionRights": "Shifting toward distributed. AI Center of Excellence originally had cross-functional advisory role. After CAIO departure, AI capabilities being 'strategically integrated directly into business and product organizations' per GM spokesperson [cio-dive-caio-departure-2025].",
        "metrics": "Super Cruise subscribers (620K+), OnStar subscribers (12M), manufacturing efficiency gains, software update capacity (10x target), over-the-air bandwidth (1000x target) [gm-forward-event-2025, gm-q4-2025-shareholder-letter]."
    },

    # ── INTEL ─────────────────────────────────────────────────────────────
    "intel": {
        "reportingStructure": "CEO Lip-Bu Tan directly leads AI and Advanced Technologies Group after CTO departure [intel-leadership-restructuring]. Three longtime technical executives (Rob Bruckner, Mike Hurley, Lisa Pearce) now report directly to CEO [intel-leadership-restructuring]. Product groups (DCAI, CCG) report directly to CEO [intel-q3-2025-earnings]. Flattened structure to reduce organizational complexity [intel-vision-2025-register].",
        "resourceAllocation": "Dedicated Intel Labs with 700+ researchers [intel-labs-ai-research]. Custom ASIC business as distinct unit with $1B+ revenue [intel-q4-2025-earnings]. Central Engineering Group created to unify horizontal functions [intel-q3-2025-earnings]. Ring-fenced foundry business. Clear separation between research (Labs) and product execution (business units).",
        "timeHorizons": "Mixed: Intel Labs does multi-year fundamental research (cognitive AI, quantum, physical AI) [intel-labs-ai-research]. Product groups work on quarterly/annual cycles (AI PCs, Xeon, Gaudi) [intel-q4-2025-earnings]. CEO mentions 'won't happen overnight' for competitive AI platform — implies multi-year horizon for turnaround [intel-vision-2025-register].",
        "decisionRights": "Significantly centralized under CEO Tan after flattening [intel-leadership-restructuring]. CEO directly oversees AI strategy. Central Engineering Group coordinates horizontal decisions [intel-q3-2025-earnings]. Quote from memo: 'This supports our emphasis on becoming an engineering-focused company and will give me visibility into what's needed to compete and win' [intel-leadership-restructuring].",
        "metrics": "Revenue by segment (DCAI grew 15% sequentially in Q4) [intel-q4-2025-earnings]. AI PC unit growth (16% in Q4) [intel-q4-2025-earnings]. Custom ASIC business growth (50%+ in 2025, 26% sequential in Q4) [intel-q4-2025-earnings]. Process node progress (18A milestone) [intel-q4-2025-earnings]. Profitability targets (64.7% loss reduction in 2025, profitability target 2026) [intel-q4-2025-earnings]."
    },

    # ── KROGER ────────────────────────────────────────────────────────────
    "kroger": {
        "reportingStructure": "AI reports through 84.51° (data science subsidiary) [kroger-cdo-magazine-2025]. SVP of Data Science and AI (Kristin Foster) leads [kroger-cdo-magazine-2025]. AI Governance Council includes technology, legal, privacy, security, HR, and business partners [kroger-cdo-magazine-2025]. Kroger Privacy Office plays critical role [kroger-cdo-magazine-2025].",
        "resourceAllocation": "Dedicated infrastructure through AI Factory platform [kroger-cdo-magazine-2025]. Ring-fenced investment in NVIDIA partnership and AI lab [kroger-nvidia-2022]. Shared services model for business units [kroger-p2pi-2025].",
        "timeHorizons": "Mixed — quarterly operational wins (shrink, pricing, fulfillment) [kroger-q2-2025-earnings] + 3-5 year strategic vision (connected intelligence, personal AI agents) [kroger-p2pi-2025]. Agentic AI initiatives like 'Agent Barney' suggest medium-term innovation [kroger-p2pi-2025].",
        "decisionRights": "Hybrid — central hub sets governance, standards, tooling; spokes have autonomy to develop AI closest to their problems within guardrails [kroger-cdo-magazine-2025]. 'Balance bottom-up innovation with top-down guardrails' [kroger-cdo-magazine-2025].",
        "metrics": "Shrink improvements, competitive pricing, faster fulfillment, e-commerce profitability [kroger-q2-2025-earnings], onboarding time (reduced from weeks to <1 day) [kroger-cdo-magazine-2025], development timelines, duplicative work reduction [kroger-p2pi-2025]."
    },

    # ── LOCKHEED MARTIN ───────────────────────────────────────────────────
    "lockheed-martin": {
        "reportingStructure": "CDAIO Mike Baylor reports to corporate leadership (likely CEO given strategic importance) [lockheed-martin-dataiq-baylor-2024]. CTO Craig Martell reports to SVP John Clark [lockheed-martin-cto-appointment-2025]. CIO Maria Demaree appears peer to CDAIO. This is a dual-track structure: CDAIO owns AI strategy/capability, CTO owns technology innovation, CIO owns operational integration [lockheed-martin-dataiq-baylor-2024].",
        "resourceAllocation": "Dedicated budget with $5B planned for 2026 CapEx/IR&D (up from $3.6B in 2025) [lockheed-martin-q4-2025-earnings]. Ring-fenced AI Factory infrastructure (NVIDIA DGX SuperPOD) [lockheed-martin-nvidia-case-study-2024]. 300+ professionals in centralized data/analytics function [lockheed-martin-dataiq-baylor-2024]. AI Factory supports 7,000 engineers enterprise-wide [lockheed-martin-nvidia-case-study-2024].",
        "timeHorizons": "Mixed horizons consistent with hub-and-spoke. LAIC supports near-term product integration (quarterly), mid-term capability development (1-2 years), and longer-term research through Advanced Technology Laboratories [lockheed-martin-capabilities-page-2024]. Taiclet's '21st Century Security' vision is multi-decade [lockheed-martin-csis-interview-2023].",
        "decisionRights": "Centralized AI governance: Data council and governance board with cross-organizational participation [lockheed-martin-dataiq-baylor-2024]. Data steward network enforces consistency. Ethical AI Advisory Committee aligned with DoD principles [lockheed-martin-capabilities-page-2024]. Standards flow from hub to spokes.",
        "metrics": "Taiclet focuses on backlog ($194B record), production increases (191 F-35s in 2025), capability delivery speed (six-month update cycles vs. multi-year) [lockheed-martin-q4-2025-earnings]. AI Factory metrics: tokens processed, projects supported, time-to-deployment, users served [lockheed-martin-nvidia-case-study-2024]."
    },

    # ── LOWE'S ────────────────────────────────────────────────────────────
    "lowes": {
        "reportingStructure": "Chandhu Nair (SVP AI, Data, Innovation) sits in tech organization [lowes-ai-innovator-2026]; Seemantini Godbole (CDIO) reports to CEO [lowes-fortune-2024]. AI Transformation Office provides cross-functional governance [lowes-fortune-2024]. Innovation Labs operates as semi-independent subsidiary in Kirkland, WA [lowes-innovation-labs-2026].",
        "resourceAllocation": "Charlotte Tech Hub is dedicated facility with up to 2,000 tech roles [lowes-fortune-2024]; Innovation Labs is separate Kirkland facility [lowes-innovation-labs-2026]; explicit investment in OpenAI partnership infrastructure [lowes-dc360-2025]. Multiple pilots running simultaneously (14 stores for ChatGPT-style tool, 50 stores for dwell alerts) [lowes-fortune-2024].",
        "timeHorizons": "Mixed: Innovation Labs works on 2-5 year horizon (Vision Pro, digital twins, spatial commerce) [lowes-innovation-labs-2026]; AI Transformation Office works quarterly to annual cadence [lowes-fortune-2024]; store rollouts measured in months (Style Your Space launched Sept, expanding through 2025-2026) [lowes-fortune-2024].",
        "decisionRights": "Centralized governance through AI Transformation Office with four-metric framework (ROI, tech investment, business readiness, brand/reputation risk) [lowes-fortune-2024]. Distributed execution to Innovation Labs for exploration, engineering for internal tools, and store ops for associate-facing tools [lowes-ai-innovator-2026].",
        "metrics": "Leading indicators: adoption rates, daily usage, weekly active users, feedback metrics [lowes-fortune-2024]. Lagging indicators: revenue growth, conversion uplift. Specific KPIs mentioned: 80% accuracy target for associate tool (aiming for 85-90%) [lowes-fortune-2024]; 2x conversion when customers engage Mylow [lowes-dc360-2025]; 200 basis point improvement in CSAT with in-store Mylow Companion [lowes-dc360-2025]; double-digit productivity gains from GenAI in code review [lowes-fortune-2024]."
    },

    # ── MAYO CLINIC ───────────────────────────────────────────────────────
    "mayo-clinic": {
        "reportingStructure": "CAIO (Tripathi) and CDAO (Sehgal) are distinct C-suite roles [mayo-clinic-oncodaily-2025, mayo-clinic-govtech-2025]. Mayo Clinic Platform (Halamka) is a separate commercialization unit [mayo-clinic-msft-podcast-2025]. DEPARTMENT of AI and Informatics (not a center or initiative) — has permanent budget authority and academic standing within the research division, giving AI research organizational permanence [mayo-clinic-msft-podcast-2025]. Mayo Clinic Platform has three sub-units: Platform_Accelerate (startup incubator), Platform_Insights (quality improvement for other health systems), Platform_Orchestrate (clinical trials acceleration) [mayo-clinic-wef-2025]. Clinical AI execution is clinician-led with department heads driving domain-specific AI [mayo-clinic-msft-podcast-2025]. Multi-agent research system using tournament framework (Generation, Reflection, Ranking, Evolution, Proximity agents) for hypothesis generation [mayo-clinic-msft-podcast-2025].",
        "resourceAllocation": "Dedicated, ring-fenced: AI Factory is a formal capability, Mayo Clinic Platform is a separate unit with its own accelerator and partnerships [mayo-clinic-msft-podcast-2025]. $9B infrastructure investment explicitly tied to AI/digital transformation [mayo-clinic-msft-podcast-2025]. Nvidia supercomputer cluster is dedicated AI infrastructure [mayo-clinic-govtech-2025].",
        "timeHorizons": "Mixed horizons consistent with hub-and-spoke: (1) Near-term: ~100 algorithms in production, clinical deployment focus [mayo-clinic-govtech-2025], (2) Medium-term: 200+ use cases in AI Factory pipeline, accelerator cohorts [mayo-clinic-msft-podcast-2025], (3) Long-term: 10-year Google partnership, 'Bold Forward' strategic plan, platform architecture for global scale [mayo-clinic-msft-podcast-2025].",
        "decisionRights": "Hybrid: Central governance for standards, security, privacy vetting (all algorithms must pass review) [mayo-clinic-govtech-2025]. Distributed execution via clinical departments. Sehgal's team provides consulting before development [mayo-clinic-msft-podcast-2025]. Halamka's Platform enables external innovation with guardrails [mayo-clinic-wef-2025].",
        "metrics": "Clinical outcomes emphasized over administrative efficiency. 320 AI algorithms cited by CEO [mayo-clinic-msft-podcast-2025]. 'Fit for use' validation via Platform_Validate [mayo-clinic-wef-2025]. Publications in Mayo Clinic Proceedings. Patient safety as primary constraint [mayo-clinic-govtech-2025]."
    },

    # ── MERCEDES-BENZ ─────────────────────────────────────────────────────
    "mercedes-benz": {
        "reportingStructure": "Chief Data & AI Officer reports within tech/IT organization [mercedes-benz-cdaio-appointment-2025]. Chief Software Officer (Magnus Östberg) oversees vehicle software and AI integration [mercedes-benz-newsweek-2025]. AI expertise added to supervisory board (Rashmi Misra, former Microsoft) [mercedes-benz-supervisory-board-2025].",
        "resourceAllocation": "Significant ring-fenced investment in MBRDNA as dedicated global AI center (600+ headcount) [mercedes-benz-mbrdna-2025]. Separate Digital Factory Campus for manufacturing AI [mercedes-benz-fast-company-2025]. Dedicated partnerships with Google, Microsoft, Nvidia, Momenta, ByteDance, Tencent [mercedes-benz-sae-interview-2025, mercedes-benz-fast-company-2025]. Academic funding for Stanford and UCSD [mercedes-benz-academic-partnerships-2024].",
        "timeHorizons": "Mixed horizons: Near-term (2026-2027) for CLA and S-Class with MB.OS [mercedes-benz-cla-unveil-2025]. Medium-term for L4 autonomous/robotaxi capabilities with Uber/Nvidia partnership [mercedes-benz-fast-company-2025]. Long-term fundamental research via academic partnerships [mercedes-benz-academic-partnerships-2024]. Clear product launch cadence driving AI integration timeline.",
        "decisionRights": "Centralized architectural decisions via MB.OS platform (replaces fragmented third-party ECU approach) [mercedes-benz-sae-interview-2025]. Distributed execution at global tech hubs [mercedes-benz-fast-company-2025]. Central standards with local adaptation (especially China partners like Momenta, ByteDance, Tencent) [mercedes-benz-fast-company-2025].",
        "metrics": "Explicit focus on processing power (508 TOPs for MB Drive Assist Pro, '5x Tesla FSD') [mercedes-benz-newsweek-2025]. Over-the-air update capability as key milestone [mercedes-benz-sae-interview-2025]. Privacy compliance as differentiator [mercedes-benz-sae-interview-2025]. Q2 2025 earnings focus on EBIT, ROS, and free cash flow rather than AI-specific metrics [mercedes-benz-investor-relations-2025]."
    },

    # ── META AI ────────────────────────────────────────────────────────────
    "meta-ai": {
        "reportingStructure": "CEO Andy Jassy driving corporate restructuring [source-1]. SVP Beth Galetti (People Experience & Technology) leading delayering initiative [source-2].",
        # Meta AI has very specific sources - skip and leave current markers
        # The source IDs are source-1 through source-5 plus many specific ones
        # Let me set all to None since the generic source-1 etc are not meaningful
        "reportingStructure": None,
        "resourceAllocation": None,
        "timeHorizons": None,
        "decisionRights": None,
        "metrics": None
    },

    # ── MOUNT SINAI HEALTH SYSTEM ─────────────────────────────────────────
    "mount-sinai-health-system": {
        "reportingStructure": "NO SINGLE CAIO — distributed leadership across specialized roles: Lisa Stump (EVP, Chief Digital Information Officer and Dean of IT at Icahn School of Medicine), Robbie Freeman (VP for Digital Experience and Chief Nursing Informatics Officer), Nicholas Gavin (VP, Chief Clinical Innovation Officer, Associate CMIO for Digital Health) [mount-sinai-dragon-copilot-2025]. AI leadership distributed across CDIO, CNIO, CCIO roles rather than unified under single CAIO. Windreich Department of AI and Human Health led by Girish Nadkarni (Chief AI Officer for academic function) [mount-sinai-ortho-spine-2025]. Domain-specific AI sub-centers: Center for AI in Children's Health (indicating segmentation by patient population) [mount-sinai-newsroom-2024]. Microsoft Dragon Copilot rolled out system-wide — major ambient clinical AI vendor partnership [mount-sinai-dragon-copilot-2025].",
        "resourceAllocation": "Dedicated 12-story facility [mount-sinai-newsroom-2024]; philanthropic funding for research center; ring-fenced AI department with full academic resources [mount-sinai-newsroom-2024]. Experience-led model considers build/buy/partner for each use case [mount-sinai-health-system-cio-2025].",
        "timeHorizons": "Mixed: research function has 3-10 year horizon (fundamental AI research, genomics, drug discovery) [mount-sinai-ortho-spine-2025]; clinical deployment has 6-24 month horizon (17 AI products deployed) [mount-sinai-health-system-cio-2025]; immediate-term workflow improvements (NutriScan, pressure injury prediction) [mount-sinai-health-system-cio-2025].",
        "decisionRights": "Centralized governance with distributed idea generation. Anyone can submit AI ideas through centralized intake [mount-sinai-ortho-spine-2025]. Risk scoring and guardrails calibrate assurance requirements to use case (lighter for back-office, heavier for clinical decision support) [mount-sinai-ortho-spine-2025]. Always human-in-the-loop for clinical tools [mount-sinai-healthcare-brew-2024].",
        "metrics": "Four-dimension evaluation: decision-making speed, reversibility, criticality, proximity to patient care [mount-sinai-ortho-spine-2025]. Also track quality ratings, reimbursement improvements (e.g., malnutrition identification 2.5-3x improvement), and documentation burden reduction (20 min per 12-hour shift) [mount-sinai-health-system-cio-2025]."
    },

    # ── PEPSICO ───────────────────────────────────────────────────────────
    "pepsico": {
        "reportingStructure": "AI reports to Chief Strategy & Transformation Officer (Kanioura), who reports directly to CEO [pepsico-cdo-interview-2023]. No dedicated CAIO — AI is bundled with strategy, M&A, data, and transformation [pepsico-cdo-interview-2023]. AI Council/Steering Committee for governance [pepsico-cdo-prioritization-2024].",
        "resourceAllocation": "Dedicated Digital Hubs with ring-fenced headcount [pepsico-digital-hubs-2021]. Central platform (PepGenX) for experimentation [pepsico-cgt-aws-2025]. Mission-based teams get cross-functional resources [pepsico-cdo-prioritization-2024]. Monthly transformation benefit tracking [pepsico-cdo-prioritization-2024].",
        "timeHorizons": "Mixed: SAP rollout is multi-year foundation [pepsico-diginomica-ceo-2024]; agentic AI deployment is near-term (2025-2026) [pepsico-cgt-aws-2025]; digital twins are medium-term (facility simulations) [pepsico-siemens-nvidia-2026]. 100 basis points operating margin expansion over 3 years [pepsico-q2-earnings-2025].",
        "decisionRights": "Hybrid — central team sets standards and prioritizes 'four or five big bets,' but mission-based teams have execution autonomy [pepsico-cdo-prioritization-2024]. AI Council vets AI-specific proposals [pepsico-cdo-prioritization-2024].",
        "metrics": "Productivity savings (record target for 2026) [pepsico-q2-earnings-2025], cloud migration %, operating margin expansion, free cash flow conversion [pepsico-q2-earnings-2025]. Joint KPIs with AWS on innovation portfolio, supply chain performance, operational productivity [pepsico-cgt-aws-2025]. Monthly benefit tracking, quarterly exec committee reporting [pepsico-cdo-prioritization-2024]."
    },

    # ── TOYOTA ────────────────────────────────────────────────────────────
    "toyota": {
        "reportingStructure": "TRI reports to Toyota corporate as R&D subsidiary [toyota-tri-announcement-2016]. Enterprise AI sits within TMNA's OneTech IT division [toyota-cdo-magazine-2025]. GAIA bridges TRI research to production across Toyota Group [toyota-global-newsroom-2025]. Incoming CEO Kenta Kon has direct experience with Woven by Toyota (automated driving startup), suggesting AI will have CEO attention [toyota-ceo-transition-2026].",
        "resourceAllocation": "Dedicated budgets for TRI ($1B initial) [toyota-tri-announcement-2016], university partnerships ($50M), and GAIA [toyota-global-newsroom-2025]. Enterprise AI has dedicated organization within OneTech IT [toyota-cdo-magazine-2025]. Multiple AI-focused entities (TRI, Woven, Toyota Connected) operate with independent budgets.",
        "timeHorizons": "Multi-horizon approach: TRI pursues long-term research (3-10 year breakthroughs in autonomy and robotics) [toyota-tri-homepage-2026]. Enterprise AI focuses on near-term productivity (20%+ developer productivity gains) [toyota-cdo-magazine-2025]. GAIA bridges research to production (1-3 year technology transfer) [toyota-global-newsroom-2025]. Manufacturing AI already deployed (troubleshooting reduced from 7 hours to 15 seconds) [toyota-cdo-magazine-2025].",
        "decisionRights": "Federated model — TRI has research autonomy, Enterprise AI has TMNA-wide mandate, GAIA coordinates cross-entity technology transfer [toyota-global-newsroom-2025]. Five Toyota Group companies collaborate through Toyota Software Academy [toyota-global-newsroom-2025]. Kursar emphasizes 'guardrails' and measurement for AI quality [toyota-cdo-magazine-2025].",
        "metrics": "ROI and TCO (Kursar emphasizes avoiding 'tech for the sake of tech') [toyota-cdo-magazine-2025]. Developer productivity (20%+ improvement with AI coding tools) [toyota-cdo-magazine-2025]. Time savings (manufacturing diagnosis: 7 hours → 15 seconds) [toyota-cdo-magazine-2025]. Code coverage improvements. Customer-facing safety metrics (Toyota Safety Sense adoption) [toyota-q3-earnings-2026]."
    },

    # ── ULTA BEAUTY ───────────────────────────────────────────────────────
    "ulta-beauty": {
        "reportingStructure": "AI reports through CTTO (Mike Maresca) and CDO (Prama Bhatt) [ulta-beauty-fortune-2025, ulta-beauty-nrf-2025]. No dedicated CAIO. Both report to CEO Kecia Steelman [ulta-beauty-nrf-2026].",
        "resourceAllocation": "Dedicated AI Center of Excellence with cross-functional AI/ML engineers [ulta-beauty-fortune-2025]. Prisma Ventures for external AI investments [ulta-beauty-dc360-2025]. Significant CapEx in technology modernization through Project SOAR [ulta-beauty-fortune-2025].",
        "timeHorizons": "Mixed: Near-term AI deployment (supply chain, payroll tools) [ulta-beauty-nrf-2026] + longer-term agentic AI development [ulta-beauty-dc360-2025]. CEO: 'There is no finish line in our technology and our investments' [ulta-beauty-pymnts-2025].",
        "decisionRights": "Centralized AI capability development (Center of Excellence) with distributed application (each function applies AI tools) [ulta-beauty-fortune-2025]. Evaluating whether to deploy single unified AI assistant vs. specialized agents [ulta-beauty-dc360-2025].",
        "metrics": "Measuring: IT productivity (25-30% improvement from AI coding tools) [ulta-beauty-fortune-2025], e-commerce growth (double-digit for 3 quarters) [ulta-beauty-pymnts-2025], loyalty members (46.3M) [ulta-beauty-pymnts-2025], app penetration (65% of online member sales) [ulta-beauty-pymnts-2025], ship-from-store expansion (1,000+ locations) [ulta-beauty-dc360-2025]."
    },
}


def main():
    updated = []

    for spec_id, new_markers in UPDATES.items():
        path = os.path.join(BASE, "specimens", f"{spec_id}.json")
        if not os.path.exists(path):
            print(f"  SKIP {spec_id}: file not found")
            continue

        # Check if ALL markers are None (skip entirely)
        if all(v is None for v in new_markers.values()):
            print(f"  SKIP {spec_id}: all markers set to None (no citations to add)")
            continue

        spec = load_json(path)

        # Validate cited source IDs exist
        source_ids = {s["id"] for s in spec.get("sources", [])}
        cited_ids = set()
        for field, text in new_markers.items():
            if text is None:
                continue
            refs = re.findall(r'\[([a-zA-Z0-9][a-zA-Z0-9_-]+)\]', text)
            for ref in refs:
                parts = [r.strip() for r in ref.split(",")]
                cited_ids.update(parts)

        missing = cited_ids - source_ids
        if missing:
            print(f"  WARNING {spec_id}: cited sources not in sources array: {missing}")

        # Update observable markers (skip None values to preserve existing)
        for field, text in new_markers.items():
            if text is not None:
                spec["observableMarkers"][field] = text

        # Add citation backfill layer (only if not already present)
        has_backfill = any(
            l.get("label") == "Citation Backfill" for l in spec.get("layers", [])
        )
        if not has_backfill:
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
