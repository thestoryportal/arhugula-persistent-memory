"""T392 exact prose repair; R264c binds the preserved target to its route."""
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


# R261 base pin from 42b5478c, captured before repair; no Git history needed.
BASE_BLOBS = {
    "code/research/visualization/README.md":
        "ec1190bde4d3a0607d8745bc83e993ae195fdea1",
}
R264C_TARGET = (
    "/Volumes/memit/llmdb-preserved/icm21-20261013/M/visualization/"
    "qwen25_3b_2layer_structure.onnx"
)


def read_file(path):
    # [LAW:single-enforcer] All file reads use the held-parent regular-file reader.
    with fdsafe.hold_root(str(path.parent)) as parent:
        return fdsafe.read_named(parent, path.name)


class RepairVisualizationReadmeTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ["LLMDB_ROOT"])
        # [LAW:one-source-of-truth] The approved route owns the replacement path.
        with io.StringIO(read_file(self.root /
                "program/migrations/icm21/units/S246/routes.tsv").decode("utf-8"),
                newline="") as stream:
            rows = [row for row in csv.DictReader(stream, delimiter="\t")
                    if row["source"].endswith(
                        "/visualization/qwen25_3b_2layer_structure.onnx")]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        # [LAW:parse-dont-validate] Reject malformed fields at the TSV boundary.
        for value in row.values():
            self.assertTrue(value)
            self.assertFalse(any(c in value for c in "\0\t\r\n"))
            value.encode("utf-8", errors="strict")
            self.assertEqual(str(PurePosixPath(value)), value)
            self.assertNotIn("..", PurePosixPath(value).parts)
        self.assertEqual(row["requirement_id"], "MV-048")
        self.assertEqual(row["kind"], "file")
        self.assertTrue(PurePosixPath(row["target"]).is_absolute())
        self.assertEqual(row["target"], R264C_TARGET)
        self.new = ("`" + row["target"] + "`").encode()

    def test_exact_repair_bytes(self):
        for name, pin in BASE_BLOBS.items():
            with self.subTest(file=name):
                current = read_file(self.root / name)
                lines = current.splitlines(keepends=True)
                old = b"`qwen25_3b_2layer_structure.onnx` (in this folder)"
                self.assertLess(15, len(lines))
                self.assertEqual(lines[15].count(self.new), 1)
                self.assertNotIn(old, current)
                lines[15] = lines[15].replace(self.new, old)
                reverted = b"".join(lines)
                # [LAW:behavior-not-structure] Exact bytes are the repair contract.
                blob = b"blob " + str(len(reverted)).encode() + b"\0" + reverted
                self.assertEqual(hashlib.sha1(blob).hexdigest(), pin)

    def test_reader_find_clean(self):
        # [LAW:effects-at-boundaries] Invoke only the lexical reader, never ONNX.
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
