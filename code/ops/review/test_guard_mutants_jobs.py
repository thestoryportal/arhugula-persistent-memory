"""Tests for guard_mutants --jobs N: up to N mutant test runs at once, with the output of --jobs 1.

Every lane is a fixture in a temp directory; no real lane, branch or PR is touched. The test command
runs HOOK in each lane copy: it logs the run's start and end (copy name, pids, time.time()), can wait
for other runs, and then judges the copy's pkg/mod.py. Overlap is proved from those logged times and
from barriers that only runs in flight together can pass, never from a wall-clock threshold.
"""
from __future__ import annotations

import contextlib
import errno
import fcntl
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import unittest
from unittest import mock

import guard_mutants as gm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "tests"))
import fault_kit as fk  # noqa: E402  (code/tests/fault_kit.py: the standard filesystem attacks)

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard_mutants.py")

# Each `if` gives a negate-if mutant (its line) and a raise-remove mutant (the next line): runs m0002..m0011
# in sorted mutant order (m0001 is the baseline). The judge checks check(0) and guards 1-3, so the
# raise-remove mutants of guards 4 and 5 survive.
MOD = textwrap.dedent("""\
    def check(n):
        if n == 1:
            raise ValueError("one")
        if n == 2:
            raise ValueError("two")
        if n == 3:
            raise ValueError("three")
        if n == 4:
            raise ValueError("four")
        if n == 5:
            raise ValueError("five")
        return n
    """)
RUN_OF = {f"m{i + 2:04d}": mid for i, mid in enumerate([
    "pkg/mod.py:2:4:negate-if", "pkg/mod.py:3:8:raise-remove", "pkg/mod.py:4:4:negate-if",
    "pkg/mod.py:5:8:raise-remove", "pkg/mod.py:6:4:negate-if", "pkg/mod.py:7:8:raise-remove",
    "pkg/mod.py:8:4:negate-if", "pkg/mod.py:9:8:raise-remove", "pkg/mod.py:10:4:negate-if",
    "pkg/mod.py:11:8:raise-remove"])}

HOOK = textwrap.dedent("""\
    import importlib.util, json, os, sys, time
    log, plan_path, tool = sys.argv[1], sys.argv[2], int(sys.argv[3])
    name = os.path.basename(os.path.dirname(os.getcwd()))  # the copy is <scratch>/mNNNN/lane
    with open(plan_path) as fh:
        plan = json.load(fh).get(name, [])

    def note(**ev):
        ev.update(name=name, t=time.time())
        fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        os.write(fd, (json.dumps(ev) + "\\n").encode())
        os.close(fd)

    def events():
        with open(log) as fh:
            return [json.loads(line) for line in fh]

    def until(cond, cap):
        end = time.time() + cap
        while not cond():
            if time.time() > end:
                note(ev="gave-up")
                return
            time.sleep(0.01)

    def gone(pid):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        return False

    def judge():
        spec = importlib.util.spec_from_file_location("mod", os.path.join("pkg", "mod.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            if mod.check(0) != 0:
                return 1
        except ValueError:
            return 1
        for k in (1, 2, 3):
            try:
                mod.check(k)
                return 1
            except ValueError:
                pass
        return 0

    note(ev="start", pid=os.getpid(), group=os.getpgrp(), tool=tool, held=os.path.isfile("pkg/mod.py"))
    rc = None
    for op, *a in plan:
        if op == "barrier":  # wait until a[0] mutant runs have started
            until(lambda: sum(e["ev"] == "start" and e["name"] != "m0001" for e in events()) >= a[0], a[1])
        elif op == "await_end":
            until(lambda: any(e["ev"] == "end" and e["name"] == a[0] for e in events()), a[1])
        elif op == "await_dead":
            pid = next(e["pid"] for e in events() if e["ev"] == "start" and e["name"] == a[0])
            until(lambda: gone(pid), a[1])
            note(ev="saw-dead", of=a[0])
        elif op == "hang":
            time.sleep(10)  # bounded: a tool that never kills it still ends
        elif op == "sleep":
            time.sleep(a[0])
        elif op == "mkdir":
            os.mkdir(os.path.join("..", a[0]))
        elif op == "mark":
            note(ev="mark", what=a[0])
    rc = judge()
    note(ev="end", rc=rc)
    sys.exit(rc)
    """)

CAP = 3  # seconds a hook waits for other runs before it gives up (and the test then fails)
# A tool that waits too long (a gate mutant) must fail this file fast, never outlive the gate's timeout:
# a SIGKILLed test run skips its cleanups and leaves its temp directory. Each test gets an alarm of at
# most PER_TEST seconds, and all of them together at most BUDGET.
PER_TEST, BUDGET = 30.0, 60.0
_DEADLINE: list[float] = []


class OverTime(Exception):
    pass


def _overtime(signum, frame):
    raise OverTime("the test ran past its time budget")


def max_overlap(events: list[dict]) -> int:
    """The most mutant runs whose logged [start, end] intervals hold one moment (an end sorts first)."""
    marks = [(e["t"], e["ev"] == "start") for e in events if e["name"] != "m0001" and e["ev"] in ("start", "end")]
    level = peak = 0
    for _, starts in sorted(marks):
        level += 1 if starts else -1
        peak = max(peak, level)
    return peak


