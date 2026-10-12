## 12. Orchestration Layer

### 12.1 Purpose

The Orchestrator is the single control point for all component coordination. Every agent invocation, every Ledger write, every queue transition, every configuration read is mediated through it. Components do not communicate peer-to-peer; all flow converges at the Orchestrator.

### 12.2 Core Non-Negotiables (C-OR1 to C-OR6)

- Must satisfy the eight non-negotiable requirements from the Session 6 matrix (control flow, state, heterogeneous steps, 2PC, HIL, observability, concurrency, extensibility).
- The write path (Patch Authorization Gate → Commit Executor → MEMIT → Git) must be deterministic, non-reasoning code. LLM-based agents never hold simultaneous write access to both state mediums.
- Agent identity and runtime framework isolated behind a single invocation wrapper (IC-OR5). Swapping agent runtime must not require re-speccing graph structure or orchestration plumbing.
- Scope Lock Registry, State Ledger, and Audit category views are Orchestrator-owned. Agents never read or write them directly.
- Aggregate retry budget preserved across task decomposition (C-OR5).
- Commit Executor FIFO queue serialization is the exclusive chokepoint (C-OR6). Fan-out above; strict serialization at the queue.

### 12.3 Three Path Options (D72 — Deferred to Operator)

Three architecturally complete paths for operator selection:
- **Path A** — LangGraph alone.
- **Path B** — Claude Agent SDK alone.
- **Path C** — Hybrid (LangGraph + SDK).

No path is recommended in this spec. All three are comparable; selection is operational policy. Regardless of path, the 2PC Transaction Controller and the Merkle-chain State Ledger are custom components — no evaluated candidate ships them natively (D80).

Eliminated from consideration:
- **Pi** (D69): correctly categorized as an agent runtime, not an orchestrator. Fails non-negotiables 1, 5, 6, 7.
- **n8n** (D70): execution model (HTTP/function-call nodes) mismatched with multi-minute GPU-bound MEMIT compile as first-class step.
- **OpenClaw + Lobster** (D71): chat-gateway-first architecture wrong deployment shape for a pure dev harness. Viable but not advantaged vs. LangGraph.

### 12.4 Scope Lock and Hold Registry (IC-CW1, IC-OR4, extended T8)

Orchestrator-owned. Agents query via API; direct registry manipulation is integrity violation (OQ-CW2 resolved D78).

Unified typed registry: `write_lock` | `dependency_hold` entries. See §17 for full concurrency model.

### 12.5 Consistency Status API (D75, extended T10 IC-OR12)

Exposes real-time consistency status to agents via Orchestrator-mediated API only (OQ-TC3 resolved D75). Six states:
- `NORMAL`
- `COMPACTION_IN_PROGRESS`
- `CIRCUIT_TRIPPED` — systemwide write suspension. READ_ONLY mode is active: inference and query operations proceed; write token issuance is suspended. Enters this state automatically on TC circuit-breaker trip. Exits only via IC-TC-RESET signed ceremony (D84).
- `DIVERGED`
- `GENESIS_LOCKED`
- `RECONCILIATION_BACKLOG` *(added T10)*

Agents must check status before task acceptance.

### 12.6 Task Lineage Ledger (IC-OR9)

`TASK_DECOMPOSED` entries link subtask IDs to original task ID. Aggregate retry count tracked across subtasks. Enables reconstruction of escalation trees for post-hoc review.

### 12.7 Review Queue Management (T10)

Orchestrator maintains two named review queues with distinct semantics. See §15.

### 12.8 Idle-Window Detection (D79, closes OQ-OC1)

Orchestrator-internal. Heuristic: queue depth 0 + active locks 0 + no `PREPARED` 2PC for N minutes (default 30). Not exposed to agents. Used to schedule compaction and other background operations.

### 12.9 Path Classification (D76, extended T4)

Path classification stored at `.harness/path-classification.json` (Tier 3 Anchored Git Config). Git-committed, per-project. Harness ships default baseline. Classification drives 2PC compensation direction:
- `parametric_required` — default (safe failure).
- `parametric_none` — cannot be self-declared by agents (C-GOC3).
- `parametric_deferred` — delayed reconciliation via Pruning catch-up.

---

═══════════════════════════════════════════════════
# PART IV — CROSS-CUTTING CONCERNS
═══════════════════════════════════════════════════

