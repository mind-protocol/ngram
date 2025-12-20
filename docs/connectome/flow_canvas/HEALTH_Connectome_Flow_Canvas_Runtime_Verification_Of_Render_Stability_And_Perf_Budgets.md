```

# flow_canvas — Health: Render Stability and Performance Budget Checks

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file ensures the canvas remains a usable diagnostic tool as the diagram grows:

* no disappearing edges
* layout determinism under stepping
* basic performance budgets (frame time and rerender counts) (lightweight)

It does not validate aesthetics in detail (colors/glows are edge_kit/node_kit).

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md
VALIDATION:      ./VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
THIS:            HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md

IMPL:            ? (planned) scripts/connectome/health/flow_canvas_health_check_runner.ts
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: canvas_stepper_render_updates
  purpose: ensure stepping never hides edges
  triggers:

  * type: manual
    source: runtime_engine Next click
    frequency:
    expected_rate: "human driven"
    peak_rate: "rapid clicking"
    risks:
  * "edge disappearance"
  * "layout jitter"
  * "label collisions"
    notes: "edge disappearance is the primary v1 failure"

* flow_id: canvas_camera_changes
  purpose: ensure pan/zoom never detaches edges
  triggers:

  * type: manual
    source: pan/zoom gestures + fit-to-view
    frequency:
    expected_rate: "frequent during use"
    risks:
  * "edge endpoint drift"
  * "label misplacement"
    ```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: canvas_edge_disappearance_detector
  flow_id: canvas_stepper_render_updates
  priority: high
  rationale: "If edges vanish, the instrument is broken."

* name: canvas_layout_determinism_integrity
  flow_id: canvas_stepper_render_updates
  priority: high
  rationale: "No node jitter during stepping."

* name: canvas_edge_attachment_and_visibility_integrity
  flow_id: canvas_camera_changes
  priority: high
  rationale: "Pan/zoom must not break attachment."
  ```

---

## CHECKER INDEX

```
checkers:

* name: health_check_edges_present_after_each_step
  purpose: "After each step release, assert all expected edge ids are still rendered."
  status: pending
  priority: high

* name: health_check_node_positions_stable_under_stepper
  purpose: "Assert node positions unchanged while stepping."
  status: pending
  priority: high

* name: health_check_edge_endpoints_attach_to_node_bounds
  purpose: "Sample endpoints and assert they are within tolerance of node bounds."
  status: pending
  priority: high
  ```

---

## HOW TO RUN

```
pnpm connectome:health flow_canvas
```

---

## KNOWN GAPS

* [ ] requires an implementation-level probe to detect “rendered edges” (React Flow hook or test harness)
* [ ] label overlap measurement not defined yet

---

## GAPS / IDEAS / QUESTIONS

* IDEA: instrument render counts per step and warn if too many rerenders
* QUESTION: do we define a frame budget threshold now (e.g., 16ms) or defer?

---

---
