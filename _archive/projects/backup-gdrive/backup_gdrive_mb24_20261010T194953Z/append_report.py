"""Validate MB24 receipts and append one report section; never run the host suite."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

receipt = Path(__file__).resolve().parent
root = receipt.parents[1]
report = root/"results/backup_gdrive_build_report.md"
status_path = "tools/backup_gdrive_status.py"
tests_path = "tools/test_backup_gdrive_addendum.py"
applet_path = "tools/launchd/MemitGdriveBackup.applescript"
wrapper_path = "tools/backup_gdrive.sh"
start = {path: digest for digest, path in
         (line.split(maxsplit=1) for line in (receipt/"start_sha256.txt").read_text().splitlines())}
digest = lambda data: hashlib.sha256(data).hexdigest()

def original(path):
    result = subprocess.run(["/opt/homebrew/bin/rtk", "proxy", "git", "show", "f22c9f2:"+path],
                            cwd=root, check=True, capture_output=True)
    assert result.stdout, path
    assert digest(result.stdout) == start[path], path
    return result.stdout

old_status = original(status_path)
new_status = (root/status_path).read_bytes()
def scan_span(data):
    function = next(node for node in ast.parse(data).body
                    if isinstance(node, ast.FunctionDef) and node.name == "recover")
    scan = next(node for node in function.body
                if isinstance(node, ast.FunctionDef) and node.name == "inspect_history")
    lines = data.splitlines(keepends=True)
    return b"".join(lines[:scan.lineno-1]), b"".join(lines[scan.end_lineno:])
assert scan_span(old_status) == scan_span(new_status), "changes outside the two-pass scan"
old_tests = original(tests_path)
new_tests = (root/tests_path).read_bytes()
old_prefix, marker, old_suffix = old_tests.partition(b"class R5CompactionTest(R5Fixture):")
new_prefix, new_marker, _inserted = new_tests.partition(b"class R7RecoveryFixture(Fixture):")
assert marker and new_marker and old_prefix == new_prefix
assert new_tests[new_tests.index(marker):] == marker+old_suffix, "existing tests changed"
for path in (applet_path, wrapper_path):
    assert digest((root/path).read_bytes()) == start[path], path
assert digest(report.read_bytes()) == start["results/backup_gdrive_build_report.md"]
assert (receipt/"real_path_listing.py").read_bytes() == (
    root/"results/backup_gdrive_mb21_20261010T191747Z/real_path_listing.py").read_bytes()

writers = []
for number, line in enumerate(new_status.decode().splitlines(), 1):
    for prefix in re.findall(r'mkstemp\(prefix="([^"]+)"', line):
        writers.append((prefix, status_path, number))
for number, line in enumerate((root/applet_path).read_text().splitlines(), 1):
    if line.startswith(("property generationShell : ", "property receiptShell : ")):
        shell = json.loads(line.split(" : ", 1)[1])
        for template in re.findall(r'tempfile\("([^"]+)"', shell):
            assert template.endswith("XXXXXX")
            writers.append((template[:-6], applet_path, number))
assert {prefix for prefix, _path, _line in writers} == {
    ".last_run.", ".recovery.", ".launch-receipt.", ".journal.", ".counter.", ".unresolved."}
assert not re.search(r"\b(?:mktemp|tempfile)\b", (root/wrapper_path).read_text())

red = json.loads((receipt/"red_index.json").read_text())
assert red["scanner_sha256"] == start[status_path]
assert red["test_sha256"] == digest(new_tests)
assert len(red["tests"]) == 16
counts = {"R7PublicationTemporaryTest": 11, "R7ArchivePrecisionTest": 5, "R5RecoveryTest": 9}
for name, count in counts.items():
    log = (receipt/("green_final_"+name+".log")).read_text()
    assert re.search(r"^Ran %s tests in " % count, log, re.M), name
    assert re.search(r"^OK$", log, re.M), name
    assert not re.search(r"^(?:FAILED|ERROR:|FAIL:)|\.\.\. skipped|^OK \(skipped", log, re.M), name
inventories = [receipt/name for name in (
    "real_paths_initial.json", "real_paths_before_final.json", "real_paths_after_final.json",
    "real_paths_before_final2.json", "real_paths_after_final2.json")]
inventory = inventories[0].read_bytes()
assert all(path.read_bytes() == inventory for path in inventories)
inventory_rows = json.loads(inventory)
scope = {"only_inspect_history_changed": True, "existing_tests_byte_identical": True,
         "applet_unchanged": True, "wrapper_unchanged": True, "real_path_listings_identical": True,
         "inventory_sha256": digest(inventory), "inventory_rows": len(inventory_rows),
         "new_tests_with_behavioral_red": 16, "final_targeted_tests": counts,
         "final_skips": 0, "temporary_writers": writers}
(receipt/"scope_checks.json").write_text(json.dumps(scope, indent=2)+"\n")
diff = subprocess.run(["/opt/homebrew/bin/rtk", "proxy", "git", "diff", "--", status_path, tests_path],
                      cwd=root, check=True, capture_output=True)
assert diff.stdout
(receipt/"source_diff.patch").write_bytes(diff.stdout)

relative = receipt.relative_to(root).as_posix()
hash_rows = "\n".join("| `%s` | `%s` | `%s` |" % (path, start[path], digest((root/path).read_bytes()))
                       for path in (status_path, tests_path, applet_path, wrapper_path))
writer_rows = "\n".join("| `%s*` | `%s:%s` |" % row for row in writers)
red_rows = "\n".join("| `%s` | `%s` | %s |" % (
    row["test"], Path(row["red_log"]).name, ", ".join(map(str, row["failure_lines"]))) for row in red["tests"])
green_rows = "\n".join("| `%s` | %s | 0 | `%s/green_final_%s.log` |" % (name, count, relative, name)
                       for name, count in counts.items())
host_script = (receipt/"host_full_addendum_mb24.sh").read_text()
section = f"""

