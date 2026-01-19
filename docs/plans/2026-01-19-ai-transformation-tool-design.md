# AI Transformation Architecture Tool - Design Document

**Date:** 2026-01-19
**Status:** Approved for implementation

---

## Overview

An interactive tool that helps leadership teams develop stances on AI transformation architecture. Based on a five-layer, eight-principle framework derived from research on 270+ organizations.

**Core philosophy:** Self-directed exploration with depth on demand. Leadership teams see the whole landscape, choose where to engage, and go deep when they want to.

---

## Architecture

### Two Distinct Concerns

1. **The Library** — Research-populated content that grows over time
2. **The Application** — Renders from Library, captures user state

---

## The Library

A structured data store that research skills write to. All organizational knowledge lives here.

### Directory Structure

```
/library/
  /framework/
    layers.json           # 5 layers with their 8 architectural principles
    diagramTemplates.json # 9 visual templates for case diagrams
    principleGroups.json  # 6 groups for organizing design principles
    tensions.json         # Cross-principle tension patterns

  /cases/
    eli-lilly.json
    google-x.json
    anthropic.json
    samsung-c-lab.json
    tesla.json
    bank-of-america.json
    jpmorgan.json
    mckinsey-quantumblack.json
    recursion.json
    pg-chatpg.json
    moderna.json
    shopify.json
    nvidia.json
    sanofi.json
    roche-genentech.json

  /designPrinciples/
    protect-deviations.json
    reward-fast-failure.json
    ride-the-exponential.json
    internal-first-validation.json
    exit-paths-entrepreneurs.json
    data-flywheel.json
    consumer-grade-ux.json
    rapid-iteration-cycles.json
    mandatory-proficiency.json
    domain-expertise.json
    remove-human-intuition-bottlenecks.json
    information-symmetry.json
    protected-exploration-time.json
    ring-fence-budget.json
    governance-lets-it-cook.json
    a-team-capability.json
    lab-to-operations-handoff.json
    ceo-as-political-shield.json
```

### Case Schema

```json
{
  "id": "google-x",
  "company": "Google X",
  "title": "The Moonshot Factory",
  "summary": "100+ experiments annually, 2% graduation rate, teams bonused for killing projects",
  "diagramTemplate": "centralized-lab",
  "architecturalPrinciples": ["locus-of-innovation"],
  "designPrinciples": ["reward-fast-failure", "ring-fence-budget", "governance-lets-it-cook"],
  "content": {
    "whatItIs": "Alphabet's 'moonshot factory'—a dedicated organization...",
    "howItWorks": ["Launches 100+ experiments annually", "2% graduation rate...", "..."],
    "coreInsight": "The incentive structure is the innovation...",
    "keyMetrics": "Graduates: Waymo, Verily, Wing, Loon, Chronicle",
    "sources": ["TechCrunch Disrupt 2025", "HBR Podcast", "NPR Interview"]
  },
  "conversations": [],
  "extendedContent": {}
}
```

### Design Principle Schema

```json
{
  "id": "reward-fast-failure",
  "title": "Reward Fast Failure Explicitly",
  "group": "incentives-monitoring-measurement",
  "architecturalPrinciples": ["locus-of-innovation", "measurement-philosophy"],
  "insight": "Most organizations implicitly punish failure even when they say they value experimentation. Explicit rewards for killing projects early are required.",
  "manifestations": [
    "Google X: 'We have bonused every single person on teams that end their projects'",
    "Pre-mortems before starting (predict why this will fail)",
    "Public celebration of killed projects, not just successes"
  ],
  "test": "Can you name the last project that was killed early and what happened to the people who killed it?",
  "conversations": [],
  "extendedContent": {}
}
```

### Design Principle Groups

| Group | Principles |
|-------|------------|
| **Protection** | Protect Deviations, Protected Exploration Time, Ring-Fence Budget, CEO as Political Shield |
| **Lab-to-Org Handoff & Integration** | Internal-First Validation, Data Flywheel, Consumer-Grade UX, Information Symmetry, Lab-to-Operations Handoff |
| **Incentives, Monitoring & Measurement** | Reward Fast Failure, Governance That Lets It Cook |
| **Culture** | Mandatory Proficiency |
| **Resources & Talent** | Exit Paths for Entrepreneurs, Domain Expertise, Remove Human Intuition Bottlenecks, A-Team Capability |
| **Managing Speed & Time Horizons** | Ride the Exponential, Rapid Iteration Cycles |

### Diagram Templates

9 templates covering structural patterns:

