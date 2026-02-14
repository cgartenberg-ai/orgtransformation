#!/usr/bin/env python3
"""
Purpose Claims Insights: Reframe + Add New
Session 22: Complementarity framing — purpose and structure as twin responses.

Changes:
1. AMEND rhetorical-division-mirrors-structure: reframe from "diagnostic tool" to
   "complementary organizational responses" — structure and rhetoric are co-produced.
2. AMEND survival-rhetoric-signals-structural-absence: strengthen — not just inverse
   correlation, but rhetorical *substitution* for missing structural response.
3. AMEND sector-rhetorical-signatures: sharpen — institutional constraints on purpose
   rhetoric are boundary conditions on organizational design choices.
4. AMEND inverse-grove: add rhetorical signature — how you can detect inverse Grove
   from purpose claims data.
5. ADD: purpose-structure-complementarity — the overarching insight.
6. ADD: ceo-silence-as-structural-signal — the CEO silence spectrum.
7. ADD: coasean-purpose-claims — theory-of-the-firm statements in purpose rhetoric.
"""

import json
import os
from datetime import date

PROJ = "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation"
INSIGHTS_PATH = os.path.join(PROJ, "synthesis/insights.json")
TODAY = date.today().isoformat()

with open(INSIGHTS_PATH) as f:
    data = json.load(f)

insights = data["insights"]
by_id = {ins["id"]: ins for ins in insights}

# ============================================================
# 1. AMEND: rhetorical-division-mirrors-structure
# Reframe from "diagnostic tool" to "complementary responses"
# ============================================================

ins = by_id["rhetorical-division-mirrors-structure"]
ins["title"] = "Purpose Rhetoric and Organizational Structure Are Co-Produced: The Division of Rhetorical Labor Mirrors Structural Design"
ins["finding"] = (
    "In M4 hub-and-spoke organizations, the division of purpose rhetoric between leaders "
    "mirrors the structural division between exploration and execution — not because rhetoric "
    "reveals structure (a diagnostic claim), but because the two are co-produced responses "
    "to the same organizational challenge. Structure allocates decision rights; purpose "
    "rhetoric allocates meaning-making rights. Together they constitute the organization's "
    "response to the AI transformation challenge. "
    "\n\nToyota is the sharpest case: Gill Pratt (exploration/TRI) speaks exclusively in "
    "teleological and higher-calling terms ('amplify not replace,' 'moral obligation,' "
    "'autonomy of people'), while Brian Kursar (execution/Enterprise AI) speaks exclusively "
    "in commercial-success terms ('20% productivity,' 'bridge research and production'). "
    "Neither crosses into the other's register. This is not Pratt 'signaling' his structural "
    "role — it's Pratt's purpose rhetoric and his structural mandate jointly constituting "
    "what TRI means inside Toyota. "
    "\n\nHoneywell shows a three-way complementarity: Kapur (CEO) handles "
    "utopian, survival, teleological, and higher-calling claims; Sheila Jordan (CDTO) "
    "handles only commercial-success claims ('flywheel,' 'early wins'); Venkatarayalu "
    "(CTO) handles framework claims. Each leader's rhetorical register and structural "
    "mandate are two aspects of the same organizational design choice. "
    "\n\nFord shows the pathological case: Farley monopolizes ALL purpose rhetoric; "
    "Doug Field (CTO/Latitude AI) is virtually silent — one press release quote in three "
    "years. The structural separation exists (Latitude AI is a subsidiary), but the "
    "complementary rhetorical separation doesn't. Farley hasn't delegated meaning-making "
    "to his exploration leader. This predicts coordination problems: the exploration "
    "unit has decision rights but not meaning-making authority. "
    "\n\nBMW is the counter-case: Zipse monopolizes all rhetoric because BMW's functional "
    "org doesn't structurally separate exploration from execution — there is no exploration "
    "leader to have a separate rhetorical register. The rhetorical concentration is "
    "complementary to the structural concentration. "
    "\n\nThe key theoretical claim: organizations that achieve complementarity between "
    "structural design and purpose rhetoric — where decision rights and meaning-making "
    "rights are coherently allocated — should outperform those where the two are misaligned. "
    "Ford (structural separation + rhetorical monopoly) is the predicted failure case. "
    "Toyota (structural separation + rhetorical separation) is the predicted success case."
)
ins["theoreticalConnection"] = (
    "This is fundamentally a complementarities argument (Milgrom & Roberts 1990, 1995): "
    "organizational design choices are interdependent, and the returns to one practice "
    "depend on the presence of others. Structural separation of exploration and execution "
    "is more effective when accompanied by complementary rhetorical separation — where "
    "exploration leaders make meaning-claims (teleological, higher-calling) and execution "
    "leaders make performance-claims (commercial-success, metrics). The co-production "
    "framing also connects to Gibbons & Henderson (2012) relational contracts: the "
    "rhetorical register a leader adopts is a form of implicit contract with their "
    "organizational constituency. And to March (1991): the language of exploration "
    "(possibility, purpose, horizon) is structurally different from the language of "
    "exploitation (efficiency, metrics, speed). What's new is treating purpose rhetoric "
    "not as a signal of structure, but as a co-equal design choice that must be coherent "
    "with structure to be effective."
)
# Add Ford misalignment as a testable implication
ins["testableImplications"] = [
    "Organizations with complementary structural + rhetorical division (Toyota, Honeywell) will show better AI exploration outcomes than those with misaligned division (Ford: structural separation + rhetorical monopoly)",
    "When organizations restructure AI leadership (new CAIO, new exploration unit), there should be a lag before rhetorical complementarity develops — the new leader needs to establish their rhetorical register",
    "M4 specimens where the hub leader and spoke leaders use the SAME rhetorical register (no differentiation) will show weaker hub-spoke coordination than specimens with differentiated registers",
    "If purpose rhetoric and structure are truly co-produced, changes to one should predict changes to the other — e.g., when a CTO is eliminated (Nike), the CEO's rhetorical register should shift to absorb the abandoned register"
]

