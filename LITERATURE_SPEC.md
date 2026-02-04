# Literature Matching Spec: Connecting Field Insights to Scholarly Conversation

## Created: February 3, 2026

---

## Design Principle: Loose Coupling

The literature matching system is **decoupled from the fieldwork pipeline.** Broad research sweeps remain curiosity-driven and unbiased. Literature matching is a separate analytical activity, triggered on demand, that asks: "What do our current field observations say to the existing scholarly conversation?"

```
FIELDWORK PIPELINE (always broad, curiosity-driven)
  /research → /curate → /synthesize
  No literature bias. Observe what's out there.

LITERATURE ANALYSIS (on demand, separate trigger)
  /literature-match → gap analysis memo → literature-gaps-queue.json
  Analytical step. What do our findings mean for theory?

TARGETED RESEARCH (on demand, separate trigger)
  /research --target [literature-gaps | low-confidence | specific-org]
  Three independent research modes. Researcher chooses.
```

---

## 1. Literature Registry

### Location
`research/literature/registry.json`

### Schema

```json
{
  "description": "Core scholarly canon for the Ambidexterity Field Guide. Papers that are in conversation with our field insights.",
  "lastUpdated": "2026-02-03",
  "papers": [
    {
      "id": "garicano-2000",
      "citation": "Garicano, L. (2000). Hierarchies and the Organization of Knowledge in Production. Journal of Political Economy, 108(5), 874-904.",
      "authors": ["Garicano"],
      "year": 2000,
      "journal": "JPE",
      "tradition": "org-econ",
      "keyMechanism": "Workers refer problems they cannot solve to specialists higher in the hierarchy. Optimal hierarchy minimizes communication costs while matching problems to expertise.",
      "predictionForAI": "AI should substitute for lower layers of the knowledge hierarchy (routine problem-solving) while increasing demand for specialists who handle exceptions. Predicts flatter hierarchies with more specialized nodes.",
      "connectedInsights": ["hub-spoke-rd-intensive", "management-delayering-convergent"],
      "connectedMechanisms": [4, 11],
      "status": "core-canon",
      "addedDate": "2026-02-03",
      "sourceFile": null
    }
  ]
}
```

### Field Definitions

| Field | Type | Purpose |
|-------|------|---------|
| `id` | string | Slug identifier (author-year format) |
| `citation` | string | Full academic citation |
| `authors` | string[] | Author last names for quick reference |
| `year` | number | Publication year |
| `journal` | string | Short journal name |
| `tradition` | enum | `"org-econ"` \| `"innovation"` \| `"strategy"` \| `"social-psych"` \| `"other"` |
| `keyMechanism` | string | The paper's core theoretical mechanism in 1-2 sentences. Plain language, no jargon. |
| `predictionForAI` | string | What would this paper predict about organizations structuring AI work? This is the bridge from theory to our domain. May require interpretation — flag uncertainty. |
| `connectedInsights` | string[] | IDs from `synthesis/insights.json` |
| `connectedMechanisms` | number[] | Mechanism IDs from `synthesis/mechanisms.json` |
| `status` | enum | `"core-canon"` \| `"connected"` \| `"candidate"` |
| `addedDate` | string | When we added this to the registry |
| `sourceFile` | string \| null | Path to PDF if available (e.g., `research/literature/pdfs/garicano-2000.pdf`) |

### Status Levels

- **`core-canon`**: Papers from our intellectual tradition that we cite repeatedly. The 15-25 foundational papers.
- **`connected`**: Papers we've read and connected to specific insights. They inform our analysis but aren't part of the core theoretical identity.
- **`candidate`**: Papers someone flagged as potentially relevant but we haven't read/connected yet.

### Adding Papers

Two pathways:
1. **From training knowledge**: I draft entries for papers I know well. You review, correct, and approve. Good for the core canon.
2. **From your library**: You share PDFs. I read them, draft the entry (especially `keyMechanism` and `predictionForAI`), you review. Better for nuance and recent work.

---

## 2. The `/literature-match` Protocol

### When to Use

Trigger manually when:
- After a synthesis cycle, you want to see how new findings connect to theory
- Before writing a paper or chapter, to map the scholarly conversation
- When you want to brainstorm what's novel about our findings
- Periodically (e.g., monthly) as a research health check

### NOT triggered by:
- The regular `/research → /curate → /synthesize` pipeline
- New specimen creation
- Any automated process