class Base(unittest.TestCase):
    def setUp(self):
        _DEADLINE[:] = _DEADLINE or [time.monotonic() + BUDGET]
        left = _DEADLINE[0] - time.monotonic()
        if left <= 0:
            self.fail("this file's time budget is spent")
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="gm-jobs-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.addCleanup(self.stop_leftovers)  # runs before the removal: no child outlives the test
        signal.signal(signal.SIGALRM, _overtime)
        signal.setitimer(signal.ITIMER_REAL, min(PER_TEST, left))
        self.addCleanup(signal.setitimer, signal.ITIMER_REAL, 0)  # runs first: no alarm during cleanup
        self.lane = os.path.join(self.tmp, "lane")
        self.tooltmp = os.path.join(self.tmp, "tooltmp")
        self.outdir = os.path.join(self.tmp, "outdir")
        for d in (os.path.join(self.lane, "pkg"), self.tooltmp, self.outdir):
            os.makedirs(d)
        with open(os.path.join(self.lane, "pkg", "mod.py"), "w") as fh:
            fh.write(MOD)
        self.hook = os.path.join(self.tmp, "hook.py")
        with open(self.hook, "w") as fh:
            fh.write(HOOK)
        self.log = os.path.join(self.tmp, "runs.log")
        self.plan_path = os.path.join(self.tmp, "plan.json")
        self.plan()
        self.out = os.path.join(self.outdir, "out.json")

    def plan(self, **steps):
        with open(self.plan_path, "w") as fh:
            json.dump(steps, fh)

    def cmd(self) -> str:
        return f"{sys.executable} -B -I {self.hook} {self.log} {self.plan_path} $PPID"

    def args(self, *extra, out=None) -> list[str]:
        return ["--file", "pkg/mod.py", "--test", self.cmd(), "--out", out or self.out, *extra]

    def run_main(self, argv):
        old = os.getcwd()
        os.chdir(self.lane)
        self.addCleanup(os.chdir, old)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(tempfile, "tempdir", self.tooltmp):
            code = gm.main(argv)
        os.chdir(old)
        return code, out.getvalue(), err.getvalue()

    def run_tool(self, argv) -> subprocess.CompletedProcess:
        env = dict(os.environ, TMPDIR=self.tooltmp)
        env.pop("PYTHONPATH", None)
        return subprocess.run([sys.executable, "-B", TOOL, *argv], cwd=self.lane, env=env,
                              capture_output=True, text=True, timeout=PER_TEST)

    def events(self) -> list[dict]:
        if not os.path.exists(self.log):
            return []
        with open(self.log) as fh:
            return [json.loads(line) for line in fh]

    def started(self) -> dict[str, dict]:
        return {e["name"]: e for e in self.events() if e["ev"] == "start"}

    def rows(self, out=None) -> list[dict]:
        with open(out or self.out) as fh:
            return json.load(fh)

    def stop_leftovers(self):
        """Kill the group of each logged run still alive, and reap each one that is this process's child."""
        for e in self.started().values():
            with contextlib.suppress(ProcessLookupError, PermissionError):
                if os.getpgid(e["pid"]) == e["group"]:
                    os.killpg(e["group"], signal.SIGKILL)
            with contextlib.suppress(ChildProcessError):
                os.waitpid(e["group"], 0)

    def assertReaped(self, pid: int):
        with self.assertRaises(ChildProcessError):
            os.waitpid(pid, os.WNOHANG)

    def assertGone(self, pid: int):
        """pid names no process within 10 s (a killed grandchild is reaped by init, not by us)."""
        end = time.monotonic() + 10
        while time.monotonic() < end:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.02)
        self.fail(f"process {pid} is still alive")

    @contextlib.contextmanager
    def flight(self):
        """Count the tool's children that are spawned and not yet reaped: box["peak"] is the most at once."""
        box = {"live": 0, "peak": 0}
        real = gm.subprocess.Popen

        class Counted(real):
            def __init__(proc, *a, **kw):
                super().__init__(*a, **kw)
                proc.counted = True
                box["live"] += 1
                box["peak"] = max(box["peak"], box["live"])

            def wait(proc, *a, **kw):
                code = super().wait(*a, **kw)
                if proc.counted:
                    proc.counted = False
                    box["live"] -= 1
                return code
        with mock.patch.object(gm.subprocess, "Popen", Counted):
            yield box

    def assertNoGiveUp(self):
        self.assertEqual([e for e in self.events() if e["ev"] == "gave-up"], [])


class Jobs(Base):
    def test_jobs_must_be_an_integer_of_at_least_1(self):
        for value in ("0", "-1", "x", "1.5", ""):
            with self.subTest(value=value):
                proc = self.run_tool(self.args("--jobs", value))
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn("--jobs", proc.stderr)
                self.assertNotIn("Traceback", proc.stderr)
                self.assertEqual(self.events(), [])  # no test run
                self.assertFalse(os.path.exists(self.out))

    def test_up_to_n_runs_at_once_and_never_more(self):
        for jobs in (2, 3):
            with self.subTest(jobs=jobs):
                self.setUp()
                # The first `jobs` mutant runs each wait until `jobs` mutant runs have started.
                self.plan(**{f"m{i:04d}": [["barrier", jobs, CAP]] for i in range(2, 2 + jobs)})
                with self.flight() as flight:
                    code, out, err = self.run_main(self.args("--jobs", str(jobs)))
                self.assertEqual(code, 1, err)
                self.assertNoGiveUp()
                self.assertEqual(max_overlap(self.events()), jobs)  # at least jobs at once, from the logged times
                self.assertEqual(flight["peak"], jobs)  # never more: unreaped children when each one is spawned
                self.assertEqual(set(self.started()), {"m0001", *RUN_OF})

    def test_jobs_1_runs_one_at_a_time(self):
        code, out, err = self.run_main(self.args("--jobs", "1"))
        self.assertEqual(code, 1, err)
        events = [e for e in self.events() if e["ev"] in ("start", "end")]
        self.assertEqual([(e["ev"], e["name"]) for e in events],
                         [(ev, n) for n in ["m0001", *RUN_OF] for ev in ("start", "end")])
        self.assertEqual(max_overlap(events), 1)

    def test_default_is_the_least_of_4_and_the_cpu_count(self):
        for cpus, expected in ((2, 2), (16, 4), (None, 1)):
            with self.subTest(cpus=cpus):
                self.setUp()
                if expected > 1:
                    self.plan(**{f"m{i:04d}": [["barrier", expected, CAP]] for i in range(2, 2 + expected)})
                with mock.patch.object(gm.os, "cpu_count", return_value=cpus), self.flight() as flight:
                    code, out, err = self.run_main(self.args())
                self.assertEqual(code, 1, err)
                self.assertNoGiveUp()
                self.assertEqual(max_overlap(self.events()), expected)
                self.assertEqual(flight["peak"], expected)

    def test_rows_and_printed_lines_equal_jobs_1_in_sorted_mutant_order(self):
        # m0002 (the first mutant, killed) ends only after m0009 (a survivor) has ended: with N > 1 the
        # completion order is not sorted, and rows in that order would put another result in m0002's place.
        self.plan(m0002=[["await_end", "m0009", CAP]])
        allow = os.path.join(self.tmp, "allow.json")
        with open(allow, "w") as fh:
            json.dump([{"id": RUN_OF["m0011"], "reason": "fixture survivor"}], fh)
        runs = {}
        for jobs in ("1", "3"):
            out = os.path.join(self.tmp, f"out{jobs}", "new.json")
            os.mkdir(os.path.dirname(out))
            code, printed, err = self.run_main(self.args("--jobs", jobs, "--allow", allow, out=out))
            with open(out, "rb") as fh:
                runs[jobs] = (code, printed.replace(out, "NEW.json"), err, fh.read(), self.events())
            os.rename(self.log, self.log + "." + jobs)
        self.assertEqual(runs["3"][:4], runs["1"][:4])
        self.assertEqual([r["id"] for r in self.rows(os.path.join(self.tmp, "out3", "new.json"))], list(RUN_OF.values()))
        ends = [e["name"] for e in runs["3"][4] if e["ev"] == "end"]
        self.assertLess(ends.index("m0009"), ends.index("m0002"))  # the run that ended first is not the first row
        rows = {r["id"]: r for r in json.loads(runs["3"][3])}
        self.assertEqual((rows[RUN_OF["m0009"]]["result"], rows[RUN_OF["m0009"]]["allowed"]), ("survived", None))
        self.assertEqual(rows[RUN_OF["m0011"]]["allowed"], "fixture survivor")
        self.assertEqual(runs["1"][0], 1)
        self.assertEqual(runs["3"][1].splitlines()[-1],
                         "guard_mutants: 10 mutants, 8 killed, 2 survived, 0 error, 1 allowed; wrote NEW.json")


