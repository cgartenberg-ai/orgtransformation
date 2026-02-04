# Handoff Document: Ambidexterity Field Guide

## Updated: January 31, 2026

---

## Project Summary

A **research-backed field guide** documenting how organizations structurally enable both AI exploration and operational execution. Uses a botanist-inspired approach: observe, document, classify, let patterns emerge. No prescriptions.

**Central question:** How do organizations structurally enable both exploration and execution in the AI era?

**Core metaphor:** Organizational herbarium — specimens collected from the field, classified by taxonomy, synthesized into patterns.

---

## Current State

### What's Operational

The three-phase workflow is running:

| Phase | Skill | Status | Key Files |
|-------|-------|--------|-----------|
| **1. Research** | `/research` | 9 sessions completed | `research/sessions/`, `research/queue.json` |
| **2. Curation** | `/curate` | 3 sessions completed | `curation/sessions/`, `curation/synthesis-queue.json` |
| **3. Synthesis** | `/synthesize` | 1 session completed | `synthesis/mechanisms.json`, `tensions.json`, `contingencies.json` |

### Collection Size

| Asset | Count | Location |
|-------|-------|----------|
| Structured specimens | 65 | `specimens/*.json` |
| Source registry | 38 sources (18 Tier 1, 20 Tier 2) | `specimens/source-registry.json` |
| Confirmed mechanisms | 10 + 5 candidates | `synthesis/mechanisms.json` |
| Core tensions | 5 | `synthesis/tensions.json` |
| Key contingencies | 5 | `synthesis/contingencies.json` |
| Type specimens | 5 (Eli Lilly, Google X, P&G, BofA, Samsung C-Lab) | `specimens/registry.json` |

### Specimen Distribution

| Structural Model | Count |
|-----------------|-------|
| Model 1: Research Lab | 9 |
| Model 2: Center of Excellence | 10 |
| Model 3: Embedded Teams | 9 |
| Model 4: Hub-and-Spoke | 21 |
| Model 5: Product/Venture Lab | 8 |
| Model 6: Unnamed/Informal | 7 |
| Model 7: Tiger Teams | 1 |

Orientation: 44 Structural, 19 Contextual, 2 Temporal.

### Validation

`node scripts/validate-workflow.js` — 0 errors, ~67 warnings (mostly null URLs from legacy specimen data).

---

## Pipeline Status

### Research Queue (Phase 1 → Phase 2)

5 sessions pending curation:

| Session | Orgs Found | Status |
|---------|-----------|--------|
| `bulk-review-batch3.md` | 11 (McKinsey, Moderna, Pfizer, Sanofi, etc.) | pending |
| `bulk-review-batch4.md` | 10 (Schneider, Shopify, Siemens, Walmart, etc.) | pending |
| `gap-coverage-session.md` | 11 (Amazon, Coca-Cola, Infosys, etc.) | pending |
| `deep-scan-session.md` | 5 (Microsoft, SSI, Google, Sierra AI, Citigroup) | pending |
| *(plus any sessions from currently running agents)* | | |

### Synthesis Queue (Phase 2 → Phase 3)

31 specimens pending synthesis (out of 53 total in queue). 22 already synthesized.

### Deep-Scan Backlog (Triaged but not transcript-scanned)

**HIGH priority:**
- Acquired: Alphabet Inc (Aug 26, 2025) — Google corporate structure
- Dwarkesh: Andrej Karpathy (Oct 17, 2025)

**MEDIUM priority:**
- Acquired: Coca-Cola (Nov 23), Jamie Dimon (Jul 16), Tobi Lutke/Shopify (Sep 18)
- BG2 Pod: Satya Nadella + Sam Altman Halloween ep, Kevin Weil (OpenAI CPO), Michael Dell
- Cheeky Pint: Greg Brockman, Des Traynor, Kyle Vogt (on hiatus — episodes exist)

### Source Coverage Gaps

**Never scanned — Tier 1 (7 sources):**
- The Pragmatic Engineer (Substack)
- LinkedIn Economic Graph (Platform)
- Wall Street Journal (Press)
- Financial Times (Press)
- Reuters Business/Tech (Press)
- Bloomberg Technology (Press)
- The Information (Press)

