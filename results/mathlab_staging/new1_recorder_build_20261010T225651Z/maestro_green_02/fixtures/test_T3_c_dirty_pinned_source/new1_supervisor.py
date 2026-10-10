import json, os, signal, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
root = Path(os.environ["LLMDB_ROOT"])
cfg = json.loads((root/"fixture.json").read_text())
run = root/"results/mathlab_staging/runs"/("new1_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
run.mkdir(exist_ok=False)
(root/"supervisor_started").write_text(str(os.getpid()))
keys = ["PATH", "TMPDIR", "LLMDB_ROOT", "LLMDB_DEVICE", "CUDA_VISIBLE_DEVICES",
        "OMP_NUM_THREADS", "MKL_NUM_THREADS", "PYTHONDONTWRITEBYTECODE"]
(root/"executed_command.json").write_text(json.dumps({"argv": sys.argv,
    "executable": sys.executable, "cwd": os.getcwd(), "env": {key:os.environ.get(key) for key in keys},
    "nice": os.getpriority(os.PRIO_PROCESS, 0), "sigint_handler": str(signal.getsignal(signal.SIGINT))}))
inventory = subprocess.run(["/bin/ps", "-axo", "pid=,ppid=,pgid=,nice=,command="], capture_output=True, text=True)
if inventory.returncode: raise RuntimeError(inventory.stderr)
(root/"recorder_inventory.txt").write_text(inventory.stdout)
def event(kind, **fields):
    row = dict(type=kind, schema=1, run_id=run.name,
               ts=datetime.now(timezone.utc).isoformat(), **fields)
    with (run/"events.jsonl").open("a") as target: target.write(json.dumps(row)+"\n")
event("run_started", step=4, title="NEW1 fixture", purpose="experiment",
      deadline_ts="2099-01-01T00:00:00Z", pid=os.getpid())
worker = None
def interrupted(*args):
    (root/"sigint_received").write_text(str(os.getpid()))
    raise KeyboardInterrupt()
signal.signal(signal.SIGINT, interrupted)
code = "PASS"
try:
    if cfg.get("mode") == "admission":
        code = "INVALID-ADMISSION"
    else:
        worker = subprocess.Popen(["/usr/bin/nice", "-n", str(cfg.get("worker_nice", 10)),
            sys.executable, "-B", str(root/"tools/new1_geometry.py")], start_new_session=True,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (root/"worker_pid").write_text(str(worker.pid))
        if cfg.get("mode") == "unreaped": time.sleep(.4)
        else: worker.wait(timeout=4)
        if cfg.get("mode") == "deadline": code = "STOPPED-DEADLINE"
        if cfg.get("mode") == "resource": code = "STOPPED-RESOURCE"
except KeyboardInterrupt:
    code = "OPERATOR"
finally:
    if worker is not None and cfg.get("mode") != "unreaped":
        if worker.poll() is None: os.killpg(worker.pid, signal.SIGTERM)
        worker.wait(timeout=4)
if code == "PASS": event("run_finished", outcome="PASS", summary="fixture complete")
elif code == "STOPPED-DEADLINE": print(code+": fixture expired; no prediction verdict", file=sys.stderr)
else: event("halted", reason=code+": fixture stop", diagnostic_path="fixture")
print(code, flush=True)
if cfg.get("mode") == "unreaped": os._exit(0)
sys.exit(0 if code == "PASS" else 3)
