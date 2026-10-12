# Gap Session 11 of 12 — Summary

**Session:** Gap Resolution 11 / 12
**Specialists convened:** State Consistency Theorist, Orchestration Comparativist
**Baseline:** v1.1 Integrated Spec + GS5–GS10 resolutions
**Gaps addressed:** GAP-12 (Ledger retention policy), GAP-14 (async threshold rationale suite), GAP-28 (Orchestrator scope-notification obligation)

---

## Session Framing

This session closes the Ledger operational-policy triad. Three gaps share a single structural concern: what *policy* applies to the Ledger and its consumers over long horizons, once the v1.1 structural spec is fixed. GAP-12 asks what survives (retention / archival). GAP-14 asks what is *checked* along the way (async thresholds, verification cadence, backlog signals). GAP-28 asks what *participants* are told when coordination state changes (scope-update notification).

The State Consistency Theorist owns the Ledger's consistency contract and the rationale for any threshold that gates integrity verification. The Orchestration Comparativist owns the coordination obligation between Orchestrator and agents for scope updates, and co-owns async thresholds where they intersect orchestrator behavior. No Warden co-review is triggered *structurally* by this session — retention floor, archival format, and threshold-update ceremony all route through the existing IC-LDG-RETAIN / GOVERNANCE writer paths already ratified under Warden oversight.

---

## GAP-12 Resolution — Ledger Retention, Archival Format, Finalization Path

### Resolution 1 — Retention Floor is Tier 1; Extensions are Additive Overlays

The minimum retention floor declared at `PROJECT_INITIATED` is **Tier 1 Immutable Anchor**, not Tier 3 Anchored Git Config.

Rationale: Tier 3 artifacts are adjustable via Git commit. Placing the retention floor in Tier 3 would create a direct bypass around the signed-ceremony requirement of C-SL2 — an operator could shorten retention with a Git commit, no signature required. The C-SL2 immutable-downward invariant is only enforceable if the floor itself is mint-once Tier 1. This confirms and crystallizes the §16.7 language ("immutable post-mint") against the Tier taxonomy.

**The floor is immutable. Extensions are not modifications to the floor — they are additive overlays.** The effective retention at any time is `max(floor, max(all RETENTION_OVERRIDE_EXTENDED entries))`. This framing cleanly preserves C-SL2: no operation can reduce the effective retention below the floor, because the floor cannot change and extensions only add to it. `RETENTION_OVERRIDE_EXTENDED` entries are append-only in the Ledger; there is no "retract extension" ceremony by design.

Operators **cannot adjust the retention period downward at all** after bootstrap, under any governance. The only post-bootstrap retention operation is extension.

### Resolution 2 — Archival Bundle Format v1.0

The archival format identifier is `"ledger-epoch-bundle/1.0"`. The format is declared explicitly to permit future migration — any future format version requires a signed ceremony and is recorded in a Tier 1 `archive_format_manifest` (parallel to `larql_migration_manifest`).

**Bundle structure:**

```
<harness_root>/.state-ledger/archive/{epoch_bundle_N}/
  format-identifier.txt        # "ledger-epoch-bundle/1.0"
  entries.jsonl.gz             # gzip of the epoch's entries in Merkle order
  manifest.json                # signed integrity manifest (see schema below)
  manifest.sig                 # operator signature over manifest.json
```

**Manifest schema (required fields, format-version 1.0):**

```
archive_manifest := {
  format_version:            "1.0",
  epoch_id:                  <opaque identifier, monotonically increasing>,
  epoch_start_entry_hash:    <sha256 of first entry in epoch>,
  epoch_end_entry_hash:      <sha256 of last entry in epoch>,
  anchor_event_id:           <ANCHOR_ESTABLISHED id that closed this epoch>,
  entry_count:               <integer>,
  first_entry_timestamp:     ISO8601,
  last_entry_timestamp:      ISO8601,
  merkle_root_at_archival:   <sha256 over the epoch's Merkle-chain-lite tail>,
  bundle_sha256:             <sha256 of entries.jsonl.gz>,
  hash_algorithm:            "sha256",   // explicit per-manifest; permits migration
  integrity_violation_count: <integer>,  // drives indefinite-retention invariant
  contains_integrity_violation: <bool>,
  signing_key_id:            <operator key identifier>,
  signing_timestamp:         ISO8601,
  predecessor_bundle_id:     <epoch_bundle_{N-1}> | null,     // chain-of-archives linkage
  predecessor_bundle_hash:   <sha256 of predecessor manifest.json> | null
}
```

**Chain-of-archives linkage:** Each manifest carries its predecessor bundle's id and manifest hash. This extends Merkle-chain-lite integrity *across* the archival boundary — a tampered archive cannot be silently substituted for a later one, because the subsequent bundle's manifest will not validate.

**Restore procedure:**

