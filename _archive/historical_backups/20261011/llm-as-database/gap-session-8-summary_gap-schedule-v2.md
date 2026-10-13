# Gap Session 8 — Summary

**Framework:** LLM as Database — Agent Harness Architecture
**Session type:** T13 / GAP-20 residuals-clearance pass
**Primary voices:** MEMIT Specialist, Orchestration Comparativist, Graph Data Architect
**Review voices:** Warden (trust boundary on dry-run artifact store), State Consistency Theorist (Ledger interaction)
**Targets:** T13 M-threshold provisional, GAP-20 bucket_map provisional, NEW-GAP-28 (dry-run artifact storage), NEW-GAP-29 (cross-agent SCOPE aggregate monitoring), T14 candidate (dry-run freshness vs. manifest authorship cycle), GAP-1 empirical calibration protocol
**Baseline:** v1.1 integrated spec as updated through GS7 (T13 core resolution, GAP-20/IC-MANIFEST-1, A4–A9, A7b)
**Status on exit:** T13 and GAP-20 residuals cleared (pending empirical calibration under GAP-1); two new gaps closed; T14 candidate resolved; GAP-1 empirical protocol specified

---

## Scope Note

GS7 (per gap-schedule-v3) ratified the T13 three-tier advisory model and IC-MANIFEST-1.
Both closures carried explicit residuals:

- **T13:** M threshold (`r ≥ 0.25`, count ≥ 75) marked **PROVISIONAL** pending GAP-1 empirical calibration of the per-hop translation error coefficient ε.
- **GAP-20:** `bucket_map` boundary thresholds (e.g. 0.33 / 0.66) marked **PROVISIONAL** pending GAP-1.
- **New gaps surfaced:** NEW-GAP-28 (dry-run artifact storage unspecified) and NEW-GAP-29 (cross-agent aggregate SCOPE monitoring).
- **T14 candidate:** dry-run 7-day freshness window vs. longer manifest authorship cycles.

GS8 addresses this residual set. The GS7 spec blocks themselves are unchanged; GS8 augments them with a calibration protocol (so the provisionals have a defined path to resolution), the dry-run artifact store spec (so IC-MANIFEST-1's `dry_run_artifact_hash` field has a backing contract), an aggregate-tier advisory spec (so GAP-27's multi-agent spray residual has an orchestrator-level countermeasure), and a resolution of the T14 freshness-vs-cycle tension.

---

## 1. GAP-1 Empirical Calibration Protocol — Spec Block (ratified)

**Context.** GAP-1 remains formally deferred (D-CRC-2) and cannot be closed through spec work. What GS8 specifies here is **not a resolution of GAP-1** — it is the measurement protocol that, when executed during implementation, produces the data required to ratify the currently-provisional thresholds. This spec block exists so that when implementation data becomes available, the values can be substituted in without re-litigating the structure.

### 1.1 MEMIT Specialist — Calibration Scope

Two provisional values depend on GAP-1:

- **ε** — per-hop translation error coefficient in `Δfidelity ≈ r × h_avg × ε`. GS7 estimated 0.02–0.05 as a provisional range derived from the approximation characteristics of RENAME/BUCKET/COMPUTE transforms. Empirical calibration must produce a measured value per transform class.
- **bucket_map boundaries** — the float-to-enum boundary thresholds used in BUCKET transforms (illustrated at 0.33 / 0.66 in GS7 IC-MANIFEST-1).

A third provisional value falls out of the first:

- **M (hard-block threshold)** — `r ≥ 0.25` or absolute count ≥ 75. M is a function of ε and the corpus compaction tolerance; once ε is measured, M is re-derived rather than independently measured.

### 1.2 Calibration Protocol (D-GS8-A) — `larql_fidelity_calibration`

Produces a calibration artifact consumable by genesis-seal update ceremonies.

**Preconditions:**
- At least one full `current_larql_version` increment has occurred, producing a non-empty migration manifest with at least one RENAME, one BUCKET, and one COMPUTE transform type populated.
- A reference patch corpus representative of production agent output exists (minimum 200 patches per transform class per version hop measured).

