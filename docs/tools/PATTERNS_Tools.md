# Tools — Patterns: Utility Scripts

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
THIS:            docs/tools/PATTERNS_Tools.md
BEHAVIORS:       ./BEHAVIORS_Tools.md
ALGORITHM:       ./ALGORITHM_Tools.md
VALIDATION:      ./VALIDATION_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tools.md
HEALTH:          ./HEALTH_Tools.md
SYNC:            ./SYNC_Tools.md
```

---

## THE PROBLEM

Utility scripts are easy to lose track of without documentation, which makes it harder to reuse them and keep them aligned with the rest of the protocol.

## THE PATTERN

Treat `tools/` as a small, documented module. Each script stays lightweight, but the module captures intent, ownership, and guardrails.