1. Verify `bundle_sha256` against `entries.jsonl.gz`.
2. Verify operator signature on `manifest.json` against `signing_key_id` from Tier 1 key registry.
3. Verify predecessor linkage if applicable.
4. Decompress `entries.jsonl.gz`; verify Merkle-chain-lite continuity internal to the bundle.
5. Verify `epoch_end_entry_hash` matches the predecessor-hash field of the next epoch's first entry (cross-bundle chain continuity).
6. Mount as read-only view at `<harness_root>/.state-ledger/restored/{epoch_bundle_N}/`. Restore is a read operation; it never writes back to the active Ledger.

**Forensic readability across multi-year horizons:** format-version 1.0 is declared in plaintext (`format-identifier.txt`) alongside the bundle. A future auditor without access to the running harness can read the plaintext format identifier, decompress with any gzip tool, and verify with any SHA-256 implementation. Signature verification requires access to the archived operator public key, which is itself a Tier 1 artifact (`orchestrator-key-anchor.json`) snapshotted in each Genesis Seal family.

**Indefinite-retention invariant surface:** `integrity_violation_count > 0` OR `contains_integrity_violation = true` flags the bundle for indefinite retention and is checked by the archival reaper before any deletion attempt. The Ledger layer refuses deletion of any bundle with this flag set, regardless of operator key validity.

### Resolution 3 — PROJECT_CLOSED is the Sole Finalization Path; No Quiescence-Based Archival

**`PROJECT_CLOSED` is the only mechanism that finalizes the Ledger (seals final epoch, makes Ledger read-only).** There is no quiescence-based or time-based implicit finalization.

Rationale: rolling archival of old epochs already happens continuously via `ANCHOR_ESTABLISHED`. A long-running project that never invokes `PROJECT_CLOSED` simply continues to archive epochs indefinitely as anchors are established — this is the *expected* steady state. The Ledger remains writeable; the old epochs are cold-stored; nothing is lost; nothing is forced.

Introducing a quiescence-based archival path (e.g., "no writes for 180 days → auto-close") would create an undefined state: a project that could silently transition from writeable to read-only without operator awareness, potentially leaving operational workflows broken after a project-dormancy window. This is explicitly rejected. Ledger finalization is always an explicit operator act.

Operational implication: operators who wish to archive a project without formally closing it simply let ANCHOR_ESTABLISHED events drive archival. The Ledger remains ready to accept new writes if the project resumes. PROJECT_CLOSED is reserved for the case where the project is genuinely done and the Ledger should become permanently read-only.

### Spec Blocks (GAP-12)

```
### Ledger Retention Floor — Spec Block
What it must guarantee:
  The minimum Ledger entry retention period declared at PROJECT_INITIATED is
  immutable post-mint under all governance paths. Effective retention may only
  grow; it may never shrink.

Hard constraints:
  - Retention floor is a Tier 1 Immutable Anchor field (not Tier 3).
  - Set exactly once via PROJECT_INITIATED (W2 bootstrap writer, mint-once).
  - No governance ceremony exists that can lower the floor. C-SL2 preserved.
  - Effective retention = max(floor, max(RETENTION_OVERRIDE_EXTENDED entries)).
  - RETENTION_OVERRIDE_EXTENDED entries are append-only; no retraction ceremony.
  - Indefinite-retention invariant (epochs with INTEGRITY_VIOLATION) dominates
    over any configured retention value.

Tradeoffs decided:
  - Tier 1 over Tier 3: chose mint-once immutability over Git-commit-adjustable
    flexibility. Cost: an operator cannot correct a poorly chosen floor at
    bootstrap without extending it (cannot shrink). Benefit: C-SL2 is
    structurally enforceable rather than relying on Gate-layer checks alone.
  - Additive-overlay model for extensions over in-place modification: preserves
    a clear audit trail of every retention decision. Cost: the Ledger carries
    multiple RETENTION_OVERRIDE_EXTENDED entries over a project lifetime.
  - No quiescence-based archival path: rejected the alternative of implicit
    finalization after a dormancy window, because it would create a silent
    writeable→read-only transition. PROJECT_CLOSED remains the sole
    finalization path.

Open questions (deferred):
  - Default floor value when PROJECT_INITIATED omits the field: currently
    PROJECT_LIFETIME. Whether a policy-driven minimum (e.g., 7 years for
    regulated domains) should replace the default is a deployment-profile
    decision, not a framework decision.

Interface contract:
  IC-LDG-RETAIN (extended):
    floor_tier:          Tier 1 Immutable Anchor
    extension_entries:   append-only RETENTION_OVERRIDE_EXTENDED sequence
    effective_retention: max(floor, max(extensions))
    reduction_path:      NONE — structurally unreachable
    indefinite_override: INTEGRITY_VIOLATION epochs retained INDEFINITELY
                         regardless of configured value
```

