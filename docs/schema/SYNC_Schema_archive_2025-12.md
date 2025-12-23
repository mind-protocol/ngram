# Archived: SYNC_Schema.md

Archived on: 2025-12-23
Original file: SYNC_Schema.md

---

## MATURITY

**STATUS: CANONICAL v1.2**

What's canonical:
- 5 node types: actor, space, thing, narrative, moment
- 9 link types:
  - Energy carriers: `expresses`, `about`, `relates`, `attached_to`
  - Structural: `contains`, `leads_to`, `sequence`, `primes`, `can_become`
- Link physics: conductivity, weight, energy, strength, emotions
- Semantic properties: name, role, direction (replaces old type differentiation)
- Unified flow formula: `flow = source.energy × rate × conductivity × weight × emotion_factor`
- Link cooling: 30% drain + 10% strength conversion (NO DECAY)
- Hot/cold filtering via heat_score
- Schema loading with project overlay
- Health check CLI and pytest suite

What's in progress:
- World runner integration
- Canon holder validation functions

What's proposed (v2):
- Full V2/V3/V7 coverage in check_health.py
- Schema versioning in nodes
- Auto-fix capabilities

---


## v1.2 CHANGES SUMMARY

### Link Types (7 → 9)

| Type | Category | From → To | Phase |
|------|----------|-----------|-------|
| `expresses` | Energy | Actor → Moment | Draw |
| `about` | Energy | Moment → Any | Flow |
| `relates` | Energy | Any → Any | Flow, Backflow |
| `attached_to` | Energy | Thing → Actor/Space | Flow |
| `contains` | Structural | Space → Actor/Thing/Space | — |
| `leads_to` | Structural | Space → Space | — |
| `sequence` | Structural | Moment → Moment | — |
| `primes` | Structural | Moment → Moment | — |
| `can_become` | Structural | Thing → Thing | — |

### Semantic Properties (NEW)

Instead of 14+ link types, use 9 types + semantic properties (`name`, `role`, `direction`):

```yaml
# Old: Actor -[BELIEVES]-> Narrative
# New:
relates:
  node_a: actor_aldric
  node_b: narrative_oath
  name: believes
  role: believer            # originator, believer, witness, subject, creditor, debtor

# Old: Actor -[OWES]-> Actor
# New:
relates:
  node_a: actor_aldric
  node_b: actor_baron
  name: owes debt to
  role: debtor

# Old: Narrative -[SUPPORTS]-> Narrative
# New:
relates:
  node_a: narrative_loyalty
  node_b: narrative_oath
  direction: support        # support, oppose, elaborate, subsume, supersede
  emotions: [[alignment, 0.8]]
```

### Physics Changes (NO DECAY)

| v1.1 | v1.2 |
|------|------|
| Decay 40%/tick | **NO DECAY** — link cooling |
| All links processed | Hot links only (top-N filter) |
| — | heat_score = energy × weight |
| — | Link drain: 30% to nodes |
| — | Strength growth: 10% converts |

### Migration from Legacy Types

```
BELIEVES       → relates (role: believer)
ORIGINATED     → relates (role: originator, higher weight)
SUPPORTS       → relates (direction: support, emotions: [[alignment, X]])
CONTRADICTS    → relates (direction: oppose, emotions: [[opposition, X]])
ELABORATES     → relates (direction: elaborate)
CAN_SPEAK/SAID → expresses
AT             → contains (INVERTED: space contains actor)
CARRIES        → attached_to (INVERTED: thing attached_to actor)
ATTACHED_TO    → about (for Moment → Any)
THEN           → sequence
CAN_LEAD_TO    → primes
```

---


## v1.1 CHANGES SUMMARY

### Node Fields

| Field | v1.0 | v1.1 | Why |
|-------|------|------|-----|
| weight | 0-1 | 0-∞ | Importance needs range (protagonist 10x villager) |
| energy | 0-1 | 0-∞ | Accumulates from moments, decay prevents explosion |

Weight does double duty: importance (ranking) + inertia (physics stability).

