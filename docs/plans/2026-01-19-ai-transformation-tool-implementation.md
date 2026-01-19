# AI Transformation Architecture Tool - Implementation Plan

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Build an interactive React application that helps leadership teams develop stances on AI transformation architecture through a five-layer, eight-principle framework with 15 case studies and 18 design principles.

**Architecture:** Static React SPA with JSON-based library content. No backend—localStorage for user state persistence. Library data bundled at build time. Desktop-first responsive design.

**Tech Stack:** React 18, TypeScript, Vite, TailwindCSS, localStorage API

---

## Phase 1: Project Scaffolding & Library Data Structure

### Task 1: Initialize React Project with Vite

**Files:**
- Create: `package.json`
- Create: `vite.config.ts`
- Create: `tsconfig.json`
- Create: `tsconfig.node.json`
- Create: `index.html`
- Create: `src/main.tsx`
- Create: `src/App.tsx`
- Create: `tailwind.config.js`
- Create: `postcss.config.js`
- Create: `src/index.css`

**Step 1: Create the project using Vite**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation
npm create vite@latest app -- --template react-ts
cd app
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Expected: Project scaffolded with React + TypeScript template

**Step 2: Configure Tailwind CSS**

Edit `app/tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        identity: '#6366f1',      // indigo - top layer
        orientation: '#8b5cf6',   // violet
        flow: '#a855f7',          // purple
        structure: '#d946ef',     // fuchsia
        work: '#ec4899',          // pink - bottom layer
      }
    },
  },
  plugins: [],
}
```

**Step 3: Add Tailwind directives to CSS**

Edit `app/src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-50 text-gray-900;
}
```

**Step 4: Verify setup works**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npm run dev
```

Expected: Dev server starts at localhost:5173, shows Vite + React page

**Step 5: Commit**

```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation
git add app/
git commit -m "feat: initialize React + Vite + Tailwind project scaffold"
```

---

### Task 2: Create TypeScript Types for Library Schemas

**Files:**
- Create: `app/src/types/library.ts`
- Create: `app/src/types/userState.ts`

**Step 1: Write the library types**

Create `app/src/types/library.ts`:
```typescript
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
```

**Step 2: Write the user state types**

Create `app/src/types/userState.ts`:
```typescript
export type PrincipleStatus = 'unexplored' | 'in-progress' | 'stance-taken';

export interface PrincipleState {
  status: PrincipleStatus;
  starredCases: string[];
  starredPrinciples: string[];
  notes: string;
  draftStance: string;
  crystallizedStance: string | null;
  lastModified: string;
}

export interface UserState {
  [principleId: string]: PrincipleState;
}

export const createEmptyPrincipleState = (): PrincipleState => ({
  status: 'unexplored',
  starredCases: [],
  starredPrinciples: [],
  notes: '',
  draftStance: '',
  crystallizedStance: null,
  lastModified: new Date().toISOString(),
});
```

**Step 3: Create index exports**

Create `app/src/types/index.ts`:
```typescript
export * from './library';
export * from './userState';
```

**Step 4: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 5: Commit**

```bash
git add app/src/types/
git commit -m "feat: add TypeScript types for library and user state schemas"
```

---

### Task 3: Create Framework JSON Data Files

**Files:**
- Create: `app/src/library/framework/layers.json`
- Create: `app/src/library/framework/architecturalPrinciples.json`
- Create: `app/src/library/framework/principleGroups.json`
- Create: `app/src/library/framework/diagramTemplates.json`

**Step 1: Create layers.json**

Create `app/src/library/framework/layers.json`:
```json
[
  {
    "id": "identity",
    "name": "Identity",
    "description": "Who we are and what we stand for",
    "principles": ["north-star"],
    "color": "#6366f1"
  },
  {
    "id": "orientation",
    "name": "Orientation",
    "description": "How we face the world and make sense of it",
    "principles": ["stance-on-uncertainty", "measurement-philosophy"],
    "color": "#8b5cf6"
  },
  {
    "id": "flow",
    "name": "Flow",
    "description": "How ideas and information move through the organization",
    "principles": ["locus-of-innovation", "information-architecture"],
    "color": "#a855f7"
  },
  {
    "id": "structure",
    "name": "Structure",
    "description": "How we organize people and resources",
    "principles": ["ambidexterity-structure", "resource-allocation"],
    "color": "#d946ef"
  },
  {
    "id": "work",
    "name": "Work",
    "description": "How humans and AI collaborate on tasks",
    "principles": ["human-ai-boundaries"],
    "color": "#ec4899"
  }
]
```

**Step 2: Create architecturalPrinciples.json**

Create `app/src/library/framework/architecturalPrinciples.json`:
```json
[
  {
    "id": "north-star",
    "name": "Organizational North Star",
    "layerId": "identity",
    "coreQuestion": "What is your organization's fundamental identity, and how does AI transformation relate to—or change—that identity?",
    "whyArchitectural": "Your identity determines what kinds of transformation are even conceivable. An organization that sees itself as a 'science company' will approach AI differently than one that sees itself as a 'customer company.'",
    "status": "coming-soon"
  },
  {
    "id": "stance-on-uncertainty",
    "name": "Stance on Uncertainty",
    "layerId": "orientation",
    "coreQuestion": "How does your organization relate to uncertainty, ambiguity, and the unknown in planning and execution?",
    "whyArchitectural": "AI transformation involves deep uncertainty. Organizations that require certainty before acting will struggle with the experimental nature of AI capability building.",
    "status": "coming-soon"
  },
  {
    "id": "measurement-philosophy",
    "name": "Measurement Philosophy",
    "layerId": "orientation",
    "coreQuestion": "What do you measure, and what do your measurements actually drive?",
    "whyArchitectural": "What you measure shapes behavior. Measuring productivity kills exploration. Measuring learning enables it. Your measurement system is your actual strategy.",
    "status": "coming-soon"
  },
  {
    "id": "locus-of-innovation",
    "name": "Locus of Innovation",
    "layerId": "flow",
    "coreQuestion": "Where do you expect the best ideas for AI transformation to originate, and how do you design the organizational mechanisms to cultivate, capture, and deploy them?",
    "whyArchitectural": "The 'lab' question is where transformation becomes concrete. Every other principle ultimately manifests through this one.",
    "status": "available"
  },
  {
    "id": "information-architecture",
    "name": "Information Architecture",
    "layerId": "flow",
    "coreQuestion": "How does information flow through your organization, and how does that enable or constrain AI transformation?",
    "whyArchitectural": "AI systems need data. Where data lives, who can access it, and how it flows determines what AI applications are even possible.",
    "status": "coming-soon"
  },
  {
    "id": "ambidexterity-structure",
    "name": "Ambidexterity Structure",
    "layerId": "structure",
    "coreQuestion": "How do you balance exploitation of current capabilities with exploration of new ones?",
    "whyArchitectural": "Organizations that optimize current operations tend to kill exploration. The structural relationship between 'explore' and 'exploit' is foundational.",
    "status": "coming-soon"
  },
  {
    "id": "resource-allocation",
    "name": "Resource Allocation Logic",
    "layerId": "structure",
    "coreQuestion": "How do resources get allocated between current operations and transformation efforts?",
    "whyArchitectural": "Budget processes often kill transformation by forcing ROI justification for exploratory work. The allocation logic must match the transformation ambition.",
    "status": "coming-soon"
  },
  {
    "id": "human-ai-boundaries",
    "name": "Human-AI Work Boundaries",
    "layerId": "work",
    "coreQuestion": "Where do humans add value that AI cannot, and how do you design work to leverage both?",
    "whyArchitectural": "The boundary between human and AI work is shifting rapidly. Your stance on this boundary determines workforce strategy, skill development, and organizational design.",
    "status": "coming-soon"
  }
]
```

**Step 3: Create principleGroups.json**

Create `app/src/library/framework/principleGroups.json`:
```json
[
  {
    "id": "protection",
    "name": "Protection",
    "color": "#3b82f6",
    "principles": ["protect-deviations", "protected-exploration-time", "ring-fence-budget", "ceo-as-political-shield"]
  },
  {
    "id": "lab-to-org",
    "name": "Lab-to-Org Handoff & Integration",
    "color": "#10b981",
    "principles": ["internal-first-validation", "data-flywheel", "consumer-grade-ux", "information-symmetry", "lab-to-operations-handoff"]
  },
  {
    "id": "incentives",
    "name": "Incentives, Monitoring & Measurement",
    "color": "#f59e0b",
    "principles": ["reward-fast-failure", "governance-lets-it-cook"]
  },
  {
    "id": "culture",
    "name": "Culture",
    "color": "#ef4444",
    "principles": ["mandatory-proficiency"]
  },
  {
    "id": "resources",
    "name": "Resources & Talent",
    "color": "#8b5cf6",
    "principles": ["exit-paths-entrepreneurs", "domain-expertise", "remove-human-intuition-bottlenecks", "a-team-capability"]
  },
  {
    "id": "speed",
    "name": "Managing Speed & Time Horizons",
    "color": "#06b6d4",
    "principles": ["ride-the-exponential", "rapid-iteration-cycles"]
  }
]
```

**Step 4: Create diagramTemplates.json**

Create `app/src/library/framework/diagramTemplates.json`:
```json
[
  {
    "id": "centralized-lab",
    "name": "Centralized Lab",
    "description": "Dedicated unit, separate from operations",
    "svgPath": "centralized-lab.svg"
  },
  {
    "id": "distributed-hubs",
    "name": "Distributed Hubs",
    "description": "Multiple semi-autonomous units",
    "svgPath": "distributed-hubs.svg"
  },
  {
    "id": "embedded-universal",
    "name": "Embedded Universal",
    "description": "AI expected everywhere, no separate lab",
    "svgPath": "embedded-universal.svg"
  },
  {
    "id": "center-of-excellence",
    "name": "Center of Excellence",
    "description": "Central team serving whole org",
    "svgPath": "center-of-excellence.svg"
  },
  {
    "id": "product-as-lab",
    "name": "Product as Lab",
    "description": "Deployed products generate learning",
    "svgPath": "product-as-lab.svg"
  },
  {
    "id": "hybrid-labs-core",
    "name": "Hybrid Labs + Core",
    "description": "Separate exploration + core product",
    "svgPath": "hybrid-labs-core.svg"
  },
  {
    "id": "tight-loop",
    "name": "Tight Loop",
    "description": "Rapid iteration between prediction/validation",
    "svgPath": "tight-loop.svg"
  },
  {
    "id": "external-acquisition",
    "name": "External Acquisition",
    "description": "Capability acquired from outside",
    "svgPath": "external-acquisition.svg"
  },
  {
    "id": "broad-deployment",
    "name": "Broad Deployment",
    "description": "Skip pilots, deploy widely immediately",
    "svgPath": "broad-deployment.svg"
  }
]
```

**Step 5: Verify JSON is valid**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
for f in src/library/framework/*.json; do echo "Checking $f"; cat "$f" | python3 -m json.tool > /dev/null && echo "Valid"; done
```

Expected: All files report "Valid"

**Step 6: Commit**

```bash
git add app/src/library/
git commit -m "feat: add framework JSON data files (layers, principles, groups, templates)"
```

---

### Task 4: Create Case Study JSON Files

**Files:**
- Create: `app/src/library/cases/eli-lilly.json`
- Create: `app/src/library/cases/google-x.json`
- Create: `app/src/library/cases/anthropic.json`
- Create: `app/src/library/cases/samsung-c-lab.json`
- Create: `app/src/library/cases/tesla.json`
- Create: `app/src/library/cases/bank-of-america.json`
- Create: `app/src/library/cases/jpmorgan.json`
- Create: `app/src/library/cases/mckinsey-quantumblack.json`
- Create: `app/src/library/cases/recursion.json`
- Create: `app/src/library/cases/pg-chatpg.json`
- Create: `app/src/library/cases/moderna.json`
- Create: `app/src/library/cases/shopify.json`
- Create: `app/src/library/cases/nvidia.json`
- Create: `app/src/library/cases/sanofi.json`
- Create: `app/src/library/cases/roche-genentech.json`

