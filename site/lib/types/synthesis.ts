export interface MechanismEvidence {
  specimenId: string;
  quote?: string | null;
  speaker?: string | null;
  source: string;
  notes?: string | null;
}

export interface ConfirmedMechanism {
  id: number;
  name: string;
  definition: string;
  problemItSolves: string;
  theoreticalConnection: string;
  specimens: string[];
  evidence: MechanismEvidence[];
}

export interface CandidateMechanism {
  name: string;
  observedIn: string[];
  hypothesis: string;
  evidenceNeeded: string;
  specimens: string[];
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

export interface Tension {
  id: number;
  name: string;
  fieldName: string;
  tradeoff: string;
  whenNegative: TensionPole;
  whenPositive: TensionPole;
  keyContingency: string;
  specimens: TensionSpecimenPosition[];
}

export interface TensionData {
  description: string;
  lastUpdated: string;
  tensions: Tension[];
}

export interface ContingencyState {
  label: string;
  favors: string[];
  mechanisms: number[];
  specimens: string[];
}

export interface ContingencyDefinition {
  id: string;
  name: string;
  whatItDetermines: string;
  high: ContingencyState;
  low: ContingencyState;
}

export interface ContingencyData {
  description: string;
  lastUpdated: string;
  contingencies: ContingencyDefinition[];
}
