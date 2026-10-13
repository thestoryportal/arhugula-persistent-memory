═══════════════════════════════════════════════════════════════
Gap Session 6 — Summary Block
Session scope: GAP-22, GAP-23 (State Consistency Theorist)
Baseline: v1.1 integrated spec; GS5 amendments applied.
═══════════════════════════════════════════════════════════════

## GAPS RESOLVED

**GAP-22** — Resolution path **(b)** adopted. `TIMED_OUT` retains its existing
shape (with `compensation_direction` as a required, non-nullable field) and is
now explicitly scoped to **incremental** PREPARED timeouts only. A new
`GENESIS_TIMEOUT` entry type (CONSISTENCY, sync) is introduced for the Genesis
case, with no `compensation_direction` field. Naming aligned with the existing
IC-TC-GENESIS contract (`GENESIS_TIMEOUT`, not `GENESIS_TIMED_OUT` as proposed
in the gap prompt) — rationale: IC-TC-GENESIS already references this exact
Ledger type in its step-1 write, and diverging the Appendix C name would
introduce a cross-reference mismatch. Resolution captured as D104 + D105 + D106.
Audit-tool correctness restored: Genesis timeouts are filterable by entry type;
no sentinel convention required; no nullable field for parsers to handle.

**GAP-23(a)** — **YES.** `DEPENDENCY_HOLD_RELEASED_SIGNED` with `release_reason:
GENESIS_RESET_PREPARATION` is a hard precondition for `CIRCUIT_RESET` when the
trip was a `DIVERGED_STATE` originating from a `GENESIS_TIMEOUT` entry. TC
verifies: (i) the signed release entry exists, (ii) its `transaction_id` matches
the `transaction_id` on the triggering `GENESIS_TIMEOUT`, (iii) its timestamp is
after `RECONCILIATION_COMPLETE(result: CONSISTENT)` and before the
`CIRCUIT_RESET` attempt. IC-TC-RESET amended accordingly (A11). D107.

**GAP-23(b)** — **Explicit signed release MUST precede `CIRCUIT_RESET`.**
`CIRCUIT_RESET` does not implicitly release any Dependency Hold. Rationale:
(i) each governance ceremony should consume its own CeremonyToken and produce
its own independently-verifiable audit artifact; (ii) implicit release would
couple two distinct authority grants (Hold release + circuit reset) into a
single signature, weakening forensic attribution; (iii) only a subset of
`DIVERGED_STATE` trips involve Genesis Holds — an implicit-release rule would
have to branch on trip origin and would be error-prone. Required Ledger
ordering enshrined as C-GEN-HOLD-2 (below). D108.

**GAP-23(c)** — **NO.** A new Genesis MAY NOT initiate while any prior Genesis
Dependency Hold remains active. Enforcement is **pre-flight** at the
Orchestrator (Genesis initiation refused; no Phase-1 PREPARED entry written),
not post-hoc at the TC. Operator resolution path is the playbook below:
the failed-Genesis Hold must be released via signed ceremony, the reset
ceremony must complete, and only then may a fresh Genesis be initiated.
Rule ratified as C-GEN-HOLD-3. D109.

**GAP-23 deadlock** — Latent deadlock resolved by the combination of C-GEN-HOLD-1
through C-GEN-HOLD-3 plus the operator playbook (A16). System cannot reach the
described state of "WRITE_ENABLED but blocked by orphaned Hold" because reset
cannot complete without prior signed Hold release.

## DECISIONS RATIFIED (continuing from D103)

- **D104** — GAP-22 resolved via path (b): separate `GENESIS_TIMEOUT` entry type.
- **D105** — Entry named `GENESIS_TIMEOUT` (aligns with IC-TC-GENESIS); the
  prompt's proposed `GENESIS_TIMED_OUT` name is NOT adopted.
- **D106** — `TIMED_OUT` entry scope narrowed to incremental PREPARED timeouts;
  `compensation_direction` remains required and non-nullable for this type.
- **D107** — Signed Hold release is a hard precondition for Genesis-originated
  `CIRCUIT_RESET` (GAP-23a).
- **D108** — `CIRCUIT_RESET` does not implicitly release Holds; explicit
  signed release must precede reset in Ledger order (GAP-23b).
