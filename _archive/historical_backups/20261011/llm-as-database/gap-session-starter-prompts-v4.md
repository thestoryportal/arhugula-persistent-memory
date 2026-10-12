# LLM as Database: Agent Harness Architecture
## Gap Session Starter Prompts v4.0 — GS10 Through GS13

> **Scope:** New sessions only (GS10–GS13). GS1–GS4 prompts in `gap-session-starter-prompts.md`
> and `gap-session-starter-prompts-v2.md`. GS5–GS9 prompts in `gap-session-starter-prompts-v3.md`.
> All prior sessions executed.
>
> **Run order:** GS10, GS11, GS12 are independent and can run in any order.
> Run GS13 last.
>
> **Model settings:**
> | Session | Model | Web Search | Deep Research |
> |---------|-------|------------|---------------|
> | GS10 | Opus 4.6 | ✓ | ✗ |
> | GS11 | Opus 4.6 | ✓ | ✗ |
> | GS12 | Sonnet 4.6 | ✓ | ✗ |
> | GS13 | Opus 4.6 | ✓ | ✗ |
>
> **Key decisions from completed sessions (referenced throughout):**
> - D92–D96 (GS4 v2/v3): Dual-key hierarchy; CeremonyToken framework; CAK physical storage;
>   IC-SCOPE-AUTH-1; IC-TC-RESET A3 populated.
> - GS5 v3: GAP-21/24/25 resolved; A1-REVISED/A2/A8/A10 applied; §13.5 step 3a added;
>   14 new Ledger entry types.
> - GS6 v3: GAP-22/23 resolved; GENESIS_TIMED_OUT added; A12 applied; C-GEN-REC-1/2/3.
> - GS7 v3: T13 resolved (three-tier legacy advisory); GAP-27 resolved; IC-MANIFEST-1 ratified
>   (A9 applied); A4–A7b applied.
> - GS8 v3: GAP-8 resolved (D93–D95: corpus-author-registry, cadence, Day-0 preconditions);
>   GAP-10 resolved (D96–D98: dual-signal tagging, Q1–Q5, promotion ceremony).
> - GS9 v3: GAP-11/12/14/28 resolved (D99–D111: external provenance, retention two-tier,
>   async threshold rationale, notification boundary).

---

═══════════════════════════════════════════════════════════════════════════════
## GS10 — NEXT SESSION 🔜
### Gaps: GAP-29, GAP-33, GAP-36, GAP-37
### Skill: framework-council (Warden primary; MEMIT + Graph Data Architect + SCT secondary)
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 10 of 13 — Warden (primary) + MEMIT Specialist + Graph Data Architect
                        + State Consistency Theorist

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline, updated by
GS1–GS9. This session addresses four Warden-primary gaps surfaced across prior
sessions, all with no upstream dependency. The W3 scope consolidation (GAP-29b)
is the highest-priority item and should be addressed first.

Gaps to resolve in this session:

─── GAP-29 ──────────────────────────────────────────────────────────────────
(Full text as in original prompt — W3 scope consolidation + manifest lattice completeness)
─────────────────────────────────────────────────────────────────────────────

─── GAP-33 (verify only — resolved in v2 GS8) ──────────────────────────────
Verify IC-DRYRUN-1 is consistent with GS4 CeremonyToken framework. Confirm the
`dry_run_executor` access role is properly registered as a CAK-authorized identity.
No re-resolution needed unless inconsistency is found.
─────────────────────────────────────────────────────────────────────────────

─── GAP-36 ──────────────────────────────────────────────────────────────────
(Full text as in original prompt — CIRCUIT_RESET_REJECTED rate limiting)
─────────────────────────────────────────────────────────────────────────────

─── GAP-37 ──────────────────────────────────────────────────────────────────
(Full text as in original prompt — governance write carve-out during CIRCUIT_TRIPPED)
─────────────────────────────────────────────────────────────────────────────

─── GAP-40 ──────────────────────────────────────────────────────────────────
Domain(s): Orchestration Comparativist + Warden
Priority: High — Source: v2 GS4

Description: First-boot CAK bootstrap tool specification. The `ceremony_authorization_key_anchor`
in `genesis-seal.json` must be written mint-once by an operator-run bootstrap tool before
harness first-boot. The harness cannot write its own ceremony key (circular trust). The tool
must: run with operator credentials outside the harness process identity; accept
operator-generated public key material; write `genesis-seal.json` atomically with hash
verification; emit a signed boot manifest the harness verifies at first boot. The tool's
trust model, distribution channel, and signing-authority chain are not yet specified. This gap
was surfaced in v2 GS4 alongside T-S4-N2 (bootstrap-tool trust asymmetry).

─── GAP-41 ──────────────────────────────────────────────────────────────────
Domain(s): Warden
Priority: Medium — Source: v2 GS4

Description: Per-CAK ceremony rate limiting. If a CAK is briefly exposed (momentary HSM
unlock, screen capture during signing), an attacker with short-window access could issue many
ceremonies rapidly before detection. A per-CAK burst limit independent of per-ceremony-type
limits is needed — distinct from GAP-27 (scope-update-specific) and GAP-38 (SCOPE_HASH_MISMATCH
aggregate detection). Requires: definition of acceptable ceremony burst patterns; burst window
duration; Ledger entry type for CAK burst exceeded.

─── GAP-42 ──────────────────────────────────────────────────────────────────
Domain(s): Warden
Priority: Medium — Source: v2 GS4

Description: Break-glass emergency channel full specification. When a CAK is declared
compromised (`CAK_COMPROMISE_DECLARED`), all ceremonies are blocked with no v1 rotation path
(T15). The channel is currently stubbed as "a second Tier 1 break-glass anchor or out-of-band
declaration." Full spec required: second key? Out-of-band Ledger injection path? Pre-signed
envelope? How is the break-glass channel itself prevented from becoming a parallel compromise
vector? Relates to GAP-19 v2 outline (OQ-S-CAK-1).

─── GAP-44 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + State Consistency Theorist
Priority: Medium — Source: v2 GS6

