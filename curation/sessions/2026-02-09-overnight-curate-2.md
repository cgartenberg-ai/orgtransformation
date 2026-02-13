    # Overnight Curate Run — 2026-02-09

    **Started:** 2026-02-09 08:21
    **Duration:** 45 minutes
    **Curated:** 32 | **New:** 32 | **Updated:** 0 | **Failed:** 0
    **Method:** `scripts/overnight-curate.py` via `claude -p --model opus`

    ## Results

    | Specimen                       | Action  | Model | Orientation | Conf.  | Compl. | Quotes | Sources | Time   |
    |--------------------------------|---------|-------|-------------|--------|--------|--------|---------|--------|
    | anduril                        | new     | M9  | Structural  | High   | High   |      6 |      10 |    75s |
| bloomberg                      | new     | M4  | Contextual  | High   | High   |     10 |       6 |    80s |
| blue-origin                    | new     | M6  | Contextual  | High   | High   |      8 |       6 |    79s |
| bmw                            | new     | M4  | Contextual  | High   | High   |      5 |       6 |    68s |
| cvs-health                     | new     | M4  | Contextual  | High   | High   |      5 |       6 |    75s |
| deere-and-co                   | new     | M4  | Structural  | High   | Medium |      3 |       7 |    65s |
| delta-air-lines                | new     | M4  | Contextual  | Medium | Medium |      7 |       7 |    78s |
| disney                         | new     | M4  | Structural  | High   | High   |     10 |       8 |    83s |
| exxonmobil                     | new     | M6  | Contextual  | Medium | Medium |      3 |       7 |    57s |
| fedex                          | new     | M4  | Contextual  | Medium | Medium |     10 |      10 |    97s |
| ford                           | new     | M4  | Structural  | Medium | Medium |     10 |       8 |    85s |
| general-motors                 | new     | M4  | Structural  | High   | High   |      4 |       6 |    68s |
| honda                          | new     | M4  | Structural  | Medium | Medium |      5 |       6 |    68s |
| honeywell                      | new     | M4  | Structural  | High   | High   |     10 |      11 |   115s |
| intel                          | new     | M4  | Structural  | Medium | High   |      9 |       6 |    78s |
| kroger                         | new     | M4  | Structural  | High   | High   |      5 |       7 |    76s |
| lockheed-martin                | new     | M4  | Structural  | High   | High   |      7 |      10 |    77s |
| lowes                          | new     | M4  | Structural  | High   | High   |     10 |       6 |   107s |
| mayo-clinic                    | new     | M4  | Structural  | High   | High   |      8 |       5 |    73s |
| mercedes-benz                  | new     | M4  | Structural  | High   | High   |     11 |       9 |   101s |
| mount-sinai-health-system      | new     | M4  | Structural  | High   | High   |      8 |       6 |    97s |
| netflix                        | new     | M4  | Contextual  | Medium | High   |      8 |      10 |    82s |
| nike                           | new     | M4  | Contextual  | Medium | Medium |      2 |       6 |    70s |
| pepsico                        | new     | M4  | Contextual  | High   | High   |      9 |      12 |   110s |
| progressive                    | new     | M6  | Contextual  | Medium | Medium |      1 |       6 |    53s |
| sutter-health                  | new     | M4  | Structural  | High   | High   |      8 |       8 |    80s |
| t-mobile                       | new     | M4  | Structural  | Medium | Medium |      7 |       7 |    75s |
| toyota                         | new     | M4  | Structural  | High   | High   |      5 |       6 |    67s |
| uber                           | new     | M4  | Structural  | Medium | Medium |      6 |       8 |    75s |
| ulta-beauty                    | new     | M4  | Contextual  | High   | High   |      8 |       6 |    75s |
| unitedhealth-group             | new     | M4  | Structural  | High   | High   |      7 |       7 |    78s |
| visa                           | new     | M4  | Structural  | Medium | Medium |      3 |       6 |    53s |

    ## Model Distribution (this batch)

    | Model                                | Count | Existing | New Total |
    |--------------------------------------|-------|----------|-----------|
    | M4 Hybrid/Hub-and-Spoke           |    28 |       29 |        57 |
| M6 Unnamed/Informal               |     3 |       14 |        17 |
| M9 AI-Native                      |     1 |        9 |        10 |

    ## Orientation Distribution

    | Orientation | Count |
    |-------------|-------|
    | Contextual  |    12 |
| Structural  |    20 |

    ## Confidence Distribution

    | Level  | Count |
    |--------|-------|
    | High   |    20 |
| Medium |    12 |

    ## Industries Covered

    | Industry                  | Count |
    |---------------------------|-------|
    | Automotive                |     6 |
| Healthcare                |     5 |
| Defense                   |     2 |
| Media / Entertainment     |     2 |
| Media / Financial Data    |     1 |
| Aerospace                 |     1 |
| Agriculture / Industrials |     1 |
| Airlines                  |     1 |
| Energy                    |     1 |
| Logistics                 |     1 |
| Industrials               |     1 |
| Semiconductors            |     1 |
| Retail / Grocery          |     1 |
| Retail / Home Improvement |     1 |
| Consumer / Retail         |     1 |
| Consumer Goods / Manufacturing |     1 |
| Insurance                 |     1 |
| Telecom                   |     1 |
| Transportation / Mobility |     1 |
| Retail / Beauty           |     1 |
| Fintech / Payments        |     1 |

    ## Per-Specimen Analysis

    ### anduril — M9 AI-Native | Structural | High

**Description:** Anduril Industries represents the paradigm case of an AI-Native organization in the defense sector. Founded in 2017 by Palmer Luckey (Oculus founder), Brian Schimpf, and others, the company was built from day one around the Lattice AI platform — an operating system that powers all Anduril products including autonomous drones (Ghost, Fury), counter-UAS systems (Roadrunner), submarines (Dive XL), an...

**Classification rationale:** Anduril is the definitional M9 AI-Native organization. Founded in 2017 specifically to build AI-powered defense technology, there is no legacy transformation or AI adoption story — AI is the foundational DNA. The Lattice AI platform powers all products from drones to submarines. No CAIO role exists because AI is not treated as a separate discipline requiring special leadership; it's the baseline assumption. The structural orientation reflects that AI capabilities are embedded in distinct product divisions (Air Dominance, Maritime, Integrated Systems for Space/Intelligence) rather than contextually balanced within individual roles.

**Mechanisms linked:** M3 Embed Product at Research Frontier, M10 Productize Internal Operational Advantages

**Key quotes:**
- "The United States needs to arm our allies and partners around the world so that they can be prickly porcupines that nobo..." — Palmer Luckey
- "The future of warfare will be superficially hardware-driven with a buttload of software smarts under the hood making it ..." — Palmer Luckey
- "AI in warfare is no longer hypothetical; it's inevitable." — Palmer Luckey

