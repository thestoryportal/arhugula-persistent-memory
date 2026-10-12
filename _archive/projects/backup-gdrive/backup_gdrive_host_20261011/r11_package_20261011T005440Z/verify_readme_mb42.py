"""Reconcile the final report with recorded bytes and raw evidence; read-only."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    entry = json.loads((HERE / "mb42_entry_snapshot.json").read_text())["hashes"]
    changed = {str(HERE.relative_to(ROOT) / name) for name in
               ("host_commands.md", "pins_v2.json", "pins_v2.sha256", "README.md")}
    for path, expected in entry.items():
        if path not in changed:
            assert digest(ROOT / path) == expected, path
    old = (HERE / "before/mb42_host_commands.md").read_text()
    expected_doc = "\n".join(
        "LLMDB_ROOT=$PWD " + line if line.startswith('/bin/sh "$R/host_commands.sh" ') else line
        for line in old.split("\n"))
    doc = (HERE / "host_commands.md").read_text()
    assert doc == expected_doc
    pins = json.loads((HERE / "pins_v2.json").read_text())
    expected_pins = json.loads((HERE / "before/mb42_pins_v2.json").read_text())
    doc_path = str(HERE.relative_to(ROOT) / "host_commands.md")
    matches = [item for item in expected_pins["files"] if item["path"] == doc_path]
    assert len(matches) == 1
    old_digest = matches[0]["sha256"]
    matches[0].update(sha256=digest(HERE / "host_commands.md"),
                      size=(HERE / "host_commands.md").stat().st_size)
    assert pins == expected_pins
    expected_sha = (HERE / "before/mb42_pins_v2.sha256").read_text().replace(
        old_digest + "  " + doc_path, matches[0]["sha256"] + "  " + doc_path)
    assert (HERE / "pins_v2.sha256").read_text() == expected_sha
    assert len(pins["files"]) == 27
    for item in pins["files"]:
        path = ROOT / item["path"]
        assert digest(path) == item["sha256"]
        assert path.stat().st_size == item["size"]

    text = (HERE / "README.md").read_text()
    assert text.startswith("# MB42")
    assert "## Single next step" in text
    assert "host/native" in text.lower() and "UNRUN" in text
    assert "MB42 HANDOFF" in text and "HOLD PYTHON" in text
    assert ">=60%" in text and "<=40%" in text
    commands = doc.split("```sh\n", 1)[1].split("\n```", 1)[0]
    assert commands in text
    for section, end in (("2", 4), ("3", 3), ("4", 7), ("5", 3), ("E", 4)):
        for number in range(1, end + 1):
            assert "| " + section + "." + str(number) + " |" in text
    astra = text.split("## Astra r11 map", 1)[1]
    for item in ("1", "2", "3", "4", "5", "E"):
        assert "| " + item + " |" in astra
    suite = json.loads((HERE / "mb41_sandbox_green/result.json").read_text())
    for skip in suite["skips"]:
        assert "| `" + skip["test"] + "` | " + skip["reason"] + " |" in text
    native = json.loads((HERE / "mb41_sandbox_green/native_not_run.json").read_text())
    for name in native:
        assert "- `" + name + "`" in text
    assert "151 run: 137 pass, 14 real-rclone skips, 0 failures/errors" in text
    assert "39 run, 39 pass, 0 skips/failures/errors" in text
    assert "GREEN 2 run/2 pass/0 skips/failures/errors" in text
    for label, code, ending in (
        ("mb42_host_root_red", 1, "FAILED (failures=1)"),
        ("mb42_host_root_green", 0, "OK"),
        ("mb42_pins_test_green", 0, "OK")):
        folder = HERE / "commands" / label
        assert int((folder / "exit_code.txt").read_text()) == code
        log = (folder / "stderr.txt").read_text()
        assert "Ran 1 test in " in log and log.rstrip().endswith(ending)
    allowed = set(entry.values())
    allowed.update(digest(path) for path in HERE.rglob("*") if path.is_file())
    allowed.update(item["sha256"] for item in pins["files"])
    for value in re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", text):
        assert value in allowed, "unverified report SHA-256: " + value
    bulk = json.loads((HERE / "bulk_not_in_git_sha256.json").read_text())
    current_bulk = [{"path": str(path.relative_to(HERE)),
                     "size": path.stat().st_size, "sha256": digest(path)}
                    for path in sorted(HERE.rglob("*"))
                    if path.is_file() and path.stat().st_size > bulk["threshold_bytes"]]
    assert current_bulk == bulk["files"]
    assert sum(path.stat().st_size for path in HERE.rglob("*") if path.is_file()) < 200_000_000
    print(json.dumps(dict(result="PASS", final_pins=27,
                          preserved_baseline=335, skips_listed=14,
                          native_exclusions_listed=4,
                          README_sha256=digest(HERE / "README.md"))))

if __name__ == "__main__":
    main()
