# Implementation Plan: Analytical Framework Restructuring

## Status: PLAN — Awaiting approval before execution
## Date: February 15, 2026
## Scope: Data files (6 operations) + Site changes (8 components) + Navigation + Matcher

---

## Overview

Restructure the entire data layer and site to reflect the converged analytical framework from `synthesis/ANALYTICAL-FRAMEWORK.md` v0.2. This replaces the 65-insight flat list with a theory-grounded architecture: 5 primitives → 5 derived tensions → 10 consolidated findings.

**Guiding principle:** Every change preserves existing empirical data (specimen placements, tension scores, contingency assignments). We restructure the analytical layer on top of the data, never touching the data itself.

---

## Phase 1: Data Layer (Steps 1-6)

### Step 1: Archive insights.json

**What:** Copy current `synthesis/insights.json` to `synthesis/insights-archive-v1.json`

**Why:** The 65 insights are consolidated into 10 findings. We preserve the original for traceability (per settled design decision: "insights are never deleted"). The archive is the permanent record; the new `findings.json` is the active analytical output.

**Files touched:**
- NEW: `synthesis/insights-archive-v1.json` (copy of current insights.json)
- MODIFIED: `synthesis/insights.json` → will be replaced in Step 3

**Risk:** None — pure copy operation.

---

### Step 2: Create `synthesis/primitives.json`

**What:** New JSON file with the 5 primitives that predict structural choice.

**Schema:**
```json
{
  "description": "The 5 primitive variables that predict AI organizational structure...",
  "lastUpdated": "2026-02-15",
  "primitives": [
    {
      "id": "work-architecture-modularity",
      "shortId": "P1",
      "name": "Work Architecture Modularity",
      "definition": "The degree to which the organization's core value-creating work can be decomposed...",
      "subDimensions": [
        {
          "id": "technical-modularity",
          "name": "Technical Architecture",
          "scoringGuide": {
            "high": "Software-first, API-driven, modular codebase",
            "medium": "Mixed digital/physical, partially modular",
            "low": "Integral physical production, tightly coupled systems"
          }
        }
      ],
      "theoreticalAnchors": ["Conway (1967)", "Colfer & Baldwin (2016)", "Simon (1962)", "Henderson & Clark (1990)"],
      "generatesTensions": [1, 3],
      "relatedFindings": ["finding-1-mirroring", "finding-5-industry-equilibria"]
    }
  ]
}
```

**The 5 primitives (from framework v0.2):**
1. P1: Work Architecture Modularity
2. P2: Work Output Measurability
3. P3: Governance Structure
4. P4: Competitive and Institutional Context (sub: P4a competitive, P4b institutional)
5. P5: Organizational Endowment (sub: P5a tech debt, P5b coupling, P5c capital intensity, P5d talent)

**Files touched:**
- NEW: `synthesis/primitives.json`

**Risk:** None — new file, no existing dependencies.

---

### Step 3: Create `synthesis/findings.json` (replaces insights.json)

**What:** New JSON file with the 10 consolidated findings. This becomes the primary analytical output file, replacing the 65-insight insights.json.

**Schema:**
```json
{
  "description": "10 consolidated findings — the converged analytical output...",
  "lastUpdated": "2026-02-15",
  "findings": [
    {
      "id": "finding-1-mirroring",
      "number": 1,
      "title": "Work Architecture Predicts Structural Model (The Mirroring Thesis)",
      "claim": "Organizational AI structure mirrors the modularity of the work...",
      "primitivesEngaged": ["P1", "P5"],
      "mechanism": "Conway's law via Colfer & Baldwin...",
      "evidence": [
        { "specimenId": "toyota", "note": "TRI hub + Enterprise AI spokes..." },
        { "specimenId": "moderna", "note": "mRNA as combinatorial optimization → M6a..." }
      ],
      "formerInsights": [
        "modularity-predicts-ai-structure",
        "combinatorial-production-function-fit",
        "automotive-m4-uniformity",
        "tight-coupling-modularity-constraint",
        "technical-debt-predicts-contextual-structural",
        "capital-intensity-constrains-ai-structure"
      ],
      "testableImplications": [
        "Organizations in modular industries (software, finance) should cluster in M3/M6",
        "Organizations in integral industries (auto, pharma, manufacturing) should cluster in M1/M4"
      ],
      "maturity": "confirmed",
      "paperLink": "paper-1-structure-follows-architecture",
      "relatedFindings": ["finding-5-industry-equilibria"]
    }
  ],
  "fieldObservations": [
    {
      "id": "ai-washing-classification",
      "observation": "AI-washing as classification signal",
      "whyPreserved": "Methodological — helps distinguish genuine structural change from narrative",
      "potentialRelevance": "May become part of Finding 10 (mechanism b)"
    }
  ]
}
```

