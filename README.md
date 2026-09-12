# QubicDB skills

Persistent project-memory workflows for Codex, Claude Code, and hosts supporting the Agent Skills format. Skills teach the agent when to create a neuron, reuse or correct memory, search one or several indexes, and assemble relevant context. They do not replace the MCP server or the host's native memory.

## Core skills

| Skill | Job |
|---|---|
| `qubic` | Integrate useful cross-session memory into an ongoing task |
| `qubic-init` | Connect or diagnose QubicDB and resolve the persistent project index |
| `qubic-search` | Choose scope, strict filters, semantic recall, or exact retrieval |
| `qubic-write` | Store durable facts, corrections and handoffs without duplicate noise |

Six optional recipes in `plugins/qubicdb-experimental` cover shared-agent findings, conversation handoffs, knowledge bases, research across indexes, context assembly, and journals. Install them when those workflows are useful; the core bundle does not require them.

## Install skills

### Codex

From a checkout of this repository, copy the four core skill directories into `~/.agents/skills/` (personal) or `.agents/skills/` in the intended project. Preserve each skill's `references/` and `agents/` subdirectories. Do not overwrite a locally modified skill without reviewing the difference.

```sh
mkdir -p ~/.agents/skills
cp -R plugins/qubicdb-skills/skills/qubic \
      plugins/qubicdb-skills/skills/qubic-init \
      plugins/qubicdb-skills/skills/qubic-search \
      plugins/qubicdb-skills/skills/qubic-write ~/.agents/skills/
```

Invoke `$qubic`, `$qubic-search`, `$qubic-write`, or `$qubic-init`, or let Codex select a relevant skill from its description. No Claude-specific runtime or hook is required. [Official Codex skill guidance](https://learn.chatgpt.com/docs/build-skills).

### Claude Code

```text
/plugin marketplace add qubicDB/skills
/plugin install qubicdb-skills@qubicdb-agent-skills
```

The optional bundle is `qubicdb-experimental@qubicdb-agent-skills`. Alternatively copy the skill directories into `~/.claude/skills/` or project `.claude/skills/`. [Official Claude Code skill guidance](https://code.claude.com/docs/en/skills).

## Connect the database

For a local deployment with its own embedding model, use the Docker Hub **`qubicdb/qubicdb-bundled`** image and `docker-compose.qubicdb.bundled.yml`. It includes MiniLM GGUF and its native embedding library. The base and vector-only variants are separate options, not substitutes for the bundled test target.

See [SETUP.md](SETUP.md) for host configuration and verification. Installing a skill does not create an MCP connection.

## Verified behavior and limits

- MCP metadata and multi-search index IDs are JSON-encoded **strings**.
- Exact duplicate content reuses/fires its neuron without updating metadata. Corrections are new, source-linked statements; old records remain.
- Global search covers loaded indexes only. Multi/global metadata boosts ranking; hard filters require separate strict single-index searches.
- Search has no per-call vector toggle. Runtime alpha is server-wide; zero removes semantic contribution but still embeds queries.
- Context budgets are estimates, and context output has no per-neuron IDs. Use selected search results when citations or strict filters matter.
- Read/search activate memories. Recall is energy-ordered, not guaranteed newest-first. Metadata references do not create synapses.
- Graph inspection, exact command queries, lifecycle and administration have REST surfaces beyond the ten MCP tools. Direct neuron mutation is disabled in the verified release.

The [capability reference](plugins/qubicdb-skills/skills/qubic/references/capabilities.md) explains when each surface is useful and which apparent features are not supported.

## Validate changes

Run the [disposable bundled evaluation](evals/README.md). It checks actual database behavior, including a semantic-versus-lexical contrast; YAML validation alone does not demonstrate correct agent decisions. The [behavioral cases](evals/cases.json) support independent agent runs and trace-based review.

Instruction design follows progressive disclosure and targeted triggers, with behavioral evaluation: [OpenAI skill eval example](https://developers.openai.com/blog/eval-skills), [Anthropic authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## How the agent chooses its memory behavior

The core workflow now separates read granularity, knowledge granularity and persistent index boundaries. It distinguishes a known record, a relevant working set, a cross-project question and a complete export; meaningful neuron formation and corrections; semantic vectors and learned spatial relationships; and checkpoints for changing long-running tasks. Read the [capability/decision coverage map](evals/capability-coverage.md) for source-backed mechanisms and evidence. Detailed instructions live in conditional references, with a counted JSONL enumeration helper for full-data requests.