```
### Ledger Archival Bundle Format v1.0 — Spec Block  ⚑ WARDEN CO-REVIEW
What it must represent:
  The on-disk format for a cold-stored Ledger epoch, sufficient for forensic
  verification by an auditor years after the project is closed, using only
  the bundle itself and archived Tier 1 key material.

Hard constraints:
  - Format identifier "ledger-epoch-bundle/1.0" declared in plaintext beside
    bundle contents.
  - Compression: gzip. Integrity hash: SHA-256. Hash algorithm declared
    per-manifest (not global) to permit future migration.
  - Manifest schema includes predecessor_bundle_id and predecessor_bundle_hash
    fields, extending Merkle-chain-lite integrity across the archival boundary.
  - Operator signature on manifest.json required at archive time; signing key
    must be an identity listed in the corresponding Genesis Seal's
    orchestrator-key-anchor.json snapshot.
  - contains_integrity_violation = true flags the bundle for INDEFINITE
    retention; archival reaper refuses deletion of any flagged bundle.
  - Format version advance requires signed ceremony and Tier 1
    archive_format_manifest update (parallel to larql_migration_manifest).

Tradeoffs decided:
  - Plaintext format identifier file over metadata-only declaration: redundancy
    accepted for forensic readability across decades where tooling evolves.
  - Chain-of-archives linkage (predecessor hash in each manifest) over bundle-
    level isolation: stronger tamper-detection guarantee at the cost of
    ordering constraint on archival restoration.
  - SHA-256 as default with explicit per-manifest algorithm declaration:
    permits migration to a stronger hash without re-archiving history.

Open questions (deferred):
  - Cold-storage medium selection (object store vs. tape vs. operator choice):
    deployment-specific.
  - Key rotation for long-dormant archives where the original signing key has
    been retired: whether bundle re-signing is required and under what
    ceremony. Intersects Warden key-lifecycle policy; flagged for Warden
    review in a future session.

Interface contract:
  IC-LDG-ARCH (new):
    format_id:         "ledger-epoch-bundle/1.0"
    bundle_layout:     {format-identifier.txt, entries.jsonl.gz,
                        manifest.json, manifest.sig}
    manifest_schema:   <as declared above>
    restore_op:        read-only mount at .state-ledger/restored/{bundle_id}/
    verify_op:         six-step restore procedure (see resolution body)
    integrity_reaper:  refuses deletion when contains_integrity_violation=true

  Before this IC is closed, the Warden must confirm:
    - Key-lifecycle policy for bundles whose signing key has been retired.
    - Whether signing-key material snapshotted in Genesis Seal family is
      sufficient authority for decades-later signature verification, or
      whether a separate key-archive ceremony is required.
```

```
### Ledger Finalization Path — Spec Block
What it must guarantee:
  A single, operator-initiated path from writeable Ledger to read-only Ledger.
  No implicit or time-triggered finalization.

Hard constraints:
  - PROJECT_CLOSED (LIFECYCLE, signed ceremony) is the sole finalization path.
  - No quiescence timer, dormancy threshold, or calendar-based auto-close.
  - Rolling epoch archival via ANCHOR_ESTABLISHED continues indefinitely
    while the project is open; this is the expected steady state for
    long-running projects.
  - PROJECT_CLOSED is write-final even if cold storage is unavailable at
    close time (archival is retried; Ledger read-only state is immediate).

Tradeoffs decided:
  - Explicit-only finalization over quiescence-triggered: rejected the
    implicit path because it would create an undefined writeable→read-only
    transition invisible to operators. Cost: long-dormant projects remain
    nominally open. Benefit: no silent state change.

Open questions (deferred):
  - Operational guidance for long-dormant projects (e.g., should a 5-year-
    dormant project be proactively closed?) — policy recommendation, not a
    framework constraint.

Interface contract:
  IC-LDG-FINAL (reaffirmed from §16.7):
    finalization_trigger:  PROJECT_CLOSED signed ceremony only
    pre_close_archival:    ongoing via ANCHOR_ESTABLISHED (no dependency)
    post_close_state:      read-only; archival retries permitted; no writes
    reversibility:         NONE — finalization is terminal
```

---

## GAP-14 Resolution — Async Threshold Rationale Framework

### Resolution 4 — Threshold Guarantees and Failure Modes

Each provisional threshold is specified with (a) the guarantee it serves, (b) the failure mode if set too low, and (c) the failure mode if set too high. Numeric values remain provisional pending empirical validation; the *policy rationale* below is not provisional.

