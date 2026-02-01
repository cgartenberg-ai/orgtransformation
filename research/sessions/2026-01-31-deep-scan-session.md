---
session_date: "2026-01-31"
sources_planned: ["dwarkesh-podcast", "acquired", "cheeky-pint", "stratechery", "press-keyword-search"]
sources_scanned: ["dwarkesh-podcast", "acquired", "cheeky-pint", "stratechery", "press-keyword-search"]
source_types_covered: ["podcast", "substack", "press"]
new_sources_discovered: []
organizations_found:
  - id: "microsoft"
    status: "evolution"
    curated: true
  - id: "ssi"
    status: "new"
    curated: true
  - id: "google"
    status: "evolution"
    curated: true
    notes: "Evolution applied to google-deepmind specimen (historical AI org arc from Acquired deep-scan)"
  - id: "sierra-ai"
    status: "new"
    curated: true
  - id: "citigroup"
    status: "new"
    curated: true
curation_status: "curated"
---

# Research Session: 2026-01-31 (Deep Scan)

Focus: Deep-scanning high-priority podcast episodes triaged in previous sessions (Dwarkesh Nadella, Dwarkesh Sutskever, Acquired Google AI, Acquired Taylor/Bavor) + catch-up on stale Tier 1 sources (Cheeky Pint, Stratechery) + fresh press.

## Sources Scanned

| Source | Type | Scanned Through | URL | Results |
|--------|------|-----------------|-----|---------|
| Dwarkesh Podcast | Podcast | Nadella ep (Nov 12) deep-scanned | https://dwarkesh.com/p/satya-nadella-2 | 1 org (Microsoft) |
| Dwarkesh Podcast | Podcast | Sutskever ep (Nov 25) deep-scanned | https://dwarkesh.com/p/ilya-sutskever-2 | 1 org (SSI) |
| Acquired | Podcast | "Google: The AI Company" (Oct 5) deep-scanned | https://acquired.fm/episodes/google-the-ai-company | 1 org (Google) |
| Acquired | Podcast | Taylor/Bavor "How is AI Different" (Aug 18) deep-scanned | https://acquired.fm/episodes/how-is-ai-different-than-other-technology-waves-with-bret-taylor-and-clay-bavor | 1 org (Sierra AI) |
| Cheeky Pint | Podcast | Checked; no new eps since Nov 25, 2025 | https://podcasts.apple.com/us/podcast/cheeky-pint/id1821055332 | 0 (on hiatus) |
| Stratechery | Substack | Checked Jan 15-31 2026; "Chip Fly" + "Technology Doings" | https://stratechery.com | 0 new orgs (macro AI infra) |
| Press | Press | AI restructuring/CAIO/layoffs Feb 2026 | Google search | 1 new org (Citigroup) |

---

## Organizations Observed

---

## Microsoft (Deep Scan — Dwarkesh: Nadella "How Microsoft is preparing for AGI")

### Raw Observations
- Nadella describes Microsoft's AI approach as **vertically integrated**: "We will have access to OpenAI models...And we'll build our own models with MAI. So we will always have a model level."
- Product-focused vertical teams rather than centralized AI center: "Whether it's in security, whether it's in knowledge work, whether it's in coding, or in science — our own application scaffolding"
- Exclusive first look at **Fairwater 2 datacenter**: hundreds of thousands of GB200s/GB300s, over 2 GW total capacity across multiple interconnected buildings
- 10x training capacity increase every 18-24 months as organizational planning cadence
- Key AI talent acquisitions: Mustafa Suleyman (Microsoft AI lab), Amar Subramanya (from Gemini 2.5 post-training), Nando de Freitas (from DeepMind)
- Resource allocation philosophy: "We have to use our knowledge to increase the ROIC on the capital spend" — knowledge-intensity drives investment decisions, not pure scale
- "Satya tokens" framing: at some point a machine produces "Satya tokens" and the board believes those are worth a lot — continuous learning models deployed broadly through economy
- Dylan Patel (SemiAnalysis) joined for datacenter tour — signals infrastructure as competitive moat

### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| Vertical AI org: models + app scaffolding | Podcast | Dwarkesh Podcast, Satya Nadella | https://www.dwarkesh.com/p/satya-nadella-2 | — | 2025-11-12 | 2026-01-31 |
| Fairwater 2: hundreds of thousands GB200s, 2GW+ | Podcast | Dwarkesh Podcast, Satya Nadella | https://www.dwarkesh.com/p/satya-nadella-2 | — | 2025-11-12 | 2026-01-31 |
| Key hires: Suleyman, Subramanya, de Freitas | Podcast | Dwarkesh Podcast, Satya Nadella | https://www.dwarkesh.com/p/satya-nadella-2 | — | 2025-11-12 | 2026-01-31 |
| 10x training capacity every 18-24 months | Podcast | Dwarkesh Podcast, Satya Nadella | https://www.dwarkesh.com/p/satya-nadella-2 | — | 2025-11-12 | 2026-01-31 |
| ROIC on capital spend philosophy | Podcast | Dwarkesh Podcast, Satya Nadella | https://www.dwarkesh.com/p/satya-nadella-2 | — | 2025-11-12 | 2026-01-31 |

### Quotes
> "We will have access to OpenAI models...And we'll build our own models with MAI. So we will always have a model level. And then we'll build — whether it's in security, whether it's in knowledge work, whether it's in coding, or in science — our own application scaffolding."
> — Satya Nadella, CEO Microsoft, Dwarkesh Podcast, November 12, 2025

> "We have to use our knowledge to increase the ROIC on the capital spend."
> — Satya Nadella, CEO Microsoft, Dwarkesh Podcast, November 12, 2025

### Evolution Flags
- EVOLUTION: Microsoft AI structure is now **dual model source** (OpenAI external + MAI internal) with **product-vertical application teams**. This extends the three-tier model (token factory → agent factory → Copilot) previously documented.

### Open Questions
- What is the org chart relationship between MAI (internal model team) and the OpenAI partnership?
- How are the product vertical teams (security, knowledge work, coding, science) structured?
- Mustafa Suleyman's exact scope and reporting at Microsoft AI?

---

## SSI (Safe Superintelligence Inc.) — Deep Scan: Dwarkesh Sutskever Episode

### Raw Observations
- SSI explicitly positioned as "a research company" — Sutskever states "We are squarely an 'age of research' company"
- Organizational model: pure research, no product teams, no sales, no customer-facing engineering
- Resource allocation philosophy: most major AI labs fragment compute across inference, products, multiple modalities; SSI concentrates all compute on research
- $3B funding, but argues "the amount of compute that SSI has for research is really not that small" because competitors dilute theirs across product/sales/engineering
- Structural argument for research org efficiency: fewer "work streams" = more focused impact per dollar
- Hiring philosophy: "people who think differently rather than the same" — values diversity of thought over scale of headcount
- Sutskever's AI era framework: 2012-2020 = age of research, 2020-2025 = age of scaling, 2026+ = age of research again "just with big computers"
- Generalization as the core bottleneck — not compute or data — implying org design should prioritize novel research approaches over engineering scale
- "Jaggedness" problem: models perform excellently on benchmarks but have limited economic impact, suggesting current product-focused orgs may be misallocating resources

### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| "Squarely an age of research company" | Podcast | Dwarkesh Podcast, Ilya Sutskever | https://www.dwarkesh.com/p/ilya-sutskever-2 | — | 2025-11-25 | 2026-01-31 |
| $3B funding, compute concentrated on research | Podcast | Dwarkesh Podcast, Ilya Sutskever | https://www.dwarkesh.com/p/ilya-sutskever-2 | — | 2025-11-25 | 2026-01-31 |
| Competitors fragment compute across products/sales | Podcast | Dwarkesh Podcast, Ilya Sutskever | https://www.dwarkesh.com/p/ilya-sutskever-2 | — | 2025-11-25 | 2026-01-31 |
| "People who think differently" hiring philosophy | Podcast | Dwarkesh Podcast, Ilya Sutskever | https://www.dwarkesh.com/p/ilya-sutskever-2 | — | 2025-11-25 | 2026-01-31 |
| Era framework: scaling → research again | Podcast | Dwarkesh Podcast, Ilya Sutskever | https://www.dwarkesh.com/p/ilya-sutskever-2 | — | 2025-11-25 | 2026-01-31 |

