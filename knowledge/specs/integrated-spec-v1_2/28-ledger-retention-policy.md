## 27. Ledger Retention Policy

### 27.1 Purpose

Ledger retention policy governs how long each entry persists, how archival is structured, and how PROJECT_CLOSED interacts with archival I/O. §27 specifies a two-tier governance model (Tier 1 floor + Tier 3 active window), a canonical archive format `ledger-archive/v1`, and an async-archival PROJECT_CLOSED ceremony. Extends and supersedes the v1.1 IC-LDG-RETAIN block (D89). Source: GAP-12 / v3 GS9 D103/D104/D105.

### 27.2 Two-Tier Retention Governance (D103)

Two-tier retention: Tier 1 declares the immutable minimum floor; Tier 3 declares the active-in-hot-storage period.

| Parameter | Tier | Default | Constraint |
|---|---|---|---|
| `ledger_retention_floor` | Tier 1 | 7 years | Minimum total retention; cannot be reduced (C-RETENTION1). |
| `ledger_active_period` | Tier 3 | 90 days | Hot-storage window; operator-tunable. |
| `ledger_archive_period` | derived | floor − active | Must be ≥ 0; archive storage holds. |

**C-SL2 interaction (immutable-downward preserved):**
- `ledger_retention_floor` is immutable once set at Genesis. It may be *extended* by the `LEDGER_RETENTION_EXTENDED` ceremony (§27.4) but never shortened.
- `ledger_active_period` is operator-tunable downward to a minimum of **30 days** (Tier 1 floor on a Tier 3 value; C-RETENTION2). Attempts to reduce below 30 days are rejected by the Transaction Controller.
- `ledger_archive_period` is not directly configured; it is derived to satisfy `active + archive ≥ floor`. Reducing `active_period` extends `archive_period` for the same total.

Rationale: Seven years mirrors standard financial / legal audit retention floors and gives a defensible forensic window for the full lifecycle of a typical project. Ninety days active reflects the practical operational-debugging query window without forcing hot-storage costs on old entries.

### 27.3 Archival Format — `ledger-archive/v1` (D104)

Canonical archive format for v1.2. Versioned identifier permits future evolution without breaking restore paths.

```
Format identifier:     ledger-archive/v1
Compression:           zstd (level 19, long mode enabled)
Per-entry integrity:   SHA-256 (matches hot-Ledger algorithm)
Archive integrity:     Merkle root over all entries in archive batch
Chain-link anchors:    chain_hash_at_start + chain_hash_at_end bind archive
                       to the hot Ledger at batch boundaries
```

**Manifest schema (`archive-manifest.json`, sibling to compressed payload):**

| Field | Type | Notes |
|---|---|---|
| `archive_id` | UUID | Unique per archive batch. |
| `format_version` | string | `ledger-archive/v1`. |
| `start_ledger_seq` | integer | First entry in archive. |
| `end_ledger_seq` | integer | Last entry in archive. |
| `start_timestamp` | ISO-8601 UTC | First entry time. |
| `end_timestamp` | ISO-8601 UTC | Last entry time. |
| `entry_count` | integer | For restore verification. |
| `chain_hash_at_start` | hex | Hash of entry at `start_ledger_seq − 1`. |
| `chain_hash_at_end` | hex | Hash of entry at `end_ledger_seq`. |
| `archive_merkle_root` | hex | Merkle root over archived entries. |
| `compression_algo` | string | `zstd`. |
| `compression_params` | string | `level=19;long=27`. |
| `payload_sha256` | hex | Hash of the compressed payload file. |
| `manifest_sha256` | hex | Self-hash excluding this field. |
| `signer_identity` | string | Operator identity signing archive. |
| `signer_public_key_material` | blob | Public key material, bound to the manifest (GAP-52 / GS11 resolution — `ARCHIVE_KEY_SEALED` Ledger entry emitted at seal time; Genesis Seal cross-check at restore). |
| `signature` | string | Signature over manifest (excluding `signature` field). |

**Restore procedure:**
1. Verify `manifest_sha256` self-consistency.
2. Verify operator signature against trusted identity registry; cross-check `signer_public_key_material` against Genesis Seal archive-key record.
3. Verify `payload_sha256` against compressed payload file.
4. Decompress payload.
5. Verify `archive_merkle_root` against decompressed entries.
6. Verify `chain_hash_at_start` links to hot-Ledger entry (`end_seq − 1`) — confirms archive is contiguous with hot Ledger.
7. Expose restored range as read-only query layer appended to hot Ledger.

Merkle-chain-lite integrity extends across archive boundaries: a chain verification pass reads the manifest's `chain_hash_at_end` to continue verification into the next archive segment or into hot Ledger, **without requiring decompression** — the chain is verifiable against anchors alone.

### 27.4 PROJECT_CLOSED Ceremony Relationship (D105)

`PROJECT_CLOSED` (LIFECYCLE, signed — delegates to IC-SCOPE-AUTH-1 ceremony_type `PROJECT_CLOSE`) is synchronous and triggers — but does not depend on — final archival (C-RETENTION4).

