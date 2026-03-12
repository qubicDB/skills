# QubicDB Setup Guide

QubicDB is a fully open-source, self-hosted semantic memory database. This guide covers Docker setup and IDE integration via MCP.

---

## Quick Start

### Option A: Non-vector Docker Compose

```bash
docker compose -f docker-compose.qubicdb.yml up -d
```

### Option B: Vector Docker Compose

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

### Option C: Docker Run (Non-vector)

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

### Verify

```bash
curl http://localhost:6060/health
```

For vector mode, use the same health check after starting `docker-compose.qubicdb.vector.yml`.

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

## Vector Setup

> ⚠️ The official `qubicdb/qubicdb:latest` image does **not** include vector support (no llama.cpp).

If you want helper instructions and patch scripts for local vector enablement, see `qubicdb/patches/` in the main repo:

- `patches/windows-local-vector/`
- `patches/linux-local-vector/`
- `patches/macos-local-vector/`
- `patches/vector-wrapper/`

Use `docker-compose.qubicdb.vector.yml` when you want semantic/vector search.

### Vector prerequisites

```text
your-folder/
├── qubicdb/
│   ├── Dockerfile.vector
│   └── dist/
│       └── MiniLM-L6-v2.Q8_0.gguf
└── skills/
    ├── docker-compose.qubicdb.yml
    └── docker-compose.qubicdb.vector.yml
```

### Download the GGUF model

Download a compatible All-MiniLM-L6-v2 GGUF model and save it as `../qubicdb/dist/MiniLM-L6-v2.Q8_0.gguf`.

**Bash:**

```bash
mkdir -p ../qubicdb/dist
curl -L "https://huggingface.co/second-state/All-MiniLM-L6-v2-Embedding-GGUF/resolve/main/all-MiniLM-L6-v2-Q8_0.gguf" \
  -o ../qubicdb/dist/MiniLM-L6-v2.Q8_0.gguf
```

**PowerShell:**

```powershell
New-Item -ItemType Directory -Force ..\qubicdb\dist | Out-Null
Invoke-WebRequest -Uri "https://huggingface.co/second-state/All-MiniLM-L6-v2-Embedding-GGUF/resolve/main/all-MiniLM-L6-v2-Q8_0.gguf" -OutFile "..\qubicdb\dist\MiniLM-L6-v2.Q8_0.gguf"
```

The filename matters because `docker-compose.qubicdb.vector.yml` expects `/app/dist/MiniLM-L6-v2.Q8_0.gguf` inside the container.

If the model file is missing, QubicDB may still start and report healthy HTTP status, but the vector layer will fail to initialize and semantic search will not work.

### Build manually

```bash
git clone https://github.com/qubicDB/qubicdb.git
cd qubicdb
docker build -f Dockerfile.vector -t qubicdb/qubicdb:vector .
```

### Start with vector compose

```bash
docker compose -f docker-compose.qubicdb.vector.yml up -d --build
```

### Docker Run (Vector)

```bash
docker run -d \
  --name qubicdb \
  --network qubicdb-net \
  -p 6060:6060 \
  -v qubicdb_data:/app/data \
  -v ./dist:/app/dist:ro \
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
  -e QUBICDB_VECTOR_ENABLED=true \
  -e QUBICDB_VECTOR_MODEL_PATH=/app/dist/MiniLM-L6-v2.Q8_0.gguf \
  -e QUBICDB_VECTOR_GPU_LAYERS=0 \
  -e QUBICDB_VECTOR_ALPHA=0.6 \
  -e QUBICDB_VECTOR_QUERY_REPEAT=2 \
  -e QUBICDB_VECTOR_EMBED_CONTEXT_SIZE=512 \
  qubicdb/qubicdb:vector
```

### Vector Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `QUBICDB_VECTOR_ENABLED` | `false` | Enable vector/semantic search |
| `QUBICDB_VECTOR_MODEL_PATH` | — | Path to GGUF embedding model |
| `QUBICDB_VECTOR_GPU_LAYERS` | `0` | Number of GPU layers (0 = CPU only) |
| `QUBICDB_VECTOR_ALPHA` | `0.6` | Hybrid search weight (0.0 = lexical, 1.0 = semantic) |
| `QUBICDB_VECTOR_QUERY_REPEAT` | `2` | Query repetition for embedding |
| `QUBICDB_VECTOR_EMBED_CONTEXT_SIZE` | `512` | Embedding context window size |

---

## Management Commands

```bash
# Start non-vector
docker compose -f docker-compose.qubicdb.yml up -d

# Stop non-vector
docker compose -f docker-compose.qubicdb.yml down

# Logs for non-vector
docker compose -f docker-compose.qubicdb.yml logs -f

# Restart non-vector
docker compose -f docker-compose.qubicdb.yml restart

# Remove non-vector stack (including data)
docker compose -f docker-compose.qubicdb.yml down -v

# Start vector
docker compose -f docker-compose.qubicdb.vector.yml up -d --build

# Stop vector
docker compose -f docker-compose.qubicdb.vector.yml down

# Logs for vector
docker compose -f docker-compose.qubicdb.vector.yml logs -f

# Restart vector
docker compose -f docker-compose.qubicdb.vector.yml restart

# Remove vector stack (including data)
docker compose -f docker-compose.qubicdb.vector.yml down -v
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
