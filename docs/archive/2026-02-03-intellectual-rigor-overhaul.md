# Intellectual Rigor Overhaul — Implementation Plan

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Raise the field guide's intellectual rigor across four workstreams: mechanism quality audit, cross-cutting insights as a first-class data object, specimen schema improvements for multi-model orgs, and theoretical grounding rooted in organizational economics.

**Architecture:** Data-first approach — all changes flow from `synthesis/*.json` data files through TypeScript types in `site/lib/types/` into data access functions in `site/lib/data/` and finally into page components. Each workstream is independent but shares the build verification step. The mechanism audit and insights creation are the highest-priority workstreams.

**Tech Stack:** JSON data files, TypeScript interfaces, Next.js 14 App Router (React Server Components), Tailwind CSS, Node.js scripts for batch operations.

---

## Workstream 1: Mechanism Quality Audit

### Task 1.1: Add maturity lifecycle to mechanism data model

**Files:**
- Modify: `site/lib/types/synthesis.ts:24-33` (ConfirmedMechanism interface)
- Modify: `site/lib/types/synthesis.ts:35-41` (CandidateMechanism interface)

**Step 1: Add maturity field to ConfirmedMechanism**

In `site/lib/types/synthesis.ts`, add the maturity type and update the interface:

```typescript
// Add BEFORE the ConfirmedMechanism interface (after AffinityProfile)
export type MechanismMaturity = "emerging" | "confirmed" | "widespread" | "deprecated";

// Add to ConfirmedMechanism interface:
export interface ConfirmedMechanism {
  id: number;
  name: string;
  definition: string;
  problemItSolves: string;
  theoreticalConnection: string;
  scholarlyAnchor?: string;          // NEW — which scholar's work + why
  maturity?: MechanismMaturity;       // NEW — lifecycle stage
  specimens: string[];
  evidence: MechanismEvidence[];
  affinityProfile?: AffinityProfile;
}
```

Also add `scholarlyAnchor` and `demotionReason` to CandidateMechanism for demoted mechanisms:

```typescript
export interface CandidateMechanism {
  name: string;
  observedIn: string[];
  hypothesis: string;
  evidenceNeeded: string;
  specimens: string[];
  demotionReason?: string;            // NEW — why it was demoted from confirmed
  previousId?: number;                // NEW — original confirmed ID before demotion
}
```

**Step 2: Commit**

```bash
git add site/lib/types/synthesis.ts
git commit -m "feat: add maturity lifecycle and scholarly anchor to mechanism types"
```

---

### Task 1.2: Demote 3 mechanisms from confirmed to candidate

**Files:**
- Modify: `synthesis/mechanisms.json`

**Step 1: Move mechanisms #2, #9, #12 from `confirmed` array to `candidates` array**

For each demoted mechanism, create a candidate entry preserving the key information:

**#2 Bonus Teams That Kill Projects → candidate**
```json
{
  "name": "Bonus Teams That Kill Projects",
  "observedIn": ["Google X moonshot factory"],
  "hypothesis": "Incentive systems that reward teams for quickly terminating failing projects enable more exploration cycles by defeating sunk cost bias.",
  "evidenceNeeded": "3+ specimens showing explicit incentive-aligned termination mechanisms. Klarna is a reversal case, not a positive example.",
  "specimens": ["google-x", "klarna"],
  "demotionReason": "Only 1 positive specimen (Google X). Klarna is tagged as reversal case. Cannot confirm a mechanism from a single exemplar.",
  "previousId": 2
}
```

**#9 Hire CAIOs from Consumer Tech → candidate**
```json
{
  "name": "Hire CAIOs from Consumer Tech",
  "observedIn": ["UK Government", "Siemens", "Meta", "Salesforce", "Tencent"],
  "hypothesis": "Importing leadership from consumer tech backgrounds brings product-oriented mental models that shape organizational structure toward exploration.",
  "evidenceNeeded": "Evidence that the hire caused structural change, not just that the hire happened. Current evidence shows hiring patterns but not structural consequences. Also, multiple counter-examples (PwC from enterprise IT, IndoStar internal promotion) contradict the 'consumer tech' frame.",
  "specimens": ["uk-government", "siemens", "meta-ai", "salesforce", "tencent", "invent-advisory", "indostar-capital", "pwc", "stagwell"],
  "demotionReason": "Hiring pattern, not structural mechanism. Evidence shows who was hired, not what structural change followed. Multiple specimens contradict the 'consumer tech' framing (PwC, IndoStar, Stagwell all came from enterprise backgrounds).",
  "previousId": 9
}
```

**#12 Business Leader as AI Chief → candidate**
```json
{
  "name": "Business Leader as AI Chief",
  "observedIn": ["Wells Fargo", "Coca-Cola", "PwC"],
  "hypothesis": "Placing business-line leaders (not technologists) atop AI functions ensures AI strategy serves business transformation rather than technology for its own sake.",
  "evidenceNeeded": "Evidence that business-background vs tech-background AI leadership produces different structural outcomes. Current evidence is thin (3 specimens) and the causal claim is speculative.",
  "specimens": ["wells-fargo", "coca-cola", "pwc"],
  "demotionReason": "Only 3 specimens with speculative causal claim. Coca-Cola evidence is particularly thin (new CDO during CEO transition — organizational reshuffling, not a mechanism). No evidence that the leader's background actually changed structure.",
  "previousId": 12
}
```

Remove these three from the `confirmed` array. Keep their IDs in a comment or note so we don't accidentally reuse them.

**Step 2: Commit**

```bash
git add synthesis/mechanisms.json
git commit -m "audit: demote mechanisms #2, #9, #12 to candidate (insufficient evidence)"
```

---

### Task 1.3: Rename mechanism #8

**Files:**
- Modify: `synthesis/mechanisms.json`

**Step 1: Rename #8 from "Log Everything When Regulators Watch" to "Turn Compliance Into Deployment Advantage"**

Update these fields on mechanism #8:

```json
{
  "id": 8,
  "name": "Turn Compliance Into Deployment Advantage",
  "definition": "Building regulatory compliance infrastructure that becomes a competitive moat — enabling AI deployment in contexts competitors cannot enter.",
  "problemItSolves": "Regulatory burden is commonly seen as a drag on AI adoption. But organizations that invest in audit trails, explainability, and compliance-by-design can deploy AI where competitors without this infrastructure cannot.",
  "theoreticalConnection": "Information economics — compliance infrastructure reduces information asymmetry between the organization and regulators, lowering the marginal cost of deploying new AI applications in regulated contexts."
}
```

**Step 2: Commit**

```bash
git add synthesis/mechanisms.json
git commit -m "audit: rename mechanism #8 to capture compliance-as-moat insight"
```

---

### Task 1.4: Split mechanism #11

**Files:**
- Modify: `synthesis/mechanisms.json`

**Step 1: Narrow #11 to the real structural mechanism (management delayering)**

Keep #11 but refocus it on the structural insight — management delayering — and move the generic headcount-reduction specimens out:

```json
{
  "id": 11,
  "name": "Flatten Management Layers to Speed AI Decisions",
  "definition": "Removing management layers because AI reduces the information-aggregation role that middle managers traditionally play. Fewer layers means faster decision-making and more autonomous teams.",
  "problemItSolves": "Management hierarchies exist partly to aggregate information upward. When AI handles information synthesis, the coordination justification for middle management weakens. Organizations that don't delayer end up with managers supervising AI-augmented workers — adding latency without value.",
  "theoreticalConnection": "Simon's information-processing view of organizations — hierarchy exists to manage bounded rationality. AI expands individual rationality, reducing the need for hierarchical information aggregation.",
  "specimens": ["microsoft", "ups", "amazon"],
  "evidence": [
    {
      "specimenId": "microsoft",
      "speaker": "Satya Nadella",
      "source": "Cheeky Pint Podcast",
      "notes": "Demands leaders act as individual contributors. Restructured exec ranks. Management delayering — elimination of coordination overhead, not just headcount."
    },
    {
      "specimenId": "ups",
      "source": "UPS case analysis",
      "notes": "-30K operational positions via AI/automation. Management delayering convergent with Microsoft pattern. Both target management layers specifically, not just operational headcount. $9B automation investment through 2028."
    },
    {
      "specimenId": "amazon",
      "quote": "It's culture.",
      "speaker": "Andy Jassy",
      "source": "CNBC",
      "notes": "CEO framed restructuring as cultural transformation — removing bureaucracy layers. 16K cuts Jan 2026 targeting coordination overhead. The structural change is the delayering, not the cost savings."
    }
  ]
}
```

Move the pure cost-cutting cases (Klarna, Citigroup, Pinterest, Dow) into a new candidate mechanism:

```json
{
  "name": "AI-Driven Headcount Reduction",
  "observedIn": ["Klarna", "Citigroup", "Pinterest", "Dow", "Salesforce"],
  "hypothesis": "Organizations use AI deployment as justification for workforce reduction. The structural question is whether this represents genuine AI-enabled restructuring or conventional cost-cutting with AI as cover.",
  "evidenceNeeded": "Evidence distinguishing genuine structural change from cost-cutting relabeled as AI transformation. Deutsche Bank has warned of 'AI redundancy washing' — using AI as cover for headcount cuts that would have happened anyway.",
  "specimens": ["klarna", "citigroup", "pinterest", "dow", "salesforce"]
}
```

**Step 2: Commit**

```bash
git add synthesis/mechanisms.json
git commit -m "audit: split #11 into delayering mechanism + headcount-reduction candidate"
```

---

### Task 1.5: Add maturity tags to all surviving confirmed mechanisms

**Files:**
- Modify: `synthesis/mechanisms.json`

**Step 1: Add maturity field to each confirmed mechanism**

| ID | Name | Maturity | Rationale |
|----|------|----------|-----------|
| 1 | Protect Off-Strategy Work | confirmed | Core mechanism, well-evidenced, not yet ubiquitous |
| 3 | Embed Product at Research Frontier | confirmed | Strong in pharma, spreading to other industries |
| 5 | Deploy to Thousands Before You Know What Works | widespread | 9 specimens, becoming table stakes at enterprise scale |
| 6 | Merge Competing AI Teams Under Single Leader | confirmed | Strong convergent evidence in big tech |
| 7 | Put Executives on the Tools | confirmed | 7 specimens but still differentiating — most execs don't do this |
| 8 | Turn Compliance Into Deployment Advantage | confirmed | Well-evidenced in regulated industries |
| 10 | Productize Internal Operational Advantages | confirmed | Clear pattern in M5c specimens |
| 11 | Flatten Management Layers to Speed AI Decisions | emerging | Real pattern but only 3 specimens focused on delayering specifically |

Add `"maturity": "<value>"` to each mechanism object in the JSON.

**Step 2: Commit**

```bash
git add synthesis/mechanisms.json
git commit -m "audit: add maturity lifecycle tags to all confirmed mechanisms"
```

---

### Task 1.6: Recompute mechanism affinity profiles

**Files:**
- Modify: `scripts/compute-mechanism-affinity.js:20-29` (update MODEL_NAMES to include M9)
- Regenerates: `synthesis/mechanisms.json` (affinityProfile fields)

**Step 1: Update MODEL_NAMES in the script to include M9**

```javascript
const MODEL_NAMES = {
  1: "Research Lab",
  2: "Center of Excellence",
  3: "Embedded Teams",
  4: "Hub-and-Spoke",
  5: "Product/Venture Lab",
  6: "Unnamed/Informal",
  7: "Tiger Teams",
  8: "Skunkworks",
  9: "AI-Native",
};
```

**Step 2: Run the script**

```bash
node scripts/compute-mechanism-affinity.js
```

**Step 3: Commit**

```bash
git add scripts/compute-mechanism-affinity.js synthesis/mechanisms.json
git commit -m "chore: recompute mechanism affinity after audit"
```

---

### Task 1.7: Update mechanism UI to show maturity badges

**Files:**
- Modify: `site/app/mechanisms/page.tsx` — add maturity badge to each mechanism card
- Modify: `site/app/mechanisms/[id]/page.tsx` — show maturity in header + scholarly anchor section

**Step 1: Add maturity badge to mechanisms list page**

