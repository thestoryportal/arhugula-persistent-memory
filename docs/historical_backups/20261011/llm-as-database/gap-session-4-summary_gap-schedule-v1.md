# Gap Session 4 Summary — Validation Contract Architect (GAP-8 Residual, GAP-10)

**Session type:** Gap resolution
**Primary skill:** validation-contract-architect
**Baseline spec:** v1.1 (GAP-8 core closed by D88 / IC-CORPUS-AUTH; residual OQ-V5 items and GAP-10 / OQ-V1 open)
**Session number:** 4 of 8 (gap schedule v3)

---

## Session scope

Closure of the two residual items from GAP-8 (authorship rotation under a mint-once Tier 1 field; cadence enforcement beyond the passive 90-day flag) and full closure of GAP-10 (runtime tagging of constitutional tests; qualification criteria; promotion ceremony from task-generated tests to the sealed constitutional suite).

The session produced four new Decisions (D89–D92), one new Constraint (C26), three new Interface Contracts (IC-CORPUS-ROSTER, IC-CORPUS-STALE, IC-CONST-PROMOTE), and amendments to two existing ICs (IC-CORPUS-AUTH, IC-SL9).

---

## GAPS RESOLVED

### GAP-8 (residual) — Corpus authorship rotation and cadence enforcement
*Status: fully resolved by D89, D90, C26, IC-CORPUS-ROSTER, and IC-CORPUS-STALE. GAP-8 is now closed in its entirety.*

**Rotation (D89).** The Tier 1 mint-once constraint and the need to rotate authorized authors over the project lifetime are not in contradiction — they were prematurely collapsed into a single field in v1.1. The resolution is indirection. Tier 1 holds only the **root authority** that may delegate authorship; Tier 2 holds the **live author roster** as an append-only delegation log. Rotation happens entirely within Tier 2 without violating the Tier 1 mint-once invariant. Existing v1.1 deployments that populated `corpus_author_identities` directly are migrated by treating that field as both the initial root authority set and the initial delegation set (one-time bootstrap).

**Cadence (D90, C26).** The 90-day staleness flag is a passive indicator that does not prevent Health Score degradation. Over 90 days of normal operation, the Meta-Validator fires roughly 12 times (weekly cadence) or more often (commit cadence) against the same held-out cases — the overfitting risk compounds silently. The skill's deployment-blocking classification rule applies: this cannot be deferred to operator policy because the first Meta-Validator run after the 90-day window would otherwise produce a meaningless score with no automated signal. C26 promotes cadence to a spec constraint and introduces a new Health Score state (`STALE_CORPUS`) that is distinct from both numeric scores and `NOT_COMPUTED`.

### GAP-10 — Constitutional test tagging and promotion ceremony
*Status: fully resolved by D91, D92, and IC-CONST-PROMOTE. OQ-V1 is closed.*

**Runtime tagging (D91).** The Validator distinguishes constitutional from task-generated tests via a three-layer defense: (1) path membership in the Tier 2 sealed `constitutional-suite/` artifact (primary trust boundary, enforced by corpus access token); (2) `test_type: "constitutional"` metadata declared in each test file (defense against mis-load if a non-constitutional test somehow lands in the path); (3) separate Validator invocation entry point that explicitly loads the constitutional suite versus the task test set. All three signals must agree. Disagreement (e.g., a test in `constitutional-suite/` without the metadata tag, or vice versa) aborts the run and logs `CONSTITUTIONAL_TAG_INCOHERENT`.

**Qualification criteria (D92, part 1).** Five criteria, all required for promotion eligibility: (1) asserts a framework-level invariant, not task-specific behavior; (2) passes against the most recent CANONICAL_SNAPSHOT in the State Ledger; (3) does not exercise task-specific code paths or runtime state; (4) authored by an identity holding an active delegation in the corpus author roster at nomination time; (5) deterministic — no randomness, no network, no unstubbed wall-clock dependencies.

**Promotion ceremony (D92, part 2).** Two-signature ceremony. Single-signature promotion is rejected: constitutional tests define Tier 3 classification behavior (C25), one of the strongest classifications in the spec, and a single compromised or mistaken author could otherwise inject weak tests into a trust-anchoring suite. The ceremony: nominator (any authenticated identity with delegation, or an operator) produces a nomination record; a second corpus author — distinct from the nominator — reviews against the five qualification criteria and either signs a `promotion-attestation` or rejects. On approval, the test file and its attestation are added to `constitutional-suite/` via the existing versioned additive directory pattern (same mechanism as meta-validator and meta-TGA corpus additions). Revocation requires a parallel two-signature ceremony and produces a revocation record; the test file itself is never deleted (append-only).

