# Visual Design Specification: "Digital Nature Documentary"
## Ambidexterity Field Guide — Graphics & Animation Overhaul
### February 2, 2026

---

## 1. Vision & Rationale

The current site is informationally strong but visually flat — text cards on cream backgrounds, a single D3 scatter plot, and no imagery. The botanical metaphor (herbarium, specimens, stratigraphy, field guide) is stated in text but never *shown* visually.

This spec transforms the site into a **Digital Nature Documentary** — where every data dimension becomes a visual property, every page tells a story through animation, and the botanical metaphor is rendered, not just described.

**Design direction:** Lean hard into the botanical/geological metaphor with organic, living visuals. Procedural SVG organisms, terrain maps, geological layers, gentle ambient motion everywhere. Think David Attenborough title sequence meets Edward Tufte data density.

**Key principle:** Every visual must be interactive and informational. No decoration for its own sake. The botanical skin is *over* real information, not replacing it.

---

## 2. Required Reading (Context for Implementer)

Before implementing, read these files in order:

1. `CLAUDE.md` — Project bootstrap, structure, session protocol
2. `APP_STATE.md` — Current state: 85 specimens, 12 mechanisms, site status
3. `SW_ARCHITECTURE.md` — Next.js 14 architecture, component patterns, data layer
4. `UI_Spec.md` — Original UI design (this spec extends it visually)
5. `Ambidexterity_Field_Guide_Spec.md` — Domain context: 7 models, 3 orientations, taxonomy

---

## 3. New Dependencies

### Install These Packages

```bash
cd site
npm install gsap @gsap/react          # Scroll animations, timeline sequencing
npm install three @react-three/fiber @react-three/drei  # 3D force graph, terrain
npm install simplex-noise              # Procedural noise for organic SVG shapes
npm install @types/three               # TypeScript types for Three.js
```

### Existing Stack (Keep As-Is)
- `framer-motion@12.29.2` — Continue using for card animations, list transitions, page transitions
- `d3@7.9.0` — Continue using for data calculations (scales, force layout math), but move rendering to SVG/Canvas/Three.js
- `tailwindcss@3.4.1` — Continue using for layout and typography
- `next@14.2.35` — No changes needed

### Tech Role Assignments

| Technology | Responsibility |
|---|---|
| **GSAP + ScrollTrigger** | Scroll-linked animations, home page storytelling, section reveals, number counters |
| **React Three Fiber (R3F)** | 3D ecosystem visualization, terrain-based tension map |
| **@react-three/drei** | Camera controls, text rendering, environment lighting for R3F scenes |
| **simplex-noise** | Procedural organic shapes for SVG organisms, terrain heightmaps |
| **D3.js** | Data calculations (scales, force math, contours) — NOT direct DOM rendering |
| **Framer Motion** | Card hover/tap, list enter/exit, tab transitions, layout animations |
| **SVG (inline React)** | Procedural organisms, geological cross-sections, mechanism diagrams |

---

## 4. Color System Updates

### Current Palette (Unchanged)
The existing botanical palette is strong. Keep all values from `tailwind.config.ts`:

- **Forest** `#1B4332` — primary, headers, links
- **Sage** `#84A98C` — secondary, borders, supporting
- **Amber** `#D4A373` — accent, highlights, CTAs
- **Cream** `#FAF3E0` — backgrounds
- **Charcoal** `#2D3436` — body text

### New: Model Color System (for procedural organisms)

Replace the current `MODEL_COLORS` in TensionMap with a shared constant. Create `site/lib/constants/colors.ts`:

```typescript
// Each model gets a primary + secondary color for gradient organisms
export const MODEL_PALETTE: Record<number, { primary: string; secondary: string; glow: string }> = {
  1: { primary: "#1B4332", secondary: "#27573E", glow: "rgba(27,67,50,0.3)" },   // Deep forest — Research Labs
  2: { primary: "#3F7D5A", secondary: "#5C9173", glow: "rgba(63,125,90,0.3)" },   // Mid forest — Centers of Excellence
  3: { primary: "#84A98C", secondary: "#A5C3AD", glow: "rgba(132,169,140,0.3)" }, // Sage — Embedded Teams
  4: { primary: "#2D6A4F", secondary: "#40916C", glow: "rgba(45,106,79,0.3)" },   // Teal forest — Hub-and-Spoke
  5: { primary: "#D4A373", secondary: "#E2BD93", glow: "rgba(212,163,115,0.3)" }, // Amber — Product/Venture Labs
  6: { primary: "#C48B55", secondary: "#D4A373", glow: "rgba(196,139,85,0.3)" },  // Deep amber — Unnamed/Informal
  7: { primary: "#A87241", secondary: "#C48B55", glow: "rgba(168,114,65,0.3)" },  // Bronze — Tiger Teams
};

// Orientation gets a subtle accent ring color
export const ORIENTATION_ACCENT: Record<string, string> = {
  "Structural": "#1B4332",  // Forest
  "Contextual": "#D4A373",  // Amber
  "Temporal": "#84A98C",    // Sage
};
```

---

