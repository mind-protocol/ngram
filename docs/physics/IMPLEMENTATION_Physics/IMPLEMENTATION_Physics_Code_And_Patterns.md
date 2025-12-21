# Physics — Implementation: Code & Patterns

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
THIS:           IMPLEMENTATION_Physics_Code_And_Patterns.md (you are here)
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## CODE STRUCTURE SNAPSHOT

- `engine/physics/tick.py`: GraphTick pump/propagate/decay loop, flip detection, energy clamps.
- `engine/physics/graph/graph_queries.py`: Read façade used by the tick and traversal layers.
- `engine/physics/graph/graph_ops.py`: Mutation façade plus mixins (attention split, PRIMES decay, contradiction pressure).
- `engine/physics/graph/graph_ops_read_only_interface.py`: Connectome-friendly read helpers (GraphReadOps) pulled into separate module.
- `engine/moment_graph/*`: Queries + traversal helpers for click/wait interactions.
- `engine/models/*`: Pydantic base models for moments, links, narratives, etc.

The tick is the orchestrator; it does not store state beyond an ephemeral context.

## FILE RESPONSIBILITIES (HIGHLIGHT)

| Artifact | Purpose | Owner | Status |
|----------|---------|-------|--------|
| `engine/physics/tick.py` | Tick metabolism and flip detection | GraphTick | WATCH (430+ lines)
| `graph_queries.py` | Read queries | GraphQueries | SPLIT (under 700 lines)
| `graph_ops.py` | Write commands | GraphOps + mixins | SPLIT (under 700 lines)
| `graph_ops_read_only_interface.py` | Search/seed reader | GraphReadOps | OK
| `moment_graph/traversal.py` | Interaction handling | Click traversal | OK

## DESIGN PATTERNS

- **Graph-first orchestration:** GraphTick reads/writes the graph; all state lives there.
- **Query/Command separation:** `graph_queries` vs `graph_ops` keeps reads and writes distinct.
- **Facades + mixins:** GraphOps composes command mixins (attention split, PRIMES, contradictions) so plumbing stays composable.
- **Observer/Events:** `graph_ops_events.py` emits hooks for downstream listeners without inlining the logic.

### Anti-patterns to avoid

- Hidden writes in query helpers.
- Stateful orchestrators that cache moment state instead of always querying the graph.

## SCHEMA & ENTRYPOINTS

- **Moment node:** `id`, `text`, `type`, `status`, `weight`, `energy`.
- **Links:** BELIEVES, ATTACHED_TO, CAN_SPEAK, THEN, etc.

Entry points:
- Physics tick: `engine/physics/tick.py:run()` invoked by the orchestrator.
- Click traversal: `engine/moment_graph/traversal.py:handle_click()`.
- Player input: `engine/infrastructure/api/moments.py`.
