```

# state_store — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* one store owns ledger + focus + timers + explanation
* atomic commit per step release
* append-only ledger within a session

**In design:**

* restart policy (clear vs boundary)
* realtime retention policy (max N vs time window)

**Deferred:**

* realtime ingestion details
* pinned focus behavior

---

## CURRENT STATE

state_store docs are defined; implementation does not exist yet. This module is the intended single authority to prevent “links disappear” and “log/explain drift” bugs.

---

## RECENT CHANGES

### 2025-12-20: Initialized state_store chain docs

* Defined append-only ledger + atomic commit semantics
* Defined wait timer and tick display signals as store-owned semantics

---

## KNOWN ISSUES

### Restart policy unresolved

* Issue: whether restart clears ledger or starts a new session boundary
* Impact: affects export format and determinism
* Current handling: documented as A/B, must be decided and locked

---

## HANDOFF: FOR AGENTS

* Implement in Zustand with explicit long action names
* Ensure each Next release is one atomic action (append+focus+explain)
* Do not allow components to keep shadow copies of ledger/focus

---

## HANDOFF: FOR HUMAN

* Please decide: Restart clears ledger OR creates a boundary (prefer boundary for auditability)
* Please decide retention policy for realtime mode (cap N vs time window)

---

## TODO

* [ ] Implement store state + actions with long descriptive filenames
* [ ] Implement export function used by log_panel
* [ ] Add state_store health runner (pending)

Run:

```
pnpm connectome:health state_store
```

---

---
