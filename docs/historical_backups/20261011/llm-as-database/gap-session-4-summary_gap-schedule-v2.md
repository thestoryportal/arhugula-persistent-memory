# Gap Session 4 Summary — Warden + Orchestration Comparativist
## Ceremony Authorization Key Model (T14 + GAP-26)

**Session type:** Gap resolution, multi-specialist (Framework Council — reduced quorum)
**Primary skills:** aisecops-specialist (Warden), orchestration-comparativist
**Baseline spec:** v1.1 (+ GS1–GS3 amendments)
**Session number:** 4 of 12 (gap schedule)
**Council constraints honored:** D-CRC-4 (unified ceremony authorization covering all three ceremony types identified in GS1–3), C-CRC-2 (IC-TC-RESET A3 amendment pending)

---

## Session scope

Resolve T14 (single-key vs. dual-key ceremony authorization) as the root dependency, then specify the unified ceremony authorization model for GAP-26 covering manifest ratification (GS1), Dependency Hold release (GS2/3), and scope update ceremony (GS3). Produce IC-SCOPE-AUTH-1. Populate the A3 placeholder in IC-TC-RESET.

---

## GAPS RESOLVED

### T14 — Single-Key vs. Dual-Key for Ceremony Authorization
**Resolution:** Dual-key model adopted. Ceremony authorization requires a key separate from the Orchestrator's first-boot key.

**Warden security argument (primary):** The single-key model collapses the trust boundary between operational writes and governance. If the Orchestrator process is compromised — via prompt injection into a write-authorized agent that can reach filesystem-resident key material, a Git-committed key-anchor substitution during a compromised build, or lateral movement into the harness user — the attacker inherits the authority to authorize its own scope expansions, Hold releases, and circuit-breaker resets. These are precisely the operations a compromised Orchestrator would want to execute without human oversight. The three ceremony types in scope (manifest ratification, Hold release, scope update) are the exact operations that determine what the Orchestrator is subsequently allowed to do — self-authorization of these is privilege escalation by design, not by exploit. The Warden accepts no single-key model that permits the Orchestrator's own signing authority to validate changes to its own scope.

**Orchestration Comparativist overhead assessment (secondary):** Separation is accepted. The acceptable operational overhead envelope:
- Ceremony key registration is a first-boot operation, not a runtime operation. The harness has no write path to ceremony key anchor state; operators use an out-of-band bootstrap tool.
- Ceremony key unavailability during an incident blocks governance ceremonies but does NOT block operational writes, read-only mode, or inference. This is acceptable — ceremonies are off-the-hot-path by design. Circuit-breaker reset blocking during keyholder-unreachability is accepted as a system feature: a system that cannot reach an authorized operator should remain in READ_ONLY.
- Rotation cadence must be bounded. Indefinite retention without rotation is not acceptable operationally or from a compromise-window perspective.
- Multi-operator (m-of-n) key support is NOT required in v1.1 — deferred — but single-keyholder availability risk must be mitigated by a documented break-glass channel.

**Resolution of OQ-S-GAP26-3:** YES — ceremony authorization key MUST be separate from the Orchestrator first-boot key (§10.5).

---

### GAP-26 — Unified ceremony authorization model

**Resolution:** A single umbrella interface contract (IC-SCOPE-AUTH-1) governs authorization for every GOVERNANCE-class ceremony. Specialized ICs (IC-HOLD-RELEASE, IC-SCOPE-UPDATE, IC-TC-RESET, IC-SCHEMA-EXTEND, IC-LDG-RETAIN, IC-SL8, and the GS1 manifest ratification IC) all delegate their authorization layer to IC-SCOPE-AUTH-1 and specify only ceremony-type-specific payload bodies and post-authorization preconditions on top of the common envelope.

**Ceremony types in unified scope (D-CRC-4 compliance):**
1. Migration manifest ratification — GS1, D-GAP1-B
2. Dependency Hold release — GS2/GS3, GAP-21 / IC-HOLD-RELEASE
3. Scope update ceremony — GS3, D90 / IC-SCOPE-UPDATE
4. Inherited GOVERNANCE ceremonies also covered: `CIRCUIT_RESET` (IC-TC-RESET), `RETENTION_OVERRIDE_EXTENDED` / `PROJECT_CLOSED` (IC-LDG-RETAIN), `SCHEMA_EXTENSION_APPROVED` (IC-SCHEMA-EXTEND), corpus manifest signing (IC-SL8), and `CEREMONY_KEY_ROTATION` itself.

