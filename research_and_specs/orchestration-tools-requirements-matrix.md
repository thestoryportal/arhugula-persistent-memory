═══════════════════════════════════════════════════
SESSION 6 — Orchestration Comparativist
PRIMARY OUTPUTS: Requirements matrix · Four-candidate 
                 evaluation · OpenClaw+Lobster audit ·
                 Three-path decision spec · Orchestrator-
                 owned OQ resolution · Interface contract
                 with all five peer layers
═══════════════════════════════════════════════════

DECISIONS MADE
───────────────────────────────────────────────────
D68. Requirements matrix established across 8 dimensions
     (control flow, state, heterogeneous steps, 2PC, HIL,
     observability, concurrency, extensibility) with 
     sources traced to Sessions 1–5. Matrix is the 
     authoritative reference for any future orchestration
     decision.

D69. Pi eliminated as orchestrator candidate. Pi is 
     correctly categorized as an agent runtime, not an 
     orchestrator. Framework doc reference to "Pi 
     orchestrator" is a category error. Raw Pi fails
     non-negotiables 1, 5, 6, 7.

D70. n8n eliminated on structural grounds. Execution 
     model (HTTP/function-call nodes) is mismatched with 
     HS-3 (multi-minute GPU-bound MEMIT compile as 
     first-class step). Strong on HIL and observability
     but wrong execution shape for the write engine.

D71. OpenClaw+Lobster audited as fifth candidate. 
     Mature deterministic workflow primitives (loops, 
     retries, on_error, typed HITL), but chat-gateway-
     first architecture is wrong deployment shape for a 
     pure dev harness. Viable but not advantaged vs. 
     LangGraph.

D72. Three live orchestration paths specced:
     — Path A: LangGraph alone
     — Path B: Claude Agent SDK alone  
     — Path C: Hybrid (LangGraph + SDK)
     No single path recommended in this session. 
     Decision deferred to harness-operator; all three
     spec blocks are complete and comparable.

D73. OQ-V2 resolved: fresh retry budget per subtask 
     after decomposition, aggregate task cap (5 events) 
     preserved as ceiling across all subtasks.

D74. OQ-TPC2 resolved: human abort authority exists, 
     always unwinds via Transaction Controller 
     compensation path, never process-kill. Post-commit 
     abort is rejected.

D75. OQ-TC3 resolved: consistency status exposed to 
     agents via Orchestrator-mediated API only, never 
     direct ledger read. Five-state response: NORMAL, 
     COMPACTION_IN_PROGRESS, CIRCUIT_TRIPPED, DIVERGED, 
     GENESIS_LOCKED.

D76. OQ-GOC1 resolved: path classification stored as 
     per-project config at .harness/path-classification.
     json (Git-committed, Genesis-tier artifact). 
     Harness ships default baseline.

D77. OQ-CW1 deferred explicitly: voluntary lock 
     release / inter-agent negotiation is out of scope 
     for v1. V1 uses timeout-only release per S5 D60.

D78. OQ-CW2 resolved: Scope Lock Registry is 
     Orchestrator-owned. Agents query via API; direct 
     registry manipulation is integrity violation.

D79. OQ-OC1 resolved: idle-window detection is 
     orchestrator-internal. Heuristic: queue depth 0 + 
     active locks 0 + no PREPARED 2PC for N minutes 
     (default 30). Not exposed to agents.

D80. Regardless of path chosen, 2PC Transaction 
     Controller and Merkle-chain State Ledger are 
     custom components. No evaluated candidate ships 
     them natively.

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C-OR1. Orchestrator must satisfy all 8 non-negotiable
       requirements from the Session 6 matrix. 
       Candidates failing structural dimensions (Pi: 
       wrong abstraction level; n8n: execution model 
       mismatch) are disqualified regardless of other 
       strengths.

C-OR2. The write path (Patch Authorization Gate → 
       Commit Executor → MEMIT → Git) MUST be 
       deterministic, non-reasoning code. Under all 
       three paths, LLM-based agents never hold 
       simultaneous write access to both state mediums.
       This reinforces S4 D40 / C30.

C-OR3. Regardless of path, agent identity and runtime 
       framework is isolated behind a single invocation 
       wrapper. Swapping agent runtime must not require
       re-speccing graph structure (Path A) or 
       orchestration plumbing (Paths B, C).

