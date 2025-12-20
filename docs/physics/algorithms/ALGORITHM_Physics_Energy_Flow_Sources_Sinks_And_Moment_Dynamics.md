# Physics — Algorithm: Energy Flow Sources Sinks And Moment Dynamics

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
THIS:           ALGORITHM_Physics_Energy_Flow_Sources_Sinks_And_Moment_Dynamics.md (you are here)
SCHEMA:         ../../schema/SCHEMA_Moments.md
VALIDATION:     ../VALIDATION_Physics.md
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## ENERGY SOURCES

### S1: Character Pumping

Characters inject energy into narratives they care about.

**Core insight:** We don't compute "proximity" separately. Energy levels ARE proximity. Characters pump into narratives proportional to belief strength. Energy flow through the graph handles the rest.

#### Character Energy Sources

| Source | Amount | When |
|--------|--------|------|
| **Baseline** | 0.01 per tick | Always (existing) |
| **Being talked about** | from ABOUT links | Others discuss you |
| **Player focus** | 1.0 / targets | Direct attention |
| **Arrival** | 0.5 one-time | Enter scene |

#### Character State

| State | Pump Modifier | Notes |
|-------|---------------|-------|
| `awake` | 1.0 | Full pumping |
| `sleeping` | 0.2 | Dreams, weak influence |
| `unconscious` | 0.0 | No pumping |
| `dead` | 0.0 | No pumping (narratives persist through others) |

```python
def get_state_modifier(state):
    return {
        'awake': 1.0,
        'sleeping': 0.2,
        'unconscious': 0.0,
        'dead': 0.0
    }.get(state, 1.0)
```

#### Pump Calculation

```python
PUMP_RATE = 0.1
BASELINE_REGEN = 0.01

def character_tick(character):
    """
    Character pumps energy into narratives.
    No proximity calculation - energy flow handles relevance.
    """
    # Baseline regeneration
    character.energy = min(
        character.energy + BASELINE_REGEN,
        MAX_CHARACTER_ENERGY
    )

    # State modifier
    state_mod = get_state_modifier(character.state)
    if state_mod == 0:
        return

    # Pump budget
    pump_budget = character.energy * PUMP_RATE * state_mod

    # Distribute by belief strength only
    beliefs = character.outgoing_belief_links()
    total_strength = sum(link.strength for link in beliefs)

    if total_strength == 0:
        return

    for link in beliefs:
        narrative = link.target
        proportion = link.strength / total_strength
        transfer = pump_budget * proportion
        narrative.energy += transfer
        character.energy -= transfer
```

**Why no proximity filter?**

Energy flow through the graph handles "relevance" automatically:
1. Player focuses on Edmund → Edmund's narratives get energy
2. Those narratives transfer to related narratives (SUPPORTS, ELABORATES)
3. High energy narratives surface
4. Low energy narratives don't

We don't pre-filter what characters pump into. We let them pump into everything they believe, and physics determines what matters.

#### Dead Characters

Dead characters don't pump. But their narratives persist through the living.

```
Edmund dies
  → Edmund.state = 'dead'
  → Edmund stops pumping
  → narr_edmund_betrayal persists
  → Aldric still pumps into it (his belief)
  → The narrative lives through believers
```

---

### S2: Player Focus Injection

What the player attends to receives energy.

```python
def player_focus_injection(player, focus_targets):
    """
    Player attention injects energy into scene.
    Focus targets: characters addressed, things examined, topics raised.
    """
    FOCUS_INJECTION = 1.0  # Per input

    for target in focus_targets:
        if isinstance(target, Character):
            target.energy += FOCUS_INJECTION / len(focus_targets)
        elif isinstance(target, Narrative):
            target.energy += FOCUS_INJECTION / len(focus_targets)
        elif isinstance(target, Thing):
            # Things don't hold energy — redirect to related narratives
            for narrative in narratives_about(target):
                narrative.energy += (FOCUS_INJECTION / len(focus_targets)) / count
```

**Why:** Player attention is the camera. What you look at lights up.

---

### S3: World Events

External events inject energy.