**Resolution of OQ-S-GAP26-1 (physical storage contract):**

| Field | Specification |
|---|---|
| **Storage medium — private half** | Operator-controlled, OUTSIDE the harness filesystem. Recommended: hardware security module (YubiKey, Nitrokey, cloud HSM). Acceptable minimum: offline-encrypted file on operator-owned hardware not reachable by the harness process via filesystem or network. The harness process MUST have no read path to the private half. This is non-negotiable — any path from harness process to private key collapses the dual-key model back to single-key. |
| **Storage medium — public half (primary)** | `genesis-seal.json` (Tier 1, mint-once at first-boot) as `CEREMONY_KEY_ANCHOR`. Immutable per §13.2 Tier 1 guarantees. |
| **Storage medium — public half (secondary)** | `<repo_root>/.harness/ceremony-key-anchor.json` (Git-committed). Boot-time hash comparison against Tier 1 primary; mismatch suspends boot (parallel to §10.5 orchestrator-key pattern). |
| **Storage medium — rotation successors** | Tier 2 Sealed Corpus `ceremony-key-rotation-registry/` (append-only, same pattern as `write-scope-definitions/` per §13.3). |
| **Governance tier** | human-approved-change. No autonomous orchestrator modification path. First-boot mint by operator bootstrap tool; runtime additions only via ceremony signed by outgoing key (rotation). |
| **Retention rule — private half** | Operator retains for key lifecycle. Expired private keys archived offline by operator for forensic availability. Minimum archival retention ≥ current Ledger retention policy (IC-LDG-RETAIN) — if PROJECT_LIFETIME, archive for project lifetime. |
| **Retention rule — public half anchors** | Initial `CEREMONY_KEY_ANCHOR` in `genesis-seal.json` is immutable-post-mint (never modified). Successor anchors appended to rotation registry; old anchors retained indefinitely for verification of historical Ledger signatures. |
| **Write authority — private half** | Human operator only, out-of-band to the harness. Never touched by any harness component. |
| **Write authority — public half (initial)** | Operator-run bootstrap tool, pre-first-boot only. |
| **Write authority — public half (successors)** | Outgoing CAK holder, via `CEREMONY_KEY_ROTATION` ceremony. |

**Resolution of OQ-S-GAP26-2 (retention and rotation):**

- **Recommended rotation cadence:** 180 days.
- **Maximum rotation cadence:** 365 days. At 365 days, Warden emits `CEREMONY_KEY_ROTATION_OVERDUE` (GOVERNANCE, sync). After 450 days, ceremony acceptance enters degraded mode: ceremonies still accepted but each emits `CEREMONY_KEY_STALE` (GOVERNANCE, sync) on use, surfaced to operator dashboard.
- **Rotation procedure (five steps):**
  1. Operator generates successor key out-of-band.
  2. Operator signs `CEREMONY_KEY_ROTATION` ceremony with outgoing key. Payload: `previous_key_ref`, `successor_key_pubkey`, `rotation_timestamp`, `operator_id`.
  3. Warden / TC verifies via IC-SCOPE-AUTH-1 using the outgoing key as `key_ref`.
  4. On valid verification: `CEREMONY_KEY_ROTATION_COMPLETE` (GOVERNANCE, sync) written to Ledger with both key references; successor anchor appended to Tier 2 rotation registry.
  5. Outgoing key immediately invalid for new ceremonies; retained solely for historical signature verification.
- **Emergency rotation (suspected compromise):** Operator declares compromise via a break-glass channel pre-registered at first-boot (a second Tier 1 "break-glass" anchor — break-glass key model specified in OQ-S-GAP26-5, deferred to GS5). Declared compromise freezes all ceremony acceptance pending human investigation. Recovery requires Tier 1 bootstrap-level intervention.

---

## NEW INTERFACE CONTRACT — IC-SCOPE-AUTH-1 (ratified)

**IC-SCOPE-AUTH-1 — Ceremony Authorization Key Hierarchy (unified across all GOVERNANCE ceremonies)**

