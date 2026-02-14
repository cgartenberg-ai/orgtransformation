#!/usr/bin/env python3
"""Enrich healthcare specimens with sector deep dive findings (Feb 10, 2026).

Focuses on incremental enrichments — these specimens are already High completeness.
Most value from the deep dive is in sector observations and new specimen candidates,
not in updating existing specimens.
"""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent / "specimens"

# =============================================
# 1. SUTTER HEALTH — clinician-CAIO detail + metric
# =============================================
sutter_path = BASE / "sutter-health.json"
with open(sutter_path) as f:
    sutter = json.load(f)

# Add Beecy clinician-CAIO detail to reporting structure
sutter["observableMarkers"]["reportingStructure"] = (
    "CAIO (Ashley Beecy, MD — cardiologist by training, appointed May 2025). "
    "CLINICIAN-CAIO variant: physician background rather than technologist — "
    "one of three healthcare CAIO variants identified (clinician-CAIO, technologist-CAIO, dual-hat CMIO/CAIO). "
    "CDO (Laura Wilt) handles digital deployment. CIO, CCIO, CDAO also present — "
    "multiple C-suite AI-adjacent roles suggest high organizational priority. "
    "Beecy: 'Working to responsibly operationalize clinical AI at scale, while staying grounded "
    "in what matters most, better care and meaningful support for both clinicians and patients.'"
)

# Add 1.5M hours saved metric
sutter["observableMarkers"]["metrics"] = (
    "1.5 million hours saved in 2025 via automation, AI-powered tools, enhanced technology, "
    "and workflow improvements. Patient safety, privacy protection, accuracy, transparency for "
    "direct care AI. Physician adoption: 3,200+ on ambient docs. Diagnostic improvement: "
    "Ferrum platform 430,000 records processed, 1,850 missed pulmonary nodules caught."
)

# Add Aidoc vendor partnership
new_sutter_source = {
    "id": "sutter-aidoc-prnewswire-2025",
    "name": "PRNewswire — Sutter Health and Aidoc AI Partnership",
    "type": "Press Release",
    "url": "https://www.prnewswire.com/news-releases/sutter-health-and-aidoc-team-up-to-transform-patient-care-with-advanced-clinical-ai-302488965.html",
    "publicationDate": "2025-06",
    "collectedDate": "2026-02-10",
    "notes": "Aidoc aiOS real-time AI operating system embedded across Sutter's care system."
}
existing_ids = {s["id"] for s in sutter["sources"]}
if new_sutter_source["id"] not in existing_ids:
    sutter["sources"].append(new_sutter_source)

# Add Beecy quote
new_sutter_quote = {
    "text": "Working to responsibly operationalize clinical AI at scale, while staying grounded in what matters most, better care and meaningful support for both clinicians and patients.",
    "speaker": "Dr. Ashley Beecy",
    "speakerTitle": "Chief AI Officer, Sutter Health",
    "source": "Sutter Health Vitals Blog",
    "sourceUrl": "https://vitals.sutterhealth.org/practical-progress-building-the-future-of-care-through-digital-health/",
    "sourceDate": "2025-12-22",
    "context": "Describing CAIO role and governance-first philosophy"
}
existing_quotes = {q.get("text", "") for q in sutter.get("quotes", [])}
if new_sutter_quote["text"] not in existing_quotes:
    sutter["quotes"].append(new_sutter_quote)

sutter["meta"]["lastUpdated"] = "2026-02-10"

with open(sutter_path, "w") as f:
    json.dump(sutter, f, indent=2, ensure_ascii=False)
print(f"✅ Sutter Health enriched — Sources: {len(sutter['sources'])}, Quotes: {len(sutter['quotes'])}")

# =============================================
# 2. UNITEDHEALTH GROUP — Optum tripartite + governance failure + talent flow
# =============================================
uhg_path = BASE / "unitedhealth-group.json"
with open(uhg_path) as f:
    uhg = json.load(f)

# Add Optum tripartite structure detail
old_rs = uhg["observableMarkers"]["reportingStructure"]
uhg["observableMarkers"]["reportingStructure"] = (
    "AI reports through Chief Digital & Technology Officer (Dadlani) and Chief AI Scientist (Pencina). "
    "Responsible AI Board (20-25 experts) provides oversight. Monthly business unit reviews, quarterly CIO monitoring. "
    "OPTUM TRIPARTITE STRUCTURE: Optum Insight (data analytics/technology — built Optum Real system), "
    "Optum Health (care delivery), Optum Rx (pharmacy benefits). AI built in one division (Insight), "
    "deployed across others. Former naviHealth subsidiary (controversial claims denial algorithm) "
    "absorbed into Optum — no longer a named subsidiary. "
    "Former CAIO Dennis Chornenky left for UC Davis Health as Chief AI Adviser (title downgrade: Officer → Adviser)."
)

