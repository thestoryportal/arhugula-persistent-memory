# Gap Session 2 Summary — State Consistency Theorist

**Session:** Gap Session 2 of 8
**Skill invoked:** `state-consistency-theorist`
**Scope:** Verify closures of GAP-6 (D84, IC-TC-RESET) and GAP-7 (D85, IC-TC-TIMEOUT) in v1.1 integrated spec
**Baseline:** `llm-as-database-v1_1-integrated-spec.md`

---

## 1. Verification of D84 / GAP-6 (Circuit Breaker Reset)

### 1.1 READ_ONLY mode definition — ✅ sufficient with one seam

§11.8.1 and §12.4 Consistency Status API cover:
- Automatic entry on trip (no human action required for READ_ONLY itself).
- Clear permitted operations: inference, query, read. Clear suspended operation: write token issuance.
- Exit is **binary** — CIRCUIT_TRIPPED → WRITE_ENABLED via signed ceremony. No intermediate partial-write state. This answers GAP-6's partial-resume question (it is binary, by policy) and the binary choice is correct: anything finer-grained would create a second trust surface during a known-compromised state.

**Residual seam — in-flight tokens at trip moment:**
The spec defines *future* token issuance as suspended, but does not define the fate of tokens already admitted through the Gate (`TOKEN_CONSUMED` written) but not yet arrived at PREPARED. Three possibilities, none currently selected:
- (a) in-flight tokens proceed to their natural outcome (PREPARED or abort),
- (b) in-flight tokens are force-abandoned (`TOKEN_ABANDONED` emitted on trip),
- (c) in-flight tokens proceed to PREPARED but cannot advance to COMMITTED.

This is flagged as NEW-GAP-SC-1 below. It is a narrow-window consistency question, but the window is exactly when the system is deciding it cannot be trusted, so "undefined" is unsafe.

### 1.2 TC precondition verification coverage — ✅ covers stated trip types; two edge cases unspecced

Per trip type:
| Trip type | Required precondition | Covered? |
|---|---|---|
| `CONSECUTIVE_FAILURE` | compensation COMPLETED + overlay hash = latest COMMITTED | ✅ |
| `CROSS_TASK_FAILURE` | same as above | ✅ |
| `DIVERGED_STATE` | `RECONCILIATION_COMPLETE` with `result: CONSISTENT`, timestamped after trip | ✅ |

**Edge cases not covered:**
- **Precondition verification infrastructure failure.** If the TC cannot read the Ledger during precondition checking (e.g., archived epoch not yet mounted, WAL replay required, integrity check in flight), what is the default? Safest assumed behavior is "refuse reset and log `CIRCUIT_RESET_REJECTED` with reason `PRECONDITION_CHECK_UNAVAILABLE`" but this is not explicit in the spec. → NEW-GAP-SC-2.
- **Rate limiting on failed reset attempts.** `CIRCUIT_RESET_REJECTED` is catalogued (Appendix C, SECURITY) but there is no rate-limit or escalation rule if an operator submits repeated bad resets. Not dangerous (signature verification blocks forgery) but creates a Ledger-noise attack surface. → NEW-GAP-SC-3 (low priority).

### 1.3 CIRCUIT_RESET Ledger entry placement — ✅ correctly catalogued, one consistency seam

Placement verified:
- Appendix C: listed under GOVERNANCE category with fields `target_trip_entry_id`, `operator_id`, `preconditions_verified` (line 1358). ✅
- §16.3 synchronous entry list includes `CIRCUIT_TRIPPED`, `CIRCUIT_RESET`, `CIRCUIT_RESET_REJECTED`. ✅
- §16.2 writer model: Transaction Controller is listed under W1 (Orchestrator-mediated). §11.8.1 explicitly excludes the W3 emergency path from reset authority. ✅

