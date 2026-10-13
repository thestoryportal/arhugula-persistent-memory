#!/usr/bin/env python3
"""Deterministic context + host-hygiene guard for the LLM-as-Database repo.

Materializes state from the host/HEAD instead of trusting remembered state.
Used by the Codex SessionStart/Stop hooks and the autonomy driver.

Modes:
  preflight   host-hygiene + run-readiness + posture. Hard-fails (exit 2) if the
              host cannot safely run an experiment. Use BEFORE substantive work.
  closeout    §0.4 documentation-obligation + verification posture. Warns (exit 0)
              unless --strict, which hard-fails on undocumented results.
  posture     quick read-only posture line (no hard checks).

Flags: --json (machine-readable), --strict (closeout hard-fail).

The guard uses stdlib only. The timed project probe imports torch and transformers.
"""
from __future__ import annotations
import os, re, sys, json, shutil, subprocess, glob
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[2]))
MODEL_HINT = "data/hf_cache/hub/models--Qwen--Qwen2.5-3B"   # the primary edit-validated model
ENGINE = "code/memit/vendor"
sys.path.insert(0, str(ROOT / "code"))

def sh(args, timeout=3):
    try:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise RuntimeError(f"{args[0]}: {e}") from e
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or "no diagnostic output"
        raise RuntimeError(f"{args[0]} exit {result.returncode}: {detail}")
    return result.stdout.rstrip("\n")


def accelerator():
    # The hook uses system Python. Read the project stack in one separate process.
    interpreter = Path(os.environ.get("CODEX_GUARD_PYTHON", ROOT / ".venv/bin/python"))
    try:
        if not interpreter.is_file():
            raise ValueError(f"missing at {interpreter}")
        out = sh([str(interpreter), "-B", "-c",
                  "import json,torch,transformers;print(json.dumps(dict("
                  "torch=torch.__version__,transformers=transformers.__version__,"
                  "mps_available=torch.backends.mps.is_available())))"], timeout=15)
        try:
            data = json.loads(out)
        except ValueError as e:
            raise ValueError(f"invalid accelerator JSON: {e}") from e
        if (not isinstance(data, dict) or type(data.get("mps_available")) is not bool
                or not all(isinstance(data.get(k), str) and data[k] for k in ("torch", "transformers"))):
            raise ValueError("invalid accelerator JSON fields")
        return dict(data, interpreter=str(interpreter))
    except (RuntimeError, ValueError, OSError) as e:
        return {"error": f"project interpreter probe ({interpreter}): {e}"}


def disk(path):
    try:
        t, u, f = shutil.disk_usage(path)
        return {"path": str(path), "total_gb": t/2**30, "used_gb": u/2**30, "free_gb": f/2**30}
    except OSError as e:
        return {"error": str(e)}


def parse_vm_stat(text):
    """Return reclaimable bytes: free + inactive + speculative pages.

    Inactive and speculative pages can be reclaimed. Exclude wired, active and
    compressor pages. Do not add purgeable pages; they overlap other page counts.
    This is an estimate of available unified memory, not an allocation guarantee.
    """
    match = re.search(r"page size of (\d+) bytes", text)
    if not match or int(match[1]) <= 0:
        raise ValueError("vm_stat: missing or invalid page size")
    counts = []
    for name in ("free", "inactive", "speculative"):
        matches = re.findall(r"^Pages " + name + r":\s*(\d+)\.\s*$", text, re.MULTILINE)
        if len(matches) != 1:
            raise ValueError(f"vm_stat: missing or invalid Pages {name}")
        counts.append(int(matches[0]))
    return sum(counts) * int(match[1])


def ram_gb():
    try:
        total = int(sh(["/usr/sbin/sysctl", "-n", "hw.memsize"]))
        available = parse_vm_stat(sh(["/usr/bin/vm_stat"]))
        if total <= 0 or available > total:
            raise ValueError("sysctl/vm_stat: invalid memory totals")
        return {"total_gb": total/2**30, "available_gb": available/2**30}
    except (RuntimeError, ValueError) as e:
        return {"error": str(e)}


