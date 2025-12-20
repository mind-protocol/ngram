```

# flow_canvas — Validation: Invariants for Readability and Render Stability

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md
THIS:            VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
HEALTH:          ./HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md
```

---

## INVARIANTS

### V1: Pan/zoom always keeps nodes and edges coherent

```
When camera changes:
node positions update consistently
edge endpoints remain attached (no drifting)
no edges disappear
```

### V2: Deterministic layout under stepper changes

```
Given identical node list and zone layout:
node positions do not change when stepping
only styling changes (active focus)
```

### V3: Label readability at 100% zoom

```
At zoom=1.0:
label font size >= minimum readable threshold (>=12px)
labels do not overlap more than acceptable threshold (policy)
```

### V4: Zones render behind nodes and edges consistently

```
Zones do not occlude edges and labels
Zones remain visible as grouping structure
```

---

## ERROR CONDITIONS

### E1: Edge vanishes during step transition

* severity: ERROR
* meaning: canvas render stability is broken (unacceptable for debugging)

### E2: Label collisions make data unreadable

* severity: WARN
* meaning: declutter policy needs improvement or node spacing too tight

---

## HEALTH COVERAGE

| Validation | Health Indicator                                |
| ---------- | ----------------------------------------------- |
| V1         | canvas_edge_attachment_and_visibility_integrity |
| V2         | canvas_layout_determinism_integrity             |
| V3         | canvas_label_readability_sampling               |
| E1         | canvas_edge_disappearance_detector              |

---

## VERIFICATION PROCEDURE

### Manual

```
[ ] Step repeatedly → no edges disappear
[ ] Resize window → no edges disappear
[ ] Zoom in/out → labels remain readable at zoom=1.0
[ ] Fit-to-view → zones frame correctly
```

### Automated (conceptual)

```
pnpm connectome:health flow_canvas
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: define measurable label overlap threshold for v1 health checks (pixel-based sampling?).

---

---
