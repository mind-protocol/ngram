# World Runner — Health: Verification Checklist

```
STATUS: DESIGNING
CREATED: 2025-12-20
UPDATED: 2025-12-21
```

---

## PURPOSE OF THIS FILE

This document translates the World Runner service's failure modes into traceable health signals so that every long action remains narratively faithful without manual spelunking.
It keeps the agent CLI, GraphOps mutations, and narrated injections under explicit scrutiny even while the runner operates off-screen.

What it protects:
- **Off-screen continuity**: Every tension resolution must feel like a seamless extension of the canonical graph.
- **CLI resiliency**: Timeouts, parse errors, and binary failures must degrade gently rather than freezing the playthrough.
- **Graph mutation fidelity**: Background mutations must stay schema-compliant and never corrupt downstream narrations.

---

## WHY THIS PATTERN

The HEALTH template sits beside the TEST and VALIDATION docs so we can monitor behaviour without altering the runtime operator.
World Runner is a high-risk flow because it invokes an agent CLI, then immediately mutates shared graph state; the health doc names its docks, indicators, and status so downstream agents know how to verify it without re-reading the implementation.
Keeping this doc canonical guards against regressions where off-screen ticks stop producing reliable injections or where CLI failures become silent state gaps.

---

## HOW TO USE THIS TEMPLATE

- Start by reading the FLOWS ANALYSIS section so you understand which events the runner is supposed to process.
- Pick one of the health indicators to focus on; follow its VALUE TO CLIENTS section to link back to `VALIDATION_World_Runner_Invariants.md` before making changes.
- Use the DOCK TYPES list whenever you need to find the code locations that feed or consume the indicator.
- After you proof your change, rerun the HOW TO RUN checklist and update the STATUS snapshot so the doctor can trace the fix.

---

## CHAIN

```
PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
HEALTH:          ./HEALTH_World_Runner.md
SYNC:            ./SYNC_World_Runner.md
```

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: world_evolution
    purpose: Advance background story beats while the player executes long actions.
    triggers:
      - type: event
        source: orchestrator.flip_detector
        notes: Fires whenever tension flips accumulate during a travel or downtime action.
    frequency:
      expected_rate: 0.5/min
      peak_rate: 5/min (travel bursts)
      burst_behavior: Clipped by the 10m agent CLI timeout and the narrators waiting on injection_queue.
    risks:
      - Agent output narrates facts that contradict the canonical graph.
      - CLI failure leaves GraphOps mutations unapplied and world_injection empty.
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: background_consistency
    flow_id: world_evolution
    priority: high
    rationale: Ensures every runner output maintains the lore already captured in the graph.
  - name: adapter_resilience
    flow_id: world_evolution
    priority: high
    rationale: Keeps fallback paths and logging visible so CLI regressions do not freeze the playthrough.
```

---

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Translate off-screen tension flips into graph mutations and world injections that read as intentional continuations of existing lore. | background_consistency | This objective pairs with the canonical schema checks so downstream agents can prove the lore never drifts when Narrator resumes, keeping every long action faithful. |
| Surface CLI, parsing, and mutation failures before they leave the runner so the Narrator never receives stale or missing injections. | adapter_resilience | By naming these indicators, the doctor can point at the exact log/error signal that needs fixing when a background action freezes the playthrough. |

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: logs
  result:
    representation: enum
    value: OK
    updated_at: 2025-12-21T12:00:00Z
    source: manual_inspection
    confidence: high
```

---

## DOCK TYPES (COMPLETE LIST)

- `agent_prompt`: The structured prompt constructed inside `_build_prompt()` that bundles tension metadata, player state, and time span so every check knows what story moment is being resolved.
- `graph_mutations`: The payload passed to `GraphOps.apply()` after the runner receives agent mutations; this dock proves we never leave inconsistent edges in the graph.
- `world_injection`: The injection saved for the narrator queue after the runner completes or is interrupted; it must always exist when the player waits for a follow-up scene.

---

## CHECKER INDEX

```yaml
checkers:
  - name: fallback_validator
    purpose: Confirm `_fallback_response()` matches the minimal schema after any CLI failure.
    status: active
    priority: high
  - name: mutation_safety_checker
    purpose: Confirm every `graph_mutations` payload contains only schema-safe edges and nodes.
    status: designing
    priority: high
  - name: context_consistency_checker
    purpose: Replay `GraphQueries` context reads to ensure flipped tensions still exist before passing them into the prompt.
    status: designing
    priority: medium
```

---

