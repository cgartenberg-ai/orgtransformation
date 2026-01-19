---
name: ai-org-models-research
description: |
  Research and maintain a comprehensive database of corporate AI organizational models, with emphasis on Product/Venture Labs. Use this skill when:
  (1) Updating the AI Organizational Models document with new cases
  (2) Researching new Product/Venture Labs, AI spinoffs, or corporate AI initiatives
  (3) Searching podcasts, substacks, SEC filings, or press for AI organizational news
  (4) Adding new cases to the existing database
  (5) Refreshing sources for the latest AI org model developments
  MANDATORY TRIGGERS: AI organizational models, Product/Venture Labs, corporate AI labs, AI spinoffs, update AI research, refresh AI cases, AI CoE, AI incubator
---

# AI Organizational Models Research Skill

Maintain and update a comprehensive database of corporate AI organizational responses, with special focus on **Product/Venture Labs** - internal teams that commercialize AI capabilities into new products and businesses.

## Quick Reference

| Task | Action |
|------|--------|
| Update document | Run research across sources, update cases, regenerate docx |
| Add new case | Categorize by model type, add to appropriate section |
| Research specific company | Search SEC filings, investor days, podcasts, press |
| Refresh all sources | Run parallel searches across all source categories |

## Taxonomy (5 Models)

See `references/taxonomy.md` for full definitions. Summary:

1. **Research Lab** - Fundamental research, 3-10 year horizon (DeepMind, FAIR)
2. **Center of Excellence** - Governance, standards, 6-24 months (JPMorgan AI CoE)
3. **Embedded Teams** - BU-integrated, quarterly cycles (Tesla AI, Stripe)
4. **Hybrid/Hub-and-Spoke** - Central + distributed (enterprise standard)
5. **Product/Venture Lab** - Commercialize AI into products/businesses, 6-36 months
   - Internal Incubator (Anthropic Labs → Claude Code)
   - Venture Builder/Spin-off Factory (Google X → Waymo)
   - Platform-to-Product (BCG X, QuantumBlack)

## Research Workflow

### 1. Parallel Source Search

Run searches across ALL source categories simultaneously:

```
PODCASTS: Cheeky Pint, No Priors, BG2, Dwarkesh, Conversations with Tyler,
          Invest Like the Best, Latent Space, Cognitive Revolution, Acquired

SUBSTACKS: Stratechery, Not Boring, One Useful Thing, The Generalist,
           Import AI, TheSequence, Construction Physics, Asianometry

SEC/INVESTOR: 10-K filings, investor day transcripts, earnings calls
              Search: "[Company] AI strategy", "[Company] AI investment"

PRESS: TechCrunch, The Information, Bloomberg, Reuters, WSJ
       Search: "AI lab", "AI incubator", "AI spinoff", "AI venture"
```

### 2. Case Extraction Template

For each new case, extract:

| Field | Description |
|-------|-------------|
| Company | Parent company name |
| Lab/Team Name | Official name of AI unit |
| Year Founded | When established |
| Key Leaders | Names + titles (CEO, Chief Scientist, etc.) |
| Products/Spinoffs | What they've built or launched |
| Business Model | Which of the 5 model types + sub-type if Product/Venture Lab |
| Funding/Investment | If known (valuations, investment amounts) |
| Source | Where information came from |

### 3. Update Document

After research, regenerate the Word document using the JavaScript generator. See `references/docx-generator.md` for the full script template.

## Source Database

See `references/sources.md` for the complete categorized source list including:
- 40+ podcast episodes with specific guests and topics
- 15+ substacks with key articles
- SEC filing search patterns
- Press outlet guidelines

## Case Database

See `references/cases.md` for the full enumerated case list (230+ cases) organized by:
- Product/Venture Labs - Named (75+ cases)
- **Unnamed/Informal AI Product Teams (45+ cases)** - Companies implementing lab-like structures without formal naming
- Traditional Models by Sector (Technology, Financial Services, Healthcare, Automotive, Retail)

## Key Search Patterns

### Finding Product/Venture Labs
```
"[Company] labs" + "product" OR "commercialize" OR "venture"
"[Company] incubator" + AI
"[Company] spin-off" + AI
"internal startup" + [Company] + AI
"zero to one" + [Company] + AI
```

