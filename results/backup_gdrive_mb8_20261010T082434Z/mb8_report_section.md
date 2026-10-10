

## MB8 Astra r2 findings 5 and 6 — 2026-10-10

**Local R2 fix build DONE: 72 tests run, 70 PASS, 2 UNVERIFIED/skipped, exit 0, 108.950 s.** All eight new tests have saved, assertion-based REDs. Binding Astra r3 and host launcher/activation checks remain with MAESTRO5. This infrastructure preserves the F1 evidence/storage boundary; no science run or new scientific claim.

Receipts: `results/backup_gdrive_mb8_20261010T082434Z/`. `verification_final.json` records acceptance and both 1,000-invocation timings; `tdd_index_final.json` maps each new test to RED/GREEN. Exact acceptance:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

### Finding 5: internal-disk launch receipt and read-only status

The applet embeds two shell literals. `launchShell` synchronously runs Bash against the wrapper and captures its actual exit. `receiptShell` is independently executable with `/bin/sh`: it writes `$HOME/Library/Logs/memit-gdrive-backup/launch_receipt.json`, containing schema, microsecond UTC, wrapper path, exit code or AppleScript error number. The receipt writer uses only internal `/bin` and `/usr/bin` tools: mkdir, mktemp, Perl with bundled JSON::PP/Time::HiRes/POSIX, mv and trap cleanup. It never sources, reads or executes the wrapper or any volume-hosted helper. The receipt is encoded as JSON and replaced with same-directory temp + mv, preserving quoted/backslash paths and one bounded final file. Microseconds avoid a later failure comparing older than a heartbeat written within the same second.

Wrapper nonzero exits, including 127 for an absent path and 75 for a held lock, are recorded without raising an applet shell error. AppleScript errors use the independent receipt-only path. Both that path and receipt-write errors are caught, with no dialog-producing handler. **AppleScript/app-bundle execution is UNVERIFIED** here; the shell execution evidence does not prove native applet behavior. `launch_shell.sh` and `receipt_shell.sh` are inspection copies extracted from the applet literals, not runtime dependencies.

Status reads the sibling launch receipt and never writes `last_run.json`. A strictly newer failed launch takes precedence over the last heartbeat's end (or start while incomplete); a completed newer/equal heartbeat recovers from older launcher evidence. Exit 75 remains a refusal and leaves a real active owner in flight. A success launch receipt alone cannot make an incomplete/failed backup healthy. Malformed/future receipts fail closed. Tests preserve heartbeat bytes across launch errors, receipt writes, status reads and active-owner exit-75 refusal.

`red_launch_status.txt`: seven tests fail against the original launcher/status, including fresh success + actual absent-wrapper invocation still reporting success, and no receipt for successful launches. `green_launch_status.txt`: all seven PASS after the fix. The receipt-only AppleScript-error regression executes the embedded writer with error -1708 and proves the supplied wrapper was never executed. The unwritable-directory regression executes real shell receipt logic, requires prompt nonzero, preserves the old receipt/heartbeat and leaves no temporary file. Neither regression greps AppleScript for try/on-error/mv as behavior proof.

### Finding 6: one latest refusal receipt

Non-owners atomically replace `<heartbeat-parent>/refusals/latest-refusal.json` using the existing fsync/rename recorder. One latest receipt preserves the current refusal/run identity with constant storage and needs no ring index or retention loop. Ownership, lock recovery rules, owner heartbeat, retry flags, excludes and upload timetable are unchanged. Historical files are preserved; this build performs no historical receipt deletion.

| Evidence | Actual Bash refusals | Wall seconds | Refusal files | Total heartbeat-directory files | Total bytes |
|---|---:|---:|---:|---:|---:|
| `red_refusal_stress.txt` | 1,000 | 58.003 | 1,000 | 1,002 | 512,414 |
| `green_final.txt` | 1,000 | 60.141 | 1 | 3 | 1,010 |

Both runs held the lock in a **real live wrapper**, with its dispatched child blocked on a local FIFO. The test checks the owner remains alive, its heartbeat is byte-for-byte unchanged, and status stays incomplete/in flight. RED fails at 1,000 refusal files versus the required bound of one; GREEN passes every assertion. The count was never reduced; both 1,000-run timings are below two minutes. Runs were foreground and used only local stubs/storage. All 54 existing addendum test methods are AST-identical; the original ten-test module is unchanged. No test was removed or weakened.

### MAESTRO5 host checks — UNVERIFIED, one copy-paste list

The acceptance suite again observes osacompile exit 1 at the Standard Additions command (`(-2741)`), plus an independent osascript raw-event control failing with `com.apple.hiservices-xpcservice` / `Connection invalid` / error -1708. Exact observations are in the two skipped lines of `green_final.txt`. Compilation, bundle manifest and native no-dialog completion are not claimed PASS. The plist remains `/usr/bin/open -W -g /Users/robertrhu/Applications/MemitGdriveBackup.app`, StartInterval=21600, RunAtLoad=false.