- **From:** Human operator (holder of Ceremony Authorization Key — CAK)
- **To:** Every ceremony verifier in the harness:
  - Gate (scope update ceremony, §10.9)
  - Transaction Controller (circuit reset ceremony, §11.8.1; Hold release delegated to Hold Registry)
  - Hold Registry (Dependency Hold / Genesis Hold release, IC-HOLD-RELEASE)
  - Migration Manifest Verifier (manifest ratification, GS1)
  - Schema Extension Ceremony handler (IC-SCHEMA-EXTEND)
  - Retention Extension / Project Close handler (IC-LDG-RETAIN)
  - Corpus Manifest Verifier (IC-SL8)
  - Ceremony Key Rotation handler (self-referential)
- **What A exposes:** Signed ceremony payload with common envelope:
  ```
  {
    ceremony_type: "SCOPE_UPDATE" | "HOLD_RELEASE" | "MANIFEST_RATIFY"
                 | "CIRCUIT_RESET"  | "SCHEMA_EXTENSION"
                 | "RETENTION_EXTEND" | "PROJECT_CLOSE"
                 | "CORPUS_MANIFEST_SIGN" | "CEREMONY_KEY_ROTATION",
    ceremony_id: UUID,
    ceremony_payload: { ... },        // type-specific body owned by the specialized IC
    operator_id,
    timestamp,
    operator_signature,
    key_ref                           // MUST equal CEREMONY_KEY_ANCHOR
  }
  ```
- **Verifier preconditions (uniform, non-delegable):**
  1. `key_ref` MUST equal the current active `CEREMONY_KEY_ANCHOR` — initial from `genesis-seal.json` OR latest successor from `ceremony-key-rotation-registry/`.
  2. `key_ref` MUST NOT equal `ORCHESTRATOR_KEY_ANCHOR`. Structural exclusion — this is checked before signature validation and before any ceremony-type-specific logic.
  3. Signature valid against the public half at `key_ref`.
  4. Timestamp within 60s of verifier's wall-clock (replay protection, matching IC-HOLD-RELEASE precedent).
  5. `key_ref` not in the revoked/rotated list (rotation registry lookup).
  6. Ceremony-type-specific preconditions delegated to the specialized IC (e.g., TC independent verification for circuit reset; hold_id HELD state for Hold release; scope hash validity for scope update).
- **Failure behaviors (SECURITY category, sync — all escalate to Warden):**
  - `key_ref == ORCHESTRATOR_KEY_ANCHOR` → `CEREMONY_AUTH_WRONG_KEY` — CRITICAL alert: Orchestrator attempted self-authorization.
  - Signature invalid → `CEREMONY_AUTH_SIGNATURE_INVALID`.
  - Stale timestamp → `CEREMONY_AUTH_REPLAY_REJECTED`.
  - `key_ref` in rotation registry's revoked list → `CEREMONY_AUTH_KEY_EXPIRED`.
  - Unknown `key_ref` → `CEREMONY_AUTH_KEY_UNKNOWN`.
  - Missing required envelope field → `CEREMONY_AUTH_MALFORMED`.
- **Relationship to existing ICs:** IC-SCOPE-AUTH-1 is the umbrella authorization contract. All existing and future GOVERNANCE-class ICs delegate authorization to IC-SCOPE-AUTH-1 and specify only their `ceremony_payload` body and type-specific preconditions on top of the common envelope. This preserves the D-CRC-4 unification requirement while allowing specialized ICs to evolve independently on their domain-specific payload schemas.

---

## AMENDMENT — IC-TC-RESET A3 Placeholder Resolved

**Previous state:** IC-TC-RESET specified that write resumption required a "signed reset ceremony" with TC independent precondition verification, but left the signing key unspecified (A3 placeholder per C-CRC-2).

**Amendment:** The reset ceremony authorization key is the Ceremony Authorization Key (CAK) per IC-SCOPE-AUTH-1. The IC-TC-RESET ceremony payload body (type `CIRCUIT_RESET`) is unchanged from v1.1 §11.8.1:
- For `CONSECUTIVE_FAILURE` / `CROSS_TASK_FAILURE` trips: TC verifies compensation `COMPLETED` + overlay hash matches Ledger's most recent `COMMITTED` entry.
- For `DIVERGED_STATE` trips: TC requires `RECONCILIATION_COMPLETE` Ledger entry with `result: "CONSISTENT"` timestamped after the trip.
- For W3 emergency path: reset via W3 is not permitted (unchanged, D84).

