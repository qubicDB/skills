---
name: knowledge-base-server
description: Build and query a QubicDB knowledge base with source-aware document chunks, revisions, and scoped retrieval.
---

# QubicDB knowledge base

Use the configured connection and existing knowledge-domain index. New documents or versions normally belong in that scope; do not allocate an index for every chunk.

Write independently understandable topical chunks with `qubicdb_write`. Metadata is a JSON-encoded string of string values: keep source URI/path, document identity, version, and chunk identity as useful. Preserve facts in content rather than expecting metadata to supply missing meaning. Do not copy credentials or private reasoning into the knowledge base.

Exact duplicate content reuses a neuron without updating its source/version metadata. For a real revision, write what changed with new version/source details and a `supersedes` reference to the prior neuron. Old versions remain searchable; this is not an automatic upsert or retention policy.

Retrieve using `qubicdb_search`. Use natural-language cues for semantic matching when the model is loaded and concrete identifiers for lexical relevance. For a mandatory document/version restriction, set `strict: true` with the metadata. Hybrid search has no per-call vector switch and is not an exact-match or exhaustive listing API.

Use `qubicdb_context` for approximate-budget unfiltered background. For citations, version filters, or precise prompt budgets, select search results and build context locally, keeping `(index_id, _id, source)` references. `recall` is currently energy-ordered, not guaranteed newest-first. Use the authorized REST `find/count` integration for exact filters when available; do not invent an MCP command tool.

The engine manages decay, consolidation and associations; index lifecycle is not a document-version state machine. Keep a real source of record for documents and decisions. A statistics export is not a full knowledge-base backup.
