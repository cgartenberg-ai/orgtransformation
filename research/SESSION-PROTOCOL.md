# Research Session Protocol

## Core Research Question

Every observation gathered in a session must speak to this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

This is the filter. Before recording any finding, apply the **Relevance Test** (see below). Surface-level observations like "Company X adopted AI tools" without structural insight are not useful.

---

## Idempotency Rules

- **Never modify a previous session file.** Each session creates a new file. If you find corrections to a prior session, record them as new observations in the current session.
- **Check `source-registry.json` before scanning.** Only scan content published AFTER the `scannedThroughDate` for that source. This prevents duplicate work.
- **Research findings stay in the curation queue** (`research/queue.json`) until Phase 2 curates them into specimens. Phase 1 never touches specimen files directly.
- **Session files are append-only to the `sessions/` directory.** New sessions get new files; old sessions are never deleted or modified.

---

## Relevance Test

Before recording an observation, it must pass at least ONE of these three checks:

1. **Structural**: Does this tell us about organizational STRUCTURES — labs, teams, reporting lines, units, governance, resource allocation — not just that they're "using AI"?
2. **Tension**: Does it reveal how the org handles the TENSION between exploring new AI capabilities and executing on current operations? Look for: trade-offs, failures, pivots, dual structures, integration challenges.
3. **Specificity**: Is there concrete detail — names, numbers, headcount, budgets, timelines, direct quotes — not just generalities?

**If it fails all three, don't record it.**

If it passes at least one, record it and note which dimension(s) it addresses. This ensures every finding is substantively useful for the field guide.

---

## Research Path Check

Before starting, determine the research path:

- **General** (`/research` or `/research general`): Follow the full protocol below
- **Low-confidence** (`/research low-confidence`): Read `research/low-confidence-queue.json` and follow the targeted research protocol in the research SKILL.md. Skip the general scanning protocol.

---

## Pre-Session Setup

Before scanning anything:

- [ ] Read `specimens/source-registry.json` — identify which sources have `scannedThrough: null` (never scanned) and which have stale `scannedThroughDate` (not scanned recently)
- [ ] Read `sources.md` "Research Refresh Protocol" section for current weekly/monthly priorities
- [ ] Plan which sources to scan this session — aim for **multiple source types** (e.g., podcasts + substacks + press), prioritizing:
  1. Tier 1 sources never scanned
  2. Tier 1 sources with new content since `scannedThroughDate`
  3. Tier 2 sources never scanned
  4. Press keyword searches (always fresh)
- [ ] Record planned sources in session file frontmatter before starting

---

## Scanning by Source Type

### Podcasts

1. **Check the feed** for new episodes since `scannedThroughDate`
   - Web search: `[podcast name] latest episodes 2026`
   - Or fetch the podcast website / Apple Podcasts / Spotify listing

2. **Triage episodes using show notes** — don't deep-scan everything. Use the Episode Evaluation Criteria from `sources.md`:
   - **High Priority** (deep-scan): Guest is AI lab founder/leader, CAIO, or CEO discussing AI org structure; topic mentions venture studios, spin-offs, reorganization
   - **Medium Priority** (scan if time): CEO discusses AI strategy, enterprise AI deployment case study
   - **Low Priority** (skip): General AI trends, pure technical capabilities, policy/regulation

3. **For each high-priority episode**:
   - **Check for full transcripts first.** Many podcast sources publish full transcripts on their websites or Substacks — check the source registry for `transcriptsAvailable: true`. These are the highest-value sources because you get exact verbatim wording in context. Sources with confirmed transcripts: Cheeky Pint, Dwarkesh, Latent Space, Acquired, Conversations with Tyler, Lex Fridman, Cognitive Revolution. For sources without official transcripts, try podscripts.co or YouTube captions.
   - Keyword scan the transcript for: "lab", "team", "structure", "report to", "Chief AI", "CoE", "incubator", "spin-off", "venture", "explore", "execute", "pilot", "deploy", "headcount", "budget"
   - Deep-read sections around keyword hits
   - Apply Relevance Test to each potential finding
   - Record findings with timestamps, quotes, and full provenance

