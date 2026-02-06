# App State: Ambidexterity Field Guide

## Last Updated: February 6, 2026

---

## How This Document Works

- **Read at session start** (via CLAUDE.md instructions) to understand current state
- **Updated at session end** — add a row to the Session Log with date and what changed
- For software architecture details, see `SW_ARCHITECTURE.md`
- For product/research spec, see `Ambidexterity_Field_Guide_Spec.md`
- For UI design spec, see `UI_Spec.md`

---

## Site Prototype Status

The reference site is a working Next.js prototype in `site/`. It implements UI Spec Phases 1-3 (Core Browse, Interactive Exploration, Situation Matcher) plus a Claude API conversational matcher and a cross-cutting field insights page. No deployment yet — runs locally via `npm run dev`. Version controlled via git (initialized 2026-02-01). Taxonomy detail pages (model/orientation) with clickable tags added in taxonomy audit sprint.

### Tech Stack (Implemented)

- **Next.js 14.2.35** — App Router, React Server Components, static generation
- **React 18** with TypeScript 5 (strict mode)
- **Tailwind CSS 3.4.1** — Custom botanical palette (forest/cream/amber/sage/charcoal)
- **shadcn/ui** — Component primitives
- **Framer Motion 12.29.2** — Card animations, page transitions, list filtering
- **D3.js 7.9.0** — Tension map force simulation, evolution timeline
- **Fonts**: Fraunces (serif headings) + Inter (body) via next/font

### Routes Implemented

| Route | Page Component | Key Components | Status |
|-------|---------------|----------------|--------|
| `/` | `app/page.tsx` | Stats, featured specimens, orientation breakdown | Working |
| `/specimens` | `app/specimens/page.tsx` | `SpecimenBrowser` — filter by model, orientation, industry, completeness; text search | Working |
| `/specimens/[id]` | `app/specimens/[id]/page.tsx` | 5 tabs: `OverviewTab`, `MechanismsTab`, `EvolutionTab`, `SourcesTab`, `RelatedTab` | Working |
| `/taxonomy` | `app/taxonomy/page.tsx` | `TaxonomyMatrix`, `ModelAccordion`, `OrientationAccordion` — matrix + accordion sections with insights | Working |
| `/taxonomy/model/[id]` | `app/taxonomy/model/[id]/page.tsx` | Model detail with description, specimens, common principles | Working |
| `/taxonomy/orientation/[id]` | `app/taxonomy/orientation/[id]/page.tsx` | Orientation detail with specimens, common principles | Working |
| `/ai-native` | `app/ai-native/page.tsx` | AI-native org analysis: model/orientation distribution, specimen grid | Working |
| `/mechanisms` | `app/mechanisms/page.tsx` | Confirmed + candidate mechanisms list with maturity badges | Working |
| `/mechanisms/[id]` | `app/mechanisms/[id]/page.tsx` | Individual mechanism with linked specimens, scholarly anchor | Working |
| `/insights` | `app/insights/page.tsx` | 13 cross-cutting field insights grouped by theme | Working |
| `/tensions` | `app/tensions/page.tsx` | `TensionMap` + enriched tension cards (drivers, contingencies, model clustering, interpretive notes) | Working |
| `/matcher` | `app/matcher/page.tsx` | `MatcherForm` — 5-dimension matching with transparent scoring | Working |
| `/compare` | `app/compare/page.tsx` | `ComparisonView` — side-by-side up to 4 | Working |
| `/about` | `app/about/page.tsx` | Methodology, taxonomy reference, academic foundation | Working |
| `/api/chat` | `app/api/chat/route.ts` | Streaming Claude API endpoint for chat matcher | Working |

### Component Inventory

