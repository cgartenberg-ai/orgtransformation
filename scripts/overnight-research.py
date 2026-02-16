#!/usr/bin/env python3
"""
overnight-research.py
=====================
Orchestrates sequential research scans for new specimen targets via Claude CLI.
Reads target-specimens.json, builds prompts for each target, invokes
`claude -p --model opus` to search for structural AI findings, and writes
research output files for subsequent curation.

Unlike overnight-purpose-claims.py (which scans EXISTING specimens for claims),
this script discovers STRUCTURAL FINDINGS for companies that don't yet have
specimen files. Output goes to research/pending/ as research session files
that feed into the /curate workflow.

Usage:
    python3 scripts/overnight-research.py                     # Run all targets
    python3 scripts/overnight-research.py --dry-run           # Show queue
    python3 scripts/overnight-research.py --limit 5           # Only scan 5
    python3 scripts/overnight-research.py --company "Apple"   # Scan one company
    python3 scripts/overnight-research.py --quadrant Q4       # Scan one quadrant
    python3 scripts/overnight-research.py --priority high     # High priority only
    python3 scripts/overnight-research.py --skip-permissions  # Unattended mode

Run from project root: orgtransformation/
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path
from textwrap import dedent

# ─── Shared Library ─────────────────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import (
    save_json, load_json, acquire_lock, release_lock,
    preflight_check, setup_logging, write_changelog,
    PROJECT_ROOT, BLOCKED_DOMAINS,
)

# ─── Configuration ───────────────────────────────────────────────────────────

TARGET_LIST = PROJECT_ROOT / "research" / "target-specimens.json"
PENDING_DIR = PROJECT_ROOT / "research" / "pending"
SPECIMENS_DIR = PROJECT_ROOT / "specimens"
SESSION_DIR = PROJECT_ROOT / "research" / "sessions"
QUEUE_FILE = PROJECT_ROOT / "research" / "queue.json"
SOURCE_REGISTRY = PROJECT_ROOT / "specimens" / "source-registry.json"
EARNINGS_CALENDAR = PROJECT_ROOT / "research" / "earnings-calendar.json"
SPECIMEN_REGISTRY = PROJECT_ROOT / "specimens" / "registry.json"
SYNTHESIS_QUEUE = PROJECT_ROOT / "curation" / "synthesis-queue.json"
SCHEDULE_FILE = PROJECT_ROOT / "scripts" / "pipeline-schedule.json"

TIMEOUT_SECONDS = 25 * 60   # 25 minutes per agent
PAUSE_BETWEEN = 10           # seconds between agents
MAX_RETRIES = 1              # retry failed targets once

# Schedule theme modes (from pipeline-schedule.json)
SCHEDULE_THEMES = [
    "earnings", "press-keyword", "podcast-feed-check", "substacks",
    "enterprise-reports", "target-specimens", "target-specimens-enrich",
    "stale-refresh", "low-confidence", "taxonomy-gap-coverage",
    "daily-news-headlines", "industry-vertical-searches",
    "source-staleness-audit", "catch-up",
]

# ─── Logging ─────────────────────────────────────────────────────────────────

log = setup_logging("overnight-research")

# ─── Taxonomy Reference ─────────────────────────────────────────────────────

TAXONOMY = """
Structural Models (classify the organization into ONE primary model):
  M1 Research Lab — Fundamental research, breakthroughs. 3-10 year horizon. Pure exploration.
  M2 Center of Excellence — Governance, standards, enablement. 6-24 month horizon.
  M3 Embedded Teams — Product-specific AI features. Quarterly cadence.
  M4 Hybrid/Hub-and-Spoke — Central standards + distributed execution. Mixed horizons.
  M5 Product/Venture Lab — Commercialize AI into products/ventures. 6-36 months.
     5a Internal Incubator — Products absorbed into parent (Adobe Firefly)
     5b Venture Builder — Creates independent companies (Google X → Waymo)
     5c Platform-to-Product — Internal capability sold externally (Walmart GoLocal)
  M6 Unnamed/Informal — Quiet transformation without formal AI structure.
     6a Enterprise-Wide Adoption — Mass deployment, 80%+ adoption (BofA)
     6b Centralized-but-Unnamed — Central team without lab branding (P&G)
     6c Grassroots/Bottom-Up — Adoption preceded formal structure
  M7 Tiger Teams — Time-boxed exploration sprints. Weeks to months.
  M8 Skunkworks — Autonomous unit with radical independence. Years.
  M9 AI-Native — ONLY for orgs whose FOUNDING PURPOSE was AI/ML (e.g., Anthropic 2021,
     OpenAI 2015). NOT for data/analytics companies that later adopted AI. If the company
     didn't mention AI in founding materials and adopted AI language post-2020, it is NOT M9.

Ambidexterity Orientation (how they balance exploration vs. execution):
  Structural — Exploration and execution in distinct units
  Contextual — Individuals balance both within their roles
  Temporal — Organization cycles between exploration and execution phases
"""

FRAMEWORK_ANTENNA = """\
## Analytical Framework — Antenna (not filter)

Our emerging theory identifies 5 primitives that predict structural choice. While scanning,
keep antenna out for evidence related to these — but do NOT filter by them. Novel patterns
that fall outside this framework are just as valuable as those that confirm it.

  P1 Work Architecture Modularity — Can the work be decomposed into discrete tasks?
  P2 Work Output Measurability — Can quality be captured in quantitative metrics?
  P3 Governance Structure — Who has authority over AI decisions? Founder vs. hired CEO?
     Formal vs. real authority? Board/shareholder constraints?
  P4 Competitive/Institutional Context — Competitive intensity, regulation, industry norms
  P5 Organizational Endowment — Legacy systems, talent base, culture, prior AI investment

