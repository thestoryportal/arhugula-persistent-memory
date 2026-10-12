"""Syntax, pins, exact publisher scope and fixture/isolation verification."""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(os.environ["LLMDB_ROOT"])
receipt = Path(__file__).resolve().parent
before = json.loads((receipt/"hashes_before.json").read_bytes())
changed = ["tools/backup_gdrive_status.py", "tools/launchd/MemitGdriveBackup.applescript",
           "tools/test_backup_gdrive_addendum.py"]
checks = []

def observed(command, *, input=None):
    result = subprocess.run(command, input=input, capture_output=True, text=True, timeout=10)
    row = {"args": command, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    checks.append(row)
    assert result.returncode == 0, row
    return result

for name in [changed[0], changed[2], str(receipt.relative_to(root)/"host_launcher_checks_mb21.py")]:
    source = (root/name).read_text()
    compile(source, name, "exec")
    checks.append({"python_syntax": name, "status": "PASS", "writes_bytecode": False})

applet = (root/changed[1]).read_text()
original = (receipt/"originals/MemitGdriveBackup.applescript").read_text()
old = "$completed >= $state->{compaction_barrier}"
assert original.count(old) == 2
assert applet == original.replace(old, "$completed > $state->{compaction_barrier}")
literals = {name: json.loads(value) for name, value in
            re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', applet, re.M)}
for name in ("generationShell", "launchShell", "receiptShell"):
    observed(["/bin/sh", "-n"], input=literals[name])
    if name == "launchShell":
        continue
    match = re.search(r" -e '(.*?)\n'", literals[name], re.S)
    assert match, "missing embedded Perl program"
    result = observed(["/usr/bin/perl", "-MJSON::PP", "-MFcntl=:flock", "-MFile::Path=make_path",
                       "-MFile::Temp=tempfile", "-MTime::HiRes=gettimeofday", "-MPOSIX=strftime",
                       "-c", "-e", match[1]])
    assert "syntax OK" in result.stdout+result.stderr

help_result = observed([sys.executable, "-B", str(receipt/"host_launcher_checks_mb21.py"), "--help"])
assert "compaction-boundary" in help_result.stdout
(receipt/"host_helper_help.txt").write_text(help_result.stdout)
help_result = observed([sys.executable, "-B", str(root/changed[0]), "recover", "--help"])
assert "--generation-floor" in help_result.stdout and "--heartbeat" in help_result.stdout
(receipt/"recovery_help.txt").write_text(help_result.stdout)

for name in changed:
    original = receipt/"originals"/Path(name).name
    diff = "".join(difflib.unified_diff(original.read_text().splitlines(True), (root/name).read_text().splitlines(True),
                                       fromfile="MB20/"+name, tofile="MB21/"+name))
    assert diff
    assert not any(line.startswith("+") and not line.startswith("+++") and line[1:].rstrip() != line[1:]
                   for line in diff.splitlines()), "new trailing whitespace"
    (receipt/(Path(name).name+".diff")).write_text(diff)

protected = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in before
             if name not in changed and name != "results/backup_gdrive_build_report.md"}
assert all(value == before[name] for name, value in protected.items())
fixture = receipt/"mb14_fixture"
for row in json.loads((receipt/"mb14_fixture_tree_sha256.json").read_bytes()):
    if row["kind"] == "file":
        assert hashlib.sha256((fixture/row["path"]).read_bytes()).hexdigest() == row["sha256"]
real_before = (receipt/"real_paths_before.json").read_bytes()
assert real_before == (receipt/"real_paths_after.json").read_bytes()
inventory = json.loads(real_before)
red = json.loads((receipt/"RED_index.json").read_bytes())
assert len(red) == 8
for row in red:
    data = (receipt/row["log"]).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row["sha256"] and ("FAIL: "+row["test"].split(".")[-1]).encode() in data
green = json.loads((receipt/"GREEN_commands.json").read_bytes())
assert sum(row["count"] for row in green) == 15 and all(row["exit_code"] == 0 for row in green)
summary = {"status": "PASS", "green_count": 15, "skipped": 0, "new_or_reversed_red_count": len(red),
           "native_cases": "UNRUN / HOST-PENDING", "activation": "BLOCKED pending Astra GO",
           "real_inventory": {"equal": True, "entries": len(inventory),
                              "files": sum(row["kind"] == "file" for row in inventory),
                              "sha256": hashlib.sha256(real_before).hexdigest()},
           "protected_hashes": protected, "checks": checks}
(receipt/"verification.json").write_text(json.dumps(summary, indent=2)+"\n")
print(json.dumps({key: value for key, value in summary.items() if key not in ("checks", "protected_hashes")}, indent=2))