**Botanist's notes:**
- [2026-02] Anduril is the clearest type specimen for M9 AI-Native — there is no transformation story because AI was the founding premise. This makes it uniquely valuable for contrast: what does AI structure look like when there's no legacy to overcome? The absence of a CAIO role is telling; AI leadership is unnecessary when AI is assumed, not added.
- [2026-02] The 'no separate AI team' structure at Anduril challenges a core assumption in the taxonomy: most models assume AI is a *function* that must be positioned somewhere. For AI-native orgs, this framing may not apply. Lattice is more like an operating system than a team — it's infrastructure that all product divisions build on, similar to how no one asks 'where is the electricity team?'
- [2026-02] The AI Grand Prix competition represents a novel talent acquisition mechanism that sidesteps traditional AI hiring. By running a competition ('If you think you can build an autonomy stack that can out-fly the world's best, show us'), Anduril turns hiring into product development. This suggests AI-native orgs may develop different organizational forms for talent acquisition, not just product development.

**Open questions:**
- What is the internal AI/ML team structure within product divisions?
- How is the OpenAI partnership structured operationally?
- What specific AI/ML talent pipeline and hiring practices does Anduril use?


### bloomberg — M4 Hybrid/Hub-and-Spoke | Contextual | High

**Description:** Bloomberg has built one of the most mature AI organizations in financial services, with roots stretching back to 2009—well before the current generative AI wave. The company employs over 350 AI researchers and engineers organized in a hub-and-spoke model: a central AI Strategy & Research team in the Office of the CTO sets direction and breaks down barriers, while specialized AI engineering teams (...

**Classification rationale:** Bloomberg exhibits classic hub-and-spoke architecture: a central AI Strategy & Research team in the CTO office (hub) sets strategy and coordinates, while 350+ AI experts are distributed across specialized engineering teams—AI Search, AI Enrichment, AI Finance—in four global locations (spokes). The 'hammers looking for nails' philosophy from Amanda Stent is the clearest articulation of contextual orientation: AI experts embedded within domains actively seek problems to solve, rather than operating in isolated research silos. This is reinforced by the needs-driven philosophy ('figure out what our clients' needs are, and then how we can address those needs, using AI if necessary') and the human-in-the-loop approach where Bloomberg Intelligence analysts train and review AI outputs. The 15-year track record since 2009 demonstrates sustained commitment rather than recent transformation.

**Mechanisms linked:** M3 Embed Product at Research Frontier, M8 Turn Compliance Into Deployment Advantage

**Key quotes:**
- "For more than a decade, Bloomberg has been leading the charge when it comes to the innovative and pragmatic use of AI in..." — Shawn Edwards
- "Generative AI illustrates all of these challenges. It is not a silly fad. It's one of the most exciting advancements we'..." — Shawn Edwards
- "Finance is an industry that relies on facts to make mission-critical decisions. So, one crucial principle we think about..." — Shawn Edwards

**Botanist's notes:**
- [2026-02] The 'hammers looking for nails' quote is one of the clearest articulations of contextual ambidexterity in our specimen collection—AI experts are explicitly positioned as embedded problem-seekers rather than isolated researchers. This contrasts with structural separation models where AI teams wait for problems to be brought to them.
- [2026-02] Bloomberg's 15-year AI timeline (since 2009) challenges narratives of 'AI transformation'—this is an organization that has been incrementally building capability, not pivoting. The M4 hub-and-spoke structure may be a natural end-state for mature AI organizations that started with M2/M3 models years ago.
- [2026-02] The founder-CEO (Michael Bloomberg) is notably absent from AI messaging despite the company bearing his name. All AI communication comes from CTO and Head of AI Strategy. This may indicate either delegation maturity or that AI is treated as technical infrastructure rather than strategic identity—worth comparing to founder-led AI messaging at other specimens.

**Open questions:**
- No direct quotes from Michael Bloomberg on AI strategy—founder appears removed from day-to-day AI messaging
- Specific AI investment levels (budget, CapEx, % of R&D) not disclosed due to private company status
- Details on AWS re:Invent 2025 NL-to-video generation presentation not found in public sources


### blue-origin — M6 Unnamed/Informal | Contextual | High

**Description:** Blue Origin represents a striking example of enterprise-wide AI adoption without formal AI organizational structure. The company has deployed over 2,700 AI agents across engineering, manufacturing, software, and supply chain functions, achieving 70% monthly adoption company-wide and 95% adoption among software engineers—all without a Chief AI Officer, dedicated AI lab, or formally branded AI initi...

**Classification rationale:** Blue Origin has achieved 70% company-wide AI adoption with 2,700+ deployed agents and 95% of software engineers using AI tools, yet has no dedicated AI lab, CAIO, or formally branded AI organization. AI capability is delivered through an internal platform (BlueGPT) managed by Enterprise Technology, not a separate exploration unit. The explicit expectation that 'everyone at Blue Origin is expected to build and collaborate with AI agents' combined with democratized agent creation makes this textbook M6a. The orientation is clearly Contextual: individuals across engineering, manufacturing, software, and supply chain balance both exploration (building new agents) and execution (using agents for core work) within their existing roles.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works, M7 Put Executives on the Tools

**Key quotes:**
- "Agentic AI has exploded at Blue Origin. Everyone at Blue is expected to build and collaborate with AI agents. We believe..." — William Brennan
- "The early days of GenAI were exciting for us, but limited to more common sorts of tasks. We needed AI that could actuall..." — William Brennan
- "This is what we see as the future of engineering teams at Blue Origin. Small teams of 2 or 3 working with large teams of..." — William Brennan

**Botanist's notes:**
- [2026-02] Blue Origin is a potential type specimen for M6a (Enterprise-Wide Adoption). The 70% company-wide adoption and 95% software engineer adoption, combined with the explicit expectation that 'everyone builds and collaborates with AI agents,' represents the clearest articulation of democratized AI adoption without formal structure we've observed. The internal marketplace model for agent sharing is a distinctive enabler.
- [2026-02] The contextual orientation is unusually explicit here. Unlike other M6a specimens where contextual ambidexterity emerges implicitly, Blue Origin has articulated a clear vision: 'small teams of 2-3 working with large teams of AI agents.' This suggests contextual ambidexterity can be a deliberate design choice, not just an emergent outcome of informal adoption.
- [2026-02] Interesting tension: Blue Origin has no CAIO or AI lab, yet has a clear AI platform strategy (BlueGPT) and articulate AI vision at the executive level. This challenges the assumption that 'unnamed' means 'uncoordinated.' The Enterprise Technology function appears to play a platform-enablement role rather than a governance role—worth distinguishing from M2 Center of Excellence patterns.

**Open questions:**
- What is the budget/headcount specifically allocated to BlueGPT platform development?
- How is the AI agent marketplace governed - who approves agents, what standards apply?
- What is the relationship between Blue Origin's internal AI work and Jeff Bezos's separate Project Prometheus AI lab?


### bmw — M4 Hybrid/Hub-and-Spoke | Contextual | High

**Description:** BMW has built a mature hub-and-spoke AI organization centered on 'Project AI,' an excellence cluster that provides governance, standards, and a Group-wide AI platform. The central platform organization, led by Marco Görgmaier (VP Enterprise Platforms and Services, Data, Artificial Intelligence), comprises over 1,000 employees dedicated to AI and data, with 10,000+ engineers across platform stacks ...

**Classification rationale:** BMW exhibits a clear M4 Hybrid/Hub-and-Spoke model. The hub is 'Project AI' (led by Michael Würtenberger) which provides central governance, standards, and the Group-wide AI platform. The spokes are individual business departments (development, production, sales, procurement) that build and deploy AI applications within this framework. Marco Görgmaier leads a 1,000+ employee platform organization with 10,000+ engineers across platform stacks and 40,000 users of the data/AI ecosystem. The contextual orientation is appropriate because BMW aims for enterprise-wide adoption where 'nearly every process will be supported by AI' rather than isolating AI in a separate structural unit. Individuals throughout the organization balance exploration (new AI applications) and execution (production AI) within their roles, enabled by a self-service GenAI platform that democratizes access.

**Mechanisms linked:** M5 Deploy to Thousands Before You Know What Works

**Key quotes:**
- "We're scaling artificial intelligence along the value chain, from development and production through to sales." — Marco Görgmaier
- "Very soon, nearly every process at the company will be supported by AI, making us even faster and more precise." — Oliver Zipse
- "We are utilising artificial intelligence throughout our value chain." — Oliver Zipse

**Botanist's notes:**
- [2026-02] BMW represents a mature M4 specimen with unusually precise metrics: 1,000+ dedicated AI employees, 10,000+ platform engineers, 40,000 ecosystem users. The scale clarity (vs. vague 'significant investment' language elsewhere) makes this a valuable benchmark for enterprise M4 implementations.
- [2026-02] The tension between M4 (hub-and-spoke) and contextual orientation is instructive. BMW uses structural mechanisms (Project AI, centralized platform) to enable contextual outcomes (enterprise-wide AI in every process). This suggests M4 may be a *means* to contextual ambidexterity rather than an alternative to it.
- [2026-02] Notable absence of a CAIO despite substantial AI investment. AI leadership reports through enterprise platforms/IT (Görgmaier) rather than a dedicated C-suite role. This may reflect German industrial companies' preference for functional integration over executive layer creation—worth comparing to other European manufacturers.

**Open questions:**
- Specific AI budget as a percentage of total R&D
- Detailed reporting structure between Project AI and business units
- How CES 2026 and Neue Klasse platform specifically integrate AI capabilities


### cvs-health — M4 Hybrid/Hub-and-Spoke | Contextual | High

**Description:** CVS Health operates a hybrid AI structure with dual central leadership—Ali Keshavarz as Chief Data Analytics & AI Officer since September 2021 and Tilak Mandadi as EVP Ventures and Chief Experience and Technology Officer since 2022—while distributing AI execution across all four business units. The company has explicitly rejected the trend of creating standalone Chief AI Officer roles, with Mandad...

**Classification rationale:** CVS exhibits classic hub-and-spoke: central AI leadership (Keshavarz as CDAIO, Mandadi as Chief Experience/Technology Officer) sets standards and platforms while AI execution is distributed across Aetna, CVS Caremark, CVS Pharmacy, and Oak Street Health. The contextual orientation is explicitly articulated—Mandadi rejected creating a CAIO role as 'mistaking a tool for a solution,' instead embedding AI into existing roles (nurses, pharmacists, call center agents). Workers balance exploration and execution within their jobs, not in separate units.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works, M8 Turn Compliance Into Deployment Advantage

**Key quotes:**
- "The absolute worst thing that companies can do is create a chief AI officer role. That is by far the worst thing that co..." — Tilak Mandadi
- "AI allows us to take the stupid out of work and allows us to do the real value-added work." — Tilak Mandadi
- "If we give the ownership of health care data to the patient, to the member, to the consumer, nobody else should have con..." — Tilak Mandadi

**Botanist's notes:**
- [2026-02] CVS presents a philosophically articulate M4—Mandadi's 'chief cellular phone officer' analogy is the clearest executive rejection of the AI-czar model in the collection. This suggests M4 may be the 'mature' end-state for enterprises that have thought through organizational design.
- [2026-02] The dual-leadership structure (Keshavarz for data/AI capability, Mandadi for technology/experience) is an interesting M4 variant—the 'hub' is itself divided. This may be more common in healthcare where data governance and technology platform concerns are distinct.
- [2026-02] CVS exhibits strong contextual orientation with structural scaffolding—they have central AI leaders but explicitly design for AI to be embedded in existing roles rather than separated. This is contextual ambidexterity enabled by hub-and-spoke infrastructure, challenging a clean structural/contextual binary.

**Open questions:**
- What is the size of Keshavarz's AI/data team? Headcount not disclosed.
- How does AI governance work between Keshavarz (data/AI) and Mandadi (technology/experience)? Reporting lines unclear.
- What is the breakdown of the $20B between AI specifically vs. broader tech modernization?


### deere-and-co — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Deere & Co has transformed from a 187-year-old agricultural equipment manufacturer into a technology company that now employs more software engineers than mechanical engineers. The company's AI strategy centers on a hub-and-spoke model where CTO Jahmy Hindman's organization sets standards and coordinates acquisitions, while specialized units execute domain-specific AI work with significant autonom...

**Classification rationale:** Deere exemplifies classic hub-and-spoke: CTO Jahmy Hindman provides central technology leadership and coordination, while specialized acquired units (Blue River Technology for computer vision, Bear Flag Robotics for autonomy) operate as distinct spokes with concentrated AI talent. The research explicitly notes Blue River has the 'largest concentration of AI talent' and these units maintain technical autonomy within the Deere umbrella. This is not M2 (pure CoE) because the spokes are autonomous execution units, not just enablement. The structural orientation is clear—exploration happens in dedicated acquired units with separate talent pools, while execution integrates into Deere's product lines.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M3 Embed Product at Research Frontier

**Key quotes:**
- "Technology is core to Deere's DNA, but we don't create tech for tech's sake. There's purpose behind everything we do, so..." — John May
- "[CES] gives us a chance to show how our purpose-driven technology has a huge impact on our customers. Our goal is to mak..." — John May
- "Our agriculture, construction, and commercial landscaping customers all have work that must get done at certain times of..." — Jahmy Hindman

**Botanist's notes:**
- [2026-02] Deere represents a clean M4 case where the 'spokes' were explicitly acquired rather than organically developed. Blue River ($305M) and Bear Flag ($250M) provide concentrated AI talent pools that maintain technical identity within the Deere umbrella. This acquisition-based spoke creation may be a distinct pattern for legacy industrials that lack internal AI talent.
- [2026-02] The 'more software engineers than mechanical engineers' observation marks a structural inflection point. This is not just adding AI capability—it's a fundamental rebalancing of organizational expertise. The hub-and-spoke model may be particularly suited for this transition because it allows legacy mechanical expertise to coexist with acquired software talent.
- [2026-02] CEO May's CES keynote framing—'purpose-driven technology' rather than 'tech for tech's sake'—suggests how legacy industrials legitimate AI investment internally. The labor shortage and sustainability narratives provide economic and social justification that pure efficiency arguments might not.

**Open questions:**
- Exact headcount of AI/ML engineers across all units (Blue River, Bear Flag, internal teams)
- Whether Blue River and Bear Flag operate as distinct P&Ls or are fully integrated
- Specific reporting relationship between CTO and the acquired company leaders


### delta-air-lines — M4 Hybrid/Hub-and-Spoke | Contextual | Medium

**Description:** Delta Air Lines operates a hybrid AI structure with a central Enterprise Data & AI organization reporting through the Chief Digital and Technology Officer (CDTO), who sits on the CEO's Leadership Committee. This central team sets standards and builds core AI capabilities, while implementation is distributed across operational domains—TechOps for predictive maintenance, commercial teams for AI-driv...

**Classification rationale:** Delta exhibits classic M4 Hub-and-Spoke: central Enterprise Data & AI organization under the CDTO sets standards and builds core capabilities, while AI implementation is distributed across operational domains (TechOps predictive maintenance, pricing/revenue management, crew scheduling, customer experience). The 'augmented intelligence' philosophy—where AI empowers frontline workers rather than replaces them—signals contextual ambidexterity: individuals across the organization balance exploration and execution within their roles. Not M2 (pure CoE) because there's clear distributed execution in business units. Not M6 because there IS a named central AI function. Innovation hubs (The Hangar, Sustainable Skies Lab) add ideation capacity but don't dominate the structure.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M7 Put Executives on the Tools

**Key quotes:**
- "I think of AI more as augmented intelligence rather than artificial intelligence...ensuring that the human is still at t..." — Ed Bastian
- "New marvels like AI, the digital revolution and sustainable technology are giving us incredible tools to transform the t..." — Ed Bastian
- "But amid the wonder of new technology, we've always understood that the entire point of innovation is to lift people up." — Ed Bastian

**Botanist's notes:**
- [2026-02] Delta's 'augmented intelligence' framing is notable: it's a deliberate rhetorical move to position AI as worker-empowering rather than worker-replacing. This contextual orientation is reinforced by the structural choice to embed AI across business functions rather than concentrate it in a separate research unit. The philosophy may shape adoption patterns more than the formal structure.
- [2026-02] The innovation hub layer (Hangar, Sustainable Skies Lab) creates interesting complexity within M4. These aren't pure research labs (not M1) nor embedded product teams (not M3), but ideation centers that feed the central-to-distributed pipeline. This suggests M4 may need a sub-variant for orgs with dedicated ideation capacity alongside hub-and-spoke execution.
- [2026-02] Ed Bastian's skepticism about the AI 'bubble' is unusual for a visible AI-adopting CEO. His measured rollout (1% of pricing AI-driven, multi-year expansion) reflects this caution. This creates tension between the public AI evangelism (CES keynote) and the actual deployment pace—worth tracking whether this represents strategic patience or structural friction.

**Open questions:**
- Size of Enterprise Data & AI team - headcount not disclosed
- Specific AI R&D budget vs. embedded technology investment
- Reporting relationship between Ash Naseer (Enterprise Data & AI) and CDTO


### disney — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Disney operates a sophisticated three-layer AI structure that combines fundamental research, governance/enablement, and distributed business unit execution. At the research frontier, Disney Research Studios in Zurich (established 16+ years ago) conducts world-class research in visual computing, machine learning, and AI for filmmaking, with close ties to ETH Zürich and additional locations in Los A...

**Classification rationale:** Disney exhibits classic M4 Hybrid/Hub-and-Spoke: (1) Disney Research Studios in Zurich provides fundamental research capability (16+ years, led by Chief Scientist Markus Gross), (2) the new Office of Technology Enablement provides central governance/standards without centralizing execution, and (3) business units (Disney+, Parks, Studios) retain decision rights on their AI projects. The OTE explicitly 'does NOT take over or centralize' business unit AI—this is coordination and enablement, not command. The $1B OpenAI partnership adds a strategic external layer. Structural orientation because exploration (Research Studios, OTE) and execution (business unit AI) are organizationally distinct. Secondary M1 classification reflects the genuine research lab component in Zurich.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M3 Embed Product at Research Frontier

**Key quotes:**
- "This deal does is by giving us the ability to curate what has been basically created by Sora onto Disney Plus is it jump..." — Bob Iger
- "We'd rather participate in the rather dramatic growth, rather than just watching it happen." — Bob Iger
- "Creativity is the new productivity, and I think you're starting to see that more and more." — Bob Iger

**Botanist's notes:**
- [2026-02] Disney presents an unusually mature M4 variant where the 'hub' is actually bifurcated: Disney Research Studios (16+ years, fundamental research) and Office of Technology Enablement (new, governance/enablement) serve different functions. Research Studios is almost M1-like in character, while OTE is pure M2 governance. The combination creates a sophisticated capability stack that few organizations achieve.
- [2026-02] The explicit design principle that OTE 'does NOT take over or centralize' business unit AI projects is structurally interesting—it's a conscious rejection of the command-and-control model that many enterprises default to. This suggests an intentional architectural choice to preserve business unit autonomy while providing coordination and standards.
- [2026-02] The $1B OpenAI partnership reveals a 'buy vs. build' decision at the generative AI frontier—Disney is buying Sora capability rather than trying to build it internally. This is economically rational given Disney's core competency is IP/storytelling not foundation model development, but it creates an interesting dependency on an external partner for a potentially strategic capability.

**Open questions:**
- What is the budget/headcount for Disney Research Studios?
- How does AI work integrate between Research Studios and the new Office of Technology Enablement?
- What specific AI capabilities has Disney deployed in Parks/Experiences beyond announced initiatives?


### exxonmobil — M6 Unnamed/Informal | Contextual | Medium

**Description:** ExxonMobil operates an unnamed/informal AI structure where AI capabilities are coordinated through Global Business Services and embedded within a centralized technology organization, rather than through a formal AI lab or branded center. The company has approximately 668 data scientists distributed across business units, with key roles including an AI Operations Manager and Digital Transformation ...

**Classification rationale:** ExxonMobil has no formal AI lab, CAIO, or branded AI center. AI capabilities are coordinated through Global Business Services (GBS) and embedded within a centralized technology organization that integrates IT with traditional engineering. The ~668 data scientists are distributed across business units rather than centralized. CEO Woods frames AI as enabling 'effectiveness rather than just cost efficiency' as a 'long-term evolution' — suggesting contextual ambidexterity where individuals balance exploration and execution within their roles. The $15B cost savings target by 2027 positions AI as an operational enabler rather than a separate exploration function.

**Key quotes:**
- "And, actually, with respect to your AI question, and Jensen, we now have because of those investments that we've made th..." — Darren Woods
- "seismic interpretation typically takes anywhere from twelve to eighteen months" — Dr. Xiaojung Huang
- "We can not scale anything up if we do not have a developed data foundation." — Dr. Xiaojung Huang

**Botanist's notes:**
- [2026-02] ExxonMobil exemplifies how legacy industrial firms adopt AI without formal AI organizations — the ~668 distributed data scientists and lack of CAIO/CDO suggests AI is treated as an operational capability rather than strategic function. This is classic M6b where the 'unnamed' quality reflects organizational conservatism about AI branding.
- [2026-02] The data foundation constraint is revealing: 'We can not scale anything up if we do not have a developed data foundation.' This suggests a sequencing pattern where M6b firms must solve enterprise data integration before AI can move from pockets to platform. Historical silos are the binding constraint.
- [2026-02] Interesting dual positioning: ExxonMobil is simultaneously an AI adopter (internal operations) and AI enabler (data center power supplier). CEO discusses Jensen Huang and low-carbon data centers but frames this as energy business opportunity rather than AI strategy. The company sees itself as 'molecule company not electron company' — AI is a customer, not an identity.

**Open questions:**
- What is the actual AI budget or spending within the $27-29B annual CapEx?
- How does the AI Operations team size compare to other energy majors?
- What is the governance structure for AI decisions - who approves new AI initiatives?


### fedex — M4 Hybrid/Hub-and-Spoke | Contextual | Medium

**Description:** FedEx has built its AI capability around FedEx Dataworks, an internal data intelligence arm that serves as the central hub for data platform development, AI model training, and technology standards. The unit is led by the Chief Digital and Information Officer (CDIO), who reports directly to CEO Raj Subramaniam and oversees all data, technology, and cybersecurity functions. This consolidation under...

**Classification rationale:** FedEx operates a clear hub-and-spoke model: FedEx Dataworks serves as the central AI/data platform (the hub), led by a Chief Digital and Information Officer reporting directly to the CEO. However, execution is pushed to the spokes through an enterprise-wide AI education program launched in December 2025, training employees in their existing roles rather than creating separate AI units. This is contextual ambidexterity—individuals are expected to balance AI exploration within their operational work. The CDIO consolidates all data, AI, technology, and cybersecurity under one leader, providing centralized standards while business functions apply AI to domain-specific problems (logistics optimization, customer service, routing). The Innovation Lab handles external startup investments as a separate mechanism for exploration.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works, M7 Put Executives on the Tools

**Key quotes:**
- "The future of business is being shaped by data and AI more than ever before." — Raj Subramaniam
- "We move 17 million packages per day through the global system. That generates multiple petabytes of data. We realised th..." — Raj Subramaniam
- "The fuel for AI is data. If you don't have your data appropriately organised, then there are limits of what you can do w..." — Raj Subramaniam

**Botanist's notes:**
- [2026-02] FedEx represents a clean M4 Hybrid/Hub-and-Spoke with unusually explicit contextual orientation. The December 2025 enterprise-wide AI education program is a deliberate bet that AI capability should be distributed through training rather than organizational restructuring—individuals balance exploration and execution in their existing roles. This is rare to see stated so explicitly; most M4 specimens have structural spokes.
- [2026-02] The 'FedEx Dataworks' naming is interesting—it's not called an 'AI Lab' or 'AI Center,' but a 'data intelligence arm.' This reflects Subramaniam's 'fuel for AI is data' philosophy and may explain why they avoided the M2 Center of Excellence trap: they frame it as platform/infrastructure rather than governance/standards, even though it performs both functions.
- [2026-02] Subramaniam's candor about humanoid robotics being 'not ready for prime time' is structurally significant—it suggests temporal separation within the portfolio (operational AI now, frontier robotics later) while maintaining contextual integration for the mature AI tools. This could be an emerging pattern: contextual orientation for proven AI, temporal orientation for speculative bets.

**Open questions:**
- What is the headcount of FedEx Dataworks specifically?
- What percentage of total R&D budget goes to AI initiatives?
- How is the relationship structured between FedEx Dataworks and business unit AI applications?


### ford — M4 Hybrid/Hub-and-Spoke | Structural | Medium

**Description:** Ford operates one of the most distributed AI structures in the automotive industry, with multiple specialized units pursuing different AI applications at varying time horizons. The flagship AI unit is Latitude AI, a 550-person wholly owned subsidiary headquartered in Pittsburgh focused on hands-free, eyes-off automated driving technology. Unlike most corporate AI labs, Latitude operates with its o...

**Classification rationale:** Ford exhibits classic M4 Hybrid/Hub-and-Spoke with multiple distributed AI units operating with significant autonomy: Latitude AI (550-person autonomous driving subsidiary), Greenfield Labs (~300 researchers in Palo Alto), FARIC (Atlanta software/AI center), and a Doug Field-led skunkworks for affordable EVs. The Ford+ restructuring that separated Model e (EVs), Ford Blue (ICE), and Ford Pro (commercial) represents textbook structural ambidexterity—exploration and execution physically and organizationally separated. Latitude AI operates as a wholly owned subsidiary with its own C-suite, which is unusual even for M4 organizations. The skunkworks under Doug Field adds an M8 secondary element for radical EV innovation.

**Mechanisms linked:** M1 Protect Off-Strategy Work

**Key quotes:**
- "Artificial intelligence is gonna replace literally half of all white-collar workers in the U.S." — Jim Farley
- "AI will leave a lot of white-collar people behind." — Jim Farley
- "There's more than one way to the American Dream, but our whole education system is focused on four-year [college] educat..." — Jim Farley

**Botanist's notes:**
- [2026-02] Ford's Latitude AI represents an unusually autonomous M4 spoke—operating as a wholly owned subsidiary with its own CEO, CTO, and President is rare for corporate AI units. This creates a structural independence that borders on M5b (Venture Builder) but without the intent to spin off. The taxonomy may need to distinguish between 'subsidiary autonomy' and 'division autonomy' within M4.
- [2026-02] CEO Farley's public framing of AI is almost entirely about workforce transformation rather than product/technology. His 'essential economy' thesis—that AI will devastate white-collar work while skilled trades become more valuable—is a distinctive strategic narrative that shapes how Ford positions its AI investments. This workforce-centric framing is rare among automotive CEOs.
- [2026-02] The Ford+ restructuring (Model e/Blue/Pro separation) combined with multiple innovation centers (Latitude AI, Greenfield Labs, FARIC, skunkworks) creates a nested structural ambidexterity: exploration vs. execution separated at both the division level AND within the innovation portfolio. This 'ambidexterity within ambidexterity' pattern may warrant taxonomic attention.

**Open questions:**
- What is Ford's total AI R&D budget as a percentage of overall R&D spend?
- How does AI governance work across Model e, Ford Blue, and Ford Pro divisions?
- What is the reporting relationship between Latitude AI and Ford corporate leadership?


### general-motors — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** General Motors operates a Hybrid/Hub-and-Spoke model for AI, combining a small elite Silicon Valley Center of Excellence with larger distributed teams executing in manufacturing and autonomous driving. The AI Center of Excellence, opened in Mountain View in 2024, initially employed fewer than 20 elite hires from Google, Meta, and AWS to advise divisions on AI capabilities, secure partnerships, and...

**Classification rationale:** GM established a classic hub-and-spoke model with a small elite AI Center of Excellence (<20 people) in Silicon Valley setting standards while distributed teams (100+ at Autonomous Robotics Center) execute in manufacturing and autonomous driving. The November 2025 CAIO departure and subsequent reorganization—moving AI under manufacturing engineering—signals evolution toward more embedded execution. This fits M4 requirements: central standards + distributed execution. The Cruise subsidiary also operated as a semi-independent M5b venture, though its operational challenges led to tighter integration. The structural separation between AI enablement (manufacturing) and AI product (autonomous/software) is clear.

**Mechanisms linked:** M6 Merge Competing AI Teams Under Single Leader, M3 Embed Product at Research Frontier

**Key quotes:**
- "It's more than just a vehicle. It makes your life easier, more streamlined, and – more importantly – safer." — Mary Barra
- "Human beings have more tolerance for human mistakes than they do for technology mistakes." — Mary Barra
- "We are strategically integrating AI capabilities directly into our business and product organizations, enabling faster i..." — GM Spokesperson

**Botanist's notes:**
- [2026-02] The 8-month CAIO tenure is a striking data point on whether centralized AI leadership works in traditional industrial companies. GM's rapid pivot from C-suite CAIO to manufacturing-embedded AI suggests the hub-and-spoke model may naturally evolve toward more embedded structures (M3) in manufacturing contexts where AI value is tied to operational expertise.
- [2026-02] GM presents an interesting contrast to tech-company AI framing. The explicit positioning that 'It's not about automating everything' and the deliberate choice to complement rather than transform automotive expertise suggests a category of 'AI-skeptical-but-investing' traditional manufacturers that may warrant its own pattern in synthesis.
- [2026-02] Cruise as a semi-independent M5b venture offers a foil: when venture-style AI independence meets safety-critical domains, governance gaps emerge. The subsequent tighter integration suggests traditional companies may struggle to maintain the autonomy that venture models require while managing enterprise risk.

**Open questions:**
- What specific factors led to CAIO Turovsky's departure after only 8 months? Was there strategic misalignment or execution challenges?
- How does Cruise's safety incidents and operational pullback affect GM's overall AI strategy and risk tolerance?
- Will GM appoint a new CAIO or is the distributed model the new permanent structure?


### honda — M4 Hybrid/Hub-and-Spoke | Structural | Medium

**Description:** Honda structures AI work through a multi-tiered Hybrid/Hub-and-Spoke model that separates fundamental research, enterprise adoption, and product ventures into distinct organizational units. The Honda Research Institutes (HRI) form a global network with locations in Silicon Valley, Japan, and Europe, focused on long-horizon fundamental research in autonomous driving, robotics, machine learning, and...

**Classification rationale:** Honda operates a classic Hybrid/Hub-and-Spoke model with three distinct structural layers: (1) Honda Research Institutes (HRI) — a global network with USA, Japan, and Europe locations focused on fundamental AI research (autonomous driving, robotics, machine learning, quantum computing); (2) American Honda IT organization handling enterprise generative AI adoption with centralized governance and Microsoft partnership; (3) Sony Honda Mobility JV pursuing AI-native product development (AFEELA). The HRI labs set research direction while enterprise AI operates under IT with clear autonomy. The AFEELA JV functions as a secondary M5 Venture Builder. This multi-tiered structure is distinctly Structural in orientation — exploration and execution are separated into distinct organizational units with different time horizons and governance structures.

**Mechanisms linked:** M1 Protect Off-Strategy Work

**Key quotes:**
- "The biggest challenge we have is keeping up with the speed of change." — Bob Brizendine
- "At Honda, we began using generative AI to support our designers' ability to demonstrate their creativity." — Toshihiro Mibe
- "Generative AI will generate design drawings of future mobility." — Toshihiro Mibe

**Botanist's notes:**
- [2026-02] Honda's tripartite structure — research institutes, enterprise IT, and JV venture — tests the M4 vs M5 boundary. The Sony Honda Mobility JV functions as a distinct M5 Venture Builder within an M4 Hub-and-Spoke parent structure, suggesting some large enterprises may layer multiple models rather than choosing one.
- [2026-02] The absence of a CAIO or central AI strategy committee at Honda Motor corporate (Japan) while American Honda IT has clear AI governance authority suggests geographic fragmentation in AI leadership. This regional autonomy pattern may be common in Japanese multinationals.
- [2026-02] Brizendine's quote about 'keeping up with the speed of change' reveals a classic execution-focused IT leader struggling with exploration demands — yet Honda addresses this through structural separation (let HRI explore, let IT execute) rather than asking IT to become ambidextrous.

**Open questions:**
- What is the total AI/ML headcount across all Honda Research Institutes globally?
- What portion of Honda's ~$8B annual R&D spend is allocated to AI specifically?
- How do the HRI labs coordinate with American Honda's enterprise AI initiatives?


### honeywell — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Honeywell operates a Hybrid/Hub-and-Spoke AI structure with clear separation between internal AI (CDTO Sheila Jordan) and product AI (CTO Suresh Venkatarayalu). A central gen AI program leader manages an 'ambassador' network across all functions and business units, governed by a 'six-chapter framework' covering employee workflows, engineering applications, cognitive automation, commercial platform...

**Classification rationale:** Honeywell exhibits a textbook hub-and-spoke model: a central gen AI program leader reports to CDTO Sheila Jordan, with 'ambassadors' distributed across each function and strategic business unit. The six-chapter framework provides central standards while business units execute against their specific use cases. There is also clear structural separation between internal AI (Jordan's team) and product/go-to-market AI (CTO Venkatarayalu's team). The ambassador network and regular cross-functional meetings demonstrate the hub-spoke coordination pattern. Secondary M2 designation reflects the Singapore and Pittsburgh Centers of Excellence for specific domains.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works

**Key quotes:**
- "Every function and every strategic business unit is now using gen AI." — Sheila Jordan
- "I think our chapters will work for any enterprise." — Suresh Venkatarayalu
- "This company looks at use cases first, value second." — Suresh Venkatarayalu

**Botanist's notes:**
- [2026-02] Honeywell's 'ambassador' model is a notable variant of M4 hub-and-spoke: rather than having dedicated AI staff in each business unit, they have designated employees who bridge between their home function and the central AI team. This creates lighter-weight coordination than full embedded teams while maintaining distributed sensing for use cases.
- [2026-02] The explicit CDTO/CTO split between internal AI and product AI is unusually clean organizational design. Most M4 specimens blur this boundary. Honeywell has essentially created two parallel spokes—one for exploration (product AI under Venkatarayalu) and one for execution (internal AI under Jordan)—with the hub coordinating both.
- [2026-02] Kapur's 'automated vs. autonomous' framing and emphasis on 'physical AI' positions Honeywell distinctively in the industrial sector. Unlike software companies deploying gen AI for knowledge work, Honeywell is building toward AI that controls physical systems—a different technical and organizational challenge that may require different structural models as the technology matures.

**Open questions:**
- Exact size of central AI team vs. distributed ambassadors
- Specific budget allocation for AI initiatives
- How AI organization will change post-3-way split (Aerospace, Automation, Advanced Materials)


### intel — M4 Hybrid/Hub-and-Spoke | Structural | Medium

**Description:** Intel operates a hybrid hub-and-spoke model for AI, with Intel Labs serving as the fundamental research hub and product groups executing AI commercialization. Intel Labs houses 700+ researchers across 30+ technical disciplines, including the dedicated AI Lab focused on video and multimodal foundation models and the Emergent AI Research Lab. This research arm operates on multi-year horizons, explor...

**Classification rationale:** Intel exhibits classic hub-and-spoke architecture: Intel Labs (700+ researchers) operates as a distinct research hub doing fundamental AI work on multi-year horizons, while product groups (CCG, DCAI, custom ASIC) execute AI products on quarterly/annual cycles. The CEO now directly leads AI strategy (the hub) after CTO departure, with flattened reporting giving him direct visibility into both research and execution. The Central Engineering Group was created to unify horizontal functions across spokes. Clear structural separation between exploration (Labs) and execution (product units) justifies Structural orientation.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M11 Flatten Management Layers to Speed AI Decisions

**Key quotes:**
- "It has been a tough period for quite a long time for Intel. We fell behind on innovation. As a result, we have been too ..." — Lip-Bu Tan
- "I'm not happy with our current position. I know that you are not happy either. I have heard the feedback loud and clear...." — Lip-Bu Tan
- "It's clear to me that organizational complexity and bureaucratic processes have been slowly suffocating the culture of i..." — Lip-Bu Tan

**Botanist's notes:**
- [2026-02] Intel presents an interesting case of M4 hub-and-spoke where the 'hub' is being reconfigured in real-time. The CTO departure to OpenAI created a vacuum that CEO Tan filled by pulling AI strategy directly to himself. This is unusual — most M4 models have a dedicated executive running the hub, not the CEO. The flattening may be temporary turnaround structure or a lasting design choice.
- [2026-02] The 'bureaucracy kills innovation' framing is explicit structural critique rare in our specimen collection. Tan is not just reorganizing — he's publicly diagnosing structural pathology. The memo language ('suffocating the culture of innovation', 'takes too long to make decisions', 'unnecessary silos') provides unusually candid evidence for Mechanism 11 (Flatten Management Layers).
- [2026-02] Intel Labs as secondary M1 component is noteworthy — 700+ researchers is larger than many pure M1 Research Labs in our collection. The tension between this protected research capacity and the urgent product-side catch-up to NVIDIA creates a live experiment in ambidexterity under competitive pressure.

**Open questions:**
- How is AI research prioritization decided between Intel Labs and product groups?
- What is the specific headcount of the AI and Advanced Technologies Group?
- How will the NVIDIA partnership change internal AI chip development strategy?


### kroger — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Kroger structures its AI work through 84.51°, a data science subsidiary that operates the 'AI Factory' platform. This platform functions as a centralized hub providing shared infrastructure, governance frameworks, and reusable accelerators. Business units across the grocery chain operate as spokes, developing and deploying AI solutions closest to their operational problems while leveraging hub res...

**Classification rationale:** Kroger operates an explicit Hub+Spoke model through their 'AI Factory' platform. The hub (84.51°) provides shared infrastructure, reusable components, base models, and governance, while business 'spokes' execute AI development closest to operational problems. This is textbook M4: central capability-building (governance, tooling, accelerators) with distributed execution (business units deploying AI to their specific domains). The structural separation between 84.51° as a distinct subsidiary and Kroger business units confirms Structural orientation.

**Mechanisms linked:** M8 Turn Compliance Into Deployment Advantage

**Key quotes:**
- "Accelerating our AI efforts is a natural step for Kroger, given our long history of leadership in data and machine learn..." — Ron Sargent
- "Our collaboration with NVIDIA supports Kroger's 'Fresh for Everyone' commitment. We look forward to learning more about ..." — Wesley Rhodes
- "Responsible AI is not a checkbox, instead it is something that should be embedded into how we build, deploy and scale AI..." — Kristin Foster

**Botanist's notes:**
- [2026-02] Kroger's use of a data science subsidiary (84.51°) as the hub is an interesting M4 variant. Unlike tech companies where central AI teams are internal, Kroger's hub is a legally distinct entity that also serves external clients. This 'subsidiary-as-hub' pattern may offer stronger ring-fencing of AI capability and clearer P&L accountability than typical corporate CoEs.
- [2026-02] The 'AI Factory' naming and explicit Hub+Spoke terminology suggest Kroger has internalized platform thinking for AI capability-building. This self-awareness about organizational structure is relatively rare — most M4 specimens evolve into hub-spoke naturally without explicitly architecting it. Worth tracking whether deliberate structural design yields better outcomes than organic evolution.
- [2026-02] Grocery retail may be an underappreciated sector for AI structural innovation. Like Walmart (M5c platform-to-product), Kroger has decades of loyalty data and operational complexity that create unique AI opportunities. The 84.51° model of monetizing retail data science externally while also serving the parent suggests an interesting blended M4/M5 potential that the current taxonomy may not fully capture.

**Open questions:**
- What is Rodney McMullen's current status? Ron Sargent was listed as interim CEO in Q2 2025 earnings materials.
- Specific AI headcount and budget figures not disclosed.
- How does the AI Governance Council interact with business unit decision-making in practice?


### lockheed-martin — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Lockheed Martin operates a mature Hybrid/Hub-and-Spoke AI model anchored by the Lockheed Martin AI Center (LAIC), established in 2021. The hub provides centralized infrastructure—an NVIDIA DGX SuperPOD processing over 1 billion tokens per week—along with MLOps tooling, training programs, and enterprise-wide governance. Mike Baylor serves as VP and Chief Digital and AI Officer, leading a 300+ perso...

**Classification rationale:** Lockheed Martin exemplifies the hub-and-spoke model: the Lockheed Martin AI Center (LAIC) serves as a centralized hub providing compute infrastructure (NVIDIA DGX SuperPOD), MLOps tools, training, and governance standards. The 7,000 engineers across all business areas act as spokes, accessing the AI Factory for their domain-specific applications. The December 2024 launch of Astris AI subsidiary adds an M5c (Platform-to-Product) secondary dimension, but the core operating model remains hub-and-spoke with structural separation between the central AI capability and distributed execution teams.

**Mechanisms linked:** M8 Turn Compliance Into Deployment Advantage, M10 Productize Internal Operational Advantages

**Key quotes:**
- "AI that's secure and reliable is critical to the success of complex missions in defense of freedom" — Jim Taiclet
- "we don't have to write all the AI software that we'll ever need" — Jim Taiclet
- "to be the AI leader in Aerospace and Defense, with our discriminator being trustworthy AI for mission assurance" — Mike Baylor

**Botanist's notes:**
- [2026-02] Lockheed Martin presents a textbook M4 hub-and-spoke with an interesting secondary M5c pattern. The Astris AI spinout (December 2024) commercializes internal AI Factory capabilities—a direct example of Mechanism 10 (Productize Internal Operational Advantages). This dual structure (M4 primary, M5c secondary) may be common in regulated industries where internal capability building precedes external productization.
- [2026-02] The defense sector's unique regulatory environment creates a 'compliance-as-moat' dynamic (Mechanism 8). Taiclet explicitly frames 'trustworthy AI for mission assurance' as a competitive discriminator. This suggests regulated industries may develop different AI structural patterns than tech-native firms—compliance requirements shape the hub's governance role more heavily.
- [2026-02] The Craig Martell appointment (former DoD CDAO) alongside existing CDAIO Mike Baylor creates an interesting dual-executive structure: CTO for technology innovation, CDAIO for AI strategy/capability, CIO for operational integration. This three-way split is unusual and worth tracking—it may indicate defense-sector-specific complexity in AI governance.

**Open questions:**
- How does AI work flow between classified and unclassified environments? The AI Factory handles both, but the governance mechanisms are unclear.
- What is the precise reporting relationship between CDAIO Baylor and CEO Taiclet? Is Baylor C-suite or VP level?
- How does the new CTO Craig Martell's role interact with CDAIO Baylor's? Is there a division between AI/digital (Baylor) and broader tech (Martell)?


### lowes — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Lowe's has constructed a sophisticated hybrid AI structure that separates exploration from execution while maintaining strong central governance. Lowe's Innovation Labs, operating as a semi-independent subsidiary in Kirkland, WA, pursues long-horizon exploration in spatial computing, digital twins (Babylon project demonstrated at NVIDIA GTC), and emerging platforms like Apple Vision Pro. Meanwhile...

**Classification rationale:** Lowe's exhibits clear M4 hub-and-spoke architecture with multiple specialized units: (1) Lowe's Innovation Labs in Kirkland, WA operates as a semi-independent exploration arm with 2-5 year horizons on spatial computing and digital twins; (2) AI Transformation Office provides centralized governance using a four-metric vetting framework; (3) Charlotte Tech Hub serves as a center of excellence for 2,000 tech roles; (4) Chandhu Nair's AI/Data platform team abstracts complexity for developers enterprise-wide; (5) embedded execution in stores via Mylow Companion on Zebra devices. The structural separation between exploration (Innovation Labs) and execution (store rollouts, engineering tools) with centralized standards (Transformation Office) is textbook hub-and-spoke.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works, M7 Put Executives on the Tools

**Key quotes:**
- "Rather than thinking about it solely as a job replacement tool, how do you think about reducing someone's workload by 50..." — Marvin Ellison
- "Achieving this milestone places Lowe's in an elite tier of companies that are not just experimenting with AI, but operat..." — Marvin Ellison
- "When our customers engage with Mylow online, the conversion rate more than doubles." — Marvin Ellison

**Botanist's notes:**
- [2026-02] Lowe's provides a clean exemplar of how M4 Hub-and-Spoke can incorporate an M1-like exploration arm (Innovation Labs) without being classified as M1. The key differentiator is that Innovation Labs is one spoke among several, not the central identity of the AI structure. The presence of the AI Transformation Office as a governance hub, the Charlotte Tech Hub as an execution center, and Nair's platform team as an enablement layer creates a multi-hub architecture that is distinctly M4.
- [2026-02] The Innovation Labs subsidiary structure is unusually clean for retail—physically separated (Kirkland vs. Charlotte), organizationally independent, with 2-5 year exploration horizons on spatial computing and digital twins. This suggests large retailers may need subsidiary-level separation to protect exploration from quarterly retail pressure, similar to what we see in M8 Skunkworks but without the secrecy emphasis.
- [2026-02] Ellison's explicit framing of AI as '50% workload reduction' rather than headcount reduction is notable as a rhetorical choice that may enable faster adoption. The 'AI isn't going to fix a hole in your roof' quote positions AI as complementary to skilled trades rather than threatening—a potentially important contingency for retail/service organizations with large frontline workforces.

**Open questions:**
- Specific size of Chandhu Nair's AI/Data team and exact reporting relationship to Godbole
- AI headcount vs. total tech headcount (2,000 in Tech Hub but unclear how many focus on AI)
- Specific CapEx or OpEx allocation to AI initiatives


### mayo-clinic — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Mayo Clinic operates a sophisticated multi-hub AI architecture designed to enable both clinical AI deployment and external innovation. Three distinct C-suite leaders coordinate different aspects: the Chief AI Implementation Officer (Micky Tripathi) governs enterprise AI implementation and safety; the Chief Data and Analytics Officer (Ajai Sehgal) runs the 'AI Factory' for rapid model development a...

**Classification rationale:** Mayo Clinic has a clear multi-hub structure with distinct central functions: CAIO (Tripathi) for implementation governance, CDAO (Sehgal) for AI enablement and the 'AI Factory', and Mayo Clinic Platform (Halamka) for external innovation and commercialization. AI execution is distributed across clinical departments (Neurology AI, Digital Pathology, Cardiovascular, Radiology) led by physician-scientists. The Platform unit has M5 characteristics—productizing internal capabilities (algorithms, data assets) for external partners and startups—but the dominant pattern is hub-and-spoke coordination across the enterprise. Strong structural separation between exploration (Platform, research) and execution (clinical deployment).

**Mechanisms linked:** M8 Turn Compliance Into Deployment Advantage, M10 Productize Internal Operational Advantages, M3 Embed Product at Research Frontier

**Key quotes:**
- "We knew that we could incorporate AI and make it better." — Gianrico Farrugia
- "Let's create a different architecture. And that architecture had to be very closely linked to artificial intelligence." — Gianrico Farrugia
- "AI is not about replacing the human touch in healthcare. It's about enhancing it—giving doctors and nurses better tools ..." — Micky Tripathi

**Botanist's notes:**
- [2026-02] Mayo represents a rare 'multi-hub' M4 variant where multiple C-suite leaders coordinate distinct AI functions (CAIO for governance, CDAO for enablement, Platform for commercialization). Most M4 specimens have a single central hub with distributed spokes—Mayo has three specialized hubs. This may warrant a sub-type for 'federated hub' architectures in highly regulated industries.
- [2026-02] The nonprofit mission framing creates interesting structural constraints: Farrugia and Tripathi consistently frame AI in service terms ('serve the people who serve others') rather than efficiency or shareholder value. This purpose orientation may explain why Mayo invests heavily in validation infrastructure (Platform_Validate) and global health applications rather than purely internal cost reduction.
- [2026-02] The 'AI Factory' concept under CDAO Sehgal deserves closer examination—it appears to be a standardized development capability that sits between research (Department of AI & Informatics) and clinical deployment (embedded teams). This middle layer for rapid prototyping may be a structural innovation worth tracking across other healthcare specimens.

**Open questions:**
- Exact size of centralized AI teams vs. embedded clinical AI staff
- Specific budget allocation to AI vs. overall R&D spending
- Governance relationship between CAIO and CDAO roles—how do they coordinate?


### mercedes-benz — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Mercedes-Benz has constructed a sophisticated multi-hub AI organization that positions AI as the new definition of automotive luxury. MBRDNA in Silicon Valley serves as the self-designated 'global AI center' with 600+ employees across six North American locations (Sunnyvale, San Jose, Long Beach, Carlsbad, Ann Arbor, Seattle), focusing on AI experiences, autonomous driving, and compute architectur...

**Classification rationale:** Mercedes-Benz exhibits a textbook hub-and-spoke model with multiple specialized hubs: MBRDNA in Silicon Valley (600+ employees) serves as the 'global AI center' for vehicle AI and autonomous driving; Digital Factory Campus in Berlin-Marienfelde handles manufacturing/production AI; and global tech hubs in Germany, Bangalore, Beijing, Shanghai, and Tel Aviv provide distributed execution. The May 2025 appointment of a Chief Data & AI Officer formalizes central governance, while MB.OS provides the architectural standards that enable distributed product teams to execute. Clear structural separation between exploration (MBRDNA research, academic partnerships) and execution (product integration, manufacturing AI).

**Key quotes:**
- "From this point forward, every Mercedes will have a supercomputer in it. Every Mercedes will have a full sensor suite." — Ola Källenius
- "So you have your own butler in the car." — Ola Källenius
- "The old paradigm...that approach is completely over." — Ola Källenius

**Botanist's notes:**
- [2026-02] Mercedes-Benz presents a multi-hub M4 variant where hubs are functionally specialized rather than just geographically distributed: MBRDNA for vehicle AI/autonomy, Digital Factory Campus for manufacturing AI. This raises the question of whether M4 should distinguish between geographic spokes vs. functional spokes.
- [2026-02] The tension between CSO (Magnus Östberg, owning MB.OS and product AI) and CDAIO (Daniel Eitler, owning enterprise AI/data) suggests a potential split in AI governance that our taxonomy doesn't explicitly capture. Product AI vs. enterprise AI may require different structural models within the same organization.
- [2026-02] Källenius's framing of 'every Mercedes will have a supercomputer' as the architectural foundation—with MB.OS routing between competing LLMs (Gemini, ChatGPT)—represents an interesting platform-as-arbiter pattern. The OS becomes the central coordination mechanism, not the AI team. This may be an emerging pattern for hardware-software companies.

**Open questions:**
- Exact headcount of AI-focused engineers globally (only MBRDNA's 600+ is specified)
- Organizational relationship between CDAIO Daniel Eitler and CSO Magnus Östberg - do they share AI responsibility?
- Budget allocation specifically for AI vs. broader software/R&D


### mount-sinai-health-system — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Mount Sinai Health System operates one of the most mature hub-and-spoke AI structures in healthcare, anchored by the Hamilton and Amabel James Center for AI and Human Health—a 65,000 square foot, 12-story facility that houses the first dedicated AI department in a US medical school. The Windreich Department of AI and Human Health, led by Chief AI Officer Girish Nadkarni, serves as the central hub ...

**Classification rationale:** Mount Sinai exhibits textbook M4 Hybrid/Hub-and-Spoke structure: the Hamilton and Amabel James Center for AI and Human Health serves as the central hub (65,000 sq ft, 12-story dedicated facility with 40+ PIs and 250+ staff), while distributed teams deploy AI across the eight-hospital system. The Windreich Department creates enterprise 'AI Fabric' infrastructure centrally, while Clinical Data Science and Digital Technology Partners teams execute in specific clinical contexts. CAIO Nadkarni explicitly advocates for 'infrastructure that spans the enterprise' with a 'hub-and-satellite model.' M2 Center of Excellence is secondary because the Windreich Department also provides governance, standards, and enablement functions. Orientation is clearly Structural—exploration (research department with 3-10 year horizons) and execution (clinical deployment with 6-24 month horizons) are housed in distinct organizational units.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M4 Consumer-Grade UX for Employee Tools, M8 Turn Compliance Into Deployment Advantage

**Key quotes:**
- "Think about building infrastructure that spans the enterprise, not just point solutions, and build to scale, not to pilo..." — Girish Nadkarni
- "If you sort of meet people where they are and include them in the change management process, that becomes this self-perp..." — Girish Nadkarni
- "We can't offer Silicon Valley salaries, but health systems are the place to make an immediate, measurable, and visible i..." — Girish Nadkarni

**Botanist's notes:**
- [2026-02] Mount Sinai represents an unusually clean M4 specimen in healthcare—most health systems lack both the philanthropic funding and academic structure to create a true research hub. The Blackstone-funded James Center provides physical and financial separation that enables structural ambidexterity rarely seen in the sector. This may be a distinctive 'academic health system' variant of M4 where the hub is explicitly academic rather than corporate.
- [2026-02] The dual CAIO/CDTO structure is notable: Nadkarni owns research and infrastructure, Freeman owns deployment and experience. This separation of 'build the platform' from 'deploy the applications' creates clear swim lanes that may be essential in high-regulatory environments where accountability must be unambiguous.
- [2026-02] Nadkarni's framing of 'infrastructure that spans the enterprise, not point solutions' and Freeman's '5% technology, 95% people/process' suggest healthcare AI leaders are converging on a shared playbook that prioritizes organizational change over technical sophistication. This may be a sector-specific adaptation to high regulatory intensity.

**Open questions:**
- Specific budget/investment figures for AI initiatives
- Total AI headcount across the three pillars (Windreich, DTP, Clinical Data Science)
- Details on the relationship between CEO Brendan Carr and AI leadership


### netflix — M4 Hybrid/Hub-and-Spoke | Contextual | Medium

**Description:** Netflix operates a distributed AI research structure where teams are explicitly NOT centralized — instead, nine research areas span Analytics, Computer Vision and Graphics, Consumer Insights, Encoding & Quality, Experimentation & Causal Inference, Machine Learning, Machine Learning Platform, NLP & Conversations, and Recommendations. These teams work in close collaboration with business and enginee...

**Classification rationale:** Netflix explicitly states that research is NOT centralized — teams are distributed across 9 research areas and work 'in close collaboration with business teams.' However, dedicated hubs exist: AIMS (AI for Member Systems) handles member-facing AI including recommendations and GenAI, while Eyeline Studios conducts VFX/computer vision research. This creates a hub-and-spoke pattern where central capabilities (AIMS, Eyeline, Netflix Research) set standards and conduct deep research, while distributed teams embed AI into specific products. The contextual orientation is indicated by the philosophy that individuals balance exploration and execution within their roles — researchers are expected to drive 'high impact' and work directly with business teams, rather than being isolated in a separate exploration unit.

**Mechanisms linked:** M3 Embed Product at Research Frontier, M4 Consumer-Grade UX for Employee Tools

**Key quotes:**
- "We remain convinced that AI represents an incredible opportunity to help creators make films and series better, not just..." — Ted Sarandos
- "I remain convinced that there's an even bigger opportunity to make movies 10% better. So, our talent today is using AI t..." — Ted Sarandos
- "I look at Gen AI as a tool for creators to create content, not for Netflix to create instead of creators. So I feel like..." — Ted Sarandos

**Botanist's notes:**
- [2026-02] Netflix presents an interesting M4 variant where the 'hub' is NOT a traditional central AI lab but rather specialized functional hubs (AIMS for member experience, Eyeline for VFX) that coexist with deeply distributed research. The explicit statement that research is 'NOT centralized' challenges the typical hub-and-spoke framing — this is more like 'multiple small hubs plus pervasive distribution.'
- [2026-02] The 'better not cheaper' framing is distinctive and may warrant tracking as a purpose-claim pattern. Sarandos has articulated this consistently since 2024, positioning AI as quality-enhancing rather than cost-reducing. This is unusual in an industry under margin pressure.
- [2026-02] Netflix's contextual orientation is unusually explicit — the research website literally states that researchers work 'in close collaboration with business teams.' Most orgs claim this but Netflix appears to have built it into the structural DNA, with experimentation culture enabling individuals to balance exploration and execution.

**Open questions:**
- Size of AIMS team specifically — how many researchers/engineers?
- What percentage of Netflix's R&D budget goes to AI/ML research?
- Relationship between Eyeline Studios and Netflix Research — are they the same or separate?


### nike — M4 Hybrid/Hub-and-Spoke | Contextual | Medium

**Description:** Nike operates a hybrid AI structure with a central Data & AI team led by Chief Data and AI Officer Alan John, responsible for AI innovation strategy, data platform modernization, and cloud infrastructure. This central capability enables hyper-personalized consumer experiences, operational intelligence, and digital growth at scale. The Nike Sport Research Lab (NSRL) in Beaverton serves as a special...

**Classification rationale:** Nike has a dedicated Chief Data and AI Officer (Alan John) running a central data/AI/cloud function — the 'hub' — while AI capabilities are embedded across the organization in supply chain (under COO), the Nike Sport Research Lab, and consumer-facing applications — the 'spokes'. The December 2025 restructuring eliminating the CTO role and moving tech under the COO signals operational integration rather than standalone tech leadership. The emphasis on 'embedding digital, data and AI across the business' (per former CTO Dogan) points to contextual orientation where individuals across the org balance AI exploration and execution within their roles, rather than structural separation into distinct units.

**Key quotes:**
- "experience, innovative mindset and team-first leadership style will be key as we continue to evolve into a more agile, t..." — Elliott Hill
- "We're getting sharper on innovative product. Emotionally inspiring storytelling. And we're paying it off in an integrate..." — Elliott Hill

**Botanist's notes:**
- [2026-02] Nike's December 2025 restructuring — eliminating the CTO and moving tech under the COO — represents an interesting organizational choice that challenges the assumption that AI leadership requires standalone C-suite representation. This may signal a broader trend of AI becoming 'infrastructure' (like IT) rather than a strategic function.
- [2026-02] The coexistence of a CDAIO (Alan John) with technology reporting to the COO creates an ambiguous reporting structure. This specimen would benefit from clarity on whether the CDAIO is the 'hub' or whether the COO now owns the hub, with CDAIO as one spoke among many.
- [2026-02] Nike's M4 classification is complicated by the NSRL, which operates with research lab characteristics (motion capture, biomechanics, long-term product innovation) but isn't positioned as an AI lab per se. It's a performance science lab that uses AI as a tool — a distinction worth tracking as other companies may embed AI in domain-specific research facilities rather than creating AI-branded labs.

**Open questions:**
- Where does Alan John (CDAIO) report — to the COO, CEO, or elsewhere after the Dec 2025 restructuring?
- What is the size of Nike's central Data & AI team?
- What happened to the 'Transformational Generative AI Initiative' after Loveland's departure?


### pepsico — M4 Hybrid/Hub-and-Spoke | Contextual | High

**Description:** PepsiCo operates a Hybrid/Hub-and-Spoke model for AI transformation, with a central transformation organization of 700-1,000 data engineers, software engineers, and data scientists reporting to Chief Strategy & Transformation Officer Athina Kanioura, who reports directly to CEO Ramon Laguarta. Two Digital Hubs in Dallas and Barcelona serve as Centers of Excellence, creating 500+ new data and digit...

**Classification rationale:** PepsiCo exhibits a clear M4 Hybrid/Hub-and-Spoke structure: a central transformation organization under CSTO Athina Kanioura (700-1,000 engineers) sets standards and coordinates strategy, while two Digital Hubs (Dallas, Barcelona) function as Centers of Excellence, and 'mission-based teams' execute cross-functional programs with autonomy. The contextual orientation is evidenced by the initiative to train all 330,000 employees on AI—expecting everyone to incorporate AI in their roles rather than delegating to specialists. The 'four or five big bets' prioritization model with central governance (AI Council) plus distributed execution confirms the hub-and-spoke topology.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works, M7 Put Executives on the Tools

**Key quotes:**
- "The scale and complexity of PepsiCo's business, from farm to shelf, is massive—and we are embedding AI throughout our op..." — Ramon Laguarta
- "It's a huge transformation." — Ramon Laguarta
- "We're going to put agentic AI across the spectrum. It will be an ecosystem of agents that we want to deploy for the tran..." — Athina Kanioura

**Botanist's notes:**
- [2026-02] PepsiCo presents an interesting M4 variant where the CSTO role bundles AI with strategy, M&A, and transformation—rather than a dedicated CAIO. This 'embedded AI leadership' pattern may be more common in consumer goods where AI is a capability within broader transformation rather than a standalone strategic bet. The recent addition of Latin America Foods CEO responsibilities to Kanioura's role (Dec 2025) suggests the organization values leaders who can bridge technology and operations.
- [2026-02] The contextual orientation here is particularly strong: training 330,000 employees on AI is an unusually ambitious commitment to broad-based capability building. Most M4 specimens maintain clearer separation between hub specialists and spoke generalists. PepsiCo's approach suggests contextual ambidexterity can coexist with hub-and-spoke structure when the hub focuses on enablement rather than monopolizing execution.
- [2026-02] The 'four or five big bets' prioritization model with AI Council governance represents a distinctive mechanism for managing exploration within a complex, geographically distributed organization. This 'portfolio of bets with central governance' pattern could be a common adaptation for global consumer goods companies that need both strategic coherence and local execution flexibility.

**Open questions:**
- What is the annual AI/digital budget allocation?
- How many of the 700-1,000 engineers are specifically AI/ML focused vs. general software?
- What are the specific metrics for the 'four or five big bets'?


### progressive — M6 Unnamed/Informal | Contextual | Medium

**Description:** Progressive operates as a data-driven 'tech-first insurer' with AI deeply embedded across operations — claims processing, risk pricing, marketing personalization, and fraud detection — but without a formally branded AI organization or dedicated Chief AI Officer. Their structural approach is invisible by design: AI capability is distributed across functional areas rather than housed in a central re...

**Classification rationale:** Progressive demonstrates sophisticated AI capability across claims, pricing, marketing, and fraud detection without any formal AI organization, named lab, or dedicated CAIO. Their 20+ year telematics heritage (14 billion miles of Snapshot data) shows organic, bottom-up capability development rather than a top-down transformation initiative. AI appears distributed across business functions with external partnerships (H2O.ai, Claritas) providing platform infrastructure. This is classic 6b: real AI capability without organizational theater. Contextual orientation fits because individuals across claims, underwriting, and marketing balance AI exploitation within their operational roles — there's no structural separation between AI exploration and execution.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works

**Key quotes:**
- "given us access to segments of the auto insurance markets that we normally did not attract" — Ray Voelker

**Botanist's notes:**
- [2026-02] Progressive exemplifies 'AI as infrastructure' rather than 'AI as strategy' — the absence of organizational theater (no CAIO, no named lab, no conference presence) paired with substantial operational AI deployment challenges our taxonomy's implicit assumption that sophisticated AI requires visible structural commitment. This may be the mature end-state that named labs evolve toward.
- [2026-02] The 20+ year telematics data foundation creates an interesting path dependency: Progressive's AI capability emerged organically from data assets rather than from an AI strategy. This 'data-first, AI-second' trajectory may be common in insurance but is underrepresented in our specimen collection which skews toward tech-forward announcements.
- [2026-02] The buy-over-build approach (H2O.ai for ML platform, Claritas for GenAI) suggests a variant of 6b where the 'central team' is actually external partners managed by distributed business units. This partnership-centric model deserves more taxonomic attention — it may be how many incumbents actually operationalize AI.

**Open questions:**
- Who leads AI/ML capability at Progressive? Is there a head of data science or analytics?
- How is the H2O.ai partnership structured? Is there an internal team that manages it?
- What is Tricia Griffith's actual position on AI? No public quotes from her on the topic were found.


### sutter-health — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Sutter Health has constructed one of the more mature AI organizational structures in non-profit healthcare, anchored by the May 2025 appointment of Ashley Beecy, MD as Chief AI Officer — a dedicated C-suite AI role still rare in the sector. The structure follows a hub-and-spoke model: a physical Innovation Center at San Francisco's Pier 1 (11,000 sq ft, 7-year lease signed January 2024) serves as ...

**Classification rationale:** Sutter Health exhibits a clear hub-and-spoke model: the SF Pier 1 Innovation Center serves as a physical hub for experimentation and partnerships, while a dedicated CAIO (Ashley Beecy) provides enterprise-wide governance. Multiple C-suite AI-adjacent roles (CDO, CIO, CCIO, CDAO) coordinate distributed implementation across 21 hospitals. The cross-functional governance structure vets each AI use case centrally, while deployment happens at the edges through vendor partnerships (Aidoc, Abridge, Hyro). Secondary M2 classification reflects the strong AI Center of Excellence characteristics with Aidoc partnership. Structural orientation is clear: exploration (Innovation Center, VC investments) and execution (enterprise AI deployment) occur in distinct organizational units.

**Mechanisms linked:** M8 Turn Compliance Into Deployment Advantage, M5 Deploy to Thousands Before You Know What Works

**Key quotes:**
- "One of our goals is to be a leader in health care AI." — Warner Thomas
- "We want to really position ourselves to be a leader in AI, and really applying AI so it gets at scale to all of our prov..." — Laura Wilt
- "It's not one single algorithm. It's really this platform that we can apply across all types of imaging." — Laura Wilt

**Botanist's notes:**
- [2026-02] Sutter represents an unusually mature M4 implementation for healthcare — a sector where regulatory complexity often pushes orgs toward slower, more centralized M2 structures. The physical Innovation Center hub combined with CAIO-led governance creates clear structural separation between exploration and execution, making this a strong healthcare exemplar of hub-and-spoke ambidexterity.
- [2026-02] The CAIO role (Ashley Beecy) is notable: a physician-informaticist with prior industry experience at IBM and Citibank. This hybrid clinical-technical background may be a pattern worth tracking for healthcare AI leadership — the role requires fluency in both clinical safety reasoning and technology deployment.
- [2026-02] Sutter's buy-versus-build partnership strategy (Aidoc, Abridge, Hyro, Ferrum) is structurally interesting — it allows faster deployment velocity while concentrating internal resources on governance and integration rather than algorithm development. This may be an emerging M4 variant for regulated industries: 'governance hub + vendor spokes' rather than 'R&D hub + product spokes.'

**Open questions:**
- What is Ashley Beecy's direct reporting structure — does she report to CEO Warner Thomas directly?
- What is Sutter's total AI investment budget or CapEx commitment?
- How does the cross-functional governance group make decisions — unanimous consent, executive override, etc.?


### t-mobile — M4 Hybrid/Hub-and-Spoke | Structural | Medium

**Description:** T-Mobile operates a Hybrid/Hub-and-Spoke AI model that separates network infrastructure AI from customer-facing AI applications. The central hub is the AI-RAN Innovation Center in Bellevue, WA, established in partnership with NVIDIA, Ericsson, and Nokia. This center houses NVIDIA's ARC-1 supercomputer and focuses on long-horizon network optimization—what Sievert calls the '5G Advanced era and beyo...

**Classification rationale:** T-Mobile exhibits clear hub-and-spoke characteristics: a centralized AI-RAN Innovation Center in Bellevue (the hub) with NVIDIA supercomputer and major vendor partnerships handles network AI exploration, while customer-facing AI (IntentCX) is distributed across product teams reporting to CIO, CPO, and President of Innovation. The absence of a CAIO and the explicit distribution of AI responsibilities across multiple executives confirms this is not M2 (pure center of excellence). The structural separation between network AI (long-horizon exploration) and customer AI (near-term execution) indicates Structural orientation rather than Contextual.

**Mechanisms linked:** M1 Protect Off-Strategy Work

**Key quotes:**
- "Just like T-Mobile led in 5G, we intend to lead in the next wave of network technology, for the benefit of our customers..." — Mike Sievert
- "AI-RAN has tremendous potential to completely transform the future of mobile networks, but it will be difficult to get r..." — Mike Sievert
- "We are a technology leader who's transformed from a telecommunications company to a tech company." — Mike Sievert

**Botanist's notes:**
- [2026-02] T-Mobile's M4 classification is distinctive because the 'hub' is explicitly an Innovation Center for network AI (AI-RAN) rather than a typical CoE for governance/standards. This is exploration-focused hub, not enablement-focused—closer to M1 Research Lab in function but organizationally M4 in structure because customer AI is distributed to product teams.
- [2026-02] The absence of a CAIO with explicit distribution of AI across CIO, CPO, and President of Innovation is notable. This 'no single throat to choke' model may reflect telecom's infrastructure-heavy nature where AI touches multiple domains (network, customer, operations) that don't naturally report to one function.
- [2026-02] T-Mobile's framing of itself as 'transformed from a telecommunications company to a tech company' (Sievert) combined with major partnerships (NVIDIA, OpenAI) suggests a buy-vs-build strategy that may be distinctive for telecom. The reliance on external partners for core AI capabilities contrasts with tech companies building in-house.

**Open questions:**
- What is the exact size of T-Mobile's internal AI/ML team? (Job postings suggest teams exist but headcount unclear)
- How does the AI-RAN Innovation Center report into the corporate structure?
- What is the total investment level in AI initiatives?


### toyota — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** Toyota operates one of the most clearly articulated multi-layered AI structures in global manufacturing. At the exploration end sits Toyota Research Institute (TRI), a Silicon Valley-based R&D subsidiary founded in 2016 with a $1 billion initial investment. Led by Chief Scientist Gill Pratt (former DARPA official), TRI pursues long-horizon breakthroughs in autonomous driving, robotics, materials s...

**Classification rationale:** Toyota exhibits a textbook Hybrid/Hub-and-Spoke structure with multiple distinct AI entities operating at different time horizons: (1) Toyota Research Institute (TRI) serves as a pure research hub with $1B investment, 3-10 year horizon, focused on autonomous driving, robotics, and fundamental AI; (2) Enterprise AI within TMNA handles near-term productivity and deployment; (3) GAIA bridges research to production; (4) Woven by Toyota operates as an automated driving startup. The structural separation is explicit—different organizations, different leaders, different mandates. TRI could qualify as M1 Research Lab on its own, making it a strong secondary model.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M3 Embed Product at Research Frontier

**Key quotes:**
- "There is tremendous enthusiasm across global Toyota for leveraging AI to improve speed and efficiency in everything from..." — Gill Pratt
- "We're now able to analyze and leverage all forms of content — structured and unstructured." — Brian Kursar
- "Our AI-powered coding tools have boosted developer productivity by at least 20%." — Brian Kursar

**Botanist's notes:**
- [2026-02] Toyota exemplifies the M4 Hybrid/Hub-and-Spoke model at its most elaborate—not just a central hub plus spokes, but multiple specialized hubs (TRI for research, Enterprise AI for productivity, Woven for automated driving) with explicit bridging mechanisms (GAIA). This raises questions about whether very large enterprises naturally evolve toward multi-hub architectures rather than simple hub-spoke patterns.
- [2026-02] Incoming CEO Kon's candid admission that Toyota trails Tesla in AI is structurally revealing—despite $1B+ investment in TRI since 2016, Toyota's structural separation may have created exploration excellence without sufficient execution velocity. The 'we can learn from them' framing suggests the M4 structure may need recalibration toward faster deployment.
- [2026-02] Brian Kursar's dual role—Head of Enterprise AI and TRI technical advisor for GAIA—is an interesting personnel-based integration mechanism. Rather than relying purely on structural processes, Toyota uses key individuals to bridge the exploration-execution divide. This 'boundary spanner' pattern may be underappreciated in the taxonomy.

**Open questions:**
- What is TRI's current headcount and budget (post-initial $1B investment)?
- How many people are in the Enterprise AI organization?
- What is the total AI R&D spend across Toyota Group companies?


### uber — M4 Hybrid/Hub-and-Spoke | Structural | Medium

**Description:** Uber structures AI work through a classic hub-and-spoke architecture centered on Uber AI Labs, founded in December 2016 through the acquisition of Geometric Intelligence. The lab operates two explicit programs: 'Core' for fundamental research in areas like Bayesian optimization, neuroevolution, and reinforcement learning, and 'Connections' for integrating AI capabilities with product teams across ...

**Classification rationale:** Uber AI Labs operates as an explicit hub-and-spoke model with 'Core' (fundamental research) and 'Connections' (product integration) programs—this is textbook M4. The central research function sets standards while distributed product teams embed AI into routing, pricing, and matching. Additionally, Uber AI Solutions represents an M5c-like productization of internal data labeling capabilities for external clients. AV strategy has shifted from internal skunkworks (ATG, divested 2020) to partnership-based execution. The structural separation between AI Labs, embedded platform AI, and the commercialized AI Solutions unit is clear evidence of structural ambidexterity.

**Mechanisms linked:** M5 Deploy to Thousands Before You Know What Works, M10 Productize Internal Operational Advantages

**Key quotes:**
- "Play-acting is how many businesses approach AI... saying the right words about AI without changing how their operations ..." — Dara Khosrowshahi
- "Allowing the AI actually to reason through that and throwing away all of the old policies is turning out to be the most ..." — Dara Khosrowshahi
- "You have to survive through a bunch of car crashes internally to do so." — Dara Khosrowshahi

**Botanist's notes:**
- [2026-02] Uber's explicit 'Core and Connections' naming for AI Labs programs is a rare case of self-aware hub-and-spoke design—most M4 specimens evolve into this structure accidentally. The nomenclature suggests deliberate organizational design thinking.
- [2026-02] The ATG divestiture (2020) and shift to AV partnerships represents an interesting structural evolution: from M8 Skunkworks to what might be called 'externalized exploration'—keeping platform coordination internally while outsourcing the hardest R&D to partners. This pattern may warrant a new subtype for M4.
- [2026-02] Uber AI Solutions productizing internal data labeling capabilities (M10 mechanism) is structurally similar to Walmart GoLocal and Amazon AWS—platform companies monetizing operational capabilities. But unlike those cases where the product targets external logistics/compute buyers, Uber is selling to other AI labs, creating an unusual B2B-AI-services revenue stream.

**Open questions:**
- What is Zoubin Ghahramani's current scope and reporting relationship? Is AI Labs still active under that name or evolved?
- How large is the AI Solutions (data labeling) business unit? Revenue? Headcount?
- Did Raquel Urtasun and the Toronto hub remain after ATG divestiture, or did they move to Aurora?


### ulta-beauty — M4 Hybrid/Hub-and-Spoke | Contextual | High

**Description:** Ulta Beauty has established a formal AI Center of Excellence under Chief Technology and Transformation Officer Mike Maresca, bringing together AI/ML engineers from across the organization into a central hub. This hub develops capabilities and standards that are then deployed across business functions—supply chain optimization, payroll and scheduling tools for associates, and personalization engine...

**Classification rationale:** Ulta Beauty exhibits clear M4 characteristics: a central AI Center of Excellence under CTTO Mike Maresca develops capabilities and standards, while distributed teams (Digital Innovation, Supply Chain, Marketing) apply AI to their specific domains. The Virtual Beauty Advisor and GlamLab products show hub-developed capabilities deployed across channels. Orientation is Contextual because AI is being embedded throughout the organization—associates use scheduling tools, supply chain uses ML optimization, marketing uses personalization—rather than exploration being isolated in a separate unit. The CDO's quote about AI enabling 'more human connection' and CEO's 'way of being' framing both emphasize contextual integration over structural separation.

**Mechanisms linked:** M4 Consumer-Grade UX for Employee Tools, M5 Deploy to Thousands Before You Know What Works

**Key quotes:**
- "Our teams are adapting well to our new ways of working and we are steadily advancing our optimization efforts. During th..." — Kecia Steelman
- "There is no finish line in our technology and our investments." — Kecia Steelman
- "Our investments to elevate the digital experience and accelerate personalization are really driving both channels up." — Kecia Steelman

**Botanist's notes:**
- [2026-02] Ulta Beauty presents a clean M4 case with an interesting dual-head structure: CTTO owns the AI Center of Excellence (capability development) while CDO owns digital innovation (consumer-facing applications). This creates potential coordination challenges but also allows specialized focus—a variant worth tracking as more retailers split AI leadership this way.
- [2026-02] The 'way of being' framing from CEO Steelman is notable for a contextual orientation—it explicitly frames AI not as a separate initiative but as embedded in organizational culture. This rhetoric aligns with contextual ambidexterity theory (Gibson & Birkinshaw) where the organization develops behavioral capacity for both exploration and exploitation rather than structural separation.
- [2026-02] The agentic AI decision point (unified assistant vs. specialized agents) represents a live structural choice that could shift the model. If they choose specialized agents deployed to different functions, it reinforces M4; if they choose a unified assistant, it could push toward M2 with stronger central control. Worth tracking in future layers.

**Open questions:**
- Exact size/headcount of AI Center of Excellence team
- Specific budget allocation for AI vs. broader technology investments
- Reporting structure details — whether AI CoE reports through CTTO, CDO, or matrix structure


### unitedhealth-group — M4 Hybrid/Hub-and-Spoke | Structural | High

**Description:** UnitedHealth Group operates what may be the largest healthcare AI deployment in the United States, with over 1,000 production use cases and 20,000 engineers leveraging AI tools. The organization follows a classic hub-and-spoke model: central governance through the Responsible AI Board (20-25 internal and external experts) and United AI Studio platform provides standards and oversight, while distri...

**Classification rationale:** UnitedHealth exhibits textbook M4 hub-and-spoke structure: central governance through Responsible AI Board (20-25 experts) and United AI Studio platform, with distributed execution across business units (UnitedHealthcare, Optum, OptumRx). Clear separation of exploration (Optum Labs R&D, academic partnerships) from execution (1,000+ production use cases). Monthly business unit reviews plus quarterly CIO cross-enterprise monitoring creates formal coordination mechanisms. The dedicated Chief AI Scientist for governance plus Chief AI Transformation Officer for strategy indicates structural separation of AI functions.

**Mechanisms linked:** M8 Turn Compliance Into Deployment Advantage, M4 Consumer-Grade UX for Employee Tools

**Key quotes:**
- "AI is never used to deny a claim. If a claim is not eligible to be approved, it goes up to a human agent." — Sandeep Dadlani
- "We want AI to be a tool" — Sandeep Dadlani
- "It's clear that our traditional services in Optum Insight have to evolve to AI-first services, then to products, and eve..." — Sandeep Dadlani

**Botanist's notes:**
- [2026-02] UnitedHealth exemplifies how hub-and-spoke (M4) can scale to massive production deployment (1,000+ use cases) when governance infrastructure is treated as deployment enablement rather than constraint. The Responsible AI Board with external experts is not just compliance theater—it's the mechanism that allows them to move fast across business units because approval pathways are clear.
- [2026-02] The three-way split of AI leadership (Chief AI Scientist for governance, Chief AI Transformation Officer for strategy, CDTO for execution) is an interesting structural pattern worth tracking. It suggests that at sufficient scale, the AI leadership function itself may require structural separation—exploration of governance standards vs. transformation strategy vs. operational execution.
- [2026-02] Notable absence from external AI conference circuit despite massive deployment. UnitedHealth prefers controlled investor/healthcare venues. This may reflect regulatory sensitivity (DOJ scrutiny) or deliberate strategy to avoid attention while scaling. Contrast with tech companies that aggressively publicize AI capabilities.

**Open questions:**
- Exact reporting lines for Chief AI Scientist (Pencina) vs Chief AI Transformation Officer (Mohiuddin) vs CDTO (Dadlani) - who reports to whom?
- Size and composition of Optum Labs team specifically
- What percentage of $1.5B tech investment is specifically AI vs broader technology?


### visa — M4 Hybrid/Hub-and-Spoke | Structural | Medium

**Description:** Visa operates a hybrid AI structure with a dedicated central research hub (Visa Research) and distributed AI deployment across its payments products. Visa Research, led by SVP Wang Min since 2015, employs 24+ research scientists working on foundational AI including machine learning security, trustworthy AI, explainable AI, and graph neural networks. This research function is complemented by a Data...

**Classification rationale:** Visa exhibits classic hub-and-spoke characteristics: a dedicated central research organization (Visa Research with 24+ AI scientists) that conducts foundational work in ML security, trustworthy AI, and graph neural networks, while AI capabilities are deployed across distributed product domains (fraud detection, agentic commerce, VisaNet payments infrastructure). The presence of distinct leadership for research (Wang Min, SVP Visa Research Labs) and platforms (Sam Hamilton, SVP Data & AI Platforms) suggests structural separation between exploration and execution. However, confidence is Medium because we lack visibility into decision-rights allocation between central and distributed teams, and no CAIO exists to clarify governance.

**Mechanisms linked:** M1 Protect Off-Strategy Work, M8 Turn Compliance Into Deployment Advantage

**Key quotes:**
- "What powers generative AI is data. We have arguably the largest global payments data set that exists." — Ryan McInerney
- "We are all in an arms race to protect this ecosystem, to protect the network." — Ryan McInerney
- "We've spent billions of dollars, we'll spend billions of dollars protecting the network of networks that we built on beh..." — Ryan McInerney

**Botanist's notes:**
- [2026-02] Visa's M4 classification raises an interesting question about what makes a 'hub' sufficiently central. Visa Research is clearly a dedicated research unit, but without a CAIO, standards-setting authority is ambiguous. The hub may be more 'research outputs' than 'governance mandates'—a softer form of hub-and-spoke than JPMorgan or other financial services M4s with stronger central control.
- [2026-02] The 'data as moat' framing is distinctive. McInerney's emphasis on Visa's payments dataset as the foundation for generative AI suggests the company's AI advantage is less about organizational structure and more about proprietary data assets. This raises questions about whether data-rich incumbents can succeed with less sophisticated AI org structures than pure-play AI companies.
- [2026-02] Absence of a CAIO in a Fortune AIQ 50 #2 company is notable. Visa distributes AI leadership across Research (Wang Min), Platforms (Sam Hamilton), and Technology (Taneja) rather than unifying under a single AI executive. This may reflect AI's deep integration into payments infrastructure—it's not a separate 'AI strategy' but embedded in core operations.

**Open questions:**
- Specific AI headcount beyond the ~24 research scientists
- What percentage of R&D budget goes to AI specifically
- How AI decisions are governed across research vs. product teams



    ## Taxonomy Feedback Summary

    - **anduril**: [2026-02] Anduril is the clearest type specimen for M9 AI-Native — there is no transformation story because AI was the founding premise. This makes it uniquely valuable for contrast: what does AI structure look like when there's no legacy to overcome? The absence of a CAIO role is telling; AI leadership is unnecessary when AI is assumed, not added.
- **anduril**: [2026-02] The 'no separate AI team' structure at Anduril challenges a core assumption in the taxonomy: most models assume AI is a *function* that must be positioned somewhere. For AI-native orgs, this framing may not apply. Lattice is more like an operating system than a team — it's infrastructure that all product divisions build on, similar to how no one asks 'where is the electricity team?'
- **anduril**: [2026-02] The AI Grand Prix competition represents a novel talent acquisition mechanism that sidesteps traditional AI hiring. By running a competition ('If you think you can build an autonomy stack that can out-fly the world's best, show us'), Anduril turns hiring into product development. This suggests AI-native orgs may develop different organizational forms for talent acquisition, not just product development.
- **bloomberg**: [2026-02] The 'hammers looking for nails' quote is one of the clearest articulations of contextual ambidexterity in our specimen collection—AI experts are explicitly positioned as embedded problem-seekers rather than isolated researchers. This contrasts with structural separation models where AI teams wait for problems to be brought to them.
- **bloomberg**: [2026-02] Bloomberg's 15-year AI timeline (since 2009) challenges narratives of 'AI transformation'—this is an organization that has been incrementally building capability, not pivoting. The M4 hub-and-spoke structure may be a natural end-state for mature AI organizations that started with M2/M3 models years ago.
- **bloomberg**: [2026-02] The founder-CEO (Michael Bloomberg) is notably absent from AI messaging despite the company bearing his name. All AI communication comes from CTO and Head of AI Strategy. This may indicate either delegation maturity or that AI is treated as technical infrastructure rather than strategic identity—worth comparing to founder-led AI messaging at other specimens.
- **blue-origin**: [2026-02] Blue Origin is a potential type specimen for M6a (Enterprise-Wide Adoption). The 70% company-wide adoption and 95% software engineer adoption, combined with the explicit expectation that 'everyone builds and collaborates with AI agents,' represents the clearest articulation of democratized AI adoption without formal structure we've observed. The internal marketplace model for agent sharing is a distinctive enabler.
- **blue-origin**: [2026-02] The contextual orientation is unusually explicit here. Unlike other M6a specimens where contextual ambidexterity emerges implicitly, Blue Origin has articulated a clear vision: 'small teams of 2-3 working with large teams of AI agents.' This suggests contextual ambidexterity can be a deliberate design choice, not just an emergent outcome of informal adoption.
- **blue-origin**: [2026-02] Interesting tension: Blue Origin has no CAIO or AI lab, yet has a clear AI platform strategy (BlueGPT) and articulate AI vision at the executive level. This challenges the assumption that 'unnamed' means 'uncoordinated.' The Enterprise Technology function appears to play a platform-enablement role rather than a governance role—worth distinguishing from M2 Center of Excellence patterns.
- **bmw**: [2026-02] BMW represents a mature M4 specimen with unusually precise metrics: 1,000+ dedicated AI employees, 10,000+ platform engineers, 40,000 ecosystem users. The scale clarity (vs. vague 'significant investment' language elsewhere) makes this a valuable benchmark for enterprise M4 implementations.
- **bmw**: [2026-02] The tension between M4 (hub-and-spoke) and contextual orientation is instructive. BMW uses structural mechanisms (Project AI, centralized platform) to enable contextual outcomes (enterprise-wide AI in every process). This suggests M4 may be a *means* to contextual ambidexterity rather than an alternative to it.
- **bmw**: [2026-02] Notable absence of a CAIO despite substantial AI investment. AI leadership reports through enterprise platforms/IT (Görgmaier) rather than a dedicated C-suite role. This may reflect German industrial companies' preference for functional integration over executive layer creation—worth comparing to other European manufacturers.
- **cvs-health**: [2026-02] CVS presents a philosophically articulate M4—Mandadi's 'chief cellular phone officer' analogy is the clearest executive rejection of the AI-czar model in the collection. This suggests M4 may be the 'mature' end-state for enterprises that have thought through organizational design.
- **cvs-health**: [2026-02] The dual-leadership structure (Keshavarz for data/AI capability, Mandadi for technology/experience) is an interesting M4 variant—the 'hub' is itself divided. This may be more common in healthcare where data governance and technology platform concerns are distinct.
- **cvs-health**: [2026-02] CVS exhibits strong contextual orientation with structural scaffolding—they have central AI leaders but explicitly design for AI to be embedded in existing roles rather than separated. This is contextual ambidexterity enabled by hub-and-spoke infrastructure, challenging a clean structural/contextual binary.
- **deere-and-co**: [2026-02] Deere represents a clean M4 case where the 'spokes' were explicitly acquired rather than organically developed. Blue River ($305M) and Bear Flag ($250M) provide concentrated AI talent pools that maintain technical identity within the Deere umbrella. This acquisition-based spoke creation may be a distinct pattern for legacy industrials that lack internal AI talent.
- **deere-and-co**: [2026-02] The 'more software engineers than mechanical engineers' observation marks a structural inflection point. This is not just adding AI capability—it's a fundamental rebalancing of organizational expertise. The hub-and-spoke model may be particularly suited for this transition because it allows legacy mechanical expertise to coexist with acquired software talent.
- **deere-and-co**: [2026-02] CEO May's CES keynote framing—'purpose-driven technology' rather than 'tech for tech's sake'—suggests how legacy industrials legitimate AI investment internally. The labor shortage and sustainability narratives provide economic and social justification that pure efficiency arguments might not.
- **delta-air-lines**: [2026-02] Delta's 'augmented intelligence' framing is notable: it's a deliberate rhetorical move to position AI as worker-empowering rather than worker-replacing. This contextual orientation is reinforced by the structural choice to embed AI across business functions rather than concentrate it in a separate research unit. The philosophy may shape adoption patterns more than the formal structure.
- **delta-air-lines**: [2026-02] The innovation hub layer (Hangar, Sustainable Skies Lab) creates interesting complexity within M4. These aren't pure research labs (not M1) nor embedded product teams (not M3), but ideation centers that feed the central-to-distributed pipeline. This suggests M4 may need a sub-variant for orgs with dedicated ideation capacity alongside hub-and-spoke execution.
- **delta-air-lines**: [2026-02] Ed Bastian's skepticism about the AI 'bubble' is unusual for a visible AI-adopting CEO. His measured rollout (1% of pricing AI-driven, multi-year expansion) reflects this caution. This creates tension between the public AI evangelism (CES keynote) and the actual deployment pace—worth tracking whether this represents strategic patience or structural friction.
- **disney**: [2026-02] Disney presents an unusually mature M4 variant where the 'hub' is actually bifurcated: Disney Research Studios (16+ years, fundamental research) and Office of Technology Enablement (new, governance/enablement) serve different functions. Research Studios is almost M1-like in character, while OTE is pure M2 governance. The combination creates a sophisticated capability stack that few organizations achieve.
- **disney**: [2026-02] The explicit design principle that OTE 'does NOT take over or centralize' business unit AI projects is structurally interesting—it's a conscious rejection of the command-and-control model that many enterprises default to. This suggests an intentional architectural choice to preserve business unit autonomy while providing coordination and standards.
- **disney**: [2026-02] The $1B OpenAI partnership reveals a 'buy vs. build' decision at the generative AI frontier—Disney is buying Sora capability rather than trying to build it internally. This is economically rational given Disney's core competency is IP/storytelling not foundation model development, but it creates an interesting dependency on an external partner for a potentially strategic capability.
- **exxonmobil**: [2026-02] ExxonMobil exemplifies how legacy industrial firms adopt AI without formal AI organizations — the ~668 distributed data scientists and lack of CAIO/CDO suggests AI is treated as an operational capability rather than strategic function. This is classic M6b where the 'unnamed' quality reflects organizational conservatism about AI branding.
- **exxonmobil**: [2026-02] The data foundation constraint is revealing: 'We can not scale anything up if we do not have a developed data foundation.' This suggests a sequencing pattern where M6b firms must solve enterprise data integration before AI can move from pockets to platform. Historical silos are the binding constraint.
- **exxonmobil**: [2026-02] Interesting dual positioning: ExxonMobil is simultaneously an AI adopter (internal operations) and AI enabler (data center power supplier). CEO discusses Jensen Huang and low-carbon data centers but frames this as energy business opportunity rather than AI strategy. The company sees itself as 'molecule company not electron company' — AI is a customer, not an identity.
- **fedex**: [2026-02] FedEx represents a clean M4 Hybrid/Hub-and-Spoke with unusually explicit contextual orientation. The December 2025 enterprise-wide AI education program is a deliberate bet that AI capability should be distributed through training rather than organizational restructuring—individuals balance exploration and execution in their existing roles. This is rare to see stated so explicitly; most M4 specimens have structural spokes.
- **fedex**: [2026-02] The 'FedEx Dataworks' naming is interesting—it's not called an 'AI Lab' or 'AI Center,' but a 'data intelligence arm.' This reflects Subramaniam's 'fuel for AI is data' philosophy and may explain why they avoided the M2 Center of Excellence trap: they frame it as platform/infrastructure rather than governance/standards, even though it performs both functions.
- **fedex**: [2026-02] Subramaniam's candor about humanoid robotics being 'not ready for prime time' is structurally significant—it suggests temporal separation within the portfolio (operational AI now, frontier robotics later) while maintaining contextual integration for the mature AI tools. This could be an emerging pattern: contextual orientation for proven AI, temporal orientation for speculative bets.
- **ford**: [2026-02] Ford's Latitude AI represents an unusually autonomous M4 spoke—operating as a wholly owned subsidiary with its own CEO, CTO, and President is rare for corporate AI units. This creates a structural independence that borders on M5b (Venture Builder) but without the intent to spin off. The taxonomy may need to distinguish between 'subsidiary autonomy' and 'division autonomy' within M4.
- **ford**: [2026-02] CEO Farley's public framing of AI is almost entirely about workforce transformation rather than product/technology. His 'essential economy' thesis—that AI will devastate white-collar work while skilled trades become more valuable—is a distinctive strategic narrative that shapes how Ford positions its AI investments. This workforce-centric framing is rare among automotive CEOs.
- **ford**: [2026-02] The Ford+ restructuring (Model e/Blue/Pro separation) combined with multiple innovation centers (Latitude AI, Greenfield Labs, FARIC, skunkworks) creates a nested structural ambidexterity: exploration vs. execution separated at both the division level AND within the innovation portfolio. This 'ambidexterity within ambidexterity' pattern may warrant taxonomic attention.
- **general-motors**: [2026-02] The 8-month CAIO tenure is a striking data point on whether centralized AI leadership works in traditional industrial companies. GM's rapid pivot from C-suite CAIO to manufacturing-embedded AI suggests the hub-and-spoke model may naturally evolve toward more embedded structures (M3) in manufacturing contexts where AI value is tied to operational expertise.
- **general-motors**: [2026-02] GM presents an interesting contrast to tech-company AI framing. The explicit positioning that 'It's not about automating everything' and the deliberate choice to complement rather than transform automotive expertise suggests a category of 'AI-skeptical-but-investing' traditional manufacturers that may warrant its own pattern in synthesis.
- **general-motors**: [2026-02] Cruise as a semi-independent M5b venture offers a foil: when venture-style AI independence meets safety-critical domains, governance gaps emerge. The subsequent tighter integration suggests traditional companies may struggle to maintain the autonomy that venture models require while managing enterprise risk.
- **honda**: [2026-02] Honda's tripartite structure — research institutes, enterprise IT, and JV venture — tests the M4 vs M5 boundary. The Sony Honda Mobility JV functions as a distinct M5 Venture Builder within an M4 Hub-and-Spoke parent structure, suggesting some large enterprises may layer multiple models rather than choosing one.
- **honda**: [2026-02] The absence of a CAIO or central AI strategy committee at Honda Motor corporate (Japan) while American Honda IT has clear AI governance authority suggests geographic fragmentation in AI leadership. This regional autonomy pattern may be common in Japanese multinationals.
- **honda**: [2026-02] Brizendine's quote about 'keeping up with the speed of change' reveals a classic execution-focused IT leader struggling with exploration demands — yet Honda addresses this through structural separation (let HRI explore, let IT execute) rather than asking IT to become ambidextrous.
- **honeywell**: [2026-02] Honeywell's 'ambassador' model is a notable variant of M4 hub-and-spoke: rather than having dedicated AI staff in each business unit, they have designated employees who bridge between their home function and the central AI team. This creates lighter-weight coordination than full embedded teams while maintaining distributed sensing for use cases.
- **honeywell**: [2026-02] The explicit CDTO/CTO split between internal AI and product AI is unusually clean organizational design. Most M4 specimens blur this boundary. Honeywell has essentially created two parallel spokes—one for exploration (product AI under Venkatarayalu) and one for execution (internal AI under Jordan)—with the hub coordinating both.
- **honeywell**: [2026-02] Kapur's 'automated vs. autonomous' framing and emphasis on 'physical AI' positions Honeywell distinctively in the industrial sector. Unlike software companies deploying gen AI for knowledge work, Honeywell is building toward AI that controls physical systems—a different technical and organizational challenge that may require different structural models as the technology matures.
- **intel**: [2026-02] Intel presents an interesting case of M4 hub-and-spoke where the 'hub' is being reconfigured in real-time. The CTO departure to OpenAI created a vacuum that CEO Tan filled by pulling AI strategy directly to himself. This is unusual — most M4 models have a dedicated executive running the hub, not the CEO. The flattening may be temporary turnaround structure or a lasting design choice.
- **intel**: [2026-02] The 'bureaucracy kills innovation' framing is explicit structural critique rare in our specimen collection. Tan is not just reorganizing — he's publicly diagnosing structural pathology. The memo language ('suffocating the culture of innovation', 'takes too long to make decisions', 'unnecessary silos') provides unusually candid evidence for Mechanism 11 (Flatten Management Layers).
- **intel**: [2026-02] Intel Labs as secondary M1 component is noteworthy — 700+ researchers is larger than many pure M1 Research Labs in our collection. The tension between this protected research capacity and the urgent product-side catch-up to NVIDIA creates a live experiment in ambidexterity under competitive pressure.
- **kroger**: [2026-02] Kroger's use of a data science subsidiary (84.51°) as the hub is an interesting M4 variant. Unlike tech companies where central AI teams are internal, Kroger's hub is a legally distinct entity that also serves external clients. This 'subsidiary-as-hub' pattern may offer stronger ring-fencing of AI capability and clearer P&L accountability than typical corporate CoEs.
- **kroger**: [2026-02] The 'AI Factory' naming and explicit Hub+Spoke terminology suggest Kroger has internalized platform thinking for AI capability-building. This self-awareness about organizational structure is relatively rare — most M4 specimens evolve into hub-spoke naturally without explicitly architecting it. Worth tracking whether deliberate structural design yields better outcomes than organic evolution.
- **kroger**: [2026-02] Grocery retail may be an underappreciated sector for AI structural innovation. Like Walmart (M5c platform-to-product), Kroger has decades of loyalty data and operational complexity that create unique AI opportunities. The 84.51° model of monetizing retail data science externally while also serving the parent suggests an interesting blended M4/M5 potential that the current taxonomy may not fully capture.
- **lockheed-martin**: [2026-02] Lockheed Martin presents a textbook M4 hub-and-spoke with an interesting secondary M5c pattern. The Astris AI spinout (December 2024) commercializes internal AI Factory capabilities—a direct example of Mechanism 10 (Productize Internal Operational Advantages). This dual structure (M4 primary, M5c secondary) may be common in regulated industries where internal capability building precedes external productization.
- **lockheed-martin**: [2026-02] The defense sector's unique regulatory environment creates a 'compliance-as-moat' dynamic (Mechanism 8). Taiclet explicitly frames 'trustworthy AI for mission assurance' as a competitive discriminator. This suggests regulated industries may develop different AI structural patterns than tech-native firms—compliance requirements shape the hub's governance role more heavily.
- **lockheed-martin**: [2026-02] The Craig Martell appointment (former DoD CDAO) alongside existing CDAIO Mike Baylor creates an interesting dual-executive structure: CTO for technology innovation, CDAIO for AI strategy/capability, CIO for operational integration. This three-way split is unusual and worth tracking—it may indicate defense-sector-specific complexity in AI governance.
- **lowes**: [2026-02] Lowe's provides a clean exemplar of how M4 Hub-and-Spoke can incorporate an M1-like exploration arm (Innovation Labs) without being classified as M1. The key differentiator is that Innovation Labs is one spoke among several, not the central identity of the AI structure. The presence of the AI Transformation Office as a governance hub, the Charlotte Tech Hub as an execution center, and Nair's platform team as an enablement layer creates a multi-hub architecture that is distinctly M4.
- **lowes**: [2026-02] The Innovation Labs subsidiary structure is unusually clean for retail—physically separated (Kirkland vs. Charlotte), organizationally independent, with 2-5 year exploration horizons on spatial computing and digital twins. This suggests large retailers may need subsidiary-level separation to protect exploration from quarterly retail pressure, similar to what we see in M8 Skunkworks but without the secrecy emphasis.
- **lowes**: [2026-02] Ellison's explicit framing of AI as '50% workload reduction' rather than headcount reduction is notable as a rhetorical choice that may enable faster adoption. The 'AI isn't going to fix a hole in your roof' quote positions AI as complementary to skilled trades rather than threatening—a potentially important contingency for retail/service organizations with large frontline workforces.
- **mayo-clinic**: [2026-02] Mayo represents a rare 'multi-hub' M4 variant where multiple C-suite leaders coordinate distinct AI functions (CAIO for governance, CDAO for enablement, Platform for commercialization). Most M4 specimens have a single central hub with distributed spokes—Mayo has three specialized hubs. This may warrant a sub-type for 'federated hub' architectures in highly regulated industries.
- **mayo-clinic**: [2026-02] The nonprofit mission framing creates interesting structural constraints: Farrugia and Tripathi consistently frame AI in service terms ('serve the people who serve others') rather than efficiency or shareholder value. This purpose orientation may explain why Mayo invests heavily in validation infrastructure (Platform_Validate) and global health applications rather than purely internal cost reduction.
- **mayo-clinic**: [2026-02] The 'AI Factory' concept under CDAO Sehgal deserves closer examination—it appears to be a standardized development capability that sits between research (Department of AI & Informatics) and clinical deployment (embedded teams). This middle layer for rapid prototyping may be a structural innovation worth tracking across other healthcare specimens.
- **mercedes-benz**: [2026-02] Mercedes-Benz presents a multi-hub M4 variant where hubs are functionally specialized rather than just geographically distributed: MBRDNA for vehicle AI/autonomy, Digital Factory Campus for manufacturing AI. This raises the question of whether M4 should distinguish between geographic spokes vs. functional spokes.
- **mercedes-benz**: [2026-02] The tension between CSO (Magnus Östberg, owning MB.OS and product AI) and CDAIO (Daniel Eitler, owning enterprise AI/data) suggests a potential split in AI governance that our taxonomy doesn't explicitly capture. Product AI vs. enterprise AI may require different structural models within the same organization.
- **mercedes-benz**: [2026-02] Källenius's framing of 'every Mercedes will have a supercomputer' as the architectural foundation—with MB.OS routing between competing LLMs (Gemini, ChatGPT)—represents an interesting platform-as-arbiter pattern. The OS becomes the central coordination mechanism, not the AI team. This may be an emerging pattern for hardware-software companies.
- **mount-sinai-health-system**: [2026-02] Mount Sinai represents an unusually clean M4 specimen in healthcare—most health systems lack both the philanthropic funding and academic structure to create a true research hub. The Blackstone-funded James Center provides physical and financial separation that enables structural ambidexterity rarely seen in the sector. This may be a distinctive 'academic health system' variant of M4 where the hub is explicitly academic rather than corporate.
- **mount-sinai-health-system**: [2026-02] The dual CAIO/CDTO structure is notable: Nadkarni owns research and infrastructure, Freeman owns deployment and experience. This separation of 'build the platform' from 'deploy the applications' creates clear swim lanes that may be essential in high-regulatory environments where accountability must be unambiguous.
- **mount-sinai-health-system**: [2026-02] Nadkarni's framing of 'infrastructure that spans the enterprise, not point solutions' and Freeman's '5% technology, 95% people/process' suggest healthcare AI leaders are converging on a shared playbook that prioritizes organizational change over technical sophistication. This may be a sector-specific adaptation to high regulatory intensity.
- **netflix**: [2026-02] Netflix presents an interesting M4 variant where the 'hub' is NOT a traditional central AI lab but rather specialized functional hubs (AIMS for member experience, Eyeline for VFX) that coexist with deeply distributed research. The explicit statement that research is 'NOT centralized' challenges the typical hub-and-spoke framing — this is more like 'multiple small hubs plus pervasive distribution.'
- **netflix**: [2026-02] The 'better not cheaper' framing is distinctive and may warrant tracking as a purpose-claim pattern. Sarandos has articulated this consistently since 2024, positioning AI as quality-enhancing rather than cost-reducing. This is unusual in an industry under margin pressure.
- **netflix**: [2026-02] Netflix's contextual orientation is unusually explicit — the research website literally states that researchers work 'in close collaboration with business teams.' Most orgs claim this but Netflix appears to have built it into the structural DNA, with experimentation culture enabling individuals to balance exploration and execution.
- **nike**: [2026-02] Nike's December 2025 restructuring — eliminating the CTO and moving tech under the COO — represents an interesting organizational choice that challenges the assumption that AI leadership requires standalone C-suite representation. This may signal a broader trend of AI becoming 'infrastructure' (like IT) rather than a strategic function.
- **nike**: [2026-02] The coexistence of a CDAIO (Alan John) with technology reporting to the COO creates an ambiguous reporting structure. This specimen would benefit from clarity on whether the CDAIO is the 'hub' or whether the COO now owns the hub, with CDAIO as one spoke among many.
- **nike**: [2026-02] Nike's M4 classification is complicated by the NSRL, which operates with research lab characteristics (motion capture, biomechanics, long-term product innovation) but isn't positioned as an AI lab per se. It's a performance science lab that uses AI as a tool — a distinction worth tracking as other companies may embed AI in domain-specific research facilities rather than creating AI-branded labs.
- **pepsico**: [2026-02] PepsiCo presents an interesting M4 variant where the CSTO role bundles AI with strategy, M&A, and transformation—rather than a dedicated CAIO. This 'embedded AI leadership' pattern may be more common in consumer goods where AI is a capability within broader transformation rather than a standalone strategic bet. The recent addition of Latin America Foods CEO responsibilities to Kanioura's role (Dec 2025) suggests the organization values leaders who can bridge technology and operations.
- **pepsico**: [2026-02] The contextual orientation here is particularly strong: training 330,000 employees on AI is an unusually ambitious commitment to broad-based capability building. Most M4 specimens maintain clearer separation between hub specialists and spoke generalists. PepsiCo's approach suggests contextual ambidexterity can coexist with hub-and-spoke structure when the hub focuses on enablement rather than monopolizing execution.
- **pepsico**: [2026-02] The 'four or five big bets' prioritization model with AI Council governance represents a distinctive mechanism for managing exploration within a complex, geographically distributed organization. This 'portfolio of bets with central governance' pattern could be a common adaptation for global consumer goods companies that need both strategic coherence and local execution flexibility.
- **progressive**: [2026-02] Progressive exemplifies 'AI as infrastructure' rather than 'AI as strategy' — the absence of organizational theater (no CAIO, no named lab, no conference presence) paired with substantial operational AI deployment challenges our taxonomy's implicit assumption that sophisticated AI requires visible structural commitment. This may be the mature end-state that named labs evolve toward.
- **progressive**: [2026-02] The 20+ year telematics data foundation creates an interesting path dependency: Progressive's AI capability emerged organically from data assets rather than from an AI strategy. This 'data-first, AI-second' trajectory may be common in insurance but is underrepresented in our specimen collection which skews toward tech-forward announcements.
- **progressive**: [2026-02] The buy-over-build approach (H2O.ai for ML platform, Claritas for GenAI) suggests a variant of 6b where the 'central team' is actually external partners managed by distributed business units. This partnership-centric model deserves more taxonomic attention — it may be how many incumbents actually operationalize AI.
- **sutter-health**: [2026-02] Sutter represents an unusually mature M4 implementation for healthcare — a sector where regulatory complexity often pushes orgs toward slower, more centralized M2 structures. The physical Innovation Center hub combined with CAIO-led governance creates clear structural separation between exploration and execution, making this a strong healthcare exemplar of hub-and-spoke ambidexterity.
- **sutter-health**: [2026-02] The CAIO role (Ashley Beecy) is notable: a physician-informaticist with prior industry experience at IBM and Citibank. This hybrid clinical-technical background may be a pattern worth tracking for healthcare AI leadership — the role requires fluency in both clinical safety reasoning and technology deployment.
- **sutter-health**: [2026-02] Sutter's buy-versus-build partnership strategy (Aidoc, Abridge, Hyro, Ferrum) is structurally interesting — it allows faster deployment velocity while concentrating internal resources on governance and integration rather than algorithm development. This may be an emerging M4 variant for regulated industries: 'governance hub + vendor spokes' rather than 'R&D hub + product spokes.'
- **t-mobile**: [2026-02] T-Mobile's M4 classification is distinctive because the 'hub' is explicitly an Innovation Center for network AI (AI-RAN) rather than a typical CoE for governance/standards. This is exploration-focused hub, not enablement-focused—closer to M1 Research Lab in function but organizationally M4 in structure because customer AI is distributed to product teams.
- **t-mobile**: [2026-02] The absence of a CAIO with explicit distribution of AI across CIO, CPO, and President of Innovation is notable. This 'no single throat to choke' model may reflect telecom's infrastructure-heavy nature where AI touches multiple domains (network, customer, operations) that don't naturally report to one function.
- **t-mobile**: [2026-02] T-Mobile's framing of itself as 'transformed from a telecommunications company to a tech company' (Sievert) combined with major partnerships (NVIDIA, OpenAI) suggests a buy-vs-build strategy that may be distinctive for telecom. The reliance on external partners for core AI capabilities contrasts with tech companies building in-house.
- **toyota**: [2026-02] Toyota exemplifies the M4 Hybrid/Hub-and-Spoke model at its most elaborate—not just a central hub plus spokes, but multiple specialized hubs (TRI for research, Enterprise AI for productivity, Woven for automated driving) with explicit bridging mechanisms (GAIA). This raises questions about whether very large enterprises naturally evolve toward multi-hub architectures rather than simple hub-spoke patterns.
- **toyota**: [2026-02] Incoming CEO Kon's candid admission that Toyota trails Tesla in AI is structurally revealing—despite $1B+ investment in TRI since 2016, Toyota's structural separation may have created exploration excellence without sufficient execution velocity. The 'we can learn from them' framing suggests the M4 structure may need recalibration toward faster deployment.
- **toyota**: [2026-02] Brian Kursar's dual role—Head of Enterprise AI and TRI technical advisor for GAIA—is an interesting personnel-based integration mechanism. Rather than relying purely on structural processes, Toyota uses key individuals to bridge the exploration-execution divide. This 'boundary spanner' pattern may be underappreciated in the taxonomy.
- **uber**: [2026-02] Uber's explicit 'Core and Connections' naming for AI Labs programs is a rare case of self-aware hub-and-spoke design—most M4 specimens evolve into this structure accidentally. The nomenclature suggests deliberate organizational design thinking.
- **uber**: [2026-02] The ATG divestiture (2020) and shift to AV partnerships represents an interesting structural evolution: from M8 Skunkworks to what might be called 'externalized exploration'—keeping platform coordination internally while outsourcing the hardest R&D to partners. This pattern may warrant a new subtype for M4.
- **uber**: [2026-02] Uber AI Solutions productizing internal data labeling capabilities (M10 mechanism) is structurally similar to Walmart GoLocal and Amazon AWS—platform companies monetizing operational capabilities. But unlike those cases where the product targets external logistics/compute buyers, Uber is selling to other AI labs, creating an unusual B2B-AI-services revenue stream.
- **ulta-beauty**: [2026-02] Ulta Beauty presents a clean M4 case with an interesting dual-head structure: CTTO owns the AI Center of Excellence (capability development) while CDO owns digital innovation (consumer-facing applications). This creates potential coordination challenges but also allows specialized focus—a variant worth tracking as more retailers split AI leadership this way.
- **ulta-beauty**: [2026-02] The 'way of being' framing from CEO Steelman is notable for a contextual orientation—it explicitly frames AI not as a separate initiative but as embedded in organizational culture. This rhetoric aligns with contextual ambidexterity theory (Gibson & Birkinshaw) where the organization develops behavioral capacity for both exploration and exploitation rather than structural separation.
- **ulta-beauty**: [2026-02] The agentic AI decision point (unified assistant vs. specialized agents) represents a live structural choice that could shift the model. If they choose specialized agents deployed to different functions, it reinforces M4; if they choose a unified assistant, it could push toward M2 with stronger central control. Worth tracking in future layers.
- **unitedhealth-group**: [2026-02] UnitedHealth exemplifies how hub-and-spoke (M4) can scale to massive production deployment (1,000+ use cases) when governance infrastructure is treated as deployment enablement rather than constraint. The Responsible AI Board with external experts is not just compliance theater—it's the mechanism that allows them to move fast across business units because approval pathways are clear.
- **unitedhealth-group**: [2026-02] The three-way split of AI leadership (Chief AI Scientist for governance, Chief AI Transformation Officer for strategy, CDTO for execution) is an interesting structural pattern worth tracking. It suggests that at sufficient scale, the AI leadership function itself may require structural separation—exploration of governance standards vs. transformation strategy vs. operational execution.
- **unitedhealth-group**: [2026-02] Notable absence from external AI conference circuit despite massive deployment. UnitedHealth prefers controlled investor/healthcare venues. This may reflect regulatory sensitivity (DOJ scrutiny) or deliberate strategy to avoid attention while scaling. Contrast with tech companies that aggressively publicize AI capabilities.
- **visa**: [2026-02] Visa's M4 classification raises an interesting question about what makes a 'hub' sufficiently central. Visa Research is clearly a dedicated research unit, but without a CAIO, standards-setting authority is ambiguous. The hub may be more 'research outputs' than 'governance mandates'—a softer form of hub-and-spoke than JPMorgan or other financial services M4s with stronger central control.
- **visa**: [2026-02] The 'data as moat' framing is distinctive. McInerney's emphasis on Visa's payments dataset as the foundation for generative AI suggests the company's AI advantage is less about organizational structure and more about proprietary data assets. This raises questions about whether data-rich incumbents can succeed with less sophisticated AI org structures than pure-play AI companies.
- **visa**: [2026-02] Absence of a CAIO in a Fortune AIQ 50 #2 company is notable. Visa distributes AI leadership across Research (Wang Min), Platforms (Sam Hamilton), and Technology (Taneja) rather than unifying under a single AI executive. This may reflect AI's deep integration into payments infrastructure—it's not a separate 'AI strategy' but embedded in core operations.

    ## Skipped Files

    | File                                               | Reason                     |
    |----------------------------------------------------|----------------------------|
    | earnings-discovery-q4-2025.json                    | Multi-company session file |
| earnings-q4-2025-amazon-google.json                | Multi-company session file |
| financial-services-earnings-q4-2025.json           | Multi-company session file |
| general-sweep-feb-2026-v2.json                     | Multi-company session file |
| general-sweep-feb-2026.json                        | Multi-company session file |
| goldman-sachs-deep-scan.json                       | Multi-company session file |
| morgan-stanley-deep-scan.json                      | Multi-company session file |
| pharma-earnings-q4-2025.json                       | Multi-company session file |
| podcast-deep-scan-feb-2026.json                    | Multi-company session file |
| podcast-substack-feed-check.json                   | Multi-company session file |

    ## Failed Specimens

    | Specimen                       | Error                                              |
    |--------------------------------|----------------------------------------------------|
    | (none) | |

    ## Next Steps

    - Run `/synthesize` to process 32 newly queued specimens
    - Run `overnight-purpose-claims.py` for 32 newly created specimens
    - Review failed specimens in `research/curate-retry-queue.json`
    - Process 10 multi-company session files via interactive `/curate`
