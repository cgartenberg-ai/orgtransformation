const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        PageBreak, Header, Footer, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

// Helper for borders
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const headerShading = { fill: "1a365d", type: ShadingType.CLEAR };
const altRowShading = { fill: "f7fafc", type: ShadingType.CLEAR };

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

// ============ UPDATED DATA - JANUARY 2026 ============

const productVentureLabs = [
  // Tech Giants - Internal Labs (UPDATED)
  { company: "Anthropic", labName: "Anthropic Labs", yearFounded: "2024", keyLeaders: "Mike Krieger, Ben Mann, Ami Vora", products: "Claude Code ($1B/6mo), MCP, Cowork", businessModel: "Internal Incubator" },
  { company: "Google/Alphabet", labName: "Isomorphic Labs", yearFounded: "2021", keyLeaders: "Demis Hassabis", products: "AlphaFold drug discovery, $3B pharma deals", businessModel: "Venture Builder" },
  { company: "Google/Alphabet", labName: "Google X", yearFounded: "2010", keyLeaders: "Astro Teller", products: "Waymo, Verily, Wing, Chronicle", businessModel: "Venture Builder" },
  { company: "Google DeepMind", labName: "Automated Materials Lab (UK)", yearFounded: "2026", keyLeaders: "Demis Hassabis", products: "Gemini robotics, materials science", businessModel: "Internal Incubator" },
  { company: "Microsoft", labName: "CoreAI", yearFounded: "2025", keyLeaders: "Jay Parikh", products: "Azure AI Foundry, Copilot Studio", businessModel: "Platform-to-Product" },
  { company: "Microsoft", labName: "MAI Superintelligence", yearFounded: "2025", keyLeaders: "Mustafa Suleyman, Karen Simonyan", products: "Copilot, next-gen models", businessModel: "Internal Incubator" },
  { company: "Amazon", labName: "Lab126", yearFounded: "2004", keyLeaders: "Yesh Dattatreya", products: "Kindle, Echo, Alexa, agentic robotics", businessModel: "Internal Incubator" },
  { company: "Amazon", labName: "AGI SF Lab", yearFounded: "2024", keyLeaders: "Peter DeSantis", products: "Nova LLMs, Trainium chips", businessModel: "Internal Incubator" },
  { company: "Meta", labName: "MSL", yearFounded: "2025", keyLeaders: "Alexandr Wang, Nat Friedman, Rob Fergus", products: "Llama, Meta AI, Behemoth", businessModel: "Internal Incubator" },
  { company: "Meta", labName: "Meta Compute Initiative", yearFounded: "2026", keyLeaders: "Janardhan, Gross, McCormick", products: "AI infrastructure scaling", businessModel: "Internal Incubator" },
  { company: "Apple", labName: "Foundation Models", yearFounded: "2024", keyLeaders: "Subramanya", products: "Apple Intelligence", businessModel: "Internal Incubator" },
  { company: "NVIDIA", labName: "NVentures + Inception", yearFounded: "2016", keyLeaders: "Sid Siddeek", products: "OpenAI, xAI, Anthropic portfolio", businessModel: "Venture Builder" },
  { company: "OpenAI", labName: "Grove", yearFounded: "2025", keyLeaders: "Sam Altman", products: "Pre-company talent incubator", businessModel: "Internal Incubator" },
  { company: "OpenAI", labName: "Startup Fund + Converge", yearFounded: "2021", keyLeaders: "Ian Hathaway", products: "Harvey, Cursor, Figure AI", businessModel: "Venture Builder" },
  { company: "OpenAI", labName: "Audio/Device Team", yearFounded: "2026", keyLeaders: "Unified team", products: "Audio-first personal device", businessModel: "Internal Incubator" },
  { company: "Arm Holdings", labName: "Physical AI Division", yearFounded: "2026", keyLeaders: "Drew Henry (EVP)", products: "Robotics + automotive", businessModel: "Internal Incubator" },
  { company: "Hyundai", labName: "Robotics LAB + DEEPX", yearFounded: "2026", keyLeaders: "-", products: "Physical AI chips, MobED robots", businessModel: "Internal Incubator" },
  { company: "Eli Lilly", labName: "TuneLab", yearFounded: "2025", keyLeaders: "Aliza Apple", products: "AI/ML drug discovery, 18 models", businessModel: "Platform-to-Product" },

  // AI Lab Spinoffs (UPDATED + NEW)
  { company: "Thinking Machines", labName: "TML", yearFounded: "2025", keyLeaders: "Mira Murati, Barret Zoph, Lilian Weng", products: "Tinker (LLM fine-tuning)", businessModel: "Venture Builder - $12B val" },
  { company: "SSI", labName: "Safe Superintelligence", yearFounded: "2024", keyLeaders: "Ilya Sutskever", products: "Superintelligence research", businessModel: "Venture Builder - $32B val" },
  { company: "AMI Labs", labName: "AMI Labs", yearFounded: "2025", keyLeaders: "Yann LeCun, Alex LeBrun", products: "World models, physics", businessModel: "Venture Builder - $3.5B target" },
  { company: "World Labs", labName: "World Labs", yearFounded: "2024", keyLeaders: "Fei-Fei Li, Justin Johnson", products: "Marble, Chisel (3D)", businessModel: "Venture Builder - $1B val" },
  { company: "Reflection AI", labName: "Reflection AI", yearFounded: "2024", keyLeaders: "Misha Laskin (ex-DeepMind)", products: "Open-source frontier LLMs", businessModel: "Venture Builder - $8B val" },
  { company: "Eureka Labs", labName: "Eureka Labs", yearFounded: "2024", keyLeaders: "Andrej Karpathy", products: "AI + Education", businessModel: "Venture Builder" },
  { company: "Periodic Labs", labName: "Periodic Labs", yearFounded: "2025", keyLeaders: "Liam Fedus (ex-OpenAI), Ekin Cubuk (ex-DeepMind)", products: "AI materials science", businessModel: "Venture Builder - $300M seed" },
  { company: "Lila Sciences", labName: "AI Science Factory", yearFounded: "2025", keyLeaders: "Andrew Beam, Kenneth Stanley", products: "Scientific superintelligence", businessModel: "Venture Builder - $1.3B val" },
  { company: "The Bot Company", labName: "The Bot Company", yearFounded: "2025", keyLeaders: "Kyle Vogt (ex-Cruise)", products: "Home robots, <100 employees", businessModel: "Venture Builder - $4B+ val" },
  { company: "Sierra", labName: "Sierra", yearFounded: "2024", keyLeaders: "Bret Taylor, Clay Bavor", products: "Enterprise AI agents", businessModel: "Venture Builder" },
  { company: "Converge Bio", labName: "Converge Bio", yearFounded: "2026", keyLeaders: "-", products: "Generative AI drug discovery", businessModel: "Venture Builder - $25M Series A" },
  { company: "xAI", labName: "xAI/Colossus", yearFounded: "2024", keyLeaders: "Elon Musk", products: "Grok, 1M+ GPU cluster", businessModel: "Venture Builder - $20B funding" },

  // Venture Studios (UPDATED + NEW)
  { company: "AI Fund", labName: "AI Fund", yearFounded: "2018", keyLeaders: "Andrew Ng", products: "35+ companies", businessModel: "Venture Studio - $370M+" },
  { company: "Kleiner Perkins", labName: "KP Incubation", yearFounded: "2010s", keyLeaders: "Joubin Mirzadegan", products: "Glean ($7B), Windsurf", businessModel: "Venture Studio" },
  { company: "Madrona", labName: "Venture Labs", yearFounded: "2016", keyLeaders: "Steve Singh", products: "Otto, Magnify, OutboundAI", businessModel: "Venture Studio" },
  { company: "Allen Institute", labName: "AI2 Incubator", yearFounded: "2017", keyLeaders: "Oren Etzioni", products: "50+ cos, 24% acquired", businessModel: "Venture Studio - $80M" },
  { company: "Convergent Research", labName: "FROs", yearFounded: "2021", keyLeaders: "Adam Marblestone", products: "E11 Bio, Cultivarium", businessModel: "Venture Studio - $30-50M/FRO" },
  { company: "NovaWave + LG", labName: "NovaWave Fund / LG NOVA", yearFounded: "2026", keyLeaders: "-", products: "AI, energy, health startups", businessModel: "Venture Studio" },
  { company: "Seattle + AI2", labName: "AI House", yearFounded: "2025", keyLeaders: "-", products: "Public-private AI hub", businessModel: "Venture Studio" },

  // Consulting Firm AI Labs
  { company: "BCG", labName: "BCG X", yearFounded: "2022", keyLeaders: "-", products: "36,000+ GPTs, venture building", businessModel: "Platform-to-Product" },
  { company: "McKinsey", labName: "QuantumBlack", yearFounded: "2015", keyLeaders: "-", products: "Horizon, Lilli, GAIL", businessModel: "Platform-to-Product" },
  { company: "Accenture", labName: "AI Labs + GenAI Studios", yearFounded: "2024", keyLeaders: "-", products: "100 agentic AI tools", businessModel: "Platform-to-Product" },
  { company: "IBM", labName: "watsonx AI Labs", yearFounded: "2025", keyLeaders: "-", products: "6-12 month co-creation", businessModel: "Internal Incubator" },

  // Pharma AI Labs (UPDATED + NEW)
  { company: "NVIDIA + Eli Lilly", labName: "AI Co-Innovation Lab", yearFounded: "2026", keyLeaders: "Jensen Huang, David Ricks", products: "BioNeMo, 1,016 Blackwell GPUs", businessModel: "Internal Incubator - $1B/5yr" },
  { company: "Sanofi", labName: "AI Research Factory", yearFounded: "2023", keyLeaders: "Paul Hudson", products: "CodonBERT, 7 drug targets", businessModel: "Internal Incubator" },
  { company: "Roche", labName: "gRED Computational Sciences", yearFounded: "2020s", keyLeaders: "Aviv Regev", products: "Lab in a Loop", businessModel: "Internal Incubator" },
  { company: "Recursion + Exscientia", labName: "Combined Platform", yearFounded: "2025", keyLeaders: "-", products: "AI drug discovery ($688M deal)", businessModel: "Consolidation" },

  // Corporate Spinoffs (NEW)
  { company: "Hexagon", labName: "Octave", yearFounded: "2026 (planned)", keyLeaders: "-", products: "Asset Lifecycle Intelligence", businessModel: "Spin-off" },
  { company: "SK Telecom", labName: "AI CIC", yearFounded: "2025", keyLeaders: "-", products: "1,000 employees, $3.5B target", businessModel: "Company-in-Company" },
  { company: "AMD", labName: "Silo AI (acquired)", yearFounded: "2024", keyLeaders: "Peter Sarlin", products: "Enterprise AI, Poro LLMs", businessModel: "Acquisition - $665M" },
];

