"""MAESTRO6 host only: Task 2 fixtures through real open -W -g, no rclone/network."""
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
    parser.add_argument("case", choices=("absent-0555", "clock-rollback", "equal-time", "writefail", "both-unwritable"))
    args = parser.parse_args()
    root = Path(os.environ["LLMDB_ROOT"])
    evidence = Path(__file__).resolve().parent/("host_mb11_"+args.case+"_"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
    evidence.mkdir()
    fixture = Path(tempfile.mkdtemp(prefix="mb11-host-"+args.case+"-", dir="/private/tmp"))
    home = fixture/"home"
    heartbeat = home/"Library/Logs/memit-gdrive-backup/last_run.json"
    receipt = heartbeat.parent/"launch_receipt.json"
    counter = home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
    journal = home/"Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl"
    heartbeat.parent.mkdir(parents=True)
    counter.parent.mkdir(parents=True)
    journal.parent.mkdir(parents=True)
    counter.write_text("10\n")
    wrapper_log, run_log = fixture/"wrapper.log", fixture/"run.jsonl"
    wrapper_log.write_text("")
    run_log.write_text("")
    stat = wrapper_log.stat()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)-dt.timedelta(seconds=2)
    value = {"schema": 1, "run_id": "mb11-host-fixture", "launch_generation": 10, "launch_mode": "applet",
             "start": (now-dt.timedelta(minutes=1)).isoformat(), "end": now.isoformat(), "exit_code": 0,
             "bytes_transferred": 0, "rclone_version": "host-stub", "log_path": str(run_log),
             "wrapper_log": str(wrapper_log), "wrapper_log_identity": [stat.st_dev, stat.st_ino],
             "wrapper_log_offset": 0}
    heartbeat.write_text(json.dumps(value)+"\n")
    previous_heartbeat = heartbeat.read_bytes()
    wrapper = Path("/Volumes")/("memit-mb11-absent-"+fixture.name)/"backup_gdrive.sh"
    assert not wrapper.parent.exists(), "absent-volume positive control failed"
    if args.case == "writefail":
        wrapper = fixture/"success-stub.sh"
        wrapper.write_text("#!/bin/sh\nexit 0\n")
    receipt.write_text(json.dumps({"schema": 1, "utc": now.isoformat(), "launch_generation": 10,
                                  "wrapper_path": str(wrapper), "exit_code": 0, "error_number": None})+"\n")
    previous_receipt = receipt.read_bytes()
    text = (root/"tools/launchd/MemitGdriveBackup.applescript").read_text()
    failure_time = now-dt.timedelta(seconds=1) if args.case == "clock-rollback" else now
    def isolate(match):
        name, literal = match.groups()
        body = json.loads(literal)
        if name == "wrapperPath":
            body = str(wrapper)
        if name in {"generationShell", "receiptShell"}:
            body = "HOME="+shlex.quote(str(home))+"\n"+body
        if name == "receiptShell" and args.case in {"clock-rollback", "equal-time"}:
            before = "my ($sec, $micro) = gettimeofday();"
            assert body.count(before) == 1, "timestamp fixture must patch precisely one declaration"
            body = body.replace(before, "my ($sec, $micro) = ("+str(int(failure_time.timestamp()))+", 0);")
        return "property "+name+" : "+json.dumps(body)
    source = fixture/"MemitGdriveBackup.applescript"
    source.write_text(re.sub(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', isolate, text, flags=re.M))
    app = fixture/"MemitGdriveBackup.app"
    commands = []
    result = {"case": args.case, "status": "UNVERIFIED", "fixture": str(fixture), "source": str(source),
              "applet_source_sha256": hashlib.sha256(text.encode()).hexdigest()}
    def record(command, completed, expected=0):
        commands.append({"args": command, "exit_code": completed.returncode,
                         "stdout": completed.stdout, "stderr": completed.stderr})
        (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        assert completed.returncode == expected, "unexpected command exit; see "+str(evidence/"commands.json")
    def status(expected):
        command = [sys.executable, "-B", str(root/"tools/backup_gdrive_status.py"), "--heartbeat", str(heartbeat)]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=5)
        record(command, completed, expected)
        assert completed.stdout.strip(), "status returned no observation"
        return completed.stdout
    locked = []
    try:
        status(0)  # Verify the observation layer against a fresh successful generation.
        if args.case in {"absent-0555", "writefail", "both-unwritable"}:
            assert os.geteuid() != 0, "0555 regression requires a non-root host runner"
            locked.append(receipt.parent)
            if args.case == "both-unwritable":
                locked.append(journal.parent)
            for directory in locked:
                directory.chmod(0o555)
        command = ["/usr/bin/osacompile", "-o", str(app), str(source)]
        record(command, subprocess.run(command, capture_output=True, text=True, timeout=15))
        assert (app/"Contents/MacOS/applet").is_file(), "compiler produced no applet"
        manifest = {str(path.relative_to(app)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in app.rglob("*") if path.is_file()}
        assert manifest, "empty applet bundle manifest"
        (evidence/"bundle_sha256.json").write_text(json.dumps(manifest, indent=2)+"\n")
        command = ["/usr/bin/open", "-W", "-g", str(app)]
        print(shlex.join(command), flush=True)
        start = time.monotonic()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate(timeout=2)
            commands.append({"args": command, "exit_code": proc.returncode, "stdout": stdout,
                             "stderr": stderr, "error": "open lifecycle timeout; inspect retained host fixture"})
            raise
        elapsed = time.monotonic()-start
        record(command, subprocess.CompletedProcess(command, proc.returncode, stdout, stderr))
        assert elapsed < 5, "prompt-free completion was not proved"
        assert heartbeat.read_bytes() == previous_heartbeat, "applet changed the owner heartbeat"
        assert counter.read_text().strip() == "11", "launch did not allocate the next generation"
        observation = status(1)
        if args.case == "both-unwritable":
            assert not journal.exists(), "unwritable journal unexpectedly accepted a marker"
            assert "unacknowledged launch generation" in observation, observation
        elif args.case in {"absent-0555", "writefail"}:
            assert "journal" in observation, observation
            markers = [json.loads(line) for line in journal.read_text().splitlines()]
            assert markers and max(marker["launch_generation"] for marker in markers) == 11
            assert any("publication" in marker["reason"] for marker in markers)
        else:
            launch = json.loads(receipt.read_text())
            assert launch["launch_generation"] == 11 and launch["exit_code"] == 127
            stamp = dt.datetime.fromisoformat(launch["utc"].replace("Z", "+00:00"))
            assert stamp == failure_time, "rollback/equality stamp fixture was not exercised"
            assert stamp <= dt.datetime.fromisoformat(value["end"])
            assert "failed backup launch" in observation, observation
            result.update(failure_time=launch["utc"], preceding_success_time=value["end"])
        if locked:
            assert receipt.read_bytes() == previous_receipt, "failed publication replaced the prior receipt"
            assert not list(receipt.parent.glob(".launch-receipt.*")), "temporary receipt leaked"
        for path in (receipt, journal, counter):
            if path.is_file():
                (evidence/path.name).write_bytes(path.read_bytes())
        # Equal/later completed generations clear failures even if their clock is earlier.
        value.update(launch_generation=11, start=(now-dt.timedelta(minutes=2)).isoformat(),
                     end=(now-dt.timedelta(seconds=2)).isoformat())
        for directory in locked:
            directory.chmod(0o700)
        heartbeat.write_text(json.dumps(value)+"\n")
        status(0)
        result.update(status="PASS", open_wall_s=elapsed, unhealthy_observation=observation.strip(),
                      recovered_generation=11)
    except (AssertionError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        result.update(status="FAILED", error=str(exc))
    finally:
        for directory in locked:
            directory.chmod(0o700)
    (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
    (evidence/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
