---
name: multi-index-research
description: Compare evidence across selected QubicDB knowledge domains or discover relevant indexes within an authorized research scope.
---

# Cross-index research

Resolve existing index ownership from configuration and `qubicdb_list_indexes`. Separate persistent knowledge owners/domains may justify different indexes; a new query or research subtopic usually does not. `qubicdb_recent_indexes` is an activity hint, not proof of relevance or authorization.

For known scopes, call `qubicdb_multi_search` with `index_ids` as a JSON-encoded string, for example `"[\"brain-cedar\",\"brain-atlas\"]"`, plus a focused `query` and small per-index `limit`. Inspect the `errors` map and keep `_index`, `_id`, and source metadata with each result.

Use `qubicdb_global_search` when discovering relevant projects across the endpoint's authorized scope. It searches loaded indexes only; it does not cover all registered/persisted brains. For known inactive domains, explicit multi-search can load them. Indexes are separate storage scopes, not a promise that a shared MCP key cannot search other domains.

Multi/global metadata is a soft boost even when the tool description says filter. For “only this source/status/thread,” run `qubicdb_search` with JSON-string `metadata` and `strict: true` separately in each selected index. Merge the verified results, including missing or failed scopes as limitations.

Cross-index merge order uses activation history rather than a calibrated semantic score. Compare the source content, not ranks across independent brains. Graph traversal occurs inside each index; cross-domain synthesis is the assistant's reasoning, not an automatic cross-index synapse.

A complete cross-project inventory needs an explicit permitted index set and counted per-index enumeration. Global similarity search is not enumeration. Preserve scope when storing any synthesized conclusion; cross-project comparison does not automatically authorize copying every source into one shared index.
