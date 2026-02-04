# Robust /curate Command Implementation Plan

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Build a deterministic, repeatable CURATION-PROTOCOL.md (like SESSION-PROTOCOL.md for research) and wire it into the `/curate` slash command so any future research sessions can be curated without a custom plan.

**Architecture:** Create `curation/CURATION-PROTOCOL.md` as the step-by-step runbook. Update `.claude/skills/curate/SKILL.md` to inject it. Add curation-specific validator checks. The protocol handles: reading the queue, processing each org (new vs existing vs evolution), classification via decision tree, stratigraphy, provenance, and all registry/queue updates.

**Tech Stack:** Markdown protocol doc, JSON specimen files, Node.js validator

---

### Task 1: Create CURATION-PROTOCOL.md

**Files:**
- Create: `curation/CURATION-PROTOCOL.md`

**Step 1: Write the protocol**

Create the file with the full content below. This mirrors SESSION-PROTOCOL.md's structure: core question, idempotency rules, quality test, pre-session setup, step-by-step processing, session wrap-up.

```markdown
# Curation Protocol

## Core Research Question

Every classification decision must serve this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

If a finding doesn't illuminate structural arrangements, tensions, or mechanisms related to this question, it shouldn't drive classification decisions.

---

## Idempotency Rules

- **Never modify a previous curation session file.** Each curation session creates a new file in `curation/sessions/`.
- **Never overwrite existing specimen layers.** New findings add new layers at the TOP of the `layers` array. Old layers are never deleted or modified (stratigraphy).
- **Check the queue before processing.** Only process sessions with `"status": "pending"` in `research/queue.json`. Skip anything already curated.
- **Check the registry before creating.** Before creating a new specimen, search `specimens/registry.json` for the org. If it exists, UPDATE (add layer) rather than CREATE.
- **One source of truth per field.** If new data contradicts old data, add the new data as a new layer with explanation — don't silently overwrite.

---

## Pre-Session Setup

Before processing anything:

- [ ] Read `research/queue.json` — identify all sessions with `"status": "pending"`
- [ ] Read `specimens/registry.json` — load the full specimen list so you know which orgs already exist
- [ ] Read `specimens/specimen-schema.json` — confirm you know the exact JSON structure
- [ ] Read `specimens/_template.json` — use this as the starting point for new specimens
- [ ] Read `skills/ambidexterity-curation/references/classification-quick-ref.md` — have the taxonomy fresh
- [ ] Read `skills/ambidexterity-curation/references/type-specimens.md` — know the reference examples
- [ ] Record the list of pending sessions and their total org count in your curation session file frontmatter

---

## Processing Loop

For each pending session in `research/queue.json`:

### Step 1: Read the Session File

Read `research/sessions/{sessionFile}`. Parse the YAML frontmatter to get `organizations_found` (list of org IDs and their status: new/existing/evolution).

### Step 2: Process Each Organization

For each org in the session, follow this decision:

```
Is the org already in specimens/registry.json?
├── NO → Go to "Create New Specimen" (below)
├── YES, status = "existing" → Go to "Add Layer to Existing Specimen"
└── YES, status = "evolution" → Go to "Add Evolution Layer"
```

---

## Create New Specimen

### A. Start from Template

Copy `specimens/_template.json` as the starting structure. Set:
- `id`: URL-safe slug from the session (e.g., "intercom", "wells-fargo")
- `name`: Display name (e.g., "Intercom", "Wells Fargo")
- `title`: Short descriptive phrase about their AI structure (e.g., "72-Hour AI Pivot", "Consumer Banking Leader as AI Head")
- `meta.created`: today's date (YYYY-MM-DD)
- `meta.lastUpdated`: today's date
- `meta.status`: "Active" if multiple sources or deep data; "Stub" if single thin source
- `meta.completeness`: assess honestly (see Completeness Guide below)

### B. Classify Using Decision Tree

Follow the classification decision tree in `skills/ambidexterity-curation/SKILL.md` Steps 2-3. For every classification:

1. **Walk the decision tree explicitly** — start at "Is there a formal AI unit?" and follow the branches
2. **Assign confidence**: High = multiple confirming sources; Medium = reasonable from available data; Low = best guess from limited data
3. **Write a classificationRationale** for EVERY specimen with Medium or Low confidence — explain what data drove the decision and what's missing
4. **Check for secondary model** — many orgs combine models (e.g., "Model 1 + Model 5b"). If you see a clear secondary, record it.
5. **Assign orientation** using the orientation table in SKILL.md Step 3

### C. Build the Specimen Content

Working through each section of the schema:

**`description`**: Write 2-3 paragraphs describing HOW this org structures AI exploration and execution. Be specific — names, units, reporting lines. Draw ONLY from facts in the session file. Do not invent or infer beyond what's sourced.

**`habitat`**: Fill in what's known — industry, sector, orgSize, employees, revenue, headquarters, geography. Use null for anything not in the data. Don't guess.

**`observableMarkers`**: Fill in what the session data reveals about reporting structure, resource allocation, time horizons, decision rights, metrics. Use null for unknowns.

**`mechanisms`**: Review the 10 mechanisms (listed in classification-quick-ref.md). For each mechanism the org demonstrates:
- Record the mechanism id, name, evidence (specific, sourced), and strength (Strong/Moderate/Emerging)
- Only include mechanisms with actual evidence — don't force-fit

**`quotes`**: Copy VERBATIM from the session file. Include speaker, speakerTitle, source, sourceUrl, timestamp, date. Never paraphrase quotes.

**`layers`**: Create a single initial layer:
```json
{
  "date": "YYYY-MM",  // when the org REVEALED this state, not when we collected it
  "label": "Initial Documentation",
  "summary": "Brief description of what this layer captures",
  "classification": null,  // only set if different from current classification
  "sourceRefs": ["source-id-1", "source-id-2"]  // references to items in the sources array
}
```

**`sources`**: Create an entry for EVERY source referenced in the session's provenance table for this org. Each source MUST have:
- `id`: descriptive slug (e.g., "cheeky-pint-dario-2025", "ubs-press-release-2025")
- `type`: match the session's source type column
- `name`: full source name
- `url`: from session's provenance table — **never null if the session provides a URL**
- `sourceDate`: when the info was published/revealed
- `collectedDate`: today's date
- `timestamp`: from session if audio/video source

**`contingencies`**: Assess the 5 contingency variables if data supports it. Use null when insufficient data. Don't guess.

**`tensionPositions`**: Score -1.0 to +1.0 on each tension axis where data exists. Use null when insufficient. Include rationale in taxonomyFeedback if scores are non-obvious.

**`openQuestions`**: Copy from session's "Open Questions" section for this org.

**`taxonomyFeedback`**: Note any of:
- Edge cases where the org doesn't fit the taxonomy cleanly
- Patterns the taxonomy doesn't capture
- Potential type specimen candidacy
- Reclassification considerations

### D. Save the Specimen

Write to `specimens/{id}.json`. Validate:
```bash
node -e "JSON.parse(require('fs').readFileSync('specimens/{id}.json','utf8')); console.log('Valid JSON')"
```

---

## Add Layer to Existing Specimen

When an org already exists and the session has NEW findings (status: "existing"):

### A. Read the Existing Specimen

Read `specimens/{id}.json`. Understand the current classification, layers, and sources.

### B. Create a New Layer

Add a new layer at the TOP of the `layers` array (most recent first):
```json
{
  "date": "YYYY-MM",   // when the org revealed this info
  "label": "Descriptive label for this layer",
  "summary": "What new information this layer adds",
  "classification": null,
  "sourceRefs": ["new-source-id-1"]
}
```

### C. Add New Sources

Append new source entries to the `sources` array. Never duplicate existing sources — check by URL.

### D. Add New Quotes

Append new quotes to the `quotes` array. Check for duplicates by quote text.

### E. Update Enrichable Fields

Update fields that were previously null if the new data fills them:
- `habitat` fields (employees, revenue, headquarters, etc.)
- `observableMarkers` fields
- `contingencies` fields
- `tensionPositions` fields
- Add new `mechanisms` entries (don't remove existing ones)
- Add to `openQuestions` (don't remove answered ones — move them to description or markers instead)

### F. Consider Reclassification

Review whether the new data changes the classification. If it does:
- Update `classification` fields
- Set the OLD classification in the new layer's `classification` field (so the layer records what changed)
- Update `classificationRationale` to explain the change
- Note the reclassification in `taxonomyFeedback`

### G. Update Meta

- `meta.lastUpdated`: today's date
- `meta.completeness`: reassess (may improve from Low → Medium if new sources added)
- Do NOT change `meta.created`

### H. Save and Validate

---

## Add Evolution Layer

When the session explicitly flags structural EVOLUTION (status: "evolution"):

Follow all steps in "Add Layer to Existing Specimen" above, plus:

### Additional Steps for Evolution

1. **The new layer's `classification` field** should record the PREVIOUS classification (before evolution)
2. **Update the specimen's current `classification`** to reflect the NEW state
3. **The layer `summary`** should explicitly describe old → new: "Evolved from [old state] to [new state]: [what changed and why]"
4. **Update `description`** to reflect the current (evolved) state, while the layers preserve history
5. **Note the evolution pattern** in `taxonomyFeedback` — evolutions are valuable data about how structures change over time

---

## Completeness Guide

| Level | Criteria |
|-------|----------|
| **High** | 3+ independent sources with URLs, mechanisms documented with evidence, verbatim quotes with attribution, observable markers filled, classification at High confidence |
| **Medium** | 2+ sources with URLs, core structure understood, some gaps in markers/mechanisms, classification at Medium+ confidence |
| **Low** | 1-2 sources, basic structure identified, many null fields, limited evidence |
| **Stub** | Single thin source, minimal structural detail, mostly open questions |

Use "Stub" for `meta.status` when the specimen is so thin it's essentially a placeholder. Use "Active" otherwise.

---

## Quality Review

Before wrapping up the curation session, review ALL processed specimens:

- [ ] Does every source in every specimen have a URL (or explicit `[paywall]`/`[no URL]` note)?
- [ ] Are all quotes verbatim with full attribution (speaker, title, source, URL, date)?
- [ ] Does every classification have a rationale (especially Medium/Low confidence)?
- [ ] Does every new layer have `sourceRefs` that match actual source IDs in the specimen?
- [ ] Were evolution flags handled correctly (old classification in layer, new in specimen)?
- [ ] Are `meta.completeness` and `meta.status` honest assessments?
- [ ] Was the classification decision tree actually walked (not just pattern-matched from the session's own annotations)?

---

## Session Wrap-Up

After ALL pending sessions are processed:

- [ ] **Update `specimens/registry.json`**:
  - Add entries for new specimens
  - Update `lastUpdated`, `layerCount`, `completeness`, `confidence` for modified specimens
  - Recalculate `totalSpecimens`, `byModel`, `byOrientation` aggregates
  - Add any new type specimens to `typeSpecimens` array

- [ ] **Update `research/queue.json`**:
  - Set `"status": "curated"` and `"curatedIn": "{session-filename}"` for each processed session

- [ ] **Update `curation/synthesis-queue.json`**:
  - Add an entry for every specimen that was created or updated:
    ```json
    {
      "specimenId": "org-id",
      "addedDate": "YYYY-MM-DD",
      "reason": "New specimen" | "Updated with new layer" | "Reclassified",
      "status": "pending"
    }
    ```
  - Update `lastUpdated`

- [ ] **Write curation session log** at `curation/sessions/YYYY-MM-DD-curation.md`:
  ```markdown
  ---
  session_date: "YYYY-MM-DD"
  sessions_processed: ["session-file-1.md", "session-file-2.md"]
  specimens_created: ["org-1", "org-2"]
  specimens_updated: ["org-3", "org-4"]
  specimens_reclassified: ["org-5"]
  ---

  # Curation Session: YYYY-MM-DD

  ## Summary
  Processed N research sessions containing M organization references.
  Created X new specimens. Updated Y existing specimens. Reclassified Z specimens.

  ## Specimens Created/Updated
  | Organization | Action | Model | Orientation | Confidence | Completeness | Notes |
  |---|---|---|---|---|---|---|
  | [org] | Created/Updated/Reclassified | [model] | [orientation] | [H/M/L] | [H/M/L/Stub] | [notes] |

  ## Reclassifications
  | Organization | Old Classification | New Classification | Rationale |
  |---|---|---|---|

  ## Taxonomy Feedback
  [Edge cases, patterns that don't fit, suggested revisions, type specimen candidates]

  ## Type Specimens Identified
  [Any specimens marked as especially clear examples]

  ## Edge Cases
  [Organizations that were difficult to classify and why]

  ## Sessions Processed
  [List of research session files processed]
  ```

- [ ] **Run validator**:
  ```bash
  node scripts/validate-workflow.js
  ```
  Fix any issues before completing.

---

## Curation Session File Frontmatter

```yaml
---
session_date: "YYYY-MM-DD"
sessions_processed: ["session-file-1.md"]
specimens_created: ["org-1", "org-2"]
specimens_updated: ["org-3"]
specimens_reclassified: []
---
```
```

**Step 2: Verify the file was created correctly**

Read back the file to confirm it saved properly and the markdown formatting is intact.

---

### Task 2: Update the /curate Slash Command

**Files:**
- Modify: `.claude/skills/curate/SKILL.md`

**Step 1: Rewrite the slash command to inject the protocol**

Replace the entire contents of `.claude/skills/curate/SKILL.md` with:

```markdown
---
name: curate
description: "Phase 2: Curate pending research findings into structured specimen cards with classification, layers, and provenance"
disable-model-invocation: true
---

# Phase 2: Curation Session

You are curating raw research findings into structured specimen cards for the Ambidexterity Field Guide.

## Core Research Question

Every classification decision must serve this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

## Curation Protocol

Follow this protocol step by step. Do NOT skip steps.

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/curation/CURATION-PROTOCOL.md"`

## Classification Rules, Taxonomy, and Stratigraphy

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/skills/ambidexterity-curation/SKILL.md"`

## Specimen Schema (structure of specimen JSON files)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/specimen-schema.json"`

## Specimen Template (starting point for new specimens)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/_template.json"`

## Classification Quick Reference

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/skills/ambidexterity-curation/references/classification-quick-ref.md"`

## Type Specimens (reference examples for each model)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/skills/ambidexterity-curation/references/type-specimens.md"`

## Curation Queue (pending research sessions to process)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/queue.json"`

## Specimen Registry (existing specimens — check before creating new ones)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/registry.json"`

## Synthesis Queue (add curated specimens here for Phase 3)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/curation/synthesis-queue.json"`

$ARGUMENTS
```

Key changes from the old version:
1. **CURATION-PROTOCOL.md is injected first** — the deterministic runbook
2. **Specimen template is injected** — so new specimens start from the right structure
3. **Full registry is injected** (not `head -60`) — needed to check all existing orgs
4. **Synthesis queue is injected** — so the agent can update it
5. **No hardcoded 7-step task list** — the protocol IS the task list
6. **Protocol comes before SKILL.md** — protocol says HOW, SKILL says WHAT (taxonomy details)

---

### Task 3: Add Curation Validator Checks

**Files:**
- Modify: `scripts/validate-workflow.js`

**Step 1: Read the current validator**

Read `scripts/validate-workflow.js` to find where to add curation checks. Look for the existing section structure (sections 1-9).

**Step 2: Add Section 10 — Curation Quality**

Add a new section after the existing ones that checks:

```javascript
// Section 10: Curation Quality
section('10. Curation Quality');

// Check: specimens with null source URLs
const specimenFiles = fs.readdirSync(SPECIMENS_DIR)
  .filter(f => f.endsWith('.json') && f !== 'registry.json' && f !== 'source-registry.json' && f !== 'specimen-schema.json' && f !== '_template.json');

let nullUrlCount = 0;
let noRationaleCount = 0;
let emptyLayersCount = 0;
let truncatedQuotesCount = 0;

for (const file of specimenFiles) {
  const specimen = JSON.parse(fs.readFileSync(path.join(SPECIMENS_DIR, file), 'utf8'));

  // Check source URLs
  const nullUrls = (specimen.sources || []).filter(s => !s.url && !s.notes?.includes('[paywall]') && !s.notes?.includes('[no URL]'));
  if (nullUrls.length > 0) {
    warn(`${file}: ${nullUrls.length} source(s) with null URL and no [paywall]/[no URL] note`);
    nullUrlCount += nullUrls.length;
  }

  // Check classification rationale for Medium/Low confidence
  if (specimen.classification?.confidence !== 'High' && !specimen.classification?.classificationRationale) {
    warn(`${file}: ${specimen.classification?.confidence} confidence but no classificationRationale`);
    noRationaleCount++;
  }

  // Check empty layers
  if (!specimen.layers || specimen.layers.length === 0) {
    warn(`${file}: no layers (every specimen needs at least one)`);
    emptyLayersCount++;
  }

  // Check truncated quotes (quotes that end abruptly)
  for (const q of (specimen.quotes || [])) {
    if (q.text && q.text.length < 20 && !q.text.endsWith('.') && !q.text.endsWith('!') && !q.text.endsWith('?') && !q.text.endsWith('"')) {
      warn(`${file}: possibly truncated quote "${q.text.substring(0, 30)}..."`);
      truncatedQuotesCount++;
    }
  }
}

if (nullUrlCount === 0) ok('All specimen sources have URLs or explicit [paywall]/[no URL] notes');
if (noRationaleCount === 0) ok('All Medium/Low confidence specimens have classification rationale');
if (emptyLayersCount === 0) ok('All specimens have at least one layer');
if (truncatedQuotesCount === 0) ok('No truncated quotes detected');

// Check: synthesis queue has entries for recently curated specimens
const synthQueuePath = path.join(BASE, 'curation', 'synthesis-queue.json');
if (fs.existsSync(synthQueuePath)) {
  const synthQueue = JSON.parse(fs.readFileSync(synthQueuePath, 'utf8'));
  const pendingSynth = (synthQueue.queue || []).filter(q => q.status === 'pending');
  ok(`Synthesis queue: ${pendingSynth.length} specimens pending synthesis`);
}
```

**Step 3: Run the validator to confirm it works**

Run: `node scripts/validate-workflow.js`

Expected: Will show warnings for existing specimens (many have null URLs, no rationale, truncated quotes from the auto-conversion). This is expected — the warnings surface the tech debt in existing specimens.

---

### Task 4: Create curation/sessions/ Directory

**Files:**
- Create: `curation/sessions/.gitkeep`

**Step 1: Create the directory**

```bash
mkdir -p "curation/sessions"
touch "curation/sessions/.gitkeep"
```

This ensures the directory exists for curation session logs.

---

### Task 5: Update SKILL.md to Reference the Protocol

**Files:**
- Modify: `skills/ambidexterity-curation/SKILL.md`

**Step 1: Add protocol reference at the top of the SKILL**

Add after line 10 (after the Purpose section), before "## Inputs":

```markdown
## Session Protocol

For step-by-step execution instructions, follow:
**`curation/CURATION-PROTOCOL.md`**

This file (SKILL.md) defines WHAT to look for and HOW to classify. The protocol defines HOW to run a curation session end-to-end.
```

This mirrors what we did for the research SKILL.md — it points to the protocol for the HOW.

---

### Task 6: Validate End-to-End and Commit

**Step 1: Run the validator**

```bash
node scripts/validate-workflow.js
```

Confirm no errors (warnings about existing specimen quality are expected and OK).

**Step 2: Verify /curate command loads correctly**

Check that `.claude/skills/curate/SKILL.md` has the right bang-includes and would inject all needed context.

**Step 3: Commit**

```bash
git add curation/CURATION-PROTOCOL.md .claude/skills/curate/SKILL.md scripts/validate-workflow.js skills/ambidexterity-curation/SKILL.md curation/sessions/.gitkeep
git commit -m "feat: add CURATION-PROTOCOL.md and wire into /curate command

Creates deterministic curation runbook (mirrors SESSION-PROTOCOL.md):
- Idempotency rules, classification decision tree walkthrough
- Create/Update/Evolution specimen processing
- Quality review checklist and completeness guide
- Session wrap-up with registry/queue updates

Updates /curate slash command to inject protocol first.
Adds curation quality checks to validator."
```

---

## What This Delivers

After executing this plan:

1. **`/curate` becomes a robust, repeatable command** — any agent invoking it gets the full protocol + taxonomy + schema + current state
2. **The protocol is deterministic** — it specifies exactly how to walk the decision tree, when to create vs. update, how to handle evolutions, and what quality checks to pass
3. **It's idempotent** — only processes pending sessions, never overwrites old layers, checks registry before creating
4. **It's self-validating** — the validator catches missing URLs, missing rationale, empty layers, and truncated quotes
5. **The next time you run `/research` and then `/curate`**, the curate command will automatically pick up whatever's pending and process it correctly
