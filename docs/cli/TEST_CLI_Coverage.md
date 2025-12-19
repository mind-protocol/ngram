# ngram Framework CLI — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
THIS:            TEST_CLI_Coverage.md (you are here)
SYNC:            ./SYNC_CLI_State.md
```

---

## TEST STRATEGY

The CLI module currently lacks automated tests. Testing is performed manually through CLI usage and repair agent execution. This document tracks what should be tested and current coverage gaps.

**Testing philosophy:**
- Commands should be tested in isolation first
- Integration tests should verify end-to-end flows
- Agent tests require mocking agent subprocess (claude or codex)

---

## UNIT TESTS (0% coverage)

**None automated.** Planned tests per command:

- **Init:** protocol dir creation, .ngram/CLAUDE.md + AGENTS.md update (includes Codex addition), force overwrite, duplicate prevention
- **Validate:** healthy project pass, missing protocol fail, broken chain detection
- **Doctor:** monolith detection, undocumented detection, stale sync, score calculation
- **Repair:** agent spawning, depth filtering, max limit, dry-run, parallel execution

---

## INTEGRATION TESTS (0% coverage)

**Planned integration tests:**
- Init → Validate cycle (protocol installation verified)
- Doctor → Repair cycle (health score improves)
- Context navigation (DOCS: references resolve)

---

## EDGE CASES (manual only)

Empty project, large codebase (1000+ files), missing YAML dependency, agent timeout, broken templates, unicode paths.

---

## TEST COVERAGE

**Overall: 0% automated test coverage** across all modules (cli, init_cmd, validate, doctor, repair, sync, context, utils).

---

## HOW TO RUN

```bash
# Currently no automated tests exist
# Manual testing commands:

# Test init
ngram init --dir /tmp/test-project
ngram validate --dir /tmp/test-project

# Test doctor
ngram doctor --no-github

# Test repair (dry run)
ngram repair --dry-run --max 3

# Test context
ngram context ngram/cli.py
```

---

## KNOWN TEST GAPS

- [ ] No unit tests for any module
- [ ] No integration tests
- [ ] No property-based tests
- [ ] No CI/CD test pipeline
- [ ] No mocking infrastructure for agent subprocess
- [ ] No test fixtures for project structures

---

## PROPOSED TEST STRUCTURE

```
tests/
├── conftest.py           # Shared fixtures
├── fixtures/
│   ├── healthy_project/  # Project passing all checks
│   ├── broken_project/   # Project with various issues
│   └── templates/        # Test template files
├── unit/
│   ├── test_init.py
│   ├── test_validate.py
│   ├── test_doctor.py
│   ├── test_repair.py
│   └── test_utils.py
└── integration/
    ├── test_full_cycle.py
    └── test_context_flow.py
```

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| (none yet) | — | — | — |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Set up pytest infrastructure
- [ ] Create test fixtures for common project states
- [ ] Add CI/CD with GitHub Actions
- [ ] Consider snapshot testing for CLI output
- IDEA: Use hypothesis for property-based testing
- IDEA: Mock agent subprocess for repair tests
- QUESTION: Should we test against real Claude or always mock?
