# Gap Session 8 — Summary

**Framework:** LLM as Database — Agent Harness Architecture
**Session type:** Gap resolution session
**Primary voice:** Validation Contract Architect
**Targets:** GAP-8 (corpus authorship policy), GAP-10 (constitutional test classification)
**Baseline:** v1.1 integrated spec as updated by GS1–GS7
**Status on exit:** Both gaps fully resolved; two deployment-blocking preconditions specified; one new minor OQ surfaced

---

## 0. Framing

Both gaps are deployment-blocking under the rule stated in the Validation Contract
Architect skill: if corpus authorship is unresolved before the first 50 commits,
the first Health Score is meaningless; if constitutional tests cannot be
distinguished at runtime, C25 (Tier 3 classification) cannot be enforced. Neither
question reduces to "operator policy." Both require spec-level resolution with
operational preconditions attached.

The Tier 2 versioned-additive-directory pattern (operator-signed manifest, `v1/`,
`v2/`, ...`vN/`, secondary copy in Genesis Vault) is already load-bearing for five
corpora in v1.1 §13.3. GS8 reuses that pattern for both resolutions rather than
inventing new machinery.

---

## 1. GAP-8 Resolution — Corpus Authorship Policy

### 1.1 Tier 1 / Tier 2 Contradiction Resolution

**Decision D93:** Adopt option (a) from the gap brief.

`corpus_author_identities` is removed from Tier 1 as a live author list and
re-sited as a new Tier 2 sealed artifact: `corpus-author-registry/`. Tier 1 retains
a strictly narrower field, `corpus_author_bootstrap_identity`, which is a single
operator identity authorized to sign the first `corpus-author-registry/v1/manifest.json`
and nothing else.

**Why option (a) over alternatives:**
- The Tier 2 versioned additive pattern is already load-bearing. A sixth corpus of
  this shape costs no new governance machinery.
- The `corpus-author-bootstrap-identity` field in Tier 1 is mint-once by nature —
  it only authorizes the first registry manifest. Subsequent registry versions are
  signed by identities listed in the registry itself (or by the bootstrap identity
  acting in its operator capacity, indistinguishably from other operators).
- Trust boundary: the Warden already governs Tier 2 manifest verification via the
  Sealed Corpus pattern. No new Warden work.

**Governance model for `corpus-author-registry/`:**

| Field                     | Value                                                        |
|---------------------------|--------------------------------------------------------------|
| Location                  | `<harness_root>/.sealed-corpora/corpus-author-registry/`     |
| Write model               | Versioned additive directories (`v1/`, `v2/`, …)             |
| Manifest signer (v1)      | `corpus_author_bootstrap_identity` (Tier 1)                  |
| Manifest signer (v2+)     | Any identity marked `registry_signer: true` in v(n-1) active |
| Record format per entry   | `{ identity_id, public_key_ref, role ∈ {author, registry_signer}, added_date, added_by, expires_at? }` |
| Agent identity forbidden  | Yes — per C-GOC4, strictly enforced at manifest validation   |
| Secondary copy            | Genesis Vault, per Tier 2 pattern                            |
| Minimum active authors    | 1                                                            |
| Read access               | Warden (for IC-SL7 / IC-SL8 authorization); Meta-* scheduler |

### 1.2 Extension Cadence Decision

**Decision D94:** Two-tier cadence, parallel to Meta-* Health Score thresholds.

The existing 90-day staleness flag is retained as advisory. A new hard cadence
floor is added: if no new case has been added to a Meta-* corpus for **180 days**
and a Meta-* run fires against that corpus, the run returns `HEALTH_SCORE_STALE`
(distinct from `NOT_COMPUTED`). The prior Health Score is surfaced but flagged as
non-authoritative. Validator/TGA suspension is **not** automatic at the 180-day
floor — the operator must act — but TC treats `HEALTH_SCORE_STALE` as equivalent
to a warning-tier Health Score for scheduling purposes (no new high-risk tasks
dispatched until cadence restored).

Cadence table:

| Age since last case | Flag state              | Meta-* Health Score result |
|---------------------|-------------------------|----------------------------|
| < 90 days           | `FRESH`                 | Computed normally          |
| 90–179 days         | `STALENESS_WARNING`     | Computed; flagged advisory |
| ≥ 180 days          | `STALE`                 | `HEALTH_SCORE_STALE`       |

