# Purpose Claims: Data Layer Specification

## Created: February 6, 2026

---

## 1. What We're Collecting

**Definition**: A purpose claim is a verbatim statement by an organizational leader that invokes organizational purpose, identity, values, or mission in the context of AI adaptation.

**Why this matters**: Purpose claims do organizational work — they authorize investment, justify sacrifice, reset employment contracts, and provide direction when profit signals are weak. The registry is primary evidence for studying how leaders use purpose rhetorically during technological transformation.

### Inclusion Criteria (ALL must be met)

1. **Verbatim quote** — Exact words, in quotation marks. No paraphrases.
2. **Named speaker** — Full name with organizational role. No anonymous sources.
3. **AI-adaptation context** — The claim was made in connection with AI/technology transformation, not generic corporate purpose.
4. **Source provenance** — URL available, source date known (at least month/year).

### Exclusion Criteria

- Paraphrases or summaries (even accurate ones)
- Anonymous sources ("a senior executive said")
- Pre-AI statements (before 2023) unless explicitly referenced in current AI context
- Analyst/journalist interpretations of what leaders meant
- Generic mission statements not connected to AI transformation

---

## 2. Claim Schema

```json
{
  "id": "specimen--NNN",
  "specimenId": "string",
  "claimType": "enum (primary type)",
  "secondaryType": "enum | null",
  "text": "Exact verbatim quote",
  "speaker": "Full name",
  "speakerTitle": "Title, Organization",
  "context": "1-2 sentences: when/where said, what prompted it",
  "rhetoricalFunction": "What organizational work is this claim doing?",
  "source": "Source name",
  "sourceUrl": "URL",
  "sourceType": "enum",
  "sourceDate": "YYYY-MM-DD or YYYY-MM",
  "collectedDate": "YYYY-MM-DD",
  "transcriptSource": true | false,
  "taxonomyFlag": "string | null (for claims that don't fit types cleanly)",
  "notes": "Optional: edge cases, cross-references, analytical flags"
}
```

### Source Types (enum)

- `Earnings Call`
- `Internal Memo`
- `Podcast`
- `Interview`
- `Press`
- `Social Media`
- `Speech`
- `Congressional Testimony`
- `Shareholder Letter`

---

## 3. Claim Type Taxonomy

### Current Types (v2.0)

The taxonomy classifies purpose claims by **what END the claim invokes to justify AI transformation**. Every purpose claim implicitly answers: "Why are we doing this?" The taxonomy classifies the *type of end* the leader invokes — not the rhetorical move, not the topic, but the ultimate justification offered.

| Type | The claim says... | Core Question | Example |
|------|-------------------|---------------|---------|
| **utopian** | We are part of a civilizational transformation | "What epoch are we in?" | Hassabis: "radical abundance"; Benioff: "we are the last generation of CEOs to manage only humans" |
| **teleological** | We exist to achieve a specific moral/social outcome | "What concrete outcome justifies our existence?" | Hassabis: "cure all disease"; Bourla: "save the world from cancer"; SSI: "building safe superintelligence" |
| **higher-calling** | We answer to a duty/purpose that supersedes profit | "What obligation overrides economic logic?" | Amodei: "we work on science and biomedical out of proportion to its immediate profitability"; Ricks: "we have a higher calling" |
| **identity** | We do this because of who we are — group commitment | "Who are we?" | Teller: "we spend most of our time breaking things"; Nadella: "growth mindset"; Amodei: "having at least one player with a strong compass" |
| **survival** | We must change or be left behind | "What threat demands action?" | Regev: "if we proceed in this stepwise way we won't move fast enough"; Sweet: "this is reversing five decades"; Hudson: "you don't delegate the revolution" |
| **commercial-success** | This will make the business perform better | "How does this improve business outcomes?" | Nadella: "increase the ROIC on the capital spend"; Wells Fargo: "deliver an even better experience for customers" |
| **unclassified** | Does not clearly invoke a purpose-end | — | Managerial directives, metrics, observations retained for review |

### Distinguishing Similar Types

**Utopian vs. Teleological vs. Higher-calling:**
- Utopian: the moment in history is the justification (epochal, civilizational)
- Teleological: a specific achievable outcome is the justification (cure cancer, build safe superintelligence)
- Higher-calling: a moral obligation that supersedes profit is the justification (we owe it to patients, we choose science over profitability)

