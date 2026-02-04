#!/usr/bin/env node

/**
 * Compute mechanism-taxonomy affinity profiles.
 *
 * For each confirmed mechanism in synthesis/mechanisms.json, reads its linked
 * specimen files to determine which structural models and orientations the
 * mechanism is most associated with. Writes affinityProfile back into mechanisms.json.
 *
 * Usage: node scripts/compute-mechanism-affinity.js
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SPECIMENS_DIR = path.join(ROOT, "specimens");
const MECHANISMS_FILE = path.join(ROOT, "synthesis", "mechanisms.json");

const MODEL_NAMES = {
  1: "Research Lab",
  2: "Center of Excellence",
  3: "Embedded Teams",
  4: "Hub-and-Spoke",
  5: "Product/Venture Lab",
  6: "Unnamed/Informal",
  7: "Tiger Teams",
  8: "Skunkworks",
  9: "AI-Native",
};

function loadSpecimen(id) {
  const filePath = path.join(SPECIMENS_DIR, `${id}.json`);
  if (!fs.existsSync(filePath)) {
    console.warn(`  WARNING: Specimen file not found: ${id}.json`);
    return null;
  }
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function computeAffinity(mechanism, allSpecimens) {
  const specimenData = mechanism.specimens
    .map((id) => {
      const cached = allSpecimens[id];
      if (cached) return cached;
      const loaded = loadSpecimen(id);
      if (loaded) allSpecimens[id] = loaded;
      return loaded;
    })
    .filter(Boolean);

  const modelCounts = {};
  const orientationCounts = { Structural: 0, Contextual: 0, Temporal: 0 };
  const total = specimenData.length;

  for (const s of specimenData) {
    const model = s.classification?.structuralModel;
    if (model) {
      if (!modelCounts[model]) {
        modelCounts[model] = { count: 0, specimens: [] };
      }
      modelCounts[model].count++;
      modelCounts[model].specimens.push(s.id);
    }

    const orientation = s.classification?.orientation;
    if (orientation && orientationCounts.hasOwnProperty(orientation)) {
      orientationCounts[orientation]++;
    }
  }

  // Add percentages
  const modelDistribution = {};
  for (const [model, data] of Object.entries(modelCounts)) {
    modelDistribution[model] = {
      count: data.count,
      percentage: total > 0 ? Math.round((data.count / total) * 1000) / 10 : 0,
      specimens: data.specimens,
    };
  }

  const orientationDistribution = {};
  for (const [orient, count] of Object.entries(orientationCounts)) {
    orientationDistribution[orient] = {
      count,
      percentage: total > 0 ? Math.round((count / total) * 1000) / 10 : 0,
    };
  }

  // Find primary model and orientation
  const primaryModel = Object.entries(modelDistribution).sort(
    (a, b) => b[1].count - a[1].count
  )[0];
  const primaryOrientation = Object.entries(orientationDistribution).sort(
    (a, b) => b[1].count - a[1].count
  )[0];

  // Generate summary
  const topModels = Object.entries(modelDistribution)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 3)
    .map(([m, d]) => `M${m} ${MODEL_NAMES[m]} (${d.count})`);

  const summary = `${primaryOrientation[1].percentage >= 60 ? "Strongly" : "Moderately"} associated with ${primaryOrientation[0]} orientation (${primaryOrientation[1].percentage}%). Most common in: ${topModels.join(", ")}.`;

  return {
    modelDistribution,
    orientationDistribution,
    primaryModel: Number(primaryModel[0]),
    primaryOrientation: primaryOrientation[0],
    specimenCount: total,
    affinitySummary: summary,
  };
}

function main() {
  console.log("Computing mechanism-taxonomy affinity profiles...\n");

  const mechanisms = JSON.parse(fs.readFileSync(MECHANISMS_FILE, "utf-8"));
  const allSpecimens = {}; // cache

  let updated = 0;
  for (const mechanism of mechanisms.confirmed) {
    console.log(`#${mechanism.id} ${mechanism.name} (${mechanism.specimens.length} specimens)`);
    const affinity = computeAffinity(mechanism, allSpecimens);
    mechanism.affinityProfile = affinity;
    console.log(`  Primary: M${affinity.primaryModel} (${MODEL_NAMES[affinity.primaryModel]}), ${affinity.primaryOrientation}`);
    console.log(`  ${affinity.affinitySummary}\n`);
    updated++;
  }

  fs.writeFileSync(MECHANISMS_FILE, JSON.stringify(mechanisms, null, 2) + "\n");
  console.log(`Done. Updated ${updated} mechanism affinity profiles in mechanisms.json`);
}

main();
