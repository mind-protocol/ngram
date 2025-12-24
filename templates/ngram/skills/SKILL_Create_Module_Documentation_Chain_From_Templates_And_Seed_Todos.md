# Skill: `ngram.create_module_documentation`
@ngram:id: SKILL.DOCS.CREATE_CHAIN_FROM_TEMPLATES.SEED_TODOS

## Maps to VIEW
`.ngram/views/VIEW_Document_Create_Module_Documentation.md`

---

## Context

Doc chains in ngram follow: PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC.

Each doc type has specific purpose:
- PATTERNS: Design decisions, why this shape
- BEHAVIORS: Observable effects, what it does
- ALGORITHM: Procedures, how it works
- VALIDATION: Invariants, what must be true
- IMPLEMENTATION: Code architecture, where code lives
- HEALTH: Runtime verification, how to check
- SYNC: Current state, handoff info

Bidirectional pointers:
- Docs reference code: `file:symbol` in IMPLEMENTATION docking points
- Code references docs: `# DOCS: path/to/PATTERNS.md` comment in source files

Templates live in `.ngram/templates/`. Copy verbatim, fill placeholders.

---

## Purpose
Create module doc directory, copy templates into full chain, add TODO plans, establish doc↔code pointers.

---

## Inputs
```yaml
module: "<area/module>"           # string, e.g., "physics/tick"
templates_root: "<path>"          # string, default ".ngram/templates"
```

## Outputs
```yaml
created_files:
  - "docs/<area>/<module>/PATTERNS_*.md"
  - "docs/<area>/<module>/BEHAVIORS_*.md"
  - "docs/<area>/<module>/ALGORITHM_*.md"
  - "docs/<area>/<module>/VALIDATION_*.md"
  - "docs/<area>/<module>/IMPLEMENTATION_*.md"
  - "docs/<area>/<module>/HEALTH_*.md"
  - "docs/<area>/<module>/SYNC_*.md"
todos_added:
  - file: "<path>"
    todo: "@ngram:TODO <plan>"
```

---

## Gates

- Must use templates verbatim as base — prevents inconsistent structure
- Must add at least one `@ngram:TODO` per doc — tracks what needs filling
- Must establish bidirectional pointers — docs→code and code→docs

---

## Process

### 1. Check existing state
```yaml
batch_questions:
  - exists: "Does docs/<area>/<module>/ already exist?"
  - partial: "If partial, which docs are missing?"
  - code_exists: "Does the code at <module> path exist?"
```
If docs exist → extend, don't overwrite.

### 2. Create directory and copy templates
Copy each template, rename with module context:
- `PATTERNS_TEMPLATE.md` → `PATTERNS_<Module_Name>.md`

### 3. Add TODOs
Each doc gets at least one `@ngram:TODO` describing what to fill:
```markdown
@ngram:TODO Fill PATTERNS with design decisions for <module>
```

### 4. Establish pointers
- In IMPLEMENTATION: Add docking points referencing code files
- In code files: Add `# DOCS: docs/<area>/<module>/PATTERNS_*.md`

---

## Protocols Referenced

| Protocol | When | Creates |
|----------|------|---------|
| `protocol:explore_space` | Before creating | Check what exists |
| `protocol:create_doc_chain` | To create docs | Full doc chain (NOT YET IMPLEMENTED) |

---

## Evidence
- Docs: `@ngram:id + file + header`
- Code: `file + symbol`

## Markers
- `@ngram:TODO`
- `@ngram:escalation`
- `@ngram:proposition`

## Never-stop
If blocked → `@ngram:escalation` + `@ngram:proposition` → proceed with proposition.
