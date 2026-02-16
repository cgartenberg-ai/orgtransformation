# scripts/

Active scripts for the Ambidexterity Field Guide project. One-off historical scripts are in `archive/`.

## Active Scripts

### Nightly Pipeline (Python)

The nightly pipeline chains research → curate → purpose claims → synthesis → validation → morning briefing. It runs on a 7-day themed rotation configured in `pipeline-schedule.json`.

| Script | Purpose | Runtime | Key I/O |
|--------|---------|---------|---------|
| `overnight-pipeline.py` | **Orchestrator** — chains all phases | ~7 hrs | Reads: schedule → Writes: `pipeline-reports/` |
| `overnight-research.py` | Research agents (14 theme modes) | ~1-5 hrs | Writes: `research/pending/`, `research/queue.json` |
| `overnight-curate.py` | Creates/updates specimen cards | ~2-4 hrs | Reads: `research/queue.json` → Writes: `specimens/*.json` |
| `overnight-purpose-claims.py` | Collects purpose claims | ~3-6 hrs | Writes: `purpose-claims/registry.json` |
| `overnight-synthesis.py` | **Autonomous synthesis** — scores specimens | ~1 hr | Writes: `synthesis/*.json`, field journal |
| `pipeline-schedule.json` | 7-day themed rotation config | — | Read by orchestrator |

**Running the pipeline:**
```bash
# Full nightly pipeline (runs tonight's schedule)
python3 scripts/overnight-pipeline.py --skip-permissions

# Preview what would run
python3 scripts/overnight-pipeline.py --dry-run --day monday

# Run a specific phase only
python3 scripts/overnight-pipeline.py --phase 1 --skip-permissions

# Run a themed research batch directly
python3 scripts/overnight-research.py --schedule-theme press-keyword --limit 4 --dry-run
```

**Schedule themes (14 modes):**
`earnings`, `press-keyword`, `podcast-feed-check`, `substacks`, `enterprise-reports`, `target-specimens`, `target-specimens-enrich`, `stale-refresh`, `low-confidence`, `taxonomy-gap-coverage`, `daily-news-headlines`, `industry-vertical-searches`, `source-staleness-audit`, `catch-up`

**Scheduling:** launchd plist at `scripts/com.fieldguide.overnight-pipeline.plist` triggers daily at 7 PM. Install:
```bash
cp scripts/com.fieldguide.overnight-pipeline.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.fieldguide.overnight-pipeline.plist
```

**Morning review:** Check `pipeline-reports/YYYY-MM-DD-morning-briefing.md` and `pipeline-reports/YYYY-MM-DD-field-journal.md`.

**Framework-aware pipeline (Session 36+):** All overnight scripts inject the analytical framework into agent prompts:
- `overnight-research.py` — P1-P5 primitive antenna + T1-T5 tension names in relevance test
- `overnight-curate.py` — Tags `primitiveIndicators` (P1-P5) and `findingRelevance` (supports/challenges F1-F10) with anti-bias guardrail
- `overnight-purpose-claims.py` — P3/P4 analytical context + `primitiveRelevance` in enrichment
- `SYNTHESIS-PROTOCOL.md` — Step 5d Findings Review + primitive lens in field notes

**Important:**
- `--dry-run` — Preview without modifying files
- `--skip-permissions` — Required for unattended runs
- PID-based lock files (`scripts/.locks/`) prevent concurrent runs
- All writes use atomic `save_json()` — tmp → validate → backup → rename
- All changes logged to `data/CHANGELOG.md`
- Time-budget-aware: skips optional batches if running long (12-hour window)

### Validation & Status (Node.js)

| Script | Purpose | Key Checks |
|--------|---------|------------|
| `validate-workflow.js` | Consistency checker | Registry vs files, source provenance, aggregates, queue staleness, purpose claims, tension/contingency coverage, insight evidence, enrichment, registry freshness |
| `rebuild-registry.js` | Rebuild registry.json from specimen files | Respects Inactive status, compares to previous, supports `--dry-run` |
| `specimen-lifecycle-status.js` | Pipeline dashboard | Cross-references 7 data sources per specimen → `data/specimen-lifecycle-status.{md,json}` |
| `check-source-freshness.js` | Source staleness alerter | Tier 1: 14-day threshold, Tier 2: 30-day threshold |
| `compute-mechanism-affinity.js` | Analysis utility | Computes mechanism-taxonomy affinity profiles |

**Running validation:**
```bash
# From project root — run after any data changes
node scripts/validate-workflow.js

# Rebuild registry from actual specimen files
node scripts/rebuild-registry.js [--dry-run]

# Generate lifecycle dashboard
node scripts/specimen-lifecycle-status.js

# Check source freshness
node scripts/check-source-freshness.js
```

### Post-Run Verification Checklist

After any overnight run or data modification:
1. `node scripts/validate-workflow.js` — 0 errors required
2. `cd site && npm run build` — must succeed
3. Review `data/CHANGELOG.md` for what changed
4. Optionally: `node scripts/specimen-lifecycle-status.js` for updated dashboard

## Shared Library (`lib/`)

Python utilities used by all overnight scripts:

| Module | Key Functions |
|--------|--------------|
| `lib/utils.py` | `save_json()`, `load_json()`, `acquire_lock()`, `release_lock()`, `preflight_check()`, `setup_logging()`, `write_changelog()` |

**Constants:** `PROJECT_ROOT`, `BLOCKED_DOMAINS`, `CLAIM_TYPES`, `LOCKS_DIR`, `CHANGELOG_PATH`

## Lock Files

- Stored in `scripts/.locks/` (git-ignored)
- PID-based: each lock file contains the process ID
- Stale locks (dead PID) are detected and reported
- One lock per overnight script prevents concurrent runs

## Backup Files

- `*.bak` files created by `save_json()` before overwriting
- Git-ignored (`.gitignore` has `*.bak`)
- Kept as local safety net — can restore if needed

## Archive (`archive/`)

43 historical one-off scripts. See `archive/README.md` for categories.
