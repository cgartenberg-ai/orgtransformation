# scripts/

Active scripts for the Ambidexterity Field Guide project. One-off historical scripts are in `archive/`.

## Active Scripts

### Overnight Automation (Python)

These scripts run Claude Code agents for batch data collection. They use the shared library in `lib/` for atomic writes, locking, and logging.

| Script | Purpose | Runtime | Key I/O |
|--------|---------|---------|---------|
| `overnight-research.py` | Runs research agents to scan sources | ~2-4 hrs | Writes: `research/queue.json`, session files |
| `overnight-purpose-claims.py` | Collects purpose claims via agents | ~3-6 hrs | Reads: `pending/*.json` → Writes: `registry.json`, `scan-tracker.json` |
| `overnight-curate.py` | Creates/updates specimen cards | ~2-4 hrs | Reads: `research/queue.json` → Writes: `specimens/*.json`, `registry.json` |

**Running overnight scripts:**
```bash
# From project root
python3 scripts/overnight-research.py [--dry-run]
python3 scripts/overnight-purpose-claims.py [--dry-run]
python3 scripts/overnight-curate.py [--dry-run]
```

**Important flags:**
- `--dry-run` — Preview what would happen without modifying any files
- All scripts acquire a PID-based lock file (`scripts/.locks/`) to prevent concurrent runs
- All data writes use atomic `save_json()` — write to `.tmp`, validate, backup original, then rename
- All modifications logged to `data/CHANGELOG.md`

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
