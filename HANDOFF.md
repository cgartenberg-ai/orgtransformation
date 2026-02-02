# Session Handoff — February 2, 2026

**Project:** Ambidexterity Field Guide (`/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/`)

---

## CRITICAL: Read This First

All work from the Feb 2 session is **committed** (`3701460` — 17 files). The first action should be:

1. `cd site && npm run build` — verify build passes
2. `node scripts/validate-workflow.js` — should be 0 errors, ~60 warnings
3. Ask the user what to work on next

---

## What Happened Since Last Commit

### Last Commits
- `3701460` — Curation + synthesis: Stagwell specimen, 2 mechanism promotions, handoff updates
- `2dce5bd` — Fix: add taxonomy audit entries to synthesis queue
- `81b4bb0` — Taxonomy audit: reclassify 4 specimens, add curation guardrails, AI-native tagging

### Uncommitted Work (13 files)

**Phase 2 — Curation** (processed research session 002):
| File | Change |
|------|--------|
| `specimens/ubs.json` | Source enrichment: 2 new sources, CAIO evolution detail |
| `specimens/commonwealth-bank.json` | Source enrichment: Capital Brief source, boomerang hire detail |
| `specimens/amazon.json` | Division-level detail layer, 3 international press sources |
| `specimens/stagwell.json` | **NEW** — M2 Structural, first ad holding company CAIO (Stagwell) |
| `specimens/registry.json` | totalSpecimens 84→85, updated model/orientation counts |
| `research/queue.json` | Last entry marked "curated" |
| `research/sessions/2026-02-01-002-research-tier1-press-broad-scan.md` | Marked curated |
| `curation/sessions/2026-02-02-curation.md` | **NEW** — Curation session log |

**Phase 3 — Synthesis** (processed 18 pending specimens):
| File | Change |
|------|--------|
| `synthesis/mechanisms.json` | Added Stagwell to M#9; promoted 2 candidates → confirmed #11 + #12 |
| `synthesis/tensions.json` | Added Stagwell to all 5 tensions |
| `synthesis/contingencies.json` | Added Stagwell to all 5 contingency buckets |
| `curation/synthesis-queue.json` | All 110 entries marked synthesized, 0 pending |
| `synthesis/sessions/2026-02-02-synthesis.md` | **NEW** — Synthesis session log |

**Handoff docs** (also uncommitted):
| File | Change |
|------|--------|
| `Ambidexterity_Field_Guide_Spec.md` | Updated to v1.2 (specimens, mechanisms, examples, current state) |
| `APP_STATE.md` | Updated counts, session log, pipeline status |
| `HANDOFF.md` | Rewritten for Feb 2 session continuity |
| `HANDOFF_UI_SPRINT.md` | Marked as archived/completed |

---

## Current State of the Herbarium

### Key Numbers
- **85 specimens** total
- **12 confirmed mechanisms** + 5 candidates
- **5 tensions**, **5 contingencies**
- **0 pending** in any queue (research → curation → synthesis all clear)
- **41 sources** tracked (18 Tier 1, 23 Tier 2)
- **0 errors**, 60 warnings in validator

### Specimen Distribution
| Model | Count | Type Specimen |
|-------|-------|---------------|
| M1: Research Lab | 9 | Google DeepMind |
| M2: Center of Excellence | 17 | — |
| M3: Embedded Teams | 10 | — |
| M4: Hub-and-Spoke | 24 | Novo Nordisk |
| M5: Product/Venture Lab | 12 | Google X (5b), Samsung C-Lab (5a) |
| M6: Unnamed/Informal | 13 | P&G, Bank of America |
| M7: Tiger Teams | 0 | — |
| M8: Skunkworks (Emerging) | 0 | — |

**Orientations**: 60 Structural, 24 Contextual, 1 Temporal
**AI-native**: 10 tagged specimens

### Recently Promoted Mechanisms (2026-02-02)
- **#11 "AI-Driven Workforce Restructuring as Structural Lever"** — 8 specimens (Amazon, Salesforce, Klarna, Citigroup, Pinterest, Dow, UPS, Microsoft). Management delayering is the leading edge.
- **#12 "Business Leader as AI Chief"** — 3 specimens (Wells Fargo, Coca-Cola, PwC). Business-line leaders heading AI ensures strategy serves transformation.

