# Gap Session 10 Summary — Warden-Led Consolidation

**Session:** GS10 of 13
**Primary skill:** aisecops-specialist (Warden)
**Supporting skills:** memit-specialist, graph-data-architect, state-consistency-theorist
**Baseline:** v1.1 integrated spec + GS1–GS9
**Gaps addressed (11):** GAP-29a, GAP-29b, GAP-33 (verify), GAP-33 (open), GAP-36, GAP-37, GAP-40, GAP-41, GAP-42, GAP-44, GAP-47
**Sequencing note:** GAP-29b resolved first per highest-priority directive; its W3 policy is then referenced by GAP-44 and the GAP-31 pre-evaluation.

---

## Resolutions

### GAP-29b — W3 Scope Consolidation Policy — Spec Block

**What it must do / represent / enforce / guarantee:**
Scope the W3 emergency escalation path to a closed set of entry types, each of which must satisfy two mandatory admission conditions. This policy governs v1 and all future carve-out requests.

**Hard constraints:**
- **C-W3-1 (Admission Criteria):** A Ledger entry type is W3-eligible only if BOTH hold:
  - (a) the normal W1 Orchestrator-mediated path is unavailable or compromised at the moment the entry must be written — i.e., writing via W1 would fail or be silently suppressed; AND
  - (b) the entry is required to preserve forensic evidence of an integrity, security, or trust-boundary failure that would otherwise be lost.
- **C-W3-2 (Rate Cap):** 1 entry per minute per component (Gate, TC, Boot-verifier). Unchanged from §16.2.
- **C-W3-3 (Schema Lock):** Each W3-eligible type has a schema fingerprint (SHA-256 of canonical serialization) recorded in Appendix C-W3. Entries failing fingerprint match are rejected and themselves logged via `INTEGRITY_VIOLATION_EMERGENCY`.
- **C-W3-4 (Post-W3 Suspension):** Any W3 write triggers write suspension per §11.8.1 and forces human investigation. Unchanged.
- **C-W3-5 (Carve-Out Registry):** Appendix C-W3 lists every W3-eligible type with source session, admission rationale, schema fingerprint, and ratification status.

**Tradeoffs decided:**
- Scope defined by admission criteria rather than a frozen enumeration — permits principled future additions without re-opening the policy.
- Rejected "freeze W3 at current types" (GS5/GS6 already demonstrated legitimate expansion patterns).
- Rejected "open W3 to any INTEGRITY/SECURITY sync entry" (recreates the unbounded carve-out problem).

**Ratification of three existing carve-outs:**

1. `DEPRECATED_ENTRY_WRITTEN_POST_CUTOFF` (GS5) — **RATIFIED.** (a) met: a deprecated entry reaching the Ledger implies Orchestrator policy enforcement failed. (b) met: without W3, a compromised Orchestrator writing deprecated entries leaves no forensic trace.

2. `ORCHESTRATOR_UNAVAILABILITY_ESCALATED` (GS5) — **RATIFIED with tightening.** (a) trivially met. (b) met. **Tightening:** activation threshold explicitly = ≥3 consecutive failed W1 attempts OR ≥30 seconds continuous unreachability, whichever fires first. Prevents nuisance escalation on transient network blips.

3. `LEDGER_SIGNATURE_REVERIFICATION_FAILED` (GS6) — **RATIFIED.** (a) met: tamper detection during reconcile means the Orchestrator-mediated path cannot be trusted to log its own failure. (b) met: the forensic record would be lost if the tampered path is also the logging path.

**Pre-evaluation of GAP-31 candidate (`HOLD_RELEASE_REASON_UNWARRANTED`):**
Likely admissible under this policy if GS11 confirms (a) unwarranted release implies a compromised signer — Orchestrator mediation is the failure mode — and (b) absence of W3 would lose the forensic record of the unwarranted reason. GS11 must produce explicit admission reasoning; this policy does **not** pre-authorize.

**Open questions (deferred):**
- W3 registry audit cadence — proposed quarterly Warden review; defer to governance layer.
- W3 schema-fingerprint residence (Genesis-baked vs. first-boot-computed) — proposed Genesis-baked; revisit in GS11 if Genesis ceremony surface becomes unwieldy.

