#!/usr/bin/env node
/**
 * Converts old-format case JSON files to new specimen format.
 *
 * Usage: node convert-cases.js
 *
 * Reads from: library/cases/*.json
 * Writes to: specimens/*.json
 * Updates: specimens/registry.json
 */

const fs = require('fs');
const path = require('path');

const BASE = path.resolve(__dirname, '..');
const CASES_DIR = path.join(BASE, 'library', 'cases');
const SPECIMENS_DIR = path.join(BASE, 'specimens');

// Skip these files (not real cases, or already converted)
const SKIP_FILES = new Set([
  'case-anthropic.json',
  'case-pg-chatpg.json',
  'case-eli-lilly.json',
]);

// Already converted as type specimens — skip
const ALREADY_CONVERTED = new Set([
  'eli-lilly.json',
  'google-x.json',
  'bank-of-america.json',
  'pg-chatpg.json',
  'samsung-c-lab.json',
]);

// Phenotype → structural model mapping
const PHENOTYPE_TO_MODEL = {
  'research-lab': { model: 1, modelName: 'Research Lab' },
  'coe': { model: 2, modelName: 'Center of Excellence' },
  'embedded': { model: 3, modelName: 'Embedded Teams' },
  'hybrid': { model: 4, modelName: 'Hybrid/Hub-and-Spoke' },
  'product-venture-lab': { model: 5, modelName: 'Product/Venture Lab' },
  'unnamed-informal': { model: 6, modelName: 'Unnamed/Informal' },
  'tiger-teams': { model: 7, modelName: 'Tiger Teams' },
};

// Subtype mapping
const SUBTYPE_MAP = {
  'internal-incubator': { subType: '5a', subTypeName: 'Internal Incubator' },
  'venture-builder': { subType: '5b', subTypeName: 'Venture Builder' },
  'platform-to-product': { subType: '5c', subTypeName: 'Platform-to-Product' },
  'enterprise-adoption': { subType: '6a', subTypeName: 'Enterprise-Wide Adoption' },
  'centralized-unnamed': { subType: '6b', subTypeName: 'Centralized-but-Unnamed' },
  'grassroots': { subType: '6c', subTypeName: 'Grassroots/Bottom-Up' },
};

// Design principle → mechanism mapping
const PRINCIPLE_TO_MECHANISM = {
  'protect-deviations': { id: 1, name: 'Protect Off-Strategy Work' },
  'ceo-as-political-shield': { id: 1, name: 'Protect Off-Strategy Work' },
  'reward-fast-failure': { id: 2, name: 'Bonus Teams That Kill Projects' },
  'internal-first-validation': { id: 3, name: 'Embed Product at Research Frontier' },
  'consumer-grade-ux': { id: 4, name: 'Consumer-Grade UX for Employee Tools' },
  'rapid-iteration-cycles': { id: 5, name: 'Deploy to Thousands Before You Know What Works' },
  'mandatory-proficiency': null, // maps to contextual orientation, not a specific mechanism
  'ride-the-exponential': null, // philosophy, not a mechanism
  'ring-fence-budget': { id: 1, name: 'Protect Off-Strategy Work' },
  'domain-expertise': null,
  'governance-lets-it-cook': { id: 1, name: 'Protect Off-Strategy Work' },
  'exit-paths-entrepreneurs': null,
  'protected-exploration-time': null,
  'a-team-capability': null,
};

// Industry inference from company name/content
const INDUSTRY_HINTS = {
  'pharma': 'Pharmaceuticals',
  'drug': 'Pharmaceuticals',
  'biotech': 'Biotechnology',
  'mRNA': 'Biotechnology',
  'bank': 'Financial Services',
  'financial': 'Financial Services',
  'insurance': 'Insurance',
  'consult': 'Professional Services',
  'government': 'Government',
  'retail': 'Retail',
  'ecommerce': 'E-commerce',
  'auto': 'Automotive',
  'robot': 'Robotics',
  'electronics': 'Consumer Electronics',
  'software': 'Technology',
  'cloud': 'Technology',
  'semiconductor': 'Semiconductors',
  'security': 'Cybersecurity',
  'industrial': 'Industrial',
  'energy': 'Energy',
  'printing': 'Manufacturing',
  'education': 'Education',
  'healthcare': 'Healthcare',
};

function inferIndustry(old) {
  const text = `${old.company} ${old.content?.whatItIs || ''} ${old.summary || ''}`.toLowerCase();
  for (const [hint, industry] of Object.entries(INDUSTRY_HINTS)) {
    if (text.includes(hint.toLowerCase())) return industry;
  }
  return 'Technology'; // default
}

