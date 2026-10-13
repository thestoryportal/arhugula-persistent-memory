## 13. Configuration Governance — The Three-Tier `.harness/` Model (T4)

### 13.1 Core Rule

Integrity-critical artifacts are classified by trust tier, not by artifact type. Three tiers with distinct integrity mechanisms:

### 13.2 Tier 1 — Immutable Anchor

Mint-once, verify-forever. Trust root.

**Artifacts:**
- `genesis-seal.json` — includes `current_larql_version`, `min_supported_larql_version`, `larql_migration_manifest`, `corpus_author_bootstrap_identity` (GAP-8 / v3 GS8 — replaces the v1.1 `corpus_author_identities` array; the evolving full list now lives in the `corpus-author-registry/` Tier 2 sealed corpus; the Tier 1 field records only the bootstrap identity that seeded the registry), `incremental_prepared_timeout`, `genesis_prepared_timeout` (no default; must be set before Genesis initiation per C-GATE-2), `ceremony_authorization_key_anchor` (A10 — public-key anchor against which every CeremonyToken envelope signature is verified, per §20 / IC-SCOPE-AUTH-1), `scope_mismatch_aggregate_threshold_n` and `scope_mismatch_aggregate_window_seconds` (GAP-38 / GS12 — see §14.3), and the genesis hash fields.
- `orchestrator-key-anchor.json` (public half of Orchestrator signing key)
- `break-glass-anchor.json` (A11-related; second Tier 1 anchor used by the break-glass channel, §23.3 / IC-BG-1).

**Write model:** produced once during bootstrap. Never modified by runtime. CAK rotation is v2 (GAP-19).

**Integrity:** dual-stored (`.state-ledger/` primary + `<repo_root>/.harness/` secondary). Boot-time hash comparison. Mismatch suspends boot.

### 13.3 Tier 2 — Sealed Artifacts

Evolving human-authored integrity-critical artifacts. Signed-append model.

