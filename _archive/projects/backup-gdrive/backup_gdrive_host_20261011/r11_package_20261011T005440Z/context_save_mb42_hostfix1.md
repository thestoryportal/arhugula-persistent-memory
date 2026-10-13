---
status: handoff-package-refresh-pending
branch: worktree-c10k-route-a
timestamp: 2026-10-11T02:12:55.684229+00:00
---

# MB42 HANDOFF — host correction GREEN; package refresh pending

## Single next step

**Finish the package refresh in this existing receipt, then provide all nine fresh host commands to MAESTRO.** The one-round code correction and focused tests are finished; no command is in flight. Do not run the existing host_commands.sh: every old r11_* label has already been used. Use the proposed fresh prefix r11_hostfix1_* for all nine actions, preflights and pins, plus the frozen inner *_all label; check that each chosen path is absent. Copy before further edits. Update the affected pins (three edited source files, plus host docs/script/plan if amended; add the new regression source), docs/README/bulk manifests, run all relevant sandbox GREENs with isolated HOME and /usr/bin/python3 -B, then final pin and README/manifests checks. The package mode now includes test_hostfix_mb42, so its expected full package count is **55** (39 existing + 16 new), subject to the actual raw GREEN. A full package run before repinning will fail PinsTest correctly. No further implementation change is known to be needed.

Pins_v2 still describe the pre-host-correction bytes; they are **STALE**, not final GREEN. Full package/sandbox/checker reruns, fresh host dispatch labels, activation-plan semantics note, bulk refresh and final package seal remain half-done. Ready token forbidden until complete. Preserve every old host/native/raw log and previous manifests; use new receipts/labels rather than overwriting. The original host run's results are immutable evidence, not GREEN on the new code.

## Done / exact evidence

- Before edits, all 27 pins and all 385 MB42 manifest entries passed under commands/mb42_hostfix1_entry_pins and commands/mb42_hostfix1_entry_manifest. Existing-file copies are before/mb42_hostfix1_<filename>; the baseline/host-evidence hashes are mb42_hostfix1_entry_snapshot.json.
- Root-cause RED: commands/mb42_hostfix1_causes_red/stderr.txt:1-79, 11 tests, **5 behavioral failures, 0 errors**, exit 1. Four failures replay the actual host DEBUG --error/error.txt contamination; the fifth executes the actual runner and observes HOME under /Volumes/memit.
- Complete RED: commands/mb42_hostfix1_full_red/stderr.txt:1-111, **16 run, 9 failures, 1 error**, exit 1. Four added failures are missing physical-proof helpers; the error is the real run_local_check.py receipt-vs-HOME containment rejection. Do not describe all ten as behavioral assertion failures.
- Focused GREEN: commands/mb42_hostfix1_focused_green/stderr.txt:1-21, **16 pass**, no failures/errors/skips, exit 0. Replays clean/excluded/symlink PASS, corruption FAIL naming alpha.txt; NOTICE-only PASS; true severity/read/unchecked errors still FAIL; actual sandbox runner placement; local-check evidence/content separation; recorded host APFS disjoint/shared/unknown identities and actual df mount resolution.
- Existing controls GREEN: commands/mb42_hostfix1_existing_controls_green/stderr.txt:1-25, **20 pass**, no failures/errors/skips, exit 0: all 11 verifier controls, eight checker tests and exact check template.
- Seven production files, both base/addendum test sources, frozen runner and old pin set remain byte-identical. mb42_hostfix1_stop_state.json records protected hashes/current source hashes and pending state. All failed host coverage/fixture receipts and MAESTRO's native diskutil probe were rehashed and preserved.
- Current allocation by file lengths is 31836992 bytes (<200 MB); new host/bulk files require the pending bulk manifest refresh. No native/real-rclone/Drive/activation command, real HOME write, unowned kill, deletion or git mutation was executed.

## Current fix and flush caveats

