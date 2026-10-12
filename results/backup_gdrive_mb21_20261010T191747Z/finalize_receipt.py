"""Finalize external hashes and verify the append after intervening reads."""
import hashlib
import json
import os
from pathlib import Path

root = Path(os.environ["LLMDB_ROOT"])
receipt = Path(__file__).resolve().parent
before = json.loads((receipt/"hashes_before.json").read_bytes())
report_name = "results/backup_gdrive_build_report.md"
report = (root/report_name).read_bytes()
original = (receipt/"originals/backup_gdrive_build_report.md").read_bytes()
append = json.loads((receipt/"report_append_sha256.json").read_bytes())
assert report[:len(original)] == original
assert hashlib.sha256(report[len(original):]).hexdigest() == append["append_sha256"]
assert len(report) == append["original_bytes"]+append["appended_bytes"]
for case in ("manual-interleave", "crash-after-allocation", "recovery", "unresolved-compaction", "compaction-boundary"):
    assert ("host_launcher_checks_mb21.py "+case).encode() in report
assert (receipt/"real_paths_initial.json").read_bytes() == (receipt/"real_paths_before.json").read_bytes()
assert (receipt/"real_paths_before.json").read_bytes() == (receipt/"real_paths_after.json").read_bytes()
names = ["tools/backup_gdrive_status.py", "tools/launchd/MemitGdriveBackup.applescript",
         "tools/test_backup_gdrive_addendum.py", report_name,
         str(receipt.relative_to(root)/"host_launcher_checks_mb21.py")]
changed = {name: {"start_sha256": before.get(name),
                  "final_sha256": hashlib.sha256((root/name).read_bytes()).hexdigest()} for name in names}
changed[names[-1]]["copied_baseline_sha256"] = before[
    "results/backup_gdrive_mb20_20261010T180133Z/host_launcher_checks_mb20.py"]
protected = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in before if name not in names}
assert all(value == before[name] for name, value in protected.items())
receipt_files = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in sorted(receipt.rglob("*")) if path.is_file() and path.name != "hashes_final.json"}
manifest = {"changed_files": changed, "protected_files": protected,
            "receipt_files_start": "absent", "receipt_files_final_sha256": receipt_files,
            "manifest_self_hash": "excluded", "report_prior_bytes_preserved": True,
            "real_inventories_equal": True}
target = receipt/"hashes_final.json"
assert not target.exists(), "refusing to overwrite final manifest"
target.write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
assert json.loads(target.read_bytes()) == manifest
for name, value in receipt_files.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == value
for name, value in changed.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == value["final_sha256"]
print(json.dumps({"changed_files": changed, "receipt_files": len(receipt_files),
                  "report_prior_bytes_preserved": True, "real_inventories_equal": True}, indent=2))
