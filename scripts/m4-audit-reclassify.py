#!/usr/bin/env python3
"""
M4 Taxonomy Audit — Reclassification Script
Session: 2026-02-12

Applies reclassifications identified during M4 audit.
For each specimen:
  1. Updates classification fields (structuralModel, secondaryModel, orientation, rationale)
  2. Adds an audit layer at the TOP of the layers array recording the change
  3. Updates meta.lastUpdated
  4. Adds taxonomyFeedback note

Does NOT modify registry.json or synthesis-queue.json — those are updated separately.
"""

import json
import os
from datetime import date

TODAY = date.today().isoformat()
SPECIMENS_DIR = "specimens"

MODEL_NAMES = {
    1: "Research Lab",
    2: "Center of Excellence",
    3: "Embedded Teams",
    4: "Hybrid/Hub-and-Spoke",
    5: "Product/Venture Lab",
    6: "Unnamed/Informal",
    7: "Tiger Teams",
    8: "Skunkworks",
    9: "AI-Native",
}

SUBTYPE_NAMES = {
    "5a": "Internal Incubator",
    "5b": "Venture Builder",
    "5c": "Platform-to-Product",
    "6a": "Enterprise-Wide Adoption",
    "6b": "Centralized-but-Unnamed",
    "6c": "Grassroots/Bottom-Up",
}

# ── All reclassifications ──────────────────────────────────────────────

