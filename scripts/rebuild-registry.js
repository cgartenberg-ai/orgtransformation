/**
 * rebuild-registry.js
 * ===================
 * Scan all specimen JSON files and rebuild specimens/registry.json from scratch.
 * Respects Inactive status: totalSpecimens and aggregate counts exclude Inactive.
 *
 * Usage:
 *   node scripts/rebuild-registry.js           # Rebuild and overwrite
 *   node scripts/rebuild-registry.js --dry-run  # Show changes without writing
 *
 * Run from project root: orgtransformation/
 */

const fs = require("fs");
const path = require("path");

const dryRun = process.argv.includes("--dry-run");
const dir = path.join(__dirname, "..", "specimens");
const registryPath = path.join(dir, "registry.json");

// ─── Scan Specimen Files ─────────────────────────────────────────────────

const files = fs.readdirSync(dir).filter((f) =>
  f.endsWith(".json") &&
  f[0] !== "_" &&
  f !== "registry.json" &&
  f !== "specimen-schema.json" &&
  f !== "source-registry.json"
);

const specimens = [];
const parseErrors = [];

for (const file of files) {
  try {
    const data = JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8"));
    const cls = data.classification || {};
    const meta = data.meta || {};

    specimens.push({
      id: data.id,
      name: data.name,
      structuralModel: cls.structuralModel || null,
      subType: cls.subType || null,
      secondaryModel: cls.secondaryModel || null,
      orientation: cls.orientation || null,
      typeSpecimen: cls.typeSpecimen || false,
      status: meta.status || "Active",
      created: meta.created || null,
      lastUpdated: meta.lastUpdated || null,
      layerCount: (data.layers && data.layers.length) || 0,
      completeness: meta.completeness || "Low",
      confidence: cls.confidence || "Low",
    });
  } catch (e) {
    parseErrors.push({ file, error: e.message });
    console.error(`❌ Error reading ${file}: ${e.message}`);
  }
}

specimens.sort((a, b) => a.id.localeCompare(b.id));

// ─── Compute Aggregates (Active Only) ────────────────────────────────────

const active = specimens.filter((s) => s.status !== "Inactive");
const inactive = specimens.filter((s) => s.status === "Inactive");

const byModel = {};
const byOrientation = {};
const typeSpecimens = [];

for (const s of active) {
  const m = String(s.structuralModel);
  if (m && m !== "null") byModel[m] = (byModel[m] || 0) + 1;

  const o = s.orientation;
  if (o) byOrientation[o] = (byOrientation[o] || 0) + 1;

  if (s.typeSpecimen) typeSpecimens.push(s.id);
}

// ─── Load Previous Registry for Comparison ───────────────────────────────

let prevRegistry = null;
try {
  prevRegistry = JSON.parse(fs.readFileSync(registryPath, "utf-8"));
} catch {
  // No previous registry — that's fine
}

const today = new Date().toISOString().split("T")[0];

const registry = {
  description:
    "Specimen Registry \u2014 tracks all specimens in the herbarium. Auto-rebuilt by rebuild-registry.js.",
  lastUpdated: today,
  totalSpecimens: active.length,
  totalFiles: specimens.length,
  inactiveCount: inactive.length,
  byModel,
  byOrientation,
  typeSpecimens,
  specimens,
};

// ─── Report Changes ──────────────────────────────────────────────────────

console.log("\n=== Registry Rebuild ===");
console.log(`Files scanned: ${files.length}`);
console.log(`Parse errors: ${parseErrors.length}`);
console.log(`Total specimens: ${specimens.length} (${active.length} active, ${inactive.length} inactive)`);
console.log(`By model: ${JSON.stringify(byModel)}`);
console.log(`By orientation: ${JSON.stringify(byOrientation)}`);
console.log(`Type specimens: ${typeSpecimens.join(", ") || "(none)"}`);

if (prevRegistry) {
  const prevTotal = prevRegistry.totalSpecimens || 0;
  const prevFiles = prevRegistry.specimens ? prevRegistry.specimens.length : 0;

  if (prevTotal !== active.length) {
    console.log(`\n  Active count change: ${prevTotal} → ${active.length}`);
  }
  if (prevFiles !== specimens.length) {
    console.log(`  File count change: ${prevFiles} → ${specimens.length}`);
  }

  // Find new/removed specimens
  const prevIds = new Set((prevRegistry.specimens || []).map((s) => s.id));
  const currIds = new Set(specimens.map((s) => s.id));
  const added = [...currIds].filter((id) => !prevIds.has(id));
  const removed = [...prevIds].filter((id) => !currIds.has(id));

  if (added.length) console.log(`  Added: ${added.join(", ")}`);
  if (removed.length) console.log(`  Removed (orphan entries): ${removed.join(", ")}`);
}

if (inactive.length > 0) {
  console.log(`\nInactive specimens: ${inactive.map((s) => s.id).join(", ")}`);
}

// ─── Write ───────────────────────────────────────────────────────────────

if (dryRun) {
  console.log("\n[DRY RUN] No changes written.");
} else {
  fs.writeFileSync(registryPath, JSON.stringify(registry, null, 2) + "\n");
  console.log(`\n✅ Registry written: ${registryPath}`);
}
