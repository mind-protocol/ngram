```

# node_kit — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* typed node variants (Player/UI/Module/GraphQueries/Moment/Agent/TickCron)
* title prominent, file path discreet
* energy badge with deterministic bucket mapping
* internal step list with singular active highlight
* separate LLM CLI Agent nodes

**In design:**

* flipped node signal source
* energy scale assumptions (0..1 vs unbounded)

---

## CURRENT STATE

Implemented node component variants with consistent theming, energy badges, step lists, player wait progress, and tick cron ring. Active step highlight derives from state_store active_focus.

---

## RECENT CHANGES

### 2026-03-08: Complete node kit pattern sections

* **What:** Added the BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, DATA, and INSPIRATIONS sections to the node kit PATTERNS doc so every required template block now explains the allowed/blocked outcomes, data dependencies, and aesthetic touchpoints.
* **Why:** DOC_TEMPLATE_DRIFT #11 flagged those sections as missing, so enriching the pattern narrative keeps the module chain canonical before future work relies on the node rendering assumptions.
* **Files:**
  * `docs/connectome/node_kit/PATTERNS_Connectome_Node_Kit_Typed_Language_Coded_Energy_Aware_Node_Rendering_Patterns.md`
  * `docs/connectome/node_kit/SYNC_Connectome_Node_Kit_Sync_Current_State.md`
* **Verification:** `ngram validate`

### 2026-03-15: Expand node kit validation guarantees

* **What:** Rewove the validation BEHAVIORS GUARANTEED, OBJECTIVES COVERED, and PROPERTIES sections so each entry now exceeds 50 characters, ties the visible badge/highlight/timer contracts back to specific invariants, and explicitly states the deterministic palette/energy/timer wiring.
* **Why:** DOC_TEMPLATE_DRIFT #11 still flagged the validation template for missing or too-short narratives, so documenting the behavioral guarantees and property contract keeps downstream readers trusting the node readability invariants.
* **Files:**
  * `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md`
  * `docs/connectome/node_kit/SYNC_Connectome_Node_Kit_Sync_Current_State.md`
* **Verification:** `ngram validate` *(fails: known `docs/connectome/health` PATTERNS/SYNC gaps, `docs/engine/membrane/PATTERN_Membrane_Modulation.md` naming mismatch, and lingering CHAIN-link warnings already flagged by the validator).*

### 2026-03-07: Fill node kit validation template sections

* **What:** Added the missing `BEHAVIORS GUARANTEED`, `OBJECTIVES COVERED`, and `PROPERTIES` narratives to the node kit validation doc so each required template block exceeds the doctor's 50-character expectation and ties back to the existing invariants. 
* **Why:** DOC_TEMPLATE_DRIFT #11 reported those sections as absent, so the doc chain needed the explicit behavioral and property guarantees before downstream agents trust the readability contract.
* **Files:**
  * `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md`
  * `docs/connectome/node_kit/SYNC_Connectome_Node_Kit_Sync_Current_State.md`
* **Verification:** `ngram validate` *(fails: known `docs/connectome/health` PATTERNS/SYNC gaps, `docs/engine/membrane/PATTERN_Membrane_Modulation.md` naming mismatch, and lingering CHAIN-link warnings already reported by the doctor).*

### 2025-12-20: Applied ecological gothic palette tokens to node rendering

* **What:** Updated node title colors, step highlight colors, and wait/tick widget hues to use the semantic palette (`substrate/potential/stream/canon/membrane`).
* **Why:** Align node visuals with the Connectome visual style guide and remove neon/debug cues.
* **Files:**
  * `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
  * `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`
  * `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
  * `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`

### 2025-12-20: Applied inertial snap and viscous decay motion tokens

* **What:** Added inertial snap transitions for node focus and viscous decay for wait bar changes.
* **Why:** Align node motion with the physics-based easing terms in the style guide.
* **Files:** `app/connectome/connectome.css`, `app/globals.css`.

### 2025-12-20: Added node hover tooltips driven by ledger

* **What:** Added node hover tooltips showing last trigger/call/duration/notes.
* **Why:** Provide hoverable remarks without cluttering the node surface.
* **Files:**
  * `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
  * `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`

### 2025-12-20: Added live wait/tick progress animation updates

* **What:** Added timer-driven re-renders for the player wait bar and tick cron ring to reflect real-time progress without manual refresh.
* **Why:** Keep wait and tick signals truthful (max 4s wait bar, animated tick ring tied to nominal interval).
* **Files:**
  * `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
  * `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`

### 2025-12-20: Implemented node kit components

* **What:** Added node variants, shared frame, energy badge, wait/tick widgets, and theme tokens.
* **Why:** Provide readable, typed nodes with truthful signals for v1.
* **Files:**
  * `app/connectome/components/node_kit/typed_connectome_node_components_with_energy_and_step_highlighting.tsx`
  * `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
  * `app/connectome/components/node_kit/connectome_energy_badge_bucketed_glow_and_value_formatter.tsx`
  * `app/connectome/components/node_kit/connectome_player_wait_progress_bar_with_four_second_cap.tsx`
  * `app/connectome/components/node_kit/connectome_tick_cron_circular_progress_ring_with_speed_label.tsx`
  * `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts`
  * `app/connectome/components/node_kit/connectome_node_step_list_and_active_step_highlighter.tsx`

### 2025-12-21: Added React Flow handles to node frames

* **What:** Added source/target handles (with explicit ids) to node frames and hid them visually.
* **Why:** Prevent React Flow edge warnings about missing handles for custom nodes.
* **Files:**
  * `app/connectome/components/node_kit/connectome_node_frame_with_title_path_and_tooltip_shell.tsx`
  * `app/connectome/connectome.css`

---

## TODO

* [ ] Decide flipped node signal source
* [ ] Add health probes for active step singularity and energy bucket mapping

Run:

```
pnpm connectome:health node_kit
```

---
