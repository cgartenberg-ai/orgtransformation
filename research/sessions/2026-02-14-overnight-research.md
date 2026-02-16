    # Overnight Research Run — 2026-02-14

    **Started:** 2026-02-14 16:20
    **Duration:** 254 minutes
    **Targets scanned:** 22
    **Succeeded:** 19
    **Failed:** 3
    **Method:** `scripts/overnight-research.py` via `claude -p --model opus`

    ## Results

    | Company | Q | Status | Model | Quotes | Time |
    |---------|---|--------|-------|--------|------|
    | Palantir                       | Q1 | ✓ | M9 | 9 quotes | 274s |
| AMD                            | Q2 | ✗ | M? | 0 quotes | 1500s |
| ASML                           | Q2 | ✓ | M6 | 7 quotes | 249s |
| Caterpillar                    | Q4 | ✗ | M? | 0 quotes | 1500s |
| AstraZeneca                    | Q2 | ✓ | M4 | 5 quotes | 237s |
| Rivian                         | Q2 | ✓ | M4 | 12 quotes | 273s |
| Comcast / NBCUniversal         | Q3 | ✓ | M5 | 3 quotes | 1118s |
| Spotify                        | Q3 | ✓ | M4 | 10 quotes | 291s |
| Stripe                         | Q3 | ✓ | M4 | 10 quotes | 263s |
| NextEra Energy                 | Q4 | ✓ | M6 | 3 quotes | 242s |
| NVIDIA                         | Q1 | ✓ | Menrich | 8 quotes | 329s |
| Novo Nordisk                   | Q2 | ✓ | Menrich | 3 quotes | 396s |
| Siemens                        | Q4 | ✓ | Menrich | 7 quotes | 240s |
| Walmart                        | Q4 | ✓ | Menrich | 11 quotes | 303s |
| Atlassian                      | Q1 | ✓ | Menrich | 10 quotes | 251s |
| ByteDance                      | Q1 | ✓ | Menrich | 4 quotes | 265s |
| Duolingo                       | Q1 | ✓ | Menrich | 11 quotes | 257s |
| Shopify                        | Q1 | ✓ | Menrich | 10 quotes | 250s |
| Deloitte                       | Q3 | ✓ | Menrich | 4 quotes | 256s |
| Infosys                        | Q3 | ✓ | Menrich | 5 quotes | 256s |
| ABB                            | Q4 | ✗ | M? | 0 quotes | 1500s |
| Coca-Cola                      | Q4 | ✓ | Menrich | 7 quotes | 252s |

    ## Model Distribution

    | Model | Count |
    |-------|-------|
    | M4 Hybrid/Hub-and-Spoke           |     4 |
| M5 Product/Venture Lab            |     1 |
| M6 Unnamed/Informal               |     2 |
| M9 AI-Native                      |     1 |
| Menrich Unknown                        |    11 |

    ## Quadrant Distribution

    | Quadrant | Count |
    |----------|-------|
    | Q1 | 6 |
| Q2 | 4 |
| Q3 | 5 |
| Q4 | 4 |

    ## Per-Company Findings

    ### Palantir — M9 AI-Native | Contextual | High

**Summary:** Palantir is a textbook example of an AI-native organization (M9) — founded in 2003 specifically to build AI/data infrastructure, it has no separate 'AI team' because the entire company is the AI team. CEO Karp describes it as an 'engineering commune' with a deliberately informal structure, no formal org chart, and 97% of employees using the Foundry platform daily. The company's contextual ambidexterity emerges from every employee balancing exploration and execution within their roles, enabled by a unified platform infrastructure.

**Classification rationale:** Palantir is fundamentally an AI-native organization — it was founded in 2003 specifically to build data and AI infrastructure, not to 'transform' from a legacy state. There is no separate 'AI team' because the entire company IS the AI team. Unlike traditional enterprises that create AI centers of excellence or labs, Palantir's core products (Gotham, Foundry, Apollo, AIP) are all AI/ML platforms. The 'engineering commune' culture Karp describes, where '97% of employees use Foundry daily,' reflects contextual ambidexterity: everyone balances exploration and execution within their roles. There is no structural separation because AI is not a function — it is the business.

**AI team structure:** Palantir does NOT have a dedicated 'AI team' in the traditional sense. According to The Information's org chart coverage, the company 'doesn't have a formal org chart, although CEO Alex Karp works closely with dozens of executives.' The entire organization is oriented around building and deploying AI platforms. Matt Welsh holds the title 'Head of AI Systems' but this appears to be a technical leadership role within an AI-native company, not a separate AI unit. The organizational structure is not...

