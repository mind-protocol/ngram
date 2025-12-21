
# state_store — Health: Verification Mechanics and Coverage

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file keeps the state_store honest so Connectome feels trustworthy when runtime events are replayed. It names the append-only ledger, single focus, atomic commit behavior, wait timer bounds, and export parity results that humans and downstream tooling rely on, and it explicitly stops short of validating rendering aesthetics or unrelated backend components.

The health harness looks only at docked signals that the implementation already emits, so it limits scope while still giving operators confidence that the runtime experience is anchored in the documented invariants.

---

## WHY THIS PATTERN

Verification here is driven by a pattern that keeps health checks close to runtime without adding sagas or modifying production code. Docking-based observations let us confirm the validation invariants (ledger append-only, single focus, atomic commits, timer clamping, export equality) while throttling events so analysts and the doctor can trust every signal that survives constant Next-click noise.

This keeps the check lightweight yet meaningful: if the docking event that fires when the atomic commit action completes is missing, we know something regressed, even if unit tests still pass.

---

## HOW TO USE THIS TEMPLATE

1. Read the full doc chain (OBJECTIFS → PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → SYNC) before touching this HEALTH doc so the rationale stays aligned with the canonical state_store story.
2. Trace the implementation docking points in `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md` to understand where each indicator can observe data noninvasively.
3. Identify the most costly failures (ledger mutation, focus divergence, timer drift) and describe the flows, checkers, and status indicators that protect them.
4. Tie every indicator to one or more validation IDs, document the algorithm that compares docks/metrics, and record throttling plus forwarding destinations so the doctor can read the status stream without guessing.
5. Keep the manual and automated run commands handy so future agents can re-run or extend these checks before shipping.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md
BEHAVIORS:       ./BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md
VALIDATION:      ./VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md
THIS:            HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md
SYNC:            ./SYNC_Connectome_State_Store_Sync_Current_State.md

IMPL:            (planned) pnpm connectome:health state_store
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: store_atomic_commit
  purpose: Keep ledger, focus, explanation, and timer selectors in sync after every step release so UI and export remain consistent.
  triggers:

  * type: event
    source: app/connectome/lib/zustand_connectome_state_store_with_atomic_commit_actions#commit_step_release_append_event...
    notes: runtime_engine emits a FlowEvent and then runs the atomic commit action.
  frequency:
    expected_rate: "0.5/min"
    peak_rate: "5/min"
    burst_behavior: "Rapid clicking during demos can push rates toward 10/min with immediate retries and no network delay."
  risks:
  * "V3: observable intermediate states if focus or explanation lag the ledger." 
  * "V1: ledger mutation or shrinking inside the session when commits race."
  notes: Observation derived from the implementation data flow listing so we tie every indicator to a concrete dock.

* flow_id: realtime_ingestion_append_and_retention
  purpose: Verify realtime telemetry appends and retention logic so long-running sessions stay performant and focused.
  triggers:

  * type: event
    source: telemetry_adapter → connectome_state_store append action
    notes: External telemetry payloads normalize to FlowEvents that the store claims before renderers react.
  frequency:
    expected_rate: "1/min"
    peak_rate: "20/min"
    burst_behavior: "Bursting metrics (bulk uploads) trigger retention logic and dock_store_retention_evictions fires once thresholds are hit."
  risks:
  * "P2: retention policy violating restart invariants when retention evicts the wrong entries." 
  * "V2: focus jumping unexpectedly if realtime focus updates fire while a commit is in motion."
  notes: The retention dock keeps the doctor honest about trimmed ledgers versus the policy described in VALIDATION.

* flow_id: restart_session_clear_or_boundary
  purpose: Ensure restart decisions (clear vs boundary) claim the right session_id and reset timers/focus so downstream selectors start clean.
  triggers:

  * type: manual
    source: connectome session restart controller
    notes: Users hit Restart or runtime policies force a boundary marker.
  frequency:
    expected_rate: "0.1/min"
    peak_rate: "1/min"
    burst_behavior: "Multiple rapid restarts are rare but the dock still records every boundary signal so we can compare to timer resets."
  risks:
  * "P2: restart policy misapplied, leaving cursor ≠0 or hints of prior focus." 
  * "E1: focus drift due to stale timer selectors after a restart docks."
  notes: The dock_store_session_restart event gives us the single authoritative point to compare new session metadata with the Validation expectations.
