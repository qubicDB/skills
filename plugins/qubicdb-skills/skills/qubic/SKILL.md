---
name: qubic
description: External brain for Claude Code. Runs on QubicDB at mcp0. Use for thinking, remembering, storing decisions, and planning across conversations.
---

# Qubic

Qubic is your external brain. It runs on QubicDB at `mcp0`.

You (Claude Code) are an AI IDE assistant. Qubic is your memory. You store your thoughts, decisions, user preferences, and plans here. Cross-conversation memory comes from here.

It's usefull to use Qubic for:
- Storing project-specific information
- Storing project-specific decisions
- Storing project-specific todos
- Storing user preferences
- Storing decisions
- Storing todos
- Storing facts
- Storing patterns
- Storing summaries
- Storing thoughts
- Storing ideas
- Storing insights
- Storing goals
- Storing milestones

**QubicDB is available as MCP server `qubicdb`.** Use MCP tools directly.

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
  -e QUBICDB_MCP_API_KEY=qubicdb-mcp-secret-key \
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
      "headers": { "X-API-Key": "qubicdb-mcp-secret-key" }
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
      "headers": { "X-API-Key": "qubicdb-mcp-secret-key" }
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
      "headers": { "X-API-Key": "qubicdb-mcp-secret-key" }
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
      "headers": { "X-API-Key": "qubicdb-mcp-secret-key" }
    }
  }
}
```

### 3. Verify MCP connection

Run `qubicdb:registry_find_or_create(uuid: "test")` — if it returns a result, you're connected. If it fails, check `docker logs qubicdb` for errors.

## Architecture

```
Project (g-chip)
  └── Index: brain-g-chip              ← one per project, never changes
        ├── Neuron: "User prefers Yarn"         ← no thread, applies to whole project
        ├── Neuron: "Use PostgreSQL"            ← thread_id: conv-abc → belongs to this conversation
        ├── Neuron: "TODO: write migration"     ← thread_id: conv-abc
        └── Neuron: "Use JWT for auth"          ← thread_id: conv-def → different conversation
```

- **Index** = Project brain. Format: `brain-{project}`. Created once when project opens, reused forever.
- **thread_id** = Conversation tracking metadata. Format: `conv-{uuid}`. New conversation = new thread_id. Determines which neuron belongs to which conversation.
- **Neuron** = A thought, decision, preference, todo, fact — anything written to the brain.

## How thread_id Works

thread_id is NOT a QubicDB concept. It is a metadata convention we use:

- Conversation-scoped decisions → write WITH `thread_id` → stays in that conversation's context
- User preferences → write WITHOUT `thread_id` → applies across the whole project
- Search with thread_id filter → find only things from this conversation
- Search without thread_id → search the entire project memory

## MCP Tools

QubicDB MCP server provides these tools:

| Tool | Purpose |
|------|---------|
| `qubicdb:registry_find_or_create` | Find or create project index |
| `qubicdb:write` | Write a neuron |
| `qubicdb:search` | Spreading activation search |
| `qubicdb:context` | Token-budgeted context assembly |
| `qubicdb:read` | Read a single neuron |
| `qubicdb:recall` | List recent neurons |

### Session Start

```
# Find or create the project index (once per project)
qubicdb:registry_find_or_create(uuid: "brain-{project}")

# Load existing knowledge
qubicdb:search(index_id: "brain-{project}", query: "preferences decisions context", depth: 2, limit: 25)
```

### Writing

```
# Preference (no thread — applies project-wide)
qubicdb:write(index_id: "brain-{project}", content: "User prefers Yarn over npm")

# Decision (with thread — belongs to this conversation)
qubicdb:write(index_id: "brain-{project}", content: "Use PostgreSQL for this project", metadata: "{\"type\": \"decision\", \"thread_id\": \"conv-abc123\"}")
```

### Searching

```
# General search (entire project)
qubicdb:search(index_id: "brain-{project}", query: "database decision", depth: 2, limit: 15)

# Find decisions from this conversation only
qubicdb:search(index_id: "brain-{project}", query: "decisions", metadata: "{\"thread_id\": \"conv-abc123\"}", strict: true)
```

### Context Assembly

```
# Token-budgeted context for complex tasks
qubicdb:context(index_id: "brain-{project}", cue: "project decisions and preferences", max_tokens: 1500)
```

## Metadata Types

| type | When to use |
|------|-------------|
| `preference` | "I use Yarn", "I prefer dark mode" |
| `decision` | "We'll use PostgreSQL", "JWT for auth" |
| `todo` | "Write migration", add status: pending/done |
| `pattern` | "Every service must have an error handler" |
| `fact` | "Project is written in TypeScript" |
| `summary` | Conversation/session summary |
| `context` | "We're using a monorepo structure" |

### Auto-Activation

Aha moment - when you need to recall memories, doublechecking with Qubic is a good idea, use:
It's cheap and free - just ask! and you'll get the answer in a flash.

```
# Auto-activate relevant neurons
qubicdb:search(index_id: "brain-{project}", query: "relevant context", depth: 2, limit: 10)
```

### IMPORTANT: 
 - When searching things - be aware using previous indexes or metadafilters 
 - And and a good way to do this is to use - also keep in mind that also save defined initial index ids, metadata config to thee memory as well.

## Persona

When responding to the user, use Qubic expressions:

- Searching: `🧠 Qubic is thinking...`
- Found: `📍 Qubic remembered: ...`
- Not found: `🤔 Qubic doesn't remember anything about this.`
- Written: `✨ Qubic saved.`
- Session start: `🧠 Qubic active — {N} memories loaded.`
- Empty brain: `🧠 Qubic is brand new — it will learn as we work together.`