**Survival vs. Commercial-success:**
- Survival: existential framing, adapt-or-die, the status quo is not viable
- Commercial-success: positive framing, this will make us better/more efficient/more competitive

**Identity vs. everything else:**
- Identity: the end IS the group's self-concept. "We do this because this is who we are." The justification terminates in collective identity itself.

### Multi-Coding Rule

Assign **primary type** based on dominant rhetorical function. Assign **secondary type** only if a second function is clearly present (not just implied). Use the `secondaryType` field.

### Taxonomy Evolution Protocol

1. **Flag edge cases**: Any claim that doesn't fit cleanly gets `"taxonomyFlag": "description of fit problem"`

2. **Quarterly review**: After every ~30 specimens, review flagged claims as a batch.

3. **Revision threshold**: If 5+ claims share a common fit problem, consider taxonomy revision.

4. **Revision options**:
   - Add new type
   - Split existing type into subtypes
   - Merge types that aren't pulling their weight
   - Redefine type boundaries

5. **When taxonomy changes**: Recode affected claims. The registry is source of truth.

6. **Changelog**: Document all taxonomy revisions in Section 10 of this spec.

---

## 4. Deduplication Rules

| Situation | Action |
|-----------|--------|
| Same quote, multiple sources | Capture once, use best source (primary > secondary, earlier > later) |
| Same idea, different words | Capture both as separate claims |
| Quote evolved over time | Capture each version with dates, note evolution in `notes` |
| Quote in prepared remarks AND Q&A | Prefer prepared remarks (more deliberate) |
| Quote in transcript AND press coverage | Prefer transcript (verbatim) over press (may be edited) |

---

## 5. Context Standards

The `context` field should answer:
- **When** was this said? (date, event)
- **What prompted it?** (question asked, announcement being made)
- **What was happening organizationally?** (restructuring, earnings, product launch)

Keep to 1-2 sentences. Context is for understanding, not analysis. The `rhetoricalFunction` field is for analysis.

---

## 6. Source Hierarchy

### Tier 1 (prefer)

- Earnings call transcripts (prepared remarks > Q&A)
- Internal memos (leaked or officially published)
- Podcast transcripts from established sources
- Official company communications (shareholder letters, blog posts)
- Congressional/regulatory testimony

### Tier 2 (acceptable)

- Press interviews (Fortune, Bloomberg, WSJ, FT, The Information)
- Conference keynotes and presentations
- Social media posts by verified leaders (LinkedIn, Threads, X)

### Tier 3 (use if only option)

- Press coverage quoting leader (verify quote appears verbatim)
- Secondary sources citing primary sources
- Aggregator sites

### Transcript Sources with Full Text Available

These sources publish full transcripts, making them high-value for purpose claims:
- Cheeky Pint (Substack)
- Dwarkesh Podcast
- Latent Space
- Acquired
- Conversations with Tyler
- Lex Fridman Podcast
- Cognitive Revolution

---

## 7. Scanning Protocol

### Step 1: Check Transcript Availability

Before web searching, check if transcript sources exist:

1. Consult `transcript-gap-queue.json` for known pairs
2. Search: `[CEO name] site:cheekypint.substack.com OR site:dwarkesh.com OR site:lexfridman.com OR site:latent.space OR site:acquired.fm`
3. Search: `[CEO name] Fortune interview transcript` / `Bloomberg interview`
4. Flag specimen as: `has-transcript` | `web-only` | `low-profile`

### Step 2: Run Standard Searches

Eight queries, all weighted equally. Record what you find, don't hunt for confirmation.

1. `[CEO name] AI transformation purpose mission`
2. `[CEO name] AI workforce employees future`
3. `[CEO name] AI strategy vision bet`
4. `[CEO name] AI restructuring layoffs why`
5. `[CEO name] AI identity "who we are" values`
6. `[CEO name] AI uncertainty ROI investment`
7. `[CEO name] AI vs [competitor] different approach`
8. `[Company] CEO AI quote interview transcript`

### Step 3: Deep-Scan Transcripts

If transcripts available:
- Read full transcript (not just search snippets)
- Extract all statements meeting inclusion criteria
- Transcripts yield richer identity, teleological, and direction-under-uncertainty claims

### Step 4: Record Findings