If you notice evidence about any of these — especially evidence that challenges or
complicates the framework, or reveals patterns we haven't captured — note it in
botanistNotes. Curiosity and exploration are the priority, not confirmation."""

# ─── Prompt Builders ─────────────────────────────────────────────────────────

def _extract_specimen_summary(slug: str) -> str:
    """Read an existing specimen file and extract a concise summary of what we already know."""
    specimen_file = SPECIMENS_DIR / f"{slug}.json"
    if not specimen_file.exists():
        return "(no existing specimen data)"

    try:
        with open(specimen_file) as f:
            spec = json.load(f)
    except (json.JSONDecodeError, KeyError):
        return "(could not parse existing specimen)"

    parts = []
    cls = spec.get("classification", {})
    parts.append(f"Current model: M{cls.get('model', '?')} ({cls.get('modelName', '?')})")
    parts.append(f"Orientation: {cls.get('orientation', '?')}")
    parts.append(f"Confidence: {cls.get('confidence', '?')}")

    desc = spec.get("description", "")
    if desc:
        parts.append(f"Description: {desc[:300]}{'...' if len(desc) > 300 else ''}")

    markers = spec.get("observableMarkers", {})
    for key in ("reportingStructure", "resourceAllocation", "timeHorizons", "decisionRights", "metrics"):
        val = markers.get(key, "")
        if val:
            parts.append(f"{key}: {val[:150]}{'...' if len(val) > 150 else ''}")

    sources = spec.get("sources", [])
    parts.append(f"Sources we already have ({len(sources)}):")
    for s in sources[:8]:
        parts.append(f"  - {s.get('name', '?')} ({s.get('sourceDate', '?')})")

    people = spec.get("keyPeople", [])
    if people:
        parts.append(f"Key people: {', '.join(p.get('name', '?') + ' (' + p.get('title', '?') + ')' for p in people[:6])}")

    return "\n".join(parts)


def build_enrich_prompt(target: dict) -> str:
    """Build a prompt for enriching an existing thin specimen with new data."""

    company = target["company"]
    leader = target["leader"]
    leader_title = target["leaderTitle"]
    sector = target["sector"]
    today = date.today().isoformat()
    slug = get_slug(company)
    output_path = str(PENDING_DIR / f"enrich-{slug}.json")

    existing = _extract_specimen_summary(slug)

    prompt = dedent(f"""\
    You are a research agent ENRICHING an existing thin specimen for "{company}".
    COMPLETE THIS IN UNDER 20 MINUTES.

    TASK: We already have a specimen file for {company} but it's LOW COMPLETENESS.
    Find NEW structural data — team sizes, reporting lines, investment figures,
    key people, recent developments — that we don't already have.

    ## SPEED RULES

    1. **NEVER make parallel WebFetch calls.** Fetch URLs ONE AT A TIME.
    2. **One retry max per URL.** If WebFetch fails, skip and move on.
    3. **Stop fetching after 6 URLs.** Prioritize quality over quantity.
    4. **Skip paywalled domains:** {', '.join(BLOCKED_DOMAINS)}
    5. **Skip mckinsey.com** — hangs indefinitely.

    ## What We Already Know

    {existing}

    ## What We NEED (focus your searches here)

    1. **Team sizes and headcount** — How many people work in AI? Named team sizes?
    2. **Reporting lines** — Who does the AI leader report to? Org chart details?
    3. **Investment signals** — AI budget, CapEx, % of R&D allocated to AI?
    4. **Recent developments (2025-2026)** — New AI hires, restructurings, product launches?
    5. **Key quotes** — Verbatim quotes from {leader} or AI leaders about strategy/structure
    6. **Named AI units/labs** — Specific team names, charter, mandate?
    7. **Time horizons and metrics** — How does the org measure AI success?

    DO NOT repeat information we already have. Only add NEW findings.

    ## Search Queries — Run ALL 5

    1. "{company}" AI team structure OR organization OR headcount 2025 2026
    2. "{leader}" AI strategy OR investment OR transformation interview 2025 2026
    3. "{company}" AI earnings call OR annual report OR investor day 2025 2026
    4. "{company}" AI chief OR CAIO OR CDO OR "head of AI" appointment
    5. "{company}" AI lab OR research center OR "center of excellence" 2025 2026

    ## Output

    Write a JSON file to: {output_path}

    Use this structure:
    {{
      "company": "{company}",
      "enrichmentDate": "{today}",
      "mode": "enrich",
      "searchesCompleted": 5,
      "urlsFetched": 0,
      "fetchFailures": [],

      "newFindings": {{
        "teamStructure": "NEW details about AI team organization not in existing specimen",
        "keyPeople": [
          {{"name": "...", "title": "...", "role": "...", "isNew": true}}
        ],
        "investmentSignals": "NEW budget/headcount/CapEx data",
        "recentDevelopments": "NEW hires, restructurings, products from 2025-2026",
        "observableMarkers": {{
          "reportingStructure": "NEW or updated reporting lines",
          "resourceAllocation": "NEW budget/allocation data",
          "timeHorizons": "NEW horizon data",
          "decisionRights": "NEW decision-rights data",
          "metrics": "NEW metrics data"
        }},
        "classificationUpdate": "If the current M-classification seems wrong based on new data, explain why and suggest a correction. Otherwise say 'classification confirmed'."
      }},

      "quotes": [
        {{
          "text": "EXACT VERBATIM QUOTE",
          "speaker": "Full Name",
          "speakerTitle": "Title",
          "source": "Source name",
          "sourceUrl": "URL",
          "sourceDate": "YYYY-MM-DD or YYYY-MM",
          "context": "What was the occasion/topic"
        }}
      ],

      "sources": [
        {{
          "name": "Source name",
          "url": "URL",
          "type": "Earnings Call|Press|Interview|Conference|Blog|Report",
          "date": "YYYY-MM-DD or YYYY-MM",
          "notes": "What was useful in this source"
        }}
      ],

      "summary": "2-3 sentence summary of what NEW we learned about this organization",
      "openQuestions": ["Things we still couldn't determine"],
      "botanistNotes": [
        "2-3 analytical observations about what the new data reveals",
        "- Does the new data change our understanding of the specimen?",
        "- Any surprises or pattern-breaking findings?"
      ]
    }}

    IMPORTANT:
    - Only include VERBATIM quotes — never paraphrase
    - Only include NEW information not already in our specimen
    - Always include source URLs
    - It's fine to write a file with limited new findings — "we looked and found little new" is data
    """)

    return prompt


def build_research_prompt(target: dict) -> str:
    """Build the full prompt for a research agent scanning a new target company."""

    company = target["company"]
    leader = target["leader"]
    leader_title = target["leaderTitle"]
    sector = target["sector"]
    quadrant = target["quadrant"]
    conference = target.get("conference") or "None known"
    rationale = target["rationale"]
    ticker = target.get("ticker") or "PRIVATE"
    today = date.today().isoformat()

    # Generate a slug for the output file
    slug = company.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    output_path = str(PENDING_DIR / f"{slug}.json")

    prompt = dedent(f"""\
    You are a research agent scanning "{company}" for organizational AI structure findings.
    COMPLETE THIS IN UNDER 20 MINUTES.

    TASK: Discover how {company} structures its AI work — team structure, leadership,
    reporting lines, investment levels, strategic framing — and produce a structured
    research output file.

    ## SPEED RULES

    1. **NEVER make parallel WebFetch calls.** Fetch URLs ONE AT A TIME.
    2. **One retry max per URL.** If WebFetch fails, skip and move on.
    3. **Stop fetching after 6 URLs.** Prioritize quality over quantity.
    4. **Skip paywalled domains:** {', '.join(BLOCKED_DOMAINS)}

    ## Target Context

    - Company: {company}
    - Ticker: {ticker}
    - CEO/Leader: {leader} ({leader_title})
    - Sector: {sector}
    - Quadrant: {quadrant}
    - Conference presence: {conference}
    - Why we're scanning: {rationale}

    ## What We're Looking For

    We study how organizations STRUCTURALLY enable both AI exploration and operational
    execution. For each company, we need to understand:

    1. **AI Team Structure**: Is there a dedicated AI team/lab? How is it organized?
       Who leads it? Does it report to the CEO, CTO, a CAIO, or somewhere else?
    2. **Structural Model**: Which of these 9 models best fits? (see taxonomy below)
    3. **Key People**: CEO, CAIO/CDO/Head of AI, key AI leaders and their titles
    4. **Investment Level**: AI headcount, budget, % of R&D, CapEx commitments
    5. **Observable Markers**: Reporting structure, resource allocation, time horizons,
       decision rights, metrics used
    6. **Key Quotes**: Verbatim quotes from leaders about AI strategy, purpose, vision
    7. **Sources**: URLs for everything — earnings calls, press, interviews, conference talks

    {TAXONOMY}

    {FRAMEWORK_ANTENNA}

    ## Search Queries — Run ALL 5

    1. "{company}" AI team OR "AI organization" OR "chief AI officer" OR CAIO structure
    2. "{leader}" AI strategy OR vision OR transformation OR investment 2025 2026
    3. "{company}" AI earnings call OR annual report OR shareholder letter 2025 2026
    4. "{company}" AI lab OR research OR "center of excellence" OR hub
    5. "{company}" "{leader}" AI interview OR podcast OR keynote OR conference

    ## WebFetch Instructions

    Fetch URLs ONE AT A TIME. Prioritize:
    1. **Earnings call transcripts** — richest structural data (team sizes, investment, reporting)
    2. **Press profiles / long-form interviews** — how leaders frame AI strategy
    3. **Conference talks** — especially from: {conference}
    4. **Company newsroom / blog posts** — official announcements of AI initiatives

    Prompt WebFetch with: "Extract all information about {company}'s AI strategy,
    team structure, leadership, investment, and organizational approach to AI.
    Include all direct quotes from executives."

    ## Output

    Write a JSON file to: {output_path}

    Use this structure:
    {{
      "company": "{company}",
      "ticker": "{ticker}",
      "leader": "{leader}",
      "leaderTitle": "{leader_title}",
      "sector": "{sector}",
      "quadrant": "{quadrant}",
      "scannedDate": "{today}",
      "searchesCompleted": 5,
      "urlsFetched": N,
      "fetchFailures": [],

      "structuralFindings": {{
        "suggestedModel": N,
        "suggestedModelName": "e.g. Hybrid/Hub-and-Spoke",
        "suggestedOrientation": "Structural|Contextual|Temporal",
        "confidence": "High|Medium|Low",
        "rationale": "Why this classification, based on evidence found",
        "aiTeamStructure": "Description of how AI work is organized",
        "keyPeople": [
          {{"name": "...", "title": "...", "role": "..."}}
        ],
        "investmentSignals": "Budget, headcount, CapEx, % of R&D",
        "observableMarkers": {{
          "reportingStructure": "Who does AI report to?",
          "resourceAllocation": "Dedicated budget? Shared? Ring-fenced?",
          "timeHorizons": "Short-term (quarters) vs. long-term (years)?",
          "decisionRights": "Centralized vs. distributed AI decisions?",
          "metrics": "What does the org measure for AI success?"
        }}
      }},

      "quotes": [
        {{
          "text": "EXACT VERBATIM QUOTE",
          "speaker": "Full Name",
          "speakerTitle": "Title",
          "source": "Source name",
          "sourceUrl": "URL",
          "sourceDate": "YYYY-MM-DD or YYYY-MM",
          "context": "What was the occasion/topic"
        }}
      ],

      "sources": [
        {{
          "name": "Source name",
          "url": "URL",
          "type": "Earnings Call|Press|Interview|Conference|Blog|Report",
          "date": "YYYY-MM-DD or YYYY-MM",
          "notes": "What was useful in this source"
        }}
      ],

      "summary": "2-3 sentence summary of how this organization structures AI work",
      "openQuestions": ["Things we couldn't determine from available sources"],
      "conferenceFindings": "What we found about their conference presentation, if applicable",

      "botanistNotes": [
        "2-4 analytical observations from a research botanist's perspective:",
        "- What is most structurally interesting or surprising about this org?",
        "- Any patterns that connect to or challenge the taxonomy?",
        "- How does this compare to what you'd expect for this industry/size?",
        "- Any provocative quotes that reveal how leaders THINK about AI structure?"
      ],
      "bestQuote": {{
        "text": "The single most revealing/provocative quote found — the one that best captures how this org thinks about AI",
        "speaker": "Full Name",
        "why": "Why this quote is analytically interesting"
      }}
    }}

    IMPORTANT:
    - Only include VERBATIM quotes — never paraphrase
    - Always include source URLs — no URL, no finding
    - If you can't determine the structural model with confidence, say so in rationale
    - It's fine to write a file with limited findings — "we looked and found little" is data
    - If the company is very secretive about AI structure (e.g., Apple), document THAT as a finding
    - The botanistNotes field is CRITICAL — this is where you record your analytical observations
      as a researcher. Don't just describe what you found; note what's interesting, surprising,
      or pattern-breaking about it.
    """)

    return prompt

# ─── Theme-Based Target Selection ─────────────────────────────────────────────

def _load_source_registry() -> list[dict]:
    """Load source-registry.json and return sources list."""
    if not SOURCE_REGISTRY.exists():
        log.warning("source-registry.json not found")
        return []
    data = load_json(SOURCE_REGISTRY)
    return data.get("sources", [])


def _load_earnings_calendar() -> dict:
    """Load earnings-calendar.json."""
    if not EARNINGS_CALENDAR.exists():
        log.warning("earnings-calendar.json not found")
        return {}
    return load_json(EARNINGS_CALENDAR)


def _load_specimen_registry() -> dict:
    """Load specimens/registry.json."""
    if not SPECIMEN_REGISTRY.exists():
        log.warning("specimens/registry.json not found")
        return {}
    return load_json(SPECIMEN_REGISTRY)


def _stale_sources(max_age_days: int = 14) -> list[dict]:
    """Find sources with scannedThroughDate older than max_age_days."""
    from datetime import timedelta
    sources = _load_source_registry()
    cutoff = date.today() - timedelta(days=max_age_days)
    stale = []
    for s in sources:
        sdate = s.get("scannedThroughDate")
        if not sdate or not isinstance(sdate, str):
            stale.append(s)
            continue
        try:
            d = date.fromisoformat(sdate)
            if d < cutoff:
                stale.append(s)
        except ValueError:
            stale.append(s)
    # Sort by staleness (oldest first), then by tier (lower = higher priority)
    def sort_key(s):
        sdate = s.get("scannedThroughDate") or "2020-01-01"
        if not isinstance(sdate, str):
            sdate = "2020-01-01"
        try:
            d = date.fromisoformat(sdate)
        except ValueError:
            d = date(2020, 1, 1)
        return (d, s.get("tier", 99))
    stale.sort(key=sort_key)
    return stale


def build_theme_targets(theme_name: str, limit: int, theme_config: dict | None = None) -> list[dict]:
    """Build a target list for a given schedule theme.

    Returns a list of synthetic target dicts with at minimum:
      { "company": str, "mode": str, "prompt": str }
    The "prompt" key holds the full agent prompt. This is different from the
    target-specimens workflow where prompts are built later.
    """
    today = date.today().isoformat()

    if theme_name == "earnings":
        return _targets_earnings(limit, today)
    elif theme_name == "press-keyword":
        return _targets_press_keyword(limit, today)
    elif theme_name == "podcast-feed-check":
        sources_filter = (theme_config or {}).get("sources", [])
        return _targets_podcast_feed_check(limit, today, sources_filter)
    elif theme_name == "substacks":
        sources_filter = (theme_config or {}).get("sources", [])
        return _targets_substacks(limit, today, sources_filter)
    elif theme_name == "enterprise-reports":
        return _targets_enterprise_reports(limit, today)
    elif theme_name == "target-specimens":
        return _targets_target_specimens(limit, enrich=False)
    elif theme_name == "target-specimens-enrich":
        return _targets_target_specimens(limit, enrich=True)
    elif theme_name == "stale-refresh":
        return _targets_stale_refresh(limit, today)
    elif theme_name == "low-confidence":
        return _targets_low_confidence(limit, today)
    elif theme_name == "taxonomy-gap-coverage":
        return _targets_taxonomy_gaps(limit, today)
    elif theme_name == "daily-news-headlines":
        return _targets_daily_news(limit, today)
    elif theme_name == "industry-vertical-searches":
        return _targets_industry_discovery(limit, today)
    elif theme_name == "source-staleness-audit":
        return _targets_staleness_audit(limit, today)
    elif theme_name == "catch-up":
        return _targets_catch_up(limit, today)
    else:
        log.warning(f"Unknown theme: {theme_name}")
        return []


def _make_theme_target(company: str, mode: str, prompt: str, slug: str = "") -> dict:
    """Create a synthetic target dict for theme-based research."""
    if not slug:
        slug = get_slug(company)
    return {
        "company": company,
        "mode": mode,
        "leader": "",
        "leaderTitle": "",
        "sector": mode,
        "quadrant": "THEME",
        "priority": "high",
        "prompt": prompt,
        "_slug": slug,
    }


def _targets_earnings(limit: int, today: str) -> list[dict]:
    """Find unscanned earnings calls from the earnings calendar."""
    cal = _load_earnings_calendar()
    companies = cal.get("companies", [])
    targets = []
    for co in companies:
        name = co.get("company", "")
        ticker = co.get("ticker", "")
        if not name:
            continue
        slug = get_slug(name)
        pending_file = PENDING_DIR / f"earnings-{slug}.json"
        if pending_file.exists():
            continue
        prompt = dedent(f"""\
        You are a research agent scanning the latest earnings call for "{name}" ({ticker}).
        COMPLETE THIS IN UNDER 20 MINUTES.

        ## SPEED RULES
        1. NEVER make parallel WebFetch calls. Fetch URLs ONE AT A TIME.
        2. One retry max per URL. If WebFetch fails, skip and move on.
        3. Stop fetching after 6 URLs.
        4. Skip paywalled domains: {', '.join(BLOCKED_DOMAINS)}
        5. Skip mckinsey.com — hangs indefinitely.

        ## TASK
        Find the most recent quarterly earnings call transcript for {name} ({ticker}).
        Extract ALL organizational-structural AI information:
        1. AI team changes, restructurings, new hires
        2. AI investment figures (CapEx, headcount, budget)
        3. AI product/platform announcements
        4. Structural keywords: reorganization, new division, CAIO, center of excellence
        5. Workforce changes tied to AI (layoffs, reskilling, hiring)
        6. Verbatim quotes from executives about AI strategy and structure

        ## Search Queries — Run ALL 5
        1. "{name}" "{ticker}" earnings call transcript Q4 2025 OR Q1 2026
        2. "{name}" earnings AI restructuring OR reorganization 2025 2026
        3. "{name}" AI investment OR CapEx OR headcount 2025 2026
        4. "{name}" chief AI officer OR CAIO OR "head of AI" 2025 2026
        5. "{name}" AI strategy OR transformation earnings call

        ## Output
        Write a JSON file to: {str(PENDING_DIR / f'earnings-{slug}.json')}
        {{
          "company": "{name}",
          "ticker": "{ticker}",
          "scannedDate": "{today}",
          "mode": "earnings",
          "quarter": "Q? FY????",
          "searchesCompleted": 5,
          "urlsFetched": 0,
          "structuralFindings": {{
            "aiTeamChanges": "...",
            "investmentSignals": "...",
            "workforceChanges": "...",
            "productAnnouncements": "..."
          }},
          "quotes": [],
          "sources": [],
          "summary": "2-3 sentence summary",
          "botanistNotes": []
        }}
        """)
        targets.append(_make_theme_target(name, "earnings", prompt, f"earnings-{slug}"))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_press_keyword(limit: int, today: str) -> list[dict]:
    """Generate press keyword sweep agents."""
    keyword_sets = [
        ("CAIO-appointments", '"chief AI officer" OR CAIO appointed OR hired 2025 2026'),
        ("AI-restructuring", 'AI restructuring OR reorganization OR "new AI division" 2025 2026'),
        ("AI-lab-launch", '"AI lab" OR "AI research center" OR "center of excellence" launched 2025 2026'),
        ("AI-workforce", 'AI layoffs OR reskilling OR "AI headcount" OR "AI hiring" 2025 2026'),
        ("AI-strategy-shift", '"AI strategy" OR "AI transformation" chief OR CEO interview 2025 2026'),
        ("AI-agent-deployment", '"AI agents" OR "agentic AI" enterprise deployment OR rollout 2025 2026'),
    ]
    targets = []
    for kw_name, kw_query in keyword_sets:
        slug = f"press-{kw_name}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        prompt = dedent(f"""\
        You are a research agent doing a press keyword sweep for organizational AI structure signals.
        COMPLETE THIS IN UNDER 20 MINUTES.

        ## SPEED RULES
        1. NEVER make parallel WebFetch calls. Fetch URLs ONE AT A TIME.
        2. One retry max per URL. If WebFetch fails, skip and move on.
        3. Stop fetching after 8 URLs.
        4. Skip paywalled domains: {', '.join(BLOCKED_DOMAINS)}
        5. Skip mckinsey.com — hangs indefinitely.

        ## TASK
        Search for recent press articles about: {kw_query}
        For each article found, extract:
        - Company name and what structural change was announced
        - Key people involved (names, titles)
        - Verbatim quotes about AI organization/structure
        - Source URL and date

        ## Search Queries — Run ALL 3
        1. {kw_query}
        2. {kw_query} site:reuters.com OR site:cnbc.com OR site:fortune.com
        3. {kw_query} -site:bloomberg.com -site:wsj.com

        ## Output
        Write a JSON file to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "press-keyword",
          "keyword": "{kw_name}",
          "scannedDate": "{today}",
          "searchesCompleted": 3,
          "urlsFetched": 0,
          "findings": [
            {{
              "company": "Company Name",
              "finding": "What was announced/discovered",
              "keyPeople": [{{"name": "...", "title": "..."}}],
              "quotes": [{{"text": "VERBATIM", "speaker": "Name", "source": "URL"}}],
              "sourceUrl": "URL",
              "sourceDate": "YYYY-MM-DD",
              "structuralRelevance": "high|medium|low"
            }}
          ],
          "summary": "Overview of what this sweep found",
          "newSpecimenCandidates": ["company names worth creating specimens for"]
        }}
        """)
        targets.append(_make_theme_target(kw_name, "press-keyword", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_podcast_feed_check(limit: int, today: str, sources_filter: list[str]) -> list[dict]:
    """Check podcast feeds for new episodes with structural content."""
    sources = _load_source_registry()
    podcasts = [s for s in sources if s.get("type") == "Podcast"]
    if sources_filter:
        podcasts = [s for s in podcasts if s["id"] in sources_filter]
    # Sort by staleness
    podcasts.sort(key=lambda s: s.get("scannedThroughDate", "2020-01-01"))
    targets = []
    for pod in podcasts:
        slug = f"podcast-{pod['id']}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        scanned = pod.get("scannedThrough", "unknown")
        prompt = dedent(f"""\
        You are a research agent checking the podcast feed for "{pod['name']}".
        COMPLETE THIS IN UNDER 15 MINUTES.

        ## SPEED RULES
        1. NEVER make parallel WebFetch calls. Fetch URLs ONE AT A TIME.
        2. One retry max per URL. If WebFetch fails, skip and move on.
        3. Stop fetching after 4 URLs.
        4. Skip paywalled domains: {', '.join(BLOCKED_DOMAINS)}
        5. Skip mckinsey.com — hangs indefinitely.

        ## CONTEXT
        - Podcast: {pod['name']}
        - Host: {pod.get('host', 'unknown')}
        - URL: {pod.get('url', '')}
        - Last scanned through: {scanned}
        - Last scan date: {pod.get('lastScanned', 'unknown')}

        ## TASK
        1. Check if there are NEW episodes since our last scan
        2. For any new episodes, assess structural relevance (HIGH/MEDIUM/LOW)
        3. For HIGH relevance episodes: extract key findings and quotes
        4. For MEDIUM: note the episode for future deep-scan
        5. Update what we've scanned through

        ## Search Queries — Run 2-3
        1. "{pod['name']}" podcast latest episodes 2026
        2. site:{pod.get('url', '').replace('https://', '').split('/')[0]} episodes
        3. "{pod['name']}" AI organization OR structure OR leadership episode

        ## Output
        Write a JSON file to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "podcast-feed-check",
          "sourceId": "{pod['id']}",
          "sourceName": "{pod['name']}",
          "scannedDate": "{today}",
          "previousScannedThrough": "{scanned}",
          "newScannedThrough": "Description of latest episode checked",
          "newEpisodes": [
            {{
              "title": "Episode title",
              "date": "YYYY-MM-DD",
              "guest": "Guest name",
              "relevance": "HIGH|MEDIUM|LOW",
              "structuralFindings": "What was found (if HIGH)",
              "quotes": [],
              "deepScanNeeded": false
            }}
          ],
          "summary": "What changed since last scan",
          "newSpecimenCandidates": []
        }}
        """)
        targets.append(_make_theme_target(pod['name'], "podcast-feed-check", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_substacks(limit: int, today: str, sources_filter: list[str]) -> list[dict]:
    """Check substacks for new posts with structural content."""
    sources = _load_source_registry()
    subs = [s for s in sources if s.get("type") in ("Substack", "Newsletter", "Blog")]
    if sources_filter:
        subs = [s for s in subs if s["id"] in sources_filter]
    subs.sort(key=lambda s: s.get("scannedThroughDate") or "2020-01-01")
    targets = []
    for sub in subs:
        slug = f"substack-{sub['id']}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        scanned = sub.get("scannedThrough", "unknown")
        prompt = dedent(f"""\
        You are a research agent checking the publication "{sub['name']}" for new AI-organizational content.
        COMPLETE THIS IN UNDER 15 MINUTES.

        ## SPEED RULES
        1. NEVER make parallel WebFetch calls. ONE AT A TIME.
        2. One retry max. Stop after 4 URLs.
        3. Skip: {', '.join(BLOCKED_DOMAINS)}, mckinsey.com

        ## CONTEXT
        - Publication: {sub['name']}
        - URL: {sub.get('url', '')}
        - Last scanned through: {scanned}

        ## TASK
        Check for new posts since last scan. For each, assess whether it contains
        organizational AI structure content (team restructurings, CAIO appointments,
        AI strategy frameworks, company case studies).

        ## Search Queries — Run 2
        1. site:{sub.get('url', '').replace('https://', '').split('/')[0]} AI 2026
        2. "{sub['name']}" AI organization OR structure OR transformation 2026

        ## Output
        Write a JSON file to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "substacks",
          "sourceId": "{sub['id']}",
          "sourceName": "{sub['name']}",
          "scannedDate": "{today}",
          "newPosts": [
            {{
              "title": "Post title",
              "date": "YYYY-MM-DD",
              "url": "URL",
              "relevance": "HIGH|MEDIUM|LOW",
              "structuralFindings": "Summary if relevant",
              "companiesMentioned": [],
              "deepScanNeeded": false
            }}
          ],
          "summary": "What was found",
          "newSpecimenCandidates": []
        }}
        """)
        targets.append(_make_theme_target(sub['name'], "substacks", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_enterprise_reports(limit: int, today: str) -> list[dict]:
    """Check enterprise AI reports (BCG, Deloitte, etc.) for new releases."""
    reports = [
        ("BCG AI Radar", "BCG AI Radar annual report AI adoption enterprise"),
        ("Deloitte Tech Trends", "Deloitte Technology Trends 2026 AI enterprise"),
        ("PwC AI Predictions", "PwC AI Predictions 2026 enterprise adoption"),
        ("State of AI Report", "State of AI Report 2025 2026 Nathan Benaich"),
        ("Mercer Global Talent", "Mercer Global Talent Trends 2026 AI workforce"),
    ]
    targets = []
    for report_name, query in reports:
        slug = f"report-{get_slug(report_name)}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        prompt = dedent(f"""\
        You are a research agent checking for new releases of "{report_name}".
        COMPLETE THIS IN UNDER 10 MINUTES.

        ## SPEED RULES
        1. ONE WebFetch at a time. Max 4 URLs. Skip: {', '.join(BLOCKED_DOMAINS)}, mckinsey.com

        ## Search Queries — Run 2
        1. {query}
        2. "{report_name}" 2026 latest release

        ## Output
        Write a JSON file to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "enterprise-reports",
          "reportName": "{report_name}",
          "scannedDate": "{today}",
          "latestVersion": "Year/edition found",
          "newFindings": "Key AI-organizational findings if new report exists",
          "companiesMentioned": [],
          "url": "URL of report",
          "summary": "What was found"
        }}
        """)
        targets.append(_make_theme_target(report_name, "enterprise-reports", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_target_specimens(limit: int, enrich: bool = False) -> list[dict]:
    """Delegate to existing load_targets for target-specimens mode.
    Returns targets with pre-built prompts for compatibility with theme runner.
    """
    targets = load_targets(enrich=enrich)
    if limit:
        targets = targets[:limit]
    # These don't get pre-built prompts — they use the existing prompt builders
    return targets


def _targets_stale_refresh(limit: int, today: str) -> list[dict]:
    """Find specimens with oldest lastUpdated dates for enrichment."""
    reg = _load_specimen_registry()
    specimens = reg.get("specimens", [])
    # Sort by lastUpdated ascending (oldest first)
    def get_date(s):
        d = s.get("lastUpdated", "2020-01-01")
        try:
            return date.fromisoformat(d)
        except (ValueError, TypeError):
            return date(2020, 1, 1)
    specimens.sort(key=get_date)
    # Filter to active only (case-insensitive)
    specimens = [s for s in specimens if s.get("status", "active").lower() == "active"]
    targets = []
    for spec in specimens:
        sid = spec["id"]
        slug = f"enrich-{sid}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        # Build an enrichment target
        spec_data = {}
        spec_file = SPECIMENS_DIR / f"{sid}.json"
        if spec_file.exists():
            try:
                spec_data = load_json(spec_file)
            except Exception:
                pass
        company = spec_data.get("name", sid)
        leader = ""
        kp = spec_data.get("keyPeople", [])
        if kp:
            leader = kp[0].get("name", "")
        target = {
            "company": company,
            "leader": leader,
            "leaderTitle": kp[0].get("title", "") if kp else "",
            "sector": spec_data.get("industry", ""),
            "quadrant": "STALE",
            "priority": "medium",
            "mode": "enrich",
        }
        targets.append(target)
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_low_confidence(limit: int, today: str) -> list[dict]:
    """Find specimens with Low confidence classifications."""
    reg = _load_specimen_registry()
    specimens = reg.get("specimens", [])
    low_conf = [s for s in specimens
                if s.get("status", "").lower() == "active"
                and s.get("confidence", "").lower() == "low"]
    targets = []
    for spec in low_conf:
        sid = spec["id"]
        slug = f"enrich-{sid}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        spec_file = SPECIMENS_DIR / f"{sid}.json"
        spec_data = load_json(spec_file) if spec_file.exists() else {}
        company = spec_data.get("name", sid)
        kp = spec_data.get("keyPeople", [])
        target = {
            "company": company,
            "leader": kp[0].get("name", "") if kp else "",
            "leaderTitle": kp[0].get("title", "") if kp else "",
            "sector": spec_data.get("industry", ""),
            "quadrant": "LOWCONF",
            "priority": "high",
            "mode": "enrich",
        }
        targets.append(target)
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_taxonomy_gaps(limit: int, today: str) -> list[dict]:
    """Discovery searches for underrepresented structural models."""
    reg = _load_specimen_registry()
    by_model = reg.get("byModel", {})
    # Initialize all 9 models at 0, then overlay actual counts.
    # Without this, models with zero specimens (M7, M8) are absent from
    # byModel and would never be found as gap candidates.
    model_counts = {str(i): 0 for i in range(1, 10)}
    for m, v in by_model.items():
        count = v if isinstance(v, int) else len(v) if isinstance(v, list) else 0
        model_counts[m] = count
    model_counts = sorted(model_counts.items(), key=lambda x: x[1])
    model_names_map = {
        "1": "Research Lab", "2": "Center of Excellence", "3": "Embedded Teams",
        "4": "Hybrid Hub-and-Spoke", "5": "Product/Venture Lab",
        "6": "Unnamed/Informal", "7": "Tiger Teams", "8": "Skunkworks", "9": "AI-Native",
    }
    targets = []
    for model_num, count in model_counts[:3]:  # Top 3 gaps
        model_name = model_names_map.get(str(model_num), f"M{model_num}")
        slug = f"taxonomy-gap-M{model_num}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        prompt = dedent(f"""\
        You are a research agent searching for companies that use a "{model_name}" (M{model_num}) structure for AI.
        COMPLETE THIS IN UNDER 15 MINUTES.

        ## SPEED RULES
        1. ONE WebFetch at a time. Max 6 URLs. Skip: {', '.join(BLOCKED_DOMAINS)}, mckinsey.com

        ## CONTEXT
        We have only {count} specimens classified as M{model_num} ({model_name}).
        We need more examples to validate the taxonomy.

        {TAXONOMY}

        ## Search Queries — Run 3
        1. company AI "{model_name.lower()}" OR AI {model_name.lower().replace(' ', ' OR ')} structure 2025 2026
        2. company AI team structure {model_name.lower()} example case study
        3. "chief AI officer" OR "AI lab" {model_name.lower()} model

        ## Output
        Write a JSON file to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "taxonomy-gap-coverage",
          "targetModel": "M{model_num}",
          "targetModelName": "{model_name}",
          "currentCount": {count},
          "scannedDate": "{today}",
          "candidates": [
            {{
              "company": "Company Name",
              "evidence": "Why this looks like M{model_num}",
              "confidence": "HIGH|MEDIUM|LOW",
              "sources": ["URL"]
            }}
          ],
          "summary": "What was found"
        }}
        """)
        targets.append(_make_theme_target(f"M{model_num}-gap", "taxonomy-gap-coverage", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_daily_news(limit: int, today: str) -> list[dict]:
    """Headline scan of daily AI news shows."""
    shows = [
        ("AI Daily Brief", "AI Daily Brief podcast latest episode structural"),
        ("The AI Breakdown", "The AI Breakdown podcast latest episode enterprise AI"),
    ]
    targets = []
    for name, query in shows:
        slug = f"news-{get_slug(name)}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        prompt = dedent(f"""\
        You are a research agent scanning recent episodes of "{name}" for AI organizational signals.
        COMPLETE THIS IN UNDER 10 MINUTES. Max 3 URLs.
        Skip: {', '.join(BLOCKED_DOMAINS)}, mckinsey.com

        Search: 1. {query} 2025 2026  2. "{name}" company AI structure OR restructuring

        Write to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "daily-news-headlines",
          "source": "{name}",
          "scannedDate": "{today}",
          "headlines": [{{"title": "...", "date": "...", "relevance": "HIGH|MEDIUM|LOW", "company": "..."}}],
          "summary": "What structural signals were found"
        }}
        """)
        targets.append(_make_theme_target(name, "daily-news-headlines", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_industry_discovery(limit: int, today: str) -> list[dict]:
    """Industry-specific discovery searches rotating weekly."""
    # Rotate industry by week number
    industries = ["healthcare AI", "insurance AI", "manufacturing AI", "automotive AI",
                  "financial services AI", "retail AI", "energy AI", "defense AI"]
    week_num = date.today().isocalendar()[1]
    industry = industries[week_num % len(industries)]
    slug = f"industry-{get_slug(industry)}"
    pending_file = PENDING_DIR / f"{slug}.json"
    if pending_file.exists():
        return []
    prompt = dedent(f"""\
    You are a research agent doing industry-specific discovery for "{industry}" organizational structures.
    COMPLETE THIS IN UNDER 15 MINUTES. Max 6 URLs.
    Skip: {', '.join(BLOCKED_DOMAINS)}, mckinsey.com

    Search: 1. {industry} team structure OR CAIO OR "chief AI officer" 2025 2026
    2. {industry} company AI transformation OR restructuring case study 2025 2026
    3. {industry} AI organization best practices OR lessons learned

    Write to: {str(PENDING_DIR / f'{slug}.json')}
    {{
      "mode": "industry-vertical-searches",
      "industry": "{industry}",
      "scannedDate": "{today}",
      "candidates": [{{"company": "...", "evidence": "...", "confidence": "HIGH|MEDIUM|LOW"}}],
      "summary": "What was found for this industry"
    }}
    """)
    return [_make_theme_target(industry, "industry-vertical-searches", prompt, slug)]


def _targets_staleness_audit(limit: int, today: str) -> list[dict]:
    """Source staleness audit — find and research the most stale sources."""
    stale = _stale_sources(max_age_days=14)
    if not stale:
        log.info("No stale sources found (all scanned within 14 days)")
        return []
    targets = []
    for src in stale:
        slug = f"staleness-{src['id']}"
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            continue
        scanned = src.get("scannedThrough", "unknown")
        prompt = dedent(f"""\
        You are a research agent refreshing the stale source "{src['name']}".
        COMPLETE THIS IN UNDER 15 MINUTES. Max 4 URLs.
        Skip: {', '.join(BLOCKED_DOMAINS)}, mckinsey.com

        ## CONTEXT
        - Source: {src['name']} ({src.get('type', 'unknown')}, Tier {src.get('tier', '?')})
        - URL: {src.get('url', '')}
        - Last scanned through: {scanned}
        - Last scan date: {src.get('lastScanned', 'never')}

        Check for new content since last scan. Extract any AI-organizational findings.

        Search: 1. site:{src.get('url', '').replace('https://', '').split('/')[0]} 2026
        2. "{src['name']}" latest 2026

        Write to: {str(PENDING_DIR / f'{slug}.json')}
        {{
          "mode": "source-staleness-audit",
          "sourceId": "{src['id']}",
          "sourceName": "{src['name']}",
          "scannedDate": "{today}",
          "previousScannedThrough": "{scanned}",
          "newScannedThrough": "Updated description",
          "newContent": [{{"title": "...", "date": "...", "relevance": "HIGH|MEDIUM|LOW"}}],
          "summary": "What changed since last scan"
        }}
        """)
        targets.append(_make_theme_target(src['name'], "source-staleness-audit", prompt, slug))
        if limit and len(targets) >= limit:
            break
    return targets


def _targets_catch_up(limit: int, today: str) -> list[dict]:
    """Adaptive catch-up — process the most behind phase."""
    # Count backlogs across phases
    pending_research = len(list(PENDING_DIR.glob("*.json"))) if PENDING_DIR.exists() else 0

    synth_queue_count = 0
    if SYNTHESIS_QUEUE.exists():
        sq = load_json(SYNTHESIS_QUEUE)
        synth_queue_count = sum(1 for q in sq.get("queue", []) if q.get("status") == "pending")

    stale_count = len(_stale_sources(max_age_days=14))

    log.info(f"Catch-up backlogs: pending_research={pending_research}, "
             f"synthesis_queue={synth_queue_count}, stale_sources={stale_count}")

    # Pick the most behind phase
    backlogs = [
        ("stale-refresh", stale_count),
        ("source-staleness-audit", stale_count),
    ]
    backlogs.sort(key=lambda x: -x[1])  # Highest backlog first

    if stale_count > 0:
        log.info(f"Catch-up: delegating to source-staleness-audit (backlog={stale_count})")
        return build_theme_targets("source-staleness-audit", limit)

    log.info("Catch-up: no significant backlogs found")
    return []


# ─── Agent Runner ─────────────────────────────────────────────────────────────

def get_slug(company: str) -> str:
    """Generate a filesystem-safe slug from company name."""
    slug = company.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
    return "".join(c for c in slug if c.isalnum() or c == "-")


def run_agent(target: dict, prompt: str, skip_permissions: bool = False,
              enrich: bool = False) -> bool:
    """Run a single Claude CLI research agent. Returns True if output file created.

    Uses Popen with process groups so timeout kills the entire process tree
    (claude + any child processes), preventing zombie orphans.
    """
    company = target["company"]
    slug = get_slug(company)
    prefix = "enrich-" if enrich else ""
    log.info(f"▶ Starting agent: {company} ({prefix}{slug})")
    start = time.time()

    cmd = ["claude", "-p", prompt, "--model", "opus"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(PROJECT_ROOT),
            start_new_session=True,
        )

        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            import signal
            try:
                pgid = os.getpgid(proc.pid)
                log.warning(f"  Timeout — killing process group {pgid}")
                os.killpg(pgid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(pgid, signal.SIGKILL)
                    proc.wait(timeout=5)
            except (ProcessLookupError, OSError):
                pass  # process already dead — that's fine
            elapsed = time.time() - start
            log.error(f"✗ {company}: TIMEOUT after {elapsed:.0f}s (process group killed)")
            return False

        elapsed = time.time() - start

        pending_file = PENDING_DIR / f"{prefix}{slug}.json"
        if pending_file.exists():
            try:
                with open(pending_file) as f:
                    data = json.load(f)
                n_quotes = len(data.get("quotes", []))
                n_sources = len(data.get("sources", []))
                if enrich:
                    log.info(
                        f"✓ {company}: enrichment found {n_quotes} quotes, "
                        f"{n_sources} new sources in {elapsed:.0f}s"
                    )
                else:
                    model = data.get("structuralFindings", {}).get("suggestedModel", "?")
                    log.info(
                        f"✓ {company}: M{model}, {n_quotes} quotes, "
                        f"{n_sources} sources in {elapsed:.0f}s"
                    )
                return True
            except json.JSONDecodeError:
                log.error(f"✗ {company}: Output exists but invalid JSON")
                pending_file.unlink()
                return False
        else:
            stdout_preview = stdout[:500] if stdout else "(empty)"
            stderr_preview = stderr[:300] if stderr else "(empty)"
            log.error(
                f"✗ {company}: No output file after {elapsed:.0f}s "
                f"(exit={proc.returncode})\n"
                f"  stdout: {stdout_preview}\n"
                f"  stderr: {stderr_preview}"
            )
            return False

    except Exception as e:
        log.error(f"✗ {company}: Exception: {e}")
        return False

def _run_theme_agent(prompt: str, slug: str, skip_permissions: bool = False) -> bool:
    """Run a theme-based agent with a pre-built prompt. Returns True if output file created."""
    log.info(f"▶ Starting theme agent: {slug}")
    start = time.time()

    cmd = ["claude", "-p", prompt, "--model", "opus"]
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(PROJECT_ROOT),
            start_new_session=True,
        )

        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            import signal
            try:
                pgid = os.getpgid(proc.pid)
                log.warning(f"  Timeout — killing process group {pgid}")
                os.killpg(pgid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(pgid, signal.SIGKILL)
                    proc.wait(timeout=5)
            except (ProcessLookupError, OSError):
                pass
            elapsed = time.time() - start
            log.error(f"✗ {slug}: TIMEOUT after {elapsed:.0f}s")
            return False

        elapsed = time.time() - start
        pending_file = PENDING_DIR / f"{slug}.json"
        if pending_file.exists():
            try:
                with open(pending_file) as f:
                    json.load(f)
                log.info(f"✓ {slug}: completed in {elapsed:.0f}s")
                return True
            except json.JSONDecodeError:
                log.error(f"✗ {slug}: Output exists but invalid JSON")
                pending_file.unlink()
                return False
        else:
            log.error(f"✗ {slug}: No output file after {elapsed:.0f}s (exit={proc.returncode})")
            return False

    except Exception as e:
        log.error(f"✗ {slug}: Exception: {e}")
        return False


# ─── Curation Queue ──────────────────────────────────────────────────────────

def append_to_curation_queue(target: dict, slug: str):
    """Append a completed research target to research/queue.json for /curate pickup."""
    try:
        with open(QUEUE_FILE) as f:
            queue_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        queue_data = {
            "description": "Curation queue — research sessions awaiting Phase 2 processing.",
            "lastUpdated": date.today().isoformat(),
            "queue": [],
        }

    pending_path = f"research/pending/{slug}.json"
    today_str = date.today().isoformat()

    entry = {
        "sessionFile": pending_path,
        "sessionDate": today_str,
        "source": f"overnight-research.py — {target['company']} ({target['sector']})",
        "organizationsFound": [slug],
        "status": "pending",
        "curatedIn": None,
    }

    queue_data["queue"].append(entry)
    queue_data["lastUpdated"] = today_str

    save_json(QUEUE_FILE, queue_data)

    log.info(f"  → Added {target['company']} to research/queue.json")


# ─── Target Queue ─────────────────────────────────────────────────────────────

def load_targets(
    quadrant: str | None = None,
    priority: str | None = None,
    company: str | None = None,
    enrich: bool = False,
) -> list[dict]:
    """Load and filter targets from target-specimens.json.

    When enrich=True, ONLY include targets that already have specimen files
    (the opposite of normal mode). Skip if an enrich-{slug}.json pending file
    already exists.
    """
    with open(TARGET_LIST) as f:
        data = json.load(f)

    targets = data["targets"]

    filtered = []
    for t in targets:
        slug = get_slug(t["company"])
        pending_file = PENDING_DIR / f"{slug}.json"
        enrich_file = PENDING_DIR / f"enrich-{slug}.json"
        specimen_file = SPECIMENS_DIR / f"{slug}.json"
        is_enrich_target = t.get("mode") == "enrich"

        if enrich:
            # Enrichment mode: only targets tagged mode=enrich that have specimens
            if not is_enrich_target:
                continue
            if not specimen_file.exists():
                log.info(f"  Skip {t['company']}: no specimen to enrich")
                continue
            if enrich_file.exists():
                log.info(f"  Skip {t['company']}: enrich file already in pending/")
                continue
            filtered.append(t)
        else:
            # Normal mode: skip enrichment targets and already-scanned
            if is_enrich_target:
                continue
            if pending_file.exists():
                log.info(f"  Skip {t['company']}: already in pending/")
                continue
            if specimen_file.exists():
                log.info(f"  Skip {t['company']}: specimen already exists")
                continue
            filtered.append(t)

    targets = filtered

    # Apply filters
    if company:
        targets = [t for t in targets if company.lower() in t["company"].lower()]
    if quadrant:
        targets = [t for t in targets if t["quadrant"] == quadrant]
    if priority:
        targets = [t for t in targets if t["priority"] == priority]

    # Sort by priority (high > medium > low), then by quadrant
    priority_order = {"high": 0, "medium": 1, "low": 2}
    targets.sort(key=lambda t: (priority_order.get(t["priority"], 9), t["quadrant"], t["company"]))

    return targets

# ─── Session Log ──────────────────────────────────────────────────────────────

def write_session_log(results: list[dict], start_time: datetime):
    """Write a rich markdown session log with per-company insights from pending files."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()
    elapsed = datetime.now() - start_time

    rows = []
    for r in results:
        status = "✓" if r["success"] else "✗"
        model = r.get("model", "?")
        quotes = r.get("quotes", 0)
        rows.append(
            f"| {r['company']:30s} | {r['quadrant']} | {status} | M{model} | "
            f"{quotes} quotes | {r.get('elapsed', 0):.0f}s |"
        )

    succeeded_results = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]

    # ── Extract rich content from pending files ─────────────────────
    specimen_sections = []
    all_open_questions = []
    model_names = {
        1: "Research Lab", 2: "Center of Excellence", 3: "Embedded Teams",
        4: "Hybrid/Hub-and-Spoke", 5: "Product/Venture Lab",
        6: "Unnamed/Informal", 7: "Tiger Teams", 8: "Skunkworks", 9: "AI-Native",
    }

    for r in succeeded_results:
        slug = get_slug(r["company"])
        pending_file = PENDING_DIR / f"{slug}.json"
        if not pending_file.exists():
            continue
        try:
            with open(pending_file) as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            continue

        findings = data.get("structuralFindings", {})
        model_num = findings.get("suggestedModel", "?")
        model_name = model_names.get(model_num, "Unknown") if isinstance(model_num, int) else "?"
        orientation = findings.get("suggestedOrientation", "?")
        confidence = findings.get("confidence", "?")
        summary = data.get("summary", "").strip()
        rationale = findings.get("rationale", "").strip()
        ai_structure = findings.get("aiTeamStructure", "").strip()
        open_qs = data.get("openQuestions", [])
        key_people = findings.get("keyPeople", [])
        n_sources = len(data.get("sources", []))
        n_quotes = len(data.get("quotes", []))

        botanist_notes = data.get("botanistNotes", [])
        best_quote = data.get("bestQuote", {})
        all_quotes = data.get("quotes", [])

        # Build per-company section
        people_str = ", ".join(
            f"{p.get('name', '?')} ({p.get('title', '?')})"
            for p in key_people[:5]
        ) if key_people else "(none identified)"

        section = f"### {r['company']} — M{model_num} {model_name} | {orientation} | {confidence}\n\n"
        if summary:
            section += f"**Summary:** {summary}\n\n"
        if rationale:
            section += f"**Classification rationale:** {rationale}\n\n"
        if ai_structure:
            # Truncate very long descriptions
            if len(ai_structure) > 500:
                ai_structure = ai_structure[:500] + "..."
            section += f"**AI team structure:** {ai_structure}\n\n"
        section += f"**Key people:** {people_str}\n\n"
        section += f"**Data:** {n_quotes} quotes, {n_sources} sources\n\n"

        # Best quote (most revealing)
        if best_quote and best_quote.get("text"):
            quote_text = best_quote["text"][:150]
            if len(best_quote.get("text", "")) > 150:
                quote_text += "..."
            section += f"**Most revealing quote:** \"{quote_text}\"\n"
            section += f"— {best_quote.get('speaker', '?')}\n"
            if best_quote.get("why"):
                section += f"*Why interesting:* {best_quote['why']}\n"
            section += "\n"
        elif all_quotes:
            # Fall back to first quote if no bestQuote field
            q = all_quotes[0]
            quote_text = q.get("text", "")[:150]
            if len(q.get("text", "")) > 150:
                quote_text += "..."
            section += f"**Notable quote:** \"{quote_text}\" — {q.get('speaker', '?')}\n\n"

        # Botanist's notes
        if botanist_notes:
            section += "**Botanist's notes:**\n"
            for note in botanist_notes:
                if isinstance(note, str) and note.strip():
                    section += f"- {note}\n"
            section += "\n"

        if open_qs:
            section += "**Open questions:**\n"
            for q in open_qs[:5]:
                section += f"- {q}\n"
            section += "\n"

        specimen_sections.append(section)

        for q in open_qs:
            all_open_questions.append(f"- **{r['company']}**: {q}")

    # ── Model distribution ──────────────────────────────────────────
    from collections import Counter
    model_counts = Counter(str(r.get("model", "?")) for r in succeeded_results)
    model_rows = []
    for m, c in sorted(model_counts.items()):
        name = model_names.get(int(m), "Unknown") if m.isdigit() else "Unknown"
        model_rows.append(f"| M{m} {name:30s} | {c:5d} |")

    # ── Sector distribution ─────────────────────────────────────────
    sector_counts = Counter(r.get("quadrant", "?") for r in succeeded_results)
    sector_rows = [f"| {q} | {c} |" for q, c in sorted(sector_counts.items())]

    content = dedent(f"""\
    # Overnight Research Run — {today_str}

    **Started:** {start_time.strftime('%Y-%m-%d %H:%M')}
    **Duration:** {elapsed.total_seconds() / 60:.0f} minutes
    **Targets scanned:** {len(results)}
    **Succeeded:** {len(succeeded_results)}
    **Failed:** {len(failed_results)}
    **Method:** `scripts/overnight-research.py` via `claude -p --model opus`

    ## Results

    | Company | Q | Status | Model | Quotes | Time |
    |---------|---|--------|-------|--------|------|
    {chr(10).join(rows)}

    ## Model Distribution

    | Model | Count |
    |-------|-------|
    {chr(10).join(model_rows) if model_rows else "| (none) | |"}

    ## Quadrant Distribution

    | Quadrant | Count |
    |----------|-------|
    {chr(10).join(sector_rows) if sector_rows else "| (none) | |"}

    ## Per-Company Findings

    {chr(10).join(specimen_sections) if specimen_sections else "(no findings to report)"}

    ## Open Questions Across All Specimens

    {chr(10).join(all_open_questions[:50]) if all_open_questions else "- (none)"}

    ## Failed Targets

    {chr(10).join(f"- {r['company']}" for r in failed_results) if failed_results else "- (none)"}

    ## Next Steps

    - Run `overnight-curate.py` to create specimen files from research findings
    - Run `overnight-purpose-claims.py` for newly created specimens
    - Review open questions above for research gaps
    """)

    log_path = SESSION_DIR / f"{today_str}-overnight-research.md"
    counter = 1
    while log_path.exists():
        counter += 1
        log_path = SESSION_DIR / f"{today_str}-overnight-research-{counter}.md"

    with open(log_path, "w") as f:
        f.write(content)
    log.info(f"Session log: {log_path}")