**Interface contract:**
- **IC-W3-POLICY-1:** Any proposed new W3-eligible type requires a written admission analysis against C-W3-1(a) and C-W3-1(b), ratified in a Warden-primary gap session, with schema fingerprint committed to Appendix C-W3 before activation.

---

### GAP-29a — Manifest Lattice Completeness (IC-MANIFEST-1 Check 8) — Spec Block

**What it must do / represent / enforce / guarantee:**
At commit time, the Gate must verify `larql_migration_manifest` provides a translation path from every supported legacy version to `current_larql_version`, so that later compaction of an Anchor-Superseded Archive patch cannot fail because of a missing lattice edge.

**Hard constraints:**
- **C-LATTICE-1:** For every v_i ∈ [min_supported_larql_version, current_larql_version), the manifest must contain a sequence of rules forming a directed path v_i → … → current_larql_version. **Transitive coverage via intermediate versions IS acceptable**; direct v_i → current rules are NOT required.
- **C-LATTICE-2:** The Gate evaluates check 8 by topological walk: for each v_i it resolves a translation chain using available rules. Any unreachable v_i aborts the commit.
- **C-LATTICE-3:** Rejection emits `MANIFEST_LATTICE_INCOMPLETE` — SECURITY, synchronous, W1 via the standard Gate path. Payload: `missing_source_version`, `missing_edge` (first unreachable hop), `manifest_hash`, `current_larql_version`.
- **C-LATTICE-4:** Check 8 runs AFTER checks 1–7 and is a hard commit-gate. No advisory path.

**Tradeoffs decided:**
- **Transitive chains accepted** rather than requiring direct rules. Rationale: the dry-run artifact (checks 5–6) already validates end-to-end translation behavior for patches that actually traversed the chain; direct-rule requirement would bloat the manifest without forensic gain. GDA concurred.
- **SECURITY over INTEGRITY** — a missing edge is either operator authoring error or manifest tampering; the Gate cannot distinguish at check time, so conservatively SECURITY.
- **Synchronous** — compaction-time failure is the alternative and is strictly worse.

**Open questions (deferred):**
- Whether `min_supported_larql_version` can itself advance via ceremony, shrinking the lattice. Yes in principle; defer ceremony type to GS11.
- Interaction with `LARQL_VERSION_LEGACY` advisory (patch-level, Gate) vs. check 8 (manifest-level). No conflict — MEMIT confirmed.

**Interface contract:**
- **IC-MANIFEST-1 (amended):** 7-check gate becomes 8-check. Check 8 as above. Checks 1–7 unchanged.

---

### GAP-33 (verify) — IC-DRYRUN-1 / GS4 CeremonyToken Consistency

**Verification result:** CONSISTENT.
- `dry_run_executor` access role is properly registered as a CAK-authorized identity per the GS4 CeremonyToken framework role enumeration.
- No re-resolution required. Logged for traceability.

---

### GAP-33 (open) — Dry-Run Artifact Store — Spec Block

**What it must do / represent / enforce / guarantee:**
Storage, retention, tamper-evidence, and access policy for dry-run reports referenced by `dry_run_artifact_hash` in `larql_migration_manifest` entries, so that IC-MANIFEST-1 checks 5–7 are deterministically evaluable.

