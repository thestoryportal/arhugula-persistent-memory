# MB44 — Drive r12 review package

Sandbox status: **GREEN, 27 tests, zero failures/errors/skips**. This is ready for
MAESTRO's host reruns and Astra r12 review; activation, live Drive checks, native
service operation, real candidate creation, remote branch/PR/CI and merge are
UNRUN. No production or backup-test file was changed. `protected_after.json`
confirms all 1,550 snapshotted protected files (including K, both backup tests,
seven production inputs and the verdicts) have identical bytes, sizes and modes.

Source worktree/branch/HEAD: `source_context.json`. Other sessions' dirty work was
preserved. Shared HEAD advanced to bc07caecaa701c1472a2079a7a5f1ca0dbd95605 during this
session; the changed paths are in source_context.json and touch none of the
1,550 protected files. Root and branch stayed unchanged; this session performed
no writing git command in the real repo. Disk budget <100 MB; this receipt, copied small evidence and synthetic
repos are small. No file in candidate scope exceeds 1,000,000 bytes. No bulk job,
remote rclone, launchctl, real-HOME write, real-repo writing git operation or
unowned process termination occurred.

## Finding 1 — backup-only candidate

`scope_allowlist.txt` enumerates every permitted candidate path literally: all
seven production files, both backup tests, chosen committed r11 inputs and the
new receipt's evidence. There are no globs. `scope_unchanged.txt` explicitly names
the four unchanged pinned inputs. The user approved this amendment in
`scope_contract_amendment.md`: exact diff equality is enforced for the remaining
paths, while unchanged inputs must equal origin/master in bytes and modes and
must have SHA-256 pins. Counting files cannot pass the gate.

| Test / counts | RED | GREEN |
|---|---|---|
| Original scope controls (6 methods) | 3 assertion failures, 0 errors/skips; group exit 1 | Superseded by 8-method final scope run; all pass, exit 0 |
| Extra staged file | Pin-only v2 adapter accepts it; assertion fails | Exact diff rejects it, underlying exit 1; test passes |
| Same count, substituted path | Adapter accepts it; assertion fails | Exact path set rejects it; test passes |
| Evidence 1,000,001 bytes | Adapter accepts it; assertion fails | Export rejects it; test passes |
| User amendment: real unchanged pin + false exception (2 new methods, 8 total) | 2 assertion failures; group/runner exit 1 | 8/8 pass; group/runner exit 0 |
| Source export, branch, pins, globs | Existing positive/negative controls held | Source commit only, backup-gdrive-r12, all held |

The scope RED adapter is explicitly synthetic: v2 had no candidate exporter and
checked deployment pins without checking a complete diff. It is preserved in
`before/` and described in `TEST_CONTRACT.md`; it is not claimed as original r11
code. The synthetic repos used real git worktree/add/diff in isolated mktemp
roots under /private/tmp only. The new exporter never commits, pushes or opens a
PR. It copies exactly allowlisted committed bytes and modes, stages them, and
checks branch, exact diff, source bytes/modes, no extra untracked files and pins.

## Finding 2 — executable and head contract

Every command-position external program in v3 uses an absolute path; the
executable-preflight row checks each program with is_file + X_OK. A separate
helper preflight checks sh, dirname, git and diskutil. Environment/caffeinate
wrappers are traversed; data filenames are not treated as executable programs.
The PR uses `/opt/homebrew/bin/gh --head backup-gdrive-r12`. Tests inject the probe
so they do not pass accidentally because a local executable exists.

| Test / counts | RED (unmodified r11 checker/plan) | GREEN |
|---|---|---|
| Missing executable, probe returns False | No finding; assertion fails | EXECUTABLE finding |
| Wrong / absent --head (2 methods) | No finding; assertions fail | PR_HEAD finding for each |
| Relative executable / all wrapped probes (2 methods) | Assertions fail | Absolute path required; env/caffeinate/rclone each probed |
| Missing/wrong format + JSON override (3 methods) | Assertions fail | LOG_FORMAT finding for each |
| Plan v3 row contract | v2 fails new contract assertion | Both content rows + executable preflight + correct head pass |
| Total (9 methods) | 9 assertion failures; 0 errors/skips; group exit 1 | 9/9 pass; 0 failures/errors/skips; group exit 0 |

