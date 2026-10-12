SESSION 2 — MEMIT Specialist
PRIMARY OUTPUTS: Write engine selection, .vindex tier architecture,
                 .larql canonical format, post-write verification
                 protocol, catastrophic forgetting mitigations

═══════════════════════════════════════════════════
DECISIONS MADE
═══════════════════════════════════════════════════
D11. All writes are overlay-based (policy-immutable .vindex files).
     Base model is never modified under any circumstances.
     This is a hard architectural constraint.

D12. MEMIT is the designated write engine. GRACE and fine-tuning
     are explicitly excluded. ROME is excluded as primary engine.

D13. Write engine operates in two modes: Genesis Mode (batch,
     mints initial .vindex stack) and Incremental Mode (smaller
     patches, buffered via L1 Cache before MEMIT compile).

D14. .vindex overlay stack is tiered to mirror Genesis layers:
     genesis_schema / genesis_domain / genesis_constraints /
     genesis_knowledge / incremental patches. Separate files
     per tier for independent rollback capability.

D15. .larql canonical format defined. Four sections: Entity
     Registration, Edge Declarations, Deletions, Compiler
     Directives. BEGIN/COMMIT bracketing required.

D16. OQ4 resolved: contains/defined_in uses one canonical
     directed edge (defined_in, child→parent). Write engine
     auto-generates reverse. Agents declare canonical direction
     only.

D17. OQ1 resolved: version_artifact is NOT an FFN base type.
     Version metadata lives in State Ledger (orchestration layer).
     Session 1 five-type taxonomy unchanged.

D18. Post-write verification is two-level: Level 1 storage probe
     (SELECT read-back, mandatory for all writes) + Level 2
     behavioral probe (generation test, mandatory for high-weight
     edges ≥ 0.85).

D19. Storage-pass / behavior-fail is a named failure mode.
     It must not be silently treated as a full pass.

D20. Orthogonal projection and covariance balancer are mandatory
     write engine operations — not optional safeguards.

D21. Provisional overlay drift thresholds: warning at 3,000
     cumulative edges; hard limit at 8,000 (pending empirical
     validation against target model).

═══════════════════════════════════════════════════
CONSTRAINTS ESTABLISHED
═══════════════════════════════════════════════════
C8.  Base model is permanently frozen. Write engine output
     must never target base model weights.
C9.  `violates` relation rejected at write engine input stage
     (pre-MEMIT filter). Full patch rejected on violation.
C10. Undeclared base_type or relation label: full patch rejection.
C11. TIER directive required in all .larql patches.
C12. Genesis L1–L3 patches require orchestrator schema migration
     token. Coder Agent patches targeting these tiers are
     hard-rejected by write engine.
C13. attention_weight must be in [0.0, 1.0]. Out-of-range is
     malformed patch — hard rejection.
C14. BEGIN TRANSACTION / COMMIT required. Partial writes
     are prohibited — all-or-nothing.
C15. Layer targeting restricted to middle-to-late FFN layers
     (L15–L25 for 32-layer model). Early syntax layers
     are off-limits for semantic injection.

═══════════════════════════════════════════════════
OPEN QUESTIONS DEFERRED
═══════════════════════════════════════════════════
OQ-W1  Cumulative edit volume degradation threshold
       (model-specific, empirical)
OQ-W2  MEMIT/Gemma architecture compatibility verification
OQ-W3  Genesis: single batch vs. sequential tier compile
       → INPUT REQUIRED: Session 3 (Validation/AISecOps)
OQ-W4  Overlay compaction spec
       → INPUT REQUIRED: Session 5 (State Consistency)
OQ-W5  attention_weight: agent-declared vs. engine-computed
       → MUST RESOLVE before .larql format is final
OQ-W6  .larql schema versioning strategy
OQ-W7  Response to storage-pass / behavior-fail
       → CRITICAL INPUT for Session 4 (Validation Contract)
OQ-W8  Behavioral probe generalization (non-code domains)
OQ-W9  Collision warning resolution authority
       → INPUT REQUIRED: Session 5 (State Consistency)
OQ-W10 Overlay compaction: full MEMIT re-run vs. delta composition
       → INPUT REQUIRED: Session 5 (State Consistency)

═══════════════════════════════════════════════════
INTERFACE CONTRACTS DEFINED
═══════════════════════════════════════════════════
IC5. Write Engine ← Validator:
     Receives schema-validated .larql patch only.
     Validator confirms: base_type declared, relation labels
     in vocabulary, `violates` absent, TIER declared,
     attention_weight in range, transaction bracketed.
     Write engine assumes pre-validated input.

IC6. Write Engine → State Ledger:
     Outputs overlay filename + hash after each successful
     compile. State Ledger maps this to current Git commit hash.

IC7. Write Engine → Orchestrator:
     Returns write result signal: {success, behavior-fail,
     storage-fail, rejected} with failure reason on non-success.

IC8. Write Engine ← Orchestrator (Genesis only):
     Receives schema migration authorization token for
     L1–L3 tier writes. Token format TBD (AISecOps session).

IC9. Behavioral Probe → Orchestrator:
     Returns probe result: {pass, storage-pass/behavior-fail}
     with the agent-declared EXPECTED_SIGNAL and actual
     generation output for review.

═══════════════════════════════════════════════════
INPUT REQUIRED FOR SESSION 3
═══════════════════════════════════════════════════
Session 3 recommended: AISecOps Specialist (The Warden)
Primary inputs from Sessions 1–2:
  — Schema migration authorization token spec (IC8, OQ-W3)
  — Genesis bootstrapping write authorization (OQ8 from S1)
  — Trust boundary between Coder Agent and write engine
  — Policy-immutable overlay enforcement mechanism
  — .larql patch supply chain integrity
  — OQ-W5 (attention_weight authority) has security implications
    — Warden should weigh in before this is closed