**Hard constraints:**
- **C-DRS-1 (Location):** `<harness_root>/.dry-run-store/` — operator-controlled directory on the same volume as the harness Git repository, outside `.vindex` overlay scope.
- **C-DRS-2 (Naming):** Filename = `{sha256_of_content}.dry-run.json.sig`. Content-addressed; filename equality ⇒ byte-identity.
- **C-DRS-3 (Tamper-Evidence):** Each report signed by a `dry_run_executor` CAK-authorized identity (per IC-DRYRUN-1). The manifest entry's `dry_run_artifact_hash` anchors the content hash into the Ledger via the manifest ceremony. Any mismatch between stored-file SHA-256 and manifest-declared hash fails check 5.
- **C-DRS-4 (Retention):** Reports retained until BOTH (a) the referencing manifest entry is compacted into the Anchor-Superseded Archive OR deprecated via ceremony, AND (b) ≥ `freshness_window + operator_review_period` has elapsed since the ceremony timestamp. v1 defaults: freshness_window = 7 days (per check 7), operator_review_period = 30 days → **37-day floor**.
- **C-DRS-5 (Pruning Authority):** Pruning occurs only under `RETENTION_PRUNING` ceremony (GAP-47). Emits `DRY_RUN_ARTIFACT_PRUNED`. Unceremonied deletion is a SECURITY event: `DRY_RUN_ARTIFACT_MISSING_UNCEREMONIED`, sync, W1.
- **C-DRS-6 (Warden Audit Surface):** Operator-owned, Warden-audited. Warden holds **read-only metadata visibility** — list of `(hash, ceremony_id, retention_deadline)` triples. No write or delete capability. No content inspection.

**Tradeoffs decided:**
- **Operator-owned over Warden-owned** — dry-run artifacts are operational scaffolding, not core security state; Warden ownership would couple Warden to harness release lifecycle unnecessarily.
- **Metadata-only audit surface** — contents may include operator-confidential test data. (Creates T-S-RP-1; accepted for v1.)
- **37-day floor** chosen to give operator review time even if freshness window expires. Deployment profile can extend; floor is non-negotiable.
- **Filesystem over CAS daemon** — v1 simplicity.

**Open questions (deferred):**
- CAS backend migration at scale. Defer.
- Cross-harness replication for HA. Outside 13-session arc.

**Interface contract:**
- **IC-DRS-1:** As specified. Integrates with IC-MANIFEST-1 checks 5–7 and IC-DRYRUN-1.

---

### GAP-36 — CIRCUIT_RESET_REJECTED Rate Limit — Spec Block

**Policy chosen: (a) — rate limit + advisory entry + operator alert.**

**What it must do / represent / enforce / guarantee:**
Cap noise-generating repeated invalid reset attempts while preserving signature verification as the actual authorization control.

**Hard constraints:**
- **C-CRR-1:** N = 5 rejections in M = 60 minutes (rolling window per harness instance).
- **C-CRR-2:** On threshold breach, emit `CIRCUIT_RESET_REJECTED_RATE_EXCEEDED` — INTEGRITY advisory, async, W1. Payload: `rejection_count`, `window_start`, `most_recent_rejection_hash_chain`.
- **C-CRR-3:** Emission triggers standard operator alert channel (email + Ledger-visible advisory).
- **C-CRR-4:** Further rejections within the same window continue to be logged as individual `CIRCUIT_RESET_REJECTED` entries but do NOT re-emit the advisory (debounced per window).
- **C-CRR-5:** Rate limit does NOT block further reset attempts — signature check remains sole authorization control. This is observability, not enforcement.

**Tradeoffs decided:**
- Rejected (b) accept current state — unbounded advisory noise is itself a forensic-evidence degradation concern.
- Advisory (INTEGRITY) rather than SECURITY — signature requirement is intact; this is behavioral signal, not confirmed attack.
- Fixed window over progressive escalation — v1 simplicity; escalation can be added if telemetry warrants.

**Open questions (deferred):**
- Whether N/M should be operator-configurable or Genesis-locked. Defer to GS11 / governance session.

**Interface contract:**
- **IC-CRR-1:** As specified. Orthogonal to per-CAK burst (GAP-41) and per-ceremony-type limits (GAP-27).

---

### GAP-37 — §11.8.1 Governance Write Carve-Out — Spec Block (closes T-SC-W-2)

**Ratification decision:** RATIFIED with one clarification (W3 cross-reference appended).

**What it must do / represent / enforce / guarantee:**
Make explicit that signed governance-category W1 writes (the ceremonies required to exit CIRCUIT_TRIPPED) proceed while ordinary token-mediated writes remain suspended.

**Ratified §11.8.1 text:**

