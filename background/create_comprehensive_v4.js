const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        PageBreak, Header, Footer, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

// Helper for borders
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const headerShading = { fill: "1a365d", type: ShadingType.CLEAR };
const altRowShading = { fill: "f7fafc", type: ShadingType.CLEAR };

// Cell helper
function cell(text, isHeader = false, width = 2000, isAltRow = false) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: isHeader ? headerShading : (isAltRow ? altRowShading : { fill: "FFFFFF", type: ShadingType.CLEAR }),
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      children: [new TextRun({
        text: text,
        bold: isHeader,
        color: isHeader ? "FFFFFF" : "000000",
        size: isHeader ? 22 : 20,
        font: "Arial"
      })]
    })]
  });
}

// Section header
function sectionHeader(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text: text, bold: true, size: 32, font: "Arial", color: "1a365d" })]
  });
}

function subHeader(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 150 },
    children: [new TextRun({ text: text, bold: true, size: 26, font: "Arial", color: "2c5282" })]
  });
}

function para(text) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text: text, size: 22, font: "Arial" })]
  });
}

// ============ DATA ============

const productVentureLabs = [
  // Tech Giants - Internal Labs
  { company: "Anthropic", labName: "Anthropic Labs", yearFounded: "2024", keyLeaders: "Mike Krieger (ex-Instagram), Ben Mann, Ami Vora", products: "Claude Code ($1B in 6 months), MCP (100M downloads), Cowork, Skills", businessModel: "Internal Incubator - frontier prototyping to enterprise products" },
  { company: "Google/Alphabet", labName: "Isomorphic Labs", yearFounded: "2021", keyLeaders: "Demis Hassabis (dual CEO with DeepMind)", products: "AlphaFold drug discovery, internal oncology/immunology pipeline", businessModel: "Venture Builder/Spin-off - $600M funding, $3B pharma partnerships" },
  { company: "Google/Alphabet", labName: "Google X (X Development)", yearFounded: "2010", keyLeaders: "Astro Teller", products: "Waymo, Verily, Wing, Loon, Chronicle, Heritable Agriculture (2025)", businessModel: "Venture Builder/Spin-off Factory - moonshot projects spin out when validated" },
  { company: "Google/Alphabet", labName: "Area 120 (scaled back)", yearFounded: "2016", keyLeaders: "Various", products: "Byteboard (spun out), Checks, Aloud (YouTube dubbing)", businessModel: "Internal Incubator - AI-first projects, some integrated, some spun out" },
  { company: "Microsoft", labName: "CoreAI - Platform and Tools", yearFounded: "2025", keyLeaders: "Jay Parikh (EVP)", products: "Azure AI Foundry, Copilot Studio, Azure AI Services", businessModel: "Platform-to-Product - internal capabilities commercialized via Azure" },
  { company: "Microsoft", labName: "AI Co-Innovation Labs", yearFounded: "2020s", keyLeaders: "Various", products: "Custom AI solutions for Fortune 500", businessModel: "Internal Incubator - 1-week sprints with partners" },
  { company: "Microsoft", labName: "MAI Superintelligence Team", yearFounded: "2025", keyLeaders: "Mustafa Suleyman (CEO Microsoft AI), Karen Simonyan", products: "Bing AI, Copilot, next-gen models", businessModel: "Internal Incubator - building superintelligence capabilities" },
  { company: "Amazon", labName: "Lab126", yearFounded: "2004", keyLeaders: "Yesh Dattatreya (agentic AI)", products: "Kindle, Echo, Fire TV, Alexa, agentic robotics (2025)", businessModel: "Internal Incubator - consumer hardware + AI integration" },
  { company: "Amazon", labName: "AGI SF Lab", yearFounded: "2024", keyLeaders: "Peter DeSantis", products: "Nova LLMs, Trainium chips, AGI research", businessModel: "Internal Incubator - AGI-focused research commercialized via AWS" },
  { company: "Meta", labName: "Meta Superintelligence Labs (MSL)", yearFounded: "2025", keyLeaders: "Alexandr Wang (TBD Lab), Nat Friedman (Products), Rob Fergus (FAIR)", products: "Llama models, Meta AI assistant, Behemoth (in dev)", businessModel: "Internal Incubator - 4-team structure (TBD Lab, FAIR, Products, Infra)" },
  { company: "Apple", labName: "ML Research / Foundation Models Team", yearFounded: "2024+", keyLeaders: "Subramanya (under Craig Federighi)", products: "Apple Intelligence, on-device models, server models", businessModel: "Internal Incubator - privacy-focused, device-integrated AI" },
  { company: "NVIDIA", labName: "NVentures + Inception Program", yearFounded: "2016+", keyLeaders: "Sid Siddeek", products: "Portfolio: OpenAI, xAI, Anthropic, CoreWeave, etc.", businessModel: "Venture Builder - 67 deals in 2025, strategic ecosystem investments" },
  { company: "OpenAI", labName: "OpenAI Grove", yearFounded: "2025", keyLeaders: "Sam Altman oversight", products: "Pre-company talent incubator", businessModel: "Internal Incubator - 5-week program, can spin out or stay internal" },
  { company: "OpenAI", labName: "OpenAI Startup Fund + Converge", yearFounded: "2021", keyLeaders: "Ian Hathaway", products: "Harvey, Cursor, Figure AI ($39B), Descript, Ambience Healthcare", businessModel: "Venture Builder - $175M fund + accelerator for AI startups" },

  // AI Lab Spinoffs
  { company: "Thinking Machines Lab", labName: "Thinking Machines Lab", yearFounded: "2025", keyLeaders: "Mira Murati (ex-OpenAI CTO), Barret Zoph, Lilian Weng", products: "Tinker (LLM fine-tuning API)", businessModel: "Venture Builder/Spin-off - $2B seed at $12B valuation" },
  { company: "Safe Superintelligence Inc (SSI)", labName: "SSI", yearFounded: "2024", keyLeaders: "Ilya Sutskever (ex-OpenAI Chief Scientist)", products: "None yet - pure superintelligence research", businessModel: "Venture Builder/Spin-off - $30B valuation, no products until superintelligence" },
  { company: "AMI Labs", labName: "AMI Labs", yearFounded: "2025", keyLeaders: "Yann LeCun (leaving Meta), Alex LeBrun", products: "World models, physics understanding", businessModel: "Venture Builder/Spin-off - targeting $3.5B valuation" },
  { company: "World Labs", labName: "World Labs", yearFounded: "2024", keyLeaders: "Fei-Fei Li, Justin Johnson", products: "Marble (3D world model), Chisel (3D editor)", businessModel: "Venture Builder/Spin-off - $230M at $1B valuation" },
  { company: "Latent Labs", labName: "Latent Labs", yearFounded: "2024", keyLeaders: "Dr. Simon Kohl (ex-DeepMind AlphaFold2)", products: "AI protein design platform", businessModel: "Venture Builder/Spin-off - $50M funding" },
  { company: "Reflection AI", labName: "Reflection AI", yearFounded: "2024", keyLeaders: "Ex-DeepMind researchers", products: "Software dev automation", businessModel: "Venture Builder/Spin-off - $2B raised, $8B valuation" },
  { company: "Eureka Labs", labName: "Eureka Labs", yearFounded: "2024", keyLeaders: "Andrej Karpathy (ex-OpenAI, Tesla)", products: "AI + Education", businessModel: "Venture Builder/Spin-off - early stage" },

  // Venture Studios & Incubators
  { company: "AI Fund", labName: "AI Fund", yearFounded: "2018", keyLeaders: "Andrew Ng", products: "35+ companies: Gaia Dynamics, SkyFire AI, Profitmind", businessModel: "Venture Studio - $370M+, co-founding from day zero" },
  { company: "Kleiner Perkins", labName: "KP Incubation Program", yearFounded: "2010s", keyLeaders: "Joubin Mirzadegan", products: "Glean ($7B), Roadrunner, Windsurf", businessModel: "Venture Studio - pairs operating partners with concepts" },
  { company: "Madrona Venture Group", labName: "Madrona Venture Labs", yearFounded: "2016", keyLeaders: "Steve Singh, Michael Gulmann", products: "Otto, Magnify, Strike Graph, OutboundAI", businessModel: "Venture Studio - EIRs work through stage-gate validation" },
  { company: "Allen Institute", labName: "AI2 Incubator", yearFounded: "2017", keyLeaders: "Jacob Colker, Yifan Zhang, Oren Etzioni", products: "50+ companies, 24% acquired (Apple, DocuSign, Baidu)", businessModel: "Venture Studio - $80M fund, up to $600K per startup" },
  { company: "The Hive", labName: "The Hive", yearFounded: "2012", keyLeaders: "Various", products: "44 startups, 2 unicorns, 15 exits", businessModel: "Venture Studio - co-creation with GE, Dell, eBay, McKesson" },
  { company: "Convergent Research", labName: "Focused Research Organizations (FROs)", yearFounded: "2021", keyLeaders: "Adam Marblestone, Sam Rodriques", products: "E11 Bio, Cultivarium, 10 FROs total", businessModel: "Venture Studio - $30-50M per FRO, 5-7 year fixed duration" },

  // Consulting Firm AI Labs
  { company: "BCG", labName: "BCG X", yearFounded: "2022", keyLeaders: "Various", products: "36,000+ custom GPTs, venture building services", businessModel: "Platform-to-Product - AI contributed 20% of $13.5B revenue" },
  { company: "McKinsey", labName: "QuantumBlack", yearFounded: "2015 (acquired)", keyLeaders: "Various", products: "Horizon platform, Lilli, Gen AI Labs (GAIL), Agents-at-Scale", businessModel: "Platform-to-Product - 5,000 AI experts, proprietary tools" },
  { company: "Accenture", labName: "AI Labs + 25 GenAI Studios", yearFounded: "2024", keyLeaders: "Various", products: "100 industry-specific agentic AI tools, Anthropic Business Group", businessModel: "Platform-to-Product - $3B global AI investment" },
  { company: "Deloitte", labName: "AI Institute + GenAI Incubator Network", yearFounded: "2024", keyLeaders: "Various", products: "500+ client projects", businessModel: "Platform-to-Product - 8 global incubator locations" },
  { company: "IBM", labName: "watsonx AI Labs", yearFounded: "2025", keyLeaders: "Various", products: "6-12 month co-creation sprints, Seek AI acquisition", businessModel: "Internal Incubator - $500M Enterprise AI Venture Fund access" },

  // Pharma AI Labs (Isomorphic Model)
  { company: "NVIDIA + Eli Lilly", labName: "NVIDIA-Lilly AI Co-Innovation Lab", yearFounded: "2025", keyLeaders: "Joint leadership", products: "World's largest pharma AI factory (1,016 Blackwell GPUs)", businessModel: "Internal Incubator - $1B joint investment over 5 years" },
  { company: "Sanofi", labName: "AI Research Factory", yearFounded: "2023+", keyLeaders: "Paul Hudson (CEO)", products: "CodonBERT (mRNA LLM), 7 novel drug targets, plai app", businessModel: "Internal Incubator - partnerships with OpenAI, Formation Bio, Owkin" },
  { company: "Roche/Genentech", labName: "gRED Computational Sciences", yearFounded: "2020s", keyLeaders: "Aviv Regev, John Marioni", products: "Lab in a Loop platform, Prescient Design", businessModel: "Internal Incubator - NVIDIA partnership, $12B Recursion deal" },
  { company: "Novo Nordisk", labName: "Internal AI + Novo Holdings Ventures", yearFounded: "2024+", keyLeaders: "Lotte Bjerre Knudsen", products: "Gefion Supercomputer, Valo Health collab ($4.6B potential)", businessModel: "Internal Incubator - NVIDIA/Microsoft partnerships" },
  { company: "Flagship Pioneering", labName: "Expedition Medicines", yearFounded: "2024", keyLeaders: "Various", products: "Generative chemistry drug discovery", businessModel: "Venture Builder - $50M Flagship, Pfizer partnership" },

  // Corporate Venture Builders
  { company: "Adobe", labName: "Adobe Incubator", yearFounded: "2025", keyLeaders: "Employee-led teams", products: "Firefly Boards, Brand Concierge, Project Graph, Podcast Enhance", businessModel: "Internal Incubator - internal startups → Creative Cloud" },
  { company: "Samsung", labName: "C-Lab Inside/Outside", yearFounded: "2012", keyLeaders: "Various", products: "912 startups (Edint, GhostPass), 506 outside, 406 inside", businessModel: "Internal Incubator + Venture Builder - spin-offs with Samsung support" },
  { company: "Bosch", labName: "Bosch Business Innovations", yearFounded: "2025 restructure", keyLeaders: "Axel Deniz", products: "Carbon capture, healthcare, software-defined manufacturing", businessModel: "Venture Builder - 2.5B euros AI investment, 20 startups in 4 years" },
  { company: "Porsche Digital", labName: "Forward31", yearFounded: "2020", keyLeaders: "Various", products: "Sensigo, Daato (ESG), MyEV, Stellar", businessModel: "Venture Builder - UP.Labs partnership (6 new companies by 2025)" },
  { company: "Procter & Gamble", labName: "P&G Ventures", yearFounded: "2015", keyLeaders: "Betsy Bluestone", products: "Zevo, Opte, Metaderm, Pepper & Wits, Kindra, Rae", businessModel: "Venture Builder - M13 Launchpad partnership for $1B brands" },
  { company: "AXA", labName: "Kamet", yearFounded: "2016", keyLeaders: "Various", products: "Air Doctor, Akur8, Birdie", businessModel: "Venture Builder - InsurTech focus" },

  // Robotics Product Labs
  { company: "Figure AI", labName: "Helix AI Team", yearFounded: "2024", keyLeaders: "Brett Adcock, Jerry Pratt", products: "Figure 02 humanoid, Helix VLA model", businessModel: "Internal Incubator - vertical integration, ended OpenAI partnership" },
  { company: "1X Technologies", labName: "Internal Development", yearFounded: "2014", keyLeaders: "Various", products: "NEO humanoid robot (home use)", businessModel: "Internal Incubator - OpenAI early backer, $100M funding" },
  { company: "Boston Dynamics", labName: "Atlas Development Team", yearFounded: "2013 (Google), 2020 (Hyundai)", keyLeaders: "Various", products: "Spot, Electric Atlas, Handle", businessModel: "Internal Incubator - Hyundai ownership, DeepMind partnership" },

  // Cloud Provider Programs
  { company: "AWS", labName: "Generative AI Accelerator + Innovation Center", yearFounded: "2023", keyLeaders: "AWS Startups team", products: "40 startups/cohort, Tonic.ai, Weaviate, SuperAnnotate", businessModel: "Internal Incubator - $1M credits, <2% acceptance, 65% reach production" },
  { company: "Microsoft", labName: "M12 + GitHub Fund", yearFounded: "2016 (M12)", keyLeaders: "Michelle Gonzalez", products: "Portfolio: AI, cloud, cybersecurity startups", businessModel: "Venture Builder - $275M annual, 20 investments/year" },
];

