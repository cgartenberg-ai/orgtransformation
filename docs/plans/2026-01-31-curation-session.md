# Curation Session: Process 3 Pending Research Sessions

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Transform raw research findings from 3 pending sessions into structured specimen JSON files — creating new specimens, adding layers to existing ones, and updating all registry/queue files.

**Architecture:** Process each research session sequentially. For each org: check if specimen exists, then either CREATE new JSON or UPDATE existing JSON with a new stratigraphic layer. All work follows the curation SKILL.md: classify with 7-model taxonomy + 3 orientations, preserve source provenance, add verbatim quotes, flag edge cases. After all orgs processed, update registry.json, mark sessions curated in queue.json, add to synthesis-queue.json, write curation session log, run validator.

**Tech Stack:** JSON specimen files following `specimens/specimen-schema.json`, Node.js validator (`scripts/validate-workflow.js`)

---

## Scope: What Needs Processing

### Session 1: `2026-01-31-no-priors-jensen-huang.md`
| Org | Status | Action |
|-----|--------|--------|
| nvidia | existing | Add layer (Jensen quotes on purpose-vs-tasks, Cursor adoption) |

### Session 2: `2026-01-31-multi-source-session.md`
| Org | Status | Action |
|-----|--------|--------|
| anthropic | existing | Add layer (7 co-founders, CEO/COO split, platform-first, compartmentalization, ~$5B ARR) |
| microsoft | existing | Add layer (3-tier AI structure, Teams channels mgmt, micro-cultures, NLWeb, DAX Copilot) |
| intercom | **new** | Create specimen (72-hr pivot, Fin agent, 4 AI roles, "refounding") |
| ubs | evolution | Add evolution layer (first CAIO appointed, Chief AI Office, reports to CTO) |
| commonwealth-bank | evolution | Add evolution layer (first CAIO, hired from Lloyds, formalizing AI leadership) |
| us-cyber-command | **new** | Create specimen (first CAIO, military pipeline) |
| fda | **new** | Create specimen (first CAIO + Head of IT, combined role) |
| boston-dynamics-deepmind | **new** | Create specimen (cross-company AI-robotics partnership) |
| world-labs | **new** | Create specimen (Fei-Fei Li academic spin-off, Marble world model) |
| harvey-ai | **new** | Create specimen (legal AI, 1000 customers in 3 years) |

### Session 3: `2026-01-31-substacks-bg2-press.md`
| Org | Status | Action |
|-----|--------|--------|
| meta | evolution | Add evolution layer (MSL 4-unit reorg, Wang as CAIO, LeCun departure, 600 layoffs) |
| google | evolution | Add evolution layer (Project EAT, AI2 consolidation) |
| eli-lilly | evolution | Add evolution layer ($1B NVIDIA co-innovation lab, 24/7 wet-dry loop) |
| wells-fargo | **new** | Create specimen (Head of AI from consumer banking, Shafiq from AWS) |
| salesforce | evolution | Add evolution layer (9K→5K support staff, Agentforce, budget 3x) |
| openai | evolution | Add evolution layer (PBC restructuring, IPO prep, $1T valuation) |
| anthropic | evolution | Add evolution layer (IPO prep, LTBT governance, ~$26B revenue) |
| nasa | **new** | Create specimen (CAIO transition, defense-to-CAIO pipeline) |
| ami-labs | **new** | Create specimen (LeCun spin-off from Meta, world models, V-JEPA) |
| databricks | **new** | Create specimen (95% AI projects fail thesis, platform play) |
| glean | **new** | Create specimen (enterprise AI search, automation harder than expected) |
| hp | **new** | Create specimen (AI-driven restructuring, $1B savings target) |
| tesla | evolution | Add evolution layer (Operation Maestro, $20B CapEx, revenue decline) |

**Totals: 11 new specimens to create, 14 existing specimens to update (some updated twice)**

---

## Task 1: Create New Specimen — Intercom

**Files:**
- Create: `specimens/intercom.json`

**Step 1: Create the specimen JSON file**

Read the Intercom section of `research/sessions/2026-01-31-multi-source-session.md` and create `specimens/intercom.json` following the schema exactly. Key classification decisions:

- **Structural Model**: Model 3 (Embedded Teams) → evolving to Model 4 (Hybrid). The 72-hour pivot dismantled existing structure and rebuilt around AI. The 4 new AI-specific roles (AI ops lead, knowledge manager, conversation designer, support automation specialist) suggest a central AI coordination layer forming. But currently the AI IS the product (Fin), so it's more embedded. **Primary: Model 3, Secondary: Model 4.** Confidence: Medium.
- **Orientation**: Temporal — the 72-hour pivot is a textbook example of temporal ambidexterity (rapid phase shift from execution to exploration).
- **Mechanisms**: #5 (Deploy to Thousands Before You Know What Works) — 7,000+ customers, 1M+ resolutions/week; also #6 (Merge Competing AI Teams Under Single Leader) — unified Customer Agent replaces multiple agents
- **Sources**: 5 sources from session with full URLs and dates
- **Quotes**: Des Traynor on org collapse, 60-80% volume reduction
- **Layer**: Single initial layer dated 2025 covering the full Fin/Pioneer/refounding arc
- **Habitat**: Technology, SaaS/Customer Support, Scaleup, San Francisco, North America
- **Contingencies**: timeToObsolescence=Fast, regulatoryIntensity=Low, talentMarketPosition=Talent-rich
- **Tension positions**: structuralVsContextual=0.3 (more contextual, AI-is-the-product), speedVsDepth=0.8 (speed — 72hr pivot, 15-day build), centralVsDistributed=-0.3 (trending central with unified Customer Agent), namedVsQuiet=-0.7 (strongly named: Fin), longVsShortHorizon=0.5 (quarterly+ cycles)
- **Open questions**: From session: internal org chart, Fin team size, what happened to scrapped teams
- **Taxonomy feedback**: This org is a strong candidate for a new pattern — "AI-native refounding" where the entire company pivots around AI as core product, not just using AI as a tool. Could be a type specimen for Model 3→temporal pivot.

**Step 2: Validate the JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('specimens/intercom.json','utf8')); console.log('Valid JSON')"` from the project root.

---

## Task 2: Create New Specimen — US Cyber Command

**Files:**
- Create: `specimens/us-cyber-command.json`

**Step 1: Create the specimen JSON file**

Key classification:
- **Structural Model**: Model 2 (Center of Excellence) — CAIO role to accelerate AI adoption across cyber operations = enablement function. Confidence: Low (limited data).
- **Orientation**: Structural — creating a dedicated CAIO office is structural separation.
- **Mechanisms**: #9 (Hire CAIOs from Consumer Tech) — counterexample: military/intel pipeline, NOT consumer tech. Note this in taxonomy feedback.
- **Habitat**: Government/Defense, Enterprise, US
- **Note**: This is a thin specimen (Stub status). Single source. Mark completeness: Low.

**Step 2: Validate JSON**

---

## Task 3: Create New Specimen — FDA

**Files:**
- Create: `specimens/fda.json`

**Step 1: Create the specimen JSON file**

Key classification:
- **Structural Model**: Model 2 (Center of Excellence) — combined CAIO + Head of IT role suggests enablement/governance. Confidence: Low.
- **Orientation**: Structural — formal CAIO appointment.
- **Mechanisms**: #9 counterexample again: IT/federal pipeline, not consumer tech.
- **Taxonomy feedback**: Combined CAIO + Head of IT is structurally interesting — suggests at some orgs AI leadership is being merged with IT rather than separated from it. Contrasts with UBS/CBA where CAIO is distinct from CTO.
- **Status**: Stub. Single source.

**Step 2: Validate JSON**

---

## Task 4: Create New Specimen — Boston Dynamics + DeepMind

**Files:**
- Create: `specimens/boston-dynamics-deepmind.json`

**Step 1: Create the specimen JSON file**

Key classification:
- **Structural Model**: Model 1 (Research Lab) — DeepMind provides foundational AI models, Boston Dynamics provides robotics execution. But this is a PARTNERSHIP, not a single org. Confidence: Low.
- **Orientation**: Structural — separate orgs handling explore (DeepMind models) vs. execute (BD hardware).
- **Taxonomy feedback**: Cross-company partnerships don't fit cleanly into the taxonomy which assumes single organizations. This is a "structural ambidexterity via partnership" — exploration and execution in different companies. Worth tracking but may not be a full specimen.
- **Status**: Stub. Single source.

