"""
scripts/lib/utils.py
====================
Shared safety primitives for overnight automation scripts.

Provides:
  - save_json()          Atomic JSON writes with backup + validation
  - load_json()          Safe JSON loading with meaningful errors
  - acquire_lock()       PID-based file locking (prevents concurrent runs)
  - release_lock()       Release a held lock
  - preflight_check()    Validate required files exist and parse before expensive runs
  - setup_logging()      Dual file+stdout logging with timestamps
  - write_changelog()    Append audit entries to data/CHANGELOG.md

Constants:
  - PROJECT_ROOT, BLOCKED_DOMAINS, CLAIM_TYPES, LOCKS_DIR, CHANGELOG_PATH
"""

import json
import logging
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ─── Constants ──────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent.parent

LOCKS_DIR = PROJECT_ROOT / "scripts" / ".locks"
CHANGELOG_PATH = PROJECT_ROOT / "data" / "CHANGELOG.md"

# Domains that always 403 — shared across all overnight scripts
BLOCKED_DOMAINS = [
    "bloomberg.com",
    "wsj.com",
    "ft.com",
    "seekingalpha.com",
    "investing.com",
    "klover.ai",
    "aimagazine.com",
    "biopharmadive.com",
    "mckinsey.com",  # hangs indefinitely on WebFetch
]

# Purpose claims taxonomy v2.0
CLAIM_TYPES = [
    "utopian",
    "teleological",
    "higher-calling",
    "identity",
    "survival",
    "commercial-success",
]


# ─── Atomic JSON I/O ───────────────────────────────────────────────────────

def save_json(
    path: str | Path,
    data: dict | list,
    *,
    backup: bool = True,
    indent: int = 2,
    trailing_newline: bool = True,
) -> Path:
    """
    Write JSON atomically: tmp file -> validate -> backup original -> os.replace().

    On success: returns the path written.
    On failure: raises exception, original file untouched, .tmp may remain for debugging.

    Args:
        path:   Target file path.
        data:   JSON-serializable data.
        backup: If True and target exists, copy original to {path}.bak before replacing.
        indent: JSON indentation level.
        trailing_newline: If True, append a newline after JSON (matches git convention).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Write to a temporary file in the same directory (same filesystem = atomic rename)
    tmp_fd, tmp_path = tempfile.mkstemp(
        suffix=".tmp",
        prefix=f".{path.stem}_",
        dir=str(path.parent),
    )

    try:
        # Write JSON to tmp
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        if trailing_newline and not content.endswith("\n"):
            content += "\n"

        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)

        # 2. Validate: re-read tmp and parse to ensure valid JSON was written
        with open(tmp_path, "r", encoding="utf-8") as f:
            json.load(f)

        # 3. Backup original if it exists
        if backup and path.exists():
            backup_path = path.with_suffix(path.suffix + ".bak")
            # Copy (not move) so original stays until os.replace
            import shutil
            shutil.copy2(str(path), str(backup_path))

        # 4. Atomic replace (POSIX: atomic; Windows: nearly atomic)
        os.replace(tmp_path, str(path))

        return path

    except Exception:
        # Clean up tmp on failure (if it still exists)
        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except OSError:
            pass
        raise


def load_json(path: str | Path) -> dict | list:
    """
    Load and parse a JSON file with clear error messages.

    Raises:
        FileNotFoundError: with the actual path that's missing.
        json.JSONDecodeError: with the file path in the message.
        ValueError: if file is empty.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        raise ValueError(f"File is empty: {path}")

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {path}: {e.msg}",
            e.doc,
            e.pos,
        ) from e


# ─── PID-Based Locking ─────────────────────────────────────────────────────

def _is_pid_alive(pid: int) -> bool:
    """Check if a process with given PID is still running."""
    try:
        os.kill(pid, 0)  # signal 0 = existence check, no actual signal sent
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # process exists but we can't signal it


