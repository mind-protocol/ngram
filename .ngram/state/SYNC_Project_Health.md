# SYNC: Project Health

```
LAST_UPDATED: 2025-12-24
UPDATED_BY: ngram doctor
STATUS: CRITICAL
```

---

## CURRENT STATE

**Health Score:** 0/100

The project has critical issues that will significantly impact agent effectiveness. Address these before starting new work.

| Severity | Count |
|----------|-------|
| Critical | 31 |
| Warning | 595 |
| Info | 845 |

---

## ISSUES

### BROKEN_IMPL_LINK (24 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: graph_ops_events.py, TickResult.flips, algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md
- `docs/building/IMPLEMENTATION_Ngram_Graph_System.md` - References 37 non-existent file(s)
  - Update or remove references: context/format.py, content/*.py, tests/building/test_ingest.py
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: ExportButtons.handleCopyJsonl, state_store.ledger
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - References 10 non-existent file(s)
  - Update or remove references: engine/physics/graph.py, test_runner.py, test_steps.py
- `docs/archive/tui_deprecated_2025-12/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md` - References 2 non-existent file(s)
  - Update or remove references: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md, docs/tui/PATTERNS_TUI_Modular_Interface_Design.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: structure/IMPLEMENTATION_Code_Structure.md
- `docs/engine/models/IMPLEMENTATION_Models.md` - References 1 non-existent file(s)
  - Update or remove references: docs/schema/models/PATTERNS_Pydantic_Schema_Models.md
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 3 non-existent file(s)
  - Update or remove references: agent_cli.run_agent, narrator/prompt_builder.py, NarratorService.generate
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: flow_event_schema_and_normalization_contract.ts
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 7 non-existent file(s)
  - Update or remove references: SYNC_World_Runner.md, Orchestrator._process_flips, GraphOps.apply
- ... and 14 more

### MONOLITH (6 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `ngram/repair_verification.py` - 974 lines (threshold: 800)
  - Split: class VerificationResult() (296L, :113), def _execute_membrane_query() (119L, :596), def create_membrane_query_function() (88L, :715)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `engine/physics/tick_v1_2.py` - 963 lines (threshold: 800)
  - Split: class GraphTickV1_2() (993L, :208), def _phase_moment_flow() (105L, :518), def _phase_narrative_backflow() (81L, :713)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)
- `ngram/doctor_graph.py` - 802 lines (threshold: 800)
  - Split: def generate_thing_id() (107L, :286), class DoctorGraphStore() (96L, :393), def create_tasks_from_issues() (94L, :872)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### DOC_LINK_INTEGRITY (52 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `ngram/tui/commands_agent.py` - Code file references docs but the bidirectional link is broken
- `engine/infrastructure/api/playthroughs.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/suggestions.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/checkers/no_negative.py` - Code file references docs but the bidirectional link is broken
- `engine/scripts/inject_to_narrator.py` - Code file references docs but the bidirectional link is broken
- `ngram/project_map.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/__init__.py` - Code file references docs but the bidirectional link is broken
- `engine/moment_graph/queries.py` - Code file references docs but the bidirectional link is broken
- `engine/health/connectome_health_service.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/app_core.py` - Code file references docs but the bidirectional link is broken
- ... and 42 more

### ESCALATION (83 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md` - Escalation marker needs decision (priority: 5)
- `docs/physics/algorithms/ALGORITHM_Physics_Schema_v1.1_Energy_Physics.md` - COMPLETION_THRESHOLD: What energy level triggers active→comp (priority: 4)
- `docs/schema/ALGORITHM_Schema.md` - Escalation marker needs decision (priority: 5)
- `docs/building/ALGORITHM_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 5)
- `docs/core_utils/IMPLEMENTATION_Core_Utils_Code_Architecture.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/prompt/IMPLEMENTATION_Prompt_Code_Architecture.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Orchestrate_Feature_Integration_Pipeline_Orchestrator_And_Progress_Router.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/api/PATTERNS_Api.md` - Should health checks include a read-only scenario asset chec (priority: 5)
- `docs/building/mapping.yaml` - Escalation marker needs decision (priority: 5)
- ... and 73 more

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/health_panel/PATTERNS_Connectome_Health_Panel_Live_Monitoring_And_Invariants_Visualization.md` - Too short: MARKERS
- `docs/connectome/runtime_engine/VALIDATION_Connectome_Runtime_Engine_Invariants_For_Stepper_And_Realtime.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md` - Missing: OBJECTIVES SERVED
- `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/physics/algorithms/ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md` - Missing: OVERVIEW, OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, MARKERS
- `docs/ngram_feature/ALGORITHM_Ngram_Feature_Placeholder_Page.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/api/sse/VALIDATION_SSE_API.md` - Missing: CHAIN, TESTS VS HEALTH, INVARIANTS, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- `docs/infrastructure/tempo/VALIDATION_Tempo.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md` - Missing: OBJECTIVES SERVED
- `docs/infrastructure/scene-memory/BEHAVIORS_Scene_Memory.md` - Missing: OBJECTIVES SERVED, EDGE CASES
- ... and 288 more

### NON_STANDARD_DOC_TYPE (25 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/health/CONNECTOME_HEALTH_PAYLOAD.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/building/DECISIONS_Ngram_Graph_System.md` - Doc filename does not use a standard prefix
- `docs/membrane/MAPPING_Issue_Type_Verification.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/api/API_Graph_Management.md` - Doc filename does not use a standard prefix
- `docs/connectome/VISUAL_STYLEGUIDE_Connectome.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TEST_World_Runner_Coverage.md` - Doc filename does not use a standard prefix
- `docs/engine/moments/TEST_Moment_Graph_Coverage.md` - Doc filename does not use a standard prefix
- ... and 15 more

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)
- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - 1 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - 1 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- ... and 1 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/world-runner/BEHAVIORS_World_Runner.md` - Doc filename 'BEHAVIORS_World_Runner.md' is too short/non-descriptive
- `docs/infrastructure/api/ALGORITHM_Api.md` - Doc filename 'ALGORITHM_Api.md' is too short/non-descriptive
- `docs/physics/VALIDATION_Energy_Physics.md` - Doc filename 'VALIDATION_Energy_Physics.md' is too short/non-descriptive
- `docs/connectome/graph_api/PATTERNS_Graph_API.md` - Doc filename 'PATTERNS_Graph_API.md' is too short/non-descriptive
- `docs/agents/narrator/OBJECTIVES_Narrator_Goals.md` - Doc filename 'OBJECTIVES_Narrator_Goals.md' is too short/non-descriptive
- `docs/physics/graph/VALIDATION_Living_Graph.md` - Doc filename 'VALIDATION_Living_Graph.md' is too short/non-descriptive
- `docs/schema/SYNC_Schema.md` - Doc filename 'SYNC_Schema.md' is too short/non-descriptive
- `docs/infrastructure/tempo/HEALTH_Tempo.md` - Doc filename 'HEALTH_Tempo.md' is too short/non-descriptive
- `docs/ngram_feature/PATTERNS_Ngram_Feature.md` - Doc filename 'PATTERNS_Ngram_Feature.md' is too short/non-descriptive
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts` - Code file 'connectome_node_background_theme_tokens_by_type_and_language.ts' contains 'and', suggesting it should be split
- ... and 8 more

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/agents/narrator` - Total 91K chars (threshold: 62K)
- `docs/membrane` - Total 106K chars (threshold: 62K)
- `docs/connectome/node_kit` - Total 83K chars (threshold: 62K)
- `docs/building` - Total 84K chars (threshold: 62K)
- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/llm_agents` - Total 79K chars (threshold: 62K)
- `docs/schema` - Total 64K chars (threshold: 62K)
- ... and 3 more

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/connectome/graphs` - Missing: HEALTH
- `docs/building` - Missing: HEALTH

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/BEHAVIORS_Physics/BEHAVIORS_Physics_Overview.md` - Multiple BEHAVIORS docs in `BEHAVIORS_Physics/`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` - Multiple ALGORITHM docs in `algorithms/`
- `docs/physics/archive/SYNC_Physics_History_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/schema/BEHAVIORS_Schema_Module_Observable_Schema_Effects.md` - Multiple BEHAVIORS docs in `schema/`
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - Multiple IMPLEMENTATION docs in `membrane/`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `schema/`
- `docs/schema/SYNC_Schema.md` - Multiple SYNC docs in `schema/`
- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/physics/VALIDATION_Energy_Physics.md` - Multiple VALIDATION docs in `physics/`
- `docs/membrane/BEHAVIORS_Membrane_System.md` - Multiple BEHAVIORS docs in `membrane/`
- ... and 8 more

### CODE_DOC_DELTA_COUPLING (30 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/physics/graph/graph_ops.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_core.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/tick_runner.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_core.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_queries_moments.py` - Code changed without corresponding doc or SYNC updates
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx` - Code changed without corresponding doc or SYNC updates
- `tools/stream_dialogue.py` - Code changed without corresponding doc or SYNC updates
- `app/api/sse/route.ts` - Code changed without corresponding doc or SYNC updates
- `engine/health/connectome_health_service.py` - Code changed without corresponding doc or SYNC updates
- `app/connectome/components/connectome_health_panel.tsx` - Code changed without corresponding doc or SYNC updates
- ... and 20 more

### NEW_UNDOC_CODE (23 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/init_db.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/activity_logger.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/api/moments.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `ngram/core_utils.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/session.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/api/app.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/memory/moment_processor.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/validation.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/world_runner.py` - Modified 1d after IMPLEMENTATION doc
- ... and 13 more

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/tui/widgets/manager_panel.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)

---

## LATER

These are minor issues that don't block work but would improve project health:

- [ ] `docs/connectome/runtime_engine/OBJECTIVES_Runtime_Engine_Goals.md` - 92% similar to `docs/connectome/page_shell/OBJECTIVES_Page_Shell_Goals.md`
- [ ] `docs/llm_agents/OBJECTIVES_Llm_Agents_Goals.md` - 94% similar to `docs/connectome/runtime_engine/OBJECTIVES_Runtime_Engine_Goals.md`
- [ ] `engine/physics/tick_v1_2.py` - Contains 22 potential magic numbers
- [ ] `docs/tools/OBJECTIVES_Tools_Goals.md` - 96% similar to `docs/engine/OBJECTIVES_Engine_Goals.md`
- [ ] `docs/physics/attention/BEHAVIORS_Attention_Split_And_Interrupts.md` - Todo marker needs attention (priority: 5)
- [ ] `/home/mind-protocol/ngram/docs/physics/VALIDATION_Energy_Physics.md` - Invariant V-TOPN-CRITICAL marked as untested
- [ ] `docs/engine/membrane/VALIDATION_Membrane_Modulation.md` - Missing: BEHAVIORS GUARANTEED
- [ ] `docs/connectome/node_kit/OBJECTIVES_Node_Kit_Goals.md` - 94% similar to `docs/infrastructure/scene-memory/OBJECTIVES_Scene_Memory_Goals.md`
- [ ] `engine/models/base.py` - No DOCS: reference in file header
- [ ] `ngram/tui/commands.py` - Contains 6 potential magic numbers
- ... and 835 more

---

## HANDOFF

**For the next agent:**

Before starting your task, consider addressing critical issues - especially if your work touches affected files. Monoliths and undocumented code will slow you down.

**Recommended first action:** Pick one MONOLITH file you'll be working in and split its largest function into a separate module.

---

*Generated by `ngram doctor`*