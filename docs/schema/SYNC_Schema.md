# Schema — Sync: Current State

```
LAST_UPDATED: 2025-12-23
UPDATED_BY: Claude (v1.2 simplified link types + no decay)
```

---

## CURRENT STATE

Schema module is **CANONICAL v1.2** — stable, doc chain complete.

**v1.2 changes APPLIED:**
- 9 link types (added `about`, `attached_to` as energy carriers)
- **NO DECAY** — link cooling replaces arbitrary decay
- Semantic properties: `name`, `role`, `direction` replace old type differentiation
- Migration: 14 old types → 9 new types (old types become property values)
- Hot/cold filtering via `heat_score = energy × weight`
- Top-N link filter (20 per node)
- Unified traversal updates energy + strength + emotions

**v1.1 changes APPLIED:**
- Bidirectional: node_a/node_b replaces from_id/to_id
- Unified link model with energy dynamics

**v1.0 migration COMPLETE:**
- Character→Actor, Place→Space: all code + 24 databases migrated

---

## RESOLVED

**SEMANTIC_PROXIMITY:** DECIDED — Option B (embedding distance)
- Accurate emotion matching worth the cost
- Cache embeddings for common emotions
- Use lightweight model (e.g., sentence-transformers)
- Fallback to keyword overlap if embedding service unavailable

---

## OPEN QUESTIONS

@ngram:todo — **MAX_EMOTIONS_PER_DIRECTION:** Cap at 7 (implemented in add_emotion)
- Currently defaults to 7, drops lowest intensity when exceeded
- Adjust if needed based on usage

---

## RESOLVED

**VALENCE_INFERENCE:** DROPPED
- Emotion names carry semantic signal
- LLM can infer positive/negative from context if needed
- No pre-computed valence required

**EMOTION_CONSOLIDATION:** IMPLEMENTED
- `consolidate_emotions()` in engine/models/links.py
- Uses diminishing returns: 0.7 + 0.3 → 0.85
- `add_emotion()` helper with max_emotions cap

---

## FILES

| File | Purpose | Status |
|------|---------|--------|
| `docs/schema/schema.yaml` | Authoritative base schema | **v1.2** |
| `engine/graph/health/schema.yaml` | Blood Ledger extension | **v1.1** |
| `engine/models/links.py` | Pydantic link models | **v1.2** (role, direction added) |
| `engine/models/nodes.py` | Pydantic node models | **v1.2** (duration_minutes added) |
| `engine/physics/flow.py` | Unified traversal primitives | **v1.2** (NEW) |
| `engine/physics/constants.py` | Physics constants | **v1.2** (no decay) |
| `engine/physics/tick_v1_2.py` | Tick implementation | **v1.2** (NEW) |
| `docs/schema/PATTERNS_Schema.md` | Design philosophy | CANONICAL |
| `docs/schema/OBJECTIVES_Schema.md` | Goals and tradeoffs | CANONICAL |
| `docs/schema/SYNC_Schema.md` | This file | **v1.2** |

---

## COMPLETED MIGRATIONS

### v1.0: Character→Actor, Place→Space (2025-12-23)

- **Code changes:** 34 files updated
- **Database migration:** 24 graphs migrated (1,143 actors, 2,019 spaces)
- **Verification:** All imports pass, no regressions

### v1.1: Link Model Simplification (2025-12-23)

- **Schema updates:** docs/schema/schema.yaml, engine/graph/health/schema.yaml
- **Model updates:** engine/models/links.py (energy field removed)
- **Physics:** No changes needed (energy already flows through nodes)
- **Database migration:** Not yet run (link field migration pending)

---

## PROPOSITIONS

- **SCHEMA_VERSIONING:** Version check in graph nodes
- **AUTO_FIX:** `--fix` flag for safe auto-repairs
- **EMOTION_VOCABULARY:** Optional vocabulary for common emotions
- **PARALLELIZE_QUERIES:** Speed up large graph validation

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** VIEW_Implement (world runner, canon holder)

**Current focus:**
1. World Runner: `run_until_visible()`, `run_until_disrupted()`
2. Canon Holder: validation functions (actors_exist, actors_available, etc.)
3. Full Dijkstra path resistance (currently simplified hop-count)

**Key context:**
- Full v1.2 spec: `engine/physics/tick_v1_2.py`
- Unified flow formula: `flow = source.energy × rate × conductivity × weight × emotion_factor`
- **NO DECAY** — link cooling replaces decay (30% drain + 10% strength)
- Hot/cold filtering via `heat_score = energy × weight`
- Top-N filter: process only hottest 20 links per node
- Semantic properties: `role` and `direction` on relates links

**Watch out for:**
- Link direction inversions: AT → contains, CARRIES → attached_to
- Use `role` and `direction` instead of creating new link types
- Moments exit physics when all links cold (not via status)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Schema v1.2 complete. Key change: **NO DECAY** — energy flows through links, cooling handles lifecycle. Simplified from many link types to 9 unified types with semantic properties (role, direction).

**Key v1.2 changes:**
- 9 link types (4 energy carriers + 5 structural)
- Semantic properties: role (believer, originator, etc.) + direction (support, oppose, etc.)
- Hot/cold filtering via heat_score (energy × weight)
- Link cooling: 30% drains to nodes, 10% converts to strength
- Top-N filter: process only hottest 20 links per node

**Implementation status:**
- Schema models: COMPLETE (links.py, nodes.py)
- Physics primitives: COMPLETE (flow.py, constants.py)
- Tick implementation: COMPLETE (tick_v1_2.py) — 48 tests passing
- Remaining: World runner, canon holder, full Dijkstra


---

## ARCHIVE

Older content archived to: `SYNC_Schema_archive_2025-12.md`
