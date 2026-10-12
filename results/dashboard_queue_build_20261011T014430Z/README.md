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


## Q2 round

Status: **QUEUE TAB READY FOR MAESTRO RUN**. Sandbox: **24/24 queue GREEN**
(original 15 Q1 criteria plus nine Q2 regressions), **40/40 shared detector GREEN**,
no errors or skips. Actual host acceptance: **UNRUN**; `host_attempt2/` is reserved
for the next host execution and is not populated by sandbox fixtures.

Before editing, the two queue files, current host runner and this README were
copied into `before_q2/`; their source SHA-256s are in `q2_before_sha256.json`.
The runner snapshot includes MAESTRO's prior capture-target correction; its
actual pre-Q2 hash is used here rather than the historical Q1 README hash.
Q1 and host-attempt-1 outputs were not overwritten.

| Evidence | Counts and result | Receipt |
| --- | --- | --- |
| Unmodified Q1 baseline | 15 tests, 15 PASS, exit 0 | `q2_baseline.log/.exit` |
| Q2 RED before fixes | 9 tests, all 9 FAIL; 14 failed assertions including subtests; 0 errors/skips, exit 1 | `q2_red.log/.exit`, tests in `q2_tests_before_fix.py` |
| Clean host-fixture RED against saved Q1 runner | 3 tests, 3 FAIL, 0 errors/skips, exit 1 | `q2_red_host_clean.log/.exit` |
| All Q2 RED reconfirmed against saved Q1 after fixture corrections | 9 tests, all 9 FAIL; 14 failed assertions including subtests; 0 errors/skips, exit 1 | `q2_red_confirmed.log/.exit` |
| First GREEN attempt | 24 tests; 23 PASS, one fixture failure, exit 1 | `q2_green_attempt1.log/.exit` |
| Final queue GREEN | 24 tests, 24 PASS, 0 errors/skips, exit 0 | `q2_green.log/.exit` |
| Existing shared detector suite | 40 tests, 40 PASS, 0 errors/skips, exit 0 | `q2_shared_detector_green.log/.exit` |
| Shell syntax, diff whitespace, protected sources | PASS, exit 0 | `q2_shell_syntax`, `q2_diff_check`, `q2_scope_check` `.log/.exit` pairs |
| Python 3.9 + real-source sandbox renders | PASS; widths 40/100 fit; abandoned NEW1 absent | `q2_sandbox_render_40` and `_100` `.txt/.stderr/.exit` |

`test_q2_01` catches the exact-session target defect; `test_q2_02` catches repeated
unavailable diagnostics; `test_q2_03` reproduces the abandoned NEW1 folder;
`test_q2_04` checks 0/599/600/601-second freshness and terminal-event exclusions;
`test_q2_05` proves shared process-to-run binding, rejects mismatched directories
and script names quoted in shell prompts, and excludes terminal runs despite a
matching process. `test_q2_06` catches the estimate timestamp wording. The last
three tests execute the real host script with shell fixtures and verify the new
output namespace and both required host failure outcomes.

Q1's fifteen test names and criteria remain. Obsolete literal expectations now
use `=NAME:`, “estimate made”, and the shared detector's PPID-bearing ps format.
Event fixtures use deterministic modification times and inspect the typed live
run's name. No assertions were dropped or turned into skips.

Process liveness reuses `tools/dashboard_live.py:123` (`detect_gpu_jobs()`), via
the same classification that `gpu_state()` at line 565 exposes to
`tools/dashboard_experiment.py:101` and `tools/dashboard_mathlab.py:157`.
`dashboard_live.py:283` (`recorded_cpu_jobs()`) requires CPU experiment steps 2/3
and a fresh resource sample; it does not fit NEW1. Its declared process roster
also excludes NEW1. The requested fallback therefore accepts only a nonempty
`events.jsonl` with no `run_finished`/`terminal` event and modification age
**0..600 seconds inclusive**, and shows “events updated N min ago”. A classified
live process bound to that exact run directory can establish liveness beyond
this age limit; a terminal event always excludes the run.

Live capture targets now use the tmux session form `=NAME:`. A failed named
session's reason appears once in its card; an unlisted failure appears once in
Running now. Failed observation never marks a builder finished. Estimate text
now says “about X-Y min left (estimate made H:MM PM)”.