**Key people:** Alexander C. Karp (CEO & Co-Founder), Shyam Sankar (President & COO), Matt Welsh (Head of AI Systems), David Glazer (CFO & Treasurer), Ryan Taylor (Chief Revenue Officer & Chief Legal Officer)

**Data:** 9 quotes, 8 sources

**Most revealing quote:** "Large language models alone will not lead us to salvation."
— Alexander C. Karp
*Why interesting:* This quote captures Palantir's entire strategic positioning: they're not competing on model capability, but on the 'orchestration layer' between raw AI and enterprise reality. It's a direct challenge to the OpenAI/Anthropic thesis that foundation models are the moat. For organizational structure research, it explains why they don't have a separate 'AI research lab' — they're not trying to build better models, they're building the software that makes models useful.

**Botanist's notes:**
- STRUCTURALLY FASCINATING: Palantir represents the rare case of M9 (AI-Native) in enterprise software — most M9 examples are consumer/social companies. They were building AI infrastructure before 'AI transformation' was a concept, making them uniquely positioned to study what an 'AI-first' organization looks like at scale.
- NO ORG CHART AS A STRATEGY: The explicit lack of formal org chart is not sloppiness — it appears to be deliberate design. Karp's 'engineering commune' framing suggests that structural ambiguity is part of how they maintain contextual ambidexterity. Everyone owns AI because no one owns AI.
- CUSTOMER BOOTCAMPS AS EXTENSION MODEL: The HD Hyundai 'Center of Excellence' partnership reveals how Palantir extends its contextual model to customers — they don't build separate AI teams for clients, they embed Palantir culture/tools into client organizations. This is M4 (Hub-and-Spoke) for THEIR CUSTOMERS, not for themselves.
- KARP'S ANTI-GENERALIST THESIS: His provocative 'Yale grad is effed' comment reveals a theory of AI that privileges domain expertise over general intelligence — which maps directly to his product strategy (ontologies, Forward Deployed Engineers, customer-specific deployments).

**Open questions:**
- What is Matt Welsh's (Head of AI Systems) specific scope vs. Shyam Sankar's product oversight?
- How does the 'engineering commune' actually make decisions on major AI investments?
- What is the internal structure of the AIP product team vs. Foundry vs. Gotham teams?
- How autonomous are Forward Deployed Engineers in making AI decisions at customer sites?


### ASML — M6 Unnamed/Informal | Contextual | Medium

**Summary:** ASML is the world's only EUV lithography supplier — its machines are essential for manufacturing advanced AI chips. However, ASML's internal AI organization is minimal and unnamed. AI is used operationally (predictive ML for manufacturing, parameter optimization) rather than as a strategic transformation initiative. The company has a Head of AI Program and Strategy but no formal AI Lab or CAIO. ASML frames AI primarily as a demand driver (their customers need AI chips) rather than an internal capability to showcase.

**Classification rationale:** ASML has AI/ML capabilities embedded in operations without a formal 'AI Lab' or 'Center of Excellence' branding. There is a Head of AI Program and Strategy (Yu Cao) and at least one Technical Program Manager AI/ML (Arnaud Hubaux), but no formal AI organization announced publicly. AI is treated as an operational tool (optimizing lithography systems, predictive ML for manufacturing) rather than a strategic transformation initiative. The company's public communications frame AI primarily as DEMAND driver (their customers need AI chips) rather than internal capability. This fits 6b: centralized capability without lab branding.

**AI team structure:** Limited visibility. Key known roles: Yu Cao (Head of AI Program and Strategy, Santa Clara), Arnaud Hubaux (Technical Program Manager AI/ML). No formal AI Lab or branded AI organization announced. AI/ML teams appear to be embedded within engineering/R&D functions rather than separated.

**Key people:** Christophe Fouquet (President and CEO), Yu Cao (Head of AI Program and Strategy), Arnaud Hubaux (Technical Program Manager AI/ML)

**Data:** 7 quotes, 6 sources

**Most revealing quote:** "AI is a game-changer for us. It helps optimize our lithography systems, which involve managing 100,000 parameters for each wafer exposure."
— Christophe Fouquet
*Why interesting:* This quote reveals ASML's AI philosophy: AI is a tool for optimization, not a strategic transformation. 'Game-changer' language but applied to operational efficiency, not new business models or org structure. The 100,000 parameters detail shows AI as execution-enabler in existing workflows.

