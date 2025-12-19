# ngram TUI — Test: Test Strategy and Coverage

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
IMPLEMENTATION:  ./IMPLEMENTATION_TUI_Code_Architecture.md
THIS:            TEST_TUI_Coverage.md (you are here)
SYNC:            ./SYNC_TUI_State.md
```

---

## TEST STRATEGY

Testing a TUI presents unique challenges:
1. **Async nature** — Textual uses async/await throughout
2. **Visual output** — Hard to assert on rendered appearance
3. **Subprocess interaction** — Agents are external processes
4. **Terminal state** — Need real terminal for some tests

**Approach:**
- **Unit tests** for pure functions (command parsing, state management)
- **Integration tests** using Textual's test framework (`App.run_test()`)
- **Manual smoke tests** for visual and terminal state verification

---

## UNIT TESTS

### Command Parsing

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_parse_repair` | `/repair` | `SlashCommand("repair", [])` | PENDING |
| `test_parse_repair_args` | `/repair --max 5` | `SlashCommand("repair", ["--max", "5"])` | PENDING |
| `test_parse_doctor` | `/doctor` | `SlashCommand("doctor", [])` | PENDING |
| `test_parse_quit` | `/quit` | `SlashCommand("quit", [])` | PENDING |
| `test_parse_unknown` | `/foo` | `SlashCommand("foo", [])` | PENDING |
| `test_parse_natural` | `hello` | raw string | PENDING |

### State Management

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| `test_add_agent` | `SessionState.add_agent(handle)` | Agent in list | PENDING |
| `test_remove_agent` | `SessionState.remove_agent(id)` | Agent removed | PENDING |
| `test_health_bounds` | Various scores | Always 0-100 | PENDING |

---

## INTEGRATION TESTS

### App Launch

```
GIVEN:  Textual app created
WHEN:   app.run_test() called
THEN:   All widgets mounted
AND:    Manager panel visible
AND:    Input bar focused
STATUS: PENDING
```

### Slash Command Execution

```
GIVEN:  App running in test mode
WHEN:   Simulated /help command
THEN:   Help text appears in manager panel
STATUS: PENDING
```

### Agent Panel Creation

```
GIVEN:  App running
WHEN:   Mock repair started with 2 issues
THEN:   2 agent panels created
AND:    Output streams to correct panels
STATUS: PENDING
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Empty input (just Enter) | Verify no crash, no action | PENDING |
| Very long command | Verify handled gracefully | PENDING |
| Rapid repeated commands | Verify no race conditions | PENDING |
| Quit during repair | Verify agents terminated | PENDING |
| Resize during render | Verify layout adjusts | PENDING |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| `commands.py` | 0% | Implementation pending |
| `state.py` | 0% | Implementation pending |
| `app.py` | 0% | Implementation pending |
| `widgets/*` | 0% | Implementation pending |

**Target:** 80% coverage for pure functions, 60% for widget code

---

## HOW TO RUN

```bash
# Once tests exist:
pytest tests/tui/

# Run specific test file
pytest tests/tui/test_commands.py

# Run with coverage
pytest tests/tui/ --cov=ngram.tui --cov-report=html

# Run only unit tests (fast)
pytest tests/tui/ -m "not integration"

# Run integration tests
pytest tests/tui/ -m "integration"
```

---

## KNOWN TEST GAPS

- [ ] No tests yet — implementation pending
- [ ] Need mock for Claude CLI subprocess
- [ ] Need strategy for testing terminal restoration
- [ ] Need strategy for testing with real terminal vs headless

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| — | — | No tests yet | — |

---

## TEST INFRASTRUCTURE NEEDED

### Mocks

```python
# Mock for agent subprocess
class MockAgentProcess:
    """Simulates agent without actually running it."""
    async def stream_output(self):
        yield "Starting repair..."
        yield "REPAIR COMPLETE"
```

### Fixtures

```python
@pytest.fixture
def app():
    """Create test app instance."""
    return NgramApp()

@pytest.fixture
def session_state():
    """Create fresh session state."""
    return SessionState()
```

### Test Utilities

```python
async def send_command(app, command: str):
    """Simulate user typing a command."""
    await app.pilot.type(command)
    await app.pilot.press("enter")
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Textual has its own test framework — evaluate `App.run_test()`
- [ ] Consider snapshot testing for widget rendering
- IDEA: Record/replay tests for complex interactions
- IDEA: Use pytest-asyncio for async test support
- QUESTION: How to test CSS styling? Visual regression?