In `site/app/mechanisms/page.tsx`, inside the mechanism card (after the specimen count badge), add:

```tsx
{m.maturity && (
  <span className={`shrink-0 rounded px-2 py-0.5 font-mono text-xs ${
    m.maturity === "widespread" ? "bg-amber-50 text-amber-700" :
    m.maturity === "emerging" ? "bg-sage-50 text-sage-600" :
    m.maturity === "deprecated" ? "bg-charcoal-100 text-charcoal-400" :
    "bg-forest-50 text-forest"
  }`}>
    {m.maturity}
  </span>
)}
```

**Step 2: Add scholarly anchor to mechanism detail page**

In `site/app/mechanisms/[id]/page.tsx`, after the "Theoretical Connection" section, add:

```tsx
{/* Scholarly Anchor */}
{mechanism.scholarlyAnchor && (
  <section>
    <h2 className="mb-2 font-serif text-lg text-forest">
      Scholarly Anchor
    </h2>
    <p className="text-sm leading-relaxed text-charcoal-600">
      {mechanism.scholarlyAnchor}
    </p>
  </section>
)}
```

Also add maturity badge to the header area:

```tsx
{mechanism.maturity && (
  <span className={`rounded px-2 py-0.5 font-mono text-xs ${
    mechanism.maturity === "widespread" ? "bg-amber-50 text-amber-700" :
    mechanism.maturity === "emerging" ? "bg-sage-50 text-sage-600" :
    "bg-forest-50 text-forest"
  }`}>
    {mechanism.maturity}
  </span>
)}
```

**Step 3: Commit**

```bash
git add site/app/mechanisms/page.tsx site/app/mechanisms/[id]/page.tsx
git commit -m "feat: show maturity badges and scholarly anchors on mechanism pages"
```

---

## Workstream 2: Cross-Cutting Insights

### Task 2.1: Create Insight types

**Files:**
- Modify: `site/lib/types/synthesis.ts` — add Insight interfaces

**Step 1: Add types at the end of the file**

```typescript
export interface InsightEvidence {
  specimenId: string;
  note: string;
}

export interface Insight {
  id: string;
  title: string;
  theme: "convergence" | "organizational-form" | "mechanism" | "workforce" | "methodology";
  finding: string;
  evidence: InsightEvidence[];
  theoreticalConnection?: string;
  discoveredIn: string;               // session file reference
  relatedMechanisms?: number[];
  relatedTensions?: number[];
}

export interface InsightData {
  description: string;
  lastUpdated: string;
  insights: Insight[];
}
```

**Step 2: Commit**

```bash
git add site/lib/types/synthesis.ts
git commit -m "feat: add Insight types for cross-cutting research findings"
```

---

### Task 2.2: Create synthesis/insights.json

**Files:**
- Create: `synthesis/insights.json`

**Step 1: Create the JSON file with all 13 curated insights**