def filter_processes(inventory, own_pid, compute_rule):
    """Validate a pid/ppid/command inventory. Exclude this process and its ancestors."""
    processes = {}
    for line in inventory.splitlines():
        fields = line.strip().split(None, 2)
        if len(fields) != 3 or not all(f.isdigit() for f in fields[:2]):
            raise ValueError(f"ps: invalid inventory row: {line!r}")
        pid, parent = map(int, fields[:2])
        if pid <= 0 or pid in processes:
            raise ValueError(f"ps: invalid or duplicate pid: {pid}")
        processes[pid] = (parent, fields[2])
    if own_pid not in processes:
        raise ValueError("ps: inventory does not contain the guard process")
    ancestors = set()
    pid = own_pid
    while pid:
        if pid in ancestors:
            raise ValueError("ps: cyclic process ancestry")
        if pid not in processes:
            raise ValueError(f"ps: missing ancestor pid {pid}")
        ancestors.add(pid)
        pid = processes[pid][0]
    candidates = "\n".join(f"{pid} {command}" for pid, (_, command) in processes.items()
                           if pid not in ancestors)
    return compute_rule(candidates, own_pid)


def running_experiments():
    from lab.runners.c10w_p2_gate import blocking_processes
    return filter_processes(sh(["/bin/ps", "-axww", "-o", "pid=,ppid=,command="]),
                            os.getpid(), blocking_processes)


def collect():
    a = accelerator(); d = disk(ROOT); r = ram_gb()
    errors = {}

    def command(name, args):
        try:
            out = sh(args, timeout=6 if name == "network" else 3).strip()
            if not out:
                raise ValueError("empty output")
            return out
        except (RuntimeError, ValueError) as e:
            errors[name] = str(e)
            return None

    network = command("network", ["/usr/bin/curl", "--fail", "--silent", "--show-error",
                                  "--head", "--max-time", "5", "https://huggingface.co"])
    branch = command("git branch", ["git", "branch", "--show-current"])
    head = command("git head", ["git", "rev-parse", "--short", "HEAD"])
    try:
        dirty_files = len(sh(["git", "status", "--porcelain"]).splitlines())
    except RuntimeError as e:
        errors["git status"] = str(e)
        dirty_files = None
    try:
        running = running_experiments()
    except (RuntimeError, ValueError, ImportError) as e:
        errors["running experiments"] = str(e)
        running = None
    # The rendered state view is the authority for this opening summary.
    view = ROOT/"_index/program-state.md"; marker = "- **Latest:** "
    try:
        txt = view.read_text(); i = txt.find(marker)
        if i == -1:
            raise ValueError(f"no '{marker.strip()}' line in {view}")
        position = "\n".join(txt[i+len(marker):][:1200].splitlines()[:6])
        if not position.strip():
            raise ValueError(f"empty current position in {view}")
    except (OSError, ValueError) as e:
        errors["current position"] = str(e)
        position = None
    flags = [Path(p).name for p in glob.glob(str(ROOT/"logs/*_DONE.flag")) + glob.glob(str(ROOT/"*_DONE.flag"))]
    return dict(accelerator=a, disk=d, ram=r, transformers=a.get("transformers"),
                model_present=(ROOT/MODEL_HINT).exists(), engine_present=(ROOT/ENGINE).exists(),
                hf_token=(ROOT/".hf_token").exists() or bool(os.environ.get("HF_TOKEN")),
                network="ok" if network else None,
                git=dict(branch=branch, head=head, dirty_files=dirty_files),
                running=running, done_flags=flags, current_position=position, probe_errors=errors)


