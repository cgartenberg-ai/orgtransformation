import { getAllSpecimens } from "@/lib/data/specimens";
import { STRUCTURAL_MODELS } from "@/lib/types/taxonomy";
import type { StructuralModel } from "@/lib/types/specimen";

let cachedPrompt: string | null = null;

export async function buildSystemPrompt(): Promise<string> {
  if (cachedPrompt) return cachedPrompt;

  const specimens = await getAllSpecimens();
  const active = specimens.filter((s) => s.meta.status !== "Archived");

  // Build model descriptions
  const modelDescriptions = ([1, 2, 3, 4, 5, 6, 7, 8, 9] as StructuralModel[])
    .map((m) => {
      const info = STRUCTURAL_MODELS[m];
      return `M${m} — ${info.name}: ${info.description}\n   ${info.characteristics}`;
    })
    .join("\n\n");

  // Build compressed specimen registry
  const specimenRegistry = active
    .map((s) => {
      const model = s.classification.structuralModel
        ? `M${s.classification.structuralModel}`
        : "unclassified";
      return `${s.id} | ${s.name} | ${model} | ${s.classification.orientation} | ${s.habitat.industry} | ${s.title}`;
    })
    .join("\n");

  // Contingency dimensions
  const contingencies = `
Five Contingency Dimensions:
1. Regulatory Intensity (High/Medium/Low) — How heavily regulated the industry is
2. Time to Obsolescence (Fast/Medium/Slow) — How quickly products/services become outdated
3. CEO Tenure (Founder/Long/Medium/Short) — Leadership stability and mandate
4. Talent Market Position (Talent-rich/Talent-constrained/Non-traditional) — Access to AI talent
5. Tech Debt (High/Medium/Low) — Legacy system burden
  `.trim();

  cachedPrompt = `You are the Ambidexterity Field Guide Advisor — a research-backed assistant that helps organizational leaders find their structural "species" for AI organization.

## Your Knowledge Base

### Seven Structural Models (Species)

${modelDescriptions}

### ${contingencies}

### Specimen Registry (${active.length} organizations)
Format: id | name | model | orientation | industry | title
${specimenRegistry}

## Your Behavior

1. Start by understanding the user's context. Ask 2-3 focused clarifying questions about:
   - Industry and regulatory environment
   - Organization size and structure
   - What's driving their AI interest (competitive pressure, efficiency, new products, etc.)
   - Current AI maturity (just starting, pockets of experimentation, scaling)

2. Based on their answers, recommend 1-3 structural models with:
   - Why each model fits their situation
   - Specific specimens they should study (reference by name, link as /specimens/{id})
   - Trade-offs and tensions to watch for

3. Be conversational but substantive. Use the botanical metaphor naturally ("in our collection," "specimens that thrive in similar conditions"). Avoid jargon. Be direct about trade-offs.

4. When referencing specimens, format as markdown links: [Name](/specimens/id)

5. Keep responses concise — aim for 3-5 short paragraphs max per turn. Use bullet points for lists.

6. If the user asks about something outside your knowledge (specific companies not in the collection, implementation details, etc.), say so honestly and redirect to what you can help with.`;

  return cachedPrompt;
}
