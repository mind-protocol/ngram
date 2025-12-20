```

# log_panel — Algorithm: Rendering, Duration Coloring, Trigger Badges, and Export

STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against ?
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Log_Panel_Step_Clarity_And_Copyable_Audit_Trail_Effects.md
THIS:            ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md (you are here)
VALIDATION:      ./VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md
HEALTH:          ./HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md
SYNC:            ./SYNC_Connectome_Log_Panel_Sync_Current_State.md
```

---

## OVERVIEW

log_panel is a pure projection:

Inputs:

* store.ledger (FlowEvent[])
* store.current_explanation
* store.active_focus
* store.cursor + optional script_total
* store.health_badges

Outputs:

* Now section content
* Ledger list UI
* Export actions

---

## ALGORITHM: `render_now_section(store_state)`

1. Determine step index:

* step_index = store.cursor (or ledger length)
* step_total = runtime_engine script total if known else `?`

2. Determine current event:

* current_event = last element of ledger OR null

3. Render:

* Step label: “Step X of Y” (if Y known) else “Step X”
* Explanation sentence:

  * store.current_explanation.sentence
  * if missing: derive from current_event label/from/to else “?”

4. Render focus summary:

* “Active: from → to : label”
* badges for trigger + call_type

---

## ALGORITHM: `render_ledger_list(store_state)`

For each event e in ledger:

* render header row:

  * timestamp (or at_ms formatted)
  * trigger badge (colored)
  * call_type badge (colored)
  * duration field (colored by thresholds)
* render body:

  * label text (not bold)
  * payload_summary (if present)
  * rate_hint (if present)
  * notes (if “?”)

---

## ALGORITHM: duration formatting and coloring

### `format_duration_text(duration_ms)`

* if undefined: return “?”
* if <1000: return `${ms}ms`
* else: return `${(ms/1000).toFixed(2)}s`

### `duration_color_class(duration_ms)`

User rules:

```
IF duration_ms is undefined:
class = muted
ELSE IF duration_ms < 1000:
class = blue
ELSE IF duration_ms < 2000:
class = yellow
ELSE IF duration_ms < 3000:
class = orange
ELSE:
class = red
AND:
NOTE: <1s is “green” by severity, but user explicitly wants ms in blue.
Therefore:
duration_ms < 1000 => blue (unit-driven override)
```

Trigger badge colors (deterministic palette):

```
direct => blue-ish badge
stream => cyan-ish badge
async  => purple-ish badge
hook   => grey/teal badge (?)
timer  => grey/orange badge (?)
```

---

## ALGORITHM: export

### Export JSONL

* one JSON object per line
* includes session_id header line optionally:

  * `{"type":"session","session_id":"...","started_at_ms":...}`
* then events in order

### Export Text

* stable human-friendly lines:

  * `[tstamp] [trigger] [call_type] [duration] from→to label — payload_summary — rate_hint — notes`

Export must be derived from ledger only (no UI-only state).

---

## COMPLEXITY

* rendering: O(n)
* export: O(n)

---

## GAPS / IDEAS / QUESTIONS

* QUESTION: Should export include cursor and speed changes as synthetic events? (nice-to-have; possibly represented as call_type=code)

---

---
