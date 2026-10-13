## 16. The Unified Ledger (T11)

### 16.1 Consolidation

The State Ledger and the previously-separate audit trail (D28) are **one artifact**. D28's intent is preserved; "audit trail" becomes an organizational lens on the Ledger via the `audit_category` entry field, not a separate store.

**Location:** `<harness_root>/.state-ledger/ledger.jsonl`. Append-only. Merkle-chain-lite integrity (D50). Outside Git and outside `.vindex`.

### 16.2 Three-Tier Writer Model (extended by GAP-29b / GS10 — W3 scope consolidation)

**Tier W1 — Orchestrator-mediated writes** (default for all component writes):
All components route writes through the Orchestrator, which verifies component identity, validates entry schema, assigns Merkle predecessor hash, and appends.

Writers under W1: Authorization Gate, Commit Executor, Meta-Validator, Meta-TGA, Validator, Pruning Agent, Transaction Controller, Human Review writers, Config Update Hook.

**Tier W2 — Bootstrap writes** (one-time):
During initial bootstrap sequence only. Writes Genesis Seal, Orchestrator Key Anchor, CAK anchor, break-glass anchor, `PROJECT_INITIATED` (retention policy declaration), and initial chain anchor. After bootstrap completes, bootstrap writer is retired; any subsequent bootstrap-class entry attempt is an integrity violation.

**Tier W3 — Emergency Escalation Path** (narrow, consolidated GAP-29b / GS10):

W3 is an **exceptional** write path: it bypasses Orchestrator mediation and is limited by policy to a small, ratified entry-type set. In v1.1 the only W3 entry type was `INTEGRITY_VIOLATION_EMERGENCY`. Subsequent gap resolutions added three further ratified carve-outs. The consolidated v1.2 W3 scope policy is given by **C-W3-1** (two admission criteria, both must hold) and **IC-W3-POLICY-1** (the consolidated admission contract).

**C-W3-1 — W3 admission criteria (both required):**

1. **Originator criterion:** the writer MUST be one of Gate, Transaction Controller, Boot-verifier, or (for ceremony-carve-out entries only) the ceremony-mediating code path executing an IC-SCOPE-AUTH-1-authorized ceremony. No other component may emit a W3 entry.
2. **Entry-type criterion:** the entry type MUST be on the ratified W3 carve-out list (below). No new entry types are added to W3 without amendment.

**IC-W3-POLICY-1 — ratified W3 carve-out list:**

| Entry Type | Carve-out Rationale | Source |
|---|---|---|
| `INTEGRITY_VIOLATION_EMERGENCY` | Original W3 scope — log compromised-Orchestrator scenarios where the normal W1 path is the problem. | v1.1 baseline. |
| Governance ceremony entries emitted during `CIRCUIT_TRIPPED` | The IC-TC-RESET ceremony itself must emit Ledger entries, but the Orchestrator's normal mediation path is suspended by the trip. Narrow carve-out: only entries whose `audit_category: GOVERNANCE` and whose `ceremony_token_id` binds them to the active ceremony. | GAP-37 / GS10 — closes T-SC-W-2, IC-GCO-1. |
| `TRUST_ROOT_LOST` entry | Emitted by the boot-verifier when both primary CAK and break-glass channel are compromise-suspect. Cannot route through Orchestrator because Orchestrator trust is itself lost. | GAP-42 / GS10 — IC-BG-1. |
| `BURST_SUSPENDED` entry | Emitted by the CAK enforcement path when per-CAK burst limit is breached; originator is Gate or TC, not Orchestrator. | GAP-41 / GS10 — IC-CAKB-1. |

Each W3 carve-out is subject to:
- Maximum 1 entry per minute per originator per entry type (rate limit).
- Strict schema enforcement — W3 entries use the same schema as their W1 equivalents; only the writer tier differs.
- Immediate write suspension on emission (except for the reset-ceremony carve-out, which by definition operates during write suspension).
- Forced human investigation via review queue cross-link.

Any W3 emission that does not meet C-W3-1 is itself a `W3_SCOPE_VIOLATION` (INTEGRITY, sync, W1) — detected at Ledger append by the Merkle-chain validator.

Aggregate-detection entry types (e.g., `GENESIS_INITIATION_ABUSE_PATTERN` from GAP-44) are **not** W3-eligible per C-W3-1 — they route through W1 because the Orchestrator remains trusted in those scenarios. The general framework convention for aggregate-detection entries (always-SECURITY category, `source_entry_hash_list` field, cross-linked review queue item) is GAP-55, deferred to post-v1 integration pass.

### 16.3 Write Mode Classification

**Synchronous (blocking)** — entries that must complete before the triggering operation proceeds:
- `TOKEN_CONSUMED` at Gate admission.
- `PREPARED` at 2PC Phase 1.
- `COMMITTED` at 2PC Phase 2.
- `COMPENSATED` entries.
- All `INTEGRITY_VIOLATION` entries.
- `CIRCUIT_TRIPPED`, `CIRCUIT_RESET`, `CIRCUIT_RESET_REJECTED`.
- `TIMED_OUT`, `RECONCILIATION_COMPLETE`.
- `SCOPE_UPDATED`, `SCOPE_UPDATE_REJECTED`.
- `RETENTION_OVERRIDE_REJECTED`.
- `PROJECT_INITIATED`, `PROJECT_CLOSED`.
- `VERSION_REJECTED`, `VERSION_UNSUPPORTED`.
- `CORPUS_WRITE_REJECTED` (UNAUTHORIZED_AUTHOR reason).
- `COMPACTION_ABORTED`, `COMPACTION_PROBE_FAILED`.

