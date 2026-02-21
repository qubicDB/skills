---
name: qubicdb-knowledge-base
description: Build a persistent knowledge base using QubicDB via MCP. Store documents with rich metadata, search with hybrid vector + lexical scoring, and assemble token-budgeted context for LLM prompts.
---

# Knowledge Base

Use QubicDB as a **persistent knowledge base** via MCP. Store documents with rich metadata, search with hybrid scoring (vector + lexical + spreading activation), and assemble token-budgeted context for LLM prompts.

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

Run `qubicdb_registry_find_or_create(uuid: "test")` — if it returns a result, you're connected. If it fails, check `docker logs qubicdb` for errors.

## Setup

```
# Create the knowledge base index
qubicdb_registry_find_or_create(uuid: "kb-product-docs")
```

## Storing Documents

```
# Store with rich metadata
qubicdb_write(index_id: "kb-product-docs", content: "QubicDB supports hybrid search combining GGUF vector embeddings with lexical BM25-style scoring. The alpha parameter (0.0-1.0) controls the weight: 0.0 = pure lexical, 1.0 = pure semantic.", metadata: "{\"source\": \"docs/search.md\", \"category\": \"search\", \"version\": \"1.0.0\"}")

# Store another document
qubicdb_write(index_id: "kb-product-docs", content: "Neurons in QubicDB have lifecycle states: Active, Idle, Sleeping, Dormant. Inactive neurons decay over time through background daemons, simulating biological memory forgetting.", metadata: "{\"source\": \"docs/lifecycle.md\", \"category\": \"architecture\"}")
```

## Search (Hybrid: Vector + Lexical + Spreading Activation)

```
# Basic search
qubicdb_search(index_id: "kb-product-docs", query: "how does search scoring work", depth: 2, limit: 10)

# Search filtered by metadata
qubicdb_search(index_id: "kb-product-docs", query: "vector embedding", metadata: "{\"category\": \"search\"}", strict: true)
```

## Context Assembly

```
# Build token-budgeted context for LLM consumption
qubicdb_context(index_id: "kb-product-docs", cue: "How does QubicDB handle memory decay and lifecycle management?", max_tokens: 1500)
```

## Recent Documents

```
# List recent memories
qubicdb_recall(index_id: "kb-product-docs", limit: 20)
```

## Use Cases

- **Product documentation** — searchable knowledge base with category filtering
- **FAQ systems** — store Q&A pairs, search by question similarity
- **Internal wikis** — metadata-organized company knowledge
- **Chatbot memory** — persistent conversation history for any chatbot framework
- **Content recommendation** — spreading activation finds related content

## Key Properties

- **Hybrid search** — vector (GGUF) + lexical + spreading activation
- **Sentiment boost** — emotional tone matching in search results
- **Token-budgeted context** — `qubicdb_context` returns exactly what fits your LLM prompt
- **Metadata filtering** — strict or soft boost by any key-value pair
- **SDKs available** — TypeScript, JavaScript, Python, Go, Ruby, React, Next.js, Vue, Nuxt