```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: store_ledger_append_only_integrity
  flow_id: store_atomic_commit
  priority: high
  rationale: "Auditability and copy/export depend on this."

* name: store_single_focus_integrity
  flow_id: store_atomic_commit
  priority: high
  rationale: "Prevents multi-glow confusion."

* name: store_atomic_commit_integrity
  flow_id: store_atomic_commit
  priority: high
  rationale: "Prevents UI/log mismatch and disappearing edges."

* name: store_wait_timer_clamp_integrity
  flow_id: store_atomic_commit
  priority: med
  rationale: "Progress bar must be truthful and bounded."

* name: store_export_equals_ledger
  flow_id: store_atomic_commit
  priority: high
  rationale: "Copy log must be exact."
```

Each indicator is tied to the validation doc so the doctor can trace every runtime signal back to V1‑V4 and the exported properties.

---

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
| --------- | ---------- | ------------------------ |
| Ledger + focus determinism across step releases so UI/log/export feel identical | store_ledger_append_only_integrity, store_single_focus_integrity, store_atomic_commit_integrity | Clients expect commits to append once, keep focus singular, and surface the same explanation text across the log, so these indicators defend that promise. |
| Timer accuracy, restart hygiene, and export fidelity so downstream tooling trusts the session history | store_wait_timer_clamp_integrity, store_export_equals_ledger | The wait timer needs clamped readings, restart boundaries must reset cursors, and exports must still match ledger data even as retention trims old rows. |

---

## STATUS (RESULT INDICATOR)

```
status:
  stream_destination: file:logs/connectome/state_store_health_status.json
  result:
    representation: enum
    value: OK
    updated_at: 2026-02-28T12:00:00Z
    source: health_check_atomic_commit_updates_all_fields
```

The status stream is derived from the atomic commit checker, so Doctor reads the file to display whether the last commit maintained ledger + focus parity.

---

## DOCK TYPES (COMPLETE LIST)

* `event` – the atomic commit, realtime focus updates, and restart controllers all emit dock events that health probes observe.
* `metric` – ledger sync counts, retention evictions, and export acknowledgments flow through metric docks instead of direct instrumentation.

These are the only dock types required for the state_store health coverage; `custom` is unnecessary because the standard event/metric pairs already expose the needed signals.

---

## CHECKER INDEX

```
checkers:

* name: health_check_ledger_is_append_only
  purpose: "Detect any mutation or deletion within a session_id."
  status: pending
  priority: high

* name: health_check_single_active_focus
  purpose: "Ensure focus is singular and stable until next release."
  status: pending
  priority: high

* name: health_check_atomic_commit_updates_all_fields
  purpose: "Ensure ledger+focus+explanation update together."
  status: pending
  priority: high

* name: health_check_wait_timer_clamps_to_max_4_seconds
  purpose: "Ensure wait timer never exceeds 4.0s and uses 0.1 display precision."
  status: pending
  priority: med

* name: health_check_export_equals_ledger
  purpose: "Exported JSONL or text equals ledger contents."
  status: pending
  priority: high
```

Pending status indicates these checks still await implementation wiring, but each purpose directly maps to a validation invariant so the indicator logic can be wired without rewriting the store.

---

## INDICATOR: store_atomic_commit_integrity

### VALUE TO CLIENTS & VALIDATION MAPPING

```
value_and_validation:
  indicator: store_atomic_commit_integrity
  client_value: "Customers see a single, in-order log, so commits must touch ledger, focus, and explanation together."
  validation:
    - validation_id: V3
      criteria: "Each step release commit appends ledger, updates focus, and updates explanation atomically."
    - validation_id: V1
      criteria: "Within a session_id the ledger length never decreases and past entries never mutate."
```

