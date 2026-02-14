# UI Improvements Backlog

Prioritized list of usability issues identified from a full walkthrough of all 10 pages on 2026-02-01. Ordered by impact — tackle top-to-bottom.

---

## 1. Redesign Home Page (Landing Experience)

**Status:** Not started
**Severity:** Major UX
**Pages affected:** `/`

**Problem:** The home page is a stats dashboard (84 specimens, 7 models, 10 mechanisms) that means nothing to a first-time visitor. There's no explanation of *what this is* or *who it's for* before the CTAs. The hero question ("How do organizations structurally enable both exploration and execution in the AI era?") is academic — an executive won't know what to do with it. The "Specimen Distribution" section shows "Model 1: 11, Model 2: 16..." with no model names, requiring taxonomy knowledge to parse.

**What good looks like:**
- A clear value proposition: "See how 84 real organizations are structuring AI — from research labs to embedded teams"
- Quick orientation for two audiences: executives ("Find peers facing your constraints") and researchers ("Browse a classified herbarium")
- Featured specimens with context, not just stats
- Model distribution should show names (e.g., "Research Lab: 11") not just "Model 1: 11"
- Consider a "Start here" guided path for first-time visitors

**Screenshots:** Home hero is stats-heavy; specimen distribution uses opaque model numbers.

---

## 2. Fix Navigation (Hierarchy, Mobile, Active States)

**Status:** Not started
**Severity:** Critical (mobile broken) + Major UX (desktop)
**Pages affected:** All pages

**Problem:** Three issues:
1. **No mobile nav at all** — The nav is `hidden md:flex` with no hamburger menu. The site is completely unnavigable on phones/tablets.
2. **Flat and overwhelming** — 7 nav items with no hierarchy. First-time users don't know where to start. "Matcher" and "Compare" sound similar. "Taxonomy" and "Mechanisms" are academic jargon.
3. **No active state** — You can't tell which page you're on from the nav bar.

**What good looks like:**
- Mobile hamburger menu
- Active page highlighted in nav
- Consider grouping: "Explore" (Specimens, Taxonomy) | "Patterns" (Mechanisms, Tensions) | "Tools" (Matcher, Compare) | About
- Or simplify to 4-5 top-level items with dropdowns

---

## 3. Redesign Tension Map (Unusable at 84+ Specimens)

**Status:** Not started
**Severity:** Critical (broken visualization)
**Pages affected:** `/tensions`

**Problem:** The D3 force-directed scatter plot was probably fine at 20 specimens but breaks badly at 84. Labels overlap massively, circles pile on each other (especially on the left/center), organization names are truncated and unreadable. The left side of the "Structural Separation vs. Contextual Integration" view is a dense, illegible blob.

**What good looks like:**
- Zoom/pan capability to explore dense regions
- Click-to-reveal labels instead of showing all labels at once
- Filter by model or orientation to reduce density
- Hover tooltip with full specimen info (already partially works)
- Consider a beeswarm plot or jittered strip plot instead of 2D scatter
- Size circles by completeness or evidence strength
- Option to toggle label visibility

---

## 4. Improve Specimen Cards & Detail Pages

**Status:** Not started
**Severity:** Major UX
**Pages affected:** `/specimens`, `/specimens/[id]`

**Problem — Cards:**
- Every card looks identical (name, subtitle, badges, truncated text)
- No visual differentiation between Type Specimens and regular ones in the grid
- The "Type" badge from the home page doesn't appear in the specimen browser
- "Low" completeness cards look the same as "High" ones — no visual signal

**Problem — Detail page:**
- Wall of text under the Overview tab
- Description paragraphs, quotes, observable markers, contingencies, classification rationale, and open questions all run together
- No visual hierarchy to guide the eye
- Habitat info line (industry, employees, revenue) is easy to miss

**What good looks like — Cards:**
- Type Specimens get a gold/amber border or badge in the browser
- Completeness affects visual treatment (e.g., "Low" cards are more muted/dashed)
- Key metrics visible at a glance (# mechanisms, # sources)

**What good looks like — Detail:**
- Structured sections with clear visual separation (cards, dividers, background colors)
- Key quotes pulled out as callout blocks
- Observable markers as a scannable grid/table, not inline text
- Contingency profile more prominent (it's buried at the bottom)

---

## 5. Polish Interactive Tools (Matcher, Compare)

**Status:** Not started
**Severity:** Major UX
**Pages affected:** `/matcher`, `/compare`

**Problem — Matcher:**
- Right panel is a cold dashed box saying "Select dimensions to find matching specimens"
- No guidance on what to expect or what the results will look like
- No indication of how many specimens match as you select dimensions

**Problem — Compare:**
- Just a lonely search box with "Search and add up to 4 specimens to compare side-by-side"
- No suggestions, no "popular comparisons," no way to get started without knowing specimen names
- Cold start problem — first-time user sees an empty page

**What good looks like — Matcher:**
- Show a preview/example of results before any selection
- Live count of matching specimens as dimensions are selected
- Better empty state with illustration or sample comparison

**What good looks like — Compare:**
- Suggest interesting comparisons (e.g., "Same industry, different model" or "Type specimens")
- Recent/popular comparisons
- "Compare these" links from specimen detail pages

---

## 6. Add Breadcrumbs & Improve Footer

**Status:** Not started
**Severity:** Polish
**Pages affected:** All pages

**Problem:**
- Breadcrumbs only exist on specimen detail pages. Mechanism detail, tension views, etc. have no way back except the nav.
- Footer is just title + tagline. No useful links, no way to navigate from the bottom of a long page.

**What good looks like:**
- Consistent breadcrumbs on all detail/sub-pages
- Footer with key nav links (Specimens, Matcher, About), plus project info

---

## 7. Clean Up Taxonomy Matrix

**Status:** Not started
**Severity:** Polish
**Pages affected:** `/taxonomy`

**Problem:**
- Dot density encoding (filled vs hollow dots) is cryptic and requires explanation
- The specimen count numbers below the dots are the actually useful data
- Dots add visual noise without clear value

**What good looks like:**
- Replace dots with a more intuitive visualization (e.g., sized squares, heat-colored cells, or just clean numbers with background intensity)
- Show specimen names on hover (already works) but make it more discoverable
- Consider making cells clickable with a clearer affordance

---

## 8. Specimens Browser: Pagination or Virtual Scroll

**Status:** Not started
**Severity:** Performance (grows with data)
**Pages affected:** `/specimens`

**Problem:** All 84 cards render in one scroll. Currently manageable but will degrade as the collection grows past 100-150 specimens. No lazy loading.

**What good looks like:**
- Paginate (20-30 per page) or virtual scroll
- Show result count prominently
- "Load more" button or infinite scroll with skeleton loading

---

## Implementation Notes

- The site uses **Next.js 14 App Router**, **Tailwind CSS**, **shadcn/ui**, **Framer Motion**, **D3.js**
- All pages are server-rendered; interactive parts are client components (`"use client"`)
- Botanical color palette: forest (#1B4332), cream (#FAF3E0), amber (#D4A373), sage (#84A98C), charcoal (#2D3436)
- Fonts: Fraunces (serif headings), Inter (sans body)
- Component inventory: ~25 React components in `/site/components/`
- See `SW_ARCHITECTURE.md` for full technical reference