**Asynchronous (durable queue)** — observation entries:
- Meta-Validator / Meta-TGA health records.
- Sealed Corpus access records.
- Config update notifications.
- `LARQL_VERSION_LEGACY` (advisory).
- `CORPUS_CASE_ADDED`.
- `COMPACTION_CORPUS_SMALL` (advisory).
- `CONTENT_SPLIT_LOOP` (advisory).

Async writes go through WAL (`<harness_root>/.state-ledger/wal/`) before acknowledgment. WAL replays on crash. Ordering preserved within the queue; Merkle-chain order remains consistent.

### 16.4 Integrity Verification Cadence

- **Boot-time:** full chain walk from Genesis Seal forward (unchanged from D50).
- **Light verification:** every 100 entries appended. Verifies last ~10 entries. Cheap; catches immediate corruption.
- **Full verification:** every 10,000 entries OR 24 hours, whichever first. Walks entire chain.

Chain-break detection during any verification triggers immediate write suspension.

**Entry-count bounds for full verification (GAP-53 / GS11).**

Full chain verification is a linear-time operation in Ledger entry count. Operating envelope on reference hardware:

- **Typical project range:** 100K–1M entries. Full verification is routinely tractable.
- **Upper operating bound:** 10M entries marks the infeasibility threshold on reference hardware — full verification at this scale is not practical inside the 24-hour cadence.

Projects approaching or exceeding 10M entries require a sampled-verification strategy. The sampled-verification design (coverage guarantee, sampling distribution, integration with the C-GTO-2 pairing-check) is flagged for v2 (GAP-59). In v1.2, operators whose projects approach 10M entries must either rotate to a fresh epoch (via project close + re-initiation) or adjust the verification cadence (operational policy; not a spec-enforced knob).

### 16.5 Tiered Read-Access Model (closes OQ-S7, OQ-SL3)

- **Orchestrator:** direct read access.
- **Humans:** mediated access via Orchestrator-provided query API. Filtering by entry type, timestamp, audit category, correlation ID.
- **Agents:** restricted to entries where `agent_id` matches their own identity. Cross-agent audit visibility requires human-level access.
- **Filesystem-level access:** restricted to Orchestrator, Boot-verifier, and Retention Manager. Enforced via filesystem permissions.

### 16.6 Audit Category Tags

Every entry carries an `audit_category` field. Initial enumeration:
- `SECURITY` — Gate interactions, token events, integrity violations.
- `CONSISTENCY` — 2PC phases, rollback, chain events.
- `VALIDATION` — Meta-Validator, Meta-TGA, Reflexion outcomes.
- `GOVERNANCE` — Config updates, sealed corpus events, reviewer decisions.
- `LIFECYCLE` — Locks, holds, scheduling, archival, project lifecycle.

Tags enable query-based views without requiring separate stores. Enumeration is extensible.

### 16.7 Ledger Epoch Archival and Retention Policy Interface (T11, D89)

Ledger entries older than the most recent `ANCHOR_ESTABLISHED` event are eligible for cold-storage archival at `<harness_root>/.state-ledger/archive/{epoch_bundle_N}/`. Parallels T9 compaction-epoch bundling.

**Retention policy (IC-LDG-RETAIN):**
Retention policy is declared at bootstrap via `PROJECT_INITIATED` (LIFECYCLE, W2 bootstrap writer, immutable post-mint). Default if not specified: PROJECT_LIFETIME. Retention is immutable-downward (C-SL2): once configured, it MUST NOT be shortened. Extensions (longer retention) are permitted via `RETENTION_OVERRIDE_EXTENDED` (GOVERNANCE, signed ceremony). The Ledger layer blocks any shortening attempt regardless of operator key validity.

**Unconditional invariant:** Epochs containing any `INTEGRITY_VIOLATION` entry are retained INDEFINITELY, regardless of configured retention policy and regardless of any operator override attempt.

**Project close:** `PROJECT_CLOSED` (LIFECYCLE, signed ceremony) seals the final epoch and makes the Ledger read-only. Archival format: gzip bundles with operator-signed SHA-256 manifest, format version `"1.0"`. `PROJECT_CLOSED` is write-final — Ledger is read-only even if archival is pending (cold storage unavailable). Archival retried with exponential backoff when storage becomes available.

Archival preserves full entry content, Merkle linkage, and integrity hash manifest. Archived epochs are verifiable; on-demand restore is supported for forensic investigation.

### 16.8 Complete Ledger Entry Type Catalog

See Appendix C. The v1.2 catalog includes all v1.1 entry types plus 50+ additions from GS1–GS13 (new ceremony-related, bootstrap, burst-state, break-glass, scope-mismatch aggregate, external-provenance, retention, hook-integrity, Q5 weak-check, and corpus-expiry types). Two v1.1 entry types are marked deprecated per A7b: `HOLD_RELEASE_SIGNATURE_INVALID` and `HOLD_RELEASE_REPLAY_REJECTED` — both subsumed by the unified CeremonyToken model (§20 / IC-SCOPE-AUTH-1).