> "Write suspension during CIRCUIT_TRIPPED applies to token-mediated application writes. Governance-category W1 Ledger entries written as part of the signed reset ceremony (`CIRCUIT_RESET`, `DEPENDENCY_HOLD_RELEASED_SIGNED` with `release_reason: GENESIS_RESET_PREPARATION`, and `RECONCILIATION_COMPLETE`) proceed regardless of CIRCUIT_TRIPPED state, provided each carries a valid CeremonyToken for its ceremony type. W3 emergency writes are also unaffected by CIRCUIT_TRIPPED (per §16.2)."

**Hard constraints:**
- **C-GCO-1 (Enumerative, not Categorical):** Only the three listed entry types plus W3 writes are exempt. No implicit expansion to "all governance-category entries."
- **C-GCO-2 (Token-First):** Token validation runs BEFORE suspension is bypassed. A ceremony entry with an invalid token is rejected normally — it does NOT gain suspension-bypass privileges.
- **C-GCO-3 (Expansion Gate):** Additions to this list require Warden-primary session ratification with carve-out rationale.

**Tradeoffs decided:**
- Enumerated list over categorical rule — minimizes surface area, prevents scope creep.
- W3 clause appended for cross-reference completeness — prevents future confusion about whether §11.8.1 and §16.2 conflict.

**Open questions (deferred):** None.

**Interface contract:**
- **IC-GCO-1:** §11.8.1 amended with ratified text. **Tension T-SC-W-2 CLOSED.**

---

### GAP-40 — CAK Bootstrap Tool — Spec Block

**What it must do / represent / enforce / guarantee:**
A pre-harness operator tool that mint-once writes `ceremony_authorization_key_anchor` into `genesis-seal.json`, establishing the CAK trust-chain root before the harness is ever started. The harness cannot produce this artifact (circular trust); the tool is the trust-chain seed.

**Hard constraints:**
- **C-BOOT-1 (Identity Separation):** Tool runs under operator credentials in a process identity distinct from any harness-owned identity. No shared filesystem user, group, or capability set with harness runtime.
- **C-BOOT-2 (Input):** Accepts operator-generated public key material (CAK public half) from an operator-controlled HSM or key ceremony. Private half never enters tool memory.
- **C-BOOT-3 (Atomic Write):** `genesis-seal.json` written via temp-file + fsync + rename, followed by post-write SHA-256 verification. Mismatch aborts boot preparation.
- **C-BOOT-4 (Boot Manifest):** Tool emits signed `boot_manifest.json` containing `genesis_seal_hash`, `operator_root_signature`, `tool_version`, `tool_binary_hash`, `timestamp`. Signed with operator root key (offline, out-of-band).
- **C-BOOT-5 (First-Boot Verification):** At first boot, harness verifies `boot_manifest` signature against a **compile-time-embedded `operator_root_public_key`**, verifies `genesis_seal_hash` matches actual file SHA-256, verifies `tool_binary_hash` against independently published release hash. Any mismatch refuses boot with `GENESIS_SEAL_UNVERIFIED` (SECURITY, via W3 boot-verifier path).
- **C-BOOT-6 (Distribution):** Distributed as a signed release artifact alongside the harness but from a **distinct signing authority chain** (operator root, not harness release key). Two independent trust roots converging at first boot.
- **C-BOOT-7 (Re-use Prohibition):** Tool refuses to overwrite an existing `genesis-seal.json`. Re-mint requires explicit operator teardown of the prior harness instance.

**Tradeoffs decided:**
- **Dual-root signing model** accepted — reduces single-vendor compromise risk at cost of operator setup complexity.
- **Per-operator harness binary** via compile-time-embedded operator root public key — harness binary is not a universal artifact. Accepted as the price of closing the bootstrap-trust gap. (Creates GAP-50.)
- **Mint-once** — rejected automated re-mint paths as reintroducing the circular-trust problem.

**Open questions (deferred):**
- Operator key-ceremony internal spec — operator-domain policy, out of scope for v1 harness spec.
- Tool upgrade path on operator root rotation — defer to GS12 or post-v1.