**WAL flush cadence:**
- **Guarantee served:** bounds the data-loss window on orchestrator crash for async Ledger writes. The window is the maximum duration between a write being acknowledged and the WAL being durably flushed.
- **Too low (aggressive flush):** excessive disk I/O, especially under async-write-heavy workloads (Meta-Validator health records, observation entries). Can become a throughput bottleneck and paradoxically degrade the very observations the async path was intended to be cheap for.
- **Too high (lazy flush):** larger data-loss window; observation entries lost on crash may obscure the root cause of the crash itself. Meta-Validator/Meta-TGA health signals are the most valuable async entries; losing their tail is the highest-cost failure mode.
- **Target bound (policy):** the flush cadence must guarantee a data-loss window of ≤ N seconds where N is the maximum acceptable blind-spot in post-crash forensic reconstruction. N is deferred empirically; the *property* (bounded blind-spot) is not.

**Light verification interval (every 100 entries):**
- **Guarantee served:** bounds the Merkle-chain-lite corruption-detection window. Between any two consecutive light verifications, at most 100 entries may have accumulated over a corrupted predecessor.
- **Too low (frequent):** verification cost dominates normal append cost; may suppress legitimate write throughput under burst load.
- **Too high (infrequent):** corruption can propagate into committed 2PC cycles or into epoch archival before detection. The catastrophic scenario is corruption detected *after* an epoch has been archived — the chain-of-archives integrity model depends on each bundle's predecessor having been verified before sealing.
- **Verifies:** last ~10 entries (per §16.4). Policy constraint: light verification must always include the tail of the chain, never a midsection, because corruption is most likely at the write frontier.

**Full verification interval (every 10,000 entries OR 24 hours):**
- **Guarantee served:** bounds *audit-completeness staleness*. Any corruption anywhere in the chain is guaranteed to be detected within one full-verification interval. This is the spec's answer to "how long could a silent corruption persist undetected?" — worst case, one full interval.
- **Too low (frequent):** cost scales with chain length; on a multi-year Ledger with millions of entries, full verification becomes expensive. This is the cost-model justification for deferring full verification relative to light verification.
- **Too high (rare):** the audit-completeness window extends, raising the risk that corruption has already been baked into archived epochs by the time it is detected.
- **Compound trigger (10,000 entries OR 24h):** covers both high-volume and low-volume operational regimes. A dormant project still gets daily verification; a high-throughput project still gets verification at every 10K-entry milestone. The OR semantics ensure neither regime creates a coverage gap.

**Reconciliation backlog thresholds (10/7d warning; 50/30d critical):**
- **Guarantee served:** proxies for an out-of-band reconciliation SLA. The thresholds encode an operational assumption about reviewer responsiveness and queue health.
- **Warning (10 items OR any >7 days):** signals that the queue is no longer at normal operational tempo. 10 items is the assumed steady-state ceiling under healthy reviewer responsiveness. 7 days is the assumed maximum reviewer turnaround for an individual item before the queue is considered stale.
- **Critical (50 items OR any >30 days):** signals systemic neglect — either reviewers are unavailable or the reconciliation pipeline is broken. At this level, the Consistency Status state itself changes (`RECONCILIATION_BACKLOG`), which may gate downstream write operations depending on operator policy.
- **Too low:** false-positive escalation noise desensitizes operators to the signal.
- **Too high:** genuine backlogs accumulate silently; out-of-band Git commits pile up unreconciled until the resulting `.vindex` drift becomes non-recoverable without extensive forensic work.
- **`stale_urgent > 1,000` independent threshold:** separate failure mode (Pruning Agent backlog), triggers write suspension directly. This threshold serves a different guarantee (graph coherence) and is not on the same rationale axis as the reconciliation queue.

### Resolution 5 — Threshold Update Ceremony

Thresholds in GAP-14 scope are **Tier 3 Anchored Git Config**, not Tier 1. These values are operational tuning parameters informed by observed system behavior; operators must be able to adjust them without a mint-once ceremony.

However, Tier 3 placement does not mean uncontrolled adjustment:

**Ceremony:**
- A threshold change is submitted as a Git commit to `.harness/async-thresholds.json` (Tier 3 artifact).
- The commit triggers a pre-receive Git hook (consistent with other Tier 3 artifacts per §5 / §13.4) that:
  1. Validates the proposed value is within declared hard bounds (see Hard Bounds below).
  2. Emits `THRESHOLD_UPDATED` Ledger entry (GOVERNANCE, sync) carrying `threshold_name`, `previous_value`, `new_value`, `operator_signature`, `rationale` (required free-text field ≥ 20 chars).
  3. On hook failure (value out of bounds OR missing signature OR missing rationale), the commit is rejected pre-receive. Rejection emits `THRESHOLD_UPDATE_REJECTED` (GOVERNANCE, sync).

**Hard bounds (policy; not operator-tunable):**

| Threshold | Min | Max | Unit |
|---|---|---|---|
| WAL flush cadence | 100ms | 30s | time |
| Light verification interval | 10 | 10,000 | entries |
| Full verification entry trigger | 1,000 | 1,000,000 | entries |
| Full verification time trigger | 1h | 168h | time |
| Reconciliation warning: item count | 5 | 100 | items |
| Reconciliation warning: age | 1d | 30d | time |
| Reconciliation critical: item count | 25 | 500 | items |
| Reconciliation critical: age | 7d | 180d | time |