Fixture correction: the first host RED used a slash-named Bash function that
cannot be exported; the corrected fixture sources the script inside its own
Bash subprocess. The first GREEN also revealed that the shared detector rejects
script source paths under temporary roots. Its positive fixture now names the
actual tools script while retaining temporary run data. Clean renewed REDs
against `before_q2/` precede the final GREEN; these were fixture corrections,
with the production detector left unchanged.

The new host validator (`check_q2_host_live.py`) compares the throwaway capture
against saved `tmux -L default list-sessions` and full ps probes, uses the same
shared detector, and independently checks the event-age fallback. It fails for
an unavailable session that exists and for every reported run outside the live
set. It never starts anything on the default server. The runner still owns only
its throwaway q1check server, records every command's output/exit code, and
refuses to overwrite an existing `host_attempt2/`. New receipts include
`default_sessions.txt/.exit`, `experiment_inventory.txt/.exit` and
`queue_live_checks.txt/.exit`, beside all earlier host checks.

Real-source sandbox renders explicitly show unavailable tmux/process observation
in this sandbox; those renders are not host liveness acceptance. No live
`dashboard` session was changed and no process was started or killed beyond
fixture subprocesses. No .venv, science/model/GPU execution, commits, pushes,
staging, MB42 backup changes, or program-state changes occurred.

MAESTRO host command:

```bash
bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh'
```

| Changed source | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `tools/dashboard_queue.py` | `7cb9132ab9809e5b3dd5660e36d6d3b299819f6f55813d8aaecf5129b007d5b5` | `f2704b90ce2beb20df7e6ca4fc605f3cf91d05b15691779f0495b2185b69241c` |
| `tools/test_dashboard_queue.py` | `aa5792d8acf1207f9b4ae71bd3d7265670687839603c2ebb2ceb64e29815eecb` | `e3433d43f9e0b8cdd877b835ce396e814c020e8f64f5e481282aaff43f6cd762` |
| `results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh` | `0ca18ffd5be230c2d3f4f5dc793771829927c544a7b5519e2ed27585d36e3f0e` | `f16577ef1d26e0a617e85d20282ab9d46b70c2c7e3c0c32fe724c0f5894f1844` |
| `results/dashboard_queue_build_20261011T014430Z/check_q2_host_live.py` | `new file` | `a192f0bc796b57b81ecc852067d322fdac3e2f448855876aab3723cb665a24f7` |

The README's before hash is `fc340d38b8d6cd7e45f3e7a5cb25a332b5934efa3fff55ce825eb6f568f47c66`; its final after hash is recorded in
`q2_after_sha256.json` (outside this self-referential document). That manifest
also records the context-save receipt and all final source hashes. The six
protected files are listed in `q2_protected_sha256.json` and remained unchanged.
Full working/staged status is saved in `q2_status_before/after.log` and
`q2_staged_before/after.log`; concurrent work belongs to its respective owners.

Context-save: `q2_context_saved.md` records decisions, verification, fixture
lessons, SHA-256s, and the single next host step inside the authorized receipt
scope; no global memory file was edited.

Binding operator context directive (2026-10-10): watch “Context N% left”. Start a new piece of work only at >=60% left. At <=40% left, or on any “Context compacted”, stop starting work, append a handoff to the receipt README with done/half-done, exact paths, SHA-256s, test state and a single next step, and reply “Q2 HANDOFF”. Restate this directive in every handoff.


## Q3 round

Status: **QUEUE TAB FIT READY FOR MAESTRO RUN**. Sandbox: **40/40 queue
GREEN**, including all original 24 tests and 16 Q3 regressions, plus **27/27
shared detector GREEN**; zero errors/skips. Native host acceptance remains
**UNRUN**, and `host_attempt3/` remains absent and reserved for MAESTRO.

MAESTRO resolved the launch contract: `-B` applies to tests and renders;
the private tab must launch exactly like `tools/dashboard_queue_tab.sh`,
`/usr/bin/python3 '<ROOT>/tools/dashboard_queue.py'`, without `-B`.
The tightened host test first failed on the prior `-B` launch, then passed
after that one command was corrected. The GPU gate and exemption assertion
remain unchanged. The runner still exports PYTHONDONTWRITEBYTECODE=1.

Before editing, `tools/dashboard_queue.py`, `tools/test_dashboard_queue.py` and
this README were copied to `before_q3/`; `q3_before_sha256.json` pins them.
The original 24-test source is retained verbatim before the appended Q3 classes.
The original host runner and host attempts 1/2 were preserved. `host_attempt3/`
remains absent and reserved for a real host execution.

