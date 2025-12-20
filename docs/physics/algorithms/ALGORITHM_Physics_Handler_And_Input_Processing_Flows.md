# Physics — Algorithm: Handler And Input Processing Flows

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
THIS:           ALGORITHM_Physics_Handler_And_Input_Processing_Flows.md (you are here)
SCHEMA:         ../../schema/SCHEMA_Moments.md
VALIDATION:     ../VALIDATION_Physics.md
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## Physics Tick

### Core Principle

**The graph is always running.**

The tick is not "processing a cascade." The tick is one heartbeat of a continuous system. The graph never stops. Speed controls how fast we tick and what we display.

---

### What Triggers a Tick

| Trigger | Notes |
|---------|-------|
| Time interval | Based on current speed setting |
| Player input | May trigger immediate tick |
| Handler completion | New potentials ready to integrate |

---

### Tick Steps (Sequential)

```python
def physics_tick(current_time: float):
    """
    One heartbeat of the continuous system.
    Steps must execute in order.

    Energy model: see the Energy Mechanics section for full details.
    Energy IS proximity — no separate focus tracking needed.
    """
    # 1. PUMP — Characters inject energy into narratives
    character_pumping()

    # 2. TRANSFER — Energy flows through narrative links
    transfer_energy()

    # 3. TENSION — Structural tensions concentrate energy
    tensions = detect_tensions()
    tension_injection(tensions)

    # 4. DECAY — Energy leaves the system
    apply_decay()

    # 5. WEIGHT — Recompute moment weights from sources
    recompute_moment_weights()

    # 6. DETECT — Find moments that crossed threshold
    flipped = detect_flips()

    # 7. EMIT — Send flipped moments to Canon Holder
    for moment in flipped:
        canon_holder.record(moment)

    # 8. BREAKS — Return any structural breaks for handling
    breaks = [t for t in tensions if is_unsustainable(t)]
    return breaks
```

---

### Step 1: Character Pumping

Characters are batteries. They pump energy into narratives they believe.

```python
def character_pumping():
    """
    Characters inject energy into narratives via BELIEVES links.
    Pump rate modified by state only. No proximity filter.
    Energy flow through the graph handles relevance.
    See the Energy Mechanics section for full details.
    """
    for char in graph.characters:
        # Baseline regeneration
        char.energy = min(char.energy + BASELINE_REGEN, MAX_CHARACTER_ENERGY)

        # State modifier (dead/unconscious = 0, sleeping = 0.2, awake = 1.0)
        state_mod = get_state_modifier(char.state)
        if state_mod == 0:
            continue

        pump_budget = char.energy * PUMP_RATE * state_mod  # 0.1 * state

        # Distribute by belief strength only - no proximity filter
        beliefs = char.believes_links()
        total_strength = sum(link.strength for link in beliefs)

        if total_strength == 0:
            continue

        for link in beliefs:
            narrative = link.target
            proportion = link.strength / total_strength
            transfer = pump_budget * proportion
            narrative.energy += transfer
            char.energy -= transfer
```

**Why characters pump:** Characters are the engine. They care, therefore the story matters. No characters caring = no energy = no drama.

**Why no proximity filter:** Energy IS proximity. We don't pre-filter what characters pump into. We let them pump into everything they believe, and energy flow through the graph (CONTRADICTS, SUPPORTS, ABOUT links) determines what matters. High energy = close to attention. Low energy = far from attention.

---

### Step 2: Energy Transfer

Links route energy between narratives. Zero-sum between linked nodes.

```python
def transfer_energy():
    """
    Narrative-to-narrative and narrative-to-subject transfers.
    See the Energy Mechanics section for full transfer mechanics.
    """
    # Narrative links
    for link in graph.narrative_links:
        if link.type == 'CONTRADICTS':
            transfer_contradiction(link)   # Bidirectional, 0.15 each way
        elif link.type == 'SUPPORTS':
            transfer_support(link)         # Equilibrating, 0.10
        elif link.type == 'ELABORATES':
            transfer_elaboration(link)     # Parent → child, 0.15
        elif link.type == 'SUBSUMES':
            transfer_subsumption(link)     # Specific → general, 0.10
        elif link.type == 'SUPERSEDES':
            transfer_supersession(link)    # Old → new + drain, 0.25

    # ABOUT links (focal point pulls)
    for link in graph.about_links:
        transfer_about(link)               # Subject pulls, 0.05
```

**Why zero-sum:** Links don't create energy — they route it. Conservation makes the system predictable.

---

### Step 3: Tension Injection

Detected tensions concentrate energy from participants into the crisis.

```python
def tension_injection(tensions):
    """
    Structural tensions draw energy from involved characters.
    Tension is computed, not stored. See the Energy Mechanics section.
    """
    for tension in tensions:
        if tension['pressure'] <= 0.3:
            continue

        # Draw from participants
        total_drawn = 0
        for char in tension['characters']:
            draw = min(char.energy * tension['pressure'] * TENSION_DRAW,
                      char.energy * 0.5)
            char.energy -= draw
            total_drawn += draw

        # Inject into related narratives
        for narrative in tension['narratives']:
            narrative.energy += total_drawn / len(tension['narratives'])
```

**Why draw from characters:** Tension doesn't create energy — it concentrates it. The participants feel drained because the crisis pulls them in.

---

### Step 4: Decay

Energy leaves the system. This is the sink.

```python
def apply_decay():
    """
    Constant drain on all energy.
    Core narratives (oath, blood, debt) decay slower.
    """
    # Narrative decay
    for narrative in graph.narratives:
        rate = DECAY_RATE  # 0.02
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25
        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_ENERGY)

    # Character decay
    for char in graph.characters:
        char.energy *= (1 - DECAY_RATE)
        char.energy = max(char.energy, MIN_ENERGY)
```

**Why decay:** Without decay, everything accumulates forever. Decay creates forgetting. Old grievances fade unless someone keeps pumping.

---

### Step 5: Moment Weight Computation

Moment weight is derived from attached sources — not accumulated.

```python
def recompute_moment_weights():
    """
    Weight = sum of energy from speakers + attached narratives + present characters.
    """
    for moment in graph.moments:
        if moment.status not in ['possible', 'active']:
            continue

        weight = 0

        # From characters who can speak it
        for link in moment.incoming_can_speak():
            char = link.source
            if char.is_present:
                weight += char.energy * link.strength

        # From attached narratives
        for link in moment.outgoing_attached_to():
            if isinstance(link.target, Narrative):
                weight += link.target.energy * link.strength

        # From attached present characters
        for link in moment.outgoing_attached_to():
            if isinstance(link.target, Character) and link.target.is_present:
                weight += link.target.energy * link.strength

        moment.weight = weight
```

**Why derived:** Moments don't have independent energy. They surface when their sources are energized. This prevents weight accumulation bugs.

---

### Step 6: Flip Detection

Identify moments that crossed the threshold.

```python
def detect_flips() -> List[Moment]:
    """
    Deterministic: weight >= threshold means flip.
    """
    flipped = []
    for moment in graph.moments:
        if moment.status == 'possible' and moment.weight >= FLIP_THRESHOLD:
            moment.status = 'active'
            flipped.append(moment)

    return sorted(flipped, key=lambda m: m.weight, reverse=True)
```

#### Deterministic vs Probabilistic

