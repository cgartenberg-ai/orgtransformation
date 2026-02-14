#!/usr/bin/env python3
"""
Merge purpose claims from Session 24 research agent outputs into registry.json.

Sources:
- research/pending/xai-deep-scan-feb-2026.json (xAI - NEW specimen)
- research/pending/intuit-caio-deep-scan-feb-2026.json (Intuit - NEW specimen)
- research/pending/klarna-ai-backfire-feb-2026.json (Klarna - UPDATE with new claims)
- research/pending/salesforce-evolution-feb-2026.json (Salesforce - UPDATE with new claims)
- research/pending/press-sweep-feb-2026.json (multiple specimens - selective extraction)
- research/pending/caio-reorg-discovery-feb-2026.json (multiple specimens - selective extraction)
- research/pending/podcast-substack-sweep-feb-2026.json (Rivian - thin)

Deduplication strategy:
- xAI claims from deep-scan supersede overlapping claims from press-sweep and caio-reorg
- For already-scanned specimens (Klarna, Salesforce), only add claims that are genuinely new
- Skip claims from specimens with existing rich scans unless the quote is distinct
"""

import json
import os
from datetime import datetime

BASE = "/Users/cgart/Penn Dropbox/Claudine Gartenberg/Feedforward/playground/orgtransformation"
REGISTRY_PATH = os.path.join(BASE, "research/purpose-claims/registry.json")
TRACKER_PATH = os.path.join(BASE, "research/purpose-claims/scan-tracker.json")

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {path}")

def next_claim_num(registry, specimen_id):
    """Get the next claim number for a specimen (IDs are {specimen-id}--{NNN})."""
    max_num = 0
    for claim in registry.get("claims", []):
        cid = claim.get("id", "")
        if cid.startswith(f"{specimen_id}--"):
            try:
                num = int(cid.split("--")[1])
                if num > max_num:
                    max_num = num
            except (ValueError, IndexError):
                pass
    return max_num + 1

def make_claim(claim_num, specimen_id, speaker, role, verbatim, claim_type,
               rhetorical_function, context, source_url, source_date,
               collected_date="2026-02-12", secondary_type=None):
    """Create a claim in registry format."""
    claim = {
        "id": f"{specimen_id}--{claim_num:03d}",
        "specimenId": specimen_id,
        "speaker": speaker,
        "speakerRole": role,
        "verbatim": verbatim,
        "claimType": claim_type,
        "rhetoricalFunction": rhetorical_function,
        "context": context,
        "source": {
            "url": source_url,
            "sourceDate": source_date,
            "collectedDate": collected_date
        },
        "starred": False,
        "taxonomyVersion": "2.0"
    }
    if secondary_type:
        claim["secondaryType"] = secondary_type
    return claim

