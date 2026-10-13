# Gap Session 9 — Summary

**Framework:** LLM as Database — Agent Harness Architecture
**Session type:** Gap resolution session (operational policy cluster)
**Primary voices:** State Consistency Theorist + Orchestration Comparativist
**Secondary voice:** MEMIT Specialist (GAP-11 only)
**Targets:** GAP-11 (external document provenance), GAP-12 (Ledger retention), GAP-14 (async threshold rationale), GAP-28 (D91 ratification)
**Baseline:** v1.1 integrated spec as updated by GS1–GS8
**Status on exit:** All four gaps fully resolved; one new OQ surfaced; no new cross-domain tensions

---

## 0. Framing

The four gaps share a common shape: each asks the spec to commit a specific
numeric or policy value where v1.1 left a heuristic placeholder. None is
architecturally contentious — the write engine, Ledger, and orchestration
patterns are all load-bearing and unchanged. What is missing is the *governance
placement* of the values (Tier 1 immutable vs. Tier 3 tunable) and the
*rationale* tying each value to a specific operational guarantee.

GS9's working principle: every threshold or retention value in this cluster must
(a) bind to a named guarantee, (b) sit in a governance tier consistent with
C-SL2 (the immutable-downward rule), and (c) be changeable only by a named
Ledger ceremony. Values without all three are rejected as incomplete.

---

## 1. GAP-11 Resolution — External Document Provenance for Layer 4 Facts

### 1.1 Tracking Decision

**Decision D99:** The harness tracks external-document provenance for any Layer 4
fact written from an external source. Tracking is mandatory, not optional — a
Layer 4 fact without provenance cannot be compiled by the write engine.

Rationale (MEMIT Specialist): Layer 4 facts are by definition the least
entrenched in the parametric layer and the most likely to require rewriting.
Without provenance, a stale Layer 4 fact is indistinguishable from a fresh one
at query time, which defeats the layering model.

Rationale (SCT): The Ledger already carries source attribution for Layer 1–3
writes via Git commit hashes. External sources need the equivalent to participate
in the same audit posture.

### 1.2 Provenance Record Structure

**Decision D100:** Provenance records are stored in two locations, mirroring
the patch/Ledger split used elsewhere.

Location A — `.larql` patch metadata (`external_provenance` block):

| Field                    | Type           | Required | Notes                                     |
|--------------------------|----------------|----------|-------------------------------------------|
| `external_source_uri`    | string (URI)   | yes      | HTTP(S), IPFS, or archive-pin URI         |
| `source_hash_at_write`   | string (hex)   | yes      | Hash of fetched content at write time     |
| `hash_algorithm`         | enum           | yes      | `SHA-256` (v1.1); others reserved         |
| `write_timestamp`        | ISO8601 UTC    | yes      | Time of fetch, not time of patch commit   |
| `fetch_method`           | enum           | yes      | `http_get`, `api_call`, `archive_fetch`   |
| `content_length_bytes`   | integer        | yes      | Detects truncation-vs-change later        |
| `etag`                   | string         | optional | Populated if server returned one          |
| `archive_uri`            | string (URI)   | optional | Best-effort archive.org / IPFS pin        |
| `refetch_policy`         | enum           | yes      | `pruning_cadence`, `hourly`, `never`      |

Location B — `EXTERNAL_PROVENANCE_RECORDED` Ledger entry (CONSISTENCY category,
async), emitted at patch commit. Fields replicate the patch metadata plus
`patch_id`, `fact_triple_hash`, `ledger_seq`.

The Ledger entry is the audit anchor; the patch metadata is the operational
record consulted by the monitoring path.

### 1.3 Staleness Detection Response

**Decision D101:** Staleness is advisory, never blocking, at detection time.
The harness does not block writes or queries on external staleness. Three state
values are defined:

| State             | Meaning                                                       | Ledger entry                         |
|-------------------|---------------------------------------------------------------|--------------------------------------|
| `FRESH`           | Last refetch hash matches `source_hash_at_write`              | none (silent success)                |
| `STALE`           | Source reachable, hash differs from `source_hash_at_write`    | `EXTERNAL_PROVENANCE_STALE` (async)  |
| `UNAVAILABLE`     | Source unreachable (404, DNS fail, timeout)                   | `EXTERNAL_PROVENANCE_UNAVAILABLE`    |

