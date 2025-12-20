# NGRAM Documentation Chain Pattern (Draft “Marco”)

> **Goal:** make agents (and humans) produce changes that are **canon-aligned, non-regressive, auditable**, and **anti-default** (no drifting back to “standard repo” habits).

---

## Recap — Action Items (Changes to adopt / formalize)

1. **Canonical reference format** for every claim:

   * **Docs:** `@ngram:id` **+ file name** **+ header path** (dense titles stay valuable)
   * **Code:** `@ngram:id` (if applicable) **+ file name** **+ symbol name** (function/class)
   * Example (doc):

     * `@ngram:id: CLI.PROMPT.OUTPUT.SECTIONS — docs/cli/prompt/BEHAVIORS_prompt.md — ## Prompt Output Structure › ### Required Sections`
   * Example (code):

     * `@ngram:id: CLI.PROMPT.GENERATOR — ngram/prompt.py — generate_bootstrap_prompt()`

2. **Doctor check: “code delta requires doc delta”** (governed areas):

   * Flag commits/changes that modify implementation without updating linked docs (and/or SYNC) for the touched module.

3. **Doctor check: doc-link integrity**:

   * Verify that doc pointers in code resolve to real paths.
   * Verify that CHAIN pointers in docs resolve.

4. **Adopt `@ngram:id` anchors** inside docs (avoid false collisions) while keeping dense titles.

5. **Migrate VIEWS → Skills**:

   * Make VIEWS procedural and executable; eliminate “revert to default repo method” by encoding the workflow.

6. **Deprecation/Archive rule (if applicable)**:

   * If there are archival docs, they must be explicitly marked and **not loaded by default** unless SYNC points to them.

---

## Canon Principles (Why this chain exists)

* **Doc is source of truth.** Implementation must match docs; docs are updated on every change.
* **Full chain comprehension is required** for robust work (no summaries that delete scope).
* **No default-pattern reversion:** comments, naming, monitoring, autonomy, and operational stance must be canon-aligned.
* **Evidence-driven shipping:** runtime/health and validation are first-class, and are surfaced to agents in real time.

---

## The Documentation Chain

**Location pattern:** `docs/{area}/{module}/` (module-local docs live together)

### File Types and Purpose (item-by-item)

#### PATTERNS_*.md

| PATTERNS_*.md | Design philosophy & scope — WHY this shape, WHAT's in/out | Before modifying module |
| ------------- | --------------------------------------------------------- | ----------------------- |

**What it must do**

* Declare **scope boundaries** (in / out) so the agent cannot “helpfully” drift.
* Define **canonical terms** and naming expectations (the anti-default vocabulary).
* Encode **anti-patterns** specific to this module (what the standard-repo brain will do wrong).

**How agents should use it**

* Load first; treat it as the **permission model** for any change.
* If a proposed edit violates a PATTERNS boundary, stop and raise `@ngram:escalation`.

**Linking rules**

* Must point forward to the rest of the chain (BEHAVIORS/VALIDATION/IMPLEMENTATION/HEALTH/SYNC).
* Should reference cross-cutting CONCEPT docs when terms are shared across modules.

---

#### BEHAVIORS_*.md

| BEHAVIORS_*.md | Observable effects — WHAT it should do | When behavior unclear |
| -------------- | -------------------------------------- | --------------------- |

**What it must do**

* Specify the **externally observable contract**: outputs, side-effects, interactions.
* Define **what counts as correct** at the interface boundary.

**How agents should use it**

* Use it to resolve “what should happen” before changing code.
* When runtime/health shows mismatch, produce a **PR plan** (align code vs align docs) plus markers.

**Linking rules**

* Must cite VALIDATION invariants that constrain the behavior.
* Should cite IMPLEMENTATION docking points that realize the behavior.

---

#### ALGORITHM_*.md

| ALGORITHM_*.md | Procedures — HOW it works (pseudocode) | When logic unclear |
| -------------- | -------------------------------------- | ------------------ |

**What it must do**

* Provide the **procedure** / step model for how behavior is achieved.
* Make the logic understandable without reading the full code.

**How agents should use it**