The bounds are **Tier 1 Immutable** — the *tuning space* is fixed at bootstrap; the *chosen value within the space* is Tier 3.

Additional constraint: `light_verification_interval < full_verification_entry_trigger / 10` (ratio invariant; full verification must meaningfully exceed light verification frequency or the two collapse into redundancy).

**Authority:** operator signature required, same key class as Tier 3 Anchored Git Config modifications.

### Spec Blocks (GAP-14)

```
### Async Threshold Rationale Framework — Spec Block
What it must represent:
  For every provisional async threshold in §16.3 / §16.4 / §15.2, a specified
  guarantee-served / failure-mode-too-low / failure-mode-too-high triplet.
  Numeric values remain empirically deferred; the rationale is not.

Hard constraints:
  - Every threshold in the WAL/verification/backlog set MUST have a named
    guarantee in the Ledger consistency contract. A threshold with no named
    guarantee is an incomplete spec and must not be shipped.
  - Failure modes at both extremes (too low / too high) must be enumerated
    before a value is declared provisional.
  - The compound trigger pattern (entry-count OR time) is preferred for any
    threshold whose corruption-detection guarantee must hold across both
    high-volume and low-volume regimes.

Tradeoffs decided:
  - Bifurcation of policy from empirical value: rationale is specified now;
    value is deferred to empirical calibration. Chose this split over
    waiting for empirical data before specifying rationale, because the
    rationale constrains the value and must be in place before calibration
    begins.
  - Separate stale_urgent threshold kept distinct from reconciliation
    backlog thresholds: they serve different guarantees (graph coherence
    vs. out-of-band sync SLA) and should not be conflated under a single
    tuning axis.

Open questions (deferred):
  - Empirical calibration of all numeric values (inherits from T5/T11 and
    GAP-1). Resolution requires write-volume and hardware measurements the
    framework spec does not attempt to supply.
  - Whether full verification should scale sub-linearly with chain length on
    very large Ledgers (e.g., sampled verification with probabilistic
    coverage guarantee). Deferred as a future optimization.

Interface contract:
  IC-ASYNC-THRESH (new):
    threshold_record := {
      name, category, guarantee_served, failure_mode_low,
      failure_mode_high, current_value, hard_min, hard_max,
      tier_classification: "Tier 3 (value) / Tier 1 (bounds)"
    }
    All async-threshold touching spec blocks reference this record by name.
```

```
### Threshold Update Ceremony — Spec Block  ⚑ WARDEN CO-REVIEW
What it must enforce:
  Every change to an async threshold (WAL flush cadence, verification
  intervals, reconciliation backlog thresholds) is Ledger-recorded,
  operator-signed, rationale-annotated, and bounded.

Hard constraints:
  - Threshold values: Tier 3 Anchored Git Config.
  - Threshold bounds (min/max): Tier 1 Immutable Anchor.
  - Pre-receive Git hook validates proposed value in-bounds, signature
    present, rationale ≥ 20 chars. Out-of-bounds rejected pre-commit.
  - THRESHOLD_UPDATED (GOVERNANCE, sync) emitted on every accepted change.
  - THRESHOLD_UPDATE_REJECTED (GOVERNANCE, sync) emitted on hook rejection.
  - Ratio invariant enforced: light_verification_interval <
    full_verification_entry_trigger / 10.

Tradeoffs decided:
  - Tier 3 for values over Tier 1: retains operational tunability required
    for empirical calibration. Cost: values can be changed without a
    mint-once ceremony. Mitigated by hard bounds (Tier 1) + Ledger audit
    trail + rationale requirement.
  - Free-text rationale (≥20 chars) over enumerated-reason field: rationale
    for a threshold change is inherently contextual; enumerated options
    would either be too coarse or multiply indefinitely.

Open questions (deferred):
  - Automated tuning proposals (e.g., an advisory agent that monitors
    threshold-relevant metrics and proposes changes): out of scope here;
    any such agent would submit through the same ceremony as a human
    operator and gains no privilege.

Interface contract:
  IC-THRESHOLD-UPDATE (new):
    update_path:       Git commit → pre-receive hook → Ledger entry
    ledger_entry:      THRESHOLD_UPDATED { threshold_name, previous_value,
                         new_value, operator_signature, rationale }
    rejection_entry:   THRESHOLD_UPDATE_REJECTED { threshold_name,
                         proposed_value, rejection_reason }
    bounds_source:     Tier 1 config (hard_min, hard_max per threshold)
    authority:         operator signature, Tier 3 Anchored Git Config class

  Before this IC is closed, the Warden must confirm:
    - Whether the pre-receive hook itself requires integrity verification
      on each invocation (defense against hook tampering).
    - Whether THRESHOLD_UPDATE_REJECTED entries should carry the operator
      identity of the attempt (surveillance on repeated failed attempts).
```

