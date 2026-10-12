# Gap Session 7 — Summary

**Framework:** LLM as Database — Agent Harness Architecture
**Session type:** GS1 completion pass + amendment batch (A4–A9)
**Primary voices:** MEMIT Specialist, Orchestration Comparativist, Graph Data Architect
**Review voices:** Warden, State Consistency Theorist (amendment review only)
**Targets:** T13, GAP-27, GAP-20/INCON-3, amendment batch A4–A9
**Baseline:** v1.1 integrated spec as updated by GS1–GS5
**Status on exit:** Phase 2 exit blocker T13 cleared; GS1 gaps fully closed

---

## 1. T13 — Advisory Boundedness vs. Operational Flexibility

### 1.1 MEMIT Specialist — Compaction Fidelity Degradation Proxy

The core claim being formalized: each legacy patch introduces approximation
error at compaction time, because migration-manifest translation is not
semantics-preserving. Error accumulates non-linearly when multiple legacy
patches are batched into a single MEMIT edit — the parametric encoding
averages over approximated content.

**Principled proxy (compaction fidelity delta):**

```
Δfidelity ≈ r × h_avg × ε
```

Where:
- `r` = ratio of legacy patches to total active patches at compaction time
- `h_avg` = average version-hop distance of legacy patches to current version
  (multi-version-gap patches chain through intermediate manifest entries;
  each hop compounds error)
- `ε` = per-hop translation error coefficient (provisional, pending GAP-1
  empirical calibration; estimated 0.02–0.05 from the approximation
  characteristics of RENAME/BUCKET/COMPUTE transform types)

**Safe-upper-bound tiers (ratio-based, with absolute-count floors to handle
small-corpus edge cases):**

| Regime            | Ratio range    | Absolute floor | Meaning |
|-------------------|----------------|----------------|---------|
| Negligible        | `r < 0.05`     | < 10 patches   | Below measurement noise |
| Measurable        | `0.05 ≤ r < 0.15` | 10–25 patches | Tolerable; monitor |
| Meaningful        | `0.15 ≤ r < 0.30` | 25–75 patches | Approaches impairment |
| Severe            | `r ≥ 0.30`     | ≥ 75 patches   | Compaction fidelity not reliable |

**Rationale:** ratio-based because absolute counts scale with corpus size;
absolute-count floors protect small corpora where 2 legacy patches in a
10-patch corpus (r = 0.20) is not actually a concern.

### 1.2 Orchestration Comparativist — Override Window and `LEGACY_EXTENSION_GRANTED`

**Minimum override window:**

Between Tier 2 warning trigger and Tier 3 hard-block enforcement: **72 hours
wall-clock** (3 business days) minimum.

**Rationale:**
- Shorter than a typical sprint cycle (1–2 weeks) so in-flight work can
  react without being cut off mid-iteration.
- Longer than overnight so human operators have access during normal
  working hours regardless of timezone.
- Operator-override (via extension ceremony) remains available through
  and past this window.

**`LEGACY_EXTENSION_GRANTED` mechanism:**

This is a new ceremony type under the GS4 CeremonyToken model (D93), named
`LEGACY_EXTENSION`.

CeremonyToken payload fields:
- `agent_id` — scope of extension (per-agent, matching AG-1)
- `extension_window_seconds` — requested duration
- `current_legacy_count` — legacy patch count at time of request
- `previous_block_threshold` — value of M in effect at request time
- `reason` — free-text operator justification (mandatory, non-empty)

Signed by operator using CAK; verified by Gate against CAK registry.

**Gate checks (ordered; all must pass):**
1. CAK signature verifies against registered CAK (per D93, CAK registry lookup)
2. CeremonyToken not previously consumed (replay rejection per GS4)
3. `extension_window_seconds ≤ max_single_extension_duration`
   (provisional default: 30 days / 2,592,000s)
4. Count of prior `LEGACY_EXTENSION_GRANTED` entries for the same
   `agent_id` within rolling 90-day window ≤ `max_extensions_per_window`
   (provisional default: 1 — allowing one renewal, so 2 total in any
   90-day window)

**On acceptance:**
- `CEREMONY_ACCEPTED` Ledger entry (per GS4)
- `LEGACY_EXTENSION_GRANTED` Ledger entry (GOVERNANCE, sync)
- Gate's effective M threshold for this `agent_id` raised to
  `current_legacy_count + M_extension_headroom` (provisional: +10 patches)
  for duration of `extension_window_seconds`
- On expiration: Gate reinstates original M; any further legacy patches
  blocked again

