# Narrative Creation Spec: Insight-Driven Field Guide Writing

## Purpose

This spec describes how the field guide's **field insights** serve as **citable empirical claims** when writing narrative chapters, executive summaries, academic papers, or teaching materials. Insights are the bridge between raw specimen data and publishable prose.

---

## The Problem

The field guide contains rich data — 85 specimens, 9 confirmed mechanisms, 13 cross-cutting insights, 5 tensions — but this data currently lives in JSON files and a reference site. To become a published field guide (book, report, or article), this data must be transformed into narrative prose that:

1. Makes empirical claims grounded in evidence
2. Cites specific specimens as support
3. Connects to organizational theory
4. Distinguishes between confirmed findings (3+ specimens) and hypotheses (1 specimen)
5. Maintains intellectual honesty about evidence strength

---

## Insights as the Citation Layer

Each insight in `synthesis/insights.json` is a self-contained empirical claim with everything needed for narrative citation:

```
┌─────────────────────────────────────────────────────────────┐
│  INSIGHT: "Hub-and-Spoke Is the Default for Regulated       │
│            Industries"                                       │
│                                                             │
│  Claim:    5 pharma companies independently adopted M4      │
│  Maturity: confirmed (5 specimens)                          │
│  Evidence: Pfizer, Roche, Sanofi, Novo Nordisk, Eli Lilly  │
│  Theory:   Arrow's information economics                    │
│  Theme:    convergence                                       │
│                                                             │
│  → Ready for narrative use as a confirmed finding           │
└─────────────────────────────────────────────────────────────┘
```

### What Makes Insights Citable

| Property | Narrative Role |
|----------|---------------|
| `finding` | The empirical claim itself — the sentence(s) you'd write in prose |
| `evidence[]` | The specimens that support the claim — your citation list |
| `maturity` | How confident the claim is — determines hedging language |
| `theoreticalConnection` | The scholarly grounding — connects to existing literature |
| `relatedMechanisms` | Cross-references to structural patterns |
| `relatedTensions` | Cross-references to trade-offs |
| `theme` | Organizational bucket for chapter structure |

---

## Maturity-Appropriate Language

The insight's maturity level determines the appropriate hedging language in narrative prose:

### Confirmed (3+ specimens)
Strong claims with direct attribution:

> "Five pharmaceutical companies independently adopted hub-and-spoke structures with central AI teams feeding into distributed therapeutic area teams (Pfizer, Roche, Sanofi, Novo Nordisk, Eli Lilly). This convergence suggests hub-and-spoke is the structurally dominant pattern for regulated industries."

### Emerging (2 specimens)
Qualified claims with explicit evidence count:

> "Early evidence from JPMorgan and Bank of America suggests that regulation doesn't slow AI deployment — it makes deployment expensive. Both organizations achieved rapid iteration cycles despite heavy regulatory oversight, suggesting that compliance infrastructure investment, not speed reduction, is the actual cost of regulation."

### Hypothesis (1 specimen)
Clearly flagged as preliminary:

> "Meta's consolidation of FAIR research into product-focused MSL provides a cautionary case for what happens when research autonomy is sacrificed for product urgency. While this is a single observation, it aligns with March's (1991) prediction that exploitation drives out exploration when organizations face competitive pressure."

---

## Narrative Structure: From Insights to Chapters

### Organizing Principle

Insights group naturally by theme, which maps to potential chapter structure:

| Theme | Potential Chapter | Insight Count |
|-------|------------------|---------------|
| `convergence` | "Convergent Evolution: When Different Organizations Arrive at the Same Structure" | 5 |
| `organizational-form` | "The Forms That AI Creates: New Organizational Species" | 2 |
| `mechanism` | "What Works and What Doesn't: Cautionary Tales and Counter-Evidence" | 3 |
| `workforce` | "The Human Side: How AI Reshapes Who Works and How" | 2 |
| `methodology` | "The Observer's Dilemma: Methodological Notes" | 1 |

### Within Each Chapter

Each chapter follows a pattern:

1. **Opening claim** — The confirmed insight as a clear empirical finding
2. **Evidence parade** — Walk through 2-3 key specimens that demonstrate the finding, with specific details (quotes, metrics, structural descriptions)
3. **Theoretical grounding** — Connect to organizational economics (the `theoreticalConnection` field)
4. **Nuance and counter-evidence** — Emerging and hypothesis insights that complicate or extend the main finding
5. **Implications** — What this means for leaders making structural decisions (executive lens) and what it means for theory (academic lens)

### Example: Writing a Convergence Chapter Section

**Source insight**: `management-delayering-convergent`

**Narrative draft**:

