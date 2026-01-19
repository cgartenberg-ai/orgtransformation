# Session Handoff: AI Organizational Models Research Project

## Overview

This document provides a complete handoff for continuing work on the AI Organizational Models research project. The user is researching corporate organizational responses to AI, with primary focus on **Product/Venture Labs** - internal teams that commercialize AI capabilities into new products and businesses.

**Catalyst:** Mike Krieger podcast about Anthropic Labs - the internal team that built Claude Code, MCP, and Cowork.

**Working Directory:** `mnt/background/`

---

## What Has Been Built

### 1. Skill Directory: `mnt/background/ai-org-models-research/`

A reusable research skill was created with:

| File | Purpose |
|------|---------|
| `SKILL.md` | Main instructions - triggers, workflow, search patterns |
| `references/taxonomy.md` | Full 5-model taxonomy with definitions, decision tree, comparison matrix |
| `references/cases.md` | 230+ enumerated cases across all models |
| `references/sources.md` | Comprehensive source list (podcasts, substacks, SEC patterns, press) |
| `references/docx-generator.md` | Template for generating Word documents |

### 2. Word Documents Generated

| Version | Location | Contents |
|---------|----------|----------|
| v1-v4 | Earlier versions | Progressive builds of taxonomy and cases |
| v5 | `mnt/background/AI_Organizational_Models_Comprehensive_v5.docx` | 48 Product/Venture Labs, 8 insights, 6 CAIOs |
| v6 | `mnt/background/AI_Organizational_Models_Comprehensive_v6.docx` | Added Unnamed/Informal section BUT lost detail |

### 3. JavaScript Generators

| File | Purpose |
|------|---------|
| `create_comprehensive_v5.js` | Generated v5 with full detail |
| `create_comprehensive_v6.js` | Generated v6 - has new section but INCOMPLETE data |

---

## The 5-Model Taxonomy (CRITICAL - PRESERVE THIS)

### Model 1: Research Lab
- **Definition:** Fundamental research, publishing, scientific breakthroughs
- **Time Horizon:** 3-10 years
- **Success Metrics:** Publications, citations, discoveries
- **Examples:** Google DeepMind, Meta FAIR, Microsoft Research, IBM Research

### Model 2: Center of Excellence (CoE)
- **Definition:** Governance, standards, enablement, internal consulting
- **Time Horizon:** 6-24 months
- **Success Metrics:** Adoption rates, compliance, cost savings
- **Examples:** JPMorgan AI CoE, Ford AI Center, Shell AI CoE

### Model 3: Embedded Teams
- **Definition:** AI distributed into product/BU teams, no central AI org
- **Time Horizon:** Quarterly sprints
- **Success Metrics:** Product KPIs, feature launches
- **Examples:** Tesla AI, Stripe, Netflix, Spotify, Uber

### Model 4: Hybrid / Hub-and-Spoke
- **Definition:** Central standards + distributed execution
- **Time Horizon:** Mixed (strategic + tactical)
- **Success Metrics:** Both central and BU KPIs
- **Examples:** Most Fortune 500 companies

### Model 5: Product/Venture Lab (USER'S PRIMARY FOCUS)
- **Definition:** Commercialize AI into products/businesses
- **Time Horizon:** 6-36 months to product, potential spin-off
- **Success Metrics:** Products launched, revenue, valuations
- **Sub-Types:**
  - **5a. Internal Incubator:** Products absorbed into parent (Anthropic Labs → Claude Code)
  - **5b. Venture Builder:** Spin-offs with independent status (Google X → Waymo)
  - **5c. Platform-to-Product:** Internal capability licensed externally (BCG X, QuantumBlack)

---

## Complete Case Data (CRITICAL - v6 LOST MUCH OF THIS)

### Tech Giant Internal Labs (Named Product/Venture Labs)