---

## GAP-28 Resolution — Scope-Update Notification Obligation

### Resolution 6 — D91 Ratified With Amendment: Single-Attempt, Outcome-Logged

D91 is **ratified**: the Orchestrator notifies agents in `affected_agent_ids` on best-effort basis; agents must not rely on proactive notification for safety-critical behavior; Gate rejection remains the authoritative enforcement mechanism.

**Amendment:** "best-effort" is now specified as **single-attempt, outcome-logged, time-bounded**:

- Exactly one notification attempt per affected agent, per `SCOPE_UPDATED` event.
- Each attempt's outcome is recorded in a `SCOPE_NOTIFICATION_ATTEMPTED` Ledger entry (async).
- Attempt must begin within a bounded delay after `SCOPE_UPDATED` (default: 5 seconds; Tier 3 tunable via the same ceremony as other async thresholds — this is an async threshold and inherits IC-THRESHOLD-UPDATE).
- Attempt outcome is one of: `DELIVERED` | `UNREACHABLE` | `TIMEOUT`. A `DELIVERED` outcome is purely informational — it does not imply the agent acted on it. Gate rejection remains the only authoritative signal.
- No retry on `UNREACHABLE` or `TIMEOUT`. Retries would create ambiguity about which notification carried the "current" scope and would subtly invite agents to wait for a delivery confirmation that is not guaranteed.

**Mechanism (underspecified by design):** the spec names the *obligation*, not the *transport*. Whether the Orchestrator uses an in-memory signal, an async queue, direct invocation, or an out-of-process channel is implementation-layer. The obligation is:

1. Attempt must happen within the bounded delay.
2. Outcome must be Ledger-recorded.
3. No retry beyond the single attempt.
4. Failure to notify must not block or delay the `SCOPE_UPDATED` write (the Ledger entry is authoritative; notification is advisory).

### Resolution 7 — OQ-S-GAP28-1 Reconfirmed Closed; Per-Type Notification Policy Baseline

Per the GS4 closure of OQ-S-GAP28-1: `scope_change_type` is a mandatory field in the `SCOPE_UPDATED` Ledger entry and in the upstream `SCOPE_UPDATE` CeremonyToken payload. Values: `EXPANDING | NARROWING | RESTRUCTURING`.

This session ratifies GS4's closure and adds the **per-type notification policy baseline** — what the per-type distinction is *for*:

| `scope_change_type` | Meaning | Notification priority | Rationale |
|---|---|---|---|
| `EXPANDING` | New tools/capabilities added; no existing capability removed | `NORMAL` | Agents in-flight are unaffected; their existing behavior remains valid. Notification is courtesy only. |
| `NARROWING` | Tools/capabilities removed; prompt content reduced | `HIGH` | Agents in-flight may be executing calls that will now fail at Gate. Early notification lets the Orchestrator (or the agent, if it receives the signal in time) abandon the call and re-plan, reducing wasted Reflexion cycles. |
| `RESTRUCTURING` | Mixed (both additions and removals) OR prompt-content change OR tool-contract semantic change without removal | `HIGH` | Semantic change; in-flight agent behavior cannot be assumed compatible. Treat as NARROWING in practice. |

Priority is surfaced in the `SCOPE_NOTIFICATION_ATTEMPTED` Ledger entry as a `priority` field. **The Orchestrator MAY apply per-type logic at its discretion** — this is a recommended baseline, not a mandate. The framework does not require that `HIGH` priority notifications use a faster transport than `NORMAL` ones; it only requires that the priority classification be recorded for auditability.

Rationale for not mandating per-type transport differences: prescribing transport behavior would conflict with the orchestration-agnostic stance of this skill. The framework specifies that the distinction *exists* and *is recorded*; operator-chosen orchestrators may or may not surface it as a routing signal.

### Spec Blocks (GAP-28)

