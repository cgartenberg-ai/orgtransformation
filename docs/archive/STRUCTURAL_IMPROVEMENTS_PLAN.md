# Structural Improvements Plan: 4 Content & Architecture Fixes
## February 2, 2026

These are content/structure improvements independent of the visual overhaul in `VISUAL_DESIGN_SPEC.md`. They address gaps in how the taxonomy, mechanisms, and tensions are surfaced and connected.

---

## Required Reading

Before implementing, read: `CLAUDE.md`, `APP_STATE.md`, `SW_ARCHITECTURE.md`, `Ambidexterity_Field_Guide_Spec.md`.

---

## Improvement 1: AI-Native Visibility + Model 8 (Skunkworks)

### Problem

- 10+ specimens are tagged `habitat.orgType: "AI-native"` but there's no prominent way to discover them. The SpecimenBrowser has an orgType toggle, but it's buried among other filters and defaults to "AI-adopter".
- Model 7 (Tiger Teams) has 0 specimens after the taxonomy audit. Model 8 (Skunkworks) was added as an emerging/predicted model but appears nowhere in the UI.
- The taxonomy matrix only shows Models 1-7. Model 8 doesn't render.

### What to Change

#### 1a. Add Model 8 to the Taxonomy Constants

**File:** `site/lib/types/taxonomy.ts`

Add Model 8 to `STRUCTURAL_MODELS`:
```typescript
8: {
  name: "Skunkworks",
  shortName: "M8",
  description: "Secret or semi-secret autonomous unit working on breakthrough AI (predicted model, no confirmed specimens yet)",
  characteristics: "A small, autonomous team operating outside normal organizational processes, often with direct executive sponsorship and minimal oversight. Distinguished from Tiger Teams (M7) by permanence and from Research Labs (M1) by secrecy and operational independence. Predicted based on historical patterns (Lockheed Skunk Works, Apple's original Macintosh team) but not yet confirmed in AI-era specimens."
}
```

Update `MODEL_NUMBERS` to `[1, 2, 3, 4, 5, 6, 7, 8]`.

Update `StructuralModel` type to `1 | 2 | 3 | 4 | 5 | 6 | 7 | 8`.

#### 1b. Show Model 8 in the Taxonomy Matrix

**File:** `site/components/taxonomy/TaxonomyMatrix.tsx`

The matrix currently iterates over `MODEL_NUMBERS`. After updating the constant, Model 8 will appear automatically as an 8th row. The cells will show 0 specimens with appropriate empty-state styling.

Add visual distinction for models with 0 specimens — lighter text, italic label, or a small "Predicted" badge.

#### 1c. Add Model 8 Detail Page

**File:** `site/app/taxonomy/models/[id]/page.tsx`

The `generateStaticParams` function iterates `MODEL_NUMBERS`, so adding 8 to the array will auto-generate the page. The page already pulls from `STRUCTURAL_MODELS[id]`, so it will render the description and characteristics. The specimens section will be empty — add an empty state message: "No confirmed specimens yet. This is a predicted structural model based on historical organizational patterns."

#### 1d. Create an AI-Native Collection Page

**New file:** `site/app/ai-native/page.tsx`

A dedicated page for AI-native organizations that:
1. Fetches all specimens, filters to `habitat.orgType === "AI-native"`
2. Renders a header explaining what "AI-native" means in this taxonomy: organizations born as AI companies, not legacy organizations adopting AI
3. Shows the 10+ AI-native specimens as SpecimenCard components
4. Shows a model distribution breakdown for AI-native orgs (likely concentrated in M1 and M5)
5. Notes how AI-native organizations differ from AI-adopters in their ambidexterity patterns

This gives AI-native organizations a proper home rather than burying them behind a filter toggle.

#### 1e. Add Navigation Link

**File:** `site/components/layout/SiteHeader.tsx`

