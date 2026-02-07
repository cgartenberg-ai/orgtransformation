# Session Handoff — February 7, 2026

**Project:** Ambidexterity Field Guide (`/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/`)

---

## CRITICAL: Read This First

All Feb 3-7 work: Batch 4 pharma purpose claims **fully merged** (53 claims from pfizer/novo-nordisk/roche-genentech/sanofi). Agent model decision: **Opus** (not Sonnet — Sonnet crashes during WebFetch, Opus completes reliably with superior analysis quality). Infrastructure improvements (cross-pollination, parallel research, permissions).

### What Was Just Completed (Feb 7)

1. **Batch 4 Pharma Purpose Claims — FULLY MERGED (4 of 4)**
   - Pfizer: **10 claims** (rich) — Bourla's "scientific renaissance" narrative
   - Novo Nordisk: **11 claims** (rich) — distributed across 6 AI/digital leaders (no CEO claims!)
   - Roche-Genentech: **18 claims** (rich) — Regev is the richest single speaker in the collection
   - Sanofi: **14 claims** (rich) — Hudson richest pharma CEO, "AI Fight Club," agency-problem framing
   - **Registry now at 166 claims across 18 specimens** (was 113 across 14)

2. **Agent Model Decision: Opus**
   - Ran Sonnet vs Opus comparison on Sanofi: Sonnet agent crashed during WebFetch (0 output), Opus completed with 14 rich claims
   - Opus produces superior rhetorical function analysis and completes reliably
   - SKILL.md updated: `model: "opus"`, serial WebFetch, 5 queries, one-retry-max, ~15-25 min per specimen
   - WebFetch latency (not model speed) is the real bottleneck — both models spend 90%+ time waiting on network

3. **Cross-Pollination Pipeline (research ↔ purpose claims)**
   - Research agents capture purpose claims opportunistically → `purposeClaimsDiscovered` array
   - Purpose claims skill checks for research cross-pollination leads in Step 1
   - Bidirectional data flow between both tracks complete

