## Appendix D — Directory Layout

```
<harness_root>/                         # Machine-local, NOT Git-tracked
  .state-ledger/
    ledger.jsonl                        # Merkle-chain Unified Ledger
    wal/                                # Async write-ahead log
    archive/{epoch_bundle_N}/           # v1.1 Ledger epoch cold storage
  .ledger-archive/                      # v1.2 addition — canonical archive per IC-RETENTION2
    {archive_id}/
      archive-manifest.json             # signed manifest (ledger-archive/v1)
      payload.zst                       # zstd-compressed Ledger entries
  .sealed-corpora/                      # Tier 2 — human-signed sealed artifacts
    meta-validator-suite/
      manifest.json
      v1/ v2/ ... vN/
    meta-tga-corpus/
      manifest.json
      v1/ v2/ ... vN/
    constitutional-suite/
      manifest.json
      v1/ v2/ ... vN/
    write-scope-definitions/
      manifest.json
      v1/ v2/ ... vN/
    reconciliation-reviewers/
      manifest.json
      v1/ v2/ ... vN/
    corpus-author-registry/             # v1.2 addition (GAP-8 / v3 GS8)
      manifest.json
      v1/ v2/ ... vN/
    hook-registry/                      # v1.2 addition (GAP-54 / GS11)
      v1/
        manifest.json                   # per-hook binary hash registry
  .orchestrator-key/                    # Private key material (permission-protected)
  .dry-run-store/                       # v1.2 addition (GAP-33) — operator-owned
    {dry_run_id}/
      report.json                       # dry-run artifact; 37-day min retention
  .larql-archive/
    active/                             # Active .larql patches
    superseded/{epoch_bundle_N}/        # Compaction-epoch bundles

<repo_root>/                            # Git-tracked project repository
  .harness/                             # Tier 3 — Anchored Git Config
    genesis-seal.json                   # Tier 1 secondary copy
                                        #   (includes ceremony_authorization_key_anchor,
                                        #   break_glass_key_anchor,
                                        #   corpus_author_bootstrap_identity,
                                        #   larql_epsilon_table, ledger_retention_floor,
                                        #   scope_mismatch_aggregate_threshold_n,
                                        #   scope_mismatch_aggregate_window_seconds)
    orchestrator-key-anchor.json        # Tier 1 secondary copy (public half)
    path-classification.json
    rate-limits.json                    # v1.2 addition (GAP-27)
                                        #   scope_update_min_interval_seconds
                                        #   per-CAK and per-ceremony-type rate params
                                        #   ledger_active_period (≥ 30d)
    larql-migration-manifest.json       # Tier 1-governed; referenced by genesis-seal
    agent-yamls/
      architect.yaml
      coder.yaml
      pruning.yaml
      tga.yaml
      validator.yaml
  src/
  tests/
  ...

<harness_release>/                      # v1.2 addition — per-operator compiled binary
  harness.bin                           # embeds operator_root_public_key (C-BOOT-5)
  boot_manifest.json                    # signed by operator root key (IC-BOOT-1)
```

Notes:
- `.vindex/` is an internal-to-harness layout managed by the Write Engine (not shown — see §8.4).
- `corpus-author-registry/` and `hook-registry/v1/` are the sixth and seventh Tier 2 sealed corpora (Appendix E).
- `.dry-run-store/` is operator-owned per T-S-RP-1; Warden audit is metadata-only (IC-DRS-1).
- `.ledger-archive/` supersedes `.state-ledger/archive/` as the canonical archive location for v1.2 (IC-RETENTION2). Operators upgrading from v1.1 retain the legacy path read-compatibility but all new archives land at `.ledger-archive/`.
- Per-operator harness binary distribution (GAP-57 / OQ-PATH-DEPLOY) is an operator-side concern; v1.2 documents the precondition but does not prescribe distribution mechanics.

