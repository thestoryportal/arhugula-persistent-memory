"""Model-free tests of code/lab/runners/c10w_p2_gate.py's GPU-exclusivity decision (P2 pre-run review, Astra B1)."""
import unittest
from unittest import mock
from lab.runners import c10w_p2_gate as G

WT = "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
CLT = "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python"
GPU_JOB = "79246 %s/.venv/bin/python -B %s/experiments/track_c/c10v_layerpick_arms.py pass1 --root %s" % (WT, WT, WT)
BENIGN = "\n".join([
    "58020 .venv/bin/python -B -m http.server 8765 --bind 0.0.0.0 --directory projects/labviz-spec-v3/receipts/bulk/labviz/site",
    "58100 .venv/bin/python -B code/apps/labviz/build.py",
    "46589 %s/.venv/bin/python -B %s/tools/context_watch.py /Users/u/.claude/projects/x/1a.jsonl 250000 60" % (WT, WT),
    "71015 %s %s/tools/dashboard_report.py" % (CLT, WT),
    "70895 %s %s/tools/dashboard_tile.py program LEAD" % (CLT, WT),
    "84594 /Users/robertrhu/.cache/uv/archive-v0/W34p/bin/python /Users/robertrhu/.cache/uv/archive-v0/W34p/bin/arxiv-mcp-server",
    "72909 /Users/robertrhu/.local/share/uv/tools/browser-harness/bin/python -m browser_harness.daemon",
    "46574 /bin/zsh -c -l eval 'W=x; .venv/bin/python -B c10w_oracle_step0.py'",
    "62978 codex -m gpt-6.1-sol -s workspace-write",
    "937 /Users/robertrhu/.local/share/uv/tools/pixeltable/lib/python3.11/site-packages/pg/bin/postgres -D x",
    "%s %s/.venv/bin/python -B %s/experiments/track_c/c10w_oracle_read.py" % (99, WT, WT),
    # the same tools from a v2-layout checkout
    "46590 %s/.venv/bin/python -B %s/code/agents/context_watch.py /Users/u/.claude/projects/x/1a.jsonl 250000 60" % (WT, WT),
    "71016 %s %s/code/apps/dashboard/dashboard_report.py" % (CLT, WT),
    "%s %s/.venv/bin/python -B %s/code/lab/track_c/c10w_oracle_read.py" % (100, WT, WT),
])


class BlockingProcesses(unittest.TestCase):
    def test_intel_copy_exact_controller(self):
        for exe in (CLT, "/Library/Developer/CommandLineTools/usr/bin/python3"):
            for path in ("tools/memit_intel_copy.py", "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/memit_intel_copy.py",
                         "code/ops/intel/memit_intel_copy.py", "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/code/ops/intel/memit_intel_copy.py"):
                line = "510 %s %s run --gen sample" % (exe, path)
                self.assertEqual(G.blocking_processes(line, own_pid=1), [])

    def test_intel_copy_near_misses_block(self):
        for exe, path, args in (
            (CLT, "tools/memit_intel_copy_other.py", "run"),
            (WT + "/.venv/bin/python", "code/ops/intel/memit_intel_copy.py", "run"),
            (CLT, "code/ops/intel/x/../memit_intel_copy.py", "run"),
            (CLT, "/tmp/tools/memit_intel_copy.py", "run"),
            (CLT, "code/ops/intel/memit_intel_copy.py/evil.py", "run"),
            (CLT, "code/ops/intel/memit_intel_copy.py", "bogus"),
        ):
            line = "511 %s %s %s" % (exe, path, args)
            self.assertEqual(G.blocking_processes(line, own_pid=1), [line])

    def test_benign_inventory_admits(self):
        self.assertEqual(G.blocking_processes(BENIGN, own_pid=1), [])

    def test_gpu_job_blocks(self):
        self.assertEqual(G.blocking_processes(BENIGN + "\n" + GPU_JOB, own_pid=1), [GPU_JOB])

    def test_unknown_python_blocks(self):
        line = "500 /opt/homebrew/bin/python3.12 train_something.py"
        self.assertEqual(G.blocking_processes(line, own_pid=1), [line])

    def test_framework_python_case_insensitive_blocks(self):
        line = "501 %s /tmp/unknown.py" % CLT
        self.assertEqual(G.blocking_processes(line, own_pid=1), [line])

    def test_local_model_runtimes_block(self):
        for line in ("502 /usr/local/bin/ollama serve", "503 /opt/llama.cpp/llama-server -m m.gguf", "504 /x/mlx_lm.server"):
            self.assertEqual(G.blocking_processes(line, own_pid=1), [line])

    def test_reader_exemption_is_exact(self):
        line = "505 %s/.venv/bin/python -B %s/experiments/track_c/c10w_oracle_eval.py P2" % (WT, WT)
        self.assertEqual(G.blocking_processes(line, own_pid=1), [line])

    def test_own_pid_skipped(self):
        self.assertEqual(G.blocking_processes(GPU_JOB, own_pid=79246), [])

    def test_tmux_exact_name(self):
        self.assertEqual(G.blocking_tmux("autoresearch2\nprogram\n"), [])
        self.assertEqual(G.blocking_tmux("program\nautoresearch\n"), ["autoresearch"])


class FailClosed(unittest.TestCase):
    def test_ps_failure_refuses(self):
        with mock.patch.object(G, "run", return_value=(1, "", "ps: Operation not permitted")):
            r = G.check_gpu()
        self.assertFalse(r["ok"]); self.assertIn("inventory failed", r["reason"])

    def test_empty_inventory_refuses(self):
        with mock.patch.object(G, "run", return_value=(0, "", "")):
            self.assertFalse(G.check_gpu()["ok"])

    def test_tmux_failure_refuses(self):
        replies = iter([(0, BENIGN, ""), (1, "", "tmux: permission denied")])
        with mock.patch.object(G, "run", side_effect=lambda *a, **k: next(replies)):
            r = G.check_gpu()
        self.assertFalse(r["ok"]); self.assertIn("tmux inventory failed", r["reason"])

    def test_tmux_connection_errors_refuse(self):
        for err in ("error connecting to /private/tmp/tmux-501/default (Permission denied)",
                    "error connecting to /private/tmp/tmux-501/default (Connection refused)"):
            replies = iter([(0, BENIGN, ""), (1, "", err)])
            with mock.patch.object(G, "run", side_effect=lambda *a, **k: next(replies)):
                self.assertFalse(G.check_gpu()["ok"], err)

    def test_no_tmux_server_admits(self):
        replies = iter([(0, BENIGN, ""), (1, "", "no server running on /private/tmp/tmux-501/default")])
        with mock.patch.object(G, "run", side_effect=lambda *a, **k: next(replies)):
            self.assertTrue(G.check_gpu()["ok"])


if __name__ == "__main__":
    unittest.main()
