"""Run the real Bash wrapper against isolated pairs and a recording rsync."""
import csv
import json
import os
import signal
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
HEADER = "reader\tsource\tdestination\texcludes\n"


def real_rsync3():
    # [LAW:single-enforcer] both test paths use the same rsync 3 requirement.
    diagnostics = []
    for candidate in (shutil.which("rsync"), "/opt/homebrew/bin/rsync"):
        if candidate is None:
            diagnostics.append("rsync not found on PATH")
            continue
        try:
            version = subprocess.run([candidate, "--version"], capture_output=True,
                                     text=True, timeout=10)
        except (OSError, subprocess.TimeoutExpired) as error:
            diagnostics.append(f"{candidate}: {error}")
            continue
        if version.returncode == 0 and "version 3" in version.stdout:
            return candidate
        diagnostics.append(f"{candidate}: exit {version.returncode}: "
                           f"{version.stdout}{version.stderr}")
    raise AssertionError("real rsync version 3 is required; " + "; ".join(diagnostics))


class BackupPairsTest(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp(prefix="backup_pairs_", dir="/tmp"))
        self.addCleanup(shutil.rmtree, self.base)
        self.script = HERE / "backup_mirror.sh"
        self.table = self.base / "pairs.tsv"
        self.calls = self.base / "calls.jsonl"
        self.excludes = self.base / "rules"
        self.excludes.write_text("/.deleted/\n/.last_success\n")
        self.sources = [self.base / f"source {i}" for i in range(2)]
        self.dests = [self.base / f"dest {i}" for i in range(2)]
        for i, source in enumerate(self.sources):
            source.mkdir()
            (source / "keep").write_text(f"payload {i}")
        self.rows = [["ssd", str(s), str(d), "rules"]
                     for s, d in zip(self.sources, self.dests)]
        self.bin = self.base / "bin"
        self.bin.mkdir()
        mount = self.bin / "mount"
        mount.write_text(f"#!/bin/bash\nprintf 'fixture on {self.base} (test)\\n'\n")
        mount.chmod(0o755)
        self.rsync = self.bin / "rsync"
        self.rsync.write_text(f"#!{sys.executable}\n" + '''import json, os, pathlib, sys
args = sys.argv[1:]
base = pathlib.Path(os.environ["PAIR_BASE"]).resolve()
consumption_log = pathlib.Path(os.environ["PAIR_CALLS"]).with_suffix(".excludes.jsonl")
paths = args[-2:] + [os.environ["PAIR_CALLS"], str(consumption_log)]
paths += [a.split("=", 1)[1] for a in args if a.startswith(("--backup-dir=", "--exclude-from="))]
for path in paths:
    if not pathlib.Path(path).resolve().is_relative_to(base):
        sys.exit("fake rsync refuses path outside fixture: " + path)
# [LAW:one-source-of-truth] record consumed bytes; real rsync owns rule behavior.
consumed = {a.split("=", 1)[1]: pathlib.Path(a.split("=", 1)[1]).read_bytes()
            for a in args if a.startswith("--exclude-from=")}
with consumption_log.open("a") as stream:
    stream.write(json.dumps({"args": args, "excludes": {
        path: data.hex() for path, data in consumed.items()}}) + "\\n")
with open(os.environ["PAIR_CALLS"], "a") as stream:
    stream.write(json.dumps(args) + "\\n")
src, dest = map(pathlib.Path, args[-2:])
if str(src) == os.environ.get("PAIR_FAIL"):
    print("Number of files: 0")
    sys.exit(23)
# [LAW:one-source-of-truth] rsync owns all copying semantics.
real = os.environ["PAIR_REAL_RSYNC"]
os.execv(real, [real] + args)
''')
        self.rsync.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("BACKUP_", "PAIR_"))}
        self.env.update(BACKUP_PAIRS=str(self.table), BACKUP_RSYNC=str(self.rsync),
                        BACKUP_MOUNT_POINT=str(self.base), BACKUP_MOUNT=str(mount),
                        PAIR_BASE=str(self.base), PAIR_CALLS=str(self.calls),
                        BACKUP_SRC=str(self.sources[0]), BACKUP_DEST=str(self.dests[0]),
                        BACKUP_EXCLUDES=str(self.excludes),
                        PATH=str(self.bin) + os.pathsep + os.defpath)
        self.env["PAIR_REAL_RSYNC"] = real_rsync3()

    def run_backup(self, table_text=None, **changes):
        self.table.write_text(table_text if table_text is not None else
                              HEADER + "".join("\t".join(r) + "\n" for r in self.rows))
        script = self.script
        text = script.read_text()
        for seam in ("BACKUP_SRC", "BACKUP_DEST", "BACKUP_EXCLUDES", "BACKUP_PAIRS",
                     "BACKUP_RSYNC", "BACKUP_MOUNT_POINT", "BACKUP_MOUNT"):
            self.assertIn(seam, text, f"W7: refusing to start backup: missing seam {seam}")
        proc = subprocess.Popen(["/bin/bash", str(script)], env=dict(self.env, **changes),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        def cleanup():
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()
        self.addCleanup(cleanup)
        stdout, stderr = proc.communicate(timeout=10)
        return subprocess.CompletedProcess(proc.args, proc.returncode, stdout, stderr)

    def recorded(self):
        return [json.loads(line) for line in self.calls.read_text().splitlines()]

    def assert_refused(self, result, reason, row="3"):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(len(result.stderr.splitlines()), 1, result.stderr)
        self.assertIn("backup_mirror: FATAL:", result.stderr)
        self.assertIn("row " + row, result.stderr)
        self.assertIn(reason, result.stderr)
        self.assertFalse(self.calls.exists(), result.stdout)
        self.assertFalse(any(d.exists() for d in self.dests))

    def test_two_rows_copy_with_custody_flags(self):
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.recorded()
        self.assertEqual(len(calls), 2)
        for i, (args, source, dest) in enumerate(zip(calls, self.sources, self.dests)):
            self.assertEqual((dest / "keep").read_text(), f"payload {i}")
            stamp = (dest / ".last_success").read_text().strip()
            self.assertRegex(stamp, r"^\d{8}T\d{6}$")
            self.assertEqual(args, ["-a", "--delete", "--backup",
                                   f"--backup-dir={dest}/.deleted/{stamp}",
                                   f"--exclude-from={self.excludes}", "--stats",
                                   "--human-readable", f"{source}/", f"{dest}/"])
            self.assertTrue((dest / ".deleted").is_dir())

    def test_missing_second_source_stops_all(self):
        self.rows[1][1] = str(self.base / "missing")
        self.assert_refused(self.run_backup(), "source dir missing")

    def test_legacy_overrides_control_copy(self):
        # [LAW:behavior-not-structure] distinct defaults expose ignored overrides.
        tool = self.base / "tool"
        tool.mkdir()
        self.script = tool / "backup_mirror.sh"
        shutil.copyfile(HERE / "backup_mirror.sh", self.script)
        (tool / "rules").write_text("alternate rules\n")
        (tool / "backup_pairs.tsv").write_text(
            HEADER + "\t".join(self.rows[1]) + "\n")
        del self.env["BACKUP_PAIRS"]
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.dests[0] / "keep").read_text(), "payload 0")
        self.assertFalse(self.dests[1].exists())
        calls = self.recorded()
        self.assertEqual(len(calls), 1)
        stamp = (self.dests[0] / ".last_success").read_text().strip()
        self.assertEqual(calls[0], ["-a", "--delete", "--backup",
                                    f"--backup-dir={self.dests[0]}/.deleted/{stamp}",
                                    f"--exclude-from={self.excludes}", "--stats",
                                    "--human-readable", f"{self.sources[0]}/",
                                    f"{self.dests[0]}/"])

    def test_explicit_pairs_ignore_legacy_overrides(self):
        source = self.base / "legacy source"
        source.mkdir()
        (source / "keep").write_text("legacy bytes")
        dest = self.base / "legacy dest"
        rules = self.base / "legacy rules"
        rules.write_text("legacy excludes\n")
        self.env.update(BACKUP_SRC=str(source), BACKUP_DEST=str(dest),
                        BACKUP_EXCLUDES=str(rules))
        self.test_two_rows_copy_with_custody_flags()
        self.assertFalse(dest.exists())

    def test_unreadable_second_source_names_cause_and_row(self):
        self.sources[1].chmod(0)
        self.addCleanup(self.sources[1].chmod, 0o755)
        result = self.run_backup()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("backup_mirror: FATAL: row 3: cannot read source directory:",
                      result.stderr)
        self.assertIn(str(self.sources[1]), result.stderr)
        self.assertFalse(self.calls.exists())
        self.assertFalse(any(d.exists() for d in self.dests))

    def test_empty_excludes_names_invalid_pair_and_row(self):
        self.rows[1][3] = ""
        self.assert_refused(self.run_backup(), "invalid pair")

    def test_empty_second_source_stops_all(self):
        empty = self.base / "empty"
        empty.mkdir()
        self.rows[1][1] = str(empty)
        self.assert_refused(self.run_backup(), "source dir is empty")

    def test_missing_second_excludes_stops_all(self):
        self.rows[1][3] = "missing"
        self.assert_refused(self.run_backup(), "exclude list missing")

    def test_same_disk_second_destination_stops_all(self):
        for disk in ("memit", "Development", "backups"):
            with self.subTest(disk=disk):
                self.rows[1][2] = f"/Volumes/{disk}/unsafe"
                self.assert_refused(self.run_backup(), "same physical disk")

    def test_bare_volume_second_destination_stops_all(self):
        for disk in ("memit", "Development", "backups"):
            with self.subTest(disk=disk):
                self.rows[1][2] = f"/Volumes/{disk}"
                self.assert_refused(self.run_backup(), "same physical disk")

    def test_missing_rsync(self):
        self.assert_refused(self.run_backup(BACKUP_RSYNC=str(self.base / "missing")),
                            "rsync not found", row="2")

    def test_unmounted(self):
        self.assert_refused(self.run_backup(BACKUP_MOUNT_POINT="/missing"),
                            "not mounted", row="2")

    def test_failed_second_rsync_has_no_success(self):
        result = self.run_backup(PAIR_FAIL=str(self.sources[1]))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("row 3", result.stderr)
        self.assertEqual(len(self.recorded()), 2)
        self.assertTrue((self.dests[0] / ".last_success").is_file())
        self.assertFalse((self.dests[1] / ".last_success").exists())

    def test_failed_first_stops_before_second(self):
        result = self.run_backup(PAIR_FAIL=str(self.sources[0]))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("row 2", result.stderr)
        self.assertEqual(len(self.recorded()), 1)
        self.assertFalse(any((d / ".last_success").exists() for d in self.dests))

    def test_dash_excludes_and_unterminated_last_row(self):
        # [LAW:behavior-not-structure] without excludes, --delete removes dest-only dirs.
        (self.sources[1] / ".deleted").mkdir()
        self.rows[1][3] = "-"
        text = HEADER + "\n".join("\t".join(r) for r in self.rows)
        result = self.run_backup(table_text=text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(self.recorded()), 2)
        stamp = (self.dests[1] / ".last_success").read_text().strip()
        self.assertEqual(self.recorded()[1], ["-a", "--delete", "--backup",
                                            f"--backup-dir={self.dests[1]}/.deleted/{stamp}",
                                            "--stats", "--human-readable",
                                            f"{self.sources[1]}/", f"{self.dests[1]}/"])
        self.assertTrue((self.dests[1] / ".last_success").exists())

    def test_invalid_table_refuses_before_copy(self):
        for text, reason in [("", "empty pairs table"),
                             ("wrong\n", "invalid header"),
                             (HEADER + "ssd\t\twhere\trules\n", "invalid pair"),
                             (HEADER + "ssd\tfrom\twhere\trules\textra\n", "invalid pair"),
                             (HEADER + "unknown\tfrom\twhere\trules\n", "unknown reader")]:
            with self.subTest(text=text):
                result = self.run_backup(table_text=text)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(reason, result.stderr)
                self.assertFalse(self.calls.exists())

    def test_excludes_must_be_beside_table(self):
        self.rows[1][3] = "../rules"
        self.assert_refused(self.run_backup(), "excludes must be next to table")

    def test_missing_table(self):
        result = self.run_backup(BACKUP_PAIRS=str(self.base / "missing"))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("pairs table missing", result.stderr)
        self.assertFalse(self.calls.exists())

    def test_mount_inspection_failure(self):
        (self.bin / "mount").write_text("#!/bin/bash\nexit 3\n")
        self.assert_refused(self.run_backup(), "cannot inspect mounts", row="2")

    def test_empty_archives_are_removed_but_custody_is_kept(self):
        for dest in self.dests:
            (dest / ".deleted/empty").mkdir(parents=True)
            (dest / ".deleted/kept").mkdir()
            (dest / ".deleted/kept/payload").write_text("prior bytes")
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for dest in self.dests:
            self.assertFalse((dest / ".deleted/empty").exists())
            self.assertEqual((dest / ".deleted/kept/payload").read_text(), "prior bytes")

    def test_r_excludes_are_passed_to_rsync(self):
        common = (HERE / "backup_mirror.excludes").read_bytes()
        r_rules = (HERE / "backup_mirror.R.excludes").read_bytes()
        self.assertEqual(r_rules, common + b"/.claude/worktrees/\n/graft/\n")
        (self.base / "R.rules").write_bytes(r_rules)
        self.rows[1][3] = "R.rules"
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        stamp = (self.dests[1] / ".last_success").read_text().strip()
        self.assertEqual(self.recorded()[1], ["-a", "--delete", "--backup",
                                            f"--backup-dir={self.dests[1]}/.deleted/{stamp}",
                                            f"--exclude-from={self.base / 'R.rules'}",
                                            "--stats", "--human-readable",
                                            f"{self.sources[1]}/", f"{self.dests[1]}/"])

    def test_r_rsync_consumes_complete_excludes_bytes(self):
        expected = (HERE / "backup_mirror.R.excludes").read_bytes()
        rules = self.base / "R.rules"
        rules.write_bytes(expected)
        self.rows[1][3] = rules.name
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        records = [json.loads(line) for line in
                   self.calls.with_suffix(".excludes.jsonl").read_text().splitlines()]
        self.assertEqual([record["args"] for record in records], self.recorded())
        self.assertEqual(records[1]["excludes"], {str(rules): expected.hex()})

    def test_r_excludes_block_worktrees_and_graft_but_copy_keep(self):
        # [LAW:behavior-not-structure] destination sentinels prove consumed rules act.
        # [LAW:no-silent-failure] this behavior requires rsync 3, never a skip.
        rsync = real_rsync3()
        source = self.base / "R source"
        for folder in (".claude/worktrees/x", "graft/x", "keep/x",
                       "nested/graft/x", "nested/.claude/worktrees/x", "graftish/x"):
            sentinel = source / folder / "sentinel"
            sentinel.parent.mkdir(parents=True)
            sentinel.write_text(folder)
        self.rows[1][1] = str(source)
        rules = self.base / "R.rules"
        rules.write_bytes((HERE / "backup_mirror.R.excludes").read_bytes())
        self.rows[1][3] = rules.name
        result = self.run_backup(BACKUP_RSYNC=rsync)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for folder in (".claude/worktrees", "graft", "nested/graft"):
            self.assertFalse((self.dests[1] / folder).exists(), folder)
        for folder in ("keep/x", "nested/.claude/worktrees/x", "graftish/x"):
            self.assertEqual((self.dests[1] / folder / "sentinel").read_text(), folder)

    def test_fake_preserves_child_symlink_without_copying_external_bytes(self):
        # [LAW:behavior-not-structure] archive mode preserves links, not target bytes.
        outside = Path(tempfile.mkdtemp(prefix="backup_pairs_outside_", dir="/tmp"))
        self.addCleanup(shutil.rmtree, outside)
        sentinel = outside / "sentinel"
        sentinel.write_bytes(b"OUTSIDE FIXTURE BYTES")
        link = self.sources[0] / "external"
        link.symlink_to(sentinel)
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        copied = self.dests[0] / "external"
        self.assertTrue(copied.is_symlink(), "external target bytes copied instead of link")
        self.assertEqual(os.readlink(copied), os.readlink(link))
        for directory, _, files in os.walk(self.dests[0], followlinks=False):
            for name in files:
                path = Path(directory) / name
                if not path.is_symlink():
                    self.assertNotIn(b"OUTSIDE FIXTURE BYTES", path.read_bytes())

    def test_fake_replaces_destination_child_symlink_without_changing_external_bytes(self):
        # [LAW:behavior-not-structure] archive mode replaces the link, not its target.
        outside = Path(tempfile.mkdtemp(prefix="backup_pairs_outside_", dir="/tmp"))
        self.addCleanup(shutil.rmtree, outside)
        sentinel = outside / "sentinel"
        sentinel.write_bytes(b"OUTSIDE ORIGINAL")
        self.dests[0].mkdir()
        child = self.dests[0] / "keep"
        child.symlink_to(sentinel)
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(sentinel.read_bytes(), b"OUTSIDE ORIGINAL")
        self.assertFalse(child.is_symlink())
        self.assertEqual(child.read_text(), "payload 0")

    def test_other_readers_do_not_run(self):
        self.rows += [["intel", "unavailable", "remote:data", "-"],
                      ["gdrive", "unavailable", "gdrive:data", "-"]]
        result = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(self.recorded()), 2)

    def test_master_table_has_current_pairs(self):
        with (HERE / "backup_pairs.tsv").open(newline="") as stream:
            rows = list(csv.reader(stream, delimiter="\t"))
        self.assertEqual(rows, [HEADER.rstrip("\n").split("\t"),
            ["ssd", "/Volumes/memit/llm-database-poc-mirror",
             "/Users/robertrhu/Backups/memit/llm-database-poc-mirror", "backup_mirror.excludes"],
            ["intel", "/Volumes/memit/llm-database-poc-mirror",
             "robertrhu_node2@192.168.10.2:memit_copy", "backup_mirror.excludes"],
            ["gdrive", "/Volumes/memit/llm-database-poc-mirror",
             "gdrive:memit-backup/llm-database-poc-mirror", "backup_mirror.excludes"]])


if __name__ == "__main__":
    unittest.main()
