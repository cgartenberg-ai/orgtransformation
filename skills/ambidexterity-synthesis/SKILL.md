---
name: ambidexterity-synthesis
description: "Phase 3 (Synthesis) of the organizational ambidexterity research workflow. Use after Phase 2 curation to identify cross-cutting patterns across specimens. Surfaces mechanisms, tensions, contingencies, and insights about how organizations structurally enable both exploration and execution. Outputs are principles grounded in evidence, not superficial observations. For executive and academic audiences."
---

# Ambidexterity Synthesis Skill (Phase 3: Patterns)

## Purpose

Identify cross-cutting patterns across the specimen collection that illuminate the central question:

> **How do organizations structurally enable both exploration and execution in the AI era?**

This is not news aggregation or trend-spotting. It is pattern recognition grounded in organizational evidence — the kind of insight useful to executives making structural decisions and academics building theory.

## Inputs

- Curated specimen cards from Phase 2
- Existing mechanism descriptions
- Taxonomy feedback from Phase 2 (edge cases, suggested revisions)

## Session Protocol

For step-by-step execution instructions, follow:

**`synthesis/SYNTHESIS-PROTOCOL.md`**

This file (SKILL.md) defines WHAT to look for and HOW to classify patterns. The protocol defines HOW to run a synthesis session end-to-end.

## What Synthesis Produces

1. **Mechanisms** — Structural practices that appear across multiple specimens, with evidence
2. **Tensions** — Trade-offs organizations face when choosing structural approaches
3. **Contingencies** — Conditions that make one approach more appropriate than another
4. **Convergent Evolution** — Different organizations independently arriving at similar solutions
5. **Taxonomy Refinements** — Updates to the classification system based on accumulated evidence

## The Core Question

Every synthesis output should connect to the central question:

> **How do organizations structurally enable both exploration and execution in the AI era?**

Ask: Does this pattern help answer that question? If not, it may be interesting but doesn't belong in this synthesis.

## Quality Standards

### For Executive Audience
- **Actionable**: Patterns should inform structural decisions
- **Specific**: Name the mechanism, cite the evidence, show the trade-off
- **Non-obvious**: Skip patterns that any competent executive already knows
- **Grounded**: Every claim traces to specimen evidence

### For Academic Audience
- **Theoretically connected**: How does this relate to ambidexterity literature?
- **Generalizable**: Does this pattern hold across contexts, or is it context-specific?
- **Falsifiable**: What would we expect to see if this mechanism works? What would disconfirm it?
- **Novel**: Does this extend or challenge existing theory?

### What to Avoid
- **Newsy**: "Company X is doing AI!" — So what?
- **Cutesy**: Clever names without substance
- **Superficial**: Observations without organizational insight
- **Tautological**: "Successful companies do things that make them successful"
- **Consultant-speak**: Vague principles that could mean anything

## Mechanism Analysis

See `synthesis/mechanisms.json` for current mechanism definitions with evidence.
See `synthesis/tensions.json` and `synthesis/contingencies.json` for tensions and contingencies data.

### Current Mechanisms (from case research)

1. **Protect Off-Strategy Work** — Structure that lets deviations survive middle management optimization pressure
2. **Bonus Teams That Kill Projects** — Incentive systems that reward early termination of unpromising work
3. **Embed Product at Research Frontier** — Product teams working directly with researchers, not downstream
4. **Consumer-Grade UX for Employee Tools** — Extending consumer-proven interfaces to employees rather than building separate enterprise systems
5. **Deploy to Thousands Before You Know What Works** — Wide deployment to discover use cases, rather than narrow pilots
6. **Merge Competing AI Teams Under Single Leader** — Consolidation when coordination costs exceed independence benefits
7. **Put Executives on the Tools** — Leaders spending significant time (8+ hours/week) personally using AI
8. **Log Everything When Regulators Watch** — Audit trails as competitive advantage in regulated industries
9. **Hire CAIOs from Consumer Tech** — Prioritizing product-shipping experience over enterprise IT background
10. **Productize Internal Operational Advantages** — Turning internal tools into external revenue streams