**On rejection (signature invalid, replay, exceeded window):**
- `CEREMONY_SIGNATURE_INVALID` / `CEREMONY_REPLAY_REJECTED` per GS4
- No threshold change

**Cumulative limit:** After 2 extensions exhausted within the 90-day rolling
window, no further extension is possible. Migration (Pruning Agent semantic
GC or operator-initiated bulk re-issue at `current_larql_version`) is
required.

### 1.3 Three-Tier Advisory Model — Ratified (Spec Block 2c)

```
### larql Legacy Patch Advisory Model — Spec Block (ratified)

What it must do:
Bound the accumulation of LARQL_VERSION_LEGACY patches to preserve
compaction fidelity, while giving operator teams predictable override
capability to avoid mid-sprint hard-blocks.

Hard constraints:
- Tier 1 (per-patch advisory): emit LARQL_VERSION_LEGACY async Ledger
  entry on any legacy patch. Patch proceeds. Unchanged from v1.1 §10.2.
- Tier 2 (aggregate warning): trigger when
    r ≥ 0.10 OR absolute legacy count ≥ 25  (whichever occurs first)
  emit LARQL_VERSION_LEGACY_WARNING (SECURITY, sync). Patches still
  proceed. Starts 72-hour minimum countdown until Tier 3 may fire.
- Tier 3 (hard-block): trigger when
    r ≥ 0.25 OR absolute legacy count ≥ 75  (whichever occurs first)
  AND at least 72 hours have elapsed since Tier 2 was first triggered
  in the current episode. emit LARQL_VERSION_HARD_BLOCKED (SECURITY,
  sync). Gate refuses further legacy patch commits for this agent_id.
  Active legacy patches already committed remain compactable.
- Override path: LEGACY_EXTENSION ceremony (see 1.2). Single extension
  ≤ 30 days; maximum 2 extensions per rolling 90-day window.

Tradeoffs decided:
- Ratio-based thresholds with absolute floors — protects small corpora
  where raw ratio is misleading.
- 72-hour window chosen to fit between "overnight" and "sprint cycle" —
  predictable for operators without being permissive enough to allow
  unbounded drift.
- 2 extensions per 90-day window caps cumulative override at 60 days
  total, bounding the worst-case legacy accumulation horizon.
- "Whichever first" between ratio and absolute floor is the safer-bound
  choice (both-must-fire was rejected — allowed corpus-size gaming).

Open questions (deferred):
- Threshold M (r ≥ 0.25, count ≥ 75) remains PROVISIONAL pending GAP-1
  empirical calibration of ε (per-hop translation error coefficient).
- Whether per-version-gap weighting of r is needed (a v0.9 patch at
  distance 2 may contribute more error than a v1.0 patch at distance 1).
  Deferred to GAP-1.

Interface contract:
- Gate queries Ledger for count of LARQL_VERSION_LEGACY entries not
  yet compacted; computes r against active patch total at commit time.
- Gate consults Ledger for LEGACY_EXTENSION_GRANTED entries within
  active window before evaluating Tier 3 threshold.
- Ledger entry types emitted by Gate: LARQL_VERSION_LEGACY (async),
  LARQL_VERSION_LEGACY_WARNING (sync), LARQL_VERSION_HARD_BLOCKED
  (sync), LEGACY_EXTENSION_GRANTED (sync, governance).
```

---

## 2. GAP-27 — `SCOPE_UPDATED` Rate Limit

### 2.1 D89 Ratified

`scope_update_min_interval_seconds`:
- Tier 1 config field (§13.2, genesis-seal.json)
- Provisional default: **3,600 seconds** (1 hour)
- Scope: **per-`agent_id`** (AG-1 closed — confirmed in spec language)
- Rate limit check **precedes** signature verification
  - Cheap-first ordering: prevents signature-verification cost being
    weaponized as DoS amplifier
  - Attacker cannot force expensive crypto work simply by sending
    ceremony requests faster than the rate window
- Rejection produces `SCOPE_UPDATE_RATE_EXCEEDED` (SECURITY, sync)
- No registry state mutation on rejection beyond the error Ledger entry

### 2.2 Multi-Agent-ID Spray Attack — Residual Risk (Formal Documentation)

**Attack description:**
An adversary with control over multiple `agent_id`s initiates
`SCOPE_UPDATE` ceremonies across all of them in rapid succession. Each
individual `agent_id` stays within its per-agent rate limit, but the
aggregate creates Gate processing pressure and Ledger write volume
disproportionate to legitimate operator activity.

**Why per-agent rate limiting is accepted as sufficient:**

