# Session Handoff — February 6, 2026

**Project:** Ambidexterity Field Guide (`/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/`)

---

## CRITICAL: Read This First

All Feb 3-6 work is **committed**. Major infrastructure work completed: PURPOSE-CLAIMS-SPEC.md, WORKFLOW.md, and Transcript Discovery Protocol.

### What Was Just Completed (Feb 6)

1. **PURPOSE-CLAIMS-SPEC.md** — Comprehensive data layer spec for purpose claims. 7-type taxonomy (added `teleological`). Taxonomy evolution protocol. Full claim schema.

2. **Transcript Discovery Protocol** — Systematic infrastructure for finding interview transcripts:
   - `research/transcript-sources.json` — 13 seed sources
   - `research/transcript-gap-queue.json` — expanded schema with quality/status tracking
   - `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` — Phase 1 quick sweep + Phase 2 deep discovery
   - Integration into both `/research` (Step 2b) and `/purpose-claims` (Step 1)

3. **WORKFLOW.md** — Complete command reference documenting both research tracks, all skills, and typical session flows. Single source of truth for "how does this work?"

4. **CLAUDE.md** — Updated to reflect two-track architecture and reference WORKFLOW.md.

### Three Priorities for Next Session

1. **Run transcript discovery for high-priority specimens.** Use the new protocol to find podcast/interview transcripts for the 82 unscanned purpose claims specimens. Start with the 10 known pairs in `transcript-gap-queue.json`. Goal: build the queue of programmatically-accessible transcripts before scanning more specimens.

2. **Scan purpose claims Batch 3.** With transcript infrastructure in place, scan pharma specimens for direction-under-uncertainty claims: novo-nordisk, pfizer, sanofi, roche-genentech. Use foreground serial scanning (background agents can't do web search).

3. **Google/Amazon Q4 2025 earnings.** Transcripts should be available now. Run `/research` earnings sessions.

### Also Pending (Lower Priority)

4. **Purpose claims synthesis protocol.** Design pattern lifecycle (emerging → confirmed → deprecated) so patterns consolidate rather than grow additively.
5. **Travelers reclassified M4→M2.** Synthesis files not yet updated for reclassification.

---

## Current State of the Herbarium

### Key Numbers
- **93 specimens** total (all synthesized — 0 pending)
- **89 purpose claims** across 11 specimens (7 types, v1.0 taxonomy)
- **82 specimens unscanned** for purpose claims
- **14 patterns**, **5 hypotheses** in analytical notes
- **9 confirmed mechanisms** + 9 candidates
- **13 field insights**
- **25 field signals**
- **5 tensions**, **5 contingencies**
- **44 sources** tracked (19 Tier 1, 25 Tier 2)
- **17 papers** in literature registry
- **13 transcript sources** registered, **10 specimen × transcript pairs** known

### Purpose Claims Status

| Batch | Specimens | Claims | Status |
|-------|-----------|--------|--------|
| Pilot | meta-ai | 11 | Complete |
| Batch 1 | microsoft, shopify, amazon-agi, servicenow, eli-lilly, anthropic | 48 | Complete |
| Batch 2 | accenture-openai, salesforce, klarna, sk-telecom | 30 | Complete |
| Batch 3+ | 82 remaining specimens | — | Pending |

### Earnings Season — Active (Q4 2025)

| Company | Status | Date |
|---------|--------|------|
| Microsoft | Scanned + Synthesized | Jan 28 |
| Meta | Scanned + Synthesized | Jan 29 |
| Salesforce (Q3 FY2026) | Scanned + Synthesized | Dec 3 |
| Travelers | Scanned + Synthesized | Jan 22 |
| ServiceNow | Scanned + Synthesized | Jan 29 |
| Accenture | Scanned + Synthesized | Jan 30 |
| Google | **PENDING** | Feb 4 |
| Amazon | **PENDING** | Feb 5 |

---

## Key Documents

| Document | Purpose | Read When |
|----------|---------|-----------|
| `APP_STATE.md` | Full project state + session log | Every session |
| `WORKFLOW.md` | **Complete command reference** | Running any workflow |
| `CLAUDE.md` | Session bootstrap, project structure | Auto-read |
| `Ambidexterity_Field_Guide_Spec.md` | Taxonomy, specimen schema | Research/curation |
| `research/purpose-claims/PURPOSE-CLAIMS-SPEC.md` | Claim types, schema, quality rules | Purpose claims work |
| `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` | Finding transcripts | Both tracks |

---

## Two Research Tracks (Quick Reference)

### Track 1: Structural Research
```
/research → /curate → /synthesize
```
**Question:** How do organizations structure AI work?
**Output:** 93 specimens, 9 mechanisms, 13 insights

### Track 2: Purpose Claims
```
/purpose-claims [specimen-id]
```
**Question:** How do leaders use purpose to authorize transformation?
**Output:** 89 claims across 11 specimens (growing)

**Shared infrastructure:** Transcript Discovery Protocol

---

## Implicit Knowledge

1. **Background agents can't do web search.** Use foreground serial scanning for purpose claims.
2. **Foreground serial scanning works well.** ~3-5 web searches + 1-2 fetches per specimen.
3. **Synthesis context overflow**: Manual batched synthesis needed (context too large).
4. **Edit tool + JSON**: Large JSON edits often fail. Include more surrounding context.
5. **Insights guardrail**: Insights are NEVER deleted — only updated or new ones added.
6. **Stratigraphic principle**: New specimen layers prepended to `layers[0]`, old layers never modified.
7. **YouTube transcripts require manual extraction.** Flag as `manual-required` and queue for user.
