# Session Handoff — UI Sprint Implementation

**Date:** 2026-02-01
**Project:** Ambidexterity Field Guide (`/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/`)
**Session Focus:** Implemented the full UI sprint: home page redesign, terminology renames, evolution tab reframe, species descriptions, and Claude API conversational matcher.

---

## CRITICAL: Read This First

The site (`site/` directory) is a Next.js 14.2.35 App Router project with Tailwind CSS and a botanical/field-guide metaphor. This session completed **all planned UI sprint changes** plus additional user-requested features. All changes are uncommitted — 20 modified files and 5 new files. The build passes cleanly.

**Immediate next action:** Commit the current changes, then ask the user what they want to work on next. The HANDOFF_UI_SPRINT.md checklist is fully complete.

---

## Where We Left Off

### Completed This Session
- [x] **Step 1: Terminology rename "Mechanisms" → "Patterns"** across 10 files (display text only, routes/types unchanged)
- [x] **Step 2: Home page redesign** — Full-bleed 5-section layout (hero, species cards, type specimens, collection summary, field observation)
- [x] **Step 3: Terminology rename "Patterns" → "Principles"** across 11 files (user changed their mind mid-sprint)
- [x] **Step 4: Evolution tab reframe** — "Stratigraphic layers" → organizational evolution language, "Current" → "Latest", "Layer N" → "Observation N"
- [x] **Step 5: Species descriptions on specimens page** — Added `characteristics` field to all 7 STRUCTURAL_MODELS, fixed URL query param reading (`?model=N`), shows description card when model filter is active
- [x] **Step 6: Claude API conversational matcher** — Streaming chat UI with system prompt built from all specimens/models, tabbed interface (Chat Advisor / Quick Match)
- [x] **Bugfix: Evolution tab crash** — `classification` in layer data can be an object (not string); added `formatClassification()` helper
- [x] **Bugfix: Chat history persistence** — Added sessionStorage to preserve conversation when navigating away and back; includes "Start new conversation" reset link

### Not Started (Potential Future Work)
- [ ] The `app/mechanisms/` route is still named "mechanisms" (only display text changed to "Principles") — could rename route to `/principles/` if desired
- [ ] Markdown rendering in chat could be richer (bold, bullet lists, headers)
- [ ] Chat could open specimen links in new tab or side panel instead of navigating away

---

## Project Overview

### What This Project Is
A Next.js research website that catalogs real organizations' AI structural approaches using a botanical field guide metaphor. Organizations are "specimens," their structural patterns are "species" (7 models like Research Lab, Center of Excellence, etc.), and the site lets users browse, compare, and find matching specimens. The data comes from JSON files in `/specimens/` and `/synthesis/` directories outside the site folder.

### Key Files and Their Purpose

| File | Purpose |
|------|---------|
| `site/app/page.tsx` | Home page — full-bleed 5-section layout with hero, species cards, specimens, stats, field observation |
| `site/app/api/chat/route.ts` | Streaming API route for Claude chat matcher |
| `site/components/matcher/ChatMatcher.tsx` | Chat UI with sessionStorage persistence, streaming, markdown links |
| `site/components/matcher/MatcherTabs.tsx` | Tab toggle between Chat Advisor and Quick Match |
| `site/components/matcher/MatcherForm.tsx` | Original dimension-based matcher (Quick Match tab) |
| `site/lib/matcher/buildSystemPrompt.ts` | Builds ~12KB system prompt with all models + specimen registry for Claude |
| `site/components/home/FieldObservation.tsx` | Random rotating quote from confirmed mechanisms |
| `site/components/specimens/SpecimenBrowser.tsx` | Specimen grid with sidebar filters + species description card |
| `site/components/specimens/EvolutionTab.tsx` | Org evolution intro text + timeline |
| `site/components/visualizations/EvolutionTimeline.tsx` | Interactive SVG timeline with classification formatting |
| `site/lib/types/taxonomy.ts` | STRUCTURAL_MODELS with name, shortName, description, characteristics |
| `site/lib/types/specimen.ts` | Full specimen type definitions |
| `site/app/specimens/page.tsx` | Server component that reads `searchParams.model` for initial filter |
| `site/components/layout/SiteHeader.tsx` | Nav with "Principles" link (was "Mechanisms" → "Patterns" → "Principles") |
| `site/tailwind.config.ts` | Custom botanical palette: forest, cream, amber, sage, charcoal |