class Threads(Base):
    def test_no_thread_and_each_test_is_a_child_of_the_one_main_thread(self):
        spawned = []
        real = gm.subprocess.Popen

        def popen(*a, **kw):
            spawned.append({"threads": threading.active_count(), "cwd": kw.get("cwd"),
                            "preexec_fn": kw.get("preexec_fn"), "session": kw.get("start_new_session")})
            proc = real(*a, **kw)
            spawned[-1]["pid"] = proc.pid
            return proc
        self.plan(**{f"m{i:04d}": [["barrier", 3, CAP]] for i in range(2, 5)})
        with mock.patch.object(gm.subprocess, "Popen", popen):
            code, out, err = self.run_main(self.args("--jobs", "3"))
        self.assertEqual(code, 1, err)
        self.assertNoGiveUp()
        self.assertEqual(max_overlap(self.events()), 3)
        self.assertEqual(len(spawned), 11)
        for s in spawned:
            self.assertEqual(s["threads"], 1)
            self.assertIsNone(s["cwd"])  # the child enters its copy by fchdir of the held fd, never by path
            self.assertTrue(callable(s["preexec_fn"]))
            self.assertTrue(s["session"])
        started = self.started()
        self.assertEqual({e["tool"] for e in started.values()}, {os.getpid()})
        self.assertEqual(sorted(e["group"] for e in started.values()), sorted(s["pid"] for s in spawned))
        self.assertTrue(all(e["held"] for e in started.values()))


class Refusal(Base):
    def test_refusal_in_a_run_kills_and_reaps_the_runs_in_flight_and_keeps_the_scratch(self):
        # m0002 leaves a directory in its mNNNN (a refusal when its run is recorded); m0003 and m0004 hang.
        self.plan(m0002=[["barrier", 3, CAP], ["mkdir", "stray"]],
                  m0003=[["barrier", 3, CAP], ["hang"]], m0004=[["barrier", 3, CAP], ["hang"]])
        code, out, err = self.run_main(self.args("--jobs", "3"))
        self.assertEqual(code, 2, out + err)
        self.assertTrue(err.startswith("guard_mutants: refused: "), err)
        self.assertIn("stray is a directory this run did not make", err)
        self.assertNotIn("Traceback", err)
        self.assertEqual(out, "")
        self.assertFalse(os.path.exists(self.out))
        started = self.started()
        self.assertEqual(set(started), {"m0001", "m0002", "m0003", "m0004"})  # no new run after the refusal
        self.assertNoGiveUp()
        for name in ("m0003", "m0004"):
            self.assertReaped(started[name]["group"])
            self.assertGone(started[name]["pid"])
        self.assertEqual([e["name"] for e in self.events() if e["ev"] == "end"], ["m0001", "m0002"])
        scratch = os.listdir(self.tooltmp)
        self.assertEqual(len(scratch), 1)
        kept = os.listdir(os.path.join(self.tooltmp, scratch[0]))
        self.assertTrue({"m0002", "m0003", "m0004"} <= set(kept), kept)
        self.assertTrue(os.path.isfile(os.path.join(self.tooltmp, scratch[0], "m0003", "lane", "pkg", "mod.py")))

    def test_unexpected_error_while_waiting_kills_and_reaps_the_runs_in_flight(self):
        self.plan(m0002=[["barrier", 2, CAP], ["hang"]], m0003=[["barrier", 2, CAP], ["hang"]])
        real = gm._wait_exit

        def wait_exit(pid, timeout):
            if sum(1 for n in self.started() if n != "m0001") >= 2:
                raise KeyboardInterrupt
            return real(pid, timeout)
        with mock.patch.object(gm, "_wait_exit", wait_exit), self.assertRaises(KeyboardInterrupt):
            self.run_main(self.args("--jobs", "2"))
        started = self.started()
        self.assertEqual(set(started), {"m0001", "m0002", "m0003"})
        for name in ("m0002", "m0003"):
            self.assertReaped(started[name]["group"])
            self.assertGone(started[name]["pid"])
        scratch = os.listdir(self.tooltmp)
        self.assertEqual(len(scratch), 1)
        self.assertTrue({"m0002", "m0003"} <= set(os.listdir(os.path.join(self.tooltmp, scratch[0]))))


class Timeout(Base):
    def test_timeout_counts_from_each_runs_own_start_and_kills_only_its_group(self):
        # m0003 hangs and times out; m0004 (in flight then) must see it die; m0005 starts after m0003's
        # timeout has passed, so a clock shared by the runs would time it out at once.
        self.plan(m0002=[["sleep", 2]], m0003=[["hang"]],
                  m0004=[["await_dead", "m0003", 30], ["sleep", 1], ["mark", "alive"]])
        code, out, err = self.run_main(self.args("--jobs", "2", "--timeout", "4"))
        self.assertEqual(code, 1, err)
        rows = {r["id"]: r for r in self.rows()}
        self.assertEqual((rows[RUN_OF["m0003"]]["result"], rows[RUN_OF["m0003"]]["detail"]),
                         ("error", "timeout after 4s"))
        self.assertEqual(rows[RUN_OF["m0005"]]["result"], "killed")
        self.assertEqual(rows[RUN_OF["m0002"]]["result"], "killed")
        # m0004 saw m0003's group die and was alive 1 s later (that kill did not reach it); m0005 started after:
        # more than m0003's 4 s after m0003 started.
        seen = [e for e in self.events() if e["ev"] == "saw-dead" and e["name"] == "m0004" and e["of"] == "m0003"]
        self.assertEqual(len(seen), 1)
        self.assertEqual([e["what"] for e in self.events() if e["ev"] == "mark" and e["name"] == "m0004"], ["alive"])
        self.assertGreater(self.started()["m0005"]["t"], seen[0]["t"])
        self.assertNoGiveUp()
        self.assertEqual(os.listdir(self.tooltmp), [])

    def test_a_test_that_exits_after_its_deadline_during_a_copy_build_is_a_timeout(self):
        # Reviewer probe test_deadline_during_build (T330 ruling 5, K1): m0002 sleeps past its 0.3 s timeout
        # and exits while m0003's copy is built; the build ends only after that exit, so the next poll sees an
        # exited test. Its exit came after its deadline: the row is the timeout, never m0002's exit code.
        self.plan(m0002=[["sleep", 0.6]])
        spawned = []
        real_popen, real_walk = gm.subprocess.Popen, gm.Session._walk

        def popen(*a, **kw):
            spawned.append(real_popen(*a, **kw))
            return spawned[-1]

        def walk(session, *a, **kw):
            if session.runs == 3 and a[2] == "" and a[3] is not None:  # m0003's copy, before it is built
                self.assertTrue(gm._wait_exit(spawned[1].pid, CAP))  # m0002's test has exited
            return real_walk(session, *a, **kw)
        with mock.patch.object(gm.subprocess, "Popen", popen), mock.patch.object(gm.Session, "_walk", walk):
            code, out, err = self.run_main(self.args("--jobs", "2", "--timeout", ".3"))
        self.assertIn(code, (0, 1), err)
        row = self.rows()[0]
        self.assertEqual(row["id"], RUN_OF["m0002"])
        self.assertEqual((row["result"], row["detail"]), ("error", "timeout after 0.3s"))
        self.assertEqual([e["rc"] for e in self.events() if e["ev"] == "end" and e["name"] == "m0002"], [1])


