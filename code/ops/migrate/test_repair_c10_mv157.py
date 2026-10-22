"""T387 exact reader repair; R387 permits depth-1, host-independent checks."""
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


# R387 pin from 5d6b9a8c, captured before the repair; no Git history needed.
BASE_BLOBS = {
    "code/lab/track_c/autoresearch_c10/sandbox_settings.py":
        "ce349a6913e35e65de1f6d16338f6d9b0308aec3",
}


def read_file(path):
    # [LAW:single-enforcer] All file reads use the held-parent regular-file reader.
    with fdsafe.hold_root(str(path.parent)) as parent:
        return fdsafe.read_named(parent, path.name)


def read_tsv(path):
    with io.StringIO(read_file(path).decode("utf-8"), newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


class RepairC10MV157Tests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ["LLMDB_ROOT"])
        # [LAW:one-source-of-truth] Approved rows own the replacement spellings.
        self.rows = [row for row in read_tsv(
            self.root / "program/migrations/icm21/repairs.tsv")
            if row["step"] == "387"]
        self.assertEqual(len(self.rows), 1, "T387 must have one approved repair")
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
                self.assertEqual(first[0]["disposition"], "move")
                second = [r for r in relocations if r["old"] == first[0]["new"]]
                self.assertEqual(len(second), 1)
                self.assertEqual(second[0]["new"], row["new_text"])
                self.assertEqual(second[0]["disposition"], "preserved")
                self.assertEqual(second[0]["unit"], "S238")

    def test_reader_find_clean(self):
        # [LAW:effects-at-boundaries] Invoke only the lexical reader, never launch.
        result = subprocess.run(
            [sys.executable, "-B", "code/ops/migrate/reader_find.py", "--check",
             "--paths", *BASE_BLOBS, "--relocations", "_index/icm21-path-map.tsv"],
            cwd=self.root, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {"stale": [], "unverified": []})


class SafeReadTests(unittest.TestCase):
    def test_symlink_leaf_refused(self):
        root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.addCleanup(shutil.rmtree, root)
        target = root / "target"
        target.write_bytes(b"regular file")
        self.assertEqual(read_file(target), b"regular file")
        leaf = root / "leaf"
        leaf.symlink_to(target)
        with self.assertRaises(fdsafe.Refusal):
            read_file(leaf)

    def test_fifo_leaf_refused(self):
        root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.addCleanup(shutil.rmtree, root)
        target = root / "target"
        target.write_bytes(b"regular file")
        self.assertEqual(read_file(target), b"regular file")
        leaf = root / "leaf"
        os.mkfifo(leaf)
        with self.assertRaises(fdsafe.Refusal):
            read_file(leaf)


if __name__ == "__main__":
    unittest.main()
