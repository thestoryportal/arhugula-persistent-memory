# MB22 storage dashboard build

Branch: `worktree-c10k-route-a`. Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`.

**Build verification: 26/26 tests PASS, zero skips.** Each test has an individual saved RED log, captured before the implementation existed. The final test run is [GREEN.log](GREEN.log): `Ran 26 tests in 0.416s`, `OK`. The real protected-path listings are identical. The tab has **not** been added to the running dashboard.

**Host verification limit:** the real project scan completed its `nice -n 19 du -sk -P` command in **3.010880166 seconds**, but the sandbox denied `setpriority`. Although du exited 0, the panel rejected its output and showed the error. Successful folder measurements at low priority on the host remain **UNVERIFIED**. There is no retry at normal priority and no fabricated zero sizes. `/bin/ps` was also denied; executable resolution was verified through Darwin's read-only `_NSGetExecutablePath` API instead.

## Files and final SHA-256

Only these product/test files were created or changed. `team_dashboard.sh` has exactly one launch-line addition and one header-comment change.

| File | Change | SHA-256 |
| --- | --- | --- |
| `tools/dashboard_storage.py` | Created | `e935e07736c2c004cb3b347732b20ce3cea3bdf78074f7aa08fb160ab8f5a13d` |
| `tools/dashboard_storage_tab.sh` | Created | `e847944c2e7116515d71a13ceea09c704c1fd8cc2608a5c4c0ddc27c7811e76a` |
| `tools/team_dashboard.sh` | Header plus launch line | `3db71c233305603818d605470dd85be2d346e69a18582cfed7284147b54e5008` |
| `tools/test_dashboard_storage.py` | Created | `c91d875e131fdccf6242e5f4418d288a534b1f449c0dc4bbb7345e3f281a36f1` |

[scope_before.json](scope_before.json) records the original scope hashes. The unchanged helper hashes are `413e6b80a435b9581073aa9f51574c34583ecbd98a0b5692a1586ea8e539094e` for `tools/dashboard_live.py` and `02938f27683c76a573e6a0b091351df511b15a28b1fe2c3974ef41124c0200a3` for `tools/dashboard_science_tab.sh`.

MB21 concurrently changed `tools/backup_gdrive_status.py`; it was not edited by MB22. Its observed hash after final verification was `1063228655fb3712705b617b5da9412f5b887a40e317311fc38cedd41a5a97a0`. Tests use its public `health()` function and do not depend on source line numbers. The other builders' MathLab/NEW-1 files were left alone. No commit, push, merge, live tmux command, rclone command, network call, model import or GPU run occurred.

## Behavior and criterion coverage

| Criterion | Tests | Evidence and resulting behavior |
| --- | ---: | --- |
| 1 | 3 | Idempotent add-one-window launcher tested with a fixture-only fake tmux; launch matches the existing GPU exemption; loop uses shared reload helpers. |
| 2 | 1 | AST plus exercised helper boundary: the only subprocess call is a literal `/usr/bin/nice -n 19 /usr/bin/du -sk -P ...` command. Rendering and health polling invoke no subprocess. |
| 3 | 11 | Disabled, running, finished and history `--once` snapshots at 80 and 160 columns; lock without heartbeat; completed heartbeat plus active lock; malformed input visible; health read-only proof. |
| 4 | 4 | statvfs totals/used/available free/percent; memit displayed once; sorted checkout/mirror/internal entries; canonical symlink targets counted once; whole-volume symlink targets refused; unavailable mounts show errors. |
| 5 | 6 | Fresh cache skips scanning; stale cache scans in a background thread and survives reload; attempts at least 900 seconds apart including failures; prior sizes retained on failure; first scan says `measuring…`; corrupt/future cache and du/priority errors visible. |
| 6 | 1 | Fixture snapshot preserves backup/app/LaunchAgents bytes, mtimes and listings. Final real-path before/after manifests also match. |

The main checkout is expanded into its entries, including `.claude/worktrees`, rather than counted again as a mirror total. Other `.claude` children are measured separately. Size rows report du's allocated bytes. Nested symlinks are not followed; explicit top-level symlink targets are measured once and labelled. Contained/duplicate aliases are labelled as included in the owning target. Internal project locations include `~/Backups`, `~/.claude/jobs`, the backup app if present, and `~/Library/Logs/memit-gdrive-backup*`.

The cache's canonical path is `$HOME/Library/Caches/memit-dashboard/storage_sizes.json`. It stores measurement/attempt timestamps, duration, sizes and errors. Cache writes and du both occur in the worker thread. The main loop redraws every five seconds and performs no tmux reads. Source reload waits for an active scan to finish and persist, preserving ownership of its du process. No scan runs on every redraw.

### health() read-only proof

**PROVEN for the current fixture-tested reader path.** The panel calls `backup_gdrive_status.health(Path(.../last_run.json))` in its own process. The test wraps that public function to prove it was actually called, exercises fresh successful/warning, failed, running and missing-heartbeat fixtures with launch-generation evidence, and uses a fresh/warning positive control. Every fixture file's bytes and nanosecond mtime and every directory listing are unchanged after each call; no file is created. Subprocess execution during those reads is forbidden by the test. Inspection of `health()` and the `launch_failure()` / `generation_state()` reader functions found no writer invocation. The final suite imports the concurrently maintained status module from disk with bytecode disabled.

### RED index

[RED_suite.log](RED_suite.log) is the original single 26-test invocation: 25 errors plus one failure because the new panel/launcher did not exist. [RED_index.json](RED_index.json) maps every test to its extracted, verbatim failure log and retains the command and suite exit. All logs below predate implementation.

| Criterion | Individual RED logs |
| --- | --- |
| 1 | [launch exemption](RED_test_1_launch_matches_gpu_exemption.log), [idempotence/failure](RED_test_1_idempotent_launcher_and_visible_failure_with_fake_tmux.log), [reload loop](RED_test_1_live_loop_uses_reload_without_tmux.log) |
| 2 | [no Python subprocess](RED_test_2_panel_never_invokes_python_subprocess.log) |
| 3a | [80](RED_test_3a_not_switched_on_once_80.log), [160](RED_test_3a_not_switched_on_once_160.log) |
| 3b | [80](RED_test_3b_running_once_80.log), [160](RED_test_3b_running_once_160.log), [lock](RED_test_3b_lock_without_heartbeat_is_running_not_disabled.log) |
| 3c | [80](RED_test_3c_finished_once_80.log), [160](RED_test_3c_finished_once_160.log) |
| 3d | [80](RED_test_3d_history_once_80.log), [160](RED_test_3d_history_once_160.log) |
| 3 | [health read-only](RED_test_3_health_is_reused_and_read_only_for_fixture_tree.log), [malformed input](RED_test_3_malformed_and_missing_progress_remain_visible.log) |
| 4 | [space](RED_test_4_space_uses_statvfs_and_shared_disk_once.log), [symlinks](RED_test_4_symlinks_counted_once_at_target_and_labelled.log), [rank/internal](RED_test_4_biggest_first_and_internal_project_paths_separate.log), [mount failure](RED_test_4_unavailable_mount_is_an_error_not_zero_space.log) |
| 5 | [fresh](RED_test_5_fresh_cache_skips_scan.log), [old/reload](RED_test_5_old_cache_scans_and_reload_reuses_it.log), [failure](RED_test_5_failed_scan_keeps_last_result_and_error.log), [nonblocking](RED_test_5_first_scan_is_nonblocking_and_says_measuring.log), [throttle](RED_test_5_attempts_are_at_least_fifteen_minutes_apart_even_on_failure.log), [bad cache/du](RED_test_5_bad_cache_and_du_failure_are_explicit.log) |
| 6 | [protected fixture](RED_test_6_snapshot_never_writes_backup_app_or_launchagents.log) |

Additional observed failures were saved before their fixes: [RED_cache_future.log](RED_cache_future.log) reproduces a future timestamp preventing rescan, and [RED_boundary_checks.log](RED_boundary_checks.log) reproduces both misleading old start time under an active lock and missing whole-volume refusal. [GREEN_candidate_1.log](GREEN_candidate_1.log) records the initial launch-test observation mistake: `sys.executable` reports the shim, while Darwin's executable API identifies the actual CLT `Python` binary. The launcher itself was not changed to satisfy that assertion.

Final command, from the worktree root (no test-command loops):

```sh
/usr/bin/python3 -B -m unittest tools.test_dashboard_storage -v
```

Receipt capture used `DASHBOARD_STORAGE_RECEIPTS=results/dashboard_storage_mb22_20261010T192500Z` and RTK's raw proxy around that command. `bash -n` on both launch scripts and `git diff --check` passed. Final fixtures and their cleanup are confined to this receipt directory. Earlier invocations used disposable `/private/tmp/mb22-storage-*` fixtures and `TemporaryDirectory` removed those fixtures; that deletion-scope mistake was corrected before the final run. No real backup or project data was deleted.

## Snapshots and real-machine scan

| Drive state | 80 columns | 160 columns |
| --- | --- | --- |
| Not switched on | [snapshot](once_disabled_80.txt) | [snapshot](once_disabled_160.txt) |
| Running | [snapshot](once_running_80.txt) | [snapshot](once_running_160.txt) |
| Finished | [snapshot](once_finished_80.txt) | [snapshot](once_finished_160.txt) |
| History | [snapshot](once_history_80.txt) | [snapshot](once_history_160.txt) |

All fixture snapshots use `--once COLS 32` and assert the row limit and terminal-cell width of every line. History without a saved heartbeat exit code explicitly says `exit unknown`; a clean-looking stats record is not treated as proof of a successful backup.

[real_measurement.json](real_measurement.json), [real_scan.log](real_scan.log) and [once_real_machine_160.txt](once_real_machine_160.txt) record real HOME `/Users/robertrhu` and actual statvfs reads. Scan attempt duration: **3.010880166 s**; total harness wall time: **3.011491208 s**. Error: `nice: setpriority: Operation not permitted`. The real measurement harness calls the same panel's `main()` in `--once 160 40` mode with its measured cache instance. Its cache path alone is injected into this receipt directory, since writing the real HOME cache is outside this builder's write scope. Backup sources and internal project paths still resolve from real HOME. Canonical HOME cache persistence is proven by fixtures; host cache permissions remain unverified.

The complete real snapshot, including its reserved blank rows, is linked above. Its visible content is:

```text
■ STORAGE · Drive backup and project disks
GOOGLE DRIVE BACKUP
Backup not switched on yet · waiting for activation
Health: missing or malformed launch receipt generation
PAST RUNS · newest first
 No recorded runs