def main():
    registry = load_json(REGISTRY_PATH)
    tracker = load_json(TRACKER_PATH)

    initial_count = len(registry["claims"])
    new_claims = []

    print(f"Registry: {initial_count} claims")

    # ========================================
    # 1. xAI (NEW SPECIMEN) — from deep-scan
    # ========================================
    print("\n--- xAI (new specimen, from deep-scan) ---")

    xai_claims = [
        # Musk — scaling authorization
        ("Elon Musk", "CEO, xAI",
         "Because we've reached a certain scale, we're organizing the company to be more effective at this scale. Now, naturally, when this happens, there are some people who are better suited for the early stages of a company and less suited for the later stages.",
         "identity", "Naturalizing talent churn as inevitable consequence of scaling — framing departures as structural necessity. Uses evolutionary language ('suited for') to depersonalize forced separations.",
         "All-hands meeting announcing four-division restructuring after SpaceX acquisition and co-founder departures",
         "https://dnyuz.com/2026/02/12/3-takeaways-from-elon-musks-xai-all-hands-from-a-moon-city-to-a-company-restructuring/",
         "2026-02-12", None),

        # Musk — velocity as purpose
        ("Elon Musk", "CEO, xAI",
         "What matters is velocity and acceleration. If you are moving faster, you will be the leader.",
         "commercial-success", "Velocity as singular organizational metric — reduces all complexity to speed. Authorizes any structural change that increases speed.",
         "Addressing co-founder departures and restructuring",
         "https://futurism.com/artificial-intelligence/cofounders-fleeing-elon-musk-xai",
         "2026-02-11", None),

        # Musk — execution framing
        ("Elon Musk", "CEO, xAI",
         "We reorganized the company to improve the speed of execution, which unfortunately required parting ways with some people. We wish them all the best for their future endeavors.",
         "commercial-success", "Frames personnel losses as necessary cost of optimization. 'Speed of execution' as authorizing purpose. Euphemistic 'parting ways' obscures whether departures were voluntary.",
         "X post addressing wave of departures from xAI",
         "https://www.nbcnews.com/tech/elon-musk/xai-musk-addresses-wave-departures-xai-founder-rcna258651",
         "2026-02-11", None),

        # Musk — Macrohard recruiting
        ("Elon Musk", "CEO, xAI",
         "Join @xAI and help build a purely AI software company called Macrohard. It's a tongue-in-cheek name, but the project is very real! In principle, given that software companies like Microsoft do not themselves manufacture any physical hardware, it should be possible to simulate an entire software company using AI.",
         "utopian", "Reductionist economic logic to authorize radical organizational experiment. If a software company is 'just' information processing, and AI can do information processing, then AI can be the workforce. Reveals implicit theory of the firm: companies are information-processing systems.",
         "Public X post recruiting for Macrohard division",
         "https://x.com/elonmusk/status/1958852874236305793",
         "2026-02-11", "teleological"),

        # Pohlen — Macrohard vision
        ("Toby Pohlen", "Head of Macrohard, xAI",
         "It should be able to do everything on a computer that a computer can do. Rocket engines should be fully designed by AI.",
         "utopian", "Maximalist framing equating computational capability with organizational capability. Rocket engine example connects Macrohard to SpaceX's core business, justifying the merger.",
         "Presenting Macrohard vision at xAI all-hands meeting",
         "https://www.trendingtopics.eu/xai-announces-major-restructuring-following-spacex-merger-as-co-founders-exit/",
         "2026-02-12", None),

        # Musk — interplanetary compute
        ("Elon Musk", "CEO, xAI",
         "Ultimately, we see a path to maybe launching as much as a terawatt per year of compute from earth, but what if you want to go beyond a mere terawatt per year? In order to do that, you have to go to the moon.",
         "utopian", "Frames AI infrastructure as requiring space colonization — connecting xAI's mission to SpaceX's. Purpose claim that transcends any single company.",
         "All-hands meeting, outlining interplanetary infrastructure vision",
         "https://dnyuz.com/2026/02/12/3-takeaways-from-elon-musks-xai-all-hands-from-a-moon-city-to-a-company-restructuring/",
         "2026-02-12", None),

        # Musk — growth requires structure
        ("Elon Musk", "CEO, xAI",
         "When a company grows, especially as quickly as xAI, the structure must evolve. This unfortunately required the separation from some employees.",
         "identity", "Deterministic framing — growth 'requires' structural evolution which 'requires' departures. Removes agency by presenting as organizational necessity.",
         "Statement on restructuring and departures",
         "https://www.trendingtopics.eu/xai-announces-major-restructuring-following-spacex-merger-as-co-founders-exit/",
         "2026-02-12", None),

        # Ba — departing co-founder
        ("Jimmy Ba", "Co-founder, xAI (departing)",
         "Grateful to have helped cofound at the start. And enormous thanks to Elon Musk... It's time to recalibrate my gradient on the big picture.",
         "identity", "Uses ML metaphor ('recalibrate my gradient') to frame departure as personal optimization rather than organizational failure. 'Big picture' implies xAI has become too narrow for a research-oriented founder.",
         "Departure post on X, announcing last day at xAI",
         "https://futurism.com/artificial-intelligence/cofounders-fleeing-elon-musk-xai",
         "2026-02-11", None),

        # Kazemi — commodification critique
        ("Vahid Kazemi", "Technical staff (multimodal), xAI (departing)",
         "All AI labs are building the exact same thing, and it's boring.",
         "identity", "Commodification critique — frames AI lab work as undifferentiated. Challenges the organizational purpose claim that xAI is doing something unique. Researcher's statement that exploration phase is over.",
         "Departure statement, left before SpaceX merger",
         "https://www.nbcnews.com/tech/elon-musk/xai-musk-addresses-wave-departures-xai-founder-rcna258651",
         "2026-02-11", None),
    ]

    xai_next = next_claim_num(registry, "xai")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in xai_claims:
        claim = make_claim(xai_next, "xai", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        xai_next += 1
    print(f"  Added {len(xai_claims)} xAI claims")

    # ========================================
    # 2. Intuit (NEW SPECIMEN) — from deep-scan
    # ========================================
    print("\n--- Intuit (new specimen, from deep-scan) ---")

    intuit_claims = [
        ("Sasan Goodarzi", "Chairman and CEO, Intuit",
         "Companies that aren't prepared to take advantage of this AI revolution will fall behind and, over time, will no longer exist.",
         "survival", "Authorization through existential threat. Classic disruption narrative to legitimize restructuring (1,800 layoffs).",
         "Used to justify July 2024 restructuring",
         "https://aiinnovision.com/intuits-ai-restructuring-lessons-for-businesses-embracing-the-ai-revolution/",
         "2024-07-01", None),

        ("Sasan Goodarzi", "Chairman and CEO, Intuit",
         "Six years ago, we shared that we're betting the entire company on data and AI.",
         "identity", "Temporal anchoring. Dates AI commitment to 2019 to position Intuit as early mover, building credibility and deep commitment rather than trend-following.",
         "Retrospective framing of AI as long-term strategic commitment",
         "https://diginomica.com/disrupting-or-disrupted-ceo-sasan-goodarzi-intuits-response-taxing-questions-saas-vendors-around-ai",
         "2025-12-01", None),

        ("Sasan Goodarzi", "Chairman and CEO, Intuit",
         "SaaS companies will either be disrupted or they will be disruptors.",
         "survival", "Binary framing. Eliminates middle ground: no option to sit this out. Forces a choice between disrupting and being disrupted.",
         "Framing AI as industry inflection point for SaaS",
         "https://diginomica.com/disrupting-or-disrupted-ceo-sasan-goodarzi-intuits-response-taxing-questions-saas-vendors-around-ai",
         "2025-12-01", None),

        ("Sasan Goodarzi", "Chairman and CEO, Intuit",
         "To try to break out what's AI-driven is a meaningless exercise because the whole company is fueled by data and AI.",
         "identity", "Integration framing. Refuses to treat AI as separate business line. Delegitimizes questions about AI ROI by making AI indivisible from business.",
         "Response to questions about separating AI revenue",
         "https://diginomica.com/disrupting-or-disrupted-ceo-sasan-goodarzi-intuits-response-taxing-questions-saas-vendors-around-ai",
         "2025-12-01", None),

        ("Ashok Srivastava", "SVP & Chief AI and Data Officer, Intuit",
         "We fundamentally believe that in order to deliver the very best customer outcomes, we need to have the most advanced capabilities.",
         "teleological", "Capability-driven framing. Links advanced AI capabilities to customer outcomes rather than competitive positioning or cost reduction.",
         "Justification for creating Intuit Foresight unit",
         "https://fortune.com/2025/12/05/how-intuits-chief-ai-officer-supercharged-the-companys-emerging-technologies-teams-and-why-not-every-company-should-follow-his-lead/",
         "2025-12-05", None),

        ("Ashok Srivastava", "SVP & Chief AI and Data Officer, Intuit",
         "Just let them write code and experiment with customers.",
         "identity", "Autonomy and speed framing. Authorizes departure from standard corporate process in favor of builder autonomy. AI development requires different organizational norms.",
         "Describing approach to structuring AI agent development teams",
         "https://fortune.com/2025/09/03/chief-ai-officer-alliancebernstein-gen-digital/",
         "2025-09-03", None),

        ("Ashok Srivastava", "SVP & Chief AI and Data Officer, Intuit",
         "We're not just taking AI or machine learning off the shelf and deploying it.",
         "identity", "Builder identity claim. Establishes Intuit does foundational AI research, not just integration. Justifies investment in Foresight unit.",
         "Distinguishing Intuit's approach from companies that only integrate external AI",
         "https://hdsr.mitpress.mit.edu/pub/5bupaly7/release/1",
         "2025-01-01", None),

        ("Ivan Lazarov", "VP of Technology, Intuit",
         "Mere efficiency is just AI table stakes.",
         "teleological", "Raising the bar. Dismisses efficiency gains as insufficient, authorizing more ambitious organizational transformation. Creates space for Level 2 and Level 3 goals.",
         "Arguing real objective is rethinking products and work, not just faster processes",
         "https://www.bain.com/insights/beyond-ai-efficiency-a-conversation-with-intuits-ivan-lazarov/",
         "2025-11-01", None),

        ("Sandeep Aujla", "CFO, Intuit",
         "It's the customer's data, and it remains on our platform. Our standards for stewardship haven't changed one bit.",
         "identity", "Continuity and trust framing. Data stewardship as unchanged principle despite major strategic shifts. Addresses privacy concerns about OpenAI partnership.",
         "Addressing data privacy concerns about $100M+ OpenAI partnership",
         "https://fortune.com/2025/11/21/intuit-cfo-talks-100-million-openai-deal-innovation-road-ahead/",
         "2025-11-21", None),
    ]

    intuit_next = next_claim_num(registry, "intuit")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in intuit_claims:
        claim = make_claim(intuit_next, "intuit", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        intuit_next += 1
    print(f"  Added {len(intuit_claims)} Intuit claims")

    # ========================================
    # 3. Klarna (UPDATE) — genuinely new claims
    # ========================================
    print("\n--- Klarna (update with new claims) ---")

    klarna_claims = [
        ("Sebastian Siemiatkowski", "CEO, Klarna",
         "AI can already do all of the jobs that we, as humans, do.",
         "utopian", "Authorization of radical workforce reduction through AI supremacy framing. CEO retracted this within 5 months.",
         "Public statement, December 2024, before reversal",
         "https://futurism.com/klarna-openai-humans-ai-back",
         "2024-12-01", None),

        ("Sebastian Siemiatkowski", "CEO, Klarna",
         "As cost unfortunately seems to have been a too predominant evaluation factor when organizing this, what you end up having is lower quality.",
         "commercial-success", "Rare public admission of organizational design failure. Identifies specific mechanism: cost became 'predominant evaluation factor.' Not blaming technology but the organizational decision framework. DE-authorizes previous strategy.",
         "Public admission, May 2025, reversing AI-maximalist position",
         "https://cresta.com/news/klarna-shifts-focus-back-from-ai-to-human-interaction",
         "2025-05-01", None),

        ("Sebastian Siemiatkowski", "CEO, Klarna",
         "From a brand perspective, a company perspective, I just think it is so critical that you are clear to your customer that there will always be a human if you want.",
         "identity", "Re-authorization of human workforce by reframing from cost efficiency to brand identity and customer trust. Shifts evaluative frame from 'cheapest' to 'critical for the brand.'",
         "Bloomberg interview, May 2025, announcing human hiring reversal",
         "https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396",
         "2025-05-01", None),

        ("Sebastian Siemiatkowski", "CEO, Klarna",
         "We focused too much on efficiency and cost. The result was lower quality, and that is not sustainable.",
         "commercial-success", "Sustainability framing to authorize course correction. Uses 'not sustainable' to frame reversal as responsible long-term thinking rather than failure.",
         "Public statement explaining AI reversal rationale",
         "https://lasoft.org/blog/klarna-walks-back-ai-overhaul-rehires-staff-after-customer-service-backlash/",
         "2025-05-01", None),
    ]

    klarna_next = next_claim_num(registry, "klarna")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in klarna_claims:
        claim = make_claim(klarna_next, "klarna", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        klarna_next += 1
    print(f"  Added {len(klarna_claims)} Klarna claims")

    # ========================================
    # 4. Salesforce (UPDATE) — genuinely new claims
    # ========================================
    print("\n--- Salesforce (update with new claims) ---")

    salesforce_claims = [
        ("Marc Benioff", "CEO, Salesforce",
         "I've reduced it from 9,000 heads to about 5,000, because I need less heads.",
         "commercial-success", "Displacement authorization — explicitly links AI to headcount reduction with zero augmentation framing. Unusually direct for a CEO. Post-validation rhetorical shift.",
         "Logan Bartlett Show podcast, September 2025",
         "https://fortune.com/2025/09/02/salesforce-ceo-billionaire-marc-benioff-ai-agents-jobs-layoffs-customer-service-sales/",
         "2025-09-02", None),

        ("Marc Benioff", "CEO, Salesforce",
         "I don't think it's dystopian at all. This is reality, at least for me.",
         "identity", "Normalization — preemptively rejects dystopian framing of AI displacement. 'At least for me' acknowledges others may disagree while asserting his reality.",
         "Logan Bartlett Show podcast, September 2025",
         "https://fortune.com/2025/09/02/salesforce-ceo-billionaire-marc-benioff-ai-agents-jobs-layoffs-customer-service-sales/",
         "2025-09-02", None),

        ("Marc Benioff", "CEO, Salesforce",
         "It may not be the right thing to learn how to code anymore.",
         "utopian", "Skill obsolescence claim — a tech CEO telling people not to learn to code. Extends displacement from job functions to entire skill categories.",
         "Public statement on AI's impact on engineering workforce",
         "https://cloudwars.com/innovation-leadership/salesforce-ceo-marc-benioff-agentic-ai-will-thrill-customers-out-of-their-minds/",
         "2025-12-01", None),

        ("Joe Inzerillo", "President, Enterprise & AI Technology, Salesforce",
         "The fusion between the human workforce and the AI workforce — with the AI dictating terms based upon its capabilities — is the future of the agentic enterprise.",
         "utopian", "Inverts typical 'humans in the loop' narrative — AI sets terms, humans adapt. Techno-deterministic: work designed around AI capabilities rather than human needs.",
         "Metis Strategy interview on agentic enterprise design",
         "https://www.metisstrategy.com/interview/joe-inzerillo/",
         "2025-12-01", None),

        ("Joe Inzerillo", "President, Enterprise & AI Technology, Salesforce",
         "Part of the job of Customer Zero is we take the challenges on head on, helping refine the products so our customers don't have to go through that same pain.",
         "teleological", "Productization of internal suffering — reframes internal displacement as 'pain' that benefits customers. Virtuous cycle: we suffer first so customers don't have to.",
         "Diginomica interview on Customer Zero model",
         "https://diginomica.com/being-customer-zero-how-salesforces-first-chief-digital-officer-picking-learnings-agentic-ai",
         "2025-12-01", None),
    ]

    sf_next = next_claim_num(registry, "salesforce")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in salesforce_claims:
        claim = make_claim(sf_next, "salesforce", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        sf_next += 1
    print(f"  Added {len(salesforce_claims)} Salesforce claims")

    # ========================================
    # 5. Dow Chemical (UPDATE) — from caio-reorg
    # ========================================
    print("\n--- Dow Chemical (first claims) ---")

    dow_claims = [
        ("Karen S. Carter", "COO, Dow Inc.",
         "Transform to Outperform builds upon the self-help actions that we have implemented over the past few years. But importantly, it goes a lot further, representing a structural reengineering of our operating model and cost base.",
         "commercial-success", "Transformation-scale authorization — distinguishes current restructuring from prior incremental efforts to justify larger workforce reductions.",
         "Q4 2025 earnings call, announcing restructuring (4,500 positions, 13% of workforce)",
         "https://cen.acs.org/business/economy/dow-cut-4500-positions-ai/104/web/2026/01",
         "2026-01-29", None),
    ]

    dow_next = next_claim_num(registry, "dow-chemical")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in dow_claims:
        claim = make_claim(dow_next, "dow-chemical", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        dow_next += 1
    print(f"  Added {len(dow_claims)} Dow Chemical claims")

    # ========================================
    # 6. Anthropic (UPDATE) — from caio-reorg
    # ========================================
    print("\n--- Anthropic (update with new claims) ---")

    anthropic_claims = [
        ("Daniela Amodei", "President, Anthropic",
         "The speed of advancement in AI demands a different approach to how we build, how we organize, and where we focus.",
         "survival", "Urgency-based authorization — using pace of technological change to justify organizational restructuring (Labs unit expansion, CPO role change).",
         "Framing the leadership restructuring (Krieger → Labs, Vora → product)",
         "https://www.techbuzz.ai/articles/anthropic-reshuffles-leadership-to-expand-ai-labs-unit",
         "2026-01-14", None),

        ("Mike Krieger", "Co-lead Labs / Former CPO, Anthropic",
         "We've reached a watershed moment in AI -- model capabilities are advancing so fast that the window to shape how they're used is now.",
         "higher-calling", "Mission-urgency claim — invoking narrow window of opportunity to justify personal role change (CPO → hands-on builder in Labs). Unique: executive voluntarily steps DOWN to exploration role.",
         "Explaining why he stepped down from CPO to work hands-on in Labs incubator",
         "https://www.techbuzz.ai/articles/anthropic-reshuffles-leadership-to-expand-ai-labs-unit",
         "2026-01-14", None),
    ]

    anth_next = next_claim_num(registry, "anthropic")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in anthropic_claims:
        claim = make_claim(anth_next, "anthropic", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        anth_next += 1
    print(f"  Added {len(anthropic_claims)} Anthropic claims")

    # ========================================
    # 7. Pinterest (UPDATE) — from press-sweep
    # ========================================
    print("\n--- Pinterest (update with new claim) ---")

    pinterest_claims = [
        ("Bill Ready", "CEO, Pinterest",
         "Those working against the direction of the company and disagreeing with the mission should consider finding another job.",
         "identity", "Coercive alignment — uses mission/direction language to suppress dissent during AI transformation. Positions disagreement with restructuring as disloyalty to mission.",
         "Town hall meeting during AI restructuring, Feb 2026 (after engineers fired for building layoff-tracking tool)",
         "https://fortune.com/2026/02/04/pinterest-layoffs-employee-dissent-ai-tools-future-of-work-ceo-bill-ready/",
         "2026-02-04", "survival"),
    ]

    pin_next = next_claim_num(registry, "pinterest")
    for (speaker, role, verbatim, ctype, rfunc, context, url, sdate, sec) in pinterest_claims:
        claim = make_claim(pin_next, "pinterest", speaker, role, verbatim, ctype,
                          rfunc, context, url, sdate, secondary_type=sec)
        new_claims.append(claim)
        pin_next += 1
    print(f"  Added {len(pinterest_claims)} Pinterest claims")

    # ========================================
    # Merge into registry
    # ========================================
    print(f"\n=== MERGE SUMMARY ===")
    print(f"  New claims to add: {len(new_claims)}")

    registry["claims"].extend(new_claims)
    registry["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
    registry["totalClaims"] = len(registry["claims"])

    save_json(REGISTRY_PATH, registry)

    print(f"  Registry: {initial_count} → {len(registry['claims'])} claims")

    # ========================================
    # Update scan-tracker
    # ========================================
    print("\n--- Updating scan-tracker ---")
    spec_list = tracker.get("specimens", [])

    # Build lookup by specimenId for updates
    spec_index = {s["specimenId"]: i for i, s in enumerate(spec_list)}

    # New entries
    spec_list.append({
        "specimenId": "xai",
        "lastScanned": "2026-02-13",
        "claimsFound": 9,
        "quality": "rich"
    })

    spec_list.append({
        "specimenId": "intuit",
        "lastScanned": "2026-02-13",
        "claimsFound": 9,
        "quality": "rich"
    })

    # Updates to existing entries
    for spec_id, added_count in [("klarna", 4), ("salesforce", 5), ("dow-chemical", 1),
                                   ("anthropic", 2), ("pinterest", 1)]:
        if spec_id in spec_index:
            idx = spec_index[spec_id]
            old_count = spec_list[idx].get("claimsFound", 0)
            spec_list[idx]["claimsFound"] = old_count + added_count
            spec_list[idx]["lastScanned"] = "2026-02-13"
        else:
            spec_list.append({
                "specimenId": spec_id,
                "lastScanned": "2026-02-13",
                "claimsFound": added_count,
                "quality": "adequate" if added_count < 5 else "rich"
            })

    tracker["specimens"] = spec_list
    tracker["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    save_json(TRACKER_PATH, tracker)

    # ========================================
    # Final summary
    # ========================================
    print(f"\n=== DONE ===")
    print(f"  Claims: {initial_count} → {len(registry['claims'])}")
    print(f"  New specimens in tracker: xai, intuit")
    print(f"  Updated specimens: klarna (+4), salesforce (+5), dow-chemical (+1), anthropic (+2), pinterest (+1)")
    print(f"  Skipped (already rich): amazon-agi, workday, lionsgate, hp/hp-inc")
    print(f"  Skipped (too thin): rivian (2 operational claims), verses-ai (1), columbia-group (1)")

if __name__ == "__main__":
    main()
