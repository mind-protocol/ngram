# Physics — Algorithm: Energy Mechanics And Link Semantics

```
CREATED: 2024-12-18
UPDATED: 2025-12-20
STATUS: Canonical
```

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Physics.md
BEHAVIORS:      ../BEHAVIORS_Physics.md
THIS:           ALGORITHM_Physics_Energy_Mechanics_And_Link_Semantics.md (you are here)
SCHEMA:         ../../schema/SCHEMA_Moments.md
VALIDATION:     ../VALIDATION_Physics.md
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## Energy Mechanics

### Core Principles

**1. Links don't create energy. They route it.**

Energy conservation within the narrative layer. Characters are external pumps. Decay and actualization are sinks.

**2. Strength is authored initially, evolved structurally.**

Narrator sets initial link strength. Events modify it. Time decays it. No magic numbers — earned through play.

**3. Energy IS proximity.**

We don't compute "proximity" as a separate concept. Energy levels encode relevance. High energy = close to attention. Low energy = far from attention. Physics handles it.

**4. Physical gating is link attributes, not functions.**

`presence_required: bool` on ATTACHED_TO links. `AT` links for character location. Graph queries, not code.

---

## NODE TYPES

All nodes that participate in the energy economy have both:
- **Weight**: Importance over time (slow, event-driven)
- **Energy**: Current activation (fast, flow-driven)

| Node | Weight | Energy | Notes |
|------|--------|--------|-------|
| **Character** | Yes | Yes | Batteries — pump energy out |
| **Narrative** | Yes | Yes | Circuits — route energy between |
| **Moment** | Yes | Yes | Spend energy on actualization |
| **Place** | No | No | Container only |
| **Thing** | No | No | Focal point only (via ABOUT links) |

### Weight vs Energy

| Property | Weight | Energy |
|----------|--------|--------|
| **What** | Importance over time | Current activation |
| **Timescale** | Slow (hours/days) | Fast (ticks/seconds) |
| **Changes by** | Events, reinforcement, decay | Flow, injection, spending |
| **Range** | 0.01 - 1.0 | 0.01 - 10.0 (chars) / 5.0 (narr/moment) |
| **Analogy** | Long-term memory strength | Working memory activation |

### Why Both Matter

| State | Meaning |
|-------|---------|
| High weight, low energy | Important but dormant — "the oath exists but no one's thinking about it" |
| Low weight, high energy | Active but trivial — "we're discussing lunch" |
| High weight, high energy | Important AND active — "the betrayal surfaces NOW" |
| Low weight, low energy | Forgotten — will decay away |

### Surfacing / Relevance

```python
def salience(node):
    """How much should this surface right now?"""
    return node.weight * node.energy
```

High salience = surfaces, dominates attention, triggers events.

### Character Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `weight` | float | Importance to story (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 10.0) |
| `state` | enum | `awake`, `sleeping`, `unconscious`, `dead` |

### Narrative Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `type` | enum | `fact`, `belief`, `oath`, `debt`, `secret`, `rumor`, `relationship` |
| `weight` | float | Importance to story (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 5.0) |
| `visibility` | enum | `public`, `secret`, `known_to_few` |
| `deadline` | datetime? | For debts, oaths with time pressure |
| `conditions` | string[]? | For oaths — when does it activate? |

### Moment Attributes

| Attribute | Type | Notes |
|-----------|------|-------|
| `id` | string | Unique identifier |
| `text` | string | The content |
| `type` | enum | `narration`, `dialogue`, `action`, `thought`, `description` |
| `status` | enum | `possible`, `active`, `spoken`, `dormant`, `decayed` |
| `weight` | float | Importance over time (0.01 - 1.0) |
| `energy` | float | Current activation (0.01 - 5.0) |
| `tone` | string? | `bitter`, `hopeful`, `urgent`, etc. |
| `tick_created` | int | When created |
| `tick_spoken` | int? | When actualized |

---

## LINK TYPES

### Character Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **BELIEVES** | Char → Narr | Char pumps into Narr | Core relationship |
| **ORIGINATED** | Char → Narr | Char pumps harder (*1.5) | Authorship |
| **AT** | Char → Place | NO flow | Spatial |
| **CARRIES** | Char → Thing | NO flow | Possession |

