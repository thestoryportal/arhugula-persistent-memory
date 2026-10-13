#!/usr/bin/env python3
"""Run the configured hooks with the Codex 0.162.1 shell contract."""
from __future__ import annotations

import json
import os
import platform
from pathlib import Path
import signal
import subprocess
import tempfile
import unittest

import codex_context_guard as guard


ROOT = Path(__file__).resolve().parents[2]
HOOKS = json.loads((ROOT / ".codex/hooks.json").read_text())["hooks"]


class CodexHooksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # SessionStart propagates the guard's readiness verdict (0 READY, 2 NOT-READY),
        # so its expected exit is whatever the guard says about this host.
        env = dict(os.environ, LLMDB_ROOT=str(ROOT), PYTHONPATH=str(ROOT / "code"))
        cls.preflight_result = subprocess.run(
            [os.sys.executable, "-B", str(ROOT / "code/agents/codex_context_guard.py"), "preflight", "--json"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=30,
        )
        cls.preflight_exit = cls.preflight_result.returncode
        # The authoritative position; the hooks must report its opening, not a stale copy.
        cls.latest = json.loads((ROOT / "program/program_state.json").read_text())["current_latest"]

    def test_guard_reads_current_position(self):
        result = self.preflight_result
        self.assertIn(result.returncode, (0, 2), result.stdout + result.stderr)
        position = json.loads(result.stdout)["current_position"]
        self.assertEqual(position.splitlines()[0], self.latest.splitlines()[0][:1200])
        self.assertTrue(self.latest.startswith(position), position)
        self.assertLessEqual(len(position.splitlines()), 6)

    @unittest.skipUnless(
        platform.system() == "Darwin" and platform.machine() == "arm64"
        and (ROOT / ".venv/bin/python").exists(),
        "READY requires Darwin arm64 and the project interpreter",
    )
    def test_ready_on_m3(self):
        result = self.preflight_result
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["verdict"], "READY")
        self.assertEqual(data["hard"], [])

    def test_no_pod_root_in_commands(self):
        for groups in HOOKS.values():
            for group in groups:
                for hook in group["hooks"]:
                    self.assertNotIn("/workspace", hook["command"])

    def test_commands_from_root_and_subfolder(self):
        for cwd in (ROOT, ROOT / "code/agents"):
            for event, groups in HOOKS.items():
                for group in groups:
                    for hook in group["hooks"]:
                        with self.subTest(cwd=cwd.relative_to(ROOT), event=event):
                            env = dict(os.environ)
                            env["LLMDB_ROOT"] = "/tmp/icm-stale-root-must-not-be-used"
                            env["PYTHONDONTWRITEBYTECODE"] = "1"
                            payload = {
                                "session_id": "icm-hook-test",
                                "transcript_path": "/tmp/icm-hook-test.jsonl",
                                "cwd": str(cwd),
                                "hook_event_name": event,
                                "permission_mode": "default",
                            }
                            if event == "SessionStart":
                                payload.update(source="startup", model="gpt-5.5")
                            elif event in ("PreToolUse", "PermissionRequest"):
                                payload.update(tool_name="Bash", tool_input={"command": "pwd"},
                                               tool_use_id="icm-hook-test-tool")
                            elif event == "Stop":
                                payload["stop_hook_active"] = False
                            process = subprocess.Popen(
                                [env.get("SHELL", "/bin/sh"), "-lc", hook["command"]],
                                cwd=cwd, env=env, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True,
                            )
                            try:
                                stdout, stderr = process.communicate(
                                    json.dumps(payload), timeout=min(hook["timeout"], 30)
                                )
                            except subprocess.TimeoutExpired:
                                os.killpg(process.pid, signal.SIGKILL)
                                stdout, stderr = process.communicate()
                                self.fail(f"{event} timed out: {stdout}\n{stderr}")
                            expected = self.preflight_exit if event == "SessionStart" else 0
                            self.assertIn(expected, (0, 2))
                            self.assertEqual(process.returncode, expected, stdout + stderr)
                            self.assertNotIn("Traceback", stdout + stderr)
                            if event == "SessionStart":
                                self.assertIn(self.latest.splitlines()[0][:1200], stdout)
                            elif event == "Stop":
                                self.assertTrue(json.loads(stdout)["continue"])


