---
name: purpose-claims
description: "Search for verbatim purpose claims by leaders at specimen organizations, made in the context of AI adaptation. Codes claims by type, retains exact wording and full source provenance."
disable-model-invocation: true
---

# Purpose Claims: Scanning for How Leaders Authorize AI Transformation

## Core Research Question

> **"How do leaders use purpose claims to authorize structural transformation in the AI era?"**

Purpose claims are statements by organizational leaders that invoke mission, identity, values, or vision to justify, explain, or direct AI-driven structural changes. We are looking for the **exact words** leaders use — not paraphrased descriptions. Every claim must be verbatim, traceable to a specific source with URL, and made in the context of AI adaptation.

---

## Claim Type Taxonomy

| Type | Definition | Example Pattern |
|------|-----------|-----------------|
| `utopian` | Grandiose, future-state, world-changing language. "The world is transforming and we exist to shape a new reality." | Zuckerberg $115-135B CapEx framing; McDermott "obliterate 20th century org charts" |
| `identity` | Organizational self-definition invoked to explain AI choices. "We exist to help others" / "This is who we are." | Nadella growth mindset / "empower every person"; Eli Lilly breakthrough therapeutics identity |
| `transformation-framing` | The organization is changing form, and here's why. "We are becoming..." | Jassy "it's culture"; Wang "fewer conversations to make a decision" |
| `employee-deal` | Resets the implicit employment contract. "What we now expect from our people." | Lutke "prove AI can't do it"; Accenture "exiting non-reskillable" |
| `sacrifice-justification` | Acknowledges cost/loss and connects it to purpose. "Why this pain is worth it." | Accenture $865M restructuring framing; UPS $9B automation investment |
| `direction-under-uncertainty` | Purpose substitutes for profit signals. "We're betting on X even though ROI is unclear." | SK Telecom $3.6B ring-fenced; Eli Lilly 18-year time horizons |

**Note:** Claims may have a secondary type. Record the primary type in `claimType` and note the secondary in `notes`.

---

## Quality Filters — All Three Must Be Met

1. **Verbatim exact words.** The `text` field must be the speaker's actual words. No paraphrasing, no summarizing. If you cannot find exact wording, do not record the claim. Partial quotes are acceptable if clearly marked with [...] for omitted portions.

2. **AI-adaptation context.** The claim must be made in the context of explaining how the organization is adapting to AI. A generic mission statement from a corporate website does NOT count. A CEO invoking that same mission statement to explain an AI restructuring DOES count.

3. **Traceable source with URL.** Every claim must have a `sourceUrl`. No URL, no claim.

---

## Source Registry (same sources as /research)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/source-registry.json"`

### Source Priority for Purpose Claims

1. **Earnings calls** — On-the-record, legally binding context. Highest credibility.
2. **Internal memos** — When leaked/published. Raw purpose language.
3. **Podcast/interview transcripts** — Full text available on Substacks or websites. Conversational context with exact wording guaranteed. Higher value than audio-only podcasts. Key transcript-rich sources:
   - Cheeky Pint (`cheekypint.substack.com`) — full transcripts for all episodes
   - Dwarkesh Podcast (`dwarkesh.com`) — full transcripts
   - Latent Space (`latent.space`) — full transcripts on Substack
   - Acquired (`acquired.fm`) — full transcripts on website
   - Conversations with Tyler (`conversationswithtyler.com`) — full transcripts on website
   - Lex Fridman (`lexfridman.com`) — full transcripts on website
   - Cognitive Revolution (`cognitiverevolution.ai`) — full transcripts on website
   - Check source registry for `transcriptsAvailable: true` flag on other sources
4. **Podcasts / long-form interviews (audio-only)** — Leaders speak freely. Rich purpose framing. But requires paraphrase verification if no transcript.
5. **Shareholder letters** — Annual framing statements. Often identity/direction claims.
6. **Press articles** — Quotes within reporting. Verify exact wording.
7. **Conference keynotes** — Public stage purpose claims. Often utopian.

---

## Specimen Registry (know who we're scanning)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/registry.json"`

---

## Per-Specimen Scanning Protocol

For each specimen:

### Step 1: Load Context
- Read the specimen JSON (`specimens/{id}.json`)
- Note: CEO/leader name, existing `quotes[]` array, key `sources[]`, structural model
- Read scan-tracker (`research/purpose-claims/scan-tracker.json`)
- If `quality` is `rich` and `lastScanned` is within 30 days, skip unless explicitly requested

### Step 2: Mine Existing Specimen Data
- Check the specimen's `quotes[]` array for any that qualify as purpose claims
- Check `layers[].keyFindings` for quoted material
- Re-code qualifying quotes using the taxonomy — these are "free" claims already in our data