---

## GAPS PARTIALLY RESOLVED

None. Both targeted gaps close in full.

---

## GAPS DEFERRED

None in this session.

---

## Decisions (for integration into v1.2 spec)

**D89 — Corpus author authority model: Tier 1 anchor, Tier 2 delegation log.**
- Tier 1 genesis-seal.json field change: `corpus_author_identities` is deprecated and renamed to `corpus_root_authority` (mint-once). This field holds one or more identities that may issue delegations; a quorum policy (M-of-N) is permitted at mint time.
- Tier 2 artifact introduced: `corpus-author-roster/`. Same versioned additive directory pattern as other sealed corpus artifacts. Each entry is either a delegation or a revocation. Both entry types require signature by an identity in `corpus_root_authority` (or by the delegator, in the case of self-revocation).
- A corpus case submission is valid only if signed by an identity with an active (delegated, not-revoked) roster entry at the submission's `authorship_date`. Historical roster state is reconstructible from the append-only log.
- Migration: v1.1 deployments with `corpus_author_identities` populated use that set as both `corpus_root_authority` and the initial delegation batch (`roster-genesis` entry), preserving audit continuity.
- No agent identity may hold a delegation (reaffirms the v1.1 constraint; now enforced at delegation issuance rather than Tier 1 field content).

**D90 — Corpus cadence is a spec constraint, not operator policy.**
- The passive 90-day staleness flag is preserved but is no longer the only cadence signal.
- C26 defines a minimum refresh rate. Falling below the rate produces a new Health Score state: `STALE_CORPUS`.
- `STALE_CORPUS` is distinct from `NOT_COMPUTED` (below minimum viable 20 cases) and from numeric thresholds. Semantically: "the score could be computed, and it would be a number, but we are declining to report the number because the corpus has gone stale and any number we produced would be unreliable."
- On `STALE_CORPUS`: Validator continues to run (not suspended — this is a reliability-of-measurement issue, not a reliability-of-Validator issue), but a 14-day operator remediation window opens. If unremediated at 14 days, escalates to Validator suspension for human review.
- Rationale for promoting this out of operator policy: the skill's deployment-blocking classification rule — the first Meta-Validator run after staleness would produce a silently meaningless Health Score. That is a silent correctness gap in the first operational cycle of the component it governs.

**D91 — Constitutional test runtime tagging: three-layer defense-in-depth.**
- Layer 1 (primary): Tests in the Tier 2 sealed `constitutional-suite/` path are treated as constitutional. Access to this path is governed by the IC-SL7 corpus access token.
- Layer 2 (mis-load defense): Each test file MUST declare `test_type: "constitutional"` metadata. The Validator verifies the declaration matches the load path.
- Layer 3 (classification context): The Validator exposes two distinct invocation entry points (`run_constitutional_suite()` and `run_task_tests()`). The active invocation determines failure classification — C25 (Tier 3) applies only when the constitutional entry point is active.
- Incoherence (any two layers disagree) aborts the run and produces an OBSERVATION ledger entry `CONSTITUTIONAL_TAG_INCOHERENT` (sync), followed by a GOVERNANCE entry flagging the affected run_id as invalid.
- Task-generated tests carry `test_type: "task"` and run under the task entry point. Mismatched metadata in a task test (e.g., a task test tagged `"constitutional"`) aborts that test's classification, not the whole run.

**D92 — Constitutional qualification criteria and two-signature promotion ceremony.**
- *Qualification (five, all required):*
  - Asserts a framework-level invariant. Example (qualifies): "a `.larql` patch with a missing or malformed schema_version header is rejected by the L1 static check." Counter-example (does not qualify): "AuthService returns 401 on expired JWT."
  - Passes against the most recent `CANONICAL_SNAPSHOT` recorded in the State Ledger at nomination time.
  - Does not exercise task-specific code paths, persistent task state, or task-specific `.vindex` entries.
  - Authored by an identity holding an active delegation in the corpus-author-roster at the nomination's `authorship_date`.
  - Deterministic: no randomness (or seeded and declared), no network access, no unstubbed wall-clock dependencies.
