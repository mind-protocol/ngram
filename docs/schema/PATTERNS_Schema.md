# Schema Design Patterns

## Core Philosophy

**Minimal, extensible, project-agnostic.**

The schema defines the graph structure that all ngram projects share. It is NOT a game schema or a dev-tool schema — it's the foundation both inherit from.

## Key Decisions

### 1. Five Node Types (Constrained)

```
node_type: actor | space | thing | narrative | moment
```

These five categories cover all graph entities:
- **actor** — anything that can act (human, agent, NPC, system)
- **space** — containers and locations (folder, module, city, room)
- **thing** — objects that can be referenced/possessed (file, weapon, document)
- **narrative** — stories and knowledge about nodes (pattern, memory, oath)
- **moment** — temporal events (task, input, thought, tick)

### 2. Subtype is Free String

```yaml
type: string  # project-specific, not constrained
```

Each project defines its own subtypes:
- ngram (dev): `agent`, `module`, `file`, `pattern`, `task`
- blood-ledger (game): `companion`, `monastery`, `weapon`, `oath`, `thought`

This keeps the schema lean while allowing project-specific vocabulary.

### 3. Two Physics Fields

```yaml
weight: float [0,1]  # persistent importance
energy: float [0,1]  # instantaneous/computed
```

- **weight** is authored/stored — "how important is this node?"
- **energy** is computed at runtime — "how activated is this node right now?"

All physics mechanisms operate on these two fields.

### 4. Links Have Polarity

```yaml
polarity: float [-1, +1]  # negative = contradict, positive = support
```

This enables the contradiction pressure mechanism — when two narratives contradict, their polarity creates tension that must be resolved.

### 5. Minimal Type-Specific Fields

Most nodes only have base fields. Type-specific additions are rare:
- `thing.uri` — optional locator
- `narrative.content` — the story text
- `moment.text`, `moment.status`, `moment.tick_*` — temporal state

## What's NOT in the Schema

- **Game-specific attributes** (skills, face, voice, atmosphere) — belong in project data
- **Computed fields** (trust, relationship strength) — derived from graph queries
- **UI/rendering hints** — belong in view layer
- **Historical fields** (provenance, version) — use links or separate tracking

## Invariants

See `schema.yaml` invariants section:
- All link endpoints must exist
- weight, energy, strength in [0,1]
- polarity in [-1, +1]
- Queries cannot mutate graph
- Hot path cannot invoke LLM