**Step 2: Validate JSON**

---

## Task 5: Create New Specimen — World Labs

**Files:**
- Create: `specimens/world-labs.json`

**Step 1: Create the specimen JSON file**

Key classification:
- **Structural Model**: Model 5b (Venture Builder) — academic spin-off from Stanford, building Marble product. Confidence: Low.
- **Orientation**: Structural — separate entity dedicated to exploration.
- **Habitat**: Technology/AI, Startup, North America
- **Status**: Stub. Single source (podcast description only).

**Step 2: Validate JSON**

---

## Task 6: Create New Specimen — Harvey AI

**Files:**
- Create: `specimens/harvey-ai.json`

**Step 1: Create the specimen JSON file**

Key classification:
- **Structural Model**: Model 5a (Internal Incubator) or pure startup. Harvey IS the AI product — not a division of a larger org. Reconsidering: Model 3 (Embedded) — AI is embedded in the product itself, there's no separate "AI team" vs "product team." Confidence: Low.
- **Orientation**: Contextual — AI IS the business, no separation between explore and execute.
- **Taxonomy feedback**: Pure AI-native startups (where AI IS the product, not a tool used by the product) don't fit the taxonomy cleanly. The taxonomy was designed for orgs that have to ADD AI to existing operations. Harvey, like Anthropic, is exploring and executing simultaneously because the AI IS the operation.
- **Status**: Stub. Single source (podcast description).
- **Open questions**: Deep-scan No Priors Gabe Pereyra episode needed.

**Step 2: Validate JSON**

---

## Task 7: Create New Specimens — Wells Fargo, NASA, AMI Labs, Databricks, Glean, HP

**Files:**
- Create: `specimens/wells-fargo.json`
- Create: `specimens/nasa.json`
- Create: `specimens/ami-labs.json`
- Create: `specimens/databricks.json`
- Create: `specimens/glean.json`
- Create: `specimens/hp.json`

**Step 1: Create each specimen JSON file**

Key classifications:

**Wells Fargo:**
- Model 4 (Hybrid) — business leader (Van Beurden) given AI mandate + tech exec (Shafiq from AWS) underneath = hub-and-spoke forming. Confidence: Medium.
- Orientation: Contextual — 90K trained, 180K desktops, but led from consumer banking not a separate unit.
- Mechanisms: #9 (Hire CAIOs from Consumer Tech) — counterexample: consumer banking leader + AWS exec pipeline. #5 (Deploy to Thousands) — 180K desktops.
- Habitat: Financial Services, Banking, Enterprise, ~250K employees, ~$82B revenue, San Francisco, North America

**NASA:**
- Model 2 (Center of Excellence) — CAIO/CDO governance role. Confidence: Medium.
- Orientation: Structural — formal CAIO appointment per federal mandate.
- Interesting: CAIO transition from defense/intel pipeline (Salvagnini) to domain expert pipeline (Murphy). Two different CAIO career paths at same org.
- Mechanisms: #8 (Log Everything When Regulators Watch) — federal mandate drove CAIO appointment.

**AMI Labs:**
- Model 1 (Research Lab) — world models research, V-JEPA architecture. Confidence: Medium.
- Orientation: Structural — dedicated research entity, separate from commercial product.
- Taxonomy feedback: Spin-off from Big Tech research lab (Meta FAIR) triggered by research-vs-product tension. This is the opposite of Google X (Model 5b venture builder) — it's a "researcher exits to preserve research autonomy" pattern.
- Habitat: Technology/AI Research, Startup, Paris, Europe

**Databricks:**
- Model 5c (Platform-to-Product) — internal AI platform capabilities sold to enterprises. Confidence: Low (limited org structure data, mostly market commentary).
- Orientation: Structural — separate platform development.
- Status: Stub.

**Glean:**
- Model 5a (Internal Incubator) — enterprise AI search product. Confidence: Low.
- Orientation: Contextual — Jain admits AI automation harder than expected, suggests org is still figuring out explore/execute balance.
- Status: Stub.