### Directory Structure
```
orgtransformation/
├── site/                    # Next.js app
│   ├── app/                 # App Router pages
│   │   ├── api/chat/        # NEW: Claude streaming endpoint
│   │   ├── matcher/         # Matcher page (now with tabs)
│   │   ├── mechanisms/      # Principles listing (route still named mechanisms)
│   │   ├── specimens/       # Specimen browser (now reads ?model= param)
│   │   └── page.tsx         # Home page (fully rewritten)
│   ├── components/
│   │   ├── home/            # NEW: FieldObservation component
│   │   ├── matcher/         # ChatMatcher, MatcherTabs (NEW), MatcherForm
│   │   ├── specimens/       # SpecimenBrowser, tabs, cards
│   │   └── visualizations/  # EvolutionTimeline (fixed)
│   ├── lib/
│   │   ├── data/            # specimens.ts, synthesis.ts (data loaders)
│   │   ├── matcher/         # NEW: buildSystemPrompt.ts
│   │   └── types/           # taxonomy.ts (updated), specimen.ts, synthesis.ts
│   └── .env.local           # SITE_ANTHROPIC_API_KEY (see gotchas below)
├── specimens/               # Raw specimen JSON files
├── synthesis/               # mechanisms.json
├── APP_STATE.md             # Project state doc (may be stale after this sprint)
├── HANDOFF_UI_SPRINT.md     # The sprint spec we implemented
└── HOME_PAGE_REDESIGN.md    # Detailed home page design spec
```

---

## Session Work Details

### Files Created
| File | Purpose |
|------|---------|
| `site/app/api/chat/route.ts` | Streaming POST endpoint, uses Anthropic SDK with claude-sonnet-4-20250514 |
| `site/components/home/FieldObservation.tsx` | Client component, random quote from mechanisms with 2+ specimens |
| `site/components/matcher/ChatMatcher.tsx` | Full chat UI: streaming, sessionStorage, markdown links, reset button |
| `site/components/matcher/MatcherTabs.tsx` | Tab toggle component (Chat Advisor / Quick Match) |
| `site/lib/matcher/buildSystemPrompt.ts` | Builds system prompt from all models + compressed specimen registry |

### Files Modified (20 files)
| File | Changes Made |
|------|--------------|
| `site/app/page.tsx` | Complete rewrite: full-bleed hero, species cards, specimens, stats, field observation |
| `site/app/specimens/page.tsx` | Added `searchParams` prop, passes `initialModel` to SpecimenBrowser |
| `site/app/matcher/page.tsx` | Now uses MatcherTabs with ChatMatcher + MatcherForm |
| `site/app/mechanisms/page.tsx` | "Patterns" → "Principles" in all display text |
| `site/app/mechanisms/[id]/page.tsx` | "Pattern" → "Principle" in breadcrumb, title, headers |
| `site/app/about/page.tsx` | "Patterns" → "Principles" in stats, methodology steps |
| `site/app/compare/page.tsx` | "patterns" → "principles" in description |
| `site/components/layout/SiteHeader.tsx` | Nav label: "Mechanisms" → "Patterns" → "Principles" |
| `site/components/specimens/SpecimenTabs.tsx` | Tab label: "Principles" |
| `site/components/specimens/MechanismsTab.tsx` | "Structural principles" heading, "No principles documented" |
| `site/components/specimens/RelatedTab.tsx` | "Shared Principles" title and description |
| `site/components/specimens/SpecimenBrowser.tsx` | Added `initialModel` prop, species description card above results |
| `site/components/specimens/EvolutionTab.tsx` | Reframed copy for organizational evolution |
| `site/components/visualizations/EvolutionTimeline.tsx` | "Latest" badge, "Observation N of N", formatClassification() |
| `site/components/compare/ComparisonView.tsx` | "Patterns" → "Principles" section label |
| `site/lib/types/taxonomy.ts` | Added `characteristics` field (2-3 sentences) to all 7 STRUCTURAL_MODELS |
| `site/package.json` | Added @anthropic-ai/sdk dependency |

### Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| `SITE_ANTHROPIC_API_KEY` env var name | Claude Code CLI sets `ANTHROPIC_API_KEY=""` which overrides .env.local | Tried `ANTHROPIC_API_KEY` first — it was always empty at runtime |
| sessionStorage (not localStorage) for chat | Chat should persist within tab session but reset on new visit | localStorage would keep stale conversations across days |
| `claude-sonnet-4-20250514` for matcher | Good balance of quality and speed for conversational UX | Could use haiku for faster responses if cost is a concern |
| Display-only renames (routes unchanged) | Routes like `/mechanisms/` stay stable; only user-facing text changes | Could rename routes but would break any existing bookmarks/links |

### Things That Didn't Work
| Attempted | Why It Failed | What Worked Instead |
|-----------|---------------|---------------------|
| `ANTHROPIC_API_KEY` in .env.local | Claude Code CLI injects empty `ANTHROPIC_API_KEY=""` into process env, overriding .env.local | Renamed to `SITE_ANTHROPIC_API_KEY` |
| `new Anthropic()` at module top level | process.env not available at module load time in Next.js API routes | Moved client instantiation inside the POST handler |
| Math.random() in useState initializer | Hydration mismatch: server and client produce different random values | Moved to useEffect (client-only) |
| Home page first design attempt | User said it was "hideous" and "looks like Yahoo circa 1998" — flat, monotone, no depth | Full-bleed dark forest hero, white cards, gradient accents, hover effects |

