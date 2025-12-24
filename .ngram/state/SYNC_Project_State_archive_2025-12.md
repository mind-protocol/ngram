# Archived: SYNC_Project_State.md

Archived on: 2025-12-23
Original file: SYNC_Project_State.md

---

## ACTIVE WORK

### Schema v1.2 — Energy Physics Migration

- **Area:** `engine/`
- **Status:** IN PROGRESS
- **Owner:** Next agent
- **Tracking:** `.ngram/state/SYNC_Schema_v1.2_Migration.md`
- **Context:** Complete spec provided. Major changes from v1.1:
  - Remove all decay logic
  - Add link.energy (hot/cold) + link.strength (permanent)
  - Unified traversal function for all energy flows
  - Top-20 link filter per node
  - New Phase 4 (moment interaction) and Phase 6 (link cooling)

### Health System (DONE)

- **Area:** `engine/health/`, `app/api/sse/`
- **Status:** Complete
- **What:** Unified health service + activity logging + SSE integration
- **Files:**
  - `engine/health/connectome_health_service.py`
  - `engine/health/activity_logger.py`
  - `app/api/sse/route.ts`
  - `tools/test_health_live.py`

---


## RECENT CHANGES

### 2025-12-23: Generic Schema Migration (Blood Ledger → Generic)

- **What:** Removed all game-specific "Blood Ledger" references, migrated Character→Actor, Place→Space
- **Why:** Decision: models should be generic, not game-specific
- **Files changed:**
  - `engine/models/nodes.py`: Header changed, docstrings updated (Actor, Space)
  - `engine/models/base.py`: Header changed to generic
  - `engine/models/links.py`: Header changed to generic
  - `engine/tests/test_spec_consistency.py`: EXPECTED_NODE_TYPES uses Actor/Space
  - 32+ engine files: Removed "Blood Ledger" from headers
  - `docs/schema/OBJECTIVES_Schema.md`: Escalation marked resolved
  - `docs/schema/IMPLEMENTATION_Schema.md`: Escalation marked resolved
- **Impact:** Schema is now project-agnostic, no game-specific terminology

### 2025-12-23: Schema v1.1 Implementation Progress

- **What:** Implemented core Schema v1.1 models and physics utilities
- **Files changed:**
  - `engine/models/base.py`: MomentStatus enum with 6 states
  - `engine/models/nodes.py`: Moment (prose, sketch, tick_activated, tick_resolved), unbounded energy/weight on all nodes
  - `engine/models/links.py`: LinkType enum, LinkBase class, blend_emotions()
  - `engine/physics/constants.py`: v1.1 constants (GENERATION_RATE, MOMENT_DRAW_RATE, etc.)
  - `engine/physics/graph/graph_query_utils.py`: calculate_link_resistance(), dijkstra_with_resistance()
  - `engine/physics/graph/graph_ops.py`: Fixed duplicate tick_resolved parameter
- **Remaining:** Tick phases, state transitions, liquidation, agent responsibilities, tests

### 2025-12-23: Major Decisions Session

- **What:** Resolved 17 escalations covering architecture, schema evolution, validation philosophy
- **Why:** Clean up decision debt, establish clear patterns
- **Impact:**
  - TUI deprecated → Next.js web interface
  - All enums → free text except `node_type`
  - Doctor stays deterministic
  - Validation: persist valid, return precise errors
  - SYNC updates: summary + pointers with function names

### 2025-12-23: tick → tick_created Migration

- **What:** Renamed Moment.tick to tick_created, removed backwards compat alias
- **Why:** Schema evolution policy — no deprecated fields
- **Impact:**
  - `engine/models/nodes.py:Moment`
  - `engine/physics/graph/graph_ops.py:add_moment`
  - `engine/physics/graph/graph_queries_moments.py`
  - Migration script: `engine/migrations/migrate_tick_to_tick_created.py`

---


## TODO

### Schema v1.1 — Energy Physics (Full Implementation)

Reference: `schema_v1.1_complete.md` (provided in session)

#### Schema Changes