### Link Fields

| Field | v1.0 | v1.1 | Why |
|-------|------|------|-----|
| from_id/to_id | string | RENAMED | → node_a/node_b (bidirectional clarity) |
| conductivity | — | 0-1 | NEW. Percentage of energy that passes through |
| weight | 0-1 | 0-∞ | Link importance (used in flow formula) |
| energy | 0-1 | 0-∞ | Current attention (decays 40%/tick) |
| strength | 0-1 | 0-∞ | Accumulated depth (decays slower) |
| polarity | -1 to +1 | REMOVED | Replaced by emotions list |
| emotions | — | List | NEW. [[name, intensity], ...] — single list |

### Link Type Collapse (10 → 7)

| Old | New | Why |
|-----|-----|-----|
| at | REMOVED | Same as `contains` reversed |
| said | **expresses** | Abstracts to thought/action/question |
| then | **sequence** | Clearer naming |
| can_lead_to | **can_become** | Clearer naming |
| attached_to | REMOVED | Use `relates` |
| about | REMOVED | Use `relates` |

**Taxonomy:**
- Organizational: contains, leads_to, expresses
- Chronological: sequence, primes, can_become
- Semantic: relates

### Emotion Model

```yaml
# All links have emotions (unified list, colored by energy flow)
link:
  emotions: [["fear", 0.7], ["respect", 0.4]]  # Hebbian: colored by what flows through
  conductivity: 0.7                             # percentage of energy flow
  weight: 1.0                                   # link importance
  energy: 0.5                                   # current attention (decays 40%/tick)
  strength: 2.3                                 # accumulated depth
```

**Hebbian coloring:** When energy flows through a link, the link's emotions blend with the flowing moment's emotions. Links "learn" what passes through them.

---


## ESCALATIONS

<!-- @ngram:escalation
title: "DECAY_RATE: What's the right global decay rate?"
priority: 5
response:
  status: resolved
  choice: "Split decay rates"
  behavior: "Link energy: 40%/tick (attention fades fast). Node energy: BASE_NODE_DECAY (0.1) × 1/(1+weight). High-weight nodes decay slower."
  notes: "2025-12-23: Specified in Schema v1.1. Decided by Nicolas."
-->

<!-- @ngram:escalation
title: "INERTIA_FORMULA: How does node weight affect energy change?"
priority: 5
response:
  status: resolved
  choice: "Weight in unified formula"
  behavior: "flow = source.energy × rate × conductivity × link.weight × emotion_factor. Weight affects flow rate directly. Decay uses 1/(1+weight) for inertia."
  notes: "2025-12-23: Specified in Schema v1.1. No separate inertia field. Decided by Nicolas."
-->


## TODOS

### Immediate

@ngram:todo — **DB_MIGRATION_V1.1:** Write and run migration for link field changes
- Rename from_id→node_a, to_id→node_b
- Add energy, strength fields to links (default 0)
- Remove polarity, add emotions list

### Physics Implementation (See SYNC_Project_State.md for full TODO)

@ngram:todo — **UNIFIED_FLOW:** Implement `flow = source.energy × rate × conductivity × weight × emotion_factor`
@ngram:todo — **HEBBIAN_COLORING:** Implement link emotion blending from energy flow
@ngram:todo — **PATH_RESISTANCE:** Implement Dijkstra with conductivity-based resistance
@ngram:todo — **LINK_CRYSTALLIZATION:** Create relates links from shared moments
@ngram:todo — **MOMENT_LIFECYCLE:** Implement possible→active→completed state machine

### Coverage

- [ ] **IMPL_V7_ENDPOINTS:** Add `validate_link_endpoints()` to check_health.py
- [ ] **NGRAM_DOCTOR_INTEGRATION:** Integrate check_health.py into ngram doctor

### Lower Priority

- [ ] **SPLIT_TEST_SCHEMA:** test_schema.py exceeds size threshold
- [ ] **E2_E3_TESTS:** Test missing schema / malformed YAML

---

