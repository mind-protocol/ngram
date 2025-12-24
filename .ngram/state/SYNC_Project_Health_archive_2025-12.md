# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### BROKEN_IMPL_LINK (25 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/cli/prompt/IMPLEMENTATION_Prompt_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: ngram/state/SYNC_Project_Health.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md` - References 3 non-existent file(s)
  - Update or remove references: schema/IMPLEMENTATION_Schema.md, structure/IMPLEMENTATION_Code_Structure.md, runtime/IMPLEMENTATION_Runtime_And_Dependencies.md
- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: graph_ops_read_only_interface.py, graph_ops_events.py, algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md` - References 4 non-existent file(s)
  - Update or remove references: ngram/state/SYNC_Project_Health.md, structure/IMPLEMENTATION_Code_Structure.md, overview/IMPLEMENTATION_Overview.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - References 2 non-existent file(s)
  - Update or remove references: ngram/state/SYNC_Project_Health.md, structure/IMPLEMENTATION_Code_Structure.md
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: flow_event_schema_and_normalization_contract.ts
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: ngram/state/SYNC_Project_Health.md
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: state_store.ledger, ExportButtons.handleCopyJsonl
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 3 non-existent file(s)
  - Update or remove references: agent_cli.run_agent, NarratorService.generate, narrator/prompt_builder.py
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - References 1 non-existent file(s)
  - Update or remove references: connectome_system_map_node_edge_manifest.ts
- ... and 15 more

### UNDOCUMENTED (39 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/moment_graph` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/health` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `engine/migrations` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `app/connectome` - No documentation mapping (24 files)
  - Add mapping to modules.yaml
- `app/api/connectome/graph` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/api` - No documentation mapping (7 files)
  - Add mapping to modules.yaml
- `engine/physics/health` - No documentation mapping (9 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/canon` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `app/ngram` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/models` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- ... and 29 more

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- `docs/agents/narrator` - Total 91K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/connectome/node_kit` - Total 83K chars (threshold: 62K)
- `docs/infrastructure/api` - Total 65K chars (threshold: 62K)
- `docs/building` - Total 75K chars (threshold: 62K)
- `docs/connectome/state_store` - Total 95K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/membrane` - Total 101K chars (threshold: 62K)
- `docs/schema` - Total 64K chars (threshold: 62K)
- ... and 3 more

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/page_shell/PATTERNS_Connectome_Page_Shell_Route_Composition_And_User_Control_Surface_Patterns.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED
- `docs/tools/ALGORITHM_Tools.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/api/sse/ALGORITHM_SSE_API.md` - Missing: CHAIN, OVERVIEW, OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, MARKERS
- `docs/connectome/flow_canvas/PATTERNS_Connectome_Flow_Canvas_Pannable_Zoomable_Zoned_System_Map_Rendering_Patterns.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, INSPIRATIONS
- `docs/architecture/cybernetic_studio_architecture/IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md` - Missing: SCHEMA, LOGIC CHAINS, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, EXTRACTION CANDIDATES
- `docs/tui/BEHAVIORS_TUI_Interactions.md` - Missing: OBJECTIVES SERVED
- `docs/physics/attention/VALIDATION_Attention_Split_And_Interrupts.md` - Missing: TESTS VS HEALTH, INVARIANTS, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- `docs/physics/HEALTH_Energy_Physics.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), HOW TO USE THIS TEMPLATE, DOCK TYPES (COMPLETE LIST), INDICATOR: {Indicator Name}; Too short: HEALTH INDICATORS SELECTED
- `docs/protocol/features/PATTERNS_Agent_Trace_Logging.md` - Missing: THE PATTERN, BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, PRINCIPLES, DATA, DEPENDENCIES, INSPIRATIONS, SCOPE, MARKERS
- `docs/cli/VALIDATION_CLI_Module_Invariants.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- ... and 288 more

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/infrastructure/orchestration/world_runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/orchestrator.py` - Modified 1d after IMPLEMENTATION doc
- `engine/moment_graph/traversal.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/validation.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/connectome_health_service.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/session.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/README.md` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_outputs.md` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_results.md` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### ESCALATION (82 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md` - Escalation marker needs decision (priority: 5)
- `docs/schema/HEALTH_Schema.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/scene-memory/ALGORITHM_Scene_Memory.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/prompt/BEHAVIORS_Prompt_Command_Output_and_Flow.md` - Escalation marker needs decision (priority: 5)
- `docs/engine/models/IMPLEMENTATION_Models.md` - Implement schema migration system (priority: 5)
- `.claude/skills/SKILL_Onboard_Understand_Existing_Module_Codebase_And_Confirm_Canon.md` - Escalation marker needs decision (priority: 5)
- `docs/building/ALGORITHM_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/scene-memory/TEST_Scene_Memory.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/ALGORITHM_CLI_Command_Execution_Logic.md` - Escalation marker needs decision (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md` - Escalation marker needs decision (priority: 5)
- ... and 72 more

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/VALIDATION_Physics/VALIDATION_Physics_Procedures.md` - Multiple VALIDATION docs in `VALIDATION_Physics/`
- `docs/membrane/BEHAVIORS_Membrane_System.md` - Multiple BEHAVIORS docs in `membrane/`
- `docs/physics/VALIDATION_Energy_Physics.md` - Multiple VALIDATION docs in `physics/`
- `docs/physics/archive/SYNC_Physics_History_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/schema/PATTERNS_Schema.md` - Multiple PATTERNS docs in `schema/`
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - Multiple IMPLEMENTATION docs in `membrane/`
- `docs/schema/BEHAVIORS_Schema_Module_Observable_Schema_Effects.md` - Multiple BEHAVIORS docs in `schema/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`
- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- ... and 8 more

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/world-runner/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/wsl-autostart.md` - Doc filename does not use a standard prefix
- `docs/connectome/VISUAL_STYLEGUIDE_Connectome.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/engine/moments/TEST_Moment_Graph_Coverage.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TEST_World_Runner_Coverage.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- ... and 14 more

### DOC_LINK_INTEGRITY (35 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/scripts/inject_to_narrator.py` - Code file references docs but the bidirectional link is broken
- `engine/infrastructure/api/playthroughs.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/flow.py` - Code file references docs but the bidirectional link is broken
- `ngram/sync.py` - Code file references docs but the bidirectional link is broken
- `ngram/doctor_checks_membrane.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_queries_moments.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_ops_events.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/checkers/no_negative.py` - Code file references docs but the bidirectional link is broken
- `engine/health/connectome_health_service.py` - Code file references docs but the bidirectional link is broken
- `ngram/validate.py` - Code file references docs but the bidirectional link is broken
- ... and 25 more

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)
- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)

### CODE_DOC_DELTA_COUPLING (28 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `ngram/doctor_checks_sync.py` - Code changed without corresponding doc or SYNC updates
- `app/connectome/components/pannable_zoomable_zoned_flow_canvas_renderer.tsx` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_ops.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/tick.py` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/playthroughs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/init_cmd.py` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/sse_broadcast.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_core.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_docs.py` - Code changed without corresponding doc or SYNC updates
- ... and 18 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md` - Naming convention violations task (15): 10 items
- `docs/tools/ALGORITHM_Tools.md` - Doc filename 'ALGORITHM_Tools.md' is too short/non-descriptive
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts` - Code file 'connectome_log_duration_formatting_and_threshold_color_rules.ts' contains 'and', suggesting it should be split
- `docs/agents/narrator/OBJECTIVES_Narrator_Goals.md` - Doc filename 'OBJECTIVES_Narrator_Goals.md' is too short/non-descriptive
- `docs/agents/world-runner/BEHAVIORS_World_Runner.md` - Doc filename 'BEHAVIORS_World_Runner.md' is too short/non-descriptive
- `docs/infrastructure/tempo/PATTERNS_Tempo.md` - Doc filename 'PATTERNS_Tempo.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/PATTERNS_Scene_Memory.md` - Doc filename 'PATTERNS_Scene_Memory.md' is too short/non-descriptive
- `docs/ngram_cli_core/OBJECTIVES_ngram_cli_core.md` - Naming convention violations task (13): 10 items
- `docs/connectome/health/INTEGRATION_NOTES.md` - Doc filename 'INTEGRATION_NOTES.md' is too short/non-descriptive
- `docs/physics/BEHAVIORS_Physics.md` - Doc filename 'BEHAVIORS_Physics.md' is too short/non-descriptive
- ... and 8 more

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - 1 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - 1 referenced files not found
- ... and 1 more

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/building` - Missing: HEALTH
- `docs/connectome/graphs` - Missing: HEALTH
- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH

### INCOMPLETE_IMPL (1 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (39 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools/mcp` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `tools` - No documentation mapping (13 files)
  - Add mapping to modules.yaml