**HP:**
- Model 6a (Enterprise-Wide Adoption, Unnamed/Informal) — company-wide restructuring via AI, no named AI lab. Confidence: Low.
- Orientation: Contextual — AI-driven productivity across all functions.
- Status: Stub. Single source.

**Step 2: Validate all JSON files**

---

## Task 8: Update Existing Specimen — NVIDIA (Session 1)

**Files:**
- Modify: `specimens/nvidia.json`

**Step 1: Add new layer to NVIDIA specimen**

Add a new layer at the top of the `layers` array:
```json
{
  "date": "2026-01",
  "label": "Purpose-vs-Tasks Framework + Pervasive AI Tooling",
  "summary": "Jensen Huang articulates 'purpose vs tasks' philosophy — software engineers solve problems, coding is one task. NVIDIA engineers use Cursor 'pervasively.' Productivity gains lead to more exploration, not fewer jobs. Continued aggressive hiring despite AI gains.",
  "classification": null,
  "sourceRefs": ["no-priors-jensen-2026"]
}
```

Add source:
```json
{
  "id": "no-priors-jensen-2026",
  "type": "Podcast",
  "name": "No Priors — Jensen Huang on Reasoning Models, Robotics",
  "url": "https://open.spotify.com/episode/4kSlkESoQ8GPU6meWACSlf",
  "timestamp": "~37:49",
  "sourceDate": "2026-01-08",
  "collectedDate": "2026-01-31",
  "notes": null
}
```

Add quotes from session. Update `meta.lastUpdated` to `2026-01-31`. Bump layerCount in registry later.

Consider reclassification: currently Model 4 (Hybrid), Structural. The new data on pervasive Cursor adoption and "purpose vs tasks" philosophy suggests Contextual orientation may be emerging as secondary. Keep current classification but note in `taxonomyFeedback`.

**Step 2: Validate JSON**

---

## Task 9: Update Existing Specimen — Anthropic (Sessions 2 + 3)

**Files:**
- Modify: `specimens/anthropic.json`

**Step 1: Add TWO new layers**

This org has findings from both Session 2 (Cheeky Pint — Dario Amodei) and Session 3 (IPO prep). Add both as separate layers.

**Layer from Session 2 (Cheeky Pint):**
```json
{
  "date": "2025-08",
  "label": "Co-Founder Structure + CEO/COO Explore-Execute Split",
  "summary": "7 co-founders with equal equity — defying standard advice, enables cultural scaling. Dario (CEO) handles strategy/exploration, Daniela (COO) handles operations/execution. Platform-first with strategic vertical investments. Information compartmentalization within open culture. Highest retention among AI companies. ~$5B ARR.",
  "classification": null,
  "sourceRefs": ["cheeky-pint-dario-2025"]
}
```

**Layer from Session 3 (IPO):**
```json
{
  "date": "2025-12",
  "label": "IPO Preparation + LTBT Governance",
  "summary": "Hired Wilson Sonsini for IPO prep. PBC with novel Long-Term Benefit Trust (LTBT) holding Class T shares. No dual-class founder structure — LTBT provides governance center of gravity. Valued ~$350B. Revenue projecting to ~$26B annualized.",
  "classification": null,
  "sourceRefs": ["techcrunch-ipo-2025", "cnbc-valuation-2025", "future-forem-ltbt-2026"]
}
```

Add all sources with URLs from both sessions. Add quotes (Dario on co-founders, CEO/COO split, product-as-window, compartmentalization).

**Reclassification opportunity:** Currently Model 5 (Product/Venture Lab), 5a (Internal Incubator), Structural. The new data on CEO/COO explore/execute split, co-founder scaling structure, and platform-first approach strengthens this but may also suggest Contextual elements (information compartmentalization, all-hands alignment). Keep Model 5a/Structural but raise confidence from Medium to High.

Update `observableMarkers` with the co-founder structure, CEO/COO split, retention data, revenue metrics.

Fill `contingencies`: regulatoryIntensity=Medium (AI safety regulation emerging), timeToObsolescence=Fast (rapid model improvement cycle), ceoTenure=Founder, talentMarketPosition=Talent-rich, technicalDebt=Low.

Fill `tensionPositions`: structuralVsContextual=-0.5 (structural — Labs team separated from product), speedVsDepth=-0.3 (validates internally before launching), centralVsDistributed=-0.6 (centralized — 7 co-founders project values outward), namedVsQuiet=-0.8 (strongly named), longVsShortHorizon=-0.5 (multi-year research horizon).