**The 10 findings (from framework v0.2):**
1. Work Architecture Predicts Structural Model (The Mirroring Thesis)
2. Measurability Drives the Overcorrection Trap (The Moral Hazard Chain)
3. Governance Structure Determines the Feasible Set of Structural Models
4. Institutional Context Shapes Cost, Not Speed
5. Organizations Converge on Industry-Specific Structural Equilibria
6. AI Structure Follows a Predictable Lifecycle (The Consolidation Arc)
7. When Exploration Is Killed, It Crosses Organizational Boundaries (Expelled Exploration)
8. Purpose Rhetoric and Organizational Structure Are Co-Produced Complements
9. AI Is Dissolving Canonical Organizational Boundaries
10. Management Delayering Is a Heterogeneous Phenomenon

**Plus 16 field observations** preserved in `fieldObservations[]` array.

**Evidence mapping:** Each finding's `evidence[]` consolidates the evidence arrays from the former insights it subsumes. The `formerInsights[]` array provides full traceability back to the archived insights.

**Files touched:**
- NEW: `synthesis/findings.json`
- REPLACED: `synthesis/insights.json` (becomes a redirect/pointer to findings.json, or is simply removed since the archive preserves it)

**Risk:** Medium — this is the largest single file creation. Must carefully map all 65 insight IDs to the correct finding.

---

### Step 4: Revise `synthesis/tensions.json`

**What:** Add `derivedFrom` and `masterTension` fields to each tension. Keep all existing data (specimen placements, poles, contingency connections).

**Changes per tension:**
```json
{
  "id": 1,
  "name": "Structural Separation vs. Contextual Integration",
  "masterTension": true,
  "derivedFrom": {
    "primitives": ["P1", "P5"],
    "explanation": "Generated by work modularity × organizational coupling"
  },
  // ... all existing fields preserved as-is ...
}
```

**Specific mappings:**
- T1 (Structural vs Contextual): `masterTension: true`, derivedFrom P1 × P5
- T2 (Speed vs Depth): derivedFrom P4 × P2
- T3 (Central vs Distributed): derivedFrom P3 × P1
- T4 (Named vs Quiet): derivedFrom P4 × P3, add `caveat` field
- T5 (Long vs Short Horizon): derivedFrom P3 × P4

**Files touched:**
- MODIFIED: `synthesis/tensions.json` (additive — new fields, no removed fields)

**Risk:** Low — purely additive changes, no existing data touched.

---

### Step 5: Revise `synthesis/contingencies.json`

**What:** Add `primitiveMapping` field to each contingency, mapping it to the primitive framework.

**Changes per contingency:**
```json
{
  "id": "regulatoryIntensity",
  "name": "Regulatory Intensity",
  "primitiveMapping": {
    "primitive": "P4",
    "subDimension": "P4b",
    "relationship": "Institutional environment — regulatory regime"
  },
  // ... all existing fields preserved ...
}
```

**Specific mappings:**
- regulatoryIntensity → P4b (institutional environment)
- timeToObsolescence → P4a (competitive dynamics)
- ceoTenure → P3 (governance structure) — add note: "Consider renaming to 'governance regime'"
- talentMarketPosition → P5d (organizational endowment — talent)
- technicalDebt → P5a (organizational endowment — tech debt)
- environmentalAiPull → P4 (decompose into P4a + P4b)

