# MB35 Drive applet comparison fix

From MAESTRO27; locked starting commit: `a19749dc96ea565bb536256c9fd5feab359ef23a`.
Receipt: `results/backup_gdrive_host_20261010/cmp_fix_20261010231913Z`.

The builder compares the app main script's decompilation with the decompilation of a fresh `.scpt` compile of the same saved canonical source. Both compiles happen during the same build after canonical text is copied to `$SOURCE`. The reference stays in the existing scratch directory. `cmp` remains byte-exact and fatal.

A compiler/decompiler round trip can append a newline, so comparing the saved input directly with its app decompilation rejects a valid build. This fix compares like with like. No newline or whitespace normalization is used. `$SOURCE` remains the text produced by the original canonicalization step.

The empty-canonical guard, `chmod 444`, and the entire Perl SHA-256 inventory are preserved byte for byte. The production diff adds one comment and two reference compile/decompile commands and changes only the first argument to `cmp`.

## Test seam

Production keeps `/usr/bin/osacompile` and `/usr/bin/osadecompile`; there is no production override or bypass. Each non-native test rewrites only those two executable paths in a temporary copy of the builder, then places fake executables on that copy's PATH. Real staging, the commit-only fixture release, canonical-source write, strict `cmp`, modes, and Perl inventory execute normally.

The fakes retain every input byte and add one newline on every decompile. Other cases alter an app byte, append an extra app-only newline, or return an empty canonical decompile. The successful case checks the saved canonical bytes, the extra round-trip newline, mode 444 on both saved text files, and the complete real Perl inventory. Mismatches must fail before inventory publication.

`test_compiled_app_full_source_equals_saved_source` now independently compiles the saved source to a fresh `.scpt`, decompiles that and the app main script to files, and compares `read_bytes()` results. It also checks the app decompile against the build's saved `.decompiled.applescript`. File redirection avoids text-mode newline translation in this native assertion.

## Sandbox evidence

Tests were edited and snapshotted before production changed. `before/` holds both originals; `test_first_snapshot.py` is the unchanged test-first version used for RED and GREEN. Each run has `command.json`: exact command, cwd, invoked/actual interpreter, fixed source/test hashes, and generated fixture-source hashes observed before subprocess starts and fixture cleanup. `started_commands.json` records subprocess invocations.

| Check | Sandbox RED | Sandbox GREEN |
| --- | --- | --- |
| Newline-growth regression | FAIL: `cmp: EOF` on saved source | PASS |
| App byte change and app-only extra newline | PASS: both rejected | PASS: both rejected |
| Empty canonical decompile | PASS: rejected | PASS: rejected |
| Focused runs | 3 run: 2 passed, 1 failed; 0 errors/skips | 3 passed; 0 failures/errors/skips |
| All eligible non-native fixtures | Not run | 136 passed; 0 failures/errors/skips |
| Native manifest, locked dispatch, compiled-source relation | UNRUN | UNRUN |
| Full host suite through frozen MB32 runner | UNRUN | UNRUN |

The non-native selection excludes four native AppleScript tests and 14 existing real-rclone tests; `sandbox_green_non_native/suite_selection.json` lists all 18. This is pending coverage, not passed coverage or added test skips. The sandbox runner invokes neither native AppleScript tools nor real rclone. `/bin/ps` is UNAVAILABLE under the supplied restriction; no global-idle claim is made.

Exact sandbox commands, from the worktree root:

```bash
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/cmp_fix_20261010231913Z/run_sandbox.py sandbox_red focus
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/cmp_fix_20261010231913Z/run_sandbox.py sandbox_green_focus focus
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/cmp_fix_20261010231913Z/run_sandbox.py sandbox_green_non_native non_native
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/cmp_fix_20261010231913Z/verify_receipt.py
```

Labels are exclusive directories: reproducing a run requires a fresh label. RED used the original builder hash below; GREEN uses the fixed builder. RED exit 1 is the expected regression failure.

## Final source SHA-256

| File | Before | Final |
| --- | --- | --- |
| `tools/launchd/build_gdrive_applet.sh` | `d467ef24968d512152f2e5d8ba5cc946ff1809acd8bfefeab850ba0cc8685076` | `33d0e8473f3d731584f163f7b90e2fee1be7df3b98432c7afc181108884f7252` |
| `tools/test_backup_gdrive_addendum.py` | `6eba5860e1fbb0c562af9a4241f8acf6f50d966d05b3d0e8ac66ec35e14e7d2c` | `f9547a3f58870881a5d78b8e2fd829a24e432979885c199865e837cfa871ab34` |

Protected scripts retain:

- `tools/backup_gdrive.sh`: `36647860fa5149f4428eee2a89eeb6fd9e50628c04a819b9a702380f031f27b8`.
- `tools/backup_gdrive_status.py`: `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46`.

`before_sha256.json` also pins staging, the AppleScript template, excludes, archive script, imported test helper, launchd plist, and frozen host runner. Final scope/source verification is recorded in `final_verification/`.

## Exact MAESTRO host commands — UNRUN here

Use the original MB32 runner without modification. Each targeted test needs its own label because the runner accepts one selector. The full-suite labels are exactly `cmpfix_red` and `cmpfix_green`.