The amendment clarifies that human attestation via CAK is NECESSARY but NOT SUFFICIENT — the TC's independent precondition verification is the non-bypassable check regardless of signature validity. This preserves the "ceremony signature is an input, not an override" principle from v1.1 §11.8.1.

**On successful CAK-authorized reset with preconditions met:** TC writes `CIRCUIT_RESET` (GOVERNANCE, sync) and transitions to WRITE_ENABLED. On CAK-authorized reset with preconditions unmet: TC writes `CIRCUIT_RESET_REJECTED` (GOVERNANCE, sync) — already exists in Appendix C.

---

## GAPS PARTIALLY RESOLVED

None.

---

## GAPS DEFERRED

None from the T14 / GAP-26 scope. Follow-on gaps newly surfaced (see below) are deferred by design; the primary gap is fully resolved.

---

## NEW GAPS SURFACED

### G-S4-N1 — First-boot CAK bootstrap tool specification
**Domain:** Orchestration Comparativist (primary), Warden (security review)
**Description:** The ceremony key anchor `CEREMONY_KEY_ANCHOR` in `genesis-seal.json` must be written mint-once by an operator-run bootstrap tool before harness first-boot. The harness itself cannot write this (circular trust — the harness would authorize its own ceremony key). The bootstrap tool must: (a) run with operator credentials outside the harness process identity, (b) accept the operator-generated public key material, (c) write `genesis-seal.json` atomically with hash verification, (d) emit a signed boot manifest the harness verifies at first boot. The tool's trust model, distribution channel, and signing-authority chain are not yet specified.
**Priority:** High (blocks any first-boot flow; currently every session has assumed `genesis-seal.json` is already present).
**Blocked by:** Orchestration capability matrix for bootstrap tooling; Warden review of tool trust model.

### G-S4-N2 — Per-CAK ceremony rate limiting
**Domain:** Warden (primary)
**Description:** If a CAK is briefly exposed (e.g., momentary unlock of HSM, screen capture during signing), an attacker with short-window access could issue many ceremonies rapidly — rotating the CAK, releasing multiple Holds, or issuing a flood of scope updates — before the operator notices. A per-CAK rate limit independent of per-ceremony-type rate limits is needed. Distinct from GAP-27 (scope-update-specific rate limiting).
**Priority:** Medium
**Blocked by:** Warden specification of acceptable ceremony burst patterns; integration with GAP-27 scope work.

### G-S4-N3 — Break-glass emergency channel full specification
**Domain:** Warden (primary)
**Description:** The rotation procedure references a break-glass channel for declared-compromise scenarios (operator emits `CEREMONY_KEY_COMPROMISE_DECLARED`). The channel is currently stubbed as "a second Tier 1 break-glass anchor or out-of-band declaration." Full spec required: is it a second key? An out-of-band Ledger injection path? A pre-signed envelope? What prevents the break-glass channel from becoming a parallel compromise vector? OQ-S-GAP26-5 in canonical OQ list.
**Priority:** Medium (system functions in the non-compromise case; this is a failure-mode gap).
**Blocked by:** Warden design decision; likely a dedicated gap session.

### G-S4-N4 — Multi-operator CAK (m-of-n) deferred; single-operator availability risk
**Domain:** Orchestration Comparativist (primary), Warden
**Description:** v1.1 accepts single-CAK-holder as the baseline. This creates a human-availability risk: key holder on leave, unreachable during incident, or incapacitated. Mitigated in v1.1 by the break-glass channel (G-S4-N3), but multi-operator support (Shamir secret sharing, m-of-n signatures) is a v2 candidate. OQ-S-GAP26-4 canonical.
**Priority:** Low for v1.1 (operational risk accepted with break-glass mitigation); Medium for v2 planning.

---

## NEW TENSIONS SURFACED

