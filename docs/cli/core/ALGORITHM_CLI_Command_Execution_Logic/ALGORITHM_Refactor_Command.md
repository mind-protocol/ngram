# ngram Framework CLI — Algorithm: Refactor Command

@ngram:id: CLI.REFRACTOR.ALGORITHM

```
STATUS: DESIGNING
CREATED: 2025-12-21
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ../BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ../ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md
THIS:            ALGORITHM_Refactor_Command.md
VALIDATION:      ../VALIDATION_CLI_Instruction_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md
HEALTH:          ../HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ../SYNC_CLI_Development_State.md
```

---

## PURPOSE

`ngram refactor` keeps the documentation graph and manifest in sync when paths move. It guarantees there is one authoritative implementation for structural changes by:

1. Paring the desired rename/move input.
2. Relocating the on-disk files/directories (docs, code modules, assets).
3. Rewriting every `docs/…` string (including `DOCS:` links, `.ngram/state` references, and `modules.yaml` entries).
4. Regenerating the project overview and re-running `ngram doctor` to refresh health state with the new layout.

The initial implementation focused on `rename`, but additional actions now exist: `move` (alias for rename), `promote` (raise a module out of its area), `demote` (place a module under an area), and `batch` (apply a filelist of refactor actions). Each action still runs the same post-workflow, so the results stay auditable.

The command can be extended to other refactor scenarios (`move`, `promote`, `demote`) once the rename flow handles the far-reaching ripple effects.

---

## STEPS

```
1. Parse args (`ngram refactor <action> ...`).
    2. Resolve paths relative to the project root (supporting `docs/…` and module directories).
    3. Move the filesystem item, creating parent directories for the target if needed.
    4. Compute canonical replacements (`old_rel` → `new_rel`, plus directory-slash variants).
    5. Scan every textual file under the project (`.md`, `.py`, `.yaml`, `.json`, etc.) and apply the replacements.
    6. Replace matching doc paths in `modules.yaml` and optionally rename the module key.
    7. Run `ngram overview --folder docs` and `ngram doctor` to refresh maps and health state.

For `batch`, each non-empty line is parsed as:
```
rename <old> <new>
move <old> <new>
promote <source> [target]
demote <module> <area>
```
Lines beginning with `#` are ignored.

Optional flags for each action:
`--overwrite` removes existing targets before moving (default), `--skip-existing` skips entries whose target already exists, and `--no-overwrite` turns off the default overwrite behavior. These flags are mutually exclusive.
```

The command is intentionally deterministic (always run overview + doctor after a structural change) so the system can claim the refactor is safe and auditable.

---

## DOCS INTEGRATION

`DOCS: ngram/refactor.py`

The implementation exposes `refactor_command()` and `refactor_rename()` to orchestrate the pipeline above. Every doc change it performs is tracked via the generated overview and doctor output.

---

## GAPS / IDEAS

- [ ] Hook `ngram refactor move` and `promote/demote` actions once a stable rename workflow is proven safe.
- IDEA: Add an `@ngram:thing:docs/...` tagging helper so the command can parse and update `@ngram:id` anchors automatically rather than relying on string replacements.
- QUESTION: Should `refactor` also adjust `@ngram:id` values when modules change names, or only file paths?
