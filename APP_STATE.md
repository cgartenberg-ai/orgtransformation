# App State: Ambidexterity Field Guide

## Last Updated: February 2, 2026

---

## How This Document Works

- **Read at session start** (via CLAUDE.md instructions) to understand current state
- **Updated at session end** — add a row to the Session Log with date and what changed
- For software architecture details, see `SW_ARCHITECTURE.md`
- For product/research spec, see `Ambidexterity_Field_Guide_Spec.md`
- For UI design spec, see `UI_Spec.md`

---

## Site Prototype Status

The reference site is a working Next.js prototype in `site/`. It implements UI Spec Phases 1-3 (Core Browse, Interactive Exploration, Situation Matcher) plus a Claude API conversational matcher. No deployment yet — runs locally via `npm run dev`. Version controlled via git (initialized 2026-02-01). Taxonomy detail pages (model/orientation) with clickable tags added in taxonomy audit sprint.

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
| `/taxonomy` | `app/taxonomy/page.tsx` | `TaxonomyMatrix` — interactive 7x3 grid | Working |
| `/taxonomy/model/[id]` | `app/taxonomy/model/[id]/page.tsx` | Model detail with description, specimens, stats | Working |
| `/taxonomy/orientation/[id]` | `app/taxonomy/orientation/[id]/page.tsx` | Orientation detail with specimens, stats | Working |
| `/mechanisms` | `app/mechanisms/page.tsx` | Confirmed + candidate mechanisms list | Working |
| `/mechanisms/[id]` | `app/mechanisms/[id]/page.tsx` | Individual mechanism with linked specimens | Working |
| `/tensions` | `app/tensions/page.tsx` | `TensionMap` — D3 force-directed scatter | Working |
| `/matcher` | `app/matcher/page.tsx` | `MatcherForm` — 5-dimension matching with transparent scoring | Working |
| `/compare` | `app/compare/page.tsx` | `ComparisonView` — side-by-side up to 4 | Working |
| `/about` | `app/about/page.tsx` | Methodology, taxonomy reference, academic foundation | Working |
| `/api/chat` | `app/api/chat/route.ts` | Streaming Claude API endpoint for chat matcher | Working |

### Component Inventory

```
site/components/
├── layout/
│   ├── SiteHeader.tsx          # Nav bar with 7 links
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
│   └── synthesis.ts        # Mechanism, Tension, Contingency types
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
│       └── getContingencies()
├── matching.ts             # Situation matcher scoring algorithm
└── utils.ts                # cn() helper (clsx + tailwind-merge)
```

**Data source**: JSON files in `../specimens/` and `../synthesis/` read at build/request time via Node fs. No database. Excludes `_template.json`, `specimen-schema.json`, `registry.json`, `source-registry.json`.

**Related specimen scoring**: Same model (+3), same orientation (+2), shared mechanisms (+2 each), same industry (+1). Returns top 12.

**Matcher scoring**: Ordinal matching — exact match = 1.0, adjacent = 0.5, different = 0. Only scores dimensions the user selects.

---

## Data Infrastructure Status

### Specimens: 85 structured

| Structural Model | Count | Type Specimen |
|-----------------|-------|---------------|
| Model 1: Research Lab | 9 | Google DeepMind |
| Model 2: Center of Excellence | 17 | — |
| Model 3: Embedded Teams | 10 | — |
| Model 4: Hub-and-Spoke | 24 | Novo Nordisk |
| Model 5: Product/Venture Lab | 12 | Google X (5b), Samsung C-Lab (5a) |
| Model 6: Unnamed/Informal | 13 | P&G (ChatPG), Bank of America |
| Model 7: Tiger Teams | 0 | — (no confirmed specimens after taxonomy audit) |
| Model 8: Skunkworks (Emerging) | 0 | — (predicted model, no confirmed specimens) |

**Orientation distribution**: 60 Structural, 24 Contextual, 1 Temporal

**AI-native specimens**: 10 tagged (harvey-ai, mercor, sierra-ai, glean, ssi, ami-labs, thinking-machines-lab, world-labs, databricks, snowflake)

### Synthesis Data

- 12 confirmed mechanisms + 5 candidates (`synthesis/mechanisms.json`)
- 5 core tensions (`synthesis/tensions.json`)
- 5 key contingencies (`synthesis/contingencies.json`)

### Source Registry

41 sources tracked (18 Tier 1, 23 Tier 2) in `specimens/source-registry.json`

### Validation

`node scripts/validate-workflow.js` — 0 errors, 60 warnings (mostly null URLs from legacy data)

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
- Pipeline fully caught up as of 2026-02-02 (all research curated, all specimens synthesized)
- Low-confidence specimens: roche-genentech (M3, Low) and lg-electronics (M2) need deeper evidence

---

## Pipeline Status

### Research (Phase 1)
- 12 sessions completed (in `research/sessions/`)
- All sessions curated — no pending items in `research/queue.json`
- Deep-scan backlog: 4 HIGH, 5 MEDIUM priority podcast episodes
- Low-confidence queue: 2 specimens (roche-genentech M3, lg-electronics M2) in `research/low-confidence-queue.json`

### Curation (Phase 2)
- 11 sessions completed (in `curation/sessions/`)
- All research sessions processed

### Synthesis (Phase 3)
- 5 sessions completed (in `synthesis/sessions/`)
- 110 specimens in synthesis queue, all synthesized — no pending items
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
├── specimens/*.json                     # 85 specimen files
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
