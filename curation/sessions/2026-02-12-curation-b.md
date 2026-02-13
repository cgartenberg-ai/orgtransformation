# Curation Session: 2026-02-12-curation-b

**Date**: February 12, 2026
**Type**: New specimen creation from pending research outputs
**Sources processed**:
- `research/pending/healthcare-sector-deep-dive.json` (3 specimens)
- `research/pending/podcast-conference-sweep-feb-10.json` (1 specimen)
- `research/pending/podcast-deep-scan-feb-2026.json` (Tesla enrichment — already done, skipped)

---

## Specimens Created

| Specimen | Model | Secondary | Orientation | Confidence | Source |
|----------|-------|-----------|-------------|------------|--------|
| cedars-sinai | M4 Hub-and-Spoke | M1 Research Lab | Structural | Medium | healthcare-sector-deep-dive |
| mass-general-brigham | M4 Hub-and-Spoke | M5 Product/Venture Lab | Structural | Medium | healthcare-sector-deep-dive |
| kaiser-permanente | M4 Hub-and-Spoke | — | Contextual | Low | healthcare-sector-deep-dive |
| mckinsey | M4 Hub-and-Spoke | M2 Center of Excellence | Contextual | Medium | podcast-conference-sweep |

## Classification Reasoning

### Cedars-Sinai
- **Decision tree**: Formal AI unit? YES (CAIRE + CAIO office) → Publishes research? YES → Central team? YES (CAIO office) → Builds or enables? Both → M4
- **Key structural feature**: Dual-reporting CAIO — reports to CIO for operations AND CMO for clinical integration. This is healthcare's answer to the dual-authority problem.
- **Secondary M1**: CAIRE is a dedicated research center with its own mission
- **Guardrails checked**: G4 (prestige bias) — CAIRE is genuinely research-focused; G2 (federation) — single hub, not federation
- **AI Council** as cross-functional governance body is the healthcare equivalent of an AI steering committee

### Mass General Brigham
- **Decision tree**: Formal AI unit? YES (1,800+ digital staff under CDIO) → Central team? YES → Builds or enables? Both → M4
- **Key structural feature**: 1,800+ digital staff is genuinely one of the largest named digital orgs in healthcare. Not prestige inflation.
- **Secondary M5**: AIwithCare spinout commercializes clinical trial screening AI — rare for an academic medical center
- **Guardrails checked**: G4 (prestige bias) — 1,800 staff IS a large org; G7 (M5 vs M8) — spinout is adjacent commercialization, not core replacement
- **Research-to-product bridge**: Cross-functional team (clinicians + data scientists + PMs + TPMs + engineers) designed for translation

### Kaiser Permanente
- **Decision tree**: Formal AI unit? YES (CAIO role exists) → Central team? YES → M4
- **Key structural feature**: Dual-hat CMIO/CAIO — Ainsley MacLean holds both roles. The integrated payer-provider model creates a natural experiment vs. UnitedHealth's separated model.
- **Low confidence**: Thin data on org structure beyond the leadership role. No information on team size, reporting lines beyond CMIO/CAIO, or specific AI initiatives.
- **Contextual orientation**: AI embedded within existing clinical and operational workflows through the integrated model

### McKinsey
- **Decision tree**: Formal AI unit? YES (QuantumBlack) → Central team? YES → Builds or enables? Both → M4
- **Key structural feature**: 60K total "employees" — 40K humans + 25K AI agents. This is the first specimen where AI agents are counted as organizational members.
- **Secondary M2**: QuantumBlack (1,700 people) operates as the AI CoE within the hub-and-spoke
- **Guardrails checked**: G4 (prestige bias) — QuantumBlack at 40% of revenue is genuine structural significance, not just a prestigious label
- **Note**: Distinct from existing `mckinsey-quantumblack` (M5c, focuses on QuantumBlack as a productized capability) and `mckinsey-workforce` (M6a Stub, workforce transformation data). This specimen captures the full organizational picture with the 25K AI agents data.

## Cross-Cutting Patterns

1. **Healthcare M4 convergence**: All 3 new healthcare specimens are M4 Hub-and-Spoke. Combined with existing Mayo Clinic, Mount Sinai, Sutter Health, CVS Health, UnitedHealth Group — healthcare is overwhelmingly M4. The sector-specific variant features clinical governance layers (AI Councils, informatics officers, dual-reporting) that don't exist in other sectors.

2. **Dual-authority governance in healthcare**: Both Cedars-Sinai (dual-reporting CAIO → CIO + CMO) and Kaiser (dual-hat CMIO/CAIO) solve the same problem differently: healthcare AI requires both technical AND clinical authority. This is the healthcare-specific version of the centralization-vs-decentralization tension (T3).

3. **Academic-to-commercial bridge**: Mass General Brigham's AIwithCare spinout mirrors a Silicon Valley structural pattern (research → spinout → commercial entity) transplanted to academic medicine. This connects to Mechanism #10 (Productize Internal Advantages).

4. **AI agents as organizational members**: McKinsey's 25K AI agents counted alongside 40K humans is the first specimen to explicitly treat AI agents as part of the organizational headcount. This is a structural signal, not just a deployment metric — it implies agents are governed, managed, and allocated like human resources.

## Taxonomy Feedback

- Healthcare's dual-authority governance (CIO for tech + CMO for clinical) may deserve recognition as a healthcare-specific M4 sub-type. The structural pattern is consistent but distinct from tech/financial services M4.
- QuantumBlack at 40% of McKinsey's revenue challenges typical M2 classification — it has outgrown the "center of excellence" container and is closer to the core business engine. Professional services AI units may need separate treatment.
- The payer-provider split (Kaiser integrated vs. UnitedHealth separated) is a natural experiment on unified vs. separated AI governance. Worth tracking as a research priority.

## Registry Impact

- **Total specimens**: 143 → 147
- **M4 count**: 62 → 66 (+4)
- **Structural**: 95 → 97 (+2: Cedars-Sinai, MGB)
- **Contextual**: 43 → 45 (+2: Kaiser, McKinsey)
- **Synthesis queue**: 4 new pending entries
