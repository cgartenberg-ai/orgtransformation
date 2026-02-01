# Curation Session: Batch 2 Bulk Review

**Date:** 2026-01-31
**Session file:** `research/sessions/2026-01-31-bulk-review-batch2.md`
**Specimens processed:** 11

## Summary Table

| Specimen | Previous | After | Action | Confidence | Key Changes |
|---|---|---|---|---|---|
| bosch-bcai | Model 4, Structural | Model 4, Structural | Validated | Medium | Fixed industry to Industrial Technology; removed spurious quote; added habitat |
| bytedance | Model 5c, Structural | Model 5c, Structural | Validated | Medium | Added sector, habitat, tension positions |
| dai-nippon-printing | Model 2, Structural | **Model 3, Contextual** | **Reclassified** | Medium | Targeted embedding, not a CoE; removed weak mechanism |
| deloitte | Model 5c, Structural | **Model 2, Structural** | **Reclassified + Stub** | Low | Data is research findings, not Deloitte's own org; downgraded to Stub |
| duolingo | Model 3, Contextual | Model 3, Contextual | Validated | Medium | Added EdTech sector; Mechanism #4; removed spurious quote |
| google-deepmind | Model 1, Structural | Model 1 **+ secondary 4**, Structural | **Enriched** | Medium | Brain+DeepMind merger = Mechanism #6; hub coordination function |
| hyundai-robotics | Model 1, Structural | Model 1, Structural | Validated | Medium | Fixed industry from Robotics to Automotive/Mobility |
| ig-group | Model 3, Contextual | Model 3, Contextual | Validated | **Low** | Fixed industry from Automotive to Financial Services; downgraded confidence (single source) |
| jpmorgan | Model 4, Structural | Model 4, Structural | Validated | **High** | Fixed industry to Financial Services; strengthened Mechanism #5; added #7; upgraded confidence |
| klarna | Model 6a, Contextual | Model 6a, Contextual | Validated | Medium | Fixed industry to Fintech; added Mechanism #3 (reversal case) |
| lg-electronics | Model 4, Contextual | **Model 2, Structural** | **Reclassified** | Medium | AX Center is a renamed CoE, not hub-and-spoke |

## Reclassifications (4)

### dai-nippon-printing: Model 2 -> Model 3
DNP deployed ChatGPT Enterprise through targeted embedding in specific business units (ICT R&D for patent research, data architecture). The description explicitly states they "avoided broad, low-impact deployments in favor of targeted high-value applications." This is the Embedded Teams pattern, not a centralized CoE.

### deloitte: Model 5c -> Model 2 (+ Stub)
Critical issue: the specimen data describes Deloitte's RESEARCH FINDINGS about agentic AI adoption across industries, NOT Deloitte's own organizational structure. The 30%/38%/14%/11% figures are survey data about Deloitte's clients. Downgraded to Stub; needs fundamental rework with sources about Deloitte's actual internal AI structure.

### google-deepmind: Added secondary Model 4
Google DeepMind remains fundamentally a Research Lab (Model 1), but the Brain+DeepMind consolidation created a hub function (secondary Model 4) that coordinates research-to-product pipeline across Google. Added Mechanism #6 (Merge Competing AI Teams) with strong evidence.

### lg-electronics: Model 4 -> Model 2
The AX Center is a renamed DX organization -- a centralized entity providing AI transformation capability to business units. This is the CoE pattern (Model 2), not Hub-and-Spoke (Model 4). Hub-and-Spoke implies distributed spokes with AI capabilities; here the data only shows a central unit with a mandate.

## Industry Corrections (5)

| Specimen | Was | Now |
|---|---|---|
| bosch-bcai | Automotive | Industrial Technology |
| hyundai-robotics | Robotics | Automotive/Mobility |
| ig-group | Automotive | Financial Services |
| jpmorgan | Technology | Financial Services |
| klarna | Technology | Financial Services/Fintech |

## Taxonomy Feedback

1. **Professional services conflation (systemic):** Deloitte specimen conflates research findings with organizational structure -- same issue noted in BCG (batch 1). Need clear guidance for curators on separating advisory firm research output from their own organizational structure.

2. **Model 2 vs Model 4 distinction:** LG Electronics case highlights that a centralized unit with a mandate (CoE) is different from a hub distributing capability to embedded spokes (Hub-and-Spoke). The distinguishing factor is whether the "spokes" have their own AI capabilities or just receive services from the center.

## Edge Cases

- **Klarna as cautionary case:** Valuable specimen showing the limits of pure AI substitution. CEO-driven full-tilt AI adoption followed by public reversal. Assigned Mechanism #3 (willingness to kill projects) for the organizational courage to reverse.
- **JPMorgan as strong Model 4:** Textbook hub-and-spoke with high confidence. 250K employee deployment + 8-week cycles in a regulated industry is remarkable.
- **Duolingo Mechanism #4:** Assigned Consumer-Grade UX mechanism for Birdbrain/GPT-4 features. While consumer-facing rather than employee-facing, demonstrates the principle of making AI delightful to use.

## Counts

- **Validated:** 7 (bosch-bcai, bytedance, duolingo, hyundai-robotics, ig-group, jpmorgan, klarna)
- **Reclassified:** 4 (dai-nippon-printing, deloitte, google-deepmind, lg-electronics)
- **Confidence upgrades:** 1 (jpmorgan: Medium -> High)
- **Confidence downgrades:** 2 (deloitte: Medium -> Low, ig-group: Medium -> Low)
- **Status changes:** 1 (deloitte: Active -> Stub)