**Interface contract:**
- **IC-BOOT-1:** As specified. Resolves T-S4-N2 (bootstrap-tool trust asymmetry).

---

### GAP-41 — Per-CAK Ceremony Burst Limit — Spec Block

**What it must do / represent / enforce / guarantee:**
Cap rapid ceremony issuance from a single CAK identity to bound blast radius of a briefly-exposed CAK before operator detection and rotation.

**Hard constraints:**
- **C-CAKB-1 (Window):** 10 minutes (rolling per CAK fingerprint).
- **C-CAKB-2 (Limit):** 5 ceremonies of any type per CAK per 10-minute window.
- **C-CAKB-3 (Breach Behavior):** 6th ceremony REJECTED (not delayed). Emits `CAK_CEREMONY_BURST_EXCEEDED` — SECURITY, synchronous, W1. Payload: `cak_fingerprint`, `ceremony_count_in_window`, `window_start`, `rejected_ceremony_type`.
- **C-CAKB-4 (Effect):** Breach places the CAK into `BURST_SUSPENDED` state — no further ceremonies accepted for 60 minutes or until an explicit `CAK_BURST_CLEARED` ceremony signed by a **different** CAK with Tier 1 authority.
- **C-CAKB-5 (Orthogonality):** Independent of per-ceremony-type limits (GAP-27) and CIRCUIT_RESET_REJECTED (GAP-36). Burst check applies first; if burst exceeded, per-type limit is not consulted.
- **C-CAKB-6 (Break-Glass Exemption):** Break-glass CAK (GAP-42) exempt — its use is already out-of-band quorum-gated.

**Tradeoffs decided:**
- **Rejection over delay** — delay would create a timing side-channel and complicate state.
- **60-minute auto-clear** with explicit-clear path — operator detection window with legitimate-burst escape hatch.
- **SECURITY category** — burst is attacker-characteristic; false-positive cost (operator re-clear) is low.
- **N=5, M=10min** — permits legitimate concurrent Genesis orchestration while flagging attack-rate usage. Subject to revision after telemetry. (Creates GAP-49.)

**Open questions (deferred):**
- Whether legitimate Genesis sequences routinely exceed 5 events in 10 minutes — requires empirical modeling. Flagged as GAP-49.
- Per-CAK window persistence across harness restart — provisionally in-memory; revisit.

**Interface contract:**
- **IC-CAKB-1:** As specified. Layered with GAP-27 and GAP-38.

---

### GAP-42 — Break-Glass Emergency Channel — Spec Block

**What it must do / represent / enforce / guarantee:**
Provide a last-resort recovery path when the primary CAK is declared compromised (`CAK_COMPROMISE_DECLARED`) and normal ceremony issuance is blocked. Must not itself become a parallel compromise vector.

**Hard constraints:**
- **C-BG-1 (Anchor):** Second Tier 1 key anchor `break_glass_key_anchor` written into `genesis-seal.json` at first-boot by the CAK bootstrap tool (extends GAP-40 scope by one field). Public half only; private half held offline under operator quorum.
- **C-BG-2 (Activation Prerequisite):** Break-glass use requires BOTH (a) a prior `CAK_COMPROMISE_DECLARED` Ledger entry AND (b) a quorum-signed `BREAK_GLASS_ACTIVATION` ceremony — M-of-N operator signatures, **M ≥ 3**, N operator-defined at bootstrap.
- **C-BG-3 (Single-Purpose Envelope):** Break-glass key can ONLY sign entries of type `CAK_ROTATION_EMERGENCY`, which replaces the primary CAK anchor with a new operator-provided public key. No general-purpose ceremonies.
- **C-BG-4 (Out-of-Band Injection):** `BREAK_GLASS_ACTIVATION` injected via a dedicated out-of-band path requiring **physical operator access** to the harness host (not over network APIs). Prevents remote exploitation even if break-glass private material is exposed.
- **C-BG-5 (Parallel-Compromise Prevention):**
  - Separate HSM from primary CAK (distinct vendor if operator policy permits).
  - M-of-N across distinct operator identities (no single-human access to M signatures).
  - Physical-access requirement (C-BG-4).
  - Emits `BREAK_GLASS_ACTIVATED` (SECURITY, sync, W1 dedicated path) — alerts regardless of CAK state.
