# ngram TUI — Implementation: Code Architecture (Planned)

```
STATUS: DRAFT
CREATED: 2025-12-18
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

## CODE STRUCTURE (Planned)

```
src/ngram/
├── tui/                          # TUI package
│   ├── __init__.py               # Package exports
│   ├── app.py                    # Main Textual App (~200L target)
│   ├── widgets/
│   │   ├── __init__.py           # Widget exports
│   │   ├── manager_panel.py      # Left column manager display
│   │   ├── agent_panel.py        # Single agent output display
│   │   ├── agent_container.py    # Columns/tabs container
│   │   ├── input_bar.py          # Bottom input widget
│   │   └── status_bar.py         # Top status bar
│   ├── styles/
│   │   └── theme.tcss            # White theme CSS
│   ├── state.py                  # Session state management
│   ├── commands.py               # Slash command handlers
│   └── manager.py                # Manager agent logic (future)
├── tui_command.py                # CLI entry point for TUI
└── repair_core.py                # Shared repair logic (EXISTS)
```

### File Responsibilities (Planned)

| File | Lines | Status | Purpose | Key Functions/Classes |
|------|-------|--------|---------|----------------------|
| `tui/app.py` | ~200L | TARGET | Main Textual application | `NgramApp`, `compose()`, `on_mount()` |
| `tui/widgets/manager_panel.py` | ~100L | TARGET | Manager message display | `ManagerPanel`, `add_message()` |
| `tui/widgets/agent_panel.py` | ~100L | TARGET | Single agent output | `AgentPanel`, `append_output()` |
| `tui/widgets/agent_container.py` | ~150L | TARGET | Multi-agent layout | `AgentContainer`, `add_agent()` |
| `tui/widgets/input_bar.py` | ~80L | TARGET | User input capture | `InputBar`, `on_submit()` |
| `tui/widgets/status_bar.py` | ~50L | TARGET | Health score display | `StatusBar`, `update_health()` |
| `tui/state.py` | ~100L | TARGET | Session state | `SessionState`, `AgentHandle` |
| `tui/commands.py` | ~150L | TARGET | Command routing | `handle_repair()`, `handle_doctor()` |
| `tui/styles/theme.tcss` | ~100L | TARGET | CSS styling | (Textual CSS) |
| `tui_command.py` | ~30L | TARGET | Entry point | `main()` |
| `repair_core.py` | ~465L | EXISTS | Shared logic | `spawn_repair_agent_async()` |

---

## DESIGN PATTERNS

### Architecture Pattern: Component-Based UI

**Pattern:** Textual widget composition

**Why:** Textual provides CSS-like styling, async support, and composable widgets. Matches Claude Code aesthetic.

**Where:** All `widgets/*.py` files compose into `app.py`

### Code Patterns

| Pattern | Where Used | Purpose |
|---------|------------|---------|
| Observer | Agent output callbacks | Stream output to panels |
| Factory | `commands.py` | Route commands to handlers |
| State | `state.py` | Centralized session state |
| Composition | `app.py` | Build UI from widgets |

### Anti-Patterns to Avoid

- **Monolithic app.py** — Keep under 200 lines, delegate to widgets
- **Sync blocking** — Never block event loop, use async throughout
- **Global state** — Use SessionState class, not module globals
- **Hardcoded colors** — All styling in theme.tcss

### Boundary Definitions

**Inside TUI module:**
- Widget rendering
- User input handling
- Layout management
- Command parsing

**Outside TUI module (use via imports):**
- Repair logic (`repair_core.py`)
- Doctor checks (`doctor.py`)
- File operations (agents handle this)

---

## SCHEMA

### SessionState

```yaml
SessionState:
  required:
    - health_score: int           # Current health 0-100
    - active_agents: List[AgentHandle]
    - running: bool               # App running state
  optional:
    - manager_messages: List[str] # Message history
    - last_command: str           # Most recent command
```

### AgentHandle

```yaml
AgentHandle:
  required:
    - id: str                     # Unique identifier
    - issue_type: str             # e.g., "INCOMPLETE_CHAIN"
    - target_path: str            # Issue target
    - process: asyncio.Process    # Subprocess handle
    - status: str                 # running/completed/failed/timeout
  optional:
    - output_buffer: List[str]    # Captured output lines
    - start_time: float           # For duration tracking
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `tui_command.py:10` (planned) | `ngram` (no args) |
| `NgramApp.compose()` | `tui/app.py:30` (planned) | Textual mount |
| `InputBar.on_submit()` | `tui/widgets/input_bar.py:40` (planned) | User Enter |

---

## DATA FLOW

### User Command Flow

```
┌─────────────────┐
│   User Input    │
│   "/repair"     │
└────────┬────────┘
         │ string
         ▼
┌─────────────────┐
│   InputBar      │ ← captures input, emits event
│   input_bar.py  │
└────────┬────────┘
         │ SlashCommand
         ▼
┌─────────────────┐
│   NgramApp      │ ← routes to handler
│   app.py        │
└────────┬────────┘
         │ dispatch
         ▼
┌─────────────────┐
│   commands.py   │ ← handle_repair()
│   handle_*()    │
└────────┬────────┘
         │ spawns agents
         ▼
┌─────────────────┐
│  repair_core    │ ← spawn_repair_agent_async()
│  repair_core.py │
└────────┬────────┘
         │ asyncio.Process per issue
         ▼
┌─────────────────┐
│ AgentContainer  │ ← displays in columns
│ agent_container │
└─────────────────┘
```

### Agent Output Flow

```
┌─────────────────┐
│   Claude Agent  │ ← subprocess
│   (external)    │
└────────┬────────┘
         │ stdout lines
         ▼
┌─────────────────┐
│ spawn_async()   │ ← on_output callback
│ repair_core.py  │
└────────┬────────┘
         │ parsed text
         ▼
┌─────────────────┐
│  AgentPanel     │ ← append_output()
│  agent_panel.py │
└────────┬────────┘
         │ render
         ▼
┌─────────────────┐
│  User Display   │
└─────────────────┘
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
app.py
    └── imports → widgets/*
    └── imports → state.py
    └── imports → commands.py

commands.py
    └── imports → repair_core.py
    └── imports → doctor.py

tui_command.py
    └── imports → app.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `textual` | TUI framework | `app.py`, `widgets/*` |
| `asyncio` | Async subprocess | `commands.py` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Session state | `state.py:SessionState` | App instance | App lifetime |
| Agent handles | `SessionState.active_agents` | Session | Per repair run |
| Widget state | Individual widgets | Widget instance | Widget lifetime |

### State Transitions

```
IDLE ──/repair──▶ RUNNING ──complete──▶ IDLE
                     │
                     ├──error──▶ IDLE (with error message)
                     │
                     └──timeout──▶ IDLE (with timeout message)
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Import textual (fail gracefully if missing)
2. Create NgramApp instance
3. Mount widgets (compose)
4. Run initial doctor check
5. Focus input bar
6. Enter event loop
```

### Main Loop

```
1. Await input event
2. Parse command
3. Dispatch to handler
4. Update UI
5. Back to step 1
```

### Shutdown

```
1. Signal all agent processes to terminate
2. Wait for graceful shutdown (timeout 5s)
3. Force kill remaining
4. Restore terminal
5. Exit
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Textual App | async | Event-driven, single thread |
| Agent processes | subprocess | Independent processes |
| Output streaming | async callback | Non-blocking |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `AGENT_TIMEOUT` | `repair_core.py` | 600s | Max agent runtime |
| Theme | `theme.tcss` | white | Visual theme |

---

## BIDIRECTIONAL LINKS

### Code → Docs (Planned)

Files will reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| `tui/app.py` | 1 | `# DOCS: docs/tui/PATTERNS_TUI_Design.md` |

### Docs → Code

| Doc Section | Will Be Implemented In |
|-------------|------------------------|
| ALGORITHM main loop | `tui/app.py:run()` |
| BEHAVIOR B1 launch | `tui_command.py:main()` |
| BEHAVIOR B2 repair | `tui/commands.py:handle_repair()` |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Exact line counts will differ from targets — update after implementation
- [ ] Need to decide: separate file for each command or single commands.py?
- IDEA: Config file for TUI settings (theme, timeout, etc.)
- QUESTION: Should widgets be classes or functions?
