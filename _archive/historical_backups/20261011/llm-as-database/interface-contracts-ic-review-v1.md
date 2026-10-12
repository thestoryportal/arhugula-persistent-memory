# LLM as Database: Agent Harness Architecture
## Interface Contract Review — Amendment Bundle v1.0

> **Document type:** Spec amendment bundle — interface contract definitions and targeted insertions.
> **Version:** 1.0
> **Iteration:** Post-Session 7 / Gap Backlog IC Negotiation — Post-Council Review Session
> **Status:** Draft — pending operator ratification
> **Supersedes:** Nothing. All insertions are additive to `llm-as-database-v1_0-integrated-spec.md`.
> **Basis:** Framework Council Interface Contract Review Session (Post-Session 7). Addresses
> T3 (partial), T5 (partial), T6 (interface shape), T9 (partial), T11 (partial), T12 (unlocatable).
> Gaps addressed: GAP-1 (interface shape only), GAP-3, GAP-5, GAP-6, GAP-7, GAP-8, GAP-12, GAP-15.
> **Specialist provenance:** All six specialists. Primary: MEMIT Specialist, State Consistency
> Theorist, Warden (AISecOps), Validation Contract Architect. Secondary: Graph Data Architect,
> Orchestration Comparativist.
> **New gaps introduced:** GAP-20.

---

## How to Apply This Bundle

Each section below defines one interface contract and specifies its **precise insertion target**
in `llm-as-database-v1_0-integrated-spec.md`. The insertion target states:

- The section heading and line context for new prose or subsection insertions.
- The appendix entry location for Appendix B (Interface Contract Index), Appendix C (Ledger
  Entry Type Catalog), and Appendix F (Decision-to-Session Cross-Reference).

Insertions are additive. No existing section text is to be removed unless explicitly marked
**(REPLACE)** — all existing decisions, constraints, and open questions retain their IDs and
prose. New decisions are assigned D81–D90. New constraints use domain-prefixed form per the
ID conventions established in Sessions 5–6.

Apply insertions in document order (§8 before §9, §9 before §10, etc.) to avoid numbering
drift during the editing pass.

---

## Provisional Decision Assignments

| ID | Content | Closes / Partially Closes |
|----|---------|--------------------------|
| D81 | `.larql` patches carry mandatory `larql_syntax_version` header field. Gate pre-check #8 defined. | GAP-3 (Gate enforcement layer) |
| D82 | Gate returns `LARQL_VERSION_LEGACY` on legacy-but-supported versions; `VERSION_REJECTED` / `VERSION_UNSUPPORTED` on hard mismatches. Compaction re-run requires versioned patch parser with migration manifest in Tier 1 config. | GAP-3 (compaction path) |
| D83 | Write Engine exposes queryable `drift_state` object to Transaction Controller. Drift tier classification applied by write engine against config thresholds. Drift counter must reconcile with Ledger-computed count within 5% tolerance. | GAP-1 (interface shape) |
| D84 | Circuit breaker reset requires signed operator ceremony plus independent TC precondition verification. TC enters READ_ONLY automatically on trip; write resumption requires ceremony. | GAP-6 |
| D85 | PREPARED-state timeout split: incremental default 2 hours, Genesis no default (must be operator-set, Gate blocks Genesis initiation if absent). Genesis timeout trips circuit breaker (DIVERGED_STATE type). Dependency Hold persists through timeout. | GAP-7 |
| D86 | Compaction verification probe failure report is structured `CompactionProbeReport` with stratified sampling and abort thresholds: CORE 100%, SUPPORTING ≥95%, INCIDENTAL ≥80%. | GAP-15 (failure report format) |
| D87 | Write Scope Definition updates are accepted mid-flight (no drain required). Gate returns `SCOPE_HASH_MISMATCH` (distinct from generic infrastructure failure) with current scope hash in payload. Active PREPARED transactions not interrupted. | GAP-5 |
| D88 | Corpus authorship is role-restricted via `corpus_author_identities` in Tier 1 config. Minimum viable corpus 20 cases. Staleness flag at 90 days without new cases. Case formats formally defined. | GAP-8 |
| D89 | Ledger retention is immutable-downward: only extensible, never shortenable post-initiation. `PROJECT_CLOSED` is a signed ceremony. Archival format is gzip + operator-signed SHA-256 manifest, format version `"1.0"`. | GAP-12 |
| D90 | T12 identified and resolved: `CONTENT_CLASSIFICATION_MIXED` rejection protocol. Gate emits structured `split_guidance` payload. Gate is classification authority; Coder Agent declarations are informational only. | T12 (resolves unlocatable tension) |

---

## New Constraint Assignments

| ID | Content | Domain |
|----|---------|--------|
| C-GATE-1 | `larql_syntax_version` is a mandatory header field on every `.larql` patch. Absence is treated as version `"0.0"` and hard-rejected at Gate pre-check #8. | Gate |
| C-GATE-2 | `genesis_prepared_timeout` carries no default value. Gate MUST block Genesis initiation if this field is absent from Tier 1 config. | Gate / TC |
| C-OC3 | Any CORE-tier probe failure in compaction verification is an immediate compaction abort. No threshold tolerance for CORE regression. | Compaction |
| C-SL2 | Ledger retention policy is immutable-downward. A configured retention policy MUST NOT be shortened post-`PROJECT_INITIATED` without an explicit security review (itself currently unspecced; see GAP-20 extended scope). The exception to this clause does not apply; shortening is blocked at the Ledger layer regardless of operator instruction. | Ledger |
| C-GOC4 | Corpus authorship is role-restricted. Only identities listed in `corpus_author_identities` (Tier 1 config) may submit cases to Meta-* held-out corpora. No agent may author corpus cases. | Governance |
| C-WE-1 | The write engine drift counter MUST reconcile with the Ledger-computed edge count within 5% tolerance. Divergence exceeding 5% triggers an `INTEGRITY_VIOLATION` Ledger entry and write suspension. | Write Engine |

---

═══════════════════════════════════════════════════
## INTERFACE CONTRACT DEFINITIONS AND INSERTION TARGETS
═══════════════════════════════════════════════════

---

## IC-GATE-8 — `.larql` Schema Version Pre-Check

**Specialist provenance:** Graph Data Architect (primary), MEMIT Specialist, Warden (secondary)
**Tension origin:** GAP-3 (OQ-W6 Gate enforcement layer); T12 precondition
**Decision references:** D81, D82, C-GATE-1

### Contract Definition

```
INTERFACE CONTRACT IC-GATE-8: .larql Schema Version Pre-Check
  From:    Coder Agent (patch author)
  To:      Gate (pre-check layer, §10.2)

  What A exposes:
    A mandatory `larql_syntax_version` header field on every .larql patch file.
    Format: string, semver (e.g., "1.1"). Absence is treated as "0.0"
    (pre-versioning), which constitutes a version-below-minimum condition.

  Conditions:
    Gate pre-check #8 (appended to the existing seven pre-checks in §10.2):
    Gate reads `larql_syntax_version` from the patch header and compares
    against two harness-configured values stored in Tier 1 config:
    `min_supported_larql_version` and `current_larql_version`.

    Outcome matrix:
    - `larql_syntax_version == current_larql_version` → pass.
    - `larql_syntax_version` is ≥ `min_supported` AND < current → pass with
      LEDGER advisory entry `LARQL_VERSION_LEGACY` (SECURITY category, async).
      Compaction re-run MUST apply versioned translation on ingestion for
      this patch.
    - `larql_syntax_version` is absent OR below `min_supported_larql_version`
      → hard reject: error code `VERSION_REJECTED`. Patch is not forwarded to
      Validator. No retry budget consumed (infrastructure failure class per D67).
    - `larql_syntax_version` exceeds `current_larql_version` (forward version
      the harness cannot parse) → hard reject: error code `VERSION_UNSUPPORTED`.
      Operator alert flag set.

    Both `min_supported_larql_version` and `current_larql_version` are stored
    in Tier 1 config (`genesis-seal.json`) alongside existing anchor values.
    They are mint-once at bootstrap for `current_larql_version` and
    operator-updatable (signed ceremony, same as Tier 1 update procedure)
    for `min_supported_larql_version` when old versions are formally deprecated.

    Compaction re-run (MEMIT re-compile path per §8.10 / D62):
    Write engine MUST maintain a versioned patch parser. For patches in the
    superseded archive carrying `larql_syntax_version` below the current
    version, the parser applies per-version translation rules declared in Tier 1
    config as a `larql_migration_manifest` field (versioned mapping of field
    transformations, e.g., old `attention_weight` → new `declared_importance`).
    Translation failure on a superseded patch during compaction re-run → compaction
    aborts; existing overlays retained.

  Failure behavior:
    `VERSION_REJECTED`: Gate writes synchronous SECURITY-category Ledger entry
    with fields: {patch_id, declared_version, minimum_supported_version,
    current_version, rejection_reason: "VERSION_REJECTED"}. Coder Agent receives
    structured error including all three version values.
    `VERSION_UNSUPPORTED`: Same fields; additional field: operator_alert: true.
    Compaction translation failure: Gate is not involved. Transaction Controller
    writes `COMPACTION_ABORTED` with reason field `"version_translation_failure"`.
```

### Insertion Targets

