# Physics — Implementation: Code Architecture

```
STATUS: STABLE
UPDATED: 2025-12-21
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Physics.md
BEHAVIORS:      ./BEHAVIORS_Physics.md
ALGORITHMS:     ./ALGORITHM_Physics.md
VALIDATION:     ./VALIDATION_Physics.md
THIS:           ./IMPLEMENTATION_Physics.md (you are here)
HEALTH:         ./HEALTH_Physics.md
SYNC:           ./SYNC_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics/IMPLEMENTATION_Physics_Code_And_Patterns.md
ARCHIVE:        ./archive/IMPLEMENTATION_Physics_archive_2025-12.md
```

---

## SUMMARY

The physics implementation story now lives inside the `IMPLEMENTATION_Physics/` folder so each document stays concise. The code-and-patterns doc captures the node/link schema, key modules, and architectural decisions. The flows doc walks through the tick metabolism, docking points, and module dependencies. The runtime doc describes state management, concurrency, configuration, and health-side links.

## ARCHIVE

- The previous canonical implementation doc is preserved at `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md` for reference and forensic detail.

## NEXT STEPS

- Keep this root as the entry point; update the linked fragments when new modules arrive.
