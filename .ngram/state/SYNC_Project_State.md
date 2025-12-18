# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent
```

---

## CURRENT STATE

ngram CLI project with doctor/repair functionality for maintaining project health.

---

## ACTIVE WORK

### Monolith Refactoring

- **Area:** `src/ngram/`
- **Status:** completed
- **Owner:** repair-agent
- **Context:** Reducing file sizes to meet 800-line threshold

---

## RECENT CHANGES

### 2025-12-18: Remove duplicate code from repair.py

- **What:** Removed ~270 lines of duplicate code from repair.py that was already defined in repair_interactive.py. Functions removed: print_progress_bar, input_listener_thread, spawn_manager_agent, check_for_manager_input, resolve_arbitrage_interactive, and associated global state variables.
- **Why:** MONOLITH issue - file was 983 lines (threshold: 800)
- **Impact:** repair.py reduced from 983 lines to 712 lines. Code now properly uses imports from repair_interactive.py instead of shadowing them with local duplicates.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| {description} | {level} | `{area}/` | {context} |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** {which VIEW}

**Current focus:** {what the project is working toward right now}

**Key context:**
{The things an agent needs to know that aren't obvious from the code/docs}

**Watch out for:**
{Project-level gotchas}

---

## HANDOFF: FOR HUMAN

**Executive summary:**
{2-3 sentences on project state}

**Decisions made recently:**
{Key choices with rationale}

**Needs your input:**
{Blocked items, strategic questions}

**Concerns:**
{Things that might be problems, flagged for awareness}

---

## TODO

### High Priority

- [ ] {Must do}

### Backlog

- [ ] {Should do}
- IDEA: {Possibility}

---

## CONSCIOUSNESS TRACE

**Project momentum:**
{Is the project moving well? Stuck? What's the energy like?}

**Architectural concerns:**
{Things that feel like they might become problems}

**Opportunities noticed:**
{Ideas that came up during work}

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `{area}/` | {status} | `docs/{area}/SYNC_*.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| {module} | `{code_path}` | `{docs_path}` | {status} |

**Unmapped code:** (run `ngram validate` to check)
- {List any code directories without module mappings}

**Coverage notes:**
{Any notes about why certain code isn't mapped, or plans to add mappings}
