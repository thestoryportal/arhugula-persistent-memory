"""Tests for record_split: tracked record, attested bulk or governed payload per leaf."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import types
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


@contextlib.contextmanager
def before_open(match, action):
    """Run action once, just before the first os.open call that match(path, kwargs) accepts."""
    real = os.open
    fired = []

    def hook(path, flags, *args, **kwargs):
        if not fired and match(os.fspath(path), kwargs):
            fired.append(True)
            action()
        return real(path, flags, *args, **kwargs)

    with mock.patch.object(os, "open", hook):
        yield fired


@contextlib.contextmanager
def fstat_reports(call_no, **delta):
    """The call_no-th os.fstat reports its fields shifted by delta (the M46 witness)."""
    real = os.fstat
    calls = []

    def fake(fd):
        st = real(fd)
        calls.append(fd)
        if len(calls) != call_no:
            return st
        fields = {k: getattr(st, k) for k in ("st_mode", "st_dev", "st_ino", "st_size", "st_mtime_ns")}
        return types.SimpleNamespace(**{k: v + delta.get(k, 0) for k, v in fields.items()})

    with mock.patch.object(os, "fstat", fake):
        yield calls


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

    def main(self, *args):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = R.main([str(a) for a in args])
        return code, err.getvalue()

    def assertRefusedCleanly(self, proc):
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        lines = proc.stderr.strip().splitlines()
        self.assertEqual(len(lines), 1, proc.stderr)
        self.assertTrue(lines[0].startswith("record_split: refused: "), proc.stderr)


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

    def test_record_kind_raises_to_record_and_encoding_never_lowers_it(self):
        # Ruling 1: launch/check JSON, manifests, notebooks and logs are records whatever
        # their bytes (SPEC.md:632-633). The record-kind list only raises; it never lowers.
        self.put("binary.json", b"\x00\x00binary")
        self.put("latin1.log", "café\n".encode("latin-1"))
        self.put("science.LOG", "step 1 loss 0.5\n".encode("utf-16"))
        self.put("rows.jsonl", b"\xff\xfe\x00")
        self.put("run.ipynb", b"\x00nb")
        self.put("RUN_Manifest.tsv", b"\x00\x01")
        self.put("notes.pt", b"plain text that happens to end in .pt\n")
        self.put("latin1.bin", "café\n".encode("latin-1"))
        rows = self.split()
        for rel in ("binary.json", "latin1.log", "science.LOG", "rows.jsonl", "run.ipynb",
                    "RUN_Manifest.tsv", "notes.pt"):
            self.assertEqual(rows[rel].cls, R.TRACKED, rel)
        self.assertEqual(rows["latin1.bin"].cls, R.PAYLOAD)

    def test_small_binary_without_attestation_is_payload(self):
        self.put("tiny.bin", b"\x00")
        self.assertEqual(self.split()["tiny.bin"].cls, R.PAYLOAD)

    def test_text_record_split_across_read_chunks_stays_text(self):
        # a multi-byte UTF-8 char straddling the read chunk boundary is still text
        data = b"a" * (R.CHUNK - 1) + "é".encode("utf-8") + b"\n"
        self.put("record.log", data)
        self.assertEqual(self.split()["record.log"].cls, R.TRACKED)

    def test_bytes_ending_in_a_cut_utf8_sequence_are_not_text(self):
        self.put("cut.bin", b"loss 0.5 " + "é".encode("utf-8")[:1])
        self.assertEqual(self.split()["cut.bin"].cls, R.PAYLOAD)

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

    def test_link_to_exactly_the_parent_refuses(self):
        os.symlink("..", self.unit / "up")
        with self.assertRaisesRegex(R.Refusal, "escapes"):
            self.split()

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


class RecordKind(Fixture):
    def test_attested_record_kind_file_refuses_and_names_it(self):
        for rel in ("launch.json", "check.jsonl", "nb.ipynb", "train.log", "MANIFEST.sha256"):
            with self.subTest(rel=rel):
                data = self.put(rel, b'{"seed": 0}\n')
                with self.assertRaisesRegex(R.Refusal, rel.replace(".", r"\.")):
                    self.split(self.attest([(rel, sha(data))], name=rel + ".att"))
                (self.unit / rel).unlink()

    def test_attested_record_kind_cli_exits_2(self):
        data = self.put("launch.json", b'{"run": "scientific-run", "seed": 0}\n')
        out = self.base / "split.json"
        proc = self.cli("--root", self.unit, "--attestation", self.attest([("launch.json", sha(data))]),
                        "--out", out)
        self.assertRefusedCleanly(proc)
        self.assertIn("launch.json", proc.stderr)
        self.assertFalse(out.exists())

    def test_attested_text_that_is_not_a_record_is_bulk(self):
        data = self.put("regen/table.txt", b"col\n1\n2\n")
        rows = self.split(self.attest([("regen/table.txt", sha(data))]))
        self.assertEqual(rows["regen/table.txt"].cls, R.BULK)


class AttestationShape(Fixture):
    def doc(self, **over):
        doc = {"attested_by": "operator", "regenerate": "python run.py",
               "leaves": [{"path": "x.pt", "sha256": "0" * 64}]}
        doc.update(over)
        return doc

    def refused(self, doc, pattern):
        with self.assertRaisesRegex(R.Refusal, pattern):
            R.parse_attestation(doc, "att.json")

    def test_top_level_not_an_object(self):
        self.refused([self.doc()], "not a JSON object")

    def test_attester_of_wrong_type(self):
        self.refused(self.doc(attested_by=[]), "attested_by")
        self.refused(self.doc(attested_by={"operator": 1}), "attested_by")

    def test_regenerate_of_wrong_type(self):
        self.refused(self.doc(regenerate=5), "regenerate")
        self.refused(self.doc(regenerate=["python", "run.py"]), "regenerate")

    def test_leaves_not_a_list(self):
        self.refused(self.doc(leaves="x.pt"), "non-empty list")
        self.refused(self.doc(leaves={"path": "x.pt", "sha256": "0" * 64}), "non-empty list")

    def test_leaf_item_not_an_object(self):
        self.refused(self.doc(leaves=["x.pt"]), "needs a path")

    def test_leaf_path_not_a_string(self):
        self.refused(self.doc(leaves=[{"path": 5, "sha256": "0" * 64}]), "needs a path")
        self.refused(self.doc(leaves=[{"sha256": "0" * 64}]), "needs a path")

    def test_leaf_digest_not_a_string(self):
        self.refused(self.doc(leaves=[{"path": "x.pt", "sha256": 5}]), "sha256")

    def test_unreadable_attestation_refuses(self):
        self.put("x.pt", b"\x00")
        with self.assertRaisesRegex(R.Refusal, "unreadable"):
            self.split(self.base / "absent.json")
        with self.assertRaisesRegex(R.Refusal, "unreadable"):
            self.split(self.base)

    def test_attestation_not_utf8_refuses(self):
        self.put("x.pt", b"\x00")
        p = self.base / "latin1.json"
        p.write_bytes('{"attested_by": "opérateur"}'.encode("latin-1"))
        with self.assertRaisesRegex(R.Refusal, "unreadable"):
            self.split(p)


class ExitContract(Fixture):
    def test_invalid_inputs_exit_2_with_one_refusal_and_no_traceback(self):
        self.put("x.pt", b"\x00")
        (self.base / "afile").write_bytes(b"")
        good = {"attested_by": "operator", "regenerate": "python run.py",
                "leaves": [{"path": "x.pt", "sha256": sha(b"\x00")}]}

        def att(name, payload):
            p = self.base / name
            p.write_bytes(payload if isinstance(payload, bytes) else json.dumps(payload).encode())
            return p

        cases = {
            "missing root": ["--root", self.base / "absent"],
            "root is a file": ["--root", self.base / "afile"],
            "missing out parent": ["--out", self.base / "missing" / "split.json"],
            "out parent is a file": ["--out", self.base / "afile" / "split.json"],
            "out names no file": ["--out", self.base / ".."],
            "out is the current directory": ["--out", "."],
            "attestation missing": ["--attestation", self.base / "absent.json"],
            "attestation is a directory": ["--attestation", self.base],
            "attestation not utf-8": ["--attestation", att("l1.json", '{"a": "é"}'.encode("latin-1"))],
            "attestation not json": ["--attestation", att("bad.json", b"{not json")],
            "attestation a list": ["--attestation", att("list.json", [good])],
            "attested_by a list": ["--attestation", att("by.json", {**good, "attested_by": []})],
            "leaf not an object": ["--attestation", att("item.json", {**good, "leaves": ["x.pt"]})],
            "path not a string": ["--attestation",
                                  att("path.json", {**good, "leaves": [{"path": 5, "sha256": sha(b"\x00")}]})],
            "sha256 not a string": ["--attestation",
                                    att("dig.json", {**good, "leaves": [{"path": "x.pt", "sha256": 5}]})],
            "regenerate not a string": ["--attestation", att("reg.json", {**good, "regenerate": 5})],
        }
        for name, extra in cases.items():
            with self.subTest(case=name):
                args = {"--root": self.unit, "--out": self.base / "split.json"}
                attestations = []
                for flag, value in zip(extra[::2], extra[1::2]):
                    if flag == "--attestation":
                        attestations.append(value)
                    else:
                        args[flag] = value
                argv = [x for kv in args.items() for x in kv]
                for a in attestations:
                    argv += ["--attestation", a]
                self.assertRefusedCleanly(self.cli(*argv))
                self.assertFalse((self.base / "split.json").exists())


class Binding(Fixture):
    """Ruling 2: size and hash come from the object that was read, and the output's parent
    is the directory that was checked."""

    def leaf(self, data=b"\x00ORIGINAL"):
        self.put("sample.bin", data)
        return self.unit / "sample.bin"

    def at_leaf_open(self, path, action):
        return before_open(lambda p, kw: p == path.name and kw.get("dir_fd") is not None, action)

    def assertChanged(self, path, action):
        with self.at_leaf_open(path, action) as fired:
            with self.assertRaisesRegex(R.Refusal, "changed"):
                self.split()
        self.assertTrue(fired)

    def test_same_size_rewrite_in_place_refuses(self):
        p = self.leaf()
        st = os.lstat(p)

        def rewrite():
            with open(p, "r+b") as fh:
                fh.write(b"\x00REPLACED")
            os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))

        self.assertChanged(p, rewrite)

    def test_size_only_change_refuses(self):
        p = self.leaf()
        st = os.lstat(p)

        def grow_keep_mtime():
            with open(p, "ab") as fh:
                fh.write(b"MORE")
            os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))

        self.assertChanged(p, grow_keep_mtime)

    def test_replaced_file_with_same_size_and_mtime_refuses(self):
        p = self.leaf()
        st = os.lstat(p)

        def replace():
            new = self.unit / "sample.new"
            new.write_bytes(b"\x00REPLACED")
            os.utime(new, ns=(st.st_atime_ns, st.st_mtime_ns))
            os.replace(new, p)
            self.assertNotEqual(os.lstat(p).st_ino, st.st_ino)

        self.assertChanged(p, replace)

    def test_leaf_swapped_for_a_symlink_refuses_and_never_reads_the_target(self):
        p = self.leaf()
        external = self.base / "external"
        external.write_bytes(b"\x00SECRET OUTSIDE THE UNIT")

        def swap():
            p.unlink()
            p.symlink_to(external)

        with self.at_leaf_open(p, swap):
            with self.assertRaisesRegex(R.Refusal, "symlink"):
                self.split()

    def test_leaf_removed_before_open_refuses(self):
        p = self.leaf()
        self.assertChanged(p, p.unlink)

    def test_symlink_swap_cli_exits_2(self):
        p = self.leaf()
        external = self.base / "external"
        external.write_bytes(b"\x00SECRET OUTSIDE THE UNIT")
        out = self.base / "split.json"

        def swap():
            p.unlink()
            p.symlink_to(external)

        with self.at_leaf_open(p, swap):
            code, err = self.main("--root", self.unit, "--out", out)
        self.assertEqual(code, 2, err)
        self.assertIn("sample.bin", err)
        self.assertFalse(out.exists())

    def test_open_fd_on_another_device_refuses_before_any_byte_is_hashed(self):
        self.leaf()
        with fstat_reports(1, st_dev=1) as calls, \
                mock.patch.object(hashlib, "sha256", side_effect=hashlib.sha256) as hashers:
            with self.assertRaisesRegex(R.Refusal, "changed before"):
                self.split()
        self.assertEqual(len(calls), 1)
        hashers.assert_not_called()

    def test_open_fd_that_changes_during_the_read_refuses(self):
        self.leaf()
        with fstat_reports(2, st_size=1) as calls:
            with self.assertRaisesRegex(R.Refusal, "changed"):
                self.split()
        self.assertEqual(len(calls), 2)

    def test_out_parent_that_is_a_symlink_refuses(self):
        self.put("a.log", b"x\n")
        real = self.base / "realdest"
        real.mkdir()
        (self.base / "dest").symlink_to(real, target_is_directory=True)
        code, err = self.main("--root", self.unit, "--out", self.base / "dest" / "split.json")
        self.assertEqual(code, 2, err)
        self.assertEqual(list(real.iterdir()), [])

    def test_out_parent_swapped_after_the_check_still_writes_outside_the_unit(self):
        leaf = self.leaf()
        dest = self.base / "dest"
        dest.mkdir()
        moved = self.base / "moved-dest"
        before = tree_state(self.unit)

        def swap():
            dest.rename(moved)
            dest.symlink_to(self.unit, target_is_directory=True)

        with self.at_leaf_open(leaf, swap) as fired:
            code, err = self.main("--root", self.unit, "--out", dest / "split.json")
        self.assertTrue(fired)
        self.assertEqual(code, 0, err)
        self.assertEqual(tree_state(self.unit), before)
        self.assertTrue((moved / "split.json").exists())

    def test_out_parent_moved_into_the_unit_refuses_and_keeps_the_written_file(self):
        self.leaf()
        dest = self.base / "dest"
        dest.mkdir()

        def move_in():
            dest.rename(self.unit / "dest")

        with before_open(lambda p, kw: p == "split.json" and "dir_fd" in kw, move_in) as fired:
            code, err = self.main("--root", self.unit, "--out", dest / "split.json")
        self.assertTrue(fired)
        self.assertEqual(code, 2, err)
        self.assertIn("split.json", err)
        self.assertTrue((self.unit / "dest" / "split.json").exists())  # never deleted


class Errno(Fixture):
    """Ruling 7: an OSError on the unit, a leaf or the output is one exit-2 refusal line."""

    def test_filesystem_errors_exit_2_with_one_refusal_naming_path_and_errno(self):
        self.put("record.log", b"good\n")
        out = self.base / "out.json"
        loop = self.base / "loop"
        loop.symlink_to(loop)

        def unwritable_parent():
            d = self.base / "ro"
            d.mkdir()
            d.chmod(0o500)
            self.addCleanup(d.chmod, 0o700)
            return ["--root", self.unit, "--out", d / "out.json"], "EACCES"

        def unreadable_leaf():
            leaf = self.unit / "record.log"
            leaf.chmod(0)
            self.addCleanup(leaf.chmod, 0o600)
            return ["--root", self.unit, "--out", out], "EACCES"

        def unreadable_subdir():
            d = self.unit / "sub"
            d.mkdir()
            d.chmod(0)
            self.addCleanup(d.chmod, 0o700)
            return ["--root", self.unit, "--out", out], "EACCES"

        cases = {
            "unwritable out parent": unwritable_parent,
            "unreadable leaf": unreadable_leaf,
            "unreadable subdirectory": unreadable_subdir,
            "root through a link loop": lambda: (["--root", loop / "unit", "--out", out], "ELOOP"),
            "out parent is a link loop": lambda: (["--root", self.unit, "--out", loop / "out.json"],
                                                  "ENOTDIR|ELOOP"),
            "out parent through a link loop": lambda: (["--root", self.unit, "--out", loop / "d" / "out.json"],
                                                       "ELOOP"),
        }
        for name, make in cases.items():
            with self.subTest(case=name):
                argv, code = make()
                proc = self.cli(*argv)
                self.assertRefusedCleanly(proc)
                self.assertRegex(proc.stderr, code)
                self.assertFalse(out.exists())

    def test_attestation_name_with_newline_is_one_refusal_line(self):
        self.put("x.pt", b"\x00")
        proc = self.cli("--root", self.unit, "--attestation", self.base / "missing\natt.json",
                        "--out", self.base / "out.json")
        self.assertRefusedCleanly(proc)

    def test_root_that_is_a_file_is_refused_as_the_root(self):
        f = self.base / "afile"
        f.write_bytes(b"")
        with self.assertRaisesRegex(R.Refusal, "unit root"):
            R.split_unit(f, [])

    def test_failed_write_refuses_and_leaves_the_output_in_place(self):
        self.put("a.log", b"x\n")
        out = self.base / "split.json"
        with mock.patch.object(os, "write", side_effect=OSError(28, "No space left on device")):
            code, err = self.main("--root", self.unit, "--out", out)
        self.assertEqual(code, 2, err)
        self.assertIn("ENOSPC", err)
        self.assertIn("split.json", err)
        self.assertTrue(out.exists())

    def test_directory_listing_error_refuses(self):
        self.put("a.log", b"x\n")
        with mock.patch.object(os, "scandir", side_effect=OSError(5, "Input/output error")):
            with self.assertRaisesRegex(R.Refusal, "EIO"):
                self.split()

    def test_entry_gone_between_listing_and_stat_refuses(self):
        self.put("a.log", b"x\n")
        gone = self.put("gone.bin", b"\x00")
        real = os.scandir

        class Listing:
            def __init__(self, fd):
                with real(fd) as it:
                    self.entries = list(it)
                (self.unit_path / "gone.bin").unlink()

            def __enter__(self):
                return iter(self.entries)

            def __exit__(self, *exc):
                return False

        Listing.unit_path = self.unit
        self.assertEqual(gone, b"\x00")
        with mock.patch.object(os, "scandir", Listing):
            with self.assertRaisesRegex(R.Refusal, "ENOENT"):
                self.split()

    def test_link_that_stops_being_a_link_before_readlink_refuses(self):
        os.symlink("a.log", self.unit / "alias")
        self.put("a.log", b"x\n")
        real = os.readlink

        def swap_then_read(name, *args, **kwargs):
            (self.unit / "alias").unlink()
            (self.unit / "alias").write_bytes(b"now a file")
            return real(name, *args, **kwargs)

        with mock.patch.object(os, "readlink", swap_then_read):
            with self.assertRaisesRegex(R.Refusal, "EINVAL"):
                self.split()

    def test_read_error_on_an_open_leaf_refuses(self):
        self.put("a.bin", b"\x00")
        with mock.patch.object(os, "fstat", side_effect=OSError(5, "Input/output error")):
            with self.assertRaisesRegex(R.Refusal, "a.bin: EIO"):
                self.split()

    def test_leaf_gone_after_its_read_refuses(self):
        p = self.put("a.bin", b"\x00")
        leaf = self.unit / "a.bin"
        real = os.fstat
        calls = []

        def unlink_on_second(fd):
            calls.append(fd)
            if len(calls) == 2:
                leaf.unlink()
            return real(fd)

        self.assertEqual(p, b"\x00")
        with mock.patch.object(os, "fstat", unlink_on_second):
            with self.assertRaisesRegex(R.Refusal, "ENOENT"):
                self.split()


class WalkBinding(Fixture):
    """Ruling 5: the walk enters each directory through its parent's fd."""

    def outside(self):
        out = self.base / "outside"
        (out / "b").mkdir(parents=True)
        secret = b"\x00SECRET OUTSIDE THE UNIT"
        (out / "secret.bin").write_bytes(secret)
        (out / "b" / "x.bin").write_bytes(secret)
        return out, sha(secret)

    def at_open(self, name, action):
        return before_open(lambda p, kw: p == name and kw.get("dir_fd") is not None, action)

    def test_directory_swapped_for_a_symlink_refuses(self):
        self.put("sub/own.bin", b"\x00OWN")
        outside, _ = self.outside()
        sub = self.unit / "sub"

        def swap():
            sub.rename(self.base / "saved-sub")
            sub.symlink_to(outside, target_is_directory=True)

        out = self.base / "split.json"
        with self.at_open("sub", swap) as fired:
            code, err = self.main("--root", self.unit, "--out", out)
        self.assertTrue(fired)
        self.assertEqual(code, 2, err)
        self.assertRegex(err, "sub: (ENOTDIR|ELOOP)")
        self.assertFalse(out.exists())

    def test_directory_replaced_by_another_directory_refuses(self):
        self.put("sub/own.bin", b"\x00OWN")
        sub = self.unit / "sub"

        def replace():
            sub.rename(self.base / "saved-sub")
            sub.mkdir()
            (sub / "secret.bin").write_bytes(b"\x00SECRET")

        with self.at_open("sub", replace) as fired:
            with self.assertRaisesRegex(R.Refusal, "changed during the walk"):
                self.split()
        self.assertTrue(fired)

    def parent_swapped_before(self, name):
        own = self.put("a/b/x.bin", b"\x00OWN BYTES")
        outside, secret_sha = self.outside()
        a = self.unit / "a"

        def swap():
            a.rename(self.base / "saved-a")
            a.symlink_to(outside, target_is_directory=True)

        with self.at_open(name, swap) as fired:
            rows = self.split()
        self.assertTrue(fired)
        self.assertEqual(rows["a/b/x.bin"].sha256, sha(own))
        self.assertNotEqual(rows["a/b/x.bin"].sha256, secret_sha)

    def test_directory_is_entered_through_the_bound_parent_not_its_path(self):
        self.parent_swapped_before("b")

    def test_leaf_is_opened_through_the_bound_directory_not_its_path(self):
        self.parent_swapped_before("x.bin")


