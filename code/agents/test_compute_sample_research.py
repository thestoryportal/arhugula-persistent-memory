"""Tests for compute_sample.py research_blockers (followup-308 Step 315) on literal check_gpu records, and --header."""
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute_sample as C  # noqa: E402

VENV = "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.venv/bin/python"
M = "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory"
FRAMEWORK = "/Library/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python"

COUNTED = {
    "ollama runtime": "901 /opt/homebrew/bin/ollama serve",
    "llama runtime": "902 /usr/local/bin/llama-server -m /models/q.gguf --port 8080",
    "mlx runtime": "903 /opt/mlx/bin/mlx_lm.server --model qwen",
    "code/lab absolute": f"904 {VENV} -B {M}/code/lab/track_c/c10w_oracle_train.py --stage P2a",
    "code/lab relative": f"905 {VENV} -u code/lab/runners/c10w_p2_dispatch.py",
    "code/memit absolute": f"906 {VENV} {M}/code/memit/apply_edit.py --config x.yaml",
    "code/memit relative": "907 python3 code/memit/apply_edit.py",
    "experiments absolute": f"908 {VENV} -B {M}/experiments/c10w/run_probe.py",
    "experiments relative": "909 python3.12 experiments/c10w/run_probe.py",
    "-m lab.": f"910 {VENV} -B -m lab.runners.c10w_p2_dispatch --stage P2a",
    "-m memit.": f"911 {VENV} -m memit.apply_edit",
    "framework Python code/lab": f"912 {FRAMEWORK} {M}/code/lab/scale/sweep.py",
    "option with argument before script": f"913 {VENV} -X importtime -W ignore code/lab/runners/x.py",
}
NOT_COUNTED = {
    "script under code/agents": f"921 {VENV} -B {M}/code/agents/context_watch.py /x/s.jsonl 300000 60",
    "-m unittest of a code/lab test module": f"922 {VENV} -B -m unittest code/lab/runners/test_c10w_p2_gate.py",
    "-m unittest discover in code/lab": f"923 {VENV} -B -m unittest discover -s code/lab/runners -p test_*.py",
    "-m unittest of a lab. module": f"924 {VENV} -m unittest lab.runners.test_c10w_p2_gate",
    "code/labviz substring": f"925 {VENV} -B {M}/code/labviz/build.py",
    "relative code/labviz substring": f"926 {VENV} code/labviz/build.py",
    "-m labviz substring": f"927 {VENV} -m labviz.serve",
    "-m memitx substring": f"928 {VENV} -m memit_tools.report",
    "scratch script": "929 python3 /private/tmp/scratch/probe.py",
    "tool module": f"930 {VENV} -B -m http.server 8000",
    "-c command naming code/lab": f"931 {VENV} -c exec(open('code/lab/x.py').read())",
    "script whose argument names code/lab": f"932 {VENV} {M}/code/ops/run.py code/lab/x.py -m lab.x",
    "bare interpreter": f"933 {VENV}",
}

OLD_COLUMNS = ("utc", "load1", "load5", "cpu_idle_pct", "mem_free_pct", "swap_used_mib",
               "astra_n", "astra_cpu_pct", "astra_rss_mib", "builders_n", "builders_cpu_pct", "builders_rss_mib",
               "tests_n", "tests_cpu_pct", "tests_rss_mib", "gpu_ok", "gpu_blockers", "memit_free_gib")


def record(procs=(), tmux=()):
    return {"ok": not procs and not tmux, "blocking_processes": list(procs), "blocking_tmux": list(tmux)}


class ResearchBlockers(unittest.TestCase):
    def test_each_counted_kind(self):
        for kind, line in COUNTED.items():
            with self.subTest(kind):
                self.assertEqual(C.research_blockers(record([line])), "1")

    def test_each_not_counted_kind(self):
        for kind, line in NOT_COUNTED.items():
            with self.subTest(kind):
                self.assertEqual(C.research_blockers(record([line])), "0")

    def test_autoresearch_tmux_counts(self):
        self.assertEqual(C.research_blockers(record(tmux=["autoresearch"])), "1")

    def test_sum_over_mixed_record(self):
        rec = record([*COUNTED.values(), *NOT_COUNTED.values()], ["autoresearch"])
        self.assertEqual(C.research_blockers(rec), str(len(COUNTED) + 1))

    def test_idle_record(self):
        self.assertEqual(C.research_blockers(record()), "0")

    def test_probe_failed(self):
        for reason in ("process inventory failed rc=1: x", "tmux inventory failed rc=1: permission denied"):
            with self.subTest(reason):
                self.assertEqual(C.research_blockers({"ok": False, "reason": reason}), "probe_failed")


