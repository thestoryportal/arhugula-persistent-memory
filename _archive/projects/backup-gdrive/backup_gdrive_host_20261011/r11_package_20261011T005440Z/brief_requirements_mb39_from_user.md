# Verbatim brief requirements and method excerpt for handoff line references
Source: MAESTRO's original brief supplied in the MB40 user message. This indexed excerpt does not replace that message's context, negative example, boundaries or CONTEXT DIRECTIVE.

<requirements>
Each numbered criterion below has its own test or check. Write those tests first, then the code and documents. "Plan v2" means activation_plan_v2.md in your receipt dir. It is written for the release-dir deployment, and it is never executed by you.

Item 2: the full-content check. You write the plan and a verifier. Nothing runs against the real remote.
2.1 Plan v2 gives the exact `rclone check` command:
  - default hash mode, with no --size-only and no sampling; state whether --one-way is used and why;
  - the same filters as the sync in tools/backup_gdrive.sh:123–126 (--exclude-from, the four tmp_obj excludes, --links);
  - report files from --combined, --differ, --missing-on-dst and --error;
  - stdout, stderr and the exit code each saved to a file;
  - a follow-up --download command for any object that has no comparable hash.
  Take the flags from `/opt/homebrew/bin/rclone check --help`. In your sandbox, `rclone version` and `rclone ... --help` are the only rclone calls allowed.
2.2 verify_check.py is stdlib only and lives in the receipt dir. It reads the saved exit code, report files and log. It prints PASS only when the exit code is 0, every report file is present and complete, no missing, differing or error entries exist, and no hash went unchecked. Anything else prints FAIL with the counts. Test it first on canned fixtures: clean → PASS. Each of these → FAIL: one differing file; one file missing on the destination; one error or unreadable file; an unchecked-hash count above 0; a missing or truncated report; a nonzero exit with empty reports.
2.3 Host fixture, run by MAESTRO through your host runner: the 2.1 command template, local→local, on a tiny fixture tree under the isolated HOME. Expected: same-size corruption → FAIL naming the file; a difference only in an excluded path → PASS; a symlink under --links → PASS; a clean copy → PASS.
2.4 Plan v2 writes out the item's sequence: initial upload → write pause (name the included writers and the command that proves they stopped) → final catch-up sync → content check → record the checked inventory. Files changed since the first start get no waiver. "fresh backup with warnings" (S:642) never satisfies the check. A later clean completion plus a passing check is required, and retirement stays blocked until then. Budget the ~287 GB local read (time, plus the throughput you assumed) and the Drive reads. The write pause and the full check are [OPERATOR GO] rows: you write them and do not run them.

Item 3: Python 3.9 coverage, pins and erratum.
3.1 run_py39_coverage.py is a new host runner in your receipt dir. Do not edit the frozen results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py; it forces BACKUP_TEST_NO_RCLONE=1 (:23) and forbids rclone (:88). The new runner:
  - selects exactly 22 tests: the 10 in tools/test_backup_gdrive.py (:60–183), the 9 HeartbeatTest cases skipped in cmpfix_green (named in its result.json), and the 3 LauncherTest cases. It does not select ArchiveTest, and it leaves BACKUP_TEST_NO_RCLONE unset;
  - asserts /usr/bin/python3 3.9.6 and niceness 0, and refuses to run otherwise;
  - puts HOME inside the run dir, unsets RCLONE_CONFIG and XDG_CONFIG_HOME, and refuses any inherited RCLONE_* variable;
  - before any test, runs a positive control: `rclone config file` must resolve inside the fixture HOME and `rclone listremotes` must print nothing;
  - refuses any child argv that contains `gdrive:`, launchctl or /usr/bin/open;
  - clears processes per test the way run_suite.py ClearedResult (:110) does, and records whether /bin/ps was available as observed (run_suite.py:200 hard-codes "UNAVAILABLE");
  - takes a read-only real-path inventory before and after the tests, using the operator's real HOME outside the isolated env. It covers the roots in results/backup_gdrive_mb25_20261010T202206Z/real_path_listing.py:9–10, plus ~/Library/Application Support/memit-gdrive-backup and /Library/Logs/memit-gdrive-backup*;
  - writes command.json with argv, cwd, interpreter, niceness, env, and the SHA-256 of every source and test file.
  Acceptance (host): 22 run, 22 pass, 0 skips, failures or errors; all owned process groups exited; the before and after inventories are byte-identical.
3.2 Pin set v2: pins_v2.sha256 (shasum -c format) plus pins_v2.json.
  - pins_v2.json sets `supersedes` to the old pin file's path and SHA-256. The old file stays untouched.
  - It records the test file's hash lineage: 766509ab → b764938 → 6eba5860 → f9547a3f → final.
  - The pins cover every deployment input: the seven production files, both test files, the frozen run_suite.py, your runner, verifier and plan checker, and plan v2.
  - The built bundle cannot be pinned before it is built, so plan v2 defines the build-time step that records the bundle's manifest and does the full source comparison.
  Acceptance: `shasum -a 256 -c pins_v2.sha256` reports all OK on the final bytes, with the count stated.
3.3 Erratum file. a091aec's commit note says "the poll loop has no sleep (busy-wait <=3 s)", but the loop sleeps 10 ms (`time.sleep(0.01)`, T:441 in the current bytes). Also record Astra's ruling on T:428. Cite current file:line for both.