Both non-FRESH states emit CONSISTENCY-category Ledger entries and mark the
underlying fact with an advisory flag visible in query results (`provenance_flag:
STALE | UNAVAILABLE`). CORE-importance facts sourced externally additionally
raise a `REQUIRES_HUMAN_REVIEW` signal on first detection, matching the pattern
used by out-of-band Git reconciliation (§11.13).

Rationale: Network flaps and benign upstream edits (whitespace changes, CDN
variance) are routine. Hard-blocking on external staleness would wedge the
harness on conditions outside operator control. The advisory pattern preserves
auditability without creating a denial-of-service vector against the harness
via external source manipulation.

### 1.4 Monitoring Mechanism

**Decision D102:** Extend the Pruning Agent with an `external_source_audit`
sub-routine. No new component.

Placement rationale: Pruning Agent already (a) runs on a known cadence (§11.12),
(b) emits advisory Ledger entries, (c) owns the `requires_human_review` output
surface. Adding a second agent with nearly-identical responsibilities would
violate the "minimal orchestration surface" principle reinforced in GS6.

Cadence:
- Default: aligned with Pruning cadence (every 50 commits or 24 hours).
- Per-fact override via `refetch_policy` field: `hourly` for fast-moving sources,
  `never` for sources intentionally pinned at a snapshot (archive-only).

Failure isolation: If N consecutive audit passes fail to reach the network,
the Pruning Agent suspends further external-audit work (not Git-side pruning)
and emits `EXTERNAL_AUDIT_SUSPENDED` — a single advisory CONSISTENCY entry. This
prevents log-flooding under sustained network partition.

### 1.5 Spec Block — External Document Provenance

```
### External Document Provenance (Layer 4) — Spec Block

What it must do:
- Bind every Layer 4 fact written from an external source to a hash-pinned
  snapshot of that source at write time.
- Detect source drift (content change) and source loss (unreachability) on a
  scheduled cadence, emitting advisory Ledger entries without blocking writes
  or queries.

What it explicitly does NOT do:
- Auto-retract or auto-rewrite facts when their source changes. Staleness is
  surfaced; reconciliation is a separate human or Coder-Agent-driven action.
- Guarantee fetch fidelity for sources that serve non-deterministic content
  (dynamic pages, auth-gated resources). Out of scope for v1.1; such sources
  should be snapshotted to an archive URI before provenance recording.

Hard constraints:
- C-EXT-PROV1: Layer 4 external facts without `external_provenance` block
  in the patch metadata cannot be compiled. Write engine rejects.
- C-EXT-PROV2: Staleness detection MUST be advisory. No code path promotes
  STALE or UNAVAILABLE to a blocking state automatically.
- C-EXT-PROV3: Pruning Agent audit sub-routine failures MUST NOT propagate
  to Git-side pruning. Isolation is explicit.

Tradeoffs decided:
- Advisory-only over hard-blocking (§1.3 rationale).
- Extended Pruning Agent over new dedicated component (§1.4 rationale).
- SHA-256 as sole hash algorithm for v1.1; field is enum-typed for future
  agility (BLAKE3 etc.) without schema migration.

Open questions (deferred):
- OQ-SC3 (new): Reconciliation workflow for STALE Layer 4 facts once detected.
  Currently the fact stays in .vindex with an advisory flag; whether a Coder
  Agent auto-proposes a refresh patch or whether operator approval is
  required first is unspecified. Likely spec in GS10.

Interface contract:

IC-EXT-PROV1 — Write engine → patch validation
  From: Layer 4 .larql patch submitted to write engine
  To: MEMIT compilation path
  What A exposes: `external_provenance` block present and well-formed.
  Failure behavior: LAYER4_MISSING_PROVENANCE (UNRECOVERABLE at patch level).

IC-EXT-PROV2 — Pruning Agent audit → State Ledger
  From: Pruning Agent external_source_audit sub-routine
  To: State Ledger CONSISTENCY stream
  What A exposes: EXTERNAL_PROVENANCE_STALE or EXTERNAL_PROVENANCE_UNAVAILABLE
    entries keyed by fact_triple_hash + source_uri.
  Conditions: Refetch performed; hash compared; non-FRESH outcome reached.
  Failure behavior: EXTERNAL_AUDIT_SUSPENDED after N consecutive network
    failures (N configurable, default 5).
```

---

## 2. GAP-12 Resolution — Ledger Retention Policy

### 2.1 Retention Governance Placement

**Decision D103:** Two-tier retention model. Tier 1 declares the immutable
minimum floor; Tier 3 declares the active-in-hot-storage period.

