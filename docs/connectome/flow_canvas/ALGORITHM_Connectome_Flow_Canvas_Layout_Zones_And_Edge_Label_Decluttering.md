```

# flow_canvas — Algorithm: Zones, Layout, and Label Decluttering

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md
THIS:            ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md (you are here)
VALIDATION:      ./VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
HEALTH:          ./HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md
```

---

## OVERVIEW

The canvas renders a stable projection:

* zones are rectangles with titles
* nodes are positioned inside zones deterministically
* edges route between nodes with stable ids
* label placement is consistent and avoids overlap as much as possible

---

## DATA STRUCTURES

### `ZoneLayout`

```
ZoneLayout:
zone_id: FRONTEND|BACKEND|GRAPH|AGENTS
x: number
y: number
width: number
height: number
title: string
```

### `NodeLayout`

```
NodeLayout:
node_id: string
zone_id: ZoneLayout.zone_id
x: number
y: number
width: number
height: number
```

### `EdgeLayout`

```
EdgeLayout:
edge_id: string
from_node_id: string
to_node_id: string
label_anchor: {x,y}
route: polyline|bezier (implementation choice)
```

---

## ALGORITHM: `compute_zone_layout(viewport)`

V1 deterministic zone coordinates:

```
FRONTEND: x=40,  y=40,  w=420, h=520
BACKEND:  x=520, y=40,  w=520, h=720
GRAPH:    x=1080,y=40,  w=420, h=520
AGENTS:   x=1080,y=600, w=420, h=260
```

These are tuned for readability and spacing; they scale with viewport.

---

## ALGORITHM: `place_nodes_within_zones(nodes, zones)`

* each node has a preferred slot (row/column)
* spacing constant ensures “nodes more far away”

```
slot_spacing_x = 260
slot_spacing_y = 180
node_padding   = 24
```

Place nodes by:

* zone_id grouping
* stable ordering by node_id or explicit “pipeline order” list

---

## ALGORITHM: `route_edges_and_place_labels(edges, node_layouts)`

Edge routing choice for v1:

* bezier curves with consistent curvature direction
* label anchored at 55% of curve length
* label background halo provided by edge_kit (render concern)

Label declutter heuristic (v1 minimal, stable):

* if two labels are within radius R, offset the newer one by (+0, +18) repeatedly up to 3 times
* if still colliding: mark `label_visibility="active_only"` when zoomed out (policy)

---

## ALGORITHM: `apply_camera_transform(camera, world_coords)`

* camera: {pan_x, pan_y, zoom}
* world→screen transform applied by rendering library

Must preserve:

* stable edge endpoints at node boundaries
* no viewBox recompute races

---

## COMPLEXITY

* layout compute: O(n + m)
* collision offset: O(m) with small constant factor

---

## GAPS / IDEAS / QUESTIONS

* IDEA: use dagre layout for v2 but pin main pipeline nodes
* QUESTION: do we allow user to drag nodes? (v1: no, to preserve determinism)

---

---
