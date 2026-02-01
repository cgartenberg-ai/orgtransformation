---
session_date: "2026-01-31"
sessions_processed: ["2026-01-31-bulk-review-batch3.md"]
specimens_created: []
specimens_updated: ["mckinsey-quantumblack", "mercado-libre", "moderna", "palo-alto-networks", "pfizer", "recursion", "roche-genentech", "sanofi", "sap"]
specimens_reclassified: ["mckinsey-workforce", "novo-nordisk"]
---

# Curation Session: 2026-01-31 (Batch 3)

## Summary
Processed 1 research session (bulk-review-batch3) containing 11 organization references.
Created 0 new specimens. Updated 9 existing specimens. Reclassified 2 specimens.

## Specimens Created/Updated
| Organization | Action | Model | Orientation | Confidence | Completeness | Notes |
|---|---|---|---|---|---|---|
| McKinsey / QuantumBlack | Updated | 5c + 2 | Structural | Medium | Low | Added secondary Model 2 (CoE). Fixed industry to Professional Services. Added Mechanism #10. |
| McKinsey (Workforce) | Reclassified | 6a | Contextual | Low | Low (Stub) | Model 2 → Model 6a. Describes workforce impact, not AI org structure. |
| Mercado Libre | Updated | 4 | Structural | Medium | Low | Fixed industry to E-commerce. Added Mechanism #7 (founder-as-hub). |
| Moderna | Updated | 6a | Contextual | Medium | Low | Fixed industry to Pharmaceuticals. Added Mechanism #5. Removed spurious quote. |
| Novo Nordisk | Reclassified | 4 | Structural | Medium | Low | Orientation: Contextual → Structural (300-person hub is structural separation). Added Mechanism #5. |
| Palo Alto Networks | Updated | 3 | Contextual | Medium | Low | Removed weak Mechanism #4. Added sector, habitat. |
| Pfizer | Updated | 4 | Structural | Medium | Low | Replaced Mechanism #5 with #3 (PACT partnership). Added habitat. |
| Recursion | Updated | 1 | Structural | Medium | Low | Edge case: entire company is the AI lab. Removed weak mechanism and spurious quote. |
| Roche / Genentech | Updated | 1 | Structural | Medium | Low | Fixed industry from Technology to Pharmaceuticals. Replaced Mechanism #5 with #3 (Lab in a Loop). |
| Sanofi | Updated | 4 | Structural | Medium | Low | Added habitat data and classification rationale. |
| SAP | Updated | 4 | Structural | Medium | Low | Fixed industry to Enterprise Software. Removed spurious quote. Added habitat. |

## Reclassifications
| Organization | Old Classification | New Classification | Rationale |
|---|---|---|---|
| McKinsey (Workforce) | Model 2 (CoE), Contextual | Model 6a (Enterprise-Wide), Contextual | Data describes workforce transformation impact, not a CoE structure. QuantumBlack specimen captures the structural AI approach. |
| Novo Nordisk | Model 4, Contextual | Model 4, Structural | The 300-person Enterprise AI hub is a distinct structural unit with its own CAIO reporting line. Structural separation is the primary organizing principle, despite mass Copilot deployment having contextual elements. |

## Taxonomy Feedback
- **Acquisition-driven AI capability building** (QuantumBlack): Buy-vs-build path is underrepresented in taxonomy. The F1→enterprise pipeline is distinctive.
- **Dual Product/CoE role** in professional services: 5c + 2 combination may warrant a specific sub-type.
- **Founder-as-hub** (Mercado Libre): Distinctive variant of Hub-and-Spoke where founder role change provides central coordination.
- **AI FOR development vs AI AS the product** (Palo Alto Networks): Model 3 may be too broad — covers both developer tool adoption and AI-in-product cases.
- **Company-as-lab edge case** (Recursion): Model 1 assumes lab is WITHIN a larger org. AI-native companies blur this.
- **Lab in a Loop** (Roche): Tight compute-wet lab cycles create structural separation with forced integration — a tension management pattern.
- **Enterprise software platform Hub-and-Spoke** (SAP): Variant specific to platform companies building AI centrally for dozens of product lines.
- **Workforce impact specimens**: mckinsey-workforce captures AI's effect on work composition, not AI organizational structure. Consider whether such specimens belong in herbarium or separate collection.

## Type Specimens Identified
None newly identified. Novo Nordisk flagged as strong Model 4 type specimen candidate if more source depth is added.

## Edge Cases
- **Recursion**: The entire company IS an AI research lab. Model 1 fits but the taxonomy assumes labs exist within larger organizations.
- **McKinsey (Workforce)**: Specimen captures workforce impact patterns, not structural AI arrangements. Borderline case for inclusion.
- **Palo Alto Networks**: Captures developer AI tool adoption (AI for development productivity) rather than AI integration into the product (cybersecurity). These are structurally different.

## Sessions Processed
- `2026-01-31-bulk-review-batch3.md` — Bulk curation review of 11 legacy specimens
