"""MB34: exercise the receipt auditor with real, fixture-owned process groups."""
import ast
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest

RECEIPT = Path(__file__).resolve().parent
RUN = RECEIPT/sys.argv[1]
RUN.mkdir()
SOURCE = Path(sys.argv[2]).resolve()
NAMES = {"observe_children", "owned_child_alive", "group_alive", "ClearedResult"}
# Load these exact definitions without the runner's command-line side effects.
definitions = [node for node in ast.parse(SOURCE.read_text()).body
               if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in NAMES]
code = compile(ast.Module(body=definitions, type_ignores=[]), str(SOURCE), "exec")
(RUN/"command.json").write_text(json.dumps({
    "command":shlex.join(["/usr/bin/python3", "-B", *sys.argv]),
    "cwd":str(Path.cwd()), "interpreter":sys.executable,
    "source":str(SOURCE), "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "fixture_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}, indent=2)+"\n")


class ClearanceAuditorTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="mb34_auditor_", dir="/private/tmp")
        self.addCleanup(self.temporary.cleanup)
        self.heartbeat = Path(self.temporary.name)/"heartbeat.json"
        self.output = RUN/self._testMethodName
        self.output.mkdir()
        self.scope = dict(os=os, sys=sys, json=json, signal=signal, time=time, unittest=unittest,
                          RUN=self.output, started=[], observed_children={},
                          active_test=None, active_fixture=None)
        exec(code, self.scope)
        self.case = unittest.FunctionTestCase(lambda: None)
        self.result = self.scope["ClearedResult"](
            unittest.runner._WritelnDecorator(io.StringIO()), True, 2)
        self.result.startTest(self.case)
        self.scope["active_fixture"] = SimpleNamespace(heartbeat=self.heartbeat)

    def process(self, *, group=None, command=None, owned=False):
        # Same-session groups let this fixture reap both leader and child itself.
        proc = subprocess.Popen(command or ["/bin/sleep", "30"],
                                preexec_fn=lambda: os.setpgid(0, group or 0),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        def cleanup():
            if proc.poll() is None:
                proc.kill()
            proc.wait(timeout=5)
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                stream.close()
        self.addCleanup(cleanup)
        if owned:
            self.scope["started"].append((proc, {"pid":proc.pid, "pgid":proc.pid,
                                                "test":self.case.id()}))
        return proc

    def observe(self, owner, child):
        self.heartbeat.write_text(json.dumps({"owner_pid":owner, "rclone_pid":child}))
        self.scope["observe_children"]()

    def audit(self):
        self.result.stopTest(self.case)
        return json.loads((self.output/"process_clearance.jsonl").read_text())

    def test_runner_pid_is_not_an_observed_child(self):
        owner = self.process(owned=True)
        self.observe(owner.pid, os.getpid())
        self.assertNotIn(os.getpid(), self.scope["observed_children"])

    def test_live_pid_outside_owned_group_is_not_observed(self):
        owner = self.process(owned=True)
        outsider = self.process()
        self.assertNotEqual(os.getpgid(outsider.pid), owner.pid)
        self.observe(owner.pid, outsider.pid)
        self.assertNotIn(outsider.pid, self.scope["observed_children"])

    def test_final_audit_excludes_runner_pid(self):
        owner = self.process(command=["/usr/bin/true"], owned=True)
        owner.wait(timeout=5)
        self.scope["observed_children"][os.getpid()] = {
            "pid":os.getpid(), "pgid":owner.pid, "test":self.case.id()}
        self.assertEqual(self.audit()["leaks"], [])
        self.assertEqual(len(self.result.failures), 0)

    def test_final_audit_rechecks_group_after_child_moves(self):
        owner = self.process(owned=True)
        child = self.process(group=owner.pid, command=["/usr/bin/python3", "-B", "-c",
            'import os, sys, time; print("ready", flush=True); sys.stdin.readline(); '
            'os.setpgid(0, 0); print("moved", flush=True); time.sleep(30)'])
        self.assertEqual(child.stdout.readline().strip(), "ready")
        self.observe(owner.pid, child.pid)
        self.assertIn(child.pid, self.scope["observed_children"])
        child.stdin.write("move\n")
        child.stdin.flush()
        self.assertEqual(child.stdout.readline().strip(), "moved")
        self.assertNotEqual(os.getpgid(child.pid), owner.pid)
        owner.terminate()
        owner.wait(timeout=5)
        self.assertEqual(self.audit()["leaks"], [])
        self.assertEqual(len(self.result.failures), 0)

    def test_genuinely_leaked_owned_child_is_reported(self):
        owner = self.process(owned=True)
        child = self.process(group=owner.pid)
        original_wait = owner.wait
        def reap_fixture_group(timeout):
            result = original_wait(timeout=timeout)
            # Both fixture processes are our direct children, so reap both before
            # the sandbox is asked to probe an otherwise zombie-only group.
            child.wait(timeout=timeout)
            return result
        owner.wait = reap_fixture_group
        self.assertEqual(os.getpgid(child.pid), owner.pid)
        self.observe(owner.pid, child.pid)
        self.assertIn(child.pid, self.scope["observed_children"])
        clearance = self.audit()
        self.assertEqual(len(self.result.failures), 1)
        self.assertIn(child.pid, [record["pid"] for record in clearance["leaks"]])
        self.assertTrue(clearance["processes"][0]["cleanup_after_failure"])
        child.wait(timeout=5)
        owner.wait(timeout=5)
        self.assertFalse(self.scope["group_alive"](owner.pid))


with (RUN/"test.log").open("w") as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ClearanceAuditorTest))
summary = {"testsRun":result.testsRun, "failures":len(result.failures),
           "errors":len(result.errors), "skipped":len(result.skipped),
           "exit_code":0 if result.wasSuccessful() else 1}
(RUN/"result.json").write_text(json.dumps(summary, indent=2)+"\n")
print(json.dumps(summary, indent=2))
sys.exit(summary["exit_code"])
