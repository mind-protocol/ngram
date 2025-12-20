# SKILL: Collaborate Pair Program With Human

**You're working in real-time with a human; act as a proactive, co-driving partner.**

---

## WHY THIS SKILL EXISTS

Pair programming with a human needs:
- Shared context without over-explaining basics
- Fast, confident iteration with clear checkpoints
- Autonomy when the human is busy or the next step is obvious

---

## CONTEXT TO LOAD

**Start from protocol state:**
- `.ngram/state/SYNC_Project_State.md`
- Relevant VIEW for the task (implement, extend, debug, review)
- Target module docs (`docs/{area}/{module}/...`) when touching code or docs

---

## COLLABORATION MODE

- Drive forward without waiting; narrate decisions briefly.
- Offer concrete next actions, then take the best one if no objection is required.
- When working on ambiguous items, choose the most likely path and leave an `@ngram:escalation` marker.
- Keep scope tight per change; keep a crisp log in SYNC.

---

## SELF-DIRECTION & AUTONOMY

- If you want to stop or are unsure what to do, run `ngram doctor` and work autonomously on the issues.
- If `ngram doctor` reports 0 issues, explore the repo for the next highest-value improvement.
- Propose improvements using `@ngram:proposition` markers and implement them to move the project forward.

---

## TESTING & VERIFICATION

- Always run the relevant HEALTH checks for changed areas.
- Verify documentation chains (PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC).
- Update docs to match implementation, or update implementation to match docs.

---

## CLOSEOUT

- Update `.ngram/state/SYNC_Project_State.md` with what changed and why.
- Note any follow-up work as `@ngram:todo` or `@ngram:proposition`.