```json
{
  "description": "Cross-cutting research findings discovered during synthesis — patterns that span multiple specimens, industries, or mechanisms. These are the field guide's key empirical contributions.",
  "lastUpdated": "2026-02-03",
  "insights": [
    {
      "id": "hub-spoke-regulated",
      "title": "Hub-and-Spoke Is the Default for Regulated Industries",
      "theme": "convergence",
      "finding": "Five pharmaceutical companies independently adopted Model 4 (Hub-and-Spoke) with central AI teams feeding into distributed therapeutic area teams. This convergence suggests hub-and-spoke is the structurally dominant pattern for regulated industries with deep domain expertise requirements — the central hub handles compliance and shared infrastructure while spokes preserve domain-specific knowledge.",
      "evidence": [
        { "specimenId": "pfizer", "note": "PACT partnership with central AI feeding into drug discovery pipeline" },
        { "specimenId": "roche-genentech", "note": "Lab in a Loop concept with central computational science team" },
        { "specimenId": "sanofi", "note": "Central AI hub feeding into therapeutic area teams" },
        { "specimenId": "novo-nordisk", "note": "300-person central hub with 20K Copilot licenses distributed across enterprise" },
        { "specimenId": "eli-lilly", "note": "Structurally separated hubs of 300-400 people operating like internal biotechs" }
      ],
      "theoreticalConnection": "Arrow's information economics: hub-and-spoke minimizes information loss in regulated environments where domain knowledge is deep and compliance costs are high. The hub centralizes the expensive compliance infrastructure; the spokes preserve specialized knowledge that can't be centralized without loss.",
      "discoveredIn": "synthesis/sessions/2026-02-01-synthesis.md",
      "relatedTensions": [3]
    },
    {
      "id": "management-delayering-convergent",
      "title": "Management Delayering Is Convergent Across Unrelated Industries",
      "theme": "convergence",
      "finding": "Microsoft (tech), UPS (logistics), and Amazon (retail/cloud) independently targeted management layers for elimination. AI reduces the information-aggregation role that middle managers traditionally play. These three companies from entirely different industries arrived at the same structural conclusion: when AI handles information synthesis, you need fewer managers.",
      "evidence": [
        { "specimenId": "microsoft", "note": "Nadella demands leaders act as individual contributors. Restructured exec ranks." },
        { "specimenId": "ups", "note": "-30K positions targeting management layers, $9B automation investment" },
        { "specimenId": "amazon", "note": "16K cuts Jan 2026 framed as removing bureaucracy, not cost-cutting" }
      ],
      "theoreticalConnection": "Simon's information-processing view of organizations: hierarchy exists to manage bounded rationality. AI expands individual cognitive capacity, reducing the need for hierarchical information aggregation. The middle manager's role as information broker becomes redundant when AI can synthesize information directly.",
      "discoveredIn": "synthesis/sessions/2026-02-01-synthesis-batch2.md",
      "relatedMechanisms": [11]
    },
    {
      "id": "ai-team-consolidation-arc",
      "title": "AI Team Consolidation Follows a Predictable Arc",
      "theme": "convergence",
      "finding": "Four of the world's largest tech companies — Google, Meta, Tencent, Amazon — independently went through the same structural evolution: scattered AI teams → parallel structures → forced merger under single leader. The coordination costs of parallel AI teams eventually exceed the benefits of independence, triggering consolidation. This appears to be a near-universal pattern for large tech organizations.",
      "evidence": [
        { "specimenId": "google-deepmind", "note": "Brain + DeepMind dual structure → merger under Hassabis" },
        { "specimenId": "meta-ai", "note": "FAIR + GenAI → consolidated MSL under Wang" },
        { "specimenId": "tencent", "note": "Scattered Hunyuan teams consolidated into unified TEG departments" },
        { "specimenId": "amazon-agi", "note": "Separate efforts unified under single leader (DeSantis)" }
      ],
      "theoreticalConnection": "Gibbons and Henderson's relational contracts: parallel teams create competing informal agreements about resource allocation and talent. As AI becomes core to the business, these competing contracts become unsustainable — the organization must consolidate to reduce coordination costs.",
      "discoveredIn": "synthesis/sessions/2026-01-31-synthesis.md",
      "relatedMechanisms": [6]
    },
    {
      "id": "caio-industry-waves",
      "title": "CAIO Appointments Spread in Industry Waves",
      "theme": "convergence",
      "finding": "CAIO (Chief AI Officer) appointments are spreading through industry peer groups: finance first (UBS, CBA, JPMorgan), then consulting (PwC, McKinsey), then advertising (Stagwell, Monks, IPG). Each wave adopts similar structural characteristics to its industry peers. The cross-industry rapidity suggests mimetic isomorphism — organizations copying peer structures — rather than independent rational analysis of what works.",
      "evidence": [
        { "specimenId": "ubs", "note": "CAIO from academic/finance pipeline (Daniele Magazzeni)" },
        { "specimenId": "commonwealth-bank", "note": "CAIO as boomerang hire from Lloyds Banking Group" },
        { "specimenId": "jpmorgan", "note": "LLM Suite deployed to 250K employees under CAIO leadership" },
        { "specimenId": "pwc", "note": "CAIO from enterprise IT background (Dan Priest)" },
        { "specimenId": "stagwell", "note": "Inaugural CAIO at ad holding company, part of industry wave" }
      ],
      "theoreticalConnection": "DiMaggio and Powell's institutional isomorphism: organizations facing uncertainty adopt structures from peers in their organizational field. The CAIO title is becoming an institutional norm — the title is convergent but the actual capabilities sought depend on the organization's primary challenge.",
      "discoveredIn": "synthesis/sessions/2026-02-02-synthesis.md"
    },
    {
      "id": "ai-native-no-ambidexterity",
      "title": "AI-Native Organizations Don't Face the Classic Ambidexterity Tension",
      "theme": "organizational-form",
      "finding": "SSI, Recursion, and Thinking Machines Lab are pure exploration organizations with no legacy execution business to balance against. The foundational premise of organizational ambidexterity — balancing exploration and exploitation — doesn't apply when there IS no exploitation business. These organizations represent a fundamentally different form where the product IS the exploration.",
      "evidence": [
        { "specimenId": "ssi", "note": "Pure research lab — no products, all compute directed at research. $3B funding with zero product pressure." },
        { "specimenId": "recursion", "note": "Entire company IS the research lab. 2.2M experiments/week without commercial application filter." },
        { "specimenId": "thinking-machines-lab", "note": "Founded to pursue next-generation AI approaches outside Big Tech product constraints" }
      ],
      "theoreticalConnection": "March (1991) assumed organizations face a tension between exploration and exploitation of existing competencies. AI-native organizations challenge this framing because there are no existing competencies to exploit — the entire organization is an exploration vehicle. This suggests ambidexterity theory has a boundary condition: it applies to organizations with legacy operations, not to de novo AI companies.",
      "discoveredIn": "synthesis/sessions/2026-01-31-synthesis.md",
      "relatedTensions": [1]
    },
    {
      "id": "founder-authority-structural-enabler",
      "title": "Founder Authority Determines Which Structural Models Are Accessible",
      "theme": "organizational-form",
      "finding": "Founder-led companies (Shopify, Recursion, Anthropic, Mercado-Libre, SSI) impose AI-first mandates that hired CEOs structurally cannot. This isn't just a contingency — it determines which organizational models are even available. Founder authority bypasses the organizational resistance that constrains professional-CEO-led companies to incremental structural change.",
      "evidence": [
        { "specimenId": "shopify", "note": "Tobi Lutke issued company-wide AI proficiency mandate" },
        { "specimenId": "recursion", "note": "Founder-driven hypothesis-free automated discovery — no hired CEO would bet the company on this" },
        { "specimenId": "anthropic", "note": "7 co-founders with equal equity carrying organizational values" },
        { "specimenId": "mercado-libre", "note": "Founder stepped down as CEO to focus hands-on on AI" }
      ],
      "theoreticalConnection": "Holmstrom's contract theory: hired CEOs face agency problems that founders don't. A founder's residual claim on the firm's value aligns their incentives with long-term structural transformation. Hired CEOs face career risk from radical restructuring — their implicit contract rewards stability, not revolution.",
      "discoveredIn": "synthesis/sessions/2026-01-31-synthesis.md"
    },
    {
      "id": "consulting-dual-identity",
      "title": "Consulting Firms Face a Dual-Identity Problem as Specimens",
      "theme": "methodology",
      "finding": "McKinsey, BCG, Accenture, and Deloitte simultaneously adopt AI internally AND publish frameworks about AI adoption. Their published frameworks may reflect their own structural biases rather than objective analysis. This creates a methodological challenge for the field guide: using consulting-published AI frameworks as sources risks circular reasoning when the consulting firm is itself a specimen.",
      "evidence": [
        { "specimenId": "mckinsey-quantumblack", "note": "QuantumBlack publishes AI adoption research while itself being an AI product lab" },
        { "specimenId": "bcg-trailblazers", "note": "BCG AI Radar published while BCG restructures for AI internally" }
      ],
      "theoreticalConnection": "Observer effect: the act of studying organizational AI adoption while being a participant in it creates bias. Consulting frameworks that recommend 'Center of Excellence' structures may do so because that's what consulting firms sell, not because it's the optimal structure.",
      "discoveredIn": "synthesis/sessions/2026-01-31-synthesis.md"
    },
    {
      "id": "meta-exploration-failure",
      "title": "Meta as Natural Experiment in Exploration Failure",
      "theme": "mechanism",
      "finding": "Meta's structural evolution provides a textbook natural experiment in what happens when Mechanism #1 (Protect Off-Strategy Work) is violated. The dual-track structure (FAIR research + GenAI product) was consolidated into MSL, research autonomy was sacrificed for product urgency, and LeCun's departure demonstrates the cost. Counter-evidence is as scientifically valuable as positive evidence.",
      "evidence": [
        { "specimenId": "meta-ai", "note": "FAIR autonomy sacrificed when GenAI + FAIR consolidated under Wang. LeCun: 'You don't tell a researcher what to do.'" }
      ],
      "theoreticalConnection": "March (1991): exploitation drives out exploration because exploitation has more certain, more proximate returns. Meta's leadership chose product urgency (exploitation) over research autonomy (exploration) — exactly the dynamic March predicted.",
      "discoveredIn": "synthesis/sessions/2026-01-31-substacks-bg2-press-session.md",
      "relatedMechanisms": [1]
    },
    {
      "id": "speed-depth-trap",
      "title": "Speed Without Depth Is a Trap",
      "theme": "mechanism",
      "finding": "Klarna's aggressive AI-driven customer service replacement led to quality degradation and a public reversal — the CEO acknowledged the correction and resumed human hiring. This is the clearest cautionary case for Mechanism #5 (Deploy to Thousands): deploying at scale is a discovery mechanism, but deploying without quality monitoring creates technical and reputational debt that's expensive to reverse.",
      "evidence": [
        { "specimenId": "klarna", "note": "Cut customer service staff aggressively for AI automation, then publicly reversed when quality degraded" }
      ],
      "theoreticalConnection": "Arrow's learning-by-doing: deploying AI at scale generates information, but only if the organization has feedback mechanisms to capture quality signals. Without monitoring, deployment becomes a bet, not an experiment.",
      "discoveredIn": "synthesis/sessions/2026-02-01-synthesis.md",
      "relatedMechanisms": [5],
      "relatedTensions": [2]
    },
    {
      "id": "regulation-expensive-not-slow",
      "title": "Regulation Doesn't Mean Slow — It Means Expensive",
      "theme": "mechanism",
      "finding": "JPMorgan deploys AI updates in 8-week cycles despite being one of the most heavily regulated financial institutions in the world. Bank of America independently developed similar rapid deployment cycles. The conventional assumption that regulation means slow AI adoption is wrong — what regulation actually requires is expensive compliance infrastructure (audit trails, review processes, explainability). Organizations that invest in this infrastructure deploy as fast as unregulated companies.",
      "evidence": [
        { "specimenId": "jpmorgan", "note": "LLM Suite updated every 8 weeks. 250K employees, multi-model architecture." },
        { "specimenId": "bank-of-america", "note": "Erica chatbot rapid iteration in regulated banking context" }
      ],
      "theoreticalConnection": "Connects to Mechanism #8 (Turn Compliance Into Deployment Advantage). The cost structure of regulatory compliance creates barriers to entry — organizations that have already paid the fixed cost of compliance infrastructure face lower marginal costs for each new AI deployment.",
      "discoveredIn": "synthesis/sessions/2026-02-01-synthesis.md",
      "relatedMechanisms": [8]
    },
    {
      "id": "google-25-year-arc",
      "title": "Google's 25-Year AI Structural Evolution Is the Most Complete Arc in the Collection",
      "theme": "convergence",
      "finding": "Google's AI organization has evolved through five distinct structural phases over 25 years: decentralized exploration (2001-2009) → incubator model via X (2009-2011) → dual structure Brain+DeepMind (2014-2023) → forced merger under Hassabis (2023) → consolidation via Project EAT (2025-2026). This is the most complete structural evolution narrative in the collection and demonstrates that organizations cycle through structural models over time.",
      "evidence": [
        { "specimenId": "google-deepmind", "note": "Brain+DeepMind merger under Hassabis after years of parallel operation" },
        { "specimenId": "google-ai-infra", "note": "Project EAT consolidates teams from Research, Cloud, and hardware into AI2 unit" },
        { "specimenId": "google-x", "note": "X operated as AI incubator from 2009, recruiting academic researchers" }
      ],
      "theoreticalConnection": "Henderson and Clark's architectural innovation: Google's structural evolution tracks the shift from AI as component innovation (embedded in products) to AI as architectural innovation (requiring organizational restructuring). Each phase represents a different answer to the same question: where does AI research belong?",
      "discoveredIn": "synthesis/sessions/2026-01-31-deep-scan-session.md",
      "relatedMechanisms": [1, 6]
    },
    {
      "id": "ai-restructuring-isomorphism",
      "title": "AI-Driven Workforce Restructuring Looks Like Institutional Isomorphism",
      "theme": "workforce",
      "finding": "Seven organizations across different industries announced AI-driven headcount reductions in a tight 2024-2026 window. The cross-industry rapidity and similar framing ('AI-enabled transformation') suggests mimetic isomorphism — organizations copying peers — rather than independent rational analysis. Deutsche Bank has warned of 'AI redundancy washing': using AI as justification for cuts that would have happened anyway.",
      "evidence": [
        { "specimenId": "klarna", "note": "Aggressive AI-driven cuts, later reversed" },
        { "specimenId": "amazon", "note": "16K cuts framed as 'culture'" },
        { "specimenId": "salesforce", "note": "Support staff 9K to 5K alongside AI deployment" },
        { "specimenId": "citigroup", "note": "-20K headcount via AI automation" },
        { "specimenId": "dow", "note": "4,500 cuts with C3 AI platform deployment" }
      ],
      "theoreticalConnection": "DiMaggio and Powell: mimetic isomorphism occurs when organizations facing uncertainty adopt practices from organizations they perceive as successful. The simultaneous AI-restructuring wave across unrelated industries is a textbook case.",
      "discoveredIn": "synthesis/sessions/2026-01-31-synthesis.md",
      "relatedMechanisms": [11]
    },
    {
      "id": "entry-level-talent-hollow",
      "title": "Entry-Level Elimination Creates a Talent Hollow",
      "theme": "workforce",
      "finding": "Companies are cutting entry-level roles (the 'Senior-Only' hiring model) while Gen Z has the highest AI proficiency of any generation. This creates a structural talent pipeline problem: organizations are eliminating the roles that develop future senior talent. The emerging 'AI Reliability Engineer' role — managing the integrity of AI output — represents a new entry point, but it's unclear whether this compensates for the breadth of traditional entry-level elimination.",
      "evidence": [
        { "specimenId": "pinterest", "note": "700-800 jobs cut (15% workforce) in AI pivot restructuring" },
        { "specimenId": "klarna", "note": "Stopped hiring entirely, relying on AI to replace roles" }
      ],
      "theoreticalConnection": "March's exploration-exploitation tradeoff applied to human capital: organizations are exploiting their current senior talent while cutting off the exploration pipeline (entry-level hiring) that would develop the next generation. This is the workforce equivalent of the short-termism trap March predicted.",
      "discoveredIn": "research/sessions/2026-01-31-tier2-podcasts-press-session.md"
    }
  ]
}
```

