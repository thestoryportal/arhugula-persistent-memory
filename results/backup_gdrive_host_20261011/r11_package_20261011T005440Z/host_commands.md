# MAESTRO hostfix1 evidence commands — all fresh actions UNRUN

Run from a host terminal at **niceness 0**, using `/usr/bin/python3` 3.9.6. Run each command separately, inspect its saved outputs and pass rule, then advance. The script takes exactly one action; it does not execute activation, contact Drive, install jobs, or run a remote-content check. Every underlying test uses local fixtures. Native tests begin only after the saved non-native E GREEN. Each label is fresh and fails on reuse; do not overwrite any earlier receipt. These commands are for MAESTRO, not the sandbox.

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
R="$PWD/results/backup_gdrive_host_20261011/r11_package_20261011T005440Z"
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" e-red
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" e-green
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" coverage
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" fixture
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" frozen
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" package
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" check-red
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" check-green
LLMDB_ROOT=$PWD /bin/sh "$R/host_commands.sh" pins
```

All previous r11 labels were used by MAESTRO; their native results are preserved in this receipt and do not accept the corrected bytes. These nine actions, all preflights, the pins capture and frozen inner r11_hostfix1_green_all use fresh r11_hostfix1_* labels. Every target was checked absent before dispatch. The additional MB43 document checks run separately from the 55-test package mode.

Evidence stays under R; HOME/fixtures/TMPDIR are allocated in a fresh owned /private/tmp/drive_r11_<label>_*/ runtime. Before coverage or fixture tests, saved df -P observations resolve source and fixture mount points; diskutil info -plist on those mount points must expose APFSPhysicalStores with disjoint physical whole-disk identities. Unknown identities or any shared physical disk mean STOP. ParentWholeDisk alone is insufficient. MAESTRO31 observed memit disk6 over disk4s3, and /System/Volumes/Data disk3 over disk0s2; /private/tmp itself is not a diskutil mount point. A different partition of physical disk4 is rejected. The live runtime placement/config positive control is host UNRUN on the corrected code. Save placement_source_df.*, placement_fixture_df.*, both placement_*_diskutil_info.* files and fixture_placement_positive_control.json; the latter must show disjoint physical identities before local rclone dispatch.

The per-action preflight uses capture.py, saves both streams and actual exit in `commands/r11_hostfix1_preflight_<action>/`, and refuses the wrong interpreter/version, niceness or any inherited RCLONE_* variable. Fix the launch environment before a new labeled run; do not bypass the refusal. Every runner saves its own command.json, source/test hashes, full child outputs, process clearance and byte-identical before/after real inventories. `/bin/ps` availability is measured by the outer runner; the frozen inner runner's hard-coded ps prose is not host observation evidence.

| Action | Exact underlying command after preflight | Acceptance and saved sink |
|---|---|---|
| e-red | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_e_red --mode e-red` | Outer exit **1**, 1 test, exactly 2 absent-parent UNSET failures, no errors/skips; sentinel-parent cases pass. `r11_hostfix1_e_red/test.log`, result.json. Uses before/tools/test_backup_gdrive_addendum_red_valid.py, never current native bytes. |
| e-green | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_e_green --mode e-green` | Exit 0; 4 tests pass, 0 failures/errors/skips. Includes shared-transform probe and all 3 Launcher cases, including native fixture receipt/counter/state assertions. `r11_hostfix1_e_green/test.log`, result.json. |
| coverage | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_py39_coverage --mode coverage` | Exit 0; exactly **22 run, 22 pass, 0 skips/failures/errors**, selection 10 base + 9 Heartbeat + 3 Launcher. BACKUP_TEST_NO_RCLONE is **unset**. HOME/config positive controls succeed and listremotes is empty. `r11_hostfix1_py39_coverage/`. |
| fixture | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_local_check --mode fixture` | Exit 0; 4 accepted cases in `r11_hostfix1_local_check/local_check/result.json`: same-size alpha.txt corruption produces verifier FAIL naming alpha.txt; excluded-only difference, --links symlink, and clean copy produce PASS. Real rclone remains local→local, HOME isolated. Preserve all raw per-case check exits, logs and reports. |
| frozen | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_green --mode frozen` | Outer exit 0 and child frozen result **155 run, 0 failures/errors, 14 real-rclone skips**, every owned group exited. Dispatches unchanged frozen `run_suite.py r11_hostfix1_green_all all`; inner sink is `results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/r11_hostfix1_green_all/`; outer sink `R/r11_hostfix1_green/` supplies real inventories and measured ps. All 14 skips remain UNVERIFIED; separate 22 coverage closes the activation dependencies. |
| package | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_package_green --mode package` | Exit 0; 55 package/helper tests pass, 0 skips/errors/failures. `r11_hostfix1_package_green/driver.stderr.txt`, result.json. |
| check-red | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_check_v1_red --mode check-red` | Child exit **1**, wrapper exit **0** means expected RED. `driver.stdout.txt` flags PIPE, GITHUB_MARKER, INTEGRITY, INTERPRETER, CONTENT_MODE, FIXED_GENERATION; it is not a plan-v1 PASS. |
| check-green | `/usr/bin/python3 -B "$R/run_py39_coverage.py" r11_hostfix1_check_v2_green --mode check-green` | Child and wrapper exits 0; `driver.stdout.txt` is `PASS []`. No activation commands run. |
| pins | `/usr/bin/shasum -a 256 -c "$R/pins_v2.sha256"` through capture.py | Exit 0; all final pin entries report OK. `commands/r11_hostfix1_pins/{stdout.txt,stderr.txt,exit_code.txt,command.json}`. Final count is in README and pins_v2.json. |

For every runner action, including expected E RED, require real_inventory_identical=true, all_owned_groups_exited=true and host ps_observation.available=true. Failures or mismatches are STOP; keep complete receipts and return them to MAESTRO. Never convert a skip, containment cleanup or unavailable observation into acceptance.

CONTEXT DIRECTIVE: start new work only at >=60% context left. At <=40% or any compaction, stop starting work, append done/in-flight paths, hashes, test state and a single next step to this receipt's README, and send MB43 HANDOFF. On HOLD PYTHON finish the current command and start no Python/tests until RESUME PYTHON.