```
site/components/
├── layout/
│   ├── SiteHeader.tsx          # Nav bar with 7 links (Specimens, Taxonomy, Principles, Insights, Tensions, Compare, About)
│   └── SiteFooter.tsx          # Footer
├── specimens/
│   ├── SpecimenBrowser.tsx     # Client: filterable list with search
│   ├── SpecimenCard.tsx        # Compact card for grids/lists
│   ├── SpecimenTabs.tsx        # Client: tab navigation
│   ├── OverviewTab.tsx         # Description, quotes, markers, contingencies
│   ├── MechanismsTab.tsx       # Linked mechanisms
│   ├── EvolutionTab.tsx        # Stratigraphic layers
│   ├── SourcesTab.tsx          # Source citations
│   └── RelatedTab.tsx          # Related specimens (scored)
├── home/
│   └── FieldObservation.tsx    # Client: random rotating quote from mechanisms
├── mechanisms/
│   └── MechanismChip.tsx       # Clickable mechanism badge
├── matcher/
│   ├── ChatMatcher.tsx         # Client: Claude API streaming chat advisor
│   ├── MatcherTabs.tsx         # Tab toggle (Chat Advisor / Quick Match)
│   └── MatcherForm.tsx         # Client: dimension-based situation matcher
├── taxonomy/
│   ├── TaxonomyMatrix.tsx      # Client: interactive 7x3 matrix
│   ├── ModelAccordion.tsx      # Client: expandable model section with mechanisms
│   ├── OrientationAccordion.tsx # Client: expandable orientation section with mechanisms
│   ├── ModelDetailPage.tsx     # Individual model detail with specimens
│   └── OrientationDetailPage.tsx # Individual orientation detail with specimens
├── compare/
│   └── ComparisonView.tsx      # Client: side-by-side comparison
├── visualizations/
│   ├── TensionMap.tsx          # Client: D3 force simulation
│   └── EvolutionTimeline.tsx   # Client: D3/SVG timeline
├── motion/
│   ├── AnimatedList.tsx        # Framer Motion list wrapper
│   └── AnimatedCard.tsx        # Framer Motion card wrapper
└── shared/
    ├── ClassificationBadge.tsx # Model/orientation badges
    ├── QuoteBlock.tsx          # Styled quote with attribution
    └── SourceCitation.tsx      # Source with dates and link
```

### Data Layer

```
site/lib/
├── types/
│   ├── specimen.ts         # Full specimen type hierarchy
│   ├── taxonomy.ts         # STRUCTURAL_MODELS, SUB_TYPES, ORIENTATIONS constants
│   └── synthesis.ts        # Mechanism, Tension, Contingency, Insight types (incl. InsightMaturity lifecycle)
├── data/
│   ├── specimens.ts        # File-based: reads ../specimens/*.json
│   │   ├── getAllSpecimens()
│   │   ├── getSpecimenById(id)
│   │   ├── getSpecimenIds()        # For generateStaticParams
│   │   ├── getComputedStats()      # Aggregate counts
│   │   └── getSpecimensByTaxonomy() # 7x3 matrix grouping
│   └── synthesis.ts        # File-based: reads ../synthesis/*.json
│       ├── getMechanisms()
│       ├── getTensions()
│       ├── getContingencies()
│       └── getInsights()
├── matching.ts             # Situation matcher scoring algorithm
└── utils.ts                # cn() helper (clsx + tailwind-merge)
```

**Data source**: JSON files in `../specimens/` and `../synthesis/` read at build/request time via Node fs. No database. Excludes `_template.json`, `specimen-schema.json`, `registry.json`, `source-registry.json`.

**Related specimen scoring**: Same model (+3), same orientation (+2), shared mechanisms (+2 each), same industry (+1). Returns top 12.

**Matcher scoring**: Ordinal matching — exact match = 1.0, adjacent = 0.5, different = 0. Only scores dimensions the user selects.

---

## Data Infrastructure Status

### Specimens: 93 structured

