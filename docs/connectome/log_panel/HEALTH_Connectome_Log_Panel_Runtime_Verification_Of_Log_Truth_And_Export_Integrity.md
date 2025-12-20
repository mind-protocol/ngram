```

# log_panel — Health: Verification of Log Truth and Export Integrity

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

log_panel HEALTH verifies that:

* Now section corresponds to the last event
* duration coloring follows strict rules
* export equals ledger

This is critical because /connectome is meant for debugging and agent audits.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md
VALIDATION:      ./VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md
THIS:            HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md
SYNC:            ./SYNC_Connectome_Log_Panel_Sync_Current_State.md

IMPL:            ? (planned) scripts/connectome/health/log_panel_health_check_runner.ts
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: log_panel_updates_on_step_release
  purpose: ensure Now and ledger stay synchronized
  triggers:

  * type: manual
    source: runtime_engine Next click
    frequency:
    expected_rate: "human driven"
    risks:
  * "Now sentence drift"
  * "wrong step count formatting"

* flow_id: log_panel_export
  purpose: ensure export is exact
  triggers:

  * type: manual
    source: Copy buttons
    frequency:
    expected_rate: "occasional"
    risks:
  * "missing events"
  * "wrong ordering"
    ```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: log_now_matches_last_event_integrity
  flow_id: log_panel_updates_on_step_release
  priority: high

* name: log_duration_color_mapping_integrity
  flow_id: log_panel_updates_on_step_release
  priority: med

* name: log_export_equals_ledger_integrity
  flow_id: log_panel_export
  priority: high
  ```

---

## CHECKER INDEX

```
checkers:

* name: health_check_now_sentence_corresponds_to_last_ledger_event
  purpose: "V1: Now corresponds to last event id/label."
  status: pending

* name: health_check_duration_color_class_matches_thresholds
  purpose: "V3: duration -> color mapping correct."
  status: pending

* name: health_check_export_contains_all_ledger_events_in_order
  purpose: "V4: export equals ledger."
  status: pending
  ```

---

## HOW TO RUN

```
pnpm connectome:health log_panel
```

---

## KNOWN GAPS

* [ ] Needs DOM/test harness or snapshot probe to inspect rendered duration color classes.
* [ ] Export checks require serializer utilities to exist.

---

## GAPS / IDEAS / QUESTIONS

* IDEA: export includes a deterministic header with session_id and schema version.

---

---