* Use it when refactoring or changing control flow to avoid logic regressions.
* If you change the algorithm, you update this doc *and* then update VALIDATION/HEALTH expectations.

**Linking rules**

* Must link to IMPLEMENTATION entry points that implement the steps.
* Must respect PATTERNS constraints and VALIDATION invariants.

---

#### VALIDATION_*.md

| VALIDATION_*.md | Invariants — WHAT must be true | Before implementing |
| --------------- | ------------------------------ | ------------------- |

**What it must do**

* Define invariants that must hold across refactors and extensions.
* Provide the **truth constraints** that HEALTH will verify.

**How agents should use it**

* Treat as non-negotiable guardrails.
* When proposing changes that might break an invariant, escalate rather than “fixing around it.”

**Linking rules**

* HEALTH indicators must map to VALIDATION (by `@ngram:id`).
* IMPLEMENTATION must list the docking points needed to verify invariants.

---

#### IMPLEMENTATION_*.md

| IMPLEMENTATION_*.md | Code architecture — WHERE code lives, data flows | When building or navigating code |
| ------------------- | ------------------------------------------------ | -------------------------------- |

**What it must do**

* Declare the **canonical file paths**, scopes, and dataflow.
* Specify docking points for inputs/outputs and HEALTH checkers.

**How agents should use it**

* Use it as the authoritative map for “where to change code” and “what not to touch.”
* Use it to prevent duplicate abstractions and naming drift.

**Linking rules**

* Must link to the exact implementation surfaces (files + symbols) that realize BEHAVIORS/ALGORITHM.
* Must link to HEALTH docs describing verification against these surfaces.

---

#### HEALTH_*.md

| HEALTH_*.md | Health checks — WHAT's verified in practice | When defining health signals |
| ----------- | ------------------------------------------- | ---------------------------- |

**What it must do**

* Define what is verified **continuously** and how it is surfaced to agents in real time.
* Map indicators to VALIDATION invariants; declare docking points from IMPLEMENTATION.

**How agents should use it**

* Prefer the health stream as runtime truth for “is the system aligned right now?”.
* When health is degraded, constrain changes to restoring invariants; escalate unknowns.

**Linking rules**

* Must reference VALIDATION by `@ngram:id` (no orphan health signals).
* Must reference docking points declared in IMPLEMENTATION.

---

#### SYNC_*.md

| SYNC_*.md | Current state — WHERE we are | Always |
| --------- | ---------------------------- | ------ |

**What it must do**

* Record the current state, open gaps, escalations, and next work.
* Capture what changed, what was verified, and what remains uncertain.

**How agents should use it**

* Always load; treat as the “present tense” of the module.
* Append outcomes of work (including markers) after changes.

**Linking rules**

* Must point to the active chain docs for the module.
* Must point to any active proposals/escalations and where they are resolved.

### Cross-Cutting Docs

| Type           | Purpose                                                | Load When                  |
| -------------- | ------------------------------------------------------ | -------------------------- |
| `CONCEPT_*.md` | Cross-cutting concept — definition + canonical terms   | When concept spans modules |
| `TOUCHES_*.md` | Index of appearances — where concept touches code/docs | When locating related code |

---

## Chain Hierarchy (Authority)

> These types do not “compete”; they cover different layers. But when deciding what to do next, the **navigation order** is authoritative.

**Navigation order (default):**

`PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC`

* **PATTERNS** constrains what’s allowed/desired (scope, philosophy, exclusions).
* **VALIDATION** constrains what must never break.
* **IMPLEMENTATION** locates the real surfaces and docking points.
* **HEALTH** defines continuous verification anchored to VALIDATION (see template alignment below).
* **SYNC** is the truth of current state, gaps, open escalations, and next work.

---

## Canon Linking Rules (Bidirectional)

### 1) Docs → Code

* Every module doc set must point to:

  * canonical entry points in code
  * dataflow paths
  * dock points for health signals
* `IMPLEMENTATION_*.md` is the canonical **index** of implementation surfaces.

### 2) Code → Docs

