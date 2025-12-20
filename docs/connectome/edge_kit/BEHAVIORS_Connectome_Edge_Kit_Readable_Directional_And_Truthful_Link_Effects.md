```

# edge_kit — Behaviors: Readable, Directional, Truthful Link Effects

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Edge_Kit_Color_Coded_Trigger_Typed_Directional_Link_Styling_Patterns.md
THIS:            BEHAVIORS_Connectome_Edge_Kit_Readable_Directional_And_Truthful_Link_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_Connectome_Edge_Kit_Edge_Rendering_Pulse_Shine_And_Label_Placement_Rules.md
VALIDATION:      ./VALIDATION_Connectome_Edge_Kit_Invariants_For_Color_Dash_And_Pulse_Truth.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md
HEALTH:          ./HEALTH_Connectome_Edge_Kit_Runtime_Verification_Of_Link_Visibility_And_Semantic_Styling.md
SYNC:            ./SYNC_Connectome_Edge_Kit_Sync_Current_State.md
```

---

## BEHAVIORS

### B1: Link meaning is readable at zoom=1.0

```
GIVEN:  the diagram is at zoom=1.0
THEN:   edge labels are readable and not overwhelmed by glow
AND:    label text is not bold
AND:    label color encodes call_type
```

### B2: Trigger type is visible without reading

```
GIVEN:  a link has trigger type direct/stream/async
THEN:   its dash style communicates it:
direct=solid
stream=dotted
async=dashed
```

### B3: Stream links visibly “flow” in the correct direction

```
GIVEN:  trigger=stream
THEN:   the edge has gentle directional animation that moves from source to target
AND:    this animation is subtle (non-distracting)
```

### B4: Active link highlight persists until next step

```
GIVEN:  a step releases an event along an edge
THEN:   that edge becomes bright/active
AND:    it stays active until the next step releases a new active focus
```

### B5: Pulses stop at node edges, not through nodes

```
GIVEN:  a pulse travels along an edge
THEN:   the pulse begins at the source node boundary
AND:    ends at the target node boundary
```

### B6: Energy transfer magnitude is perceptible but bounded

```
GIVEN:  an event has energy_delta
THEN:   pulse size/glow intensity scales with magnitude
BUT:    it is clamped so it never obscures labels or nodes
```

---

## ANTI-BEHAVIORS

### A1: Graph links rendered as nodes

```
MUST NOT: render ABOUT/THEN/SAID as card-like nodes
INSTEAD: render them as edges with optional fuzzy halos
```

### A2: Labels in bold

```
MUST NOT: bold the link title text
INSTEAD: readable size + halo/contrast
```

---

## EDGE CASES

### E1: Unknown call_type/trigger

```
GIVEN:  trigger or call_type is unknown
THEN:   render using neutral defaults and show “?” tooltip
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: should async edges have a different motion profile than stream edges? (maybe slower, more “chunky”)

---

---
