# App State: Ambidexterity Field Guide

## Last Updated: February 13, 2026

---

## How This Document Works

- **Read at session start** (via CLAUDE.md instructions) to understand current state
- **Updated at session end** — add a row to `SESSION_LOG.md` with date and what changed
- For software architecture details, see `SW_ARCHITECTURE.md`
- For product/research spec, see `Ambidexterity_Field_Guide_Spec.md`
- For UI design spec, see `UI_Spec.md`

---

## Site Prototype Status

The reference site is a working Next.js prototype in `site/`. It implements UI Spec Phases 1-3 (Core Browse, Interactive Exploration, Situation Matcher) plus a Claude API conversational matcher, a cross-cutting field insights page, and a full Purpose Claims browser with spider/radar chart visualizations. Inline citation system (`[source-id]` markers) provides fact-level auditability on specimen pages. No deployment yet — runs locally via `npm run dev`. Version controlled via git (initialized 2026-02-01).

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
| `/insights` | `app/insights/page.tsx` | Cross-cutting field insights grouped by theme | Working |
| `/tensions` | `app/tensions/page.tsx` | `TensionMap` + enriched tension cards (drivers, contingencies, model clustering, interpretive notes) | Working |
| `/matcher` | `app/matcher/page.tsx` | `MatcherForm` — 5-dimension matching with transparent scoring | Working |
| `/compare` | `app/compare/page.tsx` | `ComparisonView` — side-by-side up to 4 | Working |
| `/about` | `app/about/page.tsx` | Methodology, taxonomy reference, academic foundation | Working |
| `/purpose-claims` | `app/purpose-claims/page.tsx` | `PurposeClaimsBrowser` — 4 view modes (By Specimen, By Type, Profiles/Spider Grid, Dot Map), enrichment display, starred claims | Working |
| `/field-journal/[id]` | `app/field-journal/[id]/page.tsx` | Scan narrative viewer for enrichment scan journals | Working |
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
│   ├── OverviewTab.tsx         # Description, quotes, markers, contingencies (uses CitedText for auditability)
│   ├── PurposeClaimsTab.tsx    # Purpose claims + enrichment display (EnrichmentSummary with spider chart)
│   ├── MechanismsTab.tsx       # Linked mechanisms
│   ├── EvolutionTab.tsx        # Stratigraphic layers
│   ├── SourcesTab.tsx          # Source citations
│   ├── RelatedTab.tsx          # Related specimens (scored)
│   └── EnrichmentSummary.tsx   # Client: spider chart, key findings, rhetorical patterns, collapsible notes
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
├── purpose-claims/
│   ├── PurposeClaimsBrowser.tsx # Client: 4-mode browser (specimen, type, spider grid, dot map)
│   ├── ClaimsSpiderGrid.tsx    # Client: grouped spider small multiples (replaces heatmap)
│   ├── ClaimsHeatmap.tsx       # DEPRECATED: no longer imported, kept for reference
│   ├── claim-constants.ts      # Claim type colors, labels, order, SpecimenInfo interface
│   └── ...                     # Additional claim browser components
├── visualizations/
│   ├── TensionMap.tsx          # Client: D3 force simulation
│   ├── EvolutionTimeline.tsx   # Client: D3/SVG timeline
│   └── SpiderChart.tsx         # Client: reusable radar/spider chart (pure React SVG, 6 axes)
├── motion/
│   ├── AnimatedList.tsx        # Framer Motion list wrapper
│   └── AnimatedCard.tsx        # Framer Motion card wrapper
└── shared/
    ├── ClassificationBadge.tsx # Model/orientation badges
    ├── QuoteBlock.tsx          # Styled quote with attribution
    ├── SourceCitation.tsx      # Source with dates and link
    └── CitedText.tsx           # Inline [source-id] citations as superscript numbered links
