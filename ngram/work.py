"""
Work command for ngram CLI.

The unified entry point for AI-assisted work on a project path.
Automatically runs doctor, then spawns work agents to fix issues.

Replaces the old `ngram repair` command with a simpler interface:
    ngram work <path> [objective]
"""
# DOCS: docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md

from pathlib import Path
from typing import List, Optional

from .doctor import run_doctor, load_doctor_config, DoctorIssue
from .doctor_types import DoctorConfig
from .agent_cli import normalize_agent
from .repair_core import (
    ISSUE_PRIORITY,
    get_depth_types,
)
from .repair_escalation_interactive import (
    Colors,
)

# Import the heavy lifting from repair.py (to be consolidated later)
from .repair import (
    repair_command as _repair_command_impl,
)


def work_command(
    path: Path,
    objective: Optional[str] = None,
    max_issues: Optional[int] = None,
    issue_types: Optional[List[str]] = None,
    depth: str = "docs",
    dry_run: bool = False,
    parallel: int = 5,
    agent_provider: str = "codex",
) -> int:
    """
    Run the work command on a path.

    Args:
        path: Target path (file or directory) to work on
        objective: Optional natural language objective for the work
        max_issues: Maximum issues to fix (default: all)
        issue_types: Only fix specific issue types
        depth: Repair depth: links, docs, or full
        dry_run: Show what would be done without spawning agents
        parallel: Number of parallel agents
        agent_provider: Which agent provider to use

    Returns:
        Exit code (0 = success)
    """
    # Resolve path
    target_path = Path(path).resolve()

    # Determine target directory
    if target_path.is_file():
        target_dir = target_path.parent
        # TODO: Scope work to specific file when path is a file
    else:
        target_dir = target_path

    # Print header with objective if provided
    if objective:
        print(f"{Colors.BOLD}Objective:{Colors.RESET} {objective}")
        print()

    # Delegate to repair implementation
    # (Later: integrate objective into agent prompts)
    return _repair_command_impl(
        target_dir=target_dir,
        max_issues=max_issues,
        issue_types=issue_types,
        depth=depth,
        dry_run=dry_run,
        parallel=parallel,
        agent_provider=agent_provider,
    )
