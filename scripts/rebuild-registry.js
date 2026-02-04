const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "..", "specimens");
const files = fs.readdirSync(dir).filter(function(f) {
  return f.endsWith(".json") && f[0] !== "_" && f !== "registry.json" && f !== "specimen-schema.json" && f !== "source-registry.json";
});

const specimens = [];
const byModel = {};
const byOrientation = {};
const typeSpecimens = [];

for (const file of files) {
  try {
    const data = JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8"));
    const entry = {
      id: data.id,
      name: data.name,
      structuralModel: data.classification && data.classification.structuralModel,
      subType: (data.classification && data.classification.subType) || null,
      secondaryModel: (data.classification && data.classification.secondaryModel) || null,
      orientation: data.classification && data.classification.orientation,
      typeSpecimen: (data.classification && data.classification.typeSpecimen) || false,
      status: (data.meta && data.meta.status) || "Active",
      created: data.meta && data.meta.created,
      lastUpdated: data.meta && data.meta.lastUpdated,
      layerCount: (data.layers && data.layers.length) || 0,
      completeness: (data.meta && data.meta.completeness) || "Low",
      confidence: (data.classification && data.classification.confidence) || "Low"
    };
    specimens.push(entry);

    const m = String(data.classification && data.classification.structuralModel);
    byModel[m] = (byModel[m] || 0) + 1;

    const o = data.classification && data.classification.orientation;
    byOrientation[o] = (byOrientation[o] || 0) + 1;

    if (data.classification && data.classification.typeSpecimen) typeSpecimens.push(data.id);
  } catch(e) {
    console.error("Error reading " + file + ": " + e.message);
  }
}

specimens.sort(function(a, b) { return a.id.localeCompare(b.id); });

const registry = {
  description: "Specimen Registry \u2014 tracks all specimens in the herbarium. Updated whenever specimens are created or modified.",
  lastUpdated: "2026-02-04",
  totalSpecimens: specimens.length,
  byModel: byModel,
  byOrientation: byOrientation,
  typeSpecimens: typeSpecimens,
  specimens: specimens
};

fs.writeFileSync(path.join(dir, "registry.json"), JSON.stringify(registry, null, 2));
console.log("Registry updated. Total: " + specimens.length);
console.log("By model:", JSON.stringify(byModel));
console.log("By orientation:", JSON.stringify(byOrientation));
console.log("Type specimens:", typeSpecimens);
