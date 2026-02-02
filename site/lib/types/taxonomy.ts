import type { StructuralModel, Orientation } from "./specimen";

export const STRUCTURAL_MODELS: Record<
  StructuralModel,
  { name: string; shortName: string; description: string; characteristics: string }
> = {
  1: {
    name: "Research Lab",
    shortName: "M1",
    description: "Fundamental research, breakthroughs (3-10 year horizon)",
    characteristics:
      "A ring-fenced research unit focused on fundamental AI breakthroughs with multi-year horizons. Distinguished by academic culture, publication emphasis, and deliberate separation from product timelines. Thrives when the organization tolerates long payback periods and needs frontier research talent.",
  },
  2: {
    name: "Center of Excellence",
    shortName: "M2",
    description: "Governance, standards, enablement (6-24 month horizon)",
    characteristics:
      "A centralized team that sets AI standards, builds shared tooling, and enables business units to adopt AI responsibly. Acts as an internal consultancy — governing without building products directly. Works best when multiple business units need coordinated AI adoption and the organization values consistency over speed.",
  },
  3: {
    name: "Embedded Teams",
    shortName: "M3",
    description: "Product-specific AI features (quarterly horizon)",
    characteristics:
      "AI engineers and data scientists sit inside product or business teams, reporting to product leaders rather than a central AI function. Optimized for fast iteration and deep domain knowledge. Excels when AI is a feature differentiator within existing products and tight feedback loops with customers matter most.",
  },
  4: {
    name: "Hybrid/Hub-and-Spoke",
    shortName: "M4",
    description: "Central standards + distributed execution (mixed horizon)",
    characteristics:
      "Combines a central AI hub (for research, platforms, and standards) with embedded spokes in business units (for domain-specific execution). The most common structure at scale, balancing consistency with local autonomy. Suited to large, diversified organizations that need both shared infrastructure and business-specific AI applications.",
  },
  5: {
    name: "Product/Venture Lab",
    shortName: "M5",
    description: "Commercialize AI into products (6-36 month horizon)",
    characteristics:
      "A semi-autonomous unit chartered to turn AI capabilities into new revenue streams — internal incubators, venture builders, or platform-to-product plays. Distinguished by startup-like incentives, dedicated funding, and a mandate to ship. Thrives when the parent organization wants to explore adjacent markets without disrupting the core business.",
  },
  6: {
    name: "Unnamed/Informal",
    shortName: "M6",
    description: "Quiet transformation without formal structure",
    characteristics:
      "AI adoption happens without a named AI organization — through enterprise-wide tool rollouts, grassroots experimentation, or centralized investment that avoids the 'AI team' label. Often found in organizations where cultural resistance to formal AI programs is high, or where leadership believes AI should be invisible infrastructure rather than a separate function.",
  },
  7: {
    name: "Tiger Teams",
    shortName: "M7",
    description: "Time-boxed exploration sprints (weeks to months)",
    characteristics:
      "Cross-functional strike teams assembled for specific AI missions with fixed timelines and clear deliverables, then disbanded or rotated. Maximizes urgency and focus while minimizing permanent headcount. Best for organizations in early exploration phases or those facing acute competitive pressure that demands rapid proof-of-concept work.",
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
