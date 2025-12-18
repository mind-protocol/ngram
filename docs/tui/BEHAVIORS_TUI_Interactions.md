# ngram TUI — Behaviors: User Interactions and Observable Effects

```
STATUS: DRAFT
CREATED: 2025-12-18
VERIFIED: Not yet — implementation pending
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_TUI_Design.md
THIS:            BEHAVIORS_TUI_Interactions.md (you are here)
ALGORITHM:       ./ALGORITHM_TUI_Flow.md
VALIDATION:      ./VALIDATION_TUI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
TEST:            ./TEST_TUI_Coverage.md
SYNC:            ./SYNC_TUI_State.md
```

---

## BEHAVIORS

### B1: Launch TUI

```
GIVEN:  User is in project with .ngram directory
WHEN:   User runs `ngram` (no subcommand)
THEN:   TUI launches with multi-column layout
AND:    Manager panel appears on left (~30% width)
AND:    Agent panel area appears on right
AND:    Input bar appears at bottom with prompt
AND:    Health score displays in status bar
```

### B2: Execute Slash Command

```
GIVEN:  TUI is running with input focus
WHEN:   User types `/repair` and presses Enter
THEN:   Repair session starts
AND:    Manager panel shows orchestration status
AND:    Agent panels show individual agent outputs
AND:    Input returns to prompt when complete
```

### B3: Run Doctor Command

```
GIVEN:  TUI is running
WHEN:   User types `/doctor` and presses Enter
THEN:   Health check runs
AND:    Results display in manager panel
AND:    Health score updates in status bar
```

### B4: Quit TUI

```
GIVEN:  TUI is running
WHEN:   User types `/quit` or presses Ctrl+C
THEN:   TUI exits gracefully
AND:    Control returns to terminal
```

### B5: Display Multiple Agents

```
GIVEN:  Repair session with multiple issues
WHEN:   Agents spawn for each issue
THEN:   Each agent gets its own column (up to 3)
AND:    If >3 agents, tabs appear for switching
AND:    Agent outputs stream in real-time
```

---

## INPUTS / OUTPUTS

### Primary Interface: Input Bar

**Inputs:**

| Input | Type | Description |
|-------|------|-------------|
| User text | string | Commands starting with `/` or natural language |
| Enter key | keypress | Submit input |
| Ctrl+C | keypress | Quit TUI |

**Outputs:**

| Output | Location | Description |
|--------|----------|-------------|
| Manager messages | Left panel | Orchestration status, decisions |
| Agent outputs | Right columns | Individual agent work streams |
| Health score | Status bar | Current project health 0-100 |
| Command feedback | Manager panel | Response to slash commands |

**Side Effects:**

- File system changes (repairs, doc updates)
- Project state changes (via repair agents)
- SYNC file updates

---

## EDGE CASES

### E1: No Issues Found

```
GIVEN:  User runs `/repair` but doctor finds no issues
THEN:   Manager panel shows "No issues to repair"
AND:    Input returns to prompt
```

### E2: Textual Not Installed

```
GIVEN:  User runs `ngram` but textual is not installed
THEN:   Helpful error message shows
AND:    Suggests: `pip install ngram[tui]`
```

### E3: Agent Timeout

```
GIVEN:  Agent runs for >10 minutes
THEN:   Agent is terminated
AND:    Manager panel shows timeout message
AND:    Other agents continue
```

### E4: Very Long Output

```
GIVEN:  Agent produces very long output
THEN:   Panel scrolls automatically
AND:    User can scroll back to review
```

---

## ANTI-BEHAVIORS

### A1: Never Block on Single Agent

```
GIVEN:   Multiple repair agents running
WHEN:    One agent takes long or fails
MUST NOT: Block other agents from running
INSTEAD:  Other agents continue independently
```

### A2: Never Lose Output

```
GIVEN:   Agent produces output
WHEN:    Output is longer than visible area
MUST NOT: Discard output or truncate silently
INSTEAD:  Buffer output, allow scrolling
```

### A3: Never Corrupt Terminal

```
GIVEN:   TUI exits (normal or crash)
WHEN:    Control returns to terminal
MUST NOT: Leave terminal in broken state
INSTEAD:  Reset terminal modes properly
```

### A4: Never Run Without Context

```
GIVEN:   User is outside project directory
WHEN:    User runs `ngram`
MUST NOT: Launch TUI in wrong context
INSTEAD:  Show error about missing .ngram directory
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Behavior when terminal resizes mid-session
- [ ] Behavior when agent produces binary/non-text output
- IDEA: History of previous commands (up arrow)
- IDEA: Tab completion for slash commands
- QUESTION: Should natural language input go to manager agent?
