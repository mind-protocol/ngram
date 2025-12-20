```

# node_kit — Validation: Invariants for Readability and Correct State Reflection

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md
THIS:            VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md
HEALTH:          ./HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md
SYNC:            ./SYNC_Connectome_Node_Kit_Sync_Current_State.md
```

---

## INVARIANTS

### V1: Type and language styling is deterministic

```
Given (node_type, language):
background theme is stable and does not depend on render order
```

### V2: Title prominence invariant

```
Title is visually dominant over file_path:
title font size > path font size
path is not bold
```

### V3: Active step highlight singularity

```
At any time:
in a given node, at most one step is highlighted
if active_step_key does not match any step_key, none are highlighted
```

### V4: Energy mapping invariant

```
Given energy value e:
mapped color is deterministic per thresholds
glow intensity corresponds to bucket
```

### V5: Player wait progress bounded

```
Displayed wait seconds:
0.0 <= seconds <= 4.0
one decimal precision
```

### V6: Tick cron bounded

```
Tick progress:
0.0 <= progress_0_1 <= 1.0
Speed label matches store speed
```

---

## ERROR CONDITIONS

### E1: Multiple active steps highlighted

* severity: ERROR
* meaning: the “one function per step” debugging intent is broken

### E2: Energy color mapping inconsistent

* severity: WARN/ERROR depending on impact
* meaning: energy stops being interpretable

---

## HEALTH COVERAGE

| Validation | Health Indicator                        |
| ---------- | --------------------------------------- |
| V3         | node_active_step_singularity_integrity  |
| V4         | node_energy_color_bucket_integrity      |
| V5         | node_wait_progress_clamp_integrity      |
| V6         | node_tick_cron_progress_clamp_integrity |

---

## VERIFICATION PROCEDURE

### Manual

```
[ ] Step through events: each node highlights only one internal step at a time
[ ] Energy changes: badge glow changes bucket correctly
[ ] Wait bar never exceeds 4.0s and shows 0.1 precision
[ ] Cron ring stays within 0..1 and matches speed label
```

### Automated

```
pnpm connectome:health node_kit
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-20
VERIFIED_AGAINST:
impl: ?
health: ?
RESULT:
V1..V6: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: Should we assert minimum contrast ratios (WCAG-ish) for title readability? (nice-to-have)

---

---