**Files touched:**
- MODIFIED: `synthesis/contingencies.json` (additive — new field per contingency)

**Risk:** Low — purely additive.

---

### Step 6: Revise `synthesis/mechanisms.json`

**What:** Apply keep/demote decisions from framework Section 5. Add `findingLink` field. Move demoted mechanisms to candidates with `demotionReason`.

**Specific changes:**
- Mechanism #4 (Consumer-Grade UX): Move to candidates with `demotionReason: "Demoted to field observation — implementation detail, not mechanism"`
- Mechanism #7 (Put Executives on Tools): Move to candidates with `demotionReason: "Demoted to field observation — governance signal, not independent mechanism"`
- Mechanism #11 (AI-Driven Delayering): Move to candidates with `demotionReason: "Replaced by Finding 10 — not a single mechanism but three distinct phenomena"`

**Add `findingLink` to remaining confirmed:**
- #1 → "finding-7-expelled-exploration" (and "finding-1-mirroring" via T1)
- #3 → "finding-9-boundary-dissolution"
- #5 → "finding-2-moral-hazard" (with caveat)
- #6 → "finding-6-lifecycle"
- #8 → "finding-4-regulation-cost"
- #10 → "finding-9-boundary-dissolution"

**Add `frameworkStatus` field:**
- "core" for #1 and #8
- "keep" for #3, #5, #6, #10
- "keep-with-caveat" for #5

**Files touched:**
- MODIFIED: `synthesis/mechanisms.json`

**Risk:** Medium — moving confirmed mechanisms to candidates involves array manipulation in a large JSON file. Use Python script for safety.

---

## Phase 2: TypeScript Types & Data Access (Steps 7-8)

### Step 7: Add TypeScript types

**File:** `site/lib/types/synthesis.ts`

**New types to add:**

```typescript
// === Primitives ===
export interface PrimitiveSubDimension {
  id: string;
  name: string;
  scoringGuide: {
    high: string;
    medium: string;
    low: string;
  };
}

export interface Primitive {
  id: string;
  shortId: string; // "P1", "P2", etc.
  name: string;
  definition: string;
  subDimensions: PrimitiveSubDimension[];
  theoreticalAnchors: string[];
  generatesTensions: number[];
  relatedFindings: string[];
}

export interface PrimitiveData {
  description: string;
  lastUpdated: string;
  primitives: Primitive[];
}

// === Findings (replaces Insight) ===
export type FindingMaturity = "hypothesis" | "emerging" | "confirmed";

export interface FindingEvidence {
  specimenId: string;
  note: string;
}

export interface FieldObservation {
  id: string;
  observation: string;
  whyPreserved: string;
  potentialRelevance: string;
}

export interface Finding {
  id: string;
  number: number;
  title: string;
  claim: string;
  primitivesEngaged: string[]; // ["P1", "P5"]
  mechanism: string;
  evidence: FindingEvidence[];
  formerInsights: string[]; // IDs from insights-archive-v1.json
  testableImplications: string[];
  maturity: FindingMaturity;
  paperLink?: string;
  relatedFindings?: string[];
}

export interface FindingData {
  description: string;
  lastUpdated: string;
  findings: Finding[];
  fieldObservations: FieldObservation[];
}
```

**Modified types:**

```typescript
// Tension — add derivedFrom and masterTension
export interface TensionDerivation {
  primitives: string[]; // ["P1", "P5"]
  explanation: string;
}

export interface Tension {
  // ... existing fields ...
  masterTension?: boolean;
  derivedFrom?: TensionDerivation;
  caveat?: string; // For T4
}

// ContingencyDefinition — add primitiveMapping
export interface ContingencyPrimitiveMapping {
  primitive: string; // "P4"
  subDimension?: string; // "P4b"
  relationship: string;
}

export interface ContingencyDefinition {
  // ... existing fields ...
  primitiveMapping?: ContingencyPrimitiveMapping;
}

// ConfirmedMechanism — add findingLink and frameworkStatus
export interface ConfirmedMechanism {
  // ... existing fields ...
  findingLink?: string; // "finding-1-mirroring"
  frameworkStatus?: "core" | "keep" | "keep-with-caveat";
}
```

