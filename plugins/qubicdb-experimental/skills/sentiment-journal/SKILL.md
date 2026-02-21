---
name: sentiment-journal
description: Emotion-aware journaling and note-taking using QubicDB's built-in VADER sentiment analysis. Memories are automatically tagged with emotion labels and search results are boosted by sentiment match.
---

# Sentiment Journal

QubicDB has a **built-in VADER sentiment analyzer** that automatically labels every memory with an emotion (happiness, sadness, fear, anger, disgust, surprise, neutral) and a sentiment score. Search results are boosted when the query sentiment matches the memory sentiment.

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

## How It Works

```
Write: "I'm thrilled that the deployment went smoothly!"
  → QubicDB auto-labels: sentiment_label=happiness, sentiment_score=0.85

Write: "The production database crashed and we lost 2 hours of data"
  → QubicDB auto-labels: sentiment_label=anger, sentiment_score=-0.72

Search: "What went well today?"
  → QubicDB boosts positive-sentiment memories (happiness, surprise)

Search: "What problems did we encounter?"
  → QubicDB boosts negative-sentiment memories (anger, sadness, fear)
```

## Writing Journal Entries

```
# Positive entry — auto-labeled as happiness
qubicdb:write(index_id: "brain-daily-journal", content: "Amazing progress today! Finished the entire API layer and all tests pass. Team morale is high.", metadata: "{\"type\": \"journal\", \"date\": \"2025-02-21\"}")

# Negative entry — auto-labeled as frustration/anger
qubicdb:write(index_id: "brain-daily-journal", content: "Spent 4 hours debugging a race condition in the worker pool. Extremely frustrating. The mutex logic needs a complete rethink.", metadata: "{\"type\": \"journal\", \"date\": \"2025-02-21\"}")

# Neutral entry — auto-labeled as neutral
qubicdb:write(index_id: "brain-daily-journal", content: "Reviewed the architecture docs. The system has 6 main components: API, Worker Pool, Matrix Engine, Persistence, Daemons, and Registry.", metadata: "{\"type\": \"journal\", \"date\": \"2025-02-21\"}")
```

## Sentiment-Aware Search

```
# "What went well?" → naturally boosts positive memories
qubicdb:search(index_id: "brain-daily-journal", query: "great progress achievements success", depth: 2, limit: 10)

# "What frustrated me?" → naturally boosts negative memories
qubicdb:search(index_id: "brain-daily-journal", query: "frustrating problems bugs issues", depth: 2, limit: 10)

# "What did I learn?" → neutral/analytical
qubicdb:search(index_id: "brain-daily-journal", query: "learned insights understanding", depth: 2, limit: 10)
```

## Use Cases

- **Developer journal** — track daily wins, frustrations, and learnings
- **Team retrospectives** — aggregate positive/negative sentiment across sprint entries
- **Customer feedback** — categorize and search feedback by emotional tone
- **Meeting notes** — distinguish enthusiastic agreements from concerns
- **Therapy/coaching apps** — track emotional patterns over time

## Key Properties

- **Automatic** — no manual labeling needed. QubicDB analyzes sentiment on write
- **6 Ekman emotions** — happiness, sadness, fear, anger, disgust, surprise + neutral
- **Search boost** — sentiment match adds a [0.8, 1.2] multiplier to search scores
- **No extra config** — sentiment analysis is always enabled (zero external dependencies)
- **Compound scoring** — VADER compound score captures intensity, not just polarity