| Parameter                      | Tier   | Default    | Constraint                                 |
|--------------------------------|--------|------------|--------------------------------------------|
| `ledger_retention_floor`       | Tier 1 | 7 years    | Minimum total retention; cannot be reduced |
| `ledger_active_period`         | Tier 3 | 90 days    | Hot-storage window; tunable                |
| `ledger_archive_period`        | derived| floor − active | Must be ≥ 0; archive storage holds       |

C-SL2 interaction: the immutable-downward rule applies as follows:
- `ledger_retention_floor` is immutable once set at Genesis. It may be *extended*
  by a new ceremony (see D105 below) but never shortened.
- `ledger_active_period` is operator-tunable downward to a minimum of **30 days**
  (Tier 1 floor on Tier 3 value); attempts to reduce below 30 days are rejected
  by the Transaction Controller.
- `ledger_archive_period` is not directly configured; it's derived to satisfy
  `active + archive ≥ floor`. Reducing `active_period` extends `archive_period`
  for the same total.

Rationale (SCT): Seven years mirrors standard financial and legal audit retention
floors and gives a defensible forensic window for the full lifecycle of a
typical project. Ninety days active reflects the practical query window for
operational debugging without forcing hot-storage costs on old entries.

### 2.2 Archival Format

**Decision D104:** A single canonical archive format for v1.1, versioned to
permit future evolution without breaking restore paths.

```
Format identifier:     ledger-archive/v1
Compression:           zstd (level 19, long mode enabled)
Per-entry integrity:   SHA-256 (matches hot-Ledger algorithm)
Archive integrity:     Merkle root over all entries in archive batch
Secondary check:       Chain-link hash at archive_start and archive_end anchors
                       archive to hot Ledger at boundary seq
```

Manifest schema (`archive-manifest.json`, sibling to compressed payload):

| Field                      | Type          | Notes                                      |
|----------------------------|---------------|--------------------------------------------|
| `archive_id`               | UUID          | Unique per archive batch                   |
| `format_version`           | string        | `ledger-archive/v1`                        |
| `start_ledger_seq`         | integer       | First entry in archive                     |
| `end_ledger_seq`           | integer       | Last entry in archive                      |
| `start_timestamp`          | ISO8601 UTC   | First entry time                           |
| `end_timestamp`            | ISO8601 UTC   | Last entry time                            |
| `entry_count`              | integer       | For restore verification                   |
| `chain_hash_at_start`      | string (hex)  | Hash of entry at start_ledger_seq − 1      |
| `chain_hash_at_end`        | string (hex)  | Hash of entry at end_ledger_seq            |
| `archive_merkle_root`      | string (hex)  | Merkle root over archived entries          |
| `compression_algo`         | string        | `zstd`                                     |
| `compression_params`       | string        | `level=19;long=27`                         |
| `payload_sha256`           | string (hex)  | Hash of the compressed payload file        |
| `manifest_sha256`          | string (hex)  | Self-hash excluding this field             |
| `signer_identity`          | string        | Operator identity signing archive          |
| `signature`                | string        | Signature over manifest (excl. signature)  |

Restore procedure:
1. Verify `manifest_sha256` self-consistency.
2. Verify operator signature against trusted identity registry.
3. Verify `payload_sha256` against compressed payload file.
4. Decompress payload.
5. Verify `archive_merkle_root` against decompressed entries.
6. Verify `chain_hash_at_start` links to hot-Ledger entry (end_seq − 1) —
   this confirms archive is contiguous with hot Ledger.
7. Expose restored range as read-only query layer appended to hot Ledger.

Merkle-chain-lite integrity extends across archive boundaries: a chain
verification pass reads the manifest's `chain_hash_at_end` to continue
verification into the next archive segment or into hot Ledger, without requiring
decompression.

### 2.3 PROJECT_CLOSED Ceremony Relationship

**Decision D105:** `PROJECT_CLOSED` (LIFECYCLE, signed) is a synchronous Ledger
entry that triggers — but does not depend on — final archival.

Sequence:
1. `PROJECT_CLOSED` entry committed to Ledger synchronously. Harness enters
   `CLOSED` state — no new agent tokens issued, no new writes accepted.
2. Final snapshot emitted: `FINAL_STATE_SNAPSHOT` entry carrying the Ledger
   chain tip hash and `.vindex` snapshot hash at close.
