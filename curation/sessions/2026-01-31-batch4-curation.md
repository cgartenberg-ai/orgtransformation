# Curation Session: Batch 4 Bulk Review

**Date:** 2026-01-31
**Session file:** `research/sessions/2026-01-31-bulk-review-batch4.md`
**Curator:** Claude (Phase 2 automated curation)
**Specimens processed:** 10

## Summary

Final batch (4/4) of legacy specimen bulk curation review. All 10 specimens validated through decision tree, enriched with habitat data, observable markers, and classification rationales. Two specimens downgraded to Stub due to insufficient internal organizational data.

## Specimens Curated

### schneider-electric — Schneider Electric
- **Classification:** Model 4 (Hub-and-Spoke), Structural — validated
- **Changes:** Fixed industry to Energy Management. Removed spurious "hub-and-spoke" quote. Added habitat (Rueil-Malmaison HQ), observable markers, classification rationale.
- **Completeness:** Low

### servier — Servier
- **Classification:** Model 4 (Hub-and-Spoke), Structural — kept tentatively
- **Changes:** DOWNGRADED to Stub + Low confidence. Data describes external AI partnerships ($2B with Insilico Medicine and Iktos) rather than internal AI organizational structure. No evidence of internal AI hub, team, or CAIO.
- **Completeness:** Low (Stub)

### shopify — Shopify
- **Classification:** Model 3 (Embedded Teams), Contextual — validated
- **Changes:** Fixed industry to E-commerce. Added Mechanism #7 (Put Executives on the Tools — CEO Tobi Lutke mandate). Added employees (8,100), habitat (Ottawa HQ).
- **Completeness:** Low

### siemens — Siemens
- **Classification:** Model 4 (Hub-and-Spoke), Structural — validated
- **Changes:** Fixed industry to Industrial Technology. Added Mechanism #9 (Hire External AI Leader — Peter Koerte CTO, Nand Mulchandani from CIA CAIO, Usama Hasan from DeepMind). Added habitat (Munich HQ), observable markers.
- **Completeness:** Low

### snowflake — Snowflake
- **Classification:** Model 4 (Hub-and-Spoke), Structural — kept tentatively
- **Changes:** DOWNGRADED to Stub + Low confidence. Data primarily describes CEO Ramaswamy's commentary on industry trends ("Great Decentralization") rather than Snowflake's internal AI organizational structure. Added habitat (Bozeman HQ).
- **Completeness:** Low (Stub)

### tencent — Tencent
- **Classification:** Model 4 (Hub-and-Spoke), Structural — validated
- **Changes:** Fixed industry from Industrial to Technology. Added Mechanisms #6 (Merge Competing AI Teams — TEG and WeChat AI into Hunyuan Lab) and #9 (Hire External AI Leader). Added habitat (Shenzhen HQ), observable markers.
- **Completeness:** Low

### thinking-machines-lab — Thinking Machines Lab
- **Classification:** Model 1 (Research Lab), Structural — validated
- **Changes:** Added secondary Model 5 (Product/Venture Lab — Tinker fine-tuning product). Fixed orgSize from Enterprise to Startup. Company-as-lab edge case (like Recursion).
- **Completeness:** Low

### uk-government — UK Government
- **Classification:** Model 2 (CoE), Structural — validated
- **Changes:** Replaced Mechanism #5 (weakly evidenced) with Mechanism #9 (Hire External AI Leader — CAIO recruited from Spotify/Facebook). Added habitat, observable markers.
- **Completeness:** Low

### walmart — Walmart
- **Classification:** Model 5c (Platform-to-Product), Structural — validated
- **Changes:** Fixed industry from Technology to Retail. Added Mechanism #10 (Productize Internal Advantages — Route Optimization SaaS, GoLocal). Removed truncated quote. Added habitat (Bentonville HQ).
- **Completeness:** Low

### waystar — Waystar
- **Classification:** Model 3 (Embedded Teams), Contextual — validated
- **Changes:** Fixed industry from Automotive to Healthcare Technology. Removed spurious quote. Added habitat (Louisville HQ), observable markers.
- **Completeness:** Low

## Registry Impact

- **Model reclassifications:** None
- **Orientation changes:** None
- **Status changes:** servier Active→Stub, snowflake Active→Stub
- **New secondary models:** thinking-machines-lab added secondary Model 5

## Patterns Observed

1. **Partnership-only data problem:** Servier specimen illustrates how partnership announcements ($2B in AI deals) can look like organizational AI data but reveal nothing about internal structure.
2. **CEO commentary vs. org structure:** Snowflake specimen is primarily CEO thought leadership about industry trends, not evidence of internal AI organization.
3. **Company-as-lab pattern:** Thinking Machines Lab joins Recursion as a "company IS the lab" edge case where the entire org is the AI research function.
4. **Industry misclassification prevalence:** 4 of 10 specimens had wrong industries (Technology as default), continuing the pattern from earlier batches.