| Company | Lab Name | Year | Key Leaders | Products | Sub-Type |
|---------|----------|------|-------------|----------|----------|
| Anthropic | Anthropic Labs | 2024 | Mike Krieger, Ben Mann, Ami Vora | Claude Code ($1B/6mo), MCP (100M downloads), Cowork | Internal Incubator |
| Google/Alphabet | Isomorphic Labs | 2021 | Demis Hassabis | AlphaFold drug discovery, $3B pharma partnerships | Venture Builder |
| Google/Alphabet | Google X | 2010 | Astro Teller | Waymo, Verily, Wing, Loon, Chronicle | Venture Builder |
| Google/Alphabet | Area 120 | 2016 | Various | Byteboard (spun), Checks, Aloud | Internal Incubator |
| Google DeepMind | Automated Materials Lab (UK) | 2026 | Demis Hassabis | Gemini robotics for materials science, superconductors | Internal Incubator |
| Microsoft | CoreAI | 2025 | Jay Parikh | Azure AI Foundry, Copilot Studio | Platform-to-Product |
| Microsoft | AI Co-Innovation Labs | 2020s | Various | Custom AI for Fortune 500 | Internal Incubator |
| Microsoft | MAI Superintelligence | 2025 | Mustafa Suleyman, Karen Simonyan | Bing AI, Copilot, next-gen | Internal Incubator |
| Amazon | Lab126 | 2004 | Yesh Dattatreya | Kindle, Echo, Fire TV, Alexa, agentic robotics | Internal Incubator |
| Amazon | AGI SF Lab | 2024 | Peter DeSantis | Nova LLMs, Trainium chips | Internal Incubator |
| Meta | MSL | 2025 | Alexandr Wang, Nat Friedman, Rob Fergus | Llama, Meta AI, Behemoth | Internal Incubator |
| Meta | Meta Compute Initiative | 2026 | Santosh Janardhan, Daniel Gross, Dina Powell McCormick | AI infrastructure scaling | Internal Incubator |
| Apple | Foundation Models | 2024+ | Subramanya | Apple Intelligence | Internal Incubator |
| NVIDIA | NVentures + Inception | 2016+ | Sid Siddeek | Portfolio: OpenAI, xAI, Anthropic | Venture Builder |
| OpenAI | Grove | 2025 | Sam Altman oversight | Pre-company talent incubator | Internal Incubator |
| OpenAI | Startup Fund + Converge | 2021 | Ian Hathaway | Harvey, Cursor, Figure AI | Venture Builder |
| OpenAI | Audio/Device Team | 2026 | Unified team | Audio-first personal device | Internal Incubator |
| Arm Holdings | Physical AI Division | 2026 | Drew Henry (EVP) | Robotics + automotive combined | Internal Incubator |
| Hyundai | Robotics LAB + DEEPX | 2026 | - | Physical AI edge chips, MobED, DAL-e robots | Internal Incubator |
| Eli Lilly | TuneLab | 2025 | Aliza Apple | AI/ML drug discovery platform, 18 models, federated learning | Platform-to-Product |

### AI Lab Spinoffs

| Company | Lab Name | Year | Key Leaders | Products | Valuation |
|---------|----------|------|-------------|----------|-----------|
| Thinking Machines Lab | TML | 2025 | Mira Murati (ex-OpenAI CTO), Barret Zoph, Lilian Weng | Tinker (LLM fine-tuning) | $12B |
| SSI | Safe Superintelligence | 2024 | Ilya Sutskever (ex-OpenAI) | Superintelligence research | $32B |
| AMI Labs | AMI Labs | 2025 | Yann LeCun (leaving Meta), Alex LeBrun | World models, physics | $3.5B target |
| World Labs | World Labs | 2024 | Fei-Fei Li, Justin Johnson | Marble, Chisel (3D) | $1B |
| Latent Labs | Latent Labs | 2024 | Simon Kohl (ex-DeepMind AlphaFold2) | AI protein design | $50M funding |
| Reflection AI | Reflection AI | 2024 | Misha Laskin, Ioannis Antonoglou (ex-DeepMind) | Open-source frontier LLMs, MoE | $8B ($2B raise) |
| Eureka Labs | Eureka Labs | 2024 | Andrej Karpathy (ex-OpenAI, Tesla) | AI + Education | Early stage |
| Periodic Labs | Periodic Labs | 2025 | Liam Fedus (ex-OpenAI VP), Ekin Cubuk (ex-DeepMind) | AI materials science, superconductors | $300M seed |
| Lila Sciences | AI Science Factory | 2025 | Andrew Beam (CTO), Kenneth Stanley (SVP) | Scientific superintelligence, autonomous labs | $1.3B ($550M raised) |
| The Bot Company | The Bot Company | 2025 | Kyle Vogt (ex-Cruise, Twitch) | Home robots, <100 employees | $4B+ |
| Sierra | Sierra | 2024 | Bret Taylor (OpenAI Board Chair), Clay Bavor | Enterprise AI agents | - |
| Converge Bio | Converge Bio | 2026 | - | Generative AI drug discovery | $25M Series A |
| xAI | xAI/Colossus | 2024 | Elon Musk | Grok models, 1M+ GPU cluster | $20B funding |

