#!/usr/bin/env python3
"""
patch-synthesis-feb15.py
========================
Applies all proposed changes from the Feb 15, 2026 seven-batch synthesis run.
Operates on:
  - synthesis/tensions.json     (score updates + new placements)
  - synthesis/contingencies.json (C6 additions + other changes)
  - synthesis/mechanisms.json   (new specimen links)
  - synthesis/insights.json     (new insights)

Run from project root:
    python3 scripts/patch-synthesis-feb15.py [--dry-run] [--phase 1|2|3|4|all]

Uses atomic writes via scripts/lib/utils.py.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from lib.utils import save_json, load_json, write_changelog

TENSIONS_PATH = PROJECT_ROOT / "synthesis" / "tensions.json"
CONTINGENCIES_PATH = PROJECT_ROOT / "synthesis" / "contingencies.json"
MECHANISMS_PATH = PROJECT_ROOT / "synthesis" / "mechanisms.json"
INSIGHTS_PATH = PROJECT_ROOT / "synthesis" / "insights.json"

DRY_RUN = False
CHANGES = []  # Audit log


def log(msg):
    print(f"  {msg}")
    CHANGES.append(msg)


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1: TENSION SCORE UPDATES
# ══════════════════════════════════════════════════════════════════════════════

# Format: (specimenId, tensionFieldName, new_position, evidence_text, source_batch)
NEW_PLACEMENTS = [
    # Batch A - McKinsey (all null → new)
    ("mckinsey", "structuralVsContextual", -0.3, "QuantumBlack (1,700 people) is structurally distinct. 40% of firm revenue from AI. Moderate structural separation.", "Batch A"),
    ("mckinsey", "speedVsDepth", 0.5, "Few-thousand to 25,000 agents in 18 months. Mass deployment at extreme speed.", "Batch A"),
    ("mckinsey", "centralVsDistributed", -0.4, "QuantumBlack is centralized capability hub. Consultants use agents in distributed engagement teams.", "Batch A"),
    ("mckinsey", "namedVsQuiet", -0.5, "QuantumBlack is named, branded unit. 'Transform or die' rhetoric.", "Batch A"),
    ("mckinsey", "longVsShortHorizon", 0.0, "Mixed: outcome-based partnerships (long) vs. quarterly revenue attribution (short).", "Batch A"),
    # Batch B - google-ai-infra (T2, T5 were null)
    ("google-ai-infra", "speedVsDepth", -0.2, "Deep infrastructure work (Project EAT 'wholesale rethinking'). Competitive urgency pushes toward speed.", "Batch B"),
    ("google-ai-infra", "longVsShortHorizon", -0.3, "AI infrastructure inherently medium-to-long horizon. Competitive pressure from NVIDIA creates short-term accountability.", "Batch B"),
    # Batch C - Cedars-Sinai (all new)
    ("cedars-sinai", "structuralVsContextual", -0.5, "Dual-reporting CAIO creates structural separation. Distributed informatics officers (CHIO, CNIO, CMIO) embed governance.", "Batch C"),
    ("cedars-sinai", "speedVsDepth", -0.3, "CAIRE on research timelines. AI Council vets clinical deployments. Governance favors deliberation.", "Batch C"),
    ("cedars-sinai", "centralVsDistributed", -0.2, "AI Council provides centralized governance. Three informatics officers distribute decision-making.", "Batch C"),
    ("cedars-sinai", "namedVsQuiet", -0.6, "CAIRE is named research center. CAIO is visible C-suite role. Formally titled positions.", "Batch C"),
    ("cedars-sinai", "longVsShortHorizon", -0.3, "CAIRE multi-year research timelines. Clinical AI per-project basis. Academic mission leans long.", "Batch C"),
    # Batch C - Kaiser Permanente (all new)
    ("kaiser-permanente", "structuralVsContextual", 0.5, "Dual-hat CMIO/CAIO absorbs AI into existing role. No dedicated AI organization.", "Batch C"),
    ("kaiser-permanente", "speedVsDepth", 0.0, "Insufficient data to assess.", "Batch C"),
    ("kaiser-permanente", "centralVsDistributed", 0.0, "Unified payer-provider governance centralizes. Regional entities may federate. Insufficient data.", "Batch C"),
    ("kaiser-permanente", "namedVsQuiet", 0.6, "Dual-hat model = no dedicated AI branding. Quiet transformation.", "Batch C"),
    ("kaiser-permanente", "longVsShortHorizon", 0.0, "Insufficient data.", "Batch C"),
    # Batch C - Mass General Brigham (all new)
    ("mass-general-brigham", "structuralVsContextual", -0.6, "1,800+ digital staff under CDIO. AIwithCare spinout further separates commercialization.", "Batch C"),
    ("mass-general-brigham", "speedVsDepth", -0.4, "Academic research on multi-year grant cycles. Depth from academic research mission.", "Batch C"),
    ("mass-general-brigham", "centralVsDistributed", -0.3, "CDIO controls strategy centrally. Research faculty retain academic freedom. AIwithCare independent.", "Batch C"),
    ("mass-general-brigham", "namedVsQuiet", -0.5, "1,800+ person digital org is highly visible. AIwithCare spinout is named commercial entity.", "Batch C"),
    ("mass-general-brigham", "longVsShortHorizon", -0.5, "Academic research mission creates multi-year horizons. Grant cycles impose 3-5 year planning.", "Batch C"),
    # wells-fargo T2/T5 moved to SCORE_REVISIONS (already have values from prior session)
    # Batch G - Columbia Group (new stub)
    ("columbia-group", "structuralVsContextual", -0.3, "Head of AI appointed — structural intent. Early stage.", "Batch G"),
    ("columbia-group", "centralVsDistributed", -0.4, "'AI factory' concept implies centralized capability building. Head of AI as central coordinator.", "Batch G"),
    ("columbia-group", "namedVsQuiet", -0.3, "Named Head of AI role, public announcement. Not heavily branded.", "Batch G"),
    # Batch G - ByteDance (text → numeric conversion)
    ("bytedance", "speedVsDepth", 0.5, "12x token growth. Rapid hardware proliferation. Heavily speed-biased.", "Batch G"),
    ("bytedance", "centralVsDistributed", -0.6, "Volcano Engine is central platform. Seed research centralized under Wu.", "Batch G"),
    # Batch G - Duolingo (text → numeric conversion)
    ("duolingo", "structuralVsContextual", 0.4, "AI integrated within product. No separate AI division. frAI-days for all teams.", "Batch G"),
    ("duolingo", "speedVsDepth", -0.2, "Birdbrain developed since 2018. Patient deep integration. Daily model updates add speed.", "Batch G"),
    # FIX: amazon-agi was in SCORE_REVISIONS but doesn't exist in T3 yet — add as new placement
    ("amazon-agi", "centralVsDistributed", -0.3, "M3 embedded teams more autonomous than spokes. AGI org is central research, product teams are independent. [Feb 15 revision: M3 embedded teams more autonomous than spokes]", "Batch B"),
    # FIX: coca-cola was in SCORE_REVISIONS but doesn't exist in T1 yet — add as new placement
    ("coca-cola", "structuralVsContextual", 0.3, "M4→M6 reclass. '2 of 2,000 with AI in title'. CFO-chaired Digital Council. Contextual. [Feb 15 revision: M4→M6 reclass]", "Batch G"),
]

# Format: (specimenId, tensionFieldName, old_value, new_value, rationale, source_batch)
SCORE_REVISIONS = [
    # amazon-agi T3 moved to NEW_PLACEMENTS (not in T3 yet)
    ("meta-ai", "longVsShortHorizon", 0.4, 0.5, "Compressed FAIR horizons + Reality Labs retreat", "Batch B"),
    ("nvidia", "structuralVsContextual", 0.3, 0.5, "Stronger contextual integration signal from M1+M9", "Batch B"),
    ("apple", "structuralVsContextual", -0.6, -0.4, "M3 weakens structural separation story", "Batch B"),
    ("apple", "namedVsQuiet", -0.1, 0.1, "No named hub, AI structure invisible under M3", "Batch B"),
    ("google-deepmind", "speedVsDepth", 0.1, 0.2, "Accelerating deployment: 750M MAU, 8M Enterprise seats", "Batch B"),
    ("google-deepmind", "centralVsDistributed", -0.7, -0.6, "50% AI-generated code suggests distributed capability", "Batch B"),
    ("google-deepmind", "longVsShortHorizon", -0.4, -0.3, "CapEx doubling creates shorter accountability cycles", "Batch B"),
    ("sap", "speedVsDepth", 0.0, 0.1, "AI in 2/3 of cloud order entry, up 20+ pts from Q3", "Batch B"),
    ("servicenow", "speedVsDepth", 0.3, 0.4, "$600M+ Now Assist revenue achieved rapidly", "Batch B"),
    ("servicenow", "centralVsDistributed", -0.4, -0.5, "Centralized product development. AI Control Tower.", "Batch B"),
    ("servicenow", "longVsShortHorizon", 0.2, 0.3, "Consumption pricing creates short accountability", "Batch B"),
    ("nike", "structuralVsContextual", -0.2, 0.4, "M4→M2+M3 reclass. CTO eliminated. COO integration signals contextual.", "Batch D"),
    ("spotify", "namedVsQuiet", 0.0, -0.4, "GenAI Research Lab announced. 'Honk' branding. Spotify Research visible.", "Batch D"),
    ("bosch-bcai", "structuralVsContextual", -0.5, -0.4, "BCAI 'network' framing + embedded division experts = some contextual elements", "Batch E"),
    ("palantir", "namedVsQuiet", -0.6, -0.8, "Loudest AI brand in collection. Karp shareholder letters. AIP aggressively marketed.", "Batch F"),
    ("palantir", "longVsShortHorizon", 0.0, -0.3, "Karp rhetoric consistently long-horizon. Defense contracts multi-year.", "Batch F"),
    ("stripe", "namedVsQuiet", 0.5, 0.3, "CRO of AI role and Stripe Sessions somewhat public. No branded AI lab.", "Batch F"),
    ("stripe", "longVsShortHorizon", 0.0, -0.2, "Payments Foundation Model multi-year. Agentic commerce protocol long-term.", "Batch F"),
    ("crowdstrike", "namedVsQuiet", 0.3, -0.2, "Charlotte AI is branded product. 'Security AGI' named aspiration. Fal.Con showcases AI.", "Batch F"),
    # coca-cola T1 moved to NEW_PLACEMENTS (not in T1 yet)
    # FIX: wells-fargo T2/T5 already have values from prior session (0.3 and 0.2) — force revise
    ("wells-fargo", "speedVsDepth", 0.3, -0.3, "Banking requires validation depth. Google Agentspace to only 2K initially. 30-35% automation target.", "Batch F"),
    ("wells-fargo", "longVsShortHorizon", 0.2, 0.3, "30-35% automation target and $612M severance charge signal short-to-medium efficiency focus.", "Batch F"),
]

# Shopify T1: check if it's still at 0.3 (pre-M6 reclassification) — should be 0.9
# We'll handle this as a revision only if current value is wrong


def phase1_tensions():
    """Apply tension score updates and new placements."""
    print("\n═══ PHASE 1: TENSION SCORES ═══")
    data = load_json(TENSIONS_PATH)

    # Build lookup: fieldName -> tension object
    tension_map = {t["fieldName"]: t for t in data["tensions"]}

    # --- NEW PLACEMENTS ---
    placed = 0
    for spec_id, field, pos, evidence, batch in NEW_PLACEMENTS:
        t = tension_map[field]
        existing_ids = {s["specimenId"] for s in t["specimens"]}
        if spec_id in existing_ids:
            # Check if it has a text value that needs numeric conversion
            for s in t["specimens"]:
                if s["specimenId"] == spec_id:
                    if isinstance(s.get("position"), str) or s.get("position") is None:
                        old_val = s["position"]
                        s["position"] = pos
                        s["evidence"] = evidence
                        log(f"CONVERT T{t['id']} {spec_id}: '{old_val}' → {pos} ({batch})")
                        placed += 1
                    else:
                        log(f"SKIP T{t['id']} {spec_id}: already has numeric value {s['position']} ({batch})")
                    break
        else:
            t["specimens"].append({
                "specimenId": spec_id,
                "position": pos,
                "evidence": evidence
            })
            log(f"ADD T{t['id']} {spec_id}: {pos} ({batch})")
            placed += 1

    # --- SCORE REVISIONS ---
    revised = 0
    for spec_id, field, old_val, new_val, rationale, batch in SCORE_REVISIONS:
        t = tension_map[field]
        found = False
        for s in t["specimens"]:
            if s["specimenId"] == spec_id:
                found = True
                current = s["position"]
                # Allow revision if current matches old_val (within tolerance) or if forced
                if current is None or (isinstance(current, (int, float)) and abs(current - old_val) < 0.15):
                    s["position"] = new_val
                    s["evidence"] = s.get("evidence", "") + f" [Feb 15 revision: {rationale}]"
                    log(f"REVISE T{t['id']} {spec_id}: {current} → {new_val} ({batch}: {rationale})")
                    revised += 1
                else:
                    log(f"SKIP-MISMATCH T{t['id']} {spec_id}: expected ~{old_val}, found {current} ({batch})")
                break
        if not found:
            log(f"WARN T{t['id']} {spec_id}: not found in tension specimens ({batch})")

    # --- Shopify T1 check ---
    t1 = tension_map["structuralVsContextual"]
    for s in t1["specimens"]:
        if s["specimenId"] == "shopify":
            if isinstance(s["position"], (int, float)) and s["position"] < 0.5:
                old = s["position"]
                s["position"] = 0.9
                s["evidence"] = "Purest contextual specimen. No AI org, no CAIO. CEO mandate is sole coordination mechanism. 'Prove AI can't do it' headcount policy. [Feb 15: M3→M6 reclass correction]"
                log(f"REVISE T1 shopify: {old} → 0.9 (M6 reclass correction)")
                revised += 1
            break

    data["lastUpdated"] = "2026-02-15"
    print(f"\n  Placed: {placed}, Revised: {revised}")

    if not DRY_RUN:
        save_json(TENSIONS_PATH, data)
        print(f"  ✓ Saved {TENSIONS_PATH.name}")
    else:
        print(f"  [DRY RUN] Would save {TENSIONS_PATH.name}")


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2: CONTINGENCY UPDATES
# ══════════════════════════════════════════════════════════════════════════════

# C6 environmentalAiPull additions
# The contingencies.json stores specimens in buckets within each contingency.
# C6 structure: { "high": { "specimens": [...] }, "medium": { ... }, "low": { ... } }
# We need to understand the exact structure first, so this phase reads and patches.

C6_ADDITIONS = {
    # Strong/High
    "mckinsey": "high",
    "thomson-reuters": "high",
    "kyndryl": "high",
    "accenture-openai": "high",
    "salesforce": "high",
    "amazon-agi": "high",
    "meta-ai": "high",
    "google-deepmind": "high",
    "servicenow": "high",
    "crowdstrike": "high",
    "recruit-holdings": "high",
    "uber": "high",
    "xai": "high",
    # Medium
    "sap": "medium",
    "cedars-sinai": "medium",
    "kaiser-permanente": "medium",
    "lionsgate": "medium",
    "comcast---nbcuniversal": "medium",
    "ups": "medium",
    "fedex": "medium",
    "panasonic": "medium",
    "bosch-bcai": "medium",
    "hp-inc": "medium",
    "wells-fargo": "medium",
    # Medium-High (place in high for simplicity since JSON is binary high/medium/low)
    "mass-general-brigham": "high",
}

# Other contingency changes: (specimenId, contingencyId, old_bucket, new_bucket)
OTHER_CONTINGENCY_CHANGES = [
    # C5 technicalDebt: amazon-agi Low → Medium
    ("amazon-agi", "technicalDebt", "low", "medium"),
    # C1 regulatoryIntensity: servicenow Low → Medium
    ("servicenow", "regulatoryIntensity", "low", "medium"),
]

# C3 ceoTenure additions (specimens to add to specific buckets)
# These are for specimens with null C3 that need placement
C3_ADDITIONS = {
    # High (long tenure)
    "servicenow": "high",
    "ups": "high",
    # Medium
    "baker-mckenzie": "medium",
    "accenture-openai": "medium",
    "arm-holdings": "medium",
    # Long (founder)
    "lionsgate": "high",  # Feltheimer CEO since 2000
}


def phase2_contingencies():
    """Apply contingency updates."""
    print("\n═══ PHASE 2: CONTINGENCIES ═══")
    data = load_json(CONTINGENCIES_PATH)

    # Build lookup
    cont_map = {c["id"]: c for c in data["contingencies"]}

    # --- C6 environmentalAiPull additions ---
    c6 = cont_map.get("environmentalAiPull")
    if c6:
        added_c6 = 0
        for bucket_name in ["high", "medium", "low"]:
            if bucket_name not in c6:
                continue
            existing = set(c6[bucket_name].get("specimens", []))
            c6[bucket_name].setdefault("specimens", [])

        # Check all specimens in all buckets to avoid duplicates
        all_c6_specimens = set()
        for bucket_name in ["high", "medium", "low"]:
            if bucket_name in c6:
                all_c6_specimens.update(c6[bucket_name].get("specimens", []))

        for spec_id, bucket in C6_ADDITIONS.items():
            if spec_id not in all_c6_specimens:
                c6[bucket]["specimens"].append(spec_id)
                log(f"ADD C6 {spec_id} → {bucket}")
                added_c6 += 1
            else:
                log(f"SKIP C6 {spec_id}: already in contingency")
        print(f"  C6 additions: {added_c6}")
    else:
        print("  WARN: environmentalAiPull not found in contingencies")

    # --- C3 ceoTenure additions ---
    c3 = cont_map.get("ceoTenure")
    if c3:
        added_c3 = 0
        all_c3 = set()
        for bucket_name in ["high", "medium", "low"]:
            if bucket_name in c3:
                all_c3.update(c3[bucket_name].get("specimens", []))

        for spec_id, bucket in C3_ADDITIONS.items():
            if spec_id not in all_c3:
                c3[bucket]["specimens"].append(spec_id)
                log(f"ADD C3 {spec_id} → {bucket}")
                added_c3 += 1
            else:
                log(f"SKIP C3 {spec_id}: already placed")
        print(f"  C3 additions: {added_c3}")

    # --- Other changes (bucket moves) ---
    moves = 0
    for spec_id, cont_id, old_bucket, new_bucket in OTHER_CONTINGENCY_CHANGES:
        c = cont_map.get(cont_id)
        if not c:
            log(f"WARN: {cont_id} not found")
            continue
        # Remove from old bucket
        if old_bucket in c and spec_id in c[old_bucket].get("specimens", []):
            c[old_bucket]["specimens"].remove(spec_id)
        # Add to new bucket
        if new_bucket in c:
            c[new_bucket].setdefault("specimens", [])
            if spec_id not in c[new_bucket]["specimens"]:
                c[new_bucket]["specimens"].append(spec_id)
                log(f"MOVE {cont_id} {spec_id}: {old_bucket} → {new_bucket}")
                moves += 1
    print(f"  Bucket moves: {moves}")

    data["lastUpdated"] = "2026-02-15"

    if not DRY_RUN:
        save_json(CONTINGENCIES_PATH, data)
        print(f"  ✓ Saved {CONTINGENCIES_PATH.name}")
    else:
        print(f"  [DRY RUN] Would save {CONTINGENCIES_PATH.name}")


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3: MECHANISM LINK UPDATES
# ══════════════════════════════════════════════════════════════════════════════

# Format: (mechanism_id, specimenId, strength, notes)
# mechanism_id matches the "id" field in mechanisms.json confirmed array
MECHANISM_ADDITIONS = [
    # Batch A
    (7, "mckinsey", "Moderate", "25K AI agents — senior partners necessarily on the tools."),
    (7, "salesforce", "Moderate", "Customer Zero: Inzerillo personally deploys and evaluates Agentforce."),
    # Batch B
    (10, "amazon-agi", "Strong", "Trainium $10B+ ARR. Bedrock productizes internal model-serving infra."),
    (3, "apple", "Moderate", "AI embedded directly into product surfaces (Siri, keyboard, Photos). Zurich Vision Lab flows to products."),
    (10, "sap", "Moderate", "Joule productizes SAP's deep enterprise process knowledge."),
    # Batch C
    (8, "cedars-sinai", "Moderate", "Dual-reporting CAIO + AI Council governance creates clinical validation infrastructure."),
    (10, "mass-general-brigham", "Moderate", "AIwithCare spinout commercializes clinical trial screening AI."),
    # Batch F
    (10, "palantir", "Strong", "Entire business model is productizing internal data infrastructure. Foundry + AIP."),
    (3, "stripe", "Moderate", "Payments Foundation Model: research-grade ML shipped as production features. $6B recovered via Adaptive Acceptance."),
    (8, "crowdstrike", "Moderate", "Security compliance certifications create trust advantage competitors must match."),
    (11, "recruit-holdings", "Moderate", "4,500 cuts across three waves. Dual-hat CEO is itself delayering."),
    (1, "uber", "Moderate", "ATG divestiture externalized exploration to protect it. AV partnerships protect via external structure."),
    (8, "wells-fargo", "Moderate", "Post-2016 regulatory infrastructure repurposed for AI governance."),
    (1, "xai", "Moderate", "Macrohard is off-strategy relative to chatbot/coding core. Musk authority protects it."),
]

# Apple M6 downgrade: remove or mark as weak
MECHANISM_DOWNGRADES = [
    (6, "apple", "Remove or downgrade — not competing-teams merger; was de-centralization"),
]


def phase3_mechanisms():
    """Apply mechanism specimen link updates."""
    print("\n═══ PHASE 3: MECHANISMS ═══")
    data = load_json(MECHANISMS_PATH)

    mech_map = {m["id"]: m for m in data["confirmed"]}

    added = 0
    for mech_id, spec_id, strength, notes in MECHANISM_ADDITIONS:
        m = mech_map.get(mech_id)
        if not m:
            log(f"WARN: Mechanism {mech_id} not found in confirmed")
            continue

        existing_ids = set(m.get("specimens", []))
        # Also check evidence array
        evidence_ids = {e["specimenId"] for e in m.get("evidence", []) if "specimenId" in e}

        if spec_id not in existing_ids:
            m["specimens"].append(spec_id)

        if spec_id not in evidence_ids:
            m.setdefault("evidence", []).append({
                "specimenId": spec_id,
                "quote": None,
                "speaker": None,
                "source": f"Feb 15, 2026 synthesis batch",
                "notes": f"[{strength}] {notes}"
            })
            log(f"ADD M{mech_id} ← {spec_id} ({strength})")
            added += 1
        else:
            log(f"SKIP M{mech_id} ← {spec_id}: already linked")

    # Handle downgrades
    for mech_id, spec_id, reason in MECHANISM_DOWNGRADES:
        m = mech_map.get(mech_id)
        if m and spec_id in m.get("specimens", []):
            m["specimens"].remove(spec_id)
            # Don't remove evidence — mark it instead
            for e in m.get("evidence", []):
                if e.get("specimenId") == spec_id:
                    e["notes"] = (e.get("notes", "") + f" [Feb 15 DOWNGRADED: {reason}]").strip()
            log(f"DOWNGRADE M{mech_id} ← {spec_id}: {reason}")

    data["lastUpdated"] = "2026-02-15"
    print(f"  Added: {added}")

    if not DRY_RUN:
        save_json(MECHANISMS_PATH, data)
        print(f"  ✓ Saved {MECHANISMS_PATH.name}")
    else:
        print(f"  [DRY RUN] Would save {MECHANISMS_PATH.name}")


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4: NEW INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

NEW_INSIGHTS = [
    {
        "id": "professional-services-firewall-gradient",
        "title": "Professional Services Firms Draw AI Firewalls at the Point of Maximum Rent Extraction",
        "theme": "organizational-form",
        "finding": "Professional services firms create explicit or implicit boundaries between AI-automatable work and protected human expertise. The firewall position correlates with where the firm extracts economic rents: Baker McKenzie protects attorneys (billable hours), Thomson Reuters gates AI with 4K domain experts, McKinsey blurs the boundary toward 1:1 human-agent parity, Salesforce inverts the firewall (AI default, human exception at 2%), Forrester removes it entirely (product automated). The gradient runs from hardest firewalls in regulated high-rent-extraction roles to no firewall where the product itself is automated.",
        "evidence": [
            {"specimenId": "baker-mckenzie", "note": "Attorney exclusion firewall — support staff fully exposed, attorneys fully protected"},
            {"specimenId": "thomson-reuters", "note": "4K+ SME evaluation layer gates AI outputs before deployment"},
            {"specimenId": "mckinsey", "note": "Dissolving boundary — 25K agents alongside 40K humans, 1:1 target"},
            {"specimenId": "salesforce", "note": "Inverted firewall — 84% AI resolution, humans handle 2% escalations"},
            {"specimenId": "forrester", "note": "No firewall — Forrester AI product directly replaces human analyst delivery"}
        ],
        "theoreticalConnection": "Barzel (1997) on property rights and rent extraction: the firm draws the AI boundary where human judgment is hardest to replicate and generates the highest rents.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-a-professional-services.md",
        "relatedTensions": [1],
        "maturity": "emerging"
    },
    {
        "id": "explorer-to-operator-leadership-succession",
        "title": "AI Product Leadership Follows an Explorer-to-Operator Succession Pattern",
        "theme": "leadership",
        "finding": "Salesforce cycled through three AI leaders in under three years with progressively narrowing scope: Clara Shih (CEO of Salesforce AI, visionary) → Adam Evans (EVP/GM, builder) → Madhav Thattai (EVP/GM Agentforce, operator). Each transition narrowed the mandate from strategic AI leadership to operational product management, mirroring the exploration-to-execution transition predicted by ambidexterity theory.",
        "evidence": [
            {"specimenId": "salesforce", "note": "Three AI leaders in <3 years: Shih → Evans → Thattai, progressively narrowing scope"},
            {"specimenId": "thomson-reuters", "note": "Inverse trajectory: Hron elevated from startup CTO through three roles (operator → visionary)"}
        ],
        "theoreticalConnection": "Henderson and Clark on architectural innovation: organizational challenge shifts from invention to integration as technology matures. Holmstrom: visionary leaders tolerate ambiguity (incomplete contracts); operators require specified deliverables.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-a-professional-services.md",
        "relatedTensions": [5],
        "maturity": "emerging"
    },
    {
        "id": "alliance-mediated-ai-capability",
        "title": "Firms with High Technical Debt Default to Alliance-Mediated AI Capability",
        "theme": "organizational-form",
        "finding": "Kyndryl builds AI capabilities through hyperscaler partnerships (100 agents in 100 days with Google Cloud) rather than internal R&D. Hypothesis: firms with high technical debt (C5) and constrained talent markets (C4) default to alliance-mediated AI because transaction costs of partnerships are lower than internal costs of building from scratch.",
        "evidence": [
            {"specimenId": "kyndryl", "note": "Alliance-driven agent development with Google Cloud, Microsoft, NVIDIA, SAP"},
            {"specimenId": "capgemini", "note": "Country-specific workforce adaptation may be partner-mediated"},
            {"specimenId": "nextera-energy", "note": "Google Cloud partnership provides AI capability as a service"}
        ],
        "theoreticalConnection": "Coase (1937) on boundary of the firm: alliance-mediated capability when internal costs exceed transaction costs. Williamson (1975) on asset specificity: generic AI capabilities obtainable through alliances; firm-specific must be built.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-a-professional-services.md",
        "relatedTensions": [1, 3],
        "maturity": "hypothesis"
    },
    {
        "id": "healthcare-dual-authority-governance",
        "title": "Healthcare AI Governance Consistently Produces Dual-Authority Structures",
        "theme": "organizational-form",
        "finding": "Healthcare AI governance produces dual-authority structures because clinical AI decisions require two types of expertise (technical and clinical) that do not co-reside in any single leader. Solutions include dual-reporting CAIO (Cedars-Sinai), multi-hub C-suite (Mayo), CAIO + CDTO (Mount Sinai), dual-hat CMIO/CAIO (Kaiser), CDAIO + CXO (CVS). This is distinct from matrix management — it distributes the governance function across two leaders with complementary domains.",
        "evidence": [
            {"specimenId": "cedars-sinai", "note": "Dual-reporting CAIO (CIO + CMO). Distributed informatics officers (CHIO, CNIO, CMIO)."},
            {"specimenId": "mayo-clinic", "note": "Multi-hub C-suite: CAIO + CDAO + Platform"},
            {"specimenId": "mount-sinai-health-system", "note": "CAIO + CDTO dual leadership"},
            {"specimenId": "sutter-health", "note": "Clinician-CAIO model"},
            {"specimenId": "cvs-health", "note": "Anti-CAIO stance but CDAIO + CXO dual structure"},
            {"specimenId": "kaiser-permanente", "note": "Dual-hat CMIO/CAIO — cheapest variant, absorbs AI into existing role"}
        ],
        "theoreticalConnection": "Information cost problem: clinical AI requires bridging technical and clinical epistemologies. Dual-authority structures minimize information loss at the domain boundary.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-c-healthcare-pharma-energy.md",
        "relatedTensions": [1, 3],
        "maturity": "emerging"
    },
    {
        "id": "founder-authority-m6a-regulated",
        "title": "Founder Authority Is a Necessary Condition for M6a Contextual Adoption in Regulated Industries",
        "theme": "contingency",
        "finding": "Moderna (founder-led) achieved M6a contextual adoption in pharma with 100% proficiency mandate. No non-founder-led pharma company in the collection has achieved M6a. Founder authority provides the legitimacy to override organizational resistance that regulated industries impose on radical structural choices. Extends the broader founder-authority insight with a specific testable prediction about structural model boundaries.",
        "evidence": [
            {"specimenId": "moderna", "note": "Bancel (founder, 15yr) mandated 100% AI proficiency in 6 months"},
            {"specimenId": "shopify", "note": "Lutke (founder) imposed 'prove AI can't do it' headcount policy"},
            {"specimenId": "eli-lilly", "note": "Ricks (long tenure, not founder) achieved M4 deep separation, not M6a"},
            {"specimenId": "astrazeneca", "note": "Soriot (14yr tenure) achieved federated M4, not M6a"}
        ],
        "theoreticalConnection": "Extends founder-authority-structural-enabler: it is not tenure length but FOUNDER STATUS that predicts whether M6a contextual ambidexterity is feasible in regulated industries.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-c-healthcare-pharma-energy.md",
        "relatedTensions": [1],
        "maturity": "hypothesis"
    },
    {
        "id": "buy-exploration-protect-execution",
        "title": "Media/Entertainment Companies Outsource AI Exploration While Protecting IP Execution",
        "theme": "organizational-form",
        "finding": "Media/entertainment companies with valuable IP systematically outsource AI exploration to external partners while keeping execution internal. The logic: building generative AI internally risks creating tools that could leak or replicate the IP moat. Partnering externalizes exploration risk while maintaining IP control through licensing. Counter-example: Netflix builds AI internally because its moat is recommendation (hard to replicate from proprietary user data), not content IP.",
        "evidence": [
            {"specimenId": "disney", "note": "$1B OpenAI/Sora partnership — buy generative capability, protect IP"},
            {"specimenId": "lionsgate", "note": "Runway AI model trained on proprietary content — partnership, not internal build"},
            {"specimenId": "comcast---nbcuniversal", "note": "LIFT Labs accelerator absorbs startup AI capabilities"},
            {"specimenId": "netflix", "note": "COUNTER-EXAMPLE: builds AI internally (9 research areas, AIMS, Eyeline). Moat is recommendation, not IP."}
        ],
        "theoreticalConnection": "Teece (1986) complementary assets: when appropriability is weak (AI models replicable), firms with strong complementary assets (IP) control the assets and outsource the technology.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-d-consumer-retail-media.md",
        "relatedTensions": [1, 2],
        "maturity": "emerging"
    },
    {
        "id": "technical-debt-predicts-contextual-structural",
        "title": "Technical Debt Predicts Contextual vs. Structural AI Organizational Choice",
        "theme": "contingency",
        "finding": "Low-debt organizations adopt contextual models (M3/M6); high-debt organizations adopt structural models (M2/M4). The mechanism: universal AI tool provisioning (enabling contextual adoption) requires modern, homogeneous infrastructure. Legacy systems create interface complexity that demands structural separation between AI teams and operational teams. The relationship is gradient, not binary.",
        "evidence": [
            {"specimenId": "shopify", "note": "Low debt → M6a contextual. Cloud-native, modern stack."},
            {"specimenId": "netflix", "note": "Low debt → M3 contextual. Cloud-native, Metaflow."},
            {"specimenId": "spotify", "note": "Low debt → M4 contextual. Cloud-native."},
            {"specimenId": "walmart", "note": "High debt → M4 structural. Legacy retail systems, 10,500+ stores."},
            {"specimenId": "comcast---nbcuniversal", "note": "High debt → M5a structural. Legacy cable infrastructure."},
            {"specimenId": "nike", "note": "Medium debt → M2+M3 transitional. Intermediate position on gradient."}
        ],
        "theoreticalConnection": "Infrastructure homogeneity as a precondition for contextual integration. Williamson's asset specificity applied to internal IT: heterogeneous legacy systems are 'specific assets' requiring dedicated governance structures.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-d-consumer-retail-media.md",
        "relatedTensions": [1],
        "maturity": "emerging"
    },
    {
        "id": "capital-intensity-constrains-ai-structure",
        "title": "Capital Intensity Constrains AI Structural Choice Toward Hub-and-Spoke or Embedded Models",
        "theme": "contingency",
        "finding": "Capital-intensive industries systematically favor M4 or M6 over M1/M5 because AI must integrate with physical infrastructure. AI is a component of the physical product, not a standalone product. The constraint operates through three channels: (1) physical infrastructure creates rigid investment cycles, (2) AI value is measurable only through operational improvements, (3) high technical debt in legacy systems forces augmentation rather than replacement.",
        "evidence": [
            {"specimenId": "ups", "note": "M6, $9B automation investment integrated with physical sorting infrastructure"},
            {"specimenId": "panasonic", "note": "M4, manufacturing AI must integrate with 230K-employee industrial operations"},
            {"specimenId": "bosch-bcai", "note": "M1+M3, research center + embedded division teams for diverse physical products"},
            {"specimenId": "asml", "note": "M6b, AI optimizes 100K parameters per wafer within existing lithography machines"},
            {"specimenId": "rivian", "note": "M4+M5, custom silicon + Large Driving Model integrated with vehicle platform"},
            {"specimenId": "hp-inc", "note": "M4+M5a, HP IQ lab serves physical product lines (PCs, printers)"}
        ],
        "theoreticalConnection": "Williamson (1985) on asset specificity: capital-intensive firms have high asset specificity in physical infrastructure, constraining organizational design choices.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-e-industrial-logistics.md",
        "relatedTensions": [1, 5],
        "maturity": "emerging"
    },
    {
        "id": "simultaneous-cut-and-invest",
        "title": "Workforce Reduction and AI Investment Are Simultaneous, Not Sequential",
        "theme": "organizational-form",
        "finding": "Multiple specimens combine workforce reduction with AI investment in the same restructuring. This contradicts sequential models (cut first then invest, or invest first then cut) in favor of simultaneity where cost savings and capability investment are structurally intertwined. Exploitation savings fund exploration investments in the same organizational moment.",
        "evidence": [
            {"specimenId": "ups", "note": "-78K positions + $9B automation investment"},
            {"specimenId": "hp-inc", "note": "-4-6K positions + $116M Humane acquisition for HP IQ lab"},
            {"specimenId": "asml", "note": "-1,700 management positions + Google Cloud/Mistral AI partnerships"},
            {"specimenId": "accenture-openai", "note": "-11K positions + 77K AI hires ($865M restructuring)"},
            {"specimenId": "intel", "note": "-24K positions + GPU architect hire from AMD/Qualcomm"}
        ],
        "theoreticalConnection": "March (1991) on simultaneous exploration and exploitation. The simultaneous cut-and-invest is ambidexterity at the resource allocation level.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-e-industrial-logistics.md",
        "relatedTensions": [2, 5],
        "maturity": "emerging"
    },
    {
        "id": "moat-determines-ai-structure",
        "title": "Organizations Structurally Separate AI When AI Is Constitutive of Competitive Advantage",
        "theme": "contingency",
        "finding": "When AI is constitutive of competitive advantage, firms structurally separate it (Arm Physical AI division, Rivian autonomy hub). When AI is complementary to a non-AI competitive advantage, firms embed AI operationally (ASML where moat is physics, NextEra where moat is physical assets). The distinguishing question: does AI define the competitive advantage or enhance a non-AI advantage?",
        "evidence": [
            {"specimenId": "arm-holdings", "note": "AI-constitutive: Physical AI division structurally separated for future AI chip architecture"},
            {"specimenId": "rivian", "note": "AI-constitutive: multi-hub autonomy structure, custom silicon, structural firewall for AI work"},
            {"specimenId": "asml", "note": "AI-complementary: moat is physics/optics, AI embedded operationally, no AI structure"},
            {"specimenId": "nextera-energy", "note": "AI-complementary: moat is physical assets, AI via Google Cloud partnership"}
        ],
        "theoreticalConnection": "Teece (2007) dynamic capabilities: structural separation of AI is justified when AI is the source of dynamic capability, not when AI merely supports existing capabilities.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-e-industrial-logistics.md",
        "relatedTensions": [1],
        "maturity": "hypothesis"
    },
    {
        "id": "machine-mediated-ambidexterity",
        "title": "Autonomous AI Agents May Partially Resolve the Exploration-Execution Tension",
        "theme": "organizational-form",
        "finding": "Three very different organizations independently developed multi-agent architectures where autonomous AI agents handle routine execution (fixing bugs, processing alerts), potentially freeing human attention for exploration. If agents handle execution, the exploration/execution tension may be partially resolved through human-machine work allocation rather than organizational design.",
        "evidence": [
            {"specimenId": "stripe", "note": "'Minions' write 5% of PRs (30% during Fix-It Week) — autonomous dev agents"},
            {"specimenId": "crowdstrike", "note": "Charlotte AI's 12+ specialized agents orchestrate for threat detection"},
            {"specimenId": "xai", "note": "Macrohard aspires to staff entire software company with AI agents"}
        ],
        "theoreticalConnection": "Smith (1776) and Becker & Murphy (1992) division of labor applied to AI systems. If execution is delegated to machines, the exploration/execution tension becomes a human-machine allocation problem rather than an organizational design problem.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-f-new-and-reclass.md",
        "relatedTensions": [1, 2],
        "maturity": "hypothesis"
    },
    {
        "id": "delayering-three-mechanisms",
        "title": "Management Delayering in the AI Era Encompasses Three Distinct Mechanisms",
        "theme": "mechanism",
        "finding": "AI-era management delayering is at least three distinct phenomena, not one: (1) Automation-driven substitution — AI replaces the information-aggregation function (UPS, purest Garicano mechanism); (2) Efficiency-driven simplification — management layers cut to improve speed regardless of AI (ASML, matrix-to-product reorganization); (3) Investment-driven restructuring — headcount reduction creates budget for AI capability (HP Inc., resource reallocation). The Garicano connection applies cleanly only to mechanism 1.",
        "evidence": [
            {"specimenId": "ups", "note": "Mechanism 1: AI algorithms route packages, replacing middle managers who aggregated facility data"},
            {"specimenId": "asml", "note": "Mechanism 2: 'trim bloat to make sure engineers can be engineers again' — matrix simplification"},
            {"specimenId": "hp-inc", "note": "Mechanism 3: 4-6K cuts fund $116M Humane acquisition for AI capability"},
            {"specimenId": "fedex", "note": "Mechanism 3 variant: worker augmentation widens spans of control, indirectly reducing management need"}
        ],
        "theoreticalConnection": "Garicano (2000) knowledge hierarchies: mechanism 1 is direct substitution of the routing function; mechanisms 2 and 3 are organizational responses to AI that reduce management without AI directly replacing managers.",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-e-industrial-logistics.md",
        "relatedTensions": [1, 3],
        "maturity": "emerging"
    },
    {
        "id": "m4-overcount-discriminator",
        "title": "Hub-and-Spoke (M4) Was Over-Applied; the Discriminating Question Is Bidirectional Coordination",
        "theme": "taxonomy",
        "finding": "The Feb 2026 M4 audit revealed systematic over-classification: 7 of 8 specimens in the Big Tech batch were reclassified away from M4. Any org with a named central AI function and distributed teams looks like hub-and-spoke from outside, but M4 requires active bidirectional coordination. The discriminating question: 'Does the central entity provide shared AI infrastructure that distributed units depend on?' If no → M1+M3 or M3; if the entity builds a product → M5.",
        "evidence": [
            {"specimenId": "amazon-agi", "note": "M4→M1+M3: AGI org does research, product teams do AI independently. No coordination loop."},
            {"specimenId": "meta-ai", "note": "M4→M1+M3: MSL is research, product teams embed AI independently."},
            {"specimenId": "apple", "note": "M4→M3: AI distributed across SVPs without coordinating hub."},
            {"specimenId": "sap", "note": "M4→M5a+M2: Joule is a product, not a hub coordinating spokes."},
            {"specimenId": "servicenow", "note": "M4→M5a+M6a: AI IS the product, not a separate organizational function."}
        ],
        "theoreticalConnection": "Classification accuracy depends on distinguishing coordination mechanisms (hub-and-spoke) from colocation (research lab + embedded teams) and product development (AI product company).",
        "discoveredIn": "synthesis/sessions/2026-02-15-batch-b-big-tech-reclass.md",
        "relatedTensions": [1, 3],
        "maturity": "confirmed"
    },
]


def phase4_insights():
    """Add new insights from the synthesis batches."""
    print("\n═══ PHASE 4: NEW INSIGHTS ═══")
    data = load_json(INSIGHTS_PATH)

    existing_ids = {i["id"] for i in data["insights"]}
    added = 0
    for insight in NEW_INSIGHTS:
        if insight["id"] not in existing_ids:
            data["insights"].append(insight)
            log(f"ADD insight: {insight['id']} ({insight['maturity']})")
            added += 1
        else:
            log(f"SKIP insight: {insight['id']} — already exists")

    data["lastUpdated"] = "2026-02-15"
    print(f"  Added: {added}")

    if not DRY_RUN:
        save_json(INSIGHTS_PATH, data)
        print(f"  ✓ Saved {INSIGHTS_PATH.name}")
    else:
        print(f"  [DRY RUN] Would save {INSIGHTS_PATH.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    global DRY_RUN

    parser = argparse.ArgumentParser(description="Apply Feb 15 synthesis batch patches")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--phase", default="all", help="Phase to run: 1|2|3|4|all")
    args = parser.parse_args()
    DRY_RUN = args.dry_run

    print("╔════════════════════════════════════════════════╗")
    print("║  Feb 15, 2026 — Synthesis Batch Patch Script   ║")
    print("║  7 batches, 62 specimens                       ║")
    print(f"║  Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}                                  ║")
    print("╚════════════════════════════════════════════════╝")

    phases = args.phase
    if phases == "all":
        phase1_tensions()
        phase2_contingencies()
        phase3_mechanisms()
        phase4_insights()
    elif phases == "1":
        phase1_tensions()
    elif phases == "2":
        phase2_contingencies()
    elif phases == "3":
        phase3_mechanisms()
    elif phases == "4":
        phase4_insights()

    # Summary
    print(f"\n{'═' * 50}")
    print(f"Total changes logged: {len(CHANGES)}")
    if DRY_RUN:
        print("DRY RUN — no files were modified")

    # Write changelog entry
    if not DRY_RUN and CHANGES:
        write_changelog("patch-synthesis-feb15.py", CHANGES)
        print("✓ Changelog updated")


if __name__ == "__main__":
    main()