- [x] **1. Moment Model** (`engine/models/nodes.py`) ✓ DONE
  - Added `status` enum: `possible | active | completed | rejected | interrupted | overridden`
  - Added `tick_activated: Optional[int]`
  - Added `tick_resolved: Optional[int]`
  - Added `prose: str`, `sketch: Optional[str]`
  - Ensured `energy: float` exists (0-∞, unbounded)

- [x] **2. Link Model** (`engine/models/links.py`) ✓ DONE
  - Added `LinkType` enum with 7 types
  - Added `LinkBase` with: `node_a/node_b`, `energy`, `strength`, `emotions`, `conductivity`
  - Added `blend_emotions()` function for Hebbian coloring

- [x] **3. Actor Model** (`engine/models/nodes.py`) ✓ DONE
  - `weight` and `energy` are unbounded (0-∞)
  - No `energy_capacity` — decay handles runaway energy naturally

#### Physics Changes

- [x] **4. Tick Phases** (`engine/physics/tick.py`) ✓ DONE
  - `run_v1_1()` implements all 6 phases
  - Phase 1: `_phase_generation()` — actors generate energy
  - Phase 2: `_phase_moment_draw()` — moments draw from actors
  - Phase 3: `_phase_moment_flow()` — moments flow to nodes
  - Phase 4: `_phase_narrative_backflow()` — narratives radiate
  - Phase 5: `_phase_decay()` — link/node decay
  - Phase 6: `_phase_completion()` — liquidate + crystallize

- [x] **5. Unified Flow Formula** (`engine/physics/tick.py`) ✓ DONE
  - Implemented in phase methods: `flow = source.energy × rate × conductivity × weight`
  - `emotion_proximity()` available in constants.py

- [x] **6. Path Resistance** (`engine/physics/graph/graph_query_utils.py`) ✓ DONE
  - `calculate_link_resistance()`: resistance = 1/(conductivity × weight × emotion_factor)
  - `dijkstra_with_resistance()`: Dijkstra with hop limit, returns path + total_resistance

- [x] **7. Emotion Proximity** (`engine/physics/constants.py`) ✓ DONE
  - `emotion_proximity()`: returns [0.5, 1.5] factor based on emotion alignment
  - Returns 1.0 baseline when either list empty

- [x] **8. Hebbian Coloring** (`engine/models/links.py`) ✓ DONE
  - `blend_emotions()`: blends incoming emotions into link emotions
  - Blend rate: `flow/(flow+1)` per formula

#### New Mechanisms

- [ ] **9. Moment State Transitions** (`engine/infrastructure/canon/canon_holder.py`)
  - `possible → active`: Canon holder validates coherence
  - `active → completed`: Energy threshold + duration + validation → liquidate
  - `active → interrupted`: Superseded → liquidate to connected
  - `active → overridden`: Contradicted → redirect through player
  - `possible → rejected`: Incoherent → return energy to player

- [x] **10. Liquidation** (`engine/physics/tick.py`) ✓ DONE
  - `_liquidate_moment()`: distributes energy to connected nodes by weight share
  - Sets moment.energy = 0, moment becomes inert bridge

- [ ] **11. Redirect (Override)** (`engine/infrastructure/canon/canon_holder.py`)
  - Calculate emotion proximity between old and new moment
  - Transfer: `base (30%) + proximity × 70%` → new targets
  - Remainder "haunts" original narrative

- [x] **12. Link Crystallization** (`engine/physics/tick.py`) ✓ DONE
  - `_crystallize_actor_links()`: creates RELATES links between actors on moment completion
  - Initial strength from CRYSTALLIZATION_INITIAL_STRENGTH constant

- [x] **13. Narrative Backflow** (`engine/physics/tick.py`) ✓ DONE
  - `_phase_narrative_backflow()`: narratives above threshold radiate to believers

#### Agent Responsibilities

- [ ] **14. Runner Creates** (`engine/infrastructure/orchestration/world_runner.py`)
  - Creates possible moments
  - Creates new actors
  - Creates moment→actor links (expresses, about)
  - Does NOT create moment→narrative links (narrator does that)

