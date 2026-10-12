## Appendix B — Interface Contract Index

Canonical list of inter-component contracts. Cross-references to session of origin.

### From Session 1 (Schema)
- **IC1** — Write Engine receives base-type tag + relation-family tag; enforces `violates` hard rejection.
- **IC2** — Validator receives declared vocabulary; rejects undeclared types or relations.
- **IC3** — Pruning Agent receives deletion policy + namespace flag; restricted to Structural/Knowledge families.
- **IC4** — Orchestrator receives query results with `coverage_quality` flag; empty results route to documentation ingestion.

### From Session 2 (Write Engine)
- **IC5** — Write Engine ← Validator: pre-validated `.larql` patch.
- **IC6** — Write Engine → State Ledger: overlay filename + hash post-compile.
- **IC7** — Write Engine → Orchestrator: write result signal.
- **IC8** — Write Engine ← Orchestrator (Genesis): schema migration token (revised T7).
- **IC9** — Behavioral Probe → Orchestrator: probe result with expected and actual signals.

### From Session 3 (Security)
- **IC10** — Gate ← Agent: signed `.larql` patch + identity token (extended T5).
- **IC11** — Gate → Validator: verified patch (identity, scope, integrity confirmed).
- **IC12** — Gate → Orchestrator: rejection signal (extended with T5 reason codes).
- **IC13** — Gate → Ledger: evaluation record (every interaction).
- **IC14** — Orchestrator → Write Engine: schema migration token (revised T7, admission-time).
- **IC15** — Write Engine → Ledger: pre-write + post-write hashes + outcome.
- **IC16** — Post-Genesis Seal → Ledger: `IMMUTABLE_ANCHOR` entry.

### From Session 4 (Validation)
- **IC17** — TGA ← Orchestrator: task spec + schema vocabulary.
- **IC18** — Sandbox → Verbal Feedback Generator: execution result.
- **IC19** — Verbal Feedback Generator → Coder: structured failure report.
- **IC20** — Patch Validator → Orchestrator: patch verdict.
- **IC21** — Validator → Orchestrator: signed pass/fail signal (verified before Commit Executor spawn).
- **IC22** — Orchestrator → Commit Executor: verified signal + gate-cleared patch + code payload.
- **IC23** — Commit Executor → Transaction Controller: 2PC initiation.
- **IC24** — Meta-Validator → Ledger: health record (extended T3 per-case; v1.1: includes `corpus_staleness_flag` and `corpus_size_at_run` fields; `health_score` field is `NOT_COMPUTED` when corpus < 20 cases).

### From Session 5 (State Consistency)
- **IC-SC1** — `.larql` schema: `CONTENT_CLASSIFICATION` mandatory.
- **IC-SC2** — Gate → Write Engine: classification tag unmodified.
- **IC-SC3** — Transaction Controller ← Ledger: classification readable for rollback direction.
- **IC-TPC1** — Commit Executor ← Orchestrator: verified package + classification.
- **IC-TPC2** — Commit Executor → Ledger: `PREPARED` / `COMMITTED` entries.
- **IC-TPC3** — Commit Executor → MEMIT: compile request returns `{success, overlay_filepath, overlay_hash}`.
- **IC-TPC4** — Commit Executor → Transaction Controller: failure signal at phase boundary.
- **IC-TC1** — Transaction Controller ← Commit Executor: 2PC step outcomes.
- **IC-TC4** — Transaction Controller → Ledger: compensation records.
- **IC-TC5** — Transaction Controller → Orchestrator: circuit-breaker trip signal.
- **IC-TC6** — Transaction Controller → MEMIT: mount retry signal.
- **IC-SL1** — Ledger ← Commit Executor: `PREPARED` / `COMMITTED`.
- **IC-SL2** — Ledger ← Transaction Controller: `COMPENSATED` / `FAILED`.
- **IC-SL3** — Ledger ← Bootstrap (Genesis): `IMMUTABLE_ANCHOR`.
- **IC-SL4** — Ledger → Rollback Coordinator: commit-to-snapshot lookup.
- **IC-SL6** — Ledger → Audit: integrity-violation events.
- **IC-GOC1** — Commit Executor → Ledger: classification mandatory on entries.
- **IC-GOC2** — Pruning → Commit Executor: catch-up patch with `requires_human_review`.
- **IC-PA3** — Pruning ← Audit: gap record read access.
- **IC-PA4** — Pruning → Gate: deletions via standard write path.
- **IC-PA6** — Pruning → Orchestrator: `stale_urgent` count signal.
- **IC-CW1** — Orchestrator → Scope Lock Registry: task declarations produce lock entries.
- **IC-CW2** — Orchestrator → Coder: task assignment with declared-and-locked scope.
- **IC-CW3** — Commit Executor ← Orchestrator: verified signal carries scope lock reference.
- **IC-OC1** — Transaction Controller → Commit Executor: compaction trigger, drain signal.
- **IC-OC2** — Transaction Controller → MEMIT: Genesis-Mode recompile request.
- **IC-OC4** — MEMIT → Behavioral Probe: verification request on compacted overlay.
- **IC-OC5** — Transaction Controller → Ledger: compaction lifecycle entries.

