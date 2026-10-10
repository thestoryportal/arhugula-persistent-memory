"""Append the MB21 receipt without rewriting any prior report byte."""
import hashlib
import json
import os
from pathlib import Path

root = Path(os.environ["LLMDB_ROOT"])
receipt = Path(__file__).resolve().parent
relative = str(receipt.relative_to(root))
report = root/"results/backup_gdrive_build_report.md"
original_report = (receipt/"originals/backup_gdrive_build_report.md").read_bytes()
assert report.read_bytes() == original_report, "report changed since capture; inspect before appending"
before = json.loads((receipt/"hashes_before.json").read_bytes())
red = json.loads((receipt/"RED_index.json").read_bytes())
verification = json.loads((receipt/"verification.json").read_bytes())
changed = ["tools/backup_gdrive_status.py", "tools/launchd/MemitGdriveBackup.applescript",
           "tools/test_backup_gdrive_addendum.py", relative+"/host_launcher_checks_mb21.py"]
final = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in changed}
hash_rows = []
for name in changed:
    start = before.get(name, "New receipt copy; copied baseline "+before[
        "results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py"])
    hash_rows.append(f"| `{name}` | `{start}` | `{final[name]}` |")
hash_rows.append(f"| `results/backup_gdrive_build_report.md` | `{before['results/backup_gdrive_build_report.md']}` | See `{relative}/hashes_final.json` (external to avoid self-reference) |")
red_rows = [f"| `{row['test']}` | `{row['log']}` |" for row in red]
tree = json.loads((receipt/"mb14_fixture_tree_sha256.json").read_bytes())
tree_rows = [f"| `{row['path']}` | {row.get('bytes', 'directory')} | `{row.get('sha256', 'directory')}` |" for row in tree]
text = f'''
## MB21 Astra r6 findings 2 (P1), 3 (P2) and 4 (P2) build and verification

**GDRIVE R6 FIX BUILD DONE — 15 PASS, 0 skipped; 8 new or reversed regressions have saved behavioral RED and GREEN.** Candidate for MAESTRO17 host verification and GPT-6-Astra re-review. Activation remains **BLOCKED** until Astra says GO. Starting branch/root were verified as `worktree-c10k-route-a` / this worktree. All four supplied MB20 source pins matched before the first edit. The archived MB14 status source also matched `64d59eabbf4176c67451309a261cdd87e3c0b137094cde217e064a47a9793c9b`.

### Criteria and evidence

1. Recovery now inspects the payloads in **all** recovery directories, including raw archived counters, archived heartbeat/receipt JSON and every independently parsed archived journal line before and after torn lines. Manifests remain validated, but their maximum does not replace payload inspection. The same `inspect_history()` implementation runs before any recovery mkdir/lock and again under the allocator lock. Archived uncertain payloads are observed without being added to the list of files moved by recovery. Every archived byte stays intact.
2. Live `refusals/latest-refusal.json` is included in both observed-maximum calculations. Its valid launch generation raises the required reviewed floor. Exit 75 publishes no failure journal or additional failure interval. The absent-state recovery keeps the existing conservative lost-history range derived from the reviewed floor; with floor 100 that range is `[[1,100]]`, and the recovery barrier is 101. No refusal-specific failure is inserted. The exact corrupt-counter / absent-state / completed-10 / null-receipt / refusal-100 input refuses floor 10 with the whole Logs tree unchanged, accepts floor 100, retains the refusal bytes and becomes healthy after sequenced completion 102. A separate injected-refusal test proves the under-lock recheck.
3. All three compaction boundaries are strict: the Python reader rejects **completed <= compaction_barrier**, and both extracted Perl `resolve_state` implementations clear only for **completed > compaction_barrier**. The old equality-clears test is reversed and renamed `test_r6_3_compacted_barrier_requires_strictly_later_completion`. The previous `test_5_python_and_both_perl_publishers_agree_at_boundaries` is extended and renamed `test_r6_3_python_and_both_perl_publishers_agree_at_boundaries` to follow the required r6 criterion numbering. It checks completed = barrier - 1, barrier and barrier + 1 for Python and both publishers, as well as the original 64/65 interval boundary. The actual extracted production-shell schedule fails odd generations 11..137 and refuses the intervening evens, then allocates 139: barrier 139 is created, completion 139 remains unhealthy and both publishers retain it; allocation/refusal 140 still cannot discharge it; completion 140 becomes healthy and both publishers clear it.
4. The seven retained tests passed with the eight new/reversed regressions. The r5 torn-journal and valid-after-torn cases still preserve all bytes, refuse inadequate floors, reserve the correct barriers and require sequenced completion above recovery. The unchanged 2,000-allocation test exercises both complete production Perl programs, preserves 64-interval / 2,048-byte bounds and keeps manual, incomplete and refused completions from clearing barriers. The byte-overflow test retains `recovery_barrier`. The applet diff is verified to contain **exactly two comparison replacements**; manual-interleave, late-generation ordering, owner handling, exit-75 publication, nested catches and launch control flow were not rewritten. `tools/backup_gdrive.sh` is unchanged, so retries, bandwidth, excludes and owner-preserving refusal behavior retain their reviewed implementation. Finding 5's remaining runtime tests are part of the full host suite below; they were not rerun locally outside the authorized touched classes.
5. MB20's helper was copied, preserving the original, to `{relative}/host_launcher_checks_mb21.py`. New native case **compaction-boundary** seeds the 64 odd intervals and uses three actual isolated applet allocation/refusal invocations: first compaction at 139, then completion equal to 139 during generation/receipt publication 140 (still unhealthy; barrier retained), then completion 140 during publication 141 (healthy; barrier cleared). It saves `unresolved_compacted.json`, `unresolved_equal.json` and `unresolved_above.json`. Default fixture roots remain fresh local `/private/tmp`; explicit roots must exist, be empty and resolve outside `/Volumes`. The 20-second `open -W -g` timeout is unchanged. All five native cases are **UNRUN / HOST-PENDING here**. Only syntax and `--help` were checked for the copied helper.
6. Real HOME inventories immediately before and after the final two-class run are byte-identical: **21 entries, 18 regular files with SHA-256, 2 directories, 1 absent path**. Both listing files have SHA-256 `{verification['real_inventory']['sha256']}`. The read-only MB20 inventory script was copied unchanged to `{relative}/real_path_listing.py`. An initial inventory is retained too. Every test fixture and cleanup used `{relative}/fixtures`; the actual HOME backup-log glob, Applications app and LaunchAgents were only read by the inventory script.

### Actual MB14 fixture

`{relative}/capture_mb14_fixture.py` ran the pinned MB14 recovery **once** on the exact requested input in a receipt-local temporary directory: failure 100 followed by `{{torn`, corrupt counter, absent unresolved state, completed generation 10, null-generation receipt, floor 10. Command/exit/stdout/stderr are saved in `mb14_recovery_command.json`. Actual MB14 output had highest_seen 10 and recovery_barrier 11, while its archived journal retained failure 100. The exact archived directory names and file bytes, counter, counter lock and unresolved state are saved under `mb14_fixture/`. The regression copies this saved output layout, verifies every saved file hash, refuses floor 11 without changing any file/absence, accepts floor 100 with barrier 101, rejects completion 13 and accepts a sequenced allocation/completion 102. The original MB14 archive remains byte-identical throughout.

Machine-readable tree: `{relative}/mb14_fixture_tree_sha256.json`. Paths below are relative to `mb14_fixture/`:

| Path | Bytes / kind | SHA-256 |
| --- | --- | --- |
{chr(10).join(tree_rows)}

### RED index and scoped verification

Machine-readable index: `{relative}/RED_index.json`. Production status/applet/wrapper hashes were still the MB20 pins when the RED runs completed. Each touched class ran once in RED and once in GREEN; each individual RED receipt contains its corresponding complete class log, including that test's assertion failure. The eight indexed methods had behavioral failures and **no unittest errors or skips**. Seven retained tests were already passing. No full-suite or native execution, rclone invocation, network call or repeated test loop was performed by MB21.

| New or reversed test | RED receipt in this directory |
| --- | --- |
{chr(10).join(red_rows)}

Exact scoped commands used by `run_scoped_tests.py` (the executable resolves to this worktree's `.venv/bin/python`):

```sh
export BACKUP_TEST_NO_RCLONE=1
export BACKUP_TEST_RECEIPTS=$PWD/{relative}/fixtures
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.R5RecoveryTest -v
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum.R5CompactionTest -v
```

GREEN receipts: `GREEN_R5RecoveryTest.log` (**9 PASS**) and `GREEN_R5CompactionTest.log` (**6 PASS**), zero skips. `RED_commands.json` / `GREEN_commands.json` preserve exact argv, exits, counts and log hashes. `verification.json` records syntax checks, exact two-change publisher scope, protected pins, intact MB14 fixture hashes, eight RED receipts and identical real-path inventories. Python compilation without bytecode, all three embedded shell syntax checks, both entire extracted Perl syntax checks, helper/recovery CLI help and changed-line whitespace checks passed. Source diffs against the captured MB20 originals are saved beside those receipts. The full suite is intentionally host-pending; expected count after these six net-new methods is 119, subject to MAESTRO17's actual full-suite receipt.

### Recovery command, evidence list and refusal rule

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B tools/backup_gdrive_status.py recover --generation-floor N --heartbeat /absolute/fixture/path/last_run.json
```

N must be operator-reviewed and cover every observed generation from: the current raw counter; current `unresolved.json` issued state; current heartbeat; current launch receipt; every independently parseable current failure-journal line; current `refusals/latest-refusal.json`; every preserved recovery manifest; every archived raw counter; and JSON / individually parsed JSONL payloads in **every** archived recovery directory, including archived heartbeats, receipts, refusal heartbeats and failure journals. Recognized valid generation fields include launch_generation, issued_generation, recovery_barrier, compaction_barrier, highest_seen and generation_floor. Old directory payloads count even if a newer directory has a lower maximum. Both the pre-lock scan and under-lock recheck use this complete list.

An inadequate floor exits nonzero with `recovery refused` / `below observed maximum`; a pre-lock refusal creates no directory or lock and writes/moves nothing. An injected higher archived generation or refusal after the first scan is rejected under lock without moving/publishing recovery evidence. Exit 75 is only an observed-generation source, not an unresolved backup failure. All archived bytes remain intact even when torn. Recovery still never establishes health on its own, and neither manual completion nor refusal can discharge recovery or compaction barriers. Do not omit `--heartbeat` in fixtures: the default points at real HOME and remains an operator recovery action only after GO.

### Exact host commands for MAESTRO17

Run the full addendum suite once on the host with real **local** rclone, preserving local `/private/tmp` receipts. This is not a Drive/network self-test.

```sh
mb21_host_receipts=/private/tmp/backup_gdrive_mb21_host_$(/bin/date -u +%Y%m%dT%H%M%SZ)
/bin/mkdir "$mb21_host_receipts"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/real_path_listing.py "$mb21_host_receipts/real_paths_before.json"
LLMDB_ROOT=$PWD BACKUP_TEST_NO_RCLONE=0 BACKUP_TEST_RECEIPTS="$mb21_host_receipts" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v > "$mb21_host_receipts/acceptance.log" 2>&1
mb21_suite_exit=$?
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/real_path_listing.py "$mb21_host_receipts/real_paths_after.json"
if [ "$mb21_suite_exit" -ne 0 ]; then
    /bin/cat "$mb21_host_receipts/acceptance.log"
    exit "$mb21_suite_exit"
fi
/usr/bin/cmp "$mb21_host_receipts/real_paths_before.json" "$mb21_host_receipts/real_paths_after.json"
```

Inspect acceptance.log, exit code and identical inventories before proceeding. Run **every** native helper case on local temp paths; none was run by MB21:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/host_launcher_checks_mb21.py manual-interleave
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/host_launcher_checks_mb21.py crash-after-allocation
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/host_launcher_checks_mb21.py recovery
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/host_launcher_checks_mb21.py unresolved-compaction
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B {relative}/host_launcher_checks_mb21.py compaction-boundary
```

Provide source pins, RED/GREEN, fixture tree, isolation receipts, full-suite and five native-case evidence to GPT-6-Astra. This build establishes fixture behavior and syntax only; native privacy, real Drive copy, production activation and power-loss durability remain unverified. No commit, push, merge, Applications install, launchd mutation, real backup-log write, rclone or network call occurred here.

### Start and final SHA-256 / scope

| Changed file | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
{chr(10).join(hash_rows)}

The report is appended and every prior byte is retained. `hashes_final.json` supplies its final hash and hashes of every new receipt file (start: absent), avoiding a self-referential report hash. `hashes_before.json` and `originals/` preserve the start evidence. The copied listing script remains `{before['results/backup_gdrive_mb20_20261010T180133Z/real_path_listing.py']}`. MB14 original and both MB20 helper/listing originals remain unchanged. `tools/backup_gdrive.sh` remains `{before['tools/backup_gdrive.sh']}`; no criterion required changing it. No main-checkout staged file, dashboard file/receipt, `tools/test_dashboard_mathlab.py`, NEW-1 file or unrelated builder file was touched or hashed as protected.

Session continuation: no half-applied source change or in-flight test remains. Next: MAESTRO17 runs the host commands once, obtains Astra re-review and keeps activation blocked until GO. Learning: archived payloads retain generation authority independently of manifests; refusal generations constrain recovery floors without becoming backup failures; completion must be strictly later than a conservative compaction barrier.

Context directive remains binding for every successor/team session: watch **Context N% left**. Start a new piece of work only at **60% left or more**. At **40% left or less**, stop starting work, append a handoff with completed/in-flight work, half-applied changes, exact paths and SHA-256 and next step, then reply exactly **CONTEXT HANDOFF WRITTEN**. If **Context compacted** appears, do so immediately. Restate this directive in any handoff. Do not allow sessions to approach full-window compaction; use a fresh successor with a precise handoff.
'''
with report.open("ab") as stream:
    stream.write(text.encode())
assert report.read_bytes() == original_report+text.encode()
(receipt/"report_append_sha256.json").write_text(json.dumps({"original_bytes": len(original_report),
    "appended_bytes": len(text.encode()), "original_sha256": hashlib.sha256(original_report).hexdigest(),
    "append_sha256": hashlib.sha256(text.encode()).hexdigest()}, indent=2)+"\n")
print("Appended MB21 report; original byte prefix preserved")
