# Tools — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tools.md
BEHAVIORS:       ./BEHAVIORS_Tools.md
ALGORITHM:       ./ALGORITHM_Tools.md
VALIDATION:      ./VALIDATION_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tools.md
HEALTH:          ./HEALTH_Tools.md
THIS:            ./SYNC_Tools.md
```

---

## CURRENT STATE

Documented the tools module so utility scripts are tracked in the protocol.
Added systemd user unit templates under `tools/systemd/user/`, a v3 ngrok
config at `tools/ngrok.yml`, and a WSL autostart guide at
`docs/infrastructure/wsl-autostart.md`. Added `.ngram/logs/` plus a
`.ngram/systemd.env` placeholder to wire frontend commands into systemd.
Added `blood-fe.service` to run the `the-blood-ledger` frontend and wired it
into `ngram-stack.target`.
Expanded `docs/tools/VALIDATION_Tools.md` so the validation template now
includes behaviors guaranteed, objectives covered, properties, error
conditions, health coverage, verification procedures, sync status, and gap
analysis narratives that each exceed the 50-character guidance. Expedited
`docs/tools/ALGORITHM_Tools.md` so the algorithm ledger now highlights the
bundle splitter, dialogue streamer, and stack runner flows through overview,
objectives, data structures, algorithm callouts, decisions, data flow,
complexity, helper functions, interactions, and gaps sections so future agents
see how those helpers satisfy the protocol template requirements. Expanded
`docs/tools/HEALTH_Tools.md` so the health ledger now lists PURPOSE OF THIS
FILE, WHY THIS PATTERN, FLOWS ANALYSIS, HEALTH INDICATORS, OBJECTIVES,
STATUS, DOCK TYPES, CHECKER INDEX, indicator narratives, HOW TO RUN guidance,
and GAPS/IDEAS/QUESTIONS narratives that each exceed 50 characters.

## Agent Observations

### Remarks
- No frontend start command exists in-repo; `ngram-fe.service` now requires
  `FE_CMD` in `.ngram/systemd.env`.
- `ngram-fe.service` now targets `~/ngram/frontend`; the blood frontend has its
  own unit.
- The updated ALGORITHM doc now narrates how the bundle splitter, the narrator
  stream, and the helper stack interact so DOC_TEMPLATE_DRIFT warnings are kept
  in check on this module.
- The HEALTH doc now records flows, indicator coverage, and the checker index
  so DOC_TEMPLATE_DRIFT guardrails are satisfied for this module.

### Suggestions
- [ ] Confirm the exact frontend start command and update
  `.ngram/systemd.env` so `ngram-fe.service` can start cleanly.
- [ ] Confirm the blood frontend port/command once its build is finalized.

### Propositions
- If a canonical frontend repo exists, add a brief doc link here so future
  agents can locate its startup command quickly.

## TODO

- [ ] Add fixtures and run examples for each script to validate outputs.

## RECENT CHANGES

### 2026-01-13: Document tools algorithm template coverage

- **What:** Added the missing overview, objectives, data structures, algorithm
  callout, key decisions, data flow, complexity, helper functions, interactions,
  and gaps sections to `docs/tools/ALGORITHM_Tools.md`, giving each block more
  than 50 characters and tying the narrative back to the bundle splitter and
  stream dialogue helpers.
- **Why:** DOC_TEMPLATE_DRIFT flagged `docs/tools/ALGORITHM_Tools.md` for
  omitting the required sections, so the new narrative keeps the module
  compliant without touching the scripts themselves.
- **Files:** `docs/tools/ALGORITHM_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known
  docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN
  naming mismatch, and the existing CHAIN/link warnings).*

### 2026-01-05: Document tools validation template coverage

- **What:** Filled `docs/tools/VALIDATION_Tools.md` with the missing validation sections (behaviors guaranteed, objectives covered, properties, error conditions, health coverage, verification procedures, sync status, and gaps/ideas/questions) so every template block now meets the 50+ character expectation.
- **Why:** DOC_TEMPLATE_DRIFT warned that the validation template lacked the required narrative anchors, so this update keeps the canonical ledger authoritative without modifying the runtime scripts.
- **Files:** `docs/tools/VALIDATION_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).)*

### 2025-12-21: Expand tools algorithm template coverage

- **What:** Filled `docs/tools/ALGORITHM_Tools.md` with the missing overview, objectives, data structure, function-level, and interaction sections so every template block now exceeds the 50-character guidance.
- **Why:** DOC_TEMPLATE_DRIFT flagged the algorithm doc for lacking the required subsections, so this change keeps the module's narrative aligned with the rest of the protocol without touching the scripts themselves.
- **Files:** `docs/tools/ALGORITHM_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).)*