**Step 2: Commit**

```bash
git add synthesis/insights.json
git commit -m "feat: create insights.json with 13 cross-cutting research findings"
```

---

### Task 2.3: Add getInsights() data access function

**Files:**
- Modify: `site/lib/data/synthesis.ts`

**Step 1: Add the import and function**

Add to the imports at the top:

```typescript
import type {
  MechanismData,
  TensionData,
  ContingencyData,
  InsightData,           // NEW
} from "@/lib/types/synthesis";
```

Add a new function at the end:

```typescript
export async function getInsights(): Promise<InsightData> {
  const raw = await fs.readFile(
    path.join(SYNTHESIS_DIR, "insights.json"),
    "utf-8"
  );
  return JSON.parse(raw);
}
```

**Step 2: Commit**

```bash
git add site/lib/data/synthesis.ts
git commit -m "feat: add getInsights() data access function"
```

---

### Task 2.4: Create /insights page

**Files:**
- Create: `site/app/insights/page.tsx`
- Modify: `site/components/layout/SiteHeader.tsx` — add nav link

**Step 1: Create the insights page**

```tsx
import Link from "next/link";
import { getInsights } from "@/lib/data/synthesis";
import { getAllSpecimens } from "@/lib/data/specimens";

const THEME_LABELS: Record<string, { label: string; color: string }> = {
  convergence: { label: "Convergence Pattern", color: "bg-forest-50 text-forest" },
  "organizational-form": { label: "Organizational Form", color: "bg-amber-50 text-amber-700" },
  mechanism: { label: "Mechanism Insight", color: "bg-sage-50 text-sage-700" },
  workforce: { label: "Workforce", color: "bg-violet-50 text-violet-700" },
  methodology: { label: "Methodology", color: "bg-charcoal-100 text-charcoal-600" },
};

export const metadata = {
  title: "Research Insights — Field Guide to AI Organizations",
  description: "Cross-cutting findings from systematic observation of how organizations structure for AI",
};

export default async function InsightsPage() {
  const [insightData, specimens] = await Promise.all([
    getInsights(),
    getAllSpecimens(),
  ]);

  // Group by theme
  const themes = ["convergence", "organizational-form", "mechanism", "workforce", "methodology"];

  return (
    <div className="space-y-10">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Research Insights
        </h1>
        <p className="mt-2 max-w-3xl text-charcoal-500">
          Cross-cutting findings discovered during synthesis — patterns that
          span multiple specimens, industries, or mechanisms. These are the
          field guide&apos;s key empirical contributions.
        </p>
      </header>

      {themes.map((theme) => {
        const themeInsights = insightData.insights.filter((i) => i.theme === theme);
        if (themeInsights.length === 0) return null;
        const themeInfo = THEME_LABELS[theme];
        return (
          <section key={theme}>
            <h2 className="mb-4 font-serif text-xl text-forest">
              {themeInfo.label}s ({themeInsights.length})
            </h2>
            <div className="space-y-4">
              {themeInsights.map((insight) => (
                <div
                  key={insight.id}
                  className="rounded-lg border border-sage-200 bg-cream-50 p-5"
                >
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="font-serif text-lg font-medium text-forest">
                      {insight.title}
                    </h3>
                    <span className={`shrink-0 rounded px-2 py-0.5 text-[10px] font-medium ${themeInfo.color}`}>
                      {themeInfo.label}
                    </span>
                  </div>

                  <p className="mt-2 text-sm leading-relaxed text-charcoal-600">
                    {insight.finding}
                  </p>

                  {/* Evidence */}
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {insight.evidence.map((e) => {
                      const specimen = specimens.find((s) => s.id === e.specimenId);
                      return (
                        <Link
                          key={e.specimenId}
                          href={`/specimens/${e.specimenId}`}
                          className="rounded bg-sage-50 px-2 py-0.5 text-[10px] text-sage-700 hover:bg-sage-100"
                          title={e.note}
                        >
                          {specimen?.name ?? e.specimenId}
                        </Link>
                      );
                    })}
                  </div>

                  {/* Theoretical connection */}
                  {insight.theoreticalConnection && (
                    <div className="mt-3 rounded border-l-4 border-l-amber bg-white p-3">
                      <p className="text-xs leading-relaxed text-charcoal-500">
                        {insight.theoreticalConnection}
                      </p>
                    </div>
                  )}

                  {/* Related mechanisms/tensions */}
                  <div className="mt-2 flex flex-wrap gap-2">
                    {insight.relatedMechanisms?.map((id) => (
                      <Link
                        key={`m-${id}`}
                        href={`/mechanisms/${id}`}
                        className="text-[10px] text-forest hover:underline"
                      >
                        Principle #{id}
                      </Link>
                    ))}
                    {insight.relatedTensions?.map((id) => (
                      <Link
                        key={`t-${id}`}
                        href="/tensions"
                        className="text-[10px] text-amber-700 hover:underline"
                      >
                        Tension #{id}
                      </Link>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
```