`plan_actual_probe.json` records exit 0 from the default filesystem executable
probe as an additional sandbox observation. It does not replace the injected
negative controls or the future host preflight.

## Finding 3 — strict rclone date,time

Both default and full-population download templates explicitly pass
`--log-format date,time`, and run_local_check.py pins the same option for both
modes. Severity records are accepted only with exact YYYY/MM/DD HH:MM:SS
prefixes; unsupported check-log records fail closed. Unsupported ERROR/CRITICAL/
FATAL tokens in stderr also fail. Valid DEBUG argv mentions of error stay harmless.
No optional timestamp or widened severity regex is used.

| Test / counts | RED (unmodified r11 verifier/template) | GREEN |
|---|---|---|
| Microseconds / time only / prefix / JSON × 3 fatal severities | 12 assertion failures against copies of saved clean receipt | All 12 fail verification as required |
| JSON fatal severities in stderr × 3 | 3 assertion failures | All 3 fail verification |
| Default + download fixture template format | First missing-format assertion fails (1 failure) | Both explicit date,time argv controls pass |
| Valid DEBUG argv containing error | PASS retained | PASS retained |
| Standard ERROR/CRITICAL/FATAL and unprefixed tokens | FAIL retained | FAIL retained |
| Saved clean/excluded/symlink/corruption (4 CLI controls) | Expected 0/0/0/1 retained | Expected 0/0/0/1 retained; corruption names alpha.txt |
| Total (10 test methods; subtests counted separately above) | 16 assertion failures; 0 errors/skips; group exit 1 | 10/10 methods pass; 0 failures/errors/skips; group exit 0 |

`evidence_copy_manifest.json` links every copied r11 host evidence file to its
untouched K/F source and SHA-256. Several original logs were ignored/uncommitted;
this receipt contains byte-identical copies that MAESTRO must commit, including
.log files, before exporting the candidate. The verifier tests and standalone
`fixture_replay_r12/` receipts use copies of the saved receipt. No local→local
rclone command was run in the sandbox. Fresh host fixture acceptance is required.

## RED/GREEN receipts

`r12_sandbox_red/`: 25 original methods, failures 3/9/16 by finding (16 includes
subtest failures), each group exit 1; runner exit 0 confirms expected RED.
`r12_scope_amendment_red/`: 27 methods, only the two new scope assertions fail;
scope/runner exit 1 is the expected amendment RED, with other groups exit 0.
`r12_scope_amendment_green/` and `r12_sandbox_final_green/`: 27/27 pass (8+9+10),
all group and runner exits 0, no errors or skips. The initial
`r12_sandbox_green/` was 25/25 before the two amendment controls were added.

## Before/after SHA-256

| Changed input | Before SHA-256 (before/) | After SHA-256 |
|---|---|---|
| activation_plan_v3.md | f1639ee30835a79a118d757bbddc9540ea066f9bf33ea5d4bba360b3aa7ca11f | 3621a5e301fc126021b04bd0125ad0ee043812678711f304ffe92691aa3bab15 |
| check_plan.py | 4bca51b5a9da521afd87d8cdbd2136ccc7e4a9e784c6e9b3155207f7a41cf8e9 | cba298519ee2fdffccea12f855989a389e353e703bc32692183b2aa8d9620646 |
| verify_check.py | 5b4748c501d3d5f416a689978a8052d3d2a3390a5d0439b313f4285ab8a1fbfc | 4963b46b677fc86002cc8b0bdae3c1b273281fa627d5c85c538dfe208a08ce5f |
| run_local_check.py | 0c9045c7635919f61ca91792c8ed756074ebb1a8fcfcabfdbd66980102131a75 | 4e008d7b74745b87b8c5b4b7ee82b15e363d5ad980f10614a77bcd46c83be8ad |

The inherited helper copies capture.py, real_inventory.py and run_py39_coverage.py
are unchanged; `before/` also preserves them and both v2 pin files.

