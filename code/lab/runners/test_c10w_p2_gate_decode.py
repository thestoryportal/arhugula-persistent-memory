"""Tests for code/lab/runners/c10w_p2_gate.py (Step 341): command output holding a non-UTF-8 byte is decoded
with U+FFFD replacement, so check_gpu still returns one record and `compute_sample.py --once` still samples.

The 0xff bytes come from a real process: a child whose argv[0] is b"/bin/sl\\xffeep" (exec'd from /bin/sleep)
shows that byte in the `ps` command= column, which stopped the T209 and T218 ships (ledger 12:05:12Z, 12:08:27Z).
"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

from lab.runners import c10w_p2_gate as G

ROOT = Path(__file__).resolve().parents[3]
SAMPLER = ROOT / "code/agents/compute_sample.py"
FF_ARGV0 = b"/bin/sl\xffeep"
FF_TEXT = "/bin/sl�eep"
PS = ["/bin/ps", "-axww", "-o", "pid=,command="]


class Decode(unittest.TestCase):
    def ff_child(self):
        """A live process whose command line holds byte 0xff; killed and reaped at cleanup."""
        child = subprocess.Popen([FF_ARGV0, "30"], executable="/bin/sleep")
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        return child

    def test_run_replaces_ff_in_stdout_and_stderr(self):
        code = "import sys; sys.stdout.buffer.write(b'a\\xffb\\n'); sys.stderr.buffer.write(b'c\\xffd\\n')"
        self.assertEqual(G.run([sys.executable, "-c", code]), (0, "a�b\n", "c�d\n"))

    def test_check_gpu_with_ff_child_returns_one_record(self):
        child = self.ff_child()
        record = G.check_gpu()
        # Positive control: the child is still alive and the inventory check_gpu reads holds its line, byte replaced.
        rc, out, _ = G.run(PS)
        self.assertIsNone(child.poll())
        self.assertEqual(rc, 0)
        self.assertIn("%d %s 30" % (child.pid, FF_TEXT), [line.strip() for line in out.splitlines()])
        # The inventory record, not the "inventory failed" refusal shape.
        self.assertEqual(set(record), {"ok", "blocking_processes", "blocking_tmux"})
        self.assertIsInstance(record["ok"], bool)
        # The child is /bin/sleep, not compute work, so it never blocks.
        self.assertFalse([p for p in record["blocking_processes"] if p.split(" ", 1)[0] == str(child.pid)])

    def sampler(self, *args):
        env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "code/agents"), str(ROOT / "code")]))
        return subprocess.run([sys.executable, "-B", str(SAMPLER), *args], capture_output=True, text=True,
                              env=env, cwd=str(ROOT), timeout=120)

    def test_compute_sample_once_with_ff_child_prints_one_sample(self):
        header = self.sampler("--header")
        self.assertEqual((header.returncode, header.stderr), (0, ""))
        columns = header.stdout.rstrip("\n").split("\t")
        child = self.ff_child()
        once = self.sampler("--once")
        self.assertIsNone(child.poll())
        self.assertEqual((once.returncode, once.stderr), (0, ""))
        self.assertEqual(once.stdout.count("\n"), 1)
        self.assertTrue(once.stdout.endswith("\n"))
        self.assertEqual(len(once.stdout.rstrip("\n").split("\t")), len(columns))


if __name__ == "__main__":
    unittest.main()
