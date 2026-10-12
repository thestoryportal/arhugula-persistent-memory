# Drive backup activation plan (MAESTRO24, prepared 2026-10-10T20:50Z, NOT executed)

Prepared under the operator's approval to *prepare* activation. Nothing here has been run except the read-only inspections in §1. Every step that changes the Mac waits for the operator's separate go.

Binding order: `astra_r9_verdict.md:13` (item 5), with condition 3 recorded at `astra_r9_verdict.md:20–27`. The steps in §2 follow that order exactly.

Shorthand used below:

- `W` = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` (this worktree)
- `M` = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` (main checkout; the applet hard-codes `M/tools/backup_gdrive.sh`, `tools/launchd/MemitGdriveBackup.applescript:2`)
- `R` = a fresh receipt directory, `W/results/backup_gdrive_activation_<UTC>/`, which MAESTRO creates for this activation
- `UID` = `$(id -u)`

Markers:

- **[READ-ONLY]** means no change to Mac state outside the repo. A few of these steps write a receipt into `R` (the repo); that is said explicitly.
- **[OPERATOR GO]** means the step touches launchd, Drive, `~/Applications`, the real `~/Library/Logs` or `~/Library/LaunchAgents`, the shared main checkout or master. It also covers killing processes.
- **[OPERATOR CLICK]** means the macOS Allow prompt.

---

## 1. Fresh history or recovery: **RECOVERY**, proposed floor **0** (barrier 1)

The history is not genuinely fresh. There is no production generation history, but one piece of ambiguous applet evidence exists in the real log root. The applet's allocator refuses permanently on that evidence, so initializing the counter to zero over it is ruled out (`results/backup_gdrive_build_report.md:371`, `:476`, `:646`).

### Evidence, inspected read-only on 2026-10-10 around 20:45Z

| Item the floor must cover (r9 item 5; build report MB25 list `:1030`) | Real path | Observed |
|---|---|---|
| Current raw counter | `~/Library/Logs/memit-gdrive-backup-launch-state/counter` | **absent** (the whole `-launch-state/` directory is absent) |
| Current state | `…-launch-state/unresolved.json` | **absent** |
| Heartbeat | `~/Library/Logs/memit-gdrive-backup/last_run.json` | **absent** |
| Launch receipt | `~/Library/Logs/memit-gdrive-backup/launch_receipt.json` | **PRESENT**: 156 B, mode 0600, mtime 2026-10-10 02:47:51 local, SHA-256 `53614afd90df282c8e90f8299c0fb98b81a10b35f6838377757ff1e36d0af6b4`. Content: `{"utc":"2026-10-10T08:47:51.074479Z","error_number":null,"wrapper_path":"/private/tmp/gdrive_addendum_y14okm79/failing-backup.sh","schema":1,"exit_code":1}`. It has **no `launch_generation` key**. This is the test-leaked receipt described at `build_report.md:476`. |
| Failure journal | `~/Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl` | **absent** (directory absent) |
| Refusal | `~/Library/Logs/memit-gdrive-backup/refusals/latest-refusal.json` | **absent** (directory absent) |
| Six temporary prefixes (`.last_run.` `.launch-receipt.` `.unresolved.` `.journal.` `.counter.` `.recovery.`, `tools/backup_gdrive_status.py:304–306`) in the four live dirs (`memit-gdrive-backup/`, `…/refusals/`, `…-launch-state/`, `…-launch-journal/`, `:347–349`) | | **none**: `ls -la` of `memit-gdrive-backup/` shows only `launch_receipt.json`, and the other three dirs do not exist |
| Recursive manifests, archived counters, payloads and temporaries | `…-launch-state/recoveries/**` | **absent** |
| Ownership lock | `~/Library/Logs/memit-gdrive-backup.lock` | absent |
| Wrapper log / launchd log | `~/Library/Logs/memit-gdrive-backup.log`, `…/memit-gdrive-backup.launchd.log` | absent |
| Production app | `~/Applications/MemitGdriveBackup.app` | **absent** (never installed) |
| New job | `~/Library/LaunchAgents/*gdrive*`, `launchctl list` | **none** |
| Old job | `com.rhu.memit-backup` (`~/Library/LaunchAgents/com.rhu.memit-backup.plist`, 1860 B, runs `~/Applications/MemitBackup.app`) | loaded; `launchctl print`: not running, runs = 6, last exit code = 0. Its log last read `backup_mirror: 20261010T053954 OK` (mtime 11:20 local). |