4. **Update source-registry.json** with the episode/date scanned through

### Substacks & Newsletters

1. **Check recent posts** (last 30 days) for each Tier 1 substack:
   - Stratechery, One Useful Thing, Not Boring, The Generalist, Import AI
   - Web search: `site:[substack-url] AI strategy OR AI lab OR AI organization 2026`

2. **Scan headlines and first paragraphs** — triage for relevance to the core question

3. **Deep-read relevant articles** — apply Relevance Test, extract findings with URLs

4. **Update source-registry.json**

### Press Keyword Searches

Run these searches (from `sources.md` lines 401-410) and scan results:

```
"AI lab" + [company name]
"AI incubator" + corporate
"AI spin-off" + [company name]
"Chief AI Officer" + appointed
"AI venture" + internal
"AI research" + commercialize
"product lab" + AI
"venture studio" + AI
```

Also run broader searches:
```
"AI reorganization" 2026
"AI team structure" 2026
"Chief AI Officer" hired 2026
"AI lab" launches 2026
```

For each relevant result: read the article, apply Relevance Test, record findings with full URL and date.

### SEC Filings & Earnings

1. Search EDGAR for key companies (list in `sources.md` lines 366-372)
2. Search filings for: "artificial intelligence", "machine learning", "R&D", "generative", "large language model"
3. Extract structural details: investment levels, headcount, reporting lines, new units

### Earnings Season Protocol

Earnings calls are our **highest-density source** for organizational structure signals. CEOs make on-the-record, legally binding statements about flattening, delayering, agent deployment, CapEx, and org design. Run dedicated earnings sessions during each quarterly window.

**When:** ~3-week window each quarter (roughly Jan/Feb, Apr/May, Jul/Aug, Oct/Nov). Check `research/earnings-calendar.json` for exact dates.

**Target companies:** See `research/earnings-calendar.json` for the full list with fiscal year mappings, priorities, and scan history. Currently 34 companies across 8 industries:
- **Critical** (scan every quarter): Microsoft, Meta, Amazon, Google/Alphabet, Salesforce
- **High** (scan every quarter when time permits): Pharma (Eli Lilly, Pfizer, Moderna, Sanofi), Financial Services (JPMorgan, UBS), Industrials (Siemens), Consumer (Walmart), Logistics (UPS), IT Services (Infosys), Enterprise Software (SAP, NVIDIA, Klarna)
- **Monitor** (scan selectively): Novo Nordisk, Roche, Citigroup, Wells Fargo, Bank of America, Schneider, ABB, Coca-Cola, Dow, Publicis, Duolingo, Pinterest, Palo Alto Networks, Shopify, Atlassian, Adobe, Tesla, Apple

**Casting a wide net:** Beyond the target list, earnings sessions should also search for *new* companies making structural AI announcements during earnings. Run broad searches like `"Chief AI Officer" OR "AI restructuring" earnings call 2026` to catch companies not yet in our collection. The target list tracks known specimens; earnings season is also a discovery mechanism.

**Per-company scan process:**

1. **Find the transcript** — Search: `[company] Q[N] [FY year] earnings call transcript`
   - Primary: Seeking Alpha, Motley Fool, company IR page
   - Note: Some are paywalled. Search for press summaries + analyst coverage as backup

2. **Keyword scan** — Use the keyword categories from `research/earnings-calendar.json`:
   - `structural`: reorganize, restructure, reporting line, Chief AI, CoE, new unit/division
   - `workforce`: headcount, delayer, flatten, fewer managers, reskill, redeploy, attrition
   - `investment`: CapEx, AI infrastructure, AI investment, data center, GPU, compute
   - `deployment`: agent, agentic, copilot, resolution rate, automation rate, AI product, deploy
   - `governance`: responsible AI, AI safety, AI governance, AI board/committee

3. **Deep-read around keyword hits** — Read 2-3 paragraphs of context around each hit. Apply Relevance Test.

