---
name: research
description: "Phase 1: Execute a research session — scan sources for organizational AI structure findings following the session protocol"
disable-model-invocation: false
---

# Phase 1: Research Session

You are executing a research session for the Ambidexterity Field Guide project.

## Core Research Question

Every observation you gather must speak to this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

## Session Protocol

Follow this protocol step by step. Do NOT skip steps.

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/SESSION-PROTOCOL.md"`

## Transcript Discovery Protocol

For systematic transcript source discovery, follow:

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/TRANSCRIPT-DISCOVERY-PROTOCOL.md"`

## What to Look For and Output Format

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/skills/ambidexterity-research/SKILL.md"`

## Current Source Registry (check this FIRST to see what's been scanned)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/source-registry.json"`

## Current Curation Queue (check for pending items)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/queue.json"`

## Session Log (see what previous sessions found)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/SESSION-LOG.md"`

## Dual-Path Research

This skill supports two research paths. Specify which path when invoking:

### General Research (default)
`/research` or `/research general`

Standard multi-source scanning for new specimens and updates. Follows the full session protocol above.

### Low-Confidence Targeted Research
`/research low-confidence`

Targeted research to improve classification confidence for specific specimens. Process:

1. Read `research/low-confidence-queue.json` — identify specimens with `"status": "pending"`
2. For each pending specimen, use `whatToLookFor` to guide targeted searches
3. Search for specific structural details, org charts, reporting lines, headcounts
4. If new evidence found: update the specimen JSON (add layer, adjust confidence, update sources)
5. Increment `researchCycles` and set `lastResearchDate` in the queue entry
6. If confidence improves to Medium or High: set queue entry status to `"resolved"`
7. If no useful evidence found after 2+ cycles: set status to `"deferred"` — the specimen stays as-is until new information surfaces naturally
8. Run `node scripts/validate-workflow.js` to confirm consistency

The low-confidence path is intentionally narrow — don't expand into general research during these sessions. Stay focused on the specific specimens and questions in the queue.

## Your Task

Execute a complete research session following the protocol above:

1. Check the source registry for coverage gaps
2. Plan which sources to scan (multiple types: podcasts + substacks + press)
3. Triage episodes/articles using show notes and headlines
4. Deep-scan high-priority content, applying the Relevance Test to every finding
5. Record findings in a new session file: `research/sessions/YYYY-MM-DD-{description}.md`
6. Update source-registry.json, research/queue.json, SESSION-LOG.md
7. If new sources discovered, add to sources.md AND source-registry.json
8. Run `node scripts/validate-workflow.js` to confirm consistency

$ARGUMENTS

---

## Background Agent Execution

This skill supports parallel background agents for research sessions. Unlike purpose claims (one agent per specimen), research parallelizes by **scan task** — the orchestrator plans the session, then dispatches independent tasks to agents.

### Parallelization Unit: Scan Tasks

Each agent receives a single, self-contained scan task. The orchestrator defines tasks during session planning.

| Task Type | Example | Scope |
|-----------|---------|-------|
| `earnings` | "Scan Microsoft Q4 2025 earnings call" | 1-2 companies per agent |
| `podcast-deep-scan` | "Deep-scan No Priors Ep 147 Emil Michael" | 1 episode per agent |
| `press-keyword` | "Search 'Chief AI Officer' hired 2026" | 1 keyword batch per agent |
| `transcript-scan` | "Scan Cheeky Pint Greg Brockman transcript" | 1 transcript per agent |
| `specimen-targeted` | "Low-confidence research for roche-genentech" | 1 specimen per agent |

### Concurrency Design: No Write Conflicts

**Critical:** Agents do NOT write to shared files (`queue.json`, `source-registry.json`, `SESSION-LOG.md`). Each agent writes to its own task-specific output file. The orchestrator merges after all agents finish.

```
WRITE PATTERN:
  Agent 1 → research/pending/earnings-microsoft-q4-2025.json     (agent writes)
  Agent 2 → research/pending/podcast-no-priors-ep147.json         (agent writes)
  Agent 3 → research/pending/press-caio-search-2026.json          (agent writes)
  Agent 4 → research/pending/transcript-cheeky-pint-brockman.json (agent writes)
  ...
  Orchestrator reads all pending/*.json → merges into queue.json, session file  (single writer)
  Orchestrator updates source-registry.json, SESSION-LOG.md                     (single writer)
  Orchestrator deletes pending/*.json after successful merge
```

### How to Run in Parallel

The orchestrator (you, in the main conversation) should:

1. **Plan the session** — Read source-registry, identify coverage gaps, decide which tasks to dispatch
2. **Define 2-4 scan tasks** — Each must be self-contained (one source, one keyword batch, etc.)
3. **Launch N background agents** using the Task tool with `subagent_type: "general-purpose"` and `run_in_background: true`
4. Each agent receives a self-contained prompt (see template below)
5. **Collect results** from each agent when done
6. **Run merge protocol** — consolidate into queue.json, session file, source-registry updates
7. **Post-merge cleanup** — SESSION-LOG.md, field-signals.json, validate-workflow.js

### Background Agent Prompt Template