### Protocol Steps

**Step 1: Load current state**
- Read `research/literature/registry.json` (the canon)
- Read `synthesis/insights.json` (current field insights)
- Read `synthesis/mechanisms.json` (current mechanisms)

**Step 2: For each confirmed insight, generate a structured analysis**

For each insight with `maturity: "confirmed"` or `maturity: "emerging"`:

```
INSIGHT: [title]
FIELD FINDING: [what we observed]

LITERATURE CONNECTIONS:
  [paper-id]:
    Predicts: [what the paper would predict]
    Our finding: [confirms | extends | boundary-condition | contradicts]
    Gap: [what evidence would strengthen or weaken this connection]

COMPETING EXPLANATIONS:
  [Alternative theoretical accounts for the same observation]

WHAT'S NOVEL:
  [What our finding adds that the literature doesn't already say]

RESEARCH GAPS:
  [What specimens or evidence we'd need to make this publishable]
```

**Step 3: Generate gap flags**

For each gap identified, create an entry in `research/literature-gaps-queue.json`:

```json
{
  "id": "hub-spoke-non-pharma",
  "insightId": "hub-spoke-rd-intensive",
  "gap": "All hub-and-spoke specimens are pharma. Need non-pharma R&D-intensive specimens.",
  "targetSpecimens": "semiconductor (TSMC, Intel), aerospace (Boeing, Lockheed), biotech (Moderna)",
  "theoreticalStake": "Distinguishes Garicano's knowledge hierarchy explanation from regulation explanation.",
  "priority": "high",
  "status": "open",
  "createdDate": "2026-02-03"
}
```

**Step 4: Output session memo**

Write a dated memo to `research/literature-match/YYYY-MM-DD-literature-match.md` summarizing:
- Which insights were analyzed
- Key connections found
- Competing explanations surfaced
- Gaps flagged
- Suggested next steps (papers to read, specimens to look for)

---

## 3. Literature Gaps Queue

### Location
`research/literature-gaps-queue.json`

### Schema

```json
{
  "description": "Specimens and evidence needed to strengthen field insight → literature connections. Populated by /literature-match sessions. Used optionally by /research when doing targeted sweeps.",
  "lastUpdated": "2026-02-03",
  "gaps": [
    {
      "id": "hub-spoke-non-pharma",
      "insightId": "hub-spoke-rd-intensive",
      "gap": "All hub-and-spoke specimens are pharma. Need non-pharma R&D-intensive specimens to distinguish specialization from regulation as driver.",
      "targetSpecimens": "semiconductor (TSMC, Intel), aerospace (Boeing, Lockheed Martin), automotive R&D (Toyota, Tesla)",
      "theoreticalStake": "If non-pharma R&D-intensive firms also use M4, supports Garicano. If regulated-but-not-R&D-intensive firms use M4, supports regulation explanation.",
      "connectedPapers": ["garicano-2000", "arrow-1962"],
      "priority": "high",
      "status": "open",
      "createdDate": "2026-02-03",
      "resolvedDate": null,
      "resolution": null
    }
  ]
}
```

### Priority Levels

- **`high`**: Gap blocks a publishable claim. We can't write the paper without resolving this.
- **`medium`**: Gap would strengthen a claim but isn't blocking.
- **`low`**: Interesting theoretical question, not urgent.

### Status

- **`open`**: Not yet resolved
- **`resolved`**: New evidence found (from any research mode — broad sweep or targeted)
- **`abandoned`**: No longer relevant (e.g., insight was reframed)

### Key Design Choice

**This queue does NOT feed into `/research` automatically.** It's a reference the researcher can consult when choosing what to look for in a targeted session. The command would be:

```
/research --target literature-gaps
```

Which reads the gaps queue and focuses the search on those specific organizations/industries. But the default `/research` remains broad sweeps.

---

## 4. Relationship Types

When connecting field insights to papers, use one of four relationship types:

| Type | Meaning | Example |
|------|---------|---------|
| **confirms** | Our observation matches what the paper predicts | Hub-and-spoke convergence in pharma confirms Garicano's knowledge hierarchy logic at the organizational unit level |
| **extends** | Our observation takes the paper's logic to a new domain or scale | Garicano models individual workers; we observe the same logic at the inter-unit level |
| **boundary-condition** | Our observation reveals where the paper's logic breaks down | AI-native orgs don't face the ambidexterity tension March (1991) assumes is universal |
| **contradicts** | Our observation is inconsistent with the paper's prediction | (None yet — but we should be looking for these) |