Description: `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` Ledger entry classification. GS6 v3
specifies that a new Genesis cannot acquire a Hold while a failed Genesis's Hold is active.
The Ledger entry for this pre-flight refusal is provisionally classified INTEGRITY (operational
failure). However, if the blocking attempt comes from a compromised agent repeatedly attempting
Genesis initiation, SECURITY classification or W3 eligibility may be warranted.
Warden co-review required to confirm INTEGRITY classification is correct per threat model.
Related to GAP-29b (W3 consolidation) — Warden should review this alongside the W3 policy.

─── GAP-47 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist + Warden
Priority: Low — Source: v2 GS8

Description: Dry-run artifact store pruning ceremony authority. `DRY_RUN_ARTIFACT_PRUNED`
(per IC-DRYRUN-1, GAP-33 resolved) is emitted under a signed retention ceremony. The ceremony
type is not yet integrated into the GS4 CeremonyToken framework. Needs assignment as
`RETENTION_PRUNING` ceremony type or equivalent — a one-line addition to the CeremonyToken
ceremony_type enum.

Description (two components):

(a) Manifest lattice completeness probe (source: GS1 v1):
The `larql_migration_manifest` does not require coverage of every version pair
in [min_supported_larql_version, current_larql_version]. A missing lattice edge
(e.g., v1.1→v1.2 absent when min=v1.0 and current=v1.3) surfaces only at
compaction time as a translation failure. The Gate accepts patches at all versions
between min and current via the LARQL_VERSION_LEGACY advisory path, so Gate-time
enforcement cannot catch the gap. IC-MANIFEST-1 (ratified GS7 v3) specifies a
7-check commit gate — lattice completeness is not among them.

(b) W3 scope consolidation (source: GS5 v3):
W3 was originally single-purpose (INTEGRITY_VIOLATION_EMERGENCY only per §16.2).
Three narrow W3 carve-outs were added across GS4/GS5/GS6:
  DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF — on deprecated Ledger entry post-cutoff
  ORCHESTRATOR_UNAVAILABILITY_ESCALATED — on extended Orchestrator unavailability
  LEDGER_SIGNATURE_REVERIFICATION_FAILED — on tamper detection during reconcile
GAP-31 (GS11) may add a fourth (HOLD_RELEASE_REASON_UNWARRANTED). A Warden-led
consolidation pass must: (1) ratify each existing carve-out with explicit criteria,
(2) define the maximum W3 carve-out scope for v1, (3) establish a policy for future
carve-out additions.

─── GAP-33 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + Graph Data Architect
Priority: Medium
Status: Open — source: GS7 v3

