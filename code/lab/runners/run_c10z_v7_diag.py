#!/usr/bin/env python3
"""Model-free exclusivity launcher for the reviewed V7-DIAG probe."""
import time
import signal
import os
import sys
import math
LAUNCH_STARTED = time.monotonic()
CAP_SECONDS = 3060
if __name__ == "__main__" and "--worker" in sys.argv:
    origin = float(os.environ["C10Z_V7_LAUNCH_STARTED"])
    if not math.isfinite(origin) or origin < 0 or origin > LAUNCH_STARTED:
        raise ValueError("invalid supervisor deadline origin")
    LAUNCH_STARTED = origin
    remaining = LAUNCH_STARTED + CAP_SECONDS - time.monotonic()
    if remaining <= 0: raise TimeoutError("fixed deadline expired before worker imports")
    signal.signal(signal.SIGALRM, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGALRM})
    signal.setitimer(signal.ITIMER_REAL, remaining)

import argparse
import importlib.util
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import re
import runpy
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]


def gate_module():
    spec = importlib.util.spec_from_file_location("c10z_v7_gpu_gate", ROOT / "code/lab/runners/c10w_p2_gate.py")
    gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
    return gate


def namespace(utc):
    if not re.fullmatch(r"\d{8}T\d{6}(?:\.\d{6})?Z", utc): raise ValueError("invalid UTC namespace")
    parent = ROOT / "experiments/c10z/runs/c10z_v7_diagnostic"
    if parent.resolve() != parent: raise ValueError("namespace symlink refused")
    return parent / utc


def write_record(path, value, replace=False):
    data = json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"
    target = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp") if replace else path
    with target.open("x") as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    if replace: os.replace(target, path)


def supervised_gpu_check(gate, utc):
    token = os.environ.get("C10Z_V7_SUPERVISOR_TOKEN")
    if not token: return gate.check_gpu()
    lease = json.loads((namespace(utc) / "supervisor.json").read_text())
    origin = float(os.environ["C10Z_V7_LAUNCH_STARTED"])
    argv = lease["supervisor_argv"]
    if not (token == lease["token"] and lease["pid"] == os.getppid() and lease["deadline_origin"] == origin and
            math.isfinite(origin) and 0 <= origin <= time.monotonic() and lease["cap_seconds"] == CAP_SECONDS and
            lease["source_sha256"] == hashlib.sha256(Path(__file__).read_bytes()).hexdigest() and
            argv[1:] == ["-B", str(Path(__file__).resolve()), "--utc", utc]):
        raise ValueError("unverified model-free supervisor ownership")
    result = gate.check_gpu()
    if "blocking_processes" not in result or "blocking_tmux" not in result: return result
    kept = []; excluded = []
    for line in result["blocking_processes"]:
        pid, _, command = line.partition(" "); actual = command.split()
        if (pid == str(lease["pid"]) and actual and actual[1:] == argv[1:] and
                Path(actual[0]).resolve() == Path(argv[0]).resolve()): excluded.append(line)
        else: kept.append(line)
    return {**result, "ok": not kept and not result["blocking_tmux"], "blocking_processes": kept,
            "verified_model_free_supervisor": excluded}


def worker(utc):
    namespace(utc)
    gate = gate_module()
    fingerprint = gate.check_fingerprint()
    if not fingerprint["ok"]: raise ValueError("fingerprint refused: " + json.dumps(fingerprint))
    gpu = supervised_gpu_check(gate, utc)
    if not gpu["ok"]: raise ValueError("gpu exclusivity refused: " + json.dumps(gpu))
    path = ROOT / "code/lab/track_c/c10z_v7_diag.py"
    sys.path.insert(0, str(path.parent))
    sys.argv = [str(path), "--utc", utc]
    runpy.run_path(str(path), run_name="__main__")


def halt_diagnostic(out, returncode, reason, timed_out=False, observed=False):
    records = {}; errors = {}
    for name in ("progress.json", "verdict.json", "worker_result.json"):
        path = out / name
        if path.exists():
            try: records[name] = json.loads(path.read_text())
            except (OSError, ValueError) as exc: errors[name] = type(exc).__name__ + ": " + str(exc)
    progress = records.get("progress.json", records.get("verdict.json", {}))
    value = {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "completion": "incomplete",
             "reason": reason, "worker_returncode": returncode, "timed_out": timed_out,
             "supervisor_observed_exit": observed, "cap_seconds": CAP_SECONDS, "deadline_origin": LAUNCH_STARTED,
             "active_phase": progress.get("active_phase", "preflight_or_import"),
             "incomplete_phases": progress.get("incomplete_phases", ["setup", "F1000", "R1000", "R5000", "integrity", "cleanup", "worker_exit"]),
             "completed_phases": progress.get("completed_phases", []), "records": records, "record_read_errors": errors,
             "retained_artifacts": {str(p.relative_to(out)): {"bytes": p.stat().st_size}
                                    for p in sorted(out.rglob("*")) if p.is_file()},
             "retention_scope": "file presence and size; partial files are not admitted"}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    path = out / ("halt_diagnostic_" + stamp + ".json")
    write_record(path, value)
    previous = records.get("verdict.json", {})
    write_record(out / "verdict.json", {**previous, "outcome": "INCONCLUSIVE", "completion": "incomplete",
        "reason": reason, "halt_diagnostic": path.name, "worker_returncode": returncode,
        "supervisor_observed_exit": observed}, replace=(out / "verdict.json").exists())
    print(json.dumps({"outcome": "INCONCLUSIVE", "reason": reason, "halt_diagnostic": str(path)}), flush=True)
    return 2


