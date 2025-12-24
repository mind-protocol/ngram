# Skill: `ngram.triage_unmapped_code`
@ngram:id: SKILL.TRIAGE.UNMAPPED_CODE.DECIDE_FATE

## Maps to VIEW
`.ngram/views/VIEW_Analyze_Structural_Analysis.md`

## Purpose
Evaluate orphan code/docs without objectives. Decide: integrate into existing module, create new module with objective, deprecate, or delete.

## When Invoked
Doctor creates a TRIAGE task when:
- Issues are detected for code that has no objective in the graph
- Chain traversal fails to find an objective narrative
- Code exists but isn't mapped to any module in modules.yaml

## Inputs (YAML)
```yaml
task_id: "narrative_TASK_triage-{module}_{index}"
# Example: narrative_TASK_triage-orphan-utils_01
module: "<orphan module or path>"
issues:
  - id: "narrative_ISSUE_{type}-{module}-{file}_{hash}"
    # Example: narrative_ISSUE_no-docs-ref-orphan-utils-helpers_c3
    type: "<issue_type>"
    path: "<file_path>"
    message: "<description>"
```

## Outputs (YAML)
```yaml
decision: integrate | create_module | deprecate | delete
rationale: "<why this decision>"

# If integrate:
integrate:
  target_module: "<existing module id>"
  files_to_move: ["<paths>"]
  objective_served: "<objective_id>"

# If create_module:
create_module:
  module_id: "<new module id>"
  docs_path: "docs/<area>/<module>/"
  objectives: ["documented", "tested", ...]
  add_to_modules_yaml: true

# If deprecate:
deprecate:
  reason: "<why deprecated>"
  archive_to: "tools/archive/<name>/"
  mark_in_modules_yaml: true

# If delete:
delete:
  reason: "<why delete>"
  files_to_remove: ["<paths>"]
  confirm_unused: true
```

## Decision Criteria

### Integrate
Choose when:
- Code is actively imported by existing modules
- Code logically belongs to an existing module's scope
- Small amount of code (< 3 files)

### Create Module
Choose when:
- Code is substantial (3+ files or 200+ lines)
- Code has clear, distinct purpose
- Code is actively used or will be needed
- No existing module is appropriate

### Deprecate
Choose when:
- Code was useful but superseded
- Code may be needed for reference
- Migration path exists to replacement
- Git history should be preserved

### Delete
Choose when:
- Code is unused (no imports, no references)
- Code is broken/incomplete with no value
- Code is duplicated elsewhere
- No git history worth preserving

## Investigation Steps

1. **Check usage**
   ```bash
   # Find imports of this code
   grep -r "from {module}" --include="*.py"
   grep -r "import {module}" --include="*.py"
   ```

2. **Check git history**
   ```bash
   # Recent activity?
   git log --oneline -10 -- {path}
   # Who owns this?
   git log --format="%an" -- {path} | sort | uniq -c
   ```

3. **Check tests**
   ```bash
   # Are there tests?
   find . -name "test_*" -path "*{module}*"
   ```

4. **Check docs**
   ```bash
   # Any existing documentation?
   find docs -name "*{module}*"
   ```

## Gates (non-negotiable)
- Must verify usage before delete decision
- Must check git history for recent activity
- Must document rationale for decision
- Must not delete code that is imported elsewhere
- Must create issue/escalation if uncertain

## Evidence & Referencing
- Git history: `git log --oneline -10 -- {path}`
- Usage: grep results showing imports
- Tests: presence/absence of test files

## Markers
- `@ngram:TODO <action to take>`
- `@ngram:escalation <if decision is unclear>`
- `@ngram:proposition <if suggesting architectural change>`

## Never-stop rule
If blocked or uncertain, create `@ngram:escalation` with:
- What you found
- Options considered
- Recommended action
- Why you're uncertain

Then move to next triage task.

## Example Output

```yaml
# Example: triage orphan utils/ directory

decision: integrate
rationale: |
  utils/ contains 2 small helper files (string_helpers.py, date_utils.py)
  both are imported by ngram_cli module. They logically belong there.

integrate:
  target_module: ngram-cli
  files_to_move:
    - utils/string_helpers.py
    - utils/date_utils.py
  objective_served: narrative_OBJECTIVE_ngram-cli-maintainable

actions:
  - Move files to ngram/helpers/
  - Update imports in ngram/*.py
  - Remove empty utils/ directory
  - Update modules.yaml
```

```yaml
# Example: triage abandoned TUI code

decision: deprecate
rationale: |
  TUI code was replaced by web UI (app/ngram/).
  Code is 800+ lines, has historical value.
  modules.yaml already marks ngram_tui as DEPRECATED.

deprecate:
  reason: "Replaced by web UI in app/ngram/"
  archive_to: "tools/archive/tui_2024/"
  mark_in_modules_yaml: true

actions:
  - Move ngram/tui/ to tools/archive/tui_2024/
  - Update or remove docs/tui/ (already deleted per git status)
  - Ensure modules.yaml shows DEPRECATED
```