### T-S4-N1 — Warden ↔ State Consistency Theorist: rotation registry ordering
The `ceremony-key-rotation-registry/` (Tier 2 append-only) introduces a second anchor-versioning artifact with its own ordering semantics. When a `CEREMONY_KEY_ROTATION` ceremony commits: which anchor governs a ceremony that is mid-verification at the moment of rotation commit? The Warden's position is that the outgoing key governs any ceremony whose verification started before `CEREMONY_KEY_ROTATION_COMPLETE` was written to Ledger, and the successor governs any ceremony whose verification starts after. This requires the same Ledger ordering contract that G-S3-N1 (SCOPE_UPDATED barrier) requires — the barrier problem is now general, not specific to scope updates. State Consistency Theorist input needed to specify the ordering contract uniformly.
**Priority:** High — blocks operational correctness of rotation under concurrent load.
**Resolution path:** Uniform Ledger-barrier contract covering all anchor-versioning ceremonies (SCOPE_UPDATED, CEREMONY_KEY_ROTATION_COMPLETE, and any future anchor-mutating ceremony). Candidate for GS5 or folded into the State Consistency Theorist session handling G-S3-N1.

### T-S4-N2 — Warden ↔ Orchestration Comparativist: bootstrap-tool trust asymmetry
The bootstrap tool (G-S4-N1) runs with operator identity outside the harness and writes the harness's root trust anchor. This inverts the usual direction of trust flow (harness is typically the anchor; here an external tool anchors the harness). Orchestration Comparativist's concern: this tool must be distributable, versionable, and auditable across deployments. Warden's concern: the tool must not itself become a supply-chain attack vector — a compromised bootstrap tool can inscribe an attacker-controlled CAK at first-boot and no subsequent mechanism will detect it. Resolution path: signed bootstrap-tool distribution + out-of-band tool integrity verification by operator before first-boot. Full spec deferred to G-S4-N1 resolution.

---

## ⚠️ STATE CONSISTENCY THEORIST REVIEW REQUIRED

**Trigger conditions fired:** 1, 2, and 3.

**Decisions that triggered the flag:**
- New Ledger event types introduced: `CEREMONY_KEY_ROTATION_COMPLETE`, `CEREMONY_KEY_ROTATION_OVERDUE`, `CEREMONY_KEY_STALE`, `CEREMONY_KEY_COMPROMISE_DECLARED`, `CEREMONY_AUTH_WRONG_KEY`, `CEREMONY_AUTH_SIGNATURE_INVALID`, `CEREMONY_AUTH_REPLAY_REJECTED`, `CEREMONY_AUTH_KEY_EXPIRED`, `CEREMONY_AUTH_KEY_UNKNOWN`, `CEREMONY_AUTH_MALFORMED`. (Condition 1.)
- Common ceremony envelope schema (IC-SCOPE-AUTH-1) changes the structure of GOVERNANCE and SECURITY Ledger entries that carry `operator_signature` — envelope becomes a nested field carrying `ceremony_type`, `ceremony_id`, `key_ref`. (Condition 2.)
- New Tier 1 field (`CEREMONY_KEY_ANCHOR` in `genesis-seal.json`), new Git-committed artifact (`.harness/ceremony-key-anchor.json`), new Tier 2 Sealed Corpus (`ceremony-key-rotation-registry/`). (Condition 3.)

**Specific questions for the State Consistency Theorist:**
1. Is the Ledger ordering contract sufficient to guarantee that a `CEREMONY_KEY_ROTATION_COMPLETE` entry and any in-flight ceremony verifications maintain the "outgoing key governs ceremonies initiated before rotation; successor governs ceremonies initiated after" invariant? This is the same barrier question as G-S3-N1 (SCOPE_UPDATED ↔ commits) generalized to all anchor-versioning ceremonies. Should there be a unified anchor-barrier contract in the Ledger spec?
2. The rotation registry (`ceremony-key-rotation-registry/`) is Tier 2 Sealed Corpus — same pattern as `write-scope-definitions/`. Does its interaction with the State Ledger (which anchor is authoritative for a given commit_ts) require a pointer record in the Ledger at rotation time, or is the Tier 2 append sufficient as the authoritative source?
3. The envelope change to GOVERNANCE/SECURITY Ledger entries — is adding a common `ceremony_envelope` field backward-compatible with v1.1 entries that currently carry flat `operator_signature`? Does this require a Ledger schema version bump?

---

## INTERFACE CONTRACTS TOUCHED

