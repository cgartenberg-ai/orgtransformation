# Plan: Manual Completion of Tension & Contingency Placements

## Context

The overnight synthesis run (9 batches, ~84 specimens) successfully merged mechanism evidence and insights but **systematically dropped tension and contingency data**. The audit shows:

- **19 of 84 specimens** (23%) are fully placed (5/5 tensions, 5/5 contingencies)
- **57 specimens** are partially placed (some data, significant gaps)
- **8 specimens** are completely missing (0/0)
- **Worst gaps**: C3 (CEO Tenure) missing for 64 specimens; T2 (Speed vs. Depth) missing for 42 specimens

**Root cause**: Agent format divergence — agents wrote rich narrative analysis in session logs but either left tension/contingency arrays empty in the JSON, or used formats the normalizer couldn't parse. The two-file template fix prevents this going forward, but doesn't fix the existing data.

**Why manual**: The user said "I care more about data accuracy than automation." Session log extraction is unreliable (later batches have sparse logs, enriched specimens say "already in"), and re-running agents would repeat the format problem. Manual placement ensures every score reflects genuine analytical judgment from reading the specimen file.

## Approach: Collaborative Analytical Placement (Botanist Hat On)

This is real analytical work, not data migration. For each batch, we:

1. **Read each specimen file** (`specimens/{id}.json`) — examine description, habitat, observableMarkers, mechanisms, quotes
2. **Score all 5 tensions** — assign position values (-1.0 to +1.0) with brief evidence strings
3. **Assign all 5 contingencies** — pick the correct level key for each factor
4. **Watch for discoveries** — anything that doesn't fit, patterns across specimens, tension poles that feel wrong, new insights. When something interesting surfaces: **pause and discuss** before deciding whether/how to promote it.
5. **Write a Python patch script** per batch that adds missing placements (never overwriting existing correct data)
6. **Validate** after each batch
7. **Update field journal with ALL substantive observations** — including observations from the read-through, decisions from discussion, connections to existing hypotheses raised by either collaborator, and insights from back-and-forth conversation. The field journal is the primary analytical record. See WORKFLOW.md Phase 3 "Field Journal Protocol."
8. **Update `synthesis/insights.json` if any big ahas emerged** — promote maturity levels (hypothesis→emerging→confirmed), expand evidence arrays with new specimens, refine theoretical frameworks with new dimensions discovered during placement. See WORKFLOW.md Phase 3 "Insight Update Protocol."

### Discovery Protocol During Placement

When reading specimens for placement, we may encounter:
- **A specimen that doesn't fit any tension pole** → possible new tension or pole redefinition
- **A pattern across 3+ specimens** → possible new insight
- **Evidence that changes an existing insight's maturity** → promote hypothesis→emerging→confirmed
- **A contingency level that doesn't exist** → possible new level or new contingency
- **A specimen whose model classification seems wrong** → flag for taxonomy review

