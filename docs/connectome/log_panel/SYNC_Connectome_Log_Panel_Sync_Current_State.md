```

# log_panel — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* unified “Now + Ledger” panel
* duration coloring rules exactly as specified
* trigger and call_type badges
* copy/export is derived exclusively from store ledger

**In design:**

* filters and search (deferred)
* export format details (session header yes/no)

---

## CURRENT STATE

Docs defined; implementation not started.

Immediate priorities:

* implement panel layout with Now section and ledger list
* implement deterministic duration color rules
* implement copy/export buttons integrated with store serializers

---

## TODO

* [ ] Implement log_panel TSX component
* [ ] Implement duration formatting + coloring helper
* [ ] Implement export serializers (JSONL + text)
* [ ] Add log_panel health harness

Run:

```
pnpm connectome:health log_panel
```

---

---
