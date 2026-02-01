# App State: Ambidexterity Field Guide

## Last Updated: February 1, 2026

---

## How This Document Works

- **Read at session start** (via CLAUDE.md instructions) to understand current state
- **Updated at session end** — add a row to the Session Log with date and what changed
- For software architecture details, see `SW_ARCHITECTURE.md`
- For product/research spec, see `Ambidexterity_Field_Guide_Spec.md`
- For UI design spec, see `UI_Spec.md`

---

## Site Prototype Status

The reference site is a working Next.js prototype in `site/`. It implements UI Spec Phases 1-3 (Core Browse, Interactive Exploration, Situation Matcher). No deployment yet — runs locally via `npm run dev`. Version controlled via git (initialized 2026-02-01).

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
| `/mechanisms` | `app/mechanisms/page.tsx` | Confirmed + candidate mechanisms list | Working |
| `/mechanisms/[id]` | `app/mechanisms/[id]/page.tsx` | Individual mechanism with linked specimens | Working |
| `/tensions` | `app/tensions/page.tsx` | `TensionMap` — D3 force-directed scatter | Working |
| `/matcher` | `app/matcher/page.tsx` | `MatcherForm` — 5-dimension matching with transparent scoring | Working |
| `/compare` | `app/compare/page.tsx` | `ComparisonView` — side-by-side up to 4 | Working |
| `/about` | `app/about/page.tsx` | Methodology, taxonomy reference, academic foundation | Working |

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
├── mechanisms/
│   └── MechanismChip.tsx       # Clickable mechanism badge
├── matcher/
│   └── MatcherForm.tsx         # Client: situation matcher interface
├── taxonomy/
│   └── TaxonomyMatrix.tsx      # Client: interactive 7x3 matrix
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

### Specimens: 84 structured

| Structural Model | Count | Type Specimen |
|-----------------|-------|---------------|
| Model 1: Research Lab | 11 | Eli Lilly |
| Model 2: Center of Excellence | 16 | — |
| Model 3: Embedded Teams | 9 | — |
| Model 4: Hub-and-Spoke | 23 | — |
| Model 5: Product/Venture Lab | 11 | Google X |
| Model 6: Unnamed/Informal | 13 | P&G, Bank of America |
| Model 7: Tiger Teams | 1 | Samsung C-Lab |

**Orientation distribution**: 59 Structural, 23 Contextual, 2 Temporal

### Synthesis Data

- 10 confirmed mechanisms + 5 candidates (`synthesis/mechanisms.json`)
- 5 core tensions (`synthesis/tensions.json`)
- 5 key contingencies (`synthesis/contingencies.json`)

### Source Registry

38 sources tracked (18 Tier 1, 20 Tier 2) in `specimens/source-registry.json`

### Validation

`node scripts/validate-workflow.js` — 0 errors, ~67 warnings (mostly null URLs from legacy data)

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
- Sources with null URLs across specimens (legacy data)
- 55 legacy cases in `library/cases/` not yet converted
- Pipeline fully caught up as of 2026-02-01 (all research curated, all specimens synthesized)

---

## Pipeline Status

### Research (Phase 1)
- 11 sessions completed (in `research/sessions/`)
- All sessions curated — no pending items in `research/queue.json`
- Deep-scan backlog: 2 HIGH, 8 MEDIUM priority podcast episodes (see HANDOFF.md for list)

### Curation (Phase 2)
- 9 sessions completed (in `curation/sessions/`)
- All research sessions processed

### Synthesis (Phase 3)
- 3 sessions completed (in `synthesis/sessions/`)
- 74 specimens in synthesis queue, all synthesized — no pending items

---

## Key File Locations

```
orgtransformation/
├── CLAUDE.md                            # Session bootstrap (auto-read by Claude Code)
├── APP_STATE.md                         # THIS FILE — update at end of each session
├── SW_ARCHITECTURE.md                   # Software architecture for the site
├── Ambidexterity_Field_Guide_Spec.md    # Product spec (v1.1)
├── UI_Spec.md                           # UI/UX spec (design source of truth)
├── HANDOFF.md                           # SUPERSEDED by CLAUDE.md + APP_STATE.md
├── site/                                # Next.js prototype
│   ├── app/                             # Routes
│   ├── components/                      # React components
│   └── lib/                             # Types, data access, utils
├── specimens/*.json                     # 65 specimen files
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
