# ngram Framework CLI — Algorithm: Marker Scans and Support Utilities

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CONTEXT

Entry point: `ALGORITHM_Overview.md`.

---

## ALGORITHM: Solve Markers Command

### Step 1: Load Ignore Patterns

```
config = load_doctor_config(target_dir)
ignore = config.ignore + [log files]
```

### Step 2: Scan for Escalation, Proposition, and Todo Tags

```
for file in repo_files:
    skip if ignored or binary
    if "@ngram&#58;escalation" or "@ngram&#58;doctor&#58;escalation" in content:
        collect file path as ESCALATION
    if "@ngram&#58;proposition" or "@ngram&#58;doctor&#58;proposition" in content:
        collect file path as PROPOSITION
    if "@ngram&#58;todo" or "@ngram&#58;doctor&#58;todo" in content:
        collect file path as TODO
```

### Step 3: Sort and Print

```
sort by priority (doctor escalation/proposition/todo first) and occurrence count
print numbered list and prompt human to resolve escalations or review propositions
```

---

## HELPER FUNCTIONS

- `find_module_directories()` — scan docs/ for module directories
- `should_ignore_path()` — check ignore patterns
- `get_issue_instructions()` — return VIEW + docs + prompt per issue type

---

## INTERACTIONS (HIGH-LEVEL)

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| utils.py | `get_templates_path()` | templates directory |
| utils.py | `find_module_directories()` | doc module list |
| doctor.py | `run_doctor()` | health results |
| repair.py | `spawn_repair_agent()` | RepairResult |
