# Nightly Pipeline Implementation Plan (v2)

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Build a fully autonomous nightly pipeline that runs research → curate → purpose-claims → synthesis every night on a themed rotation, committing changes with field journal audit trail, so the morning session is focused on reviewing insights rather than executing mechanics.

**Architecture:** A new `scripts/overnight-pipeline.py` orchestrator chains the existing three scripts sequentially, then runs a new autonomous synthesis step that actually commits to the database with field journal notes. A `scripts/pipeline-schedule.json` config defines a 7-day themed rotation. Each run produces a `pipeline-reports/YYYY-MM-DD-morning-briefing.md` summarizing everything that changed overnight.

**Tech Stack:** Python 3.11+, existing `scripts/lib/utils.py` primitives, `claude` CLI for agents, `subprocess.run` for chaining scripts.

---

## Design Decisions

### Critique 1: Synthesis is autonomous, not draft-only

Previous plan had synthesis producing a draft for human review. Revised:

- **If we don't manually synthesize in the morning, the pipeline DOES the synthesis autonomously.**
- It reads each newly curated specimen, scores it against tensions and contingencies, places it, updates `synthesis/insights.json` with any new cross-cutting observations, and writes a field journal entry in the morning briefing explaining exactly what it did and why.
- The field journal note is the audit trail: `"2026-02-16 overnight-pipeline (autonomous): Placed shopify specimen against tensions T2 (Speed-Safety) and T4 (Centralize-Distribute). Rationale: Shopify's unlimited AI spending + leaderboard suggests tolerance for exploration risk (T2), while MCP-everything initiative is decentralized infrastructure (T4). Confidence: HIGH."`
- Insights guardrail still honored: existing insights are never deleted, only new ones added.
- **Morning workflow changes to: review what was committed, adjust if needed, rather than approve-then-commit.**

### Critique 2: Throughput math — what can we do in 12 hours?

