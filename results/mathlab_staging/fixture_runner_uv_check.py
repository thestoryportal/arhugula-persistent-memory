"""Fixture-only exact UV attempt through the real CPU runner; no harvest dispatch.

Admission and process sampling are test stubs. This does not establish live
admission, niceness, memory-watchdog acceptance, or successful frozen execution.
"""
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

W = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(W))
from tools import mathlab_runtime as R
from tools import mathlab_admit as A
from tools import mathlab_cpu_runner as C

step = int(sys.argv[1])
assert step in (2, 3)
paths = R.read_json(W / "results/mathlab_staging/fixture_paths.json")
previous = R.read_json(W / "results/mathlab_staging/headless_attempts.json")
parent = Path(paths["parent"])
run = R.Run(R.new_directory(parent, f"runner_uv_m{step}"), step,
            "Fixture-only exact UV attempt; admission and sampling are stubbed", 2700 if step == 2 else 1800)
run.event("admission", allowed=True, reasons=[])
R.write_new(run.directory / "admission.json", dict(tier=R.TIER, fixture=True, allowed=True, kind="cpu"))
arguments = ["runner", str(W / ("mathlab/m2_solve_repro.py" if step == 2 else "mathlab/m3_calibration.py")),
             "2700" if step == 2 else "1800", "--run-dir", str(run.directory),
             "--harvest-dir", paths["harvest"], "--output-root", str(parent / "runner_uv_outputs")]
if step == 3:
    arguments += ["--reproduction-dir", previous["prepared_m2"], "--index-path", str(parent / "runner_fixture.duckdb")]

def fixture_wait(process, run_dir):
    process.wait(timeout=30)
    return "PASS" if process.returncode == 0 else "INVALID"

real_halt = R.stage_halt
def fixture_halt(root, *args, **kwargs):
    return real_halt(parent, *args, **kwargs)

with patch.dict(os.environ, {"UV_CACHE_DIR": "/private/tmp/mathlab_uv_cache", "UV_PYTHON": str(W / ".venv/bin/python")}), \
     patch.object(sys, "argv", arguments), patch.object(A, "dispatch_check", return_value={"allowed": True, "fixture": True}), \
     patch.object(C, "watch", side_effect=fixture_wait), patch.object(R, "stage_halt", side_effect=fixture_halt):
    code = C.main()
from tools.mathlab_events import read_events
events, errors = read_events(run.directory / "events.jsonl")
assert not errors and events[-1]["type"] == "run_finished"
record = dict(fixture=True, step=step, runner_exit_code=code, run_dir=str(run.directory),
              final_event=events[-1], stubs=["dispatch_check", "watch process sampling", "diagnostic root"])
R.write_new(run.directory / "fixture_attempt.json", record)
print(json.dumps(record, indent=2))
raise SystemExit(code)