### Quotes
> "We are squarely an 'age of research' company."
> — Ilya Sutskever, CEO SSI, Dwarkesh Podcast, November 25, 2025

### Open Questions
- How many people does SSI employ? What is the researcher-to-engineer ratio?
- What is the internal team structure at SSI? Single research group or multiple?
- How does SSI plan to transition from research to product (if ever)?
- Relationship between SSI's pure research model and eventual commercialization

---

## Google (Deep Scan — Acquired "Google: The AI Company")

### Raw Observations
- **Early AI org was decentralized**: After Larry Page removed managers, "everybody was just doing whatever they wanted to do" — Noam Shazeer and George Herrick worked on language models informally from 2001
- **Google X as AI incubator** (2009): Sebastian Thrun recruited academic AI researchers as part-time consultants/interns maintaining university posts → successful model led to X creation
- **Google Brain team structure** (2011): Three principals — Jeff Dean (infrastructure/systems), Andrew Ng (research direction), Greg Corrado (neuroscience) — built DistBelief as distributed computing system
- **DNN Research acquisition** (2012): Geoff Hinton, Alex Krizhevsky, Ilya Sutskever acquired for ~$44M; joined Google Brain directly; negotiated 40/30/30 split (not equal)
- **DeepMind acquisition structure** (2014, $550M): Critical decision — DeepMind remained **operationally separate in London**, not merged into Brain or product teams. Independent oversight board ensured mission fidelity. Maintained own research agenda separate from Google product requirements
- **Dual structure = explore/execute tension**: Google Brain was product-focused (search, ads, YouTube optimization) while DeepMind was research-focused (pursuing AGI independently). This separation preserved DeepMind's mission integrity but may have **delayed Google's response to ChatGPT**
- **Talent exodus catalyst**: Summer 2015 dinner at Rosewood Hotel — Elon Musk and Sam Altman approached Google-employed researchers. Most declined but **Ilya Sutskever expressed interest** → OpenAI founded December 2015, directly siphoning talent
- **Gemini as response**: All-hands-on-deck response to ChatGPT (Nov 2022), but limited structural detail on reorganization
- **Gemini scale by Oct 2025**: 450M users, revenue at all-time highs; Google uniquely possesses all four AI pillars (application, model, chip, cloud)
- **DeepMind acquisition as "YouTube of AI"**: Hosts compare to YouTube and Instagram as greatest acquisitions of all time

### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| Early decentralized AI, no managers | Podcast | Acquired "Google: The AI Company" | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| Google X as AI incubator, academic consultant model | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| Brain team: Dean/Ng/Corrado, DistBelief | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| DNN Research: Hinton/Krizhevsky/Sutskever, $44M | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| DeepMind kept separate in London, $550M | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| Dual structure: Brain (products) vs DeepMind (AGI) | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| Rosewood dinner → Sutskever → OpenAI | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |
| Gemini 450M users, 4 AI pillars | Podcast | Acquired | https://www.acquired.fm/episodes/google-the-ai-company | — | 2025-10-05 | 2026-01-31 |

### Quotes
> "Demis can really believe Larry when Larry says, nah, stay in London. Keep working on intelligence. Do what you're doing."
> — Ben Gilbert / David Rosenthal, Acquired, October 5, 2025 (paraphrasing the acquisition dynamic)

### Evolution Flags
- EVOLUTION: Google's AI org went through distinct phases: decentralized (2001-2009) → X incubator (2009-2011) → dual structure Brain+DeepMind (2014-2023) → merged Google DeepMind (2023+) → Project EAT consolidation (2025-2026). Each phase represents a different explore/execute balance.

### Open Questions
- Transcript needs deeper reading for specific post-ChatGPT org changes
- How did the Brain/DeepMind merger actually work in practice? Who reports to whom?
- What happened to the independent oversight board for DeepMind?
- How does the Project EAT consolidation (from previous session) relate to this history?

---

## Sierra AI (Deep Scan — Acquired: Bret Taylor + Clay Bavor)

