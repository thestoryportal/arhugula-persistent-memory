## 18. Remaining Open Questions

### 18.1 Empirical / Post-Deployment Tuning

- **OQ-W1** — Cumulative edit volume degradation threshold (model-specific). All drift numbers (1,500 / 8,000 / 2,000 sub-batch) are provisional. The drift state interface shape is specced (IC-WE-1, D83); threshold values remain OQ-W1. Blocks OQ-OC3 calibration. Superset of GAP-1.
- **OQ-W2** — MEMIT/target model architecture compatibility verification.
- **OQ-W8** — Behavioral probe generalization beyond code domains. **PARTIALLY CLOSED** by §21 (L2 Probe Family — three sub-types, Semantic Assertion Criterion, three judgment methods, TGA authorship; GAP-9 / v2 GS10). Residual: threshold calibration per probe sub-type.
- **OQ-W-CALIB-1** — Numeric ε outputs of the `larql_fidelity_calibration` protocol (§22). Protocol structure is ratified (D-GS8-A); per-transform-class ε values, bucket boundaries for non-default BUCKET transforms, and derived M thresholds are implementation-phase. GAP-1, GAP-2, GAP-48 all roll up here.
- **OQ-W-PROBE-VERSION** — Probe set versioning for ε calibration. Probe-set evolution across Genesis updates is unspecified; if the probe set changes, historical ε values lose comparability (GAP-48 — GS13 scope).
- **OQ-V-JUDGE-THRESHOLD** — Threshold calibration for `judgment_method: judge_model_classification` in §21 probes — per-probe, per-domain, or global default (GAP-9 residual).
- **OQ-V-SELF-REF** — Self-referential probing: handling probes whose judge model is itself subject to `.vindex` writes (GAP-49 — GS13 scope).
- **OQ-OC3** — Compaction verification sampling calibration (failure report format and abort thresholds specced by D86, IC-OC-PROBE; sampling rates for SUPPORTING and INCIDENTAL tiers remain provisional pending OQ-W1 resolution).
- **OQ-CAKB-BURST** — Per-CAK burst-limit empirical validation. N=5 / 10-min is provisional; legitimate Genesis sequences under rapid-recovery debugging may exceed this (GAP-56 — GS13 scope; pre-ship modeling required).
- **T5 / T11** thresholds — async WAL flush cadence, verification intervals, backlog thresholds — starting heuristics.

### 18.2 Operational Policy

