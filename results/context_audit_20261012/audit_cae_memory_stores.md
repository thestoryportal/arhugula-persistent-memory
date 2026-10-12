# CAE — reconciliation of the memory stores

Read-only audit, final inventory 2026-10-12T00:55:25.169213+00:00; worktree branch `worktree-c10k-route-a`, HEAD `be7be5a7c7c722118125f08b28ccd39b6115a781`. Only this report was written. Byte counts are UTF-8 source spans unless described as whole files; body-link rows charge each affected file once in the load table, not as extra runtime cost.

Aliases: **S1** = worktree `memory_mirror/`; **S2** = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory/`; **S3** = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/`.

Transcript citations: **T-W** = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory--claude-worktrees-c10k-route-a/99001b45-b0df-4ee3-bf2a-023a834c6bf3.jsonl`; **T-M** = `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/e453bfd5-fde9-4660-83df-1e68a92c1617.jsonl`. Citations use physical JSONL line numbers; no credential contents are reproduced.

| item (file:line-range or note filename) | bytes | verdict(s) | evidence (file:line or command) | proposed action | replacement text |
|---|---:|---|---|---|---|
| S1/memory-paths-and-mirror-discipline.md:3–16 (S2 identical) | 1687 | STALE; CONFLICT | S1:8–11 names TWO places and S2 as live; WT transcript T-W:32,52 names S3; inventory below: three stores, S2=125 files, S3=23. | fix-text (three stores; active path from harness, no fixed live default) | Reviewed Git memory_mirror is the durable source; Claude uses the memory path named by its harness. S2 and S3 are derived caches. |
| S1/memory-paths-and-mirror-discipline.md:16 (S2 identical) | 263 | AMBIGUOUS | “If one dir looks thin, repopulate it FROM the fuller one”: size can select either source. S1:10 makes Git canonical; S3-only notes prove fuller S1 is incomplete. | fix-text (reconcile by evidence and commit identity, never by directory size) | Reconcile new live notes into reviewed Git first; export the reviewed version to each active cache. Directory size does not establish authority. |
| EXPERIMENT_RUNBOOK.md:235; S1/MEMORY.md:43 | 478 | CONFLICT; DUPLICATE | Runbook requires identical directories INCLUDING MEMORY.md; tools/closeout_check.py:250–251,259 exempts index equality and mirror-only files. S1 memory-paths:11,16 repeats another formulation. | merge-into memory_mirror/memory-paths-and-mirror-discipline.md | Follow memory-paths-and-mirror-discipline.md; retained cache notes match reviewed Git bytes and generated indexes resolve within their cache. |
| tools/closeout_check.py:249–266 | 1350 | MISLEADING | Default :252–253 checks S2→S1. T-W:32,52 and T-M:27,41 name S3. Mechanical emulation: S2 yields two changed notes; S3 would yield twelve changed/missing notes. | fix-text (future hygiene: discover active path and check all registered stores) | Check each registered active memory cache against reviewed Git, including both directions, index validity, and note-link dependency closure. |
| tools/closeout_check.py:250–276 (enforcement scope) | 1728 | MISLEADING | Diff uses left_only/diff_files only (:259); ignores 77 S1-only relative to S2, 190 relative to S3, index byte drift, and body links. Warnings never enter missing/stale (:269–276). | operator-decision | Choose whether memory integrity is required for close-out; keep this advisory until the operator explicitly adopts an enforcement change. |
| S2/MEMORY.md:1 | 158 | STALE; CONFLICT | “Codex at ~20% left gets a fresh successor” conflicts with S1/MEMORY.md:1, S1/context-management-every-session.md:20,22 (≥60 new; ≤45 early stop; ≤40 successor), and S3/sol-builders-blind-to-context.md:9–11. | fix-text (export the current context rule) | New task at ≥60% left; MAESTRO sends stop at 45%; handoff and successor by ≤40%, immediately after compaction. |
| S2/MEMORY.md:125 | 145 | MISLEADING | Index recommends $((10-current)); identical S1/S2 background-shell-niceness-10.md:11,13 and S1/MEMORY.md:125 distinguish the pinned literal nice -n 10 launch and separate tmux server. This row restates only the generic arithmetic. | fix-text (point to pinned launch rule rather than generic arithmetic) | For pinned launch commands, follow background-shell-niceness-10.md; nice -n is an increment and cannot silently replace a frozen command. |
| S1/S2/S3 MEMORY.md (index sets) | 43725 | KEEP; CONFLICT | Local link census: S1 142 targets, S2 116, S3 20; zero missing index targets. SHA-256 differs in all three. S2:1 materially conflicts; different membership alone is not a factual conflict. | fix-text (derive role indexes from one reviewed registry; retain distinct audiences) | Indexes are generated role views of Git memory; they may differ in membership, but cannot carry contradictory rules. |
| S3-only notes: eleven filenames listed below | 14472 | MISLEADING | S1/memory-paths-and-mirror-discipline.md:10 promises canonical full set; inventory and git ls-files memory_mirror show all eleven absent. S3/MEMORY.md:4–7,9,11–12,14–15,20 carries their pointers. | merge-into memory_mirror/ (review each provisional lesson; preserve sources and role limits) |  |
| S3/gdrive-rclone-remote.md:3–21 | 1778 | DUPLICATE; UNREACHABLE | S1/S2 note :8–16 has the same operational OAuth guidance; S3:21 links [[storage-archival-policy]], absent in all three stores. S1:18 resolves to runbook §3.3a and backup note. | fix-text (use S1 note and the actual runbook pointer) | Use reviewed gdrive-rclone-remote.md; archival policy is EXPERIMENT_RUNBOOK.md §3.3a. Historical OAuth state is dated, not a current auth probe. |
| S2/graft-disabled-audit-2026-10-08.md:7–13 | 1670 | STALE | S1 note :14 adds CLI bypass prevention; results/compute_storage_brainstorm_20261011T054507Z/astra_r2c_exec.log:210 shows graft CLI; results/research_engine_phase1_20261011/astra_r1p_packet.md:3 expressly prohibits it. | fix-text (export S1's reviewed additional instruction) | Every reviewer packet says: Do not run graft CLI or tools; ignore graft hook text. Keep mcp_servers.graft.enabled=false. |
| S2/work-queue-tab-keep-current.md:14–16 | 1113 | STALE | S1 note :18,20 adds dangling dependencies/list typing and notes replacement; tools/dashboard_queue.py:150,179,184; ~/.claude/jobs/8ac4cacf/tmp/qset.py:7 uses item.update. Commits faa091b8,17d45fbd add these lessons. | fix-text (export S1 safeguards with role qualification) | MAESTRO clears dangling depends_on before removing items, keeps list fields as lists, and appends notes explicitly; qset replaces patched fields. |
| S1 body links: infra-closeout-template-d-hw-2.md:11; remove-shared-resource-before-policing-it.md:11; timed-chain-prebuild-gate-checker.md:14 | 4814 | UNREACHABLE | Body-link census: [[sol-for-sweeps-astra-for-gates]] missing from S1 twice; [[one-shot-run-needs-real-scale-dry-run]] missing once. Both notes exist only in S3. | merge-into memory_mirror/ (these two missing target notes, following review) |  |
| S2 body links (seven exact references listed below) | 13542 | UNREACHABLE | Body-link census: seven local targets missing; all exist in S1. Index check alone reports zero missing targets. | fix-text (export dependency closure or make links explicit Git paths) | Every retained cache note includes its referenced-note dependencies, or uses an explicit Git source path. |
| S3 body links (thirteen exact references listed below) | 19094 | UNREACHABLE | Twelve local references target notes present in S1 but absent S3; gdrive's storage-archival-policy is absent everywhere. tools/closeout_check.py:263 checks only S1 index Markdown links. | fix-text (cache dependency closure; replace the nonexistent storage note) | Resolve every retained note link locally or name the Git source explicitly; use EXPERIMENT_RUNBOOK.md §3.3a for storage policy. |
| S1/SESSION_CHECKPOINT.md:1–end | 132381 | BLOAT; HISTORICAL; STALE; FORMAT | Unindexed 132381-byte snapshot has June-21 GENERATED state (:4–12), no name/description/metadata.type; canonical SESSION_CHECKPOINT.md is 546815 bytes at this read and carries Oct-10 handoff (:3–12). git ls-files confirms snapshot tracked. | move-to docs/session_summaries/ (preserve historical bytes; remove from memory-note scans) |  |
| S1/codex-watch-anchor-tokens-read-context-from-rollout.md:1–16 | 1845 | DUPLICATE; HISTORICAL | git ls-files memory_mirror excludes this file. S1/codex-watch-anchor-replies-read-context-from-rollout.md:10–11 duplicates its two watcher rules; :13,17,19 adds corrected compaction/reply/busy detection and is indexed at S1/MEMORY.md:134. | merge-into memory_mirror/codex-watch-anchor-replies-read-context-from-rollout.md |  |
| S1/MEMORY.md:130; parallel-builders-name-each-others-files.md:11 versus S3/atomic-units-parallel-worktree-lanes.md:11–15 | 1496 | MISLEADING | S1 makes shared-worktree dispatch the applied pattern; newer operator answer T-W:510 requests parallel builders in their own worktrees. S3 atomic note :11 repeats that directive while preserving build hold. | fix-text (make old shared-worktree rule a contingency, not preferred dispatch) | Dispatch parallel builders in separate worktrees. If already sharing a worktree, name each lane's authorized files and preserve concurrent edits. |
| S1/S2 prior-audit closed memory-sync repair | 0 | KEEP | results/memory_audit_20261010/README.md:12 and APPLIED.md:133,244–248 record path repair and sync; tools/closeout_check.py:252–256 still uses a local path and warns on missing directories. | keep | The pod-path/ silent-skip repair remains present; new drift is incomplete coverage and later unsynchronized writes. |
| S1/S2/S3 frontmatter and index reachability census | 0 | KEEP | Read-only required-field/type regex over every note: all ordinary notes have name, description, metadata.type; only checkpoint snapshot fails. Markdown index targets all exist. | keep | Retain required frontmatter fields and resolving index pointers. Full YAML parsing was not performed; extra metadata fields alone are not invalid. |

## Cross-source findings

1. **The live-store assumption is wrong for observed sessions.** S1/memory-paths-and-mirror-discipline.md:9 describes S2 as live and usually no worktree memory; T-W:32,52 explicitly sets S3 while cwd is the worktree. T-M:27,41 sets S3 from the main checkout. The worktree-named project directory exists but has no `memory/`. S2 has no direct session JSONLs in this machine snapshot. It remains a legacy/other-launch cache; current universal loading of S2 is unverified. Do not choose a store from cwd hashing alone: the harness chooses it.

2. **Authority, equality, and enforcement disagree.** S1 memory-paths:10 names Git the canonical full set; runbook:235 requires identical S2/S1 directories and indexes; closeout_check:250–266 allows different indexes and ignores canonical-only files. The tested pair is useful for legacy cache drift, but cannot prove either current S3 coverage or full canonical retention. No project Python was run: the audit reproduced only the stdlib `filecmp.dircmp` expression. It returns two changed notes for S2, versus twelve missing/changed notes for S3. A memory warning does not prevent close-out completion (:269–276); enforcement changes need an explicit operator choice.

3. **Four filename collisions are fully accounted for.** `MEMORY.md` differs in all three stores: S1's current ≥60/40 threshold and early 45% stop source supersede S2's ~20% index hook (S1 context note:20,22); S3 lacks that note entirely and relies on its separate blind-context note. `gdrive-rclone-remote.md` has equivalent operational content, but S3's stale body pointer fails; prefer S1's corrected pointer, without treating dated OAuth claims as a fresh auth test. `graft-disabled-audit-2026-10-08.md` and `work-queue-tab-keep-current.md` are strict S1 extensions corroborated by the cited exec log, packet, queue parser, qset source, and commits. Export those S1 versions. All other same-name notes are byte-identical at the final snapshot; that is identity evidence, not a new scientific acceptance.

4. **Prior closed repairs have regressed in coverage, not reverted to pod paths.** APPLIED.md:244–248 records byte identity after the October-10 sync; today's three indexes and two S2 notes differ, and eleven S3 notes are outside Git recall. README.md:12's old pod-path/silent-skip issue remains repaired (closeout_check:252–256). Do not re-report already fixed Intel deployment, Astra-waiver, or artifact-output claims as new regressions; this lane found no evidence of those particular reversions.

5. **Canonical recovery is incomplete.** S3-only notes below are absent from S1, so a Git-only recovery would lose them. S1 already links two of these missing targets from three ordinary notes. Conversely, most S1 notes are never exposed by S3's twenty-entry index. That alone does not require loading every historical note, but role-essential guidance must be deliberately selected and cache note links must close.

6. **Two duplicate/redundant files require different treatment.** S1's old checkpoint is a historical copy of another canonical document, not a durable one-fact note; preserve its 132381 historical bytes elsewhere after approval. The untracked `*tokens*` watcher note is superseded by the tracked/indexed `*replies*` note. The latter preserves later corrections, so blindly importing the older copy would regress guidance. `git ls-files memory_mirror` confirmed that every other S1 file is tracked in the index; index membership does not by itself prove current working bytes were committed.

7. **New operator steering is stranded in S3.** T-W:510 records the request for atomic parallel units in separate worktrees; S3 atomic note:11–15 captures it. S1/MEMORY.md:130 and its parallel-builders note:11 still present shared-worktree dispatch without this newer default. Keep the shared-worktree preservation rule as a contingency; do not drop its protection.

### Proposed single authority and sync rule

**Reviewed, committed `memory_mirror/` on the designated program branch is canonical for durable behavioral notes.** CORPUS/runbook/program_state remain authoritative for scientific findings and changing program state. Claude's harness-named S2/S3 store is a derived recall cache: newly written live notes are provisional until independently reconciled into Git with their sources. Export reviewed note bytes from Git to every registered active cache; never select a winner by size, mtime, or filename. Generate role indexes from the same registry, including core safety/context/review rules and dependency closure; different index membership is allowed, contradictory rule text is not. Validate hashes, missing/extra retained notes, index links and note-body links for S2 and S3 and any newly discovered active path. Keep historical/tombstoned files out of default recall without deleting evidence. This is a proposal for the later approved hygiene pass, not sync/deletion authorization.

### Notes present only in S3, missing from Git memory

S2-only notes: **none**. The initial inventory had 22 S3 files and ten S3-only notes; while this lane was running, `atomic-units-parallel-worktree-lanes.md` and its index pointer appeared, producing 23 files and eleven S3-only notes. The first commentary tally included an extra item; the final mechanical counts below supersede it. This audit neither created nor edited that note.

| S3-only note | bytes | Git reconciliation |
|---|---:|---|
| atomic-units-parallel-worktree-lanes.md | 1449 | Preserve provisional source; review and merge into S1/atomic-units-parallel-worktree-lanes.md; retain MAESTRO/operator role limits. |
| codex-session-can-type-into-maestro-pane.md | 1251 | Preserve provisional source; review and merge into S1/codex-session-can-type-into-maestro-pane.md; retain MAESTRO/operator role limits. |
| commit-verified-bytes-before-successor.md | 1258 | Preserve provisional source; review and merge into S1/commit-verified-bytes-before-successor.md; retain MAESTRO/operator role limits. |
| interactive-codex-brainstorm-sessions.md | 1341 | Preserve provisional source; review and merge into S1/interactive-codex-brainstorm-sessions.md; retain MAESTRO/operator role limits. |
| maestro-hash-pin-edits-go-to-builders.md | 1236 | Preserve provisional source; review and merge into S1/maestro-hash-pin-edits-go-to-builders.md; retain MAESTRO/operator role limits. |
| one-shot-run-needs-real-scale-dry-run.md | 1187 | Preserve provisional source; review and merge into S1/one-shot-run-needs-real-scale-dry-run.md; retain MAESTRO/operator role limits. |
| readonly-check-runs-in-maestro-shell.md | 1943 | Preserve provisional source; review and merge into S1/readonly-check-runs-in-maestro-shell.md; retain MAESTRO/operator role limits. |
| sealed-allowance-two-drift-windows.md | 1323 | Preserve provisional source; review and merge into S1/sealed-allowance-two-drift-windows.md; retain MAESTRO/operator role limits. |
| sol-builders-blind-to-context.md | 1026 | Preserve provisional source; review and merge into S1/sol-builders-blind-to-context.md; retain MAESTRO/operator role limits. |
| sol-for-sweeps-astra-for-gates.md | 1355 | Preserve provisional source; review and merge into S1/sol-for-sweeps-astra-for-gates.md; retain MAESTRO/operator role limits. |
| stale-predecessor-watchers-steal-events.md | 1103 | Preserve provisional source; review and merge into S1/stale-predecessor-watchers-steal-events.md; retain MAESTRO/operator role limits. |

Corroborated examples: `readonly-check-runs-in-maestro-shell.md:7–11` matches `results/compute_storage_brainstorm_20261011T054507Z/r2q_maestro_acceptance.md:3,13`; `commit-verified-bytes-before-successor.md:11–15` matches `r2t_maestro_acceptance.md:5,80` and commit `3f4f150b`; the atomic-worktree directive matches T-W:510. These corroborations do not certify every narrative in the eleven notes: content review remains part of reconciliation, particularly provenance of agent-originated pane messages and scope limits on fixes/holds.

### Missing note-body links (indexes themselves have zero missing targets)

| store | source file:line | missing local target | available home |
|---|---|---|---|
| S1 | infra-closeout-template-d-hw-2.md:11 | sol-for-sweeps-astra-for-gates.md | S3 |
| S1 | remove-shared-resource-before-policing-it.md:11 | sol-for-sweeps-astra-for-gates.md | S3 |
| S1 | timed-chain-prebuild-gate-checker.md:14 | one-shot-run-needs-real-scale-dry-run.md | S3 |
| S2 | c10-mint2-r3-provisional-no-direction.md:12 | c10-secondkey-null-large-write.md | S1 |
| S2 | bias-ablation-causal-attribution.md:12 | exhaust-options-before-blocked.md | S1 |
| S2 | codex-runs-inline-from-claude-bash.md:10 | exhaust-options-before-blocked.md | S1 |
| S2 | injection-control-is-a-stratum-not-a-floor.md:12 | c10-edit-collateral-breaks-injected-target.md | S1 |
| S2 | autoresearch-editing-loop-per-fork.md:12 | c10-stacked-solve-tradeoff.md | S1 |
| S2 | c10z-stage1-underfit-terminal.md:7 | c10-sharedz-underfit.md | S1 |
| S2 | resolve-the-gates-real-criterion.md:10 | scope-gate-batch-is-deployment-model.md | S1 |
| S3 | gdrive-rclone-remote.md:21 | storage-archival-policy.md | No store; use runbook §3.3a for storage policy |
| S3 | stale-predecessor-watchers-steal-events.md:11 | never-idle-arm-completion-watch.md | S1, S2 |
| S3 | stale-predecessor-watchers-steal-events.md:11 | context-management-every-session.md | S1, S2 |
| S3 | labviz-wireframe-before-spec-approval.md:11 | context-management-every-session.md | S1, S2 |
| S3 | readonly-check-runs-in-maestro-shell.md:11 | codex-brief-handoff-file-narrow-reads.md | S1 |
| S3 | rerun-builder-tests-host-tmpdir.md:11 | codex-sandbox-no-network.md | S1, S2 |
| S3 | one-shot-run-needs-real-scale-dry-run.md:12 | rerun-never-patch.md | S1, S2 |
| S3 | stop-open-ended-builder-self-audits.md:11 | trim-builder-reading-lists.md | S1 |
| S3 | stop-open-ended-builder-self-audits.md:11 | context-management-every-session.md | S1, S2 |
| S3 | dry-admission-probe-before-one-shot.md:12 | gpu-gate-refuses-any-venv-python.md | S1, S2 |
| S3 | dry-admission-probe-before-one-shot.md:12 | rerun-never-patch.md | S1, S2 |
| S3 | interactive-codex-brainstorm-sessions.md:12 | context-management-every-session.md | S1, S2 |
| S3 | interactive-codex-brainstorm-sessions.md:12 | codex-web-review-lanes.md | S1 |

### Other matching Claude project directories

The command was a read-only `/usr/bin/python3 -B` directory enumeration of `/Users/robertrhu/.claude/projects`, selecting names containing `llm-database` or `c10k` and testing each `memory/` path. No other matching memory directory was found.

- `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory--claude-worktrees-autoresearch-c10`: project directory exists; `memory/` absent.
- `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory--claude-worktrees-c10k-route-a`: project directory exists; `memory/` absent.
- `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-autoresearch-sandbox-c10`: project directory exists; `memory/` absent.
- `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-autoresearch-sandbox-probe`: project directory exists; `memory/` absent.
- `/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-autoresearch-v13-fixture-c10`: project directory exists; `memory/` absent.

## Load cost

Approximate tokens = ceil(UTF-8 bytes / 4), not tokenizer measurements. Stored directory totals are potential read cost, **not automatic startup cost**. MEMORY.md is an index; ordinary note bytes are paid when a session actually reads them. The table below accounts for every filename in each store, with full SHA-256; equal-name copies are grouped only when bytes match.

| store | files | all stored bytes | approximate tokens if all read | index bytes / tokens / lines | indexed targets | unindexed files excluding index |
|---|---:|---:|---:|---|---:|---:|
| S1 | 202 | 506721 | 126681 | 22597 / 5650 / 154 | 142 | 59 |
| S2 | 125 | 280148 | 70037 | 17851 / 4463 / 128 | 116 | 8 |
| S3 | 23 | 34976 | 8744 | 3277 / 820 / 20 | 20 | 2 |

S1's 202 Markdown files comprise 200 ordinary notes, one index and one checkpoint snapshot; the lane prompt's “201 notes + MEMORY.md” includes the non-note snapshot. S2 has 124 notes plus index; S3 has 22 notes plus index at the final snapshot. S1 index leaves 1803 bytes under the stated 24400-byte cap; adding the eleven notes' hooks requires planned index editing, not a blind append. None of the three indexes exceeds 200 physical lines.

| session | what is loaded | evidence and limits |
|---|---|---|
| Claude in observed main/worktree launches | S3/MEMORY.md automatically; S3 notes when recalled; S1 index/notes on explicit repository reads | T-W:32,52 and T-M:27,41 name S3 and state MEMORY.md is loaded each session. S1 recall is directed by CLAUDE.md:66 and DISCIPLINE.md:38. S2 universal auto-load is contradicted for these launches. |
| Claude launched under mirror-root/legacy project | S2 index if that launch's harness names it | S1/memory-paths:9 describes this route; project directory exists with 125 files but no direct JSONL sessions were present. Current live loading for this route is unverified. |
| Codex builder | S1 index/relevant notes when its brief or AGENTS directs reading; no evidence S2/S3 automatically load | AGENTS.md:53 and DISCIPLINE.md:38 require Git memory recall. This lane's injected instructions name S1. Files existing in Claude directories do not imply Codex visibility. |
| Astra codex exec reviewer | Packet-specific S1 material when packet requires it; no established S2/S3 auto-load | CLAUDE.md:16 defines reviewer invocation, not a Claude-memory loader; astra_r1p_packet.md:3 is a concrete reviewer packet. Exposure to a given S1 note must be verified in its packet/reads. |

### Complete filename/hash inventory and per-file read cost

Mechanical first pass used `/usr/bin/python3 -B`, `Path.iterdir`, file bytes and SHA-256. Independent verification invoked `/usr/bin/shasum -a 256` on all 350 stored files, validated exit 0/nonempty output and compared every digest to Python's digest: 350/350 matched. No secrets were extracted. Membership/counts below are the final snapshot; SHA entries are identities, not authority or freshness verdicts.

| filename | stores | bytes / approximate tokens per load (by store) | SHA-256 equality and full digest | recall route |
|---|---|---|---|---|
| MEMORY.md | S1, S2, S3 | S1: 22597 / 5650; S2: 17851 / 4463; S3: 3277 / 820 | COLLISION; S1: ecc6bd053e1dfc4fa126ef33bc9f914ff7471270a3ad9e1808e2750770ee7196; S2: 93973d9436b47ea687a9a3503ab666885a3ca51d1f2f48312a9b2826b4db26a8; S3: c1476f69b6e1225243cab2f488aae58d45bca6707056d9042693fed046a1dda8 | S3 auto; S2 conditional; S1 explicit |
| SESSION_CHECKPOINT.md | S1 | S1: 132381 / 33096 | ONLY; S1: 3376e42360cac68aa78175fab417a083908ef207ddfb489794a27754a27bbdbb | S1 explicit historical snapshot |
| anti-drift-enforce-not-autowrite.md | S1, S2 | S1: 2486 / 622; S2: 2486 / 622 | IDENTICAL; S1=S2: f467064438f52cd0750bc5e42d65d6f6c3ebafe0248e0b5caef1750bc6cf9422 | S1 explicit; matching Claude cache on recall |
| anyedit-clearing-c10-would-close-tested-write-serve-scope.md | S1 | S1: 685 / 172 | ONLY; S1: df5916d580b9b86f84b557f9944c06ea6a6bb1048aafeec11bfb1310dbe6d95d | S1 explicit |
| anyedit-connectedpapers-adds-diagnostics-not-plan-change.md | S1 | S1: 643 / 161 | ONLY; S1: c36cd4545fcc6599263c23b1754e277c6791f7fa5e61c43e463011ee9317d379 | S1 explicit |
| anyedit-default-window-collapses-c10-a7.md | S1 | S1: 625 / 157 | ONLY; S1: dfc4d65ee49c3af47ea3598b3c7ed796c5de948a7dbc743b090af962622ef97d | S1 explicit |
| anyedit-gate-upgraded-by-muke-coin-suit.md | S1 | S1: 619 / 155 | ONLY; S1: e8120a92fe199f4069dc4899c2e420fa14da2f8008093bcc46b194ba688a256d | S1 explicit |
| anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md | S1 | S1: 620 / 155 | ONLY; S1: e572607fb978a23c15b5427c7c80815c413ef87a02c5e656199d1d124000f109 | S1 explicit |
| anyedit-local-transplant-controls-fail-before-a7.md | S1 | S1: 613 / 154 | ONLY; S1: fa03924f7d2fe7b0258dec6cc86aa8f039e38e95de4470f6dc27559cb74841db | S1 explicit |
| anyedit-name-collision-dcdmllm-is-image-editing.md | S1, S2 | S1: 729 / 183; S2: 729 / 183 | IDENTICAL; S1=S2: 5b4dc95c857800b1e71d4c955a4e107b5a19a1437fdce3b596077000322b4efb | S1 explicit; matching Claude cache on recall |
| anyedit-noop-gate-is-not-active-edit-parity.md | S1, S2 | S1: 1757 / 440; S2: 1757 / 440 | IDENTICAL; S1=S2: ef6232214c3a8c87e7ca5bc72bace6d2d5ed6944e91d9b5721eb979bd90a95c3 | S1 explicit; matching Claude cache on recall |
| anyedit-port-keys-at-last-prompt-token-no-paraphrase-transfer.md | S1, S2 | S1: 2104 / 526; S2: 2104 / 526 | IDENTICAL; S1=S2: 7275c085241e148b27f34c4f7a723acbf9fb492dbaeee8f6191c962c76158936 | S1 explicit; matching Claude cache on recall |
| anyedit-precommit-triage-proceed-but-viability-gated.md | S1 | S1: 560 / 140 | ONLY; S1: 0749bbbc78daec981ddcda25880cbf308b213124b8e0ab81a871b5b0f0fad830 | S1 explicit |
| anyedit-token-alignment-gate-prevents-false-rescue.md | S1 | S1: 484 / 121 | ONLY; S1: 3a26dc7eec0f07a79bedeb4a52fceb17adefc39273259466090bfe8b4041419d | S1 explicit |
| approved-deletes-ask-then-rmtree.md | S1, S2 | S1: 1680 / 420; S2: 1680 / 420 | IDENTICAL; S1=S2: 001548bbfdf8625a9b7d5077b28f837e8f3ca1540f8b783416ef0df7a8bc687d | S1 explicit; matching Claude cache on recall |
| ask-astra-automatic-before-operator-chore.md | S1 | S1: 1400 / 350 | ONLY; S1: 1ae52093439ecdf8428497aee561587649098f705246a0f7d7e674e7d9363a2a | S1 explicit |
| atomic-units-parallel-worktree-lanes.md | S3 | S3: 1449 / 363 | ONLY; S3: 2b2cecfa996e73b0196dc941b2c973e03cfec905bbade15c408ea7da5fd98edb | S3 recall; absent Git/Codex recall |
| autonomy-drifts-from-kickoff-scope.md | S1 | S1: 1646 / 412 | ONLY; S1: 30c251d2db65cd3bb3a67ebf5d5527ca07cc0d73cc5d2eedec8daf97e12965ee | S1 explicit |
| autonomy-driver-stale-guard-deletes-result.md | S1, S2 | S1: 1579 / 395; S2: 1579 / 395 | IDENTICAL; S1=S2: 96bb431a8eb31bff194659bb5469e2f296e1a6273316be247ed1ed80d2189219 | S1 explicit; matching Claude cache on recall |
| autonomy-error-label-can-mask-completed-run.md | S1, S2 | S1: 1116 / 279; S2: 1116 / 279 | IDENTICAL; S1=S2: ab6e842529358cd965fe79991d741b05f2c7d232195d26ff7515ba92a531e95f | S1 explicit; matching Claude cache on recall |
| autoresearch-editing-loop-per-fork.md | S1, S2 | S1: 2600 / 650; S2: 2600 / 650 | IDENTICAL; S1=S2: 6596b583f6e0454fddd7478884211a2bac00fe507f128f5cb4a7cf4b1d6b6078 | S1 explicit; matching Claude cache on recall |
| autoresearch-is-not-a-faithfulness-gate.md | S1 | S1: 496 / 124 | ONLY; S1: cecf142e48f37a0d699f4a294920af612de2ff314502732742eb4e988267b5c3 | S1 explicit |
| autoresearch-sandbox-fence-and-tmux-driving.md | S1, S2 | S1: 3758 / 940; S2: 3758 / 940 | IDENTICAL; S1=S2: 7b35dd5878c744b6af7e0743753432e6011e3b726c0ecfd9bf51fb8c9364274c | S1 explicit; matching Claude cache on recall |
| background-monitor-no-premature-read.md | S1 | S1: 530 / 133 | ONLY; S1: b89b639aa307c47c285847093431739dcfd4909d3ae3b85693c8ecd65cc284a9 | S1 explicit |
| background-shell-niceness-10.md | S1, S2 | S1: 2368 / 592; S2: 2368 / 592 | IDENTICAL; S1=S2: ac9186b1fff1f3bb7b452f93f1f44d8beaed6510b34b5678104b18828570fdf3 | S1 explicit; matching Claude cache on recall |
| backup-via-memitbackup-app.md | S1, S2 | S1: 2572 / 643; S2: 2572 / 643 | IDENTICAL; S1=S2: 8746bb75b514348e39e664ffefc0cdbc6bda4e681f9a45f210e5597daf1ae0f4 | S1 explicit; matching Claude cache on recall |
| betaedit-official-repo.md | S1, S2 | S1: 2851 / 713; S2: 2851 / 713 | IDENTICAL; S1=S2: 2686c0620c7fac0d9c01779df5b1499c12f44025f3c09b06368e0640d7384175 | S1 explicit; matching Claude cache on recall |
| bias-ablation-causal-attribution.md | S1, S2 | S1: 1742 / 436; S2: 1742 / 436 | IDENTICAL; S1=S2: 71c96b11d8964fb59a09c88b31f8f80f23e6662a5dbe8cfee4fc9c62c6aa01d6 | S1 explicit; matching Claude cache on recall |
| browser-harness-for-browser-automation.md | S1, S2 | S1: 1134 / 284; S2: 1134 / 284 | IDENTICAL; S1=S2: 07cd930b743bcdf846238a30d18570a37e1485a9adef8b9c39d94b94ece72cc3 | S1 explicit; matching Claude cache on recall |
| c10-accept-bounded-means-hybrid-not-general-db.md | S1, S2 | S1: 920 / 230; S2: 920 / 230 | IDENTICAL; S1=S2: e31c942a6fcf5ee2eaa91193c9b30e29d3970d231427cbe2e882eaa756b26541 | S1 explicit; matching Claude cache on recall |
| c10-band-knobs-failed-for-hard-coined-values.md | S1 | S1: 469 / 118 | ONLY; S1: 38d5783c52c4bfcca2a59d0b500cbded2a67766cc2c1dbd4839738e68cf41dec | S1 explicit |
| c10-edit-collateral-breaks-injected-target.md | S1 | S1: 1510 / 378 | ONLY; S1: 92fe8e0d06dffaadd6f613e16f1119cc5c920c02f883fdcb9ecbe75b48dda9c1 | S1 explicit |
| c10-edit-rotates-required-target-direction.md | S1 | S1: 1389 / 348 | ONLY; S1: 16e427c39a7dc6071ae7c1f0d3c4fc6d40bb7c31416633691b0dedad4255ce99 | S1 explicit |
| c10-layerpick-null.md | S1 | S1: 1360 / 340 | ONLY; S1: a4e348aae6ba6585be00efab31c47e4eaaa0501aebe64533b339707dceab06de | S1 explicit |
| c10-memit-knobs-failed-before-anyedit.md | S1, S2 | S1: 1324 / 331; S2: 1324 / 331 | IDENTICAL; S1=S2: 9c349ea3c2a4e07d8954422801e4d7e7a194b60b869fdc2ebdd61641629c13c8 | S1 explicit; matching Claude cache on recall |
| c10-mint2-r3-provisional-no-direction.md | S1, S2 | S1: 1748 / 437; S2: 1748 / 437 | IDENTICAL; S1=S2: aaa00927ad0ca237fdf3f5b4fc23c8a916b1cd8b1f0858d160ff6f63a4a549d0 | S1 explicit; matching Claude cache on recall |
| c10-secondkey-null-large-write.md | S1 | S1: 1598 / 400 | ONLY; S1: fa911bad1801adaf890b2d7a10492c886aef24b931fa5f966c5c571539629fab | S1 explicit |
| c10-sharedz-underfit.md | S1 | S1: 2621 / 656 | ONLY; S1: 20e495d793fbfa24b04b3e68a9f7eb72977c9580cef517c6edfa38b05fa25a0b | S1 explicit |
| c10-solvefeas-underfit-at-50.md | S1 | S1: 402 / 101 | ONLY; S1: bad0dd34af879ef485bcc0de3fef4e20e4309367921534f355cf27d7177dc38a | S1 explicit |
| c10-stacked-solve-tradeoff.md | S1 | S1: 1719 / 430 | ONLY; S1: 3c86e5a953dd7fdd228cc6d069665a8b837fc3a25ae98972dfbc8e426581dc9e | S1 explicit |
| c10-status-and-session-b-residual-test.md | S1 | S1: 605 / 152 | ONLY; S1: 8d2bcb238d5f0129f4cbc4f4942ee9122deef0e888a554083980824f3d5e7495 | S1 explicit |
| c10-twopass-solve-null-at-margin.md | S1 | S1: 1476 / 369 | ONLY; S1: bf8f1fa03db3c48542a7a1c6d2b06516f0e31cb227046a047c09e9b7e3bfd08d | S1 explicit |
| c10e-harness-restores-band-only.md | S1, S2 | S1: 990 / 248; S2: 990 / 248 | IDENTICAL; S1=S2: bddda186dec75f5dc7bd7b7a2844ca5ec90e2ccb009136022a2fa2fd16133422 | S1 explicit; matching Claude cache on recall |
| c10k-route-a-resume.md | S1, S2 | S1: 611 / 153; S2: 611 / 153 | IDENTICAL; S1=S2: bdc4cd83e537cf2634c0c3090248733e07fc5964468ecc26f527e91373eda5e6 | S1 explicit; matching Claude cache on recall |
| c10w-ceiling-oracle-result.md | S1, S2 | S1: 1341 / 336; S2: 1341 / 336 | IDENTICAL; S1=S2: 896fb3c536f0c392159321fe28984e37172fe6fe0809e3f1051939e0df5a01bd | S1 explicit; matching Claude cache on recall |
| c10x-enginepath-result.md | S1, S2 | S1: 1933 / 484; S2: 1933 / 484 | IDENTICAL; S1=S2: 935664ed8ab0a532a074cb222d069e5d1f7c96577af11d2b4e7773a301fe98af | S1 explicit; matching Claude cache on recall |
| c10y-deferred-behind-drive-backup.md | S1 | S1: 1213 / 304 | ONLY; S1: 546f0f7038cb1a0de49be3f80ad1548a9e5803e176b23e6ad0994649ce00d6b2 | S1 explicit |
| c10z-a1-population-byte-identity.md | S1, S2 | S1: 497 / 125; S2: 497 / 125 | IDENTICAL; S1=S2: 3005997f6199c4daa28ae694623990ac18088a18539f3c58a21a1c25d12040e4 | S1 explicit; matching Claude cache on recall |
| c10z-stage1-underfit-terminal.md | S1, S2 | S1: 552 / 138; S2: 552 / 138 | IDENTICAL; S1=S2: cf1e2901a9866c2285af1081baca704fc74ebbd0d052664121a30e93c472ade2 | S1 explicit; matching Claude cache on recall |
| calibrate-confidence-mechanics-vs-contracts.md | S1, S2 | S1: 1528 / 382; S2: 1528 / 382 | IDENTICAL; S1=S2: 86a22ea0ed8299ec85d7b4e0caf159a4cbf25a3fe18dd04598d22ebf0eeaee61 | S1 explicit; matching Claude cache on recall |
| calibrate-symmetrically-unresolved-is-a-verdict.md | S1, S2 | S1: 2028 / 507; S2: 2028 / 507 | IDENTICAL; S1=S2: 9bd71105f4bc56c75d5cba27a7fd657d82546d3cfaf1cb4f60ab649886f83daf | S1 explicit; matching Claude cache on recall |
| canonical-fit-is-not-c10-rescue.md | S1 | S1: 468 / 117 | ONLY; S1: 24ac902ecebe201320b910812dc8b341c34ed97643f3363ab11939540866d146 | S1 explicit |
| check-for-running-duplicate-before-launch.md | S1 | S1: 1055 / 264 | ONLY; S1: 68bdb13e77d113a673e3d1747ba744cd8fd3ad14978586ba4b2e5b54712eb717 | S1 explicit |
| claude-subscription-advisor-for-codex.md | S1, S2 | S1: 1503 / 376; S2: 1503 / 376 | IDENTICAL; S1=S2: 5cdd939a62372666b44db2b3519b2f627d90e7146416e5ca19b27872382063d0 | S1 explicit; matching Claude cache on recall |
| closeout-gate-before-done.md | S1, S2 | S1: 3966 / 992; S2: 3966 / 992 | IDENTICAL; S1=S2: 3655dd52220a36c46077cfc902727a6c6ee7c86ea7a5fb463da6f0ea47d0cb0f | S1 explicit; matching Claude cache on recall |
| clustered-design-power-determinism-cheaper-lever.md | S1, S2 | S1: 3085 / 772; S2: 3085 / 772 | IDENTICAL; S1=S2: aa4982e07dd262b934f5f9c3c614d1d7a0637ccbb83c56c0f5bc72860365de00 | S1 explicit; matching Claude cache on recall |
| clustered-editing-trials-sampling-unit.md | S1, S2 | S1: 2643 / 661; S2: 2643 / 661 | IDENTICAL; S1=S2: ecafe797eee2ea78d9c516fa8615f8fcf2dfcfe87f4b0a64cffb1a80ec5c3fa3 | S1 explicit; matching Claude cache on recall |
| codex-brief-handoff-file-narrow-reads.md | S1 | S1: 1451 / 363 | ONLY; S1: 83030b0d38a9302d2f15b685169b29c187a3bb25071b370b809a198af06cdb2a | S1 explicit |
| codex-chatgpt-oauth-model-slug.md | S1 | S1: 558 / 140 | ONLY; S1: ffe94735bc3404e13cfafd5787f3727bac374834326c02effff2f436f59a4ae2 | S1 explicit |
| codex-hook-trust-prompt-at-launch.md | S1 | S1: 941 / 236 | ONLY; S1: a929f9890de88ba7e19eb88ad7fa9756396c424956a7a55cfcf83014e997137e | S1 explicit |
| codex-review-embed-evidence-and-effort.md | S1 | S1: 597 / 150 | ONLY; S1: 008f03568e97c938739e96a1d679d7f0282eb982e379388cb6cf4dfede896308 | S1 explicit |
| codex-runs-inline-from-claude-bash.md | S1, S2 | S1: 2477 / 620; S2: 2477 / 620 | IDENTICAL; S1=S2: 69e64376e9110c64b43c86529191f146a8bee64655fbff2069060efcfa922c78 | S1 explicit; matching Claude cache on recall |
| codex-sandbox-no-network.md | S1, S2 | S1: 776 / 194; S2: 776 / 194 | IDENTICAL; S1=S2: 5c4c26cbc042df3749b0ae50c0d148ddc8638152bc92f53e2a2bd050d0e9d28e | S1 explicit; matching Claude cache on recall |
| codex-session-can-type-into-maestro-pane.md | S3 | S3: 1251 / 313 | ONLY; S3: ad823ab923c598b6542fe571fb7146391b6e0db4b033a45a050198c6b1087e9a | S3 recall; absent Git/Codex recall |
| codex-watch-anchor-replies-read-context-from-rollout.md | S1 | S1: 3428 / 857 | ONLY; S1: d4d7b865a270d866d80d3852b62122c48842c04d020209e19b5cc07d17a44e36 | S1 explicit |
| codex-watch-anchor-tokens-read-context-from-rollout.md | S1 | S1: 1845 / 462 | ONLY; S1: 3a2703258b287f1a558c3c400cf2ad79c39d45e84f015fe076085b3ca3f6aa37 | S1 explicit |
| codex-web-review-lanes.md | S1 | S1: 1605 / 402 | ONLY; S1: 5a9137cd091e2cea435a010985999660bff65c52bb44afbc71f9d40bcff83b05 | S1 explicit |
| commit-forward-work-without-asking.md | S1, S2 | S1: 2287 / 572; S2: 2287 / 572 | IDENTICAL; S1=S2: 1ca98b3a3b94fc33e6eb1ee42bcf58abc6289bc32fc7bc177069caef474faecd | S1 explicit; matching Claude cache on recall |
| commit-verified-bytes-before-successor.md | S3 | S3: 1258 / 315 | ONLY; S3: db7471b7dacfb42a1587ce8a55e80580d4fa23aba8567d2eac479abedc2a64c9 | S3 recall; absent Git/Codex recall |
| confirmed-delegated-is-not-delivered.md | S1, S2 | S1: 2460 / 615; S2: 2460 / 615 | IDENTICAL; S1=S2: af008a44127f23ff27ee2eea978897ddb9c893c9700a9bbcb9ba9151a260fffe | S1 explicit; matching Claude cache on recall |
| connected-papers-api.md | S1, S2 | S1: 1713 / 429; S2: 1713 / 429 | IDENTICAL; S1=S2: 460681881a1c300cc979ec551eb1768c76cd7cc12e1ed3c3516a20458922f29b | S1 explicit; matching Claude cache on recall |
| context-management-every-session.md | S1, S2 | S1: 4006 / 1002; S2: 4006 / 1002 | IDENTICAL; S1=S2: cfcf879a53cd21c7c2072b811ef5eb29b6391ca9ea22620e74f6db45c558bf86 | S1 explicit; matching Claude cache on recall |
| control-relation-effective-cardinality.md | S1, S2 | S1: 1552 / 388; S2: 1552 / 388 | IDENTICAL; S1=S2: d0ea284e6afa91d3f5df786f9220645f18a5cfeffbeda6cff29dd8c8f8197ac9 | S1 explicit; matching Claude cache on recall |
| corpus44-rho-is-remaining-residual.md | S1, S2 | S1: 1884 / 471; S2: 1884 / 471 | IDENTICAL; S1=S2: 5ae8650538ec996e64a3f0687aa50b5cff599c9388e32c7d480318c1c8f0fd18 | S1 explicit; matching Claude cache on recall |
| cross-process-contracts-one-enforcer.md | S1 | S1: 2534 / 634 | ONLY; S1: 14093f9a3a619cee210aab715c45f972a6cd36d5f543612e7dd91dbba9fe996b | S1 explicit |
| dashboard-live-derivation.md | S1, S2 | S1: 2044 / 511; S2: 2044 / 511 | IDENTICAL; S1=S2: 82511f1d642e101f4015861278f48281420dc58f65a025c59760ae94a2249548 | S1 explicit; matching Claude cache on recall |
| decision-id-check-before-assigning.md | S1 | S1: 1098 / 275 | ONLY; S1: 338aef5fd790db2a88663df128a7b39ba2a372df2cc8fb4c8ef6c61061502724 | S1 explicit |
| default-to-the-less-flattering-reading.md | S1, S2 | S1: 2920 / 730; S2: 2920 / 730 | IDENTICAL; S1=S2: f0389244dde39b2227856fcc63e53e5bc3bc2c0df5d63e95ee61f95de55c4022 | S1 explicit; matching Claude cache on recall |
| deployment-target-intel-cpu.md | S1 | S1: 599 / 150 | ONLY; S1: d7ea7004d4fded438225d81f2d12ab019eb369bff18967ea296f1014a970cf0b | S1 explicit |
| deterministic-null-label-can-hide-real-effect.md | S1, S2 | S1: 2046 / 512; S2: 2046 / 512 | IDENTICAL; S1=S2: 1ac16a8ec03ba592311f6a690a271220cc62b59504be62b5241df3c94748e600 | S1 explicit; matching Claude cache on recall |
| disk-budget-before-dispatch.md | S1, S2 | S1: 1773 / 444; S2: 1773 / 444 | IDENTICAL; S1=S2: d2f8833773d35430e258174cfab363b3328a1172ad14ba3e1522490bc25adc23 | S1 explicit; matching Claude cache on recall |
| dry-admission-probe-before-one-shot.md | S1, S3 | S1: 1460 / 365; S3: 1460 / 365 | IDENTICAL; S1=S3: b8278374b0839af2e0cb8e4caa6d68e2eafa74cc5fee4796369ffd608ba69a7f | S1 explicit; matching Claude cache on recall |
| durable-artifact-path-collision.md | S1, S2 | S1: 2476 / 619; S2: 2476 / 619 | IDENTICAL; S1=S2: bc877ecd93e1fd7ae7b3371143835500221d72ae345a12515e8c5f4235045a88 | S1 explicit; matching Claude cache on recall |
| e2e-ground-truth-situate-on-the-map.md | S1 | S1: 465 / 117 | ONLY; S1: a1f717412be681a9645ced5d3001dd5542f6c4b288e0109ac19d39da3ed36c2d | S1 explicit |
| easyedit-assets-vendored.md | S1, S2 | S1: 1410 / 353; S2: 1410 / 353 | IDENTICAL; S1=S2: b768041040daf984b3ca1ba273461ad0ea5056475e1c149cc214470cbcdf3abf | S1 explicit; matching Claude cache on recall |
| editing-memory-eval-prior-art-landscape.md | S1, S2 | S1: 5246 / 1312; S2: 5246 / 1312 | IDENTICAL; S1=S2: 00f198d07830baa34476193dd99f0de813c11814f07746e6d73927e082db9e53 | S1 explicit; matching Claude cache on recall |
| encode-recurring-discipline-as-a-gate.md | S1, S2 | S1: 1956 / 489; S2: 1956 / 489 | IDENTICAL; S1=S2: 6cefcffe70df4976d4e263a0fe2e3f738e613b7947ae1afc39d982396143a2e5 | S1 explicit; matching Claude cache on recall |
| evidence-over-scaffolding.md | S1, S2 | S1: 2469 / 618; S2: 2469 / 618 | IDENTICAL; S1=S2: 09d2606003678a7aa90db646f405defbf3a10bc16ed6183eea88ac7dfe7002b4 | S1 explicit; matching Claude cache on recall |
| exhaust-options-before-blocked.md | S1 | S1: 1550 / 388 | ONLY; S1: 8c13bf57db4b71994e16d772c705080f2560da61ce8d60dded0a8e57e7cd6233 | S1 explicit |
| experiment-gate-before-next-science-arc.md | S1 | S1: 541 / 136 | ONLY; S1: 093260664068e7fd94a5ce5185dc238e487d34619cd8dd10d2722bd852338bfa | S1 explicit |
| experiment-runbook-is-canonical.md | S1, S2 | S1: 1782 / 446; S2: 1782 / 446 | IDENTICAL; S1=S2: 6c91eda012a2c8e3b3c29934b93f2bb9939e652b666e54609816ecd47dc1c275 | S1 explicit; matching Claude cache on recall |
| fallback-that-nullifies-spec-is-not-f1-closure.md | S1, S2 | S1: 2821 / 706; S2: 2821 / 706 | IDENTICAL; S1=S2: 7861debfe877f5e4e652d30154ec1824eed15d9b170c843ac70154fe9f9a76ff | S1 explicit; matching Claude cache on recall |
| fan-out-synthesis-subagent-results-are-leads.md | S1, S2 | S1: 2707 / 677; S2: 2707 / 677 | IDENTICAL; S1=S2: 951ccc7f1126654c89c78912d5298b8c949e944c8707e5bdeab189f98d754931 | S1 explicit; matching Claude cache on recall |
| fixed-budget-sweep-couples-iv-with-complement.md | S1, S2 | S1: 4581 / 1146; S2: 4581 / 1146 | IDENTICAL; S1=S2: b4e72de4d457407b59ad7b31fc5d3c69ba4e2a519f9a01f01cf269d80dd537bf | S1 explicit; matching Claude cache on recall |
| fp32-reductions-over-big-tensors.md | S1, S2 | S1: 1112 / 278; S2: 1112 / 278 | IDENTICAL; S1=S2: b43ca6fe9d9d9f09e326e14a67431775eae09dc355c7ed6b9c1806d4f6a173a4 | S1 explicit; matching Claude cache on recall |
| gdrive-rclone-remote.md | S1, S2, S3 | S1: 1724 / 431; S2: 1724 / 431; S3: 1809 / 453 | COLLISION; S1=S2: 4ec2fc108de09359592bf7a4c7c2b32fd107eed5468105a68fdeb2807e7809a9; S3: be30f1b88e2f5affd83284446253c9b3108f7b57e611d5232aed9de8d64289b2 | S1 explicit; matching Claude cache on recall |
| gemma4-rung4-candidate.md | S1 | S1: 573 / 144 | ONLY; S1: f4f8b8b9d1c1ae55121cb31efc5cc2f5033b071abd128ff387876cd7bcf56a57 | S1 explicit |
| git-add-all-leaks-secrets-on-public-repo.md | S1, S2 | S1: 2488 / 622; S2: 2488 / 622 | IDENTICAL; S1=S2: 0b811d90f82763dd5afdb76286ed7b9ac90bc87eb3ee0aa7ba2a593c2da8937e | S1 explicit; matching Claude cache on recall |
| gpu-gate-blocks-any-python.md | S1, S2 | S1: 471 / 118; S2: 471 / 118 | IDENTICAL; S1=S2: 75c5091b2b21f6a79fcbe3ee0616d357a17c6dd00af89030ae83e30fe86fa93f | S1 explicit; matching Claude cache on recall |
| gpu-gate-refuses-any-venv-python.md | S1, S2 | S1: 2960 / 740; S2: 2960 / 740 | IDENTICAL; S1=S2: e56bea60b8b94976871d09c7b249c5c3622c0d93092305c51024357292ce0b07 | S1 explicit; matching Claude cache on recall |
| graft-disabled-audit-2026-10-08.md | S1, S2 | S1: 2332 / 583; S2: 1884 / 471 | COLLISION; S1: a87803e61e1e869e2ba5cca9ad43172f039c13b92a067b5a83aaf1d23dcad30a; S2: b150e7007c272f87edd8f13775615a4358c7409a7376c05012e4dd2a9b71c256 | S1 explicit; matching Claude cache on recall |
| importing-external-files-traps.md | S1 | S1: 1809 / 453 | ONLY; S1: ab5d566995d09576743920a59bf10ca1e5cb8e9e21ae5ef07b0d6f6d61a351c6 | S1 explicit |
| in-weight-falsifier-must-be-weights-owned.md | S1, S2 | S1: 4759 / 1190; S2: 4759 / 1190 | IDENTICAL; S1=S2: 88e803947ff2c12d3f44952750b381410fc4bf72c9753ab9f5f49d2c4a97e97c | S1 explicit; matching Claude cache on recall |
| in-weight-knowing-insert-robust-update-fragile.md | S1, S2 | S1: 2135 / 534; S2: 2135 / 534 | IDENTICAL; S1=S2: 32cdce83846cac0ca570edce711ef362d1d819ec10693fe7b63f7bbf96a4c2d0 | S1 explicit; matching Claude cache on recall |
| in-weight-logprob-reconciliation-is-bleed-unsound.md | S1, S2 | S1: 3927 / 982; S2: 3927 / 982 | IDENTICAL; S1=S2: a5dc4de99670e9cdf47b40aac6617d585fb6d1419b24c72a301e6c017b36e3f1 | S1 explicit; matching Claude cache on recall |
| in-weight-necessity-is-scope-keyed-hybrid.md | S1, S2 | S1: 6318 / 1580; S2: 6318 / 1580 | IDENTICAL; S1=S2: 05fdbb00aa0670c9901f3fd1182567ab56a0c14291ed7b60cb1b43c62f8381f1 | S1 explicit; matching Claude cache on recall |
| in-weight-value-expression-experiment-design.md | S1, S2 | S1: 3193 / 799; S2: 3193 / 799 | IDENTICAL; S1=S2: 61690ac78480e072abceb35a0f657b04eadbf73b5e72c820dda0b0da5bb80439 | S1 explicit; matching Claude cache on recall |
| in-weight-vs-sidestore-f1-question.md | S1 | S1: 534 / 134 | ONLY; S1: 859a4ef0b24e366c0d61ea9449fe2a1689e03d793bac9831fa4c53fc59c49602 | S1 explicit |
| infra-closeout-template-d-hw-2.md | S1, S3 | S1: 1271 / 318; S3: 1271 / 318 | IDENTICAL; S1=S3: 3c86a2fbb5cf233559c9e089d89e381ca539a5401281f877fd3bcd8df614ac60 | S1 explicit; matching Claude cache on recall |
| infranodus-discourse-lens-not-coverage-tool.md | S1, S2 | S1: 4258 / 1065; S2: 4258 / 1065 | IDENTICAL; S1=S2: a080ea761758d74255f72732d069674cd7d80cba5da20242771a5ec2796cc646 | S1 explicit; matching Claude cache on recall |
| infranodus-standing-approval.md | S1, S2 | S1: 1341 / 336; S2: 1341 / 336 | IDENTICAL; S1=S2: 4e3071844e0840cd296192a266c0dab9c8a6338e19e8d1425a26316b992a315e | S1 explicit; matching Claude cache on recall |
| injection-control-is-a-stratum-not-a-floor.md | S1, S2 | S1: 1335 / 334; S2: 1335 / 334 | IDENTICAL; S1=S2: 6384142d4603be83d56b806a5452b1058d6d328e163e6fd39a6fcf889de49525 | S1 explicit; matching Claude cache on recall |
| intel-exists-to-offload-the-m3.md | S1, S3 | S1: 1368 / 342; S3: 1368 / 342 | IDENTICAL; S1=S3: a9aae70793ca078d85a50c41c953b9c5582b849873c021905602a92fd8742c07 | S1 explicit; matching Claude cache on recall |
| intel-mac-node-access.md | S1 | S1: 3830 / 958 | ONLY; S1: a8f0e552b397d92f60d128c61643f071395456def0300f43ef3ec89efec990fa | S1 explicit |
| interactive-codex-brainstorm-sessions.md | S3 | S3: 1341 / 336 | ONLY; S3: 00893c867d958adbd9ddb2df13eb6b5055d8f37e6d744ebff4e4f1dac630180e | S3 recall; absent Git/Codex recall |
| lab-view-and-live-telemetry.md | S1, S2 | S1: 2170 / 543; S2: 2170 / 543 | IDENTICAL; S1=S2: 798382e7d81a360a4a1a471c39f23d6fd83fdf8351a3595ae1d26462adc373bf | S1 explicit; matching Claude cache on recall |
| labviz-wireframe-before-spec-approval.md | S1, S3 | S1: 2040 / 510; S3: 2040 / 510 | IDENTICAL; S1=S3: d06ba31337ad55520fd46943eb1b40d11f4a6ede8fc93fecca72caa9c3206f09 | S1 explicit; matching Claude cache on recall |
| larql-the-mechanism-prior-art.md | S1 | S1: 529 / 133 | ONLY; S1: 85d03b98e444e9d20447c63dc7bff22c567d2e05f5b93e6d1c63a8fa9144f72d | S1 explicit |
| last-token-keyed-write-is-a-frame-write.md | S1, S2 | S1: 2139 / 535; S2: 2139 / 535 | IDENTICAL; S1=S2: ddb45afcd1c4191002ed17ce12ee9fd8518b43865bb80fbbc03d25fcf7497af6 | S1 explicit; matching Claude cache on recall |
| llm-as-database-program-overview.md | S1, S2 | S1: 1616 / 404; S2: 1616 / 404 | IDENTICAL; S1=S2: 987d3e3fc9b0881b955bf79fe1d51683cb22a45a38d48b39c329a9f086025650 | S1 explicit; matching Claude cache on recall |
| llm-db-local-migration-gaps.md | S1, S2 | S1: 613 / 154; S2: 613 / 154 | IDENTICAL; S1=S2: c32bb491f0f9119e2a5c8431038ba23c0a062618227b26c1cd00645208134b13 | S1 explicit; matching Claude cache on recall |
| llmdb-root-env-points-at-main-checkout.md | S1, S2 | S1: 2284 / 571; S2: 2284 / 571 | IDENTICAL; S1=S2: 1ebb2d65a445f307e3570a341b8000b06860c93ff791038497d9e48cdd3c4ef2 | S1 explicit; matching Claude cache on recall |
| llmdb-root-points-at-main-checkout.md | S1, S2 | S1: 499 / 125; S2: 499 / 125 | IDENTICAL; S1=S2: 3e63b1d392d2140c58d8e8b9a6557f01f863c9f310d01edf190dc41110442137 | S1 explicit; matching Claude cache on recall |
| local-only-hardware-rule.md | S1 | S1: 478 / 120 | ONLY; S1: 6cb6e5be97f4175f477353b7d7d73aaa67f72515ca00f3b23864306fe8ffb96d | S1 explicit |
| local-only-no-rented-compute.md | S1, S2 | S1: 1271 / 318; S2: 1271 / 318 | IDENTICAL; S1=S2: db379771fc38933e6e9242da95fe706c5a286f57d17beaf238131f80cd01fab3 | S1 explicit; matching Claude cache on recall |
| m3-hosts-the-team-no-routine-reboots.md | S1, S3 | S1: 1513 / 379; S3: 1513 / 379 | IDENTICAL; S1=S3: f4c4f128e04e2a120d78cd3def839a45715be4ed6affd3388a3ddd7cbd8e70e7 | S1 explicit; matching Claude cache on recall |
| maestro-hash-pin-edits-go-to-builders.md | S3 | S3: 1236 / 309 | ONLY; S3: e4d8a3b050f395cfaf68f118b553e7bdc3e2a65294e687bb7f67c3343edf59ce | S3 recall; absent Git/Codex recall |
| match-metric-to-the-claim.md | S1, S2 | S1: 4059 / 1015; S2: 4059 / 1015 | IDENTICAL; S1=S2: b31fd403521b646d34b2843efd9f5c172363689a7ec661b75434136bd0dc6020 | S1 explicit; matching Claude cache on recall |
| mathlab-calibration-stop-scope.md | S1, S2 | S1: 655 / 164; S2: 655 / 164 | IDENTICAL; S1=S2: 6bddd763b34853ac1f42800dab04f173989b5743fa45e45217e28830451b3a8c | S1 explicit; matching Claude cache on recall |
| mathlab-native-norm-contract.md | S1, S2 | S1: 630 / 158; S2: 630 / 158 | IDENTICAL; S1=S2: 141141b641a11a515670aa400385b6eb3b4c2936379d2319a695789410d139f7 | S1 explicit; matching Claude cache on recall |
| mbp-command-line-tools-broken.md | S1, S2 | S1: 1381 / 346; S2: 1381 / 346 | IDENTICAL; S1=S2: bedb098ef9fc6e28854aeec3ca2e8a575c8fcf3c119d6016a0dc19d2f12346ea | S1 explicit; matching Claude cache on recall |
| mbp-shell-aliases-trap.md | S1, S2 | S1: 1337 / 335; S2: 1337 / 335 | IDENTICAL; S1=S2: 97d49313997cf3117d3fd898b3cfa68a7b565173142d9a2beb9a039356156eb5 | S1 explicit; matching Claude cache on recall |
| memit-cov-inversion-not-a-hang.md | S1 | S1: 524 / 131 | ONLY; S1: 4e57b48c6981511df316cac62536850b78198b4d022c8fb80e9fd4aa3fc121b4 | S1 explicit |
| memory-paths-and-mirror-discipline.md | S1, S2 | S1: 1923 / 481; S2: 1923 / 481 | IDENTICAL; S1=S2: d570e3170c715c9ef6f75c667f9176304057bf9e7668a2863bd7c197adfc0b74 | S1 explicit; matching Claude cache on recall |
| merge-gate-first-use-learnings.md | S1, S3 | S1: 1297 / 325; S3: 1297 / 325 | IDENTICAL; S1=S3: 4ee1dc53ce36596db2564f250739a15a6c14688342a3b03d140b35c36be1be8b | S1 explicit; matching Claude cache on recall |
| method-ports-need-replication-faithfulness-gate.md | S1, S2 | S1: 1299 / 325; S2: 1299 / 325 | IDENTICAL; S1=S2: f410c8069fee5330b0b856f9c495a00b9821d32980ef49a29a22c06b20a666f3 | S1 explicit; matching Claude cache on recall |
| mint-replication-spread-and-gguf-survival.md | S1, S2 | S1: 1554 / 389; S2: 1554 / 389 | IDENTICAL; S1=S2: 08addd3efdc228fb18d59d49baefca2a9bc817abb5ee8d860e012909634809be | S1 explicit; matching Claude cache on recall |
| model-and-compute-allocation.md | S1, S2 | S1: 3381 / 846; S2: 3381 / 846 | IDENTICAL; S1=S2: e9d4f0036c92316e09daa59d5448410d888f76ac88f796de63fb19dee3d8ad68 | S1 explicit; matching Claude cache on recall |
| molab-migration-assessment.md | S1 | S1: 552 / 138 | ONLY; S1: c47704a92f9d90d4da82cf6f11ed26ce4d7cce9949433d5d9c40e396f92d3463 | S1 explicit |
| mps-offset-view-conversion-bug.md | S1, S2 | S1: 2196 / 549; S2: 2196 / 549 | IDENTICAL; S1=S2: 650c92db69a572f4f847a1dc0b319ca5bd00a6c4dbd2132085034ce4a54a1487 | S1 explicit; matching Claude cache on recall |
| name-the-manipulated-variable-not-the-arm-intent.md | S1, S2 | S1: 2463 / 616; S2: 2463 / 616 | IDENTICAL; S1=S2: 76608139f7e48bd04d7b95b514161e1c4caa8d85c4e16847b20ddd1bd77fb07a | S1 explicit; matching Claude cache on recall |
| native-applet-removable-volumes-prompt.md | S1 | S1: 1538 / 385 | ONLY; S1: 9ff0cc7ddaf42cbd3ff87fedf0a67766b97533c67073cedb4300df087eb14f93 | S1 explicit |
| native-knowledge-screen-is-not-editability.md | S1, S2 | S1: 3003 / 751; S2: 3003 / 751 | IDENTICAL; S1=S2: 8bed971ee08e3d600cbb2263dde7f24caa2a8cdb925c48dca31038a010363e23 | S1 explicit; matching Claude cache on recall |
| neuraldb-scr-keep-side-store-pressure-live.md | S1 | S1: 499 / 125 | ONLY; S1: 8907185506d84b931cd2935da0f6aa280b07d662f9156ba983e37a39728d3b3f | S1 explicit |
| never-idle-arm-completion-watch.md | S1, S2 | S1: 2351 / 588; S2: 2351 / 588 | IDENTICAL; S1=S2: c861e58ecad898c4c8a5d264e84f9f5b1cf8daba47d18915ed39717586741c3d | S1 explicit; matching Claude cache on recall |
| no-model-cleared-full-bars-c10-included.md | S1, S2 | S1: 758 / 190; S2: 758 / 190 | IDENTICAL; S1=S2: 8a5c76595fd628374d075a09b0f335c2375a1ac4b1497e2bb4812678548c2d56 | S1 explicit; matching Claude cache on recall |
| notebooklm-install-and-notebook-ids.md | S1 | S1: 471 / 118 | ONLY; S1: ee55591d77a55f8f220e6530df44956572b8f9ec5e3c1afb6c9b36da1cdf7a03 | S1 explicit |
| notebooklm-via-browser-harness.md | S1, S2 | S1: 1882 / 471; S2: 1882 / 471 | IDENTICAL; S1=S2: ed9a194c70f132bb90e211c8f380e6536cef67166e5efa56204f26a61613007c | S1 explicit; matching Claude cache on recall |
| ollama-serves-winning-defense-graphify.md | S1, S2 | S1: 1080 / 270; S2: 1080 / 270 | IDENTICAL; S1=S2: 6eb14a75e0da7b2fe205c8cae6feb1bd2b4422b4b7cf867f06adef12c83c10fa | S1 explicit; matching Claude cache on recall |
| one-shot-run-needs-real-scale-dry-run.md | S3 | S3: 1187 / 297 | ONLY; S3: 52e475637c98f3faa2c8af112e06a6527f000acc944f2858c20dfccc32f99cb8 | S3 recall; absent Git/Codex recall |
| operator-decision-scope.md | S1, S2 | S1: 1523 / 381; S2: 1523 / 381 | IDENTICAL; S1=S2: 7b0746fd3951e68b7a21ddd457d79b7b19c28e1e962c0d7d1870d72b6ad959e7 | S1 explicit; matching Claude cache on recall |
| operator-overnight-autonomy-2026-10-06.md | S1, S2 | S1: 3074 / 769; S2: 3074 / 769 | IDENTICAL; S1=S2: fe95f8eaf5e4dbdc7c28f533dbe586562eeb8de8806c8666c58f8914d427174a | S1 explicit; matching Claude cache on recall |
| operator-profile-and-standing-directive.md | S1, S2 | S1: 2533 / 634; S2: 2533 / 634 | IDENTICAL; S1=S2: a20cd0c5e4ec63ddbf6cbdf4cbef280e83d88925c8d0e7dbb6666de26e44f61f | S1 explicit; matching Claude cache on recall |
| operator-profile-llm-as-database.md | S1 | S1: 563 / 141 | ONLY; S1: 8a7a38411134a49acb34402af9f0082ae8b11da786af0dfb2031f9282bc21334 | S1 explicit |
| operator-scaffolding-phase-tooling.md | S1 | S1: 599 / 150 | ONLY; S1: 061b6756687b65c7349cf159f5bd22b8efde4e13da70228b2d7e9be010463dc6 | S1 explicit |
| parallel-builders-name-each-others-files.md | S1 | S1: 1171 / 293 | ONLY; S1: e83489dfa74d8bd0e9060abff75df7ff221b957655a5f178f2680879a7e4ad43 | S1 explicit |
| pass-label-not-equal-promotable-claim.md | S1, S2 | S1: 2418 / 605; S2: 2418 / 605 | IDENTICAL; S1=S2: 81b8289665898198800fe012a44c7d421dc45b771694691fd1df5f98dbf68a9b | S1 explicit; matching Claude cache on recall |
| perplexity-c10h-reranks-anyedit-failure-geometry-first.md | S1 | S1: 1551 / 388 | ONLY; S1: 5e663edc4036600564a026b8c57f2f66c037077f34386c1c958f17c3929c6117 | S1 explicit |
| perplexity-mcp-restore-from-pod-restore.md | S1 | S1: 743 / 186 | ONLY; S1: 9700bd391394d016d649c99a90b7b7a5eb9102a531c952a03758e73febf858a0 | S1 explicit |
| plain-language-to-operator.md | S1, S2 | S1: 1016 / 254; S2: 1016 / 254 | IDENTICAL; S1=S2: f462fac2b7a10a27ce749410dc97380804624cb3215170b4f363e612e149f7e7 | S1 explicit; matching Claude cache on recall |
| pod-restart-wipes-system-python-ml-stack.md | S1 | S1: 476 / 119 | ONLY; S1: db9ea520e540462f7bbe21ffd625768335ede2a909254a2901aca7ae3cf94cd6 | S1 explicit |
| pool-sizing-levers-items-then-determinism.md | S1, S2 | S1: 2797 / 700; S2: 2797 / 700 | IDENTICAL; S1=S2: 93852e554db0869de8cfe0d1e5809b9907fe4f647fe81265598d5b51ec1bf84a | S1 explicit; matching Claude cache on recall |
| prior-art-anyeditpp-2026.md | S1, S2 | S1: 1463 / 366; S2: 1463 / 366 | IDENTICAL; S1=S2: d2106bb3d314b284cc6a7ff0aa4afa28975500df44518dbeeddd0de4495c4fab | S1 explicit; matching Claude cache on recall |
| prior-art-arxiv-2607-batch.md | S1, S2 | S1: 1493 / 374; S2: 1493 / 374 | IDENTICAL; S1=S2: 0eb8443d6fc6fd388c2cfbb0a6c3ae5004cfbf10970087cd5819ca231049d0ad | S1 explicit; matching Claude cache on recall |
| prior-art-blendsql-small-models-2026.md | S1, S2 | S1: 1863 / 466; S2: 1863 / 466 | IDENTICAL; S1=S2: 2f7c345da2bab116befb0c891b7a42368e84a65031b7358a8481da0a29fb8ac2 | S1 explicit; matching Claude cache on recall |
| prior-art-chrishayuk-larql-2026-10.md | S1, S2 | S1: 2842 / 711; S2: 2842 / 711 | IDENTICAL; S1=S2: d882623c2c4b73354030a2516264883de1ebf85cce27d91642461a1073758f67 | S1 explicit; matching Claude cache on recall |
| prior-art-lre-hernandez-2024.md | S1, S2 | S1: 1469 / 368; S2: 1469 / 368 | IDENTICAL; S1=S2: beabc17d7c8a78ff88bcca0f90a024a6a81a3b98f3d1b42f27ccddcda505e7fc | S1 explicit; matching Claude cache on recall |
| prior-art-sleeping-llm-2026.md | S1, S2 | S1: 1608 / 402; S2: 1608 / 402 | IDENTICAL; S1=S2: cdf45015a19ce1cf256bfb41dd57310fe3b845dabbdd8b157bfb1f6a5679234c | S1 explicit; matching Claude cache on recall |
| prior-art-sweep-2026-10.md | S1, S2 | S1: 3011 / 753; S2: 3011 / 753 | IDENTICAL; S1=S2: 533c846996c94dd7fc85aaafbf34629e5defe1c7fbc71f3d57cb088c869a4acb | S1 explicit; matching Claude cache on recall |
| prototype-tautology-trap.md | S1, S2 | S1: 2834 / 709; S2: 2834 / 709 | IDENTICAL; S1=S2: 4ec1b36679d92816a7b624974c2e257adb1d2fcbbb7d1cbb38e800335d36c0e7 | S1 explicit; matching Claude cache on recall |
| push-on-milestones.md | S1, S2 | S1: 1184 / 296; S2: 1184 / 296 | IDENTICAL; S1=S2: b8a851d601cbbb89baf14b3cb4e7193a040c7b711bfab613912ee6559b042aec | S1 explicit; matching Claude cache on recall |
| q4km-quantization-survival-pass.md | S1 | S1: 3220 / 805 | ONLY; S1: 380d0d436a0ff63e11be8725f70db29eb2748fefc42ff0a515fb3ac4116b2dac | S1 explicit |
| qwen25-3b-super-weight-l2-down-proj.md | S1, S2 | S1: 1861 / 466; S2: 1861 / 466 | IDENTICAL; S1=S2: 444df5be64074bf3d0b8bebc7b6fcea5c6618f061298a36cecaa9083e6566586 | S1 explicit; matching Claude cache on recall |
| read-authoritative-source-fully.md | S1, S2 | S1: 1407 / 352; S2: 1407 / 352 | IDENTICAL; S1=S2: f2647b94641ea0945eda03b2575cbbe5651d382d288cc1ff4f234e242c8ce997 | S1 explicit; matching Claude cache on recall |
| read-handoff-before-launching-successor.md | S1 | S1: 1296 / 324 | ONLY; S1: fcc8cb9eb757dc3c693ae2e2ecbc96c9df0f10a6929792004733a659fcacf622 | S1 explicit |
| read-keying-locus-before-porting-an-editor.md | S1, S2 | S1: 1453 / 364; S2: 1453 / 364 | IDENTICAL; S1=S2: c03b2d2a082350199c55d9bcf273906fcb4ec1c930669dd3e36e5dc1675d3326 | S1 explicit; matching Claude cache on recall |
| readme-plain-words-summary.md | S1, S2 | S1: 939 / 235; S2: 939 / 235 | IDENTICAL; S1=S2: fc67bf3ea559049c8a4dcbb0fb429dc1d9055526cf304b4e74c9e71a24de9856 | S1 explicit; matching Claude cache on recall |
| readonly-check-runs-in-maestro-shell.md | S3 | S3: 1943 / 486 | ONLY; S3: 9af4c659116f098714fbd1f42890129d71446581017fb7f6c8e22589785cd038 | S3 recall; absent Git/Codex recall |
| record-provenance-per-test-run.md | S1 | S1: 1124 / 281 | ONLY; S1: 302c010c11499158f9a3ca8c5711328fa8de171d332bd31a5dda3b1bdaf44d1f | S1 explicit |
| remove-shared-resource-before-policing-it.md | S1, S3 | S1: 1453 / 364; S3: 1453 / 364 | IDENTICAL; S1=S3: 55524cbae43db6aada58c056ff3c6abaf6734421604a3abc15bcce0f601d069c | S1 explicit; matching Claude cache on recall |
| repo-reorganized-llmdb-root.md | S1 | S1: 554 / 139 | ONLY; S1: 0ff90c6424ba802692a8e594df59737809a8cb37cce59447bc59324c79e522df | S1 explicit |
| rerun-builder-tests-host-tmpdir.md | S1, S2, S3 | S1: 1545 / 387; S2: 1545 / 387; S3: 1545 / 387 | IDENTICAL; S1=S2=S3: b96b69baf43e8bd139423cecb27c00d34f29d908a5f57e996d36e00dc0acb9fb | S1 explicit; matching Claude cache on recall |
| rerun-never-patch.md | S1, S2 | S1: 1377 / 345; S2: 1377 / 345 | IDENTICAL; S1=S2: 828a40aaae5b6c10ad933403519f94e59955650c157bf38382e5b35331dc4477 | S1 explicit; matching Claude cache on recall |
| research-first-and-verify-tool-availability.md | S1, S2 | S1: 2977 / 745; S2: 2977 / 745 | IDENTICAL; S1=S2: 4f2b2d229302afa31fcd967777cca387eabdd96f107b8f1c4ad38e248ef8595d | S1 explicit; matching Claude cache on recall |
| research-pass-2026-10-06-sequence.md | S1 | S1: 618 / 155 | ONLY; S1: a5800ee4d65a0d71f984722845e16255e49fbae20ec42373ad08085de1b51b65 | S1 explicit |
| resolve-the-gates-real-criterion.md | S1, S2 | S1: 3088 / 772; S2: 3088 / 772 | IDENTICAL; S1=S2: 256033899188c32934cce3ac846f14c08396d08aaf0c99a680f6d7ded595cc5f | S1 explicit; matching Claude cache on recall |
| review-diminishing-returns-evidence-is-binding.md | S1, S2 | S1: 1643 / 411; S2: 1643 / 411 | IDENTICAL; S1=S2: 56526bafb9be21f6c1b1a7fdd0904af78e30629d2baf511900a06dd8f8fab366 | S1 explicit; matching Claude cache on recall |
| runpod-dashboard-vs-pod-metrics.md | S1 | S1: 451 / 113 | ONLY; S1: 29a939f92f59bcda5ac3c049fe9cc683592e1c69823be6b0e2d0ec32bbb8e124 | S1 explicit |
| runpod-durable-experiment-launch.md | S1 | S1: 494 / 124 | ONLY; S1: fee966a97a872ec2ba4b9ffe3e09cfff8aa2ffeb0853c7a79460ec293351a753 | S1 explicit |
| runpod-session-disconnect-cause.md | S1 | S1: 484 / 121 | ONLY; S1: 4e61a7d073ea510900bee44cacf5ae5d06612580f7649b20d1831871f974a9df | S1 explicit |
| sandbox-green-is-not-host-green.md | S1 | S1: 1349 / 338 | ONLY; S1: eb6613b9cbd045bc7b6ff2b3bc896b17a7a6a0ac7ec63e864f8bf1b1249d45b4 | S1 explicit |
| scope-gate-batch-is-deployment-model.md | S1 | S1: 1933 / 484 | ONLY; S1: 4d2bd74d03b9733bc615f43f6155c98d1e28eb6aa30d249427f669a662b7c3ab | S1 explicit |
| sealed-allowance-two-drift-windows.md | S3 | S3: 1323 / 331 | ONLY; S3: ac585b49c58d2a8d616c1694d629d3d6853bac429426692589c4ad68aaf1e784 | S3 recall; absent Git/Codex recall |
| seed-freezes-context-templates.md | S1, S2 | S1: 1872 / 468; S2: 1872 / 468 | IDENTICAL; S1=S2: a52c7e0de2148fa802221f0f9c7de2abafbea3ce24cd42440b58eb179312ef35 | S1 explicit; matching Claude cache on recall |
| sequential-edit-run-nondeterminism.md | S1, S2 | S1: 4533 / 1134; S2: 4533 / 1134 | IDENTICAL; S1=S2: d7e8fe143ba4774a5abdf7009bf58e0e629d0787ea57a63dad56070006b4ac50 | S1 explicit; matching Claude cache on recall |
| single-seed-limits-generality-not-significance.md | S1, S2 | S1: 1530 / 383; S2: 1530 / 383 | IDENTICAL; S1=S2: 8d8c17d4bfd2bdd93481c1b0cb726dc414c544de8eb8d960efc98e9b5cccb3f1 | S1 explicit; matching Claude cache on recall |
| skills-are-contracts-not-agents.md | S1, S2 | S1: 1542 / 386; S2: 1542 / 386 | IDENTICAL; S1=S2: ecc3812418b85726520dfb12366f0dc33e0ed1fd72d4d9e82e491e36dfb29ffd | S1 explicit; matching Claude cache on recall |
| sol-builders-blind-to-context.md | S3 | S3: 1026 / 257 | ONLY; S3: e9cd869c37e1cde9a1d562baacdcfa9442d4eb67cefc59945323d891e0072866 | S3 recall; absent Git/Codex recall |
| sol-for-sweeps-astra-for-gates.md | S3 | S3: 1355 / 339 | ONLY; S3: edf080a2eace64bebb51bd12749c0bf1fd060810f670a1f28bc0f1cc4c6bcb16 | S3 recall; absent Git/Codex recall |
| spec-coherence-audit-is-circular.md | S1, S2 | S1: 3457 / 865; S2: 3457 / 865 | IDENTICAL; S1=S2: a70931965ab66dc43ef19843a04d0d2cfe47e31b0dd28bac8ac31d2b2ad4d3e9 | S1 explicit; matching Claude cache on recall |
| stale-predecessor-watchers-steal-events.md | S3 | S3: 1103 / 276 | ONLY; S3: 305ce8b9fdc5a881ab6a4cb1b1c5add4a6607f9efa2ff81b013f9c1aa9d1ce81 | S3 recall; absent Git/Codex recall |
| standing-auth-forward-requirements.md | S1, S2 | S1: 1608 / 402; S2: 1608 / 402 | IDENTICAL; S1=S2: 470fbf0e2434523e48a48f80a31bac20c4b994f0ec24b0967aefe66f9af87329 | S1 explicit; matching Claude cache on recall |
| stop-open-ended-builder-self-audits.md | S1, S3 | S1: 1381 / 346; S3: 1381 / 346 | IDENTICAL; S1=S3: 68eb7ebabab8ddabfaa0ab7293500474dcacd2f1fd6c79451a3034af6f1987a9 | S1 explicit; matching Claude cache on recall |
| tailscale-remote-access.md | S1, S2 | S1: 1915 / 479; S2: 1915 / 479 | IDENTICAL; S1=S2: 6ee0fc05441d1f53921f0571a074bfe08e9155b1be20ca1958d74f3290772b55 | S1 explicit; matching Claude cache on recall |
| test-first-one-round-builds.md | S1, S2 | S1: 5690 / 1423; S2: 5690 / 1423 | IDENTICAL; S1=S2: 907d1a23fe24d9710efa51211dd7b040dce57376f120adecbc51e902240e6f8e | S1 explicit; matching Claude cache on recall |
| timed-chain-prebuild-gate-checker.md | S1, S3 | S1: 2090 / 523; S3: 2090 / 523 | IDENTICAL; S1=S3: 59fcf7d3adda0310129d24a4113ef58023633926b71caaa9fbb702fa219287e5 | S1 explicit; matching Claude cache on recall |
| tmux-kill-session-exact-name.md | S1, S2 | S1: 1415 / 354; S2: 1415 / 354 | IDENTICAL; S1=S2: c71c284b1a8332add2f2b613c4bf3876208f9fb06872008249060661cb3c744d | S1 explicit; matching Claude cache on recall |
| tmux-server-hang-dashboard.md | S1, S2 | S1: 1973 / 494; S2: 1973 / 494 | IDENTICAL; S1=S2: 97575dfdc180f69ec5e89263255b654c593c9801a0bb1e80ae089e16b6e91c05 | S1 explicit; matching Claude cache on recall |
| trim-builder-reading-lists.md | S1 | S1: 1464 / 366 | ONLY; S1: 447fa4be2a95d4535c4e10171f4e00784f5f1fcd6b76df45ec257bac6d6071a7 | S1 explicit |
| verify-canonical-state-edits-persist.md | S1, S2 | S1: 2218 / 555; S2: 2218 / 555 | IDENTICAL; S1=S2: c8978362ce56d40f544bfffcbaf491933a368973dbf3b8d26e109880aa6bdef2 | S1 explicit; matching Claude cache on recall |
| verify-external-artifacts-before-effort.md | S1, S2 | S1: 1955 / 489; S2: 1955 / 489 | IDENTICAL; S1=S2: 49026101d99f40b4341acdbe2d3c34ca729f8cdb1126626d3e6bea864ecd8cee | S1 explicit; matching Claude cache on recall |
| wide-intermediate-7b-editing-vram.md | S1 | S1: 3024 / 756 | ONLY; S1: 1e19fce3cf5a4670efbbab3114b71479675bd87424d097c5d291e3e9183ae362 | S1 explicit |
| work-queue-tab-keep-current.md | S1, S2 | S1: 2847 / 712; S2: 2191 / 548 | COLLISION; S1: 29294747a128d6029a26b9a8f4f3c10c7c7dcd1622e16713a2509480ed253db7; S2: 7f76649bf9b608658c3ad1c8e14a4256388bd8df893fcbec3a6600c77d8ff4aa | S1 explicit; matching Claude cache on recall |

### Unindexed filenames

**S1 (59)**: `SESSION_CHECKPOINT.md`, `anyedit-clearing-c10-would-close-tested-write-serve-scope.md`, `anyedit-connectedpapers-adds-diagnostics-not-plan-change.md`, `anyedit-default-window-collapses-c10-a7.md`, `anyedit-gate-upgraded-by-muke-coin-suit.md`, `anyedit-is-best-remaining-c10-rescue-not-assumed-fix.md`, `anyedit-local-transplant-controls-fail-before-a7.md`, `anyedit-precommit-triage-proceed-but-viability-gated.md`, `anyedit-token-alignment-gate-prevents-false-rescue.md`, `autonomy-drifts-from-kickoff-scope.md`, `autoresearch-is-not-a-faithfulness-gate.md`, `background-monitor-no-premature-read.md`, `c10-band-knobs-failed-for-hard-coined-values.md`, `c10-edit-collateral-breaks-injected-target.md`, `c10-edit-rotates-required-target-direction.md`, `c10-layerpick-null.md`, `c10-secondkey-null-large-write.md`, `c10-sharedz-underfit.md`, `c10-solvefeas-underfit-at-50.md`, `c10-stacked-solve-tradeoff.md`, `c10-status-and-session-b-residual-test.md`, `c10-twopass-solve-null-at-margin.md`, `c10k-route-a-resume.md`, `c10w-ceiling-oracle-result.md`, `c10x-enginepath-result.md`, `c10z-stage1-underfit-terminal.md`, `canonical-fit-is-not-c10-rescue.md`, `codex-chatgpt-oauth-model-slug.md`, `codex-review-embed-evidence-and-effort.md`, `codex-watch-anchor-tokens-read-context-from-rollout.md`, `deployment-target-intel-cpu.md`, `e2e-ground-truth-situate-on-the-map.md`, `exhaust-options-before-blocked.md`, `experiment-gate-before-next-science-arc.md`, `gemma4-rung4-candidate.md`, `gpu-gate-blocks-any-python.md`, `in-weight-vs-sidestore-f1-question.md`, `larql-the-mechanism-prior-art.md`, `llm-db-local-migration-gaps.md`, `llmdb-root-points-at-main-checkout.md`, `local-only-hardware-rule.md`, `mbp-command-line-tools-broken.md`, `memit-cov-inversion-not-a-hang.md`, `molab-migration-assessment.md`, `neuraldb-scr-keep-side-store-pressure-live.md`, `notebooklm-install-and-notebook-ids.md`, `operator-profile-llm-as-database.md`, `operator-scaffolding-phase-tooling.md`, `perplexity-c10h-reranks-anyedit-failure-geometry-first.md`, `perplexity-mcp-restore-from-pod-restore.md`, `pod-restart-wipes-system-python-ml-stack.md`, `q4km-quantization-survival-pass.md`, `repo-reorganized-llmdb-root.md`, `research-pass-2026-10-06-sequence.md`, `runpod-dashboard-vs-pod-metrics.md`, `runpod-durable-experiment-launch.md`, `runpod-session-disconnect-cause.md`, `scope-gate-batch-is-deployment-model.md`, `wide-intermediate-7b-editing-vram.md`.

**S2 (8)**: `c10k-route-a-resume.md`, `c10w-ceiling-oracle-result.md`, `c10x-enginepath-result.md`, `c10z-stage1-underfit-terminal.md`, `gpu-gate-blocks-any-python.md`, `llm-db-local-migration-gaps.md`, `llmdb-root-points-at-main-checkout.md`, `mbp-command-line-tools-broken.md`.

**S3 (2)**: `dry-admission-probe-before-one-shot.md`, `rerun-builder-tests-host-tmpdir.md`.

Unindexed is an observation, not a retirement verdict: S1 includes deliberate historical notes and tombstones retained by the October-10 audit (APPLIED.md:18–20). S2 and S3 also contain resolving but unindexed notes. Keep historical de-indexing intentional; do not blindly index all files or infer disappearance from lack of an index entry.

## Verdict counts

20 substantive table rows; dual verdicts counted separately: AMBIGUOUS 1 · BLOAT 1 · CONFLICT 4 · DUPLICATE 3 · FORMAT 1 · HISTORICAL 2 · KEEP 3 · MISLEADING 5 · STALE 5 · UNREACHABLE 4.

Structural results: 213 distinct filenames; 350 stored files; four collision filenames; S2-only zero; S3-only eleven; three resolving indexes; 23 missing local body links (S1 three, S2 seven, S3 thirteen); one non-note with absent frontmatter; one untracked S1 duplicate. Same-name identical copies are deliberate cache duplication, not candidates for deleting a safety rule.

No science, backup, network, provisioning, Git mutation, cache sync, note deletion, or hygiene was performed. Final snapshot is timestamped because another session wrote one S3 note during the audit. Scientific claims inside other notes were not reaccepted by this store-integrity lane.

Lines: 367
