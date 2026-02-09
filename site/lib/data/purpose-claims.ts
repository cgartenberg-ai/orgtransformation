import fs from "fs/promises";
import path from "path";
import type { ClaimType, PurposeClaim, PurposeClaimsData } from "@/lib/types/purpose-claims";

const DATA_ROOT = path.resolve(process.cwd(), "..");
const CLAIMS_FILE = path.join(DATA_ROOT, "research", "purpose-claims", "registry.json");

/**
 * Load the full purpose claims registry.
 */
export async function getPurposeClaims(): Promise<PurposeClaimsData> {
  const raw = await fs.readFile(CLAIMS_FILE, "utf-8");
  return JSON.parse(raw) as PurposeClaimsData;
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