**Botanist's notes:**
- ASML presents a fascinating control case: the world's most critical AI supply chain company has no formal AI organization. They are AI-enabling (their machines make AI chips) without being AI-transforming (their own operations use AI tactically, not strategically).
- The structural asymmetry is striking: ASML is mentioned by every AI company as essential infrastructure, but ASML itself never positions AI as a transformation initiative. This may be because their competitive moat is physics/optics, not software/AI.
- The Fouquet quote about '100,000 parameters per wafer exposure' reveals that AI is used for operational optimization (classic execution-side), not exploration or new business models. This is textbook Contextual ambidexterity — same engineers doing both core lithography work and AI optimization.
- Worth noting: ASML announced restructuring to 'strengthen focus on engineering and innovation' in Jan 2026 but explicitly did NOT frame this as AI-related. This supports our hypothesis that ASML is a counter-example — restructuring happens for non-AI reasons.

**Open questions:**
- Does Yu Cao (Head of AI Program and Strategy) report to the CTO or CEO?
- What is the headcount of ASML's AI/ML teams?
- Is there a formal AI strategy document or internal AI organization beyond embedded functions?
- How does the Mistral AI partnership translate into organizational structure or team additions?
- What fraction of the 14,000+ R&D employees work on AI/ML specifically?


### AstraZeneca — M4 Hybrid/Hub-and-Spoke | Structural | High

**Summary:** AstraZeneca operates a federated hub-and-spoke model for AI: a central enterprise data office under CDO Brian Dummann sets standards and governance, while business units retain full autonomy to decide which AI projects to pursue. The 'AI Accelerator' cross-functional initiative speeds implementation by unifying legal, compliance, and tech reviews. AI is deeply embedded in R&D (2x faster drug discovery, antibody leads in 3 days vs 3 months) with $13B annual R&D and $2.5B committed to a new Beijing AI lab.

**Classification rationale:** AstraZeneca operates a federated model with a central enterprise data office (led by CDO Brian Dummann) that sets standards, tools, and policies, while distributed data offices in business units retain autonomy to pursue their own AI projects. The AI Accelerator serves as a cross-functional enablement layer. They explicitly state 'there is no central group that determines what projects we will or won't do' — business leaders decide within guardrails. This is classic hub-and-spoke: central standards + distributed execution.

**AI team structure:** Federated model: Central enterprise data office defines standards and governance; business units maintain their own data offices aligned to central standards. The CDO leads a team focused on 'accelerating the impact of technology, data, and AI across AstraZeneca's value chain.' No CAIO — AI governance is deliberately integrated within data governance rather than standalone. Key structural element is the 'AI Accelerator,' a cross-functional initiative bringing together technology, legal, complian...

**Key people:** Pascal Soriot (CEO), Brian Dummann (Vice President of Insights & Technology and Chief Data Officer)

**Data:** 5 quotes, 6 sources

**Most revealing quote:** "There is no central group that determines what projects we will or won't do."
— Brian Dummann
*Why interesting:* This single quote captures AstraZeneca's unusual structural philosophy: extreme decentralization of AI decision rights within strong central guardrails. In pharma — where R&D coordination is typically centralized — this is a provocative stance that reveals a bet on distributed innovation over central optimization.

**Botanist's notes:**
- AstraZeneca's explicit rejection of a CAIO role is structurally interesting — they deliberately integrated AI governance within data governance, arguing the capabilities and processes are the same. This challenges the emerging norm of standalone AI leadership.
- The federated model with 'no central group that determines what projects we will or won't do' is unusual for pharma, which typically requires tight R&D coordination. They've solved this by separating standards (central) from project selection (distributed).
- The 'AI Accelerator' as a cross-functional initiative (tech + legal + compliance + governance) rather than a team is a different structural choice than the typical Center of Excellence — it's a coordination mechanism, not an org unit.
- The CDO role here is much broader than typical data roles — Dummann owns AI strategy, governance, and implementation across the entire value chain. This is closer to a CDAIO than a traditional CDO.

**Open questions:**
- Size of dedicated AI/data science headcount across the federated structure
- How the Modella AI acquisition (Q4 2025) changes oncology R&D AI structure
- Whether the Beijing AI lab represents a shift toward more centralized research AI
- Specific governance mechanisms for high-risk AI applications mentioned but not detailed


### Rivian — M4 Hybrid/Hub-and-Spoke | Structural | High

**Summary:** Rivian has rapidly elevated AI and autonomy to strategic priorities, building a hub-and-spoke structure with centralized control in Palo Alto and distributed execution across London, Atlanta, and Belgrade. The company's vertical integration strategy—custom 5nm silicon (RAP1), in-house Large Driving Model, and Rivian Unified Intelligence platform—positions it as a software-defined vehicle company competing with Tesla on autonomy. Board-level AI expertise (Aidan Gomez from Cohere) and the $5.8B Volkswagen software joint venture signal substantial commitment.

