# Handoff Archive

Historical context from Sessions 11-37 (February 9-15, 2026). Read only when you need deep background on a specific topic. For current state, see `HANDOFF.md` and `APP_STATE.md`.

This file grows monotonically — new sessions are appended at the top, nothing is deleted.

---

## Session 36 (continued as Session 37) — February 15, 2026

### Framework-Aware Pipeline Integration

**Verified Session 36 build**: `npm run build` (285 pages, 0 errors), `validate-workflow.js` (0 errors, 157 warnings).

**Updated all 4 pipeline stages** to inject the analytical framework (5 primitives P1-P5, 10 findings F1-F10):
- **Research** (`overnight-research.py`, `research/SKILL.md`, `SESSION-PROTOCOL.md`): P1-P5 primitive antenna + T1-T5 named in relevance test
- **Curation** (`overnight-curate.py`, `CURATION-PROTOCOL.md`): `primitiveIndicators` (P1-P5 object) + `findingRelevance` (supports/challenges direction) + anti-bias guardrail
- **Synthesis** (`SYNTHESIS-PROTOCOL.md`, `synthesize/SKILL.md`): New Step 5d Findings Review, primitive lens in field notes, findings.json in session wrap-up
- **Purpose Claims** (`overnight-purpose-claims.py`, `purpose-claims/SKILL.md`): P3/P4 analytical context + `primitiveRelevance` in enrichment

**Key design principle** (user directive): "Evidence that contradicts or falls outside the framework receives the SAME analytical weight as confirming evidence." Anti-confirmation-bias guardrail embedded at every stage. Gradient: Research (antenna) → Curation (structured tagging) → Synthesis (full lens) → Purpose Claims (light context).

**Documentation updated**: APP_STATE.md (orchestrator + framework-aware pipeline), CLAUDE.md (project structure, quick commands, synthesis directory), WORKFLOW.md (framework-aware note + primitives/findings reference tables), scripts/README.md (framework-aware note), SW_ARCHITECTURE.md (new types/routes/data access), Ambidexterity_Field_Guide_Spec.md (analytical framework section).

---

## Session 36 — February 15, 2026 (Afternoon)

### Synthesis Patch + Nightly Pipeline Build

**Phase A: Synthesis Patch**
- Applied 111 changes from 7-batch autonomous synthesis run (62 specimens analyzed)
- Created `scripts/patch-synthesis-feb15.py` with 4 phases: score revisions, new placements, contingency additions, mechanism links + insights
- Fixed 3 dry-run issues: amazon-agi T3, coca-cola T1 (moved to NEW_PLACEMENTS), wells-fargo T2/T5 (corrected old values)
- Validator: 0 errors, 157 warnings post-patch

**Phase B: Nightly Pipeline Implementation (10 tasks)**
1. Created `scripts/pipeline-schedule.json` — 7-day themed rotation config
2. Added `--schedule-theme` flag with 14 theme modes to `overnight-research.py`
3. Created `scripts/overnight-pipeline.py` — 6-phase orchestrator with time budgeting
4. Created `scripts/overnight-synthesis.py` — autonomous synthesis engine
5. Created `pipeline-reports/` directory + `.gitignore`
6. Created `scripts/com.fieldguide.overnight-pipeline.plist` — launchd for 7 PM daily
7. Integration tests: 14/14 themes pass, 7/7 pipeline days pass
8. Updated `scripts/README.md` and `WORKFLOW.md`
9. **Live end-to-end test**: `press-keyword` with limit 1 → CAIO-appointments agent completed in 345s, produced 15 findings (9.9 KB output)

**Bugs fixed during implementation:**
- `scannedThroughDate` None causing TypeError in sort
- substacks sort with None values
- `target-specimens` dry-run accessing `t['mode']` on standard targets
- `byModel` values were int counts not lists in taxonomy gaps
- Status field "Active" vs "active" case sensitivity

---