1. Write claims to `pending/[specimen-id].json`
2. Self-review for inclusion criteria compliance
3. Merge to main `registry.json`
4. Update `scan-tracker.json` with quality and transcript flags

### Step 5: Flag for Rescan

Flag for future rescan if:
- `web-only` AND claims < 3 AND leader is high-profile
- New transcript source becomes available
- Specimen undergoes major structural change (new claims likely)

---

## 8. Quality Tracking

### Scan Tracker Schema

```json
{
  "specimenId": "string",
  "lastScanned": "YYYY-MM-DD | null",
  "claimsFound": number,
  "quality": "rich | adequate | thin | none | unscanned",
  "transcriptAccess": "has-transcript | web-only | low-profile",
  "rescanFlag": true | false,
  "rescanReason": "string | null"
}
```

### Quality Levels

| Level | Claims | Interpretation |
|-------|--------|----------------|
| **rich** | 5+ | Comprehensive coverage |
| **adequate** | 2-4 | Usable, may have gaps |
| **thin** | 1 | Likely incomplete, consider rescan |
| **none** | 0 (scanned) | Either genuinely low-density OR methodology gap |
| **unscanned** | — | Not yet processed |

### Interpreting "None" Results

A `none` result requires diagnosis:
- **Genuinely low-density**: Leader is technocratic, doesn't use purpose language (valid finding)
- **Low-profile leader**: CEO not publicly visible, few interviews (data limitation)
- **Methodology gap**: Web search missed it, transcript would find it (rescan candidate)
- **Pre-AI specimen**: Organization's AI work predates purpose-claim era (valid finding)

Record diagnosis in `notes` field of scan-tracker.

---

## 9. Registry Maintenance

### After Each Scanning Session

1. Merge pending claims to `registry.json`
2. Update `scan-tracker.json`
3. If new patterns observed, update `analytical-notes.md`
4. Commit changes with session summary

### Periodic Audit (every ~30 specimens)

1. Check for duplicate claims (same quote, different IDs)
2. Verify sample of source URLs still work
3. Review `thin` and `none` specimens for rescan candidates
4. Review `taxonomyFlag` claims for taxonomy revision
5. Update claim type distribution statistics
6. Update this spec if protocols need refinement

---

## 10. Taxonomy Changelog

| Date | Version | Change | Rationale |
|------|---------|--------|-----------|
| 2026-02-06 | v1.0 | Initial 7-type taxonomy | Based on 89 claims across 11 specimens. Added `teleological` to capture Dario/Demis-style outcome-anchored claims. |
| 2026-02-08 | v2.0 | Revised from 7 types to 7 (6 + unclassified). Dropped employee-deal (managerial directives, not purpose claims). Dissolved transformation-framing, sacrifice-justification, direction-under-uncertainty (surface features, not planes of meaning). Added higher-calling, survival, commercial-success, unclassified. Reframe: types now classify the END the claim invokes, not the rhetorical move. | Session 6 analytical review of all 294 claims revealed 3 types operated at different abstraction level than other 4. 198 claims reclassified, 96 unchanged, 0 deleted. |

---

## 11. Relationship to Other Components

| Component | Relationship |
|-----------|-------------|
| `registry.json` | Primary data store. This spec governs what goes in. |
| `scan-tracker.json` | Tracks coverage. Updated after each scan. |
| `analytical-notes.md` | Patterns and hypotheses derived from registry. Secondary to data. |
| `transcript-gap-queue.json` | Known transcript sources not yet scanned. Feeds Step 1. |
| `pending/*.json` | Staging area for claims before merge to registry. |
| `SKILL.md` | Scanning execution protocol. References this spec. |

---

## 12. Design Principles

1. **Registry is primary.** Patterns, hypotheses, and analysis are derived. The claims are the citable evidence.

2. **Verbatim or nothing.** Paraphrases don't enter the registry. If we can't quote it exactly, we don't have it.

3. **Provenance is sacred.** Every claim traces to a source. Undated or unsourced claims don't enter.

4. **Taxonomy is empirical.** Types emerge from data, not theory. Flag edge cases, revise when evidence accumulates.

5. **Methodology transparency.** Document what we searched, what we found, what we might have missed. "None found" is data.

6. **Never delete.** Claims are never removed from the registry. If a claim is recoded or flagged as problematic, annotate it — don't delete it.
