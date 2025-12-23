# VIEW: Build ngram Graph System

**You're building the ngram graph system itself — dogfooding the engine on its own development.**

---

## WHY THIS VIEW EXISTS

ngram is both the tool and the first client. Building ngram using ngram proves the system works. This view tracks the meta-development process: how we use graph-based orchestration to build graph-based orchestration.

---

## CONTEXT TO LOAD

### Primary (always load)

- `docs/building/OBJECTIVES_Ngram_Graph_System.md` — what we're building and why
- `.ngram/state/SYNC_Project_State.md` — current state

### Engine Understanding

- `docs/physics/PATTERNS_*.md` — energy mechanics
- `docs/schema/PATTERNS_Schema.md` — node/link structure
- `engine/physics/` — actual implementation

### Graph State

- Current graph in FalkorDB (`ngram` graph when created)
- `engine/data/physics_config.yaml` — energy/weight defaults

---

## WHAT WE'RE BUILDING

### Phase 1: Bootstrap

1. **Create ngram graph** — Seed with Spaces (modules), Actors (agents), initial Narratives
2. **Design Space structure** — One per module? Per doc area? Per objective?
3. **Define 6+ agents** — Names, starting positions, no special prompts
4. **Human as Actor** — Same rules, generates energy, creates Moments

### Phase 2: Doc Dissolution

1. **Ingest existing docs** — Convert to Narrative nodes
2. **Link to Spaces** — Each Narrative AT a Space
3. **Establish beliefs** — Actors BELIEVES Narratives
4. **Mark types** — goal, memory, belief, etc.

### Phase 3: Live Loop

1. **World runner on ngram graph** — Continuous ticks
2. **Agent activation from energy** — Hot context triggers work
3. **Moment creation from work** — Agent output becomes Moments
4. **Strength accumulation** — Memory through use

---

## KEY DECISIONS (from OBJECTIVES)

| Decision | Choice |
|----------|--------|
| Emergence vs predictability | Emergence |
| Simplicity vs features | Simplicity |
| Task queues | No — Narratives with energy |
| Agent specialization | Emergent, not designed |
| Doc canonical | No — graph is canonical |

---

## OUTPUT

Work in this view produces:
- Graph seed files (`start_graph.yaml` or similar)
- Narratives representing current work
- Moments capturing decisions
- Updates to `docs/building/SYNC_*.md`

---

## HANDOFFS

**To next agent:** What's hot in the graph, what Narratives need attention.

**To human:** What emerged, what decisions surfaced, what needs human energy.

---

## VERIFICATION

- Is the graph the source of truth, not the docs?
- Are agents receiving context from graph state?
- Does energy flow determine what gets worked on?
- Are Moments being created from work?