### Step 3: Search for New Claims
Use the source registry sources. Prioritize by source priority list above.

**Search queries** (adapt CEO name per specimen):
- `"[CEO Name]" AI transformation purpose OR mission OR "we exist" OR "becoming"`
- `"[CEO Name]" AI restructuring OR reorganization vision OR strategy`
- `"[CEO Name]" AI employees OR workforce OR "new expectations" OR reskilling`
- `"[CEO Name]" AI investment OR CapEx OR "long-term" OR "betting on"`
- `"[CEO Name]" "north star" AI` — *"North star" is a high-signal purpose phrase: leaders use it to anchor structural transformation in identity/mission language. Always search for it.*
- `"[Company Name]" earnings call AI purpose OR mission OR identity`
- `"[Company Name]" AI memo OR letter employees OR shareholders`
- `"[CEO Name]" AI "unlike" OR "different from" OR "not like" OR "competitors" OR "other companies"` — *Competitive positioning via purpose: leaders define their organization's identity by contrasting against competitors or peers. Counter-positioning claims are high-signal because they reveal how purpose does boundary work — authorizing specific structural choices by defining what the org is NOT. Three known cases: Amodei ("strong compass" vs other AI labs), Zuckerberg (personal empowerment vs centralized superintelligence), Ricks ("higher calling" vs intermediaries who see AI as threat).*

**For earnings calls specifically:**
- `"[Company Name]" Q4 2025 OR Q3 2025 earnings call AI`
- Look for CEO/CFO opening remarks — purpose framing often appears in the first 5 minutes

**Transcript deep-scans (highest yield for verbatim claims):**
Many podcasts publish full transcripts on their Substacks or websites. When a specimen's sources include a podcast with available transcripts, fetch the full transcript and scan it directly — this is the single best source for verbatim purpose claims because you get exact wording in conversational context. Check the source registry for sources with `transcriptsAvailable: true`. Leaders in long-form podcast conversations often make purpose claims they wouldn't make in earnings calls or press — identity claims, direction-under-uncertainty, and employee-deal claims are especially common in this format.

### Step 4: Record Each Claim
For each verbatim claim found, create an entry in `research/purpose-claims/registry.json`:

```json
{
  "id": "{specimen-id}--{NNN}",
  "specimenId": "meta-ai",
  "claimType": "utopian",
  "text": "EXACT VERBATIM QUOTE — no paraphrasing",
  "speaker": "Mark Zuckerberg",
  "speakerTitle": "CEO, Meta",
  "context": "Q4 2025 earnings call, discussing $60-65B AI CapEx guidance for 2025",
  "rhetoricalFunction": "Uses world-historical framing to authorize massive capital commitment that cannot be justified by near-term ROI. Transforms a financial decision into a civilizational bet.",
  "source": "Meta Q4 2025 Earnings Call Transcript",
  "sourceUrl": "https://...",
  "sourceType": "Earnings Call",
  "sourceDate": "2025-10-30",
  "collectedDate": "2026-02-03",
  "notes": "Secondary type: direction-under-uncertainty. Cross-reference with Meta's 4th org restructuring."
}
```

**Claim ID format:** `{specimen-id}--{NNN}` where NNN is a zero-padded sequential number (001, 002, etc.).

### Step 5: Update Scan Tracker
After scanning a specimen, update `research/purpose-claims/scan-tracker.json`:
- Set `lastScanned` to today's date
- Set `claimsFound` to the count
- Set `quality`:
  - `rich` — 3+ claims found
  - `adequate` — 1-2 claims found
  - `none` — scanned, no qualifying claims found (this is data too)

### Step 6: Write Session File
Write a dated session file to `research/purpose-claims/sessions/YYYY-MM-DD-{description}.md`:

```markdown
# Purpose Claims Session: [date]

## Specimens Scanned
- [specimen-id]: [N claims found] ([quality])
- ...

## Claims Found
### [specimen-id]
1. **[claim type]** — "[first ~20 words of quote]..." — [speaker], [source]
   - Rhetorical function: [brief]
...

## Analytical Notes
[Cross-cutting observations, patterns, surprises]

## Next Steps
[Which specimens to scan next, any sources to prioritize]
```

---

## Invocation Modes

### Single Specimen
```
/purpose-claims [specimen-id]
```
Scan one specimen following the full protocol above.

### Batch Mode
```
/purpose-claims --batch N
```
Scan the next N unscanned specimens from the tracker. Prioritize by:
1. High-completeness specimens first (more existing data to mine)
2. Specimens with known CEO/founder names
3. Active status over Stubs

### Analysis Mode
```
/purpose-claims --analyze
```
Don't scan — instead analyze the existing claims registry:
- Distribution by claim type
- Which specimens are richest
- Cross-cutting patterns
- Connection to synthesis insights and mechanisms
- Gaps to fill

