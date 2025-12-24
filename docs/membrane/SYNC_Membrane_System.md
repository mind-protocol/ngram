# SYNC: Membrane System

```
LAST_UPDATED: 2025-12-24
UPDATED_BY: Claude (Agent 2 - persistence & verification)
STATUS: CANONICAL
```

---

## Terminology

| Term | Format | Purpose |
|------|--------|---------|
| **Skill** | Markdown | Domain knowledge, which protocols when |
| **Protocol** | YAML | Procedure: ask → query → branch → call_protocol → create |
| **Membrane** | Tool | Executor that runs protocols |

---

## Current State

### Coverage

```
Protocols: 20/20 implemented (100%)
├── Phase 0: add_cluster ✅
├── Phase 1: explore_space, record_work, investigate ✅
├── Phase 2: add_objectives, add_patterns, update_sync, add_behaviors, add_algorithm ✅
├── Phase 3: add_invariant, add_health_coverage, add_implementation ✅
├── Phase 4: raise_escalation, resolve_blocker, capture_decision ✅
├── Phase 5: define_space, create_doc_chain, add_goals, add_todo ✅
└── Meta: completion_handoff ✅ (called by all protocols)
```

### Implemented

| Component | Status | Location |
|-----------|--------|----------|
| MCP Server | Working | `tools/mcp/membrane_server.py` |
| ConnectomeRunner | Working | `engine/connectome/runner.py` |
| Session + call stack | Working | `engine/connectome/session.py` |
| Step execution | Working | `engine/connectome/steps.py` |
| **Graph Schema** | Working | `engine/connectome/schema.py` |
| **Graph Persistence** | Working | `engine/connectome/persistence.py` |
| Coverage validator | Working | `tools/coverage/validate.py` |
| Health checker | Working | `ngram/doctor_checks_membrane.py` |
| **Verification System** | Working | `ngram/repair_verification.py` |
| Protocols | 20 complete | `protocols/*.yaml` |
| Skills | 15 complete | `templates/ngram/skills/*.md` |
| Health doc | Complete | `docs/membrane/HEALTH_Membrane_System.md` |
| Verification doc | Complete | `docs/membrane/VALIDATION_Completion_Verification.md` |
| Issue→Verification map | Complete | `docs/membrane/MAPPING_Issue_Type_Verification.md` |

### Skills (15 total)

| Skill ID | File | Status |
|----------|------|--------|
| ngram.add_cluster | SKILL_Add_Cluster_Dynamic_Creation.md | ✅ |
| ngram.author_skills | SKILL_Author_Skills_Structure_And_Quality.md | ✅ |
| ngram.author_protocols | SKILL_Author_Protocols_Structure_And_Quality.md | ✅ |
| ngram.create_module_docs | SKILL_Create_Module_Documentation_Chain... | ✅ |
| ngram.module_define_boundaries | SKILL_Define_Module_Boundaries... | ✅ |
| ngram.implement_with_docs | SKILL_Implement_Write_Or_Modify_Code... | ✅ |
| ngram.health_define_and_verify | SKILL_Define_And_Verify_Health_Signals... | ✅ |
| ngram.debug_investigate | SKILL_Debug_Investigate_And_Fix_Issues... | ✅ |
| ngram.update_sync | SKILL_Update_Module_Sync_State... | ✅ |
| ngram.onboard | SKILL_Onboard_Understand_Existing_Module... | ✅ |
| ngram.extend | SKILL_Extend_Add_Features_To_Existing... | ✅ |
| ngram.ingest | SKILL_Ingest_Raw_Data_Sources... | ✅ |
| ngram.orchestrate | SKILL_Orchestrate_Feature_Integration... | ✅ |
| ngram.review | SKILL_Review_Evaluate_Changes... | ✅ |

### Protocols (20 total)

| Phase | Protocol | Status | Notes |
|-------|----------|--------|-------|
| 0 | add_cluster | ✅ | |
| 1 | explore_space | ✅ | |
| 1 | record_work | ✅ | |
| 1 | investigate | ✅ | |
| 2 | add_objectives | ✅ | |
| 2 | add_patterns | ✅ | |
| 2 | update_sync | ✅ | |
| 2 | add_behaviors | ✅ | |
| 2 | add_algorithm | ✅ | |
| 3 | add_invariant | ✅ | |
| 3 | add_health_coverage | ✅ | |
| 3 | add_implementation | ✅ | |
| 4 | raise_escalation | ✅ | For blocked work |
| 4 | resolve_blocker | ✅ | |
| 4 | capture_decision | ✅ | |
| 5 | define_space | ✅ | v1.1 with explanations |
| 5 | create_doc_chain | ✅ | |
| 5 | add_goals | ✅ | |
| 5 | add_todo | ✅ | For deferred work |
| Meta | completion_handoff | ✅ | Called by all protocols |

---

## Handoff

**For agents:**
- All 20 protocols in `protocols/*.yaml`
- 15 skills in `templates/ngram/skills/*.md`
- Doctor→Protocol mapping in `docs/membrane/MAPPING_Doctor_Issues_To_Protocols.md`
- Issue→Verification mapping in `docs/membrane/MAPPING_Issue_Type_Verification.md`
- Graph schema in `engine/connectome/schema.py`
- Graph persistence in `engine/connectome/persistence.py`
- Verification system in `ngram/repair_verification.py`
- `define_space.yaml` is the reference example with full explanations

**For human review:**
- Run validator: `python3 tools/coverage/validate.py`
- Review: `specs/coverage.yaml` for full mapping
- Test imports: `python3 -c "from engine.connectome.schema import validate_node; print('OK')"`
- Test verification: `python3 -c "from ngram.repair_verification import create_membrane_query_function; print('OK')"`

---

## CHAIN

- **Prev:** IMPLEMENTATION_Membrane_System.md
- **Doc root:** OBJECTIVES_Membrane_System.md


---

## ARCHIVE

Older content archived to: `SYNC_Membrane_System_archive_2025-12.md`


---

## ARCHIVE

Older content archived to: `SYNC_Membrane_System_archive_2025-12.md`