- `app/api/connectome/graphs` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/physics/health/checkers` - No documentation mapping (6 files)
  - Add mapping to modules.yaml
- `app/connectome/components` - No documentation mapping (22 files)
  - Add mapping to modules.yaml
- `engine/scripts` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `tools/archive` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/moment_graph` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `app/api/sse` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/physics` - No documentation mapping (36 files)
  - Add mapping to modules.yaml
- ... and 29 more

### BROKEN_IMPL_LINK (22 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - References 4 non-existent file(s)
  - Update or remove references: connectome_node_background_theme_tokens_by_type_and_language.ts, connectome_energy_badge_bucketed_glow_and_value_formatter.ts, active_focus.active_step_key
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md` - References 3 non-existent file(s)
  - Update or remove references: runtime/IMPLEMENTATION_Runtime_And_Dependencies.md, structure/IMPLEMENTATION_Code_Structure.md, schema/IMPLEMENTATION_Schema.md
- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: graph_queries.py, TickResult.flips, graph_ops_read_only_interface.py
- `docs/building/IMPLEMENTATION_Ngram_Graph_System.md` - References 37 non-existent file(s)
  - Update or remove references: moment.py, markers.py, content/narrative.py
- `docs/api/sse/IMPLEMENTATION_SSE_API.md` - References 4 non-existent file(s)
  - Update or remove references: NodeJS.Timeout, route.ts, Node.js
- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md` - References 4 non-existent file(s)
  - Update or remove references: implementation/IMPLEMENTATION_Physics_Dataflow.md, implementation/IMPLEMENTATION_Physics_Runtime.md, implementation/IMPLEMENTATION_Physics_Architecture.md
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - References 9 non-existent file(s)
  - Update or remove references: React Flow EdgeProps.data, connectome_node_boundary_intersection_geometry_helpers.ts, connectome_edge_directional_shine_animation_helpers.ts
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - References 2 non-existent file(s)
  - Update or remove references: app/connectome/components/telemetry_camera_controls.ts, pannable_zoomable_zoned_flow_canvas_renderer.tsx
- `docs/connectome/graphs/IMPLEMENTATION_Connectome_Graph_Listing_API_Architecture.md` - References 2 non-existent file(s)
  - Update or remove references: route.ts, connectome_read_cli.py
- `docs/schema/IMPLEMENTATION_Schema.md` - References 9 non-existent file(s)
  - Update or remove references: test_schema.py, nodes.py, test_schema_nodes.py
- ... and 12 more

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)
- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/protocol/ALGORITHM_Protocol_Core_Mechanics.md` - Missing: OVERVIEW, OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, MARKERS
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - Missing: CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, EXTRACTION CANDIDATES, MARKERS
- `docs/physics/attention/VALIDATION_Attention_Split_And_Interrupts.md` - Missing: TESTS VS HEALTH, INVARIANTS, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- `docs/tui/archive/IMPLEMENTATION_Archive_2024-12.md` - Missing: CHAIN, CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, EXTRACTION CANDIDATES, MARKERS
- `docs/engine/VALIDATION_Engine.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- `docs/protocol/VALIDATION_Protocol_Invariants.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/core_utils/SYNC_Core_Utils_State.md` - Too short: IN PROGRESS, KNOWN ISSUES
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - Missing: EXTRACTION CANDIDATES
- `docs/infrastructure/api/PATTERNS_Api.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, DATA
- `docs/agents/world-runner/ALGORITHM_World_Runner.md` - Missing: ALGORITHM: {Primary Function Name}
- ... and 288 more

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/building` - Missing: HEALTH
- `docs/connectome/graphs` - Missing: HEALTH

### CODE_DOC_DELTA_COUPLING (28 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools/stream_dialogue.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_core.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_report.py` - Code changed without corresponding doc or SYNC updates
- `engine/moment_graph/traversal.py` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/playthroughs.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_ops.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_queries_moments.py` - Code changed without corresponding doc or SYNC updates
- `ngram/init_cmd.py` - Code changed without corresponding doc or SYNC updates
- `engine/health/connectome_health_service.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/tick.py` - Code changed without corresponding doc or SYNC updates
- ... and 18 more

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/engine/moments/TEST_Moment_Graph_Coverage.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/CONNECTOME_HEALTH_PAYLOAD.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TEST_World_Runner_Coverage.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/engine/moment-graph-engine/TEST_Moment_Graph_Runtime_Coverage.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Player_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- ... and 14 more

### ESCALATION (82 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` - Should ngram without args require Textual, or fall back to C (priority: 5)
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/prompt/VALIDATION_Prompt_Bootstrap_Invariants.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Extend_Add_Features_To_Existing_Systems_With_Canon_Constraints.md` - Escalation marker needs decision (priority: 5)
- `docs/physics/algorithms/ALGORITHM_Physics_Schema_v1.1_Energy_Physics.md` - COMPLETION_THRESHOLD: What energy level triggers active→comp (priority: 4)
- `docs/infrastructure/api/VALIDATION_Api.md` - Escalation marker needs decision (priority: 5)
- `docs/engine/models/ALGORITHM_Models.md` - Should all derived properties be explicitly documented in a  (priority: 5)
- `docs/infrastructure/api/PATTERNS_Api.md` - Should health checks include a read-only scenario asset chec (priority: 5)
- `docs/building/ALGORITHM_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/core/VALIDATION_CLI_Instruction_Invariants.md` - Escalation marker needs decision (priority: 5)
- ... and 72 more

### DOC_LINK_INTEGRITY (35 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/api/playthroughs.py` - Code file references docs but the bidirectional link is broken
- `ngram/status_cmd.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_ops.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_interface.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/checkers/__init__.py` - Code file references docs but the bidirectional link is broken
- `engine/scripts/inject_to_narrator.py` - Code file references docs but the bidirectional link is broken
- `engine/graph/health/lint_terminology.py` - Code file references docs but the bidirectional link is broken
- `engine/moment_graph/traversal.py` - Code file references docs but the bidirectional link is broken
- `engine/graph/health/example_queries.cypher` - Code file references docs but the bidirectional link is broken
- `engine/moment_graph/queries.py` - Code file references docs but the bidirectional link is broken
- ... and 25 more

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/connectome/session.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/loader.py` - Modified 1d after IMPLEMENTATION doc
- `engine/init_db.py` - Modified 1d after IMPLEMENTATION doc
- `ngram/core_utils.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/activity_logger.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/world_runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/README.md` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/memory/moment_processor.py` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/connectome/log_panel` - Total 71K chars (threshold: 62K)
- `docs/connectome/node_kit` - Total 83K chars (threshold: 62K)
- `docs/schema` - Total 64K chars (threshold: 62K)
- `docs/membrane` - Total 101K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/connectome/state_store` - Total 95K chars (threshold: 62K)
- `docs/building` - Total 75K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/agents/narrator` - Total 91K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- ... and 3 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md` - Naming convention violations task (15): 10 items
- `docs/agents/world-runner/BEHAVIORS_World_Runner.md` - Doc filename 'BEHAVIORS_World_Runner.md' is too short/non-descriptive
- `docs/engine/moment-graph-engine/validation/player_dmz/VALIDATION_Player_DMZ.md` - Doc filename 'VALIDATION_Player_DMZ.md' is too short/non-descriptive
- `docs/physics/BEHAVIORS_Physics.md` - Doc filename 'BEHAVIORS_Physics.md' is too short/non-descriptive
- `docs/protocol/OBJECTIVES_Protocol_Goals.md` - Doc filename 'OBJECTIVES_Protocol_Goals.md' is too short/non-descriptive
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts` - Code file 'connectome_node_background_theme_tokens_by_type_and_language.ts' contains 'and', suggesting it should be split
- `docs/infrastructure/api/IMPLEMENTATION_Api.md` - Doc filename 'IMPLEMENTATION_Api.md' is too short/non-descriptive
- `docs/ngram_cli_core/OBJECTIVES_ngram_cli_core.md` - Naming convention violations task (13): 10 items
- `docs/infrastructure/tempo/PATTERNS_Tempo.md` - Doc filename 'PATTERNS_Tempo.md' is too short/non-descriptive
- `docs/tui/PATTERNS_TUI.md` - Doc filename 'PATTERNS_TUI.md' is too short/non-descriptive
- ... and 8 more

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - 1 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- ... and 1 more

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/VALIDATION_Physics/VALIDATION_Physics_Procedures.md` - Multiple VALIDATION docs in `VALIDATION_Physics/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`
- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/physics/VALIDATION_Energy_Physics.md` - Multiple VALIDATION docs in `physics/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- `docs/membrane/VALIDATION_Membrane_System.md` - Multiple VALIDATION docs in `membrane/`
- `docs/physics/archive/SYNC_Physics_History_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/tui/PATTERNS_TUI_Modular_Interface_Design.md` - Multiple PATTERNS docs in `tui/`
- `docs/schema/SYNC_Schema.md` - Multiple SYNC docs in `schema/`
- `docs/membrane/ALGORITHM_Membrane_System.md` - Multiple ALGORITHM docs in `membrane/`
- ... and 8 more