### Narrative Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **ABOUT** | Narr → Char/Place/Thing | Reverse: subject pulls | Focal point |
| **CONTRADICTS** | Narr ↔ Narr | Bidirectional exchange | Conflict |
| **SUPPORTS** | Narr ↔ Narr | Equilibrating | Alliance |
| **ELABORATES** | Narr → Narr | Parent → child | Detail |
| **SUBSUMES** | Narr → Narr | Specific → general | Aggregation |
| **SUPERSEDES** | Narr → Narr | Draining (old → new) | Replacement |

### Moment Links

| Link | From → To | Energy Flow | Purpose |
|------|-----------|-------------|---------|
| **CAN_SPEAK** | Char → Moment | Char energy → weight | Who speaks |
| **ATTACHED_TO** | Moment → Any | Target energy → weight | Relevance |
| **CAN_LEAD_TO** | Moment → Moment | On traversal | Conversation |
| **THEN** | Moment → Moment | NO (historical) | Canon chain |

### Link Properties

| Link | Properties |
|------|------------|
| **BELIEVES** | `strength: float`, `role: str?` (creditor/debtor/witness/etc) |
| **ORIGINATED** | `strength: float` |
| **ABOUT** | `strength: float`, `role: str?` (subject/location/object) |
| **CONTRADICTS** | `strength: float` |
| **SUPPORTS** | `strength: float` |
| **ELABORATES** | `strength: float` |
| **SUBSUMES** | `strength: float` |
| **SUPERSEDES** | `strength: float` |
| **CAN_SPEAK** | `strength: float` |
| **ATTACHED_TO** | `strength: float`, `presence_required: bool` |
| **CAN_LEAD_TO** | `strength: float`, `require_words: str[]`, `trigger: enum` |

---

## NARRATIVE TYPES

Semantic meaning lives in narrative typing, not special link types.

| Narrative Type | Special Fields | Tension Pattern |
|----------------|----------------|-----------------|
| `fact` | — | — |
| `belief` | — | Contradiction |
| `oath` | `conditions: str[]` | Conditions met |
| `debt` | `amount: float?`, `deadline: datetime?` | Time + proximity |
| `secret` | `visibility: secret` | Knower meets subject |
| `rumor` | `source: char_id?` | Spread pattern |
| `relationship` | `valence: positive/negative` | — |

**Example: Debt as Structure (not special links)**

```yaml
Narrative:
  id: narr_debt_to_merchant
  type: debt
  text: "You owe the merchant 50 silver"
  amount: 50
  deadline: 1067-03-15
```

```
merchant ──[BELIEVES {strength: 0.9, role: creditor}]──> narr_debt_to_merchant
player ──[BELIEVES {strength: 0.6, role: debtor}]──> narr_debt_to_merchant
narr_debt_to_merchant ──[ABOUT]──> merchant
narr_debt_to_merchant ──[ABOUT]──> player
```

Tension detection queries this structure — no special OWES/OWED_BY links needed.

---

## LINK STRENGTH

### Principle

**Strength = authored initially, evolved structurally**

Narrator sets initial value. Six mechanics modify it over time. No magic — earned through play.

### Timescales (No Circularity)

| Property | Changes | Timescale |
|----------|---------|-----------|
| **Energy** | Every tick | Seconds |
| **Weight** | Derived from energy | Seconds |
| **Strength** | On events | Minutes to hours |

Strength is slow. Energy is fast. Strength is effectively constant within a tick cycle.

### Default Initial Strength

| Link | Default | Notes |
|------|---------|-------|
| BELIEVES | 0.5 | Narrator sets based on conviction |
| ORIGINATED | 0.8 | You care about your own stories |
| CONTRADICTS | Computed | Semantic opposition score |
| SUPPORTS | Computed | Semantic similarity score |
| ELABORATES | 0.5 | How central is detail to parent |
| SUBSUMES | 0.5 | How much specific feeds general |
| SUPERSEDES | 0.9 | Replacement is decisive |
| ABOUT | 0.7 | Derived from narrative centrality |