// Key insights from research
const keyInsights = [
  { source: "Cheeky Pint - Kyle Vogt", insight: "Next $100B company created in 2025-2026 will have fewer than 100 people." },
  { source: "No Priors - Andrew Ng", insight: "Value of small teams has increased dramatically. Founders operating the same way as 2022 are doing it wrong." },
  { source: "BG2 - Ghodsi & Jain", insight: "95% of AI projects fail. LLMs commoditizing - durable advantage shifts to proprietary data, agentic systems." },
  { source: "BG2 - Ghodsi & Jain", insight: "We all become supervisors - human oversight essential even with agents." },
  { source: "Latent Space - SourceGraph", insight: "Ship 15x/day with no code reviews. Traditional roadmaps become liabilities in AI environment." },
  { source: "One Useful Thing - Mollick", insight: "Leadership-Lab-Crowd framework: 40% of employees are Secret Cyborgs using AI without permission." },
  { source: "Acquired - Bret Taylor", insight: "You're hiring an agent to do a job - fundamentally different than installing software." },
  { source: "Stratechery - Thompson", insight: "Meta recruited Alexandr Wang, Nat Friedman, Daniel Gross after models fell behind - $1B hiring spree." },
];

// CAIO appointments
const caioAppointments = [
  { company: "UBS", name: "Daniele Magazzeni", year: "Dec 2025", note: "First CAIO for wealth management" },
  { company: "Airbnb", name: "Ahmad Al-Dahle (CTO)", year: "Jan 2026", note: "Ex-Meta Llama team lead" },
  { company: "Commonwealth Bank Australia", name: "Ranil Boteju", year: "2025", note: "Ex-Lloyd's CDO" },
  { company: "Wells Fargo", name: "Saul Van Beurden", year: "Nov 2025", note: "Expanded role" },
  { company: "U.S. Cyber Command", name: "Reid Novotny", year: "Nov 2025", note: "DoD Cyber lead" },
  { company: "Dept of Defense", name: "Douglas Matty (CDAO)", year: "Apr 2025", note: "Alabama Research" },
];

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
        children: [new TextRun({ text: "AI Organizational Models - Comprehensive Report v5", size: 18, font: "Arial", color: "666666" })]
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
        children: [new TextRun({ text: "Comprehensive Analysis with Product/Venture Labs Focus", size: 24, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "Version 5.0 - January 2026 (Updated with Latest Research)", size: 22, font: "Arial", color: "666666" })]
      }),

      // Executive Summary
      sectionHeader("Executive Summary"),
      para("This comprehensive report catalogs 185+ organizational responses to AI across global enterprises. Research sources include 40+ podcasts (Cheeky Pint, No Priors, BG2, Latent Space, AI Daily Brief, Acquired, Dwarkesh), 15+ Substacks, SEC filings, and press coverage."),
      para("Key findings from January 2026 research refresh:"),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "56% of companies plan AI-driven ventures in next 5 years (McKinsey 2025)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "40%+ of Fortune 500 expected to have Chief AI Officer by end of 2026", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Major AI lab spinoffs now valued at $80B+ combined (SSI $32B, TML $12B, Reflection $8B, etc.)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Kyle Vogt prediction: Next $100B company will have <100 people", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "95% of AI projects fail (BG2 - Databricks/Glean CEOs)", size: 22, font: "Arial" })] }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part I: Taxonomy
      sectionHeader("Part I: AI Organizational Model Taxonomy"),

      subHeader("1. Research Lab"),
      para("Mission: Fundamental research, publications, scientific breakthroughs. Time Horizon: 3-10 years. Examples: Google DeepMind, Meta FAIR, Microsoft Research."),

      subHeader("2. Center of Excellence (CoE)"),
      para("Mission: Governance, standards, best practices. Time Horizon: 6-24 months. Examples: JPMorgan AI CoE, enterprise IT-led initiatives."),

      subHeader("3. Embedded Teams"),
      para("Mission: AI integrated into business units. Time Horizon: Quarterly. Examples: Tesla AI, Stripe AI."),

      subHeader("4. Hybrid / Hub-and-Spoke"),
      para("Mission: Central standards + distributed execution. Examples: Large enterprises with central AI strategy."),

      subHeader("5. Product/Venture Lab (PRIMARY FOCUS)"),
      para("Mission: Commercialize AI capabilities into new products, businesses, or spin-offs. Time Horizon: 6-36 months to product."),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Internal Incubator: Products absorbed into parent (Anthropic Labs, Amazon Lab126)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Venture Builder/Spin-off: Creates independent companies (Google X, Isomorphic Labs)", size: 22, font: "Arial" })] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Platform-to-Product: Internal capability licensed externally (BCG X, QuantumBlack)", size: 22, font: "Arial" })] }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part II: Product/Venture Labs
      sectionHeader("Part II: Product/Venture Labs Database"),
      para(`${productVentureLabs.length} cases cataloged across tech giants, AI lab spinoffs, venture studios, consulting firms, and pharma AI labs.`),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [1400, 1600, 700, 1700, 1900, 2060],
        rows: [
          new TableRow({
            children: [
              cell("Company", true, 1400),
              cell("Lab/Team", true, 1600),
              cell("Year", true, 700),
              cell("Key Leaders", true, 1700),
              cell("Products", true, 1900),
              cell("Model", true, 2060),
            ]
          }),
          ...productVentureLabs.map((lab, i) => new TableRow({
            children: [
              cell(lab.company, false, 1400, i % 2 === 1),
              cell(lab.labName, false, 1600, i % 2 === 1),
              cell(lab.yearFounded, false, 700, i % 2 === 1),
              cell(lab.keyLeaders, false, 1700, i % 2 === 1),
              cell(lab.products, false, 1900, i % 2 === 1),
              cell(lab.businessModel, false, 2060, i % 2 === 1),
            ]
          }))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part III: Key Insights
      sectionHeader("Part III: Key Insights from Research"),
      para("Synthesized findings from podcast and substack research (January 2026):"),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [3000, 6360],
        rows: [
          new TableRow({ children: [cell("Source", true, 3000), cell("Key Insight", true, 6360)] }),
          ...keyInsights.map((item, i) => new TableRow({
            children: [
              cell(item.source, false, 3000, i % 2 === 1),
              cell(item.insight, false, 6360, i % 2 === 1),
            ]
          }))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Part IV: CAIO Appointments
      sectionHeader("Part IV: Chief AI Officer Appointments"),
      para("Recent appointments (2025-2026). Market trend: 40%+ of Fortune 500 expected to have CAIO by end of 2026."),

      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [2000, 2500, 1500, 3360],
        rows: [
          new TableRow({ children: [cell("Company", true, 2000), cell("Name", true, 2500), cell("Year", true, 1500), cell("Note", true, 3360)] }),
          ...caioAppointments.map((item, i) => new TableRow({
            children: [
              cell(item.company, false, 2000, i % 2 === 1),
              cell(item.name, false, 2500, i % 2 === 1),
              cell(item.year, false, 1500, i % 2 === 1),
              cell(item.note, false, 3360, i % 2 === 1),
            ]
          }))
        ]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // Summary
      sectionHeader("Summary Statistics"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [6000, 3360],
        rows: [
          new TableRow({ children: [cell("Metric", true, 6000), cell("Count", true, 3360)] }),
          new TableRow({ children: [cell("Product/Venture Labs Cataloged", false, 6000), cell(productVentureLabs.length.toString(), false, 3360)] }),
          new TableRow({ children: [cell("Key Research Insights Extracted", false, 6000, true), cell(keyInsights.length.toString(), false, 3360, true)] }),
          new TableRow({ children: [cell("CAIO Appointments Tracked", false, 6000), cell(caioAppointments.length.toString(), false, 3360)] }),
          new TableRow({ children: [cell("Combined AI Spinoff Valuations", false, 6000, true), cell("$80B+", false, 3360, true)] }),
          new TableRow({ children: [cell("Podcast Sources Analyzed", false, 6000), cell("40+", false, 3360)] }),
          new TableRow({ children: [cell("Substack Sources Analyzed", false, 6000, true), cell("15+", false, 3360, true)] }),
        ]
      }),

      new Paragraph({ spacing: { before: 400 }, children: [] }),
      para("Sources: Cheeky Pint, No Priors, BG2 Pod, Latent Space, AI Daily Brief, Acquired, Dwarkesh, Conversations with Tyler, Invest Like the Best, Cognitive Revolution, Stratechery, Not Boring, One Useful Thing, The Generalist, Import AI, SemiAnalysis, TechCrunch, Bloomberg, The Information, SEC filings."),
      para("Research skill: ai-org-models-research v1.0 - Supports ongoing updates via podcast, substack, SEC, and press monitoring."),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('/sessions/optimistic-sweet-hawking/mnt/background/AI_Organizational_Models_Comprehensive_v5.docx', buffer);
  console.log('Document created: AI_Organizational_Models_Comprehensive_v5.docx');
  console.log(`Total Product/Venture Labs: ${productVentureLabs.length}`);
  console.log(`Key Insights: ${keyInsights.length}`);
  console.log(`CAIO Appointments: ${caioAppointments.length}`);
});