Description: IC-MANIFEST-1 references `dry_run_artifact_hash` in commit gate check 5
("dry_run_artifact_hash present in manifest entry exists in dry-run store") and check
6 ("dry-run report at that hash shows zero translation failures, zero unexpected
VERSION_REJECTED"). The storage location for dry-run reports, retention policy,
tamper-evidence of the artifact hash chain, and operator verification UX are
unspecified. The 7-day freshness window (check 7) requires artifacts to remain
accessible for at least 7 days; no storage spec governs this.

─── GAP-36 ──────────────────────────────────────────────────────────────────
Domain(s): Warden
Priority: Low
Status: Open — source: GS2 v1 (NEW-GAP-SC-3)

Description: No rate limit or escalation policy on repeated `CIRCUIT_RESET_REJECTED`
attempts. Signature verification blocks forgery, but an operator submitting repeated
invalid reset ceremonies creates Ledger noise without any detection or cap. A Warden
policy decision on whether to add: (a) a rate limit (N rejections in M minutes →
Ledger advisory entry + human alert), (b) a progressive escalation, or (c) accept
current state (no cap, low risk given signature requirement).

─── GAP-37 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + State Consistency Theorist
Priority: Medium
Status: Open — source: GS2 v1 (NEW-GAP-SC-4), partially addressed by A1-REVISED

Description: §11.8.1 does not explicitly state that governance-category W1 writes
proceed during CIRCUIT_TRIPPED while token-mediated writes do not. The CIRCUIT_RESET
entry (the exit mechanism) is a W1 write occurring while in CIRCUIT_TRIPPED / READ_ONLY
state, which suspends "write token issuance." The implied invariant is that governance
ceremony writes are exempt from write suspension — A1-REVISED and the CeremonyToken
model make this operative in practice — but the spec text does not state it explicitly.
Required: one sentence in §11.8.1 making the carve-out explicit.

Proposed text (for ratification or revision):
"Write suspension during CIRCUIT_TRIPPED applies to token-mediated application writes.
Governance-category W1 Ledger entries written as part of the signed reset ceremony
(CIRCUIT_RESET, DEPENDENCY_HOLD_RELEASED_SIGNED with release_reason:
GENESIS_RESET_PREPARATION, and RECONCILIATION_COMPLETE) proceed regardless of
CIRCUIT_TRIPPED state."
─────────────────────────────────────────────────────────────────────────────

Relevant context from v1.1 spec + completed sessions:

§16.2 — Three-Tier Writer Model
"W3 — Emergency Escalation Path: Gate, TC, and Boot-verifier each hold a limited
emergency-write capability restricted to a single entry type: INTEGRITY_VIOLATION_
EMERGENCY. Bypasses Orchestrator mediation. Max 1 entry per minute per component.
Strict schema enforcement. Immediate write suspension. Forced human investigation.
Purpose: log compromised-Orchestrator scenarios where normal W1 path is the problem."
[GS4/GS5/GS6 added three further W3-eligible types — each narrowly justified but
cumulatively expanding W3 scope beyond original single-purpose design.]

§11.8.1 — CIRCUIT_TRIPPED and Write Suspension (D84, A1-REVISED from GS5 v3)
"On any circuit-breaker trip, the TC enters READ_ONLY mode immediately without human
action. Inference, query, and read operations proceed normally; write token issuance
is suspended. Write resumption requires a signed reset ceremony (IC-TC-RESET)."
[CIRCUIT_RESET is a W1 write. The carve-out is operative but unstated.]

IC-MANIFEST-1 — larql_migration_manifest Entry (ratified GS7 v3, A9 applied)
Commit gate checks 5–7:
"5. dry_run_artifact_hash present in manifest entry exists in dry-run store.
 6. Dry-run report at that hash shows zero translation failures, zero unexpected
    VERSION_REJECTED.
 7. Ceremony entry timestamp is within 7 days of commit attempt (provisional
    freshness)."
[Dry-run store is referenced but unspecified.]

§8.10 — Anchor-Superseded Archive
"Patches carrying larql_syntax_version below current are translated via
larql_migration_manifest before MEMIT compile. Translation failure aborts compaction."
[Manifest lattice gap surfaces here — missing version pair = compaction-time failure.]

Appendix C — W3-eligible entries (current):
Original: INTEGRITY_VIOLATION_EMERGENCY
GS4 additions: (via CEREMONY_SIGNATURE_INVALID path — not W3)
GS5 additions: DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF, ORCHESTRATOR_UNAVAILABILITY_
  ESCALATED, LEDGER_SIGNATURE_REVERIFICATION_FAILED
GS6 pending: HOLD_RELEASE_REASON_UNWARRANTED (GAP-31, W3 eligibility TBD)

Invoke the framework-council skill. Convene Warden (primary), MEMIT Specialist, Graph
Data Architect, and State Consistency Theorist.

For GAP-29a (manifest lattice completeness):
1. Add an 8th check to IC-MANIFEST-1 commit gate: verify that the manifest contains
   a translation rule for every version pair (v_i → current) where v_i ∈
   [min_supported_larql_version, current_larql_version). Define what "covers" means
   (direct rules only, or transitive via intermediate versions?). Define the rejection
   Ledger entry (MANIFEST_LATTICE_INCOMPLETE, SECURITY, sync?).

For GAP-29b (W3 scope consolidation):
2. Ratify or restrict each of the three existing W3 carve-outs. For each: confirm the
   criteria making W1 unavailable are genuine (not just "inconvenient"); confirm the
   entry type is truly restricted in schema; confirm the 1-per-minute rate limit applies.
3. Define the maximum W3 carve-out scope policy for v1: e.g., "W3 is limited to
   INTEGRITY_VIOLATION_EMERGENCY plus entries where (a) Orchestrator is compromised
   or unavailable AND (b) the entry is required to preserve forensic evidence of the
   failure." Any future carve-out must satisfy both conditions.
4. Note that GAP-31 (GS11) may add HOLD_RELEASE_REASON_UNWARRANTED as a fourth
   carve-out candidate — the policy from step 3 should cover it.

For GAP-33 (dry-run artifact storage):
5. Define dry-run report storage: location, retention policy (must cover freshness
   window + operator review period), tamper-evidence mechanism (hash-anchored in
   Ledger or manifest?). Simplest viable approach: `<harness_root>/.dry-run-store/`
   with operator-signed SHA-256 manifest; entries retained until the manifest entry
   that references them is compacted or deprecated. Define whether storage is
   Warden-audited or operator-owned.

For GAP-36 (CIRCUIT_RESET_REJECTED rate limiting):
6. Choose one: (a) add rate limit with Ledger advisory entry and human alert after N
   rejections in M minutes; (b) accept current state. If (a), define N and M.

For GAP-37 (governance write carve-out):
7. Ratify or revise the proposed §11.8.1 explicit carve-out sentence. SCT confirms
   the write path is unambiguous. Warden confirms the scope of the exemption.

At the end of the session, generate a Gap Session Summary Block:
GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged]
NEW TENSIONS SURFACED: [any cross-domain conflicts]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GS11
### Gaps: GAP-30, GAP-31, GAP-34, GAP-35
### Skill: framework-council (State Consistency Theorist primary; Warden co-owner)
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 11 of 13 — State Consistency Theorist (primary) + Warden (co-owner)

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline, updated by
GS1–GS9. This session addresses four SCT-domain lifecycle and schema gaps with
no upstream dependency (independent of GS10).

Gaps to resolve in this session:

─── GAP-30 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist
Priority: Medium
Status: Open — source: GS6 v3

Description: GENESIS_TIMED_OUT and CIRCUIT_TRIPPED must appear in strict order within
a sync-write window. No monitor is specified for detecting "GENESIS_TIMED_OUT written
with no subsequent CIRCUIT_TRIPPED." Entry type GENESIS_TIMEOUT_TRIP_MISSING is
reserved (GS6 v3) but detection path is TBD. Without detection, a partial write
sequence (GENESIS_TIMED_OUT without CIRCUIT_TRIPPED) is an invisible consistency gap.

─── GAP-31 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist + Warden
Priority: Medium
Status: Open — source: GS6 v3

Description: If an operator signs DEPENDENCY_HOLD_RELEASED_SIGNED with
release_reason: GENESIS_RESET_PREPARATION but no matching GENESIS_TIMED_OUT entry
exists in the audit window, the TC must reject. C-GEN-REC-3 (ratified GS6 v3) states
"release_reason: GENESIS_RESET_PREPARATION legitimate only when a matching
GENESIS_TIMED_OUT precursor exists in the audit window." But the detection/rejection
logic — how the TC queries the Ledger for the GENESIS_TIMED_OUT precursor, what the
audit window duration is, and whether rejection produces HOLD_RELEASE_REASON_UNWARRANTED
as a W3 entry (fourth W3 carve-out, ties to GAP-29b) — is not specced.

─── GAP-34 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist + Warden
Priority: Medium
Status: Open — source: GS3 v1 (R-S3-3), not confirmed applied in any session

Description: `governing_scope_hash` field on commit Ledger entries. When an active
PREPARED transaction spans a SCOPE_UPDATED event, the commit Ledger entry does not
carry a reference to which scope hash governed the PREPARED state. Post-update forensic
queries cannot unambiguously determine which scope governed a given commit when the
commit and the SCOPE_UPDATED entry occupy adjacent Ledger positions.

