# Implementation Plan: Analytical Framework Pipeline Integration

## Date: 2026-02-15
## Status: Approved

---

## Principle: Exploration and Curiosity

The analytical framework (5 primitives, 10 findings, 5 tensions with primitive derivations) is a **lens, not a cage**. It enriches the pipeline's analytical vocabulary without constraining what agents see.

**Anti-bias rule:** Evidence that contradicts or falls outside the framework receives **equal analytical weight** to evidence that confirms it. We are scientists, not advocates. The principle at every stage is exploration and curiosity.

**Gradient of awareness:**

| Stage | Level | What It Does |
|-------|-------|-------------|
| Research | Antenna | Agents notice framework-relevant signals in free-form notes. No new output fields. |
| Curation | Structured tagging | Optional `primitiveIndicators` and `findingRelevance` fields. Anti-bias guardrail. |
| Synthesis | Full analytical lens | New Step 5d evaluates findings evidence. Primitive lens in field notes. |
| Purpose Claims | Light cross-reference | Optional `primitiveRelevance` in enrichment. Context only. |

---

## Step 1: overnight-research.py — Framework Cheat Sheet

**File:** `scripts/overnight-research.py`
**Change:** Add `FRAMEWORK_ANTENNA` constant (~15 lines) after the TAXONOMY constant. Inject it into `build_research_prompt()` after the TAXONOMY block.

The cheat sheet names the 5 primitives in one line each, reminds agents that novel patterns outside the framework are equally valuable, and directs observations to `botanistNotes`.

No new output fields. No changes to the JSON output schema.

---

## Step 2: Research SKILL.md — Agent Template Update

**File:** `.claude/skills/research/SKILL.md`
**Change:** Add the same framework antenna block to the background agent prompt template (the one used by the Task tool). Insert after the Relevance Test section and before the search queries.

---

## Step 3: SESSION-PROTOCOL.md — Relevance Test Update

**File:** `research/SESSION-PROTOCOL.md`
**Change:** In the Relevance Test (line 22-32), update the "Tension" check to name T1-T5 specifically rather than using the generic word "tension." Keep it as a pass/fail gate — not a scoring exercise.

---

## Step 4: overnight-curate.py — Framework Constants

**File:** `scripts/overnight-curate.py`
**Change:** Add `PRIMITIVES_REF` and `FINDINGS_REF` constants (compact, one line each) after the existing `CONTINGENCIES_REF` constant (~line 124). These are injected into agent prompts alongside the existing reference blocks.

---

## Step 5: overnight-curate.py — Agent Prompt Updates

**File:** `scripts/overnight-curate.py`
**Change:** In `build_curate_prompt()`:

**For CREATE (new specimen) prompts:**
- Add `PRIMITIVES_REF` and `FINDINGS_REF` sections after CONTINGENCIES
- Add anti-bias guardrail block
- Add output instructions for `primitiveIndicators` (optional, null when data is silent) and `findingRelevance` (optional array, supports OR challenges direction)

**For UPDATE (add layer) prompts:**
- Add the anti-bias guardrail block
- Add instructions to update `primitiveIndicators` and `findingRelevance` if new data speaks to them

---

## Step 6: CURATION-PROTOCOL.md — New Optional Fields

**File:** `curation/CURATION-PROTOCOL.md`
**Change:** In Section C "Build the Specimen Content" (after tensionPositions, before openQuestions):
- Add `primitiveIndicators` field documentation with examples
- Add `findingRelevance` field documentation with both "supports" and "challenges" examples
- Add the anti-bias principle as a boxed callout

---

## Step 7: SYNTHESIS-PROTOCOL.md — Full Framework Integration

**File:** `synthesis/SYNTHESIS-PROTOCOL.md`
**Changes:**

1. **Pre-Session Setup:** Add checklist items to read `synthesis/primitives.json` and `synthesis/findings.json`

2. **New Step 5d: Findings Review** (after Step 5b, before Step 5c):
   - Walk through 10 findings
   - Check each specimen for supporting or contradicting evidence
   - Add to finding's evidence array with direction
   - Check maturity changes
   - Propose new findings if batch reveals novel pattern (3+ specimens threshold)
   - Anti-bias reminder: contradictions flagged prominently, not suppressed

3. **Step 5c update:** Add "Primitive Lens" paragraph prompting reflection through (but not limited by) the 5 primitives. Explicitly ask: "What patterns can't the framework explain?"

4. **Session log template:** Add "Findings Updated" and "Findings Challenged" tables

5. **Session Wrap-Up:** Add `synthesis/findings.json` to the update checklist

---

## Step 8: /synthesize SKILL.md — Load New Files

**File:** `.claude/skills/synthesize/SKILL.md`
**Change:** Add two `!cat` lines to load `synthesis/primitives.json` and `synthesis/findings.json` alongside existing loads.

---

## Step 9: overnight-purpose-claims.py — Light Cross-Reference

**File:** `scripts/overnight-purpose-claims.py`
**Change:** Add ~5 lines of context to the agent prompt noting that claims often relate to P3 (governance/authority) and sometimes P4 (institutional context). Add optional `primitiveRelevance` field to enrichment output — one sentence, not a score.

---

## Step 10: Purpose Claims SKILL.md — Primitive Context

**File:** `.claude/skills/purpose-claims/SKILL.md`
**Change:** Add a brief section noting the primitive connection. Minimal — purpose claims is the most specialized pipeline.

---

## Step 11: WORKFLOW.md — Reference Section

**File:** `WORKFLOW.md`
**Change:** Add a "Primitives and Findings" reference section to the scoring guides area (~line 170), listing the 5 primitives and 10 finding titles so all pipeline stages can reference them.

---

## Step 12: Verification

- Run `cd site && npm run build` — confirm no TypeScript errors
- Run `node scripts/validate-workflow.js` — confirm data integrity
- Spot-check overnight-curate.py and overnight-research.py syntax (python3 -c "import scripts...")
