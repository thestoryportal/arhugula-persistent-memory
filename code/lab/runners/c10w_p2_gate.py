#!/usr/bin/env python3
"""D-C10w-oracle P2: decide, model-free, whether one P2 stage may dispatch now.

Folds the P2 pre-run review (experiments/c10w/reviews/c10w_oracle_reviews/p2_prerun_{astra,advisor}.md):
engine fingerprint bound to this worktree before every stage (Astra B3), a fail-closed
GPU-exclusivity inspection over the whole process inventory (Astra B1, advisor A3), and
the dispatcher's own frozen-source / authorization / projection guards replayed before
dispatch (advisor A1, A5), so a refusal leaves the P2 directory alive instead of HALTing it.

Prints one JSON record on stdout. Exit 0 = may dispatch, 3 = refuse (reason in the record).
"""
import argparse, json, os, re, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

W = Path(__file__).resolve().parents[3]
PY = W / ".venv/bin/python"

# A process counts as possible GPU/compute work when its executable is a Python or a
# local-model runtime. Each exemption below is an exact, verified model-free command
# (no torch import); anything else - including an unknown Python - blocks the stage.
COMPUTE_EXE = re.compile(r"(?i)^(python[0-9.]*|.*ollama.*|.*llama.*|.*mlx.*)$")
# Other checkouts on this host may still run the pre-v2 layout (tools/, experiments/track_c/), and the gate sees
# every process on the host, so each exemption below names both homes.
EXEMPT = (
    # Lab View static server + its 60 s rebuild (stdlib / matplotlib, code/apps/labviz/labviz_serve.sh)
    r"^\S*\.venv/bin/python -B -m http\.server 8765 --bind 0\.0\.0\.0 --directory projects/labviz-spec-v3/receipts/bulk/labviz/site$",
    r"^\S*\.venv/bin/python -B code/apps/labviz/build\.py$",
    # context watcher (reads a transcript jsonl)
    r"^\S*\.venv/bin/python -B \S*/(?:tools|code/agents)/context_watch\.py \S+\.jsonl \d+ \d+$",
    # model-free readers of this program (no torch import: checked 2026-10-07)
    r"^\S*\.venv/bin/python -B \S*/(?:experiments|code/lab)/track_c/c10(v_layerpick|w_oracle)_read\.py( .*)?$",
    # M3 load sampler, model-free: imports only the stdlib plus this file, which is stdlib (checked 2026-10-16)
    r"^\S*\.venv/bin/python -B /\S*/code/agents/compute_sample\.py( .*)?$",
    # operator desktop tooling on system Pythons
    r"^\S*/Python \S*/\.claude/powerline-config/server\.py$",
    r"^\S*/Python \S*/\.harness-dashboard/serve\.py$",
    # tmux dashboard tools run on the CLT Python 3.9, which has no torch (checked 2026-10-07)
    r"^/Library/Developer/CommandLineTools/\S*/Python \S*/(?:tools|code/apps/dashboard)/dashboard_\w+\.py( .*)?$",
    r"^/Library/Developer/CommandLineTools/(?:usr/bin/python3|Library/Frameworks/Python3\.framework/Versions/3\.9/Resources/Python\.app/Contents/MacOS/Python) (?:/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/)?(?:tools|code/ops/intel)/memit_intel_copy\.py (?:manifest|run)(?: .*)?$",
    # uv-tool MCP servers / browser daemon
    r"^/Users/[^/ ]+/\.(local/share/uv/tools|cache/uv/archive-v0)/[^ ]+/bin/python \S*/(arxiv-mcp-server|blender-mcp|mcp-server-pixeltable-developer)$",
    r"^/Users/[^/ ]+/\.local/share/uv/tools/browser-harness/bin/python -m browser_harness\.daemon$",
)
EXEMPT_RE = tuple(re.compile(p) for p in EXEMPT)


def blocking_processes(inventory, own_pid):
    """Pure: the inventory lines ('<pid> <command>') that may be competing compute work."""
    out = []
    for line in inventory.splitlines():
        pid, _, command = line.strip().partition(" ")
        command = command.strip()
        if not pid.isdigit() or int(pid) == own_pid or not command:
            continue
        exe = os.path.basename(command.split(" ", 1)[0])
        if COMPUTE_EXE.match(exe) and not any(r.match(command) for r in EXEMPT_RE):
            out.append(line.strip())
    return out


def blocking_tmux(names):
    """Pure: an exact-name autoresearch tmux session blocks (advisor A3: no prefix match)."""
    return [n for n in names.splitlines() if n.strip() == "autoresearch"]


def run(cmd, env=None):
    # Process command lines are untrusted text that check_gpu only matches and counts: a non-UTF-8 byte becomes U+FFFD.
    p = subprocess.run(cmd, capture_output=True, text=True, errors="replace", env=env)
    return p.returncode, p.stdout, p.stderr


def check_fingerprint():
    # [LAW:single-enforcer] the fingerprint tool is THE engine check; bind it to W, never inherit LLMDB_ROOT.
    rc, out, err = run([str(PY), "-B", str(W / "code/memit/engine_fingerprint.py")], env=dict(os.environ, LLMDB_ROOT=str(W)))
    return {"ok": rc == 0, "rc": rc, "output": (out + err).strip()}


