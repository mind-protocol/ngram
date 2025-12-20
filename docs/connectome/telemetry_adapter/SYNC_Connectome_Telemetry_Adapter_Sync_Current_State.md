```

# telemetry_adapter — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: RESERVED (V1 DEFERRED)
```

---

## MATURITY

**Canonical (v1 intent):**

* telemetry_adapter is the single ingress for realtime
* SSE frames become envelopes; unknowns preserved as “?”
* connection state and parse errors are visible signals

**Deferred in v1:**

* exact SSE endpoint list and event names
* buffering ownership (adapter vs runtime_engine)
* retention policy for realtime bursts

---

## CURRENT STATE

This module is reserved and documented, but implementation is deferred until:

* the stepper view is stable and trusted
* we confirm backend SSE contracts
* we decide buffering ownership policy

---

## TODO

* [ ] Confirm backend SSE endpoints and event names (moments/tempo/weights/…)
* [ ] Implement EventSource wrapper with connection state and parsing
* [ ] Emit RawTelemetryEnvelope objects to runtime_engine
* [ ] Add health harness with mock SSE generator

Run:

```
pnpm connectome:health telemetry_adapter
```

---

---
