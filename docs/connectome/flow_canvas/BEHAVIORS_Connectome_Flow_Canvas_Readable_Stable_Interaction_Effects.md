```

# flow_canvas — Behaviors: Readability, Stability, and Navigation Effects

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md
THIS:            BEHAVIORS_Connectome_Flow_Canvas_Readable_Stable_Interaction_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_Connectome_Flow_Canvas_Layout_Zones_And_Edge_Label_Decluttering.md
VALIDATION:      ./VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md
HEALTH:          ./HEALTH_Connectome_Flow_Canvas_Runtime_Verification_Of_Render_Stability_And_Perf_Budgets.md
SYNC:            ./SYNC_Connectome_Flow_Canvas_Sync_Current_State.md
```

---

## OBJECTIVES SERVED

- Keep the entire Flow Canvas readable and stable even when the graph scales to thousands of nodes so the highlighted step and zone storytelling stay legible without flickering chaos.
- Anchor navigation cues, zone labeling, and focus pulses to the deterministic layout so the canvas becomes a single source of truth for the Connectome stepper rather than a transient debug view.

## INPUTS / OUTPUTS

### INPUTS

- `state_store.current_graph.nodes` and `.edges`, plus the computed `state_store.zones`, feed the zone renderers, edge shaders, and tooltip data so the canvas always reflects the canonical graph.
- `state_store.step_cursor`, `state_store.active_focus`, and `state_store.active_edge_ids` supply the stepper focus, glow pulses, and labels that keep navigation consistent with the ledger.

### OUTPUTS

- The canvas produces stable camera transforms, zone layers, and tooltip summaries that downstream overlays reuse to explain active steps, previews, and hover details without re-computing the graph.
- Panning, zooming, fit-to-view, and focus transitions emit deterministic layout snapshots and camera bounds that instrumentation or recordings can replay for debugging or tutorials.

## BEHAVIORS

### B1: Pan/zoom makes dense diagrams inspectable without shrinking labels to noise

```
GIVEN:  nodes are spaced further apart and labels remain readable
WHEN:   user pans and zooms
THEN:   user can inspect any node and edge label without losing context
AND:    reset/fit returns them to a known view
```

### B2: Zones make the system instantly legible

```
GIVEN:  FE/BE/GRAPH/AGENTS zones exist
THEN:   user can immediately identify which area each node belongs to
AND:    edges crossing zones feel meaningful rather than spaghetti
```

### B3: Stepper focus never causes edge disappearance

```
GIVEN:  user clicks Next repeatedly
THEN:   edges remain rendered and stable
AND:    only focus/glow/pulse changes
```

### B4: Hovering provides clarifying remarks without clutter

```
GIVEN:  user hovers a node or edge
THEN:   a tooltip displays payload summary, rate, and notes (including “?”)
AND:    the main map remains uncluttered
```

### B5: Fit-to-view restores orientation

```
GIVEN:  user pans/zooms far away
WHEN:   user clicks “fit”
THEN:   camera returns to a stable view framing the zone containers
```

---

## EDGE CASES

### E1: Window resize

```
GIVEN:  viewport resizes
THEN:   camera transform remains valid and edges do not vanish
AND:    layout remains stable (no random reflow)
```

---

## ANTI-BEHAVIORS

### A1: Force layout jitter in stepper mode

```
MUST NOT: nodes move around when stepping (breaks spatial memory)
INSTEAD: force layout is computed on graph changes only; stepper focus changes are visual only
```

### A2: Label overlap as default state

```
MUST NOT: edge labels overlap to the point of unreadability at 100% zoom
INSTEAD: label placement rules and spacing prevent collisions by default
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: should labels fade when zoomed out? (likely yes, but must be predictable)
* IDEA: show only active edge label when zoom < threshold

---

---