C-OR4. Scope Lock Registry, State Ledger, and Audit 
       Trail are Orchestrator-owned. Agents never read 
       or write them directly. All access is 
       Orchestrator-mediated.

C-OR5. Aggregate retry budget is preserved across 
       task decomposition. Fresh per-subtask budgets 
       do not escape the original 5-event ceiling.

C-OR6. Commit Executor FIFO queue serialization is
       the exclusive chokepoint. Fan-out above the
       queue; strict serialization at the queue.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ-OR1  Path selection (A, B, or C) — explicitly
        deferred to harness-operator decision. All 
        three spec blocks are complete and 
        comparable; selection is operational policy.

OQ-OR2  Voluntary scope-lock release / inter-agent
        negotiation — v2 feature. V1 uses timeout-
        only release.

OQ-OR3  Abort-authority actor (ops on-call only, 
        or broader) — operational policy.

OQ-SL2  Multi-machine harness replication — 
        explicitly out of scope for v1 per user 
        confirmation. V1 is single-machine.

OQ-V2   CLOSED (see D73).
OQ-TPC2 CLOSED (see D74).
OQ-TC3  CLOSED (see D75).
OQ-GOC1 CLOSED (see D76).
OQ-CW1  DEFERRED TO V2 (see D77).
OQ-CW2  CLOSED (see D78).
OQ-OC1  CLOSED (see D79).

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC-OR1. Orchestrator → Validator (consumes S4 IC21):
        signed pass/fail signal verification step; 
        Orchestrator verifies Validator signature 
        before spawning Commit Executor.

IC-OR2. Orchestrator → Commit Executor (extends 
        S5 IC-TPC1): verified task-completion package
        + content classification + scope lock 
        reference + aggregate retry-budget state.

IC-OR3. Orchestrator → State Ledger:
        all ledger writes routed through Orchestrator
        (no agent direct writes). Orchestrator is the
        sole component with ledger write authority.

IC-OR4. Orchestrator → Scope Lock Registry:
        exclusive read/write. Agents query via API.

IC-OR5. Orchestrator → Agent Runtime Wrapper:
        agent_invoke(agent_name, input, 
        allowed_tools) → {output, token_cost, 
        tool_calls[]}. Under Path A: direct API call
        wrapped in LangGraph node. Under Path B: 
        SDK subagent spawn. Under Path C: SDK 
        subagent spawn inside LangGraph node.

IC-OR6. Orchestrator → Human Review Queue:
        pause workflow with full task package 
        (spec + retry history + decomposition log + 
        failure tier + consistency status). Resume 
        with reviewer decision + reviewer identity.
        Identity recorded in ledger entry.

IC-OR7. Orchestrator → Consistency Status API:
        GET /consistency-status returns one of: 
        NORMAL | COMPACTION_IN_PROGRESS | 
        CIRCUIT_TRIPPED | DIVERGED | GENESIS_LOCKED.
        Agents MUST check before task acceptance.

IC-OR8. Human → Orchestrator (abort authority):
        signed abort request carrying PREPARED 
        ledger entry ID + reason. Orchestrator sets 
        abort flag checkable at each 2PC phase 
        boundary. Post-commit abort rejected.

IC-OR9. Orchestrator → Task Lineage Ledger:
        TASK_DECOMPOSED entries link subtask IDs to 
        original task ID; aggregate retry count 
        tracked across subtasks.

═══════════════════════════════════════════════════
INPUT REQUIRED FOR NEXT SESSION
═══════════════════════════════════════════════════
Next session (Session 7) is the integrated spec 
assembly / Framework Council synthesis session. The 
harness now has full coverage across:
  — Session 1: Schema (Graph Data Architect)
  — Session 2: Write engine (MEMIT Specialist)
  — Session 3: Security / Warden (AISecOps)
  — Session 4: Validation (Validation Contract)
  — Session 5: Consistency (State Consistency)
  — Session 6: Orchestration (this session)

Session 7 should:
  1. Select Path A, B, or C (operator decision)
  2. Integrate all six session outputs into a single
     authoritative spec document
  3. Surface cross-session tensions for explicit 
     resolution (e.g., Warden's Write Scope 
     Definitions × State Consistency's path 
     classification × Orchestrator's Genesis config
     — three different security-sensitive 
     configuration files that should be reconciled)
  4. Run the Framework Council on the integrated 
     spec to catch any last cross-domain conflicts
  5. Produce the v1.0 specification artifact
═══════════════════════════════════════════════════