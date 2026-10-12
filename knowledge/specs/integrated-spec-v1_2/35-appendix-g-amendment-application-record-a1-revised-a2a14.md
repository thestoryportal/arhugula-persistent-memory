## Appendix G — Amendment Application Record (A1-REVISED, A2–A14)

Record of every ratified amendment applied in v1.2. Each amendment carries a section pointer to where it is applied in the spec body, the session in which it was ratified, and a one-line summary of the amendment's effect.

| Amendment | Ratified in | Applied at | Summary of effect |
|---|---|---|---|
| **A1-REVISED** | GS10 | §11.8.1.1 (new subsection); C-CRC-3 | Bounded compensation under READ_ONLY mode — the original A1 compensation-suspension rule is amended to permit narrowly-bounded compensation writes during READ_ONLY, with the bound defined by C-CRC-3. Resolves the v1.1 deadlock where a transaction held under CIRCUIT_TRIPPED could not compensate and could not abort. `BOUNDED_COMPENSATION_VIOLATION` Ledger entry added when the bound is exceeded. |
| **A2** | GS10 | §11.8.1 (revised text); GAP-35 | `CIRCUIT_RESET_REJECTED` field semantics clarified — structured precondition-unmet reason code required. Non-consumed CeremonyToken invariant: a token rejected at precondition check is NOT consumed (the ceremony never admitted), distinct from a token that admits and then fails. |
| **A3** | GS4 v2; finalized GS10 | §11.8.1 (IC-TC-RESET); §14.x (ceremony authorization); §20 | IC-TC-RESET placeholder populated. Reset ceremony is CAK-authorized via IC-SCOPE-AUTH-1 (CeremonyToken envelope). CAK-authorization is necessary-but-not-sufficient — the Transaction Controller's independent precondition verification remains. |
| **A4** | GS12 | §14.3 (SCOPE_HASH_MISMATCH handling) | Per-invocation `SCOPE_HASH_MISMATCH` escalation threshold lowered from 3 consecutive errors (v1.1) to **2 consecutive errors** (v1.2). Addresses Warden concern that a three-attempt oracle window was too permissive. `SCOPE_MISMATCH_ESCALATED` Ledger entry added. |
| **A5** | GS4 v2 | §10.9; IC-SCOPE-UPDATE | CAK verification precedes SCOPE_UPDATED Ledger write. No SCOPE_UPDATED entry is produced by a failed authorization. Orders the write side of the ceremony admission chain. |
| **A6** | GS4 v2; finalized GS7 v3 | §10.9; IC-SCOPE-UPDATE admission order; GAP-27 / D89 (scope_update_min_interval_seconds) | Rate-limit check precedes signature verification. Eliminates signature-oracle attack surface — an attacker cannot force expensive crypto work simply by sending ceremony requests faster than the rate window. Applies to all ceremony types under IC-SCOPE-AUTH-1. |
| **A7** | GS5 v3 / GS10 | Appendix C — deprecated-entries block | Schema deprecation machinery introduced. Historical deprecated entries remain chain-valid forever (C-DEPREC-1); post-cutoff writes are integrity violations (C-DEPREC-2); audit tools map deprecated entries to unified successors (C-DEPREC-3). `SCHEMA_DEPRECATION_ENACTED` and `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF` entries added. |
| **A7b** | GS5 v3 / GS10 | Appendix C — deprecation markers on `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` | Two specific v1.1 entry types deprecated and replaced by unified CeremonyToken failure-set entries (`CEREMONY_AUTH_SIGNATURE_INVALID`, `CEREMONY_AUTH_REPLAY_REJECTED`). Concrete application of A7's deprecation machinery. |
| **A8** | GS10 | §11.8 (circuit-breaker trip); Appendix C `CIRCUIT_TRIPPED` entry amendment | Cross-category trip-reason annotation. Every `CIRCUIT_TRIPPED` entry now records `originating_category ∈ {INTEGRITY, CONSISTENCY, SECURITY}` so that the reset ceremony (IC-TC-RESET) can select its precondition branch from the correct provenance context. Resolves the v1.1 ambiguity where trip provenance was inferable but not attested. |
| **A9** | GS4 v2 | §10.9; IC-SCOPE-UPDATE payload | `ceremony_token_id` field replaces the v1.1 standalone `operator_signature` field on SCOPE_UPDATED entries. Signatures are nested within the CeremonyToken envelope (IC-SCOPE-AUTH-1) rather than flat fields on the domain entry. |
| **A10** | GS4 v2 | §13.2 (genesis-seal.json); §20.3 (CAK anchor) | `ceremony_authorization_key_anchor` added to Tier 1 `genesis-seal.json`. This is the public-key anchor against which every CeremonyToken envelope signature is verified. Mint-once at Genesis. A separate `break_glass_key_anchor` is added as the second Tier 1 anchor per §23.3. |
| **A11** | GS10 / GS13 | Appendix A — Deployment Preconditions | v1 CAK backup-custodian pre-arrangement requirement. Operator MUST pre-arrange M ≥ 3 break-glass custodians BEFORE declaring the harness operational. Without pre-arranged custodians, a post-deployment CAK compromise has no recovery path short of Genesis re-initialization. Partial mitigation for T15; full resolution v2. |
| **A12** | GS9 v2 | §24.2 (Point 1); IC-CORPUS-AUTH amendment | `expires_at` predicate added to corpus author registry at submission ingress. An expired author identity cannot submit new cases. `CORPUS_WRITE_REJECTED` with reason code `AUTHOR_EXPIRED` is the enforcement record. |
| **A13** | GS9 v2 | §24.2 (Point 2); IC-SL7 amendment | `contains_expired_author_cases` response field added to IC-SL7 Meta-* token issuance. When the active corpus contains cases authored by an expired identity, the token is still issued but the Meta-* run completes in advisory posture with the `EXPIRED_AUTHOR_PRESENT` flag on the Ledger result record. No mid-run revocation. |
| **A14** | GS9 v2 / GS8 v3 residual | §25.2; Appendix C `CONSTITUTIONAL_FAILURE` amendment | Q5 weak-check field pair. Every `CONSTITUTIONAL_FAILURE` entry now carries both `invariant_statement` (from test metadata) and `failure_assertion_message` (captured verbatim from runtime). Fields are co-recorded, not compared at runtime. Operator audit query surfaces divergences. Preserves determinism requirement of D97 Q5. |

### Amendment ordering and precedence

Amendments apply in declaration order unless an amendment explicitly supersedes a prior one. A1 → A1-REVISED is the only supersession in the v1.2 set: A1 (v1.1 original) is fully replaced by A1-REVISED per GS10. A2 through A14 are strictly additive to their respective anchor sections.

No amendment in v1.2 reverses a v1.1 decision or removes a v1.1 interface contract. All v1.2 amendments are either additive or clarifying. Two v1.1 Ledger entry types are deprecated under A7b; deprecation is additive (historical entries remain chain-valid) and is the only "removal" in v1.2.

### Amendment ratification provenance

- **GS4 v2:** A3 (initial), A5, A6 (initial), A9, A10. IC-SCOPE-AUTH-1 infrastructure.
- **GS5 v3:** A7, A7b (initial — deprecation machinery).
- **GS7 v3:** A6 (finalized with GAP-27 / D89).
- **GS9 v2:** A12, A13, A14.
- **GS10:** A1-REVISED, A2, A3 (finalized), A7/A7b (finalized with migration tooling), A8, A11 (initial).
- **GS11:** (no new amendments; ratification and integration session.)
- **GS12:** A4.
- **GS13:** A11 (finalized as Appendix A precondition text).

---

