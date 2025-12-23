# Archived: SYNC_Schema_v1.2_Migration.md

Archived on: 2025-12-23
Original file: SYNC_Schema_v1.2_Migration.md

---

## PROGRESS TRACKER

### 1. SCHEMA CHANGES

#### Moment Model (`engine/models/nodes.py`)
| Field | Type | Status | Notes |
|-------|------|--------|-------|
| `status` | enum | `[x]` | possible\|active\|completed\|rejected\|interrupted\|overridden |
| `prose` | string | `[x]` | Written at creation |
| `duration_minutes` | float | `[x]` | Affects radiation rate |
| `weight` | float | `[x]` | Priority/importance |
| `tick_created` | int | `[x]` | When created |
| `tick_resolved` | Optional[int] | `[x]` | When resolved |
| `energy` | float | `[x]` | Verify exists |

#### Link Model (`engine/models/links.py`)
| Field | Type | Status | Notes |
|-------|------|--------|-------|
| `energy` | float | `[x]` | Current attention (hot/cold) |
| `strength` | float | `[x]` | Accumulated depth (permanent) |
| `emotions` | List[[str,float]] | `[x]` | Verify exists |
| `conductivity` | float | `[x]` | Verify exists |
| `weight` | float | `[x]` | Verify exists |
| `node_a/node_b` | string | `[x]` | Rename from from_id/to_id |

#### Actor Model (`engine/models/nodes.py`)
| Field | Type | Status | Notes |
|-------|------|--------|-------|
| `weight` | float | `[x]` | Unbounded (0-∞) |
| `energy` | float | `[x]` | Unbounded (0-∞) |
| Remove `energy_capacity` | - | `[x]` | Not present (confirmed) |

---

### 2. CORE PHYSICS

#### Unified Traversal (`engine/physics/flow.py`)
| Function | Status | Notes |
|----------|--------|-------|
| `energy_flows_through(link, amount, emotions, origin, target)` | `[x]` | Core traversal |
| `avg_emotion_intensity(emotions)` | `[x]` | In constants.py |
| `blend_emotions(existing, incoming, rate)` | `[x]` | In links.py |

#### Target Weight Factor
| Change | Status | Notes |
|--------|--------|-------|
| Apply `sqrt(target.weight)` to received energy | `[x]` | `target_weight_factor()` + `calculate_received()` |

#### Top-N Link Filter (`engine/physics/flow.py`)
| Function | Status | Notes |
|----------|--------|-------|
| `get_hot_links(node, n=20)` | `[x]` | Score by energy×weight |
| Define `COLD_THRESHOLD = 0.01` | `[x]` | In constants.py |

---

### 3. TICK PHASES

**Owner:** Claude Dev 2
**File:** `engine/physics/tick_v1_2.py` (NEW)

#### Phase 1: Generation
| Change | Status | Notes |
|--------|--------|-------|
| Sort actors by weight desc | `[x]` | Priority order |
| Calculate proximity via path resistance | `[x]` | Gate generation |
| Formula: `actor.energy += weight × RATE × proximity` | `[x]` | |

#### Phase 2: Moment Draw
| Change | Status | Notes |
|--------|--------|-------|
| Process BOTH possible AND active | `[x]` | Not just active |
| Sort by energy×weight desc | `[x]` | Priority |
| Get top 20 expresses links | `[x]` | Hot filter |
| Apply unified traversal | `[x]` | Update links |
| Apply sqrt(target.weight) | `[x]` | Reception |

#### Phase 3: Moment Flow
| Change | Status | Notes |
|--------|--------|-------|
| ACTIVE moments only | `[x]` | Not possible |
| Radiation rate = 1/(duration×12) | `[x]` | Duration affects |
| Sort by energy×weight desc | `[x]` | Priority |
| Top 20 outgoing links | `[x]` | Hot filter |
| Distribute by weight share | `[x]` | |
| Moment energy depletes | `[x]` | As it radiates |

#### Phase 4: Moment Interaction (NEW)
| Change | Status | Notes |
|--------|--------|-------|
| Find shared narratives | `[x]` | Between active moments |
| Calculate emotion proximity | `[x]` | 0-1 similarity |
| Support if proximity > 0.7 | `[x]` | +5% × proximity |
| Contradict if proximity < 0.3 | `[x]` | -5% × (1-proximity) |

#### Phase 5: Narrative Backflow
| Change | Status | Notes |
|--------|--------|-------|
| No threshold (all narratives) | `[x]` | Remove 0.5 threshold |
| Gate by link.energy | `[x]` | Unfocused = no backflow |
| Sort by energy desc | `[x]` | Priority |
| Top 20 actor links | `[x]` | Hot filter |
| Narrative depletes | `[x]` | As it backflows |

#### Phase 6: Link Cooling (NEW)
| Change | Status | Notes |
|--------|--------|-------|
| Drain 30% to nodes | `[x]` | Split 50/50 |
| Convert 10% to strength | `[x]` | Permanent growth |
| Apply strength formula | `[x]` | With emotions |
| Sort by energy×weight desc | `[x]` | Priority |

#### Phase 7 & 8: Completion/Rejection
| Change | Status | Notes |
|--------|--------|-------|
| Completion: just set status | `[x]` | Links cool naturally |
| Rejection: return 80% to player | `[x]` | Energy return |
| Rejection: speaker links stay warm | `[x]` | Cool naturally |

---

### 4. SUPPORTING SYSTEMS

**Owner:** Claude Dev 2