## MB24 — Astra r7 finding 2 publication-temporary / archive scan fix (2026-10-10)

**BUILD DONE; activation remains BLOCKED pending Astra re-review GO.** Worktree `worktree-c10k-route-a`; starting MB21 commit `f22c9f2`. All four supplied start hashes matched before the first source edit. Receipts: `{relative}/`. MB24 ran only the new classes and the explicitly required existing `R5RecoveryTest` (including all five r6 tests); no full suite, native case, rclone, network, install, launchd mutation, commit, push or merge ran.

### Change and scope

Only `recover.inspect_history` changed in the status tool. Both pre-lock and under-lock calls enumerate every known live publication-temporary prefix in the heartbeat directory, its `refusals/` directory, the launch-state directory and the launch-journal directory, plus every file recursively below `recoveries/`. Recursive traversal includes nested manifests and nested temporary files. Heartbeat/receipt/state temporaries are JSON objects; journal temporaries are JSONL; counter temporaries are integers. `.recovery.*` is shared by the counter, unresolved-state and manifest publishers, so it accepts the writer's exact integer format or a JSON object. Temporary evidence is read only and stays at its original path with identical bytes, including after successful recovery.

Unsupported encodings (UTF-16 included), archive file formats, wholly unparseable archived JSON/JSONL, unparseable publication temporaries, non-object archived JSON, invalid generation field types and generation fields nested in objects or arrays refuse with the evidence filename. Known damaged canonical raw counters remain preserved damaged history under the existing operator-reviewed-floor contract; they are never invented into numeric generations. Existing canonical UTF-8 failure journals still retain independently valid records before and after torn lines, as required by the unchanged R5/r6 fixtures. These supported damaged-history forms are distinct from unsupported encodings/layouts. Ordinary null-generation final receipts remain preservable ambiguous evidence.

