VERDICT: NO-GO

1. none found — **the original r5 torn-journal case is closed.** At `tools/backup_gdrive_status.py:327–360`, independent parsing retains valid generations before and after torn lines. Replaying actual functions with filesystem effects mocked in memory: floor 10 refused without mutations; floor 100 reserved barrier 101; completions 12 and 101 remained unhealthy; 102 became healthy. Archived bytes matched. Counter, issued state, heartbeat, receipt, journal and manifest maxima each triggered pre-lock refusal; an injected higher generation triggered the under-lock recheck.

2. **P1 — recovery misses failures already archived by the vulnerable version.** `tools/backup_gdrive_status.py:314–319` reads only archived manifests. Concrete replay: run MB14 recovery on failure 100 followed by `{torn`, with floor 10. It preserves that journal but records highest 10/barrier 11. Feed its actual output into MB20: floor 11 succeeds, reserves 12, and completion **13 reports healthy**, although archived failure **100** remains unacknowledged.

   **Fix:** inspect preserved evidence inside recovery directories, including independently parsed journal lines and archived counter/heartbeat/receipt generations, in both history checks. Preserve bytes. Add this MB14→MB20 regression: floor 11 must refuse unchanged; floor 100 must establish barrier 101.

3. **P2 — another observed-generation source is omitted.** `tools/backup_gdrive.sh:42–44` publishes generation-bearing `refusals/latest-refusal.json`; the recovery evidence list at `tools/backup_gdrive_status.py:301–302` excludes it. With corrupt counter, absent unresolved state, completed 10, null-generation receipt and surviving refusal generation **100**, MB20 accepts floor **10**.

   **Fix:** include that refusal heartbeat’s valid generation in both maximum calculations. Add a no-mutation refusal test. This violates the reviewed-floor rule even though exit 75 itself is not an unresolved backup failure.

4. **P2 — compaction does not require completion strictly above its barrier.** `tools/backup_gdrive_status.py:469` accepts equality; both applet publishers at `tools/launchd/MemitGdriveBackup.applescript:3,6` clear with `completed >= compaction_barrier`. Concrete schedule: failed odd generations 11…137, intervening even refusals, then allocation 139 creates interval 65 and compacts to barrier **139**. Completion **139** reports healthy and clears the barrier. I reproduced both reader acceptance and both extracted Perl clear operations.

   **Fix:** require `completed > barrier` in both publishers and reject `completed <= barrier` in status; reverse the equality expectation at `tools/test_backup_gdrive_addendum.py:1561–1564`. This is a strict-boundary contract mismatch, not demonstrated loss of a higher failure.

   Otherwise, none found: Python recovery publication and both Perl publishers enforce 64 intervals/2,048 bytes. Both extracted implementations stayed bounded through 2,000 alternating allocations, retained `recovery_barrier`, and did not let refusal or manual completion discharge barriers.

5. none found — inspected r4 manual-interleave, late generation 11 versus failure 12, owner-preserving exit 75, read-only status, nested error catches, and generation ordering (`tools/backup_gdrive_status.py:465–494`; applet `:3,6,8–16`; wrapper `:40–80`). Manual completion retained unresolved 11. `open -W -g` remains configured (`tools/launchd/com.rhu.memit-gdrive-backup.plist:12–15`); OS privacy prompts remain possible. Retries, bandwidth and excludes are unchanged (`tools/backup_gdrive.sh:123–129`).

6. **Activation remains blocked on 2–4.** After fixes and re-review: stage/hash reviewed wrapper, status tool and production app; provision counter zero only for genuinely fresh history, otherwise recover with an operator-reviewed floor covering **every observed generation**, including preserved evidence; invoke the production app, click Allow, await completion and verify sequenced health; install/load the plist, kickstart and verify fresh completion; retire the old job only after verified full-copy completion (`results/backup_gdrive_build_report.md:308,371`; plist `:7`).

All 41 manifest hashes matched. Supplied 113-test receipts, native results and identical inventories were inspected, not reproduced. No files changed.