1. **Ceremonies require operator CAK signatures.** A single-agent-only
   attacker cannot forge ceremonies — ceremony authorization is rooted
   in CAK possession, not agent credential possession. Multi-agent
   spray requires multi-agent compromise *plus* CAK compromise.

2. **CAK compromise is a separately-addressed failure mode.** GS4's
   `CAK_COMPROMISE_DECLARED` pathway is the designated response. Rate
   limiting is not the right primitive to stop a compromised CAK —
   revocation is.

3. **Cross-agent rate limiting would cause head-of-line blocking.**
   Legitimate operator scenarios involve coordinated scope updates
   across agent cohorts (e.g., rolling out a new scope schema across
   a team of 12 agents). A global rate limit would deny legitimate
   parallel updates.

4. **Orchestrator-layer load limits are the correct abstraction for
   aggregate pressure.** Per-agent rate limiting protects per-agent
   fairness; aggregate throughput is an infrastructure concern
   outside the cryptographic authorization spec.

**Mitigation recommendation (advisory, not normative):**
Monitor aggregate `SCOPE_UPDATE` ceremony throughput at the
Orchestrator layer. Alert on anomalous rate spikes. See NEW-GAP-29.

### 2.3 Appendix C Entry

```
SCOPE_UPDATE_RATE_EXCEEDED (SECURITY, sync)
  Fields:
    agent_id: string
    attempted_at: timestamp
    next_eligible_at: timestamp
  Emitted when: SCOPE_UPDATE ceremony received within
    scope_update_min_interval_seconds of prior SCOPE_UPDATED for
    same agent_id. Check precedes signature verification.
```

---

## 3. GAP-20 + INCON-3 — Migration Manifest Format

### 3.1 OQ-GAP1-1 Resolved: Architect Agent Authorship

**Resolution: PERMITTED under standard token/gate model.**

Architect Agent MAY draft `larql_migration_manifest` entry content.
Agent authorship does not alter the trust boundary because manifest
authority derives exclusively from the `MANIFEST_RATIFICATION`
ceremony (CAK-signed, human-authorized) — not from authorship.

**Workflow:**
1. Architect Agent drafts proposed manifest entry (standard agent
   invocation; token-scoped, gate-bounded)
2. Draft enters review queue (may be paired with Validator Agent
   cross-check as a pre-ratification step — non-normative)
3. Operator reviews content
4. Operator executes dry-run (see 3.2; mandatory)
5. Operator initiates `MANIFEST_RATIFICATION` ceremony, signing
   CeremonyToken with CAK; payload includes `manifest_hash` and
   `dry_run_artifact_hash`
6. `CEREMONY_ACCEPTED` written
7. Manifest commit gate verifies (see 3.3); on pass, manifest entry
   persisted to Tier 1 config

**Constraint:** Agent-drafted manifest entries are structurally valid
*proposals only*. They have no authority until the ceremony completes.
No agent credential, no scope token, and no Gate-side permission
structure grants manifest-write authority.

### 3.2 OQ-GAP1-2 Resolved: Dry-Run Mandatory

**Resolution: YES, dry-run is mandatory before `MANIFEST_RATIFICATION`.**

**Rationale:** A faulty migration manifest corrupts compaction for the
entire legacy patch backlog. Blast radius is every patch the manifest
will ever translate. Pre-ratification validation is the only
before-the-fact check; there is no cheap rollback for a corrupted
compaction.

**Dry-run protocol:**
1. Operator initiates dry-run via Orchestrator against a proposed
   manifest entry (or manifest bundle).
2. Compaction simulation applies manifest translation rules to a
   snapshot of all currently-held legacy patches that would be in
   scope for the manifest's `source_version`.
3. Simulation does NOT write to .vindex; output is a report only.
4. Dry-run report contents:
   - Translation success count
   - Translation failure count (any failure is a hard rejection)
   - Per-patch fidelity delta (estimated `Δfidelity` contribution)
   - Any `VERSION_REJECTED` cases encountered
   - Flagged semantic anomalies (e.g., BUCKET transform where source
     distribution falls entirely in one bucket — suggests miscalibration)
5. Report is content-addressed: `dry_run_artifact_hash` computed
   over canonical serialization.
6. Artifact persisted to dry-run store (see NEW-GAP-28).

**Acceptance criteria (enforced at ratification time):**
- Zero translation failures. Any non-zero count blocks ratification.
- Zero unexpected `VERSION_REJECTED` cases — every patch in scope
  must translate. Discovery of un-translatable patches means the
  manifest is incomplete.
