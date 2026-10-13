# MB37 dashboard live refresh — MAESTRO28

Scope: A–D dashboard repairs and read-only diagnosis of E. No commits, Git mutations,
real tmux mutations, `.venv` Python, model/GPU work, or changes to locked Drive files.
This improves observability of the F1 program; it makes no scientific finding.

Acceptance criteria frozen before implementation:

1. Team membership refreshes every 3 s in one process, removes retired builders,
   discovers the current lead and all live Codex builders, rotates overflow, and
   derives status-bar counts from that same full roster. Future builds use one pane.
2. Reload stamps include dashboard scripts and their derived local import closure,
   including lazy/package/relative/transitive imports, without executing imports.
   MathLab checks reload before each frame.
3. Science next-actions and updated date are re-read from program_state each frame;
   scoreboard narrative has an explicit source/date and cannot supply a fallback queue.
4. Exact uppercase READY/DONE reply lines end cleanly; test-count prose is not an
   error; actual errors and errors after a token remain visible. Last-run selection
   is shared with Experiment, excludes archived/mirrored logs, and never borrows
   an older outcome for a newer run.
5. Identify and propose the Drive-fixture isolation fix without editing or invoking
   any locked native/Drive test.

Before-copies: `before/tools/`; original hashes: `before.sha256`.
Protected baseline hashes: `locked_before.sha256`. Interpreter: `interpreter.txt`.
Sandbox probes: `ps_probe.*` and `tmux_probe.*`; both observation APIs were denied.
Host acceptance remains UNVERIFIED until MAESTRO runs the host runner.

RED/GREEN evidence and final file:line citations will be recorded here after checks.

Python quiet rule: after HOLD PYTHON, finish the current command and run no Python
or tests until RESUME PYTHON.

Context directive (binding, operator 2026-10-10): watch Context N% left. Start a
new piece of work only at >=60% left. At <=40% left, or on any Context compacted,
stop starting work, append a handoff here with done/half-done, exact paths,
SHA-256s, test state and next step, and reply MB37 HANDOFF. Every handoff must
restate this directive.

## MB37 HANDOFF — 2026-10-10T23:53:52Z

MAESTRO28 explicitly stopped this session after the edit in flight. No new tests,
matrix, fixes, or host-runner work started after that instruction. This is a
half-done implementation, **not acceptance or READY**. A fresh successor finishes it.

### Done / half-done per finding

- **A — verified; implementation half-done, GREEN unrun.** Original fixed-pane
  build: `before/tools/team_dashboard.sh:41-68`; per-pane argv session:
  `before/tools/dashboard_tile.py:123`; disabled rebuild:
  `before/tools/dashboard_report.py:136`. New `tools/dashboard_team.py:12` reads
  sessions and the current discovered lead, filters to lead plus live Codex,
  captures each screen/title once, and `:23` composes/paginates tiles and prunes
  retired state. Its loop `:56` refreshes every 3 s and `:69` publishes one
  window metadata option `@team_counts` from the full roster, including off-page
  builders. No runtime split/kill/respawn/rename. `tools/dashboard_bar.sh:5`
  reads that option rather than counting old pane statuses.
  `tools/team_dashboard.sh:16` creates one Team pane on a future authorized build;
  it was **never executed against real tmux**. `tools/dashboard_tile.py:85,93`
  now accepts a captured screen/title/time to avoid per-tile duplicate reads.
  `tools/dashboard_live.py:686` makes the obsolete layout supervisor a no-op;
  its old pure helpers remain for compatibility with existing tests.
- **B — verified; implementation half-done, GREEN unrun.** Original stamp:
  `before/tools/dashboard_live.py:374-375`; absent MathLab reload:
  `before/tools/dashboard_mathlab.py:263-278`. `tools/dashboard_live.py:375,394`
  derives imports via cached AST parsing and traverses repo-local package,
  relative, lazy and transitive imports without importing/executing modules.
  Stamp is max mtime over the dashboard roots and derived closure.
  `tools/dashboard_mathlab.py:270-272` now initializes/checks the reload stamp.
  Other existing loops retain their shared reload calls.
