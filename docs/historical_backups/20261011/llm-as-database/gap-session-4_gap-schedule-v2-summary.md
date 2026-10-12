# LLM as Database: Agent Harness Architecture
## Gap Session 4.1 — Orchestration Comparativist
### Path-Conditional Delegation Token Shape + HIL Interface Mechanism

**Session:** Gap Session 4.1 (out-of-sequence advance session on GAP-4)
**Primary skill:** `orchestration-comparativist`
**Specialist provenance:** Orchestration Comparativist (primary); State Consistency Theorist (secondary); Warden / AISecOps (secondary)
**Status:** Ratified
**Basis:** Sessions 1–7; GS1–GS4; v1.1 integrated spec
**Input gap:** GAP-4 — Open, unaddressed GS1–4
**Output gap status:** GAP-4 — RESOLVED (conditional — activates on operator path selection superseding OQ-OR1)

---

## Session Context

GAP-4 identified two downstream items blocked by OQ-OR1 / D72 (operator path selection deferred):
- **(a)** Nested sub-agent delegation token design is path-dependent.
- **(b)** Human-in-the-loop interface mechanism is path-dependent.

This session produces three conditional spec blocks — one per path (A: LangGraph alone; B: Claude Agent SDK alone; C: Hybrid) — each fully speccing both items. OQ-OR1 remains the operator's decision. GAP-4 is closed from the spec side.

---

## Phase 1 — Cross-Domain Synthesis Pass

### 1.1 Open Question Cross-Read

**OQ-OR1 (S6):** Path selection deferred. Confirmed: this session produces conditional specs, not a recommendation.

**Council T5 (invocation-scoped token model):** No delegation bubbling in v1. Every invocation requires its own Orchestrator-issued token. Explicit Council deferral: "Delegation tokens (sub-agent invocations under IC-OR5 Path B/C models) — v2. For v1, every invocation that reaches the Gate carries its own Orchestrator-signed token; nested sub-agent calls don't bubble up token authority." This session closes the path-conditional v1 mechanism that makes this policy executable.

**GS4 CAK model (D93):** HIL review decisions are NOT governance ceremonies. Reviewer identity recorded in `HIL_DECISION_RECORDED` (GOVERNANCE, synchronous); no CeremonyToken required. Warden owns ceremony authorization; HIL inbound mechanism is Orchestrator-owned. No conflict.

**S6 IC-OR6:** Outbound HIL payload fully defined. Inbound return mechanism (IC-HIL-RETURN) was not specced per path. This session closes it.

### 1.2 New Persistent Artifact Governance

| Artifact | Type | Governance Tier |
|---|---|---|
| `HIL_PAUSED` | Ledger entry | Immutable (GOVERNANCE, sync) |
| `HIL_DECISION_RECORDED` | Ledger entry | Immutable (GOVERNANCE, sync) |
| `HIL_PAUSE_SERIALIZATION_FAILED` | Ledger entry (Path B) | Immutable (SECURITY, sync) |
| `HIL_INVOCATION_DISCARDED` | Ledger entry (Path C) | Immutable (GOVERNANCE, async) |
| `SUBAGENT_SPAWN_REQUEST` | Tool contract (internal) | Ephemeral session state; produces `TOKEN_ISSUED` |

No conflicts with S3 audit trail or S5 State Ledger Merkle-chain.

### 1.3 HIL Inbound Contract Completeness

All six HIL trigger classes (schema migration, scope lock change, scope failures, integrity violation, compaction failure, diverged state) now have both outbound (IC-OR6) and inbound (IC-HIL-RETURN per path) defined. HIL contract is complete per path.

---

## Decisions Made

**D-GS4.1-1.** Delegation token design under Path A is out of scope. Path A has no nested subagent spawning layer. V1 invocation-scoped single-use token (Council T5) applies unchanged.

**D-GS4.1-2.** Mediated issuance model adopted for Path B and C. Subagent tokens issued by coordinator on `SUBAGENT_SPAWN_REQUEST`. Parent cannot issue tokens. Parent scope cannot transfer.

**D-GS4.1-3.** V1 nesting depth cap: maximum one level of subagent nesting under Path B and C. Subagents MUST NOT spawn further subagents.

**D-GS4.1-4.** `parent_invocation_id` is audit-only in subagent tokens (Path B/C). Gate does NOT verify it.

