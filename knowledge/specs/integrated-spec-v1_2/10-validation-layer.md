## 9. Validation Layer

### 9.1 Purpose

Every output that reaches the Commit Executor must be proven correct, not semantically vouched for. The Validation Layer ensures that code, tests, and `.larql` patches are *behaviorally verified* before any parametric state change occurs.

### 9.2 Actor-Critic Independence

Two hard independence rules:
- **The Coder Agent does not author its own tests** (D32, C23). The Test-Generation Agent (TGA) is a separate actor.
- **TGA reads the task specification only, never the Coder Agent's code before writing tests** (D33, C24). Independence is enforced by sequencing, not policy alone.

These rules extend to human reviewers: a reviewer who `modify_patch`es a catch-up or escalated patch cannot bypass the Validator — the modified patch re-enters the standard cascade (T10 IC-OR14).

### 9.3 Validator Four-Level Cost-Stratified Cascade (D34)

Per `.larql` patch verification:
- **L1 — Static analysis** — all patches, mandatory (syntax, schema conformance, vocabulary check, `larql_syntax_version` conformance per IC-GATE-8).
- **L2 — Inference probe** — edges with `declared_importance ∈ {CORE, SUPPORTING}`, mandatory (behavioral probe).
- **L3 — Cross-agent review** — conditional: `declared_importance = CORE` or Genesis-adjacent tier.
- **L4 — Human spot-check** — periodic audit, not a per-patch gate.

### 9.4 TGA Four-Layer Validation Cascade (T2)

The TGA itself is gated to prevent silent corruption of the correctness floor:

- **L1 — Structural check** (all outputs, mandatory). Static analysis: ≥2 assertions per test, no bare `pass` or `assert True` bodies, every assertion references spec-declared symbols, test count scales with spec complexity.
- **L2 — Stub probe** (all outputs, mandatory). TGA tests run against an empty stub implementation. Any substantive test that passes against stub is a false-positive gate; TGA is re-invoked.
- **L3 — Dual-TGA** (`declared_importance = CORE` tasks only). Two independent TGA invocations on the same spec; only behaviors asserted by both count as active gates.
- **L4 — Meta-TGA** (periodic, every 50 commits or weekly). Held-out `(spec, gold_test_set)` corpus per the Sealed Corpus pattern. TGA Health Score thresholds mirror Meta-Validator's: ≥95% no action, 85–94% warning and 48-hour review, <85% immediate suspension. Corpus authorship requirements and minimum viable corpus size (20 cases) are defined in IC-CORPUS-AUTH and §13.3 (D88). Health Score is `NOT_COMPUTED` when corpus is below 20 cases.

L1 + L2 failures do not consume Coder Agent retry budget — they are upstream infrastructure failures (consistent with D67).

### 9.5 Failure Classification and Retry Limits (D36)

Tiered retry limits:
- **Tier 1 — Syntactic / formatting:** max 2 retries.
- **Tier 2 — Logic / test failure:** max 3 retries.
- **Tier 3 — Architectural / schema violation:** max 1 retry, then immediate escalation.

**Hard cap: 5 retry events per task across all tiers** (C27). 2PC infrastructure failures do not consume this budget (D67).

Constitutional test suite failures are treated as Tier 3 regardless of the error's surface appearance (C25).

### 9.6 Failure Escalation Cascade (D37)

Four-step, in order:
1. **Task decomposition** — Orchestrator splits task into narrower subtasks, each with fresh retry budget (OQ-V2 resolved D73). Aggregate 5-event cap preserved across subtasks.
2. **Peer agent review** — second independent Coder receives full retry history and attempts task fresh. Tokenization of the peer review agent uses the standard Orchestrator ceremony; agent-to-agent trust model is deferred to v2 (GAP-20).
3. **Human escalation queue** — full package routed to the Correctness Review Queue with task spec, retry history, decomposition log, failure tier, consistency status.
4. **Logged suspension** — task suspended, named gap record written to the Ledger, `.vindex` not patched. Silent discard is prohibited at every step (C28).

### 9.7 `code_pass_patch_fail` — Hard Rejection (D35, C26)

The Validator may reject a `.larql` patch independently of code. `code_pass_patch_fail` is a named failure mode: neither output is committed when the patch fails, even if code is correct. Both must pass or neither is committed. This preserves the atomic transaction unit (C-TPC1).

### 9.8 Prompt Injection Defense — Two-Layer Sequential (D38)

- **Authorization Gate** owns *structural* inspection: field lengths, control characters, escape sequences, pattern-based. No NL parsing.
- **Validator** owns *semantic* content inspection: instruction-like language in free-text fields, override-pattern entity names.

Injection suspect events are never offered a retry (C29). Always hard rejection plus human review flag, regardless of injection confidence level.

### 9.9 Validator Has No Write Authority (D39)

Validator outputs are signed signals only, classified as orchestration communications. They pass through the Orchestrator's verification layer before the Commit Executor is spawned (IC21, IC22).

### 9.10 The Commit Executor Pattern (D40, C30)

Single-file, deterministic, non-reasoning agent. **Sole component with simultaneous write access to both Git and the MEMIT write engine.** No reasoning agent holds this access. The Commit Executor is the exclusive chokepoint for dual-medium writes (C-OR2, C-OR6).

### 9.11 Meta-Validator (D41)

Runs every 50 commits or weekly, whichever first. Evaluated against a held-out human-authored suite per the Sealed Corpus pattern. Corpus authorship requirements and minimum viable corpus size (20 cases) are defined in IC-CORPUS-AUTH and §13.3 (D88). Health Score is `NOT_COMPUTED` when corpus is below 20 cases. Validator Health Score thresholds:
- **≥ 95%:** no action.
- **85–94%:** warning flag, human review within 48 hours.
- **< 85%:** Validator suspended, immediate human review, recent passes audited.

