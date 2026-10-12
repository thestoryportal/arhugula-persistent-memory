"""Capture one actual pinned MB14 recovery; all writes stay in this receipt."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(os.environ["LLMDB_ROOT"])
receipt = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
os.environ["BACKUP_TEST_RECEIPTS"] = str(receipt/"fixtures")
os.environ["BACKUP_TEST_NO_RCLONE"] = "1"
from tools.test_backup_gdrive_addendum import R5RecoveryTest

paths = ["tools/backup_gdrive_status.py", "tools/launchd/MemitGdriveBackup.applescript",
         "tools/test_backup_gdrive_addendum.py", "tools/backup_gdrive.sh",
         "results/backup_gdrive_build_report.md",
         "results/backup_gdrive_mb20_20261010T180133Z/originals/backup_gdrive_status.py",
         "results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py",
         "results/backup_gdrive_mb20_20261010T180133Z/real_path_listing.py"]
hashes = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in paths}
(receipt/"hashes_before.json").write_text(json.dumps(hashes, indent=2, sort_keys=True)+"\n")
original = root/paths[5]
assert hashes[paths[5]] == "64d59eabbf4176c67451309a261cdd87e3c0b137094cde217e064a47a9793c9b"
case = R5RecoveryTest("test_1_torn_journal_preserves_generation_and_entire_ambiguous_file")
try:
    case.setUp()
    case.damaged_history(True)
    assert not (case.counter.parent/"unresolved.json").exists()
    command = [sys.executable, "-B", str(original), "recover", "--heartbeat", str(case.heartbeat),
               "--generation-floor", "10"]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=5)
    (receipt/"mb14_recovery_command.json").write_text(json.dumps({"args": command,
        "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}, indent=2)+"\n")
    assert completed.returncode == 0, completed.stdout+completed.stderr
    assert case.counter.read_bytes() == b"11\n"
    archives = case.counter.parent/"recoveries"
    archive, = archives.iterdir()
    manifest = json.loads((archive/"manifest.json").read_bytes())
    assert (manifest["highest_seen"], manifest["recovery_barrier"]) == (10, 11)
    target = receipt/"mb14_fixture"
    target.mkdir()
    shutil.copytree(archives, target/"recoveries")
    for name in ("counter", "unresolved.json", "counter.lock"):
        shutil.copy2(case.counter.parent/name, target/name)
    rows = [{"path": str(path.relative_to(target)), "kind": "file" if path.is_file() else "directory",
             **({"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
                if path.is_file() else {})} for path in sorted(target.rglob("*"))]
    (receipt/"mb14_fixture_tree_sha256.json").write_text(json.dumps(rows, indent=2)+"\n")
    print(json.dumps({"exit_code": completed.returncode, "barrier": 11, "tree": rows}, indent=2))
finally:
    assert case.doCleanups(), "fixture cleanup failed"