| Template ID | Pattern | Example Cases |
|-------------|---------|---------------|
| `centralized-lab` | Dedicated unit, separate from operations | Google X, Samsung C-Lab, Sanofi |
| `distributed-hubs` | Multiple semi-autonomous units | Eli Lilly |
| `embedded-universal` | AI expected everywhere, no separate lab | Shopify, Moderna, NVIDIA |
| `center-of-excellence` | Central team serving whole org | JPMorgan, Bank of America |
| `product-as-lab` | Deployed products generate learning | Tesla |
| `hybrid-labs-core` | Separate exploration + core product | Anthropic |
| `tight-loop` | Rapid iteration between prediction/validation | Roche/Genentech, Recursion |
| `external-acquisition` | Capability acquired from outside | McKinsey/QuantumBlack |
| `broad-deployment` | Skip pilots, deploy widely immediately | P&G |

Templates are architectural/org-chart style diagrams showing organizational units, information flow, and where the "lab" sits relative to operations.

### Relationships

- **Cases → Design Principles:** Explicit in case JSON (`designPrinciples` array)
- **Design Principles → Cases:** Derived at runtime (reverse lookup)
- **Both → Architectural Principles:** Explicit tags on both (`architecturalPrinciples` array)

---

## The Application

### Tech Stack

- React application
- localStorage for user state persistence
- No backend required for MVP (Library files are static JSON)

### User State (localStorage)

```json
{
  "locus-of-innovation": {
    "status": "stance-taken",
    "starredCases": ["google-x", "anthropic", "eli-lilly"],
    "starredPrinciples": ["reward-fast-failure", "protect-deviations"],
    "notes": "We're more like Lilly than Google X...",
    "draftStance": "",
    "crystallizedStance": "We believe the best ideas for AI transformation...",
    "lastModified": "2026-01-19T14:30:00Z"
  },
  "north-star": {
    "status": "in-progress",
    "starredCases": [],
    "starredPrinciples": [],
    "notes": "",
    "draftStance": "Our identity is...",
    "crystallizedStance": null,
    "lastModified": "2026-01-19T15:00:00Z"
  }
}
```

---

## UI Views

### View 1: The Stack (Home)

The five-layer architecture as the navigation spine.

**Layout:**
- Vertical stack of 5 layer blocks
- Each layer shows: layer name, architectural principles within it, status badge per principle
- Click any principle → navigates to deep-dive

**Visual treatment:**
- Layers as distinct horizontal bands (subtle background color differentiation)
- Principles as clickable rows within each layer
- Status badges:
  - `Unexplored` — gray
  - `In Progress` — amber
  - `Stance Taken` — green

**Bottom actions:**
- "View Tensions" button (disabled until 2+ stances taken)
- "Generate Artifact" button (disabled until stances exist)

```
┌─────────────────────────────────────────────────────────────┐
│ IDENTITY                                                     │
│ ○ Organizational North Star                     [Unexplored] │
├─────────────────────────────────────────────────────────────┤
│ ORIENTATION                                                  │
│ ◐ Stance on Uncertainty                        [In Progress] │
│ ○ Measurement Philosophy                        [Unexplored] │
├─────────────────────────────────────────────────────────────┤
│ FLOW                                                         │
│ ● Locus of Innovation                          [Stance Taken]│
│ ○ Information Architecture                      [Unexplored] │
├─────────────────────────────────────────────────────────────┤
│ STRUCTURE                                                    │
│ ○ Ambidexterity Structure                       [Unexplored] │
│ ○ Resource Allocation Logic                     [Unexplored] │
├─────────────────────────────────────────────────────────────┤
│ WORK                                                         │
│ ○ Human-AI Work Boundaries                      [Unexplored] │
└─────────────────────────────────────────────────────────────┘

        [View Tensions]  [Generate Artifact]
```

---

### View 2: Principle Deep-Dive

Three-zone layout when user clicks into a principle.

**Zone A: Header (~15% height, top)**
- Principle name and layer context
- The core question for this principle
- "Why this is architectural" summary
- Back arrow to return to Stack

**Zone B: Library Browser (~50% width, left)**
- Two tabs: `Cases` | `Design Principles`
- Scrollable card list within each tab

**Zone C: Workspace (~50% width, right)**
- Your Selections (starred items)
- Notes textarea
- Draft Stance textarea
- Action buttons

