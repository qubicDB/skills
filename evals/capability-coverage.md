# QubicDB capability and decision coverage

This map addresses how an agent should use QubicDB, not a model ranking. Source reviewed at core commit `5d3ec2fddfd9503c1a5c6ef932a08a330ba7e512`; runtime is the pinned Docker Hub bundled image in `compose.yml`. Source claims, live observations and agent guidelines are distinguished. “Source reviewed” does not mean every production failure mode was reproduced.

| Need/capability | Agent decision | Actual mechanism/surface | Implementation | Evidence |
|---|---|---|---|---|
| A known memory | Read its ID instead of semantic/all-data retrieval | MCP read; worker fires the neuron | pkg/api/mcp_backend.go; pkg/concurrency/brain_worker.go | Live read and original-preservation checks |
| A topical question | Retrieve the relevant subset, then assess sources and revisions | Hybrid search, strict metadata and bounded output | pkg/engine/search.go; pkg/mcp/server.go | Live hybrid contrast and strict-filter checks |
| A complete collection | Count, enumerate stable IDs, verify distinct count, write to disk | REST command count/find; recall/search are capped | pkg/protocol/executor.go; pkg/api/server.go | 520 records: 500 MCP recall, 100 REST recall, 520 verified export |
| A complete server backup | Distinguish known API records from all physical storage/internal state | Storage snapshots/WAL/manifest; API export is not a backup | pkg/persistence/store.go; pkg/api/server.go | Source reviewed; no whole-server disaster-recovery claim |
| New persistent knowledge scope | Reuse topic/session scope; create only a distinct durable domain | Registry identity separate from loaded worker/storage | pkg/registry/registry.go; pkg/concurrency/pool.go | Live registration and loaded/registered distinction |
| Selected projects together | Keep explicit scope/provenance; strict restrictions require per-index searches | Multi-search JSON-string IDs; per-index errors | pkg/api/mcp_backend.go; pkg/mcp/server.go | Live selected-index and soft/strict checks |
| Broad project discovery | Use global only when warranted; do not claim unloaded coverage | Loaded workers only; merge uses activation proxy | pkg/api/mcp_backend.go | Live broad scope check; failure-merging behavior source reviewed |
| One reusable meaning | Keep qualifications with their decision; split independently changing facts | One write creates one neuron | pkg/engine/matrix_ops.go; pkg/core/content_validation.go | Guidance traced to data and retrieval behavior |
| Unchanged fact versus repeated event | Reuse fact ID; give a distinct event real event content | Exact content hash deduplication before metadata | pkg/engine/matrix_ops.go; pkg/core/types.go | Live duplicate and revision checks |
| Correction versus erasure | Append a sourced revision; do not claim original deletion | No automatic supersession; direct mutations disabled | pkg/protocol/executor.go; pkg/api/server.go | Live mutation rejection and original retained |
| Large documents | Coherent source/versioned sections, not a mixed transcript neuron | 64KiB default; internal chunks average into one vector | pkg/core/content_validation.go; pkg/vector/vectorizer.go | Core validation tests; chunking source reviewed |
| Conceptual versus exact search | Use concepts for recall, exact ID/filter for deterministic/no-vector lookup | Lexical plus embeddings, no per-query switch | pkg/engine/search.go; pkg/protocol/query.go | Live nonlexical contrast and exact filter |
| Embedding availability | Check actual initialization/behavior, not only config/health | Model load failures can leave lexical fallback | pkg/vector/vectorizer.go; pkg/engine/search.go | Bundled MiniLM initialized and semantic contrast passed |
| Code, markup and multilingual evidence | Verify exact content and relevance; do not infer model competence | Text cleaner and English sentence chunker affect embedding input | pkg/vector/text_cleaner.go; pkg/vector/vectorizer.go | Source reviewed; no multilingual quality benchmark claim |
| Spatial versus semantic representation | Do not assign semantic axes or rank by position distance | Position separate from Embedding; scorer ignores Euclidean position | pkg/core/types.go; pkg/engine/search.go | Live initial 3D position and growth to 6D; 384D model |
| Meaningful associations | Relevant joint use can teach; noisy broad reads/imports can teach noise | Write/read/search trigger 5-second coactivation | pkg/concurrency/brain_worker.go; pkg/synapse/hebbian.go | Live edge weight/cofire count increased after joint reads |
| Spatial grouping at formation | REST top-level parent_id can influence placement; metadata cannot | Parent perturbation, random fallback if missing | pkg/api/server.go; pkg/engine/matrix_ops.go | Live parent bounds and ignored tags check |
| Cluster evolution | Inspect actual weights/positions; no promise of typed causality | Attraction, centroid pull, repulsion and sleeping reorganisation | pkg/synapse/hebbian.go; pkg/daemon/workers.go | Live pair distance decreased; synapse unit tests passed |
| Spatial growth | Do not shard just because geometry grows | Count/dimension >100 expansion; deletion can contract | pkg/engine/matrix_ops.go | 520-neuron index reached six spatial dimensions |
| Depth | Use for existing graph exploration, not deeper model reasoning | Attenuated traversal, threshold, 0 clamped to 2 | pkg/engine/search.go; pkg/api/mcp_backend.go | Live depth-default and engine tests |
| Inventory without teaching | Prefer recall/exact find/graph inspection for bulk observation | No per-neuron fire on recall/find | pkg/concurrency/brain_worker.go; pkg/protocol/executor.go | 520 exported records retained accessCount=1; recall preserved cofire count |
| Current versus historical truth | Resolve applicable versions/dates/supersession, not energy rank | Activity boosts ranking; supersedes is ordinary metadata | pkg/engine/search.go; pkg/core/types.go | Source and live original/correction preservation |
| Limited prompt context | Choose bounded relevant evidence; preserve filter/citation requirements | Context uses 50 candidates, approximate budget, first oversized item stops | pkg/api/mcp_backend.go | Live small and oversized budget checks |
| Long-task checkpoint/resume | Keep objective, latest constraints, verified outcomes, remaining work and evidence IDs | Application handoff; no automatic semantic summary/chain traversal | Skill references/long-tasks.md; pkg/mcp/server.go | Operational guidance; not presented as a long-context model benchmark |
| Consolidation | Do not expect it to summarize, merge facts, or settle contradictions | Sleeping daemon; age>=30min, accesses>=10, energy<0.5; increments depth | pkg/concurrency/brain_worker.go; pkg/core/types.go | Core/concurrency/daemon tests passed |
| Decay and forgetting | Do not promise TTL erasure of ordinary neurons | BaseEnergy0.1 above alive threshold0.01; weak synapses prune | pkg/core/types.go; pkg/synapse/hebbian.go | Core/synapse tests passed |
| Index lifecycle | Loading/waking/eviction are not create/delete of knowledge | Active/idle/sleep/dormant and persisted worker reload | pkg/lifecycle/manager.go; pkg/concurrency/pool.go | Lifecycle tests and live wake/sleep/persistence |
| Durability | Do not equate in-memory acknowledgement or persisted:true with verified disk guarantee | Scheduled/explicit persistence, fsync/WAL; handler ignores persist error | pkg/persistence/store.go; pkg/api/server.go | Persistence tests and restart test; failure acknowledgement source reviewed |
| Sentiment | Treat as secondary ranking signal; do not fabricate returned scores | VADER internal fields omitted from MCP documents | pkg/sentiment/analyzer.go; pkg/protocol/query.go | Source reviewed; no measured-emotion claim |
| Registry changes | Do not treat metadata/UUID changes as data migration or erasure | Registry update/delete separate from matrix storage | pkg/registry/registry.go; pkg/api/server.go | Source reviewed |
| Unsupported commands/fields | Use the working surface, never silently pretend success | Disabled update/delete/activate; unregistered aggregate; dropped insert metadata/tags | pkg/protocol/executor.go; pkg/api/server.go | Live mutation and ignored-tags checks; protocol tests |
| Operational acknowledgements | Inspect effect/error evidence before reporting admin success | Daemon pause/resume and GC placeholders; stats-only export | pkg/api/server.go | Source reviewed; no claim these features operate |
| MCP discovery and prompt templates | Use actual tool schema; optional prompt is a recipe, not retrieved data | 10 tools, optional qubicdb_memory_recall prompt | pkg/mcp/server.go; pkg/core/brain.go | Live schema check; prompt and allowlist validation source reviewed |
| Transport and access scope | Use configured endpoint/credentials and host authorization; namespaces are not access control | API key MCP middleware, Basic admin, deployment allowlists/rate limits | pkg/mcp/server.go; pkg/api/server.go | Live MCP/admin contracts and native Codex lookup from earlier pass |

