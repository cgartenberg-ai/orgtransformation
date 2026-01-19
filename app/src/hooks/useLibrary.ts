import { useMemo } from 'react';
import type { Layer, ArchitecturalPrinciple, Case, DesignPrinciple, PrincipleGroup, DiagramTemplate } from '../types/library';

// Import framework data
import layersData from '../library/framework/layers.json';
import architecturalPrinciplesData from '../library/framework/architecturalPrinciples.json';
import principleGroupsData from '../library/framework/principleGroups.json';
import diagramTemplatesData from '../library/framework/diagramTemplates.json';

// Import case studies
import eliLillyCase from '../library/cases/eli-lilly.json';
import googleXCase from '../library/cases/google-x.json';
import anthropicCase from '../library/cases/anthropic.json';
import samsungCLabCase from '../library/cases/samsung-c-lab.json';
import teslaCase from '../library/cases/tesla.json';
import bankOfAmericaCase from '../library/cases/bank-of-america.json';
import jpmorganCase from '../library/cases/jpmorgan.json';
import mckinseyQuantumBlackCase from '../library/cases/mckinsey-quantumblack.json';
import recursionCase from '../library/cases/recursion.json';
import pgCase from '../library/cases/pg-chatpg.json';
import modernaCase from '../library/cases/moderna.json';
import shopifyCase from '../library/cases/shopify.json';
import nvidiaCase from '../library/cases/nvidia.json';
import sanofiCase from '../library/cases/sanofi.json';
import rocheGenentechCase from '../library/cases/roche-genentech.json';

// Import design principles
import protectDeviations from '../library/designPrinciples/protect-deviations.json';
import rewardFastFailure from '../library/designPrinciples/reward-fast-failure.json';
import rideTheExponential from '../library/designPrinciples/ride-the-exponential.json';
import internalFirstValidation from '../library/designPrinciples/internal-first-validation.json';
import exitPathsEntrepreneurs from '../library/designPrinciples/exit-paths-entrepreneurs.json';
import dataFlywheel from '../library/designPrinciples/data-flywheel.json';
import consumerGradeUx from '../library/designPrinciples/consumer-grade-ux.json';
import rapidIterationCycles from '../library/designPrinciples/rapid-iteration-cycles.json';
import mandatoryProficiency from '../library/designPrinciples/mandatory-proficiency.json';
import domainExpertise from '../library/designPrinciples/domain-expertise.json';
import removeHumanIntuitionBottlenecks from '../library/designPrinciples/remove-human-intuition-bottlenecks.json';
import informationSymmetry from '../library/designPrinciples/information-symmetry.json';
import protectedExplorationTime from '../library/designPrinciples/protected-exploration-time.json';
import ringFenceBudget from '../library/designPrinciples/ring-fence-budget.json';
import governanceLetsItCook from '../library/designPrinciples/governance-lets-it-cook.json';
import aTeamCapability from '../library/designPrinciples/a-team-capability.json';
import labToOperationsHandoff from '../library/designPrinciples/lab-to-operations-handoff.json';
import ceoAsPoliticalShield from '../library/designPrinciples/ceo-as-political-shield.json';

export interface Library {
  layers: Layer[];
  architecturalPrinciples: ArchitecturalPrinciple[];
  principleGroups: PrincipleGroup[];
  diagramTemplates: DiagramTemplate[];
  cases: Case[];
  designPrinciples: DesignPrinciple[];
}

export interface LibraryLookups {
  getLayer: (id: string) => Layer | undefined;
  getArchitecturalPrinciple: (id: string) => ArchitecturalPrinciple | undefined;
  getPrincipleGroup: (id: string) => PrincipleGroup | undefined;
  getDiagramTemplate: (id: string) => DiagramTemplate | undefined;
  getCase: (id: string) => Case | undefined;
  getDesignPrinciple: (id: string) => DesignPrinciple | undefined;
  getCasesForPrinciple: (principleId: string) => Case[];
  getDesignPrinciplesForPrinciple: (principleId: string) => DesignPrinciple[];
  getDesignPrinciplesByGroup: (groupId: string) => DesignPrinciple[];
}

export interface UseLibraryResult {
  library: Library;
  lookups: LibraryLookups;
  isLoading: boolean;
}

export function useLibrary(): UseLibraryResult {
  // Assemble library from static imports
  const library: Library = useMemo(() => ({
    layers: layersData as Layer[],
    architecturalPrinciples: architecturalPrinciplesData as ArchitecturalPrinciple[],
    principleGroups: principleGroupsData as PrincipleGroup[],
    diagramTemplates: diagramTemplatesData as DiagramTemplate[],
    cases: [
      eliLillyCase,
      googleXCase,
      anthropicCase,
      samsungCLabCase,
      teslaCase,
      bankOfAmericaCase,
      jpmorganCase,
      mckinseyQuantumBlackCase,
      recursionCase,
      pgCase,
      modernaCase,
      shopifyCase,
      nvidiaCase,
      sanofiCase,
      rocheGenentechCase,
    ] as Case[],
    designPrinciples: [
      protectDeviations,
      rewardFastFailure,
      rideTheExponential,
      internalFirstValidation,
      exitPathsEntrepreneurs,
      dataFlywheel,
      consumerGradeUx,
      rapidIterationCycles,
      mandatoryProficiency,
      domainExpertise,
      removeHumanIntuitionBottlenecks,
      informationSymmetry,
      protectedExplorationTime,
      ringFenceBudget,
      governanceLetsItCook,
      aTeamCapability,
      labToOperationsHandoff,
      ceoAsPoliticalShield,
    ] as DesignPrinciple[],
  }), []);

  // Create lookup functions
  const lookups: LibraryLookups = useMemo(() => ({
    getLayer: (id: string) => library.layers.find((l) => l.id === id),
    getArchitecturalPrinciple: (id: string) =>
      library.architecturalPrinciples.find((p) => p.id === id),
    getPrincipleGroup: (id: string) =>
      library.principleGroups.find((g) => g.id === id),
    getDiagramTemplate: (id: string) =>
      library.diagramTemplates.find((t) => t.id === id),
    getCase: (id: string) => library.cases.find((c) => c.id === id),
    getDesignPrinciple: (id: string) =>
      library.designPrinciples.find((p) => p.id === id),
    getCasesForPrinciple: (principleId: string) =>
      library.cases.filter((c) =>
        c.architecturalPrinciples.includes(principleId)
      ),
    getDesignPrinciplesForPrinciple: (principleId: string) =>
      library.designPrinciples.filter((p) =>
        p.architecturalPrinciples.includes(principleId)
      ),
    getDesignPrinciplesByGroup: (groupId: string) =>
      library.designPrinciples.filter((p) => p.group === groupId),
  }), [library]);

  return { library, lookups, isLoading: false };
}
