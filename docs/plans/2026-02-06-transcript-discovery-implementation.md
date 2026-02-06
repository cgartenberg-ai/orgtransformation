# Transcript Discovery Protocol: Implementation Plan

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Implement systematic transcript discovery infrastructure that serves both specimen research and purpose claims scanning.

**Architecture:** Two-layer data storage (source registry + specimen tracking), shared protocol file, integration into existing skills via reference.

**Tech Stack:** JSON data files, Markdown protocol documentation, skill YAML configuration.

---

## Task 1: Create Source-Level Registry

**Files:**
- Create: `research/transcript-sources.json`

**Step 1: Create the transcript-sources.json file**

This file registers known transcript sources with metadata about quality and access method.

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
    },
    {
      "id": "dwarkesh-podcast",
      "name": "Dwarkesh Podcast",
      "type": "podcast",
      "url": "https://www.dwarkesh.com",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://www.dwarkesh.com/p/{episode-slug}",
      "notes": "Full transcripts published with each episode."
    },
    {
      "id": "latent-space",
      "name": "Latent Space",
      "type": "podcast",
      "url": "https://www.latent.space",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://www.latent.space/p/{episode-slug}",
      "notes": "Full transcripts on Substack."
    },
    {
      "id": "acquired",
      "name": "Acquired",
      "type": "podcast",
      "url": "https://www.acquired.fm",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://www.acquired.fm/episodes/{episode-slug}",
      "notes": "Full transcripts on website."
    },
    {
      "id": "conversations-with-tyler",
      "name": "Conversations with Tyler",
      "type": "podcast",
      "url": "https://conversationswithtyler.com",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://conversationswithtyler.com/episodes/{guest-slug}/",
      "notes": "Full transcripts published with each episode."
    },
    {
      "id": "lex-fridman",
      "name": "Lex Fridman Podcast",
      "type": "podcast",
      "url": "https://lexfridman.com",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://lexfridman.com/{guest-name}-transcript/",
      "notes": "Full transcripts published for each episode."
    },
    {
      "id": "cognitive-revolution",
      "name": "Cognitive Revolution",
      "type": "podcast",
      "url": "https://www.cognitiverevolution.ai",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://www.cognitiverevolution.ai/p/{episode-slug}",
      "notes": "Full transcripts on Substack."
    },
    {
      "id": "seeking-alpha",
      "name": "Seeking Alpha",
      "type": "earnings",
      "url": "https://seekingalpha.com",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://seekingalpha.com/article/{article-id}",
      "notes": "Earnings call transcripts. Some behind paywall."
    },
    {
      "id": "motley-fool",
      "name": "Motley Fool Transcripts",
      "type": "earnings",
      "url": "https://www.fool.com",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://www.fool.com/earnings/call-transcripts/{date}/{ticker}/",
      "notes": "Free earnings call transcripts."
    },
    {
      "id": "congress-gov",
      "name": "Congress.gov",
      "type": "official",
      "url": "https://www.congress.gov",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "transcriptUrlPattern": "https://www.congress.gov/event/{congress-number}/{chamber}/{event-id}",
      "notes": "Congressional testimony and hearing transcripts."
    },
    {
      "id": "youtube-bloomberg",
      "name": "Bloomberg YouTube",
      "type": "youtube-channel",
      "url": "https://www.youtube.com/@Bloomberg",
      "transcriptQuality": "auto-generated",
      "transcriptAccess": "manual-required",
      "transcriptUrlPattern": null,
      "notes": "Auto-captions available but require manual extraction."
    },
    {
      "id": "youtube-cnbc",
      "name": "CNBC YouTube",
      "type": "youtube-channel",
      "url": "https://www.youtube.com/@CNBC",
      "transcriptQuality": "auto-generated",
      "transcriptAccess": "manual-required",
      "transcriptUrlPattern": null,
      "notes": "Auto-captions available but require manual extraction."
    },
    {
      "id": "youtube-fortune",
      "name": "Fortune YouTube",
      "type": "youtube-channel",
      "url": "https://www.youtube.com/@FortuneMagazine",
      "transcriptQuality": "auto-generated",
      "transcriptAccess": "manual-required",
      "transcriptUrlPattern": null,
      "notes": "Auto-captions available but require manual extraction."
    }
  ]
}
```

**Step 2: Verify file was created correctly**

Run: `cat research/transcript-sources.json | head -50`
Expected: See the file header and first few sources.

**Step 3: Commit**

```bash
git add research/transcript-sources.json
git commit -m "feat: create transcript-sources.json registry

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 2: Expand transcript-gap-queue.json Schema