class Units(Base):
    def session(self, cmd):
        root_fd = gm.open_root(self.lane)
        self.addCleanup(os.close, root_fd)
        targets = gm.read_targets(root_fd, self.lane, ["pkg/mod.py"])
        stack = contextlib.ExitStack()
        stack.enter_context(mock.patch.object(tempfile, "tempdir", self.tooltmp))
        session = stack.enter_context(gm.Session(self.lane, root_fd, targets, cmd, 30))
        self.addCleanup(stack.close)
        return session, gm.mutants_for("pkg/mod.py", targets["pkg/mod.py"].data)

    def test_a_mutant_that_does_not_compile_is_an_error_row_and_never_runs(self):
        log = os.path.join(self.tmp, "echo.log")
        session, mutants = self.session(f"echo run >> {log}")
        bad = gm.Mutant(id="pkg/mod.py:1:0:raise-remove", rel="pkg/mod.py", line=1, operator="raise-remove",
                        change="broken", source=b"def f(:\n")
        session.baseline()
        found = session.results([bad, mutants[0], mutants[1]], 2)
        self.assertEqual(found[0][0], "error")
        self.assertIn("does not compile", found[0][1])
        self.assertEqual(found[1:], [("survived", "exit 0")] * 2)
        with open(log) as fh:
            self.assertEqual(len(fh.readlines()), 3)

    def test_only_a_compile_failure_is_an_error_row(self):
        session, mutants = self.session("true")
        session.baseline()
        with mock.patch.object(gm, "compile", side_effect=RuntimeError("unexpected"), create=True), \
                self.assertRaises(RuntimeError):
            session.results(mutants[:2], 2)

    def test_the_wait_for_any_run_sleeps_between_polls(self):
        proc = subprocess.Popen(["/bin/sh", "-c", "sleep 0.3"], start_new_session=True)
        self.addCleanup(proc.wait)
        naps = []
        real_sleep = time.sleep
        with mock.patch.object(gm.time, "sleep", lambda s: (naps.append(s), real_sleep(s))):
            self.assertEqual(gm._wait_any([proc.pid], 30), [proc.pid])
        self.assertTrue(naps)
        self.assertLessEqual(max(naps), 0.05)

    def test_execute_still_runs_its_test_to_the_end(self):
        """_execute (what the other suites call) drives the same steps as a run: one child, waited and reaped."""
        lane_fd = os.open(self.lane, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, lane_fd)
        self.assertEqual(gm._execute("test -f pkg/mod.py && exit 3", self.lane, self.tooltmp, 30, lane_fd),
                         ("killed", "exit 3"))

    def test_the_wait_for_any_run_gives_up_at_its_timeout(self):
        proc = subprocess.Popen(["/bin/sh", "-c", "sleep 30"], start_new_session=True)
        self.addCleanup(proc.wait)
        self.addCleanup(proc.kill)
        self.assertEqual(gm._wait_any([proc.pid], 0.2), [])
        self.assertIsNone(proc.poll())

    def test_docstring_describes_jobs_and_inert_flags(self):
        doc = gm.__doc__
        self.assertIn("[--jobs N]", doc)
        self.assertIn("min(4, os.cpu_count())", doc)
        entry = doc[doc.index("  flag-drop"):doc.index("  regex-zero")]
        self.assertIn("inert", entry)
        self.assertIn("O_RDONLY", entry)

    def test_docstring_names_jobs_and_says_an_inert_flag_makes_no_mutant(self):
        self.assertIn("--jobs", gm.__doc__)
        self.assertIn("an inert flag makes no mutant", " ".join(gm.__doc__.split()))


_REAL_FCNTL = fcntl.fcntl


def real_getpath(fd: int) -> str:
    """The fd's real path, or "" for an fd that has none (a pipe); never patched."""
    try:
        return os.fsdecode(_REAL_FCNTL(fd, fcntl.F_GETPATH, bytes(1024)).split(b"\0", 1)[0])
    except OSError:
        return ""


