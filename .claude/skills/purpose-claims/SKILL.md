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

## Claim Type Taxonomy (v2.0)

See `research/purpose-claims/PURPOSE-CLAIMS-SPEC.md` for full definitions and taxonomy evolution protocol.

The organizing principle: **what END does this claim invoke to justify AI transformation?**

| Type | The claim says... | Core Question | Example |
|------|-------------------|---------------|---------|
| `utopian` | We are part of a civilizational transformation | "What epoch are we in?" | Hassabis "radical abundance"; Benioff "last generation of CEOs to manage only humans" |
| `teleological` | We exist to achieve a specific moral/social outcome | "What concrete outcome justifies our existence?" | Hassabis "cure all disease"; Bourla "save the world from cancer" |
| `higher-calling` | We answer to a duty that supersedes profit | "What obligation overrides economic logic?" | Amodei "we work on science out of proportion to profitability"; Ricks "we have a higher calling" |
| `identity` | We do this because of who we are | "Who are we?" | Teller "we spend most of our time breaking things"; Nadella "growth mindset" |
| `survival` | We must change or be left behind | "What threat demands action?" | Regev "we won't move fast enough"; Hudson "you don't delegate the revolution" |
| `commercial-success` | This will make the business perform better | "How does this improve business outcomes?" | Nadella "increase ROIC on capital spend"; Wells Fargo "better experience for customers" |

**Key distinctions:**
- **Utopian vs. Teleological vs. Higher-calling:** Utopian = epochal moment justifies it. Teleological = specific achievable outcome justifies it. Higher-calling = moral duty supersedes profit.
- **Survival vs. Commercial-success:** Survival = existential, adapt-or-die. Commercial-success = positive, this makes us better.
- **Identity vs. everything else:** The end IS the group's self-concept. Justification terminates in who we are.

**Multi-coding:** Use `secondaryType` field for claims with clear dual function. Flag edge cases in `taxonomyFlag` field.

**What is NOT a purpose claim:** Managerial directives ("AI training is required"), adoption metrics ("100% of workers use ChatGPT"), staffing facts ("I've reduced from 9,000 to 5,000"), market observations ("LLMs are commoditizing"). These don't invoke an end.

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

### Step 1: Load Context + Check Cross-Pollination Leads + Check Transcript Availability

**Load specimen context:**
- Read the specimen JSON (`specimens/{id}.json`)
- Note: CEO/leader name, existing `quotes[]` array, key `sources[]`, structural model
- Read scan-tracker (`research/purpose-claims/scan-tracker.json`)
- If `quality` is `rich` and `lastScanned` is within 30 days, skip unless explicitly requested

**Check for research cross-pollination leads:**
- Check `research/purpose-claims/pending/research-cross-pollination-*.json` for leads matching this specimen
- These are purpose-like quotes discovered during `/research` sessions — they may or may not pass our quality filters
- If leads exist for this specimen: use them as **seed URLs and quotes** to verify. Fetch the `sourceUrl`, confirm the quote is verbatim, apply the 3 quality filters, and promote to a full claim if it passes
- Cross-pollination leads have `"source": "research-cross-pollination"` — track this provenance in the claim's notes if promoted

**Check transcript availability (follow `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`):**
1. Read `research/transcript-gap-queue.json` for this specimen
2. If no entries exist OR entries are stale (>30 days old), run Phase 1 discovery
3. Prioritize sources by quality: native > third-party > auto-generated
4. For `transcriptAccess: manual-required` sources, queue for user if high-priority specimen

### Step 2: Mine Existing Specimen Data
- Check the specimen's `quotes[]` array for any that qualify as purpose claims
- Check `layers[].keyFindings` for quoted material
- Re-code qualifying quotes using the taxonomy — these are "free" claims already in our data

### Step 3: Search for New Claims
Use the source registry sources. Prioritize by source priority list above.