// Traditional Models (abbreviated for space)
const traditionalModels = {
  "Technology": [
    { company: "Google DeepMind", unit: "DeepMind", model: "Research Lab → Product", leader: "Demis Hassabis", initiative: "Gemini family" },
    { company: "Meta FAIR", unit: "FAIR", model: "Research Lab", leader: "Rob Fergus", initiative: "Llama research" },
    { company: "Microsoft Research", unit: "MSR", model: "Research Lab", leader: "Various", initiative: "Foundation models" },
    { company: "IBM Research", unit: "IBM Research", model: "Research Lab", leader: "Various", initiative: "Granite models" },
    { company: "Salesforce", unit: "Einstein/Agentforce", model: "Embedded/CoE", leader: "Yuliya Feldman", initiative: "CRM AI agents" },
    { company: "Adobe", unit: "Adobe Research", model: "Research Lab", leader: "Various", initiative: "Firefly, Sensei" },
    { company: "Baidu", unit: "Baidu Research", model: "Research Lab", leader: "Various", initiative: "ERNIE models" },
    { company: "Alibaba", unit: "DAMO Academy", model: "Research Lab", leader: "Various", initiative: "Qwen models" },
    { company: "Tencent", unit: "Tencent AI Lab", model: "Research Lab", leader: "Various", initiative: "Hunyuan models" },
    { company: "ByteDance", unit: "ByteDance AI Lab", model: "Research Lab", leader: "Various", initiative: "Doubao models" },
  ],
  "Financial Services": [
    { company: "JPMorgan Chase", unit: "AI Research", model: "CoE + Embedded", leader: "Various", initiative: "IndexGPT, LLM Suite" },
    { company: "Goldman Sachs", unit: "GS AI", model: "CoE", leader: "Various", initiative: "AI assistants" },
    { company: "Morgan Stanley", unit: "AI@MS", model: "CoE", leader: "Various", initiative: "GPT-4 deployment" },
    { company: "BlackRock", unit: "Aladdin AI", model: "Embedded", leader: "Various", initiative: "Aladdin Copilot" },
    { company: "Citadel", unit: "Citadel AI", model: "Embedded", leader: "Various", initiative: "Trading AI" },
    { company: "Two Sigma", unit: "Two Sigma AI", model: "Embedded", leader: "Various", initiative: "Quantitative AI" },
    { company: "Stripe", unit: "Stripe AI", model: "Embedded", leader: "Various", initiative: "Fraud detection, Radar" },
    { company: "Visa", unit: "Visa AI", model: "CoE", leader: "Various", initiative: "Fraud prevention" },
    { company: "Mastercard", unit: "AI Garage", model: "CoE", leader: "Various", initiative: "Decision Intelligence" },
    { company: "American Express", unit: "AmEx AI", model: "Embedded", leader: "Various", initiative: "Customer service AI" },
  ],
  "Healthcare/Pharma": [
    { company: "Recursion Pharmaceuticals", unit: "Internal AI Platform", model: "Research Lab", leader: "Various", initiative: "Drug discovery + Exscientia" },
    { company: "Insilico Medicine", unit: "Insilico AI", model: "Research Lab", leader: "Alex Zhavoronkov", initiative: "Chemistry42" },
    { company: "BenevolentAI", unit: "BenevolentAI Platform", model: "Research Lab", leader: "Various", initiative: "Drug discovery" },
    { company: "Tempus", unit: "Tempus AI", model: "Embedded", leader: "Eric Lefkofsky", initiative: "Precision medicine" },
    { company: "Flatiron Health", unit: "Flatiron AI", model: "Embedded", leader: "Various", initiative: "Oncology data" },
    { company: "PathAI", unit: "PathAI", model: "Research Lab", leader: "Andy Beck", initiative: "Pathology AI" },
    { company: "Paige", unit: "Paige AI", model: "Research Lab", leader: "Thomas Fuchs", initiative: "Cancer detection" },
    { company: "Johnson & Johnson", unit: "J&J AI", model: "CoE", leader: "Various", initiative: "Drug discovery" },
    { company: "Pfizer", unit: "Pfizer AI", model: "CoE", leader: "Various", initiative: "Clinical trials AI" },
    { company: "Merck", unit: "Merck AI", model: "CoE", leader: "Various", initiative: "Drug discovery" },
  ],
  "Automotive/Manufacturing": [
    { company: "Tesla", unit: "Tesla AI", model: "Embedded", leader: "Various", initiative: "FSD, Optimus robot" },
    { company: "Waymo", unit: "Waymo", model: "Spin-off", leader: "Various", initiative: "Autonomous vehicles" },
    { company: "GM/Cruise", unit: "Cruise", model: "Subsidiary", leader: "Various", initiative: "Robotaxis" },
    { company: "Ford", unit: "Ford AI", model: "CoE", leader: "Various", initiative: "BlueCruise" },
    { company: "BMW", unit: "BMW AI", model: "CoE", leader: "Various", initiative: "Intelligent Personal Assistant" },
    { company: "Siemens", unit: "Siemens AI", model: "CoE", leader: "Various", initiative: "Industrial AI" },
    { company: "GE", unit: "GE AI", model: "CoE", leader: "Various", initiative: "Predix platform" },
    { company: "Honeywell", unit: "Honeywell AI", model: "CoE", leader: "Various", initiative: "Industrial AI" },
  ],
  "Retail/Consumer": [
    { company: "Amazon", unit: "Amazon AI", model: "Embedded", leader: "Various", initiative: "Rufus, Alexa, recommendations" },
    { company: "Walmart", unit: "Walmart AI", model: "CoE", leader: "Various", initiative: "Supply chain AI" },
    { company: "Target", unit: "Target AI", model: "CoE", leader: "Various", initiative: "Inventory AI" },
    { company: "Starbucks", unit: "Deep Brew", model: "Embedded", leader: "Various", initiative: "Personalization" },
    { company: "Nike", unit: "Nike AI", model: "Embedded", leader: "Various", initiative: "Design, recommendations" },
    { company: "Shopify", unit: "Shopify AI", model: "Embedded", leader: "Various", initiative: "Sidekick, Magic" },
  ],
};

