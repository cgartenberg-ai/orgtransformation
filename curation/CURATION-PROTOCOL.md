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

## Batching and Resume

Large sessions risk running out of context before all specimens are processed. The protocol handles this automatically:

### Batch Size Limit

- **Maximum 10-12 specimens per pending session.** If a research session has more, split it into multiple session files (e.g., `session-batch1.md`, `session-batch2.md`) and add each as a separate entry in `research/queue.json`.
- Each batch is an independent queue entry with its own `"status": "pending"` → `"curated"` lifecycle.

### Per-Specimen Progress Tracking

As you process each specimen within a session, **immediately update the session's YAML frontmatter** to mark it done:

```yaml
organizations_found:
  - id: google-x
    status: existing
    curated: true          # ← add this after processing
  - id: bank-of-america
    status: existing
                            # ← no curated flag = not yet processed
```

This way, if the session is interrupted:
1. The session stays `"pending"` in `research/queue.json` (wrap-up never ran)
2. Next `/curate` run reads the same session, sees which orgs have `curated: true`, and **skips them**
3. Processing resumes from the first org without `curated: true`

### Session Completion

A session is only marked `"curated"` in `research/queue.json` during Session Wrap-Up, after ALL its organizations have `curated: true`. If wrap-up doesn't run (context exhaustion), the session remains pending and the next run picks up where it left off.

### One Session Per Run (Default)

Process pending sessions **one at a time**, in queue order. Complete all organisms in one session (or as many as context allows) before moving to the next. This ensures partial progress is always saved to the current session file.

---

## Parallel Curation with Overlapping Specimens

When multiple research sessions are pending and the operator wants to process them in parallel (e.g., launching multiple agents), **overlapping specimens are a data-loss risk**. If two agents write to the same specimen file concurrently, last-writer-wins and the earlier agent's changes are lost.

### Pre-Flight: Overlap Detection

Before launching parallel curation agents, the **coordinator** (the main session) must:

1. **Read all pending session files** and extract the `organizations_found` list from each
2. **Build an org-to-sessions map** — for each org ID, list which sessions reference it
3. **Identify overlapping orgs** — any org appearing in 2+ sessions

Example:
```
meta-ai:      [session-001, session-002, session-003]  ← OVERLAP
microsoft:    [session-001, session-003]                ← OVERLAP
salesforce:   [session-003]                             ← no overlap
travelers:    [session-004]                             ← no overlap
```

### Assignment Rules

For each overlapping org, the coordinator assigns it to **exactly one session** using this priority:

1. **Richest data** — assign to the session with the most substantive findings for that org (most sources, deepest structural detail, evolution events)
2. **Evolution over addition** — if one session flags the org as "evolution" and another as "existing", the evolution session gets ownership
3. **Tie-break: later session wins** — if data richness is comparable, assign to the chronologically later session (it likely has the most recent data)

The coordinator then:
- **Marks the org as `skip: true`** in all non-owning sessions' processing instructions
- **Annotates the owning session** with a note listing the additional sources from skipped sessions that should be incorporated:

```yaml
# Example annotation for the owning agent
overlap_assignments:
  meta-ai:
    owner: session-002
    additional_sources_from:
      - session-001: "Reality Labs 1,500 cuts, Stratechery Meta Compute pivot"
      - session-003: "Q4 2025 earnings: $164.5B revenue, $65B capex, 72K employees"
```

### Agent Instructions

Each parallel agent receives:
- Its assigned session file
- The overlap assignment map
- For orgs it owns: a list of additional data from other sessions to incorporate
- For orgs it should skip: clear `skip: true` flags

Agents **must**:
- Skip any org marked `skip: true` — do not read or write that specimen
- For owned overlapping orgs: incorporate data from all sessions (not just their primary session)
- Write to specimen files only for orgs they own

### Fallback: Sequential Processing

If overlap detection is skipped or fails, fall back to sequential processing (one session at a time). This is always safe because each session reads the specimen file fresh, sees previous sessions' layers, and appends correctly.

