import json
from pathlib import Path
import tempfile
import unittest


class ProjectSettingsPathsTests(unittest.TestCase):
    # [LAW:single-enforcer] Real settings and refusal fixtures use one check.
    def assert_portable_env(self, path):
        settings = json.loads(path.read_text(encoding="utf-8"))
        for key, value in settings.get("env", {}).items():
            self.assertNotIn("/Volumes/", value, f"env.{key} in {path}")

    def settings_fixture(self, settings):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "settings.json"
        path.write_text(json.dumps(settings), encoding="utf-8")
        return path

    def test_tracked_env_has_no_machine_paths(self):
        root = Path(__file__).resolve().parents[2]
        self.assert_portable_env(root / ".claude" / "settings.json")

    def test_tracked_additional_directories_stays(self):
        root = Path(__file__).resolve().parents[2]
        settings = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(
            settings["permissions"].get("additionalDirectories"),
            ["/Volumes/memit/llm-database-poc-mirror"],
        )

    def test_check_refuses_machine_paths(self):
        for key in ("LLMDB_ROOT", "HF_HOME", "OTHER"):
            with self.subTest(key=key):
                path = self.settings_fixture(
                    {"env": {"SAFE": "relative/path", key: "prefix:/Volumes/fixture"}}
                )
                with self.assertRaisesRegex(AssertionError, f"env.{key}"):
                    self.assert_portable_env(path)

    def test_check_accepts_portable_env(self):
        path = self.settings_fixture({"env": {"CACHE": "relative/cache"}})
        self.assert_portable_env(path)

    def test_check_accepts_absent_env(self):
        path = self.settings_fixture({"permissions": {"additionalDirectories": ["/Volumes/fixture"]}})
        self.assert_portable_env(path)
