export type StructuralModel = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;

export type SubType = "5a" | "5b" | "5c" | "6a" | "6b" | "6c";

export type Orientation = "Structural" | "Contextual" | "Temporal";

export type Confidence = "High" | "Medium" | "Low";

export type MechanismStrength = "Strong" | "Moderate" | "Emerging";

export type SpecimenStatus = "Active" | "Stub" | "Archived" | "Inactive";

export type Completeness = "High" | "Medium" | "Low";

export type OrgType = "AI-native" | "AI-adopter";

export type OrgSize = "Startup" | "Scaleup" | "Mid-market" | "Enterprise";

export type Geography =
  | "North America"
  | "Europe"
  | "Asia-Pacific"
  | "Global"
  | "Other";

export type RegulatoryIntensity = "High" | "Medium" | "Low";
export type TimeToObsolescence = "Fast" | "Medium" | "Slow";
export type CeoTenure = "Long" | "Medium" | "Short" | "Founder";
export type TalentMarketPosition =
  | "Talent-rich"
  | "Talent-constrained"
  | "Non-traditional";
export type TechnicalDebt = "High" | "Medium" | "Low";

export type SourceType =
  | "Podcast"
  | "Substack"
  | "Press"
  | "SEC Filing"
  | "Earnings Call"
  | "Interview"
  | "Report"
  | "LinkedIn"
  | "Blog"
  | "Academic Paper"
  | "Press Release"
  | "Other";

export interface Classification {
  structuralModel: StructuralModel | null;
  structuralModelName?: string;
  subType: SubType | string | null;
  subTypeName?: string | null;
  secondaryModel: StructuralModel | null;
  secondaryModelName?: string | null;
  orientation: Orientation | null;
  confidence: Confidence;
  classificationRationale?: string | null;
  typeSpecimen: boolean;
}

export interface Habitat {
  industry: string;
  sector?: string | null;
  orgType?: OrgType | null;
  orgSize?: OrgSize | null;
  employees?: number | null;
  revenue?: string | null;
  headquarters?: string | null;
  geography?: Geography | null;
}

export interface ObservableMarkers {
  reportingStructure?: string | null;
  resourceAllocation?: string | null;
  timeHorizons?: string | null;
  decisionRights?: string | null;
  metrics?: string | null;
}

export interface SpecimenMechanism {
  id: number;
  name: string;
  evidence: string;
  strength: MechanismStrength;
}

export interface Quote {
  text: string;
  speaker: string;
  speakerTitle?: string | null;
  source?: string | null;
  sourceUrl?: string | null;
  timestamp?: string | null;
  date?: string | null;
}

export interface Layer {
  date: string;
  label?: string | null;
  summary: string;
  classification?: string | null;
  sourceRefs: string[];
}

export interface Source {
  id: string;
  type: SourceType;
  name: string;
  url?: string | null;
  timestamp?: string | null;
  sourceDate?: string | null;
  collectedDate?: string | null;
  notes?: string | null;
}

export type EnvironmentalAiPull = "High" | "Medium" | "Low";

export interface Contingencies {
  regulatoryIntensity: RegulatoryIntensity | null;
  timeToObsolescence: TimeToObsolescence | null;
  ceoTenure: CeoTenure | null;
  talentMarketPosition: TalentMarketPosition | null;
  technicalDebt: TechnicalDebt | null;
  environmentalAiPull?: EnvironmentalAiPull | null;
}

export interface TensionPositions {
  structuralVsContextual: number | null;
  speedVsDepth: number | null;
  centralVsDistributed: number | null;
  namedVsQuiet: number | null;
  longVsShortHorizon: number | null;
}

export interface SpecimenMeta {
  status: SpecimenStatus;
  created: string;
  lastUpdated: string;
  completeness: Completeness;
  convertedFrom?: string | null;
}

export interface Specimen {
  id: string;
  name: string;
  title: string;
  classification: Classification;
  habitat: Habitat;
  description: string;
  observableMarkers: ObservableMarkers;
  mechanisms: SpecimenMechanism[];
  quotes: Quote[];
  layers: Layer[];
  sources: Source[];
  contingencies: Contingencies;
  tensionPositions: TensionPositions;
  openQuestions?: string[];
  taxonomyFeedback?: string[];
  meta: SpecimenMeta;
}
