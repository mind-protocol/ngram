# Schema — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2025-12-23
```

---

## PURPOSE OF THIS FILE

This HEALTH file covers schema validation mechanics — how we verify that graphs comply with schema constraints at runtime.

**Why it exists:** Schema drift happens. Nodes get created with missing fields, invalid enums, orphan links. Without health checks, these issues accumulate silently until something breaks. Health checks catch violations early.

**Boundaries:**
- DOES verify: Schema compliance (required fields, enum values, link structure)
- DOES NOT verify: Business logic, game rules, narrative consistency
- DOES NOT verify: Pydantic model alignment (that's a separate concern)

---

## WHY THIS PATTERN

HEALTH is separate from tests because:
- Tests run in CI, health checks run against live graphs
- Tests use fixtures, health checks use real data
- Tests are pass/fail, health reports have severity levels

Docking-based checks are the right tradeoff because:
- We read from graph without modifying
- We can run at any time without side effects
- We generate actionable reports

Throttling protects performance:
- Large graphs can have thousands of nodes
- Query batching prevents timeout
- Report truncation prevents output explosion

---

## HOW TO USE THIS TEMPLATE

1. Read VALIDATION_Schema.md for invariants we're checking
2. Read IMPLEMENTATION_Schema.md for code locations
3. Each indicator below maps to one or more VALIDATION criteria
4. Run manually or via ngram doctor

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Schema.md
PATTERNS:       ./PATTERNS_Schema.md
BEHAVIORS:      ./BEHAVIORS_Schema.md
ALGORITHM:      ./ALGORITHM_Schema.md
VALIDATION:     ./VALIDATION_Schema.md
IMPLEMENTATION: ./IMPLEMENTATION_Schema.md
THIS:           HEALTH_Schema.md (you are here)
SYNC:           ./SYNC_Schema.md

IMPL:           engine/graph/health/check_health.py
                engine/graph/health/test_schema.py
```

> **Contract:** HEALTH checks verify input/output against VALIDATION with minimal or no code changes. After changes: update IMPL or add TODO to SYNC.

---

## FLOWS ANALYSIS

```yaml
flows_analysis:
  - flow_id: graph_validation
    purpose: Catch schema violations before they cause runtime errors
    triggers:
      - type: manual
        source: python check_health.py
        notes: Developer runs when debugging
      - type: schedule
        source: ngram doctor
        notes: Part of overall health check
    frequency:
      expected_rate: 1/day
      peak_rate: 10/day during active development
      burst_behavior: Each run independent, no queuing
    risks:
      - V6 violation: Missing required fields
      - V2 violation: Out-of-range physics values
    notes: Connects to FalkorDB, requires running instance
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: schema_compliance
    flow_id: graph_validation
    priority: high
    rationale: Schema violations cause runtime errors in physics/narrator

  - name: required_fields_present
    flow_id: graph_validation
    priority: high
    rationale: Missing id/name breaks lookups and display

  - name: enum_values_valid
    flow_id: graph_validation
    priority: med
    rationale: Invalid enums may cause display issues but often recoverable

  - name: link_structure_valid
    flow_id: graph_validation
    priority: high
    rationale: Invalid link endpoints break traversal
```

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Physics-ready structure | schema_compliance, required_fields_present | Physics needs valid weight/energy values |
| Project-agnostic foundation | link_structure_valid | Link constraints are universal |
| Minimal surface area | required_fields_present | Only essential fields checked |

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: stdout (CLI output)
  result:
    representation: enum
    value: HEALTHY | UNHEALTHY
    updated_at: per-run
    source: check_health.py HealthReport.is_healthy
```

---

## CHECKER INDEX

```yaml
checkers:
  - name: check_health_cli
    purpose: Full graph schema validation via CLI
    status: active
    priority: high

  - name: test_schema_pytest
    purpose: Schema validation test suite
    status: active
    priority: high

  - name: ngram_doctor_integration
    purpose: Schema check as part of ngram doctor
    status: pending
    priority: med
```

---

## INDICATOR: Schema Compliance

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: schema_compliance
  client_value: Prevents runtime errors from malformed graph data
  validation:
    - validation_id: V1
      criteria: All link endpoints must exist
    - validation_id: V6
      criteria: Required fields (id, name, node_type, type) present
```