For v1, flipping is deterministic. `weight >= 0.8` = flip.

Probabilistic (weight = probability per tick) adds organic feel but complicates reasoning. Can add later if mechanical feel is a problem.

---

### Step 7: Emit to Canon Holder

Flipped moments are sent to Canon Holder for recording and display.

```python
def emit_flips(flipped: List[Moment]):
    """
    Canon Holder receives flipped moments in weight order.
    Actualization costs energy — drawn from sources.
    """
    for moment in flipped:
        # Actualization cost
        cost = moment.weight * ACTUALIZATION_COST  # 0.5
        speakers = moment.can_speak_characters()
        if speakers:
            for speaker in speakers:
                speaker.energy -= cost / len(speakers)

        # Record to canon
        canon_holder.record(moment)

        # Trigger handlers for attached characters
        character = get_attached_character(moment)
        if character:
            trigger_handler(character.id, triggered_by=moment)
```

**Why actualization costs:** Speaking takes effort. The moment draws from those who produced it. This prevents infinite chatter.

---

### Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `FLIP_THRESHOLD` | 0.8 | When weight crosses this, moment flips |
| `BASELINE_REGEN` | 0.01 | Character energy regen per tick |
| `PUMP_RATE` | 0.1 | Character energy → narratives per tick |
| `DECAY_RATE` | 0.02 | 2% per tick |
| `TENSION_DRAW` | 0.2 | How much tension pulls from participants |
| `ACTUALIZATION_COST` | 0.5 | Energy cost per moment flip |
| `MIN_ENERGY` | 0.01 | Floor — can always revive |
| `MAX_CHARACTER_ENERGY` | 10.0 | Ceiling — prevent runaway |
| `MAX_NARRATIVE_ENERGY` | 5.0 | Ceiling — keep bounded |

See the Energy Mechanics section for transfer factors, state modifiers, and proximity rules.

---

### Graph States

The graph is always running but exhibits different states:

| State | Characteristics |
|-------|-----------------|
| **Active** | High energy, many flips, drama unfolding |
| **Quiet** | Low energy, few flips, equilibrium |
| **Critical** | Energy building, thresholds approaching, tension rising |

But never **stopped**.

---

### Tick Rate by Speed

| Speed | Ticks Per Second | Notes |
|-------|------------------|-------|
| 1x | ~0.2 | One tick per moment duration |
| 2x | ~2.0 | Rapid, filtered display |
| 3x | Max system speed | Only interrupts shown |

See the Speed Controller section for full speed controller logic.

---

### What Physics Does NOT Do

