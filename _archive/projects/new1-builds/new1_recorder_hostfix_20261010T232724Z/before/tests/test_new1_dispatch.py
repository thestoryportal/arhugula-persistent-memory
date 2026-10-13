"""MB33: real shell/process boundaries in temporary roots; no real NEW1 launch.

PureTests uses synthetic classifier inputs, never an invented host inventory.
DispatchTests requires a process-visible host and a niceness-zero parent.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import types
import unittest

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
gate_path = SOURCE/"tools/c10w_p2_gate.py"
gate = types.ModuleType("dispatch_gate_under_test")
gate.__file__ = str(gate_path)
exec(compile(gate_path.read_bytes(), str(gate_path), "exec"), gate.__dict__)
blocking_processes = gate.blocking_processes

PIN = "1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f"
ENV = dict(PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
           TMPDIR="/private/tmp", LLMDB_DEVICE="cpu", CUDA_VISIBLE_DEVICES="",
           OMP_NUM_THREADS="8", MKL_NUM_THREADS="8", PYTHONDONTWRITEBYTECODE="1")

WORKER = '''import json, os, signal, time
from pathlib import Path
root = Path(os.environ["LLMDB_ROOT"])
cfg = json.loads((root/"fixture.json").read_text())
signal.signal(signal.SIGTERM, lambda *args: exit(0))
if cfg.get("mode") == "unreaped":
    while not (root/"release_worker").exists(): time.sleep(.02)
else:
    time.sleep(.65)
'''

FINGERPRINT = '''import json, os, sys
from pathlib import Path
root = Path(os.environ["LLMDB_ROOT"])
cfg = json.loads((root/"fixture.json").read_text())
if cfg.get("change_hash"):
    with (root/"tools/new1_geometry.py").open("a") as target: target.write("\\n# changed at fingerprint check\\n")
print("fixture fingerprint")
sys.exit(3 if cfg.get("fingerprint_refused") else 0)
'''

ADMIT = '''import json
from pathlib import Path
def probe(kind):
    cfg = json.loads((Path(__file__).parents[1]/"fixture.json").read_text())
    return {"allowed": not cfg.get("dry_refused", False), "reasons": [],
            "checks": {"gpu": {"blocking_processes": []}}}
'''

SUPERVISOR = '''import json, os, signal, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
root = Path(os.environ["LLMDB_ROOT"])
cfg = json.loads((root/"fixture.json").read_text())
run = root/"results/mathlab_staging/runs"/("new1_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
run.mkdir(exist_ok=False)
(root/"supervisor_started").write_text(str(os.getpid()))
keys = ["PATH", "TMPDIR", "LLMDB_ROOT", "LLMDB_DEVICE", "CUDA_VISIBLE_DEVICES",
        "OMP_NUM_THREADS", "MKL_NUM_THREADS", "PYTHONDONTWRITEBYTECODE"]
(root/"executed_command.json").write_text(json.dumps({"argv": sys.argv,
    "executable": sys.executable, "cwd": os.getcwd(), "env": {key:os.environ.get(key) for key in keys},
    "nice": os.getpriority(os.PRIO_PROCESS, 0), "sigint_handler": str(signal.getsignal(signal.SIGINT))}))
inventory = subprocess.run(["/bin/ps", "-axo", "pid=,ppid=,pgid=,nice=,command="], capture_output=True, text=True)
if inventory.returncode: raise RuntimeError(inventory.stderr)
(root/"recorder_inventory.txt").write_text(inventory.stdout)
def event(kind, **fields):
    row = dict(type=kind, schema=1, run_id=run.name,
               ts=datetime.now(timezone.utc).isoformat(), **fields)
    with (run/"events.jsonl").open("a") as target: target.write(json.dumps(row)+"\\n")
event("run_started", step=4, title="NEW1 fixture", purpose="experiment",
      deadline_ts="2099-01-01T00:00:00Z", pid=os.getpid())
worker = None
def interrupted(*args):
    (root/"sigint_received").write_text(str(os.getpid()))
    raise KeyboardInterrupt()
signal.signal(signal.SIGINT, interrupted)
code = "PASS"
try:
    if cfg.get("mode") == "admission":
        code = "INVALID-ADMISSION"
    else:
        worker = subprocess.Popen(["/usr/bin/nice", "-n", str(cfg.get("worker_nice", 10)),
            sys.executable, "-B", str(root/"tools/new1_geometry.py")], start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (root/"worker_pid").write_text(str(worker.pid))
        if cfg.get("mode") == "unreaped": time.sleep(.4)
        else: worker.wait(timeout=4)
        if cfg.get("mode") == "deadline": code = "STOPPED-DEADLINE"
        if cfg.get("mode") == "resource": code = "STOPPED-RESOURCE"
except KeyboardInterrupt:
    code = "OPERATOR"
finally:
    if worker is not None and cfg.get("mode") != "unreaped":
        if worker.poll() is None: os.killpg(worker.pid, signal.SIGTERM)
        worker.wait(timeout=4)
if code == "PASS": event("run_finished", outcome="PASS", summary="fixture complete")
elif code == "STOPPED-DEADLINE": print(code+": fixture expired; no prediction verdict", file=sys.stderr)
else: event("halted", reason=code+": fixture stop", diagnostic_path="fixture")
print(code, flush=True)
if cfg.get("mode") == "unreaped": os._exit(0)
sys.exit(0 if code == "PASS" else 3)
'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def provenance(root, name):
    """Persist the bytes of generated, executing fixtures before temp cleanup."""
    destination = os.environ.get("NEW1_TEST_PROVENANCE")
    if not destination:
        return
    folder = Path(destination)/name
    folder.mkdir(parents=True, exist_ok=False)
    entries = []
    for path in sorted((root/"tools").glob("*.py")) + list((root/"tools").glob("*.sh")):
        copy = folder/path.name
        shutil.copyfile(path, copy)
        entries.append(dict(path=str(path), sha256=sha(path), preserved_as=str(copy)))
    (folder/"sources.json").write_text(json.dumps(entries, indent=2)+"\n")


def load_report():
    path = SOURCE/"tools/new1_dispatch_report.py"
    module = types.ModuleType("dispatch_report_under_test")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def start_event(name="new1_fixture"):
    return dict(type="run_started", schema=1, run_id=name, ts="2026-10-10T00:00:00Z",
                step=4, title="NEW1 fixture", purpose="experiment",
                deadline_ts="2099-01-01T00:00:00Z", pid=123)


def terminal(kind="run_finished", outcome="PASS", name="new1_fixture"):
    row = dict(type=kind, schema=1, run_id=name, ts="2026-10-10T00:00:01Z")
    if kind == "run_finished": row.update(outcome=outcome, summary="fixture")
    if kind == "halted": row.update(reason=outcome+": fixture", diagnostic_path="fixture")
    return row


class PureTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SOURCE/"tools/new1_dispatch.sh").is_file(), "recorder missing (expected RED)")
        self.assertTrue((SOURCE/"tools/new1_dispatch_report.py").is_file(), "reporter missing (expected RED)")
        self.report = load_report()

    def test_T1_shell_argv_is_not_a_compute_executable(self):
        # A declared fixture command for the pure classifier, not host clearance.
        line = "123 /bin/zsh /private/tmp/new1_fixture/tools/new1_dispatch.sh hashes.sha256 HEAD auth"
        self.assertEqual(blocking_processes(line, own_pid=456), [])
        self.assertEqual(blocking_processes("123 /usr/bin/python3 poller.py", own_pid=456),
                         ["123 /usr/bin/python3 poller.py"])

    def classify(self, events, stdout="PASS\n", stderr="", status=0):
        return self.report.classify(events, [], stdout, stderr, status)

    def test_terminal_stdout_exit_agree(self):
        result = self.classify([start_event(), terminal()])
        self.assertEqual(result["verdict_status"], "COMPLETE")
        self.assertFalse(result["counts_as_abort"])

    def test_artifacts_without_terminal_never_complete(self):
        result = self.classify([start_event()])
        self.assertEqual(result["verdict_status"], "INCOMPLETE")
        self.assertEqual(result["prediction_verdict"], "no prediction verdict")

    def test_terminal_exit_mismatch_incomplete(self):
        self.assertEqual(self.classify([start_event(), terminal()], status=3)["verdict_status"], "INCOMPLETE")

    def test_T6_deadline_stderr_without_halt_counts_abort(self):
        result = self.classify([start_event()], stdout="STOPPED-DEADLINE\n",
                               stderr="STOPPED-DEADLINE: expired", status=3)
        self.assertTrue(result["counts_as_abort"])
        self.assertEqual(result["verdict_status"], "INCOMPLETE")

    def test_T7_resource_halt_counts_abort(self):
        result = self.classify([start_event(), terminal("halted", "STOPPED-RESOURCE")],
                               stdout="STOPPED-RESOURCE\n", status=3)
        self.assertTrue(result["counts_as_abort"])
        self.assertEqual(result["prediction_verdict"], "no prediction verdict")

    def test_T8_admission_refusal_not_abort(self):
        result = self.classify([start_event(), terminal("halted", "INVALID-ADMISSION")],
                               stdout="INVALID-ADMISSION\n", status=3)
        self.assertFalse(result["counts_as_abort"])

    def test_unmatched_finishing_after_terminal_incomplete(self):
        self.assertEqual(self.classify([start_event(), terminal(), terminal("run_finishing")])["verdict_status"], "INCOMPLETE")

    def test_invalid_event_stream_never_complete(self):
        result = self.report.classify([start_event(), terminal()], ["torn JSON"], "PASS\n", "", 0)
        self.assertEqual(result["verdict_status"], "INCOMPLETE")

    def test_stdout_abort_evidence_survives_missing_terminal(self):
        self.assertTrue(self.classify([start_event()], stdout="STOPPED-RESOURCE\n", status=3)["counts_as_abort"])

    def test_no_exit_status_never_complete(self):
        self.assertEqual(self.classify([start_event(), terminal()], status=None)["verdict_status"], "INCOMPLETE")

    def history_receipt(self, old_halt, prior_receipt, unique_namespace=True):
        temp = tempfile.TemporaryDirectory(prefix="new1-report-", dir="/private/tmp")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root/"tools").mkdir()
        shutil.copyfile(SOURCE/"tools/mathlab_events.py", root/"tools/mathlab_events.py")
        runs = root/"results/mathlab_staging/runs"
        current = runs/"new1_current"
        old = runs/"new1_old"
        for run, rows in ((current, [start_event(current.name), terminal(name=current.name)]),
                          (old, [start_event(old.name)]+([terminal("halted", "STOPPED-RESOURCE", old.name)] if old_halt else []))):
            run.mkdir(parents=True)
            (run/"events.jsonl").write_text("".join(json.dumps(row)+"\n" for row in rows))
        dispatch = root/"results/mathlab_staging/new1_dispatch_current"
        dispatch.mkdir()
        for name, data in (("invocation.json", {"authorization": {"sha256":"a"*64}}),
                           ("supervisor_exit.json", {"status":0,"exited":True}),
                           ("namespace.json", {"path":str(current) if unique_namespace else None,
                                               "candidates":[str(current)], "anomaly":None if unique_namespace else "several"}),
                           ("worker.json", {"status":"NONE_OBSERVED"}),
                           ("supervisor.json", {"pid":123,"nice":0}),
                           ("disposition.json", {"status":"CLEAN","live_processes":[]})):
            (dispatch/name).write_text(json.dumps(data))
        (dispatch/"supervisor_stdout.log").write_text("PASS\n")
        (dispatch/"supervisor_stderr.log").write_text("")
        if prior_receipt:
            previous = root/"results/mathlab_staging/new1_dispatch_previous"
            previous.mkdir()
            (previous/"dispatch_receipt.json").write_text(json.dumps({
                "authorization_consumed":True, "namespace":{"path":str(old)},
                "abort_accounting":{"counts_as_abort":True}}))
        return self.report.build_receipt(root, dispatch)

    def test_prior_receipt_and_halted_namespace_count_once(self):
        self.assertEqual(self.history_receipt(True, True)["abort_accounting"]["prior_aborts"], 1)

    def test_prior_receipt_covers_deadline_without_halted(self):
        self.assertEqual(self.history_receipt(False, True)["abort_accounting"]["prior_aborts"], 1)

    def test_namespace_anomaly_prevents_complete(self):
        self.assertEqual(self.history_receipt(False, False, False)["verdict_status"], "INCOMPLETE")

    def test_pass_without_worker_observation_is_incomplete_and_blocks(self):
        receipt = self.history_receipt(False, False)
        self.assertEqual(receipt["verdict_status"], "INCOMPLETE")
        self.assertEqual(receipt["prediction_verdict"], "no prediction verdict")
        self.assertTrue(receipt["subsequent_compute_blocked"])


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SOURCE/"tools/new1_dispatch.sh").is_file(), "recorder missing (expected RED)")
        self.assertTrue((SOURCE/"tools/new1_dispatch_report.py").is_file(), "reporter missing (expected RED)")
        self.temp = tempfile.TemporaryDirectory(prefix="new1-fixture-", dir="/private/tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in ("tools", ".venv/bin", "results/mathlab_staging/runs"):
            (self.root/path).mkdir(parents=True)
        (self.root/".venv/bin/python").symlink_to(sys.executable)
        for path in ("new1_dispatch.sh", "new1_dispatch_report.py", "mathlab_events.py"):
            shutil.copy2(SOURCE/"tools"/path, self.root/"tools"/path)
        for name, content in (("new1_supervisor.py", SUPERVISOR), ("new1_geometry.py", WORKER),
                              ("engine_fingerprint.py", FINGERPRINT), ("mathlab_admit.py", ADMIT)):
            (self.root/"tools"/name).write_text(content)
        self.config = {}
        self.configure()
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgSign=false", "-c", "core.hooksPath=/dev/null", "commit", "-qm", "fixture")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.hashes = self.root/"hashes.sha256"
        self.hashes.write_text("".join(sha(path)+"  "+str(path.relative_to(self.root))+"\n"
                             for path in sorted((self.root/"tools").glob("*.py"))))
        self.auth = self.root/"authorization.txt"
        self.auth.write_text("ONE FIXTURE invocation, no real science\n")
        self.dispatcher = None
        self.addCleanup(self.ensure_processes_exit)
        provenance(self.root, self._testMethodName)

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def configure(self, **values):
        self.config.update(values)
        (self.root/"fixture.json").write_text(json.dumps(self.config))

    def dispatch(self, head=None, env=None, nice=None):
        before = set((self.root/"results/mathlab_staging").glob("new1_dispatch_*"))
        argv = [str(self.root/"tools/new1_dispatch.sh"), str(self.hashes), head or self.head, str(self.auth)]
        if nice is not None: argv = ["/usr/bin/nice", "-n", str(nice), *argv]
        self.dispatcher = subprocess.Popen(argv, cwd=self.root, env=dict(os.environ, **(env or {})),
                                           start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try: out, err = self.dispatcher.communicate(timeout=12)
        except subprocess.TimeoutExpired:
            self.fail("fixture dispatcher exceeded 12 seconds")
        self.output = (out, err)
        after = set((self.root/"results/mathlab_staging").glob("new1_dispatch_*"))
        added = after - before
        self.assertEqual(len(added), 1, (added, out, err))
        self.directory = added.pop()
        return self.dispatcher.returncode

    def receipt(self):
        path = self.directory/"dispatch_receipt.json"
        self.assertTrue(path.is_file(), self.output)
        return json.loads(path.read_text())

    @staticmethod
    def alive(pid):
        try: os.kill(pid, 0)
        except ProcessLookupError: return False
        return True

    def ensure_processes_exit(self):
        # Test cleanup is restricted to fixture-owned PID/group identities.
        (self.root/"release_worker").touch()
        owned = []
        for path in (self.root/"supervisor_started", self.root/"worker_pid"):
            if path.exists(): owned.append(int(path.read_text()))
        deadline = time.monotonic()+3
        while any(self.alive(pid) for pid in owned) and time.monotonic() < deadline:
            time.sleep(.03)
        leaked = [pid for pid in owned if self.alive(pid)]
        if leaked:
            for pid in leaked:
                try: os.kill(pid, signal.SIGKILL)
                except ProcessLookupError: pass
        if self.dispatcher is not None and self.dispatcher.poll() is None:
            leaked.append(self.dispatcher.pid)
            os.killpg(self.dispatcher.pid, signal.SIGKILL)
            self.dispatcher.communicate(timeout=3)
        self.assertEqual(leaked, [], "fixture-owned process leak (cleaned up, still a failure)")

    def refused(self, check, **kwargs):
        self.assertNotEqual(self.dispatch(**kwargs), 0)
        self.assertFalse((self.directory/"invocation.json").exists())
        self.assertFalse((self.root/"supervisor_started").exists())
        refusal = json.loads((self.directory/"refused_before_invocation.json").read_text())
        self.assertTrue(refusal["check"].startswith(check), refusal)
        self.assertFalse(refusal["authorization_consumed"])
        for key in ("command", "stdout", "stderr", "exit"):
            self.assertIn(key, refusal)

    def test_T1_observed_recorder_line_not_blocker(self):
        self.assertEqual(self.dispatch(), 0, self.output)
        pid = json.loads((self.directory/"recorder.json").read_text())["pid"]
        lines = (self.root/"recorder_inventory.txt").read_text().splitlines()
        row = next(line.strip().split(None, 4) for line in lines if line.strip().split(None, 1)[0] == str(pid))
        self.assertEqual(blocking_processes(row[0]+" "+row[4], own_pid=999999999), [])

    def test_T2_happy_path(self):
        self.assertEqual(self.dispatch(), 0, self.output)
        receipt = self.receipt()
        worker = receipt["worker"]
        supervisor = receipt["supervisor"]
        self.assertEqual(supervisor["pid"], int((self.root/"supervisor_started").read_text()))
        self.assertEqual(supervisor["nice"], 0)
        self.assertEqual(worker["pid"], int((self.root/"worker_pid").read_text()))
        self.assertEqual(worker["ppid"], supervisor["pid"])
        self.assertEqual(worker["pgid"], worker["pid"])
        self.assertEqual(worker["nice"], 10)
        self.assertIn("tools/new1_geometry.py", worker["command"])
        self.assertTrue(worker["observed_at_utc"])
        self.assertEqual(receipt["namespace"]["path"], str(next((self.root/"results/mathlab_staging/runs").glob("new1_*"))))
        self.assertEqual(receipt["supervisor_exit"]["status"], 0)
        self.assertEqual(receipt["disposition"]["status"], "CLEAN")
        self.assertEqual(receipt["verdict_status"], "COMPLETE")

    def test_T3_b_reused_authorization(self):
        old = self.root/"results/mathlab_staging/new1_dispatch_old"
        old.mkdir()
        (old/"invocation.json").write_text(json.dumps({"authorization": {"sha256": sha(self.auth)}}))
        self.refused("2b")

    def test_T3_c_wrong_head(self):
        self.refused("2c", head="0"*40)

    def test_T3_c_dirty_pinned_source(self):
        with (self.root/"tools/new1_geometry.py").open("a") as target: target.write("\n# dirty\n")
        self.refused("2c")

    def test_T3_d_bad_manifest_hash(self):
        content = self.hashes.read_text()
        self.hashes.write_text("0"*64+content[64:])
        self.refused("2d")

    def test_T3_f_stricter_disk_floor(self):
        self.refused("2f", env={"NEW1_DISPATCH_MIN_FREE_KIB": str(1 << 50)})

    def test_T3_g_fingerprint_failure(self):
        self.configure(fingerprint_refused=True)
        self.refused("2g")

    def test_T3_h_dry_probe_refusal(self):
        self.configure(dry_refused=True)
        self.refused("2h")

    def test_T3_i_hash_changed_after_first_check(self):
        self.configure(change_hash=True)
        self.refused("2i")
        self.assertEqual(json.loads((self.directory/"2d.json").read_text())["exit"], 0)

    def test_T4_nonzero_recorder_niceness(self):
        self.refused("2e", nice=1)

    def test_disk_floor_cannot_be_lowered(self):
        self.refused("2f", env={"NEW1_DISPATCH_MIN_FREE_KIB": "1"})

    def test_T5_worker_nice_three_requests_supervisor_sigint(self):
        self.configure(worker_nice=3)
        self.assertNotEqual(self.dispatch(), 0)
        receipt = self.receipt()
        self.assertEqual(receipt["worker"]["nice"], 3)
        self.assertEqual(receipt["stop_reason"], "WORKER-NICENESS-MISMATCH")
        self.assertTrue(receipt["authorization_consumed"])
        self.assertEqual(int((self.root/"sigint_received").read_text()), receipt["supervisor"]["pid"])
        self.assertEqual(receipt["disposition"]["status"], "CLEAN")

    def test_T6_deadline_no_halted_event(self):
        self.configure(mode="deadline")
        self.assertEqual(self.dispatch(), 3)
        receipt = self.receipt()
        self.assertEqual(receipt["verdict_status"], "INCOMPLETE")
        self.assertEqual(receipt["prediction_verdict"], "no prediction verdict")
        self.assertTrue(receipt["abort_accounting"]["counts_as_abort"])
        self.assertEqual(receipt["abort_accounting"]["total_aborts"], 1)

    def test_T7_resource_halted_event(self):
        self.configure(mode="resource")
        self.assertEqual(self.dispatch(), 3)
        receipt = self.receipt()
        self.assertEqual(receipt["outcome"]["terminal_event"]["type"], "halted")
        self.assertTrue(receipt["abort_accounting"]["counts_as_abort"])

    def test_T8_internal_admission_refused(self):
        self.configure(mode="admission")
        self.assertEqual(self.dispatch(), 3)
        receipt = self.receipt()
        self.assertTrue(receipt["authorization_consumed"])
        self.assertEqual(receipt["worker"]["status"], "NONE_OBSERVED")
        self.assertFalse(receipt["abort_accounting"]["counts_as_abort"])

    def test_T9_third_abort_reached(self):
        for index in range(2):
            run = self.root/"results/mathlab_staging/runs"/("new1_prior_"+str(index))
            run.mkdir()
            rows = [start_event(run.name), terminal("halted", "STOPPED-RESOURCE", run.name)]
            (run/"events.jsonl").write_text("".join(json.dumps(row)+"\n" for row in rows))
        self.configure(mode="deadline")
        self.assertEqual(self.dispatch(), 3)
        accounting = self.receipt()["abort_accounting"]
        self.assertEqual(accounting["prior_aborts"], 2)
        self.assertEqual(accounting["total_aborts"], 3)
        self.assertTrue(accounting["third_abort_rule_reached"])

    def test_T10_unreaped_group_blocks_compute(self):
        self.configure(mode="unreaped")
        self.assertNotEqual(self.dispatch(), 0)
        receipt = self.receipt()
        self.assertEqual(receipt["disposition"]["status"], "UNREAPED")
        self.assertTrue(receipt["subsequent_compute_blocked"])
        self.assertTrue(receipt["disposition"]["live_processes"])
        (self.root/"release_worker").touch()

    def test_T11_endorsed_argv_cwd_env(self):
        self.assertEqual(self.dispatch(), 0, self.output)
        actual = json.loads((self.root/"executed_command.json").read_text())
        invocation = json.loads((self.directory/"invocation.json").read_text())
        expected_env = dict(ENV, LLMDB_ROOT=str(self.root))
        self.assertEqual(actual["argv"], [str(self.root/"tools/new1_supervisor.py"), "--prereg-sha", PIN])
        self.assertEqual(actual["executable"], str(self.root/".venv/bin/python"))
        self.assertEqual(actual["cwd"], str(self.root))
        self.assertEqual(actual["env"], expected_env)
        self.assertNotEqual(actual["sigint_handler"], str(signal.SIG_IGN))
        self.assertEqual(invocation["argv"], [str(self.root/".venv/bin/python"), "-B", *actual["argv"]])
        self.assertEqual(invocation["env"], expected_env)
        self.assertEqual(invocation["cwd"], str(self.root))
        self.assertEqual(invocation["authorization"]["sha256"], sha(self.auth))
        self.assertEqual(invocation["authorization"]["path"], str(self.auth))


if __name__ == "__main__":
    unittest.main()