- Fidelity delta report must be explicitly acknowledged by operator
  (part of the ratification UX; no hard ceiling, but acknowledgment
  is mandatory).

**Freshness window:** `dry_run_artifact_hash` must correspond to a
dry-run report produced within the last **7 days** (provisional) prior
to ratification ceremony. Stale dry-runs (patch corpus may have
drifted) require re-run.

### 3.3 IC-MANIFEST-1 Ratified (with A9 Amendment Applied)

```
### Interface Contract — larql_migration_manifest Entry (IC-MANIFEST-1)

Each manifest entry is a translation rule from a specific source
larql_syntax_version to the current target version.

Fields:
  source_version: string
    The larql_syntax_version carried by patches this rule applies to.

  target_version: string
    The version patches will be translated INTO. Equal to the
    current_larql_version at ratification time.

  field_mappings: ordered list of translation rules
    Each rule:
      source_field_path: string (JSONPath-style selector)
      target_field_path: string (JSONPath-style selector)
      transform_type: enum {RENAME, BUCKET, COMPUTE, DROP, DEFAULT_INSERT}
      transform_params: object (shape depends on transform_type)
    Ordering matters — rules apply sequentially.

  bucket_map: object (required when any transform_type = BUCKET)
    Defines float → enum boundary thresholds for bucketing transforms.
    Example:
      "attention_weight_to_declared_importance": {
        "LOW": [0.0, 0.33],
        "MEDIUM": [0.33, 0.66],
        "HIGH": [0.66, 1.0]
      }
    Boundary thresholds are PROVISIONAL pending GAP-1.

  ceremony_token_id: string                          [A9 — replaces
    ID of CEREMONY_ACCEPTED Ledger entry for the       ratification_
    MANIFEST_RATIFICATION ceremony authorizing        signature]
    this manifest entry. (Per GS4 D93, INCON-3.)

  dry_run_artifact_hash: string
    Content hash of the dry-run report produced prior to ratification.

Manifest commit gate verification (ALL must pass; any fail =
MANIFEST_COMMIT_REJECTED):
  1. Ledger entry with id = ceremony_token_id exists.
  2. That entry has entry_type = CEREMONY_ACCEPTED.
  3. entry.payload.ceremony_type = MANIFEST_RATIFICATION.
  4. entry.payload.manifest_hash = hash of manifest entry being
     committed (canonical serialization).
  5. dry_run_artifact_hash present in manifest entry exists in
     dry-run store.
  6. Dry-run report at that hash shows zero translation failures,
     zero unexpected VERSION_REJECTED.
  7. Ceremony entry timestamp is within 7 days of commit attempt
     (provisional freshness).
```

---

## 4. Amendment Batch — Applied

| ID | Target | Status |
|----|--------|--------|
| A4 | §14.3 — SCOPE_HASH_MISMATCH threshold 3 → 2; add SCOPE_MISMATCH_ESCALATED | ✓ Applied |
| A5 | §10.9 — Ceremony authorization verification against CAK before SCOPE_UPDATED | ✓ Applied |
| A6 | §10.9 — Rate limit check precedes signature verification | ✓ Applied |
| A7 | Appendix C — GS3-derived entries | ✓ Applied (`DEPENDENCY_HOLD_RELEASED_SIGNED` confirmed from GS5, not re-added) |
| A7b | Appendix C — GS4 CeremonyToken-model entries | ✓ Applied; deprecation marks on `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` |
| A9 | IC-MANIFEST-1 — `ratification_signature` → `ceremony_token_id` + commit gate verification | ✓ Applied |

**Additional Appendix C entries emitted by this session's spec work
(not pre-listed in amendment batch but implied by T13 and GAP-20
resolutions):**

```
LEGACY_EXTENSION_GRANTED (GOVERNANCE, sync)
  Fields: agent_id, granted_by_cak_fingerprint,
    extension_window_seconds, previous_block_threshold

LARQL_VERSION_LEGACY_WARNING (SECURITY, sync)
  Fields: agent_id, legacy_count, total_patches, ratio,
    tier_2_trigger_timestamp

LARQL_VERSION_HARD_BLOCKED (SECURITY, sync)
  Fields: agent_id, legacy_count, total_patches, ratio,
    tier_3_trigger_timestamp, tier_2_elapsed_seconds

MANIFEST_COMMIT_REJECTED (SECURITY, sync)
  Fields: manifest_hash, ceremony_token_id_ref,
    verification_check_failed (enum: CEREMONY_NOT_FOUND |
    WRONG_CEREMONY_TYPE | MANIFEST_HASH_MISMATCH |
    DRY_RUN_ARTIFACT_MISSING | DRY_RUN_HAS_FAILURES |
    DRY_RUN_STALE)
```