- **C-BG-6 (Post-Activation):** After successful `CAK_ROTATION_EMERGENCY`, break-glass key remains active; operator SHOULD rotate it via a second break-glass ceremony at convenience. New primary CAK resumes normal ceremony authority immediately.
- **C-BG-7 (No Freeze Bypass / TRUST_ROOT_LOST):** If break-glass itself is compromised (detected via anomalous `BREAK_GLASS_ACTIVATION` attempt), harness enters `TRUST_ROOT_LOST` state — both CAK and break-glass blocked. Recovery requires full Genesis re-initialization. **No v1 third-tier recovery.**

**Tradeoffs decided:**
- **Single-purpose key** (rotation only) — minimizes blast radius if break-glass itself is compromised.
- **Physical-access requirement** — highest friction; break-glass is definitionally rare, friction acceptable. (Creates T-W-BG-1.)
- **M ≥ 3 floor** — single-operator break-glass compromise cannot activate it alone.
- **TRUST_ROOT_LOST as terminal** — no third-tier recovery avoids infinite regress of trust anchors; Genesis re-init is the recovery plan for double compromise.

**Open questions (deferred):**
- Exact M, N defaults — operator-configurable at bootstrap; M ≥ 3 hard floor only.
- Whether `CAK_ROTATION_EMERGENCY` should re-trigger reconciliation to verify post-rotation state integrity — lean yes; defer to GS11.

**Interface contract:**
- **IC-BG-1:** As specified. Resolves OQ-S-CAK-1 (GAP-19 v2). Extends IC-BOOT-1 by adding `break_glass_key_anchor` to `genesis-seal.json` schema.

---

### GAP-44 — GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE Classification — Spec Block

**What it must do / represent / enforce / guarantee:**
Correct Ledger classification for the pre-flight refusal entry emitted when a new Genesis attempts to acquire a Hold while a prior failed Genesis's Hold remains active. Must distinguish normal operator retry from abuse pattern.

**Hard constraints:**
- **C-GIB-1 (Baseline):** `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` emitted at **INTEGRITY**, synchronous, W1. Normal case — operator retry before prior Genesis fully cleaned up.
- **C-GIB-2 (Aggregate Promotion):** If ≥3 such entries within a 60-minute rolling window, a follow-on `GENESIS_INITIATION_ABUSE_PATTERN` entry is emitted at **SECURITY**, synchronous, W1. The individual INTEGRITY entries remain unchanged — aggregate detection is an additional signal, not a reclassification.
- **C-GIB-3 (W3 Eligibility):** INTEGRITY baseline is **NOT** W3-eligible (does not satisfy C-W3-1(a) — the pre-flight refusal demonstrates W1 is functioning). SECURITY aggregate entry is **ALSO NOT** W3-eligible by default (Orchestrator is up; attack is surfacing through detection, not suppressing it).
- **C-GIB-4 (Escalation):** Aggregate SECURITY entry triggers standard operator alert; repeated aggregate entries (>2 in 24h) trigger automatic hold-release ceremony freeze for 24h or until operator review.

**Tradeoffs decided:**
- **Split baseline from aggregate** — preserves Ledger signal fidelity; legitimate operator retries don't generate SECURITY noise.
- **3-in-60min** — conservative; legitimate operators rarely retry this aggressively.
- **No W3 eligibility** — applying GAP-29b's C-W3-1(a) test: pre-flight refusal means Gate and Orchestrator are both up and enforcing. W3 would be scope creep.

**Open questions (deferred):** None.

**Interface contract:**
- **IC-GIB-1:** Classification and aggregate detection as specified. Consistent with GAP-29b admission criteria. Confirms Warden-co-review requested by gap brief: INTEGRITY baseline is correct per threat model.

---

### GAP-47 — RETENTION_PRUNING Ceremony Type — Spec Block

