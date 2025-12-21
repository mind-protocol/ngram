# Tools — Algorithm: Script Flow

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tools.md
BEHAVIORS:       ./BEHAVIORS_Tools.md
THIS:            ./ALGORITHM_Tools.md
VALIDATION:      ./VALIDATION_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tools.md
HEALTH:          ./HEALTH_Tools.md
SYNC:            ./SYNC_Tools.md
```

---

## FLOWS

1. Read input files or streams.
2. Transform content into protocol-friendly outputs.
3. Emit outputs into the docs or logs required by the pipeline.

---

## OVERVIEW

Tools hosts a small set of utility scripts that plug directly into our documentation and streaming workflows, so every helper stays tracked by the protocol even when it only touches a handful of files or a playthrough stream.

## OBJECTIVES AND BEHAVIORS

These helpers support the documented behaviors by keeping chunked connectome bundles ingestible (B1) and by streaming dialogue and narration data in a reproducible way for the graph-backed narrator workflow (B2), ensuring the module stays focused on predictable outcomes.

## DATA STRUCTURES

The splitter works with a sequence of `(relative_path, section_text)` tuples plus plain string buffers, while the stream dialogue helper builds JSON properties such as `tone`, `speaker`, and inline clickable metadata before handing them to the graph layer for persistence.

## ALGORITHM: main (connectome_doc_bundle_splitter_and_fence_rewriter.py)

The primary script starts by parsing CLI arguments (input bundle path, optional repo root), normalizing line endings, and running `_split_sections` to collect safe document paths and their bodies; it then iterates the resulting tuples, rewrites the `$$$` markers into Markdown fences, creates any missing directories, and writes the canonical markdown files so the rest of the pipeline can consume them without manual intervention.

## KEY DECISIONS

- Keep each utility in `tools/` rather than folding it into larger services so these scripts can stay focused and easily callable from the CLI.
- Only rewrite fences in place instead of keeping two copies because the normalized markdown is the single source of truth that downstream docs expect.
- Sanitize every extracted path through `_is_safe_relative_path` before writing to disk to avoid directory traversal bugs that would break documentation integrity.

## DATA FLOW

Connectome bundles flow from `data/connectome/*.md` through the splitter into dedicated pages under `docs/connectome/`, while the dialogue streamer receives text arguments, resolves the playthrough graph via `get_playthrough_graph_name`, and uses `GraphOps`/`GraphQueries` to mutate state before appending events to `playthroughs/{id}/stream.jsonl`, which downstream SSE consumers tail.

## COMPLEXITY

Splitting is linear in the number of lines in the bundle plus the number of sections, since each line is inspected once while buffering and the rewrite touches each file once; streaming is bounded by the number of clickables, graph lookup latency, and JSON encoding, so it scales in practice with the size of the narrative chunk and the graph queries it must run.

## HELPER FUNCTIONS

- `_is_safe_relative_path`: rejects absolute paths and parent traversals to keep writes local to the repo.
- `_split_sections`: collects `(path, text)` tuples from bundled markdown sections.
- `get_playthrough_graph_name`: reads `player.yaml` to decide which FalkorDB graph to target for a playthrough.
- `parse_inline_clickables`: extracts `[word](speaks...)` annotations so the graph can create target moments.
- `create_moment_with_clickables`: writes the main moment and clickable targets via `GraphOps`, incrementing the world tick and capturing the current place context.

## INTERACTIONS

The module touches `docs/connectome/`, `playthroughs/`, and the `engine.physics.graph` helpers, while also cooperating with infrastructure helpers such as `tools/run_stack.sh` for environment bootstrapping and the streaming SSE endpoint in `app/api/sse` that expects the JSONL feed these scripts produce.

## GAPS / IDEAS / QUESTIONS

- Explore adding regression tests that rerun the splitter on a bundle fixture to verify the rewritten fences match the expected docs.
- Should the dialogue streamer offer a dry-run mode that only builds the JSON payload without mutating the graph, making it easier to debug CLI clients?
- Consider documenting additional tools (run_stack, ngrok config) inside this module if they gain complexity so the chain remains complete.
