# Gap Session 9 — Summary (Validation Ratification Pass)

**Framework:** LLM as Database — Agent Harness Architecture
**Session type:** Ratification + residual-OQ closure pass
**Primary voice:** Validation Contract Architect
**Targets:** GAP-8 (corpus authorship policy), GAP-10 (constitutional test classification)
**Baseline:** v1.1 integrated spec + GS8 resolutions (D93–D98)
**Status on exit:** GAP-8 and GAP-10 confirmed closed; two of three residual OQs resolved (OQ-V7, OQ-V9); OQ-V8 formally deferred to v2 with explicit rationale; one new minor OQ surfaced; no new cross-domain tensions

---

## 0. Scope Reconciliation

The prompt scopes this session to GAP-8 and GAP-10. Both were the declared targets of GS8 under the v3 schedule and were substantially resolved in `gap-session-8-summary_gap-schedule-v3.md` via D93–D98. The v3 schedule's GS9 separately covers GAP-11/12/14/28 and already exists as `gap-session-9-summary_gap-schedule-v3.md`.

This session is therefore filed as a **validation ratification pass** rather than a new resolution session. Its two functions:

1. Ratify D93–D98 against the Validation Contract Architect skill's spec output checklist.
2. Close the three residual OQs GS8 surfaced (OQ-V7, OQ-V8, OQ-V9).

Downstream integrators (framework-spec-writer, v1.2 assembly) should treat this document as a ratification addendum to GS8, not a supersession. Decision IDs D93–D98 retain their GS8 provenance. New decisions in this session are D99–D100.

---

## 1. Ratification of GS8 Decisions Against Validation Skill Checklist

Applied against the Spec Output Checklist at the foot of the Validation Contract Architect skill:

| Checklist item                                            | GS8 coverage                                    | Status |
|-----------------------------------------------------------|-------------------------------------------------|--------|
| Test suite authorship defined                             | D93 registry + IC-CORPUS-AUTH enforced role     | ✅ Ratified |
| `.larql` schema version header resolution                 | Out of GS8 scope (owned elsewhere)              | — N/A |
| Behavioral consistency validation approach                | Out of GS8 scope (owned elsewhere)              | — N/A |
| Verbal feedback format specified                          | Out of GS8 scope (owned elsewhere)              | — N/A |
| Maximum retry count defined                               | Out of GS8 scope (owned elsewhere)              | — N/A |
| Failure handling path defined                             | Out of GS8 scope (owned elsewhere)              | — N/A |
| Validator reliability assessment mechanism                | Meta-Validator cadence tiers D94 + D95 markers  | ✅ Ratified |
| Coverage gap risk acknowledged and mitigated              | D94 180-day floor prevents silent drift         | ✅ Ratified |
| Adversarial case risk acknowledged                        | D96 dual-signal cross-check (forgery requires two artifacts) | ✅ Ratified |
| ICs with MEMIT / Warden / SCT / Orchestration defined     | IC-CORPUS-REG1/2, IC-CORPUS-CADENCE1, IC-CONSTITUTIONAL-1/2 | ✅ Ratified |
| Warden-facing contract review gate (skill pre-close rule) | GS8 reuses IC-SL9 per-case audit posture; no move to aggregate | ✅ Ratified |
| Deployment-blocking classification applied                | D95 five preconditions, two hard blocks + three degraded-run markers | ✅ Ratified |

**Finding:** All checklist items within GS8's stated scope are covered to spec quality. No ratification-blocking gaps in D93–D98. The corpus-governance cluster (D93/D94/D95) and the constitutional-classification cluster (D96/D97/D98) are internally coherent and externally non-conflicting with Warden, SCT, MEMIT, and Graph Data Architect domains.

**No revisions proposed.** D93–D98 stand as v1.2-candidate baseline.

---

## 2. Closing Residual OQs

### 2.1 OQ-V7 — Registry Identity Expiry Enforcement

**Question (from GS8):** The `corpus-author-registry/` record format admits an optional `expires_at` field per D93. Where is expiry checked? What happens to in-flight Meta-* tokens issued before expiry crosses?

