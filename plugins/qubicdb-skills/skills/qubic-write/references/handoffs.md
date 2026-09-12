# Long tasks, context loss and knowledge evolution

## Keep distinct kinds of state

- The active user request and local plan/workspace track what must be done now.
- Reusable QubicDB neurons hold decisions, constraints, observations and evidence that matter across tasks.
- A task handoff connects the two: objective, current scope/constraints, completed outcomes with verification, unresolved questions, next action, and references to the relevant neurons/files/branch/commit.

Do not use an old task plan as authority over new user instructions. QubicDB complements native compaction/memory; it does not guarantee that a host reads the right skill after compaction or make an obsolete instruction current.

## Checkpoint useful transitions

Write/update the local plan and append a QubicDB handoff when there is meaningful progress to preserve: a settled architectural decision, a completed investigation phase, a user correction that changes scope, or a session handoff. Avoid a memory write for every tool call, heartbeat or paraphrase. Preserve necessary qualifications and uncertainty; an unexecuted proposal is not completed work.

Use a stable `task_id` and a real timestamp/effective date in content/metadata. A new checkpoint has distinct content and may reference the prior handoff ID. Keep the latest ID in existing local task state so the next session can read it directly. `thread_id` is optional grouping, not a new index and not automatic thread traversal. Preserve the current user correction in the next checkpoint instead of keeping contradictory plans equally authoritative.

A handoff should be compact enough to be useful on its own, with IDs/paths for details. Do not duplicate the whole transcript or entire corpus. If several independent findings are valuable, retain them separately and reference them from the handoff. Server “consolidation” does not write a semantic summary for you.

## Resume after a new session or compaction

Resolve the same project/task scope. Read the known latest handoff ID, or narrowly search `type: handoff` and the required `task_id` with strict metadata. Read stored effective dates and revisions, not just the first/highest-energy result. The current command implementation does not reliably sort internal `createdAt` time objects; application ISO-date strings such as `recorded_at` can be sorted as strings, or inspect returned dates locally.

Recover the remaining work and only the referenced facts needed next. Recheck current workspace/config/source evidence where it may have changed. If another task advanced the branch, a user revoked a decision, or a dependency changed version, reconcile that state before continuing. A successful old test is evidence about its recorded version, not about the current code.

For a changed decision, retain the replacement with its source/effective date and `supersedes`. When answering “what is current,” resolve the chain and scope. A high-energy old record can outrank the replacement; `status` or `supersedes` does not automatically hide it. Report unresolved conflicts rather than silently choosing one. For a historical question, preserve the old version instead of rewriting history.

If the requested memory is absent, distinguish an empty search from a wrong index/filter, an unloaded persisted index, a budget-limited context result, or a connection/storage failure. Do not create a new brain immediately. Global search sees loaded workers only; explicit scoped access can load a known persisted brain. If known stored data unexpectedly becomes empty, inspect storage errors before declaring a new empty project.

## Durability and forgetting

A successful write acknowledges the in-memory operation. The worker does not append a disk WAL record for each write; storage snapshots/WAL are produced by persistence operations. Periodic persistence, graceful shutdown and fsync settings determine the actual durability window. For an explicitly required durable operational handoff, use the authorized persistence/backup workflow and verify it; a statistics export is not a backup. The current admin persist handler also ignores returned storage errors, so `persisted: true` alone does not establish durable success.

Natural decay affects activation/ranking. Normal neurons have base energy 0.1, above the 0.01 alive threshold, so default decay is not a TTL deletion policy. Weak synapses can be pruned. Consolidation moves eligible mature neurons to deeper layers (age/access/energy conditions on a sleeping brain); it does not merge duplicates, summarize content, or decide which factual revision is true.

A request to correct a record and a request to erase it are different. Individual neuron mutation is disabled in this release. Appending a correction leaves the original accessible; never report it as erased. Whole-index reset/delete is a separate, destructive operation, not a substitute for targeted forgetting.
