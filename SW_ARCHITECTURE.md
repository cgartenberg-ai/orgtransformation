# Software Architecture: Ambidexterity Field Guide Site

## Last Updated: February 14, 2026

---

## 1. System Overview

An interactive reference site for browsing organizational specimens — how companies structure AI work across exploration and execution.

**Architecture pattern:** Static-first Next.js 14 with file-based data. No database, no auth. One API route for Claude chat matcher. All data lives in JSON files read by server components at build/request time via Node `fs`.

**Data flow:**
```
JSON files (../specimens/, ../synthesis/)
  → Data access layer (lib/data/)
  → Server Components (app/**/page.tsx)
  → Client Components (components/*) for interactivity
  → Rendered UI (Tailwind + Framer Motion + D3)
```

---

## 2. Rendering Strategy

**Server Components by default.** All page files (`app/**/page.tsx`) are async server components that fetch data via `lib/data/` functions. Data is passed as props to client components.

**Client Components** (`"use client"` directive) used only when interactivity is needed:

| Component | Why Client |
|-----------|-----------|
| `SpecimenBrowser` | Filter/search state, AnimatePresence |
| `SpecimenTabs` | Tab selection state |
| `MatcherForm` | Form state, real-time scoring |
| `TaxonomyMatrix` | Click interactions, cell selection |
| `ComparisonView` | Specimen add/remove state |
| `PurposeClaimsBrowser` | Multi-view mode (heatmap/dot/spider), filter state |
| `ClaimsSpiderGrid` | Spider chart interactions, group toggle |
| `TensionMap` | D3 force simulation, hover state |
| `SpiderChart` | Pure React SVG, hover interactions |
| `EvolutionTimeline` | D3 SVG rendering, Framer Motion |
| `AnimatedList`, `AnimatedCard` | Framer Motion wrappers |

**Static generation:** `/specimens/[id]` and `/mechanisms/[id]` use `generateStaticParams()` to pre-render all detail pages at build time.

**No ISR or revalidation.** Data changes require a rebuild (`npm run build`) or dev server refresh.

---

## 3. Directory Structure