### INCOMPLETE_IMPL (1 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### UNDOCUMENTED (39 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `ngram/llms` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `engine/models` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/membrane` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `engine` - No documentation mapping (104 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/orchestration` - No documentation mapping (5 files)
  - Add mapping to modules.yaml
- `engine/infrastructure/canon` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- `app/connectome/components` - No documentation mapping (22 files)
  - Add mapping to modules.yaml
- `engine/migrations` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `engine/moments` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `app` - No documentation mapping (32 files)
  - Add mapping to modules.yaml
- ... and 29 more

### BROKEN_IMPL_LINK (24 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md` - References 3 non-existent file(s)
  - Update or remove references: schema/IMPLEMENTATION_Schema.md, structure/IMPLEMENTATION_Code_Structure.md, overview/IMPLEMENTATION_Overview.md
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - References 2 non-existent file(s)
  - Update or remove references: app/connectome/components/telemetry_camera_controls.ts, pannable_zoomable_zoned_flow_canvas_renderer.tsx
- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: graph_ops.py, graph_ops_read_only_interface.py, algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: structure/IMPLEMENTATION_Code_Structure.md
- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md` - References 4 non-existent file(s)
  - Update or remove references: implementation/IMPLEMENTATION_Physics_Architecture.md, implementation/IMPLEMENTATION_Physics_Dataflow.md, implementation/IMPLEMENTATION_Physics_Runtime.md
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 7 non-existent file(s)
  - Update or remove references: GraphOps.apply, HEALTH_World_Runner.md, Orchestrator._process_flips
- `docs/building/IMPLEMENTATION_Ngram_Graph_System.md` - References 37 non-existent file(s)
  - Update or remove references: config.py, prompts.py, response.py
- `docs/archive/tui_deprecated_2025-12/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md` - References 2 non-existent file(s)
  - Update or remove references: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md, docs/tui/PATTERNS_TUI_Modular_Interface_Design.md
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: ExportButtons.handleCopyJsonl, state_store.ledger
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - References 10 non-existent file(s)
  - Update or remove references: test_runner.py, document_progress.yaml, mcp.json
- ... and 14 more

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)
- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` - Missing: OVERVIEW, OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, MARKERS
- `docs/infrastructure/api/SYNC_Api.md` - Missing: IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE
- `docs/connectome/log_panel/ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/protocol/doctor/PATTERNS_Project_Health_Doctor.md` - Missing: THE PATTERN, BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, PRINCIPLES, DATA, DEPENDENCIES, INSPIRATIONS, SCOPE, MARKERS
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` - Missing: EXTRACTION CANDIDATES
- `docs/connectome/health/HEALTH_Connectome_Live_Signals.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), PURPOSE OF THIS FILE, WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, OBJECTIVES COVERAGE, DOCK TYPES (COMPLETE LIST), CHECKER INDEX, INDICATOR: {Indicator Name}, HOW TO RUN, KNOWN GAPS, MARKERS
- `docs/engine/membrane/PATTERNS_Membrane_Modulation.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED
- `docs/connectome/runtime_engine/HEALTH_Connectome_Runtime_Engine_Runtime_Verification_Of_Pacing_And_Order.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), INDICATOR: {Indicator Name}
- `docs/core_utils/PATTERNS_Core_Utils_Functions.md` - Missing: THE PROBLEM, THE PATTERN, BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED
- `docs/protocol/doctor/SYNC_Project_Health_Doctor.md` - Missing: IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, CONSCIOUSNESS TRACE, POINTERS
- ... and 288 more

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/membrane` - Total 101K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/llm_agents` - Total 79K chars (threshold: 62K)
- `docs/connectome/state_store` - Total 95K chars (threshold: 62K)
- `docs/agents/narrator` - Total 91K chars (threshold: 62K)
- `docs/connectome/node_kit` - Total 83K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/infrastructure/api` - Total 65K chars (threshold: 62K)
- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- ... and 3 more

### ESCALATION (82 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md` - Escalation marker needs decision (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/BEHAVIORS_Cybernetic_Studio_System_Behaviors.md` - Escalation marker needs decision (priority: 5)
- `docs/schema/HEALTH_Schema.md` - Escalation marker needs decision (priority: 5)
- `ngram/doctor_checks_content.py` - message = f (priority: 5)
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` - Escalation marker needs decision (priority: 5)
- `docs/archive/tui_deprecated_2025-12/HEALTH_TUI_Component_Test_Coverage.md` - How should we handle terminal resizing failures in HEALTH? (priority: 5)
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/scene-memory/TEST_Scene_Memory.md` - Escalation marker needs decision (priority: 5)
- `docs/building/BEHAVIORS_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 5)
- `AGENTS.md` - Escalation marker needs decision (priority: 5)
- ... and 72 more

### DOC_LINK_INTEGRITY (50 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/infrastructure/api/playthroughs.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/__init__.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/app_core.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/graph/graph_queries_search.py` - Code file references docs but the bidirectional link is broken
- `engine/graph/health/lint_terminology.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/state.py` - Code file references docs but the bidirectional link is broken
- `engine/models/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/repair.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/manager_panel.py` - Code file references docs but the bidirectional link is broken
- ... and 40 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/OBJECTIVES_Narrator_Goals.md` - Doc filename 'OBJECTIVES_Narrator_Goals.md' is too short/non-descriptive
- `docs/ngram_cli_core/ALGORITHM_ngram_cli_core.md` - Doc filename 'ALGORITHM_ngram_cli_core.md' is too short/non-descriptive
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md` - Naming convention violations task (6): 10 items
- `docs/api/sse/IMPLEMENTATION_SSE_API.md` - Doc filename 'IMPLEMENTATION_SSE_API.md' is too short/non-descriptive
- `docs/infrastructure/api/ALGORITHM_Api.md` - Doc filename 'ALGORITHM_Api.md' is too short/non-descriptive
- `docs/physics/graph/VALIDATION_Living_Graph.md` - Doc filename 'VALIDATION_Living_Graph.md' is too short/non-descriptive
- `docs/physics/VALIDATION_Energy_Physics.md` - Doc filename 'VALIDATION_Energy_Physics.md' is too short/non-descriptive
- `docs/connectome/graph_api/PATTERNS_Graph_API.md` - Doc filename 'PATTERNS_Graph_API.md' is too short/non-descriptive
- `docs/ngram_feature/PATTERNS_Ngram_Feature.md` - Doc filename 'PATTERNS_Ngram_Feature.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/BEHAVIORS_Scene_Memory.md` - Doc filename 'BEHAVIORS_Scene_Memory.md' is too short/non-descriptive
- ... and 8 more

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Contradiction_Pressure.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/INTEGRATION_NOTES.md` - Doc filename does not use a standard prefix
- `docs/membrane/MAPPING_Issue_Type_Verification.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/scene-memory/TEST_Scene_Memory.md` - Doc filename does not use a standard prefix
- ... and 14 more

### CODE_DOC_DELTA_COUPLING (28 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools/stream_dialogue.py` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/playthroughs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/init_cmd.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_sync.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/tick.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `ngram/core_utils.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_ops.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/health/checker.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks.py` - Code changed without corresponding doc or SYNC updates
- ... and 18 more

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - 1 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- ... and 1 more

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/query_results.md` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/validation.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/activity_logger.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/loader.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/connectome_health_service.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/orchestrator.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `engine/init_db.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/api/app.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_outputs.md` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - Multiple IMPLEMENTATION docs in `membrane/`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` - Multiple ALGORITHM docs in `algorithms/`
- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/membrane/VALIDATION_Membrane_System.md` - Multiple VALIDATION docs in `membrane/`
- `docs/membrane/BEHAVIORS_Membrane_System.md` - Multiple BEHAVIORS docs in `membrane/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- `docs/physics/VALIDATION_Physics/VALIDATION_Physics_Procedures.md` - Multiple VALIDATION docs in `VALIDATION_Physics/`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `schema/`
- `docs/membrane/ALGORITHM_Membrane_System.md` - Multiple ALGORITHM docs in `membrane/`
- `docs/schema/SYNC_Schema.md` - Multiple SYNC docs in `schema/`
- ... and 8 more

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/building` - Missing: HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/connectome/graphs` - Missing: HEALTH

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/tui/widgets/manager_panel.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)

