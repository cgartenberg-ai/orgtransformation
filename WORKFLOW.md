# Project Workflow: Complete Command Reference

## Last Updated: February 14, 2026

This document is the single source of truth for **all research workflows and commands** in the Ambidexterity Field Guide project.

---

## Overview: Two Parallel Research Tracks

The project has **two parallel research tracks**, each with its own pipeline:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TRACK 1: STRUCTURAL RESEARCH                            │
│              "How do organizations structure AI work?"                          │
│                                                                                 │
│   /research → /curate → interactive synthesis → [insights.json, etc.]          │
│                                                                                 │
│   Output: Specimen cards, mechanisms, field insights, tensions                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TRACK 2: PURPOSE CLAIMS                                 │
│              "How do leaders use purpose to authorize transformation?"          │
│                                                                                 │
│   /purpose-claims → [registry.json] → (future: synthesis)                       │
│                                                                                 │
│   Output: Verbatim claim registry for academic paper on purpose × AI            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

Both tracks share:
- The same specimen collection as subjects
- The Transcript Discovery Protocol for finding interview sources
- The source registry (`specimens/source-registry.json`)

---

## Track 1: Structural Research Pipeline

### Phase 1: `/research` — Field Work

**What it does:** Scans sources (podcasts, press, earnings calls, substacks) for organizational AI structure findings.

**When to use:**
- Weekly refresh of Tier 1 sources
- Quarterly earnings season scans
- Ad hoc deep-dives on specific topics

**Invocation:**
```
/research                    # General multi-source scan
/research general            # Same as above
/research low-confidence     # Targeted research for low-confidence specimens
```

**Inputs:**
- `specimens/source-registry.json` — what's been scanned
- `research/SESSION-PROTOCOL.md` — step-by-step instructions
- `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` — finding transcripts

**Outputs:**
- `research/sessions/YYYY-MM-DD-NNN-{type}-{descriptor}.md` — session file
- `research/queue.json` — orgs pending curation
- Updates to `source-registry.json`

**Key protocol steps:**
1. Check source registry for coverage gaps
2. Plan sources to scan (multiple types)
3. **Step 2b: Check transcript availability** (NEW)
4. Triage and deep-scan high-priority content
5. Record findings with full provenance
6. Update queue and registry

---

### Phase 2: `/curate` — Specimen Creation

**What it does:** Transforms raw research findings into structured specimen cards.

**When to use:** After `/research` sessions have added items to the queue.

**Invocation:**
```
/curate                      # Process pending items in research/queue.json
/curate [specimen-id]        # Create or update a specific specimen
```

**Inputs (two formats):**

| Format | Source | How it works |
|--------|--------|--------------|
| **Multi-company session** | Interactive `/research` | Session file in `research/sessions/*.md` referenced by `research/queue.json`. Contains multiple orgs. Process via queue entries. |
| **Single-company JSON** | `overnight-research.py` | Structured JSON in `research/pending/{slug}.json` with `"company"` field. `overnight-curate.py` consumes these directly — no queue.json entry needed. |

Both formats converge to the same output: specimen files + synthesis queue entries.

- `research/queue.json` — pending orgs from interactive research sessions
- `research/pending/*.json` — single-company files from overnight research
- `research/sessions/*.md` — session files with findings
- Existing `specimens/*.json` if updating

**Outputs:**
- `specimens/{id}.json` — new or updated specimen cards
- `curation/synthesis-queue.json` — specimens pending synthesis
- `curation/sessions/*.md` — curation session log

**Key protocol steps:**
1. Read research findings for each org (from session file or pending JSON)
2. Classify by model (M1-M9) and orientation
3. Create/update specimen with layers
4. Queue for synthesis

---

### Phase 3: Synthesis — Interactive Botanist Mode (REQUIRED)