```
site/
├── app/                            # Next.js 14 App Router
│   ├── layout.tsx                  # Root: fonts (Inter, Fraunces), SiteHeader, SiteFooter, max-w-7xl
│   ├── globals.css                 # CSS variables for botanical palette (HSL)
│   ├── page.tsx                    # Home: stats, featured specimens, model distribution
│   ├── specimens/
│   │   ├── page.tsx                # Browse: SpecimenBrowser with filters + search
│   │   └── [id]/page.tsx           # Detail: 6-tab view (Overview, Mechanisms, Purpose Claims, Evolution, Sources, Related)
│   ├── taxonomy/
│   │   ├── page.tsx                # Matrix: 9x3 interactive grid with model/orientation accordions
│   │   ├── models/[id]/page.tsx    # Model detail: description, specimens, common principles
│   │   └── orientations/[id]/page.tsx # Orientation detail: specimens, common principles
│   ├── mechanisms/
│   │   ├── page.tsx                # All: confirmed + candidate mechanisms with maturity badges
│   │   └── [id]/page.tsx           # Detail: single mechanism with specimens, scholarly anchor, affinity profile
│   ├── insights/page.tsx           # Field insights grouped by theme with maturity badges
│   ├── purpose-claims/page.tsx      # Purpose claims browser: heatmap, dot map, spider grid views
│   ├── field-journal/
│   │   ├── page.tsx                # Field journal list: all synthesis sessions
│   │   └── [id]/page.tsx           # Field journal entry: single session details
│   ├── ai-native/page.tsx          # AI-native org analysis: M9 specimens, model/orientation distribution
│   ├── tensions/page.tsx           # Map: D3 force-directed scatter with enriched tension cards
│   ├── matcher/page.tsx            # Matcher: 6-dimension contingency matching + Claude chat advisor
│   ├── compare/page.tsx            # Compare: side-by-side up to 4
│   ├── about/page.tsx              # About: methodology, taxonomy reference
│   └── api/chat/route.ts           # Streaming Claude API endpoint for chat matcher
│
├── components/
│   ├── layout/
│   │   ├── SiteHeader.tsx          # Nav with links (Specimens, Taxonomy, Principles, Insights, Purpose Claims, Tensions, Field Journal, Compare, About)
│   │   └── SiteFooter.tsx          # Footer
│   ├── specimens/
│   │   ├── SpecimenBrowser.tsx     # Client: multi-filter list (model, orientation, industry, completeness) + text search
│   │   ├── SpecimenCard.tsx        # Compact card for grids
│   │   ├── SpecimenTabs.tsx        # Client: tab navigation for detail page
│   │   ├── OverviewTab.tsx         # Description, quotes, observable markers, contingency profile
│   │   ├── MechanismsTab.tsx       # Linked mechanisms with evidence
│   │   ├── EvolutionTab.tsx        # Stratigraphic layers (timeline)
│   │   ├── PurposeClaimsTab.tsx    # Purpose claims per specimen with enrichment
│   │   ├── EnrichmentSummary.tsx   # Enrichment display with spider chart
│   │   ├── SourcesTab.tsx          # Source citations table
│   │   └── RelatedTab.tsx          # Related specimens (scored by similarity)
│   ├── mechanisms/
│   │   └── MechanismChip.tsx       # Clickable mechanism badge
│   ├── matcher/
│   │   ├── ChatMatcher.tsx         # Client: Claude API streaming chat advisor
│   │   ├── MatcherTabs.tsx         # Tab toggle (Chat Advisor / Quick Match)
│   │   └── MatcherForm.tsx         # Client: 5-dimension form + ranked results
│   ├── taxonomy/
│   │   ├── TaxonomyMatrix.tsx      # Client: interactive 9x3 grid with cell click
│   │   ├── ModelAccordion.tsx      # Client: expandable model section with mechanisms
│   │   └── OrientationAccordion.tsx # Client: expandable orientation section
│   ├── compare/
│   │   └── ComparisonView.tsx      # Client: side-by-side comparison
│   ├── purpose-claims/
│   │   ├── PurposeClaimsBrowser.tsx # Client: multi-view browser (heatmap, dot map, spider grid)
│   │   ├── ClaimsHeatmap.tsx       # Client: claim type × model heatmap
│   │   ├── ClaimsDotMap.tsx        # Client: dot map per specimen
│   │   └── ClaimsSpiderGrid.tsx    # Client: spider chart small multiples grouped by model/industry
│   ├── visualizations/
│   │   ├── TensionMap.tsx          # Client: D3 force simulation on SVG
│   │   ├── SpiderChart.tsx         # Pure React SVG radar chart (6 axes, one per claim type)
│   │   └── EvolutionTimeline.tsx   # Client: D3/SVG vertical timeline with Framer Motion
│   ├── motion/
│   │   ├── AnimatedList.tsx        # Framer Motion AnimatePresence list wrapper
│   │   └── AnimatedCard.tsx        # Framer Motion hover/tap card wrapper
│   └── shared/
│       ├── ClassificationBadge.tsx # Model/sub-type/orientation badges with color coding
│       ├── CitedText.tsx           # Renders [source-id] markers as superscript numbered links
│       ├── QuoteBlock.tsx          # Styled blockquote with speaker and source
│       └── SourceCitation.tsx      # Source name, type, dates, link
│
└── lib/
    ├── types/
    │   ├── specimen.ts             # Full type hierarchy (see Section 4)
    │   ├── taxonomy.ts             # STRUCTURAL_MODELS, SUB_TYPES, ORIENTATIONS constants
    │   ├── synthesis.ts            # MechanismData, TensionData, ContingencyData, InsightData, PrimitiveData, FindingData types (incl. FrameworkStatus, FindingMaturity)
    │   └── purpose-claims.ts       # PurposeClaimsData, PurposeClaim, SpecimenEnrichment, ClaimType
    ├── data/
    │   ├── specimens.ts            # Data access: getAllSpecimens, getSpecimenById, getComputedStats, getSpecimensByTaxonomy
    │   ├── synthesis.ts            # Data access: getMechanisms, getTensions, getContingencies, getInsights, getPrimitives, getFindings
    │   └── purpose-claims.ts       # Data access: getPurposeClaims, getSpecimenEnrichment, getAllEnrichments
    ├── matcher/
    │   └── buildSystemPrompt.ts    # Builds dynamic system prompt for Claude chat matcher from live data
    ├── matching.ts                 # Situation matcher scoring algorithm
    ├── utils.ts                    # cn() — clsx + tailwind-merge helper
    └── utils/
        ├── citations.ts            # Parses [source-id] markers in text strings for CitedText
        └── spider-data.ts          # normalizeDistribution() for spider chart axis scaling
```

