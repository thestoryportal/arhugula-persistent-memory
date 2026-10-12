from pathlib import Path
import json
import os
import subprocess

receipt = Path(__file__).resolve().parent
trace = [json.loads(line) for line in (receipt/"execution_trace.jsonl").read_text().splitlines()]
pids = {42050, 43787, 51227}
for item in trace:
    pids.add(item["pid"])
    if "child_pid" in item:
        pids.add(item["child_pid"])
    if item["event"] == "python_start":
        pids.add(item["ppid"])
direct = json.loads((receipt/"direct_results.json").read_text())
pids.add(direct["driver_pid"])
pids.update(item["pid"] for item in direct["commands"])
assert not pids.intersection({32906,32913,32914,36233,36258,36259,37109,65807})
assert all(type(pid) is int and pid > 0 for pid in pids)
command = ["/bin/ps", "-p", ",".join(map(str, sorted(pids))), "-o", "pid=,ppid=,stat=,command="]
result = dict(checker_pid=os.getpid(), started_pids=sorted(pids), ps_command=command)
try:
    ps = subprocess.run(command, text=True, capture_output=True, timeout=10)
    result["ps"] = dict(exit_code=ps.returncode, stdout=ps.stdout, stderr=ps.stderr)
except PermissionError as error:
    result["ps"] = dict(status="UNAVAILABLE", error=repr(error))
os.kill(os.getpid(), 0)
result["liveness_positive_control"] = "current checker PID responds to signal 0"
absent, alive, unavailable = [], [], []
for pid in sorted(pids):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        absent.append(pid)
    except PermissionError as error:
        unavailable.append(dict(pid=pid, error=repr(error)))
    else:
        alive.append(pid)
result.update(absent_pids=absent, alive_pids=alive, unavailable_pids=unavailable)
(receipt/"process_check.json").write_text(json.dumps(result, indent=2)+"\n")
(receipt/"process_ps_attempt.log").write_text(json.dumps(result["ps"], indent=2)+"\n")
print("tracked PIDs="+str(len(pids))+", absent="+str(len(absent))+", alive="+str(alive)+", unavailable="+str(unavailable))
print("ps evidence: "+json.dumps(result["ps"]))
print("checker PID="+str(os.getpid()))
if alive or unavailable:
    raise SystemExit(1)