**Rationale for the 180-day floor:**
- 90-day advisory alone has no enforcement surface. An operator who never looks
  at the flag produces Health Scores that drift into irrelevance silently.
- 180 days is approximately six Meta-Validator cycles at weekly cadence or three
  at 50-commit cadence — long enough that a "we'll get to it" deferral doesn't
  immediately cause operational friction, short enough that corpus drift against
  an evolving Validator does not accumulate undetected.
- The suspension ladder (fresh → warning → stale) mirrors the Health Score
  ladder (≥95 → 85–94 → <85) structurally, which keeps operator mental model
  consistent across corpus state and Validator state.

### 1.3 Corpus Initialization Guidance — Deployment Preconditions

**Decision D95:** The following five preconditions must be met before the first
Meta-Validator or Meta-TGA trigger fires (i.e. before commit 50 or the first
weekly cadence, whichever first). These are labelled **deployment-blocking** per
the Validation Contract Architect skill rule — they are not operator-owned
policy because their absence renders the first operational cycle meaningless.

| # | Precondition                                                                                 | Consequence if absent at first trigger      |
|---|----------------------------------------------------------------------------------------------|---------------------------------------------|
| 1 | `corpus_author_bootstrap_identity` present in `genesis-seal.json`                            | Genesis initiation blocked (C-GATE-2 style) |
| 2 | `corpus-author-registry/v1/` populated, manifest signed by bootstrap identity                | First Meta-* → corpus access unauthorized   |
| 3 | `meta-validator-suite/v1/` contains ≥ 20 cases signed by registry authors                    | `HEALTH_SCORE_NOT_COMPUTED` (audit-only)    |
| 4 | `meta-tga-corpus/v1/` contains ≥ 20 cases signed by registry authors                         | `HEALTH_SCORE_NOT_COMPUTED` (audit-only)    |
| 5 | `constitutional-suite/v1/` present with ≥ 1 signed test (see §2 / GAP-10)                    | Validator L4 constitutional gate inactive   |

Preconditions 1–2 are **hard blocks** — the harness will not issue write tokens
or dispatch the first Meta-* schedule without them. Preconditions 3–5 are
**degraded-run markers** — the harness proceeds but operates in a measurably
weaker state that is explicitly announced in the State Ledger.

**Ledger announcement requirement:** At Genesis initiation, the Transaction
Controller writes a `CORPUS_INIT_STATE` entry to the State Ledger recording
which of the five preconditions are met and which are in degraded state. This
entry is the audit trail of the harness's Day-0 validation posture.

### 1.4 Spec Block — `corpus-author-registry/`

```
### corpus-author-registry (Tier 2 sealed corpus) — Spec Block

What it must prove:
- The identity submitting a Meta-* corpus case is currently authorized as a
  corpus author at the time of submission.
- Authorization is derivable from a human-signed, versioned artifact, not from
  any runtime agent or service.

What it explicitly does NOT prove:
- The semantic quality of the cases those authors submit (covered by corpus
  review process — operator-owned, not spec-owned).
- That an author is still trustworthy after they are added (rotation / removal
  handled by authoring new registry versions — see 1.1 governance table).

Input contract:
- Registry v1 manifest signed by `corpus_author_bootstrap_identity` (Tier 1).
- Registry vN (N ≥ 2) manifest signed by any identity with role
  `registry_signer` active in v(N−1).

Output contract:
- Warden / Meta-* scheduler can resolve "is identity X authorized to author
  corpus cases at time T" deterministically by walking the registry versions up
  to the active manifest at time T.

Failure behavior:
- Manifest signature invalid → `SEALED_CORPUS_INTEGRITY_FAIL` (per existing
  IC-SL7 / IC-SL8 machinery).
- No active registry version (v1 never signed) → Meta-* runs blocked; preconditions
  1–2 unmet; Ledger entry `CORPUS_INIT_STATE` records hard block.
- Agent identity appears in any version → manifest validation rejects version
  (C-GOC4, enforced at verification time, not author time).

Exit criteria:
- First registry version exists and is signed → corpus author resolution is
  deterministic and auditable. No further exit — registry is permanent.

Open questions (deferred):
- Multi-operator quorum for registry signing (deferred to v2, already in §19
  roadmap as "Multi-operator (quorum) Tier 2 signing").
- Identity expiry semantics: the record format includes optional `expires_at`
  but the expiry enforcement path is not yet specced. Surfaced as new OQ-V7.

Interface contract:

IC-CORPUS-REG1 — Registry → Warden: author resolution  [new, T8]
  From: corpus-author-registry (active version)
  To: Warden authorization path (feeds IC-CORPUS-AUTH)
  What A exposes: Deterministic "authorized-at-time-T" resolution for any
    identity_id. Verification walks manifest signatures from v1 to active vN.
  Conditions: Manifest chain integrity must be intact (no gaps, no unsigned
    intermediate version). All signers for v(N+1) must have role
    `registry_signer` active in vN.
  Failure behavior: Any broken link in chain → SEALED_CORPUS_INTEGRITY_FAIL.

IC-CORPUS-REG2 — Registry bootstrap → Genesis  [new, T8]
  From: genesis-seal.json.corpus_author_bootstrap_identity
  To: corpus-author-registry/v1/manifest.json signature slot
  What A exposes: Exactly one identity authorized to sign registry v1 and
    nothing else. Consumed exactly once; subsequent registry versions sign
    themselves through IC-CORPUS-REG1.
  Conditions: Bootstrap identity's public key recorded in Tier 1; no agent
    identity permitted (C-GOC4).
```

