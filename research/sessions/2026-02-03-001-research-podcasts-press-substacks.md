---
session_date: "2026-02-03"
sources_planned: ["no-priors", "latent-space", "bg2-pod", "stratechery", "all-in-podcast", "press-keyword-search", "linkedin-economic-graph"]
sources_scanned: ["no-priors", "stratechery", "all-in-podcast", "press-keyword-search"]
source_types_covered: ["podcast", "substack", "press"]
new_sources_discovered:
  - id: "defensescoop"
    name: "DefenseScoop"
    type: "Press"
    tier: 2
    url: "https://defensescoop.com"
    notes: "Best source for Pentagon CDAO/AI org restructuring coverage"
  - id: "statescoop"
    name: "StateScoop"
    type: "Press"
    tier: 2
    url: "https://statescoop.com"
    notes: "State government CAIO appointments and AI governance"
organizations_found:
  - id: "sk-telecom"
    status: "new"
  - id: "pentagon-cdao"
    status: "new"
  - id: "new-york-state"
    status: "new"
  - id: "meta"
    status: "evolution"
  - id: "microsoft"
    status: "evolution"
curation_status: "pending"
---

# Research Session: 2026-02-03

## Sources Scanned

| Source | Type | Scanned Through | URL | Results |
|--------|------|-----------------|-----|---------|
| No Priors | Podcast | Ep 148 (CJ Desai, Jan 22) | https://podcasts.apple.com/us/podcast/no-priors-artificial-intelligence-technology-startups/id1668002688 | 2 eps triaged (Emil Michael DoW, CJ Desai MongoDB); Emil Michael HIGH for Pentagon AI |
| Stratechery | Substack | "Microsoft and Software Survival" (Feb 3) | https://stratechery.com/2026/microsoft-and-software-survival/ | 1 org (Microsoft evolution) |
| All-In Podcast | Podcast | First triage through ~E259 (Feb 2026) | https://allin.com/episodes | Macro AI coverage; no org-specific specimens |
| Press keyword search | Press | CAIO appointments Feb 2026 | Various | 3 orgs (NY State CAIO, Pentagon CDAO, SK Telecom AI CIC) |
| Press keyword search | Press | AI layoffs/restructuring Feb 2026 | Various | 2 orgs (Meta Reality Labs, Synopsys); broader trend data |
| BG2 Pod | Podcast | Feed check — no new eps since last scan | https://bg2pod.com | 0 (no new episodes since Feb 1 scan) |
| Latent Space | Podcast | Feed check — World Labs/Fei-Fei Li, MCP ep noted | https://latent.space | 0 new org-specific (World Labs already captured; MCP is protocol, not org structure) |

## Organizations Observed

---

### SK Telecom

**Relevance Test**: STRUCTURAL (company-in-company AI unit, CEO-led, $3.6B investment, 15K employees) + SPECIFICITY (revenue targets, headcount, reporting lines)

#### Raw Observations
- Launched AI CIC (Company-in-Company) in September 2025 — a structurally independent AI business unit within the parent company
- CEO Ryu Young-sang concurrently serves as CEO of the AI CIC — CEO-led, not delegated to a CAIO or CTO
- AI CIC consolidates ALL AI functions: A. personal assistant, A. Biz enterprise service, AI data center business, global AI partnerships (OpenAI, Anthropic), R&D, messaging/authentication
- KRW 5 trillion ($3.6B) committed over 5 years; target: $3.55B in annual AI revenue by 2030
- Business now divided into two halves: MNO (mobile network operations) and AI
- "AI Transformation (AX)" — embedding AI into all internal systems and infrastructure
- New CTO appointed February 2, 2026: Jeong Seokgeun (head of AI CIC) elevated to CTO — AI leader becomes tech leader
- OpenAI exclusive B2C partnership: ChatGPT offered to all SKT subscribers
- Context: major data breach (23M customers) preceded the AI pivot; $514M security investment
- Vision: "core that leads the AI business for the entire SK Group" — not just SKT but cross-conglomerate AI leadership

#### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| AI CIC launch, CEO-led structure | Press | IEEE ComSoc Technology Blog | https://techblog.comsoc.org/2025/09/26/sk-telecom-forms-ai-cic-in-house-company-to-pursue-internal-ai-innovation/ | — | 2025-09-26 | 2026-02-03 |
| $3.6B investment, $3.55B revenue target | Press | TelecomTV | https://www.telecomtv.com/content/telcos-and-ai-channel/sk-telecom-sets-3-55bn-sales-target-for-new-ai-cic-53922/ | — | 2025-09-26 | 2026-02-03 |
| Business split MNO/AI, all AI functions consolidated | Press | Mobile World Live | https://www.mobileworldlive.com/operators/skt-brings-ai-businesses-into-single-unit/ | — | 2025-09-26 | 2026-02-03 |
| Jeong Seokgeun CTO appointment | Press | Asia Economy | https://cm.asiae.co.kr/en/article/2026020220383849862 | — | 2026-02-02 | 2026-02-03 |
| $3.6B commitment, OpenAI partnership | Press | RCR Wireless | https://www.rcrwireless.com/20250926/ai-infrastructure/sk-telecom-ai-5 | — | 2025-09-26 | 2026-02-03 |
| CEO-led CIC, trust rebuilding post-breach | Press | Neuron Expert | https://neuron.expert/news/sk-telecom-sets-355bn-sales-target-for-new-ai-cic/14409/en/ | — | 2025-09-26 | 2026-02-03 |

#### Quotes
> "the main driver of SK's AI business and, furthermore, the core that leads the AI business for the entire SK Group"
> — SK Telecom, via TelecomTV, September 2025

#### Open Questions
- How does the CIC model differ from a traditional subsidiary spin-off? What governance independence does it actually have?
- Is the MNO/AI split creating internal tension between the legacy telecom business and AI ambitions?
- Other telecom companies adopting similar CIC structures?

---

### Pentagon (Department of War) CDAO

**Relevance Test**: STRUCTURAL (CDAO restructured under R&E, dual-hatted role, 6 innovation orgs consolidated, CDAO CTO directorate dissolved) + TENSION (AI innovation speed vs. bureaucratic oversight) + SPECIFICITY (7 Pace-Setting Projects, 30-day model deployment cadence, named leaders)

#### Raw Observations
- CDAO (Chief Digital and AI Officer) restructured: previously reported to Deputy Secretary of Defense, now moved under Under Secretary of War for Research & Engineering (Emil Michael) as of August 2025
- Cameron Stanley named CDAO (January 2026): Project Maven alum, ex-AWS national security lead, dual-hatted as Senior Official for Applied AI
- CDAO now one of 6 innovation organizations under Emil Michael: SCO, DIU, CDAO, DARPA, Test Resource Management Center, Office of Strategic Capital
- Three overlapping oversight bodies dissolved (Defense Innovation Steering Group, Defense Innovation Working Group, CTO Council) → replaced by single "Action Group" under CTO
- CDAO's own CTO directorate dissolved — described as "due to inefficiencies linked to budget cuts"
- January 9, 2026: Two key strategy memos released — AI Strategy for DoW + Transforming Defense Innovation Ecosystem
- Secretary Hegseth: DoW to become "AI-first warfighting force across all components, from front to back"
- 7 Pace-Setting Projects identified for CDAO, including GenAI.mil platform
- AI model parity directive: latest AI models deployed within 30 days of public release
- "Barrier removal SWAT team" under R&E with authority to waive non-statutory requirements
- Data Decrees enforcement mandate for CDAO
- Senior technical talent exodus from CDAO reported
- Pentagon CTO picked 6 defense tech veterans to lead Critical Technology Areas (Jan 30, 2026)

#### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| AI Strategy memos, CDAO restructuring | Press | DefenseScoop | https://defensescoop.com/2026/01/13/hegseth-ai-tech-hubs-reorganization-dod-dow/ | — | 2026-01-13 | 2026-02-03 |
| Cameron Stanley named CDAO | Press | CDO Magazine | https://www.cdomagazine.tech/leadership-moves/pentagon-names-cameron-stanley-chief-digital-and-ai-officer | — | 2026-01-07 | 2026-02-03 |
| CDAO moved under R&E (Aug 2025) | Press | Congress.gov/CRS | https://www.congress.gov/crs-product/IN12615 | — | 2025-08-14 | 2026-02-03 |
| CDAO CTO directorate dissolved | Press | DEFCROS News | https://news.defcros.com/pentagons-ai-office-streamlines-operations/ | — | 2026-01-xx | 2026-02-03 |
| Pentagon AI strategy document | Filing | DoD Media | https://media.defense.gov/2026/Jan/12/2003855671/-1/-1/0/ARTIFICIAL-INTELLIGENCE-STRATEGY-FOR-THE-DEPARTMENT-OF-WAR.PDF | — | 2026-01-12 | 2026-02-03 |
| 6 CTA appointees under CTO | Press | Breaking Defense | https://breakingdefense.com/2026/01/pentagon-cto-picks-six-defense-tech-vets-to-lead-critical-technology-areas/ | — | 2026-01-30 | 2026-02-03 |
| Stanley dual-hatted, industry engagement | Press | GovConWire | https://www.govconwire.com/articles/cdao-cameron-stanley-pentagon-ai-industry | — | 2026-01-xx | 2026-02-03 |
| Innovation ecosystem consolidation | Press | Inside Government Contracts | https://www.insidegovernmentcontracts.com/2026/02/pentagon-releases-artificial-intelligence-strategy/ | — | 2026-02-xx | 2026-02-03 |

#### Quotes
> "an 'AI-first' warfighting force across all components, from front to back"
> — Secretary of War Pete Hegseth, January 2026

#### Evolution Flags
- EVOLUTION: CDAO reporting to Deputy SecDef (2022-2025) → CDAO under Under Secretary for R&E (Aug 2025+)
- EVOLUTION: 3 separate oversight bodies → single "Action Group" under CTO
- EVOLUTION: CDAO had its own CTO directorate → dissolved for efficiency

#### Open Questions
- Does consolidating 6 innovation orgs under one person (Emil Michael) help or hinder AI adoption speed?
- Senior talent exodus from CDAO — is this the explore/execute tension in action? (Innovation talent departing as bureaucratic oversight increases)
- How does the 30-day model deployment mandate actually work in classified environments?

---

### New York State

**Relevance Test**: STRUCTURAL (CAIO turnover — 2nd appointment in under a year, Empire AI consortium) + SPECIFICITY (named individuals, background details, AI training pilot for 1,000 employees)

#### Raw Observations
- Eleonore Fournier-Tombs appointed as New York State's 2nd CAIO (January 9, 2026)
- Replaces Shreya Amin, who was the state's first CAIO — departed after less than one year for "personal and professional reasons, including the launch of her new company"
- Fournier-Tombs background: 15+ years tech innovation, founded UN University's first AI policy research lab, led anticipatory action and governance for predictive analytics in crisis forecasting
- Key distinction: academic/international → government CAIO pipeline (contrast with corporate pipelines documented earlier)
- Empire AI: statewide supercomputing consortium for university AI research, launched by Governor Hochul
- AI education pilot completed: ~1,000 state employees across multiple agencies
- Priorities: expand AI tools for state employees, refine "Acceptable Use of AI Technologies" policy
- Part of broader wave: NY joins OK, MT, TX, NC, AR, IL in naming state-level CAIOs

#### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| Fournier-Tombs appointment, background | Press | StateScoop | https://statescoop.com/new-york-state-chief-ai-officer-eleonore-fournier-tombs/ | — | 2026-01-09 | 2026-02-03 |
| Official announcement, priorities | Press | NY ITS | https://its.ny.gov/news/new-york-state-office-information-technology-services-appoints-eleonore-fournier-tombs-chief | — | 2026-01-09 | 2026-02-03 |
| Amin departure details | Press | StateScoop | https://statescoop.com/new-york-state-chief-ai-officer-eleonore-fournier-tombs/ | — | 2026-01-09 | 2026-02-03 |
| Empire AI launch by Hochul | Press | Governor's Office | https://www.governor.ny.gov/news/governor-hochul-unveils-fifth-proposal-2024-state-state-empire-ai-consortium-make-new-york | — | 2024-01-xx | 2026-02-03 |

#### Open Questions
- Why did the first CAIO depart after <1 year? Is this a pattern in government CAIO roles?
- How does Empire AI compare to other state-level AI infrastructure investments?
- Is the academic/UN → government pipeline a distinct archetype from the corporate CAIO pipelines?

