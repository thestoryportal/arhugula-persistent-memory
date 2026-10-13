## 15. Review Pathways — Two-Queue Model (T10)

### 15.1 Two Distinct Review Types

**Correctness Review Queue** — populated by Reflexion escalation (D37 Step 3).
- Reviewer question: *"Is this agent output acceptable?"*
- Contains: task spec, retry history, decomposition log, failure tier, consistency status.
- Decisions: `approve_as_is` | `reject` | `re_route_for_further_work`.
- **Default on neglect:** task times out into logged suspension (D37 Step 4). Work is lost; no state changes.

**Reconciliation Review Queue** — populated by Pruning Agent catch-up patches with `requires_human_review` flag, by `external_source_audit` advisory entries (§26), and by cross-links from `SCOPE_MISMATCH_AGGREGATE_ALERT` (§14.3).
- Reviewer question: *"Should we update parametric memory to match out-of-band state change or external-document change?"*
- Contains: out-of-band Git commit hash and diff (for Pruning entries), external-document provenance staleness or unavailability signal (for provenance entries), contributing-invocation list (for aggregate-alert cross-links), proposed catch-up `.larql` patch where applicable, classification rationale, age, advisory-reason(s).
- Decisions: `approve_patch` | `reject_patch` | `modify_patch` | `defer_with_reason` | `acknowledge_advisory` (for advisory-only entries).
- **Default on neglect:** no silent default. Items accumulate; backlog signals escalate via Ledger and Consistency Status API.

**Merged queue policy (T-PM-vs-PA / GS11 — IC-REVIEW-QUEUE amended):** when multiple advisory reasons target the same `edge_id`, they merge into a single queue item rather than creating separate items. CORE-importance facts with STALE or UNAVAILABLE external-document provenance receive priority elevation in the merged item. Both advisory reasons MUST be acknowledged before the merged item can resolve. This replaces the v1.1 one-item-per-signal model.

### 15.2 Backlog Signals (Reconciliation Queue)

Tiered:
- ≤ 10 items, all < 7 days old: `NORMAL` state.
- > 10 items OR any > 7 days: `RECONCILIATION_BACKLOG_WARNING` Ledger entry; Consistency Status surfaces flag but state remains `NORMAL`.
- > 50 items OR any > 30 days: `RECONCILIATION_BACKLOG_CRITICAL` Ledger entry; Consistency Status state becomes `RECONCILIATION_BACKLOG`.
- `stale_urgent` edge count > 1,000 (D55): write suspension triggers independently.

### 15.3 Reviewer Authority

Reconciliation reviewers are a named subset in the Tier 2 sealed corpus `reconciliation-reviewers/`. Reviewer identity recorded in decisions and stamped into `.larql` patch metadata (`reconciliation_reviewer_id` field).

### 15.4 `modify_patch` Semantics

Reviewer-modified patches re-enter the standard pipeline as new submissions. Validator cascade (9.3) runs on the modified patch. Validator rejection returns the item to the queue with feedback attached. This preserves Validator independence when humans are in the authoring seat.

### 15.5 Dependency Hold Interaction

Catch-up patches respect Dependency Holds. Held edges excluded from patch delete operations. Conflicts (out-of-band change conflicts with held edge) flagged `dependency_conflict` — reviewer must explicitly resolve (wait for task resolution, or document explicit hold release).

