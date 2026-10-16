"""Tests for code/agents/compute_sample.py: parsers on captured command output, the append file and the owner rule."""
import io
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute_sample as C  # noqa: E402

# Captured on the M3 on 2026-10-16 (`top -l 2 -n 0 -s 1`, trimmed).
TOP = """Processes: 812 total, 4 running, 808 sleeping, 4120 threads
2026/10/16 08:58:01
Load Avg: 6.73, 5.96, 4.72
CPU usage: 21.6% user, 12.17% sys, 66.75% idle
SharedLibs: 612M resident, 101M data, 66M linkedit.
Processes: 812 total, 3 running, 809 sleeping, 4118 threads
2026/10/16 08:58:02
Load Avg: 6.70, 5.95, 4.71
CPU usage: 12.54% user, 4.45% sys, 83.0% idle
SharedLibs: 612M resident, 101M data, 66M linkedit.
"""
MEMORY_PRESSURE = """The system has 51539607552 (12582912 pages with a page size of 4096).

Stats:
Pages free: 1234567
Pageouts: 952858

System-wide memory free percentage: 87%
"""
SWAP = "vm.swapusage: total = 5120.00M  used = 3606.06M  free = 1513.94M  (encrypted)\n"
PS = """    1   0.0  14000 /sbin/launchd
32291   0.5  81424 /Users/robertrhu/.codex/packages/app-server-daemon/releases/0.163.0-aarch64-apple-darwin/bin/codex app-server --listen unix://
40000  55.0 400000 /opt/homebrew/Caskroom/codex/0.162.1/bin/codex exec --model gpt-6-astra -s workspace-write
79979   8.2 1508752 claude --permission-mode auto
79980  10.0 512000 /Users/robertrhu/.local/bin/claude -p brief
 4536   0.0   2208 /bin/zsh /Volumes/memit/team/gauge.sh 47 codexoC2 claude-lane
86836   7.3  37296 /Volumes/memit/x/.venv/bin/python -B -m unittest discover -s code/tests -p test_git_automation.py
86837   2.7  10000 /opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python -m unittest -v x
86838   1.0  20000 /usr/bin/python3 -c print('-m unittest')
86839   1.0  20000 /usr/bin/python3 code/agents/context_watch.py t.jsonl
86840   1.0  20000 /usr/bin/python3 -B -m http.server 8765
50774   0.4 157456 /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --type=renderer
"""


class Parsers(unittest.TestCase):
    def test_top_takes_the_last_sample(self):
        self.assertEqual(C.parse_top(TOP), (6.70, 5.95, 83.0))

    def test_top_refuses_missing_lines(self):
        for text in ("", "Load Avg: 1.0, 2.0, 3.0\n", "CPU usage: 1% user, 1% sys, 98% idle\n"):
            with self.assertRaises(ValueError):
                C.parse_top(text)

    def test_memory_pressure(self):
        self.assertEqual(C.parse_memory_pressure(MEMORY_PRESSURE), 87)
        with self.assertRaises(ValueError):
            C.parse_memory_pressure("Pages free: 10\n")

    def test_swapusage_units(self):
        self.assertAlmostEqual(C.parse_swapusage(SWAP), 3606.06)
        self.assertAlmostEqual(C.parse_swapusage("vm.swapusage: total = 4.00G  used = 1.50G  free = 2.50G"), 1536.0)
        self.assertAlmostEqual(C.parse_swapusage("vm.swapusage: total = 0.00M  used = 512.00K  free = 0.00M"), 0.5)
        for bad in ("", "vm.swapusage: total = 1M", "vm.swapusage: used = 3T"):
            with self.assertRaises(ValueError):
                C.parse_swapusage(bad)

    def test_process_groups_by_executable(self):
        groups = C.parse_processes(PS)
        self.assertEqual(groups["astra"], (2, 55.5, round((81424 + 400000) / 1024, 1)))
        self.assertEqual(groups["builders"], (2, 18.2, round((1508752 + 512000) / 1024, 1)))
        self.assertEqual(groups["tests"], (2, 10.0, round((37296 + 10000) / 1024, 1)))

    def test_process_refuses_malformed_line(self):
        with self.assertRaises(ValueError):
            C.parse_processes("123 abc 100 /bin/x\n")
        with self.assertRaises(ValueError):
            C.parse_processes("123 1.0\n")
        with self.assertRaises(ValueError):
            C.parse_processes("")

    def test_gpu_summary(self):
        self.assertEqual(C.gpu_fields({"ok": True, "blocking_processes": [], "blocking_tmux": []}), ("1", "0"))
        self.assertEqual(C.gpu_fields({"ok": False, "blocking_processes": ["1 python x"], "blocking_tmux": ["autoresearch"]}), ("0", "2"))
        self.assertEqual(C.gpu_fields({"ok": False, "reason": "process inventory failed rc=1: x"}), ("0", "probe_failed"))

    def test_ppid_comm(self):
        self.assertEqual(C.parse_ppid_comm("79979 /Users/r/.local/bin/claude\n"), (79979, "claude"))
        self.assertEqual(C.parse_ppid_comm("  1 /bin/zsh"), (1, "zsh"))