```

### Data Layer

```
site/lib/
├── types/
│   ├── specimen.ts         # Full specimen type hierarchy
│   ├── taxonomy.ts         # STRUCTURAL_MODELS, SUB_TYPES, ORIENTATIONS constants
│   ├── synthesis.ts        # Mechanism, Tension, Contingency, Insight types (incl. InsightMaturity lifecycle)
│   └── purpose-claims.ts   # PurposeClaim, ClaimType, SpecimenEnrichment types
├── data/
│   ├── specimens.ts        # File-based: reads ../specimens/*.json
│   │   ├── getAllSpecimens()
│   │   ├── getSpecimenById(id)
│   │   ├── getSpecimenIds()        # For generateStaticParams
│   │   ├── getComputedStats()      # Aggregate counts
│   │   └── getSpecimensByTaxonomy() # 7x3 matrix grouping
│   ├── synthesis.ts        # File-based: reads ../synthesis/*.json
│   │   ├── getMechanisms()
│   │   ├── getTensions()
│   │   ├── getContingencies()
│   │   └── getInsights()
│   └── purpose-claims.ts   # File-based: reads ../research/purpose-claims/
│       ├── getAllPurposeClaims()
│       ├── getSpecimenEnrichment(id)   # Single enrichment file
│       └── getAllEnrichments()          # All enrichment files
├── utils/
│   ├── citations.ts        # Parses [source-id] markers → ParsedSegment[]
│   └── spider-data.ts      # normalizeDistribution(), rawProportions(), averageDistributions()
├── matching.ts             # Situation matcher scoring algorithm
└── utils.ts                # cn() helper (clsx + tailwind-merge)
```

**Data source**: JSON files in `../specimens/` and `../synthesis/` read at build/request time via Node fs. No database. Excludes `_template.json`, `specimen-schema.json`, `registry.json`, `source-registry.json`.

**Related specimen scoring**: Same model (+3), same orientation (+2), shared mechanisms (+2 each), same industry (+1). Returns top 12.

**Matcher scoring**: Ordinal matching — exact match = 1.0, adjacent = 0.5, different = 0. Only scores dimensions the user selects.

---

## Data Infrastructure Status

### Specimens: ~99 structured (149 in registry including stubs)

| Structural Model | Count | Type Specimen |
|-----------------|-------|---------------|
| Model 1: Research Lab | 7 | Google DeepMind |
| Model 2: Center of Excellence | 25 | — |
| Model 3: Embedded Teams | 16 | — |
| Model 4: Hub-and-Spoke | 48 | Novo Nordisk |
| Model 5: Product/Venture Lab | 16 | Google X (5b), Samsung C-Lab (5a) |
| Model 6: Unnamed/Informal | 28 | P&G (ChatPG), Bank of America |
| Model 7: Tiger Teams | 0 | — (no confirmed specimens after taxonomy audit) |
| Model 8: Skunkworks (Emerging) | 0 | — (predicted model, no confirmed specimens) |
| Model 9: AI-Native | 9 | — (born-AI organizations, no legacy to transform) |

**Orientation distribution**: 98 Structural, 45 Contextual, 4 Temporal (M9 AI-Native: 8 Structural, 1 Contextual)

**AI-native specimens**: 10 tagged (harvey-ai, mercor, sierra-ai, glean, ssi, ami-labs, thinking-machines-lab, world-labs, databricks, snowflake)

### Synthesis Data

- 9 confirmed mechanisms + 14 candidates (`synthesis/mechanisms.json`)
- 65 cross-cutting field insights (`synthesis/insights.json`)
- 5 core tensions (`synthesis/tensions.json`)
- 6 key contingencies (`synthesis/contingencies.json`)

### Purpose Claims Data

- **1,384 purpose claims** across ~72 scanned specimens (v2.0 taxonomy: 6 types)
- **108 enrichment files** in `research/purpose-claims/enrichment/` with rhetorical profiles (claimTypeDistribution, keyFindings, rhetoricalPatterns)
- **Visual analytics**: Spider/radar charts on specimen pages and purpose claims browser (Profiles view)
- **Citation system**: `[source-id]` inline markers → `CitedText.tsx` superscript links. **30 High-completeness specimens** backfilled with citations across all observable markers.

### Source Registry

45 sources tracked (19 Tier 1, 26 Tier 2) in `specimens/source-registry.json`

### Validation

`node scripts/validate-workflow.js` — 0 errors, 67 warnings (mostly null URLs from legacy data)

### Classification Guardrails

8 guardrails embedded in curation protocol (`curation/CURATION-PROTOCOL.md`) to prevent common misclassifications (M7 trap, M1 trap, prestige bias, AI-native scope, M4 permissiveness, etc.)

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
- Many sources with null URLs across specimens (see validator warnings for count; legacy data)
- Legacy cases in `library/cases/` not yet converted
- ~23 specimens remaining for interactive placement (Batches 8-9)
- Low-confidence specimens: see `research/low-confidence-queue.json`
- **Citation backfill**: ✅ 30 High-completeness specimens now have `[source-id]` markers. Remaining specimens (Medium/Low completeness) can be backfilled as they're enriched.
- **Purpose claims coverage**: ~51 of ~93 structured specimens scanned. More scanning needed for spider grid to show meaningful cross-specimen patterns.

---

## Pipeline Status

### Research (Phase 1)
- 16+ sessions completed (in `research/sessions/`)
- **10 Group A files in `research/pending/`** — processed research agent outputs retained for reference (deep-scans, earnings, podcasts, sweeps). 70 Group B curation artifacts archived to `research/pending/archived-curation-artifacts/`.
- **37 target specimens** in `research/target-specimens.json` for systematic sector coverage
- **Overnight automation**: `scripts/overnight-research.py` ready for unattended runs
- **Field signals**: 37 tracked in `research/field-signals.json` (7 added Session 15c from podcast sweep)
- Deep-scan backlog: 4 HIGH, 5 MEDIUM priority podcast episodes
- Low-confidence queue: 2 specimens (roche-genentech M3, lg-electronics M2) in `research/low-confidence-queue.json`

### Curation (Phase 2)
- 14 sessions completed (in `curation/sessions/`)
- 6 specimens pending synthesis (enriched in Session 16)
- First parallel curation session completed 2026-02-04 (4 agents, overlap protocol)

### Synthesis (Phase 3) — Interactive Botanist Mode
- **Automated `/synthesize` and `overnight-synthesis.py` DEPRECATED** — synthesis requires interactive collaboration (Sessions 11-12 proved this)
- 104 specimens placed in tensions + contingencies across 7 interactive batches (Sessions 11-14, 18)
- ~23 specimens remaining across Batches 8-9 (see `HANDOFF.md` for batch breakdown with analytical questions)
- `modularity-predicts-ai-structure` and `two-dimensions-of-tacit-information` hypotheses in insights.json
- Scoring guides, discovery protocol, and stub policy documented in `WORKFLOW.md` Phase 3

---

## Key File Locations

```
orgtransformation/
├── CLAUDE.md                            # Session bootstrap (auto-read by Claude Code)
├── APP_STATE.md                         # THIS FILE — current project state
├── SESSION_LOG.md                       # Full session history — update at end of each session
├── SW_ARCHITECTURE.md                   # Software architecture for the site
├── Ambidexterity_Field_Guide_Spec.md    # Product spec (v1.2)
├── UI_Spec.md                           # UI/UX spec (design source of truth)
├── HANDOFF.md                           # SUPERSEDED by CLAUDE.md + APP_STATE.md
├── site/                                # Next.js prototype
│   ├── app/                             # Routes
│   ├── components/                      # React components
│   └── lib/                             # Types, data access, utils
├── specimens/*.json                     # Specimen files (see registry.json for count)
├── synthesis/                           # Mechanisms, tensions, contingencies
├── research/                            # Session logs, queue
├── curation/                            # Session logs, synthesis queue
├── research/target-specimens.json        # Sector coverage targets (AI Exposure × Output Type)
└── scripts/                             # validate-workflow.js, overnight-*.py
```

---

## Session Log

See **`SESSION_LOG.md`** for full session history (57 entries, Feb 1–13, 2026). Updated at end of each session per the Session End Protocol in `CLAUDE.md`.