### BROKEN_IMPL_LINK (24 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/archive/tui_deprecated_2025-12/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md` - References 2 non-existent file(s)
  - Update or remove references: docs/tui/PATTERNS_TUI_Modular_Interface_Design.md, docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 3 non-existent file(s)
  - Update or remove references: NarratorService.generate, narrator/prompt_builder.py, agent_cli.run_agent
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: structure/IMPLEMENTATION_Code_Structure.md
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - References 10 non-existent file(s)
  - Update or remove references: engine/physics/graph.py, mcp.json, document_progress.yaml
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md` - References 3 non-existent file(s)
  - Update or remove references: structure/IMPLEMENTATION_Code_Structure.md, overview/IMPLEMENTATION_Overview.md, schema/IMPLEMENTATION_Schema.md
- `docs/tools/IMPLEMENTATION_Tools.md` - References 13 non-existent file(s)
  - Update or remove references: engine.physics.graph.graph_ops.GraphOps, playthroughs/{id}/stream.jsonl, docs/infrastructure/cli-tools/PATTERNS_CLI_Agent_Utilities.md
- `docs/archive/tui_deprecated_2025-12/IMPLEMENTATION_TUI_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: ExportButtons.handleCopyJsonl, state_store.ledger
- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: graph_ops_events.py, graph_ops.py, algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md` - References 3 non-existent file(s)
  - Update or remove references: schema/IMPLEMENTATION_Schema.md, runtime/IMPLEMENTATION_Runtime_And_Dependencies.md, overview/IMPLEMENTATION_Overview.md
- ... and 14 more

### UNDOCUMENTED (1 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `app/ngram` - No documentation mapping (1 files)
  - Add mapping to modules.yaml

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/schema/BEHAVIORS_Schema_Module_Observable_Schema_Effects.md` - Multiple BEHAVIORS docs in `schema/`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` - Multiple ALGORITHM docs in `algorithms/`
- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/physics/VALIDATION_Energy_Physics.md` - Multiple VALIDATION docs in `physics/`
- `docs/schema/PATTERNS_Schema.md` - Multiple PATTERNS docs in `schema/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- `docs/membrane/VALIDATION_Membrane_System.md` - Multiple VALIDATION docs in `membrane/`
- `docs/membrane/ALGORITHM_Membrane_System.md` - Multiple ALGORITHM docs in `membrane/`
- `docs/archive/tui_deprecated_2025-12/PATTERNS_TUI_Modular_Interface_Design.md` - Multiple PATTERNS docs in `tui_deprecated_2025-12/`
- `docs/membrane/SYNC_Membrane_System.md` - Multiple SYNC docs in `membrane/`
- ... and 8 more

### DOC_LINK_INTEGRITY (50 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/physics/graph/graph_ops_read_only_interface.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/status_bar.py` - Code file references docs but the bidirectional link is broken
- `engine/moment_graph/traversal.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/app_manager.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/checkers/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/doctor_checks_membrane.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/manager_panel.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/agent_panel.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/input_bar.py` - Code file references docs but the bidirectional link is broken
- `engine/graph/health/example_queries.cypher` - Code file references docs but the bidirectional link is broken
- ... and 40 more

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/flow_canvas/VALIDATION_Connectome_Flow_Canvas_Invariants_For_Readability_And_Stability.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/physics/BEHAVIORS_Physics/BEHAVIORS_Physics_Overview.md` - Missing: OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, MARKERS
- `docs/connectome/node_kit/VALIDATION_Connectome_Node_Kit_Invariants_For_Node_Readability_And_State_Reflection.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/physics/graph/archive/ALGORITHM_Energy_Flow_archived_2025-12-20.md` - Missing: OBJECTIVES AND BEHAVIORS, ALGORITHM: {Primary Function Name}
- `docs/engine/models/ALGORITHM_Models.md` - Missing: OBJECTIVES AND BEHAVIORS, ALGORITHM: {Primary Function Name}
- `docs/physics/attention/HEALTH_Attention_Energy_Split.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), PURPOSE OF THIS FILE, WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, CHAIN, FLOWS ANALYSIS (TRIGGERS + FREQUENCY), HEALTH INDICATORS SELECTED, OBJECTIVES COVERAGE, STATUS (RESULT INDICATOR), DOCK TYPES (COMPLETE LIST), CHECKER INDEX, INDICATOR: {Indicator Name}, HOW TO RUN, KNOWN GAPS, MARKERS
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md` - Missing: OBJECTIVES SERVED
- `docs/membrane/SYNC_Membrane_System_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/engine/models/PATTERNS_Models.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md` - Missing: OBJECTIVES SERVED
- ... and 288 more

### ESCALATION (82 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/cli/prompt/PATTERNS_Prompt_Command_Workflow_Design.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Review_Evaluate_Changes_And_Produce_Auditable_Report.md` - Escalation marker needs decision (priority: 5)
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md` - Escalation marker needs decision (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/HEALTH_Cybernetic_Studio_Health_Checks.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/api/BEHAVIORS_Api.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/prompt/HEALTH_Prompt_Runtime_Verification.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/core/BEHAVIORS_CLI_Command_Effects.md` - Escalation marker needs decision (priority: 5)
- `AGENTS.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Define_And_Verify_Health_Signals_Mapped_To_Validation_Invariants.md` - Escalation marker needs decision (priority: 5)
- `docs/physics/algorithms/ALGORITHM_Physics_Schema_v1.1_Energy_Physics.md` - COMPLETION_THRESHOLD: What energy level triggers active→comp (priority: 4)
- ... and 72 more

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/physics/API_Physics.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Player_Notes.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/scene-memory/TEST_Scene_Memory.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md` - Doc filename does not use a standard prefix
- `docs/membrane/MAPPING_Doctor_Issues_To_Protocols.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/api/API_Graph_Management.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/CONNECTOME_HEALTH_PAYLOAD.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- ... and 14 more

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/core_utils.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/README.md` - Modified 1d after IMPLEMENTATION doc
- `engine/init_db.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/validation.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/loader.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_outputs.md` - Modified 1d after IMPLEMENTATION doc
- `engine/health/activity_logger.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/api/moments.py` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### CODE_DOC_DELTA_COUPLING (28 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/health/connectome_health_service.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks.py` - Code changed without corresponding doc or SYNC updates
- `engine/moment_graph/traversal.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_sync.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `app/api/sse/route.ts` - Code changed without corresponding doc or SYNC updates
- `ngram/validate.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_core.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/health/checker.py` - Code changed without corresponding doc or SYNC updates
- ... and 18 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/infrastructure/scene-memory/BEHAVIORS_Scene_Memory.md` - Doc filename 'BEHAVIORS_Scene_Memory.md' is too short/non-descriptive
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts` - Code file 'connectome_log_duration_formatting_and_threshold_color_rules.ts' contains 'and', suggesting it should be split
- `docs/ngram_cli_core/ALGORITHM_ngram_cli_core.md` - Doc filename 'ALGORITHM_ngram_cli_core.md' is too short/non-descriptive
- `docs/engine/models/SYNC_Models.md` - Doc filename 'SYNC_Models.md' is too short/non-descriptive
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md` - Naming convention violations task (6): 10 items
- `docs/agents/narrator/OBJECTIVES_Narrator_Goals.md` - Doc filename 'OBJECTIVES_Narrator_Goals.md' is too short/non-descriptive
- `docs/physics/VALIDATION_Energy_Physics.md` - Doc filename 'VALIDATION_Energy_Physics.md' is too short/non-descriptive
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts` - Code file 'connectome_node_background_theme_tokens_by_type_and_language.ts' contains 'and', suggesting it should be split
- `docs/infrastructure/tempo/HEALTH_Tempo.md` - Doc filename 'HEALTH_Tempo.md' is too short/non-descriptive
- `docs/infrastructure/api/ALGORITHM_Api.md` - Doc filename 'ALGORITHM_Api.md' is too short/non-descriptive
- ... and 8 more

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/building` - Missing: HEALTH
- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/connectome/graphs` - Missing: HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - 1 referenced files not found
- ... and 1 more

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/llm_agents` - Total 79K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/connectome/state_store` - Total 95K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/building` - Total 75K chars (threshold: 62K)
- `docs/membrane` - Total 101K chars (threshold: 62K)
- `docs/connectome/log_panel` - Total 71K chars (threshold: 62K)
- `docs/infrastructure/api` - Total 65K chars (threshold: 62K)
- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- ... and 3 more

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/tui/widgets/manager_panel.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### BROKEN_IMPL_LINK (24 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 7 non-existent file(s)
  - Update or remove references: SYNC_World_Runner.md, # DOCS: docs/agents/world-runner/PATTERNS_World_Runner.md, Orchestrator._process_flips
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md` - References 3 non-existent file(s)
  - Update or remove references: runtime/IMPLEMENTATION_Runtime_And_Dependencies.md, structure/IMPLEMENTATION_Code_Structure.md, schema/IMPLEMENTATION_Schema.md
- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: TickResult.flips, graph_queries.py, graph_ops_events.py
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: ExportButtons.handleCopyJsonl, state_store.ledger
- `docs/tools/IMPLEMENTATION_Tools.md` - References 13 non-existent file(s)
  - Update or remove references: stream.jsonl, connectome_doc_bundle_splitter_and_fence_rewriter.py, playthroughs/{id}/stream.jsonl
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - References 4 non-existent file(s)
  - Update or remove references: connectome_energy_badge_bucketed_glow_and_value_formatter.ts, window.setInterval, active_focus.active_step_key
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - References 1 non-existent file(s)
  - Update or remove references: connectome_system_map_node_edge_manifest.ts
- `docs/archive/tui_deprecated_2025-12/IMPLEMENTATION_TUI_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 3 non-existent file(s)
  - Update or remove references: NarratorService.generate, narrator/prompt_builder.py, agent_cli.run_agent
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md` - References 3 non-existent file(s)
  - Update or remove references: overview/IMPLEMENTATION_Overview.md, runtime/IMPLEMENTATION_Runtime_And_Dependencies.md, schema/IMPLEMENTATION_Schema.md
- ... and 14 more

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/archive/tui_deprecated_2025-12/archive/IMPLEMENTATION_Archive_2024-12.md` - Missing: CHAIN, CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, EXTRACTION CANDIDATES, MARKERS
- `docs/infrastructure/api/SYNC_Api.md` - Missing: IN PROGRESS, KNOWN ISSUES, HANDOFF: FOR HUMAN, CONSCIOUSNESS TRACE
- `docs/physics/attention/VALIDATION_Attention_Split_And_Interrupts.md` - Missing: TESTS VS HEALTH, INVARIANTS, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- `docs/schema/PATTERNS_Schema.md` - Missing: CHAIN, THE PROBLEM, THE PATTERN, BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, PRINCIPLES, DATA, DEPENDENCIES, INSPIRATIONS, SCOPE, MARKERS
- `docs/building/ALGORITHM_Ngram_Graph_System.md` - Missing: DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY
- `docs/infrastructure/tempo/HEALTH_Tempo.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), OBJECTIVES COVERAGE, INDICATOR: {Indicator Name}; Too short: DOCK TYPES (COMPLETE LIST)
- `docs/engine/moment-graph-engine/validation/void_tension/VALIDATION_Void_Tension.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/cli/VALIDATION_CLI_Module_Invariants.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX, MARKERS
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md` - Missing: EXTRACTION CANDIDATES
- `docs/physics/graph/PATTERNS_Graph.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, DATA
- ... and 288 more

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/engine/moments/TEST_Moment_Graph_Coverage.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/CONNECTOME_HEALTH_PAYLOAD.md` - Doc filename does not use a standard prefix
- `docs/membrane/SKILLS_AND_PROTOCOLS_Mapping.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/INTEGRATION_NOTES.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/api/API_Graph_Management.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- ... and 14 more

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/building` - Missing: HEALTH
- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/connectome/graphs` - Missing: HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - 1 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- ... and 1 more