def check_gpu():
    # [LAW:no-silent-failure] a probe that fails or returns nothing is a refusal, never "no processes".
    rc, out, err = run(["/bin/ps", "-axww", "-o", "pid=,command="])
    if rc != 0 or not out.strip():
        return {"ok": False, "reason": "process inventory failed rc=%d: %s" % (rc, err.strip())}
    procs = blocking_processes(out, os.getpid())
    trc, tout, terr = run(["/usr/bin/env", "tmux", "list-sessions", "-F", "#{session_name}"])
    # Only tmux's exact "no server running" means no sessions; permission/connection errors refuse (fold re-check B1).
    if trc != 0 and not re.fullmatch(r"no server running on [^\n]+", terr.strip()):
        return {"ok": False, "reason": "tmux inventory failed rc=%d: %s" % (trc, terr.strip())}
    sessions = blocking_tmux(tout if trc == 0 else "")
    return {"ok": not procs and not sessions, "blocking_processes": procs, "blocking_tmux": sessions}


def _check_dispatch_guards(stage):
    """Replay the dispatcher's read-only guards for this stage (c10w_oracle_step0.dispatch_stage)."""
    sys.path.insert(0, str(W / "code/lab/track_c"))
    import c10w_oracle_read as R, c10w_oracle_step0 as S, c10w_oracle_train as T
    rec = {}
    try:
        R.entry_preflight()
        step0 = R.latest_directory("step0"); frozen = R.load_frozen(step0)
        rec["frozen_sources"] = "evaluator A1; all others unchanged" if "evaluator_amendment" in frozen else "unchanged"
        p1 = R.latest_directory("p1"); authorization, minutes = S.ensure_authorized("P2", p1); rec["authorization"] = "valid"
        stages = R.TRAIN_STAGES["P2"]
        with tempfile.TemporaryDirectory() as empty:
            # The first stage creates the P2 directory; before it exists, no training record exists either.
            first = stage == stages[0]
            directory = Path(empty) if first else R.latest_directory("p2")
            # First stage: the certificate exactly as dispatch_stage would write it (c10w_oracle_step0.py:379-380).
            proof = (dict(R.load_json(p1 / "preflight.json"), phase="P2", p1_directory=str(p1), authorization=authorization,
                          authorized_projection_minutes=minutes) if first else R.load_json(directory / "preflight.json"))
            T.require_training_preflight(proof, R.sha_file(step0 / "step0.json"), R.frozen_provenance(frozen))
            rec["training_preflight"] = "valid"
            rec["p2_directory"] = None if first else str(directory)
            completed = [R.load_json(p) for p in (directory / "train").glob("*.json")]
            if stage in stages:
                index = stages.index(stage); unit = R.TRAIN_UNITS["P2"][index]
                for previous in R.TRAIN_UNITS["P2"][:index]:
                    records = [R.load_json(p) for p in (directory / "train" / (R.train_tag(previous, s) + ".json") for s in (400, 800)) if p.is_file()]
                    R.require(records and records[-1]["status"] == "PASS", "prior training unit incomplete")
                steps = 400
                if unit[0] == R.SHUF and (directory / "train" / (R.train_tag((R.A7, *unit[1:]), 800) + ".json")).exists():
                    steps = 800
                rec["steps"] = steps
                rec["projected_minutes"] = S.training_projection("P2", proof, completed, {unit: steps})
                S.guard_training_unit(directory, "P2", proof, unit, steps)
                try:  # advisory A5: would an underfit retry at this stage still fit the authorized limit?
                    S.guard_training_unit(directory, "P2", proof, unit, 800, matched_retry=True); rec["retry800_fits"] = True
                except R.Halt as exc:
                    rec["retry800_fits"] = False; rec["retry800_refusal"] = str(exc)
            else:
                R.require(stage == "p2-eval", "not a P2 stage: " + stage)
                rec["projected_minutes"] = S.training_projection("P2", proof, completed, {})
                S.guard_phase_projection(directory, "P2", proof, completed, {})
                R.phase_trains(directory, "P2")
        rec["ok"] = True
    except R.Halt as exc:
        rec.update(ok=False, reason=str(exc))
    return rec


def check_dispatch_guards(stage, reattempt_directory=None):
    if reattempt_directory is None: return _check_dispatch_guards(stage)
    sys.path.insert(0, str(W / "code/lab/track_c"))
    import c10w_oracle_read as R, c10w_p2_rerun as A
    try:
        R.require(stage=="p2-eval", "re-attempt is only for p2-eval")
        proof=A.check_reattempt(reattempt_directory)
        with A.overlay(): rec=_check_dispatch_guards(stage)
        rec["reattempt"]=proof
        if rec["ok"]:
            rec["projected_minutes_with_halted_eval"]=rec["projected_minutes"]+R.load_json(proof["archive_manifest"]["path"])["halted_eval_wall_seconds"]/60
        return rec
    except (R.Halt,OSError,KeyError,TypeError,ValueError) as exc:
        return {"ok":False,"reason":str(exc)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage"); parser.add_argument("--reattempt",type=Path)
    args=parser.parse_args(); stage=args.stage
    checks = {"fingerprint": check_fingerprint(), "gpu": check_gpu(), "dispatch_guards": check_dispatch_guards(stage,args.reattempt)}
    ok = all(c["ok"] for c in checks.values())
    print(json.dumps({"stage": stage, "at": datetime.now().astimezone().isoformat(timespec="seconds"), "ok": ok, "checks": checks}, indent=1))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