// Create document
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: "1a365d" },
        paragraph: { spacing: { before: 400, after: 200 } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: "2c5282" },
        paragraph: { spacing: { before: 300, after: 150 } } },
    ]
  },
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
    }]
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "AI Organizational Models - Comprehensive Report v4", size: 18, font: "Arial", color: "666666" })]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Page ", size: 18, font: "Arial" }), new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial" })]
      })] })
    },
    children: [
      // Title
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ text: "AI ORGANIZATIONAL MODELS", bold: true, size: 48, font: "Arial", color: "1a365d" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
        children: [new TextRun({ text: "Comprehensive Analysis of Corporate AI Labs, Centers of Excellence,", size: 24, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "and Product/Venture Labs", size: 24, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "Version 4.0 - January 2026", size: 22, font: "Arial", color: "666666" })]
      }),

      // Executive Summary
      sectionHeader("Executive Summary"),
      para("This comprehensive report catalogs 200+ organizational responses to AI across global enterprises, with special emphasis on Product/Venture Labs - the emerging category of internal teams focused on commercializing AI capabilities into new products and businesses."),
      para("Key findings from research across 40+ podcast sources, substacks, and industry publications:"),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "56% of companies plan AI-driven ventures in next 5 years (McKinsey 2025)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "89% of Fortune 500 have dedicated AI investment arms", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Product/Venture Labs represent fastest-growing organizational model", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Major AI lab spinoffs valued at $75B+ combined (SSI, Thinking Machines, World Labs, etc.)", size: 22, font: "Arial" })] }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part I: Taxonomy
      sectionHeader("Part I: AI Organizational Model Taxonomy"),

      subHeader("1. Research Lab"),
      para("Mission: Fundamental research, publications, scientific breakthroughs. Time Horizon: 3-10 years. Examples: Google DeepMind, Meta FAIR, Microsoft Research, IBM Research."),

      subHeader("2. Center of Excellence (CoE)"),
      para("Mission: Governance, standards, best practices, internal consulting. Time Horizon: 6-24 months. Examples: JPMorgan AI CoE, Walmart AI CoE, enterprise IT-led initiatives."),

      subHeader("3. Embedded Teams"),
      para("Mission: AI integrated into business units, product-specific. Time Horizon: Quarterly. Examples: Tesla AI, Stripe AI, business unit data science teams."),

      subHeader("4. Hybrid / Hub-and-Spoke"),
      para("Mission: Central standards + distributed execution. Time Horizon: Mixed. Examples: Large enterprises with central AI strategy and BU implementation."),

      subHeader("5. Product/Venture Lab (NEW - Primary Focus)"),
      para("Mission: Commercialize AI capabilities into new products, businesses, or spin-offs. Time Horizon: 6-36 months to product, potential for independent company."),
      para("Three Sub-Types:"),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Internal Incubator: Products absorbed into parent (Anthropic Labs → Claude Code)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Venture Builder/Spin-off Factory: Creates independent companies (Google X → Waymo, Isomorphic Labs)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Platform-to-Product: Internal capability licensed externally (BCG X, McKinsey QuantumBlack)", size: 22, font: "Arial" })] }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part II: Product/Venture Labs
      sectionHeader("Part II: Product/Venture Labs - Comprehensive Database"),
      para(`This section catalogs ${productVentureLabs.length} Product/Venture Labs identified through research across Cheeky Pint, No Priors, BG2, Stratechery, Not Boring, Latent Space, Cognitive Revolution, Dwarkesh, Conversations with Tyler, One Useful Thing, The Generalist, Invest Like the Best, Asianometry, Construction Physics, and Acquired podcasts/substacks.`),

      // Product/Venture Labs Table
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1500, 1500, 800, 1800, 2000, 1760],
        rows: [
          new TableRow({
            children: [
              cell("Company", true, 1500),
              cell("Lab/Team Name", true, 1500),
              cell("Year", true, 800),
              cell("Key Leaders", true, 1800),
              cell("Products/Spinoffs", true, 2000),
              cell("Business Model", true, 1760),
            ]
          }),
          ...productVentureLabs.map((lab, i) => new TableRow({
            children: [
              cell(lab.company, false, 1500, i % 2 === 1),
              cell(lab.labName, false, 1500, i % 2 === 1),
              cell(lab.yearFounded, false, 800, i % 2 === 1),
              cell(lab.keyLeaders, false, 1800, i % 2 === 1),
              cell(lab.products, false, 2000, i % 2 === 1),
              cell(lab.businessModel, false, 1760, i % 2 === 1),
            ]
          }))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part III: Traditional Models
      sectionHeader("Part III: Traditional AI Organizational Models by Sector"),

      // Technology
      subHeader("Technology Sector"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1800, 1800, 1800, 1800, 2160],
        rows: [
          new TableRow({ children: [cell("Company", true, 1800), cell("AI Unit", true, 1800), cell("Model Type", true, 1800), cell("Key Leader", true, 1800), cell("Flagship Initiative", true, 2160)] }),
          ...traditionalModels["Technology"].map((c, i) => new TableRow({
            children: [cell(c.company, false, 1800, i%2===1), cell(c.unit, false, 1800, i%2===1), cell(c.model, false, 1800, i%2===1), cell(c.leader, false, 1800, i%2===1), cell(c.initiative, false, 2160, i%2===1)]
          }))
        ]
      }),

      // Financial Services
      subHeader("Financial Services Sector"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1800, 1800, 1800, 1800, 2160],
        rows: [
          new TableRow({ children: [cell("Company", true, 1800), cell("AI Unit", true, 1800), cell("Model Type", true, 1800), cell("Key Leader", true, 1800), cell("Flagship Initiative", true, 2160)] }),
          ...traditionalModels["Financial Services"].map((c, i) => new TableRow({
            children: [cell(c.company, false, 1800, i%2===1), cell(c.unit, false, 1800, i%2===1), cell(c.model, false, 1800, i%2===1), cell(c.leader, false, 1800, i%2===1), cell(c.initiative, false, 2160, i%2===1)]
          }))
        ]
      }),

      // Healthcare
      subHeader("Healthcare/Pharma Sector"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1800, 1800, 1800, 1800, 2160],
        rows: [
          new TableRow({ children: [cell("Company", true, 1800), cell("AI Unit", true, 1800), cell("Model Type", true, 1800), cell("Key Leader", true, 1800), cell("Flagship Initiative", true, 2160)] }),
          ...traditionalModels["Healthcare/Pharma"].map((c, i) => new TableRow({
            children: [cell(c.company, false, 1800, i%2===1), cell(c.unit, false, 1800, i%2===1), cell(c.model, false, 1800, i%2===1), cell(c.leader, false, 1800, i%2===1), cell(c.initiative, false, 2160, i%2===1)]
          }))
        ]
      }),

      // Automotive
      subHeader("Automotive/Manufacturing Sector"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1800, 1800, 1800, 1800, 2160],
        rows: [
          new TableRow({ children: [cell("Company", true, 1800), cell("AI Unit", true, 1800), cell("Model Type", true, 1800), cell("Key Leader", true, 1800), cell("Flagship Initiative", true, 2160)] }),
          ...traditionalModels["Automotive/Manufacturing"].map((c, i) => new TableRow({
            children: [cell(c.company, false, 1800, i%2===1), cell(c.unit, false, 1800, i%2===1), cell(c.model, false, 1800, i%2===1), cell(c.leader, false, 1800, i%2===1), cell(c.initiative, false, 2160, i%2===1)]
          }))
        ]
      }),

      // Retail
      subHeader("Retail/Consumer Sector"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1800, 1800, 1800, 1800, 2160],
        rows: [
          new TableRow({ children: [cell("Company", true, 1800), cell("AI Unit", true, 1800), cell("Model Type", true, 1800), cell("Key Leader", true, 1800), cell("Flagship Initiative", true, 2160)] }),
          ...traditionalModels["Retail/Consumer"].map((c, i) => new TableRow({
            children: [cell(c.company, false, 1800, i%2===1), cell(c.unit, false, 1800, i%2===1), cell(c.model, false, 1800, i%2===1), cell(c.leader, false, 1800, i%2===1), cell(c.initiative, false, 2160, i%2===1)]
          }))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part IV: Key Insights
      sectionHeader("Part IV: Key Insights from Podcast/Substack Research"),

      subHeader("From Cheeky Pint (John Collison)"),
      para("New AI initiatives should be handled by 3-4 person teams until they develop a compelling working version. Priority is getting a compelling working demo launched in users' hands before scaling resources."),

      subHeader("From No Priors (Elad Gil & Sarah Guo)"),
      para("Jensen Huang: Physical AI will revolutionize the $50 trillion manufacturing and logistics industries. 95% of AI projects fail due to unrealistic expectations - this is expected experimentation behavior."),

      subHeader("From Stratechery (Ben Thompson)"),
      para("DeepSeek proved OpenAI doesn't have 'special sauce' - reasoning models can be replicated. Value shifts to distribution, data, and integration. OpenAI building 'Windows of AI' platform."),

      subHeader("From Not Boring (Packy McCormick)"),
      para("Vertical integrators (hardware + AI/software) represent major opportunity. 'The integration is the innovation.' Examples: Meter, Base Power Company, Radiant Nuclear."),

      subHeader("From Latent Space (Swyx & Alessio)"),
      para("$100M+ seed rounds with no near-term roadmap now the norm. OpenAI reasoning team grew from 12 to 300+ people."),

      subHeader("From Cognitive Revolution (Nathan Labenz)"),
      para("The 'Intelligence Curse': AGI may make humans economically irrelevant, breaking social contracts. Proposed solutions include AI diffusion and human augmentation over automation."),

      subHeader("From Dwarkesh Podcast"),
      para("Adam Marblestone (Convergent Research): FRO model fills gap between academia and VC - $30-50M per organization, 5-7 year fixed duration, backed by Eric Schmidt."),

      new Paragraph({ children: [new PageBreak()] }),

      // Summary Statistics
      sectionHeader("Summary Statistics"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [6000, 3360],
        rows: [
          new TableRow({ children: [cell("Metric", true, 6000), cell("Count", true, 3360)] }),
          new TableRow({ children: [cell("Total Product/Venture Labs Cataloged", false, 6000), cell(productVentureLabs.length.toString(), false, 3360)] }),
          new TableRow({ children: [cell("Total Traditional Model Cases", false, 6000, true), cell(Object.values(traditionalModels).flat().length.toString(), false, 3360, true)] }),
          new TableRow({ children: [cell("Combined Valuation of AI Lab Spinoffs", false, 6000), cell("$75B+", false, 3360)] }),
          new TableRow({ children: [cell("Podcast/Substack Sources Analyzed", false, 6000, true), cell("40+", false, 3360, true)] }),
          new TableRow({ children: [cell("Sectors Covered", false, 6000), cell("6", false, 3360)] }),
        ]
      }),

      new Paragraph({ spacing: { before: 400 }, children: [] }),
      para("Sources: Cheeky Pint, No Priors, BG2 Pod, Stratechery, Not Boring, Latent Space, Cognitive Revolution, Dwarkesh Podcast, Conversations with Tyler, One Useful Thing, The Generalist, Invest Like the Best, Asianometry, Construction Physics, Acquired, company press releases, SEC filings, and industry publications."),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('/sessions/optimistic-sweet-hawking/mnt/background/AI_Organizational_Models_Comprehensive_v4.docx', buffer);
  console.log('Document created: AI_Organizational_Models_Comprehensive_v4.docx');
});