**Artifacts (v1.2 — seven sealed corpora):**
- `meta-validator-suite/` — Validator held-out corpus.
- `meta-tga-corpus/` — TGA held-out corpus.
- `constitutional-suite/` — Constitutional test suite (promoted from S4 D32).
- `write-scope-definitions/` — Per-agent write authority definitions.
- `reconciliation-reviewers/` — Authorized reviewers for Reconciliation Review Queue.
- `corpus-author-registry/` — **Sixth sealed corpus (GAP-8 / v3 GS8).** Authoritative list of identities authorized to submit cases to Meta-Validator and Meta-TGA corpora. Supersedes the v1.1 Tier 1 `corpus_author_identities` array. Per-author fields include `author_id`, `key_fingerprint`, `authorized_corpora` (subset of `{meta-validator-suite, meta-tga-corpus, constitutional-suite}`), `expires_at`, and `bootstrap_link` (references the Tier 1 `corpus_author_bootstrap_identity` for the registry's initial identity). Expiry enforcement per §24.
- `hook-registry/v1` — **Seventh sealed corpus (GAP-54 / GS11).** Authoritative record of permitted boot-time and runtime hook binary hashes. Every hook binary loaded by the harness is hash-matched against this registry at boot. Mismatch produces `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) and suspends boot. See IC-HOOK-BOOT.

**Write model:** versioned additive directories (`v1/`, `v2/`, ... `vN/`). Each version signed by operator key. `manifest.json` tracks current active version and signatures.

**Integrity:** dual-store hash (`.sealed-corpora/<n>/manifest.json` + `SEALED_CORPUS_UPDATE` Ledger entry). Boot-time verification.

**Access:**
- Meta-* corpora: time-bounded capability access during Meta-* runs only. Never exposed to normal Validator or TGA operation.
- Constitutional suite: Validator has persistent read access during normal operation.
- Write Scope Definitions: Authorization Gate has persistent read access during normal operation.
- Reconciliation reviewers: Gate reads when verifying `reconciliation_reviewer_id`.
- Corpus author registry: consulted by IC-SL7 token issuance path and by Meta-* case-submission ingress (§24).
- Hook registry: consulted by boot sequence (IC-HOOK-BOOT) and by any hook-reload ceremony.

**Per-case audit reporting mandatory** for Meta-* runs (T3 closure of OQ-V5). Aggregate-only reporting is forbidden.

**Corpus Authorship Model (D88, IC-CORPUS-AUTH, extended IC-SL7 + §24)**

Corpus authorship is a restricted operator role (C-GOC4). Only identities listed in the active `corpus-author-registry/vN/` sealed corpus may submit cases. No agent identity MUST appear in the registry. Authorization is verified at two points (§24 expiry enforcement):

1. **Submission ingress** — the Orchestrator verifies author identity + `expires_at` predicate at submission time (A12-IC-CORPUS-AUTH — closes the v1.1 gap where expiry was checked only at token issuance).
2. **IC-SL7 token issuance** — the Orchestrator re-verifies expiry at Meta-* run initiation and includes a `contains_expired_author_cases` response field in the IC-SL7 envelope (A13-IC-SL7).

Case formats are formally defined:

- *Meta-Validator case format:* `{ id, prompt, expected_assertion_set: [{ type, value }...], expected_pass }`
- *Meta-TGA case format:* `{ id, specification_fragment, gold_test_set: [{ test_name, assertion_count (≥2), asserts_symbols }...] }`

Minimum viable corpus: 20 cases before any Meta-* run produces a meaningful Health Score. Below minimum, the `health_score` field is `NOT_COMPUTED` — not zero, which would be indistinguishable from a failed run. A corpus staleness flag (`corpus_staleness_flag: true`) is set on the health record if no case has been added in 90 days. Cadence is operator-owned policy, not enforced by this spec.

### 13.4 Tier 3 — Anchored Git Config

Git-committed operational configuration with integrity anchoring.

**Artifacts:**
- `path-classification.json`
- `agent-yamls/*.yaml`
- `genesis-seal.json` (secondary copy of Tier 1)
- `orchestrator-key-anchor.json` (secondary copy of Tier 1)
- `rate-limits.json` — carries `scope_update_min_interval_seconds` (per-initiator primary + per-affected-agent-id secondary; GAP-27 resolution) and related per-CAK / per-ceremony-type rate parameters. See §10.9 admission order and §14.3.

**GAP-27 Tier placement note:** `scope_update_min_interval_seconds` was resolved to Tier 3 placement in `rate-limits.json`. A separate open item remains for whether certain rate parameters that also participate in boot-time `RATE_LIMIT_RETENTION_CONFLICT` validation should migrate to Tier 1; this Tier conflict is deferred to GS13 disposition (OQ-CFG-TIER).

**Write model:** modified via Git commit. Git commit-hook writes `CONFIG_UPDATE` Ledger entry with filename, new hash, Git commit hash.

**Integrity:** Ledger anchor + boot-time hash verification. Boot-time mismatch between current file hash and most recent `CONFIG_UPDATE` entry produces `CONFIG_INTEGRITY_FAIL` and suspends writes.

**Enforcement mode:** detect-at-boot, not prevent-at-write. Stronger enforcement (pre-receive server-side hook) is v2.

### 13.5 Boot-Time Verification Sequence (T4, extended T5, T11, GS5 v3, GAP-46, GAP-54)

Fail-closed. Any step failing suspends writes and produces an integrity-violation event.

1. State Ledger Merkle chain verification from Genesis Seal forward.
2. Genesis Seal dual-store comparison.
3. **Orchestrator key anchor dual-store comparison** (T5).
3a. **CAK anchor semantic verification (v3 GS5 — locally labeled D99/D100 in GS5 v3; see Appendix H collision register).** The `ceremony_authorization_key_anchor` field in `genesis-seal.json` is not merely hash-compared — its public-key material is parsed, the key type (algorithm identifier) is verified against the permitted-algorithm set in the harness release manifest, and the break-glass anchor (`break-glass-anchor.json`) is verified to be structurally independent (distinct public-key material, distinct algorithm-parameter tuple). Failure: `CAK_ANCHOR_SEMANTIC_INVALID` (SECURITY, sync, W1) suspends boot.
4. Sealed corpus manifest verification (for each Tier 2 artifact — seven corpora in v1.2, including `corpus-author-registry/` and `hook-registry/v1`).
4a. **Hook binary integrity check (GAP-54 / GS11 — IC-HOOK-BOOT).** Every hook binary loaded from `hook-registry/v1/` has its current filesystem hash matched against the registry-declared hash. Mismatch: `HOOK_INTEGRITY_VIOLATION` (SECURITY, sync, W1) suspends boot.
5. Anchored Git config verification (for each Tier 3 artifact, including `rate-limits.json`).
5a. **Rate-limit / retention-window consistency check (GAP-46 / GS11 — IC-BOOT-RLRF).** TC verifies that `scope_update_min_interval_seconds` (both per-initiator and per-affected-agent) is strictly less than the minimum retention window for `SCOPE_UPDATED` Ledger entries. The check also verifies equivalent relationships for every rate-limited ceremony type against its corresponding Ledger retention floor. Failure: `RATE_LIMIT_RETENTION_CONFLICT` (SECURITY, sync, W1) suspends boot.
6. Agent YAML ↔ Write Scope Definition binding verification.
7. Periodic integrity verification cadence established (T11).

All pass → writes enabled. Any fail → writes suspended, `<TIER>_INTEGRITY_FAIL` (or the named-failure entry as listed above) produced, human review required.

