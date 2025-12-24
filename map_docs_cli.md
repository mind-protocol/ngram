# Repository Map: ngram/docs/cli

*Generated: 2025-12-20 11:56*

## Statistics

- **Files:** 23
- **Directories:** 6
- **Total Size:** 81.6K
- **Doc Files:** 23
- **Code Files:** 0
- **Areas:** 6 (docs/ subfolders)
- **Modules:** 11 (subfolders in areas)
- **DOCS Links:** 0 (0 avg per code file)

### By Language

- markdown: 23

## File Tree

```
├── archive/ (3.0K)
│   ├── SYNC_CLI_Development_State_archive_2025-12.md (1.0K)
│   ├── SYNC_CLI_State_Archive_2025-12.md (1.7K)
│   └── (..1 more files)
├── core/ (44.3K)
│   ├── ALGORITHM_CLI_Command_Execution_Logic/ (8.5K)
│   │   ├── ALGORITHM_Overview.md (doctor & work section) (3.9K)
│   │   ├── ALGORITHM_Overview.md (init & validate section) (1.5K)
│   │   ├── ALGORITHM_Overview.md (marker scans section) (1.6K)
│   │   └── ALGORITHM_Overview.md (1.5K)
│   ├── IMPLEMENTATION_CLI_Code_Architecture/ (9.5K)
│   │   ├── IMPLEMENTATION_Code_Structure.md (3.9K)
│   │   ├── IMPLEMENTATION_Overview.md (1.9K)
│   │   ├── IMPLEMENTATION_Runtime_And_Dependencies.md (2.9K)
│   │   └── IMPLEMENTATION_Schema.md (725)
│   ├── BEHAVIORS_CLI_Command_Effects.md (5.3K)
│   ├── HEALTH_CLI_Command_Test_Coverage.md (6.3K)
│   ├── PATTERNS_Why_CLI_Over_Copy.md (4.8K)
│   ├── SYNC_CLI_Development_State.md (4.7K)
│   └── VALIDATION_CLI_Instruction_Invariants.md (5.3K)
├── prompt/ (33.1K)
│   ├── ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md (4.4K)
│   ├── BEHAVIORS_Prompt_Command_Output_and_Flow.md (3.5K)
│   ├── HEALTH_Prompt_Runtime_Verification.md (4.0K)
│   ├── IMPLEMENTATION_Prompt_Code_Architecture.md (5.6K)
│   ├── PATTERNS_Prompt_Command_Workflow_Design.md (4.7K)
│   ├── SYNC_Prompt_Command_State.md (6.2K)
│   └── VALIDATION_Prompt_Bootstrap_Invariants.md (4.7K)
└── modules.md (1.4K)
```

## File Details

### `archive/SYNC_CLI_Development_State_archive_2025-12.md`

**Code refs:**
- `ngram/work_core.py`

**Sections:**
- # Archived: SYNC_CLI_Development_State.md
- ## SUMMARY (2025-12)
- ## AGENT OBSERVATIONS (CONDENSED)

### `archive/SYNC_CLI_State_Archive_2025-12.md`

**Code refs:**
- `ngram/doctor_checks.py`

**Sections:**
- # Archived: SYNC_CLI_State.md
- ## MATURITY
- ## RECENT CHANGES (ARCHIVED)
- ## NOTES
- ## RELATED ARCHIVES
- ## CHAIN

### `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md (doctor & work section)`

**Sections:**
- # ngram Framework CLI — Algorithm: Doctor and Repair
- ## CONTEXT
- ## ALGORITHM: Doctor Command
- ## ALGORITHM: Repair Command
- # AGENTS.md = .ngram/CLAUDE.md + templates/CODEX_SYSTEM_PROMPT_ADDITION.md
- ## KEY DECISIONS
- # Safe fixes that only touch references
- # Also create/update documentation content
- # Also make code changes

### `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md (init & validate section)`

**Sections:**
- # ngram Framework CLI — Algorithm: Init and Validate
- ## CONTEXT
- ## ALGORITHM: Init Command
- ## ALGORITHM: Validate Command

### `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md (marker scans section)`

**Sections:**
- # ngram Framework CLI — Algorithm: Marker Scans and Support Utilities
- ## CONTEXT
- ## ALGORITHM: Solve Markers Command
- ## HELPER FUNCTIONS
- ## INTERACTIONS (HIGH-LEVEL)

### `core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`

**Sections:**
- # ngram Framework CLI — Algorithm: Command Processing Logic (Overview)
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## DATA FLOW (SUMMARY)
- ## PERFORMANCE NOTES

### `core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md`

**Code refs:**
- `ngram/agent_cli.py`
- `ngram/cli.py`
- `ngram/context.py`
- `ngram/core_utils.py`
- `ngram/doctor.py`
- `ngram/doctor_checks.py`
- `ngram/doctor_checks_content.py`
- `ngram/doctor_checks_docs.py`
- `ngram/doctor_checks_quality.py`
- `ngram/doctor_checks_sync.py`
- `ngram/doctor_files.py`
- `ngram/doctor_report.py`
- `ngram/doctor_types.py`
- `ngram/github.py`
- `ngram/init_cmd.py`
- `ngram/project_map.py`
- `ngram/project_map_html.py`
- `ngram/prompt.py`
- `ngram/work.py`
- `ngram/work_core.py`
- `ngram/work_escalation_interactive.py`
- `ngram/work_instructions.py`
- `ngram/work_instructions_docs.py`
- `ngram/work_report.py`
- `ngram/repo_overview.py`
- `ngram/repo_overview_formatters.py`
- `ngram/solve_escalations.py`
- `ngram/sync.py`
- `ngram/validate.py`