| Structural Model | Count | Type Specimen |
|-----------------|-------|---------------|
| Model 1: Research Lab | 6 | Google DeepMind |
| Model 2: Center of Excellence | 17 | — |
| Model 3: Embedded Teams | 9 | — |
| Model 4: Hub-and-Spoke | 28 | Novo Nordisk |
| Model 5: Product/Venture Lab | 10 | Google X (5b), Samsung C-Lab (5a) |
| Model 6: Unnamed/Informal | 14 | P&G (ChatPG), Bank of America |
| Model 7: Tiger Teams | 0 | — (no confirmed specimens after taxonomy audit) |
| Model 8: Skunkworks (Emerging) | 0 | — (predicted model, no confirmed specimens) |
| Model 9: AI-Native | 9 | — (born-AI organizations, no legacy to transform) |

**Orientation distribution**: 64 Structural, 28 Contextual, 1 Temporal (M9 AI-Native: 8 Structural, 1 Contextual)

**AI-native specimens**: 10 tagged (harvey-ai, mercor, sierra-ai, glean, ssi, ami-labs, thinking-machines-lab, world-labs, databricks, snowflake)

### Synthesis Data

- 9 confirmed mechanisms + 9 candidates (`synthesis/mechanisms.json`)
- 13 cross-cutting field insights (`synthesis/insights.json`)
- 5 core tensions (`synthesis/tensions.json`)
- 5 key contingencies (`synthesis/contingencies.json`)

### Source Registry

44 sources tracked (19 Tier 1, 25 Tier 2) in `specimens/source-registry.json`

### Validation

`node scripts/validate-workflow.js` — 0 errors, 63 warnings (mostly null URLs from legacy data)

### Classification Guardrails

7 guardrails embedded in curation protocol (`skills/ambidexterity-curation/SKILL.md`) to prevent common misclassifications (M7 trap, M1 trap, prestige bias, AI-native scope, etc.)

---

## What's NOT Built Yet

### From UI Spec Phase 4: User Features
- Authentication (Supabase Auth)
- My Herbarium (collections, notes, recently viewed)
- Save/bookmark specimens
- Export tools (citation generator, teaching case builder)

### From UI Spec Phase 5: Research Integration
- Research status dashboard
- Trigger research cycles from UI
- Source registry management UI
- What's New feed

### From UI Spec Phase 6: Polish & Scale
- Deployment (Vercel)
- Performance optimization (react-window for long lists, lazy loading)
- Accessibility audit
- Analytics
- Dark mode (Tailwind configured for it but not implemented)
- Mobile responsive refinement
- Search (Algolia or Supabase full-text — currently just client-side filter)

### Data Gaps
- 169 sources with null URLs across specimens (legacy data)
- 55 legacy cases in `library/cases/` not yet converted
- Pipeline: 19 specimens pending synthesis as of 2026-02-04 (all research curated, synthesis next)
- Low-confidence specimens: roche-genentech (M3, Low) and lg-electronics (M2) need deeper evidence

---

## Pipeline Status

### Research (Phase 1)
- 16 sessions completed (in `research/sessions/`)
- All sessions curated — 0 pending in `research/queue.json`
- **2 earnings calls pending**: Google Q4 2025 (transcript available post-Feb 4), Amazon Q4 2025 (Feb 5)
- Deep-scan backlog: 4 HIGH, 5 MEDIUM priority podcast episodes
- Low-confidence queue: 2 specimens (roche-genentech M3, lg-electronics M2) in `research/low-confidence-queue.json`

### Curation (Phase 2)
- 12 sessions completed (in `curation/sessions/`)
- All sessions curated — 0 pending
- First parallel curation session completed 2026-02-04 (4 agents, overlap protocol)

