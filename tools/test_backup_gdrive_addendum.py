"""Backup heartbeat and archival controls; real local rclone, optional tiny Drive probe."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
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
        path.write_text('#!/bin/bash\nif [ "$1" = version ]; then echo "rclone-test"; exit 0; fi\n'+body)
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
        while not (self.base/"lock/rclone.pid").exists() and proc.poll() is None and time.monotonic()<deadline:
            time.sleep(0.01)
        self.assertTrue(self.heartbeat.exists(), "start heartbeat must precede dispatch")
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

    def test_terminal_publication_cannot_mask_a_newer_active_run(self):
        entered, release = self.base/"terminal-entered", self.base/"terminal-release"
        writer = self.base/"paused-python"
        writer.write_text('#!/bin/bash\ncase "$*" in *" --phase end "*)\n'
                          'touch "'+str(entered)+'"\n'
                          'for i in {1..300}; do [ -f "'+str(release)+'" ] && break; /bin/sleep 0.01; done\n'
                          ';; esac\nexec /usr/bin/python3 "$@"\n')
        writer.chmod(0o700)
        first = subprocess.Popen(["/bin/bash", str(BACKUP)], env=dict(self.env, BACKUP_PYTHON=str(writer)),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(first.communicate, timeout=5)
        deadline = time.monotonic()+3
        while not entered.exists() and first.poll() is None and time.monotonic()<deadline:
            time.sleep(0.01)
        self.assertTrue(entered.exists(), "positive control: first terminal publication is paused")
        dispatched = self.base/"second-dispatched"
        fake = self.fake_rclone('touch "'+str(dispatched)+'"\n/bin/sleep 1.5\n')
        second = subprocess.Popen(["/bin/bash", str(BACKUP)], env=dict(self.env, BACKUP_RCLONE=fake),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(second.communicate, timeout=5)
        deadline = time.monotonic()+2
        while second.poll() is None and not dispatched.exists() and time.monotonic()<deadline:
            time.sleep(0.01)
        release.touch()
        output = first.communicate(timeout=5)
        self.assertEqual(first.returncode, 0, output)
        if second.poll() is None:
            result = self.status()
            self.assertNotEqual(result.returncode, 0, "older terminal success must not mask a newer active sync: "+result.stdout)
        else:
            output = second.communicate(timeout=5)
            self.assertNotEqual(second.returncode, 0, "newer sync must be held until terminal publication finishes")
            self.assertIn("lock", output[1].lower())

    def test_lock_cleanup_failure_records_failed_outcome(self):
        fake = self.fake_rclone('touch "$BACKUP_LOCK_DIR/unexpected"\n')
        result = self.backup(BACKUP_RCLONE=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(json.loads(self.heartbeat.read_text())["exit_code"], 0)
        self.assert_bad("failed")

    def log_rclone(self, records, exit_code=1):
        script = self.base/"logged-rclone"
        script.write_text('#!/usr/bin/python3\nimport json,sys\nfrom pathlib import Path\n'
                          'if sys.argv[1] == "version":\n print("rclone fixture");sys.exit(0)\n'
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
        (self.src/"ordinary.sock").write_text("regular file with socket suffix")
        result=self.backup()
        self.assertEqual(result.returncode,0,result.stderr)
        mirror=self.base/"mirror"
        self.assertFalse((mirror/"repo/.git/objects/tmp_obj_live").exists())
        self.assertFalse((mirror/"repo/.git/objects/ab/tmp_obj_nested").exists())
        self.assertTrue((mirror/"repo/.git/objects/ab/permanent_hash").exists())
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
