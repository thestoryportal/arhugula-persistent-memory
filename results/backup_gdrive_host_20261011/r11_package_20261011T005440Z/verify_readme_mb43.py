"""Check MB43 report against raw receipts, protected bytes and final manifests."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHANGED = {"README.md", "activation_plan_v2.md", "host_commands.sh", "host_commands.md",
           "pins_v2.sha256", "pins_v2.json", "bulk_not_in_git_sha256.json"}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    entry = json.loads((HERE / "mb43_entry_snapshot.json").read_text())
    preserved = 0
    for name, expected in entry["hashes"].items():
        path = ROOT / name
        relative = path.relative_to(HERE).as_posix()
        if relative in CHANGED or relative.startswith("commands/mb43_entry_audit/"):
            continue
        assert digest(path) == expected, "changed historical evidence: " + name
        preserved += 1
    for name, expected in {**entry["protected"], **entry["diskutil_inputs"]}.items():
        assert digest(ROOT / name) == expected, "STOP protected drift: " + name
    pins = json.loads((HERE / "pins_v2.json").read_text())
    assert len(pins["files"]) == pins["pin_count"]
    expected_sha = ""
    for item in pins["files"]:
        path = ROOT / item["path"]
        assert digest(path) == item["sha256"] and path.stat().st_size == item["size"], item["path"]
        expected_sha += item["sha256"] + "  " + item["path"] + "\n"
    assert (HERE / "pins_v2.sha256").read_text() == expected_sha
    current = (HERE / "README.md").read_text().split("## Preserved MB42 handoff and historical reports", 1)[0]
    for label in ("mb43_sandbox_green", "mb43_package_green", "mb43_e_red", "mb43_check_v1_red", "mb43_check_v2_green"):
        run = HERE / label
        result = json.loads((run / "result.json").read_text())
        assert result["real_inventory_identical"] and result["all_owned_groups_exited"], label
        assert (run / "real_before.json").read_bytes() == (run / "real_after.json").read_bytes(), label
        assert (run / "real_after.json").read_bytes() == (HERE / "mb40_staging_green/real_after.json").read_bytes(), label
        assert (run / "exit_code.txt").read_text().strip() == ("1" if label == "mb43_e_red" else "0"), label
    suite = json.loads((HERE / "mb43_sandbox_green/result.json").read_text())
    assert (suite["testsRun"], suite["failures"], suite["errors"], suite["skipped"]) == (151, 0, 0, 14)
    assert suite["success"]
    for skip in suite["skips"]:
        assert "| `" + skip["test"] + "` | " + skip["reason"] + " |" in current
    native = json.loads((HERE / "mb43_sandbox_green/native_not_run.json").read_text())
    assert len(native) == 4
    for name in native:
        assert "- `" + name + "`" in current
    package = HERE / "mb43_package_green"
    assert json.loads((package / "result.json").read_text())["success"]
    log = (package / "driver.stderr.txt").read_text()
    assert re.search(r"Ran 55 tests in ", log) and log.rstrip().endswith("OK")
    red = json.loads((HERE / "mb43_e_red/result.json").read_text())
    assert (red["testsRun"], red["failures"], red["errors"], red["skipped"]) == (1, 2, 0, 0)
    assert "UNSET" in (HERE / "mb43_e_red/test.log").read_text()
    assert json.loads((HERE / "mb43_check_v1_red/result.json").read_text())["child_exit_code"] == 1
    assert (HERE / "mb43_check_v2_green/driver.stdout.txt").read_text().strip() == "PASS []"
    for label, count in (("mb43_refresh_green", 3), ("mb43_host_root_green", 1)):
        folder = HERE / "commands" / label
        log = (folder / "stderr.txt").read_text()
        assert re.search(r"Ran " + str(count) + r" tests? in ", log) and log.rstrip().endswith("OK")
        assert (folder / "exit_code.txt").read_text().strip() == "0"
    bulk = json.loads((HERE / "bulk_not_in_git_sha256.json").read_text())
    actual_bulk = [dict(path=str(path.relative_to(HERE)), size=path.stat().st_size, sha256=digest(path))
                   for path in sorted(HERE.rglob("*")) if path.is_file() and path.stat().st_size > bulk["threshold_bytes"]]
    assert actual_bulk == bulk["files"]
    receipt_bytes = sum(path.stat().st_size for path in HERE.rglob("*") if path.is_file())
    assert receipt_bytes < 200_000_000
    assert "55 run, 55 pass" in current and "151 run: 137 pass" in current
    assert "host UNRUN" in current and "r11_hostfix1_" in current
    for criterion in ("2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "5.1", "5.2", "5.3", "E.1", "E.2", "E.3", "E.4"):
        assert "| " + criterion + " |" in current, criterion
    print(json.dumps(dict(result="PASS", preserved_entry_files=preserved, pins=len(pins["files"]),
                          skips_listed=14, native_exclusions_listed=4, receipt_bytes=receipt_bytes,
                          README_sha256=digest(HERE / "README.md"))))

if __name__ == "__main__":
    main()