Add "AI-Native" to the navigation. Options for placement:
- As a sub-item under "Specimens" (if we add a dropdown)
- As a standalone nav link between "Specimens" and "Taxonomy"
- As a prominent callout on the home page

Recommendation: Add it as a standalone nav link. It's an important enough concept to warrant top-level navigation.

#### 1f. Improve SpecimenBrowser orgType Toggle

**File:** `site/components/specimens/SpecimenBrowser.tsx`

Current behavior: orgType filter exists but defaults to "AI-adopter" with a simple toggle. Change to:
- Default to "All" (show both AI-native and AI-adopter)
- Three-state toggle: "All" / "AI-native" / "AI-adopter"
- When "AI-native" is selected, show a brief explainer text below the filter

### Files Modified
- `site/lib/types/taxonomy.ts` — Add M8, update types
- `site/lib/types/specimen.ts` — Update StructuralModel type if defined separately
- `site/components/taxonomy/TaxonomyMatrix.tsx` — Empty model styling
- `site/app/taxonomy/models/[id]/page.tsx` — Empty specimen state message
- `site/app/ai-native/page.tsx` — **NEW**: AI-native collection page
- `site/components/layout/SiteHeader.tsx` — Add nav link
- `site/components/specimens/SpecimenBrowser.tsx` — Three-state orgType filter

### Testing
1. `npm run build` passes
2. Taxonomy matrix shows 8 rows, M8 row renders with empty/predicted styling
3. `/taxonomy/models/8` page loads with description and empty specimen state
4. `/ai-native` page shows all AI-native specimens
5. SpecimenBrowser: "All" shows 85 specimens, "AI-native" shows ~10, "AI-adopter" shows ~75

---

## Improvement 2: Mechanism-Taxonomy Affinity

### Problem

Mechanisms (principles) are presented as flat, cross-cutting patterns with no connection to the taxonomy. In reality, mechanisms cluster heavily in specific models and orientations:
- Mechanism #1 (Protect Off-Strategy Work) is 87.5% Structural orientation, concentrated in M1 and M5
- Mechanism #4 (Consumer-Grade UX) is 100% Contextual, 100% M6
- Mechanism #5 (Deploy to Thousands) is heavily Contextual M6

This structure exists implicitly in the data (specimens reference both mechanisms and models) but is never surfaced.

### What to Change

This is a two-part change: (A) compute the affinity data, and (B) surface it in the UI.

#### 2a. Compute Affinity Data — New Synthesis Script

**New file:** `scripts/compute-mechanism-affinity.js`

A Node.js script that:
1. Reads `synthesis/mechanisms.json` (confirmed mechanisms)
2. For each mechanism, reads each linked specimen JSON file
3. Extracts `classification.structuralModel` and `classification.orientation`
4. Computes:
   - `modelDistribution`: `Record<number, { count: number, percentage: number, specimens: string[] }>`
   - `orientationDistribution`: `Record<string, { count: number, percentage: number, specimens: string[] }>`
   - `primaryModel`: The model with the highest count
   - `primaryOrientation`: The orientation with the highest count
   - `affinitySummary`: One-sentence human-readable description (e.g., "Strongly associated with Structural orientation and Models 5a/5b (Venture Labs)")
5. Writes results back into `synthesis/mechanisms.json` as a new `affinityProfile` field on each confirmed mechanism

**Output structure added to each confirmed mechanism:**
```json
{
  "id": 1,
  "name": "Protect Off-Strategy Work",
  "...existing fields...",
  "affinityProfile": {
    "modelDistribution": {
      "1": { "count": 2, "percentage": 25.0, "specimens": ["ssi", "recursion"] },
      "4": { "count": 1, "percentage": 12.5, "specimens": ["eli-lilly"] },
      "5": { "count": 4, "percentage": 50.0, "specimens": ["anthropic", "google-x", "amazon-agi", "samsung-c-lab"] }
    },
    "orientationDistribution": {
      "Structural": { "count": 7, "percentage": 87.5 },
      "Contextual": { "count": 1, "percentage": 12.5 },
      "Temporal": { "count": 0, "percentage": 0 }
    },
    "primaryModel": 5,
    "primaryOrientation": "Structural",
    "affinitySummary": "Strongly associated with Structural orientation (87.5%) and exploration-focused models (M1 Research Labs, M5 Venture Labs). Most common where patient capital and long time horizons enable protected experimentation."
  }
}
```

