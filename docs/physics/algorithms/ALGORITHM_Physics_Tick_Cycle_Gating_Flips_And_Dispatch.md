# Physics — Algorithm: Tick Cycle Gating Flips And Dispatch

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
THIS:           ALGORITHM_Physics_Tick_Cycle_Gating_Flips_And_Dispatch.md (you are here)
SCHEMA:         ../../schema/SCHEMA_Moments.md
VALIDATION:     ../VALIDATION_Physics.md
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## FULL TICK CYCLE

```python
def energy_tick():
    """
    Complete energy cycle. Order matters.
    """

    # 1. Characters pump into narratives
    for char in graph.characters:
        character_tick(char)

    # 2. Narrative-to-narrative transfer
    for link in graph.narrative_links:
        if link.type == 'CONTRADICTS':
            transfer_contradiction(link)
        elif link.type == 'SUPPORTS':
            transfer_support(link)
        elif link.type == 'ELABORATES':
            transfer_elaboration(link)
        elif link.type == 'SUBSUMES':
            transfer_subsumption(link)
        elif link.type == 'SUPERSEDES':
            transfer_supersession(link)

    # 3. ABOUT links (focal point pulls)
    for link in graph.about_links:
        transfer_about(link)

    # 4. Moment energy flow
    for link in graph.can_speak_links:
        transfer_can_speak(link)

    for link in graph.attached_to_links:
        transfer_attached_to(link)

    for link in graph.can_lead_to_links:
        transfer_can_lead_to(link)

    # 5. Tension injection (structural pressure)
    tensions = detect_tensions()
    tension_injection(tensions)

    # 6. Decay (energy leaves system)
    apply_decay()

    # 7. Detect breaks
    breaks = [t for t in tensions if is_unsustainable(t)]

    return breaks


def apply_decay():
    """
    Energy decays from all nodes.
    Weight decays much slower, only without reinforcement.
    """
    # Energy decay (fast)
    for narrative in graph.narratives:
        rate = ENERGY_DECAY_RATE  # 0.02
        if narrative.type in ['oath', 'blood', 'debt']:
            rate *= 0.25
        narrative.energy *= (1 - rate)
        narrative.energy = max(narrative.energy, MIN_ENERGY)

    for character in graph.characters:
        character.energy *= (1 - ENERGY_DECAY_RATE)
        character.energy = max(character.energy, MIN_ENERGY)

    for moment in graph.moments:
        rate = get_moment_decay_rate(moment.status)
        moment.energy *= (1 - rate)
        moment.energy = max(moment.energy, MIN_ENERGY)

        # Check for status transition
        if moment.status == 'possible' and moment.energy < DECAY_THRESHOLD:
            moment.status = 'decayed'

    # Weight decay (slow, only without reinforcement)
    for node in graph.all_weighted_nodes:
        if current_tick - node.last_reinforced > WEIGHT_DECAY_DELAY:
            node.weight *= (1 - WEIGHT_DECAY_RATE)  # 0.001
            node.weight = max(node.weight, MIN_WEIGHT)


def get_moment_decay_rate(status):
    return {
        'possible': 0.02,
        'active': 0.01,
        'spoken': 0.03,
        'dormant': 0.005,
        'decayed': 0.0
    }.get(status, 0.02)
```

---

## PHYSICAL GATING

Physical presence is not "proximity." It's a binary gate.

### How It Works

**Link attribute:** `presence_required: bool` on ATTACHED_TO

**Location:** `AT` link from Character to Place

### Gating Queries

**Can this moment actualize here?**

```cypher
MATCH (m:Moment {id: $moment_id})-[r:ATTACHED_TO {presence_required: true}]->(target)
OPTIONAL MATCH (target)-[:AT]->(p:Place)
WITH m, target, p
WHERE p IS NULL OR p.id = $current_place
RETURN count(*) = 0 AS blocked
```

If any `presence_required` target is not at current place → moment cannot actualize.

**Can these characters interact?**

```cypher
MATCH (a:Character {id: $char_a})-[:AT]->(p:Place)<-[:AT]-(b:Character {id: $char_b})
RETURN p IS NOT NULL AS can_interact
```

Same place → can interact. Different places → cannot.

### What This Replaces

| Old Concept | New Reality |
|-------------|-------------|
| `physical_proximity(a, b)` | Graph query on AT links |
| `narrative_proximity(n, focus)` | **Deleted** — energy IS proximity |
| `compute_focus(scene)` | **Deleted** — energy injection handles it |
| `can_actualize(moment)` | Query presence_required attachments |
| `can_interact(a, b)` | Query AT links |

