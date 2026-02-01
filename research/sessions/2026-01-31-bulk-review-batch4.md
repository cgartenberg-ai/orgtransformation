---
session_date: "2026-01-31"
session_type: "bulk-review"
batch: 4
batch_total: 4
source: "Bulk curation review — legacy specimens from convert-cases.js (batch 4/4)"
organizations_found:
  - id: schneider-electric
    status: existing
    curated: true
  - id: servier
    status: existing
    curated: true
  - id: shopify
    status: existing
    curated: true
  - id: siemens
    status: existing
    curated: true
  - id: snowflake
    status: existing
    curated: true
  - id: tencent
    status: existing
    curated: true
  - id: thinking-machines-lab
    status: existing
    curated: true
  - id: uk-government
    status: existing
    curated: true
  - id: walmart
    status: existing
    curated: true
  - id: waystar
    status: existing
    curated: true
---

# Bulk Curation Review — Batch 4 of 4

## Purpose

Batch 4 (final) of a bulk curation review for 42 legacy specimens (10 specimens).

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
| schneider-electric | Schneider Electric | Low | Medium |
| servier | Servier | Low | Medium |
| shopify | Shopify | Low | Medium |
| siemens | Siemens | Low | Medium |
| snowflake | Snowflake | Low | Medium |
| tencent | Tencent | Low | Medium |
| thinking-machines-lab | Thinking Machines Lab | Low | Medium |
| uk-government | UK Government | Low | Medium |
| walmart | Walmart | Low | Medium |
| waystar | Waystar | Low | Medium |

## Provenance

Synthetic session generated to close the pipeline gap. No new research data — curation works from existing specimen files.