GS3 v1 refinement R-S3-3 recommended adding `governing_scope_hash` (set at PREPARE
time, preserved through COMMIT). GS5 v3 addressed the Ledger ordering question via
IC-SCOPE-RECONCILE but did not confirm R-S3-3 was applied. This session confirms
whether the field was added and, if not, applies the amendment.

─── GAP-35 ──────────────────────────────────────────────────────────────────
(Full text as in original prompt — in-flight token fate at circuit-breaker trip)
─────────────────────────────────────────────────────────────────────────────

─── GAP-43 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist + Warden
Priority: Low — Source: v2 GS5

Description: Recursive-fault reset semantics. If the circuit breaker tripped because of a
`BOUNDED_COMPENSATION_VIOLATION` (TC violated its own reversal-only constraint per A1-REVISED),
the operator signing a circuit reset re-enters a system whose last fault was the TC violating
its own bounded authority. Whether this requires a stricter reset ceremony or standard
IC-TC-RESET with documented forensic context is unspecified. Short resolution: standard
ceremony is likely sufficient; produce one sentence in §11.8.1 covering this case.

─── GAP-46 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + State Consistency Theorist
Priority: Medium — Source: v2 GS7

Description: `ceremony_initiator_id` attribution under key rotation. When `CEREMONY_KEY_ROTATION_COMPLETE`
rotates the CAK, is `operator_id` (used in per-initiator rate limiting, GAP-27) stable across
rotation? If derived from key fingerprint, rotation resets the rate-limit window — fresh budget.
If stable external identity (bound at first-boot CAK registration and carried through rotation),
window is preserved. Resolving this also closes T-S4-N1 (rotation registry ordering) — the
decision on operator_id stability determines whether a boot-time `RATE_LIMIT_RETENTION_CONFLICT`
check is needed.

─── GAP-52 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + State Consistency Theorist
Priority: Medium — Source: v2 GS11

Description: Archive key-lifecycle policy. When a Ledger bundle's signing key has been retired
from the active Orchestrator Key Anchor (e.g., 10+ years after archival), bundle restoration
requires access to archived key material. Whether the Genesis Seal snapshot suffices across
decadal horizons or whether a separate key-archive ceremony is required is unspecified. The
archival format `ledger-archive/v1` (D104, GS9 v3) specifies `signer_identity` and `signature`
on the manifest but does not address verification when the signing key is no longer in the active
anchor registry.

─── GAP-53 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist
Priority: Low — Source: v2 GS11

Description: Ledger verification on very large chains. Full verification cost (D108: 24h or
10K entries) scales with chain length. On a multi-year, multi-million-entry Ledger, this may
become an operational bottleneck. Sampled verification with probabilistic coverage guarantee
may be required as a future optimization. For v1, document: (a) what the expected upper-bound
entry count is over a single-project lifetime, and (b) at what entry count the 24h full
verification becomes infeasible on reference hardware, so operators know when to plan for v2.

─── GAP-54 ──────────────────────────────────────────────────────────────────
Domain(s): Warden
Priority: Medium — Source: v2 GS11

Description: Pre-receive Git hook integrity. The Tier 3 config modification path depends on
a pre-receive Git hook enforcing bounds, signatures, and rationale for threshold updates
(D110, GS9 v3). The spec does not define how the hook itself is integrity-protected against
local tampering. A compromised hook could silently accept out-of-bounds threshold values.
Options: (a) hook binary hash anchored in genesis-seal.json (Tier 1); (b) hook verified
against a sealed corpus artifact at boot; (c) accept as operational assumption (hook is
protected by OS filesystem permissions). Related to GAP-29 (W3 consolidation).

Description: In-flight token fate at circuit-breaker trip moment. Tokens that have
been consumed (TOKEN_CONSUMED written to Ledger) but have not yet reached PREPARED
are in undefined disposition when CIRCUIT_TRIPPED is written. Three options:
(a) in-flight tokens proceed to their natural PREPARED-or-abort outcome,
(b) in-flight tokens are force-abandoned (TOKEN_ABANDONED emitted on trip),
(c) in-flight tokens proceed to PREPARED but cannot advance to COMMITTED.

The undefined window is narrow but occurs exactly when the system has decided it
cannot be trusted — "undefined" is unsafe regardless of window size.
─────────────────────────────────────────────────────────────────────────────

Relevant context from v1.1 spec + completed sessions:

§11.8 — Circuit Breaker (D48, C-TC3)
"On trip: systemwide write suspension (READ_ONLY mode). Thresholds: 3 consecutive
2PC failures in one task; 5 across tasks in 10-minute window; diverged state →
immediate trip."

§11.8.1 — READ_ONLY Mode (D84, amended GS5/GS6)
"On any circuit-breaker trip, the TC enters READ_ONLY mode immediately. Write token
issuance is suspended. Tokens already consumed but not yet PREPARED — see GAP-35."

§11.5.1 — PREPARED-State Timeout (D85)
"Genesis timeout: circuit breaker trips immediately (DIVERGED_STATE type per IC-TC-RESET).
No auto-compensation — partial compile state preserved as forensic evidence."

§10.9 — SCOPE_UPDATED semantics (D87, IC-SCOPE-UPDATE)
"Active PREPARED transactions are not interrupted; scope changes are forward-only.
SCOPE_UPDATED must be written to Ledger before Orchestrator's in-memory scope
registry is updated."
[R-S3-3: governing_scope_hash field on PREPARED and COMMITTED entries — confirms
which scope governed the transaction through its full lifecycle.]

From GS6 v3:
- C-GEN-REC-3: "release_reason: GENESIS_RESET_PREPARATION legitimate only when a
  matching GENESIS_TIMED_OUT precursor exists in the audit window."
- GENESIS_TIMED_OUT (CONSISTENCY, sync) — fields include: genesis_op_id, affected_
  hold_ids (Hold Registry snapshot at timeout), compile_state_ref.
- HOLD_RELEASE_REASON_UNWARRANTED — entry type reserved; W3 eligibility TBD (GAP-31).
- GENESIS_TIMEOUT_TRIP_MISSING — entry type reserved; detection path TBD (GAP-30).

