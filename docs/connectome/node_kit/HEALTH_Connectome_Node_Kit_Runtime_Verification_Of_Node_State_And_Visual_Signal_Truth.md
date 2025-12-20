```

# node_kit — Health: Runtime Verification of Node Signal Truthfulness

STATUS: DRAFT
CREATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

node_kit HEALTH ensures that nodes do not lie:

* active step highlight matches store.active_focus
* energy mapping buckets match deterministic rules
* wait/tick widgets respect bounds and precision
* node identity styling remains deterministic

This is not an aesthetics judge; it verifies trust signals.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md
BEHAVIORS:       ./BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md
ALGORITHM:       ./ALGORITHM_Connectome_Node_Kit_Node_Rendering_Spec_And_Energy_Glow_Mapping.md
VALIDATION:      ./VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md
IMPLEMENTATION:  ./IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md
THIS:            HEALTH_Connectome_Node_Kit_Runtime_Verification_Of_Node_State_And_Visual_Signal_Truth.md
SYNC:            ./SYNC_Connectome_Node_Kit_Sync_Current_State.md

IMPL:            ? (planned) scripts/connectome/health/node_kit_health_check_runner.ts
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```
flows_analysis:

* flow_id: node_focus_highlight_updates
  purpose: ensure active step highlight matches store state
  triggers:

  * type: manual
    source: runtime_engine Next click
    frequency:
    expected_rate: "human driven"
    risks:
  * "multiple active steps"
  * "highlight stuck on previous step"

* flow_id: node_energy_display_updates
  purpose: ensure energy mapping is deterministic and bounded
  triggers:

  * type: event
    source: state_store energy updates (derived from FlowEvents)
    frequency:
    expected_rate: "per step in stepper; high in realtime"
    risks:
  * "bucket mismatch"
  * "unbounded energy values"
    ```

---

## HEALTH INDICATORS SELECTED

```
health_indicators:

* name: node_active_step_singularity_integrity
  flow_id: node_focus_highlight_updates
  priority: high

* name: node_energy_color_bucket_integrity
  flow_id: node_energy_display_updates
  priority: med

* name: node_wait_progress_clamp_integrity
  flow_id: node_focus_highlight_updates
  priority: high

* name: node_tick_cron_progress_clamp_integrity
  flow_id: node_focus_highlight_updates
  priority: med
  ```

---

## CHECKER INDEX

```
checkers:

* name: health_check_only_one_step_is_highlighted_per_node
  purpose: "Assert V3: singular highlight."
  status: pending
  priority: high

* name: health_check_energy_value_maps_to_correct_bucket
  purpose: "Assert V4: energy->color mapping correct."
  status: pending
  priority: med

* name: health_check_wait_progress_seconds_bounded_and_precision
  purpose: "Assert V5: 0..4 and one decimal."
  status: pending
  priority: high

* name: health_check_tick_cron_progress_bounded
  purpose: "Assert V6: 0..1 and speed label correct."
  status: pending
  priority: med
  ```

---

## HOW TO RUN

```
pnpm connectome:health node_kit
```

---

## KNOWN GAPS

* [ ] Requires an implementation-level probe to read rendered “active step” state (test harness or DOM query).
* [ ] Energy range assumptions not finalized (may need normalization in state_store).

---

## GAPS / IDEAS / QUESTIONS

* IDEA: expose a debug-only “rendered node snapshot” object to simplify HEALTH checks.

---

---