`scope_checks.json` proves byte identity outside `inspect_history`, byte identity of every existing test, unchanged applet/wrapper hashes, and copied inventory-helper identity. Consequently strict status `completed > barrier`, both Perl publishers, 64 intervals / 2,048 bytes, owner-preserving exit 75, read-only status and r4 manual-interleave code were not edited. The existing MB14 replay, refusal heartbeat and sequenced recovery-boundary tests pass here. Full-suite and native behavior beyond these targeted tests are **HOST-PENDING / not reproduced by MB24**; the MB21 host receipts remain prior host evidence. No applet/wrapper edit was needed, so requirement 4 requires no native-helper copy or new native case.

### Start and final SHA-256

| File | Start | Final |
| --- | --- | --- |
{hash_rows}

The report's start SHA-256 is `{start['results/backup_gdrive_build_report.md']}`. This section is appended only; the existing report prefix is checked byte for byte. Its final digest is in `{relative}/final_sha256.txt`, computed after append to avoid a self-referential report digest. Newly created receipt files start ABSENT; their final digests are in the same file (which excludes itself).

### Actual writer publication-temporary prefixes

| Prefix | Writer file:line |
| --- | --- |
{writer_rows}

These are all six distinct prefixes from the reviewed writers. `tools/backup_gdrive.sh` creates no publication temporary itself; at `:43` it invokes the status publisher, with refusal heartbeat destination selected at `:42`. Both applet state publishers create `.unresolved.*` (`:3` and `:6`). Every prefix is covered live and archived; `.last_run.*` includes both the ordinary heartbeat directory and the exact Astra refusal path `refusals/.last_run.ABC123`. `.recovery.*` has separate raw integer, state-object and manifest-object cases.

### Behavioral RED index and final GREEN

The scanner stayed at the supplied start SHA during both RED runs. `red_index.json` records each new test, every failure line, the baseline scanner hash and the unchanged new-test hash. All 16 new tests have behavioral REDs: 11 temporary tests / 54 failed subcases and 5 archive tests / 7 failed subcases; no import/runtime errors or skips. All fixtures are raw bytes, never outputs from the fixed scanner's helpers.

| New test | Saved RED log | Failure lines |
| --- | --- | --- |
{red_rows}

Final verification: **25 tests OK, 0 skipped** (16 new + 9 existing, including 5 r6). The final source uses the same named UTF-8 rejection helper for payloads and preserved counters; after that diagnostic consistency change, only these same three classes were rerun once. The earlier successful targeted receipts are preserved separately; counts below refer to the final runs, not sums of repeated runs.

| Class | Tests OK | Skips | Final receipt |
| --- | --- | --- | --- |
{green_rows}

Each class ran with this command, substituting the class name:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_NO_RCLONE=1 BACKUP_TEST_RECEIPTS=$PWD/{relative}/fixtures /opt/homebrew/bin/rtk proxy .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.<Class> -v
```

There are 18 live/archive floor pairs, each proving floor 10 refuses without any file/directory/lock mutation and floor 100 reserves counter/barrier 101 while keeping temporary/archive bytes intact. The lock regression injects each of the nine payload/location forms live and archived after the pre-lock scan (18 cases), then proves floor 10 refuses with the entire injected snapshot unchanged. Invalid-temporary coverage adds 18 live/archive cases. Archive tests cover `recoveries/old/nested/manifest.json`, multiline UTF-16 JSONL, nested generation fields in objects and arrays, unknown archive extensions and wholly unparseable JSON/JSONL.

The copied `real_path_listing.py` saved `real_paths_before_final2.json` and `real_paths_after_final2.json`; `cmp` exited 0. SHA-256 of each: `{digest(inventory)}` ({len(inventory_rows)} inventory rows). The initial and first-targeted-run before/after listings also match. Every unittest temporary root was forced below `{relative}/fixtures/`, including cleanup. No protected real-HOME sink was created, changed or removed.

### Recovery command, updated evidence list and refusal rule

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N --heartbeat /absolute/fixture/path/last_run.json
```

