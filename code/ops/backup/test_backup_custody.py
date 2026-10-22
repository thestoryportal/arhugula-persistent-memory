"""Prove displaced-file custody through the real backup wrapper and rsync."""
import hashlib
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
RSYNC = Path("/opt/homebrew/bin/rsync")


class BackupCustodyTest(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(prefix="backup_custody_", dir="/tmp"))
        self.addCleanup(shutil.rmtree, self.base)
        self.assertTrue(RSYNC.is_file() and os.access(RSYNC, os.X_OK),
                        f"required real rsync missing: {RSYNC}")
        self.script = HERE / "backup_mirror.sh"
        self.sources = [self.base / f"source {i}" for i in range(2)]
        self.dests = [self.base / f"destination {i}" for i in range(2)]
        self.originals = {}
        for i, (source, dest) in enumerate(zip(self.sources, self.dests)):
            source.mkdir()
            dest.mkdir()
            (source / "replaced").write_bytes(f"new longer payload {i}".encode())
            for name in ("replaced", "destination-only"):
                old = dest / name
                old.write_bytes(f"old {i} {name}".encode())
                self.originals[old] = hashlib.sha256(old.read_bytes()).hexdigest()
        self.excludes = self.base / "rules"
        self.excludes.write_text("/.deleted/\n/.last_success\n")
        self.table = self.base / "pairs.tsv"
        self.table.write_text("reader\tsource\tdestination\texcludes\n" + "".join(
            f"ssd\t{source}\t{dest}\trules\n"
            for source, dest in zip(self.sources, self.dests)))
        mount = self.base / "mount"
        mount.write_text("#!/bin/bash\n"
                         '[[ "$BACKUP_MOUNT_POINT" = "$CUSTODY_BASE" ]] || exit 91\n'
                         'printf "fixture on %s (test)\\n" "$CUSTODY_BASE"\n')
        mount.chmod(0o755)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("BACKUP_", "CUSTODY_"))}
        self.env.update(BACKUP_PAIRS=str(self.table), BACKUP_RSYNC=str(RSYNC),
                        BACKUP_MOUNT=str(mount), BACKUP_MOUNT_POINT=str(self.base),
                        BACKUP_SRC=str(self.sources[0]), BACKUP_DEST=str(self.dests[0]),
                        BACKUP_EXCLUDES=str(self.excludes), CUSTODY_BASE=str(self.base))

    def run_backup(self):
        text = self.script.read_text()
        for seam in ("BACKUP_SRC", "BACKUP_DEST", "BACKUP_EXCLUDES", "BACKUP_PAIRS",
                     "BACKUP_RSYNC", "BACKUP_MOUNT", "BACKUP_MOUNT_POINT"):
            self.assertIn(seam, text, f"W7: refusing backup: missing seam {seam}")
        for key in ("BACKUP_SRC", "BACKUP_DEST", "BACKUP_EXCLUDES", "BACKUP_PAIRS",
                    "BACKUP_MOUNT", "BACKUP_MOUNT_POINT"):
            self.assertTrue(Path(self.env[key]).resolve().is_relative_to(self.base.resolve()),
                            f"W7: path outside fixture: {key}")
        proc = subprocess.Popen(["/bin/bash", str(self.script)], env=self.env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)

        def cleanup():
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()

        self.addCleanup(cleanup)
        stdout, stderr = proc.communicate(timeout=30)
        return subprocess.CompletedProcess(proc.args, proc.returncode, stdout, stderr)

    def assert_custody(self):
        # [LAW:behavior-not-structure] archived bytes, not rsync flags, prove custody.
        for dest in self.dests:
            archives = list((dest / ".deleted").iterdir())
            self.assertEqual(len(archives), 1, f"custody archive missing at {dest}")
            archive = archives[0]
            self.assertRegex(archive.name, r"^\d{8}T\d{6}$")
            for name in ("replaced", "destination-only"):
                saved = archive / name
                self.assertTrue(saved.is_file(), f"custody missing: {saved}")
                self.assertEqual(hashlib.sha256(saved.read_bytes()).hexdigest(),
                                 self.originals[dest / name], f"custody bytes: {saved}")

    def assert_copied(self):
        for source, dest in zip(self.sources, self.dests):
            self.assertEqual((dest / "replaced").read_bytes(),
                             (source / "replaced").read_bytes())
            self.assertFalse((dest / "destination-only").exists())

    def test_success_keeps_both_pairs_originals(self):
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_copied()
        self.assert_custody()
        for dest in self.dests:
            stamp = (dest / ".last_success").read_text().strip()
            self.assertTrue((dest / ".deleted" / stamp).is_dir())

    def test_second_pair_failure_keeps_both_pairs_originals(self):
        unreadable = self.sources[1] / "unreadable"
        unreadable.write_bytes(b"cannot transfer this file")
        unreadable.chmod(0)
        self.addCleanup(unreadable.chmod, 0o600)
        result = self.run_backup()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("row 3: rsync failed", result.stderr)
        self.assertIn("Permission denied", result.stderr)
        self.assertIn("code 23", result.stderr)
        self.assert_copied()
        self.assert_custody()
        self.assertTrue((self.dests[0] / ".last_success").is_file())
        self.assertFalse((self.dests[1] / ".last_success").exists())

    def assert_mutant_loses_custody(self, old, new):
        original = self.script.read_text()
        self.assertEqual(original.count(old), 1, "mutant anchor must be unique")
        self.script = self.base / "mutant.sh"
        self.script.write_text(original.replace(old, new))
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_copied()
        with self.assertRaisesRegex(AssertionError, "custody"):
            self.assert_custody()

    def test_without_both_backup_flags_loses_custody(self):
        self.assert_mutant_loses_custody(' --backup --backup-dir="$DELETED_DIR"', "")

    def test_wrong_backup_directory_loses_custody(self):
        self.assert_mutant_loses_custody('--backup-dir="$DELETED_DIR"',
                                       '--backup-dir="$DEST/other-archive/$STAMP"')


if __name__ == "__main__":
    unittest.main()