## Sessions 34-35 (Feb 15): Research Agents + Full Curation (10 sessions, 8 new specimens)

### Session 34: Research Agent Batch
- **4 Opus research agents launched in parallel** covering Q4 2025 earnings + Feb 12-15 press/podcast sweep
- **105+ findings, 16 broader trends, 23 purpose claims** across ~20 organizations
- All 4 agent outputs merged into `research/queue.json`, `source-registry.json`, `field-signals.json`

### Session 35: Full Curation
- **10 pending research sessions curated** — the largest single curation session
- **8 new specimens created**: baker-mckenzie, arm-holdings, forrester, capgemini, fda-hhs, columbia-group, liverpool-city-region, verses-ai
- **17 existing specimens updated** with new layers (13 earnings enrichments + 4 press sweep updates)
- **Registry: 159 active specimens** (164 total including 5 inactive), up from 151
- Sessions 2-6 (deep scans) discovered to be already incorporated through overnight curation — queue entries closed
- Duplicate source IDs in disney and intel fixed (batch script artifact)
- Null-URL sources properly tagged across 8 specimens
- Validator: **0 errors, 157 warnings** (all pre-existing)

---

## Session 33 (Feb 15): Palantir Reclassification + Enrichment Merges + Research Attempt

**Pre-compaction synthesis work:**
- **Palantir reclassified M9→M6b** — AI-native prestige trap. Founded 2003 for data integration, not AI. AIP launched 2023 as GenAI response. Guardrail 5 hardened.
- **11 enrichment merges** from overnight curation (palantir, asml, astrazeneca, rivian, comcast/nbcuniversal, spotify, stripe, nextera-energy + others)
- **8 new specimens placed** into tensions/contingencies/mechanisms
- **Purpose claims background run** launched and completed

**Post-compaction:**
- Attempted online research run for Q4 2025 earnings calls + substacks
- Ad-hoc web searches gathered partial findings (Alphabet, Microsoft, Meta, Amazon, Forrester, Disney, Intel, Cognizant) — **NOT persisted to any file**
- User corrected: not following `/research` protocol. Skill invoked but context window too full to continue.
- Session ended due to context exhaustion.

---

## Session 32 (Feb 14): Pipeline Technical Debt Audit — 15 Fixes

Thorough technical debt audit of Track 1 and Track 2 pipelines via 4 deep-audit agents (code robustness, data pipeline, process gaps, documentation). All 15 identified issues fixed.

- **A1**: Designed Track 2 collect/enrich split architecture (documented in WORKFLOW.md, v2 future)
- **A2**: Added content-based dedup to overnight-purpose-claims.py merge logic (fingerprint: specimenId + text[:100] + speaker)
- **A3**: Standardized quality thresholds to 4-level scale (rich=5+, adequate=2-4, thin=1, none=0) in SKILL.md
- **A4**: Added enrichment schema validation to validate-workflow.js (Section 15)
- **A5**: Added `--rescan-stale` flag and `rescanReason` support to overnight-purpose-claims.py
- **B1**: Documented two curate input formats in WORKFLOW.md (multi-company session vs single-company JSON)
- **B2**: Clarified synthesis-queue.json description (interactive tracking, not automated)
- **B3**: Wired field-signals.json into synthesize SKILL.md and SYNTHESIS-PROTOCOL.md
- **B5**: Documented overnight scripts scope limitations in WORKFLOW.md (source-registry updates are by-design interactive)
- **C2**: Added rebuild-registry.js call after overnight-curate.py successful curation
- **C4**: Added purpose-claims-to-specimens consistency check (Section 12b in validator)
- **C5**: Added C6 environmentalAiPull to overnight-curate.py CONTINGENCIES_REF
- **D1**: Defined 7-stage specimen lifecycle gates in WORKFLOW.md
- **D2**: Updated specimen-schema.json (M8/M9, C6, Inactive, mechanism max 15)
- **D3**: Standardized session naming across tracks in WORKFLOW.md

