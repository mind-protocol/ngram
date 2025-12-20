```

# node_kit — Algorithm: Node Rendering Spec and Energy Glow Mapping

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md
THIS:            ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md (you are here)
VALIDATION:      ./VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md
HEALTH:          ./HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md
SYNC:            ./SYNC_Connectome_Node_Kit_Sync_Current_State.md
```

---

## OVERVIEW

Node rendering is deterministic: given node model + store state, it produces consistent visuals.

Inputs:

* node metadata: type, language, title, path, steps list, tooltip text
* state signals: active_focus, energy value, wait/tick progress, flipped flag (?)

Outputs:

* rendered node component with correct background, layout, highlighted step, and widgets

---

## DATA STRUCTURES

### `ConnectomeNodeViewModel`

```
ConnectomeNodeViewModel:
node_id: string
node_type:
Player|UI|Module|GraphQueries|Moment|Agent|TickCron
language: TS|PY|GRAPH|AGENT|UNKNOWN
title: string
file_path: string|null
steps:
- step_key: string
label: string
call_type: code|graphQuery|llm|graphLink|moment
energy_value: number|null
flipped: boolean|null
tooltip: {summary: string, notes: string|null}
```

---

## ALGORITHM: `render_node(view_model, store_state)`

### Step 1: Determine background theme

```
background_theme = theme_for(node_type, language)
```

Rules (v1):

* Player: distinct (warm neutral with accent)
* UI: distinct (cool grey/blue)
* Module TS: TS-blue background tint
* Module PY: PY-purple background tint
* GraphQueries: purple background tint
* Moment: yellow background tint
* Agent: green background tint
* TickCron: speed-coded tint

### Step 2: Title and path

* title rendered prominent, colored by node_type
* file_path rendered small, low contrast, not bold

### Step 3: Steps list (if present)

* render list of step labels
* active_step_key = store.active_focus.active_step_key
* if view_model has a matching step_key:

  * mark that item active (bold)
  * color it by its call_type (from view_model step definition)
* all others revert to normal

### Step 4: Energy badge

If energy_value exists:

* show value (format: 0.00 or 0.0 depending on scale; v1 choose 0.2 precision)
* compute energy_color = map_energy_to_color(energy_value)
* set glow accordingly

### Step 5: Widgets per node type

* PlayerNode:

  * show wait progress bar (value and seconds) from store selector
* TickCronNode:

  * show circular progress ring from store.tick_display.progress_0_1
  * center shows speed label

### Step 6: Flipped ring

If flipped==true:

* add outer ring glow with distinct color (e.g., pink/white) and stronger blur

---

## ALGORITHM: `map_energy_to_color(energy)`

Deterministic thresholds (v1 initial):

```
IF energy is null:
color = neutral_grey
ELSE IF energy < 0.10:
color = grey
ELSE IF energy < 0.30:
color = blue
ELSE IF energy < 0.60:
color = orange
ELSE:
color = yellow
```

Notes:

* thresholds can be tuned later but must remain deterministic
* mapping must be documented whenever changed

---

## ALGORITHM: wait progress display (PlayerNode)

Inputs from store selector:

* seconds_display: one decimal (0.0..4.0)
* value_0_1: 0..1

Color thresholds (v1):

* <1.0s green
* <2.0s yellow
* <3.0s orange
* else red

---

## COMPLEXITY

O(k) where k = number of steps in the node (small). Rendering is fast.

---

## GAPS / IDEAS / QUESTIONS

* [ ] Define exact title color tokens per node_type (shared palette file likely in node_kit).
* QUESTION: Is energy normalized 0..1 or unbounded? mapping assumes “small-ish”; mark `?` until telemetry defines it.
* IDEA: Show a tiny “TS/PY” badge in corner for Module nodes.

---

---
