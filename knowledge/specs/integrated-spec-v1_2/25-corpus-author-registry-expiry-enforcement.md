## 24. Corpus Author Registry Expiry Enforcement

### 24.1 Purpose

The `corpus-author-registry/` Tier 2 sealed corpus (§13.3; GAP-8) admits an optional `expires_at` field per author record. §24 specifies where expiry is checked, how it is enforced, and what happens to Meta-* runs whose corpus still contains cases authored by an expired identity. Source: GAP-8 residual + v2 GS9 D99.

### 24.2 Two-Point Enforcement Model

Expiry is enforced at two discrete surfaces. Mid-run revocation is explicitly **not** performed — a Meta-* run that begins before a key's expiry crosses completes in an advisory posture rather than being aborted.

**Point 1 — Corpus case submission ingress (Warden-owned, A12-IC-CORPUS-AUTH).**
When an author submits a new corpus case, the Warden verifies that the submitting identity's `expires_at` is either absent or strictly greater than `now()`. An expired identity cannot submit. This is the authoritative enforcement surface for future-case admission. Rejection emits `CORPUS_WRITE_REJECTED` with reason `AUTHOR_EXPIRED`.

**Point 2 — IC-SL7 Meta-* token issuance (A13-IC-SL7).**
When the Transaction Controller requests an IC-SL7 corpus-access token for a scheduled Meta-* run, the Corpus Seal Registry verifies that every author whose cases are in the active corpus version either has no `expires_at` or has not yet crossed it. If any author has expired *and* their cases remain in the active corpus version:

- The IC-SL7 token is still issued (no run abortion).
- The IC-SL7 response carries a `contains_expired_author_cases: true` field.
- The Meta-* run completes in advisory posture; the Ledger result record carries an `EXPIRED_AUTHOR_PRESENT` advisory flag alongside the Health Score.

No new Ledger entry type is introduced for the advisory signal — it is an additive flag on the existing Meta-* result record.

### 24.3 Spec Block — Corpus Author Registry Expiry

**What it must enforce:** Expired corpus author identities cannot submit new cases. Runs whose existing corpus contains expired-author cases complete with an advisory flag rather than being revoked.

**Hard constraints:**
- **C-CORPUS-EXP1:** Expired author identity MUST NOT be accepted at corpus case submission ingress (Point 1).
- **C-CORPUS-EXP2:** Meta-* runs encountering expired-author cases in the active corpus version MUST complete with the `EXPIRED_AUTHOR_PRESENT` flag and MUST NOT be revoked mid-run (Point 2).

**Tradeoffs decided:**
- Advisory-only at Point 2 over mid-run abort — consistent with the harness pattern that Meta-* integrity is operator-observed, not operator-blocking.
- Two-point enforcement over single-point — Point 1 alone would leave previously-admitted cases unobserved; Point 2 alone would admit new cases from expired authors.

**Open questions (deferred):**
- Corpus version cadence for removing cases authored by expired identities — operator policy, parallel to general corpus extension cadence (OQ-V5 residual).

**Interface contract amendments:**
- **A12-IC-CORPUS-AUTH** — `expires_at` predicate added at submission ingress.
- **A13-IC-SL7** — `contains_expired_author_cases` response field + `EXPIRED_AUTHOR_PRESENT` advisory flag propagation.

### 24.4 Non-Goals

§24 does not specify:
- Expiry notification / pre-expiry warning mechanisms (operator-owned alerting).
- Automatic case-removal ceremonies when an author expires (operator discretion via normal corpus versioning).

---