**Step 2: Add nav link**

In `site/components/layout/SiteHeader.tsx`, add to the navItems array:

```typescript
{ href: "/insights", label: "Insights" },
```

Place it after "Principles" and before "Tensions" for logical flow:

```typescript
const navItems = [
  { href: "/matcher", label: "Matcher" },
  { href: "/specimens", label: "Specimens" },
  { href: "/ai-native", label: "AI-Native" },
  { href: "/taxonomy", label: "Taxonomy" },
  { href: "/mechanisms", label: "Principles" },
  { href: "/insights", label: "Insights" },
  { href: "/tensions", label: "Tensions" },
  { href: "/compare", label: "Compare" },
  { href: "/about", label: "About" },
];
```

**Step 3: Commit**

```bash
git add site/app/insights/page.tsx site/components/layout/SiteHeader.tsx
git commit -m "feat: add /insights page with cross-cutting research findings"
```

---

### Task 2.5: Surface top insights on home page

**Files:**
- Modify: `site/app/page.tsx`

**Step 1: Import getInsights and fetch data**

Add to the imports:
```typescript
import { getInsights } from "@/lib/data/synthesis";  // ADD alongside existing getMechanisms import
```

Add to the Promise.all:
```typescript
const [stats, specimens, mechanismData, insightData] = await Promise.all([
  getComputedStats(),
  getAllSpecimens(),
  getMechanisms(),
  getInsights(),
]);
```

