```

# runtime_engine — Behaviors: User-Controlled Traversal and Playback Effects

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md
THIS:            BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md
VALIDATION:      ./VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md
HEALTH:          ./HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md
SYNC:            ./SYNC_Connectome_Runtime_Engine_Sync_Current_State.md
```

---

## BEHAVIORS

### B1: Next releases exactly one step, regardless of speed

```
GIVEN:  mode=stepper and user clicks Next
WHEN:   runtime_engine processes the command
THEN:   exactly one FlowEvent is released into the ledger
AND:    exactly one edge + one node-step highlight becomes “active”
AND:    glow persists until the next click
```

### B2: Speed changes animation time, not authorization

```
GIVEN:  mode=stepper and user changes speed (pause/1x/2x/3x)
THEN:   the nominal rate display changes and pulse animation duration changes
BUT:    Next still releases one and only one step
```

### B3: Realtime mode autoplays, stepper never autoplays

```
GIVEN:  mode=realtime
WHEN:   events arrive (SSE or derived)
THEN:   events release automatically unless locally paused

GIVEN:  mode=stepper
THEN:   no event releases without an explicit Next click
```

---

## INPUTS / OUTPUTS

### Primary Function: `dispatch_runtime_command()`

**Inputs**

| Name  | Type           | Notes                                                |
| ----- | -------------- | ---------------------------------------------------- |
| `cmd` | RuntimeCommand | next_step/restart/set_mode/set_speed/set_local_pause |

**Outputs**

| Name     | Type                 | Notes                          |
| -------- | -------------------- | ------------------------------ |
| `result` | RuntimeReleaseResult | released/blocked/end_of_script |

---

## EDGE CASES

### E1: End of script

```
GIVEN:  cursor is at last step
WHEN:   user clicks Next
THEN:   result=end_of_script and no new event is appended
AND:    UI explanation states “end reached”
```

### E2: Realtime burst while locally paused (deferred)

```
GIVEN:  local_pause=true in realtime
WHEN:   many events arrive quickly
THEN:   events are buffered with bounded retention (policy in state_store ?)
AND:    buffer size is visible as a health signal
```

---

## ANTI-BEHAVIORS

### A1: Speed accidentally triggers autoplay in stepper

```
MUST NOT: releasing multiple events because speed=3x
INSTEAD: speed only modifies animation duration + nominal rate text
```

### A2: UI bypasses runtime_engine and appends to ledger directly

```
MUST NOT: components append events without runtime_engine release
INSTEAD: all user-facing releases go through runtime_engine gate
```

---

## STATE MANAGEMENT

### Where State Lives

* cursor, mode, speed, pause flags live in `state_store`
* runtime_engine mutates store through explicit actions only

### State Transitions

(see PATTERNS → State Transitions)

---

## RUNTIME BEHAVIOR

### Initialization

* mode=stepper, speed=pause, cursor=0

### Main Loop / Request Cycle

* command-driven in stepper
* event-driven in realtime (deferred)

### Shutdown

* cleanly detach realtime listener (deferred)

---

## CONCURRENCY MODEL

* stepper commands are serialized
* realtime events are queued and drained (deferred)

---

## CONFIGURATION

* MIN_ANIMATION_MS = 200
* MAX_WAIT_PROGRESS_S = 4.0

---

## BIDIRECTIONAL LINKS

### Code → Docs

* runtime_engine implementation must reference this chain in file header comments

### Docs → Code

* behaviors map to runtime_engine unit-level health checks (see HEALTH)

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates

* if buffering policies expand: extract to a dedicated buffering policy helper

### Missing Implementation

* [ ] stepper script interface + release logic
* [ ] realtime mode adapter integration (deferred)

### Ideas

* IDEA: “step back” debugging
* IDEA: “jump to step N” with deterministic cursor movement

### Questions

* QUESTION: should realtime mode support “single-step realtime” (consume one buffered event per Next)? (maybe v2)

---

---
