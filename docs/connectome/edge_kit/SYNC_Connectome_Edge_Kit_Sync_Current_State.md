```

# edge_kit — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* strict trigger→dash mapping
* strict call_type→color mapping
* labels not bold, readable with halo
* stream edges have gentle directional animation
* pulses stop at node boundaries
* active edge persists until next step

**In design:**

* graphLink subtype tint (ABOUT vs THEN yellow/orange)
* arrowhead policy (hover only)

---

## CURRENT STATE

Docs defined; implementation not started.

Immediate priorities:

* implement edge render components
* implement directional shine (especially for stream)
* implement pulse boundary clamps

---

## TODO

* [ ] implement edge components in edge_kit folder
* [ ] implement style tokens and mapping tables
* [ ] implement geometry clamp helper for pulse endpoints (coordinate with flow_canvas)
* [ ] add edge_kit health checks

Run:

```
pnpm connectome:health edge_kit
```

---

---