### Raw Observations
- Sierra AI co-founded by Bret Taylor and Clay Bavor — both ex-Google AI leaders
- Taylor's career path: Google Maps co-creator → FriendFeed founder → Facebook CTO → Quip founder → Salesforce co-CEO → Twitter Board Chair → OpenAI Board Chair → Sierra CEO
- Bavor's career path: 18+ years at Google, APM alongside Taylor → ran Gmail, Drive, Docs (all Google Workspace), Google Labs, AR/VR → Sierra co-founder
- Key insight: **AI rides on cumulative infrastructure** (PCs → internet → smartphones) enabling unprecedented adoption speed
- Organizational philosophy: "We only charge our customers when their agent successfully completes the task" — outcome-based pricing model
- AI agents as organizational unit: Taylor hypothesizes "agent" will stick as a word, similar to "app" — agents will be more important than apps or websites
- Internal culture: both emphasize using AI internally — "can't succeed if they're not the poster child for automation"
- AI framing: "I don't think it's just software" — AI makes intelligence plentiful (vs. past waves making scarce goods plentiful)
- Asset-heavy business models as new norm for hyperscalers — massive CapEx required

### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| Taylor + Bavor backgrounds, Sierra founding | Podcast | Acquired ACQ2 | https://www.acquired.fm/episodes/how-is-ai-different-than-other-technology-waves-with-bret-taylor-and-clay-bavor | — | 2025-08-18 | 2026-01-31 |
| Outcome-based pricing for AI agents | Podcast | Acquired ACQ2 | https://www.acquired.fm/episodes/how-is-ai-different-than-other-technology-waves-with-bret-taylor-and-clay-bavor | — | 2025-08-18 | 2026-01-31 |
| "Agent" as organizational unit replacing "app" | Podcast | Acquired ACQ2 | https://www.acquired.fm/episodes/how-is-ai-different-than-other-technology-waves-with-bret-taylor-and-clay-bavor | — | 2025-08-18 | 2026-01-31 |
| Internal AI-first culture | Podcast | Acquired ACQ2 | https://www.acquired.fm/episodes/how-is-ai-different-than-other-technology-waves-with-bret-taylor-and-clay-bavor | — | 2025-08-18 | 2026-01-31 |

### Quotes
> "We only charge our customers when their agent successfully completes the task."
> — Clay Bavor, co-founder Sierra AI, Acquired, August 18, 2025

### Open Questions
- How is Sierra AI structured internally? Engineering vs. product vs. research?
- What is the team size and composition?
- How does Taylor's board role at OpenAI affect Sierra's positioning?

---

## Citigroup

### Raw Observations
- CFO Mark Mason expects headcount to be down by ~20,000 as part of broad overhaul
- Automation and AI-enabled systems will allow middle-office and operational functions to run with fewer employees
- Part of broader pattern: financial services AI restructuring (joins UBS CAIO appointment, Wells Fargo AI head, JPMorgan existing specimen)

### Specimen Sources

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| 20K headcount reduction via AI automation | Press | CNBC | https://www.cnbc.com/2025/12/21/ai-job-cuts-amazon-microsoft-and-more-cite-ai-for-2025-layoffs.html | — | 2025-12-21 | 2026-01-31 |

### Open Questions
- What is Citigroup's AI organizational structure? Central team or federated?
- Does Citigroup have a CAIO?
- Which specific middle-office/operational functions are being automated?

---

## Broader Trends Observed

### 1. The Explore/Execute Structural Evolution at Google
The Acquired deep-scan reveals a 25-year arc:
- **Decentralized exploration** (2001-2009): No formal AI org, researchers doing "whatever they wanted"
- **Incubator model** (2009-2011): Google X as structured exploration vehicle
- **Dual structure** (2014-2023): Brain (execution/products) + DeepMind (exploration/AGI) — separate orgs, separate missions
- **Forced merger** (2023+): ChatGPT crisis forces integration of explore and execute
- **Consolidation** (2025-2026): Project EAT merging research, cloud, hardware under AI2

This is the most complete structural evolution narrative in the entire research collection.

### 2. Pure Research Lab vs. Product Lab Organizational Models
Sutskever's SSI represents the **purest exploration model**: no products, no sales, all compute on research. This contrasts sharply with:
- **Microsoft**: Vertical integration (models + product scaffolding)
- **Google (pre-merger)**: Dual structure (research lab + product lab)
- **Sierra AI**: Product-first with outcome-based pricing