- **C — verified; implementation half-done, GREEN unrun.** Original scoreboard
  authority: `before/tools/dashboard_report.py:76,141`. The *current* scoreboard
  already differs from the audit snapshot: its `updated` is 2026-10-10 01:15 MDT,
  but it still has a manually maintained queue. Source verified directly:
  `docs/program_state.json.next_actions` is an array of strings, including
  D-C10r-rulings-17 (C10Y DEFERRED) and D-C10r-rulings-18. Both files were left
  untouched by MB37. `tools/dashboard_report.py:14,73` re-reads program state
  every render, uses its updated value, and fails visibly rather than borrowing
  a scoreboard queue. `:91` wraps/paginates all next-action text every 10 s;
  the source includes historical/superseded prose, preserved verbatim rather
  than hand-interpreted. `:103` explicitly dates the scoreboard narrative;
  scoreboard brief/results remain dated narrative. Missing narrative does not
  suppress authoritative actions. Verify readable placement and historical
  caveats in the host captures; no real visual acceptance yet.
- **D — verified; implementation half-done, GREEN unrun.** Original false alarm:
  `before/tools/dashboard_live.py:434,455`; narrow coordinator glob: `:526`;
  Experiment's broader newest source: `before/tools/dashboard_experiment.py:286`.
  `tools/dashboard_live.py:486` recognizes standalone uppercase READY/DONE tokens
  (including underscore-separated tokens), exempts errors preceding that token,
  preserves later errors, and no longer treats numeric test-count prose as an
  error. Actual FAILED-at-line-start remains an error. `:559` now supplies one
  filtered log selection to GPU state (`:565`) and Experiment
  (`tools/dashboard_experiment.py:258`); newer logs lacking a coordinator exit
  show log age plus "outcome not recorded", without inheriting an older exit.
- **E — diagnosis complete; proposed fix only, locked files untouched.**
  `tools/test_backup_gdrive_addendum.py:34` creates the `gdrive_addendum_` temp
  fixture and `:38-42` patches subprocess HOME. The leak path is
  `LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog`
  (`:2486`): `:2490` creates `failing-backup.sh`, and `:2503-2508` injects
  `HOME=<temp>/applet-home` into generationShell/receiptShell **without exporting
  HOME**. `:2514-2518` invokes native osacompile/osascript. Standard Additions
  does not inherit the test process HOME; its shell assignment is not exported
  to Perl, which can see the operator HOME and publish the fake launch receipt
  under real `~/Library/Logs/memit-gdrive-backup/`. The nearby native fixture
  explicitly documents this at `:2333` and uses `export HOME` at `:2339`.
  **Proposal for the Drive owner:** inject `HOME=<fixture>\nexport HOME\n` into
  both shell literals in the failing-wrapper test, then assert the receipt and
  generation artifacts are under the fixture HOME and verify the real sink
  remains unchanged using a host-native run with a positive control. Do not
  implement this in the dashboard successor; the Drive release is locked.
  Diagnosis is source-based; MB37 did not run the unsafe native test.

### Exact paths and SHA-256s at handoff

The authoritative manifest is `handoff.sha256` (paths relative to worktree root).
`handoff/tools/` and `handoff/tests/` preserve exact current bytes for a successor;
`before/tools/` preserves originals. Do not overwrite these snapshots.

```text
c99650e57ed82c0319977c6bc333ebf227da12ae6a6bc0b6d18a6bccad3d265f  tools/dashboard_live.py
2c56350b5503d86f87cb4972cd3035d97637bafc3582dc346b8731fbccf8a940  tools/dashboard_tile.py
40fa3ec0b4243fd7e2eca1fb7cec2a9613ee15865567fa8f1b2ae8e5e8f34613  tools/dashboard_report.py
aa7dd35cbc0b872eafc7f37e92d1a9649be46cf00e8344cc6c9343bab3c4adb7  tools/dashboard_mathlab.py
ef2578a7b86ccec6891ebb16e1c518c98b90633a8123eb28a51cdc7e3fe8bd0b  tools/dashboard_experiment.py
bd447c1fa5392f925d2a0e8c4f3eea1f4c50501e6380a6faca22405b79cd099f  tools/dashboard_bar.sh
761f0c65df0b64d9756737abe67d9a4d78e124f8da170881baa80137749e3732  tools/team_dashboard.sh
3a8c73190c31a8349293f82413c8dc2de4ce7c56da28af0fae3dec5794d4e74e  tools/dashboard_team.py
4ff711a2e7188c30a7811c9881982a3f16693ebf4c821a8a7f3ca48aa46a2da2  tests/test_dashboard_live_refresh.py
```

