# Robust /synthesize Command Implementation Plan

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Build a deterministic SYNTHESIS-PROTOCOL.md and wire it into `/synthesize`, bringing Phase 3 to the same operational reliability as Phase 1 (research) and Phase 2 (curation).

**Architecture:** Mirror the pattern that works: SKILL.md provides domain knowledge (what to look for), PROTOCOL.md provides the operational runbook (how to run a session step by step). The slash command injects both plus all data files. The protocol enforces idempotency, quality review, and session logging — making synthesis sessions reproducible across Claude sessions.

**Tech Stack:** Markdown protocol, JSON data files, Node.js validator, Claude Code slash commands with `!` bang-include syntax.

---

### Task 1: Create `synthesis/SYNTHESIS-PROTOCOL.md`

**Files:**
- Create: `synthesis/SYNTHESIS-PROTOCOL.md`
- Reference: `research/SESSION-PROTOCOL.md` (pattern to follow)
- Reference: `curation/CURATION-PROTOCOL.md` (pattern to follow)
- Reference: `skills/ambidexterity-synthesis/SKILL.md` (domain knowledge — do NOT duplicate, just reference)
- Reference: `synthesis/mechanisms.json` (current schema)
- Reference: `synthesis/tensions.json` (current schema)
- Reference: `synthesis/contingencies.json` (current schema)
- Reference: `curation/synthesis-queue.json` (queue format)

**Step 1: Write the protocol**

The protocol must cover these sections (following the research/curation protocol pattern):