### Post-Parallel Reconciliation

After all parallel agents complete, the coordinator should:

1. **Verify overlapping specimens** — read each overlapping specimen file, confirm it contains data from ALL sessions that referenced it
2. **Patch any gaps** — if an agent failed or missed data from a non-primary session, manually add the missing layers/sources/quotes
3. **Check for write conflicts** — if file timestamps suggest multiple agents wrote the same file, manually merge

This reconciliation step is required whenever parallel agents were used. Skip it only if all orgs were non-overlapping.

---

## Processing Loop

For each pending session in `research/queue.json` (one at a time):

### Step 1: Read the Session File

Read `research/sessions/{sessionFile}`. Parse the YAML frontmatter to get `organizations_found` (list of org IDs and their status: new/existing/evolution). **Skip any org that already has `curated: true`** — it was processed in a previous run.

### Step 2: Process Each Organization

For each unprocessed org in the session, follow this decision:

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

Follow the classification decision tree in `skills/ambidexterity-curation/SKILL.md` Steps 2-3. **After walking the decision tree, run all 8 Classification Guardrails from SKILL.md before finalizing the classification.** Guardrails catch common misclassification patterns (M7 permanence trap, M1 prestige bias, temporal vs. one-time pivot, etc.).

For every classification:

1. **Walk the decision tree explicitly** — start at "Is there a formal AI unit?" and follow the branches. **Record the path taken** (e.g., "Formal unit=YES → Publishes research=NO → Central team=YES → Builds+Enables → M4"). This reasoning goes into (a) the specimen's `classificationRationale` field and (b) the session log's "Classification Reasoning" table.
2. **Run all 8 guardrails** and note which were triggered. Even "guardrail checked, not triggered" is useful — it shows the classification was tested.
3. **Assign confidence**: High = multiple confirming sources; Medium = reasonable from available data; Low = best guess from limited data
4. **Write a classificationRationale** for EVERY specimen with Medium or Low confidence — explain what data drove the decision and what's missing
5. **Check for secondary model** — many orgs combine models (e.g., "Model 1 + Model 5b"). If you see a clear secondary, record it.
6. **Assign orientation** using the orientation table in SKILL.md Step 3
7. **Note cross-cutting observations** — if you see the same classification pattern across multiple specimens in this batch, flag it for the session log's "Cross-Cutting Patterns" section. These are analytically valuable.

### C. Build the Specimen Content

Working through each section of the schema:

**`description`**: Write 2-3 paragraphs describing HOW this org structures AI exploration and execution. Be specific — names, units, reporting lines. Draw ONLY from facts in the session file. Do not invent or infer beyond what's sourced.

**`habitat`**: Fill in what's known — industry, sector, orgSize, employees, revenue, headquarters, geography. Use null for anything not in the data. Don't guess.

**`observableMarkers`**: Fill in what the session data reveals about reporting structure, resource allocation, time horizons, decision rights, metrics. Use null for unknowns.

**Source attribution**: All factual claims in observable markers and description text should include inline `[source-id]` citations matching entries in the specimen's `sources` array. Example: `"AI VP reports to SVP Software Engineering [apple-ai-reorg-2025]. Team of 200+ engineers [apple-cook-push-2025]."` The app renders these as superscript numbered links.

**Metrics guidance**: The `metrics` field should capture which specific KPIs and targets the organization publicly announces it tracks or optimizes for in the AI context. Include: (a) KPIs explicitly named by leaders (e.g., "AI adoption rate", "cost per AI interaction"), (b) targets with numbers and timeframes (e.g., "30% automation by 2026"), (c) the framing used (productivity, revenue growth, cost reduction, capability). Each metric claim should include a `[source-id]` citation. Example: `"AI adoption rate across business units (target: 80% by Q4 2026) [earnings-q3-2025]. Cost per customer interaction reduced 40% via Agentforce [salesforce-agentforce-launch]."`