Validator: 0 errors, 135 warnings (pre-existing enrichment data quality). Both Python scripts parse clean.

---

## Sessions 29-30 (Feb 14): Comprehensive 6-Phase Infrastructure Refactoring

**Comprehensive 6-phase refactoring** — eliminated all technical debt identified in 6 deep audits. 18 git commits, 0 breakage throughout.

- **Phase 1: Crash-Safe Infrastructure** — Created `scripts/lib/utils.py` (atomic writes, PID-based locks, preflight checks, changelog). Wired safety primitives into all 3 overnight scripts (10 `json.dump()` → `save_json()`). Fixed pending→processed ordering in purpose-claims.
- **Phase 2: Data Quality** — Cleaned contingencies.json duplicates, marked 5 gov specimens Inactive, tagged 172 null-URL sources, backfilled `discoveredIn` for 20 insights.
- **Phase 3: Validation Infrastructure** — Extended validator 11→16 sections. Created `specimen-lifecycle-status.js` and `check-source-freshness.js`.
- **Phase 4: Type Alignment** — Fixed ContingencyDefinition types, added C6 + "Inactive" to types, added try-catch to synthesis data loaders.
- **Phase 5: Organizational Cleanup** — Archived 43 one-off scripts, moved stale docs, created scripts/README.md.
- **Phase 6: Documentation** — Updated CLAUDE.md, WORKFLOW.md, APP_STATE.md.

Validator: 0 errors, 27 warnings. Site: 258 pages. Zero breakage throughout.

## Session 31 (Feb 14): Audit Remediation — Phases 3-5

Continuation session completing the remediation plan from 4 deep audit agents (code robustness, data pipeline, process gaps, documentation).

- **Phase 3 (Validation Enhancements)**: Fixed 2 "unknown" specimenId entries in mechanisms.json (both netflix). Fixed orphan queue entry path. Added ID/filename mismatch check + schema validation to validate-workflow.js (sections 17-18). Added graceful degradation to specimen detail page (catch handlers for purpose claims + enrichment, null-safe property access in findRelated).
- **Phase 4 (Documentation Refresh)**: Updated 8 stale documentation files — SW_ARCHITECTURE.md (major rewrite: added purpose-claims subsystem, field-journal, SpiderChart, CitedText, buildSystemPrompt; fixed model range 1-9, matrix 9x3, 6 contingencies), APP_STATE.md (~11 count/path fixes), WORKFLOW.md (C6, stale counts), CLAUDE.md (v1.4, missing skills), Ambidexterity_Field_Guide_Spec.md (C6, 9 models), CURATION-PROTOCOL.md (C6), .claude/skills/research/SKILL.md (claim taxonomy v2.0).
- **Phase 5 (Data Cleanup)**: Merged hp/hp-inc duplicate (migrated 5 purpose claims, removed duplicate tension placement, deleted hp.json, rebuilt registry 149→148). Moved 2 orphan enrichment supplement files to `enrichment/supplements/`. Confirmed meta-reality-labs correctly tagged Deprecated.
- **Final state**: 0 errors, 27 warnings. Site builds clean. 3 commits: `d28b8bd` (Phase 3), `0c112aa` (Phase 4), `a46f34c` (Phase 5).

---

## Session 27 (Feb 13): Session 24 Claims + Healthcare Merge + Synthesis

