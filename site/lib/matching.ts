import type { Specimen } from "@/lib/types/specimen";

export interface MatchInput {
  regulatoryIntensity: string | null;
  timeToObsolescence: string | null;
  ceoTenure: string | null;
  talentMarketPosition: string | null;
  technicalDebt: string | null;
}

export interface DimensionMatch {
  dimension: string;
  label: string;
  userValue: string;
  specimenValue: string | null;
  score: number; // 0, 0.5, or 1
  explanation: string;
}

export interface MatchResult {
  specimen: Specimen;
  score: number; // 0-100
  matchedDimensions: number;
  totalDimensions: number;
  dimensions: DimensionMatch[];
}

// Adjacency maps for partial matching
const REGULATORY_ORDER = ["Low", "Medium", "High"];
const OBSOLESCENCE_ORDER = ["Slow", "Medium", "Fast"];
const TENURE_ORDER = ["Short", "Medium", "Long"]; // Founder treated as Long
const DEBT_ORDER = ["Low", "Medium", "High"];

function ordinalDistance(
  a: string,
  b: string,
  order: string[]
): number {
  const ai = order.indexOf(a);
  const bi = order.indexOf(b);
  if (ai === -1 || bi === -1) return 2; // unknown = no match
  return Math.abs(ai - bi);
}

function scoreDimension(
  userVal: string,
  specimenVal: string | null,
  order: string[] | null,
  label: string,
  normalizeSpecimen?: (v: string) => string
): DimensionMatch {
  if (!specimenVal) {
    return {
      dimension: label,
      label,
      userValue: userVal,
      specimenValue: null,
      score: 0,
      explanation: "No data for this specimen",
    };
  }

  const normalizedSpecimen = normalizeSpecimen
    ? normalizeSpecimen(specimenVal)
    : specimenVal;

  if (userVal === normalizedSpecimen) {
    return {
      dimension: label,
      label,
      userValue: userVal,
      specimenValue: specimenVal,
      score: 1,
      explanation: `Exact match: both ${userVal}`,
    };
  }

  if (order) {
    const dist = ordinalDistance(userVal, normalizedSpecimen, order);
    if (dist === 1) {
      return {
        dimension: label,
        label,
        userValue: userVal,
        specimenValue: specimenVal,
        score: 0.5,
        explanation: `Adjacent: you selected ${userVal}, specimen is ${specimenVal}`,
      };
    }
  }

  return {
    dimension: label,
    label,
    userValue: userVal,
    specimenValue: specimenVal,
    score: 0,
    explanation: `Different: you selected ${userVal}, specimen is ${specimenVal}`,
  };
}

export function scoreSpecimen(
  input: MatchInput,
  specimen: Specimen
): MatchResult {
  const dimensions: DimensionMatch[] = [];
  const contingencies = specimen.contingencies;

  // Only score dimensions the user has selected
  if (input.regulatoryIntensity) {
    dimensions.push(
      scoreDimension(
        input.regulatoryIntensity,
        contingencies.regulatoryIntensity,
        REGULATORY_ORDER,
        "Regulatory Intensity"
      )
    );
  }

  if (input.timeToObsolescence) {
    dimensions.push(
      scoreDimension(
        input.timeToObsolescence,
        contingencies.timeToObsolescence,
        OBSOLESCENCE_ORDER,
        "Time to Obsolescence"
      )
    );
  }

  if (input.ceoTenure) {
    dimensions.push(
      scoreDimension(
        input.ceoTenure,
        contingencies.ceoTenure,
        TENURE_ORDER,
        "CEO Tenure",
        (v) => (v === "Founder" ? "Long" : v) // Founder ≈ Long
      )
    );
  }

  if (input.talentMarketPosition) {
    dimensions.push(
      scoreDimension(
        input.talentMarketPosition,
        contingencies.talentMarketPosition,
        null, // No ordinal scale for talent
        "Talent Position"
      )
    );
  }

  if (input.technicalDebt) {
    dimensions.push(
      scoreDimension(
        input.technicalDebt,
        contingencies.technicalDebt,
        DEBT_ORDER,
        "Technical Debt"
      )
    );
  }

  const totalDimensions = dimensions.length;
  const totalScore = dimensions.reduce((sum, d) => sum + d.score, 0);
  const maxScore = totalDimensions;

  return {
    specimen,
    score: maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0,
    matchedDimensions: dimensions.filter((d) => d.score > 0).length,
    totalDimensions,
    dimensions,
  };
}

export function rankSpecimens(
  input: MatchInput,
  specimens: Specimen[]
): MatchResult[] {
  // If no inputs selected, return empty
  const hasInput = Object.values(input).some(Boolean);
  if (!hasInput) return [];

  return specimens
    .map((s) => scoreSpecimen(input, s))
    .filter((r) => r.score > 0)
    .sort((a, b) => b.score - a.score || a.specimen.name.localeCompare(b.specimen.name));
}