Further checks:

- The real-path inventory (`results/backup_gdrive_mb25_20261010T202206Z/real_path_listing.py`, written to stdout) hashes to `ec66a1f5f571981f01be772c353ba252e2ce4d5f67953631ea6293a524392b99`. That is byte-identical to MB25's before and after listings and MAESTRO23's host runs, so nothing in the real paths has changed since.
- Read-only status (`.venv/bin/python -B tools/backup_gdrive_status.py`, no args; `health()` at `:559–645` only reads) printed `backup_gdrive_status: missing or malformed launch receipt generation` and exited 1. `/usr/bin/python3` 3.9.6 gave the same output.
- `rclone lsd gdrive: --max-depth 1` exited 0 and listed `memit-archive` and `memit-backup`. `rclone lsf gdrive:memit-backup --max-depth 1` came back empty, so the Drive destination is fresh.

### Why floor 0

- The status tool's scanner (`tools/backup_gdrive_status.py:285–436`) finds no supported generation field anywhere. The only evidence file, the receipt, has no generation, so it is classed as *ambiguous* (`:398–403`) and contributes nothing to the maximum. Observed maximum = 0, so floor 0 is accepted (`:404–406`; the allowed range is `0 <= floor < 2147483646`, `:287`).
- Generation numbering did not exist when the receipt was written. It is dated 08:47:51Z, from the 0ab0c42 native test. MB11 introduced generations at about 09:26Z (`build_report.md:363–371`). The counter directory has never existed in the real HOME, and the production app has never been installed. So no generation was ever issued against the real log root, and no history was lost.
- The result of floor 0 would be: barrier 1, counter `1`, state `{"compaction_barrier":null,"issued_generation":1,"recovery_barrier":1,"schema":1,"unresolved":[]}`. The receipt is moved byte-for-byte into `recoveries/<UTC>/` (`:427–440`). The first applet launch then allocates generation 2, and completing 2 clears the barrier, because 2 > 1 (`:527–529`).
- Any larger floor is equally safe; it only raises the barrier. The floor is the operator's to confirm (`build_report.md:553`).

Initializing zero instead would hit the applet's Perl allocator: it reads `launch_receipt.json`, finds no generation, and dies with `ambiguous or non-increasing launch generation` (the allocator embedded at `MemitGdriveBackup.applescript:3`). That is known limit 2 (`build_report.md:474`).

---

## 2. Activation steps, in the binding order

### Step 0: preconditions

| # | Marker | Command | Expected / check |
|---|---|---|---|
| 0.1 | [READ-ONLY] | `cd W && shasum -a 256 -c results/backup_gdrive_mb25_20261010T202206Z/final_sha256.txt \| grep -c ': OK$'` | `33`, and no `FAILED` lines. Verified at 20:4xZ: 33/33 OK. |
| 0.2 | [READ-ONLY] | `cd W && LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B results/backup_gdrive_mb25_20261010T202206Z/real_path_listing.py /dev/stdout \| shasum -a 256` | `ec66a1f5f571981f01be772c353ba252e2ce4d5f67953631ea6293a524392b99`. Any other value means the real paths changed: redo §1 before recovery. |
| 0.3 | [READ-ONLY] | `ps -axo pid,ppid,etime,command \| grep -E 'memit_gdrive_native_\|Native_[0-9]+\.app\|held-rclone' \| grep -v grep` | Should be empty. **At 20:45Z it was not** (see §5 item 6): two orphaned fixture applets (pids 32906 and 36233) and their `held-rclone` stubs (65807, 37109). Their HOME is isolated under `/private/tmp/memit_gdrive_native_*`. |
| 0.3a | [OPERATOR GO] | Only if the owner of those host runs confirms they are abandoned: `kill 37109 65807` (the stubs), then re-check 0.3; the applets should exit once their wrapper returns. | 0.3 comes back empty. This is not strictly blocking, because their HOME is isolated, but it avoids confusing "applet" processes and sleep assertions during the Allow step. |
| 0.4 | [READ-ONLY] | `/opt/homebrew/bin/rclone lsd gdrive: --max-depth 1; /opt/homebrew/bin/rclone lsf gdrive:memit-backup --max-depth 1` | Exit 0; lists `memit-archive` and `memit-backup`; the second listing is empty. An auth error means stop and re-auth per `memory_mirror/gdrive-rclone-remote.md`. |
| 0.5 | [READ-ONLY] | `ls -d ~/Library/Logs/memit-gdrive-backup.lock; df -k / /Volumes/memit` | Lock: `No such file or directory`. Disk budget: this activation writes under 100 MB to internal `~/Library/Logs` (run JSONL at INFO for about 40k files, plus stats) and nothing to memit. Free space at 20:45Z: internal about 196 GiB, memit about 80 GiB. |