class HostProbeTest(unittest.TestCase):
    def healthy(self):
        return dict(accelerator=dict(torch="2.8.0", transformers="4.51.0", mps_available=True),
                    transformers="4.51.0", engine_present=True,
                    disk=dict(free_gb=20), ram=dict(available_gb=16),
                    model_present=True, network="ok", running=[],
                    git=dict(dirty_files=0), probe_errors={})

    def findings(self, data):
        self.assertTrue(callable(getattr(guard, "readiness_findings", None)),
                        "The guard needs a pure readiness seam")
        return guard.readiness_findings(data)

    def test_mps_unavailable_blocks(self):
        data = self.healthy()
        data["accelerator"]["mps_available"] = False
        hard, warn = self.findings(data)
        self.assertEqual(len(hard), 1)
        self.assertIn("MPS", hard[0])
        self.assertIn("not available", hard[0])
        self.assertEqual(warn, [])

    def test_engine_missing_blocks(self):
        data = self.healthy()
        data["engine_present"] = False
        hard, _ = self.findings(data)
        self.assertIn("MEMIT engine missing", hard[0])

    def test_warnings_and_thresholds(self):
        data = self.healthy()
        self.assertEqual(self.findings(data), ([], []))
        data.update(transformers="5.0.0", model_present=False, network="no")
        data["disk"]["free_gb"] = 19
        data["ram"]["available_gb"] = 15
        data["running"] = ["99 python train.py"]
        data["git"]["dirty_files"] = 1
        hard, warn = self.findings(data)
        self.assertEqual(hard, [])
        self.assertEqual(len(warn), 7)
        for word in ("transformers", "hf_cache", "network", "disk", "memory", "RUNNING", "git"):
            self.assertTrue(any(word in item for item in warn), (word, warn))

    def test_failed_optional_probes_warn(self):
        data = self.healthy()
        data.update(ram={"error": "sysctl denied"}, disk={"error": "disk denied"}, running=None)
        data["probe_errors"] = {"running experiments": "ps denied"}
        hard, warn = self.findings(data)
        self.assertEqual(hard, [])
        for cause in ("sysctl denied", "disk denied", "ps denied"):
            self.assertTrue(any(cause in item for item in warn), warn)

    def test_interpreter_failures_reach_cli(self):
        for interpreter, cause in ((str(ROOT / "missing-icm-test-python"), "missing"),
                                   ("/usr/bin/false", "exit 1"),
                                   ("/usr/bin/true", "JSON")):
            with self.subTest(interpreter=interpreter):
                env = dict(os.environ, LLMDB_ROOT=str(ROOT), PYTHONPATH=str(ROOT / "code"),
                           CODEX_GUARD_PYTHON=interpreter)
                result = subprocess.run(
                    [os.sys.executable, "-B", str(ROOT / "code/agents/codex_context_guard.py"),
                     "preflight", "--json"], cwd=ROOT, env=env,
                    capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                data = json.loads(result.stdout)
                self.assertEqual(data["verdict"], "NOT-READY")
                self.assertTrue(any("project interpreter" in item and cause in item
                                    for item in data["hard"]), data["hard"])

    def test_command_failure_and_timeout_are_visible(self):
        with self.assertRaisesRegex(RuntimeError, "exit 7.*control failed"):
            guard.sh([os.sys.executable, "-c", "import sys;sys.stderr.write('control failed');sys.exit(7)"])
        with self.assertRaisesRegex(RuntimeError, "timed out"):
            guard.sh([os.sys.executable, "-c", "import time;time.sleep(1)"], timeout=0.05)

    def test_vm_stat_available_memory(self):
        self.assertTrue(callable(getattr(guard, "parse_vm_stat", None)), "Missing vm_stat parser")
        sample = ("Mach Virtual Memory Statistics: (page size of 16384 bytes)\n"
                  "Pages free: 2.\nPages inactive: 3.\nPages speculative: 4.\n"
                  "Pages active: 100.\nPages purgeable: 20.\nPages wired down: 50.\n")
        self.assertEqual(guard.parse_vm_stat(sample), 147456)
        self.assertEqual(guard.parse_vm_stat(sample.replace("16384", "4096")), 36864)
        for bad in ("", sample.replace("16384", "0"), sample.replace("Pages inactive: 3.\n", ""),
                    sample.replace("Pages free: 2.", "Pages free: -2.")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                guard.parse_vm_stat(bad)

    def test_process_filter_excludes_ancestors_and_reuses_compute_rule(self):
        from lab.runners.c10w_p2_gate import blocking_processes
        self.assertTrue(callable(getattr(guard, "filter_processes", None)), "Missing process filter")
        inventory = ("1 0 /sbin/launchd\n"
                     "10 1 /usr/bin/python3 codex-parent.py\n"
                     "20 10 /usr/bin/python3 hook.py\n"
                     "30 20 /usr/bin/python3 guard.py\n"
                     "40 1 /tmp/.venv/bin/python train.py\n"
                     "50 1 /tmp/.venv/bin/python -B /tmp/code/agents/context_watch.py /tmp/session.jsonl 45 40\n"
                     "60 1 /usr/bin/ollama serve\n70 1 /bin/sh harmless.sh\n")
        self.assertEqual(guard.filter_processes(inventory, 30, blocking_processes),
                         ["40 /tmp/.venv/bin/python train.py", "60 /usr/bin/ollama serve"])
        for bad in ("", "invalid inventory", inventory.replace("30 20", "30 invalid"),
                    inventory.replace("30 20", "30 30")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                guard.filter_processes(bad, 30, blocking_processes)


class HostProbeCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Keep fixtures for review. The lane forbids file deletion.
        cls.fixtures = Path(tempfile.mkdtemp(prefix="icm-6e-cli-"))
        print(f"CLI fixtures: {cls.fixtures}", file=os.sys.stderr)
        cls.guard_path = Path(os.environ.get(
            "CODEX_HOOK_TEST_GUARD", ROOT / "code/agents/codex_context_guard.py"))

    def run_guard(self, name, *, mps, engine, mode="preflight"):
        root = self.fixtures / name
        root.mkdir()
        if engine:
            (root / "code/memit/vendor").mkdir(parents=True)
        # A real imported module fails before the host inventory can be read.
        gate = root / "code/lab/runners/c10w_p2_gate.py"
        gate.parent.mkdir(parents=True, exist_ok=True)
        gate.write_text("raise ImportError('process-filter import control')\n")
        interpreter = root / "probe-python"
        interpreter.write_text(
            "#!/usr/bin/python3\nimport json\nprint(json.dumps(" +
            repr(dict(torch="2.8.0", transformers="4.51.0", mps_available=mps)) + "))\n")
        interpreter.chmod(0o755)
        env = dict(os.environ, LLMDB_ROOT=str(root), PYTHONPATH=str(root / "code"),
                   CODEX_GUARD_PYTHON=str(interpreter))
        args = [os.sys.executable, "-B", str(self.guard_path), mode]
        if mode == "preflight":
            args.append("--json")
        result = subprocess.run(args, cwd=root, env=env, capture_output=True,
                                text=True, timeout=30)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        return result

    def test_mps_false_reaches_cli(self):
        result = self.run_guard("mps-false", mps=False, engine=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["verdict"], "NOT-READY")
        self.assertIs(data["accelerator"]["mps_available"], False)
        self.assertTrue(any("MPS" in finding for finding in data["hard"]), data["hard"])

    def test_missing_engine_reaches_cli(self):
        result = self.run_guard("engine-missing", mps=True, engine=False)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["verdict"], "NOT-READY")
        self.assertFalse(data["engine_present"])
        self.assertTrue(any("MEMIT engine missing" in finding for finding in data["hard"]), data["hard"])

    def test_process_filter_import_failure_warns_in_cli(self):
        result = self.run_guard("import-failure", mps=True, engine=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["verdict"], "READY")
        self.assertEqual(data["hard"], [])
        self.assertIsNone(data["running"])
        self.assertIn("process-filter import control", data["probe_errors"]["running experiments"])
        self.assertTrue(any("running experiments probe failed" in finding
                            and "process-filter import control" in finding for finding in data["warn"]),
                        data["warn"])
        posture = self.run_guard("import-failure-posture", mps=True, engine=True, mode="posture")
        self.assertEqual(posture.returncode, 0, posture.stdout + posture.stderr)
        self.assertIn("running=UNVERIFIED", posture.stdout)
        self.assertIn("running experiments probe failed", posture.stdout)
        self.assertIn("process-filter import control", posture.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
