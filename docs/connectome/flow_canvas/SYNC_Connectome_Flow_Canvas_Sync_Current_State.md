```

# flow_canvas — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* pannable/zoomable system map
* zones FE/BE/GRAPH/AGENTS
* deterministic layout
* stable edge rendering (no disappearance)

**In design:**

* label declutter heuristic thresholds
* minimap and drag behavior (likely defer)

**Deferred:**

* force layout exploration mode (separate view)

---

## CURRENT STATE

Docs defined; no implementation yet. This module exists because manual SVG edge rendering caused readability and stability failures. The plan is to use a stable canvas framework (e.g., React Flow) with deterministic positions and stable keyed elements.

---

## RECENT CHANGES

### 2025-12-20: Initialized flow_canvas chain docs

* added zones and camera behaviors
* specified deterministic layout and label decluttering

---

## TODO

* [ ] Implement FlowCanvas with pan/zoom and zones
* [ ] Implement stable node layout positions with wide spacing
* [ ] Implement stable edge label placement with minimal declutter
* [ ] Add flow_canvas health harness to detect edge disappearance

Run:

```
pnpm connectome:health flow_canvas
```

---

## HANDOFF

**For agents:**

* Do not implement force layout in v1 main view
* Ensure edges are keyed and never re-created with new ids on each render

**For human:**

* Decide whether to allow node dragging in v1 (recommended: no)

---

---
