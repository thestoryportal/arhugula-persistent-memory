# Context audit 2026-10-16: synthesis (MAESTRO)

Operator scope, verbatim: "run a context audit on MEMORY.md, AGENTS.md, CLAUDE.md to prune, fix any stale context, conflicts, collisons, and anything else that might cause context rot moving forward."
Narrowing, 2026-10-16 ~08:10 MDT, verbatim: "Subagents don't need to scan the entire repo across experiemnts, etc for science. Just how agents operate in our build workflows."
Approval, verbatim: "Approved: run the context audit on CLAUDE.md, AGENTS.md and both MEMORY.md files, and keep the OPERATING-MODEL.md reset-ruling edit."

Stores. AM = `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/` (auto-memory). M = `_system/memory/` (repo mirror). R = repo root.
Old-path resolver: `cd R && LLMDB_ROOT=$PWD .venv/bin/python code/state/resolve_path.py <old>`.

## Results that need no edit

- CLAUDE.md is clean: every path it names exists. AGENTS.md and routing.md are byte-identical to it (`code/agents/twins.py --check` exits 0).
- No broken index link in either index.

## Rulings by MAESTRO

- **Merge gate stale base.** Since 46510693 (T035, 16 Oct), the gate accepts a stale base when no file the PR changes changed on master since the merge-base and GitHub says MERGEABLE (MERGING.md:7). The 15 Oct "gate refuses stale-base PRs" is superseded. The merge-master/fresh-CI loop is only for an overlapping PR. Gate `--apply` is allow-listed since 15 Oct (no chat OK).
- **Disk.** Operator 2026-10-15 ~17:35 MDT: "I want you to autonomously mange disk storage space safely and effectively." Regenerable bulk is MAESTRO's (inspect first; delete via the allow-listed `LEAN/tools/reclaim.py LIST [--apply]`; never receipts/proof/predecessor bytes or the STORAGE.md deny-list). Any other deletion still needs a per-path ask.
- **Worktrees.** MAESTRO removes a lane worktree itself once its content is proven preserved (operator 12 Oct "You have autonomy and you assess if they can be deleted"; 14 Oct lanes released by close_unit.py).
- **Reset.** Operator 16 Oct: "You manage your own session clear reset and next session handoff using Memento. This is durable governance." Use `finalize-session --reset clear` at the ceiling or a unit's end. Never offer the operator a `/clear` plus a paste line.
- **Shared notes (in both stores).** After this round each one is byte-identical in AM and M. Reconcile per note (the newest true facts plus every still-true trap from either copy), with the operator's email address scrubbed ("the operator's Google Drive"). In M, a `[[link]]` to a note that exists only in AM gets the suffix " (Claude auto-memory, not _system/memory/)".
- **Rejected:** B2-28 (the prior-art sweep and the super-weight notes fire at different moments; both stay). Every science, experiment or prior-art path row (B2-10..36, B2-38, the science part of B1 row 32) is out of scope under the narrowing.

## E1: the auto-memory store and the shared notes

E1 owns every file in AM, plus the M copy of each shared note below. E1 does not edit M/MEMORY.md.