`locked_handoff_check.log` proves all files listed in `locked_before.sha256`
still match: locked Drive files and `tools/test_dashboard_mathlab.py` were not
edited. Existing concurrent work was preserved. No Git mutation was performed.

### Test state and exact next step

- `red.log` / `red.exit`: initial baseline, 25 tests, 23 failures and 1 harness
  error (`StringIO.fileno`). The test capture was corrected before implementation.
- `red_confirmed.log` / `red_confirmed.exit`: confirmed baseline, **25 tests,
  24 failures, zero errors**, exit 1. Failures include subtests; this is the
  unittest summary, not 24 distinct failing methods. `red.command` records the
  command; confirmed RED used the same command with a different log filename.
- **GREEN: NOT RUN. No existing-dashboard regression suite run yet. No syntax
  check, host runner, or host acceptance run yet.** Do not report passing counts.
- Observation probes: `/bin/ps` was denied (`ps_probe.stderr`, exit 126 in
  `ps_probe.exit`); tmux at `/opt/homebrew/bin/tmux` was denied
  (`tmux_probe.stderr`, `tmux_probe.exit`, exit 1). This means UNAVAILABLE, not
  GPU idle. No retries or real tmux mutations were attempted.

**First successor action, after checking for HOLD PYTHON:** verify
`handoff.sha256` against the named current files (do not treat MAESTRO HEAD
movement or MB36 changes as a STOP), read this handoff and the new tests, then
run this short system-Python command from the named worktree:

```bash
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s tests -p test_dashboard_live_refresh.py -v > results/dashboard_audit_20261010/fix_20261010T234721Z/green_first.log 2>&1
```

Save its exit code and full output before changing anything. Resolve any
failures inside the authorized dashboard/new-test scope. Then run the focused
legacy dashboard regressions using system Python: `tools.test_dashboard_live`,
`tools.test_dashboard_report`, `tools.test_dashboard_gpu_detector`,
`tools.test_dashboard_mathlab`, `tools.test_dashboard_storage` (inspect any
external side effects first; **never run the locked Drive addendum suite**).
Preserve and report pre-existing warnings/failures. New tests are entirely in
`tests/test_dashboard_live_refresh.py`; do not edit the locked MathLab test.

Next, create the still-missing receipt-local `run_host.sh LABEL red|green` and
new read-only host test file. Record per-run UTC, interpreter, source hashes,
Git identity and observation output. Use `before/tools/` for original RED code;
use current tools for GREEN; do not edit live sources to run RED. Host checks
should read real tmux membership/layout (after MAESTRO's authorized restart of
the Team tab), confirm one Team pane and roster-derived counts, capture real
Science/MathLab/Experiment output, and exercise the dependency reload using a
temporary copy/import fixture. The runner must never kill/restart/respawn/
send-keys or create synthetic real sessions. Fixture tests cover membership
transitions; host validation observes the live host honestly. The final
completion token remains `DASHBOARD FIX READY FOR MAESTRO RUN` followed by exact
host commands and RED/GREEN counts, only when builder checks are actually GREEN.

### Standing boundaries for the successor

Only `tools/dashboard_*.py`, `tools/team_dashboard.sh`, `tools/dashboard_*.sh`,
new test files, and this receipt directory may be edited. No `.venv` Python,
model/GPU/MPS/native science launches, commits, pushes, Git mutations, real tmux
layout/session mutations, tracker changes, or edits to locked Drive files / the
existing MathLab test. MB36 owns `tools/new1_dispatch.sh`,
`tools/new1_dispatch_report.py`, `tests/test_new1_dispatch.py`, and
`results/mathlab_staging/new1_recorder_*`; their edits are authorized. MAESTRO
may move HEAD by committing tracker files. HOLD PYTHON means finish the current
command and start no Python/tests until RESUME PYTHON.