**What happened:**
1. **Session 24 purpose claims extracted** (+31): xAI 9 (new), Intuit 9 (new), Klarna +4 (reversal arc), Salesforce +5 (Benioff displacement), Dow +1, Anthropic +2 (Krieger downward move), Pinterest +1.
2. **Healthcare purpose claims merged** (+48): Cedars-Sinai 16, Mayo Clinic 18, Mount Sinai 14. All from dedicated Opus agents.
3. **Registry: 1,384 claims** across ~72 scanned specimens. **Total insights: 65**.
4. **New insight**: `mission-identity-anodyne-rhetoric` — strong institutional missions produce identity-confirming, rhetorically flat purpose claims. Open question: authentic internalization vs. formulaic messaging.
5. **Synthesis updated**: Mechanisms +6 evidence entries, Tensions +4, Contingencies +3 (healthcare labor deficit evidence).
6. **Key botanist findings**: Klarna reversal = measurement-driven moral hazard smoking gun; Krieger stepping DOWN from CPO = structurally unique; healthcare survival claims grounded in demography not competition.

## Session 26 (Feb 13): Batches 13-14 Purpose Claims + Botanical Analysis

1. **Batches 13-14 merged**: 109 claims across 8 specimens (visa, honda, panasonic, lionsgate, cognizant, hp-inc, lowes, cvs-health).
2. **Botanical analysis**: 5 existing insights updated with new evidence, 3 new insights added. **Total insights: 64** (12 purpose-claims).
3. New insights: `heritage-as-authorization` (Japanese founder mythology), `audience-dependent-claim-ordering` (stakeholder-segmented rhetoric), `ceo-departure-natural-experiment` (HP Inc Lores departure).

## Session 25 (Feb 13): Batch Curation + Botanist Discussion — 3 First-Order Insights

1. **Curated 15 specimens** from Session 24's 7 agent outputs: 2 new (Intuit, xAI), 2 major updates (Salesforce, Klarna), 11 incremental updates. Registry: 149 specimens.
2. **Botanist discussion** on 8 field journal observations → 3 new first-order insights created, 2 existing insights updated. Total insights: 61.

### The 3-Insight Measurement Cluster (Session 25 — FIRST ORDER)

**Biased metrics → bounded-rational escalation → organizational overcorrection → tacit knowledge destruction → irreversible damage**

| Insight | Maturity | Core Claim |
|---------|----------|------------|
| `measurement-driven-moral-hazard` | emerging | AI transition metrics (cost, speed, volume) systematically overstate success because they capture measurable dimensions while missing unmeasurable ones (empathy, trust, institutional knowledge). Holmstrom (1979) multi-task in organizational form. |
| `measurement-inverse-grove-connection` | hypothesis | The measurement bias is the MECHANISM behind inverse-Grove. Headquarters pushes harder because the dashboard says it's working. Not CEO hubris — Simon's bounded rationality on systematically biased information. |
| `tacit-knowledge-destruction-irreversibility` | emerging | AI workforce cuts destroy Polanyi/Nelson-Winter tacit knowledge that cannot be recovered through rehiring. The measurement system can't see this destruction BECAUSE tacit knowledge is by definition unmeasurable. |
| `inverse-grove` (UPDATED) | hypothesis | Klarna evidence upgraded to complete causal chain with CEO admission. Measurement connection added. |
| `two-dimensions-of-tacit-information` (UPDATED) | hypothesis | Klarna added — within-module tacitness (Dimension 2) is what gets destroyed in AI displacement. |

### Botanist Flags Disposition (Session 25)

| # | Flag | Session 25 Outcome |
|---|------|-------------------|
| 14 | Intuit as M4 natural experiment | DONE — Specimen created, dual AI tracks documented |
| 15 | Klarna full reversal arc | DONE — Major update, measurement mechanism captured |
| 16 | Salesforce leadership churn | DONE — Major update with 5 departures, Inzerillo consolidation |
| 17 | xAI co-founder departures | DONE — New specimen, 50% departure rate documented |
| 18 | Exploration→execution transitions | WATCH — May indicate Temporal orientation shifts; Workday execution→exploration is interesting counter-case |
| 19 | Intuit dual AI tracks → two-dimensions | CURATED — Evidence captured in specimen; hypothesis connection noted |
| 20 | Customer Zero at institutional scale | CURATED — In Salesforce update |
| 21 | Measurement-driven moral hazard | ELEVATED — 3 new insights created |