### Base Functions

```python
def reinforce_link(link, amount=0.05):
    """Something confirmed/repeated this connection"""
    link.strength = min(link.strength + amount, 1.0)
    link.last_reinforced = current_tick

def challenge_link(link, amount=0.1):
    """Something contradicted/weakened this connection"""
    link.strength = max(link.strength - amount, 0.1)  # Never fully zero
    link.last_challenged = current_tick

def decay_link_strength(link):
    """Slow decay if not reinforced (part of Activation mechanic)"""
    ticks_since = current_tick - link.last_reinforced
    if ticks_since > 100:  # ~8 hours game time
        decay = 0.001 * (ticks_since - 100)
        link.strength = max(link.strength - decay, 0.1)
```

---

## STRENGTH MECHANICS (Six Categories)

### Principle

All strength changes reduce to six abstract mechanics. Specific scenarios (betrayal, oaths, gossip, trauma) emerge from combinations.

| Mechanic | Principle | Direction |
|----------|-----------|-----------|
| **Activation** | Use it or lose it | Reinforce on use, decay on neglect |
| **Evidence** | World confirms or denies | Reinforce or challenge |
| **Association** | Co-activation creates connection | Create/strengthen links |
| **Source** | Trust transfers | Initial strength inherited |
| **Commitment** | Action locks in belief | Reinforce after acting |
| **Intensity** | Emotional weight imprints | Modifier on strength change |

---

### M1: ACTIVATION

**Principle:** Links strengthen when used, decay when neglected.

**"Used" means:**
- Referenced in a moment (spoken, thought, narrated)
- Queried by player (asked about)
- Traversed (conversation followed this path)

```python
def apply_activation(link, context):
    """
    Link was used — reinforce it.
    """
    base = 0.03

    # Speaking is stronger than thinking
    if context.type == 'dialogue':
        base = 0.05

    # Direct address is strongest
    if context.direct_address:
        base = 0.08

    reinforce_link(link, amount=base)
```

**Detection:** Canon Holder, when recording any moment.

```python
def record_moment(moment):
    referenced = moment.attached_narratives()
    speaker = moment.speaker

    for narrative in referenced:
        # Speaker's belief activated
        link = get_link(speaker, 'BELIEVES', narrative)
        if link:
            apply_activation(link, moment)

        # ABOUT links activated
        for about_link in narrative.outgoing_about():
            apply_activation(about_link, moment)
```

**Examples:**
- Aldric mentions Edmund → Aldric's BELIEVES links to Edmund narratives activate
- Player asks about the sword → All ABOUT links to sword activate
- Character thinks about their father → Their BELIEVES links to father narratives activate

---

### M2: EVIDENCE

**Principle:** Events in the world confirm or deny beliefs.

```python
def apply_evidence(link, confirms: bool, evidence_weight: float, proximity: float):
    """
    Something happened that confirms or denies this belief.

    evidence_weight: how strong is the evidence (0.1 = rumor, 1.0 = witnessed firsthand)
    proximity: how close was the witness (1.0 = present, 0.5 = heard about)
    """
    effect = evidence_weight * proximity

    if confirms:
        reinforce_link(link, amount=effect * 0.15)
    else:
        challenge_link(link, amount=effect * 0.20)
```

**Detection:** Canon Holder, checking for SUPPORTS/CONTRADICTS relationships.

```python
def record_moment(moment):
    witnesses = get_present_characters(moment.location)
    moment_narratives = moment.attached_narratives()

    for witness in witnesses:
        proximity = compute_proximity(witness, moment.location)

        for narr in moment_narratives:
            # Check what this evidence supports
            supported = get_linked(narr, 'SUPPORTS')
            for supported_narr in supported:
                link = get_link(witness, 'BELIEVES', supported_narr)
                if link:
                    apply_evidence(link, confirms=True,
                                   evidence_weight=narr.weight,
                                   proximity=proximity)

            # Check what this evidence contradicts
            contradicted = get_linked(narr, 'CONTRADICTS')
            for contra_narr in contradicted:
                link = get_link(witness, 'BELIEVES', contra_narr)
                if link:
                    apply_evidence(link, confirms=False,
                                   evidence_weight=narr.weight,
                                   proximity=proximity)
```

