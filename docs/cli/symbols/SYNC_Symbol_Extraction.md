# SYNC: Symbol Extraction

## Status: CANONICAL

Implementation complete and integrated with CLI.

## What's Done

- [x] Spec created: specs/symbol-extraction.yaml
- [x] Python extractor: AST-based parsing of functions, classes, methods, constants
- [x] Relationship extraction: calls, imports, inheritance
- [x] Test inference: naming convention, file convention, explicit markers
- [x] Docs linking: markers, references, module convention
- [x] Graph upsert: FalkorDB integration via GraphOps
- [x] CLI commands: `ngram symbols`, `ngram doctor --symbols`
- [x] Documentation: PATTERNS, ALGORITHM, IMPLEMENTATION

## What's Pending

- [ ] TypeScript/JavaScript extractor
- [ ] Incremental extraction (only changed files)
- [ ] Tests for symbol extractor
- [ ] Level 3 region extraction (separate spec)

## Verified Working

```bash
# Dry run extraction
$ ngram symbols --dry-run -f engine/physics
Files scanned: 36
Symbols extracted: 407
Links created: 776

# With graph upsert
$ ngram symbols -f engine/physics --graph ngram
```

## Markers

@ngram:todo Add unit tests for PythonExtractor
@ngram:todo Add TypeScript extractor (lower priority)

## Last Updated

2024-12-24 — Initial implementation complete
