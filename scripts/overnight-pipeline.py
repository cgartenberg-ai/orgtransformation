#!/usr/bin/env python3
"""
overnight-pipeline.py
=====================
Full nightly pipeline orchestrator. Chains:
  Phase 1: Research (themed — runs 2-3 batches from schedule)
  Phase 2: Curate (processes all pending research)
  Phase 3: Purpose Claims (enriches specimens)
  Phase 4: Autonomous Synthesis (scores and commits)
  Phase 5: Validation (validate-workflow.js)
  Phase 6: Morning Briefing (compiles results)

Reads schedule from scripts/pipeline-schedule.json. Time-budget-aware:
tracks elapsed time, skips optional batches if running long.

Usage:
    python3 scripts/overnight-pipeline.py                    # Run tonight's schedule
    python3 scripts/overnight-pipeline.py --dry-run          # Show what would run
    python3 scripts/overnight-pipeline.py --day monday       # Force a specific day
    python3 scripts/overnight-pipeline.py --phase 1          # Run one phase only
    python3 scripts/overnight-pipeline.py --skip-permissions # Unattended mode

Run from project root: orgtransformation/
"""

import argparse
import json
import logging
import re
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

# ─── Shared Library ─────────────────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).parent))
from lib.utils import (
    load_json, setup_logging, write_changelog, PROJECT_ROOT,
)

# ─── Configuration ───────────────────────────────────────────────────────────

SCHEDULE_FILE = PROJECT_ROOT / "scripts" / "pipeline-schedule.json"
REPORTS_DIR = PROJECT_ROOT / "pipeline-reports"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# ─── Logging ─────────────────────────────────────────────────────────────────

log = setup_logging("overnight-pipeline")


# ─── Time Budget ─────────────────────────────────────────────────────────────

class TimeBudget:
    """Track elapsed time against a total budget."""

    def __init__(self, total_minutes: int = 720):
        self.start = datetime.now()
        self.total = timedelta(minutes=total_minutes)
        self.phase_starts: dict[str, datetime] = {}
        self.phase_elapsed: dict[str, timedelta] = {}

    def elapsed(self) -> timedelta:
        return datetime.now() - self.start

    def remaining(self) -> timedelta:
        return self.total - self.elapsed()

    def remaining_minutes(self) -> float:
        return self.remaining().total_seconds() / 60

    def is_over_budget(self) -> bool:
        return self.elapsed() > self.total

    def start_phase(self, name: str):
        self.phase_starts[name] = datetime.now()
        log.info(f"  [{self.elapsed_str()}] Starting phase: {name}")

    def end_phase(self, name: str):
        if name in self.phase_starts:
            self.phase_elapsed[name] = datetime.now() - self.phase_starts[name]
            log.info(f"  [{self.elapsed_str()}] Phase {name} done: "
                     f"{self.phase_elapsed[name].total_seconds()/60:.0f}m")

    def elapsed_str(self) -> str:
        e = self.elapsed()
        h, remainder = divmod(int(e.total_seconds()), 3600)
        m = remainder // 60
        return f"{h}h{m:02d}m"

    def should_skip(self, phase_budget_minutes: int) -> bool:
        """Check if we should skip a phase because we're running low on time."""
        return self.remaining_minutes() < phase_budget_minutes + 30  # 30 min buffer

    def summary(self) -> str:
        lines = [f"Total elapsed: {self.elapsed_str()}"]
        for name, dur in self.phase_elapsed.items():
            lines.append(f"  {name}: {dur.total_seconds()/60:.0f}m")
        lines.append(f"  Remaining: {self.remaining_minutes():.0f}m")
        return "\n".join(lines)


# ─── Phase Runners ───────────────────────────────────────────────────────────

def _parse_count(output: str, pattern: str) -> int:
    """Extract a numeric count from subprocess output using a regex pattern."""
    m = re.search(pattern, output)
    return int(m.group(1)) if m else 0