### 3. AI Workforce Restructuring: The "Re-Framing" Debate
Oxford Economics research suggests companies may be "dressing up" demand-driven cuts as AI-driven restructuring for investor relations. LinkedIn data shows AI-related roles among fastest-growing jobs. The structural reality may be reallocation rather than pure elimination.

### 4. Financial Services AI Restructuring Wave
- **Citigroup**: -20K via AI automation of middle office
- **UBS**: First CAIO (Magazzeni, Jan 2026)
- **Wells Fargo**: Head of AI (Van Beurden) + Head of AI Products (Shafiq)
- **JPMorgan**: Existing AI CoE specimen
- **Commonwealth Bank**: First CAIO (Boteju)

This sector shows the clearest pattern of structural AI-driven reorganization.

---

## Source Catch-Up Notes

### Cheeky Pint
- No new episodes published since Nov 25, 2025 (Julia DeWahl / Antares nuclear micro-reactors)
- Appears to be on seasonal hiatus
- No new content to scan; scannedThroughDate remains 2025-11-18 but confirmed no gap

### Stratechery (Jan 15-31, 2026)
- "The Chip Fly in the AI Ointment" (2026.05) — AI chip supply constraints; macro, not org-specific
- "Technology Doings" (2026.03) — Roundup: Apple/Gemini Siri deal official, Meta Compute announcement, United Airlines tech transformation
- No new org-specific specimens; content is macro AI infrastructure analysis
- scannedThroughDate can be updated to 2026-01-31

---

## Source Index

### Podcast Transcripts Deep-Scanned
- https://www.dwarkesh.com/p/satya-nadella-2 — Nadella AGI preparation transcript
- https://www.dwarkesh.com/p/ilya-sutskever-2 — Sutskever scaling→research transcript
- https://www.acquired.fm/episodes/google-the-ai-company — Google AI Company episode
- https://podscripts.co/podcasts/acquired/google-the-ai-company — Google AI transcript
- https://www.acquired.fm/episodes/how-is-ai-different-than-other-technology-waves-with-bret-taylor-and-clay-bavor — Taylor/Bavor episode

### Press
- https://www.cnbc.com/2025/12/21/ai-job-cuts-amazon-microsoft-and-more-cite-ai-for-2025-layoffs.html — AI layoffs 2025 roundup
- https://www.thehrdigest.com/are-you-next-the-truth-behind-ai-layoffs-in-2026 — AI layoffs 2026 analysis
- https://fortune.com/2025/12/17/ai-layoff-wave-just-beginning-by-design-jobless-growth/ — AI layoff wave analysis
- https://www.hrdive.com/news/ceos-eye-ai-adoption-primary-2026-goal-job-cuts-continue/807326/ — CEO AI adoption priorities

### Stratechery
- https://stratechery.com/2026/the-chip-fly-in-the-ai-ointment/ — [paywall] Chip supply constraints
- https://stratechery.com/2026/technology-doings/ — [paywall] Weekly roundup

---

## Notes for Next Session

### Deep-scan queue (still pending)
1. **Acquired: "Coca-Cola"** (Nov 23, 2025) — Cross-reference with restructuring findings
2. **Acquired: Jamie Dimon Interview** (Jul 16, 2025) — JPMorgan AI strategy
3. **Acquired: Tobi Lutke/Shopify** (Sep 18, 2025) — AI-driven org transformation
4. **Acquired: Alphabet Inc.** (Aug 26, 2025) — Corporate structure analysis

### Carryover from previous sessions
- Deep-scan: BG2 Pod Satya/Sam Halloween ep, Kevin Weil ep
- Deep-scan: Cheeky Pint Greg Brockman, Des Traynor, Kyle Vogt

### Still unscanned
- All Tier 2 podcasts
- All Tier 2.5 podcasts (Agents of Scale, AI CEO, etc.)
- All reports (BCG AI Radar, OpenAI Enterprise, Deloitte Tech Trends)
- SEC filings / earnings calls

### Follow-ups needed
- Google: deeper transcript read for post-ChatGPT org changes and Brain/DeepMind merger mechanics
- SSI: headcount and internal structure details
- Citigroup: AI org structure specifics
- Sierra AI: team composition and internal structure
- Microsoft MAI vs. OpenAI relationship org chart