**What it must do / represent / enforce / guarantee:**
Integrate dry-run artifact pruning into the GS4 CeremonyToken framework.

**Hard constraints:**
- **C-RP-1:** Add `RETENTION_PRUNING` to the CeremonyToken `ceremony_type` enum.
- **C-RP-2:** Required authority: any CAK-authorized identity with the **new** `artifact_retention_manager` role.
- **C-RP-3:** Per-ceremony rate limit: 12 invocations per 24h per harness instance.
- **C-RP-4:** Scope: may emit `DRY_RUN_ARTIFACT_PRUNED` entries (per IC-DRYRUN-1). v1 scope is dry-run store only; extensible post-v1 to other retention-managed artifact classes.
- **C-RP-5:** Per-CAK burst limit (GAP-41) applies normally.

**Tradeoffs decided:**
- **New role over reusing `dry_run_executor`** — separation of concerns between execution and retention.
- **12/24h** — placeholder; revise after first deployment telemetry.

**Open questions (deferred):**
- Unifying `RETENTION_PRUNING` with other retention-managed artifacts (e.g., Ledger compaction artifacts). Defer.

**Interface contract:**
- **IC-RP-1:** `RETENTION_PRUNING` ceremony type as specified. Completes IC-DRYRUN-1 ceremony-type integration.

---

## Gap Session Summary Block

### GAPS RESOLVED

| Gap | Resolution | Interface Contract Issued |
|-----|-----------|---------------------------|
| GAP-29a | Manifest lattice completeness → IC-MANIFEST-1 Check 8 added; transitive coverage accepted; `MANIFEST_LATTICE_INCOMPLETE` (SECURITY, sync). | IC-MANIFEST-1 (amended) |
| GAP-29b | W3 scope consolidation policy. Two admission criteria (C-W3-1). All three existing carve-outs ratified (ORCHESTRATOR_UNAVAILABILITY_ESCALATED tightened with explicit activation threshold). | IC-W3-POLICY-1 |
| GAP-33 (verify) | IC-DRYRUN-1 confirmed consistent with GS4 CeremonyToken framework. No action. | — |
| GAP-33 (open) | Dry-run artifact store: `<harness_root>/.dry-run-store/`, 37-day minimum retention, operator-owned with Warden metadata-only audit surface. | IC-DRS-1 |
| GAP-36 | CIRCUIT_RESET_REJECTED rate limit option (a): N=5 / M=60min, advisory + operator alert, observability-not-enforcement. | IC-CRR-1 |
| GAP-37 | §11.8.1 governance write carve-out text ratified with W3 cross-reference clarification. **Tension T-SC-W-2 CLOSED.** | IC-GCO-1 |
| GAP-40 | CAK bootstrap tool: dual-root signing model (operator root + harness release key), atomic write, signed boot manifest, refuse-boot semantics on verification failure. | IC-BOOT-1 |
| GAP-41 | Per-CAK burst limit: 5 ceremonies / 10 min, `BURST_SUSPENDED` state on breach, 60-minute auto-clear or Tier 1 explicit clear. | IC-CAKB-1 |
| GAP-42 | Break-glass channel: second Tier 1 anchor, M ≥ 3 of N quorum, physical-access injection, single-purpose `CAK_ROTATION_EMERGENCY`, `TRUST_ROOT_LOST` as terminal double-compromise state. Resolves OQ-S-CAK-1. | IC-BG-1 |
| GAP-44 | `GENESIS_INITIATION_BLOCKED_HOLD_ACTIVE` INTEGRITY baseline with `GENESIS_INITIATION_ABUSE_PATTERN` SECURITY aggregate (≥3 in 60 min). Neither W3-eligible per GAP-29b policy. | IC-GIB-1 |
| GAP-47 | `RETENTION_PRUNING` ceremony type added; new `artifact_retention_manager` role. | IC-RP-1 |

### GAPS PARTIALLY RESOLVED
None. All eleven items fully resolved within session scope.