Update `openQuestions` from session data. Update `meta.completeness` from "Low" to "Medium".

**Step 2: Validate JSON**

---

## Task 10: Update Existing Specimen — Microsoft (Session 2)

**Files:**
- Modify: `specimens/microsoft.json`

**Step 1: Add new layer**

Layer: 3-tier AI structure (token factory → agent factory → Copilot), CEO manages via Teams channels, micro-cultures, NLWeb, DAX Copilot vertical.

Add 5 sources with full URLs from Cheeky Pint Nadella episode. Add 3 quotes (AI diffusion, Teams channels, micro-cultures).

Reclassification: Currently Model 4 (Hybrid), Structural. The 3-tier structure confirms Hub-and-Spoke. Raise confidence. Add mechanism #7 (Put Executives on the Tools) — Nadella "lingering around Teams channels" to discover AI work.

**Step 2: Validate JSON**

---

## Task 11: Update Existing Specimens — UBS + Commonwealth Bank (Session 2, Evolutions)

**Files:**
- Modify: `specimens/ubs.json`
- Modify: `specimens/commonwealth-bank.json`

**Step 1: Add evolution layers**

**UBS:** Currently Model 2 (CoE), Contextual. Add evolution layer: first CAIO (Magazzeni), reports to Group Chief CTO, dedicated Chief AI Office, 300+ active AI use cases. This may shift classification: adding formal CAIO + dedicated office on top of existing CoE suggests Model 4 (Hybrid) emerging. Add all 5 sources with URLs. Raise confidence. Mechanism #9 counterexample (academic pipeline: King's College → JPM CoE → CAIO).

**Commonwealth Bank:** Currently Model 6a (Enterprise-Wide), Contextual. Add evolution layer: first CAIO (Boteju from Lloyds), formalizing leadership over existing broad deployment. This is interesting — moving FROM contextual (50K employees on day one, no formal AI leader) TO structural (dedicated CAIO). Note in taxonomy feedback. Add 3 sources with URLs.

**Step 2: Validate both JSON files**

---

## Task 12: Update Existing Specimens — Meta, Google, Eli Lilly, Salesforce, OpenAI, Tesla (Session 3, Evolutions)

