# Gap Session 4 Summary — Warden + Orchestration Comparativist
## LLM as Database: Agent Harness Architecture

> **Session:** Gap Session 4 of 12
> **Domain:** AISecOps Specialist / Warden (primary), Orchestration Comparativist (secondary)
> **Topic:** T14 Resolution + GAP-26 Unified Ceremony Authorization Framework
> **Baseline:** v1.1 Integrated Specification + Gap Backlog v2.0
> **Council constraint:** D-CRC-4 — GAP-26 resolution MUST produce a unified ceremony
> authorization framework covering all three ceremony types: manifest ratification (GS1),
> Dependency Hold release (GS2), and scope update ceremony (GS3).
> **Status:** Draft

---

## Session Scope

Five deliverables targeted:

1. **T14 resolution** — determine whether ceremony authorization requires a separate key
   from the Orchestrator first-boot key (OQ-S-GAP26-3). Warden provides security argument;
   Orchestration Comparativist provides operational overhead assessment.
2. **GAP-26 unified ceremony authorization model** — one framework covering all three
   ceremony types per D-CRC-4.
3. **Physical storage contract** — closing OQ-S-GAP26-1 (storage medium) and
   OQ-S-GAP26-2 (retention and rotation cadence).
4. **IC-SCOPE-AUTH-1** — ratified interface contract, generalized from scope-update-only
   to cover all ceremony types.
5. **A3 amendment** — populate the IC-TC-RESET placeholder with the resolved ceremony
   authorization key specification.

---

## Council Session Transcript

*Convened: Warden (primary), Orchestration Comparativist (secondary).*

---

### Topic 1 — T14: Single-Key vs. Dual-Key for Ceremony Authorization

---

🛡️ **WARDEN**

Before I make the security argument, let me establish what we are actually protecting
against. The threat scenario is specific:

> *A Coder Agent is compromised — via prompt injection from external content it was
> tasked to process. The compromised agent has access to the harness filesystem. The
> harness root contains the Orchestrator's signing key at `<harness_root>/.orchestrator-key/`.
> The attacker reads this key and uses it to initiate a scope update ceremony, expanding
> the compromised agent's Write Scope Definition to cover all entity types and all
> relation types. The ceremony is signed with the same key the Gate uses for all
> operational verification. The Gate accepts it. The Orchestrator writes `SCOPE_UPDATED`
> to the Ledger and updates the registry. The compromised agent now has unrestricted write
> authority.*

This is not a theoretical scenario. Prompt injection into write-authorized agents is
Risk #5 in the Warden skill's key risk catalog. The Orchestrator key (`§10.5`) is
**machine-generated** and stored **on the filesystem** by design — it must be accessible
programmatically for write token issuance. Filesystem access is a realistic attacker
surface for a compromised agent running in the same process environment.