Use the Task tool with `subagent_type: "general-purpose"` and `run_in_background: true`:

```
You are executing a research scan task for the Ambidexterity Field Guide project.

TASK: {task-description}

## Core Research Question

Every observation must speak to: "How do organizations structurally enable both exploration and execution in the AI era?"

## CRITICAL: Web Search Is Your Primary Job

Your main activity is WEB RESEARCH. You MUST use the WebSearch tool to run every search query listed below. Do not skip queries. Do not fall back to only analyzing existing data.

**Mandatory workflow:**
1. Run ALL search queries below using WebSearch
2. From search results, identify the 5-8 most promising URLs (articles with structural detail, earnings transcripts, interview transcripts)
3. Use WebFetch on each promising URL to extract the full text
4. Read the fetched content carefully for structural findings that pass the Relevance Test
5. Write all qualifying findings to the output file

**If WebSearch fails on a query:** Retry once. If it fails again, note the failure and move to the next query.
**If WebFetch fails on a URL:** Try an alternative URL. Note any URLs you could not access.

## Relevance Test (apply to every finding)

A finding must pass at least ONE of these:
1. **Structural**: Tells us about org STRUCTURES — labs, teams, reporting lines, units, governance, resource allocation
2. **Tension**: Reveals how the org handles the TENSION between exploring AI and executing operations
3. **Specificity**: Has concrete detail — names, numbers, headcount, budgets, timelines, direct quotes

If it fails all three, don't record it.

{task-type-specific-context}

## Search Queries — Run ALL of These

{search-queries}

## Output

IMPORTANT: Write your results to a task-specific file. Do NOT write to queue.json, source-registry.json, or SESSION-LOG.md.

Write a JSON file to: research/pending/{task-id}.json

The file should contain:
{
  "taskId": "{task-id}",
  "taskType": "earnings | podcast-deep-scan | press-keyword | transcript-scan | specimen-targeted",
  "scannedDate": "YYYY-MM-DD",
  "sourceScanned": {
    "sourceId": "source-registry ID if applicable, or null",
    "name": "Human-readable source name",
    "type": "Earnings Call | Podcast | Press | Substack | etc.",
    "scannedThrough": "Description of what was scanned (e.g., 'Q4 2025 call')",
    "scannedThroughDate": "YYYY-MM-DD of latest content scanned"
  },
  "searchesCompleted": N,
  "urlsFetched": N,
  "searchFailures": ["list any queries that failed"],
  "fetchFailures": ["list any URLs that could not be accessed"],
  "organizations": [
    {
      "id": "org-slug (lowercase, hyphenated)",
      "name": "Organization Name",
      "status": "new | existing | evolution",
      "observations": [
        "Factual observation with specific detail"
      ],
      "sources": [
        {
          "fact": "The specific fact being sourced",
          "sourceType": "Earnings Call | Podcast | Press | etc.",
          "source": "Source name",
          "url": "URL",
          "timestamp": "HH:MM for audio/video, '—' for text",
          "sourceDate": "YYYY-MM-DD",
          "collectedDate": "YYYY-MM-DD"
        }
      ],
      "quotes": [
        {
          "text": "EXACT VERBATIM QUOTE",
          "speaker": "Full Name",
          "speakerTitle": "Title, Organization",
          "source": "Source name",
          "url": "URL",
          "timestamp": "HH:MM or '—'",
          "date": "YYYY-MM-DD"
        }
      ],
      "evolutionFlags": [
        "EVOLUTION: [old state] → [new state] as of [date]"
      ],
      "openQuestions": [
        "What's unclear or needs more research"
      ]
    }
  ],
  "broaderTrends": [
    "One-line macro observation from this scan"
  ],
  "newSourcesDiscovered": [
    {
      "name": "Source name",
      "type": "Podcast | Substack | etc.",
      "url": "URL",
      "notes": "Why this source is relevant"
    }
  ],
  "purposeClaimsDiscovered": [
    {
      "specimenId": "org-slug matching specimens/*.json",
      "specimenName": "Organization Name",
      "text": "EXACT VERBATIM QUOTE — the leader's actual words",
      "speaker": "Full Name",
      "speakerTitle": "Title, Organization",
      "claimType": "utopian | identity | teleological | transformation-framing | employee-deal | sacrifice-justification | direction-under-uncertainty",
      "context": "1-2 sentence description of the AI-adaptation context in which this claim was made",
      "sourceUrl": "URL where the quote was found",
      "sourceType": "Earnings Call | Podcast | Press | etc.",
      "sourceName": "Human-readable source name",
      "sourceDate": "YYYY-MM-DD",
      "confidence": "high | medium — how confident you are this is verbatim"
    }
  ]
}

## Cross-Pollination: Purpose Claims Discovery

While scanning for structural findings, watch for **purpose claims** — verbatim statements by leaders that invoke mission, identity, values, or vision to justify AI-driven structural changes. These are valuable for a parallel research track.

**What counts as a purpose claim:**
- A CEO/leader's EXACT WORDS (not paraphrased) invoking purpose to authorize AI transformation
- Must be in the context of explaining AI adaptation — not generic mission statements
- Examples: "We exist to cure diseases, and AI accelerates that" or "Our people need to prove AI can't do their job"

**What does NOT count:**
- Paraphrased descriptions of what a leader said
- Generic corporate mission statements not tied to AI transformation
- Technical descriptions of AI capabilities

If you encounter purpose claims during your scan, add them to the `purposeClaimsDiscovered` array in your output. This is **opportunistic** — don't go hunting for purpose claims, but capture them when they naturally surface during structural research. Set `confidence: "high"` only if you're certain the quote is verbatim; use `"medium"` if the source may have lightly edited the wording.

If no qualifying findings found, write the file with organizations: [] and a note explaining what was searched.
```

