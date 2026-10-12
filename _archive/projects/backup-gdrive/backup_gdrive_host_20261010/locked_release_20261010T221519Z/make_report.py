"""Assemble the MB32 handoff from saved observations, never invented PASSes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex

RECEIPT = Path(__file__).resolve().parent
ROOT = RECEIPT.parents[2]
before = json.loads((RECEIPT/"before_sha256.json").read_text())
after = json.loads((RECEIPT/"after_sha256.json").read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p,h in after.items())
protected = {p:h for p,h in before.items() if p not in after}
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p,h in protected.items())
green = json.loads((RECEIPT/"green_final/result.json").read_text())
assert not green["success"] and green["failures"] == 1 and green["errors"] == 0
assert green["all_owned_groups_exited"]
processes = json.loads((RECEIPT/"green_final/process_clearance.json").read_text())
command = json.loads((RECEIPT/"green_final/command.json").read_text())
audit_alive = [c for c in processes["observed_children"] if c["alive_after_test"]]
assert len(audit_alive) == 1 and audit_alive[0]["pid"] == command["runner_pid"]
red = json.loads((RECEIPT/"red_verified_original/result.json").read_text())
assert red["testsRun"] == red["failures"] == 14 and red["errors"] == red["skipped"] == 0

tests = [
    ("test_good_release_dispatches_release_path", "1, 3, 5a", "release wrapper path; generation; receipt; exact four-file layout; read-only files/directory"),
    ("test_changed_wrapper_byte_refuses", "3, 5b", "no dispatch; file and expected/actual SHA-256 in receipt"),
    ("test_changed_status_byte_refuses", "3, 5b", "no dispatch; file and expected/actual SHA-256 in receipt"),
    ("test_changed_excludes_byte_refuses", "3, 5b", "no dispatch; file and expected/actual SHA-256 in receipt"),
    ("test_changed_manifest_byte_refuses", "3", "MANIFEST itself is also checked against a compiled stamp"),
    ("test_missing_file_refuses", "3, 5c", "receipt has expected digest and MISSING; generation reserved; no dispatch"),
    ("test_extra_file_refuses", "3, 5c", "receipt has ABSENT and the extra file digest; no dispatch"),
    ("test_checkout_pull_cannot_change_dispatch", "2, 5d", "change fixture checkout after staging; release bytes still dispatch"),
    ("test_existing_release_id_refused_without_overwrite", "2, 5e", "build refuses existing id before compiling; all original release bytes preserved"),
    ("test_dirty_checkout_stages_commit_bytes", "2, 5e", "dirty all three fixture files; git-show commit bytes are staged"),
    ("test_release_inside_another_checkout_refused", "1", "even an unrelated git checkout is refused"),
    ("test_rendered_source_stamps_release_and_all_four_hashes", "2, 3", "rendered wrapper path and all four hashes are stamped"),
    ("test_compiled_app_full_source_equals_saved_source", "2, 5f", "full byte equality with compiled main.scpt source; UNVERIFIED in sandbox"),
    ("test_compiled_app_dispatches_release_after_checkout_change", "5a, 5d", "osascript loads compiled main.scpt after checkout change; UNVERIFIED in sandbox"),
]
rows = []
runs = {}
for name in ["red_new", "red_final", "red_build_id", "green_new", "green_new_final", "red_verified_original", "green_full", "green_final"]:
    result = json.loads((RECEIPT/name/"result.json").read_text())
    completion = json.loads((RECEIPT/name/"tool_completion.json").read_text())
    assert completion["runner_completed"] and completion["exit_code"] == result["exit_code"]
    assert result["all_owned_groups_exited"]
    runs[name] = result
    rows.append(f'| `{name}` | {result["testsRun"]} | {result["failures"]} | {result["errors"]} | {result["skipped"]} | {result["exit_code"]} | {result["direct_process_count"]} |')
changes = {p:{"before_sha256":before.get(p),"after_sha256":h} for p,h in after.items()}
evidence = {"schema":1, "builder":"MB32", "dispatch":"MAESTRO26",
    "status":"STOPPED at operator context gate; final process-auditor false positive remains unfixed",
    "authority":"astra_r10_verdict.md item 1 paragraph 3 and item 5; MB32 operator brief",
    "receipt_dir":str(RECEIPT), "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source_commit_at_start":"57d51f3e2c1db9982c367612a8e55d98592dd2dd",
    "changed_files":changes, "protected_files":{p:{"before_sha256":h,"after_sha256":h} for p,h in protected.items()},
    "red":{"run":"red_verified_original", "tests":14,"failures":14,"errors":0,"skipped":0,"exit_code":1},
    "final":{"run":"green_final","tests":green["testsRun"],"passed":green["testsRun"]-green["failures"]-green["skipped"],
             "failures":green["failures"],"errors":0,"skipped":green["skipped"],"exit_code":1},
    "previous_green":{"run":"green_full","tests":151,"passed":133,"skipped":18,"exit_code":0},
    "runs":runs, "new_tests":[{"test":"LockedReleaseTest."+n,"requirement":req,"evidence":claim} for n,req,claim in tests],
    "skips":green["skips"], "generation_choice":"reserve before checking, for ordered failure receipts and unresolved generation evidence",
    "release_layout":{"default":"$HOME/Library/Application Support/memit-gdrive-backup/releases/<release-id>/",
        "files":["backup_gdrive.sh","backup_gdrive_status.py","backup_mirror.excludes","MANIFEST"],
        "file_mode":"0444", "directory_mode":"0555", "expected_hashes":"compiled AppleScript stamps; MANIFEST never supplies runtime expectations"},
    "process_clearance":{"final_direct_process_count":green["direct_process_count"],
        "observed_child_count":len(processes["observed_children"]),
        "all_owned_groups_exited":True,"all_observed_owned_children_exited":False,
        "auditor_false_positive":audit_alive,
        "ps":"UNAVAILABLE: sandbox-denied", "record":"green_final/process_clearance.json",
        "operator_pids_untouched":processes["operator_pids_not_touched"]},
    "python":{"invoked":"/usr/bin/python3", "version":"3.9.6",
              "resolved_executable":"/Library/Developer/CommandLineTools/usr/bin/python3"},
    "native_claims":"UNVERIFIED; no compiled production app or activation produced",
    "forbidden_actions_performed":[], "test_budget":"small fixtures and evidence only; no bulk backup data"}
(RECEIPT/"evidence.json").write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n")

hash_table = "\n".join(f'| `{p}` | `{before.get(p, "ABSENT")}` | `{h}` |' for p,h in after.items())
protected_table = "\n".join(f'| `{p}` | `{h}` |' for p,h in protected.items())
test_table = "\n".join(f'| `{name}` | {req} | {claim} |' for name,req,claim in tests)
skip_table = "\n".join(f'| `{s["test"].removeprefix("tools.test_backup_gdrive_addendum.")}` | '+
    ("HOST-PENDING: real rclone forbidden" if s["reason"].startswith("HOST-PENDING") else "UNVERIFIED: Standard Additions XPC sandbox failure, independently confirmed")+" |" for s in green["skips"])
commands = []
for name in ["red_verified_original", "green_final"]:
    command=json.loads((RECEIPT/name/"command.json").read_text())
    commands.append("```sh\n"+"LLMDB_ROOT=\"$PWD\" "+shlex.join(command["argv"])+"\n```")
report = f'''# MB32 locked Google Drive backup release

STOPPED at the operator's 38% context gate. Final Python 3.9.6 suite: **{green["testsRun"]} run, {green["testsRun"]-green["failures"]-green["skipped"]} passed, 1 clearance-auditor failure, {green["skipped"]} skipped, zero errors; exit 1**. The earlier full GREEN was **151 run, 133 passed, 18 skipped; exit 0**. The final run's test-method assertions all passed; the recorder added one failure after a status test deliberately used the runner's own PID as a synthetic child. This is an unfixed observation-layer defect, so the final run is not accepted as GREEN. All 14 new tests were RED against original production bytes before implementation. The final test definitions were also rerun against the saved original launcher: **14 failures, zero errors/skips; exit 1**. Native compilation, app execution and full decompile comparison remain **UNVERIFIED**, with every skip listed below for MAESTRO host rerun. No activation or production app was created.

Authority: [Astra r10](../astra_r10_verdict.md), item 1 third paragraph and item 5, plus the MB32 brief. This is backup infrastructure hardening supporting durable research evidence, not scientific evidence or an F1 closure. Other r10 items belong to the later builder.

## Design and release layout

`stage_gdrive_release.sh <git-commit> <release-id> <rendered.applescript> [release-root]` resolves the commit once, extracts each of the three payload files with `/usr/bin/git show <resolved-commit>:tools/<file>`, computes the MANIFEST, and stamps the template. The three files never come from the working tree. It resolves release-root symlinks and refuses a `.git` ancestor in any checkout/worktree, including an unrelated checkout. An exclusive directory reservation refuses reuse of an existing release id. A failed staging/build is kept for inspection and requires a fresh id for another attempt.

```text
$HOME/Library/Application Support/memit-gdrive-backup/releases/<release-id>/  (0555)
  backup_gdrive.sh         (0444)
  backup_gdrive_status.py  (0444)
  backup_mirror.excludes   (0444)
  MANIFEST                (0444; SHA-256 of the preceding three named files)
```

Exactly these four entries are allowed. `build_gdrive_applet.sh <git-commit> <release-id> <output.app> [release-root]` calls the stager, canonicalizes rendered source through a temporary compiled script, then compiles the app **from the exact saved canonical source** `<output.app>.applescript`. It decompiles the bundle's `Contents/Resources/Scripts/main.scpt` into `<output.app>.decompiled.applescript` and runs `/usr/bin/cmp` over both full files. Those sidecars become read-only. The builder also prints a SHA-256 inventory of every bundle file through one checked Perl process, avoiding hidden pipeline/find-exec failures. Its interface now requires the commit and release id; MAESTRO must update activation invocations accordingly. The staged release stays outside checkouts; keep the reviewed app and its source sidecars outside pullable checkouts as well.

The compiled applet contains the absolute release wrapper path and four expected SHA-256 values (all payload files plus MANIFEST). Each run uses system `/usr/bin/perl` with Digest::SHA to hash them and check the complete entry set; `PERL5LIB` and `PERL5OPT` are cleared for this check. The gate never derives its expectations from MANIFEST at runtime. Missing, altered, unreadable, nonregular or symlink files, an extra entry, or a failed checker suppress dispatch. Receipt `integrity_failures` contains the offending filename, `expected_sha256` and `actual_sha256`; absent/unreadable objects use explicit sentinels such as `MISSING`, and extra files use expected `ABSENT`. Integrity refusals have exit code 78 and use the existing launch receipt and failure journal mechanisms. Files are read-only after staging; this is not protection against the owner deliberately changing permissions and racing a run.

## Generation choice

**Reserve the generation before the integrity check.** Every integrity refusal can then publish a sequenced failure receipt at `$HOME/Library/Logs/memit-gdrive-backup/launch_receipt.json`, with the existing independent failure journal and unresolved-generation behavior. This prevents a fresh old heartbeat from silently hiding the failed launch. Allocation failure remains fail-closed through the existing caught error boundary. Hashing still occurs before any wrapper dispatch, and a mismatch never reaches the wrapper. The wrapper and status tool remain byte-identical, including their existing generation semantics.

## New tests to requirements

All rows belong to `LockedReleaseTest` in `tools/test_backup_gdrive_addendum.py`. Shell tests obtain dispatch composition from the actual applet source and execute the same literal sequence with stamped fixture paths. Native tests load the compiled bundle's `main.scpt`. All use tiny committed fixture payloads; no real rclone or Drive.

| New test | Requirement | What is checked |
|---|---|---|
{test_table}

The existing launcher smoke and builder tests were adapted to the new template/build interface while keeping their error-boundary and complete bundle-hash assertions.

## Runs, commands and process clearance

Every run has `command.json`, `test.log`, `result.json`, `tool_completion.json`, `started_processes.jsonl`, `process_clearance.jsonl` and `process_clearance.json`. Each command and its actual exit code are preserved. The initial failed GREEN attempt is retained: a Perl literal placeholder regex did not match; a minimal probe reproduced it, and using a variable placeholder corrected it. The first full GREEN run preceded the final native script-file path correction and the extra fixture/child evidence capture; `green_final` verifies the final bytes.

| Run | Tests | Failures | Errors | Skips | Exit | Direct processes |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Exact final RED and GREEN commands (the runner creates an isolated HOME and refuses reuse of a run directory):

{chr(10).join(commands)}

The suite is invoked with `/usr/bin/python3 -B` (3.9.6); macOS resolves that shim to `/Library/Developer/CommandLineTools/usr/bin/python3`, which is also `sys.executable` used by fixture helpers. `HOME`, `LLMDB_ROOT`, `BACKUP_TEST_NO_RCLONE=1`, `PYTHONDONTWRITEBYTECODE=1`, `BACKUP_TEST_RECEIPTS` and the Python settings are recorded in each command receipt. Release/native fixture HOMEs are under `/private/tmp`, because a receipt-dir HOME in this worktree would itself be inside a git checkout. Other safe fixtures use receipt-dir HOMEs. No tests write the real `~/Library` or `~/Applications`.

Final clearance: **{green["direct_process_count"]} directly started process leaders, all reaped, every owned process group absent**. The recorder contains {len(processes["observed_children"])} observed child records: all except one were absent at their checks. The one marked alive is PID {command["runner_pid"]}, which `command.json` identifies as the runner itself. The status test deliberately paired that PID with a dead subprocess PID; the recorder trusted that synthetic heartbeat as ownership proof. The runner then exited 1, corroborated by `tool_completion.json`. No real child leak was shown, but the child-auditor result remains failed and must be repaired/reverified. Each test uses dedicated process sessions and is failed if its leader/group remains alive after cleanup; only its own group can be killed for failed-test containment. Group absence also covers shell/Perl/Python descendants whose transient PIDs are not separately enumerated. `/bin/ps` is sandbox-denied (UNAVAILABLE, not an idle claim). Operator-owned PIDs 32906, 32913, 32914, 36233, 36258, 36259, 37109 and 65807 were never targeted. No `open`, real rclone, Drive, launchctl, commits, pushes, merges, or deletions outside receipt/temp directories were performed.

`green_final/fixture_artifacts/<test>/` preserves the actual fixture receipts, counters, dispatched path markers, rendered AppleScripts and release snapshots before temporary directories are cleaned. These copies are evidence only; their temporary release paths are not deployment paths. Full skip diagnostics and positive-control output are in `green_final/result.json` and `test.log`.

## Every skip ({green["skipped"]})

| Test | Status / reason |
|---|---|
{skip_table}

The 14 HOST-PENDING real-rclone skips are required by the no-rclone scope. The four native skips independently confirm the unavailable Standard Additions XPC service with a system `osascript` positive control; host compilation/execution/source equality is not claimed. MAESTRO reruns these tests on the host with the same isolation and process-clearance runner before activation review.

## Before and after SHA-256

`before/` holds the original copies of each existing changed file. The new helper is represented by `before/tools/launchd/stage_gdrive_release.sh.ABSENT`. The recorded hashes were rechecked after intervening operations.

| Changed file | Before SHA-256 | After SHA-256 |
|---|---|---|
{hash_table}

| Protected file (unchanged before/after) | SHA-256 |
|---|---|
{protected_table}

Shell syntax checks and scoped `git diff --check` passed; observations are in `preflight_checks.json`. All counts and hashes above are also in `evidence.json`. No other source file was edited; MB31's NEW1 receipt tree and `tools/test_dashboard_mathlab.py` were left alone.

## Context saved / MAESTRO handoff

Done: commit-only staging, stamped per-run integrity gate, full-source comparison build, 14 test-first release tests, unchanged pinned payloads, original-byte RED logs, one full GREEN run and the final failed audit run, actual fixture receipts/source snapshots, process records and this handoff. Half-applied: no partial production edits; the receipt runner's child-observation enhancement is applied but has the false positive described above and is not accepted. In flight: none; the final runner exited 1. Implementation and tests stopped immediately on the operator's 38% context instruction; no new tests or fixes were started afterward.

Changed files and current SHA-256 (absolute paths):

{chr(10).join('- `'+str(ROOT/p)+'` — `'+h+'`' for p,h in after.items())}

Unfinished receipt runner: `{RECEIPT}/run_suite.py`; SHA-256 `{hashlib.sha256((RECEIPT/'run_suite.py').read_bytes()).hexdigest()}`. Evidence and report writer: `{RECEIPT}/make_report.py`. The script-file path correction is final; all source hashes match `green_final/source_sha256.json`.

Failing test: `tools.test_backup_gdrive_addendum.StatusTest.test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs`, added by `ClearedResult.stopTest` in the receipt runner, with synthetic child PID {command["runner_pid"]} equal to the runner PID. Full exact failed command (cwd `{ROOT}`):

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py green_final all
```

Next step for a fresh successor: reproduce the child-auditor error with a new run id, exclude the runner PID and validate actual live owned-group membership before classifying a heartbeat PID as an owned child, then rerun the targeted case and the full suite in new run directories. Preserve the failed evidence. Exact targeted reproduction command:

```sh
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py clearance_fix_red StatusTest.test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs
```

After that repair, use `clearance_fix_green` for the targeted GREEN and `green_success all` for full verification. Update README/evidence with their actual counts/exit codes. MAESTRO then owns the listed host reruns and Astra re-review before any separately authorized activation. Keep wrapper/status bytes pinned; do not touch MB31's receipt tree or `tools/test_dashboard_mathlab.py`. Open risks: child-auditor ownership validation unfinished; native compilation/execution/full source equality still UNVERIFIED; no activation authorization is inferred.

Binding context directive: watch "Context N% left" for this session and every orchestrated session. Start a new piece of work only at 60% left or more. At 40% left or less, or any "Context compacted", stop starting work, write a handoff at the end of this README with done/half-applied work, exact paths and SHA-256 of changed files, failing tests and exact commands, and the next step; reply exactly "CONTEXT HANDOFF WRITTEN". Preserve this directive in every successor handoff.
'''
(RECEIPT/"README.md").write_text(report)
(RECEIPT/"context_saved.md").write_text(f'''---
status: stopped-context-handoff
branch: worktree-c10k-route-a
timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}
---

# Locked backup release context

MB32 stopped at the operator's 38% context gate with evidence in `{RECEIPT}`. Read the final README handoff and evidence.json for paths/hashes, results, skips and commands. Production wrapper/status hashes are unchanged. All directly owned test groups exited; the final child audit falsely classified the runner's PID from a synthetic heartbeat and failed one test. No process or partial production edit is in flight. A fresh successor must fix/reverify the receipt runner before MAESTRO host reruns, Astra re-review and separately authorized activation. This context-save is in the authorized receipt directory; global gstack context/telemetry paths were not written.

Binding context directive: watch "Context N% left" for this and every orchestrated session; start new work only at >=60% left; at <=40% or any "Context compacted", stop starting work, append the exact handoff (done, half-applied, paths/hashes, failing commands, next step) to README.md and reply exactly "CONTEXT HANDOFF WRITTEN". Restate this directive in every handoff.
''')
print(json.dumps({"receipt":str(RECEIPT),"red":14,"green_passed":green["testsRun"]-green["skipped"],
                  "green_run":green["testsRun"],"skips":green["skipped"],"processes":green["direct_process_count"],
                  "observed_children":len(processes["observed_children"])},indent=2))