### Example

```yaml
Moment:
  id: moment_aldric_confession
  text: "I need to tell you something about Edmund."

ATTACHED_TO:
  - target: char_aldric
    presence_required: true   # Aldric must be here
  - target: narr_edmund_secret
    presence_required: false  # Narrative doesn't need to be "present"
```

Aldric at camp, player at camp → moment can actualize.
Aldric in York, player at camp → moment blocked.

No function call. Graph structure encodes the rule.

---

## PARAMETERS

### Transfer Factors

| Link Type | Factor | Direction | Notes |
|-----------|--------|-----------|-------|
| CONTRADICTS | 0.15 * 2 | Bidirectional | High conductivity |
| SUPPORTS | 0.10 | Equilibrating | Allies share fate |
| ELABORATES | 0.15 | Parent → Child | Details inherit |
| SUBSUMES | 0.10 | Specific → General | Many feed one |
| SUPERSEDES | 0.25 | Old → New + drain | Replacement |
| ABOUT | 0.05 | Narrative → Subject | Being talked about |
| CAN_LEAD_TO | 0.15 | Origin → Destination | Conversation flow |
| CAN_SPEAK | 0.10 | Character → Moment | Speech potential |
| ATTACHED_TO | 0.10 | Target → Moment (reverse) | Relevance inheritance |

### Moment Decay Rates

| Status | Decay Rate | Notes |
|--------|------------|-------|
| `possible` | 0.02 | Unused possibilities fade |
| `active` | 0.01 | Something is happening |
| `spoken` | 0.03 | Done, recedes into past |
| `dormant` | 0.005 | Waiting to reactivate |

### Actualization

| Parameter | Value | Notes |
|-----------|-------|-------|
| ACTUALIZATION_COST | 0.6 | Partial drain on flip |

### Source Rates

| Source | Rate | Notes |
|--------|------|-------|
| Character pumping | 0.10 * energy | Per tick, distributed by belief strength |
| Origination bonus | *1.5 | Authors care more |
| Secret holding bonus | *1.2 | Secrets held tighter |
| Player focus | 1.0 | Per input, split across targets |
| Arrival boost | 0.5 | Character enters scene |
| News injection | 0.3 | Information arrives |
| Discovery injection | 0.5 | Something revealed |

### Sink Rates

| Sink | Rate | Notes |
|------|------|-------|
| Energy decay (narratives) | 0.02 | Per tick |
| Energy decay (core types) | 0.005 | Oaths, blood, debts (*0.25) |
| Energy decay (characters) | 0.02 | Per tick |
| Weight decay | 0.001 | Only after WEIGHT_DECAY_DELAY ticks without reinforcement |
| Actualization cost | 0.6 * energy | When moment flips |

### Weight Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| WEIGHT_DECAY_DELAY | 100 | Ticks before weight starts decaying |
| WEIGHT_DECAY_RATE | 0.001 | Very slow |
| MIN_WEIGHT | 0.01 | Never fully zero |
| SURFACE_THRESHOLD | 0.3 | salience (weight * energy) needed to surface |

### Floors & Ceilings

| Parameter | Value | Why |
|-----------|-------|-----|
| MIN_ENERGY | 0.01 | Never fully zero — can always revive |
| MIN_WEIGHT | 0.01 | Never fully zero — can always matter again |
| MAX_CHARACTER_ENERGY | 10.0 | Prevent runaway accumulation |
| MAX_NARRATIVE_ENERGY | 5.0 | Keep narratives bounded |
| MAX_MOMENT_ENERGY | 5.0 | Keep moments bounded |

---

## EMERGENT BEHAVIORS

### "Arguments Heat Both Sides"

Not because CONTRADICTS creates energy.

Because:
1. Aldric pumps into "Edmund betrayed us"
2. Edmund pumps into "I was right"
3. CONTRADICTS transfers between them (zero-sum)
4. Both stay hot because both have pumps

If Edmund dies → no pump → his side cools → argument fades.

### "Approach Creates Tension"

Not because we compute proximity. Because physical presence changes who pumps where.

1. Player travels toward York
2. Player arrives at York (AT link changes)
3. Edmund is now present (same location)
4. Edmund pumps into his narratives locally
5. Player's attention on Edmund → energy injection
6. Edmund's narratives heat up (via ABOUT reverse flow)
7. Contradiction with player's beliefs gets energy from both sides
8. Structural tension detected (both believers present + hot narratives)
9. Break becomes inevitable

**The AT link changing is the trigger.** Energy flow does the rest.

