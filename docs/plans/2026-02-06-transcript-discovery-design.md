# Transcript Discovery Protocol: Design Document

## Created: February 6, 2026

---

## 1. Overview

A project-wide Transcript Discovery Protocol that systematically finds long-form interview transcripts for organizational leaders. Serves both specimen research enrichment and purpose claims scanning.

### Core Principle

**Be creative and energetic about finding transcripts.** Don't limit to a hardcoded podcast list. Search broadly for any source where a leader spoke at length and a transcript exists — podcasts, YouTube, congressional testimony, analyst days, conference talks, earnings calls.

### Design Decisions Made

| Decision | Resolution |
|----------|-----------|
| Transcript scope | All types: native, third-party, auto-generated — with quality flags |
| Discovery trigger | Hybrid: quick upfront sweep + on-demand deep discovery |
| Data storage | Two layers: source-level registry + specimen-level tracking |
| Search strategy | Leader + Company + Known sources + Formal/official |
| YouTube handling | Note URLs, queue for manual pull on high-priority specimens |
| Skill integration | Shared protocol file referenced by both /research and /purpose-claims |

---

## 2. Data Architecture

### Layer 1: Source-Level Registry

**File:** `research/transcript-sources.json`

What transcript sources exist in the world. Metadata about each source's transcript quality and access method.

```json
{
  "description": "Registry of transcript sources — podcasts, channels, and platforms where leader interviews with transcripts exist.",
  "lastUpdated": "2026-02-06",
  "sources": [
    {
      "id": "cheeky-pint",
      "name": "Cheeky Pint",
      "type": "podcast",
      "url": "https://cheekypint.substack.com",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://cheekypint.substack.com/p/{episode-slug}",
      "notes": "Full transcripts on Substack. On hiatus since Nov 2025."
    }
  ]
}
```

**Source types:** `podcast` | `youtube-channel` | `news-outlet` | `conference` | `official` | `earnings`

**Transcript quality:** `native` | `third-party` | `auto-generated`

**Transcript access:** `programmatic` | `manual-required`

### Layer 2: Specimen-Level Tracking

**File:** `research/transcript-gap-queue.json` (expanded from existing)

For each specimen's leader(s), what transcript sources exist and their scan status.

```json
{
  "description": "Tracks transcript sources discovered for each specimen's leader(s). Status: discovered | scanned | queued-for-manual. Serves both /research and /purpose-claims.",
  "lastUpdated": "2026-02-06",
  "gaps": [
    {
      "specimenId": "anthropic",
      "leader": "Dario Amodei",
      "leaderTitle": "CEO",
      "sourceId": "cheeky-pint",
      "episodeTitle": "Dario Amodei — Anthropic CEO",
      "episodeUrl": "https://cheekypint.substack.com/p/dario-amodei",
      "episodeDate": "2025-09",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "high",
      "status": "scanned",
      "discoveredDate": "2026-02-03",
      "scannedDate": "2026-02-03",
      "notes": "14 purpose claims extracted."
    }
  ]
}
```

**Status values:** `discovered` | `scanned` | `queued-for-manual`

**AI relevance:** `yes` | `likely` | `unknown` (filters for purpose-relevant content)

**Priority:** `high` | `medium` | `low`

---

## 3. Discovery Protocol

### Phase 1: Quick Upfront Sweep

Run once to build baseline coverage across all 93 specimens.

**Step 1: Identify leader(s)**
- Read specimen JSON for CEO/founder name(s)
- Note title and tenure (current vs. former leaders)

**Step 2: Run discovery searches**

Leader-centric:
- `"[Leader name]" podcast interview`
- `"[Leader name]" interview transcript`
- `"[Leader name]" site:youtube.com interview`

Company-centric:
- `"[Company]" CEO interview podcast`
- `"[Company]" earnings call transcript`
- `"[Company]" analyst day transcript`

Known high-yield sources:
- `"[Leader name]" site:acquired.fm`
- `"[Leader name]" site:lexfridman.com`
- `"[Leader name]" site:dwarkesh.com`
- `"[Leader name]" site:cheekypint.substack.com`
- `"[Leader name]" site:latent.space`
- `"[Leader name]" site:conversationswithtyler.com`
- `"[Leader name]" site:cognitiverevolution.ai`

Formal/official:
- `"[Leader name]" testimony congress OR senate`
- `"[Leader name]" keynote transcript`
- `"[Company]" shareholder meeting transcript`

**Step 3: Classify each discovered source**
- Determine transcriptQuality and transcriptAccess
- Assess aiRelevance
- Set priority based on specimen importance and source quality

