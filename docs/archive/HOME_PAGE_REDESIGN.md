# Home Page Redesign — Detailed Design Document

**Date:** 2026-02-01
**Status:** Approved for implementation
**Depends on:** Also includes a global terminology refresh (see Section B)

---

## Part A: Home Page Layout

### Design Principles

1. **Go all in on the botanical metaphor.** The botany IS the brand. No half measures.
2. **No academic jargon in the hero.** "Ambidexterity" doesn't appear on the landing page.
3. **Type Specimens are the star.** Make them visually rich — like pressed specimen cards in a real herbarium.
4. **Don't segment by audience.** No "for executives" / "for researchers" — just make it beautiful and let people explore.
5. **Rotating featured observation.** A vivid quote or pattern that makes the collection feel alive.

---

### Section 1: Hero

**Replaces:** Current hero (research question + stats subtitle + 2 CTAs)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              A Field Guide to AI Organization                   │  ← Fraunces serif, large
│                                                                 │
│   Like a botanist cataloging species in the wild, we've         │  ← Inter, muted charcoal
│   documented 84 organizations and the structural forms          │
│   they've evolved to navigate the AI era.                       │
│   Browse the collection. Find your species. See what thrives.   │
│                                                                 │
│        [ Enter the Herbarium ]    [ Find Your Match ]           │  ← forest bg / outline
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation details:**
- Title: `font-serif text-4xl lg:text-5xl font-semibold text-forest`
- Subtitle: `text-lg text-charcoal-500`, max-w-2xl, centered
- "84" is dynamically pulled from `stats.totalSpecimens` and rendered `font-semibold text-forest`
- CTA 1 ("Enter the Herbarium") → links to `/specimens` — primary button (forest bg, cream text)
- CTA 2 ("Find Your Match") → links to `/matcher` — outline button (forest border + text)
- py-16 for breathing room

---

### Section 2: The Seven Species

**Replaces:** Stats row (84/7/10/date) AND "Specimen Distribution" (Model 1: 11...)

**Section heading:** "Seven Structural Species" with subtitle "Every organization in the collection fits one of these forms."

```
┌──────────────────────────────────────────────────────────────────┐
│  Seven Structural Species                                        │
│  Every organization in the collection fits one of these forms.   │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐│
│  │ M1           │ │ M2           │ │ M3           │ │ M4          ││
│  │ Research Lab  │ │ Center of    │ │ Embedded     │ │ Hybrid/Hub  ││
│  │              │ │ Excellence   │ │ Teams        │ │ -and-Spoke  ││
│  │ Fundamental  │ │ Governance,  │ │ Product-     │ │ Central     ││
│  │ research,    │ │ standards,   │ │ specific AI  │ │ standards + ││
│  │ 3-10yr       │ │ 6-24mo       │ │ features     │ │ distributed ││
│  │ horizons     │ │ horizon      │ │              │ │ execution   ││
│  │              │ │              │ │              │ │             ││
│  │ 11 collected │ │ 16 collected │ │ 9 collected  │ │ 23 collected││
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘│
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ M5           │ │ M6           │ │ M7           │               │
│  │ Product/     │ │ Unnamed/     │ │ Tiger Teams  │               │
│  │ Venture Lab  │ │ Informal     │ │              │               │
│  │ ...          │ │ ...          │ │ ...          │               │
│  │ 11 collected │ │ 13 collected │ │ 1 collected  │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
└──────────────────────────────────────────────────────────────────┘
```

**Implementation details:**
- Grid: `grid grid-cols-2 md:grid-cols-4 gap-4` (top row 4, bottom row 3)
- Each card:
  - `rounded-lg border border-sage-200 bg-cream-50 p-5 hover:shadow-md transition-shadow cursor-pointer`
  - Model code: `font-mono text-xs text-charcoal-400` (e.g., "M1")
  - Model name: `font-serif text-lg font-semibold text-forest` (e.g., "Research Lab")
  - Description: `text-sm text-charcoal-500 mt-1` — pulled from `STRUCTURAL_MODELS[n].description`
  - Count: `text-xs text-charcoal-400 mt-3` — "{count} collected" (botanical language, not "specimens")
- Each card is a `<Link href="/specimens?model={n}">` (filters specimens page by model)
- Import `STRUCTURAL_MODELS` from `@/lib/types/taxonomy`

---

### Section 3: Type Specimens — The Centerpiece

**Replaces:** Current type specimens section (enhanced significantly)

