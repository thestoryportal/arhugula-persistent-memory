"""Host-only r4 checks via real open -W -g; isolated HOME, stub child, no rclone/network."""
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
import time
import traceback


# RED baseline: MB14 behavior exposed through small test seams, before the fix.
def select_fixture_root(requested):
    return Path(__file__).resolve().parent


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("manual-interleave", "crash-after-allocation", "recovery"))
    parser.add_argument("--fixture-root", type=Path)
    args = parser.parse_args(argv)
    args.fixture_root = select_fixture_root(args.fixture_root)
    return args


def initialize_fixture(case, fixture_root):
    case.base = fixture_root/"fixture"
    case.base.mkdir()
    case.home = case.base/"home"
    case.heartbeat = case.home/"Library/Logs/memit-gdrive-backup/last_run.json"
    case.heartbeat.parent.mkdir(parents=True)
    case.counter = case.home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
    case.counter.parent.mkdir()
    case.counter.write_text("0\n")
    case.journal = case.home/"Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl"
    case.log, case.run_log = case.base/"wrapper.log", case.base/"run.jsonl"
    case.log.write_text("")
    case.run_log.write_text("")


def write_applet_source(root, case, number, wrapper, *, env=None):
    source = case.base/("Native_%s.applescript" % number)
    app = case.base/("Native_%s.app" % number)
    text = (root/"tools/launchd/MemitGdriveBackup.applescript").read_text()
    if Path(wrapper).resolve() == (root/"tools/backup_gdrive.sh").resolve():
        assert env and all(name in env for name in ("BACKUP_LOG", "BACKUP_HEARTBEAT", "BACKUP_LOCK_DIR", "BACKUP_RCLONE"))
    entered, release = case.base/"allocation-entered", case.base/"allocation-release"

    def isolate(match):
        name, literal = match.groups()
        body = json.loads(literal)
        if name == "wrapperPath":
            body = str(wrapper)
        if name in {"generationShell", "receiptShell"}:
            body = "export HOME="+shlex.quote(str(case.home))+"\n"+body
        if name == "launchShell" and env:
            body = "\n".join("export "+key+"="+shlex.quote(value) for key, value in env.items()
                             if key.startswith("BACKUP_") and key != "BACKUP_LAUNCH_GENERATION")+"\n"+body
        if name == "generationShell" and case.crash:
            # Hold the actual applet immediately after its allocation returns.
            body += "printf allocated > "+shlex.quote(str(entered))+"\n"
            body += "while [ ! -f "+shlex.quote(str(release))+" ]; do /bin/sleep 0.05; done\n"
        return "property "+name+" : "+json.dumps(body)

    source.write_text(re.sub(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', isolate, text, flags=re.M))
    return source, app


def write_refused_wrapper(base):
    wrapper = base/"refused.sh"
    wrapper.write_text("#!/bin/sh\nexit 75\n")
    return wrapper


def write_recovery_wrapper(base, marker):
    wrapper = base/"stub.sh"
    wrapper.write_text('#!/bin/sh\nprintf "%s" "$BACKUP_LAUNCH_GENERATION" > '+shlex.quote(str(marker))+'\n')
    return wrapper


def copy_fixture_evidence(case, evidence):
    return []


def filter_process_snapshot(listing, executable):
    return ""


def save_process_snapshot(evidence, executable):
    pass


def run_open(command, executable, evidence):
    return subprocess.run(command, capture_output=True, text=True, timeout=20)


def run_crash_open(command, executable, entered, release, evidence, commands):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        deadline = time.monotonic()+10
        while not entered.exists() and proc.poll() is None and time.monotonic()<deadline:
            time.sleep(0.02)
        assert entered.exists(), "native allocation never reached the pre-receipt pause"
        listing = subprocess.run(["/bin/ps", "-axo", "pid=,command="], capture_output=True, text=True, timeout=5)
        assert listing.returncode == 0 and listing.stdout.strip(), "native process inspection unavailable"
        matches = []
        for line in listing.stdout.splitlines():
            fields = line.strip().split(None, 1)
            if len(fields) == 2 and (fields[1] == str(executable) or fields[1].startswith(str(executable)+" ")):
                matches.append(int(fields[0]))
        assert len(matches) == 1, "cannot identify exactly one owned fixture applet; no process killed"
        commands.append({"action": "SIGKILL owned fixture applet", "pid": matches[0], "executable": str(executable)})
        os.kill(matches[0], signal.SIGKILL)
    finally:
        # Release the owned shell even if the process-inspection assertion fails.
        release.touch()
        stdout, stderr = proc.communicate(timeout=10)
    return subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)


def finish_case(case, evidence, result):
    for directory in (case.heartbeat.parent, case.journal.parent):
        if directory.exists():
            directory.chmod(0o700)
    if not case.doCleanups():
        result.update(status="FAIL", error="owned fixture cleanup failed")


def main(argv=None):
    args = parse_arguments(argv)
    root = Path(os.environ["LLMDB_ROOT"]).resolve()
    os.environ["BACKUP_TEST_NO_RCLONE"] = "1"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.path.insert(0, str(root))
    from tools.test_backup_gdrive_addendum import BACKUP, STATUS, GenerationLaunchTest

    evidence = Path(__file__).resolve().parent/("native_"+args.case+"_"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
    evidence.mkdir()
    commands = []

    def observed(command, completed, expected=0):
        commands.append({"args": command, "exit_code": completed.returncode,
                         "stdout": completed.stdout, "stderr": completed.stderr})
        (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        if expected is not None:
            assert completed.returncode == expected, "unexpected command exit; see commands.json"
        return completed

    class NativeCase(GenerationLaunchTest):
        number = 0
        crash = False

        def status(self):
            command = [sys.executable, "-B", str(STATUS), "--heartbeat", str(self.heartbeat)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            observed(command, result, None)
            assert result.stdout.strip(), "status observation was empty"
            return result

        def launch(self, wrapper, *, env=None):
            self.number += 1
            source, app = write_applet_source(root, self, self.number, wrapper, env=env)
            entered, release = self.base/"allocation-entered", self.base/"allocation-release"
            command = ["/usr/bin/osacompile", "-o", str(app), str(source)]
            observed(command, subprocess.run(command, capture_output=True, text=True, timeout=20))
            executable = app/"Contents/MacOS/applet"
            assert executable.is_file(), "compiler produced no native applet"
            manifest = {str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in app.rglob("*") if p.is_file()}
            (evidence/("applet_%s_sha256.json" % self.number)).write_text(json.dumps(manifest, indent=2)+"\n")
            command = ["/usr/bin/open", "-W", "-g", str(app)]
            if not self.crash:
                return observed(command, run_open(command, executable, evidence))
            return observed(command, run_crash_open(command, executable, entered, release, evidence, commands), None)

    case = NativeCase("test_1_manual_interleave_preserves_counter_only_generation_11")
    initialize_fixture(case, args.fixture_root)
    original_home = os.environ["HOME"]
    original_python = os.environ.get("BACKUP_PYTHON")
    original_generation = os.environ.pop("BACKUP_LAUNCH_GENERATION", None)
    os.environ["HOME"] = str(case.home)
    os.environ["BACKUP_PYTHON"] = sys.executable
    result = {"case": args.case, "status": "UNVERIFIED", "fixture": str(case.base), "evidence_kind": "native applet / stub child"}
    try:
        assert os.geteuid() != 0, "0555 regression needs a non-root runner"
        if args.case == "manual-interleave":
            case.test_1_manual_interleave_preserves_counter_only_generation_11()
        elif args.case == "crash-after-allocation":
            case.success_baseline()
            receipt = case.heartbeat.parent/"launch_receipt.json"
            previous = receipt.read_bytes()
            case.crash = True
            case.launch(case.base/"absent/backup_gdrive.sh")
            case.crash = False
            assert int(case.counter.read_text()) == 11 and receipt.read_bytes() == previous and not case.journal.exists()
            wrapper = write_refused_wrapper(case.base)
            case.launch(wrapper)
            value = json.loads(receipt.read_text())
            assert (value["launch_generation"], value["exit_code"]) == (12, 75)
            case.assert_bad("generation 11")
        else:
            case.success_baseline()
            marker = case.base/"dispatched-generation"
            wrapper = write_recovery_wrapper(case.base, marker)
            case.counter.write_text("corrupt\n")
            case.launch(wrapper)
            receipt = case.heartbeat.parent/"launch_receipt.json"
            assert json.loads(receipt.read_text())["launch_generation"] is None and not marker.exists()
            case.counter.write_text("10\n")
            case.launch(wrapper)
            assert not marker.exists(), "counter repair must still refuse ambiguous evidence"
            preserved = {"launch_receipt.json": receipt.read_bytes(), "failures.jsonl": case.journal.read_bytes()}
            command = [sys.executable, "-B", str(STATUS), "recover", "--heartbeat", str(case.heartbeat), "--generation-floor", "10"]
            observed(command, subprocess.run(command, capture_output=True, text=True, timeout=5))
            archive, = (case.counter.parent/"recoveries").iterdir()
            for name, data in preserved.items():
                assert (archive/name).read_bytes() == data
            barrier = int(case.counter.read_text())
            case.launch(wrapper)
            generation = int(marker.read_text())
            assert generation > barrier > 10
            case.assert_bad("recovery barrier")
            case.write_heartbeat(launch_generation=None, launch_mode="manual")
            case.assert_bad("recovery barrier")
            # The native allocation/receipt is real; completion is an explicit fixture.
            case.write_heartbeat(launch_generation=generation, launch_mode="applet")
            assert case.status().returncode == 0
        result.update(status="PASS", native_invocations=case.number)
    except Exception as exc:
        result.update(status="FAIL", error=str(exc))
        (evidence/"failure.txt").write_text(traceback.format_exc())
    finally:
        finish_case(case, evidence, result)
        os.environ["HOME"] = original_home
        if original_python is None:
            os.environ.pop("BACKUP_PYTHON", None)
        else:
            os.environ["BACKUP_PYTHON"] = original_python
        if original_generation is not None:
            os.environ["BACKUP_LAUNCH_GENERATION"] = original_generation
        result["source_sha256"] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in (BACKUP, STATUS, root/"tools/launchd/MemitGdriveBackup.applescript", root/"tools/test_backup_gdrive_addendum.py")}
        (evidence/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
