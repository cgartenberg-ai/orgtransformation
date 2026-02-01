---
name: ambidexterity-research
description: "Phase 1 (Field Work) of the organizational ambidexterity research workflow. Use when gathering observations about how organizations structure AI exploration and execution. Scans sources (podcasts, substacks, SEC filings, press) to collect raw findings with full provenance. Does NOT classify — outputs raw observations for later curation."
---

# Ambidexterity Research Skill (Phase 1: Field Work)

## Purpose

Gather wide (many organizations) and deep (specifics about each) observations about how organizations structure AI work. Focus on the exploration/execution tension.

## What to Look For

Organizations that reveal **how** they structure AI initiatives — not just that they're "doing AI." Signals:

- Structural arrangements: labs, CoEs, embedded teams, tiger teams, informal adoption
- Resource allocation: budgets, headcount, reporting lines
- Time horizons: quarterly vs. multi-year
- Integration mechanisms: how exploration connects to execution
- Leadership involvement: CEO protection, CAIO appointments
- Specific metrics: adoption rates, graduation rates, investment levels
- Quotes from leaders explaining rationale

## Source Priority

See `references/sources-quick-ref.md` for quick reference, or `../../sources.md` for full source list. Priority order:

1. **Tier 1 podcasts**: Cheeky Pint, No Priors, BG2, Dwarkesh, Latent Space, Acquired
2. **Tier 1 substacks**: Stratechery, One Useful Thing, Not Boring
3. **SEC/investor materials**: 10-K, earnings calls, investor days
4. **Press**: TechCrunch, Bloomberg, The Information

## Output Format

For each organization observed, record:

```markdown
## [Organization Name]

### Raw Observations
- [Observation 1]
- [Observation 2]
- ...

### Specimen Sources
Every fact must link to a retrievable source. Capture full URLs.

| Fact | Source Type | Source | URL | Timestamp | Source Date | Collected |
|------|-------------|--------|-----|-----------|-------------|-----------|
| "300-400 person hubs" | Podcast | Cheeky Pint, Dave Ricks | https://... | 23:45 | 2025-11-xx | 2026-01-15 |
| "$1B NVIDIA partnership" | Press | NVIDIA press release | https://... | — | 2026-01-12 | 2026-01-13 |
| "18-year program" | Article | Chief Executive Mag | https://... | — | 2025-xx-xx | 2025-12-15 |

**Source Types**: Podcast, Substack, Press, SEC Filing, Earnings Call, Interview, Report, LinkedIn

**Timestamp**: For audio/video, note the timestamp (e.g., 23:45) where the fact appears. Use "—" for text sources.

**URL is required** unless source is behind paywall or unavailable — then note "[paywall]" or "[no URL]" with enough detail to locate.

### Quotes
> "[Direct quote — verbatim]"
> — [Speaker name], [Title], [Source with URL], [Timestamp if audio/video], [Date]

Example:
> "Middle management tends to squash deviations, but the deviations are the people doing stuff off strategy, in the labs, the things that make the next breakthrough."
> — Dave Ricks, CEO Eli Lilly, [Cheeky Pint](https://...), 34:12, November 2025

### Evolution Flags
If this org appears to have CHANGED its approach (not just new detail):
- EVOLUTION: [old state] → [new state] as of [date]
- Source for change: [URL]

### Open Questions
- [What's unclear or needs more research]
```

## Collection Principles

1. **Additive only (Stratigraphy)** — Research findings ADD to existing knowledge, never replace. If an org has changed its approach, record the NEW approach with its date — don't delete the old. Each finding becomes a dated layer. Phase 2 will reconcile layers into specimen history.

2. **Flag evolution** — When you find information that suggests an org has CHANGED its approach (not just new detail about existing approach), note explicitly: "EVOLUTION: [old state] → [new state] as of [date]"

3. **No interpretation yet** — Record what you observe, not what category it fits

4. **URLs are mandatory** — Every fact needs a retrievable URL. For podcasts/videos, include timestamp. If paywalled, note "[paywall]" with enough detail to locate later.

5. **Source everything** — Every fact needs source, URL, and date. No orphan facts.

6. **Preserve quotes verbatim** — Direct quotes are gold. Capture exact wording with speaker, title, source URL, timestamp, date.

7. **Two timestamps always** — Capture both:
   - **Source Date**: When the org revealed/disclosed this (the "as-of" date)
   - **Collected**: When you found it (today)

8. **Note uncertainty** — If a date or detail is approximate, mark it (e.g., "~2025" or "2025-xx")

9. **Flag gaps** — Note what would be useful to know but isn't available

## Research Session Workflow

**IMPORTANT: Follow the step-by-step protocol in `../../research/SESSION-PROTOCOL.md` for session execution.**

The protocol ensures thorough coverage across multiple source types and deep, focused findings. Every observation must be filtered through the core research question:

> **"How do organizations structurally enable both exploration and execution in the AI era?"**

**Relevance Test** — before recording any observation, it must pass at least ONE of:
1. **Structural**: Tells us about org structures (labs, teams, reporting lines, governance, resource allocation)
2. **Tension**: Reveals how the org handles the explore/execute tension (trade-offs, dual structures, integration)
3. **Specificity**: Has concrete detail (names, numbers, headcount, budgets, timelines, direct quotes)

If it fails all three, don't record it.

**Quick summary of protocol steps:**
1. **Pre-session**: Check source-registry.json for coverage gaps, plan multi-type source scan
2. **Scan thoroughly**: Cover multiple source TYPES (podcasts + substacks + press), not just one source
3. **Triage before deep-scanning**: Use show notes/headlines to identify high-value content
4. **Apply Relevance Test**: Every finding must address the core question with structural depth
5. **Discover new sources**: Add any new sources found to sources.md and source-registry.json
6. **Record findings** in output format above — do not classify; that's Phase 2
7. **Update registries**: source-registry.json, research/queue.json
8. **Validate**: Run `node scripts/validate-workflow.js`

See `SESSION-PROTOCOL.md` for the full checklist, scan methods per source type, and quality standards.

## Keywords to Search

```
STRUCTURAL:
"AI lab", "research lab", "product lab", "center of excellence", "CoE"
"incubator", "venture studio", "venture builder", "spin-off", "tiger team"

LEADERSHIP:
"Chief AI Officer", "CAIO", "Head of AI", "VP of AI"

STRATEGY:
"AI strategy", "AI transformation", "build vs buy"
"centralized", "federated", "hub and spoke"

METRICS:
"adoption", "deployment", "rollout", "headcount"
```

## Session Output

End each research session with:

```markdown
# Research Session: [Date]

## Sources Scanned
| Source | Type | Scanned Through | URL | Results |
|--------|------|-----------------|-----|---------|
| No Priors | Podcast | Ep 127 "Jensen Huang" | https://... | 2 orgs |
| Stratechery | Substack | "AI and Enterprise" | https://... | 1 org |

## Organizations Observed
[List of orgs with findings in format above, including full Specimen Sources tables]

## Source Index
Consolidated list of all URLs captured this session:
- [URL 1] — [what it contains]
- [URL 2] — [what it contains]

## Notes for Next Session
- [What to follow up on]
- [Gaps identified]
```
