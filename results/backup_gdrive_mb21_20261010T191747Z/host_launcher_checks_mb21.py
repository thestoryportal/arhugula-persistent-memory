"""Host-only r5/r4 checks via real open -W -g; isolated HOME, stub child, no rclone/network."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import traceback


def select_fixture_root(requested):
    if requested is None:
        return Path(tempfile.mkdtemp(prefix="memit_gdrive_native_", dir="/private/tmp")).resolve()
    path = requested.resolve()
    if path.is_relative_to(Path("/Volumes")):
        raise ValueError("--fixture-root must resolve outside /Volumes")
    if not path.exists():
        raise ValueError("--fixture-root must already exist")
    if not path.is_dir():
        raise ValueError("--fixture-root must be a directory")
    if any(path.iterdir()):
        raise ValueError("--fixture-root must be empty")
    return path


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("manual-interleave", "crash-after-allocation", "recovery", "unresolved-compaction", "compaction-boundary"))
    parser.add_argument("--fixture-root", type=Path, help="existing empty directory outside /Volumes; default: fresh /private/tmp directory")
    args = parser.parse_args(argv)
    try:
        args.fixture_root = select_fixture_root(args.fixture_root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return args


def initialize_fixture(case, fixture_root):
    case.base = fixture_root/"fixture"
    case.home = case.base/"home"
    case.heartbeat = case.home/"Library/Logs/memit-gdrive-backup/last_run.json"
    case.counter = case.home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
    case.journal = case.home/"Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl"
    case.log, case.run_log = case.base/"wrapper.log", case.base/"run.jsonl"
    case.base.mkdir()
    case.heartbeat.parent.mkdir(parents=True)
    case.counter.parent.mkdir()
    case.counter.write_text("0\n")
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
    copied = evidence/"fixture_copy"
    copied.mkdir(exist_ok=True)
    paths = (case.log, case.run_log, case.counter, case.heartbeat.parent/"launch_receipt.json",
             case.heartbeat, case.journal, case.counter.parent/"unresolved.json", case.counter.parent/"recoveries")
    for path in paths:
        if path.exists():
            target = copied/path.relative_to(case.base)
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir():
                shutil.copytree(path, target)
            else:
                shutil.copy2(path, target)
    return [str(p.relative_to(copied)) for p in sorted(copied.rglob("*")) if p.is_file()]


def filter_process_snapshot(listing, executable):
    rows = []
    header = "PID PPID STAT ELAPSED COMMAND"
    for line in listing.splitlines():
        fields = line.strip().split(None, 4)
        if fields and fields[0] == "PID":
            header = line
        elif fields:
            if len(fields) != 5:
                raise ValueError("malformed ps row")
            rows.append((int(fields[0]), int(fields[1]), fields[4], line))
    executable = str(executable)
    selected = {pid for pid, _, command, _ in rows
                if command == executable or command.startswith(executable+" ")}
    if not selected:
        return "NO MATCH: applet executable absent from this process listing: "+executable+"\n"
    while True:
        children = {pid for pid, parent, _, _ in rows if parent in selected}
        if children.issubset(selected):
            break
        selected.update(children)
    return "\n".join([header, *(line for pid, _, _, line in rows if pid in selected)])+"\n"


def save_process_snapshot(evidence, executable):
    command = ["/bin/ps", "-axo", "pid,ppid,stat,etime,command"]
    text = "COMMAND: "+shlex.join(command)+"\nAPPLET: "+str(executable)+"\n"
    try:
        listing = subprocess.run(command, capture_output=True, text=True, timeout=5)
        if listing.returncode:
            text += "UNAVAILABLE: ps exit "+str(listing.returncode)+"\n"+listing.stderr
        elif not listing.stdout.strip():
            text += "UNAVAILABLE: ps returned an empty listing\n"
        else:
            text += filter_process_snapshot(listing.stdout, executable)
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        text += "UNAVAILABLE: "+str(exc)+"\n"
    # A later failure must not erase the first hung process tree.
    with (evidence/"process_snapshot.txt").open("a") as stream:
        stream.write(text+"\n")


def record_open_exception(command, evidence, exc):
    path = evidence/"commands.json"
    commands = json.loads(path.read_text()) if path.exists() else []
    entry = {"args": command, "exit_code": None, "error_type": type(exc).__name__, "error": str(exc)}
    if isinstance(exc, subprocess.TimeoutExpired):
        entry["timeout"] = exc.timeout
    commands.append(entry)
    path.write_text(json.dumps(commands, indent=2)+"\n")


def run_open(command, executable, evidence):
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        save_process_snapshot(evidence, executable)
        record_open_exception(command, evidence, exc)
        raise
    if completed.returncode:
        save_process_snapshot(evidence, executable)
    return completed


def run_crash_open(command, executable, entered, release, evidence, commands):
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except OSError as exc:
        save_process_snapshot(evidence, executable)
        record_open_exception(command, evidence, exc)
        raise
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
    except Exception as exc:
        save_process_snapshot(evidence, executable)
        record_open_exception(command, evidence, exc)
        raise
    finally:
        # Release the owned shell even if the process-inspection assertion fails.
        release.touch()
        try:
            stdout, stderr = proc.communicate(timeout=10)
        except (OSError, subprocess.TimeoutExpired) as exc:
            save_process_snapshot(evidence, executable)
            record_open_exception(command, evidence, exc)
            raise
    if proc.returncode:
        save_process_snapshot(evidence, executable)
    return subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)


def finish_case(case, evidence, result):
    result["fixture_root"] = str(case.base.parent)
    try:
        for directory in (case.heartbeat.parent, case.journal.parent):
            if directory.exists():
                directory.chmod(0o700)
        if not case.doCleanups():
            result.update(status="FAIL", error="owned fixture cleanup failed")
    except Exception as exc:
        result.update(status="FAIL", cleanup_error=str(exc))
        with (evidence/"failure.txt").open("a") as stream:
            stream.write(traceback.format_exc())
    finally:
        try:
            result["fixture_copy"] = copy_fixture_evidence(case, evidence)
        except Exception as exc:
            result.update(status="FAIL", fixture_copy_error=str(exc))
            with (evidence/"failure.txt").open("a") as stream:
                stream.write(traceback.format_exc())


def main(argv=None):
    args = parse_arguments(argv)
    root = Path(os.environ["LLMDB_ROOT"]).resolve()
    os.environ["BACKUP_TEST_NO_RCLONE"] = "1"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.path.insert(0, str(root))
    from tools.test_backup_gdrive_addendum import BACKUP, STATUS, GenerationLaunchTest, R5CompactionTest

    evidence = Path(__file__).resolve().parent/("native_"+args.case+"_"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
    evidence.mkdir()
    commands = []
    (evidence/"commands.json").write_text("[]\n")

    def observed(command, completed, expected=0):
        commands.append({"args": command, "exit_code": completed.returncode,
                         "stdout": completed.stdout, "stderr": completed.stderr})
        (evidence/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        if expected is not None:
            assert completed.returncode == expected, "unexpected command exit; see commands.json"
        return completed

    class NativeCase(GenerationLaunchTest, R5CompactionTest):
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
    original_home = os.environ["HOME"]
    original_python = os.environ.get("BACKUP_PYTHON")
    original_generation = os.environ.pop("BACKUP_LAUNCH_GENERATION", None)
    result = {"case": args.case, "status": "UNVERIFIED", "fixture": str(args.fixture_root/"fixture"),
              "fixture_root": str(args.fixture_root), "backup_python": sys.executable,
              "backup_wrapper": str(BACKUP), "evidence_kind": "native applet / stub child"}
    try:
        initialize_fixture(case, args.fixture_root)
        os.environ["HOME"] = str(case.home)
        os.environ["BACKUP_PYTHON"] = sys.executable
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
        elif args.case == "unresolved-compaction":
            # Execute the 2,000-allocation production-Perl fixture once, then cross
            # the interval boundary with actual native applet allocation/refusal.
            case.test_4_two_thousand_allocations_remain_bounded_and_fail_closed()
            state = case.state(case.INTERVAL_LIMIT)
            case.counter.write_text(str(state["issued_generation"])+"\n")
            (case.counter.parent/"unresolved.json").write_text(json.dumps(state)+"\n")
            case.write_heartbeat(launch_generation=10, launch_mode="applet")
            case.write_launch_receipt(launch_generation=10, exit_code=0)
            case.assert_bad("generation 11")
            wrapper = write_refused_wrapper(case.base)
            case.launch(wrapper)
            compacted = json.loads((case.counter.parent/"unresolved.json").read_text())
            barrier = compacted["compaction_barrier"]
            assert barrier == state["issued_generation"]+1
            assert compacted["unresolved"] == []
            assert (case.counter.parent/"unresolved.json").stat().st_size <= case.BYTE_LIMIT
            case.assert_bad("compacted barrier")
            case.write_heartbeat(launch_generation=None, launch_mode="manual")
            case.launch(wrapper)
            assert json.loads((case.counter.parent/"unresolved.json").read_text())["compaction_barrier"] == barrier
            case.assert_bad("compacted barrier")
            marker = case.base/"completed-generation"
            case.launch(write_recovery_wrapper(case.base, marker))
            generation = int(marker.read_text())
            assert generation > barrier
            case.assert_bad("compacted barrier")
            case.write_heartbeat(launch_generation=generation, launch_mode="applet")
            assert case.status().returncode == 0
            result.update(allocations_checked=2000, interval_limit=case.INTERVAL_LIMIT,
                          byte_limit=case.BYTE_LIMIT, compaction_barrier=barrier)
        elif args.case == "compaction-boundary":
            state = case.state(case.INTERVAL_LIMIT)
            state_path = case.counter.parent/"unresolved.json"
            case.counter.write_text(str(state["issued_generation"])+"\n")
            state_path.write_text(json.dumps(state)+"\n")
            case.write_heartbeat(launch_generation=10, launch_mode="applet")
            case.write_launch_receipt(launch_generation=10, exit_code=0)
            wrapper = write_refused_wrapper(case.base)
            case.launch(wrapper)
            compacted = json.loads(state_path.read_bytes())
            assert compacted["compaction_barrier"] == 139 and compacted["unresolved"] == []
            (evidence/"unresolved_compacted.json").write_bytes(state_path.read_bytes())
            case.write_heartbeat(launch_generation=139, launch_mode="applet")
            case.assert_bad("compacted barrier generation 139")
            # Both native publishers see equality during allocation/refusal 140.
            case.launch(wrapper)
            assert int(case.counter.read_text()) == 140
            assert json.loads(state_path.read_bytes())["compaction_barrier"] == 139
            case.assert_bad("compacted barrier generation 139")
            (evidence/"unresolved_equal.json").write_bytes(state_path.read_bytes())
            case.write_heartbeat(launch_generation=140, launch_mode="applet")
            assert case.status().returncode == 0
            case.launch(wrapper)
            assert int(case.counter.read_text()) == 141
            assert json.loads(state_path.read_bytes())["compaction_barrier"] is None
            assert case.status().returncode == 0
            (evidence/"unresolved_above.json").write_bytes(state_path.read_bytes())
            result.update(compaction_barrier=139, rejected_completion=139, accepted_completion=140)
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