**Procedure (per transform class, per version hop):**
1. Select reference patches at `source_version`. Compile through MEMIT to produce baseline parametric encoding; record per-patch retrieval fidelity via canonical probe set (probe set defined at Genesis; see D81).
2. Apply migration manifest translation to the same reference patches. Compile the translated patches through MEMIT. Record per-patch retrieval fidelity via the same probe set.
3. Compute per-patch fidelity delta. Aggregate mean, p50, p95, p99 across the class-hop combination.
4. The class-hop ε value = p95 of fidelity delta. (p95 chosen over mean to bound worst-case compaction batches.)

**Output artifact (`epsilon_calibration_report`):**
- Per transform class (RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT): per-hop ε values.
- Corpus statistics (patch count per class-hop, probe set version).
- Compaction tolerance assumption used for M derivation (provisional default: `Δfidelity_max = 0.05` acceptable; ratified during calibration).
- Timestamp and signing CAK.

**Ratification path:**
- Calibration artifact is submitted via the genesis-seal update ceremony (GS4 D92–D96 CeremonyToken model, `CALIBRATION_RATIFICATION` ceremony type — new; added this session).
- On acceptance: Tier 1 `genesis-seal.json` fields `larql_epsilon_table`, `compaction_tolerance`, and derived M values are populated. Provisional flags on T13 thresholds and IC-MANIFEST-1 `bucket_map` are cleared in the spec's next integrated iteration.

### 1.3 Bucket Boundary Determination (D-GS8-B)

Bucket boundaries for any BUCKET transform class are calibrated by the same protocol, producing a per-transform-class optimal boundary table rather than a fixed global default. GS7's illustrative 0.33 / 0.66 values are retained as **provisional illustrative defaults** for the `attention_weight → declared_importance` bucket only; other BUCKET transforms ratify their own boundaries at calibration time.

### 1.4 Interface Contract Delta

`IC-MANIFEST-1` `bucket_map` field description updated:
- Boundaries remain PROVISIONAL until a `CALIBRATION_RATIFICATION` ceremony is accepted for the transform class the bucket serves.
- Manifest entries authored prior to first calibration carry `calibration_state: UNCALIBRATED` and flag accordingly in dry-run reports (non-blocking; advisory only until first calibration lands).

---

## 2. NEW-GAP-28 — Dry-Run Artifact Storage Spec Block (ratified)

