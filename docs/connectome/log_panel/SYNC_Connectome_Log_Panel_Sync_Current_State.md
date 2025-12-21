```

# log_panel — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* unified “Now + Ledger” panel
* duration coloring rules exactly as specified
* trigger and call_type badges
* copy/export derived exclusively from store ledger

**In design:**

* filters and search (deferred)
* export format details (session header yes/no)

---

## CURRENT STATE

Implemented LogPanel with a “Now” section, ledger list, duration color rules, and copy/export buttons (JSONL + text) powered by state_store serializers.

---

## RECENT CHANGES

### 2026-03-28: Complete log panel patterns behavior template

* **What:** Added BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, and INSPIRATIONS sections with at least 50 characters per template block so the PATTERNS doc now satisfies the DOC_TEMPLATE_DRIFT expectations.
* **Why:** The doctor flagged those sections as missing or too brief, so the new narrative keeps the log panel’s design rationale tied to observable behaviors and cultural inspiration.
* **Files:** `docs/connectome/log_panel/PATTERNS_Connectome_Log_Panel_Unified_Explain_And_Copyable_Event_Ledger_View_Patterns.md`
* **Validation:** `ngram validate` *(fails: existing docs/connectome/health chain gaps, docs/physics naming/link warnings, and long-standing CHAIN issues tracked elsewhere).*

### 2025-12-20: Applied serif ledger headers and semantic palette badges

* **What:** Updated ledger header typography and badge colors to match the ecological gothic palette and monastic header style.
* **Why:** Make the log read like a carved ledger rather than a debug console.
* **Files:**
  * `app/connectome/connectome.css`

### 2025-12-20: Added log row hover tooltips

* **What:** Added hover tooltips on ledger rows for trigger/call/duration/payload/notes.
* **Why:** Provide hoverable remarks without adding visual clutter.
* **Files:** `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`.

### 2025-12-21: Added semantic search panel with threshold + hops sliders

* **What:** Added a search field, similarity slider, and hops slider that call the Connectome search API and render matches.
* **Why:** Enable semantic lookups and graph expansion directly from the left panel.
* **Files:** `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`, `app/connectome/connectome.css`.

### 2025-12-21: Added graph selector for existing graphs

* **What:** Added a graph selector that loads available graphs and scopes search requests.
* **Why:** Allow switching among existing FalkorDB graphs (default `seed`).
* **Files:** `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`, `app/api/connectome/graphs/route.ts`, `app/api/connectome/search/route.ts`, `app/connectome/connectome.css`.

### 2025-12-21: Default graph load in panel

* **What:** Load the full selected graph on panel mount and reveal all nodes/links.
* **Why:** Default to showing the entire graph without requiring a search.
* **Files:** `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`, `app/api/connectome/graph/route.ts`.

### 2025-12-20: Added colored node/link labels and trigger/call detail lines

* **What:** Rendered colored node labels and call-type-colored link labels in the ledger, plus explicit trigger/call detail text.
* **Why:** Make per-step causality and trigger semantics copy-friendly and visually scannable.
* **Files:**
  * `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`
  * `app/connectome/connectome.css`

### 2025-12-20: Implemented unified log panel

* **What:** Added LogPanel component, duration formatting helper, trigger/callType badge tokens, and export buttons.
* **Why:** Provide a single trustworthy log surface that matches the event ledger.
* **Files:**
  * `app/connectome/components/unified_now_and_copyable_ledger_log_panel.tsx`
  * `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts`
  * `app/connectome/components/connectome_log_trigger_and_calltype_badge_color_tokens.ts`
  * `app/connectome/components/connectome_log_export_buttons_using_state_store_serializers.tsx`

---

## TODO

* [ ] Add health probes for duration color correctness and export fidelity

Run:

```
pnpm connectome:health log_panel
```
