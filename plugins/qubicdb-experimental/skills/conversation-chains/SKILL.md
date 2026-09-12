---
name: conversation-chains
description: Resume QubicDB-backed work across sessions using saved handoffs and explicit conversation references.
---

# Conversation handoffs

Use the configured QubicDB connection and existing project index. Save a useful handoff at a task boundary: outcome, source/commit references, unresolved items, and next step. Do not log every conversation turn or create a new index for each session.

On resumption, search for the known task/topic with `qubicdb_search`. If the previous `thread_id` is known and required, pass it as JSON-string metadata with `strict: true`; otherwise search the project so cross-session decisions remain visible. Read cited neuron IDs before relying on ambiguous or superseded statements.

Store handoff metadata as a JSON string of string values, such as `{"type":"handoff","thread_id":"conv-2","parent_thread":"conv-1"}`. Include the date/task/outcome in content when a new event is distinct. Exact duplicate content reuses the old neuron and does not update metadata.

`thread_id` and `parent_thread` are application conventions, not graph edges or automatic chain traversal. Follow a known parent by an explicit filtered search; do not claim the engine assembled the whole chain. Record uncertainty when a parent or prior session is missing.

`qubicdb_context` can supply compact project background, but cannot enforce a thread filter and does not return per-neuron IDs. Assemble selected search results yourself when the handoff must be limited to a task or cited. Preserve the current user's instructions over stored plans; memory supplements the active task and local planning files.
