---
session_date: "2026-01-31"
session_type: "bulk-review"
batch: 2
batch_total: 4
source: "Bulk curation review — legacy specimens from convert-cases.js (batch 2/4)"
organizations_found:
  - id: bosch-bcai
    status: existing
    curated: true
  - id: bytedance
    status: existing
    curated: true
  - id: dai-nippon-printing
    status: existing
    curated: true
  - id: deloitte
    status: existing
    curated: true
  - id: duolingo
    status: existing
    curated: true
  - id: google-deepmind
    status: existing
    curated: true
  - id: hyundai-robotics
    status: existing
    curated: true
  - id: ig-group
    status: existing
    curated: true
  - id: jpmorgan
    status: existing
    curated: true
  - id: klarna
    status: existing
    curated: true
  - id: lg-electronics
    status: existing
    curated: true
---

# Bulk Curation Review — Batch 2 of 4

## Purpose

Batch 2 of a bulk curation review for 42 legacy specimens (11 specimens).

## Instructions for Curation

For each specimen listed below:

1. **Read the existing specimen file** at `specimens/{id}.json`
2. **Validate the classification** — walk the decision tree from scratch
3. **Add a "Curation Review" layer** to the top of the `layers` array
4. **Check source URLs** — ensure all sources have URLs where possible
5. **Assess completeness honestly** — downgrade to "Stub" if data is thin
6. **Fill in null fields** where existing specimen data supports it
7. **Add to synthesis queue** when done

## Specimens for Review

| ID | Name | Current Completeness | Current Confidence |
|---|---|---|---|
| bosch-bcai | Bosch | Low | Medium |
| bytedance | ByteDance Volcano Engine | Low | Medium |
| dai-nippon-printing | Dai Nippon Printing | Low | Medium |
| deloitte | Deloitte | Low | Medium |
| duolingo | Duolingo | Low | Medium |
| google-deepmind | Google DeepMind | Low | Medium |
| hyundai-robotics | Hyundai Motor Group | Low | Medium |
| ig-group | IG Group | Low | Medium |
| jpmorgan | JPMorgan Chase | Low | Medium |
| klarna | Klarna | Low | Medium |
| lg-electronics | LG Electronics | Low | Medium |

## Provenance

Synthetic session generated to close the pipeline gap. No new research data — curation works from existing specimen files.
