"""MB32 isolated Python 3.9 runner with per-test process-group clearance."""
import datetime
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import time
import unittest

RECEIPT = Path(__file__).resolve().parent
ROOT = RECEIPT.parents[2]
RUN = RECEIPT/sys.argv[1]
RUN.mkdir()
home = RUN/"home"
home.mkdir()
fixtures = RUN/"fixtures"
fixtures.mkdir()
os.environ.update(HOME=str(home), LLMDB_ROOT=str(ROOT), BACKUP_TEST_NO_RCLONE="1",
                  PYTHONDONTWRITEBYTECODE="1", BACKUP_TEST_RECEIPTS=str(fixtures),
                  BACKUP_PYTHON="/usr/bin/python3", MB28_BACKUP_PYTHON="/usr/bin/python3")
assert sys.flags.dont_write_bytecode
assert sys.version_info[:2] == (3, 9), sys.version
sys.path.insert(0, str(ROOT))

def save(name, value):
    (RUN/name).write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")

save("command.json", {"argv":["/usr/bin/python3", "-B", *sys.argv], "cwd":str(Path.cwd()),
    "env":{k:os.environ[k] for k in ["HOME", "LLMDB_ROOT", "BACKUP_TEST_NO_RCLONE",
           "PYTHONDONTWRITEBYTECODE", "BACKUP_TEST_RECEIPTS", "BACKUP_PYTHON", "MB28_BACKUP_PYTHON"]},
    "python_version":sys.version, "runner_pid":os.getpid()})
started = []
original_popen = subprocess.Popen.__init__
active_test = None
active_fixture = None
observed_children = {}

def observe_children():
    if active_fixture is None:
        return
    heartbeat = getattr(active_fixture, "heartbeat", None)
    if heartbeat is None or not heartbeat.is_file():
        return
    try:
        value = json.loads(heartbeat.read_text())
    except (ValueError, OSError):
        # Intentionally malformed/unreadable heartbeat fixtures contain no trusted PID.
        return
    if not isinstance(value, dict):
        return
    child, owner = value.get("rclone_pid"), value.get("owner_pid")
    groups = {r["pid"] for p, r in started if r["test"] == active_test}
    if type(child) is int and child > 0 and owner in groups and child not in groups:
        observed_children[child] = {"pid":child, "owner_pid":owner, "pgid":owner,
            "test":active_test, "source":str(heartbeat), "role":"owned fixture rclone child"}