* Every implementation file (or at least every module entry point) must include an explicit pointer to its doc chain.
* Pointer must include:

  * module doc directory path
  * doc ids or file names for PATTERNS/VALIDATION/IMPLEMENTATION/HEALTH/SYNC

### 3) Link Integrity

* Links must be **machine-checkable** by Doctor.
* Broken links are treated as “health degraded” for the module.

---

## Canon Reference Format (Stable + Dense)

### Why not “line numbers”

* Line numbers are fragile; a single edit invalidates references.

### Preferred reference tuple

**Docs:**

* `@ngram:id` (stable anchor)
* file name (dense)
* header path (human context)

**Code:**

* file name
* symbol name (function/class)
* optional `@ngram:id` if you want a stable anchor inside code comments/docstrings

#### Example

* Doc: `@ngram:id: CLI.PROMPT.OUTPUT.SECTIONS — docs/cli/prompt/BEHAVIORS_prompt.md — ## Prompt Output Structure › ### Required Sections`
* Code: `ngram/prompt.py — generate_bootstrap_prompt()`

**Rule:** any non-trivial claim must cite at least one reference tuple.

---

## Health as Runtime Truth (Sublayer surfaced to agents)

You described a **real-time health sublayer** that flags and streams health to agents. This doc chain expects HEALTH to be first-class and anchored to VALIDATION.

### HEALTH template alignment

Use the existing HEALTH template as the canonical shape for `HEALTH_*.md` (verification mechanics, docks, throttling, forwarding, status stream). fileciteturn3file0

### Required properties

* HEALTH indicators **must** map to VALIDATION IDs.
* HEALTH must use docking points declared in IMPLEMENTATION (no hidden hooks).
* HEALTH results must be forwarded to the “agent-visible stream” Doctor reads.

---

## Agent Operating Contract (What agents must do)

### Preflight (always)

1. Identify module scope from file path / doc pointer.
2. Load full doc chain for module:

   * PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH, SYNC
3. Confirm canonical terms (naming) and constraints (scope/invariants).

### Work (always)

4. Make changes **only** consistent with canon (no default repo patterns).
5. Write rich, multidimensional comments where canon expects it (context, doubts, tradeoffs).

### Proof (always)

6. Validate via:

   * HEALTH stream signals (preferred for continuous truth)
   * plus targeted runtime checks/tests when appropriate

### Reporting (always)

7. If there is a gap/decision:

   * add `@ngram:escalation` for blocks
   * add `@ngram:proposition` for improvements
8. Update module `SYNC_*.md` with:

   * what changed
   * what was verified
   * what remains open

---

## Injection Strategy (Direct injection vs “read as needed”)

In this system, agents should **not** rely on heuristics or default behavior.

### Canon approach

* **Direct injection is valid** *when scoped by module*.
* Do not inject “all modules”; inject **target module chain** + cross-cutting concepts required.

### Deterministic module injection

* From the touched file, resolve the doc directory.
* Inject the full chain for that module.
* Optionally inject relevant `CONCEPT_*` and `TOUCHES_*` that are explicitly referenced.

### Implementation note

* `--append-system-prompt` is appropriate to enforce:

  * “always load full chain”
  * “never summarize away scope”
  * “use reference tuples”
  * “write markers + SYNC updates”

---

## Doctor Responsibilities (Recommended Checks)

1. **Doc-pointer integrity**

   * code → docs path exists
   * docs → implementation paths exist

2. **Change coupling**

   * if governed implementation changes, require doc chain delta (and SYNC delta)

3. **`@ngram:id` hygiene**

   * IDs are unique within module
   * IDs are referenced when required (evidence standard)

4. **Health wiring**

   * HEALTH stream destination exists and is readable
   * health indicators map to VALIDATION IDs

---

## Templates and Enforcement

* Every doc type has a template.
* Doctor enforces adherence to:

  * required sections
  * link integrity
  * ID uniqueness
  * coupling rules

---

## Minimal “Chain Manifest” (Optional, but powerful)

Each module doc directory may include a manifest (or declare in `module.yaml`) listing:

* chain file names
* required `@ngram:id` anchors
* implementation entry points
* health stream destination

This makes injection and verification deterministic.