**Target 1 — §8.5 (The `.larql` Canonical Format), line ~295–304**
After the sentence ending "every patch (`C-SC3`). Value `mixed` rejected pre-commit (`C-SC4`).",
add the following sentence at the end of §8.5:

> Every patch MUST carry a `larql_syntax_version` header field declaring the `.larql` syntax
> version under which it was authored (D81, C-GATE-1). Current version: `"1.1"` (incorporating
> the T1 two-number importance model). The Gate's version pre-check (§10.2 pre-check #8)
> enforces this field. Compaction re-run parsing of superseded patches across version boundaries
> requires the versioned patch parser and `larql_migration_manifest` declared in Tier 1 config (D82).

**Target 2 — §10.2 (The Patch Authorization Gate), line ~447–461**
The pre-checks list currently ends at item 7 ("Agent not in `suspended_agents` set.").
Append item 8 to the `**Pre-checks (T5, T7):**` list:

> 8. `larql_syntax_version` present and within supported range (D81). Absent or
>    below-minimum → `VERSION_REJECTED`. Above current → `VERSION_UNSUPPORTED`.
>    Between minimum and current → advisory `LARQL_VERSION_LEGACY` entry, patch proceeds (D82).

Also update the section header attribution from `**Pre-checks (T5, T7):**` to
`**Pre-checks (T5, T7, D81):**`.

**Target 3 — §8.10 (Anchor-Superseded Archive), line ~346–357**
Add after the sentence ending "Delta composition is rejected — it would skip the mandatory mathematical safeguards.":

> Compaction re-run MUST parse all active `.larql` patches through the versioned patch parser.
> Patches carrying a `larql_syntax_version` below the current version are translated via the
> `larql_migration_manifest` before passing to MEMIT compile. Translation failure aborts
> compaction (D82). The migration manifest is a Tier 1 config artifact; it is updated at the
> same time as `current_larql_version` whenever a `.larql` syntax version advance occurs.

**Target 4 — Appendix B (Interface Contract Index), Session 7 subsection, line ~1201**
Add after `IC-OR14`:

> **IC-GATE-8** — Gate pre-check #8: `larql_syntax_version` header validation. Rejects absent,
> below-minimum, and forward-version patches with distinct error codes. Advisory path for
> legacy-but-supported versions. Versioned parser required for compaction re-run (D81, D82).