---

## Research Agenda History (Session 15+)

### C. Financial Services Natural Experiment — RESEARCH COMPLETE, ENRICHMENT DONE
**Goldman Sachs vs. Morgan Stanley vs. JPMorgan — same industry, three structural choices.**
- Goldman: CIO-as-AI-leader (M6a/Contextual), no CAIO, AI Champions from business divisions, multi-model vendor strategy, Anthropic embedded engineers
- Morgan Stanley: Dedicated Firmwide AI Head (McMillan) reporting to co-presidents (M4/Structural), 98% advisor adoption, deep single-vendor OpenAI, division-specific AI products
- JPMorgan: UNIQUE dual-track — Heitsenrether (CDAO, applied, Operating Committee) + Veloso (AI Research, academic). Dimon: "We took AI and data out of technology. It's too important."
- **All 3 specimens enriched** with new layers, sources, quotes. Research output: `research/pending/finserv-natural-experiment.json`
- **8 comparative observations** documented including: three-way structural divergence, all chose non-technologist AI leaders, vendor strategy reveals organizational philosophy, JPMorgan only firm to separate AI from technology org

### B. Healthcare Sector Deep Dive — RESEARCH + ENRICHMENT COMPLETE
**Research agent completed with 308-line output: `research/pending/healthcare-sector-deep-dive.json`**
- All 5 existing healthcare specimens enriched via `scripts/enrich-healthcare-deep-dive.py`
- 6 new specimen candidates identified: Cedars-Sinai (HIGH), MGB (HIGH), Kaiser (HIGH), Cleveland Clinic (MEDIUM), Hackensack Meridian (MEDIUM), UC Davis Health (LOW)
- 3 HIGH-priority specimens created (Session 16c): Cedars-Sinai (M4+M1), Mass General Brigham (M4+M5), Kaiser Permanente (M4, Low confidence)

### D. Fresh Podcast/Substack/Conference Sweep — COMPLETE
**Sweep completed Feb 10: 14 searches, 7 URL fetches. Output: `research/pending/podcast-conference-sweep-feb-10.json`**
- HIGH-priority findings: McKinsey 60K "employees" (40K humans + 25K AI agents), Dwarkesh-Musk xAI, Mollick "Management as AI Superpower," SaaStr agent ratios
- 7 new field signals added (total: 37)

### A. Enrich Thin Specimens — PARTIALLY COMPLETE
- 6 of thinnest specimens enriched in Session 16: Thomson Reuters (M6a→M4+M5), CrowdStrike (null→M3), Recruit Holdings (M6→M3), HP Inc (M6→M4+M5), Panasonic (M2→M4+M5), Kyndryl (M2 confirmed)
- Still thin: Chegg (stub), T-Mobile and Uber could use more depth
- Key finding: Workforce-reduction-only sources systematically misclassify as M6

---

## Synthesis Placement — All Batches 1-9 COMPLETE

**110+ specimens placed across T1-T5 and C1-C6.** Completed in Sessions 11-14 + 18-20.

### Key Decision: Synthesis Must Be Interactive
**Automated synthesis (`/synthesize`, `overnight-synthesis.py`) is deprecated.** See WORKFLOW.md Phase 3 for the interactive protocol.

### Batch 1: JPMorgan (1 specimen)
- Proof-of-workflow: patched T4 + C2/C3/C4/C5

### Batch 2: Banking + Pharma (8 specimens)
- bank-of-america, wells-fargo, ubs, eli-lilly, moderna, novo-nordisk, pfizer, roche-genentech
- Re-examination yielded: Lilly optimal hub size, Moderna 100% adoption speed, Pfizer explicit M4, Novo messaging strategy