**`mechanisms`**: Review the 10 mechanisms (listed in classification-quick-ref.md). For each mechanism the org demonstrates:
- Record the mechanism id, name, evidence (specific, sourced), and strength (Strong/Moderate/Emerging)
- Only include mechanisms with actual evidence — don't force-fit

**`quotes`**: Copy VERBATIM from the session file. Include speaker, speakerTitle, source, sourceUrl, timestamp, date. Never paraphrase quotes.

**`layers`**: Create a single initial layer:
```json
{
  "date": "YYYY-MM",
  "label": "Initial Documentation",
  "summary": "Brief description of what this layer captures",
  "classification": null,
  "sourceRefs": ["source-id-1", "source-id-2"]
}
```
The `date` field is when the org REVEALED this state, not when we collected it.

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

### E. Mark Progress

After saving the specimen, **immediately** update the session file's YAML frontmatter to add `curated: true` to this org's entry. This ensures progress is saved even if the run is interrupted before wrap-up.

---

## Add Layer to Existing Specimen

When an org already exists and the session has NEW findings (status: "existing"):

### A. Read the Existing Specimen

Read `specimens/{id}.json`. Understand the current classification, layers, and sources.

### B. Create a New Layer

Add a new layer at the TOP of the `layers` array (most recent first):
```json
{
  "date": "YYYY-MM",
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

### I. Mark Progress

After saving, **immediately** update the session file's YAML frontmatter to add `curated: true` to this org's entry.

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

## Out-of-Band Changes (Taxonomy Audits, Manual Edits)

When specimens are modified outside the normal `/curate` pipeline (e.g., taxonomy audits, manual reclassifications, bulk tagging), the synthesis queue will NOT be updated automatically. After any out-of-band specimen edits:

1. **Add entries to `curation/synthesis-queue.json`** for every modified specimen, with `"curatedIn"` referencing the audit/edit context (e.g., `"taxonomy-audit-2026-02-02"`)
2. **Update `specimens/registry.json`** with new model counts, orientations, type specimens
3. **Run `node scripts/validate-workflow.js`** to confirm consistency

This ensures the next `/synthesize` run picks up all changes regardless of how they were made.

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

After ALL organizations in the current session have `curated: true` (check the YAML frontmatter), perform wrap-up for that session. If there are more pending sessions and context allows, continue to the next one. If context is running low, stop — remaining pending sessions will be picked up in the next `/curate` run.

For each completed session:

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

- [ ] **Sync `research/purpose-claims/scan-tracker.json`**:
  - Add entries for any new specimens created during this curation session:
    ```json
    {
      "specimenId": "org-id",
      "lastScanned": null,
      "claimsFound": 0,
      "quality": "unscanned"
    }
    ```
  - Verify total entry count matches `specimens/registry.json` totalSpecimens
  - This keeps Track 2 (purpose claims) in sync with Track 1 specimen creation

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

  ## Classification Reasoning
  For each specimen, document the decision tree walk and guardrail checks:
  - Which decision tree path was followed (formal AI unit? → publishes research? → etc.)
  - Which guardrails were triggered and their outcome
  - What alternative classifications were considered and why they were rejected
  - For reclassifications: what new evidence changed the classification

  | Organization | Old → New | Decision Tree Path | Guardrails Applied | Key Evidence |
  |---|---|---|---|---|
  | [org] | [M6→M4] | [Formal unit=YES → Research=NO → Central team=YES → Builds+Enables=YES → M4] | [G2: Federation confirmed] | [specific evidence] |

  ## Reclassifications
  | Organization | Old Classification | New Classification | Rationale |
  |---|---|---|---|

  ## Cross-Cutting Patterns
  Observations that span multiple specimens in this batch — these are the analytical gold:
  - [Pattern 1: e.g., "All M6 specimens from thin data were wrong after enrichment"]
  - [Pattern 2: e.g., "Acqui-hire-to-CTO pipeline appears in 2+ specimens"]
  These observations feed directly into insights.json and the field journal.

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
