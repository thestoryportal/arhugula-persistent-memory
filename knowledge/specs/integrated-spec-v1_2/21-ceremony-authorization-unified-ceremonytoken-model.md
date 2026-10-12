## 20. Ceremony Authorization — Unified CeremonyToken Model

### 20.1 Purpose

Every GOVERNANCE-class ceremony in the harness — manifest ratification, Dependency Hold release, scope update, circuit reset, schema extension, retention extension, project close, corpus manifest signing, and ceremony-key rotation — is authorized through a single umbrella Interface Contract: **IC-SCOPE-AUTH-1** (v2 GS4 — ratified; supersedes the v1.1 single-ceremony `IC-SCOPE-UPDATE` authorization model). The CeremonyToken envelope is the unified shape; specialized ICs delegate authorization to IC-SCOPE-AUTH-1 and specify only their ceremony-type-specific `ceremony_payload` bodies.

### 20.2 Root of Trust

The single root is the **Ceremony Authorization Key (CAK)** — public half anchored at `ceremony_authorization_key_anchor` in Tier 1 `genesis-seal.json` (A10, §13.2). The private half is operator-held, offline, HSM-preferred. The CAK is structurally distinct from the Orchestrator signing key (`ORCHESTRATOR_KEY_ANCHOR`) — no ceremony envelope with `key_ref == ORCHESTRATOR_KEY_ANCHOR` is ever accepted.

The break-glass anchor (`break_glass_key_anchor`, §23.3) is a second, distinct Tier 1 anchor authorized for one and only one ceremony type: `CAK_ROTATION_EMERGENCY`.

### 20.3 IC-SCOPE-AUTH-1 — Ceremony Authorization Interface Contract

**From:** Human operator (holder of CAK).
**To:** Every ceremony verifier in the harness — Gate (scope update), Transaction Controller (circuit reset), Hold Registry (Dependency Hold / Genesis Hold release), Migration Manifest Verifier, Schema Extension Ceremony handler, Retention Extension / Project Close handler, Corpus Manifest Verifier, Ceremony Key Rotation handler.

**Common envelope:**

```
{
  ceremony_type: "SCOPE_UPDATE" | "HOLD_RELEASE" | "MANIFEST_RATIFY"
               | "CIRCUIT_RESET" | "SCHEMA_EXTENSION"
               | "RETENTION_EXTEND" | "PROJECT_CLOSE"
               | "CORPUS_MANIFEST_SIGN" | "CEREMONY_KEY_ROTATION"
               | "CALIBRATION_RATIFICATION" | "RETENTION_PRUNING"
               | "CAK_ROTATION_EMERGENCY" | "CAK_BURST_CLEARED",
  ceremony_id:            UUID,
  ceremony_payload:       { ... },   // type-specific body, owned by the specialized IC
  operator_id:            <stable external id, GAP-46>,
  timestamp:              <ISO-8601, wall-clock>,
  operator_signature:     <signature over the canonical envelope bytes>,
  key_ref:                <MUST equal CEREMONY_KEY_ANCHOR>
}
```

**Verifier preconditions (uniform, non-delegable):**

1. `key_ref` MUST equal the current active `ceremony_authorization_key_anchor`.
2. `key_ref` MUST NOT equal `ORCHESTRATOR_KEY_ANCHOR`. Structural exclusion — checked before signature validation and before any ceremony-type-specific logic.
3. Signature valid against the public half at `key_ref`.
4. Timestamp within 60s of verifier's wall-clock (replay protection).
5. `key_ref` not in the revoked/rotated list (rotation-registry lookup; v1.2 rotation is via the break-glass `CAK_ROTATION_EMERGENCY` path only).
6. Ceremony-type-specific preconditions delegated to the specialized IC.

**Failure behaviors (SECURITY, synchronous, W1 — all escalate to Warden):**

| Condition | Emitted Entry |
|---|---|
| `key_ref == ORCHESTRATOR_KEY_ANCHOR` | `CEREMONY_AUTH_WRONG_KEY` (CRITICAL — Orchestrator attempted self-authorization) |
| Signature invalid | `CEREMONY_AUTH_SIGNATURE_INVALID` |
| Stale timestamp | `CEREMONY_AUTH_REPLAY_REJECTED` |
| `key_ref` in revoked list | `CEREMONY_AUTH_KEY_EXPIRED` |
| Unknown `key_ref` | `CEREMONY_AUTH_KEY_UNKNOWN` |
| Missing required envelope field | `CEREMONY_AUTH_MALFORMED` |

### 20.4 Specialized IC Delegation

All existing and future GOVERNANCE-class ICs delegate authorization to IC-SCOPE-AUTH-1 and specify only their `ceremony_payload` body and type-specific preconditions:

- **IC-TC-RESET** (A3 — §11.8.1): payload body for `CIRCUIT_RESET`; preconditions branch by trip reason.
- **IC-HOLD-RELEASE**: payload body `{ hold_id, hold_type, release_reason_code }`; preconditions include HELD-state verification by Hold Registry. Supersedes v1.1 `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` entries (both deprecated per A7b — they collapse into IC-SCOPE-AUTH-1's uniform failure set).
- **IC-SCOPE-UPDATE** (A5/A6/A9 — §10.9): payload body carries scope-hash predecessor and affected agent IDs; admission order includes rate-limit → envelope check → CAK verification → precondition checks.
- **IC-SCHEMA-EXTEND, IC-LDG-RETAIN (§27), IC-SL8**: delegate authorization; payload bodies per specialized IC.
- **Manifest ratification IC** (IC-MANIFEST-1, Check 8 from GAP-29a): delegates authorization; payload body carries manifest lattice completeness evidence.
- **CALIBRATION_RATIFICATION** (§22): payload body carries `epsilon_calibration_report` artifact.
- **RETENTION_PRUNING** (GAP-47 / GS10, IC-RP-1): payload body names the `artifact_retention_manager` role and retention-boundary operation.
- **CAK_ROTATION_EMERGENCY / CAK_BURST_CLEARED** (§23): payload bodies per §23.

### 20.5 Cross-Cutting Implications

IC-SCOPE-AUTH-1 changes the structure of every GOVERNANCE and SECURITY Ledger entry that previously carried a standalone `operator_signature` field. The envelope now wraps these: `operator_signature` appears as a nested field of the envelope, alongside `ceremony_type`, `ceremony_id`, and `key_ref`. Appendix C reflects the updated entry schemas.

### 20.6 Non-Goals

IC-SCOPE-AUTH-1 does not govern:
- Non-ceremony authentication (e.g., agent identity verification at invocation-time uses the Orchestrator signing key, not CAK).
- Automatic CAK rotation — v1.2 rotation is only via break-glass `CAK_ROTATION_EMERGENCY` (§23.3). Scheduled rotation is v2 (GAP-19).

---