# ─── Main ─────────────────────────────────────────────────────────────────────

def _run_phase(queue: list[dict], skip_permissions: bool, enrich: bool = False) -> list[dict]:
    """Run a list of targets through agents. Returns list of result dicts."""
    results = []
    failed = []

    for i, target in enumerate(queue, 1):
        label = "ENRICH" if enrich else target["quadrant"]
        log.info(f"\n--- [{i}/{len(queue)}] {target['company']} ({label}) ---")

        prompt = build_enrich_prompt(target) if enrich else build_research_prompt(target)
        agent_start = time.time()
        success = run_agent(target, prompt, skip_permissions, enrich=enrich)
        agent_elapsed = time.time() - agent_start

        slug = get_slug(target["company"])
        prefix = "enrich-" if enrich else ""

        if success:
            pending_file = PENDING_DIR / f"{prefix}{slug}.json"
            try:
                with open(pending_file) as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                log.error(f"Cannot read pending file {pending_file}: {e}")
                results.append({
                    "company": target["company"],
                    "quadrant": target.get("quadrant", "?"),
                    "success": False,
                    "model": "?",
                    "quotes": 0,
                    "elapsed": agent_elapsed,
                    "mode": "enrich" if enrich else "new",
                })
                failed.append(target)
                continue
            result = {
                "company": target["company"],
                "quadrant": target.get("quadrant", "?"),
                "success": True,
                "quotes": len(data.get("quotes", [])),
                "elapsed": agent_elapsed,
                "mode": "enrich" if enrich else "new",
            }
            if enrich:
                result["model"] = "enrich"
            else:
                result["model"] = data.get("structuralFindings", {}).get("suggestedModel", "?")
            append_to_curation_queue(target, slug)
            results.append(result)
        else:
            results.append({
                "company": target["company"],
                "quadrant": target.get("quadrant", "?"),
                "success": False,
                "model": "?",
                "quotes": 0,
                "elapsed": agent_elapsed,
                "mode": "enrich" if enrich else "new",
            })
            failed.append(target)

        if i < len(queue):
            time.sleep(PAUSE_BETWEEN)

    # ─── Retry Failed ────────────────────────────────────────────────
    if failed and MAX_RETRIES > 0:
        log.info(f"\n--- RETRYING {len(failed)} failed targets ---")
        for target in failed:
            prompt = build_enrich_prompt(target) if enrich else build_research_prompt(target)
            agent_start = time.time()
            success = run_agent(target, prompt, skip_permissions, enrich=enrich)
            agent_elapsed = time.time() - agent_start

            if success:
                slug = get_slug(target["company"])
                prefix = "enrich-" if enrich else ""
                pending_file = PENDING_DIR / f"{prefix}{slug}.json"
                try:
                    with open(pending_file) as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    log.error(f"Cannot read pending file on retry {pending_file}: {e}")
                    continue
                for r in results:
                    if r["company"] == target["company"]:
                        r["success"] = True
                        r["quotes"] = len(data.get("quotes", []))
                        r["elapsed"] += agent_elapsed
                        if enrich:
                            r["model"] = "enrich"
                        else:
                            r["model"] = data.get("structuralFindings", {}).get("suggestedModel", "?")
                        break
                append_to_curation_queue(target, slug)

            time.sleep(PAUSE_BETWEEN)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Overnight research scanning for new specimen targets"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show queue and exit")
    parser.add_argument("--limit", type=int, default=0, help="Max targets to scan")
    parser.add_argument("--company", type=str, help="Scan one specific company")
    parser.add_argument("--quadrant", type=str, choices=["Q1", "Q2", "Q3", "Q4"],
                        help="Scan one quadrant only")
    parser.add_argument("--priority", type=str, choices=["high", "medium", "low"],
                        help="Filter by priority level")
    parser.add_argument("--enrich", action="store_true",
                        help="Enrichment mode: rescan existing specimens for deeper data")
    parser.add_argument("--all-phases", action="store_true",
                        help="Run Phase A (new), then Phase B (enrich), sequentially")
    parser.add_argument("--schedule-theme", type=str, choices=SCHEDULE_THEMES,
                        help="Run a themed research batch from pipeline schedule")
    parser.add_argument("--theme-config", type=str, default=None,
                        help="JSON string of theme config (passed by orchestrator)")
    parser.add_argument("--skip-permissions", action="store_true",
                        help="Add --dangerously-skip-permissions")
    args = parser.parse_args()

    log.info("=" * 60)
    if args.schedule_theme:
        mode_label = f"THEME: {args.schedule_theme}"
    elif args.enrich:
        mode_label = "ENRICHMENT"
    elif args.all_phases:
        mode_label = "ALL-PHASES"
    else:
        mode_label = "NEW TARGETS"
    log.info(f"OVERNIGHT RESEARCH RUN — {mode_label}")
    log.info("=" * 60)

    # ─── Schedule-theme shortcut ──────────────────────────────────────
    if args.schedule_theme:
        theme_config = None
        if args.theme_config:
            try:
                theme_config = json.loads(args.theme_config)
            except json.JSONDecodeError:
                log.warning(f"Could not parse --theme-config: {args.theme_config}")

        effective_limit = args.limit if args.limit > 0 else 8  # default limit for themes
        targets = build_theme_targets(args.schedule_theme, effective_limit, theme_config)

        if not targets:
            log.info(f"No targets for theme '{args.schedule_theme}' — nothing to do")
            return

        if args.dry_run:
            log.info(f"\n--- THEME: {args.schedule_theme} ({len(targets)} targets) ---")
            for i, t in enumerate(targets, 1):
                mode = t.get('mode', t.get('quadrant', '?'))
                log.info(f"  {i:2d}. {t['company']:40s} | {mode}")
            log.info(f"\nTotal: {len(targets)} targets")
            log.info("Run without --dry-run to execute.")
            return

        # Check if these are target-specimens mode (use existing prompt builders)
        if args.schedule_theme in ("target-specimens", "target-specimens-enrich",
                                    "stale-refresh", "low-confidence"):
            # These return standard target dicts — use existing _run_phase
            enrich = args.schedule_theme in ("target-specimens-enrich",
                                              "stale-refresh", "low-confidence")
            failures = preflight_check(
                required_files=[TARGET_LIST] if args.schedule_theme.startswith("target") else [],
                check_claude_cli=True,
                required_dirs=[PENDING_DIR, SESSION_DIR],
            )
            if failures:
                for f in failures:
                    log.error(f"PREFLIGHT FAIL: {f}")
                sys.exit(1)
            lock_path = acquire_lock("overnight-research")
            try:
                start_time = datetime.now()
                results = _run_phase(targets, args.skip_permissions, enrich=enrich)
                write_session_log(results, start_time)
                succeeded = [r for r in results if r["success"]]
                if succeeded:
                    entries = [f"Theme {args.schedule_theme}: {len(succeeded)}/{len(results)} succeeded"]
                    write_changelog("overnight-research.py", entries)
            finally:
                release_lock(lock_path)
            return

        # Theme targets with pre-built prompts — run them through the agent runner
        failures = preflight_check(
            required_files=[],
            check_claude_cli=True,
            required_dirs=[PENDING_DIR, SESSION_DIR],
        )
        if failures:
            for f in failures:
                log.error(f"PREFLIGHT FAIL: {f}")
            sys.exit(1)

        lock_path = acquire_lock("overnight-research")
        try:
            start_time = datetime.now()
            results = []
            failed = []
            for i, target in enumerate(targets, 1):
                log.info(f"\n--- [{i}/{len(targets)}] {target['company']} ({target['mode']}) ---")
                agent_start = time.time()
                slug = target.get("_slug", get_slug(target["company"]))
                prompt = target["prompt"]
                success = _run_theme_agent(prompt, slug, args.skip_permissions)
                elapsed = time.time() - agent_start
                results.append({
                    "company": target["company"],
                    "quadrant": target.get("quadrant", "THEME"),
                    "success": success,
                    "model": target["mode"],
                    "quotes": 0,
                    "elapsed": elapsed,
                    "mode": target["mode"],
                })
                if not success:
                    failed.append(target)
                if i < len(targets):
                    time.sleep(PAUSE_BETWEEN)

            # Retry failed
            if failed and MAX_RETRIES > 0:
                log.info(f"\n--- RETRYING {len(failed)} failed ---")
                for target in failed:
                    slug = target.get("_slug", get_slug(target["company"]))
                    success = _run_theme_agent(target["prompt"], slug, args.skip_permissions)
                    if success:
                        for r in results:
                            if r["company"] == target["company"]:
                                r["success"] = True
                                break
                    time.sleep(PAUSE_BETWEEN)

            # Summary
            succeeded = sum(1 for r in results if r["success"])
            log.info(f"\nTheme '{args.schedule_theme}': {succeeded}/{len(results)} succeeded")

            if succeeded:
                entries = [f"Theme {args.schedule_theme}: {succeeded}/{len(results)} succeeded"]
                write_changelog("overnight-research.py", entries)
        finally:
            release_lock(lock_path)
        return

    # ─── Preflight Checks ─────────────────────────────────────────────
    failures = preflight_check(
        required_files=[TARGET_LIST],
        check_claude_cli=not args.dry_run,
        required_dirs=[PENDING_DIR, SESSION_DIR],
    )
    if failures:
        for f in failures:
            log.error(f"PREFLIGHT FAIL: {f}")
        log.error("Fix the above before running. Aborting.")
        sys.exit(1)

    # ─── Lock ─────────────────────────────────────────────────────────
    lock_path = None
    if not args.dry_run:
        try:
            lock_path = acquire_lock("overnight-research")
            log.info("Lock acquired")
        except RuntimeError as e:
            log.error(f"LOCK FAIL: {e}")
            sys.exit(1)

    try:  # ← ensures lock is released even on unexpected exceptions

        # ─── Build queues ────────────────────────────────────────────────
        if args.all_phases:
            # Phase A: new targets, Phase B: enrichment targets
            queue_new = load_targets(
                quadrant=args.quadrant, priority=args.priority,
                company=args.company, enrich=False,
            )
            queue_enrich = load_targets(
                quadrant=args.quadrant, priority=args.priority,
                company=args.company, enrich=True,
            )
            log.info(f"Phase A (new): {len(queue_new)} targets")
            log.info(f"Phase B (enrich): {len(queue_enrich)} targets")
            total = len(queue_new) + len(queue_enrich)
            if args.limit > 0 and total > args.limit:
                # Prioritize new targets, then fill remaining with enrichment
                if len(queue_new) >= args.limit:
                    queue_new = queue_new[:args.limit]
                    queue_enrich = []
                else:
                    remaining = args.limit - len(queue_new)
                    queue_enrich = queue_enrich[:remaining]
                log.info(f"Limited to {args.limit} total: {len(queue_new)} new + {len(queue_enrich)} enrich")
        else:
            queue_new = load_targets(
                quadrant=args.quadrant, priority=args.priority,
                company=args.company, enrich=args.enrich,
            )
            queue_enrich = []
            if args.enrich:
                queue_enrich = queue_new
                queue_new = []
            if args.limit > 0:
                if queue_new:
                    queue_new = queue_new[:args.limit]
                if queue_enrich:
                    queue_enrich = queue_enrich[:args.limit]
            log.info(f"Queue: {len(queue_new) + len(queue_enrich)} targets")

        # ─── Dry run ─────────────────────────────────────────────────────
        if args.dry_run:
            if queue_new:
                log.info("\n--- Phase A: NEW TARGETS ---")
                for i, t in enumerate(queue_new, 1):
                    conf = " ★" if t.get("conference") else ""
                    pub = "PUB" if t.get("public", True) else "PVT"
                    log.info(
                        f"  {i:2d}. [{t['priority']:6s}] {t['company']:30s} | "
                        f"{t['quadrant']} | {t['sector']:25s} | {t['leader']:25s} | {pub}{conf}"
                    )
            if queue_enrich:
                log.info("\n--- Phase B: ENRICHMENT ---")
                offset = len(queue_new)
                for i, t in enumerate(queue_enrich, 1):
                    slug = get_slug(t["company"])
                    specimen_file = SPECIMENS_DIR / f"{slug}.json"
                    size = specimen_file.stat().st_size if specimen_file.exists() else 0
                    log.info(
                        f"  {offset + i:2d}. [{t['priority']:6s}] {t['company']:30s} | "
                        f"{t['quadrant']} | {t['sector']:25s} | {size:,d}B"
                    )
            total = len(queue_new) + len(queue_enrich)
            log.info(f"\nTotal: {total} targets (~{total * 20} min estimated)")
            log.info("Run without --dry-run to execute.")
            return

        # ─── Execute ─────────────────────────────────────────────────────
        start_time = datetime.now()
        all_results = []

        if queue_new:
            log.info(f"\n{'='*60}")
            log.info(f"PHASE A: NEW TARGETS ({len(queue_new)})")
            log.info(f"{'='*60}")
            results_a = _run_phase(queue_new, args.skip_permissions, enrich=False)
            all_results.extend(results_a)
            succeeded_a = sum(1 for r in results_a if r["success"])
            log.info(f"\nPhase A complete: {succeeded_a}/{len(results_a)} succeeded")

        if queue_enrich:
            log.info(f"\n{'='*60}")
            log.info(f"PHASE B: ENRICHMENT ({len(queue_enrich)})")
            log.info(f"{'='*60}")
            results_b = _run_phase(queue_enrich, args.skip_permissions, enrich=True)
            all_results.extend(results_b)
            succeeded_b = sum(1 for r in results_b if r["success"])
            log.info(f"\nPhase B complete: {succeeded_b}/{len(results_b)} succeeded")

        # ─── Summary ──────────────────────────────────────────────────────
        elapsed_total = datetime.now() - start_time
        succeeded = [r for r in all_results if r["success"]]
        failed_final = [r for r in all_results if not r["success"]]

        log.info("\n" + "=" * 60)
        log.info("RUN COMPLETE")
        log.info("=" * 60)
        log.info(f"Duration: {elapsed_total.total_seconds() / 60:.0f} minutes")
        log.info(f"Targets scanned: {len(all_results)}")
        log.info(f"Succeeded: {len(succeeded)} (new: {sum(1 for r in succeeded if r['mode']=='new')}, enrich: {sum(1 for r in succeeded if r['mode']=='enrich')})")
        log.info(f"Failed: {len(failed_final)}")

        new_succeeded = [r for r in succeeded if r["mode"] == "new"]
        if new_succeeded:
            from collections import Counter
            models = Counter(r["model"] for r in new_succeeded)
            log.info(f"\nModel distribution (new targets):")
            for m, c in models.most_common():
                log.info(f"  M{m}: {c}")

        if failed_final:
            log.info(f"\nFailed: {[r['company'] for r in failed_final]}")

        write_session_log(all_results, start_time)

        # Audit log
        if succeeded:
            new_names = [r["company"] for r in succeeded if r["mode"] == "new"]
            enrich_names = [r["company"] for r in succeeded if r["mode"] == "enrich"]
            entries = []
            if new_names:
                entries.append(f"New scans ({len(new_names)}): {', '.join(new_names)}")
            if enrich_names:
                entries.append(f"Enrichment scans ({len(enrich_names)}): {', '.join(enrich_names)}")
            entries.append(f"Total quotes found: {sum(r.get('quotes', 0) for r in succeeded)}")
            write_changelog("overnight-research.py", entries)

        log.info("\nPending files in research/pending/ — run /curate to create specimens.")

    finally:
        # ─── Release Lock ─────────────────────────────────────────────────
        if lock_path:
            release_lock(lock_path)
            log.info("Lock released")


if __name__ == "__main__":
    main()
