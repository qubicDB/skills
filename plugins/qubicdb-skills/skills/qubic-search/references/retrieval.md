# Retrieval: scope, evidence, and complete data

## Choose a path by the question

A known neuron ID calls for `qubicdb_read`. A bounded index scan calls for `qubicdb_recall`. A topical question calls for `qubicdb_search`, not a full export. A comparison uses the known index set through `qubicdb_multi_search`; broad discovery can use `qubicdb_global_search` within the authorized scope. Inspect index metadata/mappings before inventing an ID. Registration, activity and persisted existence are different.

Use a natural-language cue for concepts/paraphrases; include exact product names, error codes or version identifiers when they disambiguate the evidence. For a broad engineering task, use complementary cues for separate uncertainties (decision, failure cause, dependency) rather than one enormous query containing the whole conversation. Select actual relevant hits and follow known references. No result is not proof of absence; a positive hit is not proof of relevance.

MCP `metadata` is a JSON string of string values. Single-index `search` with `strict: true` enforces all supplied fields. Without strict, it is only a boost. Multi/global search have no strict flag: mandatory constraints across projects require separate strict per-index searches. `context` has no metadata filter or individual IDs; assemble selected search records locally when the question needs those constraints or citations.

When the model is loaded, search combines lexical and embedding similarity with activation/recency/frequency/depth/sentiment and graph effects. It is not pure vector ranking or an exact-match API. A missing or failed embedding can fall back to lexical behavior. Code/HTML/emoji cleaning changes what is embedded; exact code identifiers or markup should be checked in the stored content or an exact filter, not only through semantics. There is no per-call vector switch. Changing server-wide alpha for one normal lookup is not appropriate, and alpha 0 still computes the query embedding.

For “no vector” with a known ID, read it; for a small collection, recall and compare; for exact metadata/content conditions or large enumeration, use the configured authorized REST `find/count` surface. Do not use another transport to bypass an approval denial. If that surface is unavailable, explain the precise limitation rather than inventing a tool or claiming completeness.

## When the user really needs all records

Use exhaustive access for an inventory, reconciliation, export, migration, or audit whose correctness depends on complete coverage. Usually inspect counts/metadata first and keep large results on disk, passing only a relevant slice or summary into the model context. “Search all projects for a decision” and “export all data” are different jobs.

Limits in the verified release:

- MCP single-index search caps at 200 hits, recall at 500, and recall has no offset.
- REST `/v1/recall` returns a fixed 100 records and ignores requested limit/offset.
- Multi/global limits are per-index (capped at 50); global caps merged results at five times that limit. Global searches loaded indexes only and silently skips failed workers. Multi-search reports per-index errors.
- Registry listing is not a complete physical-storage manifest when unregistered persisted brains can exist. A logical export of known indexes is not a whole-server backup.
- `context` searches up to 50 candidates, uses a content-bytes/4 budget estimate and stops at the first oversized item. Empty context can coexist with valid search hits. It has no per-neuron citations.

For one known stable index, `POST /v1/command` can `count`, then `find` with an exact filter, `_id` ordering, `skip`, and bounded page size. Stop at the counted size, validate distinct IDs and recount at the end. Do **not** loop until an empty page: the current `skip >= count` implementation can return the first page again. A changing collection or repeated IDs means the enumeration is not complete. Matching counts do not establish transaction snapshot isolation.

Use [../scripts/read_all.py](../scripts/read_all.py) for this repeated operation, resolving its path from this skill directory rather than the current project. It writes API-visible neuron documents to JSONL and a manifest instead of filling the context window. It does not export hidden embeddings, internal sentiment, synapses, or a restorable `.nrdb` backup.

```sh
python3 scripts/read_all.py --url http://127.0.0.1:6060 --index CONFIRMED_INDEX --output /chosen/output/neurons.jsonl
```

Use the actual configured base URL/index and a suitable new output path; do not substitute localhost for a remote deployment. When the deployment uses an MCP key, supply the existing `QUBICDB_MCP_API_KEY` environment variable without printing it. Optional `--filter` is an exact command JSON filter with metadata keys at the top level, for example `'{"type":"decision"}'`.

For relationships as well as content, inspect/export `/v1/synapses` or `/v1/graph` separately with the same scope and record the non-transactional timing. For every registered/loaded project, establish the permitted index set explicitly and enumerate each; report missing scopes. A full consistent storage backup requires the storage/operational workflow, not merely increasing `limit`.

## Assess returned evidence

Retain `_index` or known index ID, `_id`, source and relevant version/date. Cross-index merge order uses energy/access history, not a calibrated semantic score. Recall is energy-ordered, not newest-first. Check a newer correction, the applicable environment, and the user's requested time frame before presenting an old highly activated decision as current. State which scopes/results are incomplete; do not turn a partial failure into “nothing is known.”
