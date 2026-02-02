---
name: ambidexterity-curation
description: "Phase 2 (Curation) of the organizational ambidexterity research workflow. Use after Phase 1 research to classify raw findings into structured specimen cards. Applies the 7-model taxonomy and 3 ambidexterity orientations. Preserves historical layers (stratigraphy), maintains source provenance, and flags taxonomy edge cases. Outputs structured specimens ready for the herbarium."
---

# Ambidexterity Curation Skill (Phase 2: Classification)

## Purpose

Transform raw research findings (Phase 1 output) into structured specimen cards. Apply the taxonomy, preserve source provenance, maintain historical layers, and flag edge cases that may inform taxonomy evolution.

## Session Protocol

For step-by-step execution instructions, follow:
**`curation/CURATION-PROTOCOL.md`**

This file (SKILL.md) defines WHAT to look for and HOW to classify. The protocol defines HOW to run a curation session end-to-end.

## Inputs

- Raw findings from Phase 1 research sessions (markdown files with observations, sources, quotes)
- Existing specimens that may need updating (if raw findings contain new information about known orgs)
- Specimen registry (to check if org already exists)

## The Taxonomy

See also: `references/classification-quick-ref.md` for one-line tests, `references/type-specimens.md` for clearest examples of each model.

### Dimension 1: Structural Model

*What is the organizational structure for AI?*

| Model | Mission | Time Horizon | Key Indicator |
|-------|---------|--------------|---------------|
| **1. Research Lab** | Fundamental research, breakthroughs | 3-10 years | Publications, patents, long-term R&D |
| **2. Center of Excellence** | Governance, standards, enablement | 6-24 months | Adoption rates, compliance, training |
| **3. Embedded Teams** | Product-specific AI features | Quarterly | Product KPIs, feature releases |
| **4. Hybrid/Hub-and-Spoke** | Central standards + distributed execution | Mixed | Central + BU metrics |
| **5. Product/Venture Lab** | Commercialize AI into products | 6-36 months | Revenue, valuations, launches |
| **6. Unnamed/Informal** | Quiet transformation without formal structure | Varies | Adoption metrics, no formal branding |
| **7. Tiger Teams** | Time-boxed exploration sprints | Weeks to months | Sprint outcomes, reintegration |
| **8. Skunkworks (Emerging)** | Semi-autonomous unit rebuilding core business with AI, structurally positioned to absorb legacy org | 1-3 years | [No confirmed specimens] |

**Model 5 Sub-Types:**
- **5a. Internal Incubator** — Products absorbed into parent company (e.g., Adobe Firefly)
- **5b. Venture Builder** — Creates independent companies (e.g., Google X → Waymo)
- **5c. Platform-to-Product** — Internal capability sold externally (e.g., Walmart GoLocal)

**Model 6 Sub-Types:**
- **6a. Enterprise-Wide Adoption** — Mass deployment, 80%+ adoption (e.g., BofA 95% AI usage)
- **6b. Centralized-but-Unnamed** — Central team without lab branding (e.g., P&G ChatPG)
- **6c. Grassroots/Bottom-Up** — Adoption preceded formal structure (e.g., "secret cyborg" patterns)

### Dimension 2: Ambidexterity Orientation

*How does the organization balance exploration and execution?*

| Orientation | Description | Characteristic Pattern |
|-------------|-------------|------------------------|
| **Structural** | Exploration and execution in distinct units | Ring-fenced budgets, different reporting lines, protected time horizons |
| **Contextual** | Individuals balance exploration/execution within roles | "Prove AI can't do it" mandates, AI proficiency as baseline expectation |
| **Temporal** | Organization cycles between exploration and execution phases | Sprints, time-boxed experiments, phased transitions |

Most specimens exhibit one dominant orientation, though combinations occur.

### Taxonomy Flexibility Principles

The taxonomy is a tool for navigation, not a cage. Apply these principles:

1. **"Hybrid" is valid** — Many orgs combine models. Classify as primary + secondary (e.g., "Model 1 + 5b")
2. **Edge cases are valuable** — If an org doesn't fit cleanly, note why. Edge cases inform taxonomy evolution.
3. **Flag uncertainty** — If classification is ambiguous, mark confidence level (High/Medium/Low) with rationale
4. **Suggest revisions** — If you see a pattern that the current taxonomy doesn't capture well, note it in Taxonomy Feedback section
5. **Type specimens** — Note when an org is an especially clear example of a model (useful for reference)

## Classification Process

### Step 1: Review Raw Findings

Read the Phase 1 output for the organization. Identify:
- What structural arrangements are described?
- What time horizons are mentioned?
- What integration mechanisms connect exploration to execution?
- Are there evolution flags (org changed its approach)?

### Step 2: Assign Structural Model

Ask these questions in order:

