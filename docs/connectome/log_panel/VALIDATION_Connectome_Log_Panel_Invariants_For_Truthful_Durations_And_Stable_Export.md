```

# log_panel — Validation: Invariants for Truthful Durations and Stable Export

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md
THIS:            VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md
HEALTH:          ./HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md
SYNC:            ./SYNC_Connectome_Log_Panel_Sync_Current_State.md
```

---

## INVARIANTS

### V1: Explanation matches last event

```
If ledger non-empty:
Now.explanation corresponds to last ledger event (same id or derived from it)
```

### V2: “Step X of Y” formatting is unambiguous

```
Panel never shows shorthand like "#9/16"
It shows "Step X of Y" or "Step X" only
```

### V3: Duration color mapping matches rules

```
duration_ms undefined => muted
duration_ms < 1000    => blue
duration_ms < 2000    => yellow
duration_ms < 3000    => orange
duration_ms >= 3000   => red
```

### V4: Export equals ledger

```
Export JSONL contains all ledger events in order (plus optional session header)
Export Text contains all ledger events in order (plus optional session header)
```

---

## ERROR CONDITIONS

### E1: Export mismatch

* severity: ERROR
* meaning: copy/paste debugging is broken

### E2: Duration colored incorrectly

* severity: WARN/ERROR depending on frequency
* meaning: log cannot be trusted for performance intuition

---

## HEALTH COVERAGE

| Validation | Health Indicator                     |
| ---------- | ------------------------------------ |
| V1         | log_now_matches_last_event_integrity |
| V3         | log_duration_color_mapping_integrity |
| V4         | log_export_equals_ledger_integrity   |

---

## VERIFICATION PROCEDURE

### Manual

```
[ ] Step once → Now sentence describes that step
[ ] Look at Step indicator → “Step X of Y” (no shorthand)
[ ] Confirm ms durations appear blue
[ ] Copy JSONL and paste: event count equals ledger count
```

### Automated

```
pnpm connectome:health log_panel
```

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: Should “call_type” also have a badge in export text? (likely yes for readability)

---

---
