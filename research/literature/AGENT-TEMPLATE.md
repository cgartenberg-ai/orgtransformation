# Literature Registry Agent Template

This template is used by the `/update-literature` skill to spawn one background agent per paper. The skill fills in `{{PDF_PATH}}`, `{{OUTPUT_PATH}}`, and `{{PAPER_FILENAME}}` before spawning.

---

## Agent Prompt

```
You are processing an academic paper for a literature registry.

READ this PDF: "{{PDF_PATH}}"

Then WRITE a JSON file to: "{{OUTPUT_PATH}}"

The JSON must follow this exact schema:

{
  "id": "authorlastname-year",
  "citation": "Full academic citation in APA-ish format (Authors, Year, Title, Journal, Volume, Pages)",
  "authors": ["LastName1", "LastName2"],
  "year": YYYY,
  "journal": "Short journal name or 'Book'",
  "tradition": "one of: org-econ | innovation | strategy | social-psych | other",
  "keyMechanism": "The paper's core theoretical mechanism in 2-4 sentences. Plain language, no jargon. What is the key argument or finding? Focus on the causal logic.",
  "predictionForAI": "What would this paper predict about how organizations structure AI work? 2-4 sentences. Be specific about structural predictions (centralization vs. delegation, team design, hierarchy, separation vs. integration). See context below.",
  "connectedInsights": [],
  "connectedMechanisms": [],
  "status": "candidate",
  "addedDate": "2026-02-03",
  "sourceFile": "library/research papers/{{PAPER_FILENAME}}"
}

## Context for predictionForAI

This is for a field guide studying how organizations structurally enable both AI exploration and operational execution. The central question is: "How do organizations structurally enable both exploration and execution in the AI era?"

The project documents 9 structural models:
- M1: Research Lab (pure exploration, structurally separated)
- M2: Center of Excellence (governance, standards, enablement)
- M3: Embedded Teams (AI integrated into product teams)
- M4: Hub-and-Spoke (central standards + distributed execution)
- M5: Product/Venture Lab (commercialize AI into products)
- M6: Unnamed/Informal (quiet transformation without formal structure)
- M7: Tiger Teams (time-boxed exploration sprints)
- M8: Skunkworks (autonomous unit, radical independence)
- M9: AI-Native (born-AI organization, no legacy to transform)

And 3 ambidexterity orientations:
- Structural: exploration and execution in distinct units
- Contextual: individuals balance both within their roles
- Temporal: organization cycles between exploration and execution phases

Our intellectual identity is organizational economics: Arrow, March, Simon, Garicano, Gibbons, Holmstrom, Henderson, Teece, North. We think in clean mechanisms and economic logic: information costs, incentive design, bounded rationality, coordination problems, property rights.

When writing predictionForAI, think about what this paper's core mechanism implies for:
- Whether organizations should centralize or distribute AI work
- How hierarchy and delegation change when AI augments cognition
- What structural forms (M1-M9) the theory predicts or explains
- What tensions or trade-offs the theory illuminates

## Tradition Classification

- org-econ: Arrow, Simon, Garicano, Holmstrom, Williamson, Milgrom, Roberts, Aghion, Tirole, Dessein, Gibbons, Henderson (relational contracts), North, Becker, Banerjee, Hayek
- innovation: Henderson & Clark, Teece, Christensen, O'Reilly & Tushman, Abernathy & Utterback, Nelson & Winter, Cohen & Levinthal
- strategy: Porter, Barney (RBV), Wernerfelt, Penrose, competitive dynamics
- social-psych: behavioral/psychological mechanisms, identity, motivation
- other: if none of the above fit

Leave connectedInsights and connectedMechanisms as empty arrays — those are filled in during a separate literature-match analysis.

Write ONLY the JSON file. Do not output anything else.
```
