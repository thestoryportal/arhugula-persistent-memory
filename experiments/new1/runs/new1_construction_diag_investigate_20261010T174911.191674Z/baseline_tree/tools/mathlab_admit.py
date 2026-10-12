#!/usr/bin/env python3
"""D-ML-1 pre-import admission. Stdlib only; never imports a dispatcher."""
import argparse
import os
from pathlib import Path
import sys

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W))
from tools import mathlab_runtime as R
from tools.c10w_p2_gate import check_fingerprint, check_gpu


def status_reference(ref, root, tail=False):
    path = Path(ref["status_file"] if tail else ref["path"])
    if not path.is_absolute(): path = Path(root) / path
    R.require(R.sha_file(path) == ref["sha256"], "ADMISSION", "coordinator status hash changed")
    status = R.read_json(path)
    if tail:
        R.require(status.get("past_last_gated_stage") is True, "ADMISSION", "coordinator not past its last gated stage")
    else:
        value = status.get("status", "")
        R.require(value in ("PASS", "FAIL", "DONE", "HALTED", "INVALID", "COMPLETE", "STOPPED")
                  or isinstance(value, str) and value.startswith(("HALTED-", "STOPPED-")),
                  "ADMISSION", "coordinator status is not terminal")
    return {"path": str(path), "sha256": ref["sha256"], "status": status}


def decide(kind, *, admission, fingerprint, gpu, available_gib, root=W):
    reasons = []; checks = {"fingerprint": fingerprint, "gpu": gpu, "memory_gib": available_gib}
    if fingerprint.get("ok") is not True: reasons.append("Engine fingerprint refused")
    if not isinstance(available_gib, (int, float)) or not 8 <= available_gib < float("inf"):
        reasons.append("Free memory below eight GiB or invalid probe")
    try:
        R.require(kind in ("harvest", "cpu"), "ADMISSION", "unknown admission kind")
        R.require("reason" not in gpu, "ADMISSION", "GPU inventory probe error: " + str(gpu.get("reason")))
        R.require(isinstance(gpu.get("blocking_processes"), list) and isinstance(gpu.get("blocking_tmux"), list),
                  "ADMISSION", "GPU inventories were not both collected")
        R.require(not gpu["blocking_tmux"], "ADMISSION", "GPU autoresearch session is active")
        blockers = gpu["blocking_processes"]
        if kind == "harvest":
            R.require(gpu.get("ok") is True and not blockers, "ADMISSION", "GPU compute inventory is not clear")
            R.require(admission and admission.get("no_other_coordinator_live_or_pending") is True,
                      "ADMISSION", "lead queue statement missing")
            refs = admission.get("terminal_sources", [])
            R.require(len(refs) == 2 and {r["coordinator"] for r in refs} == {"c10x-rerun3", "astra-attempt3"},
                      "ADMISSION", "both queue coordinator status files are required")
            checks["queue"] = [status_reference(ref, root) for ref in refs]
        elif blockers:
            entries = (admission or {}).get("blocking_processes", [])
            R.require(len(entries) == len(blockers), "ADMISSION", "GPU blocking processes are unaccounted")
            expected = [(int(e["pid"]), e["command"]) for e in entries]
            actual = []
            for line in blockers:
                pid, _, command = line.partition(" ")
                actual.append((int(pid), command.strip()))
            R.require(len(set(expected)) == len(expected) and sorted(expected) == sorted(actual),
                      "ADMISSION", "GPU process pid/command does not match one-to-one")
            R.require(all(isinstance(e["coordinator"], str) and e["coordinator"].strip() for e in entries),
                      "ADMISSION", "coordinator identity missing")
            checks["coordinator_tail"] = [status_reference(e, root, tail=True) for e in entries]
        else:
            R.require(gpu.get("ok") is True, "ADMISSION", "GPU probe refused without a successful inventory")
    except (ValueError, TypeError, KeyError, OSError) as error:
        reasons.append(str(error))
    return dict(tier=R.TIER, kind=kind, allowed=not reasons, reasons=reasons, checks=checks)


