# Repository Map: ngram/docs/protocol

*Generated: 2025-12-20 11:56*

## Statistics

- **Files:** 19
- **Directories:** 6
- **Total Size:** 96.5K
- **Doc Files:** 19
- **Code Files:** 0
- **Areas:** 6 (docs/ subfolders)
- **Modules:** 11 (subfolders in areas)
- **DOCS Links:** 0 (0 avg per code file)

### By Language

- markdown: 19

## File Tree

```
├── ALGORITHM/ (2.5K)
│   └── ALGORITHM_Protocol_Process_Flow.md (2.5K)
├── IMPLEMENTATION/ (5.5K)
│   └── IMPLEMENTATION_Protocol_File_Structure.md (5.5K)
├── archive/ (839)
│   └── SYNC_Archive_2024-12.md (839)
├── doctor/ (46.2K)
│   ├── ALGORITHM_Project_Health_Doctor.md (17.3K)
│   ├── BEHAVIORS_Project_Health_Doctor.md (9.0K)
│   ├── HEALTH_Project_Health_Doctor.md (5.0K)
│   ├── PATTERNS_Project_Health_Doctor.md (4.0K)
│   ├── SYNC_Project_Health_Doctor.md (5.7K)
│   └── VALIDATION_Project_Health_Doctor.md (5.2K)
├── features/ (9.4K)
│   ├── BEHAVIORS_Agent_Trace_Logging.md (3.7K)
│   ├── PATTERNS_Agent_Trace_Logging.md (3.6K)
│   └── SYNC_Agent_Trace_Logging.md (2.0K)
├── ALGORITHM_Protocol_Core_Mechanics.md (569)
├── BEHAVIORS_Observable_Protocol_Effects.md (6.7K)
├── HEALTH_Protocol_Verification.md (5.6K)
├── IMPLEMENTATION_Protocol_System_Architecture.md (697)
├── PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md (5.0K)
├── SYNC_Protocol_Current_State.md (7.9K)
└── VALIDATION_Protocol_Invariants.md (5.7K)
```

## File Details

### `ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`

**Doc refs:**
- `templates/CLAUDE_ADDITION.md`
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `templates/ngram/agents/manager/CLAUDE.md`

**Sections:**
- # ngram Framework — Algorithm: Overview
- ## CHAIN
- ## OVERVIEW
- ## CONTENTS
- ## ALGORITHM: Install Protocol in Project
- ## ALGORITHM: Agent Starts Task
- ## ALGORITHM: Create New Module
- ## ALGORITHM: Modify Existing Module
- ## ALGORITHM: Document Cross-Cutting Concept
- ## NOTES

### `IMPLEMENTATION/IMPLEMENTATION_Protocol_File_Structure.md`

**Doc refs:**
- `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`

**Sections:**
- # ngram Framework — Implementation: Overview
- ## CHAIN
- ## OVERVIEW
- ## FILE STRUCTURE
- ## SCHEMAS AND CONFIG
- ## FLOWS AND LINKS
- # DOCS: docs/{area}/{module}/PATTERNS_*.md

### `archive/SYNC_Archive_2024-12.md`

**Sections:**
- # Archived: Protocol SYNC Notes (2024-12)
- ## SUMMARY OF 2024-12 CHANGES
- ## ARCHIVED NOTES

### `doctor/ALGORITHM_Project_Health_Doctor.md`

**Sections:**
- # ALGORITHM: Project Health Doctor
- ## MAIN FLOW
- ## 1. LOAD CONFIGURATION
- ## 2. DISCOVER PROJECT STRUCTURE
- # Also find subdirectories
- ## 3. RUN CHECKS
- # Check if mapped in modules.yaml
- # Check for template placeholders
- # Look for DOCS: comment
- # Find most recent SYNC update across all SYNC files
- # 1. Folders must be snake_case
- # 2. Code files must be snake_case.py and not contain 'and'
- # 3. Doc files must be PREFIX_PascalCase_With_Underscores.md
- # Group into tasks of 10
- # Skip if no docs at all (that's UNDOCUMENTED, not ABANDONED)
- # Check if only has PATTERNS or SYNC (started but not continued)
- # Started (has 1-2 docs) but incomplete (missing 3+ docs)
- # Check if stale
- # Check directories
- # Check files
- ## 4. AGGREGATE RESULTS
- # Apply severity overrides
- # Group by severity
- ## 5. CALCULATE SCORE
- ## 6. GENERATE OUTPUT
- ## 7. EXIT CODE
- ## CHAIN

### `doctor/BEHAVIORS_Project_Health_Doctor.md`

**Sections:**
- # BEHAVIORS: Project Health Doctor
- ## COMMAND INTERFACE
- # Basic health check
- # With specific directory
- # Output formats
- # Filter by severity
- # Specific checks
- ## HEALTH CHECKS
- ## SPECIAL MARKERS
- ## OUTPUT BEHAVIOR
- ## Critical (2 issues)
- ## Warnings (3 issues)
- ## Info (3 issues)
- ## Suggested Actions
- ## GUIDED REMEDIATION
- ## Current State
- ## Recommended Steps
- # DOCS: docs/api/PATTERNS_Api_Design.md
- ## Template Commands
- # Generate PATTERNS from template
- ## Reference
- ## EXIT CODES
- ## CONFIGURATION
- # Thresholds
- # Ignore patterns
- # Disable specific checks
- # Custom severity overrides
- ## FALSE POSITIVE SUPPRESSION
- ## DOC TEMPLATE DRIFT DEFERMENTS
- ## NON-STANDARD DOC TYPE DEFERMENTS
- ## RESOLVED ESCALATION MARKERS
- ## CHAIN

### `doctor/HEALTH_Project_Health_Doctor.md`

