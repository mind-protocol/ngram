# ngram Framework CLI — Algorithm: Init and Validate

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CONTEXT

Entry point: `ALGORITHM_Overview.md`.

---

## ALGORITHM: Init Command

### Step 1: Preserve Learnings

```
if .ngram/views/*_LEARNINGS.md exists:
    preserve non-empty learnings
```

### Step 2: Copy Protocol Files

```
if .ngram/ exists and force:
    try rmtree(.ngram/)
    if permission error:
        copy files in place and warn
else:
    copytree(templates/ngram, .ngram/)
```

### Step 3: Write Bootstrap Files

```
write .ngram/CLAUDE.md
write AGENTS.md (.ngram/CLAUDE.md + CODEX_SYSTEM_PROMPT_ADDITION.md)
```

---

## ALGORITHM: Validate Command

### Step 1: Run All Checks

```
results = []
for check in [
    check_protocol_installed,
    check_views_exist,
    check_project_sync_exists,
    check_module_docs_minimum,
    check_full_chain,
    check_naming_conventions,
    check_chain_links,
    check_module_manifest,
]:
    results.append(check(target_dir))
```

### Step 2: Display Results

```
for result in results:
    if result.passed:
        print(f"✓ {result.name}")
    else:
        print(f"✗ {result.name}")
        for detail in result.details:
            print(f"  - {detail}")
```

### Step 3: Generate Fix Guidance

```
if any failures:
    for failed in results:
        print context-specific fix instructions
        print relevant VIEW to load
        print templates to use
```
