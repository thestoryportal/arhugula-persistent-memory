## 10. Security Layer

### 10.1 Purpose

Every write is authorized, verified, auditable, and bounded by the least privilege necessary. The Security Layer establishes and enforces the trust boundaries across which agents, humans, and system components communicate.

### 10.2 The Patch Authorization Gate (D22, C16, extended D81, D90)

Mandatory and exclusive. No `.larql` patch reaches the write engine without passing all checks in sequence:

**Pre-checks (T5, T7, D81):**
1. Token signature valid (verified against Orchestrator public key from dual-store anchor).
2. Token not expired (invocation tokens: 10-minute TTL; schema migration tokens: 10-minute admission-time TTL).
3. Token not previously consumed (Ledger lookup).
4. `write_scope_hash` matches current Write Scope Definition version.
5. `expected_yaml_hash` matches current Agent YAML version. Content classification pre-check: if the patch contains triples spanning multiple classification tiers, Gate returns `CONTENT_CLASSIFICATION_MIXED` with `split_guidance` payload (D90, IC-GATE-9).
6. Scope lock reference (if present) is still valid.
7. Agent not in `suspended_agents` set.
8. `larql_syntax_version` present and within supported range (D81, C-GATE-1). Absent or below `min_supported_larql_version` → `VERSION_REJECTED` (hard rejection, no retry budget consumed). Above `current_larql_version` → `VERSION_UNSUPPORTED` (hard rejection, operator alert set). Between minimum and current → `LARQL_VERSION_LEGACY` advisory entry written (async), patch proceeds (D82).

**Core checks (D22–D23):**
9. **Identity** — agent token signature verification.
10. **Scope** — entity base type + relation family + tier target within agent's declared Write Scope Definition.
11. **Integrity** — patch hash matches agent-declared hash.

Failure at any check is hard rejection; partial write is prohibited. Direct filesystem writes to `.vindex` bypass the gate and are treated as security violations (C16).

### 10.3 Scoped Agent Roles (D25, extended by T2)

Four write-authorized agent roles:

| Agent | Types | Tiers | Edge Cap | External Content |
|---|---|---|---|---|
| Architect | All types/families | All Genesis tiers (with schema migration token) | 10,000/patch | HIGH RISK flag |
| Coder | `structural_entity` only | Structural + Knowledge families, incremental tier only | 500/patch (→100 with external content) | Capped |
| Pruning | `structural_entity` + `domain_concept` | Structural + Knowledge only, DELETE authorized | No numeric cap | None processed |
| TGA | None on `.vindex` (gatekeeper-data-producer) | n/a | n/a | Task spec only, no external |

TGA writes tests as part of the atomic task-completion package but never authors `.larql` patches. Architect is the only agent authorized to target Genesis tiers; all other agents are hard-rejected at the Scope check for any L1–L3 tier target (C19).

### 10.4 Invocation-Scoped Single-Use Tokens (T5)

Structure (nine fields):
- `token_id` — unique identifier for Ledger matching.
- `agent_id` — matches Write Scope Definition.
- `invocation_id` — specific invocation scope.
- `task_id` — for lineage tracking (IC-OR9).
- `scope_lock_ref` — lock ID if applicable.
- `write_scope_hash` — Write Scope Definition version at issuance.
- `expected_yaml_hash` — Agent YAML version at issuance.
- `issued_at`, `expires_at` — 10-minute TTL.
- `signature` — Orchestrator-signed.

**Token is not a standalone credential.** It is a *witness* to the state of the entire governance layer at the moment of issuance. An attacker stealing a token must also keep every anchored document unchanged within the TTL window.

### 10.5 Orchestrator Signing Key (T5)

Generated at first boot. Private half stored at `<harness_root>/.orchestrator-key/` with strict filesystem permissions. Public half dual-stored: primary in State Ledger as `ORCHESTRATOR_KEY_ANCHOR` (immutable), secondary at `<repo_root>/.harness/orchestrator-key-anchor.json` (Git-committed). Boot-time hash comparison required; mismatch suspends boot.

Key rotation is v2 (Category 3).

### 10.6 Genesis Security Protocol (D26)