> *Microsoft, UPS, and Amazon — a software company, a logistics company, and a retailer — independently arrived at the same structural conclusion: when AI handles information synthesis, you need fewer managers. Microsoft's Satya Nadella demanded that leaders function as individual contributors. UPS eliminated 30,000 positions, targeting management layers specifically, backed by a $9 billion automation investment. Amazon cut 16,000 roles in January 2026, framing the move as "removing bureaucracy" rather than cost-cutting.*
>
> *This convergent evolution across three unrelated industries is strong evidence that management delayering is a genuine structural response to AI, not an industry-specific trend. Simon's (1947) information-processing view of organizations helps explain why: hierarchy exists to manage bounded rationality. AI expands individual cognitive capacity, reducing the need for hierarchical information aggregation.*
>
> *However, this finding should be read alongside the emerging pattern of "AI redundancy washing" — Deutsche Bank has warned that some organizations use AI as justification for cuts that would have happened anyway. The challenge for researchers is distinguishing genuine AI-driven structural change from convenient narrative.*

---

## Writing Workflow

### Step 1: Select Insights for a Writing Session

Choose insights by:
- **Theme** — write a thematic chapter
- **Maturity** — lead with confirmed, support with emerging, flag hypotheses
- **Interconnection** — insights that share `relatedMechanisms` or `relatedTensions` belong together

### Step 2: Gather Supporting Specimen Data

For each insight's `evidence[]` array, read the full specimen files to extract:
- Quotes with attribution
- Specific metrics and numbers
- Structural descriptions
- Observable markers
- Evolution layers (for "how they got here" narrative)

### Step 3: Draft with Maturity-Appropriate Language

Apply the hedging rules from the maturity table above. Never overstate a hypothesis as a confirmed finding.

### Step 4: Cross-Reference Mechanisms and Tensions

Each insight connects to broader patterns:
- **Mechanisms** tell the reader *how* organizations do it
- **Tensions** tell the reader *what trade-offs* organizations navigate
- **Contingencies** tell the reader *when* different approaches work

### Step 5: Dual-Audience Polish

Every section should be readable by both audiences:
- **Executives**: "What should I take away?" — practical structural implications
- **Academics**: "What does this mean for theory?" — theoretical connections and open questions

---

## Guardrails for Narrative Creation

1. **Never claim more than the evidence supports.** If an insight has 1 specimen, it's a hypothesis. Say so.
2. **Always cite specific specimens.** "Several organizations" is not acceptable when you can name them.
3. **Distinguish observation from prescription.** The field guide documents what organizations do, not what they should do. "We observe X" not "Organizations should do X."
4. **Preserve provenance.** When quoting a leader, include the source and date.
5. **Flag counter-evidence.** If an insight has exceptions or complications, include them. Intellectual honesty builds credibility.
6. **Never delete insights.** Even if an insight is later contradicted by new evidence, it remains in the record. Update the insight's evidence and maturity, but don't remove it.
7. **Respect the maturity lifecycle.** Don't cherry-pick a single specimen to make a sweeping claim. The maturity system exists for a reason.

---

## Future: Automated Narrative Drafting

A potential `/write` skill could:

1. Accept a theme or set of insight IDs as input
2. Load all relevant insights, their evidence specimens, and connected mechanisms/tensions
3. Draft narrative prose following the chapter structure template above
4. Apply maturity-appropriate language automatically
5. Generate proper citations with specimen names and source dates
6. Flag thin-evidence areas as "needs more research"
7. Output both executive-facing and academic-facing versions

This skill would complement the existing `/research` → `/curate` → `/synthesize` pipeline by adding a fourth phase:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  FIELD WORK │ ──▶ │  CURATION   │ ──▶ │  SYNTHESIS  │ ──▶ │  NARRATIVE  │
│  (Research) │     │  (Classify) │     │  (Patterns) │     │  (Write)    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                    │
  Gather wide &       Apply taxonomy      Identify cross-     Transform into
  deep observations   to specimens        cutting patterns    publishable prose
```

### Implementation Notes for `/write` Skill

- **Input**: Theme, insight IDs, or "all confirmed insights"
- **Protocol**: Load insights → load specimens → draft narrative → apply maturity language → cross-reference mechanisms/tensions → output
- **Output**: Markdown file in `narrative/drafts/` with:
  - Chapter draft with proper citations
  - Evidence strength annotations
  - "Needs more research" flags for thin areas
  - Executive summary version
  - Academic version with theoretical connections
- **Guardrails**: Never generate narrative for insights with `maturity: "hypothesis"` as if they were confirmed

---

## Relationship to Other Specs

| Spec | Relationship |
|------|-------------|
| `Ambidexterity_Field_Guide_Spec.md` | Defines the taxonomy, specimen structure, and mechanisms that insights reference |
| `synthesis/SYNTHESIS-PROTOCOL.md` | Defines how insights are created and updated during synthesis (Step 5b) |
| `UI_Spec.md` | Defines how insights are displayed on the reference site |
| `SW_ARCHITECTURE.md` | Defines the data types and access patterns for insight data |
| `CLAUDE.md` | Contains the guardrail that insights are never deleted |

---

*This spec was created February 3, 2026. It describes the conceptual framework for Phase 4 (Narrative Creation) of the field guide workflow. Implementation of the `/write` skill is a future work item.*