# ============================================================
# 2. AMEND: survival-rhetoric-signals-structural-absence
# Strengthen: rhetorical *substitution* for missing structural response
# ============================================================

ins2 = by_id["survival-rhetoric-signals-structural-absence"]
ins2["title"] = "Survival Rhetoric as Rhetorical Substitute for Structural Response"
ins2["finding"] = (
    "When CEOs deploy survival-type purpose claims ('adapt or die,' 'no Plan B,' 'half "
    "of all white-collar workers'), they are not merely signaling structural inadequacy — "
    "they are *substituting* rhetoric for structure. Survival rhetoric does the organizational "
    "work that a structural response would do: it creates urgency, authorizes resource "
    "reallocation, and justifies disruption to existing routines. The key insight is that "
    "purpose and structure are complementary means of organizational transformation, and "
    "when one is absent, the other must carry more weight. "
    "\n\nFord is the clearest case: Farley leads with survival rhetoric (5 of 12 claims) "
    "and has the weakest dedicated AI exploration structure among automotive peers. Latitude AI "
    "exists but Farley's public narrative is almost entirely about workforce displacement, "
    "not product AI. The survival rhetoric is doing the work that a Neue Klasse-style "
    "structural commitment would do if Ford had one. "
    "\n\nCompare BMW: zero survival claims, but BMW has the Neue Klasse platform with 20x "
    "computing power and a permanent organizational design commitment ('we will never again "
    "separate hardware from software'). BMW's structural solution carries the transformation "
    "load; Zipse's rhetoric can focus on identity rather than urgency. "
    "\n\nHoneywell shows a third pattern: Kapur uses survival rhetoric but directs it "
    "*outward* at customers ('there is no Plan B' for labor shortages), not inward at "
    "Honeywell. This is consistent with Honeywell already having an internal structural "
    "solution (AI Ambassadors, six-chapter framework). When structure handles internal "
    "transformation, survival rhetoric can be redirected as a sales tool. "
    "\n\nThe hypothesis upgraded: survival rhetoric is not merely *correlated* with structural "
    "absence — it is a *functional substitute*. Organizations allocate their transformation "
    "effort across two channels: structural (org design, resource allocation, decision rights) "
    "and rhetorical (purpose claims, urgency narratives, identity assertions). When one "
    "channel is weak, the other must compensate. This predicts that survival rhetoric should "
    "*decrease* as structural solutions are built, not merely be absent from the start."
)
ins2["theoreticalConnection"] = (
    "Reframed through Milgrom & Roberts (1990, 1995) complementarities: structure and "
    "rhetoric are complementary organizational practices. When both are present and aligned, "
    "they reinforce each other (Toyota: TRI + Pratt's teleological rhetoric). When one is "
    "absent, the other becomes a substitute — but a weaker one, because the practices are "
    "super-modular (the returns to doing both exceed the sum of returns to each alone). "
    "Also connects to Hirschman (1970): survival rhetoric is organizational 'voice' — "
    "signaling that something is wrong. But voice is a substitute for structural 'exit' "
    "(reorganizing). And to March (1991): organizations that have structurally protected "
    "exploration don't need to rhetorically justify it. The rhetoric of urgency is a "
    "lagging indicator of structural inadequacy, but more precisely, it's a *substitute* "
    "that works less well than the structural response it replaces."
)
ins2["maturity"] = "emerging"  # upgrade from hypothesis — pattern holds across 4 automotive specimens + purpose claims data

