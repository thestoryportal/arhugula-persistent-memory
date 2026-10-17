# Storage audit and reclaim, 2026-10-17

The audit freed 35 GiB on memit (17 → 52 GiB free) and 12 GiB on the internal disk (142 → 154 GiB free). It removed no science data. The operator approved every removal by item, in chat or on the decision page. Each removal has a row in the removal ledger. This note records what went, what stayed, and three lessons for the next audit.

All working files live in the audit folder SD = `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013T114331Z-2ec28dcb/icm-v2/storage-20261017/` (outside git). `_system/governance/STORAGE.md` holds the rules this audit followed.

## What was removed

Sizes are the bytes measured just before removal (`du`); the ledger is `SD/removal-ledger.tsv`.

| id | what | volume | paths | GiB |
|---|---|---|---|---|
| m1 | T330 prober's full repo clone (`reviews/T330/work-probe/tree`) | memit | 1 | 5.74 |
| m2 | W10 B1 test-run case folders | memit | 92 | 0.81 |
| m3 | review work trees of merged tickets | memit | 26 | 0.51 |
| m4 | v12 incomplete local rerun | memit | 1 | 0.41 |
| m5 | v13 failed setup probes | memit | 4 | 0.09 |
| m6 | old lane worktrees T001, T033, T084 and branches icm21/T033, icm21/T084 (no remote branches existed) | memit | 3 | 0.03 |
| m7 | git garbage in the main repo (`git gc --prune=now`) | memit | 1 | 0.24 |
| d1 | r4 verifier predecessor copies | memit | 137 | 2.77 |
| d3 | superseded ICM v2 package proof attempts, evidence-v11 to v13 | memit | 85 | 10.24 |
| d4 | macOS Spotlight index on memit (operator, Terminal `sudo`) | memit | 1 | ~14 freed |
| i2 | old Codex builds and daemon releases | internal | 10 | 2.85 |
| i3 | old review copies and merge exports | internal | 4 | 2.11 |
| i4, i4b | old session scratch dirs | internal | 36 | 1.88 |
| i5 | old ICM21 review dirs | internal | 18 | 0.88 |
| i6 | host TMPDIR test leftovers | internal | 828 | 0.25 |
| d2 | host TMPDIR icm-predecessor runs (each top-level RUN.json kept) | internal | 296 | 3.87 |

Kept by decision: d6 (backup-restore test sample) and d7 (MathLab duplicate runs), by the operator ("remove d3. Leave the other two."); i1 (uv cache, 9.0 GiB), d5 (Codex history, 4.6 GiB) and d8 (C10Y precast diagnostics, 18.6 GiB, science).

**d3 is workflow proof data, not science.** It held superseded acceptance attempts of ICM v2 packages v11 to v13. The 15 October proof rule protects it, so it needed the operator's explicit approval for the exact paths, which the operator gave. During the session MAESTRO called it "science" by mistake. The operator asked, and the label was corrected.

## Preserved before removal

`SD/preserve/PRESERVE-LOG.md` records each check. Three scripts that existed only in session scratch were copied to `LEAN/tools/` (`verify_ticket.sh`, `combined.sh`, `spot.sh`). The T088 and T090 successor test files went beside their receipts in `/Volumes/memit/llmdb-lanes/r4/T0{88,90}/`, which met d1's condition ("As long as any unique test files are moved if needed"). A blob check showed that d1's 137 trees (40,075 files, 300 distinct blobs) held no bytes found nowhere else.

## The extract: unique is not valuable

Before removal, a sweep copied every observability file with no byte-identical copy elsewhere to `SD/extract/`: 10,449 files, 195 MiB. Uniqueness was the only rule, so the copy was an unsorted dump outside any proper home. Most of it had no value.

A triage, approved by the operator ("extract stash triage is approved"), opened sample files in every group and sorted them (`SD/batches/triage/TRIAGE.md`, `decisions.tsv`):

| decision | files | MiB |
|---|---|---|
| keep | 437 | 17.2 |
| noise | 9,880 | 177.2 |
| unsure | 132 | 0.4 |

Noise means raw output whose outcome a kept record already holds. Examples: 4,274 per-mutant logs whose verdicts are in each ticket's review folder, and 76 T303 sweep files whose totals are in the sweep's `matrix.md`. MAESTRO checked that second claim and found it incomplete. 129 of the 152,615 sweep cells record a violation, and `matrix.md` keeps only per-row counts of them. Those 129 cells now sit in `LEAN/w1opt/reviews/T303/extract-20261017/t303-violation-cells.jsonl`.

Keeps went beside the records they describe, under `<home>/extract-20261017/<original path>`: ticket review folders, W10 review folders, proof-attempt folders. Audit records (memory backups, scratch probes) and the unsure files went to `SD/kept/`. `SD/batches/triage/PLACED.tsv` lists all 569 placements with their sha256; each was checked again after the copy.

The rule this produced is now step 2 of the removal order in `STORAGE.md`: extract what holds value, open real files to decide, and place each kept file beside what it describes.

## The 50.8 GiB figure

The decision page showed "memit free after: 50.8 GiB". That was the free space expected *after* removal (17.0 free + the chosen memit items, `SD/storage-reclaim.html`), not the amount freed. The operator asked why ~10 GB had been freed, not 50.8; the gap was the starting 17.0 GiB plus the items still to come. The final 52 GiB beat the estimate because d4 freed ~14 GiB, not the estimated 10.79.

## Lessons for the next audit

- **Positive-control every negative check.** `git ls-files --stdin` does not exist. `2>/dev/null` hid the error and printed a false 0 ("no tracked files"). Prove that a check can say "yes" before you trust its "no".
- **Nested and read-only trees break plain tools.** 41-level `icm-predecessor-*` chains break `os.walk` and `du` with ENAMETOOLONG (use `os.fwalk`), and frozen acceptance dirs are mode 555, so `rmtree` fails with EACCES until the dirs get u+w. `SD/remove.py` does both.
- **Partial checkouts lie to `git status`.** Every absent file shows as deleted. Test uniqueness by blob hash against the main repo instead.
- **Tools that make copies must clean them up.** The T330 prober's full clone (5.7 GB) pushed memit under the 20 GiB floor and stopped a ship. Where storage grows, and the check to run at every close, is in `program/runbook/03-operational-hygiene-runpod-gpu-memory-disk.md` §3.3b.

## Sources

In SD: `STORAGE-AUDIT-20261017.md` (the four area reports), `decisions/latest.json` (the operator's choices, sent 2026-10-17T11:41Z), `storage-reclaim.html` (the decision page), `batches/` (one TSV per item, `SUMMARY.md`, `SKIPPED.md`), `preserve/PRESERVE-LOG.md`, `removal-ledger.tsv`, `remove.py`, `batches/triage/`.
