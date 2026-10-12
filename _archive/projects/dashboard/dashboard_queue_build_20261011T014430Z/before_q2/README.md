# Q1 queue tab build

Status: READY FOR MAESTRO HOST RUN. Sandbox verification: **15/15 GREEN**, no skips. Host acceptance: **UNVERIFIED**.

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch `worktree-c10k-route-a`.

The tab reads `docs/program_state.json` beside its own tools directory, parses `work_queue` into immutable typed items, and redraws every five seconds. The queue data remains MAESTRO's source. Every tick independently reads the default tmux server, reviewer processes, and MathLab event files. No observation cache or queue data file is written. A missing or malformed source, denied probe, or incomplete event line is visible on the tab.

## Verification receipts

Original criterion RED: **11 tests, 11 failures, 0 errors, 0 skips**, exit 1 (`red.log`, `red.exit`), before any queue implementation, launcher, integration change or host runner. `tests_before_implementation.py` preserves the exact tests. The original eleven test bodies were verified unchanged by AST comparison.

Initial implementation: **11/11 GREEN** (`green_attempt1.log`). Review added four boundary regressions before their fixes. Explicit regression RED: **4 tests, 4 failures, 0 errors, 0 skips**, exit 1 (`red_edge_behavior.log`). The first edge probe also remains saved (`red_edge_regressions.log`: three assertion failures and one real `shlex` error); that exception was converted into an explicit failing assertion before the fixes. Final `/usr/bin/python3 -B tools/test_dashboard_queue.py`: **15/15 GREEN**, exit 0 (`green.log`, `green.exit`), running on Python **3.9.6**. Aggregate: all **15 distinct tests** have recorded RED and GREEN evidence.

| Criterion | Test | RED | GREEN |
| --- | --- | --- | --- |
| 1 | `test_01_parse_typed_items_and_show_each_bad_field` | FAIL, `red.log` | PASS, `green.log` |
| 2 | `test_02_renderer_is_pure_and_live_is_a_session_mapping` | FAIL, `red.log` | PASS, `green.log` |
| 3 | `test_03_display_width_word_wrap_and_long_word_hanging_indent` | FAIL, `red.log` | PASS, `green.log` |
| 4 | `test_04_ordered_cards_header_attention_and_dependency_titles` | FAIL, `red.log` | PASS, `green.log` |
| 5 | `test_05_elapsed_countdown_overrun_null_and_local_clock` | FAIL, `red.log` | PASS, `green.log` |
| 6 | `test_06_live_status_memory_and_queue_session_scope` | FAIL, `red.log` | PASS, `green.log` |
| 7 | `test_07_stale_queue_boundary_and_absent_key_plainly_visible` | FAIL, `red.log` | PASS, `green.log` |
| 8 | `test_08_loop_reloads_recovers_midwrite_redraws_and_limits_color` | FAIL, `red.log` | PASS, `green.log` |
| 9 | `test_09_launcher_idempotent_python_path_and_team_registration` | FAIL, `red.log` | PASS, `green.log` |
| 10 | `test_10_host_runner_records_every_step_and_owns_only_q1check_socket` | FAIL, `red.log` | PASS, `green.log` |
| 11 | `test_11_live_detection_unlisted_reviewers_experiment_and_finished_override` | FAIL, `red.log` | PASS, `green.log` |

| Additional regression | RED | GREEN |
| --- | --- | --- |
| test_12: unrelated process prompt quotes cannot hide reviewers | FAIL | PASS |
| test_13: state words inside notes/summary cannot gain color | FAIL | PASS |
| test_14: inherited main-checkout LLMDB_ROOT cannot redirect the tab | FAIL | PASS |
| test_15: empty successful tmux inventory cannot imply a finished builder | FAIL | PASS |

`fixture_width_40.txt`, `fixture_width_50.txt`, `fixture_width_60.txt`, `fixture_width_80.txt`, `fixture_width_100.txt`, and `fixture_width_160.txt` show static fixture renders. All lines were measured independently in terminal display cells. The criterion test also covers overlong words, wide characters, combining marks, and hanging indentation.

`bash -n` for the launcher, team script and host runner is GREEN (`shell_syntax.log`, `.exit`). `git diff --check` is GREEN (`diff_check.log`, `.exit`). Scope/integration comparison is GREEN (`scope_check.log`, `.exit`). `scoped_status.log` reports only the four authorized tools paths. `before_sha256.json` and `after_sha256.json` preserve the scoped source hashes.

