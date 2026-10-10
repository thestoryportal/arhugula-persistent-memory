"""Record the exact bounded fixture command and all project/fixture source bytes."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

directory, cwd, mode = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
pure = sys.argv[4:] == ["--pure"]
if mode not in ("red", "green") or sys.argv[4:] not in ([], ["--pure"]):
    raise SystemExit("expected RUN_DIR CWD red|green [--pure]")
argv = [sys.executable, "-B", str(cwd/"tests/test_new1_dispatch.py")]
if pure: argv.append("PureTests")
argv.append("-v")
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LLMDB_ROOT=str(cwd),
                   NEW1_TEST_PROVENANCE=str(directory/"fixtures"))
paths = [cwd/"tests/test_new1_dispatch.py", cwd/"tools/c10w_p2_gate.py", cwd/"tools/mathlab_events.py",
         cwd/"tools/new1_dispatch.sh", cwd/"tools/new1_dispatch_report.py", Path(__file__)]
runner = Path(__file__).parent/"run_tests.sh"
if runner.exists(): paths.append(runner)
sources = []
snapshot = directory/"source_snapshot"
snapshot.mkdir()
for index, path in enumerate(paths):
    if not path.exists(): continue
    saved = snapshot/(str(index)+"_"+path.name)
    shutil.copyfile(path, saved)
    sources.append({"path":str(path), "sha256":hashlib.sha256(path.read_bytes()).hexdigest(), "preserved_as":str(saved)})
metadata = {"command":argv, "cwd":str(cwd), "interpreter":sys.executable,
            "interpreter_sha256":hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
            "uid":os.getuid(), "own_niceness":int(os.environ["NEW1_TEST_NICE"]) if "NEW1_TEST_NICE" in os.environ else None,
            "mode":mode, "subset":"PureTests" if pure else "full fixture suite",
            "sources":sources, "standard_library":"provided by pinned interpreter; no third-party imports",
            "environment_assignments": {key:environment[key] for key in ("PYTHONDONTWRITEBYTECODE", "LLMDB_ROOT", "NEW1_TEST_PROVENANCE")}}
(directory/"command.json").write_text(json.dumps(metadata, indent=2)+"\n")
with (directory/"test.log").open("xb") as log:
    result = subprocess.run(argv, cwd=cwd, env=environment, stdout=log, stderr=subprocess.STDOUT)
(directory/"exit_code.txt").write_text(str(result.returncode)+"\n")
for path in sorted((directory/"fixtures").glob("*/sources.json")):
    metadata["sources"].extend(json.loads(path.read_text()))
metadata["exit_code"] = result.returncode
(directory/"command.json").write_text(json.dumps(metadata, indent=2)+"\n")
sys.exit(result.returncode)