---

## Technical State

### Build Status
```
npm run build → SUCCESS (107 static pages, 0 errors)
Routes: / (static), /api/chat (dynamic), /specimens (dynamic), /matcher (static), all others static/SSG
```

### Git Status
```
20 modified files, 5 new untracked files — ALL UNCOMMITTED
No staged changes
Branch: main (up to date with origin)
```

### Environment
- Node.js v22.20.0
- Next.js 14.2.35
- @anthropic-ai/sdk (installed)
- `SITE_ANTHROPIC_API_KEY` in `site/.env.local` (NOT `ANTHROPIC_API_KEY` — see gotchas)

---

## Implicit Knowledge (Critical!)

**Things learned this session that aren't captured in code:**

1. **Claude Code CLI env conflict**: The CLI sets `ANTHROPIC_API_KEY=""` in the process environment. Next.js won't override existing env vars from `.env.local`. Must use a different name like `SITE_ANTHROPIC_API_KEY`.

2. **Layer classification is polymorphic**: The TypeScript type says `classification?: string | null` but many specimen JSON files have `classification` as an object `{structuralModel, orientation, confidence, action}`. The fix in EvolutionTimeline.tsx handles both.

3. **Home page breaks out of layout container**: Uses `-mx-4 -mt-8 sm:-mx-6 lg:-mx-8` to break out of the `max-w-7xl px-4` container in layout.tsx for full-bleed sections.

4. **FieldObservation avoids hydration errors**: Must use `useEffect` for randomization, not `useState` initializer, because server and client would produce different random values.

5. **Specimen data lives OUTSIDE site/**: JSON files are in `orgtransformation/specimens/` and `orgtransformation/synthesis/`, loaded by `site/lib/data/specimens.ts` and `site/lib/data/synthesis.ts`.

**User preferences discovered:**
- Wants things to be visually compelling, "fun and pretty and botanistical" — not flat/corporate
- Values rich visual design with depth (shadows, gradients, dark/light alternation)
- Prefers quick iteration — "make it then let me see it"
- Uses the term "species" for the 7 structural models, "specimens" for individual organizations
- Changed terminology twice: Mechanisms → Patterns → Principles (final: "Principles")

**Codebase quirks:**
- The route is still `/mechanisms/` but displays "Principles" everywhere — intentional to avoid breaking links
- `SpecimenBrowser` is a client component that needs `initialModel` from server-side `searchParams`
- The taxonomy `characteristics` field was added to the type but only exists in the `STRUCTURAL_MODELS` constant, not in the TypeScript type definition (it's accessed dynamically)

---

## How to Continue

### Immediate Next Steps
1. **First**: Commit all changes — `git add` the 20 modified + 5 new files (exclude `.env.local`), commit with a descriptive message
2. **Then**: Ask the user what they want to work on next
3. **Potential tasks**: Update APP_STATE.md to reflect completed sprint, rename `/mechanisms/` route to `/principles/`, enhance chat markdown rendering, add more specimens

### Commands to Run on Startup
```bash
# 1. Read this handoff
cat HANDOFF.md

# 2. Read project instructions
cat site/CLAUDE.md

# 3. Verify project builds
cd site && npm run build

# 4. Start dev server
cd site && npx next dev --port 3000
```

### Open Questions
- [ ] Should the `/mechanisms/` route be renamed to `/principles/`? (Display text already says Principles)
- [ ] Does the user want APP_STATE.md updated to reflect the completed sprint?
- [ ] Should the chat matcher use a cheaper/faster model (haiku) instead of sonnet?

---

## Reference

### Available Skills
- `/superpowers-brainstorm` — Explore requirements and design
- `/superpowers-write-plan` — Create detailed implementation plans
- `/superpowers-tdd` — Test-driven development
- `/superpowers-debug` — Systematic debugging
- `/superpowers-verify` — Verification before completion
- `/extract-pdf` — Extract clean text from PDFs
- `/analyze-manuscript` — Full manuscript AI detection pipeline

### Common Commands
```bash
# Build the site
cd "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/site" && npm run build

# Dev server
cd "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/site" && npx next dev --port 3000

# Test chat API directly
curl -s -X POST http://localhost:3000/api/chat -H 'Content-Type: application/json' -d '{"messages":[{"role":"user","content":"hello"}]}'
```

---

## Session Metadata

- **Key Topics:** UI sprint, terminology rename, home page redesign, evolution tab, Claude API streaming chat, sessionStorage persistence, env var conflicts
- **User Communication Style:** Brief, direct, visual-first. Provides feedback via screenshots. Expects fast iteration. Will say "it's hideous" if it's ugly — values honest feedback loops.