---

### Meta (Evolution)

**Relevance Test**: STRUCTURAL (Reality Labs 10% cut, VR studio closures, pivot to AI wearables) + TENSION (metaverse exploration vs. AI execution) + SPECIFICITY ($70B cumulative losses, 1,500 jobs, named studios)

#### Raw Observations
- Reality Labs cuts: ~1,500 jobs (10% of ~15,000 workforce) in January 2026
- Three VR game studios closed: Armature, Sanzaru, Twisted Pixel
- Five studios retained: Camouflaj, Glassworks, Games, BigBox, OURO — narrowing, not abandoning VR
- AR/wearables teams (Ray-Ban smart glasses) NOT cut — protected as growth area
- Exploring doubling smart glasses production to 20M units/year by end of 2026
- $70B+ cumulative Reality Labs losses since 2020; Q4: $4.4B loss on $470M revenue
- CFO Susan Li: Reality Labs losses expected to peak in 2026, gradual reduction from 2027
- Meta spokesperson: "shifting some of our investment from Metaverse toward Wearables"
- This follows the earlier Wang/CAIO restructuring and Scale AI acquisition documented in prior sessions
- EVOLUTION: Metaverse exploration (2020-2025) → AI wearables + foundation models (2026+)

#### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| 1,500 cuts, 10% Reality Labs, studio closures | Press | CNBC | https://www.cnbc.com/2026/01/13/meta-lays-off-vr-employees-underscoring-zuckerbergs-pivot-to-ai.html | — | 2026-01-13 | 2026-02-03 |
| $70B cumulative losses, CFO Li guidance | Press | Storyboard18 | https://www.storyboard18.com/brand-marketing/meta-cuts-1500-jobs-as-cfo-susan-li-signals-reality-labs-pivot-towards-wearables-88694.htm | — | 2026-01-xx | 2026-02-03 |
| Studios retained/closed list | Press | GeekWire | https://www.geekwire.com/2026/report-meta-plans-to-cut-around-10-of-reality-labs-workforce/ | — | 2026-01-xx | 2026-02-03 |
| 20M smart glasses target | Press | TrendForce | https://www.trendforce.com/news/2026/01/27/news-meta-reportedly-scales-back-vr-with-10-reality-labs-layoffs-pivots-to-ai-and-wearables/ | — | 2026-01-27 | 2026-02-03 |
| Bay Area impact, 1,000+ cuts | Press | SF Chronicle | https://www.sfchronicle.com/tech/article/meta-layoffs-reality-labs-21291249.php | — | 2026-01-xx | 2026-02-03 |

#### Evolution Flags
- EVOLUTION: Reality Labs as metaverse exploration vehicle (2020-2025, $70B investment) → pivot to AI wearables + foundation models (2026), with $14.3B Scale AI/Wang hire on foundation model side

---

### Microsoft (Evolution)

**Relevance Test**: TENSION (OpenAI partnership becoming liability, 45% Azure RPO concentration) + STRUCTURAL (dependency on external AI partner vs. internal MAI)

#### Raw Observations
- Stratechery "Microsoft and Software Survival" (Feb 3, 2026): OpenAI now represents 45% of Azure's Remaining Performance Obligations (RPO)
- Market now views OpenAI concentration as a detriment, not an asset — reversal from 2023 sentiment
- "Full circle moment" — Microsoft went from biggest perceived winner of ChatGPT to facing existential software questions
- This extends the dual-model tension documented in prior sessions: OpenAI (external partner) vs. MAI (internal models under Suleyman)
- Structural question: Can Microsoft maintain a dual-source AI strategy (OpenAI + MAI) when one partner is 45% of cloud revenue?

#### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| OpenAI = 45% Azure RPO, market reversal | Substack | Stratechery | https://stratechery.com/2026/microsoft-and-software-survival/ | — | 2026-02-03 | 2026-02-03 |

#### Evolution Flags
- EVOLUTION: OpenAI partnership as strategic advantage (2023-2025) → OpenAI concentration as strategic risk (2026), with market sentiment reversal

#### Open Questions
- Does the 45% RPO concentration force Microsoft to accelerate internal MAI development?
- Is this the beginning of an OpenAI/MAI structural separation within Microsoft?

