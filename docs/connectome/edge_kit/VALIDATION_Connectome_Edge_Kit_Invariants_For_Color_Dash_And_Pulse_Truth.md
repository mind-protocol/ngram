```

# edge_kit — Validation: Invariants for Color, Dash, Direction, and Pulse Truth

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Edge_Kit_Edge_Rendering_Pulse_Shine_And_Label_Placement_Rules.md
THIS:            VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md
HEALTH:          ./HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md
SYNC:            ./SYNC_Connectome_Edge_Kit_Sync_Current_State.md
```

---

## INVARIANTS

### V1: Trigger → dash mapping is strict

```
direct  => solid
stream  => dotted
async   => dashed
```

### V2: Call type → color mapping is strict

```
graphLink  => yellow/orange
graphQuery => purple
code       => blue
llm        => green
moment     => yellow
```

### V3: Label is not bold and remains readable

```
label font weight is normal
label has halo/background for contrast
```

### V4: Pulse duration minimum

```
pulse_duration_ms >= 200ms
```

### V5: Pulse endpoints stop at node edges

```
pulse path start/end must lie on node boundary intersection (within tolerance)
```

### V6: Active edge persists until next step

```
active edge remains active until store.active_focus.edge_id changes
```

---

## ERROR CONDITIONS

### E1: Color mismatch

* severity: ERROR
* meaning: semantics are lying

### E2: Edge disappears

* severity: ERROR
* meaning: instrument broken

### E3: Pulse goes through node interior

* severity: WARN/ERROR depending on frequency

---

## HEALTH COVERAGE

| Validation | Health Indicator                      |
| ---------- | ------------------------------------- |
| V1/V2      | edge_semantic_style_mapping_integrity |
| V4         | edge_min_pulse_duration_integrity     |
| V5         | edge_pulse_endpoint_clamp_integrity   |
| V6         | edge_active_persistence_integrity     |
| E2         | edge_visibility_integrity             |

---

## VERIFICATION PROCEDURE

### Manual

```
[ ] Compare edge style to trigger badges in log
[ ] Confirm link title not bold
[ ] Stream edges show gentle directional motion
[ ] Pulses stop at node boundaries
[ ] Active edge remains bright until Next
```

### Automated

```
pnpm connectome:health edge_kit
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: define numerical tolerance for boundary intersection (pixels) → `?`

---

---