### Step 1: stage and hash the reviewed wrapper, status tool and production app

The main checkout `M` is on `master` at `557a58b`, behind `origin/master` `a424085`. **None of the backup files exist in `M`**: `tools/backup_gdrive.sh`, `tools/backup_gdrive_status.py` and `tools/launchd/{MemitGdriveBackup.applescript,build_gdrive_applet.sh,com.rhu.memit-gdrive-backup.plist}` are all missing there. `origin/master` (PR #21, which merged 186491a) carries an **older** status tool (`614a5edb…`) and applet (`446d35a6…`). The reviewed bytes exist only on `worktree-c10k-route-a`, which is 48 commits ahead of the merge base `bac4fbe`. No PR is open for it. The `M` tracked tree is clean, and none of the 7,720 paths the branch adds already exist in `M`. Staging therefore means a new PR, a gated merge, and a fast-forward of `M` (`HOST_FINDINGS.md:29–35`).

| # | Marker | Command | Expected / check |
|---|---|---|---|
| 1.1 | [READ-ONLY] (repo write: copy into `R`) | `mkdir -p R && cp -p ~/Library/Logs/memit-gdrive-backup/launch_receipt.json R/leaked_launch_receipt_20261010T084751Z.json && shasum -a 256 R/leaked_launch_receipt_20261010T084751Z.json ~/Library/Logs/memit-gdrive-backup/launch_receipt.json` | Both `53614afd…f6b4`. This satisfies "must be preserved in this repo" (`build_report.md:476`); MAESTRO commits it. It only reads `~/Library`. |
| 1.2 | [READ-ONLY] | `gh pr create --base master --head worktree-c10k-route-a …` (or a backup-only branch; see §5 item 1), wait for green Linux CI on the exact head, then `cd <isolated integration worktree> && LLMDB_ROOT=$PWD python3 tools/git_hygiene.py --dry-run` and `LLMDB_ROOT=$PWD python3 tools/git_merge_gate.py <PR> --dry-run` | Dry-runs report OK; CI is green on the head. Opening a PR is a GitHub write, so MAESTRO does it as part of normal merging. |
| 1.3 | **[OPERATOR GO]** | Following CLAUDE.md § Merging (reserve, suspend, drain): `LLMDB_ROOT=$PWD python3 tools/git_hygiene.py --apply`, then `LLMDB_ROOT=$PWD python3 tools/git_merge_gate.py <PR> --apply` | The gate reports the merge with its SHA, and master's post-merge CI passes. The operator's approval must be given in chat (`memory/merge-gate-first-use-learnings.md` item 1). |
| 1.4 | **[OPERATOR GO]** (mutates the shared main checkout) | `git -C M fetch origin && git -C M merge --ff-only origin/master` | Fast-forward with no conflict. The gate does not update `M` itself (`tools/git_merge_gate.py:138` step list). |
| 1.5 | [READ-ONLY] | `cd M && shasum -a 256 tools/backup_gdrive.sh tools/backup_gdrive_status.py tools/backup_mirror.excludes tools/launchd/MemitGdriveBackup.applescript tools/launchd/build_gdrive_applet.sh tools/launchd/com.rhu.memit-gdrive-backup.plist` | Exactly the §3 table. Any mismatch means STOP. |
| 1.6 | [READ-ONLY] | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B M/tools/backup_gdrive_status.py; echo $?` | Still `missing or malformed launch receipt generation`, exit 1. The staged copy reads the same real state. |
| 1.7 | **[OPERATOR GO]** (writes `~/Applications`) | `/bin/bash M/tools/launchd/build_gdrive_applet.sh ~/Applications/MemitGdriveBackup.app > R/production_app_manifest.txt; echo $?` | Exit 0. The builder refuses to overwrite (`build_gdrive_applet.sh:12–15`). Stdout is a `sha256  path` line for every bundle file, including `Contents/MacOS/applet` and `Contents/Resources/Scripts/main.scpt`. |
| 1.8 | [READ-ONLY] | `find ~/Applications/MemitGdriveBackup.app -type f -exec shasum -a 256 {} \; \| LC_ALL=C sort -k 2 \| diff - R/production_app_manifest.txt && osadecompile ~/Applications/MemitGdriveBackup.app/Contents/Resources/Scripts/main.scpt \| grep -c 'arhugula-persistent-memory/tools/backup_gdrive.sh' && osadecompile …/main.scpt \| grep -c 'display dialog'` | `diff` is empty; the wrapper-path count is ≥ 1; the `display dialog` count is 0 (the source has none). The bundle manifest is not pinned anywhere; see §5 item 2. MAESTRO commits `R/production_app_manifest.txt`. |

### Step 2: recovery with the operator-reviewed floor (not initialize-zero; see §1)

| # | Marker | Command | Expected / check |
|---|---|---|---|
| 2.1 | [READ-ONLY] | Re-run 0.2 and 0.5, then `for d in ~/Library/Logs/memit-gdrive-backup ~/Library/Logs/memit-gdrive-backup/refusals ~/Library/Logs/memit-gdrive-backup-launch-state ~/Library/Logs/memit-gdrive-backup-launch-journal; do ls -la "$d" 2>&1; done; find ~/Library/Logs/memit-gdrive-backup-launch-state/recoveries 2>&1` | Same as §1: only `launch_receipt.json`, and every other path is `No such file or directory`. If anything else appears, STOP and re-derive the floor with the operator. |
| 2.2 | **[OPERATOR GO]** (operator confirms floor **0**; writes the real `~/Library/Logs`) | `cd M && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor 0; echo "exit=$?"` (no `--heartbeat`, so it targets the real HOME, `build_report.md:553,646`). Keep it short and in the foreground (python GPU-admission gate, CLAUDE.md LAW 1). | Exit 0 and exactly one stdout line: `backup_gdrive_status: recovery barrier generation 1; preserved evidence: /Users/robertrhu/Library/Logs/memit-gdrive-backup-launch-state/recoveries/<YYYYMMDDTHHMMSS.ffffffZ>; requires a subsequent completed generation above the barrier` (`:441–443`). |
| 2.3 | [READ-ONLY] (copies into `R`) | `S=~/Library/Logs/memit-gdrive-backup-launch-state; cat $S/counter; cat $S/unresolved.json; A=$(ls -d $S/recoveries/*); cat $A/manifest.json; shasum -a 256 $A/launch_receipt.json; ls ~/Library/Logs/memit-gdrive-backup/; cp -p $A/manifest.json $S/unresolved.json $S/counter R/` | counter `1`; state `{"compaction_barrier":null,"issued_generation":1,"recovery_barrier":1,"schema":1,"unresolved":[]}`; manifest `{"generation_floor": 0, "highest_seen": 0, "preserved_paths": ["/Users/robertrhu/Library/Logs/memit-gdrive-backup/launch_receipt.json"], "recovery_barrier": 1, "schema": 1}`; archived receipt `53614afd…f6b4`; the live `memit-gdrive-backup/` directory is empty. |
| 2.4 | [READ-ONLY] | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B M/tools/backup_gdrive_status.py; echo $?` | `backup_gdrive_status: unacknowledged recovery barrier generation 1: requires a subsequent completed heartbeat; manual/unsequenced heartbeat cannot acknowledge applet evidence`, exit **1** (`:527–529`). Recovery never establishes health. **Exit 0 here means STOP.** |

### Step 3: invoke the production app, grant Allow, await completion, verify sequenced health

This first run is the **full initial upload**: 40,412 files and 287,080,274,442 B (`HOST_FINDINGS.md:12`). The ~69 h figure there ignores the wrapper's daytime `--bwlimit '08:00,512k 23:00,off'` (`tools/backup_gdrive.sh:129`). At 512 KiB/s for 15 h a day and the measured 1.16 MB/s for 9 h, the rate is about 66 GB/day, so expect **about 4–4.5 days**. The Mac must stay awake on AC with memit mounted throughout. The old internal-SSD job keeps running in the meantime; it is retired last.

| # | Marker | Command | Expected / check |
|---|---|---|---|
| 3.1 | **[OPERATOR GO]** (runs the app; first Drive writes; writes `~/Library/Logs`) | In a tmux pane at the Mac: `tmux new -s gdrive-first` → `/usr/bin/caffeinate -i -s /usr/bin/open -W -g ~/Applications/MemitGdriveBackup.app; echo "open exit=$?"`. `caffeinate` only keeps the invoking process awake. It is my suggestion, not part of the reviewed launcher; drop it if preferred. | Within seconds the applet allocates generation 2: `cat …-launch-state/counter` reads `2`. |
| 3.2 | **[OPERATOR CLICK]** | macOS asks for "MemitGdriveBackup" to access files on a removable volume. Click **Allow**. The operator must be physically at the Mac; a phone session cannot click it. | Afterwards, `~/Library/Logs/memit-gdrive-backup.log` shows `start /Volumes/memit/llm-database-poc-mirror/ -> gdrive:memit-backup/llm-database-poc-mirror/ …`, and `last_run.json` has `launch_generation: 2`, `launch_mode: "applet"`, `end: null` and a live `rclone_pid`. |
| 3.3 | [READ-ONLY] (poll while running) | `tail -3 ~/Library/Logs/memit-gdrive-backup.log; /usr/bin/python3 -B M/tools/backup_gdrive_status.py; pgrep -fl 'rclone sync /Volumes/memit'` | While running, status prints `unacknowledged recovery barrier generation 1: requires a subsequent completed heartbeat` (exit 1); that is expected. rclone is alive, and NOTICE stats lines appear in `~/Library/Logs/memit-gdrive-backup/runs/<STAMP>.jsonl`. Arm a Monitor watcher; this takes days. |
| 3.4 | [READ-ONLY] | After `open exit=` prints: `cat ~/Library/Logs/memit-gdrive-backup/launch_receipt.json ~/Library/Logs/memit-gdrive-backup/last_run.json; cat ~/Library/Logs/memit-gdrive-backup-launch-state/{counter,unresolved.json}; ls ~/Library/Logs/memit-gdrive-backup-launch-journal 2>&1; /usr/bin/python3 -B M/tools/backup_gdrive_status.py; echo $?` | `open exit=0`. Receipt: `launch_generation: 2`, `exit_code: 0`, `error_number: null`. Heartbeat: `launch_generation: 2`, `launch_mode: "applet"`, `exit_code: 0`, `end` set, `rclone_exit_code: 0`, `warnings: []`. Counter `2`; `unresolved: []`; no journal. Status: `backup_gdrive_status: fresh successful backup; finished <end>; launch generation 2`, **exit 0** (`:637–643`). Copy receipt, heartbeat and state into `R`. Status must be read within 13 h of `end` (stale rule, `:604`). |
| 3.5 | [READ-ONLY] (recommended full-copy check; see §5 item 4) | `/opt/homebrew/bin/rclone check /Volumes/memit/llm-database-poc-mirror/ gdrive:memit-backup/llm-database-poc-mirror/ --one-way --exclude-from M/tools/backup_mirror.excludes --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links --size-only 2>&1 \| tail -5` | `0 differences found`. Only files that changed after the run's start may differ; record those, and they are picked up on the next run. It reads Drive and does not write. |

### Step 4: install and load the plist, kickstart, verify a fresh completion

| # | Marker | Command | Expected / check |
|---|---|---|---|
| 4.1 | **[OPERATOR GO]** (writes `~/Library/LaunchAgents`) | `cp M/tools/launchd/com.rhu.memit-gdrive-backup.plist ~/Library/LaunchAgents/ && shasum -a 256 ~/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist && plutil -lint ~/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist`. Copy it; do not symlink, because launchd rejects a symlink onto the external volume (old plist comment, `~/Library/LaunchAgents/com.rhu.memit-backup.plist`). | `702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce`, `OK`. |
| 4.2 | **[OPERATOR GO]** | `launchctl bootstrap gui/UID ~/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist; launchctl print gui/UID/com.rhu.memit-gdrive-backup \| grep -E 'state\|program\|runs\|run interval'` | Bootstrap exits 0. `state = not running`, `program = /usr/bin/open`, `run interval = 21600 seconds`, `runs = 0`. `RunAtLoad` is false (`plist:19–20`), so nothing starts yet. |
| 4.3 | **[OPERATOR GO]** | `launchctl kickstart gui/UID/com.rhu.memit-gdrive-backup` | Counter goes to `3`; no new Allow prompt (the grant persists for the same bundle). |
| 4.4 | [READ-ONLY] | Poll until `pgrep -f 'MemitGdriveBackup.app/Contents/MacOS/applet'` is empty, then `cat ~/Library/Logs/memit-gdrive-backup.launchd.log; launchctl print gui/UID/com.rhu.memit-gdrive-backup \| grep -E 'runs\|last exit'; /usr/bin/python3 -B M/tools/backup_gdrive_status.py; echo $?` | The launchd log is empty or benign; `runs = 1`. Status: `fresh successful backup; finished <end>; launch generation 3`, **exit 0**; the receipt and heartbeat both show generation 3. As an incremental run this should take minutes. The launchd exit code is **not** health evidence (`HOST_FINDINGS.md:26`); the status line is. |

### Step 5: retire the old job, only after verified full-copy completion

| # | Marker | Command | Expected / check |
|---|---|---|---|
| 5.1 | [READ-ONLY] | Confirm 3.4 (generation 2 healthy, full upload), 3.5 (0 differences) and 4.4 (generation 3 healthy). | All three hold. If any is missing, do not retire. |
| 5.2 | **[OPERATOR GO]** | `launchctl bootout gui/UID/com.rhu.memit-backup; launchctl disable gui/UID/com.rhu.memit-backup; launchctl print gui/UID/com.rhu.memit-backup 2>&1 \| head -2` | The print reports `Could not find service`. `disable` keeps the job from reloading at next login, because the plist still sits in `~/Library/LaunchAgents` (§5 item 5). |
| 5.3 | **[OPERATOR GO]** (optional) | Move, do not delete, `~/Library/LaunchAgents/com.rhu.memit-backup.plist` into a parked location the operator picks, for example `~/Library/LaunchAgents.retired/`. The ~287 GB internal-SSD mirror `~/Backups/memit` and `~/Applications/MemitBackup.app` are a separate reclaim decision (storage discipline: ask, then `shutil.rmtree`; never `rm`). | The plist is gone from LaunchAgents; `launchctl list \| grep memit` shows only `com.rhu.memit-gdrive-backup`. |

**Marker counts:** **[OPERATOR GO] = 11** (0.3a, 1.3, 1.4, 1.7, 2.2, 3.1, 4.1, 4.2, 4.3, 5.2, 5.3; 0.3a and 5.3 are conditional or optional). **[OPERATOR CLICK] = 1** (3.2). Everything else is [READ-ONLY].

---

## 3. SHA-256 of every file to be staged

Computed 2026-10-10 around 20:45Z. The worktree bytes equal the `a72f638` blobs and `HEAD` `b6372c4` for every row. Re-check them in `M` at step 1.5.

| File | SHA-256 | Pinned where |
|---|---|---|
| `tools/backup_gdrive.sh` (wrapper) | `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8` | `results/backup_gdrive_mb25_20261010T202206Z/final_sha256.txt` (r9: 33/33 matched at `a72f638`; re-verified 33/33 OK now). This file also equals `origin/master`. |
| `tools/backup_gdrive_status.py` (status tool) | `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46` | same `final_sha256.txt`. `origin/master` has the **older** `614a5edb…` (186491a). |
| `tools/launchd/MemitGdriveBackup.applescript` (production-app source) | `80c7b7126bb0bc2822e71d25dd44174cdf92e18a5a9fa4076764140ce035384c` | same `final_sha256.txt`. `origin/master` has the older `446d35a6…`. |
| `tools/launchd/build_gdrive_applet.sh` | `f7ca5a5b7928faa1bc24d12ac38cdd8c6ee21ad1684e9bc7579ac8cd1260189b` | **Not** in the 33-hash list. Recorded at `build_report.md:247,347`, unchanged since MB8 and equal to `origin/master`. |
| `tools/launchd/com.rhu.memit-gdrive-backup.plist` | `702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce` | **Not** in the 33-hash list. Recorded at `build_report.md:347`, equal to `origin/master`. |
| `tools/backup_mirror.excludes` (read by the wrapper, `backup_gdrive.sh:9`) | `45bb4e2a2e4629d494b6e5ccf41dd6885133b27e329a197fc6a85bcc55e48f3f` | **Not** pinned in any review. Last changed at `1eb8131`; identical in `M`, `a72f638` and `origin/master`. |
| `~/Applications/MemitGdriveBackup.app` (production app) | the step-1.7 builder manifest | **No pinned value exists.** It is built at step 1.7 and recorded in `R/production_app_manifest.txt`. |

---

## 4. Stop conditions: halt, preserve the bytes, report

Preserving bytes means: never edit, move, rename or delete the named file. Run `shasum -a 256 <file>` and `cp -p <file> R/` (for a directory, `ditto`), then record the exact command, its output and exit code in `R`, and report. Do not retry with a different floor, and do not hand-repair state.

1. **Hash mismatch** at 0.1, 1.5 or 2.3, or 0.2 no longer `ec66a1f5…` before recovery.
2. **Unsupported evidence at recovery.** `recover` exits 1 with `backup_gdrive_status: recovery refused: …`. Any of these must stop the activation: `unsupported recovery evidence in <path>…`, `unsupported nested generation field in <path>`, `unsupported generation field … in <path>`, `duplicate JSON key`, `unsupported recovery evidence format in <path>`, `unsupported counter temporary in <path>`, `malformed preserved recovery manifest`, `malformed unresolved generation state`, `generation floor 0 is below observed maximum N`, `generation space exhausted`, `backup ownership lock exists`. Preserve the named file and the whole `~/Library/Logs/memit-gdrive-backup*` tree as found. Under-lock refusals leave every byte unchanged (`astra_r9_verdict.md:3–5`).
3. **Recovery succeeded, but the post-state differs from 2.3.** For example the counter ≠ `1`, the state ≠ the expected JSON, the archived receipt hash ≠ `53614afd…`, or a file is left in `memit-gdrive-backup/`.
4. **False green.** Status exits 0 at 2.4, or at any point before a generation above the barrier has completed.
5. **First-run failure.** Any of these, after the app has exited:
   - `open exit≠0`
   - a receipt with `exit_code ≠ 0`, `exit_code = 75` or a non-null `error_number`
   - any `…-launch-journal/failures.jsonl`
   - status naming `failed backup launch`, `failed backup (exit N)`, `token/auth error`, `dry-run or skipped operations`, `unacknowledged launch generation`, `newer heartbeat publication failed`, `stale incomplete backup` or `malformed …`
   - `Operation not permitted` in the wrapper log
   - `HEARTBEAT-FAILED` or `FATAL` in `~/Library/Logs/memit-gdrive-backup.log`
6. **No Allow prompt, or a hang.** No prompt appears and the wrapper log shows no `start` within a few minutes. Or the applet stays alive with no `rclone sync` child, which matches the modal-dialog hang in `HOST_FINDINGS.md:24`. Do not kill it before capturing `ps`, `pmset -g assertions` and the logs.
7. **Exit 0 with warnings at the first full copy.** `fresh backup with warnings` counts as healthy to the tool. Treat it as **not** a verified full copy for step 5 until each warning is explained.
8. **launchd stage.** `bootstrap` errors; the kickstart does not move the counter to 3; generation-3 status is not exit 0; or the launchd log has content beyond benign `open` output.
9. **3.5 reports differences** in files that were not modified after the run's `start`.

---

## 5. Gaps and ambiguities in the docs

1. **"Stage" has no defined mechanism, and the main checkout has none of the files.** r9 item 5 (`astra_r9_verdict.md:13`) says "stage/hash". `HOST_FINDINGS.md:29–35` says merge, then update the main checkout. But `M` is at `557a58b` with no backup files, and `origin/master` holds older status and applet bytes. So staging needs a **second gated merge** (no PR is open) and a fast-forward of the shared checkout. The branch carries 48 commits, including other agents' in-flight work. Whether to merge the whole branch or cut a backup-only PR is MAESTRO's call. The applet then runs whatever bytes sit in `M/tools/` (`MemitGdriveBackup.applescript:2`, `backup_gdrive.sh:12`), so **every later `git pull` in `M` silently changes the production wrapper and status tool**. Nothing re-hashes them per run.
2. **The production app has no pinned hash.** Only the source is pinned (`80c7b712…`). The bundle manifest exists only once built. Step 1.8 adds a manifest re-walk and a decompile spot-check, but that check is my own and has not been reviewed.
3. **Production interpreter ≠ tested interpreter.** The wrapper runs the status tool under `/usr/bin/python3`, which is 3.9.6 (`backup_gdrive.sh:11`). Every suite sets `BACKUP_PYTHON=sys.executable`, which is `.venv` 3.11.16 (`tools/test_backup_gdrive_addendum.py:39,2120`). I confirmed only that the file parses under 3.9 and that the read-only `health()`/`--help` paths run there. `record`, `classify` and `preflight` have **never** run under 3.9. Suggestion before step 3: run a targeted fixture class with `/usr/bin/python3 -B -m unittest tools.test_backup_gdrive_addendum.<Class>`, or set the interpreter explicitly. This is not done and not in the binding order.
4. **"Verified full-copy completion" is undefined.** `astra_r9_verdict.md:13` and `build_report.md:308` ("eventual full-copy verification") do not say what verifies it. I propose generation-2 status exit 0 with no warnings, plus a one-way `rclone check` (3.5). The `--size-only` choice is mine, to avoid hashing 287 GB locally. Confirm it, or ask Astra.
5. **Retirement mechanics are unspecified.** `bootout` alone reloads the old job at next login, because its plist stays in `~/Library/LaunchAgents`. Steps 5.2 and 5.3 add `disable` and an optional move. The old job also writes a ~287 GB mirror to the internal SSD, which CLAUDE.md storage discipline says is not an archive tier; reclaiming it is a separate operator decision.
6. **Orphaned native-test processes.** Two fixture applets, `Native_2.app` (pid 32906, started 12:24 local; pid 36233, started 13:36 local), each with a `held-rclone` stub, have been alive for 1–2.5 h under launchd (ppid 1). They hold `PreventUserIdleSystemSleep "handling Apple event"` assertions. Their HOME is isolated under `/private/tmp/memit_gdrive_native_*`, so real state is untouched, but a host-check helper leaked them and nobody has cleaned them up. The owner should confirm and clean them up (0.3a).
7. **Initial-upload duration is understated.** `HOST_FINDINGS.md:12` says ~69 h and ignores the daytime bwlimit (`backup_gdrive.sh:129`); the estimate here is ~4–4.5 days. The binding order holds launchd installation until this run completes, so there are no scheduled Drive runs for those days. The old job continues, which is consistent with "retire last". The 13 h staleness rule (`backup_gdrive_status.py:604`) means 3.4 has to be read promptly.
8. **Recovery-command interpreter and location.** The docs show `.venv/bin/python -B tools/backup_gdrive_status.py recover …` from the worktree (`build_report.md:550,1027`). This plan runs it from `M` against the staged, hash-checked copy, so the tool that writes recovery state is the same bytes production reads. `M/.venv` exists (3.11). This is my choice; the docs do not specify it.
9. **The status tool has no recovery dry-run.** Step 2.1 replaces one with a manual inventory, and the recovery step is a single shot. Under-lock refusal leaves bytes unchanged, which limits the blast radius.