---

## Broader Trends

### AI Workforce Restructuring Continues at Scale
- **25,000 tech jobs cut in January 2026 alone** across 27 companies (Layoffs.fyi)
- AI cited as primary driver; total AI-attributed layoffs ~55,000 in 2025 (Challenger, Gray & Christmas)
- Major January 2026 cuts: Amazon (16K), Meta Reality Labs (1,500), Synopsys (~2,000)
- **41% of companies worldwide** expect to reduce workforces over next 5 years due to AI (WEF)

### "AI-Washing" — A Growing Credibility Problem
- TechCrunch (Feb 1, 2026): "AI layoffs or AI-washing?" — companies citing AI for cuts that look like routine cost control
- Oxford Economics: "firms don't appear to be replacing workers with AI on a significant scale"
- Forrester: 55% of employers regret AI-attributed layoffs; half will be quietly rehired (offshore/lower pay)
- This supports the "redundancy washing" counter-explanation in our insight #11 (convergent restructuring)

### Pentagon Goes "AI-First"
- DoW releasing formal AI strategy memos for the first time (Jan 12, 2026)
- CDAO restructured under R&E — consolidation of 6 innovation orgs
- 30-day model deployment mandate is unprecedented for government
- "Barrier removal SWAT team" concept — structural mechanism for removing bureaucratic obstacles
- Pentagon explicitly framing AI as warfighting capability, not just administrative efficiency

### CAIO Pipeline Continues Diversifying
- **Academic/UN → Government**: NY State CAIO Fournier-Tombs (UN University → state government)
- **Military → Pentagon CDAO**: Cameron Stanley (Air Force → Project Maven → AWS → CDAO)
- CAIO turnover appearing: NY State's 1st CAIO departed in <1 year
- State-level CAIO wave expanding: NY, OK, MT, TX, NC, AR, IL now have or are hiring state CAIOs

### No Priors Podcast: DoW AI Episode
- Ep 147 with Emil Michael (Under Secretary of War for R&E) — significant for Pentagon AI org structure
- Worth deep-scan: covers GenAI.mil deployment to millions, innovation priorities, change management in government, defense industrial base rebuilding
- Flagged as HIGH priority for deep-scan backlog

### All-In Podcast: First Triage Assessment
- Primarily macro AI/market commentary, VC perspective
- AI-specific segments include AI bubble debate, Gemini 3 competitive landscape, AI moratorium debate
- Low density of org-structural findings — better for market context than specimen data
- CrowdStrike CEO Kurtz segment potentially relevant for cybersecurity AI org structure
- David Sacks now in government (DOGE) — potential future source for government AI restructuring

---

## Source Index

