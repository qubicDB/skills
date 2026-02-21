---
name: qubicdb-agent-to-agent
description: Share memory between multiple AI agents through a common QubicDB index. Agents write findings with role metadata and read each other's discoveries via search.
---

# Agent-to-Agent Memory

Multiple AI agents can share a **common QubicDB brain** using metadata to identify who wrote what. This enables collaborative multi-agent workflows where agents build on each other's findings.

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
Agent A (Researcher)     Agent B (Analyst)      Agent C (Writer)
      │                       │                       │
      └─── writes ───┐       └─── writes ───┐       └─── writes ───┐
                      ▼                      ▼                      ▼
              ┌──────────────────────────────────────────────┐
              │           brain-shared-project               │
              │  Neuron: "Found dataset X" (role: researcher)│
              │  Neuron: "Pattern Y in data" (role: analyst) │
              │  Neuron: "Draft section Z" (role: writer)    │
              └──────────────────────────────────────────────┘
```

## Writing with Agent Identity

```
# Agent A (Researcher) stores findings
qubicdb_write(index_id: "brain-project-alpha", content: "Found dataset of 10k user interactions from Q3 2025 in S3 bucket.", metadata: "{\"role\": \"researcher\", \"agent_id\": \"agent-a\", \"type\": \"finding\"}")

# Agent B (Analyst) stores analysis
qubicdb_write(index_id: "brain-project-alpha", content: "User engagement drops 40% after day 7. Retention cliff correlates with feature discovery rate.", metadata: "{\"role\": \"analyst\", \"agent_id\": \"agent-b\", \"type\": \"analysis\"}")

# Agent C (Writer) stores drafts
qubicdb_write(index_id: "brain-project-alpha", content: "Executive summary: User retention analysis reveals a critical day-7 engagement cliff linked to feature discovery.", metadata: "{\"role\": \"writer\", \"agent_id\": \"agent-c\", \"type\": \"draft\"}")
```

## Reading Other Agents' Work

```
# Analyst reads researcher's findings
qubicdb_search(index_id: "brain-project-alpha", query: "dataset user interactions", metadata: "{\"role\": \"researcher\"}", strict: true)

# Writer reads analyst's conclusions
qubicdb_search(index_id: "brain-project-alpha", query: "engagement retention analysis", metadata: "{\"role\": \"analyst\"}", strict: true)

# Any agent gets full project context
qubicdb_context(index_id: "brain-project-alpha", cue: "project findings and analysis", max_tokens: 2000)
```

## Use Cases

- **Research pipelines** — crawler → analyzer → summarizer agents
- **Code review** — linter agent + security agent + style agent sharing findings
- **Customer support** — triage agent + specialist agent + follow-up agent
- **Content creation** — research agent + writing agent + editing agent
- **DevOps** — monitoring agent + diagnostic agent + remediation agent

## Key Properties

- **Hebbian connections** form between co-activated memories — if the analyst and researcher write about the same topic, QubicDB naturally strengthens those connections
- **Metadata filtering** (`strict: true`) lets each agent read only relevant memories
- **Soft boost** (`strict: false`) lets agents discover unexpected cross-role connections
- All agents share the **same spreading activation network**
