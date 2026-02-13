---
session_date: "2026-02-12"
type: "taxonomy-audit"
specimens_reclassified: ["amazon-agi", "meta-ai", "nvidia", "bosch-bcai", "google-ai-infra", "wells-fargo", "pentagon-cdao", "sap", "cvs-health", "kaiser-permanente", "apple", "salesforce", "servicenow", "mckinsey", "accenture-openai", "netflix", "uber", "nike", "fedex"]
specimens_flagged_for_enrichment: ["hp-inc", "abb", "siemens", "coca-cola"]
specimens_kept_m4: ["eli-lilly", "pfizer", "novo-nordisk", "sanofi", "servier", "bmw", "ford", "general-motors", "honda", "mercedes-benz", "toyota", "mayo-clinic", "mount-sinai-health-system", "sutter-health", "unitedhealth-group", "cedars-sinai", "mass-general-brigham", "jpmorgan", "morgan-stanley", "bloomberg", "visa", "honeywell", "deere-and-co", "lockheed-martin", "kroger", "lowes", "thomson-reuters", "disney", "panasonic", "schneider-electric", "t-mobile", "nokia", "intel", "atlassian", "cognizant", "publicis-groupe", "mercado-libre", "pepsico", "travelers", "ulta-beauty", "microsoft", "tencent", "delta-air-lines"]
borderline_kept_m4: ["microsoft", "tencent", "delta-air-lines", "ulta-beauty"]
protocol_changes: ["New decision tree step 5 (shared infrastructure test)", "New Guardrail 8 (Hub vs. Enterprise Deployment)", "Updated classification-quick-ref.md M4 one-line test"]
---

# M4 Taxonomy Audit Session: 2026-02-12

## Problem Statement

