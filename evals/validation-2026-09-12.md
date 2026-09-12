# QubicDB validation record — 2026-09-12

## Source and operational reasoning pass (core skills 1.2.0)

The initial six-request compatibility pass below was insufficient to evaluate the full memory workflow. The subsequent work focused on understanding QubicDB and deriving the skill's choices from its actual implementation, rather than pursuing a model/provider benchmark.

- [34 capability/decision families and every documented HTTP route](capability-coverage.md) are mapped to their implementation and evidence. The map distinguishes agent choices, automatic engine behavior, disabled features and placeholder acknowledgements.
- Main guidance now separates neuron meaning/granularity, durable index boundaries, read scope, complete-data needs, semantic/spatial relationships, and evolving long-task state. Mode-specific detail is in conditional references.
- The expanded bundled live suite passed **13/13**. New checks cover actual coactivation/edge strengthening/spatial movement, REST parent placement versus metadata and ignored tags, and complete enumeration beyond recall limits.
- A 520-record index returned 500 through MCP recall and 100 through REST recall. The helper enumerated all 520 unique records using counted `_id` pages without firing those records; the index expanded to six spatial dimensions. This is a logical API export, not a transaction snapshot or restorable full-storage backup.
- A relationship probe measured edge weight increasing from 0.2 to about 0.656 after genuine coactivation, with pair distance decreasing. The spatial coordinates are separate from the 384-dimensional embeddings.
- Existing source test suites passed for core, engine, synapse, lifecycle, daemon, protocol, persistence, and concurrency.
- An independent source/skill review found no material actionable discrepancy in the reviewed decision guidance or enumeration helper.
- No claim is made that a broad model/long-context benchmark was completed. The task focus was corrected to skill reasoning and full capability understanding; model/provider work was stopped.

## Initial compatibility pass (core skills 1.1.0)

The following observations remain a historical record of the earlier narrower pass, not sufficient evidence by themselves for the revised task.

### Runtime and sources

- Core source: `qubicDB/qubicdb@5d3ec2fddfd9503c1a5c6ef932a08a330ba7e512`.
- Documentation source: `qubicDB/docs@3b33d21f81331e9084468bc0444c090fbfc603fb`.
- Previous skills: `qubicDB/skills@9ba5f61816a19db85661ef766259beda7809fd83`.
- Docker Hub image: `qubicdb/qubicdb-bundled@sha256:a05d69c08f29b084e944f69bb498e741a5fa6652ec8d01e0485946f6ad4ecf96`.
- Startup loaded `/app/dist/MiniLM-L6-v2.Q8_0.gguf`, 384 dimensions, alpha 0.6, query repeat 2. This is an embedding model, not a chat-completion model.
- All data for behavioral evaluations was synthetic, in dedicated localhost containers/volumes; no stage endpoint was used.

## Results

| Check | Result |
|---|---|
| Ten MCP tools and argument contract | Passed |
| Live contract suite from repository evaluation Compose | 10/10 passed |
| Real vector contribution | Passed: a nonlexical query had no hit at alpha 0 and found the relevant neuron at alpha 0.6; original alpha restored |
| Persistence after container restart | Original neuron content and metadata preserved |
| Skill entrypoints and relative references | All 10 validate |
| Independent original-skill run | Six requests completed, 7 operation calls, one correction write |
| Independent revised-skill run | Same six requests completed, 5 operation calls, one correction write |
| Native Codex implicit selection | Selected qubic-search/qubic without an explicit skill mention |
| Native Codex MCP lookup | Strict approved-only search returned the correct decision, source and neuron ID |
| Claude Code MCP connection | Connected |
| Native Claude Code agent run | Not completed: pre-existing configured model `qwen3.7-plus` returned HTTP 403 model-access denial before any task execution |

The two independent runs used separate seeded indexes. Both preserved the original decision, avoided a duplicate write, retained citations, and respected selected index scope. The small comparison showed no baseline correctness failure; it does not establish broad accuracy gains or universal trigger reliability. Across the ten SKILL.md entrypoints, text size fell from 50,984 to 24,521 bytes (51.9%). Supporting references are loaded conditionally.

## Actual harness limitation

The deployed QubicDB server advertises default MCP annotations marking even retrieval tools as non-read-only and destructive. A native Codex run with `approval_policy=never` was blocked by tool approval, despite successful MCP discovery. The equivalent read succeeded through Codex's built-in automatic approval review (`--approve-for-me`), without bypassing permissions. Skills now explain this distinction. Fixing server annotations requires a separate core/server release; changing Markdown cannot change the tool contract.

## Behavior now made explicit

Metadata and multi-search IDs are JSON strings. Exact duplicate content does not update metadata. Corrections append a new record and leave the original searchable. Global search sees loaded indexes, and cross-index metadata only boosts ranking. There is no per-query vector switch; alpha zero still computes embeddings. Recall is energy-ordered. Context budgets are approximate and lack per-neuron citations or filters. Graph, exact-query and administrative features have separate REST surfaces; direct neuron mutation is disabled.

## Reproduce

Use [the evaluation instructions](README.md), [live tests](test_live.py), and [behavioral cases](cases.json). Test deployment-specific schemas and approval behavior rather than inferring capability from a version string, successful health check, or a config flag. These tests are a bounded compatibility check, not a large-repository or multilingual retrieval benchmark.