class Width(unittest.TestCase):
    SAMPLE = dict(utc="2026-10-16T14:00:00Z", load1=3.1, load5=2.9, cpu_idle_pct=83.0, mem_free_pct=88,
                  swap_used_mib=3606.06, groups={g: (1, 2.0, 3.0) for g in C.GROUPS}, gpu=("0", "27"),
                  memit_free_gib=123.456, research_blockers="2")

    def test_header_is_old_columns_then_research_blockers(self):
        self.assertEqual(C.COLUMNS, (*OLD_COLUMNS, "research_blockers"))
        self.assertEqual(C.HEADER, "\t".join(C.COLUMNS) + "\n")

    def test_row_width_and_last_cell(self):
        cells = C.format_row(self.SAMPLE).rstrip("\n").split("\t")
        self.assertEqual(len(cells), len(C.COLUMNS))
        got = dict(zip(C.COLUMNS, cells))
        self.assertEqual(got["gpu_blockers"], "27")
        self.assertEqual(got["memit_free_gib"], "123.5")
        self.assertEqual(cells[-1], "2")
        probe_failed = C.format_row(dict(self.SAMPLE, research_blockers="probe_failed"))
        self.assertTrue(probe_failed.endswith("\t123.5\tprobe_failed\n"))


def _no_subprocess(*a, **k):
    raise AssertionError(f"--header ran a subprocess: {a!r}")


def _no_probe(*a, **k):
    raise AssertionError("--header ran check_gpu")


class Header(unittest.TestCase):
    def test_header_in_process_runs_no_probe(self):
        out = io.StringIO()
        with mock.patch.object(subprocess, "Popen", _no_subprocess), mock.patch.object(C, "check_gpu", _no_probe), \
                redirect_stdout(out):
            rc = C.main(["--header"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.getvalue(), C.HEADER)

    def test_header_cli(self):
        r = subprocess.run([sys.executable, "-B", str(Path(C.__file__)), "--header"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, C.HEADER)
        self.assertEqual(r.stderr, "")

    def test_header_with_once_is_refused(self):
        with mock.patch.object(subprocess, "Popen", _no_subprocess), mock.patch.object(C, "check_gpu", _no_probe), \
                redirect_stdout(io.StringIO()), mock.patch("sys.stderr", io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                C.main(["--header", "--once"])
        self.assertEqual(cm.exception.code, 2)


# Literal probe outputs (the formats compute_sample.py parses), so collect() runs without real commands.
PROBE_OUT = {
    "/usr/bin/top": "Load Avg: 3.10, 2.90, 2.70\nCPU usage: 10.0% user, 5.0% sys, 85.0% idle\n",
    "/usr/bin/memory_pressure": "System-wide memory free percentage: 88%\n",
    "/usr/sbin/sysctl": "vm.swapusage: total = 5120.00M  used = 3606.06M  free = 1513.94M  (encrypted)\n",
    "/bin/ps": "  905  50.0  2000000 /x/.venv/bin/python -u code/lab/runners/c10w_p2_dispatch.py\n",
}


class Collect(unittest.TestCase):
    def test_collect_takes_research_blockers_from_the_same_check_gpu_record(self):
        calls = []

        def fake_check_gpu():
            calls.append(1)
            return record([COUNTED["code/lab relative"], NOT_COUNTED["scratch script"]], ["autoresearch"])

        with mock.patch.object(C, "probe", lambda cmd: PROBE_OUT[cmd[0]]), mock.patch.object(C, "check_gpu", fake_check_gpu):
            sample = C.collect()
        self.assertEqual(len(calls), 1)
        self.assertEqual(sample["gpu"], ("0", "3"))
        self.assertEqual(sample["research_blockers"], "2")
        self.assertTrue(C.format_row(sample).endswith("\t2\n"))


class OnceRow(unittest.TestCase):
    def test_once_row_ends_with_research_blockers(self):
        r = subprocess.run([sys.executable, "-B", str(Path(C.__file__)), "--once"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        cells = r.stdout.rstrip("\n").split("\t")
        self.assertEqual(len(cells), len(C.COLUMNS))
        self.assertRegex(cells[-1], r"^(\d+|probe_failed)$")


if __name__ == "__main__":
    unittest.main()
