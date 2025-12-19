# ngram Framework — Implementation: File Structure

```
STATUS: STABLE
CREATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ../BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ../ALGORITHM_Overview.md
VALIDATION:      ../VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Overview.md
THIS:            ./IMPLEMENTATION_File_Structure.md
TEST:            ../TEST_Protocol_Test_Cases.md
SYNC:            ../SYNC_Protocol_Current_State.md
```

---

## PURPOSE

This document isolates the canonical file paths referenced by the protocol implementation.
See `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Overview.md` for the full implementation narrative.

---

## FILE STRUCTURE REFERENCES

### Installed Directory (Target Project)

```
.ngram/
├── PROTOCOL.md
├── PRINCIPLES.md
├── views/
├── templates/
├── modules.yaml
├── state/
│   ├── SYNC_Project_State.md
│   └── SYNC_Project_Health.md
└── traces/
```

### Bootstrap Files

- `.ngram/CLAUDE.md` — primary bootstrap entrypoint for agents
- `AGENTS.md` — repo root mirror of `.ngram/CLAUDE.md`
- `.ngram/agents/manager/AGENTS.md` — manager role bootstrap