```
### Scope Update Notification Obligation — Spec Block
What it must enforce:
  A single-attempt, outcome-logged, time-bounded notification from the
  Orchestrator to each agent listed in affected_agent_ids on every
  SCOPE_UPDATED event. Notification is advisory; Gate rejection is
  authoritative.

Hard constraints:
  - Exactly one notification attempt per affected agent per SCOPE_UPDATED.
  - Attempt must begin within bounded delay (default 5s; Tier 3 tunable).
  - SCOPE_NOTIFICATION_ATTEMPTED (async) Ledger entry records every
    attempt with outcome ∈ {DELIVERED, UNREACHABLE, TIMEOUT}.
  - No retry on UNREACHABLE or TIMEOUT.
  - Notification failure MUST NOT block or delay the SCOPE_UPDATED write.
  - Agents MUST NOT rely on notification delivery for safety-critical
    behavior. Gate-pre-check step 4 remains the authoritative enforcement
    (SCOPE_HASH_MISMATCH).

Tradeoffs decided:
  - Single-attempt over bounded-retry: rejected retry because it would
    create ambiguity about which notification carries the "current" scope
    and would subtly invite agents to wait for a delivery confirmation
    the framework does not guarantee. Cost: a lost notification is
    permanently lost; agents will discover the change at Gate rejection.
    This is the intended safety-critical path.
  - Transport unspecified: rejected prescribing a specific channel
    (in-memory / queue / direct invocation) to preserve orchestration
    agnosticism. Cost: interoperability testing between orchestrators
    must confirm obligation compliance, not channel compatibility.
  - Async Ledger entry for notification outcome: DELIVERED is not a
    security-critical signal; async write mode is appropriate. Cost:
    SCOPE_NOTIFICATION_ATTEMPTED may be lost on crash within WAL window,
    which is acceptable because Gate rejection remains authoritative.

Open questions (deferred):
  - Operational guidance for orchestrators whose transport inherently
    supports delivery confirmation (e.g., ack-based message queue):
    whether the spec should permit such orchestrators to surface
    DELIVERED with a stronger semantic. Deferred as implementation-time
    detail per GAP-28 prior note.

Interface contract:
  IC-SCOPE-NOTIFY (new):
    trigger:           SCOPE_UPDATED Ledger entry (from IC-SCOPE-UPDATE)
    obligation:        one attempt per affected_agent_id within bounded delay
    outcome_entry:     SCOPE_NOTIFICATION_ATTEMPTED (async) {
                         affected_agent_id, scope_update_event_id,
                         outcome: {DELIVERED | UNREACHABLE | TIMEOUT},
                         priority: {NORMAL | HIGH},
                         attempt_timestamp
                       }
    authoritative_enforcement: Gate pre-check #4 (SCOPE_HASH_MISMATCH)
    transport:         unspecified (orchestration-layer concern)
```

```
### Per-Type Notification Policy Baseline — Spec Block
What it must represent:
  The recommended baseline mapping from scope_change_type to notification
  priority. Orchestrator MAY apply per-type routing logic; framework
  requires only that the classification be recorded.

Hard constraints:
  - scope_change_type is already a mandatory field in SCOPE_UPDATED
    (closed GS4). This block does not re-open that decision.
  - SCOPE_NOTIFICATION_ATTEMPTED entries MUST carry the priority field
    regardless of whether the orchestrator uses it for routing.
  - Baseline priority mapping:
      EXPANDING   → NORMAL
      NARROWING   → HIGH
      RESTRUCTURING → HIGH
  - Orchestrator-specific overrides permitted; override must be declared
    in orchestrator configuration and is itself a Tier 3 artifact.

Tradeoffs decided:
  - Recommended baseline vs. mandated policy: rejected the mandated
    version to preserve orchestration agnosticism. Cost: different
    orchestrators may handle the same scope change with different urgency;
    cross-orchestrator operational playbooks must account for this.
    Benefit: the framework does not prescribe transport-layer behavior.
  - RESTRUCTURING treated as HIGH (same as NARROWING) rather than as a
    third distinct priority: in practice, semantic prompt changes without
    removals can still invalidate in-flight agent assumptions. A third
    priority level would add ceremony without operational benefit.

Open questions (deferred):
  - Whether a fourth scope_change_type should be introduced for
    "purely metadata change" cases that do not affect agent behavior at
    all. Not needed per the GS4 enumeration; flagged for future revisit
    if operational data suggests many SCOPE_UPDATED events fall outside
    the current three categories.

Interface contract:
  IC-SCOPE-NOTIFY-PRIORITY (extension of IC-SCOPE-NOTIFY):
    baseline_mapping:  {EXPANDING: NORMAL, NARROWING: HIGH,
                        RESTRUCTURING: HIGH}
    orchestrator_override_permitted: true (Tier 3 config)
    priority_field_mandatory: true (on SCOPE_NOTIFICATION_ATTEMPTED)
```

---

## Cross-Domain Synthesis Notes

**Threshold ceremony and retention ceremony share a governance pattern.** Both GAP-12 and GAP-14 resolutions use the Tier 1 bounds / Tier 3 values split. This is now a pattern the spec can reference for future operational-tuning parameters: the *space* of acceptable values is immutable; the *chosen value within the space* is tunable with audit trail. This pattern name — "bounded tunability" — is offered for future spec work.

**No Warden co-review was blocking in this session.** Two spec blocks are flagged `⚑ WARDEN CO-REVIEW` (archival bundle format v1.0, threshold update ceremony) with specific questions enumerated, consistent with the State Ledger joint-ownership rule. These questions are forward-pointed to a future session that includes the Warden, not blocking this session's output.