**Consistency seam — W1 write during CIRCUIT_TRIPPED:**
The CIRCUIT_RESET entry is a W1 (Orchestrator-mediated) write. But at the moment of writing, the system is in CIRCUIT_TRIPPED / READ_ONLY, which §11.8.1 defines as "write token issuance is suspended." The CIRCUIT_RESET is not issued through a write token — it is a governance-ceremony ledger write — but the spec does not explicitly carve out "governance writes are exempt from write suspension." Without that carve-out, the exit mechanism is definitionally blocked by the state it is meant to exit.

This is almost certainly an intended-but-unstated invariant. Making it explicit would close the seam: write-suspension applies to application writes mediated by tokens; governance-category ceremony writes (CIRCUIT_RESET, RETENTION_OVERRIDE_EXTENDED, and similar) proceed through W1 regardless of CIRCUIT_TRIPPED state. → NEW-GAP-SC-4.

---

## 2. Verification of D85 / GAP-7 (PREPARED-state Timeout)

### 2.1 Two-value timeout model handles the original Genesis scenario — ✅

The original GAP-7 example: a Genesis compile of up to 10,000 edges (sub-batched at 2,000) could exceed 2 hours. The two-value model resolves this cleanly:
- `incremental_prepared_timeout` (default 2h) applies to all non-Genesis transactions.
- `genesis_prepared_timeout` has **no default** and is Gate-blocked (C-GATE-2) until operator-set. This forces the operator to make a deliberate, measurement-informed choice before Genesis initiation — which is the right forcing function for a non-restartable event.

### 2.2 Internal consistency of the incremental-vs-Genesis asymmetry — ✅

Incremental timeout: TC Phase 1 rollback, Hold persists, retry as fresh-token infrastructure failure.
Genesis timeout: circuit trips (DIVERGED_STATE), no auto-compensation, forensic evidence preserved.

The asymmetry is **justified by the restart-ability property**:
- Incremental patches are idempotent at the task level — a retry with a fresh token produces the same validated patch and the same 2PC semantics. Auto-compensation plus retry is safe.
- Genesis is a one-shot bootstrap. Partial-compile state cannot be cleanly composed with a second attempt without first verifying the pre-Genesis IMMUTABLE_ANCHOR baseline is intact. Tripping the breaker and demanding an operator integrity check is the correct conservative posture.

§11.5.1 makes the additional requirement explicit: "Operator MUST run full model integrity check against the pre-Genesis `IMMUTABLE_ANCHOR` baseline before the reset ceremony may proceed." This ties the Genesis recovery path to the IMMUTABLE_ANCHOR seal laid in §4.3 — correct and internally consistent.

### 2.3 Hold persistence through timeout — ✅ policy stated, but missing Ledger entry type

§11.5.1 and §17.3 both establish:
- Hold MUST NOT auto-release on PREPARED timeout.
- Hold is released only via (a) successful commit on retry, or (b) **operator-signed Hold release (GOVERNANCE category, signed ceremony)**.

The operator-signed release path is a distinct ceremony with distinct trust properties from an ordinary lifecycle release. But Appendix C only lists:

> **LIFECYCLE:** `DEPENDENCY_HOLD_PLACED`, `_RENEWED`, `_RELEASED`, `_EXPIRED_UNCLAIMED`

There is no GOVERNANCE-category entry for the signed release. This is the explicit question raised in the prompt, and the answer is **yes — Appendix C needs a new entry.** This is NEW-GAP-SC-5 (high priority; spec block drafted below).

---

## 3. New Spec Block — Signed Hold Release Ledger Entry

### DEPENDENCY_HOLD_RELEASED_SIGNED — Spec Block  ⚑ WARDEN CO-REVIEW

**What it must guarantee:**
- A Dependency Hold released by operator ceremony produces a Ledger entry categorically distinct from a Hold released by successful commit or automatic expiry.
- The entry carries operator identity, signature, and the justification reason so Warden audit surfaces can distinguish routine lifecycle releases from governance-ceremony releases.

**Valid states:**
- Hold in `ACTIVE` state (placed or renewed), task in `AWAITING_OPERATOR_RETRY`, `repeated_timeout`, or other escalation state where retry is not producing resolution.

