# GPT-6-Astra (high) — r10: Google Drive backup activation readiness

Read-only. Worktree = current dir (branch `worktree-c10k-route-a`, HEAD `a091aec`). Main checkout `M` = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`.

Your r9 verdict was GO-WITH-CONDITIONS (`results/backup_gdrive_host_20261010/astra_r9_verdict.md:1`); its binding activation order is item 5 (`:13`), and condition 3 is recorded at `:20–27`. A read-only helper then wrote an activation plan that has NOT been executed: `results/backup_gdrive_host_20261010/activation_plan_maestro24.md`. §1 (`:22–57`) derives recovery floor 0. §2 (`:61–127`) lists the steps; each `[OPERATOR GO]` step waits for the operator's own go. §4 (`:147–165`) lists the stop conditions. §5 (`:169–179`) lists 9 open gaps.

The question: **is this plan ready to execute, step by step, with the operator's GO at each marked step?** Rule on items 1–5 below.

## Evidence since r9 (cite from raw files, not READMEs, where noted)

- **py3.9 run:** `results/backup_gdrive_host_20261010/py39_run_20261010T210113Z/`. Its `README.md` is UNVERIFIED (its author's context compacted). Do not rely on it.
  - Interpreter: `direct_results.json` gives `runner_executable` `/Library/Developer/CommandLineTools/usr/bin/python3`, version 3.9.6.
  - Write paths: `direct_driver.log:1–5` shows `record_start`, `classify`, `record_end`, `preflight` and `recover` each `exit=0`, all `verified: true` in `direct_results.json`. `verification.json:9` reads `all_inside_tool_versions_39: true`.
  - Addendum suite: `addendum_suite.log` (tail) reports `Ran 134 … FAILED (failures=1, skipped=14)`. The 14 skips are 9 `HeartbeatTest` and 5 `ArchiveTest`, all `HOST-PENDING: real rclone forbidden` (skip gate at `tools/test_backup_gdrive_addendum.py:28–29`). `LauncherTest` (`:2145`) was not selected (`run_safe_suites.sh:26–38`).
  - Base suite: `base_suite.log:5` says `Ran 2 tests`. Only `test_held_lock_refuses…` and `test_stale_lock_refuses…` were selected (`run_safe_suites.sh:13–14`), out of the 10 tests in `tools/test_backup_gdrive.py` (`:60–183`).
  - Real-path inventory before and after: `inventory_comparison.txt:1` = `identical`.
- **FAIL diagnosis:** `results/backup_gdrive_host_20261010/py39_heartbeat_diag_20261010T212344Z/README.md:3` gives verdict (b), a test race. 27 of 40 runs failed, all at `tools/test_backup_gdrive_addendum.py:431` (old numbering), with the same owner PID and the refusal routed to a separate file (`:18`, `:57`, `:76–78`). Raw: `matrix_results.json`, `arm_iv/run_01/`, `write_audit_run/write_audit.jsonl`.
- **Test-only fix:** commit `a091aec`, receipt `results/backup_gdrive_host_20261010/heartbeat_test_fix_20261010T214004Z/README.md`.
  - The four arms pass 10/10 each (`:29–34`).
  - The mutation fails the fixed test (`:21–25`).
  - The full safe addendum suite under 3.9 ran 134: 120 pass, 14 skip, exit 0 (`:44`; raw `full_addendum_final/arm_iii/run_01/test.log`).
  - Status tool and wrapper unchanged: `903c471f…` and `36647860…` (`:13–14`).

## My host evidence, which you cannot reproduce (2026-10-10 ~22:04Z)

- `git -C M branch --show-current; rev-parse --short HEAD origin/master` gives `master`, `557a58b`, `a424085`.
- In `M`, these are absent: `tools/backup_gdrive.sh`, `tools/backup_gdrive_status.py`, `tools/launchd/{MemitGdriveBackup.applescript,build_gdrive_applet.sh,com.rhu.memit-gdrive-backup.plist}`. `tools/backup_mirror.excludes` is present.
- `origin/master` blobs: the wrapper is `36647860…` (= reviewed). The status tool is `614a5edb…` and the applet source `446d35a6…`, both **older** than the reviewed `903c471f…` and `80c7b712…`.
- `git rev-list --count bac4fbe..HEAD` = 68, and `gh pr list --state open` is empty. The plan's "48 commits" (`activation_plan_maestro24.md:76`) was measured at `b6372c4`. 20 commits have landed since, none touching the staged files (`git diff --stat b6372c4 HEAD -- tools/backup_gdrive.sh tools/backup_gdrive_status.py tools/launchd/ tools/backup_mirror.excludes` is empty).
- `shasum -a 256 -c results/backup_gdrive_mb25_20261010T202206Z/final_sha256.txt` now gives **32 OK, 1 FAILED**: `tools/test_backup_gdrive_addendum.py` (pinned `766509ab…` at `:2`; now `b764938…` after `a091aec`). Plan step 0.1 (`activation_plan_maestro24.md:67`) expects 33 and will therefore stop.
- `ps -p 32906,32913,32914,36233,36258,36259,37109,65807 -o pid,etime`: **all 8 alive**, with etimes 03:39:50 (32906/32913/32914), 02:27:50 (36233/36258/36259), 02:27:28 (37109) and 03:04:13 (65807). The plan names only 4 of them (`:69–70`, `:176`).

## Rule on each (cite file:line)

1. **Blocker (a): staging mechanism.**
   - Production runs the wrapper in place from `M`: the applet hard-codes it (`tools/launchd/MemitGdriveBackup.applescript:2`), and the wrapper resolves the status tool beside itself (`tools/backup_gdrive.sh:12`) under `/usr/bin/python3` (`:11`).
   - The plan stages by PR, gated merge and `git merge --ff-only` of `M` (`activation_plan_maestro24.md:81–84`). It leaves whole-branch versus backup-only PR open (`:171`).
   - Facts: the branch carries unrelated in-flight work. That includes NEW-1, whose latest Astra verdict is NO-GO (`git log -1 d2f9846`). Linux CI runs no backup suite (`.github/workflows/ci.yml:35–39`), so "green CI" carries no evidence for these files. The merge gate does not update `M` (`tools/git_merge_gate.py:138`). `M` today is one `git pull` away from the **older** status tool.
   - Rule on: (i) whole-branch or backup-only PR, and the exact file set; (ii) whether in-place execution from a pull-able checkout is acceptable, or whether production bytes must be pinned (a deploy tag, a dedicated read-only checkout, or a copy outside the repo) and re-hashed per run, before step 3.1. If a per-run check needs a code change, say so; that would mean a build and re-review, not an activation edit.
2. **Blocker (c): "verified full-copy completion" is undefined.**
   - The phrase appears at `results/backup_gdrive_build_report.md:308` and is carried through each verdict (`astra_r9_verdict.md:13`). No document defines the check (`activation_plan_maestro24.md:174`).
   - The plan proposes generation-2 status exit 0 with no warnings (`:107`, `:163`), plus `rclone check --one-way --size-only` with the wrapper's excludes and `--links` (`:108`).
   - Context: the sync itself compares size and modtime (`tools/backup_gdrive.sh:123–130`). The archive tool already uses `rclone check --download --one-way` (`results/backup_gdrive_build_report.md:65`). The payload is 287,080,274,442 B in 40,412 files (`HOST_FINDINGS.md:12`).
   - Define the acceptance check: size-only, hash (Drive MD5 against a local hash of about 287 GB), `--download`, or a sampled hash. State how files changed after the run's `start` are handled, and whether `fresh backup with warnings` (`tools/backup_gdrive_status.py:642`) can ever count.
3. **Blocker (b): py3.9.** Do the evidence above, the diagnosis and `a091aec` close it?
   - Rule specifically on the base-suite gap (2 of 10 tests run under 3.9).
   - Rule on the 14 host-rclone skips and on `LauncherTest` never running under 3.9.
   - Rule on whether pin file `final_sha256.txt` must be superseded by a new pin set that includes `b764938…`.
   - The "busy-wait" nit: the commit message says the poll loop has no sleep (`git show -s a091aec`), but the committed loop sleeps 10 ms per iteration (`tools/test_backup_gdrive_addendum.py:441`, `time.sleep(0.01)`). Confirm which is true, and whether the loop's unguarded `json.loads` of the heartbeat (`:428`) can raise mid-poll.
4. **Recovery and operations.**
   - (i) Floor 0. The only evidence is the leaked receipt with no `launch_generation` (`activation_plan_maestro24.md:33`; `results/backup_gdrive_build_report.md:476`). The ambiguous path is excluded from the maximum (`tools/backup_gdrive_status.py:398–404`). The floor check is at `:409`, the barrier is `highest + 1` (`:424`), and the receipt is moved aside (`:437–438`). Is floor 0 correct? Should `recover` run under `M/.venv` 3.11 (plan `:94`, `:178`) or under production's `/usr/bin/python3` 3.9?
   - (ii) The first upload takes about 4–4.5 days under `--bwlimit '08:00,512k 23:00,off'` (`tools/backup_gdrive.sh:129`; plan `:100`). Staleness is 13 h (`tools/backup_gdrive_status.py:604`), and while the run is incomplete, status reports the barrier (`:528–529`), not health. Rule on the read window for step 3.4 (`activation_plan_maestro24.md:107`). Rule on the retry policy if generation 2 fails mid-upload (`--retries 1`, `tools/backup_gdrive.sh:127`): is it a manual re-`open` as generation 3, or recovery again? Rule on the unreviewed `caffeinate -i -s` wrapper (`:104`).
   - (iii) Retirement: `bootout` + `disable` + an optional plist move (`:124–125`, `:175`). Is that sufficient and correctly gated on item 2's check?
   - (iv) The 8 orphaned native-test processes (evidence above). Must they be cleared before step 3.1 (Allow prompt, sleep assertions, `:176`)? Is killing the 2 stubs enough (`:70`), or are all 8 named?
5. **Anything else blocking.** For example:
   - the unpinned production-app bundle (`activation_plan_maestro24.md:172`)
   - the unpinned `build_gdrive_applet.sh`, plist and excludes (`:140–142`)
   - no recovery dry-run (`:179`)
   - `RunAtLoad` false with a `StartInterval` of 21600 (`tools/launchd/com.rhu.memit-gdrive-backup.plist:17–20`)

   Restate the ordered checklist with every amendment folded in.

## Output

Under 900 words. Numbered findings, one per item above, each with file:line, the concrete failing input or schedule, and the exact required change to the plan (or to code, flagged as needing re-review). For an item with no finding, write `N. none found — <what you inspected>`. Not acceptable: restating the plan, a finding without named evidence, or "consider more testing". List every condition in the findings. The last line of your reply is exactly one of:

`VERDICT: GO` / `VERDICT: GO-WITH-CONDITIONS` (list conditions) / `VERDICT: NO-GO`