**Files:**
- Modify: `research/transcript-gap-queue.json`

**Step 1: Read current file**

Current schema has: specimenId, source, episodeTitle, transcriptUrl, leader, priority, notes

New schema adds: sourceId (rename from source), leaderTitle, episodeDate, transcriptQuality, transcriptAccess, aiRelevance, status, discoveredDate, scannedDate

**Step 2: Update the file with expanded schema**

Transform each existing entry to the new schema:

```json
{
  "description": "Tracks transcript sources discovered for each specimen's leader(s). Status: discovered | scanned | queued-for-manual. Serves both /research and /purpose-claims.",
  "lastUpdated": "2026-02-06",
  "created": "2026-02-03",
  "gaps": [
    {
      "specimenId": "intercom",
      "leader": "Des Traynor",
      "leaderTitle": "Cofounder",
      "sourceId": "cheeky-pint",
      "episodeTitle": "Des Traynor — Intercom Cofounder",
      "episodeUrl": "https://cheekypint.substack.com/p/des-traynor-cofounder-of-intercom",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "likely",
      "priority": "high",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Intercom is M3 Embedded Teams. Traynor likely has rich claims about AI customer service agents replacing human workflows."
    },
    {
      "specimenId": "shopify",
      "leader": "Tobi Lutke",
      "leaderTitle": "Founder/CEO",
      "sourceId": "cheeky-pint",
      "episodeTitle": "Tobi Lutke — Shopify Founder/CEO",
      "episodeUrl": "https://cheekypint.substack.com/p/tobi-lutke-shopify-founder-ceo",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "medium",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Shopify was web-scanned (5 claims found) but NOT transcript-deep-scanned from Cheeky Pint. May yield additional claims in conversational context."
    },
    {
      "specimenId": "ssi",
      "leader": "Ilya Sutskever",
      "leaderTitle": "CEO/Cofounder",
      "sourceId": "dwarkesh-podcast",
      "episodeTitle": "Ilya Sutskever — We're moving from the age of scaling to the age of research",
      "episodeUrl": "https://www.dwarkesh.com/p/ilya-sutskever-2",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "high",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "SSI is M9 AI-Native. Sutskever's founding vision and departure from OpenAI context — expect rich identity and direction-under-uncertainty claims."
    },
    {
      "specimenId": "microsoft",
      "leader": "Satya Nadella",
      "leaderTitle": "CEO",
      "sourceId": "dwarkesh-podcast",
      "episodeTitle": "Satya Nadella — How Microsoft is preparing for AGI (Nov 2025) + Microsoft's AGI plan (Feb 2025)",
      "episodeUrl": "https://www.dwarkesh.com/p/satya-nadella-2",
      "episodeDate": "2025-11",
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "medium",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Microsoft already has 15 claims. Two Dwarkesh episodes may yield additional direction-under-uncertainty claims about AGI preparation and CapEx."
    },
    {
      "specimenId": "google-deepmind",
      "leader": "Demis Hassabis",
      "leaderTitle": "CEO",
      "sourceId": "lex-fridman",
      "episodeTitle": "Demis Hassabis: Future of AI, Simulating Reality (Ep #475)",
      "episodeUrl": "https://lexfridman.com/demis-hassabis-2-transcript/",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "high",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Google DeepMind is M1 Research Lab. Hassabis is a Nobel Prize winner — expect identity claims about scientific mission and direction-under-uncertainty."
    },
    {
      "specimenId": "google-ai-infra",
      "leader": "Sundar Pichai",
      "leaderTitle": "CEO",
      "sourceId": "lex-fridman",
      "episodeTitle": "Sundar Pichai: CEO of Google and Alphabet (Ep #471)",
      "episodeUrl": "https://lexfridman.com/sundar-pichai-transcript/",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "high",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Pichai's structural commentary on Google's 25-year evolution and Gemini deployment. Expect transformation-framing and identity claims."
    },
    {
      "specimenId": "novo-nordisk",
      "leader": "Company history (no single leader)",
      "leaderTitle": null,
      "sourceId": "acquired",
      "episodeTitle": "Novo Nordisk (Ozempic)",
      "episodeUrl": "https://www.acquired.fm/episodes/novo-nordisk-ozempic",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "unknown",
      "priority": "medium",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Novo Nordisk is M4 Hub-and-Spoke. Acquired episode covers company history — may have structural context but less likely to have AI-specific purpose claims."
    },
    {
      "specimenId": "google-deepmind",
      "leader": "Company history (no single leader)",
      "leaderTitle": null,
      "sourceId": "acquired",
      "episodeTitle": "Google: The AI Company",
      "episodeUrl": "https://www.acquired.fm/episodes/google-the-ai-company",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "likely",
      "priority": "medium",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Already deep-scanned for research but not specifically for purpose claims. Rich structural history of Google's AI evolution."
    },
    {
      "specimenId": "mercor",
      "leader": "Brendan Foody",
      "leaderTitle": "CEO/Cofounder",
      "sourceId": "conversations-with-tyler",
      "episodeTitle": "Brendan Foody on Teaching AI and the Future of Knowledge Work (Ep #267)",
      "episodeUrl": "https://conversationswithtyler.com/episodes/brendan-foody/",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "high",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Mercor is M9 AI-Native. Youngest unicorn founder. Expect identity and direction-under-uncertainty claims about AI-native organizational design."
    },
    {
      "specimenId": "sierra-ai",
      "leader": "Bret Taylor",
      "leaderTitle": "CEO/Cofounder",
      "sourceId": "latent-space",
      "episodeTitle": "The AI Architect — Bret Taylor",
      "episodeUrl": "https://www.latent.space/p/bret",
      "episodeDate": null,
      "transcriptQuality": "native",
      "transcriptAccess": "programmatic",
      "aiRelevance": "yes",
      "priority": "high",
      "status": "discovered",
      "discoveredDate": "2026-02-03",
      "scannedDate": null,
      "notes": "Sierra is M9 AI-Native. Bret Taylor (Chairman of OpenAI, creator of Google Maps) founding a conversational AI company — expect rich identity claims about AI-native organizational design."
    }
  ]
}
```

