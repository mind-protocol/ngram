# ngram TUI — Implementation: Code Architecture

```
STATUS: IMPLEMENTED
CREATED: 2025-12-18
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
BEHAVIORS:       ./BEHAVIORS_TUI_Interactions.md
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
THIS:            IMPLEMENTATION_TUI_Code_Architecture.md (you are here)
TEST:            ./TEST_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md
```

---

## CODE STRUCTURE

```
ngram/tui/                           # TUI package root
ngram/tui/__init__.py                # Package exports (11L)
ngram/tui/app.py                     # Main Textual App (491L)
ngram/tui/state.py                   # Session state management (169L)
ngram/tui/commands.py                # Slash command handlers (637L)
ngram/tui/commands_agent.py          # Manager agent subprocess helpers (349L)
ngram/tui/manager.py                 # Manager supervisor & Claude PTY (Claude only) (275L)
ngram/tui/widgets/__init__.py        # Widget exports (20L)
ngram/tui/widgets/manager_panel.py   # Left column manager display (138L)
ngram/tui/widgets/agent_panel.py     # Single agent output display (97L)
ngram/tui/widgets/agent_container.py # Columns/tabs container (120L)
ngram/tui/widgets/input_bar.py       # Bottom input widget (133L)
ngram/tui/widgets/status_bar.py      # Top status bar (74L)
ngram/tui/styles/theme.tcss          # Paper & Parchment theme CSS (244L)
ngram/cli.py                         # CLI entry point (TUI launched via `ngram`)
ngram/repair_core.py                 # Shared repair logic (497L)
```

Manager startup prefers `.ngram/agents/manager/AGENTS.md` when present; otherwise it mirrors `.ngram/CLAUDE.md` into the manager working directory and writes AGENTS.md for Codex/Gemini compatibility.

### File Responsibilities

| File | Lines | Status | Purpose | Key Functions/Classes |
|------|-------|--------|---------|----------------------|
| `ngram/tui/app.py` | 491L | EXISTS | Main Textual application | `NgramApp`, `compose()`, `on_mount()`, `main()` |
| `ngram/tui/widgets/manager_panel.py` | 138L | EXISTS | Manager message display | `ManagerPanel`, `add_message()`, `add_thinking()` |
| `ngram/tui/widgets/agent_panel.py` | 97L | EXISTS | Single agent output | `AgentPanel`, `append_output()` |
| `ngram/tui/widgets/agent_container.py` | 120L | EXISTS | Multi-agent layout | `AgentContainer`, `add_agent()` |
| `ngram/tui/widgets/input_bar.py` | 133L | EXISTS | User input capture | `InputBar`, `on_submit()`, history, tab completion |
| `ngram/tui/widgets/status_bar.py` | 74L | EXISTS | Health score display | `StatusBar`, `update_health()` |
| `ngram/tui/state.py` | 169L | EXISTS | Session state | `SessionState`, `AgentHandle`, `ConversationHistory` |
| `ngram/tui/commands.py` | 637L | WATCH | Command routing | `handle_command()`, `handle_repair()`, `handle_doctor()` |
| `ngram/tui/commands_agent.py` | 349L | OK | Manager agent subprocess handling | `_run_agent_message()`, `_detect_commands()` |
| `ngram/tui/styles/theme.tcss` | 244L | EXISTS | CSS styling | Paper & Parchment theme |
| `ngram/tui/manager.py` | 275L | EXISTS | Manager supervisor | `ManagerSupervisor`, `ClaudePTY`, `DriftWarning` |
| `ngram/cli.py` | - | EXISTS | CLI entry point | TUI launched via `ngram` (no subcommand) |
| `ngram/repair_core.py` | 497L | EXISTS | Shared logic | `spawn_repair_agent_async()` |

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `ngram/tui/app.py:479` | `ngram` (no args) via `ngram/cli.py` |
| `NgramApp.compose()` | `ngram/tui/app.py:74` | Textual mount |
| `InputBar.action_submit()` | `ngram/tui/widgets/input_bar.py:60` | User Enter |

---

## DATA FLOW (HIGH LEVEL)

```
User input -> InputBar -> NgramApp -> commands.py handlers
  -> repair_core.spawn_repair_agent_async() -> AgentPanel output
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
ngram/tui/app.py
    -> widgets
    -> ngram/tui/state.py
    -> ngram/tui/commands.py
    -> ngram/tui/manager.py

ngram/tui/commands.py
    -> ngram/tui/commands_agent.py
    -> ngram/repair_core.py
    -> ngram/doctor.py

ngram/cli.py
    -> ngram/tui/app.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `textual` | TUI framework | ngram/tui/app.py and widget files |
| `asyncio` | Async subprocess | `ngram/tui/commands.py` |

---

## STATE MANAGEMENT (SUMMARY)

- Session state lives in `ngram/tui/state.py:SessionState`
- Agent handles stored in `SessionState.active_agents`
- Widgets own their local UI state

---

## ARCHIVED DETAIL

More detailed design/runtime notes and historical decisions are archived in:
`docs/tui/archive/IMPLEMENTATION_archive_2024-12.md`