**Files:**
- Modify: `specimens/meta-ai.json`
- Modify: `specimens/google-deepmind.json` (note: Google's specimen is google-deepmind but Project EAT is broader Google)
- Modify: `specimens/eli-lilly.json`
- Modify: `specimens/salesforce.json`
- Modify: `specimens/openai-microsoft.json`
- Modify: `specimens/tesla.json`

**Step 1: Add evolution layers to each**

**Meta:** Major update. Currently Model 1 (Research Lab), Structural. Reclassify to **Model 4 (Hybrid)** — MSL has 4 distinct units (TBD Lab, FAIR, Products & Applied Research, Infra). Primary: Model 4, Secondary: Model 1 (FAIR preserved as research unit). Add mechanism #6 (Merge Competing AI Teams) — consolidated under Wang. Add 8+ sources with URLs. Add LeCun and Wang quotes. Update description heavily. Raise completeness to Medium.

**Google:** Currently Model 1 (Research Lab), google-deepmind specimen. Project EAT is Google-wide (Research + Cloud + Hardware consolidated under AI2). Consider: this specimen should focus on Google's AI org broadly, not just DeepMind. Add evolution layer about Project EAT consolidation. May need to reconsider specimen scope. Add 3 sources.

**Eli Lilly:** Currently Model 1 + Model 5, Structural. Add layer: $1B NVIDIA co-innovation lab, co-location in SF, 24/7 wet-dry lab loop, extends to manufacturing/robotics. This deepens the existing classification. Add 4 sources. Raise completeness to High — this is one of the richest specimens.

**Salesforce:** Currently Model 4 (Hybrid), Structural. Add layer: 9K→5K support via AI agents, Agentforce + Agent Script, budget tripled to $300M, 20%+ more AEs. Add mechanism #5 (Deploy to Thousands) — 50% of conversations now AI. Interesting tension: may be shifting toward Model 6a (Enterprise-Wide/Contextual) as AI becomes the default. Add 5 sources. Add Benioff commentary.

**OpenAI:** Currently Model 5b (Venture Builder), openai-microsoft specimen. Add evolution layer: PBC restructuring completed Oct 2025, IPO prep with $1T valuation, AGI verification mechanism, SoftBank $40B. This is a STRUCTURAL evolution (nonprofit → PBC) not just product evolution. Add 7 sources.

**Tesla:** Currently Model 3 (Embedded), Contextual. Add layer: Operation Maestro, $20B CapEx, 61% income drop from AI restructuring costs. Very thin data still. Add 2 sources. Keep as Low completeness.

**Step 2: Validate all JSON files**

---

## Task 13: Update Registry, Queue, and Synthesis Queue

**Files:**
- Modify: `specimens/registry.json`
- Modify: `research/queue.json`
- Modify: `curation/synthesis-queue.json`

**Step 1: Update registry.json**

- Add 11 new specimen entries to the `specimens` array
- Update `totalSpecimens` from 52 to 63
- Update `byModel` counts to reflect new/reclassified specimens
- Update `byOrientation` counts
- Update `lastUpdated` to today
- For all updated specimens: increment `layerCount`, update `lastUpdated`

**Step 2: Mark sessions curated in queue.json**

Change all 3 queue entries from `"status": "pending"` to `"status": "curated"` and set `"curatedIn": "2026-01-31-curation.md"`.

**Step 3: Add specimens to synthesis-queue.json**

Add all 22 unique specimens (11 new + ~11 updated) to the synthesis queue with status "pending":

```json
{
  "specimenId": "intercom",
  "addedDate": "2026-01-31",
  "reason": "New specimen from multi-source session",
  "status": "pending"
}
```

**Step 4: Validate**

Run: `node scripts/validate-workflow.js`

Expected: specimen count matches (63), no stale queue items, registry totals align.

---

## Task 14: Write Curation Session Log

**Files:**
- Create: `curation/sessions/2026-01-31-curation.md`

**Step 1: Write session summary**

Following the curation SKILL.md session output format:

```markdown
# Curation Session: 2026-01-31

## Sessions Processed
- 2026-01-31-no-priors-jensen-huang.md (1 org)
- 2026-01-31-multi-source-session.md (11 orgs)
- 2026-01-31-substacks-bg2-press.md (13 orgs)

## Specimens Created/Updated
| Organization | Action | Model | Orientation | Confidence | Notes |
|...|...|...|...|...|...|

## Taxonomy Feedback
[Edge cases, suggested revisions]

## Type Specimens Identified
[Candidates]

## Reclassifications
[Orgs whose classification changed with rationale]
```

---

## Task 15: Final Validation + Commit

**Step 1: Run validator**

Run: `node scripts/validate-workflow.js`

Fix any issues.

**Step 2: Commit**

```bash
git add specimens/*.json research/queue.json curation/ docs/plans/
git commit -m "feat: curate 3 research sessions — 11 new specimens, 14 updated"
```

---

## Execution Notes

### Processing Order
Tasks 1-7 (create new specimens) can be done in any order. Tasks 8-12 (update existing) can be done in any order. Task 13 (registry/queues) must come after all specimens are done. Task 14 (session log) must come after Task 13. Task 15 (validate/commit) is last.

### Key Quality Checks During Execution
1. Every fact in a specimen must trace to a source with a URL
2. Verbatim quotes must be preserved exactly from session files
3. Never overwrite existing layers — only add new ones at the top
4. Classification rationale must be explicit when confidence is Medium or Low
5. Evolution flags from sessions must be reflected as layer transitions, not overwrites
6. `meta.completeness` should accurately reflect data richness: Stub=single thin source, Low=few sources/many gaps, Medium=core structure understood, High=multiple sources/mechanisms/quotes

### Deduplication Awareness
- Anthropic appears in Session 2 AND Session 3 — two separate layers needed (different time periods, different findings)
- Meta has LeCun departure data that overlaps with AMI Labs creation — AMI Labs gets its own specimen, Meta gets the departure as part of its evolution
- Google's Project EAT may overlap with google-deepmind specimen — keep separate for now, note in taxonomy feedback