**Files touched:**
- MODIFIED: `site/lib/types/synthesis.ts`

**Risk:** Low — additive type changes. Optional fields won't break existing code.

---

### Step 8: Add data access functions

**File:** `site/lib/data/synthesis.ts`

**New functions:**

```typescript
export async function getFindings(): Promise<FindingData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "findings.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load findings.json: ${e}`);
    return EMPTY_FINDINGS;
  }
}

export async function getPrimitives(): Promise<PrimitiveData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "primitives.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load primitives.json: ${e}`);
    return EMPTY_PRIMITIVES;
  }
}
```

**Keep `getInsights()` for backward compatibility** during transition — it will read findings.json and transform to InsightData shape, or read the archive. Decision: deprecate `getInsights()` and update all call sites.

**Files touched:**
- MODIFIED: `site/lib/data/synthesis.ts`

**Risk:** Low — new functions, deprecation of old one.

---

## Phase 3: Site Pages (Steps 9-15)

### Step 9: Create `/framework` route

**NEW:** `site/app/framework/page.tsx`

**Purpose:** The theoretical backbone page — shows the 5 primitives, how they generate tensions, and links to the 10 findings. This is a NEW page that doesn't exist yet.

**Layout:**
```
ANALYTICAL FRAMEWORK
"How do organizations structurally enable both exploration and execution?"

╔═══════════════════════════════════════════════════════════════╗
║  THE 5 PRIMITIVES                                             ║
║                                                               ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
║  │ P1       │  │ P2       │  │ P3       │  │ P4       │  │ P5       │
║  │ Work     │  │ Measur-  │  │ Govern-  │  │ Compet.  │  │ Org      │
║  │ Modular. │  │ ability  │  │ ance     │  │ Context  │  │ Endow.   │
║  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
║       │              │              │              │              │
║       └──────┬───────┴──────┬───────┴──────┬───────┘              │
║              │              │              │                      │
║  ┌───────────▼──┐  ┌───────▼───────┐  ┌──▼──────────┐           │
║  │ T1: MASTER   │  │ T2: Speed     │  │ T3: Central │           │
║  │ Structural   │  │ vs. Depth     │  │ vs. Distrib │           │
║  │ vs Context.  │  │               │  │             │           │
║  └──────────────┘  └───────────────┘  └─────────────┘           │
║                                                                  │
╚══════════════════════════════════════════════════════════════════╝

THE 10 FINDINGS
[Finding 1: The Mirroring Thesis]    ← P1, P5
[Finding 2: The Moral Hazard Chain]  ← P2, P4
... etc
```

**Data dependencies:** `getPrimitives()`, `getTensions()`, `getFindings()`, `getAllSpecimens()`

**Components needed:**
- Server-rendered page with primitives → tension flow
- Finding cards with expandable evidence
- Links to specimen detail pages

**Files touched:**
- NEW: `site/app/framework/page.tsx`

---

### Step 10: Rewrite `/insights` → Findings page

**File:** `site/app/insights/page.tsx` — **FULL REWRITE**

**Current:** 65 insights grouped by theme (convergence, organizational-form, mechanism, workforce, methodology) with maturity badges.

**New:** 10 findings organized by the primitives they engage, with expandable evidence sections, former-insight traceability, and a "Field Observations" section below.

**Layout:**
```
CONSOLIDATED FINDINGS

10 core findings from systematic observation of 157 specimens.
These are the converged analytical output of 65 field insights.

[Filter by primitive: P1 P2 P3 P4 P5] [Filter by paper: 1 2 3]