Appendix C — CONSISTENCY entries (relevant):
"TIMED_OUT (sync — non-Genesis transactions only, C-TIMED-OUT-1)"
"GENESIS_TIMED_OUT (sync — Genesis timeout, no compensation_direction field)"
"CIRCUIT_TRIPPED (sync — trip_type: CONSECUTIVE_FAILURE | CROSS_TASK_FAILURE |
  DIVERGED_STATE)"

Invoke the framework-council skill. Convene State Consistency Theorist (primary)
and Warden (co-owner for GAP-31 and GAP-34).

For GAP-30 (GENESIS_TIMED_OUT → CIRCUIT_TRIPPED ordering monitor):
1. Define the detection mechanism for "GENESIS_TIMED_OUT with no subsequent
   CIRCUIT_TRIPPED within the expected sync-write window." Options: (a) TC must write
   both entries atomically (paired write); (b) Ledger integrity monitor checks for
   orphaned GENESIS_TIMED_OUT on every full verification pass; (c) chain-break between
   the two entries triggers GENESIS_TIMEOUT_TRIP_MISSING advisory.
2. Ratify or revise the GENESIS_TIMEOUT_TRIP_MISSING entry type (category, sync/async,
   fields). Confirm whether this is a W1 entry or requires W3.

For GAP-31 (precursor validation for GENESIS_RESET_PREPARATION):
3. Define TC precursor-check logic: before accepting DEPENDENCY_HOLD_RELEASED_SIGNED
   with release_reason: GENESIS_RESET_PREPARATION, TC MUST query Ledger for a
   GENESIS_TIMED_OUT entry with matching genesis_op_id within audit window.
4. Define the audit window duration (fixed? relative to Hold placement timestamp?).
5. On missing precursor: reject signed release, emit HOLD_RELEASE_REASON_UNWARRANTED.
   Warden: decide W3 eligibility for this entry (adds to W3 consolidation context in
   GAP-29b — may defer that decision to GS10 for consolidation).

For GAP-34 (governing_scope_hash on commit entries):
6. Confirm whether R-S3-3 was applied in any session. If not: specify the amendment —
   `governing_scope_hash` field added to PREPARED and COMMITTED Ledger entries; value
   set at PREPARE time from the Orchestrator's current scope registry; preserved
   unchanged at COMMIT. Warden confirms this satisfies the forensic audit requirement
   for scope-transition boundary queries.

For GAP-35 (in-flight token fate at circuit-breaker trip):
7. Select one disposition for tokens in TOKEN_CONSUMED state when CIRCUIT_TRIPPED
   is written. Recommend option (a) — proceed to natural outcome — with rationale:
   (a) preserves the token consumer's work investment, (b) the PREPARED entry (if
   reached) will still be blocked from advancing to COMMITTED under READ_ONLY, and
   (c) force-abandonment of in-flight tokens requires a new TC→Gate communication
   path that does not currently exist. Ratify and add one sentence to §11.8.1.

At the end of the session, generate a Gap Session Summary Block:
GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged]
NEW TENSIONS SURFACED: [any cross-domain conflicts]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GS12
### Gaps: GAP-38, GAP-39
### Skill: framework-council (Warden + Orchestration + Validation)
### Independent — no upstream dependency
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 12 of 13 — Warden + Orchestration Comparativist + Validation Contract Architect

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline, updated by
GS1–GS9. Two short, bounded gaps with no upstream dependencies.

Gaps to resolve in this session:

─── GAP-38 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + Orchestration Comparativist
Priority: Low
Status: Open — source: GS3 v1 (G-S3-N3)

Description: The per-invocation SCOPE_HASH_MISMATCH escalation (A4: 2 consecutive →
human review) can be circumvented by an attacker who spreads mismatches across
invocations — trigger scope update, allow 1 mismatch, allow 1 success, repeat.
A time-windowed aggregate metric is required: N SCOPE_HASH_MISMATCH events across
ALL invocations within M seconds triggers Warden alert, independent of per-invocation
threshold. This is additive to, not a replacement for, the per-invocation rule.

Suggested starting values for spec discussion: N=10, M=60 seconds.

─── GAP-39 ──────────────────────────────────────────────────────────────────
Domain(s): Validation Contract Architect
Priority: Medium
Status: Open — source: GS4 v1 (G-S4-N3), reinforced by GS8 v3 (OQ-V9)

Description: D97 qualification criterion Q5 requires constitutional tests to be
deterministic ("no randomness, no network, no unstubbed wall-clock dependencies").
But no clock injection mechanism is specified for the Validator sandbox. Constitutional
tests that assert time-sensitive framework invariants — notably C26 (corpus staleness
transition at 180 days) and any test asserting Ledger verification cadence behavior —
require a testable clock abstraction. Without it, Q5 cannot be validated at
nomination review time (how does the reviewer confirm a test has no unstubbed wall-
clock dependencies?), and time-sensitive constitutional tests cannot be written.

GS8 v3 surfaced OQ-V9 as a related question (whether Q5 should be validated at
runtime by structural inspection of the test's failure assertion message) — both
OQ-V9 and the clock injection gap can be addressed in this session.
─────────────────────────────────────────────────────────────────────────────

Relevant context from v1.1 spec + completed sessions:

§14.3 — SCOPE_HASH_MISMATCH Failure Mode (A4 applied GS7 v3)
"Two consecutive SCOPE_HASH_MISMATCH errors for the same invocation → Orchestrator
escalates to human review queue."
[A4 covers per-invocation pattern. GAP-38 adds cross-invocation aggregate detection.]

§10.9 — Scope Update Ceremony
"active_agent_ids listed in SCOPE_UPDATED. SCOPE_UPDATED carried scope_change_type:
EXPANDING | NARROWING | RESTRUCTURING (GS4 addition)."

From GS7 v3 — GAP-27 resolution:
"scope_update_min_interval_seconds (Tier 1, default 3,600s, per-agent_id).
SCOPE_UPDATE_RATE_EXCEEDED (SECURITY, sync) on rate limit violation."
[GAP-38 is the detection complement: rate limit prevents rapid ceremony flooding;
aggregate mismatch detection catches misuse patterns that slip under per-invocation
and per-ceremony thresholds.]

From GS8 v3 — D97 Q5 qualification criterion:
"Deterministic: no randomness (or seeded and declared), no network access, no
unstubbed wall-clock dependencies."
[Clock injection mechanism not defined. OQ-V9: runtime structural validation of Q5.]

From GS8 v3 — D98 promotion ceremony:
"nomination_record: {nomination_id, test_path, task_id_of_origin,
  qualification_checklist: [{criterion, status, evidence_ref}×5], ...}"
