"""Run each touched class once per TDD phase and retain every result."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

receipt = Path(__file__).resolve().parent
root = Path(os.environ["LLMDB_ROOT"])
phase, = sys.argv[1:]
assert phase in ("RED", "GREEN")
os.environ.update(BACKUP_TEST_NO_RCLONE="1", BACKUP_TEST_RECEIPTS=str(receipt/"fixtures"),
                  PYTHONDONTWRITEBYTECODE="1")
expected = {
    "R5RecoveryTest": ["test_r6_1_mb14_archive_requires_floor_100_and_completion_102",
        "test_r6_1_every_archived_source_in_older_directories_counts",
        "test_r6_1_under_lock_rechecks_archived_journal",
        "test_r6_2_refusal_heartbeat_raises_floor_without_a_failure",
        "test_r6_2_under_lock_rechecks_refusal_heartbeat"],
    "R5CompactionTest": ["test_r6_3_compacted_barrier_requires_strictly_later_completion",
        "test_r6_3_python_and_both_perl_publishers_agree_at_boundaries",
        "test_r6_3_odd_failure_schedule_compacts_at_139"]}

def listing(name):
    command = [sys.executable, "-B", str(receipt/"real_path_listing.py"), str(receipt/name)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout+result.stderr
    assert isinstance(json.loads((receipt/name).read_bytes()), list)

if phase == "GREEN":
    listing("real_paths_before.json")
index, results = [], []
for class_name, tests in expected.items():
    command = [sys.executable, "-B", "-m", "unittest", "tools.test_backup_gdrive_addendum."+class_name, "-v"]
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=90)
    output = completed.stdout+completed.stderr
    log = receipt/(phase+"_"+class_name+".log")
    assert not log.exists(), "refusing to overwrite a TDD receipt"
    log.write_text(output)
    match = re.search(r"^Ran (\d+) tests? in", output, re.M)
    assert match, "missing unittest count; inspect "+str(log)
    counts = {"class": class_name, "phase": phase, "args": command, "exit_code": completed.returncode,
              "count": int(match[1]), "log": log.name,
              "sha256": hashlib.sha256(log.read_bytes()).hexdigest()}
    results.append(counts)
    print(json.dumps(counts), flush=True)
    assert not re.search(r"^ERROR:|skipped=|\.\.\. skipped", output, re.M), "unittest error or skip"
    if phase == "RED":
        failures = set(re.findall(r"^FAIL: (\w+)", output, re.M))
        assert completed.returncode != 0 and failures == set(tests), (failures, tests)
        for name in tests:
            individual = receipt/("RED_"+name+".log")
            individual.write_bytes(log.read_bytes())
            index.append({"test": "tools.test_backup_gdrive_addendum."+class_name+"."+name,
                          "log": individual.name, "class_log": log.name,
                          "sha256": hashlib.sha256(individual.read_bytes()).hexdigest()})
    else:
        assert completed.returncode == 0 and re.search(r"^OK$", output, re.M), "GREEN failed: "+str(log)
(receipt/(phase+"_commands.json")).write_text(json.dumps(results, indent=2)+"\n")
if phase == "RED":
    (receipt/"RED_index.json").write_text(json.dumps(index, indent=2)+"\n")
else:
    listing("real_paths_after.json")
    assert (receipt/"real_paths_before.json").read_bytes() == (receipt/"real_paths_after.json").read_bytes(), "real HOME changed"
    print("real HOME inventories byte-identical", flush=True)
