# DOCS: docs/tui/PATTERNS_TUI_Modular_Interface_Design.md
"""
ngram TUI - Claude Code-style interactive interface.

Entry point: `ngram` (no subcommand) launches the TUI.
"""

from .app import NgramApp
from .state import SessionState, AgentHandle

__all__ = ["NgramApp", "SessionState", "AgentHandle"]
