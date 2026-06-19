═══════════════════════════════════════════════════
SESSION 4 — Validation Contract Architect
PRIMARY OUTPUTS: Reflexion loop design · Sandbox spec ·
                 .larql patch validation cascade · Failure
                 escalation contract · Commit Executor pattern ·
                 Validator integrity contract · Prompt injection
                 defense boundary
═══════════════════════════════════════════════════

DECISIONS MADE
───────────────────────────────────────────────────
D32. Test authorship: hybrid model. Human-authored constitutional
     suite (permanent, Genesis) + Dedicated Test-Generation Agent
     (TGA, single-file agent, per-task incremental). Coder Agent
     never authors its own tests.

D33. TGA reads task specification only — never reads Coder Agent
     code before writing tests. Actor-Critic independence enforced
     by sequencing, not policy alone.

D34. Behavioral consistency validation is a four-level
     cost-stratified cascade:
     L1 — Static analysis (all patches, mandatory)
     L2 — Inference probe (edges ≥ 0.85, mandatory)
     L3 — Cross-agent review (conditional: edges ≥ 0.90
          or Genesis-adjacent tier)
     L4 — Human spot-check (periodic audit, not a per-patch gate)

D35. Validator may reject .larql patch independently of code.
     "code_pass_patch_fail" is a named failure mode. Neither
     output is committed when this occurs.

D36. Retry limits are tiered by failure classification:
     — Tier 1 Syntactic / formatting: max 2 retries
     — Tier 2 Logic / test failure: max 3 retries
     — Tier 3 Architectural / schema violation: max 1,
       then immediate escalation
     Hard cap: 5 retry events per task across all tiers.

D37. Failure escalation cascade (in order):
     (1) Task Decomposition — Orchestrator splits task into
         narrower subtasks, each with independent retry budget
     (2) Peer Agent Review — second independent Coder Agent
         receives full retry history and attempts task fresh
     (3) Human Escalation Queue — full package: task spec,
         all retry history, decomposition log, failure tier
     (4) Logged Suspension — task suspended, named gap written
         to audit trail, .vindex NOT patched
     Silent discard is prohibited at every step.

D38. Prompt injection defense is two-layer sequential:
     — Gate owns structural / pattern inspection (field lengths,
       control characters, escape sequences). No NL parsing.
     — Validator owns semantic content inspection (instruction-
       like language in free-text fields, override-pattern entity
       names). No retry offered for injection suspects.

D39. Validator Agent has no write authority. Validator outputs
     are signed signals only, classified as orchestration
     communications.

D40. Commit Executor pattern adopted: single-file, deterministic,
     non-reasoning agent. Sole component with simultaneous write
     access to both Git and the MEMIT write engine.

D41. Meta-Validator runs on schedule (every 50 commits or weekly,
     whichever first) against a held-out human-authored suite
     never exposed during normal operation. Validator Health Score
     tracked with defined suspension thresholds:
     — ≥ 95%: no action
     — 85–94%: warning flag, human review within 48 hours
     — < 85%: Validator suspended, immediate human review,
       recent passes audited

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C23. Coder Agent is prohibited from authoring tests for its own
     output. TGA must be a separate, independent actor.

C24. TGA sequencing: TGA reads task specification before or
     without access to Coder Agent code during test authorship.
     Sequencing is the enforcement mechanism.

C25. Constitutional test suite failures are treated as Tier 3
     (architectural) regardless of the error's surface appearance.

C26. "code_pass_patch_fail" is a hard rejection. Code is not
     committed when the patch fails, even if code is correct.
     Both outputs must pass or neither is committed.

C27. Hard retry cap: 5 events per task across all tiers combined.

C28. Every task that exhausts the retry loop must exit with a
     named outcome in the audit trail. Silent discard is
     prohibited.

C29. Injection suspect events are never offered a retry. Always
     hard rejection + human review flag, regardless of injection
     confidence level.