```
┌────────────────────────────────────────────────────────────────────────┐
│ ← Back    FLOW > Locus of Innovation                                   │
│                                                                        │
│ Core Question: Where do you expect the best ideas for AI               │
│ transformation to originate, and how do you design the organizational  │
│ mechanisms to cultivate, capture, and deploy them?                     │
├──────────────────────────────────┬─────────────────────────────────────┤
│  [Cases]  [Design Principles]    │  YOUR SELECTIONS                    │
│                                  │  ┌─────┐ ┌─────┐ ┌─────┐            │
│  ┌──────────────────────────┐    │  │GoogX│ │Anthr│ │Lilly│            │
│  │ [diagram] Google X       ☆│   │  └─────┘ └─────┘ └─────┘            │
│  │ 100+ experiments...       │   │                                     │
│  └──────────────────────────┘    │  NOTES                              │
│                                  │  ┌─────────────────────────────┐    │
│  ┌──────────────────────────┐    │  │ We're more like Lilly...    │    │
│  │ [diagram] Anthropic      ☆│   │  │                             │    │
│  │ Labs team + ride the...   │   │  └─────────────────────────────┘    │
│  └──────────────────────────┘    │                                     │
│                                  │  DRAFT STANCE                       │
│  ┌──────────────────────────┐    │  ┌─────────────────────────────┐    │
│  │ [diagram] Eli Lilly      ★│   │  │ We believe the best ideas   │    │
│  │ Decentralized domain...   │   │  │ will come from...           │    │
│  └──────────────────────────┘    │  └─────────────────────────────┘    │
│                                  │                                     │
│  ...more cards...                │  [Save as In Progress]              │
│                                  │  [Crystallize Stance]               │
└──────────────────────────────────┴─────────────────────────────────────┘
```

---

### Card Components

#### Case Card (Collapsed)

```
┌─────────────────────────────────────────────────────┐
│ ┌─────────┐                                    ☆    │
│ │ diagram │  Google X: The Moonshot Factory         │
│ │ (80x80) │  100+ experiments annually, 2%          │
│ └─────────┘  graduation rate, teams bonused for...  │
└─────────────────────────────────────────────────────┘
```

- Diagram thumbnail (~80x80px) rendered from template
- Company + title in bold
- One-line summary (truncated ~100 chars)
- Star icon (outline/filled)
- Click anywhere except star → expands

#### Case Card (Expanded)

```
┌─────────────────────────────────────────────────────┐
│ ┌───────────────┐                              ★    │
│ │   diagram     │  Google X: The Moonshot Factory   │
│ │   (larger)    │                                   │
│ └───────────────┘                                   │
├─────────────────────────────────────────────────────┤
│ What it is:                                         │
│ Alphabet's "moonshot factory"—a dedicated org...    │
│                                                     │
│ How it works:                                       │
│ • Launches 100+ experiments annually                │
│ • 2% graduation rate...                             │
│                                                     │
│ Core insight:                                       │
│ "The incentive structure is the innovation..."      │
│                                                     │
│ Key metrics: Graduates: Waymo, Verily, Wing...      │
│                                                     │
│ Illustrates: Reward Fast Failure, Ring-Fence...     │
│                                                     │
│ Sources: TechCrunch Disrupt 2025, HBR Podcast...    │
├─────────────────────────────────────────────────────┤
│ 💬 Ask about this case                              │
│ ┌─────────────────────────────────────────────┐     │
│ │                                             │     │
│ └─────────────────────────────────────────────┘     │
│                                        [Ask →]      │
└─────────────────────────────────────────────────────┘
```

- Larger diagram
- Full structured content sections
- Linked design principles (clickable)
- Sources as citations
- Conversation input (see Section below)

#### Design Principle Card (Collapsed)

```
┌─────────────────────────────────────────────────────┐
│ ▣ PROTECTION                                   ☆    │
│   Protect Deviations from Optimization Pressure     │
│   Middle management systematically kills off-...    │
└─────────────────────────────────────────────────────┘
```

- Group badge (color-coded by the 6 groups)
- Title in bold
- One-line insight (truncated)
- Star icon

#### Design Principle Card (Expanded)

- Full insight text
- Manifestations as bullet list
- The test question (highlighted/boxed)
- "Exemplified by:" linked cases (clickable)
- Conversation input

---

### Case & Principle Conversation Interface

Both case cards and design principle cards support interactive Q&A.

**Interaction flow:**
1. User types question in input field
2. System checks if answer exists in current JSON data
3. If yes → responds immediately
4. If no → triggers web research, synthesizes answer
5. New knowledge appended to JSON (`conversations` and `extendedContent`)
6. Conversation history persists on card (collapsible)

**For design principles:** Asking "Can you give me more examples?" may discover new cases → creates new case JSON files and links them.

**Data evolution example:**

```json
{
  "id": "google-x",
  "content": { ... },
  "conversations": [
    {
      "id": "conv-001",
      "question": "How do teams get bonused for killing projects?",
      "answer": "According to Astro Teller in his TechCrunch interview...",
      "source": "TechCrunch Disrupt 2025",
      "addedToContent": true,
      "timestamp": "2026-01-19T14:30:00Z"
    }
  ],
  "extendedContent": {
    "incentiveDetails": "Teams receive bonuses equivalent to what they would have earned if the project succeeded..."
  }
}
```

