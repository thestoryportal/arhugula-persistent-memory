"""Backup heartbeat and archival controls; real local rclone, optional tiny Drive probe."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.test_backup_gdrive import run_process

STATUS = ROOT / "tools/backup_gdrive_status.py"
BACKUP = ROOT / "tools/backup_gdrive.sh"
ARCHIVE = ROOT / "tools/archive_to_gdrive.sh"
RCLONE = "/opt/homebrew/bin/rclone"


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="gdrive_addendum_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
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


class StatusTest(Fixture):
    def test_fresh_success(self):
        self.write_heartbeat()
        result = self.status()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)

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
        self.env = dict(os.environ, BACKUP_SRC=str(self.src), BACKUP_DEST=str(self.base / "mirror"),
                        BACKUP_LOG=str(self.log), BACKUP_HEARTBEAT=str(self.heartbeat),
                        BACKUP_LOCK_DIR=str(self.base / "lock"), BACKUP_MOUNT_POINT="/",
                        BACKUP_RCLONE=RCLONE, BACKUP_EXCLUDES=str(ROOT / "tools/backup_mirror.excludes"))

    def backup(self, **changes):
        return run_process(["/bin/bash", str(BACKUP)], env=dict(self.env, **changes), timeout=10)

    def fake_rclone(self, body):
        path = self.base / "fake-rclone"
        path.write_text('#!/bin/bash\nif [ "$1" = version ]; then echo "rclone-test"; exit 0; fi\n'
                        'if [ "$1" = config ]; then exec '+RCLONE+' "$@"; fi\n'+body)
        path.chmod(0o700)
        return str(path)

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
                          'if sys.argv[1] == "version":\n print("rclone fixture");sys.exit(0)\n'
                          'if sys.argv[1] == "config":\n sys.exit(subprocess.call(['+repr(RCLONE)+',*sys.argv[1:]]))\n'
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
        result=self.backup(BACKUP_PYTHON=str(python))
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

    def test_differing_remote_is_immutable_and_preserves_prior_manifest(self):
        self.assertEqual(self.archive().returncode, 0)
        prior = self.manifest.read_bytes()
        self.src.write_bytes(b"different content")
        result = self.archive()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.dest/"records/tiny.bin").read_bytes(), b"irreplaceable test")
        self.assertEqual(self.manifest.read_bytes(), prior)

    def test_corrupt_remote_download_check_does_not_create_receipt(self):
        fake = self.fake_rclone('if [ "$1" = check ]; then printf corrupt > "'+str(self.dest/"records/tiny.bin")+'"; fi\nexec '+RCLONE+' "$@"\n')
        result = self.archive(ARCHIVE_RCLONE=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assert_no_receipt()
        self.assertTrue(self.src.exists())

    def test_source_drift_after_check_does_not_create_receipt(self):
        fake = self.fake_rclone(RCLONE+' "$@"\nstatus=$?\nif [ "$1" = check ] && [ "$status" = 0 ]; then printf drift >> "'+str(self.src)+'"; fi\nexit "$status"\n')
        result = self.archive(ARCHIVE_RCLONE=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("changed", result.stdout+result.stderr)
        self.assert_no_receipt()

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