**For each discovery**: Stop placement work. Present the finding with evidence. Discuss. Decide together whether to:
- Add it to the taxonomy (new insight, maturity promotion, etc.)
- Flag it for later (note in session log, don't promote yet)
- Dismiss it (interesting but not enough evidence)

This means the work may take longer than pure gap-filling, but the analytical output will be richer.

## Tension Scoring Guide (for consistent judgment)

| Tension | ID | Negative Pole | Positive Pole | Key Question |
|---------|----|---------------|---------------|--------------|
| T1 Structural vs. Contextual | 1 | Structural separation (-1) | Contextual integration (+1) | Separate AI unit, or everyone does AI? |
| T2 Speed vs. Depth | 2 | Deep pilots (-1) | Wide deployment (+1) | Deploy broadly fast, or pilot deeply first? |
| T3 Central vs. Distributed | 3 | Centralized (-1) | Distributed (+1) | One hub controls, or BUs have autonomy? |
| T4 Named vs. Quiet | 4 | Named lab (-1) | Quiet transformation (+1) | Branded AI org/role, or no formal branding? |
| T5 Long vs. Short Horizon | 5 | Long horizons (-1) | Short accountability (+1) | Multi-year R&D, or quarterly pressure? |

## Contingency Level Guide (for consistent judgment)

| Contingency | ID | Valid Levels |
|-------------|----|-------------|
| C1 Regulatory Intensity | `regulatoryIntensity` | `high`, `medium`, `low` |
| C2 Time-to-Obsolescence | `timeToObsolescence` | `high` (threatened), `medium` (augmented), `low` (stable), `fast` (rare) |
| C3 CEO Tenure | `ceoTenure` | `high` (long/strong), `founder`, `medium`, `low` (short/weak), `new` (transformation mandate), `critical` (singular driver) |
| C4 Talent Market | `talentMarketPosition` | `high`, `low`, `nonTraditional`, `non-traditional`, `talent-rich`, `talent-constrained` |
| C5 Technical Debt | `technicalDebt` | `high`, `medium`, `low` |

## Stub/Thin Specimen Policy

For specimens marked as stubs or with completeness "Low"/"Stub":
- If description + observableMarkers give enough signal → place with lower confidence (note in evidence)
- If truly insufficient data → skip and note as "insufficient data — needs enrichment"
- **Do NOT invent data** — if you can't tell, skip that dimension

## Execution Steps

### Step 1: Batch 1 — Fix JPMorgan (the one remaining gap)

JPMorgan is missing T4 and C2/C3/C4. Read `specimens/jpmorgan.json` and assign:
- T4: Named vs. Quiet position
- C2: timeToObsolescence level
- C3: ceoTenure level
- C4: talentMarketPosition level

**Why first**: Small scope (1 specimen, 4 fields), proves the workflow.

### Step 2: Batch 2 — 8 partial specimens

Specimens needing work: bank-of-america (T1-T5 all missing), wells-fargo (T5, C2-C4), ubs (T5, C2-C3), eli-lilly (C4-C5), moderna (T1-T5), novo-nordisk (T1-T5), pfizer (T1,T3-T5), roche-genentech (T1,T3-T4)

Read each specimen file. Score missing tensions and contingencies. Write patch script.

### Step 3: Batch 3 — 4 missing + 2 partial specimens

**Missing**: unitedhealth-group, accenture, cognizant, genpact (0/0 — need everything)
**Partial**: sanofi (T3-T5, C3), infosys (T1,T3-T5, C3)

### Step 4: Batch 4 — All 10 partial specimens

Every automotive/industrial specimen is partial. Need T4 universally, C1-C3 universally. This is the biggest batch of work.

### Step 5: Batch 5 — 1 missing + 8 partial specimens

**Missing**: us-air-force (assess if stub — may skip)
**Partial**: anduril, blue-origin, lockheed-martin, nasa, us-cyber-command, new-york-state, delta-air-lines, fedex

### Step 6: Batch 6 — 9 partial specimens (contingencies are the main gap)

All 10 specimens have good tension coverage (5/5 or close). Main gap: **contingencies are 0/5 for 8 specimens** (disney, netflix, lionsgate, washington-post, kroger, lowes, nike, pepsico, ulta-beauty).

### Step 7: Batch 7 — 7 partial specimens

kyndryl, panasonic, t-mobile, uber, chegg, thomson-reuters, recruit-holdings

### Step 8: Batch 8 — 2 missing + 5 partial specimens

**Missing**: apple, meta-reality-labs (assess if stubs)
**Partial**: amazon-agi, google-deepmind, meta-ai, ami-labs, intel

### Step 9: Batch 9 — 1 missing + 5 partial specimens

**Missing**: crowdstrike (assess if stub)
**Partial**: hp-inc, pinterest, salesforce, sap, workday

### Step 10: Final validation

Run `node scripts/validate-workflow.js`. Recount all specimens for completeness. Report before/after comparison.

## Files Modified

- `synthesis/tensions.json` — adding specimen placements to existing tension arrays
- `synthesis/contingencies.json` — adding specimen IDs to contingency level arrays

## Files Read (per batch)

- `specimens/{id}.json` — the specimen data (description, habitat, observableMarkers, quotes, mechanisms)
- `synthesis/sessions/2026-02-09-synthesis-batch{N}.md` — session log for cross-reference (not primary source — specimen file is primary)

## What This Work Produces

1. **Complete tension/contingency data** — every specimen placed across all 10 dimensions
2. **New insights** — discovered through careful reading, not agent output
3. **Taxonomy refinements** — if we find misclassifications, pole descriptions that need updating, etc.
4. **A session log** — documenting what we found, what we discussed, what we decided

## Verification

After each batch:
1. Run `node scripts/validate-workflow.js` — 0 errors
2. Spot-check: verify 2-3 specimens from the batch are now in the correct tension/contingency arrays
3. After all batches: full recount audit matching the format from the original audit

## Estimated Scope

- ~65 specimens need placement work (57 partial + 8 missing)
- ~5-8 specimens per batch step, reading each file carefully
- This will likely span multiple sessions — that's fine, accuracy > speed
- Start with Batch 1 (JPMorgan only) as proof of workflow, then proceed batch by batch
