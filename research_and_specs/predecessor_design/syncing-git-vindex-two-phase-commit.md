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