### ESCALATION (82 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `AGENTS.md` - Escalation marker needs decision (priority: 5)
- `docs/archive/tui_deprecated_2025-12/VALIDATION_TUI_User_Interface_Invariants.md` - How to test async Textual apps effectively? (priority: 5)
- `docs/infrastructure/api/ALGORITHM_Api.md` - Escalation marker needs decision (priority: 5)
- `docs/engine/models/ALGORITHM_Models.md` - Should all derived properties be explicitly documented in a  (priority: 5)
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/prompt/VALIDATION_Prompt_Bootstrap_Invariants.md` - Escalation marker needs decision (priority: 5)
- `docs/building/mapping.yaml` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/api/BEHAVIORS_Api.md` - Escalation marker needs decision (priority: 5)
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md` - Escalation marker needs decision (priority: 5)
- `docs/archive/tui_deprecated_2025-12/ALGORITHM_TUI_Widget_Interaction_Flow.md` - Should ngram manager run continuously in background? (priority: 5)
- ... and 72 more

### DOC_LINK_INTEGRITY (50 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `ngram/tui/widgets/input_bar.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/commands_agent.py` - Code file references docs but the bidirectional link is broken
- `engine/infrastructure/api/playthroughs.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/init_cmd.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/checkers/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/commands.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/app.py` - Code file references docs but the bidirectional link is broken
- `engine/moment_graph/queries.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/suggestions.py` - Code file references docs but the bidirectional link is broken
- ... and 40 more

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/archive/tui_deprecated_2025-12/PATTERNS_TUI_Modular_Interface_Design.md` - Multiple PATTERNS docs in `tui_deprecated_2025-12/`
- `docs/membrane/VALIDATION_Membrane_System.md` - Multiple VALIDATION docs in `membrane/`
- `docs/physics/BEHAVIORS_Physics/BEHAVIORS_Physics_Overview.md` - Multiple BEHAVIORS docs in `BEHAVIORS_Physics/`
- `docs/schema/SYNC_Schema.md` - Multiple SYNC docs in `schema/`
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - Multiple IMPLEMENTATION docs in `membrane/`
- `docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md` - Multiple ALGORITHM docs in `algorithms/`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `schema/`
- `docs/physics/VALIDATION_Energy_Physics.md` - Multiple VALIDATION docs in `physics/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- `docs/schema/PATTERNS_Schema.md` - Multiple PATTERNS docs in `schema/`
- ... and 8 more

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/agents/narrator` - Total 91K chars (threshold: 62K)
- `docs/building` - Total 75K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/membrane` - Total 101K chars (threshold: 62K)
- `docs/infrastructure/api` - Total 65K chars (threshold: 62K)
- `docs/connectome/node_kit` - Total 83K chars (threshold: 62K)
- `docs/connectome/state_store` - Total 95K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- ... and 3 more

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/memory/moment_processor.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/orchestrator.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_outputs.md` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/api/moments.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/session.py` - Modified 1d after IMPLEMENTATION doc
- `engine/models/nodes.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/api/app.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/world_runner.py` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/tui/widgets/manager_panel.py` - Contains 2 empty/incomplete function(s)
- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago

### CODE_DOC_DELTA_COUPLING (28 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `app/api/sse/route.ts` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/playthroughs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_core.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_naming.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks.py` - Code changed without corresponding doc or SYNC updates
- `app/connectome/components/connectome_health_panel.tsx` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_verification.py` - Code changed without corresponding doc or SYNC updates
- `ngram/validate.py` - Code changed without corresponding doc or SYNC updates
- ... and 18 more

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/ngram_cli_core/ALGORITHM_ngram_cli_core.md` - Doc filename 'ALGORITHM_ngram_cli_core.md' is too short/non-descriptive
- `docs/infrastructure/api/ALGORITHM_Api.md` - Doc filename 'ALGORITHM_Api.md' is too short/non-descriptive
- `docs/engine/IMPLEMENTATION_Engine.md` - Doc filename 'IMPLEMENTATION_Engine.md' is too short/non-descriptive
- `docs/connectome/graph_api/PATTERNS_Graph_API.md` - Doc filename 'PATTERNS_Graph_API.md' is too short/non-descriptive
- `docs/infrastructure/tempo/HEALTH_Tempo.md` - Doc filename 'HEALTH_Tempo.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/BEHAVIORS_Scene_Memory.md` - Doc filename 'BEHAVIORS_Scene_Memory.md' is too short/non-descriptive
- `docs/api/sse/IMPLEMENTATION_SSE_API.md` - Doc filename 'IMPLEMENTATION_SSE_API.md' is too short/non-descriptive
- `docs/physics/VALIDATION_Energy_Physics.md` - Doc filename 'VALIDATION_Energy_Physics.md' is too short/non-descriptive
- `docs/schema/SYNC_Schema.md` - Doc filename 'SYNC_Schema.md' is too short/non-descriptive
- `docs/tools/VALIDATION_Tools.md` - Doc filename 'VALIDATION_Tools.md' is too short/non-descriptive
- ... and 8 more

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### BROKEN_IMPL_LINK (24 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/schema/IMPLEMENTATION_Schema.md` - References 9 non-existent file(s)
  - Update or remove references: test_schema_links.py, base.py, check_health.py
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - References 10 non-existent file(s)
  - Update or remove references: test_loader.py, create_validation.yaml, document_progress.yaml
- `docs/physics/archive/IMPLEMENTATION_Physics_archive_2025-12.md` - References 4 non-existent file(s)
  - Update or remove references: implementation/IMPLEMENTATION_Physics_Dataflow.md, implementation/IMPLEMENTATION_Physics_Code_Structure.md, implementation/IMPLEMENTATION_Physics_Runtime.md
