Latest status 2026-10-09T22:18:12.866792+00:00: **DETECTOR DONE** —114 CPU tests and10 final-source110×40 renders PASS. Final completion and handoff are appended below; the dated parked sections are historical.

# Shared GPU detector — clean stopping point

Recorded 2026-10-09T18:37:47.804372+00:00. **STOPPED CLEANLY for the operator's priority A1-population build.** Final dashboard suite: **93 tests PASS** (27 live, 53 MathLab, 13 new detector/experiment/bar controls; 1.115s). No GPU/MPS use, model load, job launch, commits, or edits to `tools/dashboard_mathlab.py`, `tools/mathlab_events.py`, `tools/labviz/**`, or job sources. Final independent re-review and live tmux activation remain pending; no DETECTOR DONE or live-visibility acceptance is claimed.

The full advisory in `results/mathlab_staging/dashboard_astra_r2.md` was read. Detection now has one implementation in `tools/dashboard_live.py`; the status bar calls its CPU-only summary CLI and the experiment tab consumes its `gpu_state()`. Existing `running` tuples remain compatible with MathLab. Rich jobs carry name, process family, oldest observed elapsed, source-derived cap and exact known directory metadata. The actual launcher source supplies 3600s harvest / 3060s V7 / 2820s pre-cast caps without importing any job. Parent/worker rows join by verified process ancestry; independent families remain separate even when their namespace strings match.

| Requirement | Test | Implementation |
|---|---|---|
| Six launcher/worker aliases, elapsed/cap, exact namespaces | `test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace` | `detect_gpu_jobs`, `job_cap`, `gpu_state` |
| Parent/worker dedup; genuine competitors retained | `test_parent_worker_and_admission_share_one_job_with_original_elapsed`, `test_unrelated_same_namespace_process_families_are_two_competing_jobs` | PID/PPID ancestry plus owner identity |
| Interpreter's own script only; prompts, inline/module code and temp copies excluded | `test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu`, `test_bash_long_option_does_not_turn_script_into_inline_code` | Token parser and anchored legacy script regex |
| Exact paths including spaces; no guessed artifact provenance | `test_quoted_run_directory_is_preserved_as_exact_token`, `test_harvest_events_directory_never_becomes_an_inferred_artifact_directory` | Token options, separate `run_dir` / `output_dir` |
| Failed process visibility never idle | `test_denied_empty_and_malformed_inventory_are_unavailable_never_idle`, `test_experiment_denied_inventory_is_visible_at_110_by_40` | Shared unavailable record, experiment error panel |
| Both UI consumers and 110×40 rendering | `test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget`, `test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs` | Real bash/shared Python CLI; generic named-job experiment panel |
| Preserve legacy stage/PIDs/job labels and existing MathLab behavior | Legacy positive control plus full existing live/MathLab suites | Backwards-compatible tuple and worker-label adapter |

**Harvest limitation:** `--run-dir` is the admission/events directory. `tools/mathlab_harvest.py:442` separately creates the tensor/manifest artifact directory, with no current run-specific recorded link. The dashboard labels the exact run/events path and **artifact output unavailable**; it never guesses the newest artifact folder. V7 and pre-cast output namespaces come from their explicit UTC and known launcher namespaces. The detector displays caps; it does not enforce or certify job deadlines.

RED→GREEN: initial 10 tests / 20 assertion failures, then 10 PASS and full 90 PASS. Read-only fallback review found prompt false positives, attached interpreter flags, long Bash options, same-namespace competing families and quoted-path truncation. Those exact controls gave additional RED (2 then 7 assertion failures), followed by **93 final PASS**. No failures are deferred in the final suite. The older live suite retains its pre-existing unclosed-file ResourceWarning, also present in baseline output.

Actual headless experiment and unchanged MathLab commands `--once 110 40` both exit 0. This sandbox denies `/bin/ps`; the experiment changed from PermissionError crash to GPU UNAVAILABLE, and MathLab retains GPU state unavailable. Active-job rendering is fixture evidence, including each requested job at 110×40; live inventory/tmux remains **UNVERIFIED**. Bar metadata controls include the existing 150-cell status-right allowance (six cells for its clock).

Claude subscription review could not run: fresh auth probe returned `loggedIn=false`, `authMethod=none`. A read-only Codex fallback review found the counterexamples above; weaker independence is retained. No final re-review after those corrections was obtained before the operator's priority switch.

```sh
TMPDIR=/private/tmp/dashboard_gpu_detector_build /usr/bin/python3 -B -m unittest -v tools.test_dashboard_live tools.test_dashboard_mathlab tools.test_dashboard_gpu_detector
/usr/bin/python3 -B tools/dashboard_experiment.py --once 110 40
/usr/bin/python3 -B tools/dashboard_mathlab.py --once 110 40
git diff --check
```

Source SHAs at stopping point:

| File | SHA-256 |
|---|---|
| `tools/dashboard_live.py` | `5d7d9dd84eb4bb4dc9c37334ec2b6321300c82f5e15d152f1e791c091deade4c` |
| `tools/dashboard_bar.sh` | `535e04d3ea0357183e9448e95e88a673294d83aba4772208be545c2f8e3a4b0e` |
| `tools/dashboard_experiment.py` | `ff81df2a43031bb25c2cd721625b61661bc6237d8731d24a0190f8ec56c03647` |
| `tools/test_dashboard_live.py` | `b9fec5d1c0eceea40e5caad6222d56447352cf79cdbeb0ac8f984ec25e9ed81d` |
| `tools/test_dashboard_gpu_detector.py` | `886f4d114180a785cfe42c453dab9a6019d4eb7f0146eb0c432c8d9f225a1aad` |

Protected-snapshot drift: tools/labviz/test_mathlab.cjs, tools/mathlab_harvest.py. Concurrent shared edits are preserved; this is not a global clean-tree claim.

The initial temporary capture helper used an incorrect absolute Claude CLI path after recording both baseline outputs; the error was surfaced and the actual PATH-resolved CLI auth result is recorded below. No dependency install or permission escalation occurred.

## baseline_live.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_live']`; exit 0.

```text
test_clean_finish_is_not_an_alert (tools.test_dashboard_live.Alerts) ... ok
test_new_step_resets_the_clock (tools.test_dashboard_live.Alerts) ... ok
test_no_progress_while_working (tools.test_dashboard_live.Alerts) ... ok
test_stopped_on_an_error (tools.test_dashboard_live.Alerts) ... ok
test_waiting_for_an_answer (tools.test_dashboard_live.Alerts) ... ok
test_visible_width_only (tools.test_dashboard_live.Clip) ... ok
test_last_exit_line (tools.test_dashboard_live.Coordinator) ... ok
test_no_exit_yet (tools.test_dashboard_live.Coordinator) ... ok
test_real_subprocess_nonzero_and_empty_responses_are_unavailable (tools.test_dashboard_live.GPUInventory) ... ok
test_shared_detector_recognizes_harvest_but_not_a_prompt_or_temp_copy (tools.test_dashboard_live.GPUInventory) ... ok
test_successful_nonempty_inventory_can_report_no_gpu_job (tools.test_dashboard_live.GPUInventory) ... ok
test_clean_exit_reads_finished (tools.test_dashboard_live.NowLines) ... ok
test_order_and_wording (tools.test_dashboard_live.NowLines) ... ok
test_running_gpu_job (tools.test_dashboard_live.NowLines) ... ok
test_unavailable_inventory_never_reports_idle (tools.test_dashboard_live.NowLines) ... ok
test_changed_source_triggers_reload (tools.test_dashboard_live.Reload) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_live.py:57: ResourceWarning: unclosed file <_io.TextIOWrapper name='/private/tmp/dashboard_gpu_detector_build/tmpk0q71hix/dashboard_x.py' mode='w' encoding='UTF-8'>
  open(p, "w").write("x")
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_decided_rows_and_prose_are_ignored (tools.test_dashboard_live.Rulings) ... ok
test_rows_whose_status_awaits_the_operator (tools.test_dashboard_live.Rulings) ... ok
test_events_newer_than_the_report_text (tools.test_dashboard_live.Staleness) ... ok
test_unparseable_updated_counts_everything_as_newer (tools.test_dashboard_live.Staleness) ... ok
test_rebuild_only_after_the_set_is_stable (tools.test_dashboard_live.TeamTiles) ... ok
test_sessions_from_tile_start_commands (tools.test_dashboard_live.TeamTiles) ... ok
test_team_sessions_skip_dashboard_and_viewers (tools.test_dashboard_live.TeamTiles) ... ok
test_archived_logs_are_not_the_live_run (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_facts_from_the_last_recipe_with_answers (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_lines_mark_right_and_wrong_and_show_the_words (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_no_answers_recorded (tools.test_dashboard_live.WordsAndAnswers) ... ok

----------------------------------------------------------------------
Ran 27 tests in 0.126s

OK
```

## baseline_render.txt

Command: `['/usr/bin/python3', '-B', 'tools/dashboard_experiment.py', '--once', '110', '40']`; exit 1.

```text
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_experiment.py", line 351, in <module>
    main()
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_experiment.py", line 334, in main
    print("\n".join(render(int(sys.argv[i + 1]), int(sys.argv[i + 2]))))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_experiment.py", line 249, in render
    top, pids, job = running()
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_experiment.py", line 103, in running
    for line in sh("/bin/ps", "-axo", "pid=,etime=,command=").splitlines():
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/dashboard_experiment.py", line 45, in sh
    return subprocess.run(a, capture_output=True, text=True).stdout
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/subprocess.py", line 505, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/subprocess.py", line 951, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/subprocess.py", line 1821, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
PermissionError: [Errno 1] Operation not permitted: '/bin/ps'
```

## claude_auth.txt

Command: `['claude', 'auth', 'status']`; exit 1.

```text
{
  "loggedIn": false,
  "authMethod": "none",
  "apiProvider": "firstParty",
  "analyticsDisabled": false,
  "projectsDirectory": "/Users/robertrhu/.claude/projects",
  "configDirectory": "/Users/robertrhu/.claude"
}
```

## detector_red.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_gpu_detector']`; exit 1.

```text
test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... 
======================================================================
FAIL: test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 101, in test_caps_are_read_from_current_launcher_source_without_importing_jobs
    self.assertEqual(len(jobs), 1)
AssertionError: 0 != 1

======================================================================
FAIL: test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) (code=0, inventory='not a process inventory\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 119, in test_denied_empty_and_malformed_inventory_are_unavailable_never_idle
    self.assertTrue(state.get('unavailable'), 'failed visibility must never be GPU idle')
AssertionError: None is not true : failed visibility must never be GPU idle

======================================================================
FAIL: test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 122, in test_denied_empty_and_malformed_inventory_are_unavailable_never_idle
    state = L.gpu_state()
PermissionError: process inventory denied

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 124, in test_denied_empty_and_malformed_inventory_are_unavailable_never_idle
    self.fail('shared detector must return unavailable rather than crash: ' + str(error))
AssertionError: shared detector must return unavailable rather than crash: process inventory denied

======================================================================
FAIL: test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='bash tools/run_mathlab_harvest.sh results/mathlab/admission.json')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 134, in test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs
    self.assertIn(name, text)
AssertionError: 'Math-lab harvest' not found in 'No experiment logs found under results/.'

======================================================================
FAIL: test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B tools/mathlab_harvest.py --admission a.json --run-dir results/mathlab_staging/runs/harvest_20261009T230000Z_101')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 134, in test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs
    self.assertIn(name, text)
AssertionError: 'Math-lab harvest' not found in 'No experiment logs found under results/.'

======================================================================
FAIL: test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B tools/run_c10z_v7_diag.py --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 134, in test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs
    self.assertIn(name, text)
AssertionError: 'C10Z V7 probe' not found in 'No experiment logs found under results/.'

======================================================================
FAIL: test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B experiments/track_c/c10z_v7_diag.py --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 134, in test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs
    self.assertIn(name, text)
AssertionError: 'C10Z V7 probe' not found in 'No experiment logs found under results/.'

======================================================================
FAIL: test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='bash tools/run_c10y_precast_diag.sh --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 134, in test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs
    self.assertIn(name, text)
AssertionError: 'C10Y pre-cast' not found in 'No experiment logs found under results/.'

======================================================================
FAIL: test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B experiments/track_c/c10y_precast_diag.py --utc 20261009T230000Z --worker')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 134, in test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs
    self.assertIn(name, text)
AssertionError: 'C10Y pre-cast' not found in 'No experiment logs found under results/.'

======================================================================
FAIL: test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 147, in test_experiment_denied_inventory_is_visible_at_110_by_40
    text = plain('\n'.join(X.render(110, 40)))
PermissionError: process inventory denied

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 149, in test_experiment_denied_inventory_is_visible_at_110_by_40
    self.fail('headless experiment must show unavailable: ' + str(error))
AssertionError: headless experiment must show unavailable: process inventory denied

======================================================================
FAIL: test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 111, in test_harvest_events_directory_never_becomes_an_inferred_artifact_directory
    self.assertEqual(len(jobs), 1)
AssertionError: 0 != 1

======================================================================
FAIL: test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 158, in test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label
    self.assertEqual(state['running'], ('c10w', 'p2-eval', '01:02'))
AssertionError: None != ('c10w', 'p2-eval', '01:02')

======================================================================
FAIL: test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 77, in test_parent_worker_and_admission_share_one_job_with_original_elapsed
    self.assertEqual(len(jobs), 3, 'one job per live run; wrappers must not hide or double-count workers')
AssertionError: 0 != 3 : one job per live run; wrappers must not hide or double-count workers

======================================================================
FAIL: test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 190, in test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget
    self.assertIn(name, visible)
AssertionError: 'Math-lab harvest' not found in 'GPU: idle   │   working 1 · asking 1 · active 1 · idle 1'

======================================================================
FAIL: test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='bash tools/run_mathlab_harvest.sh results/mathlab/admission.json')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 58, in test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace
    self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
AssertionError: 0 != 1 : running GPU job vanished from the shared detector

======================================================================
FAIL: test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B tools/mathlab_harvest.py --admission a.json --run-dir results/mathlab_staging/runs/harvest_20261009T230000Z_101')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 58, in test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace
    self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
AssertionError: 0 != 1 : running GPU job vanished from the shared detector

======================================================================
FAIL: test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B tools/run_c10z_v7_diag.py --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 58, in test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace
    self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
AssertionError: 0 != 1 : running GPU job vanished from the shared detector

======================================================================
FAIL: test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B experiments/track_c/c10z_v7_diag.py --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 58, in test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace
    self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
AssertionError: 0 != 1 : running GPU job vanished from the shared detector

======================================================================
FAIL: test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='bash tools/run_c10y_precast_diag.sh --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 58, in test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace
    self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
AssertionError: 0 != 1 : running GPU job vanished from the shared detector

======================================================================
FAIL: test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -B experiments/track_c/c10y_precast_diag.py --utc 20261009T230000Z --worker')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 58, in test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace
    self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
AssertionError: 0 != 1 : running GPU job vanished from the shared detector

----------------------------------------------------------------------
Ran 10 tests in 0.417s

FAILED (failures=20)
```

