---
session_date: "2026-01-31"
session_type: "bulk-review"
batch: 3
batch_total: 4
source: "Bulk curation review — legacy specimens from convert-cases.js (batch 3/4)"
organizations_found:
  - id: mckinsey-quantumblack
    status: existing
    curated: true
  - id: mckinsey-workforce
    status: existing
    curated: true
  - id: mercado-libre
    status: existing
    curated: true
  - id: moderna
    status: existing
    curated: true
  - id: novo-nordisk
    status: existing
    curated: true
  - id: palo-alto-networks
    status: existing
    curated: true
  - id: pfizer
    status: existing
    curated: true
  - id: recursion
    status: existing
    curated: true
  - id: roche-genentech
    status: existing
    curated: true
  - id: sanofi
    status: existing
    curated: true
  - id: sap
    status: existing
    curated: true
---

# Bulk Curation Review — Batch 3 of 4

## Purpose

Batch 3 of a bulk curation review for 42 legacy specimens (11 specimens).

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
| mckinsey-quantumblack | McKinsey / QuantumBlack | Low | Medium |
| mckinsey-workforce | McKinsey | Low | Medium |
| mercado-libre | Mercado Libre | Low | Medium |
| moderna | Moderna | Low | Medium |
| novo-nordisk | Novo Nordisk | Low | Medium |
| palo-alto-networks | Palo Alto Networks | Low | Medium |
| pfizer | Pfizer | Low | Medium |
| recursion | Recursion Pharmaceuticals | Low | Medium |
| roche-genentech | Roche / Genentech | Low | Medium |
| sanofi | Sanofi | Low | Medium |
| sap | SAP | Low | Medium |

## Provenance

Synthetic session generated to close the pipeline gap. No new research data — curation works from existing specimen files.
