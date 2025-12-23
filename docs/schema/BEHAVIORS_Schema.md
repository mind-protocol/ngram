# Schema — Behaviors: Observable Effects of Schema Compliance

```
STATUS: STABLE
CREATED: 2025-12-23
VERIFIED: 2025-12-23 against schema.yaml v1.0
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Schema.md
THIS:           BEHAVIORS_Schema.md (you are here)
PATTERNS:       ./PATTERNS_Schema.md
ALGORITHM:      ./ALGORITHM_Schema.md
VALIDATION:     ./VALIDATION_Schema.md
IMPLEMENTATION: ./IMPLEMENTATION_Schema.md
HEALTH:         ./HEALTH_Schema.md
SYNC:           ./SYNC_Schema.md

IMPL:           docs/schema/schema.yaml
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Node Creation Requires Base Fields

```
GIVEN:  Any node being created (actor, space, thing, narrative, moment)
WHEN:   The node is persisted to the graph
THEN:   Node MUST have: id (string), name (string), node_type (enum), type (string)
AND:    Node SHOULD have: weight (float 0-1), energy (float 0-1), created_at_s, updated_at_s
```

### B2: Link Endpoints Must Exist

```
GIVEN:  A link being created with from_id and to_id
WHEN:   The link is persisted
THEN:   Both from_id and to_id MUST reference existing nodes
AND:    Orphan links are rejected
```

### B3: Physics Fields Stay In Range

```
GIVEN:  Any node or link with physics fields
WHEN:   weight, energy, or strength is set
THEN:   Values MUST be in range [0, 1]
AND:    polarity MUST be in range [-1, +1]
```

### B4: Link Type Constrains Endpoints

```
GIVEN:  A link with a specific type (at, contains, leads_to, relates, primes, then, said, can_lead_to, attached_to, about)
WHEN:   The link is created
THEN:   from/to node_types MUST match valid_from/valid_to constraints
AND:    Example: `at` links only from [actor, moment, thing] to [space]
```

### B5: Moment Status Lifecycle

```
GIVEN:  A moment node
WHEN:   Its status field is set
THEN:   Status MUST be one of: possible, active, spoken, decayed
AND:    Status transitions follow: possible → active → spoken → decayed
```

### B6: Project Schema Overlays Base

```
GIVEN:  Base schema in docs/schema/schema.yaml
WHEN:   check_health.py or test_schema.py validates a graph
THEN:   Base schema is loaded first
AND:    Project-specific schema (engine/graph/health/schema.yaml) overlays enum constraints
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Minimal surface area | Required fields are few; optional fields are truly optional |
| B2 | Physics-ready structure | Graph traversal requires valid endpoints |
| B3 | Physics-ready structure | Energy propagation needs bounded values |
| B4 | Project-agnostic foundation | Link constraints keep graph semantically valid |
| B5 | Physics-ready structure | Moment lifecycle enables temporal modeling |
| B6 | Extensible through layering | Projects add constraints without modifying base |

---

## INPUTS / OUTPUTS

### Primary Function: Schema Validation

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| node | dict | Node properties to validate |
| link | dict | Link properties to validate |
| schema | dict | Loaded schema definition |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| issues | List[Issue] | Validation violations found |
| is_healthy | bool | True if no errors |

**Side Effects:**

- None (validation is read-only)

---

## EDGE CASES

### E1: Empty Type String

```
GIVEN:  Node with type="" (empty string)
THEN:   Treated as missing required field → validation error
```

### E2: Unknown Node Type

```
GIVEN:  node_type value not in [actor, space, thing, narrative, moment]
THEN:   Validation error — unknown node type
```

### E3: Null Physics Values

```
GIVEN:  weight or energy is null/None
THEN:   Defaults apply (weight=0.5, energy=0.0)
```

---

## ANTI-BEHAVIORS

### A1: No Game-Specific Fields in Base Schema

```
GIVEN:   Base schema definition
WHEN:    Someone wants to add skills, face, atmosphere, etc.
MUST NOT: Add these to docs/schema/schema.yaml
INSTEAD:  Add to project-specific schema overlay
```

### A2: No LLM in Hot Path

```
GIVEN:   Schema validation running
WHEN:    Validating nodes/links
MUST NOT: Invoke LLM for any validation decision
INSTEAD:  Use deterministic field checks only
```

### A3: No Mutation During Validation

```
GIVEN:   Validation query running
WHEN:    Issues are found
MUST NOT: Auto-fix or mutate the graph
INSTEAD:  Report issues; let user/script decide on fixes
```

---

## MARKERS

<!-- @ngram:todo B4 enforcement is not fully implemented — check_health.py validates structure but doesn't verify all link type constraints (valid_from/valid_to). -->

<!-- @ngram:proposition Consider adding B7: Schema Version Check — validate that schema version in graph matches expected version. Would enable migration detection. -->