Three-step:
1. **Human review** of Architect Agent output patch before write engine execution (mandatory in v1; OQ-S5 fully-automated variant is v2).
2. **Schema migration authorization token** — one-time-use, cryptographically bound to patch hash, 10-minute admission-time TTL (T7, revised from D27's original 30 minutes). Validated at Phase 1 admission; compile proceeds independent of token state thereafter.
3. **Post-Genesis snapshot integrity seal** — `genesis.vindex` hash stored as `IMMUTABLE_ANCHOR` Ledger entry. Project-lifetime rollback anchor.

### 10.7 Agent Suspension — Token Revocation Mechanism (T5, closes OQ-S2)

Bulk revocation via in-memory `suspended_agents` set on the Orchestrator. Suspension triggers:
- Three consecutive scope failures from same agent in one session (D31).
- Meta-Validator or Meta-TGA Health Score below 85%.
- Warden-initiated manual suspension for integrity events (C22).

Suspended agents cannot be issued new tokens; existing tokens rejected at Gate with `TOKEN_AGENT_SUSPENDED`. Clearing suspension requires explicit human action with Ledger entry.

Full PKI (mass revocation lists, delegation chains, multi-Orchestrator trust) is v2.

### 10.8 Write Scope Definitions as Tier 2 Sealed Artifacts (D24, T4)

Stored at `<harness_root>/.sealed-corpora/write-scope-definitions/` per the Sealed Corpus pattern. Updates via versioned additive directories with human-signed manifest. Not modifiable by any agent at runtime (C17).

### 10.9 Agent YAML ↔ Write Scope Definition Binding (T4, extended D87)

**Write Scope Definition is the source of truth.** Agent YAML is the operational document, structurally subordinate. Binding enforced at invocation time:

- Orchestrator computes YAML hash, compares against `expected_yaml_hash` field in Write Scope Definition.
- Mismatch → Orchestrator refuses invocation, `YAML_BINDING_FAIL` Ledger entry.

Update ceremony scales with blast radius:
- Trivial operational tweaks (temperature, non-prompt parameters): Git commit + `CONFIG_UPDATE` Ledger entry only.
- Changes affecting prompt content or allowed tools: Git commit + Write Scope Definition update (signed ceremony) + `expected_yaml_hash` update.

**Scope Update Ceremony (D87, extended by §20 Ceremony Authorization)**

Write Scope Definition updates are accepted mid-flight — no drain of in-flight invocations is required. An update MUST produce a `SCOPE_UPDATED` Ledger entry (GOVERNANCE, synchronous) before the Orchestrator's in-memory scope registry is updated. The entry carries `previous_scope_hash`, `new_scope_hash`, `ceremony_token_id` (A9 — replaces the v1.1 `ratification_signature` / `operator_signature` field), and `affected_agent_ids`.

**Ceremony authorization (A5, A6 — applied):** SCOPE_UPDATE ceremonies are now authorized via the unified CeremonyToken model (§20, IC-SCOPE-AUTH-1). The Orchestrator enforces the following admission order for every SCOPE_UPDATE submission (order is normative):

1. **Rate-limit check** against `scope_update_min_interval_seconds` (per-initiator primary; per-affected-agent-id secondary) — per Tier 3 `rate-limits.json` (GAP-27 resolution). If the rate limit is breached, the ceremony is rejected with `SCOPE_UPDATE_RATE_LIMITED` **before** any signature verification is performed (A6). This ordering eliminates a signature-oracle attack surface.
2. **CeremonyToken envelope verification** — structural validity, ceremony_type discriminator must equal `SCOPE_UPDATE`, non-replay check against Ledger.
3. **Ceremony authorization verification against CAK** — signature over the ceremony envelope is verified against the current `ceremony_authorization_key_anchor` (§13.2, A10). Verification failure is logged as `CEREMONY_AUTH_INVALID` and the ceremony is rejected. CAK verification precedes SCOPE_UPDATED Ledger write (A5); no SCOPE_UPDATED entry is produced by a failed authorization.
4. **Precondition checks** — manifest-lattice completeness, affected-agent-id validity, scope hash predecessor consistency.
5. **SCOPE_UPDATED write** — Ledger entry synchronous; in-memory registry update follows.

Any in-flight token whose `write_scope_hash` predates the update will fail at Gate pre-check step 4 with error code `SCOPE_HASH_MISMATCH` (distinct from generic infrastructure failure). The error payload includes `current_scope_hash` and `scope_updated_at`, enabling the Orchestrator to issue a corrected token without consuming the agent's retry budget. Active PREPARED transactions are not interrupted; scope changes are forward-only.

### 10.9.1 Scope Registry Reconciliation on Orchestrator Restart (GAP-25 / v3 GS5)

On Orchestrator restart, the in-memory scope registry MUST be reconciled against the Ledger's `SCOPE_UPDATED` entry chain before any token issuance resumes. The reconciliation procedure (IC-SCOPE-RECONCILE):

1. Read Ledger from boot back to the most recent `SCOPE_ANCHOR` entry (or genesis if none).
2. Replay all `SCOPE_UPDATED` entries in causal order, reconstructing the affected-agent → scope-hash map.
3. Verify the reconstructed head `new_scope_hash` matches the current Write Scope Definition's computed hash.
4. On match: mark scope registry `RECONCILED`; token issuance resumes.
5. On mismatch: emit `SCOPE_REGISTRY_DIVERGED` (INTEGRITY, sync, W1) with the reconstructed-head and computed-head hashes; Orchestrator enters `READ_ONLY`. Manual operator intervention required.

No SCOPE_UPDATE ceremonies are accepted until reconciliation completes. In-flight transactions from the pre-restart epoch do not resume — their tokens have been revoked by the restart event.

### 10.9.2 Scope Propagation Bound (GAP-38 related)

Every SCOPE_UPDATED event must propagate to all active token-issuing paths within a 5-second ceiling from Ledger-write-acknowledgment. Propagation is measured as the interval between `SCOPE_UPDATED.ledger_write_ack` and the Orchestrator's last-touched in-memory registry timestamp for `new_scope_hash`.

If propagation exceeds the ceiling, `DIVERGED_STATE` is emitted (CONSISTENCY, sync, W1). DIVERGED_STATE is an Orchestrator-local integrity signal: it triggers an immediate scope-registry self-check and, if the self-check fails, escalates to READ_ONLY via the standard circuit breaker (§11.8).

The 5-second ceiling is a hard invariant of the scope-propagation subsystem; it is not configurable. Ceiling breach must not be silent: either the registry catches up (returning to nominal), or DIVERGED_STATE fires.

### 10.10 Three Consecutive Failure Rule (D31)

Three consecutive scope failures from the same agent in one session: agent suspended, human review flag raised. Integrity failures are always escalated regardless of count (C22).