```python
def world_event_injection(event):
    """
    News, arrivals, discoveries inject energy.
    """
    if event.type == 'arrival':
        # Character arrives — they bring their energy with them
        event.character.energy += ARRIVAL_BOOST  # 0.5

    elif event.type == 'news':
        # News creates/energizes a narrative
        narrative = event.narrative
        narrative.energy += NEWS_INJECTION  # 0.3

    elif event.type == 'discovery':
        # Discovery energizes existing narrative
        narrative = event.narrative
        narrative.energy += DISCOVERY_INJECTION  # 0.5
```

**Why:** The world beyond the player injects surprise.

---

### S4: Tension Pressure (Structural)

Detected tensions inject energy into related narratives.

```python
def tension_injection(tensions):
    """
    Structural tensions push energy toward crisis.
    Not created from nothing — drawn from participants.
    """
    for tension in tensions:
        pressure = tension['pressure']

        if pressure > 0.3:  # Only meaningful tensions
            # Draw energy from involved characters
            characters = tension['characters']
            draw_per_char = pressure * TENSION_DRAW  # 0.2

            total_drawn = 0
            for char in characters:
                drawn = min(char.energy * draw_per_char, char.energy * 0.5)
                char.energy -= drawn
                total_drawn += drawn

            # Inject into related narratives
            narratives = tension['narratives']
            for narrative in narratives:
                narrative.energy += total_drawn / len(narratives)
```

**Why:** Tension doesn't create energy — it concentrates it. The participants feel drained because their energy is being pulled into the crisis.

---

## ENERGY SINKS

### K1: Decay

Constant drain on all energy.

```python
DECAY_RATE = 0.02  # 2% per tick

def apply_decay():
    """
    Energy bleeds out of the system.
    Core narratives decay slower.
    """
    for narrative in graph.narratives:
        rate = DECAY_RATE

        # Core types resist decay
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25

        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_ENERGY)  # 0.01 floor

    for character in graph.characters:
        character.energy *= (1 - rate)
        character.energy = max(character.energy, MIN_ENERGY)
```

**Why:** Without decay, everything accumulates forever. Decay creates forgetting.

---

### K2: Actualization

When moments flip, energy is spent.

```python
def moment_actualization(moment):
    """
    Flipping a moment costs energy.
    Energy comes from attached sources.
    """
    cost = moment.weight * ACTUALIZATION_COST  # 0.5

    # Draw from speakers
    speakers = moment.can_speak_characters()
    if speakers:
        cost_per_speaker = cost / len(speakers)
        for speaker in speakers:
            speaker.energy -= cost_per_speaker

    # Draw from attached narratives
    attached = moment.attached_narratives()
    if attached:
        cost_per_narrative = cost / len(attached)
        for narrative in attached:
            narrative.energy -= cost_per_narrative

    moment.status = 'spoken'
```

**Why:** Speaking takes effort. The moment doesn't come from nowhere — it draws from those who produced it.

---

## ENERGY TRANSFER (Links)

### Principle

Links transfer energy between nodes. **Zero-sum between linked nodes.**

```
Transfer from A to B via link:
  A.energy -= transfer_amount
  B.energy += transfer_amount
```

Transfer amount depends on:
- Source energy (can't give what you don't have)
- Link strength (stronger connection = faster flow)
- Link type factor (some links conduct better)

---

### T1: CONTRADICTS (Bidirectional)

Both sides pull from each other simultaneously.

```python
CONTRADICT_FACTOR = 0.15  # Per direction, so 0.30 total exchange

def transfer_contradiction(link):
    """
    Contradiction: bidirectional exchange.

    A ←──CONTRADICTS──→ B

    A pulls from B. B pulls from A.
    Net effect: energy equalizes, both stay hot if either is hot.
    """
    A = link.source
    B = link.target
    strength = link.strength

    # A pulls from B
    transfer_A = B.energy * strength * CONTRADICT_FACTOR
    B.energy -= transfer_A
    A.energy += transfer_A

    # B pulls from A
    transfer_B = A.energy * strength * CONTRADICT_FACTOR
    A.energy -= transfer_B
    B.energy += transfer_B
```

**Why bidirectional:** You can't think about one side of an argument without the other coming to mind. Contradiction is mutual.

**Why high factor (0.30 total):** Arguments are sticky. They grab attention.

**Emergent behavior:** If Edmund pumps "I was right" and Aldric pumps "Edmund betrayed us", both narratives stay hot because:
1. Characters pump in
2. Contradiction exchanges between them
3. Neither can cool while the other is hot