[evidence_ref for Q5 must reference something — what constitutes evidence that
clock is stubbed? This session defines that.]

Invoke the framework-council skill. Convene Warden, Orchestration Comparativist
(for GAP-38), and Validation Contract Architect (for GAP-39).

For GAP-38 (cross-invocation aggregate SCOPE_HASH_MISMATCH detection):
1. Ratify aggregate threshold (N mismatches across invocations within M seconds).
   Starting values N=10, M=60s are for discussion; ratify or revise. Confirm that
   aggregate threshold is per-Orchestrator-instance (global, not per-agent-id, unlike
   the per-invocation per-agent rule).
2. Define the alert path: does exceeding the aggregate threshold produce a Ledger entry
   (new SCOPE_MISMATCH_AGGREGATE_ALERT, SECURITY, async?) or route directly to human
   review queue without Ledger entry? Or both?
3. Define whether the aggregate counter resets after each human review resolution or
   on a time window basis.

For GAP-39 (constitutional test clock dependency + OQ-V9):
4. Define the clock injection requirement for the Validator sandbox: constitutional
   tests that assert time-dependent behavior MUST declare a clock_stub_required: true
   flag in test metadata. The sandbox MUST inject a synthetic clock when this flag is
   present; failing to inject when declared is a sandbox configuration error, not a
   test failure.
5. Define what constitutes Q5 evidence in the nomination_record qualification checklist:
   for a test with no time-sensitive assertions — `clock_stub_required: false`, evidence:
   "no wall-clock assertions in test body". For a test with time-sensitive assertions —
   `clock_stub_required: true`, evidence: "clock_stub_required flag declared; synthetic
   clock injection verified in sandbox config at nomination time."
6. Resolve OQ-V9: should Q5 be validated at runtime by structural inspection of the
   test's failure assertion message? Recommend: no — structural inspection of assertion
   messages is brittle and language-specific. Operator attestation in nomination_record
   with `clock_stub_required` flag is sufficient for v1.1.

At the end of the session, generate a Gap Session Summary Block:
GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged]
NEW TENSIONS SURFACED: [any cross-domain conflicts]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GS13 — Full Council (Final Session)
### Gaps: GAP-4, GAP-9, GAP-13, GAP-15, GAP-17, GAP-18, GAP-19, T15, OQ-SC3
### Skill: framework-council (all six specialists)
### Run last
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 13 of 13 — Full Framework Council

Context: This is the final gap resolution session for the LLM as Database framework
spec. The v1.1 integrated spec is the active baseline; GS1–GS12 are assumed complete.
This session produces: (a) three contingent path specs for GAP-4; (b) formal deferral
records for GAP-9 and GAP-15; (c) v2 outline blocks for GAP-13, GAP-17, GAP-18,
GAP-19, GAP-32; (d) T15 final disposition and Amendment A11; (e) OQ-SC3 resolution
or explicit deferral. None of these items can be fully closed through spec work alone.

─── GAP-4 ───────────────────────────────────────────────────────────────────
Domain(s): Orchestration Comparativist
Priority: High — externally blocked by operator path selection

Three orchestration paths operator-decided (D72): Path A (LangGraph), Path B
(Claude Agent SDK), Path C (Hybrid). No recommendation in spec. Downstream:
(a) delegation token design is path-dependent, (b) HIL interface mechanism is
path-dependent.

Produces: Three conditional spec blocks — one per path, each marked "activates
on operator selection of Path [X]."

─── GAP-9 ───────────────────────────────────────────────────────────────────
Domain(s): Validation + MEMIT | Blocked by GAP-1

Behavioral probe generalization beyond code domains (OQ-W8). Cannot be specced
without GAP-1 empirical data. Action: confirm formal deferral; record deliverable.

─── GAP-13 ──────────────────────────────────────────────────────────────────
Domain(s): Warden + Orchestration

Genesis automation level (OQ-S5). v1 mandates human review before write engine
execution (§10.6 step 1). v2 target: secondary LLM reviewer as human-review proxy.
Produces: v2 outline block.

─── GAP-15 ──────────────────────────────────────────────────────────────────
Domain(s): Validation + MEMIT | Blocked by GAP-1

Compaction verification sampling thresholds (OQ-OC3). SUPPORTING/INCIDENTAL
sampling rates and abort thresholds provisional pending GAP-1. CORE threshold
(1.0, C-OC3) is non-provisional. Action: confirm formal deferral.

─── GAP-17 ──────────────────────────────────────────────────────────────────
Domain(s): Orchestration + State Consistency | v2-deferred (OQ-CW1)

Voluntary Write Lock release and inter-agent negotiation. No v1 mechanism.
Produces: v2 outline block.

─── GAP-18 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency | v2-deferred (OQ-SL2)

Multi-machine Ledger replication. Single-machine only in v1. The canonical archive
format `ledger-archive/v1` (D104/GS9) is single-machine. Produces: v2 outline block
that addresses how D104 interacts with replication (does the Merkle chain integrity
model scale, or does replication require a new integrity mechanism?).

─── GAP-19 ──────────────────────────────────────────────────────────────────
Domain(s): Warden | v2-deferred (scope extended GS4: OOK + CAK rotation)