### For Each Mechanism, Analyze:

```markdown
## Mechanism: [Name]

### Definition
[One paragraph: What is this mechanism? Be precise.]

### The Organizational Problem It Solves
[What tension or challenge does this address? Connect to exploration/execution.]

### Evidence from Specimens
| Organization | How They Demonstrate It | Source |
|--------------|------------------------|--------|
| [org] | [specific practice] | [URL] |

### Conditions Where It Applies
- Industry: [where this works]
- Org characteristics: [size, stage, etc.]
- Leadership: [what's required]

### Conditions Where It Doesn't Apply
- [Counter-conditions]

### Theoretical Connection
[How does this relate to ambidexterity literature? Structural/contextual/temporal?]

### Open Questions
- [What we don't yet know about this mechanism]
```

### When to Add a New Mechanism

Add a new mechanism when:
1. You observe the same structural practice in 3+ specimens
2. The practice addresses the exploration/execution tension in a specific way
3. The practice is non-obvious (not already captured by existing mechanisms)
4. You can articulate WHY it works (the organizational logic)

**Candidate mechanism format:**
```markdown
## Candidate Mechanism: [Name]

### Observed Pattern
[What are you seeing across specimens?]

### Specimens Where Observed
- [Org 1]: [evidence]
- [Org 2]: [evidence]
- [Org 3]: [evidence]

### Hypothesized Organizational Logic
[Why might this work? What problem does it solve?]

### Confidence Level
[Low/Medium/High] — based on number of specimens and quality of evidence

### What Would Strengthen This
[What additional evidence would move this from candidate to confirmed?]
```

### When to Retire or Merge a Mechanism

Consider retiring when:
- No new specimens demonstrate it
- It overlaps substantially with another mechanism
- The organizational logic doesn't hold up under scrutiny

Consider merging when:
- Two mechanisms are really the same thing with different names
- One is a special case of the other

## Tension Analysis

Tensions are trade-offs organizations face. They don't have "right answers" — they have conditions under which one pole is more appropriate.

### Format for Tensions

```markdown
## Tension: [Pole A] vs. [Pole B]

### The Trade-off
[What are organizations choosing between? Why can't they have both?]

### When [Pole A] is More Appropriate
- Conditions: [industry, stage, resources, etc.]
- Specimens that chose this: [orgs]
- Evidence: [what happened]

### When [Pole B] is More Appropriate
- Conditions: [industry, stage, resources, etc.]
- Specimens that chose this: [orgs]
- Evidence: [what happened]

### The Contingency
[What's the key variable that tips the balance?]

### Theoretical Connection
[How does this relate to ambidexterity literature?]
```

### Known Tensions to Track

- **Structural separation vs. Contextual integration** — When is it better to create separate units vs. expect individuals to switch?
- **Speed of deployment vs. Depth of pilots** — When to go wide fast vs. narrow deep?
- **Central control vs. Distributed autonomy** — When to consolidate vs. federate?
- **Named branding vs. Quiet transformation** — When does formal lab identity help vs. hinder?
- **Long time horizons vs. Short accountability cycles** — How to protect multi-year exploration in quarterly cultures?

## Contingency Analysis

Contingencies are the conditions that determine which approach works. They answer: "It depends on what?"

### Format for Contingencies

```markdown
## Contingency: [Variable Name]

### What It Determines
[Which structural choice depends on this variable?]

### When [High/Present]:
- Favors: [approach]
- Specimens: [orgs]
- Evidence: [what happened]

### When [Low/Absent]:
- Favors: [approach]
- Specimens: [orgs]
- Evidence: [what happened]

### How to Assess
[How would an executive know where their org falls on this variable?]
```

### Candidate Contingencies