**Never scanned — Tier 2 (20 sources):**
- 5 podcasts (Conversations with Tyler, Invest Like the Best, Cognitive Revolution, All-In, Lex Fridman)
- 3 substacks (Lenny's Newsletter, Elad Gil, Platformer)
- 4 reports (BCG AI Radar, OpenAI Enterprise, Deloitte Tech Trends, State of AI Report)
- 4 press (CNBC, Fortune, Wired, MIT Tech Review, The Decoder, HBR)
- 2 filings (SEC EDGAR, Earnings Call Transcripts)

---

## What Remains to Build

### 1. Reference Site (Not Started)

Full UI specification exists in `UI_Spec.md`. Core screens designed:
- Situation Matcher (killer feature — input contingencies, find peer orgs)
- Taxonomy Browser (interactive 7x3 matrix)
- Specimen Detail (tabbed view with evolution timeline)
- Tension Map (D3 force simulation)
- Comparison View (side-by-side up to 4 specimens)

Recommended stack: Next.js 14, Tailwind + shadcn/ui, Framer Motion, D3.js, Supabase.

### 2. Source URL Backfill

171 sources across specimens have null URLs (legacy data from original case conversion). Need to find and add original source URLs. Can be done incrementally during curation sessions.

### 3. Legacy Case Conversion

55 old-format files remain in `library/cases/`. Batch conversion script exists (`scripts/convert-cases.js`). Most high-value cases already converted; remaining are lower-priority duplicates or thin cases.

---

## Key Files

```
orgtransformation/
├── Ambidexterity_Field_Guide_Spec.md    # Main spec (v1.1)
├── UI_Spec.md                            # UI/UX specification
├── HANDOFF.md                            # This document
├── sources.md                            # Research source guide + refresh protocol
│
├── specimens/
│   ├── *.json (65 specimen files)        # The herbarium
│   ├── registry.json                     # Specimen registry
│   ├── source-registry.json              # Source tracking
│   ├── _template.json                    # Specimen template
│   └── specimen-schema.json              # JSON schema
│
├── research/
│   ├── SESSION-PROTOCOL.md               # Phase 1 protocol
│   ├── SESSION-LOG.md                    # Running session summary
│   ├── queue.json                        # Research → curation queue
│   └── sessions/                         # 9 session files
│
├── curation/
│   ├── CURATION-PROTOCOL.md              # Phase 2 protocol
│   ├── synthesis-queue.json              # Curation → synthesis queue
│   └── sessions/                         # 3 curation sessions
│
├── synthesis/
│   ├── SYNTHESIS-PROTOCOL.md             # Phase 3 protocol
│   ├── mechanisms.json                   # 10 confirmed + 5 candidate
│   ├── tensions.json                     # 5 core tensions
│   ├── contingencies.json                # 5 key contingencies
│   └── sessions/                         # 1 synthesis session
│
├── scripts/
│   ├── validate-workflow.js              # Consistency checker
│   └── convert-cases.js                  # Legacy case converter
│
├── .claude/skills/
│   ├── research/SKILL.md                 # /research
│   ├── curate/SKILL.md                   # /curate
│   └── synthesize/SKILL.md               # /synthesize
│
├── library/cases/                        # 55 legacy JSON files (old format)
├── library/designPrinciples/             # 20 design principles (mapped to mechanisms)
├── background/                           # AI_Organizational_Models_Complete.docx
└── research papers/ambidexterity/        # Academic foundation
```

---

## Recommended Next Steps

### Priority 1: Complete the Pipeline Backlog

The pipeline has accumulated work across all three phases:

**a) Run `/curate` on pending research sessions (5 sessions, ~37 orgs)**
- This will create/update specimens from gap-coverage, deep-scan, and bulk-review batch 3-4 findings
- Expect 15-20 new specimens plus updates to existing ones (Microsoft, Google, etc.)

**b) Run `/synthesize` on pending specimens (31 specimens)**
- This will update mechanisms, tensions, and contingencies with evidence from new specimens
- May surface new candidate mechanisms from the richer data (SSI pure research model, financial services wave, Google 25-year structural arc)

### Priority 2: Scan New Tier 1 Sources

The 7 newly added Tier 1 press sources have never been scanned:
- **The Pragmatic Engineer** — Engineering org restructuring, AI tooling impact
- **LinkedIn Economic Graph** — CAIO appointments, AI role growth data
- **WSJ / FT / Reuters / Bloomberg / The Information** — Major reorg announcements, insider lab dynamics

These are keyword-searchable archives. A single `/research` session with targeted queries ("chief AI officer," "AI restructuring," "AI center of excellence") across these sources should yield high-value specimens, particularly for:
- Fortune 500 CAIO appointments not yet captured
- European/global AI org moves (FT strength)
- AI lab internal dynamics (The Information strength)

### Priority 3: Deep-Scan Remaining High-Priority Episodes

2 HIGH + 8 MEDIUM episodes remain in the podcast deep-scan backlog. Most valuable:
- **Acquired: Alphabet Inc** — Google corporate structure deep-dive, complements the "Google: The AI Company" scan already done
- **Dwarkesh: Karpathy** — AI engineer workflow, likely rich on how AI changes individual-level work structure

### Priority 4: Source URL Backfill

171 sources across specimens have null URLs. This is the main source of validation warnings. Can be addressed:
- Incrementally during curation (each `/curate` session can fix URLs for specimens being touched)
- As a dedicated cleanup session targeting the highest-confidence specimens first

### Priority 5: Begin Reference Site Build

The research pipeline is producing structured data. The UI spec is designed. Starting the Next.js site would:
- Make specimens browsable (currently only JSON files)
- Enable the Situation Matcher (the killer feature)
- Create a public artifact from the research

**Suggested Phase 1 build:** Static specimen pages + taxonomy browser. No user auth, no Supabase, just SSG from the JSON files. Get something visible before adding interactivity.

### Priority 6: Tier 2 Source Triage

5 Tier 2 podcasts have never been scanned. A triage session would:
- Scan episode lists for each
- Identify HIGH-priority episodes for deep-scan
- Decide if any should be promoted to Tier 1 based on relevance

---

## Design Decisions (Settled)

| Decision | Resolution |
|----------|-----------|
| Specimen data format | Single JSON file per specimen with embedded layers |
| Taxonomy scope | All 3 orientations (Structural, Contextual, Temporal) |
| History model | Stratigraphy — layers never overwritten, only added |
| Source provenance | Two timestamps: Source Date + Collected Date; URL required |
| Classification confidence | High / Medium / Low with rationale |
| "Execution" not "Exploitation" | Clearer for practitioners |
| Model 7: Tiger Teams added | Samsung C-Lab as type specimen |
| 3 orientations (not 5) | Simplified from original draft |
| Botanist not Consultant | Observe and classify, don't prescribe |

---

*End of Handoff Document*