---

## Background Agent Execution

This skill is designed to run as parallel background agents. Each agent scans one specimen independently.

### How to Run in Parallel

The orchestrator (you, in the main conversation) should:

1. **Read the scan tracker** to identify unscanned specimens
2. **Launch N background agents** using the Task tool, one per specimen
3. Each agent receives a self-contained prompt (see template below)
4. **Collect results** from each agent when done
5. **Merge results** into `registry.json`, update `scan-tracker.json`, write session file
6. **Update analytical-notes.md** with any new cross-cutting patterns

### Concurrency Design: No Write Conflicts

**Critical:** Agents do NOT write to shared files (`registry.json`, `scan-tracker.json`). Each agent writes to its own specimen-specific output file. The orchestrator merges after all agents finish.

```
WRITE PATTERN:
  Agent 1 → research/purpose-claims/pending/microsoft.json     (agent writes)
  Agent 2 → research/purpose-claims/pending/shopify.json       (agent writes)
  Agent 3 → research/purpose-claims/pending/servicenow.json    (agent writes)
  ...
  Orchestrator reads all pending/*.json → merges into registry.json  (single writer)
  Orchestrator updates scan-tracker.json                              (single writer)
  Orchestrator deletes pending/*.json after successful merge
```

### Background Agent Prompt Template

Use the Task tool with `subagent_type: "general-purpose"` and `run_in_background: true`:

```
You are scanning specimen "{specimen-id}" for purpose claims.

TASK: Search for verbatim purpose claims by leaders at {org-name}, made in the context of AI adaptation.

## CRITICAL: Web Search Is Your Primary Job

Your main activity is WEB RESEARCH, not file analysis. You MUST use the WebSearch tool to run EVERY search query listed below. Do not skip queries. Do not fall back to only analyzing existing specimen data.

**Mandatory workflow:**
1. Run ALL search queries below using WebSearch (one at a time, all of them)
2. From search results, identify the 5-8 most promising URLs (articles with direct quotes, earnings call coverage, interview transcripts, press releases with CEO statements)
3. Use WebFetch on each promising URL to extract the full text
4. Read the fetched content carefully for verbatim quotes that qualify as purpose claims
5. ALSO mine the existing specimen quotes listed below — but this is supplementary, not your primary source
6. Write all qualifying claims to the output file

**If WebSearch fails on a query:** Retry it once. If it fails again, note the failure in your output and move to the next query. Do NOT silently skip failed searches.

**If WebFetch fails on a URL:** Try an alternative URL from search results. Note any URLs you could not access.

**Success criteria:** A good scan runs 6+ web searches, fetches 4+ source pages, and evaluates 10+ candidate quotes for quality filter compliance. If you finish with fewer than 3 web searches completed, your scan is incomplete.

## Specimen Context

- CEO/Leader: {leader-name} ({leader-title})
- Structural model: M{N} ({model-name})
- Key existing quotes: {list any from specimen JSON}
- Key sources: {list source URLs from specimen JSON}

## Claim Types

- utopian: Grandiose, future-state, world-changing language
- identity: Organizational self-definition invoked to explain AI choices
- transformation-framing: "We are becoming..." — org changing form
- employee-deal: Resets the implicit employment contract
- sacrifice-justification: Acknowledges cost/loss, connects to purpose
- direction-under-uncertainty: Purpose substitutes for profit signals

## Quality Filters (all three required)

1. Verbatim exact words only — no paraphrasing
2. Made in context of AI adaptation — not generic mission statements
3. Traceable source with URL — no URL, no claim

## Search Queries — Run ALL of These

1. "{leader-name}" AI transformation purpose OR mission OR "we exist" OR "becoming"
2. "{leader-name}" AI restructuring OR reorganization vision OR strategy
3. "{leader-name}" "north star" AI
4. "{org-name}" earnings call AI purpose OR mission OR identity
5. "{org-name}" AI memo OR letter employees OR shareholders
6. "{leader-name}" AI "unlike" OR "different from" OR "not like" OR "competitors"
7. "{leader-name}" AI workforce OR "new expectations" OR reskilling
8. "{leader-name}" AI investment OR CapEx OR "long-term" OR "betting on"

{additional-specimen-specific-queries}

## WebFetch Priority Targets

After running searches, prioritize fetching these source types (they yield the richest verbatim quotes):
1. **Earnings call transcripts or coverage** — CEO prepared remarks contain purpose framing
2. **Podcast/interview transcripts** — Leaders speak freely, identity and direction claims concentrate here
3. **Internal memos (when published)** — Raw purpose language
4. **Press articles with multiple direct quotes** — Look for long-form profiles, not news briefs
5. **Shareholder letters / annual reports** — Annual purpose framing statements

When fetching a page, prompt WebFetch with: "Extract all direct quotes attributed to {leader-name} or other {org-name} executives, especially quotes about AI strategy, organizational transformation, workforce changes, company mission/purpose, or long-term vision. Include the full surrounding context for each quote."

## Output

IMPORTANT: Write your results to a per-specimen file. Do NOT write to registry.json or scan-tracker.json.

Write a JSON file to: {output-path}

The file should contain:
{
  "specimenId": "{specimen-id}",
  "scannedDate": "YYYY-MM-DD",
  "claimsFound": N,
  "quality": "rich|adequate|none",
  "searchesCompleted": N,
  "urlsFetched": N,
  "searchFailures": ["list any queries that failed"],
  "fetchFailures": ["list any URLs that could not be accessed"],
  "claims": [
    {
      "id": "{specimen-id}--{NNN}",
      "specimenId": "{specimen-id}",
      "claimType": "one of 6 types",
      "text": "EXACT VERBATIM QUOTE",
      "speaker": "full name",
      "speakerTitle": "title",
      "context": "occasion and AI topic",
      "rhetoricalFunction": "what organizational work this claim does",
      "source": "source name",
      "sourceUrl": "URL",
      "sourceType": "Earnings Call | Podcast | Interview | Internal Memo | Shareholder Letter | Press | Conference",
      "sourceDate": "YYYY-MM-DD or YYYY-MM",
      "collectedDate": "2026-02-XX",
      "notes": "analytical notes, including VERIFICATION NEEDED flag if exact wording confidence is less than high"
    }
  ]
}

If no qualifying claims found, write the file with claims: [] and quality: "none".
```

