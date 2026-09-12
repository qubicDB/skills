# Decide what memory work the task needs

QubicDB is useful when prior knowledge changes the answer or when a new result should survive the conversation. It is not a reason to interrupt a task that already has sufficient context. Decide the **purpose, knowledge scope, and granularity independently**.

## Read granularity

| User's actual need | Smallest sufficient evidence | Escalate when |
|---|---|---|
| Verify a known fact/decision | Read its known neuron ID; check its source and any known revision | A correction or conflict requires related evidence |
| Resume one task | Read its latest known handoff, then the referenced decisions/open items | The handoff is stale, incomplete, or conflicts with the current workspace |
| Solve a topical problem | Focused search within the project; select supporting records | Missing dependencies or another named service require another scope |
| Understand a subsystem | Several complementary cues for its decisions, constraints and dependencies | Evidence points to related subsystems; expand the selected set, not all memory by default |
| Compare named projects | Search that explicit index set; preserve per-index provenance | The user requests broader discovery |
| Discover where knowledge lives | Inspect mappings/index metadata; global search is useful within an authorized broad scope | Known inactive indexes need targeted loading/search |
| List/count every matching record, reconcile or export | Exact filters plus counted, stable enumeration to a file | API-visible inventory is incomplete or a transaction-consistent/full-storage backup is required |

“All information about this decision” normally means enough connected evidence to explain it. “Export every record” means completeness must be verified. Do not use top-K similarity results to claim exhaustive coverage, or dump a full archive into the model context to answer one question.

## Index boundary

An index is a durable knowledge domain with its own graph, activation history and lifecycle. Reuse the established mapping. Session IDs, branches, PRs, subtasks, new topics and revised decisions normally stay in that index with useful metadata.

Create another index when the knowledge has a distinct persistent owner, project, environment, purpose, or retention/access boundary **and** the requested work needs that separation. A new long-lived product can justify a new index; a second module in the same product usually does not. Respect an existing team convention even if its names differ from `brain-*`. Registration does not itself load data, and these namespaces do not implement tenant authorization.

A shared knowledge index is for deliberately reusable common knowledge, not an automatic copy of all project findings. Cross-index search lets the assistant synthesize evidence without merging storage or creating cross-index synapses. Store a derived cross-project conclusion only when useful and within the chosen destination's scope; label inference and cite its inputs.

## Neuron boundary

Choose the smallest **independently reusable meaning**, not a fixed token count or one neuron per sentence.

- Keep a decision and the qualification needed to interpret it together: “Retries reuse the payment key; a new key is allowed only for a new payment attempt.” Splitting away the exception makes recall misleading.
- Split facts that have different subjects, sources, validity periods, or likely future corrections. A retention rule and a UI colour preference do not belong in one neuron.
- For documents, preserve coherent sections with document/section/version provenance. Server-side embedding chunking averages vectors into **one** neuron; it does not make the sections independently retrievable. A huge mixed-topic neuron both dilutes retrieval and can exhaust a context budget. The default 64 KiB content limit is a ceiling, not a target.
- Reuse an unchanged fact and its ID. Exact-content deduplication is an implementation backstop, not a reason to write it again. Metadata-only changes on identical content are ignored.
- Write genuinely new events with their event/date in content. Write revisions with the changed fact, source/effective date, and prior ID in `supersedes`. Both old and new neurons remain; retrieval must resolve them.
- Save an approved/user-confirmed decision as such; save an observation with its evidence; mark an inference or tentative proposal explicitly. Retrieval rank, energy and repeated access do not confer truth or approval.
- A checkpoint summarizes task state and references reusable facts rather than copying every fact into each new session.

Use the team's existing metadata. Useful additions include `source`, `recorded_at`/`effective_at`, `type`, `task_id`, `thread_id`, `status`, and `supersedes`, all string values in MCP JSON-string metadata. Content must remain understandable without relying on hidden metadata. Avoid inventing a mandatory taxonomy for an established corpus.

## Stop when the evidence supports the task

Resolve the immediate question, identify any material gap, and return to the main work. Broaden a cue or scope because of a specific missing fact, not because a search always returns some result. Prefer distinct cues that answer separate uncertainties over repeated broad searches that reinforce the same noisy associations. Preserve “unknown” when evidence is absent or the backend cannot provide the requested completeness.