### Modularity Hypothesis (emerged from Batch 2 re-examination)
- **Insight**: `modularity-predicts-ai-structure` — Work modularity and tacit knowledge intensity at inter-component interfaces predict both the speed of AI adoption and the structural model chosen
- **Theoretical chain**: Conway (1967) → Colfer & Baldwin (2016) → Simon (1962) → Garicano (2000) → Gibbons & Henderson (2012) → Henderson & Clark (1990) → Nadella's explicit Coase reference
- **2x2 framework**: Modular/Integral work × Explicit/Tacit interfaces → predicts M6a, M3/M4, M1, M3 respectively

### Batch 3: Healthcare + IT Services (6 specimens)
- UnitedHealth "scale without signal," IT services divergence, Moderna HR-Tech merger

### Batch 4: Automotive/Industrial (13 specimens)
- Automotive M4 Convergence (10/13), GM CAIO failure natural experiment, "Data Foundation First" sequencing, Physical AI as distinct category

### Batch 5: Defense/Transport (5 placed + 4 gov removed)
- Anduril-Lockheed modularity validation, Blue Origin CEO provenance outlier, Delta-FedEx CEO conviction gating

### Batch 6: Media/Consumer (9 specimens)
- Disney vs Netflix modularity→orientation, data-foundation-first extends to retail, M4/Contextual consumer pattern, Nike CTO elimination, **TWO-DIMENSIONS-OF-TACIT-INFORMATION** (major collaborative discovery)

### Batch 7: Mixed (7 specimens, Session 18)
- M4 taxonomy flag, product-production convergence hypothesis, CEO succession signals, sector rhetorical signatures

### Batch 8: Big Tech (7→6, Session 19)
- Expelled exploration, research-output-as-production-tool, tight-coupling-modularity-constraint, meta-exploration-failure→confirmed

### Batch 9: Enterprise Software (6, Session 20)
- **Inverse Grove hypothesis**, AI-infrastructure-vs-actor counter-positioning, dual-tempo AI structures, environmental AI pull (C6)

### Placement Progress Table

| Batch | Specimens | Status | Discoveries |
|-------|-----------|--------|-------------|
| 1 | JPMorgan | DONE | Workflow proof |
| 2 | 8 (banking + pharma) | DONE | Lilly hub size, Moderna adoption speed, Pfizer M4, Novo messaging |
| 3 | 6 (healthcare + IT services) | DONE | UHG scale-without-signal, IT services divergence, Moderna HR-Tech merger |
| 4 | 13 (automotive/industrial) | DONE | Automotive M4 convergence, GM CAIO failure, data-foundation-first, physical AI category |
| 5 | 5 placed, 4 gov removed (defense/transport) | DONE | Anduril-Lockheed modularity validation, Blue Origin CEO provenance outlier, Delta-FedEx CEO conviction gating |
| 6 | 9 (media/consumer) | DONE | Disney-Netflix modularity→orientation, data-foundation extends to retail, M4/Contextual consumer pattern, Nike CTO elimination |
| 7 | 7 (mixed) | DONE | M4 taxonomy flag, product-production convergence hypothesis, CEO succession signals, sector rhetorical signatures (purpose claims) |
| 8 | 7→6 (Big Tech; meta-reality-labs deprecated) | DONE | Expelled exploration, research-output-as-production-tool, tight-coupling-modularity-constraint, meta-exploration-failure→confirmed |
| 9 | 6 (enterprise software) | DONE | **Inverse Grove hypothesis**, AI-infrastructure-vs-actor counter-positioning, dual-tempo AI structures, environmental AI pull (C6) |

### Files Modified in Sessions 11-14

**Synthesis (central):** tensions.json, contingencies.json, insights.json, sessions/2026-02-09-placement-session.md
**Specimens:** jpmorgan, wells-fargo, pfizer, roche-genentech, moderna, novo-nordisk, accenture, cognizant, genpact, sanofi, infosys, tesla, hyundai-robotics, bosch-bcai, dow-chemical, nike
**Scripts:** patch-jpmorgan.py, patch-batch2-6.py
**Documentation:** WORKFLOW.md Phase 3 rewritten, HANDOFF.md, APP_STATE.md, SESSION_LOG.md

