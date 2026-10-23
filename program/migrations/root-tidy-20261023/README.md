# Root tidy, 2026-10-23

The operator approved this batch in chat on 2026-10-23 (AskUserQuestion, labels verbatim): moves "Lean scripted batch (Recommended)"; removals "Both graft/ folders" and "chmod 600 .hf_token". The labviz site, the pip cache, the empty folders and the test fixtures were not approved for removal, and they stay.

- `moves.tsv`: 135 same-volume renames, as old path, new path and the rule each one follows. Each child of `results/` and `logs/` was either moved or left on purpose.
- `done.tsv`: one line per move. It gives the file count, the bytes, the digest of that move's inventory and the result. All 135 are OK: 8,951 files and 65,751,194,114 bytes, with the same SHA-256 before and after.
- `inventory.tsv`: every moved entry under its move number `n`. It records the path relative to the new location, the kind, the bytes, the SHA-256 (or the link text) and the mode.
- `removed.tsv`: the inventory written before the two approved removals. They were `M/graft` (1,300 entries, 201,780,596 file bytes) and the parent folder's `graft/` (5 entries, 3,529 bytes).

Model payloads are in `models/` (`models/Qwen_Qwen2.5-3B/manifests/variants.json`). The scripts and the full ledger are in `G-build/LEAN/root-tidy-20261023/` in the corpus-consolidation-toolkit run folder.
