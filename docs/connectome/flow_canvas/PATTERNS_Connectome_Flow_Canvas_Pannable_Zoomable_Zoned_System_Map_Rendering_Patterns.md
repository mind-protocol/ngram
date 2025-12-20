```

# flow_canvas — Patterns: Pannable/Zoomable Zoned Map with Stable Edge Readability

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
THIS:            PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md
VALIDATION:      ./VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
HEALTH:          ./HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md
```

### Bidirectional Contract

```
Before modifying this doc or the code:

1. Read ALL docs in this chain
2. Read event_model + state_store (canvas is a projection)

After modifying this doc:

* Update implementation OR record mismatch in SYNC

After modifying the code:

* Update docs OR record mismatch in SYNC

Never degrade:

* pan/zoom correctness
* edge label readability
* stable rendering (no disappearing edges)
  ```

---

## THE PROBLEM

The connectome diagram must function as a **debugging instrument**, not a poster.

The current failure modes (already observed):

* edges become unreadable (over-bold, overlapping labels)
* edges “disappear” during step transitions (resize/viewBox race)
* nodes are too close and visually ungrouped
* player vs UI vs hook nodes are not distinguishable
* no pan/zoom means you choose between “readable” and “fits on screen”

We need a canvas pattern that stays readable as complexity increases.

---

## THE PATTERN

**Zoned system map projection with deterministic layout and interactive camera.**

* “Zones” are explicit containers:

  * FRONTEND
  * BACKEND
  * GRAPH
  * AGENTS
* Nodes live inside zones; edges route across zones
* Camera supports:

  * pan
  * zoom
  * fit-to-view
  * reset view

Key insight:

> If the diagram is a projection of a ledger, layout must be stable and predictable.
> Force graphs are great for exploration but bad for deterministic debugging.

---

## PRINCIPLES

### Principle 1: Camera-first (pan/zoom) before layout cleverness

A readable diagram needs:

* space between nodes (no tight packing)
* pan/zoom to inspect without shrinking labels into noise
* “reset camera” to recover orientation

### Principle 2: Deterministic layout (not physics) for the main pipeline

The connectome “main data flow” is a system diagram:

* stable positions help users build mental models
* stepper mode relies on spatial memory

Force layout can exist as a secondary exploration mode later, but v1 should be deterministic.

### Principle 3: Label readability over style bravado

* link titles are NOT bold
* labels must remain readable at 100% zoom and not overwhelm nodes
* label background or halo should ensure contrast against edges

### Principle 4: Rendering stability is a correctness requirement

Edges must not disappear:

* no manual SVG viewBox recompute races
* stable edge objects keyed by id
* camera transforms must not detach edges from nodes

---

## DATA

| Data           | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| `nodes[]`      | UI nodes with positions and zone membership                              |
| `edges[]`      | Flow edges derived from FlowEvents (or a base map + active highlighting) |
| `active_focus` | which node/edge is active; glow persists                                 |
| `camera`       | x,y,zoom (view state)                                                    |
| `zones`        | FE/BE/GRAPH/AGENTS rectangles and labels                                 |

---

## DEPENDENCIES

| Module           | Why We Depend On It                                  |
| ---------------- | ---------------------------------------------------- |
| `state_store`    | provides nodes/edges list + active_focus             |
| `runtime_engine` | drives step releases that change active focus        |
| `edge_kit`       | provides edge types and visual components            |
| `node_kit`       | provides node renderers                              |
| `event_model`    | provides callType/trigger semantics used for styling |

---

## INSPIRATIONS

* React Flow / node editor UIs
* trace viewers with stable timelines
* “systems maps” with swimlanes (zones)

---

## SCOPE

### In Scope

* pannable/zoomable canvas camera behavior
* zone containers (visual grouping)
* deterministic layout strategy for v1
* label decluttering strategy (minimal but stable)
* fit-to-view + reset view controls

### Out of Scope

* node and edge styling details (owned by node_kit / edge_kit)
* log/explain panel (owned by log_panel)
* telemetry ingestion (owned by telemetry_adapter)
* health invariants for backend truth (not owned here)

---

## PATTERNS USED (SUB-PATTERNS)

### P1: Zoned containers as “semantic declutter”

Zones reduce cognitive load:

* users can instantly locate FE vs BE vs GRAPH vs AGENTS
* edges crossing zones become meaningful and easier to read

### P2: Stable keying and memoization of graph elements

Nodes and edges must be keyed by stable ids:

* node id: stable module/entity id
* edge id: stable link id (from FlowEvent or base map)

### P3: Layering: edges above nodes (but interaction-friendly)

* edges visually on top (as requested)
* but must still allow node interaction
* solution: edges in a higher visual layer with pointer events carefully controlled

---

## ENTRY POINTS

| Entry                                                         | Purpose                                                  |
| ------------------------------------------------------------- | -------------------------------------------------------- |
| `render_connectome_canvas(nodes, edges, zones, active_focus)` | projection render                                        |
| `set_camera_pan_zoom(new_state)`                              | camera updates                                           |
| `fit_view_to_zones()`                                         | reset/fit                                                |
| `on_node_click(node_id)`                                      | interacts with runtime (player message, pin focus, etc.) |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### canvas_renders_store_projection

```
flow:
name: canvas_renders_store_projection
purpose: Render stable map from store state.
steps:
- read nodes/edges/zones/active_focus from store selectors
- render zones first
- render nodes and edges with stable keys
- apply active_focus glow persistence
- apply camera transform
docking_points:
- dock_canvas_render_commit (event): used by HEALTH for “no disappearing edges”
```

---

## GAPS / IDEAS / QUESTIONS

* [ ] Confirm whether we lock node positions in code or compute via a lightweight layout algorithm (recommended: fixed for v1).
* IDEA: optional “declutter toggle” hides secondary labels until zoom > threshold.
* QUESTION: do we need minimap in v1? (nice-to-have)

---

---