- Generate new moments (that's Handlers)
- Decide what content to create (that's Handlers)
- Record history (that's Canon Holder)
- Modify world state (that's Action Processing)
- Author tensions (tensions emerge from structure)

Physics only: pump, transfer, decay, detect.

---

### Invariants

1. **Energy conservation:** Pumps in = decay + actualization out (links are zero-sum)
2. **Continuous:** Graph never stops, only changes rate
3. **Deterministic flips:** Same state → same flips (for v1)
4. **Derived weights:** Moment weight is computed, not accumulated

---

### Relationship to the Energy Mechanics section

This file defines the **tick cycle** — when and in what order things happen.

the Energy Mechanics section defines the **energy mechanics** — how energy flows, what creates it, what consumes it.

| This File | Energy File |
|-----------|-------------|
| Tick orchestration | Transfer formulas |
| Step ordering | Link type behaviors |
| Parameter values | Emergent behaviors |
| What happens when | Why it works |

---

*"The tick is one heartbeat of a continuous system."*


---

## Canon Holder

### Core Principle

**Everything is moments. Canon Holder is the gatekeeper.**

Canon Holder records what becomes real. It doesn't decide what happens — physics and handlers do that. Canon Holder makes it permanent.

---

### The Flow

```
Energy flows
  → salience crosses threshold
  → moment flips possible → active
  → Handler generates (if needed)
  → Canon Holder records
  → moment becomes spoken
  → THEN link created
  → Actions processed
  → Strength mechanics triggered
  → Time advances
```

---

### Canon Holder Responsibilities

| Responsibility | What It Does |
|----------------|--------------|
| **Record** | Flip moment `active` → `spoken` |
| **Link** | Create THEN link to previous moment |
| **Time** | Advance game time based on moment duration |
| **Trigger** | Process actions (travel, take, etc.) |
| **Strength** | Apply strength mechanics (Activation, Evidence, etc.) |
| **Notify** | Push to frontend |

---

### The Code Shape

```python
def record_to_canon(moment, previous_moment=None):
    """
    Moment becomes canon. Everything follows from this.
    """
    # 1. Status change
    moment.status = 'spoken'
    moment.tick_spoken = current_tick

    # 2. Energy cost (actualization)
    moment.energy *= (1 - ACTUALIZATION_COST)

    # 3. THEN link (history chain)
    if previous_moment:
        create_link(previous_moment, 'THEN', moment, {
            'tick': current_tick,
            'player_caused': is_player_input()
        })

    # 4. Time passage
    duration = estimate_moment_duration(moment)
    advance_time(minutes=duration)

    # 5. Strength mechanics
    apply_activation(moment)  # M1: speaker's beliefs reinforced
    apply_evidence(moment)    # M2: witnesses' beliefs affected
    apply_association(moment) # M3: co-occurring narratives linked

    # 6. Actions
    if moment.action:
        process_action(moment)

    # 7. Notify frontend
    push_to_display(moment)
```

---

### Flip Detection

Canon Holder doesn't detect flips. It *records* them.

**Who detects flips?**

Physics tick detects when moments cross the salience threshold.

```python
def detect_ready_moments():
    """
    Find moments ready to surface.
    Called each tick or on energy change.
    """
    return query("""
        MATCH (m:Moment)
        WHERE m.status = 'possible'
          AND (m.weight * m.energy) >= $threshold
          AND all_presence_requirements_met(m)
        RETURN m
        ORDER BY (m.weight * m.energy) DESC
    """, threshold=SURFACE_THRESHOLD)
```

**What happens with multiple?**

```python
def process_ready_moments(ready):
    """
    Multiple moments can be ready. Process in order.
    """
    previous = get_last_spoken_moment()

    for moment in ready:
        # Check still valid (state may have changed)
        if not still_valid(moment):
            continue

        # Flip to active
        moment.status = 'active'

        # Handler needed?
        if needs_handler(moment):
            # Async - handler will call record_to_canon when done
            dispatch_handler(moment, previous)
        else:
            # Direct record
            record_to_canon(moment, previous)

        previous = moment
```

---

### Status Progression

```
possible ──[salience >= threshold]──> active ──[canon recorded]──> spoken
    │                                    │
    │                                    └──[handler fails]──> possible (retry)
    │
    └──[energy decays below minimum]──> decayed

spoken ──[never changes]──> (permanent history)

dormant ──[presence satisfied + energy]──> possible
```

| Status | Meaning |
|--------|---------|
| `possible` | Could happen, competing for attention |
| `active` | Crossed threshold, being processed |
| `spoken` | Canon. Happened. Immutable. |
| `dormant` | Waiting for conditions (place, person) |
| `decayed` | Lost relevance, pruned |

---

### Who Speaks?

```python
def determine_speaker(moment):
    """
    Highest-weight CAN_SPEAK link from present character.
    """
    speakers = query("""
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $id})
        WHERE c.state = 'awake'
          AND (c)-[:AT]->(:Place)<-[:AT]-(:Character {id: 'player'})
        RETURN c, r.strength
        ORDER BY r.strength DESC
        LIMIT 1
    """, id=moment.id)

    return speakers[0] if speakers else None
```

---

### Rate Limiting

```python
MAX_MOMENTS_PER_TICK = 5
MIN_MOMENT_GAP_MS = 100  # For display pacing

def process_ready_moments(ready):
    processed = 0
    for moment in ready:
        if processed >= MAX_MOMENTS_PER_TICK:
            break  # Rest next tick

        # ... process ...
        processed += 1
```

**Player Experience:** Cascades can happen, but not overwhelming. 5 moments max per tick. Display paces them for readability.

---

### Actualization Cost

When a moment is recorded, it partially drains energy from the moment itself:

```python
ACTUALIZATION_COST = 0.6

def actualize_energy(moment):
    """
    Partial drain — recent speech still has presence.
    """
    moment.energy *= (1 - ACTUALIZATION_COST)
```

**Why partial (0.6):** Just-spoken moments still have presence. They fade naturally rather than vanishing.

---

### Strength Mechanics Applied

Canon Holder triggers three of the six strength mechanics on record:

#### M1: Activation

```python
def apply_activation(moment):
    """
    Speaker's beliefs reinforced by speaking.
    """
    speaker = moment.speaker
    narratives = moment.attached_narratives()

    for narrative in narratives:
        link = get_link(speaker, 'BELIEVES', narrative)
        if link:
            base = 0.05 if moment.type == 'dialogue' else 0.03
            reinforce_link(link, amount=base)

        # ABOUT links activated
        for about_link in narrative.outgoing_about():
            reinforce_link(about_link, amount=0.03)
```

#### M2: Evidence

```python
def apply_evidence(moment):
    """
    Witnesses' beliefs affected by what they saw.
    """
    witnesses = get_present_characters(moment.location)
    moment_narratives = moment.attached_narratives()

    for witness in witnesses:
        for narr in moment_narratives:
            # Confirming evidence
            for supported in get_linked(narr, 'SUPPORTS'):
                link = get_link(witness, 'BELIEVES', supported)
                if link:
                    reinforce_link(link, amount=narr.weight * 0.15)

            # Contradicting evidence
            for contradicted in get_linked(narr, 'CONTRADICTS'):
                link = get_link(witness, 'BELIEVES', contradicted)
                if link:
                    challenge_link(link, amount=narr.weight * 0.20)
```

#### M3: Association

```python
def apply_association(moment):
    """
    Co-occurring narratives become linked.
    """
    current = moment.attached_narratives()

    # Recent narratives in same conversation
    recent = query("""
        MATCH (m:Moment)-[:THEN*1..3]->(current:Moment {id: $id})
        MATCH (m)-[:ATTACHED_TO]->(n:Narrative)
        WHERE m.tick > $threshold
        RETURN DISTINCT n
    """, id=moment.id, threshold=current_tick - 10)

    for a in current:
        for b in recent:
            if a.id != b.id:
                link = get_link(a, 'SUPPORTS', b)
                if link:
                    reinforce_link(link, amount=0.03)
                elif strength > 0.05:
                    create_link(a, 'SUPPORTS', b, strength=0.03)
```

---

### Action Processing

If moment has an action, Canon Holder triggers the action processor:

```python
def process_action(moment):
    """
    Execute world-changing action.
    """
    action = moment.action
    actor = moment.speaker
    target = get_action_target(moment)

    if action == 'travel':
        # Change AT link
        move_character(actor, target)

    elif action == 'take':
        # Change CARRIES link
        take_thing(actor, target)

    elif action == 'give':
        # Change CARRIES link
        give_thing(actor, target, recipient)

    elif action == 'attack':
        # Complex — may trigger combat
        initiate_combat(actor, target)

    elif action == 'use':
        # Thing-specific effects
        use_thing(actor, target)

    # Apply Commitment mechanic (M5)
    apply_commitment(actor, moment)
```

---

### Time Passage

```python
def estimate_moment_duration(moment):
    """
    How long does this moment take in game time?
    """
    base_minutes = {
        'dialogue': 0.5,
        'thought': 0.1,
        'action': 1.0,
        'narration': 0.2,
        'montage': 5.0
    }.get(moment.type, 0.5)

    # Adjust by text length
    words = len(moment.text.split())
    word_factor = 1 + (words / 50) * 0.5

    return base_minutes * word_factor


def advance_time(minutes):
    """
    Move game time forward.
    """
    game_state.current_time += timedelta(minutes=minutes)

    # Check for time-based events
    check_scheduled_events()

    # Decay check (large time jumps)
    if minutes > 30:
        run_decay_cycle()
```

---

### THEN Links

History chain. Created by Canon Holder, never manually.

```python
def create_then_link(previous, current):
    """
    Link moments in history.
    """
    create_link(previous, 'THEN', current, {
        'tick': current_tick,
        'player_caused': is_player_input(),
        'time_gap_minutes': time_between(previous, current)
    })
```

**Query pattern:** `MATCH (m1)-[:THEN*]->(m2)` for conversation history.

---

### Frontend Notification

```python
def push_to_display(moment):
    """
    Send moment to frontend for display.
    """
    payload = {
        'id': moment.id,
        'text': moment.text,
        'type': moment.type,
        'speaker': moment.speaker.name if moment.speaker else None,
        'tone': moment.tone,
        'clickable_words': extract_clickable(moment),
        'timestamp': game_state.current_time
    }

    websocket.send('moment', payload)
```

---

### Simultaneous Actions Are Drama

**Old thinking:** Aldric grabs sword + Mildred grabs sword = mutex = resolve conflict.

**New thinking:** Both actualize. Both canon.

```
"Aldric reaches for the sword."
"Mildred's hand closes on the hilt at the same moment."
```

That's not a problem. That's a scene. The consequences play out:
- Struggle moment generated
- Tension increases
- Drama emerges

Canon Holder does NOT block simultaneous actions. It records them both.

---

### True Mutex (Rare)

True mutex = logically impossible, not just dramatic.

#### Same Character, Incompatible Actions

```
Aldric "walks east" AND Aldric "walks west" (same tick)
```

This is impossible. Resolution:

```python
def detect_same_character_mutex(moments):
    """
    Find moments where same character has incompatible actions.
    """
    by_character = group_by_character(moments)

    conflicts = []
    for char_id, char_moments in by_character.items():
        action_moments = [m for m in char_moments if m.action]
        if len(action_moments) > 1:
            for a, b in combinations(action_moments, 2):
                if are_incompatible(a.action, b.action):
                    conflicts.append((a, b))

    return conflicts


def resolve_mutex(moment_a, moment_b):
    """
    Higher weight wins. Loser returns to potential.
    """
    winner, loser = (moment_a, moment_b) if moment_a.weight > moment_b.weight else (moment_b, moment_a)

    # Winner proceeds to canon
    record_to_canon(winner)

    # Loser returns to possible, decayed
    loser.status = 'possible'
    loser.weight *= 0.5
```

#### What's Incompatible

| Action A | Action B | Mutex? |
|----------|----------|--------|
| travel east | travel west | Yes |
| attack X | attack X | No (both attack) |
| take sword | take sword | No (drama: struggle) |
| speak | speak | No (both speak) |

Most "conflicts" are actually drama to embrace.

---

### History Is Queryable

THEN chains form traversable history.

```python
def get_character_history(character_id, limit=20):
    """
    What did this character witness?
    """
    return query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT $limit
    """, char_id=character_id, limit=limit)


def get_conversation_chain(moment_id):
    """
    Follow THEN links to reconstruct conversation.
    """
    return query("""
        MATCH path = (start:Moment {id: $id})-[:THEN*]->(end:Moment)
        RETURN nodes(path) AS moments
        ORDER BY length(path) DESC
        LIMIT 1
    """, id=moment_id)
```

The graph IS the log. No separate history storage.

---

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| `SURFACE_THRESHOLD` | 0.3 | salience (weight × energy) needed |
| `ACTUALIZATION_COST` | 0.6 | Partial energy drain on record |
| `MAX_MOMENTS_PER_TICK` | 5 | Rate limit |
| `MIN_MOMENT_GAP_MS` | 100 | Display pacing |

---

### Invariants

1. **Immutability:** Once `spoken`, a moment never changes status
2. **THEN chain:** Every `spoken` moment (except first) has exactly one incoming THEN link
3. **Time monotonic:** Game time only moves forward
4. **Rate limited:** Max 5 moments per tick
5. **Strength applied:** All three mechanics (Activation, Evidence, Association) run on every record
6. **Drama welcome:** Simultaneous actions are scenes, not conflicts

---

### What Canon Holder Does NOT Do

- Generate content (that's Handlers)
- Compute energy flow (that's Physics tick)
- Block drama (simultaneous actions are fine)
- Store tension (tension is computed)
- Decide what should happen (that's Physics + Handlers)

Canon Holder only: record, link, trigger, notify.

---

*"Canon Holder makes it real. Everything else is possibility."*


---

## Character Handlers

### Core Principle

**One handler per character. Triggered on flip. That's it.**

No arbitrary triggers. No cooldowns. No caps. The physics determines when handlers run.

---

### When Handlers Run

**On flip.** When a moment ATTACHED_TO this character crosses the flip threshold.

```python
def on_moment_flip(moment: Moment):
    """
    Called by Canon Holder when a moment flips.
    Triggers handler for the attached character.
    """
    character = query("""
        MATCH (m:Moment {id: $id})-[:ATTACHED_TO]->(c:Character)
        RETURN c
    """, id=moment.id)

    if character:
        run_handler(character.id, triggered_by=moment)
```

#### Why No Other Triggers

- Character important and close? → More energy per tick → flips more often → handler runs more
- Character distant or minor? → Less energy → flips rarely → handler runs rarely

**The physics IS the scheduling.**

No cooldowns needed. Handler produces moments with weight. Those moments exist in the graph. Until they actualize or decay, character has potentials.

If potentials depleted → character's moments have low weight → character keeps pumping into narratives → those narratives energize new moments → eventually something flips → handler runs.

---

### What Handler Receives

```python
@dataclass
class HandlerContext:
    character: Character          # Identity, beliefs, relationships, voice
    location: Place               # Where they are
    present: List[Character]      # Who else is here
    recent_history: List[Moment]  # Last N actualized moments they witnessed
    trigger: Moment               # What flipped to cause this run
    speed: SpeedSetting           # Current game speed (for prompt framing)
```

#### Context Assembly

```python
def build_handler_context(character_id: str, trigger: Moment) -> HandlerContext:
    character = get_character(character_id)
    location = get_character_location(character_id)
    present = get_characters_at(location.id)

    recent_history = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken DESC
        LIMIT 10
    """, char_id=character_id)

    return HandlerContext(
        character=character,
        location=location,
        present=present,
        recent_history=recent_history,
        trigger=trigger,
        speed=get_current_speed()
    )
```

---

### What Handler Produces

```python
@dataclass
class HandlerOutput:
    moments: List[MomentDraft]      # New potential moments
    links: List[LinkDraft]           # CAN_LEAD_TO, ATTACHED_TO, REFERENCES
    questions: List[str]             # Queries for Question Answerer
```

#### MomentDraft

```python
@dataclass
class MomentDraft:
    text: str                        # The content
    type: str                        # dialogue, thought, action, narration
    action: Optional[str]            # travel, take, attack, give (if action)
    tone: Optional[str]              # whispered, shouted, cold, warm
    # Note: NO weight field. Physics assigns weight.
```

#### Handler Does NOT Set Weight

Handler outputs text + links. Physics derives weight from:
- CAN_SPEAK link strength (set by handler based on relevance to trigger)
- Character's current energy
- ATTACHED_TO link strengths to narratives/characters

Weight = sum of (source.energy × link.strength). Energy IS proximity — no separate calculation.

No handler can "force" a high-weight moment. It proposes. Physics evaluates.

---

### Handler Implementation

```python
async def run_handler(character_id: str, triggered_by: Moment) -> HandlerOutput:
    """
    Run the character's handler. Returns new potentials.
    """
    context = build_handler_context(character_id, triggered_by)

    # Build prompt based on character type and speed
    prompt = build_handler_prompt(context)

    # LLM call
    response = await llm.complete(prompt)

    # Parse structured output
    output = parse_handler_response(response)

    # Inject into graph (physics assigns weights)
    inject_handler_output(character_id, output)

    return output
```

#### Prompt Framing by Speed

```python
def build_handler_prompt(context: HandlerContext) -> str:
    base = f"""
    You are {context.character.name}.
    {context.character.voice_description}

    Location: {context.location.name}
    Present: {', '.join(c.name for c in context.present)}

    What just happened: {context.trigger.text}
    Recent history: {format_history(context.recent_history)}

    Generate potential moments (things you might say, think, or do).
    """

    # Speed-aware framing
    if context.speed == '2x':
        base += """
        You're on a journey. Generate brief atmospheric moments,
        not full dialogue. Unless something important needs to be said.
        """
    elif context.speed == '3x':
        base += """
        Time is passing quickly. Only generate moments if something
        critical demands attention.
        """

    return base
```

---

### Moment Injection (Physics Side)

```python
def inject_handler_output(character_id: str, output: HandlerOutput):
    """
    Inject handler output into graph.

    Weight is derived from energy, not set directly.
    We set link strengths which determine energy flow → weight.
    See the Energy Mechanics section for full model.
    """
    character = get_character(character_id)

    for draft in output.moments:
        # Calculate link strength (how much character energy flows to this moment)
        relevance = calculate_relevance(draft, output.trigger)
        link_strength = max(0.3, min(0.9, relevance))

        # Create moment (weight will be computed by physics tick)
        moment_id = create_moment(
            text=draft.text,
            type=draft.type,
            action=draft.action,
            tone=draft.tone,
            weight=0.0,  # Derived, not set
            status='possible'
        )

        # Create CAN_SPEAK link (character energy → moment weight)
        create_link('CAN_SPEAK', character_id, moment_id, {
            'strength': link_strength
        })

        # Create ATTACHED_TO link
        create_link('ATTACHED_TO', moment_id, character_id, {
            'strength': link_strength,
            'presence_required': True,
            'persistent': True
        })

    # Process additional links
    for link in output.links:
        create_link(link.type, link.from_id, link.to_id, link.properties)

    # Queue questions for async answering
    for question in output.questions:
        question_answerer.queue(character_id, question)
```

---

### Handler Scaling

| Character Type | Handler Complexity |
|----------------|-------------------|
| Major (companions, antagonists) | Full LLM, rich context |
| Minor (named NPCs) | Lighter LLM, focused context |
| Grouped (guards, crowd) | Single handler for group |

#### Grouped Characters

"The Guards" can be a single character node until narrative needs differentiation.

```yaml
Character:
  id: char_guards
  name: "The Guards"
  type: group
```

They flip. Their handler runs. They act as one. 20 peasants = 1 handler, not 20 LLM calls.

#### Splitting Groups

Triggered by direct address or action targeting individual:

```python
def handle_direct_address(input_text: str, target: str):
    """
    Player addresses individual in a group.
    """
    # "You there, guard on the left!"
    if is_group_member_address(target):
        group = get_parent_group(target)
        individual = split_from_group(group, target)
        # individual now has own node, inherits group properties
```

Handler can also request split:

```python
## In handler output
{
    "split_request": {
        "from_group": "char_guards",
        "new_character": {
            "name": "The Tall Guard",
            "reason": "He steps forward, breaking ranks"
        }
    }
}
```

---

### Parallel Execution

Multiple flips = multiple parallel handler calls.

```python
async def process_flips(flipped_moments: List[Moment]):
    """
    Run handlers in parallel for all flipped moments.
    """
    tasks = []

    for moment in flipped_moments:
        character = get_attached_character(moment)
        if character:
            task = run_handler(character.id, triggered_by=moment)
            tasks.append(task)

    # Parallel execution
    results = await asyncio.gather(*tasks)

    # Each handler only writes its own character
    # No conflicts because of isolation
```

#### Why Parallel Is Safe

Each handler only writes for its character. Handler isolation is an invariant. No conflicts possible.

4 flips = 4 parallel LLM calls. Wall-clock time is ~one call, not four sequential.

---

### Reaction Scope

**Handlers only write for their own character.**

Aldric speaks. Mildred flinches. Who writes the flinch?

NOT Aldric's handler.

```
Aldric speaks (moment actualizes)
  → Energy propagates to Mildred (she witnessed, ATTACHED_TO link)
  → Her weight increases
  → She flips
  → Her handler runs
  → She generates flinch potential
  → Flinch may actualize
```

Each handler only writes its own character. Reactions propagate through energy.

---

### Pre-Generation Strategy

The graph should never be sparse for active characters.

```python
def on_character_enters_scene(character_id: str, location_id: str):
    """
    Pre-generate potentials when character enters.
    """
    # Create a synthetic "arrival" moment
    arrival = create_moment(
        text=f"{character.name} arrives.",
        type='narration',
        weight=0.5,
        status='active'
    )

    # Trigger handler with arrival as trigger
    run_handler(character_id, triggered_by=arrival)

    # By the time player engages, potentials exist
```

If truly novel (player says something completely unexpected):
- Energy flows → player character receives it (always present)
- Player character's handler runs
- "You're not sure anyone knows how to respond to that."

The player character is the fallback. They always have something.

---

### What Handler Does NOT Do

- Decide what actualizes (only proposes)
- Write for other characters (scope isolation)
- Modify world state directly (that's Action Processing)
- Set weights (that's Physics)

---

### Invariants

1. **Scope isolation:** Handler only writes for its character
2. **Triggered by flip:** No other triggers (physics is scheduler)
3. **No weight control:** Handler proposes, physics assigns weight
4. **Parallel safe:** Multiple handlers can run simultaneously

---

*"The physics IS the scheduling."*


---

## Action Processing

### Core Principle

**Moments with action fields modify world state.**

Everything is a moment. But moments with `action` field have consequences beyond display. They change the graph structure (AT links, health, possessions, relationships).

---

### Why Actions Are Special

| Moment Type | Affects Display | Affects Graph State |
|-------------|-----------------|---------------------|
| dialogue | Yes | No |
| thought | Yes | No |
| narration | Yes | No |
| action | Yes | **Yes** |

Physics doesn't distinguish — all propagate energy the same way.
Canon Holder doesn't distinguish — all get THEN links.
**Action Processing distinguishes** — only actions modify world state.

---

### Action Queue

Actions are processed sequentially to prevent conflicts.

```python
class ActionQueue:
    """
    Sequential queue for world-state-modifying actions.
    Order determined by canon arrival order.
    """
    def __init__(self):
        self.queue = []

    def add(self, moment: Moment):
        if moment.action:
            self.queue.append(moment)

    def process_next(self) -> Optional[ActionResult]:
        if not self.queue:
            return None

        moment = self.queue.pop(0)
        return process_action(moment)
```

---

### Action Processing Steps

```python
def process_action(moment: Moment) -> ActionResult:
    """
    Process a single action moment.
    """
    # 1. VALIDATE — Is action still possible?
    if not validate_action(moment):
        return ActionResult(
            success=False,
            moment=moment,
            reason="Action no longer valid"
        )

    # 2. EXECUTE — Modify graph state
    execute_action(moment)

    # 3. CONSEQUENCES — Generate consequence moments
    consequences = generate_consequences(moment)

    # 4. INJECT — Consequences enter graph with energy
    for consequence in consequences:
        inject_consequence(consequence)

    return ActionResult(success=True, moment=moment, consequences=consequences)
```

---

### Step 1: Validate

Check if action is still possible given current state.

```python
def validate_action(moment: Moment) -> bool:
    """
    Validate action against current world state.
    """
    action = moment.action
    actor = get_actor(moment)

    if action == 'travel':
        # Can actor travel to destination?
        destination = moment.action_target
        return can_travel_to(actor, destination)

    elif action == 'take':
        # Is thing still present and unowned?
        thing = moment.action_target
        return is_thing_available(thing, actor.location)

    elif action == 'attack':
        # Is target still present and alive?
        target = moment.action_target
        return is_target_attackable(target, actor)

    elif action == 'give':
        # Does actor have the thing? Is recipient present?
        thing = moment.action_target
        recipient = moment.action_recipient
        return actor_has_thing(actor, thing) and is_present(recipient, actor.location)

    return True
```

#### Why Validation?

Between canon recording and action processing, state may have changed:
- Another action executed first
- Time passed
- World event occurred

Validation catches stale actions.

---

### Step 2: Execute

Modify graph state based on action type.

```python
def execute_action(moment: Moment):
    """
    Execute the action — modify graph state.
    """
    action = moment.action
    actor = get_actor(moment)

    if action == 'travel':
        execute_travel(actor, moment.action_target)

    elif action == 'take':
        execute_take(actor, moment.action_target)

    elif action == 'attack':
        execute_attack(actor, moment.action_target)

    elif action == 'give':
        execute_give(actor, moment.action_target, moment.action_recipient)
```

#### Travel

```python
def execute_travel(actor: Character, destination_id: str):
    """
    Move character to new location.
    """
    # Remove old AT link
    query("""
        MATCH (c:Character {id: $char_id})-[r:AT]->(:Place)
        DELETE r
    """, char_id=actor.id)

    # Create new AT link
    query("""
        MATCH (c:Character {id: $char_id})
        MATCH (p:Place {id: $place_id})
        CREATE (c)-[:AT]->(p)
    """, char_id=actor.id, place_id=destination_id)

    # Handle moment dormancy (see ALGORITHM_Lifecycle.md)
    handle_location_change(actor.id, destination_id)
```

#### Take

```python
def execute_take(actor: Character, thing_id: str):
    """
    Character takes a thing.
    """
    # Remove thing's AT link
    query("""
        MATCH (t:Thing {id: $thing_id})-[r:AT]->(:Place)
        DELETE r
    """, thing_id=thing_id)

    # Create CARRIES link
    query("""
        MATCH (c:Character {id: $char_id})
        MATCH (t:Thing {id: $thing_id})
        CREATE (c)-[:CARRIES]->(t)
    """, char_id=actor.id, thing_id=thing_id)
```

#### Attack

```python
def execute_attack(actor: Character, target_id: str):
    """
    Character attacks target.
    """
    target = get_character(target_id)

    # Calculate damage (simplified)
    damage = calculate_damage(actor, target)

    # Update target health
    query("""
        MATCH (c:Character {id: $target_id})
        SET c.health = c.health - $damage
    """, target_id=target_id, damage=damage)

    # Check for death
    if target.health - damage <= 0:
        execute_death(target_id)

    # Update relationship
    query("""
        MATCH (a:Character {id: $actor_id})
        MATCH (t:Character {id: $target_id})
        MERGE (a)-[r:RELATIONSHIP]->(t)
        SET r.hostility = coalesce(r.hostility, 0) + 0.5
    """, actor_id=actor.id, target_id=target_id)
```

#### Give

```python
def execute_give(actor: Character, thing_id: str, recipient_id: str):
    """
    Character gives thing to recipient.
    """
    # Remove actor's CARRIES link
    query("""
        MATCH (c:Character {id: $actor_id})-[r:CARRIES]->(t:Thing {id: $thing_id})
        DELETE r
    """, actor_id=actor.id, thing_id=thing_id)

    # Create recipient's CARRIES link
    query("""
        MATCH (c:Character {id: $recipient_id})
        MATCH (t:Thing {id: $thing_id})
        CREATE (c)-[:CARRIES]->(t)
    """, recipient_id=recipient_id, thing_id=thing_id)
```

---

### Step 3: Generate Consequences

Actions produce consequence moments.

```python
def generate_consequences(moment: Moment) -> List[Moment]:
    """
    Generate consequence moments from action.
    """
    consequences = []
    action = moment.action
    actor = get_actor(moment)

    if action == 'travel':
        # Departure noticed
        consequences.append(create_consequence(
            text=f"{actor.name} leaves.",
            type='narration',
            attached_to=moment.location  # Old location
        ))
        # Arrival noticed
        consequences.append(create_consequence(
            text=f"{actor.name} arrives.",
            type='narration',
            attached_to=moment.action_target  # New location
        ))

    elif action == 'take':
        thing = get_thing(moment.action_target)
        consequences.append(create_consequence(
            text=f"{actor.name} takes the {thing.name}.",
            type='narration',
            attached_to=actor.id
        ))

    elif action == 'attack':
        target = get_character(moment.action_target)
        consequences.append(create_consequence(
            text=f"{actor.name} strikes at {target.name}.",
            type='action',
            attached_to=actor.id
        ))
        # Witness reactions will be generated by their handlers

    elif action == 'give':
        thing = get_thing(moment.action_target)
        recipient = get_character(moment.action_recipient)
        consequences.append(create_consequence(
            text=f"{actor.name} gives the {thing.name} to {recipient.name}.",
            type='narration',
            attached_to=actor.id
        ))

    return consequences
```

---

### Step 4: Inject Consequences

Consequence moments enter graph and may trigger further physics.

```python
def inject_consequence(consequence: Moment):
    """
    Inject consequence moment into graph.
    """
    # Create moment with initial energy
    moment_id = create_moment(
        text=consequence.text,
        type=consequence.type,
        weight=CONSEQUENCE_INITIAL_WEIGHT,  # e.g., 0.6
        status='possible'
    )

    # Create links
    create_link('ATTACHED_TO', moment_id, consequence.attached_to, {
        'presence_required': True,
        'persistent': False  # Consequences are ephemeral
    })

    # Physics takes over — consequence may flip, trigger handlers
```

---

### Mutex Handling

If two characters attempt same action on same target:

```python
def handle_action_mutex(action_a: Moment, action_b: Moment):
    """
    Two actions targeting same thing/character.
    First in queue succeeds, second gets blocked.
    """
    # First action already processed (it's first in queue)
    # Second action validation will fail

    # Generate "blocked" consequence
    actor_b = get_actor(action_b)
    blocked_consequence = create_consequence(
        text=f"{actor_b.name} reaches for it, but too late.",
        type='narration',
        attached_to=actor_b.id
    )

    inject_consequence(blocked_consequence)

    # Blocked consequence triggers actor_b's handler
    # Handler can generate reaction: frustration, new plan, etc.
```

---

### Action Types Reference

| Action | Modifies | Consequences |
|--------|----------|--------------|
| `travel` | Character AT links | Departure/arrival notices |
| `take` | Thing AT/CARRIES links | Observation moment |
| `attack` | Health, relationships | Strike moment, witness reactions |
| `give` | CARRIES links | Transfer observation |
| `speak` | Nothing (just moment) | None |

---

### Sequential Processing

Actions MUST be sequential.

```
Aldric grabs sword (action enters queue)
Mildred grabs sword (action enters queue)
    ↓
Process Aldric's action (succeeds, sword now CARRIED by Aldric)
    ↓
Process Mildred's action (validation fails, sword not available)
    ↓
Mildred gets "blocked" consequence
    ↓
Mildred's handler triggered (generates frustration/reaction)
```

This is not mutex detection — it's natural sequencing. First in queue wins.

---

### What Action Processing Does NOT Do

- Run in parallel (must be sequential)
- Generate dialogue (that's Handlers)
- Decide action priority (that's Canon order)

---

### Invariants

1. **Sequential execution:** One action at a time
2. **Validation first:** Check before execute
3. **Consequences propagate:** Actions generate observable moments
4. **State consistency:** No conflicting graph modifications

---

*"Actions are where moments change the world."*


---

## Player Input Processing

### Core Principle

**Player input is a perturbation, not an ignition.**

The graph is already running. Player input adds energy. Energy propagates. Things flip. This is not "starting a cascade" — it's perturbing a living system.

---

### Input Flow

```
Player submits text
    ↓
[SEQUENTIAL] Parse, create moment, link, inject
    ↓
[PHYSICS] Energy spreads through links
    ↓
[PHYSICS] Tick detects flips
    ↓
[CANON] Records, emits to display
    ↓
[PARALLEL] Character handlers triggered
```

---

### Step 1: Parse

Extract references from input text (names, places, things).

```python
def parse_input(text: str, context: SceneContext) -> ParseResult:
    """
    Extract references (names, places, things).
    UI may have already assisted with autocomplete.
    """
    references = []

    # Character names
    for char in context.present_characters:
        if char.name.lower() in text.lower():
            references.append(Reference(type='character', id=char.id, name=char.name))
        # Also check nicknames, titles
        for alias in char.aliases:
            if alias.lower() in text.lower():
                references.append(Reference(type='character', id=char.id, name=alias))

    # Place names
    if context.location.name.lower() in text.lower():
        references.append(Reference(type='place', id=context.location.id, name=context.location.name))

    # Thing names
    for thing in context.visible_things:
        if thing.name.lower() in text.lower():
            references.append(Reference(type='thing', id=thing.id, name=thing.name))

    return ParseResult(text=text, references=references)
```

#### UI-Assisted Recognition

Recognition happens at input time, not query time.

```
Player types: "Al"
    ↓
UI shows dropdown: "Aldric"
    ↓
Player selects
    ↓
Text shows: "Aldric" (highlighted)
    ↓
Reference already recognized before submit
```

Direct address strengthens the energy link. "Aldric, what do you think?" hits harder than "What does everyone think?"

---

### Step 2: Create Moment

Create a moment node for the player's input.

```python
def create_player_moment(parsed: ParseResult, player: Character, location: Place) -> Moment:
    """
    Create moment for player's speech.
    """
    moment_id = generate_id('moment')

    query("""
        CREATE (m:Moment {
            id: $id,
            text: $text,
            type: 'dialogue',
            status: 'spoken',
            weight: 1.0,
            tick_created: $tick,
            tick_spoken: $tick
        })
    """, id=moment_id, text=parsed.text, tick=current_tick())

    return get_moment(moment_id)
```

Player moments are immediately `spoken` (canon). They're not potentials — the player said them.

---

### Step 3: Create Links

Link the moment to relevant nodes.

```python
def create_input_links(moment: Moment, parsed: ParseResult, context: SceneContext):
    """
    Create links from player moment to relevant nodes.
    """
    # ATTACHED_TO player (they said it)
    create_link('ATTACHED_TO', moment.id, context.player.id, {
        'presence_required': False,
        'persistent': True
    })

    # ATTACHED_TO current location
    create_link('ATTACHED_TO', moment.id, context.location.id, {
        'presence_required': False,
        'persistent': True
    })

    # ATTACHED_TO all present characters (they heard it)
    for char in context.present_characters:
        create_link('ATTACHED_TO', moment.id, char.id, {
            'presence_required': False,
            'persistent': True
        })

    # REFERENCES for recognized names/things (strong energy transfer)
    for ref in parsed.references:
        create_link('REFERENCES', moment.id, ref.id, {
            'weight': 1.0  # Direct reference = strong link
        })

    # CAN_SPEAK link (player spoke this)
    create_link('CAN_SPEAK', context.player.id, moment.id, {
        'weight': 1.0
    })
```

---

### Step 4: Inject Energy

Add energy to the system based on input.

```python
def inject_input_energy(moment: Moment, parsed: ParseResult, context: SceneContext):
    """
    Player input injects energy. Referenced nodes receive based on strength.
    """
    base_energy = INPUT_ENERGY_BASE  # e.g., 0.5

    # Direct references get full energy
    for ref in parsed.references:
        if ref.type == 'character':
            # Boost all moments attached to this character
            query("""
                MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
                WHERE m.status = 'possible'
                SET m.weight = m.weight + $energy
            """, char_id=ref.id, energy=base_energy)

    # All present characters get partial energy (they heard)
    for char in context.present_characters:
        if char.id not in [r.id for r in parsed.references]:
            query("""
                MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $char_id})
                WHERE m.status = 'possible'
                SET m.weight = m.weight + $energy
            """, char_id=char.id, energy=base_energy * 0.3)
```

#### Names Have Power

```python
## "Aldric, what do you think?"
## Aldric directly referenced → full energy boost

## "What does everyone think?"
## No direct reference → distributed partial energy
```

Direct address targets energy. Indirect speech diffuses it.

---

### Step 5: Trigger Physics

After injection, physics takes over.

```python
def process_input(text: str):
    """
    Full input processing pipeline.
    """
    context = get_current_scene_context()

    # 1. Parse
    parsed = parse_input(text, context)

    # 2. Create moment
    moment = create_player_moment(parsed, context.player, context.location)

    # 3. Create links
    create_input_links(moment, parsed, context)

    # 4. Inject energy
    inject_input_energy(moment, parsed, context)

    # 5. Emit player moment to display (immediate)
    display_queue.add(moment)

    # 6. Trigger physics tick (may be immediate based on settings)
    physics.tick()

    return moment
```

---

### Energy Must Land

When energy enters, it must go somewhere.

```python
def ensure_energy_lands(context: SceneContext):
    """
    If no moments flip after input, energy returns to player character.
    Player character always has a handler → something always happens.
    """
    # After physics tick, check if anything flipped
    if not any_moments_flipped():
        # No response from NPCs
        # Energy flows back to player character
        player_fallback_energy = FALLBACK_ENERGY

        query("""
            MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $player_id})
            WHERE m.status = 'possible'
            SET m.weight = m.weight + $energy
        """, player_id=context.player.id, energy=player_fallback_energy)

        # Player character's handler will produce observation
        # "The silence stretches. No one meets your eye."
```

There is no "nothing happens." There is only "the silence stretches."

---

### Auto-Pause on Input

At any speed, typing auto-pauses or auto-drops to 1x.

```python
def on_input_start():
    """
    Player began typing. Pause or slow down.
    """
    if current_speed() in ['2x', '3x']:
        set_speed('1x')
        # Or: pause until submit
```

Player can resume speed after input processed.

---

### What Input Processing Does NOT Do

- Generate NPC responses (that's Handlers)
- Decide what happens (that's Physics + Canon)
- Block on LLM (input creates moment immediately)

---

### Invariants

1. **Immediate moment creation:** Player input becomes moment instantly
2. **Energy injection:** Input always adds energy to system
3. **Something happens:** Energy must land somewhere (player fallback)
4. **Direct address matters:** Named references get more energy

---

*"Player input is a perturbation, not an ignition."*


---

## Question Answering

### Core Principle

**When a handler queries the graph and gets sparse results, invent the missing information.**

Question Answering fills gaps in world knowledge. It creates backstory, relationships, and history that didn't exist until needed.

---

### When Questions Arise

Handler asks a question. Graph returns sparse/nothing.

```python
## In character handler
def generate_response(context: HandlerContext):
    # Handler needs to know about father
    father_info = query_graph("Who is my father?", context.character.id)

    if father_info.is_sparse():
        # Queue question for answering
        question_answerer.queue(
            asker=context.character.id,
            question="Who is my father?",
            context=context
        )
        # Handler continues with what it knows
        # Does NOT block waiting for answer
```

---

### Not Async in "Fire and Forget" Sense

The session runs until it completes. It produces nodes. Nodes enter graph with initial weight.

```
Handler runs
  → asks "Who is my father?"
  → Question Answerer session starts (parallel)
  → Handler continues with what it knows
  → Handler finishes, outputs potentials
  → Later: QA completes, injects nodes with energy
  → Those nodes propagate naturally via physics
```

Handler never waits for QA. QA is fire-and-complete, not fire-and-wait.

---

### Question Answerer Flow

```python
async def answer_question(asker_id: str, question: str, context: dict):
    """
    Answer a question by inventing consistent information.
    Session runs until complete, then injects results.
    """
    # 1. GATHER — Get relevant existing facts
    existing = gather_relevant_facts(asker_id, question)

    # 2. GENERATE — Invent answer via LLM
    answer = await generate_answer(question, existing, context)

    # 3. VALIDATE — Check consistency
    if not validate_consistency(answer, existing):
        answer = await regenerate_with_constraints(question, existing, answer.conflicts)

    # 4. INJECT — Create nodes in graph
    inject_answer(asker_id, question, answer)
```

---

### Step 1: Gather Existing Facts

Query graph for anything relevant to constrain the answer.

```python
def gather_relevant_facts(asker_id: str, question: str) -> ExistingFacts:
    """
    Find existing information that constrains the answer.
    """
    asker = get_character(asker_id)

    facts = ExistingFacts()

    # Character's existing family
    facts.family = query("""
        MATCH (c:Character {id: $id})-[:FAMILY*1..2]-(relative:Character)
        RETURN relative
    """, id=asker_id)

    # Character's origin place
    facts.origin = query("""
        MATCH (c:Character {id: $id})-[:FROM]->(p:Place)
        RETURN p
    """, id=asker_id)

    # Character's existing beliefs/narratives
    facts.beliefs = query("""
        MATCH (c:Character {id: $id})-[:BELIEVES]->(n:Narrative)
        RETURN n
    """, id=asker_id)

    # Historical events character witnessed
    facts.history = query("""
        MATCH (m:Moment)-[:ATTACHED_TO]->(c:Character {id: $id})
        WHERE m.status = 'spoken'
        RETURN m
        ORDER BY m.tick_spoken
        LIMIT 20
    """, id=asker_id)

    return facts
```

---

### Step 2: Generate Answer

Use LLM to invent consistent answer.

```python
async def generate_answer(question: str, existing: ExistingFacts, context: dict) -> Answer:
    """
    Generate answer using LLM.
    """
    prompt = f"""
    A character in Norman England (1067) is wondering: "{question}"

    Existing facts about this character:
    - Family: {format_family(existing.family)}
    - Origin: {existing.origin}
    - Beliefs: {format_beliefs(existing.beliefs)}
    - Recent history: {format_history(existing.history)}

    Invent an answer that:
    1. Does NOT contradict any existing facts
    2. Fits the historical setting (Norman Conquest era)
    3. Creates potential for drama
    4. Feels specific and real, not generic

    Return structured output:
    - New characters (if any): name, relationship, status (alive/dead), traits
    - New places (if any): name, type, relationship to character
    - New events (if any): what happened, when, who was involved
    - Potential moments: memories that could surface
    """

    response = await llm.complete(prompt)
    return parse_answer(response)
```

---

### Step 3: Validate Consistency

Check that invented information doesn't contradict existing graph.

```python
def validate_consistency(answer: Answer, existing: ExistingFacts) -> bool:
    """
    Ensure answer doesn't contradict existing facts.
    """
    # Check family conflicts
    for new_char in answer.new_characters:
        if new_char.relationship == 'father':
            existing_father = find_existing_father(existing.family)
            if existing_father and existing_father.id != new_char.id:
                return False  # Conflict: already has different father

    # Check place conflicts
    for new_place in answer.new_places:
        if new_place.relationship == 'birthplace':
            existing_origin = existing.origin
            if existing_origin and existing_origin.id != new_place.id:
                return False  # Conflict: already has different origin

    # Check temporal conflicts
    for new_event in answer.new_events:
        if conflicts_with_history(new_event, existing.history):
            return False

    return True
```

---

### Step 4: Inject Answer

Create nodes in graph with initial energy.

```python
def inject_answer(asker_id: str, question: str, answer: Answer):
    """
    Inject answer into graph. Physics takes over from here.
    """
    # Create new character nodes
    for new_char in answer.new_characters:
        char_id = create_character(
            name=new_char.name,
            status=new_char.status,
            traits=new_char.traits
        )

        # Create relationship link
        create_link('FAMILY', asker_id, char_id, {
            'relationship': new_char.relationship
        })

    # Create new place nodes
    for new_place in answer.new_places:
        place_id = create_place(
            name=new_place.name,
            type=new_place.type
        )

        # Create relationship link
        create_link('FROM', asker_id, place_id, {
            'relationship': new_place.relationship
        })

    # Create potential memory moments
    for memory in answer.potential_moments:
        moment_id = create_moment(
            text=memory.text,
            type='thought',
            weight=ANSWER_INITIAL_WEIGHT,  # e.g., 0.4
            status='possible'
        )

        create_link('ATTACHED_TO', moment_id, asker_id, {
            'presence_required': True,
            'persistent': True
        })

    # Create ANSWERED_BY link for traceability
    question_moment = create_moment(
        text=f"[Question: {question}]",
        type='meta',
        weight=0.0,  # Not for display
        status='answered'
    )

    for node_id in answer.all_created_node_ids():
        create_link('ANSWERED_BY', question_moment, node_id, {})
```

---

### No Special Mechanism for Integration

The answer doesn't "boost" anything specially. It creates nodes. Nodes have energy. Energy propagates. That's it.

```python
## After injection, physics handles integration:

## New father character exists
## Memory moments attached to asker exist
## These have initial weight (e.g., 0.4)

## Next tick:
## - Energy propagates through FAMILY links
## - Memory moments may get boosted if relevant
## - If weight crosses threshold, memory surfaces

## No special "integrate answer" logic
## Just physics
```

If the answer is relevant, its energy reaches relevant moments. If not, it decays like everything else.

---

### Constraints

Invented information must:

| Constraint | Why |
|------------|-----|
| Not contradict existing graph | Consistency |
| Fit established facts | Coherence |
| Fit historical setting | Immersion |
| Create potential drama | Gameplay value |
| Be specific, not generic | Memorability |

---

### Example: "Who is my father?"

```
Handler for Aldric asks: "Who is my father?"
Graph returns: nothing (sparse)

Question Answerer runs:

Existing facts:
- Aldric is Saxon
- Aldric is from York
- Aldric has a brother (Edmund)
- Aldric witnessed the Norman invasion

Generated answer:
- New character: Wulfstan (father, deceased)
  - Traits: blacksmith, stubborn, proud
  - Death: killed defending York against Normans
- New moment: "Father's hammer still hangs in the forge."
- New moment: "He said 'never bow' the day before they came."

Injected:
- Character node: char_wulfstan
- FAMILY link: Aldric -> Wulfstan (father)
- Moment: "Father's hammer..." (weight 0.4, possible)
- Moment: "He said 'never bow'..." (weight 0.4, possible)
- ANSWERED_BY links for traceability

Later:
- Conversation touches on fathers
- Energy propagates to Aldric's moments
- Memory crosses threshold
- Aldric says: "He said 'never bow' the day before they came."
```

---

### What Question Answerer Does NOT Do

- Block handlers (they continue without waiting)
- Force moments to surface (physics decides)
- Override existing facts (must be consistent)
- Generate dialogue directly (creates potentials)

---

### Invariants

1. **Non-blocking:** Handlers never wait for answers
2. **Consistency:** Answers cannot contradict existing graph
3. **Physics integration:** No special boost, just node injection
4. **Traceability:** ANSWERED_BY links track what was invented

---

*"The answer doesn't boost anything specially. It creates nodes. Nodes have energy. That's it."*


---