```markdown
# Synthesis Protocol

## Core Research Question

Every pattern identified must connect to this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

If a cross-cutting pattern doesn't illuminate structural arrangements, tensions, or mechanisms related to this question, it doesn't belong in the synthesis.

---

## Idempotency Rules

- **Never modify a previous synthesis session file.** Each synthesis session creates a new file in `synthesis/sessions/`.
- **Check the synthesis queue before processing.** Only process specimens with `"status": "pending"` in `curation/synthesis-queue.json`. Skip anything already synthesized.
- **Never duplicate evidence in mechanisms.json.** Before adding evidence for a specimen, check if that specimen is already in the mechanism's `specimens` array. If so, APPEND to its existing evidence — don't create a duplicate entry.
- **Never duplicate specimen links in tensions.json or contingencies.json.** Check before adding.
- **Additive updates only to living documents.** New evidence is appended. Existing evidence is never deleted or modified. Mechanism definitions can be refined but old definitions are not lost — revision notes go in the session log.
- **Don't update specimen files.** Synthesis reads specimen data but never modifies specimen JSON. Specimens are Phase 2's responsibility.

---

## Pre-Session Setup

Before analyzing anything:

- [ ] Read `curation/synthesis-queue.json` — identify all specimens with `"status": "pending"`. Record the count.
- [ ] Read `synthesis/mechanisms.json` — load current confirmed mechanisms and candidates. Note which specimens already have evidence recorded.
- [ ] Read `synthesis/tensions.json` — load current tensions. Note which already have specimen links.
- [ ] Read `synthesis/contingencies.json` — load current contingencies. Note which already have specimen links.
- [ ] Read `specimens/registry.json` — get the full specimen list for cross-referencing.
- [ ] Check for previous synthesis session files in `synthesis/sessions/` — understand what was already processed in prior sessions.
- [ ] Plan batch: If >15 specimens are pending, consider processing in batches (e.g., high-completeness first, then medium, then stubs). Stubs may have too little data for meaningful synthesis.
- [ ] Record planned batch in session file frontmatter before starting.

---

## Processing Loop

### Step 1: Read Each Pending Specimen

For each specimen in the synthesis queue with `"status": "pending"`:

1. Read `specimens/{specimenId}.json`
2. Note: classification, completeness, mechanisms already tagged, quotes, observableMarkers, contingencies, tensionPositions, taxonomyFeedback, openQuestions
3. **Skip stubs for mechanism/tension/contingency analysis** if they have insufficient data (meta.completeness = "Stub" AND no mechanisms, no quotes, no observableMarkers). Still mark them synthesized, but note "insufficient data for synthesis" in session log.

### Step 2: Mechanism Analysis (for each specimen)

Walk through all 10 confirmed mechanisms + 3 candidates. For each:

**Does this specimen demonstrate this mechanism?**

Decision tree:
```
Is there direct evidence in the specimen? (quotes, observableMarkers, description, mechanisms array)
├── YES, with quote or specific metric → Add to mechanism's evidence array (strength: "Strong")
├── YES, described but no direct quote → Add to mechanism's evidence array (strength: "Moderate")
├── MAYBE, implied but not explicit → Note as "Emerging" in session log only. Don't add to mechanisms.json yet.
└── NO → Skip
```

When adding evidence to `mechanisms.json`:
```json
{
  "specimenId": "org-id",
  "quote": "Verbatim quote if available, else null",
  "speaker": "Speaker name if available",
  "source": "Source name",
  "notes": "Brief explanation of how this specimen demonstrates the mechanism"
}
```

Also add the specimen ID to the mechanism's `specimens` array (if not already there).

**Does this specimen suggest a NEW mechanism?**

Criteria (from SKILL.md):
1. You observe the same structural practice in 3+ specimens (check across pending batch + existing evidence)
2. The practice addresses the exploration/execution tension specifically
3. It's not already captured by existing mechanisms
4. You can articulate WHY it works organizationally

If yes: add as a candidate mechanism in `mechanisms.json` `candidates` array. Don't promote to confirmed until 3+ specimens with evidence.

If a candidate mechanism now has 3+ specimens: promote from `candidates` to `confirmed`. Note the promotion in the session log.

### Step 3: Tension Analysis (for each specimen)

Walk through all 5 tensions. For each:

**Does this specimen illustrate this tension?**

Check the specimen's `tensionPositions` field. Also check description, observableMarkers, and taxonomyFeedback for tension signals.

Decision tree:
```
Does the specimen have a tensionPosition score for this tension?
├── YES (non-null) → Add specimen to tension's specimens array with position and evidence
├── NO score, but description/markers show tension at work → Add with inferred position and rationale
└── NO evidence → Skip
```

When adding a specimen to a tension:
```json
{
  "specimenId": "org-id",
  "position": -0.7,
  "evidence": "Brief explanation of how the tension manifests"
}
```

**Does this specimen reveal a NEW tension?**

Criteria:
1. A structural trade-off that multiple specimens navigate differently
2. Not captured by existing 5 tensions
3. Connected to the core research question

If yes: propose in session log. Don't add to `tensions.json` until confirmed with 3+ specimens showing different positions.

### Step 4: Contingency Analysis (for each specimen)

Walk through all 5 contingencies. For each:

**Does this specimen illustrate this contingency at work?**

Check the specimen's `contingencies` field and habitat data.

```
Does the specimen's context clearly demonstrate this contingency variable?
├── YES, high end → Add to contingency's high.specimens array
├── YES, low end → Add to contingency's low.specimens array
└── Insufficient context → Skip
```

**Does this specimen suggest a NEW contingency variable?**

If a contextual factor repeatedly determines structural choices across specimens and isn't captured by the 5 existing contingencies, propose it in the session log.

### Step 5: Convergent Evolution Check (across batch)

After processing all specimens in the batch, look for convergent evolution:

```
Are there 2+ specimens from DIFFERENT industries that independently arrived at similar structural solutions?
├── YES → Document the convergent pattern in the session log with:
│   - The similar solution
│   - Which orgs converged
│   - The organizational problem they were solving
│   - How their implementations differ in detail
└── NO → Note "No new convergent evolution patterns identified"
```

### Step 6: Taxonomy Refinement Check (across batch)

Review all `taxonomyFeedback` fields from processed specimens:

```
Are there specimens that don't fit the 7-model taxonomy cleanly?
├── 5+ specimens with similar misfit → Propose new model or sub-type
├── 2-4 specimens with similar misfit → Note as "emerging pattern, monitor"
├── Isolated misfit → Note in session log, no action
└── All fit → Note "Taxonomy adequate for current specimens"
```

Also check: Should any model be retired or merged? Should any sub-type be added?

---

## Quality Review

Before wrapping up the synthesis session:

- [ ] Does every new evidence entry in mechanisms.json have a `specimenId` that matches a real specimen?
- [ ] Are specimen arrays in mechanisms/tensions/contingencies free of duplicates?
- [ ] Were High-completeness specimens analyzed for ALL mechanisms (not just obvious ones)?
- [ ] Were evolution specimens (reclassified orgs) specifically checked for what the evolution reveals about structural dynamics?
- [ ] Does every convergent evolution observation cite at least 2 specimens from different industries?
- [ ] Are session log insights connected to the core research question (not just interesting observations)?
- [ ] Were stubs appropriately handled (marked synthesized with "insufficient data" note, not force-fitted)?

---

## Session Wrap-Up

After ALL pending specimens are processed:

- [ ] **Update `curation/synthesis-queue.json`**:
  - Set `"status": "synthesized"` for each processed specimen
  - Set `"synthesizedIn": "YYYY-MM-DD-synthesis.md"` for each
  - Update `"lastSynthesisDate": "YYYY-MM-DD"`
  - Update `"lastUpdated": "YYYY-MM-DD"`

- [ ] **Update `synthesis/mechanisms.json`**:
  - All new evidence entries added
  - All new specimen IDs added to specimens arrays
  - Any candidate promotions reflected
  - `"lastUpdated": "YYYY-MM-DD"`

- [ ] **Update `synthesis/tensions.json`**:
  - All new specimen links added
  - `"lastUpdated": "YYYY-MM-DD"`

- [ ] **Update `synthesis/contingencies.json`**:
  - All new specimen links added
  - `"lastUpdated": "YYYY-MM-DD"`

- [ ] **Write synthesis session log** at `synthesis/sessions/YYYY-MM-DD-synthesis.md`:

  Use the session output format from `skills/ambidexterity-synthesis/SKILL.md` (lines 282-334):

  ```yaml
  ---
  session_date: "YYYY-MM-DD"
  specimens_processed: ["org-1", "org-2"]
  specimens_skipped_stubs: ["org-3"]
  mechanisms_updated: [1, 5, 7]
  candidates_promoted: []
  new_candidates: []
  tensions_updated: [1, 3]
  contingencies_updated: ["regulatoryIntensity"]
  convergent_patterns: 0
  taxonomy_proposals: 0
  ---

  # Synthesis Session: YYYY-MM-DD

  ## Specimens Analyzed
  [Table: specimen, action from queue, completeness, mechanisms found, tensions found]

  ## Mechanism Updates

  ### Strengthened
  | Mechanism | New Evidence | From Specimens |
  |-----------|-------------|----------------|

  ### Candidates Identified
  | Candidate | Evidence Count | Confidence |
  |-----------|----------------|------------|

  ### Candidates Promoted to Mechanisms
  | New Mechanism | Based On |
  |---------------|----------|

  ## Tensions Identified/Updated
  | Tension | New Insight |
  |---------|-------------|

  ## Contingencies Identified/Updated
  | Contingency | New Insight |
  |-------------|-------------|

  ## Convergent Evolution Observed
  | Pattern | Organizations | Significance |
  |---------|---------------|--------------|

  ## Taxonomy Proposals
  | Proposal | Type | Confidence |
  |----------|------|------------|

  ## Key Insights for Executives
  [2-3 bullet points]

  ## Key Insights for Academics
  [2-3 bullet points]

  ## Open Questions
  [What would we most like to know that we don't?]
  ```

- [ ] **Run validator**:
  ```bash
  node scripts/validate-workflow.js
  ```
  Fix any issues before completing.
```

**Step 2: Review the protocol against both reference protocols**

Verify:
- Idempotency rules cover the same ground as research/curation protocols
- Pre-session setup is as explicit as curation's checklist
- Processing loop is deterministic (decision trees, not judgment calls)
- Quality review checklist catches real issues
- Session wrap-up updates ALL downstream files
- Session log format matches what SKILL.md defines

---

### Task 2: Rewrite `.claude/skills/synthesize/SKILL.md` with protocol injection

**Files:**
- Modify: `.claude/skills/synthesize/SKILL.md`

**Step 1: Rewrite the slash command to inject the protocol**

Follow the exact pattern from `/curate` which injects 9 files. The `/synthesize` command should inject:

1. **SYNTHESIS-PROTOCOL.md** (the new protocol — this is the primary operational guide)
2. **SKILL.md** (domain knowledge — what to look for, quality standards, formats)
3. **synthesis-queue.json** (what needs processing)
4. **mechanisms.json** (current state — what evidence exists)
5. **tensions.json** (current state)
6. **contingencies.json** (current state)
7. **registry.json** (specimen inventory for cross-referencing)

Structure:
```markdown
---
name: synthesize
description: "Phase 3: Synthesize curated specimens into cross-cutting patterns — mechanisms, tensions, contingencies, and taxonomy refinements"
disable-model-invocation: true
---

# Phase 3: Synthesis Session

## Core Research Question

Every pattern you identify must connect to this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

## Synthesis Protocol

Follow this protocol step by step. Do NOT skip steps.

!`cat "...synthesis/SYNTHESIS-PROTOCOL.md"`

## Synthesis Domain Knowledge (what to look for, quality standards, output formats)

!`cat "...skills/ambidexterity-synthesis/SKILL.md"`

## Synthesis Queue (specimens to process)

!`cat "...curation/synthesis-queue.json"`

## Current Mechanisms (update with new evidence)

!`cat "...synthesis/mechanisms.json"`

## Current Tensions (update with new evidence)

!`cat "...synthesis/tensions.json"`

## Current Contingencies (update with new evidence)

!`cat "...synthesis/contingencies.json"`

## Specimen Registry (for cross-referencing)

!`cat "...specimens/registry.json"`

$ARGUMENTS
```

**Step 2: Verify the slash command file is valid YAML frontmatter + markdown**

Check that:
- `---` delimiters are correct
- `disable-model-invocation: true` is present
- All `!` bang-includes use absolute paths matching the project location
- `$ARGUMENTS` is at the end

---

### Task 3: Add synthesis quality checks to `scripts/validate-workflow.js`

**Files:**
- Modify: `scripts/validate-workflow.js`

**Step 1: Add a new Section 11: Synthesis Quality**

After the existing Section 10 (Curation Quality), add checks for:

```javascript
// ── 11. Synthesis Quality ──
section('11. Synthesis Quality');

// Check: mechanisms.json evidence entries reference real specimens
const mechanismsPath = path.join(SYNTHESIS_DIR, 'mechanisms.json');
const mechanismsData = loadJSON(mechanismsPath);
if (mechanismsData) {
  let orphanedEvidence = 0;
  let duplicateSpecimens = 0;

  for (const mech of [...(mechanismsData.confirmed || []), ...(mechanismsData.candidates || [])]) {
    // Check for duplicate specimen IDs
    const specIds = mech.specimens || [];
    const uniqueIds = new Set(specIds);
    if (uniqueIds.size !== specIds.length) {
      warn(`Mechanism ${mech.id} "${mech.name}": duplicate specimen IDs in specimens array`);
      duplicateSpecimens++;
    }

    // Check evidence references real specimens
    for (const ev of (mech.evidence || [])) {
      if (ev.specimenId && !registryIds.has(ev.specimenId)) {
        warn(`Mechanism ${mech.id} "${mech.name}": evidence references unknown specimen "${ev.specimenId}"`);
        orphanedEvidence++;
      }
    }

    // Check specimens array matches evidence
    for (const specId of specIds) {
      if (!registryIds.has(specId)) {
        warn(`Mechanism ${mech.id} "${mech.name}": specimens array references unknown specimen "${specId}"`);
      }
    }
  }

  if (orphanedEvidence === 0 && duplicateSpecimens === 0) {
    ok('All mechanism evidence references valid specimens');
  }
}

// Check: tensions.json specimen references
const tensionsPath = path.join(SYNTHESIS_DIR, 'tensions.json');
const tensionsData = loadJSON(tensionsPath);
if (tensionsData) {
  let emptyTensions = 0;
  for (const t of (tensionsData.tensions || [])) {
    if (!t.specimens || t.specimens.length === 0) {
      warn(`Tension "${t.name}": no specimens linked`);
      emptyTensions++;
    }
  }
  if (emptyTensions === 0) {
    ok('All tensions have specimen links');
  }
}

// Check: contingencies.json specimen references
const contingenciesPath = path.join(SYNTHESIS_DIR, 'contingencies.json');
const contingenciesData = loadJSON(contingenciesPath);
if (contingenciesData) {
  let emptyContingencies = 0;
  for (const c of (contingenciesData.contingencies || [])) {
    const highSpecs = (c.high && c.high.specimens) ? c.high.specimens.length : 0;
    const lowSpecs = (c.low && c.low.specimens) ? c.low.specimens.length : 0;
    if (highSpecs + lowSpecs === 0) {
      warn(`Contingency "${c.name}": no specimens linked on either end`);
      emptyContingencies++;
    }
  }
  if (emptyContingencies === 0) {
    ok('All contingencies have specimen links');
  }
}

// Check: synthesis queue staleness
if (synthQueue) {
  const pendingCount = (synthQueue.queue || []).filter(q => q.status === 'pending').length;
  const synthesizedCount = (synthQueue.queue || []).filter(q => q.status === 'synthesized').length;
  ok(`Synthesis queue: ${synthesizedCount} synthesized, ${pendingCount} pending`);
  if (synthQueue.lastSynthesisDate === null && synthesizedCount === 0) {
    warn('Synthesis has never been run (lastSynthesisDate is null)');
  }
}
```

NOTE: The `registryIds` set needs to be built earlier in the script (or reused from existing Section 5/10 logic). Check what's available and adapt.

**Step 2: Run the validator to confirm the new section works**

```bash
node scripts/validate-workflow.js
```

Expected: Should show the new Section 11 with warnings about empty tensions/contingencies (since synthesis hasn't been run yet) and a warning about lastSynthesisDate being null.

---

### Task 4: Remove stale references from SKILL.md

**Files:**
- Modify: `skills/ambidexterity-synthesis/SKILL.md`

**Step 1: Fix the broken reference file pointers**

Lines 61-62 of the synthesis SKILL.md reference files that don't exist:
```
See `references/mechanisms-current.md` for detailed mechanism descriptions with evidence.
See `references/tensions-contingencies.md` for tensions and contingencies framework.
```

These files don't exist and aren't needed — the protocol + the JSON data files serve this purpose. Replace with:
```
See `synthesis/mechanisms.json` for current mechanism definitions with evidence.
See `synthesis/tensions.json` and `synthesis/contingencies.json` for tensions and contingencies data.
```

---

### Task 5: Add protocol reference to `skills/ambidexterity-synthesis/SKILL.md`

**Files:**
- Modify: `skills/ambidexterity-synthesis/SKILL.md`

**Step 1: Add a "Session Protocol" section after the Purpose section**

Following the pattern applied to the curation skill, add after the `## Inputs` section:

```markdown
## Session Protocol

For step-by-step execution instructions, follow:

**`synthesis/SYNTHESIS-PROTOCOL.md`**

This file (SKILL.md) defines WHAT to look for and HOW to classify patterns. The protocol defines HOW to run a synthesis session end-to-end.
```

---

### Task 6: Run validator and verify end-to-end

**Files:**
- Reference: `scripts/validate-workflow.js`

**Step 1: Run the validator**

```bash
node scripts/validate-workflow.js
```

Expected output should include:
- Section 11: Synthesis Quality checks
- Warnings for empty tensions/contingencies (expected — synthesis hasn't run yet)
- Warning for lastSynthesisDate null (expected)
- 0 errors

**Step 2: Verify the slash command file can be read**

```bash
cat ".claude/skills/synthesize/SKILL.md"
```

Confirm it has valid YAML frontmatter and all bang-includes point to real files.

**Step 3: Confirm synthesis is ready for first run**

Check that:
- `synthesis/SYNTHESIS-PROTOCOL.md` exists and is >200 lines
- `.claude/skills/synthesize/SKILL.md` injects the protocol + all data files
- `synthesis/sessions/` directory exists (has `.gitkeep`)
- `curation/synthesis-queue.json` has 23 pending specimens
- `synthesis/mechanisms.json`, `tensions.json`, `contingencies.json` are valid JSON

The user can then run `/synthesize` in a new Claude Code session to execute the first synthesis pass.
