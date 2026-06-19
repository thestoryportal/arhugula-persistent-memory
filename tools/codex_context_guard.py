#!/usr/bin/env python3
"""Deterministic context + pod-hygiene guard for the LLM-as-Database repo.

Materializes state from the pod/HEAD instead of trusting remembered state.
Used by the Codex SessionStart/Stop hooks and the autonomy driver.

Modes:
  preflight   pod-hygiene + run-readiness + posture. Hard-fails (exit 2) if the
              pod cannot safely run an experiment. Use BEFORE substantive work.
  closeout    §0.4 documentation-obligation + verification posture. Warns (exit 0)
              unless --strict, which hard-fails on undocumented results.
  posture     quick read-only posture line (no hard checks).

Flags: --json (machine-readable), --strict (closeout hard-fail).

Dependency-free (stdlib + git/nvidia-smi/df/free via subprocess).
"""
from __future__ import annotations
import os, sys, json, shutil, subprocess, glob
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[1]))
MODEL_HINT = "hf_cache/hub/models--Qwen--Qwen2.5-3B"   # the primary edit-validated model
ENGINE = "memit_dry_run/memit"

def sh(args, timeout=20):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except Exception as e:
        return f"<unavailable: {e}>"

def gpu():
    out = sh(["nvidia-smi", "--query-gpu=memory.used,memory.total,utilization.gpu", "--format=csv,noheader,nounits"])
    try:
        used, total, util = [int(x) for x in out.split(",")]
        return {"used_mib": used, "total_mib": total, "free_mib": total - used, "util_pct": util}
    except Exception:
        return {"error": out}