- **Regulatory intensity** — Highly regulated industries may need different structures
- **Time-to-obsolescence of core business** — Urgency affects willingness to disrupt
- **CEO tenure and mandate** — Structural change requires sustained leadership
- **Talent market position** — Ability to attract/retain AI talent affects viable structures
- **Existing technical debt** — Legacy systems constrain options

## Convergent Evolution Analysis

When different organizations independently arrive at similar structural solutions, that's signal. It suggests the solution addresses a real organizational problem.

### Format for Convergent Evolution

```markdown
## Convergent Pattern: [Name]

### The Similar Solution
[What structural arrangement did multiple orgs arrive at independently?]

### Organizations That Converged
| Organization | Industry | When | Their Version |
|--------------|----------|------|---------------|
| [org] | [industry] | [year] | [specifics] |

### The Organizational Problem
[What shared problem were they solving?]

### Variation Within Convergence
[How do the implementations differ in detail?]

### Implication
[What does this convergence tell us about structural solutions to ambidexterity?]
```

## Taxonomy Refinement

Phase 2 generates taxonomy feedback (edge cases, suggested revisions). Synthesis evaluates and acts on this feedback.

### When to Refine the Taxonomy

- **Add a model** when 5+ specimens don't fit existing models and share characteristics
- **Add a sub-type** when a model has meaningful variation that affects how it works
- **Merge models** when distinction doesn't predict different outcomes
- **Rename** when current name causes confusion or doesn't capture the essence

### Format for Taxonomy Proposals

```markdown
## Taxonomy Proposal: [Add/Merge/Rename/Retire]

### Current State
[What exists now]

### Proposed Change
[What should change]

### Evidence
- Specimens that motivate this: [list]
- Edge cases: [list]

### Impact
- Which specimens would be reclassified?
- Does this improve or reduce clarity?

### Confidence
[Low/Medium/High]
```

## Synthesis Session Output

```markdown
# Synthesis Session: [Date]

## Specimens Analyzed
[List of specimen cards reviewed this session]

## Mechanism Updates

### Strengthened
| Mechanism | New Evidence | From Specimens |
|-----------|--------------|----------------|
| [mech] | [what was added] | [orgs] |

### Candidates Identified
| Candidate | Evidence Count | Confidence |
|-----------|----------------|------------|
| [name] | [# specimens] | [L/M/H] |

### Candidates Promoted to Mechanisms
| New Mechanism | Based On |
|---------------|----------|
| [name] | [evidence summary] |

## Tensions Identified/Updated
| Tension | New Insight |
|---------|-------------|
| [A vs. B] | [what we learned] |

## Contingencies Identified/Updated
| Contingency | New Insight |
|-------------|-------------|
| [variable] | [what we learned] |

## Convergent Evolution Observed
| Pattern | Organizations | Significance |
|---------|---------------|--------------|
| [pattern] | [orgs] | [why it matters] |

## Taxonomy Proposals
| Proposal | Type | Confidence |
|----------|------|------------|
| [proposal] | [add/merge/etc.] | [L/M/H] |

## Key Insights for Executives
[2-3 bullet points: What should a leader making structural decisions take away?]

## Key Insights for Academics
[2-3 bullet points: What extends or challenges existing theory?]

## Open Questions
[What would we most like to know that we don't?]
```

## Principles for Good Synthesis

1. **Evidence first** — Start with what you see in specimens, not what you think should be true
2. **Explain the mechanism** — Don't just name patterns; explain why they work organizationally
3. **Embrace contingency** — "It depends" is often the right answer; specify what it depends on
4. **Connect to theory** — Ambidexterity literature provides vocabulary and hypotheses; use it
5. **Serve both audiences** — Executives need actionable insight; academics need theoretical contribution
6. **Stay humble** — Small sample sizes, self-reported data, survivorship bias — note limitations
7. **Update beliefs** — If evidence contradicts a mechanism, revise the mechanism, not the evidence
