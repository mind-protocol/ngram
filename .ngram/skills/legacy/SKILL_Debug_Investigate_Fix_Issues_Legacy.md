# Skill: `ngram.debug_investigate_fix_issues`
@ngram:id: SKILL.DEBUG.INVESTIGATE_FIX

## Maps to VIEW
`.ngram/views/VIEW_Debug_Investigate_And_Fix_Issues.md`

## Purpose
Perform the code change under canon constraints; update doc chain alongside implementation; produce markers for gaps/proposals.

## Inputs (YAML)
```yaml
module: "<area/module>"
task: "<what to change>"
```

## Outputs (YAML)
```yaml
code_changes: ["<files modified>"]
doc_updates: ["<docs updated>"]
markers:
  escalations: ["<@ngram:escalation>"]
  propositions: ["<@ngram:proposition>"]
```

## Gates (non-negotiable)
- Update doc chain for every meaningful code change.
- No new terms/names without canon support (PATTERNS/CONCEPT).
- Prefer minimal safe changes; verify via health/runtime where applicable.

## Evidence & referencing
- Docs: `@ngram:id + file + header path`
- Code: `file + symbol`

## Markers
- `@ngram:TODO <plan description>`
- `@ngram:escalation <blocker/problem>`
- `@ngram:proposition <suggestion/improvement>`

## Never-stop rule
If blocked, log `@ngram:escalation` + `@ngram:proposition`, then switch to the next unblocked task.
