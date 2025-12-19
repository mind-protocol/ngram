# DOCS: docs/tui/PATTERNS_TUI_Design.md
"""
ngram TUI - Main Textual Application.

Claude Code-style persistent chat interface with:
- Manager panel (left column)
- Agent panels (right columns/tabs)
- Input bar (bottom)
- Status bar (top)
"""

import asyncio
from pathlib import Path
from typing import Optional

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Footer, Static
    from textual.binding import Binding
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    # Stubs for type checking when textual not installed
    App = object
    ComposeResult = None

from .state import SessionState, ConversationHistory
from .manager import ManagerSupervisor, DriftWarning, ClaudePTY


def check_textual() -> None:
    """Raise ImportError if textual is not available."""
    if not TEXTUAL_AVAILABLE:
        raise ImportError(
            "textual is required for the TUI. Install with: pip install ngram[tui]"
        )


class NgramApp(App if TEXTUAL_AVAILABLE else object):
    """
    ngram TUI Application.

    Layout:
    - Top: Status bar with health score
    - Left: Manager panel (~55% width)
    - Right: Agent container (columns or tabs)
    - Bottom: Input bar with /command support
    """

    CSS_PATH = "styles/theme.tcss"

    # Light mode by default (white theme)
    dark = False

    BINDINGS = [
        Binding("ctrl+c", "interrupt_or_quit", "Interrupt/Quit", show=False),
        Binding("ctrl+d", "doctor", "Doctor", show=False),
        Binding("ctrl+r", "repair", "Repair", show=False),
        Binding("ctrl+p", "command_palette", show=False),
    ]

    def __init__(self, target_dir: Optional[Path] = None) -> None:
        """Initialize the TUI app."""
        check_textual()
        super().__init__()
        self.target_dir = target_dir or Path.cwd()
        self.state = SessionState()
        self.conversation = ConversationHistory(self.target_dir)
        self.supervisor = ManagerSupervisor(on_warning=self._handle_drift_warning)
        self._in_error_handler = False  # Prevent infinite loops
        self.claude_pty: Optional[ClaudePTY] = None
        self._ctrl_c_pending = False  # Track first Ctrl+C press

    def compose(self) -> ComposeResult:
        """Compose the TUI layout."""
        from .widgets.status_bar import StatusBar
        from .widgets.manager_panel import ManagerPanel
        from .widgets.agent_container import AgentContainer
        from .widgets.input_bar import InputBar

        yield StatusBar(folder_name=self.target_dir.name, id="status-bar")

        with Horizontal(id="main-container"):
            # Left column: manager panel + input
            with Vertical(id="manager-column"):
                yield ManagerPanel(id="manager-panel")
                yield InputBar(id="input-bar")
            # Right column: agent container
            yield AgentContainer(id="agent-container")

    async def on_mount(self) -> None:
        """Run on app mount - initial setup."""
        # Focus input bar
        input_bar = self.query_one("#input-bar")
        input_bar.focus()

        manager = self.query_one("#manager-panel")

        # Load previous conversation history
        previous = self.conversation.get_recent(limit=20)
        if previous:
            from textual.widgets import Static
            # Add separator
            sep1 = Static("[dim]─── Previous Session ───[/]", classes="message")
            manager.mount(sep1)
            manager._messages.append(sep1)

            for msg in previous:
                if msg.role == "system" and "New Session" in msg.content:
                    widget = Static(f"[dim]{msg.content}[/]", classes="message")
                elif msg.role == "user":
                    widget = Static(f"[magenta]{msg.content}[/magenta]", classes="message")
                else:
                    # Truncate long assistant messages for history display
                    content = msg.content
                    if len(content) > 500:
                        content = content[:500] + "..."
                    widget = Static(f"[dim]{content}[/]", classes="message")
                manager.mount(widget)
                manager._messages.append(widget)

            sep2 = Static("[dim]─── Current Session ───[/]", classes="message")
            manager.mount(sep2)
            manager._messages.append(sep2)

        # Mark new session start
        self.conversation.start_new_session()

        # Add welcome messages in blue
        manager.add_message("[blue]Running health check...[/]")
        manager.add_message("[blue]Waking up ngram manager...[/]")

        # Run startup tasks in background so UI appears immediately
        asyncio.create_task(self._startup_sequence())

    async def _startup_sequence(self) -> None:
        """Run startup tasks: doctor check then Claude overview."""
        # Run initial health check and show issues
        await self._run_doctor_with_display()

        # Start Claude manager session (also in this background task)
        await self._start_manager_with_overview()

    async def _start_claude_pty(self) -> None:
        """Start the interactive Claude PTY session."""
        manager = self.query_one("#manager-panel")

        # Load system prompt from .ngram/agents/manager/CLAUDE.md
        system_prompt = ""
        prompt_file = self.target_dir / ".ngram" / "agents" / "manager" / "CLAUDE.md"
        if prompt_file.exists():
            system_prompt = prompt_file.read_text()

        async def on_claude_output(text: str) -> None:
            """Handle output from Claude PTY."""
            if text.strip():
                manager.add_message(text)

        self.claude_pty = ClaudePTY(
            target_dir=self.target_dir,
            on_output=on_claude_output,
            system_prompt=system_prompt,
        )

        success = await self.claude_pty.start()
        if not success:
            manager.add_message("[dim]Claude not available - using fallback mode[/dim]")

    async def _start_manager_with_overview(self) -> None:
        """Start Claude manager and prompt for project overview."""
        import json
        import shutil

        manager = self.query_one("#manager-panel")
        initial_prompt = self._build_manager_overview_prompt()

        # Run manager from its own directory to avoid conversation conflicts
        manager_dir = self.target_dir / ".ngram" / "agents" / "manager"
        manager_dir.mkdir(parents=True, exist_ok=True)

        # Copy CLAUDE.md to manager directory if not present
        claude_md_src = self.target_dir / ".ngram" / "CLAUDE.md"
        claude_md_dst = manager_dir / "CLAUDE.md"
        if claude_md_src.exists() and not claude_md_dst.exists():
            shutil.copy(claude_md_src, claude_md_dst)

        cwd = manager_dir

        # Find GLOBAL_LEARNINGS.md
        learnings_file = self.target_dir / ".ngram" / "views" / "GLOBAL_LEARNINGS.md"

        cmd = [
            "claude",
            "-p", initial_prompt,
            "--output-format", "stream-json",
            "--verbose",
            "--dangerously-skip-permissions",
            "--add-dir", str(self.target_dir),
            "--continue",
        ]
        cmd.extend(["--allowedTools", "Bash(*) Read(*) Edit(*) Write(*) Glob(*) Grep(*) WebFetch(*) WebSearch(*) NotebookEdit(*) Task(*) TodoWrite(*)"])
        if learnings_file.exists():
            cmd.extend(["--append-system-prompt", str(learnings_file)])

        # Show loading indicator with animation
        thinking_msg = manager.add_message("[dim].[/]")
        animation_task = asyncio.create_task(self._animate_loading(thinking_msg))

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout_data, _ = await process.communicate()

            # Stop animation and remove loading indicator
            animation_task.cancel()
            thinking_msg.remove()

            response_parts = []
            for line_str in stdout_data.decode().split('\n'):
                line_str = line_str.strip()
                if not line_str:
                    continue
                try:
                    data = json.loads(line_str)
                    if data.get("type") == "assistant":
                        msg_data = data.get("message", {})
                        for content in msg_data.get("content", []):
                            if content.get("type") == "thinking":
                                thinking = content.get("thinking", "")
                                if thinking:
                                    # Add thinking as collapsible
                                    manager.add_thinking(thinking)
                            elif content.get("type") == "tool_use":
                                # Display tool call
                                tool_name = content.get("name", "unknown")
                                tool_input = content.get("input", {})
                                manager.add_tool_call(tool_name, tool_input)
                            elif content.get("type") == "text":
                                response_parts.append(content.get("text", ""))
                    elif data.get("type") == "result":
                        result = data.get("result", "")
                        if result and not response_parts:
                            response_parts.append(result)
                except json.JSONDecodeError:
                    pass

            if response_parts:
                full_response = "".join(response_parts)
                manager.add_message(full_response)
                self._llm_conversation_started = True

                # Detect commands and show interactive options
                from .commands import _detect_commands
                detected = _detect_commands(full_response)
                if detected:
                    self._pending_commands = detected
                    manager.add_message("")
                    manager.add_message("[bold]Suggested commands:[/]")
                    for i, cmd in enumerate(detected[:5], 1):
                        manager.add_message(f"  [cyan]{i}.[/] {cmd}")
                    manager.add_message("[dim]Type a number to run, or continue chatting[/]")
            else:
                await self._show_static_overview()

        except Exception as e:
            animation_task.cancel()
            thinking_msg.remove()
            self.log_error(f"Manager startup failed: {e}")
            await self._show_static_overview()

    def _build_manager_overview_prompt(self) -> str:
        """Build the initial prompt for manager to provide project overview."""
        return """Please read the following files to understand the project state, then provide an overview:

1. Read `.ngram/PRINCIPLES.md` - the working principles and vision
2. Read `.ngram/PROTOCOL.md` - the protocol overview
3. Read `.ngram/state/SYNC_Project_State.md` - the current project state

Then provide:
- Brief overview of where the project currently stands
- Any active work or recent changes
- Proposed next steps based on the handoff notes

Keep it concise but informative. Focus on actionable state."""

    async def _show_static_overview(self) -> None:
        """Show static overview when Claude is not available."""
        manager = self.query_one("#manager-panel")

        # Read SYNC file directly
        sync_file = self.target_dir / ".ngram" / "state" / "SYNC_Project_State.md"
        if sync_file.exists():
            content = sync_file.read_text()
            # Extract key sections
            lines = content.split('\n')
            summary_lines = []
            in_section = False
            for line in lines[:50]:  # First 50 lines
                if line.startswith('## CURRENT STATE') or line.startswith('## ACTIVE WORK'):
                    in_section = True
                elif line.startswith('## ') and in_section:
                    break
                elif in_section:
                    summary_lines.append(line)

            if summary_lines:
                manager.add_message("Project State:")
                manager.add_message('\n'.join(summary_lines[:15]))
            else:
                manager.add_message("No project state available. Run /doctor to check health.")
        else:
            manager.add_message("No SYNC file found. Initialize with `ngram init` or check .ngram/ directory.")

    async def _animate_loading(self, widget) -> None:
        """Animate the loading indicator until cancelled."""
        dots = [".", "..", "...", ".."]
        i = 0
        try:
            while True:
                await asyncio.sleep(0.3)
                widget.update(f"[dim]{dots[i % len(dots)]}[/]")
                i += 1
        except asyncio.CancelledError:
            pass  # Animation cancelled, exit cleanly
        except Exception:
            pass  # Widget removed or app closing

    def on_click(self) -> None:
        """Focus input bar on any click."""
        input_bar = self.query_one("#input-bar")
        input_bar.focus()

    async def on_input_bar_command_submitted(self, event) -> None:
        """Handle command submitted from input bar."""
        from .widgets.input_bar import InputBar

        try:
            await self.handle_command(event.command)
        except Exception as e:
            self.log_error(str(e))

    async def _run_doctor(self) -> None:
        """Run doctor check and update health score."""
        manager = self.query_one("#manager-panel")
        manager.add_message("[blue]Running health check...[/]")

        try:
            result = await self._run_doctor_async()
            self.state.health_score = result.get("score", 0)
            status_bar = self.query_one("#status-bar")
            status_bar.update_health(self.state.health_score)
            manager.add_message(f"Health: {self.state.health_score}/100")
        except Exception as e:
            self.log_error(f"Health check failed: {e}")

    async def _run_doctor_with_display(self) -> None:
        """Run doctor check and display issues in agent container."""
        from .widgets.agent_container import AgentContainer
        from textual.widgets import Static
        from textual.containers import VerticalScroll

        manager = self.query_one("#manager-panel")
        agent_container = self.query_one("#agent-container")
        # Message already shown in on_mount

        try:
            from ..doctor import run_doctor
            from ..doctor_types import DoctorConfig
            import asyncio

            loop = asyncio.get_event_loop()
            config = DoctorConfig()
            result = await loop.run_in_executor(
                None,
                lambda: run_doctor(self.target_dir, config)
            )

            # Update health score
            score = result.get("score", 50) if isinstance(result, dict) else 50
            issues_dict = result.get("issues", {}) if isinstance(result, dict) else {}
            self.state.health_score = score

            status_bar = self.query_one("#status-bar")
            status_bar.update_health(score)

            # Flatten issues from dict structure
            all_issues = []
            if isinstance(issues_dict, dict):
                for severity in ["critical", "warning", "info"]:
                    all_issues.extend(issues_dict.get(severity, []))

            # Show progress bar with issue count (0 completed, 0 running = all pending)
            repair_issues = [i for i in all_issues if i.severity in ("critical", "warning")]
            if repair_issues:
                status_bar.set_repair_progress(len(repair_issues), 0, 0)

            # Remove placeholder and show issues
            placeholder = agent_container.query(".placeholder")
            if placeholder:
                placeholder.first().remove()
                agent_container.remove_class("empty")

            # Show SYNC_Project_State.md in right panel by default
            sync_file = self.target_dir / ".ngram" / "state" / "SYNC_Project_State.md"
            if sync_file.exists():
                from textual.widgets import Markdown
                sync_content = sync_file.read_text()
                # Wrap in VerticalScroll for scrollability
                # Must mount container first, then add children
                scroll_container = VerticalScroll(id="sync-display-container")
                await agent_container.mount(scroll_container)
                # Use Markdown widget to render formatting
                sync_widget = Markdown(sync_content, id="sync-display")
                await scroll_container.mount(sync_widget)
                # Auto-scroll to top for initial display
                scroll_container.scroll_home(animate=False)
            elif all_issues:
                # Fallback: show issues if no SYNC file
                issue_lines = []
                for issue in all_issues:
                    if issue.severity == "critical":
                        color = "red"
                        symbol = "!"
                    elif issue.severity == "warning":
                        color = "#8B4513"
                        symbol = "?"
                    else:
                        color = "dim"
                        symbol = "·"
                    issue_lines.append(f"[{color}][{symbol}] {issue.issue_type}: {issue.path}[/]")
                # Wrap in VerticalScroll for scrollability
                # Must mount container first, then add children
                scroll_container = VerticalScroll(id="issue-summary-container")
                await agent_container.mount(scroll_container)
                summary = Static("\n".join(issue_lines), id="issue-summary")
                await scroll_container.mount(summary)
                scroll_container.scroll_home(animate=False)
            else:
                # Wrap in VerticalScroll for consistency
                # Must mount container first, then add children
                scroll_container = VerticalScroll(id="healthy-summary-container")
                await agent_container.mount(scroll_container)
                healthy = Static("Project is healthy!", id="healthy-summary")
                await scroll_container.mount(healthy)

        except Exception as e:
            self.log_error(f"Health check failed: {e}")

    async def _run_doctor_async(self) -> dict:
        """Run doctor check asynchronously."""
        import asyncio
        from ..doctor import run_doctor
        from ..doctor_types import DoctorConfig

        # Run doctor in executor to not block event loop
        loop = asyncio.get_event_loop()
        config = DoctorConfig()
        result = await loop.run_in_executor(
            None,
            lambda: run_doctor(self.target_dir, config)
        )
        return {"score": result.get("score", 50) if isinstance(result, dict) else 50}

    async def _handle_drift_warning(self, warning: DriftWarning) -> None:
        """Handle drift warning from supervisor."""
        manager = self.query_one("#manager-panel")
        manager.add_message(
            f"[warning]{warning.agent_symbol} {warning.message}[/warning]"
        )
        manager.add_message(f"  -> {warning.suggestion}")

    async def handle_command(self, command: str) -> None:
        """Handle a slash command from input bar."""
        from .commands import handle_command

        self.state.last_command = command
        await handle_command(self, command)

    def log_error(self, error: str) -> None:
        """Log an error to the manager panel and .ngram/error-log."""
        if self._in_error_handler:
            return  # Prevent infinite loops

        self._in_error_handler = True
        try:
            # Log to file
            from datetime import datetime
            error_log = self.target_dir / ".ngram" / "error.log"
            error_log.parent.mkdir(parents=True, exist_ok=True)
            with open(error_log, "a") as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] {error}\n")

            # Show in manager panel
            manager = self.query_one("#manager-panel")
            manager.add_message(f"[red]Error: {error}[/red]")
        except Exception:
            pass  # Silently fail if we can't show the error
        finally:
            self._in_error_handler = False

    def on_exception(self, error: Exception) -> bool:
        """Handle uncaught exceptions by showing in manager panel."""
        import traceback
        # Suppress selection-related IndexErrors (Textual bug with dynamic content)
        if isinstance(error, IndexError):
            tb_str = "".join(traceback.format_tb(error.__traceback__))
            if "selection" in tb_str or "get_copy_text" in tb_str:
                return True  # Suppress silently - known Textual bug
        self.log_error(str(error))
        return True  # Return True to prevent crash, keep app running

    async def action_quit(self) -> None:
        """Quit the application."""
        self.state.running = False
        # Stop Claude PTY if running
        if self.claude_pty and self.claude_pty.is_running:
            await self.claude_pty.stop()
        self.exit()

    async def action_doctor(self) -> None:
        """Run doctor check."""
        await self._run_doctor()

    async def action_repair(self) -> None:
        """Start repair session."""
        await self.handle_command("/repair")


def main(target_dir: Optional[Path] = None) -> None:
    """
    Launch the ngram TUI.

    Entry point for `ngram` command (no subcommand).
    """
    check_textual()
    app = NgramApp(target_dir=target_dir)
    app.run()


if __name__ == "__main__":
    main()