**Section heading:** "Type Specimens" with subtitle "The reference example of each species — the clearest, best-documented case in the collection."

This is the **visual star** of the page. Each type specimen card should feel like a pressed specimen card in a real herbarium — something you'd find in a museum drawer.

```
┌──────────────────────────────────────────────────────────────────┐
│  Type Specimens                                                  │
│  The reference example of each species — the clearest,           │
│  best-documented case in the collection.                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  ┌──────────────────┐                                      │  │
│  │  │ TYPE SPECIMEN     │   Eli Lilly                         │  │
│  │  │ amber label       │   Decentralized Domain Hubs         │  │
│  │  └──────────────────┘                                      │  │
│  │                                                            │  │
│  │  M1: Research Lab  ·  Structural  ·  Pharmaceuticals       │  │
│  │  43,000 employees  ·  $120B revenue  ·  Indianapolis, IN   │  │
│  │                                                            │  │
│  │  "CEO Dave Ricks explicitly shields these hubs from        │  │
│  │   corporate optimization pressure, recognizing that        │  │
│  │   middle management naturally squashes the off-strategy    │  │
│  │   deviations that produce breakthroughs."                  │  │
│  │                                                            │  │
│  │                                        View full specimen →│  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  (next type specimen card, same format)                    │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Implementation details:**
- Layout: **Single column, full-width cards** (not crammed 3-across). One card per type specimen.
  - On desktop, could do 2-column max, but 1-column is more like leafing through a collection
- Each card:
  - `rounded-lg border-2 border-amber-200 bg-cream-50 p-8 hover:shadow-lg transition-shadow`
  - **Type Specimen label**: `inline-block rounded bg-amber-100 px-3 py-1 font-mono text-xs font-medium uppercase tracking-wide text-amber-800` — styled like a museum specimen label
  - **Name**: `font-serif text-2xl font-semibold text-forest`
  - **Title/subtitle**: `text-base text-charcoal-500` (e.g., "Decentralized Domain Hubs")
  - **Classification line**: Model name (not just "M1") + orientation + industry, joined by ` · `, `font-mono text-sm text-charcoal-400`
  - **Habitat line**: employees + revenue + HQ, same style
  - **Key quote**: Pull `specimen.quotes[0].text` (or first quote). Style as:
    - `border-l-2 border-amber-300 pl-4 italic text-charcoal-600 text-sm`
    - If quote has a speaker, show it: `— {speaker}` right-aligned
  - **Link**: `text-sm text-forest font-medium hover:underline` → `/specimens/{id}`
- Need to add quote data to the home page data fetch. Currently loads `typeSpecimens` but doesn't select a key quote.
- **Data requirement**: Each type specimen must have at least one quote. If `quotes` is empty, show the first 200 chars of description instead.

**Getting the key quote:**
```typescript
// For each type specimen, pick the best quote
const keyQuote = s.quotes?.[0]?.text
  ?? s.description.slice(0, 200) + "...";
const quoteSpeaker = s.quotes?.[0]?.speaker ?? null;
```

---

### Section 4: Collection Summary

**Replaces:** "By Orientation" section (59/23/2 counts)

A single compact strip — warm, not statistical.

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  The collection spans 15 industries — from pharma giants and     │
│  banks to AI startups and government agencies.                   │
│  10 structural patterns documented. Last field update: Jan 31.   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Implementation details:**
- `text-center text-sm text-charcoal-500 py-8 border-t border-sage-200`
- "15 industries" and "10 structural patterns" in `font-semibold text-forest`
- Industry count: `stats.industries.length`
- Pattern count: `mechanisms.confirmed.length` — label as "structural patterns" (see Part B)
- Date: formatted from `stats.lastUpdated`

---

### Section 5: Rotating Field Observation

**New section.** A single vivid quote or pattern that rotates on each page load, making the collection feel alive and giving visitors a taste of the depth.

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  From the Field                                            │  │
│  │                                                            │  │
│  │  "Middle management rationally kills deviations because    │  │
│  │   they don't fit current metrics. But deviations create    │  │
│  │   breakthroughs."                                          │  │
│  │                                                            │  │
│  │  — Pattern: Protect Off-Strategy Work                      │  │
│  │    Observed across 8 organizations                         │  │
│  │                                            Explore more →  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Implementation details:**
- **Rotation strategy**: Server-side random selection. On each page load (or ISR rebuild), pick a random confirmed mechanism that has a `theoreticalConnection` or notable quote.
- Data source: `mechanisms.confirmed` array. Each mechanism has `definition`, `problemItSolves`, `theoreticalConnection`, and linked specimens.
- Selection logic:
  ```typescript
  // Pick a random mechanism with enough evidence to be interesting
  const eligible = mechanisms.confirmed.filter(m => m.specimens.length >= 2);
  const featured = eligible[Math.floor(Math.random() * eligible.length)];
  ```
- **What to show**:
  - A compelling pull-quote. Options in priority order:
    1. `mechanism.theoreticalConnection` (if vivid enough)
    2. `mechanism.problemItSolves`
    3. `mechanism.definition`
  - Pattern name: `mechanism.name`
  - Count: `mechanism.specimens.length` organizations
  - Link: → `/mechanisms/{id}`
- Styling:
  - Container: `rounded-lg border border-sage-200 bg-forest-50/30 p-8 text-center`
  - "From the Field": `font-mono text-xs uppercase tracking-wide text-sage-600`
  - Quote: `font-serif text-lg italic text-charcoal-700 max-w-2xl mx-auto`
  - Pattern name: `font-medium text-forest`
  - Count: `text-sm text-charcoal-500`
  - Link: `text-sm text-forest font-medium hover:underline`
- **Note**: Since this is a server component, `Math.random()` runs at request time in dev and at build time in production. For true rotation in production, either use `revalidate` in the route segment config or make this a client component with `useState`/`useEffect`.

**Recommended approach for rotation:**
```typescript
// In the page component (server side)
export const revalidate = 3600; // Re-pick every hour in production