```
1. Is there a formal AI unit?
   └─ NO → Model 6 (Unnamed/Informal)
      ├─ Mass adoption (>50%)? → 6a
      ├─ Central team, informal name? → 6b
      └─ Adoption preceded structure? → 6c

   └─ YES → Continue...

2. Does the unit publish academic research as PRIMARY output?
   └─ YES → Is research commercialized within 2 years?
      ├─ YES → Model 5 (Product/Venture Lab)
      └─ NO → Model 1 (Research Lab)

3. Does a central AI team exist?
   └─ NO → Model 3 (Embedded Teams)
   └─ YES → Continue...

4. Does central team BUILD products or ENABLE others?
   └─ ENABLE → Model 2 (Center of Excellence)
   └─ BUILD → Are outputs new products/companies?
      ├─ YES → Model 5 (Product/Venture Lab)
      │   ├─ Products stay in parent? → 5a
      │   ├─ Spin-offs become independent? → 5b
      │   └─ Internal tools sold externally? → 5c
      └─ NO → Model 4 (Hybrid/Hub-and-Spoke)

5. Is there a time-boxed team structure?
   └─ YES → Is it a permanent program (3+ years) with a pipeline?
      ├─ YES → Model 5 (Product/Venture Lab) — temporal cycling is orientation, not structure
      │   ├─ Is the unit building something *adjacent* to the core business? → 5a/5b/5c
      │   └─ Is the unit *reimagining* a core business line with the structural potential
      │       to absorb legacy operations? → Flag as potential M8 (Skunkworks) in Taxonomy Feedback.
      │       Classify as M5 for now until M8 has confirmed specimens.
      └─ NO → Model 7 (Tiger Teams) — ad hoc, temporary structures only
```

### Classification Guardrails

After walking the decision tree, check these common misclassification patterns before finalizing:

**Guardrail 1: Permanence vs. Time-Boxing (M7 trap)**
If you classified as M7 (Tiger Teams), ask: Has this structure existed for 3+ years with a dedicated pipeline? If YES → it's likely M5 (with Temporal orientation), not M7. M7 is reserved for *ad hoc, temporary* structures — not permanent institutional programs. The temporal cycling of individuals is an *orientation* feature, not a structural model.

**Guardrail 2: Single Lab vs. Federation (M1 trap)**
If you classified as M1 (Research Lab), ask: Are there 3+ semi-autonomous units coordinated by a central function? If YES → it's M4 (Hub-and-Spoke) regardless of whether the units do research. M1 means a single, ring-fenced research entity. Multiple distributed units with central coordination = M4.

**Guardrail 3: Research Work vs. Research Structure (M1 trap)**
If you classified as M1 (Research Lab), ask: Is the AI unit's primary integration pattern tight-loop feedback with existing teams? If YES → it's M3 (Embedded Teams) even if the people are researchers. M1 requires *deliberate separation* from product/operational timelines. Scientists who sit inside teams and iterate tightly are embedded, not ring-fenced.

**Guardrail 4: Prestige Bias Check**
M1 (Research Lab) is the most commonly over-applied model. Before finalizing M1, verify: Is the unit truly *ring-fenced and separated*, or is it integrated into the broader organization's workflow? Does it have academic culture, publications, and multi-year horizons as primary outputs?

**Guardrail 5: AI-Native Scope Check**
If the specimen is a standalone AI startup (no legacy business to balance), it may not exhibit ambidexterity tension. Tag `habitat.orgType: "AI-native"` and note that the ambidexterity framing applies differently. These specimens are valuable as competitive threat reference points for AI-adopter organizations.

**Guardrail 6: One-Time Event vs. Temporal Orientation**
If you assigned Temporal orientation, ask: Is the organization *cycling* between exploration and execution, or did it make a *one-time pivot*? A single dramatic transformation (e.g., "refounded for AI in 72 hours") is not temporal cycling. If individuals now balance both in their daily roles, the orientation is Contextual.

**Guardrail 7: Adjacent Venture vs. Core Replacement (M5 vs. M8)**
If you classified as M5, ask: Is the unit building something *adjacent* to the core business, or *reimagining* a core business line with the structural potential to absorb or replace legacy operations? No company will publicly frame this as cannibalization — look for structural signals: the unit mirrors an existing function, operates at scale, and has a pathway to become the primary way work gets done. If you see this pattern, flag as potential M8 (Skunkworks) in Taxonomy Feedback. Classify as M5 for now until M8 has confirmed specimens.

### Step 3: Assign Ambidexterity Orientation

| If you see... | Orientation is likely... |
|---------------|-------------------------|
| Separate units for exploration vs. execution, ring-fenced budgets, CEO protection | **Structural** |
| AI proficiency expected in all roles, "prove AI can't do it", no separate AI function | **Contextual** |
| Time-boxed sprints, people cycling between exploration and execution, tiger teams | **Temporal** |

### Step 4: Link to Mechanisms

Review the 10 mechanisms. Does this org demonstrate any?

