"""Backup heartbeat and archival controls; real local rclone, optional tiny Drive probe."""
import datetime as dt
import hashlib
import fcntl
import json
import os
from pathlib import Path
import plistlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.test_backup_gdrive import run_process

STATUS = ROOT / "code/ops/backup/backup_gdrive_status.py"
BACKUP = ROOT / "code/ops/backup/backup_gdrive.sh"
ARCHIVE = ROOT / "code/ops/backup/archive_to_gdrive.sh"
RCLONE = "/opt/homebrew/bin/rclone"
NO_RCLONE = os.environ.get("BACKUP_TEST_NO_RCLONE") == "1"
HOST_RCLONE = unittest.skipIf(NO_RCLONE, "HOST-PENDING: real rclone forbidden by MB14 brief")


def isolate_failing_launcher_home(source, home):
    def isolate(match):
        name, literal = match.groups()
        body = json.loads(literal)
        if name in {"generationShell", "receiptShell"}:
            body = "HOME="+shlex.quote(str(home))+"\nexport HOME\n"+body
        return "property "+name+" : "+json.dumps(body)
    return re.sub(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', isolate, source, flags=re.M)


class LauncherHomeExportTest(unittest.TestCase):
    def test_fixture_home_reaches_perl_with_absent_and_sentinel_parent_home(self):
        with tempfile.TemporaryDirectory(prefix="launcher_home_", dir="/private/tmp") as temporary:
            base = Path(temporary)
            home, sentinel = base/"fixture-home", base/"sentinel-home"
            home.mkdir()
            sentinel.mkdir()
            source = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
            # Keep the native transform; replace only each property's Perl payload.
            transformed = isolate_failing_launcher_home(source, home)
            for name in ("generationShell", "receiptShell"):
                match = re.search(r'^property '+name+r' : ("(?:\\.|[^"\\])*")$', transformed, re.M)
                self.assertIsNotNone(match)
                body = json.loads(match.group(1))
                original = json.loads(re.search(r'^property '+name+r' : ("(?:\\.|[^"\\])*")$',
                                                source, re.M).group(1))
                self.assertIn("/usr/bin/perl", original)
                self.assertTrue(body.endswith(original))
                prefix = body[:-len(original)]
                probe = prefix+"/usr/bin/perl -e 'print $ENV{HOME} // \"UNSET\"'"
                for parent in (None, str(sentinel)):
                    with self.subTest(property=name, parent_home=parent):
                        env = dict(os.environ)
                        if parent is None:
                            env.pop("HOME", None)
                        else:
                            env["HOME"] = parent
                        result = run_process(["/bin/sh", "-c", probe], env=env, timeout=5)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(result.stdout, str(home))


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="gdrive_addendum_", dir=os.environ.get("BACKUP_TEST_RECEIPTS", "/private/tmp"))
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.home = self.base/"home"
        self.home.mkdir()
        isolated = mock.patch.dict(os.environ, HOME=str(self.home), BACKUP_PYTHON=sys.executable,
                                   PYTHONDONTWRITEBYTECODE="1")
        isolated.start()
        self.addCleanup(isolated.stop)
        os.environ.pop("BACKUP_LAUNCH_GENERATION", None)
        self.log = self.base / "wrapper.log"
        self.log.write_text("")
        self.run_log = self.base / "rclone.jsonl"
        self.run_log.write_text("")
        self.heartbeat = self.base / "heartbeat/last_run.json"
        self.heartbeat.parent.mkdir()

    def status(self):
        return run_process([sys.executable, "-B", str(STATUS), "--heartbeat", str(self.heartbeat)])

    def write_heartbeat(self, **changes):
        now = dt.datetime.now(dt.timezone.utc)
        stat = self.log.stat()
        value = {"schema": 1, "run_id": "fixture", "start": (now-dt.timedelta(minutes=1)).isoformat(),
                 "end": now.isoformat(), "exit_code": 0, "bytes_transferred": 10,
                 "rclone_version": "rclone v1.75.2", "log_path": str(self.run_log),
                 "wrapper_log": str(self.log), "wrapper_log_offset": stat.st_size,
                 "wrapper_log_identity": [stat.st_dev, stat.st_ino]}
        value.update(changes)
        self.heartbeat.write_text(json.dumps(value))

    def assert_bad(self, word):
        result = self.status()
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn(word, (result.stdout+result.stderr).lower())

    def write_launch_receipt(self, **changes):
        value = {"schema": 1, "utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                 "wrapper_path": str(BACKUP), "exit_code": 127, "error_number": None}
        value.update(changes)
        path = self.heartbeat.parent/"launch_receipt.json"
        path.write_text(json.dumps(value)+"\n")
        return path

    def hold_live_owner(self):
        source = self.base/"held-source"
        source.mkdir()
        (source/"tiny.txt").write_text("local fixture")
        release = self.base/"owner-release.fifo"
        os.mkfifo(release)
        entered = self.base/"owner-entered"
        rclone = self.base/"held-rclone"
        rclone.write_text('#!/bin/bash\nif [ "$1" = version ]; then echo rclone-test; exit 0; fi\n'+
                          ('if [ "$1" = config ]; then printf "{}\\n"; exit 0; fi\n' if NO_RCLONE else
                           'if [ "$1" = config ]; then exec '+RCLONE+' "$@"; fi\n')+
                          'printf entered > '+shlex.quote(str(entered))+'\n'
                          'IFS= read -r released < '+shlex.quote(str(release))+'\n')
        rclone.chmod(0o700)
        env = dict(os.environ, BACKUP_SRC=str(source), BACKUP_DEST=("fixture:" if NO_RCLONE else "")+str(self.base/"held-mirror"),
                   BACKUP_LOG=str(self.log), BACKUP_HEARTBEAT=str(self.heartbeat),
                   BACKUP_LOCK_DIR=str(self.base/"lock"), BACKUP_MOUNT_POINT="/",
                   BACKUP_RCLONE=str(rclone), BACKUP_EXCLUDES=str(ROOT/"code/ops/backup/backup_mirror.excludes"))
        owner = subprocess.Popen(["/bin/bash", str(BACKUP)], env=env, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)
        self.addCleanup(owner.communicate, timeout=5)
        def release_owner():
            if owner.poll() is None:
                fd = os.open(release, os.O_WRONLY | os.O_NONBLOCK)
                try:
                    os.write(fd, b"release\n")
                finally:
                    os.close(fd)
        self.addCleanup(release_owner)
        deadline = time.monotonic()+3
        while owner.poll() is None and time.monotonic()<deadline:
            if (entered.exists() and self.heartbeat.exists() and
                    json.loads(self.heartbeat.read_text()).get("rclone_pid")):
                break
            time.sleep(0.01)
        self.assertTrue(entered.exists(), "positive control: real wrapper owns the lock and dispatched its child")
        self.assertIsNone(owner.poll())
        value = json.loads(self.heartbeat.read_text())
        self.assertEqual(value["owner_pid"], owner.pid)
        self.assertGreater(value["rclone_pid"], 0)
        self.assert_bad("incomplete")
        return owner, env


class StatusTest(Fixture):
    def test_fresh_success(self):
        self.write_heartbeat()
        result = self.status()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)

    def test_launch_failure_precedes_fresh_success_and_newer_heartbeat_recovers(self):
        counter = self.heartbeat.parent.parent/"memit-gdrive-backup-launch-state/counter"
        counter.parent.mkdir()
        counter.write_text("10\n")
        self.write_heartbeat(launch_generation=10, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0, "positive control: previous backup is fresh")
        previous = self.heartbeat.read_bytes()
        receipt = self.write_launch_receipt(launch_generation=11)
        counter.write_text("11\n")
        self.assert_bad("launch")
        self.assertEqual(self.heartbeat.read_bytes(), previous, "status must only read the owner's heartbeat")
        stamp = json.loads(receipt.read_text())["utc"]
        for end in [stamp, (dt.datetime.fromisoformat(stamp)+dt.timedelta(microseconds=1)).isoformat()]:
            self.write_heartbeat(end=end, launch_generation=10, launch_mode="applet")
            self.assert_bad("launch")
        self.write_heartbeat(end=stamp, launch_generation=11, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0, "only a completed equal or later generation clears the failure")
        self.write_launch_receipt(exit_code=0, launch_generation=11)
        self.write_heartbeat(exit_code=23, launch_generation=11, launch_mode="applet")
        self.assert_bad("failed")

    def test_malformed_launch_receipts_fail_closed_without_changing_heartbeat(self):
        self.write_heartbeat()
        previous = self.heartbeat.read_bytes()
        path = self.heartbeat.parent/"launch_receipt.json"
        for content in ["{torn", "[]", "{}"]:
            with self.subTest(content=content):
                path.write_text(content)
                self.assert_bad("launch")
        for changes in [{"schema": 2}, {"utc": "yesterday"}, {"utc": "2026-10-10T01:00:00"},
                        {"utc": (dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat()},
                        {"exit_code": True}, {"exit_code": None}, {"wrapper_path": ""},
                        {"error_number": "-1708"}, {"error_number": -1708}]:
            with self.subTest(changes=changes):
                self.write_launch_receipt(**changes)
                self.assert_bad("launch")
        self.assertEqual(self.heartbeat.read_bytes(), previous)

    def test_incomplete_dead_owner_and_rclone_are_stale_without_expiring_live_runs(self):
        dead = subprocess.Popen(["/usr/bin/true"])
        dead.wait(timeout=2)
        self.write_heartbeat(end=None, exit_code=None, owner_pid=dead.pid, rclone_pid=dead.pid)
        self.assert_bad("stale")
        for owner, child in [(os.getpid(), dead.pid), (dead.pid, os.getpid()), (os.getpid(), None)]:
            with self.subTest(owner=owner, child=child):
                self.write_heartbeat(end=None, exit_code=None, owner_pid=owner, rclone_pid=child)
                result = self.status()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("incomplete", result.stdout)
                self.assertNotIn("stale", result.stdout)

    def test_zero_exit_heartbeat_with_dry_run_or_skipped_log_is_not_success(self):
        for message in ["Skipped copy as --dry-run is set", "Skipped delete", "Skipping move"]:
            with self.subTest(message=message):
                self.write_heartbeat(rclone_exit_code=0)
                self.run_log.write_text(json.dumps({"level":"notice", "msg":message, "object":"tiny.txt"})+"\n")
                self.assert_bad("skipped")

    def test_stale_and_exact_thirteen_hour_boundary(self):
        for age in [13, 14]:
            with self.subTest(age=age):
                end = dt.datetime.now(dt.timezone.utc)-dt.timedelta(hours=age)
                self.write_heartbeat(start=(end-dt.timedelta(minutes=1)).isoformat(), end=end.isoformat())
                self.assert_bad("stale")

    def test_failed(self):
        self.write_heartbeat(exit_code=7)
        self.assert_bad("failed")

    def test_missing(self):
        self.assert_bad("missing")

    def test_malformed_future_and_inflight_fail_closed(self):
        self.heartbeat.write_text("{torn")
        self.assert_bad("malformed")
        self.write_heartbeat(end=None, exit_code=None)
        self.assert_bad("incomplete")
        self.write_heartbeat(end=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=1)).isoformat())
        self.assert_bad("future")

    def test_current_auth_error_and_old_auth_error_recovery(self):
        self.write_heartbeat()
        self.run_log.write_text(json.dumps({"level":"error", "msg":"oauth2: cannot fetch token: invalid_grant"})+"\n")
        self.assert_bad("auth")
        self.run_log.write_text("")
        self.log.write_text("old run: invalid_grant\nold run: HEARTBEAT-FAILED\n")
        self.write_heartbeat()
        self.assertEqual(self.status().returncode, 0)

    def test_new_publication_failure_and_log_rotation_are_not_silent(self):
        self.write_heartbeat()
        with self.log.open("a") as stream:
            stream.write("backup_gdrive: newer-run HEARTBEAT-FAILED\n")
        self.assert_bad("heartbeat")
        self.write_heartbeat()
        self.log.unlink()
        self.log.write_text("")
        self.assert_bad("log")

    def test_nonfatal_source_churn_is_visible_in_status(self):
        self.write_heartbeat(rclone_exit_code=1, warnings=[{"kind":"source_vanished", "object":"lost.bin"},
                             {"kind":"destination_deletions_suppressed"}])
        result = self.status()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("with warnings", result.stdout)
        self.assertIn("deletions suppressed", result.stdout)

    def test_malformed_warning_fields_refuse_success(self):
        for changes in [{"warnings":"source vanished"}, {"warnings":["source vanished"]},
                        {"warnings":[{"kind":"unknown"}]}, {"rclone_exit_code":"1"},
                        {"warnings":[{"kind":"source_vanished"}]},
                        {"warnings":[{"kind":"source_vanished","object":[]}]},
                        {"warnings":[{"kind":"nonregular_source_skipped","object":""}]}]:
            with self.subTest(changes=changes):
                self.write_heartbeat(**changes)
                self.assert_bad("malformed")

    def test_warning_paths_are_one_status_line(self):
        self.write_heartbeat(rclone_exit_code=0,warnings=[{"kind":"source_vanished","object":"line\nbreak"}])
        result=self.status()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(len(result.stdout.splitlines()),1)
        self.assertIn("line\\nbreak",result.stdout)


