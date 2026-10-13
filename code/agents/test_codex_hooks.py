#!/usr/bin/env python3
"""Run the configured hooks with the Codex 0.162.1 shell contract."""
from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
HOOKS = json.loads((ROOT / ".codex/hooks.json").read_text())["hooks"]


class CodexHooksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # SessionStart propagates the guard's readiness verdict (0 READY, 2 NOT-READY),
        # so its expected exit is whatever the guard says about this host.
        env = dict(os.environ, LLMDB_ROOT=str(ROOT), PYTHONPATH=str(ROOT / "code"))
        cls.preflight_exit = subprocess.run(
            [os.sys.executable, "-B", str(ROOT / "code/agents/codex_context_guard.py"), "preflight"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=30,
        ).returncode
        # The authoritative position; the hooks must report its opening, not a stale copy.
        cls.latest = json.loads((ROOT / "program/program_state.json").read_text())["current_latest"]

    def test_guard_reads_current_position(self):
        env = dict(os.environ, LLMDB_ROOT=str(ROOT), PYTHONPATH=str(ROOT / "code"))
        result = subprocess.run(
            [os.sys.executable, "-B", str(ROOT / "code/agents/codex_context_guard.py"),
             "preflight", "--json"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=30,
        )
        self.assertIn(result.returncode, (0, 2), result.stdout + result.stderr)
        position = json.loads(result.stdout)["current_position"]
        self.assertEqual(position.splitlines()[0], self.latest.splitlines()[0][:1200])
        self.assertTrue(self.latest.startswith(position), position)
        self.assertLessEqual(len(position.splitlines()), 6)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
