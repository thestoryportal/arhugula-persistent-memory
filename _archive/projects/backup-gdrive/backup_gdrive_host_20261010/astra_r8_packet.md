# GPT-6-Astra (high) — re-review r8: Google Drive backup (status tool recovery scan)

Read-only. Worktree = current dir. Your r7 verdict (`results/backup_gdrive_host_20261010/astra_r7_verdict.md`) was NO-GO on one finding, **2 (P2)**. Crash-left publication temporaries escaped both recovery maxima. Your concrete input was corrupt counter, absent unresolved state, completed 10, null-generation receipt, and a surviving `refusals/.last_run.ABC123` with generation 100. Under that input, floor 10 was accepted, 11 was reserved, and completion 12 read healthy. Applet `.launch-receipt.*` / `.journal.*` leftovers had the same gap. You also listed scan limits: nested `recoveries/old/nested/manifest.json`, nested generation fields, and UTF-16 multiline JSONL. Findings 1, 3, 4 and 5 were clean.

The fix is MB24, committed at `dba3a2c`: `git diff f22c9f2 dba3a2c -- tools/backup_gdrive_status.py tools/test_backup_gdrive_addendum.py`. The applet `tools/launchd/MemitGdriveBackup.applescript` and wrapper `tools/backup_gdrive.sh` are byte-unchanged. Read the section "MB24 — Astra r7 finding 2 …" at `results/backup_gdrive_build_report.md:829` onward. Receipts are in `results/backup_gdrive_mb24_20261010T194953Z/`: `red_index.json`, `red_*.log` / `green_final_*.log`, `scope_checks.json`, `source_diff.patch`, `final_sha256.txt`.

## My host evidence, which you cannot reproduce

All of it is in `results/backup_gdrive_mb24_20261010T194953Z/host_runs_maestro21/`, summarized in its README.md. `final_sha256.txt` re-verified 25/25 OK first.
- Real rclone against local temp destinations only: `tools.test_backup_gdrive_addendum` **125 OK, 0 skipped** (r7: 109; MB24 adds 16), plus `tools.test_backup_gdrive` **10 OK**, for 135 OK. Real-path inventory byte-identical before and after (`ec66a1f5…`).
- No native applet run: applet and wrapper bytes are unchanged and MB24 added no native case.

## Check against the code (cite file:line)

1. r7 finding 2 closed. Replay your exact r7 input with the temporary live (`refusals/.last_run.ABC123`, generation 100). Floor 10 must refuse with nothing mutated (no dir, lock, counter, state, receipt or journal change); floor 100 must reserve 101; completion 101 must not read healthy and 102 must. Repeat the replay with the same temporary archived under `recoveries/`. Is every prefix the writers actually create (`.last_run.*` `:228`, `.recovery.*` `:277`, applet `.counter.*` / `.unresolved.*` / `.launch-receipt.*` / `.journal.*` at applescript `:3`, `:6`) enumerated in each live writer directory and recursively under `recoveries/`, in both the pre-lock scan and the under-lock scan? Name any writer temporary, directory or parse path that still escapes.
2. Scan limits. Do nested manifests count, and do nested generation fields, UTF-16 or other unsupported encodings, unknown archive formats, and unparseable archived or temporary payloads each refuse nonzero, naming the file and mutating nothing, rather than being read as absent? Does any refusal path fire on a payload the reviewed writers legitimately produce, so that an ordinary history could never be recovered?
3. Scope. `scope_checks.json` claims byte identity outside `inspect_history`. Confirm it against the diff, and confirm that no r7-clean behavior regressed: the strict `completed > barrier` health rule, both Perl publishers, 64 intervals / 2,048 bytes, `recovery_barrier` retention, owner-preserving exit 75, read-only status, r4 manual-interleave, and generation (not wall-clock) ordering.
4. Anything else that blocks activation. Restate the ordered activation checklist from r7 §6, adjusted for MB24's evidence list (`results/backup_gdrive_build_report.md`, section "Recovery command, updated evidence list and refusal rule").

## Output

Under 700 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the build report, a finding without a named failing input, or "consider adding more tests".