- **D109** — Orchestrator pre-flight blocks new Genesis initiation while any
  prior Genesis Hold is unreleased (GAP-23c).
- **D110** — Operator playbook for Genesis-timeout deadlock recovery ratified
  as the canonical recovery path (A16 below).

## CONSTRAINTS RATIFIED

- **C-GEN-HOLD-1** — A Dependency Hold held by a Genesis transaction that
  experienced `GENESIS_TIMEOUT` MUST be released via a signed
  `DEPENDENCY_HOLD_RELEASED_SIGNED` entry (release_reason:
  `GENESIS_RESET_PREPARATION`) before the `CIRCUIT_RESET` of its originating
  `DIVERGED_STATE` trip is permitted. TC refusal of reset without this
  precondition produces `CIRCUIT_RESET_REJECTED` per A2-GS2 semantics.

- **C-GEN-HOLD-2** — `CIRCUIT_RESET` does not implicitly release any
  Dependency Hold. The canonical Ledger ordering for Genesis-timeout recovery
  is:
  `GENESIS_TIMEOUT` → `CIRCUIT_TRIPPED(DIVERGED_STATE)` →
  `RECONCILIATION_COMPLETE(result: CONSISTENT)` →
  `DEPENDENCY_HOLD_RELEASED_SIGNED(release_reason: GENESIS_RESET_PREPARATION)` →
  `CIRCUIT_RESET`.
  Reorderings are reset-precondition failures.

- **C-GEN-HOLD-3** — The Orchestrator MUST refuse to admit a new Genesis
  initiation while any prior Genesis Dependency Hold remains active, regardless
  of circuit state. Enforcement is pre-flight (prior to Phase-1 PREPARED
  write). Attempted initiation under an active Genesis Hold produces
  `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` (INTEGRITY, sync) — see NEW LEDGER
  ENTRY TYPES below.

## AMENDMENTS APPLIED

- **A11-IC-TC-RESET** (amendment) — Precondition list extended for
  `DIVERGED_STATE` trips whose originating Ledger entry is `GENESIS_TIMEOUT`:
  require `DEPENDENCY_HOLD_RELEASED_SIGNED` with matching `transaction_id` and
  `release_reason: GENESIS_RESET_PREPARATION`, timestamped after the matching
  `RECONCILIATION_COMPLETE(CONSISTENT)` and before the reset attempt. All
  other `DIVERGED_STATE` trip-origin preconditions (per v1.1 §11.8.1) remain
  in force unchanged.

- **A12-Appendix-C** (addition) — New entry type:
  ```
  GENESIS_TIMEOUT (CONSISTENCY, sync)
    Fields: {
      transaction_id,
      prepared_since,
      timeout_value,
      current_overlay_hash,
      pre_genesis_anchor_hash,
      partial_compile_preserved: true,
      trigger
    }
    Semantics: Emitted by TC genesis timeout monitor BEFORE circuit breaker
    trip (per IC-TC-GENESIS step sequencing). No compensation_direction field
    — Genesis timeouts prohibit auto-compensation (§11.5.1, C-GEN1).
    v1.1-amended (GS6).
  ```

- **A13-Appendix-C** (clarification) — `TIMED_OUT` entry scope is hereby
  restricted to incremental PREPARED timeouts (i.e. non-Genesis transactions).
  `compensation_direction` remains required for this entry type. Annotation
  added: *"For Genesis PREPARED timeouts, see `GENESIS_TIMEOUT` (this
  appendix)."*

- **A14-§11.5.1** — PREPARED-State Timeout Behavior text updated: Genesis
  timeout emits `GENESIS_TIMEOUT` (per IC-TC-GENESIS), then circuit breaker
  trips with `DIVERGED_STATE`. Prior implicit reference to `TIMED_OUT` for
  the Genesis case is removed.

- **A15-§17.3** (Dependency Hold) — Clarification added: Hold survives
  `GENESIS_TIMEOUT` and the subsequent `CIRCUIT_TRIPPED`. Hold release requires
  a signed ceremony with `release_reason: GENESIS_RESET_PREPARATION`.
  `CIRCUIT_RESET` alone does NOT release the Hold (C-GEN-HOLD-2). Pruning
  pre-check (§17.6, IC-PA7) continues to exclude edges under the active Hold
  throughout this period.

