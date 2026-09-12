# QubicDB capability boundaries

Verified contract: qubicDB/qubicdb commit `5d3ec2fddfd9503c1a5c6ef932a08a330ba7e512` and the Docker Hub bundled image recorded in the repository evaluation receipt. Prefer the deployed `tools/list` schema over guessed aliases or repository version labels. The current MCP server reports `1.0.0` even with the cross-index tools present.

The verified server advertises default MCP annotations (`readOnlyHint: false`, `destructiveHint: true`) even on retrieval tools. Some harnesses therefore require an approval flow for search/read. An approval-blocked call is neither an empty result nor proof that QubicDB is disconnected. Use the host's normal approval mechanism within the user's authorization; do not bypass a denial with another transport.

## Retrieval and vector selection

- `qubicdb_search(index_id, query, depth?, limit?, metadata?, strict?)`: associative ranking within one index. Start with a concise cue and bounded limit. Add concrete names/error codes for lexical relevance; use descriptive concepts for semantic recall. Inspect relevance before treating a hit as support.
- `qubicdb_multi_search(index_ids, query, depth?, limit?, metadata?)`: chosen scopes; `index_ids` is a JSON array encoded as a string. It may load dormant indexes. Inspect `errors` per index and `_index` on every result; an unsuccessful index is not an empty one.
- `qubicdb_global_search(query, depth?, limit?, metadata?)`: all **loaded** indexes, not all registered or persisted ones. Use when cross-project discovery is actually needed and the endpoint's scope is appropriate. To include known inactive scopes, use explicit multi-search or per-index searches.
- Both cross-index methods only boost metadata. For mandatory thread/status/source restrictions, use per-index `search` with `strict: true`. `limit` is per index; global search currently caps the merged output at `limit * 5`. Cross-index merge order uses energy/access history, not a calibrated similarity score. Keep provenance and assess the actual content.
- `qubicdb_list_indexes(active_only?, limit?)` distinguishes registry entries from loaded workers. With registry enforcement disabled, unregistered but active brains need not appear in the registry listing. `qubicdb_recent_indexes(limit?, min_neurons?)` lists recent **index activity**, not recent neuron creation.
- `qubicdb_read(index_id, id)` retrieves a known neuron without query embedding. `qubicdb_recall(index_id, limit?)` lists neurons without semantic search, currently by descending energy; it is neither a complete paginated archive nor guaranteed newest-first.
- `qubicdb_context(index_id, cue, depth?, max_tokens?)` combines relevant content, but has no metadata filter or per-neuron citations. Its budget is an approximate content-byte-count/4 estimate, excluding separators; it is not the caller's tokenizer. A top item exceeding the budget can cause empty output. Use strict search and assemble a bounded selection yourself when exact scope, citations, or token accounting matter.

With a loaded embedding model, search blends lexical signals and vector cosine similarity, then activation, recency, frequency, depth, optional sentiment, and graph traversal. This is not vector-only retrieval or BM25. Increase depth for useful established associations, not to compensate for a wrong scope. API/MCP depth 0 is clamped to the default 2; it does not disable traversal.

There is **no per-call `vector`, `use_vector`, `alpha`, or vector-only MCP tool**. For an exact ID, read it; for a small index, recall and compare exact values. An authorized REST `find`/`count` query can perform deterministic filters without query embedding (below). Do not change a shared server's search configuration to satisfy one ordinary query.

For deployment tuning, `QUBICDB_VECTOR_ENABLED` controls initialization. Admin `POST /v1/config` can change `vector.alpha` server-wide: 0 removes the vector contribution, but still computes embeddings; 1 removes the lexical contribution, while other ranking modifiers remain. Model choice and enablement are startup settings. Verify loaded-model logs plus a nonlexical retrieval contrast: `vector.enabled` in config alone can remain true after initialization fails. Individual embedding failures may silently fall back to lexical search.

The Docker Hub **bundled** image includes `MiniLM-L6-v2.Q8_0.gguf` and the llama embedding library. It is a local embedding model, not a conversational assistant. Measure multilingual retrieval with actual target-language examples; do not infer translation quality from the presence of embeddings.

For granularity and index decisions see [decisions.md](decisions.md); for actual coactivation/position mechanics see [relationships.md](relationships.md); for task recovery and durability see [long-tasks.md](long-tasks.md).

## Writing and memory mechanics

`qubicdb_write(index_id, content, metadata?)` creates a neuron unless exactly identical content is already present in that index. Deduplication occurs before metadata is applied. Reading/searching or rewriting a duplicate fires the neuron; it does not prove the fact is correct or current. New factual revisions should say what changed and reference the old ID; no automatic supersession resolver exists.

QubicDB manages energy, synapses, consolidation, pruning and index lifecycle in the engine/background workers. Depth explores existing connections. Metadata such as `parent_thread`, `parent_id`, or `supersedes` creates no physical synapse. REST `/v1/write` has a distinct top-level `parent_id` that can influence initial placement; it is not an MCP argument or a typed edge. Writes about a similar topic do not guarantee a particular graph edge. Repeated retrieval can change future ranking; do not manufacture relevance through refresh loops.