# ============================================================
# 3. AMEND: sector-rhetorical-signatures
# Sharpen: institutional constraints as boundary conditions on design choices
# ============================================================

ins3 = by_id["sector-rhetorical-signatures"]
ins3["title"] = "Sector Institutions Constrain Both Structural Choices and Rhetorical Registers: The Boundary Conditions on Purpose-Structure Complementarity"
# Keep existing finding but add a crucial paragraph at the end
ins3["finding"] = ins3["finding"].rstrip() + (
    "\n\nCritically, this is not just about rhetoric — the institutional constraints that "
    "limit rhetorical registers also limit structural choices. Physical production constraints "
    "(unions, supply chains, safety regulation) both prevent utopian rhetoric AND prevent "
    "aggressive structural experimentation (M8 skunkworks, rapid pivots). The rhetorical "
    "constraints and structural constraints are two expressions of the same institutional "
    "boundary conditions. This means purpose-structure complementarity (see "
    "rhetorical-division-mirrors-structure) operates differently in industrial vs. tech "
    "sectors — not because complementarity doesn't hold, but because the feasible set of "
    "complementary pairs is narrower. Industrial firms can't pair utopian rhetoric with M8 "
    "skunkworks the way tech firms can. Their complementary pairs are necessarily more "
    "conservative: identity rhetoric + embedded AI (BMW), teleological rhetoric + M4 hub "
    "(Toyota), survival rhetoric + workforce restructuring (Ford)."
)
ins3["relatedInsights"] = [
    "survival-rhetoric-signals-structural-absence",
    "rhetorical-division-mirrors-structure",
    "purpose-structure-complementarity"
]

# ============================================================
# 4. AMEND: inverse-grove
# Add rhetorical signature — how you detect inverse Grove from purpose claims
# ============================================================

ins4 = by_id["inverse-grove"]
# Add to existing finding
ins4["finding"] = ins4["finding"].rstrip() + (
    "\n\nThe Inverse Grove has a distinctive *rhetorical signature* visible in purpose claims "
    "data. Leaders experiencing inverse Grove tend toward utopian and identity claims "
    "(authorizing the future they're building), while their organizations' front-line "
    "reality creates survival and commercial-success counter-narratives from middle "
    "management and technical leaders. The rhetorical gap between CEO claims and "
    "operational-leader claims may be a measurable proxy for the degree of inverse Grove. "
    "Salesforce is the sharpest case: Benioff's 'digital labor revolution' rhetoric (utopian) "
    "vs. the Agentforce team's deterministic Agent Script recalibration (commercial-success "
    "reality). BMW: Zipse's pure identity rhetoric (choosing, not threatened) vs. the "
    "implicit factory-floor reality of Neue Klasse integration. When the rhetorical distance "
    "between CEO and operational leaders is large, the organization is likely in inverse "
    "Grove territory."
)
ins4["relatedInsights"] = [
    "speed-depth-trap",
    "product-production-convergence",
    "purpose-structure-complementarity",
    "survival-rhetoric-signals-structural-absence"
]

# ============================================================
# 5. ADD: purpose-structure-complementarity (THE overarching insight)
# ============================================================