> **DEPRECATED: Automated `/synthesize` and `overnight-synthesis.py`.**
> The overnight synthesis pipeline (Sessions 8-10) proved that synthesis CANNOT be reliably automated. Agents systematically dropped tension/contingency data, produced format divergence, and — most importantly — missed the analytical discoveries that make this work valuable. Synthesis requires the botanist's eye: reading each specimen, noticing what doesn't fit, spotting patterns across specimens, and pausing to develop theoretical connections. This is the intellectual core of the project, not a data migration task.

**What it does:** Interactive, collaborative analysis of specimens in batches — scoring tensions, placing contingencies, and watching for cross-cutting discoveries.

**When to use:** After `/curate` has processed specimens. This is always done interactively in conversation, never via background agents.

**How it works:**

1. **Read specimens in sector/theme batches** (8-15 at a time, grouped by industry or structural similarity)
2. **Score all 5 tensions** (T1-T5, positions from -1.0 to +1.0) with evidence strings
3. **Assign all 6 contingencies** (C1-C6, categorical levels)
4. **Watch for discoveries** — this is the critical step:
   - Patterns across 3+ specimens in the batch → potential new insight
   - Specimens that don't fit any tension pole → possible new tension or redefinition
   - Evidence that strengthens/weakens existing hypotheses → maturity promotion
   - Contingency levels that don't exist → possible new contingency
   - Model classifications that seem wrong → flag for taxonomy review
5. **PRESENT observations to collaborator and WAIT for discussion** — this is NON-NEGOTIABLE. Do NOT skip to the patch script. Present proposed tension/contingency scores, any patterns or discoveries, and any questions. Wait for the collaborator's response. The most valuable analytical insights emerge from back-and-forth discussion, not from unilateral analysis. If you find yourself writing the patch script without having presented observations and received feedback, you have broken the protocol.
6. **Write Python patch script** per batch (never edit JSON directly) — ONLY after discussion
7. **Validate** after each batch: `node scripts/validate-workflow.js`
8. **Update field journal with ALL substantive observations** — see Field Journal Protocol below. Include observations from BOTH collaborators and the discussion that shaped them.
9. **Update `synthesis/insights.json`** if the batch produced new evidence, boundary conditions, or refinements for existing insights, or if a new insight emerged — see Insight Update Protocol below. Discuss with collaborator before promoting maturity levels.

