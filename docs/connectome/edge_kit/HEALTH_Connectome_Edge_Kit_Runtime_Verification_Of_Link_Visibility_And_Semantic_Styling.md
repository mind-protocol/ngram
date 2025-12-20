```

# edge_kit — Health: Link Visibility and Semantic Styling Verification

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

edge_kit HEALTH ensures links do not lie or vanish:

* correct dash for trigger
* correct color for call type
* labels readable and not bold
* pulses obey min duration and boundary clamps
* active edge persistence

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Edge_Kit_Edge_Rendering_Pulse_Shine_And_Label_Placement_Rules.md
VALIDATION:      ./VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md
THIS:            HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md
SYNC:            ./SYNC_Connectome_Edge_Kit_Sync_Current_State.md

IMPL:            ? (planned) scripts/connectome/health/edge_kit_health_check_runner.ts
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: edge_render_on_step_release
  purpose: verify active edge styling and pulse behavior
  triggers:

  * type: manual
    source: runtime_engine Next click
    frequency:
    expected_rate: "human driven"
    risks:
  * "edge disappears"
  * "wrong dash/color"
  * "pulse too fast"
  * "pulse goes through nodes"
    ```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: edge_semantic_style_mapping_integrity
  flow_id: edge_render_on_step_release
  priority: high

* name: edge_visibility_integrity
  flow_id: edge_render_on_step_release
  priority: high

* name: edge_pulse_endpoint_clamp_integrity
  flow_id: edge_render_on_step_release
  priority: med
  ```

---

## CHECKER INDEX

```
checkers:

* name: health_check_trigger_maps_to_correct_dash_style
  purpose: "V1: direct/stream/async mapping."
  status: pending

* name: health_check_calltype_maps_to_correct_color
  purpose: "V2: color mapping."
  status: pending

* name: health_check_edge_labels_not_bold_and_have_halo
  purpose: "V3: readability."
  status: pending

* name: health_check_pulse_duration_minimum
  purpose: "V4: >=200ms."
  status: pending

* name: health_check_pulse_stops_at_node_boundary
  purpose: "V5: boundary clamp."
  status: pending

* name: health_check_active_edge_persists_until_next_step
  purpose: "V6: persistence."
  status: pending

* name: health_check_no_edges_disappear_on_step
  purpose: "E2: visibility integrity."
  status: pending
  ```

---

## HOW TO RUN

```
pnpm connectome:health edge_kit
```

---

## KNOWN GAPS

* [ ] Requires a render-probe to extract computed edge styles and label font weight.
* [ ] Boundary intersection checks need geometry probes from flow_canvas.

---

## GAPS / IDEAS / QUESTIONS

* IDEA: expose a debug object per rendered edge to avoid brittle DOM tests.

---

---
