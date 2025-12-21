# Physics — Algorithm: Mechanisms (Energy, Pressure, Surfacing)

```
STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against local tree
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Physics.md
BEHAVIORS:       ../BEHAVIORS_Physics.md
THIS:            ALGORITHM_Physics_Mechanisms.md (you are here)
VALIDATION:      ../VALIDATION_Physics.md
HEALTH:          ../HEALTH_Physics.md
SYNC:            ../SYNC_Physics.md

IMPL:            engine/physics/tick.py
IMPL:            engine/physics/graph/graph_queries.py
IMPL:            engine/physics/graph/graph_ops_moments.py
IMPL:            engine/moment_graph/traversal.py
IMPL:            engine/moment_graph/surface.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

This document enumerates the **mechanical mechanisms** that implement physics behavior in the graph runtime. It is a code-accurate view of what actually executes: energy sources, propagation, decay, pressure, flips, and moment lifecycle.

Mechanisms are listed with explicit function references so they can be traced in code and validated against invariants.

---

## DATA STRUCTURES

### `TickResult` (engine/physics/tick.py)

```
flips: List[Dict[str, Any]]      # Flips detected from tensions
energy_total: float              # Sum of narrative energies
avg_pressure: float              # Mean tension pressure
decay_rate_used: float           # Current decay_rate after criticality adjustment
narratives_updated: int          # Count of narratives updated
tensions_updated: int            # Count of tensions updated
moments_decayed: int             # Count of moments decayed this tick
```

### `narrative_energies` (local dict in GraphTick)

```
Dict[narrative_id: str, energy: float]
```

### `tension` record (GraphQueries results)

```
id: str
pressure: float
pressure_type: str               # gradual | hybrid | other
base_rate: float                 # pressure accumulation rate
breaking_point: float            # flip threshold
narratives: List[str]            # narrative ids contributing
```

### `moment` lifecycle fields (Moment schema)

```
status: possible | active | spoken | dormant | decayed
weight: float                    # 0.0-1.0
tick_spoken: int
tick_decayed: int
```

---

## ALGORITHM: Mechanisms by Function

### M1: Character Energy Source

**Function:** `GraphTick._compute_character_energies()`  
**Inputs:** `player_id`, `player_location`  
**Logic:**  
- Intensity from narratives about a character via `_compute_relationship_intensity()`  
- Proximity to player via `_compute_proximity()`  
**Output:** `char_energies: Dict[char_id, float]`

### M2: Belief-Weighted Energy Injection Into Narratives

**Function:** `GraphTick._flow_energy_to_narratives()`  
**Inputs:** `char_energies`, beliefs from `GraphQueries.get_character_beliefs()`  
**Logic:**  
```
energy_flow = char_energy * (belief_strength / total_strength) * BELIEF_FLOW_RATE
```
**Output:** `narrative_energies` with accumulated energy

### M3: Narrative Propagation via RELATES_TO Links

**Function:** `GraphTick._propagate_energy()`  
**Inputs:** `narrative_energies`, links from `_get_narrative_links()`  
**Logic:**  
- For each hop up to `MAX_PROPAGATION_HOPS`  
- Apply `LINK_FACTORS` per relation type  
- Apply extra drain for `supersedes`  
**Output:** Updated `narrative_energies`

### M4: Energy Decay (Type + Focus Weighted)

**Function:** `GraphTick._decay_energy()`  
**Inputs:** `narrative_energies`, narrative type + focus  
**Logic:**  
```
effective_decay = decay_rate * decay_mult * focus_mult
new_energy = max(MIN_WEIGHT, energy * (1 - effective_decay))
```
**Output:** Decayed `narrative_energies`

### M5: Narrative Weight Update (Canon Write)

**Function:** `GraphTick._update_narrative_weights()`  
**Inputs:** `narrative_energies`  
**Logic:** Clamp to `[MIN_WEIGHT, 1.0]` and write `n.weight`  
**Output:** Count of narratives updated

### M6: Criticality Thermostat

**Function:** `GraphTick._adjust_criticality()`  
**Inputs:** tensions from `GraphQueries.get_all_tensions()`  
**Logic:** Adjust `self.decay_rate` based on `avg_pressure` and `max_pressure`  
**Output:** Updated `self.decay_rate`

### M7: Tension Pressure Accumulation

**Function:** `GraphTick._tick_pressures()`  
**Inputs:** elapsed_minutes, tension list, narrative weights + focus  
**Logic:**  
```
increase = elapsed_minutes * base_rate * avg_focus * max_weight
new_pressure = min(1.0, current_pressure + increase)
```
**Output:** Tension list with updated pressures, plus writes to graph

### M8: Flip Detection (Breaking Point)

**Function:** `GraphTick._detect_flips()`  
**Inputs:** tensions with `pressure` and `breaking_point`  
**Logic:** `pressure >= breaking_point` ⇒ flip record  
**Output:** List of flips (no direct moment writes)

### M9: Moment Lifecycle Decay (Per Tick)

**Function:** `GraphTick._process_moment_tick()` → `GraphOps.decay_moments()`  
**Inputs:** elapsed_minutes  
**Logic:**  
- Iterate per 5 minutes  
- Multiply weight by `decay_rate`  
- If `weight < decay_threshold` ⇒ mark `decayed`  
**Output:** counts of updated + decayed moments

### M10: Read-Side Energy Injection (Observation Effect)

**Function:** `GraphQueries._inject_energy_for_node()`  
**Triggered by:** `MomentQueryMixin._maybe_inject_energy()`  
**Logic:** increment `n.energy` on read (`ENERGY_BOOST_PER_READ`)  
**Output:** Side-effect on node energy

### M11: Instant Traversal (Hot Path)

**Function:** `MomentTraversal.handle_click()`  
**Inputs:** moment_id, clicked word, tick  
**Logic:**  
- find target via `MomentQueries.find_click_targets()`  
- apply `weight_transfer`  
- set statuses + create `THEN` link  
**Output:** immediate traversal result

### M12: Surfacing + Decay (Batch Surface)

**Function:** `MomentSurface.check_for_flips()`, `MomentSurface.apply_decay()`  
**Inputs:** `ACTIVATION_THRESHOLD`, `DECAY_RATE`, `DECAY_THRESHOLD`  
**Logic:**  
- flip possible → active if weight >= threshold  
- decay weights and mark decayed below threshold  
**Output:** counts and flipped moments

---

## KEY DECISIONS

### D1: Tick Gating (Performance)

```
IF elapsed_minutes < MIN_TICK_MINUTES:
    skip tick entirely