**Discovery protocol during placement:**
When a discovery surfaces, STOP placement work. Present finding with evidence. Discuss together. Decide:
- Add to taxonomy (new insight, maturity promotion, etc.)
- Flag for later (note in session log, don't promote yet)
- Dismiss (interesting but insufficient evidence)

**Field Journal Protocol (MANDATORY):**
The field journal (`synthesis/sessions/YYYY-MM-DD-*.md`) must capture ALL substantive analytical observations from the batch, including:
- Observations the botanist notices during the specimen read-through
- Decisions made during discussion (e.g., removing specimens, reclassifying)
- Connections to existing hypotheses raised by either collaborator
- Observations that emerge from the back-and-forth discussion, even if they don't rise to the level of a new insight
- Cross-specimen comparisons proposed by the user
- Refinements, boundary conditions, or moderating variables identified for existing hypotheses

The field journal is the primary analytical record of this project. If something substantive was discussed during a batch session, it belongs in the journal. Write it up before moving to the next batch or ending the session.

**Insight Update Protocol (MANDATORY):**
After each batch, check whether `synthesis/insights.json` needs updating. This is as important as the field journal — insights.json is the structured analytical output that feeds into writing. Update when:
- A batch provided **new supporting or counter-evidence** for an existing insight → add specimens, update evidence string
- Discussion identified **new boundary conditions or moderating variables** → update finding/implication text
- An insight's **maturity should change** (hypothesis → emerging → confirmed) based on accumulated evidence
- A **new insight emerged** from the batch → add new entry
- **Research targets changed** (e.g., a cluster was tested, shift targets to next untested cluster)

Insights are NEVER deleted, only updated or added. The insight update should reflect the full discussion, not just the read-through observations.

**Scoring guides:**

| Tension | ID | Negative Pole (-1) | Positive Pole (+1) | Key Question |
|---------|----|---------------------|---------------------|--------------|
| T1 | structuralVsContextual | Structural separation | Contextual integration | Separate AI unit, or everyone does AI? |
| T2 | speedVsDepth | Deep pilots | Wide deployment | Deploy broadly fast, or pilot deeply first? |
| T3 | centralVsDistributed | Centralized | Distributed | One hub controls, or BUs have autonomy? |
| T4 | namedVsQuiet | Named lab | Quiet transformation | Branded AI org/role, or no formal branding? |
| T5 | longVsShortHorizon | Long horizons | Short accountability | Multi-year R&D, or quarterly pressure? |

| Contingency | ID | Valid Levels |
|-------------|----|-------------|
| C1 | regulatoryIntensity | high, medium, low |
| C2 | timeToObsolescence | high (threatened), medium (augmented), low (stable), fast (rare) |
| C3 | ceoTenure | high (long), founder, medium, low (short), new, critical |
| C4 | talentMarketPosition | high, low, nonTraditional, talent-rich, talent-constrained |
| C5 | technicalDebt | high, medium, low |
| C6 | environmentalAiPull | high (existential), medium (competitive), low (optional), resistant |

**Stub policy:** If a specimen has insufficient data to score, skip that dimension and note "insufficient data — needs enrichment." Do NOT invent data.

**Analytical Primitives (P1-P5) — predict structural choice:**

| Primitive | ID | What It Captures |
|-----------|----|------------------|
| Work Architecture Modularity | P1 | Can the work be decomposed into discrete, independently optimizable tasks? |
| Work Output Measurability | P2 | Can quality and outcomes be captured in quantitative metrics? |
| Governance Structure | P3 | Who has formal and real authority over AI decisions? |
| Competitive/Institutional Context | P4 | Competitive dynamics, regulation, industry norms, labor markets |
| Organizational Endowment | P5 | Legacy systems, talent base, culture, prior AI investment |

**Core Findings (F1-F10) — empirical claims under investigation:**

| Finding | ID | Claim |
|---------|----|-------|
| Mirroring Thesis | F1 | Work architecture predicts structural model |
| Overcorrection Trap | F2 | Measurable metrics hide quality degradation in AI transitions |
| CEO Tenure Predicts Speed | F3 | Founder-CEOs mandate faster structural transformation |
| Regulation Is Expensive Not Slow | F4 | Compliance infrastructure enables deployment speed |
| Hub-Spoke Convergence | F5 | M4 dominates enterprise AI; industry > structure for rhetoric |
| Named Labs Attract Talent | F6 | Visibility and branding drive AI talent acquisition |
| Purpose Claims as Authorization | F7 | Leaders invoke purpose to legitimate structural change |
| Two-Speed IT | F8 | Shadow AI creates ungoverned parallel infrastructure |
| AI-Native Paradox | F9 | Born-AI firms face distinct coordination problems |
| Merger Creates Coordination Crisis | F10 | Consolidating AI teams triggers authority conflicts |

> **Exploration and Curiosity First.** These primitives and findings are analytical lenses, not filters. Evidence that contradicts or falls outside the framework receives the same analytical weight as confirming evidence. Novel patterns and surprises are just as important as framework-confirming observations.

Full framework details: `synthesis/ANALYTICAL-FRAMEWORK.md`, `synthesis/primitives.json`, `synthesis/findings.json`

**Inputs:**
- `specimens/*.json` — full specimen data (primary)
- `synthesis/*.json` — existing patterns (cross-reference)
- `synthesis/primitives.json` — 5 analytical primitives
- `synthesis/findings.json` — 10 core findings + field observations

**Outputs:**
- `synthesis/mechanisms.json` — updated mechanism evidence
- `synthesis/tensions.json` — specimen placements with evidence
- `synthesis/contingencies.json` — specimen level assignments
- `synthesis/findings.json` — core findings (evidence for/against, maturity changes)
- `synthesis/insights.json` — cross-cutting insights archive (NEVER deleted, only added/updated)
- `synthesis/sessions/*.md` — session journals with discoveries
- `scripts/patch-batch*.py` — patch scripts (one per batch, kept for audit trail)

**Why interactive matters:** Sessions 11-12 demonstrated the value. Batch 3 yielded the UnitedHealth "scale without signal" observation and IT services divergence. A re-examination of Batch 2 led to the mRNA-AI modularity fit idea, which connected to Nadella's Coase reference, producing the `modularity-predicts-ai-structure` hypothesis — the kind of theoretical chain that no automated pipeline would ever produce. Batch 4 revealed the automotive M4 convergence (10/13 specimens), GM's CAIO failure as natural experiment, and the "data foundation first" sequencing pattern. Every batch has been analytically productive when approached with curiosity rather than as rote data entry.

---

## Track 2: Purpose Claims Pipeline

### `/purpose-claims` — Verbatim Claim Collection

**What it does:** Systematically searches for verbatim statements by leaders invoking purpose/mission in AI adaptation context.

**When to use:** Building the purpose claims registry for academic paper.

**Invocation:**
```
/purpose-claims [specimen-id]     # Scan one specimen
/purpose-claims batch [id1,id2]   # Scan multiple specimens
```

**Inputs:**
- `specimens/{id}.json` — specimen context (leader name, model)
- `research/purpose-claims/scan-tracker.json` — what's been scanned
- `research/transcript-gap-queue.json` — known transcript sources
- `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` — finding more transcripts

**Outputs:**
- `research/purpose-claims/pending/{id}.json` — claims pending review
- `research/purpose-claims/registry.json` — merged claim registry
- Updates to `scan-tracker.json`

**Claim Type Taxonomy (v2.0 — 6 types):**
| Type | Core Question |
|------|---------------|
| `utopian` | "What future are we building?" — grandiose, unfalsifiable |
| `teleological` | "What outcome justifies our existence?" — specific, falsifiable |
| `higher-calling` | "What duty calls us?" — moral/ethical imperative |
| `identity` | "Who are we?" — character, values, culture |
| `survival` | "What threatens us if we don't act?" — existential urgency |
| `commercial-success` | "How will this create value?" — business case framing |

*v2.0 revision (Feb 8): reorganized around what END the claim invokes. Dropped employee-deal (not purpose claims), dissolved transformation-framing/sacrifice-justification/direction-under-uncertainty, added higher-calling/survival/commercial-success.*

**Quality filters (all three required):**
1. Verbatim exact words only
2. Made in context of AI adaptation
3. Traceable source with URL

**Key protocol steps:**
1. Load specimen context
2. **Check transcript availability** (TRANSCRIPT-DISCOVERY-PROTOCOL.md)
3. Mine existing specimen data for quotes
4. Run standard searches
5. Deep-scan transcripts (highest yield)
6. Record claims with full schema
7. Update scan-tracker

**Full spec:** `research/purpose-claims/PURPOSE-CLAIMS-SPEC.md`

### Purpose Claims Visualization Infrastructure

The purpose claims pipeline now includes visual analytics and enrichment display:

**Enrichment files** (`research/purpose-claims/enrichment/{specimen-id}.json`):
- Generated by purpose claims agents (required output since Session 7)
- Contains `claimTypeDistribution`, `keyFindings`, `rhetoricalPatterns`, `comparativeNotes`, `notableAbsences`, `quality`, metadata
- 130 enrichment files currently exist (backfilled + agent-generated)
- Loaded by `getSpecimenEnrichment()` / `getAllEnrichments()` in `site/lib/data/purpose-claims.ts`

**Spider/Radar Charts** (`site/components/visualizations/SpiderChart.tsx`):
- Pure React SVG, no D3 — 6 axes (one per claim type at 60° intervals), concentric grid rings, optional comparison overlay
- Normalization: `normalizeDistribution()` in `site/lib/utils/spider-data.ts` — proportional values rescaled so max axis reaches 0.85 of radius
- Used in 3 contexts: EnrichmentSummary (220px, interactive), EnrichmentCompact (140px, sidebar), ClaimsSpiderGrid (100px small multiples + 180px group averages)

**Spider Grid** (`site/components/purpose-claims/ClaimsSpiderGrid.tsx`):
- Replaces the Heatmap view on `/purpose-claims` page (view mode label: "Profiles")
- Groups by structural model or industry (toggle)
- Per-group: large average spider + small individual specimen spiders
- Hover shows comparison overlay (specimen vs. group average)
- Click drills into by-specimen view

**Citation System** (auditability infrastructure):
- `site/lib/utils/citations.ts` — Parses `[source-id]` markers in text strings
- `site/components/shared/CitedText.tsx` — Renders as superscript numbered links
- Wired into `OverviewTab.tsx` for specimen description and observable markers
- Source IDs must match entries in specimen's `sources[]` array
- **Curation protocol updated**: all new specimens should include `[source-id]` markers in observable markers
- **34 specimens backfilled** so far — more specimens need citation backfill

### Track 2 Architecture: Collect vs. Enrich (Design Note)

**Current design (v1):** Collection and enrichment happen in a single agent pass. Each agent scans one specimen, collects claims, and generates `specimenEnrichment` (keyFindings, rhetoricalPatterns, comparativeNotes) — all in one output file. The overnight script merges claims into registry.json and writes enrichment to separate files.

**Limitation:** Each agent can only see its own specimen. The `comparativeNotes` and `rhetoricalPatterns` fields are generated without access to the full claims registry. Cross-specimen patterns (e.g., "pharma CEOs cluster on teleological claims") are only visible post-hoc in analysis mode.

**Future design (v2 — when needed):** Split into two phases:

| Phase | Script | What it does |
|-------|--------|--------------|
| **Collect** | `overnight-purpose-claims.py` (current) | Scan specimens, collect verbatim claims, write to pending/ and merge to registry.json |
| **Enrich** | `overnight-purpose-enrich.py` (new) | Read full registry + all specimens. Generate enrichment files with cross-specimen comparative analysis. Batch by structural model or industry. |

**When to split:** When the enrichment quality noticeably suffers from single-specimen context. Current enrichment is adequate — agents often produce insightful comparative notes by drawing on their training knowledge of the companies. Split when we need enrichment for the paper.

**What changes:**
1. Agent prompt for collection drops the `specimenEnrichment` requirement (faster, simpler)
2. New enrichment script reads full registry, groups by model/industry, generates richer comparative analysis
3. Enrichment files get a `version` field to track whether they were v1 (per-agent) or v2 (cross-specimen)
4. Scan-tracker gets a separate `enrichmentDate` field

**What stays the same:** Registry.json structure, scan-tracker quality levels, claim schema, merge protocol.

---

## Shared Infrastructure: Transcript Discovery

### Protocol: `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`

Both `/research` and `/purpose-claims` use this protocol to systematically find interview transcripts.

**Core principle:** Be creative and energetic about finding transcripts. Don't limit to hardcoded podcast lists.

**Data files:**
| File | Purpose |
|------|---------|
| `research/transcript-sources.json` | Registry of transcript sources |
| `research/transcript-gap-queue.json` | Specimen × source pairs with scan status |

**Phase 1: Quick Discovery (run for any specimen)**
1. Identify leader name(s) from specimen
2. Run leader-centric searches: `"[name]" podcast interview`, `"[name]" site:dwarkesh.com`, etc.
3. Run company-centric searches: `"[company]" earnings call transcript`
4. Check formal sources: congressional testimony, analyst days
5. Classify each source: quality tier, access method, AI relevance
6. Record in data files

**Phase 2: Deep Discovery (for high-priority or thin specimens)**
- Broader YouTube search
- Conference channels (Web Summit, TED, Davos)
- Third-party transcriptions (podscripts.co, rev.com)
- Industry-specific sources

**Quality tiers:**
| Tier | Access | Example |
|------|--------|---------|
| `native` | Programmatic | Dwarkesh, Acquired, Lex Fridman |
| `third-party` | Programmatic | News outlets quoting extensively |
| `auto-generated` | Manual required | YouTube auto-captions |

---

## Supporting Commands

### `/update-literature` — Literature Registry

**What it does:** Scans for new research papers and generates registry entries.

**When to use:** When adding academic papers to literature review.

**Inputs:** `library/research papers/*.pdf`
**Outputs:** `research/literature/registry.json`

---

## Quick Reference: Which Command When?

| I want to... | Command | Track |
|--------------|---------|-------|
| Find new organizational AI structure data | `/research` | 1 |
| Scan earnings calls for structural signals | `/research` (earnings mode) | 1 |
| Create/update a specimen card | `/curate` | 1 |
| Analyze patterns across specimens | Interactive synthesis (see Phase 3) | 1 |
| Find purpose claims for a specimen | `/purpose-claims [id]` | 2 |
| Find transcripts for deep scanning | Follow TRANSCRIPT-DISCOVERY-PROTOCOL.md | Both |
| Add papers to literature review | `/update-literature` | Support |

---

## File Map

```
research/
├── sessions/                      # Research session files
├── queue.json                     # Orgs pending curation
├── SESSION-PROTOCOL.md            # Research protocol
├── TRANSCRIPT-DISCOVERY-PROTOCOL.md  # Shared transcript finding
├── transcript-sources.json        # Source registry
├── transcript-gap-queue.json      # Specimen × source tracking
├── purpose-claims/
│   ├── registry.json              # All collected claims (v2.0 taxonomy)
│   ├── scan-tracker.json          # What's been scanned
│   ├── PURPOSE-CLAIMS-SPEC.md     # Full spec
│   ├── analytical-notes.md        # Patterns observed
│   ├── pending/                   # Claims pending merge
│   ├── enrichment/                # Per-specimen enrichment files (130 files)
│   │   └── {specimen-id}.json     # claimTypeDistribution, keyFindings, etc.
│   └── sessions/                  # Scanning session logs
├── literature/
│   └── registry.json              # Academic literature
└── field-signals.json             # Macro field observations

specimens/
├── registry.json                  # Master specimen list
├── source-registry.json           # Source scanning status
└── *.json                         # Specimen files (see registry.json for count)

synthesis/
├── mechanisms.json                # Confirmed + candidate mechanisms
├── tensions.json                  # 5 structural tensions
├── contingencies.json             # 6 contingency factors
└── insights.json                  # Field insights (growing collection)

curation/
├── synthesis-queue.json           # Specimens pending synthesis
└── sessions/                      # Curation session logs
```

---

## Session File Naming (All Tracks)

All session files across all tracks follow this pattern:

```
YYYY-MM-DD-{descriptor}.md
```

| Directory | Prefix convention | Examples |
|-----------|-------------------|----------|
| `research/sessions/` | Date + type + scope | `2026-02-14-research-podcasts-press.md`, `2026-02-14-earnings-q4-amazon.md` |
| `curation/sessions/` | Date + "curation" + scope | `2026-02-14-curation-batch5.md` |
| `synthesis/sessions/` | Date + "synthesis" + scope | `2026-02-14-synthesis-batch1.md` |
| `research/purpose-claims/sessions/` | Date + type | `2026-02-14-batch-15-pharma.md`, `2026-02-14-scan-microsoft.md`, `2026-02-14-overnight-run.md` |

**Overnight script sessions:** Overnight scripts name their sessions `YYYY-MM-DD-overnight-{track}.md` (e.g., `overnight-run.md` for purpose claims, `overnight-curate-run.md` for curation).

**Historical files:** Pre-2026-02-14 files may not follow this convention. Don't rename them.

---

## Typical Session Flow

### "I want to do a research session"
```
1. /research
   - Check source registry for gaps
   - Scan multiple source types
   - Record findings to session file
   - Update queue.json

2. /curate
   - Process pending items
   - Create/update specimens

3. Interactive synthesis (botanist hat ON)
   - Read specimens in sector batches
   - Score tensions + contingencies with evidence
   - Watch for discoveries — pause, discuss, decide
   - Write patch script, validate
   - Log discoveries in session journal

4. Update APP_STATE.md
5. Run validation: node scripts/validate-workflow.js
```

### "I want to collect purpose claims for a specimen"
```
1. Check transcript-gap-queue.json for known transcripts
2. If none, run transcript discovery (Phase 1)
3. /purpose-claims [specimen-id]
   - Mine existing specimen data
   - Run standard searches
   - Deep-scan transcripts
   - Record claims to pending/
4. Merge to registry.json
5. Update scan-tracker.json
```

---

## Specimen Lifecycle Gates

Every specimen moves through a defined lifecycle. Each gate defines what "done" means at that stage. Use `data/specimen-lifecycle-status.json` to track progress programmatically.

| Stage | Gate | How to verify |
|-------|------|---------------|
| **1. Researched** | Findings in `research/queue.json` with at least 1 structural observation | Check queue.json for specimen slug |
| **2. Curated** | Specimen file exists in `specimens/{id}.json` with classification, ≥1 source, ≥1 layer | `meta.status` ∈ {Active, Stub}, classification populated |
| **3. Placed** | Tension positions scored + contingencies assessed | ≥3 non-null `tensionPositions` fields, ≥3 non-null `contingencies` fields |
| **4. Synthesized** | Appears in `synthesis-queue.json` with `status: synthesized` | Check synthesis-queue for specimenId |
| **5. Claims collected** | Entry in `scan-tracker.json` with `quality` ≠ `unscanned` | `quality` ∈ {rich, adequate, thin, none} |
| **6. Enriched** | Enrichment file exists at `research/purpose-claims/enrichment/{id}.json` with keyFindings + rhetoricalPatterns | File exists with non-empty arrays |
| **7. Citation-ready** | All sources have `sourceUrl` + `sourceDate` + `collectedDate` | 0 warnings in validator Section 2 |

**"Done" for research scale-up:** A specimen is considered research-complete when it reaches Stage 6 (Enriched). Stage 7 is aspirational and can be backfilled.

**Stubs:** Remain at Stage 2 until sufficient data is found to progress. Stubs are legitimate — "not enough data yet" is a valid state.

---

## Operational Infrastructure

### Nightly Pipeline (Autonomous)

The nightly pipeline runs research → curate → purpose claims → synthesis → validation → morning briefing on a 7-day themed rotation. Config: `scripts/pipeline-schedule.json`. All phases are **framework-aware** (Session 36): research agents carry P1-P5 primitive antenna, curation agents tag `primitiveIndicators` and `findingRelevance`, and synthesis evaluates evidence for/against findings F1-F10.

**Running the pipeline:**
```bash
# Preview tonight's schedule
python3 scripts/overnight-pipeline.py --dry-run

# Run for real (unattended)
python3 scripts/overnight-pipeline.py --skip-permissions

# Force a specific day
python3 scripts/overnight-pipeline.py --dry-run --day monday

# Run a single phase
python3 scripts/overnight-pipeline.py --phase 4 --skip-permissions  # synthesis only
```

**Weekly schedule (2-3 themed research batches per night):**

| Day | Primary Theme | Secondary | Tertiary |
|-----|--------------|-----------|----------|
| Mon | Earnings sweep | Press keyword sweep | — |
| Tue | Tier 1+2 podcasts | Tier 2.5 podcasts | Daily news scan |
| Wed | Substacks (all tiers) | Enterprise reports | Target specimens (new) |
| Thu | Stale refresh (oldest 8) | Target specimens (enrich) | Press keyword sweep |
| Fri | Earnings follow-up | Low-confidence specimens | Taxonomy gap coverage |
| Sat | Tier 3 podcasts | Industry discovery | — |
| Sun | Source staleness audit | Catch-up (adaptive) | — |

**Morning review workflow:**
1. Check `pipeline-reports/YYYY-MM-DD-morning-briefing.md` — phase summary
2. Check `pipeline-reports/YYYY-MM-DD-field-journal.md` — synthesis audit trail
3. Review any new insights in `synthesis/insights.json`
4. Adjust any autonomous placements if needed

**Scheduling via launchd (7 PM daily):**
```bash
cp scripts/com.fieldguide.overnight-pipeline.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.fieldguide.overnight-pipeline.plist
```

### Running Individual Scripts

```bash
# Research with a specific theme
python3 scripts/overnight-research.py --schedule-theme press-keyword --limit 4 --dry-run

# Individual scripts (legacy mode)
python3 scripts/overnight-research.py --dry-run
python3 scripts/overnight-purpose-claims.py --dry-run
python3 scripts/overnight-curate.py --dry-run
python3 scripts/overnight-synthesis.py --dry-run
```

**Safety features:**
- Atomic writes: data written to `.tmp` → validated → backup created → atomic rename
- Lock files: `scripts/.locks/` prevents concurrent runs (PID-based, stale-lock detection)
- Preflight checks: all required files validated before expensive agent runs
- Changelog: every data modification logged to `data/CHANGELOG.md`
- Registry rebuild: `overnight-curate.py` automatically runs `rebuild-registry.js` after successful curation
- Time-budget-aware: orchestrator tracks elapsed time, skips optional batches if running long
- Field journal: autonomous synthesis writes full audit trail of every placement with rationale

**What the pipeline updates:**
- `research/pending/*.json` — Research findings
- `specimens/*.json` — Specimen cards (via curate)
- `purpose-claims/registry.json` — Purpose claims
- `synthesis/*.json` — Tension scores, contingency placements, mechanism links, insights (via autonomous synthesis)
- `pipeline-reports/*.md` — Morning briefings and field journals

### Post-Run Verification

After any overnight run or data modification:

```bash
# 1. Check consistency (REQUIRED — 0 errors expected)
node scripts/validate-workflow.js

# 2. Verify site builds (REQUIRED)
cd site && npm run build

# 3. Review what changed
# Check data/CHANGELOG.md for timestamped entries

# 4. Update lifecycle dashboard (recommended)
node scripts/specimen-lifecycle-status.js

# 5. Check source freshness (recommended)
node scripts/check-source-freshness.js
```

### When to Run Specific Scripts

| Script | When to Run |
|--------|-------------|
| `validate-workflow.js` | After ANY data change. Must show 0 errors. |
| `rebuild-registry.js` | After adding/removing specimen files, or if validator reports registry mismatch |
| `specimen-lifecycle-status.js` | Before synthesis sessions (to see which specimens need attention) |
| `check-source-freshness.js` | Before research sessions (to prioritize stale sources) |

### Lock and Backup File Conventions

- **Lock files:** `scripts/.locks/{script-name}.lock` — contains PID. Git-ignored.
- **Backup files:** `*.bak` created by `save_json()` before overwriting. Git-ignored.
- **Stale locks:** If a script crashes without releasing its lock, the next run detects the dead PID and warns. Remove manually if needed: `rm scripts/.locks/*.lock`

---

## Version History

| Date | Change |
|------|--------|
| 2026-02-06 | Created WORKFLOW.md. Consolidated all command documentation. Added Transcript Discovery Protocol integration. |
| 2026-02-09 | **DEPRECATED automated `/synthesize` and `overnight-synthesis.py`.** Replaced with Interactive Botanist Mode. Added tension scoring guide, contingency level guide, stub policy, and discovery protocol. Documented why interactive synthesis is required (Sessions 11-12 demonstrated that every batch yields analytical discoveries when approached with curiosity). |
| 2026-02-12 | Updated claim type taxonomy to v2.0 (6 types). Added Purpose Claims Visualization Infrastructure section (enrichment files, spider charts, spider grid, citation system). Updated file map with enrichment directory. |
| 2026-02-14 | Added Operational Infrastructure section: overnight automation procedures, post-run verification checklist, lock/backup conventions. |