### HEALTH REPRESENTATION

```yaml
representation:
  selected:
    - enum
    - float_0_1
  semantics:
    enum: HEALTHY (0 errors), UNHEALTHY (1+ errors)
    float_0_1: (total_nodes - error_nodes) / total_nodes
  aggregation:
    method: Any error → UNHEALTHY
    display: enum for CLI, float for dashboards
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: dock_graph_connection
    method: db.graph_ops.GraphOps._query
    location: engine/graph/health/check_health.py:272
  output:
    id: dock_validation_result
    method: HealthReport.to_dict
    location: engine/graph/health/check_health.py:79
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Query all nodes by type, check each against schema, accumulate issues
  steps:
    - Load merged schema (base + project)
    - For each node type, query all nodes
    - For each node, check required fields
    - For each node, check enum values
    - Generate HealthReport with all issues
  data_required: Graph connection, schema files
  failure_mode: Non-empty issues list with severity=error
```

### INDICATOR

```yaml
indicator:
  error:
    - name: missing_required_field
      linked_validation: [V6]
      meaning: Node lacks id, name, or type
      default_action: alert
    - name: orphan_link
      linked_validation: [V1]
      meaning: Link references non-existent node
      default_action: alert
  warning:
    - name: invalid_enum_value
      linked_validation: [V6]
      meaning: Enum field has unexpected value
      default_action: log
  info:
    - name: missing_optional_field
      linked_validation: []
      meaning: Optional field not set
      default_action: ignore
```

### THROTTLING STRATEGY

```yaml
throttling:
  trigger: manual or ngram doctor
  max_frequency: 10/hour
  burst_limit: none (stateless)
  backoff: not applicable
```

### FORWARDINGS & DISPLAYS

```yaml
forwarding:
  targets:
    - location: stdout
      transport: CLI output
      notes: Primary interface for developers
    - location: JSON file (optional --json flag)
      transport: file
      notes: Machine-readable for automation
display:
  locations:
    - surface: CLI
      location: check_health.py print_summary()
      signal: HEALTHY/UNHEALTHY with issue counts
      notes: Color-coded, grouped by category
```

### MANUAL RUN

```yaml
manual_run:
  command: python engine/graph/health/check_health.py --graph seed --verbose
  notes: Run when debugging graph issues or after bulk imports
```

---

## HOW TO RUN

```bash
# Run CLI health check
python engine/graph/health/check_health.py --graph seed --verbose

# Run with JSON output
python engine/graph/health/check_health.py --graph seed --json

# Run pytest suite
pytest engine/graph/health/test_schema.py -v

# Run specific test
pytest engine/graph/health/test_schema.py::test_character_required_fields -v
```

---

## KNOWN GAPS

| VALIDATION Criterion | Checker Status | Notes |
|----------------------|----------------|-------|
| V1 Link endpoints | Partial | Structure checked, not all link types |
| V2 Physics ranges | Partial | Defined in schema, not explicitly checked |
| V3 Polarity range | Partial | Only BELIEVES links checked |
| V4 No mutation | By design | Read-only queries |
| V5 No LLM | By design | No LLM imports |
| V6 Required fields | Covered | All node types checked |

<!-- @ngram:todo Add explicit physics range checks (V2) for weight/energy/strength on all nodes/links -->
<!-- @ngram:todo Extend polarity check (V3) to all link types that have polarity field -->
<!-- @ngram:todo Add link type endpoint validation (valid_from/valid_to from schema) -->

---

## MARKERS

<!-- @ngram:todo NGRAM_DOCTOR_INTEGRATION: Integrate check_health.py into ngram doctor command. Currently runs separately. -->

<!-- @ngram:proposition DASHBOARD_INTEGRATION: Expose HealthReport as JSON endpoint for monitoring dashboards. Would enable continuous schema health monitoring. -->

<!-- @ngram:escalation PARTIAL_COVERAGE: V2 and V3 are only partially checked. Should we add explicit checks, or is schema-defined ranges sufficient? Current state works but may miss violations. -->