### Venture Studios & Incubators

| Organization | Name | Year | Key Leaders | Portfolio | AUM/Fund Size |
|--------------|------|------|-------------|-----------|---------------|
| AI Fund | AI Fund | 2018 | Andrew Ng | 35+ cos: Gaia, SkyFire, Profitmind | $370M+ |
| Kleiner Perkins | KP Incubation | 2010s | Joubin Mirzadegan | Glean ($7B), Roadrunner, Windsurf | - |
| Madrona | Venture Labs | 2016 | Steve Singh, Michael Gulmann | Otto, Magnify, Strike Graph, OutboundAI | - |
| Allen Institute | AI2 Incubator | 2017 | Jacob Colker, Oren Etzioni | 50+ cos, 24% acquired | $80M |
| The Hive | The Hive | 2012 | Various | 44 startups, 2 unicorns, 15 exits | - |
| Convergent Research | FROs | 2021 | Adam Marblestone, Sam Rodriques | E11 Bio, Cultivarium, 10 FROs | $30-50M/FRO |

### Pharma AI Labs (Isomorphic Model)

| Company | Lab Name | Year | Key Leaders | Products | Investment |
|---------|----------|------|-------------|----------|------------|
| NVIDIA + Eli Lilly | AI Co-Innovation Lab | 2026 | Joint | World's largest pharma AI factory (1,016 Blackwell GPUs), BioNeMo | $1B/5yr |
| Sanofi | AI Research Factory | 2023+ | Paul Hudson | CodonBERT, 7 drug targets, plai app | - |
| Roche/Genentech | gRED Computational Sciences | 2020s | Aviv Regev, John Marioni | Lab in a Loop, Prescient Design | $12B Recursion |
| Novo Nordisk | Internal AI | 2024+ | Lotte Bjerre Knudsen | Gefion Supercomputer, Valo Health | $4.6B potential |
| Flagship | Expedition Medicines | 2024 | Various | Generative chemistry | $50M + Pfizer |

### Corporate Venture Builders

| Company | Lab Name | Year | Key Leaders | Products | Model |
|---------|----------|------|-------------|----------|-------|
| Adobe | Adobe Incubator | 2025 | Employee teams | Firefly Boards, Brand Concierge, Project Graph | Internal Incubator |
| Samsung | C-Lab Inside/Outside | 2012 | Various | 912 startups (Edint, GhostPass) | Mixed |
| Bosch | Business Innovations | 2025 | Axel Deniz | Carbon capture, healthcare | Venture Builder |
| Porsche Digital | Forward31 | 2020 | Various | Sensigo, Daato, MyEV, Stellar | Venture Builder |
| P&G | P&G Ventures | 2015 | Betsy Bluestone | Zevo, Opte, Kindra, Rae | Venture Builder |
| AXA | Kamet | 2016 | Various | Air Doctor, Akur8, Birdie | Venture Builder |

### Consulting Firms (Platform-to-Product)

| Company | AI Unit | Model Type | Team Size | Products |
|---------|---------|------------|-----------|----------|
| BCG | BCG X | Platform-to-Product | 3,000+ | 36,000+ GPTs, venture building |
| McKinsey | QuantumBlack | Platform-to-Product | 5,000+ | Horizon, Lilli, GAIL, Agents-at-Scale |
| Accenture | AI Labs + 25 GenAI Studios | Platform-to-Product | 30,000+ trained | 100 agentic AI tools |
| Deloitte | AI Institute + GenAI Incubators | Platform-to-Product | Large | 500+ client projects |
| IBM | watsonx AI Labs | Internal Incubator | Various | 6-12 month co-creation |

---

## Unnamed/Informal AI Product Teams (NEW IN V6)

This section was added to address user's concern that research was "over-focusing on named labs." The user specifically asked about companies like **Clorox, BofA, 3M, Walmart** that implement lab-like models WITHOUT branding them as such.

