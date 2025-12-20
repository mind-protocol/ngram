# ngram Framework CLI — Algorithm: Command Processing Logic (Overview)

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ../BEHAVIORS_CLI_Command_Effects.md
THIS:            ALGORITHM_Overview.md
VALIDATION:      ../VALIDATION_CLI_Instruction_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md
HEALTH:          ../HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ../SYNC_CLI_Development_State.md
```

---

## OVERVIEW

The CLI follows a simple dispatch pattern: parse arguments, route to a command module, execute, and return an exit code. The most complex flows are `doctor` (health analysis) and `repair` (agent orchestration); the newest addition, `ngram refactor`, keeps documentation paths and modules.yaml entries coherent when refactors happen.

**Algorithm sections:**
- `ALGORITHM_Init_And_Validate.md`
- `ALGORITHM_Doctor_And_Repair.md`
- `ALGORITHM_Markers_And_Support.md`
- `ALGORITHM_Refactor_Command.md`
- `ALGORITHM_Docs_Fix_Command.md`

---

## DATA STRUCTURES

See `../IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Schema.md` for full type definitions:
- `ValidationResult`
- `DoctorIssue`
- `RepairResult`

---

## DATA FLOW (SUMMARY)

```
User Command
    ↓
argparse (cli.py)
    ↓
Command Router (cli.py:main)
    ↓
Command Module (e.g., doctor.py)
    ↓
Health/Validation/Repair Logic
    ↓
Output (stdout + files)
```

---

## PERFORMANCE NOTES

- `doctor` and `repair` are the heaviest commands due to repo scans and agent execution.
- Parallel repair agent output is serialized with a print lock to avoid interleaving.
