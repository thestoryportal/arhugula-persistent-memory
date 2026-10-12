#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROGRAM_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd -P)"
DEST=/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2loc
if [ "$#" -gt 1 ]; then echo "usage: run_replay.sh [DEST]" >&2; exit 2; fi
if [ "$#" -eq 1 ]; then DEST="$1"; fi
export PYTHONDONTWRITEBYTECODE=1
exec "$PROGRAM_ROOT/.venv/bin/python" -B - "$SCRIPT_DIR" "$DEST" <<'PY'
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

sys.path.insert(0, sys.argv[1])
from read_replay import (BASE_COMMIT, CONTEXT_SHA, PROGRAM_ROOT, ProcessMonitor, fidelity_manifest, inspect_replay,
                         load_json, pinned_constants, process_check, require, sha_file)
from tokenizer_precheck import validate_precheck

try:
    dest = Path(sys.argv[2]).resolve(strict=True)
    interpreter = PROGRAM_ROOT / ".venv/bin/python"
    reader = Path(sys.argv[1]) / "read_replay.py"
    require(dest != PROGRAM_ROOT and (dest / ".git").is_dir(), "standalone destination required")
    for name in ("replay_launch.json", "runner_receipt.json", "run.log", "run.rc", "run.pid", "process_exclusion.jsonl", "fingerprint.log", "preflight.log", "reader.log"):
        require(not (dest / name).exists(), f"destination was already dispatched: {name}")
    require(not (dest / "runs").exists(), "destination already contains run outputs")
    launch_path = dest / "replay_launch.json"
except (OSError, ValueError) as exc:
    print(f"INVALID/HALT: prelaunch refusal: {exc}", file=sys.stderr)
    sys.exit(2)
invocation = uuid.uuid4().hex
receipt = {"invocation_id": invocation, "dest": str(dest), "runner_pid": os.getpid(),
           "base_commit": BASE_COMMIT, "child_exit": None, "child_pid": None, "owned_children": [],
           "failures": [], "exclusive_window": os.environ.get("REPLAY_EXCLUSIVE_WINDOW"), "launch": {}}
child, run_dir, score_path, rc = None, None, None, 2
process_log = dest / "process_exclusion.jsonl"
monitor, predispatch_events, reserved_paths = ProcessMonitor(), [], []


def write_json(path, value):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def exclude(phase):
    try:
        event = process_check(phase, None if child is None else child.pid, receipt["owned_children"])
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        if child is None:
            raise
        event = {"phase": phase, "probe_exit": -1, "probe_error": str(exc),
                 "runner_pid": os.getpid(), "child_pid": child.pid, "foreign": [], "ok": False}
        print(f"PROCESS PROBE RETRY: {exc}", file=sys.stderr, flush=True)
    was_invalid = monitor.invalid
    event.update(monitor.observe(event))
    for entry in event.get("owned_children", []):
        if entry not in receipt["owned_children"]:
            receipt["owned_children"].append(entry)
    if child is None:
        require(event["ok"], "GPU contenders must be closed (loop/model servers): " + json.dumps(event["foreign"]))
        predispatch_events.append(event)
    else:
        with process_log.open("a") as stream:
            stream.write(json.dumps(event, allow_nan=False) + "\n")
        if monitor.invalid and not was_invalid:
            print("PROCESS WINDOW INVALID: three consecutive contender/probe observations; editor continues, reader will reject", flush=True)
    return event


def stop_owned():
    if child is None:
        return
    pids = {child.pid} | {row["pid"] for row in receipt["owned_children"]}
    def live_owned():
        active = []
        for pid in pids:
            try:
                group = os.getpgid(pid)
            except ProcessLookupError:
                continue
            require(group == child.pid, "refuse to signal a PID outside the runner-created process group")
            active.append(pid)
        return active
    if not live_owned():
        return
    try:
        os.killpg(child.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + 5
    while live_owned() and time.monotonic() < deadline:
        child.poll()
        time.sleep(0.1)
    if live_owned():
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass  # The verified owned group finished between the probe and signal.
    try:
        child.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGKILL)
        child.wait(timeout=5)


def interrupted(signum, frame):
    raise RuntimeError(f"runner received signal {signum}")


