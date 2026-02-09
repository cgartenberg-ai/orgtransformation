# Purpose Claims Session: Feb 7, 2026 — Batch 6 (Financial Services + Consumer Goods)

## Specimens Scanned
- commonwealth-bank: 13 claims (rich)
- wells-fargo: 8 claims (rich)
- bank-of-america: 14 claims (rich)
- pg-chatpg: 9 claims (rich)

**Total: 44 new claims. Registry now at 248 claims across 25 specimens.**

## Batch Design Rationale

Batch 6 was designed as a financial services mini-batch (3 banks + 1 consumer goods for variety) to test whether UBS patterns from Batch 5 generalize across financial services. Three major banks (Commonwealth Bank, Wells Fargo, Bank of America) plus P&G/ChatPG as a consumer goods counterpoint.

## Claims Found

### commonwealth-bank (13 claims)
Matt Comyn dominates (11 of 13 claims). Key themes:
- "Tomorrow's bank today" as persistent transformation tagline bridging identity and teleology
- CEO-as-early-adopter: Comyn explicitly names "role modeling" as a mechanism for organizational adoption
- Sacrifice narrative delegated to anonymous spokesperson — CEO never publicly acknowledges job displacement
- AI framed as cornerstone of competitive positioning AND customer experience simultaneously
- Seattle Tech Hub signals global talent competition (not just domestic deployment)

### wells-fargo (8 claims)
Charlie Scharf's rhetoric is distinctively candid on sacrifice:
- "Anyone who says they don't think they'll have less headcount because of AI either doesn't know what they're talking about or is just not being totally honest" — radical candor as legitimation
- Three-part sacrifice argument: (1) headcount will shrink, (2) we'll manage via attrition, (3) the alternative (hire-then-fire) is crueler
- Van Beurden appointment defines M4 hub-and-spoke governance: business leaders own transformation, AI head is accountability mechanism
- 22 consecutive quarters of headcount reduction (275K→210K since 2019) — AI accelerates existing trajectory

### bank-of-america (14 claims)
Brian Moynihan's claims cluster heavily around identity:
- "Responsible growth" as master strategic mantra constraining AI deployment
- "Augmented intelligence" (not AI) as deliberate terminological choice embedding human-in-the-loop as identity
- Unusually specific on displacement: "We've taken 30% out of the coding part of the stream. That saves us about 2,000 people."
- Transformation narrative is acquisitions-to-organic-growth, not legacy-to-digital — AI nested inside longer pivot story
- "We don't need additional regulation about AI" — self-regulation through existing liability frameworks

### pg-chatpg (9 claims)
P&G is notably CIO-centric rather than CEO-centric:
- Vittorio Cretella (CIO) carries the transformational narrative, not Jon Moeller (CEO)
- Marc Pritchard (CBO): "Don't talk about the algorithms, don't talk about the technology, don't talk about AI… Talk about the outcome you want." — anti-technology framing from senior leader
- "AI-first business" as identity claim + conditional employee deal ("augment, not replace — providing we combine human skills with machines")
- Zero sacrifice-justification claims despite 7,000 nonmanufacturing role reductions in same period — notable silence

## Analytical Notes

### New Patterns

**#22: Financial services CEOs anchor purpose in fiduciary gravity.** Moynihan ("if I turn down your loan, that's a life-changing experience"), Comyn ("responsible AI"), Scharf (explicitly naming headcount impact). Banking claims invoke the weight of financial decisions on real people's lives to justify caution — a legitimacy source unavailable to tech firms.

**#23: Sacrifice candor varies enormously across financial services.** Scharf (Wells Fargo) is the most candid CEO on AI-driven job loss in the entire collection. Moynihan (BofA) quantifies displacement but hedges the growth promise. Comyn (CBA) delegates sacrifice rhetoric to an anonymous spokesperson. This is a spectrum from radical transparency to institutional deflection.

**#24: CIO-as-purpose-carrier is structurally interesting.** P&G's Cretella carries the transformation narrative because Moeller's style is pragmatic/sparse. This is unusual — most specimens show the CEO as primary purpose-claim source. May reflect P&G's decentralized model where the CIO has genuine authority.

**#25: "Augmented intelligence" as identity-embedding terminology.** BofA's deliberate rebranding from "AI" to "augmented intelligence" embeds human-in-the-loop as organizational identity, not just process design. This is a linguistic mechanism for managing the employee deal.

### Pentagon-CDAO Removal

Removed pentagon-cdao (18 claims) from the registry. Rationale: political entity, not corporate. Political rhetoric (national security framing, duty language, taxpayer accountability) operates on fundamentally different authorization mechanisms than corporate purpose claims. Pentagon suppliers (Palantir, Anduril) remain valid specimens. Scan-tracker marked as `"quality": "excluded"`.

### Updated Hypotheses

- **H1 (industry moderates model-claim)**: Further strengthened. Financial services now has 5 specimens with clearly distinct patterns from tech and pharma.
- **H5 (operations-heavy firms anchor in efficiency)**: Extended to banking — Scharf's rhetoric is more UPS-like than tech-like.
- **H6 (new)**: Sacrifice candor is CEO-specific, not industry-determined. Within the same industry (financial services), Scharf is radically candid while Comyn deflects to institutional voice.
- **H7 (new)**: The identity of the "purpose carrier" (CEO vs. CIO vs. other) varies by organization and may reflect governance structure.

## Visualization Work

Also in this session: built two exploratory visualization views for the Purpose Claims Browser:
1. **Heatmap Matrix**: Specimens (rows, grouped by model) × 7 claim types (columns), cell intensity = count
2. **Specimen Dot Map**: Mini stacked horizontal bars per specimen, grouped by model or industry

Both views are pure Tailwind CSS (no D3), integrated as new view modes in the existing browser toggle.

## Next Steps

- Batch 7 candidates: Pick from remaining unscanned specimens, possibly pharma (Moderna, Recursion) or tech (Nvidia, Tesla, Databricks)
- Consider scanning Palantir and/or Anduril as Pentagon supplier counterpoints
- Use heatmap and dot map to identify claim-type gaps that need more specimens
