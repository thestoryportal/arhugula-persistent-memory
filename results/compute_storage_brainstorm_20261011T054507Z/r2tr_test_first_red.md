test_alias_cross_module (__main__.Fixtures) ... FAIL
test_argv_dispatch (__main__.Fixtures) ... FAIL
test_child_program_follows_stdin_loaded_phase (__main__.Fixtures) ... FAIL
test_direct_spawn (__main__.Fixtures) ... FAIL
test_disk_round_trip_is_loaded (__main__.Fixtures) ... FAIL
test_dynamic_call_unresolved (__main__.Fixtures) ... FAIL
test_external_boundary (__main__.Fixtures) ... FAIL
test_late_require_does_not_exclude (__main__.Fixtures) ... FAIL
test_loaded_list_count_and_operand (__main__.Fixtures) ... FAIL
test_pinned_loop_count (__main__.Fixtures) ... FAIL
test_require_excludes_before_spawn (__main__.Fixtures) ... FAIL
test_shell_branch_and_variable_command (__main__.Fixtures) ... FAIL
test_round12_F1_profile19_verifier_gap (__main__.RealControls) ... FAIL
test_round12_F2_evaluator_replication_gap (__main__.RealControls) ... FAIL

======================================================================
FAIL: test_alias_cross_module (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 40, in test_alias_cross_module
    r = self.trace({"entry.py": "import worker as R\nR.launch()\n", "worker.py": "from subprocess import check_output as start\ndef launch():\n    start(['/bin/echo', 'x'])\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_argv_dispatch (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 108, in test_argv_dispatch
    r = self.trace({"entry.py": "import sys, subprocess\nif sys.argv[1] == 'yes': subprocess.run(['/bin/echo','yes'])\n"}, ['no'])
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_child_program_follows_stdin_loaded_phase (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 112, in test_child_program_follows_stdin_loaded_phase
    r = self.trace({"entry.py": "import subprocess\nsubprocess.run(['/usr/bin/python3','child.py','verify'],input='{}')\n", "child.py": "import json,sys,subprocess\np=json.loads(sys.stdin.read())\nif p['phase']=='P3': subprocess.run(['/bin/echo','replication'])\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_direct_spawn (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 34, in test_direct_spawn
    r = self.trace({"entry.py": "import subprocess as sp\nsp.run(['/bin/echo', 'hello'])\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_disk_round_trip_is_loaded (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 60, in test_disk_round_trip_is_loaded
    r = self.trace({"entry.py": """
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_dynamic_call_unresolved (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 95, in test_dynamic_call_unresolved
    r = self.trace({"entry.py": "getattr(object(), 'launch')()\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_external_boundary (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 116, in test_external_boundary
    r = self.trace({"entry.py": "import torch\ntorch.load('x')\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_late_require_does_not_exclude (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 83, in test_late_require_does_not_exclude
    r = self.trace({"entry.py": """
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_loaded_list_count_and_operand (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 46, in test_loaded_list_count_and_operand
    r = self.trace({"entry.py": """
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_pinned_loop_count (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 104, in test_pinned_loop_count
    r = self.trace({"entry.py": "import subprocess\nfor x in (1,2,3):\n subprocess.call(['/bin/echo',str(x)])\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_require_excludes_before_spawn (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 71, in test_require_excludes_before_spawn
    r = self.trace({"entry.py": """
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_shell_branch_and_variable_command (__main__.Fixtures)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 99, in test_shell_branch_and_variable_command
    r = self.trace({"entry.sh": "#!/bin/sh\nif [ -f proof.json ]; then\n /bin/echo yes\nelse\n $PROGRAM arg\nfi\n"})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 18, in trace
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_round12_F1_profile19_verifier_gap (__main__.RealControls)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 130, in test_round12_F1_profile19_verifier_gap
    r = self.run_control()
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 123, in run_control
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

======================================================================
FAIL: test_round12_F2_evaluator_replication_gap (__main__.RealControls)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 135, in test_round12_F2_evaluator_replication_gap
    r = self.run_control()
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/test_trace_r2_reachability.py", line 123, in run_control
    self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
AssertionError: False is not true : tracer implementation is absent (test-first RED)

----------------------------------------------------------------------
Ran 14 tests in 0.001s

FAILED (failures=14)

Incomplete implementation P7 run (before final shell/coverage hardening): exit 1\nUNRESOLVED 840; BOUNDARIES 17; REPRESENTED 125; REFUSED 114; GAP 281
F1/F2 computed positive controls:
[
  {
    "profile": 19,
    "entrypoint": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py",
    "argv": [
      "dispatch",
      "p1-project"
    ],
    "site": "experiments/track_c/c10w_oracle_train.py:65",
    "family": "require_training_preflight",
    "status": "GAP",
    "evidence": [],
    "chain": [
      "experiments/track_c/c10w_oracle_step0.py:436",
      "experiments/track_c/c10w_oracle_step0.py:441",
      "experiments/track_c/c10w_oracle_step0.py:386",
      "experiments/track_c/c10w_oracle_train.py:65"
    ],
    "count": {
      "kind": "pinned_constant",
      "maximum": 1,
      "enforcing_lines": [
        "experiments/track_c/c10w_oracle_train.py:65"
      ]
    },
    "operand_source": {
      "kind": "pinned_literal",
      "line": "experiments/track_c/c10w_oracle_train.py:65"
    }
  },
  {
    "profile": 4,
    "entrypoint": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_eval.py",
    "argv": [
      "P1",
      {
        "$bind": "phase_directory"
      },
      {
        "$bind": "step0_directory"
      }
    ],
    "site": "experiments/track_c/c10w_oracle_read.py:133",
    "family": "adapter_is_tracked",
    "status": "GAP",
    "evidence": [],
    "chain": [
      "experiments/track_c/c10w_oracle_eval.py:474",
      "experiments/track_c/c10w_oracle_eval.py:479",
      "experiments/track_c/c10w_oracle_eval.py:358",
      "experiments/track_c/c10w_oracle_eval.py:361",
      "experiments/track_c/c10w_oracle_train.py:65",
      "experiments/track_c/c10w_oracle_read.py:613",
      "experiments/track_c/c10w_oracle_read.py:614",
      "experiments/track_c/c10w_oracle_read.py:616",
      "experiments/track_c/c10w_oracle_read.py:588",
      "experiments/track_c/c10w_oracle_read.py:588",
      "experiments/track_c/c10w_oracle_read.py:537",
      "experiments/track_c/c10w_oracle_read.py:538",
      "experiments/track_c/c10w_oracle_read.py:549",
      "experiments/track_c/c10w_oracle_read.py:550",
      "experiments/track_c/c10w_oracle_read.py:140",
      "experiments/track_c/c10w_oracle_read.py:133"
    ],
    "count": {
      "kind": "loaded_data",
      "loops": [
        {
          "kind": "loaded_data",
          "source": "experiments/track_c/c10w_oracle_read.py:543 load_json(experiments/track_c/c10w_oracle_read.py:543 latest_directory(experiments/track_c/c10w_oracle_read.py:543)experiments/track_c/c10w_oracle_read.py:543)['train_records']",
          "reasons": [
            "loaded experiments/track_c/c10w_oracle_read.py:493 (p / 'HALT.json').exists()",
            "loaded experiments/track_c/c10w_oracle_read.py:490 base.glob(prefix.lower() + '_*')",
            "loaded experiments/track_c/c10w_oracle_read.py:490 p.is_dir()",
            "loaded experiments/track_c/c10w_oracle_read.py:89 Path(path).read_text()"
          ],
          "selection_line": "experiments/track_c/c10w_oracle_read.py:549"
        }
      ]
    },
    "operand_source": {
      "kind": "loaded_data",
      "record_field": "['/usr/bin/git', 'ls-files', '--error-unmatch', '--', str(p.relative_to(ROOT))]",
      "reasons": [
        "loaded experiments/track_c/c10w_oracle_read.py:493 (p / 'HALT.json').exists()",
        "loaded experiments/track_c/c10w_oracle_read.py:490 base.glob(prefix.lower() + '_*')",
        "loaded experiments/track_c/c10w_oracle_read.py:490 p.is_dir()",
        "loaded experiments/track_c/c10w_oracle_read.py:89 Path(path).read_text()"
      ]
    }
  }
]
