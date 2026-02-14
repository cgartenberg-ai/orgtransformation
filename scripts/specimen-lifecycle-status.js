#!/usr/bin/env node

/**
 * specimen-lifecycle-status.js
 * Cross-references all pipeline files to produce a specimen lifecycle dashboard.
 *
 * Reads from: registry.json, tensions.json, contingencies.json,
 *             scan-tracker.json, enrichment/*.json, synthesis-queue.json
 * Outputs: data/specimen-lifecycle-status.md  (human-readable)
 *          data/specimen-lifecycle-status.json (machine-readable)
 *
 * Run from project root: node scripts/specimen-lifecycle-status.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SPECIMENS_DIR = path.join(ROOT, 'specimens');
const SYNTHESIS_DIR = path.join(ROOT, 'synthesis');
const RESEARCH_DIR = path.join(ROOT, 'research');
const CURATION_DIR = path.join(ROOT, 'curation');
const DATA_DIR = path.join(ROOT, 'data');

// Ensure data directory exists before writing
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

const SKIP_FILES = new Set(['_template.json', 'specimen-schema.json', 'registry.json', 'source-registry.json']);

function loadJSON(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    console.error(`Cannot read ${path.relative(ROOT, filePath)}: ${e.message}`);
    return null;
  }
}

// ── Load all data sources ──

const registry = loadJSON(path.join(SPECIMENS_DIR, 'registry.json'));
if (!registry) {
  console.error('Cannot load registry.json — aborting');
  process.exit(1);
}

const tensionsData = loadJSON(path.join(SYNTHESIS_DIR, 'tensions.json'));
const contingenciesData = loadJSON(path.join(SYNTHESIS_DIR, 'contingencies.json'));
const insightsData = loadJSON(path.join(SYNTHESIS_DIR, 'insights.json'));
const scanTracker = loadJSON(path.join(RESEARCH_DIR, 'purpose-claims', 'scan-tracker.json'));
const claimsRegistry = loadJSON(path.join(RESEARCH_DIR, 'purpose-claims', 'registry.json'));
const synthQueue = loadJSON(path.join(CURATION_DIR, 'synthesis-queue.json'));

// ── Build lookup indexes ──

// Tension placements: specimenId → count of tensions it appears in
const tensionPlacements = {};
const TOTAL_TENSIONS = (tensionsData && tensionsData.tensions) ? tensionsData.tensions.length : 0;
if (tensionsData) {
  for (const t of (tensionsData.tensions || [])) {
    for (const s of (t.specimens || [])) {
      if (s.specimenId) {
        tensionPlacements[s.specimenId] = (tensionPlacements[s.specimenId] || 0) + 1;
      }
    }
  }
}

// Contingency placements: specimenId → count of contingencies it appears in
const contingencyPlacements = {};
const TOTAL_CONTINGENCIES = (contingenciesData && contingenciesData.contingencies) ? contingenciesData.contingencies.length : 0;
if (contingenciesData) {
  for (const c of (contingenciesData.contingencies || [])) {
    for (const [key, value] of Object.entries(c)) {
      if (value && typeof value === 'object' && !Array.isArray(value) && value.specimens) {
        for (const specId of value.specimens) {
          contingencyPlacements[specId] = (contingencyPlacements[specId] || 0) + 1;
        }
      }
    }
  }
}

// Insight mentions: specimenId → count of insights it appears in as evidence
const insightMentions = {};
if (insightsData) {
  for (const insight of (insightsData.insights || [])) {
    for (const ev of (insight.evidence || [])) {
      if (ev.specimenId) {
        insightMentions[ev.specimenId] = (insightMentions[ev.specimenId] || 0) + 1;
      }
    }
  }
}

// Scan tracker: specimenId → { lastScanned, claimsFound, quality }
const scanStatus = {};
if (scanTracker) {
  for (const s of (scanTracker.specimens || [])) {
    scanStatus[s.specimenId] = {
      lastScanned: s.lastScanned,
      claimsFound: s.claimsFound || 0,
      quality: s.quality || 'unknown',
    };
  }
}

// Claims per specimen
const claimCounts = {};
if (claimsRegistry) {
  for (const claim of (claimsRegistry.claims || [])) {
    if (claim.specimenId) {
      claimCounts[claim.specimenId] = (claimCounts[claim.specimenId] || 0) + 1;
    }
  }
}

// Enrichment files: set of specimen IDs with enrichment
const enrichmentDir = path.join(RESEARCH_DIR, 'purpose-claims', 'enrichment');
const enrichmentIds = new Set();
if (fs.existsSync(enrichmentDir)) {
  for (const f of fs.readdirSync(enrichmentDir).filter(f => f.endsWith('.json'))) {
    enrichmentIds.add(f.replace('.json', ''));
  }
}

// Synthesis queue status: specimenId → status
const synthStatus = {};
if (synthQueue) {
  for (const item of (synthQueue.queue || [])) {
    if (item.specimenId) {
      synthStatus[item.specimenId] = item.status || 'pending';
    }
  }
}

// ── Build lifecycle records ──

const lifecycleRecords = [];

for (const spec of registry.specimens) {
  const id = spec.id;
  const isActive = spec.status !== 'Inactive';

  // Read specimen file for last modified date
  const specFile = path.join(SPECIMENS_DIR, `${id}.json`);
  let specData = null;
  let lastCurated = null;
  if (fs.existsSync(specFile)) {
    specData = loadJSON(specFile);
    if (specData && specData.meta) {
      lastCurated = specData.meta.lastUpdated || specData.meta.created || null;
    }
  }

  const record = {
    id,
    status: spec.status || 'Active',
    model: spec.structuralModel || null,
    orientation: spec.orientation || null,
    completeness: spec.completeness || null,
    confidence: spec.confidence || null,
    // Pipeline stages
    curated: lastCurated,
    synthesized: synthStatus[id] || null,
    tensionPlacements: tensionPlacements[id] || 0,
    contingencyPlacements: contingencyPlacements[id] || 0,
    insightMentions: insightMentions[id] || 0,
    // Purpose claims track
    claimCount: claimCounts[id] || 0,
    scanQuality: scanStatus[id] ? scanStatus[id].quality : 'unscanned',
    lastScanned: scanStatus[id] ? scanStatus[id].lastScanned : null,
    hasEnrichment: enrichmentIds.has(id),
  };

  lifecycleRecords.push(record);
}

// Sort: active first, then by completeness (High > Medium > Low), then alphabetical
const completenessOrder = { High: 0, Medium: 1, Low: 2 };
lifecycleRecords.sort((a, b) => {
  if (a.status === 'Inactive' && b.status !== 'Inactive') return 1;
  if (a.status !== 'Inactive' && b.status === 'Inactive') return -1;
  const ca = completenessOrder[a.completeness] ?? 3;
  const cb = completenessOrder[b.completeness] ?? 3;
  if (ca !== cb) return ca - cb;
  return a.id.localeCompare(b.id);
});

// ── Generate machine-readable output ──

const jsonOutput = {
  generated: new Date().toISOString().split('T')[0],
  totalSpecimens: lifecycleRecords.filter(r => r.status !== 'Inactive').length,
  inactiveSpecimens: lifecycleRecords.filter(r => r.status === 'Inactive').length,
  totalTensions: TOTAL_TENSIONS,
  totalContingencies: TOTAL_CONTINGENCIES,
  totalInsights: insightsData ? (insightsData.insights || []).length : 0,
  totalClaims: claimsRegistry ? (claimsRegistry.claims || []).length : 0,
  summary: {
    fullyPlacedTensions: lifecycleRecords.filter(r => r.status !== 'Inactive' && r.tensionPlacements === TOTAL_TENSIONS).length,
    fullyPlacedContingencies: lifecycleRecords.filter(r => r.status !== 'Inactive' && r.contingencyPlacements === TOTAL_CONTINGENCIES).length,
    withClaims: lifecycleRecords.filter(r => r.status !== 'Inactive' && r.claimCount > 0).length,
    withEnrichment: lifecycleRecords.filter(r => r.status !== 'Inactive' && r.hasEnrichment).length,
    synthesized: lifecycleRecords.filter(r => r.status !== 'Inactive' && r.synthesized === 'synthesized').length,
    mentionedInInsights: lifecycleRecords.filter(r => r.status !== 'Inactive' && r.insightMentions > 0).length,
  },
  specimens: lifecycleRecords,
};

fs.writeFileSync(
  path.join(DATA_DIR, 'specimen-lifecycle-status.json'),
  JSON.stringify(jsonOutput, null, 2) + '\n'
);

// ── Generate human-readable output ──

const lines = [];
lines.push('# Specimen Lifecycle Status');
lines.push(`**Generated:** ${jsonOutput.generated}`);
lines.push('');
lines.push('## Summary');
lines.push(`| Metric | Count |`);
lines.push(`|--------|-------|`);
lines.push(`| Active specimens | ${jsonOutput.totalSpecimens} |`);
lines.push(`| Inactive specimens | ${jsonOutput.inactiveSpecimens} |`);
lines.push(`| Fully placed in all ${TOTAL_TENSIONS} tensions | ${jsonOutput.summary.fullyPlacedTensions} |`);
lines.push(`| Fully placed in all ${TOTAL_CONTINGENCIES} contingencies | ${jsonOutput.summary.fullyPlacedContingencies} |`);
lines.push(`| With purpose claims | ${jsonOutput.summary.withClaims} |`);
lines.push(`| With enrichment data | ${jsonOutput.summary.withEnrichment} |`);
lines.push(`| Mentioned in insights | ${jsonOutput.summary.mentionedInInsights} |`);
lines.push(`| Synthesized | ${jsonOutput.summary.synthesized} |`);
lines.push('');

// Helper for checkmark/cross display
function check(val) {
  if (val === true) return '✓';
  if (val === false || val === 0 || val === null || val === undefined) return '✗';
  return String(val);
}

function tensionDisplay(count) {
  if (count === TOTAL_TENSIONS) return `✓ ${count}/${TOTAL_TENSIONS}`;
  if (count > 0) return `◐ ${count}/${TOTAL_TENSIONS}`;
  return `✗ 0/${TOTAL_TENSIONS}`;
}

function contingencyDisplay(count) {
  if (count === TOTAL_CONTINGENCIES) return `✓ ${count}/${TOTAL_CONTINGENCIES}`;
  if (count > 0) return `◐ ${count}/${TOTAL_CONTINGENCIES}`;
  return `✗ 0/${TOTAL_CONTINGENCIES}`;
}

// Active specimens table
lines.push('## Active Specimens');
lines.push('');
lines.push('| Specimen | Model | Cmpl | Tensions | Contingencies | Claims | Enriched | Insights | Synth |');
lines.push('|----------|-------|------|----------|---------------|--------|----------|----------|-------|');

for (const r of lifecycleRecords.filter(r => r.status !== 'Inactive')) {
  const model = r.model || '—';
  const cmpl = (r.completeness || '—').charAt(0);
  const tens = tensionDisplay(r.tensionPlacements);
  const cont = contingencyDisplay(r.contingencyPlacements);
  const claims = r.claimCount > 0 ? `✓ ${r.claimCount}` : '✗';
  const enriched = r.hasEnrichment ? '✓' : '✗';
  const insights = r.insightMentions > 0 ? `✓ ${r.insightMentions}` : '✗';
  const synth = r.synthesized === 'synthesized' ? '✓' : (r.synthesized === 'pending' ? '◐' : '✗');

  lines.push(`| ${r.id} | ${model} | ${cmpl} | ${tens} | ${cont} | ${claims} | ${enriched} | ${insights} | ${synth} |`);
}

// Inactive specimens (brief)
const inactive = lifecycleRecords.filter(r => r.status === 'Inactive');
if (inactive.length > 0) {
  lines.push('');
  lines.push('## Inactive Specimens');
  lines.push('');
  lines.push('| Specimen | Model | Reason |');
  lines.push('|----------|-------|--------|');
  for (const r of inactive) {
    lines.push(`| ${r.id} | ${r.model || '—'} | Inactive |`);
  }
}

// Gap analysis
lines.push('');
lines.push('## Gap Analysis');
lines.push('');

const noTensions = lifecycleRecords.filter(r => r.status !== 'Inactive' && r.tensionPlacements === 0);
if (noTensions.length > 0) {
  lines.push(`### Not placed in any tension (${noTensions.length})`);
  lines.push(noTensions.map(r => `- ${r.id}`).join('\n'));
  lines.push('');
}

const noContingencies = lifecycleRecords.filter(r => r.status !== 'Inactive' && r.contingencyPlacements === 0);
if (noContingencies.length > 0) {
  lines.push(`### Not placed in any contingency (${noContingencies.length})`);
  lines.push(noContingencies.map(r => `- ${r.id}`).join('\n'));
  lines.push('');
}

const noClaims = lifecycleRecords.filter(r => r.status !== 'Inactive' && r.claimCount === 0);
if (noClaims.length > 0) {
  lines.push(`### No purpose claims (${noClaims.length})`);
  lines.push(noClaims.map(r => `- ${r.id} (scan: ${r.scanQuality})`).join('\n'));
  lines.push('');
}

const noInsights = lifecycleRecords.filter(r => r.status !== 'Inactive' && r.insightMentions === 0 && r.completeness === 'High');
if (noInsights.length > 0) {
  lines.push(`### High-completeness but not mentioned in any insight (${noInsights.length})`);
  lines.push(noInsights.map(r => `- ${r.id}`).join('\n'));
  lines.push('');
}

fs.writeFileSync(
  path.join(DATA_DIR, 'specimen-lifecycle-status.md'),
  lines.join('\n') + '\n'
);

// ── Console summary ──

console.log(`Specimen Lifecycle Status generated:`);
console.log(`  Active: ${jsonOutput.totalSpecimens}, Inactive: ${jsonOutput.inactiveSpecimens}`);
console.log(`  Fully placed (tensions): ${jsonOutput.summary.fullyPlacedTensions}/${jsonOutput.totalSpecimens}`);
console.log(`  Fully placed (contingencies): ${jsonOutput.summary.fullyPlacedContingencies}/${jsonOutput.totalSpecimens}`);
console.log(`  With claims: ${jsonOutput.summary.withClaims}/${jsonOutput.totalSpecimens}`);
console.log(`  With enrichment: ${jsonOutput.summary.withEnrichment}/${jsonOutput.totalSpecimens}`);
console.log(`  Mentioned in insights: ${jsonOutput.summary.mentionedInInsights}/${jsonOutput.totalSpecimens}`);
console.log(`  Synthesized: ${jsonOutput.summary.synthesized}/${jsonOutput.totalSpecimens}`);
console.log(`\n  Output: data/specimen-lifecycle-status.json`);
console.log(`  Output: data/specimen-lifecycle-status.md`);
