---
name: qubic-write
description: Persist durable facts, decisions, corrections, and session handoffs in QubicDB while avoiding duplicate neurons and preserving provenance.
---

# Write QubicDB memory

Use the configured MCP connection and established project index. `qubicdb_write` below is the wire name; use the tool prefix actually exposed by the host. Create a new index only for a new persistent knowledge scope, not for every session, task, topic, or branch.

## Decide whether this needs a neuron

| Situation | Action |
|---|---|
| Existing unchanged fact | Reuse its ID; no write needed |
| New reusable decision, fact, preference, or resolved finding | Write one self-contained statement with source and relevant scope |
| Correction or changed decision | Write the new statement, explain what it replaces, and add `supersedes` with the prior ID |
| Repeated event with distinct time/meaning | Include the event/date in content so it is distinct from the earlier event |
| Task status or session handoff needed later | Store the current outcome, evidence references, open items, and next step |
| Temporary speculation, private reasoning, secrets, or routine chatter | Do not persist it as project knowledge |

When a related memory is already known, read it or search narrowly before storing a duplicate or contradictory claim. Do not perform a blanket global search before every write. Preserve uncertainty as uncertainty; an assistant inference is not a user-approved decision.

Preserve a decision together with the exception/rationale needed to interpret it. Split records with unrelated subjects, independent validity, or separate source versions. A document embedded in internal chunks is still one neuron, so write coherent independently retrievable sections rather than one mixed-topic transcript.

For relationship construction, REST parent placement and ingestion side effects, read [references/relationships.md](references/relationships.md). For evolving decisions, checkpoints and resumption, read [references/handoffs.md](references/handoffs.md).

## Actual write contract

`qubicdb_write` accepts `index_id`, `content`, and optional `metadata`. MCP metadata is a **JSON-encoded string with string values**, not an object. Use only useful fields; `type`, `source`, `version`, `recorded_at`, `thread_id`, and `supersedes` are conventions, not required server fields.

```json
{"index_id":"brain-cedar","content":"As of ADR-12, Cedar stores receipts in SQLite; this replaces ADR-11's PostgreSQL decision.","metadata":"{\"type\":\"decision\",\"source\":\"ADR-12\",\"supersedes\":\"PRIOR_NEURON_ID\"}"}
```

Use the actual prior ID, not the placeholder. Keep each neuron independently understandable; split a large handoff or document along useful factual/topic boundaries and preserve source/chunk identity. Repeated decisions need not be copied into every session summary.

Exact duplicate **content within an index** returns/fires the existing neuron. It does not apply new metadata, and it is not an upsert. Thus writing the same content with `status: done` will not change the previous status. A real status change needs distinct content and a reference to the old record; arbitrary paraphrasing to force duplication is not useful.

Direct neuron update/delete/fire and corresponding command mutations are disabled in the current release. Do not invent `qubicdb_update` or reset an index to remove one record. A correction preserves the old record; `supersedes` does not implement automatic exclusion or guaranteed erasure.

Metadata such as `thread_id` and `parent_thread` groups records only. It creates neither an access boundary nor a synapse. The engine forms/strengthens associations through its own activation and background mechanisms.

## Verify the saved result

Check tool errors and returned `id`/`_id`, content, and metadata. A duplicate may return an existing ID; report that accurately. Return the index and ID for a useful durable reference without narrating every memory action. Continue the user's primary task.
