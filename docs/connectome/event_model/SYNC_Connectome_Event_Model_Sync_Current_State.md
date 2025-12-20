```

# event_model — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**

* FlowEvent schema exists as the single contract for /connectome event meaning.
* Normalization is deterministic and never drops events (unknown → "?").

**What's still being designed:**

* exact backend SSE event list and payload shapes
* ordering policy under out-of-order realtime arrivals
* whether raw_payload is stored by default

**What's proposed (v2+):**

* parent_event_id causal tracing (span-like)
* OpenTelemetry-style export/import
* backend docks for richer telemetry snapshots

---

## CURRENT STATE

We are defining /connectome as an agent-first dashboard that renders from a single event ledger. The event_model module is the foundation: it specifies a canonical FlowEvent contract used by both stepper and realtime mode. Implementation does not exist yet; this chain is establishing the stable contract before code is written.

---

## IN PROGRESS

### V1 FlowEvent schema + normalization rules

* **Started:** 2025-12-20
* **By:** Marco "Salthand" (agent)
* **Status:** in progress
* **Context:** Without schema-first normalization, every other module duplicates meaning and drifts.

---

## RECENT CHANGES

### 2025-12-20: Initialized event_model chain docs

* **What:** Added PATTERNS/BEHAVIORS/ALGORITHM/VALIDATION/HEALTH/SYNC/IMPLEMENTATION drafts.
* **Why:** Establish stable contract first; unblock runtime_engine and telemetry_adapter.
* **Files:** docs/connectome/event_model/*
* **Struggles/Insights:** The hard part is deciding what is “unknown-but-preserved” vs “invalid”.

---

## KNOWN ISSUES

### Unknown backend payload shapes

* **Severity:** medium
* **Symptom:** realtime mapping cannot be finalized
* **Suspected cause:** SSE contracts may still be evolving elsewhere
* **Attempted:** Marked as `?` everywhere; deferred to telemetry_adapter and backend_docks

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Where I stopped:** At “schema-first” definition for FlowEvent and normalization algorithm.

**What you need to understand:**

* Every visualization and log line must come from FlowEvent.
* Unknowns must be preserved as “?”; no silent dropping.

**Watch out for:**

* “helpful” UI logic that re-derives colors/labels from raw payloads (anti-pattern).
* Storing raw payloads unbounded (memory/privacy).

**Open questions I had:**

* ordering policy (arrival vs at_ms)
* whether parent_event_id is required for v1

---

## HANDOFF: FOR HUMAN

**Executive summary:**
We froze the FlowEvent contract as the foundation of /connectome. Everything else should consume normalized events only.

**Decisions made:**

* unknown inputs are preserved and surfaced as “?”
* duration animations clamp to minimum 200ms
* trigger and call_type drive styling and log badges

**Needs your input:**

* ordering policy for realtime events
* whether to store raw payloads by default

---

## TODO

### Doc/Impl Drift

* [ ] DOCS→IMPL: Implement FlowEvent types + normalize_flow_event() per ALGORITHM.
* [ ] DOCS→IMPL: Implement duration bucketing and trigger/callType mapping per VALIDATION.

### Health to Run

```
pnpm connectome:health event_model
```

### Immediate

* [ ] Create TypeScript file(s) and export FlowEvent schema + normalization
* [ ] Add minimal unit-level health harness to validate V1/V3

### Later

* [ ] Add replay determinism checker for stepper mode
* IDEA: add parent_event_id support once causal chains matter

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Clear. The contract is the real system; visuals can change.

**Threads I was holding:**

* keep schema stable; prevent drift
* keep unknown visible; never drop
* connect durations to user trust

**Intuitions:**

* schema must be more stable than UI and more stable than backend payloads

**What I wish I'd known at the start:**

* realtime ordering and retention must be decided early or you regret it later

---

## POINTERS

| What                   | Where            |
| ---------------------- | ---------------- |
| FlowEvent schema draft | `ALGORITHM_...`  |
| Invariants             | `VALIDATION_...` |
| Health plan            | `HEALTH_...`     |

---