The **extends** and **boundary-condition** findings are the most publishable. Confirmations are useful but not novel. Contradictions are powerful but need very strong evidence.

---

## 5. Preliminary Core Canon

Papers to seed the registry with (I'll draft full entries; you review):

### Org Econ Foundation
1. **March (1991)** — Exploration and exploitation in organizational learning. *Our entire framing.*
2. **Simon (1947/1997)** — Administrative Behavior / bounded rationality. *Delayering, information processing.*
3. **Arrow (1962)** — Economic welfare and the allocation of resources for invention. *Learning-by-doing, information economics.*
4. **Garicano (2000)** — Hierarchies and the organization of knowledge. *Hub-and-spoke, knowledge matching.*
5. **Holmstrom (1979)** — Moral hazard and observability. *Agency problems, founder vs. hired CEO.*
6. **Aghion & Tirole (1997)** — Formal and real authority. *Founder authority, delegation.*
7. **Gibbons & Henderson (2012)** — Relational contracts and organizational capabilities. *Team consolidation, coordination costs.*

### Innovation & Organizational Design
8. **Henderson & Clark (1990)** — Architectural innovation. *Component vs. architectural change, Google's structural evolution.*
9. **Teece (1986)** — Profiting from technological innovation. *Complementary assets, productizing internal tools.*
10. **Christensen (1997)** — Innovator's dilemma. *Disruption logic, though we use it cautiously.*
11. **O'Reilly & Tushman (2004)** — The ambidextrous organization. *Structural ambidexterity specifically.*
12. **Gibson & Birkinshaw (2004)** — Contextual ambidexterity. *Our contextual orientation.*

### Institutions & Information
13. **North (1990)** — Institutions, institutional change and economic performance. *Regulatory moats, compliance infrastructure.*
14. **Banerjee (1992)** — A simple model of herd behavior. *CAIO waves, information cascades.*

### Human Capital & Organizational Structure
15. **Becker (1964)** — Human Capital. *Entry-level talent hollow, training as investment.*
16. **Dessein (2002)** — Authority and communication in organizations. *Delegation, centralization vs. decentralization.*
17. **Alonso, Dessein & Matouschek (2008)** — When does coordination require centralization? *Hub-and-spoke alternative to Garicano.*

### Recent / To Be Added From Your Library
18–25. *Space for papers you bring. Especially: recent work on AI and organizational structure, anything on technology-driven restructuring, papers on knowledge hierarchies in specific industries.*

---

## 6. What This Spec Does NOT Cover

- **Site integration**: No plans to show literature connections on the reference site yet. This is research infrastructure, not UI.
- **Automated matching**: No AI-driven paper discovery. We read papers and connect them manually. The quality of `predictionForAI` depends on us thinking carefully, not on keyword matching.
- **Citation management**: This is not a replacement for Zotero/Mendeley. It's a structured analytical layer on top of whatever bibliography tool you use.

---

## 7. Next Steps

1. **You**: Gather foundational papers. Start with PDFs of the core canon (especially any where the specific model/results matter more than the punchline).
2. **Me**: Draft full registry entries for the 17 papers listed above, using my training knowledge. You review and correct.
3. **Together**: Run the first `/literature-match` session on our 3-4 strongest confirmed insights. See what gaps emerge.
4. **Then**: Decide which gaps are worth targeted research and which we live with.

---

## Relationship to Other Specs

| Spec | Relationship |
|------|-------------|
| `CLAUDE.md` | Defines our intellectual identity — the papers we cite and the traditions we avoid |
| `Ambidexterity_Field_Guide_Spec.md` | Defines the taxonomy, insights, and mechanisms the literature connects to |
| `NARRATIVE_SPEC.md` | Defines how insights become publishable prose — literature matching provides the scholarly positioning |
| `synthesis/SYNTHESIS-PROTOCOL.md` | The synthesis pipeline that produces insights. Literature matching happens AFTER synthesis, not during. |

---

*This spec describes the design for a literature matching system that connects field observations to scholarly conversation without biasing fieldwork. Implementation includes: a literature registry, an on-demand `/literature-match` skill, and a gaps queue for optional targeted research.*