4. **Extract findings** — For each relevant finding:
   - Direct quote from CEO/CFO (verbatim, with speaker and title)
   - Specific numbers (CapEx, headcount, metrics, ARR)
   - Structural signals (new units, reporting changes, role shifts)
   - Source: transcript URL + earnings date + collected date

5. **Update `research/earnings-calendar.json`** — Mark company/quarter as scanned, record session file and key findings

**Session naming:** Use type `earnings` — e.g., `2026-02-05-001-earnings-q4-2025-amazon-google.md`

**Discovery searches — casting a wide net:**

Earnings season isn't just for tracking known specimens. It's the best time to discover *new* organizations making structural AI moves, because every public company is required to speak. Run these broad discovery searches each earnings window:

```
"Chief AI Officer" OR "CAIO" earnings call transcript 2026
"AI restructuring" OR "AI reorganization" earnings call 2026
"center of excellence" AI earnings 2026
"AI lab" OR "AI division" earnings call 2026
"agentic" OR "AI agent" earnings call 2026
"generative AI" restructuring layoff earnings 2026
```

Also search by industry verticals we're underrepresented in:
```
"AI" earnings call 2026 healthcare OR hospital
"AI" earnings call 2026 insurance
"AI" earnings call 2026 manufacturing
"AI" earnings call 2026 energy OR utility
"AI" earnings call 2026 airline OR transportation
"AI" earnings call 2026 telecom
```

Any company surfaced by discovery searches that passes the Relevance Test → record as a new finding in the session file, even if it's not on the target list. This is how the herbarium grows.

**What makes earnings calls special:**
- **Legal accountability** — CEOs make statements under SEC disclosure rules. They can't hand-wave.
- **Comparative structure** — Same questions asked to every company each quarter = natural panel data.
- **Structural specificity** — Analyst Q&A probes org design decisions: "How are you structuring the AI team?" "What's the CapEx trajectory?"
- **Longitudinal tracking** — Quarter-over-quarter changes in narrative, spending, and structure are visible.

---

## During Scanning: Source Discovery

As you scan sources, watch for **new sources** not yet in `sources.md`:
- New podcasts mentioned by guests or hosts
- New substacks or newsletters referenced in articles
- Reports or white papers cited
- Conference talks or interviews linked

If you discover a new relevant source:
- Note it in the session file under "New Sources Discovered"
- Add it to `sources.md` in the appropriate tier/category
- Add it to `specimens/source-registry.json` with `scannedThrough: null`

---

## Quality Review

Before wrapping up the session, review all findings:

- [ ] Does every observation pass the Relevance Test?
- [ ] Does every fact have a source URL (or `[paywall]`/`[no URL]` with enough detail to locate)?
- [ ] Does every fact have both a Source Date and Collected Date?
- [ ] Are quotes verbatim with speaker, title, source, and timestamp?
- [ ] Were multiple source TYPES scanned (not just podcasts)?
- [ ] Were new sources discovered and recorded?

---

## Session Wrap-Up

- [ ] Complete the session file with all sections (Sources Scanned table, Organizations Observed, Source Index, Notes for Next Session)
- [ ] Update `specimens/source-registry.json` — set `scannedThrough` and `lastScanned` for each source covered
- [ ] Add session to `research/queue.json` with all organizations found
- [ ] If new sources were discovered, add them to **both** `sources.md` and `source-registry.json`
- [ ] **Update `research/SESSION-LOG.md`** — add a summary entry at the top with: sources scanned, orgs found (table with key finding per org), broader trends, new sources discovered, sources updated, follow-ups needed
- [ ] **Update `research/field-signals.json`** — see Field Signal Tracking below
- [ ] Run `node scripts/validate-workflow.js` to confirm consistency

---

## Field Signal Tracking

Field signals are macro-level observations that recur across multiple research sessions — trends, structural patterns, and emerging phenomena that aren't tied to a single specimen but emerge from the fieldwork as a whole.

**When:** At the end of every research session, after writing the Broader Trends section in the session file, review `research/field-signals.json` and update it.