class KillSet(Base):
    """The per-run refusals of test_guard_mutants.py (Bound, Contract), on the --jobs 2 path (T330 ruling 3)."""

    def assertRefused(self, code, err, *words):
        self.assertEqual(code, 2, err)
        self.assertEqual(len(err.strip().splitlines()), 1, err)
        self.assertNotIn("Traceback", err)
        self.assertTrue(err.startswith("guard_mutants: refused: "), err)
        for w in words:
            self.assertIn(w, err)

    def assertNoChildLeft(self):
        for e in self.started().values():
            self.assertReaped(e["group"])
            self.assertGone(e["pid"])

    def kept(self) -> list[str]:
        """The one scratch directory's entries: it was kept."""
        scratch = os.listdir(self.tooltmp)
        self.assertEqual(len(scratch), 1, scratch)
        return os.listdir(os.path.join(self.tooltmp, scratch[0]))

    def at_run(self, name, shell):
        """The hook's test command, then shell in copy name only; the hook's exit code is kept."""
        return f'{self.cmd()}; rc=$?; case "$(pwd -P)" in */{name}/lane) {shell};; esac; exit $rc'

    def edit_in_place(self, rel, old, new):
        """A shell command that rewrites rel in the lane in place: same inode, size and mtime."""
        assert len(old) == len(new)
        target = os.path.join(self.lane, rel)
        helper = os.path.join(self.tmp, "edit.py")
        with open(helper, "w") as fh:
            fh.write(textwrap.dedent(f"""\
                import os
                st = os.stat({target!r})
                with open({target!r}, "rb") as fh:
                    data = fh.read()
                assert {old!r} in data
                with open({target!r}, "r+b") as fh:
                    fh.write(data.replace({old!r}, {new!r}))
                os.utime({target!r}, ns=(st.st_atime_ns, st.st_mtime_ns))
                """))
        return target, f"{sys.executable} -B -I {helper}"

    def assertEditedWithIdentityKept(self, target, before, marker):
        with open(target, "rb") as fh:
            self.assertIn(marker, fh.read())
        self.assertEqual(gm._identity(os.stat(target)), before)

    def arm_first_mutant(self, attack):
        """Patch Session._steps so attack(that run's lane copy path) is armed around the first mutant run.

        With N > 1 a mutant run never goes through Session._run: the attack wraps that run's steps."""
        real_steps = gm.Session._steps
        box = {}

        def steps(session, m, timeout):
            if m is None or "copy" in box:
                return (yield from real_steps(session, m, timeout))
            box["copy"] = os.path.join(session.scratch, f"m{session.runs + 1:04d}", "lane")
            with attack(box["copy"]) as fault:
                box["fault"] = fault
                return (yield from real_steps(session, m, timeout))
        return mock.patch.object(gm.Session, "_steps", steps), box

    def rebound_copy(self, when):
        log = os.path.join(self.tmp, "where.log")
        where = (f"if test -f pkg/mod.py; then echo held >> {log}; else echo empty >> {log}; fi; {self.cmd()}")
        self.plan(m0003=[["barrier", 2, CAP], ["hang"]])  # in flight when m0002 is refused, if it starts
        patch, box = self.arm_first_mutant(lambda copy: fk.rename_and_rebind(
            fk.GETPATH, 1, copy, when=when, match=lambda fd, *a: real_getpath(fd) == copy))
        with patch:
            code, out, err = self.run_main(["--file", "pkg/mod.py", "--test", where, "--out", self.out,
                                            "--jobs", "2"])
        self.assertEqual(box["fault"].fired, 1)
        self.assertEqual(os.path.basename(os.path.dirname(box["copy"])), "m0002")
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(os.listdir(box["copy"]), [])  # the replacement is kept
        self.assertTrue(os.path.isfile(os.path.join(box["fault"].parked, "pkg", "mod.py")))  # so is the copy
        self.assertNoGiveUp()
        self.assertNoChildLeft()
        with open(log) as fh:
            return code, err, box["copy"], fh.read().split()

    def test_copy_rebound_after_the_check_runs_the_test_in_the_held_copy_and_refuses(self):
        code, err, copy, where = self.rebound_copy("after")
        self.assertRefused(code, err, copy, "after the test run", "kept")
        self.assertEqual(where, ["held", "held", "held"])  # the baseline, m0002 and m0003: never the empty path
        names = sorted(self.started())  # m0002's hook names its copy from its cwd: the parked, held copy
        self.assertEqual(names[1:], ["m0001", "m0003"], names)  # no new run after the refusal
        self.assertTrue(names[0].startswith(fk.PARK_PREFIX), names)

    def test_copy_rebound_before_the_test_runs_is_refused_and_the_test_never_runs(self):
        code, err, copy, where = self.rebound_copy("before")
        self.assertRefused(code, err, copy, "before the test run", "kept")
        self.assertEqual(where, ["held"])  # the baseline only
        self.assertEqual(set(self.started()), {"m0001"})  # m0002's test never ran, and no new run started

    def test_lane_changed_by_the_test_is_refused(self):
        # m0002 appends to a lane file once m0003 has started; m0004's copy is the first to see it.
        note = os.path.join(self.lane, "data", "note.txt")
        os.mkdir(os.path.dirname(note))
        with open(note, "w") as fh:
            fh.write("note\n")
        self.plan(m0002=[["barrier", 2, CAP]], m0003=[["barrier", 2, CAP], ["hang"]])
        cmd = self.at_run("m0002", f"printf x >> {note}")
        code, out, err = self.run_main(["--file", "pkg/mod.py", "--test", cmd, "--out", self.out, "--jobs", "2"])
        self.assertRefused(code, err, "changed", "data/note.txt")
        self.assertEqual(out, "")
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(set(self.started()), {"m0001", "m0002", "m0003"})  # refused at m0004's copy
        self.assertNoGiveUp()
        self.assertNoChildLeft()
        self.assertIn("m0003", self.kept())  # the run in flight was stopped and its copy kept

    def test_test_file_rewritten_with_its_identity_kept_after_the_baseline_is_refused(self):
        # m0002 rewrites a lane test file in place once m0003 has started: same inode, size and mtime.
        with open(os.path.join(self.lane, "pkg", "test_mod.py"), "w") as fh:
            fh.write("import mod\n")
        target, edit = self.edit_in_place("pkg/test_mod.py", b"import mod", b"assert 0  ")
        before = gm._identity(os.stat(target))
        self.plan(m0002=[["barrier", 2, CAP]], m0003=[["barrier", 2, CAP], ["hang"]])
        cmd = self.at_run("m0002", edit)
        code, out, err = self.run_main(["--file", "pkg/mod.py", "--test", cmd, "--out", self.out, "--jobs", "2"])
        self.assertEditedWithIdentityKept(target, before, b"assert 0")
        self.assertRefused(code, err, "changed", "pkg/test_mod.py")
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(set(self.started()), {"m0001", "m0002", "m0003"})  # refused at m0004's copy
        self.assertNoGiveUp()
        self.assertNoChildLeft()
        self.assertIn("m0003", self.kept())

    def test_product_file_rewritten_with_its_identity_kept_after_the_last_copy_is_refused(self):
        # m0011 (the last mutant) changes the product after the last copy: only the final scan can see it.
        target, edit = self.edit_in_place("pkg/mod.py", b"n == 5", b"n == 6")
        before = gm._identity(os.stat(target))
        cmd = self.at_run("m0011", edit)
        code, out, err = self.run_main(["--file", "pkg/mod.py", "--test", cmd, "--out", self.out, "--jobs", "2"])
        self.assertEditedWithIdentityKept(target, before, b"n == 6")
        self.assertRefused(code, err, "changed", "pkg/mod.py")
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(set(self.started()), {"m0001", *RUN_OF})
        self.assertNoChildLeft()

    def test_a_file_made_after_the_test_exited_during_a_copy_build_is_refused(self):
        # Reviewer probe test_foreign_file_after_exit (T330 ruling 5, K2): once m0002's test has exited, a
        # file appears in its copy while m0003's copy is built. It was born after the run ended: not the test's.
        spawned, made = [], []
        real_popen, real_walk = gm.subprocess.Popen, gm.Session._walk

        def popen(*a, **kw):
            spawned.append(real_popen(*a, **kw))
            return spawned[-1]

        def walk(session, *a, **kw):
            if session.runs == 3 and not made:  # m0003's copy, before it is built
                self.assertTrue(gm._wait_exit(spawned[1].pid, CAP))  # m0002's test has exited
                made.append(os.path.join(session.scratch, "m0002", "lane", "foreign"))
                with open(made[0], "w") as fh:
                    fh.write("not made by the test")
            return real_walk(session, *a, **kw)
        with mock.patch.object(gm.subprocess, "Popen", popen), mock.patch.object(gm.Session, "_walk", walk):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertRefused(code, err, made[0], "kept")
        self.assertEqual(out, "")
        self.assertFalse(os.path.exists(self.out))
        self.assertTrue(os.path.isfile(made[0]))
        self.assertNoChildLeft()

    def test_a_file_born_before_its_run_started_is_refused(self):
        # A file appears in m0002's copy after the copy is built and before its test starts (T330 ruling 6, M22).
        planted = []
        real_walk = gm.Session._walk

        def walk(session, *a, **kw):
            done = real_walk(session, *a, **kw)
            if session.runs == 2 and a[2] == "" and a[3] is not None:  # m0002's whole copy is built
                planted.append(os.path.join(a[4], "planted"))
                with open(planted[0], "w") as fh:
                    fh.write("not made by the test")
            return done
        with mock.patch.object(gm.Session, "_walk", walk):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        kept = os.path.join(os.path.dirname(os.path.dirname(planted[0])), "lane", "planted")
        self.assertRefused(code, err, kept, "made before the test run", "kept")
        self.assertEqual(out, "")
        self.assertFalse(os.path.exists(self.out))
        self.assertTrue(os.path.isfile(kept))
        self.assertIn("m0002", self.started())  # m0002's test ran: the refusal is its after-run record
        self.assertNoChildLeft()

    def test_each_finished_runs_copy_is_removed_while_the_next_runs_go_on(self):
        # When each mutant copy is built, the scratch holds that copy and those of the runs still in flight:
        # never more than N (T330 ruling 6, M20). A check after main() returns would miss it: the end of the
        # session removes the whole scratch.
        held = []
        real_walk = gm.Session._walk

        def walk(session, *a, **kw):
            if a[2] == "" and a[3] is not None:  # a copy, before it is built
                held.append(sorted(os.listdir(session.scratch)))
            return real_walk(session, *a, **kw)
        with mock.patch.object(gm.Session, "_walk", walk):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertEqual(code, 1, err)
        self.assertEqual([names[-1] for names in held], ["m0001", *RUN_OF])  # the baseline, then each mutant
        self.assertEqual(max(len(names) for names in held), 2, held)
        self.assertEqual(os.listdir(self.tooltmp), [])

    def test_a_copy_directory_rebound_at_an_unlink_keeps_the_file_now_at_its_path(self):
        # T330 ruling 13 (rd-unlink-path, F4): as m0002's pkg/mod.py is removed, its directory is parked and a new
        # one holding another mod.py is put at its path. The unlink through the held fd removes the held entry:
        # the other file is kept, and the removal refuses.
        real = os.unlink
        box = {}

        def unlink(path, *, dir_fd=None):
            target = os.path.join(real_getpath(dir_fd), path) if dir_fd is not None else path
            if not box and target.startswith(self.tooltmp + os.sep) and target.endswith("/m0002/lane/pkg/mod.py"):
                pkg = os.path.dirname(target)
                box["parked"] = os.path.join(os.path.dirname(pkg), "parked")
                os.mkdir(box["parked"])
                os.rename(pkg, os.path.join(box["parked"], "pkg"))
                os.mkdir(pkg)
                box["other"] = target
                with open(target, "w") as fh:
                    fh.write("not the copy's")
            return real(path, dir_fd=dir_fd)
        with mock.patch.object(gm.os, "unlink", unlink):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertRefused(code, err, "kept")
        self.assertTrue(os.path.isfile(box["other"]))
        with open(box["other"]) as fh:
            self.assertEqual(fh.read(), "not the copy's")
        self.assertFalse(os.path.exists(os.path.join(box["parked"], "pkg", "mod.py")))  # the held entry went
        self.assertFalse(os.path.exists(self.out))
        self.assertNoChildLeft()

    def test_a_copy_directory_replaced_once_it_is_empty_is_kept(self):
        # T330 ruling 13 (rd-now-ident): once m0002's pkg is emptied, it is removed and a new empty directory is
        # made at its name. F_GETPATH of the held fd still gives the removed directory's last path (macOS), so
        # only the identity check of the name sees the swap: the new directory is kept and the removal refuses.
        real = os.stat
        box = {}

        def stat(path, *a, dir_fd=None, **kw):
            where = real_getpath(dir_fd) if dir_fd is not None else ""
            if not box and path == "pkg" and where.startswith(self.tooltmp + os.sep) and where.endswith("/m0002/lane"):
                held = os.path.join(where, "pkg")
                if os.listdir(held) == []:
                    os.rmdir(held)
                    os.mkdir(held)
                    box["new"] = held
            return real(path, *a, dir_fd=dir_fd, **kw)
        with mock.patch.object(gm.os, "stat", stat):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertRefused(code, err, box["new"], "kept")
        self.assertTrue(os.path.isdir(box["new"]))
        self.assertFalse(os.path.exists(self.out))
        self.assertNoChildLeft()

    def test_a_copy_directory_swapped_before_its_record_is_refused_and_all_kept(self):
        # T330 ruling 13 (rec-sub-ident): as m0002's run is recorded, its pkg is parked and a new empty directory
        # is put at its name between the stat and the open. The record refuses at once: nothing is removed.
        patch, box = self.arm_first_mutant(lambda copy: fk.rename_and_rebind(
            "open", 1, os.path.join(copy, "pkg"), when="before",
            match=lambda name, *a, dir_fd=None, **kw: name == "pkg" and dir_fd is not None
            and real_getpath(dir_fd) == copy))
        with patch:
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertEqual(box["fault"].fired, 1)
        self.assertRefused(code, err, os.path.join(box["copy"], "pkg"), "changed after the test run", "kept")
        self.assertTrue(os.path.isfile(os.path.join(box["fault"].parked, "mod.py")))
        self.assertEqual(sorted(os.listdir(os.path.dirname(box["copy"]))), ["lane", "tmp"])
        self.assertFalse(os.path.exists(self.out))
        self.assertNoChildLeft()

    def test_a_baseline_copy_rebound_before_its_removal_is_refused_by_that_removal(self):
        # T330 ruling 15 (rm-keep): the baseline's copy m0001 is parked and a new empty directory put at its name
        # just before its removal opens it. That removal refuses and marks everything kept, so the session's end
        # removes nothing: the refusal reported is the removal's own, whatever order the scratch is listed in.
        real_baseline = gm.Session.baseline
        box = {}

        def baseline(session):
            box["copy"] = os.path.join(session.scratch, "m0001")
            with fk.rename_and_rebind("open", 2, box["copy"], match=lambda p, *a, **k: p == "m0001"
                                      and k.get("dir_fd") is not None) as fault:  # call 1 makes it, 2 removes it
                box["fault"] = fault
                return real_baseline(session)
        with mock.patch.object(gm.Session, "baseline", baseline):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertRefused(code, err, box["copy"], "is not a directory this run made", "kept")
        self.assertEqual(os.listdir(box["copy"]), [])
        self.assertEqual(sorted(os.listdir(box["fault"].parked)), ["lane", "tmp"])
        self.assertEqual(set(self.started()), {"m0001"})
        self.assertFalse(os.path.exists(self.out))
        self.assertNoChildLeft()

    def test_a_test_that_exits_before_its_run_is_in_flight_ends_its_window_at_that_exit(self):
        # T330 ruling 14 (stamp-spawn): m0002's test has exited before its run is in flight, so the handler had no
        # run to stamp; then m0003's copy is built and a file appears in m0002's copy. m0002's window ends at its
        # own exit (stamped as its run entered flights): that file is not the test's, and it is refused and kept.
        spawned, made = [], []
        real_popen, real_walk = gm.subprocess.Popen, gm.Session._walk

        def popen(*a, **kw):
            spawned.append(real_popen(*a, **kw))
            if len(spawned) == 2:  # m0002: its test has exited (left unreaped) before the spawn returns
                self.assertTrue(gm._wait_exit(spawned[-1].pid, CAP))
            return spawned[-1]

        def walk(session, *a, **kw):
            if session.runs == 3 and a[2] == "" and a[3] is not None:  # m0003's copy, before it is built
                made.append(os.path.join(session.scratch, "m0002", "lane", "foreign"))
                with open(made[0], "w") as fh:
                    fh.write("not made by the test")
            return real_walk(session, *a, **kw)
        with mock.patch.object(gm.subprocess, "Popen", popen), mock.patch.object(gm.Session, "_walk", walk):
            code, out, err = self.run_main(self.args("--jobs", "2"))
        self.assertRefused(code, err, made[0], "kept")
        self.assertTrue(os.path.isfile(made[0]))
        self.assertFalse(os.path.exists(self.out))
        self.assertNoChildLeft()

    def test_runs_are_judged_by_their_own_exits_while_sigchld_is_blocked(self):
        # T330 ruling 14 (stamp-wait): a caller can start the tool with SIGCHLD blocked (the mask is inherited),
        # and then the handler never runs: each exit is stamped by the wait that sees it. Without that stamp no
        # run would land before its deadline, and every row would be a timeout.
        old = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGCHLD})
        self.addCleanup(signal.pthread_sigmask, signal.SIG_SETMASK, old)
        code, out, err = self.run_main(self.args("--jobs", "2", "--timeout", "5"))
        signal.pthread_sigmask(signal.SIG_SETMASK, old)
        self.assertEqual(code, 1, err)
        self.assertEqual(out.splitlines()[-1],
                         f"guard_mutants: 10 mutants, 8 killed, 2 survived, 0 error, 0 allowed; wrote {self.out}")
        self.assertNoChildLeft()