**Step 1: Create eli-lilly.json**

Create `app/src/library/cases/eli-lilly.json`:
```json
{
  "id": "eli-lilly",
  "company": "Eli Lilly",
  "title": "Decentralized Domain Hubs",
  "summary": "15 years of decentralized R&D hubs of 300-400 people, each operating like a biotech with long time horizons",
  "diagramTemplate": "distributed-hubs",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["protect-deviations", "ring-fence-budget", "domain-expertise", "ceo-as-political-shield"],
  "content": {
    "whatItIs": "Approximately 15 years ago, Lilly decentralized its R&D into smaller hubs of 300-400 people. Each hub operates like a biotech—focused on a specific therapeutic area or modality—but without the burden of fundraising or quarterly investor pressure.",
    "howItWorks": [
      "Small enough to maintain scientific intimacy and shared tacit knowledge",
      "Large enough to have critical mass of capability",
      "Protected from corporate optimization pressure",
      "Long time horizons (the GLP-1 program ran 18+ years from first injection to Mounjaro)",
      "'Teams just grinding on a theme' rather than big-bet single projects"
    ],
    "coreInsight": "CEO Dave Ricks: 'All the studies on middle management find they tend to squash deviations, but the deviations are the people doing stuff off strategy, in the labs, the things that make the next breakthrough.'",
    "keyMetrics": "Drug development cycle: ~7 years vs. industry average of 10. R&D investment target: 20-25% of sales. At $120B revenue, R&D budget approaches NIH scale.",
    "sources": ["Cheeky Pint Podcast (Collison Brothers)", "Chief Executive Magazine", "NVIDIA/Lilly press releases January 2026"]
  },
  "conversations": [],
  "extendedContent": {
    "recentAIEvolution": "In January 2026, Lilly announced a $1B co-innovation lab with NVIDIA in South San Francisco. This adds a 'scientist-in-the-loop' AI capability to the existing decentralized structure—Lilly domain experts co-located with NVIDIA AI engineers. They're also deploying a 1,016 Blackwell Ultra GPU supercomputer (9+ exaflops)—the most powerful owned by a pharma company."
  }
}
```

**Step 2: Create google-x.json**