---

### View 3: Tensions View

Accessed from Stack when 2+ stances are taken.

Shows cross-principle interactions based on user's actual selections:

```
┌─────────────────────────────────────────────────────┐
│ ← Back    TENSIONS IN YOUR ARCHITECTURE             │
├─────────────────────────────────────────────────────┤
│ ⚠️  Locus of Innovation ↔ Measurement Philosophy    │
│                                                     │
│ You selected "Protected Deviation" models (Google X,│
│ Eli Lilly) but haven't defined measurement yet.     │
│                                                     │
│ If you measure productivity, you'll kill the        │
│ protected deviations. Consider: Transformation      │
│ Milestones or Failure Rewards models.               │
│                                        [Explore →]  │
├─────────────────────────────────────────────────────┤
│ ⚠️  Ambidexterity Structure ↔ Resource Allocation   │
│                                                     │
│ Your centralized lab model requires ring-fenced     │
│ budget protection...                                │
│                                        [Explore →]  │
└─────────────────────────────────────────────────────┘
```

- Pulls tension patterns from `tensions.json`
- Only shows tensions relevant to user's selections
- "Explore" links to related principle deep-dive

---

### View 4: Artifact Generator

Accessed from Stack. Compiles all stances into exportable document.

**Generated sections:**
1. **Architecture Summary** — Crystallized stances across principles
2. **Model Choices** — Starred cases with why they were selected
3. **Design Principles Applied** — Starred principles with how they're being applied
4. **Tensions Acknowledged** — From tensions view, with mitigation notes
5. **Open Questions** — Principles still In Progress or Unexplored
6. **Mandates by Role** — Template structure for CEO, P&L heads, Lab leader, etc.
7. **Revisit Triggers** — User-defined or suggested conditions for revisiting

**Export options:**
- View in app
- Copy to clipboard (Markdown)
- Download as Markdown file
- (Future: PDF export)

---

## MVP Scope

### In Scope
1. Stack view with all 8 principles visible
2. Deep-dive view for Principle 4 (Locus of Innovation) with full content
3. Cards for the 15 library cases
4. Cards for the 19 design principles (grouped by 6 categories)
5. Diagram templates (9 types) rendering for case cards
6. Star/unstar interaction
7. Workspace with notes, draft stance, crystallize
8. Status tracking (Unexplored / In Progress / Stance Taken)
9. localStorage persistence

### Deferred to Next Phase
- Conversation interface on cards (requires AI integration)
- Tensions view
- Artifact generator
- Deep-dive content for other 7 principles (marked "Coming Soon")
- PDF export

---

## Technical Implementation Notes

### File Structure

```
/src
  /components
    Stack.tsx
    StackLayer.tsx
    PrincipleRow.tsx
    PrincipleDeepDive.tsx
    CaseCard.tsx
    DesignPrincipleCard.tsx
    Workspace.tsx
    DiagramRenderer.tsx
  /hooks
    useLibrary.ts       # Loads and provides library data
    useUserState.ts     # localStorage state management
  /types
    library.ts          # TypeScript types for library schemas
    userState.ts
  /utils
    relationships.ts    # Derive reverse lookups
  App.tsx

/library
  /framework
    layers.json
    diagramTemplates.json
    principleGroups.json
    tensions.json
  /cases
    *.json
  /designPrinciples
    *.json
```

### Key Design Decisions

1. **Library as static JSON** — No database needed for MVP. Research skill writes directly to JSON files.

2. **Template-based diagrams** — 9 templates cover the 15 cases. New cases specify which template to use.

3. **Relationships derived at runtime** — Cases list their design principles; reverse lookup computed when needed.

4. **localStorage for user state** — Simple, no auth needed. Can migrate to backend later for team collaboration.

5. **Desktop-first** — Target audience uses this in workshop/deep-work settings.

---

## Success Criteria

A CEO should be able to:
1. See the full architecture at a glance
2. Understand what decisions they need to make
3. Dive into any principle and explore relevant cases
4. See what frontier organizations are actually doing
5. Draft their own stance informed by examples
6. Understand tensions with other choices (post-MVP)
7. Feel respected as a sophisticated thinker, not patronized

---

## Open Questions for Implementation

1. **Diagram rendering approach** — SVG components? Canvas? CSS-only?
2. **Card expansion animation** — Smooth expand/collapse or instant?
3. **Auto-save frequency** — Debounce timing for notes/draft stance?
4. **Library loading** — Bundle JSON at build time or fetch at runtime?
