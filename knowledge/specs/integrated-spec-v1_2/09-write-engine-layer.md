## 8. Write Engine Layer

### 8.1 Purpose

The write engine compiles `.larql` patches into physical modifications of FFN pathways via the MEMIT algorithm. All writes are overlay-based; the base model is permanently frozen (D11, C8).

### 8.2 MEMIT as the Designated Engine

MEMIT is the designated write engine (D12). ROME, GRACE, and full fine-tuning are explicitly excluded. MEMIT targets middle-to-late FFN layers (L15–L25 for a 32-layer model; C15). Early syntax layers are off-limits for semantic injection.

Two mandatory safeguards (D20):
- **Orthogonal projection** — new fact vectors are computed orthogonally to existing feature vectors, preventing polysemantic cluster corruption.
- **Covariance balancer** — scales injection strength relative to existing neighborhood covariance.

### 8.3 Two Operating Modes (D13)

- **Genesis Mode** — batch compile, mints the initial `.vindex` tier stack.
- **Incremental Mode** — smaller patches buffered via an L1 Cache before MEMIT compile.

### 8.4 The `.vindex` Tier Stack (D14)

```
.vindex/
  genesis_schema.vindex        ← L1 Genesis (frozen post-mint)
  genesis_domain.vindex        ← L2 Genesis (frozen post-mint)
  genesis_constraints.vindex   ← L3 Genesis (elevated-review changes only)
  genesis_knowledge.vindex     ← L4 Genesis (updatable via standard pipeline)
  incremental_NNNN.vindex      ← per-commit overlays
```

Tiered for independent rollback.

### 8.5 The `.larql` Canonical Format (D15, extended by T1, IC-SC1, D81, D90)

Four required sections, bracketed by `BEGIN TRANSACTION` / `COMMIT`:

1. **Entity Registration** — new entity nodes with base type tags.
2. **Edge Declarations** — edges with `declared_importance` enum (see 8.6).
3. **Deletions** — explicit `DELETE FROM EDGES` / `DELETE FROM ENTITIES` operations.
4. **Compiler Directives** — `TIER`, `CONTENT_CLASSIFICATION`, `ORTHOGONAL_PROJECTION`, `SET TARGET_LAYERS`.

Mandatory directives:
- `TIER` in every patch (C11).
- `CONTENT_CLASSIFICATION ∈ {structural, layer4_domain}` in every patch (C-SC3). Value `mixed` rejected pre-commit (C-SC4). When a patch contains triples spanning multiple classification tiers (detectable at Gate via triple-level `edge_category` check against the Tier 1 config `classification_tier_mapping`), Gate returns `CONTENT_CLASSIFICATION_MIXED` with a structured `split_guidance` payload specifying which triple IDs belong to each classification tier (D90, IC-GATE-9). The Coder Agent resubmits as N separate single-classification patches. Gate classification is authoritative; the Coder's declared patch-level directive is informational only.

Every patch MUST carry a `larql_syntax_version` header field declaring the `.larql` syntax version under which it was authored (D81, C-GATE-1). Current version: `"1.1"` (incorporating the T1 two-number importance model). The Gate's version pre-check (§10.2 pre-check #8) enforces this field. Compaction re-run parsing of superseded patches across version boundaries requires the versioned patch parser and `larql_migration_manifest` declared in Tier 1 config (D82).

### 8.6 Importance and Attention Weight — Two-Number Model (T1)

The agent-authored `attention_weight` field from the original `.larql` format is **split into two separate concepts**:

- **`declared_importance`** — agent-authored enum with three values: `CORE`, `SUPPORTING`, `INCIDENTAL`. Reference mapping: 0.9 / 0.7 / 0.4. Used pre-commit by the Validator to gate verification intensity.
- **`attention_weight`** — engine-computed during MEMIT compile, based on covariance balancer math. Not authored by the agent. Emitted into the State Ledger entry for audit and post-compile analysis.

A **divergence check** runs post-compile: if `declared_importance = CORE` yields engine-computed `attention_weight < 0.5`, or `declared_importance = INCIDENTAL` yields `> 0.9`, the Validator flags the write as a soft signal for review. Not a hard rejection.

### 8.7 Drift-from-Anchor Thresholds (T6)

Drift is measured relative to the most recent **anchor event**, not as total cumulative edges. Anchor events:
- Successful Genesis compile.
- Successful overlay compaction.

After an anchor event, drift resets to zero.