def acquire_lock(name: str) -> Path:
    """
    Acquire a named lock. Writes PID to scripts/.locks/{name}.lock.

    If a lock file exists:
      - If the PID is dead, warns and removes the stale lock.
      - If the PID is alive, raises RuntimeError (another instance is running).

    Returns the lock file path (pass to release_lock when done).
    """
    LOCKS_DIR.mkdir(parents=True, exist_ok=True)
    lock_path = LOCKS_DIR / f"{name}.lock"

    if lock_path.exists():
        try:
            existing_pid = int(lock_path.read_text().strip())
        except (ValueError, OSError):
            existing_pid = -1

        if existing_pid > 0 and _is_pid_alive(existing_pid):
            raise RuntimeError(
                f"Lock '{name}' held by PID {existing_pid} (still running). "
                f"If this is stale, delete: {lock_path}"
            )
        else:
            # Stale lock — PID is dead
            log = logging.getLogger("lib.utils")
            log.warning(
                f"Removing stale lock '{name}' (PID {existing_pid} is dead)"
            )
            lock_path.unlink(missing_ok=True)

    # Write our PID
    lock_path.write_text(str(os.getpid()))
    return lock_path


def release_lock(lock_path: str | Path) -> None:
    """Release a lock by removing its file. Safe to call even if already released."""
    path = Path(lock_path)
    path.unlink(missing_ok=True)


# ─── Preflight Checks ──────────────────────────────────────────────────────

def preflight_check(
    required_files: list[str | Path],
    *,
    check_claude_cli: bool = True,
    required_dirs: list[str | Path] | None = None,
) -> list[str]:
    """
    Validate prerequisites before starting an expensive run.

    Checks all conditions and collects ALL failures (doesn't stop at the first).
    Returns list of failure messages (empty = all checks passed).

    Args:
        required_files: Files that must exist and be valid JSON (if .json extension).
        check_claude_cli: If True, verify `claude` command is available.
        required_dirs: Directories that must exist (created if missing).
    """
    failures = []

    # Check required files exist and parse
    for filepath in required_files:
        p = Path(filepath)
        if not p.exists():
            failures.append(f"Missing required file: {p}")
        elif p.suffix == ".json":
            try:
                load_json(p)
            except (json.JSONDecodeError, ValueError) as e:
                failures.append(f"Invalid JSON: {p} — {e}")

    # Check/create required directories
    if required_dirs:
        for dirpath in required_dirs:
            d = Path(dirpath)
            try:
                d.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                failures.append(f"Cannot create directory {d}: {e}")

    # Check Claude CLI is available
    if check_claude_cli:
        import shutil
        if not shutil.which("claude"):
            failures.append(
                "Claude CLI not found in PATH. "
                "Install: https://docs.anthropic.com/en/docs/claude-code"
            )

    return failures


# ─── Logging Setup ──────────────────────────────────────────────────────────

def setup_logging(
    name: str,
    *,
    log_file: str | Path | None = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure dual file+stdout logging with timestamped format.

    Args:
        name:     Logger name (usually the script basename).
        log_file: Path for log file. If None, defaults to PROJECT_ROOT / f"{name}.log".
        level:    Logging level.

    Returns:
        Configured logger instance.
    """
    if log_file is None:
        log_file = PROJECT_ROOT / f"{name}.log"

    log_file = Path(log_file)

    # Reset root logger handlers to avoid duplicate output from basicConfig
    root = logging.getLogger()
    root.handlers.clear()

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )

    return logging.getLogger(name)


# ─── Changelog ──────────────────────────────────────────────────────────────

def write_changelog(
    script_name: str,
    changes: list[str],
    *,
    changelog_path: str | Path | None = None,
) -> None:
    """
    Append a timestamped entry to data/CHANGELOG.md.

    Each entry records: when, what script, and what changed.
    Format is human-readable and grep-friendly.

    Args:
        script_name:    Name of the script making the change.
        changes:        List of change descriptions (one per line).
        changelog_path: Override path (defaults to data/CHANGELOG.md).
    """
    if changelog_path is None:
        changelog_path = CHANGELOG_PATH

    changelog_path = Path(changelog_path)
    changelog_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"\n## {timestamp} — {script_name}\n",
    ]
    for change in changes:
        lines.append(f"- {change}\n")
    lines.append("\n")

    # Append (create if missing)
    with open(changelog_path, "a", encoding="utf-8") as f:
        f.writelines(lines)