signal.signal(signal.SIGTERM, interrupted)
signal.signal(signal.SIGINT, interrupted)
try:
    require(receipt["exclusive_window"] == "paused-no-relaunch", "set REPLAY_EXCLUSIVE_WINDOW=paused-no-relaunch only for the operator's reserved whole edit/scorer window")
    constants = pinned_constants(dest)
    refused = list(constants["_REFUSED_ENV"]) + ["PYTHONPATH", "PYTHONHOME", "HF_HUB_CACHE", "HUGGINGFACE_HUB_CACHE", "TRANSFORMERS_CACHE", "PYTORCH_TRANSFORMERS_CACHE", "PYTORCH_PRETRAINED_BERT_CACHE"]
    require(not any(key in os.environ for key in refused), "inherited model/runtime setting: " + ",".join(key for key in refused if key in os.environ))
    require(os.environ.get("LLMDB_DEVICE", "mps") == "mps", "location control requires the pinned MPS device")
    require((dest / ".venv").resolve(strict=True) == (PROGRAM_ROOT / ".venv").resolve(strict=True), "wrong replay runtime symlink")
    audit = inspect_replay(dest)
    require(load_json(dest / "replay_setup.json") == audit and sha_file(dest / "replay_diff.txt") == audit["diff_sha256"], "setup audit/diff no longer matches frozen source")
    receipt.update({key: audit[key] for key in ("edit_py_sha256", "diff_sha256")})
    receipt["tokenizer_precheck"] = validate_precheck(dest, audit=audit)
    env = {**os.environ, "LLMDB_ROOT": str(PROGRAM_ROOT), "PYTHONDONTWRITEBYTECODE": "1"}
    exclude("before_dispatch")
    fp = subprocess.run([str(interpreter), "-B", str(PROGRAM_ROOT / "tools/engine_fingerprint.py")], cwd=dest, env=env, capture_output=True, text=True, timeout=60)
    receipt["engine_fingerprint"] = {"exit": fp.returncode, "stdout": fp.stdout, "stderr": fp.stderr,
                                     "LLMDB_ROOT": str(PROGRAM_ROOT), "interpreter": str(interpreter)}
    print(fp.stdout, end="", flush=True)
    require(fp.returncode == 0 and bool(fp.stdout.strip()), "engine fingerprint failed or returned empty output")
    receipt["fidelity_before"] = fidelity_manifest(dest)
    # A long cache hash pass cannot replace the immediate pre-model process check.
    exclude("before_dispatch")
    mps = subprocess.run([str(interpreter), "-B", "-c", 'import torch; ok = bool(torch.backends.mps.is_available()); print("MPS_AVAILABLE=" + str(ok).lower()); raise SystemExit(0 if ok else 2)'], cwd=dest, env=env, capture_output=True, text=True, timeout=60)
    receipt["mps_preflight"] = {"exit": mps.returncode, "stdout": mps.stdout, "stderr": mps.stderr}
    require(mps.returncode == 0 and mps.stdout.strip() == "MPS_AVAILABLE=true", "MPS unavailable or unexpected preflight output")
    exclude("after_preflight")
    require(not (dest / "runs").exists() and inspect_replay(dest) == audit, "source or fresh-run state changed after preflight")
    dispatched_at = time.time()
    receipt["tokenizer_precheck"] = validate_precheck(dest, at_time=dispatched_at, audit=audit)
    launch = {key: audit[key] for key in ("base_commit", "dest", "edit_py_sha256", "diff_sha256")}
    launch.update(invocation_id=invocation, program_root=str(PROGRAM_ROOT), context_sha256=CONTEXT_SHA,
                  initial_runs=[], runner_pid=os.getpid(), child_pid=None, fidelity_before=receipt["fidelity_before"],
                  dispatched_at=dispatched_at, tokenizer_precheck_sha256=sha_file(dest / "tokenizer_precheck.json"))
    # Reserve only at dispatch; Popen failure removes only this invocation's files.
    with launch_path.open("x") as stream:
        reserved_paths.append(launch_path)
        stream.write(json.dumps(launch, indent=2, allow_nan=False) + "\n")
    env.update(REPLAY_INVOCATION_ID=invocation, REPLAY_LAUNCH_PATH=str(launch_path))
    with (dest / "run.log").open("x") as log:
        reserved_paths.append(dest / "run.log")
        child = subprocess.Popen([str(dest / ".venv/bin/python"), "-B", "edit.py"], cwd=dest, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        launch["child_pid"] = receipt["child_pid"] = child.pid
        receipt["launch"] = launch
        write_json(launch_path, launch)
        (dest / "run.pid").write_text(str(child.pid) + "\n")
        (dest / "fingerprint.log").write_text(fp.stdout + fp.stderr)
        (dest / "preflight.log").write_text(mps.stdout + mps.stderr)
        with process_log.open("x") as stream:
            for event in predispatch_events:
                stream.write(json.dumps(event, allow_nan=False) + "\n")
        print(f"invocation_id: {invocation}\neditor_pid: {child.pid}", flush=True)
        deadline = time.monotonic() + 7200
        while True:
            exclude("during_run")
            if child.poll() is not None:
                break
            require(time.monotonic() < deadline, "whole-run timeout (7200s)")
            time.sleep(1)
    receipt["child_exit"] = child.wait()
    for attempt in range(3):
        event = exclude("after_exit")
        if event["probe_exit"] == 0:
            break
        if attempt < 2:
            time.sleep(1)
    require(receipt["child_exit"] == 0, f"editor/scorer failed: exit {receipt['child_exit']}")
    require(inspect_replay(dest) == audit, "source/diff changed during execution")
    receipt["fidelity_after"] = fidelity_manifest(dest)
    require(receipt["fidelity_after"] == receipt["fidelity_before"], "runtime/config/model/cache inputs changed during execution")
except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as exc:
    receipt["failures"].append(str(exc))
    print(f"INVALID/HALT: {exc}", file=sys.stderr, flush=True)
    if child is not None:
        stop_owned()
finally:
    if child is None:
        for path in reversed(reserved_paths):
            path.unlink()
        print("REFUSED: no editor dispatched; destination remains reusable", file=sys.stderr)
        sys.exit(2)
    receipt["child_exit"] = child.wait()
    pid_path = dest / "run.pid"
    if pid_path.exists():
        require(pid_path.read_text().strip() == str(child.pid), "run.pid ownership mismatch")
        pid_path.unlink()
    scores = sorted(dest.glob("runs/*/score.json"))
    dirs = sorted((dest / "runs").iterdir()) if (dest / "runs").is_dir() else []
    if len(scores) == 1 and len(dirs) == 1 and dirs[0].is_dir() and scores[0].parent == dirs[0]:
        score_path, run_dir = scores[0].resolve(), dirs[0].resolve()
        receipt.update(run_dir=str(run_dir), score_path=str(score_path), score_sha256=sha_file(score_path))
        try:
            receipt["saved_sha256"] = load_json(score_path)["saved_sha256"]
        except (OSError, ValueError, KeyError, TypeError) as exc:
            receipt["failures"].append("score receipt parse: " + str(exc))
    elif scores:
        receipt["failures"].append(f"expected exactly one run/score; directories={len(dirs)} scores={len(scores)}")
    else:
        receipt["failures"].append("NO SCORE: editor/scorer did not produce score.json")
    if process_log.is_file():
        receipt["process_log_sha256"] = sha_file(process_log)
    receipt_path = dest / "runner_receipt.json"
    write_json(receipt_path, receipt)
    if score_path is not None:
        print(f"score_path: {score_path}", flush=True)
        with (dest / "reader.log").open("x") as reader_log:
            read = subprocess.run([str(interpreter), "-B", str(reader), str(score_path), str(receipt_path)], cwd=dest, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, stdout=reader_log, stderr=subprocess.STDOUT)
        receipt["reader_exit"] = rc = read.returncode
        print((dest / "reader.log").read_text(), end="", flush=True)
    else:
        # No exact score exists to pass to the reader. This transport code is distinct from INVALID (2).
        receipt["reader_exit"] = None
        rc = 3 if not scores else 2
    receipt["runner_exit"] = rc
    write_json(receipt_path, receipt)
    (dest / "run.rc").write_text(str(rc) + "\n")
sys.exit(rc)
PY
