# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""Status bar widget showing health score and repair progress."""

from pathlib import Path
from textual.widgets import Static


class StatusBar(Static):
    """
    Top status bar displaying project health and repair progress.

    Shows:
    - Folder name (left)
    - Progress bar with issues (center) - when repairs running
    - Health score (right)
    """

    DEFAULT_CSS = """
    StatusBar {
        dock: top;
        height: 1;
        background: $primary;
        color: white;
        padding: 0 1;
    }
    """

    def __init__(self, folder_name: str = "", **kwargs) -> None:
        self._folder = folder_name or Path.cwd().name
        self._health = 0
        # Repair progress tracking
        self._total_issues = 0
        self._completed_issues = 0
        self._running_issues = 0
        # Animation state for running indicator
        self._anim_frame = 0
        self._anim_timer = None
        # Initialize with default content
        super().__init__(self._format_bar(), **kwargs)

    def set_folder(self, folder_name: str) -> None:
        """Set the folder name."""
        self._folder = folder_name
        self._refresh_display()

    def update_health(self, score: int) -> None:
        """Update the health score display."""
        self._health = max(0, min(100, score))
        self._refresh_display()

    def set_repair_progress(
        self, total: int, completed: int, running: int
    ) -> None:
        """Update repair progress.

        Args:
            total: Total number of issues to fix
            completed: Number of completed fixes
            running: Number of currently running agents
        """
        self._total_issues = total
        self._completed_issues = completed
        self._running_issues = running
        self._refresh_display()

        # Start animation if running, stop if not
        if running > 0 and self._anim_timer is None:
            self._start_animation()
        elif running == 0 and self._anim_timer is not None:
            self._stop_animation()

    def clear_repair_progress(self) -> None:
        """Clear repair progress (repairs done)."""
        self._total_issues = 0
        self._completed_issues = 0
        self._running_issues = 0
        self._stop_animation()
        self._refresh_display()

    def _start_animation(self) -> None:
        """Start the progress bar animation."""
        if self._anim_timer is None:
            self._anim_timer = self.set_interval(0.3, self._animate)

    def _stop_animation(self) -> None:
        """Stop the progress bar animation."""
        if self._anim_timer is not None:
            self._anim_timer.stop()
            self._anim_timer = None

    def _animate(self) -> None:
        """Animation tick - alternate colors for running section."""
        self._anim_frame = (self._anim_frame + 1) % 2
        self._refresh_display()

    def _format_progress_bar(self, width: int = 40) -> str:
        """Format the progress bar with colors.

        Uses:
        - Green █ for completed
        - Yellow/Orange ░ (hachure) for running (animated)
        - Dim ─ for pending
        """
        if self._total_issues == 0:
            return ""

        # Calculate segments
        completed_width = int(width * self._completed_issues / self._total_issues)
        running_width = int(width * self._running_issues / self._total_issues)
        # Ensure at least 1 char for running if there are running agents
        if self._running_issues > 0 and running_width == 0:
            running_width = 1
        pending_width = max(0, width - completed_width - running_width)

        # Animated color for running section
        running_colors = ["yellow", "bright_yellow"]
        running_color = running_colors[self._anim_frame % len(running_colors)]

        # Build bar with colors
        completed_bar = "[green]" + "█" * completed_width + "[/]" if completed_width else ""
        running_bar = f"[{running_color}]" + "░" * running_width + "[/]" if running_width else ""
        pending_bar = "[dim]" + "─" * pending_width + "[/]" if pending_width else ""

        # Calculate percentage
        percent = int(100 * self._completed_issues / self._total_issues)

        # Progress text: "2/13 Tasks (3 in progress) - 15%"
        progress_text = f"{self._completed_issues}/{self._total_issues} Tasks"
        if self._running_issues > 0:
            progress_text += f" ({self._running_issues} in progress)"
        progress_text += f" - {percent}%"

        # Use escaped brackets \[ and \] to avoid Rich markup interpretation
        return f"\\[{completed_bar}{running_bar}{pending_bar}\\] {progress_text}"

    def _format_bar(self) -> str:
        """Format the status bar content."""
        health_color = self._get_health_color()
        left = f"ngram: {self._folder}"
        right = f"Health: [{health_color}]{self._health}/100[/]"

        # Use width from parent or default
        try:
            width = self.size.width or 80
        except Exception:
            width = 80

        # Build center section (progress bar if repairing)
        bar_width = 40
        center = self._format_progress_bar(bar_width)

        # Calculate lengths (excluding markup)
        left_len = len(left)
        right_len = len(f"Health: {self._health}/100")

        if center and self._total_issues:
            # Estimate center length (bar + text)
            # "[████░░──────] 2/13 Tasks (3 in progress) - 15%"
            percent = int(100 * self._completed_issues / self._total_issues)
            progress_text = f"{self._completed_issues}/{self._total_issues} Tasks"
            if self._running_issues > 0:
                progress_text += f" ({self._running_issues} in progress)"
            progress_text += f" - {percent}%"
            center_len = bar_width + 3 + len(progress_text)  # bar + [] + space + text

            # Three sections: left | center | right
            left_pad = " " * max(1, (width - left_len - center_len - right_len) // 2 - 1)
            right_pad = " " * max(1, width - left_len - len(left_pad) - center_len - right_len - 1)
            return f"{left}{left_pad}{center}{right_pad}{right}"
        else:
            # Two sections: left | right
            padding = " " * max(1, width - left_len - right_len - 2)
            return f"{left}{padding}{right}"

    def _refresh_display(self) -> None:
        """Refresh the status bar content."""
        self.update(self._format_bar())

    def _get_health_color(self) -> str:
        """Get color based on health score."""
        if self._health >= 80:
            return "green"
        elif self._health >= 50:
            return "yellow"
        else:
            return "red"

    def on_resize(self) -> None:
        """Handle terminal resize - reposition elements."""
        self._refresh_display()