The context directive is restated **verbatim**:

> CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch "Context N% left". Start a new piece of work only at >=60% left. At <=40% left, or on any "Context compacted", stop starting work, append a handoff to your README (done / half-done, exact paths, SHA-256s, test state, next step), and reply "MB37 HANDOFF". Restate this directive in any handoff.

MAESTRO28's stop instruction is also preserved verbatim:

> MAESTRO28 context note: you are near 45% left. Finish the edit you are on, then START NO NEW STEP (no new test matrix, no new fix). Save whatever RED/GREEN output you already have, append a handoff to your receipt README (done / half-done per finding A–E, exact paths, SHA-256s, test state, exact next step, and the context directive verbatim), then reply "MB37 HANDOFF". A fresh successor finishes the rest.

## MB38 continuation — initial verification and host-test criteria

Worktree/branch verified as the named worktree and `worktree-c10k-route-a`.
`handoff_mb38_check.log` / `.exit`: all nine handoff hashes match, exit 0.
Before any source edit, `green_first.log` / `.exit`: **25 tests, OK, exit 0**.
`legacy_first.log` / `.exit`: the five specified legacy suites, **167 tests,
OK, exit 0**, no warnings emitted in this run. Storage's `FIXTURES` constant
was redirected in memory to a fresh `/private/tmp/mb38_legacy_*` root and its
optional receipt writer disabled; existing test files were not edited. Only
fixture launchers used fake tmux. The MathLab CLI checks only rendered recorded
state. The locked Drive addendum suite was not imported or run.

Frozen host-runner criteria before writing it:

1. `run_host.sh LABEL red|green` rejects invalid input before any observation;
   each accepted invocation creates a fresh receipt with UTC, interpreter,
   Git identity, source hashes, raw observation output and explicit exits.
2. RED overlays `before/tools/` onto copies of unchanged dashboard sources,
   excludes the new Team renderer, and runs the corrected regression test
   against those copies. GREEN uses current copies. Live sources and the
   `before/` and `handoff/` snapshots are never altered.
3. Real tmux calls are read-only. Check one Team pane after MAESTRO's restart,
   capture every live dashboard pane twice, and compare the Team's rendered
   roster/counts with its own published status-bar metadata. Observe actual
   Science/MathLab/Experiment panes and save selected-source renders from real
   recorded state. No fixture session, layout mutation or send-keys is allowed.
4. Record the real process inventory. Denied/nonzero/empty observations fail
   visibly; they cannot become an idle/PASS claim.
5. Exercise actual dependency-driven `execv` in an isolated copy using a
   temporary imported helper; verify GREEN reloads and original RED misses it.
6. Fixture tests prove source selection, observation failures, mutation
   rejection and the reload control before handing the runner to MAESTRO.

Finding E remains exactly the diagnosis/proposal in MB37's handoff above; no
Drive implementation or native test is authorized in this continuation.

## MB38 final builder report — ready for MAESTRO's host run

**Builder verification GREEN; live host acceptance UNVERIFIED.** MB38 resumed
MB37's existing implementation. No dashboard production bytes needed another
edit: all nine entries in `handoff.sha256` still match. MB38 added only
`tests/test_dashboard_live_host.py`, `tests/test_dashboard_host_runner.py` and
files in this receipt. No commits, Git mutations, tmux/session/layout mutations,
`.venv` Python, model/GPU/native science runs or locked Drive tests were performed.
Read-only Git status used `GIT_OPTIONAL_LOCKS=0`; concurrent work was preserved.

### A–D implementation and acceptance evidence

