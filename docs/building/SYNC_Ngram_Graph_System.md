# ngram Graph System — Sync: Current State

```
STATUS: DESIGNING → PHASE 1
UPDATED: 2025-12-23
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Graph_System.md
PATTERNS:        ./PATTERNS_Ngram_Graph_System.md
BEHAVIORS:       ./BEHAVIORS_Ngram_Graph_System.md
ALGORITHM:       ./ALGORITHM_Ngram_Graph_System.md
VALIDATION:      ./VALIDATION_Ngram_Graph_System.md
IMPLEMENTATION:  ./IMPLEMENTATION_Ngram_Graph_System.md
HEALTH:          ./HEALTH_Ngram_Graph_System.md (not yet)
THIS:            SYNC_Ngram_Graph_System.md (you are here)
```

---

## CURRENT STATE

**Phase:** Design complete. Starting Phase 1 implementation.

---

## IMPLEMENTATION PHASES

| Phase | Goal | Value Delivered | Status |
|-------|------|-----------------|--------|
| 1. See Graph | Ingest docs → nodes | Docs queryable in graph | **NEXT** |
| 2. Active Context | Query active Narratives | Physics-driven relevance | — |
| 3. One Agent | Agent responds to Moment | Agent produces output | — |
| 4. Lasting Work | Agent creates Narratives | Knowledge growth | — |
| 5. Multi-Agent | 6 agents differentiate | Parallel work | — |
| 6. Continuous | World runs autonomously | Full vision | — |

### Phase 1 Scope

**Input:** `docs/building/*.md` + `mapping.yaml`
**Output:** Graph with Spaces, Narratives, Things
**Verify:** Query graph, see docs as nodes

Deliverables:
- `building/ingest/discover.py` — find files matching patterns
- `building/ingest/parse.py` — extract content, sections, markers
- `building/ingest/create.py` — call engine.create_* APIs
- `building/config/mapping.py` — load mapping.yaml

---

### What Exists

| Doc | Status | Content |
|-----|--------|---------|
| OBJECTIVES | Complete | 8 ranked objectives, non-objectives, tradeoffs |
| PATTERNS | Complete | 8 key decisions, invariants, open patterns |
| BEHAVIORS | Complete | 11 observable value behaviors, anti-behaviors |
| ALGORITHM | Complete | 4 client procedures (ingest, query, handler, create) |
| VALIDATION | Complete | 17 invariants across 6 categories |
| mapping.yaml | Complete | v2.0 repo-to-graph mapping |
| IMPLEMENTATION | Complete | Code structure, 3 flows with docking points |
| HEALTH | Not started | — |

### What's Designed

- **Graph structure:** 5 node types (Space, Actor, Narrative, Moment, Thing)
- **Link types:** 9 types per schema v1.2 (contains, expresses, about, relates, attached_to, leads_to, sequence, primes, can_become)
- **Physics:** Energy/weight/strength/conductivity fields defined
- **Client boundary:** Clear separation between client (us) and engine
- **Ingest pipeline:** mapping.yaml defines all transformations

### What's NOT Designed

- Agent prompts (base prompts, response format)
- Bootstrap sequence (first run procedure)
- Incremental ingest (file changes after bootstrap)
- Health checkers for this module
- Actual implementation code

---

## RECENT CHANGES

| Date | Change |
|------|--------|
| 2025-12-23 | Resolved E1-E4: Engine API verified, Pydantic chosen, file-level, two-pass |
| 2025-12-23 | Added ENGINE API MAPPING section with node/link method signatures |
| 2025-12-23 | Added mechanisms doc escalations (D1-D7, Q1-Q9) to doc chain with phase tags |
| 2025-12-23 | Defined 6-phase implementation plan |
| 2025-12-23 | Analyzed engine reuse (40% reuse, 60% new) |
| 2025-12-23 | Reviewed all escalations with recommendations |
| 2024-12-23 | Created full doc chain (OBJECTIVES → VALIDATION) |
| 2024-12-23 | Created mapping.yaml v2.0 with 9 link types |

---

## OPEN DECISIONS

| Decision | Options | Leaning | Phase |
|----------|---------|---------|-------|
| Space granularity | per module / per objective / per feature | Start with module | 1 |
| Agent count | fixed 6 / dynamic | Start fixed | 3 |
| Goal completion | physics decay / explicit close | Physics decay | 2 |
| Ingest trigger | manual / file watcher / git hook | Manual first | 1 |
| Type inference | heuristics / LLM | Heuristics first | 3 |
| [D1] Agent query mechanism | engine.get_context() / direct graph / physics-aware | engine.get_context() | 2 |
| [D2] Speed in multiplayer | global speed / per-actor | Global speed | 6 |
| [D3] Running agent injection | inject / queue / interrupt | Queue | 3 |
| [D4] Agent space assignment | config / root / dynamic | Config in agents.yaml | 3 |
| [D5] Opening message | moment only / + summary / full dump | Moment + summary | 3 |
| [D6] Module naming | mapping.yaml / conventions / LLM | mapping.yaml globs | 1 |
| [D7] Human query mechanism | CLI / API / physics-aware | CLI first | 2 |