---

## 4. Data Model

### 4.1 Specimen (Primary Entity)

**Schema:** `lib/types/specimen.ts`
**Storage:** One JSON file per specimen in `../specimens/` (see `registry.json` for current count)

```typescript
interface Specimen {
  id: string;                           // Filename slug (e.g., "eli-lilly")
  name: string;                         // Display name
  title: string;                        // Descriptive subtitle
  classification: Classification;       // Model (1-9), sub-type, orientation, confidence, typeSpecimen flag
  habitat: Habitat;                     // Industry, sector, orgSize, employees, revenue, HQ, geography
  description: string;                  // 2-3 paragraph narrative
  observableMarkers: ObservableMarkers; // Reporting, resources, time horizons, decision rights, metrics
  mechanisms: SpecimenMechanism[];      // Which of the 9 confirmed mechanisms this org demonstrates (id, name, evidence, strength)
  quotes: Quote[];                      // Verbatim with speaker, title, source, URL, date
  layers: Layer[];                      // Stratigraphic evolution (date, summary, sourceRefs)
  sources: Source[];                    // All sources with type, URL, sourceDate, collectedDate
  contingencies: Contingencies;         // 6 dimensions: regulatory, obsolescence, CEO tenure, talent, debt, environmentalAiPull
  tensionPositions: TensionPositions;   // 5 tension scores (-1.0 to +1.0 continuous scales)
  openQuestions?: string[];             // Unresolved research questions
  taxonomyFeedback?: string[];          // Edge case notes for taxonomy refinement
  meta: SpecimenMeta;                   // Status, created, lastUpdated, completeness
}
```

**Key types:**
- `StructuralModel`: `1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9`
- `SubType`: `"5a" | "5b" | "5c" | "6a" | "6b" | "6c"`
- `Orientation`: `"Structural" | "Contextual" | "Temporal"`
- `Confidence`: `"High" | "Medium" | "Low"`
- `MechanismStrength`: `"Strong" | "Moderate" | "Emerging"`
- `Completeness`: `"High" | "Medium" | "Low"`

### 4.2 Synthesis Data

**Mechanisms** (`../synthesis/mechanisms.json`):
```typescript
interface MechanismData {
  confirmed: ConfirmedMechanism[];  // id, name, definition, problemItSolves, theoreticalConnection, scholarlyAnchor, maturity, specimens[], evidence[], affinityProfile
  candidates: CandidateMechanism[]; // name, hypothesis, evidenceNeeded, observedIn[], specimens[], demotionReason?
}
// MechanismMaturity: "emerging" | "confirmed" | "widespread" | "deprecated"
```

**Insights** (`../synthesis/insights.json`):
```typescript
interface InsightData {
  insights: Insight[];  // id, title, theme, maturity, finding, evidence[], theoreticalConnection, relatedMechanisms[], relatedTensions[]
}
// InsightMaturity: "hypothesis" | "emerging" | "confirmed"
// Themes: "convergence" | "organizational-form" | "mechanism" | "workforce" | "methodology"
// GUARDRAIL: Insights are NEVER deleted — only updated with new evidence or new insights added
```

**Tensions** (`../synthesis/tensions.json`):
```typescript
interface TensionData {
  tensions: Tension[];  // 5 tensions: id, name, fieldName (maps to TensionPositions key), tradeoff, poles (whenNegative/whenPositive), specimens[] with positions
}
```

**Contingencies** (`../synthesis/contingencies.json`):
```typescript
interface ContingencyData {
  contingencies: ContingencyDefinition[];  // 6 contingencies: id, name, whatItDetermines, high{}, low{}
}
```

### 4.3 Data Access Pattern

**`lib/data/specimens.ts`:**
- `DATA_ROOT = path.resolve(process.cwd(), "..")` — reads from parent directory
- `EXCLUDED_FILES`: `_template.json`, `specimen-schema.json`, `registry.json`, `source-registry.json`
- `getAllSpecimens()` — reads all JSON files dynamically (no hardcoded list), returns sorted by name
- `getSpecimenById(id)` — reads `../specimens/{id}.json`
- `getSpecimenIds()` — for `generateStaticParams` (all IDs from getAllSpecimens)
- `getComputedStats()` — aggregates: totalSpecimens, byModel, byOrientation, typeSpecimens, byCompleteness, byIndustry, industries list, lastUpdated
- `getSpecimensByTaxonomy()` — groups into `Record<model, Record<orientation, Specimen[]>>` (9x3 matrix)