### From Session 6 (Orchestration)
- **IC-OR1** — Orchestrator → Validator: pass/fail signal verification.
- **IC-OR2** — Orchestrator → Commit Executor: verified package + classification + lock ref + retry state.
- **IC-OR3** — Orchestrator → Ledger: sole write authority (all ledger writes routed).
- **IC-OR4** — Orchestrator → Scope Lock Registry: exclusive read/write.
- **IC-OR5** — Orchestrator → Agent Runtime Wrapper: `agent_invoke(agent_name, input, allowed_tools)`.
- **IC-OR6** — Orchestrator → Human Review Queue: pause workflow with full package.
- **IC-OR7** — Orchestrator → Consistency Status API (six-state enum per T10).
- **IC-OR8** — Human → Orchestrator: signed abort request.
- **IC-OR9** — Orchestrator → Task Lineage Ledger: `TASK_DECOMPOSED` entries.

### From Session 7 (Integration)
- **IC-V-TGA1** — TGA output → Stub Probe → Pass/Fail before Coder invoked (T2).
- **IC-V-TGA2** — Meta-TGA → Ledger: health record parallel to IC24; v1.1 extended per IC-CORPUS-AUTH (T2).
- **IC-SL7** — Ledger ← Bootstrap: `SEALED_CORPUS_INTEGRITY_FAIL` on dual-store mismatch (T3).
- **IC-SL8** — Ledger ← Orchestrator: `SEALED_CORPUS_ACCESS` at Meta-* scheduling (T3).
- **IC-SL9** — Ledger ← Manifest Update Handler: `SEALED_CORPUS_UPDATE` on signed extension (T3).
- **IC-CFG1** — Git commit-hook → Ledger: `CONFIG_UPDATE` on `.harness/` file changes (T4).
- **IC-CFG2** — Bootstrap → Ledger: `CONFIG_INTEGRITY_FAIL` on boot-time mismatch (T4).
- **IC-CFG3** — Orchestrator → WSD + YAML: hash binding check at invocation; `YAML_BINDING_FAIL` on mismatch (T4).
- **IC-MEMIT-3** — Write Engine → Ledger: `ANCHOR_ESTABLISHED` flag on qualifying entries (T6).
- **IC-PA7** — Pruning → Orchestrator: Hold-state query returning `held | not_held` per edge (T8).
- **IC-PA8** — Pruning → Orchestrator: catch-up patch submission with `requires_human_review` (T10).
- **IC-OR10** — Orchestrator → Reconciliation Review Queue (T10).
- **IC-OR11** — Orchestrator → Ledger: backlog warning / critical entries (T10).
- **IC-OR12** — Orchestrator → Consistency Status: `RECONCILIATION_BACKLOG` state (T10).
- **IC-OR13** — Reconciliation Reviewer → Gate: reviewer-signed catch-up patch (T10).
- **IC-OR14** — Reviewer `modify_patch` output → Validator: modified patches re-enter cascade (T10).
- **IC-OC6** — Write Engine → Compaction Bundler: patch set consumed (T9).
- **IC-OC7** — Compaction Bundler → Ledger: `COMPACTION_BUNDLE_SEALED` (T9).
- **IC-OC8** — Retention Manager → Ledger: `SUPERSEDED_BUNDLE_EXPIRED` (T9).
- **IC-LDG1** — Component → Orchestrator: ledger write request (T11).
- **IC-LDG2** — Orchestrator → Ledger: authenticated append with chain hash (T11).
- **IC-LDG3** — Gate / TC / Boot-verifier → Ledger: emergency write path (T11).
- **IC-LDG4** — Orchestrator → Query API: tiered read access (T11).
- **IC-LDG5** — Retention Manager → Ledger: epoch archival ops (T11).