| Evidence | Result | Receipt |
| --- | --- | --- |
| Unmodified Q2 baseline | 24 tests, 24 PASS; exit 0 | `q3_baseline.log/.exit` |
| Q3 RED on current Q2 before implementation | 16 tests, all 16 FAIL; 22 failed assertions including subtests; zero errors/skips; exit 1 | `q3_red.log/.exit`, `q3_tests_before_fix.py` |
| Strengthened pressure fixtures, reconfirmed on saved Q2 | 16 tests, all 16 FAIL; 22 failed assertions; zero errors/skips; exit 1 | `q3_red_confirmed.log/.exit`, `q3_tests_before_fix_v2.py` |
| First GREEN attempt | 38 PASS, one failure and one error caused by fixtures allowing full lower-priority cards to fit | `q3_green_attempt1.log/.exit` |
| Final queue GREEN after exact launch correction | 40 tests, 40 PASS; zero errors/skips; exit 0 | `q3_green_final.log/.exit` |
| Current shared detector suite | 27 tests, 27 PASS; zero errors/skips; exit 0 | `q3_shared_detector_green.log/.exit` |
| Python and shell checks | Python 3.9.6; both Python files parse as 3.9; Bash syntax and diff whitespace PASS | `q3_python_version`, `q3_shell_syntax`, `q3_diff_check` `.log/.exit` pairs |
| Real-source sandbox renders | 40x30: 28 rows, maximum 40 characters; 100x45: 45 rows, maximum 100 characters | `q3_sandbox_render_40_30` and `_100_45` `.txt/.stderr/.exit`; `q3_render_checks.json/.exit` |
| Protected sources and existing tests | Six protected files unchanged; existing tests unchanged; staged state unchanged | `q3_protected_sha256.json`, `q3_scope_check.log/.exit` |
| Historical GPU launch conflict | Original CLT dashboard command exempt; prior `-B` launch produced a blocker, now resolved by MAESTRO | `q3_gate_launch_probe.json/.exit` |
| Tightened exact-launch regression RED | 1 test, 1 FAIL, no errors/skips; before host command correction | `q3_launch_red.log/.exit`, `q3_tests_launch_before_fix.py` |
| Tightened exact-launch regression GREEN | 1 test, 1 PASS; unchanged gate exempts the actual launch form | `q3_launch_green.log/.exit`, `q3_gate_launch_resolved.json/.exit` |
| Final shell syntax | PASS; exit 0 | `q3_shell_syntax_final.log/.exit` |

Test list (the appended `Q3Regressions` and `Q3HostRegressions` classes):

1. `test_q3_01`: crowded 40x30, 40x45 and 100x45 frames fit real height and character/cell width.
2. `test_q3_02`: time, all counts, edit age, complete Needs you titles and >3-hour warning survive crowding.
3. `test_q3_03`: running, needs_you and in_review cards keep complete details ahead of lower states; original item numbers remain.
4. `test_q3_04`: remaining cards become single numbered state/title rows; last row reports the exact omitted count; an exact compact fit needs no footer.
5. `test_q3_05`: middle dot, em dash, accented, wide and combining characters clip without splitting encoded bytes.
6. `test_q3_06`: only BUSY/WAITING builders appear under Running now; finished/idle names share a wrapped Idle builder windows line; unknown observations are separate diagnostics.
7. `test_q3_07`: the actual redraw loop queries both dimensions again after resize from 40x30 to 100x45.
8. `test_q3_08`: a full 30-row redraw has no trailing newline to scroll away its header.
9. `test_q3_09`: --once 40 30, --once 100 45 and legacy --once 40 work with height limits.
10. `test_q3_10`: missing, malformed and empty queues remain visible within height despite crowded live observations.
11. `test_q3_host_01`: fresh host_attempt3 only, both sized renders, saved exit codes and 8 seconds of waits.
12. `test_q3_host_02`: private q3check at 40x30 with the real tab's exact command and unchanged GPU exemption, visible-pane capture without scrollback, exactly one owned cleanup and read-only default inventory.
13. `test_q3_host_03`: a short scrolled capture lacking the Work queue header fails.
14. `test_q3_host_04`: a header-visible capture over 30 rows fails.
15. `test_q3_host_05`: existing q3check or host_attempt3 is refused; a failed start never triggers kill-server.
16. `test_q3_host_06`: own-PID GPU blockers fail the exemption check; unrelated blockers are recorded without killing their processes.