class Row(unittest.TestCase):
    SAMPLE = dict(utc="2026-10-16T14:00:00Z", load1=3.1, load5=2.9, cpu_idle_pct=83.0, mem_free_pct=88,
                  swap_used_mib=3606.06, groups=C.parse_processes(PS), gpu=("1", "0"), memit_free_gib=123.456)

    def test_row_matches_header(self):
        row = C.format_row(self.SAMPLE)
        self.assertTrue(row.endswith("\n"))
        cells = row.rstrip("\n").split("\t")
        self.assertEqual(len(cells), len(C.COLUMNS))
        got = dict(zip(C.COLUMNS, cells))
        self.assertEqual(got["utc"], "2026-10-16T14:00:00Z")
        self.assertEqual(got["load1"], "3.10")
        self.assertEqual(got["mem_free_pct"], "88")
        self.assertEqual(got["swap_used_mib"], "3606.1")
        self.assertEqual(got["astra_n"], "2")
        self.assertEqual(got["builders_cpu_pct"], "18.2")
        self.assertEqual(got["tests_rss_mib"], str(round((37296 + 10000) / 1024, 1)))
        self.assertEqual(got["gpu_ok"], "1")
        self.assertEqual(got["memit_free_gib"], "123.5")


class Owner(unittest.TestCase):
    def test_walks_to_nearest_claude(self):
        table = {50: (40, "zsh"), 40: (30, "claude"), 30: (1, "claude")}
        self.assertEqual(C.owner_pid(50, lookup=table.get), 40)

    def test_refuses_without_claude(self):
        table = {50: (40, "zsh"), 40: (1, "launchd")}
        with self.assertRaises(SystemExit) as cm:
            C.owner_pid(50, lookup=table.get)
        self.assertNotEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit):
            C.owner_pid(50, lookup={}.get)

    def test_alive_on_real_processes(self):
        self.assertTrue(C.alive(os.getpid()))
        child = subprocess.Popen([sys.executable, "-c", "pass"])
        child.wait()
        self.assertFalse(C.alive(child.pid))


class AppendFile(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        for name in os.listdir(self.dir):
            os.unlink(os.path.join(self.dir, name))
        os.rmdir(self.dir)

    def test_new_file_gets_header_then_rows_append(self):
        path = os.path.join(self.dir, "load.tsv")
        fd = C.open_log(path)
        C.write_all(fd, "a\n")
        os.close(fd)
        fd = C.open_log(path)
        C.write_all(fd, "b\n")
        os.close(fd)
        self.assertEqual(Path(path).read_text(), C.HEADER + "a\nb\n")

    def test_refuses_foreign_file_unchanged(self):
        path = os.path.join(self.dir, "other.tsv")
        Path(path).write_text("something else\n")
        with self.assertRaises(C.Refusal):
            C.open_log(path)
        self.assertEqual(Path(path).read_text(), "something else\n")

    def test_refuses_symlink(self):
        target = os.path.join(self.dir, "target.tsv")
        Path(target).write_text(C.HEADER)
        link = os.path.join(self.dir, "link.tsv")
        os.symlink(target, link)
        with self.assertRaises(C.Refusal):
            C.open_log(link)
        self.assertEqual(Path(target).read_text(), C.HEADER)

    def test_refuses_fifo(self):
        path = os.path.join(self.dir, "fifo.tsv")
        os.mkfifo(path)
        with self.assertRaises(C.Refusal):
            C.open_log(path)


class Watch(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(self._cleanup)
        self.path = os.path.join(self.dir, "load.tsv")

    def _cleanup(self):
        for name in os.listdir(self.dir):
            os.unlink(os.path.join(self.dir, name))
        os.rmdir(self.dir)

    def _run(self, owner, interval):
        fd = C.open_log(self.path)
        self.addCleanup(os.close, fd)
        out = io.StringIO()
        calls = []

        def bounded_sleep(seconds):
            calls.append(seconds)
            if len(calls) > 100:
                raise AssertionError("watch did not exit after its owner was gone")
            time.sleep(seconds)

        with redirect_stdout(out):
            n = C.watch(fd, owner, interval, collect=lambda: Row.SAMPLE, sleep=bounded_sleep)
        return n, out.getvalue()

    def test_exits_when_owner_gone(self):
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(0.8)"])
        self.addCleanup(child.wait)
        reaper = threading.Thread(target=child.wait)
        reaper.start()
        self.addCleanup(reaper.join)
        n, out = self._run(child.pid, 0.1)
        self.assertGreaterEqual(n, 2)
        self.assertIn("owner claude pid %d gone" % child.pid, out)
        lines = Path(self.path).read_text().splitlines()
        self.assertEqual(lines[0] + "\n", C.HEADER)
        self.assertEqual(len(lines), n + 1)
        self.assertTrue(all(line + "\n" == C.format_row(Row.SAMPLE) for line in lines[1:]))

    def test_gone_owner_writes_no_row(self):
        child = subprocess.Popen([sys.executable, "-c", "pass"])
        child.wait()
        n, out = self._run(child.pid, 0.1)
        self.assertEqual(n, 0)
        self.assertEqual(Path(self.path).read_text(), C.HEADER)


class Cli(unittest.TestCase):
    def test_once_prints_one_real_row(self):
        r = subprocess.run([sys.executable, "-B", str(Path(C.__file__)), "--once"], capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.splitlines()
        self.assertEqual(len(lines), 1, r.stdout)
        cells = lines[0].split("\t")
        self.assertEqual(len(cells), len(C.COLUMNS))
        got = dict(zip(C.COLUMNS, cells))
        self.assertRegex(got["utc"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        self.assertGreaterEqual(int(got["builders_n"]), 1)  # this test runs under a claude builder or MAESTRO
        self.assertGreaterEqual(int(got["tests_n"]), 1)  # this unittest run itself
        self.assertIn(got["gpu_ok"], ("0", "1"))
        self.assertGreater(float(got["memit_free_gib"]), 0)

    def test_rejects_bad_interval(self):
        d = tempfile.mkdtemp()
        self.addCleanup(os.rmdir, d)
        path = os.path.join(d, "x.tsv")
        r = subprocess.run([sys.executable, "-B", str(Path(C.__file__)), "--interval", "0", path],
                           capture_output=True, text=True, timeout=30)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.lexists(path))


if __name__ == "__main__":
    unittest.main()
