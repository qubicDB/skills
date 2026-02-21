---
description: Search Qubic memory with spreading activation - find related memories and context
---

# Qubic Search

Search Qubic for related memories. Use MCP tools from `qubicdb` server.

## Basic Search

```
mcp0_qubicdb_search(index_id: "brain-PROJECT_NAME", query: "SEARCH_QUERY", depth: 2, limit: 15)
```

## With Metadata Filter

```
mcp0_qubicdb_search(index_id: "brain-PROJECT_NAME", query: "SEARCH_QUERY", metadata: "{\"type\": \"decision\"}", strict: true)
```

## Persona Responses

| Result | Response |
|--------|----------|
| Found | `📍 Qubic remembered: ...` |
| Not found | `🤔 Qubic doesn't remember anything about this.` |

## Parameters

- **depth**: 1-8, spreading activation hops (default: 2)
- **limit**: max results (default: 20)
- **strict**: true = exact metadata match, false = soft boost +30%