#### Path Resistance (`engine/physics/tick_v1_2.py`)
| Function | Status | Notes |
|----------|--------|-------|
| `path_resistance(from_id, to_id)` | `[x]` | Simplified (hop count) |
| `_calculate_proximity()` | `[x]` | 1/(1+resistance) |
| Edge resistance = 1/conductance | `[ ]` | Full Dijkstra TODO |

#### Crystallization (`engine/physics/tick_v1_2.py`)
| Change | Status | Notes |
|--------|--------|-------|
| On completion: find shared actors | `[x]` | `_crystallize_actor_links()` |
| Create `relates` link if none | `[x]` | |
| Inherit emotions from moment | `[x]` | |
| Initial cond=0.2, weight=0.2 | `[x]` | |

#### Reactivation
| Type | Status | Notes |
|------|--------|-------|
| Actor: proximity change | `[x]` | Via Phase 1 generation |
| Actor: backflow if link.energy | `[x]` | Via Phase 5 |
| Moment: recall moment creation | `[ ]` | Narrator creates (separate task) |

#### World Runner (`engine/infrastructure/orchestration/world_runner.py`)
| Function | Status | Notes |
|----------|--------|-------|
| `run_until_visible()` | `[x]` | Runs ticks until moment completes at location |
| `run_until_disrupted()` | `[x]` | Runs ticks until narrative energy shifts |

#### Canon Holder (`engine/infrastructure/canon/canon_holder.py`)
| Function | Status | Notes |
|----------|--------|-------|
| `actors_exist(moment)` | `[x]` | Checks expresses + about links |
| `actors_available(moment)` | `[x]` | Checks alive status |
| `no_contradiction(moment)` | `[x]` | Checks narrative RELATES links |
| `causal_chain_valid(moment)` | `[x]` | Checks CAN_BECOME + SEQUENCE |
| `validate_for_activation()` | `[x]` | Full validation (all 4 checks) |
| `ValidationResult` dataclass | `[x]` | Collects all validation issues |
| Transition: possible→active | `[x]` | `activate_moment()` |
| Transition: possible→rejected | `[x]` | `reject_moment()` — returns 80% energy |
| Transition: active→completed | `[x]` | In tick_v1_2.py Phase 7 |
| Transition: active→interrupted | `[x]` | `interrupt_moment()` — creates SUPERSEDES link |
| Transition: active→overridden | `[x]` | `override_moment()` — redirects energy based on proximity |

---

### 5. CONSTANTS (`engine/physics/constants.py`)

| Constant | Value | Status | Notes |
|----------|-------|--------|-------|
| `GENERATION_RATE` | 0.5 | `[x]` | |
| `DRAW_RATE` | 0.3 | `[x]` | |
| `BACKFLOW_RATE` | 0.1 | `[x]` | |
| `COLD_THRESHOLD` | 0.01 | `[x]` | |
| `TOP_N_LINKS` | 20 | `[x]` | |
| `TICK_DURATION_SECONDS` | 5 | `[x]` | |
| `TICKS_PER_MINUTE` | 12 | `[x]` | |
| `LINK_DRAIN_RATE` | 0.3 | `[x]` | |
| `LINK_TO_STRENGTH_RATE` | 0.1 | `[x]` | |
| `SUPPORT_THRESHOLD` | 0.7 | `[x]` | |
| `CONTRADICT_THRESHOLD` | 0.3 | `[x]` | |
| `INTERACTION_RATE` | 0.05 | `[x]` | |
| `REJECTION_RETURN_RATE` | 0.8 | `[x]` | |

---

### 6. REMOVALS

**Owner:** Claude Dev 2

| Item | Status | Notes |
|------|--------|-------|
| Remove decay logic | `[x]` | New tick_v1_2.py has no decay |
| Test without decay | `[ ]` | Verify stability |
| Add targeted fix only if needed | `[ ]` | If accumulation issues |

**Note:** v1.2 tick (`tick_v1_2.py`) is a clean implementation with no decay.
Old tick.py still has decay for backwards compat. Migration complete when
systems switch to `GraphTickV1_2.run()`.

---

### 7. EMOTION FUNCTIONS (`engine/physics/constants.py` + `links.py` + `flow.py`)

| Function | Status | Notes |
|----------|--------|-------|
| `emotion_proximity(a, b)` | `[x]` | In constants.py, weighted Jaccard, 0.2-1.0 |
| `blend_emotions(existing, incoming, rate)` | `[x]` | In links.py |
| `avg_emotion_intensity(emotions)` | `[x]` | In constants.py |
| `get_weighted_average_emotions(moment)` | `[x]` | In flow.py |

---

### 8. TESTS (`engine/tests/test_energy_v1_2.py`)

**Owner:** Claude Dev 2
**Status:** COMPLETE — 48 tests, all passing

| Test | Status | Notes |
|------|--------|-------|
| Emotion functions (14 tests) | `[x]` | avg, proximity, blend, weighted_avg |
| Constants (12 tests) | `[x]` | All v1.2 constants verified |
| Flow formulas (5 tests) | `[x]` | Unified flow, target weight, radiation rate |
| Hot/cold links (3 tests) | `[x]` | Heat score, thresholds |
| Link cooling (5 tests) | `[x]` | Drain + strength conversion |
| Moment interaction (4 tests) | `[x]` | Support/contradict formulas |
| Rejection (1 test) | `[x]` | Energy return rate |
| TickResultV1_2 (2 tests) | `[x]` | Result dataclass |
| No decay (2 tests) | `[x]` | Energy lifecycle verification |

---

