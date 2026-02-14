---
name: handoff
description: "Session end: archive previous handoff, write fresh HANDOFF.md, update SESSION_LOG.md, run validation"
disable-model-invocation: true
---

# Session Handoff Skill

Run this at the end of every session that modified files. It maintains the handoff document as a lean, scannable summary of the current session's work and next-session priorities.

## How It Works

1. **Archive** the previous session's content from HANDOFF.md → append to HANDOFF_ARCHIVE.md
2. **Rewrite** HANDOFF.md with fresh content for the current session
3. **Update** SESSION_LOG.md with a new row
4. **Validate** if specimens or site code changed

## Step-by-Step Protocol

### Step 1: Read Current State

Read these files to understand what needs to be captured:

- `HANDOFF.md` — the outgoing session's content (will be archived)
- `SESSION_LOG.md` — to determine session number and add new row
- `APP_STATE.md` — for current data counts to cross-reference

### Step 2: Archive the Outgoing Session

Append the **entire "What Happened This Session" section** from the current HANDOFF.md to the top of HANDOFF_ARCHIVE.md (below the header). Format it as:

```markdown
## Session {N} ({date}): {short description}

{content from "What Happened This Session"}
```

This ensures nothing is ever lost. HANDOFF_ARCHIVE.md grows monotonically.

### Step 3: Present Draft Handoff to Collaborator

Before writing, present the proposed handoff content to the user for review. This is a collaborative project — the handoff should reflect both collaborators' understanding of what happened and what matters next.

Draft the following sections based on the session's work:

**What Happened This Session** — Bullet list of concrete actions:
- Data changes (claims added, specimens created/updated, insights added/updated)
- Infrastructure changes (scripts, skills, protocols)
- Key analytical findings or botanist discussions
- Include specific numbers (e.g., "Registry: 1,384 → 1,436 claims")

**Active Analytical Threads** — Table of live threads to watch across future specimens. Update from previous session:
- Add any new threads that emerged
- Mark any resolved threads
- Keep the "What to Watch For" column actionable

**Immediate Next Steps** — Numbered priorities with enough context to act on immediately. Order by urgency/importance. Each priority should be 2-3 lines max.

**Pending Botanist Discussions** — Items flagged for interactive collaborative analysis. These are NOT to be done unilaterally by Claude — they require back-and-forth discussion.

**Housekeeping** — Mechanical tasks: git commits, file cleanup, stale data fixes.

### Step 4: Write HANDOFF.md

After user confirms (or adjusts) the draft, write HANDOFF.md using this exact template:

```markdown
# Session Handoff — {date} (Session {N})

## What Happened This Session

{bullets}

## Active Analytical Threads

| Thread | Status | What to Watch For |
|--------|--------|-------------------|
{rows}

## Immediate Next Steps (Start Here)

### Priority 1: {title}
{2-3 lines of context}

### Priority 2: {title}
{2-3 lines of context}

{...more priorities as needed}

## Pending Botanist Discussions

| Topic | Context | Why It Matters |
|-------|---------|---------------|
{rows}

## Housekeeping

{bullets}

---

*For historical context, see `HANDOFF_ARCHIVE.md`.*
*For current data counts and site status, see `APP_STATE.md`.*
*For full session history, see `SESSION_LOG.md`.*
```

**Target length: under 80 lines.** If it's getting longer, you're including too much detail — push context to APP_STATE.md or HANDOFF_ARCHIVE.md.

### Step 5: Update SESSION_LOG.md

Add a new row to the session log table:

```markdown
| {date} | {one-line summary of what changed} |
```

Keep it concise — the detail is in HANDOFF.md.

### Step 6: Validate

- **If specimens changed:** Run `node scripts/validate-workflow.js` from project root
- **If site code changed:** Run `cd site && npm run build` to verify no breakage

## Guardrails

- **Never delete content from HANDOFF_ARCHIVE.md** — it only grows
- **Always archive before overwriting** — the outgoing session's "What Happened" goes to the archive BEFORE HANDOFF.md is rewritten
- **Present to user before writing** — the handoff reflects collaborative understanding, not unilateral summary
- **Keep HANDOFF.md under 80 lines** — if it's longer, you're doing it wrong
- **Don't duplicate APP_STATE.md** — HANDOFF.md captures session narrative and priorities, not data counts. Reference APP_STATE.md for current numbers.