**Search queries** (adapt CEO name per specimen — 5 queries, consolidated for speed):
1. `"[CEO Name]" AI purpose OR mission OR vision OR strategy OR transformation`
2. `"[CEO Name]" AI "north star" OR "we exist" OR "becoming" OR "unlike" OR "different from"` — *"North star" and competitive positioning are high-signal purpose phrases.*
3. `"[Company Name]" AI earnings call OR memo OR letter employees OR shareholders`
4. `"[CEO Name]" AI workforce OR reskilling OR investment OR CapEx OR "long-term"`
5. `"[Company Name]" "[CEO Name]" AI interview OR podcast OR transcript`

**For earnings calls specifically:**
- `"[Company Name]" Q4 2025 OR Q3 2025 earnings call AI`
- Look for CEO/CFO opening remarks — purpose framing often appears in the first 5 minutes

**Transcript deep-scans (highest yield for verbatim claims):**
Many podcasts publish full transcripts on their Substacks or websites. When a specimen's sources include a podcast with available transcripts, fetch the full transcript and scan it directly — this is the single best source for verbatim purpose claims because you get exact wording in conversational context. Check the source registry for sources with `transcriptsAvailable: true`. Leaders in long-form podcast conversations often make purpose claims they wouldn't make in earnings calls or press — identity, higher-calling, and survival claims are especially common in this format.

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
Scan the next N unscanned specimens from the tracker (max 4 per batch). Prioritize by:
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
2. **Launch N background agents** using the Task tool with `model: "opus"` (Opus produces higher quality analysis and completes more reliably than Sonnet for web scraping)
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

Use the Task tool with `subagent_type: "general-purpose"`, `model: "opus"`, and `run_in_background: true`:

```
You are scanning specimen "{specimen-id}" for purpose claims. COMPLETE THIS IN UNDER 25 MINUTES.

TASK: Search for verbatim purpose claims by leaders at {org-name}, made in the context of AI adaptation.

## SPEED RULES — Read These First

1. **NEVER make parallel WebFetch calls.** Fetch URLs ONE AT A TIME, sequentially. Parallel fetches cause sibling-error cascades where one 403 kills all concurrent fetches.
2. **One retry max per URL.** If WebFetch fails, try ONE alternative URL. If that fails too, skip and move on. Do NOT retry the same URL.
3. **One retry max per search.** If WebSearch fails, retry once. If it fails again, note the failure and move on.
4. **Stop fetching after 6 URLs.** Even if you found more promising links, 6 fetched pages is enough. Prioritize quality over quantity.
5. **Skip paywalled/blocked domains.** These always 403: bloomberg.com, wsj.com, ft.com, seekingalpha.com (premium), investing.com. Don't bother fetching them.

## Workflow

1. Run the 5 search queries below using WebSearch (one at a time)
2. From ALL search results, pick the 4-6 most promising URLs (articles with direct quotes, transcripts, press releases with CEO statements)
3. Fetch each URL ONE AT A TIME using WebFetch
4. Mine fetched content for verbatim quotes that qualify as purpose claims
5. ALSO mine the existing specimen quotes listed below
6. Write all qualifying claims to the output file

## Specimen Context

- CEO/Leader: {leader-name} ({leader-title})
- Structural model: M{N} ({model-name})
- Key existing quotes: {list any from specimen JSON}
- Key sources: {list source URLs from specimen JSON}

## Claim Types (6 types, v2.0 taxonomy — classify by what END the claim invokes)

- utopian: Civilizational transformation, new era. Epochal scale. "What epoch are we in?"
- teleological: Specific moral/social outcome. Achievable/falsifiable. "What outcome justifies our existence?"
- higher-calling: Moral duty supersedes profit. Obligation overrides economics. "What obligation overrides economic logic?"
- identity: Organizational character, values, culture. "Who are we?" Justification terminates in collective identity.
- survival: Adapt-or-die. Existential threat. Status quo not viable. "What threat demands action?"
- commercial-success: Business performance, efficiency, growth, customer experience. "How does this improve outcomes?"

NOT purpose claims (do NOT collect): managerial directives, adoption metrics, staffing facts, market observations, HR mandates.

## Quality Filters (all three required)

1. Verbatim exact words only — no paraphrasing
2. Made in context of AI adaptation — not generic mission statements
3. Traceable source with URL — no URL, no claim

## Search Queries — Run ALL 5

1. "{leader-name}" AI purpose OR mission OR vision OR strategy OR transformation
2. "{leader-name}" AI "north star" OR "we exist" OR "becoming" OR "unlike" OR "different from"
3. "{org-name}" AI earnings call OR memo OR letter employees OR shareholders
4. "{leader-name}" AI workforce OR reskilling OR investment OR CapEx OR "long-term"
5. "{org-name}" "{leader-name}" AI interview OR podcast OR transcript

{additional-specimen-specific-queries}

## WebFetch Instructions

Fetch URLs ONE AT A TIME. After running all searches, prioritize:
1. **Podcast/interview transcripts** — Leaders speak freely, richest claims
2. **Earnings call coverage** — CEO prepared remarks with purpose framing
3. **Long-form press profiles** — Multiple direct quotes (skip news briefs)
4. **Internal memos (when published)** — Raw purpose language

Prompt WebFetch with: "Extract all direct quotes attributed to {leader-name} or other {org-name} executives about AI strategy, transformation, workforce, mission, or long-term vision. Include surrounding context."

## Output

Write a JSON file to: {output-path}

{
  "specimenId": "{specimen-id}",
  "scannedDate": "YYYY-MM-DD",
  "claimsFound": N,
  "quality": "rich|adequate|none",
  "searchesCompleted": N,
  "urlsFetched": N,
  "searchFailures": ["queries that failed"],
  "fetchFailures": ["URLs that could not be accessed"],
  "claims": [
    {
      "id": "{specimen-id}--{NNN}",
      "specimenId": "{specimen-id}",
      "claimType": "one of 6 types: utopian|teleological|higher-calling|identity|survival|commercial-success",
      "secondaryType": "null or one of 6 types",
      "text": "EXACT VERBATIM QUOTE",
      "speaker": "full name",
      "speakerTitle": "title",
      "context": "occasion and AI topic",
      "rhetoricalFunction": "what organizational work this claim does",
      "source": "source name",
      "sourceUrl": "URL",
      "sourceType": "Earnings Call | Podcast | Interview | Internal Memo | Shareholder Letter | Press | Speech | Social Media",
      "sourceDate": "YYYY-MM-DD or YYYY-MM",
      "collectedDate": "2026-02-XX",
      "transcriptSource": true | false,
      "taxonomyFlag": null,
      "notes": ""
    }
  ],
  "specimenEnrichment": {
    "keyFindings": ["3-5 analytical observations about this specimen's purpose rhetoric — what patterns, surprises, or distinctive features you noticed"],
    "rhetoricalPatterns": ["2-4 named patterns in how leaders frame AI transformation — e.g., 'Two-register communication: epochal for employees, measured for investors'"],
    "comparativeNotes": "1-2 paragraphs comparing this specimen's rhetorical profile to others in the collection. What makes it distinctive? What is the mirror image?",
    "notableAbsences": "What claim types or speakers are missing, and why that matters analytically. 'None' is data.",
    "correctedLeaderInfo": "Any corrections to leader names/titles in the specimen file. null if none.",
    "claimTypeDistribution": { "utopian": 0, "teleological": 0, "higher-calling": 0, "identity": 0, "survival": 0, "commercial-success": 0 }
  },
  "scanNarrative": "2-4 paragraphs of markdown prose documenting your journey through the sources. Write in first person as a field researcher. Include: which searches yielded results, which URLs were blocked or empty, what surprised you, what patterns emerged mid-scan, what you would look for if scanning again. This becomes a field journal entry visible on the app."
}

**specimenEnrichment is REQUIRED.** Always populate keyFindings and rhetoricalPatterns — they are displayed on the specimen card and purpose claims browser. Even for thin specimens, note what you observed (or didn't find). comparativeNotes and notableAbsences can be null if nothing noteworthy.

**scanNarrative is REQUIRED.** This is your field notebook. Write it after completing the scan, reflecting on the research journey. It flows into the field journal and helps future researchers understand what was tried.

If no qualifying claims found, write the file with claims: [] and quality: "none". Still write specimenEnrichment (noting what you searched and why nothing was found) and scanNarrative.
```