4. **Parallel Research Agent Infrastructure**
   - `/research` SKILL.md redesigned for background agent parallelism
   - Task types: earnings, podcast-deep-scan, press-keyword, transcript-scan, specimen-targeted
   - Merge protocol with pending/*.json pattern (no write conflicts)

5. **Analytical Notes Updated (4 new patterns)**
   - #15: Patient-outcome anchoring universal in pharma
   - #16: CEO gap — pharma AI claims from AI/digital leaders, not CEO
   - #17: Regev as outlier data point (18 claims, all 7 types)
   - #18: Direction-under-uncertainty overrepresented in pharma
   - H1 revised: industry moderates model→claim relationship

### Immediate Next Steps (Start Here)

1. **Commit all Feb 7 changes** — SKILL.md updates, Batch 4 claims (all 4 merged), analytical notes, model decision.

2. **Run Batch 5** (4 specimens) with Opus agents. ~15-25 min per specimen expected.

3. **Clean up pending files** — sanofi-opus-comparison.json can be deleted after commit.

---

## Complete Research Roadmap

### Phase 1: Purpose Claims Web Scan (~20 batches)

Systematic web-based purpose claims scanning for all 75 remaining unscanned specimens. 4 specimens per batch, max 4 parallel agents.

**Priority order:**
1. High-completeness specimens (3): already data-rich, claims will be contextually strong
2. Medium-completeness specimens (21): good structural data, claims add depth
3. Low-completeness specimens (51): thin structural data, claims may surface new structural info too

**Estimated:** ~20 batches × 4 specimens = 80 specimens covered. ~3-4 sessions at 5-6 batches/session.

### Phase 2: Transcript Discovery + Deep Scan (~10-15 batches)

Run the Transcript Discovery Protocol across all 93 specimens, then deep-scan discovered transcripts.

**Current state:**
- 17 transcript sources registered in transcript-sources.json
- Only 15 specimen×source pairs discovered (in transcript-gap-queue.json)
- Only 5 scanned, 10 still `discovered` but unscanned
- 78+ specimens have zero transcript discovery coverage

**Sub-phases:**

**2a. Discovery sweep** (~10 batches, ~10 specimens/batch):
For each specimen, run Phase 1 Quick Sweep search patterns against all 17 sources + open-ended discovery. Record new specimen×source pairs in transcript-gap-queue.json.

**2b. Programmatic transcript scanning** (~5-10 batches):
For all pairs with `transcriptAccess: programmatic`, fetch and deep-scan for BOTH structural findings AND purpose claims. This is where the cross-pollination pipeline pays off — research agents capture purpose claims, purpose claims agents capture structural leads.

**2c. YouTube/manual queue**:
Flag `manual-required` sources (Bloomberg YouTube, CNBC YouTube, Fortune YouTube) for user batch processing. User extracts transcripts manually, then agents scan them.

**Why this phase matters:** Web-based purpose claims scanning (Phase 1) finds claims in press articles and earnings calls. Transcript deep-scanning finds claims in long-form interviews where leaders speak more candidly. Specimens that came up `thin` or `none` in Phase 1 may become `rich` after transcript mining.

### Phase 3: Earnings Season — Q4 2025 Coverage (~9 batches)

33 unscanned companies from earnings-calendar.json. Uses the new parallel research agent infrastructure.

**Priority tiers:**
- **Critical** (done): microsoft, meta, google, amazon, salesforce, travelers, servicenow, accenture
- **High priority** (next): eli-lilly, jpmorgan, nvidia, sap, ubs, ups, walmart, infosys, siemens, klarna, sanofi, pfizer, moderna, novo-nordisk
- **Standard**: remaining 19 companies

**Estimated:** ~9 batches × 2-3 companies/agent × 4 agents = 33 companies covered. ~3 sessions.

### Phase 4: New Specimens + Discovery

- **Goldman Sachs** — already queued. Gather structural data + purpose claims.
- **Discovery from transcript sweep** — Phase 2 will surface new organizations mentioned in interviews
- **Discovery from earnings** — Phase 3 may reveal new AI-structural moves by companies not yet in the herbarium

### Phase 5: Synthesis & Housekeeping

- **Purpose claims synthesis protocol** — Design pattern lifecycle so patterns consolidate across 100+ claims
- **CapEx arms race synthesis** — Google $175-185B, Amazon $200B, Meta, Microsoft. Major structural pattern.
- **Travelers reclassified M4→M2** — Synthesis files not yet updated
- **Cross-specimen pattern analysis** — Once claims reach ~200+, run systematic pattern detection

### Phase Ordering Notes

- Phases 1 and 2 can **interleave**: run 5-6 Phase 1 batches, then start Phase 2a discovery sweep. Specimens that came up thin in Phase 1 get prioritized in Phase 2b transcript scanning.
- Phase 3 (earnings) can run **in parallel** with Phases 1-2 since it uses different source types.
- Phase 4 depends on Phases 2-3 for discovery.
- Phase 5 should start once purpose claims cross ~150-200 total (enough mass for pattern detection).

### Also Pending (Lower Priority)

- **Purpose claims synthesis protocol.** Design pattern lifecycle so patterns consolidate.
- **Travelers reclassified M4→M2.** Synthesis files not yet updated.

---

## Current State of the Herbarium

### Key Numbers
- **93 specimens** total (all synthesized — 0 pending)
- **166 purpose claims** across 18 specimens (7 types, v1.0 taxonomy)
- **75 specimens unscanned** for purpose claims
- **18 patterns**, **5 hypotheses** in analytical notes (4 new pharma patterns this session)
- **9 confirmed mechanisms** + 9 candidates
- **13 field insights**
- **25 field signals**
- **5 tensions**, **5 contingencies**
- **44 sources** tracked (19 Tier 1, 25 Tier 2)
- **17 papers** in literature registry
- **17 transcript sources** registered, **5 transcript sources scanned**, **10 discovered but unscanned**

### Purpose Claims Status

| Batch | Specimens | Claims | Status |
|-------|-----------|--------|--------|
| Pilot | meta-ai | 11 | Complete |
| Batch 1 | microsoft, shopify, amazon-agi, servicenow, eli-lilly, anthropic | 48 | Complete |
| Batch 2 | accenture-openai, salesforce, klarna, sk-telecom | 30 | Complete |
| Batch 3 | google-deepmind, ssi, sierra-ai | 24 | Complete |
| Batch 4 | pfizer, novo-nordisk, roche-genentech, sanofi | 53 (merged) | **Complete** |
| Batch 5+ | 75 remaining specimens | — | Pending (see Roadmap) |

### Earnings Season — Active (Q4 2025)

| Company | Status | Date |
|---------|--------|------|
| Microsoft | Scanned + Synthesized | Jan 28 |
| Meta | Scanned + Synthesized | Jan 29 |
| Salesforce (Q3 FY2026) | Scanned + Synthesized | Dec 3 |
| Travelers | Scanned + Synthesized | Jan 22 |
| ServiceNow | Scanned + Synthesized | Jan 29 |
| Accenture | Scanned + Synthesized | Jan 30 |
| Google | **Scanned + Synthesized** | Feb 4 |
| Amazon | **Scanned + Synthesized** | Feb 5 |

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
**Output:** 166 claims across 18 specimens (growing — 75 specimens unscanned)

**Shared infrastructure:** Transcript Discovery Protocol, Cross-Pollination Pipeline (research ↔ purpose claims)

---

## Implicit Knowledge

1. **Background agents CAN do web search** (as of Feb 7, 2026). Global permissions in `~/.claude/settings.json` broadly allow all tools. Max 4 agents in parallel to avoid context overflow.
2. **Parallel scanning is preferred.** Launch up to 4 background agents simultaneously for both purpose claims and research batches.
3. **Cross-pollination is live.** Research agents capture purpose claims → `purposeClaimsDiscovered` array → pending files. Purpose claims agents check for research cross-pollination leads in Step 1.
4. **Research agents use pending/*.json pattern.** Each agent writes its own output file; orchestrator merges. See `/research` SKILL.md for merge protocol.
5. **Synthesis context overflow**: Manual batched synthesis needed (context too large).
6. **Edit tool + JSON**: Large JSON edits often fail. Include more surrounding context.
7. **Insights guardrail**: Insights are NEVER deleted — only updated or new ones added.
8. **Stratigraphic principle**: New specimen layers prepended to `layers[0]`, old layers never modified.
9. **YouTube transcripts require manual extraction.** Flag as `manual-required` and queue for user.
10. **Sibling tool call errors in agents**: When one parallel WebFetch fails (403), sibling calls may also error. Agents recover by retrying individually. Known pattern, not a bug.
