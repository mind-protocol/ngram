```

# state_store — Algorithm: Atomic Commits for Releases, Focus, and Timers

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md
BEHAVIORS:       ./BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md
THIS:            ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md (you are here)
VALIDATION:      ./VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md
HEALTH:          ./HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md
SYNC:            ./SYNC_Connectome_State_Store_Sync_Current_State.md
```

---

## OVERVIEW

state_store owns:

* the append-only ledger of FlowEvents
* the active focus (node/edge/step key)
* the current explanation sentence
* mode/speed flags and time signals (wait/tick widgets)

All updates for one release must occur in a single commit to prevent visual/log desync.

---

## DATA STRUCTURES

### `ConnectomeStoreState`

```
ConnectomeStoreState:
session_id: string
mode: stepper|realtime
speed: pause|1x|2x|3x
local_pause: boolean
cursor: number
ledger: FlowEvent[]
active_focus:
active_node_id: string|null
active_edge_id: string|null
active_step_key: string|null
current_explanation:
sentence: string
notes: string|null
wait_progress:
started_at_ms: number|null
stopped_at_ms: number|null
max_seconds: 4.0
tick_display:
nominal_interval_ms: number|Infinity
progress_0_1: number
speed_label: string
health_badges:
[module_name]: {status: OK|WARN|ERROR|UNKNOWN, tooltip: string}
```

---

## ALGORITHM: `commit_step_release_append_event_and_set_focus_and_explanation(release)`

Input: `release` contains:

* `event: FlowEvent`
* `focus: {node_id, edge_id, step_key}`
* `explanation_sentence: string`
* `wait_timer_action?: start|stop|none`
* `cursor_next: number`

Steps:

1. Validate minimal shape (never throw; fill `?` if needed)
2. Append event to ledger (immutable append)
3. Set active_focus exactly to focus values
4. Set current_explanation sentence and notes
5. Apply wait timer updates:

   * start: set started_at_ms=now, stopped_at_ms=null
   * stop: set stopped_at_ms=now (or set started_at_ms=null if reset policy)
6. Update cursor to cursor_next
7. Done (one transaction)

---

## ALGORITHM: `restart_session_clear_or_boundary()`

Policy must match runtime_engine.

Option A (clear):

* new session_id
* ledger=[]
* cursor=0
* clear focus/explanation
* reset timers

Option B (boundary):

* new session_id
* preserve ledger but insert a boundary marker event (call_type=code, label="SESSION_BOUNDARY") (?)
* cursor=0
* reset focus/explanation/timers

Mark the chosen policy in SYNC once decided.

---

## ALGORITHM: `append_realtime_event_and_update_focus_if_needed(event)` (deferred)

1. Append event
2. Decide focus update policy:

   * either focus latest event always
   * or focus only if user has not pinned focus
3. Apply retention policy
4. Done

---

## ALGORITHM: wait progress computation (selector)

Given:

* started_at_ms
* now_ms
  Compute:
* elapsed_s = clamp((now-start)/1000, 0, 4.0)
* value_0_1 = elapsed_s / 4.0
* display = round(elapsed_s, 1)

Store does not “tick” this; a selector can compute on render, or a lightweight interval can update tick_display only (but must not release steps).

---

## COMPLEXITY

* append: O(1) per event
* export: O(n) over ledger
* retention: O(k) evictions (bounded)

---

## GAPS / IDEAS / QUESTIONS

* [ ] Decide focus policy in realtime mode (auto-focus newest vs pinned).
* QUESTION: Should store include a “pinned_focus” that prevents realtime from overriding focus?
* IDEA: Provide a derived selector to produce “duration color class” for the log panel to avoid duplicating rules.

---

---
