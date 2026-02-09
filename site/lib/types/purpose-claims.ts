export type ClaimType =
  | "utopian"
  | "teleological"
  | "higher-calling"
  | "identity"
  | "survival"
  | "commercial-success";

export interface PurposeClaim {
  id: string;
  specimenId: string;
  claimType: ClaimType;
  secondaryType?: ClaimType | null;
  text: string;
  speaker: string;
  speakerTitle: string;
  context: string;
  rhetoricalFunction: string;
  source: string;
  sourceUrl: string;
  sourceType: string;
  sourceDate: string;
  collectedDate: string;
  notes?: string;
}

export interface PurposeClaimsData {
  description: string;
  lastUpdated: string;
  claimTypes: ClaimType[];
  taxonomyVersion: string;
  claimTypeDefinitions: Record<ClaimType, string>;
  claims: PurposeClaim[];
}