RECLASSIFICATIONS = {
    # ── DEFINITE (13) ──────────────────────────────────────────────────

    "amazon-agi": {
        "new_primary": 1,
        "new_secondary": 3,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M1+M3 (Audit 2026-02-12). AGI org under DeSantis is a consolidated research lab (M1), not a hub that coordinates shared infrastructure for product teams. Product teams (Alexa, AWS AI services) operate independently as embedded AI (M3). The consolidation-arc insight confirms: parallel structures were merged, but the result is unified research + independent product embedding, not hub-spoke coordination.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M1 Research Lab + M3 Embedded. AGI org is consolidated research, product teams are independently embedded. No bidirectional hub-spoke coordination.",
    },
    "meta-ai": {
        "new_primary": 1,
        "new_secondary": 3,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M1+M3 (Audit 2026-02-12). MSL under Wang is a consolidated research organization (M1) formed from FAIR+GenAI merger. Product teams (Instagram AI, WhatsApp AI) embed AI independently (M3). The meta-exploration-failure insight confirms: FAIR autonomy was sacrificed in consolidation, making this a research-subordinated-to-product structure, not a hub coordinating spokes. LeCun's departure is the clearest signal.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M1 Research Lab + M3 Embedded. MSL is consolidated research (FAIR+GenAI), product teams embed AI independently. No hub-spoke infrastructure sharing.",
    },
    "nvidia": {
        "new_primary": 1,
        "new_secondary": 9,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M1 (Audit 2026-02-12). NVIDIA Research is a dedicated research lab. But the broader company is AI-native (M9-adjacent) — AI IS the product across GPUs, CUDA, and enterprise software. No hub-spoke coordination because AI isn't a separate function to be coordinated; it's the company's core architecture.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M1 Research Lab with M9 AI-Native secondary. NVIDIA Research is ring-fenced research; the company itself is AI-native.",
    },
    "bosch-bcai": {
        "new_primary": 1,
        "new_secondary": 3,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M1+M3 (Audit 2026-02-12). BCAI (Bosch Center for AI) is a dedicated research center with academic publications and long-horizon R&D (M1). Product divisions embed AI for specific applications (M3). The 'hub' is a research lab, not a shared infrastructure coordinator.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M1 Research Lab + M3 Embedded. BCAI is a research center; product divisions embed AI independently.",
    },
    "google-ai-infra": {
        "new_primary": 3,
        "new_secondary": None,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M3 (Audit 2026-02-12). AI2 (Project EAT consolidation) is an engineering unit that builds AI infrastructure, not a hub that coordinates distributed spokes. The consolidation pulled teams FROM Research, Cloud, and hardware INTO a single engineering org. This is embedded engineering, not hub-spoke.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M3 Embedded Teams. AI2 consolidation created a unified engineering unit, not a hub coordinating spokes.",
    },
    "wells-fargo": {
        "new_primary": 2,
        "new_secondary": 6,
        "new_subtype": "6a",
        "orientation": "Structural",
        "rationale": "M4→M2+M6a (Audit 2026-02-12). Head of AI (Van Beurden) + Head of AI Products (Shafiq) form a CoE-style governance structure (M2). 180K desktops equipped with AI tools and 90K employees trained represents enterprise-wide adoption (M6a). No evidence of semi-autonomous business units building domain-specific AI on shared hub infrastructure. The pharma-hub-divergence insight confirms: finance 'hubs' that serve deployment/governance are CoEs, not true hub-and-spoke.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M2 CoE + M6a Enterprise-Wide Adoption. Central leadership governs and enables mass deployment, but no hub-spoke infrastructure coordination.",
    },
    "pentagon-cdao": {
        "new_primary": 2,
        "new_secondary": None,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M2 (Audit 2026-02-12). CDAO is a governance, standards, and policy body — it sets AI adoption standards for the Department of Defense but does not build shared AI infrastructure that service branches build upon. The consolidation of 6 innovation orgs under R&E umbrella is organizational streamlining, not hub-spoke coordination. Government CAIO instability insight confirms the governance-focused nature.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M2 Center of Excellence. CDAO governs and sets standards but does not build shared infrastructure for service branch spokes.",
    },
    "sap": {
        "new_primary": 5,
        "new_secondary": 2,
        "new_subtype": "5a",
        "orientation": "Structural",
        "rationale": "M4→M5a+M2 (Audit 2026-02-12). Joule is an AI product embedded in SAP's cloud suite — a product/venture that stays in the parent (M5a). Internal AI governance and Business AI unit provide CoE-style enablement (M2). No hub-spoke coordination across distributed semi-autonomous units.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M5a Internal Incubator + M2 CoE. Joule is an AI product; Business AI provides governance/enablement.",
    },
    "cvs-health": {
        "new_primary": 6,
        "new_secondary": None,
        "new_subtype": "6a",
        "orientation": "Contextual",
        "rationale": "M4→M6a (Audit 2026-02-12). Mandadi explicitly rejects CAIO role ('worst thing companies can do'). $1B savings, 90% ambient AI adoption, 300K employees — all achieved through enterprise-wide deployment without dedicated AI hub structure. The anti-CAIO thesis insight directly supports this: CVS treats AI as invisible infrastructure, not a hub-coordinated function.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M6a Enterprise-Wide Adoption. Mandadi explicitly rejects centralized AI leadership. Mass deployment without hub structure.",
    },
    "kaiser-permanente": {
        "new_primary": 6,
        "new_secondary": None,
        "new_subtype": "6a",
        "orientation": "Contextual",
        "rationale": "M4→M6a (Audit 2026-02-12). Thin data with no evidence of hub coordinating shared AI infrastructure for distributed spokes. Available evidence suggests mass adoption without formal hub-spoke structure. Low completeness — may need reclassification again after enrichment.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M6a Enterprise-Wide Adoption. Insufficient evidence for hub-spoke coordination. Provisional pending enrichment.",
    },
    "apple": {
        "new_primary": 3,
        "new_secondary": None,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M3 (Audit 2026-02-12). Apple's AI/ML is deeply embedded in product groups (Siri, Apple Intelligence, hardware ML). No evidence of a coordinating hub that provides shared AI infrastructure other product teams build upon. Apple's organizational secrecy makes structural data thin, but what we can observe is product-embedded AI, not hub-spoke.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M3 Embedded Teams. AI/ML embedded in product groups without centralized hub coordination.",
    },
    "salesforce": {
        "new_primary": 5,
        "new_secondary": 3,
        "new_subtype": "5a",
        "orientation": "Structural",
        "rationale": "M4→M5a+M3 (Audit 2026-02-12). Einstein and Agentforce are AI products embedded in the Salesforce platform — internal incubator products that stay in the parent (M5a). AI is also embedded in product teams across Sales Cloud, Service Cloud, etc. (M3). The 'hub' was really a product organization, not infrastructure-coordinating function.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M5a Internal Incubator + M3 Embedded. Einstein/Agentforce are products; product teams embed AI independently.",
    },
    "servicenow": {
        "new_primary": 5,
        "new_secondary": 6,
        "new_subtype": "5a",
        "orientation": "Contextual",
        "rationale": "M4→M5a+M6a (Audit 2026-02-12). Now Assist and AI Agent Orchestrator are AI products embedded in ServiceNow's platform (M5a). McDermott's 'obliterate 20th century org charts' mandate drives enterprise-wide contextual adoption (M6a). No hub-spoke infrastructure coordination — AI IS the product.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M5a Internal Incubator + M6a Enterprise-Wide. AI products + contextual adoption mandate, not hub-spoke.",
    },

    # ── BORDERLINE → RECLASSIFY (6) ───────────────────────────────────

    "mckinsey": {
        "new_primary": 5,
        "new_secondary": 2,
        "new_subtype": "5a",
        "orientation": "Contextual",
        "rationale": "M4→M5a+M2 (Audit 2026-02-12). QuantumBlack (1,700 people) is primarily a product lab that builds AI products (Lilli, 25K AI agents) absorbed into McKinsey's consulting practice (M5a). It also enables consultants to use AI (M2). The 'hub' doesn't coordinate semi-autonomous domain spokes building on shared infrastructure — it builds products consultants consume. The consulting-dual-identity insight confirms: QuantumBlack is a product vendor to its own firm.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M5a Internal Incubator + M2 CoE. QuantumBlack builds AI products for internal consumption; also enables consultants.",
    },
    "accenture-openai": {
        "new_primary": 6,
        "new_secondary": 5,
        "new_subtype": "6a",
        "orientation": "Contextual",
        "rationale": "M4→M6a+M5 (Audit 2026-02-12). Accenture's AI transformation is enterprise-wide adoption (77K AI professionals, mandatory reskilling, $865M restructuring) — classic M6a. AI Refinery is a product for clients (M5). The 'Reinvention Services' BU consolidation is business restructuring, not hub-spoke AI infrastructure coordination. Services-business-model-crisis insight confirms: this is a business model transformation, not an AI structural coordination problem.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M6a Enterprise-Wide Adoption + M5 Product/Venture. Enterprise-wide AI adoption + client-facing AI products, not hub-spoke.",
    },
    "netflix": {
        "new_primary": 3,
        "new_secondary": None,
        "new_subtype": None,
        "orientation": "Contextual",
        "rationale": "M4→M3 Contextual (Audit 2026-02-12). Netflix explicitly states research is NOT centralized — nine research areas are distributed and work 'in close collaboration with business teams.' AIMS is a product team for recommendations, not a coordinating hub. The contextual orientation was already assigned, which is inconsistent with M4's structural separation. Reclassifying to M3 Contextual aligns structure with orientation.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M3 Embedded Teams with Contextual orientation. Research explicitly distributed and embedded in business teams.",
    },
    "uber": {
        "new_primary": 1,
        "new_secondary": 5,
        "new_subtype": None,
        "orientation": "Structural",
        "rationale": "M4→M1+M5 (Audit 2026-02-12). Uber AI Labs operates as a research lab with 'Core' (fundamental research) and 'Connections' (product integration) programs — this is M1 with a product bridge, not a hub coordinating shared infrastructure. AV partnerships (Aurora, Wayve) represent M5 venture-style exploration. Per HANDOFF item #36: 'AI Labs looks more like M1 Research Lab + M3 Embedded than true hub-spoke coordination.' Keeping M5 secondary (AV ventures) rather than M3 since the product embedding evidence is weaker.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M1 Research Lab + M5 Product/Venture. AI Labs is research; AV partnerships are venture exploration.",
    },
    "nike": {
        "new_primary": 2,
        "new_secondary": 3,
        "new_subtype": None,
        "orientation": "Contextual",
        "rationale": "M4→M2+M3 (Audit 2026-02-12). CDAIO (Alan John) runs a central data/AI function that sets standards and builds capabilities (M2 CoE). AI is embedded in supply chain, Nike Sport Research Lab, and consumer apps (M3). December 2025 reorg moved tech under operations — the trend is toward embedding, not hub-spoke coordination. The retail-no-caio-pattern insight notes Nike deploys AI without the hub infrastructure pattern seen in pharma/automotive M4s.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M2 CoE + M3 Embedded. CDAIO provides governance/enablement; AI increasingly embedded in operations.",
    },
    "fedex": {
        "new_primary": 2,
        "new_secondary": 6,
        "new_subtype": "6a",
        "orientation": "Contextual",
        "rationale": "M4→M2+M6a (Audit 2026-02-12). FedEx Dataworks is a central data/AI platform team that provides standards and capabilities (M2 CoE). The enterprise-wide AI education program (Accenture LearnVantage, Dec 2025) is a mass adoption push (M6a). The 'spokes' are training recipients, not semi-autonomous units building domain-specific AI on shared infrastructure. The contextual-via-education insight directly supports this: FedEx pursues contextual ambidexterity through education, not hub-spoke structural separation.",
        "layer_summary": "M4 taxonomy audit: Reclassified from M4 Hub-and-Spoke to M2 CoE + M6a Enterprise-Wide. Dataworks provides central capabilities; AI education drives mass adoption.",
    },
}


