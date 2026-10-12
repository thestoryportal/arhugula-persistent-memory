#!/usr/bin/env python3
"""D-ML-1 CPU-only process watchdog. Admission occurs in the shell first."""
import argparse
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

W = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(W / "code"))
from apps.mathlab import mathlab_runtime as R


def validate_notebook(notebook, deadline_s):
    expected = {W / "code/apps/mathlab/m2_solve_repro.py": (2, 6540), W / "code/apps/mathlab/m3_calibration.py": (3, 1800)}
    notebook = Path(notebook).resolve()
    R.require(notebook in expected, "DEADLINE", "only the two frozen CPU notebooks may run")
    step, cap = expected[notebook]
    R.require(deadline_s == cap, "DEADLINE", f"step {step} hard deadline is {cap} s")
    return step


def terminate(process):
    if process.poll() is not None: return
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()


def watch(process, run_dir, sample=R.available_gib, sleep=time.sleep, sink=R.emit):
    samplers = {}
    while process.poll() is None:
        available = sample()
        sink(run_dir, "gate_result", gate_id="memory-watchdog", plain_words="Available memory stays above the six GiB emergency floor",
             observed=available, bar=6., comparison=">=", passed=available >= 6)
        if available < 6:
            terminate(process)
            return "STOPPED-RESOURCE"
        import psutil
        try:
            parent = psutil.Process(process.pid)
            family = [parent, *parent.children(recursive=True)]
            rss = sum(p.memory_info().rss for p in family) / 2 ** 30
            samplers = {p.pid: samplers.get(p.pid, p) for p in family}
            cpu = sum(p.cpu_percent() for p in samplers.values())
        except psutil.NoSuchProcess:
            if process.poll() is not None: break
            raise R.Halt("RESOURCE-PROBE", "process family changed during resource inventory")
        sink(run_dir, "resource_sample", avail_gib=available, floor_gib=6., rss_gib=rss, cpu_pct=cpu)
        sleep(5)
    return "STOPPED-DEADLINE" if process.returncode in (124, 137) else "PASS" if process.returncode == 0 else "INVALID"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path); parser.add_argument("deadline_s", type=int)
    parser.add_argument("--run-dir", type=Path, required=True)
    args, notebook_args = parser.parse_known_args()
    step = validate_notebook(args.notebook, args.deadline_s)
    from apps.mathlab.mathlab_admit import dispatch_check
    command = ["nice", "-n", "10", "/opt/homebrew/bin/timeout", "-k", "30", str(args.deadline_s),
               "uv", "run", "--script", str(args.notebook.resolve()), *notebook_args]
    env = dict(os.environ, LLMDB_ROOT=str(W), LLMDB_DEVICE="cpu", CUDA_VISIBLE_DEVICES="",
               OMP_NUM_THREADS="8", MKL_NUM_THREADS="8", PYTHONDONTWRITEBYTECODE="1", MATHLAB_RUN_DIR=str(args.run_dir))
    process = None
    try:
        R.verify_prereg(W)
        dispatch_check(args.run_dir, "cpu")
        R.enforce_stop_policy(W, step, exclude=args.run_dir)
        process = subprocess.Popen(command, cwd=W, env=env, start_new_session=True)
        outcome = watch(process, args.run_dir)
        if outcome.startswith("STOPPED-"):
            number = R.prior_aborts(W, step) + 1
            R.stage_halt(W, args.run_dir, outcome, f"resource/deadline abort {number}; " +
                         ("operator review required" if number >= 3 else "not a lab stop"), step=step)
        else:
            from apps.mathlab.mathlab_events import read_events
            events, errors = read_events(args.run_dir / "events.jsonl")
            R.require(not errors, "EVENTS", "; ".join(errors))
            completions = [e for e in events if e["type"] == "run_finished"]
            R.require(len(completions) <= 1, "EVENTS", "notebook emitted multiple closeouts")
            if not completions or outcome == "INVALID" and completions[-1]["outcome"] == "PASS":
                R.stage_halt(W, args.run_dir, "CPU-EXECUTION", f"notebook exited {process.returncode} without a successful event closeout", step=step)
                return 3
            return 0 if outcome == "PASS" and completions[-1]["outcome"] == "PASS" else 3
        return 0 if outcome == "PASS" else 3
    except BaseException as error:
        if process is not None: terminate(process)
        R.stage_halt(W, args.run_dir, error.code if isinstance(error, R.Halt) else "RESOURCE-PROBE",
                     str(error), step=step)
        raise


if __name__ == "__main__":
    sys.exit(main())