**Examples:**
- Edmund caught stealing → Confirms "Edmund is untrustworthy" for witnesses
- Brother's body found → Contradicts "My brother is alive"
- Aldric saves your life → Confirms "Aldric is loyal"

---

### M3: ASSOCIATION

**Principle:** Things that occur together become linked.

```python
def apply_association(narr_a, narr_b, strength: float = 0.03):
    """
    Two narratives co-occurred — strengthen or create SUPPORTS link.
    """
    link = get_link(narr_a, 'SUPPORTS', narr_b)

    if link:
        reinforce_link(link, amount=strength)
    else:
        # Create new association if co-occurrence is strong enough
        if strength > 0.05:
            create_link(narr_a, 'SUPPORTS', narr_b, strength=strength)
```

**Detection:** Canon Holder, tracking conversation context.

```python
def record_moment(moment):
    current = moment.attached_narratives()

    # Recent narratives in same conversation
    recent = query("""
        MATCH (m:Moment)-[:THEN*1..3]->(current:Moment {id: $id})
        MATCH (m)-[:ATTACHED_TO]->(n:Narrative)
        WHERE m.tick > $threshold
        RETURN DISTINCT n
    """, id=moment.id, threshold=current_tick - 10)

    # Co-occurring narratives associate
    for a in current:
        for b in recent:
            if a.id != b.id:
                apply_association(a, b)
```

**Examples:**
- "The Normans burned the village" + "They burned York too" → SUPPORTS link forms
- Mention sword + mention father in same conversation → Association strengthens
- Character talks about debt + talks about fear → Emotional association forms

---

### M4: SOURCE

**Principle:** New beliefs inherit strength from source credibility.

```python
def compute_initial_strength(receiver, source, narrative):
    """
    How strongly does receiver believe this, given who told them?
    """
    BASE_STRENGTH = 0.4

    # How much does receiver trust source?
    trust_narratives = query("""
        MATCH (r:Character {id: $receiver})-[b:BELIEVES]->(n:Narrative)
        WHERE n.type = 'relationship'
          AND (n)-[:ABOUT]->(:Character {id: $source})
        RETURN n, b.strength
    """, receiver=receiver.id, source=source.id)

    if not trust_narratives:
        credibility = 0.5  # Unknown source = neutral
    else:
        # Average trust from relationship narratives
        credibility = mean([b.strength for n, b in trust_narratives])

    # Direct witness vs secondhand
    if source.witnessed(narrative):
        directness = 1.0
    else:
        directness = 0.6  # Gossip discount

    return BASE_STRENGTH * credibility * directness
```

**Detection:** Handler, when creating new BELIEVES link.

```python
def character_learns(receiver, narrative, source):
    """
    Character learns something from another character.
    """
    initial = compute_initial_strength(receiver, source, narrative)
    create_link(receiver, 'BELIEVES', narrative, strength=initial)
```

**Examples:**
- Trusted friend tells you Edmund betrayed you → High initial strength
- Stranger tells you the same → Lower initial strength
- Enemy tells you something → Maybe you believe the opposite
- Gossip (X told Y who told you) → Compounding discount

---

### M5: COMMITMENT

**Principle:** Acting on a belief locks it in.

```python
def apply_commitment(character, narrative, action_cost: float):
    """
    Character acted on this belief. Reinforce it.

    action_cost: how much did the action cost? (0.1 = trivial, 1.0 = major sacrifice)
    """
    link = get_link(character, 'BELIEVES', narrative)
    if link:
        # Higher cost = stronger commitment
        reinforce_link(link, amount=0.05 + (action_cost * 0.10))
```

**Detection:** Action processor, when moment with action field actualizes.

