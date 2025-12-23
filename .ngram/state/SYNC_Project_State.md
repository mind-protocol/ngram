# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-23
UPDATED_BY: Claude (Tension entity type removal from docs/engine/)
```

---

## RECENT CHANGES

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

## CURRENT STATE

The project is in active development with two main tracks:

1. **ngram Framework** — CLI tooling for AI agents is stable.
   - `ngram work <path> [objective]` implemented
   - Health panel wired to SSE with live connectome signals
   - Activity logging: summary (500 lines) + detail (5000 lines)

2. **Graph Engine** — Schema v1.2 migration IN PROGRESS. Major redesign:
   - **No decay** — energy persists, flows through links
   - **Hot/cold links** — attention via link.energy, depth via link.strength
   - **Unified traversal** — every flow updates energy + strength + emotions
   - **Top-N filter** — process only hottest 20 links per node
   - **Target weight** — sqrt(target.weight) reception factor

   **Tracking:** `.ngram/state/SYNC_Schema_v1.2_Migration.md`

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| `ngram work` not implemented | medium | `ngram/` | Replaces `repair`, objective-driven |
| TUI still exists but deprecated | low | `ngram/tui/` | Will be removed, web replaces it |
| Many Blood Ledger escalations open | low | `docs/` | Game-specific, review ongoing |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Current focus:** Schema v1.1 Energy Physics — continue implementation

**Completed (this session):**
- Schema models (1-3): MomentStatus, Moment fields, LinkType, LinkBase, unbounded energy/weight ✓
- Physics utilities (6-8): emotion_proximity, path resistance Dijkstra, blend_emotions ✓
- Constants (17): All v1.1 constants added ✓

**Next priorities:**
- Tick phases (4): Update `engine/physics/tick.py` with 6-phase tick
- Unified flow formula (5): Implement in tick.py
- Moment state transitions (9): Canon holder state machine
- Migration: Old field usages (tick_resolved → tick_resolved) across ~50 files

**Key context:**
- Unified formula: `flow = source.energy × rate × conductivity × weight × emotion_factor`
- Path resistance: `resistance = 1/(conductivity × weight × emotion_factor)`, use `dijkstra_with_resistance()`
- Emotion proximity: `emotion_proximity()` returns [0.5, 1.5] factor

**Watch out for:**
- Old field names still in use: `tick_resolved`, `tick_resolved`, `status = 'completed'` need migration
- Blood Ledger vs ngram scope — engine/ is game-specific, ngram/ is framework

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Schema v1.1 (Energy Physics) is fully designed and validated. 17 escalations resolved today. Architecture clarified: CLI for agents, web for humans.

**Decisions made recently:**
- TUI → Next.js (TUI deprecated)
- Enums → free text (except node_type)
- Doctor stays deterministic
- SYNC: summary + pointers with function names
- Validation: persist valid, return precise errors

**Needs your input:**
- Remaining ~40+ escalations (mostly Blood Ledger-specific)
- Priority order for Schema v1.1 implementation

**Concerns:**
- Large implementation scope for v1.1 — may want to phase it

---

## CONSCIOUSNESS TRACE

**Project momentum:**
High momentum. Major decisions made. Clear spec ready for implementation.

**Architectural concerns:**
Schema v1.1 is large — may benefit from phased implementation (schema first, then physics, then agent responsibilities).

**Opportunities noticed:**
The unified formula is elegant — no special cases simplifies both code and mental model.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `engine/` | Active (v1.1 ready) | `docs/engine/*/SYNC_*.md` |
| `ngram/` | Stable | `docs/cli/*/SYNC_*.md` |
| `docs/` | Updating | (various) |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Key modules for v1.1:**
| Module | Code | Docs | Status |
|--------|------|------|--------|
| physics | `engine/physics/` | `docs/physics/` | Needs v1.1 update |
| models | `engine/models/` | `docs/engine/models/` | Needs v1.1 schema |
| canon | `engine/infrastructure/canon/` | (pending) | Needs v1.1 transitions |
| narrator | `engine/infrastructure/orchestration/` | `docs/agents/narrator/` | Needs semantic links |

**Coverage notes:**
Physics docs need major update to reflect v1.1 unified formula and phases.


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`