**Invalid states (failure modes):**
- Signed release submitted for a Hold that does not exist → reject, log `CIRCUIT_RESET_REJECTED`-equivalent security entry (requires naming; see Open questions).
- Signed release submitted for a Hold on a task with a live PREPARED transaction → reject. Governance release must not race commit.
- Signature verification failure → reject, log under SECURITY category.

**Transaction boundary:**
- Single Ledger write, synchronous. Not a 2PC — the Hold registry is Orchestrator-owned state (§12.4), not Git+`.vindex` joint state.

**Recovery behavior:**
- If the Ledger write succeeds but the Orchestrator's Hold registry update fails: reconciliation on next Orchestrator start reconstructs registry from Ledger (existing §17 pattern extended). The Ledger is authoritative.

**Open questions (unresolved):**
- Entry name: `DEPENDENCY_HOLD_RELEASED_SIGNED` vs. `HOLD_RELEASED_SIGNED` vs. a field extension on existing `DEPENDENCY_HOLD_RELEASED`. Spec recommendation: distinct name in GOVERNANCE category, because the audit category tag is the primary cross-category filter and conflating a LIFECYCLE and GOVERNANCE release behind the same type name forces query-time category inference from a fields blob.
- Rejection entry name if a signed release targets a non-existent or conflicting Hold.
- Whether repeated signed releases in a short window should produce a Ledger-level pattern flag analogous to `CONTENT_SPLIT_LOOP`.

**Interface contract:**

```
IC-HOLD-SIGNED-RELEASE — Human Operator → Orchestrator → Ledger
  From: Human Operator (signed ceremony)
  To: Orchestrator (Hold registry update) + Ledger (entry emission)
  What A exposes: Signed release token containing:
    { hold_id, task_id, release_reason, operator_id, signature }
  Orchestrator verifies signature and Hold existence, then:
    [1] Writes DEPENDENCY_HOLD_RELEASED_SIGNED (GOVERNANCE, sync, W1):
        { hold_id, task_id, release_reason, operator_id,
          signature_verification_result, prior_hold_state }
    [2] Marks Hold as released in the §12.4 Scope Lock and Hold Registry.
  Conditions: Ceremony only valid when Hold is in ACTIVE or AWAITING_RETRY
    state. Ceremony is rejected if a PREPARED transaction referencing the
    held edges is currently in flight.
  Failure behavior: Signature invalid → rejection entry under SECURITY.
    Hold not found → rejection entry. Race with PREPARED → rejection entry
    with reason PREPARED_IN_FLIGHT; operator retries after TC resolves.

Before this IC is closed, the Warden must confirm:
  - Whether DEPENDENCY_HOLD_RELEASED_SIGNED attestation must include a
    reference to the originating PREPARED timeout that created the
    persistence condition (evidentiary linkage requirement).
  - Whether rate limits or cooldowns apply to repeated signed releases
    per operator identity within an audit window.
  - Whether the signed release ceremony requires multi-operator
    co-signature (two-person rule) for Holds older than N days or
    across escalation-class tasks.
```

---

## 4. Summary of Residual Seams in D84/D85 (not blocking closure)

| # | Seam | Severity | Resolution path |
|---|---|---|---|
| 1 | In-flight token fate at trip moment | Medium | Add sentence to §11.8.1 naming one of three options |
| 2 | Precondition check infrastructure failure default | Medium | Add rejection reason `PRECONDITION_CHECK_UNAVAILABLE` to IC-TC-RESET failure behavior |
| 3 | Rate limiting on repeated `CIRCUIT_RESET_REJECTED` | Low | Warden policy, not a consistency concern |
| 4 | Governance-write carve-out during CIRCUIT_TRIPPED | Medium | Add one line to §11.8.1: "governance-category W1 writes proceed during CIRCUIT_TRIPPED; token-mediated writes do not" |
| 5 | Missing `DEPENDENCY_HOLD_RELEASED_SIGNED` entry | **High** | Adopt spec block in §3 above |

---

