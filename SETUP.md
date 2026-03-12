# QubicDB Setup Guide

QubicDB is a fully open-source, self-hosted semantic memory database. This guide covers Docker setup and IDE integration via MCP.

---

## Quick Start

### Option A: Docker Compose (Recommended)

```bash
docker compose -f docker-compose.qubicdb.yml up -d
```

### Option B: Docker Run

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
  -e QUBICDB_MCP_ENABLED=true \
  -e QUBICDB_MCP_PATH=/mcp \
  -e QUBICDB_MCP_STATELESS=true \
  -e QUBICDB_MCP_API_KEY=qubicdb-mcp-secret-key \
  qubicdb/qubicdb:latest

docker run -d \
  --name qubicdb-ui \
  --network qubicdb-net \
  -p 8080:80 \
  qubicdb/qubicdb-ui:latest
```

### Verify

```bash
curl http://localhost:6060/health
```

---

## Admin UI

Visualize how the brain thinks and how neurons form connections.

- **URL:** http://localhost:8080
- **Username:** `admin`
- **Password:** `changeme`

> ⚠️ Change the password in production!

---

## IDE Integration

### MCP Configuration

Add to your IDE's MCP settings:

**Windsurf:**
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

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "qubicdb": {
      "url": "http://localhost:6060/mcp",
      "headers": {
        "X-API-Key": "qubicdb-mcp-secret-key"
      }
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
      "headers": {
        "X-API-Key": "qubicdb-mcp-secret-key"
      }
    }
  }
}
```

**Claude Code** (`.claude/settings.local.json`):
```json
{
  "mcpServers": {
    "qubicdb": {
      "type": "url",
      "url": "http://localhost:6060/mcp",
      "headers": {
        "X-API-Key": "qubicdb-mcp-secret-key"
      }
    }
  }
}
```

> **Note:** The `QUBICDB_MCP_API_KEY` environment variable must match the `X-API-Key` header in your IDE config.

---

## Vector Support (Optional)

> ⚠️ The official `qubicdb/qubicdb:latest` image does **not** include vector support (no llama.cpp).

To enable semantic/vector search, build from `Dockerfile.vector`:

```bash
git clone https://github.com/qubicDB/qubicdb.git
cd qubicdb
docker build -f Dockerfile.vector -t qubicdb/qubicdb:vector .
```

Then update your docker-compose or docker run command:
1. Change image to `qubicdb/qubicdb:vector`
2. Set `QUBICDB_VECTOR_ENABLED=true`
3. Add vector environment variables (see `docker-compose.qubicdb.yml` comments)

---

## Management Commands

```bash
# Start
docker compose -f docker-compose.qubicdb.yml up -d

# Stop
docker compose -f docker-compose.qubicdb.yml down

# View logs
docker compose -f docker-compose.qubicdb.yml logs -f

# Restart
docker compose -f docker-compose.qubicdb.yml restart

# Remove everything (including data)
docker compose -f docker-compose.qubicdb.yml down -v
```

---

## Troubleshooting

### Health check fails
```bash
docker logs qubicdb
```

### Port conflict
Change ports `6060` or `8080` in the compose file or docker run command.

### Vector model not found
Clone the main repo and bind mount the `dist` folder, or build from `Dockerfile.vector`.

---

## Links

| Resource | Link |
|----------|------|
| **Main Repo** | https://github.com/qubicDB/qubicdb |
| **Skills Repo** | https://github.com/qubicDB/skills |
| **Admin UI** | https://github.com/qubicDB/qubicdb-ui |
| **Docker Hub** | https://hub.docker.com/r/qubicdb/qubicdb |
| **API Docs** | https://qubicdb.github.io/docs/ |

---

## Notes

- ✅ Fully open source
- ✅ Self-hosted (runs on your machine)
- ✅ Customizable (fork and patch)
- ✅ MCP protocol compatible with all modern AI IDEs