class LiveRoot(Fixture):
    """Ruling 6: containment compares with the held root fd's real path at check time."""

    def test_root_relocated_and_out_parent_moved_into_it_refuses_and_keeps_the_file(self):
        for relink in (False, True):
            with self.subTest(relink=relink):
                base = self.base / f"case{int(relink)}"
                unit = base / "unit"
                unit.mkdir(parents=True)
                (unit / "record.log").write_bytes(b"good\n")
                dest = base / "dest"
                dest.mkdir()
                moved = base / "moved-unit"

                def relocate():
                    unit.rename(moved)
                    if relink:
                        unit.symlink_to(moved, target_is_directory=True)
                    dest.rename(moved / "dest")

                match = lambda p, kw: p == "split.json" and kw.get("dir_fd") is not None
                with before_open(match, relocate) as fired:
                    code, err = self.main("--root", unit, "--out", dest / "split.json")
                self.assertTrue(fired)
                self.assertEqual(code, 2, err)
                self.assertIn("split.json", err)
                self.assertTrue((moved / "dest" / "split.json").exists())  # never deleted

    def test_out_parent_inside_the_relocated_root_is_refused_before_the_write(self):
        self.put("record.log", b"good\n")
        hold = self.base / "hold"
        (hold / "dest").mkdir(parents=True)

        def relocate():
            hold.rename(self.base / "hold-old")
            self.unit.rename(hold)
            (self.base / "hold-old" / "dest").rename(hold / "dest")

        match = lambda p, kw: p == str(hold / "dest") and "dir_fd" not in kw
        with before_open(match, relocate) as fired:
            code, err = self.main("--root", self.unit, "--out", hold / "dest" / "split.json")
        self.assertTrue(fired)
        self.assertEqual(code, 2, err)
        self.assertIn("inside the unit", err)
        self.assertFalse((hold / "dest" / "split.json").exists())

    def test_the_scan_reads_the_held_root(self):
        own = self.put("record.log", b"good\n")
        dest = self.base / "dest"
        dest.mkdir()

        def replace_root():
            self.unit.rename(self.base / "held")
            self.unit.mkdir()
            (self.unit / "other.log").write_bytes(b"other\n")

        match = lambda p, kw: p == str(dest) and "dir_fd" not in kw
        with before_open(match, replace_root) as fired:
            code, err = self.main("--root", self.unit, "--out", dest / "split.json")
        self.assertTrue(fired)
        self.assertEqual(code, 0, err)
        doc = json.loads((dest / "split.json").read_text())
        self.assertEqual([(r["path"], r["sha256"]) for r in doc["leaves"]], [("record.log", sha(own))])


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