## INDICATOR: background_consistency

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: background_consistency
  client_value: Keeps the lore steady while time skips ahead without the player watching.
  validation:
    - validation_id: V1 (Runner)
      criteria: _call_claude() always returns the expected dictionary shape that Narrator can parse.
    - validation_id: V2 (Runner)
      criteria: Runner invocations do not depend on stored state and always include the latest GraphQueries context.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: run_context
    method: engine.infrastructure.orchestration.world_runner.WorldRunnerService.process_flips
    location: engine/infrastructure/orchestration/world_runner.py:34-90
  output:
    id: world_injection
    method: engine.infrastructure.orchestration.world_runner.WorldRunnerService.process_flips
    location: engine/infrastructure/orchestration/world_runner.py:34-140
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed:
    - float_0_1
  selected:
    - float_0_1
semantics:
  float_0_1: Ratio of background runs that produced schema-compliant injections in the latest monitoring window.
  aggregation:
    method: Minimum-of-weighted-indicators so a single inconsistent injection degrades the score.
    display: Report through `ngram doctor` and the world runner health banner.
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Replay the prompt and GraphOps context to ensure the returned injection references existing facts, then compare the response shape to the validation schema.
  steps:
    - Capture the context (flips, player_state, graph_metadata) used in the original call.
    - Re-run GraphOps reads or rely on recorded query results to ensure the facts still exist.
    - Feed the stored agent output into schema checks before the Narrator consumes it.
  data_required: Flips list, player context, GraphQueries responses, mutation payload, saved `world_injection`.
  failure_mode: The agent invents contradictory lore or emits incomplete injections, so the Narrator rejects the payload and the player experiences a blank scene.
```

---

## INDICATOR: adapter_resilience

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: adapter_resilience
  client_value: Keeps the runner service alive whenever the agent CLI misbehaves, preventing freezes during long actions.
  validation:
    - validation_id: V3 (Runner)
      criteria: `_fallback_response()` always returns a safe structure after timeouts, parse errors, or CLI absence.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: claude_invocation
    method: engine.infrastructure.orchestration.world_runner.WorldRunnerService._call_claude
    location: engine/infrastructure/orchestration/world_runner.py:84-130
  output:
    id: fallback_payload
    method: engine.infrastructure.orchestration.world_runner.WorldRunnerService._fallback_response
    location: engine/infrastructure/orchestration/world_runner.py:134-180
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed:
    - enum
  selected:
    - enum
semantics:
  enum: OK / DEGRADED / FAILED as logged after each CLI invocation.
  aggregation:
    method: Reduce to the most recent severity so one CLI failure drives immediate attention.
    display: Surface under the world runner health banner and the doctor log for fast triage.
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Inspect agent CLI exit codes, timeouts, and parse exceptions, then ensure `_fallback_response()` logs the failure and leaves graph_mutations empty before returning.
  steps:
    - Trigger `_call_claude()` with a mocked failure (timeout, invalid JSON, missing binary).
    - Confirm `_fallback_response()` seeds `world_injection` with a safe placeholder and avoids applying mutations.
    - Log the failure to the health banner and mark the indicator as DEGRADED if any fallback path executed.
  data_required: CLI exit code, stdout/stderr capture, raised exception, and the returned fallback dict.
  failure_mode: CLI errors are swallowed, leaving the graph half-staged and the Narrator waiting for a missing injection.
```

---

## HOW TO RUN

1. Follow the manual checklist listed in `docs/agents/world-runner/VALIDATION_World_Runner_Invariants.md` to exercise V1–V3 and the associated error conditions.
2. Re-run the world runner-specific checks described above in your dev environment and capture the status snapshot in the STATUS section.
3. Run the protocol validator so the chain knows this HEALTH doc is compliant.

```bash
ngram validate
```

---

## KNOWN GAPS

- No automated regression harness covers CLI failure injection or timeout handling yet.
- GraphQueries context replays are not instrumented; the runner can query stale narratives if the graph evolves between checks.
- There is no schema validator for `world_injection` once GraphOps writes the mutations, so downstream Narrator errors go unnoticed.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Build an integration script that exercises `WorldRunnerService.process_flips()` from `engine.infrastructure.orchestration.orchestrator` with mocked GraphQueries so the health indicators can run in CI.
- [ ] Emit the `background_consistency` score into the `ngram doctor` log so the failure surface is easier to find during deployment.
- [ ] Add a focused telemetry stream that correlates `adapter_resilience` degradations with the failing CLI stdout/stderr for faster root cause analysis.
- QUESTION: Should the health indicator include a timeline of GraphOps mutations so we can audit exactly which edges were added or removed during long actions?
