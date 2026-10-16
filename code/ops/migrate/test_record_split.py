"""Tests for record_split: tracked record, attested bulk or governed payload per leaf."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import record_split as R

TOOL = Path(R.__file__).resolve()
BIG = 3 * 1024 * 1024  # a "large" file: far above any plausible text/record size heuristic


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_state(root: Path) -> dict:
    """Every entry under root with its bytes or link text, without following links."""
    state = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames + filenames:
            p = Path(dirpath, name)
            if p.is_symlink():
                state[str(p)] = ("link", os.readlink(p))
            elif p.is_file():
                state[str(p)] = ("file", p.read_bytes())
            else:
                state[str(p)] = ("dir",)
    return state


class Fixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.unit = self.base / "unit"
        self.unit.mkdir()

    def put(self, rel: str, data: bytes) -> bytes:
        p = self.unit / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return data

    def attest(self, leaves, attested_by="operator", regenerate="python run.py --seed 0", name="att.json"):
        p = self.base / name
        p.write_text(json.dumps({"attested_by": attested_by, "regenerate": regenerate,
                                 "leaves": [{"path": k, "sha256": v} for k, v in leaves]}))
        return p

    def split(self, *attestations):
        return {row.path: row for row in R.split_unit(self.unit, list(attestations))}

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)],
                              capture_output=True, text=True, timeout=120)


class Controls(Fixture):
    def test_launch_json_and_log_are_tracked_regardless_of_size_folder_and_ignore(self):
        # SPEC.md:640 controls. Both sit under the old results/ folder, both are large,
        # and a .gitignore would ignore them: none of that may change the class.
        self.put(".gitignore", b"results/\n*.log\n*.json\n")
        launch = b'{"run": "c10r", "seed": 0, "pad": "' + b"x" * BIG + b'"}\n'
        self.put("results/launch.json", launch)
        self.put("results/train.log", b"step 1 loss 0.5\n" * (BIG // 16 + 1))
        rows = self.split()
        self.assertEqual(rows["results/launch.json"].cls, R.TRACKED)
        self.assertEqual(rows["results/train.log"].cls, R.TRACKED)
        self.assertEqual(rows["results/launch.json"].sha256, sha(launch))
        self.assertEqual(rows[".gitignore"].cls, R.TRACKED)

    def test_large_binary_without_attestation_is_governed_payload_never_bulk(self):
        self.put("results/overlay.pt", b"\x00\x01\x02\xff" * (BIG // 4))
        rows = self.split()
        self.assertEqual(rows["results/overlay.pt"].cls, R.PAYLOAD)
        self.assertNotIn(R.BULK, {r.cls for r in rows.values()})

    def test_extension_is_not_the_rule(self):
        self.put("binary.json", b"\x00\x00binary")
        self.put("notes.pt", b"plain text that happens to end in .pt\n")
        self.put("latin1.log", "café\n".encode("latin-1"))
        rows = self.split()
        self.assertEqual(rows["binary.json"].cls, R.PAYLOAD)
        self.assertEqual(rows["notes.pt"].cls, R.TRACKED)
        self.assertEqual(rows["latin1.log"].cls, R.PAYLOAD)

    def test_small_binary_without_attestation_is_payload(self):
        self.put("tiny.bin", b"\x00")
        self.assertEqual(self.split()["tiny.bin"].cls, R.PAYLOAD)

    def test_text_record_split_across_read_chunks_stays_text(self):
        # a multi-byte UTF-8 char straddling the read chunk boundary is still text
        data = b"a" * (R.CHUNK - 1) + "é".encode("utf-8") + b"\n"
        self.put("record.log", data)
        self.assertEqual(self.split()["record.log"].cls, R.TRACKED)

    def test_bytes_ending_in_a_cut_utf8_sequence_are_not_text(self):
        self.put("cut.log", b"loss 0.5 " + "é".encode("utf-8")[:1])
        self.assertEqual(self.split()["cut.log"].cls, R.PAYLOAD)

    def test_rows_are_sorted_by_utf8_path_bytes(self):
        for rel in ("b.txt", "a/z.txt", "a.txt", "Z.txt"):
            self.put(rel, b"t\n")
        paths = [r.path for r in R.split_unit(self.unit, [])]
        self.assertEqual(paths, sorted(paths, key=lambda p: p.encode("utf-8", "surrogateescape")))

    def test_filename_with_newline_is_a_leaf(self):
        self.put("odd\nname.log", b"line\n")
        self.assertEqual(self.split()["odd\nname.log"].cls, R.TRACKED)


class Attestation(Fixture):
    def test_attested_leaf_with_matching_digest_is_bulk(self):
        data = self.put("results/overlay.pt", b"\x00\xff" * (BIG // 2))
        self.put("results/launch.json", b'{"seed": 0}\n')
        att = self.attest([("results/overlay.pt", sha(data))])
        rows = self.split(att)
        self.assertEqual(rows["results/overlay.pt"].cls, R.BULK)
        self.assertEqual(rows["results/launch.json"].cls, R.TRACKED)

    def test_attestation_for_other_leaf_leaves_large_binary_as_payload(self):
        a = self.put("a.pt", b"\x00a")
        self.put("b.pt", b"\x00b" * (BIG // 2))
        rows = self.split(self.attest([("a.pt", sha(a))]))
        self.assertEqual(rows["a.pt"].cls, R.BULK)
        self.assertEqual(rows["b.pt"].cls, R.PAYLOAD)

    def test_changed_digest_refuses(self):
        self.put("overlay.pt", b"\x00new bytes")
        with self.assertRaisesRegex(R.Refusal, "digest"):
            self.split(self.attest([("overlay.pt", sha(b"\x00old bytes"))]))

    def test_attested_path_absent_from_unit_refuses(self):
        self.put("overlay.pt", b"\x00")
        with self.assertRaisesRegex(R.Refusal, "not a leaf"):
            self.split(self.attest([("gone.pt", sha(b"\x00"))]))

    def test_duplicate_attested_path_refuses(self):
        data = self.put("overlay.pt", b"\x00")
        a1 = self.attest([("overlay.pt", sha(data))], name="a1.json")
        a2 = self.attest([("overlay.pt", sha(data))], name="a2.json")
        with self.assertRaisesRegex(R.Refusal, "twice"):
            self.split(a1, a2)

    def test_attested_link_refuses(self):
        self.put("real.pt", b"\x00")
        os.symlink("real.pt", self.unit / "link.pt")
        with self.assertRaisesRegex(R.Refusal, "not a regular file"):
            self.split(self.attest([("link.pt", sha(b"real.pt"))]))

    def test_unknown_attester_refuses(self):
        data = self.put("overlay.pt", b"\x00")
        with self.assertRaisesRegex(R.Refusal, "attested_by"):
            self.split(self.attest([("overlay.pt", sha(data))], attested_by="someone"))

    def test_empty_regenerate_refuses(self):
        data = self.put("overlay.pt", b"\x00")
        with self.assertRaisesRegex(R.Refusal, "regenerate"):
            self.split(self.attest([("overlay.pt", sha(data))], regenerate=" "))

    def test_malformed_digest_refuses(self):
        self.put("overlay.pt", b"\x00")
        with self.assertRaisesRegex(R.Refusal, "sha256"):
            self.split(self.attest([("overlay.pt", "ABC")]))

    def test_malformed_attestation_file_refuses(self):
        p = self.base / "bad.json"
        p.write_text("{not json")
        self.put("overlay.pt", b"\x00")
        with self.assertRaises(R.Refusal):
            self.split(p)

    def test_attestation_without_leaves_refuses(self):
        p = self.base / "empty.json"
        p.write_text(json.dumps({"attested_by": "operator", "regenerate": "x", "leaves": []}))
        self.put("overlay.pt", b"\x00")
        with self.assertRaisesRegex(R.Refusal, "leaves"):
            self.split(p)


class Refusals(Fixture):
    def test_link_inside_root_is_tracked_and_not_followed(self):
        self.put("data/big.pt", b"\x00" * 16)
        os.symlink("data/big.pt", self.unit / "alias.pt")
        row = self.split()["alias.pt"]
        self.assertEqual(row.cls, R.TRACKED)
        self.assertEqual(row.kind, "link")
        self.assertEqual(row.link, "data/big.pt")
        self.assertIsNone(row.sha256)

    def test_link_escaping_root_by_dotdot_refuses(self):
        (self.base / "outside.pt").write_bytes(b"\x00")
        os.symlink("../outside.pt", self.unit / "esc.pt")
        with self.assertRaisesRegex(R.Refusal, "escapes"):
            self.split()

    def test_absolute_link_refuses(self):
        (self.base / "outside.pt").write_bytes(b"\x00")
        os.symlink(str(self.base / "outside.pt"), self.unit / "abs.pt")
        with self.assertRaisesRegex(R.Refusal, "escapes"):
            self.split()

    def test_link_to_directory_is_not_walked(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.pt").write_bytes(b"\x00")
        self.put("sub/x.txt", b"t\n")
        os.symlink("sub", self.unit / "subalias")
        rows = self.split()
        self.assertEqual(set(rows), {"sub/x.txt", "subalias"})
        self.assertEqual(rows["subalias"].kind, "link")

    def test_special_file_refuses(self):
        os.mkfifo(self.unit / "pipe")
        with self.assertRaisesRegex(R.Refusal, "special"):
            self.split()

    def test_nested_git_root_refuses(self):
        self.put("inner/.git/HEAD", b"ref: refs/heads/main\n")
        with self.assertRaisesRegex(R.Refusal, "nested"):
            self.split()

    def test_root_that_is_a_link_refuses(self):
        alias = self.base / "alias"
        os.symlink(self.unit, alias)
        with self.assertRaisesRegex(R.Refusal, "root"):
            R.split_unit(alias, [])

    def test_file_changed_during_hash_refuses(self):
        self.put("growing.log", b"line\n")
        real = R._digest

        def append_after_read(path):
            out = real(path)
            with open(path, "ab") as fh:
                fh.write(b"more\n")
            return out

        with mock.patch.object(R, "_digest", append_after_read):
            with self.assertRaisesRegex(R.Refusal, "changed"):
                self.split()


class Cli(Fixture):
    def test_cli_writes_sorted_json_and_leaves_source_unchanged(self):
        self.put("results/launch.json", b'{"seed": 0}\n')
        self.put("results/run.log", b"ok\n")
        big = self.put("results/overlay.pt", b"\x00\xff" * (BIG // 2))
        reg = self.put("results/regen.pt", b"\x00regen")
        att = self.attest([("results/regen.pt", sha(reg))])
        before = tree_state(self.unit)
        out = self.base / "split.json"
        proc = self.cli("--root", self.unit, "--attestation", att, "--out", out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(tree_state(self.unit), before)
        doc = json.loads(out.read_text())
        classes = {row["path"]: row["class"] for row in doc["leaves"]}
        self.assertEqual(classes, {"results/launch.json": R.TRACKED, "results/run.log": R.TRACKED,
                                   "results/overlay.pt": R.PAYLOAD, "results/regen.pt": R.BULK})
        sizes = {row["path"]: row["size"] for row in doc["leaves"]}
        self.assertEqual(sizes["results/overlay.pt"], len(big))
        self.assertEqual([r["path"] for r in doc["leaves"]], sorted(classes))

    def test_cli_refuses_existing_out_without_overwriting(self):
        self.put("a.log", b"x\n")
        out = self.base / "split.json"
        out.write_bytes(b"keep me")
        proc = self.cli("--root", self.unit, "--out", out)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(out.read_bytes(), b"keep me")

    def test_cli_refuses_out_inside_root(self):
        self.put("a.log", b"x\n")
        before = tree_state(self.unit)
        proc = self.cli("--root", self.unit, "--out", self.unit / "split.json")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(tree_state(self.unit), before)

    def test_cli_refusal_exits_2_and_writes_nothing(self):
        self.put("overlay.pt", b"\x00new")
        att = self.attest([("overlay.pt", sha(b"\x00old"))])
        out = self.base / "split.json"
        proc = self.cli("--root", self.unit, "--attestation", att, "--out", out)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("digest", proc.stderr)
        self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