class HeartbeatTest(Fixture):
    def setUp(self):
        super().setUp()
        self.src = self.base / "source"
        self.src.mkdir()
        (self.src / "tiny.txt").write_bytes(b"eight!!!")
        self.env = dict(os.environ, BACKUP_SRC=str(self.src), BACKUP_DEST=("fixture:" if NO_RCLONE else "")+str(self.base / "mirror"),
                        BACKUP_LOG=str(self.log), BACKUP_HEARTBEAT=str(self.heartbeat),
                        BACKUP_LOCK_DIR=str(self.base / "lock"), BACKUP_MOUNT_POINT="/",
                        BACKUP_RCLONE=str(self.base/"HOST-PENDING-rclone") if NO_RCLONE else RCLONE, BACKUP_EXCLUDES=str(ROOT / "code/ops/backup/backup_mirror.excludes"))

    def backup(self, **changes):
        return run_process(["/bin/bash", str(BACKUP)], env=dict(self.env, **changes), timeout=10)

    def fake_rclone(self, body):
        path = self.base / "fake-rclone"
        path.write_text('#!/bin/bash\nif [ "$1" = version ]; then echo "rclone-test"; exit 0; fi\n'+
                        ('if [ "$1" = config ]; then printf "{}\\n"; exit 0; fi\n' if NO_RCLONE else
                           'if [ "$1" = config ]; then exec '+RCLONE+' "$@"; fi\n')+body)
        path.chmod(0o700)
        return str(path)

    @HOST_RCLONE
    def test_real_sync_publishes_actual_bytes_and_completed_success(self):
        result = self.backup()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertTrue(self.heartbeat.exists(), "every run must publish its heartbeat")
        value = json.loads(self.heartbeat.read_text())
        self.assertEqual(value["exit_code"], 0)
        self.assertEqual(value["bytes_transferred"], 8)
        self.assertTrue(value["start"] and value["end"])
        self.assertIn("v1.75.2", value["rclone_version"])
        self.assertEqual(self.status().returncode, 0)
        self.assertFalse(list(self.heartbeat.parent.glob(".last_run.*")))

    def test_refusal_still_records_failed_run_without_dispatch(self):
        result = self.backup(BACKUP_SRC=str(self.base / "missing"))
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.heartbeat.exists(), "refused runs need a terminal heartbeat")
        value = json.loads(self.heartbeat.read_text())
        self.assertNotEqual(value["exit_code"], 0)
        self.assertEqual(value["bytes_transferred"], 0)
        self.assertTrue(value["end"])
        self.assert_bad("failed")

    def test_inflight_is_visible_and_missing_stats_are_unknown(self):
        fake = self.fake_rclone("/bin/sleep 0.6\n")
        proc = subprocess.Popen(["/bin/bash", str(BACKUP)], env=dict(self.env, BACKUP_RCLONE=fake),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(proc.communicate, timeout=4)
        deadline = time.monotonic()+2
        while proc.poll() is None and time.monotonic()<deadline:
            if ((self.base/"lock/rclone.pid").exists() and self.heartbeat.exists() and
                    json.loads(self.heartbeat.read_text()).get("rclone_pid")):
                break
            time.sleep(0.01)
        self.assertTrue(self.heartbeat.exists(), "start heartbeat must precede dispatch")
        value = json.loads(self.heartbeat.read_text())
        self.assertEqual(value.get("owner_pid"), proc.pid)
        self.assertEqual(value.get("rclone_pid"), int((self.base/"lock/rclone.pid").read_text()))
        self.assert_bad("incomplete")
        output = proc.communicate(timeout=4)
        self.assertEqual(proc.returncode, 0, output)
        self.assertIsNone(json.loads(self.heartbeat.read_text())["bytes_transferred"])

    @HOST_RCLONE
    def test_start_publication_failure_invalidates_previous_success(self):
        self.assertEqual(self.backup().returncode, 0)
        self.assertTrue(self.heartbeat.exists(), "positive control needs prior success")
        previous = self.heartbeat.read_bytes()
        self.heartbeat.parent.chmod(0o555)
        try:
            result = self.backup()
            self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertEqual(self.heartbeat.read_bytes(), previous)
            self.assert_bad("heartbeat")
        finally:
            self.heartbeat.parent.chmod(0o700)

    @HOST_RCLONE
    def test_exit_publication_failure_is_loud_and_preserves_original_failure(self):
        for exit_code in [0, 23]:
            with self.subTest(exit_code=exit_code):
                self.assertEqual(self.backup().returncode, 0)
                fake = self.fake_rclone('/bin/chmod 555 "'+str(self.heartbeat.parent)+'"\nexit '+str(exit_code)+'\n')
                try:
                    result = self.backup(BACKUP_RCLONE=fake)
                    self.assertEqual(result.returncode, exit_code or 1, result.stdout+result.stderr)
                    self.assertIn("HEARTBEAT-FAILED", self.log.read_text())
                    self.assertNotEqual(self.status().returncode, 0)
                finally:
                    self.heartbeat.parent.chmod(0o700)

    def test_child_pid_publication_failure_reaps_child_and_preserves_raw_failure(self):
        fake = self.fake_rclone('/bin/chmod 555 "'+str(self.heartbeat.parent)+'"\n/bin/sleep 0.2\nexit 23\n')
        try:
            result = self.backup(BACKUP_RCLONE=fake)
            self.assertEqual(result.returncode, 23, result.stderr)
            self.assertFalse((self.base/"lock").exists(), "a reaped child permits owned-lock cleanup")
            self.assertIn("HEARTBEAT-FAILED", result.stderr)
        finally:
            self.heartbeat.parent.chmod(0o700)

    def test_terminal_publication_cannot_mask_a_newer_active_run(self):
        first_entered, first_release = self.base/"first-dispatched", self.base/"first-release"
        fake = self.fake_rclone('touch "'+str(first_entered)+'"\n'
                               'for i in {1..500}; do [ -f "'+str(first_release)+'" ] && break; /bin/sleep 0.01; done\n')
        first = subprocess.Popen(["/bin/bash", str(BACKUP)], env=dict(self.env, BACKUP_RCLONE=fake),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(first.communicate, timeout=8)
        self.addCleanup(first_release.touch)
        deadline = time.monotonic()+3
        while not first_entered.exists() and first.poll() is None and time.monotonic()<deadline:
            time.sleep(0.01)
        self.assertTrue(first_entered.exists(), "positive control: A owns the lock and is syncing")
        paused, resume = self.base/"second-before-lock", self.base/"second-resume"
        dispatched = self.base/"second-dispatched"
        second_release = self.base/"second-release"
        second_fake = self.base/"second-rclone"
        second_fake.write_text(Path(fake).read_text().replace(str(first_entered), str(dispatched))
                               .replace(str(first_release), str(second_release)))
        second_fake.chmod(0o700)
        # Pause the actual shell before mkdir, after the old pre-lock publication.
        # The corrected wrapper reaches this same boundary before publishing start.
        command = r'''
pause_lock() {
  case "$1" in '/bin/mkdir "$LOCK"')
    trap - DEBUG
    touch "$PAUSED"
    for i in {1..500}; do [ -f "$RESUME" ] && break; /bin/sleep 0.01; done
    ;;
  esac
}
set -T
trap 'pause_lock "$BASH_COMMAND"' DEBUG
source "$1"
'''
        second = subprocess.Popen(["/bin/bash", "-c", command, str(BACKUP), str(BACKUP)],
                                  env=dict(self.env, BACKUP_RCLONE=str(second_fake), PAUSED=str(paused), RESUME=str(resume)),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(second.communicate, timeout=8)
        self.addCleanup(second_release.touch)
        self.addCleanup(resume.touch)
        deadline = time.monotonic()+3
        while second.poll() is None and not paused.exists() and time.monotonic()<deadline:
            time.sleep(0.01)
        self.assertTrue(paused.exists(), "positive control: B paused before lock acquisition")
        self.assertFalse(dispatched.exists())
        first_release.touch()
        output = first.communicate(timeout=5)
        self.assertEqual(first.returncode, 0, output)
        self.assertFalse((self.base/"lock").exists(), "A must finish and release ownership before resuming B")
        resume.touch()
        deadline = time.monotonic()+3
        while second.poll() is None and not dispatched.exists() and time.monotonic()<deadline:
            time.sleep(0.01)
        self.assertTrue(dispatched.exists(), "B must be admitted and dispatch; a refused contender is not this schedule")
        self.assertIsNone(second.poll(), "B must still be syncing while status is inspected")
        result = self.status()
        self.assertNotEqual(result.returncode, 0, "older terminal success must not mask an admitted newer sync: "+result.stdout)
        self.assertIn("incomplete", result.stdout)

    def test_held_lock_refusal_cannot_overwrite_owner_heartbeat(self):
        entered, release = self.base/"owner-dispatched", self.base/"owner-release"
        fake = self.fake_rclone('touch "'+str(entered)+'"\n'
                               'for i in {1..500}; do [ -f "'+str(release)+'" ] && break; /bin/sleep 0.01; done\n')
        owner = subprocess.Popen(["/bin/bash", str(BACKUP)], env=dict(self.env, BACKUP_RCLONE=fake),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(owner.communicate, timeout=8)
        self.addCleanup(release.touch)
        # Allow up to three seconds for the owner's post-dispatch PID publication.
        deadline = time.monotonic()+3
        child_pid_path = self.base/"lock/rclone.pid"
        missing = ["post-dispatch heartbeat publication"]
        while time.monotonic()<deadline:
            value = json.loads(self.heartbeat.read_text()) if self.heartbeat.exists() else {}
            child_pid = child_pid_path.read_text().strip() if child_pid_path.exists() else ""
            published_pid = value.get("rclone_pid")
            conditions = [
                (owner.poll() is None, "running lock owner"),
                (entered.exists(), "dispatch marker"),
                (value.get("owner_pid") == owner.pid, "heartbeat owner_pid == owner.pid"),
                (type(published_pid) is int and published_pid > 0 and child_pid.isdigit() and
                 published_pid == int(child_pid), "positive heartbeat rclone_pid matching lock/rclone.pid"),
            ]
            missing = [name for reached, name in conditions if not reached]
            if not missing:
                break
            time.sleep(0.01)
        else:
            self.fail("three-second timeout waiting for: "+", ".join(missing))
        previous = self.heartbeat.read_bytes()
        result = self.backup()
        self.assertEqual(result.returncode, 75, result.stderr)
        self.assertEqual(self.heartbeat.read_bytes(), previous, "a non-owner cannot publish over the active owner")
        refusals = list((self.heartbeat.parent/"refusals").glob("*.json"))
        self.assertEqual(len(refusals), 1, "a refused schedule needs its own receipt")
        value = json.loads(refusals[0].read_text())
        self.assertEqual(value["exit_code"], 75)
        self.assertEqual(value["bytes_transferred"], 0)
        self.assert_bad("incomplete")

    def test_one_thousand_live_owner_refusals_have_bounded_storage(self):
        owner, env = self.hold_live_owner()
        previous = self.heartbeat.read_bytes()
        start = time.monotonic()
        for invocation in range(1000):
            result = run_process(["/bin/bash", str(BACKUP)], env=env, timeout=10)
            self.assertEqual(result.returncode, 75, "refusal %s: %s" % (invocation+1, result.stderr))
        elapsed = time.monotonic()-start
        files = [path for path in self.heartbeat.parent.rglob("*") if path.is_file()]
        refusals = list((self.heartbeat.parent/"refusals").glob("*.json"))
        print("refusal_stress: "+json.dumps({"invocations": 1000, "wall_s": round(elapsed, 3),
                                           "files": len(files), "refusal_files": len(refusals),
                                           "bytes": sum(path.stat().st_size for path in files)}), flush=True)
        self.assertIsNone(owner.poll(), "owner must remain live through all 1,000 refusals")
        self.assertEqual(self.heartbeat.read_bytes(), previous)
        self.assert_bad("incomplete")
        self.assertEqual(len(refusals), 1, "refusal storage must stay at one latest receipt after 1,000 real runs")
        self.assertEqual(refusals[0].name, "latest-refusal.json")
        self.assertEqual(json.loads(refusals[0].read_text())["exit_code"], 75)
        self.assertLessEqual(len(files), 3, "only owner heartbeat/log and latest refusal may remain")
        self.assertLess(sum(path.stat().st_size for path in files), 16384)
        self.assertFalse(list(self.heartbeat.parent.rglob(".last_run.*")))

    def test_behavior_changing_rclone_environment_refuses_without_dispatch(self):
        dispatched = self.base/"unexpected-dispatch"
        fake = self.fake_rclone('touch "'+str(dispatched)+'"\n')
        for name in ["RCLONE_DRY_RUN", "RCLONE_IGNORE_ERRORS", "RCLONE_DELETE_EXCLUDED",
                     "RCLONE_IGNORE_EXISTING", "RCLONE_FILTER", "RCLONE_CONFIG_FIXTURE_GLOBAL_DRY_RUN"]:
            with self.subTest(name=name):
                result = self.backup(BACKUP_RCLONE=fake, **{name:"true"})
                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertFalse(dispatched.exists(), "unsafe inherited settings must refuse before sync")
                self.assertIn(name, result.stderr)
                self.assert_bad("failed")

    @HOST_RCLONE
    def test_remote_global_overrides_refuse_without_dispatch(self):
        config = self.base/"rclone.conf"
        dispatched = self.base/"unexpected-dispatch"
        fake = self.fake_rclone('touch "'+str(dispatched)+'"\nexec '+RCLONE+' "$@"\n')
        for setting in ["global.dry_run", "global.ignore_errors", "global.delete_excluded", "override.low_level_retries"]:
            with self.subTest(setting=setting):
                config.write_text('[fixture]\ntype = local\n'+setting+' = true\n')
                result = self.backup(BACKUP_RCLONE=fake, RCLONE_CONFIG=str(config),
                                     BACKUP_DEST="fixture:"+str(self.base/"mirror"))
                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertFalse(dispatched.exists(), "config overrides must refuse before sync")
                self.assertIn(setting, result.stderr)
                self.assert_bad("failed")

    def test_remote_connection_overrides_refuse_without_dispatch(self):
        dispatched = self.base/"unexpected-dispatch"
        fake = self.fake_rclone('touch "'+str(dispatched)+'"\n')
        result = self.backup(BACKUP_RCLONE=fake, BACKUP_DEST=":local,global.dry_run=true:"+str(self.base/"mirror"))
        self.assertNotEqual(result.returncode, 0, result.stderr)
        self.assertFalse(dispatched.exists())

    @HOST_RCLONE
    def test_dispatched_sync_explicitly_enforces_safety_and_low_level_retries(self):
        args = self.base/"sync-args"
        fake = self.fake_rclone('printf "%s\\n" "$@" > "'+str(args)+'"\nexec '+RCLONE+' "$@"\n')
        result = self.backup(BACKUP_RCLONE=fake)
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = args.read_text().splitlines()
        for flag in ["--dry-run=false", "--ignore-errors=false", "--delete-excluded=false", "--interactive=false"]:
            self.assertIn(flag, actual)
        self.assertEqual(actual[actual.index("--retries")+1], "1")
        self.assertGreater(int(actual[actual.index("--low-level-retries")+1]), 1)

    @HOST_RCLONE
    def test_operator_daytime_upload_limit_is_dispatched_with_full_speed_at_night(self):
        args = self.base/"timetable-args"
        fake = self.fake_rclone('printf "%s\\n" "$@" > "'+str(args)+'"\nexec '+RCLONE+' "$@"\n')
        result = self.backup(BACKUP_RCLONE=fake)
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = args.read_text().splitlines()
        self.assertIn("--bwlimit", actual, "D-C10r-rulings-15 requires the operator's upload timetable")
        self.assertEqual(actual[actual.index("--bwlimit")+1], "08:00,512k 23:00,off")
        self.assertEqual((self.base/"mirror/tiny.txt").read_bytes(), b"eight!!!")

    def test_lock_cleanup_failure_records_failed_outcome(self):
        fake = self.fake_rclone('touch "$BACKUP_LOCK_DIR/unexpected"\n')
        result = self.backup(BACKUP_RCLONE=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(json.loads(self.heartbeat.read_text())["exit_code"], 0)
        self.assert_bad("failed")

    def log_rclone(self, records, exit_code=1):
        script = self.base/"logged-rclone"
        script.write_text('#!/usr/bin/python3\nimport json,sys,subprocess\nfrom pathlib import Path\n'
                          'if sys.argv[1] == "version":\n print("rclone fixture");sys.exit(0)\n'+
                          ('if sys.argv[1] == "config":\n print("{}");sys.exit(0)\n' if NO_RCLONE else
                           'if sys.argv[1] == "config":\n sys.exit(subprocess.call(['+repr(RCLONE)+',*sys.argv[1:]]))\n')+
                          'path=Path(sys.argv[sys.argv.index("--log-file")+1])\n'
                          'records='+repr(records)+'\n'
                          'path.write_text("".join(json.dumps(record)+"\\n" if not isinstance(record,str) else record+"\\n" for record in records))\n'
                          'sys.exit('+str(exit_code)+')\n')
        script.chmod(0o700)
        return str(script)

    def vanished_records(self, name="lost.bin", error_count=1):
        error="failed to open source object: lstat "+str(self.src/name)+": no such file or directory"
        return [{"level":"error", "msg":"Failed to copy: "+error, "object":name, "objectType":"*local.Object"},
                {"level":"error", "msg":"not deleting files as there were IO errors"},
                {"level":"error", "msg":"not deleting directories as there were IO errors"},
                {"level":"error", "msg":"Attempt 1/1 failed with "+str(error_count)+" errors and: "+error},
                {"level":"notice", "stats":{"bytes":8, "errors":error_count, "fatalError":False}},
                {"level":"notice", "msg":"Failed to sync with "+str(error_count)+" errors: "+error}]

    @HOST_RCLONE
    def test_real_queued_source_vanish_is_warning_and_keeps_raw_exit(self):
        (self.src/"tiny.txt").unlink()
        stable=self.src/"a_hold.bin"
        stable.write_bytes(b"x"*(1<<20))
        lost=self.src/"z_vanished.bin"
        lost.write_bytes(b"transient source")
        mirror=self.base/"mirror"
        mirror.mkdir()
        (mirror/"destination_only.bin").write_bytes(b"must be retained when deletion is suppressed")
        script=self.base/"controlled-real-rclone"
        script.write_text('#!/bin/bash\nif [ "$1" = version ]; then exec '+RCLONE+' "$@"; fi\n'
                          'exec '+RCLONE+' "$@" --disable Copy --bwlimit 256k --transfers 1 --check-first --order-by name --retries 1 --low-level-retries 1\n')
        script.chmod(0o700)
        proc=subprocess.Popen(["/bin/bash",str(BACKUP)], env=dict(self.env,BACKUP_RCLONE=str(script)),
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        self.addCleanup(proc.communicate,timeout=12)
        deadline=time.monotonic()+3
        while not list(mirror.glob("a_hold*")) and proc.poll() is None and time.monotonic()<deadline:
            time.sleep(.005)
        self.assertTrue(list(mirror.glob("a_hold*")),"positive control: stable file transfer has started")
        lost.unlink()
        output=proc.communicate(timeout=12)
        self.assertEqual(proc.returncode,0,output)
        value=json.loads(self.heartbeat.read_text())
        self.assertEqual(value["rclone_exit_code"],1)
        self.assertEqual(value["exit_code"],0)
        self.assertIn("source_vanished",{w["kind"] for w in value["warnings"]})
        self.assertIn("destination_deletions_suppressed",{w["kind"] for w in value["warnings"]})
        self.assertEqual((mirror/"a_hold.bin").read_bytes(),stable.read_bytes())
        self.assertTrue((mirror/"destination_only.bin").exists())
        self.assertIn("WARN",self.log.read_text())
        self.assertNotIn("FATAL",self.log.read_text())
        self.assertIn("with warnings",self.status().stdout)

    @HOST_RCLONE
    def test_git_tmp_objects_excluded_and_permanent_objects_and_regular_sock_kept(self):
        objects=self.src/"repo/.git/objects"
        objects.mkdir(parents=True)
        (objects/"tmp_obj_live").write_text("transient")
        (objects/"ab").mkdir()
        (objects/"ab/tmp_obj_nested").write_text("transient nested")
        (objects/"ab/permanent_hash").write_text("durable Git object")
        root_objects=self.src/".git/objects"
        root_objects.mkdir(parents=True)
        (root_objects/"tmp_obj_root").write_text("transient root")
        (root_objects/"ab").mkdir()
        (root_objects/"ab/tmp_obj_root_nested").write_text("transient root nested")
        (root_objects/"ab/permanent_root_hash").write_text("durable root Git object")
        (self.src/"ordinary.sock").write_text("regular file with socket suffix")
        result=self.backup()
        self.assertEqual(result.returncode,0,result.stderr)
        mirror=self.base/"mirror"
        self.assertFalse((mirror/"repo/.git/objects/tmp_obj_live").exists())
        self.assertFalse((mirror/"repo/.git/objects/ab/tmp_obj_nested").exists())
        self.assertTrue((mirror/"repo/.git/objects/ab/permanent_hash").exists())
        self.assertFalse((mirror/".git/objects/tmp_obj_root").exists())
        self.assertFalse((mirror/".git/objects/ab/tmp_obj_root_nested").exists())
        self.assertTrue((mirror/".git/objects/ab/permanent_root_hash").exists())
        self.assertEqual((mirror/"ordinary.sock").read_text(),"regular file with socket suffix")

    @HOST_RCLONE
    def test_native_nonregular_skip_is_recorded_as_warning(self):
        os.mkfifo(self.src/"runtime.sock")
        result=self.backup()
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(self.heartbeat.read_text())
        self.assertIn({"kind":"nonregular_source_skipped", "object":"runtime.sock"},value.get("warnings",[]))
        self.assertIn("with warnings",self.status().stdout)

    def test_mixed_auth_permission_and_destination_enoent_remain_fatal(self):
        for error in ["permission denied", "oauth2: cannot fetch token: invalid_grant",
                      "Failed to copy: open /unrelated-destination/lost.bin: no such file or directory"]:
            with self.subTest(error=error):
                records=self.vanished_records(error_count=2)
                records.insert(1,{"level":"error", "msg":error,"object":"other.bin"})
                result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
                self.assertEqual(result.returncode,1)
                self.assertIn("FATAL",result.stderr)
                self.assertNotEqual(self.status().returncode,0)

    def test_ambiguous_or_unverified_missing_source_remains_fatal(self):
        cases=[self.vanished_records("tiny.txt"),self.vanished_records("../escape.bin"),
               self.vanished_records()[:-2], self.vanished_records()+["{torn"]]
        for records in cases:
            with self.subTest(records=records):
                result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
                self.assertEqual(result.returncode,1)
                self.assertIn("FATAL",result.stderr)
                self.assertNotEqual(self.status().returncode,0)

    def test_non_one_exit_keeps_raw_failure_even_with_vanished_messages(self):
        result=self.backup(BACKUP_RCLONE=self.log_rclone(self.vanished_records(),7))
        self.assertEqual(result.returncode,7)
        self.assertIn("FATAL",result.stderr)
        self.assertNotEqual(self.status().returncode,0)

    def test_verified_vanish_accepts_native_and_counted_terminal_messages(self):
        for counted in [True, False]:
            with self.subTest(counted=counted):
                records=self.vanished_records()
                if not counted:
                    records[-1]["msg"]=records[-1]["msg"].replace(" with 1 errors", "")
                result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
                self.assertEqual(result.returncode,0,result.stderr)
                value=json.loads(self.heartbeat.read_text())
                self.assertEqual(value["rclone_exit_code"],1)
                self.assertEqual(value["bytes_transferred"],8)
                self.assertIn({"kind":"source_vanished", "object":"lost.bin"},value["warnings"])
                self.assertIn("deletions suppressed",self.status().stdout)

    def test_inconsistent_vanish_evidence_remains_fatal(self):
        cases=[]
        for stats in [{"bytes":8,"errors":0,"fatalError":False},
                      {"bytes":8,"errors":2,"fatalError":False},
                      {"bytes":8,"errors":1,"fatalError":True},
                      {"errors":1,"fatalError":False},
                      {"bytes":8,"errors":1,"fatalError":False,"lastError":"permission denied"},
                      {"bytes":8,"errors":1,"fatalError":False,"transferring":[{"name":"active.bin"}]},
                      *({"bytes":8,"errors":1,"fatalError":False,"transferring":bad} for bad in [0,False,"",{}])]:
            records=self.vanished_records()
            records[-2]["stats"]=stats
            cases.append(records)
        records=self.vanished_records()
        records[0]["object"]="mismatched.bin"
        cases.append(records)
        records=self.vanished_records()
        records[-1]["msg"]="Failed to sync: permission denied"
        cases.append(records)
        records=self.vanished_records()
        records.insert(1,{"level":"error","msg":"Failed to delete destination object"})
        cases.append(records)
        cases.append(self.vanished_records()+[{"level":"info","msg":"still running"}])
        for records in cases:
            with self.subTest(records=records):
                result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
                self.assertEqual(result.returncode,1,result.stderr)
                self.assertIn("FATAL",result.stderr)
                self.assertNotEqual(self.status().returncode,0)

    def test_source_symlink_escape_and_inaccessible_source_remain_fatal(self):
        outside=self.base/"outside"
        outside.mkdir()
        (self.src/"escape").symlink_to(outside,target_is_directory=True)
        hidden=self.src/"hidden"
        hidden.mkdir()
        hidden.chmod(0o000)
        try:
            for name in ["escape/lost.bin", "hidden/lost.bin", "/absolute-lost.bin", "a/../lost.bin"]:
                with self.subTest(name=name):
                    result=self.backup(BACKUP_RCLONE=self.log_rclone(self.vanished_records(name)))
                    self.assertEqual(result.returncode,1,result.stderr)
                    self.assertIn("FATAL",result.stderr)
        finally:
            hidden.chmod(0o700)

    def test_valid_json_without_final_newline_cannot_normalize_failure(self):
        fake=self.log_rclone(self.vanished_records())
        script=Path(fake)
        script.write_text(script.read_text().replace("sys.exit(1)\n", "path.write_text(path.read_text().rstrip('\\n'))\nsys.exit(1)\n"))
        result=self.backup(BACKUP_RCLONE=fake)
        self.assertEqual(result.returncode,1,result.stderr)
        self.assertIn("FATAL",result.stderr)

        fake=self.log_rclone(self.vanished_records())
        script=Path(fake)
        script.write_text(script.read_text().replace("sys.exit(1)\n", "Path("+repr(str(self.src))+ ").rename("+repr(str(self.base/"moved-source"))+")\nsys.exit(1)\n"))
        result=self.backup(BACKUP_RCLONE=fake)
        self.assertEqual(result.returncode,1,result.stderr)
        self.assertIn("FATAL",result.stderr)

    def test_recovered_source_vanish_is_visible_without_final_deletion_suppression(self):
        records=self.vanished_records()[:-1]
        records.append({"level":"notice","stats":{"bytes":8,"errors":0,"fatalError":False}})
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records,0))
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(self.heartbeat.read_text())
        self.assertEqual(value.get("rclone_exit_code"),0)
        self.assertIn({"kind":"source_vanished","object":"lost.bin"},value["warnings"])
        self.assertNotIn({"kind":"destination_deletions_suppressed"},value["warnings"])
        self.assertIn("with warnings",self.status().stdout)

    def test_classifier_failure_keeps_successful_raw_rclone_exit(self):
        python=self.base/"classification-fails"
        python.write_text('#!/bin/bash\nif [ "$2" = classify ]; then exit 5; fi\nexec /usr/bin/python3 "$@"\n')
        python.chmod(0o700)
        settings = {"BACKUP_PYTHON": str(python)}
        if NO_RCLONE:
            settings["BACKUP_RCLONE"] = self.log_rclone(
                [{"level": "notice", "stats": {"bytes": 8, "errors": 0, "fatalError": False}}], 0)
        result=self.backup(**settings)
        self.assertEqual(result.returncode,1,result.stderr)
        self.assertEqual(json.loads(self.heartbeat.read_text())["rclone_exit_code"],0)
        self.assert_bad("failed")

    def test_malformed_stats_do_not_reuse_earlier_bytes(self):
        records=[{"level":"notice","stats":{"bytes":8,"errors":0,"fatalError":False}},
                 {"level":"notice","stats":{"bytes":"torn","errors":0,"fatalError":False}}]
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records,0))
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(self.heartbeat.read_text())
        self.assertIsNone(value["bytes_transferred"])
        self.assertEqual(value["stats_status"],"malformed")
        self.assertIn("with warnings",self.status().stdout)

    def test_duplicate_fields_and_non_json_constants_cannot_hide_errors(self):
        for extra in ['{"level":"error","level":"notice","msg":"permission denied"}',
                      '{"level":"info","msg":"invalid JSON","size":NaN}']:
            with self.subTest(extra=extra):
                records=self.vanished_records()
                records.insert(1,extra)
                result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
                self.assertEqual(result.returncode,1,result.stderr)
                self.assertIn("FATAL",result.stderr)

    def test_each_retry_has_its_own_error_count_and_suppression_proof(self):
        records=self.vanished_records()[:-2]+self.vanished_records()
        records[3]["msg"]=records[3]["msg"].replace("1/1", "1/2")
        records[7]["msg"]=records[7]["msg"].replace("1/1", "2/2")
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(self.heartbeat.read_text())
        self.assertEqual(value["rclone_exit_code"],1)
        self.assertEqual(value["warnings"].count({"kind":"source_vanished","object":"lost.bin"}),1)
        # Exact Astra negative input: remove both first-attempt suppression records.
        for removed in [(1, 2), (1,), (2,), (5, 6), (5,), (6,)]:
            with self.subTest(removed=removed):
                negative = [item for index, item in enumerate(records) if index not in removed]
                result = self.backup(BACKUP_RCLONE=self.log_rclone(negative))
                self.assertEqual(result.returncode, 1, "each attempt boundary needs both suppression records: "+result.stderr)
                self.assertIn("FATAL", result.stderr)
                self.assert_bad("failed")

    def test_zero_exit_dry_run_or_skipped_operations_cannot_be_success(self):
        for message in ["Skipped copy as --dry-run is set", "Skipped delete", "Skipping move"]:
            with self.subTest(message=message):
                records = [{"level":"notice", "msg":message, "object":"tiny.txt", "size":8},
                           {"level":"notice", "stats":{"bytes":8,"errors":0,"fatalError":False}}]
                result = self.backup(BACKUP_RCLONE=self.log_rclone(records, 0))
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("FATAL", result.stderr)
                self.assert_bad("failed")

    def test_stats_before_final_attempt_do_not_prove_completion(self):
        records=self.vanished_records()
        records.insert(3,records.pop(-2))
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
        self.assertEqual(result.returncode,1,result.stderr)
        self.assertIn("FATAL",result.stderr)

    def test_native_warning_on_success_is_visible(self):
        records=[{"level":"warning","msg":"partial source notice","object":"fixture.bin"},
                 {"level":"notice","stats":{"bytes":8,"errors":0,"fatalError":False}}]
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records,0))
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(self.heartbeat.read_text())
        self.assertIn({"kind":"rclone_warning","message":"partial source notice","object":"fixture.bin"},value["warnings"])
        self.assertIn("WARN",result.stderr)
        self.assertIn("with warnings",self.status().stdout)

    def test_vanished_parent_is_warning_but_dangling_symlink_escape_is_fatal(self):
        records=self.vanished_records("removed-parent/lost.bin")
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(self.heartbeat.read_text())["rclone_exit_code"],1)
        (self.src/"removed-parent").symlink_to(self.base/"absent-outside",target_is_directory=True)
        result=self.backup(BACKUP_RCLONE=self.log_rclone(records))
        self.assertEqual(result.returncode,1,result.stderr)
        self.assertIn("FATAL",result.stderr)