**Step 4: Record in data files**
- New sources → transcript-sources.json
- New specimen×source pairs → transcript-gap-queue.json

### Phase 2: On-Demand Deep Discovery

Triggered when:
- Scanning a specimen that came up thin or none
- Specimen is high-priority and we want comprehensive coverage
- New leader joins a specimen (e.g., new CEO)

Deep discovery adds:
- Broader YouTube search (channel-specific, conference channels)
- Search for third-party transcriptions of known interviews
- Check if press articles quote extensively (pseudo-transcript)
- Industry-specific sources (e.g., healthcare conferences for pharma CEOs)

---

## 4. Transcript Quality Tiers

| Tier | Type | Quality | Access | Example |
|------|------|---------|--------|---------|
| **native** | Published by source | Verbatim | Programmatic fetch | Cheeky Pint, Dwarkesh, Acquired |
| **third-party** | Transcribed by others | Usually verbatim | Programmatic fetch | News outlets quoting extensively |
| **auto-generated** | YouTube auto-captions | ~95% accurate | Manual pull required | Bloomberg YouTube, CNBC |

### YouTube Handling

YouTube is a large source of long-form content, but auto-captions require manual pull:

1. During discovery, note YouTube URLs in transcript-gap-queue.json
2. Flag as `transcriptAccess: manual-required`
3. For high-priority specimens, add to manual pull queue
4. User batch-processes manual pulls periodically
5. When pulled, update status and scan for claims

---

## 5. Integration with Existing Skills

### Protocol File

**Location:** `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`

Both `/research` and `/purpose-claims` will `!cat` this file when they need transcript discovery.

### How /research Uses It

In SESSION-PROTOCOL.md, add Step 2b:

```
Step 2b: Check Transcript Availability

Before deep-scanning any podcast or interview source:
1. Check transcript-gap-queue.json for this specimen
2. If no entry exists, run quick discovery (see TRANSCRIPT-DISCOVERY-PROTOCOL.md)
3. Prioritize sources with transcriptAccess: programmatic
4. For manual-required sources, note in session file and add to queue
```

### How /purpose-claims Uses It

Update Step 1 in SKILL.md:

```
Step 1: Check Transcript Availability

Follow research/TRANSCRIPT-DISCOVERY-PROTOCOL.md:
1. Read transcript-gap-queue.json for this specimen
2. If no entries OR entries are stale (>30 days), run discovery
3. Prioritize native > third-party > auto-generated
4. Queue manual-required sources if high-priority specimen
```

### Shared Maintenance

After any session that discovers new transcript sources:
1. Add new sources to transcript-sources.json
2. Add new specimen×source pairs to transcript-gap-queue.json
3. Update status flags when sources are scanned

---

## 6. Implementation Plan

### New Files to Create

| File | Purpose |
|------|---------|
| `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` | Shared protocol for finding transcripts |
| `research/transcript-sources.json` | Source-level registry of transcript sources |

### Files to Modify

| File | Changes |
|------|---------|
| `research/transcript-gap-queue.json` | Expand schema with new fields |
| `research/SESSION-PROTOCOL.md` | Add Step 2b for transcript availability check |
| `.claude/skills/purpose-claims/SKILL.md` | Update Step 1 to reference shared protocol |
| `.claude/skills/research/SKILL.md` | Add reference to transcript protocol |

### Seed Data

**transcript-sources.json** — Start with known sources:
- 7 podcasts with `transcriptsAvailable: true` from source-registry.json
- Earnings call sources (Seeking Alpha, Motley Fool)
- Congressional testimony (congress.gov)
- YouTube channels (Bloomberg, CNBC, Fortune) — flagged as manual-required

**transcript-gap-queue.json** — Migrate existing 10 entries to new schema

---

## 7. Success Criteria

1. Every specimen scan checks transcript availability before searching
2. New transcript sources are added to registry as discovered
3. High-priority specimens have comprehensive transcript coverage
4. Manual-pull queue is visible and actionable
5. Purpose claims yield improves (fewer thin/none results)

---

## 8. Relationship to Other Specs

| Spec | Relationship |
|------|-------------|
| `PURPOSE-CLAIMS-SPEC.md` | Defines claim capture; transcript protocol feeds it verbatim sources |
| `SESSION-PROTOCOL.md` | Research workflow; gains transcript check step |
| `source-registry.json` | General sources; transcript-sources.json is specialized subset |
| `CLAUDE.md` | Project instructions; references this infrastructure |