def reclassify_specimen(spec_id, reclass):
    """Apply reclassification to a specimen JSON file."""
    fpath = os.path.join(SPECIMENS_DIR, f"{spec_id}.json")
    if not os.path.exists(fpath):
        print(f"  ERROR: {fpath} not found")
        return False

    with open(fpath, "r") as f:
        spec = json.load(f)

    old_model = spec["classification"]["structuralModel"]
    old_model_name = spec["classification"].get("structuralModelName", "")
    old_secondary = spec["classification"].get("secondaryModel")
    old_orientation = spec["classification"].get("orientationName", "")

    new_primary = reclass["new_primary"]
    new_secondary = reclass["new_secondary"]
    new_subtype = reclass.get("new_subtype")

    # Update classification
    spec["classification"]["structuralModel"] = new_primary
    spec["classification"]["structuralModelName"] = MODEL_NAMES[new_primary]
    spec["classification"]["secondaryModel"] = new_secondary
    spec["classification"]["secondaryModelName"] = MODEL_NAMES[new_secondary] if new_secondary else None
    spec["classification"]["subType"] = new_subtype
    spec["classification"]["subTypeName"] = SUBTYPE_NAMES.get(new_subtype) if new_subtype else None
    spec["classification"]["orientation"] = reclass["orientation"]
    spec["classification"]["orientationName"] = reclass["orientation"] + " Ambidexterity" if reclass["orientation"] != "Structural" else "Structural Ambidexterity"
    # Fix: keep it simple
    spec["classification"]["orientationName"] = reclass["orientation"]
    spec["classification"]["classificationRationale"] = reclass["rationale"]

    # Add audit layer at TOP of layers array
    old_class_str = f"M{old_model} {old_model_name}"
    if old_secondary:
        old_class_str += f" + M{old_secondary}"
    new_class_str = f"M{new_primary} {MODEL_NAMES[new_primary]}"
    if new_secondary:
        new_class_str += f" + M{new_secondary} {MODEL_NAMES[new_secondary]}"

    audit_layer = {
        "date": "2026-02",
        "label": f"M4 Taxonomy Audit: {old_class_str} → {new_class_str}",
        "summary": reclass["layer_summary"],
        "classification": old_class_str,
        "sourceRefs": ["m4-taxonomy-audit-2026-02-12"],
    }

    if "layers" not in spec or spec["layers"] is None:
        spec["layers"] = []
    spec["layers"].insert(0, audit_layer)

    # Add taxonomyFeedback note
    feedback_note = f"[2026-02-12 M4 Audit] Reclassified from M4 to M{new_primary}"
    if new_secondary:
        feedback_note += f"+M{new_secondary}"
    feedback_note += f". Key discriminator: does the hub coordinate shared AI infrastructure that distributed units depend on and build upon? Answer: No — {reclass['layer_summary'].split('. ', 1)[-1] if '. ' in reclass['layer_summary'] else reclass['layer_summary']}"

    if "taxonomyFeedback" not in spec or spec["taxonomyFeedback"] is None:
        spec["taxonomyFeedback"] = []
    spec["taxonomyFeedback"].append(feedback_note)

    # Update meta
    spec["meta"]["lastUpdated"] = TODAY

    # Write back
    with open(fpath, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")

    sec_str = f"+M{new_secondary}" if new_secondary else ""
    old_sec_str = f"+M{old_secondary}" if old_secondary else ""
    print(f"  ✓ {spec_id}: M{old_model}{old_sec_str} → M{new_primary}{sec_str}")
    return True


def main():
    print(f"M4 Taxonomy Audit — Reclassification")
    print(f"Date: {TODAY}")
    print(f"Specimens to reclassify: {len(RECLASSIFICATIONS)}")
    print()

    success = 0
    failed = 0

    for spec_id, reclass in sorted(RECLASSIFICATIONS.items()):
        if reclassify_specimen(spec_id, reclass):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} reclassified, {failed} failed")


if __name__ == "__main__":
    main()
