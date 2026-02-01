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
   - Search for transcript (podscripts.co, podcast website, YouTube captions)
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

### SEC Filings & Earnings (When Applicable)

1. Search EDGAR for key companies (list in `sources.md` lines 366-372)
2. Search filings for: "artificial intelligence", "machine learning", "R&D", "generative", "large language model"
3. Extract structural details: investment levels, headcount, reporting lines, new units

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
- [ ] Run `node scripts/validate-workflow.js` to confirm consistency

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

**Examples:**

```
2026-02-01-001-research-podcasts-press.md
2026-02-01-002-deep-scan-karpathy-alphabet.md
2026-02-03-001-bulk-review-model6-specimens.md
2026-02-05-001-gap-coverage-financial-services.md
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