### GAPS DEFERRED
- Operator key-ceremony internal spec (from GAP-40) — operator-domain policy, out of scope for v1.
- Tool upgrade path on operator root rotation (GAP-40) — GS12 or post-v1.
- CAS backend migration for `.dry-run-store/` (GAP-33) — defer until telemetry warrants.
- Cross-harness replication of dry-run store (GAP-33) — HA concern, outside 13-session arc.
- W3 registry audit cadence (GAP-29b) — governance layer.
- W3 schema-fingerprint residence (Genesis-baked vs. first-boot) — GS11 if Genesis surface becomes unwieldy.
- Break-glass default M, N values (GAP-42) — operator-configurable; M ≥ 3 floor only.
- Whether `CAK_ROTATION_EMERGENCY` re-triggers reconciliation (GAP-42) — GS11.
- Per-CAK burst-window persistence across restart (GAP-41) — provisionally in-memory; revisit.
- Configurability of GAP-36 N/M — GS11 / governance session.
- Unification of `RETENTION_PRUNING` with other retention-managed artifacts (GAP-47) — post-v1.

### NEW GAPS SURFACED

- **GAP-48 (Low)** — *Aggregate-detection entry type convention.* GAP-44's `GENESIS_INITIATION_ABUSE_PATTERN` pattern (aggregate-signal entry alongside individual entries) may warrant standardized naming/classification conventions. Always SECURITY? Always carry source-entry-hash-list? Warden + SCT co-owned. Source: GS10.
- **GAP-49 (Medium)** — *Genesis ceremony event-count modeling.* GAP-41's N=5/10min may conflict with legitimate Genesis density. Requires empirical modeling of worst-case legitimate Genesis ceremony sequences before v1 ship. Flag for GS11. Warden + SCT co-owned.
- **GAP-50 (Medium)** — *Per-operator harness binary implication.* GAP-40 C-BOOT-5 requires compile-time-embedded `operator_root_public_key` — harness binaries are not universal artifacts. Implications for release process, reproducible builds, and patch distribution undefined. Warden + Orchestration Comparativist co-owned. Source: GS10.
- **GAP-51 (Medium)** — *New state lifecycle integration.* `BURST_SUSPENDED` (GAP-41) and `TRUST_ROOT_LOST` (GAP-42) introduced this session; interaction with existing §11.8 state machine (CIRCUIT_TRIPPED, READ_ONLY, reconciliation) not explicitly modeled. SCT + Warden co-owned.

### NEW TENSIONS SURFACED

- **T-W-BG-1 (NEW, Warden-internal)** — *Break-glass friction vs. incident-response urgency.* Physical-access requirement (C-BG-4) and M ≥ 3 quorum (C-BG-2) make break-glass extremely slow to activate. Deliberate, but creates tension with real incident response requiring rapid CAK rotation. **Status:** accepted design tradeoff, documented for operator awareness; not a blocker.
- **T-S-RP-1 (NEW, Warden ↔ SCT)** — *Operator-owned dry-run store vs. Warden-audited immutability.* Warden audit surface is metadata-only (C-DRS-6). If a tampered report passes its recorded hash (e.g., content swapped pre-hashing before the executor signs), Warden cannot detect via audit surface alone. Mitigated by manifest-hash anchor in Ledger, but surfaces as asymmetry. **Status:** accepted for v1; flagged for v2.

### TENSIONS CLOSED
- **T-SC-W-2** — *Write Suspension Scope vs. Governance-Ceremony Write Path.* Closed by GAP-37 resolution.

### TRACEABILITY
- Interface contracts issued: IC-W3-POLICY-1, IC-MANIFEST-1 (amended — Check 8), IC-DRS-1, IC-CRR-1, IC-GCO-1, IC-BOOT-1, IC-CAKB-1, IC-BG-1, IC-GIB-1, IC-RP-1.
- `genesis-seal.json` schema extended by one field (`break_glass_key_anchor`) — noted as IC-BOOT-1 scope amendment.
- Appendix C-W3 requires population with ratified schema fingerprints (operator task during implementation).
- Inbound references for GS11: GAP-31 admissibility pre-evaluation (GAP-29b), GAP-49, GAP-51, post-rotation reconciliation question (GAP-42).
