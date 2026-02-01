import type { StructuralModel, Orientation } from "./specimen";

export const STRUCTURAL_MODELS: Record<
  StructuralModel,
  { name: string; shortName: string; description: string }
> = {
  1: {
    name: "Research Lab",
    shortName: "M1",
    description: "Fundamental research, breakthroughs (3-10 year horizon)",
  },
  2: {
    name: "Center of Excellence",
    shortName: "M2",
    description: "Governance, standards, enablement (6-24 month horizon)",
  },
  3: {
    name: "Embedded Teams",
    shortName: "M3",
    description: "Product-specific AI features (quarterly horizon)",
  },
  4: {
    name: "Hybrid/Hub-and-Spoke",
    shortName: "M4",
    description: "Central standards + distributed execution (mixed horizon)",
  },
  5: {
    name: "Product/Venture Lab",
    shortName: "M5",
    description: "Commercialize AI into products (6-36 month horizon)",
  },
  6: {
    name: "Unnamed/Informal",
    shortName: "M6",
    description: "Quiet transformation without formal structure",
  },
  7: {
    name: "Tiger Teams",
    shortName: "M7",
    description: "Time-boxed exploration sprints (weeks to months)",
  },
} as const;

export const SUB_TYPES: Record<string, string> = {
  "5a": "Internal Incubator",
  "5b": "Venture Builder",
  "5c": "Platform-to-Product",
  "6a": "Enterprise-Wide Adoption",
  "6b": "Centralized-but-Unnamed",
  "6c": "Grassroots/Bottom-Up",
} as const;

export const ORIENTATIONS: readonly Orientation[] = [
  "Structural",
  "Contextual",
  "Temporal",
] as const;

export const ORIENTATION_DESCRIPTIONS: Record<Orientation, string> = {
  Structural:
    "Exploration and execution in distinct units with ring-fenced budgets and separate reporting lines",
  Contextual:
    "Individuals balance exploration and execution within their roles",
  Temporal:
    "Organization cycles between exploration and execution phases over time",
};

export const MODEL_NUMBERS: readonly StructuralModel[] = [
  1, 2, 3, 4, 5, 6, 7,
] as const;