**Classification rationale:** Rivian exhibits a classic hub-and-spoke structure with a central AI/Autonomy team in Palo Alto serving as the hub, with distributed spokes in London (AI engineering), Atlanta (autonomy), Belgrade (software/enterprise), and the Volkswagen joint venture. The VP of Autonomy & AI reports centrally while distributed teams execute specialized work. The vertical integration strategy—custom silicon (RAP1), in-house Large Driving Model, and Rivian Unified Intelligence platform—is coordinated centrally but deployed across product lines. This is not a research lab (M1) because the focus is 1-3 year product horizons, not fundamental research. It's not AI-Native (M9) because Rivian was founded in 2009 as an EV company and only recently elevated AI to a strategic priority.

**AI team structure:** Rivian has a centralized AI/Autonomy function led by James Philbin (VP Autonomy & AI) based in Palo Alto, with the Chief Software Officer (Wassym Bensaid) overseeing broader software architecture including the AI assistant work that 'sits outside the joint venture with VW.' The company is building a multi-hub structure: Palo Alto (autonomy, VW JV), London (AI engineering talent hub), Atlanta East Coast HQ (autonomy teams, 100-500 employees planned), and Belgrade (vehicle software, enterprise tec...

**Key people:** RJ Scaringe (CEO & Founder), James Philbin (VP Autonomy & AI), Wassym Bensaid (Chief Software Officer), Vidya Rajagopalan (SVP Electrical Hardware), Aidan Gomez (Board Member)

**Data:** 12 quotes, 6 sources

**Most revealing quote:** "By 2030 it will be inconceivable to buy a car and not expect it to drive itself."
— RJ Scaringe
*Why interesting:* This quote reveals how Scaringe frames autonomy as inevitable, not optional—a 'when' not 'if' that justifies the structural investments Rivian is making (custom silicon, multi-hub AI teams, LDM development). It's a CEO staking reputation on a technology timeline, which creates accountability and signals commitment to the organization.

**Botanist's notes:**
- MOST INTERESTING: Rivian's decision to build custom silicon (RAP1) rather than using NVIDIA represents a structural bet that echoes Tesla's approach. Rajagopalan's rationale—'velocity, performance and cost'—reveals an economic logic: vertical integration reduces dependency on external suppliers and enables faster iteration. This is a M4 hub-and-spoke with M5 Product Lab characteristics (building commercializable tech assets).
- PATTERN CONFIRMATION: The Bensaid quote about AI assistant work 'sitting outside the joint venture with VW' reveals the classic coordination challenge in hub-and-spoke models—how do you partition work between the central team and partners? This structural tension between JV governance and internal AI development is worth watching.
- CONTRAST WITH TESLA: While both companies pursue vertical integration, Rivian's approach explicitly embraces LLM-style training ('Large Driving Model') and adds LiDAR (late 2026 R2). The Aidan Gomez board appointment signals Rivian views foundation model expertise as strategic—Tesla has not made equivalent board-level AI hires.
- SCARINGE AS AI VOICE: Unlike many automotive CEOs who delegate AI messaging, Scaringe personally articulates the technical strategy (transformer-based encoding, data flywheel, neural net vs rules-based). His '2030 inconceivable' prediction positions him as a tech-forward leader, not a traditional auto executive. This CEO ownership of AI narrative is a structural choice that shapes resource allocation.

**Open questions:**
- What is the exact headcount of Rivian's AI/autonomy teams across all locations?
- What percentage of R&D spend is allocated to autonomy vs. other functions?
- How does decision-making authority flow between the VW joint venture and Rivian's internal AI assistant work?
- What is the timeline for achieving L4 autonomy that Scaringe references?
- How does the London hub coordinate with Palo Alto—is it autonomous execution or tight integration?


### Comcast / NBCUniversal — M5 Product/Venture Lab | Structural | Medium

**Summary:** Comcast NBCUniversal structures AI work primarily through LIFT Labs, an accelerator that functions as a venture scouting mechanism — vetting 1,000+ AI startups annually and converting 90% into pilots or deals since 2018. Successful partnerships (like Waymark's AI video platform) get absorbed into operational units. No Chief AI Officer exists; AI is embedded within Connectivity & Platforms for network automation and within NBCUniversal for content applications. Brian Roberts frames AI as 'creating more bits to consume' — positioning Comcast as infrastructure for AI-generated content consumption rather than an AI creator.

**Classification rationale:** Comcast NBCUniversal structures AI work primarily through LIFT Labs, an accelerator that functions as a venture-style incubation mechanism. Since 2018, 90% of participating startups have secured pilots, POCs, or deals — and successful partnerships get absorbed into Comcast's operations (e.g., Waymark's AI video platform now powers Comcast Advertising). This is classic 5a: external exploration that feeds internal product integration. However, the lack of a visible Chief AI Officer or dedicated internal AI research lab makes this classification medium confidence. The operational AI deployments (network automation, VideoAI) suggest some embedded AI capability exists, but the dominant structural mechanism is the accelerator-to-integration pipeline.

**AI team structure:** No dedicated AI lab or Chief AI Officer. AI work is distributed across: (1) LIFT Labs accelerator that vets 1,000+ AI startups annually, (2) embedded AI within Connectivity & Platforms under Steve Crone, (3) NBCUniversal Media Labs for content/media innovation. The accelerator functions as the primary scouting and exploration mechanism, with successful startups getting integrated into business units for execution.

**Key people:** Brian Roberts (Chairman & CEO, Comcast Corporation), Michael Cavanagh (President, Comcast Corporation), Steve Crone (CEO, Connectivity and Platforms), Dave Watson (Vice Chairman, Comcast Corporation), Laura Plunkett (Executive Director, LIFT Labs Startup Engagement)

**Data:** 3 quotes, 5 sources

**Most revealing quote:** "And so what will AI do? Well, one thing it's going to do is create a lot more bits of things that we're going to consume, we're going to choose and se..."
— Brian Roberts
*Why interesting:* This quote perfectly captures Comcast's infrastructure-centric AI worldview. Roberts isn't talking about building AI — he's talking about being the delivery mechanism for AI-generated content. It's a telecom CEO's mental model: let others create, we'll be the pipe. Analytically interesting because it explains why they might not need a Chief AI Officer — if you're not building AI, you don't need an AI leader.

**Botanist's notes:**
- The 'Symphony' philosophy is analytically interesting: Comcast explicitly believes divisions are 'more powerful together' — but this coordination doctrine doesn't extend to a unified AI structure. AI remains siloed by business function (network ops vs. content vs. advertising), with LIFT Labs as the only cross-cutting mechanism.
- Roberts' 'more bits to consume' framing is revealing: he positions Comcast as the pipe for AI-generated content, not the AI generator. This is infrastructure-centric thinking — let others create AI content, we'll deliver it. Classic telecom mental model.
- The LIFT Labs → internal absorption pattern (5a) is working: Waymark went from accelerator to powering Comcast Advertising's AI video platform. But this is opportunistic integration, not strategic AI architecture.
- Conspicuous absence: no CAIO, no 'AI-first' rhetoric, no published AI principles. For a company spanning broadband + content + theme parks + advertising, the lack of visible AI coordination is notable. Either AI is deeply embedded and invisible, or it's genuinely fragmented.

**Open questions:**
- Who leads AI strategy at the corporate level? No CAIO visible, unclear if someone owns cross-company AI coordination.
- What happened to Media Labs? The NBCUniversal Technology Center launched in 2012 but current status is unclear.
- How does Peacock's recommendation AI connect to broader AI strategy? 44M paid subscribers but AI team structure not visible.
- Is there internal AI research beyond operational applications, or is LIFT Labs the primary exploration mechanism?
- What is the VideoAI team structure that won the Technology Emmy? No leadership or organizational details found.


### Spotify — M4 Hybrid/Hub-and-Spoke | Contextual | High

**Summary:** Spotify employs a hybrid/hub-and-spoke AI model adapted to their famous squad/tribe organizational structure. A central ML Platform and Research team provides recommendation algorithms and infrastructure, while product squads embed ML engineers to build features like AI DJ (90M users, 4B engagement hours). In October 2025, they announced a new Generative AI Research Lab in partnership with major labels, signaling increased investment in artist-first AI music tools. The recent CEO transition (Ek to chairman, Söderström and Norström as Co-CEOs) positions the product/technology leader to drive AI strategy.

**Classification rationale:** Spotify exhibits a classic hub-and-spoke model adapted to their squad/tribe structure. They have a central ML Platform/Research team that provides recommendation algorithms and infrastructure as a service, while product squads (personalization, ads, content) embed data scientists and ML engineers who leverage these platform services. The newly announced Generative AI Research Lab (Oct 2025) adds a formal research hub. This platform-plus-embedded approach ensures both innovation (central R&D on cutting-edge algorithms) and rapid product integration (squads quickly applying AI to user-facing features). The contextual orientation is evident in their 'Honk' system where individual engineers balance AI exploration with daily execution.

**AI team structure:** Three-layer structure: (1) Spotify Research - central AI/ML research team focused on advancing state of the art in generative AI, LLMs, reinforcement learning, and causal learning; (2) Creator Technology Research Lab - focused on AI tools for artists, formerly led by François Pachet; (3) Newly announced Generative AI Research Lab (Oct 2025) - partnership with major labels for artist-first AI music products. Product squads embed data scientists and ML engineers who leverage platform services. The...

**Key people:** Daniel Ek (Executive Chairman (former CEO)), Gustav Söderström (Co-CEO, Co-President and Chief Product and Technology Officer), Alex Norström (Co-CEO, Co-President and Chief Business Officer), François Pachet (Director, Creator Technology Research Lab)

**Data:** 10 quotes, 6 sources

**Most revealing quote:** "Taste is not a fact. It is an opinion."
— Gustav Söderström
*Why interesting:* This six-word statement captures Spotify's entire AI thesis. Unlike search (where there are canonical right answers), music recommendation requires understanding subjective, contextual, personal taste at massive scale. This is their moat: they have the global dataset of 'language-to-music' interactions that no LLM trained on canonical facts can replicate. It's both a strategic insight and an implicit challenge to AI companies who think recommendation can be solved with general-purpose models.

**Botanist's notes:**
- The Honk system is striking: top Spotify developers reportedly 'have not written a single line of code since December' and only 'generate code and supervise it.' This is one of the most aggressive internal AI adoption claims I've seen - and it comes from an earnings call, making it an on-the-record statement to investors. Suggests contextual ambidexterity where individual engineers balance exploration (AI coding) with execution (shipping features).
- The squad/tribe model may be uniquely suited to AI integration. Unlike hierarchical orgs that need formal AI teams, Spotify's autonomous squads can independently adopt AI tools. The 'platform-plus-embedded' approach (central ML platform serving product squads) mirrors the hub-and-spoke pattern but with unusually high squad autonomy.
- Ek's transition to chairman while Söderström (product/tech) becomes Co-CEO is significant timing. The earnings call framed it as freeing Ek for European tech investing (including his Helsing AI defense investment), but it also positions the technologist to drive AI transformation rather than the founder.
- The claim 'we consider ourselves the R&D department for the music industry' is a fascinating framing - it positions Spotify not as a music company using AI, but as an AI/tech company serving music. This echoes Söderström's insight that 'significant disruption happens when new technologies enable new asymmetric business models' - they're building the platform that captures AI value in music.

**Open questions:**
- What is the headcount and budget for the various AI/ML research teams?
- How does the new Generative AI Research Lab relate to existing research infrastructure?
- What is the reporting structure for François Pachet's Creator Technology Research Lab?
- How widely is the 'Honk' AI coding system deployed across engineering?
- What percentage of Spotify's R&D is allocated to AI vs. other areas?


### Stripe — M4 Hybrid/Hub-and-Spoke | Contextual | Medium

**Summary:** Stripe operates a contextually ambidextrous hybrid model where AI capability is deeply embedded throughout the organization rather than centralized in a lab. A Chief Revenue Officer of AI (Maia Josebachvili) coordinates go-to-market, while AI development emerges from domain teams — the 'minions' automated development system originated in financial operations, not a central AI unit. Nearly all employees use internal AI tools weekly, and Patrick Collison frames AI as 'acceleration not replacement,' expecting to hire more in 2026 because of AI.

**Classification rationale:** Stripe exhibits characteristics of a hybrid model with contextual ambidexterity. They have created a specialized 'Chief Revenue Officer of AI' role (Maia Josebachvili) for go-to-market, but AI development appears deeply embedded across the organization. The 'minions' automated development initiative came from the financial operations team, not a central AI lab. Patrick Collison emphasizes 'systemic AI integration' rather than isolated AI units. Nearly all employees use their internal LLM tool weekly, and Cursor adoption is widespread. This suggests AI capability is distributed throughout the organization while certain coordination functions (like AI go-to-market) are centralized.

**AI team structure:** No formal AI lab or center of excellence identified. Instead, Stripe uses a distributed model: (1) Chief Revenue Officer of AI (Maia Josebachvili) leads go-to-market for AI products; (2) Head of Information (Emily Glassberg Sands) oversees foundation model work; (3) AI development emerges from domain teams (e.g., 'minions' originated in financial ops team); (4) Company-wide AI tooling: internal LLM tool used weekly by nearly all employees, widespread Cursor adoption. The Payments Foundation Mode...

**Key people:** Patrick Collison (CEO), John Collison (President), Maia Josebachvili (Chief Revenue Officer of AI), Emily Glassberg Sands (Head of Information)

**Data:** 10 quotes, 6 sources

**Most revealing quote:** "This is not just using LLMs in Cursor. This is a human never logged into the dev box."
— Patrick Collison
*Why interesting:* This quote captures Stripe's ambitious internal AI deployment — fully autonomous development agents ('minions') that write and submit code without human involvement in the coding process. It's a concrete operational marker, not aspirational vision. Most companies talk about 'AI-assisted development'; Stripe is describing AI-autonomous development at meaningful scale (5% of all PRs).

**Botanist's notes:**
- The 'minions' story is striking: 5% of all PRs at Stripe are now generated end-to-end by automated AI agents, with humans only reviewing before merge. This is among the most concrete internal AI adoption metrics I've encountered — most companies speak abstractly about 'productivity gains.'
- The CRO of AI title is unusual — it signals that Stripe sees AI primarily as a revenue/commercial opportunity to be 'sold' rather than a technical capability to be 'built.' Most companies create CAIOs or AI Labs; Stripe created a go-to-market role.
- Patrick's philosophical reframe — 'What would we elect to do much more of?' — inverts the typical AI-and-jobs narrative. Instead of defending against replacement, he's asking what expansion AI enables. This is culturally significant.
- John's rejection of ROI justification for AI ('If you ask people to justify ROI, they'll magically produce numbers meeting any threshold') is provocatively anti-bureaucratic. It suggests Stripe treats AI investment as strategic conviction, not analytical calculation.