### Task-Type-Specific Prompt Additions

**For earnings tasks**, add to the prompt:
```
## Earnings Scan Context

Company: {company-name}
Quarter: Q{N} {FY year}
CEO: {ceo-name}
Known AI leaders: {CAIO, Head of AI, etc.}
Existing specimen: {yes/no, model if yes}

Keyword scan categories:
- structural: reorganize, restructure, reporting line, Chief AI, CoE, new unit/division
- workforce: headcount, delayer, flatten, fewer managers, reskill, redeploy, attrition
- investment: CapEx, AI infrastructure, AI investment, data center, GPU, compute
- deployment: agent, agentic, copilot, resolution rate, automation rate, AI product, deploy
- governance: responsible AI, AI safety, AI governance, AI board/committee

Search queries:
1. "{company-name}" Q{N} {FY year} earnings call transcript
2. "{company-name}" Q{N} {FY year} earnings AI restructuring OR reorganization
3. "{ceo-name}" Q{N} {FY year} AI CapEx OR investment
4. "{company-name}" Q{N} {FY year} AI headcount OR workforce
```

**For podcast deep-scan tasks**, add to the prompt:
```
## Podcast Deep-Scan Context

Podcast: {podcast-name}
Episode: {episode-number} — "{episode-title}"
Guest: {guest-name} ({guest-title})
Transcript available: {yes/no}
Transcript URL: {url if known}

If transcript available, fetch and keyword scan for: "lab", "team", "structure", "report to",
"Chief AI", "CoE", "incubator", "spin-off", "venture", "explore", "execute", "pilot",
"deploy", "headcount", "budget"

Deep-read sections around keyword hits. Apply Relevance Test to each finding.
```

**For press keyword tasks**, add to the prompt:
```
## Press Keyword Search Context

Run these keyword searches and scan all results for structural findings:

{list of keyword searches}

For each relevant result: read the article, apply Relevance Test, record findings with full URL and date.
Also note any NEW companies discovered that aren't in our specimen collection.
```

### Merge Protocol (run by orchestrator after all agents finish)

**Only the orchestrator writes to shared files.** This prevents race conditions.

1. `ls research/pending/` — list all completed agent outputs
2. Read each `pending/{task-id}.json` file
3. **Aggregate organizations** — Deduplicate across agents (same org may appear in multiple tasks)
4. **Write session file** to `research/sessions/YYYY-MM-DD-NNN-{type}-{descriptor}.md` in standard format
5. **Update `research/queue.json`** — Add entries for new/updated organizations
6. **Update `source-registry.json`** — Set `scannedThrough` and `lastScanned` from each agent's `sourceScanned`
7. **Update `field-signals.json`** — Process broader trends from all agents
8. **Update `SESSION-LOG.md`** — Add summary entry
9. **If new sources discovered** — Add to `sources.md` and `source-registry.json`
10. **Route purpose claims** — If any agents captured `purposeClaimsDiscovered`, write them to `research/purpose-claims/pending/research-cross-pollination-{date}.json` in the purpose claims pending format. These become leads for the next `/purpose-claims` run — not final claims (the purpose claims skill will verify verbatim accuracy and apply its own quality filters). Include `"source": "research-cross-pollination"` so the purpose claims merge can track provenance.
11. Delete processed `pending/*.json` files (or move to `pending/processed/`)
12. Run `node scripts/validate-workflow.js` to confirm consistency

### Recommended Batch Sizes

- **Max 4 agents per batch** (prevents context overflow crashes)
- **Parallel background agents work.** Launch up to 4 agents simultaneously with `run_in_background: true`.
- **Pre-flight check:** Verify `WebFetch` and `WebSearch` are in `~/.claude/settings.json` global permissions before starting a batch. If missing, agents will silently fail on web operations.
- Earnings sessions work best with 1-2 companies per agent (transcripts are dense)
- Podcast deep-scans should be 1 episode per agent
- Press keyword searches can batch 2-3 related queries per agent

### When to Use Parallel vs. Sequential

| Scenario | Approach |
|----------|----------|
| Earnings season: scanning 4+ companies | **Parallel** — 1-2 companies per agent |
| Deep-scanning a single rich transcript | **Sequential** — one agent, full depth |
| Press keyword discovery session | **Parallel** — different keyword batches per agent |
| Low-confidence targeted research | **Parallel** — 1 specimen per agent |
| Quick follow-up on 1-2 sources | **Sequential** — not worth the overhead |
