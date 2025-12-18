# Context Protocol CLI — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- `init` command — copies protocol files to target project
- `validate` command — checks protocol invariants
- `doctor` command — identifies health issues (monoliths, stale SYNCs, etc.)
- `repair` command — spawns Claude Code agents to fix issues
- `sync` command — manages SYNC files
- `context` command — navigates from code to docs
- `prompt` command — generates LLM bootstrap prompts
- `map` command — visual project mapping

**What's still being designed:**
- Parallel agent coordination in `repair` (works but output can be interleaved)
- GitHub issue integration depth (currently creates issues, could do more)
- Config.yaml structure for project-specific settings

**What's proposed (v2+):**
- Watch mode for continuous health monitoring
- MCP server integration for repairs
- IDE extension/plugin support

---

## CURRENT STATE

The CLI is functional and in active use. All core commands work:

**init**: Copies `.context-protocol/` directory and updates CLAUDE.md. Supports `--force` for re-initialization.

**validate**: Runs 8 validation checks including protocol installation, VIEW existence, module docs minimum, chain completeness, naming conventions, CHAIN link validity, and module manifest configuration.

**doctor**: Comprehensive health checks for 12 issue types (MONOLITH, UNDOCUMENTED, STALE_SYNC, PLACEHOLDER, INCOMPLETE_CHAIN, NO_DOCS_REF, BROKEN_IMPL_LINK, STUB_IMPL, INCOMPLETE_IMPL, UNDOC_IMPL, LARGE_DOC_MODULE, YAML_DRIFT). Generates SYNC-formatted health report. Supports GitHub issue creation.

**repair**: The most sophisticated command. Spawns Claude Code agents in parallel (default 5) to fix issues. Each agent follows a VIEW, reads required docs, makes focused changes, and updates SYNC. Supports depth levels (links, docs, full) and issue type filtering.

**sync**: Shows SYNC file status and auto-archives large files.

**context**: Given a file path, finds related documentation through modules.yaml mapping and DOCS: references.

**prompt**: Generates bootstrap prompt for LLMs working on the project.

**map**: Generates visual HTML map of modules and dependencies.

---

## IN PROGRESS

No active development at this time. The module was just documented.

---

## RECENT CHANGES

### 2025-12-18: Initial Documentation

- **What:** Created module documentation (PATTERNS + SYNC)
- **Why:** The `src/` directory had 12 files with no documentation mapping
- **Files:**
  - `modules.yaml` — added mapping
  - `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` — design rationale
  - `docs/cli/SYNC_CLI_State.md` — current state (this file)
- **Insights:** The CLI is mature enough for stable documentation. Core patterns are clear.

### Previous: Parallel Agent Execution

- **What:** Added `--parallel` flag to repair command
- **Why:** Sequential repairs were slow; parallel speeds up batch fixes
- **Files:** `repair.py`

### Previous: GitHub Integration

- **What:** Doctor command can create GitHub issues for findings
- **Why:** Track issues in the repo's native issue tracker
- **Files:** `github.py`, `doctor.py`

---

## KNOWN ISSUES

### Parallel Output Interleaving

- **Severity:** low
- **Symptom:** When running `repair --parallel`, agent outputs can intermix
- **Suspected cause:** Multiple agents writing to stdout simultaneously
- **Attempted:** Added per-agent colors and symbols for visual distinction

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Extend_Add_Features_To_Existing.md` (for new commands) or `VIEW_Debug_Investigate_And_Fix_Issues.md` (for bug fixes)

**Where I stopped:** Documentation complete. No pending work.

**What you need to understand:**
- Each command is in its own file under `src/context_protocol/`
- `cli.py` is the entry point that wires up argparse
- `utils.py` has shared utilities (template paths, module discovery)
- The repair system spawns `claude` subprocess with specific prompts

**Watch out for:**
- `repair.py` is complex — understand DEPTH_LINKS/DOCS/FULL before modifying
- YAML is optional dependency — code handles missing yaml gracefully
- Template files live in `templates/` at repo root (for dev) or in package (installed)

**Open questions I had:**
- Should repair depth default to "links" instead of "docs" for safer defaults?
- Is there value in a `context-protocol status` that combines doctor + sync output?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
CLI module now has documentation. All 8 commands work and are documented. Module mapping added to `modules.yaml`. The codebase health issue (UNDOCUMENTED for src/) is resolved.

**Decisions made:**
- Named module `context-protocol-cli` in modules.yaml (vs just `cli`)
- Put docs in `docs/cli/` (flat, not nested under an area)
- PATTERNS focuses on "why CLI over copy" as the core design question

**Needs your input:**
- None at this time

---

## TODO

### Immediate

- [x] Add modules.yaml mapping
- [x] Create PATTERNS doc
- [x] Create SYNC doc (this file)

### Later

- [ ] Create IMPLEMENTATION doc detailing file structure and data flows
- [ ] Consider adding BEHAVIORS doc for command specifications
- IDEA: Document the repair agent prompt templates in detail

---

## POINTERS

| What | Where |
|------|-------|
| CLI entry point | `src/context_protocol/cli.py` |
| Validation logic | `src/context_protocol/validate.py` |
| Health checks | `src/context_protocol/doctor.py` |
| Repair agents | `src/context_protocol/repair.py` |
| Module manifest | `modules.yaml` |
| Design rationale | `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` |
