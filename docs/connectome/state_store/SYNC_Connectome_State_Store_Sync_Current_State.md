# state_store — Sync: Current State

LAST_UPDATED: 2026-02-10
UPDATED_BY: codex
STATUS: DESIGNING

---

## MATURITY

**Canonical (v1 intent):**

* one store owns ledger + focus + timers + explanation
* atomic commit per step release
* append-only ledger within a session

**In design:**

* realtime retention policy (max N vs time window)

**Deferred:**

* realtime ingestion details
* pinned focus behavior

---

## CURRENT STATE

Implemented a Zustand store with explicit long-named actions. Step releases use a single atomic commit that appends to the ledger, sets focus, updates explanation, and adjusts wait timers. Restart currently appends a session boundary event and resets focus/timers. The implementation doc now enumerates schema, docking flows, logic chains, dependencies, runtime behavior, and the concurrency guarantees so human agents can follow the canonical design without encountering DOC_TEMPLATE_DRIFT.

---

## RECENT CHANGES

### 2026-03-01: Complete state store health template coverage

- **What:** Filled the WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, OBJECTIVES COVERAGE, STATUS, DOCK TYPES, and INDICATOR sections so the health doc now lists every required narrative plus a result stream tied to the atomic commit indicator.
- **Why:** DOC_TEMPLATE_DRIFT #11 flagged the state store health doc for missing template blocks; the expanded coverage keeps the health chain aligned with the implementation story without touching the store itself.
- **Files:** `docs/connectome/state_store/HEALTH_Connectome_State_Store_Runtime_Verification_Of_Ledger_And_Timer_Correctness.md`, `docs/connectome/state_store/SYNC_Connectome_State_Store_Sync_Current_State.md`
- **Verification:** `ngram validate`

### 2026-02-10: Document state store behavior guardrails

* **What:** Added the BEHAVIORS SUPPORTED and BEHAVIORS PREVENTED sections to the PATTERNS doc so the state_store’s behavioral guardrails are explicit and each block now exceeds the 50-character DOC_TEMPLATE_DRIFT requirement.
* **Why:** DOC_TEMPLATE_DRIFT #11 flagged the missing behavior blocks, so the new prose keeps the canonical pattern aligned with the store’s ledger/focus/timer semantics before downstream agents commit code.
* **Files:** `docs/connectome/state_store/PATTERNS_Connectome_State_Store_Single_Source_Of_Truth_For_Events_Focus_And_Timers.md`, `docs/connectome/state_store/SYNC_Connectome_State_Store_Sync_Current_State.md`
* **Verification:** `ngram validate`

### 2026-02-01: Expand state store implementation collateral

* **What:** Added SCHEMA, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, RUNTIME BEHAVIOR, and CONCURRENCY MODEL sections to the implementation doc and recorded the Observations trace so the doc chain satisfies DOC_TEMPLATE_DRIFT (#11).
* **Why:** The doctor flagged the implementation doc for missing atlas sections; expanding it keeps the store chain aligned with the PATTERNS/ALGORITHM expectations before we ship.
* **Files:** `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md`, `docs/connectome/state_store/SYNC_Connectome_State_Store_Sync_Current_State.md`
* **Verification:** `ngram validate`

### 2025-12-20: Implemented state store with atomic commits

* **What:** Added store state, atomic commit action, restart policy, and serializer utilities.
* **Why:** Provide a single source of truth to prevent UI/log drift.
* **Files:**
  * `app/connectome/lib/zustand_connectome_state_store_with_atomic_commit_actions.ts`
  * `app/connectome/lib/connectome_session_boundary_and_restart_policy_controller.ts`
  * `app/connectome/lib/connectome_wait_timer_progress_and_tick_display_signal_selectors.ts`
  * `app/connectome/lib/connectome_export_jsonl_and_text_log_serializer.ts`

---

## TODO

* [ ] Decide retention cap for realtime mode
* [ ] Add health harness to verify atomic commit invariants

Run:

```
pnpm connectome:health state_store
```

---

## AGENT OBSERVATIONS

### Remarks

* The implementation doc now lists the missing schema, flow, logic, dependency, runtime, and concurrency guidance so the chain is doc-template-compliant.
* Completed the PATTERNS behaviors template so the guardrail summary now lives next to the problem/pattern narrative.
