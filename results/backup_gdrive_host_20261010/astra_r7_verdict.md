VERDICT: NO-GO

1. none found — **the captured MB14 regression is closed.** Replaying the actual fixture through MB21’s functions with filesystem effects held in memory: floor 11 refused without mutation; floor 100 reserved barrier 101; completions 13 and 101 remained unhealthy; 102 became healthy. Archived bytes remained unchanged. The same scan runs before mkdir/lock and under lock (`tools/backup_gdrive_status.py:296–366`). Independent parsing retains valid journal records before and after torn lines.

2. **P2 — crash-left publication temporaries still escape both maxima.** The wrapper’s publisher writes and fsyncs `.last_run.*` before rename (`tools/backup_gdrive_status.py:228–235`); SIGKILL can bypass cleanup. Recovery enumerates only final live filenames, while archived payloads require `.json`/`.jsonl` suffixes (`:301–303,328–333`).

   Concrete input: corrupt counter, absent unresolved state, completed 10, null-generation receipt, and surviving `refusals/.last_run.ABC123` containing generation 100 from interrupted refusal publication. In-memory replay accepted floor **10**, reserved **11**, and reported completion **12 healthy**. Moving that same evidence to `refusals/latest-refusal.json` makes floor 10 refuse. Applet `.launch-receipt.*` and `.journal.*` leftovers have the same omission (`tools/launchd/MemitGdriveBackup.applescript:6`).

   **Fix:** include known publication-temporary patterns in both scans, live and archived. Parse heartbeat/receipt/state temporaries as JSON, journal temporaries line-by-line, and counter temporaries as integers. Preserve their bytes. Add pre-lock no-mutation and under-lock regressions proving floor 10 refuses and floor 100 reserves 101.

   Additional scan limits: deeper `recoveries/old/nested/manifest.json` is excluded by `:316,329`; nested JSON generation fields and later records in UTF-16 multiline JSONL can escape `:306–338`. Those formats/layouts are not produced by the reviewed writers. Recursive manifest enumeration and explicit rejection of unsupported archive formats would make the advertised coverage precise.

3. none found — **the final refusal heartbeat is now covered.** The specified surviving `latest-refusal.json` generation 100 rejects floor 10 unchanged and accepts floor 100 (`tools/backup_gdrive_status.py:303,352–366`). Injecting it under lock also refuses. Recovery adds no refusal-specific journal failure; its conservative lost-history interval is separate. Ordinary exit 75 preserves the active owner (`tools/backup_gdrive.sh:42–44,53–80`).

4. none found — **strict compaction boundaries are repaired.** Status rejects equality (`tools/backup_gdrive_status.py:475`); both Perl publishers clear only above the barrier (`tools/launchd/MemitGdriveBackup.applescript:3,6`). Extracted functions passed equality/above-boundary checks and 2,000 alternating allocations within 64 intervals/2,048 bytes, retaining `recovery_barrier`. The 11…137/139 schedule and native helper retain barrier 139 during publication 140, clearing it during 141 after completion 140 (`host_launcher_checks_mb21.py:348–374`).

5. none found — inspected r4 manual-interleave, late-generation ordering, refusal/manual barrier retention, owner-preserving exit 75, read-only status, and nested catches (`tools/test_backup_gdrive_addendum.py:1220–1379`; applet `:8–16`). No applet dialog was added. `open -W -g` remains configured (plist `:12–15`); retries, bandwidth and excludes remain unchanged (`tools/backup_gdrive.sh:123–129`).

6. **Activation remains blocked on finding 2.** After correction and re-review, in order: stage/hash reviewed wrapper, status tool and production app; initialize zero only for genuinely fresh history, otherwise recover using an operator-reviewed floor covering all observed generations—including archived payloads, refusal heartbeat and crash temporaries; invoke the production app, grant Allow, await completion and verify sequenced health; install/load the plist, kickstart and verify fresh completion; retire the old job only after verified full-copy completion (`results/backup_gdrive_build_report.md:308,371`; plist `:7`).

All 54 unique pinned files matched. Supplied 119-test receipts, native results and identical inventories were inspected, not reproduced. No files changed.

🌱 graft estimated ~69,019 tokens saved, 1 successful call.

