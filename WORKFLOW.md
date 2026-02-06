# Project Workflow: Complete Command Reference

## Last Updated: February 6, 2026

This document is the single source of truth for **all research workflows and commands** in the Ambidexterity Field Guide project.

---

## Overview: Two Parallel Research Tracks

The project has **two parallel research tracks**, each with its own pipeline:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TRACK 1: STRUCTURAL RESEARCH                            │
│              "How do organizations structure AI work?"                          │
│                                                                                 │
│   /research → /curate → /synthesize → [insights.json, mechanisms.json, etc.]   │
│                                                                                 │
│   Output: 93 specimen cards, 9 mechanisms, 13 insights, 5 tensions              │
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
- The same 93 specimens as subjects
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

**Inputs:**
- `research/queue.json` — pending orgs from research
- `research/sessions/*.md` — session files with findings
- Existing `specimens/*.json` if updating

**Outputs:**
- `specimens/{id}.json` — new or updated specimen cards
- `curation/synthesis-queue.json` — specimens pending synthesis
- `curation/sessions/*.md` — curation session log

**Key protocol steps:**
1. Read research findings for each org
2. Classify by model (M1-M9) and orientation
3. Create/update specimen with layers
4. Queue for synthesis

---

### Phase 3: `/synthesize` — Pattern Analysis

**What it does:** Identifies cross-cutting patterns across specimens.

**When to use:** After `/curate` has processed specimens.

**Invocation:**
```
/synthesize                  # Process pending items in synthesis queue
/synthesize [specimen-id]    # Analyze a specific specimen
```

**Inputs:**
- `curation/synthesis-queue.json` — pending specimens
- `specimens/*.json` — full specimen data
- `synthesis/*.json` — existing patterns

**Outputs:**
- `synthesis/mechanisms.json` — confirmed patterns
- `synthesis/tensions.json` — structural tensions
- `synthesis/contingencies.json` — contextual factors
- `synthesis/insights.json` — cross-cutting findings (NEVER deleted)

**Key protocol steps:**
1. Read specimen data
2. Match to existing mechanisms
3. Check tension placement
4. Identify contingency factors
5. Update or add insights

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

**Claim Type Taxonomy (v1.0 — 7 types):**
| Type | Core Question |
|------|---------------|
| `utopian` | "What future are we building?" — grandiose, unfalsifiable |
| `identity` | "Who are we?" — character, values, culture |
| `teleological` | "What outcome justifies our existence?" — specific, falsifiable |
| `transformation-framing` | "What are we becoming?" — org changing form |
| `employee-deal` | "What do we expect from people?" — employment contract reset |
| `sacrifice-justification` | "Why is this pain worth it?" — cost + purpose |
| `direction-under-uncertainty` | "Why are we betting on this?" — no clear ROI |

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

---

## Shared Infrastructure: Transcript Discovery

### Protocol: `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`

Both `/research` and `/purpose-claims` use this protocol to systematically find interview transcripts.

**Core principle:** Be creative and energetic about finding transcripts. Don't limit to hardcoded podcast lists.

**Data files:**
| File | Purpose |
|------|---------|
| `research/transcript-sources.json` | Registry of 13+ transcript sources |
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
| Analyze patterns across specimens | `/synthesize` | 1 |
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
│   ├── registry.json              # All collected claims
│   ├── scan-tracker.json          # What's been scanned
│   ├── PURPOSE-CLAIMS-SPEC.md     # Full spec
│   ├── analytical-notes.md        # Patterns observed
│   ├── pending/                   # Claims pending merge
│   └── sessions/                  # Scanning session logs
├── literature/
│   └── registry.json              # Academic literature
└── field-signals.json             # Macro field observations

specimens/
├── registry.json                  # Master specimen list
├── source-registry.json           # Source scanning status
└── *.json                         # 93 specimen files

synthesis/
├── mechanisms.json                # 9 confirmed mechanisms
├── tensions.json                  # 5 structural tensions
├── contingencies.json             # 5 contingency factors
└── insights.json                  # 13 field insights

curation/
├── synthesis-queue.json           # Specimens pending synthesis
└── sessions/                      # Curation session logs
```

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
   - Queue for synthesis

3. /synthesize
   - Match to mechanisms
   - Place in tensions
   - Update insights

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

## Version History

| Date | Change |
|------|--------|
| 2026-02-06 | Created WORKFLOW.md. Consolidated all command documentation. Added Transcript Discovery Protocol integration. |
