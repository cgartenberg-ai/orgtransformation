---
session_date: "2026-01-31"
sessions_processed: ["2026-01-31-bulk-review-batch1.md"]
specimens_created: []
specimens_updated: ["google-x", "bank-of-america", "pg-chatpg", "samsung-c-lab", "abb", "accenture-openai", "adobe-firefly", "bcg-trailblazers"]
specimens_reclassified: ["allianz-anthropic", "amazon-agi"]
---

# Curation Session: 2026-01-31 (Batch 1 Bulk Review)

## Summary
Processed 1 research session (bulk review batch 1/4) containing 10 existing specimen reviews. Updated 8 specimens with validation layers and enriched data. Reclassified 2 specimens based on decision tree walk.

## Specimens Created/Updated
| Organization | Action | Model | Orientation | Confidence | Completeness | Notes |
|---|---|---|---|---|---|---|
| Google X | Validated | 5b (Venture Builder) | Structural | High | High | Type specimen confirmed. No changes needed. |
| Bank of America | Validated | 6a (Enterprise-Wide) | Contextual | High | Medium | Type specimen confirmed. Added revenue. |
| Procter & Gamble | Validated | 6b (Centralized-but-Unnamed) | Contextual | High | Medium | Type specimen confirmed. Added employees/revenue. |
| Samsung C-Lab | Validated | 7 (Tiger Teams) | Temporal | High | Medium | Type specimen confirmed. Added employees/revenue/geography. |
| ABB | Validated | 4 (Hub-and-Spoke) | Structural | Medium | Low | Fixed industry to Industrial Automation. Added habitat, contingencies, tensions. |
| Accenture + OpenAI | Reviewed | 2 (CoE) | Contextual | Low | Low | Confidence downgraded. Noted tension with Model 6a. Added Mechanism #7. Fixed industry. |
| Adobe | Validated | 5a (Internal Incubator) | Structural | Medium | Low | Replaced weak Mechanism #1 with strong #8 (Content Credentials). Added habitat, contingencies, tensions. |
| Allianz + Anthropic | Reclassified | 6a (Enterprise-Wide) | Contextual | Low | Low | Was Model 2 (CoE). Fixed industry to Insurance. Separated Anthropic/Allianz data. Added Mechanism #8. |
| Amazon | Reclassified | 4 (Hub-and-Spoke) + Model 1 | Structural | Medium | Low | Was Model 1 (Research Lab). Fixed industry to Technology. Added Mechanism #6. |
| BCG | Reviewed | 2 (CoE) | Contextual | Medium | Low | Fixed industry to Professional Services. Noted specimen conflates research findings with org structure. |

## Reclassifications
| Organization | Old Classification | New Classification | Rationale |
|---|---|---|---|
| Allianz + Anthropic | Model 2 (CoE), Contextual | Model 6a (Enterprise-Wide), Contextual | No evidence of formal CoE at Allianz. Claude deployed to all employees = enterprise-wide adoption pattern. |
| Amazon | Model 1 (Research Lab), Structural | Model 4 (Hub-and-Spoke) + secondary Model 1, Structural | AGI org under DeSantis unites research + chips + quantum as hub; AWS AI services are execution spokes. Not purely a research lab. |

## Taxonomy Feedback
- **Partnership specimens** (Accenture+OpenAI, Allianz+Anthropic) conflate vendor capabilities with customer organizational structure. Future research should separate these.
- **Professional services firms** (Accenture, BCG) present a meta-classification challenge: they both deploy AI internally and function as external AI enablers.
- **Model 5a/3 boundary**: Adobe Firefly tests whether products incubated separately but later integrated into existing products should be 5a (incubation origin) or 3 (current embedded state).
- **Model 1/4 boundary**: Amazon's AGI org shows how research labs embedded in larger product-oriented organizations may be better classified as hubs (Model 4) with research lab secondaries.
- **ABB's distributed Model 4**: The "Engineer to Autonomy" philosophy pushes toward the distributed end of hub-and-spoke, which may warrant further taxonomy attention.

## Type Specimens Identified
All 4 existing type specimens (google-x, bank-of-america, pg-chatpg, samsung-c-lab) were validated and confirmed.

## Edge Cases
- **Accenture+OpenAI**: Could be Model 2 (advisory role) or Model 6a (40K license deployment). Classification depends on whether you're classifying Accenture's advisory function or its internal adoption.
- **BCG Trailblazers**: Specimen conflates cross-industry research findings with BCG's own organizational structure. The "Trailblazer" pattern is a synthesis finding, not a single-org specimen.
- **Adobe Firefly**: If Firefly teams have been absorbed into product engineering, the specimen may need future reclassification from 5a to 3.

## Sessions Processed
- `2026-01-31-bulk-review-batch1.md` — Bulk curation review of 10 legacy specimens (4 High/Medium completeness type specimens + 6 Low completeness auto-converted specimens)
