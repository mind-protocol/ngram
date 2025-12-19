# ngram Framework CLI — Behaviors: Command Effects and Observable Outcomes

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
THIS:            BEHAVIORS_CLI_Command_Effects.md (you are here)
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
TEST:            ./TEST_CLI_Coverage.md
SYNC:            ./SYNC_CLI_State.md
```

---

## BEHAVIORS

### B1: Init Command

```
GIVEN:  A project directory without ngram Framework
WHEN:   `ngram init` is executed
THEN:   .ngram/ directory is created with protocol files
AND:    .ngram/CLAUDE.md is created or updated with protocol bootstrap
AND:    AGENTS.md is created or updated with the bootstrap plus Codex guidance
AND:    modules.yaml template is copied to project root
AND:    Repository map is generated at docs/map.md
```

### B2: Init with Force

```
GIVEN:  A project with existing .ngram/
WHEN:   `ngram init --force` is executed
THEN:   Existing .ngram/ is removed
AND:    Fresh protocol files are copied
AND:    .ngram/CLAUDE.md and AGENTS.md are updated (not duplicated)
AND:    If removal fails due to permissions, init falls back to a partial refresh with warnings
```

### B3: Validate Command

```
GIVEN:  A project with ngram Framework installed
WHEN:   `ngram validate` is executed
THEN:   8 validation checks are run
AND:    Results are printed with pass/fail for each check
AND:    Exit code is 0 if all pass, 1 if any fail
AND:    Fix guidance is printed for failures
```

### B4: Doctor Command

```
GIVEN:  A project with ngram Framework installed
WHEN:   `ngram doctor` is executed
THEN:   12 health checks are run
AND:    Issues are grouped by severity (critical, warning, info)
AND:    Health score (0-100) is calculated
AND:    Results saved to .ngram/state/SYNC_Project_Health.md
AND:    Exit code is 0 even when issues are found
```

### B5: Repair Command

```
GIVEN:  A project with health issues from doctor
WHEN:   `ngram repair` is executed
THEN:   Repair agents are spawned for each issue
AND:    `--agents {claude,codex,gemini}` selects the agent provider
AND:    Agents follow appropriate VIEW for each issue type
AND:    Progress is streamed to terminal
AND:    Report saved to .ngram/state/REPAIR_REPORT.md
```

### B6: Context Command

```
GIVEN:  A source file path
WHEN:   `ngram context <file>` is executed
THEN:   Dependency map is printed
AND:    Linked documentation chain is found
AND:    Full doc content is printed
AND:    Access is logged to traces
```

### B7: Sync Command

```
GIVEN:  A project with SYNC files
WHEN:   `ngram sync` is executed
THEN:   SYNC file status is displayed
AND:    Large files (>200 lines) are auto-archived
```

### B8: Prompt Command

```
GIVEN:  A project with ngram Framework
WHEN:   `ngram prompt` is executed
THEN:   Bootstrap prompt for LLM is printed to stdout
AND:    Contains PROJECT, SYNC, MODULES sections
```

### B9: Overview Command

```
GIVEN:  A project directory
WHEN:   `ngram overview` is executed
THEN:   File tree is generated (respecting .gitignore/.ngramignore)
AND:    Timestamp added (YYYY-MM-DD HH:MM format)
AND:    Character counts shown for files and directories
AND:    Bidirectional links extracted (code→docs via DOCS:, docs→code via refs)
AND:    Cross-folder doc refs extracted
AND:    Section headers extracted from markdown files
AND:    Function/class definitions extracted from code files
AND:    Local imports extracted (stdlib/npm filtered out)
AND:    Module dependencies from modules.yaml included
AND:    Output saved to docs/map.{md|yaml|json}
```

**Options:**
- `--dir, -d PATH` — Target directory (default: cwd)
- `--format, -f {md,yaml,json}` — Output format (default: md)

### B10: Agents Command

```
GIVEN:  A project with ngram Framework
WHEN:   `ngram agents <agent_name>` is executed
THEN:   The specified agent is invoked with the given prompt and context
AND:    The agent's output is streamed to the terminal
```

**Agents:**
- `gemini` — Google Gemini (Note: `--system-prompt` is combined with `--prompt` due to CLI limitations)
- `claude` — Anthropic Claude
- `codex` — OpenAI Codex

---

## INPUTS / OUTPUTS

### Primary Function: `main()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| command | str | Subcommand name (init, validate, doctor, etc.) |
| --dir | Path | Target directory (default: cwd) |
| command-specific args | various | See each command |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| exit_code | int | 0 for success, 1 for failure |

**Side Effects:**

- Creates/modifies files in target directory
- Spawns subprocesses (repair command)
- Writes to stdout/stderr

---

## EDGE CASES

### E1: Protocol Not Installed

```
GIVEN:  validate/doctor run on project without .ngram/
THEN:   Returns failure with clear message
AND:    Suggests running `ngram init`
```

### E2: No Issues Found

```
GIVEN:  doctor run on healthy project
THEN:   Score is 100/100
AND:    No critical/warning issues listed
AND:    Exit code is 0
```

### E3: Empty Project

```
GIVEN:  init run on empty directory
THEN:   Protocol files are created
AND:    .ngram/CLAUDE.md is created from scratch
```

### E4: Context for Non-Existent File

```
GIVEN:  context command with non-existent file path
THEN:   Returns failure
AND:    Suggests checking path
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: No Duplicate Bootstrap Content

```
GIVEN:   .ngram/CLAUDE.md and AGENTS.md already have ngram Framework section
WHEN:    init is run
MUST NOT: Add duplicate protocol section
INSTEAD:  Skip update with message "already has ngram Framework section"
```

### A2: No Silent Failures

```
GIVEN:   Any command encounters an error
WHEN:    Processing fails
MUST NOT: Exit silently with code 0
INSTEAD:  Print error message and exit with code 1
```

### A3: No Destructive Init Without Force

```
GIVEN:   .ngram/ already exists
WHEN:    init is run without --force
MUST NOT: Overwrite existing files
INSTEAD:  Exit with error suggesting --force
```

### A4: Repair Must Not Skip SYNC Update

```
GIVEN:   Repair agent completes a fix
WHEN:    Changes are made
MUST NOT: Skip SYNC file update
INSTEAD:  Agent must update relevant SYNC with what changed
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Should `init` offer interactive mode to customize what gets installed?
- [ ] Consider adding `ngram status` combining doctor + sync
- IDEA: Watch mode for continuous health monitoring
- QUESTION: Should doctor auto-run before repair, or stay separate commands?
