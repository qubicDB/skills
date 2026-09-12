# Semantic vectors, spatial structure and learned relationships

## Three different representations

1. **Content/metadata** express the fact and its provenance.
2. **Embedding** represents semantic content; the bundled MiniLM produces 384 values. Search compares query/content embeddings with cosine similarity, alongside lexical and activation factors.
3. **Position and synapses** are the organic graph/space. Positions start at the configured minimum dimension (normally 3), are separate from embeddings, and can grow with density. Search does not use Euclidean `position` distance as its similarity metric.

Do not invent a coordinate meaning such as “axis 1 = security,” supply coordinates through MCP, or treat two nearby points as proof of a factual dependency. Use actual edge evidence and the content. Graph proximity is a learned association, not a typed knowledge-graph relation or a causal proof.

## What actually forms relationships

In the verified release, the worker calls Hebbian learning on successful **write**, **read**, and **each returned search result**. Neurons activated within a five-second window in one index form or strengthen bidirectional associations, subject to the current neighbour limit (initially 50 per neuron). A new edge starts at weight 0.2; further coactivation strengthens it. Existing-link strengthening asynchronously pulls the pair together, attracts neighbourhoods toward their centroids, and repels unconnected points. Sleeping-brain reorganisation can continue this process.

This is temporal coactivation, not an LLM checking whether two facts logically belong together. Rapidly importing unrelated documents or repeatedly retrieving broad noisy sets can create/strengthen accidental relationships. `recall`, exact command `find/count`, and graph inspection do not fire each returned neuron; use them for inventory/export/inspection when learning associations is not the purpose. They may still load/wake the index.

For ordinary work, fetch a small set of genuinely relevant decisions/dependencies and use them together. This lets real use establish associations. Do not run ritual refresh/read loops to “train the brain,” manufacture relevance, or add fixed sleeps between ordinary calls. For an ingestion design, preserve coherent units and domain boundaries; verify topology on a disposable sample before large mixed-topic imports. Current MCP has no per-write coactivation-disable switch.

## Deliberately express a relationship

When a relationship itself is useful knowledge, state it in a neuron with source and references: “The retry service must retain the original payment key because the gateway deduplicates by that key.” This preserves the semantic/causal explanation even when learned edges weaken or ranking changes.

Metadata `parent_thread`, `parent_id`, `supersedes`, or a written ID is only an application reference. It does not itself create an edge. There is no MCP `link`, `set_position`, or `set_embedding` tool.

The authorized REST `POST /v1/write` **does** accept a top-level `parent_id`: it places a new neuron close to that parent's position (roughly ±0.1 per coordinate), or falls back to random placement if the parent is missing. It does not guarantee a typed parent edge. Use it when explicitly constructing spatially grouped memory through REST, with a verified parent in the same index. It is different from putting `parent_id` inside metadata. REST metadata is an object; MCP metadata is a JSON string. The REST `tags` field is currently accepted but not applied, so do not claim tags were stored without inspecting the response.

```json
{"content":"The gateway deduplicates payment attempts by the original request key.","parent_id":"VERIFIED_PARENT_ID","metadata":{"source":"gateway-contract.md","type":"constraint"}}
```

## Inspect rather than infer

For a requested relationship/cluster investigation, use `/v1/graph` (nodes, positions, edges), `/v1/synapses` (weights/cofire counts), and `/v1/activity` with the selected `X-Index-ID`. Compare actual before/after edge weights and positions when testing an ingestion or retrieval strategy. The activity endpoint synthesizes recent state, not a complete append-only audit log. Avoid extra `read` calls merely to inspect positions when their activation would alter the measurement.

Search `depth` controls traversal of existing graph links, with hop attenuation and a threshold. It does not request deeper model reasoning, expose a causal path, or promise that every neighbour is included. Only previously unseen candidates are added; hybrid scoring may already seed many neurons. Increasing depth cannot repair a wrong index or incorrect fact. API/MCP depth 0 clamps to 2, so it is not a no-graph mode.

Dimensions expand when neuron count/current dimension exceeds 100, within configured bounds; deletion can contract a sparse matrix. These spatial dimensions are not the embedding dimension. Do not create a new index just because spatial dimensionality grew.
