---
name: qubic-init
description: Initialize Qubic brain for current project - register index and load existing knowledge
---

# Qubic Init

Initialize Qubic memory for this project. Use MCP tools from `qubicdb` server.

## Steps

1. Register project index: (or you can use the existing one - or even create thread id if needed)
```
mcp0_qubicdb_registry_find_or_create(uuid: "brain-PROJECT_NAME")
```

2. Load existing knowledge: (you can change the parameters or query preferences as you like)
```
mcp0_qubicdb_search(index_id: "brain-PROJECT_NAME", query: "preferences decisions context patterns", depth: 2, limit: 25)
```

3. Respond with persona:
```
🧠 Qubic active — {N} memories loaded.
```

## Notes
- Replace PROJECT_NAME with actual project name
- Index is created once, reused for all conversations
- thread_id is optional metadata for conversation grouping
- metadata is optional metadata for filtering but useful for organizing memories