- *Ceremony:*
  - A `nomination_record` is produced by the nominator: `{nomination_id, test_path, task_id_of_origin, qualification_checklist: [{criterion, status, evidence_ref}×5], nominator_identity, nomination_date, signature}`.
  - A second corpus author — MUST be distinct from the nominator — reviews and either signs a `promotion_attestation` or signs a `rejection_record`. Both are append-only.
  - On approval: the test file and its `promotion_attestation` are added to `constitutional-suite/` via the versioned additive directory pattern. Both files are covered by the same operator-signed manifest (IC-SL8).
  - Revocation: requires a parallel two-signature ceremony producing a `revocation_record`. The test file is never deleted; revoked tests are skipped by the constitutional entry point but remain in the sealed history.
- Rationale for two-signature (rather than single): constitutional tests define the meaning of a Tier 3 failure classification (C25). A single compromised or mistaken authorized identity could otherwise inject a weak or flawed test into the highest-stakes trust suite. The review step is independence; the attestation is the durable evidence.

---

## Constraints (for integration into v1.2 spec)

**C26 — Corpus cadence minimum.**
> Over any rolling 90-day window, the Meta-Validator corpus and the Meta-TGA corpus must each grow by at least `max(5 cases, 10% of the corpus size at window start)`. Corpora below this growth rate enter the `STALE_CORPUS` Health Score state. `STALE_CORPUS` does not suspend the Validator but triggers a 14-day operator remediation window; unremediated at 14 days escalates to `<85% threshold` suspension per §9.11.

---

## Interface Contracts

### IC-CORPUS-ROSTER — Root authority → Corpus-author roster  *[new, v1.2]*
- **From:** Identities in `corpus_root_authority` (Tier 1, mint-once)
- **To:** `corpus-author-roster/` (Tier 2, versioned additive, append-only)
- **What A exposes:** Signed delegation and revocation entries. Entry format: `{entry_id, entry_type ∈ {delegation, revocation}, subject_identity, issued_by (root authority identity), valid_from, valid_until (delegations only; ISO-8601 or "indefinite"), signature, prior_entry_hash}`.
- **Conditions:** Entries must chain by `prior_entry_hash` (tamper-evident log). Delegation subject must not be an agent identity — enforced at entry time, not at use time. Root authority quorum policy (if configured at mint) applies to every entry.
- **Failure behavior:** Invalid signature → `ROSTER_SIGNATURE_INVALID` (SECURITY, sync); entry rejected without being written. Broken hash chain → `ROSTER_CHAIN_BROKEN` (SECURITY, sync); suspends all corpus author lookups pending Warden investigation. Agent identity delegation attempt → `ROSTER_AGENT_DELEGATION_FORBIDDEN` (SECURITY, sync).

### IC-CORPUS-STALE — Corpus cadence monitor → Ledger / Validator scheduler  *[new, v1.2]*
- **From:** Corpus cadence monitor (runs at each Meta-Validator / Meta-TGA scheduling event)
- **To:** State Ledger (observation); Validator scheduler (state input)
- **What A exposes:** Cadence evaluation record: `{corpus_id, window_start, window_end, cases_added_in_window, corpus_size_at_window_start, threshold, status ∈ {HEALTHY, STALE_CORPUS, REMEDIATION_EXPIRED}, remediation_deadline}`. Status feeds directly into the Health Score computation for that run.
- **Conditions:** Evaluation at every Meta-* scheduling trigger. `STALE_CORPUS` status persists across runs until cadence threshold is met. `remediation_deadline = status_first_observed + 14 days`. REMEDIATION_EXPIRED triggers suspension via the <85% path in §9.11.
- **Failure behavior:** Monitor failure to read corpus state → `CORPUS_CADENCE_UNKNOWN` (OBSERVATION, sync). The Meta-* run proceeds but Health Score is downgraded to `NOT_COMPUTED` with reason `cadence_unknown` to prevent silent assumption of freshness.

