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
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.test_backup_gdrive import run_process

STATUS = ROOT / "tools/backup_gdrive_status.py"
BACKUP = ROOT / "tools/backup_gdrive.sh"
ARCHIVE = ROOT / "tools/archive_to_gdrive.sh"
RCLONE = "/opt/homebrew/bin/rclone"
NO_RCLONE = os.environ.get("BACKUP_TEST_NO_RCLONE") == "1"
HOST_RCLONE = unittest.skipIf(NO_RCLONE, "HOST-PENDING: real rclone forbidden by MB14 brief")


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
                   BACKUP_RCLONE=str(rclone), BACKUP_EXCLUDES=str(ROOT/"tools/backup_mirror.excludes"))
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
                        BACKUP_RCLONE=str(self.base/"HOST-PENDING-rclone") if NO_RCLONE else RCLONE, BACKUP_EXCLUDES=str(ROOT / "tools/backup_mirror.excludes"))

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
        deadline = time.monotonic()+3
        while not entered.exists() and owner.poll() is None and time.monotonic()<deadline:
            time.sleep(0.01)
        self.assertTrue(entered.exists())
        time.sleep(0.1)  # Wait for the child PID publication as well as dispatch.
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
        text = (ROOT/"tools/launchd/MemitGdriveBackup.applescript").read_text()
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
                "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh",
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
        text = (ROOT/"tools/launchd/MemitGdriveBackup.applescript").read_text()
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
        text = (ROOT/"tools/launchd/MemitGdriveBackup.applescript").read_text()
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
        text = (ROOT/"tools/launchd/MemitGdriveBackup.applescript").read_text()
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
        text = (ROOT/"tools/launchd/MemitGdriveBackup.applescript").read_text()
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


class R5CompactionTest(R5Fixture):
    INTERVAL_LIMIT = 64
    BYTE_LIMIT = 2048

    def perl_program(self, name):
        source = (ROOT/"tools/launchd/MemitGdriveBackup.applescript").read_text()
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

    def test_4_compacted_barrier_cannot_be_refused_and_completion_at_barrier_clears(self):
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
        self.assertEqual(self.status().returncode, 0)
        resolved = self.perl_publish(refused, "receiptShell", completed=barrier)
        self.assertIsNone(resolved["compaction_barrier"])

    def test_5_python_and_both_perl_publishers_agree_at_boundaries(self):
        from tools import backup_gdrive_status as status
        for count in (self.INTERVAL_LIMIT+1, self.INTERVAL_LIMIT):
            for publisher in ("generationShell", "receiptShell"):
                original = self.state(count)
                perl = self.perl_publish(original, publisher)
                python = status.compact_generation_state(original)
                self.assertEqual(perl, python)


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


class LauncherTest(Fixture):
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
        with (ROOT/"tools/launchd/com.rhu.memit-gdrive-backup.plist").open("rb") as stream:
            value = plistlib.load(stream)
        self.assertEqual(value["ProgramArguments"],
                         ["/usr/bin/open", "-W", "-g", "/Users/robertrhu/Applications/MemitGdriveBackup.app"])
        self.assertEqual(value["StartInterval"], 21600)
        self.assertIs(value["RunAtLoad"], False)

    def test_nonzero_shell_script_is_caught_promptly_without_dialog(self):
        source = ROOT/"tools/launchd/MemitGdriveBackup.applescript"
        self.assertTrue(source.is_file(), "no-dialog applet source must exist")
        marker = self.base/"failing-script-invoked"
        stub = self.base/"failing-backup.sh"
        stub.write_text('#!/bin/bash\nprintf invoked > "'+str(marker)+'"\nexit 1\n')
        variant = self.base/"failure.applescript"
        text = source.read_text()
        variant_text = text.replace("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/tools/backup_gdrive.sh", str(stub))
        self.assertNotEqual(variant_text, text, "variant must actually invoke the exit-1 stub")
        home = self.base/"applet-home"
        counter = home/"Library/Logs/memit-gdrive-backup-launch-state/counter"
        counter.parent.mkdir(parents=True)
        counter.write_text("0\n")
        def isolate(match):
            name, literal = match.groups()
            body = json.loads(literal)
            if name in {"generationShell", "receiptShell"}:
                body = "HOME="+shlex.quote(str(home))+"\n"+body
            return "property "+name+" : "+json.dumps(body)
        variant_text = re.sub(r'^property (\w+) : ("(?:\\.|[^"\\])*")$', isolate, variant_text, flags=re.M)
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

    def test_builder_compiles_applet_and_prints_complete_sha256_manifest(self):
        script = ROOT/"tools/launchd/build_gdrive_applet.sh"
        self.assertTrue(script.is_file(), "applet builder must exist")
        app = self.base/"test backup.app"
        result = run_process(["/bin/bash", str(script), str(app)], timeout=15)
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
        refused = run_process(["/bin/bash", str(script), str(app)], timeout=10)
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
        self.manifest = self.source_root / "docs/ARCHIVE_MANIFEST.tsv"
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
