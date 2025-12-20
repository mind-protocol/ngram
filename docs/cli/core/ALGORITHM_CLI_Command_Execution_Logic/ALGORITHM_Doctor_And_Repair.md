# ngram Framework CLI — Algorithm: Doctor and Repair

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CONTEXT

Entry point: `ALGORITHM_Overview.md`.

---

## ALGORITHM: Doctor Command

### Step 1: Load Configuration

```
config = load_doctor_config(target_dir)
  - Parse .gitignore patterns
  - Load config.yaml settings if exists
  - Set thresholds (monolith_lines, stale_sync_days)
```

### Step 2: Run Health Checks

```
all_issues = []
for check in [
    doctor_check_monolith,       # Files > 500 lines
    doctor_check_undocumented,   # Code without docs mapping
    doctor_check_stale_sync,     # SYNC older than 14 days
    doctor_check_placeholder,    # Unfilled templates
    doctor_check_no_docs_ref,    # Source without DOCS: comment
    doctor_check_incomplete_chain,
    doctor_check_broken_impl_links,
    doctor_check_stub_impl,
    doctor_check_incomplete_impl,
    doctor_check_undoc_impl,
    doctor_check_large_doc_module,
    doctor_check_yaml_drift,
    doctor_check_recent_log_errors,  # Recent .log errors (last hour)
]:
    all_issues.extend(check(target_dir, config))
```

### Step 3: Calculate Health Score

```
score = 100
score -= len(critical_issues) * 10
score -= len(warning_issues) * 3
score -= len(info_issues) * 1
score = max(0, score)
```

### Step 4: Randomize Issue Order

```
shuffle issues within each severity bucket
```

### Step 5: Save Report

```
markdown = generate_health_markdown(results)
write to .ngram/state/SYNC_Project_Health.md
```

---

## ALGORITHM: Repair Command

### Step 1: Identify Issues

```
results = run_doctor(target_dir, config)
issues = results.critical + results.warning
filter by depth level (links, docs, full)
filter by explicit type if specified
sort by priority (YAML_DRIFT first, NO_DOCS_REF last)
```

### Step 2: Build Agent Prompts

```
for issue in issues:
    instructions = get_issue_instructions(issue)
    existing_docs, missing_docs = split_docs_to_read(instructions.docs_to_read)
    prompt = build_agent_prompt(
        issue=issue,
        view=instructions.view,
        docs_to_read=instructions.docs,
        task_description=instructions.prompt,
    )
    # AGENTS.md = .ngram/CLAUDE.md + templates/CODEX_SYSTEM_PROMPT_ADDITION.md
```

**Docs preflight:** Missing docs are listed in a `Missing Docs at Prompt Time` section so agents can resolve paths before edits.

### Step 3: Spawn Agents (Parallel)

```
with ThreadPoolExecutor(max_workers=parallel) as executor:
    futures = {
        executor.submit(spawn_repair_agent, issue): issue
        for issue in issues
    }
    for future in as_completed(futures):
        result = future.result()
        repair_results.append(result)
```

### Step 4: Execute Agent (per issue)

```
cmd = build_agent_command(
    agent_provider,
    prompt=prompt,
    system_prompt=AGENT_SYSTEM_PROMPT,
    stream_json=(agent_provider == "claude"),
    continue_session=False,
)
process = subprocess.Popen(cmd, stdout=PIPE)
stream output, parse JSON (Claude) or text (Gemini/Codex), show progress
check for "REPAIR COMPLETE" or "REPAIR FAILED"
```

### Step 5: Generate Report

```
run doctor again to get after_results
compare before/after scores
list successful and failed repairs
save to .ngram/state/REPAIR_REPORT.md
```

---

## KEY DECISIONS

### D1: Depth Filtering

```
IF depth == "links":
    allowed = {NO_DOCS_REF, BROKEN_IMPL_LINK, YAML_DRIFT, UNDOC_IMPL}
    # Safe fixes that only touch references
ELIF depth == "docs":
    allowed = links + {UNDOCUMENTED, STALE_SYNC, PLACEHOLDER, INCOMPLETE_CHAIN, LARGE_DOC_MODULE}
    # Also create/update documentation content
ELSE (full):
    allowed = docs + {MONOLITH, STUB_IMPL, INCOMPLETE_IMPL}
    # Also make code changes
```

### D2: Issue Priority

```
priority_order = {
    YAML_DRIFT: 1,
    BROKEN_IMPL_LINK: 2,
    UNDOCUMENTED: 3,
    INCOMPLETE_CHAIN: 4,
    PLACEHOLDER: 5,
    ...
    NO_DOCS_REF: 12,
}
```
