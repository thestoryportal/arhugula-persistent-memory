# Gap Session 11 Summary — SCT Lifecycle & Schema

**Session:** GS11 of 13
**Primary skill:** state-consistency-theorist
**Co-owner:** aisecops-specialist (Warden) — GAP-31, GAP-34, GAP-46, GAP-52, GAP-54, T-PM-vs-PA
**Baseline:** v1.1 integrated spec + GS1–GS10
**Gaps addressed (10):** GAP-30, GAP-31, GAP-34, GAP-35, GAP-43, GAP-46, GAP-52, GAP-53, GAP-54, T-PM-vs-PA
**Sequencing note:** GAP-34 (governing_scope_hash schema) is resolved first because several downstream resolutions (GAP-30 precursor queries, GAP-31 audit-window queries) assume the field is present on commit-path entries. GAP-46 is resolved before GAP-31's W-tier determination because operator_id stability informs attribution semantics for the rejection entry.

---

## Resolutions

### GAP-34 — `governing_scope_hash` on Commit Entries — Spec Block

**What it must do / represent / enforce / guarantee:**
Bind every PREPARED → COMMITTED transaction to the scope registry state that governed it at PREPARE time, so post-SCOPE_UPDATED forensic queries can deterministically attribute a commit to the scope under which it was authorized.

**Hard constraints:**
- **C-GSH-1 (Capture Point):** `governing_scope_hash` is set on the PREPARED Ledger entry at the moment PREPARE is written. Value = SHA-256 of the canonical serialization of the Orchestrator's active scope registry at that instant.
- **C-GSH-2 (Preservation):** The COMMITTED entry for the same transaction MUST carry the identical `governing_scope_hash` value from its PREPARED predecessor. Mismatch is a diverged-state condition and trips the circuit breaker.
- **C-GSH-3 (Immutability Across SCOPE_UPDATED):** An intervening SCOPE_UPDATED between PREPARED and COMMITTED does not mutate the field. The commit remains attributable to its pre-update scope.
- **C-GSH-4 (Forward-Only):** Field is additive; entries written before this amendment carry `governing_scope_hash: null` and are queryable with an explicit "pre-amendment" flag — they are not retroactively filled.

**Tradeoffs decided:**
- Hash (not scope version number) — version numbers risk collision across reset ceremonies; a content-addressed hash is unambiguous.
- Capture at PREPARE, not at token consume — the authoritative governing scope is what was in force when the transaction reached the durable pre-commit state. Token consume is too early; scope could legitimately update before PREPARE without invalidating the transaction.
- Null on pre-amendment entries (not backfilled) — backfilling would require rewriting historical entries, violating Ledger append-only semantics.

**Open questions (deferred):** None. R-S3-3 is now confirmed applied.

**Interface contract:**
- IC-PREPARE-SCOPE (new): Orchestrator publishes active scope registry hash to TC at PREPARE time; TC stamps it onto the PREPARED entry before signing. No additional barrier — Orchestrator scope registry is already held under the SCOPE_UPDATED sequencing invariant (§10.9).
- Appendix C entries PREPARED and COMMITTED gain `governing_scope_hash` (32-byte hex, nullable for pre-amendment entries).

---

### GAP-30 — GENESIS_TIMED_OUT → CIRCUIT_TRIPPED Ordering Monitor — Spec Block

**What it must do / represent / enforce / guarantee:**
Guarantee that a GENESIS_TIMED_OUT entry is always followed by a matching CIRCUIT_TRIPPED entry as the immediate next Ledger position authored by the TC, and detect any deviation as a forensic finding.