First create a private `mktemp` copy of the saved pre-fix bytes. Its own temporary Git metadata borrows the live repository's objects read-only and pins HEAD to the locked commit, enabling the native builder's commit-only release. This does not change the live checkout or check out the whole repository.

```bash
MB35_ROOT="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
MB35_RECEIPT="$MB35_ROOT/results/backup_gdrive_host_20261010/cmp_fix_20261010231913Z"
CMPFIX_RED_ROOT="$(/opt/homebrew/bin/rtk proxy /usr/bin/mktemp -d /private/tmp/memit_cmpfix_red.XXXXXX)"
LLMDB_ROOT="$MB35_ROOT" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B - "$MB35_ROOT" "$MB35_RECEIPT" "$CMPFIX_RED_ROOT" <<'PY'
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

root, receipt, copied = map(lambda p: Path(p).resolve(), sys.argv[1:])
assert copied.parent == Path("/private/tmp")
assert copied.name.startswith("memit_cmpfix_red.")
assert copied.is_dir() and not any(copied.iterdir())
hashes = json.loads((receipt/"before_sha256.json").read_text())
changed = {"tools/launchd/build_gdrive_applet.sh", "tools/test_backup_gdrive_addendum.py"}
sources = {}
for name, digest in hashes.items():
    source = receipt/"before"/name if name in changed else root/name
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, name
    sources[name] = source
subprocess.run(["/usr/bin/git", "clone", "--shared", "--no-checkout", "--quiet",
                str(root), str(copied)], check=True)
subprocess.run(["/usr/bin/git", "-C", str(copied), "update-ref", "--no-deref", "HEAD",
                "a19749dc96ea565bb536256c9fd5feab359ef23a"], check=True)
for name, source in sources.items():
    destination = copied/name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert hashlib.sha256(destination.read_bytes()).hexdigest() == hashes[name], name
(copied/"copy_source_sha256.json").write_text(json.dumps(hashes, indent=2, sort_keys=True)+"\n")
print("Pre-fix source copy ready:", copied)
PY
cd "$CMPFIX_RED_ROOT"
```

Run the four RED commands independently. The first three must reproduce native `cmp: EOF` failures; the fourth runs all original 151 tests. Nonzero returns are expected; native skips do not prove RED. The frozen runner disables real rclone, accounting for 14 pre-existing full-suite skips.

```bash
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_red_builder LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_red_dispatch LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_red_source LockedReleaseTest.test_compiled_app_full_source_equals_saved_source
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_red all
```

Persist all four RED receipts before leaving the temporary copy. Each includes `command.json`, `test.log`, result, source hashes, and process-clearance evidence. There is no deletion command.

```bash
LLMDB_ROOT="$MB35_ROOT" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B - "$CMPFIX_RED_ROOT" "$MB35_RECEIPT" <<'PY'
from pathlib import Path
import shutil
import sys

copied, receipt = map(Path, sys.argv[1:])
source = copied/"results/backup_gdrive_host_20261010/locked_release_20261010T221519Z"
destination = receipt/"host_red"
destination.mkdir()
for label in ("cmpfix_red_builder", "cmpfix_red_dispatch", "cmpfix_red_source", "cmpfix_red"):
    assert (source/label/"command.json").is_file(), label
    assert (source/label/"result.json").is_file(), label
    shutil.copytree(source/label, destination/label)
PY
cd "$MB35_ROOT"
```

Run the three targeted GREEN tests and all 154 tests in place. Each targeted run requires one passed test and zero skips/errors/failures. The full run requires successful process clearance, no failures/errors, and no native skips; the 14 real-rclone skips are inherited. These are acceptance expectations, not sandbox results.

```bash
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_green_builder LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_green_dispatch LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_green_source LockedReleaseTest.test_compiled_app_full_source_equals_saved_source
LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py cmpfix_green all
```

GREEN receipts land under `results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/`. The runner/native fixtures isolate HOME below receipt or temporary fixture roots; these commands do not install in the operator's real Library or Applications.

## Session context

The two requested edits are fully applied. Focused GREEN and all 136 non-native fixture passes are saved. `final_verification/result.json` confirms the before copies, protected hashes, unchanged unrelated test AST, test-first ordering, exact production diff, build syntax, and syntax of all five host shell blocks and two embedded Python blocks. Required remaining runtime validation is the host sequence above; native results remain UNRUN. This context-save summary stays inside the authorized receipt. No repository commit, live science, native app launch, or edit of `tools/test_dashboard_mathlab.py` was made. MB33's files and receipt family were left outside this task.

MAESTRO28 reported an expected tracker-only HEAD update from `02b44af` to `436c507`. This is authorized and is not a STOP condition. The saved RED copy remains pinned to the locked pre-fix source bytes and commit; GREEN runs in place against the source hashes above.

Learning recorded here: compiler/decompiler text is an output format, so the integrity relation must compare decompilations of equally compiled saved inputs. Native permission skips cannot validate that relation.

Context directive (binding, including every successor/team session): watch “Context N% left”; start a new piece of work only at 60% left or more. At 40% left or less, or on “Context compacted”, stop starting work immediately, append a handoff at the end of this README with completed and half-applied work, exact paths and SHA-256, failing test commands, next step and open risks, and reply exactly “CONTEXT HANDOFF WRITTEN”. Restate this directive in every handoff.