**`lib/data/synthesis.ts`:**
- `SYNTHESIS_DIR = path.resolve(process.cwd(), "..", "synthesis")`
- `getMechanisms()`, `getTensions()`, `getContingencies()`, `getInsights()` — simple file reads with type casting; all wrapped in try/catch with console.error fallback
- `getPrimitives()` — reads `primitives.json`, returns `PrimitiveData`; try/catch with empty fallback
- `getFindings()` — reads `findings.json`, returns `FindingData`; try/catch with empty fallback
- `getInsights()` — **DEPRECATED**: now reads from `insights-archive-v1.json` (frozen archive); new analytical output is in findings

**`lib/data/purpose-claims.ts`:**
- `CLAIMS_FILE` → `../research/purpose-claims/registry.json`
- `ENRICHMENT_DIR` → `../research/purpose-claims/enrichment/`
- `getPurposeClaims()` — reads registry, returns `PurposeClaimsData`; try/catch with empty fallback
- `getSpecimenEnrichment(id)` — reads `enrichment/{id}.json`, returns `SpecimenEnrichment | null`
- `getAllEnrichments()` — reads all enrichment files for spider grid views

**No caching layer.** Per-request reads in dev mode; build-time reads for static pages.

### 4.4 Related Specimen Algorithm

Used by `RelatedTab.tsx`. Scoring:
- Same structural model: +3
- Same orientation: +2
- Shared mechanisms: +2 each
- Same industry: +1
- Returns top 12 by score

---

## 5. Matching Algorithm

**File:** `lib/matching.ts`

The Situation Matcher lets users input their organizational context and find peer specimens.

**Input:** 6 contingency dimensions (all nullable — user can select any subset):
- `regulatoryIntensity`: Low / Medium / High
- `timeToObsolescence`: Slow / Medium / Fast
- `ceoTenure`: Short / Medium / Long (Founder normalized to Long)
- `talentMarketPosition`: Talent-rich / Talent-constrained / Non-traditional
- `technicalDebt`: Low / Medium / High
- `environmentalAiPull`: Low / Medium / High

**Scoring:** Ordinal distance matching per dimension:
- Exact match = 1.0
- Adjacent on ordinal scale = 0.5 (e.g., Low vs Medium)
- Different = 0
- No data = 0
- Talent has no ordinal scale (exact match only)

**Output:** `MatchResult[]` sorted by score (0-100), each with per-dimension breakdown showing why it matched. Transparency is a design principle — no black-box scoring.

**Partial matching:** Only dimensions the user selected contribute to the score. If user selects 2 of 5 dimensions, scoring is against those 2 only.

---

## 6. D3 Visualization Architecture

### TensionMap (`components/visualizations/TensionMap.tsx`)