AM-only notes and the AM index:
- A1/A2: add AM index lines for `dry-admission-probe-before-one-shot.md` and `rerun-builder-tests-host-tmpdir.md`.
- A6: AM MEMORY.md merge-gate hook → "allow rule installed 15 Oct (no chat OK); since 16 Oct (T035) the gate accepts a stale base with no file overlap + MERGEABLE; otherwise merge master, fresh CI, gate".
- A9: sol-for-sweeps-astra-for-gates.md:11 "(CLAUDE.md)" → "(`_system/governance/OPERATING-MODEL.md` rule 3)".
- A11: context-hygiene-must-reach-every-store.md: `results/memory_audit_20261010/` → `_archive/projects/memory-audit/memory_audit_20261010/`. `results/context_audit_20261012/...` refs get "(removed in b4e29cbd; read with `git show b4e29cbd^:results/context_audit_20261012/<file>`)".
- A13: stale-predecessor-watchers-steal-events.md:17. Replace the "context_watch.py has no owner check … hand the operator the PID list once per session" passage with: "**context_watch.py** had no owner check until T040 (8ff19cc2, 16 Oct): 13 stale watchers piled up as 26 statusline shells, a plain `kill` was denied, and the operator ran `! kill`. It now exits when its claude owner dies or its transcript idles (`code/agents/context_watch.py:9-12`)." AM index hook: "context_watch.py lacks it (…)" → "context_watch.py has it since T040 (16 Oct; before that 13 stale, kill denied, operator `! kill`)".
- A14: context-ceiling-measure-after-continuation.md:24 → "At 300k, write the handoff and run Memento `finalize-session --reset clear` yourself ([[maestro-owns-reset-via-memento]]); never hand the operator a `/clear` plus a pointer." Keep the AM index's update-config clause (the handoffs carry "Do not load update-config"). Add one sentence to the note body: "Loading the `update-config` skill cost ~90k tokens in one session; edit settings files with Read+Edit instead, and since the skill is classifier-denied as Self-Modification anyway ([[build-gate-allow-rules]]), hand the operator a `!` one-liner."
- A16/A17/A18: lean-ticket-lane-traps.md. Line 3 drops ", Astra tempdir gap". Line 19 gets the prefix "(Superseded 16 Oct: `LEAN/tools/astra.sh` runs Astra with `-s workspace-write` and TMPDIR inside reviews/T/work; [[lean-tools-ship-and-cut-base]].)". Append to line 34: "Superseded 16 Oct ~06:00 MDT: ship.sh serializes land under `L/tools/land.lock` (ship.sh:114); launch it directly ([[lean-tools-ship-and-cut-base]])." AM index: "Astra cannot tempdir (MAESTRO baselines)" → "Astra has a writable TMPDIR via LEAN/tools/astra.sh"; "use a mkdir-lock shipone.sh" → "ship.sh holds its own land.lock: launch it directly"; "42 MB" → "43 MB".
- A19: icm-v2-maestro-autonomy-ruling.md. :15 "Hand the operator that exact command." → "See the 2026-10-15 paragraph below." :21 "record it and use another self-owned path." → "record it and use another self-owned path; if none exists, hand the operator one exact `!` command once (16 Oct: the operator ran `! kill` for 13 stale watchers)."
- A21/A22: icm-storage-placement-ruling.md. :10 → "The rule is now in `_system/governance/STORAGE.md:41`." :12 "(inventory, preserve, never delete)" → "(inventory, preserve; delete only regenerable bulk per [[fix-lane-evidence-fills-memit]])".
- A23: fix-lane-evidence-fills-memit.md. :18 → "remove through `LEAN/tools/reclaim.py` (see the 2026-10-16 bullet), then verify removal". :21 "propose deleting its `run/*/product/` trees" → "remove its `run/*/product/` trees that match reclaim.py ALLOWED with `reclaim.py LIST --apply`".
- A24: team-session-launch-traps.md:13. Delete the sentence "The repo CLAUDE.md / AGENTS.md Astra command still carries it — remove it there too" (graft is gone there).
- A25: team-session-launch-traps.md:14 "They point at `/workspace/...` (broken until step 6), so answer" → "Answer".
- A26: memento-reset-from-bg-job-drops-permission-mode.md:15 → "`~/.claude/settings.json:41` now sets `permissions.defaultMode` to `dontAsk`, so a flagless successor starts in dontAsk, not auto; still pass `--permission-mode auto`."
- A27: icm21-part2-and-workflow-approvals.md. After item 7 add: "Status 16 Oct: items 1 (T035), 2 (worker.md:21), 4 (LEAN/tools/astra.sh), 5 (tickets.py:149,153) and 6 (LEAN/tools/ship.sh) are DONE; item 3 unverified." Line 34 "(items 2-6)" → "(item 3)".
- A28: atomic-unit-builder-lifecycle.md:12 "(Codex `/new`, Claude `/clear`)" → "(Codex: `/quit` and relaunch, see Mechanics below; Claude `/clear`)".
- A29: replace each `results/<x>` path with its resolved path in readonly-check-runs-in-maestro-shell.md:11, interactive-codex-brainstorm-sessions.md:11 and atomic-units-parallel-worktree-lanes.md:11. compute_storage_brainstorm_20261011T054507Z/* → `knowledge/analyses/compute-storage/compute_storage_brainstorm_20261011T054507Z/*`. dashboard_integration_review_20261011/* → `projects/dashboard-integration-review/brief/*`. skills_pipeline_survey_20261012 → `projects/skills-pipeline-survey/drafts/skills_pipeline_survey_20261012/`.

Shared notes. E1 writes one reconciled text to both AM/<f> and M/<f>:
- dry-admission-probe-before-one-shot.md: use M's lines 3 and 8 (narrowed to the MathLab CPU diagnostic; "grants no run authority and cannot replace the actual run's admission recheck"). Fix the import: `sys.path.insert(0,"code");from apps.mathlab import mathlab_admit as A` (A3, A4, B2-9).
- gdrive-rclone-remote.md: use M's text (email scrubbed). Related → "`program/runbook/03-operational-hygiene-runpod-gpu-memory-disk.md:28` (§3.3a), [[backup-via-memitbackup-app]]" (A12, B1-15).
- infra-closeout-template-d-hw-2.md: `tools/closeout_check.py` → `code/gates/closeout_check.py`; `docs/program_state.json` → `program/program_state.json` (renders program/STATUS.md, _index/program-state.md, program/scorecard.md); "CLAUDE.md operating-model review/build rules" → `_system/governance/OPERATING-MODEL.md`; "memory_mirror/" → "_system/memory/" (A10, B2-6, B2-7).
- intel-exists-to-offload-the-m3.md, labviz-wireframe-before-spec-approval.md, m3-hosts-the-team-no-routine-reboots.md: fix the `results/` paths per A29 and B2-44/45 (dashboard_integration_review → `projects/dashboard-integration-review/brief/`).
- merge-gate-first-use-learnings.md: AM's content (items 4-5 and its How-to-apply), with line 3's "ask the operator in chat before --apply" → "gate --apply allow-listed since 15 Oct"; "Follow CLAUDE.md § Merging." → "Follow `_system/governance/MERGING.md`."; append to item 5: "Since 2026-10-16 (T035, git_merge_gate.py:143, MERGING.md:7) the gate accepts a stale base when no file the PR changes changed on master since the merge-base and GitHub says MERGEABLE; the merge-master/fresh-CI loop is only for an overlapping PR." (A6, A7, B2-1).
- remove-shared-resource-before-policing-it.md: AM's text (it has all four instances and the cost check), with line 7 replaced per A20: from "→ Intel reads…" up to "(operator GO" becomes "→ the initial Git+Drive concept kept memit M3-only"; after the citation add "The later adopted v4 (D-R2C-ADOPT) has the M3 push to approved Intel staging and the Intel do Drive uploads, retries and checks; the Intel never accesses memit; the push observes check_gpu and stops when science starts." Also apply the B2-44 compute_storage path and "memory_mirror/" → "_system/memory/".
- rerun-builder-tests-host-tmpdir.md: B2-39 paths → `code/tests/test_git_automation.py`, `code/apps/dashboard/dashboard_experiment.py` (note that :291 is historical; the fix is now at :133).
- stop-open-ended-builder-self-audits.md: no change.
- timed-chain-prebuild-gate-checker.md: "memory_mirror/" → "_system/memory/" (B2-6).
- work-from-main-folder-on-master.md: "removing a worktree folder needs operator approval" → "MAESTRO removes a lane worktree itself once its content is proven preserved ([[icm-v2-maestro-autonomy-ruling]])". "Rule home: CLAUDE.md § operating model" → "Rule home: `_system/governance/OPERATING-MODEL.md` § CURRENT OPERATING MODEL." (A8, B2-3, B2-4, B2-5).
- work-queue-tab-keep-current.md: add frontmatter (A5). Body: M's full text with B2-8 path swaps (`program/program_state.json`, `code/apps/dashboard/dashboard_queue.py`, `code/lab/runners/c10w_p2_gate.py` with ":35" → ":37", tab runs from the MAIN checkout, not "<worktree>"), with AM's "Since the ICM v2 merge" paragraph as the first body paragraph. Drop any M text that the AM paragraph supersedes, such as the `~/.claude/jobs/.../qset.py` path, unless it still exists on disk.
- NEW shared: copy AM/maestro-owns-reset-via-memento.md to M (governance OPERATING-MODEL.md § Context management cites it).

## E2: mirror-only notes and the M index

E2 owns M/MEMORY.md and every M note not listed under E1.
- B1-01, B1-02: context-management-every-session.md (:13 reset sentence; :18 known-gap recheck), text as in the B1 report.
- B1-03 .. B1-14, B1-16 .. B1-26: apply as written in the B1 report (`reports.md` § B1).
- B1 row 32, limited to closeout-gate-before-done, anti-drift-enforce-not-autowrite, approved-deletes-ask-then-rmtree and git-add-all-leaks-secrets-on-public-repo: bare `CORPUS/` → `evidence/CORPUS/`.
- B2-2: M/MEMORY.md merge-gate hook → "— gate --apply allow-listed 15 Oct (no chat OK); since 16 Oct (T035) a stale base with no file overlap is accepted; hygiene --dry-run early; detached integration worktree".
- B2-37 background-shell-niceness-10.md, B2-40 native-applet-removable-volumes-prompt.md, B2-41 parallel-builders-name-each-others-files.md, B2-42 cross-process-contracts-one-enforcer.md, B2-43 intel-mac-node-access.md, B2-44 (ask-astra-automatic-before-operator-chore.md only), B2-45 (codex-web-review-lanes.md only): path swaps as in the B2 report.
- Orphan: add an M index line for exhaust-options-before-blocked.md, worded from its description.
- Add an M index line for maestro-owns-reset-via-memento.md: "- [MAESTRO owns reset via Memento](maestro-owns-reset-via-memento.md) — operator 16 Oct durable governance: finalize-session --reset clear yourself; no /clear+paste".
- M/MEMORY.md stays at or under 24,400 bytes (`wc -c`).

## For the operator (outside the three files; not changed)

1. `_system/governance/STORAGE.md:8,10` and `OPERATING-MODEL.md:11,:27` still require operator approval for every deletion and every worktree removal. That contradicts the 12/14 Oct and 15 Oct rulings.
2. 33 MAESTRO lessons are only in Claude's auto-memory. Codex builders read only `_system/memory/`, so they never see them.
3. `code/gates/closeout_check.py:292` compares the wrong live memory directory (the mirror-root one, not the repo-root one in use).
4. `code/agents/claude_advisor.sh:5` still defaults to the pod path `/workspace`.
5. `~/.claude/settings.json:41` defaultMode is `dontAsk`, while successors launch with `--permission-mode auto`.
6. Untracked old-layout folders at the repo root: `results/`, `tools/`, `docs/`, `graft/`, `memit_dry_run/`.