### Finding AI Leaders
```
"Chief AI Officer" + [Company]
"Head of AI" + [Company]
"AI Research" + "Director" + [Company]
LinkedIn: title:"Chief AI Officer" OR title:"VP AI"
```

### SEC Filing Patterns
```
10-K: "artificial intelligence" + "research and development"
10-K: "machine learning" + "capital expenditure"
Proxy: "AI" + "executive compensation"
8-K: "AI" + "strategic initiative" OR "partnership"
```

### Finding UNNAMED/Informal AI Product Labs (NEW)

**CRITICAL**: Many companies implement Product Lab patterns WITHOUT naming them. Use these patterns to find hidden lab structures:

```
# Internal tool commercialization signals
"[Company] AI" + "rolled out" + "employees" (internal deployment)
"[Company] AI" + "licensing" OR "white-label" OR "SaaS" (external sales)
"[Company] internal" + "AI tool" + "now selling"

# Leader-Lab-Crowd indicators (implicit)
"[Company] AI Champions" OR "AI Ambassadors" OR "AI Accelerators"
"[Company] AI Factory" OR "Digital Core" OR "AI Hub"
"[Company]" + "% workforce" + "AI" OR "using AI tools"

# Cross-functional AI team signals
"[Company] AI" + "cross-functional" + "product"
"[Company] AI" + "90 days" OR "sprint" + "product"

# Sector-specific patterns
CONSUMER GOODS: "[Clorox/P&G/Unilever] ChatGPT" OR "[Company] AI assistant" + employees
FINANCIAL: "[BofA/Citi/Allstate] AI" + "workforce" OR "all employees"
INDUSTRIAL: "[3M/Caterpillar/Deere] digital" + "AI" + "products" OR "services"
RETAIL: "[Walmart/Kroger/Target] AI" + "internal" + "external" OR "partners"

# CAIO without named lab (strong indicator)
"Chief AI Officer" + [Company] (then check for named lab - if none, informal structure exists)
```

**Key Questions to Ask:**
1. Does the company have 10,000+ employees using an internal AI tool? → Lab capability exists
2. Are they selling AI capabilities that started internally? → Platform-to-Product pattern
3. Is there an AI Champions/Ambassadors program? → Leader-Lab-Crowd structure
4. CAIO appointed but no named lab? → Informal lab function exists

## Output Document Structure

The comprehensive Word document should contain:

1. **Executive Summary** - Key statistics, trends
2. **Part I: Taxonomy** - 5 model definitions with examples
3. **Part II: Product/Venture Labs (Named)** - Detailed table of formally branded labs
4. **Part III: Unnamed/Informal AI Product Teams** - Companies with lab-like structures but no formal naming
5. **Part IV: Traditional Models by Sector** - Tables by industry
6. **Part V: Key Insights** - Notable findings from sources
7. **Summary Statistics** - Counts, valuations, trends

## Updating Frequency

Recommend quarterly updates to capture:
- New AI lab announcements
- Leadership changes
- Spinoff/IPO events
- Funding rounds
- Strategic pivots
- **Unnamed lab patterns** - Internal tool deployments, AI Champions programs, internal-to-external productization

## Special Focus: Unnamed Lab Structures

The research on named labs (Google X, Anthropic Labs) systematically **underestimates** AI's organizational transformation. Many companies implement lab-like structures without formal naming:

| Company Type | Look For | Example |
|--------------|----------|---------|
| Consumer Goods | "ChatGPT for [Company]", "AI Factory", "Digital Core" | P&G ChatPG (30K users), Clorox Digital Core |
| Financial | "AI Champions", "% using AI", "AI Accelerators" | BofA (95% AI usage), Citi (2,000 AI Champions) |
| Industrial | "Digital business", "Connected Enterprise", "IoT AI" | 3M Ask 3M, Cat Digital |
| Retail | Data subsidiary, "internal tool" → SaaS | Walmart GoLocal, Kroger 84.51° |
| Healthcare | "AI Marketplace", internal clinical AI sold externally | Optum AI Marketplace |

See `references/taxonomy.md` for full identification guidance.