Item 4: recovery and operations. These are rows in plan v2.
4.1 Decide again between fresh history and recovery, from a new read-only inventory (the receipt was moved; see context). Read S's recover path (S:285–443). For an empty log root, state which command applies, its exact expected output and post-state, and the operator's confirmation that no issued history was lost. Second branch: if any evidence is present, STOP and decide again with the operator.
4.2 Every status and recover row runs /usr/bin/python3 against the deployed release's status tool, with its hash checked against the pin. No .venv, and no copy from a checkout.
4.3 Read row 3.4 strictly before end+13 h (S:604). During the upload, check the owner, child and progress separately from status (S:528–529).
4.4 Generation-2 transfer failure: diagnose, clear the lock and processes, then re-open, with the operator's approval, as the next generation observed. Recovery is only for damaged ordering history. Hard-code no generation number; expected values refer to the observed successor.
4.5 The `caffeinate -i -s open -W -g` wrapper, with `pmset -g assertions` captured to confirm the assertions.
4.6 Immediately before 3.1, check again for native-test fixture processes and the eight PIDs. Any found → STOP.
4.7 Retirement: bootout + disable, only after the item-2 checkpoint and a fresh scheduled-path completion. Verify the disabled state (`launchctl print-disabled gui/<UID>`) and that no old sync process survives.

Item 5: the checklist.
5.1 check_plan.py is stdlib only and written test-first.
  - RED on plan v1. It must flag: P:67 and P:108 (pipes hide exit codes), P:81 (PR creation without a marker), P:87 (decompile greps used as the integrity check), P:94 (recover under .venv), P:108 (--size-only), and hard-coded generation expectations (P:104–117).
  - GREEN on plan v2. Every command saves its complete stdout/stderr and its own exit code to files in R; no pipeline masks a failure; every write, launch or GitHub row carries a marker; there is no --size-only, no .venv, no decompile grep and no hard-coded generation.
5.2 Plan v2 pins the builder, stage script, plist, excludes and built bundle. Integrity is a full cmp of the rendered source against the decompile, the way build_gdrive_applet.sh does it. Plan v2 also verifies the new job's enabled state, and documents when it first runs after login, given RunAtLoad false and StartInterval 21600 (plist:17–20).
5.3 Plan v2 quotes the r10 required order verbatim and maps each of its steps to it. Keep every existing GO and stop condition (P:147–165), updated for the release-dir deployment, and record that the receipt was preserved at c1a06ea.

Item E: the HOME-export test leak, test-first.
Background: a dashboard builder diagnosed this from source and never ran it (results/dashboard_audit_20261010/fix_20261010T234721Z/README.md:95–111, uncommitted). The failing-wrapper test (T:2486) injects `HOME=<applet-home>` without export (T:2508). The sibling native fixture does export (T:2339). Host evidence weakens the claimed path: cmpfix_green ran this test natively with OK (test.log:80), and the real log sink did not change. The leak is real only when the shell's parent env has no HOME; Perl then sees no HOME at all.
E.1 RED first, non-native. Write a new test that applies the same transform the native test uses to generationShell and receiptShell. Move the transform into one helper that both tests call; do not copy it. In the new test, replace the Perl body with the probe `/usr/bin/perl -e 'print $ENV{HOME} // "UNSET"'`, and run it via `/bin/sh -c` in two cases: (a) the parent env has no HOME; (b) the parent HOME is a sentinel temp dir. Required: the probe prints the fixture HOME in both cases. Keep the RED log; case (a) is expected to fail. If nothing fails on the current bytes, STOP E and report.
E.2 GREEN: in the failing-wrapper test, inject `HOME=<fixture>\nexport HOME\n` (the T:2339 pattern).
E.3 Native positive control: after the osascript run in the failing-wrapper test, assert that the receipt and launch-state artifacts exist under the fixture applet-home.
E.4 No native run happens before the fix. Native runs happen on the host, only after GREEN, inside a run whose real-path inventory (the 3.1 roots) is identical before and after.
</requirements>

<method>
- Write the test list from the numbered criteria first, then the tests, then the code and documents. Copy every file you will change into before/ before changing it.
- Receipt dir: results/backup_gdrive_host_20261011/r11_package_<UTC>/. It holds:
  - README.md: a table per criterion (test → RED → GREEN); every skip; the before/after SHA-256 of every changed file; and a section for Astra r11 that maps r10 items 1–5 and E to evidence file:line;
  - activation_plan_v2.md, pins_v2.sha256, pins_v2.json and the erratum;
  - the runners, verify_check.py and check_plan.py;
  - RED/GREEN logs with exit codes, and a command.json per run.
  List every file over 1 MB with its size and SHA-256 in bulk_not_in_git_sha256.json. Disk budget: under 200 MB.
- In your sandbox, run every non-native test yourself with /usr/bin/python3, BACKUP_TEST_NO_RCLONE=1 and an isolated HOME, along with the verify_check.py and check_plan.py tests. The sandbox denies /bin/ps, osascript, osacompile and native rclone use, and sandbox GREEN is not host GREEN.
- For everything the sandbox cannot run, write the exact host commands MAESTRO runs at niceness 0:
  - E RED/GREEN;
  - the 3.1 runner;
  - the 2.3 fixture;
  - the full addendum suite through the frozen run_suite.py under new labels (e.g. `r11_green all`; expect 154 + your new tests, 14 real-rclone skips, all groups exited);
  - check_plan.py RED/GREEN;
  - `shasum -a 256 -c pins_v2.sha256`.
  Do not mark host tests as passed.
</method>
