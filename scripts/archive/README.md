# scripts/archive/

Historical one-off scripts moved here during the Phase 5 cleanup (Feb 2026).

These scripts were used for specific batch operations during the project's research sessions and are preserved for reference. They are **not intended to be run again** — the data they modified has already been updated.

## Categories

### Batch merge scripts
`merge-batch*.py`, `merge-session*.py`, `merge-purpose-claims-batch.py`
— Merged purpose claims from pending files into `registry.json`.

### Patch scripts
`patch-batch*.py`, `patch-jpmorgan.py`
— Applied one-time fixes to specimen or synthesis data after batch processing.

### Enrichment scripts
`enrich-*.py`, `backfill-enrichment.py`
— One-time enrichment of specific specimens with deeper data.

### Insight update scripts
`update-insights-*.py`, `batch*-insights-patch.py`, `purpose-insights-reframe.py`
— Updated `synthesis/insights.json` after specific analysis sessions.

### Taxonomy and audit scripts
`apply-taxonomy-v2.py`, `m4-audit-reclassify.py`, `m4-audit-update-registry.py`
— Applied taxonomy changes and M4 audit reclassifications.

### Other one-off utilities
`add-field-signals.py`, `add-podcast-sweep-signals.py`, `add-queue-entries.py`,
`backfill-botanist-notes.py`, `citation-backfill-*.py`, `convert-cases.js`,
`identify-pending-cleanup.py`, `split-multi-company.py`
— Various one-time data operations.

### Deprecated
`overnight-synthesis.py` — Replaced by the interactive `/synthesize` skill.