### IC-CONST-PROMOTE — Task test → Constitutional suite promotion  *[new, v1.2]*
- **From:** Task test in task test corpus, nominated for constitutional promotion
- **To:** `constitutional-suite/` (Tier 2 sealed, versioned additive)
- **What A exposes:** Two-signature ceremony artifacts: `nomination_record` (nominator-signed), `promotion_attestation` (reviewer-signed, distinct identity), or `rejection_record` (reviewer-signed terminal state). On approval, the test file and attestation are added via the same sealed-corpus additive pattern covered by IC-SL8.
- **Conditions:** Nominator and reviewer must hold distinct active delegations at the time of their respective signatures (verified against IC-CORPUS-ROSTER). Qualification checklist must cover all five D92 criteria with evidence references. Attestation covers the test's current file hash — modifying the test after attestation invalidates the promotion and requires re-ceremony.
- **Failure behavior:** Nominator and reviewer identical → `PROMOTION_SELF_REVIEW_FORBIDDEN` (SECURITY, sync). Either signer lacks active delegation → `PROMOTION_SIGNER_UNAUTHORIZED` (SECURITY, sync). Qualification criterion evidence missing → `PROMOTION_QUALIFICATION_INCOMPLETE` (correctness, sync). Test file hash changed post-attestation → `PROMOTION_ATTESTATION_STALE` (SECURITY, sync); ceremony must be re-run against the new hash.

### IC-CORPUS-AUTH — *amended in v1.2*
- Amendment: references to `corpus_author_identities` are replaced by "any identity holding an active delegation in `corpus-author-roster/` per IC-CORPUS-ROSTER." The minimum viable corpus size (20 cases), case formats, and staleness flag remain unchanged from D88.
- The existing constraint "no agent identity MUST appear in `corpus_author_identities`" migrates to IC-CORPUS-ROSTER (delegation-time enforcement).

### IC-SL9 — *amended in v1.2*
- Amendment: per-case audit entries MUST include the delegation reference used to authorize each corpus case submission (`delegation_entry_id` field). This preserves audit completeness across the new indirection and is a non-negotiable extension per the skill's Warden-facing contract review gate. Aggregate-only reporting remains forbidden (C-META1 unchanged).
- Warden sign-off is required for this amendment at integration time. Flagged for Gap Session 5 or the v1.2 integration checkpoint.

---

## NEW GAPS SURFACED

**G-S4-N1 — Roster reload semantics during long-running Meta-* evaluations.**
A Meta-Validator run may span wall-clock minutes or hours. If a roster entry (delegation or revocation) is added to `corpus-author-roster/` mid-run, does the run use the roster state at token issuance (IC-SL7) or the live roster? Token-issuance semantics are simpler and consistent with the token being time-bounded, but a revocation during a run that then includes cases submitted by the revoked identity is a security-relevant edge case. Recommend token-issuance semantics with an explicit exclusion list mechanism for emergency mid-run revocation. Routes to Warden.
*Priority: Medium. Blocks nothing structural but affects the revocation threat model.*

**G-S4-N2 — Root authority quorum policy update path.**
D89 permits an M-of-N quorum at mint time for `corpus_root_authority`. But if the M-of-N policy itself needs updating (e.g., N authorities becomes N-1 because one leaves the org permanently), there is no mechanism. This is a deeper version of the original GAP-8 contradiction — one level up. Options: (a) accept it as genuinely mint-once (project must be re-bootstrapped if root authority composition changes); (b) define an exceptional ceremony; (c) make root authority itself a two-tier structure (which becomes turtles-all-the-way-down).
*Priority: Low. Unlikely to trigger within a single project lifetime if the initial quorum is chosen wisely. Recommend accepting (a) for v1.2 and documenting as a known design limitation.*

**G-S4-N3 — Constitutional test deterministic-clock dependency.**
D92 criterion 5 disallows "unstubbed wall-clock dependencies" but does not define what a stubbed wall-clock looks like for the Validator sandbox. The sandbox spec (existing) defines reproducibility but does not specify a clock injection mechanism. If a constitutional test asserts timing behavior (e.g., "cadence monitor transitions to STALE_CORPUS when 90 days elapse without addition"), it needs a testable clock abstraction. Routes to Validation Contract Architect (this skill) for a follow-up sandbox-spec refinement in Gap Session 5 or later.
*Priority: Medium. Blocks the ability to write constitutional tests for any time-sensitive framework invariant — which includes C26 itself.*