## Public HTTP coverage index

Each documented route is accounted for below; method names are not evidence of a working operation. The behavioral map above classifies working, automatic, disabled and placeholder behavior.

| Method/path | Documented purpose | Decision family |
|---|---|---|
| `GET /health` | Health probe | Health/index lifecycle/statistics |
| `POST /v1/write` | Write a memory (create neuron) | Formation, point read, exact query; command limits above |
| `GET /v1/read/{id}` | Read one neuron by ID | Formation, point read, exact query; command limits above |
| `GET /v1/recall` | Recall neurons (list memory) | Retrieval granularity and completeness |
| `GET /v1/search` | Search neurons (GET) | Retrieval granularity and completeness |
| `POST /v1/search` | Search neurons (POST) | Retrieval granularity and completeness |
| `POST /v1/context` | Build token-aware LLM context | Retrieval granularity and completeness |
| `POST /v1/command` | Execute MongoDB-like command | Formation, point read, exact query; command limits above |
| `PUT /v1/touch` | Mutation disabled | Disabled direct neuron mutation |
| `POST /v1/touch` | Mutation disabled | Disabled direct neuron mutation |
| `DELETE /v1/forget/{id}` | Mutation disabled | Disabled direct neuron mutation |
| `POST /v1/fire/{id}` | Mutation disabled | Disabled direct neuron mutation |
| `GET /v1/brain/state` | Get brain state | Health/index lifecycle/statistics |
| `POST /v1/brain/wake` | Force brain wake | Health/index lifecycle/statistics |
| `POST /v1/brain/sleep` | Force brain sleep | Health/index lifecycle/statistics |
| `GET /v1/brain/stats` | Per-index brain statistics | Health/index lifecycle/statistics |
| `GET /v1/stats` | Global pool + lifecycle statistics | Health/index lifecycle/statistics |
| `GET /v1/synapses` | List synapses for an index | Inspect actual associations/spatial state |
| `GET /v1/graph` | Get graph nodes/edges for visualization | Inspect actual associations/spatial state |
| `GET /v1/activity` | Get recent neuron/synapse activity | Inspect actual associations/spatial state |
| `GET /v1/registry` | List registry entries | Index identity; separate from data lifecycle |
| `POST /v1/registry` | Create registry entry | Index identity; separate from data lifecycle |
| `GET /v1/registry/{uuid}` | Get registry entry | Index identity; separate from data lifecycle |
| `PUT /v1/registry/{uuid}` | Update registry entry | Index identity; separate from data lifecycle |
| `DELETE /v1/registry/{uuid}` | Delete registry entry | Index identity; separate from data lifecycle |
| `POST /v1/registry/find-or-create` | Find-or-create registry entry | Index identity; separate from data lifecycle |
| `POST /admin/login` | Validate admin credentials | Explicit operational scope; persistence/reset/delete/auth |
| `GET /admin/indexes` | List active indexes in worker pool | Explicit operational scope; persistence/reset/delete/auth |
| `GET /admin/indexes/{indexId}` | Get index details | Explicit operational scope; persistence/reset/delete/auth |
| `DELETE /admin/indexes/{indexId}` | Delete index from memory/disk and optionally registry | Explicit operational scope; persistence/reset/delete/auth |
| `POST /admin/indexes/{indexId}/reset` | Truncate index data | Explicit operational scope; persistence/reset/delete/auth |
| `POST /admin/indexes/{indexId}/wake` | Force wake for index | Explicit operational scope; persistence/reset/delete/auth |
| `POST /admin/indexes/{indexId}/sleep` | Force sleep for index | Explicit operational scope; persistence/reset/delete/auth |
| `GET /admin/indexes/{indexId}/export` | Export index stats snapshot | Inspect effect; placeholders/statistics limits above |
| `GET /admin/daemons` | Get daemon status | Inspect effect; placeholders/statistics limits above |
| `POST /admin/daemons/pause` | Pause daemons (logical endpoint) | Inspect effect; placeholders/statistics limits above |
| `POST /admin/daemons/resume` | Resume daemons (logical endpoint) | Inspect effect; placeholders/statistics limits above |
| `POST /admin/gc` | Trigger garbage collection hook | Inspect effect; placeholders/statistics limits above |
| `POST /admin/persist` | Force persist all active indexes | Explicit operational scope; persistence/reset/delete/auth |
| `GET /v1/config` | Get active runtime configuration | Requested operational tuning; server-wide settings |
| `POST /v1/config` | Patch runtime configuration | Requested operational tuning; server-wide settings |
| `GET /admin/config` | Alias of GET /v1/config | Requested operational tuning; server-wide settings |
| `POST /admin/config` | Alias of POST /v1/config | Requested operational tuning; server-wide settings |

## Decision rules added to the skills

The main entrypoint routes conditionally to knowledge granularity/index decisions, actual spatial/semantic relationships, task evolution/recovery, and detailed capability boundaries. Search adds complete-data enumeration; write adds formation/relationship and handoff guidance. The helper exports a counted set of API-visible neuron documents, not an entire restorable brain. Supporting detail is loaded for the relevant workflow instead of being forced into every task.