Finding 1: The Mirroring Thesis
Primitives: [P1] [P5]  |  Paper: Structure Follows Architecture
Claim: Organizational AI structure mirrors the modularity...
Key evidence: [toyota] [moderna] [shopify] [apple] +4 more
[▼ Expand: Show testable implications & former insights]

...

FIELD OBSERVATIONS (16)
Preserved patterns that may be elevated to findings as evidence grows.
[table of field observations]
```

**Change:** The route stays at `/insights` (familiar URL) but the page title becomes "Consolidated Findings" and the content is completely restructured. Alternatively, create `/findings` and redirect `/insights` → `/findings`.

**Decision needed from user:** Keep URL as `/insights` or change to `/findings`?

**My recommendation:** Create at `/findings` AND keep `/insights` as a redirect for backward compatibility.

**Data dependencies:** `getFindings()`, `getPrimitives()`, `getAllSpecimens()`

**Files touched:**
- REWRITTEN: `site/app/insights/page.tsx` (or NEW: `site/app/findings/page.tsx` + redirect)

---

### Step 11: Update `/tensions` page

**File:** `site/app/tensions/page.tsx`

**Changes:**
1. Add "Derived from" primitive tags to each tension card
2. Visual marker for T1 as master tension (e.g., gold border, "MASTER TENSION" badge)
3. Add T4 caveat display
4. Link primitives to `/framework` page

**Specific UI changes:**
- Each tension card gets a new row below the title: `Derived from: [P1 badge] × [P5 badge]`
- T1 gets `border-amber-400` and a crown/star icon
- T4 gets an info tooltip explaining the "interesting only when named implies structural separation" caveat

**Files touched:**
- MODIFIED: `site/app/tensions/page.tsx`

---

### Step 12: Update specimen detail page

**File:** `site/app/specimens/[id]/page.tsx`

**Changes:**
1. Replace "Field Insights" section (lines 142-194) with "Findings" section
2. Instead of filtering `insightData.insights`, filter `findingData.findings`
3. Show which primitives this specimen's findings engage
4. Update data fetching: replace `getInsights()` with `getFindings()`
5. Link findings to `/findings` instead of `/insights`

**The section currently reads:**
```tsx
const specimenInsights = insightData.insights.filter((i) =>
  i.evidence.some((e) => e.specimenId === specimen.id)
);
```

**New version:**
```tsx
const specimenFindings = findingData.findings.filter((f) =>
  f.evidence.some((e) => e.specimenId === specimen.id)
);
```

**Files touched:**
- MODIFIED: `site/app/specimens/[id]/page.tsx`

---

### Step 13: Update home page

**File:** `site/app/page.tsx`

**Changes:**
1. "Key Findings" section (lines 234-291): Change from `insightData.insights.slice(0, 6)` to `findingData.findings.slice(0, 6)`
2. Update import: `getFindings` instead of `getInsights`
3. Update card rendering — findings have `claim` instead of `finding`, `primitivesEngaged` instead of `theme`
4. Update link text: "View all 10 findings →" instead of "View all 65 insights →"
5. Update "Key Field Insights" header to "Core Findings"

**Files touched:**
- MODIFIED: `site/app/page.tsx`

---

### Step 14: Update SiteHeader navigation

**File:** `site/components/layout/SiteHeader.tsx`

**Changes:**
1. Add "Framework" nav item pointing to `/framework`
2. Rename "Insights" to "Findings" (or keep both during transition)
3. Update href from `/insights` to `/findings` if we change the URL

**Proposed nav order:**
```
Specimens | Taxonomy | Principles | Framework | Findings | Tensions | Purpose Claims | Field Journal | Compare | About
```

Or, if too crowded, group under dropdowns in a future phase.

**Files touched:**
- MODIFIED: `site/components/layout/SiteHeader.tsx`

---

### Step 15: Update matcher system prompt

**File:** `site/lib/matcher/buildSystemPrompt.ts`

**Changes:**
1. Replace "Five Contingency Dimensions" with "Five Primitives" framing
2. Add the 10 findings as context for the AI advisor
3. When recommending specimens, reference which findings they support

**This is a quality improvement** — the matcher becomes much more theoretically grounded.

**Files touched:**
- MODIFIED: `site/lib/matcher/buildSystemPrompt.ts`

---

## Phase 4: Verification (Step 16)

### Step 16: Build verification

1. `cd site && npm run build` — verify TypeScript compilation + static generation
2. `node scripts/validate-workflow.js` — verify data integrity
3. Manual smoke test: home page, framework page, findings page, specimen detail, tensions page

**Pass criteria:**
- Build succeeds with 0 errors
- Validator passes with 0 errors (warnings acceptable)
- All pages render correctly with data from new JSON files
- Specimen detail pages show findings instead of insights
- Tensions page shows primitive derivation
- Framework page renders the 5 primitives → tensions → findings flow

---

## Execution Order & Dependencies

```
Step 1 (archive) ─────────────────────────────────────────────┐
Step 2 (primitives.json) ─────────────────────────────────────┤
Step 3 (findings.json) ───────────────────────────────────────┤── Data ready
Step 4 (revise tensions.json) ────────────────────────────────┤
Step 5 (revise contingencies.json) ───────────────────────────┤
Step 6 (revise mechanisms.json) ──────────────────────────────┘
                                                              │
