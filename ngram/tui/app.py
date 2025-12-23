# DOCS: docs/tui/PATTERNS_TUI_Modular_Interface_Design.md
"""
ngram TUI entry point for the Textual application.
"""

from pathlib import Path
from typing import Optional

from .app_core import NgramApp, check_textual


def main(target_dir: Optional[Path] = None, agent_provider: str = "codex") -> None:
    """
    Launch the ngram TUI.

    Entry point for `ngram` command (no subcommand).
    """
    check_textual()
    app = NgramApp(target_dir=target_dir, agent_provider=agent_provider)
    app.run()


if __name__ == "__main__":
    main()