3. Archive ceremony dispatched asynchronously:
   - If archive storage is available and writable: archive batch produced
     per D104, manifest signed, `PROJECT_ARCHIVED` Ledger entry emitted.
   - If archive storage is unavailable: `PROJECT_ARCHIVE_PENDING` entry
     emitted instead, with SLA clock started (default: 30 days to resolve).
4. Expiry of SLA without `PROJECT_ARCHIVED` emission raises
   `PROJECT_ARCHIVE_SLA_BREACHED` — an operational incident requiring
   operator intervention. It does not alter the Ledger state of the project
   (which is `CLOSED`), but flags the archival gap in any subsequent audit.

Rationale: Decoupling `PROJECT_CLOSED` (which must succeed atomically and is a
forensic anchor) from archival I/O (which can fail for storage reasons outside
harness control) preserves the closing ceremony's atomicity without fabricating
a success signal for archival that may not have occurred.

### 2.4 Retention Update Ceremony

Retention floor extension (immutable-downward preserved): ceremony entry
`LEDGER_RETENTION_EXTENDED`, Tier 1 authority signer, carries
`new_floor_years > old_floor_years`. Attempts to reduce the floor are
rejected at entry-construction time.

Active period changes: ceremony entry `LEDGER_ACTIVE_PERIOD_UPDATED`,
Tier 3 authority (operator), carries new value ≥ 30-day floor. Reduction
permitted within floor.

### 2.5 Spec Block — Ledger Retention

```
### Ledger Retention & Archival — Spec Block

What it must guarantee:
- No Ledger entry is deleted or made unreadable within the Tier 1 retention
  floor, regardless of operator configuration.
- Archived entries remain chain-verifiable against the hot Ledger Merkle chain
  via manifest anchors.
- Project close produces a synchronous forensic anchor even when archival
  storage is temporarily unavailable.

What it explicitly does NOT guarantee:
- Uninterrupted query latency for archived entries. Restore can require
  decompression and signature verification; this is a read-time cost.
- Archival storage medium availability. External dependency, monitored via
  the SLA mechanism but not guaranteed by the harness.

Hard constraints:
- C-RETENTION1: `ledger_retention_floor` is monotonically non-decreasing
  from Genesis onward.
- C-RETENTION2: `ledger_active_period ≥ 30 days`.
- C-RETENTION3: Archive manifests MUST link chain hashes across archive
  boundaries for end-to-end Merkle verifiability.
- C-RETENTION4: PROJECT_CLOSED Ledger write MUST NOT block on archive I/O.

Tradeoffs decided:
- Single canonical archive format (zstd + SHA-256 + Merkle) over per-project
  format negotiation. Forensic readability over compression tuning.
- Seven-year floor as default, operator may only extend. Short-project
  operators bear the cost; long-lived projects are the common case.
- Async archival with SLA-tracked pending state over synchronous archival.
  Preserves closing ceremony atomicity.

Open questions (deferred):
- None new. OQ-SL1 closed by this spec block.

Interface contract:

IC-RETENTION1 — PROJECT_CLOSED → final snapshot
  From: Transaction Controller at project-close ceremony
  To: State Ledger LIFECYCLE stream
  What A exposes: Synchronous PROJECT_CLOSED + FINAL_STATE_SNAPSHOT pair;
    chain tip hash; .vindex snapshot hash.
  Failure behavior: Ceremony atomic — both succeed or neither commits.

IC-RETENTION2 — Archive manifest → restore path
  From: Completed archive batch
  To: Any future restore invocation
  What A exposes: Signed manifest with Merkle root, chain-link anchors,
    payload hash; compressed payload.
  Conditions: All archive verification steps pass (D104 sequence 1–6).
  Failure behavior: RESTORE_MANIFEST_INVALID or RESTORE_CHAIN_BREAK.
```

---

## 3. GAP-14 Resolution — Async Threshold Rationale Framework

### 3.1 WAL Flush Cadence

**Decision D106:** WAL flush policy is two-mode, keyed to fact importance class.

| Write class           | Flush policy                              | Data-loss window bound |
|-----------------------|-------------------------------------------|------------------------|
| CORE (Layer 1–2)      | fsync per entry (synchronous)             | 0 entries              |
| SUPPORTING (Layer 3)  | fsync per entry                           | 0 entries              |
| CONTEXTUAL (Layer 4)  | group commit: 10ms OR 64KB buffer         | ≤ 10ms window          |
| Async advisory stream | group commit: 100ms OR 256KB buffer       | ≤ 100ms window          |