### From IC Review Session (v1.1 — D81–D90)
- **IC-GATE-8** — Gate pre-check #8: `larql_syntax_version` header validation. Rejects absent, below-minimum, and forward-version patches with distinct error codes (`VERSION_REJECTED`, `VERSION_UNSUPPORTED`). Advisory path (`LARQL_VERSION_LEGACY`) for legacy-but-supported versions. Compaction re-run requires versioned parser and `larql_migration_manifest` in Tier 1 config (D81, D82, C-GATE-1).
- **IC-WE-1** — Write Engine → Transaction Controller: `drift_state` object. Fields: `edge_count_since_anchor`, `drift_tier` (NOMINAL/WARNING/HARD/CRITICAL), `anchor_event_id`, `overlay_file_count`, `p95_latency_ratio`. Read before every write token issuance; drift counter reconciled every 100 COMMITTED entries within 5% tolerance (D83, C-WE-1).
- **IC-TC-RESET** — Human Operator → Transaction Controller: signed circuit breaker reset ceremony. TC independently verifies preconditions before accepting. Automatic READ_ONLY on trip; write resumption via signed ceremony only. W3 path excluded from reset authority (D84).
- **IC-TC-TIMEOUT** — Transaction Controller timeout monitor → Write Engine + Orchestrator: two-value timeout model (`incremental_prepared_timeout` default 2h; `genesis_prepared_timeout` operator-set mandatory, C-GATE-2). Incremental timeout → Phase 1 rollback, Hold persists, retry as infrastructure failure. Genesis timeout → circuit breaker trips (DIVERGED_STATE), no auto-compensation (D85).
- **IC-OC-PROBE** — Behavioral Probe (compaction) → Transaction Controller: `CompactionProbeReport` struct. Stratified sampling (CORE 100%; SUPPORTING ≥20% floor; INCIDENTAL 10%); abort thresholds CORE 1.0 (C-OC3) / SUPPORTING 0.95 / INCIDENTAL 0.80. Random seed logged. Sampling rates provisional (OQ-OC3) (D86).
- **IC-SCOPE-UPDATE** — Orchestrator + Gate: Write Scope Definition update ceremony. Mid-flight updates accepted (no drain). Gate returns `SCOPE_HASH_MISMATCH` (not generic) with current scope hash. Active PREPARED transactions not interrupted. Scope changes forward-only (D87).
- **IC-CORPUS-AUTH** — Corpus Author → Sealed Corpus (Meta-Validator / Meta-TGA): role-restricted submission (C-GOC4) with format validation. Minimum 20 cases for valid Health Score. Staleness flag at 90 days. Case formats defined (D88).
- **IC-LDG-RETAIN** — Operator → Ledger: retention lifecycle interface. `PROJECT_INITIATED` (W2 bootstrap, immutable), `PROJECT_CLOSED` (write-final ceremony), `RETENTION_OVERRIDE_EXTENDED` (extensions only). Retention immutable-downward (C-SL2). INTEGRITY_VIOLATION epochs unconditionally indefinite. Archival format versioned `"1.0"` (D89).
- **IC-GATE-9** — Gate → Orchestrator → Coder Agent: `CONTENT_CLASSIFICATION_MIXED` structured rejection with `split_guidance` payload. Gate triple-level classification is authoritative over Coder declarations. `complexity_flag` set when > 5 sub-patches required → human review escalation. Loop detection at 3 equivalent re-rejections (D90).

### From Phase 2 Gap Sessions (v1.1 → v1.2)

*Grouped by originating gap session. Every contract below is a ratified addition or amendment. Deprecated / superseded v1.1 contracts are listed at the end.*

**Ceremony Authorization (v2 GS4 — GAP-26):**
- **IC-SCOPE-AUTH-1** — NEW umbrella authorization contract for all GOVERNANCE-class ceremonies. Common CeremonyToken envelope (ceremony_type / ceremony_id / ceremony_payload / key_ref = CAK). Non-delegable uniform preconditions. See §20.3.
- **IC-TC-RESET** — AMENDED (A3). Reset ceremony authorization key is the CAK per IC-SCOPE-AUTH-1. Genesis-trip Hold-release precondition branch added (A12). CAK-authorization requirement is necessary-but-not-sufficient; TC independent precondition verification unchanged.
- **IC-HOLD-RELEASE** — DELEGATION UPDATE. Authorization layer delegates to IC-SCOPE-AUTH-1. Payload body retained: `hold_id`, `hold_type`, `release_reason_code`.
- **IC-SCOPE-UPDATE** — DELEGATION UPDATE (A5, A6, A9). Payload body retained; admission order specifies rate-limit precedes signature verification. `ceremony_token_id` replaces prior standalone `ratification_signature` / `operator_signature` field.
- **IC-SCHEMA-EXTEND, IC-LDG-RETAIN, IC-SL8** — DELEGATION UPDATE. All delegate authorization to IC-SCOPE-AUTH-1.
- **IC-MANIFEST-1** — AMENDED. Ceremony authorization delegates to IC-SCOPE-AUTH-1; `bucket_map` provisional-flag semantics per §22; Check 8 added (manifest-lattice completeness, GAP-29a).

