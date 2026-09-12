# Evaluate the QubicDB skills

## Disposable live contract suite

This suite creates synthetic indexes on a **dedicated localhost** QubicDB instance. It temporarily changes the server-wide vector alpha and restores it. Never use a server containing real memories or stage data. The test credentials below belong only to the loopback-bound evaluation Compose file.

From the repository root:

```sh
docker compose -p qubicdb-skill-contract -f evals/compose.yml up -d --wait
QUBICDB_EVAL_DISPOSABLE=1 \
QUBICDB_MCP_API_KEY=qubicdb-mcp-secret-key \
QUBICDB_EVAL_ADMIN=admin:changeme \
python3 -m unittest discover -s evals -p test_live.py -v
```

Python 3's standard library is sufficient. The client rejects remote hosts; the disposable opt-in is still needed because localhost alone does not prove a database is disposable. Port 16060 must be free. The bundled image is pinned to its tested Docker Hub digest. Record the new digest and rerun the suite before updating it.

The suite also checks real coactivation/cluster movement, REST parent placement and ignored tags, plus 520-record enumeration beyond recall limits without firing the exported records.

The suite checks the ten-tool schema, idempotent registration, content deduplication and metadata preservation, append-only corrections, strict versus soft filters, cross-index scope/provenance, context budget edge cases, depth defaults, deterministic REST filters, disabled neuron mutations, graph/lifecycle inspection, and **real embedding contribution**. The embedding test compares a nonlexical query at alpha 0 and alpha 0.6 on the same bundled instance; a config flag or a mocked vector is insufficient.

After collecting evidence, remove only this evaluation project's containers and volume:

```sh
docker compose -p qubicdb-skill-contract -f evals/compose.yml down -v
```

## Agent behavior

Use [cases.json](cases.json) as independent task cases. Give the agent the skill, selected synthetic indexes, raw seed records, and a working MCP connection; do not give it the rubric or expected solution. Use a fresh evaluation state for each variant. The optional `mcp_client.py` supplies a localhost MCP transport for evaluators without native tools; it is not a production SDK.

Record actual tool calls. `QUBICDB_EVAL_TRACE=/absolute/path/trace.jsonl` logs calls made through the helper without authentication headers. With native Codex, `codex exec --json` can capture execution events; Claude Code also supports structured noninteractive output. Evaluate saved database state and cited results, not phrases copied from the skill.

Run baseline and revised skills separately. Inspect call errors, number of writes, index scope, metadata types, filtering, preservation of the original memory, source links, and handling of unavailable capabilities. A positive explicit-invocation run does not establish automatic trigger quality or broad model reliability; test realistic implicit prompts separately before making those claims.

## Authoring checks

Validate every `SKILL.md` frontmatter, confirm relative references exist, and ensure conditional setup/operations material stays in references. The core and optional bundles use standard skill entrypoints and optional Codex UI metadata; they require no Claude-only runtime. A syntax pass is supplementary to the live and behavioral checks.

[Capability and decision coverage](capability-coverage.md) distinguishes live observations, source review, and operating guidance. It is not a model/provider benchmark.