### 1.5 Spec Block — Extension Cadence

```
### Meta-* Corpus Extension Cadence — Spec Block

What it must enforce:
- Meta-* Health Scores produced against corpora that have not received new
  cases within 180 days are flagged as non-authoritative.
- The advisory 90-day staleness signal is retained and surfaces in operator
  tooling.

Hard constraints:
- C-CORPUS-CADENCE1: `staleness_state` is computed per corpus at every Meta-*
  run from `days_since_last_case_added`, derived from the highest
  `authorship_date` in the active corpus version.
- C-CORPUS-CADENCE2: `HEALTH_SCORE_STALE` is a distinct state from both
  `HEALTH_SCORE_NOT_COMPUTED` and a numeric score. All three must be
  distinguishable in the State Ledger record (IC-V-TGA2, IC-SL9).
- C-CORPUS-CADENCE3: TC treats `HEALTH_SCORE_STALE` as equivalent to a
  warning-tier Health Score for dispatch gating. No automatic suspension.

Tradeoffs decided:
- Chose two-tier (90 advisory / 180 enforced) over single-tier mandatory
  refresh. Rationale: operator autonomy preserved for low-activity periods
  where case additions are genuinely not needed, while an enforced floor
  prevents silent drift.
- Chose corpus-age as the signal rather than corpus-churn (e.g. "at least
  one new case per 100 commits"). Rationale: wall-clock age captures model
  drift and task-distribution drift, which is the actual correctness concern.

Open questions (deferred):
- Whether cadence tiers should vary between Meta-Validator and Meta-TGA
  corpora. v1.1 treats them identically. Surfaced as new OQ-V8.

Interface contract:

IC-CORPUS-CADENCE1 — Cadence computation → Meta-* run result  [new, T8]
  From: Meta-* scheduler at token issuance time (reuses IC-SL7 path)
  To: Meta-* run result record
  What A exposes: staleness_state ∈ {FRESH, STALENESS_WARNING, STALE}
    computed from registry and corpus contents at run scheduling time.
  Conditions: Computation is deterministic from sealed corpus state; no
    runtime agent input.
  Failure behavior: Computation failure (unable to read corpus manifest)
    → SEALED_CORPUS_INTEGRITY_FAIL (existing error code).
```

---

## 2. GAP-10 Resolution — Constitutional Test Classification

### 2.1 Runtime Tagging Mechanism

**Decision D96:** Defense-in-depth, dual-signal tagging. Both signals are
required; either one missing rejects the test at Validator suite-construction
time (before any test runs).

