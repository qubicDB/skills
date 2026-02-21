---
name: rag-context-assembly
description: Use QubicDB's token-budgeted context assembly for RAG (Retrieval Augmented Generation). Unlike traditional RAG, QubicDB uses spreading activation to find associatively related memories, not just vector-similar chunks.
---

# RAG Context Assembly

QubicDB's `/v1/context` endpoint (MCP: `qubicdb:context`) provides **token-budgeted context assembly** using spreading activation — a fundamentally different approach from traditional vector-only RAG.

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

## How It Differs from Traditional RAG

| Feature | Traditional RAG | QubicDB Context Assembly |
|---------|----------------|--------------------------|
| Retrieval | Top-K vector similarity | Spreading activation (associative) |
| Connections | None | Hebbian synapses between co-activated memories |
| Budget | Chunk count | Token count (max_tokens) |
| Scoring | cosine similarity only | hybrid (vector + lexical + activation energy + sentiment) |
| Evolution | Static | Memories strengthen/decay over time |
| Discovery | Only directly similar | Finds indirectly related via synapse chains |

## Usage

```
# Basic context assembly
qubicdb:context(index_id: "brain-myproject", cue: "How should we handle authentication?", max_tokens: 1500)

# Deep search context (more associative hops)
qubicdb:context(index_id: "brain-myproject", cue: "security best practices for our API", depth: 4, max_tokens: 2000)
```

## Building a RAG Pipeline

### Step 1: Populate the Knowledge Base

```
# Store project decisions
qubicdb:write(index_id: "brain-myproject", content: "We use JWT tokens for API authentication with 1-hour expiry. Refresh tokens stored in httpOnly cookies.", metadata: "{\"type\": \"decision\"}")

qubicdb:write(index_id: "brain-myproject", content: "All API endpoints require Bearer token except /health and /auth/login. Rate limiting is 100 req/min per user.", metadata: "{\"type\": \"decision\"}")

qubicdb:write(index_id: "brain-myproject", content: "User passwords are hashed with bcrypt (cost 12). We use argon2id for API key derivation.", metadata: "{\"type\": \"decision\"}")
```

### Step 2: Assemble Context for LLM Prompt

```
# When user asks: "How do we handle auth?"
context = qubicdb:context(index_id: "brain-myproject", cue: "authentication and security", max_tokens: 1500)

# The assembled context includes all related decisions —
# even ones not directly about "auth" but connected via synapses
# (e.g., rate limiting, password hashing)
```

### Step 3: Use in LLM Prompt

```
# Inject assembled context into your prompt:
system_prompt = f"""
You are a helpful assistant. Use the following project context:

{context}

Answer the user's question based on this context.
"""
```

## Spreading Activation vs Vector Search

```
Example knowledge base:
  A: "JWT tokens for auth" (directly relevant to "auth")
  B: "Rate limiting per user" (not about auth, but connected to A via API decisions)
  C: "bcrypt for passwords" (connected to A via security topic)
  D: "PostgreSQL for data storage" (unrelated)

Query: "How do we handle authentication?"

Vector-only RAG: Returns A, maybe C (cosine similarity)
QubicDB context: Returns A → follows synapses → B and C
                 (because A-B and A-C were co-activated during writes)
                 D is excluded (no synapse connection, low activation)
```

## Use Cases

- **Code assistant** — assemble project decisions as context for code generation
- **Customer support** — pull relevant product knowledge for response generation
- **Document Q&A** — token-budgeted retrieval for long-document questions
- **Agent planning** — assemble past decisions and preferences before taking action
- **Meeting prep** — gather all relevant context about a topic before a meeting

## Key Properties

- **Token-budgeted** — never exceeds your LLM's context window
- **Associative** — finds connections through Hebbian synapse chains
- **Energy-weighted** — frequently accessed memories rank higher
- **Depth-configurable** — control how many association hops to follow
- **Decay-aware** — old unused memories naturally rank lower