**Run this script as part of the synthesis workflow.** Add a note to the `/synthesize` skill that after updating mechanisms, the affinity script should be re-run.

Also add to `scripts/validate-workflow.js`: a check that all confirmed mechanisms have an `affinityProfile` field.

#### 2b. Update Synthesis Types

**File:** `site/lib/types/synthesis.ts`

Add the `AffinityProfile` type:
```typescript
export interface AffinityProfile {
  modelDistribution: Record<number, { count: number; percentage: number; specimens: string[] }>;
  orientationDistribution: Record<string, { count: number; percentage: number; specimens: string[] }>;
  primaryModel: number;
  primaryOrientation: string;
  affinitySummary: string;
}

// Update ConfirmedMechanism to include:
export interface ConfirmedMechanism {
  // ...existing fields
  affinityProfile?: AffinityProfile;
}
```

#### 2c. Surface Affinity on the Mechanisms List Page

**File:** `site/app/mechanisms/page.tsx`

For each confirmed mechanism card, add below the existing specimen tag list:
- A row of small `ClassificationBadge` components showing the primary model(s) and orientation
- The `affinitySummary` text in small/muted font
- Example rendering:
  ```
  #1 Protect Off-Strategy Work
  [Definition text...]

  Most common in: [M5 badge] [M1 badge] · [Structural badge]
  "Strongly associated with Structural orientation and exploration-focused models"

  Specimens: eli-lilly, anthropic, google-x, +5 more
  ```

#### 2d. Surface Affinity on the Mechanism Detail Page

**File:** `site/app/mechanisms/[id]/page.tsx`

Add a new section "Taxonomy Affinity" between the definition and the evidence sections:
- Bar chart or horizontal bars showing model distribution (simple Tailwind-styled bars, no D3 needed)
- Orientation breakdown as percentage bars
- The affinity summary paragraph
- Link to each model detail page that this mechanism is associated with

#### 2e. Surface Mechanisms on Taxonomy Model Detail Pages

**File:** `site/app/taxonomy/models/[id]/page.tsx`

Add a new section "Common Principles" below the characteristics section:
1. Read `getMechanisms()` and filter to mechanisms whose `affinityProfile.modelDistribution` includes this model
2. Sort by percentage (highest first)
3. Render as a list of MechanismChip components with specimen count
4. Example for Model 5 page:
   ```
   Common Principles in Venture Labs:
   • #1 Protect Off-Strategy Work (4 specimens, 50% of all occurrences)
   • #3 Embed Product at Research Frontier (2 specimens, 50% of all occurrences)
   • #10 Productize Internal Advantages (3 specimens, 60% of all occurrences)
   ```

#### 2f. Surface Mechanisms on Orientation Detail Pages

**File:** `site/app/taxonomy/orientations/[id]/page.tsx`

Same pattern as 2e but for orientations. Add a "Common Principles" section showing mechanisms whose `affinityProfile.primaryOrientation` matches this orientation, sorted by percentage.

### Files Modified/Created
- `scripts/compute-mechanism-affinity.js` — **NEW**: Compute script
- `synthesis/mechanisms.json` — MODIFIED: Add `affinityProfile` to each confirmed mechanism
- `site/lib/types/synthesis.ts` — Add `AffinityProfile` type
- `site/app/mechanisms/page.tsx` — Add affinity badges and summary
- `site/app/mechanisms/[id]/page.tsx` — Add taxonomy affinity section
- `site/app/taxonomy/models/[id]/page.tsx` — Add common principles section
- `site/app/taxonomy/orientations/[id]/page.tsx` — Add common principles section