**Open questions:**
- How exactly are Stripe's 'four AI focus areas' structured organizationally?
- What is the size and composition of the Payments Foundation Model team?
- How does Emily Glassberg Sands' 'Head of Information' role relate to AI leadership?
- What is the formal reporting structure for AI initiatives — do they roll up through product, engineering, or a separate AI function?
- How does the CRO of AI role coordinate with product/engineering on AI development vs. go-to-market?


### NextEra Energy — M6 Unnamed/Informal | Contextual | Medium

**Summary:** NextEra Energy approaches AI without a dedicated AI organization, Chief AI Officer, or formal AI lab. Instead, the company pursues AI through strategic partnerships (Google Cloud being primary) and embeds AI capabilities into existing operations (predictive maintenance, drone inspections). CEO John Ketchum frames NextEra primarily as an AI *enabler* — providing the clean energy infrastructure that powers AI data centers — rather than an AI developer. This is a contextual/partnership-driven approach where external capability (Google) is combined with internal domain expertise (grid operations) rather than building proprietary AI capabilities in-house.

**Classification rationale:** NextEra has no Chief AI Officer, no dedicated AI lab, and no formal AI organization in their executive structure. Instead, they appear to be pursuing AI through partnership-based approach (Google Cloud being the primary partner) and integrating AI into existing operations (drones for power restoration, predictive maintenance, advanced analytics). Their 35 Mules innovation hub exists but isn't AI-specific. The Google Cloud partnership will create an AI grid-management tool expected mid-2026 — suggesting external partnership is the primary mechanism for AI capability development rather than internal build. This is a contextual orientation where AI is being adopted across existing roles and operations without a separate exploration unit.

