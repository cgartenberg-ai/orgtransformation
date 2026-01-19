# Word Document Generator Template

JavaScript template for generating the comprehensive AI Organizational Models report using docx-js.

## Prerequisites

```bash
npm install -g docx
```

## Generator Script Template

Save as `create_report.js` and run with `node create_report.js`:

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        PageBreak, Header, Footer, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

// === CONFIGURATION ===
const OUTPUT_FILE = 'AI_Organizational_Models_Comprehensive.docx';
const VERSION = '4.0';
const DATE = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long' });

// === STYLING HELPERS ===
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

// === DATA ===
// Update these arrays with new cases

const productVentureLabs = [
  // Format: { company, labName, yearFounded, keyLeaders, products, businessModel }
  // Add new cases here...
];

const traditionalModels = {
  "Technology": [
    // Format: { company, unit, model, leader, initiative }
  ],
  "Financial Services": [],
  "Healthcare/Pharma": [],
  "Automotive/Manufacturing": [],
  "Retail/Consumer": [],
};

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
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
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
        spacing: { after: 400 },
        children: [new TextRun({ text: `Version ${VERSION} - ${DATE}`, size: 22, font: "Arial", color: "666666" })]
      }),

      // Add sections here...
      sectionHeader("Executive Summary"),
      para("This comprehensive report catalogs 200+ organizational responses to AI..."),

      new Paragraph({ children: [new PageBreak()] }),

      // Part I: Taxonomy
      sectionHeader("Part I: AI Organizational Model Taxonomy"),
      // ...

      // Part II: Product/Venture Labs table
      sectionHeader("Part II: Product/Venture Labs"),
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

      // Part III: Traditional models by sector
      // ...

      // Summary statistics
      sectionHeader("Summary Statistics"),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [6000, 3360],
        rows: [
          new TableRow({ children: [cell("Metric", true, 6000), cell("Count", true, 3360)] }),
          new TableRow({ children: [
            cell("Total Product/Venture Labs", false, 6000),
            cell(productVentureLabs.length.toString(), false, 3360)
          ] }),
        ]
      }),
    ]
  }]
});

// Write file
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT_FILE, buffer);
  console.log(`Document created: ${OUTPUT_FILE}`);
});
```

## Key Points

1. **Always set page size** - US Letter: 12240 x 15840 DXA
2. **Table widths must match** - columnWidths array AND individual cell widths
3. **Use ShadingType.CLEAR** - never SOLID for backgrounds
4. **Add cell margins** - 80/120 for readable padding
5. **Use alternating row colors** - improves readability

## Updating the Document

1. Update the data arrays with new cases
2. Run `node create_report.js`
3. Output file will be created in current directory