**D-GS4.1-5.** HIL pause mechanism per path: Path A — LangGraph `interrupt_before`. Path B — Controlled serialize-and-halt; external scheduler resume. Path C — LangGraph interrupt at next node boundary; mandatory early-cancel for integrity-violation triggers pending T-GAP4-A ratification.

**D-GS4.1-6.** HIL inbound return: Path A/C — LangGraph state update API `{ thread_id, hil_decision }`. Path B — `coordinator.resume(session_id, hil_decision)`.

**D-GS4.1-7.** Decision routing on HIL resumption (path-independent): APPROVED -> workflow continues. REJECTED -> TC compensation; scope lock released. APPROVED_WITH_MODIFICATION -> Gate L1 (IC-OR14). ESCALATED -> hard escalation.

**D-GS4.1-8.** Scope lock 60-min TTL (C-CW3) runs during HIL pause all paths. Expiry -> `SCOPE_LOCK_EXPIRED_DURING_HIL` (GOVERNANCE, async). Re-acquisition protocol unspecced (GAP-4c).

**D-GS4.1-9.** Post-commit HIL abort (all paths, inherited D74): `HIL_ABORT_REJECTED_POST_COMMIT` (GOVERNANCE, sync) if trigger fires after COMMITTED.

**D-GS4.1-10.** Path C: `HIL_PENDING` flag is authoritative. Once set, `agent_invocation_node` wrapper MUST NOT pass any SDK result downstream. Discarded invocation does NOT consume retry budget.

**D-GS4.1-11.** GAP-4 resolved from the spec side. Conditional spec blocks produced for all three paths on both downstream items.

---

## Constraints Established

**C-GS4.1-1.** No authority bubbling (all paths). Subagent tokens issued against subagent's own WSD. Parent scope does not transfer.

**C-GS4.1-2.** Max one nesting level in v1 (Path B, C). Subagents MUST NOT spawn further subagents.

**C-GS4.1-3.** Coordinator is sole token issuer. Parent agents MUST NOT issue tokens.

**C-GS4.1-4.** IC-OR14 universal. APPROVED_WITH_MODIFICATION -> Gate L1. No path may route a modified patch directly to Commit Executor.

**C-GS4.1-5.** Path B: serialization MUST be complete before coordinator halts. Serialization failure -> `HIL_PAUSE_SERIALIZATION_FAILED` -> `CIRCUIT_TRIPPED`.

**C-GS4.1-6.** Path B: scheduler MUST NOT call `coordinator.resume()` more than once per `session_id`. Coordinator verifies absence of `HIL_DECISION_RECORDED` before processing; duplicates rejected.

**C-GS4.1-7.** Path C: subagent spawn not intercepted by `agent_invocation_node` wrapper = `INTEGRITY_VIOLATION`.

**C-GS4.1-8.** `HIL_DECISION_RECORDED` (GOVERNANCE, sync) MUST be written before workflow continues on any HIL resumption (all paths).

---

## Spec Blocks — Path-Conditional

---

### Delegation Token Shape — Path A (LangGraph Alone)
*Activates on operator selection of Path A (D72)*

**What it must do:** Pre-issue one invocation-scoped token per LangGraph agent node. V1 token structure (Council T5): `{ token_id, agent_id, invocation_id, task_id, scope_lock_ref, write_scope_hash, expected_yaml_hash, issued_at, expires_at, signature }`. No delegation layer. No `parent_invocation_id`.

**Hard constraints:** One token per node. (C-GS4.1-3). No `parent_invocation_id` field. GAP-4 item (a) is structurally inapplicable under Path A.

**Tradeoffs decided:** Flat token model over adding an unused `parent_invocation_id` field. Embedding an agent-hierarchy concept Path A lacks is rejected.

**Open questions (deferred):** OQ-GAP4-1 residual scope — v2 only.

**Interface contract:** Coordinator -> Gate: `TOKEN_ISSUED` at node entry. Gate: signature -> expiry -> not-consumed -> `write_scope_hash` -> `expected_yaml_hash` -> `scope_lock_ref` -> D22 cascade.

---

### Delegation Token Shape — Path B (Claude Agent SDK Alone)
*Activates on operator selection of Path B (D72)*

**What it must do:** Mediated issuance — coordinator intercepts `SUBAGENT_SPAWN_REQUEST` tool calls at SDK hook layer and issues Orchestrator-signed tokens for authorized spawns.

