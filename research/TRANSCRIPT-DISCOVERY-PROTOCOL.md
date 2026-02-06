# Transcript Discovery Protocol

## Purpose

This protocol systematically finds long-form interview transcripts for organizational leaders. It serves both specimen research enrichment and purpose claims scanning.

## Core Principle

**Be creative and energetic about finding transcripts.** Don't limit to a hardcoded podcast list. Search broadly for any source where a leader spoke at length and a transcript exists — podcasts, YouTube, congressional testimony, analyst days, conference talks, earnings calls.

---

## Data Files

| File | Purpose |
|------|---------|
| `research/transcript-sources.json` | Registry of transcript sources (podcasts, channels, platforms) |
| `research/transcript-gap-queue.json` | Specimen × source pairs with scan status |

---

## Phase 1: Quick Upfront Sweep

Run for any specimen that needs transcript discovery.

### Step 1: Identify Leader(s)

Read the specimen JSON for CEO/founder name(s). Note:
- Full name
- Current title
- Tenure (current vs. former)
- Company name

### Step 2: Run Discovery Searches

Execute these search patterns:

**Leader-centric:**
```
"[Leader name]" podcast interview
"[Leader name]" interview transcript
"[Leader name]" site:youtube.com interview
```

**Company-centric:**
```
"[Company]" CEO interview podcast
"[Company]" earnings call transcript
"[Company]" analyst day transcript
```

**Known high-yield sources:**
```
"[Leader name]" site:acquired.fm
"[Leader name]" site:lexfridman.com
"[Leader name]" site:dwarkesh.com
"[Leader name]" site:cheekypint.substack.com
"[Leader name]" site:latent.space
"[Leader name]" site:conversationswithtyler.com
"[Leader name]" site:cognitiverevolution.ai
```

**Formal/official:**
```
"[Leader name]" testimony congress OR senate
"[Leader name]" keynote transcript
"[Company]" shareholder meeting transcript
```

### Step 3: Classify Each Discovered Source

For each source found, determine:

| Field | Options |
|-------|---------|
| `transcriptQuality` | `native` (published by source) \| `third-party` (transcribed by others) \| `auto-generated` (YouTube captions) |
| `transcriptAccess` | `programmatic` (can fetch directly) \| `manual-required` (needs human intervention) |
| `aiRelevance` | `yes` (definitely discusses AI) \| `likely` (probably relevant) \| `unknown` |
| `priority` | `high` (important specimen + quality source) \| `medium` \| `low` |

### Step 4: Record in Data Files

1. **New sources** → Add to `transcript-sources.json`
2. **New specimen × source pairs** → Add to `transcript-gap-queue.json` with `status: discovered`

---

## Phase 2: On-Demand Deep Discovery

Trigger when:
- Specimen came up thin or none in quick sweep
- Specimen is high-priority and needs comprehensive coverage
- New leader joins a specimen (e.g., new CEO)

### Additional Searches

**Broader YouTube search:**
```
"[Leader name]" site:youtube.com interview OR keynote OR panel
"[Company]" CEO site:youtube.com 2025 OR 2026
```

**Conference channels:**
- Web Summit, TED, Davos, Fortune Brainstorm, Bloomberg Tech Summit

**Third-party transcriptions:**
```
"[Leader name]" transcript site:podscripts.co
"[Leader name]" transcript site:rev.com
```

**Extensive press quotes (pseudo-transcripts):**
```
"[Leader name]" interview transcript site:fortune.com OR site:bloomberg.com
```

**Industry-specific sources:**
- Healthcare: JPM Healthcare Conference, HLTH
- Finance: Davos, Milken
- Tech: TechCrunch Disrupt, Web Summit, All-In Summit

---

## Transcript Quality Tiers

| Tier | Type | Quality | Access | Example |
|------|------|---------|--------|---------|
| **native** | Published by source | Verbatim | Programmatic | Cheeky Pint, Dwarkesh, Acquired |
| **third-party** | Transcribed by others | Usually verbatim | Programmatic | News outlets quoting extensively |
| **auto-generated** | YouTube auto-captions | ~95% accurate | Manual required | Bloomberg YouTube, CNBC |

---

## YouTube Handling

YouTube is a large source of long-form content, but auto-captions require manual extraction:

1. During discovery, note YouTube URLs in `transcript-gap-queue.json`
2. Set `transcriptAccess: "manual-required"`
3. For high-priority specimens, set `priority: "high"` → user will batch-process
4. When manually extracted, update `status` to `scanned` and scan for claims

**Manual extraction process (for user):**
- Open YouTube video
- Click "..." menu → "Show transcript"
- Copy transcript text
- Save to local file for scanning

---

## Status Flow

```
discovered → scanned
     ↓
queued-for-manual (if transcriptAccess: manual-required)
```

- `discovered`: Source identified, not yet scanned
- `scanned`: Transcript has been read and claims extracted
- `queued-for-manual`: YouTube or other manual-required source, waiting for user extraction

---

## Integration

### From /research

In SESSION-PROTOCOL.md Step 2b:
1. Before deep-scanning a podcast/interview, check `transcript-gap-queue.json`
2. If no entry exists, run quick discovery
3. Prioritize `transcriptAccess: programmatic` sources
4. For `manual-required` sources, note in session file and add to queue

### From /purpose-claims

In SKILL.md Step 1:
1. Read `transcript-gap-queue.json` for this specimen
2. If no entries OR entries are stale (>30 days), run discovery
3. Prioritize: native > third-party > auto-generated
4. Queue manual-required sources if high-priority specimen

---

## After Any Scanning Session

1. Add new sources to `transcript-sources.json`
2. Add new specimen × source pairs to `transcript-gap-queue.json`
3. Update `status` and `scannedDate` for sources scanned