## 5. Feature 1: Procedural SVG Organisms on Specimen Cards

### Concept

Every specimen card displays a unique, procedurally generated botanical illustration derived from the specimen's data. No two organisms look alike. The visual properties (shape, branches, size, color, complexity) map directly to real data dimensions.

### Visual Metaphor by Model

Each structural model has a distinct **morphology** — a recognizable base shape that varies per specimen:

| Model | Morphology | Visual Description |
|---|---|---|
| **M1: Research Lab** | Deep taproot system | Single thick root descending with fine branching rootlets. Represents deep, focused exploration. |
| **M2: Center of Excellence** | Radial starburst | Concentric rings emanating from center with spokes. Represents governance radiating outward. |
| **M3: Embedded Teams** | Scattered seed cluster | Small circles distributed across the card, each slightly different. Represents integration into existing structures. |
| **M4: Hub-and-Spoke** | Tree with canopy | Central trunk with spreading branches and a leafy canopy. Represents central coordination + distributed execution. |
| **M5: Product/Venture Lab** | Branching coral / vine | Upward-growing branches that fork and bloom at tips. Represents ventures growing from a base. |
| **M6: Unnamed/Informal** | Mycelium network | Organic network of thin interconnected threads. Represents invisible, distributed transformation. |
| **M7: Tiger Teams** | Lightning bolt / spark | Sharp angular lines radiating from a point. Represents time-boxed energy bursts. |

### Data → Visual Property Mapping

```
┌─────────────────────────┬──────────────────────────────────────────┐
│ Data Dimension          │ Visual Property                          │
├─────────────────────────┼──────────────────────────────────────────┤
│ structuralModel (1-7)   │ Base morphology shape (see table above)  │
│ orientation             │ Outer ring accent color                  │
│ mechanisms.length       │ Number of branches/nodes (0-12)          │
│ mechanism.strength      │ Branch thickness (Strong=3px, Moderate=  │
│                         │ 2px, Emerging=1px dashed)                │
│ layers.length           │ Growth rings / concentric layers (1-5+)  │
│ sources.length          │ Density of fine detail (more=denser)     │
│ confidence              │ Opacity: High=1.0, Medium=0.7, Low=0.4  │
│ completeness            │ Fill completeness (Low=outline only,     │
│                         │ Medium=partial fill, High=fully filled)  │
│ typeSpecimen            │ Gold border ring + star marker            │
│ orgSize                 │ Overall scale of the organism             │
│ tensionPositions        │ Asymmetry — organism leans/stretches     │
│                         │ toward its dominant tension pole          │
│ id (string hash)        │ Seed for simplex noise → unique organic  │
│                         │ variation so no two are identical         │
└─────────────────────────┴──────────────────────────────────────────┘
```

### Implementation Plan

**New component:** `site/components/specimens/OrganismGlyph.tsx`

```
interface OrganismGlyphProps {
  specimen: Specimen;
  size?: number;        // SVG viewport size (default: 120)
  animate?: boolean;    // Enable subtle idle animation (default: false)
  className?: string;
}
```

**Architecture:**
1. Component receives full `Specimen` object
2. Hash the `specimen.id` to create a deterministic noise seed (so same specimen always renders identically)
3. Use `simplex-noise` with that seed to generate organic variation
4. Switch on `structuralModel` to select base morphology generator function
5. Apply data-driven parameters (branch count, thickness, density, opacity)
6. Render as inline `<svg>` with `viewBox="0 0 120 120"`
7. Optional: add subtle CSS animation for idle "breathing" (scale 1.0 → 1.02, 3s ease-in-out infinite)

**Morphology generator functions** (one per model, in `site/lib/organisms/`):

```
site/lib/organisms/
├── index.ts            # Exports generateOrganism(specimen) → SVGPathData[]
├── taproot.ts          # Model 1: Research Lab
├── starburst.ts        # Model 2: Center of Excellence
├── seedCluster.ts      # Model 3: Embedded Teams
├── tree.ts             # Model 4: Hub-and-Spoke
├── coral.ts            # Model 5: Product/Venture Lab
├── mycelium.ts         # Model 6: Unnamed/Informal
└── spark.ts            # Model 7: Tiger Teams
```

Each generator returns an array of SVG path/circle/line elements with computed attributes. The `OrganismGlyph` component renders these.

**Integration points:**
- `SpecimenCard.tsx` — Add `<OrganismGlyph>` to left side of card (or as background watermark at 8% opacity)
- Specimen detail page header — Large `<OrganismGlyph size={200} animate>` next to classification badges
- Home page featured specimens — Medium glyphs on the type specimen showcase cards
- Taxonomy matrix cells — Tiny `<OrganismGlyph size={32}>` thumbnails in populated cells

### Example: Model 4 (Hub-and-Spoke) Tree Generator

Pseudocode for `tree.ts`:

```
Input: specimen with 3 mechanisms (1 Strong, 2 Moderate), 4 layers, 8 sources

1. Draw central trunk: vertical line, height proportional to layers (4 layers → 70% of viewbox)
2. Growth rings: 4 concentric ellipses around trunk base (one per layer), sage fill at 5% opacity
3. Branch count = mechanisms.length (3 branches)
   - Strong mechanism → thick branch (strokeWidth: 3), angles left at ~30°
   - Moderate mechanisms → medium branches (strokeWidth: 2), angle right at ~45° and ~60°
   - Each branch endpoint gets a leaf cluster (small circles) scaled by source count (8 → medium density)
4. Apply simplex noise to all coordinates for organic wobble (±2px displacement)
5. Canopy: large ellipse at top, fill with model gradient (forest primary → secondary), opacity 15%
6. Orientation accent: thin ring around canopy in ORIENTATION_ACCENT color
```

### Performance Notes

- SVGs are lightweight (~1-3KB per organism). No performance concern even with 85 on screen.
- Generate organism data at build time in server components, pass as props to client card.
- Do NOT animate organisms in list views (only on hover or detail pages).
- Use `React.memo` on `OrganismGlyph` since inputs are stable.

---

## 6. Feature 2: GSAP Scroll-Driven Home Page

### Concept

The home page becomes a **scroll-driven story** that teaches the field guide framework as you scroll. Instead of static sections, content assembles, animates, and reveals in response to scroll position.

### New Dependency Setup

GSAP's ScrollTrigger plugin must be registered once. Create a provider:

```typescript
// site/lib/gsap.ts
"use client";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
export { gsap, ScrollTrigger };
```

### Home Page Scroll Sequence (5 Acts)

The home page is restructured as a vertical scroll narrative. Each "act" is a full-viewport section with scroll-triggered animations.

```
┌──────────────────────────────────────────────────────────────────────┐
│ ACT 1: THE QUESTION (100vh, pinned)                                  │
│                                                                      │
│ On enter: Title fades in word by word                                │
│   "How do organizations structurally enable                          │
│    both exploration and execution                                    │
│    in the AI era?"                                                   │
│                                                                      │
│ On scroll: Stats counter animates up (85 specimens, 7 models, etc.) │
│ On scroll further: Subtitle appears, two CTA buttons slide up       │
│                                                                      │
│ Background: Subtle animated noise texture (CSS only, no JS)          │
│ Color: Forest background, cream text                                 │
└──────────────────────────────────────────────────────────────────────┘
                              ↓ scroll
┌──────────────────────────────────────────────────────────────────────┐
│ ACT 2: THE TAXONOMY ASSEMBLES (100vh, pinned while matrix builds)    │
│                                                                      │
│ On enter: Empty 7×3 grid skeleton fades in                           │
│ On scroll (0-30%): Row labels appear one by one (M1...M7)           │
│ On scroll (30-60%): Column labels appear (Structural, Contextual,    │
│   Temporal)                                                          │
│ On scroll (60-100%): Cells populate with dot counts, organism        │
│   thumbnails bloom into populated cells                              │
│                                                                      │
│ Final state: Complete taxonomy matrix, fully interactive              │
│ On unpin: Matrix shrinks to left side, specimen cards appear right    │
└──────────────────────────────────────────────────────────────────────┘
                              ↓ scroll
┌──────────────────────────────────────────────────────────────────────┐
│ ACT 3: SPECIMEN DEEP DIVE (150vh, scrub-animated)                    │
│                                                                      │
│ A single type specimen card builds itself layer by layer:            │
│                                                                      │
│ On scroll (0-15%): Empty card frame appears                          │
│ On scroll (15-30%): Company name and classification badges fly in    │
│ On scroll (30-45%): OrganismGlyph grows from a seed point            │
│ On scroll (45-60%): Description text types in (typewriter effect)    │
│ On scroll (60-75%): Mechanism chips slide in from right              │
│ On scroll (75-90%): Source citations stack up from bottom             │
│ On scroll (90-100%): Card complete — "Browse all 85 specimens →"     │
│                                                                      │
│ Uses: Google DeepMind (M1 type specimen) or Novo Nordisk (M4)        │
└──────────────────────────────────────────────────────────────────────┘
                              ↓ scroll
┌──────────────────────────────────────────────────────────────────────┐
│ ACT 4: THE SEVEN SPECIES (200vh, horizontal scroll section)          │
│                                                                      │
│ 7 large cards scroll horizontally as user scrolls vertically.        │
│ Each card shows:                                                     │
│   - Large OrganismGlyph (size=200, animated)                         │
│   - Model name and short description                                 │
│   - Specimen count badge                                             │
│   - 2-3 example company names                                        │
│                                                                      │
│ Cards are forest-bg with cream text. Each card's organism glyph      │
│ uses the model-specific morphology at large scale.                   │
│                                                                      │
│ GSAP ScrollTrigger pin + horizontal translate                        │
└──────────────────────────────────────────────────────────────────────┘
                              ↓ scroll
┌──────────────────────────────────────────────────────────────────────┐
│ ACT 5: FIELD OBSERVATION + ENTRY POINTS (100vh)                      │
│                                                                      │
│ The rotating field observation quote (existing component, enhanced)   │
│ Plus three entry-point cards that stagger-reveal:                     │
│   1. "Find Organizations Like Mine" → /matcher                       │
│   2. "Browse the Collection" → /specimens                            │
│   3. "Explore the Tension Map" → /tensions                           │
│                                                                      │
│ Footer follows naturally                                              │
└──────────────────────────────────────────────────────────────────────┘
```