// Or, make just the observation a client component that picks on mount:
// "use client" — FieldObservation component that receives all eligible
// mechanisms and picks one with useState(() => random)
```

The client component approach is simpler and guarantees rotation on every visit:
```typescript
"use client";
function FieldObservation({ mechanisms }: { mechanisms: ConfirmedMechanism[] }) {
  const [featured] = useState(() => {
    const eligible = mechanisms.filter(m => m.specimens.length >= 2);
    return eligible[Math.floor(Math.random() * eligible.length)];
  });
  // render...
}
```

---

### Full Page Structure Summary

| # | Section | Replaces | Data Needed |
|---|---------|----------|-------------|
| 1 | Hero | Hero + stats row | `stats.totalSpecimens` |
| 2 | Seven Structural Species | Specimen Distribution | `stats.byModel` + `STRUCTURAL_MODELS` |
| 3 | Type Specimens (star) | Type Specimens (enhanced) | `typeSpecimens` with quotes |
| 4 | Collection Summary | By Orientation | `stats.industries.length`, `mechanisms.confirmed.length`, `stats.lastUpdated` |
| 5 | Rotating Field Observation | NEW | `mechanisms.confirmed` (full objects) |

### What's Removed
- Stats row (84 / 7 / 10 / Jan 31) — folded into hero + summary
- "Model 1: 11" distribution grid — replaced by named species cards
- "By Orientation" (59/23/2) — too taxonomic for landing page
- "Ambidexterity" in hero text
- StatCard component (no longer needed on home page; may still be used elsewhere)

---

## Part B: Global Terminology Refresh

The term **"mechanisms"** is academic jargon. Rename to **"patterns"** across the entire app — it's intuitive, botanical-friendly ("growth patterns," "structural patterns"), and universally understood.

### Terminology Changes

| Current Term | New Term | Rationale |
|---|---|---|
| Mechanisms | **Patterns** | "Structural patterns" is intuitive; "mechanisms" is academic |
| Cross-cutting mechanisms | **Patterns across the collection** | Plain language |
| Cross-cutting patterns observed across... | **Structural patterns observed across...** | Cleaner |
| Confirmed Mechanisms | **Confirmed Patterns** | Direct swap |
| Candidate Mechanisms | **Emerging Patterns** | "Candidate" sounds clinical; "Emerging" is botanical |
| Mechanism #{id} | **Pattern #{id}** | Direct swap |
| Specimens Demonstrating This Mechanism | **Organizations showing this pattern** | Warmer |
| No mechanisms documented for this specimen yet | **No patterns documented for this organization yet** | Cleaner |
| Tensions | **Tensions** | KEEP — this term works. "Structural tensions" is intuitive |
| Contingencies | **Context** or **Contingency Profile** | KEEP "Contingency Profile" on detail pages — it works in context |

### Files to Update

**Navigation:**
- `components/layout/SiteHeader.tsx`: `"Mechanisms"` → `"Patterns"`

**Mechanisms page → Patterns page:**
- `app/mechanisms/page.tsx`:
  - Route stays `/mechanisms` (URL stability) but display text changes
  - Metadata title: `"Patterns — Ambidexterity Field Guide"`
  - H1: `"Patterns"`
  - Description: `"Structural patterns observed across multiple specimens. These patterns emerged from systematic observation of how organizations structurally enable both exploration and execution."`
  - Section: `"Confirmed Patterns ({n})"` and `"Emerging Patterns ({n})"`
  - Candidate description: `"Patterns emerging from some specimens but not yet confirmed across enough cases."`

**Mechanism detail page:**
- `app/mechanisms/[id]/page.tsx`:
  - Title: `"{name} — Patterns — Ambidexterity Field Guide"`
  - Breadcrumb: `"Patterns"` → `"Pattern #{id}"`
  - Section: `"Organizations Showing This Pattern ({n})"`

**Specimen detail — Patterns tab:**
- `components/specimens/SpecimenTabs.tsx`: Tab label `"Mechanisms"` → `"Patterns"`
- `components/specimens/MechanismsTab.tsx`:
  - Heading: `"Structural patterns observed in {name}:"`
  - Empty state: `"No patterns documented for this organization yet."`

**Compare page:**
- `app/compare/page.tsx`: Description mentions "mechanisms" → "patterns"
- `components/compare/ComparisonView.tsx`: Section label `"Mechanisms"` → `"Patterns"`

**Related tab:**
- `components/specimens/RelatedTab.tsx`: `"Shared Mechanisms"` → `"Shared Patterns"`

**Home page** (new version):
- Stats/summary: "10 structural patterns documented"

**About page:**
- `app/about/page.tsx`: Multiple references — all "mechanisms" → "patterns"
  - Methodology step: "Link to relevant patterns"
  - Synthesis step: "Identify patterns that appear across multiple specimens"
  - Stats label: "Patterns"

**Note:** The route URL `/mechanisms` and `/mechanisms/[id]` should NOT change (URL stability, bookmarks). Only the display text changes. The internal data structure names (`mechanisms.json`, TypeScript interfaces) also stay the same — this is a UI-only rename.

---

## Part C: Component Changes

### New Component: `FieldObservation`

**File:** `components/home/FieldObservation.tsx`
**Type:** Client component (`"use client"`)

```
Props: {
  patterns: Array<{
    id: number;
    name: string;
    definition: string;
    problemItSolves: string;
    theoreticalConnection?: string;
    specimens: Array<{ id: string; name: string }>;
  }>;
}
```

Picks a random pattern on mount, renders the "From the Field" card. See Section 5 above for styling.

### Modified Component: `StatCard`

No longer needed on the home page. Keep the component in case it's used elsewhere, but remove from `app/page.tsx`.

### New Component: `SpeciesCard`

**File:** `components/home/SpeciesCard.tsx`
**Type:** Server component (no interactivity needed)

A card for the "Seven Structural Species" section. Receives model number, name, description, count. Renders as a Link to `/specimens?model={n}`.

### Enhanced: Type Specimen Cards

These are NOT the same `SpecimenCard` used in the browser. These are custom, larger, richer cards built directly in `app/page.tsx` or extracted to `components/home/TypeSpecimenCard.tsx`.

---

## Visual Reference

### Color Usage on Home Page

| Element | Color | Tailwind |
|---------|-------|----------|
| Title text | Forest | `text-forest` |
| Body text | Charcoal 500-600 | `text-charcoal-500` |
| Card backgrounds | Cream 50 | `bg-cream-50` |
| Card borders | Sage 200 | `border-sage-200` |
| Type specimen borders | Amber 200 | `border-amber-200` |
| Type specimen label bg | Amber 100 | `bg-amber-100` |
| Type specimen label text | Amber 800 | `text-amber-800` |
| Quote border | Amber 300 | `border-amber-300` |
| Primary CTA | Forest bg, cream text | `bg-forest text-cream` |
| Observation bg | Forest 50 tint | `bg-forest-50/30` |
| "From the Field" label | Sage 600 | `text-sage-600` |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Page title | Fraunces | text-4xl/5xl | semibold |
| Section headings | Fraunces | text-2xl | semibold |
| Species name | Fraunces | text-lg | semibold |
| Type specimen name | Fraunces | text-2xl | semibold |
| Body text | Inter | text-base/lg | normal |
| Labels/codes | Mono | text-xs | medium |
| Quotes | Fraunces | text-lg | normal, italic |
