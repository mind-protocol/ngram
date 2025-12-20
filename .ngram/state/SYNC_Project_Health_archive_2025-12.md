# Archived: SYNC_Project_Health.md

Archived on: 2025-12-20
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (18 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `ngram` - No documentation mapping (55 files)
  - Add mapping to modules.yaml
- `ngram/llms` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `ngram/tui` - No documentation mapping (17 files)
  - Add mapping to modules.yaml
- `ngram/tui/widgets` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine` - No documentation mapping (55 files)
  - Add mapping to modules.yaml
- `engine/models` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/moments` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/graph/health` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine/scripts` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- ... and 8 more

### BROKEN_IMPL_LINK (13 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 2 non-existent file(s)
  - Update or remove references: narrator.py, stream_dialogue.py
- `docs/core_utils/IMPLEMENTATION_Core_Utils_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: DOCS: PATTERNS_Core_Utils_Functions.md
- `docs/physics/IMPLEMENTATION_Physics.md` - References 11 non-existent file(s)
  - Update or remove references: # DOCS: docs/physics/PATTERNS_Physics.md, graph_queries.py, graph_ops.py
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` - References 4 non-existent file(s)
  - Update or remove references: ngram/config.yaml, ngram/state/SYNC_Project_Health.md, DOCS: docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Schema.md` - References 3 non-existent file(s)
  - Update or remove references: ngram/config.yaml, ngram/state/SYNC_Project_Health.md, ngram/state/REPAIR_REPORT.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md` - References 5 non-existent file(s)
  - Update or remove references: IMPLEMENTATION_Runtime_And_Dependencies.md, archive/SYNC_archive_2024-12.md, ngram/config.yaml
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Runtime_And_Dependencies.md` - References 6 non-existent file(s)
  - Update or remove references: ngram/config.yaml, ngram/state/SYNC_Project_Health.md, ngram/state/REPAIR_REPORT.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Code_Structure.md` - References 5 non-existent file(s)
  - Update or remove references: IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md, ngram/config.yaml, ngram/state/SYNC_Project_Health.md
- `docs/cli/prompt/IMPLEMENTATION_Prompt_Code_Architecture.md` - References 5 non-existent file(s)
  - Update or remove references: ngram/config.yaml, ngram/state/SYNC_Project_Health.md, ngram/state/SYNC_Prompt_Command_State.md
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 5 non-existent file(s)
  - Update or remove references: moments.py, app.py, views.py
- ... and 3 more

### INCOMPLETE_CHAIN (5 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/world-runner` - Missing: HEALTH
- `docs/cli` - Missing: PATTERNS, BEHAVIORS, VALIDATION, HEALTH, SYNC
- `docs/infrastructure/scene-memory` - Missing: HEALTH
- `docs/engine/moment-graph-engine` - Missing: HEALTH
- `docs/engine/moments` - Missing: HEALTH

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 2 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_ops_events.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_ops_types.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (4 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/physics` - Total 226K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 53K chars (threshold: 50K)
- `docs/infrastructure/api` - Total 56K chars (threshold: 50K)
- `docs/architecture/cybernetic_studio_architecture` - Total 54K chars (threshold: 50K)

### STALE_IMPL (5 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 2 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 4 referenced files not found
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Runtime_And_Dependencies.md` - 2 referenced files not found
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - 5 referenced files not found
- `docs/engine/models/IMPLEMENTATION_Models.md` - 5 referenced files not found

### DOC_TEMPLATE_DRIFT (116 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/SYNC_Project_Repository_Map_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md` - Missing: INDICATOR: {Indicator Name}
- `docs/llm_agents/SYNC_LLM_Agents_State_archive_2025-12.md` - Too short: IN PROGRESS
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - Missing: RUNTIME BEHAVIOR, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md` - Missing: OVERVIEW, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, GAPS / IDEAS / QUESTIONS
- `docs/agents/narrator/SYNC_Narrator.md` - Missing: IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/agents/narrator/VALIDATION_Narrator.md` - Missing: INVARIANTS, PROPERTIES, ERROR CONDITIONS, HEALTH COVERAGE
- ... and 106 more

### DOC_LINK_INTEGRITY (15 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/api/tempo.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_ops.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_queries_moments.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_queries_search.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/tick.py` - Code file references docs but the bidirectional link is broken
- `engine/scripts/inject_to_narrator.py` - Code file references docs but the bidirectional link is broken
- `ngram/context.py` - Code file references docs but the bidirectional link is broken
- `ngram/github.py` - Code file references docs but the bidirectional link is broken
- `ngram/init_cmd.py` - Code file references docs but the bidirectional link is broken
- `ngram/project_map.py` - Code file references docs but the bidirectional link is broken
- ... and 5 more

### CODE_DOC_DELTA_COUPLING (4 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/orchestration/world_runner.py` - Code changed without corresponding doc or SYNC updates
- `engine/models/__init__.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_queries_moments.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Player_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TEST_World_Runner_Coverage.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/physics/API_Physics.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- ... and 14 more

### NAMING_CONVENTION (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/SYNC_Project_Repository_Map_archive_2025-12.md` - Naming convention violations task (1): 10 items
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename 'TOOL_REFERENCE.md' is too short/non-descriptive
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md` - Naming convention violations task (3): 10 items
- `docs/engine/models/HEALTH_Models.md` - Doc filename 'HEALTH_Models.md' is too short/non-descriptive
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - Doc filename 'IMPLEMENTATION_Api.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/SYNC_Scene_Memory_archive_2025-12.md` - Naming convention violations task (6): 10 items
- `docs/physics/PATTERNS_Physics.md` - Doc filename 'PATTERNS_Physics.md' is too short/non-descriptive
- `docs/schema/SCHEMA.md` - Naming convention violations task (8): 10 items
- `docs/schema/graph-health/SYNC_Graph_Health.md` - Doc filename 'SYNC_Graph_Health.md' is too short/non-descriptive

### DOC_GAPS (2 files)

**What's wrong:** A previous agent couldn't complete all work and left tasks in a GAPS section. These represent incomplete implementations, missing docs, or decisions that needed human input.

**How to fix:** Read the GAPS section in the SYNC file, complete the listed tasks, and mark them [x] done or remove the section when finished.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/SYNC_Physics.md` - 2 incomplete task(s) from previous session
- `docs/infrastructure/api/SYNC_Api.md` - 2 incomplete task(s) from previous session

### DOC_DUPLICATION (6 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `IMPLEMENTATION_CLI_Code_Architecture/`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md` - Multiple ALGORITHM docs in `ALGORITHM_CLI_Command_Execution_Logic/`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/schema/models/SYNC_Schema_Models.md` - Multiple SYNC docs in `models/`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md` - Multiple PATTERNS docs in `models/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### ESCALATION (11 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `.ngram/skills/legacy/SKILL_Sync_Update_Module_State_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Review_Evaluate_Changes_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Create_Module_Documentation_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Onboard_Understand_Module_Codebase_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Extend_Add_Features_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Debug_Investigate_Fix_Issues_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Health_Define_And_Verify_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILLS_Legacy_Index.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Ingest_Raw_Data_Sources_Legacy.md` - Escalation marker needs decision
- `.ngram/skills/legacy/SKILL_Orchestrate_Feature_Integration_Legacy.md` - Escalation marker needs decision
- ... and 1 more

### HARDCODED_CONFIG (6 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-20
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (18 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `ngram` - No documentation mapping (55 files)
  - Add mapping to modules.yaml
- `ngram/llms` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `ngram/tui` - No documentation mapping (17 files)
  - Add mapping to modules.yaml
- `ngram/tui/widgets` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine` - No documentation mapping (55 files)
  - Add mapping to modules.yaml
- `engine/models` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/moments` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/graph/health` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine/scripts` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- ... and 8 more

### BROKEN_IMPL_LINK (12 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 2 non-existent file(s)
  - Update or remove references: stream_dialogue.py, narrator.py
- `docs/core_utils/IMPLEMENTATION_Core_Utils_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: DOCS: PATTERNS_Core_Utils_Functions.md
- `docs/physics/IMPLEMENTATION_Physics.md` - References 11 non-existent file(s)
  - Update or remove references: traversal.py, graph_ops.py, engine/physics/graph/graph_ops_*.py
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` - References 3 non-existent file(s)
  - Update or remove references: ngram/config.yaml, DOCS: docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md, DOCS: docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Schema.md` - References 2 non-existent file(s)
  - Update or remove references: ngram/config.yaml, ngram/state/REPAIR_REPORT.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md` - References 5 non-existent file(s)
  - Update or remove references: archive/SYNC_archive_2024-12.md, ngram/config.yaml, IMPLEMENTATION_Schema.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Runtime_And_Dependencies.md` - References 5 non-existent file(s)
  - Update or remove references: ngram/config.yaml, ngram/state/REPAIR_REPORT.md, IMPLEMENTATION_Code_Structure.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Code_Structure.md` - References 4 non-existent file(s)
  - Update or remove references: ngram/config.yaml, IMPLEMENTATION.Runtime_And_Dependencies.md, IMPLEMENTATION_Schema.md
- `docs/cli/prompt/IMPLEMENTATION_Prompt_Code_Architecture.md` - References 3 non-existent file(s)
  - Update or remove references: ngram/state/SYNC_Prompt_Command_State.md, ngram/config.yaml, ngram/state/SYNC_Prompt_Command_State.md
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - References 5 non-existent file(s)
  - Update or remove references: playthroughs.py, views.py, app.py
- ... and 2 more

### INCOMPLETE_CHAIN (5 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/world-runner` - Missing: HEALTH
- `docs/cli` - Missing: PATTERNS, BEHAVIORS, VALIDATION, HEALTH, SYNC
- `docs/infrastructure/scene-memory` - Missing: HEALTH
- `docs/engine/moment-graph-engine` - Missing: HEALTH
- `docs/engine/moments` - Missing: HEALTH

### INCOMPLETE_IMPL (14 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains 5 empty/incomplete function(s)
- `engine/infrastructure/api/playthroughs.py` - Contains 2 empty/incomplete function(s)
- `engine/infrastructure/memory/moment_processor.py` - Contains 4 empty/incomplete function(s)
- `engine/models/base.py` - Contains 3 empty/incomplete function(s)
- `engine/models/links.py` - Contains 4 empty/incomplete function(s)
- `engine/models/nodes.py` - Contains 6 empty/incomplete function(s)
- `engine/moment_graph/queries.py` - Contains 2 empty/incomplete function(s)
- `engine/moment_graph/traversal.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_ops_events.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_ops_types.py` - Contains 2 empty/incomplete function(s)
- ... and 4 more

### LARGE_DOC_MODULE (4 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/physics` - Total 226K chars (threshold: 50K)
- `docs/infrastructure/scene-memory` - Total 53K chars (threshold: 50K)
- `docs/infrastructure/api` - Total 56K chars (threshold: 50K)
- `docs/architecture/cybernetic_studio_architecture` - Total 54K chars (threshold: 50K)

### STALE_IMPL (5 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 2 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 4 referenced files not found
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Runtime_And_Dependencies.md` - 2 referenced files not found
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - 5 referenced files not found
- `docs/engine/models/IMPLEMENTATION_Models.md` - 5 referenced files not found

### DOC_TEMPLATE_DRIFT (116 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/SYNC_Project_Repository_Map_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md` - Missing: INDICATOR: {Indicator Name}
- `docs/llm_agents/SYNC_LLM_Agents_State_archive_2025-12.md` - Too short: IN PROGRESS
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/llm_agents/ALGORITHM_Gemini_Stream_Flow.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - Missing: RUNTIME BEHAVIOR, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md` - Missing: OVERVIEW, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, GAPS / IDEAS / QUESTIONS
- `docs/agents/narrator/SYNC_Narrator.md` - Missing: IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE
- `docs/agents/narrator/SYNC_Narrator_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/agents/narrator/VALIDATION_Narrator.md` - Missing: INVARIANTS, PROPERTIES, ERROR CONDITIONS, HEALTH COVERAGE
- ... and 106 more

### DOC_LINK_INTEGRITY (15 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/api/tempo.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_ops.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_queries_moments.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_queries_search.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/tick.py` - Code file references docs but the bidirectional link is broken
- `engine/scripts/inject_to_narrator.py` - Code file references docs but the bidirectional link is broken
- `ngram/context.py` - Code file references docs but the bidirectional link is broken
- `ngram/github.py` - Code file references docs but the bidirectional link is broken
- `ngram/init_cmd.py` - Code file references docs but the bidirectional link is broken
- `ngram/project_map.py` - Code file references docs but the bidirectional link is broken
- ... and 5 more

### CODE_DOC_DELTA_COUPLING (5 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/orchestration/world_runner.py` - Code changed without corresponding doc or SYNC updates
- `engine/models/__init__.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_queries_moments.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `ngram/refactor.py` - Code changed without corresponding doc or SYNC updates

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Player_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TEST_World_Runner_Coverage.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/physics/API_Physics.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- ... and 14 more

### NAMING_CONVENTION (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/SYNC_Project_Repository_Map_archive_2025-12.md` - Naming convention violations task (1): 10 items
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename 'TOOL_REFERENCE.md' is too short/non-descriptive
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md` - Naming convention violations task (3): 10 items
- `docs/engine/models/HEALTH_Models.md` - Doc filename 'HEALTH_Models.md' is too short/non-descriptive
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - Doc filename 'IMPLEMENTATION_Api.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/SYNC_Scene_Memory_archive_2025-12.md` - Naming convention violations task (6): 10 items
- `docs/physics/PATTERNS_Physics.md` - Doc filename 'PATTERNS_Physics.md' is too short/non-descriptive
- `docs/schema/SCHEMA.md` - Naming convention violations task (8): 10 items
- `docs/schema/graph-health/SYNC_Graph_Health.md` - Doc filename 'SYNC_Graph_Health.md' is too short/non-descriptive

### DOC_GAPS (2 files)

**What's wrong:** A previous agent couldn't complete all work and left tasks in a GAPS section. These represent incomplete implementations, missing docs, or decisions that needed human input.

**How to fix:** Read the GAPS section in the SYNC file, complete the listed tasks, and mark them [x] done or remove the section when finished.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/SYNC_Physics.md` - 2 incomplete task(s) from previous session
- `docs/infrastructure/api/SYNC_Api.md` - 2 incomplete task(s) from previous session

### DOC_DUPLICATION (6 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `IMPLEMENTATION_CLI_Code_Architecture/`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md` - Multiple ALGORITHM docs in `ALGORITHM_CLI_Command_Execution_Logic/`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/schema/models/SYNC_Schema_Models.md` - Multiple SYNC docs in `models/`
- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md` - Multiple PATTERNS docs in `models/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### HARDCODED_CONFIG (6 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-20
Original file: SYNC_Project_Health.md

---

## ISSUES

### DOC_TEMPLATE_DRIFT (207 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/infrastructure/api/ALGORITHM_Api.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/schema/BEHAVIORS_Schema_Module_Observable_Schema_Effects.md` - Missing: INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, GAPS / IDEAS / QUESTIONS
- `docs/connectome/node_kit/BEHAVIORS_Connectome_Node_Kit_Visible_Clarity_And_Trust_Effects.md` - Missing: INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, GAPS / IDEAS / QUESTIONS; Too short: BEHAVIORS
- `docs/engine/SYNC_Engine.md` - Missing: MATURITY, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE, POINTERS
- `docs/protocol/IMPLEMENTATION/IMPLEMENTATION_Protocol_File_Structure.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, GAPS / IDEAS / QUESTIONS
- `docs/tui/archive/SYNC_Archive_2024-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/connectome/log_panel/HEALTH_Connectome_Log_Panel_Runtime_Verification_Of_Log_Truth_And_Export_Integrity.md` - Missing: WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, STATUS (RESULT INDICATOR), DOCK TYPES (COMPLETE LIST), INDICATOR: {Indicator Name}; Too short: HOW TO RUN
- `docs/connectome/log_panel/VALIDATION_Connectome_Log_Panel_Invariants_For_Truthful_Durations_And_Stable_Export.md` - Missing: PROPERTIES, ERROR CONDITIONS, HEALTH COVERAGE, VERIFICATION PROCEDURE, SYNC STATUS, GAPS / IDEAS / QUESTIONS; Too short: INVARIANTS
- `docs/connectome/flow_canvas/SYNC_Connectome_Flow_Canvas_Sync_Current_State.md` - Missing: IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/engine/ALGORITHM_Engine.md` - Missing: OVERVIEW, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, GAPS / IDEAS / QUESTIONS
- ... and 197 more

### DOC_DUPLICATION (6 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md` - Multiple PATTERNS docs in `models/`
- `docs/cli/core/ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md` - Multiple ALGORITHM docs in `ALGORITHM_CLI_Command_Execution_Logic/`
- `docs/schema/models/SYNC_Schema_Models.md` - Multiple SYNC docs in `models/`
- `docs/cli/archive/SYNC_CLI_State_Archive_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `IMPLEMENTATION_CLI_Code_Architecture/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/API_Physics.md` - Doc filename does not use a standard prefix
- `docs/schema/SCHEMA_Moments/SCHEMA_Moments_Example.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/schema/SCHEMA.md` - Doc filename does not use a standard prefix
- `docs/schema/SCHEMA_Moments.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- `docs/engine/moment-graph-engine/TEST_Moment_Graph_Runtime_Coverage.md` - Doc filename does not use a standard prefix
- `docs/schema/SCHEMA/SCHEMA_Tensions.md` - Doc filename does not use a standard prefix
- `docs/schema/SCHEMA/SCHEMA_Links.md` - Doc filename does not use a standard prefix
- ... and 14 more

### DOC_GAPS (2 files)

**What's wrong:** A previous agent couldn't complete all work and left tasks in a GAPS section. These represent incomplete implementations, missing docs, or decisions that needed human input.

**How to fix:** Read the GAPS section in the SYNC file, complete the listed tasks, and mark them [x] done or remove the section when finished.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/infrastructure/api/SYNC_Api.md` - 2 incomplete task(s) from previous session
- `docs/physics/SYNC_Physics.md` - 2 incomplete task(s) from previous session

### HARDCODED_CONFIG (6 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values

### DOC_LINK_INTEGRITY (15 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/physics/graph/graph_queries_moments.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_ops.py` - Code file references docs but the bidirectional link is broken
- `engine/infrastructure/api/tempo.py` - Code file references docs but the bidirectional link is broken
- `engine/scripts/inject_to_narrator.py` - Code file references docs but the bidirectional link is broken
- `ngram/init_cmd.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/tick.py` - Code file references docs but the bidirectional link is broken
- `ngram/validate.py` - Code file references docs but the bidirectional link is broken
- `ngram/context.py` - Code file references docs but the bidirectional link is broken
- `ngram/refactor.py` - Code file references docs but the bidirectional link is broken
- `ngram/github.py` - Code file references docs but the bidirectional link is broken
- ... and 5 more

### NAMING_CONVENTION (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/world-runner/archive/SYNC_archive_2024-12.md` - Naming convention violations task (3): 10 items
- `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py` - Code file 'connectome_doc_bundle_splitter_and_fence_rewriter.py' contains 'and', suggesting it should be split
- `docs/schema/SCHEMA/SCHEMA_Links.md` - Doc filename 'SCHEMA_Links.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/TEST_Scene_Memory.md` - Doc filename 'TEST_Scene_Memory.md' is too short/non-descriptive
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename 'TOOL_REFERENCE.md' is too short/non-descriptive
- `docs/infrastructure/api/SYNC_Api.md` - Doc filename 'SYNC_Api.md' is too short/non-descriptive
- `docs/physics/SYNC_Physics.md` - Doc filename 'SYNC_Physics.md' is too short/non-descriptive
- `docs/engine/BEHAVIORS_Engine.md` - Doc filename 'BEHAVIORS_Engine.md' is too short/non-descriptive
- `docs/engine/models/PATTERNS_Models.md` - Doc filename 'PATTERNS_Models.md' is too short/non-descriptive
- `docs/SYNC_Project_Repository_Map_archive_2025-12.md` - Naming convention violations task (1): 10 items
- ... and 1 more

### CODE_DOC_DELTA_COUPLING (2 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/orchestration/world_runner.py` - Code changed without corresponding doc or SYNC updates
- `engine/models/__init__.py` - Code changed without corresponding doc or SYNC updates

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `AGENTS.md` - Escalation marker needs decision

### LARGE_DOC_MODULE (1 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/physics` - Total 226K chars (threshold: 62K)

---

