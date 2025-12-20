# Archived: SYNC_Project_State.md

Archived on: 2025-12-20
Original file: SYNC_Project_State.md

---

## RECENT CHANGES

### 2025-12-20: Ran ngram validate after connectome doc import

- **What:** Executed `ngram validate` to check doc chain integrity after the bundle imports.
- **Why:** Confirm health of protocol docs and surface broken CHAIN links.
- **Impact:** Validation reports missing VIEW and multiple broken CHAIN links (details in latest CLI output); remediation needed.

### 2025-12-20: Strengthen prompt addition against symptom fixes

- **What:** Added an instruction + example to `templates/CODEX_SYSTEM_PROMPT_ADDITION.md` emphasizing underlying-issue fixes (BROKEN_IMPL_LINK example).
- **Why:** Make "fix root cause" behavior explicit in the Codex prompt template.
- **Impact:** Future AGENTS/CLAUDE prompt generation will include the new instruction.

### 2025-12-20: Expand operational proactivity guidance

- **What:** Added "don't pause before acting" and "always run HEALTH checks + verify doc chain" guidance to `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`.
- **Why:** Ensure agents act immediately and verify changes end-to-end, with docs kept current.
- **Impact:** Prompt template now explicitly requires action-first execution and health/doc verification.

### 2025-12-20: Split connectome doc bundle into module docs

- **What:** Added a splitter script and generated `docs/connectome/module/**` docs from `data/connectome/1.md`, rewriting `$$$` fences to Markdown ``` fences.
- **Why:** Turn the bundled connectome doc export into individual module docs that align with the protocol.
- **Impact:** New connectome doc chain files exist under `docs/connectome/module/`; script is reusable for future bundles.

### 2025-12-20: Split additional connectome bundles (2.md/3.md/4.md)

- **What:** Ran the bundle splitter on `data/connectome/2.md`, `data/connectome/3.md`, and `data/connectome/4.md`, rewriting `$$$` fences.
- **Why:** Import the remaining connectome documentation bundles into individual module docs.
- **Impact:** Additional connectome doc files were created/updated under `docs/connectome/`.

### 2025-12-20: Split connectome bundle 5.md

- **What:** Ran the bundle splitter on `data/connectome/5.md`, rewriting `$$$` fences.
- **Why:** Import the remaining connectome documentation bundle into individual module docs.
- **Impact:** Additional connectome doc files were created/updated under `docs/connectome/`.

### 2025-12-20: Import graph ownership files

- **What:** Copied 157 non-conflicting files from `~/the-blood-ledger` based on `data/graph_scope_classification.yaml`; skipped 45 conflicts; 4 source paths were missing upstream.
- **Why:** Bring the graph schema/physics/engine materials into this repo without overwriting existing protocol assets.
- **Impact:** New docs and engine files now exist under `docs/` and `engine/`, with remaining conflicts awaiting a decision.

### 2025-12-20: Reinitialize protocol + map

- **What:** Ran `ngram init` and `ngram map` to refresh `.ngram/` assets and regenerate the project map.
- **Why:** Ensure protocol files and map outputs are consistent after the intake.
- **Impact:** `map.md` updated and a temporary HTML map was generated at `/tmp/tmpk8j8x4s2.html`.

### 2025-12-20: Template skills for init installs

- **What:** Added `templates/ngram/skills` so `ngram init` can copy skills into `.ngram/skills`, `.claude/skills`, and `$CODEX_HOME/skills`.
- **Why:** Ensure protocol refreshes keep skills installed across agents without manual copying.
- **Impact:** `init_protocol` now installs skills and the behavior is verified with a temp init run.

### 2025-12-20: Strengthen prompt addition testing directive

- **What:** Updated `templates/CODEX_SYSTEM_PROMPT_ADDITION.md` to make the "always test" directive an explicit numbered requirement.
- **Why:** Make the testing mandate unmistakable in generated AGENTS/CLAUDE prompts.
- **Impact:** Future protocol bootstrap prompts will emphasize health checks and doc-chain verification.

### 2025-12-20: Add "never ask or wait" directive

- **What:** Added a directive to `templates/CODEX_SYSTEM_PROMPT_ADDITION.md` to proceed without pausing for user input.
- **Why:** Align agent operating posture with the current instruction set.
- **Impact:** Generated prompts will push autonomous execution and escalation markers when uncertain.

### 2025-12-20: Consolidate skills into `.ngram/skills`

- **What:** Used `ngram refactor batch` to move legacy skill files from `.claude/skills` into `.ngram/skills/legacy`, retaining the canonical `SKILL_*` set at `.ngram/skills`.
- **Why:** Standardize skills under `.ngram/skills` while preserving older variants for reference.
- **Impact:** `.claude/skills` is now empty and skill assets live under `.ngram/skills`.

### 2025-12-20: Refactor overwrite defaults

- **What:** Set `ngram refactor` to overwrite targets by default and added `--no-overwrite` to opt out.
- **Why:** Make batch operations deterministic even when targets already exist.
- **Impact:** Refactor collisions now default to replacement unless explicitly disabled.

---