ELSE:
    run full GraphTick
```

### D2: Pressure Accumulation Type

```
IF pressure_type in ['gradual', 'hybrid']:
    increase pressure
ELSE:
    keep pressure static
```

### D3: Flip Threshold

```
IF pressure >= breaking_point:
    emit flip record
ELSE:
    no flip
```

---

## DATA FLOW

```
Character energies
    ↓
Belief-weighted narrative flow
    ↓
Narrative propagation (RELATES_TO)
    ↓
Narrative decay + weight write
    ↓
Tension pressure tick
    ↓
Flip detection
    ↓
Orchestrator handlers (external)
```

Moment lifecycle decay runs alongside the above during GraphTick.

---

## COMPLEXITY

**Time:**  
O(C + B + N + L + T + M)  
Where C=characters, B=beliefs, N=narratives, L=RELATES_TO links, T=tensions, M=possible moments.

**Space:**  
O(N + T) for energy + pressure caches.

**Bottlenecks:**
- Cypher reads per narrative in `_decay_energy()` and `_tick_pressures()`
- Large moment sets in `decay_moments()` without indexing

---

## HELPER FUNCTIONS

### `_compute_relationship_intensity()`

**Purpose:** Aggregate narrative weights about a character into a base intensity.

**Logic:** Sum weights, clamp to `<= 1.0`.

### `_compute_proximity()`

**Purpose:** Convert travel distance to proximity scalar.

**Logic:** `get_path_between()` → parse distance → `distance_to_proximity()`.

### `_get_narrative_links()`

**Purpose:** Fetch RELATES_TO link strengths for propagation.

**Logic:** Read `contradicts/supports/elaborates/subsumes/supersedes`.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| `engine/physics/graph/graph_queries.py` | `get_all_characters()` | Characters list |
| `engine/physics/graph/graph_queries.py` | `get_character_beliefs()` | Belief weights |
| `engine/physics/graph/graph_queries.py` | `get_narratives_about()` | Narratives about character |
| `engine/physics/graph/graph_queries.py` | `get_path_between()` | Travel distance |
| `engine/physics/graph/graph_queries.py` | `get_all_tensions()` | Tension state |
| `engine/physics/graph/graph_queries.py` | `get_narrative()` | Narrative type/focus |
| `engine/physics/graph/graph_ops_moments.py` | `decay_moments()` | Moment decay writes |
| `engine/moment_graph/queries.py` | `find_click_targets()` | Traversal targets |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Verify whether read-side energy injection is intended as physics or UX.
- [ ] Clarify ownership between `MomentTraversal.handle_click()` and `GraphOps.handle_click()` to avoid double paths.
- IDEA: Batch narrative reads in `_decay_energy()` to reduce query count.
- QUESTION: Should tension pressure also consider narrative energy, not only weight?