- `docs/connectome/graphs/IMPLEMENTATION_Connectome_Graph_Listing_API_Architecture.md` - References 2 non-existent file(s)
  - Update or remove references: connectome_read_cli.py, route.ts
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: ExportButtons.handleCopyJsonl, state_store.ledger
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: flow_event_schema_and_normalization_contract.ts
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - References 9 non-existent file(s)
  - Update or remove references: connectome_edge_style_tokens_for_trigger_and_calltype_mapping.ts, connectome_edge_pulse_particle_animation_and_boundary_clamp_helpers.ts, connectome_node_boundary_intersection_geometry_helpers.ts
- `docs/physics/IMPLEMENTATION_Physics.md` - References 6 non-existent file(s)
  - Update or remove references: algorithms/ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md, graph_ops_events.py, graph_ops.py
- `docs/archive/tui_deprecated_2025-12/IMPLEMENTATION_TUI_Code_Architecture.md` - References 1 non-existent file(s)
  - Update or remove references: docs/tui/IMPLEMENTATION_TUI_Code_Architecture/IMPLEMENTATION_TUI_Code_Architecture_Structure.md
- `docs/tools/IMPLEMENTATION_Tools.md` - References 13 non-existent file(s)
  - Update or remove references: playthroughs/{id}/stream.jsonl, player.yaml, playthroughs/{id}/player.yaml
- ... and 14 more

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - 1 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - 1 referenced files not found
- `docs/connectome/edge_kit/IMPLEMENTATION_Connectome_Edge_Kit_Component_Map_And_Render_Tokens.md` - 6 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- ... and 1 more

### DOC_LINK_INTEGRITY (50 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/physics/graph/graph_ops_events.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/refactor.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/suggestions.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/input_bar.py` - Code file references docs but the bidirectional link is broken
- `engine/graph/health/check_health.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/agent_container.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/__init__.py` - Code file references docs but the bidirectional link is broken
- `engine/moment_graph/traversal.py` - Code file references docs but the bidirectional link is broken
- `ngram/context.py` - Code file references docs but the bidirectional link is broken
- ... and 40 more

### CODE_DOC_DELTA_COUPLING (28 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/moment_graph/traversal.py` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/playthroughs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_docs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_verification.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_report.py` - Code changed without corresponding doc or SYNC updates
- `engine/health/connectome_health_service.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_ops.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_instructions_docs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_core.py` - Code changed without corresponding doc or SYNC updates
- ... and 18 more

### NON_STANDARD_DOC_TYPE (24 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/health/INTEGRATION_NOTES.md` - Doc filename does not use a standard prefix
- `docs/cli/modules.md` - Doc filename does not use a standard prefix
- `docs/engine/moment-graph-engine/TEST_Moment_Graph_Runtime_Coverage.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Attention_Energy_Split.md` - Doc filename does not use a standard prefix
- `docs/infrastructure/wsl-autostart.md` - Doc filename does not use a standard prefix
- `docs/membrane/MAPPING_Issue_Type_Verification.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/HANDOFF_Rolling_Window_Architecture.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md` - Doc filename does not use a standard prefix
- `docs/membrane/MAPPING_Doctor_Issues_To_Protocols.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/CONNECTOME_HEALTH_PAYLOAD.md` - Doc filename does not use a standard prefix
- ... and 14 more

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/infrastructure/memory/moment_processor.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_results.md` - Modified 1d after IMPLEMENTATION doc
- `engine/moment_graph/traversal.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/activity_logger.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/orchestration/world_runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/loader.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/runner.py` - Modified 1d after IMPLEMENTATION doc
- `ngram/core_utils.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/steps.py` - Modified 1d after IMPLEMENTATION doc
- `engine/init_db.py` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/runtime/IMPLEMENTATION_Runtime_And_Dependencies.md` - Missing: EXTRACTION CANDIDATES
- `docs/connectome/log_panel/ALGORITHM_Connectome_Log_Panel_Log_Rendering_Duration_Coloring_And_Export.md` - Missing: ALGORITHM: {Primary Function Name}
- `docs/archive/tui_deprecated_2025-12/OBJECTIVES_TUI.md` - Missing: PRIMARY OBJECTIVES (ranked), NON-OBJECTIVES, TRADEOFFS (canonical decisions), SUCCESS SIGNALS (observable)
- `docs/cli/prompt/ALGORITHM_Prompt_Bootstrap_Prompt_Construction.md` - Missing: OBJECTIVES AND BEHAVIORS, ALGORITHM: {Primary Function Name}
- `docs/protocol/VALIDATION_Protocol_Invariants.md` - Missing: TESTS VS HEALTH, CONFIDENCE LEVELS, PRIORITY LEVELS, VALIDATION ID INDEX
- `docs/connectome/state_store/IMPLEMENTATION_Connectome_State_Store_Code_Structure_And_Zustand_Actions.md` - Missing: EXTRACTION CANDIDATES
- `docs/core_utils/BEHAVIORS_Core_Utils_Helper_Effects.md` - Missing: OBJECTIVES SERVED
- `docs/archive/tui_deprecated_2025-12/BEHAVIORS_TUI_Interactions.md` - Missing: OBJECTIVES SERVED
- `docs/infrastructure/tempo/PATTERNS_Tempo.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED
- `docs/engine/membrane/PATTERNS_Membrane_Scoping.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED
- ... and 288 more

### ESCALATION (82 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `.claude/skills/SKILL_Create_Module_Documentation_Chain_From_Templates_And_Seed_Todos.md` - Escalation marker needs decision (priority: 5)
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/scene-memory/ALGORITHM_Scene_Memory.md` - Escalation marker needs decision (priority: 5)
- `docs/archive/tui_deprecated_2025-12/VALIDATION_TUI_User_Interface_Invariants.md` - How to test async Textual apps effectively? (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md` - Escalation marker needs decision (priority: 5)
- `docs/infrastructure/scene-memory/TEST_Scene_Memory.md` - Escalation marker needs decision (priority: 5)
- `docs/archive/tui_deprecated_2025-12/HEALTH_TUI_Component_Test_Coverage.md` - How should we handle terminal resizing failures in HEALTH? (priority: 5)
- `docs/schema/ALGORITHM_Schema.md` - Escalation marker needs decision (priority: 5)
- `docs/building/ALGORITHM_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 5)
- `docs/building/BEHAVIORS_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 5)
- ... and 72 more

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/schema/SYNC_Schema.md` - Multiple SYNC docs in `schema/`
- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/membrane/SYNC_Membrane_System.md` - Multiple SYNC docs in `membrane/`
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - Multiple IMPLEMENTATION docs in `membrane/`
- `docs/membrane/VALIDATION_Membrane_System.md` - Multiple VALIDATION docs in `membrane/`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `schema/`
- `docs/physics/BEHAVIORS_Physics/BEHAVIORS_Physics_Overview.md` - Multiple BEHAVIORS docs in `BEHAVIORS_Physics/`
- `docs/physics/archive/SYNC_Physics_History_2025-12.md` - Multiple SYNC docs in `archive/`
- `docs/physics/VALIDATION_Physics/VALIDATION_Physics_Procedures.md` - Multiple VALIDATION docs in `VALIDATION_Physics/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- ... and 8 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts` - Code file 'connectome_log_duration_formatting_and_threshold_color_rules.ts' contains 'and', suggesting it should be split
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts` - Code file 'connectome_node_background_theme_tokens_by_type_and_language.ts' contains 'and', suggesting it should be split
- `docs/physics/graph/VALIDATION_Living_Graph.md` - Doc filename 'VALIDATION_Living_Graph.md' is too short/non-descriptive
- `docs/infrastructure/api/ALGORITHM_Api.md` - Doc filename 'ALGORITHM_Api.md' is too short/non-descriptive
- `docs/agents/narrator/OBJECTIVES_Narrator_Goals.md` - Doc filename 'OBJECTIVES_Narrator_Goals.md' is too short/non-descriptive
- `docs/engine/models/SYNC_Models.md` - Doc filename 'SYNC_Models.md' is too short/non-descriptive
- `docs/connectome/graph_api/PATTERNS_Graph_API.md` - Doc filename 'PATTERNS_Graph_API.md' is too short/non-descriptive
- `docs/infrastructure/tempo/HEALTH_Tempo.md` - Doc filename 'HEALTH_Tempo.md' is too short/non-descriptive
- `docs/ngram_feature/PATTERNS_Ngram_Feature.md` - Doc filename 'PATTERNS_Ngram_Feature.md' is too short/non-descriptive
- `docs/agents/world-runner/BEHAVIORS_World_Runner.md` - Doc filename 'BEHAVIORS_World_Runner.md' is too short/non-descriptive
- ... and 8 more

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/llm_agents` - Total 79K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/connectome/log_panel` - Total 71K chars (threshold: 62K)
- `docs/connectome/node_kit` - Total 83K chars (threshold: 62K)
- `docs/infrastructure/api` - Total 65K chars (threshold: 62K)
- `docs/membrane` - Total 101K chars (threshold: 62K)
- `docs/building` - Total 75K chars (threshold: 62K)
- ... and 3 more

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/building` - Missing: HEALTH
- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/connectome/graphs` - Missing: HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH

### STALE_SYNC (2 files)

**What's wrong:** Outdated SYNC files mislead agents about current state. They may work from wrong assumptions or miss important context about recent changes.

**How to fix:** Review the SYNC file, update LAST_UPDATED, and ensure it reflects what actually exists.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)
- `ngram/tui/widgets/manager_panel.py` - Contains 2 empty/incomplete function(s)

### TODO (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` - Replace repair with work command (priority: 8)

