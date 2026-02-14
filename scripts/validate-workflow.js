#!/usr/bin/env node

/**
 * validate-workflow.js
 * Checks consistency across the research workflow infrastructure.
 * Run from project root: node scripts/validate-workflow.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SPECIMENS_DIR = path.join(ROOT, 'specimens');
const RESEARCH_DIR = path.join(ROOT, 'research');
const CURATION_DIR = path.join(ROOT, 'curation');
const SYNTHESIS_DIR = path.join(ROOT, 'synthesis');

let errors = 0;
let warnings = 0;

function error(msg) {
  console.log(`  ❌ ${msg}`);
  errors++;
}

function warn(msg) {
  console.log(`  ⚠️  ${msg}`);
  warnings++;
}

function ok(msg) {
  console.log(`  ✅ ${msg}`);
}

function section(title) {
  console.log(`\n── ${title} ──`);
}

function loadJSON(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    error(`Cannot read ${path.relative(ROOT, filePath)}: ${e.message}`);
    return null;
  }
}

// ── 1. Specimen registry vs. actual files ──

section('1. Specimen Registry vs. Files');

const registry = loadJSON(path.join(SPECIMENS_DIR, 'registry.json'));
const SKIP_FILES = new Set(['_template.json', 'specimen-schema.json', 'registry.json', 'source-registry.json']);

if (registry) {
  const registryIds = new Set(registry.specimens.map(s => s.id));
  const fileIds = new Set();

  const files = fs.readdirSync(SPECIMENS_DIR).filter(f => f.endsWith('.json') && !SKIP_FILES.has(f));
  for (const file of files) {
    fileIds.add(file.replace('.json', ''));
  }

  // Check registry count matches (totalFiles includes inactive, totalSpecimens is active only)
  const expectedFileCount = registry.totalFiles || registry.totalSpecimens;
  if (expectedFileCount === files.length) {
    ok(`Registry file count (${expectedFileCount}) matches actual files (${files.length})`);
  } else {
    error(`Registry says ${expectedFileCount} files but found ${files.length} files`);
  }

  const activeCount = registry.totalSpecimens || 0;
  const inactiveCount = registry.inactiveCount || 0;
  if (activeCount + inactiveCount === files.length) {
    ok(`Active (${activeCount}) + Inactive (${inactiveCount}) = ${files.length} files`);
  } else if (inactiveCount > 0) {
    warn(`Active (${activeCount}) + Inactive (${inactiveCount}) = ${activeCount + inactiveCount}, but ${files.length} files exist`);
  }

  // Check every registry ID has a file
  for (const id of registryIds) {
    if (!fileIds.has(id)) {
      error(`Registry has "${id}" but no file specimens/${id}.json`);
    }
  }

  // Check every file has a registry entry
  for (const id of fileIds) {
    if (!registryIds.has(id)) {
      error(`File specimens/${id}.json exists but not in registry`);
    }
  }

  if (registryIds.size === fileIds.size && [...registryIds].every(id => fileIds.has(id))) {
    ok(`All ${registryIds.size} specimen IDs match between registry and files`);
  }

  // ── 2. Specimens with missing source URLs ──

  section('2. Source Provenance Gaps');

  let nullSourceCount = 0;
  let taggedSourceCount = 0;
  for (const file of files) {
    const specimen = loadJSON(path.join(SPECIMENS_DIR, file));
    if (!specimen) continue;
    const sources = specimen.sources || [];
    const nullUrls = sources.filter(s => !s.url);
    const untagged = nullUrls.filter(s => {
      const notes = (s.notes || '');
      return !notes.includes('[paywall]') && !notes.includes('[no URL]');
    });
    if (untagged.length > 0) {
      nullSourceCount++;
    }
    taggedSourceCount += nullUrls.length - untagged.length;
  }

  if (nullSourceCount === 0) {
    ok(`All specimens have source URLs or explicit provenance tags (${taggedSourceCount} tagged)`);
  } else {
    warn(`${nullSourceCount} of ${files.length} specimens have untagged null-URL sources`);
    if (taggedSourceCount > 0) ok(`${taggedSourceCount} null-URL sources properly tagged with [paywall]/[no URL]`);
  }

  // ── 3. byModel counts consistency ──

  section('3. Registry Aggregates');

  // Count only active specimens for aggregate validation
  const activeSpecimens = registry.specimens.filter(s => s.status !== 'Inactive');
  const modelCounts = {};
  const orientationCounts = {};
  for (const s of activeSpecimens) {
    const m = String(s.structuralModel);
    modelCounts[m] = (modelCounts[m] || 0) + 1;
    const o = s.orientation || 'Unknown';
    orientationCounts[o] = (orientationCounts[o] || 0) + 1;
  }

  let modelOk = true;
  for (const [model, count] of Object.entries(registry.byModel)) {
    if ((modelCounts[model] || 0) !== count) {
      error(`byModel["${model}"] says ${count} but counted ${modelCounts[model] || 0}`);
      modelOk = false;
    }
  }
  if (modelOk) ok('byModel counts are consistent');

  let orientOk = true;
  for (const [orient, count] of Object.entries(registry.byOrientation)) {
    if ((orientationCounts[orient] || 0) !== count) {
      error(`byOrientation["${orient}"] says ${count} but counted ${orientationCounts[orient] || 0}`);
      orientOk = false;
    }
  }
  if (orientOk) ok('byOrientation counts are consistent');
}

// ── 4. Queue files ──

section('4. Queue Files');

const queueFiles = [
  { path: path.join(RESEARCH_DIR, 'queue.json'), name: 'research/queue.json', arrayField: 'queue' },
  { path: path.join(CURATION_DIR, 'synthesis-queue.json'), name: 'curation/synthesis-queue.json', arrayField: 'queue' },
];

for (const qf of queueFiles) {
  const data = loadJSON(qf.path);
  if (data) {
    const items = data[qf.arrayField] || [];
    const pending = items.filter(i => i.status === 'pending' || !i.synthesized);
    ok(`${qf.name}: ${items.length} items (${pending.length} pending)`);

    // Check for stale items (pending > 14 days)
    const now = new Date();
    for (const item of items) {
      const dateStr = item.sessionDate || item.lastUpdated;
      if (dateStr) {
        const itemDate = new Date(dateStr);
        const daysOld = (now - itemDate) / (1000 * 60 * 60 * 24);
        if (daysOld > 14 && (item.status === 'pending' || item.synthesized === false)) {
          warn(`Stale item in ${qf.name}: "${item.sessionFile || item.specimenId}" pending for ${Math.floor(daysOld)} days`);
        }
      }
    }
  }
}

// ── 5. Source registry ──

section('5. Source Registry');

const sourceRegistry = loadJSON(path.join(SPECIMENS_DIR, 'source-registry.json'));
if (sourceRegistry) {
  const sources = sourceRegistry.sources || [];
  const tier1 = sources.filter(s => s.tier === 1);
  const tier2 = sources.filter(s => s.tier === 2);
  const scanned = sources.filter(s => s.scannedThrough !== null);
  const unscanned = sources.filter(s => s.scannedThrough === null);

  ok(`${sources.length} sources registered (${tier1.length} Tier 1, ${tier2.length} Tier 2)`);
  if (scanned.length > 0) {
    ok(`${scanned.length} sources have been scanned`);
  }
  if (unscanned.length > 0) {
    warn(`${unscanned.length} sources have never been scanned`);
  }

  // List scanned sources with dates
  for (const s of scanned) {
    ok(`  ${s.name}: scanned through ${s.scannedThrough} (${s.scannedThroughDate})`);
  }
}

// ── 6. Synthesis living documents ──

section('6. Synthesis Documents');

const synthFiles = [
  { path: path.join(SYNTHESIS_DIR, 'mechanisms.json'), name: 'mechanisms.json', countField: 'confirmed' },
  { path: path.join(SYNTHESIS_DIR, 'tensions.json'), name: 'tensions.json', countField: 'tensions' },
  { path: path.join(SYNTHESIS_DIR, 'contingencies.json'), name: 'contingencies.json', countField: 'contingencies' },
];

for (const sf of synthFiles) {
  const data = loadJSON(sf.path);
  if (data) {
    const items = data[sf.countField] || [];
    ok(`${sf.name}: ${items.length} items`);
  }
}

// ── 7. Session coverage quality ──

section('7. Session Coverage');

const sessionsDir = path.join(RESEARCH_DIR, 'sessions');
if (fs.existsSync(sessionsDir)) {
  const sessionFiles = fs.readdirSync(sessionsDir).filter(f => f.endsWith('.md'));
  ok(`${sessionFiles.length} research session(s) on file`);

  for (const file of sessionFiles) {
    const content = fs.readFileSync(path.join(sessionsDir, file), 'utf8');
    const fmMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!fmMatch) {
      warn(`${file}: no YAML frontmatter found`);
      continue;
    }
    const fm = fmMatch[1];

    // Check sources_scanned
    const scannedMatch = fm.match(/sources_scanned:\s*\[([^\]]*)\]/);
    if (scannedMatch) {
      const scanned = scannedMatch[1].split(',').map(s => s.trim().replace(/"/g, '')).filter(Boolean);
      if (scanned.length <= 1) {
        warn(`${file}: single-source session (scanned ${scanned.length} source${scanned.length === 1 ? '' : 's'})`);
      } else {
        ok(`${file}: scanned ${scanned.length} sources`);
      }
    }

    // Check source_types_covered
    const typesMatch = fm.match(/source_types_covered:\s*\[([^\]]*)\]/);
    if (typesMatch) {
      const types = typesMatch[1].split(',').map(s => s.trim().replace(/"/g, '')).filter(Boolean);
      if (types.length <= 1) {
        warn(`${file}: single-type session (only ${types[0] || 'unknown'})`);
      } else {
        ok(`${file}: covered ${types.length} source types (${types.join(', ')})`);
      }
    }

    // Check sources_planned vs sources_scanned
    const plannedMatch = fm.match(/sources_planned:\s*\[([^\]]*)\]/);
    if (plannedMatch && scannedMatch) {
      const planned = plannedMatch[1].split(',').map(s => s.trim().replace(/"/g, '')).filter(Boolean);
      const scanned = scannedMatch[1].split(',').map(s => s.trim().replace(/"/g, '')).filter(Boolean);
      if (scanned.length < planned.length) {
        warn(`${file}: incomplete — scanned ${scanned.length}/${planned.length} planned sources`);
      }
    }
  }
}

// ── 8. Source coverage staleness ──

section('8. Source Coverage Staleness');

if (sourceRegistry) {
  const sources = sourceRegistry.sources || [];
  const now = new Date();
  const tier1Sources = sources.filter(s => s.tier === 1);

  for (const s of tier1Sources) {
    if (s.lastScanned) {
      const lastDate = new Date(s.lastScanned);
      const daysAgo = Math.floor((now - lastDate) / (1000 * 60 * 60 * 24));
      if (daysAgo > 30) {
        warn(`Tier 1 source "${s.name}" last scanned ${daysAgo} days ago`);
      }
    } else {
      warn(`Tier 1 source "${s.name}" has never been scanned`);
    }
  }

  const scannedTier1 = tier1Sources.filter(s => s.lastScanned);
  if (scannedTier1.length === tier1Sources.length) {
    ok(`All ${tier1Sources.length} Tier 1 sources have been scanned`);
  }
}

// ── 9. Directory structure ──

section('9. Directory Structure');

const requiredDirs = [
  'specimens',
  'research/sessions',
  'curation/sessions',
  'synthesis/sessions',
];

for (const dir of requiredDirs) {
  const fullPath = path.join(ROOT, dir);
  if (fs.existsSync(fullPath) && fs.statSync(fullPath).isDirectory()) {
    ok(`${dir}/ exists`);
  } else {
    error(`Missing directory: ${dir}/`);
  }
}

// ── 10. Curation Quality ──

section('10. Curation Quality');

const specimenFiles = fs.readdirSync(SPECIMENS_DIR)
  .filter(f => f.endsWith('.json') && !SKIP_FILES.has(f));

let nullUrlCount = 0;
let noRationaleCount = 0;
let emptyLayersCount = 0;
let truncatedQuotesCount = 0;

for (const file of specimenFiles) {
  const specimen = loadJSON(path.join(SPECIMENS_DIR, file));
  if (!specimen) continue;

  // Check source URLs
  const nullUrls = (specimen.sources || []).filter(s => !s.url && !(s.notes && (s.notes.includes('[paywall]') || s.notes.includes('[no URL]'))));
  if (nullUrls.length > 0) {
    warn(`${file}: ${nullUrls.length} source(s) with null URL and no [paywall]/[no URL] note`);
    nullUrlCount += nullUrls.length;
  }

  // Check classification rationale for Medium/Low confidence
  if (specimen.classification && specimen.classification.confidence !== 'High' && !specimen.classification.classificationRationale) {
    warn(`${file}: ${specimen.classification.confidence} confidence but no classificationRationale`);
    noRationaleCount++;
  }

  // Check empty layers
  if (!specimen.layers || specimen.layers.length === 0) {
    warn(`${file}: no layers (every specimen needs at least one)`);
    emptyLayersCount++;
  }

  // Check truncated quotes (quotes that end abruptly)
  for (const q of (specimen.quotes || [])) {
    if (q.text && q.text.length < 20 && !q.text.endsWith('.') && !q.text.endsWith('!') && !q.text.endsWith('?') && !q.text.endsWith('"')) {
      warn(`${file}: possibly truncated quote "${q.text.substring(0, 30)}..."`);
      truncatedQuotesCount++;
    }
  }
}

if (nullUrlCount === 0) ok('All specimen sources have URLs or explicit [paywall]/[no URL] notes');
else warn(`${nullUrlCount} total sources across specimens missing URLs`);
if (noRationaleCount === 0) ok('All Medium/Low confidence specimens have classification rationale');
else warn(`${noRationaleCount} specimens lack classification rationale despite Medium/Low confidence`);
if (emptyLayersCount === 0) ok('All specimens have at least one layer');
if (truncatedQuotesCount === 0) ok('No truncated quotes detected');

// Check: synthesis queue has entries for recently curated specimens
const synthQueuePath = path.join(CURATION_DIR, 'synthesis-queue.json');
if (fs.existsSync(synthQueuePath)) {
  const synthQueue = loadJSON(synthQueuePath);
  if (synthQueue) {
    const pendingSynth = (synthQueue.queue || []).filter(q => q.status === 'pending');
    ok(`Synthesis queue: ${pendingSynth.length} specimens pending synthesis`);
  }
}

// ── 11. Synthesis Quality ──

section('11. Synthesis Quality');

// Build a set of all specimen IDs for cross-referencing
const allSpecimenIds = new Set(
  fs.readdirSync(SPECIMENS_DIR)
    .filter(f => f.endsWith('.json') && !SKIP_FILES.has(f))
    .map(f => f.replace('.json', ''))
);

// Check: mechanisms.json evidence entries reference real specimens
const mechanismsPath = path.join(SYNTHESIS_DIR, 'mechanisms.json');
const mechanismsData = loadJSON(mechanismsPath);
if (mechanismsData) {
  let orphanedEvidence = 0;
  let duplicateSpecimens = 0;

  for (const mech of [...(mechanismsData.confirmed || []), ...(mechanismsData.candidates || [])]) {
    // Check for duplicate specimen IDs
    const specIds = mech.specimens || [];
    const uniqueIds = new Set(specIds);
    if (uniqueIds.size !== specIds.length) {
      warn(`Mechanism ${mech.id} "${mech.name}": duplicate specimen IDs in specimens array`);
      duplicateSpecimens++;
    }

    // Check evidence references real specimens
    for (const ev of (mech.evidence || [])) {
      if (ev.specimenId && !allSpecimenIds.has(ev.specimenId)) {
        warn(`Mechanism ${mech.id} "${mech.name}": evidence references unknown specimen "${ev.specimenId}"`);
        orphanedEvidence++;
      }
    }

    // Check specimens array references real specimens
    for (const specId of specIds) {
      if (!allSpecimenIds.has(specId)) {
        warn(`Mechanism ${mech.id} "${mech.name}": specimens array references unknown specimen "${specId}"`);
      }
    }
  }

  if (orphanedEvidence === 0 && duplicateSpecimens === 0) {
    ok('All mechanism evidence references valid specimens');
  }
}

// Check: tensions.json specimen references
const tensionsPath = path.join(SYNTHESIS_DIR, 'tensions.json');
const tensionsData = loadJSON(tensionsPath);
if (tensionsData) {
  let emptyTensions = 0;
  for (const t of (tensionsData.tensions || [])) {
    if (!t.specimens || t.specimens.length === 0) {
      warn(`Tension "${t.name}": no specimens linked`);
      emptyTensions++;
    }
  }
  if (emptyTensions === 0) {
    ok('All tensions have specimen links');
  }
}

// Check: contingencies.json specimen references
const contingenciesPath = path.join(SYNTHESIS_DIR, 'contingencies.json');
const contingenciesData = loadJSON(contingenciesPath);
if (contingenciesData) {
  let emptyContingencies = 0;
  for (const c of (contingenciesData.contingencies || [])) {
    const highSpecs = (c.high && c.high.specimens) ? c.high.specimens.length : 0;
    const lowSpecs = (c.low && c.low.specimens) ? c.low.specimens.length : 0;
    if (highSpecs + lowSpecs === 0) {
      warn(`Contingency "${c.name}": no specimens linked on either end`);
      emptyContingencies++;
    }
  }
  if (emptyContingencies === 0) {
    ok('All contingencies have specimen links');
  }
}

// Check: synthesis queue staleness
const synthQueueData = loadJSON(path.join(CURATION_DIR, 'synthesis-queue.json'));
if (synthQueueData) {
  const pendingCount = (synthQueueData.queue || []).filter(q => q.status === 'pending').length;
  const synthesizedCount = (synthQueueData.queue || []).filter(q => q.status === 'synthesized').length;
  ok(`Synthesis progress: ${synthesizedCount} synthesized, ${pendingCount} pending`);
  if (synthQueueData.lastSynthesisDate === null && synthesizedCount === 0) {
    warn('Synthesis has never been run (lastSynthesisDate is null)');
  }
}

// ── 12. Purpose Claims Provenance ──

section('12. Purpose Claims Provenance');

const claimsRegistryPath = path.join(RESEARCH_DIR, 'purpose-claims', 'registry.json');
const claimsRegistry = loadJSON(claimsRegistryPath);
if (claimsRegistry) {
  const claims = claimsRegistry.claims || [];
  ok(`Purpose claims registry: ${claims.length} claims`);

  let nullSourceUrl = 0;
  let nullSourceDate = 0;
  let orphanedClaims = 0;
  const claimIds = new Set();
  let duplicateIds = 0;

  for (const claim of claims) {
    // Check for duplicate claim IDs
    if (claim.id) {
      if (claimIds.has(claim.id)) {
        duplicateIds++;
      }
      claimIds.add(claim.id);
    }

    // Check sourceUrl
    if (!claim.sourceUrl) {
      nullSourceUrl++;
    }

    // Check sourceDate
    if (!claim.sourceDate) {
      nullSourceDate++;
    }

    // Check specimenId references real specimen
    if (claim.specimenId && !allSpecimenIds.has(claim.specimenId)) {
      orphanedClaims++;
    }
  }

  if (duplicateIds > 0) error(`${duplicateIds} duplicate claim IDs in purpose claims registry`);
  else ok('No duplicate claim IDs');

  if (orphanedClaims > 0) error(`${orphanedClaims} claims reference specimens not in specimens/`);
  else ok('All claims reference valid specimen IDs');

  if (nullSourceUrl > 0) warn(`${nullSourceUrl} claims with null sourceUrl`);
  else ok('All claims have sourceUrl');

  if (nullSourceDate > 0) warn(`${nullSourceDate} claims with null sourceDate`);
  else ok('All claims have sourceDate');
}

// ── 13. Tension/Contingency Specimen Coverage ──

section('13. Tension/Contingency Specimen Coverage');

// Build set of active specimen IDs (exclude Inactive)
const activeSpecimenIds = new Set();
if (registry) {
  for (const s of registry.specimens) {
    if (s.status !== 'Inactive') {
      activeSpecimenIds.add(s.id);
    }
  }
}

// Check which active specimens appear in tensions
if (tensionsData && activeSpecimenIds.size > 0) {
  const specimensInTensions = new Set();
  for (const t of (tensionsData.tensions || [])) {
    for (const s of (t.specimens || [])) {
      if (s.specimenId) specimensInTensions.add(s.specimenId);
    }
  }

  const notInTensions = [...activeSpecimenIds].filter(id => !specimensInTensions.has(id));
  if (notInTensions.length === 0) {
    ok(`All ${activeSpecimenIds.size} active specimens placed in tensions`);
  } else {
    warn(`${notInTensions.length} active specimens not placed in any tension`);
  }
}

// Check which active specimens appear in contingencies
if (contingenciesData && activeSpecimenIds.size > 0) {
  const specimensInContingencies = new Set();
  for (const c of (contingenciesData.contingencies || [])) {
    // Check all keys that might have specimens arrays (high, medium, low, nonTraditional, etc.)
    for (const [key, value] of Object.entries(c)) {
      if (value && typeof value === 'object' && !Array.isArray(value) && value.specimens) {
        for (const specId of value.specimens) {
          specimensInContingencies.add(specId);
        }
      }
    }
  }

  const notInContingencies = [...activeSpecimenIds].filter(id => !specimensInContingencies.has(id));
  if (notInContingencies.length === 0) {
    ok(`All ${activeSpecimenIds.size} active specimens placed in contingencies`);
  } else {
    warn(`${notInContingencies.length} active specimens not placed in any contingency`);
  }
}

// ── 14. Insight Evidence Audit ──

section('14. Insight Evidence Audit');

const insightsPath = path.join(SYNTHESIS_DIR, 'insights.json');
const insightsData = loadJSON(insightsPath);
if (insightsData) {
  const insights = insightsData.insights || [];
  ok(`Insights: ${insights.length} total`);

  let thinEvidence = 0;
  let orphanedInsightEvidence = 0;
  let nullDiscoveredIn = 0;

  for (const insight of insights) {
    const evidence = insight.evidence || [];

    // Thin evidence check
    if (evidence.length < 2) {
      warn(`Insight "${insight.id}": only ${evidence.length} evidence entries (thin)`);
      thinEvidence++;
    }

    // Evidence specimen references
    for (const ev of evidence) {
      if (ev.specimenId && !allSpecimenIds.has(ev.specimenId)) {
        warn(`Insight "${insight.id}": evidence references unknown specimen "${ev.specimenId}"`);
        orphanedInsightEvidence++;
      }
    }

    // discoveredIn check
    if (!insight.discoveredIn) {
      warn(`Insight "${insight.id}": null discoveredIn`);
      nullDiscoveredIn++;
    }
  }

  if (thinEvidence === 0) ok('All insights have ≥2 evidence entries');
  if (orphanedInsightEvidence === 0) ok('All insight evidence references valid specimens');
  if (nullDiscoveredIn === 0) ok('All insights have discoveredIn populated');
}

// ── 15. Enrichment Completeness ──

section('15. Enrichment Completeness');

const scanTrackerPath = path.join(RESEARCH_DIR, 'purpose-claims', 'scan-tracker.json');
const scanTracker = loadJSON(scanTrackerPath);
const enrichmentDir = path.join(RESEARCH_DIR, 'purpose-claims', 'enrichment');

if (scanTracker && fs.existsSync(enrichmentDir)) {
  const scannedSpecimens = (scanTracker.specimens || []).map(s => s.specimenId);
  const enrichmentFiles = fs.readdirSync(enrichmentDir)
    .filter(f => f.endsWith('.json'))
    .map(f => f.replace('.json', ''));

  // Scanned but no enrichment file
  const scannedNoEnrichment = scannedSpecimens.filter(id => !enrichmentFiles.includes(id));
  // Enrichment file but not in registry
  const enrichmentNoRegistry = enrichmentFiles.filter(id => !allSpecimenIds.has(id));

  ok(`${scannedSpecimens.length} specimens scanned, ${enrichmentFiles.length} enrichment files`);

  if (scannedNoEnrichment.length > 0) {
    warn(`${scannedNoEnrichment.length} scanned specimens without enrichment files`);
  } else {
    ok('All scanned specimens have enrichment files');
  }

  if (enrichmentNoRegistry.length > 0) {
    warn(`${enrichmentNoRegistry.length} enrichment files for specimens not in registry: ${enrichmentNoRegistry.join(', ')}`);
  } else {
    ok('All enrichment files correspond to registered specimens');
  }
}

// ── 16. Registry Freshness ──

section('16. Registry Freshness');

if (registry) {
  // Compare totalFiles vs actual file count
  const actualFiles = fs.readdirSync(SPECIMENS_DIR)
    .filter(f => f.endsWith('.json') && !SKIP_FILES.has(f));

  const regTotalFiles = registry.totalFiles || registry.totalSpecimens;
  if (regTotalFiles !== actualFiles.length) {
    error(`Registry totalFiles (${regTotalFiles}) doesn't match actual file count (${actualFiles.length}). Run: node scripts/rebuild-registry.js`);
  } else {
    ok(`Registry totalFiles (${regTotalFiles}) matches actual files`);
  }

  // Compare byModel counts vs actual
  const actualModelCounts = {};
  for (const file of actualFiles) {
    const spec = loadJSON(path.join(SPECIMENS_DIR, file));
    if (!spec || (spec.meta && spec.meta.status === 'Inactive')) continue;
    const model = String(spec.classification && spec.classification.structuralModel ? spec.classification.structuralModel : 'null');
    actualModelCounts[model] = (actualModelCounts[model] || 0) + 1;
  }

  let modelFreshness = true;
  for (const [model, count] of Object.entries(registry.byModel || {})) {
    if ((actualModelCounts[model] || 0) !== count) {
      warn(`Registry byModel["${model}"] = ${count}, but actual count = ${actualModelCounts[model] || 0}. Run: node scripts/rebuild-registry.js`);
      modelFreshness = false;
    }
  }
  // Check reverse: actual models not in registry
  for (const [model, count] of Object.entries(actualModelCounts)) {
    if (!registry.byModel || !(model in registry.byModel)) {
      warn(`Model "${model}" has ${count} specimens but not in registry.byModel. Run: node scripts/rebuild-registry.js`);
      modelFreshness = false;
    }
  }
  if (modelFreshness) ok('Registry byModel counts match actual specimen files');
}

// ── 17. Specimen ID/Filename Mismatch ──

section('17. Specimen ID/Filename Consistency');

if (registry) {
  const specimenFiles = fs.readdirSync(SPECIMENS_DIR).filter(f => f.endsWith('.json') && !SKIP_FILES.has(f));
  let mismatches = 0;
  for (const file of specimenFiles) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(SPECIMENS_DIR, file), 'utf8'));
      const expectedId = file.replace('.json', '');
      if (data.id && data.id !== expectedId) {
        error(`ID mismatch: file "${file}" has id="${data.id}" (expected "${expectedId}")`);
        mismatches++;
      }
    } catch (e) {
      // Already caught in section 1
    }
  }
  if (mismatches === 0) ok(`All specimen file IDs match their filenames`);
}

// ── 18. Specimen Schema Validation ──

section('18. Specimen Schema Validation');

if (registry) {
  const VALID_MODELS = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  const VALID_ORIENTATIONS = ['Structural', 'Contextual', 'Temporal'];
  const VALID_STATUSES = ['Active', 'Stub', 'Inactive', 'Deprecated'];
  let schemaIssues = 0;

  const specimenFiles = fs.readdirSync(SPECIMENS_DIR).filter(f => f.endsWith('.json') && !SKIP_FILES.has(f));
  for (const file of specimenFiles) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(SPECIMENS_DIR, file), 'utf8'));
      const id = file.replace('.json', '');

      // Check structuralModel
      const model = data.classification?.structuralModel;
      if (model != null && !VALID_MODELS.includes(model)) {
        warn(`${id}: structuralModel=${model} is not a valid integer 1-9`);
        schemaIssues++;
      }

      // Check orientation
      const orientation = data.classification?.orientation;
      if (orientation != null && !VALID_ORIENTATIONS.includes(orientation)) {
        warn(`${id}: orientation="${orientation}" is not valid (expected Structural/Contextual/Temporal)`);
        schemaIssues++;
      }

      // Check status
      const status = data.meta?.status;
      if (status != null && !VALID_STATUSES.includes(status)) {
        warn(`${id}: status="${status}" is not valid (expected Active/Stub/Inactive/Deprecated)`);
        schemaIssues++;
      }

      // Check for duplicate source IDs within specimen
      const sourceIds = (data.sources || []).map(s => s.id).filter(Boolean);
      const dupes = sourceIds.filter((id, i) => sourceIds.indexOf(id) !== i);
      if (dupes.length > 0) {
        warn(`${id}: duplicate source IDs: ${[...new Set(dupes)].join(', ')}`);
        schemaIssues++;
      }
    } catch (e) {
      // Parse errors already caught in section 1
    }
  }
  if (schemaIssues === 0) ok(`All specimens pass schema validation`);
  else ok(`${specimenFiles.length - schemaIssues} specimens clean, ${schemaIssues} with issues`);
}

// ── Summary ──

console.log('\n══════════════════════════════');
if (errors === 0 && warnings === 0) {
  console.log('✅ All checks passed!');
} else {
  console.log(`${errors} error(s), ${warnings} warning(s)`);
}
console.log('══════════════════════════════\n');

process.exit(errors > 0 ? 1 : 0);