**How:**

1. **Strengthen existing signals** — If this session's broader trends match existing signals:
   - Add the session ID to the signal's `sessions` array
   - Add any new specimen slugs to `relatedSpecimens`
   - Append new data points to `dataPoints` (with source + date)
   - Update `lastUpdated`

2. **Add new signals** — If this session surfaces a macro observation not yet tracked:
   - Create a new entry with a descriptive `id` (kebab-case)
   - Set `status: "active"`, `firstObserved` to today
   - Assign a `theme` from the existing set: `workforce`, `convergence`, `governance`, `structural-form`, `deployment-reality`, `talent`, `investment`, `explore-execute`
   - Include at least one data point with source citation

3. **Record counter-evidence** — If a finding contradicts an existing signal, add it to that signal's `counterEvidence` array rather than deleting the signal. Signals are append-only.

4. **Mark saturated** — If a signal has been observed in 5+ sessions and no new dimensions are emerging, set `status: "saturated"`. It's still tracked but no longer actively sought.

5. **Promote to insights** — When a signal has enough evidence density and specificity to become a formal claim, set `status: "promoted"` and `promotedTo: "INS-XXX"` (the insight ID in `synthesis/insights.json`). Promotion happens during Phase 3 (Synthesis), not during research.

**Signal lifecycle:** `active` → `saturated` → `promoted`

**Themes:**

| Theme | What it covers |
|-------|---------------|
| `workforce` | Headcount changes, layoffs, hiring patterns, role shifts |
| `convergence` | Blurring of explore/execute, structural convergence |
| `governance` | CAIO roles, reporting lines, oversight structures |
| `structural-form` | Lab types, CoE patterns, org design |
| `deployment-reality` | Gap between AI hype and actual deployment |
| `talent` | AI talent markets, retention, competition |
| `investment` | CapEx/OpEx shifts, infrastructure spend |
| `explore-execute` | How orgs balance exploration and execution |

---

## Session File Naming Convention

Session files follow a standardized naming pattern:

```
YYYY-MM-DD-NNN-<type>-<descriptor>.md
```

| Component | Description | Examples |
|-----------|-------------|---------|
| `YYYY-MM-DD` | Session date | `2026-02-01` |
| `NNN` | Three-digit sequence number for that date, starting at `001` | `001`, `002` |
| `<type>` | Session type (see table below) | `research`, `deep-scan`, `bulk-review` |
| `<descriptor>` | Brief slug describing scope | `podcasts-press`, `pharma-gap`, `jensen-huang` |

**Session types:**

| Type | When to use |
|------|-------------|
| `research` | Standard multi-source scanning session |
| `deep-scan` | Transcript-level scan of specific episodes or articles |
| `bulk-review` | Batch review/upgrade of existing specimens |
| `gap-coverage` | Targeted session to fill taxonomy or industry gaps |
| `earnings` | Quarterly earnings call transcript scanning session |

**Examples:**

```
2026-02-01-001-research-podcasts-press.md
2026-02-01-002-deep-scan-karpathy-alphabet.md
2026-02-03-001-bulk-review-model6-specimens.md
2026-02-05-001-gap-coverage-financial-services.md
2026-02-05-002-earnings-q4-2025-amazon-google.md
```

The sequence number (`NNN`) ensures unique, sortable filenames when multiple sessions run on the same date. Check existing files for the date before choosing the next number.

---

## Session File Format

```yaml
---
session_date: "YYYY-MM-DD"
sources_planned: ["source-id-1", "source-id-2", "press-keyword-search"]
sources_scanned: ["source-id-1", "source-id-2", "press-keyword-search"]
source_types_covered: ["podcast", "substack", "press"]
new_sources_discovered: []
organizations_found:
  - id: "org-slug"
    status: "new"        # new | existing | evolution
  - id: "org-slug-2"
    status: "existing"
curation_status: "pending"
---
```

Then follow the output format from `skills/ambidexterity-research/SKILL.md` for the body content.
