

## MB6 Astra r1 and launchd corrections — 2026-10-10T07:58:39.664792+00:00

**Local fix build complete for MAESTRO4 review: 64 tests run, 62 PASS, 2 UNVERIFIED/skipped; exit 0, 47.323 s.** The two skips are actual applet compilation/manifest and behavioral no-dialog verification; they are not PASS. Binding Astra r2, host compilation/no-dialog proof, installation, Removable Volumes/TCC access and actual launchd execution remain host checks. No Drive call, full backup, installation or launchd mutation occurred in MB6. Earlier Drive and launcher observations in `backup_gdrive_host_20261010/HOST_FINDINGS.md` are MAESTRO4 host evidence, not results reproduced here.

Receipts: `results/backup_gdrive_mb6_20261010T072852Z/`. Final local result: `green_final.txt` and `verification_final.json`. Test-by-test RED pointers: `tdd_index_final.json`. Exact acceptance command:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum tools.test_backup_gdrive -v
```

Addendum: 54 tests (52 PASS, 2 UNVERIFIED). Original: 10 tests (10 PASS). Bash syntax, Python AST parsing, plist lint and scoped diff checks PASS (`syntax_final.json`). Only local storage, tiny fixtures and standard-library Python were used; no model, GPU, science or dashboard suite was run. Disk budget was under 20 MiB. Pre-write free-space observation: 89,665,060 KiB on memit and 207,328,024 KiB under `/private/tmp`, both exceeding the budget plus 20 GiB.

### Changes and behavioral evidence

1. **Astra 1 — history-safe retry policy.** Sync explicitly sets `--retries 1` and `--low-level-retries 10`. The native real-rclone/local regression archives a=v0, uploads v1, makes a queued second file vanish, then changes a to v2 at the first Attempt boundary. Pre-fix retries overwrote archived v0 with v1; the corrected run preserves v0 and leaves the mirror at v1 with source-vanish/deletion-suppression warnings. This is measured local-backend behavior, not a new Drive observation. RED: `red_retry_overlap.txt`; GREEN: `green_final.txt`.
2. **Astra 2 — configuration admission and false-success refusal.** Preflight rejects every inherited `RCLONE_*` variable except the `RCLONE_CONFIG` credential/config-file locator. The installed rclone's local `config dump` validates the selected effective config: exit, nonempty output, JSON and field shape; every remote `global.*` or `override.*` key refuses dispatch. Config values, including OAuth credentials, remain captured privately and are never printed. Inline/on-the-fly connection strings refuse too. Explicit false boolean flags disable dry-run, interactive mode, ignore-errors and delete-excluded; delete-after is explicit. No deletion-barrier override is enabled. Classification and status refuse dry-run/skipped-operation logs even with raw exit 0 and nonzero accounting bytes. Environment, config, connection-string, actual dispatched-argument and log/heartbeat controls have REDs.
3. **Astra 3 — authoritative heartbeat under ownership.** Acquire the mkdir lock and record its owner before publishing start. Start, child-PID refresh and terminal publication occur under that ownership; terminal publication precedes unlock. Non-owners never write `last_run.json`. Held-lock exit 75 gets a separate atomic receipt at `<heartbeat-parent>/refusals/<stamp>.json`; refusal-publication errors use `REFUSAL-RECORD-FAILED`, avoiding false poisoning of an owner's heartbeat. A live-owner test checks byte-for-byte preservation during refusal. The tightened admitted-overlap schedule pauses B at the actual shell command before lock acquisition (after start in the old wrapper), completes A, resumes B, requires B's dispatch marker and live process, then requires non-success/incomplete status. A refused contender can no longer satisfy it.
4. **Dead unfinished runs and publication failure.** Heartbeats record wrapper owner/rclone PIDs. After dispatch a start refresh records the child. Dead recorded processes yield `stale incomplete backup: owner and rclone PIDs are dead`, exit 1. Live-owner, live-child and pre-dispatch owner controls stay incomplete/non-success. No age-based lock expiry was added. A child-PID publication failure now waits/reaps and preserves a genuine raw failure before cleanup; `red_child_publication.txt` reproduces raw exit 23 previously becoming exit 1. Existing publication-failure assertions remain intact.
5. **Astra 6 — per-attempt proof.** Each Attempt boundary requires both files and directories deletion-suppression records. The retry-evidence test supplies Astra's exact negative input removing both first-attempt records, each individual record, and both final-attempt records; all remain FATAL/nonzero. The admitted-overlap test above closes the other overstated test's missing schedule.
6. **Launcher.** `tools/launchd/MemitGdriveBackup.applescript` wraps `/bin/bash /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh` in `try ... end try`, with no dialog-producing error handler. Executable `tools/launchd/build_gdrive_applet.sh <output.app>` refuses existing bundles, invokes `/usr/bin/osacompile`, and prints each regular bundle file's SHA-256. The plist invokes `/usr/bin/open -W -g /Users/robertrhu/Applications/MemitGdriveBackup.app`, retaining interval 21600 and RunAtLoad=false. Parsed plist behavior PASS. Actual applet build/manifest and no-dialog execution are **UNVERIFIED** below.
7. **Concurrent binding operator update.** During MB6 the runbook was committed with D-C10r-rulings-15: “Slower by day, full at night” means exact `--bwlimit '08:00,512k 23:00,off'`. The wrapper now passes that setting. Its added regression records the actual dispatched argv and completes a tiny real local sync; `red_upload_timetable.txt` proves its absence before the fix. The old host 69-hour payload estimate predates this timetable; no new duration or daytime rate measurement is claimed.

Primary flag references: [rclone retry semantics](https://rclone.org/docs/#retries-int), [remote global overrides](https://rclone.org/docs/#adding-global-configuration-to-a-remote), [configuration precedence](https://rclone.org/docs/#environment-variables). Local fixtures and exact host receipts bind over documentation assumptions.

### Applet boundary — UNVERIFIED, exact observations

The no-dialog test writes an exit-1 shell stub with a marker, substitutes it into the actual AppleScript, attempts compilation, and requires osascript exit 0 within 5 seconds plus the marker. Compilation prevented that execution: no successful stub invocation or prompt-free completion is claimed. The builder's bundle-manifest assertions were also not reached.

Actual source and exit-1 variant: osacompile exit 1, `:3: error: Expected end of line but found identifier. (-2741)`. Independent `do shell script "/usr/bin/true"` compilation/execution also failed: `A identifier can’t go after this identifier. (-2740)`. Basic `return "control"` compiled and executed successfully. Explicit AppleScript language and `use scripting additions` did not restore shell terminology. The independent raw Standard Additions command `osascript -e '«event sysoexec» "/usr/bin/true"'` returned exit 1:

```text
Connection Invalid error for service com.apple.hiservices-xpcservice.
Error received in message reply handler: Connection invalid
0:32: execution error: "/usr/bin/true" doesn’t understand the “«event sysoexec»” message. (-1708)
```

Exact command/stdout/stderr records, timestamps and PIDs are in `osa_probes.json`, `osa_terms_probes.json` and the two UNVERIFIED lines of `green_final.txt`. System-log inspection returned exit 64, `log: Cannot run while sandboxed` (`osa_log_probe.json`). The observed boundary is unavailable Standard Additions/HIServices in this execution context; the precise underlying denial was not observable. Parser errors alone do not skip tests: the independent service-connection failure is also required, and parser failures remain failures when that control works. No fake compiler, osascript result or bundle was substituted. MAESTRO4 must compile and run the exit-1 variant outside this sandbox before claiming no-dialog behavior or activation readiness.

### Test-first audit and file scope

All **14 new tests** and **3 tightened tests** have assertion-based RED receipts. `red_behavior.txt` covers the broad pre-fix failures; `red_retry_overlap.txt` supplies corrected native retry/admitted-overlap REDs; `red_child_publication.txt` covers reaping; `red_upload_timetable.txt` covers the late operator directive. `red.txt` was an initial test-string quoting SyntaxError and is excluded from RED proof. A first retry observation raced the native move of the original destination; a first overlap setup gave sourced Bash the wrong `$0`. Both test fixtures were corrected before production changes without reducing their outcome assertions. `green_first.txt` preserves publication-window and OSA failures; `green_publication.txt` verifies focused wrapper corrections; `green_second.txt` is the earlier 63-test run; `green_final.txt` is final acceptance after the upload timetable.

Only the seven code/test/launcher files below plus this appended report section were changed. Evidence/context files are in the named receipt directory. The excludes, old mirror, archive helper/manifest, CLAUDE.md, AGENTS.md and dashboard test baseline hashes match. The runbook hash changed concurrently in committed D-C10r-rulings-15; its working tree is clean (`scope_drift.json`). MB6 did not edit it or revert that progress. Baseline HEAD `b19a45664f0cc26548a6c93a8f85251833c46789`; observed HEAD `b0ee185fea0dec62f93519a5f23125aaa46f4f6d`; branch `worktree-c10k-route-a` remained unchanged. No Git mutation, repo file/branch/worktree deletion, dependency installation, Drive/full-backup call, launcher activation or memory_mirror edit occurred. One higher-priority environment-required graft lookup failed before execution because Node was absent from PATH; no graph output was used. Subsequent shell work used `/opt/homebrew/bin/rtk proxy`.

Final code/test SHA-256:

| File | SHA-256 |
|---|---|
| `tools/backup_gdrive.sh` | `b5aece49ae0f182520aa49f0c7cac8db09768c15d5212f4985c4295d04e49be7` |
| `tools/backup_gdrive_status.py` | `f7a5d933f37a928f2c0781190c43dc56a6e9ac0726beaa0d5403ddfd8f31adcd` |
| `tools/launchd/com.rhu.memit-gdrive-backup.plist` | `702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce` |
| `tools/test_backup_gdrive.py` | `3e8535a8a9440a41634af8034350f6fd446440e9adecaa5be1c2c47ce651bff5` |
| `tools/test_backup_gdrive_addendum.py` | `931588de4391e1ba1ef46adc6b9a446750dbc3567b043cc0f6516e470a8103f4` |
| `tools/launchd/MemitGdriveBackup.applescript` | `000784725e5180bca488bfc75b4752551630f54c82c0874fd261605c7b83f4c4` |
| `tools/launchd/build_gdrive_applet.sh` | `f7ca5a5b7928faa1bc24d12ac38cdd8c6ee21ad1684e9bc7579ac8cd1260189b` |

`audit.json` and `SHA256SUMS.txt` include final hashes for every changed file, including the report itself; its hash is external to avoid self-reference. `context_saved.md` saves state within the authorized receipt namespace rather than out-of-scope home state.

Done: scoped local corrections, all available checks, RED/GREEN/hash/scope/context receipts. In flight: none. Next: MAESTRO4 obtains binding Astra r2, builds the host applet and verifies its manifest and exit-1/no-dialog behavior, deploys reviewed main-checkout files and performs authorized Removable Volumes/launchd checks. No binding GO, Drive correctness guarantee or activation acceptance is claimed.

**BINDING context directive:** Watch this session and every orchestrated team's Context N% left. At approximately 20% remaining, stop starting work; write done/in-flight work, exact paths, next steps and risks into the task report; notify MAESTRO4 to use a fresh successor. Restate this directive in every handoff; never approach full-window compaction.
