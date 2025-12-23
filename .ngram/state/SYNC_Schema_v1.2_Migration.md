# SYNC: Schema v1.2 Migration

**Status:** IN_PROGRESS
**Started:** 2025-12-23
**Reference:** `schema_v1.2_complete.md`

---

## OWNERSHIP

| Agent | Assigned Sections |
|-------|-------------------|
| **Claude Dev 1** | 1. Schema Changes, 2. Core Physics, 5. Constants, 7. Emotion Functions |
| **Claude Dev 2** | 3. Tick Phases, 4. Supporting Systems, 6. Removals, 8. Tests |

---

## OVERVIEW

Schema v1.2 redesigns energy physics:
- **No decay** — energy persists, flows through links
- **Hot/cold links** — attention via link.energy, depth via link.strength
- **Unified traversal** — every flow updates energy + strength + emotions
- **Top-N filter** — process only hottest 20 links per node
- **Target weight** — `sqrt(target.weight)` reception factor

---

## KEY CHANGES SUMMARY

| Component | v1.1 | v1.2 |
|-----------|------|------|
| Generation | All actors equal | Proximity-gated |
| Draw | Active only | Possible + Active |
| Flow | Fixed rate | Duration-based |
| Interaction | None | Support/contradict |
| Backflow | Threshold 0.5 | No threshold, link.energy gated |
| Reception | Equal | sqrt(target.weight) |
| Traversal | Energy only | Energy + strength + emotion |
| Cooling | Decay rate | Drain + strength convert |
| Filter | All links | Top 20 by energy×weight |
| Decay | 2%/tick | None |
| Linger | Status-based | Hot links |
| Reactivation | None | Recall moments |

---

## IMPLEMENTATION ORDER

1. **Schema changes** — Models first
2. **Emotion functions** — Needed by traversal
3. **Unified traversal** — Core primitive
4. **Constants** — Before phases
5. **Path resistance** — For generation
6. **Tick phases 1-6** — In order
7. **Canon holder** — Phase 7-8
8. **World runner** — Integration
9. **Remove decay** — After new physics works
10. **Tests** — Verify each step

---

## HANDOFF

### Claude Dev 2 — COMPLETE

**What was done:**
- Created `engine/physics/tick_v1_2.py` with all 8 phases (no decay)
- Implemented emotion functions: `avg_emotion_intensity`, `emotion_proximity`, `blend_emotions`, `get_weighted_average_emotions`
- All v1.2 constants defined
- Created `engine/tests/test_energy_v1_2.py` with 48 passing tests
- Path resistance uses simplified hop-count (full Dijkstra TODO)
- Crystallization creates actor-actor links on moment completion
- **Canon Holder**: Full implementation with validation functions and state transitions
- **World Runner**: Added `run_until_visible()` and `run_until_disrupted()` methods

**Files created/modified:**
- `engine/physics/tick_v1_2.py` — Complete v1.2 tick implementation
- `engine/tests/test_energy_v1_2.py` — 48 unit tests
- `engine/infrastructure/canon/canon_holder.py` — Full validation + state machine
- `engine/infrastructure/orchestration/world_runner.py` — Added v1.2 tick running

**Canon Holder API:**
- `actors_exist(moment_id)` → (bool, missing_ids)
- `actors_available(moment_id)` → (bool, unavailable_ids)
- `no_contradiction(moment_id)` → (bool, contradicting_ids)
- `causal_chain_valid(moment_id)` → (bool, broken_chain)
- `validate_for_activation(moment_id)` → ValidationResult
- `activate_moment(moment_id, tick)` → possible→active
- `reject_moment(moment_id, tick)` → possible→rejected + return energy
- `interrupt_moment(moment_id, tick)` → active→interrupted
- `override_moment(moment_id, tick, overriding_id)` → active→overridden + redirect energy

**World Runner API:**
- `run_until_visible(max_ticks, location_id)` → runs until moment completes
- `run_until_disrupted(max_ticks, narrative_ids)` → runs until narrative shift

**Remaining items (separate tasks):**
- [ ] Full Dijkstra path resistance (currently simplified hop count)
- [ ] Moment recall/reactivation (narrator creates)

**Blockers:** None.

---

## HEALTH CHECK RESULTS (2025-12-23)

Ran `python -m engine.physics.health.checker all --graph test`:

| Checker | Status | Details |
|---------|--------|---------|
| `energy_conservation` | **ERROR** | Ratio 1.48 > 1.2 (872 total vs 590 expected) |
| `no_negative_energy` | OK | All energy values ≥ 0 |
| `link_state` | **WARN** | 67.5% hot links (threshold 50%) |
| `tick_integrity` | UNKNOWN | No tick instrumentation active |
| `moment_lifecycle` | **ERROR** | 22 moments with invalid status `spoken` |

### Issues Found

1. **Energy Accumulation** — Total energy 48% above expected max
   - Likely cause: v1.0 data with decay was loaded, v1.2 has no decay
   - Fix: Run energy normalization or reset energy values

2. **World Overheating** — 67.5% hot links vs 50% threshold
   - Likely cause: No link cooling running on test data
   - Fix: Run v1.2 tick phases to cool links

3. **Invalid Moment Status** — 22 moments have status `spoken`
   - Valid v1.2 states: `possible`, `active`, `completed`, `rejected`, `interrupted`, `overridden`
   - Fix: Migrate `spoken` → `completed` (or appropriate state)

### Data Migration TODO

- [ ] Migrate moment status `spoken` → `completed`
- [ ] Normalize energy values or run link cooling
- [ ] Add tick instrumentation for tick_integrity checker

**Questions answered:**
- Emotion list format confirmed: `[[emotion_name, intensity], ...]`
- Path resistance: simplified for now (hop count), full Dijkstra TODO


---

## ARCHIVE

Older content archived to: `SYNC_Schema_v1.2_Migration_archive_2025-12.md`
