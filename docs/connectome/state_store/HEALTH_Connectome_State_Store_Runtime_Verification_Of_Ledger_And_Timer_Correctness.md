```

# state_store — Health: Verification Mechanics and Coverage

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This HEALTH file ensures the state_store makes /connectome trustworthy:

* ledger append-only
* single active focus
* atomic commit behavior
* wait timer clamping correctness
* export equals ledger

It does not validate rendering aesthetics or backend correctness.

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

IMPL:            ? (planned) scripts/connectome/health/state_store_health_check_runner.ts
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: store_stepper_atomic_commit
  purpose: Prevent desync between highlight, explanation, and log.
  triggers:

  * type: manual
    source: runtime_engine Next click
    frequency:
    expected_rate: "human driven"
    peak_rate: "rapid clicking"
    risks:
  * "partial commits"
  * "focus not updated"
  * "ledger mutation"
    notes: "Primary v1 risk: UI feels glitchy (links disappear, focus wrong)."

* flow_id: store_wait_timer_progress
  purpose: Ensure progress bar semantics trustworthy.
  triggers:

  * type: event
    source: runtime_engine start_wait / stop_wait
    frequency:
    expected_rate: "per player message"
    peak_rate: "rare"
    risks:
  * "progress exceeds 4.0s"
  * "display precision wrong"
    ```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: store_ledger_append_only_integrity
  flow_id: store_stepper_atomic_commit
  priority: high
  rationale: "Auditability and copy/export depend on this."

* name: store_single_focus_integrity
  flow_id: store_stepper_atomic_commit
  priority: high
  rationale: "Prevents multi-glow confusion."

* name: store_atomic_commit_integrity
  flow_id: store_stepper_atomic_commit
  priority: high
  rationale: "Prevents UI/log mismatch and disappearing edges."

* name: store_wait_timer_clamp_integrity
  flow_id: store_wait_timer_progress
  priority: med
  rationale: "Progress bar must be truthful and bounded."

* name: store_export_equals_ledger
  flow_id: store_stepper_atomic_commit
  priority: high
  rationale: "Copy log must be exact."
  ```

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

---

## HOW TO RUN

```
pnpm connectome:health state_store
pnpm connectome:health state_store --checker health_check_atomic_commit_updates_all_fields
```

---

## KNOWN GAPS

* [ ] Dock locations are unknown until implementation exists (file:line = ?)
* [ ] Restart policy not finalized; checks must branch by policy

---

## GAPS / IDEAS / QUESTIONS

* IDEA: add “commit_id” incremented per atomic commit to make HEALTH checks trivial.
* QUESTION: should export include session_id header? recommended: yes.

---

---
