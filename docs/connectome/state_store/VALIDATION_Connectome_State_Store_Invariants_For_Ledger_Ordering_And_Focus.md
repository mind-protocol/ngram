```

# state_store — Validation: Invariants for Ledger, Focus, and Timers

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md
BEHAVIORS:       ./BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md
THIS:            VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md
HEALTH:          ./HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md
SYNC:            ./SYNC_Connectome_State_Store_Sync_Current_State.md
```

---

## INVARIANTS

### V1: Ledger is append-only within a session

```
Within a session_id:
ledger length never decreases
past entries are never mutated
```

### V2: Exactly one active focus

```
active_focus.active_node_id is one value or null
active_focus.active_edge_id is one value or null
No parallel “active set” unless explicitly designed
```

### V3: Atomic commit integrity

```
For each step release commit:
ledger appended AND focus updated AND explanation updated occur in the same commit
No observable intermediate state should exist
```

### V4: Wait timer boundaries are correct

```
If wait_progress.started_at_ms is set:
started_at_ms <= now_ms
Elapsed seconds are clamped to [0, 4.0]
Display uses 1 decimal precision
```

---

## PROPERTIES

### P1: Export equals ledger

```
Copy/export output must equal store.ledger (1:1) plus optional formatting metadata
```

### P2: Restart resets state consistently with selected policy

```
After restart:
cursor == 0
focus cleared
timers reset
session_id changes
and ledger behavior matches chosen policy (clear vs boundary)
```

---

## ERROR CONDITIONS

### E1: Focus mismatch

* symptom: multiple nodes/edges appear active simultaneously due to store state
* severity: ERROR

### E2: Ledger mutation

* symptom: existing ledger event changes after append
* severity: ERROR

---

## HEALTH COVERAGE

| Validation | Health Indicator                   |
| ---------- | ---------------------------------- |
| V1         | store_ledger_append_only_integrity |
| V2         | store_single_focus_integrity       |
| V3         | store_atomic_commit_integrity      |
| V4         | store_wait_timer_clamp_integrity   |
| P1         | store_export_equals_ledger         |
| P2         | store_restart_policy_consistency   |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Click Next once → log + focus + explanation change together
[ ] Click Next again → previous entry unchanged, ledger grows by 1
[ ] Click Restart → session_id changes, cursor=0, focus cleared
[ ] Trigger wait timer start/stop → progress clamps to 4.0s and shows 1 decimal
[ ] Copy log → export equals visible ledger count
```

### Automated

```
pnpm connectome:health state_store
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-20
VERIFIED_AGAINST:
impl: ?
health: ?
RESULT:
V1: NOT RUN
V2: NOT RUN
V3: NOT RUN
V4: NOT RUN
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: do we need a “transaction id” recorded per commit for debugging atomicity? (nice-to-have)
* IDEA: ledger entries can include `arrival_index` to guarantee ordering even with same timestamp

---

---