## detector_green1.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_gpu_detector']`; exit 0.

```text
test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.877s

OK
```

## dashboard_green.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_live', 'tools.test_dashboard_mathlab', 'tools.test_dashboard_gpu_detector']`; exit 0.

```text
test_clean_finish_is_not_an_alert (tools.test_dashboard_live.Alerts) ... ok
test_new_step_resets_the_clock (tools.test_dashboard_live.Alerts) ... ok
test_no_progress_while_working (tools.test_dashboard_live.Alerts) ... ok
test_stopped_on_an_error (tools.test_dashboard_live.Alerts) ... ok
test_waiting_for_an_answer (tools.test_dashboard_live.Alerts) ... ok
test_visible_width_only (tools.test_dashboard_live.Clip) ... ok
test_last_exit_line (tools.test_dashboard_live.Coordinator) ... ok
test_no_exit_yet (tools.test_dashboard_live.Coordinator) ... ok
test_real_subprocess_nonzero_and_empty_responses_are_unavailable (tools.test_dashboard_live.GPUInventory) ... ok
test_shared_detector_recognizes_harvest_but_not_a_prompt_or_temp_copy (tools.test_dashboard_live.GPUInventory) ... ok
test_successful_nonempty_inventory_can_report_no_gpu_job (tools.test_dashboard_live.GPUInventory) ... ok
test_clean_exit_reads_finished (tools.test_dashboard_live.NowLines) ... ok
test_order_and_wording (tools.test_dashboard_live.NowLines) ... ok
test_running_gpu_job (tools.test_dashboard_live.NowLines) ... ok
test_unavailable_inventory_never_reports_idle (tools.test_dashboard_live.NowLines) ... ok
test_changed_source_triggers_reload (tools.test_dashboard_live.Reload) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_live.py:57: ResourceWarning: unclosed file <_io.TextIOWrapper name='/private/tmp/dashboard_gpu_detector_build/tmp5gejvlca/dashboard_x.py' mode='w' encoding='UTF-8'>
  open(p, "w").write("x")
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_decided_rows_and_prose_are_ignored (tools.test_dashboard_live.Rulings) ... ok
test_rows_whose_status_awaits_the_operator (tools.test_dashboard_live.Rulings) ... ok
test_events_newer_than_the_report_text (tools.test_dashboard_live.Staleness) ... ok
test_unparseable_updated_counts_everything_as_newer (tools.test_dashboard_live.Staleness) ... ok
test_rebuild_only_after_the_set_is_stable (tools.test_dashboard_live.TeamTiles) ... ok
test_sessions_from_tile_start_commands (tools.test_dashboard_live.TeamTiles) ... ok
test_team_sessions_skip_dashboard_and_viewers (tools.test_dashboard_live.TeamTiles) ... ok
test_archived_logs_are_not_the_live_run (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_facts_from_the_last_recipe_with_answers (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_lines_mark_right_and_wrong_and_show_the_words (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_no_answers_recorded (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_admission_receipt_labels_the_scope_and_keeps_plan_unstarted (tools.test_dashboard_mathlab.Dashboard) ... ok
test_builder_sized_checks_preserve_disclaimer_machine_findings_and_questions (tools.test_dashboard_mathlab.Dashboard) ... ok
test_checks_paginate_and_keep_required_bars_ahead_of_large_observations (tools.test_dashboard_mathlab.Dashboard) ... ok
test_finding_and_candidate_keep_tier_source_and_offline_status (tools.test_dashboard_mathlab.Dashboard) ... ok
test_gpu_probe_error_is_visible_and_does_not_break_the_frame (tools.test_dashboard_mathlab.Dashboard) ... ok
test_halted_shows_reason_and_diagnostic (tools.test_dashboard_mathlab.Dashboard) ... ok
test_harvest_screen_shows_progress_deadline_cap_and_resources (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_free_gpu_and_present_files_do_not_claim_a_build_or_launch_approval (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_freeze_wait_comes_from_the_current_status_line (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_gpu_wait_names_the_current_shared_job (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_ignores_stale_next_prose (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_reads_status_with_trailing_review_prose (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_rechecks_file_presence_on_every_frame (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_shows_plan_current_prereg_status_sha_and_wait (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_unreadable_prereg_keeps_gpu_and_file_facts_visible (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_waits_for_each_missing_launcher_driver_and_notebook (tools.test_dashboard_mathlab.Dashboard) ... ok
test_invalid_calibration_does_not_render_a_cheap_stop (tools.test_dashboard_mathlab.Dashboard) ... ok
test_invalid_is_labelled_no_verdict (tools.test_dashboard_mathlab.Dashboard) ... ok
test_latest_run_is_selected_and_previous_run_is_not_rewritten (tools.test_dashboard_mathlab.Dashboard) ... ok
test_malformed_line_remains_visible_in_a_short_frame (tools.test_dashboard_mathlab.Dashboard) ... ok
test_once_cli_at_80_and_200_columns (tools.test_dashboard_mathlab.Dashboard) ... ok
test_run_selection_policy_and_other_active_run_count_are_visible (tools.test_dashboard_mathlab.Dashboard) ... ok
test_step_three_failed_check_is_explained_as_designed_cheap_stop (tools.test_dashboard_mathlab.Dashboard) ... ok
test_step_two_pass_and_missing_resource_labels (tools.test_dashboard_mathlab.Dashboard) ... ok
test_text_is_cleaned_and_width_is_bounded_at_80_200_and_300 (tools.test_dashboard_mathlab.Dashboard) ... ok
test_waiting_for_gpu_uses_shared_gpu_state_and_admission_reason (tools.test_dashboard_mathlab.Dashboard) ... ok
test_all_event_variants_round_trip (tools.test_dashboard_mathlab.EventContract) ... ok
test_append_preserves_previous_bytes_and_is_one_write_per_event (tools.test_dashboard_mathlab.EventContract) ... ok
test_duplicate_json_keys_and_wrong_run_id_are_reported (tools.test_dashboard_mathlab.EventContract) ... ok
test_malformed_schema_utf8_and_partial_lines_are_reported (tools.test_dashboard_mathlab.EventContract) ... ok
test_missing_file_is_an_explicit_read_error (tools.test_dashboard_mathlab.EventContract) ... ok
test_run_purpose_is_an_optional_validated_schema_one_discriminator (tools.test_dashboard_mathlab.EventContract) ... ok
test_short_append_raises (tools.test_dashboard_mathlab.EventContract) ... ok
test_unknown_missing_extra_and_reserved_fields_are_rejected_without_writing (tools.test_dashboard_mathlab.EventContract) ... ok
test_wrong_types_outcomes_and_tiers_are_rejected (tools.test_dashboard_mathlab.EventContract) ... ok
test_admission_only_pass_never_completes_an_experiment_step (tools.test_dashboard_mathlab.EventFold) ... ok
test_aggregate_calibration_failure_is_the_cheap_stop (tools.test_dashboard_mathlab.EventFold) ... ok
test_aggregate_calibration_preserves_producer_outcome_before_run_finished (tools.test_dashboard_mathlab.EventFold) ... ok
test_denied_gpu_admission_then_allowed (tools.test_dashboard_mathlab.EventFold) ... ok
test_finishing_a_stage_preserves_the_original_recent_events (tools.test_dashboard_mathlab.EventFold) ... ok
test_fold_is_pure_and_recent_events_are_bounded (tools.test_dashboard_mathlab.EventFold) ... ok
test_gate_two_b_failure_does_not_stop_the_lab (tools.test_dashboard_mathlab.EventFold) ... ok
test_halt_and_finished_states_survive_late_samples (tools.test_dashboard_mathlab.EventFold) ... ok
test_invalid_is_no_verdict_and_resource_halt_is_not_a_cheap_stop (tools.test_dashboard_mathlab.EventFold) ... ok
test_legacy_admission_then_real_stage_is_an_experiment_run (tools.test_dashboard_mathlab.EventFold) ... ok
test_mixed_run_stream_is_rejected (tools.test_dashboard_mathlab.EventFold) ... ok
test_new_stage_clears_previous_progress (tools.test_dashboard_mathlab.EventFold) ... ok
test_no_events_is_not_started (tools.test_dashboard_mathlab.EventFold) ... ok
test_one_proxy_can_fail_then_another_pass_without_stopping (tools.test_dashboard_mathlab.EventFold) ... ok
test_producer_gate_identifiers_join_the_shared_planned_groups (tools.test_dashboard_mathlab.EventFold) ... ok
test_running_harvest_and_progress (tools.test_dashboard_mathlab.EventFold) ... ok
test_step_two_pass_does_not_invent_step_one_pass (tools.test_dashboard_mathlab.EventFold) ... ok
test_successful_substage_does_not_finish_the_step (tools.test_dashboard_mathlab.EventFold) ... ok
test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok

----------------------------------------------------------------------
Ran 90 tests in 1.047s

OK
```

## prompt_red.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_gpu_detector']`; exit 1.

```text
test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok

======================================================================
FAIL: test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 tools/reviewer.py --prompt "experiments/track_c/c10z_v7_diag.py --utc 20261009T230000Z"')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 97, in test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu
    self.assertIsNone(state['running'])
AssertionError: ('c10z', '--utc', '00:12') is not None

======================================================================
FAIL: test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 tools/reviewer.py --prompt "experiments/track_c/c10w_oracle_arms.py p2-eval"')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 97, in test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu
    self.assertIsNone(state['running'])
AssertionError: ('c10w', 'p2-eval', '00:12') is not None

----------------------------------------------------------------------
Ran 10 tests in 0.601s

FAILED (failures=2)
```

## review_cases_red.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_gpu_detector']`; exit 1.

