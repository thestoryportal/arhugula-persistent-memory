"""Tests for code/agents/compute_sample.py (Step 339): command output holding a non-UTF-8 byte is decoded
with U+FFFD replacement, so a probe still returns text and a sample is still taken.

The 0xff bytes come from real processes: a child whose argv[0] is b"/bin/sl\\xffeep" (exec'd from /bin/sleep)
shows that byte in `ps` comm= and command= columns, which is the T218 failure (ledger 2026-10-18T11:59:48Z).
"""
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute_sample as C  # noqa: E402

FF_ARGV0 = b"/bin/sl\xffeep"
FF_TEXT = "/bin/sl�eep"
IDLE_GPU = {"ok": True, "blocking_processes": [], "blocking_tmux": []}


class Decode(unittest.TestCase):
    def ff_child(self):
        """A live process whose command line holds byte 0xff; killed and reaped at cleanup."""
        child = subprocess.Popen([FF_ARGV0, "30"], executable="/bin/sleep")
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        return child

    def test_probe_replaces_ff_in_stdout(self):
        out = C.probe([sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'a\\xffb\\n')"])
        self.assertEqual(out, "a�b\n")

    def test_ps_inventory_with_ff_parses_to_one_sample(self):
        self.ff_child()
        # Positive control: the real inventory holds the replaced byte, so collect() parses it below.
        self.assertIn(FF_TEXT, C.probe(["/bin/ps", "-axww", "-o", "pid=,pcpu=,rss=,command="]))
        # check_gpu lives in lab.runners.c10w_p2_gate (not this tool); the record is fixed so the
        # sample depends only on compute_sample's own probes.
        with mock.patch.object(C, "check_gpu", lambda: IDLE_GPU):
            sample = C.collect()
        self.assertEqual(set(sample["groups"]), set(C.GROUPS))
        row = C.format_row(sample)
        self.assertEqual(row.count("\n"), 1)
        self.assertEqual(len(row.rstrip("\n").split("\t")), len(C.COLUMNS))

    def test_ppid_comm_lookup_replaces_ff(self):
        child = self.ff_child()
        self.assertEqual(C._ps_ppid_comm(child.pid), (os.getpid(), "sl�eep"))

    def test_alive_on_ff_ps_output_is_a_refusal(self):
        # `ps -o pid=` prints digits only, so the 0xff byte is put in its stdout: the real subprocess.run
        # runs a stand-in that writes it, with the keyword arguments alive() passed.
        real_run = subprocess.run

        def ps_prints_ff(cmd, **kwargs):
            self.assertEqual(cmd[0], "/bin/ps")
            return real_run([sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'\\xff\\n')"], **kwargs)

        with mock.patch.object(C.subprocess, "run", ps_prints_ff):
            with self.assertRaisesRegex(C.Refusal, r"unclear rc=0"):
                C.alive(os.getpid())


if __name__ == "__main__":
    unittest.main()