new_complementarity = {
    "id": "purpose-structure-complementarity",
    "title": "Purpose and Structure Are Complementary Organizational Responses to AI Transformation",
    "theme": "purpose-claims",
    "maturity": "emerging",
    "finding": (
        "The central finding from 1,082 purpose claims across 51 specimens: purpose rhetoric "
        "and organizational structure are not independent channels of organizational response "
        "to AI transformation — they are complementary practices in the Milgrom & Roberts "
        "(1990, 1995) sense. Organizations that achieve coherence between their structural "
        "choices (what model, what decision rights, what resource allocation) and their purpose "
        "rhetoric (what leaders say about why AI matters and what it means for the organization) "
        "appear to execute more effectively than organizations where structure and rhetoric are "
        "misaligned."
        "\n\nThe complementarity operates through several mechanisms:"
        "\n\n1. **Rhetorical division of labor mirrors structural division.** When organizations "
        "structurally separate exploration from execution (M4 hub-and-spoke), the most effective "
        "ones also separate *meaning-making*: exploration leaders use teleological/higher-calling "
        "rhetoric, execution leaders use commercial-success rhetoric. Toyota and Honeywell "
        "demonstrate this. Ford is the predicted failure case: structural separation (Latitude AI) "
        "without rhetorical delegation (Farley monopolizes all purpose claims)."
        "\n\n2. **Survival rhetoric substitutes for structural response.** When organizations "
        "lack a structural solution (no dedicated AI exploration unit, no resource commitment), "
        "survival rhetoric fills the gap — creating urgency and authorizing change rhetorically "
        "rather than structurally. Ford (heaviest survival, weakest structure) vs. BMW (zero "
        "survival, strongest structural commitment). The substitution works less well because "
        "rhetoric and structure are super-modular: doing both exceeds the sum of doing each alone."
        "\n\n3. **Sector institutions constrain both simultaneously.** The same institutional "
        "forces (physical production, unions, regulation) that limit structural choices (no M8 "
        "skunkworks in automotive) also limit rhetorical choices (no utopian claims from "
        "industrial CEOs). This narrows the feasible set of complementary purpose-structure "
        "pairs by sector."
        "\n\n4. **Rhetorical distance signals structural misalignment.** When the CEO's "
        "purpose claims are far from operational leaders' claims (Salesforce: utopian CEO vs. "
        "pragmatic product team), the organization is likely in 'inverse Grove' territory — "
        "headquarters outrunning front lines. The rhetorical gap is a measurable proxy for "
        "structural misalignment."
        "\n\n5. **Counter-positioning extends to rhetoric.** The AI-as-infrastructure vs. "
        "AI-as-actor counter-positioning is simultaneously a structural choice (embedded vs. "
        "named units) and a rhetorical choice (quiet identity vs. visible transformation). "
        "SAP/BMW (infrastructure + identity rhetoric) vs. Salesforce/Tesla (actor + utopian "
        "rhetoric)."
        "\n\nThis reframes the purpose claims track from 'how leaders communicate about AI' to "
        "'how organizations construct coherent transformation responses across multiple channels.' "
        "Purpose rhetoric is not window-dressing on organizational structure — it is a "
        "co-equal design choice."
    ),
    "evidence": [
        {
            "specimenId": "toyota",
            "note": "Highest complementarity: M4 structural separation perfectly mirrored by rhetorical separation (Pratt = teleological, Kursar = commercial-success). Neither crosses registers."
        },
        {
            "specimenId": "bmw",
            "note": "High complementarity (different form): functionally integrated structure complemented by concentrated identity rhetoric from single leader. No structural separation → no rhetorical separation. Coherent."
        },
        {
            "specimenId": "ford",
            "note": "Predicted misalignment: structural separation (Latitude AI) but rhetorical monopoly (Farley owns everything, Field is silent). Decision rights delegated, meaning-making rights not delegated."
        },
        {
            "specimenId": "salesforce",
            "note": "Inverse Grove misalignment: CEO purpose rhetoric (utopian, 'digital labor revolution') far outpaces organizational/product readiness (Agentforce quality issues). Rhetorical distance signals structural misalignment."
        },
        {
            "specimenId": "honeywell",
            "note": "Three-way complementarity: CEO (vision), CDTO (operations), CTO (methodology). Rhetorical specialization matches structural specialization exactly."
        },
        {
            "specimenId": "uber",
            "note": "Khosrowshahi's Coasean framing ('company is a rule') reflects M1+M3 structural choice: AI replaces coordination mechanisms, not just tasks. Purpose claim directly theorizes the firm's boundary."
        }
    ],
    "theoreticalConnection": (
        "This is a Milgrom & Roberts (1990, 1995) complementarities argument applied to "
        "organizational transformation. Structure and purpose rhetoric are complementary "
        "practices: the returns to a structural choice (e.g., creating an M4 hub) depend "
        "on the accompanying rhetorical choice (delegating meaning-making to the hub leader). "
        "Super-modularity predicts that organizations doing both coherently will outperform "
        "those doing one well and the other poorly. Connects to the broader complementarities "
        "literature (Brynjolfsson & Milgrom 2013 on IT and organizational practices): just as "
        "IT investment requires complementary organizational redesign, AI transformation "
        "requires complementary rhetorical redesign. Also builds on Gibbons & Henderson "
        "(2012) relational contracts: purpose rhetoric is a form of relational contract that "
        "makes structural choices credible and sustainable."
    ),
    "discoveredIn": "synthesis/sessions/2026-02-12-purpose-structure-complementarity.md",
    "relatedMechanisms": [1, 3, 7],
    "relatedTensions": [1, 4],
    "relatedInsights": [
        "rhetorical-division-mirrors-structure",
        "survival-rhetoric-signals-structural-absence",
        "sector-rhetorical-signatures",
        "inverse-grove",
        "ai-infrastructure-vs-actor-counter-positioning"
    ],
    "testableImplications": [
        "Organizations with high purpose-structure complementarity (coherent rhetoric + structure) will show better AI deployment outcomes (adoption rates, project completion, employee satisfaction) than organizations with low complementarity",
        "Survival rhetoric should decrease over time as structural solutions are built — a longitudinal prediction testable via earnings call analysis",
        "When a structural change occurs (new CAIO, new AI unit), there should be a measurable lag before purpose rhetoric adjusts to match, during which period the organization is temporarily misaligned",
        "Within-industry variance in purpose-structure complementarity should predict within-industry variance in AI transformation success better than either structural model or rhetorical register alone",
        "Ford (structural separation + rhetorical monopoly) should show weaker exploration outcomes than Toyota (structural separation + rhetorical delegation) despite similar structural models"
    ]
}

