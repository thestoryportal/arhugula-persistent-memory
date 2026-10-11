"""Read-only checks for the MB43 pin and fresh host dispatch refresh."""
from pathlib import Path
import hashlib
import json
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LABELS = {
    "e-red": "e_red", "e-green": "e_green", "coverage": "py39_coverage",
    "fixture": "local_check", "frozen": "green", "package": "package_green",
    "check-red": "check_v1_red", "check-green": "check_v2_green", "pins": "pins",
}
PREFIX = "r11_hostfix1_"

class RefreshTest(unittest.TestCase):
    def test_all_nine_dispatch_and_preflight_labels_are_fresh(self):
        script = (HERE / "host_commands.sh").read_text()
        self.assertIn('"r11_hostfix1_preflight_$1"', script)
        for action, suffix in LABELS.items():
            label = PREFIX + suffix
            if action == "pins":
                self.assertIn('"$task_receipt" ' + label + ' /usr/bin/shasum', script)
                path = HERE / "commands" / label
            else:
                self.assertIn(action + ') task_label=' + label + ';', script)
                path = HERE / label
            self.assertFalse(path.exists(), "host label used: " + str(path))
            self.assertFalse((HERE / "commands" / (PREFIX + "preflight_" + action)).exists())
        frozen = ROOT / "results/backup_gdrive_host_20261010/locked_release_20261010T221519Z" / (PREFIX + "green_all")
        self.assertFalse(frozen.exists(), "frozen inner label already used")

    def test_pin_metadata_covers_new_regression_and_current_bytes(self):
        pins = json.loads((HERE / "pins_v2.json").read_text())
        paths = {item["path"] for item in pins["files"]}
        self.assertIn(str((HERE / "test_hostfix_mb42.py").relative_to(ROOT)), paths)
        self.assertEqual(pins["pin_count"], len(pins["files"]))
        for item in pins["files"]:
            self.assertEqual(hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest(), item["sha256"], item["path"])

    def test_host_docs_use_current_labels_counts_and_physical_gate(self):
        doc = (HERE / "host_commands.md").read_text()
        for suffix in LABELS.values():
            self.assertIn(PREFIX + suffix, doc)
        self.assertIn("55 package/helper tests", doc)
        for name in ("host_commands.md", "activation_plan_v2.md"):
            text = (HERE / name).read_text()
            for phrase in ("/private/tmp", "df -P", "APFSPhysicalStores", "disjoint", "STOP", "UNRUN"):
                self.assertIn(phrase, text, name + ": " + phrase)

if __name__ == "__main__":
    unittest.main(verbosity=2)
