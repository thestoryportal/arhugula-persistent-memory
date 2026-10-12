"""MB31 evidence capture only; never modifies worktree tools/ or tests/."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone

RECEIPT = Path(__file__).resolve().parent
WORKTREE = RECEIPT.parents[2]
EVIDENCE = RECEIPT / "evidence.json"
EXPECTED = {
    "tools/new1_supervisor.py": "3144949d9d9ed97739f4aa5e67250e5c72640796233a2b82963e3932a758a6af",
    "tests/test_new1_supervisor.py": "eccabf81552a1ec416d494e6b609597f902ec014f3fb7041059fc61dc73a8616",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    return {str(path.relative_to(WORKTREE)): sha(path)
            for folder in ("tools", "tests")
            for path in sorted((WORKTREE / folder).rglob("*")) if path.is_file()}


def save(evidence):
    EVIDENCE.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")


for name, expected in EXPECTED.items():
    actual = sha(WORKTREE / name)
    if actual != expected:
        raise SystemExit(f"STOPPED: {name}: expected {expected}, observed {actual}")

phase = sys.argv[1]
if phase == "red":
    if EVIDENCE.exists():
        raise SystemExit("Refusing to overwrite an existing evidence.json or rerun RED")
    copy = Path(subprocess.check_output(
        ["mktemp", "-d", "/private/tmp/new1_reap_r4_mb31.XXXXXX"], text=True).strip())
    if not copy.is_dir() or copy.parent != Path("/private/tmp"):
        raise SystemExit(f"Invalid mktemp directory: {copy}")
    for folder in ("tools", "tests"):
        subprocess.run(["/bin/cp", "-R", str(WORKTREE / folder), str(copy / folder)], check=True)
    shutil.copyfile(RECEIPT / "before/new1_supervisor.py", copy / "tools/new1_supervisor.py")
    for folder in ("tools", "tests"):
        for cache in (copy / folder).rglob("__pycache__"):
            shutil.rmtree(cache)
    fixtures = copy / "fixtures"
    support = copy / "receipt_support"
    fixtures.mkdir()
    support.mkdir()
    hook = support / "sitecustomize.py"
    hook.write_text('''"""Relocate hardcoded stdlib test fixture roots into MB31's copy."""
import json
import os
import tempfile

_fixture_root = os.environ["NEW1_RECEIPT_TMPROOT"]
_original_mkdtemp = tempfile.mkdtemp

def _receipt_mkdtemp(suffix=None, prefix=None, dir=None):
    requested = os.fspath(dir) if dir is not None else None
    if requested is not None and os.path.realpath(requested) == "/private/tmp":
        dir = _fixture_root
    result = _original_mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    if not os.path.realpath(result).startswith(os.path.realpath(_fixture_root) + os.sep):
        raise RuntimeError("receipt fixture escaped isolated copy: " + result)
    with open(os.environ["NEW1_RECEIPT_TMPLOG"], "a", encoding="utf-8") as record:
        record.write(json.dumps({"requested_dir": requested, "allocated_dir": result}) + "\\n")
    return result