### Synthesis (Phase 3)
- 5 sessions completed (in `synthesis/sessions/`)
- **19 specimens pending synthesis** in `curation/synthesis-queue.json` — run `/synthesize` next
- 2 candidate mechanisms promoted to confirmed (#11, #12) on 2026-02-02

---

## Key File Locations

```
orgtransformation/
├── CLAUDE.md                            # Session bootstrap (auto-read by Claude Code)
├── APP_STATE.md                         # THIS FILE — update at end of each session
├── SW_ARCHITECTURE.md                   # Software architecture for the site
├── Ambidexterity_Field_Guide_Spec.md    # Product spec (v1.2)
├── UI_Spec.md                           # UI/UX spec (design source of truth)
├── HANDOFF.md                           # SUPERSEDED by CLAUDE.md + APP_STATE.md
├── site/                                # Next.js prototype
│   ├── app/                             # Routes
│   ├── components/                      # React components
│   └── lib/                             # Types, data access, utils
├── specimens/*.json                     # 93 specimen files
├── synthesis/                           # Mechanisms, tensions, contingencies
├── research/                            # Session logs, queue
├── curation/                            # Session logs, synthesis queue
└── scripts/                             # validate-workflow.js, convert-cases.js
```

---

## Session Log

| Date | What Changed |
|------|-------------|
| 2026-02-01 | Created APP_STATE.md. Site prototype reviewed — all 10 routes working, Phases 1-3 of UI Spec implemented. |
| 2026-02-01 | Created session bootstrap system: CLAUDE.md (auto-read entry point), SW_ARCHITECTURE.md (detailed site architecture), updated APP_STATE.md with cross-references. HANDOFF.md superseded. |
| 2026-02-01 | **Phase 1 Research**: Session 001 — press+podcast+report scan. Found 6 orgs (IndoStar, NTT DATA, Invent, UPS evolution, Microsoft evolution, PwC). **Phase 2 Curation**: Created 4 new specimens (IndoStar, NTT DATA, Invent, PwC), updated 2 (UPS, Microsoft). Total specimens: 84. **Phase 3 Synthesis**: Processed all 6 — updated mechanisms #5, #8, #9, #10; added Microsoft to candidate "AI-Driven Restructuring" (8 specimens); convergent delayering pattern (UPS+MSFT); Model 2 sub-types proposed. Synthesis queue: 0 pending. |
| 2026-02-01 | **Phase 1 Research**: Session 002 — first-ever scan of 6 Tier 1 press sources (WSJ, FT, Reuters, Bloomberg, The Information, LinkedIn). Found 4 orgs (UBS CAIO evolution, CBA CAIO evolution, Stagwell new, Amazon evolution). Ad agency CAIO wave documented. Deep-scan backlog consolidated. Curation queue: 4 orgs pending. |
| 2026-02-01 | **UI Sprint Planning**: Created UI_IMPROVEMENTS.md (8-item prioritized backlog from full site walkthrough). Created HOME_PAGE_REDESIGN.md (detailed design spec for home page: hero rewrite, 7 species cards, type specimen showcase, rotating field observation). Created HANDOFF_UI_SPRINT.md. Global terminology decision: "Mechanisms" → "Patterns" (UI text only, not routes/code). Fixed stale dev server 404s (restart resolved). |
| 2026-02-01 | **UI Sprint Implementation**: Home page redesign (5-section layout), terminology rename (Mechanisms→Patterns→Principles), evolution tab reframe (stratigraphic→organizational evolution), species descriptions on specimens page, Claude API conversational matcher (streaming chat with sessionStorage). 20 modified + 5 new files. |
| 2026-02-01 | **Taxonomy Audit**: Reclassified 4 specimens (Samsung C-Lab M7→M5a, Eli Lilly M1→M4, Roche-Genentech M1→M3, Intercom Temporal→Contextual). Added 7 classification guardrails to curation protocol. Added M8 Skunkworks as emerging model. Tagged 10 AI-native specimens. Created low-confidence research queue. Added clickable taxonomy tags + model/orientation detail pages. Committed as 81b4bb0. |
| 2026-02-02 | **Curation**: Processed research session 002 (UBS, Commonwealth Bank, Amazon enrichments + Stagwell new specimen). Total specimens: 85. |
| 2026-02-02 | **Synthesis**: Processed 18 pending specimens. Promoted 2 candidate mechanisms to confirmed: #11 "AI-Driven Workforce Restructuring" (8 specimens), #12 "Business Leader as AI Chief" (3 specimens). Full Stagwell analysis across all synthesis dimensions. All queues now empty (0 pending). Updated mechanisms (12 confirmed), tensions (5), contingencies (5). |
| 2026-02-02 | **Handoff Updates**: Updated Ambidexterity_Field_Guide_Spec.md (v1.2), APP_STATE.md, HANDOFF_UI_SPRINT.md (archived), HANDOFF.md for session continuity. |
| 2026-02-02 | **Visual Design Spec**: Created VISUAL_DESIGN_SPEC.md (Digital Nature Documentary direction — procedural organisms, terrain tension map, geological timeline, 3D ecosystem). Created STRUCTURAL_IMPROVEMENTS_PLAN.md for 4 near-term improvements. |
| 2026-02-02 | **4 Structural Improvements Implemented**: (1) AI-native visibility: M8 Skunkworks added to all taxonomy constants/filters/colors, new `/ai-native` page + nav link. (2) Taxonomy enrichment: ModelAccordion and OrientationAccordion components with characteristics, sub-types, type specimens, orientation distribution, related mechanisms; 3 key insight callouts on taxonomy page. (3) Mechanism-taxonomy cross-linking: computed affinity profiles for all 12 mechanisms (`scripts/compute-mechanism-affinity.js`), surfaced on mechanisms list/detail pages, model/orientation detail pages. (4) Tensions enrichment: added drivers, connected contingencies, interpretive notes to all 5 tensions; tensions page shows model clustering per pole, drivers section, linked contingencies, interpretive notes; TensionMap hover shows position value, model name, pole label. Build verified — 121 pages. |
| 2026-02-03 | **M9 AI-Native as Structural Model**: Promoted AI-Native from orgType tag to full structural model M9. Taxonomy now 9 models × 3 orientations. Reclassified 10 AI-native specimens (ami-labs, databricks, glean, harvey-ai, mercor, sierra-ai, snowflake, ssi, thinking-machines-lab, world-labs) from their previous models (M1/M3/M4/M5) to M9. Updated all type definitions, taxonomy constants, MODEL_NUMBERS, TensionMap colors, hardcoded model arrays (6 files), home page ("Nine Structural Species"), SpecimenBrowser, model detail pages, matcher prompt. Recomputed mechanism affinity profiles. Updated AI-native page to reference M9. Build verified — 122 pages. |
| 2026-02-03 | **UX Fixes & Insight System Enhancements**: (1) TensionMap bug fix: `hoveredValue.toFixed is not a function` — changed null check to `typeof === "number"`. (2) TensionMap readability: wider padding, pole labels with directional arrows outside chart, background color zones, scale markers. (3) Nav simplified: removed Matcher and AI-Native links; final nav: Specimens, Taxonomy, Principles, Insights, Tensions, Compare, About. (4) Insight improvements: cross-references on specimen detail pages, maturity lifecycle (hypothesis→emerging→confirmed), synthesis skill integration (Step 5b in protocol), research target flags on insights page. (5) Insights guardrail added to CLAUDE.md settled decisions. (6) Spec documents updated; NARRATIVE_SPEC.md created for insight-driven narrative creation workflow. |
| 2026-02-03 | **Intellectual Rigor Overhaul**: (1) Mechanism audit: demoted #2, #9, #12 to candidate; renamed #8 to "Turn Compliance Into Deployment Advantage"; split #11 into delayering mechanism + headcount candidate; added maturity lifecycle (emerging/confirmed/widespread/deprecated); result: 9 confirmed mechanisms, 9 candidates. (2) Cross-cutting insights: created synthesis/insights.json with 13 field insights; new /insights page + nav link; top 6 insights on home page. (3) Specimen schema: added secondary models to 6 multi-model specimens (accenture-openai, bcg-trailblazers, salesforce, microsoft, nvidia, jpmorgan). (4) Theoretical grounding: added scholarlyAnchor to all 9 confirmed mechanisms connecting to March, Simon, Arrow, Holmstrom, Henderson/Clark, Eisenhardt, Gibbons/Henderson; rewrote theoreticalConnection fields as crisp one-sentence summaries. Build verified — 120 pages. |
| 2026-02-03 | **Field Insight Refinements**: (1) Reframed hub-and-spoke insight: "regulated industries" → "R&D-intensive industries"; driver is specialization/local knowledge (Garicano 2000), not regulation per se; flagged that all 5 specimens are pharma so can't yet distinguish. (2) Killed isomorphism framing: restructuring insight reframed as convergent response to common technological shock (Simon), not DiMaggio & Powell mimetic isomorphism; "redundancy washing" kept as honest counter-explanation. (3) CAIO waves: replaced isomorphism with information cascades (Banerjee 1992) — rational updating under uncertainty, not blind copying. (4) Terminology: "research insights" → "field insights" across all files. (5) Added collaboration mode to CLAUDE.md: org econ identity, two-hat workflow. |
| 2026-02-03 | **Field Signal Infrastructure**: Created `research/field-signals.json` — structured registry for macro observations across research sessions. 20 signals backfilled from 9 past sessions. Updated SESSION-PROTOCOL.md + research SKILL.md to institutionalize signal tracking. Signal lifecycle: active → saturated → promoted. |
| 2026-02-03 | **3 Research Sessions**: Session 1 (podcasts/press/substacks): SK Telecom CIC, Pentagon CDAO, NY State CAIO, Meta evolution, Microsoft evolution. Session 2 (AI labs/press): Meta MSL 5th restructuring (Wang CAIO, 4-unit structure, LeCun departure), AMI Labs (LeCun venture), Pinterest 15% AI pivot cuts, Infosys 100K Cursor CoE, Anthropic IPO prep ($350B, LTBT governance). Session 3 (earnings calls): Microsoft (-$375B correction, $37.5B CapEx, 15M Copilot seats), Meta ($115-135B 2026 CapEx, "single talented person" replaces teams), Amazon (30K cuts, Jassy contradiction), Salesforce (Agentforce $500M ARR, 84% resolution, 4K redeployed), Google (Gemini 650M MAU, Cloud $155B backlog). Earnings calls elevated to Tier 1. CIO Dive added as source. Total: 44 sources (19 Tier 1, 25 Tier 2). 22 field signals tracked. 3 sessions pending curation. |
| 2026-02-03 | **Earnings Season Protocol**: Built structured earnings call research infrastructure. Created `research/earnings-calendar.json` with 15 target companies (fiscal year mappings, priorities, scan history, keyword protocol). Updated SESSION-PROTOCOL.md with full Earnings Season Protocol section (per-company scan process, keyword categories, why earnings are special). Added `earnings` session type. Google Q4 (Feb 4) and Amazon Q4 (Feb 5) pending. |
| 2026-02-04 | **Earnings Wide-Net Research Session**: First dedicated earnings discovery session using new protocol. Found 7 orgs: Travelers (TravAI agentic AI, 20K users, 30% handle time reduction — insurance structural goldmine), ServiceNow (AI Control Tower, $600M Now Assist, McDermott "obliterate org charts"), Accenture ($865M restructuring, 11K layoffs, "exiting non-reskillable"), Nokia (Defense incubation unit — M8 candidate, €750M restructuring), Workday (1,750 layoffs — AI-washing data point), Publicis (CoreAI, 73% AI-powered), RWJBarnabas Health (healthcare AI CoE, 14 hospitals). Google Q4 and Amazon Q4 transcripts pending (calls today/tomorrow). Added Travelers + ServiceNow to earnings calendar. 2 new field signals (insurance-as-goldmine, agentic-as-restructuring-tool). 25 total field signals. 4 sessions pending curation (23 orgs total). |
| 2026-02-04 | **Parallel Curation of 4 Research Sessions**: First parallel curation session — 4 background agents curated 4 research sessions simultaneously. Updated curation protocol with "Parallel Curation with Overlapping Specimens" section. Created `scripts/rebuild-registry.js`. **8 new specimens**: sk-telecom (M5), pentagon-cdao (M4), new-york-state (M2), travelers (M4), servicenow (M4), nokia (M4), workday (M6a Stub), rwjbarnabas-health (M2 Stub — first healthcare system specimen). **12 specimens updated**: meta-ai (major evolution: MSL 4-unit structure, 7 layers, 28 sources, completeness→High), microsoft, ami-labs, pinterest, infosys, anthropic, amazon-agi, google-deepmind, salesforce, accenture-openai (reclassified M2→M4), publicis-groupe (reclassified M2→M4), eli-lilly (confirmed current). **Total specimens: 93** (was 85). 19 specimens pending synthesis. Validator: 0 errors, 63 warnings. |
| 2026-02-04 | **Batched Synthesis (19 specimens)**: Manual 3-batch synthesis to avoid `/synthesize` skill context overflow. Batch 1 (meta-ai, travelers, servicenow, accenture-openai, publicis-groupe, nokia): M11 promoted to confirmed (6 specimens); added Nokia to M1, ServiceNow to M10, Accenture to candidate. Batch 2 (sk-telecom, pentagon-cdao, microsoft, amazon-agi, google-deepmind, salesforce): added SK Telecom + Pentagon CDAO to M6 (now 7 specimens); consolidation pattern extends beyond Big Tech. Batch 3 (anthropic, ami-labs, pinterest, infosys, new-york-state, workday, rwjbarnabas-health): government CAIO wave documented. **Insight promotions**: `regulation-expensive-not-slow` emerging→confirmed (Travelers); `entry-level-talent-hollow` emerging→confirmed (Accenture); `meta-exploration-failure` hypothesis→emerging. **Insight updates**: management-delayering +3, ai-restructuring +4, ai-team-consolidation +2, caio-waves +2, consulting-dual-identity +1. All 19 specimens placed in tensions + contingencies. Synthesis queue: 0 pending. |
| 2026-02-03 | **Travelers Reclassified M4→M2**: TravAI is a central platform with business units as consumers (unidirectional enablement). No evidence of spoke-level AI development capacity — CoE, not hub-and-spoke. Confidence downgraded High→Medium. M4 count drops by 1 (to 27), M2 gains 1 (to 18). Synthesis files not yet updated for reclassification. |
| 2026-02-03 | **Purpose Claims Skill**: Created `/purpose-claims` skill for systematically searching for verbatim purpose claims by leaders at specimen organizations, made in the context of AI adaptation. 6 claim types: utopian, identity, transformation-framing, employee-deal, sacrifice-justification, direction-under-uncertainty. Created: `.claude/skills/purpose-claims/SKILL.md` (full protocol with same source registry as `/research`), `research/purpose-claims/registry.json` (empty, with schema), `research/purpose-claims/scan-tracker.json` (93 specimens, all unscanned), `research/purpose-claims/sessions/` (empty). Quality filters: verbatim-only, AI-adaptation context required, source URL required. Serves the purpose × AI transformation paper. |
| 2026-02-03 | **Literature Matching System**: Created LITERATURE_SPEC.md — full spec for connecting field observations to scholarly conversation. Design principle: loose coupling (literature analysis decoupled from fieldwork pipeline to prevent confirmation bias). Three research modes: broad sweeps (default), low-confidence targets (existing), literature gap targets (new). Registry schema with `keyMechanism`, `predictionForAI`, relationship types (confirms/extends/boundary-condition/contradicts). Created `research/literature/registry.json` with 17 core canon entries (Garicano, March, Simon, Arrow, Holmstrom, Aghion & Tirole, Gibbons & Henderson, Henderson & Clark, Teece, Christensen, O'Reilly & Tushman, Gibson & Birkinshaw, North, Banerjee, Becker, Dessein, Alonso Dessein & Matouschek). Created `research/literature-gaps-queue.json` stub. Added LITERATURE_SPEC.md to CLAUDE.md Required Reading. |
| 2026-02-03 | **Purpose Claims Batch 1 + Transcript Gap Protocol**: Scanned 7 specimens for purpose claims using parallel background agents. Results: Meta 11 (pilot), Microsoft 15 (7 web + 8 transcript), Anthropic 14 (transcript-only — the motherlode), Eli Lilly 7 (0 web → 7 transcript — proved transcript gap is real), Shopify 5, Amazon 5, ServiceNow 2. **59 total claims** in registry across 7 specimens. Claim type distribution: identity 29%, direction-under-uncertainty 20%, employee-deal 19%, transformation-framing 12%, utopian 10%, sacrifice-justification 10%. **Transcript gap discovery**: web search systematically underrepresents identity and direction-under-uncertainty claims. Eli Lilly went 0→7 with transcript access. **Protocol updates**: Added `transcriptsAvailable: true` to 7 podcast sources in source-registry.json (Cheeky Pint, Dwarkesh, Latent Space, Acquired, Conversations with Tyler, Lex Fridman, Cognitive Revolution). Updated SKILL.md with 7-source transcript list + deep-scan guidance. Updated SESSION-PROTOCOL.md with transcript check step. Created `research/transcript-gap-queue.json` with 10 known specimen×transcript pairs. Added "north star" to standard search queries (only Zuckerberg uses it — not convergent). Updated analytical-notes.md with 9 patterns, 4 hypotheses. |
| 2026-02-06 | **Purpose Claims Spec + Transcript Discovery Protocol**: (1) Created `research/purpose-claims/PURPOSE-CLAIMS-SPEC.md` — comprehensive data layer spec. 7-type taxonomy (added `teleological` for Dario/Demis-style outcome-anchored claims). Taxonomy evolution protocol (flag edge cases → quarterly review → revise when 5+ share fit problem). Claim schema with new fields: secondaryType, taxonomyFlag, transcriptSource, rhetoricalFunction. Updated registry.json with taxonomyVersion 1.0. (2) Designed + implemented Transcript Discovery Protocol: `research/transcript-sources.json` (13 seed sources: 7 podcasts, 2 earnings, 1 congressional, 3 YouTube manual-required). Expanded `research/transcript-gap-queue.json` schema (10 entries migrated to new format with sourceId, leaderTitle, transcriptQuality, transcriptAccess, aiRelevance, status, discoveredDate, scannedDate). Created `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` (Phase 1 quick sweep + Phase 2 deep discovery). Updated SESSION-PROTOCOL.md with Step 2b. Updated both /research and /purpose-claims skills to reference protocol. 7 commits. |
| 2026-02-04 | **Purpose Claims Batch 2**: Scanned 4 specimens via foreground serial scans (background agents failed due to web permission issue — `run_in_background: true` blocks WebSearch/WebFetch). Results: Accenture 8 (Sweet: reskill-or-exit, five decades of change, courage+humility, North Star), Salesforce 10 (Benioff: digital labor revolution, last generation of CEOs, "I need less heads," Benioff Contradiction), Klarna 7 (Siemiatkowski: REVERSAL CASE — cost over quality admission, "my tech bros" anti-utopian, Brussels translator), SK Telecom 5 (Ryu: golden era, leap into AI company, CEO succession register shift). **89 total claims** in registry across 11 specimens. 5 new patterns: #10 purpose claims are context-dependent performance (Benioff podcast vs. interview), #11 reversal case (Klarna), #12 anti-utopian register (Sweet+Siemiatkowski), #13 North Star update (Sweet uses it too), #14 CEO succession changes rhetorical register (SK Telecom). New hypothesis H5: podcast contexts elicit more honest purpose claims. Updated SKILL.md with stronger agent prompt template (mandatory web search). |