def launch(utc):
    out = namespace(utc)
    if out.exists(): raise ValueError("namespace already exists")
    out.parent.mkdir(parents=True, exist_ok=True); out.mkdir()
    token = uuid.uuid4().hex
    write_record(out / "supervisor.json", {"token": token, "pid": os.getpid(), "deadline_origin": LAUNCH_STARTED,
                                          "cap_seconds": CAP_SECONDS, "namespace": str(out),
                                          "supervisor_argv": sys.orig_argv,
                                          "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    py = str(ROOT / ".venv/bin/python")
    env = dict(os.environ, LLMDB_ROOT=str(ROOT), HF_HOME=str((ROOT / "data/hf_cache").resolve()), HF_DATASETS_OFFLINE="1",
               C10Z_V7_LAUNCH_STARTED=str(LAUNCH_STARTED), C10Z_V7_SUPERVISOR_TOKEN=token)
    child = None
    try:
        remaining = LAUNCH_STARTED + CAP_SECONDS - time.monotonic()
        if remaining <= 0: raise TimeoutError("fixed deadline expired before worker start")
        with (out / "worker.log").open("x") as log:
            child = subprocess.Popen([py, "-B", str(Path(__file__).resolve()), "--worker", "--utc", utc],
                                     env=env, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
            returncode = child.wait(timeout=max(0., LAUNCH_STARTED + CAP_SECONDS - time.monotonic()))
            log.flush(); os.fsync(log.fileno())
        observed = time.monotonic()
        if observed >= LAUNCH_STARTED + CAP_SECONDS:
            return halt_diagnostic(out, returncode, "fixed 3060-second deadline exceeded before observed worker exit", True, True)
        if returncode != 0:
            return halt_diagnostic(out, returncode, "abnormal worker exit: " + str(returncode), observed=True)
        receipt = json.loads((out / "worker_result.json").read_text())
        if not (receipt.get("cleanup_completed") is True and receipt.get("completion") == "awaiting_worker_exit" and
                receipt.get("deadline_origin") == LAUNCH_STARTED and receipt.get("cap_seconds") == CAP_SECONDS and
                receipt.get("outcome") in ("A1", "A2", "D")):
            raise ValueError("worker exit lacks a valid post-cleanup receipt")
        progress = json.loads((out / "progress.json").read_text())
        progress["completed_phases"].append("worker_exit")
        progress["incomplete_phases"] = [p for p in progress["incomplete_phases"] if p != "worker_exit"]
        progress["active_phase"] = "complete"
        write_record(out / "progress.json", progress, replace=True)
        result = {**receipt, "completion": "complete", "worker_exit_pending": False,
                  "supervisor_observed_exit": True, "worker_returncode": 0, "worker_exited_monotonic": observed}
        if time.monotonic() >= LAUNCH_STARTED + CAP_SECONDS: raise TimeoutError("deadline expired before success publication")
        write_record(out / "verdict.json", result, replace=True)
        if time.monotonic() >= LAUNCH_STARTED + CAP_SECONDS: raise TimeoutError("deadline expired during success publication")
        print(json.dumps(result, allow_nan=False), flush=True)
        return 0
    except (subprocess.TimeoutExpired, TimeoutError) as exc:
        if child is not None and child.poll() is None: child.kill(); child.wait()
        return halt_diagnostic(out, None if child is None else child.returncode, type(exc).__name__ + ": " + str(exc), True, child is not None)
    except Exception as exc:
        if child is not None and child.poll() is None: child.kill(); child.wait()
        return halt_diagnostic(out, None if child is None else child.returncode, type(exc).__name__ + ": " + str(exc), observed=child is not None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--utc", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.worker: worker(args.utc); return 0
        return launch(args.utc)
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "REFUSED", "reason": str(exc)}), file=sys.stderr)
        return 3
if __name__ == "__main__": sys.exit(main())
