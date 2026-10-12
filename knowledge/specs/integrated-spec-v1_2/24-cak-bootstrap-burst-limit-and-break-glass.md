## 23. CAK Bootstrap, Burst Limit, and Break-Glass

### 23.1 CAK Bootstrap Tool (GAP-40 / GS10 — IC-BOOT-1)

**Purpose:** A pre-harness operator tool that mint-once writes `ceremony_authorization_key_anchor` (and `break_glass_key_anchor`, §23.3) into `genesis-seal.json`, establishing the CAK trust-chain root before the harness starts. The harness cannot produce this artifact (circular trust); the tool is the trust-chain seed.

**Hard constraints:**

- **C-BOOT-1 (Identity Separation):** Tool runs under operator credentials in a process identity distinct from any harness-owned identity. No shared filesystem user, group, or capability set with harness runtime.
- **C-BOOT-2 (Input):** Accepts operator-generated public key material (CAK public half, break-glass public half) from an operator-controlled HSM or key ceremony. Private halves never enter tool memory.
- **C-BOOT-3 (Atomic Write):** `genesis-seal.json` written via temp-file + fsync + rename, followed by post-write SHA-256 verification. Mismatch aborts boot preparation.
- **C-BOOT-4 (Boot Manifest):** Tool emits signed `boot_manifest.json` containing `genesis_seal_hash`, `operator_root_signature`, `tool_version`, `tool_binary_hash`, `timestamp`. Signed with operator root key (offline, out-of-band).
- **C-BOOT-5 (First-Boot Verification):** At first boot, harness verifies `boot_manifest` signature against a **compile-time-embedded** `operator_root_public_key`, verifies `genesis_seal_hash` matches actual file SHA-256, verifies `tool_binary_hash` against independently published release hash. Any mismatch refuses boot with `GENESIS_SEAL_UNVERIFIED` (SECURITY, via W3 boot-verifier path).
- **C-BOOT-6 (Distribution):** Distributed as a signed release artifact alongside the harness but from a **distinct signing authority chain** (operator root, not harness release key). Two independent trust roots converging at first boot.
- **C-BOOT-7 (Re-use Prohibition):** Tool refuses to overwrite an existing `genesis-seal.json`. Re-mint requires explicit operator teardown of the prior harness instance.

**Tradeoffs decided:**
- **Dual-root signing model** accepted — reduces single-vendor compromise risk at cost of operator setup complexity.
- **Per-operator harness binary** via compile-time-embedded operator root public key — harness binary is not a universal artifact. Accepted as the price of closing the bootstrap-trust gap. Implications for release / reproducible builds are GAP-57 (GS13 scope, OQ-PATH-DEPLOY).
- **Mint-once** — rejected automated re-mint paths as reintroducing the circular-trust problem.

**Open questions (deferred):**
- Operator key-ceremony internal spec — operator-domain policy, out of scope for v1 harness spec.
- Tool upgrade path on operator root rotation — v2.

**Interface contract:** **IC-BOOT-1** — as specified. Resolves T-S4-N2 (bootstrap-tool trust asymmetry).

### 23.2 Per-CAK Ceremony Burst Limit (GAP-41 / GS10 — IC-CAKB-1)

**Purpose:** Cap rapid ceremony issuance from a single CAK identity to bound blast radius of a briefly-exposed CAK before operator detection and rotation.

**Hard constraints:**
- **C-CAKB-1 (Window):** 10 minutes, rolling per CAK fingerprint.
- **C-CAKB-2 (Limit):** 5 ceremonies of any type per CAK per 10-minute window.
- **C-CAKB-3 (Breach Behavior):** 6th ceremony REJECTED (not delayed). Emits `CAK_CEREMONY_BURST_EXCEEDED` (SECURITY, synchronous, W1). Payload: `cak_fingerprint`, `ceremony_count_in_window`, `window_start`, `rejected_ceremony_type`.
- **C-CAKB-4 (Effect):** Breach places the CAK into `BURST_SUSPENDED` state — no further ceremonies accepted for 60 minutes OR until an explicit `CAK_BURST_CLEARED` ceremony signed by a **different** CAK with Tier 1 authority.
- **C-CAKB-5 (Orthogonality):** Independent of per-ceremony-type limits (GAP-27) and `CIRCUIT_RESET_REJECTED` rate limit (GAP-36, IC-CRR-1). Burst check applies first; if burst exceeded, per-type limit is not consulted.
- **C-CAKB-6 (Break-Glass Exemption):** Break-glass CAK is exempt — its use is already out-of-band quorum-gated (§23.3).
- **C-CAKB-7 (Interaction with Circuit Trip):** A harness in `BURST_SUSPENDED` rejects IC-TC-RESET ceremonies with `CIRCUIT_RESET_REJECTED_BURST_STATE` until burst window clears (GAP-58 resolution, §11.8).