class Deadline(Base):
    def test_a_test_still_running_at_its_deadline_is_killed_there(self):
        # T330 ruling 10 (M08): m0002 sleeps past its 1 s timeout and then logs a mark. It is killed at its
        # deadline: its row is the timeout, and neither the mark nor its end is ever logged.
        self.plan(m0002=[["sleep", 3], ["mark", "late"]])
        code, out, err = self.run_main(self.args("--jobs", "2", "--timeout", "1"))
        self.assertEqual(code, 1, err)
        row = self.rows()[0]
        self.assertEqual((row["id"], row["result"], row["detail"]), (RUN_OF["m0002"], "error", "timeout after 1s"))
        self.assertEqual([e["ev"] for e in self.events() if e["name"] == "m0002"], ["start"])
        self.assertGone(self.started()["m0002"]["pid"])


class Restore(Base):
    def test_the_previous_sigchld_handler_is_back_after_a_return_a_refusal_and_an_error(self):
        # T330 ruling 11 (M30): a handler installed before main() is the one installed after it, however it ends.
        original = signal.getsignal(signal.SIGCHLD)
        self.addCleanup(signal.signal, signal.SIGCHLD, original)

        def sentinel(signum, frame):
            pass

        def ends_by_return():
            self.assertEqual(self.run_main(self.args("--jobs", "2"))[0], 1)

        def ends_by_refusal():
            self.plan(m0002=[["mkdir", "stray"]])
            self.assertEqual(self.run_main(self.args("--jobs", "2"))[0], 2)

        def ends_by_error():
            with mock.patch.object(gm, "_wait_any", side_effect=RuntimeError("test: unexpected")), \
                    self.assertRaises(RuntimeError):
                self.run_main(self.args("--jobs", "2"))
        for ends in (ends_by_return, ends_by_refusal, ends_by_error):
            with self.subTest(ends=ends.__name__):
                self.setUp()
                signal.signal(signal.SIGCHLD, sentinel)
                ends()
                self.assertIs(signal.getsignal(signal.SIGCHLD), sentinel)


