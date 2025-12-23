# Physics — Current State

```
STATUS: DESIGNING (v1.2)
UPDATED: 2025-12-23
```

## MATURITY

STATUS: DESIGNING. Schema v1.1 Energy Physics spec is complete and validated via simulation. Implementation pending.

What's canonical (v1.0):
- Core physics tick, graph ops, health checks

What's being designed (v1.1):
- Unified flow formula (no speaker/witness special cases)
- Moment lifecycle states (possible → active → completed/rejected/interrupted/overridden)
- Path resistance via Dijkstra (conductivity-based, not hops)
- Link crystallization (shared moments create relationships)
- Narrative backflow
- Liquidation on completion

## CURRENT STATE

**v1.1 Spec:** `algorithms/ALGORITHM_Physics_Schema_v1.1_Energy_Physics.md` — complete, simulation-validated

**Key v1.1 changes:**
- Unified formula: `flow = source.energy × rate × conductivity × weight × emotion_factor`
- No special cases for speaker/witness — link properties determine everything
- Emotion proximity baseline: 0.2 (not 0.5)
- No energy_capacity — decay handles runaway energy naturally

Physics documentation follows the standard chain (patterns, behaviors, implementation, validation, health). Implementation is consolidated into a single comprehensive document for better maintainability and consistency.

## RECENT CHANGES

### 2025-12-23: v1.2 Validation & Health Checker Infrastructure

- Created `docs/physics/VALIDATION_Energy_Physics.md` — 19 validation IDs covering energy conservation, link state, tick execution, moment lifecycle, generation/proximity, top-N filter, backflow, crystallization, emotions
- Created `docs/physics/HEALTH_Energy_Physics.md` — Health indicators, docking points, checker index, throttling strategies
- Implemented health checker CLI: `python -m engine.physics.health.checker`
- Created checker infrastructure:
  - `engine/physics/health/base.py` — BaseChecker with HealthStatus enum
  - `engine/physics/health/checker.py` — CLI entry point, run_all_checks()
  - `engine/physics/health/checkers/energy_conservation.py` — V-ENERGY-BOUNDED, V-ENERGY-CONSERVED
  - `engine/physics/health/checkers/no_negative.py` — V-ENERGY-NON-NEGATIVE
  - `engine/physics/health/checkers/link_state.py` — V-LINK-ALIVE, V-LINK-BOUNDED
  - `engine/physics/health/checkers/tick_integrity.py` — V-TICK-ORDER, V-TICK-COMPLETE
  - `engine/physics/health/checkers/moment_lifecycle.py` — V-MOMENT-TRANSITIONS

### 2025-12-23: Schema v1.1 Spec Complete

- Created `algorithms/ALGORITHM_Physics_Schema_v1.1_Energy_Physics.md` with full spec
- Unified flow formula replaces speaker/witness special cases
- Moment lifecycle: possible → active → completed/rejected/interrupted/overridden
- Path resistance via Dijkstra (conductivity × weight × emotion_factor)
- Link crystallization, narrative backflow, liquidation on completion
- Validated via `diffusion_sim_v2.py`

### 2025-12-21: Implementation Consolidation

- Consolidated `docs/physics/IMPLEMENTATION_Physics/` fragments back into `docs/physics/IMPLEMENTATION_Physics.md` to reduce duplication and improve context density.
- Removed redundant implementation fragments: `IMPLEMENTATION_Physics_Runtime.md`, `IMPLEMENTATION_Physics_Code_And_Patterns.md`, and `IMPLEMENTATION_Physics_Flows_And_Dependencies.md`.
- Maintained the behavior and validation fragment structures as established in previous iterations.

## KNOWN ISSUES

- Handler runtime and speed controller wiring are pending and tracked in the archive sync/pattern notes.

## ARCHIVE REFERENCES

- `docs/physics/archive/SYNC_Physics_archive_2025-12.md` holds the 2025-12 detailed changelog and diagnostics.
- `docs/physics/archive/SYNC_archive_2024-12.md` preserves the prior year snapshot for traceability.

## HANDOFF NOTES

Consolidation of implementation docs complete. Future updates should be made directly to `docs/physics/IMPLEMENTATION_Physics.md`. Maintain the single-file structure unless the implementation details exceed 500+ lines.