**Sections:**
- # ngram Framework CLI — Implementation: Code Structure
- ## CONTEXT
- ## CODE STRUCTURE
- ## FILE RESPONSIBILITIES

### `core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`

**Code refs:**
- `core_utils.py`
- `doctor_files.py`
- `ngram/cli.py`
- `ngram/doctor_checks.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`

**Sections:**
- # ngram Framework CLI — Implementation: Code Architecture and Structure (Overview)
- ## CHAIN
- ## OVERVIEW
- ## DESIGN PATTERNS
- ## BIDIRECTIONAL LINKS (ENTRY)
- ## GAPS (ACTIVE)
- ## ARCHIVE POINTER

### `core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`

**Sections:**
- # ngram Framework CLI — Implementation: Runtime and Dependencies
- ## CONTEXT
- ## ENTRY POINTS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION

### `core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md`

**Sections:**
- # ngram Framework CLI — Implementation: Schema
- ## CONTEXT
- ## SCHEMA

### `core/BEHAVIORS_CLI_Command_Effects.md`

**Doc refs:**
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`

**Sections:**
- # ngram Framework CLI — Behaviors: Command Effects and Observable Outcomes
- ## CHAIN
- ## BEHAVIORS
- ## NOTES

### `core/HEALTH_CLI_Command_Test_Coverage.md`

**Doc refs:**
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md`
- `docs/tui/HEALTH_TUI_Coverage.md`

**Sections:**
- # ngram Framework CLI — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## HOW TO USE THIS TEMPLATE
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Init Integrity
- ## HOW TO RUN
- # Run all health checks via validate
- # Run project health via doctor
- ## KNOWN GAPS
- ## GAPS / IDEAS / QUESTIONS

### `core/PATTERNS_Why_CLI_Over_Copy.md`

**Code refs:**
- `agent_cli.py`
- `context.py`
- `doctor.py`
- `github.py`
- `init_cmd.py`
- `project_map.py`
- `prompt.py`
- `work.py`
- `sync.py`
- `validate.py`

**Doc refs:**
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # ngram Framework CLI — Patterns: Why CLI Over Copy
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

### `core/SYNC_CLI_Development_State.md`

**Code refs:**
- `ngram/doctor_checks_content.py`
- `ngram/doctor_files.py`
- `ngram/prompt.py`
- `ngram/work_core.py`
- `ngram/solve_escalations.py`

**Doc refs:**
- `archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/SYNC_CLI_State.md`
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md (marker scans section)`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`

**Sections:**
- # ngram Framework CLI — Sync: Current State
- ## CHAIN
- ## CURRENT STATE
- ## IN PROGRESS
- ## KNOWN ISSUES
- ## CONFLICTS
- ## HANDOFF
- ## RECENT CHANGES
- ## GAPS
- ## Agent Observations
- ## ARCHIVE

### `core/VALIDATION_CLI_Instruction_Invariants.md`

**Doc refs:**
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`

**Sections:**
- # ngram Framework CLI — Validation: Invariants and Correctness Checks
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Run CLI commands manually for now
- # No automated test suite yet
- # TODO: Add pytest tests
- ## CHECK REFERENCES
- ## GAPS / IDEAS / QUESTIONS

### `prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md`

**Code refs:**
- `ngram/cli.py`
- `ngram/prompt.py`

**Doc refs:**
- `state/SYNC_Project_State.md`

**Sections:**
- # CLI Prompt — Algorithm: Assemble the bootstrap prompt
- ## CHAIN
- ## OVERVIEW
- ## DATA STRUCTURES
- ## ALGORITHM: `generate_bootstrap_prompt()`
- ## KEY DECISIONS
- ## DATA FLOW
- ## COMPLEXITY
- ## HELPER FUNCTIONS
- ## INTERACTIONS
- ## GAPS / IDEAS / QUESTIONS

### `prompt/BEHAVIORS_Prompt_Command_Output_and_Flow.md`

**Code refs:**
- `ngram/prompt.py`

**Doc refs:**
- `data/NGRAM Documentation Chain Pattern (Draft “Marco”).md`

**Sections:**
- # CLI Prompt — Behaviors: What the bootstrap command surfaces to agents
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

### `prompt/HEALTH_Prompt_Runtime_Verification.md`

**Code refs:**
- `ngram/prompt.py`

**Sections:**
- # CLI Prompt — Health: Runtime verification of bootstrap guidance
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES
- ## CHECKER INDEX
- ## GAPS / IDEAS / QUESTIONS

### `prompt/IMPLEMENTATION_Prompt_Code_Architecture.md`

**Code refs:**
- `ngram/cli.py`
- `ngram/prompt.py`

**Sections:**
- # CLI Prompt — Implementation: Code architecture and docking
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING
- ## LOGIC CHAINS
- ## GAPS / IDEAS / QUESTIONS

### `prompt/PATTERNS_Prompt_Command_Workflow_Design.md`

**Code refs:**
- `agent_cli.py`
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`

**Sections:**
- # CLI Prompt — Patterns: Workflow that surfacing protocol context
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

### `prompt/SYNC_Prompt_Command_State.md`

**Code refs:**
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`

**Sections:**
- # CLI Prompt Module — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

### `prompt/VALIDATION_Prompt_Bootstrap_Invariants.md`

**Code refs:**
- `ngram/prompt.py`

**Doc refs:**
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/protocol/HEALTH_Protocol_Verification.md`

**Sections:**
- # CLI Prompt — Validation: Bootstrap prompt invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

### `modules.md`

**Doc refs:**
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md`
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md`
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md`
- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`
- `docs/cli/core/SYNC_CLI_Development_State.md`
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md`
- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md`
- `docs/cli/prompt/SYNC_Prompt_Command_State.md`
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md`
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md`

**Sections:**
- # CLI Modules
