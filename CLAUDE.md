# Ambidexterity Field Guide — Project Instructions

A research-backed field guide documenting how organizations structurally enable both AI exploration and operational execution, using a botanist-inspired observe/classify/synthesize approach.

**Central question:** How do organizations structurally enable both exploration and execution in the AI era?

---

## Required Reading (Every Session)

1. **`APP_STATE.md`** — Read FIRST. Current state of everything: what's built, data counts, pipeline status, session log.
2. **`SW_ARCHITECTURE.md`** — Software architecture for the Next.js site. Read when doing site development.
3. **`Ambidexterity_Field_Guide_Spec.md`** — Product spec: taxonomy (7 models x 3 orientations), specimen cards, mechanisms, tensions, contingencies. Read when doing research/curation/synthesis or when domain context is needed.
4. **`UI_Spec.md`** — UI/UX design spec. Read when building new screens or components.

---

## Project Structure

```
orgtransformation/
├── CLAUDE.md                    # THIS FILE — auto-read at session start
├── APP_STATE.md                 # Current state (updated each session)
├── SW_ARCHITECTURE.md           # Site software architecture
├── Ambidexterity_Field_Guide_Spec.md  # Product spec (v1.1)
├── UI_Spec.md                   # UI/UX design spec
├── site/                        # Next.js 14 prototype (App Router)
│   ├── app/                     # Routes (10 pages)
│   ├── components/              # React components (~25)
│   └── lib/                     # Types, data access, matching algorithm
├── specimens/*.json             # 65 specimen data files (the herbarium)
├── synthesis/                   # mechanisms.json, tensions.json, contingencies.json
├── research/                    # Session logs, queue.json, source-registry
├── curation/                    # Session logs, synthesis-queue.json
├── scripts/                     # validate-workflow.js, convert-cases.js
└── .claude/skills/              # /research, /curate, /synthesize skills
```

---

## Skills

### `/research` — Phase 1: Field Work
Scans sources (podcasts, substacks, press) for organizational AI structure findings. Outputs session files to `research/sessions/` and updates `research/queue.json`. Use when adding new observations from the field.

### `/curate` — Phase 2: Curation
Transforms raw research findings into structured specimen cards using the 7-model taxonomy. Creates/updates `specimens/*.json` and queues specimens for synthesis. Use when processing pending research sessions.

### `/synthesize` — Phase 3: Synthesis
Identifies cross-cutting patterns across specimens — updates mechanisms, tensions, and contingencies with new evidence. Use when newly curated specimens need pattern analysis.

**Note:** Each skill is self-contained and loads its own protocols, schemas, and queues. Do not duplicate skill logic outside the skills.

After running any skill, note changes in APP_STATE.md session log (specimens created/updated, mechanisms changed, etc.).

---

## Site Development

- **Stack:** Next.js 14, Tailwind CSS, shadcn/ui, Framer Motion, D3.js
- **Data:** File-based — reads JSON from `../specimens/` and `../synthesis/` via Node fs
- **Run:** `cd site && npm run dev` (port 3000)
- **Build:** `cd site && npm run build`
- **Architecture:** See `SW_ARCHITECTURE.md` for full details

---

## Session End Protocol

Before ending any session that modified files:

1. **Update `APP_STATE.md`** — Add row to session log table: date + what changed
2. **If specimens changed:** Run `node scripts/validate-workflow.js` from project root
3. **If site code changed:** Run `cd site && npm run build` to verify no breakage

---

## Settled Design Decisions (Do Not Revisit)

| Decision | Resolution |
|----------|-----------|
| Metaphor | Botanist (observe/classify), not consultant (prescribe) |
| Terminology | "Execution" not "Exploitation" |
| History model | Stratigraphy — layers never overwritten, only added |
| Taxonomy | 7 structural models x 3 orientations (Structural, Contextual, Temporal) |
| Source provenance | Required for all facts: URL + source date + collected date |
| Data format | One JSON file per specimen with embedded layers |
| HANDOFF.md | Superseded by this file + APP_STATE.md |