### Implementation Order
1. Write and run `compute-mechanism-affinity.js` (data first)
2. Update `synthesis.ts` types
3. Update mechanisms list page (highest visibility)
4. Update mechanism detail page
5. Update model detail pages
6. Update orientation detail pages

### Testing
1. Run `node scripts/compute-mechanism-affinity.js` — verify all 12 confirmed mechanisms get affinity profiles
2. `npm run build` passes
3. Mechanisms page shows affinity badges for each principle
4. Mechanism #4 detail page shows 100% Contextual, 100% M6
5. Model 5 detail page shows Mechanisms #1, #3, #10 as common principles
6. Structural orientation page shows relevant mechanisms

---

## Improvement 3: Taxonomy Browser Enrichment

### Problem

The taxonomy matrix page (`/taxonomy`) shows a 7x3 grid with dot-density counts and links to specimen lists. Below it are model cards and orientation cards that link to detail pages. But the page doesn't teach the taxonomy — it's just a navigation tool.

The model/orientation detail pages exist and have good content (characteristics, descriptions), but they're hidden behind clicks. The matrix page itself doesn't explain what the models mean, how they differ, or why the orientation matters.

### What to Change

#### 3a. Add Inline Model Descriptions to the Taxonomy Page

**File:** `site/app/taxonomy/page.tsx`

Below the matrix but above the model/orientation card grids, add a **"Understanding the Models"** section that renders each model in an expandable/collapsible card:

```
Understanding the 7 Structural Models
──────────────────────────────────────

▼ M1: Research Lab — Fundamental research, breakthroughs (3-10 year horizon)
  A ring-fenced research unit focused on fundamental AI breakthroughs...
  [Characteristics text from STRUCTURAL_MODELS[1].characteristics]
  Type specimen: Google DeepMind
  9 specimens · 100% Structural orientation
  Common principles: #1 Protect Off-Strategy Work, #6 Merge Competing Teams
  [View all M1 specimens →]

▶ M2: Center of Excellence — Governance, standards, enablement
▶ M3: Embedded Teams — Product-specific AI features
▶ M4: Hybrid/Hub-and-Spoke — Central standards + distributed execution
▶ M5: Product/Venture Lab — Commercialize AI into products
▶ M6: Unnamed/Informal — Quiet transformation without formal structure
▶ M7: Tiger Teams — Time-boxed exploration sprints
▶ M8: Skunkworks — Autonomous secret/semi-secret units (predicted)
```

Each expanded card shows:
1. Full description from `STRUCTURAL_MODELS[id].description`
2. Full characteristics from `STRUCTURAL_MODELS[id].characteristics`
3. Type specimen name (if designated) — from `getComputedStats().typeSpecimens`
4. Specimen count + orientation distribution for this model
5. Common mechanisms (from Improvement 2, if implemented; otherwise skip this line)
6. Sub-types (for M5 and M6 only) with counts per sub-type
7. Link to full model detail page

**Implementation:** Create a new client component `site/components/taxonomy/ModelAccordion.tsx` that takes model data and uses Framer Motion for expand/collapse animation.

#### 3b. Add Inline Orientation Descriptions

**File:** `site/app/taxonomy/page.tsx`

Add a **"Three Orientations"** section with a similar expandable pattern:

```
Three Ambidexterity Orientations
──────────────────────────────────

Each specimen has one dominant orientation describing how the organization
balances exploration and execution:

▼ Structural — Exploration and execution in distinct units
  [ORIENTATION_DESCRIPTIONS.Structural expanded text]
  60 specimens · Most common in Models M1, M4, M5
  Characteristic pattern: Ring-fenced budgets, different reporting lines,
  protected time horizons
  [View all Structural specimens →]

▶ Contextual — Individuals balance exploration/execution within roles
▶ Temporal — Organization cycles between phases over time
```