### Implementation Plan

**Modified file:** `site/app/page.tsx` — Restructure into 5 act sections with `data-act` attributes and refs.

**New component:** `site/components/home/ScrollNarrative.tsx` ("use client")
- Wraps the home page content
- Registers GSAP ScrollTrigger timelines on mount via `useGSAP()` hook from `@gsap/react`
- Each act gets its own timeline with `scrollTrigger: { trigger, start, end, pin, scrub }`

**New component:** `site/components/home/AnimatedCounter.tsx` ("use client")
- Animates numbers from 0 to target value on scroll-into-view
- Uses GSAP `gsap.to()` with `textContent` tween
- Props: `value: number`, `label: string`, `duration?: number`

**New component:** `site/components/home/SpecimenBuilder.tsx` ("use client")
- The Act 3 specimen card that assembles on scroll
- Uses GSAP timeline with scrub for each layer of the card
- Receives a full `Specimen` object as prop

**New component:** `site/components/home/HorizontalSpecies.tsx` ("use client")
- The Act 4 horizontal scroll section
- Uses GSAP ScrollTrigger pin + horizontal xPercent tween
- Contains 7 large model cards with OrganismGlyphs

### GSAP Performance Notes

- Use `gsap.context()` for cleanup in React strict mode
- Use `@gsap/react`'s `useGSAP()` hook which handles cleanup automatically
- Pin sections need `pinSpacing: true` (default) to avoid layout jumps
- Set `will-change: transform` on animated elements
- Lazy load Act 3-5 content below fold
- `scrub: 1` for smooth scroll-linked feel (1 second smoothing)

### Fallback / Progressive Enhancement

- If JavaScript is disabled: all acts render as static sections (no pins, no scroll triggers)
- Server-render the final state of each act as the default HTML
- GSAP adds the animation layer on hydration
- Mobile: Simplify Act 4 to vertical stack (no horizontal scroll on < 768px)

---

## 7. Feature 3: Terrain-Based Tension Map

### Concept

Replace the current D3 dot scatter with a **topographic terrain visualization** rendered in WebGL via React Three Fiber. Specimens are pins planted in a landscape, with elevation representing density and terrain features representing tension poles.

### Visual Description

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│    STRUCTURAL ←─────────── terrain ───────────→ CONTEXTUAL           │
│    SEPARATION                                    INTEGRATION         │
│                                                                      │
│         ╱╲      🏔️                                                    │
│        ╱  ╲    ╱  ╲        ⛰️        . · .                           │
│       ╱ ●  ╲  ╱ ●  ╲      ╱╲       · ● · ●                         │
│      ╱  ●   ╲╱    ●  ╲   ╱  ╲     · ●     ·                        │
│   ──╱────●──────●──●────╲╱──●─╲──●──────●───── ─ ─                  │
│    ╱ ●         ●      ●    ●    ●    ●       ╲                       │
│   ╱                                            ╲                     │
│                                                                      │
│   [Contour lines show density]   [Pins show specimens]               │
│                                                                      │
│   Legend: 🟢 M1  🟢 M2  🟢 M3  🟢 M4  🟡 M5  🟡 M6  🟤 M7         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Architecture

**Rendering approach:** React Three Fiber with an orthographic camera looking down at a terrain mesh. This gives a 2.5D topographic map feel — 3D geometry viewed from a controlled angle.

**Terrain generation:**
1. Create a plane geometry (e.g., 200×100 segments)
2. For each specimen, place a Gaussian bump on the terrain at its tension position
3. Overlapping bumps create ridges (clusters of specimens at similar tension values)
4. Apply simplex noise at low amplitude for natural terrain texture
5. Color the terrain with a hypsometric tint (green valleys → brown peaks → white snow for highest density)