## Pane-reading choice and behavior

Reused `tools/dashboard_live.py:15` (`BUSY_RE`) and `tools/dashboard_live.py:690` (`cell_width`), both pure helpers. Its pane-reading `team_screens()` at line 623 caches observations and reads a broader roster; `sh()` at line 548 returns empty output on failure. Q1 instead uses `gather_live()` with injected command execution, exact session targets, explicit default-server selection, and visible errors. The default socket is explicit because the host smoke tab itself runs on the separate q1check socket.

Each tick captures only queue-named sessions plus every default-server `codex*` session. The latest reply is checked for READY/HANDOFF, including wrapped replies; old tokens and quoted user instructions do not finish a currently working builder. Missing running sessions and finished replies change their cards to IN REVIEW with “builder finished — waiting for MAESTRO.” Header counts use the same derived card state. Unlisted sessions, reviews and unfinished recorded runs remain visible with “not yet described in the queue.” Unavailable inventories retain an explicit unavailable observation.

The pure `render(queue, live, now, width)` receives an aware local time and all observations. ETA countdowns and local 12-hour clocks derive from those arguments. The edge alone reads the clock and applies ANSI color to the header and actual state badges for TTY stdout. Mid-write queue JSON renders an error and retries next tick; fixture loop controls verify reloads, redraws, and live gathering on every tick.

## Host acceptance — MAESTRO

```bash
bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh'
```

The runner saves every command's output and exit code in this directory. It runs the test file; renders the real program state at widths 40 and 100; refuses a pre-existing q1check server; starts the tab with `/usr/bin/python3 '<absolute tools/dashboard_queue.py>'` in a throwaway session on `tmux -L q1check`; waits about eight seconds; captures the pane; checks that the pane is alive; and kills only the server it started on that socket. During the smoke run it saves the exact `c10w_p2_gate.check_gpu()` probe. A separate receipt verifies the tab's PID/path is absent from GPU blockers. Other legitimate blockers stay visible in the full gate output. The default dashboard session is untouched by this runner.

Expected host files include `tests.txt/.exit`, `render_40.txt/.exit`, `render_100.txt/.exit`, `tmux_probe.txt/.exit`, `tmux_start.txt/.exit`, `gpu_check.txt/.exit`, `tmux_capture.txt/.exit`, `tmux_panes.txt/.exit`, `queue_exemption.txt/.exit`, `tmux_cleanup.txt/.exit`, and `host_summary.txt`. Host tmux lifecycle, actual process inventory and GPU admission have not been claimed from sandbox fixtures. The gate's documented CLT Python exemption is separately GREEN against a command-line fixture in criterion 8.

MAESTRO installs the queue tab after the host receipts pass. This build has no commits, pushes, model/science runs, .venv use, live dashboard changes, queue-data edits, staging or deletions. MB41 and MAESTRO-owned files were left alone.

## Files changed and SHA-256

The existing `tools/team_dashboard.sh` changed by one tab-list comment and one call after the storage tab. The other listed tools files and host runner are new.

| File | SHA-256 |
| --- | --- |
| `tools/dashboard_queue.py` | `7cb9132ab9809e5b3dd5660e36d6d3b299819f6f55813d8aaecf5129b007d5b5` |
| `tools/test_dashboard_queue.py` | `aa5792d8acf1207f9b4ae71bd3d7265670687839603c2ebb2ceb64e29815eecb` |
| `tools/dashboard_queue_tab.sh` | `d3fbf908b733d9e901f34a6ba7420fd23ae1b1ed6cde7b165dcad371b0957f27` |
| `tools/team_dashboard.sh` | `f5dc68bf586ea9a6a33539fee0cd2646547d151dbc876661d76da5917477d3e1` |
| `results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh` | `c96cfd451bc619d77a6bffd84a79874e1d7c6306399a2667a40159abea4e193a` |

## Session context saved

The context-save workflow is recorded in this allowed receipt directory (`context_saved.md`), preserving scope, decisions, receipts and the next host command. The useful session lessons are the main-checkout environment trap, unrelated process text at the inventory boundary, and restricting color to an actual badge. No global memory file was edited.

Binding operator context directive (2026-10-10): watch “Context N% left.” Start a new piece of work only at >=60% left. At <=40% left, or on any “Context compacted,” stop starting work, append a handoff here with done/half-done, exact paths, SHA-256s, test state and one next step, and reply “Q1 HANDOFF.” Restate this directive in every handoff.