- [ ] **15. Canon Holder Validates** (`engine/infrastructure/canon/canon_holder.py`)
  - Validates possible→active (coherence check)
  - Approves active→completed (threshold + validity)
  - Triggers interrupt/override
  - Rejects incoherent (returns energy to player)

- [ ] **16. Narrator Creates Semantic Links** (`engine/infrastructure/orchestration/narrator.py`)
  - Creates moment→narrative links (what it's "about")
  - Uses moment emotions for prose generation

#### Constants

- [x] **17. Add Physics Constants** (`engine/physics/constants.py`) ✓ DONE
  ```python
  GENERATION_RATE = 1.0
  MOMENT_DRAW_RATE = 0.5
  FLOW_RATE = 0.3
  LINK_ENERGY_DECAY_RATE = 0.4
  LINK_STRENGTH_DECAY_RATE = 0.1
  NODE_ENERGY_DECAY_RATE = 0.2
  MOMENT_COMPLETION_THRESHOLD = 0.8  # @ngram:escalation
  CRYSTALLIZATION_THRESHOLD = 3
  MAX_EMOTIONS_PER_LINK = 7
  ```

#### Tests

- [x] **18. Energy Flow Tests** (`engine/tests/test_energy_flow_v11.py`) ✓ DONE
  - 39 tests covering: flow formula, emotion proximity, path resistance, blend_emotions, models, constants
  - Test unified formula produces correct ratios
  - Test speaker draws more than witness via link properties only
  - Test path resistance uses conductivity not hops
  - Test liquidation distributes correctly
  - Test crystallization creates new links
  - Test override redirects with haunting
  - Test rejection returns to player

### ngram Framework

- [ ] Implement `ngram work <path> [objective]` to replace `repair`
- [ ] Remove deprecated TUI code (after web interface ready)
- [ ] Add `ngram doctor --benchmark` for latency measurement

### Backlog

- [ ] Remaining escalation review (~40+ open)
- [ ] Web interface (Next.js) setup
- IDEA: `ngram review` as separate AI-powered quality command

---



---

# Archived: SYNC_Project_State.md

Archived on: 2025-12-24
Original file: SYNC_Project_State.md

---

## RECENT CHANGES

### 2025-12-24: Schema v1.2 Final Items — Dijkstra + Recall

**Full Dijkstra Path Resistance:**
- `tick_v1_2.py:_path_resistance()` now uses proper Dijkstra with v1.2 formula
- `edge_resistance = 1 / (conductivity × weight × emotion_factor)`
- Falls back to hop-count if subgraph query fails

**Moment Recall/Reactivation (`canon_holder.py`):**
- `recall_moment()` — creates new recall moment referencing original
- `get_recallable_moments()` — finds moments by actor/narrative/location
- `reactivate_moment()` — revives rejected/interrupted if conditions changed

**Schema v1.2 Status:** COMPLETE — all items implemented

---

### 2025-12-24: Membrane System v1.2 Complete

**All 20 protocols verified with full v1.1 pattern:**
- 19 protocols: `gather_thoughts` → `call_handoff` → `$complete`
- 1 protocol (`completion_handoff`): terminal protocol

**Graph integration complete:**
- Schema validation: `engine/connectome/schema.py` aligned with canonical `docs/schema/schema.yaml` v1.2
- Persistence layer: `engine/connectome/persistence.py` validates before writing
- FalkorDB connection: Already exists via `GraphOps`/`GraphQueries` in `tools/mcp/membrane_server.py`
- Connectivity constraint: New clusters MUST connect to existing nodes

**Verified v1.2 objectives:**
- ✅ 100% protocol coverage (20/20)
- ✅ All protocols have attribute explanations
- ✅ Mandatory verification with graph queries
- ✅ Loop protection (max 3 retries, oscillation detection)
- ✅ Completion handoff captures feedback
- ✅ Schema validation with guidance errors

**Location:** `docs/membrane/SYNC_Membrane_System.md`

---

### 2025-12-24: Protocol v1.1 Pattern Verification

**Finding:** All 18 protocols already have the v1.1 pattern fully applied. No updates needed.

**Pattern elements present in all:**
1. Detailed WHAT/WHY/FORMAT comments on each node/link attribute
2. `gather_thoughts` step for protocol reflection/feedback
3. `call_handoff` step invoking `completion_handoff`

**Location:** `protocols/*.yaml` (20 files total)

---

### 2025-12-24: Schema v1.2 Field Migration + Coverage Validation + Doctor Cleanup

**Field Migration:**
- Migrated `status: spoken` → `status: completed` in 32 YAML protocol files
- Updated stale docstrings in 10+ Python files referencing old "spoken" status
- Updated lifecycle documentation in `nodes.py`, `graph_ops.py` to reflect v1.2 statuses
- Valid statuses now: POSSIBLE, ACTIVE, COMPLETED, REJECTED, INTERRUPTED, OVERRIDDEN

**Coverage Validation System:**
- Verified SYNC was out of date (claimed 18% coverage, reality was 100%)
- Ran `python3 tools/coverage/validate.py` — all 19 protocols pass
- Updated `docs/concepts/coverage/SYNC_Coverage_Validation.md` to CANONICAL status

**Doctor Cleanup (69 → 29 critical issues):**
- Archived deprecated TUI docs to `docs/archive/tui_deprecated_2025-12/`
- Updated `modules.yaml` with 17 module mappings (resolved 39 UNDOCUMENTED issues)
- Created `docs/building/DECISIONS_Ngram_Graph_System.md` with 18 proposed resolutions for escalations

**Remaining Critical Issues (29):**
- 24 BROKEN_IMPL_LINK — docs referencing non-existent files (need manual review)
- 4 MONOLITH — large files (acceptable for now)
- 1 ESCALATION — covered in DECISIONS doc

**Verification:**
- All 48 v1.2 energy tests pass
- Python syntax checks pass
- YAML validation passes

---

### 2025-12-23: Membrane System v1 Documentation

- **What:** Creating complete doc chain for Membrane System v1 — structured dialogues for graph interaction
- **Location:** `docs/membrane/` (new module)
- **Components:**
  - **Architecture:** Doctor → Protocol → Membrane → Graph
  - **Protocols (6):** module_design, health_coverage, feature_implementation, escalation_handling, decision_capture, progress_tracking
  - **Membranes (7):** explore_space, add_objectives, add_invariant, add_health_coverage, record_work, investigate, resolve_blocker
  - **Query language:** find/links/related/contents with presets
- **Key decisions:**
  - "Skills" renamed to "Protocols" (that's what they are)
  - Doctor should call graph for missing specs (dependency-aware)
  - Protocols and membrane YAML specs listed in docs but implemented separately
- **Status:** COMPLETE — doc chain + `call_protocol` implemented

---

### 2025-12-23: Removed Tension entity type references from docs/engine/

- **What:** Systematically removed all references to "Tension" as a graph node/entity type from 10 files in `docs/engine/` directory, replacing with appropriate pressure terminology per Schema v1.2.
- **Why:** Schema v1.2 defines only 5 node types (Actor, Space, Thing, Narrative, Moment). Tension has been replaced with "pressure" computed from narrative contradictions.
- **Changes:**
  - `tension_pressure` → `dramatic_pressure`
  - `tension_boost` → `dramatic_boost`
  - `dominant_tension_age` → `dominant_pressure_age`
  - "tension scaling" → "pressure scaling"
  - "tensions" (plural entity) → "pressure dynamics" or removed
  - Kept "tension" where used as narrative/dramatic concept (e.g., "tension shaping")
- **Files modified:** 10 files across `docs/engine/membrane/`, `docs/engine/models/`, `docs/engine/moment-graph-engine/`
- **Verification:** Remaining "tension" occurrences are all narrative/dramatic concepts or proper names (e.g., "Void Tension" validation doc), not entity types.

---

