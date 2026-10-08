#!/usr/bin/env python3
"""D-C10w-oracle P2: decide, model-free, whether one P2 stage may dispatch now.

Folds the P2 pre-run review (results/c10w_oracle_reviews/p2_prerun_{astra,advisor}.md):
engine fingerprint bound to this worktree before every stage (Astra B3), a fail-closed
GPU-exclusivity inspection over the whole process inventory (Astra B1, advisor A3), and
the dispatcher's own frozen-source / authorization / projection guards replayed before
dispatch (advisor A1, A5), so a refusal leaves the P2 directory alive instead of HALTing it.

Prints one JSON record on stdout. Exit 0 = may dispatch, 3 = refuse (reason in the record).
"""
import json, os, re, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

W = Path(__file__).resolve().parents[1]
PY = W / ".venv/bin/python"

# A process counts as possible GPU/compute work when its executable is a Python or a
# local-model runtime. Each exemption below is an exact, verified model-free command
# (no torch import); anything else - including an unknown Python - blocks the stage.
COMPUTE_EXE = re.compile(r"(?i)^(python[0-9.]*|.*ollama.*|.*llama.*|.*mlx.*)$")
EXEMPT = (
    # Lab View static server + its 60 s rebuild (stdlib / matplotlib, tools/labviz_serve.sh)
    r"^\S*\.venv/bin/python -B -m http\.server 8765 --bind 0\.0\.0\.0 --directory results/labviz/site$",
    r"^\S*\.venv/bin/python -B tools/labviz/build\.py$",
    # context watcher (reads a transcript jsonl)
    r"^\S*\.venv/bin/python -B \S*/tools/context_watch\.py \S+\.jsonl \d+ \d+$",
    # model-free readers of this program (no torch import: checked 2026-10-07)
    r"^\S*\.venv/bin/python -B \S*/experiments/track_c/c10(v_layerpick|w_oracle)_read\.py( .*)?$",
    # operator desktop tooling on system Pythons
    r"^\S*/Python \S*/\.claude/powerline-config/server\.py$",
    r"^\S*/Python \S*/\.harness-dashboard/serve\.py$",
    # tmux dashboard tools run on the CLT Python 3.9, which has no torch (checked 2026-10-07)
    r"^/Library/Developer/CommandLineTools/\S*/Python \S*/tools/dashboard_\w+\.py( .*)?$",
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
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def check_fingerprint():
    # [LAW:single-enforcer] the fingerprint tool is THE engine check; bind it to W, never inherit LLMDB_ROOT.
    rc, out, err = run([str(PY), "-B", str(W / "tools/engine_fingerprint.py")], env=dict(os.environ, LLMDB_ROOT=str(W)))
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


def check_dispatch_guards(stage):
    """Replay the dispatcher's read-only guards for this stage (c10w_oracle_step0.dispatch_stage)."""
    sys.path.insert(0, str(W / "experiments/track_c"))
    import c10w_oracle_read as R, c10w_oracle_step0 as S, c10w_oracle_train as T
    rec = {}
    try:
        R.entry_preflight()
        step0 = R.latest_directory("step0"); frozen = R.load_frozen(step0); rec["frozen_sources"] = "unchanged"
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


def main():
    stage = sys.argv[1] if len(sys.argv) == 2 else None
    if stage is None:
        print("usage: c10w_p2_gate.py <p2 stage>", file=sys.stderr); return 2
    checks = {"fingerprint": check_fingerprint(), "gpu": check_gpu(), "dispatch_guards": check_dispatch_guards(stage)}
    ok = all(c["ok"] for c in checks.values())
    print(json.dumps({"stage": stage, "at": datetime.now().astimezone().isoformat(timespec="seconds"), "ok": ok, "checks": checks}, indent=1))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