Guarantee bound: In the worst-case crash, the harness can lose at most the
entries in the open group-commit buffer at the moment of failure, bounded by
the time/size threshold for that write class. CORE and SUPPORTING writes have
a zero-entry loss guarantee.

Rationale: fsync-per-entry is the expensive path but it is the only policy
that upholds the "no silent write loss" property for important facts. Layer 4
and async advisory streams tolerate brief loss windows because their
entries are either (a) re-derivable from source or (b) advisory and
idempotently replayable.

### 3.2 Light Verification Interval

**Decision D107:** Light verification remains at every 100 entries; the
guarantee it expresses is now named.

Corruption-detection window bound: ≤ 100 entries between any storage-layer
corruption event and its detection, assuming continuous writes.

Rationale: Bit rot, partial writes, and I/O errors in append-only logs
manifest at the storage layer and do not propagate through the Merkle chain
structure (which is computed pre-write). Light verification reads the last
~10 entries and re-verifies their chain links, catching single-entry and
short-run corruption without the cost of full-chain traversal. At the canonical
write rate assumption (single-digit entries per minute for typical projects),
100 entries ≈ several hours — short enough that a silent corruption cannot
escape into an operator's routine review cycle undetected.

### 3.3 Full Verification Interval

**Decision D108:** Full verification at 10,000 entries OR 24 hours; audit-
completeness guarantee is now named.

Audit-completeness guarantee: Every Ledger entry in the hot range is
chain-verified end-to-end at least once per 24 hours or once per 10,000 entries,
whichever comes first.

