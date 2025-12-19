# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""
Container for multiple agent panels.

Switches between columns (1-3 agents) and tabs (>3 agents).
"""

from typing import TYPE_CHECKING

from textual.containers import Horizontal
from textual.widgets import Static, TabbedContent, TabPane

if TYPE_CHECKING:
    from ..state import AgentHandle


class AgentContainer(Horizontal):
    """
    Container that displays agent panels in columns or tabs.

    Behavior:
    - 1-3 agents: Side-by-side columns
    - 4+ agents: Tabbed interface

    Dynamically adds/removes panels as agents start/complete.
    """

    DEFAULT_CSS = """
    AgentContainer {
        width: 70%;
    }

    AgentContainer.empty {
        align: center middle;
    }

    AgentContainer .placeholder {
        text-align: center;
        color: $text-muted;
    }
    """

    MAX_COLUMNS = 3

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._agent_panels: dict[str, any] = {}
        self._tabbed: TabbedContent | None = None

    def on_mount(self) -> None:
        """Initialize with placeholder."""
        placeholder = Static(
            "No agents running.\nType /repair to start.",
            classes="placeholder"
        )
        self.mount(placeholder)
        self.add_class("empty")

    def add_agent(self, agent: "AgentHandle") -> None:
        """Add a panel for a new agent."""
        from .agent_panel import AgentPanel

        # Remove placeholder if present
        placeholder = self.query(".placeholder")
        if placeholder:
            placeholder.first().remove()
            self.remove_class("empty")

        panel = AgentPanel(
            agent_id=agent.id,
            symbol=agent.symbol,
            issue_type=agent.issue_type,
            target_path=agent.target_path,
            id=f"agent-panel-{agent.id}",
        )

        if len(self._agent_panels) < self.MAX_COLUMNS:
            # Use columns
            self.mount(panel)
        else:
            # Switch to tabs if needed
            if not self._tabbed:
                self._convert_to_tabs()
            # Add as new tab
            pane = TabPane(f"{agent.symbol} {agent.issue_type}", panel)
            self._tabbed.add_pane(pane)

        self._agent_panels[agent.id] = panel

    def update_agent(self, agent_id: str, text: str) -> None:
        """Update an agent's output."""
        panel = self._agent_panels.get(agent_id)
        if panel:
            panel.append_output(text)

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent's panel."""
        panel = self._agent_panels.pop(agent_id, None)
        if panel:
            panel.remove()

        # Show placeholder if empty
        if not self._agent_panels:
            placeholder = Static(
                "No agents running.\nType /repair to start.",
                classes="placeholder"
            )
            self.mount(placeholder)
            self.add_class("empty")

    def set_agent_status(self, agent_id: str, status: str) -> None:
        """Update an agent's status."""
        panel = self._agent_panels.get(agent_id)
        if panel:
            panel.set_status(status)

    def _convert_to_tabs(self) -> None:
        """Convert column layout to tabs."""
        # This would require restructuring - for now, just stack
        pass