- **IC-SCOPE-AUTH-1** — NEW, ratified this session. Umbrella authorization contract for all GOVERNANCE-class ceremonies.
- **IC-TC-RESET** — AMENDED. A3 placeholder resolved: CAK per IC-SCOPE-AUTH-1 is the reset ceremony authorization key. TC's independent precondition verification unchanged.
- **IC-HOLD-RELEASE** — DELEGATION UPDATE. Authorization layer now delegates to IC-SCOPE-AUTH-1. `ceremony_payload.hold_id`, `hold_type`, `release_reason_code` retained as ceremony-type-specific body. No change to TC-side independent verification of hold state.
- **IC-SCOPE-UPDATE** — DELEGATION UPDATE. Authorization layer now delegates to IC-SCOPE-AUTH-1. Gate verification of `operator_signature` against CAK_ANCHOR replaces the undefined "declared ceremony authorization key" from D90.
- **IC-SCHEMA-EXTEND, IC-LDG-RETAIN, IC-SL8** — DELEGATION UPDATE. All three delegate authorization to IC-SCOPE-AUTH-1.
- **Manifest ratification IC (from GS1)** — DELEGATION UPDATE. Authorization layer now delegates to IC-SCOPE-AUTH-1.

---

## REFINEMENTS TO EXISTING SPEC TEXT

**R-S4-1 — §10.5 extension:** Add a peer section describing the Ceremony Authorization Key in parallel to the Orchestrator Signing Key section. Emphasize that these are distinct keys with distinct storage contracts and distinct authorization scopes.

**R-S4-2 — §13.2 Tier 1 fields:** Add `CEREMONY_KEY_ANCHOR` to the `genesis-seal.json` field list.

**R-S4-3 — §13.3 Tier 2 Sealed Artifacts:** Add `ceremony-key-rotation-registry/` as a second Tier 2 Sealed Corpus. Same governance pattern as `write-scope-definitions/`: append-only, operator-signed, not modifiable by any agent at runtime.

**R-S4-4 — Appendix C (Ledger event types):** Register the ten new event types listed in the State Consistency Theorist review flag. All GOVERNANCE or SECURITY category, sync.

**R-S4-5 — §10.9 and IC-SCOPE-UPDATE text:** Replace "declared ceremony authorization key" with "Ceremony Authorization Key (CAK) per IC-SCOPE-AUTH-1" throughout D90 text.

---

## DECISION LABELS FOR INTEGRATED SPEC

- **D-GAP4-A** (T14 resolution, OQ-S-GAP26-3): Dual-key ceremony authorization model — separate CAK required.
- **D-GAP4-B** (GAP-26 resolution): Unified IC-SCOPE-AUTH-1 governs all GOVERNANCE-class ceremony types (D-CRC-4 satisfied).
- **D-GAP4-C** (OQ-S-GAP26-1): CAK physical storage contract — full four-field specification per table above.
- **D-GAP4-D** (OQ-S-GAP26-2): Rotation cadence 180d recommended / 365d max / 450d degraded-mode.
- **D-GAP4-E** (C-CRC-2): IC-TC-RESET A3 populated.

---

## CARRY-FORWARD TO NEXT SESSION

**Inputs to next gap session:**
- T-S4-N1 (ordering of rotation registry vs. Ledger barriers) should be bundled with G-S3-N1 / R-S3-2 for State Consistency Theorist — they are the same contract generalized. Candidate for GS5.
- G-S4-N1 (bootstrap tool specification) — route to Orchestration Comparativist with Warden security review. High priority.
- G-S4-N2 (per-CAK rate limiting) — Warden-owned, fold into GAP-27 scope when that session runs.
- G-S4-N3 (break-glass channel) — Warden-owned, schedule when security capacity available.
- G-S4-N4 (multi-operator CAK) — v2 backlog; not v1.1.
- Refinements R-S4-1 through R-S4-5 queued for integration pass; not blockers.
- T14 should be marked ✅ RESOLVED on the tension map (v2 → v3 update) with reference to D-GAP4-A and D-GAP4-B.
- GAP-26 should be marked ✅ RESOLVED on the gap backlog with reference to IC-SCOPE-AUTH-1.
- IC-SCOPE-AUTH-1 enters Appendix B as a ratified umbrella interface contract; all delegating ICs need a one-line cross-reference added in the integration pass.

**Unblocked by this session:**
- GAP-27 (rate limit design for scope updates) — no longer blocked by GAP-26; ceremony authorization entity is now defined.
- D90 implementation planning — authorization layer fully specified.
- IC-TC-RESET — A3 placeholder cleared; full ceremony contract now complete.
