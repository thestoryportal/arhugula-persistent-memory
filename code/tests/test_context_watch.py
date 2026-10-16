"""context_watch.py runs as a real subprocess under a fake claude owner (a symlink named claude to /bin/sh).

Every process a test starts is in its own session; addCleanup SIGKILLs that whole process group, pass or fail.
"""
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "agents", "context_watch.py")
# Runs the watcher as its child and records the exit code. It is not named claude, so the watcher's owner is the
# fake claude above it, and it survives the owner's death to report the watcher's exit code.
RUNNER = (
    "import subprocess, sys\n"
    "out, err, rc = sys.argv[1:4]\n"
    "with open(out, 'w') as o, open(err, 'w') as e:\n"
    "    code = subprocess.run(sys.argv[4:], stdout=o, stderr=e).returncode\n"
    "open(rc + '.tmp', 'w').write(str(code))\n"
    "import os; os.rename(rc + '.tmp', rc)\n"
)
# Orphans itself: the parent exits, the child waits until launchd (pid 1) adopts it, then runs RUNNER inline.
ORPHAN = (
    "import os, sys, time\n"
    "if os.fork():\n"
    "    os._exit(0)\n"
    "while os.getppid() != 1:\n"
    "    time.sleep(0.01)\n"
    "sys.argv = sys.argv[1:]\n"
    "exec(sys.argv[0])\n"
)


def write_transcript(path, total):
    usage = {"input_tokens": total - 300, "cache_creation_input_tokens": 100,
             "cache_read_input_tokens": 100, "output_tokens": 100}
    with open(path, "w") as f:
        f.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
        f.write(json.dumps({"type": "assistant", "message": {"usage": usage}}) + "\n")


def live_members(pgid):
    ps = subprocess.run(["/bin/ps", "-A", "-o", "pid=,pgid=,stat="], capture_output=True, text=True, check=True)
    rows = [line.split() for line in ps.stdout.splitlines()]
    return [r for r in rows if r[1] == str(pgid) and not r[2].startswith("Z")]


class WatchTest(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.dir = td.name
        self.transcript = os.path.join(self.dir, "t.jsonl")
        write_transcript(self.transcript, 1000)
        self.out, self.err, self.rc = (os.path.join(self.dir, n) for n in ("out", "err", "rc"))

    def track(self, proc):
        """Kill the process group of proc (its own session) at test end, then reap proc."""
        def kill():
            # macOS killpg can give EPERM for a group whose only members are exiting or zombie, so success is
            # judged by ps: no live member of the group is left.
            for _ in range(20):
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
                proc.poll()
                members = live_members(proc.pid)
                if not members:
                    break
                time.sleep(0.25)
            else:
                raise AssertionError(f"process group {proc.pid} still has live members after cleanup: {members}")
            proc.wait(timeout=5)
        self.addCleanup(kill)
        return proc

    def watch_args(self, *extra):
        return [sys.executable, "-B", "-S", SCRIPT, self.transcript] + [str(a) for a in extra]

    def start_owned(self, *extra):
        """fake claude (sh) -> RUNNER (python) -> watcher. Returns the fake owner's Popen."""
        claude = os.path.join(self.dir, "claude")
        os.symlink("/bin/sh", claude)
        # `& wait` keeps sh from exec'ing its last command, so the claude process stays the parent.
        argv = [claude, "-c", '"$@" & wait', "claude", sys.executable, "-B", "-S", "-c", RUNNER,
                self.out, self.err, self.rc] + self.watch_args(*extra)
        return self.track(subprocess.Popen(argv, start_new_session=True))

    def wait_rc(self, timeout):
        end = time.time() + timeout
        while time.time() < end:
            if os.path.exists(self.rc):
                return int(self.read(self.rc))
            time.sleep(0.05)
        return None

    def read(self, path):
        """The runner creates out/err after its own start, so a missing file reads as empty."""
        try:
            with open(path) as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def wait_out(self, timeout):
        end = time.time() + timeout
        while time.time() < end and not self.read(self.out):
            time.sleep(0.05)
        time.sleep(0.2)
        return self.read(self.out)

    def test_owner_gone_exits(self):
        # The WARN line is printed only after the owner walk, so the owner is killed after the watcher found it.
        write_transcript(self.transcript, 250000)
        owner = self.start_owned(300000, 1)
        self.assertTrue(self.wait_out(5), "watcher printed nothing within 5 s; stderr: " + self.read(self.err))
        self.assertIsNone(owner.poll(), "fake owner died early")
        self.assertFalse(os.path.exists(self.rc), "watcher exited while owner alive: " + self.read(self.err))
        owner.kill()
        owner.wait()
        self.assertEqual(self.wait_rc(5), 0, "watcher did not exit 0 within 5 s of owner death")
        self.assertIn(f"context_watch: owner claude pid {owner.pid} gone; watcher exits", self.read(self.out))

    def test_refuses_without_claude_ancestor(self):
        argv = [sys.executable, "-B", "-S", "-c", ORPHAN, RUNNER, self.out, self.err, self.rc] + \
            self.watch_args(300000, 1)
        self.track(subprocess.Popen(argv, start_new_session=True))
        self.assertEqual(self.wait_rc(5), 1, "watcher without a claude ancestor did not exit 1 within 5 s")
        self.assertIn("context_watch: no claude ancestor found; refusing to run unowned", self.read(self.err))
        out = self.read(self.out)
        self.assertNotIn("WARN", out)
        self.assertNotIn("CEILING", out)

    def test_idle_transcript_exits(self):
        past = time.time() - 7200
        os.utime(self.transcript, (past, past))
        self.start_owned(300000, 1, 60)
        self.assertEqual(self.wait_rc(5), 0, "watcher on an idle transcript did not exit 0 within 5 s")
        self.assertIn("context_watch: transcript idle ", self.read(self.out))
        self.assertIn(" s >= 60 s; watcher exits", self.read(self.out))

    def test_fresh_transcript_keeps_running(self):
        owner = self.start_owned(300000, 1, 60)
        time.sleep(3)
        self.assertIsNone(owner.poll(), "fake owner died early")
        self.assertFalse(os.path.exists(self.rc), "watcher on a fresh transcript exited: " + self.read(self.out))

    def test_warn_line_unchanged(self):
        write_transcript(self.transcript, 250000)
        self.start_owned(300000, 1)
        lines = self.wait_out(5).splitlines()
        self.assertTrue(lines, "watcher printed nothing within 5 s; stderr: " + self.read(self.err))
        self.assertEqual(lines[0], "WARN: context 250,000 tokens >= 80% of ceiling 300,000")


if __name__ == "__main__":
    unittest.main()