---



---

# Archived: SYNC_Project_Health.md

Archived on: 2025-12-24
Original file: SYNC_Project_Health.md

---

## ISSUES

### BROKEN_IMPL_LINK (24 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md` - References 3 non-existent file(s)
  - Update or remove references: schema/IMPLEMENTATION_Schema.md, runtime/IMPLEMENTATION_Runtime_And_Dependencies.md, structure/IMPLEMENTATION_Code_Structure.md
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - References 1 non-existent file(s)
  - Update or remove references: connectome_system_map_node_edge_manifest.ts
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - References 10 non-existent file(s)
  - Update or remove references: test_loader.py, test_runner.py, test_validation.py
- `docs/building/IMPLEMENTATION_Ngram_Graph_System.md` - References 37 non-existent file(s)
  - Update or remove references: ingest/*.py, prompts.py, agents/handler.py
- `docs/connectome/log_panel/IMPLEMENTATION_Connectome_Log_Panel_Component_Structure_And_Serializer_Integration.md` - References 2 non-existent file(s)
  - Update or remove references: ExportButtons.handleCopyJsonl, state_store.ledger
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - References 1 non-existent file(s)
  - Update or remove references: flow_event_schema_and_normalization_contract.ts
- `docs/engine/models/IMPLEMENTATION_Models.md` - References 1 non-existent file(s)
  - Update or remove references: docs/schema/models/PATTERNS_Pydantic_Schema_Models.md
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - References 3 non-existent file(s)
  - Update or remove references: NarratorService.generate, narrator/prompt_builder.py, agent_cli.run_agent
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - References 2 non-existent file(s)
  - Update or remove references: app/connectome/components/telemetry_camera_controls.ts, pannable_zoomable_zoned_flow_canvas_renderer.tsx
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` - References 7 non-existent file(s)
  - Update or remove references: Orchestrator._process_flips, HEALTH_World_Runner.md, GraphTick.run
- ... and 14 more

### MONOLITH (4 files)

**What's wrong:** Large files are hard to navigate, test, and maintain. They slow down agents who need to load context, and changes become risky because side effects are hard to predict.

**How to fix:** Extract cohesive functionality into separate modules. Start with the largest functions/classes listed above.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `engine/physics/tick_v1_2.py` - 913 lines (threshold: 800)
  - Split: class GraphTickV1_2() (934L, :207), def _phase_moment_flow() (105L, :458), def _phase_narrative_backflow() (81L, :653)
- `app/connectome/connectome.css` - 962 lines (threshold: 800)
- `engine/physics/tick.py` - 837 lines (threshold: 800)
  - Split: class GraphTick() (961L, :83), def run() (85L, :107), def _phase_completion() (68L, :518)
- `ngram/repair_core.py` - 879 lines (threshold: 800)
  - Split: async def spawn_repair_agent_async() (229L, :623), async def spawn_repair_agent_with_verification_async() (165L, :852), def run_agent_sync() (110L, :742)

### ESCALATION (1 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/building/VALIDATION_Ngram_Graph_System.md` - Escalation marker needs decision (priority: 8)
  - Review and resolve escalation in this file

### DOC_TEMPLATE_DRIFT (298 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/connectome/telemetry_adapter/HEALTH_Connectome_Telemetry_Adapter_Runtime_Verification_Of_Stream_Integrity_And_Buffer_Bounds.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, OBJECTIVES COVERAGE, STATUS (RESULT INDICATOR), DOCK TYPES (COMPLETE LIST), INDICATOR: {Indicator Name}
- `docs/infrastructure/scene-memory/IMPLEMENTATION_Scene_Memory.md` - Missing: DESIGN PATTERNS, SCHEMA, DATA FLOW AND DOCKING (FLOW-BY-FLOW), STATE MANAGEMENT, RUNTIME BEHAVIOR, CONFIGURATION, EXTRACTION CANDIDATES
- `docs/engine/ALGORITHM_Engine.md` - Missing: OVERVIEW, OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, MARKERS
- `docs/engine/moments/PATTERNS_Moments.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, DATA, INSPIRATIONS, SCOPE
- `docs/connectome/graphs/BEHAVIORS_Listing_Available_Connectome_Graphs.md` - Missing: BEHAVIORS, OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, MARKERS
- `docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md` - Missing: BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, DATA, INSPIRATIONS, SCOPE
- `docs/membrane/SYNC_Membrane_System_archive_2025-12.md` - Missing: MATURITY, CURRENT STATE, IN PROGRESS, RECENT CHANGES, KNOWN ISSUES, HANDOFF: FOR AGENTS, HANDOFF: FOR HUMAN, TODO, CONSCIOUSNESS TRACE, POINTERS
- `docs/infrastructure/api/ALGORITHM_Player_Input_Flow.md` - Missing: CHAIN, OVERVIEW, OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, COMPLEXITY, HELPER FUNCTIONS, INTERACTIONS, MARKERS
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md` - Missing: WHEN TO USE HEALTH (NOT TESTS), INDICATOR: {Indicator Name}
- ... and 288 more

### ESCALATION (83 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `docs/agents/narrator/PATTERNS_Narrator.md` - Escalation marker needs decision (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/ALGORITHM_Cybernetic_Studio_Process_Flow.md` - Escalation marker needs decision (priority: 5)
- `docs/schema/SYNC_Schema_archive_2025-12.md` - DECAY_RATE: What (priority: 5)
- `docs/cli/core/HEALTH_CLI_Command_Test_Coverage.md` - Escalation marker needs decision (priority: 5)
- `ngram/repair_instructions.py` - Components/{Path(issue.path).stem} (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md` - Escalation marker needs decision (priority: 5)
- `docs/llm_agents/HEALTH_LLM_Agent_Coverage.md` - Escalation marker needs decision (priority: 5)
- `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md` - Escalation marker needs decision (priority: 5)
- `docs/protocol/BEHAVIORS_Observable_Protocol_Effects.md` - How detailed should SYNC updates be? (priority: 5)
- `docs/agents/narrator/ALGORITHM_Scene_Generation.md` - Escalation marker needs decision (priority: 5)
- ... and 73 more

### DOC_LINK_INTEGRITY (50 files)

**What's wrong:** Code pointing to nonexistent docs or docs that do not mention the code breaks the bidirectional documentation chain.

**How to fix:** Add the referenced docs and mention the code file (IMPL/chain entries) so agents can travel both directions.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `engine/physics/graph/graph_interface.py` - Code file references docs but the bidirectional link is broken
- `app/connectome/page.tsx` - Code file references docs but the bidirectional link is broken
- `ngram/status_cmd.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/commands_agent.py` - Code file references docs but the bidirectional link is broken
- `engine/graph/health/check_health.py` - Code file references docs but the bidirectional link is broken
- `ngram/project_map.py` - Code file references docs but the bidirectional link is broken
- `engine/connectome/__init__.py` - Code file references docs but the bidirectional link is broken
- `ngram/sync.py` - Code file references docs but the bidirectional link is broken
- `engine/physics/health/base.py` - Code file references docs but the bidirectional link is broken
- `ngram/tui/widgets/input_bar.py` - Code file references docs but the bidirectional link is broken
- ... and 40 more

### DOC_DUPLICATION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/schema/ALGORITHM_Schema_Module_Doc_Routing.md` - Multiple ALGORITHM docs in `schema/`
- `docs/physics/VALIDATION_Energy_Physics.md` - Multiple VALIDATION docs in `physics/`
- `docs/infrastructure/api/ALGORITHM_Playthrough_Creation.md` - Multiple ALGORITHM docs in `api/`
- `docs/schema/PATTERNS_Schema.md` - Multiple PATTERNS docs in `schema/`
- `docs/archive/tui_deprecated_2025-12/PATTERNS_TUI_Modular_Interface_Design.md` - Multiple PATTERNS docs in `tui_deprecated_2025-12/`
- `docs/physics/VALIDATION_Physics/VALIDATION_Physics_Procedures.md` - Multiple VALIDATION docs in `VALIDATION_Physics/`
- `docs/membrane/PATTERNS_Membrane_System.md` - Multiple PATTERNS docs in `membrane/`
- `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md` - Multiple IMPLEMENTATION docs in `schema/`
- `docs/membrane/SYNC_Membrane_System.md` - Multiple SYNC docs in `membrane/`
- `docs/schema/BEHAVIORS_Schema_Module_Observable_Schema_Effects.md` - Multiple BEHAVIORS docs in `schema/`
- ... and 8 more

### LEGACY_MARKER (4 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/membrane/VALIDATION_Completion_Verification.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Legacy todo format (use @ngram:todo)
- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Legacy todo format (use @ngram:todo)

### NON_STANDARD_DOC_TYPE (25 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/engine/moments/TEST_Moment_Graph_Coverage.md` - Doc filename does not use a standard prefix
- `docs/connectome/VISUAL_STYLEGUIDE_Connectome.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TOOL_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Story_Notes.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/TEST_World_Runner_Coverage.md` - Doc filename does not use a standard prefix
- `docs/membrane/MAPPING_Issue_Type_Verification.md` - Doc filename does not use a standard prefix
- `docs/agents/world-runner/INPUT_REFERENCE.md` - Doc filename does not use a standard prefix
- `docs/physics/mechanisms/MECHANISMS_Primes_Lag_Decay.md` - Doc filename does not use a standard prefix
- `docs/connectome/health/CONNECTOME_HEALTH_PAYLOAD.md` - Doc filename does not use a standard prefix
- `docs/agents/narrator/TEMPLATE_Player_Notes.md` - Doc filename does not use a standard prefix
- ... and 15 more

### NAMING_CONVENTION (18 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/connectome/graph_api/PATTERNS_Graph_API.md` - Doc filename 'PATTERNS_Graph_API.md' is too short/non-descriptive
- `docs/cli/archive/SYNC_CLI_Development_State_archive_2025-12.md` - Naming convention violations task (6): 10 items
- `app/connectome/components/node_kit/connectome_node_background_theme_tokens_by_type_and_language.ts` - Code file 'connectome_node_background_theme_tokens_by_type_and_language.ts' contains 'and', suggesting it should be split
- `docs/tools/VALIDATION_Tools.md` - Doc filename 'VALIDATION_Tools.md' is too short/non-descriptive
- `docs/agents/narrator/OBJECTIVES_Narrator_Goals.md` - Doc filename 'OBJECTIVES_Narrator_Goals.md' is too short/non-descriptive
- `docs/infrastructure/scene-memory/BEHAVIORS_Scene_Memory.md` - Doc filename 'BEHAVIORS_Scene_Memory.md' is too short/non-descriptive
- `docs/schema/SYNC_Schema.md` - Doc filename 'SYNC_Schema.md' is too short/non-descriptive
- `docs/physics/VALIDATION_Energy_Physics.md` - Doc filename 'VALIDATION_Energy_Physics.md' is too short/non-descriptive
- `app/connectome/components/connectome_log_duration_formatting_and_threshold_color_rules.ts` - Code file 'connectome_log_duration_formatting_and_threshold_color_rules.ts' contains 'and', suggesting it should be split
- `docs/infrastructure/api/ALGORITHM_Api.md` - Doc filename 'ALGORITHM_Api.md' is too short/non-descriptive
- ... and 8 more

### STALE_IMPL (11 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/physics/IMPLEMENTATION_Physics.md` - 5 referenced files not found
- `docs/connectome/node_kit/IMPLEMENTATION_Connectome_Node_Kit_Component_Map_And_Styling_Tokens.md` - 2 referenced files not found
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` - 1 referenced files not found
- `docs/llm_agents/IMPLEMENTATION_LLM_Agent_Code_Architecture.md` - 3 referenced files not found
- `docs/schema/IMPLEMENTATION_Schema.md` - 8 referenced files not found
- `docs/membrane/IMPLEMENTATION_Membrane_System.md` - 6 referenced files not found
- `docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md` - 2 referenced files not found
- `docs/tools/IMPLEMENTATION_Tools.md` - 2 referenced files not found
- `docs/connectome/runtime_engine/IMPLEMENTATION_Connectome_Runtime_Engine_Code_Structure_And_Control_Surface.md` - 1 referenced files not found
- `docs/connectome/event_model/IMPLEMENTATION_Connectome_Event_Model_Code_Architecture_And_Schema.md` - 1 referenced files not found
- ... and 1 more

### LARGE_DOC_MODULE (13 files)

**What's wrong:** Large doc modules consume significant context window when loaded. Agents may not be able to load everything they need.

**How to fix:** Archive old sections to dated files, split into sub-modules, or remove redundant content.

**Protocol:** Load `VIEW_Refactor_Improve_Code_Structure.md` before starting.

**Files:**

- `docs/agents/narrator` - Total 91K chars (threshold: 62K)
- `docs/connectome/state_store` - Total 95K chars (threshold: 62K)
- `docs/connectome/runtime_engine` - Total 75K chars (threshold: 62K)
- `docs/physics` - Total 85K chars (threshold: 62K)
- `docs/agents/world-runner` - Total 80K chars (threshold: 62K)
- `docs/schema` - Total 64K chars (threshold: 62K)
- `docs/connectome/flow_canvas` - Total 64K chars (threshold: 62K)
- `docs/infrastructure/api` - Total 65K chars (threshold: 62K)
- `docs/llm_agents` - Total 79K chars (threshold: 62K)
- `docs/building` - Total 84K chars (threshold: 62K)
- ... and 3 more

### CODE_DOC_DELTA_COUPLING (27 files)

**What's wrong:** Code changes that are not reflected in docs or SYNC leave the documentation stale and untrustworthy.

**How to fix:** Update the doc or SYNC file after modifying the code so the timestamps stay coupled.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `tools/stream_dialogue.py` - Code changed without corresponding doc or SYNC updates
- `app/api/sse/route.ts` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor.py` - Code changed without corresponding doc or SYNC updates
- `engine/physics/graph/graph_queries_moments.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_sync.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_core.py` - Code changed without corresponding doc or SYNC updates
- `engine/infrastructure/api/playthroughs.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_reference.py` - Code changed without corresponding doc or SYNC updates
- `ngram/repair_report.py` - Code changed without corresponding doc or SYNC updates
- `ngram/doctor_checks_naming.py` - Code changed without corresponding doc or SYNC updates
- ... and 17 more

### INCOMPLETE_IMPL (2 files)

**What's wrong:** Empty functions indicate incomplete implementation. The interface exists but the behavior doesn't.

**How to fix:** Fill in the empty functions with actual implementation.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/physics/graph/graph_interface.py` - Contains 10 empty/incomplete function(s)
- `ngram/tui/widgets/manager_panel.py` - Contains 2 empty/incomplete function(s)

### NEW_UNDOC_CODE (21 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `ngram/core_utils.py` - Modified 1d after IMPLEMENTATION doc
- `engine/infrastructure/memory/moment_processor.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/loader.py` - Modified 1d after IMPLEMENTATION doc
- `engine/init_db.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/runner.py` - Modified 1d after IMPLEMENTATION doc
- `engine/connectome/validation.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/query_results.md` - Modified 1d after IMPLEMENTATION doc
- `engine/health/connectome_health_service.py` - Modified 1d after IMPLEMENTATION doc
- `engine/health/activity_logger.py` - Modified 1d after IMPLEMENTATION doc
- `engine/graph/health/example_queries.cypher` - Modified 1d after IMPLEMENTATION doc
- ... and 11 more

### INCOMPLETE_CHAIN (6 files)

**What's wrong:** Missing doc types mean agents can't answer certain questions about the module. For example, without IMPLEMENTATION, they don't know where code lives or how data flows.

**How to fix:** Create the missing doc types using templates from .ngram/templates/.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/ngram_cli_core` - Missing: VALIDATION, IMPLEMENTATION, HEALTH
- `docs/building` - Missing: HEALTH
- `docs/frontend/app_shell` - Missing: ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH
- `docs/connectome/graphs` - Missing: HEALTH
- `docs/ngram_feature` - Missing: IMPLEMENTATION, HEALTH
- `docs/connectome/graph_api` - Missing: BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH

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

- `docs/frontend/app_shell/SYNC_App_Shell_State.md` - Last updated 670 days ago
- `docs/connectome/graph_api/SYNC_Graph_API.md` - Last updated 736 days ago

### HARDCODED_CONFIG (9 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `engine/physics/graph/graph_ops.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_ops_read_only_interface.py` - Contains hardcoded configuration values
- `ngram/status_cmd.py` - Contains hardcoded configuration values
- `engine/migrations/migrate_001_schema_alignment.py` - Contains hardcoded configuration values
- `engine/graph/health/check_health.py` - Contains hardcoded configuration values
- `engine/init_db.py` - Contains hardcoded configuration values
- `ngram/llms/gemini_agent.py` - Contains hardcoded configuration values
- `engine/infrastructure/api/app.py` - Contains hardcoded configuration values
- `engine/physics/graph/graph_queries.py` - Contains hardcoded configuration values

---

