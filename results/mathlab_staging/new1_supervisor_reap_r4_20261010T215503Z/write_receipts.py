"""Derive MB31's reviewable receipts from saved logs; never runs tests."""
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess

R = Path(__file__).resolve().parent
W = R.parents[2]
E = json.loads((R / "evidence.json").read_text())
IGNORED = [
    "tools/launchd/MemitGdriveBackup.applescript",
    "tools/launchd/build_gdrive_applet.sh",
    "tools/launchd/stage_gdrive_release.sh",
    "tools/test_backup_gdrive_addendum.py",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_log(path):
    content = path.read_text()
    summary = re.search(r"^Ran (\d+) tests in ([0-9.]+)s$", content, re.M)
    outcome = re.search(r"^(OK(?: \(.*\))?|FAILED \(.*\))$", content, re.M)
    if summary is None or outcome is None:
        raise RuntimeError(f"Missing unittest summary: {path}")
    headers = list(re.finditer(r"^(FAIL|ERROR): (.+)$", content, re.M))
    records = []
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(content)
        block = content[header.end():end]
        assertion = re.search(r"^AssertionError: .+$", block, re.M)
        name = re.fullmatch(r"(\w+) \(([^)]+)\)(?: (.*))?", header.group(2))
        if name is None:
            raise RuntimeError(f"Unrecognized failure identity: {header.group(2)}")
        records.append({
            "kind": header.group(1), "full_failure_identity": header.group(2),
            "test_method": name.group(1), "qualified_test_name": name.group(2),
            "subtest": name.group(3) or "",
            "assertion_text": assertion.group() if assertion else "NO ASSERTION: " + block.strip(),
            "assertion_log_line": (content.count("\n", 0, header.end() + assertion.start()) + 1)
                if assertion else None,
            "failure_header_log_line": content.count("\n", 0, header.start()) + 1,
        })
    counts = {key: int(value) for key, value in re.findall(r"(failures|errors|skipped)=(\d+)", outcome.group())}
    return {"tests_run": int(summary.group(1)), "seconds": float(summary.group(2)),
            "summary": summary.group(), "outcome": outcome.group(),
            "failures": counts.get("failures", 0), "errors": counts.get("errors", 0),
            "skipped": counts.get("skipped", 0), "failure_records": records}


red = parse_log(R / "RED_causal_final.log")
green = parse_log(R / "GREEN_receipt.log")
strengthened = parse_log(R / "RED_strengthened.log")
red_names = {row["full_failure_identity"] for row in red["failure_records"]}
old_names = {row["full_failure_identity"] for row in strengthened["failure_records"]}
methods3 = {
    "test_resource_release_preserves_control_after_interrupted_poll": "r11 sequence 1: waitpid succeeds, SIGINT before returncode, group signal denied",
    "test_resource_release_preserves_control_from_heartbeat_cleanup": "r11 sequence 2: STOPPED-RESOURCE heartbeat, group signal denied, PID signal raises control",
}
expected3 = {(method, f"(boundary='{boundary}', control='{control}')")
             for method in methods3 for boundary in ("selector", "stdout", "stderr")
             for control in ("KeyboardInterrupt", "SystemExit")}
actual3 = set()
for row in red["failure_records"]:
    method = row["test_method"]
    text = row["assertion_text"]
    row["causal"] = row["kind"] == "FAIL" and text.startswith("AssertionError:")
    if method in methods3:
        row["requirement"] = 3
        row["coverage"] = methods3[method] + "; selected close raises OSError; preserve original control (SystemExit code 17)"
        row["causal"] = row["causal"] and "None is not " in text and "returned 'INVALID-WORKER'" in text
        actual3.add((method, row["subtest"]))
        row["classification"] = "Causal control loss" if row["causal"] else "NON-CAUSAL requirement-3 failure"
    elif method == "test_resource_release_precedence_and_unmasked_release_error":
        row["requirement"] = 1
        row["coverage"] = "ordinary Stop versus ordinary close error" if "original=" not in row["subtest"] else "original control versus different release control"
        row["causal"] = row["causal"] and ("'INVALID-WORKER' != 'STOPPED-RESOURCE'" in text or "release control replaced the original control exception" in text)
        row["classification"] = "Causal precedence failure" if row["causal"] else "NON-CAUSAL precedence failure"
    elif method == "test_supervise_resource_acquisitions_share_precedence_owner":
        row["requirement"] = 2
        row["coverage"] = "AST ownership guard: 24 unmanaged boundary/acquisition/ownership findings on old source"
        row["causal"] = row["causal"] and "Lists differ:" in text and "unreviewed call/acquisition" in text
        row["classification"] = "Expected structural RED; not a control-loss assertion"
    else:
        row["requirement"] = "OTHER"
        row["coverage"] = "Unexpected failure"
        row["causal"] = False
        row["classification"] = "NON-CAUSAL / unclassified"

for phase, parsed in (("red", red), ("green", green)):
    E["runs"][phase].update(parsed)
    record = E["runs"][phase]
    if int((R / record["exit_file"]).read_text()) != record["exit_code"]:
        raise RuntimeError(f"Saved exit code mismatch: {phase}")
    if sha(R / record["log"]) != record["log_sha256"]:
        raise RuntimeError(f"Captured log changed: {phase}")
    fixture_log = Path(record["inherited_environment"]["NEW1_RECEIPT_TMPLOG"])
    roots = [json.loads(line) for line in fixture_log.read_text().splitlines()]
    record["fixture_root_count"] = len(roots)
    record["fixtures_confined_to_copy"] = all(Path(row["allocated_dir"]).is_relative_to(Path(E["copy_dir"])) for row in roots)
    record["isolated_bytecode_prefix_remained_absent"] = not Path(record["inherited_environment"]["PYTHONPYCACHEPREFIX"]).exists()

diffs = {}
for before, after, filename in (("before/new1_supervisor.py", "tools/new1_supervisor.py", "supervisor.diff"),
                                ("before/test_new1_supervisor.py", "tests/test_new1_supervisor.py", "tests.diff")):
    argv = ["diff", "-u", before, str(W / after)]
    result = subprocess.run(argv, cwd=R, capture_output=True)
    if result.returncode != 1 or not result.stdout or result.stderr:
        raise RuntimeError(f"Unexpected diff result for {filename}: {result.returncode}, {result.stderr!r}")
    (R / filename).write_bytes(result.stdout)
    diffs[filename] = {"cwd": str(R), "exact_command": shlex.join(argv), "exit_code": result.returncode, "sha256": sha(R / filename)}

source = (W / "tools/new1_supervisor.py").read_text()
function = next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == "supervise")
owned_sites = sorted((node.lineno, ast.unparse(node.args[0])) for node in ast.walk(function)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    and isinstance(node.func.value, ast.Name) and node.func.value.id == "resources"
    and node.func.attr in ("context", "acquire_many"))
acquisitions = [
    ("432", "Path(run_dir)", "Path value only; no retained OS handle; before any worker."),
    ("433", "Run directory creation", "Persistent output namespace; no retained handle and no directory deletion."),
    ("435", "Controller", "Clock/monitor/path state (constructor at :200); no closable resource."),
    ("441", "Single ResourceOwner", "One LIFO entry list; scopes drain portions; final drain at :629."),
    ("442", "socket.socketpair: parent and child endpoints", "acquire_many registers both close callbacks (:385-389); child early release at :534; parent/root leftovers drain at :629. Failed early child release remains registered for final cleanup."),
    ("507", "worker_lifetime context", "Registered before worker allocation; ResourceOwner invokes __exit__; cleanup :448-487 kills/signals and waits for owned worker, with REAP_TIMEOUT_S=5."),
    ("508", "Whole-run hard_deadline context", "Owned __exit__ restores timer/handler (:99); LIFO removes alarm before worker_lifetime performs separately bounded reaping."),
    ("526", "worker_stdout.log open('xb')", "context stores the manager before __enter__; __exit__/close through _release when :525 scope drains."),
    ("527", "worker_stderr.log open('xb')", "Same owner path as stdout; LIFO closes stderr before stdout at the :525 scope boundary."),
    ("529", "Preallocated subprocess.Popen handle", "Assigned to process before __init__; the previously registered worker_lifetime owns its eventual PID, even if construction raises after spawning."),
    ("531", "constructor_ownership signal-handler context", "Owned __exit__ restores handlers and delivers deferred signals (:281-310); drained by the :530 owner scope."),
    ("532", "Worker created by subprocess.Popen.__init__ (call continues at :533)", "Previously registered worker_lifetime kills/signals and waits; Popen's internal constructor resources retain stdlib ownership."),
    ("536", "selectors.DefaultSelector context / selector backend", "Owned __exit__ calls close through _release; the :535 scope exits before log scopes, while retaining the governing exception."),
    ("463", "worker_reaping signal-mask context inside worker_lifetime", "Owned __exit__ restores the prior mask (:314-323); :462 scope drains after bounded wait, using the same release precedence."),
    ("617", "Halt-durability hard_deadline context", "Owned __exit__ restores timer/handler; :616 scope drains within the existing remaining budget."),
    ("462, 506, 525, 530, 535, 616", "resources.scope() context values / stack markers", "Borrow the same owner; scope records a marker and drains entries after it through close/_release (:421-428). No independent resource owner."),
    ("570", "path.read_text() artifact read", "Helper owns its temporary file internally; returns text, no retained handle in supervise."),
    ("576", "Path.glob iterator consumed by list()", "Directory iteration is consumed locally; returns a count, no retained lifetime resource."),
    ("509, 514, 516, 517, 520, 573, 576, 586, 588, 589, 591, 593, 618, 621", "emit/receipt/publish_predictions/durable_json helper I/O", "Helpers return data/receipt/publication values; transient file/directory handles remain internal to those reviewed helpers. These calls are allowlisted, not recursively audited by this guard."),
    ("522, 538, 556, 567, 570, 589, 590", "Environment, buffer, parsed data, path and receipt/publication values", "In-memory state/metadata; no independent close callback. The terminal publication is captured at :491 and verified at :602."),
]
precedence = [
    ("None", "None", "Continue normally."),
    ("None", "Ordinary exception", "Propagate the release exception from the owner."),
    ("None", "KeyboardInterrupt / SystemExit", "Propagate that control exception."),
    ("Ordinary exception (including worker error / Stop)", "None", "Preserve the original exception."),
    ("Ordinary exception", "Ordinary exception", "Preserve original; add a release-failure note."),
    ("Ordinary exception", "KeyboardInterrupt / SystemExit", "Release control wins under the existing table; add prior-exception note."),
    ("KeyboardInterrupt / SystemExit", "None", "Preserve the same original control object and SystemExit code."),
    ("KeyboardInterrupt / SystemExit", "Ordinary exception", "Preserve original control; add release-failure note."),
    ("KeyboardInterrupt / SystemExit", "KeyboardInterrupt / SystemExit", "Preserve first control object/code; add release-failure note."),
]
def test_names(path):
    return {node.name for node in ast.walk(ast.parse(path.read_text()))
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")}

before_tests = test_names(R / "before/test_new1_supervisor.py")
after_tests = test_names(W / "tests/test_new1_supervisor.py")
current_scope = {str(path.relative_to(W)): sha(path) for folder in ("tools", "tests")
                 for path in sorted((W / folder).rglob("*")) if path.is_file()}
baseline_scope = {key: value for key, value in E["worktree_scope_before"].items() if key not in IGNORED}
final_scope = {key: value for key, value in current_scope.items() if key not in IGNORED}
hashes = {
    "before": {str(path.relative_to(R)): sha(path) for path in sorted((R / "before").glob("*.py"))},
    "after": {name: sha(W / name) for name in ("tools/new1_supervisor.py", "tests/test_new1_supervisor.py", "tools/test_dashboard_mathlab.py")},
    "saved_test_copies": {str(path.relative_to(R)): sha(path) for path in sorted(R.glob("*tests.py"))},
    "other_saved_source_copies": {"GREEN_first_supervisor.py": sha(R / "GREEN_first_supervisor.py")},
    "isolated_run_files": {str(Path(E["copy_dir"]) / name): sha(Path(E["copy_dir"]) / name)
                           for name in ("tools/new1_supervisor.py", "tests/test_new1_supervisor.py")},
}
hashes["saved_test_copies"]["before/test_new1_supervisor.py"] = hashes["before"]["before/test_new1_supervisor.py"]
brief = Path("/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexmb29_r4_prompt.txt")
E.update({
    "authorities": {str(brief): sha(brief), "results/mathlab_staging/new1_supervisor_reap_astra_r12.md": sha(W / "results/mathlab_staging/new1_supervisor_reap_astra_r12.md")},
    "hashes": hashes, "diffs": diffs,
    "failure_set_comparison": {"comparison_log": "RED_strengthened.log", "matches": red_names == old_names,
        "identity_includes_subtest_parameters": True, "fresh_count": len(red_names), "strengthened_count": len(old_names),
        "only_fresh": sorted(red_names - old_names), "only_strengthened": sorted(old_names - red_names),
        "failing_methods": sorted({row["test_method"] for row in red["failure_records"]})},
    "failure_classification": red["failure_records"],
    "failure_counts_by_requirement": dict(Counter(str(row["requirement"]) for row in red["failure_records"])),
    "requirement_3": {"expected_failure_rows": len(expected3), "observed_failure_rows": len(actual3),
        "missing_or_passing_rows": sorted(expected3 - actual3), "unexpected_rows": sorted(actual3 - expected3),
        "all_fail_for_control_loss": all(row["causal"] for row in red["failure_records"] if row["requirement"] == 3),
        "systemexit_expected_code": 17, "code_assertion_source_lines": [1523, 1547]},
    "noncausal_failures": [row for row in red["failure_records"] if not row["causal"]],
    "test_method_inventory": {"before": len(before_tests), "after": len(after_tests),
        "removed": sorted(before_tests - after_tests), "added": sorted(after_tests - before_tests)},
    "owned_acquisition_ast_inventory": [{"file": "tools/new1_supervisor.py", "line": line, "factory": factory} for line, factory in owned_sites],
    "acquisitions": [{"file": "tools/new1_supervisor.py", "lines": line, "resource": resource, "release": release} for line, resource, release in acquisitions],
    "precedence": [{"in_flight": original, "release_error": release, "result": result} for original, release, result in precedence],
    "scope_verification": {"ignored_parallel_builder_paths": IGNORED,
        "ignored_parallel_builder_receipts": "results/backup_gdrive_host_20261010/locked_release_*/",
        "reason": "MAESTRO26 steering: MB32 changes here are expected; ignore them.",
        "worktree_scope_final_excluding_mb32": final_scope,
        "worktree_scope_unchanged_excluding_mb32": baseline_scope == final_scope,
        "dashboard_sha256_unchanged": E["worktree_scope_before"]["tools/test_dashboard_mathlab.py"] == hashes["after"]["tools/test_dashboard_mathlab.py"]},
    "verification_scope": "Fixture/static receipts only. No real NEW1 worker, models, GPU/MPS, commit, push, merge, or scientific run.",
})
defects = []
if red["tests_run"] != 101 or red["failures"] != 22 or red["errors"] or red["skipped"] or E["runs"]["red"]["exit_code"] != 1:
    defects.append("Fresh RED did not produce the expected 101 tests, 22 assertion failures, no errors/skips, exit 1.")
if actual3 != expected3 or not E["requirement_3"]["all_fail_for_control_loss"]:
    defects.append("A requirement-3 row passed, was missing, or failed for a non-causal reason.")
if E["noncausal_failures"]:
    defects.append("Fresh RED contains non-causal/unclassified failures.")
if green["tests_run"] != 101 or green["outcome"] != "OK" or green["failure_records"] or E["runs"]["green"]["exit_code"] != 0:
    defects.append("GREEN is not 101 tests OK, exit 0.")
if before_tests - after_tests or len(before_tests) != 97 or len(after_tests) != 101:
    defects.append("Existing/new test method inventory differs from 97 existing plus four added methods.")
if baseline_scope != final_scope:
    defects.append("Worktree tools/tests bytes outside MB32 scope changed.")
for phase in ("red", "green"):
    if not E["runs"][phase]["fixtures_confined_to_copy"] or not E["runs"][phase]["isolated_bytecode_prefix_remained_absent"]:
        defects.append(f"{phase}: fixture/cache confinement failed.")
E["defects"] = defects
E["status"] = "STOPPED" if defects else "DONE"
E["receipt_completed_at"] = datetime.now(timezone.utc).isoformat()


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
                     + ["| " + " | ".join(cell(item) for item in row) + " |" for row in rows])


hash_rows = [("before", path, value) for path, value in hashes["before"].items()]
hash_rows += [("worktree after", path, value) for path, value in hashes["after"].items()]
hash_rows += [("saved test copy", path, value) for path, value in hashes["saved_test_copies"].items()]
hash_rows += [("saved source copy", path, value) for path, value in hashes["other_saved_source_copies"].items()]
hash_rows += [("isolated RED file", path, value) for path, value in hashes["isolated_run_files"].items()]
hash_rows += [("fixture routing hook", E["fixture_hook"]["path"], E["fixture_hook"]["sha256"])]
artifacts = {str(path.relative_to(R)): sha(path) for path in sorted(R.rglob("*"))
             if path.is_file() and path.name not in ("README.md", "evidence.json", "receipt_manifest.json")}
E["artifact_hashes"] = artifacts
readme = f'''# NEW1 supervisor reap round 4 — MB31 receipts

Status: **{E["status"]}**. MAESTRO26 requested evidence only for WIP `{E["wip_commit"]}`. The current supervisor and tests stayed byte-identical throughout; they were never swapped in the worktree. All persisted MB31 outputs are here or in the isolated copy.

## Fresh run receipts

{table(["Receipt", "Tests run", "Failures", "Errors / skips", "Exit", "Result"], [("RED_causal_final.log", red["tests_run"], red["failures"], "0 / 0", E["runs"]["red"]["exit_code"], red["outcome"]), ("GREEN_receipt.log", green["tests_run"], green["failures"], "0 / 0", E["runs"]["green"]["exit_code"], green["outcome"])])}

RED has 22 failure records across four test methods: **12 requirement-3 control-loss subtests, nine additional requirement-1 precedence subtests, and one requirement-2 structural guard failure**. It does not mean 22 independent test methods failed or that only 79 methods passed. The before-test inventory contains 97 methods; the final inventory contains the same 97 plus four new methods. All 97 existing methods pass in both fresh runs. GREEN is 101/101 OK.

The full set of failing identities **{'matches' if red_names == old_names else 'does not match'} RED_strengthened.log**, including subtest parameters: fresh={len(red_names)}, strengthened={len(old_names)}, only fresh={len(red_names-old_names)}, only strengthened={len(old_names-red_names)}. This comparison corroborates the old log; that log has no recorded execution provenance and is **not** this causal receipt. Earlier RED_final.log / RED_causal.log used intermediate test copies according to the dispatch context and are not final-test causal receipts.

## Recorded provenance and fixture confinement

Copy directory: `{E["copy_dir"]}`. `capture_receipts.py` created it using `mktemp -d /private/tmp/new1_reap_r4_mb31.XXXXXX`, copied worktree `tools/` and `tests/` with `cp -R`, then overwrote **only the copy's** supervisor with `before/new1_supervisor.py`. Copied bytecode caches were removed inside the copy. The executable for both runs is the worktree's `.venv/bin/python`.

RED, cwd `{E["runs"]["red"]["cwd"]}`, executed once:

```sh
{E["runs"]["red"]["exact_command"]}
```

GREEN, cwd `{E["runs"]["green"]["cwd"]}`, executed once:

```sh
{E["runs"]["green"]["exact_command"]}
```

`tests/test_new1_supervisor.py:31` hardcodes `tempfile.TemporaryDirectory(dir='/private/tmp')`. To meet the write/deletion boundary without editing tests, both commands inherited the same recorded startup hook at `{E["fixture_hook"]["path"]}`. It redirects stdlib `tempfile.mkdtemp` requests for `/private/tmp` into `{E["copy_dir"]}/fixtures`; it leaves the supervisor, test bytes, assertions, releases, mocks, and signal behavior unchanged. The hook records requested/allocated roots in the copy. Each run allocated 101 fixture roots, all inside the copy, and the tests cleaned only those roots. This is an explicit fixture-location adjustment, not an undisclosed ordinary-environment run.

{table(["Inherited variable", "Value for both commands (except per-run log)"], [(key, value if key != "NEW1_RECEIPT_TMPLOG" else E["runs"]["red"]["inherited_environment"][key] + " / " + E["runs"]["green"]["inherited_environment"][key]) for key, value in E["runs"]["red"]["inherited_environment"].items()])}

`PYTHONPYCACHEPREFIX` selected a fresh, nonexistent cache location; `-B` and `PYTHONDONTWRITEBYTECODE=1` kept it absent in both runs, so worktree stale `.pyc` files were neither read nor deleted. `evidence.json` recorded each command, cwd, inherited environment, supervisor/test hashes and start time **before** launch; it then recorded exit, completion time, output hash and post-run hashes. The capture script prevents duplicate RED or GREEN runs. Estimated additional writes were at most 8 MiB; recorded free space exceeded that plus 20 GiB on both volumes. No temporary copy was deleted.

## Release mechanism and why it covers r12

The committed fix chooses one `ResourceOwner` (`tools/new1_supervisor.py:376`) rather than separate cleanup handlers at individual resources. `context` (:380) stores the resource's exit callback before entering it; `acquire_many` (:385) registers both socket close callbacks. Every entry passes through `_release` (:391), which catches `BaseException`, selects the governing exception using `preferred_exception` (:268), and attaches the losing error as a note. `close` (:414) drains all remaining entries in LIFO order before raising a newly selected winner. `scope` (:421) passes the propagating exception into that drain, then re-raises it. Early `release(child)` (:534) uses the same callback/precedence path and retains a failed entry for final cleanup. Callback return values cannot suppress the governing exception.

`supervise` creates one owner (:441), registers worker lifetime before construction (:507), and uses that owner's scopes for the log files (:525), constructor handlers (:530), selector (:535), bounded reap (:462), and halt-durability timer (:616). Final root drain is :629. The installed timer exits before the worker lifetime's separate five-second reap. A worker handle is assigned at :529 before `Popen.__init__` at :532 can spawn and raise, preserving ownership of an eventual PID.

In old `before/new1_supervisor.py:466`, native stdout/stderr `with` exits could replace the control exception; the old selector `with` at :473 could do the same before old worker_lifetime captured the governing exception at :393. The current selector/log exits run through `_release`, so an OSError becomes a note on the original KeyboardInterrupt or SystemExit(17). The fresh final-test RED reproduces both reviewer r11 sequences with fake processes/signals and the installed CPython `_internal_poll`; it does not launch the real NEW1 geometry worker. Fixture worker subprocesses elsewhere in the suite are stdlib stubs created by the tests.

## Precedence table

Here “in flight” means the exception delivered to the owner at that cleanup boundary. “Ordinary” excludes KeyboardInterrupt and SystemExit. The existing control-promotion rule remains: a new control exception may replace an ordinary exception, while the first control exception always wins.

{table(["In flight", "Release error", "Result"], precedence)}

These are owner-level results. A propagated ordinary exception reaching supervise's handler may still map to its existing outcome code; an unmasked root release error escapes the final drain. The precedence test also checks that latter case at `tests/test_new1_supervisor.py:1578`, so an ordinary root close error is not silently suppressed. SystemExit(17) identity/code are explicitly checked at :1520/:1523 and :1544/:1547. No deadline, outcome, event or resource-cap changes are made by this receipt task.

## Every acquisition site in supervise

All lines below refer to the current pinned `tools/new1_supervisor.py`. The nine explicit owner-routed acquisition calls extracted from its AST are also listed verbatim in evidence.json. Setup, scope markers, worker allocation, and reviewed helper I/O are included to make the boundary explicit; helper internals are not claimed to be recursively covered by this AST test.

{table(["File:line", "Resource / acquisition", "Release / ownership"], [("tools/new1_supervisor.py:" + line, resource, release) for line, resource, release in acquisitions])}

Selector registration (:537) borrows the already owned parent socket; unregister (:551) removes the registration. Poll/kill/terminate helpers retain their existing internal signal-mask handling. Neither creates an additional retained resource in supervise.

## AST guard: inspection and limits

`tests/test_new1_supervisor.py:1589` parses the full source of supervise and walks it, including nested helpers. It prints `OWNERSHIP_AST` records for **every With/AsyncWith boundary, every Call, and each owner acquisition factory** (:1614). Every with must be `resources.scope()` (:1618); calls must be in the explicit reviewed allowlist (:1600). Unknown factories, direct opens and direct closes fail (:1623). It additionally requires exactly one worker-lifetime registration and preallocated handle inside that lifetime (:1626), exactly one constructor-ownership scope with the sole initializer inside it (:1639), exactly one correctly named owner (:1651), and root final drain (:1655).

The guard test at :1661 also checks six deliberately unmanaged mutations: arbitrary native with, arbitrary factory call, direct file open, direct parent close, duplicate owner, and initializer outside constructor ownership (:1669). GREEN therefore checks both acceptance of current ownership and rejection of those additions.

It would catch r12's selector/log-file exits because their native with boundaries are not owner scopes and their raw factory calls are not allowlisted. Fresh RED reports exactly those findings: stdout/stderr native with at old :466 and selector native with at old :473, plus direct opens and selector factory. The structural assertion identifies 24 findings (`RED_causal_final.log:460`; full list :467). This is an expected structural RED, not a claim that its assertion itself detects lost control. Logged old-source probes at :499 os.getpid and :513 expression.glob further agree with the recorded old source. The guard is a reviewed-call/structure guard, not a semantic proof of arbitrary helper internals or a guarantee that changing an allowlisted callee needs no review.

## Every fresh RED failure classified

All methods belong to `tests.test_new1_supervisor.SupervisorTests`. Subtest parameters are part of each identity. Requirement-3 rows inject **OSError at the selected close**; six cover interrupted poll / successful waitpid and six cover heartbeat cleanup. All twelve reach the control-identity assertion after fixture/reap/release assertions have passed, then show `caught=None` and returned `INVALID-WORKER`: the control was lost. All six SystemExit variants use expected code **17**. None passes on old source, and none fails because of an import, fixture, missing-name or unrelated error. Non-causal failures: **{len(E["noncausal_failures"])}**.

{table(["Test name and subtest", "Requirement / coverage", "Assertion text from RED_causal_final.log", "Classification"], [(row["test_method"] + (" " + row["subtest"] if row["subtest"] else ""), str(row["requirement"]) + ": " + row["coverage"], "RED_causal_final.log:" + str(row["assertion_log_line"]) + " — " + row["assertion_text"], row["classification"]) for row in red["failure_records"]])}

For the three ordinary Stop rows, the diff assertion also prints `ordinary release replaced original Stop` at log :286/:297/:308. The structural guard prints its full unmanaged-site explanation through :493. Those are the additional causal requirement-1 failures and the intentional requirement-2 failure, respectively; they are not silently relabelled as requirement-3 control-loss tests.

## SHA-256 pins and every saved test copy

Receipt-relative paths below are relative to this directory; worktree and isolated paths are labelled. Before-source/test pins and current source/test pins were verified before either run. The isolated RED test and RED_strengthened_tests.py are byte-identical to the current final tests; the earlier intermediate copies differ.

{table(["Kind", "Path", "SHA-256"], hash_rows)}

## Diffs and artifact hashes

The requested unified diffs are **supervisor.diff** and **tests.diff**. Both `diff -u` commands returned 1 (differences found), with nonempty stdout and no stderr. Exact commands and hashes are in evidence.json. This captures the committed WIP change relative to MB29's before copies; it is not a new source edit by MB31.

{table(["Artifact", "SHA-256"], [(name, value) for name, value in artifacts.items() if name.endswith((".log", ".exit", ".diff"))])}

All captured receipt artifacts (including saved source/test copies and the two evidence helper scripts) are hashed in evidence.json. receipt_manifest.json separately hashes the final README.md and evidence.json without a self-referential hash. capture_receipts.py is the capture implementation; write_receipts.py derives this README/classification/diffs and never runs tests.

## Scope and completion record

MB31 made no edits to worktree tools/ or tests/, no real worker/model/GPU/MPS run, no commit/push/merge, and no process kill outside the processes created by the fixture suite. tools/test_dashboard_mathlab.py already had an unrelated uncommitted change on entry; its hash remains `{hashes["after"]["tools/test_dashboard_mathlab.py"]}`. The final tools/tests hash comparison excludes only MB32's four authorized paths below; every other file's bytes match the entry snapshot. MB32's results/backup_gdrive_host_20261010/locked_release_*/ receipts are also outside MB31 scope.

{table(["Expected concurrent MB32 path (ignored)"], [(path,) for path in IGNORED])}

EVIDENCE-SHOWS: final tests causally fail on the pinned old source and all 101 pass on the pinned WIP source, with recorded provenance and zero non-causal failures. Limits: fixture/static verification only; no scientific NEW1 execution or admission claim. The next owner is MAESTRO26 for receipt review and the existing promotion workflow; no further implementation is proposed or performed here. Session context is preserved in this README within the authorized write boundary.

CONTEXT DIRECTIVE (binding; survives any future handoff): watch “Context N% left” in the status line. Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work and write a handoff at the end of this README with what is done, what is half-applied, exact paths and SHA-256 of changed files, failing tests with exact commands, and next step; reply exactly “CONTEXT HANDOFF WRITTEN”. On “Context compacted”, do that at once.
'''
if defects:
    readme += "\n## DEFECT\n\n" + "\n".join("- " + defect for defect in defects) + "\n\nSource and tests were not edited. A reviewed fix requires a separate brief.\n"
(R / "README.md").write_text(readme)
(R / "evidence.json").write_text(json.dumps(E, indent=2, sort_keys=True) + "\n")
manifest = {str(path.relative_to(R)): sha(path) for path in sorted(R.rglob("*"))
            if path.is_file() and path.name != "receipt_manifest.json"}
(R / "receipt_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": E["status"], "red": {"tests": red["tests_run"], "failures": red["failures"], "exit": E["runs"]["red"]["exit_code"]},
                  "green": {"tests": green["tests_run"], "outcome": green["outcome"], "exit": E["runs"]["green"]["exit_code"]},
                  "failure_set_matches": red_names == old_names, "classification_counts": E["failure_counts_by_requirement"],
                  "noncausal_failures": len(E["noncausal_failures"]), "scope_unchanged": baseline_scope == final_scope, "defects": defects}))