The indicator protects the basic journal contract and the downstream exports that copy from the ledger, so it links to both V3 and V1.

### HEALTH REPRESENTATION

```
representation:
  allowed:
    - enum
    - binary
  selected:
    - enum
  semantics:
    enum: "OK = commit dock observed and ledger/focus/explanation stayed in sync; WARN = commit dock fired but one field lagged; ERROR = missing commit dock or ledger shrink."
  aggregation:
    method: "Take the worst depiction across the last 5 commits so a single ERROR still surfaces immediately."
    display: "Use the enum on the status stream while binary logs aggregate for analytics."
```

### DOCKS SELECTED

```
docks:
  input:
    id: dock_store_commit_action_invoked
    method: commit_step_release_append_event_and_set_focus_and_explanation
    location: docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md:107-117
  output:
    id: dock_store_ledgers_synced
    method: serializeLedgerToJsonl
    location: docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md:107-117
```

The event dock proves the action ran, the metric dock proves the ledger was flushed for export, and both links remain stable because the implementation documents these docking points.

### ALGORITHM / CHECK MECHANISM

```
mechanism:
  summary: "Compare the atomic commit dock to ledger/focus/explanation snapshots to detect drift and missing exports."
  steps:
    - "Watch `dock_store_commit_action_invoked` to know when a new release finished."
    - "Immediately read `ledger`, `active_focus`, and the explanation sentence to ensure they all changed together."
    - "Verify `dock_store_ledgers_synced` fires afterwards and exported data still matches the ledger footprint."
  data_required: "ledger array, active_focus object, explanation text, docking events."
  failure_mode: "Any mismatch sets the indicator to WARN/ERROR and surfaces that the doctor should not trust the export or UI state."
```

### INDICATOR

```
indicator:
  error:
    - name: ledger_integrity_violation
      linked_validation: [V1, V3]
      meaning: "Commit completed but ledger length shrank, focus/explanation diverged, or the export sync metric never arrived."
      default_action: stop
  warning:
    - name: export_stale_warning
      linked_validation: [P1]
      meaning: "Ledger appended but the export metric indicates the serializer is stale; copy/export output might lag."
      default_action: warn/log
  info:
    - name: step_commit_observed
      linked_validation: [E1]
      meaning: "A commit event occurred and all fields updated as expected; this helps track timing."
      default_action: log
```

### THROTTLING STRATEGY

```
throttling:
  trigger: runtime_engine step release finish event
  max_frequency: "10/min"
  burst_limit: 20
  backoff: "Exponential (halve frequency) when consecutive WARN/ERROR states persist beyond 1 minute."
```

### FORWARDINGS & DISPLAYS

```
forwarding:
  targets:
    - location: file:logs/connectome/state_store_health_status.json
      transport: file
      notes: "Doctor tails this file so engineers can monitor health without re-running commands."
display:
  locations:
    - surface: CLI log
      location: "pnpm connectome:health state_store output"
      signal: warn/ok/error
      notes: "Status lines highlight the enum value and include the latest commit timestamp."
```

### MANUAL RUN

```
manual_run:
  command: pnpm connectome:health state_store
  notes: "Run when validating new commits, especially before merges that touch the store or timer logic."
```

---

## HOW TO RUN

```
pnpm connectome:health state_store
pnpm connectome:health state_store --checker health_check_atomic_commit_updates_all_fields
```

Run all checks via the first command and target the atomic commit checker explicitly with the second, so humans can reproduce the status stream before running deploy pipelines.

---

## KNOWN GAPS

* [ ] Dock identifiers are defined but the health harness runner is still planned, so health_check_* entries remain pending until the script wires mounts (file:line = ?).
* [ ] Restart policies are still unsettled, so the manual harness must branch once we pick clear vs boundary semantics so status accurately reflects the chosen policy.

---

## GAPS / IDEAS / QUESTIONS

* IDEA: Add a `commit_id` increment per atomic commit to make delta detection for the health checker trivial.
* QUESTION: Should exports also carry the session_id header so downstream tooling can detect mismatched restarts without rehydrating the whole ledger?

---
