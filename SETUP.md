# QubicDB setup

Use an existing working endpoint when one is already configured. For a new local deployment with embeddings, select the **bundled** Docker Hub image:

```sh
docker compose -f docker-compose.qubicdb.bundled.yml up -d qubicdb
```

The optional UI can be started separately with the same Compose file. Review local port bindings, credentials and data-volume ownership before adopting an existing Compose file for another environment.

The maintained [setup reference](plugins/qubicdb-skills/skills/qubic-init/references/setup.md) contains Codex and Claude Code HTTP MCP configuration, index registration, and model verification. It is loaded by the setup skill only when needed; routine search/write skills do not repeat installation instructions.

## Image choices

| Compose file | Purpose |
|---|---|
| `docker-compose.qubicdb.bundled.yml` | Bundled MiniLM GGUF model plus embedding library; the local validation target |
| `docker-compose.qubicdb.vector.yml` | Vector-capable deployment with an externally supplied model; inspect its model mount |
| `docker-compose.qubicdb.yml` | Base deployment; do not infer working embeddings from basic health |

For changes to these skills, use [evals/compose.yml](evals/compose.yml), with a separate localhost port, project and volume. See [evals/README.md](evals/README.md). Do not point the evaluation suite at stage or an existing memory store.
