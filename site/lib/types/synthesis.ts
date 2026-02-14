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
}

export interface TensionData {
  description: string;
  lastUpdated: string;
  tensions: Tension[];
}

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

export interface ContingencyDefinition {
  id: string;
  name: string;
  whatItDetermines: string;
  evidence?: ContingencyEvidence[];
  // Standard levels (most contingencies have these)
  high?: ContingencyState;
  medium?: ContingencyState;
  low?: ContingencyState;
  // Dynamic levels for specific contingencies (e.g., founder, nonTraditional, fast, new, critical)
  [key: string]: ContingencyState | ContingencyEvidence[] | string | undefined;
}

export interface ContingencyData {
  description: string;
  lastUpdated: string;
  contingencies: ContingencyDefinition[];
}

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