Create `app/src/library/cases/google-x.json`:
```json
{
  "id": "google-x",
  "company": "Google X",
  "title": "The Moonshot Factory",
  "summary": "100+ experiments annually, 2% graduation rate, teams bonused for killing projects",
  "diagramTemplate": "centralized-lab",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["reward-fast-failure", "ring-fence-budget", "governance-lets-it-cook", "protect-deviations"],
  "content": {
    "whatItIs": "Alphabet's 'moonshot factory'—a dedicated organization for pursuing radical, high-risk innovations with potential for 10x impact. Operates on deliberately different rules than the rest of Google.",
    "howItWorks": [
      "Launches 100+ experiments annually",
      "2% graduation rate (projects that become real businesses after 5-6 years)",
      "Explicit incentives for killing projects: teams get bonuses, applause, hugs, high fives, and promotions for ending projects early",
      "'Pre-mortem' analysis before projects start (predict why it will fail)",
      "'Run at all the hardest parts of the problem first'",
      "Surviving projects get concentrated resources: 44% of X's entire budget goes to the 2% that graduate"
    ],
    "coreInsight": "CEO Astro Teller: The incentive structure is the innovation. By rewarding failure and making project termination a badge of honor, X eliminates the sunk cost fallacy and political protection of zombie projects.",
    "keyMetrics": "Graduates: Waymo, Verily, Wing, Loon, Chronicle",
    "sources": ["TechCrunch Disrupt 2025", "HBR Podcast", "NPR Interview"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 3: Create anthropic.json**

Create `app/src/library/cases/anthropic.json`:
```json
{
  "id": "anthropic",
  "company": "Anthropic",
  "title": "Labs Team + Ride the Exponential",
  "summary": "Dedicated Labs team for zero-to-one ideas, plus 'ride the exponential' product philosophy",
  "diagramTemplate": "hybrid-labs-core",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["ride-the-exponential", "internal-first-validation", "protect-deviations"],
  "content": {
    "whatItIs": "A two-part innovation model: (1) a dedicated Labs team focused on 'disruptive zero-to-one ideas' that operates independently from core product, and (2) a company-wide product philosophy of 'ride the exponential'—building for capabilities that don't exist yet.",
    "howItWorks": [
      "Labs team is separate from main product organization, focused on exploratory/disruptive innovation",
      "Labs built Claude CLI (later Claude Code), early computer use explorations, and other experimental bets",
      "Once Labs creates something promising, it gets 'buttoned up and put on a more fancy suit' for public release",
      "Internal adoption validates before external release: Claude CLI 'rapidly overtook every other coding tool we had internally' in 3 months",
      "Regular hackathons (2-3x/year) where internal teams build on Labs innovations",
      "Over time, they delete parts of the harness rather than add to it because the model can do more"
    ],
    "coreInsight": "CPO Mike Krieger: 'The more you can align with the company's general long-term perspective about where powerful AI will come from, the smoother things will go because [Anthropic] is nothing but focused.'",
    "keyMetrics": "Claude Code: $1B ARR within 6 months of launch. MCP: 'fastest-growing standard in tech history'",
    "sources": ["AI Daily Brief podcast interview with Mike Krieger (December 2025)", "Lenny's Newsletter", "Sequoia Inference Podcast"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 4: Create samsung-c-lab.json**

Create `app/src/library/cases/samsung-c-lab.json`:
```json
{
  "id": "samsung-c-lab",
  "company": "Samsung C-Lab",
  "title": "Separation with Spinoff Path",
  "summary": "Internal incubator with holacracy structure and 20% spinoff rate to independent companies",
  "diagramTemplate": "centralized-lab",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["exit-paths-entrepreneurs", "protected-exploration-time", "governance-lets-it-cook"],
  "content": {
    "whatItIs": "An internal incubator launched in 2012 after Samsung management's Silicon Valley experiences. Operates on two structural innovations: internal holacracy and a defined spinoff pathway.",
    "howItWorks": [
      "Employees vote on ideas, experts review finalists, selected audience plays 'venture capitalists' deciding whether to invest",
      "Selected employees get a full year away from regular duties—100% time, not 20% time",
      "Flat structure: 'Each team has a leader and project members. That's it.' No hierarchical systems",
      "Teams can recruit from outside Samsung if needed talent isn't available internally",
      "Clear exit mechanism: 20% of C-Lab projects have become independent companies",
      "Since 2015, promising projects can spin off as fully-fledged startups"
    ],
    "coreInsight": "Corporate innovation needs both structural freedom (flat hierarchy) AND clear exit paths (spinoff mechanism) to attract entrepreneurial talent and maintain startup-like urgency.",
    "keyMetrics": "As of February 2025: 959 total ventures supported (423 in-house, 536 external through C-Lab Outside)",
    "sources": ["Samsung Global Newsroom", "MDPI Sustainability Journal"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 5: Create tesla.json**

Create `app/src/library/cases/tesla.json`:
```json
{
  "id": "tesla",
  "company": "Tesla",
  "title": "Fleet as Distributed Lab",
  "summary": "1.5 million cars generating training data continuously, vision-only approach at scale",
  "diagramTemplate": "product-as-lab",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["data-flywheel", "remove-human-intuition-bottlenecks"],
  "content": {
    "whatItIs": "Using deployed products as the innovation system. 1.5 million cars globally, each with 8 cameras, continuously generating training data and surfacing edge cases that no human R&D team could anticipate.",
    "howItWorks": [
      "Former AI Director Andrej Karpathy: 'Build a dataset; train your network; deploy it and test it. When you notice that the network is misbehaving, you incorporate the errors into the training set.'",
      "Every week, robots process 1.5 petabytes of data requiring massive compute to train",
      "The fleet identifies edge cases that humans would never anticipate",
      "Vision-only approach (no LiDAR, no HD maps): 'It's actually quite unscalable to collect, build, and maintain high-definition lidar maps.'"
    ],
    "coreInsight": "Design products that generate training data as a byproduct of usage. The more customers use the product, the better it gets. This creates a flywheel competitors without deployed fleets cannot replicate.",
    "keyMetrics": "Cross-domain transfer: The organizational capability built for Autopilot directly enables Tesla Bot (Optimus)",
    "sources": ["Lex Fridman Podcast #333", "Tesla AI Day", "BrainCreators"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 6: Create bank-of-america.json**

Create `app/src/library/cases/bank-of-america.json`:
```json
{
  "id": "bank-of-america",
  "company": "Bank of America",
  "title": "Broad Deployment, Consumer-Grade UX",
  "summary": "Extended consumer Erica to employees, achieving 90%+ adoption across 213,000 employees",
  "diagramTemplate": "center-of-excellence",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["consumer-grade-ux", "rapid-iteration-cycles"],
  "content": {
    "whatItIs": "Rather than a separate innovation lab, BofA's approach treats enterprise AI deployment like a consumer product problem. The 'lab' is essentially a product organization focused on getting tools into everyone's hands with minimal friction.",
    "howItWorks": [
      "Erica (customer-facing virtual assistant) launched 2018",
      "Rather than building a separate employee system, extended Erica internally in 2020 as 'Erica for Employees'",
      "Leveraged existing brand recognition, user familiarity, and proven conversational patterns",
      "Pandemic timing crucial: rapid adoption when employees needed technology support for remote work",
      "Started with IT support, expanded to health benefits, payroll, tax forms—each expansion built on proven interaction patterns"
    ],
    "coreInsight": "Don't build separate enterprise and consumer AI—extend consumer-proven interfaces to employees. The best enterprise AI strategy may be 'Erica for Everyone.' Consumer-grade UX drives adoption; adoption drives value.",
    "keyMetrics": "Over 90% of 213,000 employees actively use AI tools. IT service desk calls reduced by more than 50%. Developer efficiency increased 20% through coding assistants. Over 15 years: headcount reduced from 300,000 to 212,000 while deposits doubled—$6 billion in expense savings.",
    "sources": ["BofA Newsroom", "CTO Magazine", "AIX Expert Network"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 7: Create jpmorgan.json**

Create `app/src/library/cases/jpmorgan.json`:
```json
{
  "id": "jpmorgan",
  "company": "JPMorgan Chase",
  "title": "ML Center of Excellence with Rapid Cycles",
  "summary": "200+ ML scientists, 8-week update cycles, LLM Suite deployed to 250,000 employees",
  "diagramTemplate": "center-of-excellence",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["rapid-iteration-cycles", "a-team-capability", "domain-expertise"],
  "content": {
    "whatItIs": "A centralized Machine Learning Center of Excellence with 200+ ML scientists, software engineers, and product managers positioned globally across three continents. Distinctive for its rapid iteration cadence.",
    "howItWorks": [
      "LLM Suite deployed to 250,000 employees (entire workforce except branch and call center staff)",
      "Half use it roughly every day",
      "'Every eight weeks, LLM Suite is updated as the bank feeds it more from the vast databases and software applications of its major businesses, giving the platform more abilities'",
      "Multi-model architecture using both OpenAI and Anthropic—creating optionality and avoiding vendor lock-in",
      "Led by Chief Analytics Officer Derek Waldron (former McKinsey partner with PhD in computational physics)"
    ],
    "coreInsight": "Enterprise AI transformation requires dedicated ML Centers of Excellence, but the key differentiator is the 8-week update cycle. This creates a flywheel where usage drives improvement drives usage.",
    "keyMetrics": "Vision: 'The JPMorgan Chase of the future is going to be a fully AI-connected enterprise.' Plans include AI agents for every employee, automation of every behind-the-scenes process, and AI concierges for every client experience.",
    "sources": ["CNBC", "American Banker (2025 Innovation of the Year)", "CIO Dive", "JPMorgan Press"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 8: Create mckinsey-quantumblack.json**

Create `app/src/library/cases/mckinsey-quantumblack.json`:
```json
{
  "id": "mckinsey-quantumblack",
  "company": "McKinsey / QuantumBlack",
  "title": "Domain Expertise Acquisition",
  "summary": "Acquired F1 racing analytics firm, scaled from 45 to 1,200+ practitioners",
  "diagramTemplate": "external-acquisition",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["domain-expertise", "a-team-capability"],
  "content": {
    "whatItIs": "A model where AI capability was acquired through purchasing a company with deep domain expertise in a specific, high-stakes field (Formula 1 racing), then generalized to enterprise contexts.",
    "howItWorks": [
      "QuantumBlack founded 2009 in London, specialized in F1 racing analytics—optimizing split-second decisions with advanced data science",
      "McKinsey's insight in 2015: analytical rigor developed for F1 (where milliseconds matter) would translate to enterprise contexts",
      "Acquired the 45-person startup (11 data scientists) and began expanding",
      "The F1 heritage provides credibility: 'we optimized the fastest sport in the world'"
    ],
    "coreInsight": "The best enterprise AI capabilities may come from acquiring teams who've solved extreme versions of common problems. F1 racing analytics to supply chain optimization is a more credible path than pure consulting to AI services.",
    "keyMetrics": "From 45 people in 2015 to 1,200+ practitioners by 2022, now McKinsey's center of excellence for AI, gen AI, and agentic AI. Products: Horizon (AI platform), Lilli (internal knowledge assistant), GAIL (generative AI library), Agents-at-Scale framework.",
    "sources": ["McKinsey Blog", "Consultancy.uk", "Management Consulted"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 9: Create recursion.json**

Create `app/src/library/cases/recursion.json`:
```json
{
  "id": "recursion",
  "company": "Recursion Pharmaceuticals",
  "title": "Automated Hypothesis-Free Discovery",
  "summary": "2.2 million experiments per week, robots 100 feet from CEO, hypothesis-agnostic discovery",
  "diagramTemplate": "tight-loop",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["remove-human-intuition-bottlenecks", "data-flywheel", "rapid-iteration-cycles"],
  "content": {
    "whatItIs": "A lab where the primary 'researcher' is an automated system running 2.2 million experiments per week. Humans design the system and interpret results, but the discovery process itself is largely automated and hypothesis-agnostic.",
    "howItWorks": [
      "Robots run up to 2.2 million experiments weekly, generating 40 petabytes of data from over 300+ million experiments",
      "CEO Chris Gibson: 'I'm currently sitting 100 feet away from a giant lab full of robots.'",
      "Traditional pharma starts with hypotheses about disease mechanisms. Recursion inverts this: 'The company's platform is capable of finding novel biology that may have been overlooked by humans, or considered too challenging to pursue.'",
      "LOWE: an LLM-based interface where scientists can query across animal models, commercially available compounds, and existing research using natural language"
    ],
    "coreInsight": "Remove human intuition as a bottleneck by running experiments at scales no human team could achieve. Let the data reveal biology that human hypotheses would miss. The goal is a 'self-driving lab.'",
    "keyMetrics": "By leveraging data, automation, and virtual modelling, Recursion develops a lead molecule with 10x the efficiency of traditional methods, in half the time and at a fraction of the cost. Vision: Building toward a 'virtual cell'—and eventually a virtual organ and virtual patient.",
    "sources": ["BioPharma Dive", "Fortune", "NIH Seed", "Recursion Press"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 10: Create pg-chatpg.json**

Create `app/src/library/cases/pg-chatpg.json`:
```json
{
  "id": "pg-chatpg",
  "company": "Procter & Gamble",
  "title": "Large-Scale Field Experiments",
  "summary": "Rejected small pilots, deployed ChatPG to thousands immediately, 8,000 requests in first two hours",
  "diagramTemplate": "broad-deployment",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["rapid-iteration-cycles", "mandatory-proficiency"],
  "content": {
    "whatItIs": "Rather than a traditional 'innovation lab,' P&G's approach was to build an internal AI tool and immediately deploy it to thousands of users, treating the entire company as the experimental platform.",
    "howItWorks": [
      "Built ChatPG (internal generative AI tool) and rejected 'small pilot then scale' approach",
      "Decision: test with thousands of people immediately to get it in use quickly",
      "'In the first two hours when they launched at P&G, they received 8,000 requests'",
      "Company-wide launch followed within 2-3 months",
      "Partnership with Harvard Business School's Digital Data Design Institute for rigorous academic validation",
      "Field experiment with 776 professionals: 'Individuals using chatPG achieved the same performance level as teams that did not use the AI tool, while teams that partnered with chatPG consistently produced the best outcomes'"
    ],
    "coreInsight": "For enterprise AI adoption, skip small pilots. Deploy broadly, measure rigorously with academic partners, and iterate fast based on real usage data rather than theoretical concerns.",
    "keyMetrics": "30,000+ users, mandatory 10-minute training and acceptable use policy, 35+ use cases with internal data integration. Three deployed products: ChatPG, ImagePG, AskPG. Platform enables switching between AI models 'as deemed necessary from a business perspective'—avoiding vendor lock-in.",
    "sources": ["CIO Dive", "MIT Sloan Management Review", "P&G Signal"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 11: Create moderna.json**

Create `app/src/library/cases/moderna.json`:
```json
{
  "id": "moderna",
  "company": "Moderna",
  "title": "Mandatory Proficiency with AI Academy",
  "summary": "100% AI proficiency goal in 6 months, AI Academy as innovation incubator, 80%+ mChat adoption",
  "diagramTemplate": "embedded-universal",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["mandatory-proficiency", "a-team-capability"],
  "content": {
    "whatItIs": "An approach where the 'lab' is essentially the entire organization—with a goal of 100% AI proficiency across all employees within 6 months, supported by a structured AI Academy.",
    "howItWorks": [
      "Goal: 'achieve 100% adoption and proficiency of generative AI by all its people with access to digital solutions in six months'",
      "Three-layer change management: Individual (in-depth research, listening programs, trainings), Collective (AI prompt contest identified top 100 AI power users who became 'Generative AI Champions'), Structural (AI Academy evolved from educational content to 'an innovation incubator for AI capability, projects and ideas')",
      "mChat (internal chatbot on OpenAI's API) adopted by over 80% of employees",
      "Since deploying ChatGPT Enterprise: 750+ custom GPTs across the company"
    ],
    "coreInsight": "Set aggressive, time-bound AI proficiency targets (100% in 6 months). Structure the transformation with individual, collective, and institutional change management. Create internal 'AI Champions' from your best users. Make AI proficiency a company-wide competency, not a technical specialty.",
    "keyMetrics": "Domain fit: 'The informational nature of mRNA lends itself well to drug design simulation and optimization.'",
    "sources": ["OpenAI", "Inc Magazine", "IBM Case Study", "Moderna Press"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 12: Create shopify.json**

Create `app/src/library/cases/shopify.json`:
```json
{
  "id": "shopify",
  "company": "Shopify",
  "title": "AI as Embedded Expectation",
  "summary": "Must prove AI can't do it before requesting headcount, AI usage affects performance reviews",
  "diagramTemplate": "embedded-universal",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["mandatory-proficiency", "ride-the-exponential"],
  "content": {
    "whatItIs": "Rather than a separate lab, Shopify embedded AI capability expectations into every role—making AI proficiency a condition of employment and resource allocation.",
    "howItWorks": [
      "CEO Tobi Lutke mandate (April 2025): employees must 'show jobs can't be done by artificial intelligence before asking for more headcount and resources'",
      "AI usage now 'a baseline expectation' that influences performance reviews",
      "Lutke expects employees to use AI as 'a thought partner, deep researcher, critic, tutor, or pair programmer'",
      "Developers have access to Copilot, Cursor, and Claude Code 'all pre-tooled and ready to go'",
      "AI integration formally part of monthly business reviews and product development cycles"
    ],
    "coreInsight": "Make AI proficiency a condition of employment and resource allocation. When requesting headcount, the burden of proof shifts to demonstrating why AI can't do the job.",
    "keyMetrics": "Products: Shopify Magic and Sidekick externalize this philosophy. 'RenAIssance edition' (Winter 2025) contained 150+ AI-focused product updates. Headcount dropped from 8,300 to 8,100 over the past year.",
    "sources": ["CNBC", "Business Today", "Shopify Blog", "X/Twitter"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 13: Create nvidia.json**

Create `app/src/library/cases/nvidia.json`:
```json
{
  "id": "nvidia",
  "company": "NVIDIA",
  "title": "Information Symmetry as Lab",
  "summary": "60 direct reports, no 1:1s, daily Top 5 emails, public reasoning in group settings",
  "diagramTemplate": "embedded-universal",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["information-symmetry", "governance-lets-it-cook"],
  "content": {
    "whatItIs": "A model where the 'lab' is essentially the entire company operating with complete information transparency—no separate innovation function because innovation is expected everywhere.",
    "howItWorks": [
      "CEO Jensen Huang manages 60 direct reports with no one-on-one meetings",
      "'All NVIDIA execs should be able to learn from the feedback he provides to any one of them'",
      "Instead of private meetings, Huang prefers mass gatherings where he reasons through decisions aloud",
      "Every morning, Huang reads about 100 'Top Five Things' emails from employees across the company—summaries of what each person wants leadership to know",
      "Uses these to 'stochastically sample the system' and sense whether the company is moving in the right direction",
      "No long-term or short-term plans: 'the company adopts a flexible approach, constantly re-evaluating based on ever-evolving business conditions'"
    ],
    "coreInsight": "'The mission as the boss'—prioritizing customer needs and technological breakthroughs over internal politics or predetermined roadmaps. Innovation doesn't need a separate container if everyone has complete context.",
    "keyMetrics": "Huang says he is 'allergic to hierarchy and corporate silos.'",
    "sources": ["Fortune", "CNBC", "Tom's Hardware", "Dwarkesh Podcast"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 14: Create sanofi.json**

Create `app/src/library/cases/sanofi.json`:
```json
{
  "id": "sanofi",
  "company": "Sanofi",
  "title": "AI Research Factory",
  "summary": "Centralized AI Research Factory with CodonBERT and proprietary drug discovery models",
  "diagramTemplate": "centralized-lab",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["domain-expertise", "a-team-capability"],
  "content": {
    "whatItIs": "A centralized 'AI Research Factory' model with dedicated AI scientists working on internal tools and models specific to drug discovery.",
    "howItWorks": [
      "Developed CodonBERT and other proprietary models for drug discovery",
      "7 drug targets identified through AI approaches",
      "plai platform for internal AI deployment",
      "Centralized capability that serves therapeutic areas"
    ],
    "coreInsight": "Centralized AI capability allows deep specialization in domain-specific models (like CodonBERT for genetic sequences) while serving multiple therapeutic areas.",
    "keyMetrics": "7 AI-identified drug targets in development pipeline",
    "sources": ["Sanofi press releases", "BioPharma industry coverage"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 15: Create roche-genentech.json**

Create `app/src/library/cases/roche-genentech.json`:
```json
{
  "id": "roche-genentech",
  "company": "Roche / Genentech",
  "title": "Lab in a Loop",
  "summary": "gRED Computational Sciences with tight in silico to wet lab validation cycles, $12B commitment",
  "diagramTemplate": "tight-loop",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["rapid-iteration-cycles", "domain-expertise", "data-flywheel"],
  "content": {
    "whatItIs": "Roche's gRED Computational Sciences group with 'Lab in a Loop' concept—integrating computational prediction with wet lab validation in tight cycles.",
    "howItWorks": [
      "Prescient Design acquisition brought AI protein design capabilities",
      "$12B commitment to computational sciences",
      "Tight integration between in silico prediction and experimental validation",
      "Each cycle improves the models"
    ],
    "coreInsight": "The tightest possible loop between computational prediction and experimental validation creates a flywheel where each experiment improves the models that generate the next experiments.",
    "keyMetrics": "$12B committed to computational sciences",
    "sources": ["Roche investor presentations", "BioPharma Dive"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

**Step 16: Verify all case JSON files are valid**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
for f in src/library/cases/*.json; do echo "Checking $f"; cat "$f" | python3 -m json.tool > /dev/null && echo "Valid"; done
```

Expected: All 15 files report "Valid"

**Step 17: Commit**

```bash
git add app/src/library/cases/
git commit -m "feat: add 15 case study JSON files with full content"
```

---

### Task 5: Create Design Principle JSON Files

**Files:**
- Create: `app/src/library/designPrinciples/protect-deviations.json`
- Create: `app/src/library/designPrinciples/reward-fast-failure.json`
- Create: `app/src/library/designPrinciples/ride-the-exponential.json`
- Create: `app/src/library/designPrinciples/internal-first-validation.json`
- Create: `app/src/library/designPrinciples/exit-paths-entrepreneurs.json`
- Create: `app/src/library/designPrinciples/data-flywheel.json`
- Create: `app/src/library/designPrinciples/consumer-grade-ux.json`
- Create: `app/src/library/designPrinciples/rapid-iteration-cycles.json`
- Create: `app/src/library/designPrinciples/mandatory-proficiency.json`
- Create: `app/src/library/designPrinciples/domain-expertise.json`
- Create: `app/src/library/designPrinciples/remove-human-intuition-bottlenecks.json`
- Create: `app/src/library/designPrinciples/information-symmetry.json`
- Create: `app/src/library/designPrinciples/protected-exploration-time.json`
- Create: `app/src/library/designPrinciples/ring-fence-budget.json`
- Create: `app/src/library/designPrinciples/governance-lets-it-cook.json`
- Create: `app/src/library/designPrinciples/a-team-capability.json`
- Create: `app/src/library/designPrinciples/lab-to-operations-handoff.json`
- Create: `app/src/library/designPrinciples/ceo-as-political-shield.json`

**Step 1: Create protect-deviations.json**

Create `app/src/library/designPrinciples/protect-deviations.json`:
```json
{
  "id": "protect-deviations",
  "title": "Protect Deviations from Optimization Pressure",
  "group": "protection",
  "architecturalPrinciples": ["locus-of-innovation", "ambidexterity-structure"],
  "insight": "Middle management systematically kills off-strategy work because their job is to optimize current operations. Breakthrough innovation requires structural protection from this pressure.",
  "manifestations": [
    "Separate organizational units with different reporting lines (Eli Lilly hubs, Google X)",
    "Ring-fenced budgets that require board approval to reallocate",
    "Leaders who explicitly defend 'unproductive' work",
    "Physical separation (different buildings, different cities)",
    "Different time horizons (annual reviews vs. quarterly)"
  ],
  "test": "When the core business is under pressure, what happens to exploration resources? If they get raided, protection is insufficient.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 2: Create reward-fast-failure.json**

Create `app/src/library/designPrinciples/reward-fast-failure.json`:
```json
{
  "id": "reward-fast-failure",
  "title": "Reward Fast Failure Explicitly",
  "group": "incentives",
  "architecturalPrinciples": ["locus-of-innovation", "measurement-philosophy"],
  "insight": "Most organizations implicitly punish failure even when they say they value experimentation. Explicit rewards for killing projects early (bonuses, promotions, public celebration) are required to overcome this.",
  "manifestations": [
    "Google X: 'We have bonused every single person on teams that end their projects'",
    "Pre-mortems before starting (predict why this will fail)",
    "'Run at the hardest parts first' methodology",
    "Public celebration of killed projects, not just successes",
    "Promotion criteria that include 'projects responsibly ended'"
  ],
  "test": "Can you name the last project that was killed early and what happened to the people who killed it? If they were penalized or sidelined, the incentives are wrong.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 3: Create ride-the-exponential.json**

Create `app/src/library/designPrinciples/ride-the-exponential.json`:
```json
{
  "id": "ride-the-exponential",
  "title": "Ride the Exponential (Build for Future Capabilities)",
  "group": "speed",
  "architecturalPrinciples": ["locus-of-innovation", "stance-on-uncertainty"],
  "insight": "If you build for what AI can reliably do today, you'll be behind when capabilities improve (which happens fast). Build for what's barely possible, accept breakage, and be ready when capabilities arrive. Design products that naturally get better as models improve—and delete scaffolding over time rather than adding to it.",
  "manifestations": [
    "Anthropic product principle: 'ride the exponential'—products must 'meet the moment' but 'naturally improve' as models get better",
    "Deleting harness code over time rather than adding to it because the model can do more",
    "Companies that 'pushed the limits with earlier models, hit walls, and then were ready when new capabilities emerged' are the ones succeeding (Cursor, Lovable)",
    "Designing for 10x capability improvement in 18 months",
    "Accepting that current implementations will break"
  ],
  "test": "Is your AI roadmap based on current model capabilities or anticipated capabilities? Are you deleting scaffolding over time or adding more? If you're only building for what works reliably today, you're too conservative.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 4: Create internal-first-validation.json**

Create `app/src/library/designPrinciples/internal-first-validation.json`:
```json
{
  "id": "internal-first-validation",
  "title": "Internal-First Validation Before External Release",
  "group": "lab-to-org",
  "architecturalPrinciples": ["locus-of-innovation"],
  "insight": "The best filter for whether an innovation is real is whether your own organization adopts it. Internal usage surfaces problems, discovers unexpected applications, and builds conviction before external release.",
  "manifestations": [
    "Anthropic: Labs builds tools, internal adoption validates (Claude CLI overtook other tools in 3 months), then external release",
    "Hackathons as discovery mechanism—internal teams find use cases the builders didn't anticipate",
    "'Dogfooding' as serious innovation filter, not just quality check",
    "Time between internal success and external release used to 'button it up and put on a fancy suit'"
  ],
  "test": "How long do you use your own innovations before releasing them? If internal teams aren't fighting over access, it might not be ready.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 5: Create exit-paths-entrepreneurs.json**

Create `app/src/library/designPrinciples/exit-paths-entrepreneurs.json`:
```json
{
  "id": "exit-paths-entrepreneurs",
  "title": "Create Exit Paths for Entrepreneurial Energy",
  "group": "resources",
  "architecturalPrinciples": ["locus-of-innovation"],
  "insight": "The most entrepreneurial people will leave if they feel trapped. Creating legitimate paths to 'exit' (spinoffs, internal ventures, equity participation) keeps them inside the system.",
  "manifestations": [
    "Samsung C-Lab: 20% of projects become independent companies",
    "Corporate venture structures with equity participation",
    "Clear criteria for when a project 'graduates' out of the lab",
    "Alumni networks that maintain connection even after spinoff"
  ],
  "test": "Do your most entrepreneurial people see a path to meaningful upside? If the only way to get startup-like returns is to leave, they will.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 6: Create data-flywheel.json**

Create `app/src/library/designPrinciples/data-flywheel.json`:
```json
{
  "id": "data-flywheel",
  "title": "Use Deployed Products as Data Flywheel",
  "group": "lab-to-org",
  "architecturalPrinciples": ["locus-of-innovation", "information-architecture"],
  "insight": "Products in the field generate data that improves AI capabilities that improve products. This flywheel is a durable competitive advantage.",
  "manifestations": [
    "Tesla: 1.5 million cars generating training data continuously",
    "Duolingo: 1.25 billion daily exercises training personalization algorithms",
    "Any product where usage improves the underlying AI"
  ],
  "test": "Is your AI getting better as a direct result of customer usage? If not, you're not building a flywheel.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 7: Create consumer-grade-ux.json**

Create `app/src/library/designPrinciples/consumer-grade-ux.json`:
```json
{
  "id": "consumer-grade-ux",
  "title": "Consumer-Grade UX Drives Enterprise Adoption",
  "group": "lab-to-org",
  "architecturalPrinciples": ["locus-of-innovation"],
  "insight": "Enterprise tools don't have to feel like enterprise tools. Consumer-grade UX dramatically increases adoption, and adoption is where value comes from.",
  "manifestations": [
    "Bank of America: extending consumer Erica to employees, achieving 90%+ adoption",
    "'Erica for Everyone' philosophy",
    "Measuring adoption like a consumer product (DAU, retention, NPS)"
  ],
  "test": "Would your employees choose to use your internal AI tools if they weren't required? If not, the UX isn't good enough.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 8: Create rapid-iteration-cycles.json**

Create `app/src/library/designPrinciples/rapid-iteration-cycles.json`:
```json
{
  "id": "rapid-iteration-cycles",
  "title": "Rapid Iteration Cycles Over Perfect Launches",
  "group": "speed",
  "architecturalPrinciples": ["locus-of-innovation", "measurement-philosophy"],
  "insight": "In fast-moving domains, speed of learning beats quality of initial launch. 8-week cycles mean you're never far from course correction.",
  "manifestations": [
    "JPMorgan: 8-week update cycles for LLM Suite",
    "DNP: 90% of use cases showing results in 90 days",
    "Continuous deployment over big-bang releases"
  ],
  "test": "How long between identifying a problem and deploying a fix? If it's months, you're too slow.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 9: Create mandatory-proficiency.json**

Create `app/src/library/designPrinciples/mandatory-proficiency.json`:
```json
{
  "id": "mandatory-proficiency",
  "title": "Mandatory Proficiency Creates Universal Capability",
  "group": "culture",
  "architecturalPrinciples": ["locus-of-innovation", "human-ai-boundaries"],
  "insight": "Optional AI adoption creates a bimodal distribution (power users and non-users). Mandatory proficiency with support structures creates universal capability.",
  "manifestations": [
    "Moderna: 100% AI proficiency goal within 6 months",
    "Shopify: 'prove AI can't do it before requesting headcount'",
    "AI proficiency in performance reviews",
    "Structured AI Champions/advocate programs"
  ],
  "test": "What percentage of employees use AI tools weekly? If it's under 50%, adoption is optional in practice regardless of what policy says.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 10: Create domain-expertise.json**

Create `app/src/library/designPrinciples/domain-expertise.json`:
```json
{
  "id": "domain-expertise",
  "title": "Domain Expertise is the Differentiator",
  "group": "resources",
  "architecturalPrinciples": ["locus-of-innovation"],
  "insight": "General AI capabilities are increasingly commoditized. Domain expertise in applying AI to specific contexts is the source of differentiation.",
  "manifestations": [
    "McKinsey acquiring QuantumBlack (F1 racing expertise)",
    "Eli Lilly's 18-year GLP-1 journey (protein engineering expertise)",
    "Recursion's 300M+ experiments (biology-specific automation expertise)"
  ],
  "test": "What do you know about applying AI to your domain that a general AI consultancy doesn't? If nothing, you're not building durable advantage.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 11: Create remove-human-intuition-bottlenecks.json**

Create `app/src/library/designPrinciples/remove-human-intuition-bottlenecks.json`:
```json
{
  "id": "remove-human-intuition-bottlenecks",
  "title": "Remove Human Intuition Bottlenecks at Scale",
  "group": "resources",
  "architecturalPrinciples": ["locus-of-innovation", "human-ai-boundaries"],
  "insight": "In some domains, human intuition about what to try is the bottleneck. Hypothesis-free exploration at massive scale finds what humans would miss.",
  "manifestations": [
    "Recursion: 2.2M experiments/week, hypothesis-agnostic discovery",
    "Letting data reveal patterns rather than testing human hunches",
    "'The company's platform is capable of finding novel biology that may have been overlooked by humans'"
  ],
  "test": "Are your most valuable discoveries ones that humans predicted, or ones that surprised them? If everything was predicted, you might not be exploring broadly enough.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 12: Create information-symmetry.json**

Create `app/src/library/designPrinciples/information-symmetry.json`:
```json
{
  "id": "information-symmetry",
  "title": "Information Symmetry Enables Distributed Innovation",
  "group": "lab-to-org",
  "architecturalPrinciples": ["locus-of-innovation", "information-architecture"],
  "insight": "When everyone has complete context, you don't need a separate innovation function—innovation can happen anywhere. Hierarchy creates information asymmetry that kills distributed innovation.",
  "manifestations": [
    "NVIDIA: 60 direct reports, no 1:1s, public reasoning",
    "Daily 'Top 5' emails from across the company",
    "Decisions made in group settings with full context"
  ],
  "test": "Does a frontline employee have the context to recognize and act on an innovation opportunity? If not, innovation is bottlenecked at the top.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 13: Create protected-exploration-time.json**

Create `app/src/library/designPrinciples/protected-exploration-time.json`:
```json
{
  "id": "protected-exploration-time",
  "title": "Protected Exploration Time (Not Unprotected 20% Time)",
  "group": "protection",
  "architecturalPrinciples": ["locus-of-innovation", "ambidexterity-structure"],
  "insight": "Unprotected '20% time' fails because operational demands always win when there's no structural protection. But full separation isn't the only answer—what matters is that exploration time is protected, not that it's 100%.",
  "manifestations": [
    "Full separation (Samsung C-Lab, Google X): 100% dedicated for extended periods",
    "Dedicated core + rotating contributors: Small full-time nucleus with operational people doing tours of duty",
    "Time-boxed sprints (tiger teams): Pull people out fully for 6-8 weeks",
    "Protected time blocks with structural commitment: 'Fridays are lab days' with executive enforcement"
  ],
  "test": "When was the last time exploration time survived contact with an operational crisis? If it always gets sacrificed, protection is insufficient.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 14: Create ring-fence-budget.json**

Create `app/src/library/designPrinciples/ring-fence-budget.json`:
```json
{
  "id": "ring-fence-budget",
  "title": "Ring-Fence the Budget (Board-Level Protection)",
  "group": "protection",
  "architecturalPrinciples": ["locus-of-innovation", "resource-allocation"],
  "insight": "Lab budgets get raided when the core business is under pressure—unless they're structurally protected. The protection needs to be at a level above the people who feel quarterly pressure.",
  "manifestations": [
    "Ring-fenced budgets that require board vote (not just CEO discretion) to reallocate",
    "Google X: Survives because Alphabet structure protects it from Google's P&L pressure",
    "Eli Lilly: CEO explicitly defends 'unproductive' R&D from middle management optimization",
    "Percentage of revenue automatically allocated (like R&D commitments)"
  ],
  "test": "When your core business had its last bad quarter, what happened to exploration budgets? If they got cut, protection is insufficient.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 15: Create governance-lets-it-cook.json**

Create `app/src/library/designPrinciples/governance-lets-it-cook.json`:
```json
{
  "id": "governance-lets-it-cook",
  "title": "Governance That Lets It Cook (Without Spinning Wheels)",
  "group": "incentives",
  "architecturalPrinciples": ["locus-of-innovation", "measurement-philosophy"],
  "insight": "Too much oversight kills exploration; too little enables drift and waste. The governance model must create accountability for learning and progress without demanding premature proof of ROI.",
  "manifestations": [
    "Google X: 'Pre-mortems' before projects start, then 'run at the hardest parts first'—governance focused on quality of exploration, not results",
    "JPMorgan: 8-week cycles create natural rhythm for review without micromanagement",
    "Samsung C-Lab: Employees vote on ideas, experts review finalists—peer governance, not executive oversight"
  ],
  "test": "Can a lab team explain what they learned last quarter without being asked what they shipped? Is 'we learned this won't work and killed it' a successful outcome in your governance model?",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 16: Create a-team-capability.json**

Create `app/src/library/designPrinciples/a-team-capability.json`:
```json
{
  "id": "a-team-capability",
  "title": "A-Team Capability (However You Get It)",
  "group": "resources",
  "architecturalPrinciples": ["locus-of-innovation"],
  "insight": "Labs staffed with 'whoever is available' produce mediocre results. You need A-team capability in the lab—but there are multiple ways to get it beyond pulling your best operational people.",
  "manifestations": [
    "Pull and backfill (premium model): Move top performers to the lab, explicitly hire replacements",
    "Hire externally for the lab: Recruit specifically for exploration, pair with internal 'translators'",
    "Lab as talent magnet: Use the lab to attract people you couldn't otherwise recruit",
    "Rotation with return path: Operational people do 6-12 month lab rotations with guaranteed return"
  ],
  "test": "Would your lab team be competitive in the external talent market for their roles? If not, you don't have A-team capability—you have who was available.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 17: Create lab-to-operations-handoff.json**

Create `app/src/library/designPrinciples/lab-to-operations-handoff.json`:
```json
{
  "id": "lab-to-operations-handoff",
  "title": "Design the Lab-to-Operations Handoff (Or It Dies in Translation)",
  "group": "lab-to-org",
  "architecturalPrinciples": ["locus-of-innovation", "ambidexterity-structure"],
  "insight": "Discoveries that stay in the lab create no value. But the handoff to operations is where most innovations die—either rejected by 'not invented here' or mangled in translation. The handoff mechanism must be designed, not assumed.",
  "manifestations": [
    "Anthropic: Internal adoption validates before external release—the organization is the first customer",
    "Google X: 2% graduation rate, but graduates (Waymo, Wing) get 44% of budget—massive investment in successful handoffs",
    "JPMorgan: ML Center of Excellence deploys to 250,000 employees with 8-week cycles—tight feedback loop",
    "Bank of America: Extended consumer product (Erica) to employees—familiar interface eases adoption"
  ],
  "test": "Can you trace the last three lab innovations to actual operational deployment? If they're still 'in pilot' or 'being evaluated,' your handoff is broken.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 18: Create ceo-as-political-shield.json**

Create `app/src/library/designPrinciples/ceo-as-political-shield.json`:
```json
{
  "id": "ceo-as-political-shield",
  "title": "CEO as Political Shield (Not Just Sponsor)",
  "group": "protection",
  "architecturalPrinciples": ["locus-of-innovation"],
  "insight": "Labs attract organizational antibodies—resentment from those who lost talent, skepticism from those who want ROI, competition from those who want the resources. The CEO must actively defend the lab, not just approve it.",
  "manifestations": [
    "Eli Lilly CEO Dave Ricks explicitly defends deviations: 'All the studies on middle management find they tend to squash deviations'",
    "NVIDIA: Jensen Huang's 'mission as the boss' philosophy protects unconventional approaches",
    "CEO publicly credits lab for value (even when attribution is ambiguous)",
    "CEO intervenes when operational leaders try to raid lab talent"
  ],
  "test": "When was the last time the CEO publicly defended the lab against internal criticism? If you can't remember, the lab is politically exposed.",
  "conversations": [],
  "extendedContent": {}
}
```

**Step 19: Verify all design principle JSON files are valid**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
for f in src/library/designPrinciples/*.json; do echo "Checking $f"; cat "$f" | python3 -m json.tool > /dev/null && echo "Valid"; done
```

Expected: All 18 files report "Valid"

**Step 20: Commit**

```bash
git add app/src/library/designPrinciples/
git commit -m "feat: add 18 design principle JSON files with full content"
```

---

### Task 6: Create Library Loader Hook

**Files:**
- Create: `app/src/hooks/useLibrary.ts`
- Create: `app/src/hooks/index.ts`

**Step 1: Write the useLibrary hook**

Create `app/src/hooks/useLibrary.ts`:
```typescript
import { useMemo } from 'react';
import type { Library, Case, DesignPrinciple, Layer, ArchitecturalPrinciple, PrincipleGroup, DiagramTemplate } from '../types';

// Import framework data
import layersData from '../library/framework/layers.json';
import architecturalPrinciplesData from '../library/framework/architecturalPrinciples.json';
import principleGroupsData from '../library/framework/principleGroups.json';
import diagramTemplatesData from '../library/framework/diagramTemplates.json';

// Import cases
import eliLilly from '../library/cases/eli-lilly.json';
import googleX from '../library/cases/google-x.json';
import anthropic from '../library/cases/anthropic.json';
import samsungCLab from '../library/cases/samsung-c-lab.json';
import tesla from '../library/cases/tesla.json';
import bankOfAmerica from '../library/cases/bank-of-america.json';
import jpmorgan from '../library/cases/jpmorgan.json';
import mckinseyQuantumblack from '../library/cases/mckinsey-quantumblack.json';
import recursion from '../library/cases/recursion.json';
import pgChatpg from '../library/cases/pg-chatpg.json';
import moderna from '../library/cases/moderna.json';
import shopify from '../library/cases/shopify.json';
import nvidia from '../library/cases/nvidia.json';
import sanofi from '../library/cases/sanofi.json';
import rocheGenentech from '../library/cases/roche-genentech.json';

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

const cases: Case[] = [
  eliLilly,
  googleX,
  anthropic,
  samsungCLab,
  tesla,
  bankOfAmerica,
  jpmorgan,
  mckinseyQuantumblack,
  recursion,
  pgChatpg,
  moderna,
  shopify,
  nvidia,
  sanofi,
  rocheGenentech,
] as Case[];

const designPrinciples: DesignPrinciple[] = [
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
] as DesignPrinciple[];

export interface UseLibraryReturn {
  library: Library;
  getCase: (id: string) => Case | undefined;
  getDesignPrinciple: (id: string) => DesignPrinciple | undefined;
  getLayer: (id: string) => Layer | undefined;
  getArchitecturalPrinciple: (id: string) => ArchitecturalPrinciple | undefined;
  getPrincipleGroup: (id: string) => PrincipleGroup | undefined;
  getDiagramTemplate: (id: string) => DiagramTemplate | undefined;
  getCasesForPrinciple: (principleId: string) => Case[];
  getDesignPrinciplesForCase: (caseId: string) => DesignPrinciple[];
  getCasesForDesignPrinciple: (designPrincipleId: string) => Case[];
}

export function useLibrary(): UseLibraryReturn {
  const library: Library = useMemo(() => ({
    layers: layersData as Layer[],
    architecturalPrinciples: architecturalPrinciplesData as ArchitecturalPrinciple[],
    diagramTemplates: diagramTemplatesData as DiagramTemplate[],
    principleGroups: principleGroupsData as PrincipleGroup[],
    tensions: [], // Will be populated later
    cases,
    designPrinciples,
  }), []);

  const getCase = (id: string) => library.cases.find(c => c.id === id);

  const getDesignPrinciple = (id: string) => library.designPrinciples.find(p => p.id === id);

  const getLayer = (id: string) => library.layers.find(l => l.id === id);

  const getArchitecturalPrinciple = (id: string) => library.architecturalPrinciples.find(p => p.id === id);

  const getPrincipleGroup = (id: string) => library.principleGroups.find(g => g.id === id);

  const getDiagramTemplate = (id: string) => library.diagramTemplates.find(t => t.id === id);

  // Get all cases that relate to an architectural principle
  const getCasesForPrinciple = (principleId: string) =>
    library.cases.filter(c => c.architecturalPrinciples.includes(principleId));

  // Get design principles for a case
  const getDesignPrinciplesForCase = (caseId: string) => {
    const caseData = getCase(caseId);
    if (!caseData) return [];
    return caseData.designPrinciples
      .map(id => getDesignPrinciple(id))
      .filter((p): p is DesignPrinciple => p !== undefined);
  };

  // Get cases that exemplify a design principle (reverse lookup)
  const getCasesForDesignPrinciple = (designPrincipleId: string) =>
    library.cases.filter(c => c.designPrinciples.includes(designPrincipleId));

  return {
    library,
    getCase,
    getDesignPrinciple,
    getLayer,
    getArchitecturalPrinciple,
    getPrincipleGroup,
    getDiagramTemplate,
    getCasesForPrinciple,
    getDesignPrinciplesForCase,
    getCasesForDesignPrinciple,
  };
}
```

**Step 2: Create hooks index**

Create `app/src/hooks/index.ts`:
```typescript
export { useLibrary } from './useLibrary';
export type { UseLibraryReturn } from './useLibrary';
```

**Step 3: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 4: Commit**

```bash
git add app/src/hooks/
git commit -m "feat: add useLibrary hook for loading and querying library data"
```

---

### Task 7: Create User State Hook with localStorage Persistence

**Files:**
- Create: `app/src/hooks/useUserState.ts`
- Modify: `app/src/hooks/index.ts`

**Step 1: Write the useUserState hook**

Create `app/src/hooks/useUserState.ts`:
```typescript
import { useState, useEffect, useCallback } from 'react';
import type { UserState, PrincipleState, PrincipleStatus } from '../types';
import { createEmptyPrincipleState } from '../types';

const STORAGE_KEY = 'ai-transformation-user-state';

export interface UseUserStateReturn {
  state: UserState;
  getPrincipleState: (principleId: string) => PrincipleState;
  updatePrincipleState: (principleId: string, updates: Partial<PrincipleState>) => void;
  toggleStarredCase: (principleId: string, caseId: string) => void;
  toggleStarredPrinciple: (principleId: string, designPrincipleId: string) => void;
  setNotes: (principleId: string, notes: string) => void;
  setDraftStance: (principleId: string, draft: string) => void;
  crystallizeStance: (principleId: string, stance: string) => void;
  setStatus: (principleId: string, status: PrincipleStatus) => void;
  resetPrinciple: (principleId: string) => void;
  resetAll: () => void;
}

function loadFromStorage(): UserState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    console.error('Failed to load user state from localStorage:', e);
  }
  return {};
}

function saveToStorage(state: UserState): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save user state to localStorage:', e);
  }
}

export function useUserState(): UseUserStateReturn {
  const [state, setState] = useState<UserState>(loadFromStorage);

  // Persist to localStorage whenever state changes
  useEffect(() => {
    saveToStorage(state);
  }, [state]);

  const getPrincipleState = useCallback((principleId: string): PrincipleState => {
    return state[principleId] || createEmptyPrincipleState();
  }, [state]);

  const updatePrincipleState = useCallback((principleId: string, updates: Partial<PrincipleState>) => {
    setState(prev => ({
      ...prev,
      [principleId]: {
        ...createEmptyPrincipleState(),
        ...prev[principleId],
        ...updates,
        lastModified: new Date().toISOString(),
      },
    }));
  }, []);

  const toggleStarredCase = useCallback((principleId: string, caseId: string) => {
    setState(prev => {
      const current = prev[principleId] || createEmptyPrincipleState();
      const starredCases = current.starredCases.includes(caseId)
        ? current.starredCases.filter(id => id !== caseId)
        : [...current.starredCases, caseId];

      // Auto-update status to in-progress if unexplored
      const status = current.status === 'unexplored' ? 'in-progress' : current.status;

      return {
        ...prev,
        [principleId]: {
          ...current,
          starredCases,
          status,
          lastModified: new Date().toISOString(),
        },
      };
    });
  }, []);

  const toggleStarredPrinciple = useCallback((principleId: string, designPrincipleId: string) => {
    setState(prev => {
      const current = prev[principleId] || createEmptyPrincipleState();
      const starredPrinciples = current.starredPrinciples.includes(designPrincipleId)
        ? current.starredPrinciples.filter(id => id !== designPrincipleId)
        : [...current.starredPrinciples, designPrincipleId];

      // Auto-update status to in-progress if unexplored
      const status = current.status === 'unexplored' ? 'in-progress' : current.status;

      return {
        ...prev,
        [principleId]: {
          ...current,
          starredPrinciples,
          status,
          lastModified: new Date().toISOString(),
        },
      };
    });
  }, []);

  const setNotes = useCallback((principleId: string, notes: string) => {
    updatePrincipleState(principleId, { notes });
  }, [updatePrincipleState]);

  const setDraftStance = useCallback((principleId: string, draftStance: string) => {
    setState(prev => {
      const current = prev[principleId] || createEmptyPrincipleState();
      const status = current.status === 'unexplored' ? 'in-progress' : current.status;
      return {
        ...prev,
        [principleId]: {
          ...current,
          draftStance,
          status,
          lastModified: new Date().toISOString(),
        },
      };
    });
  }, []);

  const crystallizeStance = useCallback((principleId: string, stance: string) => {
    updatePrincipleState(principleId, {
      crystallizedStance: stance,
      status: 'stance-taken',
    });
  }, [updatePrincipleState]);

  const setStatus = useCallback((principleId: string, status: PrincipleStatus) => {
    updatePrincipleState(principleId, { status });
  }, [updatePrincipleState]);

  const resetPrinciple = useCallback((principleId: string) => {
    setState(prev => {
      const { [principleId]: _, ...rest } = prev;
      return rest;
    });
  }, []);

  const resetAll = useCallback(() => {
    setState({});
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return {
    state,
    getPrincipleState,
    updatePrincipleState,
    toggleStarredCase,
    toggleStarredPrinciple,
    setNotes,
    setDraftStance,
    crystallizeStance,
    setStatus,
    resetPrinciple,
    resetAll,
  };
}
```

**Step 2: Update hooks index**

Edit `app/src/hooks/index.ts`:
```typescript
export { useLibrary } from './useLibrary';
export type { UseLibraryReturn } from './useLibrary';
export { useUserState } from './useUserState';
export type { UseUserStateReturn } from './useUserState';
```

**Step 3: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 4: Commit**

```bash
git add app/src/hooks/
git commit -m "feat: add useUserState hook with localStorage persistence"
```

---

## Phase 2: Core UI Components

### Task 8: Create Stack View Component (Home Page)

**Files:**
- Create: `app/src/components/Stack.tsx`
- Create: `app/src/components/StackLayer.tsx`
- Create: `app/src/components/PrincipleRow.tsx`
- Create: `app/src/components/StatusBadge.tsx`

**Step 1: Create StatusBadge component**

Create `app/src/components/StatusBadge.tsx`:
```typescript
import type { PrincipleStatus } from '../types';

interface StatusBadgeProps {
  status: PrincipleStatus;
}

const statusConfig: Record<PrincipleStatus, { label: string; className: string; icon: string }> = {
  'unexplored': {
    label: 'Unexplored',
    className: 'bg-gray-100 text-gray-600',
    icon: '○',
  },
  'in-progress': {
    label: 'In Progress',
    className: 'bg-amber-100 text-amber-700',
    icon: '◐',
  },
  'stance-taken': {
    label: 'Stance Taken',
    className: 'bg-green-100 text-green-700',
    icon: '●',
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${config.className}`}>
      <span className="text-sm">{config.icon}</span>
      {config.label}
    </span>
  );
}
```

**Step 2: Create PrincipleRow component**

Create `app/src/components/PrincipleRow.tsx`:
```typescript
import type { ArchitecturalPrinciple, PrincipleStatus } from '../types';
import { StatusBadge } from './StatusBadge';

interface PrincipleRowProps {
  principle: ArchitecturalPrinciple;
  status: PrincipleStatus;
  onClick: () => void;
}

export function PrincipleRow({ principle, status, onClick }: PrincipleRowProps) {
  const isAvailable = principle.status === 'available';

  return (
    <button
      onClick={isAvailable ? onClick : undefined}
      disabled={!isAvailable}
      className={`w-full flex items-center justify-between px-4 py-3 text-left transition-colors ${
        isAvailable
          ? 'hover:bg-white/50 cursor-pointer'
          : 'cursor-not-allowed opacity-60'
      }`}
    >
      <div className="flex items-center gap-3">
        <span className="text-gray-900 font-medium">{principle.name}</span>
        {!isAvailable && (
          <span className="text-xs text-gray-400 italic">Coming Soon</span>
        )}
      </div>
      {isAvailable && <StatusBadge status={status} />}
    </button>
  );
}
```

**Step 3: Create StackLayer component**

Create `app/src/components/StackLayer.tsx`:
```typescript
import type { Layer, ArchitecturalPrinciple, PrincipleState } from '../types';
import { PrincipleRow } from './PrincipleRow';

interface StackLayerProps {
  layer: Layer;
  principles: ArchitecturalPrinciple[];
  getPrincipleState: (id: string) => PrincipleState;
  onPrincipleClick: (principleId: string) => void;
}

export function StackLayer({ layer, principles, getPrincipleState, onPrincipleClick }: StackLayerProps) {
  return (
    <div
      className="border border-gray-200 rounded-lg overflow-hidden"
      style={{ borderLeftColor: layer.color, borderLeftWidth: '4px' }}
    >
      <div
        className="px-4 py-3 font-semibold text-sm uppercase tracking-wide"
        style={{ backgroundColor: `${layer.color}15`, color: layer.color }}
      >
        {layer.name}
      </div>
      <div className="divide-y divide-gray-100 bg-white">
        {principles.map(principle => (
          <PrincipleRow
            key={principle.id}
            principle={principle}
            status={getPrincipleState(principle.id).status}
            onClick={() => onPrincipleClick(principle.id)}
          />
        ))}
      </div>
    </div>
  );
}
```

**Step 4: Create Stack component**

Create `app/src/components/Stack.tsx`:
```typescript
import { useLibrary } from '../hooks/useLibrary';
import { useUserState } from '../hooks/useUserState';
import { StackLayer } from './StackLayer';

interface StackProps {
  onPrincipleClick: (principleId: string) => void;
}

export function Stack({ onPrincipleClick }: StackProps) {
  const { library, getArchitecturalPrinciple } = useLibrary();
  const { getPrincipleState, state } = useUserState();

  // Count stances taken
  const stancesTaken = Object.values(state).filter(s => s.status === 'stance-taken').length;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          AI Transformation Architecture
        </h1>
        <p className="text-gray-600">
          Develop your organization's stance on each architectural principle. Click any principle to explore cases and design your approach.
        </p>
      </div>

      <div className="space-y-4">
        {library.layers.map(layer => {
          const principles = layer.principles
            .map(id => getArchitecturalPrinciple(id))
            .filter((p): p is NonNullable<typeof p> => p !== undefined);

          return (
            <StackLayer
              key={layer.id}
              layer={layer}
              principles={principles}
              getPrincipleState={getPrincipleState}
              onPrincipleClick={onPrincipleClick}
            />
          );
        })}
      </div>

      <div className="mt-8 flex gap-4 justify-center">
        <button
          disabled={stancesTaken < 2}
          className="px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-gray-100 text-gray-700 hover:bg-gray-200"
        >
          View Tensions
        </button>
        <button
          disabled={stancesTaken === 0}
          className="px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-indigo-600 text-white hover:bg-indigo-700"
        >
          Generate Artifact
        </button>
      </div>

      {stancesTaken < 2 && (
        <p className="text-center text-sm text-gray-500 mt-4">
          Take stances on 2+ principles to view tensions and generate artifacts
        </p>
      )}
    </div>
  );
}
```

**Step 5: Create components index**

Create `app/src/components/index.ts`:
```typescript
export { Stack } from './Stack';
export { StackLayer } from './StackLayer';
export { PrincipleRow } from './PrincipleRow';
export { StatusBadge } from './StatusBadge';
```

**Step 6: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 7: Commit**

```bash
git add app/src/components/
git commit -m "feat: add Stack view components (home page)"
```

---

### Task 9: Create Case Card Component

**Files:**
- Create: `app/src/components/CaseCard.tsx`
- Create: `app/src/components/DiagramThumbnail.tsx`

**Step 1: Create DiagramThumbnail component**

Create `app/src/components/DiagramThumbnail.tsx`:
```typescript
interface DiagramThumbnailProps {
  templateId: string;
  size?: 'sm' | 'md' | 'lg';
}

// Simple placeholder diagrams using CSS shapes
// In a real implementation, these would be SVG components
const templateShapes: Record<string, string> = {
  'centralized-lab': 'bg-gradient-to-b from-indigo-100 to-indigo-200',
  'distributed-hubs': 'bg-gradient-to-r from-purple-100 via-purple-200 to-purple-100',
  'embedded-universal': 'bg-gradient-to-br from-pink-100 to-pink-200',
  'center-of-excellence': 'bg-gradient-to-b from-blue-100 to-blue-200',
  'product-as-lab': 'bg-gradient-to-r from-green-100 to-green-200',
  'hybrid-labs-core': 'bg-gradient-to-br from-violet-100 to-violet-200',
  'tight-loop': 'bg-gradient-to-r from-cyan-100 via-cyan-200 to-cyan-100',
  'external-acquisition': 'bg-gradient-to-b from-amber-100 to-amber-200',
  'broad-deployment': 'bg-gradient-to-br from-rose-100 to-rose-200',
};

const sizeClasses = {
  sm: 'w-16 h-16',
  md: 'w-20 h-20',
  lg: 'w-32 h-32',
};

export function DiagramThumbnail({ templateId, size = 'md' }: DiagramThumbnailProps) {
  const bgClass = templateShapes[templateId] || 'bg-gray-100';

  return (
    <div
      className={`${sizeClasses[size]} ${bgClass} rounded-lg flex items-center justify-center border border-gray-200`}
    >
      <span className="text-2xl opacity-30">
        {templateId === 'centralized-lab' && '◉'}
        {templateId === 'distributed-hubs' && '◈'}
        {templateId === 'embedded-universal' && '▣'}
        {templateId === 'center-of-excellence' && '◎'}
        {templateId === 'product-as-lab' && '↻'}
        {templateId === 'hybrid-labs-core' && '⊕'}
        {templateId === 'tight-loop' && '↔'}
        {templateId === 'external-acquisition' && '⊛'}
        {templateId === 'broad-deployment' && '▤'}
      </span>
    </div>
  );
}
```

**Step 2: Create CaseCard component**

Create `app/src/components/CaseCard.tsx`:
```typescript
import { useState } from 'react';
import type { Case, DesignPrinciple } from '../types';
import { DiagramThumbnail } from './DiagramThumbnail';

interface CaseCardProps {
  caseData: Case;
  isStarred: boolean;
  onToggleStar: () => void;
  relatedPrinciples: DesignPrinciple[];
  onPrincipleClick?: (principleId: string) => void;
}

export function CaseCard({
  caseData,
  isStarred,
  onToggleStar,
  relatedPrinciples,
  onPrincipleClick
}: CaseCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      {/* Collapsed View */}
      <div
        className="p-4 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex gap-4">
          <DiagramThumbnail templateId={caseData.diagramTemplate} size="md" />
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <div>
                <h3 className="font-semibold text-gray-900">
                  {caseData.company}: {caseData.title}
                </h3>
                <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                  {caseData.summary}
                </p>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onToggleStar();
                }}
                className="flex-shrink-0 p-1 hover:bg-gray-100 rounded transition-colors"
                aria-label={isStarred ? 'Unstar case' : 'Star case'}
              >
                <span className="text-xl">{isStarred ? '★' : '☆'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Expanded View */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-4 space-y-4 bg-gray-50">
          <div className="flex gap-4">
            <DiagramThumbnail templateId={caseData.diagramTemplate} size="lg" />
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 mb-2">What it is:</h4>
              <p className="text-sm text-gray-700">{caseData.content.whatItIs}</p>
            </div>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 mb-2">How it works:</h4>
            <ul className="list-disc list-inside space-y-1">
              {caseData.content.howItWorks.map((item, i) => (
                <li key={i} className="text-sm text-gray-700">{item}</li>
              ))}
            </ul>
          </div>

          <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-3">
            <h4 className="font-medium text-indigo-900 mb-1">Core insight:</h4>
            <p className="text-sm text-indigo-800 italic">"{caseData.content.coreInsight}"</p>
          </div>

          {caseData.content.keyMetrics && (
            <div>
              <h4 className="font-medium text-gray-900 mb-1">Key metrics:</h4>
              <p className="text-sm text-gray-700">{caseData.content.keyMetrics}</p>
            </div>
          )}

          {relatedPrinciples.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Illustrates:</h4>
              <div className="flex flex-wrap gap-2">
                {relatedPrinciples.map(principle => (
                  <button
                    key={principle.id}
                    onClick={() => onPrincipleClick?.(principle.id)}
                    className="text-xs px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition-colors"
                  >
                    {principle.title}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="text-xs text-gray-500">
            <span className="font-medium">Sources:</span> {caseData.content.sources.join(', ')}
          </div>
        </div>
      )}
    </div>
  );
}
```

**Step 3: Update components index**

Edit `app/src/components/index.ts` to add:
```typescript
export { Stack } from './Stack';
export { StackLayer } from './StackLayer';
export { PrincipleRow } from './PrincipleRow';
export { StatusBadge } from './StatusBadge';
export { CaseCard } from './CaseCard';
export { DiagramThumbnail } from './DiagramThumbnail';
```

**Step 4: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 5: Commit**

```bash
git add app/src/components/
git commit -m "feat: add CaseCard and DiagramThumbnail components"
```

---

### Task 10: Create Design Principle Card Component

**Files:**
- Create: `app/src/components/DesignPrincipleCard.tsx`
- Create: `app/src/components/GroupBadge.tsx`

**Step 1: Create GroupBadge component**

Create `app/src/components/GroupBadge.tsx`:
```typescript
import { useLibrary } from '../hooks/useLibrary';

interface GroupBadgeProps {
  groupId: string;
}

export function GroupBadge({ groupId }: GroupBadgeProps) {
  const { getPrincipleGroup } = useLibrary();
  const group = getPrincipleGroup(groupId);

  if (!group) return null;

  return (
    <span
      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium uppercase tracking-wide"
      style={{
        backgroundColor: `${group.color}20`,
        color: group.color
      }}
    >
      {group.name}
    </span>
  );
}
```

**Step 2: Create DesignPrincipleCard component**

Create `app/src/components/DesignPrincipleCard.tsx`:
```typescript
import { useState } from 'react';
import type { DesignPrinciple, Case } from '../types';
import { GroupBadge } from './GroupBadge';

interface DesignPrincipleCardProps {
  principle: DesignPrinciple;
  isStarred: boolean;
  onToggleStar: () => void;
  relatedCases: Case[];
  onCaseClick?: (caseId: string) => void;
}

export function DesignPrincipleCard({
  principle,
  isStarred,
  onToggleStar,
  relatedCases,
  onCaseClick
}: DesignPrincipleCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      {/* Collapsed View */}
      <div
        className="p-4 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <GroupBadge groupId={principle.group} />
            </div>
            <h3 className="font-semibold text-gray-900">{principle.title}</h3>
            <p className="text-sm text-gray-600 mt-1 line-clamp-2">
              {principle.insight}
            </p>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onToggleStar();
            }}
            className="flex-shrink-0 p-1 hover:bg-gray-100 rounded transition-colors"
            aria-label={isStarred ? 'Unstar principle' : 'Star principle'}
          >
            <span className="text-xl">{isStarred ? '★' : '☆'}</span>
          </button>
        </div>
      </div>

      {/* Expanded View */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-4 space-y-4 bg-gray-50">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">The insight:</h4>
            <p className="text-sm text-gray-700">{principle.insight}</p>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 mb-2">Manifestations:</h4>
            <ul className="list-disc list-inside space-y-1">
              {principle.manifestations.map((item, i) => (
                <li key={i} className="text-sm text-gray-700">{item}</li>
              ))}
            </ul>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
            <h4 className="font-medium text-amber-900 mb-1">The test:</h4>
            <p className="text-sm text-amber-800">{principle.test}</p>
          </div>

          {relatedCases.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Exemplified by:</h4>
              <div className="flex flex-wrap gap-2">
                {relatedCases.map(caseData => (
                  <button
                    key={caseData.id}
                    onClick={() => onCaseClick?.(caseData.id)}
                    className="text-xs px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition-colors"
                  >
                    {caseData.company}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

**Step 3: Update components index**

Edit `app/src/components/index.ts`:
```typescript
export { Stack } from './Stack';
export { StackLayer } from './StackLayer';
export { PrincipleRow } from './PrincipleRow';
export { StatusBadge } from './StatusBadge';
export { CaseCard } from './CaseCard';
export { DiagramThumbnail } from './DiagramThumbnail';
export { DesignPrincipleCard } from './DesignPrincipleCard';
export { GroupBadge } from './GroupBadge';
```

**Step 4: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 5: Commit**

```bash
git add app/src/components/
git commit -m "feat: add DesignPrincipleCard and GroupBadge components"
```

---

### Task 11: Create Workspace Component

**Files:**
- Create: `app/src/components/Workspace.tsx`

**Step 1: Create Workspace component**

Create `app/src/components/Workspace.tsx`:
```typescript
import { useState, useEffect } from 'react';
import type { PrincipleState, Case, DesignPrinciple } from '../types';
import { DiagramThumbnail } from './DiagramThumbnail';

interface WorkspaceProps {
  principleState: PrincipleState;
  starredCases: Case[];
  starredPrinciples: DesignPrinciple[];
  onNotesChange: (notes: string) => void;
  onDraftChange: (draft: string) => void;
  onCrystallize: () => void;
  onSaveInProgress: () => void;
}

export function Workspace({
  principleState,
  starredCases,
  starredPrinciples,
  onNotesChange,
  onDraftChange,
  onCrystallize,
  onSaveInProgress,
}: WorkspaceProps) {
  const [notes, setNotes] = useState(principleState.notes);
  const [draft, setDraft] = useState(principleState.draftStance);

  // Sync local state with props
  useEffect(() => {
    setNotes(principleState.notes);
    setDraft(principleState.draftStance);
  }, [principleState.notes, principleState.draftStance]);

  // Debounced save for notes
  useEffect(() => {
    const timer = setTimeout(() => {
      if (notes !== principleState.notes) {
        onNotesChange(notes);
      }
    }, 500);
    return () => clearTimeout(timer);
  }, [notes, onNotesChange, principleState.notes]);

  // Debounced save for draft
  useEffect(() => {
    const timer = setTimeout(() => {
      if (draft !== principleState.draftStance) {
        onDraftChange(draft);
      }
    }, 500);
    return () => clearTimeout(timer);
  }, [draft, onDraftChange, principleState.draftStance]);

  const canCrystallize = draft.trim().length > 0;

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 space-y-6">
      {/* Starred Selections */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Your Selections</h3>

        {starredCases.length === 0 && starredPrinciples.length === 0 ? (
          <p className="text-sm text-gray-500 italic">
            Star cases and design principles that resonate with your thinking
          </p>
        ) : (
          <div className="space-y-3">
            {starredCases.length > 0 && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Cases</p>
                <div className="flex flex-wrap gap-2">
                  {starredCases.map(c => (
                    <div
                      key={c.id}
                      className="flex items-center gap-2 bg-gray-50 rounded-lg px-2 py-1"
                    >
                      <DiagramThumbnail templateId={c.diagramTemplate} size="sm" />
                      <span className="text-sm font-medium">{c.company}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {starredPrinciples.length > 0 && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Principles</p>
                <div className="flex flex-wrap gap-2">
                  {starredPrinciples.map(p => (
                    <span
                      key={p.id}
                      className="text-sm bg-gray-50 rounded-lg px-3 py-1"
                    >
                      {p.title}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Notes */}
      <div>
        <label htmlFor="notes" className="block font-semibold text-gray-900 mb-2">
          Notes
        </label>
        <textarea
          id="notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Capture your thoughts as you explore..."
          className="w-full h-24 px-3 py-2 border border-gray-200 rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
      </div>

      {/* Draft Stance */}
      <div>
        <label htmlFor="draft" className="block font-semibold text-gray-900 mb-2">
          Draft Stance
        </label>
        <textarea
          id="draft"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="We believe the best ideas for AI transformation will come from..."
          className="w-full h-32 px-3 py-2 border border-gray-200 rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
      </div>

      {/* Crystallized Stance (if exists) */}
      {principleState.crystallizedStance && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-green-900 mb-2">Crystallized Stance</h4>
          <p className="text-sm text-green-800">{principleState.crystallizedStance}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3 pt-2">
        <button
          onClick={onSaveInProgress}
          className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
        >
          Save as In Progress
        </button>
        <button
          onClick={onCrystallize}
          disabled={!canCrystallize}
          className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Crystallize Stance
        </button>
      </div>
    </div>
  );
}
```

**Step 2: Update components index**

Edit `app/src/components/index.ts`:
```typescript
export { Stack } from './Stack';
export { StackLayer } from './StackLayer';
export { PrincipleRow } from './PrincipleRow';
export { StatusBadge } from './StatusBadge';
export { CaseCard } from './CaseCard';
export { DiagramThumbnail } from './DiagramThumbnail';
export { DesignPrincipleCard } from './DesignPrincipleCard';
export { GroupBadge } from './GroupBadge';
export { Workspace } from './Workspace';
```

**Step 3: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 4: Commit**

```bash
git add app/src/components/
git commit -m "feat: add Workspace component with notes, draft, and crystallize"
```

---

### Task 12: Create Principle Deep-Dive View

**Files:**
- Create: `app/src/components/PrincipleDeepDive.tsx`

**Step 1: Create PrincipleDeepDive component**

Create `app/src/components/PrincipleDeepDive.tsx`:
```typescript
import { useState } from 'react';
import { useLibrary } from '../hooks/useLibrary';
import { useUserState } from '../hooks/useUserState';
import type { ArchitecturalPrinciple } from '../types';
import { CaseCard } from './CaseCard';
import { DesignPrincipleCard } from './DesignPrincipleCard';
import { Workspace } from './Workspace';

interface PrincipleDeepDiveProps {
  principle: ArchitecturalPrinciple;
  onBack: () => void;
}

type Tab = 'cases' | 'principles';

export function PrincipleDeepDive({ principle, onBack }: PrincipleDeepDiveProps) {
  const [activeTab, setActiveTab] = useState<Tab>('cases');
  const {
    library,
    getCasesForPrinciple,
    getDesignPrinciplesForCase,
    getCasesForDesignPrinciple,
    getCase,
    getDesignPrinciple,
    getLayer,
  } = useLibrary();
  const {
    getPrincipleState,
    toggleStarredCase,
    toggleStarredPrinciple,
    setNotes,
    setDraftStance,
    crystallizeStance,
    setStatus,
  } = useUserState();

  const layer = getLayer(principle.layerId);
  const principleState = getPrincipleState(principle.id);
  const cases = getCasesForPrinciple(principle.id);

  // Get design principles that are associated with any of the cases for this principle
  const relevantDesignPrinciples = library.designPrinciples.filter(dp =>
    dp.architecturalPrinciples.includes(principle.id)
  );

  // Get starred items as full objects
  const starredCases = principleState.starredCases
    .map(id => getCase(id))
    .filter((c): c is NonNullable<typeof c> => c !== undefined);

  const starredPrinciples = principleState.starredPrinciples
    .map(id => getDesignPrinciple(id))
    .filter((p): p is NonNullable<typeof p> => p !== undefined);

  const handleCrystallize = () => {
    if (principleState.draftStance.trim()) {
      crystallizeStance(principle.id, principleState.draftStance);
    }
  };

  const handleSaveInProgress = () => {
    setStatus(principle.id, 'in-progress');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Zone A */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4 transition-colors"
        >
          <span>←</span>
          <span>Back to Stack</span>
        </button>

        <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <span
            className="font-medium uppercase tracking-wide"
            style={{ color: layer?.color }}
          >
            {layer?.name}
          </span>
          <span>›</span>
          <span className="font-medium text-gray-900">{principle.name}</span>
        </div>

        <h1 className="text-xl font-bold text-gray-900 mb-3">
          {principle.name}
        </h1>

        <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-4">
          <p className="text-sm font-medium text-indigo-900 mb-1">Core Question:</p>
          <p className="text-indigo-800">{principle.coreQuestion}</p>
        </div>

        <p className="text-sm text-gray-600 mt-3">
          <span className="font-medium">Why this is architectural:</span> {principle.whyArchitectural}
        </p>
      </div>

      {/* Main Content - Zone B (Library) + Zone C (Workspace) */}
      <div className="flex flex-col lg:flex-row">
        {/* Zone B: Library Browser */}
        <div className="flex-1 lg:w-1/2 p-6 lg:border-r border-gray-200">
          {/* Tabs */}
          <div className="flex gap-4 mb-6 border-b border-gray-200">
            <button
              onClick={() => setActiveTab('cases')}
              className={`pb-3 px-1 font-medium transition-colors ${
                activeTab === 'cases'
                  ? 'text-indigo-600 border-b-2 border-indigo-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Cases ({cases.length})
            </button>
            <button
              onClick={() => setActiveTab('principles')}
              className={`pb-3 px-1 font-medium transition-colors ${
                activeTab === 'principles'
                  ? 'text-indigo-600 border-b-2 border-indigo-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Design Principles ({relevantDesignPrinciples.length})
            </button>
          </div>

          {/* Card List */}
          <div className="space-y-4 max-h-[calc(100vh-400px)] overflow-y-auto">
            {activeTab === 'cases' && cases.map(caseData => (
              <CaseCard
                key={caseData.id}
                caseData={caseData}
                isStarred={principleState.starredCases.includes(caseData.id)}
                onToggleStar={() => toggleStarredCase(principle.id, caseData.id)}
                relatedPrinciples={getDesignPrinciplesForCase(caseData.id)}
              />
            ))}

            {activeTab === 'principles' && relevantDesignPrinciples.map(dp => (
              <DesignPrincipleCard
                key={dp.id}
                principle={dp}
                isStarred={principleState.starredPrinciples.includes(dp.id)}
                onToggleStar={() => toggleStarredPrinciple(principle.id, dp.id)}
                relatedCases={getCasesForDesignPrinciple(dp.id)}
              />
            ))}
          </div>
        </div>

        {/* Zone C: Workspace */}
        <div className="lg:w-1/2 p-6 bg-gray-100">
          <Workspace
            principleState={principleState}
            starredCases={starredCases}
            starredPrinciples={starredPrinciples}
            onNotesChange={(notes) => setNotes(principle.id, notes)}
            onDraftChange={(draft) => setDraftStance(principle.id, draft)}
            onCrystallize={handleCrystallize}
            onSaveInProgress={handleSaveInProgress}
          />
        </div>
      </div>
    </div>
  );
}
```

**Step 2: Update components index**

Edit `app/src/components/index.ts`:
```typescript
export { Stack } from './Stack';
export { StackLayer } from './StackLayer';
export { PrincipleRow } from './PrincipleRow';
export { StatusBadge } from './StatusBadge';
export { CaseCard } from './CaseCard';
export { DiagramThumbnail } from './DiagramThumbnail';
export { DesignPrincipleCard } from './DesignPrincipleCard';
export { GroupBadge } from './GroupBadge';
export { Workspace } from './Workspace';
export { PrincipleDeepDive } from './PrincipleDeepDive';
```

**Step 3: Verify types compile**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npx tsc --noEmit
```

Expected: No type errors

**Step 4: Commit**

```bash
git add app/src/components/
git commit -m "feat: add PrincipleDeepDive view with three-zone layout"
```

---

## Phase 3: App Assembly & Integration

### Task 13: Wire Up App.tsx with Navigation

**Files:**
- Modify: `app/src/App.tsx`

**Step 1: Update App.tsx**

Edit `app/src/App.tsx`:
```typescript
import { useState } from 'react';
import { Stack, PrincipleDeepDive } from './components';
import { useLibrary } from './hooks';

type View =
  | { type: 'stack' }
  | { type: 'principle'; principleId: string };

function App() {
  const [view, setView] = useState<View>({ type: 'stack' });
  const { getArchitecturalPrinciple } = useLibrary();

  const handlePrincipleClick = (principleId: string) => {
    const principle = getArchitecturalPrinciple(principleId);
    if (principle?.status === 'available') {
      setView({ type: 'principle', principleId });
    }
  };

  const handleBack = () => {
    setView({ type: 'stack' });
  };

  if (view.type === 'principle') {
    const principle = getArchitecturalPrinciple(view.principleId);
    if (!principle) {
      return <div>Principle not found</div>;
    }
    return (
      <PrincipleDeepDive
        principle={principle}
        onBack={handleBack}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <Stack onPrincipleClick={handlePrincipleClick} />
    </div>
  );
}

export default App;
```

**Step 2: Run the development server**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npm run dev
```

Expected: App runs and shows Stack view, clicking "Locus of Innovation" navigates to deep-dive

**Step 3: Verify app compiles without errors**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npm run build
```

Expected: Build completes successfully

**Step 4: Commit**

```bash
git add app/src/App.tsx
git commit -m "feat: wire up App.tsx with Stack and PrincipleDeepDive navigation"
```

---

### Task 14: Add Vite JSON Import Configuration

**Files:**
- Modify: `app/tsconfig.json`

**Step 1: Enable JSON imports in TypeScript**

Edit `app/tsconfig.json` to include:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Step 2: Verify build works**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npm run build
```

Expected: Build completes successfully

**Step 3: Commit**

```bash
git add app/tsconfig.json
git commit -m "chore: enable JSON module resolution in TypeScript config"
```

---

### Task 15: Final Integration Test

**Files:**
- No new files

**Step 1: Run the full application**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npm run dev
```

**Step 2: Manual verification checklist**

- [ ] Stack view loads with 5 layers and 8 principles
- [ ] Status badges show correctly (all should start as "Unexplored")
- [ ] Clicking "Locus of Innovation" navigates to deep-dive
- [ ] Deep-dive shows 15 case cards in Cases tab
- [ ] Deep-dive shows design principle cards in Principles tab
- [ ] Starring a case adds it to "Your Selections"
- [ ] Notes and draft stance auto-save (check localStorage)
- [ ] Crystallizing stance changes status to "Stance Taken"
- [ ] Back button returns to Stack view
- [ ] Status persists on refresh (localStorage)

**Step 3: Build production version**

Run:
```bash
cd /Users/cgart/Penn\ Dropbox/Claudine\ Gartenberg/Feedforward/playground/orgtranformation/app
npm run build
npm run preview
```

Expected: Production build runs and all features work

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat: complete MVP of AI Transformation Architecture Tool"
```

---

## Summary

This implementation plan covers:

1. **Phase 1: Project Scaffolding & Library Data Structure** (Tasks 1-7)
   - React + Vite + Tailwind setup
   - TypeScript types for library and user state
   - Framework JSON files (layers, principles, groups, templates)
   - 15 case study JSON files
   - 18 design principle JSON files
   - useLibrary and useUserState hooks

2. **Phase 2: Core UI Components** (Tasks 8-12)
   - Stack view (home page) with layers and principle rows
   - Case cards with expand/collapse and starring
   - Design principle cards with expand/collapse and starring
   - Workspace with notes, draft stance, and crystallize
   - PrincipleDeepDive view with three-zone layout

3. **Phase 3: App Assembly & Integration** (Tasks 13-15)
   - App.tsx with navigation between views
   - TypeScript configuration for JSON imports
   - Final integration testing

---

**Plan complete and saved to `docs/plans/2026-01-19-ai-transformation-tool-implementation.md`. Ready to execute with `/superpowers-execute-plan`?**