**Step 3: Verify the update**

Run: `cat research/transcript-gap-queue.json | head -40`
Expected: See new schema fields (sourceId, leaderTitle, transcriptQuality, etc.)

**Step 4: Commit**

```bash
git add research/transcript-gap-queue.json
git commit -m "feat: expand transcript-gap-queue.json schema

Add: sourceId, leaderTitle, episodeDate, transcriptQuality,
transcriptAccess, aiRelevance, status, discoveredDate, scannedDate.
Rename: source -> sourceId, transcriptUrl -> episodeUrl

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 3: Create TRANSCRIPT-DISCOVERY-PROTOCOL.md

**Files:**
- Create: `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`

**Step 1: Write the protocol file**

```markdown
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
```

**Step 2: Verify file was created**

Run: `head -30 research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`
Expected: See the protocol header and purpose section.

**Step 3: Commit**

```bash
git add research/TRANSCRIPT-DISCOVERY-PROTOCOL.md
git commit -m "feat: create TRANSCRIPT-DISCOVERY-PROTOCOL.md

Shared protocol for systematic transcript discovery.
Referenced by both /research and /purpose-claims skills.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Update SESSION-PROTOCOL.md

**Files:**
- Modify: `research/SESSION-PROTOCOL.md`

**Step 1: Add Step 2b after the "Pre-Session Setup" section**

Insert after line 57 (after the Pre-Session Setup section):

```markdown
---

## Transcript Availability Check (Step 2b)

Before deep-scanning any podcast or interview source for a specimen:

1. **Check existing coverage:**
   - Read `research/transcript-gap-queue.json` for this specimen's leader(s)
   - If entries exist with `status: scanned`, the transcript has been processed

2. **If no entry exists, run quick discovery:**
   - Follow `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` Phase 1
   - Add any discovered sources to the queue

3. **Prioritize by access method:**
   - `transcriptAccess: programmatic` — scan these first, they're fetchable
   - `transcriptAccess: manual-required` — note in session file, add to queue for user

4. **Update after scanning:**
   - Set `status: scanned` and `scannedDate` for each transcript processed
   - Add any new sources discovered to `transcript-sources.json`

This step ensures we don't miss available transcripts and systematically track what's been scanned.

```