| Finding | Current implementation, file:line | Builder evidence |
| --- | --- | --- |
| A: fixed retired-session Team panes | `tools/dashboard_team.py:12` re-lists the live roster and discovers the lead; `:23` composes/paginates tiles and prunes retired state; `:56` refreshes every 3 s; `:69` publishes full-roster counts. `tools/team_dashboard.sh:16` builds one future Team pane. `tools/dashboard_bar.sh:5` reads the same counts. `tools/dashboard_live.py:686` disables runtime layout rebuilding. | Membership replacement, changing lead, overflow, full-roster counts, denied inventory, fake future build and fake status-bar tests pass. No actual Team rebuild was executed. |
| B: missing dependency reloads | `tools/dashboard_live.py:375` parses imports without executing them; `:394` derives the repo-local package/relative/lazy/transitive closure. `tools/dashboard_mathlab.py:270` initializes the stamp and `:272` checks before every frame. | Closure/cycle/unrelated-source controls and the MathLab-loop test pass. An actual `execv` in an isolated helper fixture succeeds with current code and misses the edit with original code. |
| C: stale Science queue/date | `tools/dashboard_report.py:14` names program state; `:73` re-reads it each frame; `:91` renders/paginates its next-actions; `:103` dates and labels scoreboard narrative. | Frame-to-frame program replacement, missing/broken authority, missing narrative and bounded rotating actions pass. Authoritative historical prose is preserved; neither JSON source was edited. The host assertion compares the visible header prefix because `updated` contains long historical text. |
| D: false alerts / old GPU outcome | `tools/dashboard_live.py:480-486` separates true errors from exact READY/DONE lines and test-count prose; `:495` considers error order. `:559` supplies the shared filtered newest-log list; `:565` derives GPU last-run metadata; `tools/dashboard_experiment.py:258` uses that same source. | Exact tokens clear preceding errors; prose does not; subsequent errors and FAILED remain visible. Nested newest logs, absent outcomes and archive/mirror exclusion pass. |

### Saved test results

All runs used system `/usr/bin/python3 -B` and saved full logs plus exit files.
The `.command` files preserve the direct builder commands.

| Receipt files | Result |
| --- | --- |
| MB37 `red_confirmed.log` / `.exit` | 25 tests, 24 failures, zero errors, exit 1; original RED preserved. Failure totals include subtests. |
| `green_first.log` / `.exit` | 25 tests, OK, exit 0, before any source change. |
| `legacy_first.log` / `.exit` | 167 tests, OK, exit 0, across all five requested legacy suites; no warnings emitted by this run. |
| `host_runner_red.log` / `.exit` | 8 tests, 8 failures, zero errors, exit 1, before the host harness existed. |
| `host_header_red.log` / `.exit` | 9 tests, 1 failure, zero errors, exit 1, before fixing the long-header assertion. |
| `green_final.log` / `.exit` | 34 tests (25 refresh + 9 host-runner fixtures), OK, exit 0. |
| `host_runner_green_final.log` / `.exit` | 9 host-runner fixtures, OK, exit 0, after the final provenance change. |
| `receipt_staged_red.log` / `.exit` | Original sources copied under this receipt: 25 tests, 24 failures, zero errors, exit 1. |
| `receipt_staged_green.log` / `.exit` | Current sources copied under this receipt: 25 tests, OK, exit 0. |
| `receipt_stage_checks.log` / `.exit` | Python AST syntax and receipt-staged RED/GREEN controls passed, exit 0. |
| `shell_syntax_final.log` / `.exit` | Each dashboard shell script, Team builder and host runner individually checked with `bash -n`, exit 0. |

**201 distinct builder tests GREEN: 34 new + 167 legacy.** Repeated runs are not
added to that total. The five host acceptance tests are not included: they are
opt-in and have not run against the host.

Original RED emits `ResourceWarning` for unclosed reads in
`before/tools/dashboard_live.py:527` and `before/tools/dashboard_report.py:76`;
those warnings remain in both staged RED logs. The earlier `/private/tmp`
staging (`staged_red.log`) additionally made the original launcher fail Git
root discovery, since that copy was outside the worktree. This is an observation
confound, not a new product defect. The subsequent `receipt_staged_red.log`
uses the same in-worktree placement as the real host runner and retains the
24-failure RED result without that Git-root failure. No warnings were hidden.

### Host runner and exact commands

