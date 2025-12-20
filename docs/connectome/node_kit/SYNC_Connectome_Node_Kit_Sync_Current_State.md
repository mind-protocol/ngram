```

# node_kit — Sync: Current State

LAST_UPDATED: 2025-12-20
UPDATED_BY: Marco "Salthand" (agent)
STATUS: DESIGNING
```

---

## MATURITY

**Canonical (v1 intent):**

* typed node variants (Player/UI/Module/GraphQueries/Moment/Agent/TickCron)
* title prominent, file path discreet
* energy badge with deterministic bucket mapping
* internal step list with singular active highlight
* separate LLM CLI Agent nodes (Narrator, World Builder)

**In design:**

* flipped node signal source
* energy scale assumptions (0..1 vs unbounded)

---

## CURRENT STATE

Docs exist; implementation not started.

Immediate priority:

* define styling tokens and component structure
* ensure Player vs UI distinction is explicit
* implement energy glow mapping and step highlight rules

---

## TODO

* [ ] Implement node component variants and shared frame
* [ ] Implement energy bucket mapping and glow tokens
* [ ] Implement wait progress bar and tick cron ring components
* [ ] Define “flipped” signal source or keep as `?` for v1

Run:

```
pnpm connectome:health node_kit
```

---

---