- **A16-new §11.8.2** (Operator Playbook — Genesis Timeout Deadlock Recovery):

  1. TC genesis timeout monitor fires; writes `GENESIS_TIMEOUT` to Ledger
     (IC-TC-GENESIS step 1).
  2. TC trips circuit breaker: writes `CIRCUIT_TRIPPED(DIVERGED_STATE,
     triggering_transaction_id = <failed Genesis tx>)`.
  3. TC emits `GENESIS_RECOVERY_REQUIRED` to Human Review Queue
     (IC-TC-GENESIS step 3).
  4. Operator performs full model integrity check against the pre-Genesis
     `IMMUTABLE_ANCHOR` baseline (per IC-TC-TIMEOUT).
  5. Operator writes `RECONCILIATION_STARTED` (GS5), then
     `RECONCILIATION_COMPLETE` with `result: CONSISTENT`. If `result:
     DIVERGED`, recovery exits this playbook and enters the reconciliation
     recovery path (release_reason `RECONCILIATION_RESUME`, per GS5).
  6. Operator signs and submits `DEPENDENCY_HOLD_RELEASED_SIGNED` ceremony
     with `release_reason: GENESIS_RESET_PREPARATION`, referencing the failed
     Genesis `transaction_id`. Orchestrator releases the Hold; Ledger entry
     written (GOVERNANCE, sync, per GAP-21).
  7. Operator signs and submits `CIRCUIT_RESET` ceremony. TC verifies all
     IC-TC-RESET preconditions (including the new Genesis-branch precondition
     from A11). On success, TC writes `CIRCUIT_RESET` and transitions system
     to `WRITE_ENABLED`.
  8. Pruning Agent's `held_not_prunable` count on the formerly-held edges is
     cleared; `stale_urgent` counters re-evaluated on next Pruning cadence
     (§17.6, unchanged).
  9. Operator (or automated workflow) may now initiate a new Genesis.
     Orchestrator pre-flight check (C-GEN-HOLD-3) passes: no active Genesis
     Hold remains.
  10. New Genesis proceeds through normal Phase-1/Phase-2 2PC (§11.5, §11.6).
  11. On successful commit, `COMMITTED` entry closes the recovery cycle.

  Failure branches:
  - Step 5 yields `RECONCILIATION_COMPLETE(DIVERGED)` → exit to reconciliation
    recovery; this playbook does not apply.
  - Step 6 rejected → `HOLD_RELEASE_REJECTED` (SECURITY, sync, per GAP-21);
    operator must remediate and retry.
  - Step 7 rejected → `CIRCUIT_RESET_REJECTED` (per A2-GS2); operator must
    remediate (most common cause: Hold release signature missing or
    out-of-order per C-GEN-HOLD-2).
  - Step 9 rejected with `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` → indicates
    C-GEN-HOLD-3 violation; operator must return to step 6 for the
    unreleased Hold.

## GAPS PARTIALLY RESOLVED

None. Both session-scoped gaps fully resolved.

## GAPS DEFERRED

None new.

## NEW LEDGER ENTRY TYPES INTRODUCED (require Appendix C batch — extend A7b)

- `GENESIS_TIMEOUT` (CONSISTENCY, sync) — see A12.
- `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` (INTEGRITY, sync) — emitted by
  Orchestrator pre-flight when C-GEN-HOLD-3 blocks a new Genesis attempt.
  Fields: `{ attempted_genesis_op_id, blocking_hold_transaction_id,
  blocking_genesis_op_id, pre_flight_timestamp }`.

→ **Action item for GS7 A7b batch:** extend to cover these 2 new types in
addition to the prior GS4 (6+2) and GS5 (14) entries.

## NEW GAPS SURFACED