**Scope Registry (v3 GS5; GS12):**
- **IC-SCOPE-RECONCILE** — NEW. Orchestrator-restart scope-registry reconciliation against Ledger `SCOPE_UPDATED` chain. §10.9.1.
- **IC-AGG-COUNTER** — NEW. Per-Orchestrator-instance aggregate `SCOPE_HASH_MISMATCH` counter behavior (no reset on review; cooldown = M seconds). §14.3, GAP-38.
- **IC-AGG-ALERT-LINK** — NEW. Aggregate-alert → review queue cross-link format, including contributing-invocation list and source agents. §14.3.

**Transaction Controller / State Machine (GS10–GS12):**
- **IC-GCO-1** — NEW. Governance-category write carve-out under `CIRCUIT_TRIPPED` — narrow scope restricted to IC-TC-RESET ceremony entries via ceremony_token_id binding. Closes T-SC-W-2. §11.8.1, GAP-37.
- **IC-CRR-1** — NEW. `CIRCUIT_RESET_REJECTED` rate limit: N=5 / M=60min, advisory + operator alert. GAP-36.
- **IC-TC-PRECURSOR-QUERY** — NEW. TC → Ledger precursor-lookup on Hold-release ceremony admission: coverage + audit-window check. GAP-31.
- **IC-REL-PRECURSOR** — NEW. `HOLD_RELEASE_REASON_UNWARRANTED` emission when operator-cited precursor fails Hold-coverage or audit-window check. SECURITY, sync, W1 (not W3 per C-W3-1). GAP-31.
- **IC-PREPARE-SCOPE** — NEW. `governing_scope_hash` field added to PREPARED and COMMITTED entries (captured at PREPARE, preserved at COMMIT, nullable for pre-amendment entries). GAP-34.
- **IC-MON-GTOTM** — NEW. Monitor pairing-check: `GENESIS_TIMEOUT_TRIP_MISSING` on unpaired genesis-timeout. CONSISTENCY, async, W1. C-GTO-1 / C-GTO-2. GAP-30.

**Dry-Run Store (v2 GS8; GS10):**
- **IC-DRS-1** — NEW. Operator-owned `.dry-run-store/` at `<harness_root>/.dry-run-store/`; 37-day minimum retention; metadata-only Warden audit; manifest-hash anchor in Ledger. GAP-33; T-S-RP-1 accepted.
- **IC-DRYRUN-1** — NEW (v2 GS8). `dry_run_report` artifact shape for IC-MANIFEST-1 Check #5/#6 (dry-run artifact freshness + hash binding).

**Unified Ledger W3 (GS10):**
- **IC-W3-POLICY-1** — NEW. W3 admission consolidation per C-W3-1 two-admission-criteria. Four ratified carve-outs: `INTEGRITY_VIOLATION_EMERGENCY`, governance-ceremony entries under trip, `TRUST_ROOT_LOST`, `BURST_SUSPENDED`. GAP-29b. §16.2.
- **IC-MANIFEST-1** Check 8 — AMENDED. Manifest-lattice completeness verification at ratification; `MANIFEST_LATTICE_INCOMPLETE` emitted on failure (SECURITY, sync). GAP-29a.

**CAK Bootstrap / Burst / Break-Glass (GS10):**
- **IC-BOOT-1** — NEW. CAK bootstrap tool interface. Dual-root signing (operator root + harness release key); atomic write; signed boot manifest; refuse-boot on verification failure. C-BOOT-1 through C-BOOT-7. GAP-40. §23.1.
- **IC-CAKB-1** — NEW. Per-CAK burst limit N=5 / 10min; `BURST_SUSPENDED` state; 60-min auto-clear or Tier 1 explicit clear; orthogonal to GAP-27 and GAP-36. GAP-41. §23.2.
- **IC-BG-1** — NEW. Break-glass channel: second Tier 1 anchor (`break_glass_key_anchor`), M ≥ 3 quorum, physical-access injection, single-purpose `CAK_ROTATION_EMERGENCY`, `TRUST_ROOT_LOST` terminal double-compromise state. Partially closes OQ-S-CAK-1. GAP-42. §23.3.

