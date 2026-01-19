const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        PageBreak, Header, Footer, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

// === CONFIGURATION ===
const OUTPUT_FILE = 'AI_Organizational_Models_Comprehensive_v6.docx';
const VERSION = '6.0';
const DATE = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long' });

// === STYLING HELPERS ===
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const headerShading = { fill: "1a365d", type: ShadingType.CLEAR };
const altRowShading = { fill: "f7fafc", type: ShadingType.CLEAR };
const highlightShading = { fill: "fef3c7", type: ShadingType.CLEAR }; // yellow highlight for new section

function cell(text, isHeader = false, width = 2000, isAltRow = false, isHighlight = false) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: isHeader ? headerShading : (isHighlight ? highlightShading : (isAltRow ? altRowShading : { fill: "FFFFFF", type: ShadingType.CLEAR })),
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

function sectionHeader(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text, bold: true, size: 32, font: "Arial", color: "1a365d" })]
  });
}

function subHeader(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 150 },
    children: [new TextRun({ text, bold: true, size: 26, font: "Arial", color: "2c5282" })]
  });
}

function para(text) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, size: 22, font: "Arial" })]
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 22, font: "Arial" })]
  });
}

// === DATA: PRODUCT/VENTURE LABS (Named) ===
const productVentureLabs = [
  // Tech Giant Internal Labs
  { company: "Anthropic", labName: "Anthropic Labs", year: "2024", leaders: "Mike Krieger, Ben Mann, Ami Vora", products: "Claude Code ($1B/6mo), MCP, Cowork", model: "Internal Incubator" },
  { company: "Google/Alphabet", labName: "Isomorphic Labs", year: "2021", leaders: "Demis Hassabis", products: "AlphaFold drug discovery, $3B pharma deals", model: "Venture Builder" },
  { company: "Google/Alphabet", labName: "Google X", year: "2010", leaders: "Astro Teller", products: "Waymo, Verily, Wing, Loon, Chronicle", model: "Venture Builder" },
  { company: "Google/Alphabet", labName: "Area 120", year: "2016", leaders: "Various", products: "Byteboard, Checks, Aloud", model: "Internal Incubator" },
  { company: "Google DeepMind", labName: "Automated Materials Lab", year: "2026", leaders: "Demis Hassabis", products: "Gemini robotics for materials science", model: "Internal Incubator" },
  { company: "Microsoft", labName: "CoreAI", year: "2025", leaders: "Jay Parikh", products: "Azure AI Foundry, Copilot Studio", model: "Platform-to-Product" },
  { company: "Microsoft", labName: "MAI Superintelligence", year: "2025", leaders: "Mustafa Suleyman, Karen Simonyan", products: "Bing AI, Copilot, next-gen models", model: "Internal Incubator" },
  { company: "Amazon", labName: "Lab126", year: "2004", leaders: "Yesh Dattatreya", products: "Kindle, Echo, Fire TV, Alexa", model: "Internal Incubator" },
  { company: "Amazon", labName: "AGI SF Lab", year: "2024", leaders: "Peter DeSantis", products: "Nova LLMs, Trainium chips", model: "Internal Incubator" },
  { company: "Meta", labName: "MSL", year: "2025", leaders: "Alexandr Wang, Nat Friedman", products: "Llama, Meta AI, Behemoth", model: "Internal Incubator" },
  { company: "Apple", labName: "Foundation Models", year: "2024", leaders: "Subramanya", products: "Apple Intelligence", model: "Internal Incubator" },
  { company: "NVIDIA", labName: "NVentures + Inception", year: "2016", leaders: "Sid Siddeek", products: "Portfolio: OpenAI, xAI, Anthropic", model: "Venture Builder" },
  { company: "OpenAI", labName: "Grove", year: "2025", leaders: "Sam Altman oversight", products: "Pre-company talent incubator", model: "Internal Incubator" },
  { company: "OpenAI", labName: "Startup Fund + Converge", year: "2021", leaders: "Ian Hathaway", products: "Harvey, Cursor, Figure AI", model: "Venture Builder" },
  // AI Lab Spinoffs
  { company: "Thinking Machines Lab", labName: "TML", year: "2025", leaders: "Mira Murati (ex-OpenAI)", products: "Tinker (LLM fine-tuning)", model: "Spin-off ($12B)" },
  { company: "SSI", labName: "Safe Superintelligence", year: "2024", leaders: "Ilya Sutskever (ex-OpenAI)", products: "Superintelligence research", model: "Spin-off ($32B)" },
  { company: "AMI Labs", labName: "AMI Labs", year: "2025", leaders: "Yann LeCun (leaving Meta)", products: "World models, physics", model: "Spin-off ($3.5B target)" },
  { company: "World Labs", labName: "World Labs", year: "2024", leaders: "Fei-Fei Li, Justin Johnson", products: "Marble, Chisel (3D)", model: "Spin-off ($1B)" },
  { company: "Periodic Labs", labName: "Periodic Labs", year: "2025", leaders: "Liam Fedus, Ekin Cubuk", products: "AI materials science", model: "Spin-off ($300M seed)" },
  { company: "Lila Sciences", labName: "AI Science Factory", year: "2025", leaders: "Andrew Beam, Kenneth Stanley", products: "Scientific superintelligence", model: "Spin-off ($1.3B)" },
  { company: "The Bot Company", labName: "The Bot Company", year: "2025", leaders: "Kyle Vogt (ex-Cruise)", products: "Home robots", model: "Spin-off ($4B+)" },
  { company: "Sierra", labName: "Sierra", year: "2024", leaders: "Bret Taylor, Clay Bavor", products: "Enterprise AI agents", model: "Spin-off" },
  { company: "Reflection AI", labName: "Reflection AI", year: "2024", leaders: "Misha Laskin, Ioannis Antonoglou", products: "Open-source LLMs, MoE", model: "Spin-off ($8B)" },
  { company: "xAI", labName: "xAI/Colossus", year: "2024", leaders: "Elon Musk", products: "Grok models, 1M+ GPU cluster", model: "Spin-off ($20B)" },
  // Venture Studios
  { company: "AI Fund", labName: "AI Fund", year: "2018", leaders: "Andrew Ng", products: "35+ cos: Gaia, SkyFire, Profitmind", model: "Venture Builder ($370M+)" },
  { company: "Kleiner Perkins", labName: "KP Incubation", year: "2010s", leaders: "Joubin Mirzadegan", products: "Glean ($7B), Roadrunner, Windsurf", model: "Venture Builder" },
  { company: "Madrona", labName: "Venture Labs", year: "2016", leaders: "Steve Singh", products: "Otto, Magnify, Strike Graph", model: "Venture Builder" },
  { company: "Allen Institute", labName: "AI2 Incubator", year: "2017", leaders: "Jacob Colker", products: "50+ cos, 24% acquired", model: "Venture Builder ($80M)" },
  // Pharma AI Labs
  { company: "NVIDIA + Eli Lilly", labName: "AI Co-Innovation Lab", year: "2026", leaders: "Joint", products: "1,016 Blackwell GPUs, BioNeMo", model: "Platform-to-Product ($1B)" },
  { company: "Sanofi", labName: "AI Research Factory", year: "2023", leaders: "Paul Hudson", products: "CodonBERT, 7 drug targets, plai app", model: "Internal Incubator" },
  { company: "Roche/Genentech", labName: "gRED Computational Sciences", year: "2020s", leaders: "Aviv Regev", products: "Lab in a Loop, Prescient Design", model: "Internal Incubator" },
  { company: "Eli Lilly", labName: "TuneLab", year: "2025", leaders: "Aliza Apple", products: "AI/ML drug discovery platform", model: "Platform-to-Product" },
  // Corporate Venture Builders
  { company: "Adobe", labName: "Adobe Incubator", year: "2025", leaders: "Employee teams", products: "Firefly Boards, Brand Concierge", model: "Internal Incubator" },
  { company: "Samsung", labName: "C-Lab Inside/Outside", year: "2012", leaders: "Various", products: "912 startups (Edint, GhostPass)", model: "Mixed" },
  { company: "Bosch", labName: "Business Innovations", year: "2025", leaders: "Axel Deniz", products: "Carbon capture, healthcare", model: "Venture Builder" },
  { company: "Porsche Digital", labName: "Forward31", year: "2020", leaders: "Various", products: "Sensigo, Daato, MyEV, Stellar", model: "Venture Builder" },
  { company: "P&G", labName: "P&G Ventures", year: "2015", leaders: "Betsy Bluestone", products: "Zevo, Opte, Kindra, Rae", model: "Venture Builder" },
  { company: "AXA", labName: "Kamet", year: "2016", leaders: "Various", products: "Air Doctor, Akur8, Birdie", model: "Venture Builder" },
  // Consulting Firms
  { company: "BCG", labName: "BCG X", year: "2020s", leaders: "3,000+ team", products: "36,000+ GPTs, venture building", model: "Platform-to-Product" },
  { company: "McKinsey", labName: "QuantumBlack", year: "2015", leaders: "5,000+ team", products: "Horizon, Lilli, GAIL", model: "Platform-to-Product" },
  { company: "Accenture", labName: "AI Labs + GenAI Studios", year: "2020s", leaders: "30,000+ trained", products: "100 agentic AI tools", model: "Platform-to-Product" },
  { company: "Deloitte", labName: "AI Institute + Incubators", year: "2020s", leaders: "Large", products: "500+ client projects", model: "Platform-to-Product" },
  { company: "IBM", labName: "watsonx AI Labs", year: "2023", leaders: "Various", products: "6-12 month co-creation", model: "Internal Incubator" },
];