## Gap Session 2 Summary Block

**GAPS RESOLVED:**
- **GAP-6** — Circuit breaker reset authority. D84 + IC-TC-RESET close the gap. READ_ONLY is automatic on trip; write resumption requires signed operator ceremony with TC-independent precondition verification (different preconditions per trip type); reset emits `CIRCUIT_RESET` (GOVERNANCE, sync, W1); W3 path excluded. Partial-resume question is answered as binary by policy. Minor seams identified below as new gaps; closure itself holds.
- **GAP-7** — PREPARED-state timeout. D85 + IC-TC-TIMEOUT close the gap via a two-value model. The Genesis 10,000-edge scenario from the original gap description is handled: `genesis_prepared_timeout` is operator-set and Gate-blocked (C-GATE-2) until present. The incremental-vs-Genesis asymmetry (rollback+retry vs. circuit trip + forensic preservation) is internally consistent and justified by Genesis's non-restartability. Hold persistence policy through timeout is stated; the missing Ledger entry for the operator-signed release path is surfaced as a new gap, but the underlying policy in D85 is sound.

**GAPS PARTIALLY RESOLVED:** None.

**GAPS DEFERRED:** None in this session.

**NEW GAPS SURFACED:**
- **NEW-GAP-SC-1** — In-flight token fate at circuit-breaker trip. Tokens consumed but not yet PREPARED at the trip moment have undefined disposition. Priority: Medium.
- **NEW-GAP-SC-2** — Precondition verification infrastructure-failure default in IC-TC-RESET. If the TC cannot read the Ledger to verify preconditions, the fail-closed behavior is not stated explicitly. Priority: Medium.
- **NEW-GAP-SC-3** — Rate limiting / escalation on repeated `CIRCUIT_RESET_REJECTED` attempts. Ledger-noise attack surface with no defined cap. Priority: Low.
- **NEW-GAP-SC-4** — Governance-write carve-out during CIRCUIT_TRIPPED. The CIRCUIT_RESET write itself is a W1 write occurring while "write token issuance is suspended"; the exemption is implied but not stated. Priority: Medium.
- **NEW-GAP-SC-5** — `DEPENDENCY_HOLD_RELEASED_SIGNED` Ledger entry missing from Appendix C. Operator-signed Hold release ceremony (§17.3, GOVERNANCE) has no distinct entry type; only LIFECYCLE `DEPENDENCY_HOLD_RELEASED` exists. Spec block drafted above. Priority: **High** (addresses the explicit question in the session prompt).

**NEW TENSIONS SURFACED:**
- **T-NEW-SC-W-1 — Audit category vs. lifecycle event for Hold release (State Consistency ↔ Warden).** The signed release is simultaneously a lifecycle transition (registry-level Hold state change) and a governance ceremony (signed, audit-traceable operator action). Which category tag wins is a Warden-owned decision, but the consistency model wants one canonical authoritative entry per transition. Resolution via the spec block in §3 requires Warden co-review.
- **T-NEW-SC-W-2 — Write suspension scope vs. governance-ceremony write path (State Consistency ↔ Warden).** CIRCUIT_TRIPPED suspends "write token issuance," but the CIRCUIT_RESET entry that exits the tripped state is a W1 ledger write issued while in that very state. Whether "write suspension" means "token-mediated application writes only" or "all W1 writes" is the underlying policy question — consistency model needs the governance exemption, Warden owns the rule.

**INTERFACE CONTRACTS DEFINED THIS SESSION:**
- `IC-HOLD-SIGNED-RELEASE` — draft, pending Warden co-review (see spec block, §3).

**CARRY-FORWARD FOR NEXT SESSION:**
NEW-GAP-SC-5 should be resolved in the next Warden or cross-domain gap session to close Appendix C completeness. NEW-GAP-SC-1 and NEW-GAP-SC-4 are small textual additions to §11.8.1 that could be batched into the next integration pass. NEW-GAP-SC-2 is a one-line addition to IC-TC-RESET failure behavior.
