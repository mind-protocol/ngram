# ngram Graph System — Behaviors: Observable Effects of Graph-Driven Development

```
STATUS: DESIGNING
CREATED: 2024-12-23
VERIFIED: not yet
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Ngram_Graph_System.md
THIS:            BEHAVIORS_Ngram_Graph_System.md (you are here)
PATTERNS:        ./PATTERNS_Ngram_Graph_System.md
ALGORITHM:       ./ALGORITHM_Ngram_Graph_System.md
VALIDATION:      ./VALIDATION_Ngram_Graph_System.md
HEALTH:          ./HEALTH_Ngram_Graph_System.md
IMPLEMENTATION:  (engine/physics/, engine/infrastructure/orchestration/)
SYNC:            ./SYNC_Ngram_Graph_System.md

IMPL:            engine/infrastructure/orchestration/world_runner.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Thinking Produces Graph State

**Why:** All cognitive activity flows into the graph. No thinking is lost. Physics can surface what matters because everything is recorded.

```
GIVEN:  Any actor (human or agent) performs a cognitive action
WHEN:   Human writes message, agent thinks, agent queries, human decides
THEN:   A Moment is created in the graph
AND:    Moment links to touched Narratives, Spaces, Actors
AND:    Physics flows energy through new links
```

### B2: Energy Attracts Without Spawning

**Why:** No task creation logic needed. Goals don't spawn work — they attract energy. Moments near hot goals become hot. Simplicity.

```
GIVEN:  A goal Narrative exists with energy > 0
WHEN:   Human attention flows to that Narrative (proximity, interaction)
THEN:   Energy propagates to linked Moments
AND:    Moments near the goal become hot
AND:    No explicit "work creation" — just physics surfacing relevance
```

### B3: Hot Moment Triggers Agent

**Why:** Activation from physics, not orchestration. Agent works because something is hot in their Space, not because they were assigned a task.

```
GIVEN:  A Moment exists with energy > ACTIVATION_THRESHOLD
WHEN:   An agent is AT the same Space as the Moment
THEN:   Agent is triggered with context
AND:    System context = hot Narratives in agent's Space
AND:    Input = the active Moment (what to work on)
```

### B4: Work Creates More Moments

**Why:** Chain of work emerges naturally. Agent output becomes input for next cycle. No explicit task queue.

```
GIVEN:  Agent has been triggered with a hot Moment
WHEN:   Agent processes and responds
THEN:   New Moment(s) created from agent output
AND:    New Moments link to relevant Narratives/Spaces
AND:    Energy flows from completion
AND:    Cycle continues
```

### B5: World Ticks Without Human

**Why:** World is alive, not a tool that waits. Human is actor in world, not controller of it.

```
GIVEN:  World runner is active at speed x1/x2/x3
WHEN:   Tick occurs
THEN:   All actors generate energy based on proximity
AND:    Energy decays across all nodes/links
AND:    Strength accumulates where energy flowed
AND:    This happens whether or not human is active
```

### B6: Cold Links Retain Strength

**Why:** Memory without recall. Old work resurfaces via high-strength links when area reheats. Nothing truly forgotten.

```
GIVEN:  Work was done in a Space, then Space went cold
WHEN:   Human or agent revisits that Space later
THEN:   High-strength links surface relevant Narratives
AND:    Old work becomes accessible via strength, not Moment recall
```

### B7: Agents Differentiate Through State

**Why:** No designed specialization. Differentiation emerges from accumulated beliefs, memories, Space affinity. Discovery, not design.

```
GIVEN:  6+ agents start with similar state
WHEN:   Agents work over time, accumulating beliefs/memories
THEN:   Each agent develops distinct link patterns
AND:    One gravitates toward physics, another toward docs
```

### B8: Graph Becomes Canonical

**Why:** Docs are fragile, scattered, stale. Graph is queryable, connected, alive. Markdown becomes view, not source.

```
GIVEN:  Markdown docs exist in repository
WHEN:   Docs are ingested into graph
THEN:   Atomic sections become Narrative nodes
AND:    Changes create Moments
AND:    Docs can be regenerated from graph queries
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | Graph runs the dev process | All thinking becomes graph state, physics can surface it |
| B2 | Graph runs the dev process | No task queues — energy determines relevance |
| B3 | Agents receive context from graph | Activation from physics, not hardcoded orchestration |
| B4 | Agents receive context from graph | Work chain emerges from Moment creation |
| B5 | World runs continuously | World is alive, not event-driven |
| B6 | Memory through strength | Cold links retain strength for recall |
| B7 | Many agents, emergent differentiation | No specialized prompts — state determines personality |
| B8 | Docs dissolve into narratives | Markdown files are views, not source of truth |

---

## EDGE CASES

### E1: No Hot Moments in Agent's Space

```
GIVEN:  Agent is AT a Space with no Moments above threshold
THEN:   Agent remains idle
AND:    No forced work — silence is valid
```

### E2: Multiple Agents Triggered by Same Moment

```
GIVEN:  Multiple agents AT same Space, Moment crosses threshold
THEN:   All eligible agents may be triggered
AND:    Coordination handled by physics (energy split, timing)
```

### E3: Human Creates Moment in Cold Space

```
GIVEN:  Human writes message in a Space with no prior activity
THEN:   Moment created with initial energy from human
AND:    Space warms up, may trigger agents if threshold crossed
```

---

## ANTI-BEHAVIORS

### A1: No Task Queue

```
GIVEN:   Goal Narrative exists
WHEN:    System runs
MUST NOT: Create explicit task list or work queue
INSTEAD:  Energy flows, hot Moments surface naturally
```

### A2: No Agent Instructions

```
GIVEN:   Agent is triggered
WHEN:    Context is assembled
MUST NOT: Include hardcoded role instructions or specialization
INSTEAD:  Context is the instruction — hot Narratives in Space
```

### A3: No Human as Controller

```
GIVEN:   World is running
WHEN:    Human is inactive
MUST NOT: Pause world or wait for human input
INSTEAD:  World ticks continuously, agents work on hot areas
```

---

## MARKERS

<!-- @ngram:todo Define ACTIVATION_THRESHOLD value -->
<!-- @ngram:todo Specify how Moment links are auto-created from content -->
<!-- @ngram:todo Design energy split when multiple agents triggered -->