# Add governance failure metric to description layer
new_uhg_layer = {
    "date": "2026-02",
    "label": "Healthcare Deep Dive — Governance Failure + Talent Flow",
    "summary": (
        "Healthcare sector comparative research (Feb 10, 2026) reveals structural governance concerns: "
        "(1) Optum Real AI pre-authorization system reviews claims BEFORE treatment — prospective gatekeeping, "
        "not retrospective review. Minnesota federal court (Feb 2025) ruled breach of contract claims can "
        "proceed because contracts specified clinical staff, not algorithms, make coverage decisions. "
        "(2) Denial rate doubled 2020-2022 after algorithmic review; 90% of denials overturned on appeal by "
        "federal administrative law judges — suggesting AI governance optimized for throughput over accuracy. "
        "(3) Former CAIO Dennis Chornenky left for UC Davis Health — talent flow from payer to provider AI."
    ),
    "sourceRefs": ["uhg-healthcare-deep-dive-2026"]
}
uhg["layers"].insert(0, new_uhg_layer)

# Add source
new_uhg_sources = [
    {
        "id": "uhg-healthcare-deep-dive-2026",
        "name": "Healthcare sector deep dive research — UnitedHealth findings",
        "type": "research",
        "url": "n/a — compiled from multiple search results",
        "publicationDate": "2025-2026",
        "collectedDate": "2026-02-10",
        "notes": "Optum tripartite structure, Optum Real pre-authorization, Minnesota court ruling, "
                 "90% denial overturn rate, Chornenky departure to UC Davis."
    },
    {
        "id": "bankinfosecurity-uhg-ai-claims-2025",
        "name": "BankInfoSecurity — Court: UnitedHealth Must Answer for AI-Based Claim Denials",
        "type": "press",
        "url": "https://www.bankinfosecurity.com/court-unitedhealth-must-answer-for-ai-based-claim-denials-a-27534",
        "publicationDate": "2025",
        "collectedDate": "2026-02-10",
        "notes": "Minnesota federal court ruling: breach of contract because contracts specified human clinical staff."
    }
]
existing_ids = {s["id"] for s in uhg["sources"]}
for src in new_uhg_sources:
    if src["id"] not in existing_ids:
        uhg["sources"].append(src)

# Add open questions about governance failure
uhg["openQuestions"].extend([
    "Who replaced Dennis Chornenky as Optum CAIO after he departed?",
    "How does AI governance differ between Optum Insight (technology/analytics) and Optum Health (care delivery)?",
    "What changes were made to AI governance after the Minnesota federal court ruling and DOJ scrutiny?",
    "What is the current status of the naviHealth algorithm after absorption into Optum?"
])

uhg["meta"]["lastUpdated"] = "2026-02-10"

with open(uhg_path, "w") as f:
    json.dump(uhg, f, indent=2, ensure_ascii=False)
print(f"✅ UnitedHealth enriched — Sources: {len(uhg['sources'])}, Layers: {len(uhg['layers'])}")

# =============================================
# 3. MOUNT SINAI — distributed leadership detail
# =============================================
mt_path = BASE / "mount-sinai-health-system.json"
with open(mt_path) as f:
    mt = json.load(f)

# Update reporting structure with specific named leaders
mt["observableMarkers"]["reportingStructure"] = (
    "NO SINGLE CAIO — distributed leadership across specialized roles: "
    "Lisa Stump (EVP, Chief Digital Information Officer and Dean of IT at Icahn School of Medicine), "
    "Robbie Freeman (VP for Digital Experience and Chief Nursing Informatics Officer), "
    "Nicholas Gavin (VP, Chief Clinical Innovation Officer, Associate CMIO for Digital Health). "
    "AI leadership distributed across CDIO, CNIO, CCIO roles rather than unified under single CAIO. "
    "Windreich Department of AI and Human Health led by Girish Nadkarni (Chief AI Officer for academic function). "
    "Domain-specific AI sub-centers: Center for AI in Children's Health (indicating segmentation by patient population). "
    "Microsoft Dragon Copilot rolled out system-wide — major ambient clinical AI vendor partnership."
)

new_mt_source = {
    "id": "mount-sinai-dragon-copilot-2025",
    "name": "Mount Sinai Health System — Microsoft Dragon Copilot Rollout",
    "type": "press-release",
    "url": "https://www.mountsinai.org/about/newsroom/2025/mount-sinai-health-system-to-roll-out-microsoft-dragon-copilot",
    "publicationDate": "2025",
    "collectedDate": "2026-02-10",
    "notes": "System-wide Dragon Copilot deployment. Named leaders: Stump (CDIO), Freeman (CNIO), Gavin (CCIO)."
}
existing_ids = {s["id"] for s in mt["sources"]}
if new_mt_source["id"] not in existing_ids:
    mt["sources"].append(new_mt_source)