class HandlerError(Base):
    """An error the SIGCHLD handler meets, at --jobs 2 (T330 ruling 9): no test is left alive or unreaped, no new
    run starts, the scratch is kept, no NEW.json is written, and the error propagates."""

    def handler_error(self, error=None):
        """Patch gm._wait_exit to raise error (EMFILE) once, called inside the SIGCHLD handler after box["armed"].

        box["fire"]() arms it and sends SIGCHLD to this process: Python runs the handler at the next bytecode,
        within fire() itself; box["in_fire"] counts the errors met by then."""
        error = error or OSError(errno.EMFILE, "test: the handler's exit check failed")
        box = {"armed": False, "fired": 0, "error": error}
        real = gm._wait_exit

        def in_handler(frame):
            code = getattr(signal.getsignal(signal.SIGCHLD), "__code__", None)
            while frame is not None and frame.f_code is not code:
                frame = frame.f_back
            return frame is not None

        def wait_exit(pid, timeout):
            if box["armed"] and not box["fired"] and in_handler(sys._getframe(1)):
                box["fired"] += 1
                raise box["error"]
            return real(pid, timeout)

        def fire():
            box["armed"] = True
            try:
                os.kill(os.getpid(), signal.SIGCHLD)
            finally:
                box["in_fire"] = box["fired"]
        box["fire"] = fire
        return mock.patch.object(gm, "_wait_exit", wait_exit), box

    def spawns(self, after=None):
        """Patch gm.subprocess.Popen to keep each child; after(n) runs once the nth spawn has returned."""
        spawned = []
        real = gm.subprocess.Popen

        def popen(*a, **kw):
            spawned.append(real(*a, **kw))
            if after is not None:
                after(len(spawned))
            return spawned[-1]

        def stop():
            for proc in spawned:
                if proc.poll() is None:
                    gm._kill_group(proc.pid)
                    proc.wait()
        self.addCleanup(stop)
        return mock.patch.object(gm.subprocess, "Popen", popen), spawned

    def note(self, **ev):
        ev.update(t=time.time())
        with open(self.log, "a") as fh:
            fh.write(json.dumps(ev) + "\n")

    def assertStopped(self, caught, box, spawned, runs):
        self.assertIs(caught.exception, box["error"])
        self.assertEqual(box["fired"], 1)
        self.assertEqual(len(spawned), runs)  # the baseline and runs - 1 mutant runs: no new run after the error
        self.assertEqual([proc.returncode is not None for proc in spawned], [True] * runs)  # each reaped by the tool
        for proc in spawned:
            self.assertGone(proc.pid)
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(len(os.listdir(self.tooltmp)), 1)  # the scratch is kept

    def test_an_error_in_the_handler_right_after_a_spawn_leaves_no_test_alive(self):
        # Reviewer probe handler_probe.py (T330 ruling 9a, K1), with a line-independent trigger: SIGCHLD is sent
        # right after m0003's spawn returns, before its run is in flights, and the handler meets an error there:
        # an OSError, or a BaseException such as KeyboardInterrupt.
        for error in (OSError(errno.EMFILE, "test: the handler's exit check failed"), KeyboardInterrupt()):
            with self.subTest(error=type(error).__name__):
                self.setUp()
                self.plan(m0002=[["hang"]], m0003=[["hang"]])
                wait_patch, box = self.handler_error(error)
                popen_patch, spawned = self.spawns(after=lambda n: box["fire"]() if n == 3 else None)
                with wait_patch, popen_patch, self.assertRaises(type(error)) as caught:
                    self.run_main(self.args("--jobs", "2"))
                self.assertStopped(caught, box, spawned, 3)
                self.assertEqual(box["in_fire"], 1)  # met inside the spawn, before m0003's run was in flights
                self.assertNotIn("end", [e["ev"] for e in self.events() if e["name"] == "m0002"])  # stopped at once

    def test_an_error_in_the_handler_while_a_timed_out_run_is_finished_leaves_no_test_alive(self):
        # T330 ruling 9, second member: m0002 is out of flights at its deadline and its test still runs when the
        # handler meets an error, before _finish kills it. It is killed and reaped, and no new run (m0004) starts.
        self.plan(m0002=[["hang"]], m0003=[["hang"]])
        wait_patch, box = self.handler_error()
        popen_patch, spawned = self.spawns()
        real, alive = gm._finish, gm._wait_exit

        def finish(steps, exited):
            if not exited and not box["armed"]:
                self.assertFalse(alive(spawned[1].pid, 0))  # m0002's test still runs: only _finish kills it
                box["fire"]()
            return real(steps, exited)
        with wait_patch, popen_patch, mock.patch.object(gm, "_finish", finish), \
                self.assertRaises(OSError) as caught:
            self.run_main(self.args("--jobs", "2", "--timeout", "1"))
        self.assertStopped(caught, box, spawned, 3)
        self.assertEqual(box["in_fire"], 1)

    def test_an_error_in_the_handler_while_the_last_runs_drain_stops_the_rest_at_the_next_wait(self):
        # m0010 ends once m0011 has started; the handler meets an error while m0010 is finished, with m0011 in
        # flight. The next wait raises it: m0011 is stopped there, never run to its end.
        self.plan(m0010=[["barrier", 10, CAP]], m0011=[["await_end", "never", CAP]])
        wait_patch, box = self.handler_error()
        popen_patch, spawned = self.spawns()
        real = gm._finish

        def finish(steps, exited):
            if exited and len(spawned) == 11 and not box["armed"]:
                box["fire"]()
            return real(steps, exited)
        with wait_patch, popen_patch, mock.patch.object(gm, "_finish", finish), \
                self.assertRaises(OSError) as caught:
            self.run_main(self.args("--jobs", "2"))
        self.assertStopped(caught, box, spawned, 11)
        self.assertEqual(box["in_fire"], 1)
        self.assertEqual([e["ev"] for e in self.events() if e["name"] == "m0011"], ["start"])

    def test_an_error_in_the_handler_during_the_last_wait_is_raised_once_it_is_restored(self):
        # m0011 runs alone at the end and ends only once the last wait has begun; the handler meets an error at
        # its exit. No wait follows: the error is raised once the handler is restored, and no NEW.json is written.
        # The test runs the installed handler itself once that wait has seen the exit (T330 ruling 21): m0011 is
        # then still in flights and unstamped, since before the wait returns only the handler stamps it, so the
        # error is met in the last wait whenever the kernel delivers m0011's SIGCHLD.
        self.plan(m0011=[["await_end", "go", CAP]])
        wait_patch, box = self.handler_error()
        popen_patch, spawned = self.spawns()
        real = gm._wait_any

        def wait_any(pids, timeout):
            if len(spawned) == 11 and len(pids) == 1 and not box["armed"]:
                box["armed"] = True
                self.note(ev="end", name="go")  # m0011 may end now
                exited = real(pids, timeout)
                signal.getsignal(signal.SIGCHLD)(signal.SIGCHLD, None)  # no error left if a delivered SIGCHLD met it
                return exited
            return real(pids, timeout)
        with wait_patch, popen_patch, mock.patch.object(gm, "_wait_any", wait_any), \
                self.assertRaises(OSError) as caught:
            self.run_main(self.args("--jobs", "2"))
        self.assertStopped(caught, box, spawned, 11)
        self.assertNoGiveUp()

    def test_of_two_errors_the_handler_meets_the_first_is_raised(self):
        # T330 ruling 22 (M31), trigger of the reviewer's two_errors.py: right after m0003's spawn returns, before
        # its run is in flights, the test runs the installed handler twice; each run meets an error at m0002's exit
        # check. The first error recorded propagates; every started test is stopped and reaped; no NEW.json.
        first = RuntimeError("test: the first handler error")
        second = OSError(errno.EMFILE, "test: the second handler error")
        self.plan(m0002=[["hang"]], m0003=[["hang"]])
        errors, met, armed = [first, second], [], []
        real = gm._wait_exit

        def in_handler(frame):
            code = getattr(signal.getsignal(signal.SIGCHLD), "__code__", None)
            while frame is not None and frame.f_code is not code:
                frame = frame.f_back
            return frame is not None

        def wait_exit(pid, timeout):
            if armed and errors and in_handler(sys._getframe(1)):
                met.append(errors.pop(0))
                raise met[-1]
            return real(pid, timeout)

        def after(n):
            if n == 3:
                armed.append(True)
                for _ in range(2):
                    signal.getsignal(signal.SIGCHLD)(signal.SIGCHLD, None)
                self.assertEqual(met, [first, second])  # both met before m0003's run is in flights
        popen_patch, spawned = self.spawns(after=after)
        with mock.patch.object(gm, "_wait_exit", wait_exit), popen_patch, \
                self.assertRaises(BaseException) as caught:
            self.run_main(self.args("--jobs", "2"))
        self.assertIs(caught.exception, first)
        self.assertIs(type(caught.exception), RuntimeError)
        self.assertEqual(str(caught.exception), "test: the first handler error")
        self.assertEqual(len(spawned), 3)  # the baseline, m0002 and m0003: no new run after the errors
        self.assertEqual([proc.returncode is not None for proc in spawned], [True] * 3)  # each reaped by the tool
        for proc in spawned:
            self.assertGone(proc.pid)
        self.assertFalse(os.path.exists(self.out))
        self.assertEqual(len(os.listdir(self.tooltmp)), 1)  # the scratch is kept


if __name__ == "__main__":
    unittest.main()