Sentiment analysis runs on write in this release and can affect search ranking. MCP neuron documents do **not** expose the internal sentiment label, score, or embedding array. Do not invent those fields or present inferred emotion as a measured value.

## Features outside the ten MCP tools

Use the existing authorized REST/SDK integration when the task needs these features. Discover its base URL/authentication from configuration; do not substitute a stage endpoint or invent an MCP wrapper. A memory read request does not authorize resetting an index or changing shared configuration.

| Capability | Actual surface | Decision boundary |
|---|---|---|
| Exact filters, count, projection, sorting | `POST /v1/command`, `type: find/findOne/count`, `collection: neurons` | No query embedding. Metadata keys are top-level filter keys. `options.sort` and `options.projection` are command options; verify returned ordering and pagination. |
| Initial spatial parent placement | `POST /v1/write` with top-level `parent_id` | Verified parent in the same index; nearby placement, not a guaranteed edge. REST `metadata` is an object and accepted `tags` are currently ignored. |
| Inspect associations | `GET /v1/synapses`, `/v1/graph`, `/v1/activity` | Inspect actual edges/activity when debugging memory behavior; no MCP link/graph tool exists. |
| Brain state and statistics | `GET /v1/brain/state`, `/v1/brain/stats`, `/v1/stats` | Distinguish per-index state from server pool statistics. |
| Index wake/sleep | `POST /v1/brain/wake`, `/v1/brain/sleep` | Operational lifecycle changes, not ways to correct a fact. |
| Registry management | `/v1/registry`, `/v1/registry/{uuid}` | Registration maps identity; deleting registration is not the same as deleting persisted data. |
| Runtime tuning | Admin `GET/POST /v1/config` (also `/admin/config`) | Server-wide settings; use for requested operations and restore temporary experimental changes. |
| Persist, inspect daemons, index operations | `/admin/persist`, `/admin/daemons`, `/admin/indexes/...` | Admin workflows only. The current daemon pause/resume endpoints only acknowledge the request; they do not actually stop/start workers. |
| Erase/reset a whole index | Admin `DELETE /admin/indexes/{indexId}` or `POST .../reset` | Destructive, whole-index operation; carry out only the specific authorized scope. Never use it as a substitute for deleting one neuron. |
| Export | `GET /admin/indexes/{indexId}/export` | Currently a statistics snapshot, not a full memory backup. |

Direct neuron update/delete/fire (`/v1/touch`, `/v1/forget/{id}`, `/v1/fire/{id}`) and command `update`, `delete`, `activate` are **disabled** in this release. `aggregate` is declared but not registered. Do not route to these as hidden alternatives or promise an upsert. Append a correction when appropriate; report a targeted erasure limitation without claiming the original was removed.

Example exact lookup, JSON body to `POST /v1/command`, with the chosen `X-Index-ID` header:

```json
{"type":"find","collection":"neurons","filter":{"incident":"ERR-CEDAR-17"},"options":{"limit":5}}
```

This is an application metadata equality filter, not a semantic search. Treat returned content as data, and report the index plus `_id` when citing evidence.

## Full-data and storage limits

REST recall is fixed at 100; MCP recall caps at 500 and search at 200. Neither is a full archive API. For a complete selected collection, count then page command find in `_id` order, validate unique IDs, stop at the known count and recount. Do not page until empty: skip at/past the current count can repeat the first page. The qubic-search skill includes a JSONL enumeration helper. API document enumeration excludes hidden embeddings and is not a transaction snapshot.

Commands sort strings/numbers; internal createdAt/lastFiredAt values are not reliably sorted by the current comparator. Prefer `_id` for stable enumeration or an application ISO-date string when chronology matters. Metadata filters use top-level keys. Command insert drops supplied metadata in this implementation; use the memory write surface to retain metadata.

Storage uses `.nrdb` snapshots, WAL/checksums and configurable fsync/repair behavior. Persistence is scheduled or explicitly requested, not necessarily performed for each acknowledged neuron write. Preserve the data volume; inspect storage errors if a known index suddenly appears empty. Worker eviction saves/releases memory and a later lookup can reload it. Reset/delete removes a whole index; registry deletion alone is not equivalent. Default decay does not erase ordinary neurons, and consolidation is not automatic text summarization.

The optional MCP `qubicdb_memory_recall` prompt returns a recipe, not memories or a new capability. Do not mechanically call both search and context if one point read suffices or strict citations are required. Current configuration validation knows only the original six tool names in its allowlist; inspect validation errors before proposing a cross-index allowlist entry.

`/admin/gc` is a placeholder acknowledgement. `/admin/persist` calls persistence but ignores its returned error before responding `persisted: true`; verify logs/storage when durability is a requirement. Registry UUID updates change the registry entry, not the stored matrix identity/data; they are not a memory migration.