- https://techblog.comsoc.org/2025/09/26/sk-telecom-forms-ai-cic-in-house-company-to-pursue-internal-ai-innovation/ — SK Telecom AI CIC formation
- https://www.telecomtv.com/content/telcos-and-ai-channel/sk-telecom-sets-3-55bn-sales-target-for-new-ai-cic-53922/ — SKT revenue targets
- https://www.mobileworldlive.com/operators/skt-brings-ai-businesses-into-single-unit/ — SKT business split
- https://cm.asiae.co.kr/en/article/2026020220383849862 — SKT CTO appointment
- https://www.rcrwireless.com/20250926/ai-infrastructure/sk-telecom-ai-5 — SKT $3.6B commitment
- https://defensescoop.com/2026/01/13/hegseth-ai-tech-hubs-reorganization-dod-dow/ — Pentagon AI reorg
- https://www.cdomagazine.tech/leadership-moves/pentagon-names-cameron-stanley-chief-digital-and-ai-officer — CDAO appointment
- https://www.congress.gov/crs-product/IN12615 — CDAO realignment under R&E
- https://media.defense.gov/2026/Jan/12/2003855671/-1/-1/0/ARTIFICIAL-INTELLIGENCE-STRATEGY-FOR-THE-DEPARTMENT-OF-WAR.PDF — DoW AI strategy document
- https://breakingdefense.com/2026/01/pentagon-cto-picks-six-defense-tech-vets-to-lead-critical-technology-areas/ — CTA appointees
- https://news.defcros.com/pentagons-ai-office-streamlines-operations/ — CDAO CTO directorate dissolved
- https://www.insidegovernmentcontracts.com/2026/02/pentagon-releases-artificial-intelligence-strategy/ — Pentagon AI strategy analysis
- https://www.govconwire.com/articles/cdao-cameron-stanley-pentagon-ai-industry — Stanley industry engagement
- https://statescoop.com/new-york-state-chief-ai-officer-eleonore-fournier-tombs/ — NY State CAIO
- https://its.ny.gov/news/new-york-state-office-information-technology-services-appoints-eleonore-fournier-tombs-chief — NY ITS announcement
- https://www.governor.ny.gov/news/governor-hochul-unveils-fifth-proposal-2024-state-state-empire-ai-consortium-make-new-york — Empire AI
- https://www.cnbc.com/2026/01/13/meta-lays-off-vr-employees-underscoring-zuckerbergs-pivot-to-ai.html — Meta Reality Labs cuts
- https://www.storyboard18.com/brand-marketing/meta-cuts-1500-jobs-as-cfo-susan-li-signals-reality-labs-pivot-towards-wearables-88694.htm — Meta CFO guidance
- https://www.geekwire.com/2026/report-meta-plans-to-cut-around-10-of-reality-labs-workforce/ — Meta studios list
- https://www.trendforce.com/news/2026/01/27/news-meta-reportedly-scales-back-vr-with-10-reality-labs-layoffs-pivots-to-ai-and-wearables/ — Meta smart glasses target
- https://www.sfchronicle.com/tech/article/meta-layoffs-reality-labs-21291249.php — Meta Bay Area impact
- https://stratechery.com/2026/microsoft-and-software-survival/ — Microsoft/OpenAI strategic tension
- https://www.businesstoday.in/technology/news/story/one-month-into-2026-global-tech-and-startup-layoffs-near-25000-514445-2026-02-03 — 25K Jan 2026 layoffs
- https://techcrunch.com/2026/02/01/ai-layoffs-or-ai-washing/ — AI-washing credibility questions
- https://fortune.com/2026/01/07/ai-layoffs-convenient-corporate-fiction-true-false-oxford-economics-productivity/ — Oxford Economics AI layoffs analysis
- https://hrexecutive.com/the-ai-layoff-trap-why-half-will-be-quietly-rehired/ — Forrester rehiring prediction

## Notes for Next Session

### Deep-Scan Backlog (Updated)
- **HIGH**: No Priors Ep 147 — Emil Michael (Under Secretary of War) on DoW AI transformation, GenAI.mil, change management. Rich structural content.
- **HIGH**: BG2 Pod — Michael Dell ep (Dell Technologies AI org), Satya/Sam Halloween ep
- **HIGH**: Dwarkesh — Karpathy (Oct 17)
- **HIGH**: Acquired — Alphabet Inc (Aug 26)
- **MEDIUM**: Latent Space — Glean enterprise AI, World Labs/Fei-Fei Li (already captured as specimen)
- **MEDIUM**: Acquired — Coca-Cola, Dimon, Tobi Lutke

### Follow-ups Needed
- SK Telecom: CIC governance model details — how independent is it actually? Other telecom companies with similar structures?
- Pentagon CDAO: Impact of R&E consolidation on AI talent retention; GenAI.mil deployment status
- NY State CAIO turnover: Is sub-1-year tenure common in government CAIO roles? Pattern or anomaly?
- Meta: Post-Reality Labs pivot — how does the AI wearables org structure differ from the VR/metaverse org?
- Microsoft: Internal MAI team response to OpenAI RPO concentration risk
- Stratechery "AI and the Human Condition" article — check for org-structural content
- All-In Podcast: Monitor for David Sacks government AI segments (DOGE/AI policy)
- Synopsys: ~2,000 cuts tied to Ansys acquisition + AI restructuring — needs more structural detail

### Sources Still Unscanned
- Lex Fridman (Tier 2 podcast — never scanned)
- SEC filings / earnings calls (Q4 2025 season — never scanned)
- BCG AI Radar, OpenAI Enterprise Report, Deloitte Tech Trends (Tier 2 reports)
- CNBC, Fortune, Wired, MIT Tech Review (Tier 2 press)
- Mercer GTT 2026 full report (expected Feb 2026)