`host_launcher_checks.py` is a **prepared host-only helper, AST-checked but not executed here**. It compiles actual app bundles on the internal disk and invokes exactly `/usr/bin/open -W -g <bundle>` with no osascript substitute. Only the wrapper-path and isolated internal HOME literals vary; the applet executable body is the reviewed source. It preserves its fixtures/bundles, hashes the bundle, logs the full command and writes `host_<case>_<UTC>/commands.json` and `summary.json` alongside these receipts. It never installs into Applications or changes launchd. The absent case uses a nonexistent `/Volumes/memit-mb8-absent-.../backup_gdrive.sh` namespace, without unmounting the working volume. A timeout or failed assertion is FAILED, never a skip/PASS; a timed-out app may need host inspection.

Run outside the Codex sandbox from this worktree, before activation:

```sh
# Finding 9: open -W must stay live while the 3-second stub runs, then await its completion.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py long
# Finding 9: exit-75 stub must exit promptly and keep the live owner's status/heartbeat intact.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py exit75
# Absent volume path: open -W -g must exit promptly, write exit 127, and override seeded fresh success.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py absent
# Receipt-write refusal: the native applet must still exit promptly without an error dialog.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_mb8_20261010T082434Z/host_launcher_checks.py writefail
# Existing native compiler/manifest and caught exit-1 checks: all three must actually PASS on the host.
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.LauncherTest -v
```

Astra finding 9's TCC/activation conditions remain: the operator's initial Removable Volumes grant must complete before unattended activation and before demanding a fresh kickstart heartbeat. Host helper receipts do not grant production TCC or prove actual launchd activation. MAESTRO5 owns binding Astra r3, reviewed merge/deployment, production applet grant, authorized job checks and eventual full-copy verification; retire the old job only after verified full-copy completion. No activation GO is inferred from this build.

### Final scope and hashes

Bash/sh syntax, Python AST, parsed plist and scoped diff checks PASS (`syntax_final.json`). Disk budget was under 20 MiB; baseline free space was 91,809,222,656 B on memit and 212,276,322,304 B internally, exceeding budget + 20 GiB. No Drive/network/model/GPU call, dependency installation, commit/push/merge, Applications installation, launchd mutation or repo deletion was performed. The mirror excludes, old mirror, archive helper, CLAUDE.md, AGENTS.md, runbook, memory_mirror and dashboard test remain at baseline hashes. Other builders changed `results/mathlab_staging/new1_construction_diag_scope.md`, `tests/test_git_automation.py`, `tests/test_new1_construction_diag.py`, `tools/dashboard_experiment.py`, `tools/git_hygiene.py` and `tools/git_merge_gate.py` concurrently; their before/after hashes are recorded in `scope_drift.json` and no change was reverted. Branch and HEAD remained `worktree-c10k-route-a` / `5620b948ea6f88d6efcb352ebce32d8cadfef816` at this audit. One environment-required graft lookup failed before execution (Node absent); no graph output was used.

Final changed code/test SHA-256:

| File | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `506ce31845bcbe812261ce128f2119f247cfe270e69b8af08e9a612207aed9ce` |
| `tools/backup_gdrive_status.py` | `f5c98ad6adb3530ac215befbfcedc94a63368a9d153186864f67823db7c40b25` |
| `tools/launchd/MemitGdriveBackup.applescript` | `ebafee3ad82a4376ec5dda0fbc823f2170c795cddd56d62f5ede730d6d5c3bab` |
| `tools/test_backup_gdrive_addendum.py` | `efa0c4e8047279bafe4dd04cfabb2b7839ff68ea012618f93b53cfd44785d985` |

The report's final SHA-256 is recorded externally in `SHA256SUMS.txt` and `audit.json` to avoid self-reference. Those receipts include hashes for all seven reviewed code/test/launcher inputs, the appended report and prepared host helper. The preexisting report bytes are preserved exactly; this section is appended.

Done: local P1/P2 corrections, exact acceptance, eight REDs, bounded-storage evidence, syntax/scope/hash audit and prepared host commands. In flight: none. Next: MAESTRO5 runs the host list and submits these exact hashes/evidence to Astra r3; activation remains host-owned. `context_saved.md` preserves decisions and this handoff within the authorized receipt namespace. Learning for the successor: pre-wrapper failure evidence must live off the source volume, and refusal history must not become an unbounded per-launch sink.

**BINDING context directive:** Watch this session and every orchestrated team's Context N% left. At approximately 20% remaining, stop starting work; write done/in-flight work, exact paths, next steps and risks into the task report; notify MAESTRO5 to use a fresh successor. Restate this directive in every handoff; never approach full-window compaction.
