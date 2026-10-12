# CPS HANDOFF — MAESTRO67 45% stop

MAESTRO67 sent the binding STOP. No new searches were started after it. Only this handoff was written in response; PRESERVATION.md was left unchanged.

## Done
- `results/context_audit_20261012/PRESERVATION.md` is the completed original sweep, 237 lines after the master correction; last verified SHA-256 `0f65bf015969549c0cd31f838ddbd5bea9738bb4d700b29a062a8bc0bbaf64a1`.
- Original coverage: all 14 `astra_r2*verdict.md` files; 48 blocking/conditional findings (a=6, b=8, c=34); 41 ruling/routing rows; 80 sole-store files (68 S1, 12 S3); seven worktree statuses. General sweep READY was delivered before the additions.
- Master correction applied: M is the stale LOCAL folder/ref `557a58bc`, not upstream content. `git show origin/master:<path>` confirmed cached upstream `5ccbb836` contains the cleanup, Astra routing, current engine pin, merge gate, exact deletion approval and uncapped optimizer; newer context thresholds remain absent. Last correction check at HEAD `8c107cdb` counted 516 branch-unique / 3 upstream-unique commits, versus MAESTRO's earlier 511/3 snapshot. No fetch occurred.

## In progress — added R2 access-path question
Already opened evidence (`B` = `results/compute_storage_brainstorm_20261011T054507Z`):
- `B/decisions_log.md:47–53`: operator chose separate local copies, not direct shared-memit working files. `:115–121`: Intel databases/builders continue from their own files; memit transfers coordinate. `:133–139`: first inventory selected M3 internal/memit sources and stage a verified Intel checkpoint.
- `B/design.md:208`: reviewed read-only source package or Git bundle, with interface selected in the implementation brief. `:244`: source capture references an admitted immutable export/Git revision, not an assumed local M3 worktree.
- `B/design.md:275–282`: selected sources may include internal SSD and memit; distinguish canonical live sources, old mirror and unique offloads; freeze the selected source/version set before transfer. `:297`: keep memit physically on M3; named folder services only; avoid writable whole-project mounts; permitted source/copy paths await the transport brief.
- `B/shared_disk_clearance_contract_v1_1.md:24–26`: Intel requests work; only a registered M3 executor releases disk I/O; Intel must have no independent bulk route/writable memit mount/bypass. `:34`: allowance authorizes the M3 executor, not Intel direct access. `:42,47`: exact allowed source/destination paths and physical pools are required in the frozen profile; absolute normalized paths, no wildcard assumptions.
- `B/shared_disk_clearance_freeze_v11.md:27,34,37`: M3 executor holds bounded memit access; Intel worker has no memit access; SOURCE_COPY/BACKUP_READ stream M3→Intel, with exact normalized paths in the unit profile. `:42`: ingress account itself has no memit mount/access.
- Targeted read-only scan across all 14 R2 verdicts found no finding naming the bare main folder or this worktree as the cause of NO-GO. The scan's worktree mention at `astra_r2d2_verdict.md:36` verifies reviewer Git identity; it is not Intel source selection. Reboot/remount findings are resource availability, not branch disagreement.
- Provisional interpretation: transfer selected, profile-bound source bytes through M3; no verified design selection among bare M, this worktree or the whole volume. DO NOT turn that into an exhaustive no-reference claim: Intel docs/profile data have not been exhaustively checked for bare-M source references.

## Remaining — exact-match origin and final insertion
1. FIRST read `results/context_audit_20261012/operator_hypothesis_worktree_vs_main.md` (MAESTRO says commit `9d71809c`); cite its evidence, do not re-derive points 1–5. This file was NOT opened before STOP.
2. Resolve the narrow remaining access-path question: did any R2 or Intel document explicitly point Intel/source capture at `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` rather than the worktree? Keep a source-package root distinct from a science entrypoint's working directory, control metadata root, and whole-volume mount.
3. Read `B/r2_round7_decisions.md:28–31` (supplied by MAESTRO, NOT opened in this stop turn). Trace its exact-match rule backwards to the first instruction/design, Astra finding or operator ruling that demanded it. The existing report records D3's conflict with pre-release process registration at `B/astra_r2j_verdict.md:7–13`; that alone is NOT the origin of exact recipe matching.
4. Compare original contract population/closure obligations, D3 recipe declaration, and later A1 operator amendment (`B/r2_round8_decisions.md:9–19`) without conflating them. A1 requires descendants to match declared recipes and uncertainty to retain exclusion, but its later date does not establish the first origin.
5. Determine whether stale/over-broad GPU-gate recall (SYNTHESIS F12) actually drove the rule, or whether it followed from sound shared-disk exclusion needs. Missing/stale notes alone do not establish causation; cite the builder/reviewer input that used them or state unproved.
6. When both additions are source-supported, append a short section 6 to PRESERVATION.md. Existing file is 237 lines, so the overall 250-line cap leaves at most 13 additional lines, despite the separate section allowance of 25. Recompute its final `Lines:` value, re-read against the brief and additions, and return the exact READY token.

## Scope and risks
- No commits, project Python, uv/npm, rclone, SSH, web, graft, activation, transfers, deletions or other edits. Only PRESERVATION.md and the expressly authorized stop handoff may be written. R2 never ran; additions are design/verdict analysis, not host evidence.
- Shared worktree has concurrent MAESTRO/builders; preserve their files and snapshot counts. Earlier output was sometimes truncated; reopen only the relevant authoritative spans, not broad repeated searches. Do not claim every Intel document was checked from a targeted R2 scan.
- Both pre-stop exec calls completed (no yielded/running exec session); no scan was left intentionally in flight.

## Binding context directive — restated for successor
Manage context usage for yourself and every orchestrated team session; this directive must survive every handoff. Start new work only at ≥60% context left. Codex builders may not see their own percentage: MAESTRO's watcher sends the stop at 45%. On that message or ANY context compaction, stop starting work, write done/in-progress/remaining work, exact paths, next steps and open risks into the named handoff, and reply CPS HANDOFF; successor by ≤40%. Never continue through full-window compaction. This handoff obeys the MAESTRO67 STOP: no further searches until a fresh successor.