| Production/test path | Before = after SHA-256 |
|---|---|
| tools/backup_gdrive.sh | 36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8 |
| tools/backup_gdrive_status.py | 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46 |
| tools/backup_mirror.excludes | 45bb4e2a2e4629d494b6e5ccf41dd6885133b27e329a197fc6a85bcc55e48f3f |
| tools/launchd/MemitGdriveBackup.applescript | 4e1e79eec6dab2944bda793814dbcd0ee4f7fd56cfb07a523a128bff9e38a428 |
| tools/launchd/build_gdrive_applet.sh | 33d0e8473f3d731584f163f7b90e2fee1be7df3b98432c7afc181108884f7252 |
| tools/launchd/com.rhu.memit-gdrive-backup.plist | 702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce |
| tools/launchd/stage_gdrive_release.sh | b157637701cf8fd55eb121468c6852a49c7b911e2df8df25505762a36d5f3b9e |
| tools/test_backup_gdrive.py | 3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5 |
| tools/test_backup_gdrive_addendum.py | 3ff28cb712e97941476c1730928ff720f9a0dbcb2d8ba29344647ea8904501f8 |

## Pins, exact scope and host commands

`pins_v3.sha256` and `pins_v3.json` supersede and hash-link both v2 pin files;
v2 and K remain untouched. All selected v2 pins are retained and all new candidate
inputs/evidence are pinned. The two pin manifests cannot hash themselves; source
byte comparison plus comparison against the reviewed manifests covers them.
`operational_checks/` stays outside candidate scope to avoid self-referential
final/pin-check receipts. It may contain future host gate receipts; no exporter
discovers or copies it. SHA checks and literal scope counts are recorded there.

Run one host action at a time, at niceness 0 with production Python 3.9.6. The
script validates each command's actual exit and uses fresh r12_* labels. An
existing label fails rather than overwrites evidence. Required sequence:

```sh
H=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/backup_gdrive_host_20261011/r12_package_20261011T024815Z/host_commands_r12.sh
/bin/sh "$H" pins
/bin/sh "$H" check
/bin/sh "$H" package
/bin/sh "$H" fixture
/bin/sh "$H" freeze
/bin/sh "$H" pins-final
```

Host fixture requires all four expected outcomes, real before/after inventory
invariance, disjoint APFS physical stores, isolated config positive control and
all owned groups exited. Native/coverage r11 evidence remains historical; no
new claim of 155 executed passes or scientific/live-Drive acceptance is made.
Freeze incorporates fresh host evidence into literal scope and v3 pins. Submit
those final bytes and host evidence to Astra r12; any NO-GO stops the plan.

After host evidence settles, MAESTRO commits every enumerated new receipt path
(including ignored logs) in the reviewed source commit. Set
MAESTRO_SOURCE_COMMIT from that validated full commit SHA and
MAESTRO_CANDIDATE_PATH to a fresh isolated absolute path, then:

```sh
/bin/sh "$H" candidate
/bin/sh "$H" candidate-verify
```

Candidate export stages files without committing. MAESTRO commits/publishes the
backup-only branch under the plan's GO, requires exact candidate head CI green,
re-verifies pins/scope, and uses the cooperative merge gate. No PR from the broad
worktree branch is permitted. MAESTRO alone edits docs/program_state.json.

## Astra r12 map

| Finding | File:line |
|---|---|
| 1 | scope_allowlist.txt:1; scope_unchanged.txt:1; candidate.py:51; make_backup_candidate.sh:1; test_r12.py:72 |
| 2 | activation_plan_v3.md:35 / 87; check_plan.py:40 / 104; test_r12.py:121 |
| 3 | activation_plan_v3.md:290 / 311; verify_check.py:51; run_local_check.py:23; test_r12.py:199 |

The v2→v3 changed-row erratum is appended to activation_plan_v3.md and duplicated
in erratum.md. Only the finding-touched scope/pins/executable/content rows and
necessary receipt references were changed; all operational GO/STOP gates remain.

## Context save and successor directive

Context-save is scoped to this receipt because MB44 forbids writes elsewhere;
no ~/.gstack or memory file was written. Final state is in context_save.md and
SHA authority in pins_v3. Any successor must read this README, the user-approved
scope amendment and final pins before editing. Remaining work is MAESTRO's
host reruns, source commit, candidate export/CI and Astra r12 review.

**Binding operator directive (2026-10-10):** watch Context N% left. Start a new
piece only at >=60% left. At <=40% left, or on any Context compacted, stop
starting work, append a handoff here with done/half-done, exact paths, SHA-256s,
test state and a single next step, restate this directive, and reply MB44 HANDOFF.