**Resolution — Decision D99:** Two-point expiry enforcement with no mid-run revocation.

Expiry is checked at exactly two enforcement points:

1. **Corpus case submission ingress (Warden side).** When an author submits a new corpus case, the Warden verifies that the submitting identity's `expires_at` is either absent or strictly greater than `now()`. An expired author cannot submit. This is the authoritative enforcement surface for future-case admission.

2. **Meta-* token issuance (IC-SL7 side).** When the Transaction Controller requests an IC-SL7 corpus-access token for a scheduled Meta-* run, the Corpus Seal Registry verifies that every author whose cases are in the active corpus version either has no `expires_at` or has not yet crossed it. If any author has expired *and* their cases are still in the active version, the token is still issued — but the `IC-SL7` response carries a `contains_expired_author_cases: true` flag and the Meta-* run proceeds in an advisory posture (Health Score computed but flagged `EXPIRED_AUTHOR_PRESENT` in the Ledger).

**In-flight token policy:** Tokens already issued before an expiry crossing remain valid for their declared `valid_until`. Mid-run revocation is explicitly rejected — destabilizing an active Meta-* run on an expiry tick creates worse failure modes than letting it complete with the flag set. If operators need emergency removal of an author's influence, they (a) author a new registry version with the identity removed or expired, (b) separately raise a circuit break on the affected Meta-* scheduler via the standard Tier 3 circuit-breaker path. These are two distinct ceremonies, not a single fused action.

**What this implies for the Ledger:** One new advisory flag on the existing Meta-* result record (`EXPIRED_AUTHOR_PRESENT`). No new Ledger entry type. Additive, low-surface change.

**Rationale against alternatives considered:**
- *Immediate mid-run revocation:* rejected — race between expiry tick and Meta-* completion produces half-computed Health Scores, which is a worse audit artifact than a flagged completed score.
- *Scrub expired authors' cases from the active corpus version automatically:* rejected — violates the Tier 2 versioned-additive-only rule; case removal is a human-review operation, not a background sweep.

**OQ-V7 → Resolved (D99).**

---

### 2.2 OQ-V8 — Cadence Differentiation Between Meta-Validator and Meta-TGA Corpora

**Question (from GS8):** D94's cadence floor (90-day advisory, 180-day `HEALTH_SCORE_STALE`) applies uniformly to both Meta-Validator and Meta-TGA corpora. If empirical operation shows the two drift at different rates, should cadence differ?

**Resolution:** Explicitly deferred to v2. OQ-V8 remains open but is reclassified from "open question" to "post-deployment monitoring item" with a defined signal that would trigger reopening.

**Why not resolve now at v1.2:**

1. **No empirical basis.** The framework has not run. Any differentiated cadence numeric chosen now is a guess about relative drift rates between Validator FFN behavior and TGA test-authorship behavior. Either drift could dominate, and over-specification in advance risks locking in a wrong ratio.
2. **Unified cadence is the conservative v1 posture.** If the two corpora drift at different rates, the faster-drifting one still gets its staleness enforced at the 180-day floor. The slower-drifting one is over-maintained — a cost to operators, not a correctness cost. Symmetric over-maintenance is cheaper than asymmetric under-maintenance.
3. **Differentiated cadence would be a Tier 3 operator-tunable surface.** Introducing it before there is data to tune against creates a configuration point that cannot be defaulted well.

**Reopening signal (recorded for v2 roadmap):** Open OQ-V8 for reconsideration if, in any rolling 12-month post-deployment window, one of the two corpora accumulates a `HEALTH_SCORE_STALE` rate at least 3× that of the other. At that threshold, differentiated cadence is demonstrably warranted and empirical data exists to tune it.

**Recorded in v2 roadmap (§19).** No v1.2 spec change.

**OQ-V8 → Deferred to v2 with explicit reopening signal (not a spec decision, a recorded policy).**

---

### 2.3 OQ-V9 — Runtime Structural Validation of Q5 (Documented Failure Mapping)