def readiness_findings(c):
    """Pure policy over measured probe results. Only accelerator and engine block."""
    hard=[]; warn=[]
    a = c["accelerator"]
    if "error" in a:
        hard.append(a["error"])
    elif not a["mps_available"]:
        hard.append("MPS is not available in the project interpreter.")
    if not c["engine_present"]:
        hard.append(f"MEMIT engine missing at {ENGINE}")
    if "error" not in a and c["transformers"] != "4.51.0":
        warn.append(f"transformers={c['transformers']} (pin is 4.51.0)")
    for name, field, limit in (("disk", "free_gb", 20), ("ram", "available_gb", 16)):
        probe = c[name]
        if "error" in probe:
            warn.append(f"{name} probe failed: {probe['error']}")
        elif probe[field] < limit:
            label = f"disk({ROOT}) free" if name == "disk" else "unified memory available estimate"
            warn.append(f"{label} {probe[field]:.2f} GiB < {limit} GiB.")
    if not c["model_present"]:
        warn.append("Qwen2.5-3B not in hf_cache — first run needs a model pull, network, auth and about 6 GB.")
    if c["network"] != "ok" and "network" not in c["probe_errors"]:
        warn.append("network: huggingface.co unreachable — model pulls will fail.")
    if c["running"]:
        warn.append(f"{len(c['running'])} experiment process(es) already RUNNING — MPS serializes; avoid a contending run.")
    if c["git"]["dirty_files"]:
        warn.append(f"git has {c['git']['dirty_files']} uncommitted change(s).")
    warn.extend(f"{name} probe failed: {error}" for name, error in c["probe_errors"].items())
    return hard, warn


def preflight(as_json=False):
    c = collect(); hard, warn = readiness_findings(c)
    verdict = "READY" if not hard else "NOT-READY"
    if as_json:
        print(json.dumps(dict(verdict=verdict, hard=hard, warn=warn, **c), indent=2))
    else:
        print(f"=== PREFLIGHT — host hygiene & run readiness: {verdict} ===")
        print(f"accelerator: {c['accelerator']}")
        print(f"disk({ROOT}): {c['disk']}   unified memory: {c['ram']}")
        print(f"transformers={c['transformers']} engine={'ok' if c['engine_present'] else 'MISSING'} "
              f"Qwen2.5-3B={'cached' if c['model_present'] else 'PULL-on-first-use'} hf_token={c['hf_token']} net={c['network']}")
        print(f"git: {c['git']['branch']}@{c['git']['head']} dirty={c['git']['dirty_files']}")
        if c["running"]: print("RUNNING:\n  " + "\n  ".join(c["running"]))
        if c["done_flags"]: print(f"DONE flags pending review: {c['done_flags']}")
        print("current position (_index/program-state.md):\n  " +
              (c["current_position"] or "UNVERIFIED").replace("\n", "\n  "))
        if hard: print("HARD (blocks a run):\n  - " + "\n  - ".join(hard))
        if warn: print("WARN:\n  - " + "\n  - ".join(warn))
    return 2 if hard else 0


def closeout(strict=False, as_json=False):
    # §0.4: did results change without a evidence/CORPUS/runbook doc change in the same dirty set?
    try:
        dirty = sh(["git","status","--porcelain"]).splitlines()
    except RuntimeError as e:
        msg = dict(verdict="UNVERIFIED", obligations=[f"git status probe failed: {e}"])
        if as_json: print(json.dumps(msg, indent=2))
        else: print(msg["obligations"][0])
        return 2 if strict else 0
    res_changed = [l[3:] for l in dirty if re.match(r"experiments/[^/]+/runs/", l[3:]) and l[3:].endswith(".json")]
    # git lists files, so the split runbook and checkpoints count by prefix; docs/ is now knowledge/ and the records' own documents.
    doc_changed = [l[3:] for l in dirty if l[3:].startswith(("evidence/CORPUS/","knowledge/","program/runbook/","program/checkpoints/"))
                   or re.match(r"experiments/[^/]+/(design|reviews|rulings)/", l[3:]) or l[3:] == "program/EVIDENCE_INDEX.md"]
    obligations=[]
    if res_changed and not doc_changed:
        obligations.append(f"{len(res_changed)} result JSON(s) changed but NO doc update. UNATTENDED → stage to experiments/ml/reviews/pending_findings/NN_<unit>.md (NOT CORPUS). SUPERVISED → full §0.4 close-out (evidence/CORPUS/NN + 00/03 + runbook §0.3/§12/§13 + checkpoint).")
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
              f"MPS={c['accelerator'].get('mps_available', 'UNVERIFIED')} | "
              f"unified memory available={c['ram'].get('available_gb', 'UNVERIFIED')}GiB | "
              f"running={len(c['running']) if c['running'] is not None else 'UNVERIFIED'} | flags={c['done_flags']}")
        hard, warn = readiness_findings(c)
        for finding in hard + warn: print(f"finding: {finding}")
        sys.exit(0)
