"""Tests for guard_mutants --jobs N: up to N mutant test runs at once, with the output of --jobs 1.

Every lane is a fixture in a temp directory; no real lane, branch or PR is touched. The test command
runs HOOK in each lane copy: it logs the run's start and end (copy name, pids, time.time()), can wait
for other runs, and then judges the copy's pkg/mod.py. Overlap is proved from those logged times and
from barriers that only runs in flight together can pass, never from a wall-clock threshold.
"""
from __future__ import annotations

import contextlib
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


if __name__ == "__main__":
    unittest.main()
