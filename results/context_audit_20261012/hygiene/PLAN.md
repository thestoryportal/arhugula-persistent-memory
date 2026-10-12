# Context hygiene execution plan

**Goal:** make standing guidance consistent across repo/master/host/cache and catch drift; then pause for HIL. No science acceptance is claimed.
**Authority:** hygiene_planner_brief.md; SYNTHESIS §3; all D1–D5 approved. lanes.json is authoritative; briefs are self-contained. All edits this planner made are under results/context_audit_20261012/hygiene.
**Architecture:** isolated worktree per lane; complete host proposals in host_staging; unique unit receipts; dependency waves; one owner per index and generated file.
**Tools:** Python 3.9 stdlib, /usr/bin/python3 -B; no model/project Python/network/install/commit by builders.

## Dispatch and verification

1. MAESTRO creates isolated worktrees; resolves git rev-parse --git-path info/exclude (shared common-dir in linked worktrees), serializes existing writers, preserves its bytes and adds the exact two private staging paths. Verify git check-ignore --no-index in each worktree before private seeds; never stage/commit full configs. Builders never edit live host/Git metadata.
2. MAESTRO assembles accepted nonsecret predecessor outputs into a clean base; private predecessors travel only as immutable seed files. Freeze dispatch/<LANE>.json {lane,base_commit,input_hashes,private_seed_hashes} and its identical Git blob ref refs/context_hygiene/dispatch/<LANE>. Validate disjoint canonical paths/aliases; changed base or private seed halts.
3. Run lanes within each wave in parallel only after all previous-wave dependencies are accepted. Every unit≤8 min; lane≤36 min +4 finish. Budget means stop/handoff, never compress verification.
4. One Git-index owner follows every Git note reconciliation/import; cache-index owner follows every cache note export. I-MANIFEST freezes exact 196 exports before dispatch, preserving current 12 S3-only lessons (P01–P11 plus P14).
5. Shared file corrections are later-wave owners. No broad renderer --write; D-U15/16 regenerate only their destinations; D-U19 owns runbook/README/PROGRESS. Final parity check is read-only; corrections return to owners.
6. Run each lane checker plus fixture suite, read actual diffs and receipts. Behavioral RED precedes guard/renderer/sync/closeout changes. Preserve warnings/LAWs/holds/Memento; budgets are estimates, not permission to weaken rules.
7. E(n,s) is an assigned export-contract check plus 196 concrete note/cache units. Extra owners cover host settings, the new P14 note, Drive collision and retired-value/store/link drift guard.
8. Checkpoint snapshot frontmatter exemption is historical only. Same-name body notes must agree; role indexes differ only by exact approved hash/pair/reason policy. Denied or missing stores never pass.

## Waves

1. H01-01 (repo, 35m), H01-02 (repo, 35m), H01-03 (repo, 36m), H01-04 (repo, 36m), H01-05 (repo, 36m), H01-06 (repo, 36m), H01-07 (repo, 32m), H01-08 (repo, 36m), H01-09 (repo, 34m), H01-10 (host, 30m).
2. H02-11 (repo, 36m), H02-12 (repo, 13m), H02-13 (host, 17m).
3. H03-14 (repo, 30m), H03-15 (repo, 14m).
4. H04-16 (repo, 22m).
5. H05-17 (repo, 22m), H05-18 (host, 36m), H05-19 (host, 36m), H05-20 (host, 36m), H05-21 (host, 36m), H05-22 (host, 36m), H05-23 (host, 36m), H05-24 (host, 36m), H05-25 (host, 36m), H05-26 (host, 36m), H05-27 (host, 36m), H05-28 (host, 32m).
6. H06-29 (repo, 6m), H06-30 (host, 6m).
7. H07-31 (repo, 24m).
8. H08-32 (repo, 21m).
9. H09-33 (repo, 6m).

## Final steps — MAESTRO only

1. Assemble accepted nonsecret bytes, verify private hashes/public projections, every receipt/base and generated/fingerprint parity; resolve owner failures. Never stage/commit full private config/settings. Prepare D-U20–22 master patches against current main hashes, preserving unrelated forward work.
2. Apply complete host staging using host_apply.md backup + before-hash + byte-equality procedure. Settings/hook edits preserve enabled Memento. Credential-bearing config stays private; no secrets in commits.
3. Run LLMDB_ROOT=$PWD /usr/bin/python3 -B tools/context_hygiene_guard.py --root "$PWD" --policy tools/context_hygiene_policy.json --cache-manifest results/context_hygiene_20261012/memory_cache_manifest.json --host-root /Users/robertrhu --mode applied; require zero failures across guides, stores and body links.
4. Obtain completed Astra-high review of the applied result and deterministic receipts; address findings through exact owner lanes, then re-verify changed evidence. Hygiene does not qualify runtime hooks/autonomy or lift science/build/activation holds.
5. Operator asked first for master integration. MAESTRO obtains concrete PR/head/master-window GO, inventories and suspends competing writers, drains all candidate-head check/status writers, preserves master CI; integrate solely through tools/git_merge_gate.py and exact-head/full post-merge CI.
6. F01 remains open until master receives the reviewed rules through that gate. Re-run guard over master plus applied host after integration; archive backups/receipts and preserve a scoped handoff. Then pause for HIL next steps.

## Context and handoff

New work starts only at ≥60%; MAESTRO watches every team session, sends stop at 45%, successor by ≤40%. On stop or any compaction: no new unit; preserve done/in-flight/remaining, exact paths/risks and this directive in the lane-specific handoff; root uses OUT/chp_handoff.md.
Planner verification: test_check_lane.py (36 fixtures); re-read every OUT file against the brief; save scoped context/report and exact READY token. No generic /context-save writes outside OUT.

## Review focus

- Active values mixed with dated history: DG1/DG3 exempt only dated spans and exact historical paths.
- Store observation and provisional collisions: P14/P-GDRIVE/I-MANIFEST/DG4/DG5 fail closed and preserve before bytes.
- Scope/aliases/generated destinations: check_lane.py and MAESTRO dispatch validation compare exact paths and frozen base.
- Secrets and concurrent host changes: host_apply.md preserves private backups, before hashes and redacted review.
- Authority confusion: every brief preserves holds, Astra promote gate, Memento and full safety-rule homes.
