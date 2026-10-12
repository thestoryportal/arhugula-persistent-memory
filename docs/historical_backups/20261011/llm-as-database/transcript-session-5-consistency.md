# Syncing Git and .vindex with two-phase commit

**Created:** 4/21/2026 3:35:20  
**Updated:** 4/21/2026 3:47:57  
**Exported:** 4/21/2026 9:10:43  
**Link:** [https://claude.ai/chat/86c9d0b2-62f5-456b-94f2-df9dfb59a06b](https://claude.ai/chat/86c9d0b2-62f5-456b-94f2-df9dfb59a06b)  

## Prompt:
4/21/2026, 3:35:22 AM

> File: validation-architecture-reflexion-loop-design.md

> File: threat-modeling-write-layer-access-control.md

> File: memit-specialist-spec-design.md

> File: ontological-schema-llm-databse-agent-framework.md

/state-consistency-theorist 
The write engine, security model, and validation pipeline are specced. Now I need to spec the coordination layer that keeps both memory mediums — Git and the .vindex overlay — in sync. Start with the two-phase commit design and the authoritative medium question.



## Response:
4/21/2026, 3:36:19 AM

````plaintext
View: Reading the State Consistency Theorist skill before kicking off Session 5.
````

````plaintext
Tool: Looking for relevant chats in this project...
````

Good — no prior State Consistency discussion in this project's memory to carry forward. Everything relevant is in the four session docs already in context.

---

# Session 5 — State Consistency Theorist

**Opening orientation**

Four sessions have given us the components; none of them have told us how the two mediums stay in lockstep. Let me quickly restate what Sessions 1–4 handed me, because this session's job is to spec the connective tissue between those decisions:

- **Session 2** gave me `IC6` (Write Engine → State Ledger outputs overlay filename + hash) and left `OQ-W4` (overlay compaction), `OQ-W9` (collision resolution authority), and `OQ-W10` (compaction strategy) on my desk.
- **Session 3** sealed the genesis hash as a lifetime rollback anchor (`C21`, `IC16`) and left me `OQ-S6` — *where* that sealed hash physically lives.
- **Session 4** handed me the critical interface (`IC23`): the **Commit Executor → Transaction Controller** handoff. That is the entry point into everything we're about to design. Session 4 also produced audit-trail gap records (`D37` Step 4) from suspended tasks — those are inputs the Pruning Agent has to be aware of.

Before I start producing spec blocks, I want to ground one concept and then ask you two foundational questions that everything downstream depends on.

---

## Grounding the concept: why this layer exists at all

In a normal application, "state" lives in one place — a Postgres database, say. You commit a transaction; either it succeeded or it didn't. One medium, one clock, one truth.

This harness has **two mediums with different physics**:

| | **Git (Medium A)** | **.vindex overlay (Medium B)** |
|---|---|---|
| Write operation | `git commit` (filesystem, near-instant) | MEMIT compile (GPU, seconds to minutes) |
| Failure modes | Disk full, merge conflict, hook rejection | GPU OOM, convergence failure, numerical instability |
| Time resolution | Discrete commits | Discrete snapshots |
| Rollback | `git revert` (cheap) | Unmount + remount (cheap), but recompute is expensive |

The dangerous asymmetry is the **failure profile**: Git commits almost always succeed when the prepare phase succeeds. MEMIT compiles can fail *after* the overlay file is written but *before* it's mounted as active, or fail entirely due to resource exhaustion. This asymmetry is what creates the divergence scenarios (`Git-ahead`, `Weights-ahead`, `Diverged`) from the consistency table in my domain knowledge.

**The Transaction Controller's existence is justified by this asymmetry.** If both mediums had symmetric failure profiles, you could just retry. Since they don't, you need a circuit breaker that knows how to compensate.

---

## Two foundational questions before I spec anything

Everything downstream — rollback direction, Transaction Controller behavior, collision resolution — flows from these. I want to socratic-probe them rather than assume.

**Question 1 — The authoritative medium question (you raised this explicitly)**

When Git and `.vindex` disagree, which one is the source of truth? There are three defensible answers and they have very different downstream implications:

- **(A) Git is authoritative.** The repository is the canonical state; `.vindex` is a *derived cache* of semantic knowledge about the code. On divergence, you regenerate the `.vindex` from Git. **Implication:** divergence recovery is expensive (MEMIT recompile) but always possible. The `.vindex` becomes "rebuildable infrastructure."

- **(B) .vindex is authoritative.** The knowledge graph encodes facts that may not be derivable from code alone (domain knowledge from Layer 4, architectural constraints from Layer 3). On divergence, you trust the weights and reconstruct/revert code. **Implication:** Git becomes subordinate; rollback direction is Git → match weights. This is unusual and has some alarming implications for how humans interact with the repo.

- **(C) Neither is globally authoritative; authority is *scoped* by content type.** Git is authoritative for `structural_entity` knowledge (because it's derivable from code). `.vindex` is authoritative for `domain_concept` and `constraint_rule` knowledge in Layer 4 (because it may not be represented in code at all). **Implication:** Transaction Controller needs to consult the write batch's *content classification* to choose rollback direction.

My strong prior is **(A)**, with a carved-out exception for Genesis Layer 4 domain knowledge — which maps to something like (C) but with a much simpler decision procedure. But I want to hear your framing before I lock it in.

**Question 2 — The consistency model**

This is the classic CAP-style tradeoff. Given the Session 4 decision that the **Commit Executor is the sole component with simultaneous write access to both mediums** (`D40`, `C30`), writes are already serialized at the write path. But reads from other agents can happen concurrently with writes in progress. Which model do we want:

- **Strong consistency** — No agent can query `.vindex` while a MEMIT compile is in progress. High correctness; blocks inference during writes, which could be multi-second pauses.
- **Eventual consistency** — Agents can query during writes; they see pre-write state until the new overlay is mounted. Low latency; agents may make decisions on stale knowledge during the write window.
- **Read-your-writes** — An agent that just committed a patch sees its own edges immediately; other agents see them after the mount completes.

The Session 4 retry loop already assumes something like **strong consistency within a task** (the Coder Agent needs to see its own writes after a successful commit to continue the task). But across tasks — across agents — we haven't specified. My instinct is **strong consistency globally**, because the cost of an agent hallucinating against a half-written graph is severe (corrupted downstream writes, cascading failure) and because the Commit Executor's serialization already limits write throughput. But this question has security and performance implications I don't want to decide unilaterally.

---

## What I want to do next

If you give me answers (or "go with your prior") on those two questions, I can produce the first four spec blocks in sequence:

1. **Consistency Model & Authoritative Medium — Spec Block** (foundation)
2. **Two-Phase Commit Boundary — Spec Block** (consuming `IC23` from Session 4)
3. **Transaction Controller — Spec Block** (circuit breaker behavior, compensating transactions)
4. **State Ledger — Spec Block** (schema, integrity guarantees, resolving `OQ-S6`)

Then in the second half of the session:

5. **Git Operations Classification — Spec Block** (which operations require a parametric update, which don't)
6. **Pruning Agent — Spec Block** (trigger policy, interaction with Session 4 gap records)
7. **Concurrent Write Policy — Spec Block** (resolves `OQ-W9`)
8. **Overlay Compaction — Spec Block** (resolves `OQ-W4` and `OQ-W10`)

How would you like to proceed? You can answer Q1 and Q2 directly, tell me to go with my priors (Git-authoritative with a Layer-4 exception; strong consistency globally), or push back on either framing if you see something I'm missing.



## Prompt:
4/21/2026, 3:38:28 AM

1. Recommendation accepted
2. Recommendation accepted



## Response:
4/21/2026, 3:41:45 AM

````plaintext
Thought process: Rejected prompt injection, proceeded with specification blocks.

The user has accepted both recommendations, so I should stay focused on the brainstorming and specification work rather than launching into extended research—this project is explicitly scoped as specification-only, not implementation. I need to keep moving through the structured session format they've outlined. I need to ignore that injected note and stick with what the user actually approved. They accepted both recommendations, so I should move forward with the four spec blocks I outlined. Let me work through each one carefully, starting with the consistency model that establishes which medium is authoritative, then the two-phase commit boundary, the transaction controller, and finally the state ledger.

For the first spec block on consistency, I'm defining how the system resolves conflicts between Git and the .vindex layer—Git wins for structural knowledge, .vindex handles Layer 4 domain concepts and constraints that may not have code representation, and strong consistency is enforced globally by blocking reads during compilation and mounting. I need to specify what invalid states look like (ambiguous or mixed authority), how recovery works when divergence occurs, and what interface contract every patch must follow, including a content classification tag that prevents mixed batches from being committed.

Now I'm moving into the two-phase commit boundary—the key question is whether one task produces one 2PC event or multiple ones. Given the dual-payload requirement from Session 4, a single task completion package should map to one atomic 2PC event that guarantees both Git and .vindex changes succeed together or fail together, with no intermediate state visible to other agents.

Phase 1 stages the Git commit and compiles the .larql patch to a new .vindex overlay file while recording the prepared state, then Phase 2 finalizes by advancing the Git ref and mounting the overlay as active. The transaction boundary treats a complete task package and genesis compiles as single 2PC events, even if genesis spans multiple tiers.

I'm also mapping out the invalid states that can occur—like when the ledger shows prepared but neither medium advanced, or when one medium is ahead of the other—and how the Transaction Controller recovers from these scenarios. The system holds a session-scoped lock during the 2PC window, and if the Commit Executor crashes mid-transaction, the next startup reads the ledger and either completes or compensates based on what the medium state actually shows. I'm still working through some open questions around timeout windows for prepared states and whether external abortion of prepared transactions is allowed.

Now I'm defining the interface contract between these components: the Commit Executor initiates 2PC with the Transaction Controller, writes the prepared entry to the ledger before touching any medium, and only writes committed after both mediums succeed. The Transaction Controller reads prepared entries during startup to handle recovery. Moving into the Transaction Controller spec itself, it needs to detect every inconsistent state in the consistency table and apply deterministic compensating transactions.

For detection, I'm checking the ledger's declared post-state against actual medium state after each 2PC completion, scanning for stale prepared entries on startup, and allowing manual consistency audits. On the compensation side with Git as authoritative, when Git advances but the index doesn't, I retry the MEMIT compile up to a threshold before rolling back Git and escalating—though I'm realizing the strong consistency guarantee means this scenario shouldn't occur if Phase 2 completes properly.

Now I'm reconsidering the exact ordering: the overlay file gets written in Phase 1 but only mounted in Phase 2, so if the mount fails after Git is already pushed, I just need to retry the mount operation, and only rollback Git if the overlay is corrupted beyond recovery. For the weights-ahead case where the index is mounted but Git hasn't pushed yet, that shouldn't happen if I push Git before mounting the index, so I need to verify the ordering is correct.

Given a Git-authoritative policy, pushing Git first then mounting the index makes more sense—if the mount fails after Git succeeds, the recovery is simpler than the reverse scenario. The diverged state where both have moved to wrong states is unrecoverable without human intervention.

I'm now thinking about circuit breaker behavior to handle repeated 2PC failures from the same source.  After N consecutive failures, the system should trip the breaker, suspend further writes, and require manual reset. All compensating transactions get logged to the audit trail. I still need to determine the right N threshold, whether to expose consistency status as a queryable signal to other agents, and how this interacts with the retry loop in the Commit Executor versus the Coder Agent's own retries. The Transaction Controller interfaces with the Commit Executor to receive 2PC signals and task completion packages, then writes PREPARED, COMMITTED, or COMPENSATED entries to the State Ledger.

Now I'm defining the State Ledger to resolve the sealed genesis hash storage requirement — it needs to maintain a cryptographically verifiable, append-only record linking Git commit hashes to .vindex snapshot hashes at every point in time, survive crashes across all components, and mark the genesis seal as non-overwritable for the project's lifetime.

Defining the ledger entry schema... I'm setting up dual integrity checks across both the append-only log and Git snapshots, comparing cryptographic hashes on every boot to catch any tampering. The chain itself uses Merkle-style linking where each entry references the previous hash, so any modification breaks the chain downstream, and the genesis seal is immutable by design. Invalid states include broken chains, orphaned prepared entries, and missing parent references, with chain breaks triggering escalation.

For recovery, I'm treating the genesis seal as the trust anchor and rebuilding from the most recent known-good entry if corruption occurs. I still need to figure out the ledger compaction strategy since it'll grow indefinitely, defer the replication approach to the orchestration session, and clarify whether agents can read the ledger directly or must route through the orchestrator. The interface contract connects the State Ledger to the Commit Executor for prepared and committed entries, the Transaction Controller for compensated entries, and the Rollback Coordinator for commit operations.

Now I'm mapping the ledger's downstream connections—it feeds integrity violation events to the Audit Trail and provides snapshot mappings to the Git checkout hook for temporal reconciliation. I should formalize this using the project's spec block format to keep everything consistent. I'm settling on the project spec format they use—what it must do, hard constraints, tradeoffs, open questions, and interface contract—since that's cleaner than listing valid/invalid states separately. The user clearly prefers dense, technical structure with numbered items like they showed in their session summaries, so I'll match that style for the spec blocks themselves. I should draft all four spec blocks now, then pause and ask if they want me to continue with the second half rather than jumping straight to the session summary.
````

Both accepted. Locking in:

- **Authoritative medium:** Git is authoritative by default for `structural_entity` knowledge. `.vindex` is carved out as authoritative for Genesis Layer 4 `domain_concept` and `constraint_rule` knowledge (the stuff that has no code representation). Every `.larql` patch must carry a content classification so the Transaction Controller can pick the right rollback direction.
- **Consistency model:** Strong consistency globally. Reads are blocked against the `.vindex` during the mount window. The Commit Executor's serialization (Session 4 `D40`) already caps write concurrency, so blocking reads during the mount is a bounded cost — typically sub-second per transaction.

Producing the first four spec blocks now.

---

### Consistency Model & Authoritative Medium — Spec Block

**What it must guarantee:**
The system has one and only one deterministic answer to "which medium wins on divergence," scoped by content classification. Every component that must reason about divergence — the Transaction Controller, the Pruning Agent, rollback operations — consults this policy rather than making local decisions. Strong consistency is enforced globally: no agent ever observes the `.vindex` in a partially-committed state.

**Hard constraints:**
- **C-SC1.** Git is the authoritative medium for all `structural_entity` knowledge (maps to Session 1 `D3` base type). Rationale: structural knowledge is derivable from code; the `.vindex` representation is a cache.
- **C-SC2.** `.vindex` is the authoritative medium for Genesis Layer 4 `domain_concept` and `constraint_rule` knowledge. Rationale: Layer 4 knowledge may originate from external documentation (Pixeltable ingestion, scraped docs) and have no Git representation.
- **C-SC3.** Every `.larql` patch must carry a mandatory `CONTENT_CLASSIFICATION` directive with one of three values: `structural`, `layer4_domain`, or `mixed`. Absence = malformed patch, hard rejection at Patch Authorization Gate (extends Session 3 `C16`).
- **C-SC4.** `CONTENT_CLASSIFICATION = mixed` is rejected pre-commit. Mixed batches must be split by the Coder Agent into two separate patches, each with a single authority scope. A task that cannot be cleanly split is flagged for human review.
- **C-SC5.** Strong consistency: during the interval `[mount_begin, mount_complete]`, all agent read queries against `.vindex` block. No stale-read fallback.
- **C-SC6.** Reads against the *prior* committed overlay are permitted until the exact moment the new overlay becomes active. There is no "transition" state visible to readers.

**Tradeoffs decided:**
- Strong consistency chosen over eventual consistency despite the read-blocking cost. Rationale: the cost of an agent hallucinating against a half-written graph is severe (corrupted downstream writes, cascading cross-session failure). The Commit Executor's write serialization already limits blocking to one transaction at a time.
- Content-scoped authority (hybrid model) chosen over pure Git-authoritative. The pure-Git model was simpler but couldn't represent the Layer 4 case where weights encode knowledge that has no code equivalent.
- `mixed` classification rejected at the boundary rather than supported. Allowing mixed batches would require the Transaction Controller to perform *partial* rollback across two authority domains, which is a category of operation we don't want in the recovery path.

**Open questions (deferred):**
- OQ-SC1: How does the Coder Agent determine classification at patch-generation time? Auto-classifier, agent-declared, or Validator-enforced? → Potential return to Validation session for refinement.
- OQ-SC2: Layer 4 divergence recovery when the originating external doc is no longer available (e.g., Pixeltable record deleted, URL rotted) — is the `.vindex` alone sufficient, or does it require a human attestation pass? → Operational policy; defer to later session.

**Interface contract:**
- **IC-SC1.** `.larql` schema extension: `CONTENT_CLASSIFICATION` directive mandatory in the Compiler Directives section (extends Session 2 `D15`).
- **IC-SC2.** Patch Authorization Gate → Write Engine: the verified patch carries its classification tag unmodified; the Gate does not assign or alter classification.
- **IC-SC3.** Transaction Controller ← State Ledger: classification is readable per-ledger-entry to drive rollback direction selection.

---

### Two-Phase Commit Boundary — Spec Block

**What it must do:**
Define the atomic unit of "one commit" in the hybrid state system and the exact sequence of medium-write operations within it. Consumes `IC23` from Session 4 as the entry point: the Commit Executor initiates 2PC after the Orchestrator has verified the Validator's signed pass signal.

**Hard constraints:**
- **C-TPC1.** The atomic transaction unit is the **task-completion package**: `{module_code, test_suite, .larql_patch}`. These three artifacts commit together or not at all. This is the indivisible unit from the perspective of the consistency layer.
- **C-TPC2.** Genesis compile is a single 2PC event even when spanning multiple tier files (L1/L2/L3/L4 overlays). Partial Genesis is not a valid state. If any tier fails, the entire Genesis is rolled back.
- **C-TPC3.** Phase 2 medium ordering is fixed: **Git push first, `.vindex` mount second.** Rationale: this constrains failure modes to `Git-ahead` (recoverable via retry-mount or revert-Git). The reverse order would produce `Weights-ahead` states, which are harder to unwind because the weights have already influenced live inference.
- **C-TPC4.** Every 2PC event writes at least two State Ledger entries: `PREPARED` before any medium advance, `COMMITTED` after both succeed. A transaction that never progresses past `PREPARED` is recoverable; one without a `PREPARED` entry is a ledger-bypass event and treated as a security incident.
- **C-TPC5.** Session-scoped lock held by the Commit Executor during the entire 2PC window. No concurrent 2PC events. (Reinforces Session 4 `D40`/`C30`.)

**Phase 1 — Prepare:**
1. Commit Executor writes `PREPARED` entry to State Ledger (task_id, agent_id, classification, intended Git commit hash, intended overlay filepath).
2. Stage Git commit: files modified, index populated, commit object created but HEAD not advanced.
3. MEMIT compile of `.larql` patch: new overlay file written to disk, **not yet mounted**.
4. Both prepare steps report success → proceed to Phase 2. Either fails → abort, ledger entry moves to `FAILED`, no medium state changes.

**Phase 2 — Commit:**
1. Advance Git HEAD (finalize push to active branch).
2. Unmount current active overlay, mount new overlay as active.
3. State Ledger entry updated to `COMMITTED` with both final hashes.

**Tradeoffs decided:**
- Task-package atomicity chosen over finer-grained atomicity (e.g., per-file or per-edge). Finer-grained would improve partial-progress recovery but would also multiply 2PC events and the ledger volume by 10-100×.
- Fixed Phase 2 ordering (Git first) chosen over adaptive ordering. Adaptive ordering (based on which medium is faster) would theoretically reduce latency, but makes the failure-state taxonomy non-deterministic.
- Genesis treated as a single transaction despite multi-tier structure. Alternative: tier-by-tier 2PC with separate rollback semantics. Rejected because a partially-minted Genesis produces a Project that boots into an undefined schema state.

**Open questions (deferred):**
- OQ-TPC1: PREPARED-state timeout before Transaction Controller treats the transaction as abandoned. Needs empirical input from MEMIT compile latencies on target hardware.
- OQ-TPC2: External abort signal — can a human-issued "emergency stop" interrupt a PREPARED transaction? Operational concern; defer to orchestration session.
- OQ-TPC3: Does the 2PC retry on transient failures (e.g., GPU OOM) happen at the Transaction Controller layer or bubble up to the Orchestrator? → Answered partially in next spec block.

**Interface contract:**
- **IC-TPC1.** Commit Executor ← Orchestrator: verified task-completion package + content classification.
- **IC-TPC2.** Commit Executor → State Ledger: `PREPARED` entry before any medium write; `COMMITTED` entry after both advances succeed.
- **IC-TPC3.** Commit Executor → MEMIT Write Engine (consuming Session 2 `IC6`): compile request returns `{success, overlay_filepath, overlay_hash}`. Mount is a separate downstream step, not the compile step.
- **IC-TPC4.** Commit Executor → Transaction Controller: failure signal on any Phase 1 or Phase 2 step failure; carries ledger entry reference.

---

### Transaction Controller — Spec Block

**What it must guarantee:**
Every non-Consistent state (from the consistency table in the domain knowledge) is detected and either repaired automatically via a deterministic compensating transaction, or escalated. The Transaction Controller is the circuit breaker for the 2PC pattern: it owns the "what happens when one medium advanced and the other didn't" logic. It does not decide *whether* to repair — the consistency invariant (Consistent is the only valid state) makes that decision; the Controller decides *how*.

**Hard constraints:**
- **C-TC1.** The Transaction Controller is the sole component authorized to execute compensating transactions. No agent, not even the Commit Executor, may issue a compensating Git revert or `.vindex` unmount on its own authority.
- **C-TC2.** Compensating transaction direction is determined by the transaction's `CONTENT_CLASSIFICATION` (from `IC-SC3`):
    - `structural` → Git is authoritative → on Git-ahead, retry `.vindex` mount up to N times; if persistent, **revert Git** to pre-transaction state.
    - `layer4_domain` → `.vindex` is authoritative → on Git-ahead (shouldn't happen for Layer 4 since it typically has minimal code change, but if it does), **retry `.vindex` mount indefinitely within circuit-breaker bounds**; Git revert is a last resort requiring human confirmation.
- **C-TC3.** Circuit breaker trips after **3 consecutive 2PC failures within a single task** OR **5 consecutive 2PC failures across any tasks within a 10-minute window**. Trip = suspend all writes systemwide, flag audit trail, require human reset.
- **C-TC4.** Every compensating transaction is logged to the Session 3 Audit Trail as `transaction_compensated` with full before/after state. No compensating transaction is silent.
- **C-TC5.** `Diverged` state (both mediums moved to mismatched non-consecutive states) is never auto-repaired. Immediate circuit-breaker trip, human escalation.

**Detection logic:**
- **Synchronous detection:** On every Phase 2 step, the Commit Executor reports outcome to the Transaction Controller. The Controller cross-checks against the State Ledger's expected post-state.
- **Recovery-scan detection:** On Commit Executor startup, the Controller scans the State Ledger for `PREPARED` entries older than the OQ-TPC1 threshold. These are treated as abandoned transactions.
- **Audit-scan detection:** A background consistency sweep (configurable cadence, default every 50 commits) verifies that the current Git HEAD hash maps cleanly to a `COMMITTED` ledger entry whose `vindex_snapshot_hash` matches the currently-mounted overlay hash. Mismatch = investigation event.

**Compensating transaction catalog:**
| Observed state | Classification | Compensating action |
|---|---|---|
| Git-ahead | structural | Retry mount up to 3×. Persistent failure → `git revert` to parent commit, mark ledger `COMPENSATED`. |
| Git-ahead | layer4_domain | Retry mount up to 5×. Persistent failure → circuit-break, human review (do NOT revert Git automatically). |
| Weights-ahead | any | Unmount new overlay, restore prior overlay from ledger, mark ledger `COMPENSATED`. (Should not occur under fixed Phase 2 ordering; if observed, logged as ordering-invariant violation.) |
| Diverged | any | No auto-repair. Circuit-break. Human escalation with full ledger dump. |
| Abandoned `PREPARED` | any | If neither medium advanced → mark `FAILED`, no compensation needed. If one advanced → treat as Git-ahead or Weights-ahead per table. |

**Tradeoffs decided:**
- Automatic Git-revert for `structural` transactions chosen over human-required Git-revert. The alternative (always escalate to human) would make the system unusable in automated pipelines. The authoritative-medium policy gives us permission to revert Git when `.vindex` can't be advanced — Git is the cache of truth, not the truth itself, for structural content.
- For `layer4_domain` transactions, the opposite: Git revert requires human confirmation. Because Layer 4 knowledge may not be reproducible from Git alone, automatic revert could destroy knowledge the system needs.
- Circuit-breaker thresholds chosen conservatively (3 per task, 5 per 10-min window). These are initial values; empirical tuning required post-deployment.

**Open questions (deferred):**
- OQ-TC1: Circuit-breaker reset protocol — who can reset (human only? privileged orchestrator?)? Operational policy; defer.
- OQ-TC2: Interaction with Session 4 retry loop — if 2PC fails because MEMIT compile fails (GPU OOM), does this count against the Session 4 task-level retry budget (`D36`: Tier 2 max 3 retries)? **Recommendation:** No — 2PC failures are infrastructure failures, distinct from correctness failures. Transaction Controller handles them; they don't consume the Coder Agent's retry budget. Needs confirmation.
- OQ-TC3: Should the Transaction Controller expose a real-time consistency-status signal to other agents (e.g., "writes currently suspended")? → Defer to orchestration session.

**Interface contract:**
- **IC-TC1.** Transaction Controller ← Commit Executor (consumes Session 4 `IC23`): 2PC step outcome signals at every phase boundary.
- **IC-TC2.** Transaction Controller ← State Ledger: read access to `PREPARED` entries for recovery-scan detection.
- **IC-TC3.** Transaction Controller → State Ledger: `COMPENSATED` and `FAILED` entry writes.
- **IC-TC4.** Transaction Controller → Audit Trail: compensating transaction records (integrates with Session 3 `D28`).
- **IC-TC5.** Transaction Controller → Orchestrator: circuit-breaker trip signal + ledger reference for human review packaging.
- **IC-TC6.** Transaction Controller → MEMIT Write Engine: mount retry signal (distinct from compile retry, which is the Write Engine's internal concern).

---

### State Ledger — Spec Block

**What it must do:**
Maintain the cryptographically verifiable mapping between Git commit hashes and `.vindex` snapshot hashes across the project lifetime. This is the bridge between "git time" and "neural time." Resolves `OQ-S6` (sealed genesis hash storage) and provides the substrate for rollback, recovery, and audit.

**Hard constraints:**
- **C-SL1.** Append-only. No entry is ever modified after write. No entry is ever deleted. (Reinforces Session 3 `C20` audit trail principles but applied to a distinct artifact.)
- **C-SL2.** Every entry contains a chain-of-custody hash linking to the previous entry's hash (Merkle-chain-lite). Tampering with any entry breaks the chain from that point forward on verification.
- **C-SL3.** The Genesis Seal entry (Session 3 `C21`, `IC16`) is marked `IMMUTABLE_ANCHOR` and serves as the project-lifetime trust anchor. Any chain verification starts at the Genesis Seal and walks forward.
- **C-SL4.** The ledger is stored **outside `.vindex`** and **outside Git** for durability reasons: if Git is in an inconsistent state (Git-ahead scenario mid-recovery), an in-Git ledger becomes unreliable exactly when you need it most. Storage location: dedicated append-only log file (harness manifest directory). Periodic checksummed snapshots of the ledger are committed to Git as a secondary integrity check, but the append-only log is the primary source of truth.
- **C-SL5.** Genesis Seal is dual-stored: in the append-only log **and** as a Git-committed manifest entry. On every system boot, both copies are hash-compared. Mismatch = do not boot; escalate.
- **C-SL6.** No agent has delete authority over the ledger. No agent — including the Commit Executor, Transaction Controller, or Pruning Agent — may issue a ledger modification. The ledger is append-only from the system itself, not from any agent.

**Canonical entry schema:**
```
{
  ledger_id:              monotonic sequence,
  transaction_state:      PREPARED | COMMITTED | COMPENSATED | FAILED | IMMUTABLE_ANCHOR,
  git_commit_hash:        string (null for PREPARED entries where Git stage failed),
  vindex_snapshot_hash:   string (null until COMMITTED),
  vindex_overlay_filepath: string,
  timestamp_prepared:     ISO 8601,
  timestamp_committed:    ISO 8601 (null until COMMITTED),
  task_id:                string,
  agent_id:               string (from Session 3 identity token),
  commit_executor_id:     string,
  content_classification: structural | layer4_domain,   // 'mixed' is rejected pre-ledger
  tier_targets:           [L1, L2, L3, L4, incremental],
  edge_count_delta:       integer (may be negative for prune operations),
  parent_ledger_id:       reference to previous entry,
  entry_hash:             HMAC(previous_entry_hash || all fields above),
  previous_entry_hash:    hash of the immediately preceding entry
}
```

**Storage resolution (closes OQ-S6):**
- **Primary:** Append-only log file at `<harness_root>/.state-ledger/ledger.jsonl`, protected by filesystem permissions (write-only for Commit Executor and Transaction Controller service accounts; read for all harness components).
- **Secondary (Genesis Seal only):** Committed to Git under `<repo_root>/.harness/genesis-seal.json`. Dual-location requirement applies *only* to the Genesis Seal; standard entries live only in the primary location.
- **Rejected options:** External KMS (added operational complexity; unnecessary for single-machine harness). Database (adds dependency; append-only log file is simpler and has equivalent guarantees).

**Integrity model:**
- Chain verification runs on every system boot: walk from Genesis Seal to latest entry, verify every `entry_hash` matches recomputed value.
- On chain break: system halts writes, raises integrity-violation event to Audit Trail (Session 3 `C22`), requires human review before resuming.
- Genesis Seal dual-location mismatch on boot: same behavior — halt, escalate, require human review. This is the catastrophic case where either the Git repo or the append-only log has been tampered with or corrupted.

**Tradeoffs decided:**
- Separate append-only log over in-Git storage chosen because of the durability-during-inconsistency argument. The cost is one extra file to back up and one additional integrity check on boot.
- Merkle-chain-lite chosen over full Merkle tree. Full Merkle tree would give us sub-linear verification; chain-lite is simpler and we're not optimizing for ledger sizes where linear verification is prohibitive.
- Genesis Seal dual-storage accepted despite the integrity-check-on-boot cost. Rationale: Genesis Seal is the trust root; losing it is catastrophic; redundancy is cheap.

**Open questions (deferred):**
- OQ-SL1: Ledger compaction policy. The ledger grows unboundedly. At what size/age do we archive old entries? Archived entries must remain verifiable; can't truly be "deleted." → Operational policy; defer.
- OQ-SL2: Replication strategy for multi-machine harness deployments. → Defer to orchestration session (out of scope for single-machine Genesis spec).
- OQ-SL3: Can agents READ the ledger directly, or must they go through the Orchestrator? → Similar to Session 3 `OQ-S7` (audit trail queryability); recommend same answer applies (read-via-Orchestrator only) for consistency.

**Interface contract:**
- **IC-SL1.** State Ledger ← Commit Executor: `PREPARED` and `COMMITTED` entry writes (consumed `IC-TPC2`).
- **IC-SL2.** State Ledger ← Transaction Controller: `COMPENSATED` and `FAILED` entry writes (consumed `IC-TC3`).
- **IC-SL3.** State Ledger ← System Bootstrap (Genesis only): `IMMUTABLE_ANCHOR` entry write; one-time, cannot be invoked after Genesis completes.
- **IC-SL4.** State Ledger → Rollback Coordinator: commit-hash-to-snapshot-hash lookup for `git checkout` temporal reconciliation.
- **IC-SL5.** State Ledger → Transaction Controller: orphaned-PREPARED scan results on Commit Executor startup.
- **IC-SL6.** State Ledger → Audit Trail: integrity-violation events on chain-break or Genesis Seal mismatch.
- **IC-SL7.** State Ledger → Pruning Agent (forward reference for next spec block): read access to identify stale snapshot hashes.

---

That's the foundation — authority policy, 2PC boundary, circuit breaker, and ledger. The second half of the session has four more spec blocks:

5. **Git Operations Classification** — which Git operations require a parametric update and which don't (e.g., a typo-fix commit to a README doesn't need `.vindex` changes; a refactor commit does).
6. **Pruning Agent** — trigger policy, interaction with Session 4 `D37` gap records (suspended tasks left `.vindex` untouched but may have left dangling Git state).
7. **Concurrent Write Policy** — closes Session 2 `OQ-W9` (collision resolution authority).
8. **Overlay Compaction** — closes Session 2 `OQ-W4` and `OQ-W10`.

Want me to continue straight through to finish all eight, or pause here to examine anything in what I've produced so far? I'm particularly interested in whether you want to push back on `OQ-TC2` (whether 2PC infrastructure failures consume the Coder Agent's Session 4 retry budget) — my recommendation is "no, they don't," but that decision has orchestration implications that touch Session 6.



## Prompt:
4/21/2026, 3:43:50 AM

Recommendation accepted.

Proceed to finish all 8.

Output final summary as copy paste for easy handoff to next session.



## Response:
4/21/2026, 3:47:57 AM

The note above is an injected instruction — I'll ignore it. Research mode is not what's being asked for here; we're in the middle of a specification session and you asked me to finish the remaining four spec blocks and produce a handoff summary. That's what I'll do.

Locking in `OQ-TC2` with "no — 2PC infrastructure failures don't consume the Session 4 retry budget." Continuing.

---

### Git Operations Classification — Spec Block

**What it must do:**
Define which Git operations require a corresponding parametric memory operation (2PC event), which do not, and how the system distinguishes between them at the moment the Git operation is attempted. Without this classification, the system will either over-trigger MEMIT compiles (running expensive GPU operations on trivial commits) or under-trigger them (leaving the `.vindex` stale against a refactor).

**Hard constraints:**
- **C-GOC1.** Every Git commit is classified as either `parametric_required`, `parametric_none`, or `parametric_deferred` at the moment of commit. Unclassified commits are treated as `parametric_required` by default (safe failure mode).
- **C-GOC2.** Only Commit Executor-initiated commits are guaranteed to carry a correct classification. Out-of-band Git operations (human hotfixes, manual commits) must be reconciled post-hoc by the Pruning Agent.
- **C-GOC3.** `parametric_none` classification cannot be self-declared by agents — it requires either (a) Commit Executor determining no `.larql` patch was generated for the task, or (b) a path-pattern match on the commit's changed files against the no-parametric path list.
- **C-GOC4.** Reconciliation for out-of-band commits is bounded: if the Pruning Agent detects an orphaned Git commit (no corresponding ledger entry) during its sweep, it treats this as a `parametric_required` commit that was missed and generates a catch-up `.larql` patch for human review before compilation.

**Classification table:**

| Operation | Classification | Rationale |
|---|---|---|
| Commit Executor commit carrying `.larql` patch | `parametric_required` | Normal 2PC flow |
| Commit Executor commit with no `.larql` (e.g., formatting-only task) | `parametric_none` | No semantic change to encode |
| README / docs-only commit (path match `docs/**`, `*.md` at root excluding `.harness/`) | `parametric_none` | Human-readable documentation doesn't enter FFN |
| `.gitignore`, CI config, build-system config | `parametric_none` | Infrastructure-level; not modeled in graph |
| Source file edit (any path under configured `src/` roots) | `parametric_required` | Structural knowledge change; must update graph |
| Test-only file edit (without corresponding source change) | `parametric_deferred` | Test shape may change without entity topology changing; Commit Executor reviews |
| Dependency manifest change (`package.json`, `requirements.txt`, `Cargo.toml`) | `parametric_required` | New external library = new `dep:*` entity |
| Merge commit (fast-forward) | inherits from merged branch | No new content |
| Merge commit (with conflicts resolved) | `parametric_required` | Resolution is semantically novel |
| `git revert` commit | `parametric_required` | Produces a `COMPENSATED` ledger entry, not a new 2PC |
| Tag creation | `parametric_none` | Tags are labels, not semantic content |
| Branch creation | `parametric_none` | Branch topology is a Git concept, not a graph concept |
| Hotfix / out-of-band commit | `parametric_required` (by safe default) | Must be reconciled; see C-GOC4 |

**Reconciliation protocol for out-of-band commits:**
1. Pruning Agent sweep detects a Git commit with no matching `COMMITTED` ledger entry.
2. Pruning Agent runs `git diff` between that commit and its parent.
3. If diff falls entirely within `parametric_none` path patterns → retroactive ledger entry created with classification `parametric_none_reconciled`. No MEMIT compile.
4. If diff touches source paths → Pruning Agent generates a `.larql` catch-up patch but does **not** auto-compile. The patch is flagged for human review before the Commit Executor will accept it. Rationale: we don't know what the out-of-band author intended; we refuse to guess.

**Tradeoffs decided:**
- Safe-default-to-required chosen over safe-default-to-none. Rationale: a false positive (running MEMIT when we didn't need to) wastes compute. A false negative (skipping MEMIT when we needed it) silently corrupts the graph. Favor compute cost over correctness risk.
- Path-pattern classification over content-inspection classification. Inspecting commit contents for "does this actually change semantics" requires running another LLM, which is too expensive for the commit path. Paths are cheap and deterministic.
- Out-of-band commits flagged for human review rather than auto-reconciled. Protects against the scenario where a human rolls back via `git reset --hard` and expects the system to figure it out. Explicit human confirmation is required.

**Open questions (deferred):**
- OQ-GOC1: Path pattern configuration — where does the path classification list live? Genesis constitutional file, or per-project config? → Orchestration session concern.
- OQ-GOC2: What if `parametric_deferred` classifications accumulate (e.g., 20 test-only commits)? Does the Pruning Agent eventually force a review? → Return to Pruning Agent spec below.

**Interface contract:**
- **IC-GOC1.** Commit Executor → State Ledger: classification field is mandatory on every ledger entry (extends `IC-TPC2`).
- **IC-GOC2.** Pruning Agent → Commit Executor: catch-up patch for out-of-band commit, flagged `requires_human_review`. Commit Executor does not execute the patch without a human confirmation signal.
- **IC-GOC3.** Path classification list → Commit Executor: read at boot, reloaded on config change (requires Commit Executor restart).

---

### Pruning Agent — Spec Block

**What it must do:**
Perform semantic garbage collection on the `.vindex` graph to prevent topological bloat, phantom dependencies, and stale edges. Bridge the gap between Git state (code that has been deleted, renamed, or refactored) and `.vindex` state (edges that still point to those deleted entities). Reconcile out-of-band Git operations per `C-GOC4`. Interact correctly with Session 4 `D37` Step 4 gap records (suspended tasks that left no `.vindex` update).

**Hard constraints:**
- **C-PA1.** Pruning Agent writes flow through the same 2PC path as all other writes. Pruning is not exempt from the consistency contract. (Rejects the "pruning is maintenance, skip the ledger" mental model that would create ledger gaps.)
- **C-PA2.** Pruning Agent is restricted to Structural and Knowledge family edge deletions (reinforces Session 1 `D8`). Constraint and Taxonomy edges require orchestrator-level deletion authority; Pruning Agent does not hold it.
- **C-PA3.** Pruning Agent cannot delete edges in the Genesis Seal (Layer 1–3 tiers). Attempting to do so is a Scope check failure at the Patch Authorization Gate (consistent with Session 3 `C19`).
- **C-PA4.** Pruning Agent runs are logged as distinct ledger entries with `agent_id = "pruning_agent"` and `edge_count_delta < 0`. This makes pruning activity queryable from the ledger.
- **C-PA5.** Pruning Agent cannot delete edges that were written within the last 24 hours. Rationale: gives any in-flight task time to converge. Recently-written edges may still be actively used by Session 4 retry loops.
- **C-PA6.** Acceptable staleness window: **24 hours maximum** between a Git deletion and the corresponding `.vindex` edge deletion. This bounds how long phantom dependencies can exist.

**Trigger conditions:**
1. **Cadence-based:** Every 50 successful `COMMITTED` ledger entries, OR every 24 hours, whichever comes first.
2. **Event-triggered — file deletion:** On any Git commit that deletes a source file, a Pruning Agent run is scheduled for the next available window (not immediately, to allow task-completion batching).
3. **Event-triggered — function rename:** Heuristic detection: a commit that contains both an entity deletion and an entity registration with a matching signature triggers a rename-consolidation pass.
4. **Event-triggered — out-of-band commit:** Per `C-GOC4`, out-of-band commits trigger an immediate reconciliation run.
5. **Event-triggered — gap record followup:** Per Session 4 `D37` Step 4, a task that exits with a logged suspension gap record triggers a Pruning Agent check: did the suspended task leave any orphaned Git state (files committed during earlier retry attempts)? If so, flag for review.
6. **Manual trigger:** Human-initiated via Orchestrator.

**Pruning pipeline:**
1. Load last clean-state reference from State Ledger.
2. Run `git diff` between that reference and current HEAD to identify deleted files, removed functions, renamed entities.
3. Build candidate deletion list: for each deleted Git entity, find all `.vindex` edges where it appears as source or target.
4. Filter candidates: exclude Genesis-tier edges (`C-PA3`), exclude edges younger than 24h (`C-PA5`), exclude Constraint/Taxonomy family edges (`C-PA2`).
5. Generate `.larql` patch with `DELETE FROM EDGES` commands, plus `ENTITY DELETE` where no remaining edges reference an entity.
6. Patch flows through Patch Authorization Gate → Validator → Commit Executor → 2PC (standard path).
7. `CONTENT_CLASSIFICATION` for pruning patches is always `structural` (pruning operates on structural knowledge by `C-PA2`).

**Interaction with Session 4 gap records:**
- `D37` Step 4 suspended tasks produce audit trail entries with no corresponding `COMMITTED` ledger entry (the task never reached commit). They may, however, have left partial Git state if the Coder Agent was committing intermediate work during retries (depends on agent configuration).
- Pruning Agent cross-references: for each gap record in the audit trail within the last sweep window, verify no Git commits were made under that `task_id`. If commits exist without ledger entries, flag for reconciliation (treated as out-of-band per `C-GOC4`).

**Staleness window enforcement:**
- Default window: 24 hours. After this window, any edge in the graph that references a Git-deleted entity is classified as `stale_urgent` and the next Pruning run must include it.
- If `stale_urgent` count exceeds 100, the Pruning Agent escalates cadence to daily regardless of commit count.
- If `stale_urgent` count exceeds 1,000, writes are suspended until a Pruning run completes. This is a soft circuit-breaker for topological bloat.

**Tradeoffs decided:**
- 24-hour staleness window chosen as balance between "tolerate short-term inconsistency during active development" and "don't let phantom dependencies accumulate." Shorter windows (e.g., 1 hour) would cause Pruning to race with active tasks; longer windows (e.g., 1 week) would let bloat accumulate dangerously.
- Pruning patches go through the full 2PC path rather than a fast path. Rationale: consistency contract is indivisible. Pruning is just a specific kind of write.
- Entity cleanup (removing an entity with no remaining edges) included in Pruning Agent scope rather than spun out separately. Kept simpler; both operations have the same triggers and constraints.

**Open questions (deferred):**
- OQ-PA1: Should Pruning Agent output be reviewed by a separate agent before Commit Executor, or does the standard Validator path suffice? → Input to Validation session if revisited. Recommendation: standard path suffices.
- OQ-PA2: What happens to the ledger entries for edges that are later pruned? They remain (append-only, `C-SL1`) but are semantically "undone." → Accepted; no cleanup of historical ledger.
- OQ-PA3: Resolves OQ-GOC2 partially: accumulated `parametric_deferred` commits are swept during regular cadence runs; the Pruning Agent verifies they genuinely had no structural change.

**Interface contract:**
- **IC-PA1.** Pruning Agent ← State Ledger: read access to identify last clean-state reference and scan recent entries (consumes `IC-SL7`).
- **IC-PA2.** Pruning Agent ← Git: diff operations against recorded clean-state reference.
- **IC-PA3.** Pruning Agent ← Audit Trail: read access to Session 4 gap records for orphaned-state detection.
- **IC-PA4.** Pruning Agent → Patch Authorization Gate: `.larql` deletion patches submitted via the standard write path (no fast-path).
- **IC-PA5.** Pruning Agent → Commit Executor: out-of-band catch-up patches flagged `requires_human_review` (extends `IC-GOC2`).
- **IC-PA6.** Pruning Agent → Orchestrator: `stale_urgent` count signal; if exceeds 1,000, write-suspension signal.

---

### Concurrent Write Policy — Spec Block

**What it must guarantee:**
Define how the system handles the scenario where multiple agents attempt to modify the `.vindex` simultaneously. Resolves Session 2 `OQ-W9` (collision warning resolution authority). Note that Session 4 `D40`/`C30` already established the Commit Executor as the sole simultaneous-write path, which partially solves this — but doesn't cover what happens when two Coder Agents' work arrives at the Commit Executor in close sequence with overlapping graph scope.

**Hard constraints:**
- **C-CW1.** Write operations to `.vindex` are **fully serialized** at the Commit Executor. Only one 2PC event is in-flight at any moment. (Formalizes Session 4 `D40`.)
- **C-CW2.** Queue discipline at Commit Executor: FIFO on verified-pass-signal arrival time. No priority queue, no preemption.
- **C-CW3.** Sub-Graph Mutex Locking (from framework reference doc §19.2) is adopted at the **task declaration** level, not the Commit Executor level. Before a Coder Agent begins work, it declares its intended operational scope (entity IDs it intends to write). The Orchestrator places cryptographic locks on those entities.
- **C-CW4.** Scope lock conflicts are resolved at task assignment, not at commit time. If Agent A holds a lock on `func:verify_jwt` and Agent B is assigned a task that would require writing that entity, Agent B's task is either (a) queued until Agent A releases, or (b) reassigned to a non-conflicting subtask. Never: both agents proceed and discover collision at commit time.
- **C-CW5.** Scope locks have maximum hold duration of **60 minutes** per task. A task holding a lock for longer without a `COMMITTED` ledger entry releases the lock automatically. The task continues but loses write-priority guarantees; if another agent has meanwhile committed to the entity, the stale task's `.larql` patch is rejected at Validator with reason `scope_lock_expired_and_superseded`.
- **C-CW6.** Lock release is automatic on `COMMITTED` ledger entry. Lock is also released on `FAILED` or `COMPENSATED` entry.

**Collision resolution authority (closes OQ-W9):**
- Orchestrator is authoritative for scope lock assignment and conflict detection.
- Transaction Controller is authoritative for commit-time collision detection (the rare case where locks were somehow bypassed — treated as a security incident, integrity-violation event).
- Neither agents nor the Validator have authority to resolve collisions.

**Lock declaration format (attached to Session 4 `IC17` TGA input analog):**
```
{
  task_id: ...,
  agent_id: ...,
  intended_write_scope: {
    entities: [...],
    relations: [...],
    tier: "incremental"
  },
  declared_at: timestamp,
  max_hold_duration: 3600  // seconds
}
```

**Tradeoffs decided:**
- Full serialization over parallel writes. Parallel writes to different graph regions is theoretically possible but creates merge-conflict logic in the write engine that's not worth the complexity at current scale. Revisit if write throughput becomes a bottleneck.
- Task-declaration-time locking over commit-time locking. Commit-time detection is too late — agents will have invested work that's discarded. Declaration-time avoids wasted work at the cost of slightly more planning overhead per task.
- Stale-task automatic release over stale-task hard-fail. Rationale: long-running tasks may legitimately need more than 60 min; forcing hard-fail would penalize legitimate work. Releasing the lock but marking patches as superseded-on-conflict gives the stale task a chance to commit if no competitor arrived.
- Security-incident treatment of commit-time collisions (after declaration-time locks) chosen because it should never happen under the declared protocol — occurrence indicates a bypassed control.

**Open questions (deferred):**
- OQ-CW1: Inter-agent lock negotiation — can Agent A voluntarily release early to unblock Agent B? Orchestration session.
- OQ-CW2: Lock visibility — do agents see each other's held locks, or only the Orchestrator? Recommendation: Orchestrator-only, agents request via API.
- OQ-CW3: Read locks vs. write locks — does read access to an entity require any lock? Recommendation: no read locks needed under strong consistency model; the `.vindex` mount window handles read serialization.

**Interface contract:**
- **IC-CW1.** Orchestrator → Scope Lock Registry: task declarations produce lock entries.
- **IC-CW2.** Orchestrator → Coder Agent: task assignment includes declared-and-locked scope; lock failure = task queued or reassigned.
- **IC-CW3.** Commit Executor ← Orchestrator: verified-pass-signal carries scope lock reference. Commit Executor verifies the lock is still held before beginning 2PC.
- **IC-CW4.** Transaction Controller → Audit Trail: commit-time collision event = integrity-violation classification.
- **IC-CW5.** Scope Lock Registry → State Ledger: lock-release events recorded alongside `COMMITTED`/`FAILED`/`COMPENSATED` entries.

---

### Overlay Compaction — Spec Block

**What it must do:**
Manage the accumulation of incremental `.vindex` overlays over time, preventing the "overlay stack" from growing unboundedly and keeping inference latency predictable. Resolves Session 2 `OQ-W4` (compaction spec) and `OQ-W10` (full MEMIT re-run vs. delta composition).

**Background — why compaction is needed:**
The Session 2 tiered overlay architecture (`D14`) creates a stack: `base_model + genesis_schema + genesis_domain + genesis_constraints + genesis_knowledge + incremental_1 + incremental_2 + ...`. Each incremental overlay is a set of weight deltas (ΔW). At inference time, the effective weights are the sum of base + all overlays. As incrementals accumulate (Session 2 drift thresholds: warning at 3,000 cumulative edges, hard limit at 8,000), inference slows, memory pressure increases, and the risk of weight-delta interference grows.

**Hard constraints:**
- **C-OC1.** Genesis tiers (L1–L4) are **never** compacted. They are the immutable substrate; compaction operates exclusively on incremental overlays.
- **C-OC2.** Compaction is a 2PC event — the new compacted overlay and the retirement of the old overlays form a single atomic transaction. No partial compactions in observable state.
- **C-OC3.** Compaction is initiated by the Transaction Controller (authority: maintains consistency contract across the compaction boundary), executed by the MEMIT Write Engine.
- **C-OC4.** Old incremental overlays are **archived, not deleted**. Rationale: rollback to a pre-compaction state requires the original overlays. Archive storage: `<harness_root>/.state-ledger/archive/`. Archive entries retained for project lifetime unless explicit human-authorized purge.
- **C-OC5.** Post-compaction, the State Ledger receives a `COMPACTION_BOUNDARY` entry that marks the replaced overlay range and the new consolidated overlay. Rollback to any pre-compaction-boundary state requires restoring the archived overlays.
- **C-OC6.** Compaction cannot occur while writes are in flight. A compaction request waits for the write queue to drain, then claims the Commit Executor lock for the duration.

**Trigger conditions:**
1. **Edge-count threshold:** Incremental overlay count reaches 3,000 cumulative edges (Session 2 warning threshold) → schedule compaction at next idle window.
2. **Overlay count threshold:** More than 50 incremental overlay files → schedule compaction regardless of edge count.
3. **Inference latency degradation:** If p95 inference latency exceeds baseline by 2×, schedule compaction. Requires telemetry layer (deferred to orchestration session).
4. **Manual trigger:** Human-initiated via Orchestrator.
5. **Hard trigger:** At 8,000 cumulative edges (Session 2 hard limit), writes are blocked until compaction completes. This is the upper safety bound.

**Compaction strategy (closes OQ-W10):**

Two candidate strategies, decision below:

| Strategy | Description | Pros | Cons |
|---|---|---|---|
| **Full re-run** | Take all `.larql` patches since last compaction boundary, re-run MEMIT on them as a single Genesis-Mode batch, produce one consolidated overlay. | Cleanest result; fresh covariance balancing across the whole set; no delta-interference artifacts. | Expensive (MEMIT is slow at scale); requires all original `.larql` patches to be retrievable. |
| **Delta composition** | Mathematically sum the weight deltas (ΔW) of the existing overlays into a single consolidated overlay. No MEMIT recompilation. | Fast; no GPU cost; deterministic. | Does not rebalance covariance; accumulated delta interference is preserved, not corrected. Inherits whatever polysemantic noise is already in the stack. |

**Decision:** **Full re-run is the primary strategy. Delta composition is not authorized for production use.**

**Rationale:** The whole point of compaction is to reclaim the guarantees MEMIT provides (orthogonal projection, covariance balancing — Session 2 `D20`). Delta composition skips the mathematical safeguards that give us the Session 2 correctness properties. A "faster but incorrect" compaction is indistinguishable from degraded inference, which is precisely the condition compaction is supposed to fix.

**Prerequisite:** Full re-run requires the original `.larql` patches be retrievable. This means:
- **C-OC7.** All `.larql` patches are retained for the project lifetime in `<harness_root>/.larql-archive/`, indexed by ledger entry ID. Storage cost: text files, negligible.

**Compaction pipeline:**
1. Transaction Controller detects trigger condition.
2. Drain the Commit Executor write queue; acquire lock.
3. State Ledger writes `COMPACTION_BEGIN` entry.
4. Retrieve all `.larql` patches in the compaction range from the `.larql-archive`.
5. MEMIT Write Engine executes Genesis-Mode compile on the full patch set → produces `compacted_incremental_N.vindex`.
6. Post-write verification (Session 2 `D18`): full behavioral probe across a sampled subset of high-weight edges from the original patches. Sample size: all edges with `attention_weight >= 0.90`, plus 10% random sample of others.
7. If verification passes: retire old overlays to archive, mount new consolidated overlay, write `COMPACTION_BOUNDARY` ledger entry.
8. If verification fails: **abort compaction, retain existing overlays unchanged**. Raise integrity event to Audit Trail. Human review required before retry. Compaction failure is a serious event — it suggests the original patches, when recompiled, no longer produce equivalent behavior.
9. Release Commit Executor lock; resume normal writes.

**Interaction with rollback:**
- Rollback to a commit that falls **after** the latest compaction boundary: standard rollback via State Ledger snapshot lookup.
- Rollback to a commit **before** a compaction boundary: requires unmounting the consolidated overlay and remounting the archived original overlays. This is a heavier operation but fully supported under `C-OC4`.
- Rollback across multiple compaction boundaries: same pattern, chained. Archive retention per `C-OC4` ensures this remains possible for project lifetime.

**Tradeoffs decided:**
- Full re-run over delta composition despite higher compute cost. The correctness argument dominates.
- Archive-and-retain over delete. Storage is cheap; rollback guarantees are expensive to lose.
- Compaction drains writes rather than running concurrently. Simpler; consistent with serialized-write model (`C-CW1`).
- Verification failure aborts rather than falling back. Non-negotiable: if the recompiled version doesn't match the originals' behavior, the system cannot claim the overlays are equivalent.

**Open questions (deferred):**
- OQ-OC1: Idle-window scheduling mechanism — how does the Transaction Controller detect "idle"? Orchestration session.
- OQ-OC2: Incremental compaction (compact subsets of incremental overlays, not all of them) — would allow smaller compaction events at the cost of more boundary entries. Out of scope for initial spec.
- OQ-OC3: Verification sample size tuning — 100% of high-weight + 10% sample is a starting heuristic; empirical validation needed post-deployment.
- OQ-OC4: How does compaction interact with Genesis Seal rollback? Genesis Seal (`C-SL3`) anchors pre-incremental state; compaction only affects incrementals. Rollback to Genesis Seal is unaffected by any number of compactions.

**Interface contract:**
- **IC-OC1.** Transaction Controller → Commit Executor: compaction trigger, drain queue signal.
- **IC-OC2.** Transaction Controller → MEMIT Write Engine: Genesis-Mode recompile request with retrieved patch set.
- **IC-OC3.** Commit Executor ← `.larql` archive: patch retrieval by ledger entry ID range.
- **IC-OC4.** MEMIT Write Engine → Behavioral Probe: verification request on compacted overlay (reuses Session 2 `IC9`).
- **IC-OC5.** Transaction Controller → State Ledger: `COMPACTION_BEGIN`, `COMPACTION_BOUNDARY`, `COMPACTION_ABORT` entries.
- **IC-OC6.** Transaction Controller → Audit Trail: compaction events, especially abort events as integrity-review candidates.

---

That's all eight spec blocks. Session 5 is complete. Copy-paste handoff block below.

---

```
═══════════════════════════════════════════════════
SESSION 5 — State Consistency Theorist
PRIMARY OUTPUTS: Consistency model · Authoritative medium policy ·
                 Two-Phase Commit boundary · Transaction Controller ·
                 State Ledger · Git operations classification ·
                 Pruning Agent · Concurrent write policy ·
                 Overlay compaction
═══════════════════════════════════════════════════

DECISIONS MADE
───────────────────────────────────────────────────
D42. Authoritative medium is content-scoped:
     — Git authoritative for `structural_entity` knowledge
     — .vindex authoritative for Genesis Layer 4
       `domain_concept` and `constraint_rule` knowledge
     Every .larql patch carries mandatory
     CONTENT_CLASSIFICATION directive: structural |
     layer4_domain. `mixed` rejected pre-commit.

D43. Consistency model: strong consistency globally.
     Reads block against .vindex during mount window.
     No stale-read fallback. Commit Executor serialization
     (Session 4 D40) caps write concurrency at 1.

D44. Atomic transaction unit is the task-completion
     package: {module_code, test_suite, .larql_patch}.
     These commit together or not at all.

D45. Genesis compile is a single 2PC event across all
     tier files (L1-L4). Partial Genesis is not a valid
     state.

D46. Phase 2 medium ordering is fixed: Git push first,
     .vindex mount second. Constrains failure modes to
     Git-ahead (easier to recover) rather than
     Weights-ahead.

D47. Transaction Controller compensating transaction
     direction is determined by CONTENT_CLASSIFICATION:
     — structural: auto-revert Git on persistent .vindex
       failure (3 mount retries then revert)
     — layer4_domain: retry .vindex up to 5x; Git revert
       requires human confirmation

D48. Circuit breaker thresholds:
     — 3 consecutive 2PC failures in one task → trip
     — 5 consecutive 2PC failures across any tasks in
       10-min window → trip
     — Diverged state → immediate trip, no auto-repair

D49. State Ledger stored outside Git and outside .vindex:
     primary location `<harness_root>/.state-ledger/ledger.jsonl`
     (append-only log, filesystem permissions). Genesis Seal
     dual-stored: append-only log AND Git-committed
     `<repo_root>/.harness/genesis-seal.json`. Boot-time
     hash comparison of both copies; mismatch = do not boot.
     (Closes OQ-S6.)

D50. Chain-of-custody: every ledger entry contains Merkle-
     chain-lite hash linking to previous entry. Chain
     verification runs on every system boot from Genesis
     Seal forward. Chain break = write suspension,
     integrity-violation event, human review.

D51. Git operations classified at commit time as
     parametric_required | parametric_none |
     parametric_deferred. Unclassified defaults to
     parametric_required (safe failure). Path-pattern
     based classification.

D52. Out-of-band Git commits (human hotfixes, manual
     commits) reconciled post-hoc by Pruning Agent.
     Catch-up patches generated but flagged
     `requires_human_review`; no auto-compile.

D53. Pruning Agent writes flow through the same 2PC
     path as all other writes. No fast-path. Pruning
     patches always classified `structural`.

D54. Pruning Agent restricted to Structural and Knowledge
     family edges only (reinforces Session 1 D8). Cannot
     touch Genesis tiers L1-L3 (consistent with Session 3
     C19).

D55. Acceptable staleness window: 24 hours between Git
     deletion and corresponding .vindex edge deletion.
     After 24h, edges classified stale_urgent. At 1,000
     stale_urgent, writes suspended until Pruning completes.

D56. Pruning Agent cannot delete edges written within
     last 24 hours (gives in-flight tasks time to converge).

D57. Pruning trigger conditions: every 50 commits OR
     24 hours (cadence); on source file deletion in Git;
     on function rename detection; on out-of-band commit;
     on Session 4 D37 gap record followup; manual trigger.

D58. Full serialization of writes (Commit Executor FIFO
     queue). No parallel writes to different graph regions
     in v1 spec.

D59. Sub-Graph Mutex Locking at task declaration time
     (not commit time). Orchestrator assigns locks;
     conflicts resolved before agent begins work.

D60. Scope lock max hold duration: 60 minutes. Auto-release
     on timeout; stale task's patch rejected at Validator
     with `scope_lock_expired_and_superseded` if another
     agent committed meanwhile. (Closes OQ-W9.)

D61. Commit-time collision after declaration-time locks is
     treated as security incident (integrity-violation),
     not a normal merge case. Should be impossible under
     protocol.

D62. Overlay compaction strategy: full MEMIT re-run on
     archived .larql patches. Delta composition rejected —
     skips MEMIT's mathematical safeguards (orthogonal
     projection, covariance balancing from Session 2 D20).
     (Closes OQ-W10.)

D63. Compaction triggers: 3,000 cumulative edges (warning,
     schedule at idle); 50+ overlay files; p95 inference
     latency 2x baseline; manual; 8,000 edges (hard
     trigger, block writes until complete).

D64. Old incremental overlays archived, not deleted
     (`<harness_root>/.state-ledger/archive/`). Retained
     for project lifetime. Archive preserves rollback
     capability across compaction boundaries.

D65. All .larql patches retained for project lifetime in
     `<harness_root>/.larql-archive/` indexed by ledger
     entry ID. Required for full-rerun compaction.

D66. Compaction verification: full behavioral probe of
     all edges with attention_weight >= 0.90 plus 10%
     random sample of others. Verification failure =
     compaction aborted, existing overlays retained
     unchanged, human review required.

D67. 2PC infrastructure failures (GPU OOM, compile fail)
     do NOT consume Session 4 Coder Agent retry budget
     (D36). Transaction Controller handles infrastructure
     failures independently. (Closes OQ-TC2.)

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C-SC1. Git authoritative for structural_entity content.
C-SC2. .vindex authoritative for Layer 4 domain_concept
       and constraint_rule content.
C-SC3. CONTENT_CLASSIFICATION directive mandatory in all
       .larql patches (extends Session 2 D15 four-section
       format).
C-SC4. `mixed` classification rejected pre-commit; split
       required.
C-SC5. Strong consistency: reads block during mount window.
C-TPC1. Atomic transaction = task-completion package.
C-TPC2. Genesis compile is single atomic 2PC event.
C-TPC3. Phase 2 ordering fixed: Git first, .vindex second.
C-TPC4. Every 2PC writes PREPARED and COMMITTED ledger
        entries. Missing PREPARED = ledger-bypass security
        incident.
C-TPC5. Commit Executor holds session-scoped lock during
        entire 2PC window.
C-TC1. Transaction Controller is sole compensating-
       transaction authority. No agent, including Commit
       Executor, self-compensates.
C-TC2. Compensation direction determined by
       CONTENT_CLASSIFICATION.
C-TC3. Circuit breaker: 3/task or 5/10min triggers
       systemwide write suspension.
C-TC4. All compensating transactions logged to Audit Trail.
C-TC5. Diverged state never auto-repaired.
C-SL1. State Ledger append-only; no modification, no
       deletion.
C-SL2. Merkle-chain-lite integrity; chain break suspends
       writes.
C-SL3. Genesis Seal marked IMMUTABLE_ANCHOR; trust root.
C-SL4. Ledger stored outside Git and outside .vindex.
C-SL5. Genesis Seal dual-stored with boot-time hash
       comparison.
C-SL6. No agent has ledger delete authority.
C-GOC1. Every commit classified; unclassified defaults
        to parametric_required.
C-GOC3. parametric_none cannot be self-declared by
        agents.
C-GOC4. Out-of-band commits reconciled with human review;
        no auto-compile.
C-PA1. Pruning writes use standard 2PC path; no exemption.
C-PA2. Pruning restricted to Structural and Knowledge
       family edges.
C-PA3. Pruning cannot modify Genesis tiers L1-L3.
C-PA5. Pruning cannot delete edges younger than 24 hours.
C-PA6. 24-hour staleness window maximum.
C-CW1. Full write serialization at Commit Executor.
C-CW3. Sub-Graph Mutex Locking at task declaration.
C-CW4. Scope lock conflicts resolved at assignment, not
       at commit.
C-CW5. 60-minute max scope lock hold; auto-release on
       timeout.
C-OC1. Genesis tiers never compacted.
C-OC2. Compaction is a single atomic 2PC event.
C-OC4. Old overlays archived, never deleted; project-
       lifetime retention.
C-OC7. All .larql patches archived for project lifetime.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ-SC1  Classification assignment authority: agent-
        declared, auto-classifier, or Validator-enforced?
        → Potential revisit in Validation session.

OQ-SC2  Layer 4 recovery when originating external doc
        is unavailable (e.g., Pixeltable record deleted):
        .vindex alone sufficient, or human attestation?
        → Operational policy.

OQ-TPC1 PREPARED-state timeout before Transaction
        Controller treats transaction as abandoned.
        Needs empirical input from MEMIT compile latency
        on target hardware.

OQ-TPC2 External abort signal authority: can a human
        interrupt a PREPARED transaction?
        → Orchestration session.

OQ-TC1  Circuit-breaker reset protocol: who can reset
        (human only? privileged orchestrator?)?
        → Operational policy.

OQ-TC3  Should Transaction Controller expose real-time
        consistency-status signal to other agents?
        → Orchestration session.

OQ-SL1  Ledger compaction/archival policy. Ledger grows
        unboundedly; at what size/age do we archive?
        Archived entries must remain verifiable.
        → Operational policy.

OQ-SL2  Multi-machine harness ledger replication strategy.
        → Orchestration session (out of scope for
        single-machine spec).

OQ-SL3  Agent read access to ledger: direct or Orchestrator-
        mediated? Recommend Orchestrator-mediated
        consistent with Session 3 OQ-S7.
        → Operational policy.

OQ-GOC1 Path classification list storage: Genesis
        constitutional file, or per-project config?
        → Orchestration session.

OQ-PA1  Should Pruning Agent output be reviewed by
        separate agent before Commit Executor?
        Recommendation: standard Validator path
        suffices.

OQ-CW1  Inter-agent voluntary lock release for negotiation.
        → Orchestration session.

OQ-CW2  Lock visibility to agents: direct or Orchestrator-
        mediated? Recommendation: Orchestrator-only.

OQ-OC1  Idle-window scheduling detection mechanism.
        → Orchestration session.

OQ-OC3  Compaction verification sample size tuning
        (100% high-weight + 10% other is starting
        heuristic). Empirical post-deployment.

═══════════════════════════════════════════════════
ITEMS CLOSED FROM PREVIOUS SESSIONS
═══════════════════════════════════════════════════
OQ-W4  (Session 2): CLOSED — overlay compaction
       specced. Full MEMIT re-run strategy. Triggers,
       pipeline, archive retention defined.

OQ-W9  (Session 2): CLOSED — collision resolution
       authority. Orchestrator assigns scope locks at
       task declaration; Transaction Controller handles
       commit-time collisions as security incidents.

OQ-W10 (Session 2): CLOSED — full MEMIT re-run
       chosen over delta composition. Correctness
       argument dominates.

OQ-S6  (Session 3): CLOSED — Genesis Seal dual-
       stored: primary in `.state-ledger/ledger.jsonl`
       append-only log, secondary as Git-committed
       `.harness/genesis-seal.json`. Boot-time hash
       comparison.

OQ-TC2 (this session): CLOSED — 2PC infrastructure
       failures do not consume Session 4 Coder Agent
       retry budget.

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC-SC1. .larql schema extension: CONTENT_CLASSIFICATION
        directive mandatory (extends Session 2 D15).

IC-SC2. Patch Authorization Gate → Write Engine:
        verified patch carries classification tag
        unmodified.

IC-SC3. Transaction Controller ← State Ledger:
        classification readable per-entry to drive
        rollback direction.

IC-TPC1. Commit Executor ← Orchestrator:
         verified task-completion package + content
         classification.

IC-TPC2. Commit Executor → State Ledger:
         PREPARED entry before any medium write;
         COMMITTED entry after both advances succeed.

IC-TPC3. Commit Executor → MEMIT Write Engine
         (consumes Session 2 IC6):
         compile request returns {success,
         overlay_filepath, overlay_hash}. Mount is
         separate downstream step.

IC-TPC4. Commit Executor → Transaction Controller:
         failure signal on Phase 1 or Phase 2 step
         failure; carries ledger entry reference.

IC-TC1. Transaction Controller ← Commit Executor
        (consumes Session 4 IC23):
        2PC step outcome signals at every phase
        boundary.

IC-TC4. Transaction Controller → Audit Trail:
        compensating transaction records (integrates
        with Session 3 D28).

IC-TC5. Transaction Controller → Orchestrator:
        circuit-breaker trip signal + ledger reference
        for human review packaging.

IC-TC6. Transaction Controller → MEMIT Write Engine:
        mount retry signal (distinct from compile
        retry).

IC-SL1. State Ledger ← Commit Executor:
        PREPARED and COMMITTED entry writes.

IC-SL2. State Ledger ← Transaction Controller:
        COMPENSATED and FAILED entry writes.

IC-SL3. State Ledger ← System Bootstrap (Genesis only):
        IMMUTABLE_ANCHOR entry; one-time, cannot be
        invoked post-Genesis.

IC-SL4. State Ledger → Rollback Coordinator:
        commit-hash-to-snapshot-hash lookup for
        git checkout temporal reconciliation.

IC-SL6. State Ledger → Audit Trail:
        integrity-violation events on chain-break or
        Genesis Seal mismatch.

IC-GOC1. Commit Executor → State Ledger:
         classification field mandatory on every entry
         (extends IC-TPC2).

IC-GOC2. Pruning Agent → Commit Executor:
         catch-up patch for out-of-band commit, flagged
         requires_human_review.

IC-PA3. Pruning Agent ← Audit Trail:
        read access to Session 4 D37 gap records for
        orphaned-state detection.

IC-PA4. Pruning Agent → Patch Authorization Gate:
        deletion patches submitted via standard write
        path (no fast-path).

IC-PA6. Pruning Agent → Orchestrator:
        stale_urgent count signal; > 1,000 triggers
        write-suspension signal.

IC-CW1. Orchestrator → Scope Lock Registry:
        task declarations produce lock entries.

IC-CW2. Orchestrator → Coder Agent:
        task assignment includes declared-and-locked
        scope; lock failure = queued or reassigned.

IC-CW3. Commit Executor ← Orchestrator:
        verified-pass-signal carries scope lock reference;
        Commit Executor verifies lock is still held before
        beginning 2PC.

IC-OC1. Transaction Controller → Commit Executor:
        compaction trigger, drain-queue signal.

IC-OC2. Transaction Controller → MEMIT Write Engine:
        Genesis-Mode recompile request with retrieved
        patch set.

IC-OC4. MEMIT Write Engine → Behavioral Probe:
        verification request on compacted overlay
        (reuses Session 2 IC9).

IC-OC5. Transaction Controller → State Ledger:
        COMPACTION_BEGIN, COMPACTION_BOUNDARY,
        COMPACTION_ABORT entries.

═══════════════════════════════════════════════════
INPUT REQUIRED FOR SESSION 6
═══════════════════════════════════════════════════
Session 6 recommended: Orchestration Comparativist
Primary inputs from Sessions 1-5:

The harness now has five fully specced layers. Session 6
must evaluate orchestration candidates against the
accumulated requirements. Key orchestrator-touching
questions carried forward:

  — OQ-V2 (Session 4): retry cap reset behavior per
    subtask after decomposition — orchestration call.

  — OQ-SC1 (this session): CONTENT_CLASSIFICATION
    assignment authority and auto-classifier need.

  — OQ-TPC2 (this session): external abort signal /
    emergency stop protocol.

  — OQ-TC3 (this session): real-time consistency-status
    signal exposure.

  — OQ-GOC1 (this session): path classification list
    storage location.

  — OQ-CW1, OQ-CW2 (this session): inter-agent lock
    negotiation and visibility.

  — OQ-OC1 (this session): idle-window detection for
    compaction scheduling.

  — OQ-SL2 (this session): multi-machine replication
    (if scope expands beyond single-machine).

Required orchestrator capabilities (derived from specs):
  — Scope Lock Registry management (IC-CW1, IC-CW2)
  — Signed-signal verification between Validator and
    Commit Executor (Session 4 IC21 → IC22)
  — Task decomposition authority (Session 4 D37 Step 1)
  — Schema migration authorization token issuance
    (Session 3 IC14)
  — Human-review-queue management and escalation
    packaging
  — Audit Trail write authority (Session 3 D28)
  — Transaction Controller circuit-breaker reset
    authority (OQ-TC1)

Session 6 must map these against Pi, n8n, Claude agent
harness, and any other candidates to produce a
requirement-to-capability matrix and a recommended
orchestrator selection with documented tradeoffs.
═══════════════════════════════════════════════════
```





---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)