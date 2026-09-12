---
name: qubic-init
description: Set up or diagnose a QubicDB connection and resolve the persistent index for a project, including a local bundled embedding-model deployment.
---

# Connect QubicDB

Inspect the existing endpoint and project mapping first. Reuse a working deployment; installation is not a prerequisite for each read or write. Do not replace a configured stage/remote server with localhost silently.

For a requested local model-enabled installation, use Docker Hub **`qubicdb/qubicdb-bundled`**, which contains the GGUF embedding model and native library. The base `qubicdb/qubicdb` image does not include that model. Record the image digest used for testing.

Read [references/setup.md](references/setup.md) for Compose, Codex/Claude connection configuration, and model verification. Start only services needed for the task and use a distinct loopback port and data volume for experiments.

## Verify without polluting memory

1. Check health and MCP initialization/`tools/list` using the actual configured credentials. A registry write is not a health probe.
2. Discover the deployed schemas. The current server has ten `qubicdb_*` wire tools; an allowlist or older deployment can expose fewer. Do not assume the host's prefix or fixed server version tells you the available features.
3. Identify the correct existing project index from its configured ID or registry metadata. Recent activity is only a hint. If persistent memory for a new scope is requested, call `qubicdb_registry_find_or_create(uuid)` and use its returned `uuid` as `index_id`.
4. Load only context relevant to the current task. Registration alone does not make the index active; do not create a `test` brain during ordinary setup checks.

Keep the project-to-index mapping in existing project configuration or a concise local reference. Reuse it across conversations. Metadata can distinguish topics/sessions within that index. Dedicated indexes can represent genuinely different owners, environments, or retention policies; application authorization still controls who can query them.

Report the endpoint, selected index, observed tool availability, and whether the model actually loaded. If the model failed, call the connection lexical-only until verified otherwise; an enabled setting is not proof of successful initialization.