1. **Protect Off-Strategy Work** — Structure that lets deviations survive
2. **Bonus Teams That Kill Projects** — Incentivize early termination
3. **Embed Product at Research Frontier** — Product teams work directly with researchers
4. **Consumer-Grade UX for Employee Tools** — Extend consumer interfaces internally
5. **Deploy to Thousands Before You Know What Works** — Cast wide, then concentrate
6. **Merge Competing AI Teams Under Single Leader** — Consolidate when coordination costs exceed independence
7. **Put Executives on the Tools** — Leaders use AI 8+ hours/week on real work
8. **Log Everything When Regulators Watch** — Audit trails as competitive advantage
9. **Hire CAIOs from Consumer Tech** — Product-shipping experience over enterprise IT
10. **Productize Internal Operational Advantages** — Internal tools become revenue streams

### Step 5: Reconcile Historical Layers (Stratigraphy)

If the org already has a specimen, or if Phase 1 flagged evolution:

1. **Check for EVOLUTION flags** in raw findings
2. **Do NOT overwrite** existing layers — add a new layer
3. **Each layer includes:**
   - Layer date (when this state was revealed by org)
   - What changed from previous layer
   - Sources for this layer

```
SPECIMEN: [Org Name]
├── [YYYY-MM] Layer: [Classification] — [Key change]
│   └── Sources: [URLs]
├── [YYYY-MM] Layer: [Previous classification] — [State at that time]
│   └── Sources: [URLs]
└── [YYYY-MM] Layer: [Earlier state if known]
    └── Sources: [URLs]
```

### Step 6: Structure the Specimen Card

```markdown
# SPECIMEN: [Organization Name]

## Classification
- **Structural Model**: [Model X] ([Sub-type if applicable])
- **Ambidexterity Orientation**: [Structural/Contextual/Temporal]
- **Classification Confidence**: [High/Medium/Low]
- **Type Specimen**: [Yes/No] — If yes, this is a clear example of the model

## Description
[2-3 paragraph narrative description of how this org structures AI exploration and execution. What does it actually look like? Be specific.]

## Structural Mechanisms
Specific practices that make this form work:
- [Mechanism with evidence and source]
- [Mechanism with evidence and source]

## Observable Markers
How you'd recognize this form:
- **Reporting structure**: [who reports to whom]
- **Resource allocation**: [budget, headcount patterns]
- **Time horizons**: [planning cycles]
- **Decision rights**: [who decides what]

## Habitat Conditions
Conditions under which this form appears:
- **Industry**: [sector]
- **Organization size**: [employees, revenue if known]
- **Leadership factors**: [CEO involvement, CAIO presence]

## Mechanisms Demonstrated
Which of the 10 cross-cutting mechanisms this org demonstrates:
- [#X Mechanism Name] — [how they demonstrate it]

## Historical Layers
[Stratigraphy — each layer with date, state, and sources]

## Quotes & Evidence
> "[Verbatim quote]"
> — [Speaker], [Title], [Source](URL), [Timestamp if audio/video], [Date]

## Sources
| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| [fact] | [type] | [source] | [url] | [timestamp] | [date] | [date] |

## Open Questions
- [What remains unclear about this org]

## Taxonomy Feedback
- [Any observations about how this org fits or doesn't fit the taxonomy]
- [Suggested refinements if the taxonomy doesn't capture something important]
```

## Curation Principles

1. **Preserve all source provenance** — Every fact in the specimen card must trace back to a URL from Phase 1 research. Don't add facts without sources.

2. **Additive only** — New findings create new layers, not replacements. If an org evolved, show the evolution.

3. **Verbatim quotes** — Preserve exact wording. Don't paraphrase quotes.

4. **Classification rationale** — If classification isn't obvious, explain why you chose what you chose.

5. **Uncertainty is okay** — Mark confidence levels. "Medium confidence - limited sources" is better than false certainty.

6. **Edge cases are data** — Organizations that don't fit cleanly are valuable. Note them in Taxonomy Feedback.

7. **Type specimens** — When an org is an especially clear, well-documented example of a model, mark it as a Type Specimen. These become the reference examples.

## Output

For each organization processed:

1. **Specimen card** (in format above)
2. **Specimen registry update**:
   ```
   | Organization | Status | Created | Last Updated | Layer Count | Completeness | Confidence |
   ```
3. **Taxonomy feedback** (if any edge cases or suggested revisions)

## Session Output

End each curation session with:

```markdown
# Curation Session: [Date]

## Specimens Created/Updated
| Organization | Action | Model | Orientation | Confidence | Notes |
|--------------|--------|-------|-------------|------------|-------|
| [org] | Created/Updated | [model] | [orientation] | [H/M/L] | [notes] |

## Taxonomy Feedback
[Any patterns that don't fit well, suggested refinements]

## Edge Cases
[Organizations that were difficult to classify and why]

## Type Specimens Identified
[Organizations that are especially clear examples of a model]

## Sources Processed
[List of Phase 1 research files processed this session]
```