**AI team structure:** No dedicated AI team or Chief AI Officer identified. AI work appears embedded within existing operational divisions and primarily executed through external partnerships (Google Cloud). The company has a general innovation program (35 Mules startup hub, annual Innovation Summit, Hack Week) but these are not AI-specific. A Central Lab exists in West Palm Beach with 16 scientists, but this is focused on chemistry and energy testing, not AI research.

**Key people:** John W. Ketchum (Chairman, President and CEO), Armando Pimentel (CEO, Florida Power & Light Company), Brian Bolster (President and CEO, NextEra Energy Resources), Michael Dunne (EVP, Finance and CFO), Mark E. Hickson (EVP, Corporate Development and Strategy)

**Data:** 3 quotes, 6 sources

**Most revealing quote:** "The need for power is going to be more significant than anything we've seen since the post–World War II industrial revolution."
— John Ketchum
*Why interesting:* This quote reveals NextEra's strategic framing: they see themselves as infrastructure builders for a historic transformation, not AI developers. The post-WWII comparison is deliberately chosen to signal massive, long-term capital deployment. It's a claim about structural position in the economy — 'we are the foundation layer' — rather than a claim about AI capability.

**Botanist's notes:**
- DUAL IDENTITY STRATEGY: NextEra is playing both sides of the AI-energy equation. They're simultaneously (1) an AI *enabler* providing clean power for data centers and (2) an AI *adopter* using AI for grid operations. The enabler role dominates their narrative — Ketchum's 'post-WWII industrial revolution' framing positions them as infrastructure builders for the AI era, not AI builders themselves.
- PARTNERSHIP AS STRUCTURAL CHOICE: The Google Cloud partnership is structurally significant. Rather than building internal AI capabilities (M1 lab, M2 CoE), NextEra outsources AI development to a tech partner while contributing domain expertise. This is a deliberate structural choice — they don't have a CAIO, and likely won't need one if Google provides the AI layer.
- INCUMBENT ADVANTAGE: Unlike tech companies scrambling to understand energy, NextEra already owns the critical resource AI companies desperately need — electrons. The absence of formal AI structure may reflect confidence that they can acquire AI capabilities through partnerships because tech companies need them more than they need to impress anyone with AI credentials.
- TECHNOLOGY COMPANY REFRAMING: Ketchum calling NextEra 'a technology company that delivers electricity' is strategic positioning. It signals to investors that they're not a stodgy utility but a technology play. Yet the executive roster shows zero technology officers — traditional energy roles only. The rhetoric outpaces the org chart.

