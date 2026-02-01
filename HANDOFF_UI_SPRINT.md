# Handoff: UI Sprint — Home Page + Terminology

**Created:** 2026-02-01
**Priority:** This is the next task to pick up.

---

## What to Do

Two pieces of work, do them in this order:

### Step 1: Global Terminology Rename ("Mechanisms" → "Patterns")

Do this FIRST because the home page redesign uses the new terminology.

**Scope:** UI display text only. Do NOT rename routes, file names, JSON keys, or TypeScript interfaces.

**Files to touch** (see HOME_PAGE_REDESIGN.md Part B for exact strings):

| File | What changes |
|------|-------------|
| `components/layout/SiteHeader.tsx` | Nav label "Mechanisms" → "Patterns" |
| `app/mechanisms/page.tsx` | Title, H1, description, section headers |
| `app/mechanisms/[id]/page.tsx` | Title, breadcrumb, section header |
| `components/specimens/SpecimenTabs.tsx` | Tab label |
| `components/specimens/MechanismsTab.tsx` | Heading text, empty state text |
| `components/compare/ComparisonView.tsx` | Section label |
| `components/specimens/RelatedTab.tsx` | "Shared Mechanisms" → "Shared Patterns" |
| `app/compare/page.tsx` | Description text |
| `app/about/page.tsx` | Multiple references in methodology + stats |

**Also rename:**
- "Confirmed Mechanisms" → "Confirmed Patterns"
- "Candidate Mechanisms" → "Emerging Patterns"
- "Cross-cutting patterns" → "Structural patterns"

**Do NOT rename:**
- Route URLs (`/mechanisms`, `/mechanisms/[id]`)
- JSON files (`synthesis/mechanisms.json`)
- TypeScript types (`MechanismData`, `ConfirmedMechanism`, etc.)
- Data access functions (`getMechanisms()`)
- Internal variable names

### Step 2: Home Page Redesign

**Full spec in:** `HOME_PAGE_REDESIGN.md`

**Summary of the 5 sections:**

1. **Hero** — "A Field Guide to AI Organization" + botanical intro + 2 CTAs ("Enter the Herbarium" / "Find Your Match")
2. **Seven Structural Species** — Named model cards with descriptions + counts (replaces stats row + opaque model distribution)
3. **Type Specimens** — Full-width rich cards with key quotes, habitat lines, amber specimen-label styling. This is the visual star.
4. **Collection Summary** — One-line compact strip (industries, patterns, last update)
5. **Rotating Field Observation** — Client component that picks a random confirmed pattern on mount and shows a vivid quote

**New components to create:**
- `components/home/FieldObservation.tsx` (client, rotating pattern quote)
- `components/home/SpeciesCard.tsx` (optional — can inline in page.tsx)
- Type specimen cards (built in page.tsx or extracted)

**Data changes:**
- Home page already loads `getAllSpecimens()`, `getComputedStats()`, `getMechanisms()`
- Need to pass `mechanisms.confirmed` (filtered to 2+ specimens) to `FieldObservation`
- Need to access `specimen.quotes[0]` for type specimen cards
- Need to import `STRUCTURAL_MODELS` from taxonomy for species names/descriptions

---

## Key Files to Read Before Starting

1. **`HOME_PAGE_REDESIGN.md`** — The full design spec (you're implementing this)
2. **`site/app/page.tsx`** — Current home page (you're rewriting this)
3. **`site/lib/types/taxonomy.ts`** — `STRUCTURAL_MODELS` constant with names/descriptions
4. **`site/lib/data/specimens.ts`** — Data fetching functions
5. **`site/lib/data/synthesis.ts`** — `getMechanisms()` function
6. **`UI_IMPROVEMENTS.md`** — Full backlog (this is item #1)

---

## After Implementation

1. Run `cd site && npm run build` — must pass
2. Visually check all pages that had terminology changes (mechanisms, compare, about, specimen detail)
3. Check home page at multiple widths (mobile, tablet, desktop)
4. Update `UI_IMPROVEMENTS.md` — mark item #1 status as "Done" and note the terminology rename
5. Update `APP_STATE.md` — add session log entry
6. Commit with descriptive message

---

## Design Decisions Already Made (Do Not Revisit)

| Decision | Resolution |
|----------|-----------|
| "Mechanisms" → "Patterns" | Approved. UI text only, not routes/code |
| "Candidate" → "Emerging" | Approved. More botanical |
| No audience segmentation | No "for executives" / "for researchers" sections |
| Botany metaphor: go all in | "Enter the Herbarium", "collected", "species", "field guide" |
| Type specimens = visual star | Full-width cards, key quotes, amber specimen-label styling |
| Section 5 rotates | Client component with useState random pick on mount |
| Remove stats row | Folded into hero text + collection summary |
| Remove "By Orientation" | Too taxonomic for landing page |
| Keep "Tensions" terminology | It works — no rename needed |
| Keep "Contingency Profile" | Works in context on detail pages |
| Route URLs don't change | `/mechanisms` stays even though display says "Patterns" |