# ============================================================
# 6. ADD: ceo-silence-as-structural-signal
# ============================================================

new_silence = {
    "id": "ceo-silence-spectrum",
    "title": "The CEO Silence Spectrum: How CEO Engagement with AI Rhetoric Reveals Organizational AI Priority",
    "theme": "purpose-claims",
    "maturity": "emerging",
    "finding": (
        "CEOs range from total monopoly over AI purpose rhetoric to complete silence on AI, "
        "and the position on this spectrum is itself an organizational design choice that "
        "complements structural decisions."
        "\n\n**Sole-voice monopolists** (Uber, Anduril, Disney, Netflix): The CEO or founder "
        "makes ALL purpose claims about AI. No CTO, Chief Scientist, or CAIO is publicly "
        "visible in the purpose narrative. Khosrowshahi (16/16 claims), Luckey (12/12), "
        "Iger (14/14), Sarandos (13/14). This pattern signals that AI is a *CEO-level "
        "strategic concern*, not a technical one. The structural complement: these organizations "
        "typically don't have a strong separate AI exploration unit — the CEO IS the "
        "exploration mandate."
        "\n\n**Distributed speakers** (Toyota, Honeywell, Novo Nordisk): Multiple leaders "
        "make purpose claims, each in their own rhetorical register. This signals structural "
        "differentiation: AI has been organizationally distributed, and meaning-making rights "
        "have been distributed along with decision rights."
        "\n\n**CEO silence** (Nike): Hill makes ZERO AI claims despite being CEO of a company "
        "undergoing AI transformation. All AI rhetoric came from the CTO — and then the CTO "
        "role was eliminated in December 2025. The structural decision (killing the CTO role) "
        "*enacts* the rhetorical choice (AI is not part of this CEO's identity). This is the "
        "strongest evidence that some organizations are deliberately de-emphasizing AI in their "
        "purpose narrative, and the rhetorical de-emphasis and structural de-emphasis are "
        "complementary moves."
        "\n\nThe spectrum from sole-voice to silence maps predictably to organizational strategy: "
        "sole-voice CEOs are making AI-as-strategic-transformation bets; distributed speakers "
        "have operationalized AI across the org; silent CEOs are either deliberately subordinating "
        "AI to other priorities (Nike: sport identity) or haven't yet decided AI is CEO-level."
    ),
    "evidence": [
        {
            "specimenId": "uber",
            "note": "16/16 claims from Khosrowshahi. Zero from Ghahramani (Chief Scientist/AI Labs) or any CTO. Total CEO monopoly. AI is a CEO-level transformation bet."
        },
        {
            "specimenId": "anduril",
            "note": "12/12 claims from Luckey (founder, not CEO). Actual CEO Schimpf and Chairman Stephens make zero AI claims. Charismatic founder eclipses operational leadership entirely."
        },
        {
            "specimenId": "nike",
            "note": "CEO Hill: zero AI claims. All AI rhetoric from CTO Dogan (departed Dec 2025) and VP-level. Then CTO role eliminated. Rhetorical silence + structural elimination = complementary de-emphasis."
        },
        {
            "specimenId": "toyota",
            "note": "Distributed: Pratt (TRI), Kursar (Enterprise AI), Kon (CEO-level). Each speaks in own register. AI has been organizationally distributed."
        },
        {
            "specimenId": "disney",
            "note": "Iger: 14/14 claims. Maximum CEO concentration. CTO/CPTO invisible. 'Absent technical leader' pattern in media/entertainment."
        },
        {
            "specimenId": "netflix",
            "note": "Sarandos 13/14 claims, CTO Stone zero. CEO monopolizes AI rhetoric while CTO is invisible."
        }
    ],
    "theoreticalConnection": (
        "Connects to the complementarity between purpose rhetoric and structural design: "
        "who speaks about AI is itself an allocation of meaning-making rights that must "
        "be coherent with the allocation of decision rights. Sole-voice CEOs who haven't "
        "structurally delegated AI exploration are coherent (if sub-optimal). CEOs who "
        "have structurally delegated but retain rhetorical monopoly (Ford) are incoherent. "
        "Silent CEOs who have also structurally de-emphasized AI (Nike) are coherent in "
        "the opposite direction. The spectrum parallels Aghion & Tirole (1997) formal vs. "
        "real authority: CEOs may retain formal authority over AI purpose narratives while "
        "delegating real authority over AI decisions, or vice versa."
    ),
    "discoveredIn": "synthesis/sessions/2026-02-12-purpose-structure-complementarity.md",
    "relatedMechanisms": [1, 7],
    "relatedTensions": [4],
    "relatedInsights": [
        "purpose-structure-complementarity",
        "rhetorical-division-mirrors-structure"
    ],
    "watchFor": (
        "Does founder-led status predict sole-voice concentration? Both Uber (Khosrowshahi "
        "isn't founder but has founder-like authority) and Anduril (Luckey IS founder) show "
        "sole-voice. Check Amazon/Jassy, Tesla/Musk, Shopify/Lütke. Also: does CEO succession "
        "change the silence spectrum position? SK Telecom's Ryu succession changed rhetorical "
        "register — check if it changed speaker concentration too."
    )
}