**G-S4-N4 — v1.1→v1.2 migration path for existing Tier 1 configurations.**
D89 describes migration as "treat existing `corpus_author_identities` as both root authority and initial delegation batch." This is a spec-side instruction but does not define the mechanical migration record — is there a one-time genesis-delta entry in the State Ledger? Does the migration itself require a ceremony, or is it a declarative spec-upgrade rule applied automatically at v1.2 adoption? Routes to State Consistency Theorist.
*Priority: Low-Medium. Structurally clean but needs a concrete migration-record format before v1.2 deployment.*

---

## NEW TENSIONS SURFACED

**T-S4-1: Warden / Validation Contract — Audit completeness under roster indirection.**
The IC-SL9 amendment adds `delegation_entry_id` to per-case audit entries. This is necessary for audit completeness under the new indirection, but it expands the per-case audit payload and creates a secondary audit object (the roster entry itself) that the Warden must now also treat as audit-relevant. The tension: does audit completeness now require the Warden to audit the roster's append-only log on the same cadence as corpus manifest verification? Recommend yes, but this extends the Warden's per-access verification scope. Flagged for resolution at v1.2 integration.

**T-S4-2: State Consistency / Validation Contract — Roster state at snapshot boundaries.**
The `corpus-author-roster/` is Tier 2 sealed and append-only. But the State Ledger tracks CANONICAL_SNAPSHOTs that bundle model state and Git state. Does a snapshot also bind the roster state? If a rollback to an earlier CANONICAL_SNAPSHOT occurs, does the roster also roll back (reverting recent delegations/revocations), or is the roster snapshot-invariant because it is append-only? Recommend snapshot-invariant with rationale: the roster is an authorization log, not a system state; rolling back authorization records would undo legitimate revocations and reintroduce compromised identities. This preserves security monotonicity across rollbacks. Flagged for State Consistency Theorist review.

**T-S4-3: Orchestration / Validation Contract — Two-signature ceremony latency.**
D92's promotion ceremony requires two distinct human signatures for every constitutional promotion. This creates a real throughput bottleneck as the constitutional suite grows: every promotion requires coordination between two authorized humans. The alternative — batch promotions where one reviewer signs off on N nominations simultaneously — reduces latency but weakens the per-test independence of the review. Flagged for Orchestration Comparativist: does the orchestration layer need a ceremony-coordination primitive (e.g., a nomination queue and review workflow), or is ceremony coordination out of orchestration scope?

---

## Gap Session Summary Block

**GAPS RESOLVED:**
- GAP-8 (residual) — Corpus authorship rotation (D89, IC-CORPUS-ROSTER) and cadence enforcement (D90, C26, IC-CORPUS-STALE). GAP-8 is now fully closed.
- GAP-10 — Constitutional test runtime tagging (D91), qualification criteria and two-signature promotion ceremony (D92, IC-CONST-PROMOTE). OQ-V1 closed.

**GAPS PARTIALLY RESOLVED:** None.

**GAPS DEFERRED:** None in this session.

**NEW GAPS SURFACED:**
- G-S4-N1 — Roster reload semantics during long-running Meta-* evaluations (Medium; routes to Warden).
- G-S4-N2 — Root authority quorum policy update path (Low; recommend acceptance as a mint-once limitation).
- G-S4-N3 — Constitutional test deterministic-clock dependency and sandbox clock injection spec (Medium; routes to Validation Contract Architect, future session).
- G-S4-N4 — v1.1→v1.2 migration record format for existing Tier 1 corpus author configurations (Low-Medium; routes to State Consistency Theorist).

**NEW TENSIONS SURFACED:**
- T-S4-1 (Warden / Validation Contract) — Roster log as audit object; extends Warden per-access verification scope.
- T-S4-2 (State Consistency / Validation Contract) — Roster snapshot-binding under rollback; recommended snapshot-invariant to preserve security monotonicity.
- T-S4-3 (Orchestration / Validation Contract) — Ceremony coordination primitive needed in orchestration layer, or out of scope?

**Integration notes for v1.2:**
- Four decisions (D89–D92), one constraint (C26), three new ICs (IC-CORPUS-ROSTER, IC-CORPUS-STALE, IC-CONST-PROMOTE), two IC amendments (IC-CORPUS-AUTH, IC-SL9).
- IC-SL9 amendment requires Warden sign-off at v1.2 integration per the skill's Warden-facing contract review gate — it touches the audit trail payload.
- Three new tensions to be surfaced in cross-domain review; none is blocking for v1.2 drafting but all should be resolved before v1.2 is sealed.