If the Orchestrator's Operational Key (OOK) also serves as the ceremony authorization
key, then physical security of the entire ceremony authorization layer reduces to:
*filesystem access controls*. That is not a governance boundary — it is an operational
boundary, and it can be crossed by the same class of attack that the harness already
assumes is possible (Risk #5).

The correct model: ceremony authorization must require a **human physical action** that
cannot be replicated by a compromised process. A key that is machine-held on the filesystem
cannot enforce this requirement. Therefore, the ceremony authorization key MUST be
separate from the OOK.

**Security argument summary:** A single-key model collapses governance authority into
operational authority. A compromised Orchestrator — or any process with filesystem read
access — can authorize its own scope changes. The dual-key hierarchy is not a preference;
it is the minimum trust boundary capable of surviving an OOK-level filesystem compromise.

---

🔀 **ORCHESTRATION COMPARATIVIST**

The Warden's argument is sound. My concern is the operational overhead model — specifically
whether a human-held key creates a de facto availability bottleneck for a system that may
need to execute governance ceremonies under pressure (for example, a circuit reset ceremony
following a midnight incident).

Let me quantify the overhead against the ceremony frequency:

| Ceremony Type | Expected Frequency | Urgency Profile |
|---|---|---|
| Manifest ratification (GS1) | Once per `.larql` schema version advance | Low urgency — planned governance event |
| Dependency Hold release (GS2) | Once per Genesis lifecycle (project init or reset) | Medium urgency — blocks system restart |
| Scope update ceremony (GS3) | Bounded by `scope_update_min_interval_seconds` (≥3,600 s per D89) | Variable — could be urgent if scope error discovered |

None of these are per-write operations. The highest-frequency ceremony (scope update) is
rate-limited to at most once per hour per agent. The most urgent (circuit reset) may occur
at unpredictable times.

**Conclusion:** The overhead is acceptable IF and only IF the physical storage contract
for the CAK does not require a specific human's physical presence. An operator-on-call
model with the CAK on a hardware security token (which can travel with the on-call
engineer) or on encrypted removable media stored in a physically accessible location
(not a bank vault requiring business-hours access) satisfies both the Warden's isolation
requirement and the operational availability requirement.

The single-key model is not worth the risk. The dual-key hierarchy is accepted, with the
constraint that the CAK storage contract explicitly addresses the availability requirement
for unplanned ceremonies (circuit reset in particular).

---

**T14 RESOLUTION — D92**

> **D92:** The ceremony authorization key (CAK) is a separate key from the Orchestrator
> Operational Key (OOK). Two distinct key hierarchies govern the harness:
>
> - **Orchestrator Operational Key (OOK):** Machine-generated at first boot. Private half
>   stored at `<harness_root>/.orchestrator-key/`. Authorizes operational writes: write
>   token issuance, agent invocation signatures, and routine Ledger entries. Key scope is
>   operational and runtime-continuous.
> - **Ceremony Authorization Key (CAK):** Human-generated. Human-held. Physical presence
>   or PIN required for signing. Authorizes all governance ceremonies (manifest
>   ratification, Dependency Hold release, scope update, circuit reset). Key scope is
>   governance-only and episodic.
>
> The CAK public key is registered in Tier 1 `genesis-seal.json` at first-boot as
> `ceremony_authorization_key_anchor`. This registration is immutable post-genesis.
> OQ-S-GAP26-3 is closed.

---

### Topic 2 — GAP-26: Unified Ceremony Authorization Framework (D-CRC-4)

---

🛡️ **WARDEN**

With T14 resolved, the framework can now be specified. D-CRC-4 requires the same key
hierarchy and verification procedure across all three ceremony types. The correct
structure is a **unified ceremony token envelope** — a canonical signed object that
all ceremony processors consume identically, with a `ceremony_type` discriminator
field for ceremony-specific payload.

This avoids three separate verification procedures that could drift in security guarantees.
One verification path means one code path to audit.

---

🔀 **ORCHESTRATION COMPARATIVIST**

Agreed. A unified token envelope also simplifies the orchestration logic: any ceremony
initiation produces a token of the same structural form, and the ceremony processor
dispatches on `ceremony_type` after signature verification — not before. This prevents
ceremony-type-specific bypass attacks (e.g., crafting a HOLD_RELEASE token with a
SCOPE_UPDATE header to confuse a processor that checks type before verifying the
signature).

The ceremony_id field is critical for replay protection and I want it in the base
envelope, not ceremony-specific. Duplicate ceremony_id detection must span ceremony types.

---

**UNIFIED CEREMONY TOKEN ENVELOPE — D93**

> **D93:** All governance ceremonies in the harness consume a unified ceremony token
> envelope. The canonical structure is:
>
> ```
> CeremonyToken {
>   ceremony_type:    MANIFEST_RATIFICATION | HOLD_RELEASE | SCOPE_UPDATE | CIRCUIT_RESET
>   ceremony_id:      UUID — unique per ceremony invocation; replay-detection scope: 24 hours
>   operator_id:      Identifier matching CAK registration in genesis-seal.json
>   timestamp:        ISO 8601 — verified within 60 seconds of receipt (replay protection)
>   key_ref:          CAK fingerprint — identifies which registered CAK signed this token
>   payload:          Ceremony-type-specific fields (see §2.1–2.4 below)
>   operator_signature: Signature over canonical JSON of all fields except this one
> }
> ```
>
> Verification procedure (same for all ceremony types):
> 1. Verify `timestamp` is within 60 seconds of current time. If stale →
>    `CEREMONY_REPLAY_REJECTED` (SECURITY, sync); halt.
> 2. Verify `ceremony_id` has not been seen within the past 24 hours. If duplicate →
>    `CEREMONY_REPLAY_REJECTED` (SECURITY, sync); halt.
> 3. Resolve `key_ref` against `genesis-seal.json::ceremony_authorization_key_anchor`.
>    If `key_ref` unknown → `CEREMONY_SIGNATURE_INVALID` (SECURITY, sync); halt.
> 4. Verify `operator_signature` against resolved public key. If invalid →
>    `CEREMONY_SIGNATURE_INVALID` (SECURITY, sync); halt.
> 5. Verify `operator_id` matches the identity registered at `key_ref`. If mismatch →
>    `CEREMONY_SIGNATURE_INVALID` (SECURITY, sync); halt.
> 6. Dispatch to ceremony-type-specific processor with verified payload.
>
> Steps 1–5 execute in order. Step 6 executes only if steps 1–5 all pass. No
> ceremony-type-specific logic executes before signature verification completes.

---

#### §2.1 — Manifest Ratification Ceremony Payload

```
payload {
  manifest_hash:    SHA-256 of larql_migration_manifest body
  manifest_version: Target version string (e.g., "1.1→2.0")
  ratification_note: Human-authored rationale (free text, max 500 chars)
}
```

Producing component: Human operator (ratifying machine-drafted migration manifest per
GS1 outline spec block 2a). Consuming component: Orchestrator (manifest commit gate).

---

#### §2.2 — Dependency Hold Release Ceremony Payload

```
payload {
  hold_id:           Hold Registry entry ID
  hold_type:         GENESIS_HOLD | DEPENDENCY_HOLD
  release_reason:    TIMEOUT_NO_RETRY | GENESIS_RESET_PREPARATION | OPERATOR_OVERRIDE
  preconditions_ref: Ledger entry ID confirming preconditions verified (TC-generated)
}
```

Producing component: Human operator (executing Hold release per IC-HOLD-RELEASE).
Consuming component: Transaction Controller (Hold Registry). Amendment to IC-HOLD-RELEASE:
`key_ref` in the existing contract now resolves to `ceremony_authorization_key_anchor`
(previously under-specified). Failure events `HOLD_RELEASE_SIGNATURE_INVALID` and
`HOLD_RELEASE_REPLAY_REJECTED` are superseded by unified `CEREMONY_SIGNATURE_INVALID`
and `CEREMONY_REPLAY_REJECTED` (with `ceremony_type: HOLD_RELEASE`). IC-HOLD-RELEASE
is amended accordingly.

---

#### §2.3 — Scope Update Ceremony Payload

```
payload {
  agent_id:            Target agent whose Write Scope Definition is being updated
  previous_scope_hash: SHA-256 of current Write Scope Definition YAML
  new_scope_hash:      SHA-256 of replacement Write Scope Definition YAML
  scope_change_type:   EXPANDING | NARROWING | RESTRUCTURING
}
```

Producing component: Human operator. Consuming component: Orchestrator (scope registry
processor). This payload satisfies the D90 `operator_signature` verification requirement
and the `expected_yaml_hash` update requirement. `scope_change_type` resolves
OQ-S-GAP27-1 (carry-forward from GS3) as a required payload field — Orchestrator may
apply per-type notification policy at its discretion.

---

#### §2.4 — Circuit Reset Ceremony Payload

```
payload {
  trip_entry_id:       Ledger entry ID of the CIRCUIT_TRIPPED event being reset
  preconditions_verified: Boolean (true only — TC independently re-verifies;
                           this field is a human attestation supplement, not sole authority)
  reset_rationale:     Human-authored rationale (free text, max 500 chars)
}
```

Producing component: Human operator (initiating circuit reset per §11.8.1).
Consuming component: Transaction Controller. This payload population is the **A3
amendment** to IC-TC-RESET. TC verification of the ceremony token (steps 1–5 of
the unified procedure) is required before TC precondition re-verification proceeds —
an OOK-signed token MUST be rejected at step 3 (key_ref not matching CAK anchor).

---

### Topic 3 — Physical Storage Contract for CAK (OQ-S-GAP26-1, OQ-S-GAP26-2)

---

🛡️ **WARDEN**

The CAK physical storage contract must answer all four required fields. I will specify
them now.

**Storage medium (OQ-S-GAP26-1):**

Two acceptable storage classes, in preference order:

1. **Hardware Security Token (preferred):** FIDO2 or PKCS#11-compatible device. Private
   key is generated on-device and non-exportable. Signing requires physical presence
   (button press) or PIN. Device must not be left permanently connected to any networked
   machine. The public key is exported at registration time and stored in
   `genesis-seal.json::ceremony_authorization_key_anchor`.

2. **Encrypted Offline Key File (acceptable fallback):** Private key stored in a
   strongly-encrypted file (encryption algorithm and key derivation function are
   implementation-specific; this spec does not prescribe). File stored on removable media
   (USB drive) physically secured in an operator-accessible location (not restricted to
   business-hours access — see OC's availability requirement above). Passphrase must not
   be stored on any networked system. File must not be copied to the harness filesystem.

**Filesystem storage of CAK private key material is explicitly prohibited** (C-CAK-1).
Any first-boot procedure that generates and stores the CAK on the harness filesystem
MUST be rejected as a spec violation regardless of subsequent deletion.

---

🔀 **ORCHESTRATION COMPARATIVIST**

The hardware token preference is correct. I want to document one operational constraint:
the on-call engineer must have physical access to the CAK storage medium for unplanned
ceremonies (circuit reset in particular). The first-boot registration ceremony must
therefore designate at minimum one backup custodian — a second individual who can access
the CAK or a second registered CAK — to avoid single-person key availability failures.

This is an operational requirement, not a spec mechanism. For v1 it is documented as a
deployment risk (OQ-S-CAK-2 addresses multi-operator quorum as a v2 mechanism).

---

**D94 — CAK Physical Storage Contract**

> **D94:** Physical storage contract for the Ceremony Authorization Key (CAK):
>
> | Field | Specification |
> |---|---|
> | **Storage medium** | Hardware Security Token (FIDO2/PKCS#11, preferred) or encrypted offline key file on removable media (acceptable fallback). Filesystem storage of CAK private key material is prohibited (C-CAK-1). |
> | **Governance tier** | `human-approved-change` — no agent or Orchestrator component may read, modify, or replace the CAK registration. Key registration is a one-time first-boot ceremony. |
> | **Retention rule** | CAK private key is retained until explicit v2 key rotation ceremony (OQ-S-CAK-1) or confirmed key compromise event. On compromise: CAK is immediately revoked; system halts pending manual re-genesis or v2 rotation ceremony; `CAK_COMPROMISE_DECLARED` Ledger entry (SECURITY, sync) is written by the Orchestrator on operator notification. CAK registration in `genesis-seal.json` is immutable (Tier 1, mint-once); a compromised key requires v2 re-genesis or rotation protocol. |
> | **Write authority** | Human operator only, out-of-band to the harness. The CAK private key is never read by any harness component. Only the signed ceremony token it produces is consumed by harness verification logic. |
>
> OQ-S-GAP26-1 is closed by this contract.
> OQ-S-GAP26-2 is partially closed: retention rule is specified; rotation cadence is
> deferred to v2 (OQ-S-CAK-1). No automated rotation in v1.

---

### Topic 4 — IC-SCOPE-AUTH-1 Ratification

IC-SCOPE-AUTH-1 was produced as a skeleton in GS3. With the unified ceremony token
envelope established (D93) and the CAK physical storage contract specified (D94), the
contract can now be ratified in its generalized form.

**D95:** IC-SCOPE-AUTH-1 is ratified as the Unified Ceremony Authorization Framework
interface contract. Its scope extends from scope-update-only (GS3 skeleton) to all four
ceremony types. See Interface Contracts section below for the ratified text.

---

### Topic 5 — A3 Amendment to IC-TC-RESET

**D96:** The A3 placeholder in §11.8.1 IC-TC-RESET is populated as follows:

> *Amendment A3 to §11.8.1:*
>
> "The signed reset ceremony required by IC-TC-RESET MUST be a ceremony token with
> `ceremony_type: CIRCUIT_RESET`, signed by the CAK registered in
> `genesis-seal.json::ceremony_authorization_key_anchor`. The TC executes the five-step
> unified verification procedure (D93) against the ceremony token before performing any
> precondition verification. An OOK-signed ceremony token submitted for circuit reset is
> rejected at verification step 3 — `CEREMONY_SIGNATURE_INVALID` (SECURITY, sync) is
> written; no reset proceeds. Precondition verification (D84) executes only after the
> ceremony token passes all five verification steps. Human attestation in the ceremony
> payload is a supplement to TC precondition verification, not a substitute. (D92, D93,
> D95, D96, C-CAK-4)"

---

## Spec Blocks

---

### Ceremony Authorization Key (CAK) — Spec Block

**Specialist provenance:** Warden (primary), Orchestration Comparativist (secondary)

**What it must enforce:**

The CAK is the sole signing authority for all governance ceremonies in the harness. Its
physical separation from the OOK ensures that a compromised machine process cannot
self-authorize governance actions, including scope expansions, Hold releases, schema
version advances, or circuit resets.

**Threat scenario it defends against:**

A compromised Coder Agent or external attacker with filesystem access obtains the OOK
private key. With OOK authority, the attacker attempts to authorize a scope update
ceremony to expand the compromised agent's Write Scope Definition to unrestricted.
The Gate's ceremony verification resolves `key_ref` against
`genesis-seal.json::ceremony_authorization_key_anchor` (the CAK anchor, not the OOK
anchor). Verification step 3 fails — `key_ref` does not match the registered CAK
fingerprint. `CEREMONY_SIGNATURE_INVALID` is written. No scope update proceeds.
The attack is blocked at the verification layer regardless of OOK compromise.

**Hard constraints:**

- C-CAK-1: CAK private key material MUST NOT reside on the harness filesystem at any
  point — including during generation, registration, or use.
- C-CAK-2: CAK public key is registered in `genesis-seal.json::ceremony_authorization_key_anchor`
  at first-boot. This registration is immutable (Tier 1, mint-once). No runtime
  modification of the anchor is permitted.
- C-CAK-3: Ceremony tokens are replay-protected. `timestamp` MUST be within 60 seconds
  of verification time. `ceremony_id` MUST be unique within the past 24 hours across all
  ceremony types. Both checks execute before signature verification proceeds.
- C-CAK-4: The OOK MUST NOT be accepted as a ceremony authorization key for any of the
  four ceremony types. Any ceremony token whose `key_ref` resolves to the OOK anchor
  rather than the CAK anchor MUST be rejected with `CEREMONY_SIGNATURE_INVALID`.
- C-CAK-5: Ceremony token verification (steps 1–5 of the unified procedure, D93) MUST
  complete before any ceremony-type-specific processing begins. No ceremony-specific
  payload is read or acted upon prior to full signature verification.

**Immutability requirements:**

`genesis-seal.json::ceremony_authorization_key_anchor` is immutable post-genesis per
Tier 1 (mint-once, never modified). The Ledger entry `CAK_REGISTERED` (GOVERNANCE,
sync) is written at first-boot on CAK anchor registration and is not modifiable.
CAK private key replacement requires v2 key rotation ceremony (OQ-S-CAK-1).

**Audit trail requirements:**

Every ceremony token evaluation — regardless of outcome — produces a synchronous
Ledger entry:

| Event | Category | Trigger |
|---|---|---|
| `CEREMONY_ACCEPTED` | GOVERNANCE | All 5 verification steps passed |
| `CEREMONY_SIGNATURE_INVALID` | SECURITY | Steps 3, 4, or 5 fail |
| `CEREMONY_REPLAY_REJECTED` | SECURITY | Steps 1 or 2 fail |
| `CAK_REGISTERED` | GOVERNANCE | First-boot CAK anchor registration |
| `CAK_COMPROMISE_DECLARED` | SECURITY | Operator notifies harness of CAK compromise |

All entries carry: `ceremony_type`, `ceremony_id`, `operator_id`, `key_ref`,
`verification_step_failed` (for failure events), `timestamp`.

**Authorization model:**

CAK is the sole signing authority for governance ceremonies. No agent, no Orchestrator,
and no automated process is authorized to sign ceremony tokens. The Orchestrator's role
is verification and dispatch — not signing.

**Failure behavior:**

- `CEREMONY_SIGNATURE_INVALID` → ceremony halted; no state changes; Warden alerted;
  entry written to Ledger; rejection payload returned to initiator.
- `CEREMONY_REPLAY_REJECTED` → same as above; additionally, three replay rejections
  within one hour for the same `operator_id` trigger `CEREMONY_REPLAY_THRESHOLD_EXCEEDED`
  (SECURITY, sync) and Warden escalation.
- `CAK_COMPROMISE_DECLARED` → system transitions to MAINTENANCE mode; all ceremony
  processing suspended; operator must execute v2 CAK rotation ceremony or re-genesis
  before ceremonies resume. This transition is irreversible by any automated process.

**Open questions (deferred):**

- OQ-S-CAK-1: v2 CAK rotation ceremony design — how is the CAK replaced without
  re-genesis? Tier 1 `genesis-seal.json` is mint-once; a rotation mechanism requires
  a v2 extension protocol for Tier 1 governed artifacts.
- OQ-S-CAK-2: Multi-operator quorum model — for high-availability deployments, can
  an m-of-n threshold signing scheme replace a single CAK? What orchestration
  requirements does this impose on ceremony initiation?
- OQ-S-CAK-3: Escalation path for `CEREMONY_REPLAY_THRESHOLD_EXCEEDED` — does the
  harness attempt to notify an out-of-band channel (e.g., operator pager) when this
  event fires, and if so, what is the notification contract?

**Interface contract:**

See IC-SCOPE-AUTH-1 (ratified, D95) and Amendment to IC-HOLD-RELEASE below.

**Non-goals:**

- This spec block does not specify the CAK's cryptographic algorithm or key length
  (implementation-specific; must satisfy applicable security standards at deployment time).
- This spec block does not specify the hardware token vendor or PKCS#11 implementation.
- This spec block does not specify multi-operator quorum (v2, OQ-S-CAK-2).

---

### Unified Ceremony Authorization Framework — Spec Block

**Specialist provenance:** Warden (primary), Orchestration Comparativist (secondary)

**What it must do:**

Provide a single verification path and a single token structure for all four ceremony
types in the harness. Ceremony-specific logic executes only after the unified verification
path completes. This eliminates per-ceremony bypass surfaces and produces a consistent
audit trail regardless of ceremony type.

**Hard constraints:**

- C-CRC-4: All ceremony types MUST use the unified ceremony token envelope (D93).
  A ceremony-type-specific verification procedure that deviates from D93 steps 1–5
  is a spec violation.
- C-CRC-5: `ceremony_id` uniqueness MUST be checked across ceremony types. A
  `ceremony_id` that appeared in a SCOPE_UPDATE ceremony cannot be reused in a
  HOLD_RELEASE ceremony within the 24-hour replay detection window.
- C-CRC-6: Ceremony token verification produces a Ledger entry regardless of outcome.
  A ceremony that fails verification silently (no Ledger entry written) is a spec
  violation and must be treated as a harness integrity failure.

**Tradeoffs decided:**

- Unified failure events (`CEREMONY_SIGNATURE_INVALID`, `CEREMONY_REPLAY_REJECTED`)
  replace the GS2 ceremony-type-specific events (`HOLD_RELEASE_SIGNATURE_INVALID`,
  `HOLD_RELEASE_REPLAY_REJECTED`). This trades backward compatibility (existing Appendix C
  entries) for a consistent audit trail schema. The superseded events are marked as
  deprecated in Appendix C; new Ledger implementations MUST emit the unified types.
  Existing implementations may emit either until the next spec version.
- Ceremony-type-specific payload fields are isolated inside the `payload` field.
  Ceremony processor dispatch occurs after unified verification, not before. This was
  chosen over a type-first dispatch model to prevent type-spoofing attacks.

**Open questions (deferred):**

- OQ-S-CAK-3: Replay threshold escalation path (same as CAK spec block, above).
- GAP-27 (OQ-S-GAP26-2 rate limiting): The `scope_update_min_interval_seconds`
  rate limit applies to SCOPE_UPDATE ceremonies. Rate limiting for other ceremony types
  is not specified in v1 and is deferred to v2. GAP-27 (rate limit design for SCOPE_UPDATED
  events) is now unblocked by this session's GAP-26 resolution.

**Interface contract:**

See IC-SCOPE-AUTH-1 (ratified) below.

**Non-goals:**

- This spec block does not specify the implementation language or framework for the
  unified verification procedure.
- This spec block does not govern operational ceremonies outside the harness (e.g., CAK
  registration during first-boot is a pre-harness human action, not a harness-enforced
  ceremony).

---

## Interface Contracts

---

### IC-SCOPE-AUTH-1 — Unified Ceremony Authorization Framework (Ratified, D95)

```
INTERFACE CONTRACT IC-SCOPE-AUTH-1 (Ratified — Gap Session 4):
  From: Ceremony Token Processor (Orchestrator-embedded component)
  To: Ceremony-type-specific processor (Scope Registry | Transaction Controller |
      Manifest Commit Gate)
  Specialists: Warden (primary), Orchestration Comparativist (secondary)

  What A exposes:
    Verified ceremony dispatch: after completing D93 verification steps 1–5 against
    a CeremonyToken, the Ceremony Token Processor delivers a verified payload to the
    appropriate downstream processor. The downstream processor receives ONLY the
    ceremony_type and payload fields — verification metadata (key_ref, operator_signature,
    timestamp, ceremony_id) is consumed by the verifier and NOT forwarded.

    Failure events emitted directly to State Ledger on verification failure:
      CEREMONY_SIGNATURE_INVALID  (SECURITY, sync) — verification steps 3, 4, or 5 failed
      CEREMONY_REPLAY_REJECTED    (SECURITY, sync) — verification steps 1 or 2 failed

    Success event emitted to State Ledger on verification pass:
      CEREMONY_ACCEPTED           (GOVERNANCE, sync) — all 5 steps passed;
                                  carries ceremony_type, ceremony_id, operator_id

  Conditions:
    (a) Verification steps execute in order 1 through 5 per D93.
    (b) No payload field is read prior to completion of step 5.
    (c) key_ref MUST resolve to genesis-seal.json::ceremony_authorization_key_anchor.
        A key_ref that resolves to the OOK anchor triggers CEREMONY_SIGNATURE_INVALID
        regardless of signature validity.
    (d) For SCOPE_UPDATE ceremony type: rate limit check (D89,
        scope_update_min_interval_seconds) executes BEFORE ceremony token verification
        (i.e., before step 1). Rate limit failure → SCOPE_UPDATE_RATE_EXCEEDED
        (SECURITY, sync); ceremony token not evaluated.
    (e) Downstream processors MUST independently verify that their preconditions are
        satisfied after receiving a verified payload. IC-SCOPE-AUTH-1 guarantees only
        that the ceremony was authorized — not that the preconditions for the ceremony
        action are met.

  Failure behavior:
    CEREMONY_SIGNATURE_INVALID → ceremony token rejected; no downstream dispatch;
    Ledger entry written; rejection reason returned to initiator; Warden alerted.
    CEREMONY_REPLAY_REJECTED → same as above; if threshold exceeded (3 within 1 hour
    for same operator_id) → CEREMONY_REPLAY_THRESHOLD_EXCEEDED (SECURITY, sync);
    Warden escalation.
    If Ledger write fails during failure event emission → ceremony processing halts
    entirely; no partial state is written; Orchestrator surfaces write failure to
    operator; no ceremony action proceeds.
```

---

### Amendment to IC-HOLD-RELEASE (CAK Specification, D92/D95)

The existing IC-HOLD-RELEASE contract (Warden skill, GAP-21) specifies `key_ref` in
the Hold release token as "key_ref in Tier 1 anchor" — previously under-specified.

**Amendment:** `key_ref` MUST resolve to `genesis-seal.json::ceremony_authorization_key_anchor`
(the CAK anchor, not the OOK anchor). Verification of Hold release tokens now executes
via the unified five-step procedure of D93 rather than the previously-implicit
ceremony-specific check. Failure events `HOLD_RELEASE_SIGNATURE_INVALID` and
`HOLD_RELEASE_REPLAY_REJECTED` are superseded by unified `CEREMONY_SIGNATURE_INVALID`
and `CEREMONY_REPLAY_REJECTED` (with `ceremony_type: HOLD_RELEASE`). The rest of
IC-HOLD-RELEASE (Hold Registry transition, precondition verification by TC) is unchanged.

---

### Amendment to IC-TC-RESET (A3 Population, D96)

```
Amendment A3 to §11.8.1 IC-TC-RESET:

  The signed reset ceremony MUST be a CeremonyToken with ceremony_type: CIRCUIT_RESET.
  The TC executes the unified five-step verification procedure (D93) against the ceremony
  token. Verification executes BEFORE TC precondition re-verification (D84).

  OOK-signed tokens: rejected at step 3 (key_ref does not match CAK anchor) →
    CEREMONY_SIGNATURE_INVALID (SECURITY, sync); no reset proceeds.

  Precondition re-verification (D84 — compensation COMPLETED, overlay hash match,
  RECONCILIATION_COMPLETE if DIVERGED_STATE trip) executes only after steps 1–5 pass.

  Human attestation in ceremony payload (preconditions_verified: true) is a supplement
  to TC precondition re-verification. TC MUST independently re-verify preconditions
  regardless of this field value. A ceremony token where preconditions_verified: true
  but TC re-verification fails → reset rejected; CIRCUIT_RESET_REJECTED (SECURITY, sync);
  CEREMONY_ACCEPTED (GOVERNANCE, sync) is still written (the ceremony was authorized —
  it is the preconditions that failed, not the authorization).

  (D84, D92, D93, D95, D96, C-CAK-4, C-CAK-5)
```

---

## Decisions Made

| ID | Decision | Closes |
|---|---|---|
| D92 | Dual-key hierarchy established: CAK (human-held, governance) and OOK (machine-held, operational) are separate keys. OOK MUST NOT authorize governance ceremonies. | OQ-S-GAP26-3, T14 |
| D93 | Unified Ceremony Token Envelope: canonical CeremonyToken structure and five-step verification procedure covering all four ceremony types. | D-CRC-4 (primary mechanism) |
| D94 | CAK physical storage contract: hardware security token preferred; encrypted offline media acceptable; filesystem storage prohibited. Governance tier: human-approved-change. Retention: until v2 rotation ceremony. Write authority: human operator only. | OQ-S-GAP26-1 (full close), OQ-S-GAP26-2 (partial close — rotation deferred to v2) |
| D95 | IC-SCOPE-AUTH-1 ratified as Unified Ceremony Authorization Framework interface contract; scope expanded from scope-update-only to all four ceremony types. | GAP-26 |
| D96 | A3 amendment to §11.8.1 IC-TC-RESET populated: CAK is the authorizing key for circuit reset ceremonies; OOK-signed reset tokens rejected at verification step 3. | IC-TC-RESET A3 placeholder |

---

## Constraints Established

| ID | Constraint |
|---|---|
| C-CAK-1 | CAK private key material MUST NOT reside on the harness filesystem at any point. |
| C-CAK-2 | CAK public key is registered in `genesis-seal.json::ceremony_authorization_key_anchor` at first-boot; immutable post-genesis. |
| C-CAK-3 | Ceremony tokens are replay-protected: `timestamp` within 60 seconds of verification; `ceremony_id` unique within 24 hours across all ceremony types. |
| C-CAK-4 | OOK MUST NOT be accepted as ceremony authorization for any ceremony type. |
| C-CAK-5 | Unified five-step verification (D93) completes before any ceremony-type-specific payload processing. |
| C-CRC-4 | All ceremony types MUST use the unified ceremony token envelope (D93). Ceremony-type-specific verification deviations are a spec violation. |
| C-CRC-5 | `ceremony_id` uniqueness is checked across ceremony types within the 24-hour replay detection window. |
| C-CRC-6 | Every ceremony token evaluation produces a Ledger entry regardless of outcome. Silent failure is a harness integrity violation. |

---

## OQ Status Table

| OQ ID | Question | Status | Resolution |
|---|---|---|---|
| OQ-S-GAP26-3 | Must CAK be separate from OOK? | ✅ Closed | D92 — dual-key hierarchy; CAK MUST be separate |
| OQ-S-GAP26-1 | Where is CAK stored, under what physical storage contract? | ✅ Closed | D94 — hardware token preferred; encrypted offline media acceptable; filesystem prohibited |
| OQ-S-GAP26-2 | Retention and rotation cadence for CAK? | 🔶 Partial | D94 — retention specced; rotation deferred to v2 (OQ-S-CAK-1) |
| OQ-S-GAP27-1 | Should `SCOPE_UPDATED` carry `scope_change_type`? | ✅ Closed | D93 §2.3 — `scope_change_type: EXPANDING\|NARROWING\|RESTRUCTURING` added to SCOPE_UPDATE ceremony payload as required field |
| OQ-S-CAK-1 | v2 CAK rotation ceremony design | 🟡 Open (v2) | Deferred — rotation requires v2 extension protocol for Tier 1 artifacts |
| OQ-S-CAK-2 | Multi-operator quorum / m-of-n signing | 🟡 Open (v2) | Deferred — v2 high-availability deployment concern |
| OQ-S-CAK-3 | Escalation path for `CEREMONY_REPLAY_THRESHOLD_EXCEEDED` | 🟡 Open | Blocked by GAP-16 (notification channel design — deployment-specific) |

---

## New Ledger Entry Types Required

| Entry Type | Category | Mode | Trigger | Supersedes |
|---|---|---|---|---|
| `CEREMONY_ACCEPTED` | GOVERNANCE | Sync | All 5 verification steps passed | — |
| `CEREMONY_SIGNATURE_INVALID` | SECURITY | Sync | Verification steps 3, 4, or 5 fail | `HOLD_RELEASE_SIGNATURE_INVALID` (deprecated) |
| `CEREMONY_REPLAY_REJECTED` | SECURITY | Sync | Verification steps 1 or 2 fail | `HOLD_RELEASE_REPLAY_REJECTED` (deprecated) |
| `CEREMONY_REPLAY_THRESHOLD_EXCEEDED` | SECURITY | Sync | 3+ CEREMONY_REPLAY_REJECTED for same operator_id within 1 hour | — |
| `CAK_REGISTERED` | GOVERNANCE | Sync | First-boot CAK anchor registration | — |
| `CAK_COMPROMISE_DECLARED` | SECURITY | Sync | Operator notifies harness of CAK compromise | — |

All entries carry: `ceremony_type`, `ceremony_id`, `operator_id`, `key_ref`, `timestamp`.
Failure entries additionally carry: `verification_step_failed` (integer 1–5).
All entries must be added to Appendix C of the v1.1 integrated spec.

---

## New Gaps Surfaced

None. This session produced no previously-uncatalogued gaps. The CAK rotation question
(OQ-S-CAK-1) falls within the existing scope of GAP-19 (Warden, Low, Deferred to v2 —
"Orchestrator signing key rotation. First-boot key is not rotated in v1. Full PKI is v2
scope.") GAP-19's scope is hereby extended to cover CAK rotation in addition to OOK
rotation.

---

## New Tensions Surfaced

---

### T15 — CAK Availability vs. Ceremony Urgency

**Status:** Open — documented risk; v2 resolution path identified
**Specialists:** Warden + Orchestration Comparativist

**Core conflict:** A single human-held CAK creates an availability bottleneck. If the
designated CAK custodian is unavailable (illness, travel, off-hours incident), urgent
governance ceremonies (in particular, circuit reset after a midnight incident) cannot
execute. This is a single point of failure in the governance ceremony chain.

**v1 disposition:** Documented operational risk. The CAK physical storage contract (D94)
requires that the CAK storage medium be accessible to on-call personnel — not locked to
a single individual's physical possession. Operators MUST designate a backup custodian
at first-boot as an operational requirement (not enforced by the spec mechanism).

**v2 resolution path:** Multi-operator quorum signing (OQ-S-CAK-2) — threshold signature
scheme allowing m-of-n designated operators to co-sign ceremony tokens. Resolves the
single-custodian availability failure without introducing a machine-held key.

---

## Spec Amendments Required

### §13.2 — Tier 1 `genesis-seal.json` (mint-once, never modified)

Add field: `ceremony_authorization_key_anchor` — SHA-256 fingerprint of CAK public key
plus public key material (PEM). Written at first-boot during CAK registration ceremony.
Immutable post-genesis. (D92, D94, C-CAK-2)

### §10.9 — Scope Update Ceremony (D87, D90)

Replace: "The entry carries `operator_signature`..."
With: "The entry carries a verified CeremonyToken (ceremony_type: SCOPE_UPDATE) per the
unified ceremony authorization framework (D93, IC-SCOPE-AUTH-1). `operator_signature`
in the Ledger entry is the signature field from the verified CeremonyToken."

### Appendix C — Ledger Entry Type Catalog

Add all six new entry types listed above. Mark `HOLD_RELEASE_SIGNATURE_INVALID` and
`HOLD_RELEASE_REPLAY_REJECTED` as deprecated; reference unified replacements.

### GAP-19 Scope Extension

GAP-19 scope extended from "Orchestrator signing key rotation only" to "OOK and CAK
rotation — Full PKI is v2 scope." Both keys share the v2 rotation deferral.

---

## ⚠️ STATE CONSISTENCY THEORIST REVIEW REQUIRED

```
⚠️ STATE CONSISTENCY THEORIST REVIEW REQUIRED

Trigger: Condition 1 — decisions affect what is recorded in the State Ledger
         (six new entry types introduced; two existing entries deprecated and superseded;
         CAK_REGISTERED ties Tier 1 genesis-seal.json to a new Ledger event at first-boot)
         Condition 3 — D94 places CAK registration in Tier 1 genesis-seal.json
         (mint-once, §13.2 artifact), adding a new field that intersects config
         governance at the highest immutability tier.

Decision that triggered it (Condition 1):
  D93/D95 introduce six new Ledger entry types. CEREMONY_SIGNATURE_INVALID and
  CEREMONY_REPLAY_REJECTED supersede two entries already in the spec
  (HOLD_RELEASE_SIGNATURE_INVALID, HOLD_RELEASE_REPLAY_REJECTED from GS2).
  The State Consistency Theorist must confirm:
  (a) Existing Ledger implementations that emit deprecated entry types do not create
      a Merkle-chain-lite integrity gap when entries with the new unified types are
      interleaved in the log.
  (b) CEREMONY_ACCEPTED carries ceremony_id and operator_id — confirm these fields do
      not create implicit foreign-key expectations that complicate append-only semantics.

Decision that triggered it (Condition 3):
  D94 adds ceremony_authorization_key_anchor to genesis-seal.json (Tier 1, mint-once).
  The State Consistency Theorist must confirm:
  (a) This addition does not conflict with the genesis-seal.json field set already
      specified at §13.2, and does not require a schema versioning mechanism for Tier 1
      artifacts (Tier 1 is currently unversioned by spec).
  (b) The CAK_REGISTERED Ledger entry written at first-boot is correctly sequenced
      relative to other first-boot Ledger entries (GENESIS_STARTED etc.).

Specific questions for State Consistency Theorist:
  (1) Does the Merkle-chain-lite integrity structure need an explicit
      SUPERSEDED_ENTRY_TYPE mapping so that audit consumers reading a log containing
      both deprecated and unified event types can verify chain integrity without gaps?
  (2) Is genesis-seal.json currently versioned or schema-typed in any way? If not,
      the addition of ceremony_authorization_key_anchor may silently succeed — or it may
      conflict if first-boot tooling has a closed field list. Confirm.
  (3) Where in the first-boot sequence does CAK_REGISTERED appear relative to
      GENESIS_STARTED and ORCHESTRATOR_KEY_ANCHOR? Order matters if the Ledger's
      genesis sequence is independently verified at startup.
```

---

## Gap Session Summary Block

```
╔══════════════════════════════════════════════════════════════════════════╗
║  GAP SESSION 4 — SUMMARY BLOCK                                           ║
║  Warden (primary) + Orchestration Comparativist (secondary)              ║
║  Topic: T14 Resolution + GAP-26 Unified Ceremony Authorization           ║
╚══════════════════════════════════════════════════════════════════════════╝

GAPS RESOLVED:
  GAP-26 — Ceremony Authorization Model Unspecified
    Resolution: D92 (dual-key hierarchy), D93 (unified ceremony token envelope),
    D94 (CAK physical storage contract), D95 (IC-SCOPE-AUTH-1 ratified), D96 (A3
    amendment to IC-TC-RESET). D-CRC-4 satisfied: unified framework covers all three
    ceremony types from GS1–GS3 plus circuit reset ceremony (GS2 IC-TC-RESET A3).
    OQ-S-GAP26-3 closed. OQ-S-GAP26-1 closed. OQ-S-GAP27-1 closed (scope_change_type
    added to SCOPE_UPDATE ceremony payload). GAP-26 is fully resolved.

TENSIONS RESOLVED:
  T14 — Single-Key vs. Dual-Key for Ceremony Authorization
    Resolution: D92 — dual-key hierarchy. CAK (human-held) MUST be separate from OOK
    (machine-held). Security argument: OOK filesystem residence makes single-key model
    vulnerable to filesystem-level compromise enabling self-authorized scope expansion.
    Operational assessment: overhead is acceptable given low ceremony frequency and
    hardware token portability.

GAPS PARTIALLY RESOLVED:
  OQ-S-GAP26-2 (Retention and rotation cadence for CAK):
    Retention rule: specified (D94 — until v2 rotation or compromise event).
    Rotation cadence: deferred to v2 (OQ-S-CAK-1). GAP-19 scope extended to cover
    CAK rotation alongside OOK rotation.

GAPS UNBLOCKED (not addressed in this session):
  GAP-27 — Rate limit design for SCOPE_UPDATED events (was blocked by GAP-26;
    now unblocked; assigned to GS7).
  GAP-21 — Ledger → Registry propagation window (was blocked by GAP-26 co-dependency;
    IC-HOLD-RELEASE amendment completed in this session; GAP-21 may now proceed).

GAPS DEFERRED:
  None from session scope.

NEW GAPS SURFACED:
  None. CAK rotation question subsumed under GAP-19 (scope extended).

NEW TENSIONS SURFACED:
  T15 — CAK Availability vs. Ceremony Urgency
    Status: Open (documented risk). v1 mitigation: operational requirement for backup
    custodian designation at first-boot. v2 resolution: OQ-S-CAK-2 (quorum signing).

NEW OPEN QUESTIONS:
  OQ-S-CAK-1 — v2 CAK rotation ceremony design (v2 deferred)
  OQ-S-CAK-2 — Multi-operator quorum / m-of-n signing (v2 deferred)
  OQ-S-CAK-3 — CEREMONY_REPLAY_THRESHOLD_EXCEEDED escalation path
                (blocked by GAP-16 — deployment-specific)

DECISIONS MADE: D92, D93, D94, D95, D96

CONSTRAINTS ESTABLISHED: C-CAK-1, C-CAK-2, C-CAK-3, C-CAK-4, C-CAK-5,
                          C-CRC-4, C-CRC-5, C-CRC-6

INTERFACE CONTRACTS DEFINED OR AMENDED:
  IC-SCOPE-AUTH-1 (ratified — Unified Ceremony Authorization Framework)
  IC-HOLD-RELEASE (amended — CAK specified; unified failure events)
  IC-TC-RESET §11.8.1 A3 (populated — CAK authorizes circuit reset ceremonies)

LEDGER ENTRY TYPES INTRODUCED: CEREMONY_ACCEPTED, CEREMONY_SIGNATURE_INVALID,
  CEREMONY_REPLAY_REJECTED, CEREMONY_REPLAY_THRESHOLD_EXCEEDED, CAK_REGISTERED,
  CAK_COMPROMISE_DECLARED (all require Appendix C addition)
LEDGER ENTRY TYPES DEPRECATED: HOLD_RELEASE_SIGNATURE_INVALID,
  HOLD_RELEASE_REPLAY_REJECTED (superseded by unified types)

SPEC AMENDMENTS REQUIRED:
  §13.2 genesis-seal.json — add ceremony_authorization_key_anchor field
  §10.9 Scope Update Ceremony — reference unified CeremonyToken
  Appendix C — six new entry types; two deprecated entries marked
  GAP-19 — scope extended to include CAK rotation

⚠️ STATE CONSISTENCY THEORIST REVIEW REQUIRED
  Trigger: Condition 1 (six new Ledger entry types; two deprecated), Condition 3
  (ceremony_authorization_key_anchor added to Tier 1 genesis-seal.json)
  Priority: REQUIRED before GS5 (which addresses Ledger reconciliation — GAP-25,
  GAP-21). The deprecated entry type question must be resolved before GS5 works
  the Ledger consistency model for ceremony-adjacent entries.

RECOMMENDED NEXT SESSION (GS5):
  State Consistency Theorist + Warden — GAP-25 (Ledger → Registry propagation),
  GAP-21 (TC timeout field / Genesis Hold lifecycle), A1 amendment (READ_ONLY mode
  TC compensation exemption). State Consistency Theorist review from this session
  feeds directly into GS5 scope.

╔══════════════════════════════════════════════════════════════════════════╗
║  Session: Gap Session 4 — Warden + Orchestration Comparativist           ║
║  Basis: T14, GAP-26, OQ-S-GAP26-1/2/3, D-CRC-4, IC-TC-RESET A3         ║
║  Status: Draft — awaiting State Consistency Theorist review flag         ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

*Gap Session 4 — Warden (primary) + Orchestration Comparativist (secondary)*
*v1.1 baseline — GAP-26 resolved, T14 resolved, IC-SCOPE-AUTH-1 ratified, A3 amendment
populated, 1 new tension (T15), State Consistency Theorist review flagged*