**Sequence:**
1. `PROJECT_CLOSED` entry committed to Ledger synchronously. Harness enters `CLOSED` state — no new agent tokens issued, no new writes accepted.
2. `FINAL_STATE_SNAPSHOT` entry emitted, paired atomically with `PROJECT_CLOSED`, carrying the Ledger chain tip hash and the `.vindex` snapshot hash at close. (IC-RETENTION1 contract: atomic pair; either both commit or neither commits.)
3. Archive ceremony dispatched **asynchronously**:
   - If archive storage is available and writable: archive batch produced per §27.3, manifest signed, `PROJECT_ARCHIVED` Ledger entry emitted.
   - If archive storage is unavailable: `PROJECT_ARCHIVE_PENDING` entry emitted instead, with SLA clock started (default 30 days to resolve).
4. Expiry of SLA without `PROJECT_ARCHIVED` emission raises `PROJECT_ARCHIVE_SLA_BREACHED` (LIFECYCLE, sync, W1) — an operational incident requiring operator intervention. It does not alter the Ledger state of the project (which remains `CLOSED`) but flags the archival gap in any subsequent audit.

Rationale: Decoupling `PROJECT_CLOSED` (which must succeed atomically as a forensic anchor) from archival I/O (which can fail for storage reasons outside harness control) preserves closing-ceremony atomicity without fabricating a success signal for archival that may not have occurred.

### 27.5 Retention Update Ceremonies

**Floor extension (immutable-downward preserved):**
`LEDGER_RETENTION_EXTENDED` ceremony (IC-SCOPE-AUTH-1 ceremony_type `RETENTION_EXTEND`), Tier 1 authority signer (CAK), carries `new_floor_years > old_floor_years`. Attempts to reduce the floor are rejected at entry-construction time — the ceremony is structurally incapable of expressing a reduction.

**Active-period changes:**
`LEDGER_ACTIVE_PERIOD_UPDATED`, Tier 3 authority (operator), carries new value ≥ 30-day floor. Reduction permitted within floor.

### 27.6 Spec Block — Ledger Retention

**What it must guarantee:**
- No Ledger entry is deleted or made unreadable within the Tier 1 retention floor, regardless of operator configuration.
- Archived entries remain chain-verifiable against the hot Ledger Merkle chain via manifest anchors.
- Project close produces a synchronous forensic anchor even when archival storage is temporarily unavailable.

**What it explicitly does NOT guarantee:**
- Uninterrupted query latency for archived entries. Restore can require decompression and signature verification — a read-time cost.
- Archival storage medium availability. External dependency, monitored via SLA mechanism but not guaranteed by the harness.

**Hard constraints:**
- **C-RETENTION1:** `ledger_retention_floor` is monotonically non-decreasing from Genesis onward.
- **C-RETENTION2:** `ledger_active_period ≥ 30 days`.
- **C-RETENTION3:** Archive manifests MUST link chain hashes across archive boundaries for end-to-end Merkle verifiability.
- **C-RETENTION4:** PROJECT_CLOSED Ledger write MUST NOT block on archive I/O.

**Tradeoffs decided:**
- Single canonical archive format (zstd + SHA-256 + Merkle) over per-project format negotiation — forensic readability over compression tuning.
- Seven-year floor as default, operator may only extend — short-project operators bear the cost; long-lived projects are the common case.
- Async archival with SLA-tracked pending state over synchronous archival — preserves closing-ceremony atomicity.

**Open questions (deferred):**
- OQ-SL1 is **closed** by this spec block.
- GAP-60 (retired-key revocation metadata: retired-clean vs. retired-compromised classification for archive signing keys) deferred to v2.

**Interface contracts:**

```
IC-RETENTION1 — PROJECT_CLOSED → final snapshot
  From: Transaction Controller at project-close ceremony
  To:   State Ledger LIFECYCLE stream
  What A exposes: Synchronous PROJECT_CLOSED + FINAL_STATE_SNAPSHOT pair;
    chain tip hash; .vindex snapshot hash.
  Failure behavior: Ceremony atomic — both succeed or neither commits.

IC-RETENTION2 — Archive manifest → restore path
  From: Completed archive batch
  To:   Any future restore invocation
  What A exposes: Signed manifest with Merkle root, chain-link anchors,
    payload hash; compressed payload.
  Conditions: All archive verification steps pass (§27.3 sequence 1–7).
  Failure behavior: RESTORE_MANIFEST_INVALID or RESTORE_CHAIN_BREAK.
```

### 27.7 Non-Goals

§27 does not specify:
- External cold-storage export format (v2 — separate from archive format).
- Cross-project archive sharing policies (v2).
- Retired-key revocation metadata (GAP-60; v2-deferred).

---

═══════════════════════════════════════════════════
# PART VII — REFERENCE APPENDICES
═══════════════════════════════════════════════════