**Step 2: Add an insights section before the Collection Summary section**

Find the comment `Section 4: Collection Summary` and add a new section before it:

```tsx
{/* ═══════════════════════════════════════════════════════════
    Section: Key Research Insights
    ═══════════════════════════════════════════════════════════ */}
<section className="bg-cream-50 px-4 py-16 sm:px-6 lg:px-8">
  <div className="mx-auto max-w-7xl">
    <div className="text-center">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage-500">
        From the Field
      </p>
      <h2 className="mt-2 font-serif text-3xl font-semibold text-forest">
        Key Findings
      </h2>
      <p className="mx-auto mt-3 max-w-lg text-charcoal-500">
        Cross-cutting patterns discovered across the specimen collection.
      </p>
    </div>
    <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {insightData.insights.slice(0, 6).map((insight) => (
        <Link
          key={insight.id}
          href="/insights"
          className="group rounded-xl border border-sage-200 bg-white p-5 transition-all hover:-translate-y-1 hover:shadow-md"
        >
          <p className="font-mono text-[10px] uppercase tracking-wide text-sage-500">
            {insight.theme.replace("-", " ")}
          </p>
          <p className="mt-2 font-serif text-base font-medium text-forest group-hover:text-forest-600">
            {insight.title}
          </p>
          <p className="mt-2 line-clamp-3 text-sm leading-snug text-charcoal-500">
            {insight.finding}
          </p>
          <div className="mt-3 flex flex-wrap gap-1">
            {insight.evidence.slice(0, 3).map((e) => (
              <span
                key={e.specimenId}
                className="rounded bg-sage-50 px-1.5 py-0.5 text-[10px] text-sage-600"
              >
                {e.specimenId}
              </span>
            ))}
            {insight.evidence.length > 3 && (
              <span className="text-[10px] text-charcoal-400">
                +{insight.evidence.length - 3} more
              </span>
            )}
          </div>
        </Link>
      ))}
    </div>
    <div className="mt-8 text-center">
      <Link
        href="/insights"
        className="font-mono text-sm text-forest hover:underline"
      >
        View all {insightData.insights.length} insights &rarr;
      </Link>
    </div>
  </div>
</section>
```

**Step 3: Commit**

```bash
git add site/app/page.tsx
git commit -m "feat: surface top 6 insights on home page"
```

---

## Workstream 3: Specimen Schema Improvements

### Task 3.1: Identify consulting specimens needing secondary models

**Files:**
- Modify: Various `specimens/*.json` files

Note: The `Classification` interface already has `secondaryModel` and `secondaryModelName` fields (confirmed in `site/lib/types/specimen.ts:54-55`). McKinsey already uses them. This task adds secondary models to other multi-model specimens.

**Step 1: Update the following specimens with secondary models**

Use a Node.js script to batch-update:

```bash
node -e "
const fs = require('fs');
const updates = {
  'accenture-openai': { secondaryModel: 2, secondaryModelName: 'Center of Excellence' },
  'bcg-trailblazers': { secondaryModel: 5, secondaryModelName: 'Product/Venture Lab' },
  'salesforce': { secondaryModel: 5, secondaryModelName: 'Product/Venture Lab' },
  'microsoft': { secondaryModel: 1, secondaryModelName: 'Research Lab' },
  'nvidia': { secondaryModel: 1, secondaryModelName: 'Research Lab' },
  'jpmorgan': { secondaryModel: 2, secondaryModelName: 'Center of Excellence' },
};
for (const [id, fields] of Object.entries(updates)) {
  const path = 'specimens/' + id + '.json';
  if (!fs.existsSync(path)) { console.log('SKIP: ' + id); continue; }
  const d = JSON.parse(fs.readFileSync(path, 'utf-8'));
  if (d.classification.secondaryModel) { console.log('ALREADY: ' + id); continue; }
  Object.assign(d.classification, fields);
  fs.writeFileSync(path, JSON.stringify(d, null, 2) + '\n');
  console.log('UPDATED: ' + id + ' +M' + fields.secondaryModel);
}
"
```

**Step 2: Commit**

```bash
git add specimens/*.json
git commit -m "feat: add secondary models to multi-model specimens"
```

---

## Workstream 4: Theoretical Grounding

### Task 4.1: Add scholarly anchors to all confirmed mechanisms

**Files:**
- Modify: `synthesis/mechanisms.json` — add `scholarlyAnchor` field to each confirmed mechanism

**Step 1: Add scholarly anchors**

For each surviving confirmed mechanism, add a `scholarlyAnchor` field that names the scholar, the specific work, and explains the connection in plain language. Not jargon — economics-flavored clarity.

