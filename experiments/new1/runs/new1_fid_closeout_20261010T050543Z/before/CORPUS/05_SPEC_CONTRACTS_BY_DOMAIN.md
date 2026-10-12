# 05 — SPEC CONTRACTS BY DOMAIN (the audit baseline)
_The spec's own requirements per council domain, with section anchors. Council audits EVIDENCE (00-02) against THESE clauses. Spec: `research_and_specs/llm-as-database-v1_2-integrated-spec.md`. Read the cited sections directly — this is a faithful index, not a substitute._

## 🔬 MEMIT Specialist — Write Engine (§8, §1)
- Facts enter weights via MEMIT; **all writes overlay-based, base model permanently FROZEN (D11, C8)**; `.vindex` tier stack (§8.4); `.larql` patches compiled to FFN deltas (§8.1).
- Incremental mode buffers patches via L1 cache before MEMIT compile (§8.3).
- **MEMIT sub-batch ceiling + edit capacity** = implementation-phase numeric (GAP-1/2; §8 / line 229). `attention_weight` engine-computed via covariance balancer (§8.5).
- Drift-from-anchor thresholds (§8.7). Forgetting/capacity are the Specialist's standing concern.

## 🗂️ Graph Data Architect — Schema/Query (§7)
- Entity taxonomy (§7.2); **5 relation families (D6)** (§7.3); triple model entity→relation→target; **`target` reserved, prohibited as entity (C3)**.
- `violates` relation is **ephemeral-only (D7)** — never written to `.vindex`; write engine hard-rejects patches containing it (C6, C9).
- Query surface: SELECT / INSERT INTO EDGES / DELETE FROM EDGES; deletion semantics; KNN graph-walk; polysemantic noise; Genesis scope.
- Undeclared relation labels = schema violations (C5), rejected by Validator BEFORE MEMIT (§ line 282).

## 🛡️ Warden — Security (§14 tokens/authz, §20 ceremony, layer table §6)
- **Patch Authorization Gate** + signed pass; **tokens + Write Scope Definitions per agent**; audit trail (§6 Security row; §14).
- Ceremony Authorization / CeremonyToken (§20); CAK bootstrap/burst/break-glass (§23); external-document provenance (§26).
- Least privilege; tamper detection; immutability boundary; blast radius. Suspicious of automated pipelines touching weights.

## ⚖️ State Consistency Theorist — Consistency (§ State Ledger, §8.4/8.7)
- **Two state mediums**: Git (syntactic) + `.vindex` (parametric) must agree.
- **2PC + Transaction Controller**; **State Ledger maps Git commit ↔ .vindex snapshot (Merkle-chain)** (§6 row, line 178, 357); circuit breaker → READ_ONLY on trip.
- Tiered `.vindex` for **independent rollback** (§8.4, line 335); ANCHOR events reset drift; Pruning Agent / semantic GC; COMPACTION_REGRESSION probe (prior facts survive recompile).
- Concern: state if power fails mid-write; authoritative-medium definition.

## ✅ Validation Contract Architect — Correctness (§ Reflexion/TGA, §21)
- **Reflexion loop** (Coder→Test→Fail→Fix→Retry); **TGA cascade**; **Validator + Meta-Validator with actor-critic INDEPENDENCE (D32-33)** — no self-testing.
- **L1 Storage probe (mandatory all writes): SELECT read-back confirms the edge was written**; **L2 behavioral/inference probe** for CORE/SUPPORTING (§21).
- `declared_importance` {CORE/SUPPORTING/INCIDENTAL} gates verification intensity. Deterministic sandbox; retry exit criteria; unrecoverable-failure escalation.

## 🔀 Orchestration Comparativist — Coordination (§12)
- Single **Orchestrator-mediated control plane** over six layers (§ line 100-107); review queues; **lock/hold registry**.
- **Path-conditional deployment: Path A (LangGraph) / B (SDK) / C (Hybrid)**, activates on operator selection (GAP-4/56/57/58).
- Must support: 2PC coordination, human-in-the-loop, audit-trail emission, concurrency model. No orchestrator pre-committed.

## CROSS-DOMAIN (the council's pre-mapped tensions live here)
The spec already notes cross-cutting tensions (e.g., Warden immutability vs State-Theorist mutable-during-2PC-window). The council's job: map where OUR EVIDENCE creates or resolves such tensions — e.g., the decoupled bridge (our-pipeline writes the `.vlp`) vs Warden's "who authorized this write + audit" and State-Theorist's "2PC/Ledger", which our file-level rollback does NOT yet satisfy.
