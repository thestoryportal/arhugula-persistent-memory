"""Tests for guard_mutants._execute: the test's process group is killed before the test is reaped.

Each test runs a real /bin/sh child that enters a temp directory through a held fd. os.killpg
and os.waitpid are wrapped as witnesses that call the real functions; only the kill-error
tests replace the kill's outcome with an injected error.
"""
from __future__ import annotations

import errno
import os
import select
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from unittest import mock

import guard_mutants as gm

REAL_KILLPG = os.killpg
REAL_WAITPID = os.waitpid


def _exists(pid: int) -> bool:
    """pid still names a process: running, or exited and not yet reaped."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


def _reap_if_unreaped(pid: int) -> None:
    """Kill and reap a child this test made, only while it is unreaped (its group id is still its own)."""
    try:
        if REAL_WAITPID(pid, os.WNOHANG) != (0, 0):
            return  # it had exited; that call reaped it
    except ChildProcessError:
        return  # already reaped
    try:
        REAL_KILLPG(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    REAL_WAITPID(pid, 0)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="t316-")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.lane = os.path.join(self.tmp, "lane")
        self.tooltmp = os.path.join(self.tmp, "tmp")
        os.mkdir(self.lane)
        os.mkdir(self.tooltmp)
        self.lane_fd = os.open(self.lane, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, self.lane_fd)
        self.kills: list[tuple[int, int, bool]] = []  # (pgid, signal, pgid still a process at the kill)
        self.reaps: list[int] = []  # pids that os.waitpid returned (reaped) during the run

    def execute(self, cmd: str, timeout: float = 30, kill_error: OSError | None = None) -> tuple[str, str]:
        def killpg(pgid, sig):
            self.kills.append((pgid, sig, _exists(pgid)))
            self.addCleanup(_reap_if_unreaped, pgid)
            if kill_error is not None:
                raise kill_error
            return REAL_KILLPG(pgid, sig)

        def waitpid(pid, options):
            result = REAL_WAITPID(pid, options)
            if result[0] != 0:
                self.reaps.append(result[0])
            return result

        with mock.patch.object(gm.os, "killpg", killpg), mock.patch.object(gm.os, "waitpid", waitpid):
            return gm._execute(cmd, self.lane, self.tooltmp, timeout, self.lane_fd)

    def assertReaped(self, pid: int) -> None:
        with self.assertRaises(ChildProcessError):
            REAL_WAITPID(pid, os.WNOHANG)

    def spawn(self, cmd: str) -> subprocess.Popen:
        proc = subprocess.Popen(["/bin/sh", "-c", cmd], start_new_session=True,
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(proc.wait)  # after the reap below; it only settles the Popen's own state
        self.addCleanup(_reap_if_unreaped, proc.pid)
        return proc


class KillBeforeReap(Base):
    def test_grandchild_left_running_is_killed_at_end_of_run(self):
        result = self.execute("sleep 60 & echo $! > grandchild; exit 0")
        self.assertEqual(result, ("survived", "exit 0"))
        with open(os.path.join(self.lane, "grandchild")) as f:
            grandchild = int(f.read())
        pgid = self.kills[0][0]

        def kill_stray():
            with_group = _exists(grandchild) and os.getpgid(grandchild) == pgid
            if with_group:
                os.kill(grandchild, signal.SIGKILL)
        self.addCleanup(kill_stray)
        deadline = time.monotonic() + 10
        while _exists(grandchild) and time.monotonic() < deadline:
            time.sleep(0.02)  # SIGKILLed; its new parent (init or launchd) reaps it
        self.assertFalse(_exists(grandchild), "the test's background grandchild still runs after the call")

    def test_child_that_exits_at_once_gives_the_same_result_as_before(self):
        for cmd, expected in (("exit 0", ("survived", "exit 0")), ("exit 3", ("killed", "exit 3"))):
            with self.subTest(cmd=cmd):
                self.kills.clear()
                self.reaps.clear()
                self.assertEqual(self.execute(cmd), expected)
                pid = self.kills[0][0]
                self.assertEqual(self.reaps, [pid])
                self.assertReaped(pid)

    def test_kill_happens_while_the_child_is_not_yet_reaped(self):
        self.execute("exit 0")
        self.assertEqual(len(self.kills), 1)
        pid, sig, existed = self.kills[0]
        self.assertEqual(sig, signal.SIGKILL)
        self.assertTrue(existed, "the child was reaped before its group was killed")
        self.assertEqual(self.reaps, [pid])

    def test_timeout_kills_once_and_reaps_once(self):
        start = time.monotonic()
        result = self.execute("sleep 30", timeout=0.5)
        elapsed = time.monotonic() - start
        self.assertEqual(result, ("error", "timeout after 0.5s"))
        self.assertGreaterEqual(elapsed, 0.5)
        self.assertLess(elapsed, 10)
        self.assertEqual(len(self.kills), 1)
        pid, sig, existed = self.kills[0]
        self.assertEqual(sig, signal.SIGKILL)
        self.assertTrue(existed)
        self.assertEqual(self.reaps, [pid])
        self.assertReaped(pid)


class KillErrors(Base):
    def test_permission_error_at_the_kill_is_tolerated(self):
        result = self.execute("exit 4", kill_error=PermissionError(errno.EPERM, "Operation not permitted"))
        self.assertEqual(result, ("killed", "exit 4"))
        self.assertReaped(self.kills[0][0])

    def test_process_lookup_error_at_the_kill_is_tolerated(self):
        result = self.execute("exit 0", kill_error=ProcessLookupError(errno.ESRCH, "No such process"))
        self.assertEqual(result, ("survived", "exit 0"))
        self.assertReaped(self.kills[0][0])

    def test_other_oserror_at_the_kill_surfaces(self):
        for err in (OSError(errno.EINVAL, "Invalid argument"), OSError(errno.EIO, "Input/output error")):
            with self.subTest(errno=err.errno):
                self.kills.clear()
                with self.assertRaises(OSError) as caught:
                    self.execute("exit 0", kill_error=err)
                self.assertIs(caught.exception, err)
                self.assertEqual(len(self.kills), 1)


class WaitWithoutReaping(Base):
    def test_platform_wait_is_one_function_picked_once(self):
        expected = gm._wait_exit_waitid if hasattr(os, "waitid") else gm._wait_exit_kqueue
        self.assertIs(gm._wait_exit, expected)

    def test_wait_returns_for_an_exited_child_and_leaves_it_unreaped(self):
        proc = self.spawn("exit 5")
        time.sleep(0.3)  # the child has exited and is not reaped when the wait starts
        self.assertTrue(gm._wait_exit(proc.pid, 10))
        self.assertTrue(_exists(proc.pid))
        self.assertEqual(REAL_WAITPID(proc.pid, os.WNOHANG), (proc.pid, 5 << 8))

    def test_wait_returns_when_a_running_child_exits(self):
        proc = self.spawn("sleep 0.3; exit 0")
        self.assertTrue(gm._wait_exit(proc.pid, 10))
        self.assertEqual(REAL_WAITPID(proc.pid, os.WNOHANG), (proc.pid, 0))

    def test_wait_gives_up_after_the_timeout_on_a_running_child(self):
        proc = self.spawn("sleep 30")
        start = time.monotonic()
        self.assertFalse(gm._wait_exit(proc.pid, 0.3))
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.29)
        self.assertLess(elapsed, 5)
        self.assertEqual(REAL_WAITPID(proc.pid, os.WNOHANG), (0, 0))

    @unittest.skipUnless(hasattr(select, "kqueue"), "kqueue path: macOS and BSD")
    def test_kqueue_registration_error_other_than_esrch_surfaces(self):
        """Only ESRCH (the child already exited) counts as an exit; any other registration error is raised."""
        proc = self.spawn("exit 0")
        real_kqueue = select.kqueue

        class Kqueue:
            def __init__(self):
                self.kq = real_kqueue()

            def control(self, changes, nevents, timeout):
                change = changes[0]
                return [select.kevent(change.ident, change.filter, change.flags | select.KQ_EV_ERROR,
                                      change.fflags, errno.EINVAL)]

            def close(self):
                self.kq.close()

        with mock.patch.object(gm.select, "kqueue", Kqueue), self.assertRaises(OSError) as caught:
            gm._wait_exit_kqueue(proc.pid, 10)
        self.assertEqual(caught.exception.errno, errno.EINVAL)


if __name__ == "__main__":
    unittest.main()