OOK and CAK key rotation. GS5 v3 added §13.5 step 3a (CAK anchor semantic verification
at boot) and `ceremony_authorization_key_anchor` in Tier 1 genesis-seal.json (A10).
CAK rotation must account for: (a) how step 3a handles multiple historical
CAK_REGISTERED entries during rotation, (b) how CAK_COMPROMISED_AT_BOOT is cleared
during rotation, (c) interaction with OQ-S-CAK-2 (m-of-n CAK principals). Tier 1
is mint-once — rotation cannot simply update genesis-seal.json. Produces: v2 outline
block that is a dependency map.

─── T15 — CAK Availability vs. Ceremony Urgency ─────────────────────────────
Status: Partial — v1 mitigation documented; v2 resolution pending

v1 supports exactly one registered CAK anchor. "Backup custodian" = second person
with physical access to same CAK medium, not a second registered key. Amendment A11
(deployment guidance clarification) must be applied this session.

v2 resolution: OQ-S-CAK-1 (rotation ceremony accounting for mint-once Tier 1
interaction) + OQ-S-CAK-2 (m-of-n CAK principals). Both are GAP-19 v2 outline
block content.

─── OQ-SC3 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency + MEMIT (GS9 carry-forward)
Priority: Medium

Reconciliation workflow for STALE Layer 4 facts. Once Pruning Agent external_source_
audit sub-routine detects EXTERNAL_PROVENANCE_STALE: the fact remains in .vindex with
an advisory flag (D101). Whether a Coder Agent may auto-propose a refresh patch or
whether operator approval is required first before any write is issued is unspecified.
Options: (a) Coder Agent may auto-propose, routes through standard pipeline (no special
authorization); (b) operator must explicitly flag the fact for refresh before Coder Agent
is dispatched; (c) refresh proposals require a distinct STALE_FACT_REFRESH_REQUESTED
ceremony type in the CeremonyToken model. Decide and record.

─── GAP-27 (Tier conflict resolution) ───────────────────────────────────────
Domain(s): Warden + State Consistency Theorist
Priority: Conflict requires resolution

v3 GS7 placed `scope_update_min_interval_seconds` at Tier 1 (mint-once, not tunable).
v2 GS7 placed it at Tier 3 Anchored Git Config (tunable via `rate-limits.json`).
Tier 3 is architecturally sounder — rate limits should be operator-tunable post-bootstrap;
Tier 1 mint-once is inappropriate for an operational threshold. This session selects the
authoritative placement. Also confirm the dual-layer rate limit model from v2 GS7
(per-ceremony-initiator primary + per-affected-agent-id secondary) vs. v3 GS7's per-agent-id
only model. Recommendation: adopt v2 GS7's dual-layer model and Tier 3 placement.

─── GAP-48 ──────────────────────────────────────────────────────────────────
Domain(s): MEMIT Specialist
Priority: Medium — Source: v2 GS8

Probe set versioning for ε calibration. The `larql_fidelity_calibration` protocol (D-GS8-A,
v2 GS8) references "the canonical probe set defined at Genesis." If the probe set evolves
across Genesis updates, historical ε values lose comparability. A probe-set versioning contract
is needed: when the probe set changes, prior ε values are tagged inapplicable to the new set.
Related to GAP-1 (empirical calibration), T13 (M threshold provisional).

─── GAP-49 ──────────────────────────────────────────────────────────────────
Domain(s): Validation Contract Architect + MEMIT Specialist
Priority: Medium — Source: v2 GS10

Self-referential probing. When the judge model used in `judge_model_classification` probes is
itself subject to `.vindex` writes from the harness, probe outcomes may drift silently as the
judge model's state changes. No mechanism isolates judge-model state from the write stream it
verifies. Options: (a) pin judge-model version at probe template authorship time; (b) use a
separate frozen judge-model instance; (c) include judge-model state hash in CompactionProbeReport.
Related to GAP-9 resolution (v2 GS10 probe protocol).

─── GAP-50 ──────────────────────────────────────────────────────────────────
Domain(s): Validation Contract Architect
Priority: Medium — Source: v2 GS10

TGA skill-profile divergence. v2 GS10 assigned probe template authorship (three sub-types)
to the TGA alongside executable test generation. Whether a single agent role can cover both
without quality degradation is unverified. Triage: (a) accept as design constraint (actor-critic
independence requires concentration); (b) split into TGA-Test and TGA-Probe as separate roles.

─── GAP-51 ──────────────────────────────────────────────────────────────────
Domain(s): State Consistency Theorist + MEMIT Specialist
Priority: Medium — Source: v2 GS10

Provenance record lifecycle for re-verified Layer 4 facts. When a Layer 4 external-sourced
fact is re-written after staleness detection, the relationship between original and successor
provenance records (extend, replace, or chain via `prior_provenance_id`) is specified
narratively in GS9 v3 but not formally. Related to GAP-11 (resolved), OQ-SC3.

Relevant context from v1.1 spec + completed sessions:

§12.3 — Three Path Options (D72)
"Path A — LangGraph alone. Path B — Claude Agent SDK alone. Path C — Hybrid.
No path recommended. 2PC TC and Merkle-chain State Ledger are custom components
regardless of path (D80)."

§15 — Review Pathways (two-queue model)
"Correctness Review Queue decisions: approve_as_is | reject | re_route_for_further_work.
Default on neglect: logged suspension.
Reconciliation Review Queue decisions: approve_patch | reject_patch | modify_patch |
defer_with_reason. Default on neglect: backlog signals escalate."

§10.6 — Genesis Security Protocol (D26)
"Human review of Architect Agent output patch before write engine execution (mandatory
in v1; OQ-S5 fully-automated variant is v2)."

§10.4 — Invocation Token (9 fields)
write_scope_hash, expected_yaml_hash, scope_lock_ref, signature (OOK-signed). All
token signatures are OOK-signed. Delegation tokens for nested sub-agents (Path B/C)
are v2-deferred but path-conditional contingent spec blocks must outline the shape.

§6 — Category 3: Deferred to v2
"Full PKI: OOK rotation, CAK rotation, multi-Orchestrator trust.
Delegation tokens for nested sub-agents (Path B/C nested cases).
Multi-machine Ledger replication and distributed consensus.
Voluntary Write Lock release (OQ-CW1). Genesis automation (OQ-S5)."