```text
test_bash_long_option_does_not_turn_script_into_inline_code (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... test_quoted_run_directory_is_preserved_as_exact_token (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL
test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_unrelated_same_namespace_process_families_are_two_competing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... FAIL

======================================================================
FAIL: test_bash_long_option_does_not_turn_script_into_inline_code (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 121, in test_bash_long_option_does_not_turn_script_into_inline_code
    self.assertEqual(len(jobs), 1)
AssertionError: 0 != 1

======================================================================
FAIL: test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 tools/reviewer.py --prompt "experiments/track_c/c10z_v7_diag.py --utc 20261009T230000Z"')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 100, in test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu
    self.assertIsNone(state['running'])
AssertionError: ('c10z', '--utc', '00:12') is not None

======================================================================
FAIL: test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 tools/reviewer.py --prompt "experiments/track_c/c10w_oracle_arms.py p2-eval"')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 100, in test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu
    self.assertIsNone(state['running'])
AssertionError: ('c10w', 'p2-eval', '00:12') is not None

======================================================================
FAIL: test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -cpass tools/run_c10z_v7_diag.py --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 100, in test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu
    self.assertIsNone(state['running'])
AssertionError: ('c10z', 'v7-diag', '00:12') is not None

======================================================================
FAIL: test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) (command='python3 -munittest tools/run_c10z_v7_diag.py --utc 20261009T230000Z')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 100, in test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu
    self.assertIsNone(state['running'])
AssertionError: ('c10z', 'v7-diag', '00:12') is not None

======================================================================
FAIL: test_quoted_run_directory_is_preserved_as_exact_token (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 117, in test_quoted_run_directory_is_preserved_as_exact_token
    self.assertEqual(jobs[0]['run_dir'], path)
AssertionError: "/private/tmp/dashboard_gpu_detector_buil[38 chars]ions" != '/Volumes/memit/observations with space/harvest'
- /private/tmp/dashboard_gpu_detector_build/tmpcm0sa16k/'/Volumes/memit/observations
+ /Volumes/memit/observations with space/harvest


======================================================================
FAIL: test_unrelated_same_namespace_process_families_are_two_competing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_gpu_detector.py", line 109, in test_unrelated_same_namespace_process_families_are_two_competing_jobs
    self.assertEqual(len(jobs), 2, 'matching output paths do not establish common process ownership')
AssertionError: 1 != 2 : matching output paths do not establish common process ownership

----------------------------------------------------------------------
Ran 13 tests in 0.681s

FAILED (failures=7)
```

## dashboard_final_green.txt

Command: `['/usr/bin/python3', '-B', '-m', 'unittest', '-v', 'tools.test_dashboard_live', 'tools.test_dashboard_mathlab', 'tools.test_dashboard_gpu_detector']`; exit 0.

```text
test_clean_finish_is_not_an_alert (tools.test_dashboard_live.Alerts) ... ok
test_new_step_resets_the_clock (tools.test_dashboard_live.Alerts) ... ok
test_no_progress_while_working (tools.test_dashboard_live.Alerts) ... ok
test_stopped_on_an_error (tools.test_dashboard_live.Alerts) ... ok
test_waiting_for_an_answer (tools.test_dashboard_live.Alerts) ... ok
test_visible_width_only (tools.test_dashboard_live.Clip) ... ok
test_last_exit_line (tools.test_dashboard_live.Coordinator) ... ok
test_no_exit_yet (tools.test_dashboard_live.Coordinator) ... ok
test_real_subprocess_nonzero_and_empty_responses_are_unavailable (tools.test_dashboard_live.GPUInventory) ... ok
test_shared_detector_recognizes_harvest_but_not_a_prompt_or_temp_copy (tools.test_dashboard_live.GPUInventory) ... ok
test_successful_nonempty_inventory_can_report_no_gpu_job (tools.test_dashboard_live.GPUInventory) ... ok
test_clean_exit_reads_finished (tools.test_dashboard_live.NowLines) ... ok
test_order_and_wording (tools.test_dashboard_live.NowLines) ... ok
test_running_gpu_job (tools.test_dashboard_live.NowLines) ... ok
test_unavailable_inventory_never_reports_idle (tools.test_dashboard_live.NowLines) ... ok
test_changed_source_triggers_reload (tools.test_dashboard_live.Reload) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_live.py:57: ResourceWarning: unclosed file <_io.TextIOWrapper name='/private/tmp/dashboard_gpu_detector_build/tmpiajyshzs/dashboard_x.py' mode='w' encoding='UTF-8'>
  open(p, "w").write("x")
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_decided_rows_and_prose_are_ignored (tools.test_dashboard_live.Rulings) ... ok
test_rows_whose_status_awaits_the_operator (tools.test_dashboard_live.Rulings) ... ok
test_events_newer_than_the_report_text (tools.test_dashboard_live.Staleness) ... ok
test_unparseable_updated_counts_everything_as_newer (tools.test_dashboard_live.Staleness) ... ok
test_rebuild_only_after_the_set_is_stable (tools.test_dashboard_live.TeamTiles) ... ok
test_sessions_from_tile_start_commands (tools.test_dashboard_live.TeamTiles) ... ok
test_team_sessions_skip_dashboard_and_viewers (tools.test_dashboard_live.TeamTiles) ... ok
test_archived_logs_are_not_the_live_run (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_facts_from_the_last_recipe_with_answers (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_lines_mark_right_and_wrong_and_show_the_words (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_no_answers_recorded (tools.test_dashboard_live.WordsAndAnswers) ... ok
test_admission_receipt_labels_the_scope_and_keeps_plan_unstarted (tools.test_dashboard_mathlab.Dashboard) ... ok
test_builder_sized_checks_preserve_disclaimer_machine_findings_and_questions (tools.test_dashboard_mathlab.Dashboard) ... ok
test_checks_paginate_and_keep_required_bars_ahead_of_large_observations (tools.test_dashboard_mathlab.Dashboard) ... ok
test_finding_and_candidate_keep_tier_source_and_offline_status (tools.test_dashboard_mathlab.Dashboard) ... ok
test_gpu_probe_error_is_visible_and_does_not_break_the_frame (tools.test_dashboard_mathlab.Dashboard) ... ok
test_halted_shows_reason_and_diagnostic (tools.test_dashboard_mathlab.Dashboard) ... ok
test_harvest_screen_shows_progress_deadline_cap_and_resources (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_free_gpu_and_present_files_do_not_claim_a_build_or_launch_approval (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_freeze_wait_comes_from_the_current_status_line (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_gpu_wait_names_the_current_shared_job (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_ignores_stale_next_prose (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_reads_status_with_trailing_review_prose (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_rechecks_file_presence_on_every_frame (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_shows_plan_current_prereg_status_sha_and_wait (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_unreadable_prereg_keeps_gpu_and_file_facts_visible (tools.test_dashboard_mathlab.Dashboard) ... ok
test_idle_waits_for_each_missing_launcher_driver_and_notebook (tools.test_dashboard_mathlab.Dashboard) ... ok
test_invalid_calibration_does_not_render_a_cheap_stop (tools.test_dashboard_mathlab.Dashboard) ... ok
test_invalid_is_labelled_no_verdict (tools.test_dashboard_mathlab.Dashboard) ... ok
test_latest_run_is_selected_and_previous_run_is_not_rewritten (tools.test_dashboard_mathlab.Dashboard) ... ok
test_malformed_line_remains_visible_in_a_short_frame (tools.test_dashboard_mathlab.Dashboard) ... ok
test_once_cli_at_80_and_200_columns (tools.test_dashboard_mathlab.Dashboard) ... ok
test_run_selection_policy_and_other_active_run_count_are_visible (tools.test_dashboard_mathlab.Dashboard) ... ok
test_step_three_failed_check_is_explained_as_designed_cheap_stop (tools.test_dashboard_mathlab.Dashboard) ... ok
test_step_two_pass_and_missing_resource_labels (tools.test_dashboard_mathlab.Dashboard) ... ok
test_text_is_cleaned_and_width_is_bounded_at_80_200_and_300 (tools.test_dashboard_mathlab.Dashboard) ... ok
test_waiting_for_gpu_uses_shared_gpu_state_and_admission_reason (tools.test_dashboard_mathlab.Dashboard) ... ok
test_all_event_variants_round_trip (tools.test_dashboard_mathlab.EventContract) ... ok
test_append_preserves_previous_bytes_and_is_one_write_per_event (tools.test_dashboard_mathlab.EventContract) ... ok
test_duplicate_json_keys_and_wrong_run_id_are_reported (tools.test_dashboard_mathlab.EventContract) ... ok
test_malformed_schema_utf8_and_partial_lines_are_reported (tools.test_dashboard_mathlab.EventContract) ... ok
test_missing_file_is_an_explicit_read_error (tools.test_dashboard_mathlab.EventContract) ... ok
test_run_purpose_is_an_optional_validated_schema_one_discriminator (tools.test_dashboard_mathlab.EventContract) ... ok
test_short_append_raises (tools.test_dashboard_mathlab.EventContract) ... ok
test_unknown_missing_extra_and_reserved_fields_are_rejected_without_writing (tools.test_dashboard_mathlab.EventContract) ... ok
test_wrong_types_outcomes_and_tiers_are_rejected (tools.test_dashboard_mathlab.EventContract) ... ok
test_admission_only_pass_never_completes_an_experiment_step (tools.test_dashboard_mathlab.EventFold) ... ok
test_aggregate_calibration_failure_is_the_cheap_stop (tools.test_dashboard_mathlab.EventFold) ... ok
test_aggregate_calibration_preserves_producer_outcome_before_run_finished (tools.test_dashboard_mathlab.EventFold) ... ok
test_denied_gpu_admission_then_allowed (tools.test_dashboard_mathlab.EventFold) ... ok
test_finishing_a_stage_preserves_the_original_recent_events (tools.test_dashboard_mathlab.EventFold) ... ok
test_fold_is_pure_and_recent_events_are_bounded (tools.test_dashboard_mathlab.EventFold) ... ok
test_gate_two_b_failure_does_not_stop_the_lab (tools.test_dashboard_mathlab.EventFold) ... ok
test_halt_and_finished_states_survive_late_samples (tools.test_dashboard_mathlab.EventFold) ... ok
test_invalid_is_no_verdict_and_resource_halt_is_not_a_cheap_stop (tools.test_dashboard_mathlab.EventFold) ... ok
test_legacy_admission_then_real_stage_is_an_experiment_run (tools.test_dashboard_mathlab.EventFold) ... ok
test_mixed_run_stream_is_rejected (tools.test_dashboard_mathlab.EventFold) ... ok
test_new_stage_clears_previous_progress (tools.test_dashboard_mathlab.EventFold) ... ok
test_no_events_is_not_started (tools.test_dashboard_mathlab.EventFold) ... ok
test_one_proxy_can_fail_then_another_pass_without_stopping (tools.test_dashboard_mathlab.EventFold) ... ok
test_producer_gate_identifiers_join_the_shared_planned_groups (tools.test_dashboard_mathlab.EventFold) ... ok
test_running_harvest_and_progress (tools.test_dashboard_mathlab.EventFold) ... ok
test_step_two_pass_does_not_invent_step_one_pass (tools.test_dashboard_mathlab.EventFold) ... ok
test_successful_substage_does_not_finish_the_step (tools.test_dashboard_mathlab.EventFold) ... ok
test_bash_long_option_does_not_turn_script_into_inline_code (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_caps_are_read_from_current_launcher_source_without_importing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_experiment_denied_inventory_is_visible_at_110_by_40 (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_parent_worker_and_admission_share_one_job_with_original_elapsed (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_quoted_run_directory_is_preserved_as_exact_token (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok
test_unrelated_same_namespace_process_families_are_two_competing_jobs (tools.test_dashboard_gpu_detector.SharedGPUDetector) ... ok

----------------------------------------------------------------------
Ran 93 tests in 1.115s

OK
```

## experiment_headless_110x40.txt

Command: `['/usr/bin/python3', '-B', 'tools/dashboard_experiment.py', '--once', '110', '40']`; exit 0.

```text
[1m[38;5;231m[48;5;124m GPU UNAVAILABLE [0m[38;5;124m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m
 [Errno 1] Operation not permitted: '/bin/ps'
```

## mathlab_headless_110x40.txt

Command: `['/usr/bin/python3', '-B', 'tools/dashboard_mathlab.py', '--once', '110', '40']`; exit 0.

```text
[1m[38;5;231m[48;5;25m■ MATH LAB · test math estimates using saved model inputs                                                     [0m[0m
 [1mMATH-PROXY · math estimate, not evidence[0m[0m
 Run dml2_build_acceptance_20261009T175517.460160Z · finished · step 2[0m
 View: newest events file by mtime · other active runs (events): 0[0m
 Elapsed 0m00s / hard deadline 1h48m · ends 2026-10-09T19:44:17.460357+00:00[0m
 D-ML-2 implementation accepted; CPU fixture/tooling only; production feasibility UNVERIFIED[0m
[1m[38;5;231m[48;5;24m PLAN · ✓ passed ✗ failed ▶ current · not recorded [0m[38;5;24m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 · 1 · Harvest: record internal model inputs for every prompt (one GPU pass).[0m
 ✓ 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.[0m
 · 3 · Calibrate: check estimates against past results; failure stops cheaply.[0m
 · 4 · Candidate questions: explore ideas later, after a new written plan.[0m
[1m[38;5;231m[48;5;28m NOW [0m[38;5;28m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 Verify amended CPU implementation and recorded fixture evidence[0m
 Progress not recorded · stage time 0m00s / cap 1m00s[0m
[1m[38;5;231m[48;5;25m CHECKS · 6 recorded · 0 failed / 0 invalid · page 1/2 [0m[38;5;25m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 [38;5;40mPASS stage-memory-build-acceptance[0m · bar >= 8 · measured 26.197402954101562[0m
  At least eight GiB of memory before this stage[0m
 [38;5;40mPASS budget-build-acceptance[0m · bar meets 6540 · measured object:5[0m
  This stage fits the remaining deadline[0m
 [38;5;40mPASS dml2-validation[0m · bar meets "All GREEN exit codes equal zero" · measured object:3[0m
  All CPU tests, DuckDB, marimo and shell checks pass[0m
 [38;5;40mPASS dml2-peak-rss[0m · bar meets {"svd_reserve_gib":5,"solve_reserve_gib":9} · measured object:2[0m
  Complete full-shape CPU peaks fit the frozen reserves[0m
 [38;5;40mPASS dml2-frozen-runtime[0m · bar meets "Runner exit 0 and matching PASS event for each notebook" · measured ob…[0m
  Both notebooks finished through real runner and uv on fixture harvest[0m
 [38;5;40mPASS dml2-prereg[0m · bar meets "4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507" · measured "…[0m
  Exact frozen amended prereg bytes still match the pinned SHA[0m
 [2m· Safe launch · need engine unchanged; GPU queue cleared[0m[0m
 [2m· Same prompt inputs · need frozen context and tokenisation match[0m[0m
 [2m· Observation changes nothing · need LAW#5 and observer-parity pass[0m[0m
 [2m· Known model answers reproduce · need all three fresh baselines pass their frozen ranges[0m[0m
[1m[38;5;231m[48;5;30m MACHINE · samples from this run; GPU display is shared [0m[38;5;30m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 Free memory [38;5;39m████████┃███████[0m 26.1974 GiB · floor 8 GiB (┃) · +18.1974 GiB above floor[0m
 Lab memory 0.0237427 GiB · CPU 1249.52% · GPU state unavailable: [Errno 1] Operation not permitted: '/bin/ps'[0m
[1m[38;5;231m[48;5;96m FINDINGS · MATH-PROXY: math estimate, not evidence (0) [0m[38;5;96m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 None staged yet.[0m
[1m[38;5;231m[48;5;96m CANDIDATE QUESTIONS (0; newest 3) · ideas to test [0m[38;5;96m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 None yet; step 4 needs its own pre-registration.[0m
[1m[38;5;231m[48;5;238m LAST EVENTS · newest 1 of 8 recent [0m[38;5;238m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m[0m
 17:55:17 Run finished PASS: D-ML-2 implementation accepted; CPU fixture/tooling only; production feasibility [0m
```


## Resumed then parked for priority A1 fix — 2026-10-09T19:50:58.144353+00:00

Status: **PARKED AGAIN at MAESTRO priority interrupt.** No new detector, bar, experiment or test edits during this resume. The resumed CPU baseline passed all93 tests in1.430s (`/private/tmp/dashboard_gpu_detector_build/resume_baseline.txt`). No new renders or job launches; no commits.

Read current CPU launcher/runner/notebook interfaces and C10Z benchmark/attempt launch interfaces. CPU6540/1800s caps and benchmark600s cap were located. Proposed controls for CPU notebooks, benchmark and attempt4 remain unwritten; no production extension implemented. `/bin/ps` remains denied (fresh probe exit1), so live process visibility remains UNVERIFIED. The step2 events stream `results/mathlab_staging/runs/m2_20261009T192821Z_82233/events.jsonl` records PID82270, an admitted step2 with6540s deadline and fresh5s resource samples; current detector does not yet display it. Planned explicit recorded-CPU fallback must preserve that evidence boundary and keep CPU activity separate from GPU occupancy. Exact CPU artifact directory is not linked in the run record; do not guess newest output.

Next detector work after priority fix: test-first aliases for `run_mathlab_cpu.sh`, CPU runner, `uv run --script mathlab/m*.py`, C10Z benchmark and attempt/stage/resident; preserve executable filtering and ancestry deduplication, add source/record-derived caps and exact known paths, show recorded CPU activity when inventory unavailable, rerun full dashboard suite and110×40 renders, obtain final read-only review. Review request was parked before any review execution. Do not touch `dashboard_mathlab.py`, `mathlab_events.py`, `labviz/**` or science/job sources.

Source SHAs at the second stopping point:

| File | SHA-256 |
|---|---|
| `tools/dashboard_live.py` | `5d7d9dd84eb4bb4dc9c37334ec2b6321300c82f5e15d152f1e791c091deade4c` |
| `tools/dashboard_bar.sh` | `535e04d3ea0357183e9448e95e88a673294d83aba4772208be545c2f8e3a4b0e` |
| `tools/dashboard_experiment.py` | `ff81df2a43031bb25c2cd721625b61661bc6237d8731d24a0190f8ec56c03647` |
| `tools/test_dashboard_live.py` | `b9fec5d1c0eceea40e5caad6222d56447352cf79cdbeb0ac8f984ec25e9ed81d` |
| `tools/test_dashboard_gpu_detector.py` | `886f4d114180a785cfe42c453dab9a6019d4eb7f0146eb0c432c8d9f225a1aad` |


## Parked for benchmark rerun #3 admission priority — 2026-10-09T20:34:11.356303+00:00

Status: **PARKED, requested extension still RED.** Existing shared-detector runtime restored to its original stopping-point bytes, SHA `5d7d9dd84eb4bb4dc9c37334ec2b6321300c82f5e15d152f1e791c091deade4c`; existing93 controls PASS again. No detector behavior is claimed complete. New CPU/benchmark/attempt controls are retained in `tools/test_dashboard_gpu_detector.py` (28 detector tests: original13 plus15 new); RED before any production edit was25 assertion failures, zero errors (`/private/tmp/dashboard_gpu_detector_resume2/red_binding.txt`). Initial partial production extension was saved, then only our `dashboard_live.py` edit restored to the verified snapshot; experiment renderer and bar were not changed. No job/model/GPU/MPS/commit execution; no protected MathLab/Lab View or science-source edits by this task.

Done: baseline93 PASS; real step2 fresh events observed; test-design fallback review PROCEED; CPU aliases/wrappers, GPU separation, real bar/110×40 denied-inventory activity, benchmark/source caps, explicit/unique PID-and-age-bound attempt dirs, missing stage2 origin, P2 overlapping recorded scopes, stale/future/expired/terminal CPU stream rejection controls written first. Current source remains pre-extension.

In flight: implementation. Exact partial source `/private/tmp/dashboard_gpu_detector_resume2/dashboard_live_partial_green.py` adds transparent command parsing, CPU/benchmark/attempt aliases, cap readers, PID/age-bound recorded budget and validated CPU event helpers; it has NOT been GREEN-tested and the helpers are NOT yet wired into gpu_state/renderers. Do not apply it blindly: compare current sources and preserve concurrent edits. Current tests/source/report snapshots, complete RED logs and existing93 GREEN output are under that directory.

Next: after priority admission, apply/reconcile the saved production delta; wire gpu_state CPU records separately from GPU jobs, add recorded CPU display to summary/experiment/NOW, run the28 detector controls plus existing live/MathLab suites, render real and fixture110×40, obtain final read-only review. Cap snapshots must say recorded scope, never certify current enforced phase; stage2 requested without origin shows budget unavailable. CPU events PID is provenance, not notebook liveness; denied ps remains GPU unavailable. Exact artifact output is unavailable unless explicitly linked, never guess newest folders. Claude auth remains loggedIn=false; fallback review is weaker independence. No DETECTOR DONE.

**Context rule:** watch Context N% left. Before approximately20%, stop starting new work; append a handoff with done/in-flight/exact paths/next step/risks to this report and tell the operator so a fresh successor can start. Every handoff restates this rule.

## Detector completion — 2026-10-09T22:18:12.866792+00:00

**DETECTOR DONE.** All requested GPU launchers/workers and Math-lab CPU notebooks use the one shared detector in tools/dashboard_live.py. Status bar and experiment tab display names, elapsed/cap and exact known output/run directories. CPU activity is separate from GPU occupancy. Final verification: **114 tests PASS** (34 detector/experiment/bar, 27 live, 53 MathLab; 4.502s), **10 final-source headless renders PASS at110×40**, and real status-bar output. The live render shows fresh Math-lab step2 recorded activity with6540s cap and the exact event directory. Process inventory is denied by this sandbox; the dashboard says GPU unavailable and CPU process unverified.