### Consumer Goods

| Company | Internal Structure | Key Indicators | Products |
|---------|-------------------|----------------|----------|
| **Procter & Gamble** | AI Factory + Cross-functional Subgroup | ChatPG: 30,000+ users | Internal AI assistants, packaging optimization |
| **Unilever** | Horizon3 Lab + AI Research Hub | 500+ AI projects | Predictive maintenance, consumer insights |
| **Colgate-Palmolive** | "AI Hub" (Informal) | 4,000 weekly users; CAIO appointed | AI formulation, marketing automation |
| **General Mills** | MillsChat Team | 20,000 employees using MillsChat | Internal ChatGPT, recipe development |
| **Clorox** | "Digital Core" Platform Team | 90-day AI-to-product cycle | Consumer innovation, marketing AI |
| **Nestlé** | AI & Digital Acceleration Team | Cookie Coach reached millions | Ruth chatbot, consumer-facing AI |
| **PepsiCo** | Data & Analytics Transformation | Cross-functional AI squads | Demand sensing, route optimization |
| **Kraft Heinz** | Agile Digital Factory | Sprint-based AI development | Consumer insights, Not Heinz campaign |

### Financial Services

| Company | Internal Structure | Key Indicators | Products |
|---------|-------------------|----------------|----------|
| **Bank of America** | Erica for Employees + AI Enablement | 95% of workforce using AI | Erica internal, code gen, doc processing |
| **Citigroup** | AI Champions Network + Citi Stylus | 2,000+ AI Champions; 140K+ Stylus users | Enterprise AI tools, trading AI |
| **Capital One** | Academic Centers of Excellence (ACEs) | PhD talent embedded | ML production, fraud models |
| **Allstate** | "AI Factory" (Internal Only) | 8-12 person cross-functional teams | Risk models, agent assist, claims AI |
| **State Farm** | InsurTech Innovation Unit | Cross-functional, no branding | Claims processing, underwriting AI |

### Industrial & Manufacturing

| Company | Internal Structure | Key Indicators | Products |
|---------|-------------------|----------------|----------|
| **3M** | GenAI CoE "Action Office" | Ask 3M deployed; cross-divisional | Ask 3M knowledge assistant, Digital Hub |
| **Honeywell** | Connected Enterprise + Forge | AI in all BUs; unified platform | Predictive maintenance, building AI |
| **Caterpillar** | Cat Digital | Separate digital business | Equipment analytics, autonomous mining |
| **John Deere** | Technology Innovation Center | See & Spray, autonomous tractors | Computer vision, precision agriculture |

### Retail

| Company | Internal Structure | Key Indicators | Products |
|---------|-------------------|----------------|----------|
| **Walmart** | Data Ventures | Route Optimization sold as SaaS | GoLocal, supply chain licensed externally |
| **Kroger** | 84.51° "AI Factory" | Data science subsidiary; CPG products | Retail media AI, CPG insights platform |
| **Target** | Digital Transformation + Store AI | 1,800 stores running AI | Inventory AI, pickup optimization |
| **Home Depot** | THD Innovation Hub | Orange Apron GPT | Associate AI tools, inventory opt |

### Healthcare

| Company | Internal Structure | Key Indicators | Products |
|---------|-------------------|----------------|----------|
| **UnitedHealth/Optum** | AI Marketplace (External Sales) | Selling AI to external providers | Clinical decision support, claims AI |
| **HCA Healthcare** | Clinical AI Team | 186 hospitals; AI systemwide | Sepsis prediction, readmission AI |

### Key Patterns Identified

1. **Leader-Lab-Crowd (Implicit):** Companies using "AI Champions" (Leaders), "AI Factory" (Lab), and enterprise-wide tools (Crowd) without Mollick's terminology
2. **Internal → External:** Walmart GoLocal, Kroger 84.51°, Optum Marketplace - internal tools become revenue lines
3. **"Secret Cyborgs":** BofA's 95% usage, P&G's 30K ChatPG users suggest grassroots adoption preceded formal programs

---

## Chief AI Officer Appointments (2025-2026)