- **OQ-S5** — Minimum viable Genesis security for fully automated pipelines (v1 requires human review; full automation is v2 or operator policy).
- **OQ-S8** — Notification channels for integrity violations (email, Slack, logging — not spec).
- **OQ-V1** — Constitutional test failures as Tier 3 classification (policy). Mechanism (constitutional suite in Tier 2 sealed corpus) is specced; runtime tagging and promotion ceremony are not. **PARTIALLY CLOSED** by §25 (Q5 Weak-Check `CONSTITUTIONAL_FAILURE` with invariant_statement + failure_assertion_message field pair, A14).
- **OQ-V5** — PARTIALLY CLOSED by D88 (IC-CORPUS-AUTH), §24 expiry enforcement, and the `corpus-author-registry/` Tier 2 sealed corpus (GAP-8). Corpus extension cadence and authorship rotation policy remain operator-owned.
- **OQ-SC2** — Layer 4 recovery when originating external document unavailable. **PARTIALLY CLOSED** by §26 external document provenance (mandatory provenance block, advisory staleness, external_source_audit, IC-EXT-PROV1/2). Residual: stale-fact reconciliation workflow (OQ-SC3).
- **OQ-SC3** — Stale Layer 4 fact reconciliation workflow. Open; implementation-time decision per GS13 disposition.
- **OQ-W6** — PARTIALLY CLOSED at Gate enforcement layer (D81, D82, IC-GATE-8). Gate version pre-check (#8) and compaction versioned parser are specced. Remaining deferred to v2: migration path authorship, deprecation ceremony for old versions, multi-version team deployment.
- **OQ-CFG-TIER** — Tier placement conflict for rate-limit parameters participating in boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation. GAP-27 placed `scope_update_min_interval_seconds` at Tier 3; whether boot-participating parameters should migrate to Tier 1 is deferred (GS13 disposition).

### 18.3 Deferred to v2

- **OQ-CW1** — Voluntary scope-lock / Write Lock release and inter-agent negotiation (GAP-17).
- **OQ-SL2** — Multi-machine harness Ledger replication (GAP-18).
- **OQ-W6 (residual)** — `.larql` schema version migration path authorship, deprecation ceremony, multi-version team deployment.
- **OQ-GENESIS-AUTO** — Genesis automation (secondary LLM reviewer as human-review proxy) (GAP-13).
- **OQ-KEY-ROTATION** — OOK and CAK key rotation ceremonies with full dependency map (GAP-19). CAK rotation is a v2 deliverable; §23.3 break-glass is the v1.2 emergency substitute.
- **OQ-S-CAK-2** — T15 m-of-n CAK availability path (T15 v2; GAP-42 break-glass partially addresses OQ-S-CAK-1 in v1.2).
- **OQ-BATCH-HOLD** — T16 batch Genesis Hold release and multi-Hold ceremony scoping. Per-Hold model is the v1.2 path.
- **OQ-RATE-POLICY-EVOL** — Further scope-update rate-limit policy evolution beyond GAP-27 resolution (GAP-32).
- **OQ-SAMPLED-VERIFY** — Sampled-verification design for Ledger chains exceeding 10M entries (GAP-59; per GAP-53 documentation threshold).
- **OQ-RETIRED-KEY-META** — Retired-key revocation metadata semantics: retired-clean vs. retired-compromised classification for archive-bundle signing keys (GAP-60).
- **OQ-AGG-CONVENTION** — Formal framework convention for aggregate-detection entry types (always-SECURITY category, `source_entry_hash_list` field, cross-linked review queue item) (GAP-55; post-v1 integration pass).
- **OQ-PATH-DEPLOY** — Path-conditional deployment architecture for GAP-4 Path A/B/C, accounting for GAP-56 burst-limit density, GAP-57 per-operator binary, GAP-58 state-machine completeness per path. Activates on operator path selection.
- **OQ-TGA-SPLIT** — T-TGA-load v2-reconsider: TGA split into TGA-Test / TGA-Probe if v1.2 operation surfaces concrete failure-mode evidence.
- **OQ-DRS-CAS** — Content-addressed immutable storage for `.dry-run-store/` (T-S-RP-1 v2-flag; replaces metadata-only Warden audit with content-level immutability).

### 18.4 Closed in Integration

Closed during Session 7 synthesis (v1.0 → v1.1):
- **OQ-W5** — `attention_weight` authority (T1: two-number split model).
- **OQ-V2** — Retry budget reset per subtask (D73: fresh per subtask, aggregate cap preserved).
- **OQ-V3** — TGA test validation (T2: four-layer cascade).
- **OQ-S1** — Prompt injection ownership (D38: two-layer sequential).
- **OQ-S2** — Token revocation (T5: agent-suspension-flag model).
- **OQ-S3** — Validator write authority (D39: no authority, Commit Executor pattern).
- **OQ-S6** — Genesis seal storage (D49: dual-store).
- **OQ-S7** — Audit queryability (T11: tiered read-access).
- **OQ-SL3** — Agent ledger access (T11: restricted to own-identity).
- **OQ-TC2** — Infrastructure failures vs. retry budget (D67: independent).
- **OQ-TC3** — Consistency status exposure (D75: Orchestrator-mediated API).
- **OQ-GOC1** — Path classification storage (D76: Tier 3 Anchored Git Config).
- **OQ-CW2** — Lock visibility (D78: Orchestrator-mediated only).
- **OQ-OC1** — Idle-window detection (D79: Orchestrator-internal heuristic).
- **OQ-TPC2** — Human abort authority (D74: compensation path, no process-kill).
- **OQ-W10** — Compaction strategy (D62: full MEMIT re-run mandated).

Closed during IC Review Session (v1.1):
- **OQ-TC1** — Circuit breaker reset authority (D84: signed ceremony with independent TC precondition verification; IC-TC-RESET). READ_ONLY automatic on trip; write resumption via ceremony only.
- **OQ-TPC1** — PREPARED-state timeout value (D85: two-value model — `incremental_prepared_timeout` default 2 hours; `genesis_prepared_timeout` no default, Gate-blocked if absent; IC-TC-TIMEOUT).
- **OQ-S4** — Scope version management across long-running projects (D87: mid-flight update model; `SCOPE_HASH_MISMATCH` error code defined; superseded by §20 CeremonyToken model).
- **OQ-SL1** — Full Ledger retention policy (D89: immutable-downward model; `PROJECT_CLOSED` ceremony; archival format versioned `"1.0"`; IC-LDG-RETAIN; extended by §27).

Closed during Phase 2 gap sessions (v1.1 → v1.2):
- **OQ-S-CAK-1** — CAK availability when primary CAK compromised — PARTIALLY CLOSED by §23.3 break-glass (GAP-42 / GS10). Residual m-of-n variant is OQ-S-CAK-2 (v2).
- **OQ-V9** — Validator nomination-time attestation for constitutional tests — CLOSED by GAP-39 / GS12 (nomination-time declarative attestation + dry-run sufficient for v1.2; IC-CLK-META, IC-CLK-SANDBOX, IC-NOM-DRYRUN).
- **T-S4-N1 / T-S7-N1** — Rotation registry ordering + rate-limit derived-vs-primary state — CLOSED by GAP-46 / GS11 (IC-CAK-IDENTITY, IC-BOOT-RLRF).
- **T-SC-W-2** — Write suspension vs. governance-ceremony write — CLOSED by GAP-37 / GS10 (IC-GCO-1).
- **T-PM-vs-PA** — Provenance Monitor vs. Pruning Agent advisory queue priority — CLOSED by GS11 merge policy (IC-REVIEW-QUEUE amended).
- **T-TGA-load** — TGA authority concentration — CLOSED (Accepted) by GS12; v2-reconsider flag set.