This completion supersedes the historical parked sections above. No GPU/MPS/model load, job/probe/benchmark/attempt launch or commit was performed. No changes to tools/dashboard_mathlab.py, tools/mathlab_events.py, tools/labviz/** or science sources. This resume changed only tools/dashboard_live.py, tools/dashboard_experiment.py and tools/test_dashboard_gpu_detector.py; the prior bar integration and live-test adaptation are unchanged.

### Requirement → test → implementation

| Requirement | Test / evidence | Implementation |
|---|---|---|
| One shared classifier for both consumers | Real bash bar, six original alias controls, named-job110×40 panels; original live/MathLab suites retained | dashboard_live.detect_gpu_jobs:123 and central JOB_TYPES; dashboard_bar.sh:4 shared summary CLI; dashboard_experiment.py:238 uses shared gpu_state |
| Harvest, V7 probe, C10Y pre-cast wrapper/worker | test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace; source-cap and ancestry controls; final harvest/V7/precast fixture renders | The same catalog includes tools/run_mathlab_harvest.sh/mathlab_harvest.py, tools/run_c10z_v7_diag.py/experiments/track_c/c10z_v7_diag.py, tools/run_c10y_precast_diag.sh/experiments/track_c/c10y_precast_diag.py; source caps3600/3060/2820s |
| C10Z benchmark supervisor/worker and transparent wrappers | test_transparent_wrappers_keep_GPU_jobs_and_exact_benchmark_output; test_benchmark_and_CPU_caps_read_sources_without_importing_native_jobs | script_call:20 reads env/caffeinate/nice/timeout and interpreter/uv tokens; benchmark aliases bind explicit --out; job_cap:209 reads current supervise cap600s without import |
| Attempt4 launcher/stage/resident and exact output/recorded budget | Explicit output/go, unique PID-and-age-bound record, missing requested2 origin, overlapping P2 deadlines, independent-family, stale/closed/ambiguous/malformed record controls | run_c10z_attempt.sh/run_c10z_stage.sh/c10z_astra_arms.py share one family; attempt_budget:233 reads explicit paths or unique matching record; nested process2/run.json supported; earliest recorded nominal deadline selected |
| Record binds its own PID age, never oldest family age | test_older_launcher_cannot_rescue_a_reused_resident_PID_record: parent1200s, resident12s, stale origin1000s ago RED; fresh-origin positive GREEN | Dedup keeps raw per-PID ages; record must match that PID's observed age (5s observation tolerance); family-oldest elapsed remains for ordinary job display |
| Nested env -i clears outer pins | test_nested_env_ignore_environment_clears_outer_output_and_go_bindings: both -i and --ignore-environment RED; later-assignment positives GREEN | script_call clears accumulated explicit env at ignore-environment and retains subsequent assignments; observer os.environ is never used for job output/go |
| CPU runner/shell/uv/direct notebook aliases, steps2/3 | test_CPU_launchers_runners_uv_and_notebook_workers_are_separate_from_GPU_jobs; test_CPU_parent_timeout_and_uv_worker_are_one_verified_process_family | Same JOB_TYPES catalog; CPU jobs exposed as cpu_jobs and never set GPU running; frozen CPU runner source supplies6540/1800s caps |
| Recorded CPU remains visible when ps denied | Real bar/shared-state/110×40 negative-inventory control; actual step2 event sample shown below | recorded_cpu_jobs:283 reuses mathlab_events.read_events/fold, admitted CPU experiment2/3 only; fresh sample≤30s, unexpired deadline, running status; event PID is provenance, not notebook liveness |
| Stale/future/expired/halted/finished/admission/wrong-kind/refused/broken CPU records fail closed | test_stale_future_expired_halted_finished_admission_and_wrong_kind_do_not_claim_CPU_activity; test_malformed_CPU_stream_is_refused_and_explained | Shared event validator/fold; errors displayed, no stale waiting/status file; resource freshness bounds checked every draw |
| Actual event timestamp precision | test_recorded_CPU_accepts_actual_publisher_microsecond_timestamps reproduced strptime ValueError RED | CPU event timestamps parse ISO microseconds/Z as emitted by the producer |
| Prompt/inline/module/temp copies/native selftest/help are not GPU jobs | Original exclusion controls plus test_native_selftests_and_help_do_not_claim_GPU_jobs (four RED subcases) | Exact executable script token only; no prompt scanning; --selftest/--help/-h excluded |
| Metadata and unavailable observations visible in bar/experiment/NOW; no guessed directories | Real144-cell bar metadata controls, GPU+CPU panels, output path with spaces, full10-render bounds | gpu_summary:328, now_lines:443, gpu_state:477; generic named-job panel wraps/clips at110 columns |

### Persistence and evidence limits

Only explicitly bound namespaces are shown. V7/precast paths derive from the actual UTC token; benchmark from explicit --out; attempt from explicit command env or one open record matching the exact process PID and age. No newest-folder or observer-env inference. Harvest --run-dir and CPU --run-dir are event directories, not a tensor-artifact namespace. Where no run-specific artifact link is published, Output is unavailable; the exact known events path is shown separately. Existing harvest artifact limitation remains as documented above.

Attempt caps are **recorded scopes**, not proof of the phase currently enforcing the deadline: publications can lag. Requested stage2 without its published origin reports budget unavailable while showing selected launch caps. Process2's stage01 and stage3 overlap is respected. This display neither validates a scientific go nor enforces/certifies deadlines. CPU event activity is recorded and process unverified when ps is denied; GPU occupancy remains unavailable, never idle on denial. No native GPU/job liveness or scientific success is claimed.

### RED → GREEN

| Evidence file under /private/tmp/dashboard_gpu_detector_final | Result |
|---|---|
| red.txt, before any resumed production edit | 28 tests,25 assertion failures,0 errors; retained extension remains RED |
| red_additional.txt, nested P2 and malformed-record controls added first | 30 tests,31 assertion failures,0 errors |
| microseconds_red.txt | Actual producer microsecond timestamp raises ValueError (1 test,1 error) |
| green1.txt | 31 detector controls PASS after wiring/type/timestamp fixes |
| full_green.txt | Initial111 dashboard controls PASS |
| native_selftest_red.txt | Native selftest/help wrongly appears as a GPU job, four assertion failures |
| full_final_green.txt | Interim112 dashboard controls PASS after exclusion |
| pid_parent_red.txt | Review's stale resident PID accepted through older parent age, one assertion failure |
| env_clear_red.txt | Review's nested -i/--ignore-environment retained outer output/go, two assertion failures |
| review_fix_green.txt | Final114 dashboard tests PASS; all negatives plus fresh-PID/later-env positive controls GREEN |

Final review: Claude CLI auth freshly returned loggedIn=false/authMethod=none. Existing read-only Codex fallback reviewed sources, controls, live captures and complete evidence: initial **FIX-FIRST** identified the exact PID-age and nested-env seams above; both reproduced RED before their fixes. Final re-review **PROCEED**, no remaining concrete blocker. This is weaker independence than Astra and supplies no GPU or science approval.

### Exact CPU verification commands

```bash
/opt/homebrew/bin/rtk proxy env PYTHONPYCACHEPREFIX=/private/tmp/dashboard_gpu_detector_final/review-fix-pycache .venv/bin/python -B -m unittest discover -s tools -p 'test_dashboard*.py' -v
/opt/homebrew/bin/rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/dashboard_experiment.py --once 110 40
/opt/homebrew/bin/rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/dashboard_mathlab.py --once 110 40
/opt/homebrew/bin/rtk proxy bash tools/dashboard_bar.sh
/opt/homebrew/bin/rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /private/tmp/dashboard_gpu_detector_final/render_final.py
```

The discovery run executes tools/test_dashboard_live.py, tools/test_dashboard_mathlab.py and all detector/experiment/status-bar tests. There is no other experiment-tab test file. Fresh cache prefixes avoid stale bytecode. Full final output:

```text
test_CPU_launchers_runners_uv_and_notebook_workers_are_separate_from_GPU_jobs (test_dashboard_gpu_detector.SharedGPUDetector.test_CPU_launchers_runners_uv_and_notebook_workers_are_separate_from_GPU_jobs) ... ok
test_CPU_parent_timeout_and_uv_worker_are_one_verified_process_family (test_dashboard_gpu_detector.SharedGPUDetector.test_CPU_parent_timeout_and_uv_worker_are_one_verified_process_family) ... ok
test_GPU_and_CPU_jobs_are_both_visible_without_CPU_changing_GPU_occupancy (test_dashboard_gpu_detector.SharedGPUDetector.test_GPU_and_CPU_jobs_are_both_visible_without_CPU_changing_GPU_occupancy) ... ok
test_attempt_launcher_stage_and_resident_use_explicit_output_and_bound_budget (test_dashboard_gpu_detector.SharedGPUDetector.test_attempt_launcher_stage_and_resident_use_explicit_output_and_bound_budget) ... ok
test_bash_long_option_does_not_turn_script_into_inline_code (test_dashboard_gpu_detector.SharedGPUDetector.test_bash_long_option_does_not_turn_script_into_inline_code) ... ok
test_benchmark_and_CPU_caps_read_sources_without_importing_native_jobs (test_dashboard_gpu_detector.SharedGPUDetector.test_benchmark_and_CPU_caps_read_sources_without_importing_native_jobs) ... ok
test_caps_are_read_from_current_launcher_source_without_importing_jobs (test_dashboard_gpu_detector.SharedGPUDetector.test_caps_are_read_from_current_launcher_source_without_importing_jobs) ... ok
test_conflicting_observer_env_closed_and_ambiguous_records_never_invent_output (test_dashboard_gpu_detector.SharedGPUDetector.test_conflicting_observer_env_closed_and_ambiguous_records_never_invent_output) ... ok
test_denied_empty_and_malformed_inventory_are_unavailable_never_idle (test_dashboard_gpu_detector.SharedGPUDetector.test_denied_empty_and_malformed_inventory_are_unavailable_never_idle) ... ok
test_denied_inventory_keeps_recorded_CPU_visible_in_real_bar_and_110_by_40_experiment (test_dashboard_gpu_detector.SharedGPUDetector.test_denied_inventory_keeps_recorded_CPU_visible_in_real_bar_and_110_by_40_experiment) ... ok
test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs (test_dashboard_gpu_detector.SharedGPUDetector.test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs) ... ok
test_experiment_denied_inventory_is_visible_at_110_by_40 (test_dashboard_gpu_detector.SharedGPUDetector.test_experiment_denied_inventory_is_visible_at_110_by_40) ... ok
test_harvest_events_directory_never_becomes_an_inferred_artifact_directory (test_dashboard_gpu_detector.SharedGPUDetector.test_harvest_events_directory_never_becomes_an_inferred_artifact_directory) ... ok
test_independent_attempt_families_keep_conflicting_explicit_dirs_and_go_caps (test_dashboard_gpu_detector.SharedGPUDetector.test_independent_attempt_families_keep_conflicting_explicit_dirs_and_go_caps) ... ok
test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label (test_dashboard_gpu_detector.SharedGPUDetector.test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label) ... ok
test_malformed_CPU_stream_is_refused_and_explained (test_dashboard_gpu_detector.SharedGPUDetector.test_malformed_CPU_stream_is_refused_and_explained) ... ok
test_malformed_attempt_snapshots_show_unavailable_without_crashing_or_guessing (test_dashboard_gpu_detector.SharedGPUDetector.test_malformed_attempt_snapshots_show_unavailable_without_crashing_or_guessing) ... ok
test_native_selftests_and_help_do_not_claim_GPU_jobs (test_dashboard_gpu_detector.SharedGPUDetector.test_native_selftests_and_help_do_not_claim_GPU_jobs) ... ok
test_nested_env_ignore_environment_clears_outer_output_and_go_bindings (test_dashboard_gpu_detector.SharedGPUDetector.test_nested_env_ignore_environment_clears_outer_output_and_go_bindings) ... ok
test_new_wrappers_prompts_inline_modules_and_temp_copies_are_not_jobs (test_dashboard_gpu_detector.SharedGPUDetector.test_new_wrappers_prompts_inline_modules_and_temp_copies_are_not_jobs) ... ok
test_older_launcher_cannot_rescue_a_reused_resident_PID_record (test_dashboard_gpu_detector.SharedGPUDetector.test_older_launcher_cannot_rescue_a_reused_resident_PID_record) ... ok
test_parent_worker_and_admission_share_one_job_with_original_elapsed (test_dashboard_gpu_detector.SharedGPUDetector.test_parent_worker_and_admission_share_one_job_with_original_elapsed) ... ok
test_process2_record_is_bound_from_its_actual_nested_output (test_dashboard_gpu_detector.SharedGPUDetector.test_process2_record_is_bound_from_its_actual_nested_output) ... ok
test_process2_recorded_earlier_stage01_deadline_beats_stage3 (test_dashboard_gpu_detector.SharedGPUDetector.test_process2_recorded_earlier_stage01_deadline_beats_stage3) ... ok
test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu (test_dashboard_gpu_detector.SharedGPUDetector.test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu) ... ok
test_quoted_run_directory_is_preserved_as_exact_token (test_dashboard_gpu_detector.SharedGPUDetector.test_quoted_run_directory_is_preserved_as_exact_token) ... ok
test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget (test_dashboard_gpu_detector.SharedGPUDetector.test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget) ... ok
test_recorded_CPU_accepts_actual_publisher_microsecond_timestamps (test_dashboard_gpu_detector.SharedGPUDetector.test_recorded_CPU_accepts_actual_publisher_microsecond_timestamps) ... ok
test_reused_PID_with_older_open_record_cannot_supply_output (test_dashboard_gpu_detector.SharedGPUDetector.test_reused_PID_with_older_open_record_cannot_supply_output) ... ok
test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace (test_dashboard_gpu_detector.SharedGPUDetector.test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace) ... ok
test_stage2_requested_without_published_origin_has_no_invented_active_cap (test_dashboard_gpu_detector.SharedGPUDetector.test_stage2_requested_without_published_origin_has_no_invented_active_cap) ... ok
test_stale_future_expired_halted_finished_admission_and_wrong_kind_do_not_claim_CPU_activity (test_dashboard_gpu_detector.SharedGPUDetector.test_stale_future_expired_halted_finished_admission_and_wrong_kind_do_not_claim_CPU_activity) ... ok
test_transparent_wrappers_keep_GPU_jobs_and_exact_benchmark_output (test_dashboard_gpu_detector.SharedGPUDetector.test_transparent_wrappers_keep_GPU_jobs_and_exact_benchmark_output) ... ok
test_unrelated_same_namespace_process_families_are_two_competing_jobs (test_dashboard_gpu_detector.SharedGPUDetector.test_unrelated_same_namespace_process_families_are_two_competing_jobs) ... ok
test_clean_finish_is_not_an_alert (test_dashboard_live.Alerts.test_clean_finish_is_not_an_alert) ... ok
test_new_step_resets_the_clock (test_dashboard_live.Alerts.test_new_step_resets_the_clock) ... ok
test_no_progress_while_working (test_dashboard_live.Alerts.test_no_progress_while_working) ... ok
test_stopped_on_an_error (test_dashboard_live.Alerts.test_stopped_on_an_error) ... ok
test_waiting_for_an_answer (test_dashboard_live.Alerts.test_waiting_for_an_answer) ... ok
test_visible_width_only (test_dashboard_live.Clip.test_visible_width_only) ... ok
test_last_exit_line (test_dashboard_live.Coordinator.test_last_exit_line) ... ok
test_no_exit_yet (test_dashboard_live.Coordinator.test_no_exit_yet) ... ok
test_real_subprocess_nonzero_and_empty_responses_are_unavailable (test_dashboard_live.GPUInventory.test_real_subprocess_nonzero_and_empty_responses_are_unavailable) ... ok
test_shared_detector_recognizes_harvest_but_not_a_prompt_or_temp_copy (test_dashboard_live.GPUInventory.test_shared_detector_recognizes_harvest_but_not_a_prompt_or_temp_copy) ... ok
test_successful_nonempty_inventory_can_report_no_gpu_job (test_dashboard_live.GPUInventory.test_successful_nonempty_inventory_can_report_no_gpu_job) ... ok
test_clean_exit_reads_finished (test_dashboard_live.NowLines.test_clean_exit_reads_finished) ... ok
test_order_and_wording (test_dashboard_live.NowLines.test_order_and_wording) ... ok
test_running_gpu_job (test_dashboard_live.NowLines.test_running_gpu_job) ... ok
test_unavailable_inventory_never_reports_idle (test_dashboard_live.NowLines.test_unavailable_inventory_never_reports_idle) ... ok
test_changed_source_triggers_reload (test_dashboard_live.Reload.test_changed_source_triggers_reload) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/test_dashboard_live.py:57: ResourceWarning: unclosed file <_io.TextIOWrapper name='/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmp0tv4jub5/dashboard_x.py' mode='w' encoding='UTF-8'>
  open(p, "w").write("x")
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_decided_rows_and_prose_are_ignored (test_dashboard_live.Rulings.test_decided_rows_and_prose_are_ignored) ... ok
test_rows_whose_status_awaits_the_operator (test_dashboard_live.Rulings.test_rows_whose_status_awaits_the_operator) ... ok
test_events_newer_than_the_report_text (test_dashboard_live.Staleness.test_events_newer_than_the_report_text) ... ok
test_unparseable_updated_counts_everything_as_newer (test_dashboard_live.Staleness.test_unparseable_updated_counts_everything_as_newer) ... ok
test_rebuild_only_after_the_set_is_stable (test_dashboard_live.TeamTiles.test_rebuild_only_after_the_set_is_stable) ... ok
test_sessions_from_tile_start_commands (test_dashboard_live.TeamTiles.test_sessions_from_tile_start_commands) ... ok
test_team_sessions_skip_dashboard_and_viewers (test_dashboard_live.TeamTiles.test_team_sessions_skip_dashboard_and_viewers) ... ok
test_archived_logs_are_not_the_live_run (test_dashboard_live.WordsAndAnswers.test_archived_logs_are_not_the_live_run) ... ok
test_facts_from_the_last_recipe_with_answers (test_dashboard_live.WordsAndAnswers.test_facts_from_the_last_recipe_with_answers) ... ok
test_lines_mark_right_and_wrong_and_show_the_words (test_dashboard_live.WordsAndAnswers.test_lines_mark_right_and_wrong_and_show_the_words) ... ok
test_no_answers_recorded (test_dashboard_live.WordsAndAnswers.test_no_answers_recorded) ... ok
test_admission_receipt_labels_the_scope_and_keeps_plan_unstarted (test_dashboard_mathlab.Dashboard.test_admission_receipt_labels_the_scope_and_keeps_plan_unstarted) ... ok
test_builder_sized_checks_preserve_disclaimer_machine_findings_and_questions (test_dashboard_mathlab.Dashboard.test_builder_sized_checks_preserve_disclaimer_machine_findings_and_questions) ... ok
test_checks_paginate_and_keep_required_bars_ahead_of_large_observations (test_dashboard_mathlab.Dashboard.test_checks_paginate_and_keep_required_bars_ahead_of_large_observations) ... ok
test_finding_and_candidate_keep_tier_source_and_offline_status (test_dashboard_mathlab.Dashboard.test_finding_and_candidate_keep_tier_source_and_offline_status) ... ok
test_gpu_probe_error_is_visible_and_does_not_break_the_frame (test_dashboard_mathlab.Dashboard.test_gpu_probe_error_is_visible_and_does_not_break_the_frame) ... ok
test_halted_shows_reason_and_diagnostic (test_dashboard_mathlab.Dashboard.test_halted_shows_reason_and_diagnostic) ... ok
test_harvest_screen_shows_progress_deadline_cap_and_resources (test_dashboard_mathlab.Dashboard.test_harvest_screen_shows_progress_deadline_cap_and_resources) ... ok
test_idle_free_gpu_and_present_files_do_not_claim_a_build_or_launch_approval (test_dashboard_mathlab.Dashboard.test_idle_free_gpu_and_present_files_do_not_claim_a_build_or_launch_approval) ... ok
test_idle_freeze_wait_comes_from_the_current_status_line (test_dashboard_mathlab.Dashboard.test_idle_freeze_wait_comes_from_the_current_status_line) ... ok
test_idle_gpu_wait_names_the_current_shared_job (test_dashboard_mathlab.Dashboard.test_idle_gpu_wait_names_the_current_shared_job) ... ok
test_idle_ignores_stale_next_prose (test_dashboard_mathlab.Dashboard.test_idle_ignores_stale_next_prose) ... ok
test_idle_reads_status_with_trailing_review_prose (test_dashboard_mathlab.Dashboard.test_idle_reads_status_with_trailing_review_prose) ... ok
test_idle_rechecks_file_presence_on_every_frame (test_dashboard_mathlab.Dashboard.test_idle_rechecks_file_presence_on_every_frame) ... ok
test_idle_shows_plan_current_prereg_status_sha_and_wait (test_dashboard_mathlab.Dashboard.test_idle_shows_plan_current_prereg_status_sha_and_wait) ... ok
test_idle_unreadable_prereg_keeps_gpu_and_file_facts_visible (test_dashboard_mathlab.Dashboard.test_idle_unreadable_prereg_keeps_gpu_and_file_facts_visible) ... ok
test_idle_waits_for_each_missing_launcher_driver_and_notebook (test_dashboard_mathlab.Dashboard.test_idle_waits_for_each_missing_launcher_driver_and_notebook) ... ok
test_invalid_calibration_does_not_render_a_cheap_stop (test_dashboard_mathlab.Dashboard.test_invalid_calibration_does_not_render_a_cheap_stop) ... ok
test_invalid_is_labelled_no_verdict (test_dashboard_mathlab.Dashboard.test_invalid_is_labelled_no_verdict) ... ok
test_latest_run_is_selected_and_previous_run_is_not_rewritten (test_dashboard_mathlab.Dashboard.test_latest_run_is_selected_and_previous_run_is_not_rewritten) ... ok
test_malformed_line_remains_visible_in_a_short_frame (test_dashboard_mathlab.Dashboard.test_malformed_line_remains_visible_in_a_short_frame) ... ok
test_once_cli_at_80_and_200_columns (test_dashboard_mathlab.Dashboard.test_once_cli_at_80_and_200_columns) ... ok
test_run_selection_policy_and_other_active_run_count_are_visible (test_dashboard_mathlab.Dashboard.test_run_selection_policy_and_other_active_run_count_are_visible) ... ok
test_step_three_failed_check_is_explained_as_designed_cheap_stop (test_dashboard_mathlab.Dashboard.test_step_three_failed_check_is_explained_as_designed_cheap_stop) ... ok
test_step_two_pass_and_missing_resource_labels (test_dashboard_mathlab.Dashboard.test_step_two_pass_and_missing_resource_labels) ... ok
test_text_is_cleaned_and_width_is_bounded_at_80_200_and_300 (test_dashboard_mathlab.Dashboard.test_text_is_cleaned_and_width_is_bounded_at_80_200_and_300) ... ok
test_waiting_for_gpu_uses_shared_gpu_state_and_admission_reason (test_dashboard_mathlab.Dashboard.test_waiting_for_gpu_uses_shared_gpu_state_and_admission_reason) ... ok
test_all_event_variants_round_trip (test_dashboard_mathlab.EventContract.test_all_event_variants_round_trip) ... ok
test_append_preserves_previous_bytes_and_is_one_write_per_event (test_dashboard_mathlab.EventContract.test_append_preserves_previous_bytes_and_is_one_write_per_event) ... ok
test_duplicate_json_keys_and_wrong_run_id_are_reported (test_dashboard_mathlab.EventContract.test_duplicate_json_keys_and_wrong_run_id_are_reported) ... ok
test_malformed_schema_utf8_and_partial_lines_are_reported (test_dashboard_mathlab.EventContract.test_malformed_schema_utf8_and_partial_lines_are_reported) ... ok
test_missing_file_is_an_explicit_read_error (test_dashboard_mathlab.EventContract.test_missing_file_is_an_explicit_read_error) ... ok
test_run_purpose_is_an_optional_validated_schema_one_discriminator (test_dashboard_mathlab.EventContract.test_run_purpose_is_an_optional_validated_schema_one_discriminator) ... ok
test_short_append_raises (test_dashboard_mathlab.EventContract.test_short_append_raises) ... ok
test_unknown_missing_extra_and_reserved_fields_are_rejected_without_writing (test_dashboard_mathlab.EventContract.test_unknown_missing_extra_and_reserved_fields_are_rejected_without_writing) ... ok
test_wrong_types_outcomes_and_tiers_are_rejected (test_dashboard_mathlab.EventContract.test_wrong_types_outcomes_and_tiers_are_rejected) ... ok
test_admission_only_pass_never_completes_an_experiment_step (test_dashboard_mathlab.EventFold.test_admission_only_pass_never_completes_an_experiment_step) ... ok
test_aggregate_calibration_failure_is_the_cheap_stop (test_dashboard_mathlab.EventFold.test_aggregate_calibration_failure_is_the_cheap_stop) ... ok
test_aggregate_calibration_preserves_producer_outcome_before_run_finished (test_dashboard_mathlab.EventFold.test_aggregate_calibration_preserves_producer_outcome_before_run_finished) ... ok
test_denied_gpu_admission_then_allowed (test_dashboard_mathlab.EventFold.test_denied_gpu_admission_then_allowed) ... ok
test_finishing_a_stage_preserves_the_original_recent_events (test_dashboard_mathlab.EventFold.test_finishing_a_stage_preserves_the_original_recent_events) ... ok
test_fold_is_pure_and_recent_events_are_bounded (test_dashboard_mathlab.EventFold.test_fold_is_pure_and_recent_events_are_bounded) ... ok
test_gate_two_b_failure_does_not_stop_the_lab (test_dashboard_mathlab.EventFold.test_gate_two_b_failure_does_not_stop_the_lab) ... ok
test_halt_and_finished_states_survive_late_samples (test_dashboard_mathlab.EventFold.test_halt_and_finished_states_survive_late_samples) ... ok
test_invalid_is_no_verdict_and_resource_halt_is_not_a_cheap_stop (test_dashboard_mathlab.EventFold.test_invalid_is_no_verdict_and_resource_halt_is_not_a_cheap_stop) ... ok
test_legacy_admission_then_real_stage_is_an_experiment_run (test_dashboard_mathlab.EventFold.test_legacy_admission_then_real_stage_is_an_experiment_run) ... ok
test_mixed_run_stream_is_rejected (test_dashboard_mathlab.EventFold.test_mixed_run_stream_is_rejected) ... ok
test_new_stage_clears_previous_progress (test_dashboard_mathlab.EventFold.test_new_stage_clears_previous_progress) ... ok
test_no_events_is_not_started (test_dashboard_mathlab.EventFold.test_no_events_is_not_started) ... ok
test_one_proxy_can_fail_then_another_pass_without_stopping (test_dashboard_mathlab.EventFold.test_one_proxy_can_fail_then_another_pass_without_stopping) ... ok
test_producer_gate_identifiers_join_the_shared_planned_groups (test_dashboard_mathlab.EventFold.test_producer_gate_identifiers_join_the_shared_planned_groups) ... ok
test_running_harvest_and_progress (test_dashboard_mathlab.EventFold.test_running_harvest_and_progress) ... ok
test_step_two_pass_does_not_invent_step_one_pass (test_dashboard_mathlab.EventFold.test_step_two_pass_does_not_invent_step_one_pass) ... ok
test_successful_substage_does_not_finish_the_step (test_dashboard_mathlab.EventFold.test_successful_substage_does_not_finish_the_step) ... ok

----------------------------------------------------------------------
Ran 114 tests in 4.502s

OK
```

### Final110×40 render checks

| Capture under /private/tmp/dashboard_gpu_detector_final | Lines | Maximum visible width | Result |
|---|---|---|---|
| experiment_live_final_110x40 | 8 | 110 | PASS |
| mathlab_live_final_110x40 | 39 | 110 | PASS |
| fixture_harvest_final_110x40 | 6 | 110 | PASS |
| fixture_v7_final_110x40 | 4 | 110 | PASS |
| fixture_precast_final_110x40 | 4 | 110 | PASS |
| fixture_benchmark_final_110x40 | 4 | 110 | PASS |
| fixture_cpu_uv_final_110x40 | 6 | 110 | PASS |
| fixture_attempt4_final_110x40 | 6 | 110 | PASS |
| fixture_cpu_denied_final_110x40 | 8 | 110 | PASS |
| fixture_combined_final_110x40 | 15 | 110 | PASS |

Actual experiment CLI capture after final source changes (latest event sample2026-10-09T22:13:31.082490Z):

```text
 GPU UNAVAILABLE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [Errno 1] Operation not permitted: '/bin/ps'
 CPU RECORDED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Math-lab step 2 · 57:56 elapsed / cap 6540s
 Output: unavailable
 Run/events dir: results/mathlab_staging/runs/m2_20261009T211535Z_57196
 Fresh recorded activity; process unverified. Latest sample: 2026-10-09T22:13:31.082490Z

```

Actual status bar:

```text
GPU unavailable · CPU recorded: Math-lab step 2 57:56/6540s · out ? · events results/mathlab_staging/runs/m2_20261009T211535Z_57196   │   working 0 · asking 0 · active 0 · idle 0
```

mathlab_live_final_110x40:

```text
■ MATH LAB · test math estimates using saved model inputs                                                     
 MATH-PROXY · math estimate, not evidence
 Run m2_20261009T211535Z_57196 · running · step 2
 View: newest events file by mtime · other active runs (events): 0
 Elapsed 57m56s / hard deadline 1h48m · ends 2026-10-09T23:04:35.963345+00:00 · 51m03s left
 PLAN · ✓ passed ✗ failed ▶ current · not recorded ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 · 1 · Harvest: record internal model inputs for every prompt (one GPU pass).
 ▶ 2 · Reproduce: repeat the saved write calculation on CPU; check it matches.
 · 3 · Calibrate: check estimates against past results; failure stops cheaply.
 · 4 · Candidate questions: explore ideas later, after a new written plan.
 NOW ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Reproduce the saved write
 █████████░░░░░░░ 16/30 layer writes · stage time 57m54s / cap 1h49m
 CHECKS · 44 recorded · 0 failed / 0 invalid · page 4/6 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PASS 2a-update-A1_single-5 · bar <= 1e-05 · measured 0.0
  Offline write reproduces the saved calculation
 PASS 2a-projector-A2_coherent2-5 · bar meets {"null_n":7119,"probe_relative_max":1e-06} · measured object:2
  Offline projection matches the recorded write
 PASS 2a-update-A2_coherent2-5 · bar <= 1e-05 · measured 0.0
  Offline write reproduces the saved calculation
 PASS 2a-projector-A7_coined_coined-5 · bar meets {"null_n":7119,"probe_relative_max":1e-06} · measured objec…
  Offline projection matches the recorded write
 PASS 2a-update-A7_coined_coined-5 · bar <= 1e-05 · measured 0.0
  Offline write reproduces the saved calculation
 PASS 2a-projector-mint1_s0-5 · bar meets {"null_n":7119,"probe_relative_max":1e-06} · measured object:2
  Offline projection matches the recorded write
 PASS 2a-update-mint1_s0-5 · bar <= 1e-05 · measured 0.0
  Offline write reproduces the saved calculation
 PASS 2a-projector-mint1_s1-5 · bar meets {"null_n":7119,"probe_relative_max":1e-06} · measured object:2
  Offline projection matches the recorded write
 MACHINE · samples from this run; GPU display is shared ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Free memory ████████┃███████ 27.3035 GiB · floor 6 GiB (┃) · +21.3035 GiB above floor
 Lab memory 4.99937 GiB · CPU 106.3% · GPU state unavailable: [Errno 1] Operation not permitted: '/bin/ps'
 FINDINGS · MATH-PROXY: math estimate, not evidence (0) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None staged yet.
 CANDIDATE QUESTIONS (0; newest 3) · ideas to test ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 None yet; step 4 needs its own pre-registration.
 LAST EVENTS · newest 1 of 8 recent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 22:13:31 Machine: free 27.3035 GiB; lab 4.99937 GiB; CPU 106.3%
```

fixture_harvest_final_110x40:

```text
 GPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Math-lab harvest · 02:00 elapsed / cap 3600s
 Output: unavailable
 Run/events dir: unavailable
 Harvest artifact output is not linked in the run record.

```

fixture_v7_final_110x40:

```text
 GPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C10Z V7 probe · 02:00 elapsed / cap 3060s
 Output: results/c10z_v7_diagnostic/20261009T230000Z

```

fixture_precast_final_110x40:

```text
 GPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C10Y pre-cast · 02:00 elapsed / cap 2820s
 Output: results/c10y_precast_diag/20261009T230000Z

```

fixture_benchmark_final_110x40:

```text
 GPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C10Z benchmark · 02:00 elapsed / cap 600s
 Output: results/c10z_astra_benchmark/fixture

```

fixture_cpu_uv_final_110x40:

```text
 GPU IDLE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 CPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Math-lab step 2 · 02:00 elapsed / cap 6540s
 Output: unavailable
 Run/events dir: unavailable

```

fixture_attempt4_final_110x40:

```text
 GPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C10Z attempt 4 · 1:40 elapsed / cap 7200s
 Output: results/c10z_astra_attempt4
 Recorded budget stage01; current phase may have advanced
 Selected launch caps: stage01 7200s, stage2 18000s, stage3 24000s

```

fixture_cpu_denied_final_110x40:

```text
 GPU UNAVAILABLE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ps exit 1: fixture denial
 CPU RECORDED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Math-lab step 2 · 0:12 elapsed / cap 6540s
 Output: unavailable
 Run/events dir: results/mathlab_staging/runs/m2_fixture
 Fresh recorded activity; process unverified. Latest sample: 2026-10-09T20:00:00+00:00

```

fixture_combined_final_110x40:

```text
 GPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 C10Z V7 probe · 00:12 elapsed / cap 3060s
 Output: results/c10z_v7_diagnostic/20261009T230000Z

 CPU RUNNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Math-lab step 3 · 00:34 elapsed / cap 1800s
 Output: unavailable
 Run/events dir: unavailable

 CPU RECORDED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Math-lab step 2 · 0:12 elapsed / cap 6540s
 Output: unavailable
 Run/events dir: results/mathlab_staging/runs/m2_fixture
 Fresh recorded activity; process unverified. Latest sample: 2026-10-09T20:00:00+00:00

```

### Final source SHA-256 and scope

| File | SHA-256 |
|---|---|
| tools/dashboard_live.py | 75ca7100c0f64bc3debd14e05c6e65a2109238057dfa98620f96f5082c35b572 |
| tools/dashboard_experiment.py | 933c2336c5813e3a9f444b88ee58ba0ab8a255917db051d5331dcdfbe2d7b640 |
| tools/dashboard_bar.sh | 535e04d3ea0357183e9448e95e88a673294d83aba4772208be545c2f8e3a4b0e |
| tools/test_dashboard_live.py | b9fec5d1c0eceea40e5caad6222d56447352cf79cdbeb0ac8f984ec25e9ed81d |
| tools/test_dashboard_gpu_detector.py | e2b86fad7dd00bab2c4b8a349d33c0abb91a2a4cc43cf70c6603a33128153173 |

All **36** protected snapshots from this resume are unchanged: bar/live-test adaptation, tools/dashboard_mathlab.py, tools/mathlab_events.py, every captured tools/labviz/** file and prereg/driver/reader/benchmark/c10e/engine source. This is a scoped hash comparison, not a global clean-tree claim. Snapshot and source deltas: /private/tmp/dashboard_gpu_detector_final/before.json, scope_check.json and *.delta.patch. Prior parked text/RED evidence is retained; no shared/unrelated work reverted.

### Completion handoff — 2026-10-09T22:18:12.866792+00:00

**Done:** shared detector and both consumers complete; all requested harvest/V7/precast/benchmark/attempt4/CPU aliases; explicit directory provenance, source/recorded caps, CPU/GPU separation, fresh event fallback; native-selftest/help exclusion; reviewed PID-age/nested-env fixes; final114 tests and10 final-source110×40 captures plus real bar PASS. Exact report: results/dashboard_gpu_detector_report.md; production files: tools/dashboard_live.py and tools/dashboard_experiment.py; controls: tools/test_dashboard_gpu_detector.py. Complete evidence and source snapshots under /private/tmp/dashboard_gpu_detector_final/.

**In flight / next:** no detector implementation remains. MAESTRO's Astra admission/go review is separate and has priority if it requests a fix. The earlier admission receipt/go draft stay unchanged at results/c10z_astra_attempt4_prep/admission_receipt_drift3.md and go_record_draft.json. No live go/attempt4 is created by the detector. Dashboard CLI/bar renders are verified; active native GPU process inventory and interactive tmux visibility remain UNVERIFIED because ps is denied here. Existing panes already reload changed dashboard sources on their normal loop; no tmux rebuild/activation was initiated.

**Risks / boundaries:** do not treat CPU event PID as liveness, recorded budget snapshots as current phase/deadline guarantees, or unknown artifact directories as the newest folder. Preserve concurrent shared edits and all historical outcomes. No GPU/MPS/model load, job launch, commits or mutating git. Do not edit tools/dashboard_mathlab.py, tools/mathlab_events.py or tools/labviz/**. Context-save checkpoint is stored under temporary GSTACK_HOME in /private/tmp; no home-memory updates.

**Binding context rule:** watch Context N% left. Before approximately20%, stop starting new work; append a handoff with done / in flight / exact paths / next step / risks to the report and tell the operator so a fresh successor can start. Every handoff restates this rule.

## Operator-requested final stopping point — 2026-10-09T22:26:39.364484+00:00

**Detector state: COMPLETE.** No implementation is in flight or deferred. The final114-test run (34 detector/experiment/bar,27 live,53 MathLab;4.502 s) and ten final-source110×40 renders are already verified and retained in /private/tmp/dashboard_gpu_detector_final/review_fix_green.txt and render_final_checks.json. No tests, GPU/model jobs or launches were rerun during this handoff. Native process inventory and interactive teamdash/tmux visibility remain UNVERIFIED because ps is denied here; the operator can observe the queued jobs outside the sandbox. Do not launch a job to obtain that evidence. No excluded MathLab/Lab View or science file was edited.

**Exact handoff:** results/c10z_astra_attempt4_prep/handoff_codexz2_20261009.md covers all V7/A1 builds and fixes, frozen/current SHAs, CPU test commands using TMPDIR under /private/tmp, drift#3 admission, the live go and the strict process2 gate. Current read-only check: the published live go equals approved draft SHA850988a5df22446d1f456c2ce270e2bffcd988c6f118bcb14d77f4f1ae9ca04f. MAESTRO reports process1 queued via tools/run_c10z_attempt.sh after C10Y pre-cast; attempt4 directory and chain/stage3 logs are not yet present at closeout. This supersedes earlier dated statements that the live go did not exist. Scheduling is operator-provided, not verified process liveness.

**Next / risks:** no detector code step remains. Native dashboard acceptance is unverified; current Astra approvals are A1 FREEZE+GO and admission ADMIT+GO. Preserve sources/evidence; do not duplicate the queue, infer GPU clearance, or start process2 before a clean completed K2 survivor requests3 and process1 actually exits. No commits.

**BINDING CONTEXT RULE:** watch Context N% left. Before approximately20%, stop starting new work, record done / in flight / exact paths / next step / risks in the report and tell MAESTRO so a fresh successor can start. Every handoff restates this rule. Codex Z2 stops after writing and verifying the named handoff.

## Codex Z3 successor verification — 2026-10-09T22:32:34.880140+00:00

**DETECTOR DONE.** Z2's final implementation was already complete: all five dashboard source/test hashes match the predecessor handoff. Z3 read that handoff in full, the detector report's current completion and historical stopping states, and current frozen §12. Fresh test-first verification passed **114 tests (34 detector/experiment/bar + 27 live + 53 MathLab), zero failures/errors/skips**, in 2.966 s. No new failing control or production edit was needed; the retained RED→GREEN evidence above remains historical evidence, not a fresh RED claim.

The one shared detector remains tools/dashboard_live.py; tools/dashboard_bar.sh uses its --gpu-summary, and tools/dashboard_experiment.py uses gpu_state(). Controls cover Math-lab harvest and CPU launcher/runner/uv notebooks, C10Z V7, benchmark, attempt/stage/resident, and C10Y pre-cast; name, elapsed/cap and exact known namespace; ancestry deduplication, conflicting jobs, PID-age budget binding, env clearing, prompt/selftest/help exclusion, and CPU/GPU separation. Unknown artifact output remains explicitly unavailable, with run/events provenance separate.

**Fresh headless evidence:** ten captures passed at **110×40**, plus the real status-bar CLI. Live experiment observation showed a fresh Math-lab step-2 event (sample 2026-10-09T22:29:50.190884Z), elapsed 1:14:18/cap 6540s, exact events directory results/mathlab_staging/runs/m2_20261009T211535Z_57196, process unverified. /bin/ps was denied; GPU is UNAVAILABLE, never inferred idle. The independently timed live bar capture likewise reports GPU unavailable. Native process inventory and interactive teamdash/tmux acceptance remain **UNVERIFIED**. Fixtures establish active-job display, not live GPU liveness or science admission.

| Capture in /private/tmp/dashboard_gpu_detector_z3.Y8CQmC | Lines | Maximum width | Result |
|---|---|---|---|
| experiment_live_final_110x40 | 8 | 110 | PASS |
| mathlab_live_final_110x40 | 39 | 110 | PASS |
| fixture_harvest_final_110x40 | 6 | 110 | PASS |
| fixture_v7_final_110x40 | 4 | 110 | PASS |
| fixture_precast_final_110x40 | 4 | 110 | PASS |
| fixture_benchmark_final_110x40 | 4 | 110 | PASS |
| fixture_cpu_uv_final_110x40 | 6 | 110 | PASS |
| fixture_attempt4_final_110x40 | 6 | 110 | PASS |
| fixture_cpu_denied_final_110x40 | 8 | 110 | PASS |
| fixture_combined_final_110x40 | 15 | 110 | PASS |

Exact commands (fresh private temporary root; bytecode disabled):

    /opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/dashboard_gpu_detector_z3.Y8CQmC PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/dashboard_gpu_detector_z3.Y8CQmC/verify_dashboard.py
    /opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/dashboard_gpu_detector_z3.Y8CQmC PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/dashboard_gpu_detector_z3.Y8CQmC/render_z3.py
    /opt/homebrew/bin/rtk proxy git diff --check -- tools/dashboard_live.py tools/dashboard_experiment.py tools/dashboard_bar.sh tools/test_dashboard_live.py tools/test_dashboard_gpu_detector.py

The test runner and render driver reject science imports (torch, transformers, datasets, huggingface_hub, numpy, scipy). Tests and actual render CLI/bar calls exit0 and yield nonempty output. Complete verbose test output and all captures are retained in the named evidence directory. These are single-use evidence writers; reproduce in a fresh directory rather than overwriting them.

**Scope:** all **49** captured protected files remain byte-identical, including dashboard sources/tests, excluded tools/dashboard_mathlab.py, tools/mathlab_events.py, all captured tools/labviz/**, science sources/launchers, frozen prereg and published go. Scoped git diff --check passed. Z3’s only intentional repository edit is this report; helpers/evidence/checkpoint are under /private/tmp. This 49-file comparison is scoped source evidence, not a global clean-tree or cache-immutability claim. Graft’s ignored graft/.cache/ask-index.json was not included in the snapshot; no pre-call hash or mutation attribution is claimed. Existing dirty/untracked work was preserved. No GPU/MPS/model load, job launch, dashboard restart, commits or mutating git operations.

| Current source | SHA-256 |
|---|---|
| tools/dashboard_live.py | 75ca7100c0f64bc3debd14e05c6e65a2109238057dfa98620f96f5082c35b572 |
| tools/dashboard_experiment.py | 933c2336c5813e3a9f444b88ee58ba0ab8a255917db051d5331dcdfbe2d7b640 |
| tools/dashboard_bar.sh | 535e04d3ea0357183e9448e95e88a673294d83aba4772208be545c2f8e3a4b0e |
| tools/test_dashboard_live.py | b9fec5d1c0eceea40e5caad6222d56447352cf79cdbeb0ac8f984ec25e9ed81d |
| tools/test_dashboard_gpu_detector.py | e2b86fad7dd00bab2c4b8a349d33c0abb91a2a4cc43cf70c6603a33128153173 |

| Evidence file in /private/tmp/dashboard_gpu_detector_z3.Y8CQmC | SHA-256 |
|---|---|
| verify_dashboard.py | 3403bd794f7f2b55adf8477148f9e9631914cdc7ff2f76b7d310dc58bb6fff21 |
| dashboard_tests.txt | d09f4460f8a8aea68e3c6d94dbf1c11837340bb29cad36975b8a5dba155834f6 |
| test_summary.json | 5b6967e74186e84cffaeb28aea01a769143f6a7ae9dece399c9b1bfc68c3b4f9 |
| render_z3.py | 970f862c263644bd4eff41cc2a9c4e5f21821acf858515592e8131cd197ebfd6 |
| render_final_checks.json | cdb5ae144b5c277a805864e80fd5ca5b0ac3eb41e0b8ae8a8c2d6672caba8b7e |
| scope_check.json | 2355f632e3b0238221d4eebb8da491227621cef0db18da03af8ca5602b7771b4 |
| bar_live_final.txt | 744619d213230ff2ae50a1a0919e6fe64c3851e9ee1b57b654438e8df1e4cde5 |

**Context saved:** /private/tmp/dashboard_gpu_detector_z3.Y8CQmC/gstack/projects/c10k-route-a/checkpoints/20261009-223049-codex-z3-detector-complete-attempt4-standby.md, using the context-save format with temporary GSTACK_HOME; no home-memory writes or external synchronization.

**Done / in flight / next / risks:** detector verification complete; no implementation remains. Task2 is STANDBY until MAESTRO asks for attempt-4 process1 outcome reading. Authority: results/c10z_astra_attempt4_prep/handoff_codexz2_20261009.md, “Reading attempt-4 outcomes and the process-2 gate,” and frozen docs/C10Z_ASTRA_PREREG.md §12. Use the actual directory reader at that time; process2 needs validated scientific_verdict=true/next_stage=3, clean closed completed=2/no halt, actual resident AND coordinator exit evidence from the operator, current bound ceilings/source/environment/go/benchmark and clear queue, and a nonexistent fresh process2/ namespace. No process2 permission is asserted now. Main risks: treating recorded events as process liveness, missing/denied observation as GPU clearance, stale source identity, or premature/duplicate dispatch.

**BINDING CONTEXT RULE:** watch Context N% left; before approximately20%, stop starting new work, write done / in flight / exact paths / next step / risks into this report, and tell MAESTRO so a fresh successor can start. Every handoff restates this rule.

## Codex Z3 detector fix round 1 — 2026-10-09T22:44:33.145939+00:00

**DETECTOR FIX DONE.** Read results/dashboard_gpu_detector_astra_r1.md in full; reproduced both BLOCKING findings before production edits and fixed them in one round. The previous114 controls missed these cases. Final evidence: **120 dashboard tests PASS (40 detector/experiment/bar +27 live +53 MathLab), zero failures/errors/skips, 4.242s; sixteen110×40 headless captures PASS; real live status bar and real worker-only fixture bar PASS.** No science/GPU permission or process2 eligibility is implied.

| Astra blocker / boundary | RED before edits | Fix / GREEN |
|---|---|---|
| Lone legacy _job falsely free | blockers_red.txt: shared running=None; experiment GPU IDLE; unchanged MathLab GPU free. Real bar already busy. Three failing subtests; worker-only test tools/test_dashboard_gpu_detector.py:551. | dashboard_live.py:502 still prefers a coordinator and falls back to an observed GPU worker. worker_green.txt: worker-only across all three consumers plus existing coordinator-priority control PASS. |
| CPU activity removes legacy details | blockers_red.txt: all three live-CPU, fresh-recorded-CPU and malformed-CPU-record cases lose stage p2-eval. Legacy-only positive control already PASS, proving the fixtures/observation sink. Tests tools/test_dashboard_gpu_detector.py:588/597/605. | dashboard_experiment.py:256 selects legacy detail when legacy GPU jobs exist; cpu_lines at:238 composes CPU/event-error metadata alongside it. Final render retains stage, progress1 of3, finished27/72, NOW/training step7 and exact live-log marker at110×40. |
| Legacy worker starts before a log exists | no_logs_red.txt: one assertion failure, zero errors; stage _job absent. Test tools/test_dashboard_gpu_detector.py:579. | Explicit active-GPU/no-log display plus CPU summaries; metadata and unavailable sink remain visible. |

Initial blocker run:5 tests,6 assertion failures,0 errors; no-log boundary:1 test,1 assertion failure,0 errors. After the respective edits: worker2 PASS; all6 new controls PASS. Full dashboard discovery then passed120. The original alias, namespace/cap, PID-age, env-clear, unavailable-inventory and CPU-event controls remain GREEN.

The CPU rendering block is shared between generic and legacy panels; it preserves process-verified versus recorded/unverified status, elapsed/cap, exact known output/events directories and error text. Legacy rows remain width-clipped. No changes to detector aliases, science paths, admission/go records, frozen prereg or excluded MathLab/Lab View files.

Exact commands; all temporary state/fixtures under /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau, bytecode disabled:

    /opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/run_checks.py blockers_red test_dashboard_gpu_detector.SharedGPUDetector.test_worker_only_inventory_is_busy_in_all_three_consumers test_dashboard_gpu_detector.SharedGPUDetector.test_legacy_experiment_fixture_contains_progress_results_and_logs test_dashboard_gpu_detector.SharedGPUDetector.test_legacy_experiment_details_survive_concurrent_CPU_process test_dashboard_gpu_detector.SharedGPUDetector.test_legacy_experiment_details_survive_recorded_CPU_activity test_dashboard_gpu_detector.SharedGPUDetector.test_legacy_experiment_details_survive_CPU_record_error
    /opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/run_checks.py no_logs_red test_dashboard_gpu_detector.SharedGPUDetector.test_legacy_worker_without_logs_keeps_GPU_and_CPU_activity_visible
    /opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/run_checks.py all_dashboard_green
    /opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/render_fix1_corrected.py
    /opt/homebrew/bin/rtk proxy git diff --check -- tools/dashboard_live.py tools/dashboard_experiment.py tools/test_dashboard_gpu_detector.py

Evidence writers are exclusive/single-use: use a fresh namespace when reproducing. The first temporary expanded-render helper used literal backslash-n joins in its new fixture section and failed its width assertion. Failure retained in render_helper_initial_failure.txt and partial captures retained at the evidence root. Only that temporary helper was corrected; all16 successful final captures are in renders_corrected/. No dashboard-source change was made to accommodate the helper failure. Both runners reject torch/transformers/datasets/huggingface_hub/numpy/scipy imports.

| Final capture under /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/renders_corrected | Lines | Maximum width | Result |
|---|---|---|---|
| experiment_live_final_110x40 | 8 | 110 | PASS |
| mathlab_live_final_110x40 | 24 | 110 | PASS |
| fixture_harvest_final_110x40 | 6 | 110 | PASS |
| fixture_v7_final_110x40 | 4 | 110 | PASS |
| fixture_precast_final_110x40 | 4 | 110 | PASS |
| fixture_benchmark_final_110x40 | 4 | 110 | PASS |
| fixture_cpu_uv_final_110x40 | 6 | 110 | PASS |
| fixture_attempt4_final_110x40 | 6 | 110 | PASS |
| fixture_cpu_denied_final_110x40 | 8 | 110 | PASS |
| fixture_combined_final_110x40 | 15 | 110 | PASS |
| fixture_worker_only_110x40 | 13 | 110 | PASS |
| fixture_mathlab_worker_only_110x40 | 38 | 110 | PASS |
| fixture_legacy_CPU_running_110x40 | 18 | 110 | PASS |
| fixture_legacy_CPU_recorded_110x40 | 19 | 110 | PASS |
| fixture_legacy_CPU_error_110x40 | 16 | 110 | PASS |
| fixture_legacy_worker_no_logs_110x40 | 8 | 110 | PASS |

**Scope:**49 captured source/protected hashes; exactly the3 permitted dashboard/test sources changed, all46 others unchanged, including tools/dashboard_mathlab.py, tools/mathlab_events.py, tools/labviz/**, bar/live/MathLab tests, launchers/science sources, frozen prereg and published go. Own deltas retained in *.delta.patch. Scoped git diff --check PASS; workspace/branch reconfirmed worktree-c10k-route-a. This is scoped evidence, not a global clean-tree/cache claim. Repository edits in this round: tools/dashboard_live.py, tools/dashboard_experiment.py, tools/test_dashboard_gpu_detector.py and this append-only report. No GPU/MPS/model load, science/job launch, commits or dashboard restart; concurrent work preserved.

| Final changed source | SHA-256 |
|---|---|
| tools/dashboard_live.py | adab10516a889bee1227706597869693a113b7e56af5b2b6757771fd44ecb96b |
| tools/dashboard_experiment.py | 40e6dd310446935e660ec81aea2aa8d0655b4218de320abff2737e224cb0d772 |
| tools/test_dashboard_gpu_detector.py | 7122338f12c0bc8461847301ba90bcdd0c1b3a9c4220433ef0033d83a98005ab |

| Evidence in /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau | SHA-256 |
|---|---|
| blockers_red.txt | 5e5d6706cf6305a20fc86655517cd05a0e758e693476b9c159595a38cf62f9b7 |
| no_logs_red.txt | 4c5be5688a6047111718d0efca3802a812de6ea5cf7ddf987a2ec7dabd58cd33 |
| worker_green.txt | e858a9acb1e5025ebf481fc50ab663ad31265fc5d5933acab2d31252b70858f4 |
| blockers_green.txt | b014cb6fb8d6d835fdf69370e9995631c04f6d2717488bee5a87b277533f00a5 |
| all_dashboard_green.txt | 0558df8cb951f9e2b66b717e1199d70be1a8f6a61182934f0ef25d554bfea99d |
| scope_check.json | 720259c97762efd3db3b617df0114c59c93381cc64d0c5ee406f20d341afef6c |
| render_helper_initial_failure.txt | c2dc313ecf70ebd372c8070b34fc978c404780610137297e877be0cba19dcc96 |
| render_fix1_corrected.py | ce4982cbc510d1b0b3d431dc4bcae3b00a0226a4321bd21cf607726a9f815b76 |
| renders_corrected/render_final_checks.json | 417265be25bec18b4ea4f0c4e9d0cca4bbbc970e4171fe8de82160ec795fbee8 |

**Evidence limits:** native successful process inventory and interactive tmux acceptance remain UNVERIFIED: actual CLI rendering reports GPU unavailable on denied /bin/ps. Fixtures verify rendering and shared state, not native liveness or science results. Astra's non-blocking refresh-scan/ps-timeout suggestion was not part of these two BLOCKING fixes; existing read behavior remains unchanged. No new independent Astra re-review is claimed.

**Context-save / standby handoff:** /private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/gstack/projects/c10k-route-a/checkpoints/20261009-224305-codex-z3-detector-fix1-complete-attempt4-standby.md. Done: both BLOCKING fixes, RED/GREEN,120-test suite,16 renders and scoped preservation. In flight: none. Next: MAESTRO's review and attempt4 process1 outcome request; attempt4 standby still takes priority on interrupt. Source-faithful gate remains the Z2 handoff plus frozen §12: actual reader scientific_verdict=true/next_stage3, clean closed completed2/no halt, operator-native resident AND coordinator exit, current bound source/environment/go/benchmark/ceilings and clear queue, fresh nonexistent process2 namespace. Do not launch, retry, or infer clearance; no process2 permission asserted now. Main risks: misreading recorded CPU activity as liveness, denied ps as idle, stale hashes, or premature/duplicate dispatch.

**BINDING CONTEXT RULE:** watch Context N% left; before approximately20%, stop starting new work, write done/in-flight/exact paths/next step/risks into the task report and tell MAESTRO to start a fresh successor. Every handoff restates this rule.