§10.5 — Orchestrator Signing Key (OOK)
"Generated at first boot. Key rotation is v2."
[GS5 v3 added §13.5 step 3a for CAK anchor; A10 added ceremony_authorization_key_
anchor to Tier 1 genesis-seal.json. CAK rotation must account for this addition.]

From GS9 v3 — External Provenance (D99–D102)
"D101: Three-state staleness FRESH/STALE/UNAVAILABLE; advisory-only. CORE facts raise
REQUIRES_HUMAN_REVIEW on first detection. D102: Pruning Agent external_source_audit
sub-routine. No auto-retract or auto-rewrite on source change."
[OQ-SC3: whether auto-proposal of refresh patch by Coder Agent is authorized or whether
operator approval must precede any write is unresolved.]

From T16 (tension map v4)
"Ceremony-Scope Narrowness vs. Operational Batching (Warden vs SCT). Warden: one-
authorization-one-ceremony. SCT: batch ceremony for N Holds is operationally viable.
v2 target; per-Hold path specced for v1."

Invoke the framework-council skill. Convene all six specialist voices.

For GAP-4 (Orchestration primary; Warden + SCT + MEMIT contribute per path):
1. Produce three conditional spec blocks — one per path — marked "activates on
   operator selection of Path [X]":
   Path A (LangGraph): subgraph delegation token shape; HIL decision-return within
     LangGraph concurrency; 2PC TC placement in LangGraph execution graph.
   Path B (Claude Agent SDK): nested sub-agent delegation token shape; HIL via SDK
     callback or interrupt; sub-agent write scope inheritance model.
   Path C (Hybrid): token handoff at LangGraph ↔ SDK boundary; HIL in mixed
     concurrency; scope inheritance when SDK sub-agent spawned from LangGraph node.
2. Per path: Warden defines trust boundary shape and where CeremonyToken verification
   happens. SCT defines 2PC TC placement and compaction scheduling trigger point.
   MEMIT defines any path-conditional write engine behavior.

For GAP-9: Confirm formal deferral (blocked by GAP-1, D-CRC-2). Record behavioral
probe generalization as implementation-phase deliverable.

For GAP-13 (Warden + Orchestration): v2 outline — what must v2 define about a secondary
LLM reviewer as Genesis human-review proxy? Minimum required properties. Trust level
relative to the CAK-anchored Warden model. Authorization: would the proxy require its
own agent YAML + Write Scope Definition? v1 constraint: Genesis authorization requires
a trusted non-Orchestrator party. v2 must not cross this boundary without a new council
session.

For GAP-15: Confirm formal deferral. CORE threshold 1.0 (C-OC3) is non-provisional and
remains authoritative regardless of GAP-1 outcome.

For GAP-17 (Orchestration + SCT): v2 outline — voluntary Write Lock release ceremony
requirements (Lock Registry atomicity; in-progress operation safety; distinguishable
from TTL auto-release in the Ledger). Inter-agent write region negotiation protocol
requirements. v1 consistency guarantees that the negotiation must preserve.

For GAP-18 (SCT): v2 outline — distributed Ledger consistency model requirements.
Specifically: does the Merkle-chain-lite model (D50) require modification for
replication, or can each replica run an independent chain with a reconciliation layer?
Leader-election requirements. `ledger-archive/v1` format (D104/GS9) interaction with
replication — does the archive format need versioning for distributed scenarios?

For GAP-19 (Warden): v2 outline — produce a dependency map. Every component that binds
on OOK or CAK anchor at boot or runtime. For each: what does a key rotation event
require from that component? Special focus: §13.5 step 3a (CAK boot verification added
GS5 v3); `ceremony_authorization_key_anchor` in Tier 1 (mint-once — rotation cannot
simply update genesis-seal.json; requires a new bootstrap or exceptional ceremony);
CAK_REGISTERED Ledger entries as the historical chain (how does rotation clear the
old anchor while preserving historical audit chain?).

For T15 (Warden + Orchestration): Apply Amendment A11 — add to deployment guidance:
"v1 supports exactly one registered CAK anchor in genesis-seal.json. A second
registered CAK is not a v1 capability. The backup custodian is a second person with
physical access to the same CAK medium, not a second registered key." Confirm T15
is accepted as 🔶 Partial with v2 resolution via OQ-S-CAK-1 + OQ-S-CAK-2 (both in
GAP-19 v2 outline). T16 (Ceremony-Scope Narrowness): accept as v2 concern (per-Hold
path specced and workable for v1); v2 outline note in GAP-32 context.

For OQ-SC3 (SCT + MEMIT): Choose disposition for stale Layer 4 fact reconciliation:
(a) Coder Agent auto-proposal via standard pipeline (advisory flag in query results
is sufficient operator signal), (b) operator-explicit refresh flag required first,
(c) new CeremonyToken ceremony_type: STALE_FACT_REFRESH_AUTHORIZATION required. Note
that D101 specifies no auto-retract or auto-rewrite — any resolution here applies to
the proposal phase, not the write phase.

For GAP-32 (v2 outline, Warden + SCT): Note that batch Genesis Hold release requires
T16 resolution in v2. v2 outline: batch ceremony must preserve individual Hold audit
trail (each Hold must have a distinct release record in the Ledger, even if CAK
signature covers all holds collectively).

At the end of the session, generate a Gap Session Summary Block:
GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged]
NEW TENSIONS SURFACED: [any cross-domain conflicts]
```

---

*Gap Session Starter Prompts v4.0 — GS10 through GS13 (4 sessions)*
*GS1–GS3 prompts: gap-session-starter-prompts.md*
*GS4 prompt: gap-session-starter-prompts-v2.md*
*GS5–GS9 prompts: gap-session-starter-prompts-v3.md*
*Sources: gap-backlog-v4.md · gap-session-schedule-v4.md · llm-as-database-v1_1-integrated-spec.md*
*All v1 and v3 gap session summaries*
