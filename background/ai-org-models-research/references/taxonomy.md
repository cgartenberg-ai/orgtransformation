# AI Organizational Model Taxonomy

Five distinct organizational models for corporate AI initiatives, with detailed definitions and classification criteria.

## Table of Contents
1. [Model 1: Research Lab](#model-1-research-lab)
2. [Model 2: Center of Excellence (CoE)](#model-2-center-of-excellence-coe)
3. [Model 3: Embedded Teams](#model-3-embedded-teams)
4. [Model 4: Hybrid / Hub-and-Spoke](#model-4-hybrid--hub-and-spoke)
5. [Model 5: Product/Venture Lab](#model-5-productventure-lab)
6. [Classification Decision Tree](#classification-decision-tree)
7. [Comparison Matrix](#comparison-matrix)

---

## Model 1: Research Lab

### Definition
Dedicated unit focused on fundamental AI research, publishing academic papers, and achieving scientific breakthroughs. Operates with long time horizons and measures success through research impact rather than immediate commercial returns.

### Characteristics
| Attribute | Description |
|-----------|-------------|
| **Mission** | Fundamental research, scientific breakthroughs |
| **Time Horizon** | 3-10 years |
| **Success Metrics** | Publications, citations, breakthrough discoveries |
| **Reporting** | Often to CTO or Chief Scientist |
| **Funding** | R&D budget, long-term investment |
| **Talent** | PhD researchers, research scientists |

### Key Indicators
- Publishes at top AI conferences (NeurIPS, ICML, ICLR)
- Employs research scientists with academic backgrounds
- Has "Research" or "Lab" in official name
- Operates semi-independently from product teams
- Long publication pipeline (6-18 months)

### Canonical Examples
- **Google DeepMind** (Demis Hassabis)
- **Meta FAIR** (Rob Fergus)
- **Microsoft Research** (Various)
- **IBM Research**
- **Baidu Research**

---

## Model 2: Center of Excellence (CoE)

### Definition
Centralized unit providing AI governance, standards, best practices, and internal consulting services. Focuses on enabling other business units to adopt AI rather than building products directly.

### Characteristics
| Attribute | Description |
|-----------|-------------|
| **Mission** | Governance, standards, enablement |
| **Time Horizon** | 6-24 months |
| **Success Metrics** | Adoption rates, compliance, cost savings |
| **Reporting** | Often to CIO or CDO |
| **Funding** | IT/Digital budget |
| **Talent** | ML engineers, data scientists, program managers |

### Key Indicators
- Creates AI policies and guidelines
- Runs internal AI training programs
- Reviews/approves AI projects across company
- Maintains shared AI platforms and tools
- Tracks AI adoption metrics

### Canonical Examples
- **JPMorgan AI CoE**
- **Walmart AI CoE**
- **Ford AI Center**
- **Shell AI CoE**
- **Unilever AI CoE**

---

## Model 3: Embedded Teams

### Definition
AI capabilities distributed directly into business units or product teams. No central AI organization; each team owns its AI development end-to-end.

### Characteristics
| Attribute | Description |
|-----------|-------------|
| **Mission** | Product-specific AI features |
| **Time Horizon** | Quarterly sprints |
| **Success Metrics** | Product KPIs, feature launches |
| **Reporting** | To BU/Product leadership |
| **Funding** | BU P&L |
| **Talent** | ML engineers embedded in product teams |

### Key Indicators
- AI team members sit within product/BU teams
- No separate "AI" org chart
- Product managers own AI roadmaps
- Tight integration with engineering sprints
- Success measured by product metrics

### Canonical Examples
- **Tesla AI** (embedded in Autopilot, Optimus)
- **Stripe AI** (embedded in Radar, fraud)
- **Netflix** (recommendations team)
- **Spotify** (personalization)
- **Uber** (pricing, matching)

---

## Model 4: Hybrid / Hub-and-Spoke

### Definition
Combination of central AI strategy/policy with distributed execution. Central team sets standards and provides shared services; business units execute with autonomy.

### Characteristics
| Attribute | Description |
|-----------|-------------|
| **Mission** | Central standards + distributed execution |
| **Time Horizon** | Mixed (strategic + tactical) |
| **Success Metrics** | Both central and BU KPIs |
| **Reporting** | Matrix (dotted line to central, solid to BU) |
| **Funding** | Shared (central platform + BU projects) |
| **Talent** | Central platform team + embedded practitioners |

### Key Indicators
- Central AI platform team exists
- BU teams have "dotted line" to central
- Shared infrastructure/tools
- Central governance, distributed building
- Regular cross-BU AI syncs

### Canonical Examples
- **Most Fortune 500 companies**
- **Large banks** (central risk AI + BU applications)
- **Healthcare systems** (central standards + department AI)
- **Retail conglomerates**

---

## Model 5: Product/Venture Lab

### Definition
Internal team focused on commercializing AI capabilities into new products, businesses, or spin-off companies. Operates with startup-like autonomy but parent company resources.

### Characteristics
| Attribute | Description |
|-----------|-------------|
| **Mission** | Commercialize AI into products/businesses |
| **Time Horizon** | 6-36 months to product, potential for spin-off |
| **Success Metrics** | Products launched, revenue, valuations |
| **Reporting** | To CEO or Chief Product Officer |
| **Funding** | Venture-style (milestones) or R&D budget |
| **Talent** | Product managers, engineers, entrepreneurs |

### Sub-Types

#### 5a. Internal Incubator
Products absorbed into parent company's portfolio.

**Indicators:**
- Products stay under parent brand
- Team integrates with existing BUs after launch
- Success = product adoption within company
- Examples: Anthropic Labs → Claude Code, Adobe Incubator → Firefly

#### 5b. Venture Builder / Spin-off Factory
Creates independent companies that may IPO or be acquired.

**Indicators:**
- Spin-offs get independent entity status
- External funding rounds
- Separate branding/leadership
- Examples: Google X → Waymo, Isomorphic Labs

#### 5c. Platform-to-Product
Internal capability licensed/sold externally.

**Indicators:**
- Started as internal tool
- Now offered as product/service to others
- Generates external revenue
- Examples: BCG X, McKinsey QuantumBlack, AWS (from Amazon internal)

### Key Indicators for Any Product/Venture Lab
- "Zero to one" language in descriptions
- Product managers alongside researchers
- Revenue or valuation targets
- Startup-like team structure (3-10 people initially)
- Demo-driven development
- CEO/CPO oversight (not CTO)

### Canonical Examples
- **Anthropic Labs** (Mike Krieger) - Internal Incubator
- **Google X** (Astro Teller) - Venture Builder
- **Isomorphic Labs** (Demis Hassabis) - Venture Builder
- **BCG X** - Platform-to-Product
- **OpenAI Grove** - Internal Incubator
- **Amazon Lab126** - Internal Incubator
- **Samsung C-Lab** - Mixed (Inside + Outside programs)

---

## Classification Decision Tree

```
START: Does the unit publish academic research as primary output?
│
├─ YES → Is research commercialized within 2 years typically?
│        ├─ YES → Model 5: Product/Venture Lab (Research → Product)
│        └─ NO → Model 1: Research Lab
│
└─ NO → Does a central AI team exist?
         │
         ├─ NO → Model 3: Embedded Teams
         │
         └─ YES → Does central team BUILD products or ENABLE others?
                  │
                  ├─ ENABLE → Model 2: Center of Excellence
                  │
                  └─ BUILD → Are outputs new products/companies?
                             │
                             ├─ YES → Model 5: Product/Venture Lab
                             │        └─ Do products spin out? → 5b. Venture Builder
                             │        └─ Stay in parent? → 5a. Internal Incubator
                             │        └─ Licensed externally? → 5c. Platform-to-Product
                             │
                             └─ NO → Is execution distributed to BUs?
                                      ├─ YES → Model 4: Hybrid
                                      └─ NO → Model 2: CoE (heavy-touch)
```

---

## Comparison Matrix

| Attribute | Research Lab | CoE | Embedded | Hybrid | Product/Venture Lab |
|-----------|--------------|-----|----------|--------|---------------------|
| **Primary Output** | Papers, breakthroughs | Standards, enablement | Product features | Both | Products, companies |
| **Time Horizon** | 3-10 years | 6-24 months | Quarterly | Mixed | 6-36 months |
| **Success Metric** | Citations | Adoption | Product KPIs | Mixed | Revenue, valuation |
| **Autonomy** | High | Medium | Low | Medium | Very High |
| **Risk Tolerance** | High | Low | Medium | Medium | Very High |
| **Typical Size** | 50-500 | 10-50 | 5-20/team | Varies | 3-50 |
| **Reporting** | CTO/Chief Scientist | CIO/CDO | BU Head | Matrix | CEO/CPO |

---

## Classification Tips

### Red Flags for Misclassification

**Don't confuse Research Lab with Product/Venture Lab:**
- Research Labs prioritize publications over products
- Product/Venture Labs prioritize shipping over publishing

**Don't confuse CoE with Hybrid:**
- CoEs don't build products directly
- Hybrid models have both central AND distributed builders

**Don't confuse Embedded with Hybrid:**
- Embedded has NO central AI org
- Hybrid has central standards/platform team

### When Classification is Unclear
1. Look at team composition (researchers vs. product managers)
2. Check reporting structure (CTO vs. CPO vs. BU)
3. Examine outputs (papers vs. products vs. guidelines)
4. Review success metrics (citations vs. revenue vs. adoption)
5. Ask: "What would success look like in 2 years?"

---

## Identifying Unnamed/Informal Product Labs

### The Problem: Hidden Lab Structures

Many companies implement Product/Venture Lab patterns **without formal naming or branding**. These represent the "quiet transformation" - internal reorganization to capture AI opportunities without fanfare. Traditional research focusing on named labs (Google X, Anthropic Labs) **misses the majority of enterprise AI transformation**.

### Key Indicators of Unnamed Lab Structures

Look for these patterns even when no "lab" or "innovation hub" name exists:

#### 1. Internal AI Tool → External Product Path
- Internal productivity tool gets productized
- SaaS offering of internally-developed AI
- Examples: Walmart Route Optimization → GoLocal, Kroger 84.51° → CPG Platform

#### 2. Leader-Lab-Crowd Pattern (Implicit)
Even without using Ethan Mollick's terminology:
- **"Leaders"**: AI Champions, AI Ambassadors, AI Evangelists, "Power Users"
- **"Lab"**: Central AI team, AI Factory, Digital Core, Innovation Hub, AI Enablement
- **"Crowd"**: Enterprise-wide tool deployment (10,000+ users), AI adoption metrics

#### 3. Cross-Functional AI Teams with Product Mandates
- Small teams (8-12 people) from multiple functions
- 90-day or quarterly AI-to-product cycles
- Sprint-based AI development
- Demo-driven approach

#### 4. "Secret Cyborg" Indicators
Signs that informal AI adoption preceded formal programs:
- Sudden high adoption rates (e.g., "95% of workforce using AI")
- Enterprise ChatGPT equivalents with massive organic adoption
- Policy formalization after widespread grassroots use

### Search Patterns for Finding Unnamed Labs

```
# Job postings that suggest Product Lab structure
"AI Product Manager" + [Company] (not "AI Researcher")
"AI Engineer" + "product" + [Company]
"AI/ML" + "commercialization" + [Company]

# News patterns
[Company] + "AI tool" + "employees" + "rolled out"
[Company] + "AI" + "internal" + "selling" OR "licensing"
[Company] + "AI" + "factory" OR "hub" OR "acceleration"

# Executive language
[CEO Name] + "AI" + "products" (not "AI research")
[Company] + "AI transformation" + "new products"
[Company] earnings call + "AI revenue" OR "AI products"

# Partnership patterns
[Company] + "white-label AI" OR "AI licensing"
[Company] + "API" + "AI" + "partners"
```

### Sector-Specific Patterns

#### Consumer Goods (Clorox, P&G, Unilever pattern)
- Look for: "Digital Core", "AI Factory", "ChatGPT for [Company]"
- Key indicator: Internal tool deployed to 5,000+ employees
- Revenue indicator: AI-optimized product formulations, marketing AI

#### Financial Services (BofA, Citi pattern)
- Look for: "AI Champions", "AI Accelerator", "AI Enablement"
- Key indicator: % of workforce using AI tools
- Revenue indicator: AI-powered customer products (not just internal efficiency)

#### Industrial (3M, Caterpillar pattern)
- Look for: "Digital business unit", "Connected Enterprise", "IoT platform"
- Key indicator: Sensor data AI productized externally
- Revenue indicator: Predictive maintenance as a service

#### Retail (Walmart, Kroger pattern)
- Look for: Data subsidiary (like 84.51°), "Route optimization", "Retail media"
- Key indicator: Internal logistics AI sold to competitors
- Revenue indicator: AI-powered services for CPG partners

### Questions to Identify Unnamed Labs

1. **"Is there an internal AI tool used by >10,000 employees?"**
   - If yes → Lab-like development capability exists

2. **"Do they sell AI capabilities externally that started internally?"**
   - If yes → Platform-to-Product Lab pattern

3. **"Is there a named 'AI Champion' or 'AI Ambassador' program?"**
   - If yes → Leader-Lab-Crowd structure (implicit)

4. **"Have they announced CAIO but no named lab?"**
   - If yes → Lab function likely exists under different name

5. **"Do earnings calls mention 'AI products' or 'AI revenue'?"**
   - If yes → Product Lab function exists (implicit or explicit)

### Why This Matters

The named labs (Google X, Anthropic Labs) get media coverage, but **unnamed lab structures at traditional companies may represent the larger economic impact**:

- P&G's ChatPG (30,000 users) affects more product decisions than many startup AI labs
- Walmart's internal AI (route optimization) is now a revenue line item
- Bank of America's 95% AI adoption represents more deployed AI than most AI startups

Research focused only on named labs **systematically underestimates** AI's organizational transformation in the economy.