| Company | Name | Year | Previous Role |
|---------|------|------|---------------|
| UBS Group AG | Daniele Magazzeni | Dec 2025 | First CAIO for wealth management |
| Commonwealth Bank Australia | Ranil Boteju | 2025 | Lloyd's Chief Data & Analytics Officer |
| Wells Fargo | Saul Van Beurden (expanded) | Nov 2025 | CEO Consumer/Small Business Banking |
| LinkedIn | Deepak Agarwal | 2025 | - |
| Airbnb | Ahmad Al-Dahle (CTO) | Jan 2026 | Meta generative AI lead, Llama team |
| U.S. Cyber Command | Reid Novotny | Nov 2025 | DoD Cyber Force Generation lead |
| Department of Defense | Douglas Matty (CDAO) | Apr 2025 | University of Alabama Research Director |
| Department of Labor | Mangala Kuppa | June 2025 | Deputy CAIO |

**Market Trend:** 40%+ of Fortune 500 expected to have CAIO by end of 2026. Salary range: $354K-$648K.

---

## Key Insights (8 Findings)

1. **Unnamed Lab Structures:** Many companies (P&G, BofA, 3M, Walmart) implement Product Lab patterns WITHOUT formal naming - the "quiet transformation" missed by named-lab research
2. **Leader-Lab-Crowd Pattern:** Companies implementing Mollick's model without terminology - look for "AI Champions" (Leaders), "AI Factory" (Lab), enterprise tools (Crowd)
3. **Internal-to-External Path:** Classic Product Lab pattern: Walmart Route Opt → GoLocal, Kroger 84.51° → CPG Platform, Optum → AI Marketplace
4. **Secret Cyborg Indicators:** BofA 95% AI usage, P&G 30K ChatPG users, General Mills 20K MillsChat users suggest unofficial adoption preceded formal programs
5. **Spinoff Valuations Soaring:** TML ($12B), SSI ($32B), Reflection ($8B), xAI ($20B), Bot Company ($4B+)
6. **Pharma AI Consolidation:** Recursion + Exscientia ($688M), NVIDIA + Lilly ($1B) - drug discovery industrialization
7. **Physical AI Emergence:** Figure ($2.6B), Boston Dynamics, Bot Company, Google Materials Lab, Arm Physical AI Division
8. **CAIO Role Expansion:** 40%+ Fortune 500 by 2026; role now encompasses product strategy, not just governance

---

## Current Issue

**The v6 Word document lost detail.** The v6 generator (`create_comprehensive_v6.js`) has:
- Only 43 Named Product/Venture Labs (should be 75+)
- Only 40 Unnamed/Informal cases (should be 45+)
- Missing many cases from v5

**What the new session needs to do:**
1. Read the complete `references/cases.md` file (which has ALL 230+ cases)
2. Create a new generator script that includes ALL data from cases.md
3. Generate v7 with:
   - Full 5-model taxonomy with decision tree
   - All 75+ Named Product/Venture Labs
   - All 45+ Unnamed/Informal AI Product Teams
   - All Traditional Models by Sector (Technology, Financial, Healthcare, Automotive, Retail)
   - All CAIO appointments
   - All key insights

---

## Source Files (All Complete)

The reference files contain complete data:

| File | Status | Content |
|------|--------|---------|
| `ai-org-models-research/references/cases.md` | COMPLETE | 230+ cases, all sectors |
| `ai-org-models-research/references/taxonomy.md` | COMPLETE | Full 5-model definitions + unnamed lab identification |
| `ai-org-models-research/references/sources.md` | COMPLETE | 40+ podcasts, 15+ substacks, SEC patterns, show notes workflow |
| `ai-org-models-research/SKILL.md` | COMPLETE | Research workflow, search patterns |

---

## User's Key Interests

1. **Product/Venture Labs** - primary focus (spawned the project)
2. **Unnamed/Informal implementations** - companies implementing lab models without branding
3. **Leader-Lab-Crowd pattern** - explicit or implicit implementations
4. **Periodic updates** - skill was built for quarterly refreshes
5. **Comprehensive Word document** - the main deliverable

---

## Next Steps for New Session

1. **Read** `ai-org-models-research/references/cases.md` completely
2. **Read** `ai-org-models-research/references/taxonomy.md` for full model definitions
3. **Create** new generator script that captures ALL data
4. **Generate** v7 Word document with complete information
5. **Verify** all 75+ named labs, 45+ unnamed teams, all sectors included

The skill directory and reference files are complete - only the Word document generator needs to be rebuilt with full data.
