## Appendix C — Ledger Entry Type Catalog

Organized by audit category tag. v1.2 additions are marked `v1.2`. v1.0 and v1.1 entries are preserved verbatim from the v1.1 baseline; dispositions (DEPRECATED per A7b, AMENDED per A8 or A14) are attached inline.

**Category mapping note:** The catalog's audit categories — SECURITY, CONSISTENCY, VALIDATION, GOVERNANCE, LIFECYCLE — are the tags used by the Unified Ledger (§16). Every entry carries exactly one category tag. Writes under the W1 / W2 / W3 admission policy (§16.2, IC-W3-POLICY-1) reference this tag at admission time — carve-outs under `CIRCUIT_TRIPPED` are narrowed by category (IC-GCO-1) and the W3 emergency path (IC-LDG3) is restricted to the four ratified carve-outs documented at §16.2.

### SECURITY category

**v1.0 / v1.1 (preserved):**
- `TOKEN_ISSUED`, `TOKEN_CONSUMED`, `TOKEN_REJECTED`, `TOKEN_ABANDONED`
- `SCHEMA_MIGRATION_TOKEN_ISSUED`, `_CONSUMED`, `_REJECTED`, `_EXPIRED_UNUSED`
- `AGENT_SUSPENDED`, `AGENT_UNSUSPENDED`
- `ORCHESTRATOR_KEY_ANCHOR`
- `INTEGRITY_VIOLATION`, `INTEGRITY_VIOLATION_EMERGENCY`
- `YAML_BINDING_FAIL`, `CONFIG_INTEGRITY_FAIL`
- `SEALED_CORPUS_INTEGRITY_FAIL`
- `LARQL_VERSION_LEGACY` *(async advisory — legacy .larql syntax version, still within supported range; v1.1)*
- `VERSION_REJECTED` *(sync — Gate pre-check #8 hard rejection: absent or below-minimum version; v1.1)*
- `VERSION_UNSUPPORTED` *(sync — Gate pre-check #8: patch declares version above current; v1.1)*
- `SCOPE_UPDATE_REJECTED` *(sync — unsigned or invalid Write Scope Definition update attempt; v1.1)*
- `CORPUS_WRITE_REJECTED` *(sync for UNAUTHORIZED_AUTHOR reason; GOVERNANCE category for FORMAT_VIOLATION or DUPLICATE_CASE_ID; v1.1. **v1.2 AMEND:** adds `AUTHOR_EXPIRED` reason code per §24.2 / A12.)*
- `RETENTION_OVERRIDE_REJECTED` *(sync — retention shortening attempt blocked; v1.1)*
- `CONTENT_SPLIT_LOOP` *(async advisory — Coder Agent repeatedly resubmitting mixed-classification patches; v1.1)*
- `CIRCUIT_RESET_REJECTED` *(sync — failed reset ceremony attempt; v1.1; field amended per A2 — structured precondition-unmet reason code required; non-consumed CeremonyToken per GAP-35.)*

**v1.2 additions — Unified CeremonyToken failure set (GS4 / IC-SCOPE-AUTH-1):**
- `CEREMONY_AUTH_SIGNATURE_INVALID` *(sync, W1 — signature on CeremonyToken envelope fails verification against the current CAK anchor; §20.4 admission check 3.)*
- `CEREMONY_AUTH_REPLAY_REJECTED` *(sync, W1 — ceremony_id observed in prior Ledger entry; replay protection; §20.4 admission check 4.)*
- `CEREMONY_AUTH_KEY_EXPIRED` *(sync, W1 — CAK key material past expiration timestamp at verification time.)*
- `CEREMONY_AUTH_KEY_UNKNOWN` *(sync, W1 — `key_ref` resolves to no anchor in Tier 1.)*
- `CEREMONY_AUTH_WRONG_KEY` *(sync, W1 — ceremony signed by OOK or other key rather than CAK; dual-key invariant violation.)*
- `CEREMONY_AUTH_MALFORMED` *(sync, W1 — envelope fails structural validation.)*
- `CEREMONY_REJECTED_BURST_SUSPENDED` *(sync, W1 — ceremony received while CAK in BURST_SUSPENDED state per IC-CAKB-1 / §23.2.)*
- `CEREMONY_REJECTED_CIRCUIT_TRIPPED` *(sync, W1 — ceremony received under CIRCUIT_TRIPPED outside the IC-GCO-1 carve-out.)*
- `CEREMONY_REJECTED_TRUST_ROOT_LOST` *(sync, W1 — ceremony received after TRUST_ROOT_LOST entered; see §23.3.)*
- `CEREMONY_REJECTED_MULTI_CAUSE` *(sync, W1 — multiple rejection conditions simultaneous; carries ordered cause list for forensic clarity.)*

**v1.2 additions — CAK lifecycle (GS10 / §23.1):**
- `CAK_REGISTERED` *(sync, W2 bootstrap — first-boot CAK anchor record; fields: `operator_id`, `cak_public_key`, `anchor_hash`, `boot_manifest_ref`.)*
- `CAK_COMPROMISE_DECLARED` *(sync, W1 — operator declaration via standard ceremony path; triggers defensive posture.)*
- `CAK_COMPROMISED_AT_BOOT` *(sync, W1 — boot-time detection of tamper or anchor mismatch; triggers boot-suspend.)*
- `COMPROMISED_AT_BOOT` *(sync, W1 — generic boot-time compromise detection, distinct from CAK-specific variant above.)*

**v1.2 additions — Burst limit (GS10 / §23.2 / IC-CAKB-1):**
- `BURST_SUSPENDED` *(sync, W1 — CAK entered BURST_SUSPENDED state after exceeding N=5 ceremonies per 10-minute window.)*
- `CAK_BURST_LIMIT_EXCEEDED` *(sync, W1 — triggering event for BURST_SUSPENDED; same window boundary.)*
- `CAK_CEREMONY_BURST_EXCEEDED` *(alias — GS10 co-usage; identical semantics to CAK_BURST_LIMIT_EXCEEDED. [COUNCIL-FLAG: two names appear across GS10 source; recommend canonical spelling `CAK_BURST_LIMIT_EXCEEDED` and treat alias as dropped in final docs.])*
- `CAK_BURST_AUTO_CLEARED` *(async — 60-minute automatic clear of BURST_SUSPENDED state.)*
- `CAK_BURST_CLEARED` *(sync, W1 — Tier 1 explicit-clear ceremony; distinct from auto-clear.)*
- `RESET_WOULD_EXTEND_BURST` *(sync, W1 — advisory-path reset attempt that would re-start the burst window without clearing; rejected.)*

**v1.2 additions — Circuit reset rate (GS10 / IC-CRR-1 / GAP-36):**
- `CIRCUIT_RESET_REJECTED_RATE_EXCEEDED` *(sync, W1 — rate-limit breach N=5 / M=60min; advisory + operator alert.)*

**v1.2 additions — Genesis initiation (GS10 / IC-GIB-1 / GAP-44):**
- `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` *(sync, W1 — genesis initiation attempted while a Dependency Hold remains active from the pre-trip epoch.)*
- `GENESIS_INITIATION_ABUSE_PATTERN` *(aggregate — ≥ 3 blocked initiations in 60 minutes; not W3-eligible per C-W3-1.)*

**v1.2 additions — Hook registry (GS11 / IC-HOOK-BOOT / GAP-54):**
- `HOOK_INTEGRITY_VIOLATION` *(sync, W1 — boot-time hook binary hash mismatch against Tier 2 `hook-registry/v1`.)*

**v1.2 additions — Boot-time rate-limit / retention validation (GS11 / IC-BOOT-RLRF / GAP-46):**
- `RATE_LIMIT_RETENTION_CONFLICT` *(sync, W1 — per-initiator or per-agent rate-limit interval is not strictly less than the minimum retention window for its associated Ledger entry type. Closes T-S7-N1.)*

**v1.2 additions — Scope mismatch aggregate (GS12 / GAP-38):**
- `SCOPE_MISMATCH_AGGREGATE_ALERT` *(sync, W1 — aggregate threshold breached: N mismatches within window M, per Tier 1 `scope_mismatch_aggregate_threshold_n` and `_window_seconds`. Includes contributing-invocation list per IC-AGG-ALERT-LINK.)*
- `SCOPE_MISMATCH_ESCALATED` *(sync, W1 — per-invocation escalation after 2 consecutive `SCOPE_HASH_MISMATCH` errors per A4; routes to human review.)*
- `SCOPE_UPDATE_RATE_EXCEEDED` *(sync, W1 — per-`agent_id` rate-limit breach under `scope_update_min_interval_seconds`; check precedes signature verification per A6 / GS7 GAP-27 / D89.)*
- `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED` *(alias — GS10 variant spelling; identical semantics. [COUNCIL-FLAG: two names across source; recommend canonical `SCOPE_UPDATE_RATE_EXCEEDED`.])*

**v1.2 additions — Trust root lost (GS10 / §23.3 / IC-BG-1):**
- `TRUST_ROOT_LOST` *(sync, W1 — terminal double-compromise state declaration; both CAK and break-glass keys compromised. Harness refuses further ceremony acceptance.)*
- `TRUST_ROOT_LOST_ENTERED` *(alias / state-entry marker — may be paired with declaration entry for audit clarity.)*

**v1.2 additions — Reconciliation path (GS5 v3 / IC-SCOPE-RECONCILE):**
- `LEDGER_SIGNATURE_REVERIFICATION_FAILED` *(sync, W3 — tampering detection during post-boot scope-registry reconciliation. Routes through the SECURITY W3 emergency carve-out.)*
- `ORCHESTRATOR_UNAVAILABILITY_ESCALATED` *(sync, W3 — GS5 v3 D102 / IC-TC-RESET-DEGRADED: extended Orchestrator outage during reset ceremony. Narrow W3 carve-out; not W1. C-TC-RESET-DEG-1 through C-TC-RESET-DEG-3.)*

**v1.2 additions — Schema deprecation (GS5 v3 / D98):**
- `SCHEMA_DEPRECATION_ENACTED` *(sync, W1 — records deprecated-type → unified-successor map; historical deprecated entries remain chain-valid per C-DEPREC-1.)*
- `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF` *(sync, W1 — post-cutoff write of a deprecated type; integrity violation per C-DEPREC-2.)*

**v1.2 additions — External document provenance (§26 / GS9 v3 / GAP-11):**
- `LAYER4_MISSING_PROVENANCE` *(sync, W1 — Layer 4 external-source fact submitted without `external_provenance` block; UNRECOVERABLE at patch level per C-EXT-PROV1 / IC-EXT-PROV1.)*

**v1.2 additions — Bounded compensation violation (§11.8.1.1 / A1-REVISED):**
- `BOUNDED_COMPENSATION_VIOLATION` *(sync, W1 — compensation-under-READ_ONLY exceeded its bound per C-CRC-3; carries bound-type and observed-excess fields.)*

**v1.2 additions — Archive-key compromise / mismatch (GS11 / GAP-52):**
- `ARCHIVE_KEY_MATERIAL_MISMATCH` *(sync, W1 — restore-time mismatch between archive-manifest `signer_public_key_material` and Genesis Seal `ARCHIVE_KEY_SEALED` record.)*

### CONSISTENCY category

**v1.0 / v1.1 (preserved):**
- `PREPARED`, `COMMITTED`, `COMPENSATED`, `FAILED`
- `IMMUTABLE_ANCHOR`
- `ANCHOR_ESTABLISHED` (flag on qualifying `COMMITTED` entries)
- `COMPACTION_BEGIN`, `COMPACTION_BOUNDARY`, `COMPACTION_ABORT`
- `COMPACTION_BUNDLE_SEALED`, `SUPERSEDED_BUNDLE_EXPIRED`
- `LEDGER_EPOCH_ARCHIVED`
- `CHAIN_VERIFICATION_RESULT`
- `DEPENDENCY_CONFLICT_FLAGGED`
- `TIMED_OUT` *(sync — PREPARED-state timeout; fields: transaction_id, compensation_direction, trigger; v1.1)*
- `CIRCUIT_TRIPPED` *(sync — circuit breaker trip event; fields: `trip_type {CONSECUTIVE_FAILURE | CROSS_TASK_FAILURE | DIVERGED_STATE}`, `triggering_transaction_id`; v1.1. **v1.2 AMEND per A8:** adds `originating_category` field recording whether the signal that triggered the trip was INTEGRITY, CONSISTENCY, or SECURITY. Reset ceremony (IC-TC-RESET) selects its precondition branch using this annotation.)*
- `RECONCILIATION_COMPLETE` *(sync — full reconciliation run result; field: result {CONSISTENT | DIVERGED}; v1.1)*
- `COMPACTION_ABORTED` *(sync — compaction verification failure; payload: serialized CompactionProbeReport; v1.1)*
- `COMPACTION_PROBE_FAILED` *(sync — Behavioral Probe infrastructure failure during compaction, distinct from COMPACTION_ABORTED; v1.1)*
- `COMPACTION_CORPUS_SMALL` *(async advisory — probe corpus below sampling floor; v1.1)*

**v1.2 additions — Genesis-timeout pairing (GS10 / IC-MON-GTOTM / GAP-30):**
- `GENESIS_TIMED_OUT` *(sync — Genesis initiation exceeded `genesis_prepared_timeout`; triggers circuit-breaker trip in DIVERGED_STATE mode per IC-TC-TIMEOUT.)*
- `GENESIS_TIMEOUT_TRIP_MISSING` *(async, W1 — monitor-pairing check: `GENESIS_TIMED_OUT` observed without paired `CIRCUIT_TRIPPED` within bounded window; C-GTO-1 / C-GTO-2.)*

**v1.2 additions — Hold release / precursor (GS10 / GS11 / GAP-31 / IC-TC-PRECURSOR-QUERY):**
- `DEPENDENCY_HOLD_RELEASE_SIGNED` *(sync — CAK-signed Hold-release ceremony committed; GS5 v3 GAP-21 / D101.)*
- `DEPENDENCY_HOLD_RELEASED_SIGNED` *(alias — GS5/GS10 co-spellings. [COUNCIL-FLAG: both appear in source; recommend canonical `DEPENDENCY_HOLD_RELEASE_SIGNED`.])*
- `HOLD_RELEASE_REASON_UNWARRANTED` *(sync, W1 — operator-cited precursor fails Hold-coverage or audit-window check at admission time; IC-REL-PRECURSOR. W1 per C-W3-1, not W3.)*

**v1.2 additions — Manifest lattice completeness (GS10 / GAP-29a / IC-MANIFEST-1 Check 8):**
- `MANIFEST_LATTICE_INCOMPLETE` *(sync, W1 — manifest-lattice completeness verification failed at ratification.)*
- `MANIFEST_COMMIT_REJECTED` *(sync — pre-commit rejection at manifest submission; GS7 v3 / GAP-20.)*
- `MANIFEST_RATIFICATION` *(sync — successful manifest ratification ceremony; GS7 v3 / GAP-20. [COUNCIL-FLAG: verify placement — this may fit GOVERNANCE more naturally since it is a signed operator ceremony outcome. Kept in CONSISTENCY here pending clarification.])*

**v1.2 additions — Preserved scope binding on 2PC (GS10 / IC-PREPARE-SCOPE / GAP-34):**
- (Field addition, not new entry type) `PREPARED` and `COMMITTED` entries now carry `governing_scope_hash` field, captured at PREPARE and preserved at COMMIT. Nullable for pre-amendment entries.

**v1.2 additions — External document provenance (§26 / IC-EXT-PROV2):**
- `EXTERNAL_PROVENANCE_RECORDED` *(async — Layer 4 external-source patch commit replicating provenance metadata; fields include `patch_id`, `fact_triple_hash`, `ledger_seq`.)*
- `EXTERNAL_PROVENANCE_STALE` *(async advisory — Pruning Agent audit detected source-hash drift.)*
- `EXTERNAL_PROVENANCE_UNAVAILABLE` *(async advisory — Pruning Agent audit could not reach source.)*
- `EXTERNAL_AUDIT_SUSPENDED` *(async — N consecutive network failures in the audit sub-routine; audit paused while Git-side pruning continues per C-EXT-PROV3.)*

**v1.2 additions — Dry-run store (GS8 v2 / GS10 / IC-DRS-1 / IC-DRYRUN-1):**
- `DRY_RUN_ARTIFACT_STORED` *(async — operator-owned `.dry-run-store/` manifest-hash anchor written to Ledger.)*
- `DRY_RUN_ARTIFACT_PRUNED` *(async — retention-driven pruning of dry-run artifact after 37-day minimum.)*
- `DRY_RUN_STALE` *(sync — dry-run artifact older than freshness policy when referenced.)*
- `DRY_RUN_CORPUS_DRIFTED` *(sync — corpus state at dry-run differs from corpus state at submission.)*
- `DRY_RUN_SIGNATURE_INVALID` *(sync — executor signature on dry-run report fails verification.)*
- `DRY_RUN_TIME_CEILING_EXCEEDED` *(sync — time between dry-run and referencing ceremony exceeds ceiling.)*

**v1.2 additions — Write Lock lifecycle (GS10 / GS12 partial):**
- `WRITE_LOCK_VOLUNTARY_RELEASED` *(sync — v2-scope hint; v1.2 records event only for future-proofing. [COUNCIL-FLAG: v2 scope item per §19 — included for forensic completeness if emitted by operator tooling; no v1 code path produces this entry.])*
- `VOLUNTARY_WRITE_LOCK_RELEASE` *(alias form.)*
- `WRITE_LOCK_ABANDONED` *(sync — lock-holder agent abandoned scope; normal liveness recovery.)*

### VALIDATION category

**v1.0 / v1.1 (preserved):**
- Meta-Validator health records *(per-case; v1.1: `health_score` field is `NOT_COMPUTED` when corpus < 20 cases; includes `corpus_staleness_flag` and `corpus_size_at_run`.)*
- Meta-TGA health records *(per-case; same v1.1 extensions as Meta-Validator.)*
- Task gap records *(D37 Step 4.)*
- `CONSTITUTIONAL_FAILURE` *(v1.1 — constitutional test failure. **v1.2 AMEND per A14:** entry now carries a mandatory field pair — `invariant_statement` (copied from test metadata) + `failure_assertion_message` (captured verbatim from runtime). Both fields REQUIRED. No runtime comparison. §25 weak-check pattern.)*

**v1.2 additions — Sandbox / synthetic clock (GS12 / IC-CLK-SANDBOX / GAP-39):**
- `SANDBOX_CONFIG_ERROR` *(sync — constitutional test with `clock_stub_required=true` submitted to a sandbox configuration missing synthetic-clock injection; treated as a configuration error, NOT a test failure.)*

**v1.2 additions — Frozen judge model (GS12 / §21 L2 probe family):**
- `FROZEN_JUDGE_MODEL_BOOTSTRAPPED` *(sync — initial pin of frozen judge model at first boot.)*
- `FROZEN_JUDGE_MODEL_DRIFT_DETECTED` *(async — empirical drift observed against the frozen reference.)*
- `FROZEN_JUDGE_MODEL_WRITE_ATTEMPTED` *(sync, W1 — any attempted write path targeting the frozen judge model; structurally forbidden.)*

**v1.2 additions — Corpus init / staleness (GS8 v3 / D94 / D95):**
- `CORPUS_INIT_STATE` *(sync — Day-0 corpus initialization marker; emitted after the five preconditions pass.)*
- `HEALTH_SCORE_STALE` *(async advisory — corpus older than 180-day enforced floor; Meta-* result records emit companion `corpus_staleness_flag`.)*

**v1.2 additions — Forensic capture (GS10 / GS11):**
- `LEDGER_FORENSIC_EVIDENCE_CAPTURE` *(sync — point-in-time forensic snapshot reference committed to Ledger during incident response.)*
- `VINDEX_FORENSIC_SNAPSHOT_REF` *(sync — `.vindex` overlay snapshot hash paired with forensic-capture entry.)*

### GOVERNANCE category

**v1.0 / v1.1 (preserved):**
- `CONFIG_UPDATE`
- `SEALED_CORPUS_UPDATE`, `SEALED_CORPUS_ACCESS`
- `RECONCILIATION_REVIEW_DECISION`
- `RECONCILIATION_BACKLOG_WARNING`, `RECONCILIATION_BACKLOG_CRITICAL`
- `CIRCUIT_RESET` *(sync — successful circuit breaker write resumption; fields: target_trip_entry_id, operator_id, preconditions_verified; GOVERNANCE category; v1.1. **v1.2:** authorized via CeremonyToken / IC-SCOPE-AUTH-1 per A3.)*
- `SCOPE_UPDATED` *(sync — Write Scope Definition updated; v1.1 fields: previous_scope_hash, new_scope_hash, operator_signature, affected_agent_ids. **v1.2 AMEND per A9:** `ceremony_token_id` replaces standalone `operator_signature` field.)*
- `CORPUS_CASE_ADDED` *(async — corpus case successfully appended; fields: case_id, author_id, corpus_target, new_corpus_size; v1.1)*
- `RETENTION_OVERRIDE_EXTENDED` *(sync — retention period extended; operator-signed; v1.1. v1.2: delegates authorization to IC-SCOPE-AUTH-1 / ceremony_type `RETENTION_EXTEND`. See also `LEDGER_RETENTION_EXTENDED` below.)*

**v1.2 additions — Unified ceremony lifecycle (GS4 / IC-SCOPE-AUTH-1):**
- `CEREMONY_ACCEPTED` *(sync — CeremonyToken admitted; common success marker across all GOVERNANCE-class ceremonies.)*
- `CEREMONY_KEY_ANCHOR` *(sync, W2 bootstrap — initial CAK anchor record; parallel to `ORCHESTRATOR_KEY_ANCHOR`.)*
- `CEREMONY_KEY_ROTATION_COMPLETE` *(sync — successful CAK rotation ceremony; carries previous_key_ref and successor anchor.)*
- `CEREMONY_KEY_ROTATION_OVERDUE` *(sync — 365-day rotation ceiling reached without rotation.)*
- `CEREMONY_KEY_STALE` *(sync — 450-day degraded-mode threshold reached; ceremonies still accepted but each emits this entry.)*
- `CEREMONY_KEY_COMPROMISE_DECLARED` *(sync, W1 — operator declaration via ceremony; triggers defensive posture. Parallel to `CAK_COMPROMISE_DECLARED`.)*
- `CEREMONY_REPLAY_REJECTED` *(deprecated alias — see `CEREMONY_AUTH_REPLAY_REJECTED` in SECURITY; retained for transitional compat.)*
- `CEREMONY_SIGNATURE_INVALID` *(deprecated alias — see `CEREMONY_AUTH_SIGNATURE_INVALID` in SECURITY; retained for transitional compat.)*

**v1.2 additions — Scope-update aggregate advisories (GS12 / GAP-38):**
- `SCOPE_UPDATE_ACCEPTED` *(sync — ceremony admitted successfully; GS5 v3 companion to `SCOPE_UPDATED`.)*
- `SCOPE_UPDATE_AGGREGATE_ADVISORY` *(async — aggregate-volume advisory under threshold.)*
- `SCOPE_UPDATE_AGGREGATE_WARNING` *(sync — aggregate volume approaching `SCOPE_MISMATCH_AGGREGATE_ALERT` threshold.)*

**v1.2 additions — Calibration (§22 / GS7 v3 / GS8 v2):**
- `CALIBRATION_RATIFICATION` *(sync — `larql_fidelity_calibration` artifact ratified via CeremonyToken; new ceremony type.)*

**v1.2 additions — Retention (§27):**
- `LEDGER_RETENTION_EXTENDED` *(sync — Tier 1 authority CAK-signed ceremony; `new_floor_years > old_floor_years` required by construction. Ceremony-type `RETENTION_EXTEND` under IC-SCOPE-AUTH-1.)*
- `LEDGER_ACTIVE_PERIOD_UPDATED` *(sync — Tier 3 operator ceremony updating hot-storage window; reduction permitted within 30-day floor.)*
- `PROJECT_ARCHIVED` *(sync — async-dispatched archive ceremony completed; pairs with manifest per IC-RETENTION2.)*
- `PROJECT_ARCHIVE_PENDING` *(sync — PROJECT_CLOSED committed but archival I/O unavailable; 30-day SLA clock started.)*
- `ARCHIVE_KEY_SEALED` *(sync — archive-signing key material sealed at Genesis Seal during initial setup; cross-check anchor for restore path per GAP-52.)*

**v1.2 additions — Retention pruning (GS10 / IC-RP-1 / GAP-47):**
- `RETENTION_PRUNING` *(sync — retention-pruning ceremony under `artifact_retention_manager` role; new ceremony type.)*

**v1.2 additions — Legacy extension grant (GS7 v3 / GAP-20):**
- `LEGACY_EXTENSION_GRANTED` *(sync — operator grant extending legacy-larql-version support window; Tier 3 governance decision.)*

**v1.2 additions — Stale-fact refresh (GS13 / IC-SFR-1 / OQ-SC3 resolution):**
- `STALE_FACT_REFRESH_REQUESTED` *(sync — Pruning Agent initiates refresh ceremony upon detecting `EXTERNAL_PROVENANCE_STALE`. CORE-tier facts automatically attach `REQUIRES_HUMAN_REVIEW` flag per C-SFR-4.)*
- `STALE_FACT_REFRESH_APPROVED` *(sync — operator approval via Reconciliation Review Queue; dispatches Coder Agent with refresh scope.)*
- `STALE_FACT_REFRESH_REJECTED` *(sync — operator declines refresh; fact remains STALE with advisory flag per D101.)*
- `STALE_FACT_REFRESH_DEFERRED` *(sync — operator defers decision with reason; no action taken; fact remains STALE.)*

**v1.2 additions — Operator identity / recovery (GS11 / IC-CAK-IDENTITY):**
- `OPERATOR_IDENTITY_REGISTERED` *(sync — stable external `operator_id` bound at first-boot CAK registration; carried unchanged across rotation. Closes T-S4-N1.)*
- `OPERATOR_RECOVERY_ACTION_LOGGED` *(sync — recovery-ceremony metadata record for post-incident audit.)*

**v1.2 additions — Genesis review (GS7 v3):**
- `GENESIS_REVIEW_DECISION_AI` *(sync — Architect Agent's drafted manifest review outcome; non-authoritative informational record, does not grant ratification authority per D-GAP1-B.)*

**v1.2 additions — Break-glass (GS10 / §23.3 / IC-BG-1):**
- `BREAK_GLASS_ACTIVATED` *(sync, W1 — break-glass channel single-purpose `CAK_ROTATION_EMERGENCY` ceremony committed via the second Tier 1 anchor and M ≥ 3 quorum.)*
- `CAK_ROTATION_EMERGENCY` *(sync — completion record of the emergency CAK rotation; pair with `BREAK_GLASS_ACTIVATED`.)*

**v1.2 additions — OOK lifecycle (GS11 / GS12):**
- `OOK_ROTATED` *(sync — Orchestrator Operator Key rotation completion. [COUNCIL-FLAG: source material shows this emitted from both GOVERNANCE and LIFECYCLE contexts; placed in GOVERNANCE here to pair with the CAK-rotation entries; if implementation treats it as pure lifecycle, move to LIFECYCLE category.])*

### LIFECYCLE category

**v1.0 / v1.1 (preserved):**
- `TASK_DECOMPOSED`
- `DEPENDENCY_HOLD_PLACED`, `_RENEWED`, `_RELEASED`, `_EXPIRED_UNCLAIMED`
- Scope Lock entries
- Compaction scheduling events
- `PROJECT_INITIATED` *(sync, W2 bootstrap — retention policy declaration, mint-once; fields: default_retention_policy, operator_signature; v1.1)*
- `PROJECT_CLOSED` *(sync — final epoch sealed, Ledger made read-only; v1.1 fields: operator_signature, final_epoch_id, archival_status {COMPLETE | PENDING}. **v1.2 AMEND per §27.4:** authorization delegated to IC-SCOPE-AUTH-1 ceremony_type `PROJECT_CLOSE`; paired atomically with `FINAL_STATE_SNAPSHOT` per IC-RETENTION1; archival dispatched asynchronously — `archival_status=COMPLETE` or `PENDING` reflects archive-ceremony outcome only after async completion, not at the moment of PROJECT_CLOSED commit.)*

**v1.2 additions — Final state snapshot (§27.4 / IC-RETENTION1):**
- `FINAL_STATE_SNAPSHOT` *(sync — carries Ledger chain tip hash and `.vindex` snapshot hash at close; atomic pair with `PROJECT_CLOSED`.)*

**v1.2 additions — Archive SLA (§27.4):**
- `PROJECT_ARCHIVE_SLA_BREACHED` *(sync, W1 — 30-day default SLA for resolving `PROJECT_ARCHIVE_PENDING` expired without `PROJECT_ARCHIVED` emission. [COUNCIL-FLAG: §27.4 text places this as LIFECYCLE sync W1; if the intended semantic is a governance/operational-incident record, consider GOVERNANCE category. Kept as LIFECYCLE per §27.4 verbatim.])*

**v1.2 additions — Genesis initiation ceremony (GS10):**
- `GENESIS_INITIATION` *(sync — Genesis initiation ceremony committed; distinct from Genesis Seal event.)*

**v1.2 additions — Expired-author advisory flag (§24.2 / A13):**
- `EXPIRED_AUTHOR_PRESENT` *(flag on Meta-* Ledger result record — not a standalone entry type. Additive to existing Meta-* health-record entries per A13.)*

### Deprecated in v1.2 (per A7b — unified-failure-set collapse)

The following v1.1 entry types are DEPRECATED and replaced by their unified-CeremonyToken counterparts in the SECURITY category. Historical entries of these types remain chain-valid forever (C-DEPREC-1). Post-cutoff writes are integrity violations per C-DEPREC-2 and emit `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF`. Audit tools map deprecated entries to unified successors per C-DEPREC-3.

- `HOLD_RELEASE_SIGNATURE_INVALID` *(DEPRECATED; successor: `CEREMONY_AUTH_SIGNATURE_INVALID`.)*
- `HOLD_RELEASE_REPLAY_REJECTED` *(DEPRECATED; successor: `CEREMONY_AUTH_REPLAY_REJECTED`.)*

### Catalog scope notes

- **Running total:** The v1.2 catalog contains all v1.1 entries plus 50+ v1.2 additions spanning CeremonyToken failure modes (10), CAK lifecycle and burst state (8), hook / rate-limit / archive-key integrity (4), genesis-initiation blocking (2), scope-mismatch aggregate and rate (5), trust-root-lost (2), reconciliation-path failures (2), dry-run artifact lifecycle (6), manifest lattice and commit (3), provenance and staleness (4 + 4 refresh), retention governance (5), break-glass (2), deprecation machinery (2), calibration and legacy extension (2), and several miscellaneous operator / forensic entries.
- **Alias register.** Several entries have variant spellings across session sources (`DEPENDENCY_HOLD_RELEASE_SIGNED` vs. `DEPENDENCY_HOLD_RELEASED_SIGNED`; `CAK_BURST_LIMIT_EXCEEDED` vs. `CAK_CEREMONY_BURST_EXCEEDED`; `SCOPE_UPDATE_RATE_EXCEEDED` vs. `SCOPE_UPDATE_RATE_LIMIT_EXCEEDED`). Aliases are marked inline with [COUNCIL-FLAG] and recommended canonical names are noted. Implementation should pick one per pair and retire the other; aliases are documentation-only, not separate types.
- **Not catalogued here:** per-entry field schemas (JSON-schema-level). Those are documented inline with the interface contracts in Appendix B or in the source gap-session summaries. This catalog enumerates entry TYPES and their category placement only.