def disk(path):
    try:
        t, u, f = shutil.disk_usage(path); return {"total_gb": t//2**30, "used_gb": u//2**30, "free_gb": f//2**30}
    except Exception as e:
        return {"error": str(e)}

def ram_gb():
    try:
        mem = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo") if l.split(":")[0] in ("MemTotal","MemAvailable")}
        return {"total_gb": mem["MemTotal"]//2**20, "available_gb": mem["MemAvailable"]//2**20}
    except Exception as e:
        return {"error": str(e)}

def running_experiments():
    out = sh(["bash","-lc","ps -eo pid,etimes,cmd | grep -E 'python.*(g6_scale_n|run_edit|evaluate|a2|a7|c2|b3|cov)' | grep -v grep || true"])
    return [l for l in out.splitlines() if l.strip()]

def collect():
    g = gpu(); d = disk(ROOT); shm = disk("/dev/shm"); r = ram_gb()
    tf = sh(["python3","-c","import transformers;print(transformers.__version__)"])
    model_present = (ROOT/MODEL_HINT).exists()
    engine_present = (ROOT/ENGINE).exists()
    hf_token = (ROOT/".hf_token").exists() or bool(os.environ.get("HF_TOKEN"))
    net = sh(["bash","-lc","timeout 6 curl -sI https://huggingface.co >/dev/null 2>&1 && echo ok || echo no"])
    git_branch = sh(["git","branch","--show-current"]); git_head = sh(["git","rev-parse","--short","HEAD"])
    git_dirty = sh(["git","status","--porcelain"]);
    s03 = ""
    rb = ROOT/"EXPERIMENT_RUNBOOK.md"
    if rb.exists():
        txt = rb.read_text(errors="ignore"); i = txt.find("§0.3 — CURRENT POSITION")
        if i!=-1:
            s03 = "\n".join(txt[i:i+1200].splitlines()[:6])
    flags = [Path(p).name for p in glob.glob(str(ROOT/"logs/*_DONE.flag")) + glob.glob(str(ROOT/"*_DONE.flag"))]
    return dict(gpu=g, disk=d, shm=shm, ram=r, transformers=tf, model_present=model_present,
                engine_present=engine_present, hf_token=hf_token, network=net,
                git=dict(branch=git_branch, head=git_head, dirty_files=len([l for l in git_dirty.splitlines() if l.strip()])),
                running=running_experiments(), done_flags=flags, runbook_0_3=s03)

def preflight(as_json=False):
    c = collect(); hard=[]; warn=[]
    g = c["gpu"]
    if "error" in g: hard.append(f"GPU not queryable: {g['error']}")
    elif g["free_mib"] < 16000: warn.append(f"GPU free {g['free_mib']} MiB < 16 GiB — a 3B/7B edit may not fit; check `running`.")
    if not c["engine_present"]: hard.append(f"MEMIT engine missing at {ENGINE}")
    if c["transformers"] != "4.51.0": warn.append(f"transformers={c['transformers']} (pin is 4.51.0)")
    fd = c["disk"].get("free_gb")
    if fd is not None and fd < 20: warn.append(f"/workspace free {fd} GB low (cluster pool — TRUE VOLUME QUOTA IS OPERATOR-KNOWN, df undercounts; confirm before a model pull).")
    if not c["model_present"]: warn.append("Qwen2.5-3B not in hf_cache — first run will PULL it (needs network + auth + ~6 GB; standing-auth: OK).")
    if c["network"] != "ok": warn.append("huggingface.co unreachable — model pulls will fail.")
    if c["running"]: warn.append(f"{len(c['running'])} experiment process(es) already RUNNING — GPU serializes; don't launch a contending run.")
    if c["git"]["dirty_files"] > 0: warn.append(f"git has {c['git']['dirty_files']} uncommitted change(s).")
    verdict = "READY" if not hard else "NOT-READY"
    if as_json:
        print(json.dumps(dict(verdict=verdict, hard=hard, warn=warn, **c), indent=2)); return 2 if hard else 0
    print(f"=== PREFLIGHT — pod hygiene & run readiness: {verdict} ===")
    print(f"GPU: {g}")
    print(f"disk(/workspace): {c['disk']}   shm: {c['shm']}   ram: {c['ram']}")
    print(f"transformers={c['transformers']} engine={'ok' if c['engine_present'] else 'MISSING'} "
          f"Qwen2.5-3B={'cached' if c['model_present'] else 'PULL-on-first-use'} hf_token={c['hf_token']} net={c['network']}")
    print(f"git: {c['git']['branch']}@{c['git']['head']} dirty={c['git']['dirty_files']}")
    if c["running"]: print("RUNNING:\n  " + "\n  ".join(c["running"]))
    if c["done_flags"]: print(f"DONE flags pending review: {c['done_flags']}")
    if c["runbook_0_3"]: print("runbook §0.3 (what's next):\n  " + c["runbook_0_3"].replace("\n","\n  "))
    if hard: print("HARD (blocks a run):\n  - " + "\n  - ".join(hard))
    if warn: print("WARN:\n  - " + "\n  - ".join(warn))
    return 2 if hard else 0

def closeout(strict=False, as_json=False):
    # §0.4: did results change without a CORPUS/runbook doc change in the same dirty set?
    dirty = sh(["git","status","--porcelain"]).splitlines()
    res_changed = [l[3:] for l in dirty if l[3:].startswith("results/") and l[3:].endswith(".json")]
    doc_changed = [l[3:] for l in dirty if l[3:].startswith(("CORPUS/","docs/")) or l[3:] in ("EXPERIMENT_RUNBOOK.md","SESSION_CHECKPOINT.md","EVIDENCE_INDEX.md")]
    obligations=[]
    if res_changed and not doc_changed:
        obligations.append(f"{len(res_changed)} result JSON(s) changed but NO doc update. UNATTENDED → stage to logs/pending_findings/NN_<unit>.md (NOT CORPUS). SUPERVISED → full §0.4 close-out (CORPUS/NN + 00/03 + runbook §0.3/§12/§13 + checkpoint).")
    msg = dict(verdict="OBLIGATIONS" if obligations else "CLEAN",
               results_changed=res_changed, docs_changed=doc_changed, obligations=obligations,
               reminder="Report the exact verification commands + their results. Do NOT claim success without them. A cleanly-HALTED run with a diagnostic is a SUCCESS.")
    if as_json: print(json.dumps(msg, indent=2))
    else:
        print("=== CLOSEOUT posture ===")
        if obligations: print("OBLIGATIONS:\n  - " + "\n  - ".join(obligations))
        else: print("No undocumented result changes detected.")
        print(msg["reminder"])
    return 2 if (obligations and strict) else 0

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "posture"
    aj = "--json" in sys.argv; strict = "--strict" in sys.argv
    if mode == "preflight": sys.exit(preflight(aj))
    elif mode == "closeout": sys.exit(closeout(strict, aj))
    else:
        c = collect()
        print(f"posture: git {c['git']['branch']}@{c['git']['head']} dirty={c['git']['dirty_files']} | "
              f"GPU free {c['gpu'].get('free_mib','?')}MiB | running={len(c['running'])} | flags={c['done_flags']}")
        sys.exit(0)
