# Tools — Validation: Invariants

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tools.md
BEHAVIORS:       ./BEHAVIORS_Tools.md
ALGORITHM:       ./ALGORITHM_Tools.md
THIS:            ./VALIDATION_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tools.md
HEALTH:          ./HEALTH_Tools.md
SYNC:            ./SYNC_Tools.md
```

---

## BEHAVIORS GUARANTEED

| Behavior ID | Behavior | Why This Validation Matters |
|-------------|----------|-----------------------------|
| B1 | Documentation Bundle Splitter writes one doc per bundle section without leaking paths | Prevents canonical docs from being overwritten by unsafe relative paths or missing fences while keeping the bundle-to-module flow traceable.
| B2 | Dialogue Stream helper produces moment graph updates instead of traversal logs | Keeps narration/moment orchestration consistent so downstream players and stream consumers see the same textual and interactive output.

---

## OBJECTIVES COVERED

| Objective ID | Objective | Validation anchor |
|--------------|-----------|------------------|
| O1 | Tools correctness — preserve core invariants | V1/V2 describe safe file handling and safe moment writes so each script can run without silently corrupting the repo or graph state.
| O2 | Tools clarity — keep observable outputs legible | PROPERTIES and the error tables explain how output formatting is guarded so logs stay readable and clickable interactions stay consistent.
| O3 | Tools performance — stay within intended budgets | V3 ensures stream writes and bundle rewrites avoid redundant cycles or repeated rewrites by short-circuiting when no sections/files exist.

---

## PROPERTIES

- P1: Deterministic fencing replacement ensures repeated runs over the same bundle generate bit-for-bit identical markdown documents and LED metadata in the target tree.
- P2: Safe path enforcement guarantees that every bundle section lands inside the repo root and rejects sections with `..` or absolute targets, which preserves repository hygiene.
- P3: Moment streaming operates in append-only fashion to the playthrough stream JSONL, creating new active moments without mutating existing timestamps or rewriting earlier entries.

---

## INVARIANTS

### V1: Bundle section creation is deterministic and safe

```
When the split script encounters a line starting with "### <path>.md", it treats <path> as a safe, relative, normalized pathname, rejects unsafe candidates, and rewrites any "$$$" fences into exactly three backticks before writing the file.
```

### V2: Streaming creates only new moments and links

```
The stream helper always appends to `playthroughs/*/stream.jsonl`, generates a new active moment for each canonical write, and never updates existing moment text except via explicit narrator follow-ups linked through CAN_LEAD_TO.
```

### V3: Scripts fail noisily when inputs are missing or malformed

```
Both scripts exit with a non-zero status when required inputs (bundle file, valid clickable syntax, existing playthrough graph) cannot be satisfied so the upstream flow notices the failure instead of proceeding with partial artifacts.
```

---

## ERROR CONDITIONS

### E1: Empty bundle or missing sections

```
WHEN:   `_split_sections` returns no entries or the input file cannot be read
THEN:   splitter prints a diagnostic and exits with code 1
SYMPTOM: Bundled docs remain untouched and doctor flags stale map links.
```

### E2: Unsafe target path detected

```
WHEN:   relative path includes absolute references or ".."
THEN:   script logs the unsafe path and skips writing that section
SYMPTOM: Missing documents and a warning in the console telling operators how to hand-edit the bundle.
```

### E3: Stream target graph unavailable

```
WHEN:   GraphOps cannot connect to the playthrough graph (missing credentials, closed DB)
THEN:   stream helper raises or prints the exception and exits non-zero
SYMPTOM: The `stream.jsonl` file stops growing and the narrator log shows the traceback for manual intervention.
```

---

## HEALTH COVERAGE

The tools health doc (`docs/tools/HEALTH_Tools.md`) tracks `ngram doctor` coverage for the module-wide manifest and encourages executing every script against known fixtures so the invariants above keep their signal instead of aging into silent failures. Keeping the doctor passing ensures this validation page aligns with the health indicators for the Tools module.

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Run `python3 tools/connectome_doc_bundle_splitter_and_fence_rewriter.py data/connectome/1.md --root docs/connectome/test` and inspect `docs/connectome/test` to confirm each section has a trailing newline and fences were replaced.
[ ] Run `python3 tools/stream_dialogue.py -p default -t dialogue --speaker char_aldric "Sample line"` while pointing `PLAYTHROUGH` env to a fixture and ensure the JSONL file grows with a new moment.
[ ] Confirm logs capture skipped unsafe paths or graph failures so debugging is visible.
```

### Automated Sanity

```
ngram doctor --scope tools
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2026-01-05
VERIFIED_AGAINST:
  implementation: tools/connectome_doc_bundle_splitter_and_fence_rewriter.py
  implementation: tools/stream_dialogue.py
  docs: docs/tools/*
VERIFIED_BY: doc-only review and manual script runs described above
RESULT: Tools validation template now includes all template sections and traces back to health checks and behaviors.
```

---

## GAPS / IDEAS / QUESTIONS

- The splitter currently relies on `data/connectome/1.md` formatting; should we extend it to accept zipped bundles or other delimiters for future imports without breaking existing repo state?
- The stream helper appends raw clickables to `stream.jsonl`; we could add an optional dry-run mode that prints the moment payloads without writing to the file for testing narrators without touching graphs.
- Verification currently leans on manual runs; adding fixture-based unit tests that simulate clicking words would give stronger automated guarantees but needs test harness support.