**Context.** IC-MANIFEST-1 requires every manifest commit to reference `dry_run_artifact_hash` pointing at a dry-run report produced within the 7-day freshness window. GS7 specified the field and the commit-gate check (check #5 and #6) but left the artifact's storage medium, retention, and tamper-evidence unspecified.

### 2.1 Warden + Graph Data Architect — Requirements

**Trust requirements (Warden):**
- The artifact must be tamper-evident: the `dry_run_artifact_hash` on a manifest entry must bind to content that cannot have been altered between dry-run execution and manifest commit.
- The artifact must be fetchable by the Gate during commit-gate verification without depending on the producing agent's state.
- The artifact store must not be writable by agents outside the dry-run execution path.

**Schema requirements (Graph Data Architect):**
- The artifact must be serializable in a canonical form such that content hashes are stable across re-serialization.
- The artifact must include sufficient detail for the seven-point commit-gate check to run without re-executing the dry-run.

### 2.2 `dry_run_report` — Artifact Shape (IC-DRYRUN-1)

```
INTERFACE CONTRACT IC-DRYRUN-1:
  From: Dry-Run Executor (Architect Agent or authorized validation harness)
  To: Gate (at manifest commit-gate verification time)

  What the Executor exposes:
    Canonical-serialized dry_run_report with fields:
      manifest_hash: string                      — hash of the candidate manifest entry
      corpus_sample_descriptor: object           — snapshot identifier for the legacy patch
                                                   corpus the dry-run ran against (patch-set hash
                                                   + count + version distribution)
      translation_outcomes: ordered list
        each: {patch_id_hash, source_version,
               target_version, outcome_enum,
               error_class (if outcome = failure)}
        outcome_enum: SUCCESS | TRANSLATION_FAILURE |
                      UNEXPECTED_VERSION_REJECTED
      aggregate_summary:
        total_patches: int
        success_count: int
        translation_failure_count: int
        unexpected_version_rejected_count: int
        per_transform_class_breakdown: object
      executor_cak_fingerprint: string
      executed_at_timestamp: ISO-8601
      artifact_schema_version: string (starts "1.0")

  Conditions:
    - Report MUST be signed by a CAK registered for dry-run execution authority
      (new scope: dry_run_executor; added to CAK registry schema).
    - Report MUST be written to the dry_run_artifact_store (below) before the
      manifest ratification ceremony is requested.
    - Report's manifest_hash MUST match the canonical hash of the manifest
      entry being submitted.

  Failure behavior:
    - Report write failure: ceremony cannot proceed; operator retries dry-run.
    - Report signature invalid at commit-gate read time: MANIFEST_COMMIT_REJECTED
      with verification_check_failed = DRY_RUN_SIGNATURE_INVALID (new Appendix C
      entry; additive to GS7 MANIFEST_COMMIT_REJECTED enum).
```

### 2.3 `dry_run_artifact_store` — Store Contract (D-GS8-C)

**Store properties:**
- Append-only. Existing artifacts may not be modified or deleted by agents.
- Content-addressed: the store key for any report is its content hash (matching the `dry_run_artifact_hash` field in IC-MANIFEST-1).
- Hash-chained into the Ledger via `DRY_RUN_ARTIFACT_STORED` entry (new Appendix C entry, GOVERNANCE, sync) emitted when a new artifact is written. This is the tamper-evidence anchor: altering a stored artifact would break the Ledger's Merkle-chain-lite integrity check.
- Retention: minimum **90 days** (wall-clock) from write timestamp. Covers the IC-MANIFEST-1 7-day freshness window with substantial margin for replay, audit, and post-incident forensics.
- Pruning after 90 days is permitted but governed by a signed retention ceremony (`DRY_RUN_ARTIFACT_PRUNED` entry; Ledger entry remains permanent even after artifact content is removed).

**Access control:**
- Write: only CAK-registered `dry_run_executor` scope.
- Read: Gate (for commit-gate verification), operator (via read-only UX), Warden (audit).
- No agent has direct write access to the store outside the dry-run execution path.

**Ledger entries added this session (NEW-GAP-28 closure):**
- `DRY_RUN_ARTIFACT_STORED` (GOVERNANCE, sync) — fields: `artifact_hash`, `manifest_hash`, `executor_cak_fingerprint`, `executed_at_timestamp`, `corpus_sample_descriptor_hash`
- `DRY_RUN_ARTIFACT_PRUNED` (GOVERNANCE, sync) — fields: `artifact_hash`, `pruned_at_timestamp`, `retention_ceremony_token_id`
- `DRY_RUN_SIGNATURE_INVALID` (SECURITY, sync) — appended to MANIFEST_COMMIT_REJECTED verification_check_failed enum

**Storage medium — deliberately unspecified.** The spec does not prescribe filesystem, object store, or content-addressable store backing. Operational assumption: any backing that satisfies append-only, content-addressed, and hash-chain-anchor properties is conformant. Not defended by spec mechanisms beyond the Ledger anchor.

---

## 3. T14 Candidate — Dry-Run Freshness vs. Manifest Authorship Cycle

### 3.1 Conflict Statement

GS7 set the `dry_run_artifact_hash` freshness window at 7 days. When manifest authorship extends beyond a week (Architect Agent drafting + human review + operator scheduling), the dry-run must be re-executed before ratification, potentially multiple times as review iterations occur. This is either acceptable operational cost or a misconfigured tradeoff.

### 3.2 Orchestration Comparativist — Framing

The freshness window protects against one specific failure mode: the active patch corpus drifts between dry-run execution and manifest commit, rendering the dry-run's statistical claims stale. The drift rate is a function of patch commit rate, not authorship cycle length.

A pure time-based window is a poor proxy for actual corpus drift. A direct test — "has the patch corpus changed since dry-run execution?" — is cheaper than re-running the dry-run and answers the actual question.

### 3.3 Resolution (D-GS8-D) — Corpus-Delta Freshness Check

Replace the pure 7-day time window with a **two-gate freshness check**:

**Gate A — corpus identity check (primary):**
At commit-gate verification time, compute the current `corpus_sample_descriptor` (patch-set hash + count + version distribution, same shape as the dry-run's recorded descriptor). Compare to the descriptor recorded in the dry-run report.

- If descriptors match (no patches added, removed, or version-changed since dry-run): freshness satisfied regardless of wall-clock age, up to a hard ceiling of 90 days (matching artifact retention).
- If descriptors differ: dry-run is stale; re-run required.

**Gate B — hard time ceiling (backstop):**
Independent of corpus state, a dry-run older than 90 days is considered stale. Protects against slow drift in model weights from accumulated commits that the corpus-identity check doesn't capture.

**Commit-gate verification check #7 updated:**
- Old (GS7): "Ceremony entry timestamp is within 7 days of commit attempt (provisional freshness)."
- New (GS8): "Gate A — corpus_sample_descriptor at commit time matches dry_run_report.corpus_sample_descriptor — OR — (Gate B fallback) dry_run executed_at_timestamp is within 90 days of commit attempt."

**Rejection entry:**
- `MANIFEST_COMMIT_REJECTED` `verification_check_failed` enum gains two values replacing the single prior `DRY_RUN_STALE`:
  - `DRY_RUN_CORPUS_DRIFTED` (Gate A failed)
  - `DRY_RUN_TIME_CEILING_EXCEEDED` (Gate B failed)

**T14 candidate status:** resolved. Operational cost of re-running dry-runs during extended authorship cycles eliminated for the common case (corpus stable). Safety preserved via Gate A (catches actual drift faster than 7-day window) and Gate B (backstops against weight drift).

---

## 4. NEW-GAP-29 — Cross-Agent Aggregate `SCOPE_UPDATE` Monitoring Spec Block (ratified)

### 4.1 Orchestration Comparativist — Framing

GAP-27 per-agent rate limit (`scope_update_min_interval_seconds`, default 3,600s, per-`agent_id`) is sound at the per-agent axis but leaves a residual documented at GS7 §2.2: a coordinated multi-`agent_id` spray can generate aggregate ceremony pressure above safe throughput while each individual agent stays within rate. The correct layer for a countermeasure is the Orchestrator — it observes all `agent_id` activity in aggregate, which no single agent does.

This is an **advisory-tier** mechanism, not a hard gate. Hard-gating at the aggregate level creates a new vulnerability surface (all agents blocked because of one misbehaving peer); advisory surfacing informs operator action without coupling unrelated agents.

### 4.2 Aggregate Advisory Spec (D-GS8-E)

Orchestrator maintains a **rolling aggregate window** of `SCOPE_UPDATE_ACCEPTED` Ledger entries across all `agent_id`:

- **Window:** rolling 60-minute wall-clock.
- **Advisory threshold (Tier 1):** aggregate count ≥ **N_agg_advisory** (provisional default: 50 ceremonies / 60 min). Emit `SCOPE_UPDATE_AGGREGATE_ADVISORY` (SECURITY, async).
- **Warning threshold (Tier 2):** aggregate count ≥ **N_agg_warning** (provisional default: 100 ceremonies / 60 min). Emit `SCOPE_UPDATE_AGGREGATE_WARNING` (SECURITY, sync).

**No Tier 3 hard-block at the aggregate level.** Deliberate. Hard-blocking at aggregate would couple otherwise-independent agents and create DoS-via-peer.

**Payload fields (both entries):**
- `window_start_timestamp`, `window_end_timestamp`
- `aggregate_count`
- `participating_agent_count` (distinct `agent_id` contributing to window)
- `top_n_agents` (list of (agent_id, count) for top 5 contributors — operational forensics; helps operator identify whether pressure is concentrated or distributed)

**Operator action surface:**
- Tier 1 advisory: logged; no operator action required unless persistent.
- Tier 2 warning: operator dashboard alert. Operator decides whether to tighten per-agent rate limits, revoke CAKs for suspicious agents, or take no action.

**Thresholds marked PROVISIONAL** — empirical tuning deferred to implementation phase deployment. Not blocked by GAP-1 (these are operational-throughput thresholds, not fidelity thresholds).

### 4.3 Ledger Entries Added

```
SCOPE_UPDATE_AGGREGATE_ADVISORY (SECURITY, async)
  Fields: window_start_timestamp, window_end_timestamp,
    aggregate_count, participating_agent_count, top_n_agents

SCOPE_UPDATE_AGGREGATE_WARNING (SECURITY, sync)
  Fields: window_start_timestamp, window_end_timestamp,
    aggregate_count, participating_agent_count, top_n_agents
```

---

## 5. Appendix C Additions This Session

```
SCOPE_UPDATE_AGGREGATE_ADVISORY       (SECURITY, async)
SCOPE_UPDATE_AGGREGATE_WARNING        (SECURITY, sync)
DRY_RUN_ARTIFACT_STORED               (GOVERNANCE, sync)
DRY_RUN_ARTIFACT_PRUNED               (GOVERNANCE, sync)
CALIBRATION_RATIFICATION (ceremony)   (GOVERNANCE, sync — follows GS4 CeremonyToken framework)

MANIFEST_COMMIT_REJECTED verification_check_failed enum extensions:
  + DRY_RUN_SIGNATURE_INVALID
  + DRY_RUN_CORPUS_DRIFTED          (replaces DRY_RUN_STALE when Gate A fails)
  + DRY_RUN_TIME_CEILING_EXCEEDED   (replaces DRY_RUN_STALE when Gate B fails)
  - DRY_RUN_STALE                   (deprecated; split into above two)
```

---

## Session Summary Block

═══════════════════════════════════════════════════════════════════════════════

**GAPS RESOLVED:**
- **NEW-GAP-28 — Dry-run artifact storage:** Closed. IC-DRYRUN-1 ratified; `dry_run_artifact_store` contract specified with append-only, content-addressed, Ledger-anchored properties; 90-day minimum retention; access control scoped to CAK-registered `dry_run_executor`. Three new Appendix C entries added (`DRY_RUN_ARTIFACT_STORED`, `DRY_RUN_ARTIFACT_PRUNED`, `DRY_RUN_SIGNATURE_INVALID`). Storage medium deliberately unspecified (operational assumption).
- **NEW-GAP-29 — Cross-agent aggregate SCOPE_UPDATE monitoring:** Closed. Advisory-tier spec (D-GS8-E) ratified with two tiers (advisory async, warning sync) over a rolling 60-minute window. Hard-block at aggregate level explicitly rejected to avoid DoS-via-peer. Thresholds provisional pending deployment tuning. Two new Appendix C entries.
- **T14 candidate — Dry-run freshness vs. manifest authorship cycle:** Resolved (D-GS8-D). Pure 7-day time window replaced with two-gate freshness check: Gate A (corpus_sample_descriptor identity match, primary), Gate B (90-day time ceiling, backstop). Commit-gate verification check #7 updated. GS7 `DRY_RUN_STALE` deprecated in favor of split `DRY_RUN_CORPUS_DRIFTED` / `DRY_RUN_TIME_CEILING_EXCEEDED`. T14 candidate closed — does not enter tension map as numbered tension.

**GAPS PARTIALLY RESOLVED:**
- **T13 M-threshold provisionals** and **IC-MANIFEST-1 bucket_map provisionals**: structural resolution path ratified (D-GS8-A calibration protocol; D-GS8-B bucket boundary determination). Actual numerical values remain pending GAP-1 empirical execution — not closable via spec work, but now have a defined measurement protocol producing a `CALIBRATION_RATIFICATION` ceremony output consumable by genesis-seal update.

**GAPS DEFERRED:**
- **GAP-1 itself** remains formally deferred (D-CRC-2) per v1.1. GS8 did not attempt to close GAP-1; it specified the protocol that consumes GAP-1's eventual empirical outputs.
- **N_agg_advisory / N_agg_warning thresholds** (NEW-GAP-29): provisional pending deployment-phase tuning. Not blocked by GAP-1 (operational-throughput, not fidelity).

**NEW GAPS SURFACED:**
- **NEW-GAP-30 (Low priority, owner: State Consistency Theorist):** Dry-run artifact store pruning ceremony authority. `DRY_RUN_ARTIFACT_PRUNED` is emitted under a signed retention ceremony, but the ceremony type is not yet integrated into the GS4 CeremonyToken framework. Needs assignment as `RETENTION_PRUNING` ceremony type or equivalent. Candidate for folding into GS10 Appendix cleanup.
- **NEW-GAP-31 (Medium priority, owner: MEMIT Specialist):** Probe set versioning for ε calibration. D-GS8-A references "canonical probe set (probe set defined at Genesis; see D81)" — probe set evolution across Genesis updates is not specified. If the probe set changes, historical ε values lose comparability. Needs probe-set versioning contract.

**NEW TENSIONS SURFACED:**
- None. All cross-domain interactions in GS8 (Warden ↔ Graph Data on artifact store; Orchestration ↔ Warden on aggregate advisory vs. hard-block) were resolvable within session.

**INTERFACE CONTRACTS FINALIZED THIS SESSION:**
- **IC-DRYRUN-1** (ratified) — Dry-Run Executor → Gate contract for dry_run_report shape and signing requirements.
- **IC-MANIFEST-1** (amended) — Commit-gate verification check #7 replaced; `bucket_map` field description updated to reflect per-transform-class calibration path.

**AMENDMENTS APPLIED THIS SESSION:**
- IC-MANIFEST-1 check #7 replacement (Gate A / Gate B freshness).
- IC-MANIFEST-1 `bucket_map` provisional semantics (`calibration_state: UNCALIBRATED` flag).
- `MANIFEST_COMMIT_REJECTED` verification_check_failed enum: `DRY_RUN_STALE` deprecated; two replacement values added.

**DECISIONS RATIFIED THIS SESSION:**
- **D-GS8-A** — `larql_fidelity_calibration` empirical protocol for ε measurement.
- **D-GS8-B** — Per-transform-class bucket boundary determination via calibration.
- **D-GS8-C** — `dry_run_artifact_store` append-only, content-addressed, Ledger-anchored contract; 90-day retention.
- **D-GS8-D** — Two-gate freshness check (corpus-identity primary, time-ceiling backstop).
- **D-GS8-E** — Aggregate SCOPE_UPDATE advisory-tier spec (two tiers, no hard-block at aggregate level).

**PHASE 2 EXIT STATUS:**
- T13 and GAP-20 core closures (GS7) unaffected and re-verified in light of GS8 augmentations.
- Provisionals on T13 and IC-MANIFEST-1 now have a defined resolution path — calibration protocol becomes an implementation-phase deliverable, not a spec-phase blocker.
- No new Phase 2 exit blockers introduced.

**NEXT SESSION (GS9) per gap-schedule-v3:**
- GS9 primary targets remain GAP-11, GAP-12, GAP-14, GAP-28. GS8 outputs feed GS9 only indirectly (NEW-GAP-31 probe-set versioning and NEW-GAP-30 pruning ceremony are both Low–Medium priority and can cluster into GS10 Appendix cleanup rather than forcing GS9 scope expansion).
- Recommend triaging NEW-GAP-30 and NEW-GAP-31 into gap-backlog-v4 before GS9 opens.

═══════════════════════════════════════════════════════════════════════════════

*End of GS8 summary — input baseline for GS9.*