DISKS · space measured now
Internal SSD: 730.2 GiB used (78.8%) · 196.2 GiB free · 926.4 GiB total
memit SSD: 338.8 GiB used (80.8%) · 80.3 GiB free · 419.1 GiB total
Development and backups share memit's physical SSD; counted once.
Project folders · not measured yet · every 15 min
Size scan error: OSError: size scan failed (exit 0): nice: setpriority: Operation not permitted
Folder sizes unavailable; no completed measurement
```

## Criterion 6: protected real paths

[protected_before.json](protected_before.json) and [protected_after.json](protected_after.json) contain listings, file SHA-256, sizes, modes and nanosecond mtimes for all real `~/Library/Logs/memit-gdrive-backup*` roots, `~/Applications/MemitGdriveBackup.app` and `~/Library/LaunchAgents`, recursively without following directory symlinks. Both list **21 paths** and are byte-identical. Both manifest SHA-256 values are:

```text
898650b9b2925919e9edb26a8f6eab7e0553045b6434238c2de11f754389308e
```

The before listing precedes the real scan and final suite; the after listing follows the final suite. Receipt tooling only reads the protected trees and writes alongside itself.

## MAESTRO17 handoff

No half-applied source changes remain. MAESTRO17 owns host verification, adding the tab and committing. Successful host priority/cache behavior and actual tmux window geometry are unverified; the fake-tmux tests do not claim deployment. Backup activation remains separate: today's panel correctly says it is not switched on yet. Use the latest MB21 status source when rerunning the suite on the host.

Exact add-tab command (recorded only, not executed):

```sh
LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' /bin/bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_storage_tab.sh' dashboard
```

The resulting pane command is exactly:

```sh
/usr/bin/python3 '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_storage.py'
```

[launch_exemption.json](launch_exemption.json) records the actual Darwin binary path and the matching existing exemption regex, including rejection of a `-B` variant. No admission rule was edited.

**Binding context directive for this handoff and successors:** watch `Context N% left` for this session and every orchestrated team session. Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work, append a handoff with completed/in-flight work, exact paths and SHA-256, risks and the next step, then reply exactly `CONTEXT HANDOFF WRITTEN`. On seeing `Context compacted`, do so immediately. Preserve the directive in every later handoff. The AGENTS.md Team mode contract also persists: test-first, scope hashes and receipts, no unauthorized real run, commit, push, merge or live dashboard mutation; MAESTRO verifies and commits.
