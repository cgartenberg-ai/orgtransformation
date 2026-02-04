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
- [ ] Read `synthesis/insights.json` — load current cross-cutting insights. Note maturity levels and which specimens are already cited. **Remember: insights are NEVER deleted.**
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
3. **Skip stubs for mechanism/tension/contingency analysis** if they have insufficient data (meta.completeness = "Stub" AND no mechanisms, no quotes, no filled observableMarkers). Still mark them synthesized, but note "insufficient data for synthesis" in session log.

### Step 2: Mechanism Analysis (for each non-stub specimen)

Walk through all confirmed mechanisms + candidates. For each:

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

### Step 3: Tension Analysis (for each non-stub specimen)

Walk through all tensions. For each:

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

The `position` value maps to the tension's poles:
- **Negative values (-1.0 to -0.1)**: Lean toward the `whenNegative` pole (e.g., separation, deep pilots, centralization)
- **Positive values (0.1 to 1.0)**: Lean toward the `whenPositive` pole (e.g., integration, wide deployment, distribution)
- **Near zero (-0.1 to 0.1)**: Balanced or ambiguous position

**Does this specimen reveal a NEW tension?**

Criteria:
1. A structural trade-off that multiple specimens navigate differently
2. Not captured by existing tensions
3. Connected to the core research question

If yes: propose in session log. Don't add to `tensions.json` until confirmed with 3+ specimens showing different positions.

### Step 4: Contingency Analysis (for each non-stub specimen)

Walk through all contingencies. For each:

**Does this specimen illustrate this contingency at work?**

Check the specimen's `contingencies` field and habitat data.

```
Does the specimen's context clearly demonstrate this contingency variable?
├── YES, high end → Add to contingency's high.specimens array
├── YES, low end → Add to contingency's low.specimens array
└── Insufficient context → Skip
```

**Does this specimen suggest a NEW contingency variable?**

If a contextual factor repeatedly determines structural choices across specimens and isn't captured by the existing contingencies, propose it in the session log.

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

Convergent evolution is strong evidence that a structural solution addresses a real organizational problem. Examples:
- Multiple firms creating dual CAIO + CTO roles independently
- Multiple firms appointing business-line leaders as AI heads (rather than technologists)
- Multiple firms collapsing separate AI teams under one leader after coordination costs rose

### Step 5b: Insight Review (across batch)

After processing all specimens in the batch, review cross-cutting insights:

**GUARDRAIL: Insights are NEVER deleted. They can only be updated with new evidence or new insights can be added.**

**Does any newly processed specimen provide evidence for an existing insight?**

Walk through `synthesis/insights.json`. For each insight, check if any newly synthesized specimen provides evidence:

```
Does the specimen support an existing insight?
├── YES → Add the specimen to the insight's `evidence` array
│         Update insight maturity: 1 specimen = "hypothesis", 2 = "emerging", 3+ = "confirmed"
└── NO → Skip
```

**Does this batch reveal a NEW cross-cutting insight?**

Criteria:
1. A finding that spans multiple specimens, industries, or mechanisms
2. Connected to the core research question about structural exploration/execution
3. Not already captured by existing insights
4. Has a theoretical connection (even if preliminary)

If yes: add as a new insight with `"maturity": "hypothesis"` (1 specimen) or `"emerging"` (2 specimens) or `"confirmed"` (3+).

New insight format:
```json
{
  "id": "kebab-case-id",
  "title": "Clear, Specific Title",
  "theme": "convergence | organizational-form | mechanism | workforce | methodology",
  "maturity": "hypothesis | emerging | confirmed",
  "finding": "The empirical finding in 2-4 sentences.",
  "evidence": [{ "specimenId": "org-id", "note": "How this specimen demonstrates it" }],
  "theoreticalConnection": "Connection to organizational economics theory",
  "discoveredIn": "synthesis/sessions/YYYY-MM-DD-synthesis.md",
  "relatedMechanisms": [1, 5],
  "relatedTensions": [2]
}
```

**Are any existing hypothesis/emerging insights now ready for promotion?**

Check evidence counts: if a `"hypothesis"` insight now has 2+ specimens → promote to `"emerging"`. If an `"emerging"` insight now has 3+ → promote to `"confirmed"`.

---

### Step 6: Taxonomy Refinement Check (across batch)

Review all `taxonomyFeedback` fields from processed specimens:

```
Are there specimens that don't fit the 7-model taxonomy cleanly?
├── 5+ specimens with similar misfit → Propose new model or sub-type
├── 2-4 specimens with similar misfit → Note as "emerging pattern, monitor"
├── Isolated misfit → Note in session log, no action
└── All fit → Note "Taxonomy adequate for current specimens"
```

Also check:
- Should any model be retired or merged?
- Should any sub-type be added?
- Are any Model 6 sub-types underspecified?
- Do evolution specimens suggest common structural trajectories?

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

- [ ] **Update `synthesis/insights.json`** (NEVER delete existing insights):
  - New evidence added to existing insights
  - Maturity promotions applied (hypothesis→emerging→confirmed based on evidence count)
  - New insights added (if discovered)
  - `"lastUpdated": "YYYY-MM-DD"`

- [ ] **Write synthesis session log** at `synthesis/sessions/YYYY-MM-DD-synthesis.md`:

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
  insights_updated: []
  new_insights: []
  ---

  # Synthesis Session: YYYY-MM-DD

  ## Specimens Analyzed
  | Specimen | Queue Action | Completeness | Mechanisms Found | Tensions Found |
  |----------|-------------|--------------|------------------|----------------|
  | [org] | created/updated/evolution | High/Medium/Low | [list] | [list] |

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

  ## Insights Updated
  | Insight | New Evidence | Maturity Change |
  |---------|-------------|-----------------|

  ## New Insights Discovered
  | Insight | Theme | Evidence Count | Maturity |
  |---------|-------|----------------|----------|

  ## Key Insights for Executives
  [2-3 bullet points: What should a leader making structural decisions take away?]

  ## Key Insights for Academics
  [2-3 bullet points: What extends or challenges existing theory?]

  ## Open Questions
  [What would we most like to know that we don't?]
  ```

- [ ] **Run validator**:
  ```bash
  node scripts/validate-workflow.js
  ```
  Fix any issues before completing.