// === DATA: UNNAMED/INFORMAL AI PRODUCT TEAMS (NEW SECTION) ===
const unnamedLabs = [
  // Consumer Goods
  { company: "Procter & Gamble", structure: "AI Factory + Cross-functional Subgroup", indicators: "ChatPG deployed to 30,000+ users", products: "Internal AI assistants, packaging optimization", pattern: "Leader-Lab-Crowd (implicit)" },
  { company: "Unilever", structure: "Horizon3 Lab + AI Research Hub", indicators: "500+ AI projects running", products: "Predictive maintenance, consumer insights", pattern: "Lab-like moonshot unit" },
  { company: "Colgate-Palmolive", structure: "AI Hub (informal name)", indicators: "4,000 weekly active users, CAIO appointed", products: "AI formulation, marketing automation", pattern: "Central Hub serving BUs" },
  { company: "General Mills", structure: "MillsChat Team", indicators: "20,000 employees using MillsChat", products: "Internal ChatGPT, recipe development AI", pattern: "Massive Crowd adoption" },
  { company: "Clorox", structure: "Digital Core Platform Team", indicators: "90-day AI-to-product cycle", products: "Consumer innovation, marketing AI", pattern: "Fast-cycle Lab development" },
  { company: "Nestle", structure: "AI & Digital Acceleration Team", indicators: "Cookie Coach reached millions", products: "Ruth chatbot, consumer-facing AI", pattern: "Central team ships products" },
  { company: "PepsiCo", structure: "Data & Analytics Transformation", indicators: "Cross-functional AI squads", products: "Demand sensing, route optimization", pattern: "BU-embedded + central" },
  { company: "Kraft Heinz", structure: "Agile Digital Factory", indicators: "Sprint-based AI development", products: "Consumer insights, Not Heinz campaign", pattern: "Factory = Lab model" },
  { company: "Kellogg's", structure: "Digital & Technology Team", indicators: "AI embedded in supply chain", products: "Production optimization, personalization", pattern: "Embedded Lab functions" },
  { company: "Mondelez", structure: "Snacking Future Team", indicators: "AI-driven innovation pipeline", products: "Consumer trend prediction, DTC", pattern: "Innovation team = Lab" },
  // Financial Services
  { company: "Bank of America", structure: "Erica for Employees + AI Enablement", indicators: "95% of workforce using AI tools", products: "Erica extension, code gen, doc processing", pattern: "Massive Crowd; central team" },
  { company: "Citigroup", structure: "AI Champions + Citi Stylus", indicators: "2,000+ AI Champions; 140K+ Stylus users", products: "Enterprise AI tools, trading AI", pattern: "Named Champions = Leaders" },
  { company: "Capital One", structure: "Academic Centers of Excellence", indicators: "PhD talent embedded via ACEs", products: "ML production, fraud models", pattern: "External Lab talent source" },
  { company: "State Farm", structure: "InsurTech Innovation Unit", indicators: "Cross-functional teams, no lab brand", products: "Claims processing, underwriting AI", pattern: "Quiet transformation" },
  { company: "Allstate", structure: "AI Factory (internal only)", indicators: "8-12 person cross-functional teams", products: "Risk models, agent assist, claims AI", pattern: "Factory = explicit Lab term" },
  { company: "Progressive", structure: "Snapshot & AI Telematics Team", indicators: "Deep product integration of AI", products: "Usage-based insurance, Flo AI", pattern: "Embedded product Lab" },
  { company: "American Express", structure: "AI & ML Center", indicators: "Centralized team serving products", products: "Fraud detection, recommendations", pattern: "CoE with Product Lab traits" },
  { company: "Charles Schwab", structure: "Intelligent Investing Team", indicators: "AI embedded in advisor workflows", products: "Schwab Intelligent Portfolios", pattern: "Product team = Lab mandate" },
  // Industrial & Manufacturing
  { company: "3M", structure: "GenAI CoE Action Office", indicators: "Ask 3M deployed; cross-divisional", products: "Ask 3M knowledge assistant, Digital Hub", pattern: "CoE acting as Product Lab" },
  { company: "Honeywell", structure: "Honeywell Connected Enterprise", indicators: "AI embedded in all BUs; Forge platform", products: "Predictive maintenance, building AI", pattern: "Platform = Lab productizing" },
  { company: "Caterpillar", structure: "Cat Digital", indicators: "Sensor data AI products; separate biz", products: "Equipment analytics, autonomous mining", pattern: "Digital unit = shadow Lab" },
  { company: "John Deere", structure: "Technology Innovation Center", indicators: "See & Spray, autonomous tractors", products: "Computer vision, precision ag AI", pattern: "R&D with product mandate" },
  { company: "Emerson", structure: "Digital Transformation Team", indicators: "Process automation AI; no named lab", products: "DeltaV AI, control optimization", pattern: "Engineering-led productization" },
  { company: "Parker Hannifin", structure: "IoT & AI Analytics Team", indicators: "Industrial IoT AI applications", products: "Predictive maintenance, VoC AI", pattern: "Embedded product innovation" },
  { company: "Illinois Tool Works", structure: "Decentralized AI Adoption", indicators: "Each BU running AI pilots", products: "Welding AI, food equipment opt", pattern: "80/20 model applied to AI" },
  { company: "Eaton", structure: "Digital Team (Brightlayer)", indicators: "Electrical sector AI products", products: "Energy management AI, grid opt", pattern: "Platform productization" },
  // Retail & Consumer Services
  { company: "Walmart", structure: "Data Ventures (selling internal AI)", indicators: "Route Optimization sold as SaaS", products: "GoLocal, supply chain licensed external", pattern: "Internal tool -> External product" },
  { company: "Target", structure: "Digital Transformation + Store AI", indicators: "1,800 stores running AI experiments", products: "Inventory AI, pickup optimization", pattern: "Distributed AI = Crowd" },
  { company: "Kroger", structure: "84.51 AI Factory", indicators: "Data science subsidiary; CPG products", products: "Retail media AI, CPG insights platform", pattern: "Subsidiary acts as Lab" },
  { company: "Home Depot", structure: "THD Innovation Hub", indicators: "AI for associate productivity", products: "Orange Apron GPT, inventory opt", pattern: "Named Hub = informal Lab" },
  { company: "Lowe's", structure: "Innovation Labs (low profile)", indicators: "AI experiments across stores", products: "AI customer service, inventory", pattern: "Labs without public profile" },
  { company: "CVS Health", structure: "Digital Transformation Team", indicators: "Pharmacy AI integration", products: "Medication adherence AI, MinuteClinic", pattern: "Health services productization" },
  { company: "Walgreens", structure: "Healthcare & Digital Innovation", indicators: "AI-enabled pharmacy operations", products: "Prescription optimization, health recs", pattern: "Embedded AI in services" },
  // Healthcare
  { company: "UnitedHealth/Optum", structure: "AI Marketplace (external sales)", indicators: "Selling AI to external providers", products: "Clinical decision support, claims AI", pattern: "Internal AI -> marketplace" },
  { company: "HCA Healthcare", structure: "Clinical AI Team", indicators: "186 hospitals; AI systemwide", products: "Sepsis prediction, readmission AI", pattern: "System-wide Crowd adoption" },
  { company: "Kaiser Permanente", structure: "Health Tech Innovation", indicators: "Integrated care AI; no named lab", products: "Care gap identification, pop health", pattern: "Embedded AI in care" },
  { company: "McKesson", structure: "Digital & AI Solutions", indicators: "Distribution AI; pharmaceutical AI", products: "Supply chain opt, pharmacy automation", pattern: "Distribution AI productization" },
  // Media & Entertainment
  { company: "Disney", structure: "OTE (Office of Tech Enablement)", indicators: "Central AI coordination; park opt", products: "Guest experience AI, content recs", pattern: "OTE = Lab without Lab name" },
  { company: "Comcast", structure: "LIFT Labs + AI Everywhere", indicators: "Innovation arm + AI in all products", products: "Xfinity AI, content AI, advertising", pattern: "LIFT = venture function" },
  { company: "Warner Bros Discovery", structure: "Technology & AI Team", indicators: "Streaming AI; content production", products: "Max recommendations, production opt", pattern: "Embedded AI commercialization" },
];