The renderer reserves the header and the existing Needs you title block, then
budgets live observations and full cards ordered running / needs_you / in_review.
When the next card cannot fit, it and all following items collapse to one line;
the remaining item count uses the last row when necessary. Unbounded pure
`render(..., width)` snapshots keep original card order; the live loop and both
CLI forms always pass a height. Optional live detail overflow is counted separately.
A window shorter than the mandatory header/Needs you block plus its item footer
raises a clear ValueError: that physical limit cannot satisfy both full attention
text and bounded output. No mandatory text is silently cut to fit such a window.

Every line fits by Python character count and terminal cell count. The specified
`+K more items (taller window shows more)` sentence is 41 characters for two-digit
K, so its tail is character-clipped at width 40. At 100 columns it is complete.
The two pressure-fixture corrections increased input size and preserved every
assertion; renewed RED against saved Q2 preceded the final GREEN.

### Q3 completion and MAESTRO host step

Done: renderer and CLI changes in `tools/dashboard_queue.py`; 16 new regressions
in `tools/test_dashboard_queue.py`; saved behavioral RED / GREEN and source-size
receipts; proposed `run_host_checks_q3.sh` with guarded host_attempt3, private
40x30 q3check, visible capture after 2+6 seconds, header/row validation, inherited
Q2 liveness validation and own-PID GPU exemption check. Native tmux acceptance is
UNRUN. Sandbox fixtures never started or killed a real tmux server. No live
`dashboard` mutation, science/model/GPU work, commits, pushes or writing git
commands occurred. MAESTRO's program state and MB43's backup files were not edited.

Launch conflict resolved: the throwaway tab now uses exactly
`/usr/bin/python3 '<ROOT>/tools/dashboard_queue.py'`. Tests and sized renders
retain `/usr/bin/python3 -B`. `q3_launch_red.log/.exit` captures the tightened
assertion's failure before this command change, and `q3_launch_green.log/.exit`
captures its PASS. `q3_gate_launch_resolved.json/.exit` confirms the canonical
CLT process command is exempt under the unchanged gate, with the old `-B` form
still correctly treated as a blocker. The six protected hashes remain pinned.

Before the resolution edits, the current test file, host runner and README were
copied into `before_q3/launch_resolution/`; hashes are saved in
`q3_resolution_before_sha256.json`. Earlier RED/GREEN, handoff and launch-conflict
receipts remain historical evidence. `q3_context_ready.md` records the final
context-save state; the older `q3_context_saved.md` is superseded for task status.

Single next step: **MAESTRO runs the prepared host command**. It will refuse
an existing host_attempt3 or q3check server, wait 8 seconds, capture only the
visible pane, require its first nonblank line to start Work queue and at most
30 lines, verify GPU exemption, and kill only the private server it started.

```bash
bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_queue_build_20261011T014430Z/run_host_checks_q3.sh'
```

| Changed source | Before SHA-256 | Current SHA-256 |
| --- | --- | --- |
| `tools/dashboard_queue.py` | `f2704b90ce2beb20df7e6ca4fc605f3cf91d05b15691779f0495b2185b69241c` | `2d200620dd6a7d02283b80619192d2d7b03d38b11a9485b15d6f201ab6cfa85f` |
| `tools/test_dashboard_queue.py` | `e3433d43f9e0b8cdd877b835ce396e814c020e8f64f5e481282aaff43f6cd762` | `5258f3d4fa66ed12235a1c8e407d4e1122eed26ae034d217f3bf19a67b70244a` |
| `results/dashboard_queue_build_20261011T014430Z/run_host_checks_q3.sh` | `new file` | `5cc9703cf5e1b382a42bfa20c223c5a247473258de6cb40bc5f48f890e0bdf8c` |

README before SHA-256: `ad3364da36f7c8c4be90f1e7ed74e9d241dd276e4aa02756cb573cc8f88bc231`.
Final README / ready-context / source hashes live in `q3_final_sha256.json` to
avoid self-reference. `q3_after_sha256.json` pins the earlier handoff state.

CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch “Context N% left”.
Start a new piece of work only at >=60% left. At <=40% left, or on any
“Context compacted”, stop starting work, append a handoff to this README with
done/half-done, exact paths, SHA-256s, test state and a single next step, and reply
“Q3 HANDOFF”. Restate this directive in every handoff, including every team session.
