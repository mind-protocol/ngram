# Physics — Behaviors: What Should Happen

```
STATUS: CANONICAL
UPDATED: 2024-12-18
```

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Physics.md
THIS:           BEHAVIORS_Physics_Overview.md (you are here)
ALGORITHMS:
  - ../ALGORITHM_Physics.md      (Consolidated: energy, tick, canon, handlers, input, actions, QA, speed)
SCHEMA:         ../../schema/SCHEMA_Moments.md
API:            ../API_Physics.md
VALIDATION:     ../VALIDATION_Physics.md
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## Overview

Observable behaviors of the moment graph system:

| Behavior | What You See |
|----------|--------------|
| B1 | Instant display, eventual depth |
| B2 | Conversations are multi-participant |
| B3 | Characters think unprompted |
| B4 | Silence is an answer |
| B5 | Names have power |
| B6 | History is traversable |
| B7 | Actions have consequences |
| B8 | Cascades create drama |
| B9 | Characters have opinions |
| B10 | The world continues elsewhere |
| B11 | The Snap |
| B12 | Journey conversations |

---

## MECHANISMS (Implementation Anchors)

These behaviors are produced by concrete mechanisms listed in:
`docs/physics/algorithms/ALGORITHM_Physics_Mechanisms.md`.

Key anchors:
- Energy pump and propagation (GraphTick: character → narrative → narrative)
- Pressure accumulation + flip detection (GraphTick: tensions)
- Moment lifecycle decay and surfacing (GraphTick + MomentSurface)
- Instant traversal (MomentTraversal hot path)

---

## BEHAVIORS

The physics system exposes the B1–B12 behaviors below; each section describes
what the player observes and the internal energy/graph conditions that make it
repeatable during ticks, flips, and action processing.

---

## B1: Instant Display, Eventual Depth

**What player sees:** Response appears quickly after input.

**What's actually happening:** Pre-existing potentials actualize instantly. New potentials generate in background. Depth emerges over time.

The player never waits for generation. They might wait for the *right* response, but something always happens now.

### Why It Works

```
Player input arrives
  → energy propagates to existing potentials (instant)
  → some cross threshold (instant)
  → those display (instant)
  → meanwhile: handlers generate new potentials (background)
  → new potentials enter graph (when ready)
  → available for next interaction
```

### Pre-Generation Strategy

- Handlers run on flip
- Handlers also run when character enters scene
- Character arrives → handler generates potentials for this context
- By the time player engages, potentials exist

### Fallback

If truly novel input (nothing relevant exists):
- Energy flows → player character receives it
- Player character's handler runs
- "You're not sure anyone knows how to respond to that."

The player character is always the fallback. They always have something.

---

## B2: Conversations Are Multi-Participant

Player asks a question to the room.
Multiple characters may respond.
Responses arrive in weight order.
Conversation emerges from multiple voices, not turn-taking with one NPC.

### How It Works

```
Player: "What should we do about the Normans?"
  → energy flows to all present characters
  → Aldric's "we fight" potential crosses threshold first (weight 0.9)
  → Mildred's "we hide" potential crosses second (weight 0.85)
  → Godwin's "we negotiate" crosses third (weight 0.7)
```

Display shows all three, in weight order. A debate, not a single response.

### Weight Determines Order

Characters with stronger opinions on the topic → higher weight potentials → respond first.
Characters with weak or no opinion → low weight → respond later or not at all.

---

## B3: Characters Think Unprompted

Characters have internal lives.
Their handlers generate thoughts, doubts, desires.
These exist as potentials.
When pressure builds, they surface.

### Example

```
Player is mid-conversation with Mildred.
Aldric's "confession" potential has been gaining weight.
It crosses threshold.
Aldric interrupts: "I need to tell you something."
```

Player didn't trigger it. Pressure did.

### Why It Happens

- Handlers generate potentials even when not directly addressed
- Characters pump energy into narratives they believe
- Narratives transfer energy via links (CONTRADICTS, SUPPORTS, etc.)
- Moment weight derived from attached sources' energy
- Eventually something flips

Characters don't wait to be asked. They have agency.

---

## B4: Silence Is An Answer

Player says something no one can respond to.
Energy flows to present characters.
No relevant potentials exist.
Energy returns to player character.
Player character observes the non-response.

### The Flow

```
Player: "I've decided to become a fish."
  → energy flows to Aldric, Mildred, Godwin
  → none have relevant potentials
  → energy returns to player character
  → player character flips
  → handler generates: "The silence stretches. No one meets your eye."
```

There is no "nothing happens." There is "the silence stretches."

### Why Energy Must Land

See Pattern P5. Energy entering the system always goes somewhere. The player character is the sink of last resort.

---

## B5: Names Have Power

Player types a name → that character receives energy.
Direct address strengthens the link.

### Comparison

| Input | Energy Distribution |
|-------|---------------------|
| "What does everyone think?" | Split across all present |
| "Aldric, what do you think?" | Concentrated on Aldric |

Direct address = REFERENCES link with strong energy transfer.

### Node Recognition

Happens at input time, not query time.
UI assists: "Al" → dropdown "Aldric" → highlighted in text.
Recognized nodes become REFERENCES links.

---

## B6: History Is Traversable

Everything that happens is linked.
THEN links form chains.
Chains can be queryable by:

| Query | Returns |
|-------|---------|
| Character | What did they witness? |
| Place | What happened here? |
| Time | What happened when? |
| Topic | What was said about X? |

No separate log. The graph is the log.

### Example Query

```cypher
MATCH (m:Moment)-[:THEN*]->(end)
WHERE m.tick > 100 AND m.tick < 200
  AND (m)-[:ATTACHED_TO]->(:Character {id: 'char_aldric'})
RETURN m.text, m.tick
ORDER BY m.tick
```

"Show me everything Aldric said or witnessed between tick 100 and 200."

---