Each expanded card shows:
1. Description from `ORIENTATION_DESCRIPTIONS[orientation]`
2. Specimen count
3. Model distribution (which models this orientation appears most in)
4. Characteristic patterns from the spec
5. Link to orientation detail page

#### 3c. Enrich Matrix Cell Hover/Click

**File:** `site/components/taxonomy/TaxonomyMatrix.tsx`

Currently hovering a cell shows specimen names. Enrich the hover tooltip to show:
- Specimen count
- Names (existing)
- Type specimen indicator (if any specimen in this cell is a type specimen)
- Average completeness level
- Whether this is a "dense" cell (>5 specimens) or "sparse" (<3)

Also: clicking a cell currently navigates to `/specimens?model=X`. Instead, show an inline expansion below the matrix row that lists the specimens in that cell with compact cards, without leaving the taxonomy page. Add a "View all in browser →" link for the full filtered view.

#### 3d. Add Key Insight Callouts

**File:** `site/app/taxonomy/page.tsx`

Add 2-3 callout boxes highlighting key taxonomy insights:

```
┌─────────────────────────────────────────────────────────────────┐
│ 💡 Key Insight: The Quiet Majority                               │
│                                                                   │
│ Model 6 (Unnamed/Informal) captures AI adoption that happens     │
│ without formal structure. Research focused only on named labs     │
│ (Models 1-5) systematically underestimates AI's organizational  │
│ transformation.                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 💡 Key Insight: Structural Dominance                             │
│                                                                   │
│ 60 of 85 specimens (71%) have a Structural orientation —         │
│ separate units for exploration and execution. This may reflect   │
│ reporting bias (structural approaches are more visible) rather  │
│ than actual prevalence.                                          │
└─────────────────────────────────────────────────────────────────┘
```

These should be curated insights, not auto-generated. Hard-code 2-3 that are grounded in the data.

### Files Modified/Created
- `site/app/taxonomy/page.tsx` — Major restructure: add accordion sections, insight callouts
- `site/components/taxonomy/ModelAccordion.tsx` — **NEW**: Expandable model card
- `site/components/taxonomy/OrientationAccordion.tsx` — **NEW**: Expandable orientation card
- `site/components/taxonomy/TaxonomyMatrix.tsx` — Enhanced hover, inline expansion
- `site/lib/data/specimens.ts` — May need a new helper: `getTypeSpecimens()` to identify type specimens per model

### Implementation Order
1. Build `ModelAccordion.tsx` component
2. Build `OrientationAccordion.tsx` component
3. Restructure `taxonomy/page.tsx` to add the accordion sections
4. Enhance `TaxonomyMatrix.tsx` hover/click behavior
5. Add insight callouts (write the copy)

### Testing
1. `npm run build` passes
2. Taxonomy page loads with matrix + "Understanding the Models" + "Three Orientations" sections
3. Each model expands/collapses with animation
4. Expanded model shows: description, characteristics, type specimen, count, orientation distribution
5. M5 expanded shows 3 sub-types with counts
6. M8 expanded shows "predicted" state with no specimens
7. Orientation cards expand to show model distribution and specimen count
8. Matrix cell hover shows enhanced tooltip
9. Insight callout boxes render with correct data

---

## Improvement 4: Tensions Page Enrichment

### Problem

The tensions page shows a D3 scatter plot and a reference section listing each tension's poles. But it doesn't help users understand:
- What drives organizations toward each pole
- How their context (contingencies) relates to where they'd likely fall
- What the clusters mean (why do some models cluster together?)
- How to interpret the visualization for decision-making

### What to Change

#### 4a. Add Interpretive Context Around Each Tension

**File:** `site/app/tensions/page.tsx`

The current reference section shows tension name + tradeoff + two-column poles. Expand each tension card to also include:

1. **"What Drives This Choice"** — A paragraph explaining what organizational factors push toward each pole. Source from `Ambidexterity_Field_Guide_Spec.md` Section 7 (Tensions table) which already has this data but it's not in `tensions.json`.

   Add a new field to each tension in `synthesis/tensions.json`:
   ```json
   {
     "id": 1,
     "name": "Structural Separation vs. Contextual Integration",
     "drivers": "Talent scarcity, coordination costs, and cultural readiness drive where organizations land on this spectrum. Organizations with deep AI talent tend toward structural separation (they can staff dedicated units), while talent-constrained organizations favor contextual integration (everyone must contribute).",
     "...existing fields..."
   }
   ```

2. **"Connected Contingencies"** — Which of the 5 contingencies most influence this tension. For example, Tension 1 (Structural vs. Contextual) is most influenced by Talent Market Position and Regulatory Intensity.

   Add to `tensions.json`:
   ```json
   {
     "connectedContingencies": [
       {
         "contingencyId": "talentMarketPosition",
         "relationship": "Talent-rich organizations can staff separate units (structural). Talent-constrained organizations default to integration (contextual)."
       },
       {
         "contingencyId": "regulatoryIntensity",
         "relationship": "High regulation pushes toward structural separation to contain compliance scope."
       }
     ]
   }
   ```

3. **"Model Clustering"** — A note on which structural models cluster where on this tension. Computed from specimen tension positions grouped by model.

   This can be computed at render time:
   ```
   For Tension 1 (Structural vs. Contextual):
   - M1 (Research Lab): average position -0.7 → strongly structural separation
   - M6 (Unnamed/Informal): average position +0.5 → contextual integration
   - M4 (Hub-and-Spoke): average position -0.3 → moderately structural
   ```

   Render as a compact horizontal bar showing model averages:
   ```
   Model Clustering:
   Structural ◄─────────────────────────────► Contextual
        M1▪  M4▪    M2▪           M6▪  M3▪
   ```

#### 4b. Add a "What Does This Mean For You?" Section

**File:** `site/app/tensions/page.tsx`

After the visualization and reference sections, add a short interpretive section:

```
What Tensions Mean For Your Organization
─────────────────────────────────────────

Tensions are not problems to solve — they are trade-offs to navigate.
Where your organization lands on each tension depends on your context
(see the Situation Matcher for personalized results).

Key patterns from our observations:

• Organizations in highly regulated industries cluster toward structural
  separation and depth-over-speed — compliance requires clear boundaries.

• AI-native companies cluster toward contextual integration — when AI is
  the business, everyone does AI.

• Organizations with long CEO tenure show more tolerance for the
  "long horizon" pole — they can protect multi-year bets.

[Find where your organization fits → Situation Matcher]
```

This is curated content, not auto-generated. Hard-code it based on the patterns visible in the data.

#### 4c. Add a "All Tensions at a Glance" Small Multiples View

**File:** `site/app/tensions/page.tsx`

Above the full interactive tension map, add a small-multiples summary showing all 5 tensions simultaneously as simplified horizontal bars. Each bar is 200px wide, with specimen dots positioned along it. No interaction needed — just a visual overview.

**New component:** `site/components/visualizations/TensionSummary.tsx`

```typescript
interface TensionSummaryProps {
  specimens: Specimen[];
  tensions: Tension[];
}
```

Renders 5 horizontal mini-bars stacked vertically:
```
Structural vs. Contextual    ←|·· ·· · ·    ·  · ··  · · ··|→
Speed vs. Depth               ←|· ·· ··· · · ··  ·   ··· · ·|→
Central vs. Distributed       ←|···· ··  ·  · ·   · · ···  ·|→
Named vs. Quiet               ←|···  ·· ·· ·     · · ·· · ··|→
Long vs. Short Horizon        ←|· ···  ·· · · ·  ·· ·  ···  |→
```