`run_host.sh` validates arguments before observations, uses a fresh
`host_LABEL_PHASE_UTC_random/` namespace and invokes the opt-in read-only tests
in `tests/test_dashboard_live_host.py`. Every run saves UTC, interpreter,
copied-source/test/runner hashes, initial state-input hashes, Git root/branch/HEAD,
raw process and tmux observations with commands/exit codes, all-pane captures
twice across a refresh interval, selected-source Science/MathLab/Experiment
renders, newest-run comparison, an actual isolated helper reload, full
regression/host logs, and `run.exit`. `tests/test_dashboard_host_runner.py`
checks source selection, mutation rejection, failed/empty observation handling,
bounded-header comparison and original/current reload controls.

The runner never creates real fixture sessions or sends control input. Its
tmux boundary rejects mutation verbs. The dependency probe writes only in the
fresh receipt's `reload_fixture/`; production sources are not edited. Source
copies use `before/tools/` for RED and current tools for GREEN. Original live
pane captures still describe the host at invocation time, even during a RED
copied-source run; they are not claimed as historical screenshots.

From the named worktree, while Python is released by MAESTRO:

```bash
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /bin/bash results/dashboard_audit_20261010/fix_20261010T234721Z/run_host.sh MB38 red
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /bin/bash results/dashboard_audit_20261010/fix_20261010T234721Z/run_host.sh MB38 green
```

RED is expected to exit 1 because original source checks fail. MAESTRO performs
the already-authorized dashboard restart between RED and GREEN as appropriate;
GREEN requires the new one-pane Team view. A denied, malformed or empty required
observation fails visibly as UNAVAILABLE. Transient membership/count changes
during a capture fail with a request to rerun at a stable frame. Neither outcome
can establish idle or host acceptance. No real tmux or `/bin/ps` probe was
retried by MB38 after the inherited sandbox denials.

### E — MB37 diagnosis/proposal carried forward verbatim

- **E — diagnosis complete; proposed fix only, locked files untouched.**
  `tools/test_backup_gdrive_addendum.py:34` creates the `gdrive_addendum_` temp
  fixture and `:38-42` patches subprocess HOME. The leak path is
  `LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog`
  (`:2486`): `:2490` creates `failing-backup.sh`, and `:2503-2508` injects
  `HOME=<temp>/applet-home` into generationShell/receiptShell **without exporting
  HOME**. `:2514-2518` invokes native osacompile/osascript. Standard Additions
  does not inherit the test process HOME; its shell assignment is not exported
  to Perl, which can see the operator HOME and publish the fake launch receipt
  under real `~/Library/Logs/memit-gdrive-backup/`. The nearby native fixture
  explicitly documents this at `:2333` and uses `export HOME` at `:2339`.
  **Proposal for the Drive owner:** inject `HOME=<fixture>\nexport HOME\n` into
  both shell literals in the failing-wrapper test, then assert the receipt and
  generation artifacts are under the fixture HOME and verify the real sink
  remains unchanged using a host-native run with a positive control. Do not
  implement this in the dashboard successor; the Drive release is locked.
  Diagnosis is source-based; MB37 did not run the unsafe native test.

### Scope and completion context

`locked_mb38_check.log` / `.exit` confirms all nine protected hashes, including
the existing MathLab test and locked Drive release. `snapshots_mb38_check.log`
confirms the seven original snapshots. The final scope manifest and continuation
context are `mb38_final.sha256` and `MB38_CONTEXT.md`; `mb38_git_status.txt` and
`mb38_git_diff_stat.txt` preserve the read-only Git observation. The handoff
snapshots remain intact. No scientific or F1 finding is claimed.

The context-save procedure records state in this authorized receipt instead of
the skill's default home-directory location, under the operator's explicit
scope. Learning retained here: host assertions must allow a clipped current
`updated` prefix; RED copied launchers require in-worktree Git ancestry to avoid
confounding a product failure with a test placement failure. External host
acceptance is the remaining MAESTRO action.

CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch "Context N% left". Start
a new piece of work only at >=60% left. At <=40% left, or on any "Context
compacted", stop starting work, append a handoff to the README (done / half-done,
exact paths, SHA-256s, test state, next step), and reply "MB38 HANDOFF". Restate
this directive in any handoff.