**Question (from GS8):** D97's Q5 qualification criterion requires that a constitutional test document, in its failure assertion message, which invariant is being violated. GS8 accepted Q5 as operator attestation only. Should the Validator structurally verify at runtime that the assertion message actually identifies the claimed invariant?

**Resolution — Decision D100:** Introduce a **weak structural check** — a Ledger-logged co-record, not a blocking verification.

Structural verification of natural-language assertion messages against a claimed `invariant_statement` field is brittle when attempted as a blocking gate: either the parser is too strict and legitimate failures are rejected, or it is too lenient and the check provides no actual signal. Neither failure mode is acceptable for a Tier 3 classification path (where false blocks would halt the Reflexion loop on a formatting nit and false passes would erase the check's value).

**The weak-check pattern:**

1. When a constitutional test fails, the Validator emits an existing Ledger entry of type `CONSTITUTIONAL_FAILURE` (already defined in Appendix C batch A7b) with a new field pair:
   - `invariant_statement` — copied from the test's metadata (authoritative)
   - `failure_assertion_message` — captured verbatim from the test's runtime output
2. **The Validator does NOT block on mismatch.** The Tier 3 classification proceeds per C25 regardless of whether the two strings align.
3. An operator-facing audit query (operator-owned tooling, not spec-mandated code) can surface cases where the strings diverge for human review. Over time, this query's output becomes a signal that Q5 is being honored or eroded at the authoring stage.

**Why this resolves OQ-V9:** The question was whether runtime structural validation is warranted. The answer is: runtime **blocking** validation is not warranted (brittle, low-signal), but runtime **logging** of the two strings for later audit is cheap, additive, and preserves exactly the audit trail that operators would need to detect Q5 degradation. This converts a runtime enforcement question into an audit-visibility answer.

**What this implies for other domains:**
- **Warden:** None. The new field pair is on an existing Ledger entry type.
- **State Consistency Theorist:** Additive Ledger field. Merkle-chain-lite integrity unaffected.
- **Graph Data Architect:** None.
- **MEMIT:** None.
- **Orchestration:** None.

**What this does NOT do:** It does not elevate Q5 from operator attestation to structural gate. If a future version wants to make Q5 enforceable, the logged co-record is the data substrate that would enable writing a blocking check in v2 — but v1.2 does not do that.

**OQ-V9 → Resolved (D100).**

---

## 3. Cross-Domain Tension Check

| Domain                       | Tension surfaced?                                                                 |
|------------------------------|------------------------------------------------------------------------------------|
| Warden                       | No — D99 expiry check uses existing submission ingress and existing IC-SL7 token issuance path. Additive predicate. D100 adds field pair to existing Ledger entry type. |
| State Consistency Theorist   | No — D99 adds one advisory flag value to an existing Ledger record; D100 adds two fields to an existing Ledger entry type. Both strictly additive. |
| MEMIT Specialist             | No — no write engine surface touched.                                             |
| Graph Data Architect         | No — schema untouched.                                                            |
| Orchestration Comparativist  | No — no dispatch-path change; D99's `EXPIRED_AUTHOR_PRESENT` is equivalent to the existing warning-tier posture for TC scheduling, treated identically. |
| Validation Contract          | Owned — resolved here.                                                            |

No new cross-domain conflicts surfaced.

---

## 4. Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-8** — Confirmed closed. GS8's D93 (Tier 2 `corpus-author-registry/` + Tier 1 narrowed to `corpus_author_bootstrap_identity`), D94 (90/180-day cadence tiers), and D95 (five Day-0 deployment preconditions) ratified against the Validation Contract Architect spec output checklist without revision. D99 (this session) closes the residual registry-expiry enforcement question.
- **GAP-10** — Confirmed closed. GS8's D96 (dual-signal directory + module marker tagging), D97 (five qualification criteria Q1–Q5), and D98 (standard Tier 2 versioned additive promotion ceremony with qualification attestation block) ratified without revision. D100 (this session) closes the residual Q5 runtime-validation question via the weak-check pattern.

**GAPS PARTIALLY RESOLVED:**
- None.

**GAPS DEFERRED:**
- None from GS8 closed scope. OQ-V8 (a GS8-surfaced OQ, not a GAP) deferred to v2 with an explicit reopening signal (§2.2).

**NEW GAPS SURFACED:**
- **OQ-V10** — The weak-check pattern introduced in D100 assumes operator tooling will be written to query the Ledger for `invariant_statement` vs. `failure_assertion_message` divergences. The spec does not mandate that this tooling exist — it is an operator-owned convenience. If an operator never writes this query, Q5 degradation is logged but never observed. Whether the spec should mandate a minimum audit-query suite (distinct from the constitutional test suite) is an open question. Low priority; parallel to OQ-V9's original framing about audit visibility.

**NEW TENSIONS SURFACED:**
- None. Cross-domain check clean (see §3).

**NEW DECISIONS (for v1.2 spec update):**
- **D99** — Corpus author registry expiry enforced at submission ingress and at Meta-* token issuance only. No mid-run revocation. In-flight runs with expired-author cases complete with `EXPIRED_AUTHOR_PRESENT` flag on the existing Meta-* Ledger result record.
- **D100** — Q5 (constitutional test failure mapping) validated via weak-check pattern: `CONSTITUTIONAL_FAILURE` Ledger entry gains paired fields `invariant_statement` and `failure_assertion_message`; no runtime block on mismatch; operator audit query surfaces divergences for review.

**NEW CONSTRAINTS:**
- **C-CORPUS-EXP1** — Expired author identity MUST NOT be accepted at corpus case submission ingress.
- **C-CORPUS-EXP2** — Meta-* runs encountering expired-author cases in the active corpus version MUST complete with the `EXPIRED_AUTHOR_PRESENT` flag and MUST NOT be revoked mid-run.
- **C-CONSTITUTIONAL-Q5** — `CONSTITUTIONAL_FAILURE` Ledger entry MUST include both `invariant_statement` (from test metadata) and `failure_assertion_message` (captured verbatim from runtime).

**NEW INTERFACE CONTRACTS:**
- No new top-level ICs required. D99 extends IC-CORPUS-AUTH (submission ingress expiry predicate) and IC-SL7 (token issuance flag propagation) by additive amendment. D100 extends the `CONSTITUTIONAL_FAILURE` Ledger entry schema by field addition. Amendment entries:
  - **A12-IC-CORPUS-AUTH** — Add `expires_at` predicate at submission ingress.
  - **A13-IC-SL7** — Add `contains_expired_author_cases` response field and `EXPIRED_AUTHOR_PRESENT` advisory flag propagation to Meta-* Ledger result record.
  - **A14-AppendixC-CONSTITUTIONAL_FAILURE** — Add `invariant_statement` and `failure_assertion_message` field pair to `CONSTITUTIONAL_FAILURE` Ledger entry type.

**AMENDMENT OBLIGATIONS (v1.2 integration):**

| Ref | Section | Amendment | Status |
|-----|---------|-----------|--------|
| A12 | IC-CORPUS-AUTH | Submission-ingress expiry predicate (D99) | Outstanding |
| A13 | IC-SL7 + Meta-* result record | Expiry-flag propagation (D99) | Outstanding |
| A14 | Appendix C `CONSTITUTIONAL_FAILURE` | Q5 weak-check field pair (D100) | Outstanding |

**v2 ROADMAP ADDITIONS:**
- OQ-V8 reopening signal recorded: 3× differential `HEALTH_SCORE_STALE` rate over 12-month rolling window between Meta-Validator and Meta-TGA corpora.
- OQ-V10 evaluation: whether a minimum operator audit-query suite should be spec-mandated.
- Per D100's closing note: if Q5 promotion from weak-check to blocking-gate becomes desirable, the Ledger field pair from A14 is the data substrate.

---

**Session exit posture:** GAP-8 and GAP-10 confirmed closed. Three residual OQs from GS8 addressed — two resolved (OQ-V7 via D99; OQ-V9 via D100), one deferred to v2 with explicit reopening signal (OQ-V8). One new low-priority OQ surfaced (OQ-V10). No cross-domain tensions. Three additive amendments queued for v1.2 integration. Ready for absorption.