Step 7 (TypeScript types) ────────────────────────────────────┤── Types ready
Step 8 (data access functions) ───────────────────────────────┘
                                                              │
Step 9 (framework page) ──────────────────────────────────────┤
Step 10 (findings page) ──────────────────────────────────────┤
Step 11 (tensions page) ──────────────────────────────────────┤── Pages ready
Step 12 (specimen detail) ────────────────────────────────────┤
Step 13 (home page) ──────────────────────────────────────────┤
Step 14 (SiteHeader) ─────────────────────────────────────────┤
Step 15 (matcher prompt) ─────────────────────────────────────┘
                                                              │
Step 16 (build + verify) ─────────────────────────────────────── Done
```

Steps 1-6 can be done in parallel (independent JSON files).
Steps 7-8 depend on Steps 1-6 (types must match data).
Steps 9-15 depend on Steps 7-8 (pages import types).
Step 16 depends on all above.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Evidence mapping errors (insights → findings) | Medium | Cross-check every `formerInsights[]` ID against archive |
| TypeScript compile errors from type changes | Low | Optional fields, additive changes |
| Large JSON edits fail via Edit tool | Medium | Use Python scripts for mechanism moves |
| Specimen pages break if insights.json removed before findings.json ready | High | Do Steps 1-3 atomically: archive → create findings → remove old |
| Nav too crowded with "Framework" added | Low | Can group later; for now 10 items is manageable |
| Matcher prompt too long with findings context | Low | Summarize findings, don't embed full text |

---

## What This Does NOT Touch

- **Specimen JSON files** — no changes to any `specimens/*.json`
- **Purpose claims** — no changes to `research/purpose-claims/`
- **Nightly pipeline scripts** — left for future session (requires agent prompt updates)
- **Curation protocol** — left for future session (needs primitive-scoring guidance)
- **Validator script** — may need updates if it checks insights.json; will update if build fails
- **Field journal** — no changes
- **Compare view** — no changes (doesn't reference insights)
- **Taxonomy pages** — no changes (don't reference insights)

---

## Estimated Effort

| Phase | Steps | Estimated Time |
|-------|-------|---------------|
| Data Layer | 1-6 | 30-45 min |
| Types & Access | 7-8 | 15-20 min |
| Site Pages | 9-15 | 60-90 min |
| Verification | 16 | 10-15 min |
| **Total** | **16** | **~2-3 hours** |

---

## Decision Point

One open question before execution:

**URL for findings page:** Keep at `/insights` (familiar URL, no broken links) or create `/findings` (cleaner, matches new terminology)?

**Recommendation:** Create `/findings` as the primary route. Keep `/insights` as a Next.js redirect. This gives us clean URLs going forward while not breaking any existing bookmarks or links in the codebase.
