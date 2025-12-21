# Physics — Implementation: Flows & Dependencies

```
STATUS: STABLE
UPDATED: 2025-12-21
```

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Physics.md
BEHAVIORS:      ../BEHAVIORS_Physics.md
ALGORITHMS:     ../ALGORITHM_Physics.md
VALIDATION:     ../VALIDATION_Physics.md
THIS:           IMPLEMENTATION_Physics_Flows_And_Dependencies.md (you are here)
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## physics_tick FLOW (METABOLISM)

1. Characters pump energy into narratives via BELIEVES/ABOUT links (`_flow_energy_to_narratives`).
2. Narrative energy transfers across RELATES_TO/SUPPORTS links (`_propagate_energy`).
3. Energy flows into moments (`ATTACHED_TO`, `CAN_SPEAK`), then clamps/decays (`_decay_energy`).
4. Salience is computed (weight × energy); `_detect_flips` surfaces events when thresholds cross.
5. Flip metadata returns to orchestrator to trigger handlers and canon.
6. Updates are persisted through `graph_ops` and reported to observers (events, health, display).

### Docking & Observability

- **start:** orchestrator calls GraphTick with elapsed time.
- **flip_output:** returns flip list for handler/canon scheduling.
- **health anchor:** `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` references the per-mechanism functions for monitoring.

## LOGIC CHAINS

- **Flip detection:** Tension/energy crosses threshold → `TickResult.flips` → orchestrator dispatch → handler output.
- **Action queue:** Action moment actualizes → queued by `process_actions` → updates graph (AT, possession, tension) → cascade occurs.
- **Drama cascade:** One actualization energizes witnesses → new flips follow (B8 behavior).

## MODULE DEPENDENCIES

- `engine/infrastructure/orchestration/orchestrator.py` → imports `engine/physics/tick.py` and `engine/moment_graph/queries.py`.
- `engine/physics/tick.py` → reads via `graph_queries.py`, writes via `graph_ops.py`, coordinates `graph_ops_events.py` for listeners.
- `engine/physics/graph/graph_ops.py` → composes mixins for attention split, PRIMES decay, contradiction pressure.
- `engine/physics/graph/graph_ops_read_only_interface.py` → consumed by Connectome search + GraphReadOps for seed queries.

### External packages

- `falkordb` for graph database access.
- `pydantic` for node/link models.
