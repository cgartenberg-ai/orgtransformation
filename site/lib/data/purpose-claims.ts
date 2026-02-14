import fs from "fs/promises";
import path from "path";
import type { ClaimType, PurposeClaim, PurposeClaimsData, SpecimenEnrichment } from "@/lib/types/purpose-claims";

const DATA_ROOT = path.resolve(process.cwd(), "..");
const CLAIMS_FILE = path.join(DATA_ROOT, "research", "purpose-claims", "registry.json");
const ENRICHMENT_DIR = path.join(DATA_ROOT, "research", "purpose-claims", "enrichment");

/**
 * Load the full purpose claims registry.
 */
export async function getPurposeClaims(): Promise<PurposeClaimsData> {
  try {
    const raw = await fs.readFile(CLAIMS_FILE, "utf-8");
    return JSON.parse(raw) as PurposeClaimsData;
  } catch (e) {
    console.error("[purpose-claims] Failed to load registry:", e);
    return { claims: [], claimTypes: [], claimTypeDefinitions: {} } as unknown as PurposeClaimsData;
  }
}

/**
 * Get all claims for a specific specimen.
 */
export async function getClaimsBySpecimen(specimenId: string): Promise<PurposeClaim[]> {
  const data = await getPurposeClaims();
  return data.claims.filter((c) => c.specimenId === specimenId);
}

/**
 * Get all claims of a specific type.
 */
export async function getClaimsByType(claimType: ClaimType): Promise<PurposeClaim[]> {
  const data = await getPurposeClaims();
  return data.claims.filter((c) => c.claimType === claimType);
}

/**
 * Get enrichment data for a specific specimen.
 * Returns null if no enrichment file exists.
 */
export async function getSpecimenEnrichment(
  specimenId: string,
): Promise<SpecimenEnrichment | null> {
  const filePath = path.join(ENRICHMENT_DIR, `${specimenId}.json`);
  try {
    const raw = await fs.readFile(filePath, "utf-8");
    return JSON.parse(raw) as SpecimenEnrichment;
  } catch {
    return null;
  }
}

/**
 * Get all enrichment files (for the purpose claims browser overview).
 */
export async function getAllEnrichments(): Promise<SpecimenEnrichment[]> {
  try {
    const files = await fs.readdir(ENRICHMENT_DIR);
    const enrichments: SpecimenEnrichment[] = [];
    for (const file of files) {
      if (!file.endsWith(".json")) continue;
      const raw = await fs.readFile(path.join(ENRICHMENT_DIR, file), "utf-8");
      enrichments.push(JSON.parse(raw));
    }
    return enrichments;
  } catch {
    return [];
  }
}