// === DATA: CHIEF AI OFFICERS ===
const caioAppointments = [
  { company: "UBS Group AG", name: "Daniele Magazzeni", year: "Dec 2025", previous: "First CAIO for wealth management" },
  { company: "Commonwealth Bank Australia", name: "Ranil Boteju", year: "2025", previous: "Lloyd's Chief Data & Analytics Officer" },
  { company: "Wells Fargo", name: "Saul Van Beurden (expanded)", year: "Nov 2025", previous: "CEO Consumer/Small Business Banking" },
  { company: "LinkedIn", name: "Deepak Agarwal", year: "2025", previous: "-" },
  { company: "Airbnb", name: "Ahmad Al-Dahle (CTO)", year: "Jan 2026", previous: "Meta generative AI lead, Llama team" },
  { company: "U.S. Cyber Command", name: "Reid Novotny", year: "Nov 2025", previous: "DoD Cyber Force Generation lead" },
  { company: "Department of Defense", name: "Douglas Matty (CDAO)", year: "Apr 2025", previous: "University of Alabama Research Director" },
  { company: "Department of Labor", name: "Mangala Kuppa", year: "June 2025", previous: "Deputy CAIO" },
];

// === KEY INSIGHTS ===
const keyInsights = [
  "Unnamed Lab Structures: Many companies (P&G, BofA, 3M, Walmart) implement Product Lab patterns WITHOUT formal naming - this represents the 'quiet transformation' missed by research focused on named labs.",
  "Leader-Lab-Crowd Pattern: Companies implementing Ethan Mollick's model without using that terminology - look for 'AI Champions' (Leaders), 'AI Factory' (Lab), and enterprise-wide tool adoption (Crowd).",
  "Internal-to-External Path: Classic Product Lab pattern where internal tools become external products: Walmart Route Optimization -> GoLocal, Kroger 84.51 -> CPG Platform, Optum -> AI Marketplace.",
  "Secret Cyborg Indicators: BofA's 95% AI usage, P&G's 30K ChatPG users, General Mills' 20K MillsChat users suggest massive unofficial adoption preceded formal programs.",
  "Spinoff Valuations Soaring: TML ($12B), SSI ($32B), Reflection ($8B), xAI ($20B), The Bot Company ($4B+) - AI talent with product-building mandates commands unprecedented valuations.",
  "Pharma AI Consolidation: Recursion + Exscientia ($688M), NVIDIA + Lilly ($1B), multiple partnership deals signal AI-driven drug discovery industrialization.",
  "Physical AI Emergence: Figure ($2.6B), Boston Dynamics, The Bot Company, Google's Materials Lab, Arm's Physical AI Division - robotics + AI convergence accelerating.",
  "CAIO Role Expansion: 40%+ of Fortune 500 expected to have CAIO by end of 2026; role now encompasses product strategy, not just governance.",
];