**Orchestration agnosticism held under pressure.** GAP-28's resolution resisted prescribing transport mechanism despite the temptation to specify delivery-guarantee behavior. The spec records the *obligation*; the orchestrator-layer records the *implementation*. This is consistent with the Orchestration Comparativist's stated non-advocacy stance.

---

## Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-12** — Ledger retention policy fully specified. Retention floor placed at Tier 1 Immutable Anchor (set once via PROJECT_INITIATED; no shortening path exists). Extensions modeled as additive overlays preserving C-SL2 structurally. Archival bundle format v1.0 specified with complete manifest schema, chain-of-archives linkage, and six-step restore procedure. PROJECT_CLOSED confirmed as sole finalization path; quiescence-based archival explicitly rejected.
- **GAP-14** — Async threshold rationale framework specified for all thresholds in §16.3 / §16.4 / §15.2 (WAL flush cadence, light and full verification intervals, reconciliation backlog warning and critical thresholds). Each threshold has named guarantee-served, failure-mode-too-low, failure-mode-too-high. Threshold update ceremony specified with Tier 3 values / Tier 1 bounds split ("bounded tunability"), pre-receive Git hook enforcement, Ledger-recorded outcome with operator signature and mandatory rationale.
- **GAP-28** — D91 ratified with amendment specifying notification as single-attempt, outcome-logged, time-bounded. SCOPE_NOTIFICATION_ATTEMPTED (async) entry type introduced. Per-type notification policy baseline specified (EXPANDING → NORMAL; NARROWING / RESTRUCTURING → HIGH) while preserving orchestration-layer latitude. OQ-S-GAP28-1 reconfirmed closed per GS4; `scope_change_type` remains mandatory on SCOPE_UPDATED.

**GAPS PARTIALLY RESOLVED:** none.

**GAPS DEFERRED:**
- Empirical calibration of async threshold numeric values (inherits from T5/T11 and GAP-1; requires write-volume and hardware measurement).
- Key-lifecycle policy for long-dormant archived bundles whose signing key has been retired — flagged for future Warden-inclusive session.
- Whether the archival format's pre-receive hook itself requires runtime integrity verification (defense against hook tampering) — flagged for Warden review.
- Policy-driven default retention floor (e.g., 7-year regulated-domain default) — treated as deployment-profile concern, not framework concern.
- Automated threshold tuning proposals from an advisory agent — out of scope; any such agent uses the same ceremony as a human operator.
- Operational guidance for long-dormant projects (proactive close threshold) — policy recommendation, not framework constraint.

**NEW GAPS SURFACED:**
- **GAP-16 (new)** — Archive key-lifecycle policy. When a bundle's signing key has been retired from the active Orchestrator Key Anchor (e.g., 10+ years after archival), restoration requires access to archived key material. Whether the Genesis Seal family snapshot is forensically sufficient across decadal horizons, or whether a separate key-archive ceremony is required, is unspecified. Owner: Warden (primary), State Consistency Theorist (co-owner for restore procedure).
- **GAP-17 (new)** — Ledger verification on very large chains. Full verification cost scales with chain length. On a multi-year, multi-million-entry Ledger, the 24h/10K-entry full verification may itself become an operational bottleneck. Sampled verification with probabilistic coverage guarantee may be required as a future optimization. Owner: State Consistency Theorist.
- **GAP-18 (new)** — Pre-receive Git hook integrity. The Tier 3 config modification path depends on a pre-receive Git hook that enforces bounds, signatures, and rationale for threshold updates. The spec does not define how the hook itself is integrity-protected against local tampering. Owner: Warden (primary).

**NEW TENSIONS SURFACED:**
- **T-BT** ("Bounded Tunability") — Recurring pattern now applied to both retention (Tier 1 bounds = no shortening path / Tier 3 extensions) and thresholds (Tier 1 bounds / Tier 3 values). Pattern is coherent within each gap but carries a latent tension: if an operator discovers that a Tier 1 bound was set too tightly at bootstrap, there is no recovery path within the current spec. A future spec decision may need to define a rare, high-ceremony "bound revision" path, distinct from the normal tuning path, for cases where the bound itself must change. Flagged but not resolved.
- **T-NOTIFY-LOSS** — GAP-28's single-attempt-no-retry decision creates a narrow operational window where an agent's in-flight work is wasted because a notification was lost and the agent continued until Gate rejection. This is intentional (prevents notification-delivery ambiguity) but creates a failure mode where long-running tool calls from an affected agent cannot be preemptively aborted. No resolution here; surfaced for awareness.

---

*End of Gap Session 11 Summary. Baseline for Session 12: v1.1 integrated spec + GS5–GS11 resolutions. New gaps (GAP-16, GAP-17, GAP-18) and tensions (T-BT, T-NOTIFY-LOSS) added to the backlog. Three spec-block forward pointers await Warden review in a future session (archival bundle format key lifecycle, threshold update ceremony hook integrity, bound revision path).*
