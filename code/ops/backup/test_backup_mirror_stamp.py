"""Caller stamps on the real wrapper, with isolated recording boundaries."""
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent


class BackupMirrorStampTest(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(prefix="backup_stamp_", dir="/tmp"))
        self.addCleanup(shutil.rmtree, self.base)
        self.script = HERE / "backup_mirror.sh"
        self.sources = [self.base / f"source {i}" for i in range(2)]
        self.dests = [self.base / f"dest {i}" for i in range(2)]
        for source in self.sources:
            source.mkdir()
            (source / "payload").write_bytes(b"source bytes\n")
        self.excludes = self.base / "rules"
        self.excludes.write_bytes((HERE / "backup_mirror.excludes").read_bytes())
        self.table = self.base / "pairs.tsv"
        self.table.write_text("reader\tsource\tdestination\texcludes\n" + "".join(
            f"ssd\t{source}\t{dest}\trules\n"
            for source, dest in zip(self.sources, self.dests)))
        self.mount_calls = self.base / "mount.jsonl"
        self.rsync_calls = self.base / "rsync.jsonl"
        self.mount_calls.write_bytes(b"")
        self.rsync_calls.write_bytes(b"")
        mount = self.base / "mount"
        mount.write_text(f"#!{sys.executable}\n" + '''import json, os, pathlib
base = pathlib.Path(os.environ["STAMP_BASE"]).resolve()
with (base / "mount.jsonl").open("a") as stream:
    stream.write(json.dumps(["mount"]) + "\\n")
print(f"fixture on {base} (test)")
''')
        mount.chmod(0o755)
        rsync = self.base / "rsync"
        rsync.write_text(f"#!{sys.executable}\n" + '''import json, os, pathlib, sys, time
args = sys.argv[1:]
base = pathlib.Path(os.environ["STAMP_BASE"]).resolve()
paths = args[-2:] + [a.split("=", 1)[1] for a in args
                    if a.startswith(("--backup-dir=", "--exclude-from="))]
for path in paths:
    if not pathlib.Path(path).resolve().is_relative_to(base):
        sys.exit("recording rsync refuses path outside fixture: " + path)
calls = base / "rsync.jsonl"
first = not calls.read_bytes()
with calls.open("a") as stream:
    stream.write(json.dumps(args) + "\\n")
# Cross a clock second between rows so per-row stamp reads cannot hide.
if first and os.environ.get("STAMP_CROSS_SECOND") == "1":
    second = int(time.time())
    deadline = time.monotonic() + 3
    while int(time.time()) == second:
        if time.monotonic() >= deadline:
            sys.exit("clock did not advance at the recording boundary")
        time.sleep(0.01)
print("Number of files: 1")
''')
        rsync.chmod(0o755)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("BACKUP_", "STAMP_"))}
        self.env.update(BACKUP_PAIRS=str(self.table), BACKUP_RSYNC=str(rsync),
                        BACKUP_MOUNT=str(mount), BACKUP_MOUNT_POINT=str(self.base.resolve()),
                        BACKUP_SRC=str(self.sources[0]), BACKUP_DEST=str(self.dests[0]),
                        BACKUP_EXCLUDES=str(self.excludes), STAMP_BASE=str(self.base))

    def manifest(self):
        # [LAW:behavior-not-structure] observe all fixture bytes and modes, including logs.
        result = []
        for path in [self.base, *sorted(self.base.rglob("*"))]:
            mode = path.lstat().st_mode
            kind = stat.S_IFMT(mode)
            data = path.read_bytes() if stat.S_ISREG(mode) else b""
            result.append((str(path.relative_to(self.base)), kind, data, stat.S_IMODE(mode)))
        return result

    def run_backup(self, stamp):
        text = self.script.read_text()
        for seam in ("BACKUP_SRC", "BACKUP_DEST", "BACKUP_EXCLUDES", "BACKUP_PAIRS",
                     "BACKUP_RSYNC", "BACKUP_MOUNT", "BACKUP_MOUNT_POINT"):
            self.assertRegex(text, r"(?<![A-Za-z0-9_])" + seam + r"(?![A-Za-z0-9_])",
                             f"W7: refusing to start backup: missing seam {seam}")
        env = dict(self.env)
        if stamp is None:
            env["STAMP_CROSS_SECOND"] = "1"
        else:
            env["BACKUP_STAMP"] = stamp
        return subprocess.run(["/bin/bash", str(self.script)], env=env,
                              capture_output=True, text=True, timeout=10)

    def assert_success(self, supplied):
        before = self.manifest()
        proc = self.run_backup(supplied)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "")
        stamps = [(dest / ".last_success").read_bytes() for dest in self.dests]
        self.assertRegex(stamps[0], rb"\A[0-9]{8}T[0-9]{6}\n\Z")
        stamp = stamps[0][:-1].decode()
        if supplied is not None:
            self.assertEqual(stamp, supplied)
        self.assertEqual(stamps, [(stamp + "\n").encode()] * 2)
        calls = [json.loads(line) for line in self.rsync_calls.read_text().splitlines()]
        self.assertEqual(len(calls), 2)
        for args, source, dest in zip(calls, self.sources, self.dests):
            self.assertEqual(args[-2:], [str(source) + "/", str(dest) + "/"])
            self.assertEqual([arg for arg in args if arg.startswith("--backup-dir=")],
                             [f"--backup-dir={dest}/.deleted/{stamp}"])
        self.assertEqual(proc.stdout.splitlines(), [line for source, dest in
                         zip(self.sources, self.dests) for line in
                         (f"backup_mirror: {stamp} start  {source} -> {dest}",
                          "Number of files: 1", f"backup_mirror: {stamp} OK")])
        self.assertEqual(self.mount_calls.read_text().splitlines(), ['["mount"]'] * 2)
        self.assertNotEqual(self.manifest(), before)

    def test_recording_clock_source_and_call_count(self):
        text = self.script.read_text()
        self.assertEqual(text.count("/bin/date"), 1)
        clock_stamp = "20010203T040506"
        clock_calls = self.base / "clock.jsonl"
        clock = self.base / "clock"
        # [LAW:effects-at-boundaries] observe the clock through its real argv interface.
        clock.write_text(f"#!{sys.executable}\n"
                         "import json, sys\n"
                         f"with open({str(clock_calls)!r}, 'a') as stream:\n"
                         "    stream.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                         f"print({clock_stamp!r})\n")
        clock.chmod(0o755)
        self.script = self.base / "backup_mirror.sh"
        self.script.write_text(text.replace("/bin/date", str(clock)))
        for supplied, expected, calls in (
                (None, clock_stamp, [["+%Y%m%dT%H%M%S"]]),
                ("20261023T104500", "20261023T104500", [])):
            with self.subTest(supplied=supplied):
                for log in (clock_calls, self.mount_calls, self.rsync_calls):
                    log.write_bytes(b"")
                self.assert_success(supplied)
                self.assertEqual([json.loads(line) for line in
                                  clock_calls.read_text().splitlines()], calls)
                self.assertEqual([(dest / ".last_success").read_bytes()
                                  for dest in self.dests],
                                 [(expected + "\n").encode()] * 2)

    def test_unset_uses_one_clock_stamp_across_rows(self):
        self.assert_success(None)

    def test_valid_stamp_positive_control(self):
        self.assert_success("20261023T104500")

    def test_valid_old_stamp(self):
        self.assert_success("19991231T235959")

    def test_invalid_stamps_have_no_effect(self):
        for stamp in ("", " ", "A0261022T010203", "20261022T01020", "20261022T0102030",
                      "20261022X010203", "20261022T010203\n", " 20261022T010203",
                      "20261022T010203 ", "../20261022T010203"):
            with self.subTest(stamp=stamp):
                before = self.manifest()
                proc = self.run_backup(stamp)
                self.assertEqual(proc.returncode, 1, proc.stderr)
                self.assertRegex(proc.stderr, r"\Abackup_mirror: FATAL: BACKUP_STAMP [^\n]+\n\Z")
                self.assertEqual(proc.stdout, "")
                self.assertEqual(self.mount_calls.read_bytes(), b"")
                self.assertEqual(self.rsync_calls.read_bytes(), b"")
                self.assertEqual(self.manifest(), before)


if __name__ == "__main__":
    unittest.main()