---

### T2: SUPPORTS (Bidirectional)

Allies share fate.

```python
SUPPORT_FACTOR = 0.10  # Per direction

def transfer_support(link):
    """
    Support: bidirectional sharing.

    A ←──SUPPORTS──→ B

    Energy equalizes. Doubt one, doubt all.
    """
    A = link.source
    B = link.target
    strength = link.strength

    # Energy flows toward equilibrium
    diff = A.energy - B.energy
    transfer = diff * strength * SUPPORT_FACTOR

    A.energy -= transfer
    B.energy += transfer
```

**Why equilibrium:** Supporting narratives should have similar energy. If one rises, it lifts the others. If one falls, it drags the others.

**Lower factor than contradiction:** Agreement is less grabby than conflict.

---

### T3: ELABORATES (Unidirectional, Parent → Child)

Details inherit from their source.

```python
ELABORATE_FACTOR = 0.15

def transfer_elaboration(link):
    """
    Elaboration: parent feeds child.

    A ──ELABORATES──→ B

    Parent energizes details. Not reverse.
    """
    parent = link.source
    child = link.target
    strength = link.strength

    transfer = parent.energy * strength * ELABORATE_FACTOR
    parent.energy -= transfer
    child.energy += transfer
```

**Why unidirectional:** "Edmund betrayed us" (parent) energizes "Edmund opened the gate" (detail). The detail doesn't energize the parent — it's downstream.

---

### T4: SUBSUMES (Unidirectional, Specific → General)

Many specifics feed one generalization.

```python
SUBSUME_FACTOR = 0.10

def transfer_subsumption(link):
    """
    Subsumption: specific feeds general.

    A ──SUBSUMES──→ B

    "He lied" + "He stole" + "He cheated" → "He's untrustworthy"
    """
    specific = link.source
    general = link.target
    strength = link.strength

    transfer = specific.energy * strength * SUBSUME_FACTOR
    specific.energy -= transfer
    general.energy += transfer
```

**Why low factor:** Each specific contributes a little. The general accumulates from many sources.

---

### T5: SUPERSEDES (Draining)

New truth drains old.

```python
SUPERSEDE_FACTOR = 0.25

def transfer_supersession(link):
    """
    Supersession: old feeds new, loses in the process.

    A ──SUPERSEDES──→ B (A is old, B is new)

    "Edmund is in York" → "Edmund fled York"
    """
    old = link.source
    new = link.target
    strength = link.strength

    transfer = old.energy * strength * SUPERSEDE_FACTOR
    old.energy -= transfer
    new.energy += transfer

    # Additional drain: old loses extra (world moved on)
    old.energy *= (1 - SUPERSEDE_FACTOR * 0.5)
```

**Why draining:** Supersession isn't just transfer — the old becomes irrelevant. It loses more than it gives.

---

### T6: ABOUT (Focal Point Pulls)

Being talked about attracts energy.

```python
ABOUT_FACTOR = 0.05

def transfer_about(link):
    """
    About: focal point pulls from narratives.

    Narrative ──ABOUT──→ Character/Thing

    Reverse flow: the subject draws energy from stories about them.
    """
    narrative = link.source
    subject = link.target

    if isinstance(subject, Character):
        transfer = narrative.energy * link.strength * ABOUT_FACTOR
        narrative.energy -= transfer
        subject.energy += transfer
    # Things don't hold energy — skip
```

**Why reverse flow:** Being the subject of attention energizes you. Aldric is talked about → Aldric becomes more present.

---

### T7: CAN_LEAD_TO (Moment to Moment)

Energy flows through conversation structures.

```python
CAN_LEAD_TO_FACTOR = 0.15

def transfer_can_lead_to(link):
    """
    Conversation potential: energy flows to connected moments.

    Moment_A ──[CAN_LEAD_TO]──> Moment_B

    Unidirectional by default. Bidirectional if link.bidirectional = true.
    """
    origin = link.source
    destination = link.target
    strength = link.strength

    # Forward flow
    transfer = origin.energy * strength * CAN_LEAD_TO_FACTOR
    origin.energy -= transfer
    destination.energy += transfer

    # Reverse flow only if bidirectional
    if link.bidirectional:
        reverse = destination.energy * strength * CAN_LEAD_TO_FACTOR
        destination.energy -= reverse
        origin.energy += reverse
```