def probe(kind, admission=None):
    R.verify_prereg(W)
    os.environ["LLMDB_ROOT"] = str(W)
    return decide(kind, admission=admission, fingerprint=check_fingerprint(), gpu=check_gpu(),
                  available_gib=R.available_gib(), root=W)


def dispatch_check(run_dir, kind, admission_path=None):
    """Bind the separate pre-import check to this shell exec and recheck its evidence."""
    from tools.mathlab_events import read_events
    run_dir = Path(run_dir); proof = R.read_json(run_dir / "admission.json")
    R.require(proof["allowed"] and proof["kind"] == kind and proof["launcher_pid"] == os.getpid(),
              "ADMISSION", "admission belongs to a different or refused shell launch")
    events, errors = read_events(run_dir / "events.jsonl")
    R.require(not errors and not any(e["type"] in ("stage_started", "run_finished") for e in events),
              "ADMISSION", "run already dispatched or event history is invalid")
    source = proof["lead_source"]
    if source is None:
        R.require(kind == "cpu" and admission_path is None, "ADMISSION", "lead queue evidence is required")
        lead = None
    else:
        path = Path(source["path"])
        R.require(R.sha_file(path) == source["sha256"] and
                  (admission_path is None or Path(admission_path).resolve() == path.resolve()),
                  "ADMISSION", "lead admission identity changed")
        lead = R.read_json(path)
    current = probe(kind, lead)
    R.emit(run_dir, "gate_result", gate_id="dispatch-admission", plain_words="Admission evidence remains valid immediately before dispatch",
           observed=current, bar="allowed", comparison="meets", passed=current["allowed"])
    R.require(current["allowed"], "ADMISSION", "; ".join(current["reasons"]))
    return current


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("cpu", "harvest"), required=True)
    parser.add_argument("--admission", type=Path)
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--step", type=int, choices=(1, 2, 3))
    parser.add_argument("--deadline-s", type=int, default=300)
    args = parser.parse_args()
    run_dir = args.run_dir or R.new_directory(W / "results/mathlab_staging/runs", "admission")
    own_run = args.run_dir is None
    run = R.Run(run_dir, args.step or (1 if args.kind == "harvest" else 2), "Check whether the lab can start", args.deadline_s,
                purpose="admission" if own_run else "experiment")
    try:
        result = probe(args.kind, R.read_json(args.admission) if args.admission else None)
        R.enforce_stop_policy(W, args.step or (1 if args.kind == "harvest" else 2), exclude=run_dir)
    except (OSError, ValueError, TypeError, KeyError) as error:
        result = dict(tier=R.TIER, kind=args.kind, allowed=False, reasons=[str(error)], checks={})
    result["launcher_pid"] = os.getppid()
    result["lead_source"] = ({"path": str(args.admission.resolve()), "sha256": R.sha_file(args.admission)}
                             if args.admission and args.admission.is_file() else None)
    R.emit(run_dir, "admission", allowed=result["allowed"], reasons=result["reasons"])
    R.emit(run_dir, "gate_result", gate_id="admission", plain_words="The launch is allowed by all admission checks",
           observed=result, bar="allowed", comparison="meets", passed=result["allowed"])
    for name, observed in result["checks"].items():
        passed = observed.get("ok") is True if isinstance(observed, dict) else bool(result["allowed"])
        if name == "memory_gib": passed = observed >= 8
        R.emit(run_dir, "gate_result", gate_id="admission-" + name, plain_words="Launch check: " + name.replace("_", " "),
               observed=observed, bar=8 if name == "memory_gib" else "allowed", comparison="meets", passed=passed)
    R.write_new(run_dir / "admission.json", result)
    if not result["allowed"]:
        R.stage_finding(W, run_dir, "admission", "Waiting for admission: " + "; ".join(result["reasons"]))
    if own_run: R.emit(run_dir, "run_finished", outcome="PASS" if result["allowed"] else "INVALID", summary="Admission allowed" if result["allowed"] else "; ".join(result["reasons"]))
    import json
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["allowed"] else 3


if __name__ == "__main__":
    sys.exit(main())
