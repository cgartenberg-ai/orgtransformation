# Batch 11: M4 Hub-and-Spoke Purpose Claims
**Date:** 2026-02-12
**Registry before:** 1,082 claims | **After:** 1,142 claims (+60)

## Specimens Scanned

| Specimen | Claims | Quality | Distribution |
|----------|--------|---------|--------------|
| thomson-reuters | 16 | Rich | commercial-success:8, utopian:4, survival:3, identity:3, higher-calling:1 |
| deere-and-co | 14 | Rich | commercial-success:5, utopian:3, higher-calling:2, identity:2, survival:2 |
| unitedhealth-group | 16 | Rich | identity:6, teleological:5, higher-calling:2, commercial-success:2, survival:1 |
| delta-air-lines | 14 | Rich | identity:7, higher-calling:3, utopian:2, commercial-success:2, survival:1 |

## Batch Theme: M4 Hub-and-Spoke Rhetorical Registers

All 4 specimens are M4 (Hub-and-Spoke) across different industries. This batch tests whether hub-and-spoke leaders use distinctive rhetorical registers.

### Key Finding: Industry > Structure for Rhetoric

The rhetorical registers vary dramatically despite shared structural model:

1. **Thomson Reuters (Legal Tech/Media)**: Heavy commercial-success (8/16). AI is both product and production method. Claims center on competitive positioning ("professional-grade AI"), content moats, and M&A-as-learning. Most commercially oriented of the four.

2. **Deere & Co (Agriculture)**: Balanced with notable higher-calling presence. "Purpose-driven technology" and "feeding the world" frames anchor the rhetoric. Labor shortage serves as primary legitimation mechanism — AI fills demographic gaps, not displaces workers. Distinctive rhetorical cascade from CEO to product managers.

3. **UnitedHealth Group (Healthcare)**: Identity-dominant (6/16) + teleological (5/16). Defensive identity claims dominate — "AI is never used to deny a claim" — reflecting governance controversy. Healthcare system as "maze" that AI navigates. Most defensive rhetoric in the collection.

4. **Delta Air Lines (Airlines)**: Identity-dominant (7/14) with higher-calling (3/14). "Augmented intelligence" philosophy is the anchor — AI empowers humans, doesn't replace them. "The entire point of innovation is to lift people up." Most human-centered rhetoric of the four.

### Analytical Pattern: Defensive vs. Aspirational Identity

The batch reveals a spectrum from aspirational to defensive identity claims:
- **Aspirational**: Deere ("purpose-driven technology"), Delta ("lift people up")
- **Defensive**: UnitedHealth ("AI is never used to deny a claim"), Thomson Reuters (competitive positioning)

This aligns with the hypothesis that governance controversy (UHG) and competitive pressure (TR) produce more defensive purpose framing, while customer-facing brands (Delta, Deere) lean aspirational.

## Technical Notes

- **Agent model:** Opus (all 4)
- **Concurrency:** 4 agents launched simultaneously
- **Completion:** 3/4 completed in ~10 min. Delta agent hung on McKinsey.com WebFetch (known failure pattern). Killed and re-launched with McKinsey excluded — completed in ~15 min.
- **Total search queries:** 24 (6 per specimen)
- **Total URLs fetched:** 23 (6+6+5+6)
- **Fetch failures:** entrepreneur.com (404), acuitymag.com (403), businesschief.com (403), aibusiness.com (403)
- **Merge script:** `scripts/merge-batch11-claims.py`

## Updated Memory Note

Added to blocked domains: McKinsey.com hangs on WebFetch (not just CSS-only as previously noted — can hang indefinitely, requiring agent kill). Must be explicitly excluded in agent prompts.
