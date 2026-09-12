# Native plugin packaging validation

Validated on 2026-09-12 with Codex CLI `0.154.0-alpha.6.2` and Claude Code `2.1.177`.
Core package: `qubicdb-skills` 1.3.0. Optional package: `qubicdb-experimental` 0.4.0.

## What was exercised

- Added this checkout as a marketplace in isolated Codex and Claude Code configuration directories.
- Installed both packages through each client's native plugin installer: all four installs succeeded.
- Codex app-server `skills/list` discovered all ten enabled, namespaced skills from the installed plugin cache, including `qubicdb-skills:qubic` and the six optional workflows.
- Claude Code `plugin details` reported four core skills and six optional skills, with no bundled MCP servers or hooks.
- Connected the isolated Codex configuration to the existing model-bundled local QubicDB server using a temporary protected credential. Native `mcpServerStatus/list` discovered ten tools; the temporary credential was removed afterward.
- Ran both Codex plugin-creator validators and both Claude Code plugin validators: all passed.
- Ran `python3 evals/test_packaging.py`: four tests passed for marketplace resolution, release identity, skill resources, and avoiding a duplicate MCP connection.

## Packaging decision

QubicDB is self-hosted: endpoints and API keys belong to the user's deployment. The previous plugin `.mcp.json` hardcoded localhost and a demo key with the obsolete `type: url` transport. It is removed. Both clients use their existing authenticated QubicDB connection, configured once using the bundled `qubic-init` setup reference. Plugin installation and removal therefore leave that connection alone.

The portable Agent Plugins HTTP format does not interpolate environment variables in URLs or headers. An environment-based Claude HTTP example is consequently not a portable `mcp.json`. These packages deliberately publish skills without that invalid companion configuration or a custom credential bridge.

The portable root manifests coexist with Codex compatibility manifests and Claude Code manifests. All share the same package identity and version. Core skill contents and the database runtime are unchanged by this packaging release; earlier capability and database evaluations remain documented in [the capability coverage map](capability-coverage.md).

## Reproduce

From the repository root:

```sh
python3 evals/test_packaging.py
claude plugin validate plugins/qubicdb-skills
claude plugin validate plugins/qubicdb-experimental
```

For installation, use a separate test profile or configuration directory, add the repository root with each client's `plugin marketplace add` command, and install both names from `qubicdb-agent-skills`. For Codex, use `plugin add`; for Claude Code, use `plugin install`. Inspect Codex app-server `skills/list` and Claude Code `plugin details` rather than treating installation exit status as evidence of loaded skills. Retain all files nested beneath each installed skill directory.

These checks verify native packaging, resource discovery and MCP coexistence. They are not a new model benchmark or a claim of curated-directory approval.

Primary format references: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference), [Agent Plugins MCP specification](https://agent-plugins.org/plugin-authors/mcp-servers).