| ID | Mechanism | Scholar | Anchor |
|----|-----------|---------|--------|
| 1 | Protect Off-Strategy Work | March (1991) | March predicted exploitation crowds out exploration because it has more certain, more proximate returns. This mechanism is the organizational design response: structural separation forces resource allocation to exploration that market logic would otherwise kill. Our data shows the protection mechanism varies by model — ring-fencing (M1), separate governance (M5), CEO shielding (M4) — extending March's insight into a taxonomy of protection strategies. |
| 3 | Embed Product at Research Frontier | Henderson & Clark (1990) | Henderson and Clark showed that architectural innovation fails when organizations treat it as component innovation. This mechanism embeds product teams at the research frontier specifically to prevent that failure — ensuring product development absorbs architectural changes in real time rather than trying to bolt them on after the fact. |
| 5 | Deploy to Thousands Before You Know What Works | Arrow (1962) | Arrow's learning-by-doing framework: productivity gains come from cumulative production experience, not from ex ante planning. Deploying AI broadly before knowing the ROI is a bet on learning-by-doing — the information value of observing thousands of usage patterns exceeds the cost of premature deployment. The mechanism works because organizations that wait for perfect information deploy too late. |
| 6 | Merge Competing AI Teams Under Single Leader | Gibbons & Henderson (2012) | Gibbons and Henderson's relational contracts: parallel teams create competing informal agreements about resources, talent, and direction. When AI shifts from peripheral to core, these competing contracts become unsustainable. Consolidation reduces the coordination costs that relational contracts impose. |
| 7 | Put Executives on the Tools | Eisenhardt (1989) | Eisenhardt's strategic decision-making in high-velocity environments: the quality and speed of decisions improve when executives have direct access to real-time information rather than filtered reports. When executives use AI tools themselves, they develop intuitions about AI capability that no briefing can provide — enabling faster, better-informed structural decisions about AI investment and organization. |
| 8 | Turn Compliance Into Deployment Advantage | Arrow (1974) | Arrow's limits of organization: organizations exist to solve information problems that markets cannot. Regulatory compliance infrastructure solves an information asymmetry problem between the organization and its regulators. Once that infrastructure is built, the marginal cost of deploying new AI applications drops — creating an information-economic moat that competitors without this infrastructure cannot easily replicate. |
| 10 | Productize Internal Operational Advantages | Holmstrom & Milgrom (1991) | Holmstrom's multitask principal-agent model: when organizations build AI for internal operations, the returns are capped by internal demand. Productizing extends the return on the same investment — the principal (the firm) captures value from multiple tasks (internal efficiency + external revenue) without proportional additional cost. This is why the M5c Platform-to-Product pathway is structurally rational. |
| 11 | Flatten Management Layers to Speed AI Decisions | Simon (1947) | Simon's information-processing view: hierarchy exists to manage bounded rationality. Managers aggregate, filter, and transmit information upward. AI expands individual cognitive capacity by automating information synthesis — directly substituting for the aggregation function that justified management layers. Delayering is the structural consequence of reduced need for human information processing. |

Write these as the `scholarlyAnchor` field value for each mechanism in `synthesis/mechanisms.json`.

**Step 2: Update the existing `theoreticalConnection` fields**

Replace the current boilerplate `theoreticalConnection` values with crisp, one-sentence connections. Example replacements:

- #1: Current: "Structural ambidexterity — physical separation protects exploration from exploitation pressures." → New: "March (1991): exploitation crowds out exploration without deliberate structural protection. This mechanism is how organizations implement that protection."
- #5: Current: "Contextual ambidexterity at scale — let individuals find explore/execute balance." → New: "Arrow (1962): the information value of observing AI usage at scale exceeds the cost of premature deployment."

**Step 3: Commit**

```bash
git add synthesis/mechanisms.json
git commit -m "feat: add scholarly anchors grounded in organizational economics"
```

---

## Final: Build Verification and State Update

### Task F.1: Run production build

**Step 1: Build**

```bash
cd site && npm run build
```

Expected: All pages compile successfully, no TypeScript errors, no lint errors.

**Step 2: Verify page count**

The build should generate pages for the new `/insights` route. Total should be 123+ pages (122 previously + insights page).

---

### Task F.2: Update APP_STATE.md

**Step 1: Add session log entry**

Add a new row to the Session Log table:

```markdown
| 2026-02-03 | **Intellectual Rigor Overhaul**: (1) Mechanism audit: demoted #2, #9, #12 to candidate; renamed #8 to "Turn Compliance Into Deployment Advantage"; split #11 into delayering mechanism + headcount candidate; added maturity lifecycle (emerging/confirmed/widespread/deprecated); result: 8 confirmed mechanisms. (2) Cross-cutting insights: created synthesis/insights.json with 13 research findings; new /insights page + nav link; top 6 insights on home page. (3) Specimen schema: added secondary models to 6 multi-model specimens. (4) Theoretical grounding: added scholarlyAnchor to all 8 confirmed mechanisms connecting to March, Simon, Arrow, Holmstrom, Henderson/Clark, Eisenhardt, Gibbons/Henderson. Build verified. |
```

**Step 2: Update synthesis data counts**

Change: `12 confirmed mechanisms + 5 candidates` → `8 confirmed mechanisms + 9 candidates`

**Step 3: Commit**

```bash
git add APP_STATE.md
git commit -m "docs: update APP_STATE for intellectual rigor overhaul"
```

---

## Execution Order

The recommended execution order minimizes dependencies:

1. **Task 1.1** — Add types (maturity, scholarly anchor)
2. **Task 2.1** — Add Insight types
3. **Task 2.3** — Add getInsights() function
4. **Task 1.2** — Demote 3 mechanisms
5. **Task 1.3** — Rename #8
6. **Task 1.4** — Split #11
7. **Task 1.5** — Add maturity tags
8. **Task 4.1** — Add scholarly anchors + theoretical connections
9. **Task 1.6** — Recompute affinity
10. **Task 2.2** — Create insights.json
11. **Task 1.7** — Update mechanism UI
12. **Task 2.4** — Create /insights page + nav
13. **Task 2.5** — Surface insights on home page
14. **Task 3.1** — Secondary model specimens
15. **Task F.1** — Build verification
16. **Task F.2** — Update APP_STATE.md
