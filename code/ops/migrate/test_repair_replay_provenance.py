"""T263 exact reader repairs under R261/R263, including depth-1 CI."""
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


# Base c584ec8b, captured before repairs; CI needs no Git history.
BASE_BLOBS = {
    "code/lab/track_c/autoresearch_c10/replay_exp2/setup_replay.sh":
        "50d707bea4217523d6ad415461ee79e8098bf465",
    "code/memit/patches/replay_provenance.sh":
        "17682b8ccc4a0c7b72a4a329194599345957f175",
}
OLD_PARENT = "/Volumes/memit/llm-database-poc-mirror/"
PRESERVED_PARENT = "/Volumes/memit/llmdb-preserved/icm21-20261013/parent/"


def read_file(path):
    # [LAW:single-enforcer] R261(4) binds every read to a held parent.
    with fdsafe.hold_root(str(path.parent)) as parent:
        return fdsafe.read_named(parent, path.name)


def read_tsv(path):
    with io.StringIO(read_file(path).decode("utf-8"), newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


class RepairReplayProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ["LLMDB_ROOT"])
        # [LAW:one-source-of-truth] G5-approved rows own replacement spellings.
        self.rows = [row for row in read_tsv(
            self.root / "program/migrations/icm21/repairs.tsv")
            if row["step"] == "263"]
        self.assertEqual(len(self.rows), 4)
        for row in self.rows:
            self.assertIn(row["file"], BASE_BLOBS)
            # [LAW:parse-dont-validate] Check raw row paths at the TSV boundary.
            for field in ("file", "old_text", "new_text"):
                value = row[field]
                self.assertTrue(value)
                self.assertFalse(any(c in value for c in "\0\t\r\n"))
                value.encode("utf-8", errors="strict")
                self.assertEqual(str(PurePosixPath(value)), value)
                self.assertNotIn("..", PurePosixPath(value).parts)
            self.assertFalse(PurePosixPath(row["file"]).is_absolute())
            self.assertTrue(row["old_text"].startswith(OLD_PARENT))
            self.assertEqual(row["new_text"], PRESERVED_PARENT +
                             row["old_text"][len(OLD_PARENT):])
            row["line"] = int(row["line"])
            self.assertGreater(row["line"], 0)
        self.path_map = read_tsv(self.root / "_index/path-map.tsv")
        self.relocations = read_tsv(self.root / "_index/icm21-path-map.tsv")

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
                # [LAW:behavior-not-structure] Pin every byte, including suffixes.
                blob = b"blob " + str(len(reverted)).encode() + b"\0" + reverted
                self.assertEqual(hashlib.sha1(blob).hexdigest(), pin)

    def test_preserved_maps(self):
        for row in self.rows:
            with self.subTest(file=row["file"], line=row["line"]):
                first = [r for r in self.path_map if r["old"] == row["old_text"]]
                self.assertEqual(len(first), 1)
                disposition = first[0]["disposition"]
                self.assertIn(disposition, ("move", "quarantine"))
                if disposition == "move":
                    second = [r for r in self.relocations
                              if r["old"] == first[0]["new"]]
                    self.assertEqual(len(second), 1)
                    self.assertEqual(second[0]["new"], row["new_text"])
                    self.assertEqual(second[0]["disposition"], "preserved")
                else:
                    self.assertEqual(first[0]["new"], "")
                    self.assertFalse([r for r in self.relocations
                                      if r["old"] == row["old_text"]])

    def test_reader_find_clean(self):
        for name in BASE_BLOBS:
            read_file(self.root / name)
        # [LAW:effects-at-boundaries] Run the lexical checker, never the readers.
        result = subprocess.run(
            [sys.executable, "-B", "code/ops/migrate/reader_find.py", "--check",
             "--paths", *BASE_BLOBS, "--relocations", "_index/icm21-path-map.tsv"],
            cwd=self.root, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {"stale": [], "unverified": []})


class ReadFileTests(unittest.TestCase):
    def test_refuses_symlink_leaf(self):
        root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.addCleanup(shutil.rmtree, root)
        target = root / "target"
        target.write_bytes(b"regular file")
        self.assertEqual(read_file(target), b"regular file")
        leaf = root / "leaf"
        leaf.symlink_to(target)
        with self.assertRaises(fdsafe.Refusal):
            read_file(leaf)

    def test_refuses_fifo_leaf(self):
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
