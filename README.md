# QubicDB Agent Skills

Brain-like organic memory for AI agents and IDE assistants — powered by [QubicDB](https://github.com/qubicDB/qubicdb).

Includes ready-to-use configurations for **Windsurf**, **Cursor**, **VS Code (GitHub Copilot)**, and **Claude Code**. Also available as a **Claude Code Plugin** via marketplace.

---

## Quick Start

### 1. Start QubicDB

**Option A: Non-vector Docker Compose**

```bash
docker compose -f docker-compose.qubicdb.yml up -d
```

**Option B: Vector Docker Compose**

Clone `qubicdb` and `skills` side-by-side:

```text
your-folder/
├── qubicdb/
└── skills/
```

Then run:

```bash
docker compose -f docker-compose.qubicdb.vector.yml up -d --build
```

`docker-compose.qubicdb.vector.yml` expects the vector model at `../qubicdb/dist/MiniLM-L6-v2.Q8_0.gguf`.

**Important:** Download the GGUF model first. Full download commands are documented in [SETUP.md](./SETUP.md).

Helper instructions and local patch scripts are also available in the main `qubicdb` repo:

- [patches/windows-local-vector](https://github.com/qubicDB/qubicdb/tree/main/patches/windows-local-vector)
- [patches/linux-local-vector](https://github.com/qubicDB/qubicdb/tree/main/patches/linux-local-vector)
- [patches/macos-local-vector](https://github.com/qubicDB/qubicdb/tree/main/patches/macos-local-vector)
- [patches/vector-wrapper](https://github.com/qubicDB/qubicdb/tree/main/patches/vector-wrapper)

**Option C: Bundled Vector Docker Compose**

```bash
docker compose -f docker-compose.qubicdb.bundled.yml up -d
```

This lane uses `qubicdb/qubicdb-bundled:latest`, which includes the example MIT-licensed `MiniLM-L6-v2.Q8_0.gguf` model (about 25 MB). No local build or `dist` mount is required.

**Option D: Docker Run (non-vector)**

```bash
docker pull qubicdb/qubicdb:latest
docker pull qubicdb/qubicdb-ui:latest

docker network create qubicdb-net

docker run -d \
  --name qubicdb \
  --network qubicdb-net \
  -p 6060:6060 \
  -v qubicdb_data:/app/data \
  -e QUBICDB_HTTP_ADDR=:6060 \
  -e QUBICDB_DATA_PATH=/app/data \
  -e QUBICDB_ADMIN_ENABLED=true \
  -e QUBICDB_ADMIN_USER=admin \
  -e QUBICDB_ADMIN_PASSWORD=changeme \
  -e QUBICDB_MCP_ENABLED=true \
  -e QUBICDB_MCP_PATH=/mcp \
  -e QUBICDB_MCP_STATELESS=true \
  -e QUBICDB_MCP_RATE_LIMIT_RPS=30 \
  -e QUBICDB_MCP_RATE_LIMIT_BURST=60 \
  -e QUBICDB_MCP_ENABLE_PROMPTS=true \
  -e QUBICDB_MCP_API_KEY=qubicdb-mcp-secret-key \
  -e QUBICDB_ALLOWED_ORIGINS=http://localhost:6060,http://localhost:8080,http://127.0.0.1:8080 \
  -e QUBICDB_REGISTRY_ENABLED=false \
  qubicdb/qubicdb:latest

docker run -d \
  --name qubicdb-ui \
  --network qubicdb-net \
  -p 8080:80 \
  qubicdb/qubicdb-ui:latest
```

> 📖 For full non-vector setup, vector setup, vector parameters, and troubleshooting, see [SETUP.md](./SETUP.md).

Verify:

```bash
curl http://localhost:6060/health
```

Admin UI: `http://localhost:8080` — login with `admin` / `changeme`.

> **Note:** The `QUBICDB_MCP_API_KEY` must match the `X-API-Key` header in your IDE's MCP config. Change both if you use a custom key.

### 2. Install skills

**Option A: Claude Code Plugin (recommended for Claude Code)**

```bash
/plugin marketplace add qubicDB/skills
/plugin install qubicdb-skills@qubicdb-agent-skills
```

**Option B: Copy IDE folder** — pick your IDE below, copy the relevant folder into your project root.

### 3. Start using

Start a conversation — the AI will use QubicDB as persistent memory automatically.

---

## Windsurf

Copy `.windsurf/` into your project root. Add MCP server in Windsurf settings (or use `mcp_config.json` as reference):

```
your-project/
└── .windsurf/
    ├── rules/
    │   └── qubic.md              ← always-on rules (191 lines)
    ├── skills/
    │   └── qubic/
    │       └── SKILL.md          ← skill definition (140 lines)
    └── workflows/
        ├── qubic-init.md         ← /qubic-init workflow
        ├── qubic-search.md       ← /qubic-search workflow
        └── qubic-write.md        ← /qubic-write workflow
```

MCP config for Windsurf settings:

```json
{
  "mcpServers": {
    "qubicdb": {
      "serverUrl": "http://localhost:6060/mcp",
      "headers": {
        "X-API-Key": "qubicdb-mcp-secret-key"
      }
    }
  }
}
```

---

## Cursor

Copy `.cursor/` into your project root:

```
your-project/
└── .cursor/
    ├── mcp.json                  ← MCP server config
    └── rules/
        ├── qubic-rules.mdc      ← always-on rules (full port of Windsurf rules)
        ├── qubic-skill.mdc      ← skill definition (full port of Windsurf skill)
        ├── qubic-init.mdc       ← init workflow
        ├── qubic-search.mdc     ← search workflow
        └── qubic-write.mdc      ← write workflow
```

---

## VS Code (GitHub Copilot)

Copy `.vscode/` and `.github/` into your project root:

```
your-project/
├── .vscode/
│   └── mcp.json                  ← MCP server config
└── .github/
    └── copilot-instructions.md   ← all rules + skills + workflows combined
```

---

## Claude Code

Copy `.claude/` into your project root:

```
your-project/
└── .claude/
    ├── CLAUDE.md                     ← project rules (always loaded)
    ├── settings.local.json           ← MCP server config
    └── skills/
        ├── qubic/
        │   └── SKILL.md              ← main skill definition
        ├── qubic-init/
        │   └── SKILL.md              ← /qubic-init skill
        ├── qubic-search/
        │   └── SKILL.md              ← /qubic-search skill
        └── qubic-write/
            └── SKILL.md              ← /qubic-write skill
```

---

## What's Included

### Per-IDE Files

| IDE | MCP Config | Rules/Skills |
|-----|-----------|--------------|
| **Windsurf** | `mcp_config.json` (add in settings) | `.windsurf/rules/` + `.windsurf/skills/` + `.windsurf/workflows/` |
| **Cursor** | `.cursor/mcp.json` | `.cursor/rules/*.mdc` (5 files) |
| **VS Code** | `.vscode/mcp.json` | `.github/copilot-instructions.md` |
| **Claude Code** | `.claude/settings.local.json` | `.claude/CLAUDE.md` + `.claude/skills/` (4 skills) |

### Content (identical across all IDEs)

| Content | Description |
|---------|-------------|
| **Rules** | Always-on behavior: session lifecycle, forced behaviors (no fabrication, auto-write triggers), persona, naming conventions |
| **Skill** | Architecture (index/thread/neuron model), MCP tool reference, metadata types, usage examples |
| **Init workflow** | Register project brain index, load existing memories |
| **Search workflow** | Spreading activation search, metadata filters, parameters |
| **Write workflow** | Store decisions, preferences, todos, facts with metadata |

---

## How It Works

QubicDB gives your AI assistant a persistent, organic memory across conversations:

- **One brain per project** — `brain-{project}` index, created once, reused forever
- **One thread per conversation** — `conv-{uuid}` groups neurons within a session
- **Hebbian learning** — memories that fire together, wire together
- **Spreading activation search** — finds related memories through synapse connections
- **Lifecycle states** — Active → Idle → Sleeping → Dormant with automatic consolidation

---

## Claude Code Plugin (Marketplace)

This repo is a **Claude Code Plugin Marketplace**. Install directly:

```bash
# Add the marketplace
/plugin marketplace add qubicDB/skills

# Install core skills (MCP memory: write, search, recall, context)
/plugin install qubicdb-skills@qubicdb-agent-skills

# Install experimental skills (multi-index, agent-to-agent, sentiment, REST API, RAG)
/plugin install qubicdb-experimental@qubicdb-agent-skills
```

Plugin structure:

```
plugins/
├── qubicdb-skills/              ← core plugin
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json                ← auto-configures MCP server
│   └── skills/
│       ├── qubic/SKILL.md
│       ├── qubic-init/SKILL.md
│       ├── qubic-search/SKILL.md
│       └── qubic-write/SKILL.md
└── qubicdb-experimental/        ← experimental plugin
    ├── .claude-plugin/plugin.json
    └── skills/
        ├── multi-index-research/SKILL.md
        ├── agent-to-agent/SKILL.md
        ├── conversation-chains/SKILL.md
        ├── sentiment-journal/SKILL.md
        ├── knowledge-base-server/SKILL.md
        └── rag-context-assembly/SKILL.md
```

---

## New in v1.1.0: Cross-Index MCP Tools

QubicDB now supports **global and multi-index operations** via MCP:

| Tool | Description |
|------|-------------|
| `qubicdb_list_indexes` | List all registered indexes with stats |
| `qubicdb_global_search` | Search across ALL active indexes |
| `qubicdb_multi_search` | Search across a specific list of indexes |
| `qubicdb_recent_indexes` | Get most recently active indexes |

**Use case:** Agents can now discover relationships across hundreds of repositories/indexes — perfect for monorepo insights and cross-project memory.

---

## Experimental Skills

The `qubicdb-experimental` plugin showcases diverse use cases beyond IDE memory:

| Skill | Description |
|-------|-------------|
| **multi-index-research** | Separate brains per research domain, cross-reference between them |
| **agent-to-agent** | Multiple agents sharing memory through a common brain with role metadata |
| **conversation-chains** | Track multi-session conversations with thread_id chaining and parent links |
| **sentiment-journal** | Emotion-aware journaling leveraging built-in VADER sentiment analysis |
| **knowledge-base** | Build a persistent knowledge base with rich metadata and hybrid search |
| **rag-context-assembly** | Token-budgeted context assembly using spreading activation (not just vector similarity) |

> Each skill includes full Prerequisites with Docker setup and MCP config for all 4 IDEs.

---

## Links

- **QubicDB Server:** [github.com/qubicDB/qubicdb](https://github.com/qubicDB/qubicdb)
- **Admin UI:** [github.com/qubicDB/qubicdb-ui](https://github.com/qubicDB/qubicdb-ui)
- **Docker Hub:** [hub.docker.com/r/qubicdb/qubicdb](https://hub.docker.com/r/qubicdb/qubicdb)
- **Website:** [qubicdb.github.io/qubicdb-web](https://qubicdb.github.io/qubicdb-web/)
- **API Docs:** [qubicdb.github.io/docs](https://qubicdb.github.io/docs/)
