---
name: qubicdb-conversation-chains
description: Track long multi-session conversations using thread_id chaining. Resume context across sessions, link related conversations, and build conversation trees.
---

# Conversation Chains

Use QubicDB metadata to **chain conversations** across sessions. Each conversation gets a unique `thread_id`, and you can link them by storing parent references. QubicDB's spreading activation naturally connects related topics across threads.

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

## Concept

```
Session 1 (conv-001)          Session 2 (conv-002)          Session 3 (conv-003)
"Set up PostgreSQL"    →     "Add user auth"         →     "Fix login bug"
    │                             │                             │
    └── thread_id: conv-001      └── thread_id: conv-002      └── thread_id: conv-003
                                     parent: conv-001              parent: conv-002
```

## Starting a New Conversation Chain

```
# Session 1: Start a new chain
qubicdb_write(index_id: "brain-myproject", content: "Session started: Setting up PostgreSQL database for the project.", metadata: "{\"type\": \"session-start\", \"thread_id\": \"conv-001\"}")

# Store decisions during the session
qubicdb_write(index_id: "brain-myproject", content: "Decided to use PostgreSQL 16 with pgvector extension for future vector search needs.", metadata: "{\"type\": \"decision\", \"thread_id\": \"conv-001\"}")

# End session with summary
qubicdb_write(index_id: "brain-myproject", content: "Session summary: Set up PostgreSQL 16, created users table, added pgvector extension, configured connection pooling.", metadata: "{\"type\": \"summary\", \"thread_id\": \"conv-001\"}")
```

## Resuming in a New Session

```
# Session 2: Load previous context
qubicdb_search(index_id: "brain-myproject", query: "PostgreSQL setup decisions", metadata: "{\"thread_id\": \"conv-001\"}", strict: true)

# Link to parent conversation
qubicdb_write(index_id: "brain-myproject", content: "Session started: Adding user authentication. Continuing from conv-001 (PostgreSQL setup).", metadata: "{\"type\": \"session-start\", \"thread_id\": \"conv-002\", \"parent_thread\": \"conv-001\"}")
```

## Finding Related Conversations

```
# Find all sessions about a topic (soft search across all threads)
qubicdb_search(index_id: "brain-myproject", query: "PostgreSQL database configuration", depth: 3, limit: 20)

# Find all session summaries
qubicdb_search(index_id: "brain-myproject", query: "session summary", metadata: "{\"type\": \"summary\"}", strict: true)

# Build full context from conversation chain
qubicdb_context(index_id: "brain-myproject", cue: "authentication and database decisions across all sessions", max_tokens: 2000)
```

## Use Cases

- **Multi-day development** — chain daily coding sessions
- **Customer journey** — track support interactions across tickets
- **Meeting notes** — link follow-up meetings to original discussions
- **Research progress** — chain literature review sessions
- **Debugging sessions** — link bug investigation across multiple attempts

## Key Properties

- **Spreading activation** naturally connects related topics across threads — even without explicit `parent_thread` links
- **Strict metadata filter** retrieves only memories from a specific thread
- **Soft boost** finds connections across threads while preferring the current one
- **Hebbian synapses** strengthen between neurons from different threads that share topics
- **Context assembly** can pull the most relevant memories across all threads within a token budget
