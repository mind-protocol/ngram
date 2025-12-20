```

# runtime_engine — Health: Verification Mechanics and Coverage

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file verifies that runtime_engine preserves the guarantees that make /connectome a trustworthy debugger:

* stepper: one click → one event
* speed: presentation only (no authorization leak)
* minimum animation duration enforced
* no autoplay leaks in stepper mode

This file does not verify:

* edge rendering correctness (edge_kit)
* ledger storage correctness (state_store)
* backend correctness (Tempo/Canon invariants)

---

## WHY THIS PATTERN

Stepper dashboards fail silently: everything “looks animated” but the semantics are wrong.

HEALTH exists to make incorrect semantics visible:

* a double-release becomes a red indicator immediately
* an autoplay leak becomes a red indicator immediately

---

## HOW TO USE THIS TEMPLATE

* Define the flows runtime_engine owns (stepper release; mode switch)
* Define checkers that can sample store state transitions
* Emit a simple enum status: OK/WARN/ERROR

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Runtime_Engine_Stepper_And_Realtime_Traversal_Control_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Runtime_Engine_User_Controlled_Traversal_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Runtime_Engine_Step_Release_And_Realtime_Scheduling.md
VALIDATION:      ./VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md
THIS:            HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md
SYNC:            ./SYNC_Connectome_Runtime_Engine_Sync_Current_State.md

IMPL:            ? (planned) scripts/connectome/health/runtime_engine_health_check_runner.ts
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: runtime_engine_stepper_next_step_release
  purpose: Guarantee “one Next → one event” and no autoplay.
  triggers:

  * type: manual
    source: UI button "Next step"
    notes: direct user command
    frequency:
    expected_rate: "human-driven: <= 5/min typical; burst <= 5/s"
    peak_rate: "human-driven; bounded"
    burst_behavior: "must remain correct under rapid clicking"
    risks:
  * "double-release bug"
  * "cursor desync"
  * "duration clamp missing"
    notes: "Realtime not required for v1"

* flow_id: runtime_engine_speed_change
  purpose: Ensure speed does not release steps in stepper mode.
  triggers:

  * type: manual
    source: UI speed selector
    frequency:
    expected_rate: "rare"
    peak_rate: "user spam"
    burst_behavior: "must not alter ledger/cursor"
    risks:
  * "autoplay leak due to speed timer"
    notes: "Speed is presentation only in stepper"
    ```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: runtime_stepper_single_step_integrity
  flow_id: runtime_engine_stepper_next_step_release
  priority: high
  rationale: "If broken, /connectome cannot be trusted."

* name: runtime_speed_authorization_separation
  flow_id: runtime_engine_speed_change
  priority: high
  rationale: "Prevents the most common regression: speed triggers autoplay."

* name: runtime_min_duration_enforced
  flow_id: runtime_engine_stepper_next_step_release
  priority: med
  rationale: "Trust + readability requirement."

* name: runtime_autoplay_leak_detector
  flow_id: runtime_engine_stepper_next_step_release
  priority: high
  rationale: "Any release without Next in stepper is catastrophic."
  ```

---

## STATUS (RESULT INDICATOR)

```
status:
stream_destination: "file:?/var/connectome/health/runtime_engine_status.json"
result:
representation: enum
value: UNKNOWN
updated_at: "2025-12-20T00:00:00+01:00"
source: runtime_stepper_single_step_integrity
```

---

## DOCK TYPES (COMPLETE LIST)

* event (Next click, speed change)
* file (exported status JSON)
* config (MIN_ANIMATION_MS)
* metric (ledger length deltas, cursor deltas)

---

## CHECKER INDEX

```
checkers:

* name: health_check_stepper_one_click_one_event
  purpose: "Assert V1: ledger+cursor increments exactly 1 per Next."
  status: pending
  priority: high

* name: health_check_speed_does_not_release_steps
  purpose: "Assert V2: speed changes do not change ledger/cursor."
  status: pending
  priority: high

* name: health_check_min_duration_clamp_applied
  purpose: "Assert V3: duration >= 200ms for all releases."
  status: pending
  priority: med

* name: health_check_autoplay_leak_in_stepper_mode
  purpose: "Assert E2: no events appended without Next command."
  status: pending
  priority: high
  ```

---

## INDICATOR: runtime_stepper_single_step_integrity

### VALUE TO CLIENTS & VALIDATION MAPPING

```
value_and_validation:
indicator: runtime_stepper_single_step_integrity
client_value: "Agents can single-step the pipeline and trust semantics."
validation:
- validation_id: V1
criteria: "One Next releases exactly one event and advances cursor by 1."
```

### HEALTH REPRESENTATION

```
representation:
selected: [enum]
semantics:
enum: "OK=always 1; WARN=rare mismatch but detected; ERROR=double-release or cursor desync"
aggregation:
method: "worst_state"
```

### DOCKS SELECTED

```
docks:
input:
- id: dock_next_command_received
type: event
location: connectome/runtime_engine:dispatch_runtime_command (?)
output:
- id: dock_ledger_length_after_release
type: metric
location: connectome/state_store:append_event (?)
- id: dock_cursor_after_release
type: metric
location: connectome/state_store:set_cursor (?)
```

### ALGORITHM / CHECK MECHANISM

```
mechanism:
steps:
- "On each Next command, record ledger_length_before and cursor_before"
- "After release completes, record ledger_length_after and cursor_after"
- "Assert deltas are exactly 1 unless end_of_script"
- "Emit OK/WARN/ERROR"
```

### INDICATOR

```
indicator:
error:
- name: double_release_detected
linked_validation: [V1]
meaning: "More than one event released for one Next"
default_action: page
warning:
- name: cursor_mismatch_detected
linked_validation: [V1]
meaning: "Cursor did not match ledger increment"
default_action: warn/log
info:
- name: single_step_ok
linked_validation: [V1]
meaning: "Deltas correct"
default_action: log
```

### THROTTLING STRATEGY

```
throttling:
trigger: event
max_frequency: "1/0s"   # evaluate every Next click
burst_limit: 100
backoff: "none"
```

### FORWARDINGS & DISPLAYS

```
forwarding:
targets:
- location: "/connectome UI header badge — runtime_engine"
transport: event
display:
locations:
- surface: UI
location: "Log panel header"
signal: "OK/WARN/ERROR badge with tooltip counts"
```

### MANUAL RUN

```
manual_run:
command: "pnpm connectome:health runtime_engine"
```

---

## HOW TO RUN

```
pnpm connectome:health runtime_engine
pnpm connectome:health runtime_engine --checker health_check_stepper_one_click_one_event
```

---

## KNOWN GAPS

* [ ] Dock locations are unknown until implementation exists (file:line = ?)
* [ ] Realtime-related indicators are deferred for v1

---

## GAPS / IDEAS / QUESTIONS

* IDEA: Add a “rapid-click fuzz” mode to stress test V1 quickly.
* QUESTION: Should health checks run in CI, or only as an on-demand dev tool?

---

---
