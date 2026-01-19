// Framework types
export interface Layer {
  id: string;
  name: string;
  description: string;
  principles: string[]; // IDs of architectural principles in this layer
  color: string;
}

export interface ArchitecturalPrinciple {
  id: string;
  name: string;
  layerId: string;
  coreQuestion: string;
  whyArchitectural: string;
  status: 'available' | 'coming-soon';
}

export interface DiagramTemplate {
  id: string;
  name: string;
  description: string;
  svgPath: string; // Path to SVG or inline SVG
}

export interface PrincipleGroup {
  id: string;
  name: string;
  color: string;
  principles: string[]; // IDs of design principles
}

export interface Tension {
  id: string;
  principles: [string, string]; // Pair of architectural principle IDs
  description: string;
  guidance: string;
}

// Case types
export interface CaseContent {
  whatItIs: string;
  howItWorks: string[];
  coreInsight: string;
  keyMetrics?: string;
  sources: string[];
}

export interface Conversation {
  id: string;
  question: string;
  answer: string;
  source?: string;
  addedToContent: boolean;
  timestamp: string;
}

export interface Case {
  id: string;
  company: string;
  title: string;
  summary: string;
  diagramTemplate: string;
  architecturalPrinciples: string[];
  designPrinciples: string[];
  content: CaseContent;
  conversations: Conversation[];
  extendedContent: Record<string, string>;
}

// Design Principle types
export interface DesignPrinciple {
  id: string;
  title: string;
  group: string;
  architecturalPrinciples: string[];
  insight: string;
  manifestations: string[];
  test: string;
  conversations: Conversation[];
  extendedContent: Record<string, string>;
}

// Library aggregate
export interface Library {
  layers: Layer[];
  architecturalPrinciples: ArchitecturalPrinciple[];
  diagramTemplates: DiagramTemplate[];
  principleGroups: PrincipleGroup[];
  tensions: Tension[];
  cases: Case[];
  designPrinciples: DesignPrinciple[];
}
