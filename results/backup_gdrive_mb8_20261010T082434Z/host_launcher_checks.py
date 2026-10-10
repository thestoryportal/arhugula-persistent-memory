"""MAESTRO5 HOST ONLY: actual app bundles through the plist's open -W -g chain."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("long", "exit75", "absent", "writefail"))
    args = parser.parse_args()
    root = Path(os.environ["LLMDB_ROOT"])
    evidence = Path(__file__).resolve().parent/("host_"+args.case+"_"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
    evidence.mkdir()
    # Preserve fixtures and bundles for inspection; never install or load a job.
    fixture = Path(tempfile.mkdtemp(prefix="mb8-host-"+args.case+"-", dir="/private/tmp"))
    home = fixture/"home"
    heartbeat = home/"Library/Logs/memit-gdrive-backup/last_run.json"
    heartbeat.parent.mkdir(parents=True)
    wrapper_log, run_log = fixture/"wrapper.log", fixture/"run.jsonl"
    wrapper_log.write_text("")
    run_log.write_text("")
    stat = wrapper_log.stat()
    now = dt.datetime.now(dt.timezone.utc)
    value = {"schema": 1, "run_id": "host-fixture", "start": (now-dt.timedelta(minutes=1)).isoformat(),
             "end": now.isoformat(), "exit_code": 0, "bytes_transferred": 0,
             "rclone_version": "host-stub", "log_path": str(run_log), "wrapper_log": str(wrapper_log),
             "wrapper_log_identity": [stat.st_dev, stat.st_ino], "wrapper_log_offset": 0}
    if args.case == "exit75":
        value.update(end=None, exit_code=None, owner_pid=os.getpid(), rclone_pid=None)
    heartbeat.write_text(json.dumps(value)+"\n")
    previous = heartbeat.read_bytes()
    marker = fixture/"long-stub.marker"
    wrapper = fixture/"backup-stub.sh"
    if args.case == "long":
        wrapper.write_text("#!/bin/sh\n/usr/bin/printf 'started\\n' > "+shlex.quote(str(marker))+
                           "\n/bin/sleep 3\n/usr/bin/printf 'finished\\n' >> "+shlex.quote(str(marker))+"\n")
    elif args.case == "exit75":
        wrapper.write_text("#!/bin/sh\nexit 75\n")
    elif args.case == "writefail":
        wrapper.write_text("#!/bin/sh\nexit 0\n")
    else:
        # A nonexistent volume namespace models the unmounted-volume case.
        wrapper = Path("/Volumes")/("memit-mb8-absent-"+fixture.name)/"backup_gdrive.sh"
        assert not wrapper.parent.exists(), "absent-volume positive control failed"
    text = (root/"tools/launchd/MemitGdriveBackup.applescript").read_text()
    def isolate(match):
        name, literal = match.groups()
        content = json.loads(literal)
        if name == "wrapperPath":
            content = str(wrapper)
        if name == "receiptShell":
            content = "HOME="+shlex.quote(str(home))+"\n"+content
        return "property "+name+" : "+json.dumps(content)
    variant = re.sub(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', isolate, text, flags=re.M)
    source = fixture/"MemitGdriveBackup.applescript"
    source.write_text(variant)
    app = fixture/"MemitGdriveBackup.app"
    commands = []
    result = {"case": args.case, "status": "UNVERIFIED", "fixture": str(fixture),
              "source": str(source), "applet_source_sha256": hashlib.sha256(text.encode()).hexdigest()}
    receipt = heartbeat.parent/"launch_receipt.json"
    prior_receipt = None
    if args.case == "writefail":
        assert os.geteuid() != 0, "permission failure requires a non-root host runner"
        receipt.write_text(json.dumps({"schema": 1, "utc": now.isoformat(), "wrapper_path": str(wrapper),
                                       "exit_code": 0, "error_number": None})+"\n")
        prior_receipt = receipt.read_bytes()
        receipt.parent.chmod(0o555)
    def record(command, completed):
        commands.append({"args": command, "exit_code": completed.returncode,
                         "stdout": completed.stdout, "stderr": completed.stderr})
        (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        assert completed.returncode == 0, "command failed; see "+str(evidence/"commands.json")
    try:
        command = ["/usr/bin/osacompile", "-o", str(app), str(source)]
        record(command, subprocess.run(command, capture_output=True, text=True, timeout=15))
        assert (app/"Contents/MacOS/applet").is_file(), "compiler did not produce an applet"
        manifest = {str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in app.rglob("*") if p.is_file()}
        (evidence/"bundle_sha256.json").write_text(json.dumps(manifest, indent=2)+"\n")
        command = ["/usr/bin/open", "-W", "-g", str(app)]
        print(shlex.join(command), flush=True)
        start = time.monotonic()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        try:
            if args.case == "long":
                deadline = time.monotonic()+5
                while not marker.exists() and proc.poll() is None and time.monotonic()<deadline:
                    time.sleep(0.02)
                assert marker.exists(), "positive control: long stub never started"
                assert proc.poll() is None, "open -W exited while the stub was still running"
            stdout, stderr = proc.communicate(timeout=10 if args.case == "long" else 5)
        except (AssertionError, subprocess.TimeoutExpired):
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate(timeout=2)
            commands.append({"args": command, "exit_code": proc.returncode, "stdout": stdout,
                             "stderr": stderr, "error": "lifecycle timeout/assertion; app may still need host inspection"})
            (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
            raise
        elapsed = time.monotonic()-start
        record(command, subprocess.CompletedProcess(command, proc.returncode, stdout, stderr))
        if args.case == "long":
            assert elapsed >= 3 and "finished" in marker.read_text(), "open -W must await stub completion"
        else:
            assert elapsed < 5, "prompt-free completion was not proved"
        launch = json.loads(receipt.read_text())
        (evidence/"launch_receipt.json").write_bytes(receipt.read_bytes())
        assert launch["wrapper_path"] == str(wrapper)
        assert launch["exit_code"] == {"long": 0, "exit75": 75, "absent": 127, "writefail": 0}[args.case]
        if args.case == "writefail":
            assert receipt.read_bytes() == prior_receipt, "failed receipt write must preserve the previous file"
            assert not list(receipt.parent.glob(".launch-receipt.*")), "failed write leaked a temporary receipt"
        assert heartbeat.read_bytes() == previous, "applet must never write the owner heartbeat"
        command = [sys.executable, "-B", str(root/"tools/backup_gdrive_status.py"), "--heartbeat", str(heartbeat)]
        status = subprocess.run(command, capture_output=True, text=True, timeout=5)
        commands.append({"args": command, "exit_code": status.returncode, "stdout": status.stdout, "stderr": status.stderr})
        if args.case == "exit75":
            assert status.returncode != 0 and "incomplete" in status.stdout and "failed" not in status.stdout
        elif args.case == "absent":
            assert status.returncode != 0 and "failed backup launch" in status.stdout
        else:
            assert status.returncode == 0, status.stdout+status.stderr
        result.update(status="PASS", open_wall_s=elapsed, launch=launch)
    except (AssertionError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        result.update(status="FAILED", error=str(exc))
    finally:
        if args.case == "writefail":
            receipt.parent.chmod(0o700)
    (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
    (evidence/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