**Specimen pins:**
- Small 3D cylinders or cones planted on the terrain surface
- Colored by model (MODEL_PALETTE)
- On hover: pin grows taller, label appears (HTML overlay via `@react-three/drei`'s `Html` component)
- On click: navigate to specimen detail

### Implementation Plan

**New component:** `site/components/visualizations/TerrainTensionMap.tsx` ("use client")

```typescript
interface TerrainTensionMapProps {
  specimens: Specimen[];
  tensions: TensionData;
  initialTension?: string;  // fieldName of the tension to display
}
```

**Sub-components:**
- `TerrainMesh.tsx` — The heightmap plane with hypsometric coloring
- `SpecimenPin.tsx` — Individual pin with hover/click interaction
- `TensionLabels.tsx` — HTML overlay labels for tension poles
- `TerrainControls.tsx` — Tension selector dropdown (reuse existing UI, positioned as HTML overlay)

**Data flow:**
1. Parent server component passes specimens + tensions as props
2. Client component extracts tension positions for selected tension
3. Generate heightmap from specimen positions (Gaussian kernel density estimation)
4. Render Three.js scene with terrain + pins

**Camera setup:**
- Orthographic camera at ~45° angle looking down
- Slight rotation allowed (orbit controls with constrained polar angle: 30°-60°)
- Zoom allowed (min/max bounded)
- Default view shows the full map

**Tension switching:**
- When user selects a different tension from the dropdown, animate specimen pins sliding to new positions
- Terrain morphs smoothly (lerp heightmap values over ~1 second)
- Use `useFrame()` for smooth interpolation

### Fallback

- Detect WebGL support via `@react-three/fiber`'s built-in check
- If no WebGL: fall back to the current D3 SVG scatter (keep as `TensionMapFallback.tsx`)
- Use dynamic import with `next/dynamic` and `ssr: false` for the Three.js component

### Performance Notes

- Terrain mesh: ~20,000 vertices (200×100). Lightweight for any modern GPU.
- Specimen pins: 85 instances. Use `InstancedMesh` for performance.
- Heightmap recalculation on tension switch: run in `requestAnimationFrame`, not blocking main thread.
- `Canvas` component should have `frameloop="demand"` — only re-render when camera moves or data changes.

---

## 8. Feature 4: Geological Cross-Section Evolution Timeline

### Concept

Replace the current horizontal dot timeline on specimen detail pages with a **geological cross-section** visualization. Each stratigraphic layer is rendered as a sediment band, stacking from bottom (oldest) to top (newest), with embedded markers showing what changed.

### Visual Description

```
┌──────────────────────────────────────────────────────────────────────┐
│  ORGANIZATIONAL EVOLUTION                                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                                                                │  │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  │
│  │  ░░░░░░░ JANUARY 2026 — Current ░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  │
│  │  ░░░ Model 4 + 5b · Added NVIDIA co-innovation lab ░░░░░░░░░ │  │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  │
│  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │  ▓▓▓▓▓▓▓ JUNE 2025 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │  ▓▓▓ Model 4 · Hub structure publicly detailed ▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  │
│  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  │
│  │  ████████████████████████████████████████████████████████████  │  │
│  │  ████████ 2023 — Foundation █████████████████████████████████  │  │
│  │  ████ Initial AI R&D structure established █████████████████  │  │
│  │  ████████████████████████████████████████████████████████████  │  │
│  │                                                                │  │
│  │  ◀──── OLDEST ────────────────────────── NEWEST ────▶         │  │
│  │        (deepest layer)                   (surface)            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Click any layer to expand details and sources                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Layer Visual Properties

Each geological layer is an SVG rectangle with:

- **Height:** Proportional to the time gap to the next layer (larger gap = thicker sediment). Minimum height of 60px so text fits.
- **Fill:** Gradient using specimen's model color. Older layers are darker/more saturated, newer layers lighter. Apply simplex noise displacement to the top edge of each layer for organic, wavy sediment lines.
- **Top edge:** Not a straight line — use SVG `<path>` with noise-displaced points to create an irregular geological boundary.
- **Embedded fossils/markers:** Small icons or glyphs embedded in the layer:
  - Classification change: small ClassificationBadge
  - New mechanism: MechanismChip miniature
  - Source added: tiny document icon
- **Selected state:** Layer expands vertically, detail card slides out to the right with full summary, sources, and classification at that point in time.

### Implementation Plan

**New component:** `site/components/visualizations/GeologicalTimeline.tsx` ("use client")

```typescript
interface GeologicalTimelineProps {
  layers: Layer[];
  specimen: Specimen;  // For color derivation
  className?: string;
}
```

**Rendering approach:** Inline SVG (not Canvas/WebGL — this is 2D and needs to be accessible).

**Layer stacking:**
1. Reverse layers array (oldest first = bottom)
2. Calculate each layer's height: `baseHeight + (daysSinceNextLayer / maxGap) * bonusHeight`
3. Stack from bottom of SVG viewport, each layer's y = sum of all layers below it
4. Generate wavy top edges using simplex noise seeded by layer index

**Animation (scroll-triggered with GSAP):**
- When the Evolution tab is selected, layers "deposit" from bottom to top with staggered timing
- Each layer slides in from below with opacity 0 → 1, y offset → 0
- Delay: `index * 0.15s`
- Use Framer Motion's `AnimatePresence` since this is triggered by tab change, not scroll

**Click interaction:**
- Clicking a layer adds a `selected` state
- Selected layer grows in height (animated), darker border appears
- Detail panel renders to the right (or below on mobile) with layer summary, classification change notes, and source references

### Integration

Replace the current `EvolutionTimeline.tsx` usage in `EvolutionTab.tsx` with `GeologicalTimeline`. Keep the old component as `EvolutionTimelineLegacy.tsx` until the new one is verified.

---

## 9. Feature 5: 3D Ecosystem Force Graph

### Concept

A full 3D visualization of the entire specimen collection as a living ecosystem. Specimens are glowing nodes floating in space, connected by threads (shared mechanisms, same model, same orientation). The graph breathes — nodes drift gently, connections pulse.

This is the **signature visual** of the site. It appears:
1. As a background element on the home page hero (Act 1) — dark, atmospheric, partially obscured
2. As a full interactive exploration tool on a new `/ecosystem` route

### Visual Description

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│              · · ·          ·                                         │
│           ·  ◉───◉  · ·  ·  ·       ◉ = specimen node               │
│         ◉───◉     ◉──◉    ·         ─ = mechanism connection         │
│        · ╲ ·  ◉  · ╲  ╲  ◉          · = ambient particle            │
│       ·   ◉───◉───◉──◉  ╱                                           │
│          · ╲       ╱ · ◉             Color = structural model        │
│         ·   ◉──◉──◉   ·             Size = source count              │
│              · · ·  ·                Glow = confidence                │
│                     · ·              Connection = shared mechanism    │
│                                                                      │
│   [Orbit with mouse] [Scroll to zoom] [Click node for detail]       │
└──────────────────────────────────────────────────────────────────────┘
```

### Architecture

**React Three Fiber scene with:**

1. **Specimen nodes:** `InstancedMesh` with sphere geometry (85 instances)
   - Radius: `2 + (sources.length / maxSources) * 3` (scaled by evidence depth)
   - Color: `MODEL_PALETTE[model].primary`
   - Emissive glow: `MODEL_PALETTE[model].glow`
   - Opacity: confidence-mapped (High=1.0, Med=0.8, Low=0.5)

2. **Connection lines:** `<Line>` from `@react-three/drei`
   - Drawn between specimens sharing mechanisms
   - Line opacity proportional to number of shared mechanisms
   - Color: average of the two endpoint model colors
   - Animate: subtle pulse (opacity oscillation, 0.3 → 0.5 → 0.3 over 4s)

3. **Force simulation:** Run D3's `forceSimulation` in 3D (extend with z-axis)
   - `forceX/Y/Z` for clustering by model (same model pulls toward same region)
   - `forceCollide` for collision avoidance
   - `forceManyBody` with weak repulsion for spread
   - `forceLink` for mechanism connections (weak spring)
   - Run 300 ticks at init, then let simulation cool

4. **Ambient particles:** 200-500 small dim spheres drifting slowly (simplex noise velocity) for atmosphere

5. **Camera:**
   - `OrbitControls` from `@react-three/drei` with damping
   - Auto-rotation at very slow speed (0.1 rad/s) when no interaction
   - Zoom bounds: min 20, max 200

6. **Hover interaction:**
   - Raycasting detects hovered node
   - Hovered node scales up 1.5x, glow intensifies
   - Connected nodes highlight, unconnected nodes dim
   - HTML overlay label appears (`@react-three/drei` `Html` component)

7. **Click interaction:**
   - Clicking a node: camera smoothly flies to focus on it, detail panel slides in from right
   - Detail panel shows: name, model, orientation, mechanism list, link to full specimen page
   - Click background: returns to default view

### Implementation Plan

**New route:** `site/app/ecosystem/page.tsx`
- Server component that fetches all specimens + mechanisms
- Passes data to client EcosystemView

**New component:** `site/components/ecosystem/EcosystemView.tsx` ("use client")
- R3F `<Canvas>` with scene setup
- Contains: `SpecimenNodes`, `ConnectionLines`, `AmbientParticles`, `EcosystemControls`

**New components:**
```
site/components/ecosystem/
├── EcosystemView.tsx         # Main canvas + overlay UI
├── SpecimenNodes.tsx         # InstancedMesh for all 85 specimens
├── ConnectionLines.tsx       # Lines between connected specimens
├── AmbientParticles.tsx      # Background particle field
├── NodeDetailPanel.tsx       # Right-side panel on click
└── EcosystemLegend.tsx       # Model color legend overlay
```

**Force simulation:**
- Compute positions in a `useMemo` or `useEffect` on mount
- Use D3's `forceSimulation` but extend node positions to include z:
  ```typescript
  nodes.forEach(n => { n.z = 0; });
  // Add custom forceZ similar to forceX/forceY
  ```
- Alternatively, use a 3D force library if available, or implement simple 3D forces manually

**Home page integration:**
- On the home page hero (Act 1), render a simplified version:
  - No interaction (no raycasting, no hover)
  - Dark background, nodes at 30% opacity
  - Slow auto-rotation
  - Gaussian blur overlay for depth-of-field effect
  - Rendered behind the text content
  - Use `<Canvas style={{ position: 'absolute', inset: 0, zIndex: 0 }}>` with text content at `zIndex: 10`

### Performance Notes

- `InstancedMesh` is critical — do NOT create 85 separate `<mesh>` components
- Use `frameloop="demand"` in non-interactive contexts (home page background)
- Use `frameloop="always"` for the interactive `/ecosystem` page
- Dynamic import the Canvas with `next/dynamic({ ssr: false })`
- Set `dpr={[1, 1.5]}` to cap pixel ratio on high-DPI screens
- Connection lines: if > 200 connections, batch into a single `BufferGeometry` with line segments

---

## 10. Feature 6: Mechanism Infographic Diagrams (Bonus)

### Concept

Each of the 12 confirmed mechanisms gets a signature diagram — a small, reusable SVG infographic that explains the pattern visually. These appear on:
- The mechanisms list page (next to each mechanism)
- Specimen detail's Mechanisms tab (next to the mechanism chip)
- The home page as icons

### Examples

| Mechanism | Diagram Concept |
|---|---|
| #1 Protect Off-Strategy Work | Shield icon with a diverging arrow protected inside |
| #2 Bonus Teams That Kill Projects | Tombstone with a checkmark (celebrating project death) |
| #3 Embed Product at Research Frontier | Two overlapping circles (Venn diagram) merging |
| #4 Consumer-Grade UX for Employee Tools | Phone screen morphing into a desktop dashboard |
| #5 Deploy to Thousands Before You Know | Scatter of dots from single source, widening cone |
| #6 Merge Competing AI Teams | Two separate circles being pulled into one |
| #7 Put Executives on the Tools | Briefcase with a cursor/keyboard overlay |
| #8 Log Everything When Regulators Watch | Stack of paper with magnifying glass |
| #9 Hire CAIOs from Consumer Tech | Arrow from phone/app icon to office building |
| #10 Productize Internal Advantages | Internal gear transforming into a product box |
| #11 AI-Driven Workforce Restructuring | Org chart with some nodes being removed/replaced |
| #12 Business Leader as AI Chief | Person icon with both briefcase and circuit board |

### Implementation

Create `site/components/mechanisms/MechanismIcon.tsx`:

```typescript
interface MechanismIconProps {
  mechanismId: number;
  size?: number;        // default 48
  className?: string;
}
```

Each mechanism's SVG is a hand-crafted inline SVG. Alternatively, design in Figma and export as optimized SVG components. Use the model-appropriate colors from the botanical palette.

---

## 11. Implementation Order & Dependencies

### Phase A: Foundation (do first)

1. **Install new dependencies** (gsap, three, simplex-noise, types)
2. **Create `lib/constants/colors.ts`** with MODEL_PALETTE and ORIENTATION_ACCENT
3. **Create `lib/gsap.ts`** client-side GSAP registration
4. **Create `lib/organisms/index.ts`** with organism generator framework

### Phase B: Procedural Organisms (highest visual impact)

5. **Build 7 morphology generators** in `lib/organisms/`
6. **Build `OrganismGlyph.tsx`** component
7. **Integrate into `SpecimenCard.tsx`** — add organism as card visual element
8. **Integrate into specimen detail page** — large animated organism in header
9. **Integrate into `TaxonomyMatrix.tsx`** — tiny organism thumbnails in cells

### Phase C: Home Page Scroll Story

10. **Restructure `app/page.tsx`** into 5 acts with section refs
11. **Build `ScrollNarrative.tsx`** wrapper with GSAP ScrollTrigger setup
12. **Build `AnimatedCounter.tsx`** for stat counters
13. **Build `SpecimenBuilder.tsx`** for Act 3 card assembly
14. **Build `HorizontalSpecies.tsx`** for Act 4 horizontal scroll
15. **Test and tune scroll timing** (this will need iteration)

### Phase D: Geological Timeline

16. **Build `GeologicalTimeline.tsx`** with wavy SVG layers
17. **Replace `EvolutionTimeline` usage** in `EvolutionTab.tsx`
18. **Add scroll-triggered layer deposition animation**
19. **Add click-to-expand layer detail**

### Phase E: Terrain Tension Map

20. **Build `TerrainTensionMap.tsx`** R3F scene
21. **Build `TerrainMesh.tsx`** heightmap from specimen density
22. **Build `SpecimenPin.tsx`** instanced pins
23. **Add tension switching** with animated terrain morphing
24. **Add WebGL fallback** detection → legacy TensionMap
25. **Replace TensionMap usage** on `/tensions` page

### Phase F: 3D Ecosystem

26. **Create `/ecosystem` route** and page
27. **Build `EcosystemView.tsx`** with R3F Canvas
28. **Build `SpecimenNodes.tsx`** with InstancedMesh
29. **Build `ConnectionLines.tsx`** with mechanism-based connections
30. **Build `AmbientParticles.tsx`** for atmosphere
31. **Integrate simplified version** into home page hero background
32. **Add nav link** to ecosystem in SiteHeader

### Phase G: Mechanism Icons (optional, can be done anytime)

33. **Design 12 mechanism SVG icons**
34. **Build `MechanismIcon.tsx`** component
35. **Integrate** into mechanisms list and specimen detail tabs

---

## 12. File Structure (New & Modified)

```
site/
├── lib/
│   ├── constants/
│   │   └── colors.ts              # NEW: MODEL_PALETTE, ORIENTATION_ACCENT
│   ├── gsap.ts                    # NEW: GSAP registration
│   └── organisms/                 # NEW: Procedural organism generators
│       ├── index.ts               # generateOrganism() entry point
│       ├── types.ts               # SVG element types
│       ├── taproot.ts             # M1 generator
│       ├── starburst.ts           # M2 generator
│       ├── seedCluster.ts         # M3 generator
│       ├── tree.ts                # M4 generator
│       ├── coral.ts               # M5 generator
│       ├── mycelium.ts            # M6 generator
│       └── spark.ts               # M7 generator
│
├── components/
│   ├── specimens/
│   │   ├── OrganismGlyph.tsx      # NEW: Procedural SVG organism
│   │   ├── SpecimenCard.tsx       # MODIFIED: Add OrganismGlyph
│   │   └── ... (existing)
│   │
│   ├── home/
│   │   ├── ScrollNarrative.tsx    # NEW: GSAP scroll controller
│   │   ├── AnimatedCounter.tsx    # NEW: Number counter animation
│   │   ├── SpecimenBuilder.tsx    # NEW: Act 3 card assembly
│   │   ├── HorizontalSpecies.tsx  # NEW: Act 4 horizontal scroll
│   │   └── FieldObservation.tsx   # EXISTING (minor enhancements)
│   │
│   ├── visualizations/
│   │   ├── GeologicalTimeline.tsx # NEW: Geological cross-section
│   │   ├── TerrainTensionMap.tsx  # NEW: R3F terrain map
│   │   ├── TerrainMesh.tsx        # NEW: Heightmap plane
│   │   ├── SpecimenPin.tsx        # NEW: 3D map pin
│   │   ├── TensionMap.tsx         # EXISTING → rename TensionMapLegacy.tsx
│   │   └── EvolutionTimeline.tsx  # EXISTING → rename EvolutionTimelineLegacy.tsx
│   │
│   ├── ecosystem/
│   │   ├── EcosystemView.tsx      # NEW: Main R3F canvas
│   │   ├── SpecimenNodes.tsx      # NEW: Instanced sphere nodes
│   │   ├── ConnectionLines.tsx    # NEW: Mechanism connections
│   │   ├── AmbientParticles.tsx   # NEW: Background particles
│   │   ├── NodeDetailPanel.tsx    # NEW: Click detail panel
│   │   └── EcosystemLegend.tsx    # NEW: Color legend overlay
│   │
│   └── mechanisms/
│       ├── MechanismChip.tsx      # EXISTING (unchanged)
│       └── MechanismIcon.tsx      # NEW: SVG infographic icons
│
├── app/
│   ├── page.tsx                   # MODIFIED: Restructured into 5 acts
│   ├── ecosystem/
│   │   └── page.tsx               # NEW: Ecosystem visualization route
│   └── tensions/
│       └── page.tsx               # MODIFIED: Use TerrainTensionMap
│
└── package.json                   # MODIFIED: New dependencies
```

---

## 13. Testing & Validation

After each phase:

1. **Build check:** `cd site && npm run build` — must pass with zero errors
2. **Visual check:** Run `npm run dev` and verify on localhost:3000
3. **Performance check:** Open Chrome DevTools Performance tab, scroll through home page, verify:
   - No jank (consistent 60fps)
   - No layout shifts
   - Memory stable (no leaks from GSAP/Three.js)
4. **Fallback check:** Disable JavaScript in browser → home page should still render readable content
5. **Mobile check:** Resize to 375px width → all content accessible, no horizontal overflow

### Specific Tests Per Phase

| Phase | Test |
|---|---|
| B (Organisms) | All 7 model types render distinct shapes. Same specimen always renders same organism. Type specimens show gold ring. |
| C (Home scroll) | Full scroll-through with no pinning glitches. Stats counter reaches correct numbers. Act 4 horizontal scroll works. |
| D (Geological) | Layers stack correctly (oldest at bottom). Click expands layer. Animation plays on tab switch. |
| E (Terrain) | Tension switching morphs terrain. Pins clickable. Fallback renders on non-WebGL browsers. |
| F (Ecosystem) | 85 nodes visible. Connections drawn. Hover highlights. Click shows detail. Auto-rotation works. |

---

## 14. Open Questions for Implementer

1. **Organism detail level:** Should organisms on compact SpecimenCards be simplified (fewer branches, no growth rings) vs. detail page organisms? Recommendation: Yes — create a `detail` prop that controls complexity level.

2. **Home page load time:** The 3D ecosystem background in Act 1 may add significant JS bundle size. Consider: load it lazily after initial paint, fade it in after 1-2 seconds.

3. **Accessibility:** The terrain map and ecosystem are inherently visual. Ensure:
   - All specimens are still accessible via the existing list views
   - Terrain map has a "list view" toggle
   - 3D scene has `role="img"` with `aria-label` describing the visualization
   - Keyboard navigation for pins/nodes (tab + enter)

4. **Mobile WebGL:** Terrain map and ecosystem may struggle on older phones. Test on: iPhone 12+ (Safari), mid-range Android (Chrome). Fall back gracefully.

5. **Dark mode interaction:** These visuals work well on dark backgrounds. Consider implementing dark mode alongside this work — the ecosystem and terrain map are natural dark-background features.

---

*This spec provides enough detail for a new session to implement all 6 features without additional design decisions. Implementation should follow the phased order in Section 11. Each phase is independently valuable — the site improves with each one shipped.*
