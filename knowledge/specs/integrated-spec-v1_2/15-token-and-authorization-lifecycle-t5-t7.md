## 14. Token and Authorization Lifecycle (T5, T7)

### 14.1 Unified Token Model

Two token types share the same admission-time-validation pattern:

**Invocation Token (T5):**
- Issued per agent invocation by Orchestrator.
- 10-minute TTL, single-use.
- Consumed at Authorization Gate on patch submission.

**Schema Migration Token (T7, revised D27):**
- Issued when human authorization gesture completes (Genesis or L1–L3 modification).
- 10-minute admission-time TTL.
- Consumed at 2PC Phase 1 admission. Compile proceeds independent of subsequent token state.

Both tokens carry hashes binding them to the full governance state at issuance time (Write Scope Definition version, Agent YAML version). Stealing a token is insufficient if any bound document changes within the TTL window.

### 14.2 Token Lifecycle Ledger Entries

Each token produces a paired issuance/outcome record in the Ledger. Every `*_ISSUED` resolves to exactly one of `CONSUMED`, `REJECTED`, or `EXPIRED_UNUSED`. Unresolved tokens past the reconciliation window are an integrity signal.

### 14.3 Failure Mode Interaction with Retry Budget

- **Token expiry before Gate consumption** — infrastructure failure class. Fresh token issued; retry budget not consumed.
- **Hash mismatch (mid-flight governance update)** — infrastructure failure class. Agent re-reads current state; retry budget not consumed.
- **Double-consumption** — security incident. Agent suspended; retry budget not consumed (task aborted, not retried).
- **Signature failure** — security incident. Agent suspended; retry budget not consumed.
- **Scope hash mismatch (`SCOPE_HASH_MISMATCH`)** — infrastructure failure class (D87). Gate returns structured payload including `current_scope_hash` and `scope_updated_at`. Orchestrator MUST re-issue token against current scope hash — NOT the stale hash. Retry budget not consumed. Distinguished from generic hash-mismatch by the `SCOPE_HASH_MISMATCH` error code. **Two consecutive `SCOPE_HASH_MISMATCH` errors for the same invocation (A4 — threshold lowered from 3 in v1.1 to 2 in v1.2)** → Orchestrator emits `SCOPE_MISMATCH_ESCALATED` (SECURITY, sync, W1) and routes the invocation to human review queue. The lowered threshold reflects the Warden's concern that three-attempt repetition provided a narrow oracle window.

**Aggregate `SCOPE_HASH_MISMATCH` detection (GAP-38 / GS12 — IC-AGG-COUNTER, IC-AGG-ALERT-LINK).**

Per-invocation escalation (above) catches narrow loops; a per-Orchestrator-instance aggregate counter catches low-signal-rate distributed attacks.

- **Aggregate threshold:** `scope_mismatch_aggregate_threshold_n` (default N=10) within a sliding window of `scope_mismatch_aggregate_window_seconds` (default M=60). Both parameters are Tier 1 config (`genesis-seal.json`).
- **Scope:** per-Orchestrator-instance global; counts across all invocations and all agents.
- **Alert path (IC-AGG-ALERT-LINK):** on threshold breach, emit `SCOPE_MISMATCH_AGGREGATE_ALERT` (SECURITY, async, W1) and cross-link to a newly-created review queue item. The cross-link carries the list of contributing invocation IDs and their source agents.
- **Counter behavior (IC-AGG-COUNTER):** counter increments on each `SCOPE_HASH_MISMATCH` regardless of per-invocation re-issue outcome. Counter is **not reset** by review-queue acknowledgment. Cooldown after alert: equal to the sliding window (M seconds); during cooldown the counter continues to accumulate but suppresses duplicate alerts.
- **Failure behavior:** alert is advisory at the aggregate level. It does not directly trip the circuit breaker — but if the Warden's operator-defined escalation policy maps `SCOPE_MISMATCH_AGGREGATE_ALERT` to circuit trip, the breaker's existing cross-category machinery (§11.8, A8) applies.

Both the per-invocation and aggregate thresholds are parameters the operator may tune. Both are Tier 1 — their modification is a Genesis Seal change.

### 14.4 Orchestrator-Signed as the Unifying Authority

Invocation tokens, schema migration tokens, and Ledger write authorization all route through the Orchestrator. The Orchestrator's signing key is the single cryptographic anchor that ties together agent identity, write authorization, and integrity-anchored record-keeping.