**Hard constraints:**
- **C-GTO-1 (Paired Sync-Write):** TC writes GENESIS_TIMED_OUT and CIRCUIT_TRIPPED (`trip_type: DIVERGED_STATE`, with reference to `genesis_op_id`) in the same sync-write window, as the two immediately consecutive TC-authored entries. No other TC-authored entry may fall between them. (Non-TC entries from other authorized writers at adjacent positions do not violate the invariant — the constraint is on TC's own authoring sequence.)
- **C-GTO-2 (Monitor Detection):** The Ledger integrity monitor, on every full verification pass (§16.4), performs a pairing check: for every GENESIS_TIMED_OUT entry, the next TC-authored entry MUST be a CIRCUIT_TRIPPED with matching `genesis_op_id` field. A missing, non-matching, or out-of-sequence successor emits a `GENESIS_TIMEOUT_TRIP_MISSING` advisory.
- **C-GTO-3 (Advisory Semantics):** `GENESIS_TIMEOUT_TRIP_MISSING` is a forensic advisory, not a state-mutating action. It does not itself trip the circuit breaker (the monitor already operates in a post-hoc verification context where the breaker's state is whatever it actually is); it flags the Ledger for human review.

**Ratification — `GENESIS_TIMEOUT_TRIP_MISSING` entry type:**
- Category: **CONSISTENCY**
- Mode: **async** (authored by monitor during verification pass, not in the hot write path)
- W-tier: **W1** (monitor is an Orchestrator-mediated component; no W3 carve-out required — the finding is advisory, not an emergency state-preservation action)
- Fields: `detected_at`, `offending_genesis_op_id`, `orphan_timeout_entry_position`, `observed_successor_entry_position`, `observed_successor_entry_type`, `verification_pass_id`

**Tradeoffs decided:**
- Rejected (a) "atomic paired write" — Ledger entries are append-only signed records, not a transactional pair; "atomicity" would require a new primitive. Sequential constraint with post-hoc monitor detection is the simpler, existing-pattern solution.
- Chose monitor on full-verification pass, not continuous stream monitor — continuous monitor introduces hot-path coupling; the window between actual trip and next verification pass is bounded by D108 thresholds (24h or 10K entries), which is acceptable for a forensic finding.
- W1 over W3 — the advisory records an ordering anomaly; it does not itself preserve evidence that would otherwise be lost (the GENESIS_TIMED_OUT entry is already durable). W3 is reserved for entries that would not otherwise reach the Ledger.

**Open questions (deferred):** None.

**Interface contract:**
- IC-MON-GTOTM (new): Ledger integrity monitor exposes a `pairing_check` sub-routine invoked during full verification. On failure, emits `GENESIS_TIMEOUT_TRIP_MISSING` via W1 and attaches the anomaly to the verification-pass report.
- Appendix C: new advisory entry type registered.

---

### GAP-31 — Precursor Validation for GENESIS_RESET_PREPARATION — Spec Block

**What it must do / represent / enforce / guarantee:**
Before accepting a `DEPENDENCY_HOLD_RELEASED_SIGNED` with `release_reason: GENESIS_RESET_PREPARATION`, the TC MUST verify a matching `GENESIS_TIMED_OUT` precursor exists in the Ledger and covers the affected Holds. This closes the C-GEN-REC-3 (GS6 v3) enforcement gap.

**Hard constraints:**
- **C-GEN-REC-3-ENF-1 (Cited Precursor):** The operator-signed release payload MUST cite a `precursor_genesis_op_id`. A release without this field is rejected at signature-envelope validation (pre-TC).
- **C-GEN-REC-3-ENF-2 (Precursor Presence):** TC queries the Ledger for a `GENESIS_TIMED_OUT` entry with matching `genesis_op_id`. Missing entry → reject.
- **C-GEN-REC-3-ENF-3 (Hold Coverage):** The cited GENESIS_TIMED_OUT's `affected_hold_ids` MUST be a superset of the `hold_ids` named in the release. Partial coverage → reject.
- **C-GEN-REC-3-ENF-4 (Audit Window):** The precursor GENESIS_TIMED_OUT MUST postdate the placement timestamp of every Hold in `hold_ids` and predate the signed release request timestamp. No fixed time bound — the window is anchored to Hold lifetime. Holds are long-lived by design; introducing a fixed decay adds failure modes without adding safety.
- **C-GEN-REC-3-ENF-5 (Rejection Emission):** On any of C-GEN-REC-3-ENF-1..4 failing, TC writes `HOLD_RELEASE_REASON_UNWARRANTED` (SECURITY, sync) carrying: `rejected_release_signature`, `operator_id`, `cited_precursor_genesis_op_id` (if present), `failure_reason` ∈ {MISSING_CITATION, PRECURSOR_NOT_FOUND, HOLD_COVERAGE_INCOMPLETE, WINDOW_VIOLATION_HOLD_PREDATES, WINDOW_VIOLATION_RELEASE_PREDATES}. The signed release is NOT written to the Ledger.

**Ratification — `HOLD_RELEASE_REASON_UNWARRANTED` entry type:**
- Category: **SECURITY**
- Mode: **sync**
- W-tier: **W1** (written through normal Orchestrator-mediated path; TC is the rejecting authority and is itself Orchestrator-mediated). The rejection is recorded before any state change — no forensic-preservation emergency exists. W3 carve-out is not warranted under the GS10 C-W3-1 admission criteria (the W1 path is available and not compromised at the moment of rejection).
- Fields as enumerated in C-GEN-REC-3-ENF-5.

**Tradeoffs decided:**
- Operator-cited precursor (vs. TC auto-discovers latest matching GENESIS_TIMED_OUT) — citation makes operator attestation explicit and auditable, and eliminates ambiguity when multiple Genesis timeouts have occurred.
- Hold-anchored window (vs. fixed e.g. 30-day bound) — Holds are already the authoritative scoping mechanism for Genesis state; bounding the window to Hold lifetime preserves that single-source-of-truth.
- W1 (vs. W3) — the TC is online and mediating; this is a normal rejection path. The GS10 GAP-29b admission criteria explicitly reserve W3 for cases where W1 is unavailable or compromised.

**Open questions (deferred):** None.

**Interface contract:**
- IC-REL-PRECURSOR (new): release-signature envelope schema extends with `precursor_genesis_op_id` (required when `release_reason: GENESIS_RESET_PREPARATION`).
- IC-TC-PRECURSOR-QUERY (new): TC exposes a precursor-lookup primitive against the Ledger, bounded to the audit window defined in C-GEN-REC-3-ENF-4.
- Appendix C: `HOLD_RELEASE_REASON_UNWARRANTED` registered as W1 SECURITY sync.

---

### GAP-35 — In-Flight Token Fate at Circuit-Breaker Trip — Spec Block

**What it must do / represent / enforce / guarantee:**
Eliminate the undefined-disposition window for tokens consumed but not yet PREPARED at the moment `CIRCUIT_TRIPPED` is written.

**Hard constraints:**
- **C-IFT-1 (Natural Outcome):** Tokens with `TOKEN_CONSUMED` recorded but no corresponding `PREPARED` at the moment of trip proceed to their natural PREPARED-or-abort outcome. No force-abandon signal is issued.
- **C-IFT-2 (Post-Trip PREPARED Blocking):** Any PREPARED entry arriving after `CIRCUIT_TRIPPED` is admitted to the Ledger (the Gate accepts signed PREPARED entries regardless of breaker state) but CANNOT advance to COMMITTED — READ_ONLY mode blocks token issuance for the second-phase commit signal. The PREPARED entry is preserved as forensic evidence for reset-time reconciliation.
- **C-IFT-3 (No New Gate↔TC Channel):** The spec explicitly does NOT introduce a trip-propagation signal from TC to the write Gate for in-flight token abandonment. The breaker is a TC-side suspension; in-flight tokens are handled by the natural termination path.

**§11.8.1 addition (one sentence):**
> Tokens consumed but not yet PREPARED at the moment `CIRCUIT_TRIPPED` is written proceed to their natural PREPARED-or-abort outcome; any resulting PREPARED entry is admitted to the Ledger but blocked from advancing to COMMITTED by READ_ONLY mode and is preserved as forensic evidence for reset-time reconciliation.

**Tradeoffs decided:**
- (a) over (b) and (c): option (a) preserves the token consumer's work investment, requires no new TC→Gate communication channel, and yields forensic completeness at reset. Option (b) (force-abandon) costs a new cross-component signal and discards evidence. Option (c) (proceed to PREPARED but cannot advance) is the realized behavior of (a) under READ_ONLY — (a) is the cleaner framing.

**Open questions (deferred):** None.

**Interface contract:** No new contract. §11.8.1 is the authoritative clause.

---

### GAP-43 — Recursive-Fault Reset Semantics — Spec Block

**§11.8.1 addition (one sentence):**
> When the triggering fault was a `BOUNDED_COMPENSATION_VIOLATION` (TC exceeded its reversal-only authority per A1-REVISED), standard IC-TC-RESET ceremony is sufficient; the `CIRCUIT_TRIPPED` entry with `trip_reason: TC_COMPENSATION_OVER_SCOPE` is the forensic record of the underlying cause, and no stricter reset ceremony is required.

**Tradeoffs decided:**
- Standard ceremony (vs. elevated ceremony) — the CIRCUIT_TRIPPED entry already provides the forensic attribution the Warden needs; elevating ceremony would conflate "what caused the trip" with "what reset requires." Trip-cause is already a first-class field.

**Open questions (deferred):** None.

**Interface contract:** No new contract; §11.8.1 clause is authoritative.

---

### GAP-46 — `ceremony_initiator_id` Under Key Rotation — Spec Block
**(Closes T-S4-N1 and T-S7-N1)**

**What it must do / represent / enforce / guarantee:**
Bind `operator_id` to a stable external identity established at first-boot CAK registration, and preserve the per-initiator rate-limit window across CAK rotation events.

**Hard constraints:**
- **C-OPID-1 (Stable Identity):** `operator_id` is a stable external identifier assigned at first-boot CAK registration ceremony and carried unchanged through all subsequent `CEREMONY_KEY_ROTATION_COMPLETE` events. It is NOT derived from the key fingerprint.
- **C-OPID-2 (Rotation Transparency):** Rate-limit windows keyed on `operator_id` (GAP-27 per-initiator limits) are preserved across rotation. A rotation does not reset the window.
- **C-OPID-3 (First-Boot Binding):** At first-boot CAK registration, the operator presents an external identity token; the registration ceremony writes `OPERATOR_IDENTITY_REGISTERED` recording `operator_id` bound to the initial CAK fingerprint. Subsequent rotations write `CEREMONY_KEY_ROTATION_COMPLETE` with `operator_id` carried forward and new CAK fingerprint.
- **C-OPID-4 (No Boot-Time Retention Check Needed — T-S4-N1):** Because `operator_id` is stable, the "outgoing key governs ceremonies initiated before rotation" invariant is satisfied naturally: ceremonies initiated pre-rotation carry the same `operator_id` as post-rotation ceremonies, and the rotation boundary is marked by the CAK fingerprint change on the ceremony signature envelope, not by an identity change. No new Ledger barrier contract is required.

**Closing T-S7-N1 (rate-limit state derived vs. primary):**
- **C-RLRF-1 (Retention Floor Constraint):** `scope_update_min_interval_seconds` MUST be strictly less than the minimum retention window for `SCOPE_UPDATED` Ledger entries. Rate-limit state derived from Ledger scans requires the source entries to outlive the rate-limit window; otherwise derivation silently degrades.
- **C-RLRF-2 (Boot-Time Validation):** On boot, the Orchestrator validates the configured interval against the retention floor. If `scope_update_min_interval_seconds >= min_retention_window_SCOPE_UPDATED`, boot is suspended with `RATE_LIMIT_RETENTION_CONFLICT` (SECURITY, sync, W1) carrying: `configured_interval_seconds`, `retention_floor_seconds`, `violated_constraint: C-RLRF-1`.
- Placement: §14.3 (rate-limit configuration) with cross-reference from §16.7 (boot validation).

**Tradeoffs decided:**
- Stable external identity (vs. key-fingerprint-derived) — preserves the intent of GAP-27 per-initiator rate limits across rotation; key-derived identity would silently reset the window on every rotation, defeating the purpose of the limit.
- First-boot binding + Ledger-recorded rotation history (vs. identity-provider integration) — keeps identity management inside the Ledger trust boundary; no external IdP dependency introduced for v1.
- Boot-time retention check (vs. runtime drift detection) — cheaper to fail fast at boot than to tolerate a silent rate-limit degradation that only manifests under SCOPE_UPDATED retention turnover.

**Open questions (deferred):** None. Both T-S4-N1 and T-S7-N1 close.

**Interface contract:**
- IC-CAK-IDENTITY (new): CAK registration and rotation ceremonies carry `operator_id` as a protocol-level field, stable across the rotation lifecycle.
- IC-BOOT-RLRF (new): boot sequence includes the retention-floor validation step before write path activation.
- Appendix C: `OPERATOR_IDENTITY_REGISTERED` and `RATE_LIMIT_RETENTION_CONFLICT` registered. `CEREMONY_KEY_ROTATION_COMPLETE` schema extended with `operator_id` (stable) and `new_cak_fingerprint` / `outgoing_cak_fingerprint`.

---

### GAP-52 — Archive Key-Lifecycle Policy — Spec Block

**What it must do / represent / enforce / guarantee:**
Ensure `ledger-archive/v1` bundles remain verifiable across decadal horizons without requiring an additional key-archive ceremony, by self-containing the verification material.

**Hard constraints:**
- **C-AKL-1 (Self-Contained Verification):** The `ledger-archive/v1` manifest (D104) MUST include `signer_public_key_material` — the full public-key bytes of the key used to sign the manifest — in addition to the existing `signer_identity` (identity string) and `signature` fields.
- **C-AKL-2 (Genesis Seal Anchoring):** At archive time, the signing key's public-key material is itself covered by a Genesis Seal snapshot entry (`ARCHIVE_KEY_SEALED`) so that the manifest's self-contained key can be cross-verified against the Seal family at restoration time.
- **C-AKL-3 (No Separate Key-Archive Ceremony):** With C-AKL-1 and C-AKL-2, restoration at decadal horizons requires only: (i) the archive bundle, (ii) the Genesis Seal snapshot covering the archive window, (iii) the current CAK for authorizing the restoration operation. No separate retired-key registry is required.
- **C-AKL-4 (Cross-Check Requirement):** Restoration MUST verify: the manifest's `signer_public_key_material` matches the key material covered by the `ARCHIVE_KEY_SEALED` entry in the Genesis Seal snapshot. Mismatch → restoration aborts with `ARCHIVE_KEY_MATERIAL_MISMATCH` (INTEGRITY, sync, W1).

**Tradeoffs decided:**
- Self-contained public key in manifest (vs. pure identity-string reference) — decouples verification from a live key registry that may not exist decades later.
- Genesis Seal cross-check (vs. trusting the manifest alone) — manifest self-containment alone would permit a substitution attack; anchoring the key material in the Seal family closes that gap.
- No separate key-archive ceremony (vs. a second archive flow just for keys) — reuses the existing Seal mechanism; adds one field and one entry type rather than a new subsystem.

**Open questions (deferred):** None for v1. V2 may consider key-revocation metadata (retired-but-not-compromised vs. retired-due-to-compromise) propagated into restoration trust decisions.

**Interface contract:**
- D104 manifest schema amended: `signer_public_key_material` (public-key bytes, required) added alongside existing `signer_identity` and `signature`.
- Appendix C: `ARCHIVE_KEY_SEALED` (INTEGRITY, sync, W1) and `ARCHIVE_KEY_MATERIAL_MISMATCH` (INTEGRITY, sync, W1) registered.

---

### GAP-53 — Ledger Verification on Very Large Chains — Documentation Addition

**Target section:** §16.4 (full verification operational notes).

**Documentation (to be inserted, no spec change):**

Expected upper-bound entry count — single-project lifetime:
- Reference workload: multi-year active project with ~100 Ledger entries/day average (mix of commit-path CONSISTENCY entries, periodic SECURITY entries, scheduled Pruning advisories, and SCOPE_UPDATED events).
- 1-year lifetime: ~36K entries.
- 5-year lifetime: ~180K entries.
- 10-year lifetime (decadal archival horizon): ~360K entries.
- Upper bound for a very active long-lived project: approximately 1M entries.

Full-verification feasibility — reference hardware:
- D108 full-verification budget: 24h or 10K entries (whichever fires). The 10K bound is a progress-pacing threshold, not a total-chain ceiling.
- At ~10ms per entry (signature + chain continuity check): 100K entries ≈ 17 minutes; 1M entries ≈ 2.8 hours; 10M entries ≈ 28 hours.
- **Infeasibility threshold:** 24h full verification on reference hardware becomes infeasible at approximately **10M entries**. Operators should plan for sampled-verification (v2 optimization) before approaching this threshold.

Operator guidance:
- Plan archival rotations to keep the active Ledger chain below 1M entries for comfortable full-verification headroom.
- Monitor chain length as an operational metric; at 5M entries, begin scoping sampled-verification tooling for v2 adoption.

**Open questions (deferred to v2):**
- Sampled verification with probabilistic coverage guarantee — target coverage percentage, sampling distribution, and integration with the pairing-check sub-routine (C-GTO-2).

---

### GAP-54 — Pre-Receive Git Hook Integrity — Spec Block

**What it must do / represent / enforce / guarantee:**
Protect the Tier 3 threshold-update pre-receive Git hook (D110) from local tampering that would silently accept out-of-bounds values.

**Decision:** **Option (b) — Tier 2 sealed artifact verification at boot**, with operational assumption fallback (c) explicitly noted.

**Hard constraints:**
- **C-HOOK-1 (Sealed Artifact Registration):** The canonical hook binary hash is recorded in a Tier 2 sealed corpus artifact (`hook-registry/v1`), anchored to the Genesis Seal family at initial registration and updated through the existing Tier 2 sealed-artifact rotation ceremony.
- **C-HOOK-2 (Boot-Time Verification):** At Orchestrator boot, the live hook binary hash is computed and compared against the sealed registry. Mismatch → boot suspends with `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) carrying: `expected_hook_hash`, `observed_hook_hash`, `sealed_artifact_id`.
- **C-HOOK-3 (No Runtime Re-Verification Hot-Path):** The hook is re-verified at boot only. Per-push re-hashing would introduce unbounded latency on a critical write path; boot-time sealing combined with OS-level filesystem protection (the assumption-layer fallback) is the layered defense.
- **C-HOOK-4 (Rotation Path):** Hook binary updates flow through the Tier 2 sealed-artifact rotation ceremony; an out-of-band hook replacement without a corresponding `hook-registry/v1` update fails boot verification on next restart.

**Tradeoffs decided:**
- (b) over (a): genesis-seal.json is Tier 1 mint-once — a hook bug-fix would require a full Genesis ceremony. Unacceptable friction for a maintenance artifact.
- (b) over (c) alone: OS filesystem permissions protect against casual tampering but not against privileged compromise. Sealed-artifact verification adds a cryptographic check that does not depend on OS trust.
- (b) reuses an existing pattern (sealed-artifact rotation) — no new subsystem introduced.

**Open questions (deferred):** None for v1.

**Interface contract:**
- IC-HOOK-BOOT (new): boot sequence includes hook-registry verification as a precondition to accepting Tier 3 config update pushes.
- Appendix C: `HOOK_INTEGRITY_VIOLATION` registered (SECURITY, sync, W1).

---

### T-PM-vs-PA — Provenance Monitor vs. Pruning Agent Advisory Queue Priority — Spec Block
**(Closes T-PM-vs-PA)**

**What it must do / represent / enforce / guarantee:**
Present a single, prioritized operator-review item per edge when both Git-side (`REQUIRES_HUMAN_REVIEW`) and external-source (`EXTERNAL_PROVENANCE_STALE`) advisories attach to the same edge, with auto-elevation for CORE-tier facts.

**Decision:** **Merge (a) + CORE-tier priority elevation (b).** Rejected (c) — two independent queue items — to avoid operator confusion and duplicate-resolution risk.

**Hard constraints:**
- **C-PMPA-1 (Merge Policy):** When an edge already has a `REQUIRES_HUMAN_REVIEW` record and an `EXTERNAL_PROVENANCE_STALE` advisory is emitted for the same `edge_id`, the external-provenance advisory APPENDS to the existing review record as an additional advisory-reason entry. No new queue item is created.
- **C-PMPA-2 (Reverse Direction):** When an `EXTERNAL_PROVENANCE_STALE` advisory already exists for an edge and a new `REQUIRES_HUMAN_REVIEW` is emitted for the same edge, the review record is extended (not replaced) to carry both reasons.
- **C-PMPA-3 (CORE-Tier Priority Elevation):** If the edge is CORE-tier and carries `EXTERNAL_PROVENANCE_STALE`, the merged review record's `priority` is auto-promoted to `HIGH`. Non-CORE tiers retain their baseline priority.
- **C-PMPA-4 (Single Queue Item):** The operator review queue displays at most one item per `edge_id`, with advisory reasons enumerated in the item's `advisory_reasons` field.
- **C-PMPA-5 (Resolution Semantics):** Resolving the review item requires the operator to acknowledge all enumerated advisory reasons. Partial resolution (e.g., acknowledging the Git-side reason but not the external-provenance reason) leaves the item in the queue with remaining reasons surfaced.

**Tradeoffs decided:**
- Merge (a) over independent items (c) — prevents operator blind spots where one item is resolved and the other lingers unattended for the same edge; also simplifies Pruning Agent queue-management logic.
- CORE-tier elevation (b) layered on merge (a) — addresses the real concern behind (b) without fragmenting the queue.
- Reverse-direction symmetry (C-PMPA-2) — closes the temporal ordering ambiguity: merge behavior should not depend on which advisory arrived first.

**Open questions (deferred):** None for v1.

**Interface contract:**
- IC-REVIEW-QUEUE (amended): review record schema gains `advisory_reasons` (ordered list, each with `reason_type`, `emitted_at`, `emitter_component`) and `priority` (computed per C-PMPA-3). Single record per `edge_id` invariant enforced by the Pruning Agent's `external_source_audit` sub-routine (D102).

---

## Gap Session Summary Block

**GAPS RESOLVED:**
- GAP-30 — Paired sync-write constraint (C-GTO-1) + monitor pairing-check on full verification (C-GTO-2); `GENESIS_TIMEOUT_TRIP_MISSING` ratified as CONSISTENCY async W1 advisory.
- GAP-31 — C-GEN-REC-3 enforcement specified: operator-cited precursor, Ledger lookup, Hold coverage + audit-window checks; `HOLD_RELEASE_REASON_UNWARRANTED` ratified as SECURITY sync W1 (not W3 — does not meet GS10 C-W3-1 admission criteria).
- GAP-34 — R-S3-3 applied: `governing_scope_hash` added to PREPARED and COMMITTED Ledger entries, captured at PREPARE, preserved at COMMIT, nullable for pre-amendment entries.
- GAP-35 — Option (a) ratified (natural-outcome); single sentence added to §11.8.1 covering post-trip PREPARED preservation under READ_ONLY.
- GAP-43 — Standard IC-TC-RESET ceremony confirmed sufficient for `BOUNDED_COMPENSATION_VIOLATION`-triggered trips; single-sentence addition to §11.8.1 per recommended text.
- GAP-46 — Stable external `operator_id` bound at first-boot CAK registration, carried across rotation; **closes T-S4-N1** (rotation registry ordering) and **T-S7-N1** (rate-limit retention floor constraint, boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation).
- GAP-52 — D104 manifest amended with `signer_public_key_material`; Genesis Seal cross-check via `ARCHIVE_KEY_SEALED` entry; no separate key-archive ceremony needed.
- GAP-53 — §16.4 documentation addition: expected upper-bound entry counts (100K–1M typical single-project, 10M infeasibility threshold on reference hardware); sampled-verification flagged for v2.
- GAP-54 — Option (b) selected: hook binary hash in Tier 2 sealed artifact (`hook-registry/v1`), boot-time verification, `HOOK_INTEGRITY_VIOLATION` on mismatch.
- **T-PM-vs-PA — RESOLVED.** Merge + CORE-tier priority elevation; single queue item per `edge_id`; both-reason acknowledgment required for resolution.

**GAPS PARTIALLY RESOLVED:** None.

**GAPS DEFERRED:** None from this session's allocation.

**NEW GAPS SURFACED:**
- **GAP-55 (Low, SCT):** Sampled-verification design for Ledger chains >10M entries (coverage guarantee, sampling distribution, integration with C-GTO-2 pairing-check). Deferred to v2 per GAP-53 documentation.
- **GAP-56 (Low, Warden):** Retired-key revocation metadata semantics for archive restoration (retired-clean vs. retired-compromised) — propagation into restoration trust decisions. Deferred to v2 per GAP-52 open question.

**NEW TENSIONS SURFACED:** None. GS11 closes two tensions (T-S4-N1, T-S7-N1, T-PM-vs-PA) and surfaces no new cross-domain conflicts.

**INTERFACE CONTRACTS DEFINED (new):**
- IC-PREPARE-SCOPE — Orchestrator → TC scope-hash publication at PREPARE (GAP-34).
- IC-MON-GTOTM — Ledger integrity monitor pairing-check sub-routine (GAP-30).
- IC-REL-PRECURSOR — release-signature envelope precursor-citation extension (GAP-31).
- IC-TC-PRECURSOR-QUERY — TC precursor-lookup primitive against the Ledger (GAP-31).
- IC-CAK-IDENTITY — stable `operator_id` carried across CAK rotation (GAP-46).
- IC-BOOT-RLRF — boot-time retention-floor validation (GAP-46 / T-S7-N1).
- IC-HOOK-BOOT — hook-registry boot verification (GAP-54).
- IC-REVIEW-QUEUE (amended) — single review record per edge, enumerated advisory reasons (T-PM-vs-PA).

**APPENDIX C ADDITIONS (new entry types):**
- `GENESIS_TIMEOUT_TRIP_MISSING` (CONSISTENCY, async, W1)
- `HOLD_RELEASE_REASON_UNWARRANTED` (SECURITY, sync, W1)
- `OPERATOR_IDENTITY_REGISTERED` (SECURITY, sync, W1)
- `RATE_LIMIT_RETENTION_CONFLICT` (SECURITY, sync, W1)
- `ARCHIVE_KEY_SEALED` (INTEGRITY, sync, W1)
- `ARCHIVE_KEY_MATERIAL_MISMATCH` (INTEGRITY, sync, W1)
- `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1)

**SCHEMA AMENDMENTS:**
- PREPARED / COMMITTED: + `governing_scope_hash` (nullable for pre-amendment entries).
- `ledger-archive/v1` manifest (D104): + `signer_public_key_material`.
- `CEREMONY_KEY_ROTATION_COMPLETE`: + `operator_id` (stable), + `outgoing_cak_fingerprint`, + `new_cak_fingerprint`.
- Review record (Pruning Agent): + `advisory_reasons` (ordered list), + `priority` (computed).

**DOWNSTREAM INPUTS TO GS12/GS13:**
- W-tier determinations in GS11 are W1-only; no new W3 carve-outs proposed. GS10's C-W3 admission criteria held as the gating policy — no revision to Appendix C-W3 from this session.
- Chain-length operational guidance (GAP-53) feeds into v2 roadmap discussions in GS12/GS13 if those sessions scope post-v1 planning.
