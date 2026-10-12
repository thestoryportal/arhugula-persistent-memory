# GPT-6-Astra (high) — re-review r9: Google Drive backup (status tool recovery scan)

Read-only. Worktree = current dir. Your r8 verdict (`results/backup_gdrive_host_20261010/astra_r8_verdict.md`) was NO-GO on two P2 findings. **Finding 2:** current `unresolved.json` was read separately (`tools/backup_gdrive_status.py:297–303` at r8) and skipped nested-generation validation. Your input was a corrupt counter, completed 10, a null-generation receipt, and `{"schema":1,"issued_generation":10,"unresolved":[],"recovery_barrier":null,"x":{"launch_generation":100}}`. Floor 10 was accepted, 11 reserved, the nested evidence overwritten, and completion 12 read healthy. **Finding 3:** ordinary `json.loads` kept the last duplicate key, so `recoveries/old/x.json` = `{"launch_generation":100,"launch_generation":10}` erased generation 100, with the same outcome. Findings 1, 4 and 5 were clean.

The fix is MB25, committed at `a72f638`: `git diff dba3a2c a72f638 -- tools/backup_gdrive_status.py tools/test_backup_gdrive_addendum.py`. The applet `tools/launchd/MemitGdriveBackup.applescript` and wrapper `tools/backup_gdrive.sh` are byte-unchanged. Read the section "MB25 — Astra r8 findings 2 and 3 …" at `results/backup_gdrive_build_report.md:962` onward. Receipts are in `results/backup_gdrive_mb25_20261010T202206Z/`: `red_index.json`, `red_*.log` / `green_*.log`, `scope_checks.json`, `source_and_tests.diff`, `final_sha256.txt`.

## My host evidence, which you cannot reproduce

All of it is in `results/backup_gdrive_mb25_20261010T202206Z/host_runs_maestro23/`, summarized in its README.md. `final_sha256.txt` re-verified 33/33 OK first.
- My rerun of the new classes (builder env, no rclone): R8CurrentUnresolvedTest 4 OK, R8DuplicateKeysTest 8 OK.
- Real rclone against local temp destinations only: `tools.test_backup_gdrive_addendum` **137 OK, 0 skipped** (r8: 125; MB25 adds 12), plus `tools.test_backup_gdrive` **10 OK**, for 147 OK. Real-path inventory byte-identical before and after (`ec66a1f5…`, same as MB24).
- No native applet run: applet and wrapper bytes are unchanged and MB25 added no native case.

## Check against the code (cite file:line)

1. r8 finding 2 closed. Replay your exact r8 finding-2 input. Floor 10 must refuse nonzero, naming `unresolved.json`, with nothing mutated (no dir, lock, counter, state, receipt or journal change, and the `unresolved.json` bytes preserved). Floor 100 must reserve 101; completion 101 must not read healthy and 102 must. Does the same validation (encoding, nested generation fields, generation-field type) now apply to current unresolved state in BOTH the pre-lock and under-lock scans, before any mutation? Name any other current-state file read outside `observe()` that still escapes.
2. r8 finding 3 closed. Replay `recoveries/old/x.json` = `{"launch_generation":100,"launch_generation":10}`, and the same duplicate inside a recognized JSON temporary, a JSONL line, a live state file and a nested object. Each must refuse nonzero naming the file, mutating nothing. Is duplicate-key rejection kept distinct from the tolerated torn-JSONL-line path, so that a duplicate on a JSONL line cannot be swallowed as "torn"? Does any refusal fire on a payload the reviewed writers (both Perl publishers, the applet, `backup_gdrive.sh`) legitimately produce, so that an ordinary history could never be recovered?
3. Scope. `scope_checks.json` claims byte identity outside the changed functions. Confirm against the diff and that no r8-clean behavior regressed: r7's temporary-file closure (live and archived), recursive manifests, UTF-16/unknown-format/unparseable refusals, the strict `completed > barrier` health rule, 64 intervals / 2,048 bytes, `recovery_barrier` retention, owner-preserving exit 75, read-only status, r4 manual-interleave, and generation (not wall-clock) ordering.
4. Anything else that blocks activation. Restate the ordered activation checklist from r8 §6, adjusted for MB25's evidence list (`results/backup_gdrive_build_report.md`, MB25 section, "Recovery command, updated evidence list and refusal rule").

## Output

Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the build report, a finding without a named failing input, or "consider adding more tests".