N must be operator-reviewed and cover every observed generation from the current raw counter, current unresolved issued state, current heartbeat, current launch receipt, every independently parseable current failure-journal line, current `refusals/latest-refusal.json`, **every known publication temporary in the four live writer directories listed above**, every preserved recovery manifest at any recursive depth, every archived raw counter, every archived JSON/JSONL payload and **every known archived publication temporary**. Older directories count even when newer manifests have lower maxima. Top-level generation fields include launch_generation, issued_generation, recovery_barrier, compaction_barrier, highest_seen and generation_floor. `.journal.*` is parsed line by line and `.counter.*` as an integer; `.recovery.*` supports the publisher's JSON and integer forms.

Both scans use the complete same evidence set. A floor below the observed maximum refuses nonzero with `recovery refused` / `below observed maximum`; the pre-lock refusal creates no directory or lock and changes no bytes. Unsupported temporary/archive encodings, formats or nested generation layouts refuse nonzero and name the file instead of treating it as absent. A higher temporary, archive record or refusal injected between scans refuses under lock without moving or publishing recovery evidence. Crash-left temporary bytes remain exactly in place on refusal and success. Exit 75 remains observed history, not an unresolved backup failure; recovery itself never establishes health, and manual completion/refusal cannot discharge a recovery or compaction barrier. Fixtures must keep explicit `--heartbeat`; operator recovery/activation remains blocked until re-review GO.

### Exact MAESTRO19 host commands and remaining handoff

Run from this worktree once:

```sh
LLMDB_ROOT=$PWD /opt/homebrew/bin/rtk proxy /bin/bash {relative}/host_full_addendum_mb24.sh
```

The script below runs the full addendum suite exactly once, in a fresh local receipt root; it records real-path listings before/after even when tests fail, compares them and returns the test or inventory failure. It deliberately clears the builder-only no-rclone switch for MAESTRO's host local-fixture suite. Expected host count is MB21's 109 addendum tests + 16 new = 125, with 0 skipped; MB24 has not run it. No new native case exists because the applet and wrapper are byte-identical.

```sh
{host_script.rstrip()}
```

Next: MAESTRO19 runs that host command, inspects its logs/inventory equality, and submits final source hashes plus these RED/GREEN/scope receipts to Astra. Activation remains BLOCKED until re-review GO. No source change is half-applied and no targeted test remains failing.

**Binding context directive for this handoff:** watch `Context N% left` for this and every team session. Start a new piece of work only at 60% left or more; at 40% left or less stop starting work, append a handoff with done/in-flight/half-applied state, exact paths and hashes, failing test commands and next step, and reply exactly `CONTEXT HANDOFF WRITTEN`. If `Context compacted` appears, do that immediately. The AGENTS Team mode and Context management sections continue to bind; no commits, real/native runs or out-of-scope edits by the builder. Every successor handoff must restate the directive.
"""
before = report.read_bytes()
with report.open("ab") as stream:
    stream.write(section.encode())
assert report.read_bytes() == before+section.encode()
scope["report_prefix_sha256"] = digest(before)
scope["report_prefix_bytes"] = len(before)
scope["report_final_sha256"] = digest(report.read_bytes())
(receipt/"scope_checks.json").write_text(json.dumps(scope, indent=2)+"\n")
paths = [root/path for path in (status_path, tests_path, applet_path, wrapper_path)] + [report]
paths += [path for path in sorted(receipt.rglob("*")) if path.is_file() and path.name != "final_sha256.txt"]
(receipt/"final_sha256.txt").write_text("".join(
    digest(path.read_bytes())+"  "+path.relative_to(root).as_posix()+"\n" for path in paths))
print("Report appended; 25 final targeted tests OK, 0 skipped; all 16 new tests have RED; inventories identical")
print("Status SHA-256:", digest(new_status))
print("Tests SHA-256:", digest(new_tests))
print("Report SHA-256:", scope["report_final_sha256"])
