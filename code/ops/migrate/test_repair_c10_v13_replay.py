"""T262 exact reader repair; R261 permits depth-1, host-independent checks."""
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import unittest

from ops.migrate import fdsafe


# R261 pins from c584ec8b, captured before the repair; no Git history needed.
BASE_BLOBS = {
    "code/lab/track_c/autoresearch_c10/v13_build.py":
        "3d009aa46591fe53228e9cefd7397a320f95e3ac",
    "code/lab/track_c/autoresearch_c10/v13_law3_equivalence.sh":
        "b6fe9367949b414a4febac371e3bf3438ef46c23",
}


def read_file(path):
    # [LAW:single-enforcer] Every file read uses the held-parent regular-file boundary.
    with fdsafe.hold_root(str(path.parent)) as parent:
        return fdsafe.read_named(parent, path.name)


def read_tsv(path):
    with io.StringIO(read_file(path).decode("utf-8"), newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


class RepairC10V13ReplayTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ["LLMDB_ROOT"])
        # [LAW:one-source-of-truth] Approved rows own the replacement spellings.
        self.rows = [row for row in read_tsv(
            self.root / "program/migrations/icm21/repairs.tsv")
            if row["step"] == "262"]
        self.assertTrue(self.rows, "T262 must have approved repairs")
        for row in self.rows:
            self.assertIn(row["file"], BASE_BLOBS)
            # [LAW:parse-dont-validate] Reject malformed paths at the TSV boundary.
            for field in ("file", "old_text", "new_text"):
                value = row[field]
                self.assertTrue(value)
                self.assertFalse(any(c in value for c in "\0\t\r\n"))
                value.encode("utf-8", errors="strict")
                self.assertEqual(str(PurePosixPath(value)), value)
                self.assertNotIn("..", PurePosixPath(value).parts)
            self.assertFalse(PurePosixPath(row["file"]).is_absolute())
            self.assertTrue(PurePosixPath(row["old_text"]).is_absolute())
            self.assertTrue(PurePosixPath(row["new_text"]).is_absolute())
            row["line"] = int(row["line"])
            self.assertGreater(row["line"], 0)

    def test_exact_repair_bytes(self):
        for name, pin in BASE_BLOBS.items():
            with self.subTest(file=name):
                current = read_file(self.root / name)
                lines = current.splitlines(keepends=True)
                for row in self.rows:
                    if row["file"] != name:
                        continue
                    index = row["line"] - 1
                    old, new = row["old_text"].encode(), row["new_text"].encode()
                    self.assertLess(index, len(lines))
                    self.assertEqual(lines[index].count(new), 1)
                    self.assertNotIn(old, current)
                    lines[index] = lines[index].replace(new, old)
                reverted = b"".join(lines)
                # [LAW:behavior-not-structure] Exact bytes are the repair contract.
                blob = b"blob " + str(len(reverted)).encode() + b"\0" + reverted
                self.assertEqual(hashlib.sha1(blob).hexdigest(), pin)

    def test_preserved_map_chain(self):
        path_map = read_tsv(self.root / "_index/path-map.tsv")
        relocations = read_tsv(self.root / "_index/icm21-path-map.tsv")
        for row in self.rows:
            with self.subTest(file=row["file"], line=row["line"]):
                first = [r for r in path_map if r["old"] == row["old_text"]]
                self.assertEqual(len(first), 1)
                second = [r for r in relocations if r["old"] == first[0]["new"]]
                self.assertEqual(len(second), 1)
                self.assertEqual(second[0]["new"], row["new_text"])
                self.assertEqual(second[0]["disposition"], "preserved")

    def test_read_file_refuses_symlink(self):
        root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.addCleanup(shutil.rmtree, root)
        target = root / "target"
        target.write_bytes(b"regular file")
        self.assertEqual(read_file(target), b"regular file")
        leaf = root / "link"
        leaf.symlink_to(target)
        with self.assertRaises(fdsafe.Refusal):
            read_file(leaf)

    def test_read_file_refuses_fifo(self):
        root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.addCleanup(shutil.rmtree, root)
        target = root / "target"
        target.write_bytes(b"regular file")
        self.assertEqual(read_file(target), b"regular file")
        leaf = root / "fifo"
        os.mkfifo(leaf)
        with self.assertRaises(fdsafe.Refusal):
            read_file(leaf)

    def test_reader_find_clean(self):
        # [LAW:effects-at-boundaries] Invoke only the lexical reader, never launch.
        result = subprocess.run(
            [sys.executable, "-B", "code/ops/migrate/reader_find.py", "--check",
             "--paths", *BASE_BLOBS, "--relocations", "_index/icm21-path-map.tsv"],
            cwd=self.root, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {"stale": [], "unverified": []})


if __name__ == "__main__":
    unittest.main()