- **GAP-30 (provisional)** — Cross-reference audit: IC-TC-GENESIS in the
  State Consistency Theorist skill header references `GENESIS_TIMEOUT` as if
  canonical, but this was only formally ratified into Appendix C in this
  session (GS6 / A12). The v1.1 integrated spec document must be scanned for
  any stale references to `TIMED_OUT` in Genesis-case contexts that need to
  be updated to `GENESIS_TIMEOUT` per A14. Suggested home: GS7 consolidation
  pass concurrent with the A7b Appendix C batch.

- **GAP-31 (provisional)** — The `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE`
  entry is classified INTEGRITY (operational failure) rather than SECURITY,
  on the basis that the Orchestrator pre-flight is doing its job correctly
  and no integrity violation has occurred. However, if the blocking attempt
  comes from a non-authorized source or exhibits a repeat pattern (e.g., a
  suspected compromised agent repeatedly attempting Genesis), this may
  warrant W3 eligibility or a separate SECURITY-category escalation entry.
  Suggested home: GS7 (alongside GAP-29 W3 scope consolidation — the two
  are thematically related) or a Warden-led mini-session. Flagged ⚑ WARDEN
  CO-REVIEW per skill checklist.

## NEW TENSIONS SURFACED

- **T13 (provisional)** — *Ceremony atomicity vs. ceremony decomposition.*
  GAP-23(b) resolves in favor of decomposed ceremonies (Hold release is
  separate from circuit reset) for forensic-clarity reasons. A later
  refactor aimed at reducing operator burden (fewer ceremonies) could
  reintroduce the pressure to make `CIRCUIT_RESET` implicitly release
  Holds. The tension between **auditability (many narrow ceremonies)** and
  **operator ergonomics (fewer consolidated ceremonies)** is now a
  framework-level axis that will recur in any future multi-ceremony
  recovery design. Owners: State Consistency Theorist (primary) + Warden
  (co-review). Relates to but is distinct from T8 (Audit Throughput) and
  T11 (Ceremony Governance).

## INCONSISTENCIES CLOSED

None new. GS6 does not touch prior INCON-N tracked items.

## INTERFACE CONTRACTS DEFINED / AMENDED

- **IC-TC-RESET** — amended via A11 (Genesis-branch precondition added).
- **IC-TC-GENESIS** — existing in skill header; now fully ratified into spec
  via GAP-22 path (b) resolution. No contract text change; Ledger type it
  references is now Appendix-C canonical.
- **IC-PA7** (Pruning pre-check Hold query) — unchanged in contract; behavior
  during Genesis recovery clarified in A15.
- **Hold release interface** (per GAP-21 GS5) — unchanged; the
  `GENESIS_RESET_PREPARATION` release_reason value is now exercised by the
  playbook (A16 step 6).

⚑ **WARDEN CO-REVIEW flag:** A11 amends precondition logic on a governance
ceremony (circuit reset), and C-GEN-HOLD-3 defines an Orchestrator pre-flight
refusal rule. Before IC-TC-RESET amendment is closed, the Warden must confirm:
(i) the Genesis-branch precondition does not create a bypass route around
existing CeremonyToken consumption semantics (A2-GS2); (ii) the pre-flight
refusal at the Orchestrator does not shift any authority that should remain
with TC; (iii) `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` classification
(INTEGRITY vs. SECURITY) is correct given threat-model considerations (see
GAP-31).

## CARRY-FORWARD ITEMS FOR SUBSEQUENT SESSIONS

- **GS7 (Appendix C batch A7 + A7b + GS5 + GS6 additions)** — Must merge
  2 new GS6 entry types (`GENESIS_TIMEOUT`,
  `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE`) with the already-pending GS3,
  GS4 (8), and GS5 (14). Running total: 24+ new Appendix C entries pending
  consolidation. GS7 should also address:
  - GAP-29 (W3 scope consolidation — carried from GS5).
  - GAP-30 (§ reference scan for stale `TIMED_OUT`/Genesis mentions).
  - GAP-31 (classification review for `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE`).
- **T13 logged** to tension map; no session-scoped resolution required.
- **Warden co-review** of IC-TC-RESET amendment (A11) and C-GEN-HOLD-3
  required before v1.2 cut. Small scope — suitable for async review or a
  brief mini-session.

═══════════════════════════════════════════════════════════════
End of Gap Session 6 Summary
═══════════════════════════════════════════════════════════════