// === DOCUMENT GENERATION ===
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
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({
          text: `AI Organizational Models - v${VERSION}`,
          size: 18, font: "Arial", color: "666666"
        })]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "Page ", size: 18, font: "Arial" }),
          new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial" })
        ]
      })] })
    },
    children: [
      // Title page
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ text: "AI ORGANIZATIONAL MODELS", bold: true, size: 48, font: "Arial", color: "1a365d" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
        children: [new TextRun({ text: "Corporate Responses to the AI Transformation", size: 26, font: "Arial", color: "666666" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: `Version ${VERSION} - ${DATE}`, size: 22, font: "Arial", color: "666666" })]
      }),

      // Executive Summary
      sectionHeader("Executive Summary"),
      para(`This comprehensive report catalogs 230+ organizational responses to AI across five distinct models, with special focus on Product/Venture Labs and a NEW section on Unnamed/Informal AI Product Teams - companies implementing lab-like structures without formal branding.`),
      para(""),
      subHeader("Key Statistics"),
      bullet(`${productVentureLabs.length} Named Product/Venture Labs tracked (tech giants, spinoffs, pharma, consulting)`),
      bullet(`${unnamedLabs.length} Unnamed/Informal AI Product Teams identified (consumer goods, financial, industrial, retail, healthcare)`),
      bullet(`${caioAppointments.length} Recent Chief AI Officer appointments (2025-2026)`),
      bullet("Spinoff valuations: TML $12B, SSI $32B, Reflection $8B, xAI $20B, The Bot Company $4B+"),
      bullet("Leader-Lab-Crowd pattern identified at P&G, Clorox, BofA, Citi, Allstate, Disney without using that terminology"),
      para(""),
      para("NEW IN V6: The 'Unnamed/Informal' section addresses the observation that research focusing on formally named labs (Google X, Anthropic Labs) systematically underestimates AI's organizational transformation in traditional companies."),

      new Paragraph({ children: [new PageBreak()] }),

      // Part I: Taxonomy
      sectionHeader("Part I: AI Organizational Model Taxonomy"),
      para("Five distinct models for organizing AI capabilities within enterprises:"),
      para(""),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2000, 2500, 2000, 2860],
        rows: [
          new TableRow({ children: [
            cell("Model", true, 2000),
            cell("Definition", true, 2500),
            cell("Time Horizon", true, 2000),
            cell("Examples", true, 2860),
          ]}),
          new TableRow({ children: [
            cell("1. Research Lab", false, 2000),
            cell("Fundamental research, publishing, breakthroughs", false, 2500),
            cell("3-10 years", false, 2000),
            cell("DeepMind, FAIR, MSR", false, 2860),
          ]}),
          new TableRow({ children: [
            cell("2. Center of Excellence", false, 2000, true),
            cell("Governance, standards, enablement", false, 2500, true),
            cell("6-24 months", false, 2000, true),
            cell("JPMorgan AI CoE, Ford AI", false, 2860, true),
          ]}),
          new TableRow({ children: [
            cell("3. Embedded Teams", false, 2000),
            cell("AI in product/BU teams, no central org", false, 2500),
            cell("Quarterly", false, 2000),
            cell("Tesla AI, Stripe, Netflix", false, 2860),
          ]}),
          new TableRow({ children: [
            cell("4. Hybrid/Hub-and-Spoke", false, 2000, true),
            cell("Central standards + distributed execution", false, 2500, true),
            cell("Mixed", false, 2000, true),
            cell("Most Fortune 500", false, 2860, true),
          ]}),
          new TableRow({ children: [
            cell("5. Product/Venture Lab", false, 2000),
            cell("Commercialize AI into products/businesses", false, 2500),
            cell("6-36 months", false, 2000),
            cell("Anthropic Labs, Google X, BCG X", false, 2860),
          ]}),
        ]
      }),
      para(""),
      para("Product/Venture Lab Sub-Types: (a) Internal Incubator - products absorbed into parent; (b) Venture Builder - spin-offs with independent status; (c) Platform-to-Product - internal capability licensed externally."),

      new Paragraph({ children: [new PageBreak()] }),

      // Part II: Named Product/Venture Labs
      sectionHeader("Part II: Product/Venture Labs (Named)"),
      para(`${productVentureLabs.length} formally branded labs and venture programs with explicit product commercialization mandates.`),
      para(""),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1400, 1600, 700, 1600, 2200, 1860],
        rows: [
          new TableRow({ children: [
            cell("Company", true, 1400),
            cell("Lab/Team Name", true, 1600),
            cell("Year", true, 700),
            cell("Key Leaders", true, 1600),
            cell("Products/Spinoffs", true, 2200),
            cell("Business Model", true, 1860),
          ]}),
          ...productVentureLabs.map((lab, i) => new TableRow({ children: [
            cell(lab.company, false, 1400, i % 2 === 1),
            cell(lab.labName, false, 1600, i % 2 === 1),
            cell(lab.year, false, 700, i % 2 === 1),
            cell(lab.leaders, false, 1600, i % 2 === 1),
            cell(lab.products, false, 2200, i % 2 === 1),
            cell(lab.model, false, 1860, i % 2 === 1),
          ]}))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part III: Unnamed/Informal AI Product Teams (NEW)
      sectionHeader("Part III: Unnamed/Informal AI Product Teams (NEW)"),
      para("Companies implementing Product/Venture Lab patterns WITHOUT formal naming or branding. These represent the 'quiet transformation' - internal reorganization to capture AI opportunities without fanfare, often implementing versions of the 'Leader-Lab-Crowd' model without consciously following that terminology."),
      para(""),
      subHeader("Why This Matters"),
      bullet("Research focused on named labs (Google X, Anthropic Labs) systematically underestimates AI's organizational transformation"),
      bullet("P&G's ChatPG (30,000 users) affects more product decisions than many startup AI labs"),
      bullet("Walmart's internal route optimization AI is now a revenue line item (GoLocal SaaS)"),
      bullet("Bank of America's 95% AI adoption represents more deployed AI than most AI startups"),
      para(""),
      subHeader("Identification Patterns Used"),
      bullet("Internal tool -> External product path (Walmart, Kroger, Optum)"),
      bullet("Leader-Lab-Crowd indicators: AI Champions (Leaders), AI Factory (Lab), 10K+ users (Crowd)"),
      bullet("Cross-functional teams with 90-day product cycles"),
      bullet("CAIO appointed but no named lab (lab function exists under different name)"),
      para(""),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1500, 2200, 2000, 2000, 1660],
        rows: [
          new TableRow({ children: [
            cell("Company", true, 1500),
            cell("Internal Structure", true, 2200),
            cell("Key Indicators", true, 2000),
            cell("Products/Outcomes", true, 2000),
            cell("Pattern Identified", true, 1660),
          ]}),
          ...unnamedLabs.map((lab, i) => new TableRow({ children: [
            cell(lab.company, false, 1500, i % 2 === 1),
            cell(lab.structure, false, 2200, i % 2 === 1),
            cell(lab.indicators, false, 2000, i % 2 === 1),
            cell(lab.products, false, 2000, i % 2 === 1),
            cell(lab.pattern, false, 1660, i % 2 === 1),
          ]}))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part IV: Key Insights
      sectionHeader("Part IV: Key Insights"),
      para("Notable patterns and findings from research across podcasts, SEC filings, earnings calls, and press coverage:"),
      para(""),
      ...keyInsights.map((insight, i) => bullet(`${i + 1}. ${insight}`)),

      new Paragraph({ children: [new PageBreak()] }),

      // Part V: Chief AI Officer Appointments
      sectionHeader("Part V: Chief AI Officer Appointments"),
      para("Recent CAIO appointments (2025-2026) - over 40% of Fortune 500 expected to have a CAIO by end of 2026:"),
      para(""),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2500, 2500, 1500, 2860],
        rows: [
          new TableRow({ children: [
            cell("Company", true, 2500),
            cell("Name", true, 2500),
            cell("Year", true, 1500),
            cell("Previous Role", true, 2860),
          ]}),
          ...caioAppointments.map((caio, i) => new TableRow({ children: [
            cell(caio.company, false, 2500, i % 2 === 1),
            cell(caio.name, false, 2500, i % 2 === 1),
            cell(caio.year, false, 1500, i % 2 === 1),
            cell(caio.previous, false, 2860, i % 2 === 1),
          ]}))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Summary Statistics
      sectionHeader("Summary Statistics"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [6000, 3360],
        rows: [
          new TableRow({ children: [cell("Category", true, 6000), cell("Count", true, 3360)] }),
          new TableRow({ children: [cell("Named Product/Venture Labs", false, 6000), cell(productVentureLabs.length.toString(), false, 3360)] }),
          new TableRow({ children: [cell("Unnamed/Informal AI Product Teams (NEW)", false, 6000, true), cell(unnamedLabs.length.toString(), false, 3360, true)] }),
          new TableRow({ children: [cell("Chief AI Officer Appointments", false, 6000), cell(caioAppointments.length.toString(), false, 3360)] }),
          new TableRow({ children: [cell("Key Insights Documented", false, 6000, true), cell(keyInsights.length.toString(), false, 3360, true)] }),
          new TableRow({ children: [cell("TOTAL CASES", false, 6000), cell((productVentureLabs.length + unnamedLabs.length + caioAppointments.length).toString(), false, 3360)] }),
        ]
      }),
      para(""),
      para("Note: The Unnamed/Informal section represents a methodological expansion - moving beyond named labs to identify companies implementing equivalent organizational patterns without formal branding. This captures the 'quiet transformation' at traditional companies like Clorox, Bank of America, 3M, and Walmart."),
      para(""),
      para(`Last Updated: ${DATE}`),
    ]
  }]
});

// Write file
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT_FILE, buffer);
  console.log(`Document created: ${OUTPUT_FILE}`);
  console.log(`- Named Product/Venture Labs: ${productVentureLabs.length}`);
  console.log(`- Unnamed/Informal AI Product Teams: ${unnamedLabs.length}`);
  console.log(`- CAIO Appointments: ${caioAppointments.length}`);
  console.log(`- Key Insights: ${keyInsights.length}`);
});