def run_subprocess(cmd: list[str], label: str, timeout_seconds: int = 3600,
                   dry_run: bool = False) -> tuple[bool, str]:
    """Run a subprocess with timeout. Returns (success, output_summary)."""
    if dry_run:
        log.info(f"  [DRY RUN] Would run: {' '.join(cmd)}")
        return True, "[dry run]"

    log.info(f"  Running: {' '.join(cmd[:6])}...")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_seconds,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout[-1000:] if result.stdout else ""
        if result.returncode != 0:
            log.error(f"  {label} failed (exit {result.returncode})")
            if result.stderr:
                log.error(f"  stderr: {result.stderr[-500:]}")
            return False, f"Exit {result.returncode}: {result.stderr[-200:]}"
        return True, output
    except subprocess.TimeoutExpired:
        log.error(f"  {label} TIMEOUT ({timeout_seconds}s)")
        return False, "TIMEOUT"
    except Exception as e:
        log.error(f"  {label} exception: {e}")
        return False, str(e)


def phase1_research(day_config: dict, budget: TimeBudget, skip_permissions: bool,
                    dry_run: bool) -> dict:
    """Run themed research batches."""
    budget.start_phase("research")
    themes = day_config.get("themes", [])
    results = {"batches": [], "total_targets": 0, "succeeded": 0, "skipped": []}

    budget_limit = 300  # 5 hours default
    defaults = load_json(SCHEDULE_FILE).get("defaults", {})
    budget_limit = defaults.get("phaseBudgetMinutes", {}).get("research", 300)

    for i, theme in enumerate(themes):
        name = theme["name"]
        mode = theme["mode"]
        limit = theme.get("limit", 8)
        theme_config_json = json.dumps(theme)

        if budget.should_skip(budget_limit // (len(themes) - i) if i < len(themes) - 1 else 30):
            log.warning(f"  Skipping theme '{name}' — running low on time ({budget.remaining_minutes():.0f}m left)")
            results["skipped"].append(name)
            continue

        cmd = [
            "python3", str(SCRIPTS_DIR / "overnight-research.py"),
            "--schedule-theme", mode,
            "--limit", str(limit),
            "--theme-config", theme_config_json,
        ]
        if skip_permissions:
            cmd.append("--skip-permissions")

        success, output = run_subprocess(
            cmd, f"Research batch '{name}'",
            timeout_seconds=budget_limit * 60 // max(len(themes), 1),
            dry_run=dry_run,
        )

        results["batches"].append({
            "name": name, "mode": mode, "success": success,
            "limit": limit,
        })
        if success:
            results["succeeded"] += 1

    budget.end_phase("research")
    return results


def phase1b_split(budget: TimeBudget, dry_run: bool) -> dict:
    """Split multi-company research files into single-company files for curation."""
    budget.start_phase("split")
    cmd = ["python3", str(SCRIPTS_DIR / "split-pending-research.py")]
    if dry_run:
        cmd.append("--dry-run")
    success, output = run_subprocess(cmd, "Split pending research",
                                     timeout_seconds=120, dry_run=False)
    budget.end_phase("split")

    # Parse split count from output
    items = 0
    for line in output.split("\n"):
        if "single-company files created" in line:
            try:
                items = int(line.split(":")[1].strip().split()[0])
            except (ValueError, IndexError):
                pass

    return {"success": success, "items_processed": items}


def phase2_curate(day_config: dict, budget: TimeBudget, skip_permissions: bool,
                  dry_run: bool) -> dict:
    """Run curation on pending research."""
    budget.start_phase("curate")
    curate_config = day_config.get("curate", {"limit": 16})
    limit = curate_config.get("limit", 16)

    defaults = load_json(SCHEDULE_FILE).get("defaults", {})
    budget_minutes = defaults.get("phaseBudgetMinutes", {}).get("curate", 120)

    if budget.should_skip(budget_minutes):
        log.warning(f"  Skipping curate — low time ({budget.remaining_minutes():.0f}m left)")
        budget.end_phase("curate")
        return {"skipped": True}

    cmd = [
        "python3", str(SCRIPTS_DIR / "overnight-curate.py"),
        "--limit", str(limit),
    ]
    if skip_permissions:
        cmd.append("--skip-permissions")

    success, output = run_subprocess(
        cmd, "Curate",
        timeout_seconds=budget_minutes * 60,
        dry_run=dry_run,
    )

    budget.end_phase("curate")
    curated = _parse_count(output, r"Specimens curated:\s*(\d+)")
    failed = _parse_count(output, r"Failed:\s*(\d+)")
    return {"success": success, "limit": limit, "items_processed": curated, "failed": failed}


def phase3_purpose_claims(day_config: dict, budget: TimeBudget, skip_permissions: bool,
                          dry_run: bool) -> dict:
    """Run purpose claims collection."""
    budget.start_phase("purpose-claims")
    pc_config = day_config.get("purposeClaims", {"limit": 8})
    limit = pc_config.get("limit", 8)

    defaults = load_json(SCHEDULE_FILE).get("defaults", {})
    budget_minutes = defaults.get("phaseBudgetMinutes", {}).get("purposeClaims", 150)

    if budget.should_skip(budget_minutes):
        log.warning(f"  Skipping purpose claims — low time ({budget.remaining_minutes():.0f}m left)")
        budget.end_phase("purpose-claims")
        return {"skipped": True}

    cmd = [
        "python3", str(SCRIPTS_DIR / "overnight-purpose-claims.py"),
        "--limit", str(limit),
        "--rescan-stale",  # Always include — script prioritizes unscanned first
    ]
    if skip_permissions:
        cmd.append("--skip-permissions")

    success, output = run_subprocess(
        cmd, "Purpose Claims",
        timeout_seconds=budget_minutes * 60,
        dry_run=dry_run,
    )

    budget.end_phase("purpose-claims")
    scanned = _parse_count(output, r"Succeeded:\s*(\d+)")
    claims_added = _parse_count(output, r"Total claims added:\s*(\d+)")
    return {"success": success, "limit": limit, "items_processed": scanned, "claims_added": claims_added}


def phase4_synthesis(day_config: dict, budget: TimeBudget, skip_permissions: bool,
                     dry_run: bool) -> dict:
    """Run autonomous synthesis."""
    budget.start_phase("synthesis")
    synth_config = day_config.get("synthesis", {"limit": 16})
    limit = synth_config.get("limit", 16)

    defaults = load_json(SCHEDULE_FILE).get("defaults", {})
    budget_minutes = defaults.get("phaseBudgetMinutes", {}).get("synthesis", 60)

    if budget.should_skip(budget_minutes):
        log.warning(f"  Skipping synthesis — low time ({budget.remaining_minutes():.0f}m left)")
        budget.end_phase("synthesis")
        return {"skipped": True}

    cmd = [
        "python3", str(SCRIPTS_DIR / "overnight-synthesis.py"),
        "--limit", str(limit),
    ]
    if skip_permissions:
        cmd.append("--skip-permissions")

    success, output = run_subprocess(
        cmd, "Synthesis",
        timeout_seconds=budget_minutes * 60,
        dry_run=dry_run,
    )

    budget.end_phase("synthesis")
    synthesized = _parse_count(output, r"Processed:\s*(\d+)")
    return {"success": success, "limit": limit, "items_processed": synthesized}


def phase5_validation(budget: TimeBudget, dry_run: bool) -> dict:
    """Run validate-workflow.js."""
    budget.start_phase("validation")
    cmd = ["node", str(SCRIPTS_DIR / "validate-workflow.js")]
    success, output = run_subprocess(cmd, "Validation", timeout_seconds=120, dry_run=dry_run)
    budget.end_phase("validation")

    # Parse error count from output
    errors = 0
    warnings = 0
    for line in output.split("\n"):
        if "error(s)" in line:
            try:
                errors = int(line.split()[0])
            except (ValueError, IndexError):
                pass
        if "warning(s)" in line:
            try:
                warnings = int(line.split()[0].replace(",", ""))
            except (ValueError, IndexError):
                pass

    return {"success": success, "errors": errors, "warnings": warnings}


# ─── Morning Briefing ────────────────────────────────────────────────────────

def write_morning_briefing(day: str, budget: TimeBudget, phase_results: dict,
                           dry_run: bool = False):
    """Generate the morning briefing markdown."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    briefing_path = REPORTS_DIR / f"{today}-morning-briefing.md"

    research = phase_results.get("research", {})
    split = phase_results.get("split", {})
    curate = phase_results.get("curate", {})
    claims = phase_results.get("purpose_claims", {})
    synthesis = phase_results.get("synthesis", {})
    validation = phase_results.get("validation", {})

    content = f"""# Morning Briefing — {today} ({day.capitalize()})

**Pipeline started:** {budget.start.strftime('%Y-%m-%d %H:%M')}
**Duration:** {budget.elapsed_str()}
**Mode:** {'DRY RUN' if dry_run else 'LIVE'}

## Phase Summary

| Phase | Status | Details |
|-------|--------|---------|
| Research | {_status_icon(research)} | {len(research.get('batches', []))} batches, {len(research.get('skipped', []))} skipped |
| Split | {_status_icon(split)} | {split.get('items_processed', '?')} single-company files created |
| Curate | {_status_icon(curate)} | {curate.get('items_processed', '?')}/{curate.get('limit', '?')} curated, {curate.get('failed', 0)} failed |
| Purpose Claims | {_status_icon(claims)} | {claims.get('items_processed', '?')}/{claims.get('limit', '?')} scanned, +{claims.get('claims_added', 0)} claims |
| Synthesis | {_status_icon(synthesis)} | {synthesis.get('items_processed', '?')}/{synthesis.get('limit', '?')} synthesized |
| Validation | {_status_icon(validation)} | {validation.get('errors', '?')} errors, {validation.get('warnings', '?')} warnings |

## Time Budget

{budget.summary()}

## Research Batches

"""
    for batch in research.get("batches", []):
        icon = "✓" if batch.get("success") else "✗"
        content += f"- {icon} **{batch['name']}** ({batch['mode']}, limit={batch['limit']})\n"
    if research.get("skipped"):
        content += f"\nSkipped (time pressure): {', '.join(research['skipped'])}\n"

    content += f"""
## Validation

- Errors: {validation.get('errors', 'not run')}
- Warnings: {validation.get('warnings', 'not run')}

## Review Checklist

- [ ] Check field journal: `pipeline-reports/{today}-field-journal.md`
- [ ] Review any new insights added to `synthesis/insights.json`
- [ ] Check for validation errors
- [ ] Review failed phases and investigate

---
*Generated by `scripts/overnight-pipeline.py`*
"""

    if not dry_run:
        with open(briefing_path, "w") as f:
            f.write(content)
        log.info(f"Morning briefing: {briefing_path}")
    else:
        log.info(f"[DRY RUN] Would write briefing to {briefing_path}")


def _status_icon(result: dict) -> str:
    if not result:
        return "-- Not run"
    if result.get("skipped"):
        return "⏭ Skipped"
    if result.get("success") is False:
        return "✗ Failed"
    items = result.get("items_processed", None)
    if items is not None and items == 0:
        return "⚠ Empty queue"
    if result.get("success"):
        return "✓"
    return "-- Not run"


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Nightly pipeline orchestrator"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    parser.add_argument("--day", type=str,
                        choices=["monday", "tuesday", "wednesday", "thursday",
                                 "friday", "saturday", "sunday"],
                        help="Override day of week (default: today)")
    parser.add_argument("--phase", type=str,
                        choices=["1", "2", "3", "4", "5", "6", "all"],
                        default="all", help="Run specific phase")
    parser.add_argument("--budget-minutes", type=int, default=720,
                        help="Total time budget in minutes (default: 720 = 12 hours)")
    parser.add_argument("--skip-permissions", action="store_true",
                        help="Pass --skip-permissions to child scripts")
    args = parser.parse_args()

    # ─── Load Schedule ────────────────────────────────────────────────
    if not SCHEDULE_FILE.exists():
        log.error(f"Schedule file not found: {SCHEDULE_FILE}")
        sys.exit(1)

    schedule = load_json(SCHEDULE_FILE)

    # ─── Determine Day ────────────────────────────────────────────────
    if args.day:
        day = args.day
    else:
        days = ["monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday"]
        day = days[date.today().weekday()]

    day_config = schedule.get("schedule", {}).get(day)
    if not day_config:
        log.error(f"No schedule config for {day}")
        sys.exit(1)

    # ─── Banner ───────────────────────────────────────────────────────
    log.info("╔════════════════════════════════════════════════════╗")
    log.info(f"║  OVERNIGHT PIPELINE — {day.upper():10s}                    ║")
    log.info(f"║  {date.today().isoformat()}                                 ║")
    log.info(f"║  Mode: {'DRY RUN' if args.dry_run else 'LIVE':8s}                              ║")
    log.info("╚════════════════════════════════════════════════════╝")

    themes = day_config.get("themes", [])
    log.info(f"\nSchedule for {day}:")
    for t in themes:
        log.info(f"  Research: {t['name']} ({t['mode']}, limit={t.get('limit', 8)})")
    log.info(f"  Curate: limit={day_config.get('curate', {}).get('limit', 16)}")
    log.info(f"  Purpose Claims: limit={day_config.get('purposeClaims', {}).get('limit', 8)}")
    log.info(f"  Synthesis: limit={day_config.get('synthesis', {}).get('limit', 16)}")

    # ─── Time Budget ─────────────────────────────────────────────────
    budget = TimeBudget(args.budget_minutes)
    phase_results = {}

    # ─── Execute Phases ──────────────────────────────────────────────
    phases_to_run = args.phase

    if phases_to_run in ("all", "1"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 1: RESEARCH")
        log.info(f"{'='*60}")
        phase_results["research"] = phase1_research(
            day_config, budget, args.skip_permissions, args.dry_run
        )

    if phases_to_run in ("all", "1", "2"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 1b: SPLIT RESEARCH → SINGLE-COMPANY")
        log.info(f"{'='*60}")
        phase_results["split"] = phase1b_split(budget, args.dry_run)

    if phases_to_run in ("all", "2"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 2: CURATE")
        log.info(f"{'='*60}")
        phase_results["curate"] = phase2_curate(
            day_config, budget, args.skip_permissions, args.dry_run
        )

    if phases_to_run in ("all", "3"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 3: PURPOSE CLAIMS")
        log.info(f"{'='*60}")
        phase_results["purpose_claims"] = phase3_purpose_claims(
            day_config, budget, args.skip_permissions, args.dry_run
        )

    if phases_to_run in ("all", "4"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 4: SYNTHESIS")
        log.info(f"{'='*60}")
        phase_results["synthesis"] = phase4_synthesis(
            day_config, budget, args.skip_permissions, args.dry_run
        )

    if phases_to_run in ("all", "5"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 5: VALIDATION")
        log.info(f"{'='*60}")
        phase_results["validation"] = phase5_validation(budget, args.dry_run)

    if phases_to_run in ("all", "6"):
        log.info(f"\n{'='*60}")
        log.info("PHASE 6: MORNING BRIEFING")
        log.info(f"{'='*60}")
        write_morning_briefing(day, budget, phase_results, args.dry_run)

    # ─── Final Summary ───────────────────────────────────────────────
    log.info(f"\n{'='*60}")
    log.info("PIPELINE COMPLETE")
    log.info(f"{'='*60}")
    log.info(budget.summary())

    if not args.dry_run:
        write_changelog("overnight-pipeline.py", [
            f"Nightly pipeline ran for {day}",
            f"Duration: {budget.elapsed_str()}",
            f"Phases: {phases_to_run}",
        ])


if __name__ == "__main__":
    main()