`SUBAGENT_SPAWN_REQUEST` tool contract:
- Request: `requested_agent_id` (must match registered agent YAML), `task_id` (inherited from parent), `parent_invocation_id` (parent's invocation_id; audit only), `scope_hint` (optional)
- Response: `token` (subagent_token), `spawn_authorized` (bool), `rejection_reason` (string, optional)

Subagent token structure (Path B/C): standard v1 token fields plus `parent_invocation_id: string` (audit field only; Gate does not verify).

**Hard constraints:** No bubbling — subagent `write_scope_hash` issued against subagent's own WSD. (C-GS4.1-1). Max one nesting level. (C-GS4.1-2). `parent_invocation_id` audit-only. (D-GS4.1-4). Coordinator sole issuer. (C-GS4.1-3). `TOKEN_ISSUED` Ledger entry written on each authorization. Spawn rejection: `spawn_authorized: false` if WSD conflicts with scope lock.

**Tradeoffs decided:** Mediated issuance over speculative pre-issuance. Speculative tokens waste TTL and generate abandoned-token noise. Cost: synchronous round-trip per spawn; acceptable for v1 single-machine.

**Open questions (deferred):** OQ-GAP4-1 (v2 nesting depth); OQ-GAP4-2 (scope_hint validation).

**Interface contract:** Parent agent -> Coordinator: `SUBAGENT_SPAWN_REQUEST` via SDK hook intercept. Coordinator -> Ledger: `TOKEN_ISSUED`. Gate: standard v1 verification; `parent_invocation_id` logged, not checked.

---

### Delegation Token Shape — Path C (Hybrid: LangGraph + SDK)
*Activates on operator selection of Path C (D72)*

**What it must do:** Mediated issuance, identical policy to Path B. Interception point is the `agent_invocation_node` wrapper (Session 6) at the LangGraph node boundary.

**Hard constraints:** All Path B constraints apply. Additionally: subagent spawn not intercepted by `agent_invocation_node` wrapper = `INTEGRITY_VIOLATION`. (C-GS4.1-7)

**Tradeoffs decided:** Path C mediated issuance is strictly cleaner than Path B. Node boundary is a more deterministic interception point. If delegation token correctness is a priority, Path C is preferred over Path B.

**Open questions (deferred):** OQ-GAP4-1, OQ-GAP4-2 (same as Path B).

**Interface contract:** SDK agent inside LangGraph node -> `agent_invocation_node` wrapper: `SUBAGENT_SPAWN_REQUEST` intercepted at wrapper boundary. All other contracts identical to Path B.

---

### HIL Interface Mechanism — Path A (LangGraph Alone)
*Activates on operator selection of Path A (D72)*

**What it must do:** LangGraph native `interrupt_before` / `interrupt_after` as HIL pause mechanism. Full graph state persists to Postgres checkpointer on suspension (SM-1 satisfied natively).

**Pause mechanism:** HIL gate node: (1) calls IC-OR6 outbound + `thread_id`; (2) writes `HIL_PAUSED` (GOVERNANCE, sync): `{ thread_id, task_id, trigger_class, pause_timestamp, scope_lock_ref }`; (3) `interrupt_before` fires.

**Inbound return (IC-HIL-RETURN — Path A):**
Delivered via LangGraph state update API: `{ thread_id, hil_decision: { decision, reviewer_id, modified_patch_ref?, rejection_reason?, escalation_target?, decision_timestamp } }`.
On receipt: coordinator writes `HIL_DECISION_RECORDED` (GOVERNANCE, sync) before workflow continues. (C-GS4.1-8)

**Hard constraints:** Scope lock TTL runs during pause. (D-GS4.1-8). Post-commit abort: `HIL_ABORT_REJECTED_POST_COMMIT`. (D-GS4.1-9). IC-OR14: APPROVED_WITH_MODIFICATION -> Gate L1. (C-GS4.1-4). Human review surface MUST deliver decisions via LangGraph state update API.

**Tradeoffs decided:** LangGraph native interrupt over custom suspend library. Coupling point (review surface calls LangGraph API) accepted; durable first-class thread suspension outweighs cost.

**Open questions (deferred):** OQ-OR3 (abort-authority actor) — operational policy, unchanged.

**Interface contract:**
```
IC-HIL-RETURN (Path A):
  From: Human review surface (operator-provided)
  To: Orchestrator via LangGraph state update API
  What it exposes: { thread_id, hil_decision }
  Conditions: thread_id references active SUSPENDED thread.
  Failure behavior: Invalid thread_id -> rejected.
    Missing required fields -> rejected.
```

---

### HIL Interface Mechanism — Path B (Claude Agent SDK Alone)
*Activates on operator selection of Path B (D72)*

**What it must do:** Controlled serialize-and-halt with external scheduler-driven resumption. No native graph-interrupt primitive.

**Pause mechanism:** (1) Current SDK invocation completes or TTL ceiling; result discarded if HIL trigger invalidates work. (2) Full state serialized to Postgres: `{ session_id, task_package, retry_history, scope_lock_registry_snapshot, pending_2PC_state, active_subagent_tokens, consistency_status_at_pause }`. (3) `HIL_PAUSED` (GOVERNANCE, sync). (4) IC-OR6 outbound + `session_id`. (5) Coordinator halts.

**Serialization failure:** MUST NOT halt if serialization fails. Write `HIL_PAUSE_SERIALIZATION_FAILED` (SECURITY, sync) -> `CIRCUIT_TRIPPED`. (C-GS4.1-5; GAP-4a covers full failure-mode spec)

**Inbound return (IC-HIL-RETURN — Path B):**
Via `coordinator.resume(session_id, hil_decision)`. Coordinator deserializes Postgres bundle; writes `HIL_DECISION_RECORDED` (GOVERNANCE, sync) before any further action. (C-GS4.1-8). Duplicate resume rejected. (C-GS4.1-6)

**Path B-specific failure modes:**

| Failure | Ledger entry | Response |
|---|---|---|
| Serialization failure | `HIL_PAUSE_SERIALIZATION_FAILED` (SECURITY, sync) | Circuit trip; task abandoned |
| Deserialization failure on resume | Coordinator failure log | Circuit trip; operator intervention |
| Scope lock expiry during review | `SCOPE_LOCK_EXPIRED_DURING_HIL` (GOVERNANCE, async) | Re-acquisition required (GAP-4c) |
| Scheduler outage | GOVERNANCE alert | Manual resume trigger |

**Hard constraints:** (C-GS4.1-4, C-GS4.1-5, C-GS4.1-6, C-GS4.1-8, D-GS4.1-8, D-GS4.1-9)

**Tradeoffs decided:** Controlled-halt-and-serialize over custom suspend library. Tradeoffs accepted: serialization failure is new circuit-trip surface; external scheduler dependency; resume latency bounded by poll interval. Operators for whom these tradeoffs are unacceptable SHOULD select Path A or C.

**Open questions (deferred):** OQ-GAP4-3 — scheduler poll interval; operational policy; suggested default 60 s.

**Interface contract:**
```
IC-HIL-RETURN (Path B):
  From: Human review surface -> job queue -> scheduler
  To: Orchestrator coordinator via coordinator.resume()
  What it exposes: { session_id, hil_decision }
  Conditions: session_id references SUSPENDED Postgres bundle.
    Coordinator verifies no existing HIL_DECISION_RECORDED.
  Failure behavior: Deserialization failure -> circuit trip.
    Duplicate -> rejected.
```

---

### HIL Interface Mechanism — Path C (Hybrid: LangGraph + SDK)
*Activates on operator selection of Path C (D72)*

**What it must do:** Path C inherits LangGraph native `interrupt_before` / `interrupt_after`. The `agent_invocation_node` wrapper creates a "next-boundary" latency window: HIL triggers that fire mid-SDK-invocation cannot immediately suspend the thread.

**Pause mechanism:** (1) Coordinator writes `HIL_PENDING: true` to thread state on trigger. (2) Current SDK invocation continues to exit or TTL ceiling. (3) `agent_invocation_node` wrapper detects `HIL_PENDING` at node exit; does NOT pass SDK result downstream; writes `HIL_INVOCATION_DISCARDED` (GOVERNANCE, async); discarded invocation does NOT consume retry budget. (D-GS4.1-10). (4) Routes to HIL gate node; `interrupt_before` suspends. (5) `HIL_PAUSED` (GOVERNANCE, sync).

**Early-cancel (pending T-GAP4-A ratification):** For `INTEGRITY_VIOLATION`-class triggers, coordinator MAY issue early cancellation to in-flight SDK invocation. Status: advisory until T-GAP4-A ratified.

**Inbound return and decision routing:** Identical to Path A — LangGraph state update API, `{ thread_id, hil_decision }`. Decision routing per D-GS4.1-7.

**Hard constraints:** `HIL_PENDING` authoritative; wrapper MUST NOT pass SDK result downstream once set. (D-GS4.1-10, C-GS4.1-8). Scope lock TTL runs. (D-GS4.1-8). Post-commit abort: `HIL_ABORT_REJECTED_POST_COMMIT`. (D-GS4.1-9). IC-OR14. (C-GS4.1-4).

**Tradeoffs decided:** Next-boundary latency over mid-invocation cancellation as default. Mid-invocation LLM cancellation produces undefined partial state; latency bounded by TTL ceiling is preferable.

**Open questions (deferred):** OQ-GAP4-4 — early-cancel hard requirement vs advisory for HIGH-priority triggers; pending T-GAP4-A ratification.

**Interface contract:**
```
IC-HIL-RETURN (Path C):
  From: Human review surface (operator-provided)
  To: Orchestrator via LangGraph state update API
  What it exposes: { thread_id, hil_decision } — identical to Path A.
  Conditions: HIL_PENDING true in thread state before suspension.
  Failure behavior: identical to Path A.
```

---

## IC-HIL-RETURN — Consolidated Cross-Path Contract

```
IC-HIL-RETURN — GS4.1
Extends: IC-OR6 (outbound, S6) — adds inbound mechanism per path

Outbound (IC-OR6, all paths):
  { task_id, pause_reason, patch_content_ref,
    validation_report_ref, scope_lock_ref, context_summary }
  Path A/C: + thread_id | Path B: + session_id

Inbound:
  Path A: LangGraph state update API — { thread_id, hil_decision }
  Path B: coordinator.resume()       — { session_id, hil_decision }
  Path C: LangGraph state update API — { thread_id, hil_decision }

hil_decision payload (all paths):
  decision: APPROVED|REJECTED|APPROVED_WITH_MODIFICATION|ESCALATED
  reviewer_id: string (required)
  modified_patch_ref: string?   — required if APPROVED_WITH_MODIFICATION
  rejection_reason: string?     — required if REJECTED
  escalation_target: string?    — required if ESCALATED
  decision_timestamp: ISO8601

Shared Ledger entries (all paths):
  HIL_PAUSED (GOVERNANCE, synchronous) — at pause
  HIL_DECISION_RECORDED (GOVERNANCE, synchronous) — on resumption

Path B only: HIL_PAUSE_SERIALIZATION_FAILED (SECURITY, synchronous)
Path C only: HIL_INVOCATION_DISCARDED (GOVERNANCE, asynchronous)

Invariant (C-GS4.1-4): APPROVED_WITH_MODIFICATION -> Gate L1 (IC-OR14).
Invariant (C-GS4.1-8): HIL_DECISION_RECORDED before workflow continues.
```

---

## Cross-Path Operator Commitment Comparison

| Commitment | Path A | Path B | Path C |
|---|---|---|---|
| Delegation token design | None — no nesting | Mediated issuance via SUBAGENT_SPAWN_REQUEST | Mediated issuance at agent_invocation_node wrapper |
| HIL pause mechanism | LangGraph interrupt_before | Serialize-and-halt | LangGraph interrupt at next boundary |
| HIL pause latency | ~0 | ~0 (scheduler poll on resume) | <= current SDK invocation TTL |
| HIL resume latency | ~0 | 1 scheduler poll interval | ~0 |
| Additional operational component | None | External scheduler | None |
| New HIL failure modes | None | Serialization failure -> circuit trip | Discarded SDK invocation |
| parent_invocation_id in token | Not used | Required (audit only) | Required (audit only) |
| Max nesting depth | N/A | 1 level | 1 level |
| T-GAP4-A exposure | None | None | Requires ratification |

---

## Open Questions

| ID | Description | Status | Blocks |
|---|---|---|---|
| OQ-OR1 | Path selection | Deferred — operator decision | Activation of conditional blocks |
| OQ-GAP4-1 | Max nesting depth v2 (Path B/C) | Deferred to v2 | Nothing in v1 |
| OQ-GAP4-2 | scope_hint validation policy | Deferred — low priority | Nothing in v1 |
| OQ-GAP4-3 | Path B scheduler poll interval | Operational policy; default 60 s | Nothing in v1 |
| OQ-GAP4-4 | Path C early-cancel requirement vs advisory | Pending T-GAP4-A ratification | Path C integrity-trigger behavior |

---

## New Gaps Surfaced

### GAP-4a — HIL_PAUSE_SERIALIZATION_FAILED Full Failure-Mode Spec (Path B)
**Domain(s):** Orchestration Comparativist (primary); State Consistency Theorist (secondary)
**Priority:** Medium | **Status:** Open — activates only if Path B selected
**Description:** Scope lock fate on serialization failure (auto-released or held?) and task fate (escalation Step 3 or Step 4?) are underspecced.
**Blocked by:** Nothing. **Blocks:** Clean Path B spec if selected.

### GAP-4b — SUBAGENT_SPAWN_REQUEST Tool Contract Full Spec (Path B and C)
**Domain(s):** Orchestration Comparativist (primary); Warden (secondary)
**Priority:** Medium | **Status:** Open — activates only if Path B or C selected
**Description:** Trust boundary placement for spawn-request interception (Gate vs coordinator only); whether `SUBAGENT_SPAWN_REJECTED` should be a Ledger entry type.
**Blocked by:** Nothing. **Blocks:** Clean Path B/C spec if selected.

### GAP-4c — Scope Lock Re-acquisition Protocol Mid-HIL-Review (All Paths)
**Domain(s):** State Consistency Theorist (primary); Orchestration Comparativist (secondary)
**Priority:** Medium | **Status:** Open — affects all three paths
**Description:** Re-acquisition protocol when scope lock expires during HIL pause is unspecced. Restart from beginning or from last durable checkpoint?
**Blocked by:** Nothing. **Blocks:** Clean HIL spec for long-duration reviews.
**Operator mitigation note (all paths):** Operators SHOULD define HIL reviewer SLA <= 55 minutes for tasks with active scope locks, OR provision GAP-4c re-acquisition protocol before deploying.

---

## New Tensions Surfaced

### T-GAP4-A — HIL Responsiveness vs. Path C Node-Boundary Constraint
**Domains:** Orchestration Comparativist x Validation Contract Architect (x Warden)
**Status:** UNRESOLVED — requires ratification if Path C selected
**Description:** Path C suspends at next node boundary, not immediately. For INTEGRITY_VIOLATION-class triggers (immediate response required), the in-flight SDK invocation continues during the latency window.
**Proposed resolution:** Two-tier HIL pause for Path C — mandatory early-cancel for INTEGRITY_VIOLATION-class triggers; standard next-boundary for all others.
**Session:** Fold into Path C activation session. Moot if Path A or B selected.

### T-GAP4-B — Scope Lock Duration vs. Human Review SLA
**Domains:** State Consistency Theorist x Orchestration Comparativist
**Status:** DEFERRED — operational policy
**Description:** 60-minute scope lock TTL (C-CW3) established independently of HIL reviewer SLA design. Extended reviews routinely exceed 60 minutes.
**Disposition:** Operator mitigation note added. Deferred to operational policy.

---

## Amendment Obligations

| Ref | Target | Amendment | Priority |
|---|---|---|---|
| A-GS4.1-1 | Appendix C | Add: HIL_PAUSED, HIL_DECISION_RECORDED, HIL_PAUSE_SERIALIZATION_FAILED, HIL_INVOCATION_DISCARDED | Outstanding — execute on path selection |
| A-GS4.1-2 | IC-OR6 (S6) | Append inbound return mechanism (IC-HIL-RETURN) per path | Outstanding |
| A-GS4.1-3 | S7 delegation token note | Update "deferred to v2" note with v1 mediated issuance clarification | Outstanding |
| A-GS4.1-4 | gap-backlog-v3.md GAP-4 | Status -> RESOLVED (conditional); add GAP-4a, GAP-4b, GAP-4c | Outstanding |

---

## Gap Session Summary Block

```
================================================================
GAP SESSION 4.1 — Orchestration Comparativist
Gaps targeted: GAP-4
Primary output: Path-conditional spec blocks (A / B / C) x
  two downstream items (delegation token shape + HIL mechanism)
Decisions: D-GS4.1-1 through D-GS4.1-11
Constraints: C-GS4.1-1 through C-GS4.1-8
================================================================

GAPS RESOLVED
----------------------------------------------------------------
GAP-4 — RESOLVED (conditional — activates on operator path
  selection superseding OQ-OR1)

  (a) Delegation token shape:
    Path A: V1 invocation-scoped token unchanged; no nesting;
            no parent_invocation_id field.
    Path B: Mediated issuance via SUBAGENT_SPAWN_REQUEST at SDK
            hook layer. Token + parent_invocation_id (audit
            only). Max 1 nesting level. No authority bubbling.
    Path C: Mediated issuance at agent_invocation_node wrapper.
            Identical token structure to Path B. Cleaner
            interception point.

  (b) HIL interface mechanism:
    Path A: LangGraph interrupt_before. thread_id handle.
            State update API inbound. No added failure modes.
    Path B: Serialize-and-halt. Postgres bundle. External
            scheduler resume. HIL_PAUSE_SERIALIZATION_FAILED
            -> CIRCUIT_TRIPPED. Most operationally complex.
    Path C: LangGraph interrupt at next boundary. thread_id.
            State update API inbound. Mandatory early-cancel
            for INTEGRITY_VIOLATION triggers pending T-GAP4-A.

  New Ledger entry types (all paths):
    HIL_PAUSED (GOVERNANCE, sync)
    HIL_DECISION_RECORDED (GOVERNANCE, sync)
  Path B only: HIL_PAUSE_SERIALIZATION_FAILED (SECURITY, sync)
  Path C only: HIL_INVOCATION_DISCARDED (GOVERNANCE, async)

  IC-HIL-RETURN: fully specced (inbound) per path.
  IC-OR6 (outbound) + IC-HIL-RETURN (inbound) = complete.

GAPS PARTIALLY RESOLVED
----------------------------------------------------------------
None. GAP-4 closed completely from the spec side.

GAPS DEFERRED
----------------------------------------------------------------
OQ-OR1 — Path selection — operator decision, unchanged.
OQ-GAP4-1 — Max nesting depth for v2 (Path B/C) — v2.
OQ-GAP4-2 — scope_hint validation policy — low priority.
OQ-GAP4-3 — Path B scheduler poll interval — operational policy.
OQ-GAP4-4 — Path C early-cancel requirement vs advisory —
  pending T-GAP4-A ratification.

NEW GAPS SURFACED
----------------------------------------------------------------
GAP-4a — HIL_PAUSE_SERIALIZATION_FAILED full failure-mode spec
  Domain: Orchestration + State Consistency | Priority: Medium
  Scope lock + task fate on Path B serialization failure.
  Activates only if Path B selected.

GAP-4b — SUBAGENT_SPAWN_REQUEST tool contract full spec
  Domain: Orchestration + Warden | Priority: Medium
  Trust boundary placement; SUBAGENT_SPAWN_REJECTED entry type.
  Activates only if Path B or C selected.

GAP-4c — Scope lock re-acquisition protocol mid-HIL-review
  Domain: State Consistency (primary) + Orchestration
  Priority: Medium | Affects all three paths.

NEW TENSIONS SURFACED
----------------------------------------------------------------
T-GAP4-A — HIL Responsiveness vs. Path C Node-Boundary Constraint
  Domains: Orchestration x Validation Contract Architect x Warden
  Status: UNRESOLVED — requires ratification if Path C selected
  Proposed: Two-tier HIL pause. Mandatory early-cancel for
  INTEGRITY_VIOLATION triggers; next-boundary for all others.
  Session: Fold into Path C activation session.

T-GAP4-B — Scope Lock Duration vs. Human Review SLA
  Domains: State Consistency x Orchestration
  Status: DEFERRED — operational policy
  Mitigation: operator SLA <= 55 min, OR provision GAP-4c first.
================================================================
```

---

*Gap Session 4.1 — Orchestration Comparativist*
*Primary skill: orchestration-comparativist*
*Specialist provenance: Orchestration Comparativist (primary); State Consistency Theorist, Warden (secondary)*
*Basis: Sessions 1-7; GS1-GS4; v1.1 integrated spec; gap-backlog-v3.md*
*Status: Ratified — conditional spec blocks produced; activation pending OQ-OR1 operator decision*