**Signal 1 (structural):** Tests in the active `constitutional-suite/vN/`
directory (as selected by the manifest's `active_version` field) are enumerated
by the Validator at suite construction. Every enumerated test receives
`origin: CONSTITUTIONAL` in the Validator's internal test registry.

**Signal 2 (declarative):** Every test file under `constitutional-suite/vN/`
MUST declare a module-level marker `__constitutional__ = True` alongside an
`__invariant__` string giving the asserted architectural invariant in one
sentence.

**Cross-check:** At suite construction, the Validator verifies for each test:
- Test is under `constitutional-suite/<active_version>/` (Signal 1 present)
- Module carries `__constitutional__ = True` (Signal 2 present)
- Module carries non-empty `__invariant__` string (Signal 2 well-formed)

Any asymmetry (present in directory but missing marker, or marker present but
outside directory) → suite construction fails with `CONSTITUTIONAL_SUITE_MALFORMED`.
This is an `UNRECOVERABLE` failure in the sense of the Reflexion loop — the
Validator does not run any tests until operators correct the suite.

**Task-generated tests (TGA output):** carry `origin: TGA` and are enumerated from
the TGA Stub Probe output path, never from any sealed corpus. A TGA-produced test
cannot structurally appear in `constitutional-suite/vN/` because TGA is an agent
and C-GOC4 forbids agent-authored sealed corpus cases.

### 2.2 Constitutional Qualification Criteria

**Decision D97:** Five objective criteria. A test must satisfy all five to be
eligible for promotion. The criteria are check-listable so that a second
operator reviewing a promoted test can verify compliance mechanically.

| # | Criterion             | What it rules out                                        |
|---|-----------------------|----------------------------------------------------------|
| Q1| Invariant scope       | Task-specific assertions (must be harness-wide property) |
| Q2| Fixture determinism   | Network calls, uncontrolled filesystem, agent invocation |
| Q3| Compaction stability  | Tests that examine ephemeral per-run state               |
| Q4| Schema-version binding| Tests that silently assume a single frozen schema version — either the test is schema-agnostic, or it declares `__applicable_versions__` |
| Q5| Documented failure mapping | Tests whose failure message doesn't identify the violated invariant |

**Examples of tests that qualify:**
- Every committed `.larql` patch carries a non-empty `larql_syntax_version`.
- No agent identity appears in any Tier 2 manifest signer list.
- The Write Engine's circuit breaker opens within the TC-specified window of
  `drift_tier = CRITICAL`.
- Meta-Validator returns `NOT_COMPUTED`, never a numeric score, when its
  active corpus has fewer than 20 cases.
- The Gate rejects any patch with `CONTENT_CLASSIFICATION = mixed`.

**Examples of tests that do NOT qualify:**
- "The `AuthService` module correctly validates JWT tokens" (Q1 fail —
  task-specific).
- "The Coder Agent returns within 30 seconds on this prompt" (Q2 fail —
  runtime behavior dependent on context state).
- "The knowledge graph contains an edge for `UserService`" (Q3 fail — state
  that changes per compaction).

### 2.3 Promotion Ceremony

**Decision D98:** Direct operator addition via the standard Tier 2
versioned-additive-directory pattern. No separate nomination step in v1.1.

**Procedure:**
1. Operator drafts new test file with `__constitutional__`, `__invariant__`,
   and `__applicable_versions__` (if Q4-bound) markers.
2. Operator writes a new version directory
   `constitutional-suite/v(N+1)/` containing the superset of v(N) plus the new
   test(s).
3. Operator writes `v(N+1)/manifest.json` including for each newly added test a
   **qualification attestation block**:
   ```
   {
     "test_id": "…",
     "invariant_statement": "…",
     "qualification_criteria_met": ["Q1", "Q2", "Q3", "Q4", "Q5"],
     "promoter_identity": "…",
     "promotion_date": "…"
   }
   ```
4. Operator signs the manifest with an operator key already authorized for
   `constitutional-suite/` signing (per existing Tier 2 pattern).
5. The Warden verifies the manifest signature and, at next Validator
   persistent-read refresh, the new version becomes active.

**Minimum bar for v1.1:** Single operator signature suffices. This matches the
rest of the Tier 2 pattern. Multi-operator quorum for constitutional promotion
is deferred to v2 (already in §19 roadmap). This intentionally accepts that a
single operator can promote — the qualification attestation provides the audit
trail, and the criteria are objective enough for post-hoc review.

**Demotion / removal:** Constitutional suite is permanent-additive, same as
other Tier 2 corpora. A test cannot be removed; if an operator believes a
promoted test was miscategorized, the path is to publish a new version that
marks the test as `__deprecated__ = True` with an attestation block explaining
why. The Validator continues running deprecated tests but the results are
advisory, not Tier 3. This preserves the audit history.

### 2.4 Spec Block — Constitutional Suite Classification

```
### Constitutional Test Suite — Classification & Promotion Spec Block

What it must prove:
- Every test the Validator treats as constitutional (i.e. whose failure maps
  to Tier 3 regardless of surface appearance, per C25) is verifiably the
  result of an operator promotion ceremony.
- Runtime classification is deterministic and does not depend on agent
  judgment, heuristics, or file content inspection beyond declared markers.

What it explicitly does NOT prove:
- That a promoted test actually tests the invariant it claims to (Q5 is
  operator attestation, not runtime verification).
- That the set of promoted tests is complete — no mechanism guarantees every
  invariant has a constitutional test covering it.

Input contract:
- Active `constitutional-suite/vN/` directory with signed manifest.
- Each test file in that directory declares `__constitutional__`,
  `__invariant__`, optional `__applicable_versions__`, optional `__deprecated__`.

Output contract:
- Validator's test registry at run time contains, for every constitutional
  test: `origin: CONSTITUTIONAL`, `invariant_statement`, `deprecated: bool`.
- Failures of non-deprecated constitutional tests are classified Tier 3 (C25).
- Failures of deprecated constitutional tests are advisory and do not trigger
  Tier 3 classification.

Failure behavior:
- Dual-signal mismatch (directory presence without marker, or vice versa):
  CONSTITUTIONAL_SUITE_MALFORMED — Validator halts before running any tests
  until operators fix.
- Missing qualification attestation in manifest for a newly added test:
  MANIFEST_ATTESTATION_INCOMPLETE — version rejected at Warden verification.

Exit criteria:
- Suite construction succeeds when every test under the active version passes
  both signals and every test in the manifest has a well-formed attestation
  block. No other exit.

Open questions (deferred):
- Whether a separate operator-quorum promotion path is required for
  constitutional suite specifically, given the elevated trust implications
  (Tier 3 classification bypasses retry tiers 1–2). Single-operator is the
  v1.1 position; v2 roadmap carries multi-operator Tier 2 signing which
  naturally extends to this case. Surfaced as confirmed, not new OQ.
- Whether Q5 ("documented failure mapping") should be validated at runtime
  by structural inspection of the test's failure assertion message. v1.1
  treats this as operator attestation only. Surfaced as new OQ-V9.

Interface contract:

IC-CONSTITUTIONAL-1 — Suite construction → Validator run  [new, T8]
  From: Validator suite-construction phase (reads constitutional-suite/vN/)
  To: Validator run phase
  What A exposes: Test registry with `origin: CONSTITUTIONAL` tags and
    invariant strings for every qualifying test.
  Conditions: Dual-signal cross-check passes for every test; manifest
    attestation blocks well-formed.
  Failure behavior: CONSTITUTIONAL_SUITE_MALFORMED (UNRECOVERABLE) or
    MANIFEST_ATTESTATION_INCOMPLETE (halts at Warden verification step).

IC-CONSTITUTIONAL-2 — Tier 3 classification  [confirms C25]
  From: Validator run result with `origin: CONSTITUTIONAL` test failure
  To: Reflexion loop dispatcher
  What A exposes: Failed constitutional test → Tier 3 classification
    regardless of surface error appearance (C25), unless test is marked
    `__deprecated__ = True` in which case failure is advisory.
  Conditions: Constitutional origin tag present and verified.
```

---

## 3. Cross-Domain Tension Check

| Domain                    | Tension surfaced?                                                                 |
|---------------------------|------------------------------------------------------------------------------------|
| Warden                    | No — resolutions reuse Sealed Corpus pattern Warden already governs. D93's new bootstrap field in Tier 1 is the narrowest possible Tier 1 extension (single identity, single-use). |
| State Consistency Theorist| No — `HEALTH_SCORE_STALE` is a new Ledger record value, additive. IC-SL9 extends naturally. |
| MEMIT Specialist          | No — no write engine surface is touched.                                          |
| Graph Data Architect      | No — schema untouched.                                                            |
| Orchestration Comparativist| Low-surface — TC dispatch gating gains one new input state (`HEALTH_SCORE_STALE` → warning-tier equivalent). Additive, no orchestration pattern changes. |
| Validation Contract       | Owned — resolved here.                                                            |

No new cross-domain conflicts surfaced.

---

## 4. Gap Session Summary Block

**GAPS RESOLVED:**
- **GAP-8** — Corpus authorship policy fully specced. Tier 1 contradiction
  resolved via D93 (Tier 2 `corpus-author-registry/` + Tier 1
  `corpus_author_bootstrap_identity`). Extension cadence specified via D94
  (90-day advisory / 180-day enforcement). Corpus initialization defined as
  five deployment preconditions (D95), two hard blocks and three
  degraded-run markers, with `CORPUS_INIT_STATE` Ledger record at Genesis.
- **GAP-10** — Constitutional test classification fully specced. Dual-signal
  runtime tagging via D96 (directory placement + module markers, both
  required). Five qualification criteria (Q1–Q5) via D97. Promotion ceremony
  via D98 (standard Tier 2 versioned additive pattern with qualification
  attestation block in manifest). Single-operator signing accepted for v1.1;
  multi-operator quorum deferred to v2 per §19 roadmap.

**GAPS PARTIALLY RESOLVED:**
- None.

**GAPS DEFERRED:**
- None from the GS8 scope. Both target gaps resolved in full.

**NEW GAPS SURFACED:**
- **OQ-V7** — Registry identity expiry enforcement. The `corpus-author-registry/`
  record format admits an optional `expires_at` field per D93, but the expiry
  enforcement path (where expiry is checked, what happens to in-flight Meta-*
  tokens issued before expiry crosses) is not specified in v1.1. Low priority;
  can live as an open question until a use case emerges.
- **OQ-V8** — Cadence tier differentiation between Meta-Validator and Meta-TGA
  corpora. v1.1 treats both cadence tiers identically (D94). If empirical
  operation shows the two corpora drift at different rates, differentiated
  cadence may be warranted. Low priority; monitor post-deployment.
- **OQ-V9** — Runtime structural validation of Q5 (documented failure mapping).
  v1.1 treats Q5 as operator attestation; no runtime check that a failing
  constitutional test's assertion message actually identifies the violated
  invariant. Could be tightened in v2. Low priority.

**NEW TENSIONS SURFACED:**
- None. Cross-domain check clean (see §3).

**NEW DECISIONS (for v1.2 / v1.1+ spec update):**
- D93 — `corpus_author_identities` relocated from Tier 1 to Tier 2 `corpus-author-registry/`; Tier 1 narrowed to `corpus_author_bootstrap_identity` (single-use).
- D94 — Meta-* corpus extension cadence: 90-day advisory / 180-day enforced (`HEALTH_SCORE_STALE`).
- D95 — Five Day-0 deployment preconditions for corpus initialization, with `CORPUS_INIT_STATE` Ledger entry.
- D96 — Dual-signal constitutional test tagging (directory + module markers).
- D97 — Five qualification criteria (Q1–Q5) for constitutional test promotion.
- D98 — Constitutional test promotion via standard Tier 2 versioned additive pattern, single-operator signature in v1.1, with in-manifest qualification attestation block.

**NEW CONSTRAINTS:**
- C-CORPUS-CADENCE1, C-CORPUS-CADENCE2, C-CORPUS-CADENCE3 (cadence computation and TC dispatch gating).
- C-CONSTITUTIONAL-DUAL (dual-signal requirement for constitutional test classification — asymmetry is an UNRECOVERABLE failure).

**NEW INTERFACE CONTRACTS:**
- IC-CORPUS-REG1 — Registry author resolution → Warden.
- IC-CORPUS-REG2 — Tier 1 bootstrap identity → registry v1 signature slot.
- IC-CORPUS-CADENCE1 — Staleness computation → Meta-* run result.
- IC-CONSTITUTIONAL-1 — Suite construction → Validator run (dual-signal check).
- IC-CONSTITUTIONAL-2 — Tier 3 classification confirmation (reinforces C25).

**ARTIFACT INVENTORY UPDATE — §13.3 Sealed Corpora table gains one row:**

| `corpus-author-registry/` | Authorized corpus author list | Warden read (authorization path); Meta-* scheduler read | 1 active author | Permanent additive versioning |

Tier 2 sealed corpora count: **6** (was 5 in v1.1).

---

**Session exit posture:** Both deployment-blocking gaps closed with concrete
spec language. Three minor open questions surfaced, none deployment-blocking.
Ready for absorption into v1.2 (or v1.1+) integrated spec.