### Merge Protocol (run by orchestrator after all agents finish)

**Only the orchestrator writes to shared files.** This prevents race conditions.

1. `ls research/purpose-claims/pending/` — list all completed agent outputs
2. Read each `pending/{specimen-id}.json` file
3. Append all claims to `research/purpose-claims/registry.json` (single write)
4. Update each specimen's entry in `research/purpose-claims/scan-tracker.json` (single write)
5. **Write enrichment file**: For each pending file, normalize `specimenEnrichment` and write to `research/purpose-claims/enrichment/{specimen-id}.json`. This file is read by the site and displayed on the specimen card and purpose claims browser.
6. **Write scan narrative to field journal**: If `scanNarrative` is present, write it as a markdown file to `research/purpose-claims/sessions/YYYY-MM-DD-scan-{specimen-id}.md`. This is automatically discovered by the field journal.
7. **Process correctedLeaderInfo**: Note any leader corrections for specimen updates in the next `/curate` pass.
8. Write a batch session file to `research/purpose-claims/sessions/YYYY-MM-DD-batch-{description}.md`
9. Read `research/purpose-claims/analytical-notes.md` and append any new patterns observed
10. Update `HANDOFF.md` with results and next targets
11. Move processed `pending/*.json` files to `pending/processed/`

### Recommended Batch Sizes

- **Max 4 specimens per batch** (prevents context overflow crashes)
- **Parallel background agents work.** Launch up to 4 agents simultaneously with `run_in_background: true`.
- **Always use `model: "opus"`** when launching agents. Opus produces higher quality rhetorical analysis and completes more reliably than Sonnet (which tends to crash during WebFetch phase).
- **Pre-flight check:** Verify `WebFetch` and `WebSearch` are in `~/.claude/settings.json` global permissions before starting a batch. If missing, agents will silently fail on web operations.
- Group specimens by richness: scan High-completeness specimens first (more data to mine)
- Each agent takes ~15-25 minutes with Opus model. If agents take >40 minutes, check for stuck retry loops.

### Known Failure Patterns

- **Sibling-error cascades:** If an agent makes parallel WebFetch calls and one returns 403, ALL sibling calls fail. This is why the template says "fetch ONE AT A TIME." If you see agents taking 30+ minutes, they are probably stuck in sibling-error retry loops.
- **Always-blocked domains:** bloomberg.com, wsj.com, ft.com, seekingalpha.com (premium), investing.com, klover.ai, aimagazine.com, biopharmadive.com always return 403. Don't fetch these.
- **JS-rendered pages:** Some sites (MIT Sloan Review, McKinsey) return empty content from WebFetch because they require JavaScript rendering. Skip these after one attempt.

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
3. Different claim types invoke different ENDS to justify transformation:
   - **Utopian** — we are part of a civilizational moment (authorizes CapEx at epochal scale)
   - **Teleological** — we exist to achieve a specific moral/social outcome (anchors transformation in mission)
   - **Higher-calling** — we answer to a duty that supersedes profit (rare, analytically important)
   - **Identity** — we do this because of who we are (maintains relational contracts through disruption)
   - **Survival** — we must change or be left behind (creates urgency without positive vision)
   - **Commercial-success** — this will make the business perform better (the baseline — standard business logic)
4. The type and frequency of purpose claims varies systematically with structural model, orientation, and industry

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

**Session end:** When done with purpose claims scanning, run `/handoff` to update the handoff document and session log.

$ARGUMENTS
