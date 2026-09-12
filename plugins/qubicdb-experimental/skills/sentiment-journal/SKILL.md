---
name: sentiment-journal
description: Store and retrieve QubicDB journal or feedback entries while distinguishing optional sentiment ranking from measured labels.
---

# QubicDB journal and feedback

Use the existing journal/project index and configured MCP tools when the user wants entries retained or recalled. Do not infer a request to store personal feelings from ordinary frustration in a conversation.

Write a useful self-contained entry with `qubicdb_write`. Its optional metadata is a JSON-encoded string of string values, such as type, event date, source, or user-provided category. Include the event/date in content when identical wording describes a new occurrence: duplicate content otherwise reuses the earlier neuron and leaves metadata unchanged.

Search with a cue reflecting the actual question. Use `qubicdb_search` plus `strict: true` and metadata when the result must belong to a specific date/category. A soft ranking boost is not a filter, and `qubicdb_context` has no metadata parameter. `recall` is energy-ordered, not chronological.

This release initializes VADER internally and can use query/memory sentiment to modify ranking. The ten MCP tools do not expose per-neuron sentiment labels or scores. Do not fabricate a numerical score, claim a label was returned, or describe sentiment ranking as an exact classifier. For a user-requested sentiment analysis, distinguish your analysis from measured server output and retain uncertainty, especially across languages.

Automatic sentiment is a secondary retrieval signal. It is not evidence that an entry is true, a diagnostic assessment, or a substitute for reading the original feedback.

Preserve event dates and distinguish repeated events from duplicate facts. Default energy decay is a ranking effect, not a TTL erasure policy; do not promise that old personal entries will disappear automatically.