**Step 2: Verify the edit**

Run: `grep -n "Transcript Availability" research/SESSION-PROTOCOL.md`
Expected: Find "Transcript Availability Check (Step 2b)"

**Step 3: Commit**

```bash
git add research/SESSION-PROTOCOL.md
git commit -m "feat: add transcript availability check step to SESSION-PROTOCOL

Step 2b integrates TRANSCRIPT-DISCOVERY-PROTOCOL.md into research workflow.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 5: Update purpose-claims SKILL.md

**Files:**
- Modify: `.claude/skills/purpose-claims/SKILL.md`

**Step 1: Find the Step 1 section and update it**

Locate the "Step 1" section in the skill file and update it to reference the transcript discovery protocol.

The updated Step 1 should read:

```markdown
### Step 1: Check Transcript Availability

Follow `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md`:

1. **Read the queue:**
   - Check `research/transcript-gap-queue.json` for this specimen
   - Look for entries where `status: discovered` (not yet scanned)

2. **Run discovery if needed:**
   - If no entries exist OR entries are stale (>30 days old), run Phase 1 discovery
   - Use the search patterns from the protocol

3. **Prioritize sources:**
   - Native transcripts (programmatic) — highest value, scan first
   - Third-party transcripts — good quality, scan second
   - Auto-generated (YouTube) — queue for manual if high-priority specimen

4. **Update after scanning:**
   - Set `status: scanned` and `scannedDate` for each transcript processed
   - Claims found → add to `pending/[specimen-id].json`
```

**Step 2: Verify the edit**

Run: `grep -A 15 "Step 1:" .claude/skills/purpose-claims/SKILL.md`
Expected: See "Check Transcript Availability" section with protocol reference.

**Step 3: Commit**

```bash
git add .claude/skills/purpose-claims/SKILL.md
git commit -m "feat: update purpose-claims Step 1 to use transcript discovery protocol

References TRANSCRIPT-DISCOVERY-PROTOCOL.md for systematic source discovery.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 6: Update research SKILL.md

**Files:**
- Modify: `.claude/skills/research/SKILL.md`

**Step 1: Add reference to transcript discovery protocol**

After the SESSION-PROTOCOL.md cat command (line 21), add:

```markdown
## Transcript Discovery Protocol

!`cat "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/research/TRANSCRIPT-DISCOVERY-PROTOCOL.md"`
```

**Step 2: Verify the edit**

Run: `grep -n "TRANSCRIPT-DISCOVERY" .claude/skills/research/SKILL.md`
Expected: Find reference to the protocol file.

**Step 3: Commit**

```bash
git add .claude/skills/research/SKILL.md
git commit -m "feat: add transcript discovery protocol reference to research skill

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Validate and Final Commit

**Step 1: Run validation**

```bash
node scripts/validate-workflow.js
```
Expected: No errors related to new files.

**Step 2: Verify all files exist**

```bash
ls -la research/transcript-sources.json research/transcript-gap-queue.json research/TRANSCRIPT-DISCOVERY-PROTOCOL.md
```
Expected: All three files exist.

**Step 3: Update APP_STATE.md**

Add session log entry documenting the transcript discovery infrastructure implementation.

**Step 4: Final verification commit**

If any files were missed, add them:

```bash
git status
git add -A
git commit -m "chore: update APP_STATE.md with transcript discovery implementation

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Summary of Files Changed

| File | Action | Purpose |
|------|--------|---------|
| `research/transcript-sources.json` | Create | Source-level registry (13 sources seeded) |
| `research/transcript-gap-queue.json` | Modify | Expand schema with quality/status fields |
| `research/TRANSCRIPT-DISCOVERY-PROTOCOL.md` | Create | Shared discovery protocol |
| `research/SESSION-PROTOCOL.md` | Modify | Add Step 2b for transcript check |
| `.claude/skills/purpose-claims/SKILL.md` | Modify | Update Step 1 to reference protocol |
| `.claude/skills/research/SKILL.md` | Modify | Add protocol reference |
| `APP_STATE.md` | Modify | Document session changes |