Rationale: The 24-hour ceiling bounds the worst-case time a subtle corruption
(one that evades light verification's 10-entry window) can persist before
detection. The 10,000-entry ceiling handles the opposite case: long idle periods
where time alone would not trigger full verification frequently enough if the
harness were later restarted at scale. Both ceilings are required — time alone
fails under burst load; entry count alone fails under idle.

Archive boundaries are included in full verification via manifest chain-link
anchors (D104), so the guarantee extends across the hot/archive split.

### 3.4 Reconciliation Backlog Thresholds

**Decision D109:** Thresholds reaffirmed; out-of-band-sync SLA now explicit.

Out-of-band sync SLA: The harness expects out-of-band Git changes (commits
made outside the harness pipeline per §11.13) to be reviewed by a human or
auto-reconciliation pass within 7 days. Exceeding this is a degradation
signal; exceeding 30 days is an operational incident.

| Backlog state                      | Meaning                                              | Consequence                         |
|------------------------------------|------------------------------------------------------|-------------------------------------|
| NORMAL                             | ≤10 items, all <7d                                   | none                                |
| RECONCILIATION_BACKLOG_WARNING     | >10 items OR any ≥7d                                 | Advisory Ledger entry, no gating    |
| RECONCILIATION_BACKLOG             | >50 items OR any ≥30d                                | Circuit breaker: new writes gated   |

Rationale: The 7-day first threshold reflects a typical work-week review
cadence; a backlog crossing this suggests the operator review workflow is
falling behind. 30 days and >50 items together indicate systemic
disengagement — at that point, continuing to write into a divergent state is
likely to produce harder-to-reconcile consequences later, so the circuit
breaker engages.

### 3.5 Threshold Update Ceremony

**Decision D110:** All thresholds in §3.1–§3.4 are Tier 3 tunable with Tier 1
ordering invariants. A single ceremony entry type handles updates.

Ceremony entry: `ASYNC_THRESHOLDS_UPDATED` (CONFIG category, signed).

Fields: any subset of {`wal_flush_policy`, `light_verification_interval`,
`full_verification_max_entries`, `full_verification_max_hours`,
`reconciliation_warn_count`, `reconciliation_warn_age_days`,
`reconciliation_critical_count`, `reconciliation_critical_age_days`}.

Tier 1 invariants enforced at entry construction (rejected if violated):
- `light_verification_interval < full_verification_max_entries`
- `reconciliation_warn_count < reconciliation_critical_count`
- `reconciliation_warn_age_days < reconciliation_critical_age_days`
- `wal_flush_policy` for CORE and SUPPORTING classes MUST remain fsync-per-entry
  (cannot be downgraded to group-commit; this is the one Tier 1 hard pin on
  a threshold, not a tunable).

Authority: operator signer. The ceremony is versioned — prior threshold
values remain in Ledger history for forensic reconstruction of past behavior.

### 3.6 Spec Block — Async Threshold Framework

```
### Async Threshold Framework — Spec Block

What it must do:
- Bind every async threshold to a named operational guarantee.
- Keep all thresholds tunable subject to ordering invariants that preserve
  the guarantees' meaning.
- Produce an auditable record of threshold changes so past Ledger behavior
  is reconstructible.

What it explicitly does NOT do:
- Adapt thresholds automatically based on workload. Thresholds are declared
  values, not learned ones, in v1.1.

Hard constraints:
- C-ASYNC1: CORE and SUPPORTING writes use fsync-per-entry WAL policy. Not
  tunable.
- C-ASYNC2: Light < full verification interval.
- C-ASYNC3: Warn < critical for both count and age reconciliation thresholds.
- C-ASYNC4: Every threshold change emits ASYNC_THRESHOLDS_UPDATED Ledger
  entry with prior and new values.

Tradeoffs decided:
- Named guarantees over opaque heuristics (each threshold now has a
  consequence sentence).
- Tunable with invariants over hardcoded values — operators face diverse
  workload realities; invariants preserve the semantic core.
- Fsync-per-entry for CORE/SUPPORTING as Tier 1 pin — performance cost
  accepted in exchange for zero-loss guarantee on the important layer.

Open questions (deferred):
- None new from this decision set.

Interface contract:

IC-ASYNC1 — Threshold update → Transaction Controller
  From: ASYNC_THRESHOLDS_UPDATED Ledger entry
  To: TC operational parameters
  What A exposes: New threshold values after Tier 1 invariant check.
  Failure behavior: ASYNC_THRESHOLDS_INVALID — entry rejected pre-commit.
```

---

## 4. GAP-28 Resolution — D91 Ratification

**Decision D111:** D91 stands as final. Best-effort proactive notification is
augmented with a minimal spec boundary: at-least-one-attempt-before-TTL.

Specification:
- Upon `SCOPE_UPDATED` Ledger commit, the Orchestrator SHALL attempt
  delivery of a scope-update notification to each agent in `affected_agent_ids`
  at least once before the notification TTL expires.
- Notification TTL: **60 seconds** from `SCOPE_UPDATED` entry commit (Tier 3
  tunable; Tier 1 floor of 10 seconds).
- Attempted but failed deliveries (agent unreachable, queue full) are logged
  but not retried past TTL.
- Per-type notification logic from GS4's `scope_change_type` is preserved:
  the Orchestrator may choose to prioritize `RESTRUCTURING` notifications
  within the TTL window over `EXPANDING` notifications, as an implementation
  optimization.

Agent responsibility reaffirmation: Agents MUST NOT rely on proactive
notification for safety-critical behavior. The authoritative source of scope
truth remains the Ledger itself; agents check the `SCOPE_UPDATED` stream on
any operation that depends on current scope. This is the closing seal on D91:
notification is a performance hint, not a safety mechanism.

Spec boundary rationale: "Best-effort with no attempt" is pathological and
indistinguishable from non-compliance in audit. The one-attempt-before-TTL
boundary forbids that pathology without specifying a retry strategy (which
remains implementation-owned).

### 4.1 Spec Block — Proactive Scope Notification

```
### Proactive Scope Notification — Spec Block

What it must do:
- Attempt delivery of a scope-update notification to each affected agent
  at least once before TTL.
- Log attempted deliveries and their outcomes (delivered, queue-full,
  unreachable) to the Ledger as a single AGGREGATE entry per SCOPE_UPDATED
  event.

What it explicitly does NOT do:
- Guarantee delivery. Agents treat notification as a hint.
- Retry past TTL.
- Block scope activation on notification success.

Hard constraints:
- C-NOTIFY1: At least one delivery attempt per affected agent per
  SCOPE_UPDATED, before TTL expiry.
- C-NOTIFY2: Notification TTL ≥ 10 seconds.
- C-NOTIFY3: Agent safety-critical operations MUST read SCOPE_UPDATED from
  Ledger; notification is advisory only (reaffirms D91).

Tradeoffs decided:
- Minimal spec boundary (one attempt) over full delivery guarantee.
  Avoids over-constraining implementation while forbidding the no-attempt
  pathology.
- TTL as Tier 3 tunable (floor 10s) balances responsiveness against retry
  latency in slow-network deployments.

Open questions (deferred):
- None. GAP-28 closed.

Interface contract:

IC-NOTIFY1 — SCOPE_UPDATED → Orchestrator dispatch
  From: SCOPE_UPDATED Ledger entry (carries affected_agent_ids and
    scope_change_type per GS4)
  To: Orchestrator notification dispatcher
  What A exposes: Commit event with payload; notification TTL window opens.
  Conditions: One attempt per affected agent before TTL.
  Failure behavior: Per-agent attempt failure is logged, not escalated.

IC-NOTIFY2 — Agent scope read → Ledger
  From: Agent performing scope-sensitive operation
  To: State Ledger SCOPE_UPDATED stream
  What A exposes: Current scope for the agent, read authoritatively.
  Conditions: Agent reads Ledger on any scope-dependent branch.
  Failure behavior: Agent MUST NOT proceed on stale proactive-notification
    data for safety-critical operations.
```

---

## 5. Cross-Domain Tension Check

| Domain                      | Tension surfaced?                                                                  |
|-----------------------------|------------------------------------------------------------------------------------|
| MEMIT Specialist            | No — external provenance is additive metadata; write engine gains a validation check but no compilation semantics change. |
| Graph Data Architect        | No — schema untouched. Provenance is metadata on the patch, not on the triple.     |
| Warden                      | Low-surface — operator signatures newly required on `LEDGER_RETENTION_EXTENDED` and `ASYNC_THRESHOLDS_UPDATED` ceremonies. Reuses existing signer registry. |
| Validation Contract         | No — validation pipeline untouched.                                                |
| State Consistency Theorist  | Owned — resolved here.                                                             |
| Orchestration Comparativist | Owned — resolved for GAP-14 (threshold ceremony dispatch) and GAP-28 (notification contract). Dispatch surface is minor-additive only. |

No new cross-domain conflicts surfaced. All new ceremonies (D103–D110 retention
and threshold updates; D111 notification) reuse the existing Tier 1/Tier 3
governance pattern and the existing operator-signer trust chain. No new trust
boundaries were introduced.

---

## 6. Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-11** — External document provenance for Layer 4 facts fully specced.
  Mandatory provenance block (D99/D100), advisory-only staleness states with
  three-value enum (D101), Pruning Agent extension as monitoring mechanism
  (D102). Covers both STALE (source changed) and UNAVAILABLE (source gone)
  conditions with audit-trail Ledger entries.
- **GAP-12** — Ledger retention policy fully specced. Two-tier governance
  with 7-year Tier 1 floor and 90-day Tier 3 active period (D103); canonical
  `ledger-archive/v1` format with zstd compression, SHA-256 + Merkle
  integrity, manifest anchors for cross-boundary chain verification (D104);
  PROJECT_CLOSED decoupled from archival I/O with SLA-tracked pending state
  (D105).
- **GAP-14** — Async threshold rationale framework fully specced. Every
  threshold now binds to a named guarantee: WAL zero-loss for CORE/SUPPORTING
  with bounded-window for Layer 4 (D106), ≤100-entry corruption-detection
  window (D107), ≤24h or ≤10,000-entry audit-completeness (D108), 7d/30d
  reconciliation SLA (D109), all tunable via `ASYNC_THRESHOLDS_UPDATED`
  ceremony under Tier 1 ordering invariants (D110).
- **GAP-28** — D91 ratified as final. Minimal delivery spec boundary added:
  at-least-one-attempt-before-TTL with 60-second default TTL (Tier 3, Tier 1
  floor 10s); agent safety responsibility reaffirmed; retry strategy left
  implementation-owned (D111).

**GAPS PARTIALLY RESOLVED:**
- None.

**GAPS DEFERRED:**
- None from GS9 scope. All four target gaps resolved in full.

**NEW GAPS SURFACED:**
- **OQ-SC3** (new) — Reconciliation workflow for STALE Layer 4 facts once
  provenance staleness is detected. Spec currently says the fact stays in
  `.vindex` with an advisory flag; whether a Coder Agent auto-proposes a
  refresh patch, or whether operator approval is always required first, is
  unspecified. Medium priority; candidate for GS10 if scheduled.

**NEW TENSIONS SURFACED:**
- None. Cross-domain check clean (see §5).

**NEW DECISIONS (for v1.2 / v1.1+ spec update):**
- D99 — Mandatory external-document provenance for Layer 4 facts (write engine rejects without).
- D100 — Provenance record structure (9 fields in `.larql` metadata; replicated to `EXTERNAL_PROVENANCE_RECORDED` Ledger entry).
- D101 — Three-state staleness enum (FRESH / STALE / UNAVAILABLE); advisory-only, CORE facts raise `REQUIRES_HUMAN_REVIEW` on first detection.
- D102 — Pruning Agent gains `external_source_audit` sub-routine; no new component.
- D103 — Ledger retention two-tier model: Tier 1 `ledger_retention_floor` (7y default) + Tier 3 `ledger_active_period` (90d default, 30d floor).
- D104 — Canonical archive format `ledger-archive/v1` (zstd + SHA-256 + Merkle + manifest chain anchors).
- D105 — `PROJECT_CLOSED` synchronous; archival async with SLA-tracked `PROJECT_ARCHIVE_PENDING` state.
- D106 — WAL flush policy keyed to write class: fsync-per-entry for CORE/SUPPORTING, group-commit for Layer 4 and async advisory.
- D107 — Light verification interval 100 entries — bound: ≤100-entry corruption-detection window.
- D108 — Full verification 10,000 entries OR 24h — bound: 24h audit-completeness guarantee.
- D109 — Reconciliation backlog thresholds reaffirmed; out-of-band sync SLA now explicit (7d warn, 30d circuit-breaker).
- D110 — `ASYNC_THRESHOLDS_UPDATED` ceremony with Tier 1 ordering invariants; fsync-per-entry for CORE/SUPPORTING is Tier 1 hard pin.
- D111 — D91 ratified; at-least-one-attempt-before-TTL notification boundary; 60s default TTL (Tier 3, 10s Tier 1 floor).

**NEW CONSTRAINTS:**
- C-EXT-PROV1, C-EXT-PROV2, C-EXT-PROV3 (external provenance: required, advisory-only, isolation from Git pruning).
- C-RETENTION1, C-RETENTION2, C-RETENTION3, C-RETENTION4 (retention monotonicity, active floor, archive chain-linking, close/archive decoupling).
- C-ASYNC1, C-ASYNC2, C-ASYNC3, C-ASYNC4 (fsync pin, verification ordering, reconciliation ordering, threshold auditability).
- C-NOTIFY1, C-NOTIFY2, C-NOTIFY3 (notification attempt guarantee, TTL floor, agent safety read-through).

**NEW INTERFACE CONTRACTS:**
- IC-EXT-PROV1 — Write engine patch validation for Layer 4 provenance.
- IC-EXT-PROV2 — Pruning Agent external audit → State Ledger.
- IC-RETENTION1 — PROJECT_CLOSED → FINAL_STATE_SNAPSHOT paired atomic commit.
- IC-RETENTION2 — Archive manifest → restore path.
- IC-ASYNC1 — Threshold update → Transaction Controller.
- IC-NOTIFY1 — SCOPE_UPDATED → Orchestrator notification dispatch.
- IC-NOTIFY2 — Agent scope-sensitive read → Ledger.

**NEW LEDGER ENTRY TYPES:**
- `EXTERNAL_PROVENANCE_RECORDED` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_STALE` (CONSISTENCY, async)
- `EXTERNAL_PROVENANCE_UNAVAILABLE` (CONSISTENCY, async)
- `EXTERNAL_AUDIT_SUSPENDED` (CONSISTENCY, async, rate-limited)
- `FINAL_STATE_SNAPSHOT` (LIFECYCLE, signed, paired with PROJECT_CLOSED)
- `PROJECT_ARCHIVED` (LIFECYCLE, signed)
- `PROJECT_ARCHIVE_PENDING` (LIFECYCLE, signed)
- `PROJECT_ARCHIVE_SLA_BREACHED` (LIFECYCLE, signed)
- `LEDGER_RETENTION_EXTENDED` (CONFIG, signed, immutable-downward enforced)
- `LEDGER_ACTIVE_PERIOD_UPDATED` (CONFIG, signed)
- `ASYNC_THRESHOLDS_UPDATED` (CONFIG, signed)

---

**Session exit posture:** All four operational-policy gaps closed with spec
language. One new open question (OQ-SC3) surfaced, medium priority, non-blocking.
v1.1 integrated spec gains thirteen new decisions (D99–D111), four constraint
clusters, seven interface contracts, and eleven Ledger entry types. Ready for
absorption into v1.2 (or v1.1+) integrated spec. GS10 can proceed in any order
against remaining backlog.
