"""MB22 receipt tooling. Writes only beside this file; backup paths are read-only."""
import hashlib
import contextlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import time
from unittest import mock

RECEIPT = Path(__file__).resolve().parent
ROOT = RECEIPT.parent.parent


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def protected():
    home = Path.home()
    logs = home / "Library/Logs"
    roots = sorted(logs.glob("memit-gdrive-backup*"))
    roots += [home / "Applications/MemitGdriveBackup.app", home / "Library/LaunchAgents"]
    result = {"home": str(home), "paths": []}
    for root in roots:
        paths = [root]
        if root.is_dir() and not root.is_symlink():
            paths += sorted(root.rglob("*"))
        for path in paths:
            if not path.exists() and not path.is_symlink():
                result["paths"].append({"path": str(path), "exists": False})
                continue
            info = path.lstat()
            kind = "symlink" if stat.S_ISLNK(info.st_mode) else "file" if stat.S_ISREG(info.st_mode) else "directory"
            entry = {"path": str(path), "kind": kind, "mode": info.st_mode,
                     "size": info.st_size, "mtime_ns": info.st_mtime_ns}
            if kind == "file":
                entry["sha256"] = digest(path)
            elif kind == "symlink":
                entry["target"] = os.readlink(path)
                entry["sha256"] = hashlib.sha256(os.fsencode(entry["target"])).hexdigest()
            result["paths"].append(entry)
    return result


def red_index():
    text = (RECEIPT / "RED_suite.log").read_text()
    blocks = list(re.finditer(r"^(ERROR|FAIL): (test_\S+) \([^\n]+\)\n", text, re.M))
    summary = text[text.rfind("\nRan "):]
    count = int(re.search(r"Ran (\d+) tests", summary).group(1))
    if len(blocks) != count:
        raise RuntimeError("every test must be RED: %s failures / %s tests" % (len(blocks), count))
    index = []
    for i, block in enumerate(blocks):
        end = blocks[i+1].start() if i+1 < len(blocks) else text.rfind("\nRan ")
        name = "RED_" + block[2] + ".log"
        (RECEIPT / name).write_text(
            "Command: /usr/bin/python3 -B -m unittest tools.test_dashboard_storage -v\n"
            "Suite exit: 1; extracted verbatim test failure from RED_suite.log\n\n" +
            text[block.start():end] + summary)
        index.append({"test": block[2], "log": name, "result": block[1]})
    (RECEIPT / "RED_index.json").write_text(json.dumps(index, indent=2) + "\n")
    print("Saved %s individual RED logs from one %s-test invocation" % (len(index), count))


def measure_real():
    sys.path.insert(0, str(ROOT))
    from tools import dashboard_storage as storage
    home = Path.home()
    if str(home).startswith(("/tmp/", "/private/tmp/")):
        raise ValueError("measure-real requires real HOME")
    cache = storage.SizeCache(home=home, path=RECEIPT/"real_size_cache.json")
    began = time.monotonic()
    print("Starting real project-only scan with nice -n 19; cache is receipt-local", flush=True)
    cache.refresh()
    if cache.thread is not None:
        cache.thread.join()
    view = cache.snapshot()
    disks = {}
    for path in ("/", "/Volumes/memit"):
        try:
            disks[path] = storage.disk_space(path)
        except OSError as exc:
            disks[path] = {"error": str(exc)}
    value = {"home": str(home), "cache_override": str(cache.path), "wall_duration_s": time.monotonic()-began,
             "measured_duration_s": view.get("duration_s"), "failed_attempt_duration_s": view.get("last_duration_s"),
             "measured_at": view["measured_at"], "error": view["error"], "disks": disks,
             "default_cache": str(home/"Library/Caches/memit-dashboard/storage_sizes.json")}
    (RECEIPT/"real_measurement.json").write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")
    with mock.patch.object(sys, "argv", [str(ROOT/"tools/dashboard_storage.py"), "--once", "160", "40"]), \
         (RECEIPT/"once_real_machine_160.txt").open("w") as output, contextlib.redirect_stdout(output):
        storage.main(cache=cache)
    print(json.dumps(value, indent=2, sort_keys=True))


def audit():
    names = ["tools/dashboard_storage.py", "tools/dashboard_storage_tab.sh",
             "tools/team_dashboard.sh", "tools/test_dashboard_storage.py"]
    report = (RECEIPT/"build_report.md").read_text()
    pins = {name: digest(ROOT/name) for name in names}
    for name, sha in pins.items():
        if name not in report or sha not in report:
            raise RuntimeError("report hash missing or stale: " + name)
    before = json.loads((RECEIPT/"scope_before.json").read_text())
    for name, sha in before["protected_helpers"].items():
        if digest(ROOT/name) != sha:
            raise RuntimeError("protected dashboard helper changed: " + name)
    green = (RECEIPT/"GREEN.log").read_text()
    if not re.search(r"Ran 26 tests in .*\n\nOK\s*$", green):
        raise RuntimeError("missing final GREEN result")
    reds = json.loads((RECEIPT/"RED_index.json").read_text())
    if len(reds) != 26 or len({row["test"] for row in reds}) != 26:
        raise RuntimeError("incomplete RED index")
    for row in reds:
        if row["test"] not in (RECEIPT/row["log"]).read_text():
            raise RuntimeError("incorrect RED receipt")
    snapshots = ["once_%s_%s.txt" % (state, width) for state in ("disabled", "running", "finished", "history") for width in (80, 160)]
    snapshots.append("once_real_machine_160.txt")
    artifacts = {name: digest(RECEIPT/name) for name in snapshots}
    if (RECEIPT/"protected_before.json").read_bytes() != (RECEIPT/"protected_after.json").read_bytes():
        raise RuntimeError("protected path listings differ")
    value = {"files_sha256": pins, "red_test_count": len(reds), "green_test_count": 26,
             "protected_before_sha256": digest(RECEIPT/"protected_before.json"),
             "protected_after_sha256": digest(RECEIPT/"protected_after.json"),
             "green_sha256": digest(RECEIPT/"GREEN.log"), "snapshots_sha256": artifacts,
             "report_sha256": digest(RECEIPT/"build_report.md"),
             "backup_status_sha256_observed": digest(ROOT/"tools/backup_gdrive_status.py")}
    (RECEIPT/"final_audit.json").write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")
    print("Audit OK: 26 RED receipts, 26 GREEN tests, nine snapshots, report hashes current, protected listings identical")


if sys.argv[1] == "red-index":
    red_index()
elif sys.argv[1] in ("protect-before", "protect-after"):
    name = "protected_" + sys.argv[1].split("-")[1] + ".json"
    value = protected()
    (RECEIPT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    print(name + ": %s paths" % len(value["paths"]))
    if sys.argv[1] == "protect-after":
        if (RECEIPT / "protected_before.json").read_bytes() != (RECEIPT / name).read_bytes():
            raise RuntimeError("protected real paths changed")
        print("Protected real paths IDENTICAL (bytes, SHA-256, mtimes, listings)")
elif sys.argv[1] == "measure-real":
    measure_real()
elif sys.argv[1] == "audit":
    audit()
else:
    raise ValueError("unknown receipt operation")