@contextlib.contextmanager
def fail_call(module, name, call_no, err=OSError(5, "Input/output error"), after=False):
    """The call_no-th module.name call raises err; after=True runs the real call first."""
    real = getattr(module, name)
    calls = []

    def hook(*args, **kwargs):
        calls.append(args)
        if len(calls) == call_no and not after:
            raise err
        result = real(*args, **kwargs)
        if len(calls) == call_no:
            raise err
        return result

    with mock.patch.object(module, name, hook):
        yield calls


# A child process holds the os.open hook, so a blocking open fails the test by timeout.
FIFO_FOR_DIRECTORY = r"""
import os, sys
sys.path.insert(0, os.path.dirname(sys.argv[1]))
import record_split as R
unit, out = sys.argv[2], sys.argv[3]
real = os.open
fired = []
def hook(path, flags, *args, **kwargs):
    if path == "sub" and kwargs.get("dir_fd") is not None and not fired:
        fired.append(True)
        os.rmdir(os.path.join(unit, "sub"))
        os.mkfifo(os.path.join(unit, "sub"))
    return real(path, flags, *args, **kwargs)
os.open = hook
sys.exit(R.main(["--root", unit, "--out", out]))
"""


class Round3(Fixture):
    """Rulings 8-10: F_GETPATH and close errors are refusals, leaf refusals carry errno,
    and the round-3 surviving guards each have a witness."""

    BLOCK_TIMEOUT = 10

    def run_main(self, out):
        code, err = self.main("--root", self.unit, "--out", out)
        lines = err.strip().splitlines()
        self.assertEqual(len(lines), 1, err)
        self.assertTrue(lines[0].startswith("record_split: refused: "), err)
        return code, err

    def test_getpath_error_is_a_refusal_naming_path_and_errno(self):
        # Calls 1-2 are the pre-write check (root, out parent); 3-4 come after the write.
        self.put("record.log", b"good\n")
        for call_no, written in ((1, False), (2, False), (3, True), (4, True)):
            with self.subTest(call=call_no):
                out = self.base / f"split{call_no}.json"
                with fail_call(R.fcntl, "fcntl", call_no) as calls:
                    code, err = self.run_main(out)
                self.assertEqual(len(calls), call_no)
                self.assertEqual(code, 2, err)
                self.assertIn("EIO", err)
                self.assertIn(str(self.unit if call_no in (1, 4) else self.base), err)
                self.assertEqual(out.exists(), written)
                if written:
                    self.assertIn(str(out), err)

    def test_close_error_is_a_refusal_and_keeps_the_written_output(self):
        # Closes in order: the output, its parent, the root. Each is after the write.
        self.put("record.log", b"good\n")
        for call_no, named in ((1, "split1.json"), (2, str(self.base)), (3, str(self.unit))):
            with self.subTest(call=call_no):
                out = self.base / f"split{call_no}.json"
                with fail_call(os, "close", call_no, after=True):
                    code, err = self.run_main(out)
                self.assertEqual(code, 2, err)
                self.assertIn("EIO", err)
                self.assertIn(named, err)
                self.assertIn(str(out), err)
                self.assertTrue(out.exists())  # never deleted
                self.assertEqual(json.loads(out.read_text())["leaves"][0]["path"], "record.log")

    def test_directory_close_error_is_a_refusal_naming_the_directory(self):
        (self.unit / "sub").mkdir()
        out = self.base / "split.json"
        with fail_call(os, "close", 1, after=True):
            code, err = self.run_main(out)
        self.assertEqual(code, 2, err)
        self.assertIn(f"{self.unit / 'sub'}: EIO", err)
        self.assertFalse(out.exists())

    def test_leaf_refusals_carry_the_errno_name(self):
        leaf = self.unit / "sample.bin"

        def to_symlink():
            leaf.unlink()
            leaf.symlink_to("missing")

        def enotdir(path, flags, *args, real=os.open, **kwargs):
            if path == "sample.bin" and kwargs.get("dir_fd") is not None:
                raise OSError(20, "Not a directory")
            return real(path, flags, *args, **kwargs)

        cases = {
            "ELOOP": lambda: before_open(lambda p, kw: p == "sample.bin" and "dir_fd" in kw, to_symlink),
            "ENOENT": lambda: before_open(lambda p, kw: p == "sample.bin" and "dir_fd" in kw, leaf.unlink),
            "ENOTDIR": lambda: mock.patch.object(os, "open", enotdir),
        }
        for name, hook in cases.items():
            with self.subTest(errno=name):
                self.put("sample.bin", b"\x00OWN")
                try:
                    with hook():
                        code, err = self.run_main(self.base / f"{name}.json")
                finally:
                    with contextlib.suppress(FileNotFoundError):
                        leaf.unlink()
                self.assertEqual(code, 2, err)
                self.assertIn("sample.bin", err)
                self.assertIn(f"[{name}]", err)

    def test_out_parent_that_is_a_fifo_refuses_without_blocking(self):  # M61
        self.put("record.log", b"good\n")
        fifo = self.base / "fifo-parent"
        os.mkfifo(fifo)
        proc = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(self.unit),
                               "--out", str(fifo / "out.json")],
                              capture_output=True, text=True, timeout=self.BLOCK_TIMEOUT)
        self.assertRefusedCleanly(proc)
        self.assertIn("ENOTDIR", proc.stderr)

    def test_directory_replaced_by_a_fifo_refuses_without_blocking(self):  # M70
        (self.unit / "sub").mkdir()
        out = self.base / "split.json"
        proc = subprocess.run([sys.executable, "-B", "-c", FIFO_FOR_DIRECTORY, str(TOOL),
                               str(self.unit), str(out)],
                              capture_output=True, text=True, timeout=self.BLOCK_TIMEOUT)
        self.assertRefusedCleanly(proc)
        self.assertIn("sub: ENOTDIR", proc.stderr)
        self.assertFalse(out.exists())

    def test_directory_on_another_device_refuses(self):  # M72
        (self.unit / "sub").mkdir()
        with fstat_reports(1, st_dev=1) as calls:
            with self.assertRaisesRegex(R.Refusal, "directory 'sub' changed during the walk"):
                self.split()
        self.assertEqual(len(calls), 1)

    def test_directory_fstat_error_is_a_refusal(self):  # M85
        (self.unit / "sub").mkdir()
        out = self.base / "split.json"
        with mock.patch.object(os, "fstat", side_effect=OSError(5, "Input/output error")):
            code, err = self.run_main(out)
        self.assertEqual(code, 2, err)
        self.assertIn(f"{self.unit / 'sub'}: EIO", err)
        self.assertFalse(out.exists())

    def test_non_oserror_from_the_scan_still_propagates(self):  # M93
        self.put("record.log", b"good\n")
        out = self.base / "split.json"
        with mock.patch.object(os, "scandir", side_effect=RuntimeError("not a filesystem error")):
            with self.assertRaisesRegex(RuntimeError, "not a filesystem error"):
                R.main(["--root", str(self.unit), "--out", str(out)])
        self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