---

## BLOCKERS

None currently. Ready for implementation.

---

## NEXT STEPS (Phase 1)

1. ~~**Resolve Phase 1 escalations**~~ — ✅ E1-E4 resolved
2. **Create building/ package** — `__init__.py`, directory structure
3. **Implement mapping loader** — `config/mapping.py` with Pydantic models
4. **Implement discover** — `ingest/discover.py` file pattern matching
5. **Implement parse** — `ingest/parse.py` doc parsing, marker extraction
6. **Implement create** — `ingest/create.py` engine API calls + Space→Narrative link
7. **Test with docs/building/** — verify 8 docs become Narratives

---

## ENGINE API MAPPING (Verified)

### Node Creation

| mapping.yaml | Engine Method | Key Args |
|--------------|---------------|----------|
| `Space` | `GraphOps.add_place()` | `id, name, type, weight, energy` |
| `Narrative` | `GraphOps.add_narrative()` | `id, name, content, type, weight` |
| `Thing` | `GraphOps.add_thing()` | `id, name, type, weight, energy` |
| `Actor` | `GraphOps.add_character()` | `id, name, type, weight, energy` |

### Link Creation

| mapping.yaml | Engine Method | Notes |
|--------------|---------------|-------|
| `contains` (Space→Space) | `add_contains()` | Exists |
| `contains` (Space→Narrative) | Custom cypher | Need to add |
| `relates` | `add_narrative_link()` | `supports, contradicts, elaborates` |
| `about` | `add_about()` | `moment_id, target_id, weight` |

### Gap: Space→Narrative Containment

Current `add_contains()` only handles Space→Space. For Phase 1, add custom:

```python
def add_narrative_to_space(space_id: str, narrative_id: str):
    cypher = """
    MATCH (s:Space {id: $space_id})
    MATCH (n:Narrative {id: $narr_id})
    MERGE (s)-[:CONTAINS]->(n)
    """
```

---

## HANDOFFS

### For Phase 1 Implementation

**Resolved:**
- ✅ Engine API verified — `add_place`, `add_narrative`, `add_thing` exist
- ✅ Mapping parser — use Pydantic

**Remaining decisions:**
- Section granularity — start file-level
- Link timing — two-pass (nodes first, then links)

**Build order:**
1. `building/config/mapping.py` — load + validate mapping.yaml
2. `building/ingest/discover.py` — glob patterns from mapping
3. `building/ingest/parse.py` — markdown parsing, marker extraction
4. `building/ingest/create.py` — engine API calls + custom Space→Narrative link

### For Human

Review remaining escalations: E2-E4 (parser, granularity, link timing).

---

## MARKERS

### Phase 1 TODOs

<!-- @ngram:done Verify engine API exists and signatures -->
<!-- @ngram:todo Create building/ package directory structure -->
<!-- @ngram:todo Implement mapping.py with Pydantic models -->
<!-- @ngram:todo Implement discover.py file pattern matching -->
<!-- @ngram:todo Implement parse.py markdown + marker extraction -->
<!-- @ngram:todo Implement create.py engine API calls -->
<!-- @ngram:todo Add Space→Narrative containment link method -->
<!-- @ngram:todo Test ingest with docs/building/ -->

### Phase 1 Escalations

<!-- @ngram:resolved E1 Engine API verified — add_place, add_narrative, add_thing, add_character exist. Gap: Space→Narrative containment needs custom cypher. -->
<!-- @ngram:resolved E2 Mapping parser — use Pydantic models for validation -->
<!-- @ngram:resolved E3 Section granularity — start file-level, defer section extraction -->
<!-- @ngram:resolved E4 Link timing — two-pass (all nodes, then all links) -->

### Future Phase TODOs

<!-- @ngram:todo Create agents.yaml with initial agents (Phase 3) -->
<!-- @ngram:todo Define physics constants (Phase 2) -->
<!-- @ngram:todo Create HEALTH doc with runtime checkers (Phase 6) -->

### Propositions

<!-- @ngram:proposition Create a "dry run" mode that logs what would be created without touching graph -->
<!-- @ngram:proposition Start ingest with docs/building/ only, expand after verified -->