- **D3 force simulation** positions specimens on a horizontal axis (-1.0 to +1.0) based on tension scores from `specimen.tensionPositions`
- Dropdown selects which of 5 tensions to display (fieldName maps to TensionPositions key)
- Y-axis: force simulation with weak centering + collision avoidance
- **Simulation runs synchronously** (200 ticks on mount) — no continuous animation
- Circles colored by structural model (MODEL_COLORS map, forest/sage/amber hues)
- Model number displayed inside circle as "M1", "M2", etc. (r=13 circles)
- Name label below each circle (truncated to 14 chars)
- **Pole labels** with directional arrows (`← label` / `label →`) outside chart area at vertical center
- **Background color zones**: warm (#F8F0E8) for negative pole, cool (#E8F0E8) for positive pole
- **Scale markers** (-1, -0.5, 0, +0.5, +1) along bottom axis
- 120px padding on each side for pole labels; chart height 420px
- Hover: shows specimen preview panel below the map (uses `typeof hoveredValue === "number"` guard)
- Click: navigates to specimen detail page via Next.js Link
- Legend shows all 9 model colors
- SVG viewBox responsive, contained in `overflow-x-auto` wrapper

### EvolutionTimeline (`components/visualizations/EvolutionTimeline.tsx`)

- SVG-based vertical timeline
- Renders `specimen.layers[]` in reverse chronological order
- Each layer node: date, classification change, summary
- Connecting lines between layer nodes
- Framer Motion for reveal animations (staggered by index)
- Clickable nodes show layer detail

---

## 7. Component Patterns

### Server/Client Boundary

```
Page (Server Component)
  ├── fetches data via lib/data/* functions
  ├── renders static content directly
  └── passes data as props to:
      └── Client Component ("use client")
          ├── manages local state (filters, hover, selection)
          ├── handles user interactions
          └── renders Framer Motion / D3 visualizations
```

Pages use `Promise.all()` for parallel data fetching:
```typescript
const [specimens, stats, mechanisms] = await Promise.all([
  getAllSpecimens(),
  getComputedStats(),
  getMechanisms(),
]);
```

### Animation Patterns

**Framer Motion** (UI animations):
- `AnimatedCard`: hover scale 1.02, shadow deepens, y: -4, tap scale 0.98
- `AnimatedList`: `AnimatePresence` with `layout` prop for smooth reordering during filter
- Item enter: opacity 0 → 1, height 0 → auto
- Item exit: opacity 1 → 0, height auto → 0

**D3** (data visualizations):
- Force simulations for positioning (TensionMap)
- SVG rendering with manual DOM manipulation via `useRef` + `useEffect`
- D3 handles data binding; React handles container and state

### Styling Conventions

**Botanical palette** (Tailwind custom colors):
- `forest` (primary): `#1B4332` — headers, links, badges, nav
- `cream` (background): `#FAF3E0` — page bg, card bg
- `amber` (accent): `#D4A373` — CTAs, highlights, Model 5-7 colors
- `sage` (supporting): `#84A98C` — secondary text, borders, Model 3
- `charcoal` (text): `#2D3436` — body text, dark elements

Each color has a full scale (50-900) defined in `tailwind.config.ts`.

**Typography:**
- Headings: `font-serif` (Fraunces) — via CSS variable `--font-fraunces`
- Body: `font-sans` (Inter) — via CSS variable `--font-inter`
- Data/labels: `font-mono` for taxonomic codes (M1, M2, etc.)

**Spacing:** `space-y-*` for vertical stacking, `gap-*` for grid/flex gaps. Cards use `p-4` to `p-6`. Sections separated by `space-y-8` or `space-y-12`.

**Borders/surfaces:** `border-sage-200` for card borders, `bg-cream-50` for card surfaces, `rounded-lg` standard radius.

---

## 8. Route Architecture

| Route | Page Data Dependencies | Key Client Component | Static? |
|-------|----------------------|---------------------|---------|
| `/` | `getAllSpecimens`, `getComputedStats`, `getMechanisms`, `getFindings` | (none — server rendered) | No |
| `/specimens` | `getAllSpecimens` | `SpecimenBrowser` | No |
| `/specimens/[id]` | `getSpecimenById`, `getAllSpecimens` (related), `getMechanisms`, `getFindings`, `getPurposeClaims`, `getSpecimenEnrichment` | `SpecimenTabs` | Yes (generateStaticParams) |
| `/taxonomy` | `getSpecimensByTaxonomy`, `getMechanisms` | `TaxonomyMatrix`, `ModelAccordion`, `OrientationAccordion` | No |
| `/taxonomy/models/[id]` | `getAllSpecimens`, `getMechanisms` | (none) | Yes (generateStaticParams) |
| `/taxonomy/orientations/[id]` | `getAllSpecimens`, `getMechanisms` | (none) | Yes (generateStaticParams) |
| `/mechanisms` | `getMechanisms` | (none) | No |
| `/mechanisms/[id]` | `getMechanisms`, `getAllSpecimens` | (none) | Yes (generateStaticParams) |
| `/framework` | `getPrimitives`, `getTensions`, `getFindings` | (none) | No |
| `/findings` | `getFindings`, `getAllSpecimens` | (none) | No |
| `/insights` | — | Redirects to `/findings` | No |
| `/purpose-claims` | `getPurposeClaims`, `getAllEnrichments`, `getAllSpecimens` | `PurposeClaimsBrowser` | No |
| `/field-journal` | synthesis session files | (none) | No |
| `/field-journal/[id]` | single session file | (none) | Yes (generateStaticParams) |
| `/ai-native` | `getAllSpecimens`, `getMechanisms` | (none) | No |
| `/tensions` | `getTensions`, `getAllSpecimens` | `TensionMap` | No |
| `/matcher` | `getAllSpecimens`, `getContingencies` | `MatcherForm`, `ChatMatcher` | No |
| `/compare` | `getAllSpecimens` | `ComparisonView` | No |
| `/about` | (none) | (none) | No |
| `/api/chat` | — | — | No (API route) |

---

## 9. Build & Development

### Commands

```bash
cd site
npm run dev      # Development server on port 3000
npm run build    # Production build (generates static pages)
npm start        # Production server
npm run lint     # ESLint
```

### Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `next` | 14.2.35 | Framework |
| `react` | 18 | UI library |
| `typescript` | 5 | Type safety |
| `tailwindcss` | 3.4.1 | Styling |
| `framer-motion` | 12.29.2 | UI animations |
| `d3` | 7.9.0 | Data visualization |
| `@radix-ui/*` | (via shadcn) | Accessible primitives |
| `clsx` + `tailwind-merge` | — | Class name utility (`cn()`) |

### Configuration Files

- `next.config.mjs` — Minimal (empty config, all defaults)
- `tailwind.config.ts` — Custom palette, fonts, darkMode: "class", tailwindcss-animate plugin
- `tsconfig.json` — Strict mode, path alias `@/*` → `./*`, bundler resolution
- `components.json` — shadcn/ui config: RSC enabled, TypeScript, CSS variables, neutral base color

### Validation

- **Data integrity:** `node scripts/validate-workflow.js` (from project root) — 18-section validator covering JSON schema, queue consistency, purpose claims provenance, tension/contingency coverage, insight evidence, enrichment completeness, registry freshness, ID/filename consistency, and specimen schema validation
- **Build verification:** `npm run build` in `site/` — TypeScript compilation + static generation catches type errors and data issues

---

## 10. Testing Strategy (Not Yet Implemented)

### Recommended Stack
- **Unit:** Vitest (fast, native ESM, Next.js compatible)
- **Component:** React Testing Library
- **E2E:** Playwright (browser-based user flow testing)
- **Data:** Existing `validate-workflow.js` script

### Priority Test Targets

1. **`matching.ts`** — Scoring correctness: exact match, adjacent, no data, partial dimensions
2. **`lib/data/specimens.ts`** — Data loading, file exclusion, stat computation, taxonomy grouping
3. **`SpecimenBrowser`** — Filter interactions, search, clear filters
4. **`TensionMap`** — D3 renders with specimen data, tension switching
5. **E2E flow:** Home → Browse → Filter → Specimen Detail → Related → Back

---

## 11. What's Not Built Yet

Mapped to UI Spec implementation phases:

### Phase 4: User Features
- Authentication (Supabase Auth)
- My Herbarium: collections, notes, recently viewed, export queue
- Save/bookmark specimens
- Export: citation generator, teaching case builder, PPTX/PDF/Markdown

### Phase 5: Research Integration
- Research status dashboard (trigger cycles from UI)
- Source registry management UI
- What's New feed (recent updates/new specimens)

### Phase 6: Polish & Scale
- Deployment to Vercel
- Dark mode (Tailwind configured but not implemented)
- Full-text search (Algolia or Supabase — currently client-side filter only)
- Performance: react-window for long lists, lazy loading below fold, D3 simulation pause when not visible
- Accessibility audit
- Mobile responsive refinement (TensionMap needs mobile rethinking)
- Analytics integration

---

## 12. Adding to the Codebase

### Adding a new page

1. Create `app/{route}/page.tsx` as async server component
2. Fetch data via `lib/data/` functions
3. If interactivity needed: create client component in `components/{feature}/`, pass data as props
4. Add nav link in `components/layout/SiteHeader.tsx`

### Adding a new component

1. Place in appropriate `components/{feature}/` directory
2. Only use `"use client"` if the component manages state or uses browser APIs
3. Follow Tailwind conventions: botanical palette colors, `font-serif` for headings, `font-mono` for data labels
4. For animations: Framer Motion for UI, D3 for data visualization

### When specimen data changes

After adding/modifying specimens or synthesis files:
1. Run `node scripts/validate-workflow.js` from project root
2. If dev server is running, refresh the page (fs reads are per-request)
3. For production: run `npm run build` in `site/`
