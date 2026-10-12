## 26. External Document Provenance for Layer 4 Facts

### 26.1 Purpose

Layer 4 facts sourced from external documents (documentation sites, standards bodies, API references) require a provenance record binding the fact to a hash-pinned snapshot of its source at write time. §26 specifies the mandatory provenance block, the three-state staleness model, and the `external_source_audit` sub-routine on the Pruning Agent. Source: GAP-11 / v3 GS9 D101/D102.

### 26.2 Mandatory Provenance Block

Every Layer 4 fact written from an external source carries an `external_provenance` block in its patch metadata. Absence of this block for a Layer 4 external fact is a compile-time rejection: the Write Engine emits `LAYER4_MISSING_PROVENANCE` (UNRECOVERABLE at patch level; C-EXT-PROV1).

**Provenance block fields:**

| Field | Type | Required | Purpose |
|---|---|---|---|
| `source_uri` | URI | yes | Canonical location of the external document. |
| `source_hash_at_write` | hex (SHA-256) | yes | Hash of document content at write time. |
| `source_fetch_timestamp` | ISO-8601 UTC | yes | When the content was fetched. |
| `content_length_bytes` | integer | yes | Detects truncation vs. change later. |
| `etag` | string | optional | Populated if server returned one. |
| `archive_uri` | string (URI) | optional | Best-effort archive.org / IPFS pin. |
| `refetch_policy` | enum | yes | `pruning_cadence` \| `hourly` \| `never`. |

On patch commit, an `EXTERNAL_PROVENANCE_RECORDED` Ledger entry (CONSISTENCY, async) is emitted, replicating the patch metadata plus `patch_id`, `fact_triple_hash`, `ledger_seq`. The Ledger entry is the audit anchor; the patch metadata is the operational record consulted by the monitoring path.

### 26.3 Three-State Staleness Model — Advisory Only

Staleness is **advisory at detection time**, never blocking. The harness does not block writes or queries on external staleness (C-EXT-PROV2).

| State | Meaning | Ledger entry |
|---|---|---|
| `FRESH` | Last refetch hash matches `source_hash_at_write` | none (silent success) |
| `STALE` | Source reachable, hash differs from `source_hash_at_write` | `EXTERNAL_PROVENANCE_STALE` (async) |
| `UNAVAILABLE` | Source unreachable (404, DNS fail, timeout) | `EXTERNAL_PROVENANCE_UNAVAILABLE` (async) |

Both non-FRESH states emit CONSISTENCY-category entries and mark the underlying fact with an advisory `provenance_flag ∈ {STALE, UNAVAILABLE}` visible in query results. CORE-importance facts sourced externally additionally raise a `REQUIRES_HUMAN_REVIEW` signal on first detection, matching the pattern used by out-of-band Git reconciliation (§11.13) and merged through the Reconciliation Review Queue (§15.1, T-PM-vs-PA policy).

Rationale: Network flaps and benign upstream edits (whitespace changes, CDN variance) are routine. Hard-blocking on external staleness would wedge the harness on conditions outside operator control. The advisory pattern preserves auditability without creating a DoS vector against the harness via external source manipulation.

### 26.4 Monitoring — Pruning Agent `external_source_audit` Sub-Routine

The monitoring responsibility is placed on the Pruning Agent as a new sub-routine. No new component is introduced.

**Cadence:**
- Default: aligned with Pruning cadence (every 50 commits or 24 hours; §11.12).
- Per-fact override via `refetch_policy` field: `hourly` for fast-moving sources, `never` for sources intentionally pinned at a snapshot.

**Failure isolation (C-EXT-PROV3):** If N consecutive audit passes fail to reach the network (default N=5, configurable), the Pruning Agent suspends further external-audit work — but **not** Git-side pruning — and emits `EXTERNAL_AUDIT_SUSPENDED` (CONSISTENCY, async). This prevents log-flooding under sustained network partition.

### 26.5 Spec Block — External Document Provenance

**What it must do:**
- Bind every Layer 4 fact written from an external source to a hash-pinned snapshot of that source at write time.
- Detect source drift (content change) and source loss (unreachability) on a scheduled cadence, emitting advisory Ledger entries without blocking writes or queries.

**What it explicitly does NOT do:**
- Auto-retract or auto-rewrite facts when their source changes. Staleness is surfaced; reconciliation is a separate human- or Coder-Agent-driven action.
- Guarantee fetch fidelity for sources that serve non-deterministic content (dynamic pages, auth-gated resources). Such sources should be snapshotted to an `archive_uri` before provenance recording.

**Hard constraints:**
- **C-EXT-PROV1:** Layer 4 external facts without `external_provenance` block in the patch metadata cannot be compiled. Write engine rejects.
- **C-EXT-PROV2:** Staleness detection MUST be advisory. No code path promotes STALE or UNAVAILABLE to a blocking state automatically.
- **C-EXT-PROV3:** Pruning Agent audit sub-routine failures MUST NOT propagate to Git-side pruning. Isolation is explicit.

**Tradeoffs decided:**
- Advisory-only over hard-blocking (§26.3 rationale).
- Extended Pruning Agent over new dedicated component (§26.4 rationale).
- SHA-256 as sole hash algorithm for v1.2; field is enum-typed for future agility (BLAKE3 etc.) without schema migration.

**Open questions (deferred):**
- **OQ-SC3** — Reconciliation workflow for STALE Layer 4 facts once detected. Currently the fact stays in `.vindex` with an advisory flag; whether a Coder Agent auto-proposes a refresh patch or whether operator approval is required first is unspecified. Implementation-time decision per GS13 disposition.

**Interface contracts:**

```
IC-EXT-PROV1 — Write engine → patch validation
  From: Layer 4 .larql patch submitted to write engine
  To:   MEMIT compilation path
  What A exposes: external_provenance block present and well-formed.
  Failure behavior: LAYER4_MISSING_PROVENANCE (UNRECOVERABLE at patch level).

IC-EXT-PROV2 — Pruning Agent audit → State Ledger
  From: Pruning Agent external_source_audit sub-routine
  To:   State Ledger CONSISTENCY stream
  What A exposes: EXTERNAL_PROVENANCE_STALE or EXTERNAL_PROVENANCE_UNAVAILABLE
    entries keyed by fact_triple_hash + source_uri.
  Conditions: Refetch performed; hash compared; non-FRESH outcome reached.
  Failure behavior: EXTERNAL_AUDIT_SUSPENDED after N consecutive network
    failures (N configurable, default 5).
```

### 26.6 Non-Goals

§26 does not specify:
- Archive-URI population strategy (operator chooses archive.org, IPFS pin, or none).
- Reconciliation workflow for STALE facts (OQ-SC3 deferred).
- Per-source auth credential handling (out of scope; authoritative sources should be public or snapshotted).

---

