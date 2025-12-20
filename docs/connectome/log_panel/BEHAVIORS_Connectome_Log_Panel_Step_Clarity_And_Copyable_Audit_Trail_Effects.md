```

# log_panel — Behaviors: Step Clarity and Copyable Audit Trail

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md
THIS:            BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md
VALIDATION:      ./VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md
HEALTH:          ./HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md
SYNC:            ./SYNC_Connectome_Log_Panel_Sync_Current_State.md
```

---

## BEHAVIORS

### B1: One step has one explanation sentence, always in sync

```
GIVEN:  a step is released
THEN:   the “Now” sentence updates exactly once
AND:    it matches the most recent ledger event
AND:    the active focus shown in the panel matches the active edge glow
```

### B2: “Step X of Y” is always readable and unambiguous

```
GIVEN:  ledger has N entries and step script has total T (if known)
THEN:   the panel displays “Step (cursor) of (T)” (or “Step (cursor)” if T unknown)
AND:    never displays ambiguous shorthand like “#9/16”
```

### B3: Duration coloring communicates severity at a glance

```
GIVEN:  a duration exists
THEN:   duration text is color-coded:
ms: blue
<1s: green
<2s: yellow
<3s: orange
else: red
```

### B4: Trigger types are visibly distinct in the log

```
GIVEN:  trigger is direct/stream/async/hook/timer
THEN:   a trigger badge uses distinct colors (deterministic palette)
```

### B5: Export is copy/paste reliable

```
GIVEN:  user clicks “Copy log”
THEN:   clipboard contains a stable representation of the ledger
AND:    user can paste it back into tools to replay/debug
```

---

## ANTI-BEHAVIORS

### A1: Log line lies about what happened

```
MUST NOT: display an explanation that doesn’t correspond to the last event
INSTEAD: explanation is derived from the last released FlowEvent
```

### A2: Export does not match ledger

```
MUST NOT: export a filtered/partial list without telling the user
INSTEAD: export indicates filters, or exports full ledger by default
```

---

## EDGE CASES

### E1: Unknown duration

```
GIVEN:  duration is unknown
THEN:   display “?” with muted styling
AND:    show notes in tooltip
```

### E2: Realtime bursts (deferred)

```
GIVEN:  realtime emits many events
THEN:   log remains usable with retention/pagination policy (owned by state_store)
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: Should duration thresholds be configurable? (v1: no, fixed)
* IDEA: Provide a “copy last 20” option in v1.1

---

---