**Tradeoffs decided:**
- **Rejection over delay** — delay creates a timing side-channel and complicates state.
- **60-minute auto-clear with explicit-clear path** — operator detection window with legitimate-burst escape hatch.
- **SECURITY category** — burst is attacker-characteristic; false-positive cost (operator re-clear) is low.
- **N=5, M=10min** — permits legitimate concurrent Genesis orchestration while flagging attack-rate usage. Subject to empirical validation per GAP-56 (OQ-CAKB-BURST).

**Open questions (deferred):**
- Worst-case legitimate Genesis-sequence modeling (GAP-56 / GS13).
- Per-CAK window persistence across harness restart — provisionally in-memory; revisit.

**Interface contract:** **IC-CAKB-1** — as specified. Layers with GAP-27 (per-ceremony rate limit) and GAP-38 (aggregate SCOPE_HASH_MISMATCH).

### 23.3 Break-Glass Emergency Channel (GAP-42 / GS10 — IC-BG-1)

**Purpose:** A last-resort recovery path when the primary CAK is declared compromised (`CAK_COMPROMISE_DECLARED`) and normal ceremony issuance is blocked. Must not itself become a parallel compromise vector.

**Hard constraints:**

- **C-BG-1 (Anchor):** Second Tier 1 key anchor `break_glass_key_anchor` written into `genesis-seal.json` at first-boot by the CAK bootstrap tool (extends IC-BOOT-1 scope by one field). Public half only; private half held offline under operator quorum.
- **C-BG-2 (Activation Prerequisite):** Break-glass use requires BOTH (a) a prior `CAK_COMPROMISE_DECLARED` Ledger entry AND (b) a quorum-signed `BREAK_GLASS_ACTIVATION` ceremony — M-of-N operator signatures, **M ≥ 3**, N operator-defined at bootstrap.
- **C-BG-3 (Single-Purpose Envelope):** Break-glass key can ONLY sign entries of ceremony_type `CAK_ROTATION_EMERGENCY`, which replaces the primary CAK anchor with a new operator-provided public key. No general-purpose ceremonies.
- **C-BG-4 (Out-of-Band Injection):** `BREAK_GLASS_ACTIVATION` injected via a dedicated out-of-band path requiring **physical operator access** to the harness host (not over network APIs). Prevents remote exploitation even if break-glass private material is exposed. See Appendix A deployment preconditions.
- **C-BG-5 (Parallel-Compromise Prevention):**
  - Separate HSM from primary CAK (distinct vendor if operator policy permits).
  - M-of-N across distinct operator identities (no single-human access to M signatures).
  - Physical-access requirement (C-BG-4).
  - Emits `BREAK_GLASS_ACTIVATED` (SECURITY, sync, dedicated W1 path, not W3) — alerts regardless of CAK state.
- **C-BG-6 (Post-Activation):** After successful `CAK_ROTATION_EMERGENCY`, break-glass key remains active; operator SHOULD rotate it via a second break-glass ceremony at convenience. New primary CAK resumes normal ceremony authority immediately.
- **C-BG-7 (No Freeze Bypass / TRUST_ROOT_LOST):** If break-glass itself is compromised (detected via anomalous `BREAK_GLASS_ACTIVATION` attempt), harness enters `TRUST_ROOT_LOST` terminal state — both CAK and break-glass blocked. Recovery requires full Genesis re-initialization. **No v1.2 third-tier recovery.**

**Tradeoffs decided:**
- **Single-purpose key** (rotation only) — minimizes blast radius if break-glass itself is compromised.
- **Physical-access requirement** — highest friction; break-glass is definitionally rare, friction acceptable. Creates T-W-BG-1 (Accepted design tradeoff, GS10).
- **M ≥ 3 floor** — single-operator break-glass compromise cannot activate it alone.
- **TRUST_ROOT_LOST as terminal** — no third-tier recovery avoids infinite regress of trust anchors; Genesis re-init is the recovery plan for double compromise.

**Open questions (deferred):**
- Exact M, N defaults — operator-configurable at bootstrap; M ≥ 3 hard floor only.
- Whether `CAK_ROTATION_EMERGENCY` re-triggers reconciliation to verify post-rotation state integrity — lean yes (see GS11 residual).

**Interface contract:** **IC-BG-1** — as specified. Partially closes OQ-S-CAK-1 (GAP-19 v2 residual). Extends IC-BOOT-1 by adding `break_glass_key_anchor` to `genesis-seal.json` schema. The m-of-n availability variant (OQ-S-CAK-2 / T15 v2) is not addressed in v1.2.

### 23.4 Non-Goals

§23 does not specify:
- CAK scheduled rotation (GAP-19 / v2).
- Operator-internal key ceremony procedures (operator policy).
- Custodian pre-arrangement workflow (Appendix A deployment precondition; T-W-BG-1 accepted friction).

---