**Code refs:**
- `doctor_checks.py`
- `doctor_report.py`
- `ngram/doctor.py`

**Doc refs:**
- `docs/tui/HEALTH_TUI_Coverage.md`

**Sections:**
- # Project Health Doctor — Health: Verification Mechanics and Coverage
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Score Sanity
- ## HOW TO RUN
- # Run all doctor checks on the current project
- # Run with JSON output for machine parsing
- ## KNOWN GAPS
- ## GAPS / IDEAS / QUESTIONS

### `doctor/PATTERNS_Project_Health_Doctor.md`

**Sections:**
- # PATTERNS: Project Health Doctor
- ## THE PROBLEM
- ## THE INSIGHT
- ## DESIGN DECISIONS
- ## WHAT WE CHECK
- ## WHAT WE DON'T CHECK
- ## ALTERNATIVES CONSIDERED
- ## CHAIN

### `doctor/SYNC_Project_Health_Doctor.md`

**Code refs:**
- `doctor.py`

**Doc refs:**
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md`

**Sections:**
- # SYNC: Project Health Doctor
- ## MATURITY
- ## CURRENT STATE
- ## IMPLEMENTATION ORDER
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## GAPS
- ## CHAIN

### `doctor/VALIDATION_Project_Health_Doctor.md`

**Sections:**
- # VALIDATION: Project Health Doctor
- ## INVARIANTS
- ## CHECK CORRECTNESS
- ## OUTPUT FORMAT CORRECTNESS
- ## EDGE CASES
- ## PERFORMANCE BOUNDS
- ## VERIFICATION COMMANDS
- # Verify determinism
- # Verify exit codes
- # Verify JSON validity
- # Verify ignore patterns
- ## CHAIN

### `features/BEHAVIORS_Agent_Trace_Logging.md`

**Sections:**
- # Agent Trace Logging — Behaviors: Observable Effects
- ## CHAIN
- ## COMMANDS
- ## AUTOMATIC TRACING
- ## TRACE FILE FORMAT
- ## INTEGRATION POINTS
- ## Usage (auto-generated)
- ## WHAT GETS TRACED
- ## WHAT DOESN'T GET TRACED

### `features/PATTERNS_Agent_Trace_Logging.md`

**Sections:**
- # Agent Trace Logging — Patterns: Why This Design
- ## CHAIN
- ## THE PROBLEM
- ## THE INSIGHT
- ## DESIGN DECISIONS
- ## WHAT THIS ENABLES
- ## TRADEOFFS
- ## ALTERNATIVES CONSIDERED
- ## OPEN QUESTIONS

### `features/SYNC_Agent_Trace_Logging.md`

**Code refs:**
- `ngram/cli.py`

**Sections:**
- # Agent Trace Logging — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IMPLEMENTATION PLAN
- ## HANDOFF: FOR AGENTS
- ## TODO
- ## OPEN QUESTIONS

### `ALGORITHM_Protocol_Core_Mechanics.md`

**Sections:**
- # ngram Framework — Algorithm: Overview
- ## CHAIN
- ## ENTRY POINT

### `BEHAVIORS_Observable_Protocol_Effects.md`

**Sections:**
- # ngram Framework — Behaviors: Observable Protocol Effects
- ## CHAIN
- ## BEHAVIORS
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS
- ## GAPS / IDEAS / QUESTIONS

### `HEALTH_Protocol_Verification.md`

**Code refs:**
- `ngram/prompt.py`
- `ngram/validate.py`

**Doc refs:**
- `docs/cli/HEALTH_CLI_Coverage.md`

**Sections:**
- # ngram Framework — Health: Protocol Verification and Mechanics
- ## PURPOSE OF THIS FILE
- ## WHY THIS PATTERN
- ## CHAIN
- ## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)
- ## HEALTH INDICATORS SELECTED
- ## STATUS (RESULT INDICATOR)
- ## DOCK TYPES (COMPLETE LIST)
- ## CHECKER INDEX
- ## INDICATOR: Chain Completeness
- ## HOW TO RUN
- # Verify protocol health for the current project
- # Verify a specific module
- ## KNOWN GAPS
- ## GAPS / IDEAS / QUESTIONS

### `IMPLEMENTATION_Protocol_System_Architecture.md`

**Doc refs:**
- `docs/protocol/ALGORITHM/ALGORITHM_Protocol_Process_Flow.md`

**Sections:**
- # ngram Framework — Implementation: Overview
- ## CHAIN
- ## ENTRY POINT

### `PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`

**Sections:**
- # ngram Framework — Patterns: Bidirectional Documentation Chain for AI Agent Workflows
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- # Descriptive names
- # Not
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## WHAT THIS DOES NOT SOLVE
- ## GAPS / IDEAS / QUESTIONS

### `SYNC_Protocol_Current_State.md`

**Code refs:**
- `ngram/cli.py`

**Doc refs:**
- `archive/SYNC_archive_2024-12.md`
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md`
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_File_Structure.md`
- `docs/protocol/PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md`
- `docs/protocol/SYNC_Protocol_Current_State.md`
- `templates/CLAUDE_ADDITION.md`
- `templates/ngram/PRINCIPLES.md`
- `templates/ngram/PROTOCOL.md`

**Sections:**
- # ngram Framework — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## STRUCTURE
- ## POINTERS
- ## ARCHIVE
- ## Agent Observations
- ## GAPS

### `VALIDATION_Protocol_Invariants.md`

**Code refs:**
- `scripts/check_chain_links.py`
- `scripts/check_doc_completeness.py`
- `scripts/check_doc_refs.py`
- `scripts/check_orphans.py`

**Sections:**
- # ngram Framework — Validation: Protocol Invariants
- ## CHAIN
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- # Check all invariants
- # Check specific invariant
- # Check specific module
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS
