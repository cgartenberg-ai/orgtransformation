// === Mechanism Types ===

export interface MechanismEvidence {
  specimenId: string;
  quote?: string | null;
  speaker?: string | null;
  source: string;
  notes?: string | null;
}

export interface AffinityDistribution {
  count: number;
  percentage: number;
  specimens?: string[];
}

export interface AffinityProfile {
  modelDistribution: Record<number, AffinityDistribution>;
  orientationDistribution: Record<string, AffinityDistribution>;
  primaryModel: number;
  primaryOrientation: string;
  specimenCount: number;
  affinitySummary: string;
}

export type MechanismMaturity = "emerging" | "confirmed" | "widespread" | "deprecated";
export type FrameworkStatus = "core" | "keep" | "keep-with-caveat";

export interface ConfirmedMechanism {
  id: number;
  name: string;
  definition: string;
  problemItSolves: string;
  theoreticalConnection: string;
  scholarlyAnchor?: string;
  maturity?: MechanismMaturity;
  specimens: string[];
  evidence: MechanismEvidence[];
  affinityProfile?: AffinityProfile;
  // Framework integration (added v0.2)
  findingLink?: string;
  frameworkStatus?: FrameworkStatus;
}

export interface CandidateMechanism {
  name: string;
  observedIn: string[];
  hypothesis: string;
  evidenceNeeded: string;
  specimens: string[];
  demotionReason?: string;
  previousId?: number;
}

export interface MechanismData {
  description: string;
  lastUpdated: string;
  confirmed: ConfirmedMechanism[];
  candidates: CandidateMechanism[];
}

// === Tension Types ===

export interface TensionPole {
  label: string;
  conditions: string[];
}

export interface TensionSpecimenPosition {
  specimenId: string;
  position: number;
  evidence: string;
}

export interface TensionContingencyConnection {
  contingencyId: string;
  relationship: string;
}

export interface TensionDerivation {
  primitives: string[]; // ["P1", "P5"]
  explanation: string;
}

export interface Tension {
  id: number;
  name: string;
  fieldName: string;
  tradeoff: string;
  whenNegative: TensionPole;
  whenPositive: TensionPole;
  keyContingency: string;
  drivers?: string;
  connectedContingencies?: TensionContingencyConnection[];
  interpretiveNote?: string;
  specimens: TensionSpecimenPosition[];
  // Framework integration (added v0.2)
  masterTension?: boolean;
  derivedFrom?: TensionDerivation;
  caveat?: string;
}

export interface TensionData {
  description: string;
  lastUpdated: string;
  tensions: Tension[];
}

// === Contingency Types ===

export interface ContingencyState {
  label?: string;
  favors?: string[];
  mechanisms?: number[];
  specimens: string[];
  notes?: string;
}

export interface ContingencyEvidence {
  finding: string;
  specimens: string[];
}

export interface ContingencyPrimitiveMapping {
  primitive: string; // "P4"
  subDimension?: string; // "P4b"
  relationship: string;
}

export interface ContingencyDefinition {
  id: string;
  name: string;
  whatItDetermines: string;
  evidence?: ContingencyEvidence[];
  // Framework integration (added v0.2)
  primitiveMapping?: ContingencyPrimitiveMapping;
  // Standard levels (most contingencies have these)
  high?: ContingencyState;
  medium?: ContingencyState;
  low?: ContingencyState;
  // Dynamic levels for specific contingencies (e.g., founder, nonTraditional, fast, new, critical)
  [key: string]: ContingencyState | ContingencyEvidence[] | ContingencyPrimitiveMapping | string | undefined;
}

export interface ContingencyData {
  description: string;
  lastUpdated: string;
  contingencies: ContingencyDefinition[];
}

// === Primitive Types (NEW — Framework v0.2) ===

export interface PrimitiveScoringGuide {
  high: string;
  medium: string;
  low: string;
}

export interface PrimitiveSubDimension {
  id: string;
  name: string;
  scoringGuide: PrimitiveScoringGuide;
}

export interface Primitive {
  id: string;
  shortId: string; // "P1", "P2", etc.
  name: string;
  definition: string;
  subDimensions: PrimitiveSubDimension[];
  theoreticalAnchors: string[];
  generatesTensions: number[];
  relatedFindings: string[];
}

export interface PrimitiveData {
  description: string;
  lastUpdated: string;
  primitives: Primitive[];
}

// === Finding Types (NEW — Framework v0.2, replaces Insight) ===

export type FindingMaturity = "hypothesis" | "emerging" | "confirmed";

export interface FindingEvidence {
  specimenId: string;
  note: string;
}

export interface FieldObservation {
  id: string;
  observation: string;
  whyPreserved: string;
  potentialRelevance: string;
}

export interface Finding {
  id: string;
  number: number;
  title: string;
  claim: string;
  primitivesEngaged: string[]; // ["P1", "P5"]
  mechanism: string;
  evidence: FindingEvidence[];
  formerInsights: string[]; // IDs from insights-archive-v1.json
  testableImplications: string[];
  maturity: FindingMaturity;
  paperLink?: string;
  relatedFindings?: string[];
}

export interface FindingData {
  description: string;
  lastUpdated: string;
  findings: Finding[];
  fieldObservations: FieldObservation[];
}

// === Legacy Insight Types (DEPRECATED — kept for backward compatibility) ===

export interface InsightEvidence {
  specimenId: string;
  note: string;
}

export type InsightMaturity = "hypothesis" | "emerging" | "confirmed";

export interface Insight {
  id: string;
  title: string;
  theme: "convergence" | "organizational-form" | "mechanism" | "workforce" | "methodology";
  maturity: InsightMaturity;
  finding: string;
  evidence: InsightEvidence[];
  theoreticalConnection?: string;
  discoveredIn: string;
  relatedMechanisms?: number[];
  relatedTensions?: number[];
}

export interface InsightData {
  description: string;
  lastUpdated: string;
  insights: Insight[];
}
