"""
Apply Purpose Claims Taxonomy v2.0 reclassifications.

v1.0 (7 types): utopian, identity, teleological, transformation-framing,
                employee-deal, sacrifice-justification, direction-under-uncertainty

v2.0 (7 types including unclassified): utopian, identity, teleological,
                higher-calling, survival, commercial-success, unclassified

- No claims are deleted. Claims that don't fit v2.0 go to "unclassified".
- All reclassifications preserve existing fields (rhetoricalFunction, notes, etc.)
- Only claimType is changed; secondaryType references to old types are cleared.
"""

import json
import copy
from collections import Counter

REGISTRY_PATH = "research/purpose-claims/registry.json"

# ============================================================
# RECLASSIFICATION MAP
# key = claim ID, value = new v2.0 type
# Only IDs that CHANGE are listed here.
# Claims not listed keep their current type (utopian/teleological/identity stay).
# ============================================================

RECLASSIFICATIONS = {
    # === EMPLOYEE-DEAL (37 claims) ===
    "meta-ai--005": "commercial-success",
    "meta-ai--006": "commercial-success",
    "amazon-agi--005": "unclassified",
    "anthropic--009": "identity",
    "anthropic--012": "identity",
    "eli-lilly--002": "identity",
    "microsoft--013": "survival",
    "microsoft--014": "survival",
    "shopify--001": "unclassified",
    "shopify--002": "unclassified",
    "shopify--003": "unclassified",
    "shopify--005": "unclassified",
    "accenture-openai--001": "survival",
    "accenture-openai--006": "survival",
    "salesforce--005": "unclassified",
    "salesforce--006": "commercial-success",
    "klarna--003": "identity",
    "roche-genentech--005": "identity",
    "roche-genentech--006": "identity",
    "roche-genentech--013": "identity",
    "roche-genentech--014": "commercial-success",
    "sanofi--005": "commercial-success",
    "google-x--004": "identity",
    "ubs--004": "identity",
    "commonwealth-bank--002": "commercial-success",
    "commonwealth-bank--010": "commercial-success",
    "wells-fargo--006": "survival",
    "bank-of-america--003": "commercial-success",
    "bank-of-america--010": "commercial-success",
    "pg-chatpg--002": "commercial-success",
    "pg-chatpg--009": "commercial-success",
    "databricks--013": "unclassified",
    "walmart--007": "commercial-success",
    "walmart--008": "unclassified",
    "walmart--012": "unclassified",
    "moderna--007": "unclassified",
    "deloitte--003": "identity",

    # === SACRIFICE-JUSTIFICATION (24 claims) ===
    "meta-ai--004": "teleological",
    "amazon-agi--001": "identity",
    "anthropic--004": "higher-calling",
    "anthropic--005": "higher-calling",
    "eli-lilly--007": "higher-calling",
    "accenture-openai--008": "identity",
    "salesforce--009": "unclassified",
    "klarna--001": "unclassified",
    "klarna--005": "unclassified",
    "novo-nordisk--005": "commercial-success",
    "roche-genentech--003": "survival",
    "roche-genentech--010": "teleological",
    "sanofi--007": "survival",
    "sanofi--011": "survival",
    "google-x--003": "identity",
    "google-x--005": "identity",
    "ups--004": "survival",
    "commonwealth-bank--013": "commercial-success",
    "wells-fargo--005": "survival",
    "wells-fargo--007": "commercial-success",
    "bank-of-america--011": "commercial-success",
    "databricks--006": "identity",
    "walmart--006": "survival",
    "walmart--011": "higher-calling",

    # === TRANSFORMATION-FRAMING (59 claims) ===
    "meta-ai--003": "commercial-success",
    "anthropic--014": "identity",
    "microsoft--004": "commercial-success",
    "microsoft--007": "identity",
    "microsoft--011": "identity",
    "microsoft--012": "identity",
    "shopify--004": "utopian",
    "accenture-openai--003": "utopian",
    "salesforce--002": "unclassified",
    "klarna--006": "unclassified",
    "klarna--007": "unclassified",
    "sk-telecom--002": "identity",
    "pfizer--001": "survival",
    "pfizer--004": "commercial-success",
    "pfizer--008": "teleological",
    "pfizer--009": "commercial-success",
    "novo-nordisk--003": "teleological",
    "novo-nordisk--006": "survival",
    "novo-nordisk--010": "identity",
    "roche-genentech--001": "survival",
    "roche-genentech--002": "survival",
    "roche-genentech--017": "commercial-success",
    "sanofi--004": "survival",
    "sanofi--006": "identity",
    "sanofi--009": "teleological",
    "sanofi--013": "commercial-success",
    "google-x--010": "identity",
    "ubs--005": "commercial-success",
    "ubs--008": "commercial-success",
    "ubs--010": "commercial-success",
    "ups--003": "identity",
    "ups--005": "survival",
    "ups--007": "identity",
    "ups--011": "commercial-success",
    "ups--014": "commercial-success",
    "commonwealth-bank--003": "commercial-success",
    "commonwealth-bank--008": "commercial-success",
    "commonwealth-bank--012": "commercial-success",
    "wells-fargo--001": "survival",
    "wells-fargo--008": "commercial-success",
    "bank-of-america--004": "commercial-success",
    "bank-of-america--006": "identity",
    "bank-of-america--012": "commercial-success",
    "pg-chatpg--001": "identity",
    "pg-chatpg--007": "commercial-success",
    "pg-chatpg--008": "survival",
    "databricks--008": "unclassified",
    "walmart--003": "identity",
    "walmart--010": "utopian",
    "walmart--014": "survival",
    "moderna--004": "survival",
    "moderna--005": "unclassified",
    "moderna--006": "unclassified",
    "moderna--009": "unclassified",
    "moderna--010": "unclassified",
    "moderna--011": "unclassified",
    "deloitte--001": "identity",
    "deloitte--002": "identity",
    "deloitte--004": "unclassified",

    # === DIRECTION-UNDER-UNCERTAINTY (58 claims) ===
    "meta-ai--009": "commercial-success",
    "meta-ai--011": "identity",
    "amazon-agi--004": "commercial-success",
    "anthropic--008": "identity",
    "anthropic--010": "identity",
    "anthropic--011": "identity",
    "eli-lilly--005": "identity",
    "eli-lilly--006": "identity",
    "microsoft--002": "commercial-success",
    "microsoft--008": "unclassified",
    "microsoft--010": "commercial-success",
    "microsoft--015": "identity",
    "accenture-openai--002": "survival",
    "accenture-openai--007": "commercial-success",
    "salesforce--007": "unclassified",
    "salesforce--010": "unclassified",
    "klarna--002": "commercial-success",
    "klarna--004": "survival",
    "sk-telecom--005": "survival",
    "google-deepmind--006": "utopian",
    "google-deepmind--010": "identity",
    "ssi--006": "identity",
    "ssi--008": "identity",
    "sierra-ai--006": "commercial-success",
    "pfizer--003": "teleological",
    "novo-nordisk--004": "teleological",
    "novo-nordisk--008": "teleological",
    "novo-nordisk--009": "teleological",
    "novo-nordisk--011": "higher-calling",
    "roche-genentech--009": "identity",
    "roche-genentech--011": "survival",
    "roche-genentech--012": "survival",
    "sanofi--003": "survival",
    "sanofi--008": "survival",
    "sanofi--012": "higher-calling",
    "google-x--007": "identity",
    "google-x--013": "identity",
    "ubs--003": "commercial-success",
    "ubs--007": "commercial-success",
    "ups--006": "identity",
    "ups--012": "identity",
    "commonwealth-bank--004": "identity",
    "commonwealth-bank--007": "commercial-success",
    "commonwealth-bank--009": "commercial-success",
    "wells-fargo--002": "commercial-success",
    "bank-of-america--001": "identity",
    "bank-of-america--013": "commercial-success",
    "pg-chatpg--003": "commercial-success",
    "pg-chatpg--004": "commercial-success",
    "pg-chatpg--006": "commercial-success",
    "databricks--001": "identity",
    "databricks--002": "identity",
    "databricks--005": "identity",
    "databricks--007": "identity",
    "databricks--011": "unclassified",
    "databricks--012": "unclassified",
    "walmart--004": "commercial-success",
    "walmart--009": "survival",

    # === EDGE CASES FROM KEEPER TYPES ===
    # utopian → other
    "wells-fargo--003": "commercial-success",
    "bank-of-america--009": "commercial-success",
    "pg-chatpg--005": "commercial-success",
    "databricks--014": "commercial-success",
    "walmart--015": "commercial-success",
    # teleological → other
    "roche-genentech--008": "higher-calling",
    "ubs--001": "commercial-success",
    "ubs--009": "commercial-success",
    "ups--009": "identity",
    "ups--013": "commercial-success",
    "commonwealth-bank--005": "commercial-success",
    "commonwealth-bank--006": "commercial-success",
    "commonwealth-bank--011": "commercial-success",
    "databricks--003": "identity",
    "databricks--009": "unclassified",
    # identity → other
    "salesforce--001": "commercial-success",
    "salesforce--008": "commercial-success",
    "ubs--002": "commercial-success",
    "ubs--006": "commercial-success",
    "roche-genentech--016": "commercial-success",
}