def record_popen(self, *args, **kwargs):
    command = kwargs.get("args", args[0] if args else [])
    argv = list(command) if isinstance(command, (list, tuple)) else [str(command)]
    forbidden = {"/opt/homebrew/bin/rclone", "launchctl", "/bin/launchctl", "/usr/bin/open"}
    if any(str(a) in forbidden for a in argv):
        raise RuntimeError("Forbidden real rclone/activation command: "+repr(argv))
    # Every directly launched process has an owned group, including test git repos.
    kwargs["start_new_session"] = True
    original_popen(self, *args, **kwargs)
    record = {"pid":self.pid, "pgid":self.pid, "argv":argv, "test":active_test,
              "started_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    started.append((self, record))
    observe_children()
    with (RUN/"started_processes.jsonl").open("a") as stream:
        stream.write(json.dumps(record)+"\n")

subprocess.Popen.__init__ = record_popen

def group_alive(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False

class ClearedResult(unittest.TextTestResult):
    def startTest(self, test):
        global active_test, active_fixture
        active_test = test.id()
        active_fixture = None
        self.first_process = len(started)
        super().startTest(test)

    def stopTest(self, test):
        clearance = []
        leaked = []
        for proc, record in started[self.first_process:]:
            record["returncode"] = proc.poll()
            # Reaping the leader plus an absent group proves all in-group children exited.
            deadline = time.monotonic()+0.5
            while group_alive(record["pgid"]) and time.monotonic() < deadline:
                time.sleep(0.01)
                proc.poll()
            alive = group_alive(record["pgid"])
            record["group_alive_after_test"] = alive
            record["returncode"] = proc.poll()
            if alive or record["returncode"] is None:
                leaked.append(dict(record))
                # Cleanup only the group created by this runner; the test remains failed.
                if alive:
                    os.killpg(record["pgid"], signal.SIGKILL)
                proc.wait(timeout=5)
                record["cleanup_after_failure"] = True
            record["group_alive_after_cleanup"] = group_alive(record["pgid"])
            clearance.append(record)
        with (RUN/"process_clearance.jsonl").open("a") as stream:
            children = [r for r in observed_children.values() if r["test"] == test.id()]
            for child in children:
                try:
                    os.kill(child["pid"], 0)
                    child["alive_after_test"] = True
                    leaked.append(dict(child))
                except ProcessLookupError:
                    child["alive_after_test"] = False
            stream.write(json.dumps({"test":test.id(), "processes":clearance,
                                     "observed_children":children, "leaks":leaked})+"\n")
        if leaked:
            try:
                raise AssertionError("test left owned processes alive: "+repr(leaked))
            except AssertionError:
                self.addFailure(test, sys.exc_info())
        super().stopTest(test)

import tools.test_backup_gdrive_addendum as addendum
original_fixture_setup = addendum.Fixture.setUp
def evidence_setup(self):
    global active_fixture
    original_fixture_setup(self)
    active_fixture = self
    def snapshot():
        observe_children()
        if isinstance(self, addendum.LockedReleaseTest):
            output = RUN/"fixture_artifacts"/self._testMethodName
            output.mkdir(parents=True)
            files = list(self.base.glob("*.applescript"))
            for attr in ["counter", "receipt", "marker"]:
                path = getattr(self, attr, None)
                if path is not None and path.is_file():
                    files.append(path)
            for path in files:
                shutil.copyfile(path, output/path.name)
            if self.release.is_dir():
                shutil.copytree(self.release, output/"release")
    self.addCleanup(snapshot)
addendum.Fixture.setUp = evidence_setup
selector = sys.argv[2] if len(sys.argv) > 2 else "all"
if len(sys.argv) > 3 and sys.argv[3] == "--original-launcher":
    assert selector == "LockedReleaseTest"
    addendum.ROOT = RECEIPT/"before"
if selector == "all":
    suite = unittest.defaultTestLoader.loadTestsFromModule(addendum)
else:
    suite = unittest.defaultTestLoader.loadTestsFromName(selector, addendum)
save("suite_selection.json", {"selector":selector, "test_count":suite.countTestCases(),
    "native_tests_enabled":True, "real_rclone_disabled":addendum.NO_RCLONE})
with (RUN/"test.log").open("w") as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2, resultclass=ClearedResult).run(suite)
clear = all(r.get("returncode") is not None and not r.get("group_alive_after_test", True)
            and not r.get("group_alive_after_cleanup", True) for p, r in started)
summary = {"testsRun":result.testsRun, "failures":len(result.failures), "errors":len(result.errors),
    "skipped":len(result.skipped), "skips":[{"test":t.id(), "reason":reason} for t, reason in result.skipped],
    "failure_tests":[t.id() for t, reason in result.failures],
    "error_tests":[t.id() for t, reason in result.errors], "direct_process_count":len(started),
    "all_owned_groups_exited":clear, "ps":"UNAVAILABLE: sandbox denied /bin/ps",
    "success":result.wasSuccessful() and clear}
exit_code = 0 if summary["success"] else 1
summary["exit_code"] = exit_code
save("result.json", summary)
save("process_clearance.json", {"runner_pid":os.getpid(), "runner_expected_exit":exit_code,
    "records":[r for p, r in started], "all_owned_groups_exited":clear,
    "observed_children":list(observed_children.values()),
    "scope":"direct Popen processes and their complete session groups; no detached/native open launches",
    "operator_pids_not_touched":[32906,32913,32914,36233,36258,36259,37109,65807]})
print(json.dumps(summary, indent=2))
sys.exit(exit_code)