run_py39_coverage.py now keeps evidence in this receipt and allocates a fresh owned /private/tmp/drive_r11_<label>_*/ runtime containing HOME/fixtures/TMPDIR. Host coverage and fixture modes first run saved df -P observations, resolve each path to its mount point, then call diskutil info -plist on the mount points. APFSPhysicalStores are reduced to physical whole disks; unknown or intersecting sets STOP. ParentWholeDisk alone is deliberately insufficient: source memit is virtual disk6 over physical disk4s3; Data is virtual disk3 over physical disk0s2. Another external partition such as disk4s1 must be refused. The current parser requires evidenced APFS physical stores and fails closed for unsupported/missing identities.

MAESTRO's authoritative host probe is host_diskutil_probe_maestro31/README.txt:1-5 plus the three successful plists. /private/tmp is not a diskutil mount point (rc 1); df resolves it to /System/Volumes/Data. Probe hashes are mb42_hostfix1_diskutil_inputs.json. Sandbox diskutil was actually probed and cannot use DiskManagement; actual new runtime physical positive control is still **host UNRUN**, despite replayed native data passing.

verify_check.py now matches severity only at a log-line prefix, preserving ERROR/CRITICAL/FATAL and read/unchecked/report failures. The three recorded clean host cases falsely failed because the DEBUG argv included --error and error.txt; removing only that line made the missing-config NOTICE pass before the fix. The raw logs/reports are never altered; tests replay them in owned /private/tmp fixtures.

run_local_check.py now validates its output below this receipt and isolated HOME below /private/tmp, so the separate content/evidence roots are legal. Production's same-source-volume destination guard is untouched. .deleted/rclone.pid/timeout/start-success failures occur after the refused dispatch; no separate policy fix was made. Their shared cause is **I-INFER** until the fresh exact 22 host run passes.

The original host run at maestro_host_20261011T015745Z/rcs.txt passed E RED as expected, E GREEN 4/4, frozen 155/0 failures/14 skips, package/checker/pins; coverage failed 22 run/13 failures and fixture failed three clean cases. These are pre-fix host results. All nine actions must be rerun under fresh labels after the package refresh, including the seven previously passing actions.

## Current source identities

| File | Before SHA-256 | Current SHA-256 |
|---|---|---|
| run_py39_coverage.py | d5a7094de35b528d423c47962a66bde9ea52b69f538007c28c5c49223a65965b | f66dec5193003aeec02ce72a22760597c1beb685f00b8a7580c73aceec4bf41b |
| verify_check.py | a7126bd62cf127c757873f348db745b981fae9603246a5afff604736c8fc49e5 | 5b4748c501d3d5f416a689978a8052d3d2a3390a5d0439b313f4285ab8a1fbfc |
| run_local_check.py | d2c93d25c4d169447c08a003765f2bb1aee04e60da1a94d2fc60af75d1eb0059 | 0c9045c7635919f61ca91792c8ed756074ebb1a8fcfcabfdbd66980102131a75 |
| test_hostfix_mb42.py | ABSENT | c8f246b419009dd0bb5d13250e00fd19392e1300872e269a9e0e2284647807bf |

## Binding continuation directives

CONTEXT DIRECTIVE (binding, operator 2026-10-10): watch Context N% left. Start a new piece only at >=60% left. At <=40% or any compaction, stop starting work; append done/half-done/in-flight exact paths, SHA-256s, test state and one single next step to README, restate this directive and reply MB42 HANDOFF. MAESTRO additionally reported this session at 50% and ordered completion of the current fix/tests, then a handoff if under 45% instead of starting the full package refresh. This session stops after the completed fix/tests; no refresh is started. Every successor/team session inherits the directive.

PYTHON QUIET: HOLD PYTHON means finish the current command and start no Python/tests until RESUME PYTHON. Production/base/addendum/frozen runner/old pins are read-only. No remote rclone, native applets, launchctl, activation, real HOME writes, unowned kills or git mutation. Preserve the exact original exclusions, including all Q1 dashboard_queue/team_dashboard files/results and MAESTRO docs/program_state.json and closeout files. Unexpected protected drift → STOP. Ready token only when every authorized sandbox-runnable GREEN and package refresh passes.

## Preserved prior package report — pre-host-correction bytes

The prior report below is historical; its final-byte/readiness/pin/UNRUN claims do not describe the current host-correction state above.