# ============================================================
# 7. ADD: coasean-purpose-claims
# ============================================================

new_coase = {
    "id": "coasean-purpose-claims",
    "title": "Theory-of-the-Firm Purpose Claims: When Leaders Theorize Organizational Boundaries",
    "theme": "purpose-claims",
    "maturity": "hypothesis",
    "finding": (
        "A small but analytically significant subset of purpose claims go beyond authorizing "
        "transformation to explicitly theorize *why the firm exists* and *what AI does to "
        "the firm boundary*. These are Coasean purpose claims — statements where leaders, "
        "whether knowingly or not, engage with the theory of the firm."
        "\n\n**Uber — Khosrowshahi (Davos 2024):** 'What's a company? Essentially, it's a "
        "rule. It's a bunch of policies... What if, instead of a static set of guidelines, "
        "those rules could reason through every possible scenario?' This is practically a "
        "Coase (1937) paraphrase: the firm exists to reduce transaction costs via internal "
        "coordination rules, and AI may replace those coordination mechanisms. If AI can "
        "'reason through every possible scenario,' the coordination rationale for the firm "
        "dissolves."
        "\n\n**Satya Nadella (multiple contexts):** Has explicitly referenced Coase's theory — "
        "'The Coase argument for why firms exist is that there are transaction costs... AI is "
        "changing the nature of those costs.' This is the most explicitly theoretical CEO "
        "statement in the collection."
        "\n\n**McKinsey — Sternfels:** The '60K entities' framing (40K humans + 25K AI agents) "
        "implicitly treats AI agents as organizational members, blurring the firm boundary "
        "between human and machine labor. If agents are members, what does the firm boundary "
        "contain?"
        "\n\nThese claims are important because they reveal leaders grappling, in real time, "
        "with the foundational questions that organizational economists study: What is the "
        "firm? What determines its boundaries? What holds it together? Most purpose claims "
        "operate at the strategic level (what should we do about AI). Coasean claims operate "
        "at the ontological level (what IS the organization, and does AI change that answer). "
        "\n\nWe should flag these systematically. They connect purpose claims directly to "
        "our theoretical framework and may identify leaders whose mental models are closest "
        "to — or furthest from — the economic logic of organizational design."
    ),
    "evidence": [
        {
            "specimenId": "uber",
            "note": "Khosrowshahi: 'What's a company? Essentially, it's a rule.' Most explicitly Coasean CEO statement in collection. Reduces the firm to coordination mechanisms, then argues AI replaces them."
        },
        {
            "specimenId": "microsoft",
            "note": "Nadella has explicitly referenced Coase's theory of the firm in the context of AI reducing transaction costs. The only CEO who cites the academic literature by name."
        },
        {
            "specimenId": "mckinsey",
            "note": "Sternfels' '60K entities' framing treats AI agents as organizational members. Implicitly theorizes what the firm boundary contains — if 42% of your 'employees' are software, what is the boundary of the firm?"
        }
    ],
    "theoreticalConnection": (
        "Directly engages Coase (1937), Williamson (1975, 1985), and the property rights "
        "tradition. The question these leaders are grappling with — what happens to the firm "
        "when AI reduces coordination costs — is the central question of organizational "
        "economics applied to AI. Khosrowshahi's 'company is a rule' echoes Alchian & "
        "Demsetz (1972) team production: if AI can monitor and coordinate team production, "
        "the information advantage of internal organization over markets diminishes. Nadella's "
        "explicit Coase reference suggests some CEOs are consciously reasoning about firm "
        "boundaries. The McKinsey agent-as-member framing connects to Gibbons (2005) on "
        "what 'inside the firm' means when organizational membership becomes ambiguous. "
        "These claims are where practitioner language most closely approaches the academic "
        "conversation we're contributing to."
    ),
    "discoveredIn": "synthesis/sessions/2026-02-12-purpose-structure-complementarity.md",
    "relatedMechanisms": [],
    "relatedTensions": [1, 3],
    "relatedInsights": [
        "purpose-structure-complementarity",
        "product-production-convergence"
    ],
    "watchFor": (
        "Flag any purpose claim that explicitly or implicitly theorizes: (1) why the firm "
        "exists, (2) what the firm boundary contains, (3) what coordination mechanism AI "
        "replaces, (4) whether AI agents are 'inside' or 'outside' the firm. These are "
        "rare but analytically invaluable. Also watch for anti-Coasean claims — leaders "
        "who argue that AI makes the firm MORE necessary (e.g., because AI requires more "
        "organizational coordination, not less)."
    )
}

# ============================================================
# Insert new insights at the end
# ============================================================

insights.append(new_complementarity)
insights.append(new_silence)
insights.append(new_coase)

data["lastUpdated"] = TODAY

with open(INSIGHTS_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Updated insights.json:")
print(f"   - AMENDED: rhetorical-division-mirrors-structure (complementarity reframe)")
print(f"   - AMENDED: survival-rhetoric-signals-structural-absence (substitution framing, promoted to emerging)")
print(f"   - AMENDED: sector-rhetorical-signatures (boundary conditions framing)")
print(f"   - AMENDED: inverse-grove (added rhetorical signature)")
print(f"   - ADDED: purpose-structure-complementarity (overarching insight)")
print(f"   - ADDED: ceo-silence-spectrum")
print(f"   - ADDED: coasean-purpose-claims")
print(f"   Total insights: {len(insights)}")