---

## Site Prototype Status

Working Next.js 14 prototype with 12 routes + 1 API endpoint. All Phases 1-3 of UI Spec implemented.

### Key Technical Details
- **Env var**: Claude chat uses `SITE_ANTHROPIC_API_KEY` (not `ANTHROPIC_API_KEY` — Claude Code CLI overrides it)
- **Data source**: JSON files in `../specimens/` and `../synthesis/` read at build time via Node fs
- **Build**: `cd site && npm run build` — should produce ~107 static pages
- **Dev**: `cd site && npx next dev --port 3000`
- **Terminology**: Display text says "Principles" but route is still `/mechanisms/`

### Routes
| Route | Purpose |
|-------|---------|
| `/` | Home (5-section full-bleed layout) |
| `/specimens` | Filterable browser with model descriptions |
| `/specimens/[id]` | 5-tab detail (Overview, Principles, Evolution, Sources, Related) |
| `/taxonomy` | Interactive 7x3 matrix with clickable tags |
| `/taxonomy/model/[id]` | Model detail page with specimens |
| `/taxonomy/orientation/[id]` | Orientation detail page with specimens |
| `/mechanisms` | Confirmed + candidate mechanisms list |
| `/mechanisms/[id]` | Individual mechanism with linked specimens |
| `/tensions` | D3 force-directed tension map |
| `/matcher` | Tabbed: Chat Advisor (Claude API) + Quick Match (dimensions) |
| `/compare` | Side-by-side up to 4 specimens |
| `/about` | Methodology, taxonomy reference |
| `/api/chat` | Streaming Claude API endpoint |

---

## What Needs Doing Next

### Immediate (this session)
1. Verify build + validate
2. Ask user for direction

### Research Backlog
- **Deep-scan backlog**: 4 HIGH, 5 MEDIUM priority podcast episodes
- **Low-confidence queue**: roche-genentech (M3, Low), lg-electronics (M2)
- **Tier 2 sources**: Many not yet scanned

### Data Gaps
- 169 sources with null URLs (legacy data)
- 55 legacy cases in `library/cases/` not yet converted
- M7 has 0 specimens (may need a real tiger team example)

### Site Features Not Built
- **Phase 4**: Auth, My Herbarium, bookmarks, export tools
- **Phase 5**: Research dashboard, trigger cycles from UI, What's New feed
- **Phase 6**: Deployment (Vercel), performance, accessibility, dark mode, mobile polish

---

## Key Documents

| Document | Purpose | Currency |
|----------|---------|----------|
| `CLAUDE.md` | Auto-read session bootstrap | Current |
| `APP_STATE.md` | Full project state + session log | Updated 2026-02-02 |
| `Ambidexterity_Field_Guide_Spec.md` | Product spec v1.2 | Updated 2026-02-02 |
| `SW_ARCHITECTURE.md` | Site software architecture | Current (2026-02-01) |
| `UI_Spec.md` | UI/UX design spec | Current |
| `HANDOFF_UI_SPRINT.md` | UI sprint spec (ARCHIVED) | Complete |

---

## Implicit Knowledge

1. **Edit tool + JSON**: Large JSON edits often fail with "String to replace not found" due to whitespace mismatches. Use Python scripts for complex JSON modifications or read exact lines before editing.
2. **Layer classification is polymorphic**: `classification` in layer data can be string or object — EvolutionTimeline.tsx handles both via `formatClassification()`.
3. **Home page breaks out of layout**: Uses negative margins to achieve full-bleed sections.
4. **FieldObservation randomization**: Must use `useEffect` (not `useState` initializer) to avoid hydration mismatch.
5. **Candidate promotion threshold**: 3+ specimens with evidence required.
6. **Stratigraphic principle**: New layers prepended to `layers[0]`, old layers never modified.

---

## User Preferences
- Visually compelling, "fun and pretty and botanistical" — not flat/corporate
- Rich visual design with depth (shadows, gradients, dark/light alternation)
- Quick iteration style — "make it then let me see it"
- Uses "species" for models, "specimens" for organizations
- Final terminology: "Principles" (was Mechanisms → Patterns → Principles)
- Communication: Brief, direct, visual-first. Will say "it's hideous" if it's ugly.