- **Drift warning:** 1,500 edges since last anchor → schedule compaction at next idle window.
- **Drift hard trigger:** 8,000 edges since last anchor → writes suspended until compaction completes.

Deletions count toward drift the same as additions (absolute edge changes).

All thresholds are provisional pending empirical validation against target model (OQ-W1 remains open).

The Write Engine exposes a queryable `drift_state` object to the Transaction Controller, updated after each `COMMITTED` Ledger entry and reset to baseline after each `ANCHOR_ESTABLISHED` event (D83, IC-WE-1). Fields: `edge_count_since_anchor`, `drift_tier` (enum `NOMINAL | WARNING | HARD | CRITICAL`), `anchor_event_id`, `overlay_file_count`, and `p95_latency_ratio`. The TC reads `drift_state` before issuing any new write token; tier-to-action mapping is specified in IC-WE-1. Tier boundary values are sourced from Tier 1 config; all values remain provisional (OQ-W1).

The drift counter MUST reconcile with the Ledger-computed edge count within 5% tolerance. Divergence exceeding this threshold triggers `INTEGRITY_VIOLATION` and write suspension (C-WE-1).

### 8.8 Architect Capacity Model (T6)

Two-ceiling model:
- **Hard security cap (per-patch):** Architect 10,000 edges, Coder 500 edges (100 when external content flagged), Pruning unbounded-in-principle but family-scope restricted.
- **MEMIT recommended batch size:** 2,000 edges. Patches exceeding this are sub-batched internally by the write engine. Sub-batching is transparent to the ledger — a 10K Architect patch remains one atomic 2PC event (preserves C-TPC2).

All Coder caps are per-patch (not per-session or per-task).

### 8.9 Post-Write Verification (D18)

Two-level mandatory probe:
- **L1 — Storage probe** (mandatory for all writes): `SELECT` read-back confirms the edge was written.
- **L2 — Behavioral probe** (mandatory for `declared_importance ∈ {CORE, SUPPORTING}`): generation test confirms the fact fires correctly in inference.

**Storage-pass / behavior-fail** is a named failure mode (D19, D30). Recorded as `write_outcome = "behavior_fail"` in the Ledger — explicitly not collapsed into success.

Compaction verification uses a distinct probe class (`probe_type: "COMPACTION_REGRESSION"`) that tests whether *previously encoded facts survived a recompile*, not whether a new fact was accepted. This probe is defined in IC-OC-PROBE and produces a `CompactionProbeReport` rather than the per-edge storage/behavioral probe signals of L1/L2.

**L2 probe family (§21):** L2 behavioral probes are authored from a three-member domain-agnostic probe family — Generation probe, Assertion probe, Constraint probe — subject to the Semantic Assertion Criterion with three judgment methods. Full protocol in §21. TGA is the authorship authority (v2 GS10 — GAP-9 resolution).

**Post-write fidelity calibration (§22):** The ε coefficient used in behavioral-probe pass thresholds is itself a measured quantity, produced by the `larql_fidelity_calibration` protocol per-transform-class. Protocol structure is ratified in §22; numeric ε outputs are implementation-phase per OQ-W1 (v2 GS8 — D-GS8-A; GAP-48 probe-set versioning open).

### 8.10 Anchor-Superseded Archive (T9)

`.larql` patches exist in three states:
- **Active** — feeds into the most recent anchor or subsequent incremental overlays. Retained in `.larql-archive/active/`.
- **Superseded** — earlier than the most recent anchor. Content embedded in that anchor's compacted overlay. Moved to `.larql-archive/superseded/{epoch_bundle_N}/` as compressed, manifest-sealed bundles.
- **Retained-for-audit** — ledger record (hash, metadata, classification, timestamp, issuing agent, outcome) is permanent regardless of archive state.

**Classification-differentiated retention:**
- Structural-classified superseded patches: **90-day default** retention.
- Layer4_domain-classified superseded patches: **project-lifetime** retention in cold storage.

Compaction is a full MEMIT re-run on archived patches (D62, closes OQ-W10). Delta composition is rejected — it would skip the mandatory mathematical safeguards. Time-based compaction scheduling: every 30 days since the last anchor, triggered during idle windows.

Compaction re-run MUST parse all active `.larql` patches through the versioned patch parser. Patches carrying a `larql_syntax_version` below the current version are translated via the `larql_migration_manifest` before passing to MEMIT compile. Translation failure aborts compaction (D82). The migration manifest is a Tier 1 config artifact; it is updated at the same time as `current_larql_version` whenever a `.larql` syntax version advance occurs.