**Target 5 — Appendix C (Ledger Entry Type Catalog), SECURITY category, line ~1231**
Add to SECURITY category:
> - `LARQL_VERSION_LEGACY` (async advisory — legacy patch version detected, still within supported range)
> - `VERSION_REJECTED`, `VERSION_UNSUPPORTED` (sync — Gate pre-check #8 hard rejections)

**Target 6 — §18.3 (Deferred to v2)**
Update the OQ-W6 entry:

**(REPLACE)** `- **OQ-W6** — .larql schema versioning strategy (v1 → v2 migration path has first-use case via T1 .larql format change).`

**(WITH):** `- **OQ-W6** — `.larql` schema versioning strategy: Gate enforcement layer and compaction re-run parser now specced (D81, D82, IC-GATE-8). Remaining deferred to v2: migration path authorship, deprecation ceremony for old versions, and multi-version deployment across a project team.`

---

## IC-WE-1 — Drift State Reporting

**Specialist provenance:** MEMIT Specialist (primary), State Consistency Theorist (secondary)
**Tension origin:** GAP-1 (OQ-W1 interface shape only — threshold values remain provisional)
**Decision references:** D83, C-WE-1

### Contract Definition

```
INTERFACE CONTRACT IC-WE-1: Drift State Reporting
  From:    Write Engine (drift counter, maintained internally)
  To:      Transaction Controller

  What A exposes:
    A queryable `drift_state` object, updated after each `COMMITTED` Ledger entry
    and reset to baseline after each `ANCHOR_ESTABLISHED` event. Fields:
      - `edge_count_since_anchor`: integer (raw drift count since last anchor)
      - `drift_tier`: enum { NOMINAL | WARNING | HARD | CRITICAL }
        Tier boundaries applied against current Tier 1 config threshold values.
        CRITICAL is triggered by overlay file count ≥ threshold OR p95 latency
        trigger, in addition to edge count thresholds.
      - `anchor_event_id`: Ledger entry ID of the most recent anchor event
        (for TC cross-reference and reconciliation).
      - `overlay_file_count`: integer (count of active .larql files, for
        the overlay-count compaction trigger).
      - `p95_latency_ratio`: float (current p95 inference latency divided
        by baseline established at last anchor, for the latency trigger).

  Conditions:
    Transaction Controller reads `drift_state` before issuing any new write
    token. Tier-to-action mapping:
    - `drift_tier == NOMINAL`: no action.
    - `drift_tier == WARNING`: TC writes CONSISTENCY-category advisory Ledger
      entry; compaction scheduling at next idle window; write tokens unblocked.
    - `drift_tier == HARD`: TC triggers compaction scheduling; write tokens for
      non-CORE tasks suspended pending compaction initiation.
    - `drift_tier == CRITICAL` (overlay count or latency trigger): TC escalates
      to circuit-breaker evaluation.

    Threshold values populating tier classification are sourced from Tier 1
    config. All threshold values remain provisional pending empirical validation
    against the target model (OQ-W1 remains open). Interface shape is ratified;
    values are not.

    Reconciliation check (C-WE-1): TC performs a spot reconciliation every 100
    `COMMITTED` entries (light verification interval per §16.4). Reconciliation
    computes Ledger-derived edge count since `anchor_event_id` and compares
    against `edge_count_since_anchor`. Tolerance: 5%. Divergence exceeding 5%
    triggers `INTEGRITY_VIOLATION` Ledger entry (SECURITY category, synchronous)
    and write suspension.

  Failure behavior:
    Write engine cannot report `drift_state` (internal error): TC treats as
    `drift_tier == HARD`. Conservative fail-safe — compaction scheduling triggered
    rather than write suspension, to avoid blocking work on instrumentation failure.
    Compaction itself failing cascades normally to the circuit-breaker path.
    Sustained `drift_state` unavailability (3 consecutive read failures): TC
    escalates to `drift_tier == CRITICAL`.
```

### Insertion Targets

**Target 1 — §8.7 (Drift-from-Anchor Thresholds), line ~315–328**
Add a new paragraph after "Deletions count toward drift the same as additions (absolute edge changes).":

> The Write Engine exposes a queryable `drift_state` object to the Transaction Controller,
> updated after each `COMMITTED` Ledger entry and reset to baseline after each
> `ANCHOR_ESTABLISHED` event (D83, IC-WE-1). Fields: `edge_count_since_anchor`,
> `drift_tier` (enum `NOMINAL | WARNING | HARD | CRITICAL`), `anchor_event_id`,
> `overlay_file_count`, and `p95_latency_ratio`. The TC reads `drift_state` before
> issuing any new write token; tier-to-action mapping is specified in IC-WE-1.
> Tier boundary values are sourced from Tier 1 config; all values remain provisional (OQ-W1).
>
> The drift counter MUST reconcile with the Ledger-computed edge count within 5% tolerance.
> Divergence exceeding this threshold triggers `INTEGRITY_VIOLATION` and write suspension (C-WE-1).

**Target 2 — §11.14 (Overlay Compaction), line ~662–676**
Update the first sentence under **Triggers (revised T9):** to read:

> Compaction trigger evaluation uses the `drift_state` object exposed by the Write Engine
> (IC-WE-1, D83). Trigger conditions (revised T9):

**Target 3 — Appendix B, Session 7 subsection**
Add after IC-GATE-8:
> **IC-WE-1** — Write Engine → Transaction Controller: `drift_state` object. Fields:
> `edge_count_since_anchor`, `drift_tier` (NOMINAL/WARNING/HARD/CRITICAL),
> `anchor_event_id`, `overlay_file_count`, `p95_latency_ratio`. Read before every
> new token issuance; reconciled every 100 COMMITTED entries within 5% tolerance (D83, C-WE-1).

---

## IC-TC-RESET — Circuit Breaker Reset Ceremony

**Specialist provenance:** State Consistency Theorist (primary), Warden (co-primary)
**Tension origin:** GAP-6 (OQ-TC1)
**Decision references:** D84, C-GATE-2 (adjacent)

### Contract Definition

```
INTERFACE CONTRACT IC-TC-RESET: Circuit Breaker Reset Ceremony
  From:    Human Operator (signed reset request artifact)
  To:      Transaction Controller

  What A exposes:
    A signed reset request artifact containing:
      - `reset_type`: enum { CONSECUTIVE_FAILURE | CROSS_TASK_FAILURE |
        DIVERGED_STATE } — MUST match the `trip_type` field of the target
        `CIRCUIT_TRIPPED` Ledger entry.
      - `operator_review_statement`: free-text attestation of diagnosis and
        remediation. Not machine-validated; required for auditability only.
      - `operator_signature`: signed with the operator key (same key used for
        schema migration tokens and Tier 2 sealed corpus updates).
      - `target_ledger_entry_id`: Ledger ID of the `CIRCUIT_TRIPPED` event
        this reset responds to. TC validates this ID exists in the Ledger
        before proceeding.

  Conditions:
    Automatic behavior on trip (no ceremony required):
    TC enters READ_ONLY mode immediately on `CIRCUIT_TRIPPED`. Inference and
    `.larql` query operations (reads) proceed normally. Write token issuance
    is suspended. Consistency Status API state transitions to `CIRCUIT_TRIPPED`
    (§12.5). No human action required to enter READ_ONLY.

    Reset ceremony — TC independent precondition verification before write
    resumption:

    For `reset_type == CONSECUTIVE_FAILURE` or `CROSS_TASK_FAILURE`:
    - MUST verify: compensation event for the triggering failure has
      `status == COMPLETED` in the Ledger.
    - MUST verify: current `.vindex` overlay hash matches the Ledger's most
      recent `COMMITTED` entry (no partial in-flight write remains).

    For `reset_type == DIVERGED_STATE`:
    - MUST verify: a `RECONCILIATION_COMPLETE` Ledger entry exists with
      timestamp after the `CIRCUIT_TRIPPED` timestamp.
    - MUST verify: the `RECONCILIATION_COMPLETE` entry carries
      `result: "CONSISTENT"`.

    Signature verification: operator key checked against the dual-store anchor
    (Ledger `ORCHESTRATOR_KEY_ANCHOR` + `.harness/orchestrator-key-anchor.json`).

    All preconditions met AND valid signature → TC exits SUSPENDED state, enters
    WRITE_ENABLED state. TC writes `CIRCUIT_RESET` Ledger entry (GOVERNANCE
    category, synchronous). Fields: {target_trip_entry_id, operator_id (derived
    from signature), preconditions_verified: true, timestamp}.

    Partial resume is automatic (READ_ONLY on trip; no ceremony). Write resumption
    requires full ceremony. The TC MUST NOT self-resume writes; only a valid signed
    reset request triggers WRITE_ENABLED.

  Failure behavior:
    Precondition verification fails: TC rejects request with structured error
    specifying which precondition failed and what must be true before resubmission.
    TC remains in SUSPENDED state. Ledger entry: `CIRCUIT_RESET_REJECTED`
    (SECURITY category, synchronous). Fields: {target_trip_entry_id,
    rejection_reason, failed_precondition_description}.

    Invalid operator signature: `CIRCUIT_RESET_REJECTED` with
    `rejection_reason: "SIGNATURE_INVALID"`. If this occurs ≥ 3 times within
    1 hour, TC writes an additional `INTEGRITY_VIOLATION` advisory entry
    (potential operator key compromise; Warden escalation).

    TC MUST NOT be reset via the W3 emergency Ledger write path. The signed
    operator ceremony is the exclusive mechanism for write resumption after a
    circuit-breaker trip.
```

### Insertion Targets

**Target 1 — §11.8 (Circuit Breaker — Transaction Controller), line ~590+**
*(Note: §11.8 is referenced in §11.7 at line ~586 but its full content may appear in a
subsection. Locate the section defining circuit-breaker trip conditions and reset.)*

After the existing circuit-breaker trip conditions, add a new subsection **§11.8.1 — READ_ONLY
Mode and Reset Ceremony**:

> **§11.8.1 — READ_ONLY Mode (Automatic) and Write Resumption Ceremony (D84)**
>
> On any circuit-breaker trip, the TC enters READ_ONLY mode immediately without human action.
> Inference, query, and read operations proceed normally; write token issuance is suspended.
> Consistency Status API state transitions to `CIRCUIT_TRIPPED` (§12.5).
>
> Write resumption requires a signed reset ceremony (IC-TC-RESET). The TC independently
> verifies preconditions before accepting any reset request — human attestation is not
> sufficient alone. For `CONSECUTIVE_FAILURE` and `CROSS_TASK_FAILURE` trips, TC verifies
> compensation is `COMPLETED` and current overlay matches the Ledger. For `DIVERGED_STATE`
> trips, TC requires a `RECONCILIATION_COMPLETE` Ledger entry with `result: "CONSISTENT"`
> timestamped after the trip. All preconditions met plus valid operator signature → TC writes
> `CIRCUIT_RESET` (GOVERNANCE, synchronous) and enters WRITE_ENABLED.
>
> Reset via the W3 emergency Ledger path is not permitted. The signed ceremony is exclusive.

**Target 2 — §18.2 (Operational Policy)**
**(REPLACE)** the OQ-TC1 entry (if present in §18) with:

> **OQ-TC1** — Circuit breaker reset authority: CLOSED by D84. Reset is a signed operator
> ceremony with independent TC precondition verification. See IC-TC-RESET and §11.8.1.

**Target 3 — Appendix B, Session 7 subsection**
Add:
> **IC-TC-RESET** — Human Operator → Transaction Controller: signed reset request artifact.
> TC verifies preconditions independently before accepting. Automatic READ_ONLY on trip; write
> resumption requires ceremony. W3 path excluded from reset authority (D84).

**Target 4 — Appendix C, CONSISTENCY category**
Add:
> - `CIRCUIT_TRIPPED` (sync — trip event; includes `trip_type` and triggering transaction ID)
> - `CIRCUIT_RESET` (sync — successful write resumption; GOVERNANCE category)
> - `CIRCUIT_RESET_REJECTED` (sync — failed reset attempt; SECURITY category)
> - `RECONCILIATION_COMPLETE` (sync — full reconciliation run result, `result: CONSISTENT | DIVERGED`)

**Target 5 — §18.4 (Closed in Integration)**
Add:
> - **OQ-TC1** — Circuit breaker reset authority (D84: signed ceremony with independent TC
>   precondition verification; IC-TC-RESET).

---

## IC-TC-TIMEOUT — PREPARED-State Timeout Behavior

**Specialist provenance:** State Consistency Theorist (primary), MEMIT Specialist (Genesis path)
**Tension origin:** GAP-7 (OQ-TPC1)
**Decision references:** D85, C-GATE-2

### Contract Definition

```
INTERFACE CONTRACT IC-TC-TIMEOUT: PREPARED-State Timeout Behavior
  From:    Transaction Controller (timeout monitor)
  To:      Write Engine, Orchestrator

  What A exposes:
    Two configurable timeout values stored in Tier 1 config:
      - `incremental_prepared_timeout`: default 2 hours. Applies to all non-Genesis
        2PC transactions.
      - `genesis_prepared_timeout`: NO DEFAULT. MUST be operator-set before Genesis
        initiation. Gate MUST block Genesis initiation if this field is absent from
        Tier 1 config (C-GATE-2).

  Conditions:
    Incremental patch PREPARED timeout triggered:
    1. TC writes `TIMED_OUT` Ledger entry (CONSISTENCY category, synchronous).
       Fields: {transaction_id, patch_id, time_in_prepared_state,
       compensation_direction, trigger: "PREPARED_TIMEOUT"}.
    2. TC executes Phase 1 rollback: Write Lock released. `.larql` patch status
       set to `COMPENSATED_TIMEOUT` in Ledger.
    3. `.vindex` overlay reverted to the snapshot hash recorded at transaction
       open (cross-referenced via `anchor_event_id` in IC-WE-1 drift state, or
       directly via the PREPARED Ledger entry hash field).
    4. Dependency Hold on the originating task PERSISTS. Task status set to
       `AWAITING_OPERATOR_RETRY`. The Hold prevents other tasks from acquiring
       the same write region during the uncertainty window.
    5. Retry: fresh token issuance required (infrastructure failure class per
       D67 — no retry budget consumed). The timeout event itself does not
       constitute a Reflexion retry.
    6. If the same task incurs PREPARED timeout 3 times: task escalated to human
       review queue (Correctness Review Queue per §15.1), flagged `repeated_timeout`.

    Genesis PREPARED timeout triggered:
    1. TC writes `TIMED_OUT` Ledger entry (CONSISTENCY category, synchronous)
       AND immediately writes `CIRCUIT_TRIPPED` with `trip_type: DIVERGED_STATE`
       (synchronous).
    2. Systemwide write suspension (READ_ONLY mode per IC-TC-RESET).
    3. TC does NOT auto-compensate. Partial compile state is preserved as
       forensic evidence; no automatic overlay rollback.
    4. Required operator path: (a) run full model integrity check against the
       pre-Genesis baseline hash recorded in `IMMUTABLE_ANCHOR` Ledger entry;
       (b) determine whether any partial weight writes occurred; (c) if partial
       writes confirmed, restore base model from pre-Genesis snapshot; (d) then
       proceed with the IC-TC-RESET signed ceremony.

    Interaction with Dependency Hold across timeout:
    Hold is placed at task declaration (pre-PREPARED). PREPARED timeout does not
    automatically release the Hold. The Hold MUST persist until either:
    - Successful commit on retry, OR
    - Explicit operator-signed Hold release (same ceremony as schema migration
      token — operator-signed, Ledger-recorded, GOVERNANCE category).
    This prevents other tasks from entering the uncertain write region during
    the timeout-to-retry window.

  Failure behavior:
    TC cannot write the `TIMED_OUT` Ledger entry (Ledger unavailable): TC enters
    W3 emergency path. `INTEGRITY_VIOLATION_EMERGENCY` written. Circuit breaker
    trips. No further writes until Ledger availability is restored.
    `genesis_prepared_timeout` absent from Tier 1 config at Genesis initiation:
    Gate issues hard rejection before Phase 1 admission. No PREPARED entry written.
    Agent receives `GENESIS_TIMEOUT_UNSET` error (infrastructure failure class).
```

### Insertion Targets

**Target 1 — §11.5 (Two-Phase Commit Protocol), line ~565–580**
Add a new subsection after the existing Phase 2 content:

> **§11.5.1 — PREPARED-State Timeout Behavior (D85)**
>
> Two configurable timeout values apply (both stored in Tier 1 config):
> `incremental_prepared_timeout` (default 2 hours) for all non-Genesis transactions,
> and `genesis_prepared_timeout` (no default; Gate blocks Genesis initiation if absent,
> C-GATE-2) for Genesis compiles.
>
> Incremental timeout: TC executes Phase 1 rollback, releases Write Lock, sets task to
> `AWAITING_OPERATOR_RETRY`. Dependency Hold persists through timeout. Retry requires fresh
> token (infrastructure failure class per D67). Three consecutive timeouts on the same task
> → human review queue escalation.
>
> Genesis timeout: circuit breaker trips immediately (`DIVERGED_STATE` type per IC-TC-RESET).
> No auto-compensation — partial compile state preserved for forensic investigation. Operator
> MUST run full model integrity check before the reset ceremony may proceed (IC-TC-TIMEOUT).

**Target 2 — §18.1 (Empirical / Post-Deployment Tuning)**
**(REPLACE)** the OQ-TPC1 entry:

> `- **OQ-TPC1** — PREPARED-state timeout value (decoupled from token TTL per T7; 2-hour working starting value).`

**(WITH):**
> `- **OQ-TPC1** — CLOSED by D85. Timeout split: `incremental_prepared_timeout` default 2 hours
>   (configurable); `genesis_prepared_timeout` has no default (must be operator-set; Gate blocks
>   Genesis initiation if absent). Genesis timeout trips circuit breaker (DIVERGED_STATE). Dependency
>   Hold persists through timeout. See IC-TC-TIMEOUT.`

**Target 3 — Appendix B, Session 7 subsection**
Add:
> **IC-TC-TIMEOUT** — Transaction Controller timeout monitor → Write Engine + Orchestrator:
> two-value timeout model (incremental default 2h; Genesis operator-set mandatory). Incremental
> timeout → Phase 1 rollback, Hold persists, retry as infrastructure failure. Genesis timeout →
> circuit breaker trips, no auto-compensation (D85, C-GATE-2).

**Target 4 — Appendix C, CONSISTENCY category**
Add:
> - `TIMED_OUT` (sync — PREPARED-state timeout; includes transaction_id, compensation_direction, trigger)
> - `AWAITING_OPERATOR_RETRY` (status tag on task record, not a standalone entry type — note for implementers)

**Target 5 — §18.4 (Closed in Integration)**
Add:
> - **OQ-TPC1** — PREPARED-state timeout value (D85: two-value model, incremental default 2h,
>   Genesis operator-set mandatory, IC-TC-TIMEOUT).

---

## IC-OC-PROBE — Compaction Verification Probe Report

**Specialist provenance:** Validation Contract Architect (primary), MEMIT Specialist (secondary)
**Tension origin:** T9 (partial, OQ-OC3); GAP-15
**Decision references:** D86, C-OC3

### Contract Definition

```
INTERFACE CONTRACT IC-OC-PROBE: Compaction Verification Probe Report
  From:    Behavioral Probe (compaction verification run)
  To:      Transaction Controller (compaction 2PC coordinator)

  What A exposes:
    A structured `CompactionProbeReport` returned at the end of the verification
    run, before Phase 2 of the compaction 2PC:
      - `total_probes_run`: integer
      - `sampling_method_applied`: object {
          CORE: "full" (100% of CORE edges probed),
          SUPPORTING: "stratified" (minimum 20% sampled, floor of 5 probes
            regardless of corpus size),
          INCIDENTAL: "stratified" (10% sampled, floor of 3 probes)
        }
      - `random_seed`: integer (logged for reproducibility; enables replication
        of the sample for audit or dispute resolution).
      - `results_by_tier`: object {
          CORE:       { total: int, passed: int, failed: int,
                        failed_edge_ids: [string...] },
          SUPPORTING: { total: int, passed: int, failed: int,
                        failed_edge_ids: [string...] },
          INCIDENTAL: { total: int, passed: int, failed: int,
                        failed_edge_ids: [string...] }
        }
      - `pass_rate_by_tier`: { CORE: float, SUPPORTING: float, INCIDENTAL: float }
      - `overall_verdict`: enum { PASS | ABORT }
        PASS requires ALL of: CORE pass_rate == 1.0 AND SUPPORTING pass_rate ≥ 0.95
        AND INCIDENTAL pass_rate ≥ 0.80. Any deviation → ABORT (C-OC3).
      - `probe_type`: literal "COMPACTION_REGRESSION" (distinguishes this probe
        class from incremental write acceptance probes in the Ledger and in §8.9).

  Conditions:
    TC receives `CompactionProbeReport` before Phase 2 of compaction 2PC.

    `overall_verdict == PASS` → TC proceeds to Phase 2 COMMIT.

    `overall_verdict == ABORT` → TC executes compaction rollback: new compacted
    overlay discarded, existing overlays retained, compaction Write Lock released.
    Ledger entry: `COMPACTION_ABORTED` (CONSISTENCY category, synchronous). The full
    `CompactionProbeReport` is serialized as the entry payload.
    CORE failures: all failed_edge_ids individually listed in the Ledger entry.
    SUPPORTING and INCIDENTAL failures: summary-logged (tier-level counts only)
    UNLESS failed_edge_ids ≤ 10, in which case all IDs are listed.

    Sampling method note: Stratification is within-tier proportional. For tiers where
    the corpus is smaller than the floor (e.g., fewer than 5 CORE edges at compaction
    time), TC logs `COMPACTION_CORPUS_SMALL` advisory entry (CONSISTENCY, async) and
    proceeds. The floor is a quality signal; it is not a hard gate.

    Sampling calibration: the 20% SUPPORTING floor, 10% INCIDENTAL rate, and per-tier
    abort thresholds (0.95, 0.80) are starting heuristics pending empirical calibration
    once drift/compaction frequency is empirically understood (OQ-OC3, blocked by OQ-W1).
    The CORE 100% requirement and the 1.0 pass-rate threshold are not provisional (C-OC3).

  Failure behavior:
    Behavioral Probe fails to complete (infrastructure error, probe timeout): TC treats
    as ABORT. Probe infrastructure failure logged as `COMPACTION_PROBE_FAILED`
    (CONSISTENCY, synchronous). Distinct from `COMPACTION_ABORTED` (content failure)
    for operator diagnostics.
    Compaction retry after abort: operator-authorized retry only (same ceremony as
    PREPARED-timeout retry — fresh token, no retry budget consumed).
    Version translation failure during compaction re-run (IC-GATE-8 path): also
    treated as ABORT with `COMPACTION_ABORTED` payload noting `abort_reason:
    "version_translation_failure"`.
```

### Insertion Targets

**Target 1 — §11.14 (Overlay Compaction), line ~662–676**
Extend the **Verification (D66):** paragraph. **(REPLACE):**

> `**Verification (D66):** full behavioral probe of all edges with `declared_importance = CORE`
> plus 10% random sample of others. Verification failure → compaction aborted, existing overlays
> retained, human review required.`

**(WITH):**
> **Verification (D66, extended D86):** Behavioral Probe returns a structured `CompactionProbeReport`
> to the TC before Phase 2 commit (IC-OC-PROBE). Sampling: 100% of CORE edges (full), ≥20% of
> SUPPORTING edges (stratified, floor 5), 10% of INCIDENTAL edges (stratified, floor 3). Random
> seed logged for reproducibility. Abort thresholds: CORE pass rate must equal 1.0 (C-OC3 — any
> CORE failure is immediate abort); SUPPORTING ≥95%; INCIDENTAL ≥80%. Abort → existing overlays
> retained, `COMPACTION_ABORTED` Ledger entry with serialized report payload. CORE failures
> individually listed; SUPPORTING and INCIDENTAL failures summary-logged unless ≤10 IDs.
> Probe failure (infrastructure) → `COMPACTION_PROBE_FAILED`. Both are distinct from success.
> All SUPPORTING and INCIDENTAL thresholds and sampling rates are provisional pending OQ-OC3
> / OQ-W1 calibration. CORE 1.0 threshold and C-OC3 are not provisional.

**Target 2 — §8.9 (Post-Write Verification)**
Add a note after the existing L1/L2 probe description:

> Compaction verification uses a distinct probe class (`probe_type: "COMPACTION_REGRESSION"`)
> that tests whether *previously encoded facts survived a recompile*, not whether a new fact was
> accepted. This probe is defined in IC-OC-PROBE and produces a `CompactionProbeReport` rather
> than the per-edge storage/behavioral probe signals of L1/L2.

**Target 3 — Appendix B, Session 7 subsection**
Add:
> **IC-OC-PROBE** — Behavioral Probe (compaction) → Transaction Controller: `CompactionProbeReport`
> struct. Stratified sampling; abort thresholds CORE 1.0 / SUPPORTING 0.95 / INCIDENTAL 0.80.
> CORE 1.0 is a hard constraint (C-OC3). Sampling rates provisional (OQ-OC3) (D86).

**Target 4 — Appendix C, CONSISTENCY category**
Add:
> - `COMPACTION_ABORTED` (sync — verification abort; serialized `CompactionProbeReport` as payload)
> - `COMPACTION_PROBE_FAILED` (sync — probe infrastructure failure, distinct from content failure)
> - `COMPACTION_CORPUS_SMALL` (async advisory — probe corpus below sampling floor)

---

## IC-SCOPE-UPDATE — Write Scope Definition Update Ceremony

**Specialist provenance:** Warden (primary), Orchestration Comparativist (co-primary)
**Tension origin:** T5 (partial, OQ-S4); GAP-5
**Decision references:** D87

### Contract Definition

```
INTERFACE CONTRACT IC-SCOPE-UPDATE: Write Scope Definition Update Ceremony
  From:    Orchestrator (scope update event) + Gate (mismatch reporting)
  To:      Gate (enforcement) + Orchestrator (recovery routing) + Agent (error receipt)

  What A exposes (two parts):

  Part A — Scope Update Ceremony (Operator → Orchestrator → Ledger):
    Write Scope Definition updates MUST produce, in order:
    1. Updated Tier 2 `write-scope-definitions/` entry (versioned additive
       directory, operator-signed manifest — identical mechanics to other Tier 2
       sealed corpus updates per §13.3).
    2. Synchronous GOVERNANCE-category Ledger entry: `SCOPE_UPDATED`. Fields:
       { previous_scope_hash, new_scope_hash, operator_signature, timestamp,
         affected_agent_ids: [list of agent IDs whose write_scope_hash bindings
         are now stale] }.
    3. Orchestrator updates its in-memory scope registry to the new hash.

    No drain of in-flight invocations is required. Scope updates are accepted
    mid-flight (D87). In-flight invocations carrying the stale scope hash will
    fail at Gate on token presentation; the recovery path (Part B) handles them.

    Scope update MUST NOT be accepted without a valid operator signature. An
    unsigned or incorrectly signed scope update attempt MUST produce
    `SCOPE_UPDATE_REJECTED` (SECURITY category, synchronous).

  Part B — Gate Mismatch Reporting and Orchestrator Recovery:
    When Gate pre-check step 4 (`write_scope_hash` mismatch) detects that an
    invocation token's `write_scope_hash` does not match the current authoritative
    scope hash, Gate MUST return error code `SCOPE_HASH_MISMATCH` — NOT the
    generic infrastructure failure code. This distinction MUST be preserved so
    the Orchestrator can route recovery correctly.

    `SCOPE_HASH_MISMATCH` error payload:
    { error: "SCOPE_HASH_MISMATCH",
      rejected_scope_hash: <hash from the submitted token>,
      current_scope_hash: <current authoritative scope hash>,
      scope_updated_at: <timestamp from the SCOPE_UPDATED Ledger entry> }

    Orchestrator recovery path on receiving `SCOPE_HASH_MISMATCH`:
    1. Orchestrator MUST NOT re-issue a token using the stale scope hash.
    2. Orchestrator issues a fresh token binding to the CURRENT scope hash.
    3. Agent is notified that re-invocation is required.
    4. No retry budget consumed (infrastructure failure class per D67).
    5. If Orchestrator receives 3 consecutive `SCOPE_HASH_MISMATCH` errors for
       the same invocation: escalate to human review queue — possible recovery
       loop or scope update ceremony failure.

    Active PREPARED transactions: a scope update issued while a 2PC transaction
    is in PREPARED state does NOT interrupt that transaction. The existing Write
    Lock and PREPARED entry remain valid to completion. The agent's NEXT token
    (issued after that transaction commits or compensates) will bind to the
    updated scope. Scope changes are forward-only.

  Failure behavior:
    `SCOPE_UPDATED` Ledger entry cannot be written (Ledger unavailable): scope
    update is rejected at the Orchestrator layer. Operator retries when Ledger
    is available. No Tier 2 file change occurs if the Ledger write fails — file
    write and Ledger entry MUST be atomic (both succeed or both are aborted).
    Unsigned scope update attempt: `SCOPE_UPDATE_REJECTED` (SECURITY, sync).
    If 3 unsigned attempts within 1 hour: additional `INTEGRITY_VIOLATION`
    advisory entry (potential unauthorized scope modification attempt).
```

### Insertion Targets

**Target 1 — §10.9 (Agent YAML ↔ Write Scope Definition Binding), line ~519–528**
Add a new paragraph at the end of §10.9:

> **Scope Update Ceremony (D87, IC-SCOPE-UPDATE)**
>
> Write Scope Definition updates are accepted mid-flight — no drain of in-flight invocations
> is required. An update MUST produce a `SCOPE_UPDATED` Ledger entry (GOVERNANCE, synchronous)
> before the Orchestrator's in-memory scope registry is updated. The entry carries
> `previous_scope_hash`, `new_scope_hash`, `operator_signature`, and `affected_agent_ids`.
>
> Any in-flight token whose `write_scope_hash` predates the update will fail at Gate pre-check
> step 4 with error code `SCOPE_HASH_MISMATCH` (distinct from generic infrastructure failure).
> The error payload includes `current_scope_hash` and `scope_updated_at`, enabling the
> Orchestrator to issue a corrected token without consuming the agent's retry budget. Active
> PREPARED transactions are not interrupted; scope changes are forward-only.

**Target 2 — §14.3 (Failure Mode Interaction with Retry Budget), line ~848–852**
Append a new row to the failure mode list:

> - **Scope hash mismatch (`SCOPE_HASH_MISMATCH`)** — infrastructure failure class. Gate
>   returns structured payload including `current_scope_hash`. Orchestrator re-issues token
>   against current scope. Retry budget not consumed. Distinct from generic hash-mismatch
>   infrastructure failure: recovery path uses the current scope hash, not simple re-issue (D87).

**Target 3 — §18.2 (Operational Policy)**
**(REPLACE)** the OQ-S4 entry:

> `- **OQ-S4** — Scope version management across long-running projects (partially addressed
> by Sealed Corpus pattern; full policy deferred).`

**(WITH):**
> `- **OQ-S4** — CLOSED by D87. Scope update serialization model resolved: mid-flight updates
>   accepted, `SCOPE_HASH_MISMATCH` error code defined, recovery path specified. Active PREPARED
>   transactions not interrupted. See IC-SCOPE-UPDATE.`

**Target 4 — Appendix B, Session 7 subsection**
Add:
> **IC-SCOPE-UPDATE** — Orchestrator + Gate: Write Scope Definition update ceremony. Mid-flight
> updates accepted; Gate returns `SCOPE_HASH_MISMATCH` (not generic) with current scope hash.
> Active PREPARED transactions not interrupted. Scope changes forward-only (D87).

**Target 5 — Appendix C, GOVERNANCE category**
Add:
> - `SCOPE_UPDATED` (sync — Write Scope Definition updated; fields: previous/new hashes, affected agent IDs)
> - `SCOPE_UPDATE_REJECTED` (sync — unsigned or invalid update attempt; SECURITY category)

**Target 6 — §18.4 (Closed in Integration)**
Add:
> - **OQ-S4** — Scope version management across long-running projects (D87: mid-flight update
>   model, IC-SCOPE-UPDATE).

---

## IC-CORPUS-AUTH — Meta-* Corpus Authorship

**Specialist provenance:** Validation Contract Architect (primary), Warden (co-primary)
**Tension origin:** T3 (partial, OQ-V5); GAP-8
**Decision references:** D88, C-GOC4

### Contract Definition

```
INTERFACE CONTRACT IC-CORPUS-AUTH: Meta-* Corpus Authorship
  From:    Designated Corpus Author (role-bound operator identity)
  To:      Sealed Corpus (Tier 2 artifact — `meta-validator-suite/` or
           `meta-tga-corpus/`)

  What A exposes:
    A signed corpus addition request containing:
      - `corpus_target`: enum { META_VALIDATOR | META_TGA }
      - `case`: object conforming to the target-specific format (see below).
      - `author_id`: identifier of the submitting corpus author.
      - `operator_signature`: signed with the corpus-author key.
        Corpus authorship is a restricted role: only identities listed in
        `corpus_author_identities` (a Tier 1 config field, C-GOC4) may submit.
        No agent identity MUST appear in `corpus_author_identities`. This
        restriction is enforced at the corpus write gate.

    Case format — Meta-Validator:
      { id: string (unique across corpus, operator-assigned),
        prompt: string,
        expected_assertion_set: [ AssertionPredicate... ]
          where AssertionPredicate = { type: string, value: any }
          Examples: { type: "contains", value: "X" },
                    { type: "excludes", value: "Y" },
                    { type: "matches_pattern", value: "regex_string" },
        expected_pass: boolean }

    Case format — Meta-TGA:
      { id: string (unique across corpus),
        specification_fragment: string,
        gold_test_set: [ GoldTestCase... ]
          where GoldTestCase = { test_name: string,
                                 assertion_count: int (≥ 2),
                                 asserts_symbols: [string...] } }

  Conditions:
    Corpus write gate validates in order:
    1. Signature against `corpus_author_identities` list (Tier 1 config).
    2. Case format structural conformance for the declared `corpus_target`.
    3. Assertion set non-trivial check: no bare `assert True`, no empty
       assertion sets, every assertion in `expected_assertion_set` MUST have
       both `type` and `value` populated. (Mirrors TGA L1 structural check per §9.4.)
    4. Unique ID check: submitted `id` MUST NOT collide with any existing ID
       in the corpus.

    All pass → case appended to corpus (versioned additive directory; manifest
    re-signed). Ledger entry: `CORPUS_CASE_ADDED` (GOVERNANCE category, async).
    Fields: { case_id, author_id, corpus_target, new_corpus_size }.

    Minimum viable corpus:
    Meta-Validator: 20 cases before Health Score is computed.
    Meta-TGA: 20 cases before Health Score is computed.
    Below minimum: Meta-* run proceeds (not blocked), but `health_score` field
    in the Ledger health record is set to `NOT_COMPUTED` rather than a numeric
    value. Ledger entry also carries `corpus_size_at_run` for operator awareness.

    Corpus staleness signal:
    If the most recent `CORPUS_CASE_ADDED` entry for the target corpus is
    more than 90 calendar days prior to the Meta-* run timestamp, the health
    record carries `corpus_staleness_flag: true`. This is an advisory signal;
    it does not gate the Meta-* run or alter the numeric Health Score.

    Corpus access timing (unchanged from T3 / §13.3):
    Corpora are time-bounded capability — accessible only during scheduled
    Meta-* runs, never during normal Validator or TGA operation. Submission
    (corpus write) is permitted outside run windows; access for probe execution
    is not.

  Failure behavior:
    Invalid signature (author not in `corpus_author_identities`):
    `CORPUS_WRITE_REJECTED` (SECURITY category, synchronous).
    Fields: { rejection_reason: "UNAUTHORIZED_AUTHOR", author_id }.
    Malformed case: `CORPUS_WRITE_REJECTED` with
    `rejection_reason: "FORMAT_VIOLATION"` and a structured error identifying
    the specific field(s) failing validation.
    ID collision: `CORPUS_WRITE_REJECTED` with
    `rejection_reason: "DUPLICATE_CASE_ID"` and the conflicting existing ID.
    Corpus access attempt outside a scheduled Meta-* run window:
    `CORPUS_ACCESS_DENIED` (SECURITY, synchronous). Time-bounded access is
    enforced at the sealed corpus access layer, not at submission.
    Corpus locked (Meta-* run currently in progress):
    `CORPUS_WRITE_REJECTED` with `rejection_reason: "CORPUS_LOCKED"`.
    Retry after Meta-* run completes.
```

### Insertion Targets

**Target 1 — §13.3 (Tier 2 — Sealed Artifacts), line ~773–793**
After the sentence "**Per-case audit reporting mandatory** for Meta-* runs (T3 closure of OQ-V5).
Aggregate-only reporting is forbidden.", add a new paragraph:

> **Corpus Authorship Model (D88, IC-CORPUS-AUTH)**
>
> Corpus authorship is a restricted operator role (C-GOC4). Only identities listed in
> `corpus_author_identities` (Tier 1 config field) may submit cases. No agent identity
> MUST appear in this list. Case formats are formally defined: Meta-Validator cases carry
> `(id, prompt, expected_assertion_set, expected_pass)`; Meta-TGA cases carry
> `(id, specification_fragment, gold_test_set)`.
>
> Minimum viable corpus: 20 cases before any Meta-* run produces a meaningful Health Score.
> Below minimum, the `health_score` field is `NOT_COMPUTED` (not zero — a zero score would
> be indistinguishable from a failed run). A corpus staleness flag is set if no case has been
> added in 90 days. Cadence is operator-owned policy, not enforced by this spec.

**Target 2 — §9.11 (Meta-Validator) and §9.4 (TGA Four-Layer Cascade, L4)**
In §9.11, after "Evaluated against a held-out human-authored suite per the Sealed Corpus pattern.",
add:

> Corpus authorship requirements and minimum viable corpus size are defined in IC-CORPUS-AUTH
> and §13.3 (D88). Health Score is `NOT_COMPUTED` when corpus is below 20 cases.

**Target 3 — §18.2 (Operational Policy)**
**(REPLACE)** the OQ-V5 entry:

> `- **OQ-V5** — Held-out corpus authorship cadence and authority (mechanism specced T3; policy deferred).`

**(WITH):**
> `- **OQ-V5** — PARTIALLY CLOSED by D88. Authorship role (role-restricted, C-GOC4), case formats
>   (Meta-Validator triple; Meta-TGA pair), and minimum viable corpus size (20 cases) now specced.
>   Corpus extension cadence remains operator-owned policy. See IC-CORPUS-AUTH.`

**Target 4 — Appendix B, Session 7 subsection**
Add:
> **IC-CORPUS-AUTH** — Corpus Author → Sealed Corpus (Meta-Validator / Meta-TGA): role-restricted
> submission with format validation. Minimum 20 cases for valid Health Score. Staleness flag at
> 90 days. Case formats defined (D88, C-GOC4).

**Target 5 — Appendix C, GOVERNANCE category**
Add:
> - `CORPUS_CASE_ADDED` (async — case successfully appended to sealed corpus; fields: case_id, author_id, new corpus size)
> - `CORPUS_WRITE_REJECTED` (sync — rejected submission; SECURITY category for UNAUTHORIZED_AUTHOR reason, GOVERNANCE for FORMAT_VIOLATION or DUPLICATE_CASE_ID)

**Target 6 — Appendix C, VALIDATION category**
Add:
> - `HEALTH_SCORE_NOT_COMPUTED` (status value in health record entries when corpus < 20 cases; not a standalone entry type)
> - Note: `corpus_staleness_flag: true` and `corpus_size_at_run` are fields on existing health record entries (IC24, IC-V-TGA2), not new entry types.

---

## IC-LDG-RETAIN — Ledger Retention Policy Interface

**Specialist provenance:** State Consistency Theorist (primary), Warden (secondary)
**Tension origin:** T11 (partial, OQ-SL1); GAP-12
**Decision references:** D89, C-SL2

### Contract Definition

```
INTERFACE CONTRACT IC-LDG-RETAIN: Ledger Retention Policy Interface
  From:    Operator (signed lifecycle governance events)
  To:      Ledger (retention enforcement and archival)

  What A exposes (three parts):

  Part A — Project Lifecycle Declaration (at first boot):
    `PROJECT_INITIATED` Ledger entry (LIFECYCLE category, synchronous, W2 bootstrap
    writer path — one-time). Fields:
      - `default_retention_policy`: object {
          unit: enum { DAYS | PROJECT_LIFETIME | INDEFINITE },
          value: int (if DAYS) | null (if PROJECT_LIFETIME or INDEFINITE)
        }
        Default if operator does not specify at bootstrap: PROJECT_LIFETIME.
      - `operator_signature`: signed with operator key.

    This entry is produced by the W2 bootstrap writer and is immutable post-mint.
    The retention policy declared here MUST NOT be shortened post-initiation
    without the extension ceremony (C-SL2). Shortening attempts are blocked at
    the Ledger layer; see Failure behavior below.

  Part B — Project Close Ceremony:
    `PROJECT_CLOSED` Ledger entry (LIFECYCLE category, synchronous). Fields:
      - `operator_signature`: signed with operator key.
      - `final_epoch_id`: ID of the last epoch being sealed.

    Effects:
    - Ledger becomes read-only after `PROJECT_CLOSED` is written and verified.
    - Final epoch is sealed and queued for archival per configured retention policy.
    - Archival to cold storage triggered: compressed (`gzip`) bundles, each
      carrying an operator-signed SHA-256 manifest. Archival format version field:
      `"1.0"` (for future forensic readability across schema versions).
    - If cold storage is unavailable at close time: Ledger remains in local storage;
      `PROJECT_CLOSED` is recorded with `archival_status: "PENDING"`. Archival is
      retried with exponential backoff. Ledger remains read-only even during
      PENDING state — PROJECT_CLOSED is write-final regardless of archival status.

  Part C — Retention Extension (optional, post-initiation):
    Operators MAY extend retention (e.g., DAYS → PROJECT_LIFETIME,
    PROJECT_LIFETIME → INDEFINITE) via `RETENTION_OVERRIDE_EXTENDED` (GOVERNANCE
    category, synchronous). Fields:
      - `old_policy`: object (previous retention policy, for audit).
      - `new_policy`: object (new policy; MUST be at least as long as old_policy).
      - `operator_signature`: signed with operator key.
      - `justification`: free-text (required for auditability; not machine-validated).

    Hard invariants enforced by the Ledger layer (C-SL2):
    - Retention MUST only be extended, never shortened.
    - Epochs containing any `INTEGRITY_VIOLATION` entry are INDEFINITE regardless
      of any configured retention policy. No operator override MUST ever shorten
      an `INTEGRITY_VIOLATION` epoch. This invariant is enforced unconditionally.
    - A shortening attempt (new policy shorter than old) MUST produce
      `RETENTION_OVERRIDE_REJECTED` (SECURITY category, synchronous) and set an
      operator alert flag. This applies even if the operator key signature is valid.

  Failure behavior:
    `PROJECT_CLOSED` without valid operator signature: rejected. Ledger remains
    active. `LIFECYCLE_VIOLATION` advisory entry written (SECURITY category).
    Archival failure (cold storage unavailable): `PROJECT_CLOSED` written with
    `archival_status: "PENDING"`. Ledger is read-only; archival retried independently.
    Retention shortening attempt (valid signature but shorter policy):
    `RETENTION_OVERRIDE_REJECTED` (SECURITY, sync). Fields: {rejected_policy,
    current_policy, rejection_reason: "RETENTION_SHORTENING_PROHIBITED"}.
    Retention shortening attempt with invalid signature: `RETENTION_OVERRIDE_REJECTED`
    with `rejection_reason: "SIGNATURE_INVALID"`. SECURITY escalation if ≥ 3 attempts
    within 1 hour.
```

### Insertion Targets

**Target 1 — §16.7 (Ledger Epoch Archival), line ~963–972**
**(REPLACE)** the existing §16.7 content with the following expanded version:

> **§16.7 — Ledger Epoch Archival and Retention Policy Interface (T11, D89)**
>
> Ledger entries older than the most recent `ANCHOR_ESTABLISHED` event are eligible for
> cold-storage archival at `<harness_root>/.state-ledger/archive/{epoch_bundle_N}/`.
> Parallels T9 compaction-epoch bundling.
>
> **Retention policy (IC-LDG-RETAIN):**
> Retention policy is declared at bootstrap via `PROJECT_INITIATED` (LIFECYCLE, W2 bootstrap
> writer, immutable post-mint). Default if not specified: PROJECT_LIFETIME.
>
> Retention is immutable-downward (C-SL2): once configured, it MUST NOT be shortened.
> Extensions (longer retention) are permitted via `RETENTION_OVERRIDE_EXTENDED` (GOVERNANCE,
> signed ceremony). The Ledger layer blocks any shortening attempt regardless of operator key
> validity.
>
> **Unconditional invariant:** Epochs containing any `INTEGRITY_VIOLATION` entry are retained
> INDEFINITELY, regardless of configured retention policy and regardless of any operator override.
>
> **Project close:** `PROJECT_CLOSED` (LIFECYCLE, signed ceremony) seals the final epoch and
> makes the Ledger read-only. Archival format: gzip bundles with operator-signed SHA-256 manifest,
> format version `"1.0"`. Archival pending (cold storage unavailable) does not defer read-only
> status — `PROJECT_CLOSED` is write-final.
>
> Archival preserves full entry content, Merkle linkage, and integrity hash manifest. Archived
> epochs are verifiable; on-demand restore is supported for forensic investigation.

**Target 2 — §18.2 (Operational Policy)**
**(REPLACE)** the OQ-SL1 entry:

> `- **OQ-SL1** — Full ledger retention policy (mechanism specced T11; policy deferred).`

**(WITH):**
> `- **OQ-SL1** — CLOSED by D89. Retention interface specced: PROJECT_INITIATED declares policy
>   at bootstrap (immutable-downward, C-SL2); PROJECT_CLOSED ceremony seals and archives;
>   INTEGRITY_VIOLATION epochs are unconditionally indefinite. Archival format versioned.
>   See IC-LDG-RETAIN.`

**Target 3 — Appendix B, Session 7 subsection**
Add:
> **IC-LDG-RETAIN** — Operator → Ledger: retention lifecycle interface. PROJECT_INITIATED
> (bootstrap, immutable), PROJECT_CLOSED (write-final ceremony), RETENTION_OVERRIDE_EXTENDED
> (extensions only). Retention immutable-downward (C-SL2). INTEGRITY_VIOLATION epochs
> unconditionally indefinite. Archival format versioned `"1.0"` (D89).

**Target 4 — Appendix C, LIFECYCLE category**
Add:
> - `PROJECT_INITIATED` (sync, W2 bootstrap — retention policy declaration, mint-once)
> - `PROJECT_CLOSED` (sync — final epoch sealed, Ledger made read-only; archival_status field)

**Target 5 — Appendix C, GOVERNANCE category**
Add:
> - `RETENTION_OVERRIDE_EXTENDED` (sync — retention extension; operator-signed)
> - `RETENTION_OVERRIDE_REJECTED` (sync — retention shortening attempt blocked; SECURITY category)

**Target 6 — §18.4 (Closed in Integration)**
Add:
> - **OQ-SL1** — Full Ledger retention policy (D89: immutable-downward model, PROJECT_CLOSED
>   ceremony, format versioned, IC-LDG-RETAIN).

---

## IC-GATE-9 — `CONTENT_CLASSIFICATION_MIXED` Rejection Protocol

**Specialist provenance:** Graph Data Architect (primary), Warden (secondary), Orchestration
Comparativist (recovery path)
**Tension origin:** T12 (identifies and resolves the previously unlocatable tension)
**Decision references:** D90

### Contract Definition

```
INTERFACE CONTRACT IC-GATE-9: CONTENT_CLASSIFICATION_MIXED Rejection Protocol
  From:    Gate (content classification pre-check)
  To:      Orchestrator (structured error routing) → Coder Agent (split guidance)

  What A exposes:
    When Gate content classification pre-check (pre-check step 5 per §10.2,
    enforcing C-SC4) detects that a .larql patch contains triples spanning
    multiple classification tiers (e.g., both `structural` and `layer4_domain`
    classified triples in a single patch), Gate returns error code
    `CONTENT_CLASSIFICATION_MIXED` with a structured payload:

    { error: "CONTENT_CLASSIFICATION_MIXED",
      patch_id: string,
      detected_classifications: [string...],
        (e.g., ["structural", "layer4_domain"])
      split_guidance: {
        patches: [
          { classification: string,
            triple_ids: [string...] },
          ...
        ]
      },
      complexity_flag: boolean
        (true if split_guidance would produce > 5 sub-patches)
    }

    Classification authority:
    Gate classification is authoritative. The Gate determines the classification
    tier of each triple by reading the triple's `edge_category` field against the
    classification tier mapping declared in Tier 1 config. The Coder Agent's declared
    `CONTENT_CLASSIFICATION` directive at the patch level is informational — it MUST
    match, but the Gate independently verifies each triple's category. A patch with
    a correct patch-level directive but mixed triple-level categories is still rejected.

    The Tier 1 config `classification_tier_mapping` field maps `edge_category` values
    to `structural | layer4_domain | operational` classification tiers.

  Conditions:
    Orchestrator receives `CONTENT_CLASSIFICATION_MIXED` and:
    1. Does NOT consume retry budget (infrastructure failure class per D67).
    2. If `complexity_flag == false`: Orchestrator routes `split_guidance` to
       the Coder Agent as structured feedback (not free-text). The Coder Agent
       MUST use the `split_guidance.patches` array as the authoritative split —
       it MUST NOT re-classify triples independently.
    3. If `complexity_flag == true` (> 5 sub-patches): Orchestrator escalates
       to human review queue before re-dispatching to Coder Agent. A patch
       requiring > 5 splits indicates probable task scope conflation; human
       review MUST assess whether the original task should be re-decomposed.
    4. Coder Agent produces N separate patches as directed, one per entry in
       `split_guidance.patches`. Each patch is submitted independently through
       the full Gate pre-check sequence, including pre-check #8 (IC-GATE-8)
       and this pre-check (#5).

    Loop detection: If Coder Agent receives 3 consecutive `CONTENT_CLASSIFICATION_MIXED`
    rejections for patches that are semantically equivalent to the original rejected
    patch (detected by Gate via patch hash similarity — implementation note, not spec):
    Orchestrator escalates to human review queue. Ledger entry: `CONTENT_SPLIT_LOOP`
    (SECURITY category, advisory — Coder Agent may have a systematic scope
    conflation issue requiring prompt-level correction).

  Failure behavior:
    Gate MUST NOT silently re-classify a mixed patch as single-classification.
    Gate MUST NOT pass a mixed patch downstream on any retry condition.
    The `split_guidance` payload MUST accurately represent the Gate's own
    classification result — it MUST NOT be derived from the Coder Agent's
    declarations. This is a security requirement: a malicious patch might
    declare `structural` classification at the patch level while embedding
    `layer4_domain` triples that would receive less stringent Gate scrutiny
    under structural classification. Gate triple-level verification is the
    authoritative defense.
```

### Insertion Targets

**Target 1 — §8.5 (The `.larql` Canonical Format), line ~293–304**
Extend the description of `CONTENT_CLASSIFICATION`. After the sentence "Value `mixed` rejected
pre-commit (C-SC4).", add:

> When a patch contains triples spanning multiple classification tiers (detectable at Gate
> via triple-level `edge_category` check against the Tier 1 config `classification_tier_mapping`),
> Gate returns `CONTENT_CLASSIFICATION_MIXED` with a structured `split_guidance` payload
> specifying which triple IDs belong to each classification tier (D90, IC-GATE-9). The Coder
> Agent resubmits as N separate single-classification patches. Gate classification is
> authoritative; the Coder's declared patch-level directive is informational only.

**Target 2 — §11.2 (Content-Scoped Authoritative Medium), line ~541–545**
After the sentence "Value `mixed` is rejected pre-commit (C-SC4).", add:

> The `CONTENT_CLASSIFICATION_MIXED` rejection (IC-GATE-9) carries split guidance
> directing the Coder Agent to resubmit as distinct single-classification patches. The
> split is driven by Gate's triple-level classification check, not the Coder's declared
> directive. This preserves the authoritative-medium assignment per D42.

**Target 3 — Appendix B, Session 7 subsection**
Add:
> **IC-GATE-9** — Gate → Orchestrator → Coder Agent: `CONTENT_CLASSIFICATION_MIXED` structured
> rejection with `split_guidance` payload. Gate classification is authoritative. > 5 sub-patches
> → human review escalation. Loop detection at 3 equivalent re-rejections (D90).

**Target 4 — Appendix C, SECURITY category**
Add:
> - `CONTENT_SPLIT_LOOP` (async advisory — Coder Agent repeatedly re-submitting mixed-classification patches)

**Target 5 — Appendix F (Decision-to-Session Cross-Reference)**
Extend the T1–T12 entry. **(REPLACE):**

> `- **T1–T12:** Session 7 (Integration — cross-domain resolutions)`

**(WITH):**
> `- **T1–T12:** Session 7 (Integration — cross-domain resolutions).`
> `- **T12 — IDENTIFIED:** CONTENT_CLASSIFICATION_MIXED rejection protocol (D90). Warden vs.`
> `  Graph Data Architect: Gate classification authority and Coder Agent split-feedback path.`
> `  Previously unlocatable; resolved by IC-GATE-9. See tension-map-v1.md entry for T12.`

---

═══════════════════════════════════════════════════
## SUMMARY TABLES
═══════════════════════════════════════════════════

---

## Open Question Status Updates

Apply the following status changes to §18 of the integrated spec:

| OQ ID | Previous Status | New Status | Closing Reference |
|-------|----------------|------------|-------------------|
| OQ-S4 | Operational Policy (partial) | CLOSED | D87, IC-SCOPE-UPDATE |
| OQ-TC1 | Operational Policy | CLOSED | D84, IC-TC-RESET |
| OQ-TPC1 | Empirical / Post-Deployment | CLOSED | D85, IC-TC-TIMEOUT |
| OQ-SL1 | Operational Policy (partial) | CLOSED | D89, IC-LDG-RETAIN |
| OQ-V5 | Operational Policy (partial) | PARTIALLY CLOSED | D88, IC-CORPUS-AUTH |
| OQ-OC3 | Empirical / Post-Deployment | PARTIALLY CLOSED | D86, IC-OC-PROBE |
| OQ-W6 | Deferred to v2 | PARTIALLY CLOSED (Gate layer) | D81, D82, IC-GATE-8 |

Move OQ-S4, OQ-TC1, OQ-TPC1, OQ-SL1 from their current §18 sections into **§18.4 (Closed in
Integration)** with updated text per insertion targets above. OQ-V5, OQ-OC3, OQ-W6 remain in
their current sections with updated text noting the partial closure.

---

## New Ledger Entry Types — Master Additions List

Apply all of the following to Appendix C. Group by category as indicated.

**SECURITY category — new entries:**
- `LARQL_VERSION_LEGACY` (async advisory)
- `VERSION_REJECTED` (sync — Gate pre-check #8 hard rejection)
- `VERSION_UNSUPPORTED` (sync — Gate pre-check #8 forward-version rejection)
- `SCOPE_UPDATE_REJECTED` (sync — unsigned/invalid scope update attempt)
- `CORPUS_WRITE_REJECTED` (sync for UNAUTHORIZED_AUTHOR; GOVERNANCE for FORMAT_VIOLATION / DUPLICATE_CASE_ID)
- `RETENTION_OVERRIDE_REJECTED` (sync — retention shortening blocked)
- `CONTENT_SPLIT_LOOP` (async advisory — repeated mixed-classification resubmission)

**CONSISTENCY category — new entries:**
- `TIMED_OUT` (sync — PREPARED-state timeout; fields: transaction_id, compensation_direction, trigger)
- `CIRCUIT_TRIPPED` (sync — trip event; fields: trip_type, triggering_transaction_id)
- `RECONCILIATION_COMPLETE` (sync — full reconciliation result; field: `result: CONSISTENT | DIVERGED`)
- `COMPACTION_ABORTED` (sync — compaction verification failure; payload: CompactionProbeReport)
- `COMPACTION_PROBE_FAILED` (sync — probe infrastructure failure during compaction)
- `COMPACTION_CORPUS_SMALL` (async advisory — probe corpus below sampling floor)

**GOVERNANCE category — new entries:**
- `CIRCUIT_RESET` (sync — successful circuit breaker write resumption)
- `CIRCUIT_RESET_REJECTED` (sync — failed reset attempt; SECURITY category for SIGNATURE_INVALID reason)
- `SCOPE_UPDATED` (sync — Write Scope Definition updated; fields: previous/new scope hashes, affected agent IDs)
- `CORPUS_CASE_ADDED` (async — corpus case successfully appended)
- `RETENTION_OVERRIDE_EXTENDED` (sync — retention period extended)

**LIFECYCLE category — new entries:**
- `PROJECT_INITIATED` (sync, W2 bootstrap — retention policy declaration, mint-once)
- `PROJECT_CLOSED` (sync — final epoch sealed, Ledger read-only; field: archival_status)

---

## Gap Backlog Status Updates

Apply the following status changes to `gap-backlog-v1.md` (or to a new `gap-backlog-v1.1.md`):

| GAP | Previous Status | New Status | Resolved By |
|-----|----------------|------------|-------------|
| GAP-3 | 🔴 Critical | 🟠 Reduced (Gate enforcement layer specced; v2 migration strategy remains) | D81, D82, IC-GATE-8 |
| GAP-5 | 🟠 High | ✅ Closed | D87, IC-SCOPE-UPDATE |
| GAP-6 | 🟠 High | ✅ Closed | D84, IC-TC-RESET |
| GAP-7 | 🟠 High | ✅ Closed | D85, IC-TC-TIMEOUT |
| GAP-8 | 🟠 High | 🟡 Reduced (authorship authority/format/minimum defined; cadence operator policy) | D88, IC-CORPUS-AUTH |
| GAP-12 | 🟡 Medium | ✅ Closed | D89, IC-LDG-RETAIN |
| GAP-15 | 🟡 Medium | 🟡 Reduced (failure report format defined; sample calibration deferred to OQ-W1) | D86, IC-OC-PROBE |
| GAP-1 | 🔴 Critical | 🔴 Reduced (interface shape closed; threshold values remain OQ-W1) | D83, IC-WE-1 |

**New gap introduced — GAP-20:**
- **Domain(s):** Warden, Orchestration Comparativist
- **Description:** Peer agent review authorization model (D37 Step 2 escalation). The spec
  describes a second independent Coder Agent receiving a task for peer review, but does not
  define how this agent is tokenized. Agent-to-agent delegation is not modeled in the current
  trust boundary spec. Questions: Does the second Coder Agent receive its own invocation token
  from the Orchestrator (same ceremony as any Coder Agent invocation)? If so, is there any
  trust distinction between a first-invocation Coder Agent and a peer-review Coder Agent?
  Does the peer-review agent's Write Scope Definition require any difference? Is the peer
  agent's identity independently auditable in the Ledger?
- **Blocked by:** A decision on whether peer-review agent invocation uses the standard
  Orchestrator token ceremony (likely yes) or a distinct delegation model.
- **Blocks:** Complete §9.6 (Failure Escalation Cascade) Step 2 spec; IC definition for
  agent-to-agent trust in the escalation path.
- **Priority:** 🟠 High (trust boundary gap adjacent to core agent security model).

---

## Consistency Status API — Partial Addendum

The `CIRCUIT_TRIPPED` state in §12.5 already exists. IC-TC-RESET introduces explicit READ_ONLY
mode semantics for the CIRCUIT_TRIPPED state. Apply the following clarification to §12.5:

In the six-state enum, extend the `CIRCUIT_TRIPPED` entry:

> `CIRCUIT_TRIPPED` — systemwide write suspension. READ_ONLY mode: inference and query
> operations proceed; write token issuance suspended. Enters this state automatically on
> TC circuit-breaker trip. Exits only via IC-TC-RESET signed ceremony. (D84)

---

## Appendix F — T12 Resolution Entry

Add to Appendix F after the T1–T12 cross-reference line:

> **T12 identified and resolved:** `CONTENT_CLASSIFICATION_MIXED` rejection protocol.
> Primary tension: Warden (Gate as classification authority — security integrity of
> triple-level content classification enforcement) vs. Graph Data Architect (Coder
> Agent feedback path — how the agent learns which triples require splitting and into
> which classification tier). Resolved by IC-GATE-9 (D90): Gate emits structured
> `split_guidance`; Gate classification is authoritative over Coder declarations.
> Recovery path routed through Orchestrator to preserve audit trail.

---

*Interface Contract Review Amendment Bundle v1.0*
*9 interface contracts defined (IC-GATE-8, IC-WE-1, IC-TC-RESET, IC-TC-TIMEOUT,*
*IC-OC-PROBE, IC-SCOPE-UPDATE, IC-CORPUS-AUTH, IC-LDG-RETAIN, IC-GATE-9)*
*10 provisional decisions (D81–D90) · 6 new constraints (C-GATE-1, C-GATE-2,*
*C-OC3, C-SL2, C-GOC4, C-WE-1) · 20 new Ledger entry types · 1 new gap (GAP-20)*
*Ready for operator ratification and insertion into llm-as-database-v1_0-integrated-spec.md*