**Empirical timing (from MEMORY.md and today's agents):**
| Phase | Per-specimen time | Serialized | 2-parallel | 4-parallel |
|-------|-------------------|-----------|-----------|-----------|
| Research agent | 15-25 min | 25 min | 13 min | 7 min |
| Curate agent | 10-15 min | 15 min | 8 min | 4 min |
| Purpose claims agent | 15-25 min | 25 min | 13 min | 7 min |
| Synthesis agent | 5-10 min/specimen | 10 min | 5 min | — |

**12-hour window budget (7:00 PM → 7:00 AM = 720 minutes):**

| Phase | Agents | Parallelism | Specimens/companies | Est. time |
|-------|--------|-------------|---------------------|-----------|
| Research | 6 agents | 2 parallel | 18-24 companies | ~90 min |
| Curate | 16 agents | 4 parallel | 16 specimens | ~60 min |
| Purpose claims | 8 agents | 2 parallel | 8 specimens | ~100 min |
| Synthesis | 1 agent | serial | batch of 16 | ~45 min |
| Briefing gen | script | — | — | ~2 min |
| **Buffer (retries, hangs)** | — | — | — | ~120 min |
| **Total** | | | | **~417 min ≈ 7 hours** |

**That leaves ~5 hours of slack** in a 12-hour window. So we can safely do:
- **18-24 companies researched per night** (6 research agents, 3-4 companies each, 2 at a time)
- **16 specimens curated per night** (handles research output + backlog)
- **8 specimens enriched with purpose claims per night**
- **16 specimens synthesized per night**
- **Full pipeline in ~7 hours with generous buffer**

Compare to the original plan: 8 companies, 8 curations, 4 purpose claims. **The revised plan is 3x throughput.**

### Critique 3: Source coverage — use sources.md as the master checklist

The `research/sources.md` file documents ~100+ sources across 9 categories. The 7-day rotation must systematically cover ALL of them over time, not just the subset we remember.

**Source universe (from sources.md):**

| Category | Count | Scan frequency needed |
|----------|-------|----------------------|
| Tier 1 podcasts | 6 shows | Every episode (weekly) |
| Tier 2 podcasts | 8 shows | Weekly check |
| Tier 2.5 podcasts | 8 shows | Weekly check |
| Tier 2.6 enterprise reports | 9 sources | Monthly |
| Tier 3 podcasts | 8+ shows | Monthly |
| Daily AI news shows | 5+ shows | Weekly headline scan |
| Tier 1 substacks | 6 pubs | Every issue (2-3x/week) |
| Tier 2 substacks | 7 pubs | Weekly |
| Tier 2.5 substacks | 3 pubs | Weekly |
| Earnings calendar companies | 40 companies | Quarterly earnings |
| Press keyword searches | 8+ query templates | Weekly |
| Target specimens (Phase A+B) | 55 targets | Rolling |
| Active specimens (stale refresh) | 146 specimens | Monthly refresh cycle |

**Key insight: a single "press-sweep" or "podcast" night is not enough.** We need MULTIPLE research runs per night, serialized. The 12-hour window supports this.

**Revised 7-day rotation — each night runs 2-3 themed research batches:**

| Day | Theme 1 (primary) | Theme 2 (secondary) | Theme 3 (tertiary) |
|-----|-------------------|---------------------|-------------------|
| **Monday** | Earnings sweep (6-8 companies) | Press keyword sweep | — |
| **Tuesday** | Tier 1+2 podcast feed check + deep-scan | Tier 2.5 podcast check | Daily news headline scan |
| **Wednesday** | Substacks (all tiers) | Enterprise reports scan | Target specimens (Phase A) |
| **Thursday** | Stale refresh (oldest 8 specimens) | Target specimens (Phase B enrich) | Press keyword sweep |
| **Friday** | Earnings follow-up (newly reported) | Low-confidence specimens | Taxonomy gap coverage |
| **Saturday** | Tier 3 + extended podcasts | Industry-specific discovery searches | — |
| **Sunday** | Full source-registry staleness audit | Catch-up on anything behind schedule | — |

This gives us **~15-20 themed research runs per week** instead of 7. Each run is 2-4 research agents.

### Why chain existing scripts (not rewrite)?
- Three scripts already work and are battle-tested
- Each has its own lock, logging, error handling, retry logic
- The orchestrator sequences them with the right flags and collects results
- Avoids introducing new bugs in critical data paths

---

## Pipeline Flow (Revised)

```
overnight-pipeline.py
│
├── Phase 1: Research (themed — runs 2-3 batches serially)
│   ├── Batch 1: overnight-research.py --schedule-theme {primary} --limit 8
│   ├── Batch 2: overnight-research.py --schedule-theme {secondary} --limit 6
│   └── Batch 3: overnight-research.py --schedule-theme {tertiary} --limit 4 (if time)
│
├── Phase 2: Curate (processes ALL pending)
│   └── overnight-curate.py --skip-permissions --limit 16
│
├── Phase 3: Purpose Claims
│   └── overnight-purpose-claims.py --skip-permissions --limit 8
│
├── Phase 4: Autonomous Synthesis (NEW — commits to database)
│   └── claude -p "Full synthesis..." → updates synthesis/*.json, writes field journal
│
├── Phase 5: Post-run validation
│   └── node scripts/validate-workflow.js
│
└── Phase 6: Morning Briefing
    └── Compile all results → pipeline-reports/YYYY-MM-DD-morning-briefing.md
```

---

## Schedule Configuration

```json
// scripts/pipeline-schedule.json
{
  "description": "7-day themed rotation with multiple research batches per night. 12-hour window (7PM-7AM). Source coverage designed from sources.md master list.",
  "schedule": {
    "monday": {
      "themes": [
        {
          "name": "earnings",
          "mode": "earnings",
          "limit": 8,
          "agentsParallel": 2,
          "notes": "Scan earnings calendar for unscanned Q results. Priority: critical > high > monitor."
        },
        {
          "name": "press-keyword",
          "mode": "press-keyword",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Structural keyword searches: CAIO, AI lab, restructuring, center of excellence."
        }
      ],
      "curate": { "limit": 16, "agentsParallel": 4 },
      "purposeClaims": { "limit": 8, "agentsParallel": 2 },
      "synthesis": { "limit": 16, "autonomous": true }
    },
    "tuesday": {
      "themes": [
        {
          "name": "tier1-tier2-podcasts",
          "mode": "podcast-feed-check",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Check all Tier 1 (6) + Tier 2 (8) podcast feeds. Deep-scan new high-priority episodes.",
          "sources": ["cheeky-pint", "no-priors", "bg2-pod", "dwarkesh-podcast", "latent-space", "acquired", "conversations-with-tyler", "invest-like-the-best", "cognitive-revolution", "all-in-podcast", "lex-fridman"]
        },
        {
          "name": "tier25-podcasts",
          "mode": "podcast-feed-check",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Check Tier 2.5 AI Leadership podcasts (8 shows).",
          "sources": ["agents-of-scale", "the-ai-ceo", "leadership-next", "the-data-chief", "training-data", "morgan-stanley-insights", "pigment-perspectives", "hg-orbit"]
        },
        {
          "name": "daily-news-scan",
          "mode": "daily-news-headlines",
          "limit": 2,
          "agentsParallel": 1,
          "notes": "Headline scan of AI Daily Brief, The AI Breakdown, Last Week in AI for structural signals."
        }
      ],
      "curate": { "limit": 16, "agentsParallel": 4 },
      "purposeClaims": { "limit": 8, "agentsParallel": 2 },
      "synthesis": { "limit": 16, "autonomous": true }
    },
    "wednesday": {
      "themes": [
        {
          "name": "substacks-all-tiers",
          "mode": "substacks",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Scan all Tier 1 (6), Tier 2 (7), Tier 2.5 (3) substacks for new structural content.",
          "sources": ["stratechery", "one-useful-thing", "not-boring", "the-generalist", "import-ai", "pragmatic-engineer", "thesequence", "construction-physics", "semianalysis", "ai-snake-oil", "interconnects", "the-batch", "last-week-in-ai", "lennys-newsletter", "elad-gils-blog", "platformer"]
        },
        {
          "name": "enterprise-reports",
          "mode": "enterprise-reports",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Check BCG AI Radar, OpenAI State of Enterprise AI, Deloitte Tech Trends, PwC AI Predictions, HBR AI Strategy, Mercer, Oxford Economics, i4cp, State of AI Report.",
          "sources": ["bcg-ai-radar", "openai-enterprise", "deloitte-tech-trends", "pwc-ai-predictions", "hbr-ai-strategy", "mercer-global-talent", "oxford-economics", "i4cp", "state-of-ai-report"]
        },
        {
          "name": "target-specimens-phase-a",
          "mode": "target-specimens",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Work through target-specimens.json Phase A (new specimens). Priority by quadrant coverage gaps."
        }
      ],
      "curate": { "limit": 16, "agentsParallel": 4 },
      "purposeClaims": { "limit": 8, "agentsParallel": 2 },
      "synthesis": { "limit": 16, "autonomous": true }
    },
    "thursday": {
      "themes": [
        {
          "name": "stale-refresh",
          "mode": "stale-refresh",
          "limit": 8,
          "agentsParallel": 2,
          "notes": "Find specimens with oldest lastUpdated dates. Enrich with fresh data. Target: cycle through all 146 active specimens over ~18 Thursdays (2 months)."
        },
        {
          "name": "target-specimens-phase-b",
          "mode": "target-specimens-enrich",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Enrich existing specimens from target-specimens.json Phase B."
        },
        {
          "name": "press-keyword",
          "mode": "press-keyword",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Second weekly press sweep — different keyword set from Monday."
        }
      ],
      "curate": { "limit": 16, "agentsParallel": 4 },
      "purposeClaims": { "limit": 8, "agentsParallel": 2 },
      "synthesis": { "limit": 16, "autonomous": true }
    },
    "friday": {
      "themes": [
        {
          "name": "earnings-followup",
          "mode": "earnings",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Follow up on any earnings reported this week that weren't caught Monday."
        },
        {
          "name": "low-confidence",
          "mode": "low-confidence",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Targeted research for specimens with low-confidence classifications."
        },
        {
          "name": "taxonomy-gaps",
          "mode": "taxonomy-gap-coverage",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Discovery searches for underrepresented structural models in the taxonomy grid."
        }
      ],
      "curate": { "limit": 16, "agentsParallel": 4 },
      "purposeClaims": { "limit": 8, "agentsParallel": 2 },
      "synthesis": { "limit": 16, "autonomous": true }
    },
    "saturday": {
      "themes": [
        {
          "name": "tier3-extended-podcasts",
          "mode": "podcast-feed-check",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Monthly cycle through Tier 3 (8+ shows) and extended network podcasts.",
          "sources": ["acq2", "flux", "asianometry", "a16z-podcast", "gradient-dissent", "twiml-ai", "practical-ai", "eye-on-ai"]
        },
        {
          "name": "industry-discovery",
          "mode": "industry-vertical-searches",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Run industry-specific discovery searches from earnings-calendar.json discoveryProtocol. Rotate: healthcare, insurance, manufacturing, automotive weekly."
        }
      ],
      "curate": { "limit": 12, "agentsParallel": 4 },
      "purposeClaims": { "limit": 6, "agentsParallel": 2 },
      "synthesis": { "limit": 12, "autonomous": true }
    },
    "sunday": {
      "themes": [
        {
          "name": "source-staleness-audit",
          "mode": "source-staleness-audit",
          "limit": 4,
          "agentsParallel": 2,
          "notes": "Read source-registry.json. Find all sources where scannedThroughDate is > 14 days old. Generate priority list for the week ahead. Run targeted research on the most stale sources."
        },
        {
          "name": "catch-up",
          "mode": "catch-up",
          "limit": 6,
          "agentsParallel": 2,
          "notes": "Process any research backlog: pending files not yet curated, specimens in synthesis queue, stale source-registry entries. Adaptive — picks the most behind phase."
        }
      ],
      "curate": { "limit": 12, "agentsParallel": 4 },
      "purposeClaims": { "limit": 6, "agentsParallel": 2 },
      "synthesis": { "limit": 12, "autonomous": true }
    }
  },
  "defaults": {
    "maxAgentsConcurrent": 4,
    "agentTimeoutMinutes": 25,
    "skipOnFailure": true,
    "retryOnCrash": true,
    "maxRetries": 1,
    "startTimeLocal": "19:00",
    "endTimeLocal": "07:00",
    "windowMinutes": 720,
    "phaseBudgetMinutes": {
      "research": 300,
      "curate": 120,
      "purposeClaims": 150,
      "synthesis": 60,
      "validation": 5,
      "briefing": 5,
      "buffer": 80
    }
  },
  "weeklyThroughputTargets": {
    "companiesResearched": 120,
    "specimensCurated": 100,
    "purposeClaimsCollected": 50,
    "specimensSynthesized": 100,
    "notes": "At 18-24 companies/night × 7 nights = 126-168/week. This covers the full earnings calendar (40 companies/quarter = ~3.5/week) with substantial room for podcasts, substacks, press, and discovery. Stale refresh cycles through all 146 specimens in ~18 days."
  }
}
```

---

## Source Coverage Verification

**Will the 7-day rotation cover the full sources.md universe?**

| Source category | How covered | Cycle time |
|----------------|------------|-----------|
| Tier 1 podcasts (6) | Tuesday primary batch | Weekly ✓ |
| Tier 2 podcasts (8) | Tuesday primary batch | Weekly ✓ |
| Tier 2.5 podcasts (8) | Tuesday secondary batch | Weekly ✓ |
| Tier 2.6 enterprise reports (9) | Wednesday secondary batch | Weekly (rotate subset) |
| Tier 3 podcasts (8+) | Saturday primary batch | Monthly (rotate 2/week) ✓ |
| Daily news shows (5+) | Tuesday tertiary batch | Weekly headline scan ✓ |
| Tier 1 substacks (6) | Wednesday primary batch | Weekly ✓ |
| Tier 2+2.5 substacks (10) | Wednesday primary batch | Weekly ✓ |
| Press keywords | Monday secondary + Thursday tertiary | 2x/week ✓ |
| Earnings (40 companies) | Monday primary + Friday primary | 2x/week during season ✓ |
| Target specimens Phase A (new) | Wednesday tertiary | Weekly ✓ |
| Target specimens Phase B (enrich) | Thursday secondary | Weekly ✓ |
| Stale refresh (146 specimens) | Thursday primary (8/week) | Full cycle in 18 weeks |
| Low-confidence specimens | Friday secondary | Weekly ✓ |
| Taxonomy gap searches | Friday tertiary | Weekly ✓ |
| Industry discovery | Saturday secondary | Weekly (rotate industry) ✓ |
| Source staleness audit | Sunday primary | Weekly ✓ |

**Gaps identified: NONE.** Every category in sources.md is covered by the rotation.

**Stale refresh math:** 146 active specimens ÷ 8 per Thursday = 18.25 Thursdays = ~4.5 months for full cycle. If we also use Sunday catch-up for stale specimens, we can cut this to ~3 months.

---

## Autonomous Synthesis Design

### What it does (Phase 4)

For each newly curated specimen in the synthesis queue:

1. **Read the specimen** — full JSON with all layers
2. **Score against 5 tensions** — rate involvement (high/medium/low/none) with rationale
3. **Score against 6 contingencies** — rate relevance with rationale
4. **Check for cross-cutting patterns** — does this specimen illuminate an existing insight or suggest a new one?
5. **Write updates** — update `synthesis/tensions.json`, `synthesis/contingencies.json`, and possibly add to `synthesis/insights.json`
6. **Write field journal entry** — structured note in `pipeline-reports/YYYY-MM-DD-field-journal.md` documenting every change and why

### Field journal format

```markdown
## Field Journal — 2026-02-16 (Autonomous Synthesis)

### Specimen: shopify (Shopify)
**Model:** M6 (Informal) | **Orientation:** Contextual

**Tension placements:**
- T2 Speed-Safety: HIGH — unlimited AI spending + no budget caps = extreme speed tolerance. Leaderboard for token spending = gamification of exploration risk.
- T4 Centralize-Distribute: HIGH — MCP-everything initiative is decentralized infrastructure. Any employee builds workflows. Contrast with T4-centralize specimens like Sanofi.

**Contingency placements:**
- C1 Industry: RELEVANT — Shopify's e-commerce context enables universal AI access (low-stakes experimentation) vs. pharma where AI touches patient safety.
- C3 Leadership Tenure: RELEVANT — Lutke as founder-CEO enables radical policy (no hiring without proving AI can't do it) that a hired CEO couldn't.

**New insight candidate:**
> "Universal AI access with spending leaderboards represents a novel mechanism for distributed exploration — incentive design at the tool-access level, not the project level."
> **Evidence:** Shopify leaderboard, Moderna 4000+ GPTs, contrasted with centralized CAIO models.
> **Confidence:** MEDIUM — need more examples to confirm as general pattern.

### Specimen: intel (Intel)
[...]
```

### Guardrails

- **Never delete existing insights** — can add new ones, update evidence for existing ones
- **Confidence threshold** — only adds insights if confidence ≥ MEDIUM and backed by ≥2 specimens
- **Field journal is append-only** — complete audit trail
- **validate-workflow.js runs after** — catches any structural inconsistencies

---

## Task Breakdown

### Task 1: Create `scripts/pipeline-schedule.json`

Write the full schedule config above (v2 with multiple themes per night).

### Task 2: Add `--schedule-theme` flag and multi-theme support to `overnight-research.py`

- Add `--schedule-theme` flag with all theme choices
- Add target selection functions for each mode
- Support being called multiple times in sequence (the orchestrator calls it once per theme batch)

### Task 3: Create `scripts/overnight-pipeline.py` — the orchestrator (v2)

Major changes from v1:
- Runs **multiple research batches per night** (loops over `themes` array)
- Phase 4 is **autonomous synthesis** that commits to database
- Phase 5 runs **validate-workflow.js**
- Phase 6 generates morning briefing
- **Time-budget-aware**: tracks elapsed time, skips optional batches if running long
- Start time 19:00, end time 07:00

### Task 4: Create `scripts/overnight-synthesis.py` — the autonomous synthesis engine

New script, distinct from the deprecated `overnight-synthesis.py` (which was a thin wrapper). This one:
- Reads synthesis queue
- For each pending specimen: reads full JSON, scores tensions/contingencies
- Writes updates to `synthesis/*.json` using atomic writes
- Writes field journal entries
- Uses `claude -p` with a carefully designed prompt that includes full taxonomy, tension definitions, and contingency definitions
- Honors insights guardrail (append-only)

### Task 5: Add `pipeline-reports/` directory, field journal format, `.gitignore`

- `pipeline-reports/` for briefings and field journals
- Field journal files are version-controlled (they're the audit trail)
- Briefing files are not (ephemeral)

### Task 6: Add source-staleness-audit mode

New research mode that:
- Reads `source-registry.json`
- Computes days-since-last-scan for every source
- Generates a priority list (sorted by staleness × tier)
- Runs targeted research on the most stale sources
- Updates source-registry with new scan dates

### Task 7: Add catch-up mode (Sunday)

Adaptive mode that:
- Counts pending items across all phases (research/pending/, synthesis-queue, etc.)
- Picks the most behind phase and allocates research agents there
- Prevents any single bottleneck from accumulating

### Task 8: Add cron/launchd scheduling (start at 7PM)

Update the launchd plist to start at 19:00 instead of 01:00. Add time-budget logic so the pipeline knows it must finish by 07:00.

### Task 9: Integration tests

- `--dry-run` with every theme
- Schedule completeness (all 7 days covered)
- Source coverage verification (all sources.md categories mapped to at least one theme)
- Synthesis guardrails (insights never deleted)

### Task 10: Update WORKFLOW.md, scripts/README.md, APP_STATE.md

Document the full nightly pipeline, morning review workflow, and source coverage mapping.

---

## Implementation Order

1. **Task 1** — Schedule config (pure data)
2. **Task 5** — Reports directory + gitignore
3. **Task 2** — `--schedule-theme` and target selection functions
4. **Task 6** — Source-staleness-audit mode
5. **Task 7** — Catch-up mode
6. **Task 4** — Autonomous synthesis engine
7. **Task 3** — Orchestrator (depends on 2, 4, 6, 7)
8. **Task 8** — Launchd scheduling
9. **Task 9** — Integration tests
10. **Task 10** — Documentation

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Autonomous synthesis makes bad placements | Field journal provides full audit trail; validate-workflow.js catches structural errors; morning review catches judgment errors |
| Pipeline exceeds 12-hour window | Time-budget tracking; optional batches skipped if running long; morning briefing reports which batches were skipped |
| Too many concurrent agents crash | Max 4 concurrent (from MEMORY.md); orchestrator enforces this |
| Source-registry gets stale despite automation | Sunday staleness audit explicitly checks every source; weekly briefing flags lagging sources |
| Agent costs escalate | Phase budget limits prevent runaway; `--limit` flags on every phase |
| Pipeline corrupts data files | All writes use atomic save_json(); backups before every replace; validate-workflow.js runs post-pipeline |
| McKinsey.com or blocked domain hangs | BLOCKED_DOMAINS in lib/utils.py; agent timeout at 25 min |