tempfile.mkdtemp = _receipt_mkdtemp
''')
    evidence = {
        "task": "MB31 / MAESTRO26: NEW1 supervisor reap round 4 receipts",
        "status": "IN_PROGRESS",
        "worktree": str(WORKTREE),
        "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=WORKTREE, text=True).strip(),
        "wip_commit": subprocess.check_output(["git", "rev-parse", "ec7561d"], cwd=WORKTREE, text=True).strip(),
        "copy_dir": str(copy),
        "copy_method": "mktemp -d /private/tmp/new1_reap_r4_mb31.XXXXXX; cp -R tools and tests; copy before/new1_supervisor.py over copied tools/new1_supervisor.py",
        "worktree_scope_before": snapshot(),
        "fixture_hook": {"path": str(hook), "sha256": sha(hook),
            "purpose": "Redirect tempfile.mkdtemp(dir='/private/tmp') only; no changes to supervisor/tests or their assertions/release/signal behavior. Default temporary paths use TMPDIR inside the copy."},
        "disk_budget": {"projected_new_bytes_upper_bound": 8 * 1024 ** 2,
            "copy_volume_free_bytes": shutil.disk_usage(copy).free,
            "receipt_volume_free_bytes": shutil.disk_usage(RECEIPT).free},
        "runs": {},
    }
elif phase == "green":
    evidence = json.loads(EVIDENCE.read_text())
    copy = Path(evidence["copy_dir"])
    if "green" in evidence["runs"]:
        raise SystemExit("Refusing to rerun GREEN")
    if sha(Path(evidence["fixture_hook"]["path"])) != evidence["fixture_hook"]["sha256"]:
        raise SystemExit("Fixture routing hook changed")
else:
    raise SystemExit("usage: capture_receipts.py red|green")

cwd = copy if phase == "red" else WORKTREE
stem = "RED_causal_final" if phase == "red" else "GREEN_receipt"
command = (f"LLMDB_ROOT={shlex.quote(str(cwd))} PYTHONDONTWRITEBYTECODE=1 "
           f"{shlex.quote(str(WORKTREE / '.venv/bin/python'))} -B -m unittest -v tests.test_new1_supervisor")
env = os.environ.copy()
env.update({
    "PYTHONPATH": str(copy / "receipt_support"),
    "PYTHONPYCACHEPREFIX": str(copy / "empty_pycache"),
    "TMPDIR": str(copy / "fixtures"),
    "NEW1_RECEIPT_TMPROOT": str(copy / "fixtures"),
    "NEW1_RECEIPT_TMPLOG": str(copy / f"{stem}_fixture_roots.jsonl"),
})
record = {"cwd": str(cwd), "exact_command": command,
    "started_at": datetime.now(timezone.utc).isoformat(),
    "supervisor_sha256": sha(cwd / "tools/new1_supervisor.py"),
    "tests_sha256": sha(cwd / "tests/test_new1_supervisor.py"),
    "inherited_environment": {key: env[key] for key in (
        "PYTHONPATH", "PYTHONPYCACHEPREFIX", "TMPDIR", "NEW1_RECEIPT_TMPROOT", "NEW1_RECEIPT_TMPLOG")},
    "log": stem + ".log", "exit_file": stem + ".exit"}
evidence["runs"][phase] = record
save(evidence)  # Provenance is durable on disk before the command is started.
with (RECEIPT / record["log"]).open("xb") as output:
    result = subprocess.run(["/bin/sh", "-c", command], cwd=cwd, env=env,
                            stdout=output, stderr=subprocess.STDOUT)
(RECEIPT / record["exit_file"]).write_text(str(result.returncode) + "\n")
record.update({"exit_code": result.returncode, "finished_at": datetime.now(timezone.utc).isoformat(),
    "supervisor_sha256_after": sha(cwd / "tools/new1_supervisor.py"),
    "tests_sha256_after": sha(cwd / "tests/test_new1_supervisor.py"),
    "log_sha256": sha(RECEIPT / record["log"]),
    "fixture_roots_sha256": sha(Path(env["NEW1_RECEIPT_TMPLOG"]))})
evidence["worktree_scope_after_" + phase] = snapshot()
evidence["worktree_scope_unchanged_after_" + phase] = (
    evidence["worktree_scope_before"] == evidence["worktree_scope_after_" + phase])
evidence["status"] = phase.upper() + "_CAPTURED"
save(evidence)
if not evidence["worktree_scope_unchanged_after_" + phase]:
    raise SystemExit("STOPPED: worktree tools/tests file bytes changed")
print(json.dumps({"phase": phase, "cwd": str(cwd), "exit_code": result.returncode,
    "supervisor_sha256": record["supervisor_sha256"], "tests_sha256": record["tests_sha256"],
    "worktree_scope_unchanged": True}))
