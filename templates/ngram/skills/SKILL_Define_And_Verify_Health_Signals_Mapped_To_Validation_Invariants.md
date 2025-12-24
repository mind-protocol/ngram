# Skill: `ngram.health_define_and_verify`
@ngram:id: SKILL.HEALTH.DEFINE_VERIFY.MAP_TO_VALIDATION

## Maps to VIEW
`.ngram/views/VIEW_Health_Define_Health_Checks_And_Verify.md`

---

## Context

Health system in ngram:
- Health indicators = runtime verification that tests can't catch (drift, ratios, production states)
- Docking points = code locations where observation happens (input dock, output dock)
- Mapping = each health indicator links to VALIDATION invariants via `relates` with direction=verifies

Structure:
```
VALIDATION (invariant) ←── relates[verifies] ←── HEALTH (indicator)
                                                      │
                                                      ├── attached_to ──→ input_dock (thing)
                                                      └── attached_to ──→ output_dock (thing)
```

Docking points declared in IMPLEMENTATION docs. Health reads values at those points.

Health stream: `ngram doctor --stream` outputs live signals. Use to verify indicators work.

Priority inheritance: Health indicators inherit priority from the VALIDATION they verify. HIGH validation → HIGH health indicator.

---

## Purpose
Define/extend health signals and verify via real-time health sublayer; map indicators to VALIDATION invariants and declared docking points.

---

## Inputs
```yaml
module: "<area/module>"                    # string
invariants: ["<VALIDATION @ngram:id>"]     # list, invariants to cover
```

## Outputs
```yaml
health_signals:
  - id: "<signal name>"
    maps_to: "<VALIDATION id>"
    input_dock: "<file:symbol>"
    output_dock: "<file:symbol>"
    mechanism: "<how it's checked>"
verification:
  - signal: "<signal name>"
    status: "pass|warn|fail"
    evidence: "<health stream output>"
```

---

## Gates

- Health indicators must map to VALIDATION — no orphan health signals
- Docking points must be declared in IMPLEMENTATION — traceable observation
- Verification required before marking complete — prove it works

---

## Process

### 1. Check prerequisites
```yaml
batch_questions:
  - validations_exist: "Do VALIDATION docs exist for target module?"
  - implementation_exists: "Does IMPLEMENTATION with docking points exist?"
  - existing_health: "What health signals already cover this module?"
```
If VALIDATION missing → run `protocol:add_invariant` first.
If IMPLEMENTATION missing → run `protocol:add_implementation` first.

### 2. Identify gaps
For each VALIDATION invariant, check if health coverage exists.
Prioritize: HIGH priority validations first.

### 3. Define health indicator
```yaml
indicator:
  name: "h_<module>_<what_measured>"
  validates: "<VALIDATION @ngram:id>"
  mechanism: "<specific measurement approach>"
  threshold:
    warning: "<value>"
    error: "<value>"
  input_dock: "<file:symbol where value observed>"
  output_dock: "<file:symbol where result checked>"
```

### 4. Add to HEALTH doc
Update `docs/<area>/<module>/HEALTH_*.md` with new indicator.

### 5. Verify via health stream
Run `ngram doctor --stream` and check indicator fires correctly.
Document evidence of pass/fail.

---

## Protocols Referenced

| Protocol | When | Creates |
|----------|------|---------|
| `protocol:explore_space` | Before defining | Understand existing coverage |
| `protocol:add_invariant` | If validation missing | VALIDATION narrative + ensures links |
| `protocol:add_health_coverage` | To add indicator | health narrative + docks + verifies links |

---

## Evidence
- Docs: `@ngram:id + file + header`
- Code: `file + symbol`

## Markers
- `@ngram:TODO`
- `@ngram:escalation`
- `@ngram:proposition`

## Never-stop
If blocked → `@ngram:escalation` + `@ngram:proposition` → proceed with proposition.
