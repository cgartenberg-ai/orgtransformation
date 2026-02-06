# Session Handoff — February 6, 2026 (Evening)

**Project:** Ambidexterity Field Guide (`/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/`)

---

## CRITICAL: Read This First

All Feb 3-6 work is **committed**. Major infrastructure work completed AND tested: PURPOSE-CLAIMS-SPEC.md, WORKFLOW.md, Transcript Discovery Protocol, and first batch of scaled purpose claims scanning.

### What Was Just Completed (Feb 6 Evening)

1. **Scaled Purpose Claims to 113 claims across 14 specimens**
   - Merged 10 google-deepmind claims from pending (Hassabis: teleological, identity, utopian, direction-under-uncertainty from 3 transcripts)
   - Scanned SSI: 8 claims (Sutskever) — pure identity/teleological/direction-under-uncertainty mix
   - Scanned Sierra-AI: 6 claims (Taylor/Bavor) — utopian, teleological, identity mix
   - Updated transcript-gap-queue.json (SSI and Sierra marked scanned, new Acquired episode added)

2. **Earlier today: Infrastructure**
   - PURPOSE-CLAIMS-SPEC.md — 7-type taxonomy
   - Transcript Discovery Protocol — 17 sources registered
   - WORKFLOW.md — Complete command reference
   - Tested workflow on google-deepmind (worked end-to-end)

### Three Priorities for Next Session

1. **Google/Amazon Q4 2025 earnings.** Transcripts should be available now. Run `/research` earnings sessions. High priority — time-sensitive.

2. **Continue purpose claims Batch 3.** Scan pharma specimens: novo-nordisk, pfizer, sanofi, roche-genentech. Also mercor (Brendan Foody on Conversations with Tyler).

3. **Run transcript discovery sweep.** Use Phase 1 Quick Sweep for high-priority unscanned specimens. 79 specimens still unscanned for purpose claims.

### Also Pending (Lower Priority)

4. **Purpose claims synthesis protocol.** Design pattern lifecycle so patterns consolidate.
5. **Travelers reclassified M4→M2.** Synthesis files not yet updated.

---

## Current State of the Herbarium

### Key Numbers
- **93 specimens** total (all synthesized — 0 pending)
- **113 purpose claims** across 14 specimens (7 types, v1.0 taxonomy)
- **79 specimens unscanned** for purpose claims
- **14 patterns**, **5 hypotheses** in analytical notes
- **9 confirmed mechanisms** + 9 candidates
- **13 field insights**
- **25 field signals**
- **5 tensions**, **5 contingencies**
- **44 sources** tracked (19 Tier 1, 25 Tier 2)
- **17 papers** in literature registry
- **17 transcript sources** registered, **6 transcript sources scanned**

### Purpose Claims Status

| Batch | Specimens | Claims | Status |
|-------|-----------|--------|--------|
| Pilot | meta-ai | 11 | Complete |
| Batch 1 | microsoft, shopify, amazon-agi, servicenow, eli-lilly, anthropic | 48 | Complete |
| Batch 2 | accenture-openai, salesforce, klarna, sk-telecom | 30 | Complete |
| Batch 3 | google-deepmind, ssi, sierra-ai | 24 | **Complete** |
| Batch 4+ | 79 remaining specimens | — | Pending |

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
**Output:** 113 claims across 14 specimens (growing)

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
