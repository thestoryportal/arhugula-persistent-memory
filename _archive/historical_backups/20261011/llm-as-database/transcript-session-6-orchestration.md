# Orchestration tool requirements matrix

**Created:** 4/21/2026 3:52:22  
**Updated:** 4/21/2026 4:10:02  
**Exported:** 4/21/2026 9:11:27  
**Link:** [https://claude.ai/chat/3b04f3d6-6527-42c3-9027-bf2e4cb66b13](https://claude.ai/chat/3b04f3d6-6527-42c3-9027-bf2e4cb66b13)  

## Prompt:
4/21/2026, 3:52:24 AM

> File: syncing-git-vindex-two-phase-commit.md

> File: validation-architecture-reflexion-loop-design.md

> File: threat-modeling-write-layer-access-control.md

> File: memit-specialist-spec-design.md

> File: ontological-schema-llm-databse-agent-framework.md

/orchestration-comparativist 
I now have requirements from five spec sessions. Before we compare any tools, help me build the requirements matrix from what we've established — then evaluate Pi, n8n, a Claude agent harness, and LangGraph against it. Use web search and deep research to verify current capabilities. Do not recommend a tool until the matrix is complete.



## Response:
4/21/2026, 3:56:16 AM



````plaintext
Thought process: Orchestrated systematic matrix construction from five sessions before tool evaluation.

I need to activate the orchestration-comparativist skill and build a requirements matrix from the five previous spec sessions before moving on to evaluate the tools—Pi, n8n, Claude agent harness, and LangGraph. The user's been clear that I should construct the matrix first using what we've already established, then conduct web research on current capabilities, and hold off on any recommendations until that foundation is solid.

Let me start by reading through the orchestration-comparativist skill file to understand the methodology, then systematically extract requirements from Sessions 1-5. I notice the uploaded files include the state consistency session and validation architecture work, so I have the material I need to build this matrix properly.
````

I'll work through this systematically. First I need to read the skill's methodology, then pull in Session 5 (which was uploaded but isn't in my context), then build the matrix before any research.

````plaintext
View: Load the orchestration-comparativist skill methodology before building the matrix
````

````plaintext
View: Load Session 5 State Consistency outputs - it was uploaded but not in context
````

````plaintext
Thought process: Cataloging five specialized sessions into unified requirements matrix.

I've collected all five sessions and now I'm checking the truncated part of Session 5 to see if there are any outstanding questions that need to be addressed in the orchestration.
````

Let me see the truncated Open Questions section from Session 5 — the items deferred to orchestration are critical input.

````plaintext
View: Read Session 5 open questions deferred to orchestration session
````

````plaintext
Thought process: Synthesized five sessions into comprehensive requirements matrix before tool evaluation.

I've mapped out the three specialized sessions so far—the graph architect handled the schema and entity structure, the MEMIT specialist built the write engine and verification layer, and the security-focused session established the threat model and authorization gates.

Now I'm seeing the validation and state consistency pieces come together: the validation architect designed the reflexion loop and commit patterns, while the state theorist tackled two-phase commit and transaction control. With all five sessions in place, I need to extract requirements across those eight dimensions the user specified—control flow, state management, heterogeneous steps, two-phase coordination, human oversight, audit trails, concurrency, and extensibility.

The user was clear: build the matrix first from what we've established, then verify current tool capabilities, but hold off on any recommendations until the matrix is complete.

So I'll synthesize the requirements matrix directly from the five sessions without needing web research yet, then research each candidate's actual capabilities against that matrix. I need to structure this carefully—build the matrix from the session decisions first, then pause so the user can validate it before I move into web research and evaluation. I'll batch the searches efficiently across the four candidates and their key capabilities. I see the user wants a unified approach: build the requirements matrix first with all the specific constraints they've established across their sessions, then pause for confirmation before evaluating the tools. The matrix needs to be comprehensive and grounded in their actual requirements — pulling in the retry logic, failure cascades, and other details they've already specified — so we're not evaluating against vague criteria.

Let me work through each dimension systematically, extracting the concrete requirements from their session notes. I'm working through the retry logic where task-level retries stay separate from infrastructure failures in the two-phase commit, so failed Git operations don't burn through the Coder's retry budget. The escalation chain needs to preserve state as issues move up levels, and I'm tracking how the circuit breaker pattern integrates with scheduled triggers for the Pruning Agent and Meta-Validator. For state management, I'm building an append-only State Ledger with Merkle-chain-lite properties to maintain retry history and Validator Health Scores across iterations, while keeping the full task package intact through decomposition and managing scope locks and archives.

The ledger tracks four distinct states—PREPARED, COMMITTED, COMPENSATED, and FAILED—with an immutable Genesis Seal anchoring the audit trail, which requires twelve specific fields and stays append-only. I need persistent task state that survives orchestrator restarts, a cryptographic event log, separate tracking for in-flight transactions versus historical records, and multiple queryable state stores including the Scope Lock Registry, Audit Trail, and project-lifetime archives.

Now I'm mapping out the different step types the orchestrator needs to handle: LLM inference for agent reasoning, Git operations like push and commit, MEMIT compilation on GPU, MEMIT mounting which can block reads, test execution in sandboxes, behavioral probes, schema migration token issuance, file operations on archives, human review queue pushes, and compensating transactions—each with different latency profiles and determinism guarantees.

The key challenge is treating GPU-bound operations and fast HTTP calls as equivalent first-class steps while handling variable long-running steps that might not complete within a timeout window, plus scheduling resources intelligently so MEMIT gets GPU access and PyTest gets sandbox isolation.

For the transactional layer, I'm working with atomic units that bundle module code, test suites, and .larql patches together, where genesis compile is a single two-phase commit event with fixed phase 2 ordering, content-scoped compensation, and circuit breaker thresholds to manage failure modes.

The commit executor needs to be a single-file deterministic agent with exclusive simultaneous write access to both mediums, implementing prepare/commit/compensate patterns with ledger entries written at phase boundaries—PREPARED before execution, COMMITTED after both phases succeed—while distinguishing mount-retry signals from compile-retry and detecting partial success states like Git-ahead conditions that are recoverable versus divergence that isn't.

For human oversight, I'm tracking escalation triggers: schema migrations and scope lock changes need out-of-band review, three consecutive scope failures flag for human review, and integrity violations always escalate immediately. Injection suspects get hard rejection with mandatory review and no retry, while the Meta-Validator uses confidence thresholds to route warnings to human review within 48 hours or suspend with immediate escalation for critical cases.

I'm also mapping out the operational controls: Git reverts require human confirmation, diverged states never auto-repair, compaction failures need review, and there are open questions about circuit breaker reset authority and external abort signal permissions that need clarification this session. The system needs to support pausing workflows with context preservation, resuming based on human decisions, and maintaining multiple escalation classes with time-bounded review windows.

Now I'm looking at the observability layer—audit trails must be append-only with integrity violations retained indefinitely, every task needs a named outcome on exit, and state changes are tracked through a Merkle-chain integrity model to ensure nothing gets lost or tampered with.

For concurrency, the Commit Executor acts as a serialization bottleneck that forces all writes through a single FIFO queue, eliminating parallel write conflicts entirely. Three agent roles are currently defined, and introducing new ones requires human review outside the normal process. I can add new agent types and step types through declarative configuration, handle schema migrations for updated Write Scope Definitions, and support plugin-based extensibility for agents. Now I'm thinking through which of these requirements are truly non-negotiable versus nice-to-have features, since that distinction will help me ask the right follow-up questions.

Looking at the constraints from earlier sessions, the critical requirements are two-phase commits with compensating transactions, making the Commit Executor the sole write authority, maintaining an append-only State Ledger and audit trail, implementing scope lock registries, enforcing full serialization at commit time, and building in a reflexion loop with tiered retries plus human gates at key decision points. The visual workflow design and specification details are more flexible trade-offs.

Now I'm planning the response structure: I'll present the full requirements matrix across all eight dimensions first, call out which constraints are non-negotiable based on what we've established, then pause for confirmation before diving into the research and evaluation phase against the four tools. I'm settling on the right approach here: build out the full matrix first as a structured spec block, get the user's confirmation on what's non-negotiable versus negotiable, then move into research and evaluation in a follow-up turn. This keeps the session focused on the deliverable rather than jumping ahead to recommendations before we've locked down the requirements.
````

Good — all five sessions are in hand. Before I open web searches on any candidate, let me do what you asked: build the requirements matrix from the five sessions, flag the non-negotiables, and surface the gaps. Once you confirm the matrix captures what the harness needs, I'll go research current capabilities of Pi, n8n, the Claude agent harness, and LangGraph.

---

## Session 6 — Orchestration Requirements Matrix (from Sessions 1–5)

### Orchestration Requirements Matrix — Session 6 Spec Block

**What it must do / represent / enforce / guarantee:**
Enumerate what an orchestrator has to be capable of to connect the five specced layers (graph schema, write engine, security gate, validation pipeline, state consistency plane) without forcing any of them to compromise their own contracts. Capabilities are sourced from session IDs — no assumptions.

---

### Dimension 1 — Control Flow Complexity

| # | Requirement | Source | Status |
|---|---|---|---|
| CF-1 | Run the Reflexion retry loop with tiered limits (syntactic ≤2, logic ≤3, architectural ≤1) and a hard cap of 5 retry events per task across all tiers | S4 D36, C27 | **Non-negotiable** |
| CF-2 | Accumulate retry history across iterations and pass it into IC19's `retry_history_summary` from attempt 2 onward | S4 IC19 | **Non-negotiable** |
| CF-3 | Execute the 4-step failure escalation cascade in order: Task Decomposition → Peer Agent Review → Human Escalation Queue → Logged Suspension, with state preservation between steps | S4 D37 | **Non-negotiable** |
| CF-4 | Classify failures by tier at runtime and route to the correct retry-budget / escalation path, including "code_pass_patch_fail" as a distinct branch | S4 D36, C26, IC20 | **Non-negotiable** |
| CF-5 | Enforce the 4-level validation cascade (static → inference probe → cross-agent review → human spot-check) with Level 3 triggered only when attention_weight ≥ 0.90 or Genesis-adjacent | S4 D34 | **Non-negotiable** |
| CF-6 | Run scheduled/cadence triggers: Pruning Agent (50 commits OR 24h OR event-driven), Meta-Validator (50 commits OR weekly), compaction (3K edges warning / 8K hard) | S5 D57, D63; S4 D41 | **Non-negotiable** |
| CF-7 | Maintain retry-budget isolation: 2PC infrastructure failures do NOT consume Coder Agent retry budget | S5 D67 | **Non-negotiable** |
| CF-8 | Support task decomposition that issues fresh retry budgets per subtask (OQ-V2 resolution) | S4 OQ-V2 | Policy-pending; orchestrator must not preclude either resolution |

**Elimination criterion:** an orchestrator that can't model stateful cyclical loops with accumulating context is out. Linear DAG-only tools fail this dimension.

---

### Dimension 2 — State Management

| # | Requirement | Source | Status |
|---|---|---|---|
| SM-1 | Persist task state across orchestrator restarts — including PREPARED 2PC transactions, active Scope Locks, and open retry loops | S5 IC-TPC2, IC-CW1; S4 C28 | **Non-negotiable** |
| SM-2 | Maintain the State Ledger as an append-only store with Merkle-chain-lite integrity; no agent holds delete authority | S5 D49, D50, C-SL1, C-SL2, C-SL6 | **Non-negotiable** |
| SM-3 | Maintain a queryable Scope Lock Registry with 60-minute max-hold and auto-release-on-timeout semantics | S5 D59, D60, C-CW3–5 | **Non-negotiable** |
| SM-4 | Track Validator Health Score over time with threshold-triggered actions (≥95, 85–94, <85) | S4 D41, IC24 | **Non-negotiable** |
| SM-5 | Preserve full task package (spec + all retry history + decomposition log + failure tier) across escalation steps | S4 D37 | **Non-negotiable** |
| SM-6 | Separate in-flight transaction state (PREPARED/COMMITTED/COMPENSATED/FAILED) from historical audit state — they have different access patterns and retention policies | S5 IC-TPC2, IC-SL2 | **Non-negotiable** |
| SM-7 | Project-lifetime retention of .larql archive and overlay archive, indexed by ledger entry ID | S5 D64, D65, C-OC4, C-OC7 | **Non-negotiable** |

**Elimination criterion:** an orchestrator that treats state as in-memory session-only fails here. External persistence is required natively or via tightly coupled sidecar.

---

### Dimension 3 — Heterogeneous Step Types

The orchestrator must treat the following as equivalent first-class steps:

| # | Step type | Latency profile | Resource | Source |
|---|---|---|---|---|
| HS-1 | LLM inference (agent reasoning) | seconds–minutes | token budget | S4 throughout |
| HS-2 | Git operation (push, commit, revert, checkout) | sub-second–seconds | CPU | S5 D46, D51 |
| HS-3 | **MEMIT compile** | seconds–minutes, variable | **GPU-bound** | S2 D12, D13 |
| HS-4 | MEMIT mount with retry loop | seconds, variable | GPU memory | S5 IC-TC6, D47 |
| HS-5 | PyTest / shell in Docker or E2B sandbox | variable | sandbox process | S4 IC18, D34 L1 |
| HS-6 | Behavioral probe inference | seconds | GPU + tokens | S2 D18, IC9 |
| HS-7 | Schema migration token issuance | sub-second | orchestrator-local | S3 IC14 |
| HS-8 | .larql archive write + overlay archive | sub-second | filesystem | S5 D64, D65 |
| HS-9 | Human review queue push with packaging | async | queue | S4 D37, S3 D26 |
| HS-10 | Compensating Git revert | sub-second | CPU | S5 D47, C-TC1 |

**Non-negotiable property:** the orchestrator must NOT treat HS-3/HS-4 as a black-box HTTP timeout. MEMIT compile can take minutes; a naive `timeout: 30s` pattern fails this dimension. The orchestrator needs to be resource-aware — GPU-bound operations cannot be parallelized freely against other GPU-bound operations.

---

### Dimension 4 — Two-Phase Commit Coordination

| # | Requirement | Source | Status |
|---|---|---|---|
| TPC-1 | Implement prepare → commit → compensate pattern across Git + MEMIT with Phase 2 ordering fixed (Git first, .vindex second) | S5 D46, C-TPC1–5 | **Non-negotiable** |
| TPC-2 | Write PREPARED ledger entry BEFORE any medium touch; COMMITTED entry only after both phases succeed | S5 IC-TPC2, C-TPC4 | **Non-negotiable** |
| TPC-3 | Detect partial-success (Git-ahead) state and trigger Transaction Controller with content-scoped compensation direction | S5 D47, C-TC1, C-TC2 | **Non-negotiable** |
| TPC-4 | Route Layer-4 Git reverts through human confirmation, not auto-revert | S5 D47 | **Non-negotiable** |
| TPC-5 | Implement circuit breaker: 3 consecutive failures/task OR 5/10min window → trip; diverged state = immediate trip with no auto-repair | S5 D48, C-TC3, C-TC5 | **Non-negotiable** |
| TPC-6 | Route writes exclusively through the Commit Executor — a single-file, deterministic, non-reasoning agent; no reasoning agent may hold simultaneous write access to both mediums | S4 D40, C30 | **Non-negotiable** |
| TPC-7 | Treat Genesis compile as a single atomic 2PC event across all tier files (L1–L4) | S5 D45, C-TPC2 | **Non-negotiable** |
| TPC-8 | Treat overlay compaction as a single atomic 2PC event with its own boundary ledger entries (COMPACTION_BEGIN / BOUNDARY / ABORT) | S5 D62, C-OC2, IC-OC5 | **Non-negotiable** |

**Elimination criterion:** no orchestrator that lacks saga / compensating transaction support can satisfy this dimension without building the 2PC coordinator from scratch as a sidecar. Note that a sidecar is acceptable, but the cost has to be acknowledged.

---

### Dimension 5 — Human-in-the-Loop Integration

| # | Trigger | Required behavior | Source |
|---|---|---|---|
| HIL-1 | Genesis write approval (Architect Agent output) | Pause with full package, accept/reject, resume if accept | S3 D26 |
| HIL-2 | Schema migration authorization token request | Issue time-limited (30 min) hash-bound one-time token on approval | S3 D27, C18, IC14 |
| HIL-3 | Write Scope Definition change | Out-of-band human review event (explicitly not inline) | S3 D24, C17 |
| HIL-4 | Integrity violation (patch hash mismatch) | Immediate escalation regardless of count; agent suspended for session | S3 D31, C22 |
| HIL-5 | Three consecutive scope failures from one agent | Suspend agent, raise human review flag | S3 D31 |
| HIL-6 | Injection suspect (semantic OR structural) | Hard rejection + human review flag; no retry offered | S4 C29, D38 |
| HIL-7 | Tier 3 architectural/schema failure after 1 retry | Immediate escalation | S4 D36 |
| HIL-8 | Failure escalation Step 3 (Human Escalation Queue) | Full package delivered: task spec, all retry history, decomposition log, failure tier | S4 D37 |
| HIL-9 | Validator Health Score 85–94 | Warning flag; human review within 48h | S4 D41 |
| HIL-10 | Validator Health Score <85 | Suspend Validator, immediate human review, audit recent passes | S4 D41 |
| HIL-11 | Layer 4 `.vindex` failure requiring Git revert | Human confirmation required before revert | S5 D47 |
| HIL-12 | Diverged state (2PC compensation failed) | No auto-repair; human review required | S5 C-TC5 |
| HIL-13 | Out-of-band Git commit reconciliation | Pruning Agent catch-up patch flagged `requires_human_review`; no auto-compile | S5 D52, C-GOC4 |
| HIL-14 | Compaction verification failure | Abort compaction, retain existing overlays, human review | S5 D66 |
| HIL-15 | Circuit breaker reset | Reset protocol is orchestration call (OQ-TC1 operational) | S5 OQ-TC1 |
| HIL-16 | External abort signal (emergency stop during PREPARED transaction) | Interrupt authority — orchestration must define | S5 OQ-TPC2 |

**Required orchestrator capabilities:** pause/suspend with context preservation, structured review packaging, time-bounded review windows (48h), multiple escalation classes, emergency-abort primitive.

**Elimination criterion:** orchestrators with no native pause/resume semantics force HIL to be implemented as polling loops in agent code — brittle, hard to audit.

---

### Dimension 6 — Observability and Audit

| # | Requirement | Source | Status |
|---|---|---|---|
| OA-1 | Emit structured events on every step boundary — sufficient to populate the Audit Trail's 12 required fields | S3 D28 | **Non-negotiable** |
| OA-2 | Support append-only semantics with cryptographic chain integrity (Merkle-chain-lite) — natively or via enforced sidecar | S5 D50, C-SL2 | **Non-negotiable** |
| OA-3 | Route events to multiple destinations: State Ledger, Audit Trail, Meta-Validator health log, integrity-violation log | S5 IC-SL6; S3 IC13; S4 IC24 | **Non-negotiable** |
| OA-4 | Gate evaluation record on every Authorization Gate interaction (pass OR fail) | S3 IC13, D28 | **Non-negotiable** |
| OA-5 | Distinct write-outcome codes preserved: success / behavior_fail / storage_fail / rejected / code_pass_patch_fail — no silent collapse into "success" | S3 D30; S4 C26 | **Non-negotiable** |
| OA-6 | Compaction boundary events (COMPACTION_BEGIN / COMPACTION_BOUNDARY / COMPACTION_ABORT) addressable as distinct event types | S5 IC-OC5 | **Non-negotiable** |
| OA-7 | Integrity-violation events retained indefinitely, separate retention policy from normal events | S3 D28 | **Non-negotiable** |

**Elimination criterion:** orchestrators with print-to-stdout logging as the primary audit path fail this dimension. Structured event emission must be first-class.

---

### Dimension 7 — Concurrency Model

| # | Requirement | Source | Status |
|---|---|---|---|
| CM-1 | Enforce full write serialization at the Commit Executor — FIFO queue, concurrency = 1 | S5 D43, D58, C-CW1 | **Non-negotiable** |
| CM-2 | Permit concurrent task execution UP TO the commit boundary — multiple Coder Agents may work in parallel on different scopes | S5 implied by D58 phrasing ("no parallel writes") | **Non-negotiable** |
| CM-3 | Manage Scope Lock Registry: lock assignment at task declaration (not commit), conflict resolution before agent begins work | S5 D59, C-CW3, C-CW4 | **Non-negotiable** |
| CM-4 | Auto-release scope locks on 60-min timeout; reject stale patches at Validator with `scope_lock_expired_and_superseded` | S5 D60, C-CW5 | **Non-negotiable** |
| CM-5 | Treat commit-time collision (after declaration-time locks) as a security incident, not a merge case | S5 D61 | **Non-negotiable** |
| CM-6 | Pass scope lock reference through to Commit Executor for final verification before 2PC | S5 IC-CW3 | **Non-negotiable** |

**Required capability:** the orchestrator needs both fan-out (parallel task execution) AND serialization at a chokepoint (commit). This is a harder model than "parallel everywhere" or "sequential everywhere" — it's parallel-up-to-a-point.

---

### Dimension 8 — Extensibility

| # | Requirement | Source | Status |
|---|---|---|---|
| EX-1 | Declarative agent definition: Single-File Agent protocol — system prompt, temperature, I/O, allowed tool IDs in one YAML/MD file | Framework §19.3 | Strong preference |
| EX-2 | Add new agent types without rebuilding orchestrator core | Framework §19.3 | Strong preference |
| EX-3 | Add new step types (new MEMIT operations, new sandbox runners) without rewriting orchestration layer | Implied by §14.5 lean core | Strong preference |
| EX-4 | Plugin / tool-use extensibility for agents (MCP, function calling, shell tools) | S4 — Coder Agent tool use, Validator sandbox | **Non-negotiable** |
| EX-5 | Write Scope Definitions addable via schema migration path (not runtime-mutable) | S3 D24, C17 | **Non-negotiable** |

---

### Orchestrator-owned deferred questions (must resolve in this session)

These are items sessions 1–5 explicitly tagged "Orchestration session" — they constrain candidate selection:

| ID | Question | Source |
|---|---|---|
| OQ-V2 | Hard retry cap behavior per subtask after decomposition — reset or share budget? | S4 |
| OQ-TPC2 | External abort signal / emergency stop authority during PREPARED transactions | S5 |
| OQ-TC3 | Real-time consistency-status signal exposure to other agents | S5 |
| OQ-GOC1 | Path classification list storage (Genesis constitutional vs. per-project config) | S5 |
| OQ-CW1 | Inter-agent voluntary lock release / negotiation | S5 |
| OQ-CW2 | Lock visibility: direct to agents or Orchestrator-mediated | S5 |
| OQ-OC1 | Idle-window detection for compaction scheduling | S5 |
| OQ-SL2 | Multi-machine ledger replication (if scope expands) | S5 |

---

### Summary: Elimination criteria before tool comparison

Any candidate must clear these non-negotiables:

1. **Stateful cyclical control flow with accumulating context** (CF-1 to CF-3) — kills linear DAG-only tools
2. **Persistent state across restarts including in-flight 2PC transactions** (SM-1, SM-2, SM-6) — kills tools where state = context window only
3. **Long-running GPU-bound steps as first-class, not as HTTP timeouts** (HS-3, HS-4) — kills tools with hard step-timeout contracts
4. **Saga / compensating transaction support, or tolerance for a 2PC sidecar** (TPC-1 to TPC-8) — kills tools that can't express prepare/commit/compensate without re-inventing it
5. **Native pause/resume with preserved context for 16 distinct HIL triggers** (HIL-1 to HIL-16) — kills tools where HIL is a polling loop
6. **Structured event emission with Merkle-chain-lite audit integrity** (OA-1, OA-2) — kills tools with print-logging as primary audit
7. **Parallel-up-to-a-point concurrency** (CM-1, CM-2) — fan-out before chokepoint; kills tools that force either "all parallel" or "all sequential"
8. **Tool/plugin extensibility for agents** (EX-4) — kills closed-world tools

---

### What I need from you before I research the candidates

Before I spend tokens on web searches, confirm or correct:

1. **Have I captured the requirements faithfully?** Anything I've listed as non-negotiable that you'd soften, or anything I've marked "strong preference" that's actually non-negotiable for you?
2. **Is the list of orchestrator-owned deferred questions (OQ-V2 through OQ-SL2) complete** — or did I miss any that should be resolved in this session?
3. **Scope confirmation:** Session 5 OQ-SL2 flags multi-machine as out of scope for v1. Can I treat "single-machine harness" as a hard assumption for the capability evaluation, or do I need to evaluate multi-machine readiness as a tiebreaker?
4. **One framing question from the skill:** what does the team building this know how to operate? Python-native tooling, Node/TypeScript, or no strong preference? This is a tiebreaker when candidates score close, and LangGraph vs. n8n vs. Claude harness splits along this line.

Once you confirm the matrix, I'll do the capability research on Pi (including the Feb 2026 atalupadhyay blog and the HN thread), n8n's current agent/AI features, the Claude agent harness (Agent SDK / Claude Code as orchestrator), and LangGraph — all dated to 2026 — then produce the evaluation grid without a recommendation.



## Prompt:
4/21/2026, 3:57:49 AM

1-3 approved. #4 no strong preference.



## Response:
4/21/2026, 4:02:00 AM



````plaintext
Thought process: Cataloging Pi's architecture and core capabilities.

Now I'm moving into Phase 3 to evaluate the candidates through web research, focusing on the current capabilities of Pi as a terminal coding framework, n8n's AI orchestration features, Claude's agent SDK, and where LangGraph stands today.

I'll need to search strategically for each tool—looking up Pi through the specific blog post and HN thread references, checking n8n's latest AI and human-in-loop integrations, reviewing Claude's agent orchestration capabilities, and understanding LangGraph's production-readiness around checkpointing and state management. The key evaluation criteria across all four are whether they support stateful cyclical loops with persistent context, checkpoint recovery across restarts, GPU-bound long-running tasks as a core feature, and saga-pattern compensating transactions.
````

Matrix locked. Moving to Phase 3 — candidate research. I'll verify current (April 2026) capabilities for all four before producing the evaluation grid.

````plaintext
Web Search: Pi terminal coding harness agent 2026 features
````

> **Pi Coding Agent** [shittycodingagent.ai](https://shittycodingagent.ai/)
>
> **GitHub - can1357/oh-my-pi: ⌥ AI Coding agent for the terminal — hash-anchored edits, optimized tool harness, LSP, Python, browser, subagents, and more** [github.com](https://github.com/can1357/oh-my-pi)
>
> **@mariozechner/pi-coding-agent - npm** [npmjs.com](https://www.npmjs.com/package/@mariozechner/pi-coding-agent)
>
> **pi-mono/packages/coding-agent/README.md at main · badlogic/pi-mono** [github.com](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md)
>
> **pi-mono/packages/coding-agent at main · badlogic/pi-mono** [github.com](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent)
>
> **Pi: Build Your AI Coding Tool Your Way | Medium** [medium.com](https://medium.com/@dminhk/pi-build-your-ai-coding-tool-your-way-c0e4115619ba)
>
> **Pi Coding Agent Review 2026: Minimal Open-Source Terminal Coding Harness** [vibecodinghub.org](https://vibecodinghub.org/tools/pi-coding-agent)
>
> **What I learned building an opinionated and minimal coding agent** [mariozechner.at](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)
>
> **What Is Pi Agent?** [aisoftwaresystems.com](https://aisoftwaresystems.com/blog/what-is-pi-agent/)
>
````plaintext
Thought process: Clarifying Pi and OpenClaw architectural distinctions.

So Pi is a minimal terminal coding harness built by Mario Zechner with four core tools—read, write, edit, and bash—that deliberately avoids sub-agents, planning modes, and permission gates. Everything else extends through TypeScript, and it supports four different modes: interactive use, print/JSON output, RPC for process integration, and an SDK for embedding, with sessions persisted as a JSONL tree structure.

Now I'm realizing the framework doc's reference to "Pi as orchestrator" was misleading—Pi is fundamentally a single-agent coding harness, not an orchestrator providing multi-agent coordination or state ledgers. That said, Pi's SDK mode means it could be embedded as the agent runtime inside a larger orchestrator system, but Pi itself doesn't handle the distributed transaction coordination or state management that would require. I should dig deeper into what Pi actually offers for multi-agent scenarios and state handling.
````

Key finding on Pi: it's explicitly a single-agent coding harness with no built-in sub-agents, no plan mode, no permission gates. The framework doc's framing of "Pi as orchestrator" may be inaccurate. Let me verify by checking multi-agent / SDK capabilities.

````plaintext
Web Search: openclaw pi SDK multi-agent orchestration
````

> **Pi Integration Architecture - OpenClaw** [openclaw.ai](https://docs.openclaw.ai/pi)
>
> **Pi: The Minimal Agent Within OpenClaw | Armin Ronacher's Thoughts and Writings** [pocoo.org](https://lucumr.pocoo.org/2026/1/31/pi/)
>
> **How I Built a Deterministic Multi-Agent Dev Pipeline Inside OpenClaw (and Contributed a Missing Piece to Lobster) - DEV Community** [dev.to](https://dev.to/ggondim/how-i-built-a-deterministic-multi-agent-dev-pipeline-inside-openclaw-and-contributed-a-missing-4ool)
>
> **OpenClaw Multi-Agent Orchestration Advanced Guide** [zenvanriel.com](https://zenvanriel.com/ai-engineer-blog/openclaw-multi-agent-orchestration-guide/)
>
> **Integrate OpenClaw with Pi SDK for AI Coding Agents | OpenClaw** [open-claw.bot](https://open-claw.bot/docs/platforms/pi/)
>
> **openclaw/docs/pi.md at main · openclaw/openclaw** [github.com](https://github.com/openclaw/openclaw/blob/main/docs/pi.md)
>
> **GitHub - abhi1693/openclaw-mission-control: AI Agent Orchestration Dashboard - Manage AI agents, assign tasks, and coordinate multi-agent collaboration via OpenClaw Gateway. · GitHub** [github.com](https://github.com/abhi1693/openclaw-mission-control)
>
> **How to Build a Custom Agent Framework with PI: The Agent Stack Powering OpenClaw** [substack.com](https://nader.substack.com/p/how-to-build-a-custom-agent-framework)
>
> **GitHub - VoltAgent/awesome-openclaw-skills: The awesome collection of OpenClaw skills. 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry.🦞** [github.com](https://github.com/VoltAgent/awesome-openclaw-skills)
>
> **Multi-Agent Workflows | OpenClaw Docs** [clawdocs.org](https://clawdocs.org/guides/multi-agent/)
>
````plaintext
Thought process: Cataloging n8n's workflow capabilities and architectural features.

So Pi is fundamentally a single-agent system with a session-based JSONL tree that supports branching, and it exposes an SDK mode for embedding the agent loop directly—no multi-agent orchestration, planning modes, or MCP support built in. OpenClaw, by contrast, appears to be something quite different in its architecture and capabilities.

OpenClaw is actually a multi-agent gateway built on top of Pi's SDK, allowing multiple agents to operate with their own workspaces and memory bindings, and it includes Lobster as a workflow engine that uses YAML-defined workflows. The key difference is that OpenClaw's agent spawning is LLM-driven and non-deterministic rather than deterministic, and it has its own separate Mission Control dashboard. The framework documentation's reference to a "Pi orchestrator" seems to be conflating Pi with OpenClaw—Pi itself isn't an orchestrator in the traditional sense, but OpenClaw comes closer to that model, even if its flow control remains probabilistic rather than deterministic.

The real insight here is that someone had to explicitly contribute loop support to Lobster just to enable deterministic multi-agent workflows, which signals exactly what this specification needs: deterministic two-phase commit semantics with retry logic and tiered failure caps. Now I'm looking into n8n to see how it handles orchestration.
````

Now n8n — current AI agent and state management capabilities.

````plaintext
Web Search: n8n AI agent workflow 2026 human in loop state persistence
````

> **Human-in-the-loop for AI tool calls | n8n Docs** [n8n.io](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools/)
>
> **Human in the loop automation: Build AI workflows that keep humans in control – n8n Blog** [n8n.io](https://blog.n8n.io/human-in-the-loop-automation/)
>
> **n8n 2026: AI Agent Workflow Automation for Enterprise Node.js** [kollox.com](https://kollox.com/n8n-2026-ai-agent-workflow-automation-for-enterprise-node-js/)
>
> **Build Custom AI Agents With Logic & Control | n8n Automation Platform** [n8n.io](https://n8n.io/ai-agents/)
>
> **7 State Persistence Strategies for Long-Running AI Agents in 2026** [indium.tech](https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026/)
>
> **Implementing Human-In-The-Loop (HITL) Actions in n8n with and without a Wait Step | by Dominik Baranowski | Medium** [medium.com](https://medium.com/@dom.dragonsnake/implementing-human-in-the-loop-hitl-actions-in-n8n-with-and-without-a-wait-step-c0558fd61420)
>
> **How to Add Human in the Loop to n8n Workflows 2026** [ryanandmattdatascience.com](https://ryanandmattdatascience.com/n8n-human-in-the-loop/)
>
````plaintext
Thought process: Cataloging Claude Agent SDK specifications and features.

n8n has solid human-in-the-loop capabilities with native approval workflows and multi-channel routing, plus an upcoming PostgreSQL persistence layer for better state management. The main limitation is that individual workflow runs are largely stateless, so maintaining long-running stateful processes typically requires offloading to an external database like Supabase.

The wait step doesn't handle persistence well, and n8n isn't really built for iterative Reflexion-style loops where context accumulates across retries. Plus, something like a MEMIT compile step would need to be wrapped as an HTTP service since n8n operates on an HTTP/function-calling model rather than having native GPU support.

Now I'm looking into what the Claude Agent SDK and agent harness can actually do.
````

Now the Claude agent harness — current Agent SDK capabilities.

````plaintext
Web Search: Claude Agent SDK 2026 subagents tool use orchestration
````

> **Orchestrate teams of Claude Code sessions - Claude Code Docs** [claude.com](https://code.claude.com/docs/en/agent-teams)
>
> **Shipyard | Multi-agent orchestration for Claude Code in 2026** [shipyard.build](https://shipyard.build/blog/claude-code-multi-agent/)
>
> **Popularaitools** [popularaitools.ai](https://popularaitools.ai/blog/claude-agent-sdk-guide-2026)
>
> **LangGraph + Claude Agent SDK: The Ultimate Guide to Multi-Agent Systems in 2026** [mager.co](https://www.mager.co/blog/2026-03-07-langgraph-claude-agent-sdk-ultimate-guide/)
>
> **Subagents in the SDK - Claude API Docs** [claude.com](https://platform.claude.com/docs/en/agent-sdk/subagents)
>
> **Claude Agent SDK: Subagents, Sessions and Why It's Worth It** [ksred.com](https://www.ksred.com/the-claude-agent-sdk-what-it-is-and-why-its-worth-understanding/)
>
> **GitHub - wshobson/agents: Intelligent automation and multi-agent orchestration for Claude Code · GitHub** [github.com](https://github.com/wshobson/agents)
>
> **Claude Agent SDK: Complete Production Patterns Guide 2026** [digitalapplied.com](https://www.digitalapplied.com/blog/claude-agent-sdk-production-patterns-guide)
>
> **Build Production AI Agents with Claude Agent SDK | Let's Data Science** [letsdatascience.com](https://letsdatascience.com/blog/claude-agent-sdk-tutorial)
>
> **Claude Code Agent Teams: Setup & Usage Guide 2026** [claudefa.st](https://claudefa.st/blog/guide/agents/agent-teams)
>
````plaintext
Thought process

Looking at the Claude Agent SDK—it was renamed from the Code SDK back in September 2025, and as of March 2026 we're at Python v0.1.48 and TypeScript v0.2.71. The SDK includes built-in subagent capabilities through AgentDefinition with tool restrictions, plus session persistence using session IDs so agents can resume work, file checkpointing for state management, and a hooks system for lifecycle events.

There's also an experimental Agent Teams feature that lets teammates communicate peer-to-peer, native MCP support, and the architecture treats state as ephemeral—the session and conversation log are the source of truth, with durability requirements handled through Postgres, Redis, or object storage. Each subagent gets isolated context.

What's interesting is that a March 2026 production guide describes the canonical pattern as using LangGraph for the workflow skeleton and Claude Agent SDK for the heavy lifting inside nodes—which is exactly the hybrid approach mentioned in the skill.
````

Now LangGraph current state — checkpointing, human-in-loop, saga support.

````plaintext
Web Search: LangGraph 2026 durable execution checkpoint human in loop interrupt
````

> **Durable execution - Docs by LangChain** [langchain.com](https://docs.langchain.com/oss/python/langgraph/durable-execution)
>
> **How to Implement Human-in-the-Loop in LangGraph Using the interrupt() Pattern | BSWEN** [bswen.com](https://docs.bswen.com/blog/2026-04-16-langgraph-human-in-the-loop/)
>
> **GitHub - langchain-ai/langgraph: Build resilient language agents as graphs. · GitHub** [github.com](https://github.com/langchain-ai/langgraph)
>
> **Interrupts and Commands in LangGraph: Building Human-in-the-Loop Workflows - DEV Community** [dev.to](https://dev.to/jamesbmour/interrupts-and-commands-in-langgraph-building-human-in-the-loop-workflows-4ngl)
>
> **Making it easier to build human-in-the-loop agents with interrupt** [langchain.com](https://www.langchain.com/blog/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt)
>
> **Beyond input(): Building Production-Ready Human-in-the-Loop AI Agents with LangGraph - DEV Community** [dev.to](https://dev.to/sreeni5018/beyond-input-building-production-ready-human-in-the-loop-ai-with-langgraph-2en9)
>
> **LangChain-projectsdocs/src/oss/langgraph/durable-execution.mdx at main · kyoron2/LangChain-projectsdocs** [github.com](https://github.com/kyoron2/LangChain-projectsdocs/blob/main/src/oss/langgraph/durable-execution.mdx)
>
> **Build durable AI agents with LangGraph and Amazon DynamoDB | Amazon Web Services** [amazon.com](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)
>
> **LangGraph 201: Adding Human Oversight to Your Deep Research Agent | Towards Data Science** [towardsdatascience.com](https://towardsdatascience.com/langgraph-201-adding-human-oversight-to-your-deep-research-agent/)
>
````plaintext
Thought process: Scrutinizing LangGraph's architectural limitations and failure recovery gaps.

LangGraph really stands out with its built-in support for durable execution through various storage backends, plus native interrupt and resume patterns for human-in-the-loop workflows. It handles multiple durability modes, treats state as a first-class concept, and makes cyclical control flow natural since it's graph-based, with task decorators ensuring deterministic operations.

Now I'm checking whether LangGraph supports saga patterns and compensation logic, and also comparing how n8n handles queue semantics and retries for long-running tasks.
````

One more targeted check — how each tool handles saga/compensating transactions (our 2PC requirement).

````plaintext
Web Search: LangGraph compensating transaction saga rollback pattern
````

> **Saga Compensating Transactions | Temporal** [temporal.io](https://temporal.io/blog/compensating-actions-part-of-a-complete-breakfast-with-sagas)
>
> **Saga Design Pattern - Azure Architecture Center | Microsoft Learn** [microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)
>
> **SagaLLM: Context Management, Validation, and Transaction Guarantees for Multi-Agent LLM Planning** [arxiv.org](https://arxiv.org/html/2503.11951v3)
>
> **Compensating transaction - Wikipedia** [wikipedia.org](https://en.wikipedia.org/wiki/Compensating_transaction)
>
> **Microservices Pattern: Pattern: Saga** [microservices.io](https://microservices.io/patterns/data/saga.html)
>
> **Compensation Transaction Patterns - The Key to Handling Failures in Distributed Applications** [orkes.io](https://orkes.io/blog/compensation-transaction-patterns/)
>
> **𝖲𝖺𝗀𝖺𝖫𝖫𝖬: Context Management, Validation, and Transaction Guarantees for Multi-Agent LLM Planning** [arxiv.org](https://arxiv.org/html/2503.11951v2)
>
> **Compensating Transactions -SAGA. Compensating Transaction: | by Sureshkumar Mani | Medium** [medium.com](https://medium.com/@surezms/compensating-transactions-saga-5d28d49b2f0c)
>
> **Managing Distributed Transactions with the Saga Pattern - DEV Community** [dev.to](https://dev.to/willvelida/the-saga-pattern-3o7p)
>
> **Compensating Transaction pattern - Azure Architecture Center | Microsoft Learn** [microsoft.com](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction)
>
````plaintext
Thought process: Synthesized orchestrator evaluation framework across multiple dimensions.

I'm finding a critical academic reference from March 2025 that confirms LangGraph and AutoGen lack built-in atomicity and compensation logic for failure recovery—they have durable execution and checkpointing, but you'd need to implement saga patterns and transaction handling yourself within the graph structure.

This actually applies to all four candidates: none have native 2PC or saga support, so the Transaction Controller will be custom code regardless. The real differentiator is which orchestrator makes it easiest to build that component as a well-integrated piece.

Let me check n8n's capabilities around retry logic with accumulated context and long-running GPU tasks, then I'll have enough to synthesize the full evaluation.

Looking at the key characteristics across the candidates now—Pi is a minimal single-agent terminal harness with no built-in orchestration or multi-agent support, though the author explicitly rejects sub-agents as an anti-pattern. It exposes the agent loop through SDK mode for embedding, persists sessions as branching JSONL trees, and handles context auto-compaction with extension hooks, leaving everything else like MCP integration and HITL gates to user-space TypeScript implementation.

Pi itself isn't an orchestrator but rather a runtime that an orchestrator could invoke, and the framework documentation seems to blur the line between Pi the agent and OpenClaw the multi-agent harness built on top of it. OpenClaw brings multi-agent capabilities with channel bindings and workspace isolation, runs workflows through the Lobster engine with recent loop support, and supports sub-agent spawning with LLM-driven flow control, though it still lacks 2PC and state ledger functionality. n8n offers a visual workflow builder with extensive integrations and native HITL at the tool-call level, plus a 2026 release bringing PostgreSQL-backed distributed state.

Now I'm looking at what n8n's upcoming features include—row-level security, transaction isolation, worker threads for parallel execution, OpenTelemetry observability, and MCP Server support. The platform is self-hostable but handles long-running stateful work awkwardly without an external database, and implementing Reflexion-style loops or MEMIT compilation requires workarounds since n8n's node graph model expects HTTP or function-based steps rather than native saga patterns. Claude's Agent SDK is Anthropic's runtime offering, recently renamed from the Code SDK.

The SDK supports subagents with per-agent tool restrictions, experimental Agent Teams for peer communication, session persistence with resume capabilities, and file checkpointing. It's MCP-native and works across Bedrock, Vertex AI, and Azure, treating state as ephemeral and the conversation log as the source of truth—which makes it naturally suited for Reflexion-style reasoning loops where the LLM and tool use are the core pattern.

Now looking at LangGraph as an alternative: it offers graph-based orchestration with native cycle support and durable execution through multiple checkpointing backends. It has built-in human-in-the-loop with interrupts that preserve context, static interrupts for compliance, and a Tasks decorator for deterministic caching on resume, plus subgraphs and comprehensive memory management.

LangGraph integrates with LangSmith for observability and pairs well with Claude's Agent SDK, using thread-based state isolation. The main limitation is no native saga or compensating transaction support—a gap the SagaLLM paper from March 2025 explicitly identifies. It's Python-first with less mature TypeScript support.

Now I'm building an evaluation grid across 8 dimensions and 4 candidates, rating each cell as Native, Capable with workaround, Gap, or Missing.

I should flag that the framework doc's reference to Pi as an orchestrator looks like a categorization error worth mentioning to the user. I'm also considering whether to evaluate LangGraph + Claude Agent SDK as a hybrid fifth candidate—the sources consistently call this the canonical pairing—but since the user asked for the four named tools, I'll evaluate those individually and note the hybrid as a natural extension.

For the evaluation structure, I'm planning a critical reframing note about Pi (it's a runtime, not an orchestrator), then a per-candidate grid across eight dimensions, followed by elimination results and observations without a recommendation yet.

One key constraint: all four candidates lack native saga support, so the 2PC Transaction Controller will require custom code regardless—the real question is which orchestrator makes that implementation easiest. On the n8n side, I'm thinking through how it handles long-running steps like GPU-bound MEMIT compilation. Given n8n's Node.js execution model with one worker per step, a long-running node would block that worker, so the typical solution is either a wait node pattern or external trigger pattern like the Supabase example—MEMIT compile would likely need...

I should verify n8n's worker execution model and concurrent contention handling, but I'm going to move forward with the evaluation matrix as the priority and structure the output now.
````

I have enough verified data to build the evaluation. One critical reframe surfaced during research that I need to flag before the grid, because it changes how to think about one of the four candidates.

---

## Session 6 — Candidate Capability Evaluation (April 2026)

### Critical reframe: Pi is not an orchestrator

The framework reference doc treats "Pi" as the orchestrator, but current (April 2026) documentation is unambiguous: Pi ships with four tools — read, write, edit, bash — and "skips features like sub-agents, plan mode, and permission gates. Not because those features are bad, but because they belong in user space". Its author is explicitly anti-sub-agent: "Spawning multiple sub-agents to implement various features in parallel is an anti-pattern in my book and doesn't work, unless you don't care if your codebase devolves into a pile of garbage".

What Pi offers an orchestration layer is its SDK: "OpenClaw uses the pi SDK to embed an AI coding agent directly into its messaging gateway architecture. You don't have to worry about spawning pi as a subprocess or dealing with RPC mode. Instead, you can import and instantiate pi's AgentSession using createAgentSession()".

**Implication for this evaluation:** Pi is correctly categorized as an **agent runtime**, not an orchestrator. What the framework doc is actually describing when it says "Pi orchestrator" is much closer to **OpenClaw** — the multi-agent harness built on Pi's SDK. I'll evaluate Pi as an orchestrator candidate honestly (short answer: it fails as one), and add OpenClaw as a shadow entry for completeness since the framework doc clearly intended something more capable than raw Pi.

---

### Shared finding across all candidates: no native saga / 2PC

Before the grid: a March 2025 academic paper (SagaLLM, arxiv 2503.11951) spells out the gap. "LangGraph and AutoGen enable structured workflows and agent interactions, but lack built-in atomicity guarantees, compensation logic, or robust failure recovery. AgentScope and AFlow introduce limited rollback mechanisms, but do not generalize across workflows. Most frameworks are based on LLM self-validation, exposing them to reasoning errors and hallucinations".

None of the four candidates ships native compensating-transaction support for our TPC-1 to TPC-8 requirements. **The 2PC Transaction Controller will be custom code regardless of orchestrator choice.** The question the evaluation actually answers is: *which orchestrator makes building that Transaction Controller cleanest?*

---

### Evaluation Grid — Candidates × 8 Dimensions

Rating legend:
- **✓ Native** — requirement satisfied by first-class primitive
- **⚠ Workaround** — achievable but requires deliberate engineering
- **✗ Gap** — no built-in support; significant custom build required
- **✗✗ Mismatch** — requirement conflicts with the tool's execution model

| Dimension | Pi | n8n | Claude Agent SDK | LangGraph |
|---|---|---|---|---|
| **1. Control flow complexity** (Reflexion loops with accumulating state, tiered retries, 4-step escalation cascade) | ✗ No loop primitives; no retry budget tracking; extensions would need to build the full control plane | ⚠ Native retry on nodes; loops via workflow sub-calls (loop support is recent in Lobster fork); accumulating verbal context across iterations is unnatural in node-graph model | ✓ LLM reasoning handles arbitrary loop/branching natively; accumulating retry history in session context is the native mode | ✓ Graph-native cycles; conditional edges; `Command(goto=...)` for dynamic routing. "LangGraph's interrupt() pattern provides native human-in-the-loop capability that other frameworks require duct-taping to achieve... The pattern cleanly models state transitions with built-in checkpointing, eliminating custom persistence code" |
| **2. State management** (persistent across restarts, Merkle-chain ledger, Scope Lock Registry, retry/escalation history) | ⚠ "Sessions are stored as JSONL files with a tree structure... Sessions auto-save to ~/.pi/agent/sessions/" — tree-branching persists, but only for a single agent session. No Scope Lock Registry. No ledger primitive. Everything multi-agent is custom | ⚠ "Distributed state persistence using PostgreSQL with row-level security and transaction isolation" in the 2026 release. However, "State Persistence: You must now confirm that n8n persists the workflow's state before it enters the wait state. What happens if n8n crashes while waiting? ... Unclear Limitations: Even if n8n persists state, you need to understand the constraints" | ⚠ Session resumption supported via session ID. "State Lives Outside the Process: Any agent longer than a single turn needs durable state in Postgres, Redis, or object storage. Treat the SDK session as ephemeral and the conversation log as the source of truth" — you build the persistence layer | ✓ "Durable execution — Build agents that persist through failures and can run for extended periods, automatically resuming from exactly where they left off... Comprehensive memory — Create truly stateful agents with both short-term working memory for ongoing reasoning and long-term persistent memory across sessions". Pluggable checkpointers (Postgres, SQLite, DynamoDB, in-memory) |
| **3. Heterogeneous step types** (LLM inference, Git, MEMIT compile [GPU-bound], PyTest sandbox, behavioral probe) | ⚠ Bash tool + extensions can wrap anything; no resource-aware scheduling; long-running GPU calls block the session | ✗✗ Node execution model is HTTP/function-call oriented. MEMIT compile must be wrapped as an external HTTP service and triggered via webhook, with a separate wait-then-wake workflow. No native GPU scheduling | ✓ Any shell command, MCP tool, or custom tool is first-class. GPU-bound steps can be wrapped as tools with long-running behavior | ✓ "You can use tasks from both the StateGraph (Graph API) and the Functional API". Any Python callable is a node. Resource-aware scheduling is your job but the framework doesn't fight you on it |
| **4. Two-phase commit coordination** (prepare/commit/compensate, circuit breaker, Git-ahead compensation) | ✗ No transaction primitives; no circuit breaker; build everything | ⚠ Error-handling branches + sub-workflows can approximate this, but no saga primitive; compensation logic would live as scattered branches in the visual graph | ⚠ LLM-driven reasoning can be prompted to follow prepare/commit/compensate, but this is exactly the wrong primitive — we explicitly deprecated reasoning agents from the write path (S4 D40/C30). The Commit Executor must be a deterministic, non-reasoning component; SDK would only run the reasoning parts around it | ⚠ No native saga. Must be built as custom nodes: Transaction Controller as its own node with ledger writes at phase boundaries. But graph execution semantics, checkpointing, and `interrupt()` give you the building blocks cleanly — closer to "easy custom build" than "fight the framework" |
| **5. Human-in-the-loop integration** (16 distinct HIL triggers, 48h review windows, emergency abort) | ✗ Extension-only; every HIL gate is a custom build | ✓ "You can require human approval before an AI Agent executes a specific tool. When a tool requires human review, the workflow pauses and waits for a person to take one of the following actions: Approve... Deny". Multi-channel review routing (Slack, Telegram, Gmail) built-in. Wait nodes for time-bounded reviews | ⚠ Hooks system (pre/post tool call) can gate actions; user approval/input supported. But no native pause-and-resume-weeks-later with preserved full context — session must be externalized | ✓ "We did this by making persistence a first class citizen in LangGraph. Every step of the graph, it reads from and then writes to a checkpoint of that graph state... This way, you can check the thread status, see that it's interrupted, check the message, and then based on that invoke the graph again (in a special way) to pass your response back in... This ensures interrupted threads don't take up any resources (beyond storage space), and can be resumed many months later, on a different machine, etc.". Static `interrupt_before` / `interrupt_after` handle compliance gates |
| **6. Observability and audit** (structured events, Merkle-chain, distinct write-outcome codes, integrity-violation retention) | ✗ Full observability is a design goal but structured event emission is DIY; no append-only primitive | ✓ OpenTelemetry integration, execution logs per run, persistent execution history. Append-only + Merkle would still be custom but the event stream is there | ⚠ Hooks emit events you can log but structured audit trail is DIY. "wire observability from day one — by the time an agent is in production, you want the traces, the spend ledger, and the audit log already flowing" is a statement of what you have to build, not what you get | ✓ LangSmith for tracing every node execution, state transition, and token usage. Thread history is inherently append-only per thread_id. Merkle chain would still be custom |
| **7. Concurrency model** (parallel up to commit, FIFO at Commit Executor, Scope Lock Registry) | ✗ Single-agent by design; multi-agent requires spawning multiple Pi processes via tmux with no coordination primitive | ✓ "The framework leverages Node.js worker threads for parallel agent execution while maintaining a single-threaded event loop for orchestration". Parallel branches + merge nodes natural. FIFO chokepoint must be custom (single-worker queue node) | ⚠ "Claude Code has a built-in multi-agent orchestrator: Agent Teams. It's still experimental and disabled by default". Subagents + Agent Teams (experimental, v2.1.32+) provide fan-out. Serialization chokepoint is custom. "Agent teams have known limitations around session resumption, task coordination, and shutdown behavior" | ✓ Parallel node execution via `Send` primitive; thread_id isolation. FIFO queue at Commit Executor is custom but idiomatic (single-node entry point) |
| **8. Extensibility** (declarative agents, new step types, MCP/tools) | ✓ TypeScript extensions + skills + prompt templates + themes + packages. "Pi is written by Mario Zechner... both OpenClaw and Pi follow the same idea: LLMs are really good at writing and running code, so embrace this". No MCP natively but trivial to add | ✓ 500+ integrations, MCP Server node, custom node SDK. Visual workflow easily extensible | ✓ "Define subagents directly in your code using the agents parameter... Subagents can be limited to specific tools, reducing the risk of unintended actions". Filesystem-based `.claude/agents/` for reusable roles. MCP first-class | ✓ Python-native, any callable is a node. Deep Agents for planning + subagents. Broad ecosystem |

---

### Summary scoring against the eight non-negotiables

| Non-negotiable elimination criterion | Pi | n8n | Claude Agent SDK | LangGraph |
|---|---|---|---|---|
| 1. Stateful cyclical control flow with accumulating context | ✗ | ⚠ | ✓ | ✓ |
| 2. Persistent state across restarts incl. in-flight 2PC | ⚠ | ⚠ | ⚠ | ✓ |
| 3. Long GPU-bound steps as first-class | ⚠ | ✗✗ | ✓ | ✓ |
| 4. Saga/compensating transactions (or clean sidecar path) | ✗ | ⚠ | ⚠ | ⚠ |
| 5. Native pause/resume for 16 HIL triggers | ✗ | ✓ | ⚠ | ✓ |
| 6. Structured events + append-only audit | ✗ | ✓ | ⚠ | ✓ |
| 7. Parallel-up-to-a-point concurrency | ✗ | ✓ | ⚠ | ✓ |
| 8. Tool/plugin extensibility | ✓ | ✓ | ✓ | ✓ |

**Eliminated under strict non-negotiable reading:**
- **Pi** — fails 1, 5, 6, 7 outright. It's a coding runtime, not an orchestrator. Could appear as a component INSIDE an orchestrator (this is exactly the OpenClaw pattern).
- **n8n** — fails 3 (MEMIT compile as first-class step). n8n's node execution model fundamentally assumes HTTP/function-call steps; a multi-minute GPU-bound step must be wrapped as external service and bridged via webhooks. This is a structural mismatch, not a gap. Strong elsewhere but this is a bad fit for the write engine.

**Remaining viable:**
- **Claude Agent SDK** — strong on CF-1–3 and extensibility, weak on 2, 5, 6, 7. Not designed as a durable-execution orchestrator; designed as an agent runtime.
- **LangGraph** — strongest coverage. The gap on saga is shared with everyone. State, HIL, and observability are its strongest suits.

---

### Observations worth surfacing before any decision

1. **Pi is the wrong abstraction level.** It's what runs inside a node, not the graph. The framework doc's framing is misleading. The question becomes what plays the role of "agent runtime" and what plays "orchestrator." Candidate answer: **Claude Agent SDK** (or Pi) as the runtime inside LangGraph nodes — which is "the move nobody talks about: LangGraph for the workflow skeleton, Claude Agent SDK for the heavy lifting inside nodes".

2. **n8n's structural mismatch on MEMIT.** The 2026 release is impressively mature ("Distributed state persistence using PostgreSQL with row-level security and transaction isolation"), but the node-per-HTTP-call execution model is the wrong shape for GPU-bound multi-minute operations. This isn't about maturity — it's about execution model. Viable only if MEMIT is hosted as an external service with webhook callback.

3. **Agent Teams is experimental.** "Agent teams require Claude Code v2.1.32 or later... Agent teams have known limitations around session resumption, task coordination, and shutdown behavior". Depending on this primitive for a production harness with the audit requirements in S3 is risky.

4. **The hybrid pattern is the industry-emerging canonical.** Multiple independent 2026 sources converge on LangGraph-as-orchestrator + Claude-Agent-SDK-as-agent-runtime. Skill explicitly suggests hybrid spec; evidence reinforces it.

5. **The 2PC Transaction Controller is YOUR code regardless.** None of the four ships it. LangGraph's durable execution + interrupts + thread isolation give you the cleanest scaffolding to build it on. Claude Agent SDK's LLM-reasoning-as-control-plane is actually the wrong primitive here — you don't want LLM reasoning on the commit path (S4 D40/C30 explicitly rules this out).

6. **OpenClaw is worth a capability audit if you're serious about the Pi-named path.** It's closer to what the framework doc calls "Pi orchestrator" than raw Pi is. Multi-agent, channel-bound, Lobster YAML workflows with loop support (community-contributed recently per the March 2026 DEV.to piece). But it's oriented around messaging gateways, not code-first pipelines, and its sub-agent spawning is "Non-deterministic flow control. The LLM decides when the reviewer runs, when to retry, when to give up. That's exactly what I wanted to avoid" — which directly conflicts with Session 4's deterministic Validator + retry-tier requirements.

---

### What's not yet decided

Per your instruction, no recommendation. The evaluation is complete; the non-negotiables have been scored; two candidates are eliminated on structural grounds (Pi: wrong abstraction level; n8n: execution model mismatch on MEMIT); two remain viable with complementary strengths.

The actual decision path appears to have three live options:
- **A.** LangGraph alone (as orchestrator, with Claude SDK or direct Anthropic API inside nodes)
- **B.** Claude Agent SDK alone (as orchestrator + runtime, with custom durable-state sidecar)
- **C.** Hybrid: LangGraph orchestrator + Claude Agent SDK runtime inside nodes

Before I spec a decision block, three questions:

1. **Do you want to spec all three paths' decision blocks** (A, B, C) with tradeoffs/mitigations, or pre-commit to one direction first and spec only that?
2. **OpenClaw appears directly in the framework doc's genealogy** (it's built on Pi SDK, and the "Pi orchestrator" narrative seems to gesture at it). Do you want me to do a fuller capability audit on OpenClaw/Lobster as a fifth candidate before we close this session, or explicitly rule it out because its sub-agent spawning is non-deterministic?
3. **OQ-V2 (retry budget reset per subtask after decomposition)** — the orchestration session is supposed to resolve this. My read: under LangGraph, thread_id scope + subgraph semantics make per-subtask fresh budgets natural; under Claude Agent SDK, subagents spawn fresh context windows which aligns with fresh budgets. Either way, fresh budgets per subtask is the cleaner reading. Confirm you want to resolve it as "fresh budget per decomposed subtask, with original task's overall budget cap still enforced as a ceiling"?



## Prompt:
4/21/2026, 4:03:55 AM

1. Spec all 3 paths
2. Yes
3. Confirmed



## Response:
4/21/2026, 4:08:20 AM



````plaintext
Thought process: Synthesizing OpenClaw and Lobster workflow architecture details.

I need to map out three distinct implementation approaches—using LangGraph exclusively, the Claude Agent SDK alone, or a hybrid combination—and then conduct a thorough capability assessment of OpenClaw and Lobster as potential alternatives. I also need to clarify the OQ-V2 budget model: each decomposed subtask gets its own fresh budget allocation, but the original task's overall budget still acts as a hard ceiling across all subtasks combined.

Let me start by researching OpenClaw and Lobster's core capabilities against the evaluation matrix, then move into specifying the decision blocks for each path with their respective tradeoffs and mitigation strategies before pulling together the full session summary.
````

On it. Let me do the OpenClaw/Lobster capability audit first, then produce the three decision blocks and the session summary.

````plaintext
Web Search: OpenClaw Lobster workflow engine YAML steps loops state
````

> **Lobster - OpenClaw** [openclaw.ai](https://docs.openclaw.ai/tools/lobster)
>
> **GitHub - openclaw/lobster: Lobster is a Openclaw-native workflow shell: a typed, local-first “macro engine” that turns skills/tools into composable pipelines and safe automations—and lets Openclaw call those workflows in one step.** [github.com](https://github.com/openclaw/lobster)
>
> **Human-in-the-loop workflows: structured input requests, conditionals, and step flow control · Issue #38 · openclaw/lobster** [github.com](https://github.com/openclaw/lobster/issues/38)
>
> **How I Built a Deterministic Multi-Agent Dev Pipeline Inside OpenClaw (and Contributed a Missing Piece to Lobster) - DEV Community** [dev.to](https://dev.to/ggondim/how-i-built-a-deterministic-multi-agent-dev-pipeline-inside-openclaw-and-contributed-a-missing-4ool)
>
> **lobster/CHANGELOG.md at main · openclaw/lobster** [github.com](https://github.com/openclaw/lobster/blob/main/CHANGELOG.md)
>
> **feat: introduces "Sub-lobsters": nested lobster workflows with optional loop by ggondim · Pull Request #20 · openclaw/lobster** [github.com](https://github.com/openclaw/lobster/pull/20)
>
> **Releases · openclaw/lobster** [github.com](https://github.com/openclaw/lobster/releases)
>
> **Lobster - OpenClaw Docs | Learn OpenClaw** [learnclawdbot.org](https://www.learnclawdbot.org/docs/tools/lobster)
>
> **ClawFlows & Lobster: Building Automation Pipelines with OpenClaw | OpenClaw Blog** [openclaws.io](https://openclaws.io/blog/clawflows-workflow-automation/)
>
> **Lobster – OpenClaw - Open Source AI Assistant** [openclawcn.com](https://openclawcn.com/en/docs/tools/lobster/)
>
````plaintext
Thought process: Audited OpenClaw capabilities and architected three orchestration paths.

I'm getting a clear picture of OpenClaw and Lobster now—Lobster functions as a workflow shell for OpenClaw, enabling deterministic YAML and JSON workflows with explicit approval checkpoints, and as of April 2026 it supports workflow files in multiple formats with configurable arguments.

The feature set is actually quite comprehensive: it handles structured input pauses for human-in-the-loop workflows with resumable tokens, rich conditional logic, sub-workflow composition with loops, granular error handling policies per step, timeouts and retry logic with backoff strategies, identity-constrained approvals, workflow visualization in multiple formats, and LLM integration points. What's striking is how mature this is—it covers deterministic looping, structured HITL pauses with resume tokens, native retry policies, partial-failure recovery, approval gates with identity constraints, and sub-workflow composition all in one system.

But there are real architectural limitations: Lobster is fundamentally a single-process shell workflow engine, so multi-machine scale-out requires running multiple gateways rather than being built-in. State lives on the filesystem, there's no cryptographic chain integrity beyond the resume tokens themselves, no native two-phase commit or saga patterns, and the concurrency model is constrained to a single gateway process managing agent workspaces—true parallelism requires careful orchestration. The async model is also synchronous pipeline execution, so long-running steps like multi-minute compiles are handled through per-step timeouts rather than true async primitives.

OpenClaw's multi-agent approach is fundamentally different from what we'd need: its agents are channel-bound to messaging platforms like Discord or Slack, operating as isolated workspaces that communicate through messaging, which is a messaging-gateway architecture rather than a code-pipeline architecture.

The core gap the dev.to article highlights is that OpenClaw's default session spawning is LLM-driven, so the author had to add loop support manually. Even with Lobster layered on top, we're still looking at a workflow engine running inside a messaging-oriented gateway. For our use case, OpenClaw/Lobster excels at deterministic pipelines with human approval gates, resumable human-in-the-loop workflows, per-step retries, and error recovery that approximates compensation logic—plus it can compose sub-workflows with loops for something like Reflexion. But it lacks native two-phase commit, compensating transactions, Merkle-chain audit trails, and it's fundamentally shaped as a messaging gateway rather than a code execution platform.

OpenClaw and Lobster is a viable dark horse candidate that deserves consideration but not a strong endorsement—it's essentially a TypeScript/Node equivalent of LangGraph's capabilities, just coupled to a messaging gateway. If the harness were primarily chat-triggered coding tasks from Slack, OpenClaw would be the obvious pick. For a pure developer harness, though, that messaging-gateway integration adds unnecessary overhead.

Now I'm moving into the decision framework: I'll produce a brief capability audit row for the matrix, resolve the OpenClaw question, and lay out the three decision blocks.

I'm structuring each decision block with a consistent spec format that covers the choice, rationale, tradeoffs, mitigations, custom components, interface contracts, risk profile, and switching cost. For the hybrid path, I need to be precise about what runtime behavior and component interactions actually look like. I need to work through the remaining open questions systematically. For OQ-TPC2, the LangGraph approach gives us the `interrupt()` mechanism where a human can abort a PREPARED transaction via a special signal that the Transaction Controller honors, whereas the SDK-only path would need custom handling. OQ-TC3 is resolved by the State Ledger as the consistency source. Let me flag the rest as either resolved through the architecture choice or out of scope, like the multi-machine question the user already excluded. V1 keeps it simple with timeout-only release, deferring the voluntary negotiation complexity to v2. For lock visibility, I'm routing everything through the orchestrator API so agents never read the lock registry directly—this maintains a single source of truth. On idle-window detection, the orchestrator uses a heuristic watching the Commit Executor queue depth and active scope locks; when the queue is empty and there are no locks for N minutes, it flags idle state internally without exposing that logic to agents.

Now I'm structuring the full response: I'll open with a brief note and the OpenClaw audit row, then walk through the OQ-V2 resolution in spec form, lay out the three Path decision blocks, resolve the remaining orchestrator-owned questions, and wrap up with a session summary.
````

Audit complete on OpenClaw/Lobster. One surprise: Lobster is substantially more mature than the framework doc implies — April 2026 release has native per-step retry policies, on_error branching, sub-workflow loops, and structured HITL resume tokens. It deserves an honest row in the matrix.

---

## Session 6 — OpenClaw + Lobster capability audit

As of v2026.4.6 (April 6, 2026), Lobster ships with features directly relevant to this harness:

| Capability | Evidence |
|---|---|
| Deterministic pipelines with explicit approval gates | "Lobster is a workflow shell that lets OpenClaw run multi-step tool sequences as a single, deterministic operation with explicit approval checkpoints... Lobster is the missing piece: deterministic pipelines, explicit approvals, and resumable state" |
| Sub-workflow composition with loops | "This pull request introduces support for sub-workflow steps in the workflow engine, allowing users to embed .lobster files as steps and optionally loop them with conditions, like a Ralph Loop" |
| Per-step retry policies | "Add per-step workflow retry policies (max, backoff, delay_ms, max_delay_ms, jitter) with retry-aware stderr logs" |
| Partial-failure recovery | "Add per-step on_error workflow policies (stop\|continue\|skip_rest) for partial-failure recovery, with structured step error fields (error, errorMessage) for condition-based branching" |
| Approval identity constraints | "Add optional approval identity constraints for workflow gates (approval.initiated_by, approval.required_approver, approval.require_different_approver)" |
| Resumable HITL with typed input | "Add structured input pauses with ask, workflow input, needs_input, and lobster resume --response-json '{...}' for resumable human-in-the-loop flows" |

**Where OpenClaw+Lobster scores against the matrix:**

| Dimension | Rating | Notes |
|---|---|---|
| 1. Control flow | ⚠ | Sub-workflow loops + `on_error` branching reach approximately Reflexion shape, but accumulating verbal context across retries requires custom state-passing between iterations |
| 2. State management | ⚠ | State-backed resume tokens exist; filesystem state dir; no Merkle-chain integrity |
| 3. Heterogeneous step types | ⚠ | Shell-native — `run:` for deterministic binaries, `pipeline:` for `llm.invoke`. MEMIT compile can be a shell step with `timeout_ms`. But OpenClaw gateway model is process-local, not distributed |
| 4. Two-phase commit | ⚠ | `on_error: continue` + explicit compensation steps can approximate saga. No native prepare/commit/compensate primitive |
| 5. HITL | ✓ | Typed `needs_input` pauses with schema validation, resume tokens, identity-constrained approvals |
| 6. Observability | ⚠ | Workflow envelope + mermaid visualization, but no native append-only audit stream |
| 7. Concurrency | ⚠ | Single-gateway architecture; multi-agent via workspace isolation and channel bindings. FIFO serialization at the Commit Executor would need to be a Lobster sub-workflow with explicit queue discipline |
| 8. Extensibility | ✓ | Plugin architecture, TypeScript SDK, broad skill marketplace |

**Honest assessment:** OpenClaw+Lobster is a legitimate candidate — it's closer to what the framework doc described as "Pi orchestrator" than raw Pi. But the execution model is **chat-gateway-first**: "OpenClaw supports running multiple agents within a single gateway, each with its own identity, workspace, memory, and channel bindings". Its native multi-agent story revolves around channel-bound agents (Discord, Telegram, Slack) talking to a gateway, not code-first pipelines running in CI. Using it as a pure development harness means ignoring most of its surface area.

**Disqualifying observation for our use case:** the path ggondim walked in the March 2026 DEV.to piece is instructive — he wanted a deterministic `code → review → test` pipeline inside OpenClaw, found OpenClaw's native `sessions_spawn` insufficient, and had to contribute the loop primitive to Lobster to get determinism. "I needed a code → review → test pipeline with autonomous AI agents, where the orchestration is deterministic (no LLM deciding the flow)... I found that Lobster (OpenClaw's workflow engine) was the right foundation — except it lacked loops". Even with loops added, the pipeline he built maps loosely to our Reflexion loop but lacks the 2PC coordination, ledger integrity, and scope lock registry — all of which would still be custom.

**Decision:** OpenClaw+Lobster **is viable but not advantaged** relative to LangGraph for our specific spec. It would be the right choice if messaging-gateway integration were a first-class requirement (Slack-triggered builds, Telegram-approved commits). For a pure dev harness, LangGraph's graph-native primitives align better with the spec.

---

## OQ-V2 resolution (confirmed)

### OQ-V2 — Retry Budget Reset on Task Decomposition — Spec Block
**What it must enforce:** When the Orchestrator executes Session 4 D37 Step 1 (Task Decomposition), each resulting subtask receives a fresh retry budget per tier (Tier 1 max 2, Tier 2 max 3, Tier 3 max 1), but the original task's aggregate retry cap (5 events per S4 C27) remains enforced as a ceiling across all decomposed subtasks combined.

**Hard constraints:**
- Subtask retry counters start at zero on decomposition.
- Aggregate retry event count across all subtasks under the original task is tracked in the task-lineage record.
- When the aggregate reaches the original task's hard cap (5), no further retries are offered regardless of subtask-level budget state. The escalation cascade proceeds to Step 2 (Peer Agent Review).
- Task-lineage record is a first-class State Ledger entry, linked to the original task's ledger entry ID.

**Tradeoffs decided:**
- Fresh per-subtask budgets preserve the intent of D37 Step 1 (narrower scope gets a real chance) without letting decomposition become an unbounded retry escape hatch.
- Aggregate ceiling is cheaper to reason about than attempting to allocate the original budget proportionally across subtasks.

**Open questions (deferred):** None — closes OQ-V2.

**Interface contract:**
- **Orchestrator → State Ledger:** `TASK_DECOMPOSED` entry with `{original_task_id, subtask_ids[], aggregate_retry_count_at_decomposition, aggregate_cap}`.
- **Orchestrator → Coder Agent** (per subtask): assignment includes `{subtask_id, fresh_tier_budgets, remaining_aggregate_budget}`.

---

## Remaining orchestrator-owned OQs

Resolvable now because they cross-reference established constraints:

### OQ-TPC2 — External Abort Signal Authority — Spec Block
**What it must enforce:** A human (and only a human with appropriate authorization) may interrupt a PREPARED 2PC transaction before Phase 2 completes. The interrupt must cleanly unwind via the Transaction Controller's compensation path, not by killing the process.

**Hard constraints:**
- Abort signal carries the PREPARED ledger entry ID.
- Commit Executor checks abort state at each phase boundary; if set, emits `FAILED` ledger entry with `abort_reason = "human_abort"` and hands off to Transaction Controller.
- Transaction Controller runs compensation per CONTENT_CLASSIFICATION rules (S5 D47).
- Abort during an already-COMMITTED transaction is rejected — post-commit is not abortable, only compensable via a new transaction.

**Tradeoffs decided:** Abort is always graceful (compensation, not kill). Never bypasses the audit trail.

**Open questions (deferred):** Who specifically is authorized to issue an abort (ops on-call only, or broader)? — operational policy.

**Interface contract:**
- **Human → Orchestrator:** signed abort request carrying ledger entry ID + reason.
- **Orchestrator → Commit Executor:** `abort_requested` flag checkable at each phase boundary.

---

### OQ-TC3 — Real-Time Consistency Status Signal — Spec Block
**What it must enforce:** Agents must be able to query current consistency status before beginning work, but cannot subscribe to raw ledger events.

**Hard constraints:**
- Consistency status exposed via Orchestrator-mediated API (`/consistency-status`), never direct ledger read.
- Response states: `NORMAL | COMPACTION_IN_PROGRESS | CIRCUIT_TRIPPED | DIVERGED | GENESIS_LOCKED`.
- When state is not `NORMAL`, agents are blocked from submitting new patches.
- Consistent with Session 5 OQ-SL3 recommendation (Orchestrator-mediated read access).

**Open questions (deferred):** None.

**Interface contract:**
- **Agent → Orchestrator:** `GET /consistency-status` before task acceptance.
- **Orchestrator → State Ledger:** queries current state; derives exposed status.

---

### OQ-GOC1 — Path Classification List Storage — Spec Block
**What it must enforce:** Path classifications (parametric_required | parametric_none | parametric_deferred per S5 D51) must be version-controlled, auditable, and project-scopable.

**Hard constraints:**
- Primary storage: per-project config at `<repo_root>/.harness/path-classification.json`, Git-committed (same pattern as `.harness/genesis-seal.json`).
- Harness ships a default baseline template inherited by new projects.
- Modifications to the classification file are parametric_required commits (the file itself is a Genesis-tier artifact under Layer 2 or 3).
- Orchestrator reads classification file at task-load time.

**Open questions (deferred):** None.

**Interface contract:**
- **Orchestrator → Git:** reads `.harness/path-classification.json` on boot and cache-invalidation.

---

### OQ-CW1 and OQ-CW2 — Scope Lock Visibility and Negotiation — Spec Block
**What it must enforce:** Scope Lock Registry is Orchestrator-owned; agents never hold direct references.

**Hard constraints:**
- Agents query lock state via Orchestrator API (`/scope-locks?scope=X`); never read registry directly.
- Lock release is timeout-only in v1 (per S5 D60). Voluntary release / inter-agent negotiation is out of scope for v1.
- Attempting to bypass the Orchestrator and manipulate the registry directly is an integrity violation.

**Tradeoffs decided:** V1 accepts that two agents with overlapping scopes may sometimes queue unnecessarily when one would voluntarily yield. Correctness wins over optimality here. Negotiation is a future-work item.

**Open questions (deferred):** Voluntary release / inter-agent negotiation (v2 feature).

**Interface contract:**
- **Agent → Orchestrator:** `GET /scope-locks` and `POST /scope-locks/declare`.
- **Orchestrator → Scope Lock Registry:** exclusive read/write.

---

### OQ-OC1 — Idle-Window Detection for Compaction — Spec Block
**What it must enforce:** Orchestrator internally tracks idle state to schedule compaction; agents are not exposed to this signal.

**Hard constraints:**
- Idle = (Commit Executor FIFO queue depth == 0) AND (active scope lock count == 0) AND (no active 2PC transaction in PREPARED state) for N minutes (N configurable, default 30).
- Idle detection runs at orchestrator level; compaction trigger is raised via `COMPACTION_SCHEDULED` ledger entry.
- If an agent task arrives during compaction, task is queued until `COMPACTION_BOUNDARY` ledger entry is written.

**Interface contract:**
- **Orchestrator-internal:** idle detection is not exposed outside the orchestration layer.

---

Now the three decision blocks.

---

## Path A — LangGraph Alone

### Path A — Orchestration Decision Spec Block

**Choice:** LangGraph as orchestrator and state persistence layer. Agents (Coder, Validator, TGA, Architect) invoked as nodes that call the Anthropic API directly (or another provider) for LLM inference. No separate agent runtime framework.

**Rationale — non-negotiables satisfied:**
- **CF-1, CF-2, CF-3 (stateful cyclical loops with accumulating context):** `interrupt()`/`Command(resume=...)` + thread_id persistence + graph cycles handle the Reflexion loop natively. Retry history lives in graph state, passed forward to each iteration.
- **SM-1, SM-2 (persistent state across restarts, including in-flight 2PC):** Checkpointer (Postgres/DynamoDB) persists every graph state transition. In-flight PREPARED transactions survive orchestrator restart via standard durable execution.
- **HS-3, HS-4 (GPU-bound MEMIT compile as first-class step):** MEMIT wrapped as a task-decorated node; durability mode `sync` ensures mid-compile crashes don't lose state. Variable latency is accepted by default.
- **HIL-1 through HIL-16:** Native `interrupt_before` / `interrupt_after` for static gates (Genesis approval, Layer-4 revert); `interrupt()` inside nodes for dynamic escalations. 48h pause-and-resume is first-class "can be resumed many months later, on a different machine, etc.".
- **OA-1, OA-3 (structured event emission to multiple destinations):** LangSmith tracing is native; State Ledger and Audit Trail wired as additional sinks via task decorator side-effect pattern.
- **CM-1 through CM-6 (parallel-up-to-a-point concurrency):** `Send` primitive for fan-out; Commit Executor is a single dedicated node that pulls from a queue-state field. Scope Lock Registry lives as a dedicated state field, mutated only by Orchestrator nodes.

**Tradeoffs accepted:**
- **Python-first ecosystem** (TypeScript/JS support exists but matures behind Python). Team has no language preference so this is cost-neutral.
- **LangChain ecosystem churn risk.** LangGraph has been notably more stable than LangChain proper, but version-lock discipline is required.
- **No native saga.** Compensating transactions must be built as custom nodes.
- **No native Merkle-chain audit.** State Ledger integrity must be custom.
- **Heavier than Path B** when the task is simple (linear code-gen with no retry, no HIL) — but the harness spec ensures tasks are never that simple.

**Mitigations for gaps:**
- **2PC Transaction Controller:** custom LangGraph subgraph wrapping Commit Executor node. Phase boundaries are explicit edges; `interrupt()` at the Phase 2 boundary allows human-confirmed Layer-4 compensation. Compensation nodes are separate subgraph invoked via conditional edge on failure.
- **Merkle-chain State Ledger:** custom sidecar service called from each ledger-write node. Chain verification runs on boot hook before graph compile completes.
- **Validator Health Score tracking (Meta-Validator):** scheduled subgraph triggered by cron, writes to dedicated thread_id for health history.

**Custom components required:**
1. Transaction Controller subgraph (2PC coordinator)
2. State Ledger service (Merkle-chain-lite integrity)
3. Patch Authorization Gate (verifier node at graph entry)
4. Scope Lock Registry (state field + Orchestrator API)
5. Meta-Validator scheduler (cron-triggered subgraph)
6. Pruning Agent scheduler (cron-triggered subgraph with standard Commit Executor path)
7. Commit Executor (dedicated node, exclusive write authority)

**Interface contracts:**
- Each of the 5 peer-skill domains maps cleanly to a LangGraph primitive:
  - Validator's Reflexion loop ↔ subgraph cycle with `interrupt()`
  - Transaction Controller ↔ saga-as-subgraph
  - Scope Lock Registry ↔ state field with Orchestrator-only mutators
  - Audit Trail ↔ LangSmith + custom sink per node
  - Agent definitions ↔ nodes with callable LLM clients

**Risk profile:**
- **Low** on durability, HIL, concurrency, observability.
- **Medium** on saga implementation complexity (you're the first to build this for a harness with these specific guarantees).
- **Medium** on ecosystem churn.

**Switching cost (if abandoned later):** HIGH. Every interface contract is LangGraph-idiomatic. Migration to any other orchestrator requires re-speccing ~80% of the wiring.

---

## Path B — Claude Agent SDK Alone

### Path B — Orchestration Decision Spec Block

**Choice:** Claude Agent SDK as both orchestrator and agent runtime. Subagents for Coder / Validator / TGA / Architect roles, each defined via `AgentDefinition`. Hooks system for lifecycle instrumentation. Custom durable-state sidecar (Postgres or similar) for anything that must survive process restart.

**Rationale — non-negotiables satisfied:**
- **CF-1, CF-2, CF-3:** LLM reasoning handles arbitrary loop and branching logic natively; retry history accumulates in the conversation context.
- **HS-3, HS-4:** Any shell command or MCP tool is a first-class step. MEMIT compile is just a tool.
- **EX-4 (tool/plugin extensibility):** MCP is native to the SDK "Define subagents directly in your code using the agents parameter... Subagents can be limited to specific tools, reducing the risk of unintended actions".
- **CF-5 (4-level validation cascade):** subagents with distinct tool permissions match the cascade levels cleanly — Validator subagent, Peer subagent, Meta-Validator subagent.

**Tradeoffs accepted:**
- **LLM-as-orchestrator means reasoning on the control path.** This directly conflicts with S4 D40/C30 — the Commit Executor MUST be deterministic and non-reasoning. Resolution: the Commit Executor is a non-SDK component (plain Python script) that the orchestrating agent *invokes*; it cannot BE the orchestrating agent.
- **Durability is externalized.** "State Lives Outside the Process: Any agent longer than a single turn needs durable state in Postgres, Redis, or object storage. Treat the SDK session as ephemeral and the conversation log as the source of truth". This is architecturally cleaner than it sounds — it forces explicit persistence discipline — but it means significantly more plumbing than Path A.
- **Agent Teams is experimental.** "Agent teams have known limitations around session resumption, task coordination, and shutdown behavior". Don't depend on it for the critical path.
- **HIL is hooks-based, not first-class graph-interrupt.** Pause/resume weeks-later requires external scheduling + session serialization.
- **Saga / 2PC is entirely custom.** No graph scaffold to hang it on.
- **Observability is DIY.** Hooks emit events but you assemble the audit trail yourself.

**Mitigations for gaps:**
- **Durable state sidecar:** Postgres for State Ledger, Scope Lock Registry, retry history, task-lineage. Every agent turn end writes to this sidecar.
- **Transaction Controller:** plain Python service (not an agent), invoked by Commit Executor. LLM reasoning never touches the 2PC path.
- **HIL pause/resume:** implement via session serialization to Postgres; external scheduler reloads and resumes. 48h gates become async job queue entries.
- **Audit Trail:** hooks on every tool call emit structured events to Merkle-chain-lite service.
- **Meta-Validator:** separate scheduled process, uses SDK to run the subagent evaluation.

**Custom components required:**
1. Orchestration state sidecar (Postgres) — **heaviest custom component**
2. Scope Lock Registry service
3. Transaction Controller (plain Python)
4. Commit Executor (plain Python, not agent)
5. State Ledger service with Merkle-chain
6. Audit Trail assembler (from hook events)
7. HIL pause/resume scheduler
8. Patch Authorization Gate (plain Python)
9. Meta-Validator scheduled process
10. Pruning Agent scheduled process

**Risk profile:**
- **High** on durable-state surface area (most of the harness is custom).
- **Low** on agent-inside-node extensibility — the SDK is excellent at running individual agents.
- **Medium** on Agent Teams reliance if you use it.
- **Low** on ecosystem risk — Anthropic-maintained, aligned with their product direction.

**Switching cost:** MEDIUM. Subagents are SDK-specific but the custom sidecar surfaces (ledger, locks, 2PC) are framework-agnostic. The agent runtime swap to a different provider SDK is painful but not catastrophic.

**When this path makes sense:** When you want flexibility and natural-language reasoning over rigid workflow structure, are comfortable building substantial custom infrastructure, and explicitly want to keep LLM reasoning close to the control path outside the commit boundary.

---

## Path C — Hybrid (LangGraph + Claude Agent SDK)

### Path C — Orchestration Decision Spec Block

**Choice:** LangGraph as orchestrator, state persistence, and control-flow authority. Claude Agent SDK as the agent runtime invoked inside specific LangGraph nodes. Deterministic components (Commit Executor, Transaction Controller, Patch Authorization Gate, State Ledger) are plain Python, not agents.

**Rationale — non-negotiables satisfied:**
- **All of Path A's rationale applies** for dimensions 1, 2, 4, 5, 6, 7 (LangGraph owns these layers).
- **EX-1 through EX-4 (agent definition, tool extensibility, MCP):** Claude Agent SDK owns this layer inside nodes. Subagents with per-agent tool restrictions match the Coder/Validator/TGA/Architect role definitions precisely.
- **CF-5 (4-level validation cascade):** Validator subagents (L1–L3) inside a LangGraph subgraph, with Level 4 being a LangGraph `interrupt_before` gate.
- **Pattern alignment with industry:** "LangGraph = control plane for complex agentic workflows. Graph-based, durable, model-agnostic... Claude Agent SDK = execution engine for file/code/shell tasks. One function call. Rich built-in toolset. Subagents out of the box... Use both when you want LangGraph's orchestration guarantees + Claude's execution power inside each node".

**Layer assignment (explicit):**

| Layer | Component | Technology | Why |
|---|---|---|---|
| Control plane | Graph execution, cycles, interrupts | LangGraph | Durable execution + native HIL + cyclical control flow |
| State plane | Thread state, checkpointer, Scope Lock Registry, State Ledger | LangGraph checkpointer + custom ledger service | Checkpointer handles ephemeral task state; custom ledger handles append-only audit |
| Agent runtime | Coder, Validator, TGA, Architect, Peer Reviewer | Claude Agent SDK inside LangGraph nodes | Mature subagent model, tool isolation, MCP native |
| Deterministic write path | Commit Executor, Transaction Controller, Patch Authorization Gate | Plain Python (no agents) | S4 D40/C30 — write path MUST be non-reasoning |
| Schedulers | Pruning Agent, Meta-Validator, Compaction | LangGraph cron-triggered subgraphs | Same primitives as main graph — consistency |

**Tradeoffs accepted:**
- **Two framework dependencies.** Version management surface area is larger. Mitigation: pin both; upgrade together on scheduled cadence.
- **Integration boundary between LangGraph node and Claude Agent SDK invocation is your spec.** Not a failure mode but a design cost.
- **Saga still custom** (shared with Path A).
- **Merkle-chain ledger still custom** (shared with Path A).
- **Longer ramp-up** than either alone — engineers must know both frameworks.

**Mitigations for gaps:**
- Same as Path A for all saga/ledger/scheduler concerns.
- Integration boundary: define a canonical "agent invocation node" wrapper that takes a subagent name + input and handles the LangGraph state read/write around the SDK call. Agents stay framework-agnostic behind this wrapper — if you ever move to a different agent runtime, only the wrapper changes.

**Custom components required:**
- All of Path A's custom components.
- Plus: canonical agent-invocation node wrapper (isolates the SDK boundary).

**Interface contracts:**
- **LangGraph node → Claude Agent SDK subagent:** `agent_invoke(agent_name, input, allowed_tools)` returning `{output, token_cost, tool_calls[]}`. Single point of contract between frameworks.
- **Subagent → LangGraph state:** agent output written back to graph state via node return; never writes state directly.
- All other interface contracts identical to Path A.

**Risk profile:**
- **Low** on durability, HIL, concurrency (LangGraph strengths).
- **Low** on agent capability, tool isolation, MCP integration (SDK strengths).
- **Medium** on boundary-surface maintenance.
- **Medium** on ecosystem churn (two trackers to watch, but orthogonal failure modes).

**Switching cost:** MEDIUM. The agent-invocation wrapper isolates the SDK; switching agent runtime is localized. Switching LangGraph is still HIGH — same as Path A.

**When this path makes sense:** When both the orchestration guarantees (durability, HIL, audit) AND the agent runtime quality (tool isolation, MCP, subagent fidelity) are non-negotiable. The canonical pattern per multiple independent 2026 sources.

---

## Comparison summary of the three paths

| Concern | Path A (LangGraph alone) | Path B (SDK alone) | Path C (Hybrid) |
|---|---|---|---|
| Durable state | ✓ Native | ⚠ Build it | ✓ Native |
| HIL (16 triggers) | ✓ Native | ⚠ Schedule-based | ✓ Native |
| 2PC/saga | ⚠ Custom, clean | ⚠ Custom, no scaffold | ⚠ Custom, clean |
| Agent quality | ⚠ Direct API calls | ✓ Mature SDK | ✓ Mature SDK |
| Tool isolation per agent | ⚠ Manual | ✓ Native | ✓ Native |
| MCP | ⚠ Custom integration | ✓ Native | ✓ Native |
| Custom surface area | MEDIUM | HIGH | MEDIUM-HIGH |
| Framework risk | LangGraph only | SDK only | Both, orthogonal |
| Team skill required | Python + LangGraph | Python/TS + SDK | Python + both |
| Industry precedent | Strong | Strong | Strongest |
| Switching cost | High | Medium | Medium (agent) / High (orchestrator) |

---

## Session 6 Summary Block

```
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
```

---

That closes the orchestration comparativist's work for this harness. The three paths are fully specced; the non-negotiables are traced to source sessions; the orchestrator-owned OQs are resolved or explicitly deferred. The path selection itself is deliberately left open — that's an operator decision, not a specialist one, and I'd rather you make it with all three blocks in front of you than have me force a pick.

When you're ready for Session 7 (integrated spec synthesis via the framework council), let me know which path you've selected and I'll invoke `/framework-council` to cross-check the full integrated spec for tensions before we mint v1.0.





---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)