**Why unidirectional default:** Conversations flow forward. "What happened next?" pulls energy downstream.

**When bidirectional:** Parallel options, back-and-forth debates, revisitable topics.

---

### T8: CAN_SPEAK (Character to Moment)

Characters energize moments they can speak.

```python
CAN_SPEAK_FACTOR = 0.1

def transfer_can_speak(link):
    """
    Character can speak this moment → character energy flows in.

    Character ──[CAN_SPEAK]──> Moment
    """
    character = link.source
    moment = link.target
    strength = link.strength

    # Only if character is awake and present
    if character.state != 'awake':
        return

    transfer = character.energy * strength * CAN_SPEAK_FACTOR
    character.energy -= transfer
    moment.energy += transfer
```

**Why:** Characters energize their potential speech. More invested character → more energy into what they might say.

---

### T9: ATTACHED_TO (Moment from Sources)

Moments draw energy from what they're attached to.

```python
ATTACHED_TO_FACTOR = 0.1

def transfer_attached_to(link):
    """
    Moment attached to something → draws energy from it.

    Moment ──[ATTACHED_TO]──> Character | Narrative | Place | Thing

    Reverse flow: source energizes the moment.
    """
    moment = link.source
    target = link.target
    strength = link.strength

    # Only nodes with energy
    if not hasattr(target, 'energy'):
        return

    # Reverse flow: target → moment
    transfer = target.energy * strength * ATTACHED_TO_FACTOR
    target.energy -= transfer
    moment.energy += transfer
```

**Why reverse:** A moment about Edmund draws energy when Edmund is hot. Relevance emerges from what's energized.

---

### Actualization (Energy Spent)

When moment flips `active` → `spoken`:

```python
ACTUALIZATION_COST = 0.6

def actualize_moment(moment):
    """
    Moment becomes canon. Energy partially spent.
    """
    # Partial drain — recent speech still has presence
    cost = moment.energy * ACTUALIZATION_COST
    moment.energy -= cost

    # Status change
    moment.status = 'spoken'
    moment.tick_spoken = current_tick

    # Remaining energy decays normally from here
```

**Why partial (0.6):** Just-spoken moments still have presence. They fade naturally rather than vanishing.

---

### Moment Decay by Status

| Status | Decay Rate | Notes |
|--------|------------|-------|
| `possible` | 0.02 | Normal — unused possibilities fade |
| `active` | 0.01 | Slower — something is happening |
| `spoken` | 0.03 | Faster — it's done, recedes into past |
| `dormant` | 0.005 | Very slow — waiting to reactivate |
| `decayed` | N/A | No energy, no decay |

---

## MOMENT ENERGY & WEIGHT

Moments have both weight (importance) and energy (activation). Both matter for surfacing.

### Surfacing Logic

```python
def salience(moment):
    """How much should this moment surface right now?"""
    return moment.weight * moment.energy

def should_surface(moment):
    """Does this moment cross the threshold?"""
    return salience(moment) >= SURFACE_THRESHOLD
```

### Energy Flow Into Moments

Moments receive energy from:
- Characters via CAN_SPEAK links (T8)
- Narratives/Characters via ATTACHED_TO links (T9)
- Other moments via CAN_LEAD_TO links (T7)
- Player focus injection

Energy flows OUT via:
- CAN_LEAD_TO links to other moments
- Actualization (partial spend)
- Decay

### Weight Evolution

Weight changes slowly via the six strength mechanics:
- Activation (moment spoken)
- Evidence (confirms/denies attached narratives)
- Association (co-occurs with important content)
- Commitment (player acted on this)
- Intensity (high-stress context)

```python
def reinforce_moment_weight(moment, amount):
    moment.weight = min(moment.weight + amount, 1.0)
    moment.last_reinforced = current_tick
```

### Example

```
moment_aldric_confession:
  weight: 0.8   # Important (has been building)
  energy: 0.3   # Not currently active
  salience: 0.24  # Below threshold

Player asks about Edmund:
  → energy injected into Edmund-related content
  → narr_edmund_betrayal heats up
  → moment_aldric_confession attached to that narrative
  → energy flows into moment (T9)
  → energy: 0.3 → 0.7
  → salience: 0.56  # Crosses threshold
  → Moment surfaces
```

---