// Infer orientation from phenotype and content
function inferOrientation(old) {
  const phenotype = old.phenotype;
  const principles = old.designPrinciples || [];
  const text = `${old.content?.whatItIs || ''} ${old.content?.howItWorks?.join(' ') || ''}`.toLowerCase();

  // Contextual signals
  if (principles.includes('mandatory-proficiency') ||
      text.includes('every employee') || text.includes('all employees') ||
      text.includes('proficiency') || text.includes('embedded in every role')) {
    return 'Contextual';
  }

  // Temporal signals
  if (phenotype === 'tiger-teams' || text.includes('time-boxed') ||
      text.includes('sprint') || text.includes('temporary')) {
    return 'Temporal';
  }

  // Model-based defaults
  if (phenotype === 'research-lab' || phenotype === 'product-venture-lab') return 'Structural';
  if (phenotype === 'unnamed-informal') return 'Contextual';
  if (phenotype === 'embedded') return 'Contextual';
  if (phenotype === 'coe') return 'Structural';
  if (phenotype === 'hybrid') return 'Structural';

  return 'Structural'; // default
}

function extractQuotes(old) {
  const quotes = [];
  const insight = old.content?.coreInsight || '';

  // Try to parse quotes from coreInsight
  const quoteMatch = insight.match(/(?:['"]|:\s*')(.+?)(?:['"])/);
  if (quoteMatch) {
    // Try to find speaker
    const speakerMatch = insight.match(/(?:CEO|CTO|CPO|CAIO|Chief|President|VP|Head|Director|Founder)\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)/);
    const nameBeforeQuote = insight.match(/([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)(?:\s*:|\s+says|\s+said)/);

    quotes.push({
      text: quoteMatch[1],
      speaker: speakerMatch?.[1] || nameBeforeQuote?.[1] || null,
      speakerTitle: null,
      source: null,
      sourceUrl: null,
      timestamp: null,
      date: null
    });
  }

  return quotes;
}

function extractMechanisms(old) {
  const principles = old.designPrinciples || [];
  const mechanisms = [];
  const seen = new Set();

  for (const p of principles) {
    const mech = PRINCIPLE_TO_MECHANISM[p];
    if (mech && !seen.has(mech.id)) {
      seen.add(mech.id);
      mechanisms.push({
        id: mech.id,
        name: mech.name,
        evidence: `Identified via design principle '${p}' in original case data. Evidence needs strengthening from sources.`,
        strength: 'Moderate'
      });
    }
  }

  return mechanisms;
}

function buildSources(old) {
  const rawSources = old.content?.sources || [];
  return rawSources.map((s, i) => ({
    id: `source-${i + 1}`,
    type: inferSourceType(s),
    name: s,
    url: null,
    timestamp: null,
    sourceDate: null,
    collectedDate: old.lastUpdated || '2026-01-20',
    notes: null
  }));
}

function inferSourceType(sourceName) {
  const s = sourceName.toLowerCase();
  if (s.includes('podcast') || s.includes('pint') || s.includes('priors')) return 'Podcast';
  if (s.includes('substack') || s.includes('newsletter')) return 'Substack';
  if (s.includes('press') || s.includes('newsroom')) return 'Press Release';
  if (s.includes('linkedin')) return 'LinkedIn';
  if (s.includes('sec') || s.includes('10-k') || s.includes('filing')) return 'SEC Filing';
  if (s.includes('earning')) return 'Earnings Call';
  if (s.includes('blog') || s.includes('signal')) return 'Blog';
  if (s.includes('journal') || s.includes('review') || s.includes('hbr') || s.includes('mit')) return 'Academic Paper';
  if (s.includes('interview')) return 'Interview';
  if (s.includes('report') || s.includes('study') || s.includes('case study')) return 'Report';
  return 'Press';
}

function buildLayers(old) {
  const layers = [];
  const lastUpdated = old.lastUpdated || '2026-01-20';
  const datePrefix = lastUpdated.substring(0, 7); // YYYY-MM

  // If there's extendedContent, that's likely a more recent layer
  const ext = old.extendedContent || {};
  const extKeys = Object.keys(ext).filter(k => ext[k] && typeof ext[k] === 'string' && ext[k].length > 10);

  if (extKeys.length > 0) {
    layers.push({
      date: datePrefix,
      label: 'Latest Update',
      summary: extKeys.map(k => ext[k]).join(' ').substring(0, 300) + (extKeys.map(k => ext[k]).join(' ').length > 300 ? '...' : ''),
      classification: null,
      sourceRefs: []
    });
  }

  // Base layer from original content
  layers.push({
    date: extKeys.length > 0 ? '2025' : datePrefix,
    label: 'Initial Documentation',
    summary: old.content?.whatItIs || old.summary || '',
    classification: null,
    sourceRefs: buildSources(old).map(s => s.id)
  });

  return layers;
}

function convertCase(old, filename) {
  const phenotypeInfo = PHENOTYPE_TO_MODEL[old.phenotype] || { model: null, modelName: '' };
  const subtypeInfo = old.phenotypeSubtype ? (SUBTYPE_MAP[old.phenotypeSubtype] || { subType: null, subTypeName: null }) : { subType: null, subTypeName: null };
  const orientation = inferOrientation(old);

  const description = [
    old.content?.whatItIs || '',
    '',
    (old.content?.howItWorks || []).map(h => `- ${h}`).join('\n'),
  ].filter(Boolean).join('\n');

  return {
    id: old.id,
    name: old.company,
    title: old.title,

    classification: {
      structuralModel: phenotypeInfo.model,
      structuralModelName: phenotypeInfo.modelName,
      subType: subtypeInfo.subType,
      subTypeName: subtypeInfo.subTypeName,
      secondaryModel: null,
      secondaryModelName: null,
      orientation: orientation,
      orientationName: orientation,
      confidence: 'Medium',
      classificationRationale: `Auto-converted from legacy phenotype '${old.phenotype}'${old.phenotypeSubtype ? ` / '${old.phenotypeSubtype}'` : ''}. Orientation inferred from content and design principles. Needs human review.`,
      typeSpecimen: false
    },

    habitat: {
      industry: inferIndustry(old),
      sector: null,
      orgSize: 'Enterprise',
      employees: null,
      revenue: null,
      headquarters: null,
      geography: null
    },

    description: description,

    observableMarkers: {
      reportingStructure: null,
      resourceAllocation: null,
      timeHorizons: null,
      decisionRights: null,
      metrics: old.content?.keyMetrics || null
    },

    mechanisms: extractMechanisms(old),
    quotes: extractQuotes(old),
    layers: buildLayers(old),
    sources: buildSources(old),

    contingencies: {
      regulatoryIntensity: null,
      timeToObsolescence: null,
      ceoTenure: null,
      talentMarketPosition: null,
      technicalDebt: null
    },

    tensionPositions: {
      structuralVsContextual: null,
      speedVsDepth: null,
      centralVsDistributed: null,
      namedVsQuiet: null,
      longVsShortHorizon: null
    },

    openQuestions: [],
    taxonomyFeedback: [],

    meta: {
      status: 'Active',
      created: '2026-01-31',
      lastUpdated: '2026-01-31',
      completeness: 'Low',
      convertedFrom: `library/cases/${filename}`
    }
  };
}

// Main
function main() {
  const files = fs.readdirSync(CASES_DIR).filter(f => f.endsWith('.json'));
  const converted = [];
  const skipped = [];

  for (const filename of files) {
    if (SKIP_FILES.has(filename) || ALREADY_CONVERTED.has(filename)) {
      skipped.push(filename);
      continue;
    }

    const filePath = path.join(CASES_DIR, filename);
    const raw = fs.readFileSync(filePath, 'utf8');
    let old;
    try {
      old = JSON.parse(raw);
    } catch (e) {
      console.error(`Failed to parse ${filename}: ${e.message}`);
      skipped.push(filename);
      continue;
    }

    // Validate it's a real case file
    if (!old.id || !old.company || !old.content) {
      skipped.push(filename);
      continue;
    }

    const specimen = convertCase(old, filename);
    const outPath = path.join(SPECIMENS_DIR, `${old.id}.json`);

    // Don't overwrite existing type specimens
    if (fs.existsSync(outPath)) {
      console.log(`SKIP (exists): ${old.id}`);
      skipped.push(filename);
      continue;
    }

    fs.writeFileSync(outPath, JSON.stringify(specimen, null, 2) + '\n');
    converted.push(specimen);
    console.log(`CONVERTED: ${old.id} (${old.phenotype}) → Model ${specimen.classification.structuralModel} / ${specimen.classification.orientation}`);
  }

  // Update registry
  const registryPath = path.join(SPECIMENS_DIR, 'registry.json');
  const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));

  // Add converted specimens to registry
  for (const spec of converted) {
    registry.specimens.push({
      id: spec.id,
      name: spec.name,
      structuralModel: spec.classification.structuralModel,
      subType: spec.classification.subType,
      secondaryModel: spec.classification.secondaryModel,
      orientation: spec.classification.orientation,
      typeSpecimen: spec.classification.typeSpecimen,
      status: spec.meta.status,
      created: spec.meta.created,
      lastUpdated: spec.meta.lastUpdated,
      layerCount: spec.layers.length,
      completeness: spec.meta.completeness,
      confidence: spec.classification.confidence
    });
  }

  // Update counts
  registry.totalSpecimens = registry.specimens.length;
  registry.lastUpdated = '2026-01-31';

  const byModel = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0 };
  const byOrientation = { 'Structural': 0, 'Contextual': 0, 'Temporal': 0 };
  for (const s of registry.specimens) {
    if (s.structuralModel) byModel[String(s.structuralModel)]++;
    if (s.orientation) byOrientation[s.orientation]++;
  }
  registry.byModel = byModel;
  registry.byOrientation = byOrientation;

  fs.writeFileSync(registryPath, JSON.stringify(registry, null, 2) + '\n');

  console.log(`\n--- Summary ---`);
  console.log(`Converted: ${converted.length}`);
  console.log(`Skipped: ${skipped.length} (${skipped.join(', ')})`);
  console.log(`Total in registry: ${registry.totalSpecimens}`);
  console.log(`By model:`, byModel);
  console.log(`By orientation:`, byOrientation);
}

main();
