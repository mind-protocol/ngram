# Physics — Implementation: Runtime & Health

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
THIS:           IMPLEMENTATION_Physics_Runtime.md (you are here)
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## STATE MANAGEMENT

- **Graph state:** Lives in FalkorDB (`Moment`, `Link`, `Narrative` nodes). No cached state outside the graph.
- **Active tensions:** Derived from contradictions/demands; persist as relationships, not dedicated nodes.
- **Energy:** Stored on node properties; decays each tick.

## RUNTIME BEHAVIOR

- Orchestrator calls `GraphTick.run()` with elapsed time; tick returns flips.
- Handlers (planned) consume flips to generate potentials; canon holder records `THEN` links.
- Speed controller (planned) adjusts display speed while canon chain stays invariant.

## CONCURRENCY & CONFIG

- Physics tick runs synchronously; energy math is linear.
- Handlers execute asynchronously (LLM calls) but writing occurs sequentially through graph ops.
- Configs: `DECAY_RATE`, `BELIEF_FLOW_RATE` stored in `engine/physics/constants.py`.

## BIDIRECTIONAL LINKS

- Code → docs: tick, display snaps, cluster monitors point to `docs/physics/PATTERNS_Physics.md`/`ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md`.
- Docs → code: ALGORITHM steps map to `_flow_energy_to_narratives`, `_decay_energy`, `_detect_flips`.

## GAPS / PROPOSITIONS

- Handler runtime wiring still pending (captured in SYNC).
- Speed controller and canon holder integrations remain future work increments.

## RUNTIME PATTERNS

- **Scene as query:** Scenes are query results, not objects.
- **Time passage:** `advance_time(minutes)` called on spoken moments to drive ticks.
- **Character movement:** Travel moments update `AT` links and spawn consequence moments.
