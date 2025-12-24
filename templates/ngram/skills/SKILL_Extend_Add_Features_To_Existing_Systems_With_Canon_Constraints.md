# Skill: `ngram.extend_add_features`
@ngram:id: SKILL.EXTEND.ADD_FEATURES.CANON_CONSTRAINTS

## Maps to VIEW
`.ngram/views/VIEW_Extend_Add_Features_To_Existing.md`

---

## Context

Feature extension in ngram requires canon alignment:
- PATTERNS defines scope — feature must fit within module boundaries
- VALIDATION defines invariants — feature must not violate existing constraints
- BEHAVIORS defines observable effects — new effects need documentation
- HEALTH defines verification — behavior surface changes need updated signals

Canon = authoritative source of truth. When extending, canon constrains:
- Naming: Use terms from PATTERNS/CONCEPT, don't invent new terminology
- Structure: Follow patterns established in IMPLEMENTATION
- Verification: Update HEALTH when behavior surface changes

Regression risk: Extensions can break existing behavior. Check VALIDATION invariants before and after.

---

## Purpose
Extend existing systems with new features while enforcing canon constraints and avoiding regressions.

---

## Inputs
```yaml
module: "<area/module>"            # string
feature: "<what to add>"           # string
```

## Outputs
```yaml
code_changes:
  - "<files modified/added>"
doc_updates:
  - "<docs updated>"
validation_check:
  - invariant: "<VALIDATION id>"
    status: "maintained|updated|new"
```

---

## Gates

- Must align with PATTERNS scope — no out-of-scope features
- Must maintain VALIDATION invariants — no broken constraints
- Must update HEALTH when behavior surface changes — verification stays accurate

---

## Process

### 1. Understand existing system
```yaml
batch_questions:
  - patterns: "What are the module's boundaries and design decisions?"
  - behaviors: "What observable effects exist?"
  - validations: "What invariants must hold?"
  - implementation: "Where does code live, what's the structure?"
```
Read PATTERNS, BEHAVIORS, VALIDATION, IMPLEMENTATION before coding.

### 2. Verify feature fits
- Does feature align with PATTERNS scope?
- Will feature violate any VALIDATION invariants?
- If no → proceed. If uncertain → `@ngram:escalation`.

### 3. Implement with canon naming
Use terms from PATTERNS/CONCEPT. Follow structure from IMPLEMENTATION.

### 4. Update doc chain
- BEHAVIORS: Add new observable effects
- VALIDATION: Add new invariants if applicable
- IMPLEMENTATION: Update docking points if new surfaces
- HEALTH: Update signals if behavior surface changed

### 5. Verify no regressions
Run existing tests/health checks. Confirm VALIDATION invariants still hold.

---

## Protocols Referenced

| Protocol | When | Creates |
|----------|------|---------|
| `protocol:explore_space` | Before extending | Understanding of current state |
| `protocol:add_invariant` | If new constraint | VALIDATION narrative |
| `protocol:add_health_coverage` | If behavior surface changed | health indicator + docks |

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