```python
def process_action(moment):
    if not moment.action:
        return

    actor = moment.speaker

    # What beliefs motivated this action?
    motivating = query("""
        MATCH (m:Moment {id: $id})-[:ATTACHED_TO]->(n:Narrative)
        MATCH (c:Character {id: $actor})-[:BELIEVES]->(n)
        RETURN n
    """, id=moment.id, actor=actor.id)

    action_cost = estimate_action_cost(moment.action)

    for narrative in motivating:
        apply_commitment(actor, narrative, action_cost)
```

**Examples:**
- Accuse Edmund publicly → Locked into "Edmund is guilty"
- Give away money → Locked into belief that justified it
- Risk your life for someone → Strongly locked into trusting them

---

### M6: INTENSITY

**Principle:** High-emotion contexts amplify strength changes.

```python
def compute_intensity_modifier(context):
    """
    How emotionally intense is this moment?
    Returns multiplier for strength changes.
    """
    base = 1.0

    # Tension pressure
    active_tensions = detect_tensions()
    max_pressure = max([t['pressure'] for t in active_tensions], default=0)
    base += max_pressure * 0.5  # Up to +0.5 from tension

    # Danger
    if context.danger_level:
        base += context.danger_level * 0.3  # Up to +0.3 from danger

    # Emotional weight of moment
    if context.tone in ['grief', 'rage', 'terror', 'ecstasy']:
        base += 0.3
    elif context.tone in ['sad', 'angry', 'afraid', 'joyful']:
        base += 0.15

    return min(base, 2.0)  # Cap at 2x
```

**Application:** Wraps all other mechanics.

```python
def record_moment(moment):
    intensity = compute_intensity_modifier(moment)

    # All strength changes multiplied by intensity
    for narrative in moment.attached_narratives():
        link = get_link(moment.speaker, 'BELIEVES', narrative)
        if link:
            apply_activation(link, moment)
            link.last_change *= intensity  # Amplify the change
```

**Examples:**
- Learn something during battle → Stronger imprint
- Confession during high tension → More impactful
- Casual mention during calm → Normal strength change
- Traumatic revelation → 2x strength effect

---

### Summary

| Mechanic | Trigger | Effect Range |
|----------|---------|--------------|
| Activation | Link referenced/used | +0.03 to +0.08 |
| Evidence+ | Confirming event witnessed | +0.05 to +0.15 |
| Evidence- | Contradicting event witnessed | -0.05 to -0.30 |
| Association | Co-occurrence | +0.03, create if none |
| Source | New belief from someone | initial × credibility |
| Commitment | Acted on belief | +0.05 to +0.15 |
| Intensity | High-stress context | ×1.0 to ×2.0 multiplier |

### Agents That Modify Strength

| Agent | Mechanics Applied |
|-------|-------------------|
| **Canon Holder** | Activation, Evidence, Association |
| **Input Parser** | Activation |
| **Handler** | Source (when character learns), Evidence (deciding response) |
| **Action Processor** | Commitment |
| **All** | Intensity (wraps other mechanics) |

### Emergent Scenarios

| Scenario | Mechanics Involved |
|----------|-------------------|
| Betrayal | Evidence- (strong), Intensity (high) |
| Oath made | Activation, Commitment, Intensity |
| Oath broken | Evidence- (strong), Intensity (high) |
| Gossip spreads | Source (compounding discount), Association |
| Trauma | Evidence, Intensity (×2.0) |
| Trusted friend tells you | Source (high credibility) |
| Enemy's accusation | Source (low/negative credibility) |
| Public declaration | Activation (strong), Commitment |
| Place triggers memory | Activation (via ATTACHED_TO place) |

---

### Why Conservation

| Approach | Problem |
|----------|---------|
| Links create energy | System explodes. Requires arbitrary dampening. |
| No conservation | Tuning nightmare. Magic numbers everywhere. |
| **Conservation + external pumps** | Predictable. "Heat" emerges from structure. |

"Arguments heat both sides" because both sides have believers pumping — not because contradiction creates energy from nothing.

---

### The Energy Equation

```
Per tick:

  ΔE_system = injection - decay - actualization

Where:
  injection    = Σ (character pumping)
  decay        = Σ (narrative.energy * decay_rate)
  actualization = Σ (moment.weight) for moments that flip
```

Links redistribute within the system. They don't change total energy.

---
