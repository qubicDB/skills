---
name: multi-index-research
description: Use multiple QubicDB indexes as isolated knowledge domains. Create separate brains for different research topics, then cross-reference between them for interdisciplinary insights.
---

# Multi-Index Research

QubicDB supports **unlimited isolated indexes** — each with its own organic memory matrix, Hebbian synapses, and lifecycle. Use this to create separate knowledge domains and cross-reference between them.

## Prerequisites

### 1. Pull and run QubicDB

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
  -e QUBICDB_ALLOWED_ORIGINS=http://localhost:8080 \
  -e QUBICDB_REGISTRY_ENABLED=false \
  -e QUBICDB_MCP_ENABLED=true \
  -e QUBICDB_MCP_PATH=/mcp \
  -e QUBICDB_MCP_STATELESS=true \
  -e QUBICDB_MCP_RATE_LIMIT_RPS=30 \
  -e QUBICDB_MCP_RATE_LIMIT_BURST=60 \
  -e QUBICDB_MCP_ENABLE_PROMPTS=true \
  -e QUBICDB_MCP_API_KEY=vaipn-mcp-key-2024 \
  qubicdb/qubicdb:latest

docker run -d \
  --name qubicdb-ui \
  --network qubicdb-net \
  -p 8080:80 \
  qubicdb/qubicdb-ui:latest
```

Verify:

```bash
curl http://localhost:6060/health
```

Admin UI: `http://localhost:8080` — login with `admin` / `changeme`.

> **Note:** The `QUBICDB_MCP_API_KEY` must match the `X-API-Key` header in your IDE's MCP config. Change both if you use a custom key.

### 2. Add MCP config to your IDE

**Claude Code** (`.claude/settings.local.json`):
```json
{
  "mcpServers": {
    "qubicdb": {
      "type": "url",
      "url": "http://localhost:6060/mcp",
      "headers": { "X-API-Key": "vaipn-mcp-key-2024" }
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "qubicdb": {
      "url": "http://localhost:6060/mcp",
      "headers": { "X-API-Key": "vaipn-mcp-key-2024" }
    }
  }
}
```

**VS Code** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "qubicdb": {
      "type": "http",
      "url": "http://localhost:6060/mcp",
      "headers": { "X-API-Key": "vaipn-mcp-key-2024" }
    }
  }
}
```

**Windsurf** (add in Windsurf MCP settings):
```json
{
  "mcpServers": {
    "qubicdb": {
      "serverUrl": "http://localhost:6060/mcp",
      "headers": { "X-API-Key": "vaipn-mcp-key-2024" }
    }
  }
}
```

### 3. Verify MCP connection

Run `qubicdb:registry_find_or_create(uuid: "test")` — if it returns a result, you're connected. If it fails, check `docker logs qubicdb` for errors.

## Concept

```
brain-neuroscience   ← neuroscience papers, findings, terminology
brain-ai-ml          ← machine learning concepts, architectures
brain-philosophy     ← philosophical frameworks, consciousness theories

Cross-reference: "How does Hebbian learning relate to transformer attention?"
  → Search brain-neuroscience for "Hebbian learning"
  → Search brain-ai-ml for "attention mechanism"
  → Synthesize connections
```

## Setup

```
# Create isolated indexes for each domain
qubicdb:registry_find_or_create(uuid: "brain-neuroscience")
qubicdb:registry_find_or_create(uuid: "brain-ai-ml")
qubicdb:registry_find_or_create(uuid: "brain-philosophy")
```

## Writing to Different Domains

```
# Store neuroscience knowledge
qubicdb:write(index_id: "brain-neuroscience", content: "Hebbian learning: neurons that fire together wire together. Synaptic strength increases with co-activation.", metadata: "{\"type\": \"concept\", \"source\": \"Hebb 1949\"}")

# Store ML knowledge
qubicdb:write(index_id: "brain-ai-ml", content: "Transformer attention mechanism computes weighted relationships between all token pairs in a sequence.", metadata: "{\"type\": \"concept\", \"source\": \"Vaswani et al. 2017\"}")
```

## Cross-Domain Search

```
# Search across domains for interdisciplinary connections
qubicdb:search(index_id: "brain-neuroscience", query: "associative learning synaptic plasticity", depth: 3, limit: 10)
qubicdb:search(index_id: "brain-ai-ml", query: "attention mechanism associative", depth: 3, limit: 10)

# Use context assembly for synthesis
qubicdb:context(index_id: "brain-neuroscience", cue: "biological learning mechanisms", max_tokens: 1000)
qubicdb:context(index_id: "brain-ai-ml", cue: "learning mechanisms in neural networks", max_tokens: 1000)
```

## Use Cases

- **Literature review** — separate indexes per research area
- **Competitive analysis** — one brain per competitor
- **Course notes** — one brain per subject
- **Project management** — one brain per project, cross-reference shared patterns
- **Multi-tenant apps** — one brain per user/customer

## Key Properties

- Each index has its own **Hebbian synapse network** — memories within a domain strengthen each other naturally
- **Spreading activation** finds connections you didn't explicitly create
- Indexes are fully **isolated** — no data leakage between domains
- **Lifecycle states** are per-index — inactive domains go to sleep automatically