---

## Session Summary Block

**GAPS RESOLVED:**
- **T13 — Advisory Boundedness vs. Operational Flexibility:**
  Three-tier advisory model ratified. MEMIT provided the compaction
  fidelity degradation proxy (`Δfidelity ≈ r × h_avg × ε`) with
  ratio-based thresholds backed by absolute-count floors. Orchestration
  specified 72-hour minimum override window and the `LEGACY_EXTENSION`
  ceremony mechanism (CAK-signed, max 30-day single extension, 2
  extensions per 90-day rolling window). Spec block 2c upgraded from
  outline to ratified; threshold M remains provisional pending GAP-1
  empirical calibration of ε.
- **GAP-27 — `SCOPE_UPDATED` rate limit:** D89 ratified.
  `scope_update_min_interval_seconds` (Tier 1, provisional default 3,600s),
  per-`agent_id` scope confirmed (AG-1 closed). Rate limit check precedes
  signature verification. Multi-agent-ID spray attack residual formally
  documented with four-point rationale. `SCOPE_UPDATE_RATE_EXCEEDED`
  added to Appendix C.
- **GAP-20 + INCON-3 — Migration manifest format:** IC-MANIFEST-1
  ratified with A9 amendment applied (`ceremony_token_id` replaces
  `ratification_signature`). Dry-run made mandatory with explicit
  protocol, acceptance criteria, and 7-day freshness window. Architect
  Agent authorship permitted under standard token/gate model. Manifest
  commit gate verification specified in seven ordered checks.

**GAPS PARTIALLY RESOLVED:**
- None — all three targeted gaps fully closed.

**GAPS DEFERRED:**
- Threshold M (hard-block trigger: `r ≥ 0.25` or count ≥ 75) remains
  **PROVISIONAL** pending GAP-1 empirical calibration of the per-hop
  translation error coefficient ε.
- `bucket_map` boundary thresholds in IC-MANIFEST-1 (e.g., 0.33 / 0.66
  breakpoints for attention_weight → declared_importance) remain
  **PROVISIONAL** pending GAP-1.
- Per-version-gap weighting of the ratio `r` (whether multi-hop patches
  should count more heavily than single-hop patches) deferred to GAP-1.

**NEW GAPS SURFACED:**
- **NEW-GAP-28 (Medium priority, owner: Warden + Graph Data Architect):**
  Dry-run artifact storage. Where dry-run reports are persisted,
  retention policy, tamper-evidence of the artifact hash chain, and
  operator-side verification UX. Referenced by IC-MANIFEST-1 but
  unspecified.
- **NEW-GAP-29 (Low priority, owner: Orchestration Comparativist):**
  Cross-agent aggregate `SCOPE_UPDATE` ceremony throughput monitoring.
  Advisory-tier mechanism at the Orchestrator layer to complement
  per-agent rate limiting. Explicitly called out in GAP-27 residual
  risk documentation as the correct abstraction for aggregate
  pressure, but not yet specified.

**NEW TENSIONS SURFACED:**
- **T14 candidate — Dry-run freshness vs. manifest authorship lifecycle:**
  The 7-day freshness window on `dry_run_artifact_hash` can conflict
  with longer manifest authorship cycles (e.g., when Architect Agent
  drafting + human review extends beyond a week). Forces dry-run re-run
  before ratification. May be acceptable operational cost or may need
  tuning; flag for future review.

**INTERFACE CONTRACTS FINALIZED THIS SESSION:**
- IC-MANIFEST-1 (ratified, A9 applied)

**AMENDMENTS APPLIED THIS SESSION:**
- A4, A5, A6, A7, A7b, A9
- Implicit additions: `LEGACY_EXTENSION_GRANTED`,
  `LARQL_VERSION_LEGACY_WARNING`, `LARQL_VERSION_HARD_BLOCKED`,
  `MANIFEST_COMMIT_REJECTED` (all SECURITY/GOVERNANCE, sync)

**PHASE 2 EXIT STATUS:**
- T13 (Phase 2 exit blocker) — **cleared** (spec block 2c ratified;
  M provisional pending GAP-1 is an expected deferral, not a blocker).

**NEXT SESSION (GS8):** Input to GS8 is the set of GAPS DEFERRED and
NEW GAPS SURFACED above, plus the v1.1 spec with GS1–GS7 amendments
consolidated. T14 candidate should be triaged into the tension map
before GS8 begins.