Dots are colored by model. This gives a quick visual of the distribution across all 5 tensions before the user selects one to explore in detail.

#### 4d. Enhance the Tension Map Hover Panel

**File:** `site/components/visualizations/TensionMap.tsx`

Current hover shows: name, title, model badge, orientation badge, 200 chars of description.

Add to the hover panel:
1. The specimen's exact position value on the current tension (e.g., "Position: -0.5 (moderately structural)")
2. Which mechanisms this specimen demonstrates (as MechanismChip components)
3. Key contingency values (regulatory intensity, talent position) if available

This makes the tension map more informative without leaving the page.

#### 4e. Update tensions.json with New Fields

**File:** `synthesis/tensions.json`

Add the following fields to each tension object:
```json
{
  "id": 1,
  "name": "Structural Separation vs. Contextual Integration",
  "drivers": "...",                    // NEW: What drives this choice (paragraph)
  "connectedContingencies": [...],     // NEW: Related contingencies with explanations
  "interpretiveNote": "...",           // NEW: One-sentence insight about this tension
  "...existing fields..."
}
```

This is a synthesis task — the content should be written thoughtfully using the existing specimen data and the spec's Tensions table as source material.

### Files Modified/Created
- `synthesis/tensions.json` — Add `drivers`, `connectedContingencies`, `interpretiveNote` fields
- `site/lib/types/synthesis.ts` — Update `Tension` type with new optional fields
- `site/app/tensions/page.tsx` — Major restructure: add interpretive sections, small multiples, model clustering
- `site/components/visualizations/TensionSummary.tsx` — **NEW**: Small multiples overview
- `site/components/visualizations/TensionMap.tsx` — Enhanced hover panel

### Implementation Order
1. Update `tensions.json` with new content fields (synthesis task — write the drivers, contingency connections, interpretive notes)
2. Update `synthesis.ts` types
3. Build `TensionSummary.tsx` small multiples component
4. Restructure `tensions/page.tsx` with new sections
5. Enhance `TensionMap.tsx` hover panel

### Testing
1. `npm run build` passes
2. Tensions page shows small multiples summary above the main map
3. Each tension reference card shows: drivers paragraph, connected contingencies, model clustering bar
4. Interpretive "What Does This Mean" section renders with curated content
5. Tension map hover shows position value, mechanisms, and contingencies
6. All specimen dots appear in small multiples view

---

## Implementation Sequence Across All 4 Improvements

These improvements are independent and can be done in any order. However, Improvement 2 (mechanism affinity) benefits Improvements 3 and 4, so the recommended order is:

### Wave 1: Data Layer
1. **Improvement 1a-1b**: Add Model 8 to taxonomy constants (5 min, unblocks everything)
2. **Improvement 2a**: Run `compute-mechanism-affinity.js` to generate affinity data (30 min)
3. **Improvement 4e**: Write new tensions.json content (synthesis task, requires domain thinking)

### Wave 2: Core UI
4. **Improvement 1c-1f**: AI-native page, nav link, SpecimenBrowser update
5. **Improvement 2c-2d**: Mechanism affinity on mechanisms pages
6. **Improvement 3a-3b**: Taxonomy accordion sections

### Wave 3: Cross-Linking
7. **Improvement 2e-2f**: Mechanisms on taxonomy pages (depends on 2a + 3a)
8. **Improvement 3c-3d**: Matrix enrichment + insight callouts
9. **Improvement 4a-4d**: Tensions page enrichment + small multiples

### After Each Wave
- Run `npm run build` to verify
- Run `node scripts/validate-workflow.js` to check data integrity
- Update `APP_STATE.md` session log

---

## Session End Checklist

After implementing any of these improvements:
1. Update `APP_STATE.md` with session log entry
2. Run `node scripts/validate-workflow.js`
3. Run `cd site && npm run build`
4. If specimens or synthesis data changed, verify the site renders correctly on `localhost:3000`
