```

# runtime_engine — Algorithm: Step Release Gate and Realtime Scheduling

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md
THIS:            ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md (you are here)
VALIDATION:      ./VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md
HEALTH:          ./HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md
SYNC:            ./SYNC_Connectome_Runtime_Engine_Sync_Current_State.md
```

---

## OVERVIEW

runtime_engine is a small controller that:

* receives UI commands (Next/Restart/Mode/Speed)
* releases exactly one FlowEvent per Next in stepper mode
* schedules continuous release in realtime mode (deferred)
* applies minimum animation duration policy (>=200ms)

It does not render and does not store ledgers directly.

---

## DATA STRUCTURES

### `RuntimeCommand`

(see PATTERNS)

### `RuntimeReleaseResult`

(see PATTERNS)

---

## ALGORITHM: `release_next_step()`

### Step 1: Guard conditions

* If mode != stepper → return blocked (wrong mode)
* If cursor at end → return end_of_script

### Step 2: Fetch raw step

* raw_step = step_script[cursor]
* cursor_next = cursor + 1 (store update happens after successful normalization)

### Step 3: Normalize to FlowEvent

* event = event_model.normalize_flow_event(raw_step)
* If event invalid → preserve unknowns “?” and proceed (never drop)

### Step 4: Compute animation duration

* duration_ms = clamp(event.duration_ms ?? default_for_speed, MIN_ANIMATION_MS)

### Step 5: Commit to store (single atomic update)

* append event to ledger
* set “active focus” (active node id, active edge id, active step_key)
* set explanation text for this step
* set cursor=cursor_next

### Step 6: Return result

* return released with event id

---

## ALGORITHM: `dispatch_runtime_command(cmd)`

### Step 1: Switch on cmd.kind

* next_step → call release_next_step()
* restart → reset cursor, clear active focus, clear ledger (or clear view) (policy in state_store)
* set_mode → stepper/realtime
* set_speed → store speed; affects duration defaults + progress widgets
* set_local_pause → only used in realtime

### Step 2: Emit result for UI

* return RuntimeReleaseResult (released/blocked/end_of_script)

---

## KEY DECISIONS

### D1: Duration default policy

```
default_duration_for_speed(speed):
pause: 650ms
1x:    650ms
2x:    450ms
3x:    300ms
and then clamp to MIN_ANIMATION_MS=200ms
```

Rationale:

* speed changes “feel” without changing authorization

### D2: End-of-script behavior

```
When end reached:
do not wrap automatically
require Restart
```

Rationale:

* preserves debugging clarity and prevents surprise loops

---

## DATA FLOW

```
UI command
→ runtime_engine.dispatch_runtime_command
→ (optional) release_next_step
→ event_model.normalize_flow_event
→ state_store.commit_update (append + focus + explanation + cursor)
```

---

## COMPLEXITY

* stepper release: O(1) per click
* realtime (deferred): O(1) per event + optional buffering

---

## HELPER FUNCTIONS

### `compute_animation_duration_ms(event, speed)`

* returns >=200ms
* returns declared duration if available and >200ms

### `build_explanation_sentence(event)`

* produces one truthful sentence for the unified log/explain panel
* if unknown: adds “?” marker

---

## INTERACTIONS

| Module                       | Interaction                               |
| ---------------------------- | ----------------------------------------- |
| event_model                  | normalize raw step/payload → FlowEvent    |
| state_store                  | commit atomic state updates for release   |
| telemetry_adapter (deferred) | provide realtime payload stream           |
| log_panel                    | reads store and displays current + ledger |

---

## GAPS / IDEAS / QUESTIONS

* [ ] Decide ledger reset policy on Restart (clear all vs mark new cycle boundary)
* QUESTION: Should “Restart” preserve old logs and start a new session id? (likely yes for copy/export)

---

---