class LaunchReceiptTest(Fixture):
    def setUp(self):
        super().setUp()
        self.home = self.base/"home"
        self.heartbeat = self.home/"Library/Logs/memit-gdrive-backup/last_run.json"
        self.heartbeat.parent.mkdir(parents=True)
        counter = self.home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
        counter.parent.mkdir(parents=True)
        counter.write_text("0\n")

    def launch(self, wrapper, *, error_number=None, env=None):
        text = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
        literals = {name: json.loads(literal) for name, literal in
                    re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', text, re.M)}
        if "launchShell" in literals:
            # Execute the same literal composition passed to /bin/sh by the applet.
            if error_number is None:
                body, args = literals.get("generationShell", "")+literals["launchShell"]+literals["receiptShell"], [str(wrapper)]
            else:
                body, args = literals.get("generationShell", "")+literals["receiptShell"], [str(wrapper), "", str(error_number)]
        else:
            # Execute MB6's original shell command for its behavioral RED baseline.
            command = next(line.strip()[len("do shell script "):] for line in text.splitlines()
                           if line.strip().startswith("do shell script "))
            body = json.loads(command).replace(
                "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/code/ops/backup/backup_gdrive.sh",
                shlex.quote(str(wrapper)))
            args = []
        environment = dict(os.environ, **(env or {}))
        environment["HOME"] = str(self.home)
        return run_process(["/bin/sh", "-c", body, "backup-launch", *args],
                           env=environment, timeout=5)

    def test_absent_wrapper_launch_fails_fresh_success_promptly(self):
        self.write_heartbeat()
        self.assertEqual(self.status().returncode, 0, "positive control: previous success is fresh")
        previous = self.heartbeat.read_bytes()
        wrapper = self.base/"absent-volume/backup_gdrive.sh"
        start = time.monotonic()
        result = self.launch(wrapper)
        self.assertLess(time.monotonic()-start, 5)
        self.assert_bad("launch")
        receipt = json.loads((self.heartbeat.parent/"launch_receipt.json").read_text())
        self.assertEqual(receipt["exit_code"], 127)
        self.assertIsNone(receipt["error_number"])
        self.assertEqual(receipt["wrapper_path"], str(wrapper))
        self.assertGreater(dt.datetime.fromisoformat(receipt["utc"].replace("Z", "+00:00")),
                           dt.datetime.fromisoformat(json.loads(previous)["end"]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.heartbeat.read_bytes(), previous)

    def test_exit_75_launch_preserves_real_active_owner_and_inflight_status(self):
        owner, env = self.hold_live_owner()
        previous = self.heartbeat.read_bytes()
        result = self.launch(BACKUP, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.heartbeat.parent/"launch_receipt.json"
        self.assertTrue(receipt.is_file(), "a refused launch still needs its internal-disk receipt")
        self.assertEqual(json.loads(receipt.read_text())["exit_code"], 75)
        self.assertIsNone(owner.poll())
        self.assert_bad("incomplete")
        self.assertNotIn("failed", self.status().stdout)
        self.assertEqual(self.heartbeat.read_bytes(), previous)

    def test_launch_receipt_is_atomically_replaced_and_stays_one_file(self):
        wrapper = self.base/"wrapper 'quoted' \"back\\slash\".sh"
        wrapper.write_text("#!/bin/sh\nexit 0\n")
        self.write_heartbeat(end=None, exit_code=None, owner_pid=os.getpid())
        previous = self.heartbeat.read_bytes()
        path = self.heartbeat.parent/"launch_receipt.json"
        inode = None
        for invocation in range(20):
            result = self.launch(wrapper)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(path.is_file(), "launch must publish a receipt even without a wrapper heartbeat")
            value = json.loads(path.read_text())
            self.assertEqual(value["wrapper_path"], str(wrapper))
            self.assertEqual(value["exit_code"], 0)
            self.assertIsNone(value["error_number"])
            self.assertNotEqual(path.stat().st_ino, inode, "publication must replace the file, not truncate it")
            inode = path.stat().st_ino
        self.assertEqual({p.name for p in path.parent.iterdir()}, {"last_run.json", "launch_receipt.json"})
        self.assertEqual(self.heartbeat.read_bytes(), previous)
        self.assert_bad("incomplete")

    def test_applescript_error_receipt_runs_without_executing_wrapper(self):
        self.write_heartbeat()
        previous = self.heartbeat.read_bytes()
        marker = self.base/"must-not-run"
        wrapper = self.base/"volume-wrapper.sh"
        wrapper.write_text('#!/bin/sh\nprintf invoked > '+shlex.quote(str(marker))+'\n')
        result = self.launch(wrapper, error_number=-1708)
        self.assert_bad("launch")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists(), "the error-receipt path must not execute volume-hosted code")
        value = json.loads((self.heartbeat.parent/"launch_receipt.json").read_text())
        self.assertIsNone(value["exit_code"])
        self.assertEqual(value["error_number"], -1708)
        self.assertEqual(self.heartbeat.read_bytes(), previous)

    def test_receipt_write_failure_is_prompt_and_preserves_existing_files(self):
        self.write_heartbeat()
        receipt = self.write_launch_receipt(exit_code=0)
        previous, heartbeat = receipt.read_bytes(), self.heartbeat.read_bytes()
        wrapper = self.base/"success.sh"
        wrapper.write_text("#!/bin/sh\nexit 0\n")
        receipt.parent.chmod(0o555)
        try:
            start = time.monotonic()
            result = self.launch(wrapper)
            self.assertNotEqual(result.returncode, 0, "shell receipt failure must reach the applet's caught error boundary")
            self.assertLess(time.monotonic()-start, 5)
            self.assertEqual(receipt.read_bytes(), previous)
            self.assertEqual(self.heartbeat.read_bytes(), heartbeat)
            self.assertFalse(list(receipt.parent.glob(".launch-receipt.*")))
        finally:
            receipt.parent.chmod(0o700)


class GenerationStatusTest(Fixture):
    def setUp(self):
        super().setUp()
        self.counter = self.heartbeat.parent.parent/"memit-gdrive-backup-launch-state/counter"
        self.counter.parent.mkdir()
        self.counter.write_text("10\n")
        self.journal = self.heartbeat.parent.parent/"memit-gdrive-backup-launch-journal/failures.jsonl"
        self.ordered_heartbeat()

    def ordered_heartbeat(self, generation=10, **changes):
        self.write_heartbeat(launch_generation=generation, launch_mode="applet" if generation else "manual", **changes)

    def ordered_receipt(self, generation=11, **changes):
        self.counter.write_text(str(generation)+"\n")
        return self.write_launch_receipt(launch_generation=generation, **changes)

    def marker(self, generation=11, **changes):
        self.counter.write_text(str(generation)+"\n")
        self.journal.parent.mkdir(exist_ok=True)
        value = {"schema": 1, "launch_generation": generation, "reason": "receipt publication failed"}
        value.update(changes)
        self.journal.write_text(json.dumps(value)+"\n")

    def test_clock_rollback_failure_is_newer_by_generation(self):
        self.assertEqual(self.status().returncode, 0)
        end = json.loads(self.heartbeat.read_text())["end"]
        earlier = (dt.datetime.fromisoformat(end)-dt.timedelta(seconds=1)).isoformat()
        self.ordered_receipt(utc=earlier)
        self.assert_bad("launch")

    def test_equal_timestamp_failure_needs_equal_or_later_completed_generation(self):
        end = json.loads(self.heartbeat.read_text())["end"]
        self.ordered_receipt(utc=end)
        self.assert_bad("launch")
        self.ordered_heartbeat(11, end=end)
        self.assertEqual(self.status().returncode, 0)

    def test_later_wall_time_cannot_clear_failure(self):
        end = json.loads(self.heartbeat.read_text())["end"]
        self.ordered_receipt(utc=end)
        self.ordered_heartbeat(10)
        self.assert_bad("launch")

    def test_incomplete_equal_generation_does_not_acknowledge_failure(self):
        self.ordered_receipt()
        self.ordered_heartbeat(11, start=dt.datetime.now(dt.timezone.utc).isoformat(),
                               end=None, exit_code=None, owner_pid=os.getpid())
        self.assert_bad("launch")
        self.ordered_heartbeat(11)
        self.assertEqual(self.status().returncode, 0)

    def test_missing_or_malformed_receipt_generation_is_ambiguous(self):
        end = json.loads(self.heartbeat.read_text())["end"]
        for generation in [None, True, "11", 0, -1, 2147483648]:
            with self.subTest(generation=generation):
                self.write_launch_receipt(launch_generation=generation, utc=end, exit_code=0)
                self.assert_bad("generation")
        path = self.write_launch_receipt(utc=end, exit_code=0)
        self.assertNotIn("launch_generation", json.loads(path.read_text()))
        self.assert_bad("generation")

    def test_malformed_heartbeat_generation_is_ambiguous(self):
        for generation in [True, "10", 0, -1, 2147483648]:
            with self.subTest(generation=generation):
                self.ordered_heartbeat(generation)
                self.assert_bad("generation")

    def test_missing_corrupt_or_decreasing_counter_is_unhealthy(self):
        self.assertEqual(self.status().returncode, 0)
        self.counter.unlink()
        self.assert_bad("counter")
        for content in ["torn\n", "0\n", "9\n", "10.0\n", "2147483648\n"]:
            with self.subTest(content=content):
                self.counter.write_text(content)
                self.assert_bad("counter")

    def test_issued_launch_without_receipt_is_unhealthy(self):
        self.counter.write_text("11\n")
        self.assert_bad("generation")

    def test_manual_heartbeat_is_explicit_and_cannot_clear_applet_failure(self):
        self.counter.unlink()
        self.ordered_heartbeat(None)
        result = self.status()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("manual/unsequenced", result.stdout)
        self.ordered_receipt()
        self.assert_bad("manual/unsequenced")
        self.ordered_heartbeat(11)
        self.assertEqual(self.status().returncode, 0)

    def test_journal_failure_needs_completed_generation(self):
        self.ordered_receipt(10, exit_code=0)
        self.marker()
        self.assert_bad("journal")
        self.ordered_heartbeat(11, end=None, exit_code=None, owner_pid=os.getpid())
        self.assert_bad("journal")
        self.ordered_heartbeat(11)
        self.assertEqual(self.status().returncode, 0)

    def test_malformed_journal_cannot_report_success(self):
        self.journal.parent.mkdir()
        for content in ["", "{torn\n", "{}\n", "[]\n",
                        json.dumps({"schema": 1, "launch_generation": None, "reason": "failed"})+"\n",
                        json.dumps({"schema": 1, "launch_generation": 11, "reason": "failed"})+"\n"]:
            with self.subTest(content=content):
                self.journal.write_text(content)
                self.assert_bad("journal")

    def test_refused_contender_does_not_acknowledge_journal_failure(self):
        self.marker()
        self.ordered_receipt(12, exit_code=75)
        self.assert_bad("journal")


    def test_json_null_launch_receipt_cannot_be_ignored(self):
        (self.heartbeat.parent/"launch_receipt.json").write_text("null\n")
        self.assert_bad("launch")


class GenerationLaunchTest(Fixture):
    launch = LaunchReceiptTest.launch

    def setUp(self):
        super().setUp()
        self.home = self.base/"home"
        self.heartbeat = self.home/"Library/Logs/memit-gdrive-backup/last_run.json"
        self.heartbeat.parent.mkdir(parents=True)
        self.counter = self.home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
        self.counter.parent.mkdir()
        self.counter.write_text("0\n")
        self.journal = self.home/"Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl"

    def success_baseline(self):
        self.counter.write_text("10\n")
        self.write_heartbeat(launch_generation=10, launch_mode="applet")
        self.write_launch_receipt(launch_generation=10, exit_code=0)
        self.assertEqual(self.status().returncode, 0, "positive control: fresh completed generation 10")

    def test_generation_is_incremented_and_passed_to_wrapper_and_receipt(self):
        marker = self.base/"generations"
        wrapper = self.base/"stub.sh"
        wrapper.write_text('#!/bin/sh\nprintf "%s\\n" "${BACKUP_LAUNCH_GENERATION:-missing}" >> '+shlex.quote(str(marker))+'\n')
        for generation in (1, 2):
            result = self.launch(wrapper)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(marker.read_text().splitlines()[-1], str(generation))
            self.assertEqual(self.counter.read_text().strip(), str(generation))
            self.assertEqual(json.loads((self.heartbeat.parent/"launch_receipt.json").read_text())["launch_generation"], generation)

    def test_missing_corrupt_or_rolled_back_counter_refuses_wrapper(self):
        self.success_baseline()
        marker = self.base/"must-not-dispatch"
        wrapper = self.base/"stub.sh"
        wrapper.write_text('#!/bin/sh\nprintf ran > '+shlex.quote(str(marker))+'\n')
        for content in [None, "broken\n", "9\n", "2147483647\n"]:
            with self.subTest(content=content):
                if self.counter.exists():
                    self.counter.unlink()
                if content is not None:
                    self.counter.write_text(content)
                self.launch(wrapper)
                self.assertFalse(marker.exists(), "ambiguous allocation must refuse dispatch")
                self.assert_bad("generation")

    def test_concurrent_launches_allocate_unique_generations(self):
        marker = self.base/"generations"
        wrapper = self.base/"stub.sh"
        wrapper.write_text('#!/bin/sh\nprintf "%s\\n" "${BACKUP_LAUNCH_GENERATION:-0}" >> '+shlex.quote(str(marker))+'\n')
        text = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
        literals = {name: json.loads(literal) for name, literal in re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', text, re.M)}
        body = literals.get("generationShell", "")+literals["launchShell"]+literals["receiptShell"]
        procs = [subprocess.Popen(["/bin/sh", "-c", body, "backup-launch", str(wrapper)],
                                 env=dict(os.environ, HOME=str(self.home)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for _ in range(12)]
        for proc in procs:
            stdout, stderr = proc.communicate(timeout=5)
            self.assertEqual(proc.returncode, 0, stdout+stderr)
        self.assertEqual(sorted(map(int, marker.read_text().splitlines())), list(range(1, 13)))
        self.assertEqual(self.counter.read_text().strip(), "12")

    def test_absent_wrapper_and_0555_receipt_directory_publish_independent_journal(self):
        self.success_baseline()
        receipt = self.heartbeat.parent/"launch_receipt.json"
        prior, heartbeat = receipt.read_bytes(), self.heartbeat.read_bytes()
        receipt.parent.chmod(0o555)
        try:
            result = self.launch(self.base/"absent-volume/backup_gdrive.sh")
            self.assertNotEqual(result.returncode, 0)
            self.assert_bad("journal")
            self.assertEqual(receipt.read_bytes(), prior)
            self.assertEqual(self.heartbeat.read_bytes(), heartbeat)
            value = json.loads(self.journal.read_text().splitlines()[-1])
            self.assertEqual(value["launch_generation"], 11)
            self.assertIn("publication", value["reason"])
            self.assertNotEqual(self.journal.parent, receipt.parent)
        finally:
            receipt.parent.chmod(0o700)

    def test_both_failure_sinks_unwritable_leave_unacknowledged_generation(self):
        self.success_baseline()
        self.journal.parent.mkdir()
        self.journal.parent.chmod(0o555)
        self.heartbeat.parent.chmod(0o555)
        try:
            self.launch(self.base/"absent/backup_gdrive.sh")
            self.assert_bad("generation")
            self.assertEqual(self.counter.read_text().strip(), "11")
            self.assertFalse(self.journal.exists())
        finally:
            self.heartbeat.parent.chmod(0o700)
            self.journal.parent.chmod(0o700)

    def test_failure_journal_is_bounded_and_keeps_newest_generation(self):
        self.success_baseline()
        self.heartbeat.parent.chmod(0o555)
        try:
            for _ in range(80):
                self.launch(self.base/"absent/backup_gdrive.sh")
            self.assertTrue(self.journal.is_file(), "failure journal must exist independently")
            markers = [json.loads(line) for line in self.journal.read_text().splitlines()]
            self.assertLessEqual(len(markers), 64)
            self.assertEqual(max(value["launch_generation"] for value in markers), 90)
            self.assertLessEqual(self.journal.stat().st_size, 65536)
            self.assert_bad("journal")
        finally:
            self.heartbeat.parent.chmod(0o700)

    def test_success_receipt_alone_does_not_clear_prior_failure(self):
        self.write_heartbeat(launch_generation=None, launch_mode="manual")
        self.launch(self.base/"absent/backup_gdrive.sh")
        wrapper = self.base/"success.sh"
        wrapper.write_text("#!/bin/sh\nexit 0\n")
        self.launch(wrapper)
        self.assert_bad("journal")
        self.write_heartbeat(launch_generation=2, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)

    def test_allocator_refuses_string_generation_evidence(self):
        self.success_baseline()
        marker = self.base/"must-not-dispatch"
        wrapper = self.base/"stub.sh"
        wrapper.write_text('#!/bin/sh\nprintf ran > '+shlex.quote(str(marker))+'\n')
        self.write_launch_receipt(launch_generation="10", exit_code=0)
        self.launch(wrapper)
        self.assertFalse(marker.exists(), "JSON strings are not integer generations")
        self.assert_bad("generation")

    def test_unwritable_journal_refusal_cannot_hide_uncompleted_failure(self):
        self.success_baseline()
        self.journal.parent.mkdir()
        self.journal.parent.chmod(0o555)
        try:
            self.launch(self.base/"absent/backup_gdrive.sh")
            self.assert_bad("launch")
            failed = (self.heartbeat.parent/"launch_receipt.json").read_bytes()
            wrapper = self.base/"refused.sh"
            wrapper.write_text("#!/bin/sh\nexit 75\n")
            self.launch(wrapper)
            self.assert_bad("launch")
            self.assertEqual((self.heartbeat.parent/"launch_receipt.json").read_bytes(), failed)
            self.write_heartbeat(launch_generation=12, launch_mode="applet")
            self.assertEqual(self.status().returncode, 0)
        finally:
            self.journal.parent.chmod(0o700)


    def shell_literal(self, name, *args):
        text = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
        literals = {key: json.loads(value) for key, value in
                    re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', text, re.M)}
        return run_process(["/bin/sh", "-c", literals[name], "backup-fixture", *map(str, args)],
                           env=dict(os.environ, HOME=str(self.home)), timeout=5)

    def recover(self, floor=10):
        return run_process([sys.executable, "-B", str(STATUS), "recover", "--heartbeat", str(self.heartbeat),
                            "--generation-floor", str(floor)], timeout=5)

    def test_1_manual_interleave_preserves_counter_only_generation_11(self):
        self.success_baseline()
        self.journal.parent.mkdir()
        self.journal.parent.chmod(0o555)
        self.heartbeat.parent.chmod(0o555)
        try:
            self.launch(self.base/"absent/backup_gdrive.sh")
            self.assertEqual(self.counter.read_text().strip(), "11")
            self.assertFalse(self.journal.exists())
            self.heartbeat.parent.chmod(0o700)
            owner, env = self.hold_live_owner()
            prior = self.heartbeat.read_bytes()
            result = self.launch(BACKUP, env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads((self.heartbeat.parent/"launch_receipt.json").read_text())
            self.assertEqual((receipt["launch_generation"], receipt["exit_code"]), (12, 75))
            self.assertEqual(self.heartbeat.read_bytes(), prior)
            self.assertIsNone(owner.poll())
            with (self.base/"owner-release.fifo").open("w") as stream:
                stream.write("release\n")
            stdout, stderr = owner.communicate(timeout=5)
            self.assertEqual(owner.returncode, 0, stdout+stderr)
            self.assertIsNone(json.loads(self.heartbeat.read_text())["launch_generation"])
            self.assert_bad("generation 11")
        finally:
            self.heartbeat.parent.chmod(0o700)
            self.journal.parent.chmod(0o700)

    def test_2_crash_after_allocation_then_refusal_preserves_generation_11(self):
        self.success_baseline()
        previous = (self.heartbeat.parent/"launch_receipt.json").read_bytes()
        text = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
        literal = re.search(r'^property generationShell : ("(?:\\.|[^"\\])*")$', text, re.M)[1]
        result = run_process(["/bin/sh", "-c", json.loads(literal)+"/bin/kill -KILL $$\n"],
                             env=dict(os.environ, HOME=str(self.home)), timeout=5)
        self.assertEqual(result.returncode, -9)
        self.assertEqual(self.counter.read_text().strip(), "11")
        self.assertEqual((self.heartbeat.parent/"launch_receipt.json").read_bytes(), previous)
        self.assertFalse(self.journal.exists())
        wrapper = self.base/"refused.sh"
        wrapper.write_text("#!/bin/sh\nexit 75\n")
        self.assertEqual(self.launch(wrapper).returncode, 0)
        self.assert_bad("generation 11")

    def test_3_refusal_discharges_only_itself_and_completed_generations_resolve_set(self):
        self.success_baseline()
        for generation in (11, 12, 13):
            result = self.shell_literal("generationShell")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(int(result.stdout), generation)
        result = self.shell_literal("receiptShell", BACKUP, 75, "", 12)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_bad("generation 11")
        state = json.loads((self.counter.parent/"unresolved.json").read_text())
        self.assertEqual(state["unresolved"], [[11, 11], [13, 13]])
        self.write_heartbeat(launch_generation=None, launch_mode="manual")
        self.assert_bad("generation 11")
        self.write_heartbeat(launch_generation=10, launch_mode="applet")
        self.assert_bad("generation 11")
        self.write_heartbeat(launch_generation=13, launch_mode="applet", end=None, exit_code=None)
        self.assertNotEqual(self.status().returncode, 0)
        self.write_heartbeat(launch_generation=11, launch_mode="applet")
        self.assert_bad("generation 13")
        self.write_heartbeat(launch_generation=13, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)

    def test_3_corrupt_unresolved_set_refuses_dispatch(self):
        self.success_baseline()
        self.assertEqual(self.shell_literal("generationShell").returncode, 0)
        (self.counter.parent/"unresolved.json").write_text("{torn\n")
        marker = self.base/"must-not-dispatch"
        wrapper = self.base/"stub.sh"
        wrapper.write_text('#!/bin/sh\nprintf ran > '+shlex.quote(str(marker))+'\n')
        self.launch(wrapper)
        self.assertFalse(marker.exists(), "corrupt unresolved generations must refuse dispatch")
        self.assert_bad("unresolved")

    def test_4_recovery_preserves_null_evidence_and_requires_sequenced_completion(self):
        self.success_baseline()
        self.assertEqual(self.shell_literal("generationShell").returncode, 0)
        self.counter.write_text("corrupt\n")
        marker = self.base/"dispatched-generation"
        wrapper = self.base/"stub.sh"
        wrapper.write_text('#!/bin/sh\nprintf "%s" "$BACKUP_LAUNCH_GENERATION" > '+shlex.quote(str(marker))+'\n')
        self.assertNotEqual(self.launch(wrapper).returncode, 0)
        result = self.shell_literal("receiptShell", wrapper, "", 1, "")
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = self.heartbeat.parent/"launch_receipt.json"
        self.assertIsNone(json.loads(receipt.read_text())["launch_generation"])
        prior = {"launch_receipt.json": receipt.read_bytes(), "failures.jsonl": self.journal.read_bytes()}
        self.counter.write_text("10\n")
        self.assertNotEqual(self.launch(wrapper).returncode, 0)
        self.assertFalse(marker.exists())
        result = self.recover(11)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        archives = list((self.counter.parent/"recoveries").iterdir())
        self.assertEqual(len(archives), 1)
        for name, data in prior.items():
            self.assertEqual((archives[0]/name).read_bytes(), data, "ambiguous evidence must survive byte-for-byte")
        barrier = int(self.counter.read_text())
        self.assertGreater(barrier, 11, "recovery must retain the generation lost from the repaired counter")
        self.assertEqual(self.launch(wrapper).returncode, 0)
        generation = int(marker.read_text())
        self.assertGreater(generation, barrier)
        self.assert_bad("recovery barrier")
        self.write_heartbeat(launch_generation=None, launch_mode="manual")
        self.assert_bad("recovery barrier")
        self.write_heartbeat(launch_generation=generation, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)

    def test_4_null_evidence_publication_waits_for_recovery_counter_lock(self):
        self.success_baseline()
        text = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
        literal = re.search(r'^property receiptShell : ("(?:\\.|[^"\\])*")$', text, re.M)[1]
        entered = self.base/"publisher-entered"
        body = 'touch '+shlex.quote(str(entered))+'\n'+json.loads(literal)
        with (self.counter.parent/"counter.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            proc = subprocess.Popen(["/bin/sh", "-c", body, "backup-receipt", str(BACKUP), "", "1", ""],
                                    env=dict(os.environ, HOME=str(self.home)),
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.addCleanup(proc.communicate, timeout=5)
            deadline = time.monotonic()+3
            while not entered.exists() and proc.poll() is None and time.monotonic()<deadline:
                time.sleep(0.01)
            self.assertTrue(entered.exists(), "positive control: publisher process started")
            time.sleep(0.15)
            self.assertIsNone(proc.poll(), "null-generation evidence must serialize with recovery")
        stdout, stderr = proc.communicate(timeout=5)
        self.assertEqual(proc.returncode, 0, stdout+stderr)
        self.assertIsNone(json.loads((self.heartbeat.parent/"launch_receipt.json").read_text())["launch_generation"])

    def test_4_missing_counter_and_repeated_recovery_keep_monotonic_barriers(self):
        self.success_baseline()
        self.counter.unlink()
        self.assertNotEqual(self.shell_literal("generationShell").returncode, 0)
        self.assertEqual(self.shell_literal("receiptShell", BACKUP, "", 1, "").returncode, 0)
        result = self.recover(20)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        first = int(self.counter.read_text())
        archives = self.counter.parent/"recoveries"
        original = {str(path.relative_to(archives)): path.read_bytes() for path in archives.rglob("*") if path.is_file()}
        self.counter.write_text("10\n")
        result = self.recover(0)
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(self.counter.read_text(), "10\n")
        result = self.recover(first)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertGreater(int(self.counter.read_text()), first)
        for name, data in original.items():
            self.assertEqual((archives/name).read_bytes(), data)
        self.assert_bad("recovery barrier")

class R5Fixture(Fixture):
    success_baseline = GenerationLaunchTest.success_baseline
    shell_literal = GenerationLaunchTest.shell_literal
    recover = GenerationLaunchTest.recover
    launch = LaunchReceiptTest.launch

    def setUp(self):
        super().setUp()
        self.heartbeat = self.home/"Library/Logs/memit-gdrive-backup/last_run.json"
        self.heartbeat.parent.mkdir(parents=True)
        self.counter = self.home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
        self.counter.parent.mkdir()
        self.counter.write_text("0\n")
        self.journal = self.home/"Library/Logs/memit-gdrive-backup-launch-journal/failures.jsonl"


class R5RecoveryTest(R5Fixture):
    def damaged_history(self, torn):
        self.success_baseline()
        self.counter.write_text("corrupt\n")
        self.write_launch_receipt(launch_generation=None)
        self.journal.parent.mkdir()
        self.journal.write_bytes(b'{"schema":1,"launch_generation":100,"reason":"failed launch"}\n'+
                                 (b'{torn\n' if torn else b''))

    def snapshot(self):
        logs = self.home/"Library/Logs"
        return {str(p.relative_to(logs)): p.read_bytes() if p.is_file() else None
                for p in sorted(logs.rglob("*"))}

    def assert_low_floor_refused_unchanged(self, floor=10):
        before = self.snapshot()
        result = self.recover(floor)
        self.assertEqual(self.snapshot(), before, "low floor must not write or move any recovery evidence")
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("observed", result.stderr)

    def test_1_torn_journal_preserves_generation_and_entire_ambiguous_file(self):
        self.damaged_history(True)
        self.assert_low_floor_refused_unchanged()
        original = self.journal.read_bytes()
        result = self.recover(100)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        archive, = (self.counter.parent/"recoveries").iterdir()
        self.assertEqual((archive/"failures.jsonl").read_bytes(), original)
        self.assertEqual(int(self.counter.read_text()), 101)
        # Criterion 3: recovery and a manual completion cannot discharge the barrier.
        self.assert_bad("recovery barrier generation 101")
        self.write_heartbeat(launch_generation=None, launch_mode="manual")
        self.assert_bad("recovery barrier generation 101")
        self.write_heartbeat(launch_generation=12, launch_mode="applet")
        self.assert_bad("recovery barrier generation 101")
        self.write_heartbeat(launch_generation=101, launch_mode="applet")
        self.assert_bad("recovery barrier generation 101")
        result = self.shell_literal("generationShell")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(int(result.stdout), 102)
        self.write_heartbeat(launch_generation=102, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)
        self.assertEqual((archive/"failures.jsonl").read_bytes(), original)

    def test_1_valid_generation_after_torn_line_still_counts(self):
        self.damaged_history(True)
        with self.journal.open("ab") as stream:
            stream.write(b'{"schema":1,"launch_generation":103,"reason":"failed"}\n')
        original = self.journal.read_bytes()
        self.assert_low_floor_refused_unchanged(100)
        result = self.recover(103)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(int(self.counter.read_text()), 104)
        archive, = (self.counter.parent/"recoveries").iterdir()
        self.assertEqual((archive/"failures.jsonl").read_bytes(), original)
        self.assert_bad("recovery barrier generation 104")

    def test_2_floor_below_valid_journal_is_read_only(self):
        self.damaged_history(False)
        self.assert_low_floor_refused_unchanged()

    def test_2_floor_below_torn_journal_is_read_only(self):
        self.damaged_history(True)
        self.assert_low_floor_refused_unchanged()


    def test_r6_1_mb14_archive_requires_floor_100_and_completion_102(self):
        self.success_baseline()
        fixture = ROOT/"_archive/projects/backup-gdrive/backup_gdrive_mb21_20261010T191747Z/mb14_fixture"
        rows = json.loads((fixture.parent/"mb14_fixture_tree_sha256.json").read_text())
        for row in rows:
            if row["kind"] == "file":
                self.assertEqual(hashlib.sha256((fixture/row["path"]).read_bytes()).hexdigest(), row["sha256"])
        shutil.copytree(fixture/"recoveries", self.counter.parent/"recoveries")
        for name in ("counter", "unresolved.json", "counter.lock"):
            (self.counter.parent/name).write_bytes((fixture/name).read_bytes())
        (self.heartbeat.parent/"launch_receipt.json").unlink()
        archived = {name: data for name, data in self.snapshot().items() if "/recoveries/" in name}
        self.assert_low_floor_refused_unchanged(11)
        result = self.recover(100)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(self.counter.read_bytes(), b"101\n")
        self.assertEqual(json.loads((self.counter.parent/"unresolved.json").read_text())["recovery_barrier"], 101)
        self.write_heartbeat(launch_generation=13, launch_mode="applet")
        self.assert_bad("recovery barrier generation 101")
        allocated = self.shell_literal("generationShell")
        self.assertEqual(allocated.returncode, 0, allocated.stderr)
        self.assertEqual(int(allocated.stdout), 102)
        self.write_heartbeat(launch_generation=102, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)
        after = self.snapshot()
        self.assertEqual({name: after[name] for name in archived}, archived)

    def test_r6_1_every_archived_source_in_older_directories_counts(self):
        self.success_baseline()
        self.counter.write_text("corrupt\n")
        self.write_launch_receipt(launch_generation=None)
        archives = self.counter.parent/"recoveries"
        older = archives/"20000101T000000Z"
        for directory in (older, archives/"20990101T000000Z"):
            directory.mkdir(parents=True)
            (directory/"manifest.json").write_text(json.dumps({"recovery_barrier": 11, "highest_seen": 10}))
        sources = (("counter", b"100\n", 100),
                   ("last_run.json", b'{"launch_generation":110}\n', 110),
                   ("launch_receipt.json", b'{"launch_generation":120}\n', 120),
                   ("failures.jsonl", b'{"launch_generation":130}\n{torn\n', 130),
                   ("failures.jsonl", b'{"launch_generation":130}\n{torn\n{"launch_generation":140}\n', 140))
        for name, data, generation in sources:
            with self.subTest(source=name, generation=generation):
                (older/name).write_bytes(data)
                before = {str(p.relative_to(archives)): p.read_bytes() for p in archives.rglob("*") if p.is_file()}
                self.assert_low_floor_refused_unchanged(generation-1)
                result = self.recover(generation)
                self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                self.assertEqual(int(self.counter.read_text()), generation+1)
                for relative, preserved in before.items():
                    self.assertEqual((archives/relative).read_bytes(), preserved)

    def assert_under_lock_rechecked(self, evidence, floor):
        from tools import backup_gdrive_status as status
        (self.counter.parent/"counter.lock").write_bytes(b"")
        observed = []

        def inject(_lock, _operation):
            evidence.parent.mkdir(parents=True, exist_ok=True)
            evidence.write_bytes(b'{"launch_generation":100}\n{torn\n' if evidence.suffix == ".jsonl" else
                                 b'{"launch_generation":100,"exit_code":75}\n')
            observed.append(self.snapshot())

        with mock.patch.object(status.fcntl, "flock", side_effect=inject):
            with self.assertRaisesRegex(ValueError, "below observed maximum 100"):
                status.recover(SimpleNamespace(heartbeat=str(self.heartbeat), generation_floor=floor))
        self.assertEqual(len(observed), 1, "positive control: history changed after the pre-lock check")
        self.assertEqual(self.snapshot(), observed[0], "under-lock refusal must leave injected evidence unchanged")

    def test_r6_1_under_lock_rechecks_archived_journal(self):
        self.success_baseline()
        archive = self.counter.parent/"recoveries/20000101T000000Z"
        archive.mkdir(parents=True)
        (archive/"manifest.json").write_text('{"recovery_barrier":11,"highest_seen":10}\n')
        self.assert_under_lock_rechecked(archive/"failures.jsonl", 11)

    def test_r6_2_refusal_heartbeat_raises_floor_without_a_failure(self):
        self.success_baseline()
        self.counter.write_text("corrupt\n")
        self.write_launch_receipt(launch_generation=None)
        refusal = self.heartbeat.parent/"refusals/latest-refusal.json"
        refusal.parent.mkdir()
        refusal.write_bytes(b'{"schema":1,"launch_generation":100,"launch_mode":"applet","exit_code":75}\n')
        original = refusal.read_bytes()
        self.assert_low_floor_refused_unchanged(10)
        result = self.recover(100)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(self.counter.read_bytes(), b"101\n")
        state = json.loads((self.counter.parent/"unresolved.json").read_text())
        self.assertEqual(state["unresolved"], [[1, 100]], "lost-history range derives from the reviewed floor")
        self.assertEqual(state["recovery_barrier"], 101)
        self.assertFalse(self.journal.exists(), "exit 75 must not publish an unresolved failure")
        self.assertEqual(refusal.read_bytes(), original)
        allocation = self.shell_literal("generationShell")
        self.assertEqual(allocation.returncode, 0, allocation.stderr)
        self.assertEqual(allocation.stdout.strip(), "102")
        self.write_heartbeat(launch_generation=102, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)

    def test_r6_2_under_lock_rechecks_refusal_heartbeat(self):
        self.success_baseline()
        self.assert_under_lock_rechecked(self.heartbeat.parent/"refusals/latest-refusal.json", 10)


class R7RecoveryFixture(Fixture):
    temporaries = {
        "refusal": ("memit-gdrive-backup/refusals", ".last_run.",
                    b'{"schema":1,"launch_generation":100,"launch_mode":"applet","exit_code":75}\n'),
        "heartbeat": ("memit-gdrive-backup", ".last_run.",
                      b'{"schema":1,"launch_generation":100,"launch_mode":"applet","exit_code":0}\n'),
        "receipt": ("memit-gdrive-backup", ".launch-receipt.",
                    b'{"schema":1,"launch_generation":100,"exit_code":75}\n'),
        "journal": ("memit-gdrive-backup-launch-journal", ".journal.",
                    b'{"schema":1,"launch_generation":11,"reason":"failed launch"}\n'
                    b'{"schema":1,"launch_generation":100,"reason":"failed launch"}\n'),
        "counter": ("memit-gdrive-backup-launch-state", ".counter.", b'100\n'),
        "unresolved": ("memit-gdrive-backup-launch-state", ".unresolved.",
                       b'{"schema":1,"issued_generation":100,"unresolved":[[1,100]],'
                       b'"recovery_barrier":null,"compaction_barrier":null}\n'),
        "recovery_state": ("memit-gdrive-backup-launch-state", ".recovery.",
                           b'{"schema":1,"issued_generation":100,"unresolved":[[1,100]],'
                           b'"recovery_barrier":null,"compaction_barrier":null}\n'),
        "recovery_manifest": ("memit-gdrive-backup-launch-state", ".recovery.",
                              b'{"schema":1,"recovery_barrier":100,"highest_seen":10,"generation_floor":99}\n'),
        "recovery_counter": ("memit-gdrive-backup-launch-state", ".recovery.", b'100\n'),
    }

    def raw_history(self, name):
        logs = self.base/name/"Library/Logs"
        heartbeat = logs/"memit-gdrive-backup/last_run.json"
        heartbeat.parent.mkdir(parents=True)
        heartbeat.write_bytes(b'{"schema":1,"launch_generation":10,"launch_mode":"applet",'
                              b'"end":"2026-10-10T00:00:00Z","exit_code":0}\n')
        (heartbeat.parent/"launch_receipt.json").write_bytes(
            b'{"schema":1,"launch_generation":null,"exit_code":127,"error_number":null}\n')
        state_dir = logs/"memit-gdrive-backup-launch-state"
        state_dir.mkdir()
        (state_dir/"counter").write_bytes(b'corrupt\n')
        self.assertFalse((state_dir/"unresolved.json").exists())
        self.assertFalse((state_dir/"counter.lock").exists())
        return heartbeat

    def history_snapshot(self, heartbeat):
        logs = heartbeat.parent.parent
        return {str(path.relative_to(logs)): path.read_bytes() if path.is_file() else None
                for path in sorted(logs.rglob("*"))}

    def recover_history(self, heartbeat, floor):
        return run_process([sys.executable, "-B", str(STATUS), "recover", "--heartbeat", str(heartbeat),
                            "--generation-floor", str(floor)], timeout=5)

    def temporary_path(self, heartbeat, source, archived):
        directory, prefix, _data = self.temporaries[source]
        logs = heartbeat.parent.parent
        parent = (logs/"memit-gdrive-backup-launch-state/recoveries/old/nested" if archived else logs/directory)
        return parent/(prefix+"ABC123")

    def assert_floor_pair(self, heartbeat, evidence):
        before = self.history_snapshot(heartbeat)
        original = evidence.read_bytes()
        result = self.recover_history(heartbeat, 10)
        self.assertEqual(self.history_snapshot(heartbeat), before,
                         "pre-lock refusal must leave all bytes and directories identical")
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("below observed maximum 100", result.stderr)
        state_dir = heartbeat.parent.parent/"memit-gdrive-backup-launch-state"
        self.assertFalse((state_dir/"counter.lock").exists())
        result = self.recover_history(heartbeat, 100)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual((state_dir/"counter").read_bytes(), b'101\n')
        state = json.loads((state_dir/"unresolved.json").read_bytes())
        self.assertEqual(state["recovery_barrier"], 101)
        self.assertEqual(state["unresolved"], [[1, 100]])
        self.assertEqual(evidence.read_bytes(), original, "a surviving publication temporary is evidence")
        after = self.history_snapshot(heartbeat)
        self.assertEqual({name: after[name] for name in before if "/recoveries/" in name},
                         {name: data for name, data in before.items() if "/recoveries/" in name})
        self.assertFalse((heartbeat.parent.parent/"memit-gdrive-backup-launch-journal/failures.jsonl").exists())

    def assert_temporary_floor_pair(self, source):
        for archived in (False, True):
            with self.subTest(source=source, archived=archived):
                heartbeat = self.raw_history(source+str(archived))
                evidence = self.temporary_path(heartbeat, source, archived)
                evidence.parent.mkdir(parents=True, exist_ok=True)
                evidence.write_bytes(self.temporaries[source][2])
                self.assert_floor_pair(heartbeat, evidence)

    def assert_format_refused(self, heartbeat, evidence, word):
        before = self.history_snapshot(heartbeat)
        result = self.recover_history(heartbeat, 100)
        self.assertEqual(self.history_snapshot(heartbeat), before,
                         "unsupported evidence must refuse before directory/lock creation")
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("recovery refused", result.stderr)
        self.assertIn(str(evidence), result.stderr)
        self.assertIn(word, result.stderr)


class R7PublicationTemporaryTest(R7RecoveryFixture):
    def test_r7_1_refusal_last_run_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("refusal")

    def test_r7_1_heartbeat_last_run_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("heartbeat")

    def test_r7_1_launch_receipt_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("receipt")

    def test_r7_1_journal_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("journal")

    def test_r7_1_counter_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("counter")

    def test_r7_1_unresolved_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("unresolved")

    def test_r7_1_recovery_state_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("recovery_state")

    def test_r7_1_recovery_manifest_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("recovery_manifest")

    def test_r7_1_recovery_counter_temporary_live_and_archived_floor_pair(self):
        self.assert_temporary_floor_pair("recovery_counter")

    def test_r7_1_under_lock_rechecks_every_live_and_archived_temporary(self):
        from tools import backup_gdrive_status as status
        for source in self.temporaries:
            for archived in (False, True):
                with self.subTest(source=source, archived=archived):
                    heartbeat = self.raw_history(source+str(archived))
                    state_dir = heartbeat.parent.parent/"memit-gdrive-backup-launch-state"
                    (state_dir/"counter.lock").write_bytes(b'')
                    evidence = self.temporary_path(heartbeat, source, archived)
                    observed = []

                    def inject(_lock, _operation):
                        evidence.parent.mkdir(parents=True, exist_ok=True)
                        evidence.write_bytes(self.temporaries[source][2])
                        observed.append(self.history_snapshot(heartbeat))

                    with mock.patch.object(status.fcntl, "flock", side_effect=inject):
                        with self.assertRaisesRegex(ValueError, "below observed maximum 100"):
                            status.recover(SimpleNamespace(heartbeat=str(heartbeat), generation_floor=10))
                    self.assertEqual(len(observed), 1, "positive control: injection occurred after pre-lock scan")
                    self.assertEqual(self.history_snapshot(heartbeat), observed[0],
                                     "under-lock refusal must preserve every injected byte and directory")

    def test_r7_1_unparseable_temporary_live_and_archived_refuses_with_filename(self):
        for source in self.temporaries:
            for archived in (False, True):
                with self.subTest(source=source, archived=archived):
                    heartbeat = self.raw_history(source+str(archived))
                    evidence = self.temporary_path(heartbeat, source, archived)
                    evidence.parent.mkdir(parents=True, exist_ok=True)
                    evidence.write_bytes(b'not JSON or an integer\n')
                    self.assert_format_refused(heartbeat, evidence, "unsupported")


class R7ArchivePrecisionTest(R7RecoveryFixture):
    def test_r7_2_nested_manifest_requires_floor_100_and_reserves_101(self):
        heartbeat = self.raw_history("manifest")
        evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/recoveries/old/nested/manifest.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b'{"schema":1,"recovery_barrier":100,"highest_seen":10}\n')
        self.assert_floor_pair(heartbeat, evidence)

    def test_r7_2_utf16_jsonl_refuses_unchanged_and_names_file(self):
        heartbeat = self.raw_history("utf16")
        evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/recoveries/old/failures.jsonl"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b'\xff\xfe'+('{"launch_generation":10}\n{"launch_generation":100}\n').encode("utf-16-le"))
        self.assert_format_refused(heartbeat, evidence, "UTF-8")

    def test_r7_2_nested_generation_refuses_unchanged_and_names_file(self):
        for name, data in (("object", b'{"launch_generation":10,"payload":{"launch_generation":100}}\n'),
                           ("array", b'{"launch_generation":10,"records":[{"issued_generation":100}]}\n')):
            with self.subTest(layout=name):
                heartbeat = self.raw_history(name)
                evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/recoveries/old/launch_receipt.json"
                evidence.parent.mkdir(parents=True)
                evidence.write_bytes(data)
                self.assert_format_refused(heartbeat, evidence, "nested generation")

    def test_r7_2_unknown_archive_format_refuses_unchanged_and_names_file(self):
        heartbeat = self.raw_history("unknown")
        evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/recoveries/old/evidence.bin"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b'{"launch_generation":100}\n')
        self.assert_format_refused(heartbeat, evidence, "unsupported")

    def test_r7_2_unparseable_archived_json_and_jsonl_refuse_with_filename(self):
        for name in ("last_run.json", "failures.jsonl"):
            with self.subTest(format=name):
                heartbeat = self.raw_history(name)
                evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/recoveries/old"/name
                evidence.parent.mkdir(parents=True)
                evidence.write_bytes(b'not JSON\n')
                self.assert_format_refused(heartbeat, evidence, "unsupported")


class R8RecoveryFixture(R7RecoveryFixture):
    nested_state = (b'{"schema":1,"issued_generation":10,"unresolved":[],"recovery_barrier":null,'
                    b'"x":{"launch_generation":100}}')
    invalid_field_state = (b'{"schema":1,"issued_generation":10,"unresolved":[],"recovery_barrier":null,'
                           b'"launch_generation":"100"}')
    duplicate_generation = b'{"launch_generation":100,"launch_generation":10}'
    duplicate_state = (b'{"schema":1,"issued_generation":100,"issued_generation":10,'
                       b'"unresolved":[],"recovery_barrier":null}')

    def assert_pre_lock_refusal(self, heartbeat, evidence, word):
        before = self.history_snapshot(heartbeat)
        result = self.recover_history(heartbeat, 10)
        self.assertEqual(self.history_snapshot(heartbeat), before,
                         "pre-lock refusal must preserve every byte and directory")
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("recovery refused", result.stderr)
        self.assertIn(str(evidence), result.stderr)
        self.assertIn(word, result.stderr)
        self.assertFalse((heartbeat.parent.parent/"memit-gdrive-backup-launch-state/counter.lock").exists())

    def assert_under_lock_refusal(self, heartbeat, evidence, payload, word):
        from tools import backup_gdrive_status as status
        (heartbeat.parent.parent/"memit-gdrive-backup-launch-state/counter.lock").write_bytes(b'')
        observed = []

        def inject(_lock, _operation):
            evidence.parent.mkdir(parents=True, exist_ok=True)
            evidence.write_bytes(payload)
            observed.append(self.history_snapshot(heartbeat))

        with mock.patch.object(status.fcntl, "flock", side_effect=inject):
            with self.assertRaises(ValueError) as refused:
                status.recover(SimpleNamespace(heartbeat=str(heartbeat), generation_floor=10))
        self.assertEqual(len(observed), 1, "positive control: evidence injected after the pre-lock scan")
        self.assertIn(str(evidence), str(refused.exception))
        self.assertIn(word, str(refused.exception))
        self.assertEqual(self.history_snapshot(heartbeat), observed[0],
                         "under-lock refusal must preserve every injected byte and directory")


class R8CurrentUnresolvedTest(R8RecoveryFixture):
    def test_r8_2_current_unresolved_nested_generation_pre_lock_refuses_unchanged(self):
        heartbeat = self.raw_history("nested-state")
        evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/unresolved.json"
        evidence.write_bytes(self.nested_state)
        self.assert_pre_lock_refusal(heartbeat, evidence, "nested generation")

    def test_r8_2_current_unresolved_validation_under_lock_refuses_unchanged(self):
        for name, payload, word in (("nested", self.nested_state, "nested generation"),
                                    ("encoding", b'\xff'+self.nested_state, "UTF-8"),
                                    ("field", self.invalid_field_state, "generation field")):
            with self.subTest(criterion=name):
                heartbeat = self.raw_history(name)
                evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/unresolved.json"
                self.assert_under_lock_refusal(heartbeat, evidence, payload, word)

    def test_r8_2_current_unresolved_non_utf8_refuses_with_filename(self):
        heartbeat = self.raw_history("non-utf8-state")
        evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/unresolved.json"
        evidence.write_bytes(b'\xff'+self.nested_state)
        self.assert_pre_lock_refusal(heartbeat, evidence, "UTF-8")

    def test_r8_2_current_unresolved_invalid_generation_field_refuses_with_filename(self):
        heartbeat = self.raw_history("invalid-state-field")
        evidence = heartbeat.parent.parent/"memit-gdrive-backup-launch-state/unresolved.json"
        evidence.write_bytes(self.invalid_field_state)
        self.assert_pre_lock_refusal(heartbeat, evidence, "generation field")


class R8DuplicateKeysTest(R8RecoveryFixture):
    def duplicate_path(self, heartbeat, location):
        return {
            "archived": heartbeat.parent.parent/"memit-gdrive-backup-launch-state/recoveries/old/x.json",
            "live": heartbeat.parent/"launch_receipt.json",
            "temporary": heartbeat.parent/".last_run.ABC123",
            "journal": heartbeat.parent.parent/"memit-gdrive-backup-launch-journal/failures.jsonl",
            "state": heartbeat.parent.parent/"memit-gdrive-backup-launch-state/unresolved.json",
        }[location]

    def assert_duplicate_refused(self, location):
        heartbeat = self.raw_history(location)
        evidence = self.duplicate_path(heartbeat, location)
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_bytes(self.duplicate_state if location == "state" else self.duplicate_generation)
        self.assert_pre_lock_refusal(heartbeat, evidence, "duplicate JSON key")

    def test_r8_3_archived_json_duplicate_keys_refuse_unchanged_with_filename(self):
        self.assert_duplicate_refused("archived")

    def test_r8_3_live_json_duplicate_keys_refuse_unchanged_with_filename(self):
        self.assert_duplicate_refused("live")

    def test_r8_3_recognized_json_temporary_duplicate_keys_refuse_unchanged_with_filename(self):
        self.assert_duplicate_refused("temporary")

    def test_r8_3_jsonl_duplicate_keys_refuse_instead_of_torn_line_tolerance(self):
        self.assert_duplicate_refused("journal")

    def test_r8_3_current_unresolved_duplicate_keys_refuse_unchanged_with_filename(self):
        self.assert_duplicate_refused("state")

    def test_r8_3_duplicate_keys_under_lock_refuse_every_evidence_location_unchanged(self):
        for location in ("archived", "live", "temporary", "journal", "state"):
            with self.subTest(location=location):
                heartbeat = self.raw_history(location)
                evidence = self.duplicate_path(heartbeat, location)
                payload = self.duplicate_state if location == "state" else self.duplicate_generation
                self.assert_under_lock_refusal(heartbeat, evidence, payload, "duplicate JSON key")

    def test_r8_3_nested_duplicate_keys_refuse_unchanged_with_filename(self):
        for name, payload in (("object", b'{"launch_generation":10,"x":{"value":100,"value":10}}'),
                              ("array", b'{"launch_generation":10,"x":[{"value":100,"value":10}]}')):
            with self.subTest(layout=name):
                heartbeat = self.raw_history(name)
                evidence = self.duplicate_path(heartbeat, "archived")
                evidence.parent.mkdir(parents=True)
                evidence.write_bytes(payload)
                self.assert_pre_lock_refusal(heartbeat, evidence, "duplicate JSON key")

    def test_r8_3_genuinely_torn_final_jsonl_line_remains_tolerated(self):
        heartbeat = self.raw_history("torn-final-line")
        evidence = self.duplicate_path(heartbeat, "journal")
        evidence.parent.mkdir()
        payload = b'{"launch_generation":100,"reason":"failed launch"}\n{"launch_generation":200'
        evidence.write_bytes(payload)
        before = self.history_snapshot(heartbeat)
        result = self.recover_history(heartbeat, 10)
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("below observed maximum 100", result.stderr)
        self.assertEqual(self.history_snapshot(heartbeat), before)
        result = self.recover_history(heartbeat, 100)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        state_dir = heartbeat.parent.parent/"memit-gdrive-backup-launch-state"
        self.assertEqual((state_dir/"counter").read_bytes(), b'101\n')
        state = json.loads((state_dir/"unresolved.json").read_bytes())
        self.assertEqual(state["recovery_barrier"], 101)
        self.assertEqual(state["unresolved"], [[1, 100]])
        archived = list((state_dir/"recoveries").rglob("failures.jsonl"))
        self.assertEqual(len(archived), 1)
        self.assertEqual(archived[0].read_bytes(), payload)
        self.assertFalse(evidence.exists())


class R5CompactionTest(R5Fixture):
    INTERVAL_LIMIT = 64
    BYTE_LIMIT = 2048

    def perl_program(self, name):
        source = (ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
        literal = json.loads(re.search(r'^property '+name+r' : ("(?:\\.|[^"\\])*")$', source, re.M)[1])
        # The program is the actual argument to Perl -e, including both publishers.
        match = re.search(r" -e '(.*?)\n'", literal, re.S)
        self.assertIsNotNone(match)
        return match[1]

    def perl_publish(self, state, name="generationShell", completed=0, refused=0):
        program = self.perl_program(name)
        helpers = program[program.index("sub state_integer"):]
        helpers = helpers[:helpers.index("my ($completed, $refused)") if name == "generationShell" else
                          helpers.index("my ($sec, $micro)")]
        (self.counter.parent/"unresolved.json").write_text(json.dumps(state))
        result = run_process(["/usr/bin/perl", "-MJSON::PP", "-MFile::Temp=tempfile", "-e", helpers+
            '\nmy ($dir,$issued,$completed,$refused)=@ARGV;\n'+
            'my $state=read_state($dir,$issued,$completed);\n'+
            'resolve_state($state,$completed,$refused); publish_state($dir,$state);\n',
            str(self.counter.parent), str(state["issued_generation"]), str(completed), str(refused)], timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = (self.counter.parent/"unresolved.json").read_bytes()
        self.assertLessEqual(len(data), self.BYTE_LIMIT, "unresolved state byte bound")
        value = json.loads(data)
        self.assertLessEqual(len(value["unresolved"]), self.INTERVAL_LIMIT, "unresolved state interval bound")
        return value

    def state(self, count):
        return {"schema": 1, "issued_generation": 10+count*2,
                "unresolved": [[11+2*i, 11+2*i] for i in range(count)], "recovery_barrier": None}

    def test_4_exact_limit_and_limit_plus_one_compaction(self):
        at_limit = self.perl_publish(self.state(self.INTERVAL_LIMIT))
        self.assertEqual(at_limit["unresolved"], self.state(self.INTERVAL_LIMIT)["unresolved"])
        self.assertIsNone(at_limit.get("compaction_barrier"))
        overflow = self.perl_publish(self.state(self.INTERVAL_LIMIT+1))
        self.assertEqual(overflow["unresolved"], [])
        self.assertEqual(overflow["compaction_barrier"], overflow["issued_generation"])

    def test_4_byte_overflow_preserves_the_recovery_barrier(self):
        state = self.state(1)
        state.update(recovery_barrier=10, padding="x"*self.BYTE_LIMIT)
        compacted = self.perl_publish(state)
        self.assertEqual(compacted["recovery_barrier"], 10)
        self.assertEqual(compacted["compaction_barrier"], state["issued_generation"])
        self.assertEqual(compacted["unresolved"], [])

    def test_4_two_thousand_allocations_remain_bounded_and_fail_closed(self):
        self.success_baseline()
        allocation = self.perl_program("generationShell")
        receipt = self.perl_program("receiptShell")
        self.assertIn("exit($published ? 0 : 1);", receipt)
        # Keep the production IO and interval logic; suppress only process exit/output.
        receipt = receipt.replace("exit($published ? 0 : 1);", 'die "receipt failed" unless $published;')
        harness = 'my ($allocation,$receipt,$dir)=@ARGV;\n'
        harness += '$allocation=eval "sub {".$allocation."}"; die $@ if $@;\n'
        harness += '$receipt=eval "sub {".$receipt."}"; die $@ if $@;\n'
        harness += 'for my $g (11..2010) {\n'
        harness += ' { my $output=""; open my $capture, ">", \\$output or die $!; local *STDOUT=$capture; $allocation->(); }\n'
        harness += ' if ($g % 2 == 0) { local @ARGV=("fixture-wrapper",75,"",$g); $receipt->(); }\n'
        harness += ' open my $in, "<", "$dir/unresolved.json" or die $!; my $data=do {local $/; <$in>}; close $in or die $!;\n'
        harness += ' print encode_json({generation=>$g,bytes=>length($data),state=>decode_json($data)}),"\\n"; }\n'
        result = run_process(["/usr/bin/perl", "-MJSON::PP", "-MFcntl=:flock", "-MFile::Path=make_path",
                              "-MFile::Temp=tempfile", "-MTime::HiRes=gettimeofday", "-MPOSIX=strftime",
                              "-e", harness, allocation, receipt, str(self.counter.parent)], timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        snapshots = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(snapshots), 2000)
        from tools import backup_gdrive_status as status
        self.write_launch_receipt(launch_generation=10, exit_code=0)
        for snapshot in snapshots:
            state = snapshot["state"]
            self.assertLessEqual(snapshot["bytes"], self.BYTE_LIMIT)
            self.assertLessEqual(len(state["unresolved"]), self.INTERVAL_LIMIT)
            self.counter.write_text(str(snapshot["generation"])+"\n")
            with mock.patch.object(status, "generation_state", return_value=state):
                ok, reason = status.health(self.heartbeat)
            self.assertFalse(ok, reason)
            self.assertTrue("generation 11" in reason or "compacted barrier" in reason, reason)
        self.counter.write_text("2010\n")
        compacted = json.loads((self.counter.parent/"unresolved.json").read_text())
        barrier = compacted["compaction_barrier"]
        self.assertGreaterEqual(barrier, 11)
        # A manual heartbeat, an incomplete sequence and another refusal cannot clear it.
        self.write_heartbeat(launch_generation=None, launch_mode="manual")
        self.assert_bad("compacted barrier")
        self.write_heartbeat(launch_generation=barrier, launch_mode="applet", end=None, exit_code=None)
        self.assert_bad("compacted barrier")
        self.write_heartbeat(launch_generation=10, launch_mode="applet")
        self.assertEqual(self.shell_literal("generationShell").returncode, 0)
        self.assertEqual(self.shell_literal("receiptShell", BACKUP, 75, "", 2011).returncode, 0)
        self.assert_bad("compacted barrier")
        self.write_heartbeat(launch_generation=2011, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)

    def test_r6_3_compacted_barrier_requires_strictly_later_completion(self):
        self.success_baseline()
        overflow = self.state(self.INTERVAL_LIMIT+1)
        compacted = self.perl_publish(overflow)
        self.counter.write_text(str(overflow["issued_generation"])+"\n")
        barrier = compacted["compaction_barrier"]
        refused = self.perl_publish(compacted, "receiptShell", completed=10, refused=barrier)
        self.assertEqual(refused["compaction_barrier"], barrier)
        self.assert_bad("compacted barrier")
        self.write_heartbeat(launch_generation=None, launch_mode="manual")
        self.assert_bad("compacted barrier")
        self.write_heartbeat(launch_generation=barrier-1, launch_mode="applet")
        self.assert_bad("compacted barrier")
        self.write_heartbeat(launch_generation=barrier, launch_mode="applet")
        self.assert_bad("compacted barrier")
        for publisher in ("generationShell", "receiptShell"):
            with self.subTest(publisher=publisher):
                equal = self.perl_publish(refused, publisher, completed=barrier)
                self.assertEqual(equal["compaction_barrier"], barrier)
                later = dict(equal, issued_generation=barrier+1)
                self.counter.write_text(str(barrier+1)+"\n")
                self.write_heartbeat(launch_generation=barrier+1, launch_mode="applet")
                resolved = self.perl_publish(later, publisher, completed=barrier+1)
                self.assertIsNone(resolved["compaction_barrier"])
                self.assertEqual(self.status().returncode, 0)

    def test_r6_3_python_and_both_perl_publishers_agree_at_boundaries(self):
        from tools import backup_gdrive_status as status
        self.success_baseline()
        for count in (self.INTERVAL_LIMIT+1, self.INTERVAL_LIMIT):
            for publisher in ("generationShell", "receiptShell"):
                original = self.state(count)
                perl = self.perl_publish(original, publisher)
                python = status.compact_generation_state(original)
                self.assertEqual(perl, python)
        compacted = status.compact_generation_state(self.state(self.INTERVAL_LIMIT+1))
        barrier = compacted["compaction_barrier"]
        for completed in (barrier-1, barrier, barrier+1):
            for publisher in ("generationShell", "receiptShell"):
                with self.subTest(completed=completed, publisher=publisher):
                    original = dict(compacted, issued_generation=max(barrier, completed))
                    perl = self.perl_publish(original, publisher, completed=completed)
                    self.assertEqual(perl["compaction_barrier"], None if completed > barrier else barrier)
                    (self.counter.parent/"unresolved.json").write_text(json.dumps(original))
                    self.counter.write_text(str(original["issued_generation"])+"\n")
                    self.write_heartbeat(launch_generation=completed, launch_mode="applet")
                    healthy, reason = status.health(self.heartbeat)
                    self.assertEqual(healthy, completed > barrier, reason)

    def test_r6_3_odd_failure_schedule_compacts_at_139(self):
        self.success_baseline()
        for generation in range(11, 139):
            allocation = self.shell_literal("generationShell")
            self.assertEqual(allocation.returncode, 0, allocation.stderr)
            self.assertEqual(int(allocation.stdout), generation)
            receipt = self.shell_literal("receiptShell", BACKUP, 1 if generation % 2 else 75, "", generation)
            self.assertEqual(receipt.returncode, 0, receipt.stderr)
        state_path = self.counter.parent/"unresolved.json"
        state = json.loads(state_path.read_text())
        self.assertEqual(state["unresolved"], [[generation, generation] for generation in range(11, 138, 2)])
        allocation = self.shell_literal("generationShell")
        self.assertEqual(allocation.returncode, 0, allocation.stderr)
        self.assertEqual(allocation.stdout.strip(), "139")
        compacted = json.loads(state_path.read_text())
        self.assertEqual(compacted["compaction_barrier"], 139)
        self.assertEqual(compacted["unresolved"], [])
        self.write_heartbeat(launch_generation=139, launch_mode="applet")
        self.assert_bad("compacted barrier generation 139")
        for publisher in ("generationShell", "receiptShell"):
            equal = self.perl_publish(compacted, publisher, completed=139)
            self.assertEqual(equal["compaction_barrier"], 139)
        allocation = self.shell_literal("generationShell")
        self.assertEqual(allocation.returncode, 0, allocation.stderr)
        self.assertEqual(allocation.stdout.strip(), "140")
        refusal = self.shell_literal("receiptShell", BACKUP, 75, "", 140)
        self.assertEqual(refusal.returncode, 0, refusal.stderr)
        equal = json.loads(state_path.read_text())
        self.assertEqual(equal["compaction_barrier"], 139)
        self.assert_bad("compacted barrier generation 139")
        self.write_heartbeat(launch_generation=140, launch_mode="applet")
        self.assertEqual(self.status().returncode, 0)
        for publisher in ("generationShell", "receiptShell"):
            later = self.perl_publish(equal, publisher, completed=140)
            self.assertIsNone(later["compaction_barrier"])


class GenerationWrapperTest(Fixture):
    def wrapper_records(self, generation):
        trace = self.base/"heartbeats.jsonl"
        shim = self.base/"record-python"
        shim.write_text('#!/bin/sh\n'+shlex.quote(sys.executable)+' -B "$@"\ncode=$?\n'
                        'if [ -f '+shlex.quote(str(self.heartbeat))+' ]; then /bin/cat '+shlex.quote(str(self.heartbeat))+' >> '+shlex.quote(str(trace))+'; fi\nexit "$code"\n')
        shim.chmod(0o700)
        env = dict(os.environ, BACKUP_PYTHON=str(shim), BACKUP_LOG=str(self.log),
                   BACKUP_HEARTBEAT=str(self.heartbeat), BACKUP_LOCK_DIR=str(self.base/"lock"),
                   BACKUP_RCLONE=str(self.base/"nonexistent-rclone"))
        env.pop("BACKUP_LAUNCH_GENERATION", None)
        if generation is not None:
            env["BACKUP_LAUNCH_GENERATION"] = generation
        result = run_process(["/bin/bash", str(BACKUP)], env=env, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        return [json.loads(line) for line in trace.read_text().splitlines()]

    def test_wrapper_start_and_end_record_applet_generation(self):
        records = self.wrapper_records("7")
        self.assertEqual(len(records), 2)
        self.assertIsNone(records[0]["end"])
        self.assertIsNotNone(records[1]["end"])
        for value in records:
            self.assertEqual(value.get("launch_generation"), 7)
            self.assertEqual(value.get("launch_mode"), "applet")

    def test_manual_wrapper_records_explicit_unsequenced_mode(self):
        records = self.wrapper_records(None)
        for value in records:
            self.assertIn("launch_generation", value)
            self.assertIsNone(value["launch_generation"])
            self.assertEqual(value.get("launch_mode"), "manual")

    def test_invalid_wrapper_generation_refuses_before_any_rclone_dispatch(self):
        marker = self.base/"must-not-dispatch"
        rclone = self.base/"stub-rclone"
        rclone.write_text('#!/bin/sh\nprintf ran > '+shlex.quote(str(marker))+'\nexit 1\n')
        rclone.chmod(0o700)
        env = dict(os.environ, BACKUP_PYTHON=sys.executable, BACKUP_LOG=str(self.log),
                   BACKUP_HEARTBEAT=str(self.heartbeat), BACKUP_LOCK_DIR=str(self.base/"lock"),
                   BACKUP_RCLONE=str(rclone), BACKUP_LAUNCH_GENERATION="broken")
        result = run_process(["/bin/bash", str(BACKUP)], env=env, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists(), "invalid generation must fail before preflight")
        self.assertFalse(self.heartbeat.exists())


class LockedReleaseTest(Fixture):
    """MB32: removing the release gate must dispatch corrupted fixture bytes."""
    FILES = ("backup_gdrive.sh", "backup_gdrive_status.py", "backup_mirror.excludes")

    def setUp(self):
        # A receipt-dir HOME is itself in a checkout; release fixtures must be outside it.
        temporary_root = mock.patch.dict(os.environ, BACKUP_TEST_RECEIPTS="/private/tmp")
        temporary_root.start()
        self.addCleanup(temporary_root.stop)
        super().setUp()
        self.checkout = self.base/"checkout"
        launchd = self.checkout/"code/ops/backup/launchd"
        launchd.mkdir(parents=True)
        self.original = {
            "backup_gdrive.sh": b'#!/bin/sh\nprintf "%s\\n" "$0" > "$HOME/dispatched-wrapper"\nprintf "%s\\n" "$BACKUP_LAUNCH_GENERATION" > "$HOME/dispatched-generation"\n',
            "backup_gdrive_status.py": b'# committed fixture status\n',
            "backup_mirror.excludes": b'# committed fixture excludes\n',
        }
        for name, content in self.original.items():
            (self.checkout/"tools"/name).write_bytes(content)
        for name in ("MemitGdriveBackup.applescript", "build_gdrive_applet.sh", "stage_gdrive_release.sh"):
            source = ROOT/"code/ops/backup/launchd"/name
            if source.exists():
                shutil.copyfile(source, launchd/name)
        self.git("init", "-q")
        self.git("add", "tools")
        self.git("-c", "user.name=MB32 Fixture", "-c", "user.email=fixture@invalid",
                 "-c", "core.hooksPath=/dev/null", "commit", "-qm", "locked release fixture")
        self.commit = self.git("rev-parse", "HEAD").stdout.strip()
        self.release_root = self.home/"Library/Application Support/memit-gdrive-backup/releases"
        self.release = self.release_root/"fixture-r1"
        self.rendered = self.base/"rendered source.applescript"
        self.counter = self.home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
        self.counter.parent.mkdir(parents=True)
        self.counter.write_text("0\n")
        self.receipt = self.home/"Library/Logs/memit-gdrive-backup/launch_receipt.json"
        self.marker = self.home/"dispatched-wrapper"

    def git(self, *args):
        result = run_process(["/usr/bin/git", "-C", str(self.checkout), *args], timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        return result

    def stage(self, *, baseline=True, root=None, rendered=None):
        script = self.checkout/"code/ops/backup/launchd/stage_gdrive_release.sh"
        if not script.exists() and baseline:
            # Safely exercise the old dispatch: its checkout path is a tiny stub.
            self.release.mkdir(parents=True)
            for name, content in self.original.items():
                (self.release/name).write_bytes(content)
            manifest = "".join(hashlib.sha256(self.original[n]).hexdigest()+"  "+n+"\n" for n in self.FILES)
            (self.release/"MANIFEST").write_text(manifest)
            source = (self.checkout/"code/ops/backup/launchd/MemitGdriveBackup.applescript").read_text()
            source = re.sub(r'^property wrapperPath : .*$',
                            lambda m: 'property wrapperPath : '+json.dumps(str(self.checkout/"code/ops/backup/backup_gdrive.sh")),
                            source, flags=re.M)
            self.rendered.write_text(source)
            return subprocess.CompletedProcess([], 0, "", "")
        self.assertTrue(script.is_file(), "commit-only release staging entrypoint is missing")
        args = ["/bin/bash", str(script), self.commit, "fixture-r1", str(rendered or self.rendered)]
        if root is not None:
            args.append(str(root))
        return run_process(args, timeout=10)

    def ready(self):
        result = self.stage()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)

    def dispatch(self):
        source = self.rendered.read_text()
        literals = {name: json.loads(literal) for name, literal in
                    re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', source, re.M)}
        # Same ordered shell literals and stamped wrapperPath as the applet.
        composition = re.search(r'quoted form of \(([^)]+)\).*" backup-launch "', source)
        self.assertIsNotNone(composition, "applet dispatch composition must be exercised")
        body = literals["generationShell"]+"".join(literals[name.strip()] for name in composition[1].split("&"))
        return run_process(["/bin/sh", "-c", body, "backup-launch", literals["wrapperPath"]], timeout=5)

    def refused(self, name, expected, actual):
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertFalse(self.marker.exists(), "integrity failure dispatched the wrapper")
        self.assertTrue(self.receipt.is_file(), "integrity refusal needs the existing receipt sink")
        value = json.loads(self.receipt.read_text())
        self.assertEqual(value["launch_generation"], 1)
        self.assertNotEqual(value["exit_code"], 0)
        failure = next((f for f in value.get("integrity_failures", []) if f["file"] == name), None)
        self.assertIsNotNone(failure, "failure receipt must name "+name)
        self.assertEqual(failure["expected_sha256"], expected)
        self.assertEqual(failure["actual_sha256"], actual)
        self.assertEqual(self.counter.read_text(), "1\n", "reserve before checking to sequence refusals")

    def change_byte(self, name):
        self.ready()
        path = self.release/name
        previous = path.read_bytes()
        changed = bytes([previous[0] ^ 1])+previous[1:]
        path.chmod(0o600)
        path.write_bytes(changed)
        self.refused(name, hashlib.sha256(previous).hexdigest(), hashlib.sha256(changed).hexdigest())

    def test_good_release_dispatches_release_path(self):
        self.ready()
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(self.marker.read_text().strip(), str(self.release/"backup_gdrive.sh"))
        self.assertEqual((self.home/"dispatched-generation").read_text(), "1\n")
        self.assertEqual(json.loads(self.receipt.read_text())["wrapper_path"], str(self.release/"backup_gdrive.sh"))
        self.assertEqual({p.name for p in self.release.iterdir()}, set(self.FILES)|{"MANIFEST"})
        for path in [self.release, *self.release.iterdir()]:
            self.assertEqual(path.stat().st_mode & 0o222, 0, str(path)+" must be read-only")

    def test_changed_wrapper_byte_refuses(self):
        self.change_byte("backup_gdrive.sh")

    def test_changed_status_byte_refuses(self):
        self.change_byte("backup_gdrive_status.py")

    def test_changed_excludes_byte_refuses(self):
        self.change_byte("backup_mirror.excludes")

    def test_changed_manifest_byte_refuses(self):
        self.change_byte("MANIFEST")

    def test_missing_file_refuses(self):
        self.ready()
        self.release.chmod(0o700)
        path = self.release/"backup_gdrive_status.py"
        previous = path.read_bytes()
        path.unlink()
        self.refused(path.name, hashlib.sha256(previous).hexdigest(), "MISSING")

    def test_extra_file_refuses(self):
        self.ready()
        self.release.chmod(0o700)
        path = self.release/"unexpected file"
        path.write_bytes(b"unapproved")
        self.refused(path.name, "ABSENT", hashlib.sha256(b"unapproved").hexdigest())

    def test_checkout_pull_cannot_change_dispatch(self):
        self.ready()
        (self.checkout/"code/ops/backup/backup_gdrive.sh").write_text("#!/bin/sh\nexit 99\n")
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertTrue(self.marker.is_file(), "pull changed what the applet dispatches")
        self.assertEqual(self.marker.read_text().strip(), str(self.release/"backup_gdrive.sh"))
        self.assertEqual((self.release/"backup_gdrive.sh").read_bytes(), self.original["backup_gdrive.sh"])

    def test_existing_release_id_refused_without_overwrite(self):
        self.ready()
        before = {p.name: p.read_bytes() for p in self.release.iterdir()}
        result = run_process(["/bin/bash", str(self.checkout/"code/ops/backup/launchd/build_gdrive_applet.sh"),
                              self.commit, "fixture-r1", str(self.base/"second.app")], timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("existing release", result.stderr.lower())
        self.assertEqual({p.name: p.read_bytes() for p in self.release.iterdir()}, before)
        self.assertFalse((self.base/"second.app.applescript").exists())

    def test_dirty_checkout_stages_commit_bytes(self):
        for name in self.FILES:
            (self.checkout/"tools"/name).write_bytes(b"dirty working tree\n")
        result = self.stage(baseline=False)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        for name in self.FILES:
            self.assertEqual((self.release/name).read_bytes(), self.original[name])

    def test_release_inside_another_checkout_refused(self):
        other = self.base/"other checkout"
        other.mkdir()
        result = run_process(["/usr/bin/git", "init", "-q", str(other)], timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.stage(baseline=False, root=other/"releases")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("git checkout", result.stderr.lower())
        self.assertFalse((other/"releases/fixture-r1").exists())

    def test_rendered_source_stamps_release_and_all_four_hashes(self):
        self.ready()
        source = self.rendered.read_text()
        literals = {name: json.loads(literal) for name, literal in
                    re.findall(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', source, re.M)}
        self.assertEqual(literals["wrapperPath"], str(self.release/"backup_gdrive.sh"))
        for path in self.release.iterdir():
            self.assertIn(hashlib.sha256(path.read_bytes()).hexdigest(), source)

    def build_native(self):
        self.assertTrue((self.checkout/"code/ops/backup/launchd/stage_gdrive_release.sh").is_file(),
                        "locked release build entrypoint is missing")
        # Standard Additions does not inherit subprocess HOME; embed the fixture HOME.
        template = self.checkout/"code/ops/backup/launchd/MemitGdriveBackup.applescript"
        def isolate(match):
            name, literal = match.groups()
            body = json.loads(literal)
            if name in {"generationShell", "integrityShell", "receiptShell"}:
                body = "HOME="+shlex.quote(str(self.home))+"\nexport HOME\n"+body
            return "property "+name+" : "+json.dumps(body)
        template.write_text(re.sub(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', isolate,
                                   template.read_text(), flags=re.M))
        app = self.base/"locked fixture.app"
        result = run_process(["/bin/bash", str(self.checkout/"code/ops/backup/launchd/build_gdrive_applet.sh"),
                              self.commit, "fixture-r1", str(app)], timeout=20)
        LauncherTest.osa_result(self, result, "locked release build")
        return app

    def build_with_fake_osa(self, mode):
        fake_bin = self.base/("fake-osa-"+mode)
        fake_bin.mkdir()
        fake = '#!'+sys.executable+'\n'+'''import os
from pathlib import Path
import sys

mode = os.environ["FAKE_OSA_MODE"]
if Path(sys.argv[0]).name == "osacompile":
    assert len(sys.argv) == 4 and sys.argv[1] == "-o", sys.argv
    output, source = map(Path, sys.argv[2:])
    data = source.read_bytes()
    if output.suffix == ".app":
        script = output/"Contents/Resources/Scripts/main.scpt"
        script.parent.mkdir(parents=True)
        executable = output/"Contents/MacOS/applet"
        executable.parent.mkdir()
        executable.write_bytes(b"fixture applet\\n")
    else:
        script = output
        if output.name == "rendered.scpt":
            (Path(__file__).parent/"rendered_input.applescript").write_bytes(data)
    script.write_bytes(data)
else:
    assert len(sys.argv) == 2, sys.argv
    script = Path(sys.argv[1])
    data = script.read_bytes()+b"\\n"
    if mode == "empty_canonical" and script.name == "rendered.scpt":
        data = b""
    if script.name == "main.scpt":
        if mode == "extra_newline":
            data += b"\\n"
        if mode == "changed_byte":
            data = bytes([data[0] ^ 1])+data[1:]
    sys.stdout.buffer.write(data)
'''
        for name in ("osacompile", "osadecompile"):
            path = fake_bin/name
            path.write_text(fake)
            path.chmod(0o700)
        # Substitute only tool paths in this fixture copy; production has no override.
        builder = self.checkout/"code/ops/backup/launchd/build_gdrive_applet.sh"
        source = (ROOT/"code/ops/backup/launchd/build_gdrive_applet.sh").read_text()
        for name in ("osacompile", "osadecompile"):
            self.assertIn("/usr/bin/"+name, source)
            source = source.replace("/usr/bin/"+name, name)
        builder.write_text(source)
        app = self.base/(mode+" fixture.app")
        env = dict(os.environ, PATH=str(fake_bin)+os.pathsep+os.environ["PATH"],
                   FAKE_OSA_MODE=mode, TMPDIR=str(self.base))
        result = run_process(["/bin/bash", str(builder), self.commit, "fixture-"+mode, str(app)],
                             env=env, timeout=20)
        return app, fake_bin, result

    def test_builder_compares_fresh_saved_compile_with_newline_growth(self):
        app, fake_bin, result = self.build_with_fake_osa("normal")
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        saved = Path(str(app)+".applescript")
        decompiled = Path(str(app)+".decompiled.applescript")
        self.assertEqual(saved.read_bytes(), (fake_bin/"rendered_input.applescript").read_bytes()+b"\n")
        self.assertEqual(decompiled.read_bytes(), saved.read_bytes()+b"\n")
        for path in (saved, decompiled):
            self.assertEqual(path.stat().st_mode & 0o777, 0o444)
        manifest = dict((path, digest) for digest, path in
                        (line.split("  ", 1) for line in result.stdout.splitlines()))
        self.assertEqual(manifest, {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                   for path in app.rglob("*") if path.is_file()})

    def test_builder_rejects_app_decompile_byte_mismatch(self):
        for mode in ("extra_newline", "changed_byte"):
            with self.subTest(mode=mode):
                app, fake_bin, result = self.build_with_fake_osa(mode)
                self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
                self.assertNotEqual(Path(str(app)+".decompiled.applescript").read_bytes(),
                                    Path(str(app)+".applescript").read_bytes()+b"\n")
                self.assertFalse(any(re.match(r"^[0-9a-f]{64}  ", line)
                                     for line in result.stdout.splitlines()))

    def test_builder_rejects_empty_canonical_decompile(self):
        app, fake_bin, result = self.build_with_fake_osa("empty_canonical")
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn("Empty canonical AppleScript", result.stderr)
        self.assertFalse(app.exists())

    def test_compiled_app_full_source_equals_saved_source(self):
        app = self.build_native()
        saved = Path(str(app)+".applescript")
        reference = self.base/"saved source.scpt"
        result = run_process(["/usr/bin/osacompile", "-o", str(reference), str(saved)], timeout=10)
        LauncherTest.osa_result(self, result, "osacompile saved source")
        app_source, reference_source = self.base/"app decompile.applescript", self.base/"saved decompile.applescript"
        for compiled, decompiled in ((app/"Contents/Resources/Scripts/main.scpt", app_source),
                                     (reference, reference_source)):
            result = run_process(["/bin/sh", "-c", 'exec /usr/bin/osadecompile "$1" > "$2"',
                                  "osadecompile", str(compiled), str(decompiled)], timeout=10)
            LauncherTest.osa_result(self, result, "osadecompile "+str(compiled))
        self.assertEqual(app_source.read_bytes(), reference_source.read_bytes())
        self.assertEqual(app_source.read_bytes(), Path(str(app)+".decompiled.applescript").read_bytes())

    def test_compiled_app_dispatches_release_after_checkout_change(self):
        app = self.build_native()
        (self.checkout/"code/ops/backup/backup_gdrive.sh").write_text("#!/bin/sh\nexit 99\n")
        result = run_process(["/usr/bin/osascript", str(app/"Contents/Resources/Scripts/main.scpt")], timeout=5)
        LauncherTest.osa_result(self, result, "osascript locked app")
        self.assertEqual(self.marker.read_text().strip(), str(self.release/"backup_gdrive.sh"))
        self.assertEqual(json.loads(self.receipt.read_text())["exit_code"], 0)


class LauncherTest(Fixture):
    def setUp(self):
        temporary_root = mock.patch.dict(os.environ, BACKUP_TEST_RECEIPTS="/private/tmp")
        temporary_root.start()
        self.addCleanup(temporary_root.stop)
        super().setUp()

    def osa_result(self, result, command):
        output = result.stdout+result.stderr
        if result.returncode and any(reason in output.lower() for reason in
                                      ["operation not permitted", "not authorized", "permission denied", "sandbox"]):
            self.skipTest("UNVERIFIED: "+command+" exit "+str(result.returncode)+": "+output.strip())
        if result.returncode and any(code in output for code in ["(-2740)", "(-2741)"]):
            # Check the missing Standard Additions service independently of our source.
            control = run_process(["/usr/bin/osascript", "-e", '«event sysoexec» "/usr/bin/true"'], timeout=5)
            if (control.returncode and "com.apple.hiservices-xpcservice" in control.stderr and
                    "Connection invalid" in control.stderr):
                self.skipTest("UNVERIFIED: "+command+" exit "+str(result.returncode)+": "+output.strip()+
                              "; Standard Additions control exit "+str(control.returncode)+": "+control.stderr.strip())
        self.assertEqual(result.returncode, 0, command+": "+output)

    def test_launchd_waits_for_background_applet(self):
        with (ROOT/"code/ops/backup/launchd/com.rhu.memit-gdrive-backup.plist").open("rb") as stream:
            value = plistlib.load(stream)
        self.assertEqual(value["ProgramArguments"],
                         ["/usr/bin/open", "-W", "-g", "/Users/robertrhu/Applications/MemitGdriveBackup.app"])
        self.assertEqual(value["StartInterval"], 21600)
        self.assertIs(value["RunAtLoad"], False)

    def test_nonzero_shell_script_is_caught_promptly_without_dialog(self):
        source = ROOT/"code/ops/backup/launchd/MemitGdriveBackup.applescript"
        self.assertTrue(source.is_file(), "no-dialog applet source must exist")
        marker = self.base/"failing-script-invoked"
        stub = self.base/"failing-backup.sh"
        stub.write_text('#!/bin/bash\nprintf invoked > "'+str(marker)+'"\nexit 1\n')
        variant = self.base/"failure.applescript"
        text = source.read_text()
        variant_text = re.sub(r'^property wrapperPath : .*$',
                              lambda m: 'property wrapperPath : '+json.dumps(str(stub)), text, flags=re.M)
        # This existing smoke tests the caught wrapper error; release checks have their own tests.
        variant_text = re.sub(r'^property integrityShell : .*$', 'property integrityShell : ""',
                              variant_text, flags=re.M)
        self.assertNotEqual(variant_text, text, "variant must actually invoke the exit-1 stub")
        home = self.base/"applet-home"
        counter = home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
        counter.parent.mkdir(parents=True)
        counter.write_text("0\n")
        variant_text = isolate_failing_launcher_home(variant_text, home)
        variant.write_text(variant_text)
        compiled = self.base/"failure.scpt"
        result = run_process(["/usr/bin/osacompile", "-o", str(compiled), str(variant)], timeout=10)
        self.osa_result(result, "osacompile failure variant")
        self.assertTrue(compiled.is_file())
        start = time.monotonic()
        result = run_process(["/usr/bin/osascript", str(compiled)], timeout=5)
        self.osa_result(result, "osascript exit-1 variant")
        self.assertLess(time.monotonic()-start, 5)
        self.assertTrue(marker.is_file(), "positive control: the failing shell script was run")
        receipt = home/"Library/Logs/memit-gdrive-backup/launch_receipt.json"
        state = counter.parent/"unresolved.json"
        for artifact in (receipt, counter, state):
            self.assertTrue(artifact.is_file(), "positive control: fixture artifact "+str(artifact))
        self.assertEqual(json.loads(receipt.read_text())["exit_code"], 1)
        self.assertGreater(int(counter.read_text()), 0)

    def test_builder_compiles_applet_and_prints_complete_sha256_manifest(self):
        script = ROOT/"code/ops/backup/launchd/build_gdrive_applet.sh"
        self.assertTrue(script.is_file(), "applet builder must exist")
        app = self.base/"test backup.app"
        commit = run_process(["/usr/bin/git", "-C", str(ROOT), "rev-parse", "HEAD"], timeout=5)
        self.assertEqual(commit.returncode, 0, commit.stderr)
        result = run_process(["/bin/bash", str(script), commit.stdout.strip(), "native-builder", str(app)], timeout=20)
        self.osa_result(result, "build_gdrive_applet.sh")
        self.assertTrue((app/"Contents/MacOS/applet").is_file())
        files = {str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in app.rglob("*") if path.is_file()}
        manifest = {}
        for line in result.stdout.splitlines():
            digest, path = line.split("  ", 1)
            self.assertEqual(len(digest), 64)
            self.assertNotIn(path, manifest)
            manifest[path] = digest
        self.assertEqual(manifest, files)
        previous = manifest.copy()
        refused = run_process(["/bin/bash", str(script), commit.stdout.strip(), "native-builder", str(app)], timeout=10)
        self.assertNotEqual(refused.returncode, 0, "builder must not overwrite an existing app bundle")
        self.assertEqual({str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in app.rglob("*") if path.is_file()}, previous)


class ArchiveTest(Fixture):
    def setUp(self):
        super().setUp()
        self.source_root = self.base / "repo"
        self.source_root.mkdir()
        self.src = self.source_root / "records/tiny.bin"
        self.src.parent.mkdir()
        self.src.write_bytes(b"irreplaceable test")
        self.dest = self.base / "remote"
        self.manifest = self.source_root / "evidence/manifests/ARCHIVE_MANIFEST.tsv"
        self.env = dict(os.environ, ARCHIVE_ROOT=str(self.source_root), ARCHIVE_DEST=str(self.dest),
                        ARCHIVE_MANIFEST=str(self.manifest), ARCHIVE_RCLONE=RCLONE)

    def archive(self, *paths, **changes):
        return run_process(["/bin/bash", str(ARCHIVE), *(str(p) for p in paths or [self.src])],
                           env=dict(self.env, **changes), timeout=20)

    def fake_rclone(self, body):
        path = self.base / "fake-archive-rclone"
        path.write_text('#!/bin/bash\n'+body)
        path.chmod(0o700)
        return str(path)

    def assert_no_receipt(self):
        if self.manifest.exists():
            self.assertLessEqual(len(self.manifest.read_text().splitlines()), 1)

    @HOST_RCLONE
    def test_real_copy_download_check_and_sha_receipt_never_delete_source(self):
        result = self.archive()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual((self.dest / "records/tiny.bin").read_bytes(), self.src.read_bytes())
        rows = self.manifest.read_text().splitlines()
        self.assertEqual(rows[0], "sha256\tsize_bytes\tremote_path")
        self.assertEqual(rows[1].split("\t"), [hashlib.sha256(self.src.read_bytes()).hexdigest(),
                         str(self.src.stat().st_size), str(self.dest/"records/tiny.bin")])
        self.assertTrue(self.src.exists())
        self.assertEqual(self.archive().returncode, 0, "identical remote content may be verified again")

    @HOST_RCLONE
    def test_differing_remote_is_immutable_and_preserves_prior_manifest(self):
        self.assertEqual(self.archive().returncode, 0)
        prior = self.manifest.read_bytes()
        self.src.write_bytes(b"different content")
        result = self.archive()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.dest/"records/tiny.bin").read_bytes(), b"irreplaceable test")
        self.assertEqual(self.manifest.read_bytes(), prior)

    @HOST_RCLONE
    def test_corrupt_remote_download_check_does_not_create_receipt(self):
        fake = self.fake_rclone('if [ "$1" = check ]; then printf corrupt > "'+str(self.dest/"records/tiny.bin")+'"; fi\nexec '+RCLONE+' "$@"\n')
        result = self.archive(ARCHIVE_RCLONE=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assert_no_receipt()
        self.assertTrue(self.src.exists())

    @HOST_RCLONE
    def test_source_drift_after_check_does_not_create_receipt(self):
        fake = self.fake_rclone(RCLONE+' "$@"\nstatus=$?\nif [ "$1" = check ] && [ "$status" = 0 ]; then printf drift >> "'+str(self.src)+'"; fi\nexit "$status"\n')
        result = self.archive(ARCHIVE_RCLONE=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("changed", result.stdout+result.stderr)
        self.assert_no_receipt()

    @HOST_RCLONE
    def test_manifest_write_failure_is_loud(self):
        blocker = self.source_root/"blocker"
        blocker.write_text("not a directory")
        result = self.archive(ARCHIVE_MANIFEST=str(blocker/"ARCHIVE_MANIFEST.tsv"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest", (result.stdout+result.stderr).lower())
        self.assertTrue(self.src.exists())

    def test_invalid_paths_refuse_before_any_copy(self):
        outside = self.base/"outside.bin"
        outside.write_text("outside")
        link = self.source_root/"escape.bin"
        link.symlink_to(outside)
        tab = self.source_root/"bad\tname.bin"
        tab.write_text("bad")
        for bad in [outside, link, self.src.parent, tab]:
            with self.subTest(path=bad):
                result = self.archive(self.src, bad)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.dest.exists(), "all input paths must be admitted before copies")
                self.assert_no_receipt()


def archive_drive_selftest():
    remote = "gdrive:memit-archive/_selftest"
    out = ROOT/"results"/("backup_gdrive_archive_"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    out.mkdir(exist_ok=False)
    commands, touched = [], False
    result = {"status": "INCOMPLETE"}

    def call(args, env=None):
        proc = run_process(args, env=env, timeout=180)
        commands.append({"args": args, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
        (out/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        if proc.returncode:
            raise RuntimeError(proc.stderr)
        return proc.stdout

    try:
        call([RCLONE, "lsd", "gdrive:", "--contimeout", "10s", "--timeout", "30s", "--retries", "1", "--low-level-retries", "1"])
        with tempfile.TemporaryDirectory(prefix="archive_drive_", dir="/private/tmp") as directory:
            base = Path(directory)
            source = base/"tiny.bin"
            source.write_bytes(b"archive-download-checked-tiny-fixture")
            env = dict(os.environ, ARCHIVE_ROOT=str(base), ARCHIVE_DEST=remote,
                       ARCHIVE_MANIFEST=str(out/"selftest_manifest.tsv"), ARCHIVE_RCLONE=RCLONE)
            touched = True
            call(["/bin/bash", str(ARCHIVE), str(source)], env=env)
            assert source.read_bytes() == b"archive-download-checked-tiny-fixture"
            row = (out/"selftest_manifest.tsv").read_text().splitlines()[1].split("\t")
            assert row == [hashlib.sha256(source.read_bytes()).hexdigest(), str(source.stat().st_size), remote+"/tiny.bin"]
            result.update(status="PASS", manifest="selftest_manifest.tsv", source_preserved=True)
    except Exception as exc:
        result.update(status="FAILED", error=str(exc))
    finally:
        if touched:
            try:
                call([RCLONE, "purge", "gdrive:memit-archive/_selftest/", "--contimeout", "10s", "--timeout", "30s", "--retries", "1", "--low-level-retries", "1"])
                result["cleanup"] = "PASS"
            except Exception as exc:
                result.update(status="FAILED", cleanup="FAILED", cleanup_error=str(exc))
        else:
            result["cleanup"] = "NOT NEEDED: no remote writes attempted"
        (out/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--archive-drive"]:
        sys.exit(archive_drive_selftest())
    unittest.main()