C30. Commit Executor is the exclusive component with simultaneous
     write access to both state mediums (Git + MEMIT write
     engine). No reasoning agent holds this access.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ-V1  Should constitutional test failures always be Tier 3,
       or can a constitutional syntax test be classified Tier 1?
       → Human policy decision required

OQ-V2  Hard retry cap resets per subtask after decomposition
       — confirm behavior with Orchestration session
       → INPUT REQUIRED: Session 6 (Orchestration)

OQ-V3  TGA outputs: do TGA-generated tests require their own
       validation pass, or is the constitutional suite sufficient
       as a correctness floor?
       → Deferred

OQ-V4  Cross-agent review (Level 3): how is structural agreement
       between two independent patches scored? Exact match vs.
       semantic similarity threshold?
       → Deferred

OQ-V5  Held-out suite authorship and update cadence — who
       maintains it and how often is it extended?
       → Human operational policy decision

═══════════════════════════════════════════════════
ITEMS CLOSED FROM PREVIOUS SESSIONS
═══════════════════════════════════════════════════
OQ-S1 (Session 3): CLOSED — Gate owns structural injection
      inspection; Validator owns semantic inspection. Both
      layers required, sequential.

OQ-S3 (Session 3): CLOSED — Validator Agent has no write
      authority. Commit Executor pattern adopted as write-action
      isolation mechanism.

OQ-W7 (Session 2): CLOSED — storage-pass/behavior-fail is a
      named failure mode in the behavioral consistency cascade
      (Level 2 inference probe). Not silently collapsed into
      success. Logged as distinct write outcome.

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC17. TGA ← Orchestrator:
      task specification + schema vocabulary. TGA does NOT
      receive Coder Agent code output.

IC18. Sandbox → Verbal Feedback Generator:
      {exit_code, stdout, stderr, failed_test_ids,
      assertion_messages}

IC19. Verbal Feedback Generator → Coder Agent:
      structured failure report with required fields:
      {failure_tier, failed_component, failed_test_ids,
      localized_error, suspected_cause,
      retry_history_summary (mandatory from attempt 2),
      constraint_reminder, suggested_focus}

IC20. Patch Validator → Orchestrator:
      {patch_verdict: "pass" | "schema_fail" |
      "behavioral_fail" | "code_pass_patch_fail"}

IC21. Validator Agent → Orchestrator:
      signed pass/fail signal. Signal passes Orchestrator
      verification layer before Commit Executor is spawned.
      Validator does not communicate directly with Commit
      Executor.

IC22. Orchestrator → Commit Executor:
      {verified_pass_signal, gate-cleared .larql patch,
      code payload, target project vindex}

IC23. Commit Executor → Transaction Controller (Session 5):
      two-phase commit initiation. PRIMARY INPUT FOR SESSION 5.

IC24. Meta-Validator → Audit Trail:
      validator health record: {health_score, threshold_status,
      sample_cases_reviewed, validator_version, timestamp}

═══════════════════════════════════════════════════
INPUT REQUIRED FOR SESSION 5
═══════════════════════════════════════════════════
Session 5 recommended: State Consistency Theorist
Primary inputs from Sessions 1–4:
  — IC23: Commit Executor → Transaction Controller handoff
    is the primary interface to spec in Session 5
  — OQ-W4 (Session 2): overlay compaction spec — State
    Consistency Theorist owns this domain
  — OQ-W9 (Session 2): collision warning resolution authority
  — OQ-W10 (Session 2): overlay compaction — full MEMIT
    re-run vs. delta composition
  — OQ-S6 (Session 3): genesis snapshot hash sealed storage
    — State Ledger owns this domain
  — Transaction Controller circuit breaker behavior must be
    fully specced (Git commit succeeds, MEMIT compile fails)
  — Pruning Agent deletion trigger policy relative to audit
    trail gap records created in this session (D37, Step 4)
  — Two-phase commit must guarantee: either both state mediums
    update, or neither does