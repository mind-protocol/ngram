# SYNC: Dense Clustering

## Status: DESIGNING

The dense clustering concept is documented. Implementation is pending.

## What's Canonical

- [x] Core insight: Documents describe graph, extract the graph
- [x] Node type patterns (narrative_HEALTH, thing_DOCK, etc.)
- [x] Link type patterns (contains, verifies, attached_to, etc.)
- [x] ID patterns (deterministic, slugified)
- [x] Provenance via moments
- [x] Upsert semantics (MERGE, not CREATE)

## What's Documented

| Doc | Status |
|-----|--------|
| OBJECTIVES | Complete |
| PATTERNS | Complete |
| BEHAVIORS | Complete |
| ALGORITHM | Complete |
| VALIDATION | Complete |
| IMPLEMENTATION | Complete (design) |
| HEALTH | Complete (design) |
| SYNC | This file |

## What's Implemented

| Component | Status | Location |
|-----------|--------|----------|
| Code symbol extraction | DONE | `ngram/symbol_extractor.py` |
| Doc structure extraction | PENDING | `ngram/doc_extractor.py` |
| Cluster building | PENDING | `ngram/cluster_builder.py` |
| Health checks | PENDING | `ngram/cluster_health.py` |
| CLI integration | PENDING | `ngram/cli.py` |
| Tests | PENDING | `tests/ngram/test_cluster_builder.py` |

## Implementation Plan

### Phase 1: DocExtractor

Create `ngram/doc_extractor.py`:
- YAML block parsing
- Marker extraction (@ngram:todo, etc.)
- Reference detection
- Section parsing

### Phase 2: ClusterBuilder

Create `ngram/cluster_builder.py`:
- Node creation from definitions
- Link creation from relationships
- Reference resolution (find or stub)
- Moment creation
- Graph upsert

### Phase 3: CLI Integration

Update `ngram/cli.py`:
- Add `--cluster` flag to doctor
- Add `ngram cluster` command
- Integrate with existing symbol extraction

### Phase 4: Health Checks

Create `ngram/cluster_health.py`:
- Implement H-CLUSTER-* checks
- Add to doctor scan
- Create coverage queries

### Phase 5: Tests

Create `tests/ngram/test_cluster_builder.py`:
- Extraction tests
- Upsert stability tests
- Coverage tests

## Markers

@ngram:todo Create DocExtractor class
@ngram:todo Create ClusterBuilder class
@ngram:todo Add cluster command to CLI
@ngram:todo Implement health checks
@ngram:todo Write tests

@ngram:proposition Consider merging with symbol_extractor.py — both extract structure to graph, could share infrastructure

## Dependencies

| Depends On | For |
|------------|-----|
| `ngram/symbol_extractor.py` | Pattern reference, shared utilities |
| `engine/physics/graph/graph_ops.py` | Graph queries |
| Doctor scan infrastructure | CLI integration |

## Open Questions

1. **Incremental vs full extraction?**
   - Current design: Extract full doc each time, MERGE handles updates
   - Alternative: Track doc hashes, skip unchanged
   - Decision: Start with full, optimize later if needed

2. **Stub resolution strategy?**
   - When stub created, how/when is it resolved?
   - Option A: Manual — human creates the real node
   - Option B: Auto — next extraction that defines it resolves
   - Decision: Auto-resolution on next extraction

3. **Space assignment?**
   - How to determine which space a doc belongs to?
   - Current: Path-based (docs/engine/* → space_AREA_engine)
   - Alternative: Explicit in doc frontmatter
   - Decision: Path-based default, frontmatter override

## Last Updated

2024-12-24 — Initial documentation complete, implementation pending
