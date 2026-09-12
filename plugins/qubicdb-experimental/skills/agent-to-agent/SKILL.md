---
name: agent-to-agent
description: Share and retrieve QubicDB findings among agents already collaborating on the same authorized project.
---

# Shared agent findings

Use the existing shared project index and configured MCP connection. This skill stores/retrieves collaboration evidence; it does not itself authorize spawning agents or expanding their access.

Persist useful findings with `qubicdb_write(index_id, content, metadata)`. Metadata is a JSON-encoded string with string values. Useful fields include `agent_id`, `role`, `task_id`, `source`, and `type`. Separate source observations from agent interpretations in the content. Save outputs and evidence references, not private reasoning transcripts.

Readers use `qubicdb_search` with a focused cue. Add `strict: true` and the required role/task metadata when the result must come from a particular producer or task. A soft boost does not enforce that restriction. `qubicdb_context` has no metadata filtering; manually assemble filtered results for a scoped handoff.

Reuse unchanged facts. Exact duplicate content returns the existing neuron without replacing its metadata, so another agent writing the same content does not change authorship. A distinct finding, revision, or event should say what is new and reference the prior ID when relevant.

Metadata is provenance, not authentication, a lock, a queue, or a delivery guarantee. Read/search affect activation; similar writes do not guarantee graph edges. Retain `(index_id, _id)` references and resolve conflicting findings against sources and the current task.

Write/read/search activity within the same index can form associations through a five-second coactivation window, including between unrelated rapid imports. Use coherent records and relevant working sets; for full inventory/export, prefer exact enumeration that does not fire every neuron. Internal embedding chunks do not become separate retrievable records.
