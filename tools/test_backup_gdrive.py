"""Behavioral checks using real rclone/local storage; no Drive or production sync."""
import os
import datetime
import json
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/backup_gdrive.sh"


def run_process(args, *, env=None, timeout=1800):
    proc = subprocess.Popen(args, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        output, error = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            print("selftest: timed-out process group already exited", file=sys.stderr)
        output, error = proc.communicate()
        raise subprocess.TimeoutExpired(args, timeout, output, error) from exc
    return subprocess.CompletedProcess(args, proc.returncode, output, error)


class BackupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="backup_gdrive_", dir="/private/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.src = self.base / "source"
        self.src.mkdir()
        (self.src / "keep.txt").write_text("original")
        self.dest = self.base / "mirror"
        self.lock = self.base / "run.lock"
        self.log = self.base / "backup.log"
        self.env = dict(os.environ, BACKUP_SRC=str(self.src), BACKUP_DEST=str(self.dest),
                        BACKUP_EXCLUDES=str(ROOT / "tools/backup_mirror.excludes"),
                        BACKUP_LOG=str(self.log), BACKUP_LOCK_DIR=str(self.lock),
                        BACKUP_HEARTBEAT=str(self.base / "last_run.json"),
                        BACKUP_MOUNT_POINT="/", BACKUP_RCLONE="/opt/homebrew/bin/rclone")

    def run_backup(self, timeout=20, **changes):
        return run_process(["/bin/bash", str(SCRIPT)], env=dict(self.env, **changes), timeout=timeout)

    def assert_refused(self, result, reason):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(self.log.is_file(), "refusal must be logged")
        self.assertIn(reason, self.log.read_text().lower())

    def test_three_runs_keep_old_versions_and_exclude_regenerable_files(self):
        # Removing --backup-dir, --exclude-from or --links must break this check.
        (self.src / "gone.txt").write_text("deleted version")
        (self.src / ".cache").mkdir()
        (self.src / ".cache/ignored").write_text("exclude me")
        (self.src / "keep.link").symlink_to("keep.txt")
        first = self.run_backup()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual((self.dest / "keep.txt").read_text(), "original")
        self.assertFalse((self.dest / ".cache/ignored").exists())
        self.assertTrue((self.dest / "keep.link").is_symlink())
        self.assertEqual((self.dest / "keep.link").readlink().as_posix(), "keep.txt")
        (self.src / "keep.txt").write_text("modified contents")
        second = self.run_backup()
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual((self.dest / "keep.txt").read_text(), "modified contents")
        (self.src / "gone.txt").unlink()
        third = self.run_backup()
        self.assertEqual(third.returncode, 0, third.stdout + third.stderr)
        self.assertFalse((self.dest / "gone.txt").exists())
        archived = self.base / ".deleted"
        self.assertEqual([p.read_text() for p in archived.glob("*/keep.txt")], ["original"])
        self.assertEqual([p.read_text() for p in archived.glob("*/gone.txt")], ["deleted version"])
        self.assertFalse(self.lock.exists())

    def test_held_lock_refuses_and_logs_without_changing_destination(self):
        self.lock.mkdir()
        (self.lock / "owner").write_text(str(os.getpid()))
        self.assert_refused(self.run_backup(), "lock")
        self.assertTrue(self.lock.exists())
        self.assertFalse(self.dest.exists())

    def test_stale_lock_refuses_explicitly_without_auto_removal(self):
        self.lock.mkdir()
        (self.lock / "owner").write_text("unknown owner")
        self.assert_refused(self.run_backup(), "stale")
        self.assertTrue(self.lock.exists())

    def test_empty_source_cannot_erase_existing_backup(self):
        self.dest.mkdir()
        (self.dest / "keep.txt").write_text("preserve")
        (self.src / "keep.txt").unlink()
        self.assert_refused(self.run_backup(), "empty")
        self.assertEqual((self.dest / "keep.txt").read_text(), "preserve")

    def test_missing_source_refuses(self):
        self.assert_refused(self.run_backup(BACKUP_SRC=str(self.base / "missing")), "missing")
        self.assertFalse(self.dest.exists())

    def test_unmounted_volume_refuses(self):
        self.assert_refused(self.run_backup(BACKUP_MOUNT_POINT="/Volumes/backup-selftest-not-mounted"), "mounted")
        self.assertFalse(self.dest.exists())

    def test_real_rclone_failure_is_nonzero_and_logged(self):
        self.assert_refused(self.run_backup(BACKUP_DEST="backup_selftest_missing_remote:folder/mirror"), "rclone failed")
        self.assertFalse(self.lock.exists())

    def test_interruption_retains_lock_while_child_may_still_run(self):
        # A controlled slow external process makes the shell's signal window reproducible.
        slow = self.base / "slow-rclone"
        slow.write_text("#!/bin/bash\nif [ \"$1\" = version ]; then echo rclone-test; exit 0; fi\nexec /bin/sleep 2\n")
        slow.chmod(0o700)
        proc = subprocess.Popen(["/bin/bash", str(SCRIPT)], env=dict(self.env, BACKUP_RCLONE=str(slow)),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(proc.communicate, timeout=5)
        deadline = time.monotonic() + 3
        while not (self.lock / "rclone.pid").exists() and proc.poll() is None and time.monotonic() < deadline:
            time.sleep(0.02)
        self.assertTrue((self.lock / "rclone.pid").exists(), "sync child must have lock ownership recorded")
        self.assertGreater(int((self.lock / "rclone.pid").read_text()), 0)
        proc.send_signal(signal.SIGTERM)
        output = proc.communicate(timeout=5)
        self.assertNotEqual(proc.returncode, 0, output)
        self.assertTrue(self.lock.exists(), "interruption must not unlock a possible live sync child")
        self.assert_refused(self.run_backup(), "lock")
        time.sleep(2.1)

    def test_timeout_stops_entire_sync_group_before_cleanup(self):
        # Killing only Bash leaves its child writing and its capture pipes open.
        slow = self.base / "slow-rclone"
        heartbeat = self.base / "heartbeat"
        slow.write_text("#!/bin/bash\nif [ \"$1\" = version ]; then echo rclone-test; exit 0; fi\nfor i in {1..150}; do printf x >> '" + str(heartbeat) + "'; /bin/sleep 0.02; done\n")
        slow.chmod(0o700)
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            self.run_backup(timeout=1, BACKUP_RCLONE=str(slow))
        self.assertLess(time.monotonic() - start, 2, "timeout must reap the group before returning to cleanup")
        self.assertTrue(heartbeat.exists(), "positive control: the sync child started")
        before = heartbeat.read_bytes()
        time.sleep(0.1)
        self.assertEqual(heartbeat.read_bytes(), before, "no live child may write after timeout")


def drive_selftest():
    """Explicit opt-in: three tiny Drive syncs, one upload, real-source DRY RUN only."""
    remote = "gdrive:memit-backup/_selftest"
    out = ROOT / "results" / ("backup_gdrive_drive_" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    out.mkdir(exist_ok=False)
    rclone = "/opt/homebrew/bin/rclone"
    commands = []
    touched = False
    result = {"status": "INCOMPLETE", "evidence_dir": str(out)}

    def call(args, timeout=1800):
        proc = run_process(args, timeout=timeout)
        entry = {"args": args, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        commands.append(entry)
        (out / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        if proc.returncode:
            raise RuntimeError(f"command failed (exit {proc.returncode}): {args[0:2]}; {proc.stderr}")
        return proc.stdout

    def rc(*args):
        return call([rclone, *args, "--contimeout", "10s", "--timeout", "60s", "--retries", "1", "--low-level-retries", "1"])

    try:
        rc("lsd", "gdrive:memit-backup")  # No effect before genuine remote admission.
        with tempfile.TemporaryDirectory(prefix="backup_gdrive_drive_", dir="/private/tmp") as d:
            base = Path(d)
            src = base / "source"
            src.mkdir()
            (src / "keep.txt").write_text("original")
            (src / "gone.txt").write_text("deleted version")
            (src / ".cache").mkdir()
            (src / ".cache/ignored").write_text("excluded")
            dest = remote + "/mirror"
            env = dict(os.environ, BACKUP_SRC=str(src), BACKUP_DEST=dest,
                       BACKUP_LOG=str(out / "selftest.log"), BACKUP_LOCK_DIR=str(base / "lock"),
                       BACKUP_HEARTBEAT=str(out / "last_run.json"),
                       BACKUP_MOUNT_POINT="/", BACKUP_EXCLUDES=str(ROOT / "tools/backup_mirror.excludes"))
            def sync(failure_reason=None, **changes):
                proc = run_process(["/bin/bash", str(SCRIPT)], env=dict(env, **changes), timeout=180)
                commands.append({"args": ["/bin/bash", str(SCRIPT)], "exit_code": proc.returncode,
                                 "stdout": proc.stdout, "stderr": proc.stderr})
                (out / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
                if failure_reason:
                    assert proc.returncode != 0 and failure_reason in proc.stderr.lower()
                elif proc.returncode:
                    raise RuntimeError(proc.stderr)
            touched = True
            sync()
            assert rc("cat", dest + "/keep.txt") == "original"
            assert {x["Path"] for x in json.loads(rc("lsjson", dest, "--recursive", "--files-only"))} == {"keep.txt", "gone.txt"}
            (src / "keep.txt").write_text("modified contents")
            sync()
            assert rc("cat", dest + "/keep.txt") == "modified contents"
            (src / "gone.txt").unlink()
            sync()
            assert {x["Path"] for x in json.loads(rc("lsjson", dest, "--recursive", "--files-only"))} == {"keep.txt"}
            old = json.loads(rc("lsjson", remote + "/.deleted", "--recursive", "--files-only"))
            keep = [x["Path"] for x in old if x["Path"].endswith("/keep.txt")]
            gone = [x["Path"] for x in old if x["Path"].endswith("/gone.txt")]
            assert len(keep) == len(gone) == 1
            assert rc("cat", remote + "/.deleted/" + keep[0]) == "original"
            assert rc("cat", remote + "/.deleted/" + gone[0]) == "deleted version"
            result["three_run_sync_archive_excludes"] = "PASS"
            lock = base / "lock"
            lock.mkdir()
            sync(failure_reason="lock")
            lock.rmdir()
            sync(failure_reason="mounted", BACKUP_MOUNT_POINT="/Volumes/backup-selftest-not-mounted")
            empty = base / "empty"
            empty.mkdir()
            sync(failure_reason="empty", BACKUP_SRC=str(empty))
            assert rc("cat", dest + "/keep.txt") == "modified contents"
            result["held_lock_unmounted_empty_refusal"] = "PASS"
            payload = base / "upload_rate.bin"
            size = 200_000_000
            with payload.open("wb") as f:
                remaining = size
                while remaining:
                    block = os.urandom(min(1 << 20, remaining))
                    f.write(block)
                    remaining -= len(block)
            start = time.monotonic()
            rc("copyto", str(payload), remote + "/upload_rate.bin")
            elapsed = time.monotonic() - start
            uploaded = json.loads(rc("lsjson", remote, "--files-only"))
            assert next(x["Size"] for x in uploaded if x["Path"] == "upload_rate.bin") == size
            result.update(upload_bytes=size, upload_wall_s=elapsed, measured_bytes_per_s=size / elapsed)
            changes = out / "dry_run_changes.txt"
            source = "/Volumes/memit/llm-database-poc-mirror/"
            excludes = str(ROOT / "tools/backup_mirror.excludes")
            rc("sync", source, "gdrive:memit-backup/llm-database-poc-mirror/", "--dry-run", "--links",
               "--exclude-from", excludes, "--backup-dir", "gdrive:memit-backup/.deleted/DRY-RUN/", "--combined", str(changes))
            local = json.loads(rc("lsjson", source, "--recursive", "--files-only", "--links", "--exclude-from", excludes))
            sizes = {x["Path"]: x["Size"] for x in local}
            planned = [line[2:] for line in changes.read_text().splitlines() if line.startswith(("+ ", "* "))]
            total = sum(sizes[name] for name in planned)
            result.update(status="PASS", dry_run_transfer_files=len(planned), dry_run_transfer_bytes=total,
                          payload_rate_estimate_s=total / (size / elapsed),
                          estimate_scope="Payload-rate projection; small-file/API overhead and source churn not measured")
    except Exception as exc:
        result.update(status="FAILED", error=str(exc))
    finally:
        if touched:
            try:
                rc("purge", "gdrive:memit-backup/_selftest/")  # Exact authorized cleanup target only.
                result["cleanup"] = "PASS"
            except Exception as exc:
                result.update(status="FAILED", cleanup="FAILED", cleanup_error=str(exc))
        else:
            result["cleanup"] = "NOT NEEDED: no remote writes attempted"
        (out / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--drive"]:
        sys.exit(drive_selftest())
    unittest.main()