**Open questions:**
- What internal AI/data science capabilities exist within operational units?
- How is the Google Cloud partnership governed — joint venture, customer relationship, or strategic alliance?
- What specific AI applications are deployed beyond drones and predictive maintenance?
- Is there a technology/digital transformation leader below C-suite driving AI adoption?
- What metrics does NextEra use internally to measure AI success?



    ## Open Questions Across All Specimens

    - **Palantir**: What is Matt Welsh's (Head of AI Systems) specific scope vs. Shyam Sankar's product oversight?
- **Palantir**: How does the 'engineering commune' actually make decisions on major AI investments?
- **Palantir**: What is the internal structure of the AIP product team vs. Foundry vs. Gotham teams?
- **Palantir**: How autonomous are Forward Deployed Engineers in making AI decisions at customer sites?
- **ASML**: Does Yu Cao (Head of AI Program and Strategy) report to the CTO or CEO?
- **ASML**: What is the headcount of ASML's AI/ML teams?
- **ASML**: Is there a formal AI strategy document or internal AI organization beyond embedded functions?
- **ASML**: How does the Mistral AI partnership translate into organizational structure or team additions?
- **ASML**: What fraction of the 14,000+ R&D employees work on AI/ML specifically?
- **AstraZeneca**: Size of dedicated AI/data science headcount across the federated structure
- **AstraZeneca**: How the Modella AI acquisition (Q4 2025) changes oncology R&D AI structure
- **AstraZeneca**: Whether the Beijing AI lab represents a shift toward more centralized research AI
- **AstraZeneca**: Specific governance mechanisms for high-risk AI applications mentioned but not detailed
- **Rivian**: What is the exact headcount of Rivian's AI/autonomy teams across all locations?
- **Rivian**: What percentage of R&D spend is allocated to autonomy vs. other functions?
- **Rivian**: How does decision-making authority flow between the VW joint venture and Rivian's internal AI assistant work?
- **Rivian**: What is the timeline for achieving L4 autonomy that Scaringe references?
- **Rivian**: How does the London hub coordinate with Palo Alto—is it autonomous execution or tight integration?
- **Comcast / NBCUniversal**: Who leads AI strategy at the corporate level? No CAIO visible, unclear if someone owns cross-company AI coordination.
- **Comcast / NBCUniversal**: What happened to Media Labs? The NBCUniversal Technology Center launched in 2012 but current status is unclear.
- **Comcast / NBCUniversal**: How does Peacock's recommendation AI connect to broader AI strategy? 44M paid subscribers but AI team structure not visible.
- **Comcast / NBCUniversal**: Is there internal AI research beyond operational applications, or is LIFT Labs the primary exploration mechanism?
- **Comcast / NBCUniversal**: What is the VideoAI team structure that won the Technology Emmy? No leadership or organizational details found.
- **Spotify**: What is the headcount and budget for the various AI/ML research teams?
- **Spotify**: How does the new Generative AI Research Lab relate to existing research infrastructure?
- **Spotify**: What is the reporting structure for François Pachet's Creator Technology Research Lab?
- **Spotify**: How widely is the 'Honk' AI coding system deployed across engineering?
- **Spotify**: What percentage of Spotify's R&D is allocated to AI vs. other areas?
- **Stripe**: How exactly are Stripe's 'four AI focus areas' structured organizationally?
- **Stripe**: What is the size and composition of the Payments Foundation Model team?
- **Stripe**: How does Emily Glassberg Sands' 'Head of Information' role relate to AI leadership?
- **Stripe**: What is the formal reporting structure for AI initiatives — do they roll up through product, engineering, or a separate AI function?
- **Stripe**: How does the CRO of AI role coordinate with product/engineering on AI development vs. go-to-market?
- **NextEra Energy**: What internal AI/data science capabilities exist within operational units?
- **NextEra Energy**: How is the Google Cloud partnership governed — joint venture, customer relationship, or strategic alliance?
- **NextEra Energy**: What specific AI applications are deployed beyond drones and predictive maintenance?
- **NextEra Energy**: Is there a technology/digital transformation leader below C-suite driving AI adoption?
- **NextEra Energy**: What metrics does NextEra use internally to measure AI success?

    ## Failed Targets

    - AMD
- Caterpillar
- ABB

    ## Next Steps

    - Run `overnight-curate.py` to create specimen files from research findings
    - Run `overnight-purpose-claims.py` for newly created specimens
    - Review open questions above for research gaps
