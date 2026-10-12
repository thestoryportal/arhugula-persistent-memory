#!/usr/bin/env python3
"""Post-exit NEW1 receipt; stdlib only. Never starts or signals compute.

Terminal authority: mathlab_events.py:56-58,278-303; supervisor.py:592-627.
Abort history: new1_supervisor.py:168-190. Main's stdout/exit:632-651.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import types
import os

ABORTS = ("STOPPED-RESOURCE", "STOPPED-DEADLINE")


def classify(events, errors, stdout, stderr, exit_status):
    """Pure reconciliation; artifacts never substitute for terminal publication."""
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    code = lines[-1] if lines and re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*", lines[-1]) else None
    terminal = None
    for event in events:
        if event["type"] == "run_finishing": terminal = None
        elif event["type"] in ("run_finished", "halted"): terminal = event
    halt_aborts = [event["reason"].split(":", 1)[0] for event in events
                   if event["type"] == "halted" and event["reason"].split(":", 1)[0] in ABORTS]
    evidence = sorted(set(halt_aborts + [reason for reason in ABORTS
                          if reason == code or re.search(r"\b"+reason+r"\b", stderr)]))
    expected = None
    if terminal is not None:
        expected = terminal["outcome"] if terminal["type"] == "run_finished" else terminal["reason"].split(":", 1)[0]
    starts = [event for event in events if event["type"] == "run_started"]
    identity = len(starts) == 1 and starts[0]["step"] == 4 and starts[0]["title"].startswith("NEW1 ") and starts[0].get("purpose") == "experiment"
    agreement = (identity and not errors and expected is not None and code == expected
                 and type(exit_status) is int and exit_status == (0 if code == "PASS" else 3)
                 and not (code == "PASS" and evidence))
    return {"stdout_code": code, "terminal_event": terminal, "terminal_event_found": terminal is not None,
            "exit_status": exit_status, "event_errors": errors, "verdict_status": "COMPLETE" if agreement else "INCOMPLETE",
            "prediction_verdict": "terminal PASS; individual predictions remain in events.jsonl" if agreement and code == "PASS" else "no prediction verdict",
            "counts_as_abort": bool(evidence), "abort_reasons": evidence}


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError("duplicate JSON key: "+key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonfinite JSON constant: "+value)


def read_json(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object, parse_constant=reject_constant)
    if not isinstance(data, dict): raise ValueError(str(path)+": JSON object required")
    return data


def event_reader(root):
    # Compile current source bytes; do not trust an older .pyc or another cwd.
    path = root/"tools/mathlab_events.py"
    module = types.ModuleType("new1_receipt_events")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module.read_events


def prior_aborts(root, dispatch, excluded, read_events):
    """Union by namespace, so a halted stream plus its receipt counts once."""
    counted, errors, sources = set(), [], []
    runs = root/"results/mathlab_staging/runs"
    for directory in sorted(runs.glob("new1_*")):
        key = str(directory.resolve())
        if key in excluded: continue
        if directory.is_symlink() or not directory.is_dir():
            errors.append(str(directory)+": invalid history namespace")
            continue
        rows, failures = read_events(directory/"events.jsonl")
        starts = [row for row in rows if row["type"] == "run_started"]
        if failures or len(starts) != 1 or starts[0]["step"] != 4 or not starts[0]["title"].startswith("NEW1 ") or starts[0].get("purpose") != "experiment":
            errors.extend(failures or [str(directory)+": invalid NEW1 run identity"])
        # The scanner's exact counting rule is any qualifying halted per namespace.
        if any(row["type"] == "halted" and row["reason"].split(":", 1)[0] in ABORTS for row in rows):
            counted.add(key)
            sources.append({"source": str(directory/"events.jsonl"), "identity": key})
    for receipt_path in sorted((root/"results/mathlab_staging").glob("new1_dispatch_*/dispatch_receipt.json")):
        if receipt_path.parent.resolve() == dispatch.resolve(): continue
        try:
            previous = read_json(receipt_path)
            if previous.get("authorization_consumed") is not True: continue
            abort = previous["abort_accounting"]["counts_as_abort"]
            if type(abort) is not bool: raise ValueError("boolean counts_as_abort required")
            if not abort: continue
            namespace = previous["namespace"].get("path")
            if namespace is not None:
                namespace = Path(namespace)
                if not namespace.is_absolute(): namespace = root/namespace
                key = str(namespace.resolve())
                if namespace.parent.resolve() != runs.resolve() or not namespace.name.startswith("new1_"):
                    raise ValueError("receipt namespace outside NEW1 runs")
            else:
                key = "dispatch:"+str(receipt_path.parent.resolve())
            if key not in excluded:
                counted.add(key)
                sources.append({"source": str(receipt_path), "identity": key})
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(str(receipt_path)+": "+str(error))
    return len(counted), errors, sources


def build_receipt(root, dispatch):
    root, dispatch = Path(root).resolve(), Path(dispatch).resolve()
    invocation_exists = (dispatch/"invocation.json").exists()
    invocation = read_json(dispatch/"invocation.json") if invocation_exists else None
    supervisor_exit = read_json(dispatch/"supervisor_exit.json")
    if supervisor_exit.get("exited") is not True:
        raise ValueError("reporter requires exited supervisor; no Python reporting while it is alive")
    namespace = read_json(dispatch/"namespace.json")
    worker = read_json(dispatch/"worker.json")
    supervisor = read_json(dispatch/"supervisor.json")
    disposition = read_json(dispatch/"disposition.json")
    read_events = event_reader(root)
    namespace_errors = []
    candidates = namespace.get("candidates", [])
    selected = namespace.get("path")
    if namespace.get("anomaly") or len(candidates) != 1 or selected != candidates[0]:
        namespace_errors.append("namespace anomaly: exactly one new namespace required")
    if selected:
        selected_path = Path(selected)
        if selected_path.parent.resolve() != (root/"results/mathlab_staging/runs").resolve() or not selected_path.name.startswith("new1_") or selected_path.is_symlink():
            namespace_errors.append("namespace identity is invalid")
        if not namespace_errors: rows, errors = read_events(selected_path/"events.jsonl")
        else: rows, errors = [], []
    else: rows, errors = [], []
    outcome = classify(rows, errors+namespace_errors, (dispatch/"supervisor_stdout.log").read_text(),
                       (dispatch/"supervisor_stderr.log").read_text(), supervisor_exit.get("status"))
    excluded = {str(Path(path).resolve()) for path in candidates}
    count, history_errors, history_sources = prior_aborts(root, dispatch, excluded, read_events)
    stop_path = dispatch/"stop.json"
    stop = read_json(stop_path) if stop_path.exists() else None
    observed_c1 = (worker.get("status") == "OBSERVED"
                   and type(worker.get("nice")) is int and worker["nice"] == 10
                   and type(supervisor.get("nice")) is int and supervisor["nice"] == 0
                   and type(worker.get("pid")) is int and worker["pid"] > 0
                   and worker.get("ppid") == supervisor.get("pid")
                   and worker.get("pgid") == worker["pid"]
                   and "tools/new1_geometry.py" in worker.get("command", ""))
    c1_failure = outcome["stdout_code"] == "PASS" and not observed_c1
    if history_errors or stop or not invocation_exists or c1_failure:
        outcome["verdict_status"] = "INCOMPLETE"
        outcome["prediction_verdict"] = "no prediction verdict"
    outcome["c1_observation_verified"] = observed_c1
    raw_processes = disposition.get("live_processes", [])
    processes = []
    for line in raw_processes:
        if isinstance(line, dict): processes.append(line); continue
        fields = line.strip().split(None, 4)
        if len(fields) != 5: raise ValueError("invalid disposition process row: "+line)
        processes.append(dict(zip(("pid", "ppid", "pgid", "nice"), map(int, fields[:4])), command=fields[4]))
    disposition["live_processes"] = processes
    blocked = disposition["status"] in ("UNREAPED", "UNAVAILABLE") or bool(processes) or c1_failure
    if processes: disposition["status"] = "UNREAPED"
    current_abort = invocation_exists and outcome["counts_as_abort"]
    total = count+int(current_abort)
    return {"recorded_at_utc": datetime.now(timezone.utc).isoformat(), "invocation": invocation,
            "authorization_consumed": invocation_exists, "supervisor": supervisor, "worker": worker,
            "supervisor_exit": supervisor_exit, "namespace": namespace, "disposition": disposition,
            "stop_reason": stop["reason"] if stop else None, "stop": stop,
            "outcome": outcome, "verdict_status": outcome["verdict_status"], "prediction_verdict": outcome["prediction_verdict"],
            "abort_accounting": {"counts_as_abort": current_abort, "reasons": outcome["abort_reasons"],
                                 "prior_aborts": count, "total_aborts": total, "third_abort_rule_reached": total >= 3,
                                 "accounting_complete": not history_errors, "history_errors": history_errors,
                                 "history_sources": history_sources},
            "subsequent_compute_blocked": blocked,
            "operator_message": "subsequent compute blocked until worker/group disposition is resolved" if blocked else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dispatch", type=Path)
    args = parser.parse_args()
    destination = args.dispatch/"dispatch_receipt.json"
    try:
        data = build_receipt(Path.cwd(), args.dispatch)
        with destination.open("x") as target:
            json.dump(data, target, indent=2, allow_nan=False)
            target.write("\n")
            target.flush()
            os.fsync(target.fileno())
        print(data["verdict_status"])
        return 3 if data["subsequent_compute_blocked"] else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("NEW1 receipt failed: "+str(error), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