### "Forgotten Things Bite Back"

Not because hidden timer. Because neglected narratives still get pumped.

1. Debt narrative exists
2. Creditor pumps into it (constant, from their belief)
3. Player doesn't pump (doesn't believe it strongly, or doesn't think about it)
4. But creditor keeps pumping → narrative stays warm
5. Creditor travels toward player (AT link changes)
6. Now both present → can interact
7. Tension detection finds: debt narrative hot + creditor present + debtor present
8. Break: creditor demands payment

**You can't make someone else stop caring by ignoring them.**

### "The World Feels Alive"

Not because NPCs have complex AI.

Because:
1. Every character pumps into what they believe
2. Energy flows through narrative network
3. Tensions emerge from structure
4. Moments surface based on weight
5. The system has its own metabolism

No one decided "now is dramatic." The structure created drama.

### "Thinking About Someone Far Away"

Not proximity calculation. Energy injection.

1. Player says "I wonder what Aldric is doing"
2. Input parser detects reference to char_aldric
3. Energy injected into char_aldric
4. Aldric's energy flows to narratives about him (ABOUT reverse)
5. Those narratives surface (high energy = high weight moments)
6. Player "thinks about" Aldric — his stories come to mind

Aldric isn't "closer." His narratives are hotter. Same effect, no proximity concept.

---

## M11: FLIP DETECTION

Physics tick detects when moments cross the salience threshold. Canon Holder records them.

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

### Detection Query

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

### Processing Multiple Ready Moments

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

### Speaker Resolution

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

## M12: CANON HOLDER

**Everything is moments. Canon Holder is the gatekeeper.**

Canon Holder records what becomes real. It doesn't decide what happens — physics and handlers do that. Canon Holder makes it permanent.

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

### Canon Holder Responsibilities

| Responsibility | What It Does |
|----------------|--------------|
| **Record** | Flip moment `active` → `spoken` |
| **Link** | Create THEN link to previous moment |
| **Time** | Advance game time based on moment duration |
| **Trigger** | Process actions (travel, take, etc.) |
| **Strength** | Apply strength mechanics (Activation, Evidence, etc.) |
| **Notify** | Push to frontend |

### Recording Function

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

### Strength Mechanics on Record

Canon Holder triggers three of the six strength mechanics:

#### M1: Activation

```python
def apply_activation(moment):
    """Speaker's beliefs reinforced by speaking."""
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
    """Witnesses' beliefs affected by what they saw."""
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
    """Co-occurring narratives become linked."""
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

### Time Passage

```python
def estimate_moment_duration(moment):
    """How long does this moment take in game time?"""
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
    """Move game time forward."""
    game_state.current_time += timedelta(minutes=minutes)

    # Check for time-based events
    check_scheduled_events()

    # Decay check (large time jumps)
    if minutes > 30:
        run_decay_cycle()
```

### Action Processing

```python
def process_action(moment):
    """Execute world-changing action."""
    action = moment.action
    actor = moment.speaker
    target = get_action_target(moment)

    if action == 'travel':
        move_character(actor, target)

    elif action == 'take':
        take_thing(actor, target)

    elif action == 'give':
        give_thing(actor, target, recipient)

    elif action == 'attack':
        initiate_combat(actor, target)

    elif action == 'use':
        use_thing(actor, target)

    # Apply Commitment mechanic (M5)
    apply_commitment(actor, moment)
```

### THEN Links

History chain. Created by Canon Holder, never manually.

```python
def create_then_link(previous, current):
    """Link moments in history."""
    create_link(previous, 'THEN', current, {
        'tick': current_tick,
        'player_caused': is_player_input(),
        'time_gap_minutes': time_between(previous, current)
    })
```

**Query pattern:** `MATCH (m1)-[:THEN*]->(m2)` for conversation history.

### Frontend Notification

```python
def push_to_display(moment):
    """Send moment to frontend for display."""
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

### True Mutex (Rare)

True mutex = logically impossible, not just dramatic.

#### Same Character, Incompatible Actions

```
Aldric "walks east" AND Aldric "walks west" (same tick)
```

This is impossible. Resolution:

```python
def detect_same_character_mutex(moments):
    """Find moments where same character has incompatible actions."""
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
    """Higher weight wins. Loser returns to potential."""
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

### What Canon Holder Does NOT Do

- Generate content (that's Handlers)
- Compute energy flow (that's Physics tick)
- Block drama (simultaneous actions are fine)
- Store tension (tension is computed)
- Decide what should happen (that's Physics + Handlers)

Canon Holder only: record, link, trigger, notify.

---

## M13: AGENT DISPATCH

Four agents at three levels.

### The Agents

| Agent | Level | Responsibility | Timing |
|-------|-------|----------------|--------|
| **Runner** | World | Pressure, time, events, breaks | Tick-based |
| **Narrator** | Scene | Architecture, backstory, consequences | On demand |
| **Citizen** | Character | Dialogue, thoughts, freeform | Parallel async |
| **Canon Holder** | Record | Makes moments canon, THEN links | On flip |

### Runner (World)

```python
async def runner_tick():
    energy_tick()

    # Detect and process breaks
    tensions = detect_tensions()
    breaks = [t for t in tensions if is_unsustainable(t)]

    while breaks:
        for tension in breaks:
            await narrator_break(tension)  # Narrator generates consequences
        tensions = detect_tensions()
        breaks = [t for t in tensions if is_unsustainable(t)]

    # Scheduled events
    for event in get_due_events(current_tick):
        inject_event(event)

    update_travel_progress()
    check_time_transitions()
```

### Narrator (Scene)

```python
async def narrator_backstory(query_moment):
    """Query moment spoken → generate backstory."""
    character = get_attached_character(query_moment)
    result = await llm(backstory_prompt(character, query_moment.query))

    narrative = create_narrative(result.fact)
    create_link(character, 'BELIEVES', narrative, strength=0.8)
    create_link(character, 'ORIGINATED', narrative, strength=0.9)

    for memory in result.memories:
        m = create_moment(memory, status='dormant')
        attach(m, character)
        attach(m, narrative)
        create_link(query_moment, 'ANSWERED_BY', m)

    query_moment.query_filled = True


async def narrator_break(tension):
    """Tension broke → generate consequences."""
    result = await llm(break_prompt(tension))

    for consequence in result.consequences:
        create_moment(consequence, status='possible', weight=0.7, energy=0.9)
```

### Citizen (Character)

```python
async def citizen_respond(character, player_input):
    """Player addressed this character."""
    identity = build_character_context(character)
    result = await llm(respond_prompt(character, identity, player_input))

    m = create_moment(result.text, type='dialogue', status='possible', weight=0.6, energy=0.8)
    create_link(character, 'CAN_SPEAK', m, strength=0.9)
    return m


async def citizen_think(character):
    """Background thinking."""
    identity = build_character_context(character)
    drives = get_character_drives(character)
    result = await llm(think_prompt(character, identity, drives))

    for thought in result.thoughts:
        m = create_moment(thought.text, type=thought.type, status='possible', weight=0.3, energy=0.4)
        create_link(character, 'CAN_SPEAK', m, strength=0.7)


async def citizen_react(character, witnessed_moment):
    """Witnessed something → react."""
    result = await llm(react_prompt(character, witnessed_moment))

    if result.reacts:
        m = create_moment(result.text, status='possible', weight=0.4, energy=0.6)
        create_link(character, 'CAN_SPEAK', m, strength=0.8)
```

### Main Loop

```python
async def main_loop():
    while game_running:
        await runner_tick()

        ready = detect_ready_moments()
        for moment in ready[:MAX_MOMENTS_PER_TICK]:
            speaker = determine_speaker(moment)

            if moment.needs_generation:
                await narrator_fill_text(moment)
            if moment.query and not moment.query_filled:
                await narrator_backstory(moment)

            record_to_canon(moment, speaker, previous)
            previous = moment

            for witness in get_witnesses(moment, exclude=speaker):
                asyncio.create_task(citizen_react(witness, moment))

        if tempo.should_generate_more():
            for char in get_present_characters():
                asyncio.create_task(citizen_think(char))

        await asyncio.sleep(TICK_INTERVAL)


def on_player_input(text):
    matches = semantic_match(text)
    if matches:
        for m, score in matches:
            m.energy += score * 0.5
        return

    responder = select_responder(get_present_characters(), text)
    asyncio.create_task(citizen_respond(responder, text))
```

---

## WHAT WE DON'T DO

| Anti-pattern | Why Avoid |
|--------------|-----------|
| Set energy directly | Energy emerges from structure |
| Create energy from links | Violates conservation, unpredictable |
| Compute proximity separately | Energy IS proximity |
| Use functions for physical gating | Link attributes (presence_required, AT) |
| Arbitrary dampening | Hides broken dynamics |
| Magic thresholds | "0.7" means nothing without structure |
| Author tensions | Tensions emerge, aren't declared |

---

*"Characters pump. Links route. Decay drains. Energy IS proximity. The story emerges."*


---
