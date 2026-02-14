#!/usr/bin/env node

/**
 * check-source-freshness.js
 * Flags sources that haven't been scanned recently.
 *
 * Thresholds:
 *   Tier 1: stale after 14 days
 *   Tier 2: stale after 30 days
 *
 * Reads: specimens/source-registry.json
 * Run from project root: node scripts/check-source-freshness.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SOURCE_REGISTRY_PATH = path.join(ROOT, 'specimens', 'source-registry.json');

const TIER1_STALE_DAYS = 14;
const TIER2_STALE_DAYS = 30;

function loadJSON(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    console.error(`Cannot read ${path.relative(ROOT, filePath)}: ${e.message}`);
    return null;
  }
}

const sourceRegistry = loadJSON(SOURCE_REGISTRY_PATH);
if (!sourceRegistry) {
  console.error('Cannot load source-registry.json — aborting');
  process.exit(1);
}

const sources = sourceRegistry.sources || [];
const now = new Date();

const stale = [];
const neverScanned = [];
const fresh = [];

for (const source of sources) {
  const staleDays = source.tier === 1 ? TIER1_STALE_DAYS : TIER2_STALE_DAYS;

  if (!source.lastScanned) {
    neverScanned.push(source);
    continue;
  }

  const lastDate = new Date(source.lastScanned);
  const daysAgo = Math.floor((now - lastDate) / (1000 * 60 * 60 * 24));

  if (daysAgo > staleDays) {
    stale.push({ ...source, daysAgo, threshold: staleDays });
  } else {
    fresh.push({ ...source, daysAgo });
  }
}

// ── Output ──

console.log('Source Freshness Report');
console.log(`Generated: ${now.toISOString().split('T')[0]}`);
console.log(`Thresholds: Tier 1 = ${TIER1_STALE_DAYS} days, Tier 2 = ${TIER2_STALE_DAYS} days`);
console.log('');

if (stale.length > 0) {
  console.log(`⚠️  STALE SOURCES (${stale.length}):`);
  // Sort by staleness (most overdue first)
  stale.sort((a, b) => b.daysAgo - a.daysAgo);
  for (const s of stale) {
    console.log(`  ${s.name} (Tier ${s.tier}): ${s.daysAgo} days since last scan (threshold: ${s.threshold}d)`);
    if (s.scannedThrough) {
      console.log(`    Last coverage: ${s.scannedThrough.substring(0, 80)}${s.scannedThrough.length > 80 ? '...' : ''}`);
    }
  }
  console.log('');
}

if (neverScanned.length > 0) {
  console.log(`❌ NEVER SCANNED (${neverScanned.length}):`);
  for (const s of neverScanned) {
    console.log(`  ${s.name} (Tier ${s.tier}): ${s.type}`);
  }
  console.log('');
}

if (fresh.length > 0) {
  console.log(`✅ FRESH (${fresh.length}):`);
  // Sort by days since scan (oldest first)
  fresh.sort((a, b) => b.daysAgo - a.daysAgo);
  for (const s of fresh) {
    console.log(`  ${s.name} (Tier ${s.tier}): scanned ${s.daysAgo} day${s.daysAgo === 1 ? '' : 's'} ago`);
  }
  console.log('');
}

// Summary
const total = sources.length;
console.log('────────────────────────────');
console.log(`Total: ${total} sources | Fresh: ${fresh.length} | Stale: ${stale.length} | Never scanned: ${neverScanned.length}`);

if (stale.length > 0 || neverScanned.length > 0) {
  process.exit(1);
}
