#!/usr/bin/env python3
"""
Merge enrich-*.json specimens into their originals, then delete the enrich files.
One-off script for the 2026-02-14 overnight enrichment batch.

Strategy per specimen:
- Add a new stratigraphy layer recording the enrichment
- Merge new quotes (dedup by text[:80])
- Merge new sources (dedup by URL)
- Merge new mechanisms (dedup by id)
- Update observable markers (fill nulls, replace with richer data)
- Apply classification changes where approved
- Update habitat fields where original was null
- Update contingencies and tension positions where original was null
- Bump confidence where enrichment has higher
- Update meta.lastUpdated
"""

import json, os, sys, shutil
from pathlib import Path
from datetime import date

SPECIMENS = Path("/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation/specimens")

TODAY = date.today().isoformat()
TODAY_MONTH = TODAY[:7]

# Classification decisions from botanist review:
# key = specimen id, value = dict of overrides (or None to accept enrichment as-is)
CLASSIFICATION_DECISIONS = {
    "atlassian": None,          # M4→M4, just confidence up + data
    "bytedance": None,          # M5c→M1, accept (Seed team evidence)
    "coca-cola": None,          # M4→M6b, accept (only 2/2000 have AI titles)
    "deloitte": None,           # M2→M4, accept (actual AI structure found)
    "duolingo": None,           # M3→M6c, accept (frAI-days, grassroots)
    "infosys": None,            # M2→M4, accept (Topaz platform, dual leadership)
    "novo-nordisk": None,       # M4→M4, just confidence up + data
    "nvidia": {                 # M1→M1, REJECT orientation flip
        "orientation": "Structural",
        "orientationName": "Structural",
    },
    "shopify": None,            # M3→M6a, accept
    "siemens": None,            # M4→M4, just confidence up + data
    "walmart": None,            # M5c→M4, accept
}


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def merge_specimen(specimen_id):
    orig_path = SPECIMENS / f"{specimen_id}.json"
    enrich_path = SPECIMENS / f"enrich-{specimen_id}.json"

    if not orig_path.exists():
        print(f"  ERROR: Original {orig_path.name} not found!")
        return False
    if not enrich_path.exists():
        print(f"  ERROR: Enrichment {enrich_path.name} not found!")
        return False

    orig = load_json(orig_path)
    enrich = load_json(enrich_path)

    old_model = orig["classification"]["structuralModel"]
    old_model_name = orig["classification"].get("structuralModelName", "")
    old_orientation = orig["classification"].get("orientation", "")
    old_confidence = orig["classification"].get("confidence", "")

    new_model = enrich["classification"]["structuralModel"]
    new_model_name = enrich["classification"].get("structuralModelName", "")
    new_orientation = enrich["classification"].get("orientation", "")
    new_confidence = enrich["classification"].get("confidence", "")

    classification_changed = (old_model != new_model or old_orientation != new_orientation)

    # --- 1. Classification ---
    # Start with enrichment classification
    for key in enrich["classification"]:
        orig["classification"][key] = enrich["classification"][key]

    # Apply any botanist overrides
    overrides = CLASSIFICATION_DECISIONS.get(specimen_id)
    if overrides:
        for key, val in overrides.items():
            orig["classification"][key] = val

    # --- 2. Habitat (fill nulls, update with enrichment) ---
    if "habitat" in enrich:
        for key, val in enrich["habitat"].items():
            if val is not None:
                orig_val = orig.get("habitat", {}).get(key)
                if orig_val is None or orig_val == "" or key in ("revenue", "employees"):
                    orig.setdefault("habitat", {})[key] = val

    # --- 3. Description (replace with richer enrichment) ---
    if enrich.get("description") and len(enrich["description"]) > len(orig.get("description", "")):
        orig["description"] = enrich["description"]

    # --- 4. Title (use enrichment if more descriptive) ---
    if enrich.get("title"):
        orig["title"] = enrich["title"]

    # --- 5. Observable markers (replace with enrichment where richer) ---
    if "observableMarkers" in enrich:
        for key, val in enrich["observableMarkers"].items():
            if val is not None:
                orig.setdefault("observableMarkers", {})[key] = val

    # --- 6. Quotes (merge, dedup by text[:80]) ---
    existing_quotes = {q.get("text", "")[:80] for q in orig.get("quotes", [])}
    for q in enrich.get("quotes", []):
        if q.get("text", "")[:80] not in existing_quotes:
            orig.setdefault("quotes", []).append(q)
            existing_quotes.add(q["text"][:80])

    # --- 7. Sources (merge, dedup by URL) ---
    existing_urls = {s.get("url", "") for s in orig.get("sources", []) if s.get("url")}
    existing_ids = {s.get("id", "") for s in orig.get("sources", [])}
    for s in enrich.get("sources", []):
        url = s.get("url", "")
        sid = s.get("id", "")
        if url and url not in existing_urls and sid not in existing_ids:
            orig.setdefault("sources", []).append(s)
            existing_urls.add(url)
            existing_ids.add(sid)

    # --- 8. Mechanisms (merge, dedup by id) ---
    existing_mech_ids = {m.get("id") for m in orig.get("mechanisms", [])}
    for m in enrich.get("mechanisms", []):
        if m.get("id") not in existing_mech_ids:
            orig.setdefault("mechanisms", []).append(m)
            existing_mech_ids.add(m["id"])
        else:
            # Update existing mechanism with richer evidence if enrichment has more
            for existing_m in orig["mechanisms"]:
                if existing_m["id"] == m["id"]:
                    if len(m.get("evidence", "")) > len(existing_m.get("evidence", "")):
                        existing_m["evidence"] = m["evidence"]
                    # Upgrade strength if enrichment is stronger
                    strength_order = {"Emerging": 0, "Moderate": 1, "Strong": 2}
                    if strength_order.get(m.get("strength"), 0) > strength_order.get(existing_m.get("strength"), 0):
                        existing_m["strength"] = m["strength"]

    # --- 9. Contingencies (fill from enrichment) ---
    if "contingencies" in enrich and enrich["contingencies"]:
        for key, val in enrich["contingencies"].items():
            if val is not None:
                orig.setdefault("contingencies", {})[key] = val

    # --- 10. Tension positions (fill from enrichment) ---
    if "tensionPositions" in enrich and enrich["tensionPositions"]:
        for key, val in enrich["tensionPositions"].items():
            if val is not None:
                orig_val = orig.get("tensionPositions", {}).get(key)
                if orig_val is None or orig_val == 0.0:
                    orig.setdefault("tensionPositions", {})[key] = val

    # --- 11. Open questions (merge) ---
    existing_qs = set(orig.get("openQuestions", []))
    for q in enrich.get("openQuestions", []):
        if q not in existing_qs:
            orig.setdefault("openQuestions", []).append(q)

    # --- 12. Taxonomy feedback (merge) ---
    existing_fb = set(orig.get("taxonomyFeedback", []))
    for fb in enrich.get("taxonomyFeedback", []):
        if fb not in existing_fb:
            orig.setdefault("taxonomyFeedback", []).append(fb)

    # --- 13. New stratigraphy layer ---
    layer = {
        "date": TODAY_MONTH,
        "label": "Enrichment merge",
        "summary": f"Merged enrichment data from overnight research run (2026-02-14).",
    }
    if classification_changed:
        layer["label"] = f"Enrichment: M{old_model}→M{new_model}"
        layer["classification"] = {
            "previousModel": old_model,
            "previousModelName": old_model_name,
            "previousOrientation": old_orientation,
            "newModel": new_model,
            "newModelName": new_model_name,
            "newOrientation": new_orientation,
        }
        layer["summary"] = (
            f"Reclassified from M{old_model} ({old_model_name}) {old_orientation} "
            f"to M{new_model} ({new_model_name}) {new_orientation} based on enrichment data. "
            f"Confidence: {old_confidence}→{new_confidence}."
        )

    enrich_source_ids = [s.get("id", "") for s in enrich.get("sources", [])[:3]]
    layer["sourceRefs"] = enrich_source_ids

    orig.setdefault("layers", []).insert(0, layer)

    # --- 14. Meta ---
    orig.setdefault("meta", {})["lastUpdated"] = TODAY
    # Bump completeness if enrichment has richer data
    if len(orig.get("quotes", [])) >= 3 and len(orig.get("sources", [])) >= 3:
        orig["meta"]["completeness"] = "High"
    elif len(orig.get("quotes", [])) >= 1:
        orig["meta"]["completeness"] = "Medium"

    # --- Save ---
    save_json(orig_path, orig)
    print(f"  ✓ Merged into {orig_path.name}")

    # Log summary
    n_new_quotes = len(enrich.get("quotes", []))
    n_new_sources = len(enrich.get("sources", []))
    class_note = f"M{old_model}→M{new_model}" if classification_changed else "no change"
    print(f"    Classification: {class_note} | +{n_new_quotes} quotes, +{n_new_sources} sources")

    return True


def main():
    print("=" * 60)
    print("Enrichment Merge Script — 2026-02-14 overnight batch")
    print("=" * 60)

    enrich_files = sorted(SPECIMENS.glob("enrich-*.json"))
    print(f"\nFound {len(enrich_files)} enrichment files to merge.\n")

    success = 0
    failed = 0
    for ef in enrich_files:
        specimen_id = ef.stem.replace("enrich-", "")
        print(f"\n[{specimen_id}]")
        if merge_specimen(specimen_id):
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Merged: {success} | Failed: {failed}")

    if failed == 0:
        print(f"\nDeleting {len(enrich_files)} enrichment files...")
        for ef in enrich_files:
            ef.unlink()
            print(f"  ✗ Deleted {ef.name}")
        print("\nDone. Run `node scripts/rebuild-registry.js` to update the registry.")
    else:
        print("\nSome merges failed — enrichment files NOT deleted. Fix errors and re-run.")


if __name__ == "__main__":
    main()