mt["meta"]["lastUpdated"] = "2026-02-10"

with open(mt_path, "w") as f:
    json.dump(mt, f, indent=2, ensure_ascii=False)
print(f"✅ Mount Sinai enriched — Sources: {len(mt['sources'])}")

# =============================================
# 4. MAYO CLINIC — Department + Platform detail
# =============================================
mayo_path = BASE / "mayo-clinic.json"
with open(mayo_path) as f:
    mayo = json.load(f)

# Update with department-level authority detail
old_rs = mayo["observableMarkers"]["reportingStructure"]
if "research DEPARTMENT" not in old_rs:
    mayo["observableMarkers"]["reportingStructure"] = (
        "CAIO (Tripathi) and CDAO (Sehgal) are distinct C-suite roles. "
        "Mayo Clinic Platform (Halamka) is a separate commercialization unit. "
        "DEPARTMENT of AI and Informatics (not a center or initiative) — has permanent budget authority "
        "and academic standing within the research division, giving AI research organizational permanence. "
        "Mayo Clinic Platform has three sub-units: Platform_Accelerate (startup incubator), "
        "Platform_Insights (quality improvement for other health systems), "
        "Platform_Orchestrate (clinical trials acceleration). "
        "Clinical AI execution is clinician-led with department heads driving domain-specific AI. "
        "Multi-agent research system using tournament framework (Generation, Reflection, Ranking, "
        "Evolution, Proximity agents) for hypothesis generation."
    )

mayo["meta"]["lastUpdated"] = "2026-02-10"

with open(mayo_path, "w") as f:
    json.dump(mayo, f, indent=2, ensure_ascii=False)
print(f"✅ Mayo Clinic enriched — reporting structure updated with department authority detail")

# =============================================
# 5. CVS HEALTH — unified platform + metrics
# =============================================
cvs_path = BASE / "cvs-health.json"
with open(cvs_path) as f:
    cvs = json.load(f)

# Add Mandadi quote
new_cvs_quote = {
    "text": "AI is not an add-on to this platform. It is embedded end to end - from personalization to workflow automation.",
    "speaker": "Tilak Mandadi",
    "speakerTitle": "EVP, Chief Experience and Technology Officer, CVS Health",
    "source": "Digital Commerce 360",
    "sourceUrl": "https://www.digitalcommerce360.com/2026/01/05/cvs-health-ai-digital-strategy/",
    "sourceDate": "2026-01-05",
    "context": "Describing AI-native consumer engagement platform connecting Pharmacy, Caremark, Aetna, and Oak Street Health"
}
existing_quotes = {q.get("text", "") for q in cvs.get("quotes", [])}
if new_cvs_quote["text"] not in existing_quotes:
    cvs["quotes"].append(new_cvs_quote)

# Add cross-business platform detail to description markers
old_ra = cvs["observableMarkers"]["resourceAllocation"]
if "300+ claims/second" not in old_ra:
    cvs["observableMarkers"]["resourceAllocation"] = (
        "$20B tech modernization over 10 years with AI central. $1B+ in operational savings reinvested. "
        "AI-native consumer engagement platform connects CVS Pharmacy, CVS Caremark, Aetna, and Oak Street Health "
        "into single digital interface — unified rather than federated. "
        "Business-unit-specific AI: Aetna (90 min/day saved per nurse, 30% call center reduction, "
        "4 care management systems → 1), Caremark (300+ claims/sec at peak), "
        "Oak Street Health (ambient AI scribe at 90% of facilities). "
        "'Engagement as a service' positions AI as horizontal capability across all four businesses."
    )

new_cvs_source = {
    "id": "digitalcommerce360-cvs-ai-strategy-2026",
    "name": "Digital Commerce 360 — CVS Health AI Digital Strategy",
    "type": "press",
    "url": "https://www.digitalcommerce360.com/2026/01/05/cvs-health-ai-digital-strategy/",
    "publicationDate": "2026-01-05",
    "collectedDate": "2026-02-10",
    "notes": "AI-native consumer engagement platform. Mandadi: 'AI is not an add-on...embedded end to end.'"
}
existing_ids = {s["id"] for s in cvs["sources"]}
if new_cvs_source["id"] not in existing_ids:
    cvs["sources"].append(new_cvs_source)

cvs["meta"]["lastUpdated"] = "2026-02-10"

with open(cvs_path, "w") as f:
    json.dump(cvs, f, indent=2, ensure_ascii=False)
print(f"✅ CVS Health enriched — Sources: {len(cvs['sources'])}, Quotes: {len(cvs['quotes'])}")

print("\n🏥 All 5 healthcare specimens enriched with deep dive findings.")