### Merge Protocol (run by orchestrator after all agents finish)

**Only the orchestrator writes to shared files.** This prevents race conditions.

1. `ls research/purpose-claims/pending/` — list all completed agent outputs
2. Read each `pending/{specimen-id}.json` file
3. Append all claims to `research/purpose-claims/registry.json` (single write)
4. Update each specimen's entry in `research/purpose-claims/scan-tracker.json` (single write)
5. Write a session file to `research/purpose-claims/sessions/YYYY-MM-DD-batch-{description}.md`
6. Read `research/purpose-claims/analytical-notes.md` and append any new patterns observed
7. Update `HANDOFF.md` with results and next targets
8. Delete processed `pending/*.json` files (or move to `pending/processed/`)

### Recommended Batch Sizes

- **3-5 agents in parallel** is optimal (balances throughput vs. merge complexity)
- Group specimens by richness: scan High-completeness specimens first (more data to mine)
- Each agent takes ~2-5 minutes depending on source availability

### Priority Queue for Next Batches

Maintain a priority list in HANDOFF.md. Suggested ordering:
1. **High-value first:** Specimens with known CEO names, rich existing quotes, High/Medium completeness
2. **Thematic batches:** Group by claim type you expect (e.g., all pharma for direction-under-uncertainty)
3. **Stubs last:** Low-completeness specimens unlikely to yield claims from existing data

---

## What We're Building Toward

This claim registry serves the paper on **purpose and AI-era organizational transformation**. The theoretical argument:

1. AI creates structural uncertainty that standard economic signals (ROI, market price) cannot resolve
2. Leaders use purpose claims to authorize transformations that lack clear profit justification
3. Different claim types do different organizational work:
   - **Utopian** claims authorize CapEx at civilizational scale
   - **Identity** claims maintain relational contracts through structural disruption
   - **Employee-deal** claims renegotiate the employment contract
   - **Sacrifice-justification** claims make painful changes feel meaningful
   - **Direction-under-uncertainty** claims substitute for absent profit signals
4. The type and frequency of purpose claims varies systematically with structural model and orientation

The registry provides the empirical base. Every claim is citable, traceable, and coded.

---

## Analytical Notes (accumulating insights)

After each session (single or batch), update `research/purpose-claims/analytical-notes.md`:
- Add any new patterns to "Emerging Patterns" section
- Update hypotheses with confirming/disconfirming evidence
- Update the session log table at the bottom
- Add cross-references to field insights as they emerge

This file is the intellectual spine of the purpose claims project. It accumulates across sessions and feeds directly into the paper.

---

## Guardrails

- **Never paraphrase.** If you can't find exact words, don't record it.
- **Never invent context.** If you're unsure whether a claim was made in AI-adaptation context, note the uncertainty — don't assume.
- **Always include URL.** No URL, no claim. Period.
- **Don't force-fit.** If a quote doesn't clearly fit one of the six types, note it in `notes` with your reasoning and assign the closest type. Some claims may genuinely be ambiguous.
- **"None" is data.** A specimen with zero purpose claims after thorough scanning is an interesting finding — it may indicate purely technocratic leadership or a different authorization mechanism.

$ARGUMENTS
