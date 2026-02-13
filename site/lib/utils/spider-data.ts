import type { ClaimType, PurposeClaim } from "@/lib/types/purpose-claims";

const CLAIM_TYPES: ClaimType[] = [
  "utopian",
  "teleological",
  "higher-calling",
  "identity",
  "survival",
  "commercial-success",
];

/**
 * Normalize a claim type distribution to 0-1 proportions.
 * Each axis = count / total. Specimens with different total claim counts
 * become comparable on shape (rhetorical profile).
 *
 * After proportional normalization, values are rescaled so the largest
 * axis reaches TARGET_MAX (0.85). This preserves the shape but fills
 * the spider chart's visual space — without rescaling, balanced
 * distributions produce values around 0.17 (1/6) and charts are
 * unreadably small.
 */
const TARGET_MAX = 0.85;

export function normalizeDistribution(
  distribution: Partial<Record<ClaimType, number>>
): Record<ClaimType, number> {
  const total = Object.values(distribution).reduce(
    (sum, v) => sum + (v || 0),
    0
  );
  if (total === 0) {
    return Object.fromEntries(
      CLAIM_TYPES.map((t) => [t, 0])
    ) as Record<ClaimType, number>;
  }

  // Step 1: proportional normalization (shape-preserving)
  const proportions = CLAIM_TYPES.map(
    (t) => (distribution[t] || 0) / total
  );

  // Step 2: rescale so max value → TARGET_MAX
  const maxVal = Math.max(...proportions);
  const scale = maxVal > 0 ? TARGET_MAX / maxVal : 1;

  return Object.fromEntries(
    CLAIM_TYPES.map((t, i) => [t, proportions[i] * scale])
  ) as Record<ClaimType, number>;
}

/**
 * Proportional normalization only (no rescaling) — for tooltip percentages.
 * Returns the true proportion each type represents of the total.
 */
export function rawProportions(
  distribution: Partial<Record<ClaimType, number>>
): Record<ClaimType, number> {
  const total = Object.values(distribution).reduce(
    (sum, v) => sum + (v || 0),
    0
  );
  if (total === 0) {
    return Object.fromEntries(
      CLAIM_TYPES.map((t) => [t, 0])
    ) as Record<ClaimType, number>;
  }
  return Object.fromEntries(
    CLAIM_TYPES.map((t) => [t, (distribution[t] || 0) / total])
  ) as Record<ClaimType, number>;
}

/**
 * Average multiple raw claim type distributions, then normalize+rescale.
 *
 * Takes raw count distributions (NOT already-normalized), averages the
 * counts, then applies the same normalize-and-rescale as individual specimens.
 * This ensures average spiders fill the chart space the same way individuals do.
 */
export function averageDistributions(
  rawDistributions: Partial<Record<ClaimType, number>>[]
): Record<ClaimType, number> {
  if (rawDistributions.length === 0) {
    return Object.fromEntries(
      CLAIM_TYPES.map((t) => [t, 0])
    ) as Record<ClaimType, number>;
  }

  // Sum raw counts across all distributions
  const sums: Partial<Record<ClaimType, number>> = {};
  for (const dist of rawDistributions) {
    for (const t of CLAIM_TYPES) {
      sums[t] = (sums[t] || 0) + (dist[t] || 0);
    }
  }

  // Divide by N to get average counts, then normalize+rescale
  const n = rawDistributions.length;
  const avgCounts: Partial<Record<ClaimType, number>> = {};
  for (const t of CLAIM_TYPES) {
    avgCounts[t] = (sums[t] || 0) / n;
  }

  return normalizeDistribution(avgCounts);
}

/**
 * Compute a raw claim type count distribution from a list of claims.
 * Used for specimens that don't have enrichment files.
 */
export function computeDistributionFromClaims(
  claims: PurposeClaim[]
): Partial<Record<ClaimType, number>> {
  const counts: Partial<Record<ClaimType, number>> = {};
  for (const c of claims) {
    counts[c.claimType] = (counts[c.claimType] || 0) + 1;
  }
  return counts;
}
