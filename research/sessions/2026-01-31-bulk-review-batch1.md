---
session_date: "2026-01-31"
session_type: "bulk-review"
batch: 1
batch_total: 4
source: "Bulk curation review — legacy specimens from convert-cases.js (batch 1/4: High + Medium completeness)"
organizations_found:
  - id: google-x
    status: existing
    curated: true
  - id: bank-of-america
    status: existing
    curated: true
  - id: pg-chatpg
    status: existing
    curated: true
  - id: samsung-c-lab
    status: existing
    curated: true
  - id: abb
    status: existing
    curated: true
  - id: accenture-openai
    status: existing
    curated: true
  - id: adobe-firefly
    status: existing
    curated: true
  - id: allianz-anthropic
    status: existing
    curated: true
  - id: amazon-agi
    status: existing
    curated: true
  - id: bcg-trailblazers
    status: existing
    curated: true
---

# Bulk Curation Review — Batch 1 of 4

## Purpose

Batch 1 of a bulk curation review for 42 legacy specimens. This batch covers the High/Medium completeness specimens plus the first group of Low completeness specimens (10 total).

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
| google-x | Google X | High | High |
| bank-of-america | Bank of America | Medium | High |
| pg-chatpg | Procter & Gamble | Medium | High |
| samsung-c-lab | Samsung C-Lab | Medium | High |
| abb | ABB | Low | Medium |
| accenture-openai | Accenture + OpenAI | Low | Medium |
| adobe-firefly | Adobe | Low | Medium |
| allianz-anthropic | Allianz + Anthropic | Low | Medium |
| amazon-agi | Amazon | Low | Medium |
| bcg-trailblazers | BCG | Low | Medium |

## Provenance

Synthetic session generated to close the pipeline gap. No new research data — curation works from existing specimen files.
