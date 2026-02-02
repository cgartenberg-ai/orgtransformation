---
name: research
description: "Phase 1: Execute a research session — scan sources for organizational AI structure findings following the session protocol"
disable-model-invocation: true
---

# Phase 1: Research Session

You are executing a research session for the Ambidexterity Field Guide project.

## Core Research Question

Every observation you gather must speak to this question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

## Session Protocol

Follow this protocol step by step. Do NOT skip steps.

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/SESSION-PROTOCOL.md"`

## What to Look For and Output Format

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/skills/ambidexterity-research/SKILL.md"`

## Current Source Registry (check this FIRST to see what's been scanned)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens/source-registry.json"`

## Current Curation Queue (check for pending items)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/queue.json"`

## Session Log (see what previous sessions found)

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/SESSION-LOG.md"`

## Dual-Path Research

This skill supports two research paths. Specify which path when invoking:

### General Research (default)
`/research` or `/research general`

Standard multi-source scanning for new specimens and updates. Follows the full session protocol above.

### Low-Confidence Targeted Research
`/research low-confidence`

Targeted research to improve classification confidence for specific specimens. Process:

1. Read `research/low-confidence-queue.json` — identify specimens with `"status": "pending"`
2. For each pending specimen, use `whatToLookFor` to guide targeted searches
3. Search for specific structural details, org charts, reporting lines, headcounts
4. If new evidence found: update the specimen JSON (add layer, adjust confidence, update sources)
5. Increment `researchCycles` and set `lastResearchDate` in the queue entry
6. If confidence improves to Medium or High: set queue entry status to `"resolved"`
7. If no useful evidence found after 2+ cycles: set status to `"deferred"` — the specimen stays as-is until new information surfaces naturally
8. Run `node scripts/validate-workflow.js` to confirm consistency

The low-confidence path is intentionally narrow — don't expand into general research during these sessions. Stay focused on the specific specimens and questions in the queue.

## Your Task

Execute a complete research session following the protocol above:

1. Check the source registry for coverage gaps
2. Plan which sources to scan (multiple types: podcasts + substacks + press)
3. Triage episodes/articles using show notes and headlines
4. Deep-scan high-priority content, applying the Relevance Test to every finding
5. Record findings in a new session file: `research/sessions/YYYY-MM-DD-{description}.md`
6. Update source-registry.json, research/queue.json, SESSION-LOG.md
7. If new sources discovered, add to sources.md AND source-registry.json
8. Run `node scripts/validate-workflow.js` to confirm consistency

$ARGUMENTS