M4 (Hub-and-Spoke) had grown to 66 of 147 specimens (45%) — nearly half the collection. A model that captures half of all specimens has lost its discriminatory power. This was flagged in Session 18 (HANDOFF item #36): "The decision tree is too permissive. All 65+ M4 specimens need audit with tighter criteria."

## Root Cause

The decision tree's fatal branch was Step 4:

```
Does central team BUILD products or ENABLE others?
└─ BUILD → Are outputs new products/companies?
   └─ NO → Model 4 (Hub-and-Spoke)
```

Almost every large enterprise has SOME central AI team that builds SOMETHING that isn't a standalone product. The tree routed all of these to M4 without asking the discriminating question: **Does the hub coordinate shared infrastructure that distributed units depend on and build upon?**

## The Discriminating Question

True M4 requires:
1. A central hub that builds **shared AI infrastructure** (platform, models, standards)
2. **3+ semi-autonomous spokes** that build domain-specific AI applications on that infrastructure
3. **Bidirectional coordination**: hub→spokes (infrastructure/standards); spokes→hub (domain requirements/data)

False M4 patterns:
- Central team + mass deployment = M2+M6a
- Research lab + independent product teams = M1+M3
- AI product embedded in platform + enterprise mandate = M5+M6a
- CoE that sets standards + embedded teams that build independently = M2+M3

## Insights That Informed Reclassification

| Insight | How It Informed the Audit |
|---------|---------------------------|
| pharma-hub-and-spoke-divergence | Confirmed pharma M4s are genuine (exploration hubs). Revealed finance M4 "hubs" that serve deployment/governance are CoEs, not true hub-spoke. |
| automotive-m4-uniformity | Confirmed all 6 auto M4s are genuine — hub coordinates shared AI infra, BUs build domain apps. |
| anti-caio-thesis | Several anti-CAIO specimens (CVS, Goldman, Bloomberg, Visa) were M4. CVS reclassified to M6a; Bloomberg/Visa kept M4 (genuine research hub). |
| caio-failure-industrial-context | GM's CAIO departure → embedded AI suggests M3+M4 rather than pure M4. |
| modularity-predicts-ai-structure | Modular architectures → M6a/M9; integral architectures → M4/M3. Cross-check: software-first companies less likely to be true M4. |
| ai-team-consolidation-arc | Big Tech "M4s" are really post-consolidation parallel structures (M1+M3), not hub-spoke coordination. |
| services-business-model-crisis | Accenture's restructuring is business model transformation (M6a+M5), not AI hub-spoke. |
| contextual-via-education | FedEx pursues contextual ambidexterity via training (M2+M6a), not hub-spoke structural separation. |
| retail-no-caio-pattern | Nike, PepsiCo, Ulta deploy AI without hub-spoke infrastructure seen in pharma/auto. |

## Reclassifications (19 specimens)

| Specimen | Old | New | Key Evidence |
|----------|-----|-----|-------------|
| amazon-agi | M4+M1 | M1+M3 | AGI org is consolidated research; product teams embed AI independently |
| meta-ai | M4+M1 | M1+M3 | MSL is consolidated research (FAIR+GenAI merger); product teams embed independently |
| nvidia | M4+M1 | M1+M9 | NVIDIA Research is ring-fenced lab; company itself is AI-native |
| bosch-bcai | M4 | M1+M3 | BCAI is research center; product divisions embed AI independently |
| google-ai-infra | M4 | M3 | AI2 consolidation created unified engineering unit, not hub coordinating spokes |
| wells-fargo | M4 | M2+M6a | Head of AI governs + 180K desktops deployed. No spoke-specific customization evidence |
| pentagon-cdao | M4+M2 | M2 | CDAO is governance/standards body, not shared AI infrastructure builder |
| sap | M4 | M5a+M2 | Joule is AI product; Business AI provides governance/enablement |
| cvs-health | M4 | M6a | Mandadi explicitly rejects CAIO. Mass deployment without hub structure |
| kaiser-permanente | M4 | M6a | Thin data, no hub-spoke evidence. Provisional pending enrichment |
| apple | M4 | M3 | AI/ML embedded in product groups without centralized hub coordination |
| salesforce | M4+M5 | M5a+M3 | Einstein/Agentforce are products; product teams embed AI independently |
| servicenow | M4+M5 | M5a+M6a | Now Assist is product; enterprise mandate drives mass adoption |
| mckinsey | M4+M2 | M5a+M2 | QuantumBlack builds AI products for internal consumption; also enables consultants |
| accenture-openai | M4 | M6a+M5 | Enterprise-wide AI adoption + client-facing products, not hub-spoke |
| netflix | M4 | M3 Contextual | Research explicitly distributed and embedded in business teams |
| uber | M4+M5 | M1+M5 | AI Labs is research; AV partnerships are venture exploration |
| nike | M4 | M2+M3 | CDAIO provides governance; tech moving under ops = embedding |
| fedex | M4 | M2+M6a | Dataworks provides central capabilities; AI education drives mass adoption |

## Kept M4 (43 specimens)

Genuine hub-and-spoke specimens confirmed across these industry clusters:
- **Pharmaceuticals (5)**: eli-lilly, pfizer, novo-nordisk, sanofi, servier
- **Automotive (6)**: bmw, ford, general-motors, honda, mercedes-benz, toyota
- **Healthcare (7)**: mayo-clinic, mount-sinai-health-system, sutter-health, unitedhealth-group, cedars-sinai, mass-general-brigham, travelers
- **Financial Services (4)**: jpmorgan, morgan-stanley, bloomberg, visa
- **Technology (4 kept)**: intel, atlassian, microsoft, tencent
- **Industrial (6)**: honeywell, deere-and-co, lockheed-martin, panasonic, schneider-electric
- **Other (7)**: kroger, lowes, thomson-reuters, disney, t-mobile, nokia, cognizant, publicis-groupe, mercado-libre, pepsico, ulta-beauty, delta-air-lines

## Flagged for Enrichment (4 specimens)

| Specimen | Issue |
|----------|-------|
| hp-inc | Three-pillar structure could be M4 or M1+M3. Needs enrichment. |
| abb | Genix platform story sounds M4 but completeness too low to confirm. |
| siemens | Xcelerator + Industrial Copilot could be M4 or M2+M5. Needs enrichment. |
| coca-cola | Almost no structural data. Poorly supported M4 at Low/Low. |

## Protocol Changes

1. **New decision tree step 5**: Added "shared AI infrastructure" discriminator between Step 4 (build vs. enable) and the time-boxed question
2. **New Guardrail 8**: "Hub-and-Spoke vs. Enterprise Deployment (M4 trap)" — checks for bidirectional coordination and 3+ semi-autonomous spokes
3. **Updated classification-quick-ref.md**: M4 one-line test now reads "Hub builds shared AI infra + 3+ domain spokes build on it (bidirectional)"

## New Distribution

| Model | Before | After | Change |
|-------|--------|-------|--------|
| M1 Research Lab | 7 (5%) | 12 (8%) | +5 |
| M2 CoE | 20 (14%) | 24 (16%) | +4 |
| M3 Embedded | 11 (7%) | 14 (10%) | +3 |
| M4 Hub-and-Spoke | 66 (45%) | 47 (32%) | -19 |
| M5 Product/Venture | 11 (7%) | 15 (10%) | +4 |
| M6 Unnamed/Informal | 21 (14%) | 24 (16%) | +3 |
| M9 AI-Native | 10 (7%) | 10 (7%) | 0 |

M4 drops from 45% to 32% of the collection. Still the largest model (appropriate for R&D-intensive and domain-knowledge-intensive industries where hub-spoke is genuinely the dominant pattern), but no longer dominating. The gains spread meaningfully across M1, M2, M3, M5, and M6.

## Cross-Cutting Patterns

1. **Big Tech parallel structures are not hub-spoke.** Amazon, Meta, NVIDIA, and Google all had "research + product" structures classified as M4. In each case, the research and product teams operate independently — the research doesn't coordinate shared infrastructure that products build on. These are M1+M3.

2. **Enterprise deployment ≠ hub-spoke.** Wells Fargo, FedEx, CVS Health, and Kaiser Permanente all had central teams deploying AI tools to large employee populations. But mass deployment of tools is M2 (governance/enablement) + M6a (adoption), not M4. The "spokes" are tool recipients, not semi-autonomous units building domain AI.

3. **AI products in platforms ≠ hub-spoke.** Salesforce (Agentforce), SAP (Joule), ServiceNow (Now Assist) all embed AI products in their platforms. This is M5 (product/venture), not M4. The AI is the product, not shared infrastructure enabling other units.

4. **The pharma/auto M4s are genuine and stable.** All 11 pharma+auto M4 specimens survived the audit. These industries have the structural features that make hub-spoke necessary: deep domain expertise in distributed units, shared AI infrastructure needs, multi-year R&D horizons.

## Taxonomy Feedback

- The M4 definition was too loose. The new discriminator ("shared infrastructure that distributed units depend on and build upon") provides much better separation.
- The audit suggests M4 is genuinely the dominant structure in R&D-intensive, domain-knowledge-intensive industries (pharma, auto, healthcare, industrial). This is the structural equilibrium where specialized domain knowledge must be preserved in distributed units while shared AI infrastructure must be coordinated centrally.
- M4 may be OVER-represented in our collection not because it's the most common structure in the wild, but because R&D-intensive firms are more visible and better documented. M6a (enterprise-wide adoption) may actually be the most common real-world pattern but is harder to observe from public sources.
- Future work: the 4 enrichment-needed specimens (HP Inc, ABB, Siemens, Coca-Cola) should be revisited with more data. The borderline-kept specimens (Microsoft, Tencent, Delta, Ulta) should be reconsidered if new evidence emerges.
