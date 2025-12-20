# Project — Sync: Current State

```
LAST_UPDATED: {DATE}
UPDATED_BY: {AGENT/HUMAN}
```

---

## CURRENT STATE

{Narrative of the project's current state. Not a feature list — the story of where things are.}

---

## ACTIVE WORK

### {Work Stream}

- **Area:** `{area}/`
- **Status:** {in progress / blocked}
- **Owner:** {agent/human}
- **Context:** {what's happening, why it matters}

---

## RECENT CHANGES

### 2025-12-20: Fix Gemini agent Pydantic validation errors

- **What:** Corrected the `history` initialization and tool result handling in `ngram/llms/gemini_agent.py`. Replaced the invalid `content` key with `parts` and wrapped tool outputs in `function_response` blocks as required by the `google-genai` SDK.
- **Why:** To resolve "Extra inputs are not permitted" errors triggered by Pydantic during LLM interactions.
- **Impact:** Stabilizes the Gemini agent communication loop, preventing crashes during tool-intensive tasks.

### 2025-12-20: Transition from TEST to HEALTH documentation format

- **What:** {description}
- **Why:** {motivation}
- **Impact:** {what this affects}

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