# Valid v2.0 types
VALID_V2_TYPES = {"utopian", "teleological", "higher-calling", "identity", "survival", "commercial-success", "unclassified"}


def main():
    with open(REGISTRY_PATH) as f:
        data = json.load(f)

    claims = data["claims"]

    # Verify all IDs in reclassification map exist
    claim_ids = {c["id"] for c in claims}
    missing = set(RECLASSIFICATIONS.keys()) - claim_ids
    if missing:
        print(f"ERROR: IDs in reclassification map not found in registry: {missing}")
        return

    # Verify all target types are valid
    invalid_types = {v for v in RECLASSIFICATIONS.values() if v not in VALID_V2_TYPES}
    if invalid_types:
        print(f"ERROR: Invalid target types: {invalid_types}")
        return

    # Count before
    before_counts = Counter(c["claimType"] for c in claims)
    print("=== BEFORE (v1.0) ===")
    for t, count in sorted(before_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")
    print(f"  TOTAL: {sum(before_counts.values())}")
    print()

    # Apply reclassifications
    changed = 0
    for claim in claims:
        cid = claim["id"]
        if cid in RECLASSIFICATIONS:
            old_type = claim["claimType"]
            new_type = RECLASSIFICATIONS[cid]
            claim["claimType"] = new_type
            changed += 1

            # Clear secondaryType if it references an old dissolved type
            old_dissolved = {"transformation-framing", "employee-deal", "sacrifice-justification", "direction-under-uncertainty"}
            if claim.get("secondaryType") and claim["secondaryType"] in old_dissolved:
                claim["secondaryType"] = None

    # Also clean up secondaryType references in notes for non-reclassified claims
    for claim in claims:
        if claim.get("secondaryType") and claim["secondaryType"] in {"transformation-framing", "employee-deal", "sacrifice-justification", "direction-under-uncertainty"}:
            claim["secondaryType"] = None

    # Update metadata
    data["taxonomyVersion"] = "2.0"
    data["lastUpdated"] = "2026-02-08"
    data["claimTypes"] = [
        "utopian",
        "teleological",
        "higher-calling",
        "identity",
        "survival",
        "commercial-success",
        "unclassified"
    ]
    data["claimTypeDefinitions"] = {
        "utopian": "We are part of a civilizational transformation. Scale is beyond the organization. Epochal, new-era language.",
        "teleological": "We exist to achieve a specific moral/social outcome. Concrete enough to be achievable/falsifiable.",
        "higher-calling": "We answer to a duty/purpose that supersedes profit. Moral obligation overrides economic logic.",
        "identity": "We do this because of who we are. Group character, values, culture. The justification terminates in collective identity.",
        "survival": "We must change or be left behind. Existential framing, adapt-or-die. The status quo is not viable.",
        "commercial-success": "This will make the business perform better. Customer experience, growth, efficiency, competitive positioning.",
        "unclassified": "Claims that do not clearly invoke a purpose-end, or that are managerial directives, metrics, or observations rather than purpose claims proper. Retained for review."
    }

    # Count after
    after_counts = Counter(c["claimType"] for c in claims)
    print("=== AFTER (v2.0) ===")
    for t in ["utopian", "teleological", "higher-calling", "identity", "survival", "commercial-success", "unclassified"]:
        print(f"  {t}: {after_counts.get(t, 0)}")
    print(f"  TOTAL: {sum(after_counts.values())}")
    print()
    print(f"Claims reclassified: {changed}")
    print(f"Claims unchanged: {len(claims) - changed}")

    # Verify no old types remain
    old_types = {"transformation-framing", "employee-deal", "sacrifice-justification", "direction-under-uncertainty"}
    remaining_old = {c["claimType"] for c in claims} & old_types
    if remaining_old:
        print(f"\nWARNING: Old types still present: {remaining_old}")
        for t in remaining_old:
            ids = [c["id"] for c in claims if c["claimType"] == t]
            print(f"  {t}: {ids}")
    else:
        print("\nAll old types successfully dissolved.")

    # Write updated registry
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nRegistry written to {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