**Genesis Initiation / Hold Interaction (GS10; GS11):**
- **IC-GIB-1** — NEW. `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` (INTEGRITY, sync, W1) + `GENESIS_INITIATION_ABUSE_PATTERN` (SECURITY, aggregate, ≥ 3 in 60min). Neither W3-eligible per C-W3-1. GAP-44.
- **IC-RP-1** — NEW. `RETENTION_PRUNING` ceremony type + `artifact_retention_manager` role. GAP-47.

**Rotation Registry / Boot-Time Validation (GS11):**
- **IC-CAK-IDENTITY** — NEW. Stable external `operator_id` bound at first-boot CAK registration; carried unchanged across rotation. Closes T-S4-N1. GAP-46.
- **IC-BOOT-RLRF** — NEW. Boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation: per-initiator and per-agent rate-limit intervals strictly less than corresponding Ledger-entry minimum retention windows. Closes T-S7-N1. §13.5 step 5a. GAP-46.
- **IC-HOOK-BOOT** — NEW. Boot-time hook binary hash verification against Tier 2 `hook-registry/v1`. `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) on mismatch. §13.5 step 4a. GAP-54.

**Constitutional Tests / Sandbox (GS12):**
- **IC-CLK-META** — NEW. `clock_stub_required` flag required on every constitutional test nomination. Declarative attestation. GAP-39.
- **IC-CLK-SANDBOX** — NEW. Sandbox synthetic-clock injection mandatory when `clock_stub_required=true`; missing injection → `SANDBOX_CONFIG_ERROR` (not test failure). GAP-39.
- **IC-NOM-DRYRUN** — NEW. Nomination-time declarative attestation + dry-run sufficient for v1.2 Q-gate evidence (closes OQ-V9). GAP-39.

**External Document Provenance (v3 GS9 — GAP-11):**
- **IC-EXT-PROV1** — NEW. Write engine patch validation: `external_provenance` block required for Layer 4 external facts; absence → `LAYER4_MISSING_PROVENANCE` (UNRECOVERABLE). §26.5.
- **IC-EXT-PROV2** — NEW. Pruning Agent `external_source_audit` → Ledger: `EXTERNAL_PROVENANCE_STALE` / `EXTERNAL_PROVENANCE_UNAVAILABLE` advisory (CONSISTENCY, async). `EXTERNAL_AUDIT_SUSPENDED` on N consecutive network failures (default N=5). §26.5.

**Ledger Retention (v3 GS9 — GAP-12):**
- **IC-RETENTION1** — NEW. PROJECT_CLOSED + FINAL_STATE_SNAPSHOT paired atomic commit. §27.4, §27.6.
- **IC-RETENTION2** — NEW. Archive-manifest restore path: seven-step verification (manifest self-hash → signer identity → payload hash → decompress → Merkle root → chain-link continuity → expose as read-only query layer). §27.3, §27.6.

**Review Queue (GS11 — T-PM-vs-PA):**
- **IC-REVIEW-QUEUE (amended)** — Merged-queue policy: external-provenance advisories merge into the existing review queue item for the same `edge_id`. CORE-importance facts with STALE or UNAVAILABLE provenance receive priority elevation; both advisory reasons must be acknowledged. §15.1.

**Corpus Authorship (GS8; v2 GS9):**
- **IC-CORPUS-AUTH (amended A12)** — `expires_at` predicate at submission ingress. §24.2.
- **IC-SL7 (amended A13)** — `contains_expired_author_cases` response field; `EXPIRED_AUTHOR_PRESENT` advisory flag on Meta-* Ledger result record. §24.2.
- **IC-SL8** — corpus manifest signing; delegates authorization to IC-SCOPE-AUTH-1.

**Deprecated / Superseded in v1.2:**
- **IC-SCOPE-UPDATE (v1.1 standalone authorization form)** — superseded by IC-SCOPE-AUTH-1 delegation. `operator_signature` field no longer standalone; now nested within CeremonyToken envelope.
- **`HOLD_RELEASE_SIGNATURE_INVALID`, `HOLD_RELEASE_REPLAY_REJECTED`** (Ledger entry types; A7b) — deprecated. Both collapse into the uniform IC-SCOPE-AUTH-1 failure set (`CEREMONY_AUTH_SIGNATURE_INVALID`, `CEREMONY_AUTH_REPLAY_REJECTED`).

