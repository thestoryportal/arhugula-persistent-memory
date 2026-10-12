"""MB35 non-native evidence runner; native AppleScript and real rclone are excluded."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import unittest

RECEIPT = Path(__file__).resolve().parent
ROOT = RECEIPT.parents[2]
label, selector = sys.argv[1:]
RUN = RECEIPT/label
RUN.mkdir()
home, fixtures = RUN/"home", RUN/"fixtures"
home.mkdir()
fixtures.mkdir()
os.environ.update(HOME=str(home), LLMDB_ROOT=str(ROOT), BACKUP_TEST_NO_RCLONE="1",
                  PYTHONDONTWRITEBYTECODE="1", BACKUP_TEST_RECEIPTS=str(fixtures),
                  BACKUP_PYTHON="/usr/bin/python3", MB28_BACKUP_PYTHON="/usr/bin/python3")
assert sys.flags.dont_write_bytecode
assert Path.cwd() == ROOT
sys.path.insert(0, str(ROOT))
import tools.test_backup_gdrive_addendum as addendum

def save(name, value):
    (RUN/name).write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")

names = list(json.loads((RECEIPT/"before_sha256.json").read_text()))
paths = [*(ROOT/name for name in names), Path(__file__).resolve()]
hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
          for path in paths}
argv = ["/usr/bin/python3", "-B", *sys.argv]
command = 'LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy '+shlex.join(argv)
metadata = {"argv": argv, "command": command, "cwd": str(Path.cwd()),
            "interpreter": sys.executable, "invoked_interpreter": "/usr/bin/python3",
            "python_version": sys.version, "source_sha256": hashes,
            "env": {k: os.environ[k] for k in ("HOME", "LLMDB_ROOT", "BACKUP_TEST_NO_RCLONE",
                    "PYTHONDONTWRITEBYTECODE", "BACKUP_TEST_RECEIPTS", "BACKUP_PYTHON",
                    "MB28_BACKUP_PYTHON")}}
save("command.json", metadata)
fixture_hashes = {}
processes = []
active_fixture = None
original_setup = addendum.Fixture.setUp
original_popen = subprocess.Popen.__init__

def capture_sources():
    if active_fixture is None or not active_fixture.base.is_dir():
        return
    for path in active_fixture.base.rglob("*"):
        if ".git" in path.relative_to(active_fixture.base).parts:
            continue
        if path.is_file() and (path.suffix in {".py", ".sh", ".applescript", ".scpt", ".excludes"}
                               or path.stat().st_mode & 0o111):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            fixture_hashes.setdefault(str(path), set()).add(digest)

def evidence_setup(self):
    global active_fixture
    original_setup(self)
    active_fixture = self
    self.addCleanup(capture_sources)

def observed_popen(self, args, *positional, **kwargs):
    capture_sources()
    processes.append({"args": args, "cwd": str(kwargs.get("cwd") or Path.cwd())})
    return original_popen(self, args, *positional, **kwargs)

addendum.Fixture.setUp = evidence_setup
subprocess.Popen.__init__ = observed_popen

def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item

native = {
    "LockedReleaseTest.test_compiled_app_full_source_equals_saved_source",
    "LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change",
    "LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest",
    "LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog",
}
focus = [
    "LockedReleaseTest.test_builder_compares_fresh_saved_compile_with_newline_growth",
    "LockedReleaseTest.test_builder_rejects_app_decompile_byte_mismatch",
    "LockedReleaseTest.test_builder_rejects_empty_canonical_decompile",
]
if selector == "focus":
    suite = unittest.defaultTestLoader.loadTestsFromNames(focus, addendum)
    excluded = []
elif selector == "non_native":
    included, excluded = [], []
    for test in flatten(unittest.defaultTestLoader.loadTestsFromModule(addendum)):
        name = test.id().removeprefix(addendum.__name__+".")
        method = getattr(test, test._testMethodName)
        if name in native or getattr(method, "__unittest_skip__", False):
            excluded.append({"test": test.id(), "reason": "native AppleScript UNRUN" if name in native
                             else getattr(method, "__unittest_skip_why__")})
        else:
            included.append(test)
    suite = unittest.TestSuite(included)
else:
    raise ValueError("selector must be focus or non_native")
save("suite_selection.json", {"selector": selector, "count": suite.countTestCases(),
                             "excluded": excluded, "native_tests_enabled": False})
with (RUN/"test.log").open("w") as stream:
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
metadata["fixture_source_sha256"] = {path: sorted(values) for path, values in fixture_hashes.items()}
metadata["source_sha256_after"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in paths}
save("command.json", metadata)
save("started_commands.json", processes)
summary = {"testsRun": result.testsRun, "passed": result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
           "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
           "failure_tests": [test.id() for test, detail in result.failures],
           "error_tests": [test.id() for test, detail in result.errors],
           "sources_unchanged_during_run": hashes == metadata["source_sha256_after"],
           "native": "UNRUN", "ps": "UNAVAILABLE: /bin/ps denied per MB35 brief",
           "success": result.wasSuccessful() and hashes == metadata["source_sha256_after"]}
save("result.json", summary)
print(json.dumps(summary, indent=2))
sys.exit(0 if summary["success"] else 1)

