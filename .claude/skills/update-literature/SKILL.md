---
name: update-literature
description: "Scan for new research papers in library/research papers/ and generate literature registry entries via background agents. Each paper is read in a separate process to protect main context."
---

# Update Literature Registry

You are updating the literature registry for the Ambidexterity Field Guide. Your job is to find new PDFs that haven't been processed yet, spawn background agents to read them, and help merge the results.

## Core Principle

**Protect the main context.** Paper PDFs are large. Never read a PDF directly in this conversation. Always delegate PDF reading to background Task agents (subagent_type: "general-purpose", run_in_background: true).

## Protocol

Follow this protocol step by step. Do NOT skip steps.

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/literature/LITERATURE-PROTOCOL.md"`

## Agent Template

When spawning agents in Step 4, use this template for the agent prompt (with substitutions filled in):

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/literature/AGENT-TEMPLATE.md"`

## Current Registry

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/literature/registry.json"`

## Literature Spec (for reference)

The full literature matching system design is in `LITERATURE_SPEC.md` at the project root. Consult it if you need context on registry schema, relationship types, or the `/literature-match` protocol.

$ARGUMENTS