---

## Implicit Knowledge (Items 21-68)

Items 1-20 from earlier sessions are referenced but not preserved here. Items below accumulated across Sessions 11-27.

21. **Synthesis is ALWAYS interactive — STOP AND DISCUSS BEFORE WRITING.** Automated `/synthesize` and `overnight-synthesis.py` are deprecated. Every synthesis batch must be treated as a **collaborative analytical session**. The correct workflow is: (1) Read specimens, (2) Present observations/discoveries to the collaborator, (3) **WAIT for back-and-forth discussion** before committing anything to the field journal or insights.json, (4) Only after discussion, write the patch script and update files. **Do NOT skip step 3.** The most valuable insights (mirroring hypothesis, CEO congruence, modularity→orientation) emerged from collaborative discussion, not from unilateral analysis. If you find yourself writing observations directly to the field journal without presenting them for discussion first, you've broken the protocol. Read WORKFLOW.md Phase 3.
22. **Contingencies.json uses plain string IDs** in specimen arrays. Tensions.json uses `{specimenId, position, evidence}` objects. Don't mix formats.
23. **Contingency levels are DIRECT keys** on the contingency object, not nested under a `levels` sub-object. E.g., `contingency.high.specimens`, not `contingency.levels.high.specimens`.
24. **Modularity hypothesis needs pressure-testing** against Batch 5 (defense, integral/high-tacit) and Batch 8 (Big Tech, modular/explicit). These are the critical tests.
25. **GM CAIO failure is a natural experiment.** 8-month tenure, then reorganization under manufacturing. Use as evidence for domain-embedding requirement in M4 industrial hubs.
26. **"Data foundation first" is an industrial sequencing pattern.** ExxonMobil and Honeywell both solved enterprise data infrastructure before scaling AI. Track whether this appears in other legacy sectors.
27. **Tesla's T4 (Named vs. Quiet) is analytically interesting.** Scored +0.5 (quiet) because AI IS the product — there's no separate "AI Center" because Tesla brands itself as AI. This "quiet by integration" pattern is distinct from "quiet by neglect" (Dow, ExxonMobil).
28. **Dow Chemical is a stub.** Only T4 scored; all other tensions skipped for insufficient data. Needs enrichment before further placement.
29. **Two-dimensions-of-tacit-information hypothesis (Session 14).** Two independent dimensions: (1) tacit information at interfaces → predicts org structure choice (Conway/Colfer & Baldwin), (2) tacit information within modules → predicts depth of AI capability penetration (new dimension). Discriminating cases: Netflix (low interface / high within), JPMorgan (high interface / low within).
30. **M4/Contextual is the consumer-sector default.** Nike, PepsiCo, Ulta Beauty, Netflix — hub provides tooling, AI embedded in existing roles.
31. **Data-foundation-first extends beyond heavy industry.** PepsiCo (SAP), Ulta Beauty (Project SOAR), Kroger (84.51°). Broadened to "legacy organizations."
32. **Pending research files in research/pending/.** ~80 files from overnight runs. 10 large research agent outputs, ~70 curation artifacts (mostly merged).
33. **Spider chart normalization uses TARGET_MAX=0.85.** `normalizeDistribution()` in `site/lib/utils/spider-data.ts`.
34. **Citation format: `[source-id]` inline markers.** Parsed by `citations.ts`, rendered by `CitedText.tsx`.
35. **ClaimsHeatmap deprecated but not deleted.** View mode key still `"heatmap"` to avoid URL breakage; label shows "Profiles".
36. **M4 TAXONOMY REVIEW completed (Session 21).** 19 specimens reclassified. M4 66→48. Guardrail 8 added.
37. **Product-production convergence hypothesis (Session 18).** For SaaS/services firms, internal/external boundaries dissolve. Added to insights.json.
38. **Enrichment files at `research/purpose-claims/enrichment/{specimen-id}.json`.** ~108 files. Schema documented in WORKFLOW.md.
39. **Purpose claims sector rhetorical signatures (Session 18).** Finserv = commercial-success only; media = diverse/political; semiconductor = identity-heavy.
40. **Thomson Reuters automated tension scores were wrong.** Corrected in Session 18. Further evidence automated synthesis is unreliable.
41. **Contingencies.json has legacy duplicate keys for talentMarketPosition.** Needs cleanup.
42. **Expelled exploration hypothesis (Session 19).** March (1991) boundary condition: exploration crosses organizational boundaries. AMI Labs is clearest case.
43. **Research-output-as-production-tool is SEPARATE from product-production-convergence (Session 19).** Different organizational layers. User explicitly requested separation.
44. **Tight-coupling-modularity-constraint connects to Podolny & Hansen HBR 2020 (Session 19).** Apple test case.
45. **Industrial CEOs use purpose claims fundamentally differently from tech CEOs (Session 19).** Zero utopian claims across all 53 industrial/automotive claims.
46. **BMW's pure identity authorization is the most distinctive rhetorical profile (Session 19).** Zero survival, zero utopian.
47. **Survival rhetoric inversely correlated with structural exploration investment (Session 19).** Ford vs BMW.
48. **Rhetorical division of labor mirrors M4 structural division (Session 19).** Toyota, Honeywell. Purpose claims as diagnostic tool.
49. **Analytical Depth Requirement in SYNTHESIS-PROTOCOL.md (Session 19).** 5 questions after mechanical scoring.
50. **Inverse Grove hypothesis is potentially paper-worthy (Session 20).** Track original Grove vs. inverse Grove across all specimens.
51. **AI-as-infrastructure vs. AI-as-actor counter-positioning axis (Session 20).** Different failure modes per positioning.
52. **Environmental AI Pull (C6) added to contingencies.json (Session 20).** High/medium/low pull → different Grove risk profiles.
53. **Dual-tempo AI structures (Session 20).** CrowdStrike CTO/CTIO, Uber AI Labs. Works when interface tacitness is high.
54. **Pinterest and Workday are the AI-washing control group (Session 20).** Define zero point on structural response scale.
55. **Purpose claims pending merge status (Session 20).** Now resolved — merged in subsequent sessions.
56. **M4 Guardrail 8 (Session 21).** Bidirectional hub-spoke coordination required. Reclassified 19 specimens.
57. **Citation backfill complete for all High-completeness specimens (Session 21).** 30 specimens with `[source-id]` markers.
58. **4 thin M4 specimens flagged (Session 21).** HP Inc, ABB, Siemens, Coca-Cola need enrichment.
59. **Purpose claims batch 10 merged (Session 21).** Bloomberg, Lockheed Martin, Mercedes-Benz, PepsiCo.
60. **Industry > Structure for Rhetoric (Session 22).** M4 specimens vary dramatically by industry.
61. **Cross-model rhetorical patterns (Session 22).** Explore models show less commercial-success; M9 shows concentrated teleological.
62. **Commercial-moral register convergence (Session 22).** Co-occurrence vs. substitution question.
63. **Batch 12 agent selection rationale (Session 22).** Model diversity testing.
64. **Purpose claims registry growth trajectory.** ~60 claims/batch with 4 specimens. Rich enough for paper-quality analysis.
65. **Measurement-driven moral hazard causal chain (Session 25).** Three connected insights. Klarna traverses complete chain.
66. **Intuit as measurement-problem candidate (Session 25).** Flagged for monitoring.
67. **Session 25 botanist flag dispositions.** Exploration→execution WATCH, management layer + ASML combined, platform governance journal note.
68. **Registry byModel keys use numeric strings (Session 25).** `"4"` not `"M4"`.
