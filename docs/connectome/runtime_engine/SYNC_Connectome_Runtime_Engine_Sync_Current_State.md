```

# runtime_engine — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* stepper: Next releases exactly one event, speed never autoplays
* min duration clamp 200ms

**In design:**

* restart policy (clear ledger vs session boundary)
* realtime mode buffering (deferred)

**Deferred:**

* realtime adapter wiring
* buffering policy and retention

---

## CURRENT STATE

runtime_engine docs are defined; implementation does not exist yet. The engine is explicitly separated from state_store (storage) and from rendering (flow_canvas, node_kit, edge_kit).

---

## IN PROGRESS

### Stepper engine scaffolding

* Status: not implemented
* Next: implement command dispatch + step release using event_model normalization

---

## RECENT CHANGES

### 2025-12-20: Initialized runtime_engine chain docs

* Defined gating semantics and invariants
* Defined health checks that detect autoplay leaks

---

## KNOWN ISSUES

### Realtime ambiguity

* Issue: realtime ordering + buffering policy not decided
* Impact: telemetry_adapter + runtime_engine realtime mode cannot be finalized
* Current handling: deferred; marked `?`

---

## HANDOFF: FOR AGENTS

* Start at IMPLEMENTATION doc: create files with long descriptive names
* Ensure event_model is imported; do not duplicate normalization
* Ensure speed change does NOT schedule timers in stepper mode

---

## HANDOFF: FOR HUMAN

* V1 decision needed: Restart clears ledger or creates session boundary?
* V1 can ship without realtime

---

## TODO

### Doc/Impl Drift

* [ ] Implement runtime_engine per ALGORITHM
* [ ] Add health harness that can observe ledger/cursor deltas

### Tests to Run

```
pnpm connectome:health runtime_engine
```

### Immediate

* [ ] Build step script interface used by simulator
* [ ] Implement release_next_step with min duration clamp

### Later

* [ ] Realtime buffering and drain policy
* [ ] “Step back” support

---

## CONSCIOUSNESS TRACE

* Key risk: accidentally implementing autoplay via speed timers
* Key invariant: authorization is Next button only (stepper)

---

## POINTERS

| Item                   | Location                             |
| ---------------------- | ------------------------------------ |
| FlowEvent contract     | docs/connectome/event_model/* |
| Step gating invariants | VALIDATION file in this module       |

---

---
