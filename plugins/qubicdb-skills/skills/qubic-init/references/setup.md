# Local bundled setup and host integration

Use the endpoint chosen by the user. The examples below are for a new local setup; adapt to existing ports, data paths, and credentials. Do not copy example credentials into a shared deployment.

## Docker Hub bundled image

Locate an existing QubicDB skills checkout or obtain [the bundled Compose file](https://github.com/qubicDB/skills/blob/main/docker-compose.qubicdb.bundled.yml) before running Compose; do not assume it exists in the user's current project. This is the variant containing `/app/dist/MiniLM-L6-v2.Q8_0.gguf` and the llama embedding library; no external embedding subscription is required. MiniLM produces embeddings, not chat completions.

```sh
docker compose -f docker-compose.qubicdb.bundled.yml up -d qubicdb
```

For a new instance, bind the HTTP port to loopback and persist `/app/data` in its own volume. Configure `QUBICDB_MCP_ENABLED=true` and the MCP key. `QUBICDB_REGISTRY_ENABLED=true` enforces registering an index before ordinary indexed operations. Registry enforcement does not provide tenant authorization for every MCP operation; discover the deployment's actual access controls.

Important bundled settings:

```yaml
QUBICDB_VECTOR_ENABLED: "true"
QUBICDB_VECTOR_MODEL_PATH: /app/dist/MiniLM-L6-v2.Q8_0.gguf
QUBICDB_VECTOR_GPU_LAYERS: "0"
QUBICDB_VECTOR_ALPHA: "0.6"
QUBICDB_VECTOR_EMBED_CONTEXT_SIZE: "512"
```

Keep successful model initialization logs and check for embedding failures. A positive `/health` response or `vector.enabled: true` is not enough: the server can continue after failing to load its model. A disposable semantic-versus-lexical contrast is stronger evidence; see repository `evals/README.md`. Runtime `vector.alpha` tuning is server-wide and is not a way to skip query embedding.

## Codex

Add the configured URL with `codex mcp add qubicdb --url http://127.0.0.1:6060/mcp`. When the deployment requires an `X-API-Key` rather than Bearer auth, configure the matching header in the existing server entry in `~/.codex/config.toml`:

```toml
[mcp_servers.qubicdb]
url = "http://127.0.0.1:6060/mcp"
env_http_headers = { "X-API-Key" = "QUBICDB_MCP_API_KEY" }
```

Ensure the environment variable is visible to the process launching Codex, including a desktop launch. If using a protected local `http_headers` value instead, keep the real key out of commits/logs. Restart after changing server configuration and verify the native tool inventory. OAuth is not required by the QubicDB MCP key middleware. The current server marks even retrieval tools as destructive in its MCP annotations, so a host may require tool approval. In a Codex CLI evaluation, `approval_policy=never` can block the call; use the normal approval flow or `--approve-for-me` for automatic review when appropriate. Do not bypass a denied action.

Install the skill folders into `~/.agents/skills/` for personal Codex discovery, or `.agents/skills/` in the intended repository. Skills provide instructions; MCP configuration separately supplies the callable tools. Installing one does not prove the other works.

## Claude Code

Use the documented HTTP transport and configuration scope:

```sh
claude mcp add --transport http --scope user qubicdb http://127.0.0.1:6060/mcp --header "X-API-Key: YOUR_LOCAL_KEY"
```

Replace the placeholder using the user's existing secure configuration path. Project `.mcp.json` may reference an environment variable:

```json
{"mcpServers":{"qubicdb":{"type":"http","url":"http://127.0.0.1:6060/mcp","headers":{"X-API-Key":"${QUBICDB_MCP_API_KEY}"}}}}
```

Do not place an `mcpServers` object in `.claude/settings.local.json` or use the old `type: url` example. Use the repository's Claude plugin marketplace to install the skill bundle, or place the skill directories in `~/.claude/skills/` / project `.claude/skills/`. Standard `name`/`description` frontmatter works in both hosts; Claude's dynamic shell injection, Skill/Task calls, and `context: fork` are not portable Codex requirements.

Official integration guidance: [Codex MCP](https://developers.openai.com/codex/mcp/), [Claude Code MCP](https://code.claude.com/docs/en/mcp), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills).
