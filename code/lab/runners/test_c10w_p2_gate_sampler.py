"""Model-free tests: check_gpu admits only the compute sampler's exact command lines (LEAN follow-up Step 314)."""
import unittest
from unittest import mock
from lab.runners import c10w_p2_gate as G

M = "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory"
WT = M + "/.claude/worktrees/c10k-route-a"
CLT = "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python"
ROW = r"^\S*\.venv/bin/python -B \S*/code/agents/compute_sample\.py( .*)?$"


def sampler(root, args, exe=None):
    return "%s -B %s/code/agents/compute_sample.py%s" % (exe or root + "/.venv/bin/python", root, args)


# The sampler as ship.sh (--once) and an admission loop (--interval N OUT.tsv / OUT.tsv) start it, from two checkouts.
SAMPLER_LINES = [
    "600 " + sampler(M, " --once"),
    "601 " + sampler(M, " --interval 10 /Volumes/memit/corpus-consolidation-toolkit/workspace/load.tsv"),
    "602 " + sampler(M, " /Volumes/memit/corpus-consolidation-toolkit/workspace/load.tsv"),
    "603 " + sampler(WT, " --once"),
    "604 " + sampler(WT, " --interval 5 /tmp/load.tsv"),
]
GPU_JOB = "79246 %s/.venv/bin/python -B %s/code/lab/track_c/c10v_layerpick_arms.py pass1 --root %s" % (M, M, M)

PY = M + "/.venv/bin/python"
NEAR_MISSES = {
    "different script name": [
        "700 %s -B %s/code/agents/compute_sampler.py --once" % (PY, M),
        "701 %s -B %s/code/agents/compute_samples.py --once" % (PY, M),
        "702 %s -B %s/code/agents/context_sample.py --once" % (PY, M),
        "703 %s -B %s/code/agents/train_compute.py --once" % (PY, M),
    ],
    "compute_sample.py outside code/agents/": [
        "710 %s -B %s/tools/compute_sample.py --once" % (PY, M),
        "711 %s -B /tmp/compute_sample.py --once" % PY,
        "712 %s -B %s/code/compute_sample.py --once" % (PY, M),
        "713 %s -B %s/code/agents/sub/compute_sample.py --once" % (PY, M),
        "714 %s -B %s/code/agentsx/compute_sample.py --once" % (PY, M),
        "715 %s -B %s/xcode/agents/compute_sample.py --once" % (PY, M),
    ],
    "non-venv python": [
        "720 " + sampler(M, " --once", exe="/opt/homebrew/bin/python3"),
        "721 " + sampler(M, " --once", exe="/usr/bin/python3"),
        "722 " + sampler(M, " --once", exe=CLT),
        "723 " + sampler(M, " --once", exe=M + "/venv/bin/python"),
        "724 " + sampler(M, " --once", exe=M + "/.venv/bin/python3.12"),
        "725 " + sampler(M, " --once", exe=M + "/.venv/lib/python"),
    ],
    "-c command": [
        "730 %s -B -c import torch  # %s/code/agents/compute_sample.py --once" % (PY, M),
        "731 %s -c import runpy; runpy.run_path('%s/code/agents/compute_sample.py')" % (PY, M),
        "732 %s -B -c import torch" % PY,
    ],
    "suffix after compute_sample.py": [
        "740 %s -B %s/code/agents/compute_sample.py.bak --once" % (PY, M),
        "741 %s -B %s/code/agents/compute_sample.py.bak" % (PY, M),
        "742 %s -B %s/code/agents/compute_sample.pyc" % (PY, M),
        "743 %s -B %s/code/agents/compute_sample.py/evil.py --once" % (PY, M),
        "744 %s -B %s/code/agents/compute_sample.py--once" % (PY, M),
    ],
    "sampler name passed as an argument to another script": [
        "750 %s -B %s/code/lab/train.py %s/code/agents/compute_sample.py --once" % (PY, M, M),
        "751 %s -B %s/code/agents/other.py --script %s/code/agents/compute_sample.py" % (PY, M, M),
        "752 %s -B -m torch.distributed.run %s/code/agents/compute_sample.py --once" % (PY, M),
    ],
    "sampler without -B": [
        "760 %s %s/code/agents/compute_sample.py --once" % (PY, M),
        "761 %s -u %s/code/agents/compute_sample.py --once" % (PY, M),
    ],
}


class SamplerExemption(unittest.TestCase):
    def test_row_is_the_approved_pattern(self):
        self.assertEqual(G.EXEMPT.count(ROW), 1)

    def test_sampler_lines_admitted(self):
        for line in SAMPLER_LINES:
            with self.subTest(line=line):
                self.assertEqual(G.blocking_processes(line, own_pid=1), [])

    def test_sampler_lines_admitted_beside_a_gpu_job_that_still_blocks(self):
        inventory = "\n".join(SAMPLER_LINES + [GPU_JOB])
        self.assertEqual(G.blocking_processes(inventory, own_pid=1), [GPU_JOB])

    def test_near_misses_block(self):
        for kind, lines in NEAR_MISSES.items():
            for line in lines:
                with self.subTest(kind=kind, line=line):
                    self.assertEqual(G.blocking_processes(line, own_pid=1), [line])

    def test_near_misses_block_in_one_inventory_with_sampler(self):
        misses = [line for lines in NEAR_MISSES.values() for line in lines]
        inventory = "\n".join(SAMPLER_LINES + misses)
        self.assertEqual(G.blocking_processes(inventory, own_pid=1), misses)


class CheckGpuWithSampler(unittest.TestCase):
    # Only the ps/tmux probe is replaced; check_gpu's own decision runs unchanged.
    def test_sampler_running_leaves_gpu_idle(self):
        replies = iter([(0, "\n".join(SAMPLER_LINES) + "\n", ""), (1, "", "no server running on /private/tmp/tmux-501/default")])
        with mock.patch.object(G, "run", side_effect=lambda *a, **k: next(replies)):
            r = G.check_gpu()
        self.assertEqual(r, {"ok": True, "blocking_processes": [], "blocking_tmux": []})

    def test_near_miss_beside_sampler_refuses(self):
        miss = NEAR_MISSES["suffix after compute_sample.py"][0]
        replies = iter([(0, "\n".join(SAMPLER_LINES + [miss]) + "\n", ""), (1, "", "no server running on /private/tmp/tmux-501/default")])
        with mock.patch.object(G, "run", side_effect=lambda *a, **k: next(replies)):
            r = G.check_gpu()
        self.assertFalse(r["ok"]); self.assertEqual(r["blocking_processes"], [miss])


if __name__ == "__main__":
    unittest.main()
