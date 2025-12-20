```

# state_store — Behaviors: Observable Effects of a Single Canonical Store

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md
THIS:            BEHAVIORS_Connectome_State_Store_Observable_State_Consistency_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_Connectome_State_Store_Atomic_Commits_For_Step_Releases_And_Realtime.md
VALIDATION:      ./VALIDATION_Connectome_State_Store_Invariants_For_Ledger_Ordering_And_Focus.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md
HEALTH:          ./HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md
SYNC:            ./SYNC_Connectome_State_Store_Sync_Current_State.md
```

---

## BEHAVIORS

### B1: “One step” feels atomic everywhere

```
GIVEN:  a step is released
WHEN:   the store updates
THEN:   the diagram highlight, explanation sentence, and log entry change together
AND:    there is no intermediate state where the highlight changed but the log did not (or vice versa)
```

### B2: The ledger is always copyable and truthful

```
GIVEN:  the user presses “Copy log”
THEN:   the exported data is exactly the ledger entries in the store
AND:    the export includes stable ids and required fields (per event_model)
```

### B3: Focus is singular and persistent

```
GIVEN:  a step is released
THEN:   there is exactly one active edge and one active node focus
AND:    they remain active until the next release
```

### B4: Wait progress bar behaves like time-under-load, not animation

```
GIVEN:  a player message is “sent”
WHEN:   no answer has arrived yet
THEN:   wait progress increases up to max 4.0s
AND:    when the answer arrives, progress stops and resets (or marks completion)
```

### B5: Tick cron display is consistent with speed selection

```
GIVEN:  speed is set to pause/1x/2x/3x
THEN:   store updates nominal tick interval and tick display label
AND:    the cron node fill reflects the interval (signal only; rendering owns animation)
```

---

## EDGE CASES

### E1: Rapid Next clicking

```
GIVEN:  user clicks Next rapidly
THEN:   store commits remain ordered and consistent (no lost steps)
```

### E2: Out-of-order realtime events (deferred)

```
GIVEN:  two realtime events arrive out of order
THEN:   store preserves a stable ordering policy (arrival order or at_ms policy)
AND:    UI remains readable
```

---

## ANTI-BEHAVIORS

### A1: Component-local shadow ledger

```
MUST NOT: maintain a separate log list in a component
INSTEAD: log is derived exclusively from store.ledger
```

### A2: Focus ambiguity

```
MUST NOT: multiple active edges remain lit simultaneously (unless explicitly allowed)
INSTEAD: store.active_focus is singular
```

---

## INPUTS / OUTPUTS

Store is a state authority; it does not return values except selectors.

**Inputs (actions):** explicit store actions (see PATTERNS).
**Outputs:** updated state; selectors for UI.

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: Should focus include “active_zone_id” (FE/BE/GRAPH/AGENTS) to improve zone highlighting?
* IDEA: Include a “session_id” so exports clearly separate restarts.

---

---
